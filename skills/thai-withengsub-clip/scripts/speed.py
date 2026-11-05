"""Speed a finished voice by an exact factor and keep subtitles in sync.

usage: speed.py narration.wav subtitles.json out_dir --factor 1.12
Use this when the user asks for a speed such as 1.12x. Use retime.py when they ask for a target length.
Writes out_dir/narration.wav and out_dir/subtitles.json, then measures the real factor.
"""
import argparse
import json
import subprocess
from pathlib import Path

KEYS = ("in", "out", "start", "end")


def duration(path):
    done = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(done.stdout.strip())


def scaled(rows, factor):
    return [{**row, **{key: round(row[key] / factor, 3) for key in KEYS if key in row}} for row in rows]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("subtitles")
    ap.add_argument("out")
    ap.add_argument("--factor", type=float, required=True)
    args = ap.parse_args()
    if not 0.5 <= args.factor <= 2.0:
        raise SystemExit("--factor must be between 0.5 and 2.0")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    wav = out / "narration.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", args.audio, "-filter:a", f"atempo={args.factor}", str(wav)], check=True)
    rows = json.loads(Path(args.subtitles).read_text(encoding="utf-8"))
    (out / "subtitles.json").write_text(json.dumps(scaled(rows, args.factor), ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {wav}, measured {duration(args.audio) / duration(wav):.3f}x, {duration(wav):.2f}s")


if __name__ == "__main__":
    main()
