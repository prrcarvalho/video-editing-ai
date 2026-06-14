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
├── refresh_cookies.py   # recovery: re-harvest cookies via a dedicated Chrome profile
├── dump_models.py       # debug: dumps the raw model-registry RPC
├── prompts/default.md   # default prompt template
└── outputs/             # generated reports land here by default
```

As of 2026-06, `<repo>` = `/Users/pedrocarvalho/projects/video_editing_ai/main`. The folder may move; if that path is stale, locate it with `find ~/projects -maxdepth 4 -type d -name gemini_pipeline`. All commands below assume you `cd` into `gemini_pipeline/` first.

## Quick start

```bash
cd <repo>/gemini_pipeline
uv run gemini_video.py analyze /path/to/video.mp4 \
    --prompt /path/to/my_prompt.md \
    --model gemini-3-flash-thinking
```

Upload + analysis of a short video takes a few minutes (~2 min for a 10 MB clip). Either run it in the background and watch for the final `wrote <path>` line, or run it in the foreground with a generous timeout (≥600 s) — both work; the script prints the model and video size, then blocks until the response arrives.

Model availability varies per account and over time — `gemini-3-flash-thinking` and `gemini-3-pro` have intermittently shown as NOT AVAILABLE. Run the `models` command (below) to see what works right now rather than assuming.

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
- The body below the frontmatter is sent verbatim as the prompt. No other substitutions exist.
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
| `--temporary` | keep the chat out of the user's Gemini history |
| `--no-thoughts` | omit the thinking trace from the output file |
| `-v` | debug logging (put it BEFORE the subcommand: `gemini_video.py -v analyze ...`) |

## Caveats for agents

- Timestamps in video analyses come from Gemini's frame sampling — treat sub-second precision as approximate, and sanity-check beat-level claims against the actual video before building on them.
- The upload goes to the user's personal Google account. Don't upload videos the user hasn't asked you to, and use `--temporary` if they don't want it in their Gemini history.
- One video per call; the script takes exactly one file.
- Don't run two `analyze`/`models` commands concurrently — parallel cookie rotation can invalidate the session server-side and both env-file writes race.

## Worked example

Read `references/case-study.md` for a complete real run — an Instagram reel deconstructed with a custom retention-engineering prompt, including the auth failure that happened, how it was diagnosed, and what the output looked like. Follow that shape when running your own analyses.
