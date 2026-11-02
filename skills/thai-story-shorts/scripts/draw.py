"""Flat SVG parts for a 1080x1920 canvas. Each function returns an SVG string."""
import random

THEMES = {
    "night": dict(deep="#10172a", sky="#1d2a48", haze="#34466b", wall="#57617a", floor="#2e3448", metal="#8a93a6", paper="#f4efe3", ink="#272a33", danger="#d6423c", glow="#f4d27a", skin="#d9ae88", shirt="#4d7a78", dog="#c9a26b", dog_dark="#8d6c43"),
    "dusk": dict(deep="#26151f", sky="#5b2f3d", haze="#a35d4f", wall="#74584f", floor="#3f2e2d", metal="#a1928a", paper="#f7ecdc", ink="#30231f", danger="#c93a2e", glow="#ffc66e", skin="#d6a780", shirt="#3f6c7a", dog="#d7c3a2", dog_dark="#9a8466"),
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


def fact_card(card_id, heading, number, note=""):
    return f'<div class="fact" id="{card_id}">{heading}<b>{number}</b>{note}</div>'
