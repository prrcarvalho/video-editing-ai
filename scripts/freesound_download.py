#!/usr/bin/env python3
"""Freesound OAuth login and original-file downloader.

This complements the Freesound MCP server, which is used for catalog search.
Original-quality downloads require Freesound OAuth2, so downloads live here as a
repo-local, agent-agnostic CLI that Codex, Claude Code, OpenCode, or a human can
all call the same way.
"""

from __future__ import annotations

import argparse
import email.message
import json
import os
import re
import secrets
import shlex
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any


API_BASE = "https://freesound.org/apiv2"
DEFAULT_TOKEN_FILE = Path.home() / ".config" / "video_editing_ai" / "freesound-oauth.json"
DEFAULT_ENV_FILE = Path.home() / ".config" / "video_editing_ai" / "freesound.env"
DEFAULT_OUT_DIR = Path("assets/sfx/freesound")
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_REDIRECT_URI = "http://freesound.org/home/app_permissions/permission_granted/"
SOUND_FIELDS = ",".join(
    [
        "id",
        "name",
        "username",
        "license",
        "url",
        "type",
        "duration",
        "filesize",
        "previews",
        "tags",
    ]
)


class FreesoundError(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")
    tmp_path.replace(path)
    if mode is not None:
        path.chmod(mode)


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line.removeprefix("export ").strip()
        if "=" not in line:
            continue
        key, raw_value = line.split("=", 1)
        key = key.strip()
        if not key or key in os.environ:
            continue
        try:
            value = shlex.split(raw_value, posix=True)[0]
        except (IndexError, ValueError):
            value = raw_value.strip().strip("\"'")
        os.environ[key] = value


def request_json(url: str, headers: dict[str, str] | None = None, data: dict[str, str] | None = None) -> dict[str, Any]:
    encoded = None
    if data is not None:
        encoded = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=encoded, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise FreesoundError(f"Freesound HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise FreesoundError(f"Freesound request failed: {exc.reason}") from exc


def post_token(data: dict[str, str]) -> dict[str, Any]:
    token = request_json(f"{API_BASE}/oauth2/access_token/", data=data)
    token["expires_at"] = int(time.time()) + int(token.get("expires_in", 0))
    token["created_at"] = now_iso()
    return token


def oauth_login(args: argparse.Namespace) -> None:
    client_id = require_env("FREESOUND_CLIENT_ID")
    client_secret = require_env("FREESOUND_CLIENT_SECRET")
    redirect_uri = args.redirect_uri
    state = secrets.token_urlsafe(24)
    parsed = urllib.parse.urlparse(redirect_uri)
    local_callback = parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"}

    result: dict[str, str] = {}

    class CallbackHandler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *handler_args: object) -> None:
            return

        def do_GET(self) -> None:
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            result["code"] = query.get("code", [""])[0]
            result["state"] = query.get("state", [""])[0]
            result["error"] = query.get("error", [""])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            if result.get("code"):
                self.wfile.write(b"Freesound OAuth complete. You can close this tab.")
            else:
                self.wfile.write(b"Freesound OAuth failed. Return to the terminal.")

    auth_url = f"{API_BASE}/oauth2/authorize/?" + urllib.parse.urlencode(
        {"client_id": client_id, "response_type": "code", "state": state}
    )
    print(f"Opening Freesound authorization URL:\n{auth_url}\n")
    if not webbrowser.open(auth_url):
        print("Open the URL above in your browser.", file=sys.stderr)

    if local_callback:
        server = HTTPServer((parsed.hostname or "127.0.0.1", parsed.port or 8765), CallbackHandler)
        server.handle_request()
        server.server_close()
    else:
        print("After authorizing, Freesound will show an authorization code on the fallback page.")
        result["code"] = args.code or input("Paste Freesound authorization code: ").strip()
        result["state"] = state

    if result.get("error"):
        raise FreesoundError(f"OAuth denied: {result['error']}")
    if not result.get("code") or result.get("state") != state:
        raise FreesoundError("OAuth callback did not include a valid code/state")

    token = post_token(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": result["code"],
        }
    )
    token["redirect_uri"] = redirect_uri
    write_json(args.token_file, token, mode=0o600)
    print(f"Saved Freesound OAuth token to {args.token_file}")


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise FreesoundError(f"Missing required environment variable: {name}")
    return value


def load_token(path: Path) -> dict[str, Any]:
    token = load_json(path, {})
    if not token.get("access_token"):
        env_token = os.environ.get("FREESOUND_ACCESS_TOKEN")
        if env_token:
            return {"access_token": env_token, "expires_at": 0}
        raise FreesoundError(f"No OAuth token found. Run: {Path(__file__).name} login")
    return token


def ensure_access_token(path: Path) -> str:
    token = load_token(path)
    expires_at = int(token.get("expires_at") or 0)
    if expires_at and expires_at - int(time.time()) < 120 and token.get("refresh_token"):
        client_id = require_env("FREESOUND_CLIENT_ID")
        client_secret = require_env("FREESOUND_CLIENT_SECRET")
        refreshed = post_token(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "refresh_token",
                "refresh_token": str(token["refresh_token"]),
            }
        )
        if "refresh_token" not in refreshed:
            refreshed["refresh_token"] = token["refresh_token"]
        write_json(path, refreshed, mode=0o600)
        token = refreshed
    return str(token["access_token"])


def auth_headers(access_token: str | None = None, api_key: str | None = None) -> dict[str, str]:
    if access_token:
        return {"Authorization": f"Bearer {access_token}"}
    if api_key:
        return {"Authorization": f"Token {api_key}"}
    return {}


def get_sound_metadata(sound_id: int, access_token: str | None = None) -> dict[str, Any]:
    api_key = os.environ.get("FREESOUND_API_KEY")
    query = urllib.parse.urlencode({"fields": SOUND_FIELDS})
    return request_json(f"{API_BASE}/sounds/{sound_id}/?{query}", headers=auth_headers(access_token, api_key))


def safe_slug(value: str, fallback: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip(".-_")
    return slug[:96] or fallback


def filename_from_headers(headers: email.message.Message) -> str | None:
    disposition = headers.get("Content-Disposition")
    if not disposition:
        return None
    match = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)"?', disposition)
    if not match:
        return None
    return urllib.parse.unquote(match.group(1))


def download_original(sound_id: int, access_token: str, out_path: Path) -> None:
    url = f"{API_BASE}/sounds/{sound_id}/download/"
    req = urllib.request.Request(url, headers=auth_headers(access_token))
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with out_path.open("wb") as f:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
            header_name = filename_from_headers(response.headers)
            if header_name and out_path.name == f"freesound-{sound_id}":
                renamed = out_path.with_name(safe_slug(header_name, out_path.name))
                out_path.replace(renamed)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise FreesoundError(f"Download failed with HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise FreesoundError(f"Download failed: {exc.reason}") from exc


def manifest_entry(path: Path, metadata: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    license_name = str(metadata.get("license", ""))
    attribution_required = "zero" not in license_name.lower() and "cc0" not in license_name.lower()
    return {
        "file": path.as_posix(),
        "source": "freesound",
        "sound_id": metadata.get("id"),
        "name": metadata.get("name"),
        "username": metadata.get("username"),
        "url": metadata.get("url"),
        "license": license_name,
        "attribution_required": attribution_required,
        "duration": metadata.get("duration"),
        "type": metadata.get("type"),
        "filesize": metadata.get("filesize"),
        "tags": metadata.get("tags", []),
        "usage": args.usage,
        "description": args.description,
        "downloaded_at": now_iso(),
    }


def upsert_manifest(path: Path, entry: dict[str, Any]) -> None:
    manifest = load_json(path, {"clips": []})
    clips = manifest.setdefault("clips", [])
    clips[:] = [clip for clip in clips if clip.get("sound_id") != entry.get("sound_id")]
    clips.append(entry)
    write_json(path, manifest)


def download(args: argparse.Namespace) -> None:
    access_token = ensure_access_token(args.token_file)
    metadata = get_sound_metadata(args.sound_id, access_token)
    ext = str(metadata.get("type") or "audio").lower().lstrip(".")
    basename = args.filename or f"freesound-{args.sound_id}-{safe_slug(str(metadata.get('name', 'sound')), 'sound')}.{ext}"
    out_path = args.out_dir / basename
    if out_path.exists() and not args.force:
        raise FreesoundError(f"Refusing to overwrite existing file: {out_path} (use --force)")
    download_original(args.sound_id, access_token, out_path)
    if not out_path.exists():
        matches = sorted(args.out_dir.glob(f"freesound-{args.sound_id}*"))
        out_path = matches[-1] if matches else out_path
    entry = manifest_entry(out_path, metadata, args)
    upsert_manifest(args.manifest, entry)
    print(json.dumps(entry, indent=2, sort_keys=True))


def show_status(args: argparse.Namespace) -> None:
    token = load_json(args.token_file, {})
    if not token:
        print(f"No token file at {args.token_file}")
        return
    expires_at = int(token.get("expires_at") or 0)
    expires = datetime.fromtimestamp(expires_at, tz=timezone.utc).isoformat() if expires_at else "unknown"
    print(json.dumps({"token_file": str(args.token_file), "expires_at": expires, "has_refresh_token": bool(token.get("refresh_token"))}, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Freesound OAuth downloader for the Asset KB")
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_FILE)
    parser.add_argument("--token-file", type=Path, default=DEFAULT_TOKEN_FILE)
    subparsers = parser.add_subparsers(dest="command", required=True)

    login_parser = subparsers.add_parser("login", help="Authorize Freesound OAuth2 and store a local token")
    login_parser.add_argument("--redirect-uri", default=DEFAULT_REDIRECT_URI)
    login_parser.add_argument("--code", help="Authorization code from Freesound's fallback page")
    login_parser.set_defaults(func=oauth_login)

    status_parser = subparsers.add_parser("status", help="Show local OAuth token status")
    status_parser.set_defaults(func=show_status)

    download_parser = subparsers.add_parser("download", help="Download an original Freesound asset")
    download_parser.add_argument("sound_id", type=int)
    download_parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    download_parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    download_parser.add_argument("--filename")
    download_parser.add_argument("--usage", default="")
    download_parser.add_argument("--description", default="")
    download_parser.add_argument("--force", action="store_true")
    download_parser.set_defaults(func=download)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    load_env_file(args.env_file)
    try:
        args.func(args)
    except FreesoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
