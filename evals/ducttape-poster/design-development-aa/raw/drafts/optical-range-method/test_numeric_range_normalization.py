"""Pure normalization behavior tests; no case/packet/view/score fixtures."""
import ast
import copy
import itertools
from pathlib import Path
import re
import unicodedata
import unittest

from numeric_range_normalization import normalize, validate_entry


def entry(text, left=None, right=None, **extra):
    value = {"text": text, "kind": "text", "fixed_newlines": False, **extra}
    if left is not None:
        value.update(fixed_spacing=False,
                     optical_numeric_ranges=[{"left": left, "separator": "–", "right": right}])
    return value


class OpticalRangeBehavior(unittest.TestCase):
    def test_opted_in_gaps_are_equivalent_idempotent_and_do_not_mutate(self):
        # Several independently generated intervals, not one mirrored example.
        intervals = [(str(left), str(right)) for left, right in [(2, 7), (13, 29), (100, 450)]]
        intervals += [("2031.04.05", "04.07"), ("09:15", "17:40")]
        for left, right in intervals:
            source = f"기간 {left}–{right} 안내"
            policy = entry(source, left, right)
            snapshot = copy.deepcopy(policy)
            for before, after in itertools.product(["", " ", "   ", "\t", "\n"], repeat=2):
                raw = f"기간 {left}{before}–{after}{right} 안내"
                normalized = normalize(raw, policy)
                self.assertEqual(normalized, source)
                self.assertEqual(normalize(normalized, policy), normalized)
                self.assertEqual(policy, snapshot)
                self.assertIn(before + "–" + after, raw)

    def test_all_changed_digits_and_separator_classes_remain_different(self):
        source = "시간 09:15–17:40 안내"
        policy = entry(source, "09:15", "17:40")
        for index, char in enumerate(source):
            if char.isascii() and char.isdigit():
                for replacement in "0123456789":
                    if replacement != char:
                        corrupted = source[:index] + replacement + source[index + 1:]
                        self.assertNotEqual(normalize(corrupted, policy), source)
        for symbol in ["-", "−", "—", "·", "/", ":", "", "––"]:
            self.assertNotEqual(normalize(source.replace("–", symbol), policy), source)
        self.assertNotEqual(normalize("시간 17:40–09:15 안내", policy), source)

    def test_only_declared_pair_gets_an_exception(self):
        source = "첫 범위 10–20 다음 범위 30–40"
        policy = entry(source, "10", "20")
        raw = "첫 범위 10 – 20 다음 범위 30 – 40"
        normalized = normalize(raw, policy)
        self.assertEqual(normalized, "첫 범위 10–20 다음 범위 30 – 40")
        self.assertNotEqual(normalized, source)
        strict = entry("10–20")
        self.assertNotEqual(normalize("10 – 20", strict), strict["text"])

    def test_word_boundaries_endpoint_internal_spacing_and_punctuation_survive(self):
        source = "토·일 방문 09:15–17:40 안내"
        policy = entry(source, "09:15", "17:40")
        for wrong in ["토·일방문 09:15 – 17:40 안내", "토·일 방문 0 9:15 – 17:40 안내",
                      "토·일 방문 09 :15 – 17:40 안내", "토·일 방문 09.15 – 17:40 안내",
                      "토·일 방문 09:15 – 17:40안내", "토·일 방문 09:15 – 17:40 안 내"]:
            self.assertNotEqual(normalize(wrong, policy), source)

    def test_client_fixed_spacing_and_newlines_are_not_normalized_away(self):
        literal = entry("시간  10 – 20\n안내", fixed_spacing=True, fixed_newlines=True)
        self.assertEqual(normalize(literal["text"], literal), literal["text"])
        self.assertNotEqual(normalize("시간 10 – 20\n안내", literal), literal["text"])
        self.assertNotEqual(normalize("시간  10–20\n안내", literal), literal["text"])
        self.assertNotEqual(normalize("시간  10 – 20 안내", literal), literal["text"])
        dot = entry("안내 · 방문", fixed_spacing=True)
        self.assertNotEqual(normalize("안내·방문", dot), dot["text"])
        declared = entry("10–20\n안내", "10", "20", fixed_newlines=True)
        self.assertNotEqual(normalize("10\n–20\n안내", declared), declared["text"])
        self.assertNotEqual(normalize("10–20 안내", declared), declared["text"])

    def test_url_has_no_optical_exception_even_for_numeric_range_tokens(self):
        url = {"text": "https://events.example/10–20", "kind": "url", "fixed_newlines": False}
        for wrong in ["https://events.example/10 – 20", "https://events.example /10–20",
                      "https://events.example/10-20", "https://events.example/1 0–20"]:
            self.assertNotEqual(normalize(wrong, url), url["text"])
        bad = dict(url, fixed_spacing=False,
                   optical_numeric_ranges=[{"left": "10", "separator": "–", "right": "20"}])
        with self.assertRaises(ValueError): validate_entry(bad)

    def test_invalid_or_unjustified_declarations_are_rejected_before_comparison(self):
        valid = entry("10–20", "10", "20")
        bad_values = []
        missing = copy.deepcopy(valid); missing.pop("fixed_spacing"); bad_values.append(missing)
        fixed = copy.deepcopy(valid); fixed["fixed_spacing"] = True; bad_values.append(fixed)
        missing_pair = copy.deepcopy(valid); missing_pair["text"] = "11–20"; bad_values.append(missing_pair)
        repeated = copy.deepcopy(valid); repeated["text"] = "10–20 또는 10–20"; bad_values.append(repeated)
        identifier = copy.deepcopy(valid); identifier["text"] = "SKU10–20"; bad_values.append(identifier)
        negative = copy.deepcopy(valid); negative["text"] = "-10–20"; bad_values.append(negative)
        extra = copy.deepcopy(valid); extra["optical_numeric_ranges"][0]["guess"] = True; bad_values.append(extra)
        wrong_dash = copy.deepcopy(valid); wrong_dash["optical_numeric_ranges"][0]["separator"] = "—"; bad_values.append(wrong_dash)
        letters = copy.deepcopy(valid); letters["optical_numeric_ranges"][0]["left"] = "one"; bad_values.append(letters)
        duplicate = copy.deepcopy(valid); duplicate["optical_numeric_ranges"] *= 2; bad_values.append(duplicate)
        wrong_flag = copy.deepcopy(valid); wrong_flag["fixed_spacing"] = "false"; bad_values.append(wrong_flag)
        for bad in bad_values:
            with self.subTest(policy=bad), self.assertRaises(ValueError): validate_entry(bad)

    def test_no_opt_in_matches_frozen_v1_for_existing_valid_entry_behavior(self):
        # Load only the frozen pure function AST, never execute a round helper,
        # CLI, case, packet, summary or critic. This is a compatibility check.
        source = Path(__file__).resolve().parents[2] / "work/round22/summarize.py"
        function = next(node for node in ast.parse(source.read_text()).body
                        if isinstance(node, ast.FunctionDef) and node.name == "normalize")
        namespace = {"re": re, "unicodedata": unicodedata,
                     "URL": re.compile(r"(?i)(?:https?://|www\.)\S+")}
        exec(compile(ast.Module(body=[function], type_ignores=[]), str(source), "exec"), namespace)
        baseline = namespace["normalize"]
        samples = ["가 나 · 다", "가나·다", "a / b", "  첫  줄\r\n 둘째 줄 ",
                   "10 – 20", "\u1100\u1161", "https://example.invalid/a/b"]
        for kind, fixed in itertools.product(["text", "url"], [False, True]):
            for value in samples:
                # The current packet already prohibits URL-bearing kind=text.
                if kind == "text" and value.startswith("https://"): continue
                policy = {"text": value, "kind": kind, "fixed_newlines": fixed}
                self.assertEqual(normalize(value, policy), baseline(value, policy))


if __name__ == "__main__":
    unittest.main()
