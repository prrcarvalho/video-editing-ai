---
video: instagram-real.MP4
model: gemini-3-flash-thinking
prompt_template: prompts/PROMPT-GEMINI-SIGNAL-GROUNDED.md
generated_at: 20260615T011256Z
analysis_context: /Users/pedrocarvalho/projects/video_editing_ai/gemini_pipeline/outputs/instagram-real/signals/signals_for_gemini.md
---

<details>
<summary>Model thinking</summary>

**Defining the Deliverables**

I'm now clarifying the scope and requirements for the "Viral Pattern Report" using the `SIGNAL PACK` data.


**Defining the Analysis Parameters**

I've established the 2026 timeframe and crucial formatting guidelines for the Viral Pattern Report.



**Analyzing Coherence & Pattern**

I've determined visual cuts match autoshots closely and the dominant viral pattern is "You're Doing It Wrong" with rapid delivery.


**Deconstructing Claude's Usage**

I'm now identifying incorrect Claude code applications, aiming to create a "You're Doing It Wrong" hook.


**Mapping Scene Elements**

I've constructed a scene cut and beat sheet cross-reference for the "You're Doing It Wrong" hook.

</details>

## A. Signal Integrity

The provided signal pack demonstrates exceptional mathematical coherence and physical tracking precision. A rigorous check reveals the following system alignments:
* **Visual/Scene-Cut Consistency:** The algorithmic `autoshot_cut` scores align flawlessly with the `vis_scene` content cuts. For example, `autoshot_cut_0001` (00:01.83, frame 110) directly maps to `vis_scene_0001` (00:01.85, frame 111) with an acceptable sub-frame variance of 0.02 seconds. This consistency is maintained across all 18 visual transitions.
* **Audio Onset Realism:** Rhythmic spikes closely frame the narrative boundaries. For instance, the transition into the video's core value hook at `seg_0004` matches `aud_onset_0055` at 00:06.30.
* **Transcript and Word Alignments:** WhisperX word-level bounding segments show no anomalous gaps or overlaps. Notable pauses are correctly isolated at exactly 3 points, preventing distortion of the calculated articulation velocity.

> **Status:** Coherent. No `needs_review` items identified. The timing matrix is fully validated as the production source of truth.

---

## B. Viral Pattern Summary

* **Dominant Viral Pattern:** The **"Contra-Expert Inversion"** framework. It captures attention by declaring standard behavior wrong, then builds retention by analyzing the optimized workflow used by an elite authority figure.
* **Main Attention-Retention Driver:** An aggressive pacing structure where complex technical UI changes occur every 1.32 seconds. This rapid editing matches a high verbal speed of 265 WPM, keeping viewers focused to avoid missing key technical information.
* **The High-Value Action Moment:** The transition at `seg_0004` (00:06.30), where the narrator reveals the exact structural separation between **"Plan Mode"** and **"Build Mode"**. This is the key moment viewers are likely to save or screenshot.
* **Strongest Reusable Craft Move:** Using a high-contrast terminal theme (dark background with glowing neon syntax) to frame code blocks. This technique turns dry programming work into a vibrant, scannable visual asset.
* **Highest-Risk Detail to Replicate:** The extremely fast articulation rate (331.7 WPM excluding pauses). If a creator attempts this speed without highly expressive voice acting and perfect text-to-voice synchronization, it will cause cognitive fatigue and cause viewers to scroll away.

### Bridge-Variable Analysis

| bridge variable | diagnosis | cited_signal_ids | Recreation implication |
|---|---|---|---|
| **Target Emotion** | Enlightened dissatisfaction shifting into systematic control. | `seg_0001`, `seg_0009` | Start with a critique of current user habits, then transition into a structured solution. |
| **Payoff/Send-Moment** | The systematic breakdown of a secret file workflow. | `seg_0008`, `aud_peak_0020` | Ensure this phase features high-contrast UI highlights and clear visual markers. |
| **Genre Archetype** | Technical Inversion / Workflow Deconstruction. | `seg_0003`, `seg_0005` | Replace general lifestyle commentary with a precise, step-by-step technical teardown. |
| **Funnel Position** | Middle-of-Funnel (MoF) targeting practitioners. | `word_0004`, `word_0005` | Skip basic tool introductions; dive straight into expert-level usage strategies. |
| **Platform Goal Metric** | High Share Rate and Save Rate, supplemented by Comment Automation. | `seg_0010`, `word_0102` | End with a clear keyword trigger ("Comment creator") to automate resource delivery. |
| **Playback Environment** | Muted mobile feeds or fast-paced split-screen browsing. | `vis_scene_0001` to `0018` | Use bold keyword-highlighted captions to ensure the video remains readable when muted. |

---

## C. Hook And Entry Stack

### Hook Boundary Analysis
The programmatic hook terminates precisely at **00:01.81** (`seg_0001`, `word_0008`). 
* **First Spoken Words:** *"Most people use Claude code the wrong way."*
* **Hook Classification:** **Negative Paradigm Frame / Counter-Intuitive Callout.**
* **Open Viewer Question:** *"What exactly am I doing wrong with this tool, and what is the correct approach used by the creator?"*

### The Hook Stack Integration

* **Verbal Hook:** Launches immediately on frame 3 (`word_0001`) with no dead air. It leverages a negative frame ("the wrong way") to create an instant cognitive gap.
* **First-Frame Visual Salience:** Displays a high-contrast terminal execution screen paired with a talking-head video. This composition establishes immediate domain authority.
* **On-Screen Title/Text Hook:** Displays bold, centered text highlighting **"use claude code"** across the speaker's face, utilizing yellow/green styling to draw the eye.
* **Audio Bait / First-Second Curve:** Features an immediate audio onset peak at 00:00.10 (`aud_peak_0001`) hitting a high amplitude of -2.27 dB. This strong start breaks through background noise on the feed.
* **First Pattern Interrupt:** Occurs at 00:01.83 (`autoshot_cut_0001`), cutting cleanly to a zoomed screen capture of automated software scripts running in real time.
* **Re-Hook Segment:** Positioned between 00:04.00 and 00:06.22 (`seg_0003`). It introduces an elite authority figure to validate the hook: *"But the guy who created Claude code does the opposite."*
* **Target Audience Alignment:** The presentation avoids basic definitions. By using specific industry terms like "Claude Code" in the first second, it instantly signals relevance to software engineers and developers while filtering out casual viewers.

---

## D. Signal-Grounded Beat Sheet

This beat sheet condenses the 61 candidate audio-visual markers into major narrative blocks, using the provided signal IDs as the definitive source of truth.

| beat | time | cited_signal_ids | role in loop | visual/text/audio stack | interrupt type | psychology mechanism | transferability | Recreation instruction |
|---|---:|---|---|---|---|---|---|---|
| **01** | 00:00.00 | `beat_0001`, `seg_0001` | Psychological Hook | Talking head + terminal background overlay. Text: "Most people use Claude code..." Audio peak at -2.27 dB. | Media Entry / Baseline | Information Gap / Pattern Interruption | `form_transfers_any_subject` | Deliver a direct, negative frame statement within the first 5 frames. |
| **02** | 00:01.83 | `beat_0005`, `vis_scene_0001`, `seg_0002` | Problem Demonstration | Zoomed UI code execution sequence. Captions switch to "the wrong way." | Hard Camera Cut / Scale Shift | Cognitive Dissonance / Relatability | `form_transfers_any_subject` | Show the inefficient user behavior via a close-up screen recording. |
| **03** | 00:03.13 | `beat_0009`, `vis_scene_0002` | Negative Outcome | Fast-scrolling error logs/terminal outputs. On-screen animation asset appears. | B-Roll Swap | Loss Aversion / Visual Proof | `mixed` | Match fast visual movement with the delivery of negative keywords. |
| **04** | 00:03.95 | `beat_0010`, `vis_scene_0003`, `seg_0003` | Authority Pivot | Cut back to talking head; clean profile shot of industry authority figure inserts. | Subject Matter Cut | Authority Bias / Curated Insight | `form_transfers_any_subject` | Introduce an expert or creator to present the optimal solution. |
| **05** | 00:05.53 | `beat_0014`, `vis_scene_0004` | Secret Revelation | UI Graphic overlay highlighting: **"Section 1: Plan Mode"** | Text overlay over talking head | Reward Prediction Error | `form_transfers_any_subject` | Use bold, clean title cards to introduce named concepts. |
| **06** | 00:06.25 | `beat_0016`, `vis_scene_0005`, `seg_0004` | Conceptual Contrast | Interactive UI panels highlighting "Plan Mode" vs "Build Mode" layout. | UI Layout Flip | Categorization / Mental Chunking | `form_transfers_any_subject` | Contrast the right approach against the wrong approach using explicit labels. |
| **07** | 00:07.42 | `beat_0019`, `vis_scene_0006` | Tactical Step 1 | Code IDE architecture view highlighting project tasks. | Deep Zoom to Asset | Orienting Response | `mixed` | Highlight specific lines of code or text inside the interface. |
| **08** | 00:08.42 | `beat_0022`, `vis_scene_0007` | Tactical Step 2 | Terminal execution blocks flashing completion checkmarks. | Asset State Change | Goal Completion Reward | `mixed` | Show the successful system state right after explaining the step. |
| **09** | 00:09.20 | `beat_0024`, `vis_scene_0008`, `seg_0005` | Mechanical Execution | Code text scrolling upward rapidly; sound frequency broadens. | Kinetic UI Scrolling | Neural Coupling via Motion | `content_specific` | Ensure code animation moves quickly to emphasize workflow speed. |
| **10** | 00:10.92 | `beat_0028`, `vis_scene_0009` | Validation Phase | Return to narrator talking head. Text: "explains why most people..." | Zoom Out to Narrator | Validation / Relief | `form_transfers_any_subject` | Return to the speaker's face when summarizing the core takeaway. |
| **11** | 00:12.00 | `beat_0031`, `vis_scene_0010`, `seg_0006` | Casual Escalation | Code window displaying interactive configuration files. | Context Swap | Zeigarnik Loop (Open Loop) | `form_transfers_any_subject` | Use a transition phrase like "And that's not all" to introduce secondary value. |
| **12** | 00:13.25 | `beat_0035`, `vis_scene_0011` | Optimization Step 1 | Simple file directory structure layout view. | Minimalist B-Roll Cut | Simplicity Bias / Lowering Friction | `mixed` | Match words like "simple" with clean, uncluttered visual layouts. |
| **13** | 00:14.65 | `beat_0036`, `vis_scene_0012`, `seg_0007` | Optimization Step 2 | Self-correcting loop animation on IDE screen. | Dynamic UI State Transition | Trust Generation | `content_specific` | Show automated verification processes in the interface. |
| **14** | 00:15.25 | `beat_0038`, `vis_scene_0013`, `seg_0008` | Optimization Step 3 | Side-by-side terminal session configurations. Loudness peak -2.83 dB. | Spatial Screen Split | Systematic Completeness | `mixed` | Use multi-window visuals to illustrate handling separate tasks simultaneously. |
| **15** | 00:16.52 | `beat_0043`, `vis_scene_0014` | Implementation View | Detailed code repository structures flashing on screen. | Micro-Macro Cut | Continuous Novelty | `content_specific` | Scroll through complex technical files to highlight depth. |
| **16** | 00:17.72 | `beat_0046`, `vis_scene_0015` | Structural Framework | Abstract block diagrams representing code boundaries. | Graphical Flowchart | Cognitive Load Reduction | `form_transfers_any_subject` | Simplify dense workflows into clean, scannable diagrams. |
| **17** | 00:19.73 | `beat_0050`, `vis_scene_0016`, `seg_0009` | Comprehensive Summary | Narrator talking head with code files faintly visible in background. | Frame Focus Reset | Synthesis / Crystallization | `form_transfers_any_subject` | Bring the narrator back into clear focus for the final conclusion. |
| **18** | 00:21.07 | `beat_0054`, `vis_scene_0017` | Final Takeaway | Code repository file blocks fly across the upper third overlay. | Graphic Animation Layer | Arousal-Driven Value Build | `mixed` | Add moving visual elements to maintain energy right before the call to action. |
| **19** | 00:22.62 | `beat_0058`, `vis_scene_0018`, `seg_0010` | Interactive Outro / CTA | Clear talking head pointing downward; "Comment creator" caption lockup. | Static Frame Stabilization | Direct Action Trigger | `form_transfers_any_subject` | Hold a steady close-up shot of the speaker during the final call to action. |

---

### Structural Metric Computations

```
Macro Metrics:
├── Total Video Duration: 24.897 seconds
├── Total Hard Content Cuts: 18 iterations
└── Mean Shot Duration: 1.310 seconds (Pacing Index: Ultra-Fast)
```

* **Pacing Cadence Pattern:** The video maintains a tight visual rotation loop. It switches between a talking-head shot and a high-contrast user interface recording every 1.1 to 1.4 seconds. This strict timing prevents visual fatigue and keeps the viewer engaged.
* **The Structural Loop Map:**
  * **Micro-Looping:** Every visual change is timed directly to technical keywords. For example, the cut at `vis_scene_0004` hits exactly as the word "plan" starts (`word_0039`). This creates a continuous flow of information gaps and resolution loops.
  * **Macro-Looping:** The video is engineered to loop seamlessly. The final phrase, *"send over the free guide"* (`seg_0010`), cuts off right as the audio drops. This matches the opening frame (`beat_0001`), which immediately launches back into *"Most people use..."* This transition creates an infinite playback loop that helps boost retention metrics.
* **Temporal Binding Analysis (100–250 ms Match Window):**
  * `vis_scene_0008` lands within 40 ms of `aud_onset_0076` and exactly matches `word_0044` ("Slows").
  * `vis_scene_0013` executes within 20 ms of `aud_onset_0126` and pairs with `aud_peak_0020`.
  This precise synchronization combines sight, sound, and text to anchor the viewer's attention during key transitions.

---

## E. Audio, Prosody, And Emotion Arc

### Speech Pace vs Audio Tempo
* **Speech Rate (WPM):** **265.1 WPM** across the entire video, with an articulation velocity of **331.7 WPM** when pauses are excluded. This places the narration at a high-energy pace.
* **Rhythmic Audio Pulse (BPM):** **112.5 BPM**. The underlying musical pulse acts as a steady rhythm that anchors the delivery. It provides a solid baseline that makes the fast-paced speech easier to follow without feeling overwhelming.

### Prosody & Emotional Design
* **Voice Profile Analysis:** The speaker maintains a confident, authoritative tone, shown by a stable mean pitch (`F0semitoneFrom27.5Hz_sma3nz_amean`: 23.86). The narrow variance (0.23) avoids wild pitch swings, reinforcing trust and technical competence.
* **Strategic Volume Shifting:** The audio energy is carefully controlled (`loudness_sma3_stddevNorm`: 0.51). It builds momentum during the core value breakdown (`seg_0008`) and peaks significantly at 00:15.43 (`aud_peak_0020`, -2.83 dB). This loud audio peak emphasizes the final rule: *"runs separate sessions for separate problems."*
* **Frisson & Technical Payoffs:** The track uses crisp interface sound effects (mechanical keyboard clicks and UI chimes) layered over a steady bassline. This audio design provides satisfying sensory feedback as technical milestones appear on screen.

---

## F. Captions, Text, And Cognitive Load

```
Caption Architecture Layout
┌────────────────────────────────────────────────────────┐
│                      [VIDEO FRAME]                     │
│                                                        │
│   Primary Visual Area: Talking Head / Terminal IDE    │
│                                                        │
│                                                        │
│   Captions Safe Zone: Lower Third (Center-Aligned)     │
│   Text Container: [ BOLD SANS-SERIF CAPTIONS ]        │
│   Color Strategy: White Core / Yellow Action Keywords  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

* **Caption Sizing and Layout:** The video uses keyword-focused captions placed safely in the lower-third area of the vertical frame. This positioning ensures text remains clearly visible and doesn't get covered by native platform interfaces.
* **Visual Tracking Strategy:** Words appear in small, bite-sized groups (1 to 3 words per line) to match the fast 265 WPM speech rate. This approach allows viewers to read and process key phrases instantly.
* **Managing Cognitive Load:** The video balances information delivery by pairing dense narration with clean, minimalist visuals. When the speaker covers complex ideas, the screen shows simplified UI layouts or clear diagrams. This technique helps prevent information overload, keeping technical details easy to digest.

---

## G. Viral Pattern Facets

### 1. Hook & Entry
* `form_craft`: Launch immediately with a negative frame statement that challenges common user habits.
* `content_angle`: Target specific, widely used software tools or professional development workflows.
* `platform_distribution`: Optimize for the first 1.5 seconds of watch time to prevent users from scrolling past.
* `psychology_substrate`: Triggers the information gap mechanism; users stay to learn how to fix their mistakes.
* `transferability`: `form_transfers_any_subject`

### 2. Narrative & Loop Structure
* `form_craft`: Frame the tutorial as an exclusive look into an industry expert's personal system.
* `content_angle`: Deconstruct technical workflows into clear, step-by-step rules.
* `platform_distribution`: Design the final sentence to flow seamlessly back into the opening frame, encouraging repeat views.
* `psychology_substrate`: Leverages the authority bias to build trust and make insights feel highly valuable.
* `transferability`: `form_transfers_any_subject`

### 3. Pacing & Visual Editing
* `form_craft`: Maintain an fast edit pace with hard cuts every 1.1 to 1.4 seconds.
* `content_angle`: Alternate between a direct talking-head video and crisp, high-contrast screen recordings.
* `platform_distribution`: Keep total video duration under 25 seconds to maximize completion rate metrics.
* `psychology_substrate`: Uses continuous visual changes to stimulate the viewer's orienting response and maintain focus.
* `transferability`: `mixed`

### 4. Captions & On-Screen Text
* `form_craft`: Group text into short 1-3 word lines, using bright color accents on key terms.
* `content_angle`: Use industry-specific technical vocabulary to match the visual presentation.
* `platform_distribution`: Keep text inside safe zones to ensure readability across different mobile feeds.
* `psychology_substrate`: Uses dual-coding theory to reinforce spoken words with clear visual text, boosting comprehension when muted.
* `transferability`: `form_transfers_any_subject`

### 5. Audio, Color & Multimodal Orchestration
* `form_craft`: Keep speech volume consistently high (-2 dB to -5 dB) over a steady musical backing track.
* `content_angle`: Use dark UI themes paired with vibrant accent colors to make code elements stand out.
* `platform_distribution`: Clear, crisp audio delivery ensures high retention on built-in mobile phone speakers.
* `psychology_substrate`: Synchronizing audio peaks with visual cuts creates an engaging, high-energy viewing experience.
* `transferability`: `mixed`

### 6. Platform & Distribution Signals
* `form_craft`: Place an explicit keyword trigger in the last 3 seconds to drive comment engagement.
* `content_angle`: Offer a valuable free resource (like a setup guide or template) in exchange for user comments.
* `platform_distribution`: Automated comment replies help boost engagement velocity, signaling the platform algorithm to expand reach.
* `psychology_substrate`: Lowers user friction by replacing external profile link clicks with a simple comment action.
* `transferability`: `form_transfers_any_subject`

### 7. Emotional & Arousal Design
* `form_craft`: Shift the narrative focus from an initial problem statement to a structured, optimized solution.
* `content_angle`: Position the workflow system as the key to avoiding messy or frustrating results.
* `platform_distribution`: High-energy delivery increases share rates across professional and peer messaging groups.
* `psychology_substrate`: Capitalizes on the desire for efficiency, converting initial frustration into a feeling of productivity.
* `transferability`: `form_transfers_any_subject`

### 8. Content Angle & Subject Strategy
* `form_craft`: Target intermediate to advanced users by focusing on workflow optimization rather than basic tool tutorials.
* `content_angle`: Analyze specialized developer tools, terminal workflows, or automation systems.
* `platform_distribution`: Attracts a dedicated tech audience, which can help drive higher advertiser value (CPM).
* `psychology_substrate`: Validates professional competence while introducing highly practical efficiency tips.
* `transferability`: `content_specific`

---

## H. Recreation Spec

This operational framework defines the structural rules needed to create a new video using the verified pacing and retention patterns of the source material.

### 1. Architectural Timing Configuration
* **Target Total Duration:** 24.00 to 25.00 seconds.
* **Visual Edit Cadence:** Apply hard cuts every 1.20 to 1.35 seconds.
* **Narration Density:** Target a baseline speed of 260 WPM, ensuring clean voice acting with no awkward pauses.

### 2. The Hook Sequence (0.00–2.00s)
* **Visual Framing:** Start with a split-screen or talking-head layout featuring a high-contrast dark interface theme.
* **On-Screen Text Layer:** Center-align a bold caption hook using high-contrast color choices.
* **Audio Track Entry:** The music or voiceover track must hit an immediate volume peak between -2 dB and -3 dB on the very first frame.
* **Script Framework:** `"[Target Audience Group] are using [System/Tool Name] the wrong way."`

### 3. Narrative Pivot & Expert Validation (2.00–6.50s)
* **Visual Rotation:** Cut from the speaker to a close-up recording of the tool in use, followed by a transition introducing the expert reference.
* **Script Framework:** `"They just open it, [perform basic action], and hope for the best. But the team that optimized [System/Tool] does the exact opposite."`

### 4. Core Value Breakdown (6.50–19.50s)
* **Visual Editing Rules:** Use clean title cards and split layouts to present information in organized blocks. Ensure visual cuts align within 100 ms of key spoken phrases.
* **Script Framework:** `"Most of their workflow starts in [Optimized State A], not [Standard State B]. They [Action Step 1] first, clarify the structure, then let the system run. That single shift explains why most people get messy outcomes. To fix this, they keep files clean, force automated self-checks, and separate processes into independent blocks."`

### 5. Call To Action & Continuous Loop (19.50–25.00s)
* **Visual Framing:** Return to a steady talking-head shot. Add subtle visual motion in the upper portion of the frame to maintain energy during the call to action.
* **Script Framework:** `"So it's not just about trying harder, it's about building a consistent system. Comment [Keyword], and I'll send over the complete configuration template."`
* **Loop Transition Rule:** Cut the audio abruptly on the final word to create a smooth, continuous loop back to the opening hook statement.

---

## I. Forward QA Gate For The Recreation

Before rendering the final video asset, verify that the project satisfies all structural quality conditions below:

| QA test | pass condition | why it matters |
|---|---|---|
| **Hook Velocity Test** | Spoken narration starts within the first 3 frames; includes a strong negative frame statement completed under 1.85 seconds. | Prevents users from scrolling past immediately on fast-moving social feeds. |
| **100ms Sync Test** | Every major technical keyword aligns within 6 frames (100 ms at 60 fps) of its corresponding visual cut or UI highlight. | Creates strong audio-visual reinforcement, which helps maintain viewer focus. |
| **Cognitive Load Test** | Visual layouts remain clean and uncluttered whenever the narration velocity exceeds a speed of 300 WPM. | Avoids overwhelming the viewer, ensuring technical details are easy to process. |
| **Pacing Index Check** | The calculated average duration of all visual segments falls strictly between 1.10 and 1.40 seconds. | Maintains an engaging rhythm that helps optimize platform watch-time metrics. |
| **Mute Environment Check** | Key action terms and main subject nouns are highlighted using a distinct color layout in the safe zones. | Ensures the video content remains fully readable and effective on muted mobile feeds. |
| **Phone-Speaker Integrity** | Narration frequencies are optimized between 2 kHz and 5 kHz, sitting clearly above the backing music track. | Guarantees clean, intelligible voice delivery across standard mobile hardware. |
| **Audio Headroom Audit** | Primary audio peaks stay consistently between -2.0 dB and -4.0 dB without showing any digital clipping. | Delivers a clean, high-impact audio presence that commands attention on entry. |
| **Macro-Loop Precision** | The final frame cut creates a smooth rhythmic transition back into the opening second of the video. | Encourages repeat views by making the loop point feel invisible to the audience. |
