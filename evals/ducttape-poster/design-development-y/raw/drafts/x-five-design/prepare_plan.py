"""Author ONE prospective five-direction plan; font metrics only, no raster or render."""
from copy import deepcopy
from pathlib import Path
import json
from PIL import ImageFont

ROOT = Path("/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster")
OUT = ROOT / "drafts/x-five-design"
SOURCE = ROOT / "work/round20/planning/single-five-case.json"
source = json.loads(SOURCE.read_text(encoding="utf-8"))["cases"][0]
copy = deepcopy(source["copy"])
SANS = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
SERIF = "/System/Library/Fonts/Supplemental/AppleMyungjo.ttf"
BODY3 = [
    "작은 화분부터 오래 키운 나무까지 만납니다.",
    "재배자의 이야기를 듣고,",
    "우리 집의 빛과 생활에 맞는 식물을 골라보세요.",
]
BODY2 = [
    "작은 화분부터 오래 키운 나무까지 만납니다.",
    "재배자의 이야기를 듣고, 우리 집의 빛과 생활에 맞는 식물을 골라보세요.",
]
BODY5 = [
    "작은 화분부터 오래 키운",
    "나무까지 만납니다.",
    "재배자의 이야기를 듣고,",
    "우리 집의 빛과 생활에 맞는",
    "식물을 골라보세요.",
]


def region(entry, x, y, width, height, size, *, face=2, serif=False,
           lines=None, leading=None):
    return {
        "entry": entry,
        "copy": copy[entry - 1]["text"],
        "lines": lines or [copy[entry - 1]["text"]],
        "fixed_newlines": copy[entry - 1]["fixed_newlines"],
        "x": x, "y": y, "align": "left",
        "line_spacing": leading or round(size * 1.35),
        "area": {"width": width, "height": height},
        "font": {"path": SERIF if serif else SANS,
                 "index": 0 if serif else face, "size": size},
        "color": "#202624",
    }


def rect(x, y, width, height, fill):
    return {"type": "rect", "x": x, "y": y, "width": width,
            "height": height, "fill": fill}


def ellipse(x, y, width, height, fill):
    return {"type": "ellipse", "x": x, "y": y, "width": width,
            "height": height, "fill": fill}


def polygon(points, fill):
    return {"type": "polygon", "points": points, "fill": fill}


def concept(image_geometry, shapes, regions):
    canvas = {"width": 1600, "height": 900, "background": "#F2F1EE"}
    return {
        "status": "Authored neutral planning spec only; not rendered or generated",
        "canvas": canvas,
        "image_geometry_concepts": image_geometry,
        "text_regions": regions,
        "shapes": shapes,
        "limits": [
            "1600x900 and installed-font anatomy are current planning choices, not new client pixel rules or final-font certification.",
            "Neutral object and crop shapes denote substantive image structure. They are new own planning inputs, not final poster style or a borrowed raster.",
            "No shape, stem, pot edge, divider or shadow mark is placed inside text or immediately beside glyphs; broad separate mass boundaries carry transitions.",
            "Later native generation makes the complete final poster including all copy directly; no manual type overlay or bitmap final composition.",
            "Coordinates and line counts may change where the actual result preserves conditions, meaningful reading and substantial whole-system distinction.",
        ],
    }


directions = [
    {
        "role": "R21-C1-M1", "ratio": "16:9",
        "working_name_not_printed": "A close nursery encounter at two photographic distances",
        "whole_relationship": "A left full-height close nursery encounter and an upper-right detail edit create an L-shaped photographic whole; its right reading area identifies the market immediately, explains selection, then descends through locally paired visit and care rows.",
        "positive_direction": """Make the decision to choose a living plant tangible through photographic distance. The left picture occupies the full poster height: look obliquely along a real nursery bench crowded with several differently scaled, clearly planted houseplants. A cropped grower's unlettered apron and one hand steadying a modest pot establish this as a shared market encounter, with readable support rather than a posed mascot. Crop pot rims and selected leaves close, with stems attached to their actual bases; retain a farther taller plant inside the crowded view so small and established plants coexist. Across the upper-right edge, edit three unequal close details of leaf attachment, pot rim and visible soil; their tight shared crop edge establishes the breadth of the market rather than inventing technical labels.

Immediately below this upper crop, the Korean identity and nearby market name tell the viewer what this is. The Latin companion belongs locally to that identity. A smaller slogan begins a broad three-line explanation, with a medium-weight mature Korean sans body, open counters, stable syllable proportions, proportional Latin and lining numerals. Give the actual paragraph enough width and normal leading before deciding the photo boundaries. Use a controlled Korean serif title of modest optical weight; the event identifier stays clearly readable beside it.

At the paragraph's end, the date/hours row begins on the same left axis. Venue and access form the next row; care follows locally, then the invitation and URL share the final row. The row spacing distinguishes functions without adding labels or dividers. These are substantial readable lines, not a footer. Keep the whole in cool natural greens, warm gray pottery, convincing daylight and crisp planar type. The continuous left view, upper detail edit and right prose-led reading plane are one photographic editorial relationship.""",
        "hierarchy": {
            "primary": {"entry": 1, "role": "Modest serif identity at the right crop's reading entrance."},
            "support": [{"entry": 5, "role": "Market identifier immediately adjoining the title cluster."},
                        {"entry": 2, "role": "Close smaller Latin companion."},
                        {"entry": 3, "role": "Slogan introduces prose immediately below."}],
            "explanation": {"entries": [4], "shape": "Broad three-line right paragraph under the upper detail crop."},
            "visit": {"entries": [6, 7, 8], "shape": "Date/hours row, then venue on the same local start."},
            "next_action": {"entries": [9, 10, 11, 12], "shape": "Access adjoins venue; care next, then invitation/URL together."},
        },
        "body_line_groups": BODY3,
        "body_end_to_next_info": "One local vertical gap on the paragraph's left axis leads directly to the date; hours shares that first useful row. Venue/access, care and invitation/URL continue in the same right area without searching a different corner.",
        "nearest_peer": {
            "role_id": "R21-C1-M4",
            "structural_distinction": "M1 is an L-shaped nursery/detail edit with useful reading inside one broad right area. M4 uses two large close contact crops enclosing a central five-line paragraph, schedule already beside the upper identity, and two local action rows under the paragraph.",
            "style_distinction": "M1 is color photography emphasizing multiple planted scales and close nursery surfaces. M4 is a strongly cropped monochrome workbench/contact image, emphasizing hands, supported rootball and pot.",
        },
        "guide_geometry_concept": concept([
            {"bounds": [0, 0, 560, 900], "content": "Full-height oblique nursery bench, attached plant stems, several pot sizes and a larger farther plant; not a blank image panel."},
            {"bounds": [650, 0, 950, 190], "content": "Unequal tight photographic leaf/pot/soil details across the upper edge, not three equal decorative thumbnails."},
        ], [
            rect(0, 0, 560, 900, "#D6D7D2"),
            polygon([[0, 0], [185, 0], [205, 166], [154, 244], [0, 214]], "#BEC2B6"),
            polygon([[20, 520], [535, 340], [535, 385], [20, 575]], "#8F938C"),
            polygon([[40, 600], [175, 600], [152, 840], [73, 840]], "#AAAFA6"),
            polygon([[202, 548], [332, 510], [310, 760], [244, 785]], "#A1A69E"),
            polygon([[350, 468], [515, 425], [495, 688], [390, 727]], "#979D93"),
            polygon([[0, 565], [70, 566], [114, 596], [110, 622], [56, 613], [0, 596]], "#C3C6BD"),
            polygon([[82, 608], [62, 332], [83, 275], [95, 606]], "#838A7E"),
            ellipse(5, 302, 122, 162, "#ADB4A5"),
            ellipse(120, 258, 112, 206, "#99A38E"),
            ellipse(275, 142, 172, 330, "#A4AD9C"),
            polygon([[390, 470], [406, 60], [426, 40], [412, 462]], "#818A77"),
            ellipse(424, 31, 125, 260, "#B7BEAD"),
            rect(650, 0, 275, 185, "#D0D4C9"),
            ellipse(685, 35, 200, 120, "#A1AC96"),
            rect(941, 0, 384, 185, "#DCDDD8"),
            polygon([[970, 158], [988, 35], [1267, 60], [1272, 170]], "#A7A9A2"),
            rect(1341, 0, 259, 185, "#D0CEC5"),
            ellipse(1370, 20, 199, 145, "#A6A399"),
        ], [
            region(1, 650, 240, 870, 70, 50, serif=True),
            region(5, 650, 318, 440, 53, 38, face=4),
            region(2, 1140, 318, 400, 51, 34),
            region(3, 650, 379, 900, 54, 40),
            region(4, 650, 440, 900, 166, 40, lines=BODY3, leading=54),
            region(6, 650, 621, 430, 54, 40),
            region(7, 1120, 621, 430, 53, 38),
            region(8, 650, 681, 330, 52, 38),
            region(9, 1030, 681, 520, 52, 38),
            region(10, 650, 741, 900, 52, 38),
            region(11, 650, 803, 470, 51, 36),
            region(12, 1170, 803, 380, 48, 34),
        ]),
    },
    {
        "role": "R21-C1-M2", "ratio": "16:9",
        "working_name_not_printed": "The market is a lively horizon of different plants",
        "whole_relationship": "A full-width mid-height plant frieze separates one close upper identity-and-schedule relation from a nearly full-width two-line lower paragraph; that paragraph descends directly into two spacious action rows instead of a right-tree/upper-left-prose scaffold.",
        "positive_direction": """Make a full-width graphic market horizon from the actual range of plants. Look across a nursery table close enough to distinguish compact leafy pots, narrow blades and a branching larger plant, but render them through energetic observed ink contours and substantial screen-printed color planes. Let their heights rise and fall across the middle of the landscape; clear stems enter real pot rims, and some broad leaves cross the crop. A larger open pot-and-soil detail continues the table's right end downward, giving the care subject a concrete presence. This is a coherent crowded botanical horizon without mascots, labels or decorative leaf icons.

The upper-left market name and Korean title form one immediate purpose cluster. Latin is a compact companion, and the slogan belongs to that same upper entry. Date, hours and venue are a nearby upper-right schedule cluster, clearly subordinate to the market identifier but large enough for immediate visiting decisions. Their optical axes and similar row rhythm connect the top across the actual table rather than scattering one item per corner.

Below the plant horizon, set the full explanation as two broad meaning lines on one left start, in precise medium-weight Korean sans with open inner spaces, stable proportions and clean numeric and Latin forms. Its first line introduces the range of plants; its second describes the grower's story and home-specific selection. Reserve the real nearly full-width reading area and normal leading before editing the table. Its final line is followed directly below by the access/care row, then the invitation/URL row. These substantial useful rows extend the table's actual horizontal rhythm. Keep warm ochre, strong coral-red details, olive and dense charcoal as controlled plant/table planes; make small copy crisp and flat. The substantive plant horizon, upper purpose/schedule and wide prose-to-action ledge organize the whole, rather than a passive information panel dressed by an image strip.""",
        "hierarchy": {
            "primary": {"entry": 5, "role": "Upper-left market identifier introduces purpose immediately."},
            "support": [{"entry": 1, "role": "Korean identity immediately below market name."},
                        {"entry": 2, "role": "Latin companion on the local upper entry."},
                        {"entry": 3, "role": "Promise beside the local identity."}],
            "visit": {"entries": [6, 7, 8], "shape": "Three aligned schedule rows in the adjacent upper-right cluster."},
            "explanation": {"entries": [4], "shape": "Nearly full-width two-line paragraph directly under the actual botanical horizon."},
            "next_action": {"entries": [9, 10, 11, 12], "shape": "Two generous full-width useful rows immediately below the prose."},
        },
        "body_line_groups": BODY2,
        "body_end_to_next_info": "The paragraph ends over the access start on its own left edge with one short vertical gap; care shares that row, followed immediately by invitation and URL in the next row. Schedule was already encountered in a close upper cluster.",
        "nearest_peer": {
            "role_id": "R21-C1-M1",
            "structural_distinction": "M2's dominant image is a mid-height full-width horizon, with schedule above and prose/action below. M1 uses a full-height left encounter plus upper-right detail crop, with all useful prose/schedule/actions inside the right reading plane.",
            "style_distinction": "M2 uses observed ink contours and controlled bold printed color planes; M1 uses camera-specific botanical surfaces and light.",
        },
        "guide_geometry_concept": concept([
            {"bounds": [0, 272, 1600, 242], "content": "A full-width rising/falling market-table plant horizon; many actual attached pots and leaf types organize this major image."},
            {"bounds": [1070, 344, 450, 156], "content": "A closer pot rim and soil detail joins the horizon's right end; one cropped supporting hand makes the market selection/care relationship concrete."},
        ], [
            polygon([[0, 464], [1600, 444], [1600, 514], [0, 512]], "#B3B7AE"),
            polygon([[36, 410], [185, 408], [165, 501], [58, 503]], "#949C8C"),
            ellipse(20, 300, 190, 103, "#BDC6B2"),
            polygon([[276, 412], [420, 401], [406, 496], [297, 501]], "#A6AD9E"),
            polygon([[323, 409], [284, 280], [319, 309], [347, 408]], "#899680"),
            polygon([[360, 408], [403, 280], [392, 335], [373, 408]], "#A0AA95"),
            polygon([[505, 405], [675, 397], [651, 497], [531, 500]], "#909A87"),
            ellipse(477, 272, 217, 127, "#B4BFAB"),
            polygon([[817, 407], [978, 400], [960, 491], [839, 494]], "#AAB2A1"),
            ellipse(760, 288, 251, 112, "#8F9C83"),
            polygon([[1100, 405], [1263, 399], [1246, 486], [1123, 490]], "#969F8C"),
            ellipse(1037, 277, 286, 117, "#C0C8B6"),
            polygon([[1400, 412], [1569, 404], [1546, 487], [1419, 490]], "#A7AF9D"),
            ellipse(1330, 305, 270, 93, "#B7C0AC"),
            polygon([[1270, 369], [1356, 369], [1431, 402], [1420, 434], [1350, 419], [1290, 398]], "#C2C6B7"),
        ], [
            region(5, 64, 43, 810, 63, 46, face=4),
            region(1, 64, 112, 850, 65, 50, serif=True),
            region(2, 64, 189, 330, 49, 34),
            region(3, 448, 185, 530, 52, 38),
            region(6, 1060, 43, 476, 60, 44),
            region(7, 1060, 112, 476, 55, 40),
            region(8, 1060, 181, 476, 55, 40),
            region(4, 64, 555, 1472, 126, 40, lines=BODY2, leading=62),
            region(9, 64, 752, 650, 55, 40),
            region(10, 830, 752, 706, 55, 40),
            region(11, 64, 814, 750, 52, 38),
            region(12, 830, 814, 706, 50, 36),
        ]),
    },
    {
        "role": "R21-C1-M3", "ratio": "16:9",
        "working_name_not_printed": "An opening inside plants with different growth silhouettes",
        "whole_relationship": "Substantial planted silhouettes at both sides create an irregular central passage; one continuous central market/identity/schedule-to-prose-to-care route sits inside that active plant organization, with five-line serif prose rather than a broad side paragraph.",
        "positive_direction": """Build an energetic cut-paper plant passage as a market display of different living silhouettes. A low broad-leaf plant enters from the left foreground and a tall narrow-bladed plant grows from a clearly attached right pot. A third shorter leafy pot intrudes into the ragged right side of the prose opening, at a visibly different planted height, making the selection range tangible. Make pots, stems and leaf attachment explicit, and let actual large curved and angular plant masses organize the landscape across its full height. They create an irregular wide central opening, with image masses interlocking its useful copy footprints rather than forming a symmetric wreath or small leaf border around a card. Clean cuts, selected overlaps and substantial opaque shapes are the image grammar.

The market name leads at the upper entrance of the passage. The nearby Korean title and smaller Latin companion identify the event as the same reading encounter; the slogan and local date/hours/venue continue immediately. Make the market name's weight strongest in this cluster without making every line a competing headline. The title can be modest. Give the explanation a five-line continuous serif paragraph on the central shared left edge: generous Korean inner spaces, sturdy controlled thin strokes, restrained terminals and stable syllable proportions. Its deliberate word groups preserve the actual sentence and sit at a full readable body, with even baselines and ordinary leading. Numeric and Latin forms match optical body weight.

At its last line, the access start follows directly on that same axis. Care, invitation and URL remain nearby successive lines, allowing the useful action to emerge without traversing the plant edges again. Use warm mineral coral, deep blue-green, pale citron and a small plum accent through the active shapes; keep type flat and clear on the open contrasting passage. This individual central-column choice is derived from the plants' different growth silhouettes; it is not a default information panel or a five-poster common scaffold.""",
        "hierarchy": {
            "primary": {"entry": 5, "role": "Market name at the passage entrance, strongest local weight."},
            "support": [{"entry": 1, "role": "Modest Korean identity in the same close entry."},
                        {"entry": 2, "role": "Smaller companion immediately adjoining it."},
                        {"entry": 3, "role": "Promise continues locally."}],
            "visit": {"entries": [6, 7, 8], "shape": "Date/hours one row, venue following, all before the prose on the same local route."},
            "explanation": {"entries": [4], "shape": "Five-line central serif paragraph with a stable shared left edge."},
            "next_action": {"entries": [9, 10, 11, 12], "shape": "Direct continuous descent after paragraph, access/care then invitation/URL."},
        },
        "body_line_groups": BODY5,
        "body_end_to_next_info": "A short vertical continuation on the paragraph's left edge introduces access; care and invitation/URL remain inside the same route. Schedule has already been read locally above. Plant edges organize the passage but do not divide or underline copy.",
        "nearest_peer": {
            "role_id": "R21-C1-M5",
            "structural_distinction": "M3 uses one central connected reading route inside surrounding planted silhouettes. M5 places purpose and schedule on the left, substantive overhead plant masses through the middle/lower left, and prose-to-care on the right; its two copy footprints are connected across the image's actual pot-rim rhythm.",
            "style_distinction": "M3 uses clean abrupt paper-cut silhouette boundaries; M5 uses expressive gouache masses and top-down pottery/light shapes.",
        },
        "guide_geometry_concept": concept([
            {"bounds": [0, 40, 365, 810], "content": "Broad-leaf left plant, attached low pot and mid-height secondary stems; substantive full-height plant structure."},
            {"bounds": [1335, 80, 265, 770], "content": "Tall narrow-blade right plant and attached pot, a contrasting living silhouette opening the passage."},
            {"bounds": [1132, 362, 180, 296], "content": "Shorter leafy pot enters the prose opening's ragged unused right edge; actual planted scale interlocks the copy footprint rather than being a decorative outer border."},
        ], [
            polygon([[45, 610], [325, 610], [280, 842], [88, 842]], "#A3AB98"),
            polygon([[168, 615], [128, 262], [155, 238], [195, 615]], "#8E997F"),
            ellipse(0, 246, 225, 259, "#BCC5AD"),
            ellipse(111, 61, 254, 280, "#A6B293"),
            ellipse(39, 484, 278, 116, "#B3BDA4"),
            polygon([[1380, 593], [1569, 593], [1543, 844], [1410, 844]], "#A6AE9B"),
            polygon([[1430, 603], [1335, 224], [1370, 156], [1455, 601]], "#919D82"),
            polygon([[1468, 602], [1470, 82], [1504, 134], [1496, 602]], "#ADB99B"),
            polygon([[1500, 602], [1598, 269], [1575, 205], [1520, 602]], "#BBC4AE"),
            polygon([[1140, 450], [1298, 450], [1275, 658], [1163, 658]], "#AFB79F"),
            polygon([[1205, 453], [1198, 386], [1211, 386], [1218, 452]], "#8E9B7D"),
            ellipse(1132, 362, 180, 82, "#C0C8B0"),
        ], [
            region(5, 435, 36, 830, 60, 44, face=4),
            region(1, 435, 103, 830, 62, 48),
            region(2, 435, 171, 830, 45, 32),
            region(3, 435, 220, 830, 49, 36),
            region(6, 435, 276, 360, 49, 36),
            region(7, 865, 276, 400, 49, 36),
            region(8, 435, 330, 830, 49, 36),
            region(4, 435, 392, 830, 244, 38, serif=True, lines=BODY5, leading=48),
            region(9, 435, 650, 830, 49, 36),
            region(10, 435, 703, 830, 49, 36),
            region(11, 435, 756, 830, 49, 36),
            region(12, 435, 814, 830, 47, 34),
        ]),
    },
    {
        "role": "R21-C1-M4", "ratio": "16:9",
        "working_name_not_printed": "The planted contact of a repotting demonstration",
        "whole_relationship": "Two substantial monochrome contact crops enclose a central five-line prose opening; purpose and schedule are already connected in the upper encounter, so the paragraph descends directly into two neighboring access/care and invitation/URL rows rather than returning to a remote date.",
        "positive_direction": """Edit two close photographic views of actual repotting contact, making the market's demonstration promise tangible. In the tall left crop, a grower's hand supports a planted rootball from beneath over an ordinary unlettered cloth: fingers, soil and attached stems have distinct ownership. In the right crop, a second observed contact shows a hand steadying an ordinary pot rim beside planted soil. Treat these as related close views of work, not a claimed identical-plant transformation or a chronological tutorial. Their unequal heights and decisive inner crop boundaries enclose the central prose opening; the lower cloth/soil field extends across the bottom and joins the observed work. Use restrained monochrome olive-gray tonal separation, clear contact, believable support and specific ordinary surfaces.

The upper-left Korean title and compact Latin companion belong to the nearby upper market identifier and schedule. Their shared baselines and close row rhythm make the first encounter a plant-market purpose and visiting decision. Let the market name carry confident weight while the serif title remains controlled. Date and hours share a row, with venue immediately following; they do not wait in a corner after the explanation. At the central opening, the slogan leads into five full meaning lines of precise medium-weight Korean sans: generous counters, stable syllable proportions, normal word spaces, matched Latin/numerals and even baselines. Reserve its real area before editing the contact pictures.

The paragraph's final line leads directly below to access on the same start; care shares that row. Invitation and URL continue in the next local row. There is no upper-right-to-lower-left return to find the schedule. The close hand/rootball and hand/pot crops organize the paragraph's boundaries and the lower joined work field grounds its action rows. Keep all type upright and flat, away from photographic folds or glyph-like small marks. The contact edit and central explanatory/action footprint distinguish this whole from the nursery comparison and the continuous central plant passage.""",
        "hierarchy": {
            "primary": {"entry": 5, "role": "Confident upper market identifier adjoining the Korean identity and schedule."},
            "support": [{"entry": 2, "role": "Close small Latin companion."},
                        {"entry": 1, "role": "Controlled upper-left Korean serif identity in the same purpose encounter."},
                        {"entry": 3, "role": "Promise immediately above prose."}],
            "explanation": {"entries": [4], "shape": "Central five-line prose opening between the unequal contact crops."},
            "visit": {"entries": [6, 7, 8], "shape": "Date/hours row and venue immediately below in the upper purpose encounter, before explanation."},
            "next_action": {"entries": [9, 10, 11, 12], "shape": "Two neighboring access/care and invitation/URL rows immediately below the central paragraph."},
        },
        "body_line_groups": BODY5,
        "body_end_to_next_info": "The final prose line has one short vertical continuation to access on its own left start; care shares that row. Invitation/URL directly follow. Date/hours/venue were already connected to the first purpose encounter, so no backward diagonal search is needed.",
        "nearest_peer": {
            "role_id": "R21-C1-M1",
            "structural_distinction": "M4 encloses five-line central prose between two contact crops, with schedule above and action rows below. M1's L-shaped nursery/detail edit places all prose/schedule/action in one broad right area. M4 does not mirror or reuse that actual copy footprint.",
            "style_distinction": "M4 is near monochrome, close overhead and action/contact focused; M1 is natural-color oblique nursery distance plus unequal botanical detail crops.",
        },
        "guide_geometry_concept": concept([
            {"bounds": [0, 245, 390, 575], "content": "Tall close crop of a supporting hand, planted rootball and attached foliage; clear ownership and observed work."},
            {"bounds": [1210, 245, 390, 370], "content": "Unequal close hand/pot-rim/soil contact crop enclosing the other edge of the central paragraph; no claimed identical-plant or chronological transformation."},
            {"bounds": [0, 825, 1600, 75], "content": "Broad joined cloth/soil work field grounds the contact edit below the readable action rows, not a decorative fine divider."},
        ], [
            rect(0, 245, 390, 575, "#D1D3CA"),
            ellipse(12, 270, 289, 210, "#A6B094"),
            ellipse(162, 340, 224, 268, "#B6BDA9"),
            polygon([[155, 506], [285, 530], [326, 668], [191, 713], [128, 627]], "#8F9887"),
            polygon([[0, 661], [125, 658], [206, 720], [270, 728], [239, 778], [112, 762], [0, 732]], "#A3A89E"),
            rect(1210, 245, 390, 370, "#CDCEC6"),
            ellipse(1245, 434, 314, 90, "#979F8D"),
            polygon([[1262, 482], [1545, 482], [1514, 604], [1295, 604]], "#A6AD9B"),
            polygon([[1354, 245], [1410, 245], [1386, 380], [1365, 428], [1322, 428], [1325, 376]], "#A8AC9F"),
            polygon([[0, 845], [399, 827], [1010, 855], [1600, 825], [1600, 900], [0, 900]], "#BBBFB4"),
        ], [
            region(1, 64, 43, 470, 75, 54, serif=True),
            region(2, 64, 126, 470, 49, 34),
            region(5, 610, 43, 926, 63, 46, face=4),
            region(6, 610, 120, 360, 58, 42),
            region(7, 1040, 120, 496, 55, 40),
            region(8, 610, 184, 926, 55, 40),
            region(3, 465, 315, 690, 52, 38),
            region(4, 465, 379, 690, 279, 40, lines=BODY5, leading=54),
            region(9, 465, 681, 430, 55, 40),
            region(10, 1000, 681, 536, 55, 40),
            region(11, 465, 751, 570, 52, 38),
            region(12, 1090, 751, 446, 50, 36),
        ]),
    },
    {
        "role": "R21-C1-M5", "ratio": "16:9",
        "working_name_not_printed": "Looking down into a gathering of living pots",
        "whole_relationship": "An overhead gouache gathering of pots and canopy masses fills the middle and lower-left; left identity/schedule opens across that actual pot-rim rhythm into a right five-line explanation and its directly continuing care/action.",
        "positive_direction": """Paint a gathering of houseplants seen close from above, where the pleasure is looking into different living canopies and pottery. Place one leafy plant high in the middle, a more open branching plant below it, and a broad lower-left canopy whose actual pot rim and center attachment remain legible. Their pot circles and asymmetric leaf masses overlap at different scales without repeating a stamp grid. Let window light skim the rims and cast attached oblique shadows across the grouped plants; keep the spatial support consistent. Build expressive gouache masses, selective dry edges and precise planted centers, not a single heroic tree on the right.

The left upper identity immediately pairs the Korean title with the market name and small Latin companion. Its date, hours and venue continue down that same left route. Keep the identifier forceful enough to tell the purpose immediately without turning every line into a headline. Across the central pot rhythm, the right slogan begins the explanatory paragraph. Use five full meaning lines in mature medium-weight Korean sans, open counters, stable syllable proportions, clean proportional Latin and consistent lining numerals. Give the paragraph a genuine readable body and normal leading within its own uninterrupted area. The close plant canopy and rim spacing join these two useful reading starts rather than being unrelated decor between information islands.

The last paragraph line descends directly to access and care on the same right axis. Invitation and URL follow there without a second corner search. The practical information thus has two different functional homes: identifying/visiting first on the left, understanding/care/actions next on the right. Use deep plum, sap green, soft ochre and controlled creamy light in the painted plant masses; retain clean planar type. Bold painted botanical geometry fills the middle and expands into the lower left where the schedule ends, creating a major whole-image difference from an upper-left paragraph with a large right tree and lower information.""",
        "hierarchy": {
            "primary": {"entry": 1, "role": "Upper-left Korean identity, immediately paired with the market name."},
            "support": [{"entry": 5, "role": "Adjacent event identifier connects identity to visiting."},
                        {"entry": 2, "role": "Close small Latin companion."},
                        {"entry": 3, "role": "Right prose entry reached across the actual central pot rhythm."}],
            "visit": {"entries": [6, 7, 8], "shape": "One left local schedule column immediately under the identity."},
            "explanation": {"entries": [4], "shape": "Five-line right paragraph; its actual footprint differs from the broad side prose of M1/M4."},
            "next_action": {"entries": [9, 10, 11, 12], "shape": "Direct right continuation under paragraph: access/care then invitation/URL."},
        },
        "body_line_groups": BODY5,
        "body_end_to_next_info": "The last prose line leads directly down the right shared start to access/care; invitation/URL continue immediately there. Identity and schedule were already connected in the first left encounter, and the image's actual pot rims link that start to the right promise/prose.",
        "nearest_peer": {
            "role_id": "R21-C1-M3",
            "structural_distinction": "M5 has a left purpose/schedule column and a right promise/prose/care column separated and connected by overhead plant masses that expand into the lower left. M3 has one central continuous purpose-to-prose-to-care route inside side plant silhouettes.",
            "style_distinction": "M5 is expressive gouache seen from above, with pot-rim light and asymmetric canopy masses. M3 is clean flat cut-paper growth silhouette construction with upright attached pots.",
        },
        "guide_geometry_concept": concept([
            {"bounds": [560, 40, 410, 535], "content": "Close overhead pots and attached canopy centers, unequal masses and rim rhythm link the two useful reading starts."},
            {"bounds": [0, 590, 935, 310], "content": "Broad lower-left overhead canopy expands where the schedule ends, connected to the middle plant gathering; not a separate image strip."},
        ], [
            ellipse(573, 48, 317, 235, "#ABB49E"),
            ellipse(663, 77, 91, 75, "#7F8D75"),
            ellipse(700, 257, 256, 282, "#B8BEAD"),
            ellipse(767, 337, 86, 86, "#8C997F"),
            polygon([[690, 178], [573, 294], [591, 424], [666, 493], [724, 489], [675, 366], [723, 267]], "#A0AD92"),
            polygon([[930, 234], [967, 269], [967, 524], [908, 575], [875, 539], [938, 399]], "#BCC3B0"),
            ellipse(0, 592, 610, 303, "#BBC4AE"),
            ellipse(294, 590, 420, 310, "#A6B395"),
            ellipse(628, 638, 308, 262, "#C7CCBE"),
            ellipse(425, 700, 132, 119, "#829475"),
            polygon([[670, 522], [743, 520], [722, 645], [653, 657]], "#9EAA91"),
        ], [
            region(1, 64, 47, 420, 75, 54, serif=True),
            region(5, 64, 130, 420, 61, 44, face=4),
            region(2, 64, 198, 420, 49, 34),
            region(6, 64, 309, 420, 58, 42),
            region(7, 64, 378, 420, 55, 40),
            region(8, 64, 447, 420, 55, 40),
            region(3, 1040, 49, 510, 52, 38),
            region(4, 1040, 125, 510, 312, 42, lines=BODY5, leading=60),
            region(9, 1040, 493, 510, 55, 40),
            region(10, 1040, 561, 510, 55, 40),
            region(11, 1040, 629, 510, 52, 38),
            region(12, 1040, 697, 510, 50, 36),
        ]),
    },
]

measurements = []
for direction in directions:
    assert " ".join(direction["body_line_groups"]) == copy[3]["text"]
    regions = direction["guide_geometry_concept"]["text_regions"]
    assert sorted(block["entry"] for block in regions) == list(range(1, 13))
    for block in regions:
        assert " ".join(block["lines"]) == block["copy"]
        font = ImageFont.truetype(block["font"]["path"], block["font"]["size"],
                                  index=block["font"]["index"])
        advances = [font.getlength(line) for line in block["lines"]]
        ascent, descent = font.getmetrics()
        assert max(advances) <= block["area"]["width"], (
            direction["role"], block["entry"], advances, block["area"])
        painted = []
        for ordinal, line in enumerate(block["lines"]):
            bounds = font.getbbox(line, anchor="ls")
            baseline = block["y"] + ascent + ordinal * block["line_spacing"]
            placed = [block["x"] + bounds[0], baseline + bounds[1],
                      block["x"] + bounds[2], baseline + bounds[3]]
            assert 0 <= placed[0] <= placed[2] <= 1600
            assert 0 <= placed[1] <= placed[3] <= 900
            painted.append(placed)
        measurements.append({
            "role": direction["role"], "entry": block["entry"],
            "font_family_style": font.getname(),
            "line_advances": advances, "painted_bounds": painted,
            "planned_area": block["area"],
            "measurement_only": "No bitmap, SVG or PNG rendered.",
        })
    direction["guide_spec"] = {
        "canvas": deepcopy(direction["guide_geometry_concept"]["canvas"]),
        "shapes": deepcopy(direction["guide_geometry_concept"]["shapes"]),
        "text_blocks": [{key: deepcopy(value) for key, value in block.items()
                         if key != "entry"} for block in regions],
    }

roles = deepcopy(source["roles"])
for ordinal, role in enumerate(roles, start=1):
    role["role_id"] = f"R21-C1-M{ordinal}"
plan = {
    "schema_version": 1, "case_id": "R21-C1",
    "status": "ONE prospective matched-development five-direction plan for candidate X; candidate audit/adoption and later root guide review remain separate. No guide rendered or native call initiated.",
    "request": source["request"], "copy": copy,
    "conditions": deepcopy(source["conditions"]),
    "assets": deepcopy(source["assets"]),
    "count": source["count"], "ratios": deepcopy(source["ratios"]),
    "styles": deepcopy(source["styles"]), "roles": roles,
    "common_constraints": deepcopy(source["conditions"]) + [
        "1600x900 is the authored neutral guide canvas, not a new client preservation or final pixel condition. Usage720 remains the same internal reading assumption.",
        "All guide inputs are new own code/text/shapes. No prior poster, source artwork, bitmap input or manual final typography composition is used.",
        "The installed Mac font paths/faces are explicit current-case planning choices. Native generation is not certified to apply those font bytes.",
        "No character clipart, clay/toy package, passive black/gray information field, repeated big-object/title/tiny-footer scaffold or generic invitation separated from event purpose.",
        "Every first encounter locally links identity or market to the supplied promise and useful visit participation. No fabricated new heading, bullet, pipe, arrow, label or plant tag.",
        "Keep original en dashes, middle dots, ampersand, punctuation and spaces. Give dates, times and URL clear consistent numeral/Latin forms.",
        "Substantive image geometry and full actual copy were authored together; material names or alternate first words do not establish whole-system diversity.",
        "No new source-reading obligation, font installation, fixed five-style runtime menu, quality gate or expected score. Final posters require actual image observation later.",
    ],
    "directions": directions,
    "design_provenance": {
        "source_request": str(SOURCE.relative_to(ROOT)),
        "source_case_id": source["case_id"],
        "instruction_basis": ["drafts/candidate-x/references/production-brief.md",
                              "drafts/candidate-x/references/parallel-production.md",
                              "drafts/candidate-x/references/design-grammar.md"],
        "schema_example_only": "drafts/w-five-design/prepare_plan.py and plan.json",
        "source_use": "Reused accumulated grammar ideas without reopening source artwork or web.",
        "not_opened": ["prior poster pixels", "critic score/review files", "source raster", "raw evaluation transcripts"],
        "execution": {"native_calls": 0, "guides_rendered": 0, "child_agents": 0},
        "font_measurement_only": "Known installed font metrics read via Pillow; no font binaries copied, no raster read or rendered. Measurements only aid actual copy/shape authoring and do not prove final readability or poster quality.",
        "measurements": measurements,
        "case_conservation": "Request, twelve copy entries, conditions, assets[], count5, ratios and role attempt/correction limits copied exactly; only prospective case/role identity changes.",
        "development_limit": "Matched prospective development after the parent-closed R20. Not a held-out independent test, quality replay or isolated causal result.",
    },
}
assert plan["request"] == source["request"] and plan["copy"] == source["copy"]
assert plan["conditions"] == source["conditions"] and plan["assets"] == source["assets"]
assert plan["count"] == 5 and plan["ratios"] == ["16:9"] * 5

rationale = """# X 한 요청의 전향적 다섯 전체 계획

R20의 실제 식물 마켓 요청·12개 카피·조건·assets[]·수량·비율을 유지한 R21-C1 설계다. 원기록·스킬·라운드 폴더를 바꾸지 않았으며 기존 결과의 개별 보정 계획도 아니다. X의 현재 제작 명세·병렬 제작·구성 문법을 읽고 축적한 아이디어를 현재 내용과 실제 글자 면적에 맞게 새로 조직했다. 웹·원작 이미지·기존 포스터 픽셀·평가 파일은 열지 않았다.

| 역할 | 주요 이미지 덩어리와 실제 카피 면적 | 읽는 연결 |
| --- | --- | --- |
| M1 | 왼쪽 전체 높이의 가까운 식물 시장 사진 + 오른쪽 상단 불균등 세부 편집; 오른쪽 넓은 실제 읽기 면적 | 같은 진입에서 제목·행사 식별 → 설명 → 날짜/시간 → 장소/입장 → 관리 → 초대/URL |
| M2 | 가로로 높이가 오르내리는 식물 시장의 중간 장면; 위쪽 식별·일정, 아래쪽 거의 전체 폭의 두 줄 설명과 두 행동 행 | 가까운 상단 행사·이름·약속과 일정 → 실질적인 식물 장면 → 두 줄 설명 → 같은 시작점의 입장/관리 → 초대/URL |
| M3 | 두 쪽의 큰 식물 실루엣이 여는 비대칭 중앙 통로; 하나의 연속 중앙 읽기 열 | 행사·이름·약속·일정 → 다섯 줄 명조 본문 → 바로 아래 입장·관리·초대·URL |
| M4 | 불균등한 두 분갈이 접촉 크롭이 중앙 다섯 줄 본문을 둘러쌈; 상단 목적·일정을 먼저 만나고 본문 아래 두 행동 행으로 이어짐 | 가까운 제목·행사·일정 → 중앙 약속·본문 → 같은 시작점의 입장/관리 → 초대/URL |
| M5 | 위에서 보는 식물·화분 군집이 중앙과 아래왼쪽을 실질적으로 채움; 왼쪽 식별·일정과 오른쪽 본문·관리 | 제목·행사와 왼쪽 일정 → 실제 화분 가장자리의 리듬을 건너 약속·다섯 줄 본문 → 같은 축의 입장/관리·초대·URL |

M1/M4의 가까운 사진 관계도 실제 발판이 다르다. M1은 L자 사진 편집과 오른쪽 연속 읽기 면적이며, M4는 두 접촉 크롭이 여는 중앙 다섯 줄 본문과 그 아래 행동 행이다. M4는 먼저 만난 상단 일정으로 되돌아가거나 먼 좌하단 날짜를 찾아야 하는 전환을 제거했다. M2는 오른쪽 큰 나무에 위왼쪽 본문·하단 안내를 붙이지 않는다. 실질적인 식물 시장 이미지가 가운데 가로 지평선을 만들고 거의 전체 폭의 실제 두 줄 본문과 행동 행이 그 아래에서 이어진다. M5는 중앙·아래왼쪽의 위에서 본 군집을 사이에 둔 왼쪽 목적·일정과 오른쪽 이해·관리다. M3과 M5는 식물 군집을 쓰더라도 하나의 중앙 열과 서로 다른 두 기능 열이라는 카피 점유 면적·순서가 다르다. M3의 더 작은 화분은 본문의 실제 오른쪽 자투리 공간 안으로 들어오며 문자와 안전한 거리를 유지해 단순 외곽 테두리의 관계를 줄였다.

각 방향의 첫 만남에서 실제 이름 또는 행사와 약속·참여가 가까이 연결되게 했다. 일반 초대나 장문을 크게 만들고 이름을 먼 구석에 떨어뜨리는 방식은 사용하지 않았다. 12개 항목은 각 명세에 정확히 한 번 배정했고 본문을 의미가 이어지는 실제 2줄·3줄·5줄로 나눴다. 줄바꿈·몸체·이미지 경계를 함께 정하고, 각 문단 끝에서 다음 실제 안내를 찾는 가까운 시작점·공유 축을 구체화했다.

1600×900 가이드 스펙에는 설치된 AppleSDGothicNeo TTC의 Medium/Semibold와 AppleMyungjo0, 실제 copy/lines, text_blocks와 새 shapes가 들어 있다. 큰 식물·화분·작업 접촉 형태를 중립적인 덩어리로 표시하며 가이드 선·물체를 본문 안이나 글자 바로 옆에 붙이지 않았다. 이는 자신의 계획 입력이며 최종 포스터·원작 이미지·고객 제공 자산이 아니다. 향후 실제 글꼴이 가이드에 쓰여도 최종 네이티브 이미지에 그 파일이 적용됐다고 주장할 수 없다.

확인한 것은 원문·조건 보존, 12개 실제 문구의 한 번 배정과 줄 재결합, 설치 글꼴의 실제 줄 폭과 캔버스 안 활자 범위다. 글꼴 메트릭만 읽었고 가이드 SVG/PNG·이미지 생성·이미지 편집·점수·새 에이전트를 실행하지 않았다. 이 계획은 현재 내용을 위한 다섯 authored 선택이며 영구 스타일 메뉴나 새 픽셀 규칙·평가 문턱이 아니다. 실제 다섯 가이드의 전체 관계를 부모가 본 뒤 한 요청만 동결·생성할 수 있다. 계획만으로 하이엔드 품질이나 최종 다양성을 선언하지 않는다.
"""

OUT.mkdir(parents=True, exist_ok=True)
for name, value in [
    ("plan.json", json.dumps(plan, ensure_ascii=False, indent=2) + "\n"),
    ("rationale.md", rationale),
]:
    with (OUT / name).open("x", encoding="utf-8") as stream:
        stream.write(value)
print(json.dumps({
    "directions": len(directions), "actual_copy_regions": len(measurements),
    "request_copy_conditions": "exact", "body_reconstruction": "exact",
    "guides_rendered": 0, "native_calls": 0,
    "outputs": ["plan.json", "rationale.md"],
}, ensure_ascii=False))
