# Short demo that exercises the pipeline. Its story and advice are placeholders, not checked safety guidance.
from compose import flicker, rise, sway
from draw import *


def build(ep):
    ep.sound("assets/drone.wav", volume=0.2)
    ep.shot("lift", line=0, art=room() + elevator() + person(540, 1085, 1.15) + dark(0.3), zoom=1.08)
    ep.shot("panel", line=2, art=room() + button_panel(485, 610, lit_id="@alarm"),
            html=fact_card("@card", "ขั้นแรก", "กดปุ่ม", "เรียกความช่วยเหลือ"),
            motion=rise("#@card", 0.2) + flicker("#@alarm", 0.5), focus="50% 35%")
    ep.shot("dog", line=4, art=room() + vent(690, 300) + dog(330, 1085, 1.4, ear_id="@ear", tail_id="@tail") + dark(0.35),
            motion=sway("#@ear", 12) + sway("#@tail", -14, pivot="0% 100%"))
    ep.shot("end", line=6, art=room() + vent(620, 540) + beam(0, 660, 0, beam_id="@beam") + dark(0.5), motion=flicker("#@beam", 0.2), zoom=1.03)
