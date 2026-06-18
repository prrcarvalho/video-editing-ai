---
video: instagram-real.MP4
model: gemini-3-flash
prompt_template: prompts/PROMPT-GEMINI-SIGNAL-GROUNDED.md
generated_at: 20260615T001758Z
analysis_context: /Users/pedrocarvalho/projects/video_editing_ai/gemini_pipeline/outputs/instagram-real/signals/signals_for_gemini.md
---

Here is the retention engineering analysis and replication specification for the provided short-form video.

---

## A. Signal Integrity

The signal pack is highly coherent and accurately matches the multi-modal profile of the media file. 
* **Transcript Verification:** Spoken terms match perfectly with the text timelines.
* **Shot Boundaries:** The video contains rapid visual state changes. `vis_scene_####` cuts line up precisely with logical clause endings and hard screen changes.
* **Review Items:** No conflicts were detected between the physical media stream and the provided signal pack. 

---

## B. Hook And Curiosity Logic

* **Hook Text:** *"Most people use Claude code the wrong way."* (`seg_0001`)
* **Hook Boundary:** Ends at `00:01.83` (`beat_0005`, `autoshot_cut_0001`). This marks the transition from the speaker setting up the problem on screen to a hard cut showing code execution.
* **Hook Type:** **Negative Frame / Cognitive Error.** It asserts that the vast majority of users are performing a common task incorrectly, threatening the viewer's sense of competence.
* **Viewer Curiosity Question:** *"Am I using it wrong, and what is the secret correct way to do it?"* ---

## C. Signal-Grounded Beat Sheet

| beat | time | cited_signal_ids | visual purpose | caption/text state | audio/voice cue | loop opened/closed | interrupt type | replication meaning |
|---|---:|---|---|---|---|---|---|---|
| 01 | 00:00.00 | `beat_0001`, `seg_0001` | Talking head framing with dynamic UI overlay behind. | "use claude code" | Spoken: "Most people use..." with high energy onset. | Opens Macro Loop (The Wrong Way vs. The System). | None (Entry Point) | Establish immediate topic context within 0.5s. |
| 02 | 00:01.83 | `beat_0005`, `autoshot_cut_0001` | Cut to screen recording of IDE/Terminal workspace. | "the wrong way" | Spoken: "They open it..." | Opens Micro Loop 1 (How amateurs fail). | Hard Cut to B-Roll Workspace | Inject visual variety at the first logical narrative pause. |
| 03 | 00:03.13 | `beat_0009`, `autoshot_cut_0002` | UI transition showing prompt input box. | "type what" | Spoken: "...hope for the best." | Sustains Micro Loop 1. | Micro-zoom / UI Change | Keep the eye moving during a long single-sentence thought. |
| 04 | 00:03.95 | `beat_0010`, `autoshot_cut_0003` | Hard cut to high-profile industry guest podcast clip. | "But the guy who" | Spoken voice switch: "But the guy..." | Closes Micro Loop 1; Opens Micro Loop 2 (The Authority Source). | External Video Insertion (Social Proof) | Pivot the argument using external authority to break monologue fatigue. |
| 05 | 00:05.53 | `beat_0014`, `autoshot_cut_0004` | Cut back to code environment showing workflow configurations. | "Claude code" | Spoken: "...does the opposite." | Sustains Micro Loop 2. | Hard Cut back to Tech Workspace | Link authority's claim directly back to actionable workspace proof. |
| 06 | 00:06.23 | `beat_0016`, `autoshot_cut_0005` | Hard cut back to talking head profile framing. | "opposite. He says" | Spoken: "He says most of..." | Opens Micro Loop 3 (Plan Mode vs. Build Mode). | Hard Cut to Creator A-Roll | Re-establish creator authority as the narrator of the breakdown. |
| 07 | 00:07.40 | `beat_0019`, `autoshot_cut_0006` | Cut away to thoughtful stock footage overlay. | "Plan Mode" | Spoken: "...start in plan mode..." | Sustains Micro Loop 3. | Contextual B-Roll Swap | Slow down visual rhythm to emphasize a conceptual distinction. |
| 08 | 00:08.40 | `beat_0022`, `autoshot_cut_0007` | Cut to terminal execution screen showing step checks. | "Slows down" | Spoken: "...not build mode." | Sustains Micro Loop 3. | Hard Cut to Tech Workspace | Match the phrase "build mode" with concrete technical UI. |
| 09 | 00:09.18 | `beat_0024`, `autoshot_cut_0008` | Zoom out / panel shift on terminal workspace. | "Gets the plan" | Spoken: "Slows down first..." | Sustains Micro Loop 3. | Micro-zoom / UI Change | Maintain high engagement during technical explanation. |
| 10 | 00:10.90 | `beat_0028`, `autoshot_cut_0009` | Panel transition highlighting build outcomes. | "execute" | Spoken: "...then lets Claude execute." | Closes Micro Loop 3. | Hard Cut / Viewport Shift | Complete the core workflow payoff loop visually. |
| 11 | 00:11.97 | `beat_0031`, `autoshot_cut_0010` | Hard cut back to talking head profile framing. | "That one shift" | Spoken: "That one shift alone..." | Opens Micro Loop 4 (The Messy Results Trap). | Hard Cut to Creator A-Roll | Use a direct face-to-camera shot to signal a high-value summary statement. |
| 12 | 00:13.23 | `beat_0035`, `autoshot_cut_0011` | Cut to IDE file trees displaying cleanly organized configurations. | "why most people" | Spoken: "...explains why most people..." | Sustains Micro Loop 4. | Hard Cut to Tech Workspace | Visually contrast the spoken word "messy" with clean code configurations. |
| 13 | 00:14.50 | `beat_0036`, `autoshot_cut_0012` | Shift attention to automated script terminal outputs. | "results" | Spoken: "...get messy results." | Closes Micro Loop 4. | Hard Cut / Viewport Shift | Solidify the visual consequence of the amateur strategy. |
| 14 | 00:15.23 | `beat_0038`, `autoshot_cut_0013` | Hard cut to screen interface presenting distinct session windows. | "He keeps his" | Spoken: "And that's not all. He keeps..." | Opens Micro Loop 5 (Advanced Systemization Mechanics). | Hard Cut to UI Graphic Workflow | Transition to a rapid-fire list of secondary tactics. |
| 15 | 00:16.50 | `beat_0043`, `autoshot_cut_0014` | Panel wipe showing step-by-step checkboxes updating. | "simple, makes" | Spoken: "...file simple, makes Claude..." | Sustains Micro Loop 5. | UI Step Transition / Auto-Wipe | Match sequential verbal pacing with auto-updating list mechanics. |
| 16 | 00:17.70 | `beat_0046`, `autoshot_cut_0015` | Multi-panel screen tracking simultaneous independent processes. | "check its own" | Spoken: "...check its own work..." | Sustains Micro Loop 5. | Layout Transition (Grid View) | Visually demonstrate "separate sessions" using a grid layout. |
| 17 | 00:19.72 | `beat_0050`, `autoshot_cut_0016` | Hard cut back to talking head profile framing. | "So he's not" | Spoken: "So he's not just prompting..." | Closes Micro Loop 5. | Hard Cut to Creator A-Roll | Re-center the narrative onto the speaker for the ultimate takeaway. |
| 18 | 00:21.05 | `beat_0054`, `autoshot_cut_0017` | Quick screen overlay displaying system diagram summaries. | "better, he's using" | Spoken: "...using Claude code like a system." | Closes Macro Loop. | Informational Graphic Overlay | Provide an abstract visual model matching the "system" punchline. |
| 19 | 00:22.60 | `beat_0058`, `autoshot_cut_0018` | Final transition back to talking head holding a clear call to action. | "Comment creator" | Spoken: "Comment creator, and I'll send..." | Conversion Funnel Action | CTA Card / Freeze Frame Focus | Explicitly prompt engagement using a low-friction keyword. |

---

### Rhythm Metrics & Structural Flow

* **Average Beat Length:** ~1.26 seconds per edit or significant state change ($24.897\text{s} / 19\text{ beats}$).
* **Interrupt Cadence:** The edit style continuously alternates between **A-Roll Monologue**, **Interface Screen Capture**, and **Thematic Cutaways**. A structural interruption occurs roughly every 1.3 seconds, resetting viewer attention spans before cognitive fatigue can occur.
* **Loop Architecture:**
    * **Macro-Loop:** Opened at `00:00.05` via the declaration of an improper standard behavior. It is held open across multiple practical demonstrations and permanently resolved at `00:22.30` with the thesis synthesis (*"using it like a system"*).
    * **Micro-Loops:** Nested mini-narratives running 2–3 seconds apiece (e.g., Creator $\rightarrow$ Expert Proof $\rightarrow$ Code Interface $\rightarrow$ Problem Resolution $\rightarrow$ Creator). Each loop answers one immediate sub-question before triggering the next.
* **Peak Multi-Modal Synchronization:** Occurs between `00:15.23` and `00:19.71` (`beat_0038` to `beat_0046`). Spoken delivery speeds up while listing architectural steps, and the visual workspace updates cleanly in tandem with each spoken item.

---

## D. Audio, Prosody, And Emotion Arc

### Acoustic Landscape
* **Tempo Structure:** Steady speech cadence calculated at approximately 112.5 BPM. The rhythm utilizes an implicit metronome where phrase peaks land predictable emphasis beats.
* **Voice Energy Profile:** High mean vocal pitch ($23.86\text{ semitones}$) combined with a strong standard deviation in amplitude ($0.518\text{ loudness variance}$). This indicates a energetic, highly inflected delivery that avoids monotonic drone.

### Emotional Intensity Curve
```
Intensity
   ^
   |                                     [Payoff Climax: 00:19.72 - 00:22.30]
   |                                                    /-----\
   |                         /-----\                   /       \
   |      /-----\           /       \                 /         \
   |_____/       \_________/         \_______________/           \________ (CTA)
   +--------------------------------------------------------------------------> Time
 00:00         00:04               00:10           00:15       00:20    00:24
```

* **Payoff Moment:** Located at `00:19.79-00:22.64` (`seg_0009`). Spoken volume slightly climbs, vocabulary shifts from step-by-step description to conceptual framing (*"not just prompting better... like a system"*), and visual transitions resolve into a finalized overview diagram.

---

## E. Viral Pattern Facets

### 1. Hook & Entry
* **Form Craft:** Introduce the topic via a direct challenge to the status quo. Frame standard usage as inherently flawed.
* **Content Angle:** Swap "Claude Code" with any developer tool, productivity application, or specialized framework (e.g., *"Most people use Notion databases the wrong way"*).
* **Psychology Substrate:** Leverages loss aversion and FOMO. Viewers who use the tool are immediately anxious that they are wasting effort or missing out on peak output efficiency.

### 2. Narrative & Loop Structure
* **Form Craft:** Divide information into an initial mistake phase, an expert endorsement phase, an operational breakdown phase, and an architectural summary phase.
* **Content Angle:** Substitute the primary authority creator (e.g., transition from an official engineer quote to a recognized design systems expert).
* **Psychology Substrate:** Utilizes authority bias (the expert quote) alongside immediate practical validation to transition the user smoothly from skepticism to high trust.

### 3. Pacing & Visual Editing
* **Form Craft:** Never keep a static asset on screen for longer than 1.5 seconds. alternate between human talking head faces and direct operational workspaces.
* **Content Angle:** Exchange terminal recordings with application canvas screen capture or high-fidelity UI design files.
* **Psychology Substrate:** Pattern-interrupt mechanics prevent habituation, forcing the viewer's focus to actively reset with each physical shift in visual layout.

### 4. Captions & On-Screen Text
* **Form Craft:** Centered, high-contrast, single-phrase or word level animation strings. Emphasize nouns and action predicates using distinct accent colors.
* **Content Angle:** Customize brand styling, typography selections, and color palettes to fit the thematic context of the target niche.
* **Psychology Substrate:** Dual-coding theory. Presenting text that is perfectly synchronous with auditory inputs secures higher comprehension and lower drop-off rates across silent or noisy environments.

### 5. Audio, Color & Multimodal Orchestration
* **Form Craft:** Rely on crisp, localized vocal onsets to drive pacing rather than background music tracks. Keep color schemas split strictly between human environment tones and high-contrast dark-mode workspaces.
* **Content Angle:** Re-grade target video files to alternate between warm personal environments and cool corporate digital applications.
* **Psychology Substrate:** High contrast elements keep information readable across small mobile form factors.

### 6. Platform & Distribution Signals
* **Form Craft:** Build an inbound comment loop directly into the final seconds. Request a specific context-rich keyword rather than a generic profile interaction.
* **Content Angle:** Change the automated lead-magnet phrase from "creator" to target resources like "template", "workflow", or "backend".
* **Psychology Substrate:** Algorithmic signal boosting. Directing users to comment a precise keyword triggers automated delivery infrastructure, boosting engagement metrics and signaling high relevance to platform recommendation engines.

### 7. Emotional & Arousal Design
* **Form Craft:** Maintain a persistent sense of urgency and discovery. Start with an intellectual conflict and systematically transition toward absolute clarity.
* **Content Angle:** Modify workflow examples to evoke specific workflow breakthroughs relevant to different technical user archetypes.
* **Psychology Substrate:** Moves the viewer along a calculated satisfaction pathway—transitioning them from initial curiosity, through structured validation, and arriving at a clear, actionable resolution.

### 8. Content Angle & Subject Strategy
* **Form Craft:** Demystify an intricate, specialized development capability by breaking it down into an elegant, easy-to-understand design methodology.
* **Content Angle:** Pivot the topic from automation configurations to system architecture patterns, UI assembly lines, or script generation workflows.
* **Psychology Substrate:** The simplicity paradox. Viewers are highly attracted to deep, complex topics, but require them to be translated into crisp, modular, easily digestible frameworks.

---

## F. Replication Spec

### Structural Blueprint
1.  **0.0s – 1.8s (The Hook):** Open on a centered talking head. State an assertive, negative-frame critique regarding how an audience uses a specific workflow tool.
2.  **1.8s – 4.0s (The Contrast):** Hard cut to an interface screen capture showing standard operation. Pivot sharply to contrast it with the correct execution method.
3.  **4.0s – 6.2s (The Authority Anchor):** Insert a 2-second external clip of an industry expert or the platform creator explicitly confirming this hidden workflow philosophy.
4.  **6.2s – 12.0s (The Mechanical Breakdown):** Return to the narrator, then cut back and forth between active workspaces every 1.2 seconds. Walk through the core mechanical distinction step-by-step (e.g., Phase A vs. Phase B).
5.  **12.0s – 15.2s (The Consequence Gap):** Re-center onto the speaker to summarize why alternative approaches fail, creating a sharp contrast between messy typical results and clean organized outputs.
6.  **15.2s – 19.7s (The Feature Sprint):** Execute a rapid-fire sequence of interface panels showing auxiliary best-practices, using screen wipes or grid layouts that match your verbal cadence.
7.  **19.7s – 22.6s (The Paradigm Shift Payoff):** Present a definitive summary graphic. Synthesize the individual steps into one overarching mental model.
8.  **22.6s – 24.9s (The Automation Call-to-Action):** Return to a clean talking head frame. Prompt viewers to comment a specific keyword to receive a free detailed implementation guide.

```json
{
  "exemplar": "instagram-real.MP4",
  "pattern_summary": "Negative-frame tool hook transition into authority social proof, followed by a rapid terminal workflow breakdown and a high-value comment automation funnel trigger.",
  "hook_end_signal_ids": ["beat_0005", "autoshot_cut_0001"],
  "payoff_signal_ids": ["beat_0050", "beat_0054", "vis_scene_0017"],
  "needs_review_signal_ids": [],
  "replication_beats": [
    {
      "beat_id": "rep_0001",
      "time": 0.0,
      "cited_signal_ids": ["beat_0001"],
      "purpose": "Establish subject hook framework and deliver cognitive error premise.",
      "recreation_instruction": "Frame narrator closely, center screen, display high-contrast single-phrase overlay stating standard execution is wrong."
    },
    {
      "beat_id": "rep_0002",
      "time": 1.83,
      "cited_signal_ids": ["beat_0005", "autoshot_cut_0001"],
      "purpose": "Expose standard amateur behavior flaws visually.",
      "recreation_instruction": "Hard cut to dark-mode application screen capture showing common low-efficiency input sequences."
    },
    {
      "beat_id": "rep_0003",
      "time": 3.95,
      "cited_signal_ids": ["beat_0010", "autoshot_cut_0003"],
      "purpose": "Introduce social proof anchoring via a recognized industry authority figure.",
      "recreation_instruction": "Insert third-party podcast format video frame showing tool creator verifying the underlying philosophy."
    },
    {
      "beat_id": "rep_0004",
      "time": 6.23,
      "cited_signal_ids": ["beat_0016", "autoshot_cut_0005"],
      "purpose": "Differentiate core workflow states clearly.",
      "recreation_instruction": "Cut back to talking head to introduce key concepts, then alternate rapidly with UI screens that contrast preparation vs execution."
    },
    {
      "beat_id": "rep_0005",
      "time": 11.97,
      "cited_signal_ids": ["beat_0031", "autoshot_cut_0010"],
      "purpose": "Highlight the consequences of ignoring this paradigm shift.",
      "recreation_instruction": "Return to narrator face-to-camera framing. Deliver a high-emphasis structural statement explaining standard failure points."
    },
    {
      "beat_id": "rep_0006",
      "time": 15.23,
      "cited_signal_ids": ["beat_0038", "autoshot_cut_0013"],
      "purpose": "Deliver a fast-paced rundown of advanced operational habits.",
      "recreation_instruction": "Sequence rapid UI transformations (grid panels, updates, list completions) matching each spoken tip in real time."
    },
    {
      "beat_id": "rep_0007",
      "time": 19.72,
      "cited_signal_ids": ["beat_0050", "autoshot_cut_0016"],
      "purpose": "Synthesize individual features into a complete cohesive system.",
      "recreation_instruction": "Display a clean workflow summary graphic over a talking head shot, driving home the main structural takeaway."
    },
    {
      "beat_id": "rep_0008",
      "time": 22.6,
      "cited_signal_ids": ["beat_0058", "autoshot_cut_0018"],
      "purpose": "Trigger automated viewer conversion pipeline.",
      "recreation_instruction": "Maintain direct eye contact with the camera. Pitch a free resource using an explicit comment keyword call to action."
    }
  ]
}
```
