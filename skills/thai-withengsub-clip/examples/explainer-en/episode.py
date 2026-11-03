# English explainer demo. Use with --preset explainer-paper --subs primary. The claims are placeholders.
from compose import grow, pop, rise, sway
from draw import *


def build(ep):
    wave = sway("#@arm", 8, pivot="0% 100%")
    ep.sound("assets/drone.wav", volume=0.08)
    ep.shot("hook", line=0, art=plain() + host(500, 1920, 1.15, arm_id="@arm"),
            html=fact_card("@card", "Attention", "3 sec", top=560), motion=pop("#@card", 0.5) + wave, label="// 01 · hook", counter="1 / 3")
    ep.shot("why", line=2, art=plain() + host(500, 1920, 1.15, arm_id="@arm"),
            html=bars("@chart", "Where viewers leave", [("Slow intro", "High", 86), ("Middle", "Low", 28), ("Ending", "Low", 18)], top=540),
            motion=rise("#@chart", 0.2) + grow("#@chart-0", 0.6) + grow("#@chart-1", 0.8) + grow("#@chart-2", 1.0) + wave, label="// 02 · why", counter="2 / 3")
    ep.shot("cta", line=5, art=plain() + host(500, 1920, 1.15, arm_id="@arm"), html=pill("Comment GUIDE", 620), motion=wave, label="// 03 · next", counter="3 / 3")
