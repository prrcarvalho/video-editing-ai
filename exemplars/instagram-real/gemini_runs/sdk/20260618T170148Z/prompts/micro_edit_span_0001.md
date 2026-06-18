# ROLE

You are a high-FPS visual evidence extractor inspecting one short span from the
attached Exemplar video `instagram-real.MP4`.

You are not the creative strategist. Do not explain virality. Do not write a
Viral Pattern, Recreation blueprint, or general advice. Only describe visible
evidence inside the provided span.

# GLOBAL TIMING CONTEXT

# Deterministic Signal Context

Gemini must use these IDs as timing anchors. Do not infer new timing IDs.
WhisperX word rows, WPM/prosody rows, shot spans, cut boundaries, and candidate beats are the source-of-truth constraints.
The edit-mechanics taxonomy is only a label menu for visible evidence inside these deterministic constraints.
`MM:SS:FF` values are Resolve-style frame timecodes, not decimal seconds.
The final field is frames at the media FPS; at 60 FPS, `00:02:21` means 2 seconds + 21 frames.
Do not calculate decimal seconds from these timecodes; downstream tools derive seconds from signal IDs, frames, and FPS.

## Media

{
  "duration": 24.897,
  "duration_timecode": "00:24:54",
  "filename": "instagram-real.MP4",
  "fps": 60.0,
  "frame_count": 1492,
  "resolution": {
    "height": 1920,
    "width": 1080
  }
}

## Speech And Audio Summary

{
  "estimated_audio_tempo_bpm": 112.5,
  "global_prosody_summary": {
    "feature_level": "Functionals",
    "feature_set": "eGeMAPSv02",
    "features": {
      "F0semitoneFrom27.5Hz_sma3nz_amean": 23.863064,
      "F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2": 6.334299,
      "F0semitoneFrom27.5Hz_sma3nz_stddevNorm": 0.233475,
      "jitterLocal_sma3nz_amean": 0.05824,
      "loudnessPeaksPerSec": 5.943775,
      "loudness_sma3_amean": 1.988146,
      "loudness_sma3_pctlrange0-2": 1.802184,
      "loudness_sma3_stddevNorm": 0.518649,
      "shimmerLocaldB_sma3nz_amean": 1.484885
    },
    "scope": "global full-video voice/acoustic functionals, not time-aligned",
    "status": "ok",
    "tool": "opensmile"
  },
  "speech_metrics": {
    "definitions": {
      "bpm": "beats per minute, the dominant rhythmic audio pulse from librosa over the mixed audio",
      "wpm": "words per minute, the speaker/narrator speech rate from WhisperX word timings"
    },
    "overall": {
      "articulation_wpm_word_durations_only": 331.725,
      "media_duration_seconds": 24.897,
      "speech_span_seconds": 24.847,
      "spoken_word_duration_seconds": 19.896,
      "word_count": 110,
      "wpm_first_word_to_last_word": 265.626,
      "wpm_over_media_duration": 265.092
    },
    "pauses": {
      "count": 3,
      "duration_summary": {
        "max": 0.14,
        "mean": 0.127,
        "median": 0.121,
        "min": 0.12,
        "p10": 0.1202,
        "p90": 0.1362
      },
      "min_pause_seconds": 0.12,
      "notable_pauses": [
        {
          "after_word": "results.",
          "after_word_id": "word_0065",
          "before_word": "And",
          "before_word_id": "word_0066",
          "duration": 0.14,
          "end": 14.687,
          "end_timecode": "00:14:41",
          "start": 14.547,
          "start_timecode": "00:14:33"
        },
        {
          "after_word": "creator,",
          "after_word_id": "word_0103",
          "before_word": "and",
          "before_word_id": "word_0104",
          "duration": 0.121,
          "end": 23.597,
          "end_timecode": "00:23:36",
          "start": 23.476,
          "start_timecode": "00:23:29"
        },
        {
          "after_word": "Comment",
          "after_word_id": "word_0102",
          "before_word": "creator,",
          "before_word_id": "word_0103",
          "duration": 0.12,
          "end": 23.056,
          "end_timecode": "00:23:03",
          "start": 22.936,
          "start_timecode": "00:22:56"
        }
      ]
    },
    "segment_rates": [
      {
        "duration": 1.762,
        "end": 1.813,
        "end_timecode": "00:01:49",
        "segment_id": "seg_0001",
        "signal_id": "speech_rate_0001",
        "start": 0.051,
        "start_timecode": "00:00:03",
        "text": "Most people use Claude code the wrong way.",
        "word_count": 8,
        "wpm": 272.418
      },
      {
        "duration": 2.042,
        "end": 3.895,
        "end_timecode": "00:03:54",
        "segment_id": "seg_0002",
        "signal_id": "speech_rate_0002",
        "start": 1.853,
        "start_timecode": "00:01:51",
        "text": "They open it, type what they want, and hope for the best.",
        "word_count": 12,
        "wpm": 352.595
      },
      {
        "duration": 2.223,
        "end": 6.218,
        "end_timecode": "00:06:13",
        "segment_id": "seg_0003",
        "signal_id": "speech_rate_0003",
        "start": 3.995,
        "start_timecode": "00:04:00",
        "text": "But the guy who created Claude code does the opposite.",
        "word_count": 10,
        "wpm": 269.906
      },
      {
        "duration": 2.943,
        "end": 9.241,
        "end_timecode": "00:09:14",
        "segment_id": "seg_0004",
        "signal_id": "speech_rate_0004",
        "start": 6.298,
        "start_timecode": "00:06:18",
        "text": "He says most of his sessions start in plan mode, not build mode.",
        "word_count": 13,
        "wpm": 265.036
      },
      {
        "duration": 2.703,
        "end": 11.964,
        "end_timecode": "00:11:58",
        "segment_id": "seg_0005",
        "signal_id": "speech_rate_0005",
        "start": 9.261,
        "start_timecode": "00:09:16",
        "text": "Slows down first, gets the plan right, then lets Claude execute.",
        "word_count": 11,
        "wpm": 244.173
      },
      {
        "duration": 2.523,
        "end": 14.547,
        "end_timecode": "00:14:33",
        "segment_id": "seg_0006",
        "signal_id": "speech_rate_0006",
        "start": 12.024,
        "start_timecode": "00:12:01",
        "text": "That one shift alone explains why most people get messy results.",
        "word_count": 11,
        "wpm": 261.593
      },
      {
        "duration": 0.52,
        "end": 15.207,
        "end_timecode": "00:15:12",
        "segment_id": "seg_0007",
        "signal_id": "speech_rate_0007",
        "start": 14.687,
        "start_timecode": "00:14:41",
        "text": "And that's not all.",
        "word_count": 4,
        "wpm": 461.538
      },
      {
        "duration": 4.424,
        "end": 19.712,
        "end_timecode": "00:19:43",
        "segment_id": "seg_0008",
        "signal_id": "speech_rate_0008",
        "start": 15.288,
        "start_timecode": "00:15:17",
        "text": "He keeps his Claude file simple, makes Claude check its own work, and runs separate sessions for separate problems.",
        "word_count": 19,
        "wpm": 257.685
      },
      {
        "duration": 2.844,
        "end": 22.636,
        "end_timecode": "00:22:38",
        "segment_id": "seg_0009",
        "signal_id": "speech_rate_0009",
        "start": 19.792,
        "start_timecode": "00:19:48",
        "text": "So he's not just prompting better, he's using Claude code like a system.",
        "word_count": 13,
        "wpm": 274.262
      },
      {
        "duration": 2.222,
        "end": 24.898,
        "end_timecode": "00:24:54",
        "segment_id": "seg_0010",
        "signal_id": "speech_rate_0010",
        "start": 22.676,
        "start_timecode": "00:22:41",
        "text": "Comment creator, and I'll send over the free guide.",
        "word_count": 9,
        "wpm": 243.024
      }
    ],
    "status": "ok",
    "tool": "whisperx_derived"
  }
}

## Word-Level Transcript

These WhisperX rows are the exact spoken-word timing source of truth. Use `word_*` IDs when visible edits, captions, cuts, or motion appear synchronized to speech.

| signal_id | time | frames | score | word |
|---|---:|---:|---:|---|
| word_0001 | 00:00:03-00:00:11 | 3-11 | 0.872 | Most |
| word_0002 | 00:00:13-00:00:27 | 13-27 | 0.774 | people |
| word_0003 | 00:00:32-00:00:39 | 32-39 | 0.726 | use |
| word_0004 | 00:00:42-00:00:57 | 42-57 | 0.82 | Claude |
| word_0005 | 00:01:00-00:01:18 | 60-78 | 0.838 | code |
| word_0006 | 00:01:20-00:01:25 | 80-85 | 0.832 | the |
| word_0007 | 00:01:27-00:01:38 | 87-98 | 0.809 | wrong |
| word_0008 | 00:01:40-00:01:49 | 100-109 | 0.906 | way. |
| word_0009 | 00:01:51-00:01:58 | 111-118 | 0.892 | They |
| word_0010 | 00:02:02-00:02:13 | 122-133 | 0.762 | open |
| word_0011 | 00:02:15-00:02:20 | 135-140 | 0.838 | it, |
| word_0012 | 00:02:25-00:02:34 | 145-154 | 0.728 | type |
| word_0013 | 00:02:36-00:02:43 | 156-163 | 0.742 | what |
| word_0014 | 00:02:44-00:02:51 | 164-171 | 0.789 | they |
| word_0015 | 00:02:55-00:03:08 | 175-188 | 0.907 | want, |
| word_0016 | 00:03:12-00:03:16 | 192-196 | 0.838 | and |
| word_0017 | 00:03:18-00:03:25 | 198-205 | 0.535 | hope |
| word_0018 | 00:03:26-00:03:32 | 206-212 | 0.829 | for |
| word_0019 | 00:03:33-00:03:37 | 213-217 | 0.991 | the |
| word_0020 | 00:03:39-00:03:54 | 219-234 | 0.898 | best. |
| word_0021 | 00:04:00-00:04:06 | 240-246 | 0.832 | But |
| word_0022 | 00:04:07-00:04:13 | 247-253 | 0.804 | the |
| word_0023 | 00:04:15-00:04:27 | 255-267 | 0.955 | guy |
| word_0024 | 00:04:30-00:04:36 | 270-276 | 0.972 | who |
| word_0025 | 00:04:38-00:04:55 | 278-295 | 0.834 | created |
| word_0026 | 00:04:57-00:05:11 | 297-311 | 0.736 | Claude |
| word_0027 | 00:05:13-00:05:31 | 313-331 | 0.845 | code |
| word_0028 | 00:05:35-00:05:44 | 335-344 | 0.674 | does |
| word_0029 | 00:05:45-00:05:50 | 345-350 | 0.835 | the |
| word_0030 | 00:05:54-00:06:13 | 354-373 | 0.97 | opposite. |
| word_0031 | 00:06:18-00:06:23 | 378-383 | 0.883 | He |
| word_0032 | 00:06:25-00:06:36 | 385-396 | 0.71 | says |
| word_0033 | 00:06:39-00:06:50 | 399-410 | 0.676 | most |
| word_0034 | 00:06:51-00:06:55 | 411-415 | 0.75 | of |
| word_0035 | 00:06:58-00:07:02 | 418-422 | 0.841 | his |
| word_0036 | 00:07:04-00:07:26 | 424-446 | 0.82 | sessions |
| word_0037 | 00:07:31-00:07:46 | 451-466 | 0.842 | start |
| word_0038 | 00:07:48-00:07:53 | 468-473 | 0.841 | in |
| word_0039 | 00:07:55-00:08:11 | 475-491 | 0.913 | plan |
| word_0040 | 00:08:12-00:08:25 | 492-505 | 0.976 | mode, |
| word_0041 | 00:08:29-00:08:37 | 509-517 | 0.75 | not |
| word_0042 | 00:08:43-00:08:58 | 523-538 | 0.742 | build |
| word_0043 | 00:09:00-00:09:14 | 540-554 | 0.818 | mode. |
| word_0044 | 00:09:16-00:09:29 | 556-569 | 0.763 | Slows |
| word_0045 | 00:09:31-00:09:41 | 571-581 | 0.936 | down |
| word_0046 | 00:09:43-00:10:00 | 583-600 | 0.805 | first, |
| word_0047 | 00:10:07-00:10:16 | 607-616 | 0.862 | gets |
| word_0048 | 00:10:18-00:10:23 | 618-623 | 0.824 | the |
| word_0049 | 00:10:24-00:10:37 | 624-637 | 0.757 | plan |
| word_0050 | 00:10:41-00:10:54 | 641-654 | 0.893 | right, |
| word_0051 | 00:10:57-00:11:04 | 657-664 | 0.921 | then |
| word_0052 | 00:11:05-00:11:16 | 665-676 | 0.623 | lets |
| word_0053 | 00:11:18-00:11:31 | 678-691 | 0.747 | Claude |
| word_0054 | 00:11:34-00:11:58 | 694-718 | 0.9 | execute. |
| word_0055 | 00:12:01-00:12:10 | 721-730 | 0.776 | That |
| word_0056 | 00:12:15-00:12:21 | 735-741 | 0.855 | one |
| word_0057 | 00:12:22-00:12:35 | 742-755 | 0.773 | shift |
| word_0058 | 00:12:38-00:12:54 | 758-774 | 0.796 | alone |
| word_0059 | 00:12:57-00:13:15 | 777-795 | 0.812 | explains |
| word_0060 | 00:13:17-00:13:23 | 797-803 | 0.963 | why |
| word_0061 | 00:13:27-00:13:35 | 807-815 | 0.8 | most |
| word_0062 | 00:13:36-00:13:48 | 816-828 | 0.762 | people |
| word_0063 | 00:13:50-00:13:56 | 830-836 | 0.864 | get |
| word_0064 | 00:13:58-00:14:11 | 838-851 | 0.948 | messy |
| word_0065 | 00:14:12-00:14:33 | 852-873 | 0.853 | results. |
| word_0066 | 00:14:41-00:14:45 | 881-885 | 0.996 | And |
| word_0067 | 00:14:47-00:14:56 | 887-896 | 0.915 | that's |
| word_0068 | 00:14:57-00:15:03 | 897-903 | 0.82 | not |
| word_0069 | 00:15:05-00:15:12 | 905-912 | 0.877 | all. |
| word_0070 | 00:15:17-00:15:22 | 917-922 | 0.837 | He |
| word_0071 | 00:15:23-00:15:33 | 923-933 | 0.928 | keeps |
| word_0072 | 00:15:35-00:15:40 | 935-940 | 0.837 | his |
| word_0073 | 00:15:42-00:15:56 | 942-956 | 0.756 | Claude |
| word_0074 | 00:15:57-00:16:10 | 957-970 | 0.885 | file |
| word_0075 | 00:16:11-00:16:29 | 971-989 | 0.908 | simple, |
| word_0076 | 00:16:34-00:16:44 | 994-1004 | 0.804 | makes |
| word_0077 | 00:16:46-00:17:01 | 1006-1021 | 0.743 | Claude |
| word_0078 | 00:17:03-00:17:15 | 1023-1035 | 0.881 | check |
| word_0079 | 00:17:17-00:17:22 | 1037-1042 | 0.977 | its |
| word_0080 | 00:17:25-00:17:32 | 1045-1052 | 0.653 | own |
| word_0081 | 00:17:34-00:17:45 | 1054-1065 | 0.93 | work, |
| word_0082 | 00:17:46-00:17:52 | 1066-1072 | 0.687 | and |
| word_0083 | 00:17:55-00:18:05 | 1075-1085 | 0.818 | runs |
| word_0084 | 00:18:09-00:18:25 | 1089-1105 | 0.898 | separate |
| word_0085 | 00:18:27-00:18:47 | 1107-1127 | 0.893 | sessions |
| word_0086 | 00:18:51-00:18:58 | 1131-1138 | 0.84 | for |
| word_0087 | 00:19:01-00:19:18 | 1141-1158 | 0.851 | separate |
| word_0088 | 00:19:19-00:19:43 | 1159-1183 | 0.839 | problems. |
| word_0089 | 00:19:48-00:19:54 | 1188-1194 | 0.84 | So |
| word_0090 | 00:19:55-00:20:03 | 1195-1203 | 0.723 | he's |
| word_0091 | 00:20:06-00:20:13 | 1206-1213 | 0.786 | not |
| word_0092 | 00:20:14-00:20:21 | 1214-1221 | 0.798 | just |
| word_0093 | 00:20:24-00:20:43 | 1224-1243 | 0.808 | prompting |
| word_0094 | 00:20:45-00:21:00 | 1245-1260 | 0.938 | better, |
| word_0095 | 00:21:06-00:21:13 | 1266-1273 | 0.805 | he's |
| word_0096 | 00:21:16-00:21:27 | 1276-1287 | 0.908 | using |
| word_0097 | 00:21:28-00:21:43 | 1288-1303 | 0.746 | Claude |
| word_0098 | 00:21:45-00:22:00 | 1305-1320 | 0.976 | code |
| word_0099 | 00:22:02-00:22:09 | 1322-1329 | 0.829 | like |
| word_0100 | 00:22:12-00:22:14 | 1332-1334 | 0.502 | a |
| word_0101 | 00:22:18-00:22:38 | 1338-1358 | 0.877 | system. |
| word_0102 | 00:22:41-00:22:56 | 1361-1376 | 0.932 | Comment |
| word_0103 | 00:23:03-00:23:29 | 1383-1409 | 0.84 | creator, |
| word_0104 | 00:23:36-00:23:41 | 1416-1421 | 0.9 | and |
| word_0105 | 00:23:43-00:23:51 | 1423-1431 | 0.816 | I'll |
| word_0106 | 00:23:53-00:24:05 | 1433-1445 | 0.684 | send |
| word_0107 | 00:24:08-00:24:18 | 1448-1458 | 0.847 | over |
| word_0108 | 00:24:20-00:24:24 | 1460-1464 | 0.99 | the |
| word_0109 | 00:24:27-00:24:39 | 1467-1479 | 0.707 | free |
| word_0110 | 00:24:41-00:24:54 | 1481-1494 | 0.527 | guide. |

## Prosody Segments

These rows are transcript-segment-level voice delivery signals. Use them only to check visual/audio synchronization, not to explain virality.

| signal_id | segment_id | time | frames | WPM | tags | pitch_mean | pitch_range | loudness_mean | loudness_range | text |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|
| prosody_seg_0001 | seg_0001 | 00:00:03-00:01:49 | 3-109 | 272.418 | fast_speech, low_relative_pitch, high_relative_pitch_range | 22.593464 | 11.374205 | 1.976617 | 1.733409 | Most people use Claude code the wrong way. |
| prosody_seg_0002 | seg_0002 | 00:01:51-00:03:54 | 111-234 | 352.595 | very_fast_speech, high_relative_speech_rate, low_relative_pitch, high_relative_pitch_range | 19.721867 | 8.397023 | 1.979484 | 1.72899 | They open it, type what they want, and hope for the best. |
| prosody_seg_0003 | seg_0003 | 00:04:00-00:06:13 | 240-373 | 269.906 | fast_speech, high_relative_pitch, low_relative_loudness, high_relative_loudness_range | 24.484482 | 5.979692 | 1.870291 | 2.092583 | But the guy who created Claude code does the opposite. |
| prosody_seg_0004 | seg_0004 | 00:06:18-00:09:14 | 378-554 | 265.036 | fast_speech, low_relative_pitch_range, low_relative_loudness | 23.626446 | 4.930212 | 1.948928 | 1.677741 | He says most of his sessions start in plan mode, not build mode. |
| prosody_seg_0005 | seg_0005 | 00:09:16-00:11:58 | 556-718 | 244.173 | low_relative_speech_rate, low_relative_pitch_range, low_relative_loudness, high_relative_loudness_range | 23.435558 | 4.722115 | 1.922656 | 2.081059 | Slows down first, gets the plan right, then lets Claude execute. |
| prosody_seg_0006 | seg_0006 | 00:12:01-00:14:33 | 721-873 | 261.593 | fast_speech, high_relative_pitch, high_relative_loudness, low_relative_loudness_range | 24.091484 | 5.318092 | 2.049378 | 1.674982 | That one shift alone explains why most people get messy results. |
| prosody_seg_0007 | seg_0007 | 00:14:41-00:15:12 | 881-912 | 461.538 | very_fast_speech, high_relative_speech_rate, low_relative_pitch | 22.359394 | 5.953016 | 1.966895 | 1.687174 | And that's not all. |
| prosody_seg_0008 | seg_0008 | 00:15:17-00:19:43 | 917-1183 | 257.685 | fast_speech, low_relative_speech_rate, high_relative_pitch_range, low_relative_loudness_range | 23.410107 | 7.359701 | 2.016428 | 1.650832 | He keeps his Claude file simple, makes Claude check its own work, and runs separate sessions for separate problems. |
| prosody_seg_0009 | seg_0009 | 00:19:48-00:22:38 | 1188-1358 | 274.262 | fast_speech, high_relative_speech_rate, low_relative_pitch_range, high_relative_loudness, low_relative_loudness_range | 23.897676 | 4.33617 | 2.071107 | 1.600765 | So he's not just prompting better, he's using Claude code like a system. |
| prosody_seg_0010 | seg_0010 | 00:22:41-00:24:54 | 1361-1494 | 243.024 | low_relative_speech_rate, high_relative_pitch, high_relative_loudness, high_relative_loudness_range | 27.35873 | 6.424967 | 2.342706 | 1.850657 | Comment creator, and I'll send over the free guide. |

## Shot Boundaries

| signal_id | kind | timecode | frame | confidence | needs_review | source_signal_ids |
|---|---|---:|---:|---:|---|---|
| edit_boundary_0001 | hard_cut_with_detector_agreement | 00:01:51 | 111 | 0.95 | False | autoshot_cut_0001, vis_diff_0001, vis_scene_0001 |
| edit_boundary_0002 | candidate_cut_review | 00:02:21 | 141 | 0.45 | True | autoshot_candidate_0001 |
| edit_boundary_0003 | hard_cut_with_detector_agreement | 00:03:09 | 189 | 0.95 | False | autoshot_cut_0002, vis_diff_0002, vis_scene_0002 |
| edit_boundary_0004 | hard_cut_with_detector_agreement | 00:03:58 | 238 | 0.95 | False | autoshot_cut_0003, vis_diff_0003, vis_scene_0003 |
| edit_boundary_0005 | hard_cut_with_detector_agreement | 00:05:33 | 333 | 0.95 | False | autoshot_cut_0004, vis_diff_0004, vis_scene_0004 |
| edit_boundary_0006 | hard_cut_with_detector_agreement | 00:06:16 | 376 | 0.95 | False | autoshot_cut_0005, vis_diff_0005, vis_scene_0005 |
| edit_boundary_0007 | hard_cut_with_detector_agreement | 00:07:25 | 445 | 0.95 | False | autoshot_cut_0006, vis_scene_0006 |
| edit_boundary_0008 | hard_cut_with_detector_agreement | 00:08:25 | 505 | 0.95 | False | autoshot_cut_0007, vis_diff_0006, vis_scene_0007 |
| edit_boundary_0009 | hard_cut_with_detector_agreement | 00:09:12 | 552 | 0.95 | False | autoshot_cut_0008, vis_diff_0007, vis_scene_0008 |
| edit_boundary_0010 | hard_cut_with_detector_agreement | 00:10:55 | 655 | 0.95 | False | autoshot_cut_0009, vis_diff_0008, vis_scene_0009 |
| edit_boundary_0011 | hard_cut_with_detector_agreement | 00:12:00 | 720 | 0.95 | False | autoshot_cut_0010, vis_diff_0009, vis_scene_0010 |
| edit_boundary_0012 | hard_cut_with_detector_agreement | 00:13:15 | 795 | 0.95 | False | autoshot_cut_0011, vis_diff_0010, vis_scene_0011 |
| edit_boundary_0013 | hard_cut_with_detector_agreement | 00:14:39 | 879 | 0.95 | False | autoshot_cut_0012, vis_diff_0011, vis_scene_0012 |
| edit_boundary_0014 | hard_cut_with_detector_agreement | 00:15:15 | 915 | 0.95 | False | autoshot_cut_0013, vis_diff_0012, vis_scene_0013 |
| edit_boundary_0015 | hard_cut_with_detector_agreement | 00:16:31 | 991 | 0.95 | False | autoshot_cut_0014, vis_diff_0013, vis_scene_0014 |
| edit_boundary_0016 | hard_cut_with_detector_agreement | 00:17:43 | 1063 | 0.95 | False | autoshot_cut_0015, vis_diff_0014, vis_scene_0015 |
| edit_boundary_0017 | hard_cut_with_detector_agreement | 00:19:44 | 1184 | 0.95 | False | autoshot_cut_0016, vis_diff_0015, vis_scene_0016 |
| edit_boundary_0018 | hard_cut_with_detector_agreement | 00:21:04 | 1264 | 0.95 | False | autoshot_cut_0017, vis_diff_0016, vis_scene_0017 |
| edit_boundary_0021 | hard_cut_with_detector_agreement | 00:22:37 | 1357 | 0.95 | False | autoshot_cut_0018, vis_diff_0019, vis_scene_0018 |

## Shot Spans

| signal_id | start | end | frames | duration | boundary_ids |
|---|---:|---:|---|---:|---|
| edit_span_0001 | 00:00:00 | 00:01:51 | 0-111 | 1.8438 | media_start -> edit_boundary_0001 |
| edit_span_0002 | 00:01:51 | 00:02:21 | 111-141 | 0.5062 | edit_boundary_0001 -> edit_boundary_0002 |
| edit_span_0003 | 00:02:21 | 00:03:09 | 141-189 | 0.7938 | edit_boundary_0002 -> edit_boundary_0003 |
| edit_span_0004 | 00:03:09 | 00:03:58 | 189-238 | 0.8167 | edit_boundary_0003 -> edit_boundary_0004 |
| edit_span_0005 | 00:03:58 | 00:05:33 | 238-333 | 1.5833 | edit_boundary_0004 -> edit_boundary_0005 |
| edit_span_0006 | 00:05:33 | 00:06:16 | 333-376 | 0.7167 | edit_boundary_0005 -> edit_boundary_0006 |
| edit_span_0007 | 00:06:16 | 00:07:25 | 376-445 | 1.1479 | edit_boundary_0006 -> edit_boundary_0007 |
| edit_span_0008 | 00:07:25 | 00:08:25 | 445-505 | 1.0021 | edit_boundary_0007 -> edit_boundary_0008 |
| edit_span_0009 | 00:08:25 | 00:09:12 | 505-552 | 0.7833 | edit_boundary_0008 -> edit_boundary_0009 |
| edit_span_0010 | 00:09:12 | 00:10:55 | 552-655 | 1.7167 | edit_boundary_0009 -> edit_boundary_0010 |
| edit_span_0011 | 00:10:55 | 00:12:00 | 655-720 | 1.0833 | edit_boundary_0010 -> edit_boundary_0011 |
| edit_span_0012 | 00:12:00 | 00:13:15 | 720-795 | 1.25 | edit_boundary_0011 -> edit_boundary_0012 |
| edit_span_0013 | 00:13:15 | 00:14:39 | 795-879 | 1.4 | edit_boundary_0012 -> edit_boundary_0013 |
| edit_span_0014 | 00:14:39 | 00:15:15 | 879-915 | 0.6 | edit_boundary_0013 -> edit_boundary_0014 |
| edit_span_0015 | 00:15:15 | 00:16:31 | 915-991 | 1.2667 | edit_boundary_0014 -> edit_boundary_0015 |
| edit_span_0016 | 00:16:31 | 00:17:43 | 991-1063 | 1.2 | edit_boundary_0015 -> edit_boundary_0016 |
| edit_span_0017 | 00:17:43 | 00:19:44 | 1063-1184 | 2.0167 | edit_boundary_0016 -> edit_boundary_0017 |
| edit_span_0018 | 00:19:44 | 00:21:04 | 1184-1264 | 1.3333 | edit_boundary_0017 -> edit_boundary_0018 |
| edit_span_0019 | 00:21:04 | 00:22:37 | 1264-1357 | 1.55 | edit_boundary_0018 -> edit_boundary_0021 |
| edit_span_0020 | 00:22:37 | 00:24:54 | 1357-1494 | 2.2865 | edit_boundary_0021 -> media_end |

## Candidate Beats

| signal_id | timecode | frame | source_types | source_signal_ids |
|---|---:|---:|---|---|
| beat_0001 | 00:00:00 | 0 | audio_loudness_peak, audio_onset, boundary, first_word, transcript_segment_start | media_start, aud_onset_0001, seg_0001, word_0001, aud_onset_0002, aud_peak_0001 |
| beat_0002 | 00:00:24 | 24 | audio_loudness_peak | aud_peak_0002 |
| beat_0003 | 00:00:49 | 49 | audio_loudness_peak | aud_peak_0003 |
| beat_0004 | 00:01:20 | 80 | audio_loudness_peak | aud_peak_0004 |
| beat_0005 | 00:01:50 | 110 | audio_loudness_peak, audio_onset, transcript_segment_start, visual_autoshot_cut, visual_frame_diff, visual_scene_cut | autoshot_cut_0001, vis_diff_0001, vis_scene_0001, seg_0002, aud_onset_0014, aud_peak_0005 |
| beat_0006 | 00:02:14 | 134 | audio_loudness_peak, audio_onset, visual_autoshot_candidate | aud_peak_0006, autoshot_candidate_0001, aud_onset_0019 |
| beat_0007 | 00:02:30 | 150 | audio_loudness_peak | aud_peak_0007 |
| beat_0008 | 00:02:44 | 164 | audio_loudness_peak, audio_onset | aud_onset_0023, aud_peak_0008 |
| beat_0009 | 00:03:08 | 188 | visual_autoshot_cut, visual_frame_diff, visual_scene_cut | autoshot_cut_0002, vis_diff_0002, vis_scene_0002 |
| beat_0010 | 00:03:57 | 237 | audio_onset, transcript_segment_start, visual_autoshot_cut, visual_frame_diff, visual_scene_cut | autoshot_cut_0003, vis_diff_0003, vis_scene_0003, seg_0003, aud_onset_0034, aud_onset_0035 |
| beat_0011 | 00:04:16 | 256 | audio_loudness_peak, audio_onset | aud_onset_0036, aud_peak_0009 |
| beat_0012 | 00:04:37 | 277 | audio_onset | aud_onset_0038 |
| beat_0013 | 00:05:13 | 313 | audio_loudness_peak, audio_onset | aud_onset_0043, aud_peak_0010 |
| beat_0014 | 00:05:32 | 332 | visual_autoshot_cut, visual_frame_diff, visual_scene_cut | autoshot_cut_0004, vis_diff_0004, vis_scene_0004 |
| beat_0015 | 00:06:00 | 360 | audio_onset | aud_onset_0051 |
| beat_0016 | 00:06:14 | 374 | audio_onset, transcript_segment_start, visual_autoshot_cut, visual_frame_diff, visual_scene_cut | aud_onset_0054, autoshot_cut_0005, vis_diff_0005, vis_scene_0005, seg_0004, aud_onset_0055 |
| beat_0017 | 00:06:30 | 390 | audio_loudness_peak | aud_peak_0011 |
| beat_0018 | 00:06:42 | 402 | audio_loudness_peak | aud_peak_0012 |
| beat_0019 | 00:07:24 | 444 | visual_autoshot_cut, visual_scene_cut | autoshot_cut_0006, vis_scene_0006 |
| beat_0020 | 00:07:39 | 459 | audio_loudness_peak | aud_peak_0013 |
| beat_0021 | 00:07:56 | 476 | audio_onset | aud_onset_0068 |
| beat_0022 | 00:08:24 | 504 | audio_onset, visual_autoshot_cut, visual_frame_diff, visual_scene_cut | autoshot_cut_0007, vis_diff_0006, vis_scene_0007, aud_onset_0072 |
| beat_0023 | 00:08:47 | 527 | audio_loudness_peak | aud_peak_0014 |
| beat_0024 | 00:09:11 | 551 | audio_onset, transcript_segment_start, visual_autoshot_cut, visual_frame_diff, visual_scene_cut | autoshot_cut_0008, vis_diff_0007, vis_scene_0008, aud_onset_0076, seg_0005 |
| beat_0025 | 00:09:22 | 562 | audio_loudness_peak | aud_peak_0015 |
| beat_0026 | 00:09:33 | 573 | audio_loudness_peak | aud_peak_0016 |
| beat_0027 | 00:10:24 | 624 | audio_onset | aud_onset_0087 |
| beat_0028 | 00:10:54 | 654 | audio_onset, visual_autoshot_cut, visual_frame_diff, visual_scene_cut | autoshot_cut_0009, vis_diff_0008, vis_scene_0009, aud_onset_0090 |
| beat_0029 | 00:11:22 | 682 | audio_onset | aud_onset_0094 |
| beat_0030 | 00:11:37 | 697 | audio_onset | aud_onset_0096, aud_onset_0097 |
| beat_0031 | 00:11:58 | 718 | audio_loudness_peak, audio_onset, transcript_segment_start, visual_autoshot_cut, visual_frame_diff, visual_scene_cut | aud_onset_0098, autoshot_cut_0010, vis_diff_0009, vis_scene_0010, seg_0006, aud_onset_0099, aud_peak_0017 |
| beat_0032 | 00:12:15 | 735 | audio_loudness_peak | aud_peak_0018 |
| beat_0033 | 00:12:42 | 762 | audio_loudness_peak, audio_onset | aud_onset_0104, aud_peak_0019 |
| beat_0034 | 00:12:59 | 779 | audio_onset | aud_onset_0106, aud_onset_0107 |
| beat_0035 | 00:13:14 | 794 | visual_autoshot_cut, visual_frame_diff, visual_scene_cut | autoshot_cut_0011, vis_diff_0010, vis_scene_0011 |
| beat_0036 | 00:14:30 | 870 | audio_onset, visual_autoshot_cut, visual_frame_diff, visual_scene_cut | aud_onset_0120, autoshot_cut_0012, vis_diff_0011, vis_scene_0012 |
| beat_0037 | 00:14:41 | 881 | transcript_segment_start | seg_0007 |
| beat_0038 | 00:15:14 | 914 | audio_onset, transcript_segment_start, visual_autoshot_cut, visual_frame_diff, visual_scene_cut | autoshot_cut_0013, vis_diff_0012, vis_scene_0013, aud_onset_0126, seg_0008, aud_onset_0127 |
| beat_0039 | 00:15:26 | 926 | audio_loudness_peak | aud_peak_0020 |
| beat_0040 | 00:15:42 | 942 | audio_loudness_peak, audio_onset | aud_onset_0129, aud_onset_0130, aud_peak_0021 |
| beat_0041 | 00:16:01 | 961 | audio_loudness_peak | aud_peak_0022 |
| beat_0042 | 00:16:14 | 974 | audio_onset | aud_onset_0134 |
| beat_0043 | 00:16:30 | 990 | audio_onset, visual_autoshot_cut, visual_frame_diff, visual_scene_cut | autoshot_cut_0014, vis_diff_0013, vis_scene_0014, aud_onset_0136 |
| beat_0044 | 00:16:50 | 1010 | audio_loudness_peak, audio_onset | aud_onset_0139, aud_peak_0023 |
| beat_0045 | 00:17:07 | 1027 | audio_loudness_peak, audio_onset | aud_onset_0141, aud_peak_0024, aud_onset_0142 |
| beat_0046 | 00:17:42 | 1062 | visual_autoshot_cut, visual_frame_diff, visual_scene_cut | autoshot_cut_0015, vis_diff_0014, vis_scene_0015 |
| beat_0047 | 00:17:56 | 1076 | audio_loudness_peak, audio_onset | aud_peak_0025, aud_onset_0149 |
| beat_0048 | 00:18:11 | 1091 | audio_loudness_peak, audio_onset | aud_onset_0150, aud_peak_0026 |
| beat_0049 | 00:18:30 | 1110 | audio_loudness_peak | aud_peak_0027 |
| beat_0050 | 00:19:40 | 1180 | audio_onset, transcript_segment_start, visual_autoshot_cut, visual_frame_diff, visual_scene_cut | aud_onset_0164, autoshot_cut_0016, vis_diff_0015, vis_scene_0016, seg_0009 |
| beat_0051 | 00:20:04 | 1204 | audio_loudness_peak, audio_onset | aud_onset_0168, aud_peak_0028 |
| beat_0052 | 00:20:26 | 1226 | audio_loudness_peak, audio_onset | aud_onset_0171, aud_peak_0029 |
| beat_0053 | 00:20:45 | 1245 | audio_onset | aud_onset_0173 |
| beat_0054 | 00:21:03 | 1263 | visual_autoshot_cut, visual_frame_diff, visual_scene_cut | autoshot_cut_0017, vis_diff_0016, vis_scene_0017 |
| beat_0055 | 00:21:34 | 1294 | audio_loudness_peak, audio_onset | aud_peak_0030, aud_onset_0181 |
| beat_0056 | 00:22:04 | 1324 | visual_frame_diff | vis_diff_0017 |
| beat_0057 | 00:22:25 | 1345 | visual_frame_diff | vis_diff_0018 |
| beat_0058 | 00:22:36 | 1356 | transcript_segment_start, visual_autoshot_cut, visual_frame_diff, visual_scene_cut | autoshot_cut_0018, vis_diff_0019, vis_scene_0018, seg_0010 |
| beat_0059 | 00:22:59 | 1379 | audio_onset | aud_onset_0193 |
| beat_0060 | 00:23:13 | 1393 | audio_loudness_peak | aud_peak_0031 |
| beat_0061 | 00:24:04 | 1444 | audio_loudness_peak, audio_onset | aud_onset_0200, aud_peak_0032 |

# SPAN TO INSPECT

{
  "nearby_candidate_beats": [
    {
      "frame": 0,
      "signal_id": "beat_0001",
      "source_signal_ids": [
        "media_start",
        "aud_onset_0001",
        "seg_0001",
        "word_0001",
        "aud_onset_0002",
        "aud_peak_0001"
      ],
      "source_types": [
        "audio_loudness_peak",
        "audio_onset",
        "boundary",
        "first_word",
        "transcript_segment_start"
      ],
      "time": 0.0,
      "timecode": "00:00:00"
    },
    {
      "frame": 24,
      "signal_id": "beat_0002",
      "source_signal_ids": [
        "aud_peak_0002"
      ],
      "source_types": [
        "audio_loudness_peak"
      ],
      "time": 0.4,
      "timecode": "00:00:24"
    },
    {
      "frame": 49,
      "signal_id": "beat_0003",
      "source_signal_ids": [
        "aud_peak_0003"
      ],
      "source_types": [
        "audio_loudness_peak"
      ],
      "time": 0.8167,
      "timecode": "00:00:49"
    },
    {
      "frame": 80,
      "signal_id": "beat_0004",
      "source_signal_ids": [
        "aud_peak_0004"
      ],
      "source_types": [
        "audio_loudness_peak"
      ],
      "time": 1.3333,
      "timecode": "00:01:20"
    },
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
      "time": 1.8333,
      "timecode": "00:01:50"
    }
  ],
  "nearby_prosody_segments": [
    {
      "delivery_tags": [
        "fast_speech",
        "low_relative_pitch",
        "high_relative_pitch_range"
      ],
      "end": 1.813,
      "end_frame": 109,
      "end_timecode": "00:01:49",
      "features": {
        "loudness_mean": 1.976617,
        "loudness_peaks_per_sec": 6.285714,
        "loudness_range": 1.733409,
        "pitch_mean": 22.593464,
        "pitch_range": 11.374205
      },
      "relative_delivery": {
        "loudness": "mid",
        "loudness_range": "mid",
        "pitch": "low",
        "pitch_range": "high",
        "speech_rate": "mid"
      },
      "segment_id": "seg_0001",
      "signal_id": "prosody_seg_0001",
      "start": 0.051,
      "start_frame": 3,
      "start_timecode": "00:00:03",
      "text": "Most people use Claude code the wrong way.",
      "word_count": 8,
      "wpm": 272.418
    },
    {
      "delivery_tags": [
        "very_fast_speech",
        "high_relative_speech_rate",
        "low_relative_pitch",
        "high_relative_pitch_range"
      ],
      "end": 3.895,
      "end_frame": 234,
      "end_timecode": "00:03:54",
      "features": {
        "loudness_mean": 1.979484,
        "loudness_peaks_per_sec": 6.896552,
        "loudness_range": 1.72899,
        "pitch_mean": 19.721867,
        "pitch_range": 8.397023
      },
      "relative_delivery": {
        "loudness": "mid",
        "loudness_range": "mid",
        "pitch": "low",
        "pitch_range": "high",
        "speech_rate": "high"
      },
      "segment_id": "seg_0002",
      "signal_id": "prosody_seg_0002",
      "start": 1.853,
      "start_frame": 111,
      "start_timecode": "00:01:51",
      "text": "They open it, type what they want, and hope for the best.",
      "word_count": 12,
      "wpm": 352.595
    }
  ],
  "nearby_words": [
    {
      "end": 0.191,
      "end_frame": 11,
      "end_timecode": "00:00:11",
      "score": 0.872,
      "signal_id": "word_0001",
      "start": 0.051,
      "start_frame": 3,
      "start_timecode": "00:00:03",
      "word": "Most"
    },
    {
      "end": 0.451,
      "end_frame": 27,
      "end_timecode": "00:00:27",
      "score": 0.774,
      "signal_id": "word_0002",
      "start": 0.211,
      "start_frame": 13,
      "start_timecode": "00:00:13",
      "word": "people"
    },
    {
      "end": 0.652,
      "end_frame": 39,
      "end_timecode": "00:00:39",
      "score": 0.726,
      "signal_id": "word_0003",
      "start": 0.532,
      "start_frame": 32,
      "start_timecode": "00:00:32",
      "word": "use"
    },
    {
      "end": 0.952,
      "end_frame": 57,
      "end_timecode": "00:00:57",
      "score": 0.82,
      "signal_id": "word_0004",
      "start": 0.692,
      "start_frame": 42,
      "start_timecode": "00:00:42",
      "word": "Claude"
    },
    {
      "end": 1.292,
      "end_frame": 78,
      "end_timecode": "00:01:18",
      "score": 0.838,
      "signal_id": "word_0005",
      "start": 0.992,
      "start_frame": 60,
      "start_timecode": "00:01:00",
      "word": "code"
    },
    {
      "end": 1.412,
      "end_frame": 85,
      "end_timecode": "00:01:25",
      "score": 0.832,
      "signal_id": "word_0006",
      "start": 1.332,
      "start_frame": 80,
      "start_timecode": "00:01:20",
      "word": "the"
    },
    {
      "end": 1.633,
      "end_frame": 98,
      "end_timecode": "00:01:38",
      "score": 0.809,
      "signal_id": "word_0007",
      "start": 1.453,
      "start_frame": 87,
      "start_timecode": "00:01:27",
      "word": "wrong"
    },
    {
      "end": 1.813,
      "end_frame": 109,
      "end_timecode": "00:01:49",
      "score": 0.906,
      "signal_id": "word_0008",
      "start": 1.673,
      "start_frame": 100,
      "start_timecode": "00:01:40",
      "word": "way."
    },
    {
      "end": 1.973,
      "end_frame": 118,
      "end_timecode": "00:01:58",
      "score": 0.892,
      "signal_id": "word_0009",
      "start": 1.853,
      "start_frame": 111,
      "start_timecode": "00:01:51",
      "word": "They"
    },
    {
      "end": 2.213,
      "end_frame": 133,
      "end_timecode": "00:02:13",
      "score": 0.762,
      "signal_id": "word_0010",
      "start": 2.033,
      "start_frame": 122,
      "start_timecode": "00:02:02",
      "word": "open"
    }
  ],
  "span": {
    "duration": 1.8438,
    "end": 1.8438,
    "end_boundary_confidence": 0.95,
    "end_boundary_id": "edit_boundary_0001",
    "end_boundary_kind": "hard_cut_with_detector_agreement",
    "end_frame": 111,
    "end_timecode": "00:01:51",
    "signal_id": "edit_span_0001",
    "start": 0.0,
    "start_boundary_id": "media_start",
    "start_frame": 0,
    "start_timecode": "00:00:00"
  }
}

# TASK

Grounding contract:

- The deterministic context is the source of truth for exact spoken words,
  word timings, speech pace/WPM, prosody segments, candidate beats, audio
  onsets, hard cuts, candidate cuts, shot spans, frames, and timecodes.
- The edit-mechanics taxonomy is only a controlled vocabulary for classifying
  what you visibly observe inside the supplied span.
- Do not create new transcript words, new cut boundaries, new shot spans, or
  new timing anchors.
- Every layout row and craft event must cite supplied IDs in
  `anchor_signal_ids` and grouped `grounding_constraints`.
- If a visible mechanic seems to happen between supplied anchors, bind it to
  the nearest supplied span/word/beat/prosody/cut IDs and set
  `needs_review: true` when the timing cannot be verified from the signals.
- For shot-boundary claims, cite `edit_span_*`, `edit_boundary_*`, or `sync_*`
  IDs. For speech/caption/prosody sync, cite `word_*` and/or
  `prosody_seg_*` IDs. For beat/audio sync, cite `beat_*`, `sync_*`, or audio
  signal IDs when supplied.

Inspect only this span. Report the exact visible mechanics that a future Codex
reasoning stage and video editor would need as evidence:

- layout/layer stack: talking head, facecam, screen recording, split screen,
  picture-in-picture, UI demo, b-roll, graphic cards, captions, callouts,
  progress bars, stickers, background plates;
- cut/transition rhythm near the span edges: hard cut, candidate cut, jump cut,
  match cut, cut on action, smash cut, whip-pan cut, false cut, layout-only
  cut, overlay-only cut, dissolve, dip, wipe, slide, zoom, morph, glitch, or
  flash transition;
- framing and keyframed motion within the span: punch-in, punch-out, slow push,
  pull-out, zoom ramp, digital zoom, crop shift, reframe, resize, rotation, pan,
  tilt, shake, stabilization snap, parallax, object/face tracking;
- speed/time effects: speed ramp, slow motion, freeze frame, frame hold,
  timelapse, time remap, stutter cut, repeated frames, reversed motion;
- captions/text: full captions, keyword captions, word-by-word captions,
  active-word highlight, karaoke state, caption pop/slide/bounce, color
  emphasis, size pop, title card, lower third, text hook, callout, counter,
  progress bar;
- overlays/graphics: arrows, circles, boxes, stickers, emoji/icons, image
  overlays, b-roll inserts, diagrams, background replacement, border frames,
  split-screen or picture-in-picture changes;
- screen/UI behavior: cursor motion, click/tap indicator, pointer highlight,
  selection highlight, typing indicator, text-field focus, scroll, swipe, drag,
  hover state, menu open, modal popup, app/browser state change;
- VFX/color/light: blur, motion blur, glow, flash, lens flare, light leak,
  color punch, grade shift, exposure pulse, vignette, mask reveal, track matte,
  rotoscope mask, green-screen composite, glitch, chromatic aberration, grain,
  depth-of-field shift, focus pull;
- audio-visible sync: visible edit landing near a deterministic word, beat,
  onset, SFX hit, whoosh, riser, silence/drop, bass drop, voice emphasis, or
  `prosody_seg_*` anchor.

The SDK response schema contains the allowed enum values; choose the closest
allowed value instead of inventing new labels.

Use only anchor IDs from the supplied context. If the span is too blurry,
sampled too sparsely, or ambiguous, mark `needs_review: true`.
Voice/prosody context is supplied only to help identify visible edit-sync moments.
Do not turn prosody into virality reasoning or strategy.

Controlled hypothesis rule:

- Use `craft_function_hypothesis` only as a small craft-purpose label for the
  visible mechanism, not as a virality explanation.
- Use `hypothesis_basis: visible_only` when the claim is directly visible.
- Use `hypothesis_basis: visible_plus_audio_signal` when the visible action is
  tied to supplied beat/audio/prosody IDs.
- Use `hypothesis_basis: weak_inference` and `needs_review: true` when the
  purpose is plausible but not directly clear.
- A taxonomy label without a cited deterministic anchor is not valid evidence.

Timing rules:

- `MM:SS:FF` means Resolve-style frame timecode, not decimal seconds.
- The final field is frames at the media FPS. At 60 FPS, `00:02:21` means
  2 seconds + 21 frames, not 2.21 seconds.
- Do not calculate or emit decimal seconds.
- Anchor timing with `time_range` and `anchor_signal_ids`; downstream tools will
  derive seconds from the cited signal IDs, frames, and media FPS.

# OUTPUT

Return valid JSON only, conforming to the SDK response schema. Do not wrap it
in markdown. The local tool will turn your JSON into `analysis.md` for human
inspection.
