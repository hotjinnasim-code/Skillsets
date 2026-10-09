"""New disposable diagrams only; all fixtures live inside this directory."""

import copy
from contextlib import contextmanager
import hashlib
import json
import os
import struct
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import make_layout_guide as guide


TEST_FONT = Path("/System/Library/Fonts/AppleSDGothicNeo.ttc")
SERIF_FONT = Path("/System/Library/Fonts/Supplemental/AppleMyungjo.ttf")
SVG_NS = "{http://www.w3.org/2000/svg}"


class DiagramTests(unittest.TestCase):
    def setUp(self):
        self.workspace = Path.cwd().resolve()
        self.temp = tempfile.TemporaryDirectory(prefix=".guide-test-", dir=self.workspace)
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    @contextmanager
    def in_workspace(self, directory):
        previous = Path.cwd()
        os.chdir(directory)
        try:
            yield
        finally:
            os.chdir(previous)

    def shapes_spec(self):
        return {
            "canvas": {"width": 600, "height": 300, "background": "none"},
            "shapes": [
                {"type": "rect", "x": 10, "y": 10, "width": 60, "height": 30, "fill": "#123456"},
                {"type": "ellipse", "x": 90, "y": 10, "width": 50, "height": 40,
                 "fill": "none", "stroke": "#345678", "stroke_width": 2},
                {"type": "polygon", "points": [[160, 10], [185, 40], [145, 40]], "fill": "#567890"},
                {"type": "line", "x1": 210, "y1": 15, "x2": 250, "y2": 45,
                 "stroke": "#789012", "stroke_width": 3},
            ],
            "text_blocks": [],
        }

    def block(self, actual_copy, lines, fixed=False):
        return {
            "copy": actual_copy, "lines": lines, "fixed_newlines": fixed,
            "x": 20, "y": 70, "align": "left", "line_spacing": 32,
            "area": {"width": 550, "height": 150},
            "font": {"path": str(TEST_FONT), "index": 0, "size": 24},
            "color": "#234567",
        }

    def render_spec(self, spec, name="new-diagram"):
        path = self.directory / f"{name}-input.json"
        path.write_text(json.dumps(spec, ensure_ascii=False, allow_nan=False), encoding="utf-8")
        paths = guide.render(path, self.directory / "outputs", name)
        manifest = json.loads(paths[".manifest.json"].read_text(encoding="utf-8"))
        return path, paths, manifest

    def test_cli_uses_calling_workspace_not_installed_script_directory(self):
        project = self.directory / "separate-project"
        project.mkdir()
        (project / "layout.json").write_text(json.dumps(self.shapes_spec()), encoding="utf-8")
        source = Path(guide.__file__).resolve()
        before = source.read_bytes()
        result = subprocess.run([sys.executable, "-B", str(source), "layout.json", "--output-dir", "guides", "--name", "own-diagram"], cwd=project, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((project / "guides/own-diagram.png").is_file())
        self.assertEqual(source.read_bytes(), before)
        escaped = subprocess.run([sys.executable, "-B", str(source), "layout.json", "--output-dir", "../outside", "--name", "outside"], cwd=project, capture_output=True, text=True)
        self.assertEqual(escaped.returncode, 2)
        self.assertFalse((self.directory / "outside").exists())

    def test_imported_api_uses_workspace_at_each_render_call(self):
        # guide was already imported in the parent workspace before entering this project.
        project = self.directory / "api-project"
        project.mkdir()
        old_input = self.directory / "old-input.json"
        old_input.write_text(json.dumps(self.shapes_spec()), encoding="utf-8")
        (project / "layout.json").write_text(json.dumps(self.shapes_spec()), encoding="utf-8")
        with self.in_workspace(project):
            paths = guide.render("layout.json", "guides", "own-diagram")
            self.assertTrue(all(path.parent == project / "guides" for path in paths.values()))
            manifest = json.loads(paths[".manifest.json"].read_text(encoding="utf-8"))
            self.assertEqual(manifest["input"]["path"], "layout.json")
            with self.assertRaisesRegex(guide.GuideError, "inside"):
                guide.render(old_input, "guides", "old-input")
            with self.assertRaisesRegex(guide.GuideError, "inside"):
                guide.render("layout.json", self.directory / "old-output", "old-output")
        # A later call gets its own boundary; the API retains no project from the prior call.
        later = self.directory / "later-project"
        later.mkdir()
        (later / "layout.json").write_text(json.dumps(self.shapes_spec()), encoding="utf-8")
        with self.in_workspace(later):
            paths = guide.render("layout.json", "guides", "later-diagram")
            self.assertTrue(all(path.parent == later / "guides" for path in paths.values()))
            with self.assertRaisesRegex(guide.GuideError, "inside"):
                guide.render(project / "layout.json", "guides", "previous-project")
        self.assertFalse((self.directory / "old-output").exists())

    def test_render_keeps_one_workspace_snapshot_when_cwd_changes_during_call(self):
        project = self.directory / "captured-project"
        other = self.directory / "changed-project"
        project.mkdir()
        other.mkdir()
        (project / "layout.json").write_text(json.dumps(self.shapes_spec()), encoding="utf-8")
        original_read = guide.read_spec

        def read_then_chdir(path, workspace):
            result = original_read(path, workspace)
            os.chdir(other)
            return result

        with self.in_workspace(project), patch.object(guide, "read_spec", side_effect=read_then_chdir):
            paths = guide.render("layout.json", "guides", "captured")
            self.assertEqual(Path.cwd(), other)
            self.assertTrue(all(path.parent == project / "guides" for path in paths.values()))
            self.assertEqual(json.loads(paths[".manifest.json"].read_text())["input"]["path"], "layout.json")
        self.assertFalse((other / "guides").exists())

    def test_render_checks_project_font_under_the_current_workspace(self):
        project = self.directory / "font-project"
        project.mkdir()
        marker = b"test-only font-path marker; not a font binary"
        current_font = project / "explicit.ttf"
        old_font = self.directory / "old.ttf"
        current_font.write_bytes(marker)
        old_font.write_bytes(marker)
        spec = self.shapes_spec()
        spec["text_blocks"] = [self.block("Exact copy.", ["Exact copy."])]
        for font_path, error, reached in ((current_font, "reached explicit project font", True),
                                          (old_font, "current-workspace font", False)):
            spec["text_blocks"][0]["font"]["path"] = str(font_path)
            (project / "layout.json").write_text(json.dumps(spec), encoding="utf-8")
            with self.subTest(font_path=font_path), self.in_workspace(project), \
                    patch.object(guide, "sfnt_tables", side_effect=guide.GuideError("reached explicit project font")) as parse:
                with self.assertRaisesRegex(guide.GuideError, error):
                    guide.render("layout.json", "guides", "font-permission")
                if reached:
                    parse.assert_called_once_with(marker, 0)
                else:
                    parse.assert_not_called()
        self.assertFalse((project / "guides").exists())

    def test_new_shapes_and_manifest_hashes(self):
        spec = self.shapes_spec()
        source, paths, manifest = self.render_spec(spec)
        self.assertTrue(manifest["draft_only"])
        self.assertEqual(manifest["input"]["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
        self.assertEqual(paths[".png"].read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
        for kind, suffix in (("svg", ".svg"), ("png", ".png")):
            self.assertEqual(manifest["outputs"][kind]["sha256"], hashlib.sha256(paths[suffix].read_bytes()).hexdigest())
        root = ET.fromstring(paths[".svg"].read_bytes())
        self.assertEqual([node.tag.removeprefix(SVG_NS) for node in root], ["rect", "ellipse", "polygon", "line"])
        self.assertFalse(root.findall(f"{SVG_NS}text"))
        self.assertEqual(len(manifest["shapes"]), 4)

    def test_copy_conservation_preserves_spacing_and_punctuation(self):
        block = self.block("Keep  spaces,\nand punctuation!", ["Keep  spaces,", "and punctuation!"])
        self.assertEqual(guide.conserved_lines(block), block["lines"])
        for lines in (["Keep spaces,", "and punctuation!"],
                      ["Keep  spaces,", "punctuation!"],
                      ["Keep  spaces,", "and new punctuation!"],
                      ["Keep  spaces", "and punctuation!"],
                      ["Keep  spaces,", "and", "punctuation! "]):
            with self.subTest(lines=lines), self.assertRaises(guide.GuideError):
                guide.conserved_lines({**block, "lines": lines})
        # Line boundaries may replace word spaces even when the copy has no newline.
        self.assertEqual(guide.conserved_lines(self.block("One  two. Three!", ["One  two.", "Three!"])),
                         ["One  two.", "Three!"])

    def test_fixed_newlines_include_blank_and_trailing_lines(self):
        block = self.block("First.\n\nLast!\n", ["First.", "", "Last!", ""], fixed=True)
        self.assertEqual(guide.conserved_lines(block), ["First.", "", "Last!", ""])
        with self.assertRaisesRegex(guide.GuideError, "fixed newlines"):
            guide.conserved_lines({**block, "lines": ["First.", "Last!"]})
        with self.assertRaisesRegex(guide.GuideError, "fixed newlines"):
            guide.conserved_lines({**block, "lines": ["First.", "", "Last!"]})

    def test_exclusive_output_set_and_rollback_preserve_existing_files(self):
        for suffix in (".svg", ".png", ".manifest.json"):
            with self.subTest(suffix=suffix):
                output = self.directory / suffix[1:]
                output.mkdir()
                existing = output / f"reserved{suffix}"
                existing.write_bytes(b"already here")
                source = self.directory / "exclusive-input.json"
                source.write_text(json.dumps(self.shapes_spec()), encoding="utf-8")
                with self.assertRaisesRegex(guide.GuideError, "already exists"):
                    guide.render(source, output, "reserved")
                self.assertEqual(existing.read_bytes(), b"already here")
                self.assertEqual(sorted(p.name for p in output.iterdir()), [existing.name])

    def test_rerender_never_overwrites_any_output(self):
        source, paths, _ = self.render_spec(self.shapes_spec())
        previous = {suffix: path.read_bytes() for suffix, path in paths.items()}
        with self.assertRaises(guide.GuideError):
            guide.render(source, paths[".svg"].parent, "new-diagram")
        self.assertEqual(previous, {suffix: path.read_bytes() for suffix, path in paths.items()})

    def test_bounded_output_and_input_locations(self):
        source = self.directory / "input.json"
        source.write_text(json.dumps(self.shapes_spec()), encoding="utf-8")
        for output in (self.workspace.parent, self.workspace / ".." / "escape", "/private/tmp"):
            with self.subTest(output=output), self.assertRaisesRegex(guide.GuideError, "inside"):
                guide.render(source, output, "escape")
        for name in ("../escape", "a/b", "a\\b", ".hidden", "", "name.svg", "/absolute"):
            with self.subTest(name=name), self.assertRaises(guide.GuideError):
                guide.render(source, self.directory, name)
        escape = self.directory / "outside-link"
        escape.symlink_to(self.workspace.parent, target_is_directory=True)
        with self.assertRaisesRegex(guide.GuideError, "inside"):
            guide.render(source, escape / "outputs", "escape")
        with self.assertRaisesRegex(guide.GuideError, "inside"):
            guide.render(escape / "input.json", self.directory, "escape")
        for path in ("", "bad\x00path", None):
            with self.subTest(path=repr(path)), self.assertRaises(guide.GuideError):
                guide.bounded(path, "path", self.workspace)

    def test_output_symlink_collision_is_not_followed(self):
        target = self.directory / "unchanged.txt"
        target.write_text("unchanged", encoding="utf-8")
        output = self.directory / "outputs"
        output.mkdir()
        (output / "reserved.manifest.json").symlink_to(target)
        source = self.directory / "input.json"
        source.write_text(json.dumps(self.shapes_spec()), encoding="utf-8")
        with self.assertRaises(guide.GuideError):
            guide.render(source, output, "reserved")
        self.assertEqual(target.read_text(encoding="utf-8"), "unchanged")
        self.assertEqual([p.name for p in output.iterdir()], ["reserved.manifest.json"])

    def test_invalid_numbers_are_rejected(self):
        spec = self.shapes_spec()
        for value in (None, "", "12", True, 0, -1, 1.5, float("nan"), float("inf"), 10 ** 1000):
            with self.subTest(value=str(value)[:20]), self.assertRaises(guide.GuideError):
                guide.number(value, "dimension", positive=True, integer=True)
        for key, value in (("width", 0), ("height", True), ("width", 10000)):
            invalid = copy.deepcopy(spec)
            invalid["canvas"][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(guide.GuideError):
                self.render_spec(invalid)
        source = self.directory / "nonfinite.json"
        source.write_text('{"canvas": NaN}', encoding="utf-8")
        with self.assertRaisesRegex(guide.GuideError, "nonfinite"):
            guide.read_spec(source, self.workspace)
        source.write_text('{"canvas": {}, "canvas": {}}', encoding="utf-8")
        with self.assertRaisesRegex(guide.GuideError, "duplicate"):
            guide.read_spec(source, self.workspace)

    def test_malformed_shapes_and_canvas_clipping(self):
        canvas = self.shapes_spec()["canvas"]
        invalid = [
            {"type": "unknown"},
            {"type": "rect", "x": 0, "y": 0, "width": -2, "height": 10, "fill": "#ffffff"},
            {"type": "ellipse", "x": 5, "y": 5, "width": 10, "height": 0, "fill": "#ffffff"},
            {"type": "rect", "x": 10, "y": 10, "width": 20, "height": 20, "fill": "none"},
            {"type": "rect", "x": 0, "y": 10, "width": 20, "height": 20,
             "fill": "none", "stroke": "#ffffff", "stroke_width": 2},
            {"type": "polygon", "points": [[0, 0], [2, 2]], "fill": "#ffffff"},
            {"type": "polygon", "points": [[10, 10], [20, 20], [30, 30]], "fill": "#ffffff"},
            {"type": "polygon", "points": [[10, 10], [40, 40], [10, 40], [40, 10]], "fill": "#ffffff"},
            {"type": "polygon", "points": [[10, 10], [40, 10], [10, 10], [10, 40]], "fill": "#ffffff"},
            {"type": "line", "x1": 10, "y1": 10, "x2": 10, "y2": 10,
             "stroke": "#ffffff", "stroke_width": 1},
            {"type": "line", "x1": "", "y1": 10, "x2": 20, "y2": 20,
             "stroke": "#ffffff", "stroke_width": 1},
        ]
        for shape in invalid:
            with self.subTest(shape=shape), self.assertRaises(guide.GuideError):
                guide.validate_shape(shape, canvas)
        clipped = self.shapes_spec()
        clipped["shapes"][0]["x"] = -1
        with self.assertRaisesRegex(guide.GuideError, "clip"):
            self.render_spec(clipped)
        self.assertFalse((self.directory / "outputs").exists())

    @unittest.skipUnless(TEST_FONT.is_file(), "explicit test system font unavailable; no substitute or copied font")
    def test_xml_escaping_actual_copy_and_font_manifest(self):
        spec = self.shapes_spec()
        actual_copy = 'Exact <copy> & "quotes";  한글!'
        spec["text_blocks"] = [self.block(actual_copy, [actual_copy])]
        _, paths, manifest = self.render_spec(spec)
        svg = paths[".svg"].read_text(encoding="utf-8")
        self.assertIn("&lt;copy&gt; &amp;", svg)
        root = ET.fromstring(svg)
        texts = root.findall(f"{SVG_NS}text")
        self.assertEqual([node.text for node in texts], [actual_copy])
        self.assertEqual(texts[0].attrib["{http://www.w3.org/XML/1998/namespace}space"], "preserve")
        self.assertEqual(texts[0].attrib["font-family"], '"Apple SD Gothic Neo"')
        info = manifest["text_blocks"][0]
        self.assertEqual(info["copy"], actual_copy)
        self.assertEqual(info["lines"], [actual_copy])
        self.assertEqual(info["line_measurements"][0]["text"], actual_copy)
        self.assertEqual(info["font"]["index"], 0)
        self.assertEqual(info["font"]["family"], "Apple SD Gothic Neo")
        self.assertEqual(info["font"]["sha256"], hashlib.sha256(TEST_FONT.read_bytes()).hexdigest())
        self.assertEqual(info["font"]["path"], str(TEST_FONT.resolve()))
        self.assertGreater(info["line_measurements"][0]["advance_px"], 0)

    @unittest.skipUnless(SERIF_FONT.is_file(), "explicit serif system font unavailable; no substitute or copied font")
    def test_serif_without_os2_renders_with_honest_nominal_style_metadata(self):
        data = SERIF_FONT.read_bytes()
        tables = guide.sfnt_tables(data, 0)
        self.assertNotIn(b"OS/2", tables, "this regression requires the explicit no-OS/2 serif face")
        flags = struct.unpack_from(">H", tables[b"head"], 44)[0]
        actual_copy = '한글 본문 <&>  그대로.'
        block = self.block(actual_copy, [actual_copy])
        block["font"]["path"] = str(SERIF_FONT)
        spec = self.shapes_spec()
        spec["text_blocks"] = [block]
        _, paths, manifest = self.render_spec(spec, "explicit-serif")
        info = manifest["text_blocks"][0]
        face = info["font"]
        self.assertEqual((face["path"], face["index"], face["sha256"]),
                         (str(SERIF_FONT.resolve()), 0, hashlib.sha256(data).hexdigest()))
        self.assertIsNone(face["weight"])
        self.assertIsNone(face["stretch_percent"])
        self.assertEqual(face["head_mac_style"], flags)
        self.assertIsNone(face["style_provenance"]["weight"])
        self.assertIsNone(face["style_provenance"]["stretch_percent"])
        self.assertEqual(face["style_provenance"]["slant"], "head.macStyle")
        self.assertEqual(face["style_provenance"]["svg_style"],
                         {"font-weight": "head.macStyle (nominal)", "font-style": "head.macStyle (nominal)"})
        nodes = ET.fromstring(paths[".svg"].read_bytes()).findall(f"{SVG_NS}text")
        self.assertEqual([node.text for node in nodes], [actual_copy])
        self.assertEqual(nodes[0].attrib["font-weight"], "bold" if flags & 1 else "normal")
        self.assertEqual(nodes[0].attrib["font-style"], "italic" if flags & 2 else "normal")
        self.assertNotIn("font-stretch", nodes[0].attrib)
        self.assertEqual(nodes[0].attrib["{http://www.w3.org/XML/1998/namespace}space"], "preserve")
        self.assertEqual((info["copy"], info["lines"]), (actual_copy, [actual_copy]))
        engine = getattr(guide.ImageFont.Layout, face["layout_engine"])
        supplied = guide.ImageFont.truetype(guide.io.BytesIO(data), size=24, index=0, layout_engine=engine)
        self.assertEqual((face["family"], face["style"]), supplied.getname())
        self.assertAlmostEqual(info["line_measurements"][0]["advance_px"], supplied.getlength(actual_copy))
        # Absent style metadata does not weaken copy, coverage, index or canvas constraints.
        for actual, x, index, error in (("Missing \U0010ffff", 20, 0, "lacks glyphs"),
                                         ("Canvas clipping.", 590, 0, "clip"),
                                         ("Exact copy.", 20, 1, "non-collection")):
            invalid = self.shapes_spec()
            invalid["text_blocks"] = [self.block(actual, [actual])]
            invalid["text_blocks"][0]["font"].update(path=str(SERIF_FONT), index=index)
            invalid["text_blocks"][0]["x"] = x
            with self.subTest(error=error), self.assertRaisesRegex(guide.GuideError, error):
                self.render_spec(invalid, "rejected-serif")
            self.assertFalse((self.directory / "outputs/rejected-serif.png").exists())

    @unittest.skipUnless(TEST_FONT.is_file(), "explicit test system font unavailable")
    def test_render_fixed_newline_groups_exactly(self):
        spec = self.shapes_spec()
        spec["text_blocks"] = [self.block("First.\n\nLast!\n", ["First.", "", "Last!", ""], fixed=True)]
        _, paths, manifest = self.render_spec(spec)
        nodes = ET.fromstring(paths[".svg"].read_bytes()).findall(f"{SVG_NS}text")
        self.assertEqual([node.text or "" for node in nodes], ["First.", "", "Last!", ""])
        lines = manifest["text_blocks"][0]["line_measurements"]
        self.assertEqual([line["baseline_px"] for line in lines], [lines[0]["baseline_px"] + i * 32 for i in range(4)])

    @unittest.skipUnless(TEST_FONT.is_file(), "explicit test system font unavailable")
    def test_planned_area_overflow_is_a_measurement(self):
        spec = self.shapes_spec()
        spec["text_blocks"] = [self.block("Measured overflow.", ["Measured overflow."])]
        spec["text_blocks"][0]["area"] = {"width": 10, "height": 10}
        _, _, manifest = self.render_spec(spec)
        excess = manifest["text_blocks"][0]["planned_area_overflow_px"]
        self.assertGreater(excess["right"], 0)
        self.assertGreater(excess["bottom"], 0)
        self.assertNotIn("pass", manifest)
        self.assertNotIn("score", manifest)

    @unittest.skipUnless(TEST_FONT.is_file(), "explicit test system font unavailable")
    def test_text_clipping_and_missing_glyphs_fail_without_outputs(self):
        cases = [self.block("Canvas clipping.", ["Canvas clipping."]), self.block("Missing \U0010ffff", ["Missing \U0010ffff"])]
        cases[0]["x"] = 590
        for block, message in zip(cases, ("clip", "lacks glyphs")):
            spec = self.shapes_spec()
            spec["text_blocks"] = [block]
            with self.subTest(message=message), self.assertRaisesRegex(guide.GuideError, message):
                self.render_spec(spec)
            self.assertFalse((self.directory / "outputs").exists())

    @unittest.skipUnless(TEST_FONT.is_file(), "explicit test system font unavailable")
    def test_ttc_index_is_exposed_and_checked(self):
        cache = {}
        zero = guide.load_font({"path": str(TEST_FONT), "index": 0, "size": 24}, cache, self.workspace)[2]
        other = guide.load_font({"path": str(TEST_FONT), "index": 1, "size": 24}, cache, self.workspace)[2]
        self.assertEqual(other["index"], 1)
        self.assertEqual((other["family"], other["style"]),
                         guide.ImageFont.truetype(str(TEST_FONT), size=24, index=1).getname())
        self.assertEqual(zero["sha256"], other["sha256"])
        for index in (-1, 9999, True, "0"):
            with self.subTest(index=index), self.assertRaises(guide.GuideError):
                guide.load_font({"path": str(TEST_FONT), "index": index, "size": 24}, {}, self.workspace)

    @unittest.skipUnless(TEST_FONT.is_file(), "explicit test system font unavailable")
    def test_alignment_uses_requested_area_and_actual_advance(self):
        for align in ("left", "center", "right"):
            block = self.block("Alignment.", ["Alignment."])
            block["align"] = align
            _, info = guide.measure_block(block, self.shapes_spec()["canvas"], {}, self.workspace)
            line = info["line_measurements"][0]
            offset = {"left": 0, "center": (550 - line["advance_px"]) / 2, "right": 550 - line["advance_px"]}[align]
            self.assertAlmostEqual(line["x_px"], 20 + offset)

    def test_no_implicit_font_or_control_character_fallback(self):
        block = self.block("Exact copy.", ["Exact copy."])
        for key in ("path", "index", "size"):
            font = dict(block["font"])
            del font[key]
            with self.subTest(key=key), self.assertRaises(guide.GuideError):
                guide.load_font(font, {}, self.workspace)
        for char in ("\r", "\t", "\x00", "\u200d", "\ufe0f", "\ud800", "\u2028", "\u2029"):
            with self.subTest(char=repr(char)), self.assertRaises(guide.GuideError):
                guide.conserved_lines(self.block(f"Copy{char}.", [f"Copy{char}."]))


class CmapTests(unittest.TestCase):
    """Synthetic cmap bytes only; no installed face is needed to exercise disagreement."""

    @staticmethod
    def format4(glyph):
        # U+0041 plus the required U+FFFF sentinel; direct idDelta mappings.
        return struct.pack(">7H2HH2H2h2H", 4, 32, 0, 4, 4, 1, 0,
                           0x41, 0xFFFF, 0, 0x41, 0xFFFF, glyph - 0x41, 1, 0, 0)

    @staticmethod
    def format12(glyph, code=0x41):
        return struct.pack(">HHIII3I", 12, 0, 28, 0, 1, code, code, glyph)

    @staticmethod
    def table(*maps):
        records = []
        offset = 4 + 8 * len(maps)
        for encoding, subtable in maps:
            records.append(struct.pack(">HHI", 3, encoding, offset))
            offset += len(subtable)
        return struct.pack(">HH", 0, len(maps)) + b"".join(records) + b"".join(sub for _, sub in maps)

    def paired_coverage(self, glyph4, glyph12):
        return guide.cmap_coverage(self.table((1, self.format4(glyph4)), (10, self.format12(glyph12))))

    def test_single_supported_subtables_have_present_and_absent_controls(self):
        for encoding, make in ((1, self.format4), (10, self.format12)):
            for glyph in (0, 1):
                with self.subTest(encoding=encoding, glyph=glyph):
                    coverage = guide.cmap_coverage(self.table((encoding, make(glyph))))
                    self.assertEqual(coverage(0x41), bool(glyph))

    def test_disagreeing_supported_cmaps_reject_requested_character(self):
        for first, second in ((1, 0), (0, 1)):
            with self.subTest(first=first, second=second):
                coverage = self.paired_coverage(first, second)
                with self.assertRaisesRegex(guide.GuideError, "unsupported font:.*disagree.*U\\+0041"):
                    coverage(0x41)
                # Disagreement on A does not reject an unrequested character at parse time.
                self.assertFalse(coverage(0x42))

    def test_consistent_supported_cmap_coverage_does_not_require_identical_glyph_ids(self):
        self.assertTrue(self.paired_coverage(1, 2)(0x41))
        self.assertFalse(self.paired_coverage(0, 0)(0x41))

    def test_supplementary_coverage_is_conservatively_checked_against_bmp_cmap(self):
        table = self.table((1, self.format4(1)), (10, self.format12(1, code=0x10000)))
        with self.assertRaisesRegex(guide.GuideError, "disagree.*U\\+10000"):
            guide.cmap_coverage(table)(0x10000)


class FontStyleTests(unittest.TestCase):
    def test_head_flags_remain_nominal_and_do_not_invent_numeric_metadata(self):
        for flags in (0, 1, 2, 3, 32, 64):
            head = b"\0" * 44 + struct.pack(">H", flags)
            with self.subTest(flags=flags):
                info = guide.font_style_metadata({b"head": head})
                self.assertIsNone(info["weight"])
                self.assertIsNone(info["stretch_percent"])
                self.assertEqual(info["head_mac_style"], flags)
                self.assertEqual(info["svg_style"], {"font-weight": "bold" if flags & 1 else "normal",
                                                     "font-style": "italic" if flags & 2 else "normal"})
        absent = guide.font_style_metadata({})
        self.assertEqual(absent["svg_style"], {})
        self.assertIsNone(absent["slant"])

    def test_absence_support_does_not_hide_malformed_present_style_tables(self):
        head = b"\0" * 44 + struct.pack(">H", 3)
        with self.assertRaises(struct.error):
            guide.font_style_metadata({b"head": head, b"OS/2": b"\0"})
        with self.assertRaisesRegex(guide.GuideError, "invalid OS/2"):
            guide.font_style_metadata({b"head": head, b"OS/2": b"\0" * 64})
        with self.assertRaises(struct.error):
            guide.font_style_metadata({b"head": b"\0" * 44})


if __name__ == "__main__":
    unittest.main()
