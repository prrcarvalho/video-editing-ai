# Gemini SDK Visual Evidence Analysis

Video: `/Users/pedrocarvalho/projects/video_editing_ai/assets/instagram-real.MP4`
Generated: `20260618T181655Z`

This is a Visual Evidence Pack for human inspection. It describes observable edit mechanics only; it is not a Viral Pattern report, Beat Sheet, or Recreation spec.

Use the time column as Resolve-style frame timecode (`MM:SS:FF`). The final field is frames at the media FPS, not decimal seconds.

## Run Summary

- Layout timeline rows: 12
- Visual craft events: 11
- Micro passes: 0
- Usage metadata file: `/Users/pedrocarvalho/projects/video_editing_ai/exemplars/instagram-real/gemini_runs/sdk/20260618T181458Z/sdk_usage.json`

## Layout Timeline

| time | anchors | layout | surface roles | focus | confidence | review |
|---|---|---|---|---|---:|---|
| 00:00:00-00:01:51 | edit_span_0001 | talking_head_over_broll | screen_recording, talking_head, caption_layer | Claude Code UI demonstrating automated file creation. | 0.95 | no |
| 00:01:51-00:03:09 | edit_span_0002, edit_span_0003 | screen_recording | screen_recording, caption_layer | Google search and Claude terminal input field. | 0.90 | no |
| 00:03:09-00:03:58 | edit_span_0004 | talking_head_over_broll | screen_recording, talking_head, sticker_emoji, caption_layer | Praying hands emoji sticker overlay. | 0.95 | no |
| 00:03:58-00:05:33 | edit_span_0005 | talking_head | b_roll, caption_layer | Podcast speaker. | 0.95 | no |
| 00:05:33-00:06:16 | edit_span_0006 | talking_head | talking_head, caption_layer | Speaker face. | 0.95 | no |
| 00:06:16-00:08:25 | edit_span_0007, edit_span_0008 | talking_head_over_broll | screen_recording, talking_head, caption_layer, graphic_card | Section 1: Plan Mode title graphic. | 0.95 | no |
| 00:08:25-00:09:12 | edit_span_0009 | talking_head | talking_head, caption_layer | Speaker face. | 0.95 | no |
| 00:09:12-00:10:55 | edit_span_0010 | talking_head | talking_head, caption_layer | Host body language (thoughtful contemplation). | 0.95 | no |
| 00:10:55-00:12:00 | edit_span_0011 | talking_head_over_broll | screen_recording, talking_head, caption_layer | Completed green checkmarks on checklist. | 0.95 | no |
| 00:12:00-00:15:15 | edit_span_0012, edit_span_0013, edit_span_0014 | mixed | talking_head, screen_recording, caption_layer | Host facial delivery and visual proof of code results. | 0.95 | no |
| 00:15:15-00:19:44 | edit_span_0015, edit_span_0016, edit_span_0017 | mixed | screen_recording, talking_head, caption_layer | Claude workspace code changes and statistics. | 0.95 | no |
| 00:19:44-00:24:54 | edit_span_0018, edit_span_0019, edit_span_0020 | mixed | screen_recording, talking_head, caption_layer, callout_layer | Comment CREATOR green callout text layer. | 0.95 | no |

## Visual Craft Events

| time | anchors | family | event type | intensity | sync | craft function | basis | confidence | review |
|---|---|---|---|---|---|---|---|---:|---|
| 00:00:00-00:01:51 | edit_span_0001 | caption_text | word-by-word captions | subtle | caption_sync | pattern_interrupt | visible_plus_audio_signal | 0.95 | no |
| 00:00:00-00:01:51 | edit_span_0001 | screen_ui_interaction | typing_indicator | subtle | word_sync | cognitive_load_reduction | visible_only | 0.90 | no |
| 00:01:51-00:01:51 | edit_boundary_0001 | cut_boundary | hard cut | medium | cut_sync | pattern_interrupt | visible_plus_audio_signal | 0.95 | no |
| 00:03:09-00:03:58 | edit_span_0004 | graphic_overlay | sticker_emoji | medium | word_sync | reveal_accent | visible_plus_audio_signal | 0.95 | no |
| 00:03:58-00:03:58 | edit_boundary_0004 | cut_boundary | hard cut | medium | cut_sync | pattern_interrupt | visible_plus_audio_signal | 0.95 | no |
| 00:05:33-00:05:33 | edit_boundary_0005 | cut_boundary | hard cut | medium | cut_sync | pattern_interrupt | visible_plus_audio_signal | 0.95 | no |
| 00:07:25-00:08:25 | edit_span_0008 | graphic_overlay | graphic_card | strong | word_sync | information_chunking | visible_plus_audio_signal | 0.95 | no |
| 00:09:12-00:10:55 | edit_span_0010 | framing_motion | reframe | strong | cut_sync | pattern_interrupt | visible_plus_audio_signal | 0.95 | no |
| 00:10:55-00:12:00 | edit_span_0011 | speed_time | timelapse | strong | word_sync | cognitive_load_reduction | visible_only | 0.95 | no |
| 00:11:37-00:11:45 | edit_span_0011 | screen_ui_interaction | click_indicator | strong | beat_sync | payoff_marker | visible_plus_audio_signal | 0.95 | no |
| 00:22:37-00:24:54 | edit_span_0020 | caption_text | word-by-word captions | strong | word_sync | caption_emphasis | visible_plus_audio_signal | 0.95 | no |

## Event Details

### craft_0001 - word-by-word captions - 00:00:00-00:01:51

- Anchors: `edit_span_0001`
- Grounding constraints: `shot_span_ids=edit_span_0001; candidate_beat_ids=beat_0001; word_ids=word_0001, word_0002, word_0003, word_0004, word_0005; prosody_segment_ids=prosody_seg_0001`
- Affected layer: caption_layer
- Visible evidence: Plain white central caption word transitions saying 'Most people' matching speaker timing.
- Motion: direction `none`, profile `none`, duration `sustained_over_1500ms`
- Sync: `caption_sync` - The word pop alignment tracks perfectly with the starting word 'Most' on frame 3.
- Controlled hypothesis: `pattern_interrupt` based on `visible_plus_audio_signal`
- Recreate visually: High. The opening hook text grabs viewer attention.
- Review: no. 

### craft_0002 - typing_indicator - 00:00:00-00:01:51

- Anchors: `edit_span_0001`
- Grounding constraints: `shot_span_ids=edit_span_0001; word_ids=word_0001, word_0002, word_0003, word_0004, word_0005; prosody_segment_ids=prosody_seg_0001`
- Affected layer: screen_recording
- Visible evidence: Typing cursor inserts 'Calculatin...' and automated command strings on top screen layer.
- Motion: direction `right`, profile `linear`, duration `sustained_over_1500ms`
- Sync: `word_sync` - The screen updates with auto-typing actions synchronized with narrative execution context.
- Controlled hypothesis: `cognitive_load_reduction` based on `visible_only`
- Recreate visually: Medium. Auto-typing helps convey screen demo execution progress.
- Review: no. 

### craft_0003 - hard cut - 00:01:51-00:01:51

- Anchors: `edit_boundary_0001`
- Grounding constraints: `shot_span_ids=edit_span_0001, edit_span_0002; cut_boundary_ids=edit_boundary_0001; candidate_beat_ids=beat_0005; word_ids=word_0009`
- Affected layer: screen_recording
- Visible evidence: Instantaneous cut from the split VS Code terminal view to Google Search browser viewport.
- Motion: direction `none`, profile `none`, duration `micro_under_250ms`
- Sync: `cut_sync` - Transition lands cleanly on word transition 'They' at frame 111.
- Controlled hypothesis: `pattern_interrupt` based on `visible_plus_audio_signal`
- Recreate visually: High. Typical TikTok workflow progression cut.
- Review: no. 

### craft_0004 - sticker_emoji - 00:03:09-00:03:58

- Anchors: `edit_span_0004`
- Grounding constraints: `shot_span_ids=edit_span_0004; cut_boundary_ids=edit_boundary_0003; candidate_beat_ids=beat_0009; word_ids=word_0016, word_0017, word_0018, word_0019, word_0020; prosody_segment_ids=prosody_seg_0002`
- Affected layer: sticker_emoji
- Visible evidence: Yellow praying hands emoji overlay centered on screen.
- Motion: direction `none`, profile `none`, duration `short_250_750ms`
- Sync: `word_sync` - Appears precisely as narrator says 'hope for the best' over frame 189.
- Controlled hypothesis: `reveal_accent` based on `visible_plus_audio_signal`
- Recreate visually: High. High-impact meme representation of the scripted joke.
- Review: no. 

### craft_0005 - hard cut - 00:03:58-00:03:58

- Anchors: `edit_boundary_0004`
- Grounding constraints: `shot_span_ids=edit_span_0004, edit_span_0005; cut_boundary_ids=edit_boundary_0004; candidate_beat_ids=beat_0010; word_ids=word_0021`
- Affected layer: b_roll
- Visible evidence: Clean transition from the Claude terminal to portrait podcast B-roll video.
- Motion: direction `none`, profile `none`, duration `micro_under_250ms`
- Sync: `cut_sync` - The transition lands exactly on the onset 'But' at frame 238.
- Controlled hypothesis: `pattern_interrupt` based on `visible_plus_audio_signal`
- Recreate visually: High. Shifts perspective to support secondary narrative reference.
- Review: no. 

### craft_0006 - hard cut - 00:05:33-00:05:33

- Anchors: `edit_boundary_0005`
- Grounding constraints: `shot_span_ids=edit_span_0005, edit_span_0006; cut_boundary_ids=edit_boundary_0005; candidate_beat_ids=beat_0014; word_ids=word_0028`
- Affected layer: talking_head
- Visible evidence: Hard cut back to the main host portrait close-up.
- Motion: direction `none`, profile `none`, duration `micro_under_250ms`
- Sync: `cut_sync` - Transition coincides with word onset 'does' at frame 333.
- Controlled hypothesis: `pattern_interrupt` based on `visible_plus_audio_signal`
- Recreate visually: High. Keeps dynamic focus centered on host's main narrative.
- Review: no. 

### craft_0007 - graphic_card - 00:07:25-00:08:25

- Anchors: `edit_span_0008`
- Grounding constraints: `shot_span_ids=edit_span_0008; cut_boundary_ids=edit_boundary_0007; candidate_beat_ids=beat_0019; word_ids=word_0038, word_0039, word_0040; prosody_segment_ids=prosody_seg_0004`
- Affected layer: graphic_card
- Visible evidence: Plan Mode neon title card overlay appears in the top screen segment.
- Motion: direction `none`, profile `none`, duration `beat_750_1500ms`
- Sync: `word_sync` - Pops cleanly on 'plan mode' delivery context.
- Controlled hypothesis: `information_chunking` based on `visible_plus_audio_signal`
- Recreate visually: High. Clear chapter title breaks increase visual polish.
- Review: no. 

### craft_0008 - reframe - 00:09:12-00:10:55

- Anchors: `edit_span_0010`
- Grounding constraints: `shot_span_ids=edit_span_0010; cut_boundary_ids=edit_boundary_0009; candidate_beat_ids=beat_0024; word_ids=word_0044, word_0045; prosody_segment_ids=prosody_seg_0005`
- Affected layer: talking_head
- Visible evidence: Reframe wide-angle transition showing host leaning back on desk.
- Motion: direction `none`, profile `snap`, duration `sustained_over_1500ms`
- Sync: `cut_sync` - Landed cleanly on transition 'Slows down' at frame 552.
- Controlled hypothesis: `pattern_interrupt` based on `visible_plus_audio_signal`
- Recreate visually: High. Shifts pacing beautifully to match verbal context.
- Review: no. 

### craft_0009 - timelapse - 00:10:55-00:12:00

- Anchors: `edit_span_0011`
- Grounding constraints: `shot_span_ids=edit_span_0011; cut_boundary_ids=edit_boundary_0010; candidate_beat_ids=beat_0028; word_ids=word_0051, word_0052, word_0053, word_0054; prosody_segment_ids=prosody_seg_0005`
- Affected layer: screen_recording
- Visible evidence: Accelerated terminal screen capture running automated verification workflow checks.
- Motion: direction `up`, profile `linear`, duration `sustained_over_1500ms`
- Sync: `word_sync` - The high speed workflow typing loops over 'then lets Claude execute'.
- Controlled hypothesis: `cognitive_load_reduction` based on `visible_only`
- Recreate visually: Medium. Speeds up technical proof sections.
- Review: no. 

### craft_0010 - click_indicator - 00:11:37-00:11:45

- Anchors: `edit_span_0011`
- Grounding constraints: `shot_span_ids=edit_span_0011; candidate_beat_ids=beat_0030; word_ids=word_0054`
- Affected layer: graphic_card
- Visible evidence: A massive neon green box with a dark checkmark graphic pops over the screen center.
- Motion: direction `in`, profile `bounce`, duration `short_250_750ms`
- Sync: `beat_sync` - The checkmark pops perfectly on a loud peak beat_0030.
- Controlled hypothesis: `payoff_marker` based on `visible_plus_audio_signal`
- Recreate visually: High. Reinforces positive feedback loop logic on programmatic success.
- Review: no. 

### craft_0011 - word-by-word captions - 00:22:37-00:24:54

- Anchors: `edit_span_0020`
- Grounding constraints: `shot_span_ids=edit_span_0020; cut_boundary_ids=edit_boundary_0021; candidate_beat_ids=beat_0058; word_ids=word_0102, word_0103; prosody_segment_ids=prosody_seg_0010`
- Affected layer: callout_layer
- Visible evidence: Neon green background highlighted overlay behind the word 'CREATOR' in final captions.
- Motion: direction `none`, profile `none`, duration `sustained_over_1500ms`
- Sync: `word_sync` - The neon green highlighted text block emphasizes CTA trigger word 'Comment CREATOR' immediately after cut_0021.
- Controlled hypothesis: `caption_emphasis` based on `visible_plus_audio_signal`
- Recreate visually: High. Key trigger highlighted CTA for short form conversions.
- Review: no. 


## Micro Pass Review Notes

No micro passes written yet.
