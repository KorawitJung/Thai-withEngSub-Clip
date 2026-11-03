"""Flat SVG parts for a 1080x1920 canvas. Each function returns an SVG string."""
import math
import random

import html as _html

_BASE = dict(text="#ffffff", muted="#aeb6c6", good="#2f8f5b", vignette=True, skin="#d9ae88", dog="#c9a26b", dog_dark="#8d6c43", paper="#f4efe3", ink="#272a33", danger="#d6423c", glow="#f4d27a")
THEMES = {
    "night": {**_BASE, "deep": "#10172a", "sky": "#1d2a48", "haze": "#34466b", "wall": "#57617a", "floor": "#2e3448", "metal": "#8a93a6", "shirt": "#4d7a78"},
    "dusk": {**_BASE, "deep": "#26151f", "sky": "#5b2f3d", "haze": "#a35d4f", "wall": "#74584f", "floor": "#3f2e2d", "metal": "#a1928a", "shirt": "#3f6c7a", "glow": "#ffc66e"},
    "horror": {**_BASE, "deep": "#07090d", "sky": "#141a22", "haze": "#26313c", "wall": "#1d242c", "floor": "#11161b", "metal": "#5d6a75", "shirt": "#3a4650", "danger": "#c1272d", "glow": "#f0b23c"},
    "paper": {**_BASE, "deep": "#efece6", "sky": "#efece6", "haze": "#d9d4ca", "wall": "#e4e0d8", "floor": "#d9d4ca", "metal": "#8f8b83", "shirt": "#6c675f", "text": "#17171a", "muted": "#7b7870", "paper": "#ffffff", "ink": "#17171a", "danger": "#d92c20", "glow": "#d92c20", "vignette": False},
    "clean": {**_BASE, "deep": "#faf9f6", "sky": "#faf9f6", "haze": "#ebe8e1", "wall": "#f1efe9", "floor": "#e4e1da", "metal": "#a8a49b", "shirt": "#8d897f", "text": "#1c1c1e", "muted": "#8c8a84", "paper": "#ffffff", "ink": "#1c1c1e", "danger": "#bd5a45", "glow": "#2f6fdb", "vignette": False},
}
_C = THEMES["night"]


def use_theme(name):
    global _C
    _C = THEMES[name]
    return _C


def backdrop(top=None, bottom=None, gid="bg"):
    top, bottom = top or _C["deep"], bottom or _C["sky"]
    return f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs><rect width="1080" height="1920" fill="url(#{gid})"/>'


def skyline(base=1100, seed=11, color=None):
    rng, out, x = random.Random(seed), "", -20
    color = color or _C["deep"]
    while x < 1100:
        width, height = rng.randint(90, 180), rng.randint(180, 620)
        out += f'<rect x="{x}" y="{base - height}" width="{width}" height="{height}" fill="{color}"/>'
        for row in range(2, height // 60):
            for col in range(1, width // 45):
                if rng.random() < 0.12:
                    out += f'<rect x="{x + col * 40}" y="{base - height + row * 52}" width="16" height="24" fill="{_C["glow"]}" opacity=".7"/>'
        x += width + rng.randint(4, 24)
    return out + f'<rect y="{base}" width="1080" height="{1920 - base}" fill="{color}"/>'


def room(floor_y=1100):
    return f'<rect width="1080" height="{floor_y}" fill="{_C["wall"]}"/><rect y="{floor_y}" width="1080" height="{1920 - floor_y}" fill="{_C["floor"]}"/>'


def elevator(doors_id=None):
    mark = f' id="{doors_id}"' if doors_id else ""
    return (
        f'<rect x="170" y="200" width="740" height="900" fill="{_C["metal"]}"/>'
        f'<g{mark}><rect x="200" y="230" width="336" height="870" fill="{_C["haze"]}"/><rect x="544" y="230" width="336" height="870" fill="{_C["haze"]}"/></g>'
    )


def vent(x, y, width=300, height=240):
    slats = "".join(f'<rect x="{x + 20}" y="{y + 24 + row * 42}" width="{width - 40}" height="18" fill="{_C["deep"]}"/>' for row in range((height - 24) // 42))
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="8" fill="{_C["metal"]}"/>{slats}'


def button_panel(x=900, y=760, lit_id=None):
    mark = f' id="{lit_id}"' if lit_id else ""
    out = f'<rect x="{x}" y="{y}" width="110" height="280" rx="12" fill="{_C["ink"]}"/>'
    out += "".join(f'<circle cx="{x + 55}" cy="{y + 50 + row * 60}" r="18" fill="{_C["metal"]}"/>' for row in range(3))
    return out + f'<circle{mark} cx="{x + 55}" cy="{y + 230}" r="24" fill="{_C["danger"]}"/>'


def person(x, y, scale=1.0, flip=False):
    sx = -scale if flip else scale
    return (
        f'<g transform="translate({x} {y}) scale({sx} {scale})">'
        f'<rect x="-38" y="-270" width="30" height="270" rx="14" fill="{_C["ink"]}"/><rect x="8" y="-270" width="30" height="270" rx="14" fill="{_C["ink"]}"/>'
        f'<rect x="-58" y="-540" width="116" height="300" rx="46" fill="{_C["shirt"]}"/>'
        f'<circle cy="-620" r="70" fill="{_C["skin"]}"/><path d="M-72 -628 A72 72 0 0 1 72 -628 L54 -650 L-54 -650Z" fill="{_C["ink"]}"/>'
        f'<circle cx="22" cy="-620" r="6" fill="{_C["ink"]}"/><circle cx="48" cy="-620" r="6" fill="{_C["ink"]}"/></g>'
    )


def dog(x, y, scale=1.0, flip=False, ear_id=None, tail_id=None):
    sx = -scale if flip else scale
    ear = f' id="{ear_id}"' if ear_id else ""
    tail = f' id="{tail_id}"' if tail_id else ""
    return (
        f'<g transform="translate({x} {y}) scale({sx} {scale})">'
        f'<path{tail} d="M-92 -70 Q-160 -110 -140 -180" fill="none" stroke="{_C["dog"]}" stroke-width="24" stroke-linecap="round"/>'
        f'<rect x="-110" y="-130" width="210" height="96" rx="46" fill="{_C["dog"]}"/>'
        f'<rect x="-92" y="-60" width="30" height="60" rx="10" fill="{_C["dog"]}"/><rect x="52" y="-60" width="30" height="60" rx="10" fill="{_C["dog"]}"/>'
        f'<rect x="58" y="-226" width="130" height="110" rx="42" fill="{_C["dog"]}"/><rect x="150" y="-176" width="66" height="50" rx="20" fill="{_C["dog_dark"]}"/>'
        f'<path{ear} d="M84 -220 L68 -292 L126 -226Z" fill="{_C["dog_dark"]}"/>'
        f'<circle cx="150" cy="-190" r="8" fill="{_C["ink"]}"/></g>'
    )


def beam(x, y, angle=20, beam_id=None):
    mark = f' id="{beam_id}"' if beam_id else ""
    return f'<polygon{mark} transform="translate({x} {y}) rotate({angle})" points="0,0 720,-180 720,180" fill="{_C["glow"]}" opacity=".3"/>'


def dark(opacity=0.6):
    return f'<rect width="1080" height="1920" fill="#000" opacity="{opacity}"/>'


def plain():
    return f'<rect width="1080" height="1920" fill="{_C["deep"]}"/>'


def host(x=540, y=1920, scale=1.0, flip=False, hat=None, arm_id=None):
    """Bust of an on-screen presenter, for explainer layouts. hat sets a cap color."""
    sx = -scale if flip else scale
    mark = f' id="{arm_id}"' if arm_id else ""
    cap = f'<path d="M-112 -470 A112 112 0 0 1 112 -470 Z" fill="{hat}"/>' if hat else f'<path d="M-112 -440 A112 112 0 0 1 112 -440 L80 -480 L-80 -480Z" fill="{_C["ink"]}"/>'
    return (
        f'<g transform="translate({x} {y}) scale({sx} {scale})">'
        f'<path d="M-230 0 Q-230 -270 -80 -300 L80 -300 Q230 -270 230 0Z" fill="{_C["shirt"]}"/>'
        f'<path{mark} d="M180 -120 Q300 -210 330 -340" fill="none" stroke="{_C["shirt"]}" stroke-width="58" stroke-linecap="round"/>'
        f'<circle cx="332" cy="-372" r="38" fill="{_C["skin"]}"/>'
        f'<rect x="-42" y="-340" width="84" height="70" fill="{_C["skin"]}"/>'
        f'<circle cy="-440" r="112" fill="{_C["skin"]}"/>{cap}'
        f'<circle cx="-40" cy="-440" r="9" fill="{_C["ink"]}"/><circle cx="40" cy="-440" r="9" fill="{_C["ink"]}"/>'
        f'<path d="M-30 -388 Q0 -366 30 -388" fill="none" stroke="{_C["ink"]}" stroke-width="7" stroke-linecap="round"/></g>'
    )


def _t(text):
    return _html.escape(str(text))


def fact_card(card_id, heading, number, note="", top=240, translation=""):
    extra = f"<small>{_t(translation)}</small>" if translation else ""
    return f'<div class="panel" id="{card_id}" style="top:{top}px">{_t(heading)}<b>{_t(number)}</b>{_t(note)}{extra}</div>'


def pill(text, top=200):
    return f'<div class="pill" style="top:{top}px">{_t(text)}</div>'


def clock(text):
    return f'<div class="chip">{_t(text)}</div>'


def versus(box_id, left, right, top=260):
    """left and right are (label, value) pairs; the right side is the better one."""
    return f'<div class="versus" id="{box_id}" style="top:{top}px"><div>{_t(left[0])}<b>{_t(left[1])}</b></div><div class="good">{_t(right[0])}<b>{_t(right[1])}</b></div></div>'


def bars(box_id, title, rows, top=380):
    """rows are (name, value, percent); the first row is highlighted. Fills get ids box_id-0, box_id-1, ..."""
    out = f'<div class="panel bars" id="{box_id}" style="top:{top}px">{_t(title)}'
    for number, (name, value, percent) in enumerate(rows):
        row = "row top" if number == 0 else "row"
        out += f'<div class="{row}"><span class="name">{_t(name)}</span><span class="track" style="display:block"><span id="{box_id}-{number}" class="fill" style="display:block;width:{percent}%"></span></span><span>{_t(value)}</span></div>'
    return out + "</div>"


def photo_card(card_id, src, credit, tag="", top=300, tilt=0, shown=False):
    """Real photo in a frame, with its credit always visible. src is relative to the video folder."""
    label = f'<span class="tag">{_t(tag)}</span>' if tag else ""
    style = f"top:{top}px" + (";opacity:1" if shown else "")
    return f'<div class="photo" id="{card_id}" style="{style}"><div style="transform:rotate({tilt}deg)">{label}<img src="{_t(src)}" alt=""></div><small>{_t(credit)}</small></div>'


def time_sky(progress, gid="sky", start=("#2a3a6b", "#f2a07c"), end=("#8cc8f0", "#e8f4f4")):
    """Sky that follows story time, from 0 (first light) to 1 (morning)."""
    def mix(a, b):
        return "#" + "".join(f"{round(int(a[k:k + 2], 16) * (1 - progress) + int(b[k:k + 2], 16) * progress):02x}" for k in (1, 3, 5))
    return backdrop(mix(start[0], end[0]), mix(start[1], end[1]), gid)


def signboard(sign_id, title, rule="", top=420):
    return f'<div class="sign" id="{sign_id}" style="top:{top}px">{_t(title)}<small>{_t(rule)}</small></div>'


def _map_path(points):
    return "M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in points)


def _route_parts(data, frame):
    """Project map_route.py data into frame, keeping real proportions around the stops."""
    x, y, w, h = frame
    lats, lons = [s[1] for s in data["stops"]], [s[2] for s in data["stops"]]
    mid_lat, mid_lon = (min(lats) + max(lats)) / 2, (min(lons) + max(lons)) / 2
    wide = math.cos(math.radians(mid_lat))
    scale = 0.8 * min(h / max(max(lats) - min(lats), 1e-4), w / max((max(lons) - min(lons)) * wide, 1e-4))

    def place(lat, lon):
        return x + w / 2 + (lon - mid_lon) * wide * scale, y + h / 2 - (lat - mid_lat) * scale

    route = [(lat, lon) for lon, lat in data["route"]]
    cuts = [0]
    for _, lat, lon in data["stops"][1:]:
        cuts.append(min(range(cuts[-1], len(route)), key=lambda i: (route[i][0] - lat) ** 2 + (route[i][1] - lon) ** 2))
    cuts[-1] = len(route) - 1
    segments = [_map_path(place(*p) for p in route[a:b + 1]) for a, b in zip(cuts, cuts[1:])]
    return place, segments


def route_map(data, count=None, done=None, drawing=None, active=None, labels=None, frame=(50, 220, 980, 880), line="#ff5a5f", land="#fff6dd", water="#7fd6f5", border="#ffc93c"):
    """Map from map_route.py. Returns (art, html); pass them to ep.shot with route_motion when a leg is drawing.

    count: stops shown. done: finished legs. drawing: leg to animate. active: stop to highlight, its label gets id @tag.
    labels: {stop name: text or (text, dx, dy)}. Credit the map: (c) OpenStreetMap contributors.
    """
    stops = data["stops"]
    count = len(stops) if count is None else count
    place, segments = _route_parts(data, frame)
    done = len(segments) if done is None else done
    labels = labels or {}
    x, y, w, h = frame
    wet, big, small = "", "", ""
    for way in data["ways"]:
        tags, path = way["tags"], _map_path(place(*p) for p in way["pts"])
        if tags.get("waterway") == "river":
            wet += f'<path d="{path}" fill="none" stroke="{water}" stroke-width="100" stroke-linejoin="round"/>'
        elif tags.get("natural") == "water":
            wet += f'<path d="{path}" fill="{water}" stroke="{water}" stroke-width="4"/>'
        elif tags.get("highway") in ("primary", "secondary"):
            big += path
        elif tags.get("highway"):
            small += path
    stroke = f'fill="none" stroke="{line}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"'
    art = (f'<defs><clipPath id="@mapclip"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="36"/></clipPath></defs>'
           f'<g clip-path="url(#@mapclip)"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{land}"/>{wet}'
           f'<path d="{small}" fill="none" stroke="#eadfc0" stroke-width="5"/><path d="{big}" fill="none" stroke="#e6d6a8" stroke-width="10"/></g>'
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="36" fill="none" stroke="{border}" stroke-width="8"/>')
    art += "".join(f'<path d="{segment}" {stroke}/>' for segment in segments[:done])
    if drawing is not None:
        art += f'<path id="@seg" d="{segments[drawing]}" pathLength="1" stroke-dasharray="1" {stroke}/>'
    tags = ""
    for number, (key, lat, lon) in enumerate(stops[:count]):
        px, py = place(lat, lon)
        art += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="20" fill="#fff" stroke="{line}" stroke-width="8"/>'
        label = labels.get(key, key)
        text, dx, dy = (label, 30, -30) if isinstance(label, str) else label
        back, ink = (line, "#fff") if number == active else ("#fff", "#23323a")
        tag_id = ' id="@tag"' if number == active else ""
        tags += f'<div{tag_id} style="position:absolute;left:{px + dx:.0f}px;top:{py + dy:.0f}px;padding:6px 20px;border-radius:30px;background:{back};color:{ink};font-size:36px;font-weight:600;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,.18)">{number + 1}. {_t(text)}</div>'
    return art, tags


def route_motion(share=0.85):
    """Draw the @seg leg of route_map across most of the shot."""
    return f'tl.fromTo("#@seg",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:D*{share},ease:"none"}},T+.05);\n'


def end_card(logo, top=340, width=780):
    """Logo for a still closing shot; keep it on screen with compose.py --hold."""
    return f'<img src="{_t(logo)}" alt="" style="position:absolute;left:{(1080 - width) // 2}px;top:{top}px;width:{width}px">'
