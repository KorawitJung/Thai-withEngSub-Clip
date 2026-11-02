"""Write a single-file HyperFrames project from an episode script.

usage: compose.py episode.py video_dir subtitles.json [--tail 2.5]

episode.py defines build(ep). Shots start on a subtitle line and last until the next shot,
so timing follows the narration. In art, html and motion, "@name" becomes a shot-unique id.
Motion code can use tl (timeline), T (shot start) and D (shot length).
"""
import argparse
import html
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from draw import THEMES  # noqa: E402

GSAP = "https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"
FONT_FACES = """@font-face{font-family:"Thai Story";font-weight:400 600;src:local("Leelawadee UI"),local("Sukhumvit Set Medium"),local("Noto Sans Thai"),local("Tahoma")}
@font-face{font-family:"Thai Story";font-weight:700;src:local("Leelawadee UI Bold"),local("Sukhumvit Set Bold"),local("Noto Sans Thai Bold"),local("Tahoma Bold")}"""
FONT = '"Thai Story",sans-serif'


def rise(target, at):
    return f'tl.fromTo("{target}",{{y:36,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"power2.out"}},T+{at});\n'


def sway(target, angle, at=0, each=0.7, times=4, pivot="50% 100%"):
    return f'tl.fromTo("{target}",{{rotation:0,transformOrigin:"{pivot}"}},{{rotation:{angle},transformOrigin:"{pivot}",duration:{each},ease:"sine.inOut",yoyo:true,repeat:{times - 1}}},T+{at});\n'


def flicker(target, at=0, times=6):
    return f'tl.fromTo("{target}",{{opacity:1}},{{opacity:.25,duration:.12,ease:"none",yoyo:true,repeat:{times - 1}}},T+{at});\n'


class Episode:
    def __init__(self, subtitles, tail=2.5, theme="night"):
        self.subtitles = subtitles
        self.tail = tail
        self.theme = THEMES[theme]
        self.shots = []
        self.sounds = []

    def shot(self, name, line, art, html="", motion="", zoom=1.06, focus="50% 50%"):
        if not re.fullmatch(r"[a-z][a-z0-9-]*", name):
            raise ValueError(f"bad shot name: {name}")
        if not 0 <= line < len(self.subtitles):
            raise ValueError(f"shot {name}: no subtitle line {line}")
        if self.shots and line <= self.shots[-1]["line"]:
            raise ValueError(f"shot {name}: line {line} must come after the previous shot")
        if any(item["name"] == name for item in self.shots):
            raise ValueError(f"duplicate shot: {name}")
        self.shots.append(dict(name=name, line=line, art=art, html=html, motion=motion, zoom=zoom, focus=focus))

    def sound(self, src, start=0.0, volume=1.0, automation=None):
        self.sounds.append(dict(src=src, start=start, volume=volume, automation=automation))

    @property
    def total(self):
        return round(self.subtitles[-1]["out"] + self.tail, 3)

    def schedule(self):
        if not self.shots:
            raise ValueError("episode has no shots")
        if self.shots[0]["line"] != 0:
            raise ValueError("the first shot must start on line 0")
        timed = []
        for number, item in enumerate(self.shots):
            start = 0.0 if number == 0 else self.subtitles[item["line"]]["in"]
            end = self.total if number + 1 == len(self.shots) else self.subtitles[self.shots[number + 1]["line"]]["in"]
            timed.append({**item, "start": round(start, 3), "dur": round(end - start, 3)})
        return timed


def audio_length(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    if out.returncode:
        raise ValueError(f"cannot read audio: {path}")
    return float(out.stdout)


def render(ep, video_dir):
    W, H = 1080, 1920
    layers, script = [], []
    for item in ep.schedule():
        pid = item["name"]
        fix = lambda text: re.sub(r"@([a-z][a-z0-9-]*)", rf"{pid}-\1", text)
        layers.append(
            f'<div id="{pid}" class="clip shot" data-start="{item["start"]}" data-duration="{item["dur"]}" data-track-index="1">'
            f'<div id="{pid}-cam" class="cam" style="transform-origin:{item["focus"]}">'
            f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{fix(item["art"])}</svg></div>{fix(item["html"])}</div>'
        )
        script.append(
            f'(function(T,D){{tl.fromTo("#{pid}-cam",{{scale:1}},{{scale:{item["zoom"]},duration:D,ease:"sine.inOut"}},T);\n{fix(item["motion"])}}})({item["start"]},{item["dur"]});'
        )
    for number, sub in enumerate(ep.subtitles):
        body = "<br>".join(html.escape(part) for part in sub["show"].split("|"))
        kind = "sub alert" if sub["alert"] else "sub"
        layers.append(f'<div id="sub-{number}" class="clip {kind}" data-start="{sub["in"]}" data-duration="{round(sub["out"] - sub["in"], 3)}" data-track-index="3"><span>{body}</span></div>')
    for number, sound in enumerate(ep.sounds):
        path = Path(video_dir) / sound["src"]
        length = round(min(audio_length(path), ep.total - sound["start"]), 3)
        extra = f" data-automation='{json.dumps(sound['automation'])}'" if sound["automation"] else ""
        layers.append(f'<audio id="snd-{number}" class="clip" src="{sound["src"]}" data-start="{sound["start"]}" data-duration="{length}" data-track-index="{10 + number}" data-volume="{sound["volume"]}"{extra}></audio>')
    colors = ep.theme
    page = f"""<!doctype html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}">
<script src="{GSAP}"></script>
<style>
{FONT_FACES}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{colors['deep']}}}
#main{{position:relative;width:{W}px;height:{H}px;overflow:hidden;font-family:{FONT}}}
.shot,.cam,.cam svg{{position:absolute;inset:0;width:{W}px;height:{H}px}}
.shot{{overflow:hidden;z-index:1}}
.fact{{position:absolute;left:96px;right:144px;top:240px;padding:32px 40px;border-radius:12px;background:{colors['paper']};color:{colors['ink']};opacity:0;font-size:44px;font-weight:600;line-height:1.35}}
.fact b{{display:block;color:{colors['danger']};font-size:112px;line-height:1.15}}
.sub{{position:absolute;left:72px;right:144px;top:1120px;text-align:center;color:#fff;font-size:66px;font-weight:700;line-height:1.35;z-index:10;text-shadow:0 2px 14px #000,0 0 4px #000}}
.alert span{{background:{colors['danger']};padding:4px 22px 8px;border-radius:8px;text-shadow:none;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
#shade{{position:absolute;inset:0;z-index:5;pointer-events:none;background:radial-gradient(ellipse at 50% 45%,transparent 55%,rgba(0,0,0,.5))}}
</style>
</head>
<body>
<div id="main" data-composition-id="main" data-start="0" data-duration="{ep.total}" data-width="{W}" data-height="{H}">
{chr(10).join(layers)}
<div id="shade"></div>
</div>
<script>
window.__timelines=window.__timelines||{{}};
const tl=gsap.timeline({{paused:true}});
{chr(10).join(script)}
window.__timelines["main"]=tl;
</script>
</body>
</html>
"""
    target = Path(video_dir)
    target.mkdir(parents=True, exist_ok=True)
    (target / "index.html").write_text(page, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("video")
    ap.add_argument("subtitles")
    ap.add_argument("--tail", type=float, default=2.5)
    ap.add_argument("--theme", default="night")
    args = ap.parse_args()
    spec = importlib.util.spec_from_file_location("episode", args.episode)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ep = Episode(json.loads(Path(args.subtitles).read_text(encoding="utf-8")), args.tail, args.theme)
    module.build(ep)
    render(ep, args.video)
    for item in ep.schedule():
        note = "  <- outside 2-8s" if not 2 <= item["dur"] <= 8 else ""
        print(f'{item["name"]:12} {item["start"]:7.2f} {item["dur"]:6.2f}{note}')
    print(f"total {ep.total}s")


if __name__ == "__main__":
    main()
