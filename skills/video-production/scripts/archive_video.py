#!/usr/bin/env python3
"""Archive a finished video into the video-production backup tree and update manifest.json."""
import argparse
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(os.environ.get("VIDEO_PRODUCTION_ROOT", Path.home() / "video-productions")).expanduser()


def load_manifest(job: Path):
    path = job / "manifest.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    return path, data


def main():
    ap = argparse.ArgumentParser(description="Archive a completed MP4 and update the job manifest")
    ap.add_argument("video", help="Path to completed video, usually an MP4")
    ap.add_argument("--job", help="Job directory; defaults to video-productions/current")
    ap.add_argument("--name", help="Output basename without extension")
    args = ap.parse_args()

    src = Path(args.video).expanduser().resolve()
    if not src.exists():
        raise SystemExit(f"Video not found: {src}")
    job = Path(args.job).expanduser().resolve() if args.job else (ROOT / "current").resolve()
    if not job.exists():
        raise SystemExit(f"Job directory not found: {job}")

    manifest_path, manifest = load_manifest(job)
    slug = manifest.get("slug") or src.stem
    stamp = datetime.now().astimezone().strftime("%Y-%m-%d-%H%M%S")
    base = args.name or f"{stamp}-{slug}"
    final = job / "exports" / f"{base}.mp4"
    final.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, final)

    backup_dir = ROOT / "backups" / datetime.now().astimezone().strftime("%Y-%m-%d")
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / f"{base}.mp4"
    shutil.copy2(final, backup)

    manifest.update({
        "status": "completed",
        "final_video": str(final),
        "backup_video": str(backup),
        "completed_at": datetime.now().astimezone().isoformat(),
    })
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(final)
    print(backup)


if __name__ == "__main__":
    main()
