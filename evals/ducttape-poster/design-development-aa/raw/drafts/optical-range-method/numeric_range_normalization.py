"""Optional prospective optical-range method; no actors, packets or scores.

This module is a draft, not an adopted replacement for any frozen helper.
No input text or metadata is mutated. Returned text is comparison text only.
"""
from __future__ import annotations

import re
import unicodedata

NORMALIZATION = "nfc-ws-optical-ranges-v2"
URL = re.compile(r"(?i)(?:https?://|www\.)\S+")
ENDPOINT = re.compile(r"[0-9]+(?:[.:][0-9]+)*\Z")


def _nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value.replace("\r\n", "\n").replace("\r", "\n"))


def _whitespace(value: str, entry: dict, fixed: bool | None = None) -> str:
    keep_newlines = entry["fixed_newlines"] if fixed is None else fixed
    if entry.get("fixed_spacing") is True:
        # Preserve every horizontal whitespace codepoint/run and outer gap.
        # Only an explicitly soft LF can become one ordinary word-space.
        return value if keep_newlines else value.replace("\n", " ")
    if keep_newlines:
        return "\n".join(re.sub(r"[^\S\n]+", " ", line).strip() for line in value.split("\n"))
    return re.sub(r"\s+", " ", value).strip()


def _pattern(declaration: dict) -> re.Pattern:
    # Anchors must be entire numeric tokens, never parts of a word, URL,
    # negative value, identifier or a longer decimal/time token.
    return re.compile(
        r"(?<![\w.:/+\-\u2013])(" + re.escape(declaration["left"]) +
        r") *(\u2013) *(" + re.escape(declaration["right"]) +
        r")(?![\w.:/+\-\u2013])"
    )


def _outside_urls(value: str, pattern: re.Pattern) -> list[re.Match]:
    protected = [(match.start(), match.end()) for match in URL.finditer(value)]
    return [match for match in pattern.finditer(value)
            if not any(match.start() < end and match.end() > start for start, end in protected)]


def validate_entry(entry: dict) -> tuple[re.Pattern, ...]:
    """Validate the *declared* source policy, never a critic's observed reading.

    Each allowed range is one unique literal pair in the supplied source.
    Duplicate/missing targets are deliberately unsupported, not guessed.
    """
    if not isinstance(entry, dict) or not isinstance(entry.get("text"), str) or not entry["text"]:
        raise ValueError("A nonempty actual supplied text entry is required")
    if entry.get("kind") not in ("text", "url") or type(entry.get("fixed_newlines")) is not bool:
        raise ValueError("kind=text/url and explicit boolean fixed_newlines are required")
    if "fixed_spacing" in entry and type(entry["fixed_spacing"]) is not bool:
        raise ValueError("fixed_spacing must be a boolean when declared")
    ranges = entry.get("optical_numeric_ranges", [])
    if not isinstance(ranges, list):
        raise ValueError("optical_numeric_ranges must be an array")
    if entry["kind"] == "text" and URL.search(entry["text"]):
        raise ValueError("URL-bearing supplied copy must use kind=url")
    if not ranges:
        return ()
    if entry["kind"] != "text" or entry.get("fixed_spacing") is not False:
        raise ValueError("Numeric optical ranges need kind=text and explicit fixed_spacing:false")
    source = _whitespace(_nfc(entry["text"]), entry)
    seen, spans, patterns = set(), [], []
    for declaration in ranges:
        if not isinstance(declaration, dict) or set(declaration) != {"left", "separator", "right"}:
            raise ValueError("A range declaration has exactly left/separator/right")
        if declaration["separator"] != "\u2013":
            raise ValueError("Only the exact U+2013 range separator is eligible")
        if any(not isinstance(declaration[key], str) or not ENDPOINT.fullmatch(declaration[key])
               for key in ("left", "right")):
            raise ValueError("Endpoints must be complete ASCII numeric/date/time tokens")
        identity = (declaration["left"], declaration["right"])
        if identity in seen:
            raise ValueError("Duplicate numeric range declarations are unsupported")
        seen.add(identity)
        pattern = _pattern(declaration)
        matches = _outside_urls(source, pattern)
        if len(matches) != 1:
            raise ValueError("A declared range must occur exactly once as complete source tokens")
        start, end = matches[0].span()
        if any(start < old_end and end > old_start for old_start, old_end in spans):
            raise ValueError("Overlapping range declarations are unsupported")
        spans.append((start, end))
        patterns.append(pattern)
    return tuple(patterns)


def _legacy_optical(value: str) -> str:
    pieces, previous = [], 0
    for match in URL.finditer(value):
        pieces.append(re.sub(r" *([\u00b7/]) *", r"\1", value[previous:match.start()]))
        pieces.append(match.group())
        previous = match.end()
    pieces.append(re.sub(r" *([\u00b7/]) *", r"\1", value[previous:]))
    return "".join(pieces)


def normalize(raw: str, entry: dict, *, fixed: bool | None = None) -> str:
    """Return a prospective comparison form, preserving raw and all symbols.

    ``fixed`` matches the old summary's layout-only diagnostic override. A
    fidelity comparison must use the default; that override cannot erase a
    client's newline condition for mandatory PASS.
    """
    if not isinstance(raw, str):
        raise ValueError("Actual raw transcription must be a string; no supplied-copy fallback")
    if fixed is not None and type(fixed) is not bool:
        raise ValueError("Diagnostic fixed override must be a boolean")
    patterns = validate_entry(entry)
    value = _whitespace(_nfc(raw), entry, fixed)
    if entry["kind"] == "url" or entry.get("fixed_spacing") is True:
        return value
    value = _legacy_optical(value)
    for pattern in patterns:
        matches = _outside_urls(value, pattern)
        if len(matches) == 1:
            match = matches[0]
            # Reuse matched observed characters, not a required-copy fallback.
            compact = "".join(match.group(index) for index in (1, 2, 3))
            value = value[:match.start()] + compact + value[match.end():]
    return value
