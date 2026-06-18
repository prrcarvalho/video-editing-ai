#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-genai>=2.8.0",
#     "pyyaml>=6.0",
# ]
# ///
"""
Official Gemini SDK video evidence extractor.

This script is intentionally separate from gemini_video.py. The existing
gemini_video.py talks to the Gemini web app through cookies and can produce
human-facing analyses. This script talks to the official Gemini API and is
limited to visual evidence extraction for fast-paced Exemplar videos.

Gemini's job here is "what is visibly happening?" The downstream Codex/GPT
reasoning stage decides "why did it work?" and how to recreate the Pattern.
"""

from __future__ import annotations

import argparse
import copy
import json
import mimetypes
import os
import re
import shlex
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent

DEFAULT_MODEL = "gemini-3.5-flash"
DEFAULT_SURVEY_PROMPT = HERE / "prompts" / "PROMPT-GEMINI-SDK-VISUAL-SURVEY.md"
DEFAULT_MICRO_PROMPT = HERE / "prompts" / "PROMPT-GEMINI-SDK-MICRO-EFFECTS.md"
DEFAULT_CODEX_PROMPT = HERE / "prompts" / "PROMPT-CODEX-VIRAL-REASONING.md"
DEFAULT_API_KEY_ENV_FILES = [
    Path.home() / "gemini_api_key.env",
    Path.home() / ".gemini_api_key.env",
]

VIDEO_FILENAME_PLACEHOLDER = "{{video_filename}}"
ANALYSIS_CONTEXT_PLACEHOLDER = "{{analysis_context}}"
SPAN_CONTEXT_PLACEHOLDER = "{{span_context}}"
VISUAL_EVIDENCE_PLACEHOLDER = "{{visual_evidence_context}}"

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
JSON_FENCE_RE = re.compile(r"\A\s*```(?:json)?\s*(.*?)\s*```\s*\Z", re.DOTALL)

PROSODY_CONTEXT_KEYS = [
    "F0semitoneFrom27.5Hz_sma3nz_amean",
    "F0semitoneFrom27.5Hz_sma3nz_stddevNorm",
    "F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2",
    "loudness_sma3_amean",
    "loudness_sma3_stddevNorm",
    "loudness_sma3_pctlrange0-2",
    "loudnessPeaksPerSec",
    "jitterLocal_sma3nz_amean",
    "shimmerLocaldB_sma3nz_amean",
]

MECHANIC_FAMILIES = [
    "cut_boundary",
    "transition",
    "framing_motion",
    "camera_motion",
    "speed_time",
    "caption_text",
    "graphic_overlay",
    "vfx_compositing",
    "screen_ui_interaction",
    "color_light",
    "audio_visual_sync",
    "layout_layering",
    "other",
]

LAYOUT_TYPES = [
    "talking_head",
    "screen_recording",
    "split_screen",
    "picture_in_picture",
    "facecam_over_screen",
    "talking_head_over_broll",
    "graphic_card",
    "ui_demo",
    "mixed",
    "other",
]

SURFACE_ROLES = [
    "talking_head",
    "facecam",
    "screen_recording",
    "browser_ui",
    "app_ui",
    "mobile_ui",
    "caption_layer",
    "title_layer",
    "callout_layer",
    "cursor_pointer",
    "click_indicator",
    "b_roll",
    "graphic_card",
    "background_plate",
    "progress_bar",
    "sticker_emoji",
    "other",
]

EDIT_MECHANIC_TYPES = [
    "hard_cut",
    "candidate_cut",
    "jump_cut",
    "match_cut",
    "cut_on_action",
    "smash_cut",
    "whip_pan_cut",
    "invisible_cut",
    "false_cut",
    "layout_only_cut",
    "overlay_only_cut",
    "cross_dissolve",
    "dip_to_black",
    "dip_to_white",
    "fade_in",
    "fade_out",
    "wipe",
    "slide_transition",
    "zoom_transition",
    "morph_transition",
    "glitch_transition",
    "flash_transition",
    "punch_in",
    "punch_out",
    "slow_push_in",
    "slow_pull_out",
    "zoom_ramp",
    "digital_zoom",
    "crop_shift",
    "reframe",
    "resize",
    "rotate",
    "camera_pan",
    "camera_tilt",
    "handheld_shake",
    "stabilization_snap",
    "parallax_motion",
    "object_tracking",
    "face_tracking",
    "speed_ramp",
    "slow_motion",
    "freeze_frame",
    "frame_hold",
    "timelapse",
    "time_remap",
    "stutter_cut",
    "repeated_frame",
    "reversed_motion",
    "full_caption",
    "keyword_caption",
    "word_by_word_caption",
    "active_word_highlight",
    "karaoke_caption",
    "caption_pop",
    "caption_slide",
    "caption_bounce",
    "caption_color_emphasis",
    "caption_size_pop",
    "title_card",
    "lower_third",
    "text_hook",
    "text_callout",
    "counter_timer",
    "progress_bar",
    "arrow_callout",
    "circle_highlight",
    "box_highlight",
    "sticker_pop",
    "emoji_pop",
    "icon_pop",
    "image_overlay",
    "b_roll_insert",
    "graphic_card",
    "diagram_overlay",
    "background_replacement",
    "border_frame",
    "split_screen_change",
    "picture_in_picture_change",
    "cursor_motion",
    "click_indicator",
    "tap_indicator",
    "pointer_highlight",
    "selection_highlight",
    "typing_indicator",
    "text_field_focus",
    "scroll",
    "swipe",
    "drag",
    "hover_state",
    "menu_open",
    "modal_popup",
    "app_state_change",
    "browser_tab_change",
    "blur_effect",
    "motion_blur",
    "glow_effect",
    "flash",
    "lens_flare",
    "light_leak",
    "color_punch",
    "color_grade_shift",
    "exposure_pulse",
    "vignette",
    "mask_reveal",
    "track_matte",
    "rotoscope_mask",
    "green_screen_composite",
    "glitch_effect",
    "chromatic_aberration",
    "noise_grain",
    "depth_of_field_shift",
    "focus_pull",
    "beat_synced_cut",
    "sfx_hit_sync",
    "whoosh_transition",
    "riser_sync",
    "silence_drop",
    "bass_drop_sync",
    "voice_emphasis_sync",
    "prosody_spike_sync",
    "no_visible_change",
    "other",
]

MOTION_DIRECTIONS = [
    "none",
    "in",
    "out",
    "left",
    "right",
    "up",
    "down",
    "clockwise",
    "counterclockwise",
    "mixed",
    "unknown",
]

MOTION_PROFILES = [
    "none",
    "linear",
    "ease_in",
    "ease_out",
    "ease_in_out",
    "snap",
    "ramp",
    "bounce",
    "elastic",
    "handheld",
    "unknown",
]

INTENSITY_LEVELS = ["none", "subtle", "medium", "strong", "unknown"]

DURATION_CLASSES = [
    "flash_1_4_frames",
    "micro_under_250ms",
    "short_250_750ms",
    "beat_750_1500ms",
    "sustained_over_1500ms",
    "unknown",
]

SYNC_KINDS = [
    "none",
    "word_sync",
    "beat_sync",
    "onset_sync",
    "sfx_hit_sync",
    "cut_sync",
    "prosody_sync",
    "silence_drop_sync",
    "riser_sync",
    "caption_sync",
    "unclear",
]

CRAFT_FUNCTIONS = [
    "pattern_interrupt",
    "beat_sync",
    "caption_emphasis",
    "reveal_accent",
    "layout_orientation",
    "cognitive_load_reduction",
    "interaction_focus",
    "tension_build",
    "payoff_marker",
    "motion_continuity",
    "information_chunking",
    "unclear",
]

HYPOTHESIS_BASES = ["visible_only", "visible_plus_audio_signal", "weak_inference"]


def load_template(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if match:
        config = yaml.safe_load(match.group(1)) or {}
        body = text[match.end():]
    else:
        config, body = {}, text
    body = body.strip()
    if not body:
        sys.exit(f"error: prompt template is empty: {path}")
    return config, body


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {path}")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    print(f"wrote {path}")


def update_run_manifest(out_dir: Path, data: dict[str, Any]) -> None:
    path = out_dir / "run_manifest.json"
    existing = read_json(path, {})
    existing.update(
        {
            "schema_version": 1,
            "updated_at": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            **data,
        }
    )
    write_json(path, existing)


def prompt_slug(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "-", name).strip("-") or "prompt"


def write_prompt_artifact(out_dir: Path, name: str, prompt: str) -> Path:
    path = out_dir / "prompts" / f"{prompt_slug(name)}.md"
    write_text(path, prompt)
    write_prompt_index(out_dir)
    return path


def write_prompt_index(out_dir: Path) -> None:
    prompt_dir = out_dir / "prompts"
    prompts = sorted(prompt_dir.glob("*.md")) if prompt_dir.is_dir() else []
    lines = [
        "# Gemini SDK Prompt Index",
        "",
        "Exact rendered prompts preserved for this SDK run.",
        "",
    ]
    if prompts:
        lines += [f"- `{path.relative_to(out_dir)}`" for path in prompts]
    else:
        lines.append("- No rendered prompt artifacts yet.")
    write_text(out_dir / "prompt.md", "\n".join(lines))


def write_input_signal_artifact(out_dir: Path, signal_context: str) -> None:
    write_text(out_dir / "input_signals_for_gemini.md", signal_context)


def jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json", exclude_none=True)
    if hasattr(value, "dict"):
        return value.dict()
    return str(value)


def enum_string(values: list[str], description: str | None = None) -> dict[str, Any]:
    schema: dict[str, Any] = {"type": "string", "enum": values}
    if description:
        schema["description"] = description
    return schema


def plain_string(description: str | None = None) -> dict[str, Any]:
    schema: dict[str, Any] = {"type": "string"}
    if description:
        schema["description"] = description
    return schema


def string_list(description: str | None = None) -> dict[str, Any]:
    schema: dict[str, Any] = {"type": "array", "items": {"type": "string"}}
    if description:
        schema["description"] = description
    return schema


def grounding_constraints_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "shot_span_ids",
            "cut_boundary_ids",
            "candidate_beat_ids",
            "word_ids",
            "prosody_segment_ids",
            "audio_signal_ids",
        ],
        "properties": {
            "shot_span_ids": string_list("Supplied edit_span_* IDs that bound this claim."),
            "cut_boundary_ids": string_list("Supplied edit_boundary_* or sync_* IDs used for cut/boundary timing."),
            "candidate_beat_ids": string_list("Supplied beat_* IDs used as nearby beat/onset anchors."),
            "word_ids": string_list("Supplied word_* IDs used for exact spoken-word timing."),
            "prosody_segment_ids": string_list("Supplied prosody_seg_* IDs used for delivery/pace sync."),
            "audio_signal_ids": string_list("Supplied audio/onset/sync IDs used for audio-visible sync."),
        },
        "description": "Grouped deterministic signal IDs. Use empty arrays when a category is not applicable; never invent IDs.",
    }


def confidence_schema() -> dict[str, Any]:
    return {"type": "number", "minimum": 0, "maximum": 1}


def visual_layout_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "evidence_id",
            "time_range",
            "anchor_signal_ids",
            "grounding_constraints",
            "layout_type",
            "visible_layers",
            "surface_roles",
            "layer_stack_description",
            "dominant_focus",
            "composition_notes",
            "confidence",
            "needs_review",
        ],
        "properties": {
            "evidence_id": {"type": "string"},
            "time_range": {
                "type": "string",
                "description": "Resolve-style MM:SS:FF-MM:SS:FF or HH:MM:SS:FF-HH:MM:SS:FF.",
            },
            "anchor_signal_ids": string_list("Deterministic signal IDs used as timing anchors."),
            "grounding_constraints": grounding_constraints_schema(),
            "layout_type": enum_string(LAYOUT_TYPES),
            "visible_layers": string_list("Plain names of visible layers, top-to-bottom when possible."),
            "surface_roles": {
                "type": "array",
                "items": enum_string(SURFACE_ROLES),
            },
            "layer_stack_description": {"type": "string"},
            "dominant_focus": {"type": "string"},
            "composition_notes": {"type": "string"},
            "confidence": confidence_schema(),
            "needs_review": {"type": "boolean"},
        },
    }


def visual_craft_event_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "evidence_id",
            "time_range",
            "anchor_signal_ids",
            "grounding_constraints",
            "mechanic_family",
            "event_type",
            "visible_evidence",
            "affected_layer",
            "motion_direction",
            "motion_profile",
            "intensity",
            "duration_class",
            "sync_kind",
            "sync_observation",
            "craft_function_hypothesis",
            "hypothesis_basis",
            "recreation_relevance",
            "confidence",
            "needs_review",
            "review_reason",
        ],
        "properties": {
            "evidence_id": {"type": "string"},
            "time_range": {
                "type": "string",
                "description": "Resolve-style MM:SS:FF-MM:SS:FF or HH:MM:SS:FF-HH:MM:SS:FF.",
            },
            "anchor_signal_ids": string_list("Deterministic signal IDs used as timing anchors."),
            "grounding_constraints": grounding_constraints_schema(),
            "mechanic_family": enum_string(MECHANIC_FAMILIES),
            "event_type": plain_string(
                "Taxonomy label from the prompt's edit-mechanic list. Do not invent labels."
            ),
            "visible_evidence": {"type": "string"},
            "affected_layer": {"type": "string"},
            "motion_direction": enum_string(MOTION_DIRECTIONS),
            "motion_profile": enum_string(MOTION_PROFILES),
            "intensity": enum_string(INTENSITY_LEVELS),
            "duration_class": enum_string(DURATION_CLASSES),
            "sync_kind": enum_string(SYNC_KINDS),
            "sync_observation": {"type": "string"},
            "craft_function_hypothesis": enum_string(CRAFT_FUNCTIONS),
            "hypothesis_basis": enum_string(HYPOTHESIS_BASES),
            "recreation_relevance": {"type": "string"},
            "confidence": confidence_schema(),
            "needs_review": {"type": "boolean"},
            "review_reason": {"type": "string"},
        },
    }


def visual_survey_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "visual_layout_timeline",
            "visual_craft_events",
            "visual_evidence_notes",
        ],
        "properties": {
            "visual_layout_timeline": {
                "type": "array",
                "items": visual_layout_schema(),
            },
            "visual_craft_events": {
                "type": "array",
                "items": visual_craft_event_schema(),
            },
            "visual_evidence_notes": {"type": "string"},
        },
    }


def visual_micro_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "span_id",
            "time_range",
            "layout_snapshot",
            "visual_craft_events",
            "negative_observations",
            "review_notes",
        ],
        "properties": {
            "span_id": {"type": "string"},
            "time_range": {
                "type": "string",
                "description": "Resolve-style MM:SS:FF-MM:SS:FF or HH:MM:SS:FF-HH:MM:SS:FF.",
            },
            "layout_snapshot": visual_layout_schema(),
            "visual_craft_events": {
                "type": "array",
                "items": visual_craft_event_schema(),
            },
            "negative_observations": {
                "type": "array",
                "items": {"type": "string"},
            },
            "review_notes": {"type": "string"},
        },
    }


def default_signals_dir(video: Path) -> Path:
    return HERE / "outputs" / video.stem / "signals"


def resolve_signals_dir(video: Path, signals_dir_arg: str | None) -> Path:
    if signals_dir_arg:
        return Path(signals_dir_arg).expanduser().resolve()
    return default_signals_dir(video).resolve()


def exemplar_slug(video: Path) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", video.stem.lower()).strip("-")
    return slug or "exemplar"


def new_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sdk_runs_dir(video: Path) -> Path:
    return REPO_ROOT / "exemplars" / exemplar_slug(video) / "gemini_runs" / "sdk"


def default_sdk_out_dir(video: Path) -> Path:
    return sdk_runs_dir(video) / new_run_id()


def resolve_out_dir(video: Path, out_dir_arg: str | None) -> Path:
    if out_dir_arg:
        return Path(out_dir_arg).expanduser().resolve()
    return default_sdk_out_dir(video).resolve()


def resolve_existing_out_dir(video: Path, out_dir_arg: str | None) -> Path:
    if out_dir_arg:
        return Path(out_dir_arg).expanduser().resolve()
    root = sdk_runs_dir(video)
    candidates = sorted(path for path in root.glob("*") if path.is_dir())
    if not candidates:
        sys.exit(f"error: no SDK run directory found under {root}; pass --out-dir")
    return candidates[-1].resolve()


def ensure_shared_out_dir(args: argparse.Namespace, video: Path) -> None:
    if not args.out_dir:
        args.out_dir = str(default_sdk_out_dir(video))


def seconds_to_offset(seconds: float) -> str:
    text = f"{max(0.0, seconds):.3f}".rstrip("0").rstrip(".")
    return f"{text or '0'}s"


def seconds_to_timecode(seconds: float, fps: float) -> str:
    seconds = max(0.0, seconds)
    total_seconds = int(seconds)
    frames = int(round((seconds - total_seconds) * fps))
    if frames >= int(round(fps)):
        total_seconds += 1
        frames = 0
    minutes, secs = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}:{frames:02d}"
    return f"{minutes:02d}:{secs:02d}:{frames:02d}"


def frame_at(seconds: float, fps: float) -> int:
    return int(round(max(0.0, seconds) * fps))


def media_fps(media: dict[str, Any]) -> float:
    fps = media.get("fps") or media.get("timecode_timebase_fps") or 60.0
    return float(fps)


def media_duration(media: dict[str, Any]) -> float:
    return float(media.get("duration") or 0.0)


def normalize_media_resolution(value: str | None) -> str | None:
    if not value:
        return None
    value = value.upper()
    if value.startswith("MEDIA_RESOLUTION_"):
        return value
    return f"MEDIA_RESOLUTION_{value}"


def table_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|").strip()


def comma_list(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value or "")


def grounding_summary(value: Any) -> str:
    if not isinstance(value, dict):
        return ""
    parts = []
    for key in [
        "shot_span_ids",
        "cut_boundary_ids",
        "candidate_beat_ids",
        "word_ids",
        "prosody_segment_ids",
        "audio_signal_ids",
    ]:
        ids = comma_list(value.get(key, []))
        if ids:
            parts.append(f"{key}={ids}")
    return "; ".join(parts)


def markdown_bool(value: Any) -> str:
    return "yes" if bool(value) else "no"


def markdown_confidence(value: Any) -> str:
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return ""


def render_analysis_markdown(out_dir: Path, video: Path) -> str:
    craft = read_json(out_dir / "visual_craft_events.json", {})
    layout = read_json(out_dir / "visual_layout_timeline.json", {})
    micro = read_json(out_dir / "visual_micro_passes.json", {})
    usage = read_json(out_dir / "sdk_usage.json", {})

    events = craft.get("events", []) if isinstance(craft, dict) else []
    layouts = layout.get("layout_timeline", []) if isinstance(layout, dict) else []
    passes = micro.get("passes", []) if isinstance(micro, dict) else []

    generated_at = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "# Gemini SDK Visual Evidence Analysis",
        "",
        f"Video: `{video}`",
        f"Generated: `{generated_at}`",
        "",
        "This is a Visual Evidence Pack for human inspection. It describes observable edit mechanics only; it is not a Viral Pattern report, Beat Sheet, or Recreation spec.",
        "",
        "Use the time column as Resolve-style frame timecode (`MM:SS:FF`). The final field is frames at the media FPS, not decimal seconds.",
        "",
        "## Run Summary",
        "",
        f"- Layout timeline rows: {len(layouts)}",
        f"- Visual craft events: {len(events)}",
        f"- Micro passes: {len(passes)}",
        f"- Usage metadata file: `{(out_dir / 'sdk_usage.json')}`" if usage else "- Usage metadata file: not written yet",
        "",
        "## Layout Timeline",
        "",
        "| time | anchors | layout | surface roles | focus | confidence | review |",
        "|---|---|---|---|---|---:|---|",
    ]
    if layouts:
        for item in layouts:
            lines.append(
                "| {time} | {anchors} | {layout_type} | {roles} | {focus} | {confidence} | {review} |".format(
                    time=table_cell(item.get("time_range", "")),
                    anchors=table_cell(comma_list(item.get("anchor_signal_ids", []))),
                    layout_type=table_cell(item.get("layout_type", "")),
                    roles=table_cell(comma_list(item.get("surface_roles", item.get("visible_layers", [])))),
                    focus=table_cell(item.get("dominant_focus") or item.get("description", "")),
                    confidence=markdown_confidence(item.get("confidence")),
                    review=markdown_bool(item.get("needs_review")),
                )
            )
    else:
        lines.append("|  |  |  |  | no survey layout timeline written |  |  |")

    lines += [
        "",
        "## Visual Craft Events",
        "",
        "| time | anchors | family | event type | intensity | sync | craft function | basis | confidence | review |",
        "|---|---|---|---|---|---|---|---|---:|---|",
    ]
    if events:
        for item in events:
            lines.append(
                "| {time} | {anchors} | {family} | {event_type} | {intensity} | {sync} | {function} | {basis} | {confidence} | {review} |".format(
                    time=table_cell(item.get("time_range", "")),
                    anchors=table_cell(comma_list(item.get("anchor_signal_ids", []))),
                    family=table_cell(item.get("mechanic_family", "")),
                    event_type=table_cell(item.get("event_type", "")),
                    intensity=table_cell(item.get("intensity", "")),
                    sync=table_cell(item.get("sync_kind", "")),
                    function=table_cell(item.get("craft_function_hypothesis", "")),
                    basis=table_cell(item.get("hypothesis_basis", "")),
                    confidence=markdown_confidence(item.get("confidence")),
                    review=markdown_bool(item.get("needs_review")),
                )
            )
    else:
        lines.append("|  |  |  |  |  |  |  |  |  | no visual craft events written |")

    lines += ["", "## Event Details", ""]
    if events:
        for item in events:
            evidence_id = item.get("evidence_id", "event")
            event_type = item.get("event_type", "unknown")
            time_range = item.get("time_range", "")
            lines += [
                f"### {evidence_id} - {event_type} - {time_range}",
                "",
                f"- Anchors: `{comma_list(item.get('anchor_signal_ids', []))}`",
                f"- Grounding constraints: `{grounding_summary(item.get('grounding_constraints', {}))}`",
                f"- Affected layer: {item.get('affected_layer', '')}",
                f"- Visible evidence: {item.get('visible_evidence', '')}",
                f"- Motion: direction `{item.get('motion_direction', '')}`, profile `{item.get('motion_profile', '')}`, duration `{item.get('duration_class', '')}`",
                f"- Sync: `{item.get('sync_kind', '')}` - {item.get('sync_observation', '')}",
                f"- Controlled hypothesis: `{item.get('craft_function_hypothesis', '')}` based on `{item.get('hypothesis_basis', '')}`",
                f"- Recreate visually: {item.get('recreation_relevance', '')}",
                f"- Review: {markdown_bool(item.get('needs_review'))}. {item.get('review_reason', '')}",
                "",
            ]
    else:
        lines.append("No event details yet.")

    lines += ["", "## Micro Pass Review Notes", ""]
    if passes:
        for item in passes:
            evidence = item.get("evidence", {})
            notes = evidence.get("review_notes", "") if isinstance(evidence, dict) else ""
            negative = evidence.get("negative_observations", []) if isinstance(evidence, dict) else []
            lines += [
                f"### {item.get('span_id', '')} - {item.get('start_timecode', '')}-{item.get('end_timecode', '')}",
                "",
                f"- FPS: {item.get('fps')} (reasons: {comma_list(item.get('fps_reasons', [])) or 'default'})",
                f"- Review notes: {notes or 'none'}",
                f"- Negative observations: {comma_list(negative) or 'none'}",
                "",
            ]
    else:
        lines.append("No micro passes written yet.")
    return "\n".join(lines)


def write_analysis_markdown(out_dir: Path, video: Path) -> None:
    write_text(out_dir / "analysis.md", render_analysis_markdown(out_dir, video))


def compact_prosody_features(prosody: dict[str, Any]) -> dict[str, Any]:
    features = prosody.get("features", {})
    return {
        "tool": prosody.get("tool"),
        "feature_set": prosody.get("feature_set"),
        "feature_level": prosody.get("feature_level"),
        "status": prosody.get("status"),
        "scope": "global full-video voice/acoustic functionals, not time-aligned",
        "features": {key: features[key] for key in PROSODY_CONTEXT_KEYS if key in features},
    }


def compact_prosody_segment(item: dict[str, Any]) -> dict[str, Any]:
    features = item.get("features", {})
    return {
        "signal_id": item.get("signal_id"),
        "segment_id": item.get("segment_id"),
        "start": item.get("start"),
        "end": item.get("end"),
        "start_timecode": item.get("start_timecode"),
        "end_timecode": item.get("end_timecode"),
        "start_frame": item.get("start_frame"),
        "end_frame": item.get("end_frame"),
        "word_count": item.get("word_count"),
        "wpm": item.get("wpm"),
        "relative_delivery": item.get("relative_delivery", {}),
        "delivery_tags": item.get("delivery_tags", []),
        "text": item.get("text", ""),
        "features": {
            "pitch_mean": features.get("F0semitoneFrom27.5Hz_sma3nz_amean"),
            "pitch_range": features.get("F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2"),
            "loudness_mean": features.get("loudness_sma3_amean"),
            "loudness_range": features.get("loudness_sma3_pctlrange0-2"),
            "loudness_peaks_per_sec": features.get("loudnessPeaksPerSec"),
        },
    }


def compact_word(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "signal_id": item.get("signal_id"),
        "word": item.get("word"),
        "start": item.get("start"),
        "end": item.get("end"),
        "start_timecode": item.get("start_timecode"),
        "end_timecode": item.get("end_timecode"),
        "start_frame": item.get("start_frame"),
        "end_frame": item.get("end_frame"),
        "score": item.get("score"),
    }


def compact_signal_context(signals_dir: Path, max_beats: int = 80, max_words: int = 320) -> str:
    media = read_json(signals_dir / "media.json", {})
    transcript = read_json(signals_dir / "transcript.words.json", {})
    edits = read_json(signals_dir / "edit_mechanisms.json", {})
    beats = read_json(signals_dir / "candidate_beats.json", {})
    speech = read_json(signals_dir / "speech_metrics.json", {})
    audio = read_json(signals_dir / "audio_features.json", {})
    prosody = read_json(signals_dir / "prosody_features.json", {})
    prosody_segments = read_json(signals_dir / "prosody_segments.json", {})

    boundaries = edits.get("boundary_mechanisms", [])
    spans = edits.get("shot_spans", [])
    words = transcript.get("words", [])[:max_words]
    beat_rows = beats.get("beats", [])[:max_beats]
    prosody_rows = prosody_segments.get("segments", [])[:24]
    fps = media_fps(media)

    lines = [
        "# Deterministic Signal Context",
        "",
        "Gemini must use these IDs as timing anchors. Do not infer new timing IDs.",
        "WhisperX word rows, WPM/prosody rows, shot spans, cut boundaries, and candidate beats are the source-of-truth constraints.",
        "The edit-mechanics taxonomy is only a label menu for visible evidence inside these deterministic constraints.",
        "`MM:SS:FF` values are Resolve-style frame timecodes, not decimal seconds.",
        "The final field is frames at the media FPS; at 60 FPS, `00:02:21` means 2 seconds + 21 frames.",
        "Do not calculate decimal seconds from these timecodes; downstream tools derive seconds from signal IDs, frames, and FPS.",
        "",
        "## Media",
        "",
        json.dumps(
            {
                "filename": media.get("filename"),
                "duration": media.get("duration"),
                "duration_timecode": media.get("duration_timecode"),
                "fps": media.get("fps"),
                "frame_count": media.get("frame_count"),
                "resolution": media.get("resolution"),
            },
            indent=2,
            sort_keys=True,
        ),
        "",
        "## Speech And Audio Summary",
        "",
        json.dumps(
            {
                "speech_metrics": speech,
                "estimated_audio_tempo_bpm": audio.get("tempo_bpm")
                or audio.get("estimated_tempo_bpm"),
                "global_prosody_summary": compact_prosody_features(prosody),
            },
            indent=2,
            sort_keys=True,
        ),
        "",
        "## Word-Level Transcript",
        "",
        "These WhisperX rows are the exact spoken-word timing source of truth. Use `word_*` IDs when visible edits, captions, cuts, or motion appear synchronized to speech.",
        "",
        "| signal_id | time | frames | score | word |",
        "|---|---:|---:|---:|---|",
    ]
    for item in words:
        compact = compact_word(item)
        lines.append(
            "| {signal_id} | {start_timecode}-{end_timecode} | {start_frame}-{end_frame} | {score} | {word} |".format(
                signal_id=compact.get("signal_id", ""),
                start_timecode=compact.get("start_timecode") or "",
                end_timecode=compact.get("end_timecode") or "",
                start_frame=compact.get("start_frame") or "",
                end_frame=compact.get("end_frame") or "",
                score=compact.get("score") or "",
                word=table_cell(compact.get("word", "")),
            )
        )
    if len(transcript.get("words", [])) > len(words):
        lines.append(
            f"| truncated |  |  |  | Showing first {len(words)} of {len(transcript.get('words', []))} words. |"
        )
    lines += [
        "",
        "## Prosody Segments",
        "",
        "These rows are transcript-segment-level voice delivery signals. Use them only to check visual/audio synchronization, not to explain virality.",
        "",
        "| signal_id | segment_id | time | frames | WPM | tags | pitch_mean | pitch_range | loudness_mean | loudness_range | text |",
        "|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|",
    ]
    for item in prosody_rows:
        compact = compact_prosody_segment(item)
        features = compact["features"]
        lines.append(
            "| {signal_id} | {segment_id} | {start_timecode}-{end_timecode} | {start_frame}-{end_frame} | {wpm} | {tags} | {pitch_mean} | {pitch_range} | {loudness_mean} | {loudness_range} | {text} |".format(
                signal_id=compact.get("signal_id", ""),
                segment_id=compact.get("segment_id", ""),
                start_timecode=compact.get("start_timecode") or "",
                end_timecode=compact.get("end_timecode") or "",
                start_frame=compact.get("start_frame") or "",
                end_frame=compact.get("end_frame") or "",
                wpm=compact.get("wpm") or "",
                tags=table_cell(", ".join(compact.get("delivery_tags", []))),
                pitch_mean=features.get("pitch_mean") or "",
                pitch_range=features.get("pitch_range") or "",
                loudness_mean=features.get("loudness_mean") or "",
                loudness_range=features.get("loudness_range") or "",
                text=table_cell(compact.get("text", "")),
            )
        )
    lines += [
        "",
        "## Shot Boundaries",
        "",
        "| signal_id | kind | timecode | frame | confidence | needs_review | source_signal_ids |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    for event in boundaries:
        lines.append(
            "| {signal_id} | {event_kind} | {timecode} | {frame} | {confidence} | {needs_review} | {source_signal_ids} |".format(
                signal_id=event.get("signal_id", ""),
                event_kind=event.get("event_kind", ""),
                timecode=event.get("timecode") or seconds_to_timecode(float(event.get("time", 0)), fps),
                frame=event.get("frame", ""),
                confidence=event.get("confidence", ""),
                needs_review=event.get("needs_review", ""),
                source_signal_ids=", ".join(event.get("source_signal_ids", [])),
            )
        )

    lines += [
        "",
        "## Shot Spans",
        "",
        "| signal_id | start | end | frames | duration | boundary_ids |",
        "|---|---:|---:|---|---:|---|",
    ]
    for span in spans:
        lines.append(
            "| {signal_id} | {start_timecode} | {end_timecode} | {start_frame}-{end_frame} | {duration} | {start_boundary_id} -> {end_boundary_id} |".format(
                signal_id=span.get("signal_id", ""),
                start_timecode=span.get("start_timecode", ""),
                end_timecode=span.get("end_timecode", ""),
                start_frame=span.get("start_frame", ""),
                end_frame=span.get("end_frame", ""),
                duration=span.get("duration", ""),
                start_boundary_id=span.get("start_boundary_id") or "media_start",
                end_boundary_id=span.get("end_boundary_id") or "",
            )
        )

    lines += [
        "",
        "## Candidate Beats",
        "",
        "| signal_id | timecode | frame | source_types | source_signal_ids |",
        "|---|---:|---:|---|---|",
    ]
    for beat in beat_rows:
        lines.append(
            "| {signal_id} | {timecode} | {frame} | {source_types} | {source_signal_ids} |".format(
                signal_id=beat.get("signal_id", ""),
                timecode=beat.get("timecode") or seconds_to_timecode(float(beat.get("time", 0)), fps),
                frame=beat.get("frame", ""),
                source_types=", ".join(beat.get("source_types", [])),
                source_signal_ids=", ".join(beat.get("source_signal_ids", [])),
            )
        )
    return "\n".join(lines)


def render_prompt(body: str, replacements: dict[str, str]) -> str:
    prompt = body
    for key, value in replacements.items():
        prompt = prompt.replace(key, value)
    leftovers = [
        marker
        for marker in [
            VIDEO_FILENAME_PLACEHOLDER,
            ANALYSIS_CONTEXT_PLACEHOLDER,
            SPAN_CONTEXT_PLACEHOLDER,
            VISUAL_EVIDENCE_PLACEHOLDER,
        ]
        if marker in prompt
    ]
    if leftovers:
        sys.exit(f"error: unresolved prompt placeholders: {', '.join(leftovers)}")
    return prompt


def parse_json_response(text: str) -> tuple[dict[str, Any] | list[Any] | None, str | None]:
    candidate = text.strip()
    match = JSON_FENCE_RE.match(candidate)
    if match:
        candidate = match.group(1).strip()
    try:
        return json.loads(candidate), None
    except json.JSONDecodeError as exc:
        return None, str(exc)


def load_media(signals_dir: Path, video: Path) -> dict[str, Any]:
    media = read_json(signals_dir / "media.json", {})
    if not media:
        media = {
            "filename": video.name,
            "duration": None,
            "fps": 60.0,
            "source_path": str(video),
        }
    return media


def load_spans(signals_dir: Path, media: dict[str, Any]) -> list[dict[str, Any]]:
    edits = read_json(signals_dir / "edit_mechanisms.json", {})
    spans = list(edits.get("shot_spans") or [])
    if spans:
        return spans
    duration = media_duration(media)
    fps = media_fps(media)
    return [
        {
            "signal_id": "edit_span_0001",
            "start": 0.0,
            "end": duration,
            "duration": duration,
            "start_frame": 0,
            "end_frame": frame_at(duration, fps),
            "start_timecode": seconds_to_timecode(0.0, fps),
            "end_timecode": seconds_to_timecode(duration, fps),
            "start_boundary_id": "media_start",
            "end_boundary_id": "media_end",
        }
    ]


def load_boundary_map(signals_dir: Path) -> dict[str, dict[str, Any]]:
    edits = read_json(signals_dir / "edit_mechanisms.json", {})
    return {
        str(item.get("signal_id")): item
        for item in edits.get("boundary_mechanisms", [])
        if item.get("signal_id")
    }


def span_review_reasons(
    span: dict[str, Any],
    boundary_map: dict[str, dict[str, Any]],
    *,
    short_span_seconds: float,
    low_confidence_threshold: float,
) -> list[str]:
    reasons: list[str] = []
    duration = float(span.get("duration") or 0.0)
    if duration and duration <= short_span_seconds:
        reasons.append(f"short_span<={short_span_seconds:g}s")

    for edge in ("start", "end"):
        boundary_id = span.get(f"{edge}_boundary_id")
        if not boundary_id:
            continue
        boundary = boundary_map.get(str(boundary_id), {})
        event_kind = str(boundary.get("event_kind") or span.get(f"{edge}_boundary_kind") or "")
        confidence = boundary.get("confidence", span.get(f"{edge}_boundary_confidence"))
        needs_review = bool(boundary.get("needs_review", False))
        if needs_review or "candidate" in event_kind or "review" in event_kind:
            reasons.append(f"{edge}_boundary_review:{boundary_id}")
        try:
            if confidence is not None and float(confidence) < low_confidence_threshold:
                reasons.append(f"{edge}_boundary_confidence<{low_confidence_threshold:g}:{boundary_id}")
        except (TypeError, ValueError):
            pass
    return reasons


def choose_span_fps(
    span: dict[str, Any],
    boundary_map: dict[str, dict[str, Any]],
    *,
    base_fps: float,
    review_fps: float,
    adaptive_fps: bool,
    short_span_seconds: float,
    low_confidence_threshold: float,
) -> tuple[float, list[str]]:
    if not adaptive_fps:
        return base_fps, []
    reasons = span_review_reasons(
        span,
        boundary_map,
        short_span_seconds=short_span_seconds,
        low_confidence_threshold=low_confidence_threshold,
    )
    return (max(base_fps, review_fps), reasons) if reasons else (base_fps, [])


def response_needs_high_fps_retry(
    parsed: dict[str, Any] | list[Any] | None,
    *,
    low_confidence_threshold: float,
) -> tuple[bool, list[str]]:
    if not isinstance(parsed, dict):
        return True, ["unparseable_or_non_object_response"]

    reasons: list[str] = []
    layout = parsed.get("layout_snapshot")
    if isinstance(layout, dict):
        if layout.get("needs_review"):
            reasons.append("layout_snapshot_needs_review")
        try:
            confidence = layout.get("confidence")
            if confidence is not None and float(confidence) < low_confidence_threshold:
                reasons.append("layout_snapshot_low_confidence")
        except (TypeError, ValueError):
            pass

    for index, event in enumerate(parsed.get("visual_craft_events", [])):
        if not isinstance(event, dict):
            continue
        if event.get("needs_review"):
            reasons.append(f"event_{index}_needs_review")
        try:
            confidence = event.get("confidence")
            if confidence is not None and float(confidence) < low_confidence_threshold:
                reasons.append(f"event_{index}_low_confidence")
        except (TypeError, ValueError):
            pass
    return bool(reasons), reasons


def select_spans(
    spans: list[dict[str, Any]],
    requested_ids: str | None,
    max_spans: int | None,
) -> list[dict[str, Any]]:
    if requested_ids:
        wanted = {item.strip() for item in requested_ids.split(",") if item.strip()}
        spans = [span for span in spans if span.get("signal_id") in wanted]
    if max_spans is not None:
        spans = spans[:max_spans]
    if not spans:
        sys.exit("error: no spans selected for micro analysis")
    return spans


def beats_for_span(signals_dir: Path, start: float, end: float) -> list[dict[str, Any]]:
    beats = read_json(signals_dir / "candidate_beats.json", {}).get("beats", [])
    result = []
    for beat in beats:
        time_value = float(beat.get("time") or 0.0)
        if start - 0.25 <= time_value <= end + 0.25:
            result.append(
                {
                    "signal_id": beat.get("signal_id"),
                    "time": beat.get("time"),
                    "timecode": beat.get("timecode"),
                    "frame": beat.get("frame"),
                    "source_types": beat.get("source_types", []),
                    "source_signal_ids": beat.get("source_signal_ids", []),
                }
            )
    return result


def words_for_span(signals_dir: Path, start: float, end: float) -> list[dict[str, Any]]:
    words = read_json(signals_dir / "transcript.words.json", {}).get("words", [])
    result = []
    for item in words:
        word_start = float(item.get("start") or 0.0)
        word_end = float(item.get("end") or 0.0)
        if word_end >= start - 0.25 and word_start <= end + 0.25:
            result.append(compact_word(item))
    return result


def prosody_for_span(signals_dir: Path, start: float, end: float) -> list[dict[str, Any]]:
    segments = read_json(signals_dir / "prosody_segments.json", {}).get("segments", [])
    result = []
    for item in segments:
        segment_start = float(item.get("start") or 0.0)
        segment_end = float(item.get("end") or 0.0)
        if segment_end >= start - 0.25 and segment_start <= end + 0.25:
            result.append(compact_prosody_segment(item))
    return result


def span_context(signals_dir: Path, span: dict[str, Any], media: dict[str, Any]) -> str:
    fps = media_fps(media)
    start = float(span.get("start") or 0.0)
    end = float(span.get("end") or media_duration(media))
    context = {
        "span": {
            "signal_id": span.get("signal_id"),
            "start": start,
            "end": end,
            "duration": span.get("duration"),
            "start_timecode": span.get("start_timecode") or seconds_to_timecode(start, fps),
            "end_timecode": span.get("end_timecode") or seconds_to_timecode(end, fps),
            "start_frame": span.get("start_frame") or frame_at(start, fps),
            "end_frame": span.get("end_frame") or frame_at(end, fps),
            "start_boundary_id": span.get("start_boundary_id") or "media_start",
            "end_boundary_id": span.get("end_boundary_id") or "media_end",
            "end_boundary_kind": span.get("end_boundary_kind"),
            "end_boundary_confidence": span.get("end_boundary_confidence"),
        },
        "nearby_words": words_for_span(signals_dir, start, end),
        "nearby_candidate_beats": beats_for_span(signals_dir, start, end),
        "nearby_prosody_segments": prosody_for_span(signals_dir, start, end),
    }
    return json.dumps(context, indent=2, sort_keys=True)


def import_sdk():
    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        sys.exit(f"error: google-genai is not installed or could not import: {exc}")
    return genai, types


def api_key_from_env_file(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        lines = path.read_text().splitlines()
    except OSError:
        return None
    values: dict[str, str] = {}
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        try:
            parts = shlex.split(line, comments=True, posix=True)
        except ValueError:
            continue
        if not parts or "=" not in parts[0]:
            continue
        name, value = parts[0].split("=", 1)
        if name in {"GEMINI_API_KEY", "GOOGLE_API_KEY"} and value:
            values[name] = value
    return values.get("GEMINI_API_KEY") or values.get("GOOGLE_API_KEY")


def resolve_api_key(api_key: str | None) -> str | None:
    if api_key:
        return api_key
    for env_name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        value = os.environ.get(env_name)
        if value:
            return value
    for path in DEFAULT_API_KEY_ENV_FILES:
        value = api_key_from_env_file(path)
        if value:
            return value
    return None


def make_client(api_key: str | None):
    genai, _types = import_sdk()
    resolved_api_key = resolve_api_key(api_key)
    if resolved_api_key:
        return genai.Client(api_key=resolved_api_key)
    return genai.Client()


def state_name(state: Any) -> str:
    if state is None:
        return ""
    return getattr(state, "name", str(state))


def upload_video(client: Any, types: Any, video: Path, timeout: float) -> Any:
    mime_type, _encoding = mimetypes.guess_type(str(video))
    uploaded = client.files.upload(
        file=str(video),
        config=types.UploadFileConfig(
            display_name=video.name,
            mime_type=mime_type or "video/mp4",
        ),
    )
    started = time.monotonic()
    while state_name(getattr(uploaded, "state", None)) == "PROCESSING":
        if time.monotonic() - started > timeout:
            sys.exit(f"error: timed out waiting for File API processing: {uploaded.name}")
        time.sleep(2)
        uploaded = client.files.get(name=uploaded.name)
    if state_name(getattr(uploaded, "state", None)) == "FAILED":
        sys.exit(f"error: File API processing failed: {jsonable(uploaded)}")
    return uploaded


def build_video_part(
    types: Any,
    uploaded: Any,
    *,
    fps: float,
    media_resolution: str | None,
    start: float | None = None,
    end: float | None = None,
) -> Any:
    part = types.Part(
        file_data=types.FileData(
            file_uri=uploaded.uri,
            mime_type=uploaded.mime_type or "video/mp4",
        ),
        video_metadata=types.VideoMetadata(
            start_offset=seconds_to_offset(start) if start is not None else None,
            end_offset=seconds_to_offset(end) if end is not None else None,
            fps=fps,
        ),
    )
    if media_resolution:
        part.media_resolution = types.PartMediaResolution(level=media_resolution)
    return part


def generate_json_evidence(
    client: Any,
    types: Any,
    *,
    model: str,
    uploaded: Any,
    prompt: str,
    fps: float,
    media_resolution: str | None,
    thinking_level: str | None,
    start: float | None,
    end: float | None,
    max_output_tokens: int,
    count_tokens: bool,
    response_json_schema: dict[str, Any] | None,
) -> tuple[dict[str, Any] | list[Any] | None, str, dict[str, Any]]:
    video_part = build_video_part(
        types,
        uploaded,
        fps=fps,
        media_resolution=media_resolution,
        start=start,
        end=end,
    )
    contents = [
        types.Content(
            role="user",
            parts=[
                video_part,
                types.Part.from_text(text=prompt),
            ],
        )
    ]
    config_kwargs: dict[str, Any] = {
        "response_mime_type": "application/json",
        "max_output_tokens": max_output_tokens,
    }
    if response_json_schema:
        config_kwargs["response_json_schema"] = response_json_schema
    if thinking_level:
        config_kwargs["thinking_config"] = types.ThinkingConfig(
            thinking_level=thinking_level
        )
    config = types.GenerateContentConfig(**config_kwargs)
    usage: dict[str, Any] = {}
    if count_tokens:
        token_response = client.models.count_tokens(model=model, contents=contents)
        usage["count_tokens"] = jsonable(token_response)
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )
    raw_text = response.text or ""
    parsed, parse_error = parse_json_response(raw_text)
    if parsed is None and getattr(response, "parsed", None) is not None:
        parsed = jsonable(getattr(response, "parsed"))
        parse_error = None
    usage["usage_metadata"] = jsonable(getattr(response, "usage_metadata", None))
    if parse_error:
        usage["parse_error"] = parse_error
    return parsed, raw_text, usage


def survey_output_payload(
    parsed: dict[str, Any] | list[Any] | None,
    raw_text: str,
    *,
    video: Path,
    model: str,
    fps: float,
    media_resolution: str | None,
    thinking_level: str | None,
) -> tuple[dict[str, Any], dict[str, Any], str]:
    if isinstance(parsed, dict):
        events = parsed.get("visual_craft_events", [])
        layout = parsed.get("visual_layout_timeline", [])
        notes = parsed.get("visual_evidence_notes", "")
    else:
        events, layout, notes = [], [], raw_text
    metadata = {
        "schema_version": 1,
        "source": "gemini_sdk_visual_survey",
        "video": video.name,
        "model": model,
        "fps": fps,
        "media_resolution": media_resolution,
        "thinking_level": thinking_level,
        "generated_at": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "gemini_role": "visual_evidence_extractor_only",
    }
    return (
        {**metadata, "events": events},
        {**metadata, "layout_timeline": layout},
        str(notes or raw_text),
    )


def run_survey(args: argparse.Namespace, uploaded: Any | None = None) -> dict[str, Any]:
    video = Path(args.video).expanduser().resolve()
    if not video.is_file():
        sys.exit(f"error: video not found: {video}")
    signals_dir = resolve_signals_dir(video, args.signals_dir)
    out_dir = resolve_out_dir(video, args.out_dir)
    media = load_media(signals_dir, video)
    config, body = load_template(Path(args.prompt).expanduser().resolve())
    model = args.model or config.get("model", DEFAULT_MODEL)
    fps = float(args.fps or config.get("fps", 5))
    media_resolution = normalize_media_resolution(
        args.media_resolution or config.get("media_resolution")
    )
    thinking_level = args.thinking_level or config.get("thinking_level")
    signal_context = compact_signal_context(signals_dir)
    prompt = render_prompt(
        body,
        {
            VIDEO_FILENAME_PLACEHOLDER: video.name,
            ANALYSIS_CONTEXT_PLACEHOLDER: signal_context,
        },
    )
    schema = visual_survey_schema()
    write_input_signal_artifact(out_dir, signal_context)
    write_prompt_artifact(out_dir, "survey", prompt)
    write_json(out_dir / "response_schema_survey.json", schema)
    update_run_manifest(
        out_dir,
        {
            "video": str(video),
            "signals_dir": str(signals_dir),
            "out_dir": str(out_dir),
            "mode": "survey",
            "model": model,
            "survey": {
                "fps": fps,
                "media_resolution": media_resolution,
                "thinking_level": thinking_level,
                "prompt": "prompts/survey.md",
                "response_schema": "response_schema_survey.json",
            },
        },
    )

    if args.dry_run:
        preview = out_dir / "sdk_visual_survey_prompt_preview.md"
        write_text(preview, prompt)
        return {"dry_run": True, "prompt_preview": str(preview), "media": media}

    client = make_client(args.api_key)
    _genai, types = import_sdk()
    try:
        uploaded = uploaded or upload_video(client, types, video, args.upload_timeout)
        parsed, raw_text, usage = generate_json_evidence(
            client,
            types,
            model=model,
            uploaded=uploaded,
            prompt=prompt,
            fps=fps,
            media_resolution=media_resolution,
            thinking_level=thinking_level,
            start=None,
            end=None,
            max_output_tokens=args.max_output_tokens,
            count_tokens=args.count_tokens,
            response_json_schema=schema,
        )
    finally:
        client.close()

    craft_events, layout_timeline, notes = survey_output_payload(
        parsed,
        raw_text,
        video=video,
        model=model,
        fps=fps,
        media_resolution=media_resolution,
        thinking_level=thinking_level,
    )
    write_json(out_dir / "visual_craft_events.json", craft_events)
    write_json(out_dir / "visual_layout_timeline.json", layout_timeline)
    write_text(out_dir / "visual_evidence_notes.md", notes)
    write_json(out_dir / "sdk_usage.json", {"survey": usage})
    write_analysis_markdown(out_dir, video)
    return {"survey": craft_events, "layout": layout_timeline, "usage": usage}


def run_micro(args: argparse.Namespace, uploaded: Any | None = None) -> dict[str, Any]:
    video = Path(args.video).expanduser().resolve()
    if not video.is_file():
        sys.exit(f"error: video not found: {video}")
    signals_dir = resolve_signals_dir(video, args.signals_dir)
    out_dir = resolve_out_dir(video, args.out_dir)
    media = load_media(signals_dir, video)
    all_spans = load_spans(signals_dir, media)
    boundary_map = load_boundary_map(signals_dir)
    selected_spans = select_spans(all_spans, args.span_ids, args.max_spans)
    config, body = load_template(Path(args.prompt).expanduser().resolve())
    model = args.model or config.get("model", DEFAULT_MODEL)
    base_fps = float(args.fps or config.get("fps", 12))
    review_fps = float(args.review_fps)
    adaptive_fps = not args.no_adaptive_fps
    media_resolution = normalize_media_resolution(
        args.media_resolution or config.get("media_resolution") or "HIGH"
    )
    thinking_level = args.thinking_level or config.get("thinking_level")
    signal_context = compact_signal_context(signals_dir)
    schema = visual_micro_schema()
    write_input_signal_artifact(out_dir, signal_context)
    write_json(out_dir / "response_schema_micro.json", schema)
    update_run_manifest(
        out_dir,
        {
            "video": str(video),
            "signals_dir": str(signals_dir),
            "out_dir": str(out_dir),
            "mode": "micro",
            "model": model,
            "micro": {
                "base_fps": base_fps,
                "review_fps": review_fps,
                "adaptive_fps": adaptive_fps,
                "media_resolution": media_resolution,
                "thinking_level": thinking_level,
                "prompt_dir": "prompts/",
                "response_schema": "response_schema_micro.json",
            },
        },
    )

    if args.dry_run:
        previews = []
        planned_spans = []
        for span in selected_spans:
            planned_fps, fps_reasons = choose_span_fps(
                span,
                boundary_map,
                base_fps=base_fps,
                review_fps=review_fps,
                adaptive_fps=adaptive_fps,
                short_span_seconds=args.short_span_seconds,
                low_confidence_threshold=args.low_confidence_threshold,
            )
            prompt = render_prompt(
                body,
                {
                    VIDEO_FILENAME_PLACEHOLDER: video.name,
                    ANALYSIS_CONTEXT_PLACEHOLDER: signal_context,
                    SPAN_CONTEXT_PLACEHOLDER: span_context(signals_dir, span, media),
                },
            )
            write_prompt_artifact(out_dir, f"micro_{span.get('signal_id')}", prompt)
            path = out_dir / f"sdk_micro_prompt_preview_{span.get('signal_id')}.md"
            write_text(path, prompt)
            previews.append(str(path))
            planned_spans.append(
                {
                    **span,
                    "planned_fps": planned_fps,
                    "planned_fps_reasons": fps_reasons,
                }
            )
        write_json(
            out_dir / "visual_micro_passes.json",
            {
                "schema_version": 1,
                "dry_run": True,
                "base_fps": base_fps,
                "review_fps": review_fps,
                "adaptive_fps": adaptive_fps,
                "thinking_level": thinking_level,
                "selected_spans": planned_spans,
                "prompt_previews": previews,
            },
        )
        return {"dry_run": True, "prompt_previews": previews}

    client = make_client(args.api_key)
    _genai, types = import_sdk()
    passes = []
    usage_by_span: dict[str, Any] = {}
    try:
        uploaded = uploaded or upload_video(client, types, video, args.upload_timeout)
        for span in selected_spans:
            start = float(span.get("start") or 0.0)
            end = float(span.get("end") or media_duration(media))
            span_fps, fps_reasons = choose_span_fps(
                span,
                boundary_map,
                base_fps=base_fps,
                review_fps=review_fps,
                adaptive_fps=adaptive_fps,
                short_span_seconds=args.short_span_seconds,
                low_confidence_threshold=args.low_confidence_threshold,
            )
            prompt = render_prompt(
                body,
                {
                    VIDEO_FILENAME_PLACEHOLDER: video.name,
                    ANALYSIS_CONTEXT_PLACEHOLDER: signal_context,
                    SPAN_CONTEXT_PLACEHOLDER: span_context(signals_dir, span, media),
                },
            )
            prompt_path = write_prompt_artifact(out_dir, f"micro_{span.get('signal_id')}", prompt)
            parsed, raw_text, usage = generate_json_evidence(
                client,
                types,
                model=model,
                uploaded=uploaded,
                prompt=prompt,
                fps=span_fps,
                media_resolution=media_resolution,
                thinking_level=thinking_level,
                start=start,
                end=end,
                max_output_tokens=args.max_output_tokens,
                count_tokens=args.count_tokens,
                response_json_schema=schema,
            )
            span_id = str(span.get("signal_id"))
            retry_payload = None
            retry_needed, retry_reasons = response_needs_high_fps_retry(
                parsed,
                low_confidence_threshold=args.low_confidence_threshold,
            )
            if (
                adaptive_fps
                and not args.no_rerun_low_confidence
                and retry_needed
                and span_fps < review_fps
            ):
                retry_parsed, retry_raw_text, retry_usage = generate_json_evidence(
                    client,
                    types,
                    model=model,
                    uploaded=uploaded,
                    prompt=prompt,
                    fps=review_fps,
                    media_resolution=media_resolution,
                    thinking_level=thinking_level,
                    start=start,
                    end=end,
                    max_output_tokens=args.max_output_tokens,
                    count_tokens=args.count_tokens,
                    response_json_schema=schema,
                )
                retry_payload = {
                    "fps": review_fps,
                    "retry_reasons": retry_reasons,
                    "raw_text": retry_raw_text if retry_parsed is None else None,
                    "evidence": retry_parsed,
                }
                usage = {"initial": usage, "retry": retry_usage}
                parsed = retry_parsed
                raw_text = retry_raw_text
                span_fps = review_fps
                fps_reasons = fps_reasons + [f"retry:{reason}" for reason in retry_reasons]
            usage_by_span[span_id] = usage
            passes.append(
                {
                    "span_id": span_id,
                    "start": start,
                    "end": end,
                    "start_timecode": span.get("start_timecode"),
                    "end_timecode": span.get("end_timecode"),
                    "model": model,
                    "fps": span_fps,
                    "base_fps": base_fps,
                    "review_fps": review_fps,
                    "fps_reasons": fps_reasons,
                    "media_resolution": media_resolution,
                    "thinking_level": thinking_level,
                    "prompt": str(prompt_path.relative_to(out_dir)),
                    "raw_text": raw_text if parsed is None else None,
                    "evidence": parsed,
                    "retry": retry_payload,
                }
            )
            payload = build_micro_payload(
                video=video,
                model=model,
                base_fps=base_fps,
                review_fps=review_fps,
                adaptive_fps=adaptive_fps,
                media_resolution=media_resolution,
                thinking_level=thinking_level,
                passes=passes,
            )
            write_micro_outputs(out_dir, video, payload, usage_by_span)
    finally:
        client.close()

    payload = build_micro_payload(
        video=video,
        model=model,
        base_fps=base_fps,
        review_fps=review_fps,
        adaptive_fps=adaptive_fps,
        media_resolution=media_resolution,
        thinking_level=thinking_level,
        passes=passes,
    )
    write_micro_outputs(out_dir, video, payload, usage_by_span)
    return payload


def build_micro_payload(
    *,
    video: Path,
    model: str,
    base_fps: float,
    review_fps: float,
    adaptive_fps: bool,
    media_resolution: str | None,
    thinking_level: str | None,
    passes: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "source": "gemini_sdk_visual_micro_passes",
        "video": video.name,
        "model": model,
        "base_fps": base_fps,
        "review_fps": review_fps,
        "adaptive_fps": adaptive_fps,
        "media_resolution": media_resolution,
        "thinking_level": thinking_level,
        "generated_at": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "gemini_role": "visual_evidence_extractor_only",
        "passes": passes,
    }


def write_micro_outputs(
    out_dir: Path,
    video: Path,
    payload: dict[str, Any],
    usage_by_span: dict[str, Any],
) -> None:
    write_json(out_dir / "visual_micro_passes.json", payload)
    merge_visual_craft_events(out_dir, payload)
    merge_sdk_usage(out_dir, {"micro": usage_by_span})
    write_analysis_markdown(out_dir, video)


def merge_visual_craft_events(out_dir: Path, micro_payload: dict[str, Any]) -> None:
    existing = read_json(out_dir / "visual_craft_events.json", {})
    events = list(existing.get("events", []))
    for item in micro_payload.get("passes", []):
        evidence = item.get("evidence")
        if isinstance(evidence, dict):
            for event in evidence.get("visual_craft_events", []):
                events.append(event)
    if not events:
        return
    unique_events: list[dict[str, Any]] = []
    seen = set()
    for event in events:
        key = event.get("evidence_id") or json.dumps(event, sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        unique_events.append(event)
    existing.update(
        {
            "schema_version": 1,
            "source": "gemini_sdk_visual_evidence_merged",
            "generated_at": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "gemini_role": "visual_evidence_extractor_only",
            "events": unique_events,
        }
    )
    write_json(out_dir / "visual_craft_events.json", existing)


def merge_sdk_usage(out_dir: Path, new_data: dict[str, Any]) -> None:
    path = out_dir / "sdk_usage.json"
    usage = read_json(path, {})
    usage.update(new_data)
    write_json(path, usage)


def run_extract(args: argparse.Namespace) -> None:
    video = Path(args.video).expanduser().resolve()
    ensure_shared_out_dir(args, video)
    survey_args = copy.copy(args)
    micro_args = copy.copy(args)
    micro_args.prompt = args.micro_prompt

    if args.dry_run:
        if args.include_survey:
            run_survey(survey_args)
        run_micro(micro_args)
        return

    client = make_client(args.api_key)
    _genai, types = import_sdk()
    try:
        uploaded = upload_video(client, types, video, args.upload_timeout)
    finally:
        client.close()

    if args.include_survey:
        run_survey(survey_args, uploaded=uploaded)
    run_micro(micro_args, uploaded=uploaded)


def build_codex_context(args: argparse.Namespace) -> None:
    video = Path(args.video).expanduser().resolve()
    signals_dir = resolve_signals_dir(video, args.signals_dir)
    out_dir = resolve_existing_out_dir(video, args.out_dir)

    files = {
        "media": signals_dir / "media.json",
        "transcript_words": signals_dir / "transcript.words.json",
        "speech_metrics": signals_dir / "speech_metrics.json",
        "audio_features": signals_dir / "audio_features.json",
        "prosody_features": signals_dir / "prosody_features.json",
        "prosody_segments": signals_dir / "prosody_segments.json",
        "candidate_beats": signals_dir / "candidate_beats.json",
        "edit_mechanisms": signals_dir / "edit_mechanisms.json",
        "visual_craft_events": out_dir / "visual_craft_events.json",
        "visual_layout_timeline": out_dir / "visual_layout_timeline.json",
        "visual_micro_passes": out_dir / "visual_micro_passes.json",
        "sdk_usage": out_dir / "sdk_usage.json",
    }
    visual_summary = {
        "visual_craft_events": read_json(files["visual_craft_events"], {}),
        "visual_layout_timeline": read_json(files["visual_layout_timeline"], {}),
        "visual_micro_passes": read_json(files["visual_micro_passes"], {}),
    }
    body = "\n".join(
        [
            "# Codex Viral Reasoning Context",
            "",
            f"Video: `{video}`",
            "",
            "Gemini SDK has only supplied visual evidence. Codex/GPT is responsible for the Viral Pattern, transfer logic, Recreation spec, and specialist-agent task cards.",
            "",
            "## Source Files",
            "",
            *[f"- `{name}`: `{path}`" for name, path in files.items()],
            "",
            "## Deterministic Timing Context",
            "",
            compact_signal_context(signals_dir),
            "",
            "## Gemini SDK Visual Evidence",
            "",
            "```json",
            json.dumps(visual_summary, indent=2, sort_keys=True),
            "```",
            "",
            "## Codex Reasoning Prompt",
            "",
            f"Use `{DEFAULT_CODEX_PROMPT}` as the downstream high-reasoning prompt template.",
        ]
    )
    write_text(out_dir / "codex_reasoning_context.md", body)


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("video", help="path to the Exemplar video")
    parser.add_argument("--signals-dir", help="directory containing deterministic signal files")
    parser.add_argument(
        "--out-dir",
        help=(
            "directory for SDK evidence outputs; default is "
            "exemplars/<slug>/gemini_runs/sdk/<run_id>"
        ),
    )
    parser.add_argument("--model", help=f"Gemini API model (default: {DEFAULT_MODEL})")
    parser.add_argument("--api-key", help="Gemini API key; env vars also work")
    parser.add_argument("--upload-timeout", type=float, default=180.0)
    parser.add_argument("--dry-run", action="store_true", help="render prompts without calling Gemini")


def add_generation_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--fps", type=float, help="video FPS sent to Gemini")
    parser.add_argument(
        "--review-fps",
        type=float,
        default=24.0,
        help="higher FPS for short/review spans or low-confidence retries",
    )
    parser.add_argument(
        "--short-span-seconds",
        type=float,
        default=1.0,
        help="spans at or below this duration use review FPS when adaptive FPS is enabled",
    )
    parser.add_argument(
        "--low-confidence-threshold",
        type=float,
        default=0.7,
        help="confidence below this threshold triggers review FPS/retry logic",
    )
    parser.add_argument(
        "--no-adaptive-fps",
        action="store_true",
        help="disable automatic review-FPS selection for short/review spans",
    )
    parser.add_argument(
        "--no-rerun-low-confidence",
        action="store_true",
        help="do not rerun a 12 FPS span at review FPS when Gemini returns low confidence",
    )
    parser.add_argument("--media-resolution", help="LOW, MEDIUM, HIGH, or MEDIA_RESOLUTION_*")
    parser.add_argument(
        "--thinking-level",
        choices=["minimal", "low", "medium", "high"],
        help="Gemini 3.x thinking level; use high for deeper visual inspection tests",
    )
    parser.add_argument("--max-output-tokens", type=int, default=8192)
    parser.add_argument("--count-tokens", action="store_true", help="call count_tokens before generation")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="gemini_sdk_video",
        description="Official Gemini SDK visual evidence extractor",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    survey = sub.add_parser("survey", help="whole-video visual evidence survey")
    add_common_arguments(survey)
    add_generation_arguments(survey)
    survey.add_argument("--prompt", default=str(DEFAULT_SURVEY_PROMPT))
    survey.set_defaults(func=run_survey)

    micro = sub.add_parser("micro", help="per-shot/per-span high-FPS visual evidence passes")
    add_common_arguments(micro)
    add_generation_arguments(micro)
    micro.add_argument("--prompt", default=str(DEFAULT_MICRO_PROMPT))
    micro.add_argument("--span-ids", help="comma-separated edit_span IDs to analyze")
    micro.add_argument("--max-spans", type=int, default=24)
    micro.set_defaults(func=run_micro)

    extract = sub.add_parser("extract", help="run survey and micro passes")
    add_common_arguments(extract)
    add_generation_arguments(extract)
    extract.add_argument("--prompt", default=str(DEFAULT_SURVEY_PROMPT))
    extract.add_argument("--micro-prompt", default=str(DEFAULT_MICRO_PROMPT))
    extract.add_argument("--span-ids", help="comma-separated edit_span IDs to analyze")
    extract.add_argument("--max-spans", type=int, default=24)
    extract.add_argument(
        "--include-survey",
        action="store_true",
        help="also run the optional whole-video 5 FPS survey before micro passes",
    )
    extract.set_defaults(func=run_extract)

    codex = sub.add_parser("build-codex-context", help="write a Codex reasoning handoff context")
    add_common_arguments(codex)
    codex.set_defaults(func=build_codex_context)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
