# AI Video Orchestration Handoff

## Purpose

Define the high-level orchestration model for a system that analyzes granular source videos, produces a structured report, delegates work to specialist agents, generates new video/audio/visual assets, reviews them, and assembles everything into one final video.

This document intentionally avoids choosing or referencing any specific framework, vendor, runtime, or stack.

## Core Principle

The system should not be one large autonomous agent. It should be a directed production pipeline with one accountable orchestrator and multiple specialist agents. The orchestrator owns planning, state, approvals, and routing. Specialist agents execute narrow tasks and return structured artifacts.

## Primary Agent

### Orchestrator Agent

Owns the whole project lifecycle.

Responsibilities:

- Interpret the user's goal and convert it into a production objective.
- Maintain the single source of truth for project state.
- Decide which specialist agents are needed for each job.
- Decompose the work into task cards with clear inputs, outputs, deadlines, and acceptance criteria.
- Route tasks to specialist agents.
- Enforce approval gates before expensive or irreversible steps.
- Track progress, failures, retries, and dependencies.
- Decide when to retry, revise, escalate, or stop.
- Ensure the final assembly follows the approved report and plan.

Important rule:

The Orchestrator Agent should not directly generate clips, write final prompts, edit assets, or assemble the final timeline. It directs the work and validates the handoffs.

## Specialist Agents

### Intake Agent

Clarifies the request before production starts.

Responsibilities:

- Capture target audience, objective, duration, aspect ratio, tone, style, constraints, and success criteria.
- Identify required source videos and supporting assets.
- Ask only blocking questions.
- Produce the initial project brief.

Output:

- `ProjectBrief`

### Source Video Analyst Agent

Analyzes the supplied videos at a granular level.

Responsibilities:

- Segment source videos into scenes, shots, beats, and notable moments.
- Extract transcript, speaker changes, visual events, motion, objects, locations, and audio cues.
- For fast-paced short-form Exemplars, deterministic ingest should let
  `--content-profile auto` enable AutoShot alongside PySceneDetect/OpenCV, or
  use `--content-profile short-form` when forcing the short-form path.
- For fast-paced short-form Exemplars, run a high-FPS visual evidence pass
  after deterministic ingest to capture layout, motion edits, overlays,
  transitions, VFX, scrolling, and cursor/click indicators.
- Identify high-value moments, weak moments, risks, and missing context.
- Preserve timestamps and source references.

Output:

- `SourceAnalysis`
- `VisualEvidencePack` when high-FPS visual mechanics are needed

### Report Synthesizer Agent

Turns raw analysis into a compact production report.

Responsibilities:

- Merge source observations into a structured narrative report.
- Treat `VisualEvidencePack` as evidence only. The Report Synthesizer, not
  Gemini, decides which visual mechanics matter for the Viral Pattern and
  Recreation plan.
- Identify themes, strongest moments, useful quotes, visual motifs, and editing opportunities.
- Mark unusable or risky sections.
- Produce a report that downstream agents can treat as the contract.

Output:

- `VideoReport`

### Creative Director Agent

Turns the report into a creative direction.

Responsibilities:

- Define the final video's story arc, pacing, tone, and visual treatment.
- Decide which moments should be source footage, generated clips, text, voiceover, graphics, or transitions.
- Produce a beat-by-beat creative plan.

Output:

- `CreativePlan`

### Shot Planner Agent

Converts the creative plan into production-ready shot requirements.

Responsibilities:

- Create a timeline outline.
- Define each shot or segment with duration, intent, source dependency, generated asset needs, and acceptance criteria.
- Flag dependencies between shots.

Output:

- `EditPlan`

### Prompt Writer Agent

Creates generation instructions for each required asset.

Responsibilities:

- Convert shot requirements into precise prompts.
- Include style, motion, camera, subject, framing, duration, and negative constraints.
- Generate variants when needed.
- Keep prompts traceable to the report and edit plan.

Output:

- `PromptPack`

### Video Generation Agent

Generates or requests generated video clips.

Responsibilities:

- Execute assigned video generation tasks.
- Return generated clips with metadata, prompt, source references, duration, and status.
- Report failures clearly.

Output:

- `GeneratedVideoAsset`

### Image and Graphic Asset Agent

Creates still images, cards, overlays, diagrams, thumbnails, or supporting visuals.

Responsibilities:

- Generate or prepare non-video visual assets.
- Preserve style consistency and source traceability.

Output:

- `GeneratedVisualAsset`

### Voice and Audio Agent

Creates or prepares narration, music, sound effects, and audio treatments.

Responsibilities:

- Produce scripts, voiceover assets, music beds, sound cues, and timing notes.
- Ensure audio assets match the edit plan.

Output:

- `GeneratedAudioAsset`

### Caption and Text Agent

Produces captions, titles, lower thirds, callouts, and on-screen copy.

Responsibilities:

- Convert transcript and creative plan into readable on-screen text.
- Respect timing, readability, tone, and visual hierarchy.

Output:

- `TextAssetPack`

### Consistency Agent

Maintains style and continuity across all generated outputs.

Responsibilities:

- Check character, brand, color, tone, pacing, and visual continuity.
- Detect drift between generated assets.
- Recommend prompt corrections or regeneration.

Output:

- `ConsistencyReview`

### Quality Review Agent

Validates each asset before assembly.

Responsibilities:

- Score assets against task acceptance criteria.
- Check duration, resolution, audio quality, visual quality, safety, brand fit, and relevance to the report.
- Approve, reject, or request retry with specific feedback.

Output:

- `AssetReview`

### Assembly Agent

Builds the final assembly plan from approved assets.

Responsibilities:

- Convert approved source clips, generated assets, captions, audio, and transitions into a deterministic assembly manifest.
- Ensure every timeline item has a source, duration, and intent.
- Avoid creative changes that were not approved.

Output:

- `AssemblyManifest`

### Render and Export Agent

Produces preview and final exports.

Responsibilities:

- Render a preview from the assembly manifest.
- Report technical failures and output metadata.
- Produce final export after approval.

Output:

- `PreviewExport`
- `FinalExport`

### Archive Agent

Packages the final result and provenance.

Responsibilities:

- Store the final video, report, edit plan, prompts, generated assets, reviews, and manifest.
- Ensure the project can be audited, resumed, or reused.

Output:

- `ProjectArchive`

## Workflow

### 1. Intake

The user provides the goal, source videos, and constraints. The Intake Agent produces `ProjectBrief`.

Exit criteria:

- Objective is clear.
- Target duration and format are known.
- Source videos are available.
- Blocking questions are resolved.

### 2. Source Ingestion

The Orchestrator creates a project workspace and indexes all source videos and assets.

Exit criteria:

- Every source has a stable identifier.
- Metadata and access paths are recorded.
- The project has a single source of truth.

### 3. Granular Analysis

The Source Video Analyst Agent analyzes videos into structured observations.

Exit criteria:

- Important moments are timestamped.
- Transcript or spoken content is captured when present.
- Visual and audio cues are mapped.
- Risks and unusable sections are marked.

### 4. Report Synthesis

The Report Synthesizer Agent creates the canonical `VideoReport`.

Exit criteria:

- Downstream agents can understand the source material without rewatching everything.
- Best moments and source references are explicit.
- The report is approved or accepted by the Orchestrator.

### 5. Creative Planning

The Creative Director Agent creates the high-level story, structure, and treatment.

Exit criteria:

- The creative arc is clear.
- The role of source footage vs generated footage is clear.
- The Orchestrator can request user approval before production starts.

### 6. Edit Planning

The Shot Planner Agent creates an `EditPlan` with segment-level requirements.

Exit criteria:

- Every timeline segment has an intent, duration, and asset requirement.
- Generated clips and source clips are clearly distinguished.
- Dependencies are listed.

### 7. Approval Gate: Plan

The user or supervising reviewer approves the report and edit plan before expensive generation starts.

Allowed outcomes:

- Approve.
- Request edits.
- Remove or add segments.
- Change direction.
- Cancel.

### 8. Task Decomposition

The Orchestrator creates task cards for specialist agents.

Each task card must include:

- Task ID.
- Assigned agent.
- Input artifacts.
- Required output artifact.
- Acceptance criteria.
- Maximum attempts.
- Dependencies.

### 9. Parallel Asset Production

Prompt, video, image, audio, caption, and graphic agents work in parallel where dependencies allow.

Exit criteria:

- Every required asset has either an approved output or a documented failure.
- Failed assets have specific retry feedback.

### 10. Review and Retry Loop

The Consistency Agent and Quality Review Agent inspect outputs.

Retry policy:

- Retry only with specific feedback.
- Do not retry indefinitely.
- Escalate repeated failures to the Orchestrator.
- Request human review when failure affects creative direction or budget.

Exit criteria:

- Approved assets are marked ready for assembly.
- Rejected assets are excluded or regenerated.

### 11. Assembly Manifest

The Assembly Agent converts the approved plan and assets into `AssemblyManifest`.

Exit criteria:

- Every timeline item references an approved source or generated asset.
- Timing, captions, transitions, and audio instructions are complete.
- No unapproved assets are included.

### 12. Preview Export

The Render and Export Agent creates a preview.

Exit criteria:

- Preview is technically valid.
- Timeline matches the approved assembly manifest.
- Issues are reported as structured review notes.

### 13. Approval Gate: Preview

The user or supervising reviewer approves the preview.

Allowed outcomes:

- Approve final export.
- Request edit changes.
- Request asset regeneration.
- Request timing/audio/caption fixes.

### 14. Final Export

The Render and Export Agent creates the final video.

Exit criteria:

- Final video meets the requested technical format.
- Final output is traceable to the approved manifest.

### 15. Archive

The Archive Agent stores all final artifacts and provenance.

Exit criteria:

- Final video is stored.
- Report, plan, prompts, assets, reviews, and manifest are stored.
- Project can be audited or resumed later.

## Required Artifacts

The workflow should produce these artifacts in order:

1. `ProjectBrief`
2. `SourceAnalysis`
3. `VideoReport`
4. `CreativePlan`
5. `EditPlan`
6. `PromptPack`
7. `GeneratedAssets`
8. `AssetReviews`
9. `AssemblyManifest`
10. `PreviewExport`
11. `FinalExport`
12. `ProjectArchive`

## Coordination Rules

- One project workspace is the single source of truth.
- The Orchestrator owns task routing and state.
- Specialist agents only work on assigned task cards.
- All outputs must be structured and persisted.
- Every generated asset must include its prompt, source references, and metadata.
- Expensive generation requires prior approval.
- Final assembly may only use approved assets.
- Rendering/export should not make creative decisions.
- Retry loops must be bounded.
- Human approval is required when direction, budget, rights, or brand risk changes.

## Suggested Skills For A Future Agent

- `handoff` — use when transferring this plan to another session.
- `video-report` — use if concrete source videos are supplied and need analysis.
- `grill-me` — use if the orchestration assumptions need to be stress-tested before implementation.

## Non-Goals For The Next Agent

- Do not choose implementation frameworks yet.
- Do not pick vendors or model providers yet.
- Do not implement the system yet.
- Do not design UI details yet.
- Do not skip the report-first workflow.

## Next Recommended Step

Turn this into a concrete product spec with schemas for each artifact, especially `VideoReport`, `EditPlan`, `TaskCard`, `GeneratedAsset`, `AssetReview`, and `AssemblyManifest`.
