import argparse
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "skills" / "thai-withengsub-clip"
SCRIPTS = ROOT / "scripts"
DEMO = ROOT / "examples" / "demo"
sys.path.insert(0, str(SCRIPTS))

import audio_check  # noqa: E402
import compose  # noqa: E402
import cover  # noqa: E402
import draw  # noqa: E402
import fonts  # noqa: E402
import master  # noqa: E402
import music  # noqa: E402
import pace  # noqa: E402
import sfx  # noqa: E402
import soundscape  # noqa: E402
import tighten  # noqa: E402
import timing  # noqa: E402


class TimingTests(unittest.TestCase):
    def test_lines_are_ordered_and_do_not_overlap(self):
        text = (DEMO / "narration.txt").read_text(encoding="utf-8").strip()
        lines = json.loads((DEMO / "lines.json").read_text(encoding="utf-8"))
        timed = timing.build_subtitles(lines, timing.estimate_alignment(text))
        self.assertEqual(len(timed), len(lines))
        for first, second in zip(timed, timed[1:]):
            self.assertLessEqual(first["out"], second["in"])

    def test_missing_line_is_reported(self):
        with self.assertRaises(ValueError):
            timing.build_subtitles([{"say": "ไม่มีคำนี้", "show": "x"}], timing.estimate_alignment("สวัสดี"))


class SnapTests(unittest.TestCase):
    def test_edges_leave_silence(self):
        timed = [{"start": 1.0, "end": 3.0}, {"start": 8.16, "end": 11.0}]
        moved = timing.snap_to_audio(timed, [(2.5, 3.5), (7.5, 8.66)])
        self.assertEqual(moved, 2)
        self.assertEqual(timed[0]["end"], 2.5)
        self.assertEqual(timed[1]["start"], 8.66)

    def test_short_blip_does_not_split_a_pause(self):
        timed = [{"start": 6.12, "end": 8.0}]
        timing.snap_to_audio(timed, [(5.76, 6.06), (6.12, 6.33)])
        self.assertEqual(timed[0]["start"], 6.33)

    def test_line_in_speech_or_all_silent_is_kept(self):
        timed = [{"start": 1.0, "end": 2.0}, {"start": 5.2, "end": 5.8}]
        self.assertEqual(timing.snap_to_audio(timed, [(5.0, 6.0)]), 0)
        self.assertEqual(timed[1]["start"], 5.2)


class ComposeTests(unittest.TestCase):
    def subtitles(self):
        return [{"show": "ก", "alert": False, "start": k * 3, "end": k * 3 + 2, "in": k * 3, "out": k * 3 + 2} for k in range(3)]

    def test_shots_follow_subtitles(self):
        ep = compose.Episode(self.subtitles(), tail=1)
        ep.shot("a", 0, "")
        ep.shot("b", 2, "")
        first, second = ep.schedule()
        self.assertEqual((first["start"], first["dur"]), (0.0, 6))
        self.assertEqual((second["start"], second["dur"]), (6, 3))

    def test_shots_must_move_forward(self):
        ep = compose.Episode(self.subtitles())
        ep.shot("a", 1, "")
        with self.assertRaises(ValueError):
            ep.shot("b", 1, "")

    def test_ids_are_scoped_and_thai_is_utf8(self):
        with tempfile.TemporaryDirectory() as folder:
            ep = compose.Episode([{**self.subtitles()[0], "show": "ภาษาไทย"}])
            ep.shot("a", 0, '<rect id="@box"/>', motion='tl.set("#@box",{x:1},T);')
            compose.render(ep, folder)
            page = (Path(folder) / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="a-box"', page)
        self.assertIn('"#a-box"', page)
        self.assertIn("ภาษาไทย", page)


class LanguageTests(unittest.TestCase):
    def page(self, preset, subs):
        line = {"show": "สวัสดี *โลก*", "sub": "Hello <world>", "alert": False, "start": 0, "end": 2, "in": 0, "out": 2}
        with tempfile.TemporaryDirectory() as folder:
            ep = compose.Episode([line], preset=preset, subs=subs)
            ep.shot("a", 0, "")
            compose.render(ep, folder)
            return (Path(folder) / "index.html").read_text(encoding="utf-8")

    def test_both_languages_are_shown_and_escaped(self):
        page = self.page("story-night", "both")
        self.assertIn("<em>โลก</em>", page)
        self.assertIn("Hello &lt;world&gt;", page)

    def test_subtitle_modes(self):
        self.assertNotIn("Hello", self.page("story-night", "primary"))
        secondary = self.page("story-night", "secondary")
        self.assertIn("Hello", secondary)
        self.assertNotIn('<span>สวัสดี', secondary)

    def test_every_preset_renders(self):
        for preset in compose.PRESETS:
            self.assertIn(f'class="clip sub {compose.PRESETS[preset]["captions"]}', self.page(preset, "both"))

    def test_mixed_language_estimate_finds_lines(self):
        text = "ข่าววันนี้ in twenty seconds."
        timed = timing.build_subtitles([{"say": "in twenty seconds", "show": "x", "sub": "y"}], timing.estimate_alignment(text))
        self.assertEqual(timed[0]["sub"], "y")
        self.assertGreater(timed[0]["end"], timed[0]["start"])


class FontTests(unittest.TestCase):
    def test_accent_can_span_words(self):
        self.assertEqual(compose.chunks("in *20 seconds* now|ok"), ["in", "*20*", "*seconds*", "now", "ok"])

    def test_preset_fonts_exist(self):
        for preset in compose.PRESETS.values():
            for role in ("th", "en", "accent"):
                self.assertIn(preset[role], fonts.LIBRARY)

    def test_install_uses_cached_files_once(self):
        with tempfile.TemporaryDirectory() as folder:
            original = fonts.CACHE
            fonts.CACHE = Path(folder) / "cache"
            fonts.CACHE.mkdir()
            for weight in (500, 700):
                (fonts.CACHE / f"kanit-{weight}.ttf").write_bytes(b"x")
            try:
                css = fonts.install(["kanit", "kanit"], Path(folder) / "video")
            finally:
                fonts.CACHE = original
            self.assertEqual(css.count("@font-face"), 2)
            self.assertTrue((Path(folder) / "video" / "assets" / "fonts" / "kanit-700.ttf").exists())

    def test_unknown_font_is_rejected(self):
        with self.assertRaises(ValueError):
            fonts.install(["nope"], "unused")


class AudioToolTests(unittest.TestCase):
    def make_tone_gap_tone(self, path):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=f=440:d=1", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono:d=2", "-f", "lavfi", "-i", "sine=f=440:d=1",
                        "-filter_complex", "[0:a]aresample=44100,aformat=channel_layouts=mono[a];[2:a]aresample=44100,aformat=channel_layouts=mono[c];[a][1:a][c]concat=n=3:v=0:a=1[o]", "-map", "[o]", str(path)], check=True)

    def test_remap_follows_removed_silence(self):
        spans = tighten.keep_spans([(1.0, 3.0)], 4.0, 0.4)
        self.assertEqual(spans, [(0.0, 1.2), (2.8, 4.0)])
        self.assertEqual(tighten.remap(1.0, spans), 1.0)
        self.assertEqual(tighten.remap(3.0, spans), 1.4)
        self.assertEqual(tighten.remap(4.0, spans, 2.0), 1.2)

    def test_tighten_shortens_audio_and_alignment(self):
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder)
            self.make_tone_gap_tone(work / "n.wav")
            (work / "a.json").write_text(json.dumps({"characters": ["ก", "ข"], "character_start_times_seconds": [0.0, 3.0], "character_end_times_seconds": [1.0, 4.0]}), encoding="utf-8")
            subprocess.run([sys.executable, str(SCRIPTS / "tighten.py"), str(work / "n.wav"), str(work / "a.json"), str(work / "out"), "--max-gap", "0.4"], check=True, capture_output=True)
            self.assertAlmostEqual(tighten.duration_of(work / "out" / "narration.wav"), 2.4, delta=0.1)
            data = json.loads((work / "out" / "alignment.json").read_text(encoding="utf-8"))
            self.assertAlmostEqual(data["character_start_times_seconds"][1], 1.4, delta=0.1)

    def test_music_extend_reaches_length(self):
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder)
            self.make_tone_gap_tone(work / "raw.wav")
            music.extend(work / "raw.wav", 10, work / "long.wav")
            self.assertAlmostEqual(tighten.duration_of(work / "long.wav"), 10, delta=0.1)

    def test_sfx_search_filters_license_unless_asked(self):
        self.assertIn("license_type=commercial", sfx.search_url("rain", 3))
        self.assertNotIn("license_type", sfx.search_url("rain", 3, any_license=True))

    def test_master_writes_review_and_flags_problems(self):
        good = {"width": 1080, "height": 1920, "seconds": 60.0, "lufs": -14.1}
        self.assertEqual(master.problems(good, -14, 90), [])
        self.assertEqual(len(master.problems({"width": 720, "height": 1280, "seconds": 120.0, "lufs": None}, -14, 90)), 3)
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=black:s=1080x1920:d=3:r=30", "-f", "lavfi", "-i", "sine=f=440:d=3", "-shortest", "-c:v", "libx264", "-c:a", "aac", str(work / "r.mp4")], check=True)
            subprocess.run([sys.executable, str(SCRIPTS / "master.py"), str(work / "r.mp4"), str(work / "ep1.mp4")], check=True, capture_output=True)
            self.assertIn("1080x1920", (work / "ep1-review.md").read_text(encoding="utf-8"))

    def test_new_sounds_are_generated(self):
        for name in ("rain", "wind"):
            self.assertTrue(any(getattr(soundscape, name)(0.5)))
        self.assertEqual(len(soundscape.bubbles()), int(1.5 * soundscape.RATE))


class PaceTests(unittest.TestCase):
    def lines(self):
        return [{"show": str(k), "start": k * 1.0 + 0.1, "end": k * 1.0 + 0.9} for k in range(3)]

    def test_gaps_reach_minimum_and_pads_add_up(self):
        _, timed = pace.plan(self.lines(), 3.0, min_gap=0.5, pads={2: 0.25})
        self.assertAlmostEqual(timed[1]["start"] - timed[0]["end"], 0.5, places=3)
        self.assertAlmostEqual(timed[2]["start"] - timed[1]["end"], 0.75, places=3)

    def test_large_gap_is_kept_and_cut_is_mid_gap(self):
        lines = [{"show": "a", "start": 0.0, "end": 1.0}, {"show": "b", "start": 3.0, "end": 4.0}]
        pieces, timed = pace.plan(lines, 4.0, min_gap=0.4)
        self.assertEqual(pieces[0][:2], (0.0, 2.0))
        self.assertEqual(timed[1]["start"], 3.0)

    def test_drop_removes_the_line_and_its_audio(self):
        pieces, timed = pace.plan(self.lines(), 3.0, min_gap=0.0, drop={1})
        self.assertEqual([item["show"] for item in timed], ["0", "2"])
        self.assertEqual(len(pieces), 2)

    def test_audio_length_matches_plan(self):
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=f=440:d=3", str(work / "n.wav")], check=True)
            (work / "s.json").write_text(json.dumps(self.lines()), encoding="utf-8")
            subprocess.run([sys.executable, str(SCRIPTS / "pace.py"), str(work / "n.wav"), str(work / "s.json"), str(work / "out"), "--min-gap", "0.5", "--pad", "2=0.3"], check=True, capture_output=True)
            timed = json.loads((work / "out" / "subtitles.json").read_text(encoding="utf-8"))
            self.assertAlmostEqual(tighten.duration_of(work / "out" / "narration.wav"), timed[-1]["end"] + 0.1, delta=0.05)


class ChannelAndCoverTests(unittest.TestCase):
    def test_channel_fills_only_what_is_unset(self):
        line = {"show": "ก", "start": 0, "end": 1, "in": 0, "out": 1}
        ep = compose.Episode([line])
        ep.brand = "ของตอนนี้"
        compose.apply_channel(ep, {"brand": "ช่อง", "still": True, "outro": {"name": "ช่อง"}})
        self.assertEqual(ep.brand, "ของตอนนี้")
        self.assertTrue(ep.still)
        self.assertEqual(ep.closing["name"], "ช่อง")

    def test_template_channel_uses_real_preset_and_fonts(self):
        channel = json.loads((ROOT / "templates" / "channel.json").read_text(encoding="utf-8"))
        self.assertIn(channel["preset"], compose.PRESETS)
        for font in channel["fonts"].values():
            self.assertIn(font, fonts.LIBRARY)

    def test_still_turns_off_camera_zoom(self):
        line = {"show": "ก", "start": 0, "end": 1, "in": 0, "out": 1}
        with tempfile.TemporaryDirectory() as folder:
            ep = compose.Episode([line])
            ep.still = True
            ep.shot("a", 0, "", zoom=1.5)
            compose.render(ep, folder)
            self.assertNotIn("scale:1.5", (Path(folder) / "index.html").read_text(encoding="utf-8"))

    def test_photo_card_shows_escaped_credit(self):
        card = draw.photo_card("x", "assets/a.jpg", "ภาพ: A<B> · CC BY 4.0", tag="ภาพจริง")
        self.assertIn("A&lt;B&gt;", card)
        self.assertIn("assets/a.jpg", card)

    def test_cover_requires_credit_for_photo(self):
        args = argparse.Namespace(out="unused", title="ก", kicker="", sub="", photo="a.jpg", inset=None, tag="", credit="", logo=None, preset="story-night", system_fonts=True)
        with self.assertRaises(SystemExit):
            cover.build(args)


class AudioCheckTests(unittest.TestCase):
    def test_flags_loud_and_hissy_bed_and_suggests_volume(self):
        found = audio_check.report(-16, {"full": -16, "treble": -20, "mid": -40}, 1.0, 13)
        self.assertEqual(len(found), 3)
        self.assertIn("0.22", found[0])

    def test_good_bed_passes(self):
        self.assertEqual(audio_check.report(-16, {"full": -16, "treble": -55, "mid": -18}, 0.22, 13), [])

    def test_pad_has_no_noise_above_4khz(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "pad.wav"
            soundscape.save(soundscape.pad(6), str(path))
            self.assertLess(master.loudness(path, "highpass=f=4000,highpass=f=4000") or -99, -50)


class EndToEndTests(unittest.TestCase):
    def test_demo_builds(self):
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder)
            run = lambda *args: subprocess.run([sys.executable, *map(str, args)], check=True, capture_output=True)
            run(SCRIPTS / "timing.py", "--estimate", DEMO / "narration.txt", work / "alignment.json")
            run(SCRIPTS / "timing.py", DEMO / "lines.json", work / "alignment.json", work / "subtitles.json")
            run(SCRIPTS / "soundscape.py", "drone", 30, work / "video" / "assets" / "drone.wav") if (work / "video" / "assets").mkdir(parents=True) is None else None
            run(SCRIPTS / "compose.py", DEMO / "episode.py", work / "video", work / "subtitles.json", "--system-fonts")
            self.assertIn("<audio", (work / "video" / "index.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
