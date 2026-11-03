"""Give narration room to breathe, or drop a line, without generating the voice again.

usage: pace.py narration.wav subtitles.json out_dir [--min-gap 0.42] [--pad 7=0.4 --pad 8=0.5] [--drop 12]
Line numbers are the ones timing.py prints. Cuts fall in the middle of the gap between lines, with short fades.
Writes out_dir/narration.wav and out_dir/subtitles.json. Run it after timing.py.
"""
import argparse
import json
import subprocess
from pathlib import Path

from tighten import duration_of
from timing import fit_windows

FADE = 0.012


def plan(subtitles, duration, min_gap=0.42, pads=None, drop=()):
    """Return audio pieces (start, end, silence before) and the retimed subtitles."""
    pads = pads or {}
    edges = [0.0] + [(a["end"] + b["start"]) / 2 for a, b in zip(subtitles, subtitles[1:])] + [duration]
    pieces, timed, now = [], [], 0.0
    for number, line in enumerate(subtitles):
        if number in drop:
            continue
        a, b = edges[number], edges[number + 1]
        lead = line["start"] - a
        silence = 0.0
        if timed:
            silence = max(0.0, min_gap - (now + lead - timed[-1]["end"])) + pads.get(number, 0.0)
        now += silence
        start = now + lead
        timed.append({**line, "start": round(start, 3), "end": round(start + line["end"] - line["start"], 3)})
        pieces.append((a, b, silence))
        now += b - a
    if not timed:
        raise ValueError("every line was dropped")
    return pieces, fit_windows(timed)


def join(wav, pieces, target):
    parts = []
    for k, (a, b, silence) in enumerate(pieces):
        fade = min(FADE, (b - a) / 2)
        delay = f",adelay={int(silence * 1000)}:all=1" if silence else ""
        parts.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=in:d={fade},afade=out:st={b - a - fade}:d={fade}{delay}[p{k}]")
    inputs = "".join(f"[p{k}]" for k in range(len(pieces)))
    graph = ";".join(parts) + f";{inputs}concat=n={len(pieces)}:v=0:a=1[out]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-filter_complex", graph, "-map", "[out]", str(target)], check=True)


def parse_pad(text):
    line, _, seconds = text.partition("=")
    return int(line), float(seconds)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("subtitles")
    ap.add_argument("out")
    ap.add_argument("--min-gap", type=float, default=0.42)
    ap.add_argument("--pad", action="append", default=[], type=parse_pad, help="line=seconds of extra silence before that line")
    ap.add_argument("--drop", action="append", default=[], type=int, help="line number to remove")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    subtitles = json.loads(Path(args.subtitles).read_text(encoding="utf-8"))
    pieces, timed = plan(subtitles, duration_of(args.wav), args.min_gap, dict(args.pad), set(args.drop))
    join(args.wav, pieces, out / "narration.wav")
    (out / "subtitles.json").write_text(json.dumps(timed, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(timed)} lines, {duration_of(out / 'narration.wav'):.1f}s, wrote {out}")


if __name__ == "__main__":
    main()
