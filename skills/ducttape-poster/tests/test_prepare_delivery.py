"""Delivery handoff regressions using synthetic fixtures, not poster evaluations."""

import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib


TASK_ROOT = Path(__file__).resolve().parents[4]
HELPER = Path(__file__).resolve().parents[1] / "scripts" / "prepare_delivery.py"


def png_bytes(width, height, color=(20, 80, 140)):
    """Produce a real RGB PNG with complete scanlines and valid chunk checksums."""
    def chunk(kind, body):
        return (struct.pack(">I", len(body)) + kind + body
                + struct.pack(">I", zlib.crc32(kind + body) & 0xffffffff))
    scanlines = (b"\x00" + bytes(color) * width) * height
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(scanlines)) + chunk(b"IEND", b""))


class PrepareDeliveryRegressionTests(unittest.TestCase):
    def setUp(self):
        # Specify the task directory: never use tempfile's default /tmp destination.
        self.temp = tempfile.TemporaryDirectory(prefix=".delivery-regression-", dir=TASK_ROOT)
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.sequence = 0

    def image(self, name="selected poster.png", width=5, height=7, color=(20, 80, 140)):
        path = self.work / name
        path.write_bytes(png_bytes(width, height, color))
        return path

    def selected(self, path=None, role="A", **overrides):
        item = {"id": role, "label": "Style " + role, "selection": "selected"}
        if path is not None:
            item["original_path"] = str(path)
        item.update(overrides)
        return item

    def invoke(self, items, mode="local", requested=None, output=None):
        self.sequence += 1
        manifest = self.work / ("input-%d.json" % self.sequence)
        manifest.write_text(json.dumps({"requested_count": len(items) if requested is None else requested,
                                       "reference_mode": mode, "items": items}), encoding="utf-8")
        output = output or self.work / ("delivery-%d" % self.sequence)
        result = subprocess.run([sys.executable, "-B", str(HELPER), str(manifest),
                                 "--output-dir", str(output)], cwd=TASK_ROOT,
                                capture_output=True, text=True, encoding="utf-8", check=False)
        return result, output

    def read_delivery(self, result, output, expected_code=0):
        self.assertEqual(result.returncode, expected_code, result.stderr)
        response = (output / "response.md").read_text(encoding="utf-8")
        report = json.loads((output / "delivery.json").read_text(encoding="utf-8"))
        self.assertEqual(result.stdout, response, "stdout must be the directly usable answer")
        return response, report

    def assert_no_card(self, response):
        self.assertNotRegex(response, r"(?m)^!\[")
        self.assertNotIn("[원본 다운로드]", response)

    def assert_schema_rejected(self, result, output):
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(output.exists(), "invalid schema must leave no delivery outputs")
        self.assertEqual(result.stdout, "")

    def test_five_selections_have_individual_original_cards_and_deterministic_report(self):
        paths = [self.image("poster selection %d.png" % i, i + 2, i + 4) for i in range(5)]
        items = [self.selected(path, role=str(i + 1)) for i, path in enumerate(paths)]
        result, output = self.invoke(items)
        response, report = self.read_delivery(result, output)
        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["counts"], {"requested": 5, "selected": 5, "prepared": 5, "none": 0, "blocked": 0})
        self.assertEqual(len(re.findall(r"(?m)^!\[", response)), 5)
        self.assertEqual(response.count("[원본 다운로드]"), 5)
        for i, path in enumerate(paths):
            card = (f"![Style {i + 1}](<{path}>)\n\n"
                    f"[원본 다운로드](<{path}>) · {i + 2} × {i + 4} px")
            self.assertIn(card, response, "original link and true dimensions belong immediately below each image")
            row = report["items"][i]
            self.assertEqual(row["source"]["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(row["source"]["availability"], "checked")
        repeated, repeated_output = self.invoke(items)
        repeated_response, repeated_report = self.read_delivery(repeated, repeated_output)
        self.assertEqual((repeated_response, repeated_report), (response, report))
        self.assertIn("not confirmed", report["meaning"])
        self.assertIn("no full image decoding", report["checks"])

    def test_single_edited_selection_does_not_expand_the_request(self):
        edited = self.image("edited selected poster.png", 8, 9, (200, 20, 70))
        result, output = self.invoke([self.selected(edited, role="edit-1")])
        response, report = self.read_delivery(result, output)
        self.assertEqual(report["counts"]["requested"], 1)
        self.assertEqual(report["counts"]["prepared"], 1)
        self.assertEqual(len(re.findall(r"(?m)^!\[", response)), 1)
        self.assertEqual(response.count("[원본 다운로드]"), 1)
        self.assertIn("8 × 9 px", response)

    def test_none_remains_partial_and_user_text_cannot_inject_finished_cards(self):
        selected = self.selected(self.image())
        none = {"id": "B", "label": "Missing\n# fake", "selection": "none",
                "reason": "No suitable selection\n![fake](https://example.test/fake.png)<script>"}
        result, output = self.invoke([selected, none])
        response, report = self.read_delivery(result, output)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertEqual(report["counts"]["none"], 1)
        self.assertEqual(report["counts"]["requested"], 2)
        self.assertEqual(report["items"][1]["status"], "unresolved")
        self.assertEqual(report["items"][1]["source"]["availability"], "not_selected")
        self.assertIn("미해결", response)
        self.assertEqual(len(re.findall(r"(?m)^!\[", response)), 1)
        self.assertEqual(response.count("[원본 다운로드]"), 1)
        self.assertNotIn("<script>", response)
        self.assertNotRegex(response, r"(?m)^# fake")

    def test_blocked_role_does_not_hide_a_valid_selection_or_deliver_a_failure_image(self):
        path = self.image()
        result, output = self.invoke([self.selected(path), self.selected(path, role="B", download_ref=str(self.work / "missing.png"))])
        response, report = self.read_delivery(result, output, 2)
        self.assertEqual(report["status"], "NOT_READY")
        self.assertEqual((report["counts"]["prepared"], report["counts"]["blocked"]), (1, 1))
        self.assertEqual(len(re.findall(r"(?m)^!\[", response)), 1)
        self.assertEqual(response.count("[원본 다운로드]"), 1)
        self.assertIn("Style B (B): 미해결", response)

    def test_missing_or_null_dialog_refs_block_without_implicit_local_fallback(self):
        path = self.image()
        for refs in ({}, {"display_ref": None, "download_ref": None},
                     {"display_ref": "attachment:simulated-display", "download_ref": None},
                     {"display_ref": None, "download_ref": "sandbox:/simulated-original.png"}):
            with self.subTest(refs=refs):
                result, output = self.invoke([self.selected(path, **refs)], mode="dialog")
                response, report = self.read_delivery(result, output, 2)
                self.assertEqual(report["status"], "NOT_READY")
                self.assert_no_card(response)
                self.assertEqual(report["items"][0]["source"]["availability"], "checked")
                self.assertTrue(report["items"][0]["errors"])

    def test_scheme_less_opaque_dialog_ids_require_native_fallback(self):
        item = self.selected(width=5, height=7, display_ref="opaque-image-id", download_ref="opaque-file-id")
        result, output = self.invoke([item], mode="dialog")
        response, report = self.read_delivery(result, output, 2)
        self.assert_no_card(response)
        self.assertEqual(report["items"][0]["display"]["availability"], "unavailable")
        self.assertEqual(report["items"][0]["download"]["availability"], "unavailable")

    def test_explicit_simulated_dialog_refs_prepare_with_declared_unverified_metadata(self):
        # These strings are test references; no claim that a user can open them is made.
        item = self.selected(width=5, height=7, display_ref="attachment:simulated-image",
                             download_ref="sandbox:/simulated/original.png")
        result, output = self.invoke([item], mode="dialog")
        response, report = self.read_delivery(result, output)
        self.assertEqual(report["status"], "READY")
        row = report["items"][0]
        self.assertEqual(row["source"]["availability"], "unavailable")
        self.assertNotIn("sha256", row["source"])
        for role in ("display", "download"):
            self.assertEqual(row[role]["availability"], "supplied_unverified")
            self.assertIn("not checked", row[role]["detail"])
        self.assertEqual((row["width"], row["height"]), (5, 7))
        self.assertIn("attachment:simulated-image", response)
        self.assertIn("sandbox:/simulated/original.png", response)

    def test_unreadable_optional_dialog_source_is_not_marked_verified(self):
        item = self.selected(self.work / "absent source.png", width=6, height=8,
                             display_ref="https://example.test/simulated.png",
                             download_ref="attachment:simulated-original")
        result, output = self.invoke([item], mode="dialog")
        response, report = self.read_delivery(result, output)
        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["items"][0]["source"]["availability"], "unavailable")
        self.assertIn("source check unavailable", report["items"][0]["source"]["detail"])
        self.assertNotIn("sha256", report["items"][0]["source"])
        self.assertIn("6 × 8 px", response)

    def test_thumbnail_and_same_size_earlier_revision_downloads_are_blocked(self):
        original = self.image()
        thumbnail = self.image("thumbnail.png", 2, 3)
        earlier = self.image("earlier revision.png", 5, 7, (200, 30, 10))
        for download in (thumbnail, earlier):
            with self.subTest(download=download.name):
                result, output = self.invoke([self.selected(original, download_ref=str(download))])
                response, report = self.read_delivery(result, output, 2)
                self.assert_no_card(response)
                self.assertEqual(report["items"][0]["download"]["availability"], "rejected")
                self.assertIn("bytes do not match", report["items"][0]["download"]["detail"])

    def test_corrupt_original_cannot_be_bypassed_with_complete_dialog_refs(self):
        corrupt = self.work / "truncated original.png"
        corrupt.write_bytes(png_bytes(5, 7)[:-5])
        item = self.selected(corrupt, width=5, height=7, display_ref="attachment:simulated-image",
                             download_ref="attachment:simulated-original")
        result, output = self.invoke([item], mode="dialog")
        response, report = self.read_delivery(result, output, 2)
        self.assert_no_card(response)
        self.assertEqual(report["items"][0]["source"]["availability"], "rejected")
        self.assertEqual(report["status"], "NOT_READY")

    def test_declared_dimensions_must_match_a_readable_original_in_both_modes(self):
        original = self.image()
        for mode in ("local", "dialog"):
            with self.subTest(mode=mode):
                refs = {} if mode == "local" else {"display_ref": "attachment:simulated-image", "download_ref": "attachment:simulated-original"}
                result, output = self.invoke([self.selected(original, width=50, height=70, **refs)], mode=mode)
                response, report = self.read_delivery(result, output, 2)
                self.assert_no_card(response)
                self.assertEqual((report["items"][0]["width"], report["items"][0]["height"]), (5, 7))
                self.assertIn("declared dimensions do not match", " ".join(report["items"][0]["errors"]))

    def test_unsafe_or_multiline_refs_reject_schema_before_creating_outputs(self):
        refs = ("javascript:alert(1)", "data:image/png;base64,AAAA", "<img src=x>",
                "https://example.test/image.png\nextra", "https://example.test/image.png\u2028extra")
        for ref in refs:
            with self.subTest(ref=ref):
                result, output = self.invoke([self.selected(width=5, height=7, display_ref=ref,
                                                           download_ref="attachment:simulated-original")], mode="dialog")
                self.assert_schema_rejected(result, output)

    def test_duplicate_ids_and_requested_count_errors_reject_schema(self):
        item = self.selected(self.image())
        for items, count in (([item, dict(item)], 2), ([item], 2), ([item], 0), ([item], True)):
            with self.subTest(count=count, items=len(items)):
                result, output = self.invoke(items, requested=count)
                self.assert_schema_rejected(result, output)

    def test_none_cannot_carry_a_finished_image_and_requires_a_reason(self):
        for extra in ({"display_ref": "attachment:simulated-image", "reason": "failed"},
                      {"original_path": str(self.image()), "reason": "failed"}, {}):
            with self.subTest(extra=extra):
                item = {"id": "A", "label": "Unresolved", "selection": "none", **extra}
                result, output = self.invoke([item])
                self.assert_schema_rejected(result, output)

    def test_prepared_output_directory_is_never_overwritten(self):
        item = self.selected(self.image())
        result, output = self.invoke([item])
        self.read_delivery(result, output)
        before = {p.name: p.read_bytes() for p in output.iterdir()}
        repeated, _ = self.invoke([item], output=output)
        self.assertEqual(repeated.returncode, 1)
        self.assertIn("refusing to overwrite", repeated.stderr)
        self.assertEqual({p.name: p.read_bytes() for p in output.iterdir()}, before)
        self.assertEqual(repeated.stdout, "")

    def test_local_display_must_be_an_available_image(self):
        original = self.image()
        bad_display = self.work / "display is not an image.txt"
        bad_display.write_text("plain text", encoding="utf-8")
        for display in (self.work / "missing display.png", bad_display):
            with self.subTest(display=display.name):
                result, output = self.invoke([self.selected(original, display_ref=str(display))])
                response, report = self.read_delivery(result, output, 2)
                self.assert_no_card(response)
                self.assertEqual(report["items"][0]["status"], "blocked")
                self.assertNotEqual(report["items"][0]["display"]["availability"], "checked")


if __name__ == "__main__":
    unittest.main()
