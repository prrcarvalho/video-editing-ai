#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = [
#     "librosa>=0.10.2",
#     "numpy>=1.26",
#     "opencv-python-headless>=4.9",
#     "opensmile>=2.5.1",
#     "pillow>=10.0",
#     "pytesseract>=0.3.10",
#     "scenedetect[opencv]>=0.6.4",
#     "soundfile>=0.12.1",
#     "whisperx>=3.3.0",
# ]
# ///
"""
Create a signal-grounded Exemplar ingest pack.

The output is designed for Gemini prompts that should interpret timing signals,
not invent them. Run from the repo root:

    uv run scripts/exemplar_ingest.py assets/instagram-real.MP4
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_ROOT = REPO_ROOT / "gemini_pipeline" / "outputs"


@dataclass(frozen=True)
class EventPoint:
    time: float
    frame: int
    signal_id: str
    kind: str
    weight: float = 1.0


def run_command(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            cmd,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"required executable not found: {cmd[0]}") from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        raise RuntimeError(f"{cmd[0]} failed: {message}") from exc


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_probe(video_path: Path) -> dict[str, Any]:
    result = run_command(
        [
            "ffprobe",
            "-hide_banner",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size,bit_rate:stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,nb_frames,sample_rate,channels",
            "-of",
            "json",
            str(video_path),
        ]
    )
    return json.loads(result.stdout)


def ratio_to_float(value: str | None) -> float:
    if not value or value == "0/0":
        return 0.0
    if "/" not in value:
        return float(value)
    num, den = value.split("/", 1)
    return float(num) / float(den)


def frame_for_time(seconds: float, fps: float) -> int:
    return max(0, int(round(seconds * fps)))


def seconds(value: float | int | str | None) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def fmt_time(value: float) -> str:
    minutes = int(value // 60)
    secs = value - minutes * 60
    return f"{minutes:02d}:{secs:05.2f}"


def md_cell(value: Any) -> str:
    text = str(value).replace("\n", " ").strip()
    return text.replace("|", "\\|")


def media_metadata(video_path: Path) -> dict[str, Any]:
    probe = read_probe(video_path)
    video_stream = next(
        (stream for stream in probe.get("streams", []) if stream.get("codec_type") == "video"),
        {},
    )
    audio_stream = next(
        (stream for stream in probe.get("streams", []) if stream.get("codec_type") == "audio"),
        {},
    )
    duration = float(probe.get("format", {}).get("duration") or 0)
    fps = ratio_to_float(video_stream.get("avg_frame_rate")) or ratio_to_float(
        video_stream.get("r_frame_rate")
    )
    frame_count = int(video_stream.get("nb_frames") or round(duration * fps))
    return {
        "source_path": str(video_path),
        "filename": video_path.name,
        "duration": duration,
        "fps": fps,
        "frame_count": frame_count,
        "resolution": {
            "width": int(video_stream.get("width") or 0),
            "height": int(video_stream.get("height") or 0),
        },
        "video": {
            "codec": video_stream.get("codec_name"),
            "r_frame_rate": video_stream.get("r_frame_rate"),
            "avg_frame_rate": video_stream.get("avg_frame_rate"),
        },
        "audio": {
            "codec": audio_stream.get("codec_name"),
            "sample_rate": int(audio_stream.get("sample_rate") or 0),
            "channels": int(audio_stream.get("channels") or 0),
        },
        "format": {
            "size": int(probe.get("format", {}).get("size") or 0),
            "bit_rate": int(probe.get("format", {}).get("bit_rate") or 0),
        },
    }


def extract_audio(video_path: Path, work_dir: Path) -> tuple[Path, Path]:
    work_dir.mkdir(parents=True, exist_ok=True)
    asr_audio = work_dir / "audio_16k_mono.wav"
    analysis_audio = work_dir / "audio_48k_mono.wav"
    run_command(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(video_path),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-sample_fmt",
            "s16",
            str(asr_audio),
        ]
    )
    run_command(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(video_path),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "48000",
            "-sample_fmt",
            "s16",
            str(analysis_audio),
        ]
    )
    return asr_audio, analysis_audio


def run_whisperx(audio_path: Path, fps: float, args: argparse.Namespace) -> dict[str, Any]:
    import whisperx

    audio = whisperx.load_audio(str(audio_path))
    model = whisperx.load_model(
        args.whisper_model,
        args.device,
        compute_type=args.compute_type,
        language=args.language,
    )
    result = model.transcribe(audio, batch_size=args.batch_size, language=args.language)
    language = result.get("language") or args.language

    align_model, metadata = whisperx.load_align_model(language_code=language, device=args.device)
    aligned = whisperx.align(
        result.get("segments", []),
        align_model,
        metadata,
        audio,
        args.device,
        return_char_alignments=False,
    )

    words: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for segment_index, segment in enumerate(aligned.get("segments", [])):
        for word_index, item in enumerate(segment.get("words", [])):
            start = seconds(item.get("start"))
            end = seconds(item.get("end"))
            raw_word = str(item.get("word") or "").strip()
            if start is None or end is None or not raw_word:
                skipped.append(
                    {
                        "segment_index": segment_index,
                        "word_index": word_index,
                        "word": raw_word,
                        "reason": "missing_timing_or_text",
                    }
                )
                continue
            words.append(
                {
                    "signal_id": f"word_{len(words) + 1:04d}",
                    "word": raw_word,
                    "start": round(start, 4),
                    "end": round(end, 4),
                    "start_frame": frame_for_time(start, fps),
                    "end_frame": frame_for_time(end, fps),
                    "score": item.get("score"),
                    "segment_index": segment_index,
                }
            )

    segments = []
    for index, segment in enumerate(aligned.get("segments", [])):
        start = seconds(segment.get("start"))
        end = seconds(segment.get("end"))
        segments.append(
            {
                "signal_id": f"seg_{index + 1:04d}",
                "start": round(start or 0.0, 4),
                "end": round(end or 0.0, 4),
                "start_frame": frame_for_time(start or 0.0, fps),
                "end_frame": frame_for_time(end or 0.0, fps),
                "text": str(segment.get("text") or "").strip(),
            }
        )

    return {
        "tool": "whisperx",
        "model": args.whisper_model,
        "language": language,
        "device": args.device,
        "compute_type": args.compute_type,
        "word_count": len(words),
        "segments": segments,
        "words": words,
        "skipped_words": skipped,
    }


def stats(values: Any) -> dict[str, float | None]:
    import numpy as np

    array = np.asarray(values, dtype=float)
    array = array[np.isfinite(array)]
    if array.size == 0:
        return {"min": None, "max": None, "mean": None, "median": None, "p10": None, "p90": None}
    return {
        "min": round(float(np.min(array)), 6),
        "max": round(float(np.max(array)), 6),
        "mean": round(float(np.mean(array)), 6),
        "median": round(float(np.median(array)), 6),
        "p10": round(float(np.percentile(array, 10)), 6),
        "p90": round(float(np.percentile(array, 90)), 6),
    }


def local_maxima(values: Any, threshold: float, min_gap: int) -> list[int]:
    import numpy as np

    array = np.asarray(values, dtype=float)
    peaks: list[int] = []
    last = -min_gap
    for index in range(1, max(1, len(array) - 1)):
        if index - last < min_gap:
            continue
        if array[index] < threshold:
            continue
        if array[index] >= array[index - 1] and array[index] >= array[index + 1]:
            peaks.append(index)
            last = index
    return peaks


def silence_intervals(mask: Any, times: Any, min_duration: float) -> list[dict[str, float]]:
    intervals: list[dict[str, float]] = []
    start: float | None = None
    previous_time = 0.0
    for is_silent, time_value in zip(mask, times):
        time_float = float(time_value)
        if bool(is_silent) and start is None:
            start = time_float
        if not bool(is_silent) and start is not None:
            if previous_time - start >= min_duration:
                intervals.append({"start": round(start, 4), "end": round(previous_time, 4)})
            start = None
        previous_time = time_float
    if start is not None and previous_time - start >= min_duration:
        intervals.append({"start": round(start, 4), "end": round(previous_time, 4)})
    return intervals


def run_audio_features(audio_path: Path, fps: float, duration: float) -> dict[str, Any]:
    import librosa
    import numpy as np

    y, sr = librosa.load(str(audio_path), sr=None, mono=True)
    hop_length = max(1, int(round(sr / fps)))
    frame_length = max(2048, hop_length * 4)
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    rms_db = librosa.amplitude_to_db(rms, ref=max(float(np.max(rms)), 1e-9))
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    onset_frames = librosa.onset.onset_detect(
        onset_envelope=onset_env,
        sr=sr,
        hop_length=hop_length,
        backtrack=False,
        units="frames",
    )
    tempo, beat_frames = librosa.beat.beat_track(
        y=y,
        sr=sr,
        hop_length=hop_length,
        units="frames",
    )
    if hasattr(tempo, "__len__"):
        tempo = float(tempo[0]) if len(tempo) else 0.0
    tempo = float(tempo)

    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop_length)[0]
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, hop_length=hop_length)[0]
    flatness = librosa.feature.spectral_flatness(y=y, hop_length=hop_length)[0]
    zcr = librosa.feature.zero_crossing_rate(y, hop_length=hop_length)[0]
    times = librosa.frames_to_time(range(len(rms)), sr=sr, hop_length=hop_length)

    onset_events = []
    for index, frame in enumerate(onset_frames):
        time_value = min(float(librosa.frames_to_time(frame, sr=sr, hop_length=hop_length)), duration)
        onset_events.append(
            {
                "signal_id": f"aud_onset_{index + 1:04d}",
                "time": round(time_value, 4),
                "frame": frame_for_time(time_value, fps),
                "strength": round(float(onset_env[int(frame)]), 6),
            }
        )

    peak_threshold = float(np.percentile(rms, 90)) if len(rms) else 0.0
    peak_frames = local_maxima(rms, peak_threshold, max(1, int(round(fps * 0.18))))
    loudness_peaks = []
    for index, frame in enumerate(peak_frames[:120]):
        time_value = min(float(times[frame]), duration)
        loudness_peaks.append(
            {
                "signal_id": f"aud_peak_{index + 1:04d}",
                "time": round(time_value, 4),
                "frame": frame_for_time(time_value, fps),
                "rms": round(float(rms[frame]), 6),
                "db_relative_to_peak": round(float(rms_db[frame]), 3),
            }
        )

    silence_mask = rms_db < -35.0
    silences = silence_intervals(silence_mask, times, min_duration=0.16)
    for index, item in enumerate(silences):
        item["signal_id"] = f"aud_silence_{index + 1:04d}"
        item["start_frame"] = frame_for_time(item["start"], fps)
        item["end_frame"] = frame_for_time(item["end"], fps)

    beat_events = []
    for index, frame in enumerate(beat_frames[:160]):
        time_value = min(float(librosa.frames_to_time(frame, sr=sr, hop_length=hop_length)), duration)
        beat_events.append(
            {
                "signal_id": f"aud_beat_{index + 1:04d}",
                "time": round(time_value, 4),
                "frame": frame_for_time(time_value, fps),
            }
        )

    return {
        "tool": "librosa",
        "sample_rate": sr,
        "hop_length": hop_length,
        "tempo_bpm": round(tempo, 3),
        "summary": {
            "rms": stats(rms),
            "rms_db_relative": stats(rms_db),
            "onset_strength": stats(onset_env),
            "spectral_centroid": stats(centroid),
            "spectral_rolloff": stats(rolloff),
            "spectral_flatness": stats(flatness),
            "zero_crossing_rate": stats(zcr),
        },
        "events": {
            "onsets": onset_events,
            "loudness_peaks": loudness_peaks,
            "silences": silences,
            "beats": beat_events,
        },
    }


def run_prosody(audio_path: Path) -> dict[str, Any]:
    try:
        import numpy as np
        import opensmile

        smile = opensmile.Smile(
            feature_set=opensmile.FeatureSet.eGeMAPSv02,
            feature_level=opensmile.FeatureLevel.Functionals,
        )
        frame = smile.process_file(str(audio_path))
        if frame.empty:
            return {"tool": "opensmile", "feature_set": "eGeMAPSv02", "status": "empty"}
        row = frame.iloc[0]
        features = {}
        for key, value in row.items():
            number = float(value)
            if np.isfinite(number):
                features[str(key)] = round(number, 6)
        return {
            "tool": "opensmile",
            "feature_set": "eGeMAPSv02",
            "feature_level": "Functionals",
            "status": "ok",
            "features": features,
        }
    except Exception as exc:  # openSMILE is useful, but not worth killing the whole ingest.
        return {
            "tool": "opensmile",
            "feature_set": "eGeMAPSv02",
            "status": "skipped",
            "reason": str(exc),
        }


def detect_scenes_with_pyscenedetect(video_path: Path, fps: float, threshold: float) -> list[dict[str, Any]]:
    try:
        from scenedetect import SceneManager, open_video
        from scenedetect.detectors import ContentDetector
    except Exception:
        return []

    video = open_video(str(video_path))
    manager = SceneManager()
    manager.add_detector(ContentDetector(threshold=threshold))
    manager.detect_scenes(video)
    scenes = manager.get_scene_list()
    cuts = []
    for index, (start, _end) in enumerate(scenes[1:]):
        time_value = start.get_seconds()
        cuts.append(
            {
                "signal_id": f"vis_scene_{index + 1:04d}",
                "time": round(time_value, 4),
                "frame": frame_for_time(time_value, fps),
                "detector": "pyscenedetect.ContentDetector",
            }
        )
    return cuts


def save_frame(video_path: Path, frame_number: int, output_path: Path) -> bool:
    import cv2

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))
    try:
        cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, frame_number))
        ok, frame = cap.read()
        if not ok:
            return False
        return bool(cv2.imwrite(str(output_path), frame))
    finally:
        cap.release()


def normalize_ocr(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[^A-Za-z0-9 ]+", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def ocr_frame(frame: Any, args: argparse.Namespace) -> str:
    import cv2
    import pytesseract
    from PIL import Image

    height, width = frame.shape[:2]
    crop = frame[int(height * 0.08) : int(height * 0.9), int(width * 0.04) : int(width * 0.96)]
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    image = Image.fromarray(binary)
    return pytesseract.image_to_string(image, lang=args.ocr_lang, config="--psm 6")


def detect_visual_events(
    video_path: Path,
    media: dict[str, Any],
    out_dir: Path,
    args: argparse.Namespace,
) -> dict[str, Any]:
    import cv2
    import numpy as np

    fps = float(media["fps"])
    duration = float(media["duration"])
    scene_cuts = detect_scenes_with_pyscenedetect(video_path, fps, args.scene_threshold)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"OpenCV could not open {video_path}")

    diffs: list[tuple[int, float]] = []
    previous = None
    frame_index = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            resized = cv2.resize(frame, (180, 320), interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            if previous is not None:
                diff = float(np.mean(cv2.absdiff(gray, previous)) / 255.0)
                diffs.append((frame_index, diff))
            previous = gray
            frame_index += 1
    finally:
        cap.release()

    diff_values = np.asarray([value for _, value in diffs], dtype=float)
    threshold = float(np.percentile(diff_values, args.diff_percentile)) if diff_values.size else 0.0
    threshold = max(threshold, args.min_diff_score)
    candidate_indices = local_maxima(
        diff_values,
        threshold,
        max(1, int(round(fps * args.visual_min_gap))),
    )
    frame_diff_events = []
    for index, diff_index in enumerate(candidate_indices[:160]):
        frame_number, score = diffs[diff_index]
        time_value = min(frame_number / fps, duration)
        frame_diff_events.append(
            {
                "signal_id": f"vis_diff_{index + 1:04d}",
                "time": round(time_value, 4),
                "frame": frame_number,
                "score": round(float(score), 6),
                "threshold": round(threshold, 6),
            }
        )

    keyframes = []
    keyframe_times = [0.0]
    keyframe_times.extend(item["time"] for item in scene_cuts[:80])
    keyframe_times.extend(item["time"] for item in frame_diff_events[:80])
    seen_frames = set()
    for index, time_value in enumerate(sorted(set(round(t, 3) for t in keyframe_times))):
        frame_number = frame_for_time(time_value, fps)
        if frame_number in seen_frames:
            continue
        seen_frames.add(frame_number)
        relative_path = Path("keyframes") / f"keyframe_{len(keyframes) + 1:04d}.jpg"
        if save_frame(video_path, frame_number, out_dir / relative_path):
            keyframes.append(
                {
                    "signal_id": f"keyframe_{len(keyframes) + 1:04d}",
                    "time": round(time_value, 4),
                    "frame": frame_number,
                    "path": str(relative_path),
                }
            )

    ocr_states = []
    if not args.skip_ocr:
        cap = cv2.VideoCapture(str(video_path))
        current: dict[str, Any] | None = None
        current_norm = ""
        sample_count = max(1, int(math.ceil(duration / args.ocr_interval))) + 1
        try:
            for sample_index in range(sample_count):
                time_value = min(sample_index * args.ocr_interval, duration)
                frame_number = min(frame_for_time(time_value, fps), int(media["frame_count"]) - 1)
                cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, frame_number))
                ok, frame = cap.read()
                if not ok:
                    continue
                text = re.sub(r"\s+", " ", ocr_frame(frame, args)).strip()
                norm = normalize_ocr(text)
                if norm == current_norm:
                    continue
                if current is not None:
                    current["end"] = round(time_value, 4)
                    current["end_frame"] = frame_number
                    if current.get("text"):
                        ocr_states.append(current)
                current_norm = norm
                current = {
                    "signal_id": f"ocr_state_{len(ocr_states) + 1:04d}",
                    "start": round(time_value, 4),
                    "end": round(duration, 4),
                    "start_frame": frame_number,
                    "end_frame": frame_for_time(duration, fps),
                    "text": text,
                    "normalized_text": norm,
                }
            if current is not None and current.get("text"):
                ocr_states.append(current)
        finally:
            cap.release()

    return {
        "tooling": {
            "scene_detector": "pyscenedetect.ContentDetector",
            "frame_diff": "opencv mean grayscale absdiff",
            "ocr": "pytesseract" if not args.skip_ocr else "skipped",
        },
        "scene_cuts": scene_cuts,
        "frame_diff_events": frame_diff_events,
        "ocr_states": ocr_states,
        "keyframes": keyframes,
    }


def word_window(words: list[dict[str, Any]], time_value: float) -> list[dict[str, Any]]:
    nearby = []
    for word in words:
        start = float(word["start"])
        if time_value - 0.35 <= start <= time_value + 0.8:
            nearby.append(
                {
                    "signal_id": word["signal_id"],
                    "word": word["word"],
                    "start": word["start"],
                    "end": word["end"],
                }
            )
    return nearby[:12]


def ocr_at_time(ocr_states: list[dict[str, Any]], time_value: float) -> str | None:
    for state in ocr_states:
        if float(state["start"]) <= time_value <= float(state["end"]):
            text = state.get("text")
            return str(text) if text else None
    return None


def build_candidate_beats(
    media: dict[str, Any],
    transcript: dict[str, Any],
    audio_features: dict[str, Any],
    visual_events: dict[str, Any],
    merge_window: float,
) -> dict[str, Any]:
    fps = float(media["fps"])
    points: list[EventPoint] = []

    def add(time_value: float | None, signal_id: str, kind: str, weight: float = 1.0) -> None:
        if time_value is None:
            return
        duration = float(media["duration"])
        clamped = min(max(0.0, float(time_value)), duration)
        points.append(EventPoint(clamped, frame_for_time(clamped, fps), signal_id, kind, weight))

    add(0.0, "media_start", "boundary", 2.0)
    for item in visual_events.get("scene_cuts", []):
        add(item.get("time"), item["signal_id"], "visual_scene_cut", 1.4)
    for item in visual_events.get("frame_diff_events", []):
        add(item.get("time"), item["signal_id"], "visual_frame_diff", 1.0)
    for item in visual_events.get("ocr_states", []):
        text = str(item.get("normalized_text") or item.get("text") or "").strip()
        if len(text) < 8:
            continue
        if float(item.get("end", 0.0)) - float(item.get("start", 0.0)) < 0.2:
            continue
        add(item.get("start"), item["signal_id"], "ocr_caption_change", 1.3)

    events = audio_features.get("events", {})
    strong_onsets = sorted(
        events.get("onsets", []),
        key=lambda item: float(item.get("strength") or 0.0),
        reverse=True,
    )[:45]
    for item in sorted(strong_onsets, key=lambda item: float(item.get("time") or 0.0)):
        add(item.get("time"), item["signal_id"], "audio_onset", 0.8)
    for item in events.get("loudness_peaks", []):
        add(item.get("time"), item["signal_id"], "audio_loudness_peak", 0.7)
    for item in events.get("silences", []):
        add(item.get("start"), item["signal_id"], "audio_silence_start", 1.0)

    for segment in transcript.get("segments", []):
        add(segment.get("start"), segment["signal_id"], "transcript_segment_start", 1.1)

    previous_word = None
    for word in transcript.get("words", []):
        if previous_word is None:
            add(word.get("start"), word["signal_id"], "first_word", 1.0)
        else:
            gap = float(word["start"]) - float(previous_word["end"])
            if gap >= 0.22:
                add(word.get("start"), word["signal_id"], "word_after_pause", min(1.5, gap))
        previous_word = word

    points.sort(key=lambda item: (item.time, item.signal_id))
    grouped: list[dict[str, Any]] = []
    for point in points:
        if not grouped or point.time - float(grouped[-1]["time"]) > merge_window:
            grouped.append(
                {
                    "signal_id": f"beat_{len(grouped) + 1:04d}",
                    "time": round(point.time, 4),
                    "frame": point.frame,
                    "sources": [
                        {
                            "signal_id": point.signal_id,
                            "kind": point.kind,
                            "time": round(point.time, 4),
                            "frame": point.frame,
                            "weight": point.weight,
                        }
                    ],
                }
            )
        else:
            grouped[-1]["sources"].append(
                {
                    "signal_id": point.signal_id,
                    "kind": point.kind,
                    "time": round(point.time, 4),
                    "frame": point.frame,
                    "weight": point.weight,
                }
            )

    words = transcript.get("words", [])
    ocr_states = visual_events.get("ocr_states", [])
    for beat in grouped:
        time_value = float(beat["time"])
        source_types = sorted({source["kind"] for source in beat["sources"]})
        beat["source_types"] = source_types
        beat["source_signal_ids"] = [source["signal_id"] for source in beat["sources"]]
        beat["near_words"] = word_window(words, time_value)
        beat["ocr_text"] = ocr_at_time(ocr_states, time_value)

    by_kind: dict[str, int] = defaultdict(int)
    for beat in grouped:
        for kind in beat["source_types"]:
            by_kind[kind] += 1

    return {
        "merge_window_seconds": merge_window,
        "beat_count": len(grouped),
        "source_type_counts": dict(sorted(by_kind.items())),
        "beats": grouped,
    }


def transcript_text(transcript: dict[str, Any]) -> str:
    words = [str(item.get("word") or "").strip() for item in transcript.get("words", [])]
    return re.sub(r"\s+", " ", " ".join(words)).strip()


def render_signals_markdown(
    video_path: Path,
    media: dict[str, Any],
    transcript: dict[str, Any],
    audio_features: dict[str, Any],
    prosody: dict[str, Any],
    visual_events: dict[str, Any],
    beats: dict[str, Any],
) -> str:
    lines: list[str] = []
    lines.append(f"# Signal Pack: {video_path.name}")
    lines.append("")
    lines.append("This is the deterministic timing context for Gemini. Use signal IDs as the timing source of truth.")
    lines.append("")
    lines.append("## Media")
    lines.append("")
    lines.append("| field | value |")
    lines.append("|---|---|")
    lines.append(f"| duration | {media['duration']:.3f}s |")
    lines.append(f"| fps | {media['fps']:.3f} |")
    lines.append(f"| frame_count | {media['frame_count']} |")
    lines.append(f"| resolution | {media['resolution']['width']}x{media['resolution']['height']} |")
    lines.append(f"| audio | {media['audio']['codec']}, {media['audio']['sample_rate']} Hz, {media['audio']['channels']} channels |")
    lines.append("")
    lines.append("## Transcript")
    lines.append("")
    lines.append(f"Word count: {transcript.get('word_count', 0)}")
    lines.append("")
    text = transcript_text(transcript)
    lines.append(text if text else "_No timed transcript words were produced._")
    lines.append("")
    if transcript.get("words"):
        lines.append("| word_id | time | frames | word | score |")
        lines.append("|---|---:|---:|---|---:|")
        for word in transcript["words"]:
            score = word.get("score")
            score_text = "" if score is None else f"{float(score):.3f}"
            lines.append(
                f"| {word['signal_id']} | {fmt_time(float(word['start']))}-{fmt_time(float(word['end']))} | "
                f"{word['start_frame']}-{word['end_frame']} | {md_cell(word['word'])} | {score_text} |"
            )
        lines.append("")
    if transcript.get("segments"):
        lines.append("## Transcript Segments")
        lines.append("")
        lines.append("| segment_id | time | frames | text |")
        lines.append("|---|---:|---:|---|")
        for segment in transcript["segments"]:
            lines.append(
                f"| {segment['signal_id']} | {fmt_time(float(segment['start']))}-{fmt_time(float(segment['end']))} | "
                f"{segment['start_frame']}-{segment['end_frame']} | {md_cell(segment['text'])} |"
            )
        lines.append("")

    lines.append("## Audio Signals")
    lines.append("")
    lines.append(f"Estimated tempo: {audio_features.get('tempo_bpm')} BPM")
    lines.append("")
    lines.append("| signal_id | kind | time | frame | detail |")
    lines.append("|---|---|---:|---:|---|")
    strong_onsets = sorted(
        audio_features.get("events", {}).get("onsets", []),
        key=lambda item: float(item.get("strength") or 0.0),
        reverse=True,
    )[:25]
    for item in sorted(strong_onsets, key=lambda item: float(item.get("time") or 0.0)):
        lines.append(
            f"| {item['signal_id']} | onset | {fmt_time(float(item['time']))} | {item['frame']} | strength {item.get('strength')} |"
        )
    for item in audio_features.get("events", {}).get("loudness_peaks", [])[:20]:
        lines.append(
            f"| {item['signal_id']} | loudness_peak | {fmt_time(float(item['time']))} | {item['frame']} | "
            f"rms {item.get('rms')}, dB {item.get('db_relative_to_peak')} |"
        )
    for item in audio_features.get("events", {}).get("silences", [])[:80]:
        lines.append(
            f"| {item['signal_id']} | silence | {fmt_time(float(item['start']))}-{fmt_time(float(item['end']))} | "
            f"{item['start_frame']}-{item['end_frame']} | low RMS |"
        )
    lines.append("")

    lines.append("## Prosody Summary")
    lines.append("")
    if prosody.get("status") == "ok":
        selected = [
            "F0semitoneFrom27.5Hz_sma3nz_amean",
            "F0semitoneFrom27.5Hz_sma3nz_stddevNorm",
            "loudness_sma3_amean",
            "loudness_sma3_stddevNorm",
            "jitterLocal_sma3nz_amean",
            "shimmerLocaldB_sma3nz_amean",
        ]
        for key in selected:
            if key in prosody.get("features", {}):
                lines.append(f"- `{key}`: {prosody['features'][key]}")
    else:
        lines.append(f"- status: {prosody.get('status')}")
        if prosody.get("reason"):
            lines.append(f"- reason: {prosody['reason']}")
    lines.append("")

    lines.append("## Visual Signals")
    lines.append("")
    lines.append("| signal_id | kind | time | frame | detail |")
    lines.append("|---|---|---:|---:|---|")
    for item in visual_events.get("scene_cuts", [])[:80]:
        lines.append(
            f"| {item['signal_id']} | scene_cut | {fmt_time(float(item['time']))} | {item['frame']} | PySceneDetect content cut |"
        )
    for item in visual_events.get("frame_diff_events", [])[:80]:
        lines.append(
            f"| {item['signal_id']} | frame_diff | {fmt_time(float(item['time']))} | {item['frame']} | score {item.get('score')} |"
        )
    lines.append("")
    if visual_events.get("ocr_states"):
        lines.append("## OCR Caption States")
        lines.append("")
        lines.append("| signal_id | time | frames | detected text |")
        lines.append("|---|---:|---:|---|")
        durable_ocr = [
            item
            for item in visual_events["ocr_states"]
            if len(str(item.get("normalized_text") or item.get("text") or "")) >= 8
            and float(item.get("end", 0.0)) - float(item.get("start", 0.0)) >= 0.2
        ]
        for item in durable_ocr[:35]:
            lines.append(
                f"| {item['signal_id']} | {fmt_time(float(item['start']))}-{fmt_time(float(item['end']))} | "
                f"{item['start_frame']}-{item['end_frame']} | {md_cell(item['text'])} |"
            )
        lines.append("")

    lines.append("## Candidate Beats")
    lines.append("")
    lines.append("| beat_id | time | frame | source_signal_ids | source_types | nearby words |")
    lines.append("|---|---:|---:|---|---|---|")
    for beat in beats.get("beats", []):
        nearby = " ".join(word["word"] for word in beat.get("near_words", []))
        lines.append(
            f"| {beat['signal_id']} | {fmt_time(float(beat['time']))} | {beat['frame']} | "
            f"{md_cell(', '.join(beat.get('source_signal_ids', [])))} | "
            f"{md_cell(', '.join(beat.get('source_types', [])))} | "
            f"{md_cell(nearby)} |"
        )
    lines.append("")
    lines.append("## Gemini Use")
    lines.append("")
    lines.append("- Do not invent timestamps.")
    lines.append("- Do not create a Beat Sheet from scratch.")
    lines.append("- Treat the tables above as the timing source of truth.")
    lines.append("- Gemini may merge, label, and explain candidate beats, but output beats should cite signal IDs.")
    lines.append("- If video inspection contradicts a signal, mark `needs_review` instead of silently overriding it.")
    lines.append("")
    return "\n".join(lines)


def default_output_dir(video_path: Path) -> Path:
    return DEFAULT_OUT_ROOT / video_path.stem / "signals"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create deterministic timing signals for an Exemplar video."
    )
    parser.add_argument("video", help="path to the Exemplar mp4")
    parser.add_argument("--out", help="output signal folder")
    parser.add_argument("--whisper-model", default="large-v3")
    parser.add_argument("--language", default="en")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--compute-type", default="int8")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--skip-transcript", action="store_true")
    parser.add_argument("--skip-prosody", action="store_true")
    parser.add_argument("--skip-ocr", action="store_true")
    parser.add_argument("--ocr-lang", default="eng")
    parser.add_argument("--ocr-interval", type=float, default=0.25)
    parser.add_argument("--scene-threshold", type=float, default=30.0)
    parser.add_argument("--diff-percentile", type=float, default=98.5)
    parser.add_argument("--min-diff-score", type=float, default=0.06)
    parser.add_argument("--visual-min-gap", type=float, default=0.18)
    parser.add_argument("--merge-window", type=float, default=0.18)
    parser.add_argument("--force", action="store_true", help="overwrite an existing signal folder")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    video_path = Path(args.video).expanduser().resolve()
    if not video_path.is_file():
        sys.exit(f"error: {video_path} is not a file")

    out_dir = Path(args.out).expanduser().resolve() if args.out else default_output_dir(video_path)
    if out_dir.exists() and args.force:
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir = out_dir / "_work"

    media = media_metadata(video_path)
    write_json(out_dir / "media.json", media)
    print(f"wrote {out_dir / 'media.json'}")

    asr_audio, analysis_audio = extract_audio(video_path, work_dir)

    if args.skip_transcript:
        transcript = {
            "tool": "whisperx",
            "status": "skipped",
            "word_count": 0,
            "segments": [],
            "words": [],
            "skipped_words": [],
        }
    else:
        transcript = run_whisperx(asr_audio, float(media["fps"]), args)
    write_json(out_dir / "transcript.words.json", transcript)
    print(f"wrote {out_dir / 'transcript.words.json'}")

    audio_features = run_audio_features(analysis_audio, float(media["fps"]), float(media["duration"]))
    write_json(out_dir / "audio_features.json", audio_features)
    print(f"wrote {out_dir / 'audio_features.json'}")

    prosody = (
        {"tool": "opensmile", "feature_set": "eGeMAPSv02", "status": "skipped"}
        if args.skip_prosody
        else run_prosody(analysis_audio)
    )
    write_json(out_dir / "prosody_features.json", prosody)
    print(f"wrote {out_dir / 'prosody_features.json'}")

    visual_events = detect_visual_events(video_path, media, out_dir, args)
    write_json(out_dir / "visual_events.json", visual_events)
    print(f"wrote {out_dir / 'visual_events.json'}")

    beats = build_candidate_beats(
        media,
        transcript,
        audio_features,
        visual_events,
        merge_window=args.merge_window,
    )
    write_json(out_dir / "candidate_beats.json", beats)
    print(f"wrote {out_dir / 'candidate_beats.json'}")

    signals_md = render_signals_markdown(
        video_path,
        media,
        transcript,
        audio_features,
        prosody,
        visual_events,
        beats,
    )
    (out_dir / "signals_for_gemini.md").write_text(signals_md + "\n", encoding="utf-8")
    print(f"wrote {out_dir / 'signals_for_gemini.md'}")
    print(f"\nsignal pack: {out_dir}")


if __name__ == "__main__":
    main()
