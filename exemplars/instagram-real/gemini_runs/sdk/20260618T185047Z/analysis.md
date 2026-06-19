# Gemini SDK Visual Evidence Analysis

Video: `/Users/pedrocarvalho/projects/video_editing_ai/assets/instagram-real.MP4`
Generated: `20260618T185133Z`

This is a Visual Evidence Pack for human inspection. It describes observable edit mechanics only; it is not a Viral Pattern report, Beat Sheet, or Recreation spec.

Use the time column as Resolve-style frame timecode (`MM:SS:FF`). The final field is frames at the media FPS, not decimal seconds.

## Run Summary

- Layout timeline rows: 0
- Visual craft events: 2
- Micro passes: 1
- Usage metadata file: `/Users/pedrocarvalho/projects/video_editing_ai/exemplars/instagram-real/gemini_runs/sdk/20260618T185047Z/sdk_usage.json`

## Layout Timeline

| time | anchors | layout | surface roles | focus | confidence | review |
|---|---|---|---|---|---:|---|
|  |  |  |  | no survey layout timeline written |  |  |

## Visual Craft Events

| time | anchors | family | event type | intensity | sync | craft function | basis | confidence | review |
|---|---|---|---|---|---|---|---|---:|---|
| 00:01:51-00:01:51 | edit_boundary_0001, sync_0001 | cut_boundary | hard_cut | strong | word_sync | pattern_interrupt | visible_plus_audio_signal | 0.95 | no |
| 00:01:51-00:02:21 | edit_boundary_0001, word_0009 | caption_text | caption_pop | medium | caption_sync | caption_emphasis | visible_plus_audio_signal | 0.95 | no |

## Event Details

### craft_event_0001 - hard_cut - 00:01:51-00:01:51

- Anchors: `edit_boundary_0001, sync_0001`
- Grounding constraints: `shot_span_ids=edit_span_0001, edit_span_0002; cut_boundary_ids=edit_boundary_0001; candidate_beat_ids=beat_0005; word_ids=word_0008, word_0009; prosody_segment_ids=prosody_seg_0001, prosody_seg_0002; audio_signal_ids=aud_onset_0014`
- Affected layer: background_plate
- Visible evidence: Hard cut from talking head footage to web browser screen recording.
- Motion: direction `none`, profile `none`, duration `flash_1_4_frames`
- Sync: `word_sync` - Cut is frame-accurate to word_0009 ('They') and aud_onset_0014.
- Controlled hypothesis: `pattern_interrupt` based on `visible_plus_audio_signal`
- Recreate visually: Essential transition to change visual context in sync with the audio topic change.
- Review: no. 

### craft_event_0002 - caption_pop - 00:01:51-00:02:21

- Anchors: `edit_boundary_0001, word_0009`
- Grounding constraints: `shot_span_ids=edit_span_0002; cut_boundary_ids=edit_boundary_0001; candidate_beat_ids=beat_0005; word_ids=word_0009, word_0010, word_0011; prosody_segment_ids=prosody_seg_0002`
- Affected layer: caption_layer
- Visible evidence: Subtitles update instantly to 'They open it' with red and white styling matching voice onset.
- Motion: direction `none`, profile `none`, duration `sustained_over_1500ms`
- Sync: `caption_sync` - Subtitle appearance is perfectly synced to the spoken words 'They open it'.
- Controlled hypothesis: `caption_emphasis` based on `visible_plus_audio_signal`
- Recreate visually: Critical for viewer retention and comprehension during fast pacing.
- Review: no. 


## Micro Pass Review Notes

### post_cut_edit_boundary_0001 - 00:01:45-00:02:45

- FPS: 24.0 (reasons: post_cut_boundary_window, hard_cut_with_detector_agreement)
- Review notes: Hard cut matches voice delivery rate, transitioning from talking head mode to a visual screen recording cleanly.
- Negative observations: No post-cut digital zoom or camera motion was applied to the screen recording immediately after the cut.
