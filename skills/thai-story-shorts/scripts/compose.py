"""Write a single-file HyperFrames project from an episode script.

usage: compose.py episode.py video_dir subtitles.json [--preset story-night] [--subs both] [--tail 2.5]

episode.py defines build(ep). Shots start on a subtitle line and last until the next shot,
so timing follows the narration. In art, html and motion, "@name" becomes a shot-unique id.
Motion code can use tl (timeline), T (shot start) and D (shot length).
Subtitle text accepts *word* for accent styling.
--subs: both = show + sub, primary = show only, secondary = sub only.
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
import draw  # noqa: E402
import fonts  # noqa: E402

GSAP = "https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"
FONT_FACES = """@font-face{font-family:"Thai Story";font-weight:400 600;src:local("Leelawadee UI"),local("Sukhumvit Set Medium"),local("Noto Sans Thai"),local("Tahoma")}
@font-face{font-family:"Thai Story";font-weight:700;src:local("Leelawadee UI Bold"),local("Sukhumvit Set Bold"),local("Noto Sans Thai Bold"),local("Tahoma Bold")}"""
FALLBACK = '"Thai Story",sans-serif'

PRESETS = {
    "story-night": dict(theme="night", captions="cinema", th="kanit", en="inter", accent="kanit"),
    "story-warm": dict(theme="dusk", captions="cinema", th="mitr", en="rubik", accent="mitr"),
    "horror-rules": dict(theme="horror", captions="stack", th="chakra-petch", en="oswald", accent="chakra-petch"),
    "explainer-paper": dict(theme="paper", captions="headline", th="prompt", en="inter", accent="playfair"),
    "data-clean": dict(theme="clean", captions="spotlight", th="ibm-thai", en="inter", accent="ibm-thai"),
}


def rise(target, at):
    return f'tl.fromTo("{target}",{{y:36,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"power2.out"}},T+{at});\n'


def pop(target, at):
    return f'tl.fromTo("{target}",{{scale:.7,opacity:0}},{{scale:1,opacity:1,duration:.3,ease:"back.out(2)"}},T+{at});\n'


def sway(target, angle, at=0, each=0.7, times=4, pivot="50% 100%"):
    return f'tl.fromTo("{target}",{{rotation:0,transformOrigin:"{pivot}"}},{{rotation:{angle},transformOrigin:"{pivot}",duration:{each},ease:"sine.inOut",yoyo:true,repeat:{times - 1}}},T+{at});\n'


def flicker(target, at=0, times=6):
    return f'tl.fromTo("{target}",{{opacity:1}},{{opacity:.25,duration:.12,ease:"none",yoyo:true,repeat:{times - 1}}},T+{at});\n'


def grow(target, at=0, each=0.5):
    return f'tl.fromTo("{target}",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,transformOrigin:"0% 50%",duration:{each},ease:"power2.out"}},T+{at});\n'


def rich(text):
    safe = html.escape(text)
    return re.sub(r"\*([^*]+)\*", r'<em>\1</em>', safe).replace("|", "<br>")


def chunks(text):
    """Split display text into reveal words; an *accent* spanning several words stays accented on each."""
    units = []
    for number, part in enumerate(re.split(r"\*", text)):
        for word in part.replace("|", " ").split():
            units.append(f"*{word}*" if number % 2 else word)
    return units


class Episode:
    def __init__(self, subtitles, tail=2.5, preset="story-night", subs="both"):
        if preset not in PRESETS:
            raise ValueError(f"unknown preset: {preset}; choose from {', '.join(PRESETS)}")
        if subs not in ("both", "primary", "secondary"):
            raise ValueError(f"unknown subs mode: {subs}")
        self.subtitles = subtitles
        self.tail = tail
        self.preset = preset
        self.captions = PRESETS[preset]["captions"]
        self.theme = draw.use_theme(PRESETS[preset]["theme"])
        self.subs = subs
        self.fonts = {role: PRESETS[preset][role] for role in ("th", "en", "accent")}
        self.font_faces = ""
        self.font_body = FALLBACK
        self.font_accent = FALLBACK
        self.brand = ""
        self.closing = None
        self.shots = []
        self.sounds = []

    def shot(self, name, line, art, html="", motion="", zoom=1.06, focus="50% 50%", label="", counter=""):
        if not re.fullmatch(r"[a-z][a-z0-9-]*", name):
            raise ValueError(f"bad shot name: {name}")
        if not 0 <= line < len(self.subtitles):
            raise ValueError(f"shot {name}: no subtitle line {line}")
        if self.shots and line <= self.shots[-1]["line"]:
            raise ValueError(f"shot {name}: line {line} must come after the previous shot")
        if any(item["name"] == name for item in self.shots):
            raise ValueError(f"duplicate shot: {name}")
        self.shots.append(dict(name=name, line=line, art=art, html=html, motion=motion, zoom=zoom, focus=focus, label=label, counter=counter))

    def sound(self, src, start=0.0, volume=1.0, automation=None):
        self.sounds.append(dict(src=src, start=start, volume=volume, automation=automation))

    def outro(self, name, handle=""):
        self.closing = dict(name=name, handle=handle)

    def use_fonts(self, video_dir):
        """Install the chosen fonts; the English font comes first because Thai fonts carry their own Latin letters."""
        chosen = self.fonts
        self.font_faces = fonts.install(chosen.values(), video_dir)
        self.font_body = f'{fonts.stack(chosen["en"], chosen["th"])},{FALLBACK}'
        self.font_accent = f'{fonts.stack(chosen["accent"], chosen["th"])},{FALLBACK}'

    @property
    def speech_end(self):
        return self.subtitles[-1]["out"]

    @property
    def total(self):
        return round(self.speech_end + self.tail, 3)

    def schedule(self):
        if not self.shots:
            raise ValueError("episode has no shots")
        if self.shots[0]["line"] != 0:
            raise ValueError("the first shot must start on line 0")
        last_end = self.speech_end if self.closing else self.total
        timed = []
        for number, item in enumerate(self.shots):
            start = 0.0 if number == 0 else self.subtitles[item["line"]]["in"]
            end = last_end if number + 1 == len(self.shots) else self.subtitles[self.shots[number + 1]["line"]]["in"]
            timed.append({**item, "start": round(start, 3), "dur": round(end - start, 3)})
        return timed


def audio_length(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    if out.returncode:
        raise ValueError(f"cannot read audio: {path}")
    return float(out.stdout)


def caption_layers(ep):
    layers, script = [], []
    for number, sub in enumerate(ep.subtitles):
        first, second = sub["show"], sub.get("sub", "")
        if ep.subs == "primary":
            second = ""
        elif ep.subs == "secondary" and second:
            first, second = second, ""
        cid = f"sub-{number}"
        kind = f"sub {ep.captions}" + (" alert" if sub.get("alert") else "")
        timing = f'data-start="{sub["in"]}" data-duration="{round(sub["out"] - sub["in"], 3)}" data-track-index="3"'
        if ep.captions in ("headline", "spotlight"):
            parts = []
            units = chunks(first)
            span = max(0.1, sub["end"] - sub["start"])
            for index, unit in enumerate(units):
                wid = f"{cid}-w{index}"
                parts.append(f'<span class="word" id="{wid}">{rich(unit)}</span>')
                at = sub["start"] + span * index / len(units)
                start_style = "{opacity:0,y:18}" if ep.captions == "headline" else "{opacity:.25,y:0}"
                script.append(f'tl.fromTo("#{wid}",{start_style},{{opacity:1,y:0,duration:.16,ease:"power2.out"}},{at:.3f});')
            body = f'<div class="main">{" ".join(parts)}</div>'
        else:
            body = f'<div class="main"><span>{rich(first)}</span></div>'
        if second:
            body += f'<div class="second"><span>{rich(second)}</span></div>'
        layers.append(f'<div id="{cid}" class="clip {kind}" {timing}>{body}</div>')
    return layers, script


def render(ep, video_dir):
    W, H = 1080, 1920
    colors = ep.theme
    layers, script = [], []
    for item in ep.schedule():
        pid = item["name"]
        fix = lambda text: re.sub(r"@([a-z][a-z0-9-]*)", rf"{pid}-\1", text)
        chrome = ""
        if item["label"]:
            chrome += f'<div class="section">{html.escape(item["label"])}</div>'
        if item["counter"]:
            chrome += f'<div class="counter">{html.escape(item["counter"])}</div>'
        layers.append(
            f'<div id="{pid}" class="clip shot" data-start="{item["start"]}" data-duration="{item["dur"]}" data-track-index="1">'
            f'<div id="{pid}-cam" class="cam" style="transform-origin:{item["focus"]}">'
            f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{fix(item["art"])}</svg></div>{fix(item["html"])}{chrome}</div>'
        )
        script.append(
            f'(function(T,D){{tl.fromTo("#{pid}-cam",{{scale:1}},{{scale:{item["zoom"]},duration:D,ease:"sine.inOut"}},T);\n{fix(item["motion"])}}})({item["start"]},{item["dur"]});'
        )
    if ep.closing:
        handle = f'<div class="handle">{html.escape(ep.closing["handle"])}</div>' if ep.closing["handle"] else ""
        layers.append(f'<div id="closing" class="clip closing" data-start="{ep.speech_end}" data-duration="{round(ep.total - ep.speech_end, 3)}" data-track-index="1"><div id="closing-name" class="name">{html.escape(ep.closing["name"])}</div>{handle}</div>')
        script.append(f'(function(T){{{rise("#closing-name", 0.1)}}})({ep.speech_end});')
    captions, caption_script = caption_layers(ep)
    layers += captions
    script += caption_script
    for number, sound in enumerate(ep.sounds):
        path = Path(video_dir) / sound["src"]
        length = round(min(audio_length(path), ep.total - sound["start"]), 3)
        extra = f" data-automation='{json.dumps(sound['automation'])}'" if sound["automation"] else ""
        layers.append(f'<audio id="snd-{number}" class="clip" src="{sound["src"]}" data-start="{sound["start"]}" data-duration="{length}" data-track-index="{10 + number}" data-volume="{sound["volume"]}"{extra}></audio>')
    brand = f'<div id="brand">{html.escape(ep.brand)}</div>' if ep.brand else ""
    vignette = '<div id="shade"></div>' if colors["vignette"] else ""
    page = f"""<!doctype html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}">
<script src="{GSAP}"></script>
<style>
{FONT_FACES}
{ep.font_faces}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{colors['deep']}}}
#main{{position:relative;width:{W}px;height:{H}px;overflow:hidden;font-family:{ep.font_body};color:{colors['text']}}}
.shot,.closing,.cam,.cam svg{{position:absolute;inset:0;width:{W}px;height:{H}px}}
.shot,.closing{{overflow:hidden;z-index:1}}
.closing{{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;background:{colors['deep']}}}
.closing .name{{font-size:96px;font-weight:700;opacity:0}}.closing .handle{{font-size:42px;color:{colors['muted']}}}
.section,.counter{{position:absolute;top:190px;font:500 26px "JetBrains Mono",monospace;color:{colors['muted']}}}
.section{{left:90px}}.counter{{right:150px}}
#brand{{position:absolute;top:190px;right:150px;z-index:6;font-size:32px;font-weight:700;color:{colors['danger']}}}
.panel{{position:absolute;left:96px;right:144px;padding:32px 40px;border-radius:16px;background:{colors['paper']};color:{colors['ink']};opacity:0;font-size:42px;font-weight:600;line-height:1.35;box-shadow:0 18px 40px rgba(0,0,0,.25)}}
.panel b{{display:block;color:{colors['danger']};font-size:112px;line-height:1.4}}
.panel small{{display:block;margin-top:6px;font-size:28px;font-weight:500;opacity:.65}}
.pill{{position:absolute;left:50%;transform:translateX(-50%);padding:12px 32px;border-radius:40px;background:{colors['danger']};color:#fff;font-size:34px;font-weight:600;white-space:nowrap}}
.chip{{position:absolute;left:90px;top:220px;padding:10px 24px;border-radius:10px;background:{colors['paper']};color:{colors['ink']};font-size:36px;font-weight:700}}
.versus{{display:flex;gap:18px;position:absolute;left:96px;right:144px;opacity:0}}
.versus>div{{flex:1;padding:26px 16px;border-radius:14px;background:{colors['paper']};color:{colors['ink']};text-align:center;font-size:32px;font-weight:600}}
.versus b{{display:block;font-size:68px;color:{colors['danger']}}}.versus .good b{{color:{colors['good']}}}
.bars .row{{display:flex;align-items:center;gap:16px;margin-top:18px;font-size:32px}}
.bars .name{{width:220px;flex:none}}.bars .track{{flex:1;height:34px;border-radius:17px;background:rgba(0,0,0,.08)}}
.bars .fill{{height:100%;border-radius:17px;background:{colors['muted']}}}.bars .row.top .fill{{background:{colors['danger']}}}
.sign{{position:absolute;left:90px;right:150px;padding:36px 44px;border:10px solid {colors['metal']};border-radius:8px;background:{colors['floor']};color:{colors['glow']};opacity:0;font-size:46px;font-weight:700;line-height:1.3}}
.sign small{{display:block;font-size:34px;font-weight:500;color:{colors['text']}}}
.sub{{position:absolute;left:72px;right:144px;text-align:center;z-index:10}}
.sub em{{font-style:normal;color:{colors['glow']}}}
.sub.cinema,.sub.stack{{top:1120px}}
.cinema .main,.stack .main{{color:#fff;font-size:64px;font-weight:700;line-height:1.3;text-shadow:0 2px 14px #000,0 0 4px #000}}
.cinema .second span{{display:inline-block;margin-top:12px;padding:5px 18px;border-radius:8px;background:rgba(0,0,0,.55);color:#fff;font-size:36px;font-weight:500}}
.stack .second span{{display:inline-block;margin-top:10px;padding:4px 20px;border-radius:6px;background:{colors['danger']};color:#fff;font-size:50px;font-weight:700}}
.alert.cinema .main span,.alert.stack .main span{{background:{colors['danger']};padding:4px 22px 8px;border-radius:8px;text-shadow:none;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.sub.headline{{top:240px;left:90px;right:150px;text-align:left}}
.headline .main{{color:{colors['text']};font-size:70px;font-weight:600;line-height:1.2}}
.headline em,.spotlight em{{font-family:{ep.font_accent};font-style:italic;font-weight:500;color:{colors['danger']}}}
.headline .second{{margin-top:12px;color:{colors['muted']};font-size:36px}}
.sub.spotlight{{top:1120px}}
.spotlight .main{{color:{colors['text']};font-size:58px;font-weight:600;line-height:1.3}}
.spotlight .second{{margin-top:10px;color:{colors['muted']};font-size:34px}}
.word{{display:inline-block;margin-right:.08em}}
#shade{{position:absolute;inset:0;z-index:5;pointer-events:none;background:radial-gradient(ellipse at 50% 45%,transparent 55%,rgba(0,0,0,.5))}}
</style>
</head>
<body>
<div id="main" data-composition-id="main" data-start="0" data-duration="{ep.total}" data-width="{W}" data-height="{H}">
{chr(10).join(layers)}
{brand}
{vignette}
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
    ap.add_argument("--preset", default="story-night", choices=sorted(PRESETS))
    ap.add_argument("--subs", default="both", choices=["both", "primary", "secondary"])
    ap.add_argument("--font-th", help="Thai font id, see fonts.py list")
    ap.add_argument("--font-en", help="English font id")
    ap.add_argument("--font-accent", help="font id for *accent* words")
    ap.add_argument("--system-fonts", action="store_true", help="skip downloads and use fonts already on this computer")
    args = ap.parse_args()
    ep = Episode(json.loads(Path(args.subtitles).read_text(encoding="utf-8")), args.tail, args.preset, args.subs)
    for role, value in (("th", args.font_th), ("en", args.font_en), ("accent", args.font_accent)):
        if value:
            ep.fonts[role] = value
    if not args.system_fonts:
        try:
            ep.use_fonts(args.video)
        except OSError as err:
            sys.exit(f"Could not download fonts ({err}). Check the connection or pass --system-fonts.")
    spec = importlib.util.spec_from_file_location("episode", args.episode)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.build(ep)
    render(ep, args.video)
    for item in ep.schedule():
        note = "  <- outside 2-8s" if not 2 <= item["dur"] <= 8 else ""
        print(f'{item["name"]:12} {item["start"]:7.2f} {item["dur"]:6.2f}{note}')
    print(f"total {ep.total}s")


if __name__ == "__main__":
    main()
