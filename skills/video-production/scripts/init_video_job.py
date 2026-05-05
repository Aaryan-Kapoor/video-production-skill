#!/usr/bin/env python3
"""Create a clean, reusable workspace for a video-production job."""
import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(os.environ.get("VIDEO_PRODUCTION_ROOT", Path.home() / "video-productions")).expanduser()


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return (slug or "video")[:64].strip("-") or "video"


def main():
    ap = argparse.ArgumentParser(description="Initialize a video production job workspace")
    ap.add_argument("title", help="Human-readable video topic/title")
    ap.add_argument("--slug", help="Optional stable slug")
    ap.add_argument("--prompt", help="Original user prompt/request")
    ap.add_argument("--source", action="append", default=[], help="Source URL/path/ID; can repeat")
    args = ap.parse_args()

    now = datetime.now().astimezone()
    slug = slugify(args.slug or args.title)
    job_id = f"{now.strftime('%Y-%m-%d-%H%M')}-{slug}"
    job = ROOT / "jobs" / job_id
    for sub in ["assets", "audio", "frames", "src", "renders", "logs", "exports"]:
        (job / sub).mkdir(parents=True, exist_ok=False)
    (ROOT / "backups").mkdir(parents=True, exist_ok=True)
    (ROOT / "packages").mkdir(parents=True, exist_ok=True)

    manifest = {
        "job_id": job_id,
        "title": args.title,
        "slug": slug,
        "created_at": now.isoformat(),
        "prompt": args.prompt or args.title,
        "sources": args.source,
        "status": "initialized",
        "final_video": None,
        "backup_video": None,
        "host_url": None,
        "notes": [],
    }
    (job / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (job / "README.md").write_text(
        f"# {args.title}\n\nJob: `{job_id}`\n\nUse this folder for durable artifacts. Use `/tmp/video-production-{slug}/` for disposable intermediates when appropriate.\n",
        encoding="utf-8",
    )

    latest = ROOT / "current"
    if latest.exists() or latest.is_symlink():
        latest.unlink()
    latest.symlink_to(job, target_is_directory=True)

    print(job)


if __name__ == "__main__":
    main()
