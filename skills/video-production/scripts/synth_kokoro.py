#!/usr/bin/env python3
"""Synthesize segmented narration with Kokoro TTS.

Inputs may be a JSON segments file or a plain text file. Outputs are per-segment WAVs,
a combined voice_raw.wav, a loudness-normalized voice.wav, and timings.json.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path
from typing import Any, Iterable

DEFAULT_SAMPLE_RATE = 24000
REEXEC_FLAG = "__VIDEO_PRODUCTION_KOKORO_REEXEC"

INSTALL_MESSAGE = """Kokoro TTS is not available.
Install/configure one of these portable options:
  1. Install Kokoro in the active Python environment, e.g. `python -m pip install kokoro` plus system espeak-ng.
  2. Set KOKORO_PYTHON=/path/to/python for an environment where `import kokoro` works.
  3. Set KOKORO_TTS_DIR=/path/to/kokoro/repo to prepend that repo to PYTHONPATH.
Optional env: KOKORO_VOICE=af_heart, KOKORO_LANG_CODE=a.
""".strip()


def env_path(name: str) -> Path | None:
    value = os.environ.get(name)
    return Path(value).expanduser() if value else None


def maybe_reexec_with_kokoro_python() -> None:
    requested = env_path("KOKORO_PYTHON")
    if not requested or os.environ.get(REEXEC_FLAG):
        return
    # Do not resolve symlinks here. Virtualenv interpreters are often symlinks to
    # the system Python binary, but executing the venv path is what activates the
    # venv's sys.prefix/site-packages. Comparing resolved paths would incorrectly
    # skip re-exec and then fail to import Kokoro.
    current = Path(sys.executable).absolute()
    target = requested.absolute()
    if str(current) == str(target):
        return
    if not target.exists():
        raise SystemExit(f"KOKORO_PYTHON points to a missing executable: {target}\n{INSTALL_MESSAGE}")
    env = os.environ.copy()
    env[REEXEC_FLAG] = "1"
    os.execve(str(target), [str(target), str(Path(__file__).resolve()), *sys.argv[1:]], env)


def configure_import_path() -> None:
    kokoro_dir = env_path("KOKORO_TTS_DIR")
    if kokoro_dir:
        resolved = kokoro_dir.resolve()
        sys.path.insert(0, str(resolved))
        src = resolved / "src"
        if src.exists():
            sys.path.insert(0, str(src))


def require_binary(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"Required executable not found: {name}. Install ffmpeg/ffprobe and retry.")
    return path


def import_kokoro():
    maybe_reexec_with_kokoro_python()
    configure_import_path()
    try:
        from kokoro import KPipeline  # type: ignore
    except Exception as exc:  # pragma: no cover - environment dependent
        raise SystemExit(f"{INSTALL_MESSAGE}\n\nImport error: {exc}") from exc
    return KPipeline


def slugify(text: str, fallback: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return (slug or fallback)[:48].strip("-") or fallback


def read_segments(path: Path) -> list[dict[str, str]]:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        raise SystemExit(f"No segment text found in {path}")

    data: Any | None = None
    if path.suffix.lower() == ".json":
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc

    if data is None:
        chunks = [p.strip() for p in re.split(r"\n\s*\n", raw) if p.strip()]
        if len(chunks) == 1:
            chunks = [line.strip() for line in raw.splitlines() if line.strip()]
        return [
            {"id": f"segment-{i:03d}", "text": text}
            for i, text in enumerate(chunks, start=1)
        ]

    if isinstance(data, dict):
        candidates = data.get("segments") or data.get("scenes") or data.get("narration")
        if candidates is None:
            raise SystemExit("JSON object must contain a `segments`, `scenes`, or `narration` list")
    else:
        candidates = data

    if not isinstance(candidates, list) or not candidates:
        raise SystemExit("Segments JSON must contain a non-empty list")

    segments: list[dict[str, str]] = []
    for i, item in enumerate(candidates, start=1):
        if isinstance(item, str):
            text = item.strip()
            seg_id = f"segment-{i:03d}"
        elif isinstance(item, dict):
            text = str(item.get("text") or item.get("narration") or item.get("voiceover") or "").strip()
            seg_id = str(item.get("id") or item.get("slug") or item.get("name") or f"segment-{i:03d}")
        else:
            raise SystemExit(f"Segment {i} must be a string or object")
        if not text:
            raise SystemExit(f"Segment {i} has no text")
        segments.append({"id": slugify(seg_id, f"segment-{i:03d}"), "text": text})
    return segments


def default_output_dir(input_path: Path) -> Path:
    if input_path.parent.name == "src":
        return input_path.parent.parent / "audio"
    root = env_path("VIDEO_PRODUCTION_ROOT")
    if root and (root / "current").exists():
        return root / "current" / "audio"
    return Path.cwd() / "audio"


def to_float_list(audio: Any) -> list[float]:
    # Kokoro returns a torch Tensor in common installs, but numpy/list outputs also work.
    if hasattr(audio, "detach"):
        audio = audio.detach().cpu().numpy()
    elif hasattr(audio, "cpu"):
        audio = audio.cpu().numpy()
    if hasattr(audio, "tolist"):
        audio = audio.tolist()
    if isinstance(audio, (int, float)):
        return [float(audio)]
    return [float(x) for x in audio]


def write_pcm16_wav(path: Path, samples: Iterable[float], sample_rate: int = DEFAULT_SAMPLE_RATE) -> int:
    values = bytearray()
    count = 0
    for sample in samples:
        if math.isnan(sample) or math.isinf(sample):
            sample = 0.0
        sample = max(-1.0, min(1.0, float(sample)))
        pcm = int(round(sample * 32767.0))
        values.extend(pcm.to_bytes(2, byteorder="little", signed=True))
        count += 1
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(values)
    return count


def extract_audio(item: Any) -> Any:
    """Extract audio from Kokoro outputs across common API versions."""
    # Newer Kokoro returns KPipeline.Result with output.audio.
    output = getattr(item, "output", None)
    if output is not None and hasattr(output, "audio"):
        return output.audio
    if hasattr(item, "audio"):
        return item.audio
    # Older examples commonly yield tuples like (graphemes, phonemes, audio).
    if isinstance(item, tuple):
        return item[-1]
    return item


def synth_segment(pipeline: Any, text: str, voice: str, speed: float, lang_code: str) -> list[float]:
    kwargs = {"voice": voice, "speed": speed}
    generator = pipeline(text, **kwargs)
    samples: list[float] = []
    for item in generator:
        audio = extract_audio(item)
        samples.extend(to_float_list(audio))
    if not samples:
        raise SystemExit("Kokoro returned no audio for a segment")
    return samples


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wf:
        return wf.getnframes() / float(wf.getframerate())


def combine_wavs(paths: list[Path], out: Path, gap_ms: int) -> list[float]:
    starts: list[float] = []
    current = 0.0
    gap_frames = 0
    params = None
    with wave.open(str(out), "wb") as dest:
        for i, path in enumerate(paths):
            with wave.open(str(path), "rb") as src:
                src_params = src.getparams()
                if params is None:
                    params = src_params
                    dest.setparams(src_params)
                    gap_frames = int(src.getframerate() * gap_ms / 1000)
                elif src_params[:3] != params[:3]:
                    raise SystemExit(f"WAV format mismatch while combining: {path}")
                starts.append(current)
                frames = src.readframes(src.getnframes())
                dest.writeframes(frames)
                current += src.getnframes() / float(src.getframerate())
                if gap_frames and i < len(paths) - 1:
                    dest.writeframes(b"\x00" * gap_frames * src.getnchannels() * src.getsampwidth())
                    current += gap_frames / float(src.getframerate())
    return starts


def normalize(raw: Path, out: Path) -> None:
    require_binary("ffmpeg")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(raw),
            "-af",
            "loudnorm=I=-16:TP=-1.5:LRA=11",
            str(out),
        ],
        check=True,
    )


def build_timings(
    segments: list[dict[str, str]],
    wavs: list[Path],
    starts: list[float],
    out_dir: Path,
    voice: str,
    lang_code: str,
    speed: float,
    gap_ms: int,
) -> dict[str, Any]:
    entries = []
    for i, (segment, wav, start) in enumerate(zip(segments, wavs, starts), start=1):
        duration = wav_duration(wav)
        entries.append(
            {
                "index": i,
                "id": segment["id"],
                "text": segment["text"],
                "wav": str(wav),
                "start": round(start, 3),
                "duration": round(duration, 3),
                "end": round(start + duration, 3),
            }
        )
    total = wav_duration(out_dir / "voice_raw.wav")
    return {
        "voice_name": voice,
        "lang_code": lang_code,
        "speed": speed,
        "gap_ms": gap_ms,
        "sample_rate": DEFAULT_SAMPLE_RATE,
        "voice_raw": str(out_dir / "voice_raw.wav"),
        "voice_wav": str(out_dir / "voice.wav"),
        "total_duration": round(total, 3),
        "segments": entries,
    }


def check_environment() -> None:
    require_binary("ffmpeg")
    require_binary("ffprobe")
    import_kokoro()
    print("Kokoro, ffmpeg, and ffprobe are available.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthesize Kokoro narration for video-production segments")
    parser.add_argument("segments", nargs="?", help="segments.json or plain text file")
    parser.add_argument("--out", help="Output audio directory; defaults to job audio/ when input is under src/")
    parser.add_argument("--voice", default=os.environ.get("KOKORO_VOICE", "af_heart"))
    parser.add_argument("--lang-code", default=os.environ.get("KOKORO_LANG_CODE", "a"), help="Kokoro language code, default: a")
    parser.add_argument("--speed", type=float, default=float(os.environ.get("KOKORO_SPEED", "1.0")))
    parser.add_argument("--gap-ms", type=int, default=120, help="Silence inserted between segments in voice_raw.wav")
    parser.add_argument("--check", action="store_true", help="Validate Kokoro/ffmpeg availability and exit")
    args = parser.parse_args()

    if args.check:
        check_environment()
        return
    if not args.segments:
        parser.error("segments file is required unless --check is used")

    require_binary("ffmpeg")
    require_binary("ffprobe")
    KPipeline = import_kokoro()

    input_path = Path(args.segments).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Segments file not found: {input_path}")
    segments = read_segments(input_path)
    out_dir = Path(args.out).expanduser().resolve() if args.out else default_output_dir(input_path).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    per_segment = out_dir / "segments"
    per_segment.mkdir(parents=True, exist_ok=True)

    pipeline = KPipeline(lang_code=args.lang_code)
    wavs: list[Path] = []
    for i, segment in enumerate(segments, start=1):
        wav = per_segment / f"{i:03d}-{segment['id']}.wav"
        samples = synth_segment(pipeline, segment["text"], args.voice, args.speed, args.lang_code)
        write_pcm16_wav(wav, samples, DEFAULT_SAMPLE_RATE)
        wavs.append(wav)
        print(f"wrote {wav}")

    raw = out_dir / "voice_raw.wav"
    starts = combine_wavs(wavs, raw, max(0, args.gap_ms))
    normalized = out_dir / "voice.wav"
    try:
        normalize(raw, normalized)
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"ffmpeg loudnorm failed while creating {normalized}: {exc}") from exc

    timings = build_timings(segments, wavs, starts, out_dir, args.voice, args.lang_code, args.speed, max(0, args.gap_ms))
    (out_dir / "timings.json").write_text(json.dumps(timings, indent=2) + "\n", encoding="utf-8")
    print(raw)
    print(normalized)
    print(out_dir / "timings.json")


if __name__ == "__main__":
    main()
