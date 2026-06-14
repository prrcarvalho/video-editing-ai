# HANDOFF - Video Analysis + Recreation Pipeline on Hermes

## What this is

You are picking up the orchestration design for a video analysis + recreation pipeline running on the always-on Mac mini M4 (16GB).

**Use case in one line:** ingest a short viral social-media video, understand why it went viral at a granular level (per-shot visual + audio + caption + motion analysis), then recreate similar content end-to-end through specialized sub-agents driven by a high-reasoning main orchestrator.

This handoff covers ONLY the orchestration approach. Model providers, CLI choices, video tools, and file layout are explicitly out of scope here - those are decisions for the implementing agent at scaffold time.

---

## Orchestrator: Hermes alone

**Hermes Agent is the orchestrator. There is no second framework on the critical path.**

The pipeline lives entirely inside the Hermes Kanban board (`~/.hermes/kanban.db`). Every step is a task with one of seven states (triage → todo → ready → running → blocked → done → archived). The Hermes dispatcher auto-spawns workers when tasks reach `ready`, heartbeats keep stalled work from being abandoned, and the self-improving skill layer distills successful runs into reusable recipes after ~5 calls and re-evaluates every 15 tasks. We get this all for free.

Cross-agent communication is **always** a Kanban task transition with structured handoff metadata. Sub-agents never call each other directly - they read input from the task payload, do their one job, and write output through `kanban_complete`. The Kanban board IS the message bus.

---

## Sub-agent topology

Six specialized roles. Each is a Hermes worker with a single responsibility, a tight tool allow-list, and a hard "must not" boundary.

| Role | Owns | Hard "must not" |
|---|---|---|
| **eyes** | Per-shot visual analysis: composition, motion, hooks, on-screen text, retention hypothesis | Call other models; ingest more than the sampled frames per shot |
| **ears** | Audio analysis: transcript, music characteristics, SFX events, voice pace, hook-audio curve | Look at frames; call generative APIs |
| **hands** | Generate or re-stage shots from a storyboard | Call eyes/critic; exceed retry budget |
| **mouth** | Voice synthesis, lip-sync hints, music bed selection | Generate video; modify scripts |
| **critic** | Rubric-judge generated output against original insights + storyboard; emit pass / retry / abort with retry instructions | Generate; modify originals; exceed retry budget |
| **librarian** | Post-run: distill successful run patterns into Hermes skills, append durable lessons | Run during a live pipeline (post-completion only) |

The orchestrator role (deciding "why did this go viral" and "what should we recreate") is two synthesis tasks owned by the high-reasoning model directly, not a sub-agent.

---

## Canonical Kanban task chain

```
video.ingest
  → video.decompose                              (split shots, extract audio)
  → video.analyze.frames     (parallel per shot, sub-agent: eyes)
  → video.analyze.audio                          (sub-agent: ears)
  → video.synthesize.insights                    (orchestrator: why viral)
  → video.plan.recreation                        (orchestrator: storyboard)
  → video.generate.shots     (parallel per shot, sub-agent: hands)
  → video.generate.voice                         (sub-agent: mouth)
  → video.compose.final                          (assemble)
  → video.critic.check                           (sub-agent: critic)
       ↳ on retry: re-run generate.shots + compose.final, up to N attempts
       ↳ on pass: done
  → librarian distills the run                   (post-completion)
```

Only two tasks (`synthesize.insights` and `plan.recreation`) need the most expensive reasoning model. Everything else should route to cheaper, faster models. The Kanban board enforces this by carrying the model-tier hint in each task payload - the worker honors it.

---

## The secret sauce: vision critic with auto-retry

The critic is the single most important component. The community pattern that proves this design works end-to-end on consumer hardware (FLUX-and-Wan-Pipeline on a single GPU, 45 min E2E) hinges on a vision critic that compares the generated output against the original insights, scores it against a rubric, and either passes it or returns concrete retry instructions for `generate.shots` and `compose.final`.

**Build the critic and its rubric BEFORE any generator.** A working critic against known-good and known-bad fixtures is the gate to building hands/mouth. Without it, the pipeline cannot self-correct and will need a human reviewer for every run.

---

## Self-improving skill layer

Hermes auto-distills successful workflows into reusable recipes. Seed the layer with a small number of starter skills (one per viral-content archetype - comedy reel, ASMR vlog, explainer talking-head, etc.). Each skill is a YAML recipe that maps to a task chain plus a `heuristics:` block.

After ~5 successful runs of a given archetype, the librarian post-completion task updates the `heuristics:` block based on critic verdicts. Over time, the recipes get sharper without code changes.

---

## OpenClaw verdict

**For this project: drop. Hermes alone is sufficient.**

OpenClaw is running on the Mac mini for its own concerns (a separate agent identity, unrelated to this pipeline). It is not on the critical path here. Hermes already provides everything OpenClaw would contribute - heartbeats, hooks-via-handoffs, MCP, identity-via-skills, worker spawning, structured logging. Coupling this pipeline to OpenClaw adds complexity without adding capability.

**Revisit only if one of these triggers fires later:**

| Trigger | Narrowly integrate | Not before |
|---|---|---|
| Human approval gate needed between analysis and generation | OpenClaw's Lobster Workflow Engine for that one gate | A real approval requirement appears |
| Scheduled video crawls ("every 6h grab today's top reels") | macOS `launchd` (first choice) or OpenClaw cron | A real schedule appears |
| Chat-channel notifications when a run completes | One OpenClaw channel adapter | A real notification need appears |

Do not pre-build any of these.

---

## Anti-scope (do NOT build)

- ❌ Custom multi-agent framework on top of Hermes
- ❌ Coupling to OpenClaw on the critical path
- ❌ Web dashboard - Kanban is queryable directly
- ❌ Vector DB / RAG layer - per-run files + a lessons-learned doc suffice until memory exceeds ~50k tokens
- ❌ Agent-to-agent direct messaging - every handoff is a Kanban task
- ❌ Local frontier vision-language models - 16GB RAM cannot run a useful one; offload via subscription LLMs
- ❌ Abstract "model router" service - the model-tier hint in each Kanban task payload IS the router
- ❌ Premature parallelism beyond the two task types where it's obviously needed (per-shot analysis, per-shot generation)
- ❌ A memory-consolidation daemon - the librarian runs post-completion only

The corpus signal driving these vetoes: "framework choice barely matters; context engineering matters." Implementation effort goes to the critic rubric and the synthesis prompt, not to architecture flourishes.

---

## First step for the picking-up agent

Before any scaffold:

1. Read this handoff end to end.
2. Open Hermes' Kanban + skills docs and confirm everything described above is supported as-shipped (it is).
3. Decide on the stack (which reasoning model for synthesis, which provider for each sub-agent, which video tools). That is the next plan, not this one.
4. Start by writing the critic rubric. Treat it as the spec the rest of the pipeline must satisfy.

The raw research backing this design (community signals, model landscape, anti-patterns) is at `~/Documents/Last30Days/multi-agent-video-analysis-pipeline-and-ai-video-generation-stack-raw-v3.md`.
