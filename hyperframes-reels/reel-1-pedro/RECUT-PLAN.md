# Recut reel-1-pedro to the viral formula — feasibility + plan

> Companion to `gemini_pipeline/outputs/reel-1-pedro/formula-gap-analysis_20260612.md`.
> This plan keeps all 3 screencast-production options open so each retry can try a different one.

## Context

The formula gap analysis produced a retimed ~24s edit grid: a 16-shot hard-cut montage
(8 real screencasts, 1 authority b-roll, 1 full-frame graphic card, 5 headshot anchors),
compressed keyword captions, a flat music bed, and a loopable ending. Question answered here:
can the HyperFrames stack in `hyperframes-reels/` execute this recut, and what's missing?

**Verdict: yes — HyperFrames can execute every mechanic in the grid. What's lacking is raw
footage assets (screencasts, authority b-roll, music) and ffmpeg pre-processing for VO
speed-up. No framework blockers.**

### User decisions locked in
- **VO**: speed up the existing `0601.mov` with ffmpeg, *approximate* timing — do **not** chase
  the exact 24.0s grid. Mild ~1.1–1.25x compression, prioritize natural sound over precision.
  Accept ~26–27s total if that keeps the voice clean.
- **Upgrades**: KEEP the SFX / reveal-chime / CLAUDE.md-asset upgrades per the decision table
  in the gap analysis; revert everything else to the formula.
- **Screencasts**: all 3 production options stay in this plan; pick one per attempt.

## Capability matrix (verified against hyperframes source + skills)

| Grid requirement | Supported? | Evidence |
| --- | --- | --- |
| Cut source mp4 into segments at exact timestamps, sequence hard cuts | ✅ | `data-media-start` trim offset + `data-start`/`data-duration` per clip; same-track clips sequence back-to-back (`.claude/skills/hyperframes/SKILL.md` §Data Attributes) |
| Interleave full-frame screencast mp4 clips | ✅ | Multiple videos on separate tracks; PiP/multi-video patterns (`.claude/skills/hyperframes/patterns.md`) |
| Simultaneous videos (terminal overlay over headshot at 0:00) | ✅ | Text-behind-subject pattern runs 2 videos at once (`patterns.md` lines 39–75) |
| Timed caption chunks, instant swaps | ✅ | Already implemented in `index.html` CAPS array — needs restyle/retiming only |
| Full-frame graphic card shot | ✅ | Timed `div` clip (existing `#spk-plan` restyled full-frame) |
| Music bed + SFX at timestamps + per-track volume | ✅ | `<audio class="clip">` with `data-start`/`data-volume` — 17 SFX already wired in `index.html` |
| Source-video audio survives render | ✅ | Separate `<audio src="0601.mov">` (muted video + audio element; ffmpeg mux in render path) |
| 1080×1920 render to mp4 | ✅ | Current project already renders this spec (`renders/*.mp4`) |
| **Per-segment speed-up at render** | ❌ | `data-playback-rate` lives only in the Studio editing layer (`packages/core/src/studio-api/helpers/sourceMutation.ts:422`); render-path `playbackRate` is global preview speed (`packages/core/src/runtime/init.ts:1592`). **Workaround: pre-process with ffmpeg** (`/opt/homebrew/bin/ffmpeg` present) |

> Note: the hyperframes "no jump cuts / always use transitions" rule is a house-style default
> for *designed* scenes. The recut's hard cuts are ordinary sequential video clips on a track,
> not a framework violation.

## What's lacking — exactly

1. **8 real Claude Code screencast clips** (~3–20s each, croppable to 1080×1920). Shot list → grid slots:
   - S1 — terminal, prompt being typed (slot ~01.3; also reused for the 0:00 top-left overlay)
   - S2 — task checklist executing / ticking (slot ~09.5)
   - S3 — different color-theme terminal (slot ~12.5)
   - S4 — fast compilation / output scroll (slot ~13.8)
   - S5 — live checklist updating (slot ~14.8)
   - S6 — scrolling config (slot ~16.0)
   - S7 — split chat UI (slot ~17.4)
   - S8 — real `CLAUDE.md` open in editor/terminal (slot ~20.1 — replaces the static mockup, keeps the asset-showcase upgrade)
2. **Authority b-roll** (~1.3s): real third-party footage of the Claude Code creator (podcast/interview)
   for slot ~03.2. Pedro must source it (third-party content — his usage call).
   Fallback: keep the existing Boris sticker pop (weaker, but needs no new asset).
3. **Music bed**: ~115 BPM flat minor-key lo-fi synth track, ≥30s, constant energy.
   **There is no music file in the project at all** (`assets/` holds only SFX) — the current
   render has zero music. Pedro picks a licensed/royalty-free track he owns.
4. **Speed-adjusted VO/video segments**: we produce these with ffmpeg from `0601.mov` (30.87s). No new asset.
5. **Terminal-recording tooling** — only if screencast Option B is chosen: `brew install vhs`
   (none of vhs/asciinema/agg currently installed).
6. **Open formula gap that stays open without a re-record**: the viral escalation engine is 4
   *spoken* stacked tips; the current narration has consequence + asset instead. ffmpeg can
   re-time speech but not add content, so the 4-screencast escalation run plays over the
   existing narration (visual-only escalation). Fully closing this needs a VO re-record
   (explicitly deferred by the user).

## Screencast production options (pick one per attempt)

- **Option A — record real sessions** (most authentic, zero install): Pedro records with macOS
  `Cmd-Shift-5` against the shot list above; we crop/trim with ffmpeg.
- **Option B — vhs-scripted terminals** (fully automated, deterministic): `brew install vhs`;
  one `.tape` per shot (typed commands, output scroll, per-slot themes) rendered straight to mp4.
  Repeatable across retries.
- **Option C — animated HTML terminal sub-compositions** (no assets at all): build terminal-chrome
  sub-comps in HyperFrames (registry has terminal blocks). Caveat: still "mockups" — the exact
  weakness the analysis flagged; use only as a fast draft pass.

## Implementation steps

1. **ffmpeg pre-process** → `reel-1-pedro/assets/cuts/`:
   - Cut `0601.mov` into the 5 headshot anchor segments (hook, pivot, mid re-engage, synthesis,
     CTA) + matching full-length audio segments at the same offsets.
   - Mild speed-up where a segment overshoots its slot:
     `-filter:v "setpts=PTS/R" -filter:a "atempo=R"`, R ≈ 1.1–1.25 (cap ~1.3 for natural sound).
   - Crop/trim screencast clips to 1080×1920 cover.
2. **Rewrite `index.html`** (keep scaffolding, CAPS-array approach, SFX wiring):
   - Track 0: sequenced video clips per the grid (headshot ↔ screencast ↔ b-roll) with
     `data-media-start` trims; separate `<audio>` clip per VO segment.
   - 0:00 frame: locked headshot (delete the 1.0s punch-in) + small live-terminal overlay top-left.
   - ~05.8 slot: full-frame "SECÇÃO 1: PLAN MODE" graphic card as its own ~2.2s clip (speaker
     off-screen, hard cut in/out, no slide); standalone caption swap "não em execute mode" ~1.3s into the hold.
   - Captions: rebuild CAPS as 1–3 word white lowercase fragments, center-screen (~y 880–1040),
     instant swaps, no color/caps/gradients/weight-shift; ~20 chunks; mid-hold swap on any clip held >1.5s.
   - Delete: crimson/white flashes, chroma spikes, ERRADA red treatment, yellow `<b>` brand
     coloring, camera-shake, gesture-dependent beats, `#ig` end-screen block + SEGUE pill,
     final spike fade. (Grade/grain ramp: optional keep if subtle.)
   - Ending: clean headshot framed like frame 1; two-beat CTA captions ("comenta criador" →
     "guia grátis"); no graphics; hard end.
   - Audio: music bed `<audio>` full-runtime at constant volume (no duck); keep SFX but re-time
     each to land within ~100ms of its cut; keep the reveal chime.
3. **Validate + render**: `npm run check` (lint/validate/inspect), then `npm run render`.

## Verification

1. `npm run check` passes; `npx hyperframes inspect` clean at hero frames (0.0, 0.7, reveal slot, CTA).
2. Render, then `ffprobe` duration + scrub exported frames at each grid timestamp to confirm the
   cut pattern (H→SR→BR→H→GFX→…).
3. First/last frame diff: confirm final framing matches 0:00 for the rewatch loop.
4. **Formula acceptance test**: run the new render through the gemini analysis pipeline
   (`gemini-video-analysis` skill → `PROMPT-GEMINI.md`) and diff the new beat sheet against the
   viral reference — the same verification that produced the gap analysis, now used as the gate.
