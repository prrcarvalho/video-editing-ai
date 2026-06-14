# AI Video Recreation

A system that ingests a viral piece of social media content, learns *why it worked* as a reusable pattern, and applies that pattern to produce a new, polished piece of content — optionally about a different subject. The defining idea is **learn-a-pattern-then-apply**, not re-cut-the-source.

## Language

**Exemplar**:
A viral video supplied by the user — most often a TikTok / YouTube / Instagram link, sometimes an uploaded file — to be learned from. Normally the user's *own* content. Its primary value is the Pattern it teaches; optionally, on request, pieces of its footage may be re-cut into the output.
_Avoid_: source video, raw footage (these frame the supplied video as footage-to-cut-down, when its main value is the Pattern)

**Exemplar Asset**:
A concrete piece extracted from an Exemplar — a scene, frame, SFX, or sound — that may optionally be reused in the Recreation. The decision to reuse one is made either by the planner (when it fits) or by an explicit user request.

**Viral Pattern**:
The reusable, *mostly* subject-independent specification of HOW an Exemplar wins and holds attention, structured as a bundle of **facets**. The form/craft facets are the durable spine that transfers to any subject; a thinner content-angle layer records subject-bound choices that are re-chosen per Recreation. Every facet is grounded in a psychology mechanism (the WHY) and carries a transferability tag.
_Avoid_: template, formula, blueprint, recipe

**Pattern Library**:
The growing, documented store of Viral Patterns. Reusable across projects on demand, and auto-matchable — the agent can pick the best-fit Pattern for a new idea or newly supplied Exemplar.

**Asset Knowledge Base**:
A documented index of raw material the system can draw from to fill a video, fed by two channels: (1) the user's **owned** content — most importantly long-form pieces (YouTube tutorials/demos) ingested and **segmented by Gemini analysis** into reusable clips; and (2) **internet-discoverable stock**, reached through stock connectors so an agent can outsource media on demand. Modeled on the "LLM-wiki" pattern so agents quickly know what is available for a task.
_Avoid_: media library, asset store (too generic; this one is *documented for agents*)

**Asset Segment**:
A reusable sub-clip carved out of an owned long-form piece by Gemini analysis (a demo step, a b-roll-able moment, an SFX/sound), indexed in the Asset Knowledge Base for reuse in later Recreations. The mechanism by which long-form production feeds short-form supply.

**Stock Connector**:
An MCP-mediated bridge to a third-party stock library (e.g. Pexels, Coverr, Freesound) that lets an agent search and pull licensed media to fill a beat the owned channel can't. The stock channel of the Asset Knowledge Base.

**Freesound Connector**:
The first concrete Stock Connector for SFX/audio accents. Agents search Freesound through the shared MCP server documented in [docs/mcp/freesound.md](./docs/mcp/freesound.md), then download selected original assets through `scripts/freesound_download.py` so OAuth tokens stay outside the repo and attribution/license metadata is recorded in `assets/sfx/freesound/manifest.json`.

**Beat Sheet**:
The per-shot timed grid an edit is built from — each row a shot with its timestamp, source-type (headshot / screencast / b-roll / graphic card), caption fragment, and audio cue. Doubles as the keying structure for asset sourcing: an agent fills each beat from an **Asset Segment** or a **Stock Connector**.
_Avoid_: edit grid, shot list (use Beat Sheet for the canonical artifact)

**Recreation**:
The finished new video the system produces. Follows a Viral Pattern but may cover a similar *or different* subject than the Exemplar.
_Avoid_: edit, cut, render (those name steps, not the deliverable)

**Entry Mode** — how a project starts. Two kinds:
- **Exemplar-led**: the user supplies an Exemplar to learn a Pattern from.
- **Idea-led**: the user supplies only an idea/brief and no video; the system applies a Pattern already in the Library.

## Viral Pattern facets

A Pattern is a bundle of **facets**, each belonging to one **category**:
- **form_craft** — how the video is built; transfers across subjects (the durable spine).
- **content_angle** — what it's about + funnel position; abstract moves transfer, concrete bindings rebind per subject.
- **psychology_substrate** — the cognitive/neuro mechanism explaining *why* a craft choice works; linked from the tactics it powers, not stored as a producible step.
- **platform_distribution** — algorithm signals, format/length, audio discovery, the pre-publish QA gate, iteration thresholds; treat specific weights as directional, plan on the mechanism.

**Transferability** — a tag on every tactic: `form_transfers_any_subject` | `mixed` | `content_specific`. Tells the system which parts survive a subject swap.

**Bridge variable** — a content-chosen knob that drives form decisions: *target emotion, payoff/send-moment, genre archetype, funnel position*. Bridge variables are the link by which `content_angle` parameterizes `form_craft` via the substrate.

**Playback environment** — the assumed target device: a tinny phone speaker, frequently muted, one-handed. The single constraint motivating timbre, loudness, noise-floor, burn-in captions, and the mute/phone-speaker checks.

The eight facets a stored Pattern records (the ninth, the substrate, is the linked WHY layer):
1. **Hook & Entry** (form) — first ~0–8s (+ pre-click title/thumbnail) that win the thumb-stop and open the first curiosity gap.
2. **Narrative & Loop Structure** (form) — design-backward-from-the-payoff; one macro open-loop + micro-loops; stair-step escalation; loop-count picks the format.
3. **Pacing & Visual Editing** (form) — pattern-interrupt cadence, shot length, motion-in-every-frame, value-per-second, claims-to-visuals.
4. **Captions & On-Screen Text** (form) — mute-first keyword captions, kinetic state machine, top-third placement.
5. **Audio, Color & Multimodal Orchestration** (form) — score-first 8-track beat-sheet; coincident cues in the ~100ms binding window; frisson reveal stack; voice as load-bearing channel.
6. **Platform & Distribution Signals** (platform) — per-platform goal metric → ending/CTA; CTR+retention must rise together; QA gate; numeric iteration ladder.
7. **Emotional & Arousal Design** (content) — pick ONE high-arousal target emotion; engineer the arousal arc; tempo→arousal (non-monotonic), mode→valence.
8. **Content Angle & Subject Strategy** (content) — abstract angle moves transfer; genre/shot-mix/funnel-position rebind per subject.

> The full grounded model (every tactic, mechanism, citation, conflict, and gap) lives in [docs/viral-pattern-taxonomy.md](./docs/viral-pattern-taxonomy.md).

## Flagged ambiguities

- **"Source video" (handoff doc) vs "Exemplar" (here)** — The handoff doc's *Source Video Analyst / Report Synthesizer / Assembly* chain assumes the supplied video's clips are cut down and reused as the *backbone* of the output. That assumption is rejected. The supplied video is an **Exemplar**: studied primarily for its **Viral Pattern**. Re-cutting some of its footage into the **Recreation** is allowed, but only as an *optional, per-request* content source — never the default.

## Example dialogue

**Dev:** When the user pastes a TikTok, do we cut clips out of it for the final video?
**Creator:** Usually no — its main job is to teach the Pattern. But I might *optionally* ask to re-cut a few pieces of it in too.
**Dev:** So the final video — the Recreation — might be a totally different topic?
**Creator:** Right. Same hook structure and pacing, different subject. The footage to fill it comes from my own channels, stock we find, generated clips — or, optionally, bits of the Exemplar itself.
**Dev:** And next time you don't even need an Exemplar?
**Creator:** Exactly — Idea-led. I give an idea, the agent grabs the best-fit Pattern from the Library and applies it.
