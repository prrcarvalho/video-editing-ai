---
name: gemini-video-analysis
description: Analyze a video file with Google Gemini using the gemini_pipeline CLI — uploads an mp4 plus a markdown prompt template to the Gemini web app and writes the model's full response to a markdown report. Use whenever the user wants to run a video through Gemini, analyze/deconstruct/ingest a video or reel with an LLM, run a prompt template against a video file, pick between Gemini model variants for video analysis, or mentions gemini_video.py, gemini_pipeline, or "upload this video to Gemini". Also use when debugging UNAUTHENTICATED/cookie errors from gemini-webapi.
---

# Gemini Video Analysis Pipeline

`gemini_video.py` is a self-contained PEP 723 Python script (run it with `uv run`, no venv setup needed). It uploads a video to the **Gemini web app** — your personal Google account via session cookies, NOT the official Gemini API — runs a markdown prompt template against it, and writes the full response to a markdown file. Because it rides the web app, it's free, but auth is cookie-based and the model names are aliases (see below).

## Where the pipeline lives

Currently a POC at:

```
<repo>/gemini_pipeline/
├── gemini_video.py      # the CLI
├── gemini_sdk_video.py  # official Gemini API visual evidence extractor
├── refresh_cookies.py   # recovery: re-harvest cookies via a dedicated Chrome profile
├── dump_models.py       # debug: dumps the raw model-registry RPC
├── prompts/default.md   # default prompt template
└── outputs/             # generated reports land here by default
```

As of 2026-06, `<repo>` = `/Users/pedrocarvalho/projects/video_editing_ai`. Do not add or assume a `main/` subfolder. If the path is stale, locate it with `find ~/projects -maxdepth 4 -type d -name gemini_pipeline`. All commands below assume you `cd` into `gemini_pipeline/` first.

## Quick start

```bash
cd <repo>/gemini_pipeline
uv run gemini_video.py analyze /path/to/video.mp4 \
    --prompt /path/to/my_prompt.md \
    --model gemini-3-flash-thinking
```

Upload + analysis of a short video takes a few minutes (~2 min for a 10 MB clip). Either run it in the background and watch for the final `wrote <path>` line, or run it in the foreground with a generous timeout (≥600 s) — both work; the script prints the model and video size, then blocks until the response arrives.

Model availability varies per account and over time — `gemini-3-flash-thinking` and `gemini-3-pro` have intermittently shown as NOT AVAILABLE. Run the `models` command (below) to see what works right now rather than assuming.

## Signal-grounded Exemplar workflow

For Exemplar analysis, do not ask Gemini to be the stopwatch. Generate the local signal pack first, render/check the prompt locally if needed, then upload the video plus `signals_for_gemini.md` with the signal-grounded prompt.

In signal-grounded reports, keep WPM and BPM distinct. WPM is speech pace from WhisperX word timings: how fast the speaker/narrator is talking. BPM is mixed-audio rhythmic tempo from librosa: the dominant pulse of the music bed, rhythmic SFX, edit accents, or whole waveform.

Keep prosody layers distinct too. `prosody_features.json` is a whole-video
openSMILE summary, useful for the global delivery fingerprint but not exact
word timing. `prosody_segments.json` is the time-aligned delivery artifact:
it aggregates openSMILE functionals and WPM over WhisperX transcript segments.
SDK prompts may use `prosody_seg_*` IDs as sync anchors for visible edit timing,
but Gemini SDK must not turn prosody into virality reasoning or strategy.

For human evidence review, prefer Resolve-style timecodes from the signal pack:
`MM:SS:FF` (or `HH:MM:SS:FF` for long videos) plus the frame number.
The final field is frames at the media FPS, not decimal seconds. For example,
on a 60 FPS timeline, `00:02:21` means 2 seconds + 21 frames = 2.35 seconds,
not 2.21 seconds. Do not present decimal seconds as the primary evidence
location; decimal seconds are kept in JSON for machine math only. If Gemini
emits `start_seconds` or `end_seconds`, treat those as untrusted unless the
pipeline has normalized them from deterministic signal IDs, frame numbers, and
media FPS.

The signal pack also includes `edit_mechanisms.json`. It is shot-boundary/timing evidence only, with no OCR. Gemini should use `edit_boundary_*`, `edit_span_*`, and `sync_*` IDs when it claims a hard cut, candidate cut, shot span, pacing rhythm, or boundary/audio/word synchronization. Gemini must not cite this file as deterministic proof of punch-in/punch-out, digital zoom, crop shift, pan/scroll, split-screen layout, overlay, or VFX. Those are semantic visual-review claims anchored to the relevant shot span/keyframe and should be marked `needs_review` when uncertain.

Short-form viral content means the user asks about a reel, TikTok, Short, Instagram/YouTube short-form clip, viral pattern, fast-paced social video, or a vertical clip around social length. Use the learned short-video detector in addition to PySceneDetect:

```bash
cd <repo>
uv run scripts/exemplar_ingest.py assets/instagram-real.MP4 \
    --force \
    --autoshot-device auto \
    --autoshot-download-kaggle
```

`exemplar_ingest.py` defaults to `--content-profile auto`, which enables
AutoShot for vertical social-length videos. Use `--content-profile short-form`
to force AutoShot on for a short-form Exemplar that does not match the auto
shape/duration heuristic, or `--no-autoshot` only when explicitly testing the
PySceneDetect/OpenCV baseline.

Long-form content means podcasts, tutorials, YouTube long-form, webinars, calls, demos, or videos where shot boundaries are slower and semantic segmentation matters more than reel micro-cuts. Default to PySceneDetect/OpenCV only; do not add AutoShot unless the user explicitly asks to test short-form shot-boundary detection on it:

```bash
cd <repo>
uv run scripts/exemplar_ingest.py /path/to/long-form.mp4 --force --content-profile long-form
```

Then run Gemini with the signal-grounded prompt and context:

```bash
cd <repo>/gemini_pipeline
uv run gemini_video.py analyze ../assets/instagram-real.MP4 \
    --prompt prompts/PROMPT-GEMINI-SIGNAL-GROUNDED.md \
    --context outputs/instagram-real/signals/signals_for_gemini.md \
    --model gemini-3-flash
```

## Official SDK visual evidence workflow

For fast-paced short-form content where the user cares about punch-ins, zoom
ramps, crop shifts, scrolling, cursor/click indicators, overlays, transitions,
VFX, split-screen structure, or other fast visual mechanics, use the official
Gemini SDK path after deterministic ingest.

This path is API-key based and separate from the Gemini web-app cookie path.
It accepts `--api-key`, exported `GEMINI_API_KEY` / `GOOGLE_API_KEY`, or the
local private env file `~/gemini_api_key.env` / `~/.gemini_api_key.env`.
Gemini SDK is only the visual evidence extractor. Codex/GPT is the
high-reasoning stage that turns evidence into the Viral Pattern, Beat Sheet,
Recreation plan, and specialist-agent task cards.

Default command for a fast Exemplar:

```bash
cd <repo>/gemini_pipeline
uv run gemini_sdk_video.py extract ../assets/instagram-real.MP4 \
    --signals-dir outputs/instagram-real/signals \
    --count-tokens
```

By default, `extract` skips the whole-video survey and analyzes the shot spans
directly. This keeps the production path focused on the high-FPS evidence that
matters for fast edits. Add `--include-survey` only when a cheap global layout
map is useful:

```bash
uv run gemini_sdk_video.py extract ../assets/instagram-real.MP4 \
    --signals-dir outputs/instagram-real/signals \
    --include-survey \
    --count-tokens
```

For targeted checks such as "did the editor punch in / zoom / reframe right
after the cut?", use the rate-limit-friendly post-cut motion test instead of
re-running broad micro spans:

```bash
uv run gemini_sdk_video.py post-cut-motion ../assets/instagram-real.MP4 \
    --signals-dir outputs/instagram-real/signals \
    --dry-run
```

Then remove `--dry-run` to call the API. This command sends one compact
boundary-local context per `edit_boundary_*` plus a short video offset window,
instead of the full signal bundle. It defaults to 24 FPS, medium media
resolution, `thinking_level: medium`, sequential requests with a 12s sleep for
free-tier RPM pacing, and retry handling for retryable 429 /
RESOURCE_EXHAUSTED errors. Use `--boundary-ids edit_boundary_0002,...` for a
small manual test, `--hard-cuts-only` to skip candidate cuts, and
`--request-sleep-seconds` / `--max-retries` when tuning rate-limit behavior.

Outputs are evidence artifacts under the Exemplar SDK run folder, not inside
`signals/`:

```text
<repo>/exemplars/<exemplar_slug>/gemini_runs/sdk/<run_id>/
```

| file | purpose |
|------|---------|
| `analysis.md` | human-readable Visual Evidence Pack for Resolve side-by-side inspection |
| `prompt.md` + `prompts/*.md` | prompt index plus exact rendered SDK prompts |
| `input_signals_for_gemini.md` | compact deterministic signal context sent to Gemini |
| `run_manifest.json` | model/config/artifact manifest for the SDK run |
| `response_schema_survey.json` / `response_schema_micro.json` | strict JSON schemas sent through the official SDK |
| `visual_craft_events.json` | visible motion/edit/VFX/layout/interaction evidence |
| `visual_layout_timeline.json` | layout/layer timeline by anchored span |
| `visual_micro_passes.json` | per-span high-FPS Gemini observations |
| `sdk_usage.json` | token counts and usage metadata from the official API |
| `visual_evidence_notes.md` | short uncertainty notes or raw fallback text |

Then create the Codex reasoning handoff:

```bash
uv run gemini_sdk_video.py build-codex-context ../assets/instagram-real.MP4 \
    --signals-dir outputs/instagram-real/signals
```

When `--out-dir` is omitted, `build-codex-context` reads the latest SDK run for
that Exemplar. Pass `--out-dir <sdk_run_dir>` to target a specific run. This
writes `codex_reasoning_context.md`, which Codex/GPT should use with
`prompts/PROMPT-CODEX-VIRAL-REASONING.md`.

SDK defaults:

- `survey`: optional whole-video pass at 5 FPS, high media resolution,
  `thinking_level: medium`.
- `micro`: per-shot/span passes at 12 FPS, high media resolution.
- Use `--thinking-level high` when testing higher-fidelity Gemini 3.5 Flash
  visual inspection. Do not tune `temperature`, `top_p`, or `top_k` for Gemini
  3.x visual evidence passes; use strict prompts, structured JSON, and
  `thinking_level` instead.
- SDK generation uses `response_mime_type: application/json` plus a strict
  `response_json_schema`. The model returns structured evidence; the local tool
  renders `analysis.md` from that JSON for human review.
- The SDK edit-mechanics taxonomy is only a controlled label vocabulary. It is
  grounded by the deterministic ingest that runs before Gemini: WhisperX
  `word_*` timings, WPM/speech metrics, `prosody_seg_*` delivery rows,
  candidate `beat_*` rows, audio/onset/sync rows, and `edit_span_*` /
  `edit_boundary_*` shot evidence.
- Every SDK layout/effect claim should cite supplied IDs in `anchor_signal_ids`
  and grouped `grounding_constraints`. If Gemini sees a visible mechanic
  between anchors, bind it to the nearest supplied span/word/beat/prosody/cut
  IDs and mark `needs_review` when timing cannot be verified.
- The visual evidence taxonomy includes cuts/transitions, keyframed framing
  motion, camera motion, speed/time effects, captions/text states, graphics,
  screen/UI interactions, VFX/compositing, color/light changes, and
  audio-visible sync. `craft_function_hypothesis` is allowed only as a
  constrained craft-purpose label, never as virality reasoning.
- Adaptive FPS is enabled by default for `micro`: spans at or below 1 second,
  spans touching candidate/review boundaries, and spans touching low-confidence
  boundaries use 24 FPS.
- If a 12 FPS micro pass returns low confidence or `needs_review`, the tool can
  rerun that same span at 24 FPS unless `--no-rerun-low-confidence` is set.
- Use `--dry-run` first when checking prompt rendering without calling the API.

Prompt rule: Gemini SDK prompts must not ask for virality reasoning, strategy,
a final report, a Beat Sheet, or a Recreation spec. They should return
structured evidence with signal IDs, confidence, and `needs_review`.
Do not ask Gemini SDK to calculate decimal seconds from `MM:SS:FF` timecodes;
`MM:SS:FF` is Resolve-style frame timecode. Downstream code or Codex should
derive seconds from the cited signal IDs and frame numbers when seconds are
needed.

AutoShot guidance:

- Keep PySceneDetect as the baseline hard-cut detector. AutoShot is an additional learned short-form signal, not a replacement.
- Treat high-confidence `autoshot_cut_*` events as learned visual-cut evidence.
- Treat low-threshold `autoshot_candidate_*` events as review/keyframe/Beat Sheet anchors, not canonical cuts.
- On Apple Silicon, `--autoshot-device auto` should use MPS when possible; the ingest script enables PyTorch MPS CPU fallback before Torch imports.

PySceneDetect 0.7 guidance:

- Use/pin `scenedetect>=0.7,<0.8`; the old `scenedetect[opencv]` extra is not needed in 0.7.
- PySceneDetect 0.7 overhauled timestamp handling for VFR videos. Use `FrameTimecode.seconds` and `frame_rate`; avoid deprecated `get_seconds()`/`framerate` forms in project code.
- Cast `frame_rate`/`FrameTimecode` values explicitly when JSON, formatting, or float math requires a `float`.

## Auth (self-maintaining)

Cookies are managed automatically — no `source`, no hand-copying, no cache clearing:

1. `gemini_video.py` reads `~/.gemini_cookies.env` itself, and after **every** run (even failed ones) writes any rotated `__Secure-1PSIDTS` back to that file (atomically, mode 600, still `source`-able). A stderr line `[gemini_video] rotated __Secure-1PSIDTS persisted to ...` confirms a rotation was captured.
2. Env vars `GEMINI_1PSID` / `GEMINI_1PSIDTS` still take precedence over the file, so `source ~/.gemini_cookies.env` or one-off overrides keep working.
3. The library's rotated-cookie cache lives at `~/.cache/gemini_webapi/` (not volatile `$TMPDIR`), and the script reconciles it automatically: if the env file was hand-edited, the stale cache is deleted before init. Never `rm` it manually.
4. **If the session is fully dead, recovery is automatic too**: on an `AuthError` or an upload failing with API error 1100, `gemini_video.py` runs `refresh_cookies.py` itself, then retries the command once. A Chrome window flashes for a few seconds during the re-harvest — that's normal. You can also run it by hand anytime:

```bash
uv run refresh_cookies.py
```

It uses a dedicated pipeline-owned Chrome profile (`~/.gemini_pipeline_chrome`, its own Google session — decoupled from the user's daily Chrome). **Only intervention ever needed**: if that profile's own Google session was revoked (password change, security sweep), the window shows a Google login instead of closing — the user must complete it (the script waits 5 min by default, `--login-timeout SECS` to extend). So if a run seems to hang after "re-harvesting cookies", tell the user to check for a Chrome login window. Last resort if all else fails: hand-copy `__Secure-1PSID`/`__Secure-1PSIDTS` from DevTools into `~/.gemini_cookies.env`. Never echo cookie values into the chat or logs.

Why this split works — two distinct failure modes:

- **Stale 1PSIDTS, live session** (the common case): Google usually re-issues a fresh token during the init handshake. Symptom: one or two UNAUTHENTICATED warnings, then the run succeeds and auto-persists the new value. Self-healing; do nothing.
- **Session revoked or cookies invalid**: nothing left to rotate. Crucially, this does NOT fail loudly at init — the library degrades silently into a half-dead session where read RPCs still work (`models` lists fine, usually with a warning and with `flash-thinking`/`pro` showing NOT AVAILABLE) but uploads fail with error 1100. That 1100 is what triggers the auto-recovery above. So: **models listing + NOT AVAILABLE on models the account normally has = degraded auth**, expect the next `analyze` to recover itself.

Cheap auth check before committing to a multi-minute upload:

```bash
uv run gemini_video.py models
```

Reading the warnings:

- **One UNAUTHENTICATED warning, then normal progress** — benign; the library recovered. Let it run.
- **`AuthError` or `APIError ... 1100`** — handled automatically: the script re-harvests cookies and retries once (window flash is expected). You only act if the automatic attempt also fails: then run `uv run refresh_cookies.py` by hand and check for a pending Google login in its window.
- **The same warning repeating 2–3+ times with no progress** — kill it, run `uv run gemini_video.py models` to see the session state, and let the next `analyze` trigger auto-recovery (or run `refresh_cookies.py` directly).

## Models

List what the account can use, with the alias → actual mapping:

```bash
uv run gemini_video.py models
```

The library's model names are **stale aliases** — Google upgrades models in place behind the same internal id, so the name understates what actually runs. As of 2026-06:

| `--model` value           | actually runs | use for |
|---------------------------|---------------|---------|
| `gemini-3-flash`          | 3.5 Flash     | fast, cheap passes |
| `gemini-3-flash-thinking` | 3.5 Thinking  | default — best quality/speed for analysis |
| `gemini-3-pro`            | 3.1 Pro       | when thinking-model output isn't enough |

Re-run `models` rather than trusting this table — the mapping drifts as Google ships. (`dump_models.py` dumps the raw RPC if you need the versioned name per id.)

Model resolution order: `--model` flag → `model:` in the prompt template's frontmatter → hardcoded default (`gemini-3-flash-thinking`).

## Prompt templates

A template is a markdown file, optionally with YAML frontmatter:

```markdown
---
model: gemini-3-flash-thinking   # optional default model
timeout: 900                     # optional request timeout (seconds)
---

You are a senior video editor analyzing the attached video ({{video_filename}}).
... rest of the prompt ...
```

- `{{video_filename}}` is replaced with the video's filename — useful so the model knows what file it's looking at.
- `{{analysis_context}}` is replaced by the markdown file passed with `--context`; signal-grounded prompts should require this.
- The body below the frontmatter is sent verbatim as the prompt after supported substitutions.
- Omitting `--prompt` automatically uses `prompts/default.md` (a general "senior video editor" breakdown). Any markdown file works via `--prompt` — it does NOT need frontmatter (a plain markdown prompt is fine; flags/defaults fill in model and timeout).

## Output

The response is written to `<out_dir>/<video-stem>_<UTC timestamp>.md` (default out_dir: `gemini_pipeline/outputs/`, override with `--out`). Structure:

```markdown
---
video: instagram-real.MP4
model: gemini-3-flash-thinking
prompt_template: /path/to/prompt.md
generated_at: 20260612T152106Z
---

<details><summary>Model thinking</summary> ... </details>

<the model's full response>
```

The script's last stdout line is `wrote <path>` — parse that for the definitive output location rather than guessing the timestamp.

## Useful flags

| flag | effect |
|------|--------|
| `--model NAME` | override model from template frontmatter |
| `--out DIR` | output directory (created if missing) |
| `--timeout SECS` | request timeout (default 900; videos take minutes) |
| `--context PATH` | markdown context used to replace `{{analysis_context}}` in signal-grounded prompts |
| `--temporary` | keep the chat out of the user's Gemini history; do not use unless the user explicitly asks for temporary/private/no-history mode |
| `--no-thoughts` | omit the thinking trace from the output file |
| `-v` | debug logging (put it BEFORE the subcommand: `gemini_video.py -v analyze ...`) |

## Caveats for agents

- Timestamps in video analyses come from Gemini's frame sampling — treat sub-second precision as approximate, and sanity-check beat-level claims against the actual video before building on them.
- The upload goes to the user's personal Google account. Don't upload videos the user hasn't asked you to. By default, do NOT use `--temporary`; only add it when the user explicitly asks for temporary/private/no-history mode.
- One video per call; the script takes exactly one file.
- Don't run two `analyze`/`models` commands concurrently — parallel cookie rotation can invalidate the session server-side and both env-file writes race.

## Worked example

Read `references/case-study.md` for a complete real run — an Instagram reel deconstructed with a custom retention-engineering prompt, including the auth failure that happened, how it was diagnosed, and what the output looked like. Follow that shape when running your own analyses.
