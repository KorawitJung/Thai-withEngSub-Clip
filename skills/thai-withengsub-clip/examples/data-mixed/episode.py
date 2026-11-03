# Mixed Thai and English data demo. Use with --preset data-clean. All figures are sample data.
from compose import grow, pop, rise
from draw import *


def build(ep):
    ep.sound("assets/drone.wav", volume=0.06)
    ep.shot("intro", line=0, art=plain(), html=pill("ข้อมูลตัวอย่าง · Sample data", 260) + fact_card("@card", "Daily brief", "20 sec", top=480), motion=pop("#@card", 0.3))
    ep.shot("growth", line=1, art=plain(), html=pill("1) รายได้ · Revenue", 260) + bars("@chart", "ไตรมาสนี้ · This quarter", [("Now", "+40%", 90), ("Before", "+12%", 30)], top=480),
            motion=rise("#@chart", 0.1) + grow("#@chart-0", 0.5) + grow("#@chart-1", 0.7))
    ep.shot("cost", line=2, art=plain(), html=pill("2) ค่าใช้จ่าย · Cost", 260) + versus("@box", ("ก่อน · Before", "100"), ("ตอนนี้ · Now", "50"), top=500), motion=rise("#@box", 0.2))
    ep.shot("end", line=3, art=plain(), html=pill("ติดตาม · Follow", 500), zoom=1.03)
