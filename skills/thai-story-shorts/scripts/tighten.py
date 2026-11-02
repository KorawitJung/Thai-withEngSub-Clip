"""Shorten long pauses in narration and keep the character timing in sync.

usage: tighten.py narration.wav alignment.json out_dir [--max-gap 0.35] [--speed 1.0] [--noise -35]
Writes out_dir/narration.wav and out_dir/alignment.json. Run it before timing.py.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path


def find_silences(path, noise, min_length):
    log = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", f"silencedetect=noise={noise}dB:d={min_length}", "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=True,
    ).stderr
    starts = [float(v) for v in re.findall(r"silence_start: (-?[\d.]+)", log)]
    ends = [float(v) for v in re.findall(r"silence_end: (-?[\d.]+)", log)]
    return [(max(0.0, a), b) for a, b in zip(starts, ends)]


def keep_spans(silences, duration, max_gap):
    spans, cursor = [], 0.0
    for start, end in silences:
        if end - start > max_gap:
            spans.append((cursor, start + max_gap / 2))
            cursor = end - max_gap / 2
    spans.append((cursor, duration))
    return spans


def remap(t, spans, speed=1.0):
    elapsed = 0.0
    for start, end in spans:
        if t <= end:
            return round((elapsed + max(0.0, t - start)) / speed, 3)
        elapsed += end - start
    return round(elapsed / speed, 3)


def tighten(wav, spans, speed, target):
    parts = [f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[p{k}]" for k, (a, b) in enumerate(spans)]
    inputs = "".join(f"[p{k}]" for k in range(len(spans)))
    graph = ";".join(parts) + f";{inputs}concat=n={len(spans)}:v=0:a=1,atempo={speed}[out]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-filter_complex", graph, "-map", "[out]", str(target)], check=True)


def duration_of(path):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("alignment")
    ap.add_argument("out")
    ap.add_argument("--max-gap", type=float, default=0.35)
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--noise", type=float, default=-35)
    args = ap.parse_args()
    if not 0.5 <= args.speed <= 2.0:
        raise SystemExit("--speed must be between 0.5 and 2.0")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    before = duration_of(args.wav)
    spans = keep_spans(find_silences(args.wav, args.noise, args.max_gap), before, args.max_gap)
    tighten(args.wav, spans, args.speed, out / "narration.wav")

    data = json.loads(Path(args.alignment).read_text(encoding="utf-8"))
    for key in ("character_start_times_seconds", "character_end_times_seconds"):
        data[key] = [remap(t, spans, args.speed) for t in data[key]]
    (out / "alignment.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"{before:.1f}s -> {duration_of(out / 'narration.wav'):.1f}s, wrote {out}")


if __name__ == "__main__":
    main()
