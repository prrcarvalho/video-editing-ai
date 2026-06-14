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
- `gemini_pipeline/` — Gemini analysis scripts, prompts, and outputs.
- `assets/` — repo-local media assets.
- `scripts/` — utility scripts.
- `tools/` — local connector/tooling code.
- `hyperframes-reels/` — concrete reel projects; each may have its own instructions.

Do not reintroduce a `main/` subfolder. The project root is `/Users/pedrocarvalho/projects/video_editing_ai`.

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

For `hyperframes-reels/reel-1-pedro`, follow that folder's `AGENTS.md` and run checks from inside the reel folder.
