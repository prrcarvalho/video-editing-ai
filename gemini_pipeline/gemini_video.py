#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "gemini-webapi[browser]>=2.0",
#     "orjson",
#     "pyyaml>=6.0",
# ]
# ///
"""
Pipeline CLI: upload an mp4 to the Gemini web app (your account, via browser
cookies) and run a prompt template against it, writing the full response to a
markdown file.

Usage:
    uv run gemini_video.py analyze video.mp4
    uv run gemini_video.py analyze video.mp4 --prompt prompts/default.md --out outputs/
    uv run gemini_video.py analyze video.mp4 --model gemini-3-flash-thinking
    uv run gemini_video.py models          # list models your account can use

Auth: cookies are read from ~/.gemini_cookies.env (or GEMINI_1PSID /
GEMINI_1PSIDTS env vars, which take precedence) and rotated values are written
back to that file after every run. If the session is fully dead, re-harvest
with: uv run refresh_cookies.py. Last resort: browser-cookie3 auto-detection.
"""

import argparse
import asyncio
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml
from gemini_webapi import APIError, AuthError, GeminiClient, set_log_level

HERE = Path(__file__).resolve().parent
DEFAULT_PROMPT = HERE / "prompts" / "default.md"

COOKIE_ENV_PATH = Path(
    os.environ.get("GEMINI_COOKIE_ENV", "~/.gemini_cookies.env")
).expanduser()
DEFAULT_COOKIE_CACHE_DIR = Path.home() / ".cache" / "gemini_webapi"

VIDEO_FILENAME_PLACEHOLDER = "{{video_filename}}"
ANALYSIS_CONTEXT_PLACEHOLDER = "{{analysis_context}}"

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
COOKIE_ENV_LINE_RE = re.compile(
    r"^\s*(?:export\s+)?(GEMINI_1PSID|GEMINI_1PSIDTS)=(.*?)\s*$"
)


def load_template(path: Path) -> tuple[dict, str]:
    """Split a markdown prompt template into (frontmatter config, prompt body)."""
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if match:
        config = yaml.safe_load(match.group(1)) or {}
        body = text[match.end():]
    else:
        config, body = {}, text
    body = body.strip()
    if not body:
        sys.exit(f"error: prompt template {path} has an empty body")
    return config, body


def render_prompt(
    prompt_body: str,
    video_name: str,
    context_path_arg: str | None,
    context_required: bool = False,
) -> tuple[str, Path | None]:
    """Apply supported prompt-template substitutions."""
    prompt = prompt_body.replace(VIDEO_FILENAME_PLACEHOLDER, video_name)
    needs_context = ANALYSIS_CONTEXT_PLACEHOLDER in prompt

    if context_required and not context_path_arg:
        sys.exit(
            f"error: prompt template requires {ANALYSIS_CONTEXT_PLACEHOLDER}; "
            "pass --context PATH"
        )
    if context_path_arg and not needs_context:
        sys.exit(
            f"error: --context was supplied, but the prompt has no "
            f"{ANALYSIS_CONTEXT_PLACEHOLDER} placeholder"
        )
    if needs_context and not context_path_arg:
        sys.exit(
            f"error: prompt template contains {ANALYSIS_CONTEXT_PLACEHOLDER}; "
            "pass --context PATH"
        )
    if not context_path_arg:
        return prompt, None

    context_path = Path(context_path_arg).expanduser().resolve()
    if not context_path.is_file():
        sys.exit(f"error: analysis context file not found: {context_path}")
    context = context_path.read_text(encoding="utf-8").strip()
    if not context:
        sys.exit(f"error: analysis context file is empty: {context_path}")
    return prompt.replace(ANALYSIS_CONTEXT_PLACEHOLDER, context), context_path


def parse_cookie_env(path: Path) -> dict[str, str]:
    """Read GEMINI_1PSID / GEMINI_1PSIDTS from a `source`-able env file."""
    values: dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return values
    for line in text.splitlines():
        match = COOKIE_ENV_LINE_RE.match(line)
        if match:
            value = match.group(2)
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
                value = value[1:-1]
            values[match.group(1)] = value
    return values


def load_cookie_values() -> tuple[str | None, str | None]:
    """Env vars win (so `source` and one-off overrides still work), then the file."""
    psid = os.environ.get("GEMINI_1PSID")
    psidts = os.environ.get("GEMINI_1PSIDTS")
    if psid:
        return psid, psidts
    values = parse_cookie_env(COOKIE_ENV_PATH)
    return values.get("GEMINI_1PSID") or None, values.get("GEMINI_1PSIDTS") or None


def write_cookie_env(psid: str, psidts: str | None) -> None:
    """Atomically rewrite the cookie env file, mode 600, still `source`-able."""
    content = (
        "# Managed by gemini_video.py — auto-updated with rotated cookies after each run.\n"
        "# Recovery when the session is dead: uv run refresh_cookies.py\n"
        f"export GEMINI_1PSID='{psid}'\n"
        f"export GEMINI_1PSIDTS='{psidts or ''}'\n"
    )
    tmp = COOKIE_ENV_PATH.with_name(COOKIE_ENV_PATH.name + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        os.write(fd, content.encode("utf-8"))
    finally:
        os.close(fd)
    os.replace(tmp, COOKIE_ENV_PATH)


def cookie_from_jar(cookies, name: str) -> str | None:
    """Extract a cookie value from a curl_cffi Cookies object."""
    for cookie in cookies.jar:
        if cookie.name == name:
            return cookie.value
    return None


def reconcile_cache(psid: str, psidts: str | None) -> None:
    """If the env file was hand-refreshed, it wins: drop the library's cookie
    cache when its 1PSIDTS differs from the (non-empty) env-file value, since
    init() would otherwise prefer the stale cache and loop UNAUTHENTICATED."""
    cache_path = Path(os.environ["GEMINI_COOKIE_PATH"]) / f".cached_cookies_{psid}.json"
    if not cache_path.is_file():
        return
    try:
        cached = {c["name"]: c["value"] for c in json.loads(cache_path.read_text())}
        cached_psidts = cached.get("__Secure-1PSIDTS")
    except (OSError, ValueError, TypeError, KeyError):
        cache_path.unlink(missing_ok=True)
        return
    if psidts and cached_psidts and psidts != cached_psidts:
        cache_path.unlink(missing_ok=True)
        print(
            "[gemini_video] cookie env file was updated by hand; "
            "cleared stale library cookie cache",
            file=sys.stderr,
        )


def persist_cookies(
    client: GeminiClient, prev_psid: str | None, prev_psidts: str | None
) -> None:
    """Write the session's live (possibly rotated) cookies back to the env file."""
    try:
        psid = cookie_from_jar(client.cookies, "__Secure-1PSID")
        psidts = cookie_from_jar(client.cookies, "__Secure-1PSIDTS")
        if not psid:
            print(
                "[gemini_video] no __Secure-1PSID in session; cookie env file untouched",
                file=sys.stderr,
            )
            return
        if (psid, psidts) == (prev_psid, prev_psidts) and COOKIE_ENV_PATH.exists():
            return
        write_cookie_env(psid, psidts)
        action = (
            f"rotated __Secure-1PSIDTS persisted to {COOKIE_ENV_PATH}"
            if prev_psid
            else f"bootstrapped {COOKIE_ENV_PATH} from browser cookies"
        )
        print(f"[gemini_video] {action}", file=sys.stderr)
    except OSError as exc:
        print(f"[gemini_video] could not persist cookies: {exc}", file=sys.stderr)


def make_client() -> tuple[GeminiClient, str | None, str | None]:
    psid, psidts = load_cookie_values()
    if psid:
        reconcile_cache(psid, psidts)
        return GeminiClient(secure_1psid=psid, secure_1psidts=psidts), psid, psidts
    # browser-cookie3: reads cookies from local browser
    return GeminiClient(), None, None


async def fetch_versioned_names(client: GeminiClient) -> dict[str, str]:
    """Map model_id -> versioned display name (e.g. "3.5 Flash") from the raw
    GetUserStatus RPC. The library only reads fields [0..2] and maps ids to
    stale hardcoded names; the versioned name lives at field [11]."""
    from gemini_webapi.constants import GRPC
    from gemini_webapi.types import RPCData
    from gemini_webapi.utils import extract_json_from_response, get_nested_value
    import orjson

    response = await client._batch_execute(
        [RPCData(rpcid=GRPC.GET_USER_STATUS, payload="[]")]
    )
    names: dict[str, str] = {}
    for part in extract_json_from_response(response.text):
        part_body_str = get_nested_value(part, [2])
        if not part_body_str:
            continue
        part_body = orjson.loads(part_body_str)
        models_list = get_nested_value(part_body, [15])
        if not isinstance(models_list, list):
            continue
        for model_data in models_list:
            if isinstance(model_data, list) and model_data:
                model_id = get_nested_value(model_data, [0], "")
                versioned = get_nested_value(model_data, [11], "")
                if model_id and versioned:
                    names[model_id] = versioned
    return names


async def cmd_models(args: argparse.Namespace) -> None:
    client, prev_psid, prev_psidts = make_client()
    await client.init(timeout=60, auto_refresh=False, verbose=args.verbose)
    try:
        models = client.list_models()
        if not models:
            print("No dynamic model registry returned; predefined names:")
            from gemini_webapi.constants import Model

            for m in Model:
                if m is not Model.UNSPECIFIED:
                    print(f"  {m.model_name}")
            return
        versioned_names = await fetch_versioned_names(client)
        for m in models:
            tier = "advanced/plus" if m.advanced_only else "free"
            avail = "" if m.is_available else "  [NOT AVAILABLE on this account]"
            actual = versioned_names.get(m.model_id, m.display_name)
            print(f"  {m.model_name:36s} -> {actual} ({tier}){avail}")
            if args.verbose and m.description:
                print(f"      {m.description}")
    finally:
        await client.close()
        persist_cookies(client, prev_psid, prev_psidts)


async def cmd_analyze(args: argparse.Namespace) -> None:
    video = Path(args.video).expanduser().resolve()
    if not video.is_file():
        sys.exit(f"error: {video} is not a file")

    prompt_path = Path(args.prompt).expanduser()
    config, prompt_body = load_template(prompt_path)

    model = args.model or config.get("model", "gemini-3-flash-thinking")
    timeout = float(args.timeout or config.get("timeout", 900))
    prompt, context_path = render_prompt(
        prompt_body,
        video.name,
        args.context,
        context_required=bool(config.get("context_required")),
    )

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = out_dir / f"{video.stem}_{stamp}.md"

    client, prev_psid, prev_psidts = make_client()
    # Long timeout: video upload + analysis of a full clip can take minutes.
    await client.init(timeout=timeout, auto_refresh=False, verbose=args.verbose)
    try:
        print(f"model:  {model}")
        print(f"video:  {video} ({video.stat().st_size / 1e6:.1f} MB)")
        print("uploading and generating... (this can take a few minutes)")
        response = await client.generate_content(
            prompt,
            files=[video],
            model=model,
            temporary=args.temporary,
        )
    finally:
        await client.close()
        persist_cookies(client, prev_psid, prev_psidts)

    parts = [
        "---",
        f"video: {video.name}",
        f"model: {model}",
        f"prompt_template: {prompt_path}",
        f"generated_at: {stamp}",
    ]
    if context_path:
        parts.append(f"analysis_context: {context_path}")
    parts += ["---", ""]
    if response.thoughts and args.thoughts:
        parts += [
            "<details>",
            "<summary>Model thinking</summary>",
            "",
            response.thoughts.strip(),
            "",
            "</details>",
            "",
        ]
    parts.append(response.text.strip())
    out_path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"\nwrote {out_path}")


def attempt_cookie_recovery() -> bool:
    """Escalation rung 3: re-harvest cookies from the dedicated Chrome profile.
    A window opens briefly; on the very first use it waits for a Google login."""
    script = HERE / "refresh_cookies.py"
    if not script.is_file():
        print(f"[gemini_video] {script} not found; cannot auto-recover", file=sys.stderr)
        return False
    print(
        "[gemini_video] session is dead; re-harvesting cookies (a Chrome window "
        "will open briefly — if it shows a Google login, complete it)...",
        file=sys.stderr,
    )
    try:
        result = subprocess.run(["uv", "run", str(script)], cwd=HERE)
    except OSError as exc:
        print(f"[gemini_video] could not launch refresh_cookies.py: {exc}", file=sys.stderr)
        return False
    return result.returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="gemini_video", description="Gemini web-app video analysis pipeline"
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    p_analyze = sub.add_parser("analyze", help="upload an mp4 and run the prompt template")
    p_analyze.add_argument("video", help="path to the mp4 file")
    p_analyze.add_argument(
        "--prompt", default=str(DEFAULT_PROMPT), help="markdown prompt template (default: prompts/default.md)"
    )
    p_analyze.add_argument(
        "--context",
        help=(
            "markdown analysis context used to replace "
            f"{ANALYSIS_CONTEXT_PLACEHOLDER} in the prompt"
        ),
    )
    p_analyze.add_argument("--model", help="override model from the template frontmatter")
    p_analyze.add_argument("--out", default=str(HERE / "outputs"), help="output directory")
    p_analyze.add_argument("--timeout", type=float, help="request timeout in seconds")
    p_analyze.add_argument(
        "--temporary", action="store_true", help="keep the chat out of your Gemini history"
    )
    p_analyze.add_argument(
        "--no-thoughts", dest="thoughts", action="store_false",
        help="omit the model's thinking trace from the output file",
    )
    p_analyze.set_defaults(func=cmd_analyze)

    p_models = sub.add_parser("models", help="list models available to your account")
    p_models.set_defaults(func=cmd_models)

    args = parser.parse_args()
    set_log_level("DEBUG" if args.verbose else "WARNING")
    # Durable, user-controlled location for the library's rotated-cookie cache
    # (default is volatile $TMPDIR). setdefault keeps explicit overrides working.
    os.environ.setdefault("GEMINI_COOKIE_PATH", str(DEFAULT_COOKIE_CACHE_DIR))
    Path(os.environ["GEMINI_COOKIE_PATH"]).mkdir(parents=True, exist_ok=True)
    try:
        asyncio.run(args.func(args))
    except (AuthError, APIError) as exc:
        # AuthError = cookies rejected at init. APIError 1100 = session half-dead:
        # read RPCs still work but uploads/generation fail. Both mean rotation
        # can't save us — escalate to a full cookie re-harvest, then retry once.
        if isinstance(exc, APIError) and "1100" not in str(exc):
            raise
        if not attempt_cookie_recovery():
            if args.verbose:
                raise
            sys.exit(
                "error: Gemini session is dead and automatic recovery failed. "
                "Run by hand: uv run refresh_cookies.py"
            )
        # The refreshed env file must win the retry, so drop any stale env vars
        # (they take precedence over the file in load_cookie_values).
        os.environ.pop("GEMINI_1PSID", None)
        os.environ.pop("GEMINI_1PSIDTS", None)
        print("[gemini_video] cookies re-harvested; retrying...", file=sys.stderr)
        asyncio.run(args.func(args))


if __name__ == "__main__":
    main()
