# Signal-grounded Exemplar ingest before Gemini analysis

Gemini must not be the primary stopwatch for Exemplar analysis. Before a
semantic Gemini pass, the Source Video Analyst workflow should generate a
deterministic signal pack for the Exemplar: media metadata, word-level
transcript, audio/onset/loudness features, prosody summaries, visual cut/diff
events, keyframes, and a merged candidate beat grid.

The signal pack is the timing source of truth. Gemini receives it as prompt
context and labels what the moments mean for the Viral Pattern: hook logic,
curiosity loops, caption strategy, audio/emotion arc, payoff design, and
replication meaning. If Gemini sees something in the video that contradicts
the signal pack, it should mark `needs_review` rather than silently override
the deterministic metadata.

## Why

The existing raw Gemini prompt asks one model to segment, transcribe, estimate
timings, and interpret craft in one pass. That is useful for exploration, but
too unstable for downstream Beat Sheets and Recreation work. Assembly and
rendering need frame-indexed artifacts that can be audited and reused.

WhisperX/faster-whisper is a better source for word timings, librosa and
openSMILE are better sources for repeatable audio/prosody signals, and
PySceneDetect/OpenCV are better sources for cuts, frame-diff events, and
keyframes. Gemini is strongest when it interprets those signals semantically.

## Consequences

- `scripts/exemplar_ingest.py` is the reusable local entry point for generating
  Exemplar signal packs.
- Signal-grounded Gemini prompts should include `{{analysis_context}}` and be
  run with `gemini_video.py analyze --context <signals_for_gemini.md>`.
- Beat Sheet rows produced by Gemini should cite signal IDs.
- Raw Gemini-only analysis can still be useful for quick exploration, but it is
  not the canonical timing source for production.
- ASR and acoustic features can be wrong. The improvement is that errors
  become explicit signal artifacts that can be reviewed instead of hidden model
  guesses.
- openSMILE is acceptable for local/private analysis. Its license should be
  reviewed before this becomes commercial product code.
