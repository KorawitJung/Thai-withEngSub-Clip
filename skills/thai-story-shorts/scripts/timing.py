"""Turn a line plan and character alignment into timed subtitle lines.

usage: timing.py lines.json alignment.json subtitles.json
       timing.py --estimate narration.txt alignment.json [--rate 9]

lines.json: [{"say": "text as written in narration.txt", "show": "on-screen text, | breaks", "alert": false}]
--estimate writes a rough alignment so a storyboard can be previewed before paying for narration.
"""
import argparse
import json
import re
from pathlib import Path

LEAD_IN = 0.06
HOLD = 0.3
MIN_ON_SCREEN = 0.8
GAP = 0.08


def estimate_alignment(text, rate=9.0):
    chars, starts, ends, now = [], [], [], 0.0
    for part in re.split(r"(\[[^\]]*\])", text):
        tag = part.startswith("[")
        for ch in part:
            step = 0.0 if tag or ch.isspace() else (0.12 if ch == "." else 1 / rate)
            chars.append(ch)
            starts.append(round(now, 3))
            now += step
            ends.append(round(now, 3))
    return {"characters": chars, "character_start_times_seconds": starts, "character_end_times_seconds": ends}


def build_subtitles(lines, alignment):
    text = "".join(alignment["characters"])
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]
    timed, cursor = [], 0
    for number, line in enumerate(lines):
        say = line["say"].strip()
        begin = text.find(say, cursor)
        if begin < 0:
            raise ValueError(f"line {number}: not found in narration order: {say!r}")
        last = begin + len(say.rstrip(". ")) - 1
        timed.append({"show": line["show"], "alert": bool(line.get("alert")), "start": starts[begin], "end": ends[last]})
        cursor = last + 1
    for number, item in enumerate(timed):
        item["in"] = round(max(0.0, item["start"] - LEAD_IN), 3)
        wanted = max(item["end"] + HOLD, item["in"] + MIN_ON_SCREEN)
        limit = timed[number + 1]["start"] - LEAD_IN - GAP if number + 1 < len(timed) else wanted
        item["out"] = round(max(item["in"] + 0.1, min(wanted, limit)), 3)
    return timed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--estimate", action="store_true")
    ap.add_argument("--rate", type=float, default=9.0)
    ap.add_argument("paths", nargs="+")
    args = ap.parse_args()
    if args.estimate:
        source, target = args.paths
        data = estimate_alignment(Path(source).read_text(encoding="utf-8").strip(), args.rate)
        Path(target).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        print(f"estimated {data['character_end_times_seconds'][-1]:.1f}s")
        return
    plan, alignment, target = args.paths
    timed = build_subtitles(
        json.loads(Path(plan).read_text(encoding="utf-8")),
        json.loads(Path(alignment).read_text(encoding="utf-8")),
    )
    Path(target).write_text(json.dumps(timed, ensure_ascii=False, indent=1), encoding="utf-8")
    for number, item in enumerate(timed):
        print(f"{number:3} {item['in']:7.2f} {item['out']:7.2f} {'!' if item['alert'] else ' '} {item['show']}".encode("ascii", "backslashreplace").decode())


if __name__ == "__main__":
    main()
