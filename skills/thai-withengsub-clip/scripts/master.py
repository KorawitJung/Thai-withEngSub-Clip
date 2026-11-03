"""Normalize audio loudness without re-encoding video, then write a review note.

usage: master.py rendered.mp4 final.mp4 [--lufs -14] [--max-seconds 90]
Writes final-review.md next to the final video.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path


def loudness(path, before=""):
    chain = f"{before},ebur128" if before else "ebur128"
    log = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", chain, "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=True,
    ).stderr
    found = re.findall(r"I:\s+(-?[\d.]+) LUFS", log)
    return float(found[-1]) if found else None


def measure(path):
    info = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout)
    stream = info["streams"][0]
    return {"width": stream["width"], "height": stream["height"], "seconds": float(info["format"]["duration"]), "lufs": loudness(path)}


def problems(result, lufs, max_seconds):
    found = []
    if (result["width"], result["height"]) != (1080, 1920):
        found.append(f"ขนาดภาพเป็น {result['width']}x{result['height']} ไม่ใช่ 1080x1920")
    if result["seconds"] > max_seconds:
        found.append(f"ยาว {result['seconds']:.1f} วินาที เกิน {max_seconds:g} วินาที")
    if result["lufs"] is None or abs(result["lufs"] - lufs) > 1.5:
        found.append(f"ความดังวัดได้ {result['lufs']} LUFS ห่างจากเป้า {lufs:g}")
    return found


def review_note(name, result, found):
    rows = "\n".join(f"- ⚠ {item}" for item in found) or "- ไม่พบปัญหาจากการวัด"
    return f"""# บันทึกตรวจงาน: {name}

## วัดอัตโนมัติ
- ภาพ: {result['width']}x{result['height']}
- ความยาว: {result['seconds']:.1f} วินาที
- ความดัง: {result['lufs']} LUFS
{rows}

## ให้คนตรวจ
- [ ] ฟังเสียงพากย์ คำอ่าน และความดังของดนตรีเทียบกับเสียงพูด
- [ ] ดูจังหวะซับและการตัดช็อตแบบวิดีโอ
- [ ] ตรวจข้อเท็จจริงและแหล่งข้อมูลใน `script.md`
- [ ] ตรวจที่มาของเสียงใน `credits.md` ถ้ามี
- [ ] ลองเปิดบนแอปจริงว่าปุ่มไม่บังตัวอักษร
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("target")
    ap.add_argument("--lufs", type=float, default=-14)
    ap.add_argument("--max-seconds", type=float, default=90)
    args = ap.parse_args()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", args.source, "-c:v", "copy", "-af", f"loudnorm=I={args.lufs}:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", args.target], check=True)
    target = Path(args.target)
    result = measure(target)
    found = problems(result, args.lufs, args.max_seconds)
    note = target.with_name(f"{target.stem}-review.md")
    note.write_text(review_note(target.name, result, found), encoding="utf-8")
    print(f"wrote {target} and {note}, {result['seconds']:.1f}s, {result['lufs']} LUFS, {len(found)} problems")


if __name__ == "__main__":
    main()
