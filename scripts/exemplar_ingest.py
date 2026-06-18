#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = [
#     "einops>=0.7",
#     "kagglehub>=0.3.6",
#     "librosa>=0.10.2",
#     "numpy>=1.26",
#     "opencv-python-headless>=4.9",
#     "opensmile>=2.5.1",
#     "scenedetect>=0.7,<0.8",
#     "soundfile>=0.12.1",
#     "torch>=2.2",
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
import importlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_ROOT = REPO_ROOT / "gemini_pipeline" / "outputs"
SHORT_FORM_MAX_DURATION_SECONDS = 90.0
os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

PROSODY_SUMMARY_KEYS = [
    "F0semitoneFrom27.5Hz_sma3nz_amean",
    "F0semitoneFrom27.5Hz_sma3nz_stddevNorm",
    "F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2",
    "loudness_sma3_amean",
    "loudness_sma3_stddevNorm",
    "loudness_sma3_pctlrange0-2",
    "loudnessPeaksPerSec",
    "jitterLocal_sma3nz_amean",
    "shimmerLocaldB_sma3nz_amean",
]

PROSODY_SEGMENT_KEYS = [
    "F0semitoneFrom27.5Hz_sma3nz_amean",
    "F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2",
    "F0semitoneFrom27.5Hz_sma3nz_meanRisingSlope",
    "F0semitoneFrom27.5Hz_sma3nz_meanFallingSlope",
    "loudness_sma3_amean",
    "loudness_sma3_pctlrange0-2",
    "loudness_sma3_meanRisingSlope",
    "loudness_sma3_meanFallingSlope",
    "loudnessPeaksPerSec",
    "spectralFlux_sma3_amean",
]


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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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


def timebase_for_fps(fps: float) -> int:
    return max(1, int(round(fps)))


def timecode_for_frame(frame: int, fps: float) -> str:
    timebase = timebase_for_fps(fps)
    frame = max(0, int(frame))
    total_seconds, frame_in_second = divmod(frame, timebase)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds_value = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{seconds_value:02d}:{frame_in_second:02d}"
    return f"{minutes:02d}:{seconds_value:02d}:{frame_in_second:02d}"


def timecode_for_time(value: float, fps: float) -> str:
    return timecode_for_frame(frame_for_time(value, fps), fps)


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


def add_timecodes(data: Any, fps: float) -> Any:
    if isinstance(data, dict):
        if "frame" in data and "timecode" not in data:
            data["timecode"] = timecode_for_frame(int(data["frame"]), fps)
        elif "time" in data and "timecode" not in data:
            value = seconds(data.get("time"))
            if value is not None:
                data["timecode"] = timecode_for_time(value, fps)

        if "start_frame" in data and "start_timecode" not in data:
            data["start_timecode"] = timecode_for_frame(int(data["start_frame"]), fps)
        elif "start" in data and "start_timecode" not in data:
            value = seconds(data.get("start"))
            if value is not None:
                data["start_timecode"] = timecode_for_time(value, fps)

        if "end_frame" in data and "end_timecode" not in data:
            data["end_timecode"] = timecode_for_frame(int(data["end_frame"]), fps)
        elif "end" in data and "end_timecode" not in data:
            value = seconds(data.get("end"))
            if value is not None:
                data["end_timecode"] = timecode_for_time(value, fps)

        for value in data.values():
            add_timecodes(value, fps)
    elif isinstance(data, list):
        for item in data:
            add_timecodes(item, fps)
    return data


def fmt_time(value: float, fps: float) -> str:
    return timecode_for_time(value, fps)


def fmt_range(start: float, end: float, fps: float) -> str:
    return f"{fmt_time(start, fps)}-{fmt_time(end, fps)}"


def fmt_frame_duration(start_frame: int, end_frame: int, fps: float) -> str:
    frames = max(0, int(end_frame) - int(start_frame))
    return f"{frames} frames ({timecode_for_frame(frames, fps)})"


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


def is_short_form_media(media: dict[str, Any], max_duration_seconds: float) -> bool:
    duration = float(media.get("duration") or 0.0)
    resolution = media.get("resolution") or {}
    width = int(resolution.get("width") or 0)
    height = int(resolution.get("height") or 0)
    is_social_shape = height >= width and width > 0
    return 0 < duration <= max_duration_seconds and is_social_shape


def resolve_autoshot_setting(
    args: argparse.Namespace,
    media: dict[str, Any],
) -> tuple[bool, str, bool]:
    short_form_detected = is_short_form_media(media, args.short_form_max_duration)
    if args.autoshot is not None:
        reason = "forced_on_by_flag" if args.autoshot else "forced_off_by_flag"
        return bool(args.autoshot), reason, short_form_detected
    if args.content_profile == "short-form":
        return True, "content_profile_short_form", short_form_detected
    if args.content_profile == "long-form":
        return False, "content_profile_long_form", short_form_detected
    if short_form_detected:
        return True, "auto_detected_vertical_short_form", short_form_detected
    return False, "auto_not_short_form", short_form_detected


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


def finite_feature_dict(row: Any) -> dict[str, float]:
    import numpy as np

    features = {}
    for key, value in row.items():
        number = float(value)
        if np.isfinite(number):
            features[str(key)] = round(number, 6)
    return features


def selected_features(features: dict[str, Any], keys: list[str]) -> dict[str, Any]:
    return {key: features[key] for key in keys if key in features}


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
        features = finite_feature_dict(row)
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
        from scenedetect import ContentDetector, SceneManager, open_video
    except Exception:
        return []

    video = open_video(str(video_path))
    manager = SceneManager()
    manager.add_detector(ContentDetector(threshold=threshold))
    manager.detect_scenes(video)
    scenes = manager.get_scene_list()
    cuts = []
    for index, (start, _end) in enumerate(scenes[1:]):
        time_value = float(start.seconds)
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


def cached_autoshot_model_dir() -> Path | None:
    cache_root = Path.home() / ".cache" / "kagglehub" / "models" / "tuktuai" / "autoshot"
    candidates = sorted(cache_root.glob("pyTorch/v*/**/ckpt_0_200_0.pth"), reverse=True)
    if not candidates:
        return None
    return candidates[0].parent


def resolve_autoshot_model_dir(args: argparse.Namespace) -> Path:
    if args.autoshot_model_dir:
        model_dir = Path(args.autoshot_model_dir).expanduser().resolve()
    else:
        model_dir = cached_autoshot_model_dir()
        if model_dir is None and args.autoshot_download_kaggle:
            import kagglehub

            model_dir = Path(kagglehub.model_download("tuktuai/autoshot/pyTorch/v1")).resolve()

    if model_dir is None:
        raise RuntimeError(
            "AutoShot model not found. Provide --autoshot-model-dir or run with "
            "--autoshot-download-kaggle to fetch the Kaggle mirror."
        )

    required = [
        model_dir / "ckpt_0_200_0.pth",
        model_dir / "linear.py",
        model_dir / "supernet_flattransf_3_8_8_8_13_12_0_16_60.py",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise RuntimeError(f"AutoShot model dir is missing required files: {', '.join(missing)}")
    return model_dir


def choose_autoshot_device(torch: Any, requested: str) -> str:
    if requested == "auto":
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
        return "cpu"
    if requested == "mps":
        if not (hasattr(torch.backends, "mps") and torch.backends.mps.is_available()):
            raise RuntimeError("AutoShot requested --autoshot-device mps, but MPS is not available")
        return "mps"
    return "cpu"


def set_autoshot_module_devices(model: Any, device: str) -> None:
    for module in model.modules():
        if hasattr(module, "device"):
            module.device = device


def load_autoshot_frames(video_path: Path) -> tuple[Any, float]:
    import cv2
    import numpy as np

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"OpenCV could not open {video_path}")

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    frames = []
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            resized = cv2.resize(frame, (48, 27), interpolation=cv2.INTER_AREA)
            frames.append(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
    finally:
        cap.release()

    if not frames:
        raise RuntimeError("AutoShot could not read any frames")
    return np.asarray(frames, dtype=np.uint8), fps


def autoshot_batches(frames: Any) -> Any:
    import numpy as np

    remainder = (50 - len(frames) % 50) % 50
    padded = np.concatenate([frames[:1]] * 25 + [frames] + [frames[-1:]] * (remainder + 25), 0)
    for index in range(0, len(padded) - 50, 50):
        yield padded[index : index + 100]


def autoshot_peak_events(
    predictions: Any,
    fps: float,
    duration: float,
    threshold: float,
    min_gap_seconds: float,
    prefix: str,
    detector: str,
    max_events: int,
) -> list[dict[str, Any]]:
    min_gap = max(1, int(round(fps * min_gap_seconds)))
    indices = local_maxima(predictions, threshold, min_gap)
    events = []
    for index, frame_number in enumerate(indices[:max_events]):
        score = float(predictions[frame_number])
        time_value = min(frame_number / fps, duration)
        events.append(
            {
                "signal_id": f"{prefix}_{index + 1:04d}",
                "time": round(time_value, 4),
                "frame": int(frame_number),
                "score": round(score, 6),
                "threshold": round(float(threshold), 6),
                "detector": detector,
            }
        )
    return events


def run_autoshot_once(
    video_path: Path,
    media: dict[str, Any],
    model_dir: Path,
    device: str,
    args: argparse.Namespace,
) -> dict[str, Any]:
    import numpy as np
    import torch

    if device == "cpu":
        torch.set_num_threads(max(1, min(8, os.cpu_count() or 1)))

    sys.path.insert(0, str(model_dir))
    try:
        module = importlib.import_module("supernet_flattransf_3_8_8_8_13_12_0_16_60")
    finally:
        try:
            sys.path.remove(str(model_dir))
        except ValueError:
            pass

    model = module.TransNetV2Supernet().eval()
    checkpoint = torch.load(model_dir / "ckpt_0_200_0.pth", map_location=device)
    model_state = model.state_dict()
    pretrained = {key: value for key, value in checkpoint["net"].items() if key in model_state}
    model_state.update(pretrained)
    model.load_state_dict(model_state)
    model.to(device)
    set_autoshot_module_devices(model, device)

    frames, detected_fps = load_autoshot_frames(video_path)
    fps = float(media["fps"]) or detected_fps
    duration = float(media["duration"])
    predictions = []
    started = time.perf_counter()
    with torch.inference_mode():
        for batch in autoshot_batches(frames):
            tensor = torch.from_numpy(batch.transpose((3, 0, 1, 2))[np.newaxis]).float().to(device)
            output = model(tensor)
            if isinstance(output, tuple):
                output = output[0]
            probabilities = torch.sigmoid(output[0]).detach().cpu().numpy()
            predictions.append(probabilities[25:75])

    prediction_values = np.concatenate(predictions, 0)[: len(frames)].reshape(-1)
    detector = "AutoShot.TransNetV2Supernet"
    confident = autoshot_peak_events(
        prediction_values,
        fps,
        duration,
        args.autoshot_threshold,
        args.visual_min_gap,
        "autoshot_cut",
        detector,
        args.autoshot_max_events,
    )
    candidates = autoshot_peak_events(
        prediction_values,
        fps,
        duration,
        args.autoshot_candidate_threshold,
        args.visual_min_gap,
        "autoshot_candidate",
        detector,
        args.autoshot_max_events,
    )
    confident_frames = {item["frame"] for item in confident}
    candidate_only = []
    for item in candidates:
        if item["frame"] in confident_frames:
            continue
        candidate = dict(item)
        candidate["signal_id"] = f"autoshot_candidate_{len(candidate_only) + 1:04d}"
        candidate_only.append(candidate)

    return {
        "status": "ok",
        "detector": detector,
        "model_dir": str(model_dir),
        "device": device,
        "frame_size": {"width": 48, "height": 27},
        "frame_count": int(len(frames)),
        "runtime_seconds": round(time.perf_counter() - started, 3),
        "threshold": args.autoshot_threshold,
        "candidate_threshold": args.autoshot_candidate_threshold,
        "cuts": confident,
        "candidate_cuts": candidate_only,
    }


def detect_autoshot_events(
    video_path: Path,
    media: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    if not args.autoshot:
        return {"status": "disabled", "cuts": [], "candidate_cuts": []}

    os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
    import torch

    model_dir = resolve_autoshot_model_dir(args)
    requested = choose_autoshot_device(torch, args.autoshot_device)
    try:
        return run_autoshot_once(video_path, media, model_dir, requested, args)
    except Exception as exc:
        if args.autoshot_device != "auto" or requested == "cpu":
            raise
        fallback = run_autoshot_once(video_path, media, model_dir, "cpu", args)
        fallback["requested_device"] = requested
        fallback["fallback_reason"] = str(exc)
        return fallback


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
    autoshot = detect_autoshot_events(video_path, media, args)

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
    post_boundary_offset = max(1.0 / fps, min(0.06, args.visual_min_gap / 3.0))
    keyframe_times.extend(min(duration, item["time"] + post_boundary_offset) for item in scene_cuts[:80])
    keyframe_times.extend(
        min(duration, item["time"] + post_boundary_offset) for item in autoshot.get("cuts", [])[:80]
    )
    keyframe_times.extend(
        min(duration, item["time"] + post_boundary_offset)
        for item in autoshot.get("candidate_cuts", [])[:80]
    )
    keyframe_times.extend(
        min(duration, item["time"] + post_boundary_offset) for item in frame_diff_events[:80]
    )
    seen_frames: list[int] = []
    for index, time_value in enumerate(sorted(set(round(t, 3) for t in keyframe_times))):
        frame_number = frame_for_time(time_value, fps)
        if any(abs(frame_number - seen) <= 2 for seen in seen_frames):
            continue
        seen_frames.append(frame_number)
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

    return {
        "tooling": {
            "scene_detector": "pyscenedetect.ContentDetector",
            "learned_shot_detector": autoshot,
            "frame_diff": "opencv mean grayscale absdiff",
        },
        "scene_cuts": scene_cuts,
        "autoshot_cuts": autoshot.get("cuts", []),
        "autoshot_candidate_cuts": autoshot.get("candidate_cuts", []),
        "frame_diff_events": frame_diff_events,
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
    for item in visual_events.get("autoshot_cuts", []):
        add(item.get("time"), item["signal_id"], "visual_autoshot_cut", 1.4)
    for item in visual_events.get("autoshot_candidate_cuts", []):
        add(item.get("time"), item["signal_id"], "visual_autoshot_candidate", 0.9)
    for item in visual_events.get("frame_diff_events", []):
        add(item.get("time"), item["signal_id"], "visual_frame_diff", 1.0)

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
    for beat in grouped:
        time_value = float(beat["time"])
        source_types = sorted({source["kind"] for source in beat["sources"]})
        beat["source_types"] = source_types
        beat["source_signal_ids"] = [source["signal_id"] for source in beat["sources"]]
        beat["near_words"] = word_window(words, time_value)

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


def timed_event_value(item: dict[str, Any]) -> float | None:
    value = seconds(item.get("time"))
    if value is not None:
        return value
    value = seconds(item.get("start"))
    if value is not None:
        return value
    return seconds(item.get("end"))


def nearest_timed_event(
    items: list[dict[str, Any]],
    time_value: float,
    kind: str | None = None,
) -> dict[str, Any] | None:
    best: dict[str, Any] | None = None
    best_offset: float | None = None
    for item in items:
        event_time = timed_event_value(item)
        if event_time is None:
            continue
        offset = event_time - time_value
        if best_offset is None or abs(offset) < abs(best_offset):
            best = item
            best_offset = offset
    if best is None or best_offset is None:
        return None
    result = {
        "signal_id": best.get("signal_id"),
        "kind": kind or best.get("kind"),
        "time": round(float(timed_event_value(best) or 0.0), 4),
        "offset_ms": round(best_offset * 1000.0, 1),
    }
    if "word" in best:
        result["word"] = best["word"]
    if "strength" in best:
        result["strength"] = best["strength"]
    if "db_relative_to_peak" in best:
        result["db_relative_to_peak"] = best["db_relative_to_peak"]
    return result


def nearest_word(words: list[dict[str, Any]], time_value: float) -> dict[str, Any] | None:
    best: dict[str, Any] | None = None
    best_offset: float | None = None
    for word in words:
        start = seconds(word.get("start"))
        end = seconds(word.get("end"))
        if start is None or end is None:
            continue
        center = (start + end) / 2.0
        offset = center - time_value
        if best_offset is None or abs(offset) < abs(best_offset):
            best = word
            best_offset = offset
    if best is None or best_offset is None:
        return None
    return {
        "signal_id": best.get("signal_id"),
        "word": best.get("word"),
        "start": best.get("start"),
        "end": best.get("end"),
        "offset_ms": round(best_offset * 1000.0, 1),
    }


def collect_edit_boundaries(
    media: dict[str, Any],
    visual_events: dict[str, Any],
    merge_window: float,
) -> list[dict[str, Any]]:
    fps = float(media["fps"])
    duration = float(media["duration"])
    points: list[dict[str, Any]] = []

    def add(item: dict[str, Any], kind: str, weight: float) -> None:
        time_value = seconds(item.get("time"))
        if time_value is None:
            return
        clamped = min(max(0.0, time_value), duration)
        points.append(
            {
                "time": clamped,
                "frame": int(item.get("frame") or frame_for_time(clamped, fps)),
                "signal_id": item["signal_id"],
                "kind": kind,
                "weight": weight,
                "score": item.get("score"),
            }
        )

    for item in visual_events.get("scene_cuts", []):
        add(item, "pyscenedetect_scene_cut", 1.0)
    for item in visual_events.get("autoshot_cuts", []):
        add(item, "autoshot_cut", 1.0)
    for item in visual_events.get("autoshot_candidate_cuts", []):
        add(item, "autoshot_candidate_cut", 0.55)
    for item in visual_events.get("frame_diff_events", []):
        add(item, "opencv_frame_diff_spike", 0.7)

    grouped: list[dict[str, Any]] = []
    for point in sorted(points, key=lambda item: (item["time"], item["signal_id"])):
        if not grouped or point["time"] - float(grouped[-1]["time"]) > merge_window:
            grouped.append(
                {
                    "time": point["time"],
                    "frame": point["frame"],
                    "sources": [point],
                }
            )
            continue
        grouped[-1]["sources"].append(point)
        total_weight = sum(float(source["weight"]) for source in grouped[-1]["sources"])
        grouped[-1]["time"] = sum(
            float(source["time"]) * float(source["weight"])
            for source in grouped[-1]["sources"]
        ) / max(total_weight, 1e-9)
        grouped[-1]["frame"] = frame_for_time(float(grouped[-1]["time"]), fps)

    boundaries = []
    for index, group in enumerate(grouped):
        source_kinds = sorted({source["kind"] for source in group["sources"]})
        source_ids = [source["signal_id"] for source in group["sources"]]
        has_scene_or_autoshot = any(
            kind in {"pyscenedetect_scene_cut", "autoshot_cut"} for kind in source_kinds
        )
        has_candidate = "autoshot_candidate_cut" in source_kinds
        has_diff = "opencv_frame_diff_spike" in source_kinds
        agreement_count = len(source_kinds)
        if has_scene_or_autoshot and agreement_count >= 2:
            event_kind = "hard_cut_with_detector_agreement"
            confidence = 0.95
        elif has_scene_or_autoshot:
            event_kind = "hard_cut"
            confidence = 0.82
        elif has_candidate and has_diff:
            event_kind = "candidate_cut_with_frame_diff"
            confidence = 0.68
        elif has_candidate:
            event_kind = "candidate_cut_review"
            confidence = 0.45
        else:
            continue
        boundaries.append(
            {
                "signal_id": f"edit_boundary_{index + 1:04d}",
                "time": round(float(group["time"]), 4),
                "frame": int(group["frame"]),
                "event_kind": event_kind,
                "confidence": round(confidence, 3),
                "source_signal_ids": source_ids,
                "source_kinds": source_kinds,
                "needs_review": confidence < 0.7,
            }
        )
    return boundaries


def build_shot_spans(media: dict[str, Any], boundaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fps = float(media["fps"])
    duration = float(media["duration"])
    ordered = sorted(boundaries, key=lambda item: float(item["time"]))
    spans = []
    start = 0.0
    start_boundary: str | None = None
    for boundary in ordered:
        end = min(max(start, float(boundary["time"])), duration)
        if end - start >= 0.02:
            spans.append(
                {
                    "signal_id": f"edit_span_{len(spans) + 1:04d}",
                    "start": round(start, 4),
                    "end": round(end, 4),
                    "duration": round(end - start, 4),
                    "start_frame": frame_for_time(start, fps),
                    "end_frame": frame_for_time(end, fps),
                    "start_boundary_id": start_boundary,
                    "end_boundary_id": boundary["signal_id"],
                    "end_boundary_kind": boundary["event_kind"],
                    "end_boundary_confidence": boundary["confidence"],
                }
            )
        start = end
        start_boundary = boundary["signal_id"]
    if duration - start >= 0.02:
        spans.append(
            {
                "signal_id": f"edit_span_{len(spans) + 1:04d}",
                "start": round(start, 4),
                "end": round(duration, 4),
                "duration": round(duration - start, 4),
                "start_frame": frame_for_time(start, fps),
                "end_frame": frame_for_time(duration, fps),
                "start_boundary_id": start_boundary,
                "end_boundary_id": "media_end",
                "end_boundary_kind": "media_end",
                "end_boundary_confidence": 1.0,
            }
        )
    return spans


def build_sync_windows(
    events: list[dict[str, Any]],
    transcript: dict[str, Any],
    audio_features: dict[str, Any],
    max_offset_seconds: float,
) -> list[dict[str, Any]]:
    words = transcript.get("words", [])
    audio_events = audio_features.get("events", {})
    timed_audio = []
    for kind, items in [
        ("audio_onset", audio_events.get("onsets", [])),
        ("audio_loudness_peak", audio_events.get("loudness_peaks", [])),
        ("audio_beat", audio_events.get("beats", [])),
    ]:
        for item in items:
            candidate = dict(item)
            candidate["kind"] = kind
            timed_audio.append(candidate)

    sync_windows = []
    for event in events:
        time_value = seconds(event.get("time"))
        if time_value is None:
            continue
        word = nearest_word(words, time_value)
        audio = nearest_timed_event(timed_audio, time_value)
        word_ok = word is not None and abs(float(word["offset_ms"])) <= max_offset_seconds * 1000.0
        audio_ok = audio is not None and abs(float(audio["offset_ms"])) <= max_offset_seconds * 1000.0
        if not word_ok and not audio_ok:
            event["sync_signal_ids"] = []
            continue
        sync = {
            "signal_id": f"sync_{len(sync_windows) + 1:04d}",
            "event_signal_id": event["signal_id"],
            "event_kind": event.get("event_kind"),
            "time": round(time_value, 4),
            "binding_window_ms": int(round(max_offset_seconds * 1000.0)),
            "nearest_word": word if word_ok else None,
            "nearest_audio": audio if audio_ok else None,
        }
        event["sync_signal_ids"] = [sync["signal_id"]]
        sync_windows.append(sync)
    return sync_windows


def build_edit_mechanisms(
    video_path: Path,
    media: dict[str, Any],
    transcript: dict[str, Any],
    audio_features: dict[str, Any],
    visual_events: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    if args.skip_edit_mechanisms:
        return {
            "tooling": {
                "status": "skipped",
                "reason": "--skip-edit-mechanisms",
            },
            "shot_spans": [],
            "boundary_mechanisms": [],
            "sync_windows": [],
        }

    boundaries = collect_edit_boundaries(media, visual_events, args.edit_boundary_merge_window)
    spans = build_shot_spans(media, boundaries)
    sync_windows = build_sync_windows(
        boundaries,
        transcript,
        audio_features,
        args.edit_sync_window,
    )

    return {
        "tooling": {
            "status": "ok",
            "boundary_detectors": [
                "pyscenedetect.ContentDetector",
                "AutoShot.TransNetV2Supernet when enabled",
                "opencv mean grayscale absdiff",
            ],
            "scope": "shot-boundary and shot-span evidence only; within-shot visual effects are not inferred here",
            "no_ocr": True,
        },
        "definitions": {
            "boundary_mechanisms": "merged cut/diff events that explain shot boundaries or review candidates",
            "shot_spans": "shot ranges derived from the merged boundary timeline",
            "sync_windows": "shot-boundary events close to transcript words or audio accents inside the configured binding window",
        },
        "thresholds": {
            "boundary_merge_window_seconds": args.edit_boundary_merge_window,
            "sync_window_seconds": args.edit_sync_window,
        },
        "shot_spans": spans,
        "boundary_mechanisms": boundaries,
        "sync_windows": sync_windows,
    }


def safe_wpm(word_count: int, duration_seconds: float | None) -> float | None:
    if duration_seconds is None or duration_seconds <= 0:
        return None
    return round((word_count / duration_seconds) * 60.0, 3)


def words_in_segment(words: list[dict[str, Any]], start: float, end: float) -> list[dict[str, Any]]:
    return [
        word
        for word in words
        if float(word.get("start", 0.0)) >= start - 0.001
        and float(word.get("end", 0.0)) <= end + 0.001
    ]


def run_speech_metrics(media: dict[str, Any], transcript: dict[str, Any]) -> dict[str, Any]:
    words = transcript.get("words", [])
    duration = float(media.get("duration") or 0.0)
    if not words:
        return {
            "tool": "whisperx_derived",
            "status": "skipped",
            "reason": "no timed words",
            "definitions": {
                "wpm": "words per minute, the speaker/narrator speech rate",
                "bpm": "beats per minute, the dominant rhythmic audio pulse from librosa",
            },
        }

    first_start = float(words[0]["start"])
    last_end = float(words[-1]["end"])
    speech_span = max(0.0, last_end - first_start)
    spoken_word_duration = sum(
        max(0.0, float(word["end"]) - float(word["start"])) for word in words
    )
    word_count = len(words)

    gaps = []
    for previous, current in zip(words, words[1:]):
        gap = max(0.0, float(current["start"]) - float(previous["end"]))
        if gap >= 0.12:
            gaps.append(
                {
                    "after_word_id": previous["signal_id"],
                    "before_word_id": current["signal_id"],
                    "after_word": previous["word"],
                    "before_word": current["word"],
                    "start": round(float(previous["end"]), 4),
                    "end": round(float(current["start"]), 4),
                    "duration": round(gap, 4),
                }
            )

    segment_rates = []
    for segment in transcript.get("segments", []):
        start = float(segment.get("start") or 0.0)
        end = float(segment.get("end") or 0.0)
        segment_words = words_in_segment(words, start, end)
        segment_duration = max(0.0, end - start)
        segment_rates.append(
            {
                "signal_id": f"speech_rate_{len(segment_rates) + 1:04d}",
                "segment_id": segment["signal_id"],
                "start": round(start, 4),
                "end": round(end, 4),
                "duration": round(segment_duration, 4),
                "word_count": len(segment_words),
                "wpm": safe_wpm(len(segment_words), segment_duration),
                "text": segment.get("text", ""),
            }
        )

    return {
        "tool": "whisperx_derived",
        "status": "ok",
        "definitions": {
            "wpm": "words per minute, the speaker/narrator speech rate from WhisperX word timings",
            "bpm": "beats per minute, the dominant rhythmic audio pulse from librosa over the mixed audio",
        },
        "overall": {
            "word_count": word_count,
            "media_duration_seconds": round(duration, 4),
            "speech_span_seconds": round(speech_span, 4),
            "spoken_word_duration_seconds": round(spoken_word_duration, 4),
            "wpm_over_media_duration": safe_wpm(word_count, duration),
            "wpm_first_word_to_last_word": safe_wpm(word_count, speech_span),
            "articulation_wpm_word_durations_only": safe_wpm(word_count, spoken_word_duration),
        },
        "pauses": {
            "min_pause_seconds": 0.12,
            "count": len(gaps),
            "duration_summary": stats([item["duration"] for item in gaps]),
            "notable_pauses": sorted(gaps, key=lambda item: item["duration"], reverse=True)[:12],
        },
        "segment_rates": segment_rates,
    }


def relative_level(value: float | None, values: list[float]) -> str:
    if value is None or len(values) < 3:
        return "unknown"
    ordered = sorted(values)
    low = ordered[max(0, round((len(ordered) - 1) * 0.25))]
    high = ordered[min(len(ordered) - 1, round((len(ordered) - 1) * 0.75))]
    if value <= low:
        return "low"
    if value >= high:
        return "high"
    return "mid"


def numeric_value(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def add_relative_delivery_tags(rows: list[dict[str, Any]]) -> None:
    wpm_values = [
        value
        for value in (numeric_value(row.get("wpm")) for row in rows)
        if value is not None
    ]
    pitch_values = [
        value
        for value in (
            numeric_value(row.get("features", {}).get("F0semitoneFrom27.5Hz_sma3nz_amean"))
            for row in rows
        )
        if value is not None
    ]
    pitch_range_values = [
        value
        for value in (
            numeric_value(row.get("features", {}).get("F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2"))
            for row in rows
        )
        if value is not None
    ]
    loudness_values = [
        value
        for value in (
            numeric_value(row.get("features", {}).get("loudness_sma3_amean")) for row in rows
        )
        if value is not None
    ]
    loudness_range_values = [
        value
        for value in (
            numeric_value(row.get("features", {}).get("loudness_sma3_pctlrange0-2"))
            for row in rows
        )
        if value is not None
    ]

    for row in rows:
        features = row.get("features", {})
        wpm = numeric_value(row.get("wpm"))
        pitch = numeric_value(features.get("F0semitoneFrom27.5Hz_sma3nz_amean"))
        pitch_range = numeric_value(features.get("F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2"))
        loudness = numeric_value(features.get("loudness_sma3_amean"))
        loudness_range = numeric_value(features.get("loudness_sma3_pctlrange0-2"))
        relative = {
            "speech_rate": relative_level(wpm, wpm_values),
            "pitch": relative_level(pitch, pitch_values),
            "pitch_range": relative_level(pitch_range, pitch_range_values),
            "loudness": relative_level(loudness, loudness_values),
            "loudness_range": relative_level(loudness_range, loudness_range_values),
        }
        tags = []
        if wpm is not None:
            if wpm >= 300:
                tags.append("very_fast_speech")
            elif wpm >= 250:
                tags.append("fast_speech")
        for key, value in relative.items():
            if value == "high":
                tags.append(f"high_relative_{key}")
            elif value == "low":
                tags.append(f"low_relative_{key}")
        row["relative_delivery"] = relative
        row["delivery_tags"] = tags


def run_prosody_segments(
    audio_path: Path,
    media: dict[str, Any],
    transcript: dict[str, Any],
    speech_metrics: dict[str, Any],
) -> dict[str, Any]:
    segments = transcript.get("segments", [])
    words = transcript.get("words", [])
    if not segments:
        return {
            "tool": "opensmile",
            "feature_set": "eGeMAPSv02",
            "feature_level": "Functionals_by_transcript_segment",
            "status": "skipped",
            "reason": "no transcript segments",
            "segments": [],
        }

    try:
        import opensmile
        import soundfile as sf

        audio, sample_rate = sf.read(str(audio_path), dtype="float32", always_2d=False)
        if getattr(audio, "ndim", 1) > 1:
            audio = audio.mean(axis=1)
        smile = opensmile.Smile(
            feature_set=opensmile.FeatureSet.eGeMAPSv02,
            feature_level=opensmile.FeatureLevel.Functionals,
        )
    except Exception as exc:
        return {
            "tool": "opensmile",
            "feature_set": "eGeMAPSv02",
            "feature_level": "Functionals_by_transcript_segment",
            "status": "skipped",
            "reason": str(exc),
            "segments": [],
        }

    fps = float(media["fps"])
    speech_rates = {
        item.get("segment_id"): item for item in speech_metrics.get("segment_rates", [])
    }
    rows: list[dict[str, Any]] = []
    for segment in segments:
        start = float(segment.get("start") or 0.0)
        end = float(segment.get("end") or 0.0)
        duration = max(0.0, end - start)
        segment_words = words_in_segment(words, start, end)
        rate = speech_rates.get(segment.get("signal_id"), {})
        row = {
            "signal_id": f"prosody_seg_{len(rows) + 1:04d}",
            "segment_id": segment.get("signal_id"),
            "start": round(start, 4),
            "end": round(end, 4),
            "duration": round(duration, 4),
            "start_frame": frame_for_time(start, fps),
            "end_frame": frame_for_time(end, fps),
            "word_count": len(segment_words),
            "word_ids": [word.get("signal_id") for word in segment_words],
            "wpm": rate.get("wpm") if rate else safe_wpm(len(segment_words), duration),
            "text": segment.get("text", ""),
            "features": {},
        }
        if duration < 0.12:
            row["status"] = "skipped"
            row["reason"] = "segment_too_short_for_stable_prosody"
            rows.append(row)
            continue

        start_sample = max(0, int(round(start * sample_rate)))
        end_sample = min(len(audio), int(round(end * sample_rate)))
        if end_sample <= start_sample:
            row["status"] = "skipped"
            row["reason"] = "empty_audio_slice"
            rows.append(row)
            continue

        try:
            frame = smile.process_signal(audio[start_sample:end_sample], sample_rate)
            if frame.empty:
                row["status"] = "empty"
            else:
                row["status"] = "ok"
                row["features"] = selected_features(
                    finite_feature_dict(frame.iloc[0]),
                    PROSODY_SEGMENT_KEYS,
                )
        except Exception as exc:
            row["status"] = "skipped"
            row["reason"] = str(exc)
        rows.append(row)

    add_relative_delivery_tags(rows)
    return {
        "tool": "opensmile",
        "feature_set": "eGeMAPSv02",
        "feature_level": "Functionals_by_transcript_segment",
        "status": "ok" if any(row.get("status") == "ok" for row in rows) else "skipped",
        "definitions": {
            "scope": "Each row aggregates acoustic functionals over one WhisperX transcript segment.",
            "wpm": "words per minute from WhisperX word timings for the same segment",
            "relative_delivery": "low/mid/high bucket relative to other transcript segments in this Exemplar",
        },
        "segments": rows,
    }


def transcript_text(transcript: dict[str, Any]) -> str:
    words = [str(item.get("word") or "").strip() for item in transcript.get("words", [])]
    return re.sub(r"\s+", " ", " ".join(words)).strip()


def render_signals_markdown(
    video_path: Path,
    media: dict[str, Any],
    transcript: dict[str, Any],
    speech_metrics: dict[str, Any],
    audio_features: dict[str, Any],
    prosody: dict[str, Any],
    prosody_segments: dict[str, Any],
    visual_events: dict[str, Any],
    beats: dict[str, Any],
    edit_mechanisms: dict[str, Any],
) -> str:
    fps = float(media["fps"])
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
    lines.append(f"| Resolve timecode timebase | {timebase_for_fps(fps)} fps, `MM:SS:FF` |")
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
                f"| {word['signal_id']} | {fmt_range(float(word['start']), float(word['end']), fps)} | "
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
                f"| {segment['signal_id']} | {fmt_range(float(segment['start']), float(segment['end']), fps)} | "
                f"{segment['start_frame']}-{segment['end_frame']} | {md_cell(segment['text'])} |"
            )
        lines.append("")

    lines.append("## Speech Pace")
    lines.append("")
    lines.append("WPM is speech pace: how fast the speaker/narrator is talking, derived from WhisperX word timings.")
    lines.append("BPM is audio rhythm: the dominant beat/pulse estimated from the mixed audio by librosa, often music or rhythmic edit/SFX energy when present.")
    lines.append("")
    if speech_metrics.get("status") == "ok":
        overall = speech_metrics.get("overall", {})
        lines.append("| metric | value | meaning |")
        lines.append("|---|---:|---|")
        lines.append(
            f"| speech_rate_wpm_media_duration | {overall.get('wpm_over_media_duration')} | "
            "spoken words divided by full video duration |"
        )
        lines.append(
            f"| speech_rate_wpm_first_to_last_word | {overall.get('wpm_first_word_to_last_word')} | "
            "spoken words divided by first-word to last-word span |"
        )
        lines.append(
            f"| articulation_wpm_word_durations_only | {overall.get('articulation_wpm_word_durations_only')} | "
            "spoken words divided by summed word durations; excludes pauses |"
        )
        lines.append(
            f"| notable_pause_count | {speech_metrics.get('pauses', {}).get('count')} | "
            f"gaps >= {speech_metrics.get('pauses', {}).get('min_pause_seconds')}s between timed words |"
        )
        lines.append("")
        segment_rates = [item for item in speech_metrics.get("segment_rates", []) if item.get("wpm") is not None]
        if segment_rates:
            lines.append("| speech_rate_id | segment_id | time | words | WPM | text |")
            lines.append("|---|---|---:|---:|---:|---|")
            for item in segment_rates:
                lines.append(
                    f"| {item['signal_id']} | {item['segment_id']} | "
                    f"{fmt_range(float(item['start']), float(item['end']), fps)} | "
                    f"{item['word_count']} | {item['wpm']} | {md_cell(item.get('text', ''))} |"
                )
            lines.append("")
    else:
        lines.append(f"- status: {speech_metrics.get('status')}")
        if speech_metrics.get("reason"):
            lines.append(f"- reason: {speech_metrics['reason']}")
        lines.append("")

    lines.append("## Audio Signals")
    lines.append("")
    lines.append(f"Estimated audio tempo: {audio_features.get('tempo_bpm')} BPM")
    lines.append("BPM here is not speech speed; it is the dominant rhythmic pulse of the mixed audio.")
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
            f"| {item['signal_id']} | onset | {fmt_time(float(item['time']), fps)} | {item['frame']} | strength {item.get('strength')} |"
        )
    for item in audio_features.get("events", {}).get("loudness_peaks", [])[:20]:
        lines.append(
            f"| {item['signal_id']} | loudness_peak | {fmt_time(float(item['time']), fps)} | {item['frame']} | "
            f"rms {item.get('rms')}, dB {item.get('db_relative_to_peak')} |"
        )
    for item in audio_features.get("events", {}).get("silences", [])[:80]:
        lines.append(
            f"| {item['signal_id']} | silence | {fmt_range(float(item['start']), float(item['end']), fps)} | "
            f"{item['start_frame']}-{item['end_frame']} | low RMS |"
        )
    lines.append("")

    lines.append("## Prosody Summary")
    lines.append("")
    lines.append(
        "Global openSMILE functionals summarize the full voice track; use `prosody_segments.json` for time-aligned delivery evidence."
    )
    lines.append("")
    if prosody.get("status") == "ok":
        for key in PROSODY_SUMMARY_KEYS:
            if key in prosody.get("features", {}):
                lines.append(f"- `{key}`: {prosody['features'][key]}")
    else:
        lines.append(f"- status: {prosody.get('status')}")
        if prosody.get("reason"):
            lines.append(f"- reason: {prosody['reason']}")
    lines.append("")

    lines.append("## Prosody Segments")
    lines.append("")
    lines.append(
        "These rows align voice-delivery features to transcript segments. They are not word-level pitch tracks, but they can identify where speech is faster, louder, higher-pitched, or more varied relative to the rest of the Exemplar."
    )
    lines.append("")
    if prosody_segments.get("status") == "ok" and prosody_segments.get("segments"):
        lines.append(
            "| prosody_id | segment_id | time | frames | words | WPM | pitch_mean | pitch_range | loudness_mean | loudness_range | tags | text |"
        )
        lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|")
        for item in prosody_segments.get("segments", []):
            features = item.get("features", {})
            lines.append(
                f"| {item['signal_id']} | {item.get('segment_id')} | "
                f"{fmt_range(float(item['start']), float(item['end']), fps)} | "
                f"{item.get('start_frame')}-{item.get('end_frame')} | "
                f"{item.get('word_count')} | {item.get('wpm')} | "
                f"{features.get('F0semitoneFrom27.5Hz_sma3nz_amean', '')} | "
                f"{features.get('F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2', '')} | "
                f"{features.get('loudness_sma3_amean', '')} | "
                f"{features.get('loudness_sma3_pctlrange0-2', '')} | "
                f"{md_cell(', '.join(item.get('delivery_tags', [])))} | "
                f"{md_cell(item.get('text', ''))} |"
            )
        lines.append("")
    else:
        lines.append(f"- status: {prosody_segments.get('status')}")
        if prosody_segments.get("reason"):
            lines.append(f"- reason: {prosody_segments['reason']}")
        lines.append("")

    lines.append("## Visual Signals")
    lines.append("")
    lines.append("| signal_id | kind | time | frame | detail |")
    lines.append("|---|---|---:|---:|---|")
    for item in visual_events.get("scene_cuts", [])[:80]:
        lines.append(
            f"| {item['signal_id']} | scene_cut | {fmt_time(float(item['time']), fps)} | {item['frame']} | PySceneDetect content cut |"
        )
    for item in visual_events.get("autoshot_cuts", [])[:80]:
        lines.append(
            f"| {item['signal_id']} | autoshot_cut | {fmt_time(float(item['time']), fps)} | {item['frame']} | "
            f"score {item.get('score')} |"
        )
    for item in visual_events.get("autoshot_candidate_cuts", [])[:80]:
        lines.append(
            f"| {item['signal_id']} | autoshot_candidate | {fmt_time(float(item['time']), fps)} | {item['frame']} | "
            f"low-threshold score {item.get('score')} |"
        )
    for item in visual_events.get("frame_diff_events", [])[:80]:
        lines.append(
            f"| {item['signal_id']} | frame_diff | {fmt_time(float(item['time']), fps)} | {item['frame']} | score {item.get('score')} |"
        )
    lines.append("")

    lines.append("## Candidate Beats")
    lines.append("")
    lines.append("| beat_id | time | frame | source_signal_ids | source_types | nearby words |")
    lines.append("|---|---:|---:|---|---|---|")
    for beat in beats.get("beats", []):
        nearby = " ".join(word["word"] for word in beat.get("near_words", []))
        lines.append(
            f"| {beat['signal_id']} | {fmt_time(float(beat['time']), fps)} | {beat['frame']} | "
            f"{md_cell(', '.join(beat.get('source_signal_ids', [])))} | "
            f"{md_cell(', '.join(beat.get('source_types', [])))} | "
            f"{md_cell(nearby)} |"
        )
    lines.append("")

    lines.append("## Shot Boundary Signals (No OCR)")
    lines.append("")
    lines.append(
        "These signals estimate cut boundaries and shot spans from detector timing only. They do not read text or infer within-shot visual effects such as punch-ins, zooms, pans, split screens, or VFX."
    )
    lines.append("")
    tooling = edit_mechanisms.get("tooling", {})
    lines.append(f"- status: {tooling.get('status', 'ok')}")
    if tooling.get("scope"):
        lines.append(f"- scope: {tooling['scope']}")
    lines.append("")

    if edit_mechanisms.get("shot_spans"):
        lines.append("### Shot Spans")
        lines.append("")
        lines.append("| span_id | time | frames | boundary | duration |")
        lines.append("|---|---:|---:|---|---:|")
        for span in edit_mechanisms.get("shot_spans", [])[:80]:
            lines.append(
                f"| {span['signal_id']} | {fmt_range(float(span['start']), float(span['end']), fps)} | "
                f"{span['start_frame']}-{span['end_frame']} | "
                f"{md_cell(str(span.get('start_boundary_id') or 'media_start'))}->{md_cell(str(span.get('end_boundary_id')))} | "
                f"{fmt_frame_duration(int(span['start_frame']), int(span['end_frame']), fps)} |"
            )
        lines.append("")

    if edit_mechanisms.get("boundary_mechanisms"):
        lines.append("### Boundary Mechanisms")
        lines.append("")
        lines.append("| signal_id | kind | time | frame | source_signal_ids | confidence | review |")
        lines.append("|---|---|---:|---:|---|---:|---|")
        for item in edit_mechanisms.get("boundary_mechanisms", [])[:100]:
            lines.append(
                f"| {item['signal_id']} | {item.get('event_kind')} | {fmt_time(float(item['time']), fps)} | "
                f"{item['frame']} | {md_cell(', '.join(item.get('source_signal_ids', [])))} | "
                f"{item.get('confidence')} | {item.get('needs_review')} |"
            )
        lines.append("")

    if edit_mechanisms.get("sync_windows"):
        lines.append("### Boundary/Audio/Word Sync Windows")
        lines.append("")
        lines.append("| signal_id | event | time | nearest_word | nearest_audio |")
        lines.append("|---|---|---:|---|---|")
        for item in edit_mechanisms.get("sync_windows", [])[:100]:
            word = item.get("nearest_word") or {}
            audio = item.get("nearest_audio") or {}
            word_text = ""
            if word:
                word_text = f"{word.get('signal_id')} {word.get('word')} ({word.get('offset_ms')}ms)"
            audio_text = ""
            if audio:
                audio_text = (
                    f"{audio.get('signal_id')} {audio.get('kind')} "
                    f"({audio.get('offset_ms')}ms)"
                )
            lines.append(
                f"| {item['signal_id']} | {item.get('event_signal_id')} {item.get('event_kind')} | "
                f"{fmt_time(float(item['time']), fps)} | {md_cell(word_text)} | {md_cell(audio_text)} |"
            )
        lines.append("")

    lines.append("## Gemini Use")
    lines.append("")
    lines.append("- Do not invent timestamps.")
    lines.append("- Do not create a Beat Sheet from scratch.")
    lines.append("- Treat the tables above as the timing source of truth.")
    lines.append("- Gemini may merge, label, and explain candidate beats, but output beats should cite signal IDs.")
    lines.append("- Use `edit_boundary_*`, `edit_span_*`, and `sync_*` when making claims about cuts, shot spans, pacing, or boundary/audio synchronization.")
    lines.append("- Do not use this signal pack as evidence for within-shot visual effects. Ask Gemini to visually inspect each shot span for punch-ins, zoom animations, split-screen layout, overlays, or VFX and mark those claims as semantic visual review.")
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
    parser.add_argument("--scene-threshold", type=float, default=30.0)
    parser.add_argument("--diff-percentile", type=float, default=98.5)
    parser.add_argument("--min-diff-score", type=float, default=0.06)
    parser.add_argument("--visual-min-gap", type=float, default=0.18)
    parser.add_argument(
        "--content-profile",
        choices=["auto", "short-form", "long-form"],
        default="auto",
        help=(
            "auto enables AutoShot for vertical social-length videos; short-form "
            "forces it on; long-form keeps it off unless --autoshot is set"
        ),
    )
    parser.add_argument(
        "--short-form-max-duration",
        type=float,
        default=SHORT_FORM_MAX_DURATION_SECONDS,
        help="maximum duration, in seconds, for auto short-form detection",
    )
    autoshot_group = parser.add_mutually_exclusive_group()
    autoshot_group.add_argument(
        "--autoshot",
        dest="autoshot",
        action="store_true",
        help="force the AutoShot learned short-video shot detector on",
    )
    autoshot_group.add_argument(
        "--no-autoshot",
        dest="autoshot",
        action="store_false",
        help="force AutoShot off even for short-form content",
    )
    parser.set_defaults(autoshot=None)
    parser.add_argument("--autoshot-model-dir", help="directory containing ckpt_0_200_0.pth and AutoShot model files")
    parser.add_argument("--autoshot-download-kaggle", action="store_true", help="download/use the public Kaggle mirror if no local AutoShot model is found")
    parser.add_argument("--autoshot-device", choices=["auto", "mps", "cpu"], default="auto")
    parser.add_argument("--autoshot-threshold", type=float, default=0.296)
    parser.add_argument("--autoshot-candidate-threshold", type=float, default=0.05)
    parser.add_argument("--autoshot-max-events", type=int, default=160)
    parser.add_argument("--merge-window", type=float, default=0.18)
    parser.add_argument("--skip-edit-mechanisms", action="store_true")
    parser.add_argument("--edit-boundary-merge-window", type=float, default=0.12)
    parser.add_argument("--edit-sync-window", type=float, default=0.25)
    parser.add_argument(
        "--reuse-existing",
        action="store_true",
        help="reuse existing JSON signal files in the output folder when present; edit_mechanisms.json is still regenerated",
    )
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

    media_path = out_dir / "media.json"
    transcript_path = out_dir / "transcript.words.json"
    speech_metrics_path = out_dir / "speech_metrics.json"
    audio_features_path = out_dir / "audio_features.json"
    prosody_path = out_dir / "prosody_features.json"
    prosody_segments_path = out_dir / "prosody_segments.json"
    visual_events_path = out_dir / "visual_events.json"
    beats_path = out_dir / "candidate_beats.json"
    edit_mechanisms_path = out_dir / "edit_mechanisms.json"

    if args.reuse_existing and media_path.exists() and not args.force:
        media = read_json(media_path)
        print(f"reused {media_path}")
    else:
        media = media_metadata(video_path)
    media["timecode_timebase_fps"] = timebase_for_fps(float(media["fps"]))
    media["duration_timecode"] = timecode_for_time(float(media["duration"]), float(media["fps"]))
    autoshot_enabled, autoshot_reason, short_form_detected = resolve_autoshot_setting(args, media)
    args.autoshot = autoshot_enabled
    media["ingest_profile"] = {
        "content_profile": args.content_profile,
        "short_form_detected": short_form_detected,
        "short_form_max_duration_seconds": args.short_form_max_duration,
        "autoshot_enabled": autoshot_enabled,
        "autoshot_reason": autoshot_reason,
    }
    write_json(media_path, media)
    print(f"wrote {media_path}")
    print(
        "AutoShot {state} ({reason})".format(
            state="enabled" if autoshot_enabled else "disabled",
            reason=autoshot_reason,
        )
    )

    asr_audio, analysis_audio = extract_audio(video_path, work_dir)

    if args.reuse_existing and transcript_path.exists() and not args.force:
        transcript = read_json(transcript_path)
        print(f"reused {transcript_path}")
    elif args.skip_transcript:
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
    add_timecodes(transcript, float(media["fps"]))
    write_json(transcript_path, transcript)
    print(f"wrote {transcript_path}")

    if args.reuse_existing and speech_metrics_path.exists() and not args.force:
        speech_metrics = read_json(speech_metrics_path)
        print(f"reused {speech_metrics_path}")
    else:
        speech_metrics = run_speech_metrics(media, transcript)
    add_timecodes(speech_metrics, float(media["fps"]))
    write_json(speech_metrics_path, speech_metrics)
    print(f"wrote {speech_metrics_path}")

    if args.reuse_existing and audio_features_path.exists() and not args.force:
        audio_features = read_json(audio_features_path)
        print(f"reused {audio_features_path}")
    else:
        audio_features = run_audio_features(analysis_audio, float(media["fps"]), float(media["duration"]))
    add_timecodes(audio_features, float(media["fps"]))
    write_json(audio_features_path, audio_features)
    print(f"wrote {audio_features_path}")

    if args.reuse_existing and prosody_path.exists() and not args.force:
        prosody = read_json(prosody_path)
        print(f"reused {prosody_path}")
    else:
        prosody = (
            {"tool": "opensmile", "feature_set": "eGeMAPSv02", "status": "skipped"}
            if args.skip_prosody
            else run_prosody(analysis_audio)
        )
    add_timecodes(prosody, float(media["fps"]))
    write_json(prosody_path, prosody)
    print(f"wrote {prosody_path}")

    if args.reuse_existing and prosody_segments_path.exists() and not args.force:
        prosody_segments = read_json(prosody_segments_path)
        print(f"reused {prosody_segments_path}")
    else:
        prosody_segments = (
            {
                "tool": "opensmile",
                "feature_set": "eGeMAPSv02",
                "feature_level": "Functionals_by_transcript_segment",
                "status": "skipped",
                "reason": "--skip-prosody",
                "segments": [],
            }
            if args.skip_prosody
            else run_prosody_segments(analysis_audio, media, transcript, speech_metrics)
        )
    add_timecodes(prosody_segments, float(media["fps"]))
    write_json(prosody_segments_path, prosody_segments)
    print(f"wrote {prosody_segments_path}")

    if args.reuse_existing and visual_events_path.exists() and not args.force:
        visual_events = read_json(visual_events_path)
        print(f"reused {visual_events_path}")
    else:
        visual_events = detect_visual_events(video_path, media, out_dir, args)
    add_timecodes(visual_events, float(media["fps"]))
    write_json(visual_events_path, visual_events)
    print(f"wrote {visual_events_path}")

    if args.reuse_existing and beats_path.exists() and not args.force:
        beats = read_json(beats_path)
        print(f"reused {beats_path}")
    else:
        beats = build_candidate_beats(
            media,
            transcript,
            audio_features,
            visual_events,
            merge_window=args.merge_window,
        )
    add_timecodes(beats, float(media["fps"]))
    write_json(beats_path, beats)
    print(f"wrote {beats_path}")

    edit_mechanisms = build_edit_mechanisms(
        video_path,
        media,
        transcript,
        audio_features,
        visual_events,
        args,
    )
    add_timecodes(edit_mechanisms, float(media["fps"]))
    write_json(edit_mechanisms_path, edit_mechanisms)
    print(f"wrote {edit_mechanisms_path}")

    signals_md = render_signals_markdown(
        video_path,
        media,
        transcript,
        speech_metrics,
        audio_features,
        prosody,
        prosody_segments,
        visual_events,
        beats,
        edit_mechanisms,
    )
    (out_dir / "signals_for_gemini.md").write_text(signals_md + "\n", encoding="utf-8")
    print(f"wrote {out_dir / 'signals_for_gemini.md'}")
    print(f"\nsignal pack: {out_dir}")


if __name__ == "__main__":
    main()
