# Gemini SDK Visual Evidence Analysis

Video: `/Users/pedrocarvalho/projects/video_editing_ai/assets/instagram-real.MP4`
Generated: `20260618T170432Z`

This is a Visual Evidence Pack for human inspection. It describes observable edit mechanics only; it is not a Viral Pattern report, Beat Sheet, or Recreation spec.

Use the time column as Resolve-style frame timecode (`MM:SS:FF`). The final field is frames at the media FPS, not decimal seconds.

## Run Summary

- Layout timeline rows: 0
- Visual craft events: 3
- Micro passes: 3
- Usage metadata file: `/Users/pedrocarvalho/projects/video_editing_ai/exemplars/instagram-real/gemini_runs/sdk/20260618T170148Z/sdk_usage.json`

## Layout Timeline

| time | anchors | layout | surface roles | focus | confidence | review |
|---|---|---|---|---|---:|---|
|  |  |  |  | no survey layout timeline written |  |  |

## Visual Craft Events

| time | anchors | family | event type | intensity | sync | craft function | basis | confidence | review |
|---|---|---|---|---|---|---|---|---:|---|
| 00:01:51-00:01:55 | edit_boundary_0001, beat_0005 | cut_boundary | hard_cut | strong | beat_sync | pattern_interrupt | visible_plus_audio_signal | 0.95 | no |
| 00:01:51-00:02:13 | word_0010 | screen_ui_interaction | typing_indicator | subtle | word_sync | cognitive_load_reduction | visible_only | 0.90 | no |
| 00:02:21-00:02:21 | edit_boundary_0002, beat_0006 | cut_boundary | jump_cut | medium | beat_sync | pattern_interrupt | visible_plus_audio_signal | 0.85 | yes |

## Event Details

### event_0001 - hard_cut - 00:01:51-00:01:55

- Anchors: `edit_boundary_0001, beat_0005`
- Grounding constraints: `shot_span_ids=edit_span_0002; cut_boundary_ids=edit_boundary_0001; candidate_beat_ids=beat_0005; word_ids=word_0009; prosody_segment_ids=prosody_seg_0002`
- Affected layer: all
- Visible evidence: Hard cut transition to start the split-screen sequence.
- Motion: direction `none`, profile `none`, duration `micro_under_250ms`
- Sync: `beat_sync` - The hard cut aligns perfectly with the start of the word 'They' and beat_0005 audio onset.
- Controlled hypothesis: `pattern_interrupt` based on `visible_plus_audio_signal`
- Recreate visually: Highly relevant to establish visual pacing.
- Review: no. 

### event_0002 - typing_indicator - 00:01:51-00:02:13

- Anchors: `word_0010`
- Grounding constraints: `shot_span_ids=edit_span_0002; word_ids=word_0009, word_0010; prosody_segment_ids=prosody_seg_0002`
- Affected layer: screen_recording
- Visible evidence: Simulated high-speed typing animation of the text 'Calculating...' and then 'Thinking...' inside the Claude Code CLI window.
- Motion: direction `right`, profile `linear`, duration `sustained_over_1500ms`
- Sync: `word_sync` - Terminal animation syncs with voiceover talking about opening and using Claude Code.
- Controlled hypothesis: `cognitive_load_reduction` based on `visible_only`
- Recreate visually: Key UI visual context.
- Review: no. 

### event_0003 - jump_cut - 00:02:21-00:02:21

- Anchors: `edit_boundary_0002, beat_0006`
- Grounding constraints: `shot_span_ids=edit_span_0002; cut_boundary_ids=edit_boundary_0002; candidate_beat_ids=beat_0006; word_ids=word_0011; prosody_segment_ids=prosody_seg_0002`
- Affected layer: screen_recording
- Visible evidence: A sharp jump cut is visible in the terminal CLI state, jumping to print 'Flibbertigibbet...' to fast-track user-experience delay.
- Motion: direction `none`, profile `none`, duration `micro_under_250ms`
- Sync: `beat_sync` - Aligns with the candidate cut at edit_boundary_0002 and beat_0006.
- Controlled hypothesis: `pattern_interrupt` based on `visible_plus_audio_signal`
- Recreate visually: Important to keep CLI demonstration pacing highly responsive.
- Review: yes. The candidate cut has low detector confidence but shows a clear abrupt jump in CLI output.


## Micro Pass Review Notes

### edit_span_0001 - 00:00:00-00:01:51

- FPS: 24.0 (reasons: retry:unparseable_or_non_object_response)
- Review notes: none
- Negative observations: none

### edit_span_0002 - 00:01:51-00:02:21

- FPS: 24.0 (reasons: short_span<=1s, end_boundary_review:edit_boundary_0002, end_boundary_confidence<0.7:edit_boundary_0002)
- Review notes: The transition at the end of the span (00:02:21) skips idle typing delay in the screen recording while maintaining split-screen alignment.
- Negative observations: No zooming, keyframed motion, text formatting changes, or floating graphic stickers in this span.

### edit_span_0003 - 00:02:21-00:03:09

- FPS: 24.0 (reasons: short_span<=1s, start_boundary_review:edit_boundary_0002, start_boundary_confidence<0.7:edit_boundary_0002)
- Review notes: none
- Negative observations: none
