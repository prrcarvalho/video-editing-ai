# AGENTS.md

## Signal-Grounded Gemini Notes

- Signal-grounded analysis uses `PROMPT-GEMINI-SIGNAL-GROUNDED.md` plus `gemini_video.py analyze --context <signals_for_gemini.md>`; the signal pack is the stopwatch, Gemini is the semantic analyst.
- For production analysis of fast-paced short-form visual craft, prefer the official SDK path: `gemini_sdk_video.py extract <video> --signals-dir <signals>`. This creates evidence files for Codex/GPT to reason over, not a final Viral Pattern report. `extract` is micro-first by default; add `--include-survey` only when a whole-video 5 FPS survey is useful. SDK outputs belong under `exemplars/<slug>/gemini_runs/sdk/<run_id>/`, not under `signals/`.
- The SDK API key can come from `--api-key`, exported `GEMINI_API_KEY` /
  `GOOGLE_API_KEY`, or the private local env file `~/gemini_api_key.env` /
  `~/.gemini_api_key.env`. Never print key values in logs or chat.
- For Gemini 3.5 Flash SDK tests, control visual-inspection effort with `--thinking-level`. Use the prompt default `medium` for normal survey/micro passes and `--thinking-level high` when comparing higher-fidelity evidence extraction. Leave `temperature`, `top_p`, and `top_k` unset for Gemini 3.x.
- SDK visual evidence uses strict `response_json_schema` artifacts and renders a
  local `analysis.md` for human inspection. Keep Gemini's direct output as JSON
  evidence; do not ask the SDK pass to free-write a final Markdown report.
- SDK runs should preserve `input_signals_for_gemini.md`, `prompt.md`,
  `prompts/*.md`, `run_manifest.json`, response schema JSON files, and
  `analysis.md` whenever practical.
- Keep the model roles separate: deterministic ingest is the stopwatch, Gemini SDK is the high-FPS visual evidence extractor, and Codex/GPT is the high-reasoning stage that writes the Viral Pattern, Beat Sheet, Recreation instructions, and specialist-agent task cards.
- The SDK edit-mechanics taxonomy is only a controlled label vocabulary. It
  must be grounded in deterministic inputs from the prior ingest: WhisperX
  `word_*` timings, WPM/speech metrics, `prosody_seg_*` delivery rows,
  candidate `beat_*` rows, audio/onset/sync rows, and `edit_span_*` /
  `edit_boundary_*` shot evidence.
- Gemini SDK evidence prompts must not ask for virality reasoning, strategy, a Recreation spec, or a Beat Sheet. They should describe visible layout, motion, edits, VFX, cursor/click indicators, overlays, transitions, and uncertainty.
- Every SDK layout/effect claim should cite supplied IDs in `anchor_signal_ids`
  and grouped `grounding_constraints`. If the model sees something between
  anchors, bind it to the nearest supplied span/word/beat/prosody/cut IDs and
  mark `needs_review` when timing cannot be verified.
- `craft_function_hypothesis` is allowed only as a constrained craft-purpose
  label such as `pattern_interrupt`, `caption_emphasis`, `interaction_focus`,
  or `unclear`. Pair it with `hypothesis_basis`; never let it become "this went
  viral because..." reasoning.
- SDK prompt context may include compact global prosody plus `prosody_seg_*` rows. Treat those as voice-delivery sync anchors only; Gemini SDK should not explain why the delivery worked or turn prosody into strategy.
- Treat signal-pack timecodes as Resolve-style `MM:SS:FF` frame timecode, not decimal seconds. At 60 FPS, `00:02:21` means 2 seconds + 21 frames, not 2.21 seconds. If Gemini emits decimal seconds, normalize or ignore them in favor of cited `edit_span_*`/`beat_*` IDs, frames, and media FPS.
- When testing prompt readiness, render/inspect the prompt locally first and confirm `{{analysis_context}}` and `{{video_filename}}` are gone before any Gemini upload.
- `gemini_video.py analyze --temporary` keeps the Gemini web-app run out of visible Gemini chat history.
- Keep `signals_for_gemini.md` compact. Very large signal contexts can fail or time out in the Gemini web-app path before model reasoning begins.
