"""Fit a finished voice to a target length by speeding it up, keeping subtitles in sync and a held final card.

usage: retime.py narration.wav subtitles.json out_dir --target 60 [--hold 5] [--card-line]
--hold is how long the final card stays on screen. --card-line means the last subtitle is spoken over that card.
Writes out_dir/narration.wav and out_dir/subtitles.json, then prints the --hold to pass to compose.py.
Prefer cutting the script: speeding above 1.25x starts to sound rushed, so the script warns.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

RUSHED = 1.25
FASTEST = 2.0


def plan(subtitles, target, hold=0.0, card_line=False):
    """Return the speed factor and the retimed subtitles."""
    body = target - hold
    if body <= 0:
        raise ValueError("--hold must be shorter than --target")
    spoken = subtitles[-1]["in"] if card_line else subtitles[-1]["out"]
    factor = spoken / body
    if factor < 1:
        raise ValueError(f"already fits: speech takes {spoken:.2f}s of {body:.2f}s, and this tool only speeds up")
    if factor > FASTEST:
        raise ValueError(f"needs {factor:.2f}x, faster than {FASTEST}x: cut the script instead")
    timed = [{**line, **{key: round(line[key] / factor, 3) for key in ("in", "out", "start", "end")}} for line in subtitles]
    if card_line and timed[-1]["out"] - timed[-1]["in"] > hold:
        raise ValueError("the last line is longer than --hold")
    return factor, timed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("subtitles")
    ap.add_argument("out")
    ap.add_argument("--target", type=float, required=True)
    ap.add_argument("--hold", type=float, default=0.0)
    ap.add_argument("--card-line", action="store_true")
    args = ap.parse_args()
    subtitles = json.loads(Path(args.subtitles).read_text(encoding="utf-8"))
    try:
        factor, timed = plan(subtitles, args.target, args.hold, args.card_line)
    except ValueError as err:
        sys.exit(str(err))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", args.audio, "-af", f"atempo={factor:.4f}", str(out / "narration.wav")], check=True)
    (out / "subtitles.json").write_text(json.dumps(timed, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"speed {factor:.2f}x, speech ends at {timed[-1]['out']:.2f}s")
    if factor > RUSHED:
        print(f"warning: above {RUSHED}x can sound rushed, listen to it or cut the script")
    if args.hold:
        print(f"compose.py: --hold {args.hold:g}")


if __name__ == "__main__":
    main()
