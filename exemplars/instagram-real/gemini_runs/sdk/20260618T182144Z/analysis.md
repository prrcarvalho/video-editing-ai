# Gemini SDK Visual Evidence Analysis

Video: `/Users/pedrocarvalho/projects/video_editing_ai/assets/instagram-real.MP4`
Generated: `20260618T182414Z`

This is a Visual Evidence Pack for human inspection. It describes observable edit mechanics only; it is not a Viral Pattern report, Beat Sheet, or Recreation spec.

Use the time column as Resolve-style frame timecode (`MM:SS:FF`). The final field is frames at the media FPS, not decimal seconds.

## Run Summary

- Layout timeline rows: 12
- Visual craft events: 14
- Micro passes: 0
- Usage metadata file: `/Users/pedrocarvalho/projects/video_editing_ai/exemplars/instagram-real/gemini_runs/sdk/20260618T182144Z/sdk_usage.json`

## Layout Timeline

| time | anchors | layout | surface roles | focus | confidence | review |
|---|---|---|---|---|---:|---|
| 00:00:00-00:01:51 | edit_span_0001 | split_screen | screen_recording, talking_head, caption_layer | VS Code Claude Code terminal typing automation activity | 0.95 | no |
| 00:01:51-00:02:34 | edit_span_0002, edit_span_0003 | screen_recording | screen_recording, browser_ui, caption_layer | Google Search browser window showing Claude Code link and mouse pointer movement | 0.95 | no |
| 00:02:34-00:03:09 | edit_span_0003 | screen_recording | screen_recording, app_ui, caption_layer | Prompt execution box and automated cursor animation | 0.90 | no |
| 00:03:09-00:03:58 | edit_span_0004 | split_screen | screen_recording, talking_head, sticker_emoji, caption_layer | Rhythmic talking head speaker matching prompt text overlay activity | 0.95 | no |
| 00:03:58-00:05:33 | edit_span_0005 | talking_head | talking_head, b_roll, caption_layer | Podcast interview guest speaking | 0.95 | no |
| 00:05:33-00:06:16 | edit_span_0006 | talking_head | talking_head, caption_layer | Speaker's face and dramatic verbal transition | 0.95 | no |
| 00:06:16-00:09:12 | edit_span_0007, edit_span_0008, edit_span_0009 | split_screen | screen_recording, talking_head, graphic_card, caption_layer | Terminal workspace activity paired with Plan Mode custom popup visual | 0.95 | no |
| 00:09:12-00:10:55 | edit_span_0010 | talking_head | talking_head, background_plate, caption_layer | Speaker performance in context-rich secondary background workspace | 0.95 | no |
| 00:10:55-00:12:00 | edit_span_0011 | screen_recording | screen_recording, app_ui, sticker_emoji, caption_layer | Successful automation code tests scrolling UI | 0.95 | no |
| 00:12:00-00:15:15 | edit_span_0012, edit_span_0013, edit_span_0014 | mixed | screen_recording, talking_head, caption_layer | Speaker articulating contrast between messy outcomes and structured workflows | 0.95 | no |
| 00:15:15-00:17:43 | edit_span_0015, edit_span_0016 | screen_recording | screen_recording, app_ui, caption_layer | Integrated code-scrolling window demonstrating file simplicity rules | 0.90 | no |
| 00:17:43-00:24:54 | edit_span_0017, edit_span_0018, edit_span_0019, edit_span_0020 | mixed | screen_recording, talking_head, caption_layer | System-focused workflow chat demo followed by direct speaker CTA targeting audience growth | 0.95 | no |

## Visual Craft Events

| time | anchors | family | event type | intensity | sync | craft function | basis | confidence | review |
|---|---|---|---|---|---|---|---|---:|---|
| 00:01:51-00:01:51 | edit_boundary_0001 | cut_boundary | hard_cut | strong | word_sync | pattern_interrupt | visible_plus_audio_signal | 0.95 | no |
| 00:03:09-00:03:09 | edit_boundary_0003 | cut_boundary | hard_cut | strong | word_sync | layout_orientation | visible_plus_audio_signal | 0.95 | no |
| 00:03:58-00:03:58 | edit_boundary_0004 | cut_boundary | hard_cut | strong | word_sync | pattern_interrupt | visible_plus_audio_signal | 0.95 | no |
| 00:05:33-00:05:33 | edit_boundary_0005 | cut_boundary | hard_cut | strong | word_sync | pattern_interrupt | visible_only | 0.90 | no |
| 00:06:16-00:06:16 | edit_boundary_0006 | cut_boundary | hard_cut | strong | word_sync | layout_orientation | visible_plus_audio_signal | 0.95 | no |
| 00:07:25-00:07:25 | edit_boundary_0007 | cut_boundary | hard_cut | medium | word_sync | reveal_accent | visible_plus_audio_signal | 0.90 | no |
| 00:09:12-00:09:12 | edit_boundary_0009 | cut_boundary | hard_cut | strong | word_sync | pattern_interrupt | visible_plus_audio_signal | 0.95 | no |
| 00:10:55-00:10:55 | edit_boundary_0010 | cut_boundary | hard_cut | strong | word_sync | pattern_interrupt | visible_plus_audio_signal | 0.95 | no |
| 00:12:00-00:12:00 | edit_boundary_0011 | cut_boundary | hard_cut | strong | word_sync | layout_orientation | visible_plus_audio_signal | 0.95 | no |
| 00:07:25-00:08:25 | edit_span_0008 | graphic_overlay | graphic_card | medium | word_sync | reveal_accent | visible_plus_audio_signal | 0.95 | no |
| 00:10:55-00:12:00 | edit_span_0011 | graphic_overlay | sticker | strong | word_sync | reveal_accent | visible_plus_audio_signal | 0.95 | no |
| 00:00:00-00:24:54 | prosody_seg_0001, prosody_seg_0005, prosody_seg_0006, prosody_seg_0010 | caption_text | word_by_word_captions | medium | caption_sync | cognitive_load_reduction | visible_plus_audio_signal | 0.98 | no |
| 00:01:51-00:02:30 | beat_0005, beat_0006 | screen_ui_interaction | click_indicator | subtle | word_sync | interaction_focus | visible_plus_audio_signal | 0.90 | no |
| 00:03:09-00:03:58 | beat_0009, beat_0010 | graphic_overlay | sticker | medium | word_sync | reveal_accent | visible_plus_audio_signal | 0.95 | no |

## Event Details

### craft_event_0001 - hard_cut - 00:01:51-00:01:51

- Anchors: `edit_boundary_0001`
- Grounding constraints: `shot_span_ids=edit_span_0001, edit_span_0002; cut_boundary_ids=edit_boundary_0001; candidate_beat_ids=beat_0005; word_ids=word_0008, word_0009; prosody_segment_ids=prosody_seg_0001, prosody_seg_0002`
- Affected layer: all
- Visible evidence: Sudden vertical shift from 50-50 vertical split-screen terminal layout to full height browser search recording.
- Motion: direction `none`, profile `snap`, duration `flash_1_4_frames`
- Sync: `word_sync` - Hard cut lands precisely on the conclusion of 'way.' and segment transition boundary.
- Controlled hypothesis: `pattern_interrupt` based on `visible_plus_audio_signal`
- Recreate visually: Crucial edit pace dynamic separating setup statement from visual search execution.
- Review: no. 

### craft_event_0002 - hard_cut - 00:03:09-00:03:09

- Anchors: `edit_boundary_0003`
- Grounding constraints: `shot_span_ids=edit_span_0003, edit_span_0004; cut_boundary_ids=edit_boundary_0003; candidate_beat_ids=beat_0009; word_ids=word_0015, word_0016; prosody_segment_ids=prosody_seg_0002`
- Affected layer: all
- Visible evidence: Hard cut returning to split-screen format, adding static prayer hands emoji visual.
- Motion: direction `none`, profile `snap`, duration `flash_1_4_frames`
- Sync: `word_sync` - Cut occurs exactly at the end of spoken word 'want,' to cue split layout.
- Controlled hypothesis: `layout_orientation` based on `visible_plus_audio_signal`
- Recreate visually: Establishes narrative rhythm by returning speaker facecam under terminal code demo.
- Review: no. 

### craft_event_0003 - hard_cut - 00:03:58-00:03:58

- Anchors: `edit_boundary_0004`
- Grounding constraints: `shot_span_ids=edit_span_0004, edit_span_0005; cut_boundary_ids=edit_boundary_0004; candidate_beat_ids=beat_0010; word_ids=word_0020, word_0021; prosody_segment_ids=prosody_seg_0002, prosody_seg_0003`
- Affected layer: all
- Visible evidence: Cut to external B-roll talking head speaker (bald guest in podcast studio set).
- Motion: direction `none`, profile `snap`, duration `flash_1_4_frames`
- Sync: `word_sync` - Precisely matched to transition from segment 2 ('best.') to segment 3 ('But').
- Controlled hypothesis: `pattern_interrupt` based on `visible_plus_audio_signal`
- Recreate visually: Integrates high value social proof asset into tutorial format.
- Review: no. 

### craft_event_0004 - hard_cut - 00:05:33-00:05:33

- Anchors: `edit_boundary_0005`
- Grounding constraints: `shot_span_ids=edit_span_0005, edit_span_0006; cut_boundary_ids=edit_boundary_0005; candidate_beat_ids=beat_0014; word_ids=word_0028; prosody_segment_ids=prosody_seg_0003`
- Affected layer: all
- Visible evidence: Hard cut back to close up of primary speaker, framing him slightly to the left of frame center.
- Motion: direction `none`, profile `snap`, duration `flash_1_4_frames`
- Sync: `word_sync` - Cut occurs near 'does' to focus viewer attention on primary narrator.
- Controlled hypothesis: `pattern_interrupt` based on `visible_only`
- Recreate visually: Smooth re-centering of narrator authority.
- Review: no. 

### craft_event_0005 - hard_cut - 00:06:16-00:06:16

- Anchors: `edit_boundary_0006`
- Grounding constraints: `shot_span_ids=edit_span_0006, edit_span_0007; cut_boundary_ids=edit_boundary_0006; candidate_beat_ids=beat_0016; word_ids=word_0030, word_0031; prosody_segment_ids=prosody_seg_0003, prosody_seg_0004`
- Affected layer: all
- Visible evidence: Sudden transition back to the dark VS Code split screen setup.
- Motion: direction `none`, profile `snap`, duration `flash_1_4_frames`
- Sync: `word_sync` - Synced with the critical transition from 'opposite.' to 'He'.
- Controlled hypothesis: `layout_orientation` based on `visible_plus_audio_signal`
- Recreate visually: Maintains structural split rhythm during main technical explanations.
- Review: no. 

### craft_event_0006 - hard_cut - 00:07:25-00:07:25

- Anchors: `edit_boundary_0007`
- Grounding constraints: `shot_span_ids=edit_span_0007, edit_span_0008; cut_boundary_ids=edit_boundary_0007; candidate_beat_ids=beat_0019; word_ids=word_0036, word_0037; prosody_segment_ids=prosody_seg_0004`
- Affected layer: all
- Visible evidence: Jump cut/hard cut framing shift within split layout, introducing 'Plan Mode' overlay card.
- Motion: direction `none`, profile `snap`, duration `flash_1_4_frames`
- Sync: `word_sync` - Cut is placed directly before 'start' to coordinate card appearance.
- Controlled hypothesis: `reveal_accent` based on `visible_plus_audio_signal`
- Recreate visually: Smooth structural punctuation pointing to important interface modal details.
- Review: no. 

### craft_event_0007 - hard_cut - 00:09:12-00:09:12

- Anchors: `edit_boundary_0009`
- Grounding constraints: `shot_span_ids=edit_span_0009, edit_span_0010; cut_boundary_ids=edit_boundary_0009; candidate_beat_ids=beat_0024; word_ids=word_0043, word_0044; prosody_segment_ids=prosody_seg_0004, prosody_seg_0005`
- Affected layer: all
- Visible evidence: Cut to alternative medium-wide bookshelf desk workspace angle.
- Motion: direction `none`, profile `snap`, duration `flash_1_4_frames`
- Sync: `word_sync` - Perfect sync separating 'mode.' from segment 5's opening word 'Slows'.
- Controlled hypothesis: `pattern_interrupt` based on `visible_plus_audio_signal`
- Recreate visually: Provides necessary layout variety so the narrative doesn't feel monotonous.
- Review: no. 

### craft_event_0008 - hard_cut - 00:10:55-00:10:55

- Anchors: `edit_boundary_0010`
- Grounding constraints: `shot_span_ids=edit_span_0010, edit_span_0011; cut_boundary_ids=edit_boundary_0010; candidate_beat_ids=beat_0028; word_ids=word_0050, word_0051; prosody_segment_ids=prosody_seg_0005`
- Affected layer: all
- Visible evidence: Sudden hard cut from talking head to full screen recording of automated green checkmark executions.
- Motion: direction `none`, profile `snap`, duration `flash_1_4_frames`
- Sync: `word_sync` - Cut lands exactly on the onset of 'then' during delivery.
- Controlled hypothesis: `pattern_interrupt` based on `visible_plus_audio_signal`
- Recreate visually: Shifts focus entirely to code execution results.
- Review: no. 

### craft_event_0009 - hard_cut - 00:12:00-00:12:00

- Anchors: `edit_boundary_0011`
- Grounding constraints: `shot_span_ids=edit_span_0011, edit_span_0012; cut_boundary_ids=edit_boundary_0011; candidate_beat_ids=beat_0031; word_ids=word_0054, word_0055; prosody_segment_ids=prosody_seg_0005, prosody_seg_0006`
- Affected layer: all
- Visible evidence: Transition returning to primary tight close up talking head.
- Motion: direction `none`, profile `snap`, duration `flash_1_4_frames`
- Sync: `word_sync` - Transitions clean at start of word 'That' in segment 6.
- Controlled hypothesis: `layout_orientation` based on `visible_plus_audio_signal`
- Recreate visually: Enforces a direct personal tone during structural conclusions.
- Review: no. 

### craft_event_0010 - graphic_card - 00:07:25-00:08:25

- Anchors: `edit_span_0008`
- Grounding constraints: `shot_span_ids=edit_span_0008; cut_boundary_ids=edit_boundary_0007; candidate_beat_ids=beat_0019, beat_0020; word_ids=word_0037, word_0038, word_0039, word_0040; prosody_segment_ids=prosody_seg_0004`
- Affected layer: graphic_card
- Visible evidence: Floating UI window overlay card reading 'Section 1 Plan Mode' with sleek neon purple outline.
- Motion: direction `in`, profile `ease_out`, duration `beat_750_1500ms`
- Sync: `word_sync` - The card slides in and highlights active screen area precisely during words 'plan mode'.
- Controlled hypothesis: `reveal_accent` based on `visible_plus_audio_signal`
- Recreate visually: Premium visual anchor identifying custom sections.
- Review: no. 

### craft_event_0011 - sticker - 00:10:55-00:12:00

- Anchors: `edit_span_0011`
- Grounding constraints: `shot_span_ids=edit_span_0011; cut_boundary_ids=edit_boundary_0010; candidate_beat_ids=beat_0028, beat_0029; word_ids=word_0051, word_0052, word_0053, word_0054; prosody_segment_ids=prosody_seg_0005`
- Affected layer: sticker_emoji
- Visible evidence: Slightly bouncing giant green checkmark checkbox graphics popping up over the scrolling tests.
- Motion: direction `none`, profile `bounce`, duration `beat_750_1500ms`
- Sync: `word_sync` - Green checks pop up sequentially with the successful terminal test reports as Claude 'executes'.
- Controlled hypothesis: `reveal_accent` based on `visible_plus_audio_signal`
- Recreate visually: Visual satisfaction cues demonstrating automated software success.
- Review: no. 

### craft_event_0012 - word_by_word_captions - 00:00:00-00:24:54

- Anchors: `prosody_seg_0001, prosody_seg_0005, prosody_seg_0006, prosody_seg_0010`
- Grounding constraints: `shot_span_ids=edit_span_0001, edit_span_0006, edit_span_0011, edit_span_0015, edit_span_0020; prosody_segment_ids=prosody_seg_0001, prosody_seg_0005, prosody_seg_0006, prosody_seg_0010`
- Affected layer: caption_layer
- Visible evidence: Centrally placed vertical short-form active-word highlighted captions utilizing color emphasis.
- Motion: direction `none`, profile `snap`, duration `sustained_over_1500ms`
- Sync: `caption_sync` - The coloring follows WhisperX vocal timings exactly, utilizing red for mistakes ('wrong way', 'messy') and green for success ('Claude Code', 'execute').
- Controlled hypothesis: `cognitive_load_reduction` based on `visible_plus_audio_signal`
- Recreate visually: Primary retention tool essential for portrait video structures.
- Review: no. 

### craft_event_0013 - click_indicator - 00:01:51-00:02:30

- Anchors: `beat_0005, beat_0006`
- Grounding constraints: `shot_span_ids=edit_span_0002; cut_boundary_ids=edit_boundary_0001; candidate_beat_ids=beat_0005, beat_0006; word_ids=word_0009, word_0010; prosody_segment_ids=prosody_seg_0002`
- Affected layer: screen_recording
- Visible evidence: A cursor moves toward search links, generating a round semi-transparent yellow click highlight effect upon clicking.
- Motion: direction `mixed`, profile `ease_in_out`, duration `micro_under_250ms`
- Sync: `word_sync` - Indicator hits on word 'open' as narrator describes opening the tool.
- Controlled hypothesis: `interaction_focus` based on `visible_plus_audio_signal`
- Recreate visually: Improves screen readability by drawing eyes directly to critical UI actions.
- Review: no. 

### craft_event_0014 - sticker - 00:03:09-00:03:58

- Anchors: `beat_0009, beat_0010`
- Grounding constraints: `shot_span_ids=edit_span_0004; cut_boundary_ids=edit_boundary_0003; candidate_beat_ids=beat_0009, beat_0010; word_ids=word_0017; prosody_segment_ids=prosody_seg_0002`
- Affected layer: sticker_emoji
- Visible evidence: Static blue & yellow prayer hands emoji sitting centrally on the split-screen border line.
- Motion: direction `none`, profile `none`, duration `beat_750_1500ms`
- Sync: `word_sync` - The emoji is placed exactly as 'hope' is spoken by the presenter.
- Controlled hypothesis: `reveal_accent` based on `visible_plus_audio_signal`
- Recreate visually: Playful symbolic accent that keeps the split layout engaging.
- Review: no. 


## Micro Pass Review Notes

No micro passes written yet.
