"""Report which tools are installed and whether a narration key is configured. The key is never printed.

usage: check_env.py [--env-file .env]
"""
import argparse
import os
import shutil
import sys
from pathlib import Path


def has_key(env_file):
    if os.environ.get("ELEVENLABS_API_KEY"):
        return True
    path = Path(env_file)
    if not path.exists():
        return False
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        name, _, value = line.partition("=")
        if name.strip() == "ELEVENLABS_API_KEY" and value.strip():
            return True
    return False


ap = argparse.ArgumentParser()
ap.add_argument("--env-file", default=".env")
args = ap.parse_args()

missing = [tool for tool in ("ffmpeg", "ffprobe", "node", "npx") if not shutil.which(tool)]
print("python", sys.version.split()[0])
print("missing:", ", ".join(missing) if missing else "none")
print("elevenlabs key:", "found" if has_key(args.env_file) else "not found (needed for real narration)")
print("uv:", "found" if shutil.which("uv") else "not found (needed only for music.py)")
print(f"free disk: {shutil.disk_usage('.').free / 1024 ** 3:.1f} GB (music.py needs about 4 GB)")
sys.exit(1 if missing else 0)
