#!/usr/bin/env python3
"""Scaffold and validate browser B-roll demo artifacts.

This creates the repo-standard files for a deterministic browser-demo
Screencast Asset Segment. It intentionally does not run browser automation;
the generated `replay.mjs` is reviewed and then executed with
`playwright-cli-patched run-code --filename replay.mjs`.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VIEWPORT = {"width": 1080, "height": 1920, "device_scale_factor": 1}
DEFAULT_DURATION_SECONDS = 6.0
VALID_ACTIONS = {
    "goto",
    "click",
    "fill",
    "type",
    "press",
    "hover",
    "drag",
    "scroll",
    "wait",
    "snapshot",
    "assert_visible",
}
VALID_PROFILE_POLICIES = {"demo_profile", "saved_storage_state", "real_chrome", "no_login"}


class SpecError(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SpecError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SpecError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SpecError(f"{path}: expected a JSON object")
    return data


def write_json(path: Path, data: dict[str, Any], force: bool = False) -> None:
    if path.exists() and not force:
        raise SpecError(f"refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, force: bool = False) -> None:
    if path.exists() and not force:
        raise SpecError(f"refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def require_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SpecError(f"missing required string field: {key}")
    return value


def require_number(data: dict[str, Any], key: str) -> float:
    value = data.get(key)
    if not isinstance(value, (int, float)) or value <= 0:
        raise SpecError(f"missing positive number field: {key}")
    return float(value)


def validate_viewport(value: Any) -> None:
    if not isinstance(value, dict):
        raise SpecError("viewport must be an object")
    for key in ("width", "height"):
        if not isinstance(value.get(key), int) or value[key] < 320:
            raise SpecError(f"viewport.{key} must be an integer >= 320")
    scale = value.get("device_scale_factor", 1)
    if not isinstance(scale, (int, float)) or scale < 1:
        raise SpecError("viewport.device_scale_factor must be >= 1")


def validate_privacy_mode(value: Any) -> str:
    if not isinstance(value, dict):
        raise SpecError("privacy_mode must be an object")
    policy = value.get("profile_policy")
    if policy not in VALID_PROFILE_POLICIES:
        raise SpecError(f"privacy_mode.profile_policy must be one of {sorted(VALID_PROFILE_POLICIES)}")
    if value.get("store_private_evidence") is not False:
        raise SpecError("privacy_mode.store_private_evidence must default to false for reusable demos")
    return str(policy)


def validate_step(step: Any, index: int) -> list[str]:
    if not isinstance(step, dict):
        raise SpecError(f"steps[{index}] must be an object")
    step_id = step.get("step_id")
    if not isinstance(step_id, str) or not step_id:
        raise SpecError(f"steps[{index}].step_id is required")
    action = step.get("action")
    if action not in VALID_ACTIONS:
        raise SpecError(f"{step_id}: action must be one of {sorted(VALID_ACTIONS)}")

    warnings: list[str] = []
    if action in {"click", "fill", "type", "hover", "drag", "assert_visible"} and not step.get("locator"):
        warnings.append(f"{step_id}: interactive action has no locator")
    if action == "drag" and not step.get("to_locator"):
        warnings.append(f"{step_id}: drag action has no to_locator")
    if action == "goto" and not step.get("url"):
        warnings.append(f"{step_id}: goto will use top-level target_url")
    if action in {"click", "drag"} and step.get("cursor_behavior") in {None, "none"}:
        warnings.append(f"{step_id}: click/drag has no visible cursor_behavior")
    if action in {"click", "drag"} and not step.get("zoom_behavior"):
        warnings.append(f"{step_id}: click/drag has no zoom_behavior")
    return warnings


def validate_spec(spec: dict[str, Any]) -> list[str]:
    if spec.get("artifact_type") != "DemoRunSpec":
        raise SpecError("artifact_type must be DemoRunSpec")
    require_string(spec, "version")
    require_string(spec, "recreation_slug")
    require_string(spec, "shot_id")
    require_string(spec, "target_url")
    require_number(spec, "duration_seconds")
    validate_viewport(spec.get("viewport"))
    validate_privacy_mode(spec.get("privacy_mode"))

    rows = spec.get("beat_sheet_row_ids")
    if not isinstance(rows, list) or not rows or not all(isinstance(row, str) and row for row in rows):
        raise SpecError("beat_sheet_row_ids must be a non-empty string array")

    steps = spec.get("steps")
    if not isinstance(steps, list) or not steps:
        raise SpecError("steps must be a non-empty array")

    warnings: list[str] = []
    seen_ids: set[str] = set()
    for index, step in enumerate(steps):
        step_warnings = validate_step(step, index)
        step_id = step["step_id"]
        if step_id in seen_ids:
            raise SpecError(f"duplicate step_id: {step_id}")
        seen_ids.add(step_id)
        warnings.extend(step_warnings)
    return warnings


def default_spec(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "artifact_type": "DemoRunSpec",
        "version": "v001",
        "recreation_slug": args.recreation_slug,
        "shot_id": args.shot_id,
        "target_url": args.target_url,
        "viewport": DEFAULT_VIEWPORT,
        "duration_seconds": args.duration_seconds,
        "beat_sheet_row_ids": args.beat_row,
        "automation_tool": "playwright-cli-patched",
        "renderer": "hyperframes",
        "privacy_mode": {
            "profile_policy": args.profile_policy,
            "store_private_evidence": False,
            "requires_action_approval": True,
            "redaction_notes": [],
        },
        "wait_conditions": [{"kind": "load_state", "value": "domcontentloaded", "timeout_ms": 10000}],
        "steps": [
            {
                "step_id": "step_001_open",
                "action": "goto",
                "url": args.target_url,
                "pause_after_ms": 800,
                "caption_cue": "open the page",
            },
            {
                "step_id": "step_002_snapshot",
                "action": "snapshot",
                "pause_after_ms": 300,
                "caption_cue": "show the starting state",
            },
        ],
        "visual_treatment": {
            "caption_style": "mute-first keyword captions",
            "output_aspect_ratio": "9:16",
            "output_resolution": DEFAULT_VIEWPORT,
            "sfx_policy": "click cues within 100ms of visible action",
            "cursor": {"keyframes": [], "click_ripples": [], "zoom_boxes": []},
            "notes": "Add cursor and zoom cues after locators and target bounds are known.",
        },
        "acceptance_notes": [
            "Replay three times with the same user-visible states and comparable duration.",
            "Styled output must keep the target UI unobscured at 1080x1920.",
        ],
    }


def js_string(value: str) -> str:
    return json.dumps(value)


def generate_replay_script(spec: dict[str, Any]) -> str:
    viewport = spec["viewport"]
    lines = [
        "async page => {",
        "  const path = await import('node:path');",
        "  await page.setViewportSize({ width: %d, height: %d });" % (viewport["width"], viewport["height"]),
        "  await page.screencast?.start?.({ path: path.join('raw', 'browser_capture.webm'), size: { width: %d, height: %d } });"
        % (viewport["width"], viewport["height"]),
        "",
        "  const pause = ms => page.waitForTimeout(ms);",
        "  const locatorFor = value => value && value.startsWith('getBy')",
        "    ? Function('page', `return page.${value}`)(page)",
        "    : page.locator(value);",
        "  const cue = async (text, duration = 900) => {",
        "    if (!text || !page.screencast?.showOverlay) return;",
        "    await page.screencast.showOverlay(`",
        "      <div style=\"position:absolute;left:36px;bottom:42px;padding:10px 14px;",
        "        border-radius:8px;background:rgba(0,0,0,.72);color:white;",
        "        font:600 18px system-ui,sans-serif;letter-spacing:0;\">${text}</div>`",
        "    , { duration });",
        "  };",
        "",
    ]

    for step in spec["steps"]:
        step_id = step["step_id"]
        action = step["action"]
        pause_after = int(step.get("pause_after_ms", 250))
        caption = step.get("caption_cue", "")
        lines.append(f"  // {step_id}: {action}")
        if caption:
            lines.append(f"  await cue({js_string(caption)});")

        if action == "goto":
            lines.append(f"  await page.goto({js_string(step.get('url') or spec['target_url'])});")
        elif action == "click":
            lines.append(f"  await locatorFor({js_string(step.get('locator', 'body'))}).click();")
        elif action == "fill":
            lines.append(
                f"  await locatorFor({js_string(step.get('locator', 'body'))}).fill({js_string(step.get('text', ''))});"
            )
        elif action == "type":
            lines.append(
                f"  await locatorFor({js_string(step.get('locator', 'body'))}).pressSequentially({js_string(step.get('text', ''))}, {{ delay: 55 }});"
            )
        elif action == "press":
            if step.get("locator"):
                lines.append(f"  await locatorFor({js_string(step['locator'])}).press({js_string(step.get('key', 'Enter'))});")
            else:
                lines.append(f"  await page.keyboard.press({js_string(step.get('key', 'Enter'))});")
        elif action == "hover":
            lines.append(f"  await locatorFor({js_string(step.get('locator', 'body'))}).hover();")
        elif action == "drag":
            lines.append(
                f"  await locatorFor({js_string(step.get('locator', 'body'))}).dragTo(locatorFor({js_string(step.get('to_locator', 'body'))}));"
            )
        elif action == "scroll":
            lines.append(f"  await page.mouse.wheel({int(step.get('scroll_x', 0))}, {int(step.get('scroll_y', 0))});")
        elif action == "wait":
            lines.append(f"  await pause({pause_after});")
        elif action == "snapshot":
            lines.append(f"  await page.screenshot({{ path: path.join('snapshots', {js_string(step_id + '.png')}) }});")
        elif action == "assert_visible":
            lines.append(f"  await locatorFor({js_string(step.get('locator', 'body'))}).waitFor({{ state: 'visible' }});")

        if step.get("expected_url_contains"):
            expected_url = str(step["expected_url_contains"])
            message = f"Expected URL to contain {expected_url}"
            lines.append(
                f"  if (!page.url().includes({js_string(expected_url)})) throw new Error({js_string(message)});"
            )
        if step.get("expected_text"):
            lines.append(f"  await page.getByText({js_string(step['expected_text'])}).waitFor();")
        if action != "wait" and pause_after:
            lines.append(f"  await pause({pause_after});")
        lines.append("")

    lines.extend(
        [
            "  await page.screencast?.stop?.();",
            "}",
            "",
        ]
    )
    return "\n".join(lines)


def manifest_for(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "AutomationRunManifest",
        "version": spec.get("version", "v001"),
        "recreation_slug": spec["recreation_slug"],
        "shot_id": spec["shot_id"],
        "created_at": now_iso(),
        "tool_versions": {
            "playwright-cli-patched": "pending",
            "hyperframes": "pending",
        },
        "demo_run_spec_path": "demo_run_spec.json",
        "replay_script_path": "replay.mjs",
        "raw_recording_path": "raw/browser_capture.webm",
        "styled_render_path": "styled/screencast_asset_segment.mp4",
        "trace_paths": [],
        "snapshot_paths": [],
        "network_evidence_paths": [],
        "profile_policy": spec["privacy_mode"]["profile_policy"],
        "redaction_notes": spec["privacy_mode"].get("redaction_notes", []),
        "approval_status": "draft",
    }


def asset_segment_for(spec: dict[str, Any]) -> dict[str, Any]:
    asset_id = f"{spec['recreation_slug']}_{spec['shot_id']}_screencast_v001"
    return {
        "artifact_type": "ScreencastAssetSegment",
        "version": spec.get("version", "v001"),
        "asset_segment_id": asset_id,
        "recreation_slug": spec["recreation_slug"],
        "shot_id": spec["shot_id"],
        "source_manifest_path": "automation_run_manifest.json",
        "media_path": "styled/screencast_asset_segment.mp4",
        "duration_seconds": spec["duration_seconds"],
        "reuse_notes": [],
        "license_or_rights": "owned/generated demo capture",
    }


def hyperframes_notes_for(spec: dict[str, Any]) -> str:
    rows = ", ".join(spec["beat_sheet_row_ids"])
    return f"""# HyperFrames Notes

Recreation: `{spec['recreation_slug']}`
Shot ID: `{spec['shot_id']}`
Beat Sheet rows: `{rows}`

Use `styled/screencast_asset_segment.mp4` as the approved screencast source for
this Beat Sheet slot after review.

Composition expectations:

- Preserve the user-visible UI target from `demo_run_spec.json`.
- Add or keep synthetic cursor/click/drag/zoom layers only when they clarify the action.
- Keep captions and cursor clear of the target UI in a 1080x1920 frame.
- Land click SFX within about 100ms of the visible click state change.
- Update `automation_run_manifest.json` with final trace, snapshot, network, and render paths.
"""


def command_new_spec(args: argparse.Namespace) -> int:
    spec = default_spec(args)
    validate_spec(spec)
    write_json(args.out, spec, force=args.force)
    print(f"wrote {args.out}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    spec = read_json(args.spec)
    warnings = validate_spec(spec)
    print(f"{args.spec}: valid DemoRunSpec")
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    return 0


def command_scaffold(args: argparse.Namespace) -> int:
    spec = read_json(args.spec)
    warnings = validate_spec(spec)
    base = args.root / "recreations" / spec["recreation_slug"] / "assets" / "screencasts" / spec["shot_id"]
    for dirname in ("raw", "styled", "traces", "snapshots", "network"):
        (base / dirname).mkdir(parents=True, exist_ok=True)

    write_json(base / "demo_run_spec.json", spec, force=args.force)
    write_json(base / "automation_run_manifest.json", manifest_for(spec), force=args.force)
    write_json(base / "screencast_asset_segment.json", asset_segment_for(spec), force=args.force)
    write_text(base / "replay.mjs", generate_replay_script(spec), force=args.force)
    write_text(base / "hyperframes_notes.md", hyperframes_notes_for(spec), force=args.force)

    print(f"scaffolded {base}")
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_spec = subparsers.add_parser("new-spec", help="write a starter DemoRunSpec")
    new_spec.add_argument("recreation_slug")
    new_spec.add_argument("shot_id")
    new_spec.add_argument("--target-url", required=True)
    new_spec.add_argument("--beat-row", action="append", required=True)
    new_spec.add_argument("--duration-seconds", type=float, default=DEFAULT_DURATION_SECONDS)
    new_spec.add_argument(
        "--profile-policy",
        choices=sorted(VALID_PROFILE_POLICIES),
        default="demo_profile",
    )
    new_spec.add_argument("--out", type=Path, required=True)
    new_spec.add_argument("--force", action="store_true")
    new_spec.set_defaults(func=command_new_spec)

    validate = subparsers.add_parser("validate", help="validate a DemoRunSpec")
    validate.add_argument("spec", type=Path)
    validate.set_defaults(func=command_validate)

    scaffold = subparsers.add_parser("scaffold", help="create the Screencast Asset Segment folder")
    scaffold.add_argument("spec", type=Path)
    scaffold.add_argument("--root", type=Path, default=REPO_ROOT)
    scaffold.add_argument("--force", action="store_true")
    scaffold.set_defaults(func=command_scaffold)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except SpecError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
