# Case study: deconstructing an Instagram reel (2026-06-12)

A complete real run, including the auth failure that happened on the way. Follow this shape when running your own analyses — **but note the auth/cookie handling described here is HISTORICAL**: later that same day, cookie management was automated (auto-persist of rotated cookies in `gemini_video.py`, recovery via `refresh_cookies.py`). The `source` / hand-copy / `rm`-the-cache steps below no longer apply — see SKILL.md "Auth (self-maintaining)" for the current flow. The prompt-template, model-picking, and output-reading parts remain accurate.

## The task

> "Use PROMPT-GEMINI.md as the prompt and instagram-real.MP4 as the video to ingest, use gemini 3 flash thinking, tell me where the output was written."

- Video: `instagram-real.MP4`, 9.8 MB, a 24-second Instagram reel about Claude Code.
- Prompt: `PROMPT-GEMINI.md`, a ~100-line "short-form retention engineer" framework — plain markdown, **no frontmatter** (templates don't need it; model came from the `--model` flag). It demanded a timestamp for every claim, `[INFERRED]` markers for anything not directly observed, and five deliverables (hook autopsy, beat sheet, audio/emotion arc, structure analysis, scorecard + replication spec).

## What was run, in order

### 1. First attempt — failed on auth

```bash
cd <repo>/gemini_pipeline
uv run gemini_video.py analyze /path/to/instagram-real.MP4 \
    --prompt /path/to/PROMPT-GEMINI.md \
    --model gemini-3-flash-thinking
```

No env vars set, so the script fell back to browser-cookie3 auto-detection. Output was an endless loop of:

```
WARNING | gemini_webapi.client:_fetch_user_status:402 - Account status: UNAUTHENTICATED - Session is not authenticated or cookies have expired.
```

Lesson: this loop never recovers. Kill the process as soon as you see it repeat 2–3 times.

### 2. Fresh cookies — STILL failed

The user copied fresh `__Secure-1PSID` / `__Secure-1PSIDTS` values from Chrome DevTools into `~/.gemini_cookies.env`. Re-ran with `source ~/.gemini_cookies.env && ...` — **same UNAUTHENTICATED loop**, even though the cookies were verifiably fresh and complete.

### 3. Root cause: the library's cookie cache

Grepping the gemini-webapi source showed it caches rotated cookies at `$TMPDIR/gemini_webapi/.cached_cookies_<1PSID>.json` and loads the cache **in preference to** explicitly passed values. A cache file from a run earlier that day held a stale rotated `1PSIDTS` for the same `1PSID`, poisoning every subsequent run.

```bash
rm "${TMPDIR:-/tmp}/gemini_webapi/".cached_cookies_*.json
```

### 4. Cheap auth verification before retrying the upload

```bash
source ~/.gemini_cookies.env && uv run gemini_video.py models
```

```
  gemini-3-flash                       -> 3.5 Flash (free)
  gemini-3-flash-thinking              -> 3.5 Thinking (free)
  gemini-3-pro                         -> 3.1 Pro (free)
```

Auth confirmed in seconds instead of discovering failure minutes into an upload. Note the alias → actual mapping: the requested "gemini 3 flash thinking" actually ran **Gemini 3.5 Thinking**.

### 5. Successful run

```bash
source ~/.gemini_cookies.env && uv run gemini_video.py analyze \
    /Users/pedrocarvalho/projects/video_editing_ai/instagram-real.MP4 \
    --prompt /Users/pedrocarvalho/projects/video_editing_ai/PROMPT-GEMINI.md \
    --model gemini-3-flash-thinking
```

stdout:

```
model:  gemini-3-flash-thinking
video:  /Users/pedrocarvalho/projects/video_editing_ai/instagram-real.MP4 (9.8 MB)
uploading and generating... (this can take a few minutes)

wrote /Users/pedrocarvalho/projects/video_editing_ai/hyper_frames_test_reel/gemini_pipeline/outputs/instagram-real_20260612T152106Z.md
```

Total wall time ~3 minutes for a 9.8 MB / 24-second clip. The run was launched in the background and the final `wrote <path>` line was used as the definitive output location.

## What the output looked like

A 175-line markdown file: YAML frontmatter (video, model, prompt_template, generated_at), a collapsed `<details>` thinking trace, then the model's response following the prompt's requested structure. Excerpt:

```markdown
## A. HOOK AUTOPSY

* **Hook End Point:** 00:01.3. The video transitions from the negative positioning
  statement ("the wrong way") to explaining common behavior ("They open it...").
* **First Spoken Words:** "Most people use Claude Code the wrong way." (00:00.0)
* **Hook Classification:** Contrarian / Frame-breaking.
...

## B. FULL BEAT SHEET

*Note: Due to standard video player playback, frame sampling precision is limited
to approximately ± 0.1 seconds.*

| t | Visual / b-roll / VFX | Cut or motion type | On-screen text | ... |
| **00:00.0** | Speaker center frame, code overlay top left | Direct cut | "use claude code" | ... |
| **00:01.3** | Screen share: Terminal window with input cursor | Hard cut | "type what" | ... |
...

### Retentive Metrics & Patterns
* **Average Shot Length (ASL):** Overall ASL is **1.41 seconds** (17 visual cuts /
  changes over 24.0 seconds). The opening section (00:00.0 - 00:05.8) moves faster
  with an ASL of **1.16 seconds**.
* **Audiovisual Sync:** Cut points and caption updates are precisely aligned to
  spoken word transients [INFERRED]. Dedicated SFX drops are not utilized.
```

Two things worth noting about output quality:

- A well-structured prompt template directly shaped a well-structured response — the model honored the table format, the `[INFERRED]` marking convention, and even volunteered its own frame-sampling precision limit (±0.1s) because the prompt told it to admit sampling limits rather than guess.
- The per-beat timestamps (00:00.7, 00:01.3, …) are plausible but derived from sparse frame sampling — they were reported to the user with the caveat to spot-check against the real video before using them to drive an automated editing pipeline.

## Postscript: what a second agent's run added (same day)

A fresh agent following this skill reproduced the flow with `gemini-3-flash` and the default template, and hit two refinements now reflected in SKILL.md:

- `models` printed the model list **and** one UNAUTHENTICATED warning; treating that as "auth works" led to `analyze` crashing with `APIError: Unknown API error code: 1100`. The cache is rewritten by *every* run, so the fix is clearing it in the same command as the `analyze` invocation.
- Its `models` output showed `gemini-3-flash-thinking` and `gemini-3-pro` as NOT AVAILABLE on the account that morning had run flash-thinking fine — availability fluctuates; always check live.

## Checklist distilled from these runs (updated to the current auto-cookie flow)

1. `uv run gemini_video.py models` — verify auth (no UNAUTHENTICATED warnings at all) + see which aliases actually run and are available right now. No `source` needed; the script reads `~/.gemini_cookies.env` itself.
2. `AuthError` / error 1100 recover **automatically** (the script runs `refresh_cookies.py` and retries once; a Chrome window flash is expected). Only intervene if that also fails — then run `uv run refresh_cookies.py` by hand and check its window for a pending Google login. (Do NOT `rm` cookie caches by hand — the script reconciles them.)
3. Run `analyze` in the background (or foreground with ≥600 s timeout); it takes minutes.
4. Take the output path from the final `wrote <path>` stdout line.
5. Report timestamps from the analysis as approximate.

### Postscript 2 (same day, evening): the cookie automation itself

The dying session described above eventually went **dead beyond rotation**: `models` still listed models (read-only RPCs worked) but every `analyze` upload failed with error 1100 — fresh hand-copied cookies could not fix it. `refresh_cookies.py` (dedicated Chrome profile, one-time login) recovered it in one run, after which `models` printed with **zero** warnings and the previously NOT-AVAILABLE `gemini-3-flash-thinking`/`gemini-3-pro` became available again. Lesson: a half-dead session can also shrink model availability; a clean re-login restores both auth and the full model list.
