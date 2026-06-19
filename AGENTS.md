# AGENTS.md

Always answer in English.

## Start Here

This repo is an AI video recreation workspace. A new agent should orient in this order:

1. Read `CONTEXT.md` for the project glossary and domain language.
2. Read `docs/ai_video_orchestration_handoff.md` for the production pipeline.
3. Read `docs/adr/` before changing workflow, sourcing, acceptance, or renderer decisions.
4. Read `docs/viral-pattern-taxonomy.md` when working on pattern analysis or transfer.
5. Read the local `AGENTS.md` inside a concrete reel folder before editing that reel.

## Project Language

Use the glossary terms from `CONTEXT.md`. In particular:

- Use `Exemplar` for the viral video being learned from.
- Use `Viral Pattern` for the reusable structure learned from an Exemplar.
- Use `Beat Sheet` for the per-shot timed grid.
- Use `Asset Knowledge Base`, `Asset Segment`, and `Stock Connector` for sourcing language.
- Use `Recreation` for the finished new video.

Do not reframe the Exemplar as default footage to cut down. Reusing Exemplar footage is optional and request-specific.

## Repository Layout

- `CONTEXT.md` — glossary only; no implementation details or planning notes.
- `docs/ai_video_orchestration_handoff.md` — canonical orchestration pipeline.
- `docs/hermes_orchestration_handoff.md` — earlier Hermes-oriented pipeline notes.
- `docs/adr/` — durable architecture decisions.
- `docs/mcp/freesound.md` — Freesound Stock Connector setup and workflow.
- `gemini_pipeline/` — Gemini analysis scripts and prompts. Keep new analysis outputs under the relevant Exemplar or Recreation folder unless a legacy script still requires this path.
- `assets/` — shared Asset Knowledge Base material only: SFX, stock, owned Asset Segments, and generated reusable assets. Do not place Exemplar source videos or final polished Recreation exports here.
- `exemplars/` — target home for Exemplar intake, deterministic signal packs, Gemini runs, Markdown comparisons, and human synthesis.
- `patterns/` — target home for promoted reusable Viral Patterns.
- `recreations/` — target home for concrete Recreation projects from brief through final export.
- `scripts/` — utility scripts.
- `tools/` — local connector/tooling code.
- `hyperframes-reels/` — existing HyperFrames reel projects; each may have its own instructions. Prefer `recreations/<recreation_slug>/build/hyperframes/` for new projects or when migrating.

Do not reintroduce a `main/` subfolder. The project root is `/Users/pedrocarvalho/projects/video_editing_ai`.

## Artifact Governance

Use this lifecycle for new work and for gradual cleanup of legacy outputs:

```text
Exemplar source
-> deterministic signal pack
-> Gemini web-app and SDK runs
-> Markdown comparison
-> human synthesis
-> promoted Viral Pattern, when reusable
-> Recreation project
-> acceptance review
-> final polished export
```

### Target Folder Shape

```text
exemplars/<exemplar_slug>/
  source/
  signals/
  gemini_runs/
    web_app/<run_id>/
    sdk/<run_id>/
  comparisons/
    markdown/
  synthesis/

patterns/<pattern_slug>/
  pattern.md
  evidence_index.md
  source_exemplars.md

recreations/<recreation_slug>/
  brief/
  beat_sheet/
  assets/
  build/
  renders/
  acceptance/
  exports/
    final/
  archive/
```

### Naming Rules

- Use stable lowercase slugs: `instagram-real`, `reel-1-pedro`, `claude-code-system-shortform`.
- Use UTC-like run IDs: `YYYYMMDDTHHMMSSZ`.
- Use explicit versions for deliverables: `v001`, `v002`, `v003`.
- Prefer role names over ad hoc names: `analysis.md`, `prompt.md`, `run_manifest.json`, `comparison_notes.md`, `beat_sheet.md`.
- Name final exports as `<recreation_slug>_final_<version>_<run_id>.mp4`.

### Exemplar Rules

- Put incoming Exemplar media in `exemplars/<exemplar_slug>/source/`.
- Do not put Exemplar source videos in `assets/`; the Exemplar teaches a Viral Pattern and is not automatically reusable media.
- Store deterministic ingest output in `exemplars/<exemplar_slug>/signals/`.
- Treat `signals_for_gemini.md` as a generated Gemini input bundle only. Do not hand-edit it, and do not treat it as the source of truth.
- Keep canonical timing and evidence in JSON artifacts such as `media.json`, `transcript.words.json`, `audio_features.json`, `visual_events.json`, `speech_metrics.json`, `edit_mechanisms.json`, and `candidate_beats.json`.
- Treat `signals/_work/` as disposable cache unless exact reproduction requires preserving it.

### Gemini Run Rules

- Store Gemini web-app outputs under `exemplars/<exemplar_slug>/gemini_runs/web_app/<run_id>/`.
- Store Gemini SDK outputs under `exemplars/<exemplar_slug>/gemini_runs/sdk/<run_id>/`.
- Keep SDK outputs out of `signals/`; `signals/` is for deterministic inputs and evidence, not model outputs.
- For both web-app and SDK runs, use `analysis.md` as the main human-readable output.
- Preserve `prompt.md`, `input_signals_for_gemini.md`, and `run_manifest.json` with every run when practical.
- When comparing human-readable outputs, copy the exact pair into `exemplars/<exemplar_slug>/comparisons/markdown/<comparison_id>/` as `web_app.analysis.md` and `sdk.analysis.md`.

### Recreation Rules

- Start concrete Recreation work under `recreations/<recreation_slug>/`.
- Put renderer/framework-specific project files under `recreations/<recreation_slug>/build/<renderer>/`, for example `build/hyperframes/`.
- Put draft renders in `recreations/<recreation_slug>/renders/`.
- Put acceptance artifacts, Gemini re-analysis, and gap analysis in `recreations/<recreation_slug>/acceptance/`.
- Put polished deliverables only in `recreations/<recreation_slug>/exports/final/`.
- Do not put final polished videos in root `assets/`.

### Promotion Rules

- Promote only reusable, reviewed Viral Patterns into `patterns/<pattern_slug>/`.
- Keep Exemplar-specific observations in `exemplars/<exemplar_slug>/synthesis/` unless they have been abstracted into a reusable Viral Pattern.
- Keep stock, SFX, owned Asset Segments, and generated reusable assets in `assets/` with manifests when licensing or provenance matters.

## Documentation Rules

When using `grill-with-docs`, follow `/Users/pedrocarvalho/.agents/skills/grill-with-docs/SKILL.md`.

- If a domain term is resolved, update `CONTEXT.md` immediately.
- Keep `CONTEXT.md` as a glossary, not a spec or scratchpad.
- Create or update ADRs only for decisions that are hard to reverse, surprising without context, and based on a real tradeoff.
- Prefer updating the relevant existing doc over creating a new doc.

## Working Rules

- State assumptions before making non-trivial changes.
- Keep changes surgical and tied to the request.
- Do not refactor adjacent files unless the task requires it.
- Verify with the narrowest relevant check available.
- There is no single root test command yet; use the touched subproject's commands.

## Useful Commands

Freesound setup:

```sh
./tools/freesound/setup_mcp.sh
./scripts/freesound_download.py login
```

