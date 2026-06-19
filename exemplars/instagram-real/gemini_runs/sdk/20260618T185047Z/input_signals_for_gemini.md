# Compact Post-Cut Motion Signal Contexts

These are the exact compact deterministic contexts sent to Gemini for the post-cut motion test.
Each request receives only one boundary-local context plus the short video offset window.

## edit_boundary_0001

```json
{
  "adjacent_spans": {
    "next_span": {
      "duration": 0.5062,
      "end_boundary_id": "edit_boundary_0002",
      "end_frame": 141,
      "end_timecode": "00:02:21",
      "signal_id": "edit_span_0002",
      "start_boundary_id": "edit_boundary_0001",
      "start_frame": 111,
      "start_timecode": "00:01:51"
    },
    "previous_span": {
      "duration": 1.8438,
      "end_boundary_id": "edit_boundary_0001",
      "end_frame": 111,
      "end_timecode": "00:01:51",
      "signal_id": "edit_span_0001",
      "start_boundary_id": "media_start",
      "start_frame": 0,
      "start_timecode": "00:00:00"
    }
  },
  "boundary": {
    "confidence": 0.95,
    "event_kind": "hard_cut_with_detector_agreement",
    "frame": 111,
    "needs_review": false,
    "signal_id": "edit_boundary_0001",
    "source_signal_ids": [
      "autoshot_cut_0001",
      "vis_diff_0001",
      "vis_scene_0001"
    ],
    "sync_signal_ids": [
      "sync_0001"
    ],
    "timecode": "00:01:51"
  },
  "contract": [
    "Use only this compact deterministic context as timing truth.",
    "Inspect the post-cut window for visible motion/edit mechanics.",
    "Do not infer transcript words, cut boundaries, shot spans, or decimal seconds.",
    "If no post-cut punch/zoom/reframe/crop/resize/shake is visible, say that in negative_observations."
  ],
  "inspection_window": {
    "boundary_frame": 111,
    "boundary_id": "edit_boundary_0001",
    "boundary_timecode": "00:01:51",
    "end_frame": 165,
    "end_timecode": "00:02:45",
    "start_frame": 105,
    "start_timecode": "00:01:45"
  },
  "media": {
    "duration_timecode": "00:24:54",
    "filename": "instagram-real.MP4",
    "fps": 60.0,
    "resolution": {
      "height": 1920,
      "width": 1080
    }
  },
  "nearby_candidate_beats": [
    {
      "frame": 110,
      "signal_id": "beat_0005",
      "source_signal_ids": [
        "autoshot_cut_0001",
        "vis_diff_0001",
        "vis_scene_0001",
        "seg_0002",
        "aud_onset_0014",
        "aud_peak_0005"
      ],
      "source_types": [
        "audio_loudness_peak",
        "audio_onset",
        "transcript_segment_start",
        "visual_autoshot_cut",
        "visual_frame_diff",
        "visual_scene_cut"
      ],
      "timecode": "00:01:50"
    },
    {
      "frame": 134,
      "signal_id": "beat_0006",
      "source_signal_ids": [
        "aud_peak_0006",
        "autoshot_candidate_0001",
        "aud_onset_0019"
      ],
      "source_types": [
        "audio_loudness_peak",
        "audio_onset",
        "visual_autoshot_candidate"
      ],
      "timecode": "00:02:14"
    },
    {
      "frame": 150,
      "signal_id": "beat_0007",
      "source_signal_ids": [
        "aud_peak_0007"
      ],
      "source_types": [
        "audio_loudness_peak"
      ],
      "timecode": "00:02:30"
    },
    {
      "frame": 164,
      "signal_id": "beat_0008",
      "source_signal_ids": [
        "aud_onset_0023",
        "aud_peak_0008"
      ],
      "source_types": [
        "audio_loudness_peak",
        "audio_onset"
      ],
      "timecode": "00:02:44"
    }
  ],
  "nearby_prosody_segments": [
    {
      "delivery_tags": [
        "fast_speech",
        "low_relative_pitch",
        "high_relative_pitch_range"
      ],
      "end_frame": 109,
      "end_timecode": "00:01:49",
      "segment_id": "seg_0001",
      "signal_id": "prosody_seg_0001",
      "start_frame": 3,
      "start_timecode": "00:00:03",
      "text": "Most people use Claude code the wrong way.",
      "wpm": 272.418
    },
    {
      "delivery_tags": [
        "very_fast_speech",
        "high_relative_speech_rate",
        "low_relative_pitch",
        "high_relative_pitch_range"
      ],
      "end_frame": 234,
      "end_timecode": "00:03:54",
      "segment_id": "seg_0002",
      "signal_id": "prosody_seg_0002",
      "start_frame": 111,
      "start_timecode": "00:01:51",
      "text": "They open it, type what they want, and hope for the best.",
      "wpm": 352.595
    }
  ],
  "nearby_words": [
    {
      "end_frame": 98,
      "end_timecode": "00:01:38",
      "signal_id": "word_0007",
      "start_frame": 87,
      "start_timecode": "00:01:27",
      "word": "wrong"
    },
    {
      "end_frame": 109,
      "end_timecode": "00:01:49",
      "signal_id": "word_0008",
      "start_frame": 100,
      "start_timecode": "00:01:40",
      "word": "way."
    },
    {
      "end_frame": 118,
      "end_timecode": "00:01:58",
      "signal_id": "word_0009",
      "start_frame": 111,
      "start_timecode": "00:01:51",
      "word": "They"
    },
    {
      "end_frame": 133,
      "end_timecode": "00:02:13",
      "signal_id": "word_0010",
      "start_frame": 122,
      "start_timecode": "00:02:02",
      "word": "open"
    },
    {
      "end_frame": 140,
      "end_timecode": "00:02:20",
      "signal_id": "word_0011",
      "start_frame": 135,
      "start_timecode": "00:02:15",
      "word": "it,"
    },
    {
      "end_frame": 154,
      "end_timecode": "00:02:34",
      "signal_id": "word_0012",
      "start_frame": 145,
      "start_timecode": "00:02:25",
      "word": "type"
    },
    {
      "end_frame": 163,
      "end_timecode": "00:02:43",
      "signal_id": "word_0013",
      "start_frame": 156,
      "start_timecode": "00:02:36",
      "word": "what"
    },
    {
      "end_frame": 171,
      "end_timecode": "00:02:51",
      "signal_id": "word_0014",
      "start_frame": 164,
      "start_timecode": "00:02:44",
      "word": "they"
    },
    {
      "end_frame": 188,
      "end_timecode": "00:03:08",
      "signal_id": "word_0015",
      "start_frame": 175,
      "start_timecode": "00:02:55",
      "word": "want,"
    }
  ],
  "purpose": "post_cut_motion_inspection",
  "sync_window": {
    "binding_window_ms": 250,
    "event_signal_id": "edit_boundary_0001",
    "nearest_audio": {
      "kind": "audio_onset",
      "offset_ms": 39.5,
      "signal_id": "aud_onset_0014",
      "strength": 13.815112,
      "timecode": "00:01:53"
    },
    "nearest_word": {
      "offset_ms": 69.2,
      "signal_id": "word_0009",
      "word": "They"
    },
    "signal_id": "sync_0001",
    "timecode": "00:01:51"
  }
}
```

## edit_boundary_0002

```json
{
  "adjacent_spans": {
    "next_span": {
      "duration": 0.7938,
      "end_boundary_id": "edit_boundary_0003",
      "end_frame": 189,
      "end_timecode": "00:03:09",
      "signal_id": "edit_span_0003",
      "start_boundary_id": "edit_boundary_0002",
      "start_frame": 141,
      "start_timecode": "00:02:21"
    },
    "previous_span": {
      "duration": 0.5062,
      "end_boundary_id": "edit_boundary_0002",
      "end_frame": 141,
      "end_timecode": "00:02:21",
      "signal_id": "edit_span_0002",
      "start_boundary_id": "edit_boundary_0001",
      "start_frame": 111,
      "start_timecode": "00:01:51"
    }
  },
  "boundary": {
    "confidence": 0.45,
    "event_kind": "candidate_cut_review",
    "frame": 141,
    "needs_review": true,
    "signal_id": "edit_boundary_0002",
    "source_signal_ids": [
      "autoshot_candidate_0001"
    ],
    "sync_signal_ids": [
      "sync_0002"
    ],
    "timecode": "00:02:21"
  },
  "contract": [
    "Use only this compact deterministic context as timing truth.",
    "Inspect the post-cut window for visible motion/edit mechanics.",
    "Do not infer transcript words, cut boundaries, shot spans, or decimal seconds.",
    "If no post-cut punch/zoom/reframe/crop/resize/shake is visible, say that in negative_observations."
  ],
  "inspection_window": {
    "boundary_frame": 141,
    "boundary_id": "edit_boundary_0002",
    "boundary_timecode": "00:02:21",
    "end_frame": 195,
    "end_timecode": "00:03:15",
    "start_frame": 135,
    "start_timecode": "00:02:15"
  },
  "media": {
    "duration_timecode": "00:24:54",
    "filename": "instagram-real.MP4",
    "fps": 60.0,
    "resolution": {
      "height": 1920,
      "width": 1080
    }
  },
  "nearby_candidate_beats": [
    {
      "frame": 134,
      "signal_id": "beat_0006",
      "source_signal_ids": [
        "aud_peak_0006",
        "autoshot_candidate_0001",
        "aud_onset_0019"
      ],
      "source_types": [
        "audio_loudness_peak",
        "audio_onset",
        "visual_autoshot_candidate"
      ],
      "timecode": "00:02:14"
    },
    {
      "frame": 150,
      "signal_id": "beat_0007",
      "source_signal_ids": [
        "aud_peak_0007"
      ],
      "source_types": [
        "audio_loudness_peak"
      ],
      "timecode": "00:02:30"
    },
    {
      "frame": 164,
      "signal_id": "beat_0008",
      "source_signal_ids": [
        "aud_onset_0023",
        "aud_peak_0008"
      ],
      "source_types": [
        "audio_loudness_peak",
        "audio_onset"
      ],
      "timecode": "00:02:44"
    },
    {
      "frame": 188,
      "signal_id": "beat_0009",
      "source_signal_ids": [
        "autoshot_cut_0002",
        "vis_diff_0002",
        "vis_scene_0002"
      ],
      "source_types": [
        "visual_autoshot_cut",
        "visual_frame_diff",
        "visual_scene_cut"
      ],
      "timecode": "00:03:08"
    }
  ],
  "nearby_prosody_segments": [
    {
      "delivery_tags": [
        "very_fast_speech",
        "high_relative_speech_rate",
        "low_relative_pitch",
        "high_relative_pitch_range"
      ],
      "end_frame": 234,
      "end_timecode": "00:03:54",
      "segment_id": "seg_0002",
      "signal_id": "prosody_seg_0002",
      "start_frame": 111,
      "start_timecode": "00:01:51",
      "text": "They open it, type what they want, and hope for the best.",
      "wpm": 352.595
    }
  ],
  "nearby_words": [
    {
      "end_frame": 133,
      "end_timecode": "00:02:13",
      "signal_id": "word_0010",
      "start_frame": 122,
      "start_timecode": "00:02:02",
      "word": "open"
    },
    {
      "end_frame": 140,
      "end_timecode": "00:02:20",
      "signal_id": "word_0011",
      "start_frame": 135,
      "start_timecode": "00:02:15",
      "word": "it,"
    },
    {
      "end_frame": 154,
      "end_timecode": "00:02:34",
      "signal_id": "word_0012",
      "start_frame": 145,
      "start_timecode": "00:02:25",
      "word": "type"
    },
    {
      "end_frame": 163,
      "end_timecode": "00:02:43",
      "signal_id": "word_0013",
      "start_frame": 156,
      "start_timecode": "00:02:36",
      "word": "what"
    },
    {
      "end_frame": 171,
      "end_timecode": "00:02:51",
      "signal_id": "word_0014",
      "start_frame": 164,
      "start_timecode": "00:02:44",
      "word": "they"
    },
    {
      "end_frame": 188,
      "end_timecode": "00:03:08",
      "signal_id": "word_0015",
      "start_frame": 175,
      "start_timecode": "00:02:55",
      "word": "want,"
    },
    {
      "end_frame": 196,
      "end_timecode": "00:03:16",
      "signal_id": "word_0016",
      "start_frame": 192,
      "start_timecode": "00:03:12",
      "word": "and"
    },
    {
      "end_frame": 205,
      "end_timecode": "00:03:25",
      "signal_id": "word_0017",
      "start_frame": 198,
      "start_timecode": "00:03:18",
      "word": "hope"
    },
    {
      "end_frame": 212,
      "end_timecode": "00:03:32",
      "signal_id": "word_0018",
      "start_frame": 206,
      "start_timecode": "00:03:26",
      "word": "for"
    }
  ],
  "purpose": "post_cut_motion_inspection",
  "sync_window": {
    "binding_window_ms": 250,
    "event_signal_id": "edit_boundary_0002",
    "nearest_audio": {
      "kind": "audio_onset",
      "offset_ms": 50.0,
      "signal_id": "aud_onset_0019",
      "strength": 8.587917,
      "timecode": "00:02:24"
    },
    "nearest_word": {
      "offset_ms": -57.0,
      "signal_id": "word_0011",
      "word": "it,"
    },
    "signal_id": "sync_0002",
    "timecode": "00:02:21"
  }
}
```
