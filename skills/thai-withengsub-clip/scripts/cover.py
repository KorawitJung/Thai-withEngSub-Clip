"""Make a 1080x1920 cover image that shares the clip's style and fonts.

usage: cover.py out_dir --title "ชื่อเรื่อง" [--kicker "มีจริงไหม?"] [--sub "บรรทัดรอง"] [--photo bg.jpg] [--inset mural.jpg --credit "ที่มาภาพ"] [--logo logo.png] [--preset story-night]
Writes out_dir/cover.png. Text accepts | for a new line. --credit is required when a photo is used.
"""
import argparse
import html
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compose  # noqa: E402
import draw  # noqa: E402


def text(value):
    return html.escape(value).replace("|", "<br>").replace("@", "&#64;")


def copy_asset(source, folder, name):
    target = Path(folder) / "assets" / f"{name}{Path(source).suffix.lower()}"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return f"assets/{target.name}"


def layout(args, folder):
    parts = []
    if args.photo:
        parts.append(f'<img class="cover-bg" src="{copy_asset(args.photo, folder, "background")}" alt="">')
    block = ""
    if args.kicker:
        block += f'<div class="kicker">{text(args.kicker)}</div>'
    block += f'<div class="title">{text(args.title)}</div>'
    if args.sub:
        block += f'<div class="sub-title">{text(args.sub)}</div>'
    parts.append(f'<div class="cover-text">{block}</div>')
    if args.inset:
        parts.append(draw.photo_card("inset", copy_asset(args.inset, folder, "inset"), args.credit, args.tag, top=1120, tilt=3, shown=True).replace("@", "&#64;"))
    elif args.photo:
        parts.append(f'<div class="photo" style="top:1830px;opacity:1"><small>{text(args.credit)}</small></div>')
    if args.logo:
        parts.append(f'<img class="cover-logo" src="{copy_asset(args.logo, folder, "logo")}" alt="">')
    return "".join(parts)


def build(args):
    if (args.photo or args.inset) and not args.credit:
        raise SystemExit("--credit is required when a photo is used")
    folder = Path(args.out)
    line = {"show": "", "sub": "", "alert": False, "start": 0.0, "end": 0.5, "in": 0.0, "out": 0.5}
    ep = compose.Episode([line], tail=0.5, preset=args.preset, subs="primary")
    if not args.system_fonts:
        ep.use_fonts(folder)
    ep.shot("cover", 0, draw.backdrop(), html=layout(args, folder), zoom=1)
    compose.render(ep, folder)
    return folder


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--title", required=True)
    ap.add_argument("--kicker", default="")
    ap.add_argument("--sub", default="")
    ap.add_argument("--photo")
    ap.add_argument("--inset")
    ap.add_argument("--tag", default="")
    ap.add_argument("--credit", default="")
    ap.add_argument("--logo")
    ap.add_argument("--preset", default="story-night", choices=sorted(compose.PRESETS))
    ap.add_argument("--system-fonts", action="store_true")
    args = ap.parse_args()
    folder = build(args)
    subprocess.run([shutil.which("npx") or "npx", "--yes", "hyperframes", "snapshot", str(folder), "--at", "0.2", "--no-end", "--keep", "-o", str(folder / "still")], check=True)
    shutil.copyfile(folder / "still" / "at-0.2s.png", folder / "cover.png")
    print("wrote", folder / "cover.png")


if __name__ == "__main__":
    main()
