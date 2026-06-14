---
video: instagram-real.MP4
model: gemini-3-flash
prompt_template: gemini_pipeline/prompts/PROMPT-GEMINI-SIGNAL-GROUNDED.md
generated_at: 20260614T090136Z
analysis_context: /Users/pedrocarvalho/projects/video_editing_ai/gemini_pipeline/outputs/instagram-real/signals/signals_for_gemini.md
---

## A. Signal Integrity

The provided signal pack for `instagram-real.MP4` is highly coherent and accurately aligns across all modal tracks. The transcript, audio onset, and visual scene-cut markers map directly to the pacing changes observable in the video.

* **Review Status**: No anomalies or discrepancies detected.
* **`needs_review` Items**: None. The signal pack stands as the verified timing source of truth.

---

## B. Hook And Curiosity Logic

* **Hook Content**: Spoken words: *"Most people use Claude Code the wrong way."* (`word_0001` to `word_0008`). On-screen text: *"use claude code"* (`ocr_state_0001` to `ocr_state_0003`).
* **Hook End**: `beat_0008` (00:01.75). This marks the transition from the problem statement to the explanation of typical user behavior via a clean scene cut (`vis_scene_0001`).
* **Hook Classification**: **Negative Frame / Common Mistake**. By telling the viewer they are likely doing something wrong with a trending tool, it creates instant friction.
* **Open Viewer Question**: *"Am I using Claude Code wrong, and what is the correct way that gives better results?"*

---

## C. Signal-Grounded Beat Sheet

### Integrated Edit Timeline

| beat | time | cited_signal_ids | visual purpose | caption/text state | audio/voice cue | loop opened/closed | interrupt type | replication meaning |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **B01** | 00:00.00 | beat_0001, ocr_state_0001 | Establish speaker presence and native tool context. | "use claude code" | High-energy onset (`aud_onset_0001`) | Macro-loop opened (Mistake introduced) | Baseline | Hook viewer with high-relevance tech tool. |
| **B02** | 00:01.75 | beat_0008, vis_scene_0001, seg_0002 | Show terminal UI automation to depict standard usage. | "the wrong way" -> "type what" | Smooth spoken transition (`word_0009`) | Retains open loop | Visual Scene Cut (UI Drop) | Shift from speaker to code interface to maintain pacing. |
| **B03** | 00:03.15 | beat_0013, vis_scene_0002 | Show code execution interface to emphasize "hoping for the best". | "for the best" | Mid-sentence breath control | Retains open loop | Visual Scene Cut (UI Switch) | Maintain immediate sensory variation. |
| **B04** | 00:03.97 | beat_0017, vis_scene_0003, seg_0003 | Cut to authority figure (podcast interview style insert). | "But the guy who" | Strong audio onset (`aud_onset_0034`) | Micro-loop opened (Authority introduced) | Visual Scene Cut (Context Switch) | Introduce social proof to validate the upcoming lesson. |
| **B05** | 00:05.55 | beat_0023, vis_scene_0004 | Return to main speaker for the core pivot statement. | "Claude code" | Emphatic delivery (`word_0027`) | Retains open loop | Visual Scene Cut (Speaker Return) | Re-establish host authority before dropping the solution. |
| **B06** | 00:06.27 | beat_0026, vis_scene_0005, seg_0004 | Flash UI screen detailing technical steps/files. | "does the opposite" -> "Plan Mode" | Immediate vocal pickup (`aud_onset_0055`) | Micro-loop closed (Solution named) | Visual Scene Cut (UI Dashboard) | Match the naming of the solution with an intricate visual asset. |
| **B07** | 00:07.42 | beat_0030, vis_scene_0006 | Zoom/adjust focus on the specific structural planning step. | "Plan Mode" title card graphic | Steady pitch rhythm | Retains open loop | Visual Scene Cut (Graphic Overlay) | Signal a high-value core lesson using a dedicated graphic component. |
| **B08** | 00:08.42 | beat_0034, vis_scene_0007 | Show a thoughtful persona shot to emphasize deep tactical focus. | "not build mode" | Lower pitch cadence | Retains open loop | Visual Scene Cut (B-Roll Insert) | Give conceptual breathing room using abstract narrative footage. |
| **B09** | 00:09.20 | beat_0038, vis_scene_0008, seg_0005 | Highlight specific text lines within terminal UI. | "Slows down first" | Loudness peak (`aud_peak_0015`) | Retains open loop | Visual Scene Cut (Code Detail) | Deliver the foundational framework step-by-step. |
| **B10** | 00:10.92 | beat_0044, vis_scene_0009 | Flash successful code execution checks (green validation iconography). | "lets Claude execute" | High-energy termination (`word_0054`) | Retains open loop | Visual Scene Cut (Validation UI) | Provide visual satisfaction confirming the workflow works. |
| **B11** | 00:12.00 | beat_0048, vis_scene_0010, seg_0006 | Return to speaker profile emphasizing the transformation. | "That one shift alone" | Loudness peak (`aud_peak_0017`) | Macro-loop closed (Value proven) | Visual Scene Cut (Speaker Return) | Drive home the ultimate realization/consequence of the trick. |
| **B12** | 00:13.25 | beat_0053, vis_scene_0011 | Shift back to complex multi-file codebase layout to prove systematic execution. | "messy results" | Fluid sentence connection | Retains open loop | Visual Scene Cut (Code Matrix) | Visually back up the claim that this method beats "messy" code. |
| **B13** | 00:14.65 | beat_0058, vis_scene_0012 | Retain system view while introducing extended sub-tips. | "And that's not all" | Quick pick up (`aud_onset_0120`) | Micro-loop opened (Bonus Value) | Visual Scene Cut (UI Shift) | Use a stackable hook ("And that's not all") to maintain retention. |
| **B14** | 00:15.25 | beat_0060, vis_scene_0013, seg_0008 | Display configuration workspace showing workflow simplicity. | "He keeps his Claude file simple" | High onset strength (`aud_onset_0126`) | Retains open loop | Visual Scene Cut (Workspace UI) | Provide structural proof of the sub-tips. |
| **B15** | 00:16.52 | beat_0065, vis_scene_0014 | Shift window framing to show iterative evaluation loops. | "makes Claude check its own work" | Emphatic vocal drop (`aud_onset_0136`) | Retains open loop | Visual Scene Cut (Framing Shift) | Keep a fast visual cadence while explaining system features. |
| **B16** | 00:17.72 | beat_0070, vis_scene_0015 | Display parallel text chat channels mimicking isolated sessions. | "runs separate sessions" | Even metric flow | Retains open loop | Visual Scene Cut (Split Layout) | Provide an exact layout guide for the modular setup. |
| **B17** | 00:19.73 | beat_0077, vis_scene_0016, seg_0009 | Return to speaker for the grand summary wrap-up. | "using Claude Code like a system" | Rhythmic sentence finish | Retains open loop | Visual Scene Cut (Speaker Return) | Summarize the overarching theme into a single memorable mantra. |
| **B18** | 00:21.07 | beat_0082, vis_scene_0017 | Scroll through raw code logs quickly to imply extensive resource volume. | "like a system" | High momentum modulation | Retains open loop | Visual Scene Cut (Fast Scroll) | Give a final burst of deep technical authority before the CTA. |
| **B19** | 00:22.62 | beat_0088, vis_scene_0018, seg_0010 | Return to speaker with an explicit lead generation call-to-action. | "Comment creator" | Calculated closing cadence | Macro-loop closed (CTA Delivery) | Visual Scene Cut (Speaker Close) | Direct the primed viewer toward conversion. |

* **Merged Beats**: `beat_0002` through `beat_0007` represent continuous text/state parsing within a single sequence and are logically consolidated under the structural milestones **B01** and **B02** to reflect distinct editorial actions.

---

### Timeline Analytics

* **Average Beat / Shot Length**: ~1.31 seconds per visual segment (19 cuts across 24.897 seconds), highlighting an elite retention pacing strategy.
* **Interrupt Cadence**: Fast, continuous rotation. It shifts predictably between: **Speaker Piece-to-Camera** $\rightarrow$ **UI Screencast** $\rightarrow$ **Abstract/Authority B-Roll** $\rightarrow$ **Graphic Asset Card**. The pattern loops roughly every 3-4 beats, keeping cognitive fatigue low.
* **Loop Maps**:
    * *Macro-Loop*: Formed at `beat_0001` ("You are using this wrong") $\rightarrow$ Sustained via tactical reveals $\rightarrow$ Concluded at `beat_0088` with a direct lead magnet exchange ("Get the free guide to fix it").
    * *Micro-Loops*: Nested throughout. For example, `beat_0017` introduces a creator reference, which is answered in `beat_0026`. `beat_0058` drops a stackable hook ("that's not all"), which is paid off by the technical breakdowns through `beat_0077`.
* **Multimodal Sync Strengths**: The absolute strongest point of alignment occurs at `beat_0038` (00:09.20). The voice delivers the word *"Slows"* with a massive loudness peak (`aud_peak_0015`), synchronized exactly with a visual scene cut (`vis_scene_0008`) and an immediate caption rewrite displaying *"Slows down first"*.

---

## D. Audio, Prosody, And Emotion Arc

* **Tempo & Structural Rhythm**: The audio drives a highly steady, continuous rhythm calculated at approximately **112.5 BPM**. This creates a relentless forward momentum free of long pauses or dead air.
* **Voice Energy & Loudness Architecture**: The host employs a tight volume range with standard deviations (`loudness_sma3_stddevNorm`: ~0.51), maintaining an authoritative delivery. Onsets are kept crisp and assertive, dropping significant emphasis spikes on action verbs (e.g., *Most*, *Open*, *Slows*, *Execute*).
* **The Payoff Moment**: The core payoff hits at `beat_0038` to `beat_0044` (00:09.20 - 00:10.92) during the line *"Slows down first, gets the plan right, then lets Claude execute."* Here, the vocal pitch drops to an intentional, instructive tone while the video fires off three fast visual cuts demonstrating clean code architecture and automated checkmarks.

---

## E. Viral Pattern Facets

### 1. Hook & Entry
* **Form Craft**: Open with an adversarial frame targeting a highly relevant industry utility tool. Use the syntax: `[Target Demographic] use [Modern Tool/System] the wrong way.`
* **Content Angle**: Swap "Claude Code" for any contemporary technology, software application, or productivity framework (e.g., *Cursor IDE*, *Excel Macros*, *Figma Components*).
* **Psychology Substrate**: Leverages **loss aversion** and **imposter syndrome**. Viewers who use the tool daily stop scrolling instantly to verify if their current workflow is inefficient or broken.

### 2. Narrative & Loop Structure
* **Form Craft**: Build a multi-layered value sandwich: Problem $\rightarrow$ Anti-Pattern $\rightarrow$ Authority Reveal $\rightarrow$ Core Trick $\rightarrow$ Extra Stacked Value $\rightarrow$ Solution Call-to-Action.
* **Content Angle**: Keep the workflow architecture intact while updating the specific tool metrics and feature sets.
* **Psychology Substrate**: Utilizes **open-loop chaining**. By introducing a secondary hook ("And that's not all") right after resolving the first problem, the creator keeps the viewer hooked past the typical mid-video drop-off point.

### 3. Pacing & Visual Editing
* **Form Craft**: Maintain an uncompromising sub-1.5-second visual cut rate. Never leave a static screen running. Alternate speaking shots with crisp, high-contrast user interface demonstrations.
* **Content Angle**: Swap the terminal UI shots with screen recordings of whichever software aligns with your specific niche.
* **Psychology Substrate**: Combats **visual habituation**. Constantly altering the depth of field and context resets the viewer's attention clock, maintaining high engagement.

### 4. Captions & On-Screen Text
* **Form Craft**: Implement centralized, dynamic 2-3 word captions utilizing distinct primary/secondary color emphasis blocks. Supplement this with clean, retro UI elements (like the pixelated "Plan Mode" title banner).
* **Content Angle**: Translate the style guidelines directly onto the target terminology of the chosen topic.
* **Psychology Substrate**: Enhances **dual-channel processing**. Delivering clean visual textual cues simultaneously with sharp vocal emphasis ensures high clarity even when muted.

### 5. Audio, Color & Multimodal Orchestration
* **Form Craft**: Use a warm, saturated color grade for piece-to-camera segments, balanced by dark-mode interfaces with bright, high-contrast code highlights (neon greens, pinks, cyans).
* **Content Angle**: Maintain the clean, tech-focused aesthetic while swapping code blocks for relevant visual assets like spreadsheets, design canvases, or workflow diagrams.
* **Psychology Substrate**: Uses **chromatic contrast** to anchor focus. Bright accent indicators on dark backgrounds act as visual targets that guide the viewer's eyes to key details.

### 6. Platform & Distribution Signals
* **Form Craft**: Integrate a high-intent comment trigger ("Comment [Keyword] for the guide") right at the video's peak value state.
* **Content Angle**: Tailor the automated asset giveaway to match the specific tool being broken down.
* **Psychology Substrate**: Exploits the **platform algorithm loop**. Swapping low-friction text comments for a high-value resource boosts engagement metrics, signals relevance, and drives the video onto algorithmic feeds.

### 7. Emotional & Arousal Design
* **Form Craft**: Steer the viewer's emotional journey from concern (FOMO) to curiosity, scientific discovery, and finally to feeling empowered by systematic execution.
* **Content Angle**: Rebind the emotional curve by shifting from tech troubleshooting frustrations to the relief of optimized workflows.
* **Psychology Substrate**: Drives **social currency**. Viewers are highly motivated to finish the video and share it because mastering an advanced tool elevates their status among peers.

### 8. Content Angle & Subject Strategy
* **Form Craft**: Demystify elite workflows by revealing the hidden strategies used by the creators of popular tools themselves.
* **Content Angle**: Can be applied to any domain by examining how elite figures use a tool (e.g., *"The designer who built Figma does the opposite..."*).
* **Psychology Substrate**: Leverages the **Authority Bias**. Viewers naturally assign higher credibility to advice that comes directly from the creator or an elite user of a platform.

---

## F. Replication Spec

### 1. Timing & Rhythm Structure
* **Total Target Duration**: 24–26 seconds.
* **Visual Cut Cadence**: Hard cut every 1.1 to 1.4 seconds. No cross-dissolves.
* **Speaker vs. Screen Allocation**:
    * 00:00 - 00:01.75: Speaker On-Camera (Hook)
    * 00:01.75 - 00:03.97: Software/UI Screencast (The Problem)
    * 00:03.97 - 00:05.55: Authority Profile Insert (The Twist)
    * 00:05.55 - 00:12.00: Rapid alternation between Graphic Cards and Interface details (The Secret)
    * 00:12.00 - 00:13.25: Speaker On-Camera (The Realization)
    * 00:13.25 - 00:19.73: High-contrast split-screen application views (The System)
    * 00:19.73 - End: Speaker On-Camera (Summary and CTA Exchange)

### 2. Audio & Vocal Blueprint
* **Speech Delivery Rate**: ~4.4 words per second. Keep delivery punchy and free of long pauses.
* **Audio Accent Pattern**: Apply a 1.5x volume and crisp pitch emphasis on structural verbs (*Stop*, *Plan*, *Check*, *Comment*).
* **BGM Formatting**: Use a minimalist, low-frequency synthetic background beat set to a steady **112–115 BPM**, ducked significantly (-18dB) beneath the vocal track.

### 3. Caption & Graphic Guide
* **Caption Layout**: Center screen, stacked vertically within a 150px safe zone bounding block.
* **Typography Scheme**: Sans-serif bold face text. Main phrases in clean white; high-impact technical nouns or power metrics colored in high-visibility neon yellow or green.
* **Graphic Overlays**: Use sharp, pixelated title cards (e.g., 8-bit text accent banners) to divide major conceptual chapters.

### 4. Interactive Call-To-Action Loop
* **Closing Mechanics**: Frame the final shot on the speaker from 00:22.50 to the end. The speaker must point slightly downward toward the caption zone while stating the exact comment trigger word.
* **Automation Blueprint**: Pair the launch of the video with an automated DM fulfillment sequence triggered by the designated keyword.

---

```json
{
  "exemplar": "instagram-real.MP4",
  "pattern_summary": "High-pacing tutorial pattern analyzing a popular software utility tool by comparing common bad habits against an elite authority workflow, concluding with a keyword-triggered DM comment loop.",
  "hook_end_signal_ids": [
    "beat_0008",
    "vis_scene_0001"
  ],
  "payoff_signal_ids": [
    "beat_0038",
    "aud_peak_0015",
    "vis_scene_0008"
  ],
  "needs_review_signal_ids": [],
  "replication_beats": [
    {
      "beat_id": "R_B01",
      "time": 0.0,
      "cited_signal_ids": [
        "beat_0001"
      ],
      "purpose": "Negative frame hook introducing a common mistake.",
      "recreation_instruction": "Position host center frame talking to camera. Display primary tool title text below the chin line. Deliver the mistake claim with high vocal energy."
    },
    {
      "beat_id": "R_B02",
      "time": 1.75,
      "cited_signal_ids": [
        "beat_0008",
        "vis_scene_0001"
      ],
      "purpose": "Visually demonstrate the incorrect workflow using software screencasts.",
      "recreation_instruction": "Hard cut to a screen recording of the application interface. Show fast mouse movements or typical terminal input to simulate user frustration."
    },
    {
      "beat_id": "R_B03",
      "time": 3.97,
      "cited_signal_ids": [
        "beat_0017",
        "vis_scene_0003"
      ],
      "purpose": "Introduce authority figure to disrupt the narrative flow and validate the solution.",
      "recreation_instruction": "Cut away to a secondary clip or clean profile insert of a known expert or creator to back up your claim."
    },
    {
      "beat_id": "R_B04",
      "time": 6.27,
      "cited_signal_ids": [
        "beat_0026",
        "vis_scene_0005"
      ],
      "purpose": "Present the optimized step-by-step framework.",
      "recreation_instruction": "Alternate rapidly between clean title cards and targeted screen recordings showing the successful workflow in action."
    },
    {
      "beat_id": "R_B05",
      "time": 12.0,
      "cited_signal_ids": [
        "beat_0048",
        "vis_scene_0010"
      ],
      "purpose": "Return to the speaker to deliver a secondary retention hook.",
      "recreation_instruction": "Cut back to the host center frame. Deliver an engaging transitional line like 'And that's not all' to keep viewers hooked for the bonus tips."
    },
    {
      "beat_id": "R_B06",
      "time": 15.25,
      "cited_signal_ids": [
        "beat_0060",
        "vis_scene_0013"
      ],
      "purpose": "Break down the advanced technical details of the systematic approach.",
      "recreation_instruction": "Show split views or close-up captures of the optimized workflow settings to highlight how clean and structured it is."
    },
    {
      "beat_id": "R_B07",
      "time": 22.62,
      "cited_signal_ids": [
        "beat_0088",
        "vis_scene_0018"
      ],
      "purpose": "Deliver a high-conversion call to action to close the video loop.",
      "recreation_instruction": "Return to the host on camera. Look directly into the lens and state the comment trigger keyword clearly, pointing downward to match the caption placement."
    }
  ]
}
```
