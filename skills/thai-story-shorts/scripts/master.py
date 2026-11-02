"""Normalize audio loudness for short-video platforms without re-encoding video.

usage: master.py rendered.mp4 final.mp4 [--lufs -15]
"""
import argparse
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument("source")
ap.add_argument("target")
ap.add_argument("--lufs", type=float, default=-15)
args = ap.parse_args()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", args.source, "-c:v", "copy", "-af", f"loudnorm=I={args.lufs}:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", args.target], check=True)
print("wrote", args.target)
