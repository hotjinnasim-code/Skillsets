# Planning-diagram renderer

This small helper renders a planning reference from explicit
JSON shapes and actual copy. It demonstrates selected text anatomy and planned
areas to image_gen. It is not poster generation, a quality gate, a benchmark, or
final approval. Final posters still use native image_gen. Follow the scoped use in
[layout-guide.md](layout-guide.md): with complex prose and practical information,
use an available suitable font and renderer to design actual copy and substantive
image-region geometry before the first native call. Simple-copy requests need no
mandatory guide. Without a usable font runtime, use the positive native brief.

The renderer uses Python stdlib and installed Pillow. It has no bitmap input,
image compositing, image_gen postprocessing, font downloads, embedded fonts,
house layout, automatic wrapping, or automatic font/style choices. Only supplied
shapes and actual lines appear on the canvas; measurement labels and numbers are
kept in the manifest. Planned areas are not automatically drawn. Supply an explicit
shape if a planned area should be visible.

Run from the current task/project workspace with an available Python containing Pillow:

```sh
python /path/to/skill/scripts/make_layout_guide.py your-spec.json --output-dir your-subdirectory --name your-new-name
```

This creates `your-new-name.svg`, `your-new-name.png`, and
`your-new-name.manifest.json`. All three use exclusive creation. If any filename
already exists, including a symlink, the renderer preserves it and removes only
new files reserved during that attempt. It never overwrites outputs. Ordinary
errors roll back the set; a killed process can leave a partial set, so choose a
fresh name after interruption.

The importable API is `render(spec_path, output_dir, name)` in
`make_layout_guide.py`; it returns a mapping from `.svg`, `.png`, and
`.manifest.json` to their new paths. Input JSON and output directories must resolve
inside the calling process’s current workspace, including through symlinks. Each
`render()` call captures the resolved current working directory once and passes
that boundary through input/output validation, relative-path resolution, manifest
input paths, and project-font checks. The module can be imported before entering
the task workspace; later calls capture their own workspace without changing a
module global. Relative paths resolve against that call's captured workspace.
The installed skill directory is never the output boundary. The output name accepts 1–80 ASCII letters,
digits, underscores, or hyphens, beginning with a letter or digit. Directories may
be created inside this boundary. CLI errors explain the constraint and exit 2;
the API raises `GuideError` for spec constraints and `OSError` for filesystem errors.

## Explicit JSON contract

Every listed field is required unless marked optional. Unknown fields and duplicate
JSON keys are rejected. Coordinates, sizes, spacing and measurements are in pixels.
Paint order is background, shapes in array order, then text blocks in array order.
Block positions belong to the creator's design; none is a universal requirement.

| Object | Fields and meaning |
| --- | --- |
| Root | `canvas`, `shapes`, `text_blocks`; the latter two are arrays, and at least one must be nonempty. |
| `canvas` | Positive integer `width`, `height`; explicit `background` of `#RRGGBB` or `"none"` for transparency. |
| Rectangle / ellipse | `type`: `"rect"` or `"ellipse"`; `x`, `y`, positive `width`, `height`, `fill`. An ellipse occupies this bounding rectangle. |
| Polygon | `type`: `"polygon"`; `points`: 3–256 distinct `[x, y]` pairs, implicitly closed; `fill`. Must enclose nonzero area without crossing/touching nonadjacent edges. |
| Line | `type`: `"line"`; `x1`, `y1`, `x2`, `y2`, distinct endpoints; `stroke`, positive integer `stroke_width`. |
| Shape paint | `fill` is `#RRGGBB` or `"none"`. Optional `stroke` and `stroke_width` must appear together. At least one paint must be visible. Lines require visible stroke. Strokes use round caps/joins. |
| Text block | `copy`, `lines`, `fixed_newlines`, `x`, `y`, `align`, `line_spacing`, `area`, `font`, `color`. |
| `copy` / `lines` | Full actual copy string and deliberate array of line strings; no invented print. See conservation below. |
| `fixed_newlines` | Explicit boolean: whether every original newline is fixed. |
| Text position | `x`, `y` locate the top-left of the planned area. `align` is `"left"`, `"center"`, or `"right"` within its width, using measured advance. |
| `line_spacing` | Positive baseline-to-baseline distance. First baseline is `y + font ascent`. Smaller spacing may deliberately overlap line boxes. No automatic adjustment. |
| `area` | Positive `width`, `height` of the planned area. Does not clip text or create visible art. |
| `font` | Explicit absolute installed font `path`, nonnegative integer face `index` (including for TTC), positive integer `size`. A non-collection font requires index 0. |
| Text `color` | Explicit `#RRGGBB`. |

Font paths must resolve under `/System/Library/Fonts`, `/Library/Fonts`, or the
current user's `~/Library/Fonts`, common Linux/Windows font directories, or explicit
font files inside the workspace captured for that render call. Fonts are read only when explicitly supplied.
No font binary is copied into the repository. The helper does not discover or
select fonts. Its installed-font tests read only
`/System/Library/Fonts/AppleSDGothicNeo.ttc` and
`/System/Library/Fonts/Supplemental/AppleMyungjo.ttf` when available; the corresponding tests
skip if their explicit font is absent, without substitution. Cmap and style-table
regressions also use synthetic in-memory table bytes. Project-font path tests use
temporary marker bytes and a mocked table parser; they do not copy a font binary.

Canvas dimensions are at most 8192 each, with at most 32 million pixels. Font size
and stroke width are at most 1024. There are at most 256 shapes, 128 text blocks,
256 lines per block, and 20000 copy characters per block. Input is at most 2 MB.
All numbers must be actual finite JSON numbers within ±1000000; booleans, nulls,
empty strings, NaN and infinity are invalid numbers. Positive/integer constraints
apply where specified. These bounds limit accidental resource exhaustion.

## Copy and font fidelity

For fixed newlines, `lines` must exactly equal `copy.split("\n")`. Empty lines and
a trailing newline remain explicit. For nonfixed newlines, every group must contain
non-whitespace copy, and `" ".join(lines)` must exactly equal
`copy.replace("\n", " ")`. Thus a boundary can replace one word space/nonfixed
newline, while words, punctuation, repeated spaces and leading/trailing spaces
remain conserved. No trimming or whitespace normalization occurs. Use LF (`\n`)
newlines; tabs, CR, Unicode line/paragraph separators, control/format characters and Unicode variation selectors are
unsupported and rejected. A line string itself cannot contain a newline.

SVG text is XML-escaped and uses preserved whitespace. PNG uses the exact supplied
font bytes and face index. The manifest records the actual family, style, index,
size, font-file SHA-256, available style metadata and Pillow layout engine.
When OS/2 exists, its actual weight/width/slant metadata supplies the numeric SVG
hints. When OS/2 is absent, numeric `weight` and `stretch_percent` are `null`;
available `head.macStyle` flags supply only nominal SVG `normal`/`bold` weight and
`normal`/`italic` style. The raw head flags and per-attribute provenance are
recorded. No numeric weight or width is inferred, and `font-stretch` is omitted
on this nominal path. If both style tables are absent, unavailable SVG style
attributes are omitted. Malformed present style tables remain errors.

For each requested character, nonzero-glyph coverage must agree across every
eligible Unicode format-4/12 cmap subtable. Uniformly absent characters fail with
their code points; disagreement fails with a clear unsupported-font error.
Unused-character disagreements are not checked. This conservative policy may
reject a usable face, including supplementary characters covered by format 12
alongside a format-4 BMP subtable that cannot represent them. It does not identify
FreeType's active cmap or prove that the loaded face uses a checked mapping.
Fonts without supported Unicode format-4/12 cmaps are unsupported. Variable font
axis selection, Unicode variation sequences and font fallback are outside this
first generation. The caller can skip this optional guide if the supplied font is
unsupported; the helper never changes copy or substitutes another font.

RAQM is used when present in installed Pillow; otherwise Pillow BASIC is used and
recorded. Cmap coverage does not establish correct complex-script shaping,
ligatures, emoji appearance, or text direction. SVG requests the actual installed
family and available style hints but cannot select a TTC index by file path without
embedding/outlining the font. A viewer may substitute a face. Pillow and SVG
viewers can differ in shaping, kerning and fractional rasterization. Treat SVG as
editable planning text and PNG as the supplied-font reference, not identical
pixel proofs. Neither asset applies that font to a future image_gen result.

## Measurements and clipping

The exclusive manifest includes the raw input SHA-256, output SVG/PNG hashes,
actual copy and line groups, per-line advance, coordinates, baselines, font bounds,
ascent/descent, planned area and measured overflow on each side. Layout bounds
include line boxes and advances (including whitespace and blank fixed lines);
painted font bounds use Pillow's glyph bounding boxes. Shape bounds include a
conservative half-stroke margin. Manifest metadata is never printed in the art.

Overflow beyond a planned area is reported in pixels and rendering proceeds if
the painted bounds stay on the canvas. This is a design measurement, with no
pixel-quality PASS/FAIL or score. **Painted bounds extending beyond the canvas
fail before any outputs are created**, so a creator is not handed an apparently
fitting clipped guide. Font bounding boxes and round-stroke bounds can be
conservative; raster edge rounding can differ by a pixel. This rule does not
evaluate poster quality or approve a design.

## Verification

```sh
python -B -m unittest -v test_layout_guide.py
```

Tests create only new disposable planning diagrams in temporary subdirectories
inside the current working workspace, and clean them up. They cover copy conservation,
fixed/blank/trailing newlines, XML escaping, actual font/index/hash metadata,
exclusive outputs and rollback, path/symlink boundaries, API import-then-chdir
behavior and one workspace snapshot per call, explicit project-font containment,
disagreeing supported cmaps, absent-OS/2 serif metadata, malformed shapes and
numbers, missing glyphs, alignment, and the distinction between measured planned
area overflow and canvas clipping. They never open bitmap inputs or inspect
existing posters or evaluation reports.
