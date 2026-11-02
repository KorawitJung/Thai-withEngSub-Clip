"""Generate narration with ElevenLabs and save per-character timing.

usage: narrate.py narration.txt audio_dir --voice VOICE_ID [--model eleven_v3] [--env-file .env] [--dry-run]
The API key comes from ELEVENLABS_API_KEY or --env-file and is never printed.
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128"


def read_key(env_file):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if key or not env_file:
        return key
    for line in Path(env_file).expanduser().read_text(encoding="utf-8-sig").splitlines():
        name, _, value = line.partition("=")
        if name.strip() == "ELEVENLABS_API_KEY":
            return value.strip().strip("'\"")
    return None


def spoken_length(text):
    return len(re.sub(r"\s|\.", "", re.sub(r"\[[^\]]*\]", "", text)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("text")
    ap.add_argument("out")
    ap.add_argument("--voice", default=os.environ.get("ELEVENLABS_VOICE_ID"))
    ap.add_argument("--model", default="eleven_v3")
    ap.add_argument("--stability", type=float, default=0.0)
    ap.add_argument("--env-file")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    text = Path(args.text).read_text(encoding="utf-8").strip()
    print(f"{len(text)} characters billed, {spoken_length(text)} spoken")
    if args.dry_run:
        return
    if not args.voice:
        sys.exit("Missing voice: pass --voice or set ELEVENLABS_VOICE_ID")
    key = read_key(args.env_file)
    if not key:
        sys.exit("Missing ELEVENLABS_API_KEY: set it or pass --env-file")

    body = {"text": text, "model_id": args.model, "voice_settings": {"stability": args.stability}}
    request = urllib.request.Request(
        API.format(voice=args.voice),
        data=json.dumps(body).encode("utf-8"),
        headers={"xi-api-key": key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.load(response)
    except urllib.error.HTTPError as err:
        sys.exit(f"ElevenLabs error {err.code}: {err.read()[:400].decode('utf-8', 'replace')}")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "narration.mp3").write_bytes(base64.b64decode(result["audio_base64"]))
    (out / "alignment.json").write_text(json.dumps(result["alignment"], ensure_ascii=False), encoding="utf-8")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out / "narration.mp3"), "-ar", "48000", "-ac", "2", str(out / "narration.wav")], check=True)
    print(f"wrote {out / 'narration.wav'}")


if __name__ == "__main__":
    main()
