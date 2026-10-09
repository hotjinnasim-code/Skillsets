"""Draft planning diagrams from explicit shapes and conserved copy; no bitmap inputs."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import struct
import sys
import unicodedata
from xml.sax.saxutils import escape, quoteattr

from PIL import Image, ImageDraw, ImageFont, features


SYSTEM_FONT_ROOTS = (
    Path("/System/Library/Fonts"),
    Path("/Library/Fonts"),
    Path.home() / "Library/Fonts",
    Path("/usr/share/fonts"),
    Path("/usr/local/share/fonts"),
    Path.home() / ".local/share/fonts",
    Path("C:/Windows/Fonts"),
    Path.home() / "AppData/Local/Microsoft/Windows/Fonts",
)
LIMITATIONS = [
    "DRAFT ONLY: optional planning reference, not a poster or an approval/quality gate.",
    "PNG uses the supplied font bytes and TTC index. SVG requests the installed "
    "family and available style metadata; head.macStyle provides nominal SVG "
    "weight/slant when OS/2 is absent, without inferred numeric weight/width. "
    "A viewer cannot be bound to a TTC index. "
    "No font is embedded, bundled or downloaded; SVG viewers may substitute fonts.",
    "Pillow and SVG viewers can differ in shaping, kerning and fractional rasterization. "
    "Requested-character coverage must agree across supported Unicode cmaps. "
    "This conservative check does not identify FreeType's active cmap or prove "
    "correct shaping or appearance.",
    "Only LF newlines in copy; no other control/format characters, Unicode line/paragraph "
    "separators, variation sequences or automatic font fallback. "
    "Only Unicode cmap formats 4 and 12 are supported.",
    "Measured planned-area overflow is a design measurement. Painted bounds outside "
    "the canvas stop rendering; shape stroke bounds are conservative.",
    "A reference does not apply fonts to image_gen. Final posters still use native image_gen; "
    "skip this optional guide when it is unhelpful or no usable font runtime exists.",
]


class GuideError(ValueError):
    """An input or output constraint the creator can correct."""


def require(condition, message):
    if not condition:
        raise GuideError(message)


def fields(value, required, optional=(), label="object"):
    require(isinstance(value, dict), f"{label} must be an object")
    require(set(required) <= value.keys(), f"{label} missing fields: {sorted(set(required) - value.keys())}")
    require(value.keys() <= set(required) | set(optional),
            f"{label} unknown fields: {sorted(value.keys() - set(required) - set(optional))}")


def number(value, label, positive=False, integer=False):
    require(type(value) in (int, float), f"{label} must be a finite number")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    require(finite and abs(value) <= 1_000_000, f"{label} must be finite and within +/-1000000")
    require(not positive or value > 0, f"{label} must be positive")
    require(not integer or type(value) is int, f"{label} must be an integer")
    return value


def color(value, label, allow_none=False):
    require(isinstance(value, str) and
            (bool(re.fullmatch(r"#[0-9a-fA-F]{6}", value)) or (allow_none and value == "none")),
            f"{label} must be #RRGGBB" + (" or 'none'" if allow_none else ""))
    return value


def bounded(path, label, workspace, exists=False):
    require(isinstance(path, (str, os.PathLike)) and bool(str(path)) and "\x00" not in str(path),
            f"{label} must be a nonempty filesystem path without NUL characters")
    candidate = Path(path)
    candidate = (candidate if candidate.is_absolute() else workspace / candidate).resolve()
    require(candidate.is_relative_to(workspace), f"{label} must stay inside {workspace}")
    require(not exists or candidate.is_file(), f"{label} must be an existing regular file")
    return candidate


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise GuideError(f"nonfinite JSON number: {value}")


def read_spec(path, workspace):
    path = bounded(path, "spec", workspace, exists=True)
    require(path.suffix.lower() == ".json", "spec must be a JSON file")
    require(path.stat().st_size <= 2_000_000, "spec is too large (maximum 2 MB)")
    raw = path.read_bytes()
    try:
        spec = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                          parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise GuideError(f"invalid UTF-8 JSON: {exc}") from exc
    return spec, {"path": str(path.relative_to(workspace)), "sha256": hashlib.sha256(raw).hexdigest()}


def text_value(value, label, multiline=False):
    require(isinstance(value, str), f"{label} must be text")
    for char in value:
        code = ord(char)
        if char == "\n" and multiline:
            continue
        require(unicodedata.category(char) not in ("Cc", "Cf", "Cs", "Zl", "Zp") and
                code not in (0xFFFE, 0xFFFF) and
                not (0xFE00 <= code <= 0xFE0F or 0xE0100 <= code <= 0xE01EF),
                f"{label} contains unsupported control/variation character U+{code:04X}")
    return value


def conserved_lines(block):
    copy = text_value(block["copy"], "copy", multiline=True)
    require(bool(copy.strip()) and len(copy) <= 20_000, "copy must be nonempty (maximum 20000 characters)")
    lines = block["lines"]
    require(isinstance(lines, list) and 0 < len(lines) <= 256, "lines must contain 1..256 explicit strings")
    for line in lines:
        text_value(line, "line")
    require(type(block["fixed_newlines"]) is bool, "fixed_newlines must be a boolean")
    if block["fixed_newlines"]:
        require(lines == copy.split("\n"), "fixed newlines require lines exactly equal to copy.split('\\n')")
    else:
        require(all(line.strip() for line in lines), "nonfixed line groups must be nonempty")
        require(" ".join(lines) == copy.replace("\n", " "),
                "line groups must conserve exact copy; only a word space/nonfixed newline may become a line boundary")
    return lines


def sfnt_tables(data, index):
    """Read one supplied SFNT/TTC face, without copying a font to disk."""
    try:
        if data[:4] == b"ttcf":
            count = struct.unpack_from(">I", data, 8)[0]
            require(index < count, f"TTC index {index} is outside 0..{count - 1}")
            base = struct.unpack_from(">I", data, 12 + 4 * index)[0]
        else:
            require(index == 0, "a non-collection font requires index 0")
            base = 0
        require(data[base:base + 4] in (b"\x00\x01\x00\x00", b"OTTO", b"true"),
                "supplied font must be a supported SFNT/TTC font")
        count = struct.unpack_from(">H", data, base + 4)[0]
        tables = {}
        for slot in range(count):
            tag, _, offset, length = struct.unpack_from(">4sIII", data, base + 12 + 16 * slot)
            require(offset + length <= len(data), "font contains an out-of-bounds table")
            tables[tag] = data[offset:offset + length]
        return tables
    except struct.error as exc:
        raise GuideError("supplied font has truncated SFNT/TTC tables") from exc


def cmap_coverage(table):
    """Require consistent coverage in supported cmaps, without selecting a cmap."""
    maps = []
    try:
        count = struct.unpack_from(">H", table, 2)[0]
        for slot in range(count):
            platform, encoding, offset = struct.unpack_from(">HHI", table, 4 + 8 * slot)
            if platform != 0 and (platform != 3 or encoding not in (1, 10)):
                continue
            fmt = struct.unpack_from(">H", table, offset)[0]
            if fmt == 4:
                length, _, seg_twice = struct.unpack_from(">HHH", table, offset + 2)
                sub = table[offset:offset + length]
                n = seg_twice // 2
                require(n > 0 and len(sub) == length and 16 + 8 * n <= length, "invalid format 4 cmap")
                maps.append((4, sub, n))
            elif fmt == 12:
                length = struct.unpack_from(">I", table, offset + 4)[0]
                sub = table[offset:offset + length]
                groups = struct.unpack_from(">I", sub, 12)[0]
                require(len(sub) == length and 16 + 12 * groups <= length, "invalid format 12 cmap")
                maps.append((12, sub, groups))
        require(bool(maps), "font has no supported Unicode cmap (formats 4/12)")

        def map_has_glyph(code, fmt, sub, n):
            try:
                if fmt == 12:
                    # Binary search avoids scanning a large CJK coverage table per character.
                    low, high = 0, n
                    while low < high:
                        middle = (low + high) // 2
                        start, end, glyph = struct.unpack_from(">III", sub, 16 + 12 * middle)
                        if code < start:
                            high = middle
                        elif code > end:
                            low = middle + 1
                        else:
                            if glyph + code - start != 0:
                                return True
                            break
                elif code <= 0xFFFF:
                    for slot in range(n):
                        end = struct.unpack_from(">H", sub, 14 + 2 * slot)[0]
                        start = struct.unpack_from(">H", sub, 16 + 2 * n + 2 * slot)[0]
                        if start <= code <= end:
                            delta = struct.unpack_from(">h", sub, 16 + 4 * n + 2 * slot)[0]
                            address = 16 + 6 * n + 2 * slot
                            relative = struct.unpack_from(">H", sub, address)[0]
                            glyph = ((code + delta) & 0xFFFF) if not relative else 0
                            if relative:
                                glyph = struct.unpack_from(">H", sub, address + relative + 2 * (code - start))[0]
                                glyph = ((glyph + delta) & 0xFFFF) if glyph else 0
                            if glyph:
                                return True
                            break
                return False
            except struct.error as exc:
                raise GuideError("supplied font has a malformed Unicode cmap") from exc

        def has_glyph(code):
            present = [map_has_glyph(code, *cmap) for cmap in maps]
            require(all(present) or not any(present),
                    f"unsupported font: supported Unicode cmaps disagree on glyph coverage for U+{code:04X}")
            return all(present)

        return has_glyph
    except (struct.error, TypeError) as exc:
        raise GuideError("supplied font has a malformed Unicode cmap") from exc


def font_style_metadata(tables):
    """Read numeric OS/2 metadata or explicit, nominal head.macStyle flags."""
    head_style = struct.unpack_from(">H", tables[b"head"], 44)[0] if b"head" in tables else None
    weight, stretch, slant = None, None, None
    svg_style = {}
    provenance = {"weight": None, "stretch_percent": None, "slant": None, "svg_style": {}}
    if b"OS/2" in tables:
        weight, width = struct.unpack_from(">HH", tables[b"OS/2"], 4)
        selection = struct.unpack_from(">H", tables[b"OS/2"], 62)[0]
        require(1 <= weight <= 1000 and 1 <= width <= 9, "font has invalid OS/2 style metadata")
        stretch = (50, 62.5, 75, 87.5, 100, 112.5, 125, 150, 200)[width - 1]
        slant = "italic" if selection & 1 else ("oblique" if selection & 512 else "normal")
        svg_style = {"font-weight": weight, "font-stretch": f"{stretch}%", "font-style": slant}
        provenance.update({"weight": "OS/2.usWeightClass", "stretch_percent": "OS/2.usWidthClass",
                           "slant": "OS/2.fsSelection",
                           "svg_style": {"font-weight": "OS/2.usWeightClass", "font-stretch": "OS/2.usWidthClass",
                                         "font-style": "OS/2.fsSelection"}})
    elif head_style is not None:
        slant = "italic" if head_style & 2 else "normal"
        svg_style = {"font-weight": "bold" if head_style & 1 else "normal", "font-style": slant}
        provenance.update({"slant": "head.macStyle",
                           "svg_style": {"font-weight": "head.macStyle (nominal)",
                                         "font-style": "head.macStyle (nominal)"}})
    return {"weight": weight, "stretch_percent": stretch, "slant": slant,
            "head_mac_style": head_style, "svg_style": svg_style, "style_provenance": provenance}


def load_font(request, cache, workspace):
    fields(request, {"path", "index", "size"}, label="font")
    require(isinstance(request["path"], str) and "\x00" not in request["path"] and Path(request["path"]).is_absolute(),
            "font.path must be an explicit absolute available font path")
    path = Path(request["path"]).resolve()
    require(path.is_relative_to(workspace) or
            any(path.is_relative_to(root.resolve()) for root in SYSTEM_FONT_ROOTS if root.is_absolute()),
            "font.path must refer to an available system or current-workspace font directory")
    require(path.is_file(), "supplied system font is unavailable; skip the optional guide or supply an available font")
    index = number(request["index"], "font.index", integer=True)
    size = number(request["size"], "font.size", positive=True, integer=True)
    require(index >= 0 and size <= 1024, "font index must be nonnegative and size must be <=1024 px")
    key = (str(path), index, size)
    if key in cache:
        return cache[key]
    data = path.read_bytes()
    tables = sfnt_tables(data, index)
    require(b"cmap" in tables, "font requires a Unicode cmap")
    coverage = cmap_coverage(tables[b"cmap"])
    try:
        style_metadata = font_style_metadata(tables)
        engine = ImageFont.Layout.RAQM if features.check_feature("raqm") else ImageFont.Layout.BASIC
        font = ImageFont.truetype(io.BytesIO(data), size=size, index=index, layout_engine=engine)
    except (OSError, struct.error) as exc:
        raise GuideError(f"could not load supplied font face: {exc}") from exc
    family, style = font.getname()
    info = {"path": str(path), "index": index, "size_px": size,
            "sha256": hashlib.sha256(data).hexdigest(), "family": family, "style": style,
            **style_metadata,
            "layout_engine": engine.name}
    cache[key] = (font, coverage, info)
    return cache[key]


def bounds(points, padding=0):
    return [min(p[0] for p in points) - padding, min(p[1] for p in points) - padding,
            max(p[0] for p in points) + padding, max(p[1] for p in points) + padding]


def overflow(box, area):
    return {"left": max(0, area[0] - box[0]), "top": max(0, area[1] - box[1]),
            "right": max(0, box[2] - area[2]), "bottom": max(0, box[3] - area[3])}


def inside_canvas(box, canvas, label):
    excess = overflow(box, [0, 0, canvas["width"], canvas["height"]])
    require(not any(excess.values()), f"{label} would clip the canvas; measured overflow (px): {excess}")


def simple_polygon(points):
    def cross(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    def touches(a, b, c):
        return cross(a, b, c) == 0 and min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])

    require(len(set(map(tuple, points))) == len(points), "polygon vertices must be distinct; closure is implicit")
    edges = list(zip(points, points[1:] + points[:1]))
    for i, (a, b) in enumerate(edges):
        for j, (c, d) in enumerate(edges[i + 1:], i + 1):
            if j == i + 1 or (i == 0 and j == len(edges) - 1):
                continue
            intersects = (cross(a, b, c) * cross(a, b, d) < 0 and cross(c, d, a) * cross(c, d, b) < 0)
            require(not intersects and not any((touches(a, b, c), touches(a, b, d), touches(c, d, a), touches(c, d, b))),
                    "polygon must be simple; nonadjacent edges cannot cross or touch")
    require(sum(a[0] * b[1] - b[0] * a[1] for a, b in edges) != 0, "polygon must enclose nonzero area")


def validate_shape(shape, canvas):
    require(isinstance(shape, dict), "shape must be an object")
    kind = shape.get("type")
    require(kind in ("rect", "ellipse", "polygon", "line"), "shape.type must be rect, ellipse, polygon or line")
    geometry = {"rect": {"x", "y", "width", "height"}, "ellipse": {"x", "y", "width", "height"},
                "polygon": {"points"}, "line": {"x1", "y1", "x2", "y2"}}[kind]
    fields(shape, {"type"} | geometry | ({"stroke", "stroke_width"} if kind == "line" else {"fill"}),
           () if kind == "line" else {"stroke", "stroke_width"}, "shape")
    stroke = color(shape.get("stroke", "none"), "shape.stroke", allow_none=True)
    require(("stroke" in shape) == ("stroke_width" in shape), "stroke and stroke_width must be supplied together")
    width = number(shape["stroke_width"], "stroke_width", positive=True, integer=True) if "stroke_width" in shape else 0
    require(width <= 1024, "stroke_width must be <=1024 px")
    fill = color(shape["fill"], "shape.fill", allow_none=True) if kind != "line" else "none"
    require(stroke != "none" or fill != "none", "shape must have explicit visible paint")
    if kind == "polygon":
        points = shape["points"]
        require(isinstance(points, list) and 3 <= len(points) <= 256, "polygon requires 3..256 points")
        for point in points:
            require(isinstance(point, list) and len(point) == 2, "each polygon point must be [x, y]")
            for value in point:
                number(value, "polygon coordinate")
        simple_polygon(points)
    elif kind == "line":
        for key in geometry:
            number(shape[key], key)
        points = [[shape["x1"], shape["y1"]], [shape["x2"], shape["y2"]]]
        require(points[0] != points[1], "line endpoints must differ")
    else:
        for key in geometry:
            number(shape[key], key, positive=key in ("width", "height"))
        x, y, w, h = (shape[key] for key in ("x", "y", "width", "height"))
        points = [[x, y], [x + w, y + h]]
    box = bounds(points, width / 2 if stroke != "none" else 0)
    inside_canvas(box, canvas, "shape")
    return {"type": kind, "painted_bounds_px": box}


def measure_block(block, canvas, cache, workspace):
    fields(block, {"copy", "lines", "fixed_newlines", "x", "y", "align", "line_spacing", "area", "font", "color"}, label="text block")
    lines = conserved_lines(block)
    x, y = number(block["x"], "text.x"), number(block["y"], "text.y")
    spacing = number(block["line_spacing"], "line_spacing", positive=True)
    require(block["align"] in ("left", "center", "right"), "align must be left, center or right")
    color(block["color"], "text.color")
    fields(block["area"], {"width", "height"}, label="area")
    w = number(block["area"]["width"], "area.width", positive=True)
    h = number(block["area"]["height"], "area.height", positive=True)
    font, coverage, font_info = load_font(block["font"], cache, workspace)
    missing = sorted({ord(c) for c in block["copy"] if c != "\n" and not coverage(ord(c))})
    require(not missing, "supplied font lacks glyphs: " + ", ".join(f"U+{c:04X}" for c in missing))
    ascent, descent = font.getmetrics()
    measured, layout_points, painted_points = [], [], []
    for i, line in enumerate(lines):
        advance = font.getlength(line)
        pen_x = x + {"left": 0, "center": (w - advance) / 2, "right": w - advance}[block["align"]]
        baseline = y + ascent + i * spacing
        left, top, right, bottom = font.getbbox(line, anchor="ls")
        box = [pen_x + left, baseline + top, pen_x + right, baseline + bottom]
        if top != bottom:
            inside_canvas(box, canvas, "text glyph bounds")
            painted_points.extend([[box[0], box[1]], [box[2], box[3]]])
        layout_points.extend([[min(pen_x, box[0]), y + i * spacing],
                              [max(pen_x + advance, box[2]), baseline + descent]])
        measured.append({"text": line, "x_px": pen_x, "baseline_px": baseline,
                         "advance_px": advance, "font_bounds_px": box})
    area = [x, y, x + w, y + h]
    layout = bounds(layout_points)
    info = {"copy": block["copy"], "lines": list(lines), "fixed_newlines": block["fixed_newlines"],
            "font": font_info, "color": block["color"], "alignment": block["align"],
            "line_spacing_px": spacing, "ascent_px": ascent, "descent_px": descent,
            "planned_area_px": area, "layout_bounds_px": layout,
            "painted_font_bounds_px": bounds(painted_points) if painted_points else None,
            "planned_area_overflow_px": overflow(layout, area), "line_measurements": measured}
    return font, info


def svg_shape(shape):
    kind = shape["type"]
    attributes = {key: value for key, value in shape.items() if key not in ("type", "points", "stroke_width")}
    if kind == "ellipse":
        attributes = {"cx": shape["x"] + shape["width"] / 2, "cy": shape["y"] + shape["height"] / 2,
                      "rx": shape["width"] / 2, "ry": shape["height"] / 2,
                      **{key: value for key, value in attributes.items() if key not in ("x", "y", "width", "height")}}
    if kind == "polygon":
        attributes["points"] = " ".join(f"{x},{y}" for x, y in shape["points"])
    if "stroke_width" in shape:
        attributes.update({"stroke-width": shape["stroke_width"], "stroke-linejoin": "round", "stroke-linecap": "round"})
    return "<" + kind + " " + " ".join(f"{key}={quoteattr(str(value))}" for key, value in attributes.items()) + "/>"


def draw_shape(draw, shape):
    kind = shape["type"]
    fill = None if shape.get("fill", "none") == "none" else shape["fill"]
    stroke = None if shape.get("stroke", "none") == "none" else shape["stroke"]
    width = shape.get("stroke_width", 0)
    if kind in ("rect", "ellipse"):
        x, y, w, h = (shape[key] for key in ("x", "y", "width", "height"))
        box = [x, y, x + w, y + h]
        if kind == "ellipse":
            draw.ellipse(box, fill=fill)
            if stroke:
                draw.ellipse([x - width / 2, y - width / 2, x + w + width / 2, y + h + width / 2], outline=stroke, width=width)
            return
        points = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    elif kind == "polygon":
        points = list(map(tuple, shape["points"]))
    else:
        points = [(shape["x1"], shape["y1"]), (shape["x2"], shape["y2"])]
    if fill:
        draw.polygon(points, fill=fill)
    if stroke:
        draw.line(points + ([points[0]] if kind != "line" else []), fill=stroke, width=width, joint="curve")
        # Round caps/joins agree with the explicit SVG stroke policy.
        radius = width / 2
        for x, y in points:
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=stroke)


def exclusive_outputs(directory, name, payloads, workspace):
    directory = bounded(directory, "output directory", workspace)
    require(isinstance(name, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", name),
            "name must contain 1..80 ASCII letters, digits, underscores or hyphens, starting with a letter/digit")
    directory.mkdir(parents=True, exist_ok=True)
    opened = []
    try:
        # Reserve the whole set before writing; never truncate an existing file.
        for suffix, payload in payloads.items():
            path = directory / f"{name}{suffix}"
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            opened.append((fd, path, payload))
        for fd, _, payload in opened:
            with os.fdopen(fd, "wb", closefd=False) as handle:
                handle.write(payload)
    except FileExistsError as exc:
        for _, path, _ in opened:
            path.unlink()
        raise GuideError("output already exists; use a new name (SVG, PNG and manifest are exclusive)") from exc
    except BaseException:
        for _, path, _ in opened:
            path.unlink()
        raise
    finally:
        for fd, _, _ in opened:
            os.close(fd)
    return {suffix: path for suffix, (_, path, _) in zip(payloads, opened)}


def render(spec_path, output_dir, name):
    """Create a new SVG, PNG and exclusive manifest inside the current working workspace."""
    workspace = Path.cwd().resolve()
    # Validate destinations before loading fonts or allocating a canvas.
    directory = bounded(output_dir, "output directory", workspace)
    require(isinstance(name, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", name), "invalid output name")
    spec, input_info = read_spec(spec_path, workspace)
    fields(spec, {"canvas", "shapes", "text_blocks"}, label="spec")
    canvas = spec["canvas"]
    fields(canvas, {"width", "height", "background"}, label="canvas")
    for key in ("width", "height"):
        number(canvas[key], f"canvas.{key}", positive=True, integer=True)
        require(canvas[key] <= 8192, "canvas dimensions must be <=8192 px")
    require(canvas["width"] * canvas["height"] <= 32_000_000, "canvas must be <=32 million pixels")
    color(canvas["background"], "canvas.background", allow_none=True)
    require(isinstance(spec["shapes"], list) and len(spec["shapes"]) <= 256, "shapes must be a list of at most 256 shapes")
    require(isinstance(spec["text_blocks"], list) and len(spec["text_blocks"]) <= 128, "text_blocks must be a list of at most 128 blocks")
    require(spec["shapes"] or spec["text_blocks"], "diagram must contain a shape or actual-copy block")
    shape_info = [validate_shape(shape, canvas) for shape in spec["shapes"]]
    cache = {}
    blocks = [measure_block(block, canvas, cache, workspace) for block in spec["text_blocks"]]
    background = (0, 0, 0, 0) if canvas["background"] == "none" else canvas["background"]
    image = Image.new("RGBA", (canvas["width"], canvas["height"]), background)
    draw = ImageDraw.Draw(image)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas["width"]}" height="{canvas["height"]}" viewBox="0 0 {canvas["width"]} {canvas["height"]}">']
    if canvas["background"] != "none":
        svg.append(f'<rect width="100%" height="100%" fill="{canvas["background"]}"/>')
    for shape in spec["shapes"]:
        draw_shape(draw, shape)
        svg.append(svg_shape(shape))
    for font, info in blocks:
        face = info["font"]
        for line in info["line_measurements"]:
            draw.text((line["x_px"], line["baseline_px"]), line["text"], font=font, fill=info["color"], anchor="ls")
            # Text is literal XML content; preserved spaces do not collapse in SVG.
            attrs = {"x": line["x_px"], "y": line["baseline_px"], "fill": info["color"],
                     "font-family": json.dumps(face["family"], ensure_ascii=False),
                     "font-size": face["size_px"], **face["svg_style"],
                     "xml:space": "preserve", "style": "white-space:pre;font-synthesis:none"}
            svg.append("<text " + " ".join(f"{key}={quoteattr(str(value))}" for key, value in attrs.items()) + ">" + escape(line["text"]) + "</text>")
    svg.append("</svg>")
    svg_bytes = ("\n".join(svg) + "\n").encode("utf-8")
    png_buffer = io.BytesIO()
    image.save(png_buffer, format="PNG")
    png_bytes = png_buffer.getvalue()
    manifest = {"schema_version": 1, "draft_only": True, "purpose": "optional native planning reference",
                "input": input_info, "canvas": canvas, "shapes": shape_info,
                "text_blocks": [info for _, info in blocks], "limitations": LIMITATIONS,
                "outputs": {"svg": {"file": f"{name}.svg", "sha256": hashlib.sha256(svg_bytes).hexdigest()},
                            "png": {"file": f"{name}.png", "sha256": hashlib.sha256(png_bytes).hexdigest()},
                            "manifest": {"file": f"{name}.manifest.json"}}}
    payloads = {".svg": svg_bytes, ".png": png_bytes,
                ".manifest.json": (json.dumps(manifest, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")}
    return exclusive_outputs(directory, name, payloads, workspace)


def main():
    parser = argparse.ArgumentParser(description="DRAFT ONLY: render an explicit JSON planning diagram; exclusive outputs.")
    parser.add_argument("spec", help="JSON spec inside the current working workspace")
    parser.add_argument("--output-dir", required=True, help="directory inside the current working workspace")
    parser.add_argument("--name", required=True, help="new output stem, without a suffix")
    args = parser.parse_args()
    workspace = Path.cwd().resolve()
    try:
        paths = render(args.spec, args.output_dir, args.name)
    except (GuideError, OSError) as exc:
        print(f"Draft guide not rendered: {exc}", file=sys.stderr)
        return 2
    print("Created draft planning guide:")
    for path in paths.values():
        print(path.relative_to(workspace))
    return 0


if __name__ == "__main__":
    sys.exit(main())
