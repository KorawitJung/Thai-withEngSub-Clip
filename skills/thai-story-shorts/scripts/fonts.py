"""Font library: downloads Google Fonts on demand and prepares them for a video project.

usage: fonts.py list [--lang th|en] [--mood WORD]
       fonts.py preview out.html [--lang th|en]
"""
import argparse
import html
import os
import re
import shutil
import urllib.request
from pathlib import Path

CACHE = Path(os.environ.get("THAI_STORY_FONT_CACHE", Path.home() / ".cache" / "thai-story-shorts" / "fonts"))
REGULAR = (500, 700)
SINGLE = (400,)
RANGE = (400, 700)

# id: (family, language, mood, weights)
LIBRARY = {
    "kanit": ("Kanit", "th", "subtitle bold tiktok readable", REGULAR),
    "prompt": ("Prompt", "th", "modern clean loopless", REGULAR),
    "noto-thai": ("Noto Sans Thai", "th", "neutral safe news", REGULAR),
    "noto-looped": ("Noto Sans Thai Looped", "th", "school textbook looped", REGULAR),
    "sarabun": ("Sarabun", "th", "official formal", REGULAR),
    "ibm-thai": ("IBM Plex Sans Thai", "th", "tech data sharp", REGULAR),
    "anuphan": ("Anuphan", "th", "modern airy", REGULAR),
    "mitr": ("Mitr", "th", "friendly rounded dense", REGULAR),
    "athiti": ("Athiti", "th", "slim polite", REGULAR),
    "bai-jamjuree": ("Bai Jamjuree", "th", "graphic squarish", REGULAR),
    "chakra-petch": ("Chakra Petch", "th", "military scifi disaster", REGULAR),
    "k2d": ("K2D", "th", "wide mobile readable", REGULAR),
    "krub": ("Krub", "th", "warm rounded", REGULAR),
    "kodchasan": ("Kodchasan", "th", "playful cartoon", REGULAR),
    "koho": ("KoHo", "th", "tall magazine", REGULAR),
    "niramit": ("Niramit", "th", "soft round", REGULAR),
    "fahkwang": ("Fahkwang", "th", "luxury high-contrast", REGULAR),
    "mali": ("Mali", "th", "cute handwriting", REGULAR),
    "playpen-thai": ("Playpen Sans Thai", "th", "pen handwriting", REGULAR),
    "noto-serif-thai": ("Noto Serif Thai", "th", "serif traditional serious", REGULAR),
    "pridi": ("Pridi", "th", "serif newspaper", REGULAR),
    "taviraj": ("Taviraj", "th", "serif classic retro", REGULAR),
    "trirong": ("Trirong", "th", "serif novel mystery", REGULAR),
    "maitree": ("Maitree", "th", "serif long-reading", REGULAR),
    "chonburi": ("Chonburi", "th", "display heavy high-contrast", SINGLE),
    "itim": ("Itim", "th", "round handwriting", SINGLE),
    "sriracha": ("Sriracha", "th", "brush handwriting", SINGLE),
    "pattaya": ("Pattaya", "th", "display italic poster", SINGLE),
    "charm": ("Charm", "th", "calligraphy elegant", RANGE),
    "charmonman": ("Charmonman", "th", "calligraphy delicate", RANGE),
    "srisakdi": ("Srisakdi", "th", "antique ghost folklore", RANGE),
    "thasadith": ("Thasadith", "th", "thin airy minimal", RANGE),
    "bebas": ("Bebas Neue", "en", "headline documentary tall", SINGLE),
    "anton": ("Anton", "en", "headline heavy impact", SINGLE),
    "oswald": ("Oswald", "en", "condensed news", REGULAR),
    "archivo-black": ("Archivo Black", "en", "heavy numbers", SINGLE),
    "staatliches": ("Staatliches", "en", "uppercase poster", SINGLE),
    "teko": ("Teko", "en", "condensed sports hud", REGULAR),
    "barlow-cond": ("Barlow Condensed", "en", "condensed readable", REGULAR),
    "roboto-cond": ("Roboto Condensed", "en", "condensed standard", REGULAR),
    "russo": ("Russo One", "en", "game heavy rounded", SINGLE),
    "montserrat": ("Montserrat", "en", "geometric popular", REGULAR),
    "poppins": ("Poppins", "en", "round modern", REGULAR),
    "inter": ("Inter", "en", "mobile sharp neutral", REGULAR),
    "rubik": ("Rubik", "en", "friendly rounded", REGULAR),
    "playfair": ("Playfair Display", "en", "serif luxury accent", REGULAR),
    "cinzel": ("Cinzel", "en", "serif epic roman", REGULAR),
    "creepster": ("Creepster", "en", "horror zombie", SINGLE),
    "nosifer": ("Nosifer", "en", "horror blood heavy", SINGLE),
    "metal-mania": ("Metal Mania", "en", "horror metal gothic", SINGLE),
    "special-elite": ("Special Elite", "en", "typewriter secret-file", SINGLE),
    "black-ops": ("Black Ops One", "en", "military stencil", SINGLE),
    "rubik-glitch": ("Rubik Glitch", "en", "glitch signal", SINGLE),
    "bangers": ("Bangers", "en", "comic cartoon", SINGLE),
    "permanent-marker": ("Permanent Marker", "en", "marker handwriting", SINGLE),
    "righteous": ("Righteous", "en", "retro display", SINGLE),
    "press-start": ("Press Start 2P", "en", "pixel retro game", SINGLE),
}


def font_url(family, weight):
    query = f"family={family.replace(' ', '+')}:wght@{weight}"
    request = urllib.request.Request(f"https://fonts.googleapis.com/css2?{query}", headers={"User-Agent": "Mozilla/4.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        css = response.read().decode("utf-8")
    found = re.search(r"url\((https://[^)]+\.ttf)\)", css)
    if not found:
        raise ValueError(f"no TTF offered for {family} {weight}")
    return found.group(1)


def fetch(font_id, weight):
    """Return the cached TTF for a font weight, downloading it the first time."""
    path = CACHE / f"{font_id}-{weight}.ttf"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(font_url(LIBRARY[font_id][0], weight), timeout=120) as response:
            data = response.read()
        path.write_bytes(data)
    return path


def weight_range(weights, weight):
    if len(weights) == 1:
        return "400 900"
    return "400 600" if weight == weights[0] else "700 900"


def install(font_ids, video_dir):
    """Copy fonts into the project and return their @font-face CSS. Repeated ids are handled once."""
    css = []
    target = Path(video_dir) / "assets" / "fonts"
    for font_id in dict.fromkeys(font_ids):
        if font_id not in LIBRARY:
            raise ValueError(f"unknown font: {font_id}; run fonts.py list")
        family, _, _, weights = LIBRARY[font_id]
        for weight in weights:
            target.mkdir(parents=True, exist_ok=True)
            name = f"{font_id}-{weight}.ttf"
            shutil.copyfile(fetch(font_id, weight), target / name)
            css.append(f'@font-face{{font-family:"{family}";font-weight:{weight_range(weights, weight)};src:url("assets/fonts/{name}")}}')
    return "\n".join(css)


def stack(font_id, *more):
    names = [LIBRARY[item][0] for item in (font_id, *more) if item]
    return ",".join(f'"{name}"' for name in dict.fromkeys(names))


def select(lang=None, mood=None):
    return {key: value for key, value in LIBRARY.items() if (not lang or value[1] == lang) and (not mood or mood in value[2])}


def preview(path, lang=None):
    rows, faces = [], []
    for font_id, (family, language, mood, weights) in select(lang).items():
        for weight in weights:
            faces.append(f'@font-face{{font-family:"{font_id}";font-weight:{weight_range(weights, weight)};src:url("{fetch(font_id, weight).as_uri()}")}}')
        sample = "ถ้าน้ำท่วมบ้านคุณ คุณจะรอดไหม? 1784" if language == "th" else "WOULD YOU SURVIVE? Day 3 · 1784"
        rows.append(f'<div style="padding:12px 0;border-bottom:1px solid #333"><small>{html.escape(font_id)} · {html.escape(family)} · {html.escape(mood)}</small><div style="font:700 44px \'{font_id}\'">{sample}</div></div>')
    Path(path).write_text(f'<!doctype html><meta charset="utf-8"><title>Font library</title><style>{"".join(faces)}body{{background:#14161c;color:#f2ece0;font-family:sans-serif;margin:24px}}</style>{"".join(rows)}', encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["list", "preview"])
    ap.add_argument("out", nargs="?")
    ap.add_argument("--lang", choices=["th", "en"])
    ap.add_argument("--mood")
    args = ap.parse_args()
    if args.command == "preview":
        if not args.out:
            ap.error("preview needs an output path")
        preview(args.out, args.lang)
        print("wrote", args.out)
        return
    for font_id, (family, language, mood, _) in select(args.lang, args.mood).items():
        print(f"{font_id:18} {language}  {family:24} {mood}")


if __name__ == "__main__":
    main()
