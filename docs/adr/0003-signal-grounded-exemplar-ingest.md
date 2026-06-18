# Signal-grounded Exemplar ingest and role-separated Gemini analysis

Gemini must not be the primary stopwatch for Exemplar analysis. Before a
semantic Gemini pass, the Source Video Analyst workflow should generate a
deterministic signal pack for the Exemplar: media metadata, word-level
transcript, audio/onset/loudness features, prosody summaries, visual cut/diff
events, speech-rate metrics, segment-aligned prosody features, learned shot-boundary events for short-form
Exemplars, keyframes, shot-boundary signals, and a merged candidate beat grid.

The signal pack is the timing source of truth. The Gemini web-app path can
still be used for quick semantic exploration, but the production path separates
roles: the official Gemini SDK performs high-FPS visual evidence extraction for
fast-paced content, and Codex/GPT performs the final high-reasoning Viral
Pattern and Recreation synthesis. If Gemini sees something in the video that
contradicts the signal pack, it should mark `needs_review` rather than silently
override the deterministic metadata.

## Why

The existing raw Gemini prompt asks one model to segment, transcribe, estimate
timings, and interpret craft in one pass. That is useful for exploration, but
too unstable for downstream Beat Sheets and Recreation work. Assembly and
rendering need frame-indexed artifacts that can be audited and reused.

WhisperX/faster-whisper is a better source for word timings and speech-rate
WPM. Librosa is a better source for mixed-audio rhythmic BPM and
onset/loudness signals, openSMILE is a better source for repeatable global and
transcript-segment prosody summaries, and PySceneDetect/OpenCV are better sources for baseline cuts,
frame-diff events, keyframes, and shot spans. For fast short-form Exemplar
videos, a learned short-video detector such as AutoShot should add candidate
shot-boundary evidence beside PySceneDetect by default. Within-shot creator
effects such as punch-ins, zoom animations, crop shifts, split-screen layout,
overlays, and VFX should not be inferred by the current deterministic signal
pack. Gemini is strongest as a visual microscope when it is anchored to known
shot spans and asked to describe what is visibly present. Codex/GPT is
responsible for deciding why the evidence matters, which craft moves transfer,
and how the Recreation should be planned.

## Consequences

- `scripts/exemplar_ingest.py` is the reusable local entry point for generating
  Exemplar signal packs.
- Signal-grounded Gemini prompts should include `{{analysis_context}}` and be
  run with `gemini_video.py analyze --context <signals_for_gemini.md>`.
- For production fast-form visual craft analysis, use `gemini_sdk_video.py` to
  create `analysis.md`, `prompt.md`, `input_signals_for_gemini.md`,
  `run_manifest.json`, strict response schema files,
  `visual_craft_events.json`, `visual_layout_timeline.json`,
  `visual_micro_passes.json`, `sdk_usage.json`, and
  `codex_reasoning_context.md` under
  `exemplars/<slug>/gemini_runs/sdk/<run_id>/`.
- The SDK `extract` command is micro-first by default: it analyzes deterministic
  shot spans directly rather than always running a whole-video survey first.
  The survey pass is optional via `--include-survey`.
- SDK micro passes use 12 FPS by default, with adaptive 24 FPS for short spans,
  candidate/review boundaries, low-confidence boundaries, or low-confidence
  model results that need a retry.
- Gemini SDK prompts must not explain virality, create a Viral Pattern, write a
  Beat Sheet, or produce a Recreation spec. They only describe visible layout,
  motion, effects, interaction indicators, overlays, transitions, and
  uncertainty.
- Gemini SDK direct responses should stay structured as JSON with
  `response_json_schema`; the local tool renders `analysis.md` from those JSON
  artifacts for Resolve-side human inspection.
- The SDK visual evidence taxonomy should explicitly cover cut/transition
  rhythm, framing/keyframed motion, camera motion, speed/time effects,
  captions/text states, overlays/graphics, screen/UI interactions,
  VFX/compositing, color/light changes, and audio-visible sync. A constrained
  `craft_function_hypothesis` is acceptable as an evidence label, but not as
  final virality reasoning.
- The SDK visual evidence taxonomy is not an independent source of evidence.
  It is a controlled label vocabulary grounded in the deterministic ingest:
  WhisperX `word_*` timings, WPM/speech metrics, `prosody_seg_*` delivery rows,
  candidate `beat_*` rows, audio/onset/sync rows, and `edit_span_*` /
  `edit_boundary_*` shot evidence.
- SDK layout/effect claims should cite supplied IDs in `anchor_signal_ids` and
  grouped `grounding_constraints`. If a visible mechanic lands between anchors,
  bind it to the nearest supplied span/word/beat/prosody/cut IDs and set
  `needs_review` when timing cannot be verified.
- SDK prompt context may include compact global prosody and `prosody_seg_*`
  rows. Treat them as voice-delivery synchronization anchors only; they do not
  authorize Gemini SDK to explain why the delivery worked.
- Codex/GPT is the only stage that should synthesize the deterministic signal
  pack and Gemini SDK evidence into a Viral Pattern, Beat Sheet, Recreation
  instructions, and specialist-agent task cards.
- Beat Sheet rows produced by the Codex/GPT reasoning stage should cite signal
  IDs and Gemini visual evidence IDs.
- Shot-boundary claims should cite `edit_boundary_*`, `edit_span_*`, or
  `sync_*` IDs from `edit_mechanisms.json`.
- Signal-pack timecodes are Resolve-style frame timecodes: `MM:SS:FF` or
  `HH:MM:SS:FF`, where the final field is frames at the media FPS. Gemini must
  not reinterpret `00:02:21` as 2.21 seconds on a 60 FPS timeline; downstream
  seconds should be derived from cited signal IDs, frame numbers, and FPS.
- WPM and BPM must stay separate: WPM is narrator/speaker speech pace derived
  from WhisperX words; BPM is the dominant rhythmic pulse of the mixed audio
  estimated by librosa, often music/bed/SFX/edit rhythm when present.
- Raw Gemini-only analysis can still be useful for quick exploration, but it is
  not the canonical timing source for production.
- Learned shot-boundary scores are not all equal. High-confidence AutoShot
  events can be treated like visual cuts, while low-threshold AutoShot events
  are review candidates that may still be useful for keyframes and Beat Sheet
  anchoring.
- For short-form Exemplar ingest, AutoShot should be on by default alongside
  PySceneDetect/OpenCV. The ingest CLI uses `--content-profile auto` to enable
  AutoShot for vertical social-length videos, `--content-profile short-form` to
  force it on, and `--content-profile long-form` or `--no-autoshot` to keep it
  off.
- The edit-mechanism artifact is boundary-only and does not perform OCR. It can
  say when a shot likely cuts or where a detector candidate needs review. It
  must not be treated as proof that a frame zoomed, shifted, panned, or used a
  split-screen/VFX layout.
- ASR and acoustic features can be wrong. The improvement is that errors
  become explicit signal artifacts that can be reviewed instead of hidden model
  guesses.
- openSMILE is acceptable for local/private analysis. Its license should be
  reviewed before this becomes commercial product code.
