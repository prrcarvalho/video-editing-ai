# AGENTS.md

## Exemplar Ingest Notes

- `exemplar_ingest.py` keeps PySceneDetect as the baseline hard-cut detector. With the default `--content-profile auto`, AutoShot is enabled for vertical social-length videos and merged as an additional learned short-video signal, not a replacement. Use `--content-profile short-form` to force it on, `--content-profile long-form` or `--no-autoshot` to keep it off.
- Keep WPM and BPM separate in signal outputs: WPM is speech pace from WhisperX words; BPM is mixed-audio rhythmic pulse from librosa, often music/bed/SFX/edit rhythm.
- Keep global and time-aligned prosody separate. `prosody_features.json` is a whole-video openSMILE summary; `prosody_segments.json` aligns openSMILE functionals and WPM to transcript segments so agents can inspect where delivery is faster, louder, higher-pitched, or more varied.
- Use `scenedetect>=0.7,<0.8` without the old `scenedetect[opencv]` extra; prefer `FrameTimecode.seconds`/`frame_rate` over deprecated `get_seconds()`/`framerate`.
- On Apple Silicon, run AutoShot through `--autoshot-device auto`; the script sets `PYTORCH_ENABLE_MPS_FALLBACK=1` before Torch imports so unsupported MPS ops can fall back to CPU.
- AutoShot's confident threshold can miss subtle UI-state transitions. Low-threshold `autoshot_candidate_*` events are review candidates, useful for keyframes/Beat Sheet anchors but not canonical cuts.
- Keyframes should sample just after visual boundaries. Sampling exactly at the boundary can save the previous shot frame, especially around fast UI cuts.
- WhisperX/pyannote may warn about `torchcodec`; this ingest path extracts WAV with ffmpeg first, so that warning is usually non-blocking.
