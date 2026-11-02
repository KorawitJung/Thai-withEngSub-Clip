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
