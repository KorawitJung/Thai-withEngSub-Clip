"""Synthesize royalty-free ambience and effects with the standard library only.

usage: soundscape.py drone seconds out.wav [--seed 3] [--root 55]
       soundscape.py hit|tick|rush out.wav
"""
import argparse
import array
import math
import random
import wave

RATE = 24000


def save(samples, path):
    peak = max(1e-6, max(abs(s) for s in samples))
    data = array.array("h", (int(s / peak * 0.85 * 32767) for s in samples))
    with wave.open(path, "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(data.tobytes())


def drone(seconds, seed=3, root=55.0):
    rng = random.Random(seed)
    count = int(seconds * RATE)
    partials = [(root * ratio, rng.uniform(0, 6.28), rng.uniform(0.03, 0.09), rng.uniform(0, 6.28), gain)
                for ratio, gain in ((1, 1.0), (1.5, 0.45), (2.01, 0.3), (2.99, 0.12))]
    fade = int(min(2.0, seconds / 4) * RATE)
    noise, out = 0.0, []
    for n in range(count):
        t = n / RATE
        noise = 0.995 * noise + 0.005 * rng.uniform(-1, 1)
        value = noise * 2.0
        for freq, phase, lfo, lfo_phase, gain in partials:
            value += gain * (0.65 + 0.35 * math.sin(6.283 * lfo * t + lfo_phase)) * math.sin(6.283 * freq * t + phase)
        out.append(value * min(1.0, n / max(fade, 1), (count - n) / max(fade, 1)))
    return out


def hit():
    return [math.exp(-6 * n / RATE) * math.sin(6.283 * (70 - 30 * n / (1.2 * RATE)) * n / RATE) for n in range(int(1.2 * RATE))]


def tick():
    rng = random.Random(1)
    return [math.exp(-90 * n / RATE) * rng.uniform(-1, 1) for n in range(int(0.12 * RATE))]


def rush():
    rng = random.Random(2)
    count, low, out = int(1.6 * RATE), 0.0, []
    for n in range(count):
        x = n / count
        cut = 0.02 + 0.25 * x
        low += cut * (rng.uniform(-1, 1) - low)
        out.append(low * math.sin(math.pi * x) ** 2)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["drone", "hit", "tick", "rush"])
    ap.add_argument("rest", nargs="+")
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--root", type=float, default=55.0)
    args = ap.parse_args()
    if args.kind == "drone":
        save(drone(float(args.rest[0]), args.seed, args.root), args.rest[1])
    else:
        save({"hit": hit, "tick": tick, "rush": rush}[args.kind](), args.rest[0])
    print("wrote", args.rest[-1])


if __name__ == "__main__":
    main()
