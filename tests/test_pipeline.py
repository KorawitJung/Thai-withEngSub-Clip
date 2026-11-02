import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "skills" / "thai-story-shorts"
SCRIPTS = ROOT / "scripts"
DEMO = ROOT / "examples" / "demo"
sys.path.insert(0, str(SCRIPTS))

import compose  # noqa: E402
import fonts  # noqa: E402
import master  # noqa: E402
import music  # noqa: E402
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
