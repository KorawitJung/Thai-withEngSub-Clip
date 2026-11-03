# /// script
# requires-python = ">=3.10"
# dependencies = ["torch", "transformers", "scipy"]
# ///
"""Generate a background music bed on this computer with MusicGen.

usage: uv run music.py "dark ambient, slow, no drums" 70 video/assets/music.wav [--model facebook/musicgen-small]
The first run downloads Python packages and the model (plan for about 4 GB) and can take a long time, so run it in the background.
The default model's license is non-commercial: for monetized clips use soundscape.py or music you have rights to.
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

TOKENS_PER_SECOND = 50
MAX_SECONDS = 30


def extend(source, seconds, target):
    fade = min(2.0, seconds / 4)
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-i", str(source), "-t", str(seconds),
         "-af", f"afade=in:d={fade},afade=out:st={seconds - fade}:d={fade}", "-ar", "48000", "-ac", "2", str(target)],
        check=True,
    )


def generate(prompt, seconds, model_id, target):
    import scipy.io.wavfile
    from transformers import AutoProcessor, MusicgenForConditionalGeneration

    processor = AutoProcessor.from_pretrained(model_id)
    model = MusicgenForConditionalGeneration.from_pretrained(model_id)
    inputs = processor(text=[prompt], padding=True, return_tensors="pt")
    audio = model.generate(**inputs, do_sample=True, max_new_tokens=int(min(seconds, MAX_SECONDS) * TOKENS_PER_SECOND))
    scipy.io.wavfile.write(target, model.config.audio_encoder.sampling_rate, audio[0, 0].cpu().numpy())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("seconds", type=float)
    ap.add_argument("out")
    ap.add_argument("--model", default="facebook/musicgen-small")
    args = ap.parse_args()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as folder:
        raw = Path(folder) / "raw.wav"
        generate(args.prompt, args.seconds, args.model, raw)
        extend(raw, args.seconds, args.out)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
