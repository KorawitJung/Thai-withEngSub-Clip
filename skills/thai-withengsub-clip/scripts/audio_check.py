"""Measure whether a background bed sits well under the voice. It measures only; a person still has to listen.

usage: audio_check.py narration.wav bed.wav [--volume 0.2] [--below 13]
--volume is the value given to ep.sound for the bed.
"""
import argparse
import math
import sys

from master import loudness

HISS_LIMIT = -50


def report(voice, bed, volume, below):
    """Return readable problems from measured LUFS values; bed is {"full", "treble", "mid"}."""
    level = bed["full"] + 20 * math.log10(volume)
    found = []
    gap = voice - level
    if abs(gap - below) > 3:
        found.append(f"bed is {gap:.1f} LU under the voice, aim for about {below:g}: use volume {10 ** ((voice - below - bed['full']) / 20):.2f}")
    treble = bed["treble"] + 20 * math.log10(volume)
    if treble > HISS_LIMIT:
        found.append(f"energy above 4 kHz is {treble:.1f} LUFS, over {HISS_LIMIT}: may sound like hiss")
    if bed["mid"] < bed["full"] - 12:
        found.append("little energy at 100-700 Hz: phone speakers may not play this bed")
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("voice")
    ap.add_argument("bed")
    ap.add_argument("--volume", type=float, default=0.2)
    ap.add_argument("--below", type=float, default=13)
    args = ap.parse_args()
    voice = loudness(args.voice)
    bed = {"full": loudness(args.bed), "treble": loudness(args.bed, "highpass=f=4000,highpass=f=4000"), "mid": loudness(args.bed, "highpass=f=100,lowpass=f=700")}
    print(f"voice {voice} LUFS, bed {bed['full']} LUFS at volume 1.0")
    found = report(voice, bed, args.volume, args.below)
    for item in found:
        print("-", item)
    print("no problems measured" if not found else f"{len(found)} problems")
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
