import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "gemini_sdk_video.py"
SPEC = importlib.util.spec_from_file_location("gemini_sdk_video", MODULE_PATH)
gemini_sdk_video = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(gemini_sdk_video)


class PostCutMotionContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.signals_dir = Path(self.tmp.name)
        self._write(
            "media.json",
            {
                "filename": "example.mp4",
                "duration": 5.0,
                "duration_timecode": "00:05:00",
                "fps": 60.0,
                "resolution": {"width": 1080, "height": 1920},
            },
        )
        self._write(
            "edit_mechanisms.json",
            {
                "boundary_mechanisms": [
                    {
                        "signal_id": "edit_boundary_0001",
                        "event_kind": "hard_cut_with_detector_agreement",
                        "time": 1.0,
                        "timecode": "00:01:00",
                        "frame": 60,
                        "confidence": 0.95,
                        "needs_review": False,
                        "source_signal_ids": ["vis_scene_0001"],
                        "sync_signal_ids": ["sync_0001"],
                    },
                    {
                        "signal_id": "edit_boundary_0002",
                        "event_kind": "candidate_cut_review",
                        "time": 2.0,
                        "timecode": "00:02:00",
                        "frame": 120,
                        "confidence": 0.45,
                        "needs_review": True,
                        "source_signal_ids": ["autoshot_candidate_0001"],
                        "sync_signal_ids": ["sync_0002"],
                    },
                ],
                "shot_spans": [
                    {
                        "signal_id": "edit_span_0001",
                        "start": 0.0,
                        "end": 1.0,
                        "duration": 1.0,
                        "start_boundary_id": None,
                        "end_boundary_id": "edit_boundary_0001",
                    },
                    {
                        "signal_id": "edit_span_0002",
                        "start": 1.0,
                        "end": 2.0,
                        "duration": 1.0,
                        "start_boundary_id": "edit_boundary_0001",
                        "end_boundary_id": "edit_boundary_0002",
                    },
                ],
                "sync_windows": [
                    {
                        "signal_id": "sync_0001",
                        "event_signal_id": "edit_boundary_0001",
                        "nearest_word": {"signal_id": "word_0001", "word": "cut"},
                    }
                ],
            },
        )
        self._write(
            "transcript.words.json",
            {
                "words": [
                    {
                        "signal_id": "word_0001",
                        "word": "cut",
                        "start": 0.95,
                        "end": 1.08,
                        "start_timecode": "00:00:57",
                        "end_timecode": "00:01:05",
                    },
                    {
                        "signal_id": "word_far",
                        "word": "far",
                        "start": 4.0,
                        "end": 4.2,
                    },
                ]
            },
        )
        self._write(
            "candidate_beats.json",
            {
                "beats": [
                    {
                        "signal_id": "beat_0001",
                        "time": 1.03,
                        "timecode": "00:01:02",
                        "frame": 62,
                        "source_types": ["audio_onset"],
                        "source_signal_ids": ["aud_onset_0001"],
                    }
                ]
            },
        )
        self._write(
            "prosody_segments.json",
            {
                "segments": [
                    {
                        "signal_id": "prosody_seg_0001",
                        "segment_id": "seg_0001",
                        "start": 0.8,
                        "end": 1.4,
                        "wpm": 260,
                        "delivery_tags": ["fast_speech"],
                        "text": "cut here",
                        "features": {},
                    }
                ]
            },
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write(self, name: str, data: object) -> None:
        (self.signals_dir / name).write_text(json.dumps(data), encoding="utf-8")

    def test_select_boundaries_keeps_review_candidates_by_default(self) -> None:
        boundaries = gemini_sdk_video.load_boundaries(self.signals_dir)
        selected = gemini_sdk_video.select_boundaries(
            boundaries,
            requested_ids=None,
            max_boundaries=None,
            hard_cuts_only=False,
        )
        self.assertEqual(
            [item["signal_id"] for item in selected],
            ["edit_boundary_0001", "edit_boundary_0002"],
        )

    def test_select_boundaries_can_limit_to_hard_cuts(self) -> None:
        boundaries = gemini_sdk_video.load_boundaries(self.signals_dir)
        selected = gemini_sdk_video.select_boundaries(
            boundaries,
            requested_ids=None,
            max_boundaries=None,
            hard_cuts_only=True,
        )
        self.assertEqual([item["signal_id"] for item in selected], ["edit_boundary_0001"])

    def test_post_cut_context_is_boundary_local(self) -> None:
        media = gemini_sdk_video.load_media(self.signals_dir, Path("example.mp4"))
        boundary = gemini_sdk_video.load_boundaries(self.signals_dir)[0]
        window, context_text = gemini_sdk_video.post_cut_motion_context(
            self.signals_dir,
            boundary,
            media,
            window_before=0.1,
            window_after=0.9,
        )
        context = json.loads(context_text)

        self.assertEqual(window["start_timecode"], "00:00:54")
        self.assertEqual(window["end_timecode"], "00:01:54")
        self.assertEqual(context["boundary"]["signal_id"], "edit_boundary_0001")
        self.assertEqual(
            context["adjacent_spans"]["previous_span"]["signal_id"],
            "edit_span_0001",
        )
        self.assertEqual(
            context["adjacent_spans"]["next_span"]["signal_id"],
            "edit_span_0002",
        )
        self.assertIn("word_0001", context_text)
        self.assertNotIn("word_far", context_text)
        self.assertIn("beat_0001", context_text)
        self.assertIn("prosody_seg_0001", context_text)


if __name__ == "__main__":
    unittest.main()
