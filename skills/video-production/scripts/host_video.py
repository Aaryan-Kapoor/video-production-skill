#!/usr/bin/env python3
"""Host one video file over the machine's Tailscale IP with Python's static server.

This script intentionally prints the command to run rather than daemonizing itself; start it via exec
with background=true so OpenClaw can track/stop the process.
"""
import argparse
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(os.environ.get("VIDEO_PRODUCTION_ROOT", Path.home() / "video-productions")).expanduser()


def tailscale_ip() -> str:
    out = subprocess.check_output(["tailscale", "ip", "-4"], text=True).strip().splitlines()
    if not out:
        raise SystemExit("No Tailscale IPv4 found")
    return out[0]


def main():
    ap = argparse.ArgumentParser(description="Prepare a one-file Tailscale video host directory")
    ap.add_argument("video")
    ap.add_argument("--port", type=int, default=8791)
    ap.add_argument("--slug")
    args = ap.parse_args()

    src = Path(args.video).expanduser().resolve()
    if not src.exists():
        raise SystemExit(f"Video not found: {src}")
    slug = args.slug or src.stem
    serve_dir = ROOT / "serve" / slug
    serve_dir.mkdir(parents=True, exist_ok=True)
    dest = serve_dir / src.name
    shutil.copy2(src, dest)
    ip = tailscale_ip()
    print(f"cd {serve_dir}")
    print(f"python3 -m http.server {args.port} --bind {ip}")
    print(f"URL: http://{ip}:{args.port}/{dest.name}")


if __name__ == "__main__":
    main()
