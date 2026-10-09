"""Preserve original X plan; author a new Title-hierarchy revision, metrics only."""
from copy import deepcopy
from pathlib import Path
import json
from PIL import ImageFont

ROOT = Path("/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster")
OUT = ROOT / "drafts/x-five-design"
SOURCE = ROOT / "work/round20/planning/single-five-case.json"
source = json.loads(SOURCE.read_text(encoding="utf-8"))["cases"][0]
original = json.loads((OUT / "plan.json").read_text(encoding="utf-8"))
plan = deepcopy(original)
copy = source["copy"]
SANS = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
SERIF = "/System/Library/Fonts/Supplemental/AppleMyungjo.ttf"
TITLE2 = ["집 안의", "작은 숲"]
BODY2 = original["directions"][1]["body_line_groups"]
BODY3 = original["directions"][0]["body_line_groups"]
BODY5 = original["directions"][2]["body_line_groups"]


def region(entry, x, y, width, height, size, *, face=2, serif=False,
           lines=None, leading=None):
    return {
        "entry": entry, "copy": copy[entry - 1]["text"],
        "lines": lines or [copy[entry - 1]["text"]],
        "fixed_newlines": copy[entry - 1]["fixed_newlines"],
        "x": x, "y": y, "align": "left",
        "line_spacing": leading or round(size * 1.35),
        "area": {"width": width, "height": height},
        "font": {"path": SERIF if serif else SANS,
                 "index": 0 if serif else face, "size": size},
        "color": "#202624",
    }


new_regions = [
    [
        region(5, 650, 208, 900, 44, 32, face=4),
        region(1, 650, 260, 900, 100, 78, serif=True),
        region(2, 650, 365, 900, 41, 28),
        region(3, 650, 416, 900, 50, 36, face=4),
        region(4, 650, 475, 900, 156, 38, lines=BODY3, leading=50),
        region(6, 650, 650, 430, 49, 36),
        region(7, 1120, 650, 430, 49, 36),
        region(8, 650, 708, 330, 47, 34),
        region(9, 1030, 708, 520, 47, 34),
        region(10, 650, 766, 900, 47, 34),
        region(11, 650, 824, 470, 47, 34),
        region(12, 1170, 824, 380, 44, 32),
    ],
    [
        region(5, 64, 39, 910, 44, 32, face=4),
        region(1, 64, 91, 910, 104, 80, face=4),
        region(2, 64, 211, 330, 42, 28),
        region(3, 448, 211, 530, 47, 34, face=4),
        region(4, 64, 555, 1472, 126, 40, lines=BODY2, leading=62),
        region(6, 1060, 78, 476, 53, 38),
        region(7, 1060, 140, 476, 50, 36),
        region(8, 1060, 199, 476, 50, 36),
        region(9, 64, 710, 650, 50, 36),
        region(10, 830, 710, 706, 50, 36),
        region(11, 64, 773, 750, 47, 34),
        region(12, 830, 773, 706, 44, 32),
    ],
    [
        region(5, 435, 28, 830, 44, 32, face=4),
        region(1, 435, 77, 830, 101, 76, serif=True),
        region(2, 435, 184, 830, 41, 28, serif=True),
        region(3, 435, 232, 830, 47, 34, face=4),
        region(4, 435, 291, 830, 244, 38, serif=True, lines=BODY5, leading=48),
        region(6, 435, 554, 310, 47, 34),
        region(7, 775, 554, 490, 47, 34),
        region(8, 435, 610, 300, 47, 34),
        region(9, 775, 610, 490, 47, 34),
        region(10, 435, 666, 830, 47, 34),
        region(11, 435, 724, 830, 47, 34),
        region(12, 435, 782, 830, 44, 32),
    ],
    [
        region(5, 64, 36, 1000, 44, 32, face=4),
        region(1, 64, 87, 1000, 108, 82, face=4),
        region(2, 64, 201, 1000, 44, 30),
        region(3, 465, 309, 690, 50, 36, face=4),
        region(4, 465, 369, 690, 270, 38, lines=BODY5, leading=52),
        region(6, 465, 656, 430, 47, 34),
        region(7, 1060, 656, 476, 47, 34),
        region(8, 465, 714, 430, 47, 34),
        region(9, 1050, 714, 486, 47, 34),
        region(10, 465, 772, 1071, 47, 34),
        region(11, 465, 828, 540, 46, 33),
        region(12, 1090, 828, 446, 44, 32),
    ],
    [
        region(5, 64, 35, 420, 44, 32, face=4),
        region(1, 64, 90, 420, 195, 82, serif=True, lines=TITLE2, leading=90),
        region(2, 64, 298, 420, 41, 28),
        region(3, 1040, 127, 510, 47, 34, face=4),
        region(4, 1040, 193, 510, 286, 38, lines=BODY5, leading=56),
        region(6, 1040, 520, 510, 47, 34),
        region(7, 1040, 573, 510, 47, 34),
        region(8, 1040, 626, 510, 47, 34),
        region(9, 1040, 679, 510, 47, 34),
        region(10, 1040, 732, 510, 47, 34),
        region(11, 1040, 785, 510, 47, 34),
        region(12, 1040, 840, 510, 44, 32),
    ],
]

positive_directions = [
    """Keep the whole photographic L-shaped nursery encounter and upper unequal detail edit. In the full-height left view, close planted pots, a farther established plant and the grower's cropped supporting hand make choosing a living plant a market encounter rather than an empty room decoration. Leaf attachment, soil and pot-rim details across the upper right determine the start of its reading area.

The actual Korean Title is the dominant verbal anchor directly below the crop: a generous mature serif body, open inner counters and controlled contrast, substantially larger than prose, Latin, dates and invitation. The market name is its smaller eyebrow immediately above; Latin is a quiet companion immediately below. The subtitle promise then enters a broad three-line explanation. Pair the serif Title with one consistent medium-weight Korean sans reading system: stable squared syllables, open counters, proportionate Latin/numerals and ordinary leading. Semibold is reserved for eyebrow/subtitle; practical lines remain regular medium.

The paragraph descends directly into date/hours, venue/access, care and invitation/URL rows on the same right optical axis. Preserve meaningful word spaces and distinct range dashes. Cool natural greens, pottery and daylight carry the image; type stays precise and planar. Title prominence and this photographic edit are authored together, with the picture remaining substantive.""",
    """Retain the full-width market plant horizon, where distinct small pots, upright blades and branching established plants rise and fall across the actual table. One close supporting hand and planted soil detail express selection and care without a mascot or invented plant label. Printed color planes and observed contour density, not texture garnish, organize the major picture.

Give the actual Korean Title a clearly dominant 80-pixel planning body in the same mature sans family used throughout. The smaller market eyebrow sits immediately above, Latin and the promise subtitle immediately below. Date/hours/venue form a nearby upper schedule cluster with plainly lower size and weight; the Title remains recognizable before any date. Use medium for prose and useful information, semibold for Title and subtitle, consistent glyph width, stable baselines and harmonious Korean/Latin/numeral optical size.

The substantive plant horizon leads down to the actual two-line wide paragraph. Its first sentence introduces the range, its second links the grower's story to choosing for home. Access/care and invitation/URL follow directly on that paragraph's left start in two generous rows. Keep these substantial readable elements rather than a tiny footer. Strong coral and ochre details, olive plant structure and crisp type make a deliberate graphic market poster, with no large right tree and upper-left prose scaffold.""",
    """Keep the irregular planted passage as a display of different living silhouettes. Large broad leaves enter from the left, tall attached blades from the right, and a shorter leafy pot enters the actual ragged edge beside the prose. Those substantial forms interlock copy footprints; they are not a decorative border around a passive information panel.

The actual Korean Title is now the immediately recognizable primary anchor at the passage entrance. Set it as a generous mature serif, substantially larger than every supporting element. Pair the same serif anatomy with the five-line body: sturdy thin strokes, open counters, stable Korean proportions and normal meaning-preserving line groups. The smaller market eyebrow is directly above; the restrained serif Latin companion is directly below. A compatible clear sans supplies subtitle and practical information, with consistent width and baselines and deliberate medium/semibold roles.

Read Title to promise subtitle to full body. The body then descends directly into date/hours, venue/access, care and invitation/URL on the same central start, with a short local gap at each functional turn. Original range dashes and middle dots remain distinct. Mineral coral, blue-green and citron belong to the active cut shapes while copy remains clean. The Title has clear hierarchy inside a content-derived plant passage; different whole organization carries the variation.""",
    """Keep two unequal close contact photographs: a tall planted rootball supported by a readable hand at the left, and a hand steadying a real pot rim beside soil at the right. These related repotting views make the market's demonstration offer concrete without claiming an identical-plant transformation or a chronological tutorial. Their inner crop boundaries enclose central prose.

The actual Korean Title is a dominant upper verbal anchor in a generous semibold mature sans; the smaller market eyebrow precedes it and its compact Latin companion follows. That same family supplies the subtitle, prose and useful information, with moderate medium strokes, open counters, harmonious Latin/numeral size and stable baselines. The Title is clearly stronger than the full five-line paragraph and any date; subtitle emphasis is controlled rather than another competing headline.

The subtitle leads into the central full paragraph. Directly below its end, date/hours introduce participation; venue/access share the next row, care follows, then invitation/URL. Every transition uses the existing central start or adjacent local row, so the viewer does not return to a remote schedule. Keep photographs monochrome with restrained olive-gray separation and observed contacts, while all type remains crisp and planar. The contact edit, central body and paired useful rows sustain a whole relationship distinct from the L-shaped nursery poster.""",
    """Keep an overhead painted gathering of actual planted pots: a leafy center high in the middle, an open branching canopy below it and a broad lower-left plant whose rim and attachment remain clear. Their unequal pot circles and asymmetric leaf masses overlap at different living scales; attached shadows and selected window light give the market gathering coherent support. Gouache masses and controlled dry edges carry the image, not a single giant right tree.

The actual Korean Title is now a generous two-line primary anchor at the left, using the meaningful groups ‘집 안의 / 작은 숲’. A smaller market eyebrow immediately precedes it; Latin directly follows. The large serif's open inner spaces and controlled stroke contrast remain harmonious with one consistent sans reading system. Across the actual pot-rim rhythm, the clearly secondary subtitle begins the right five-line explanation. The Title has much greater body and optical weight than that paragraph, Latin, date and invitation.

The explanation then descends directly on the same right start through date/hours/venue, access/care and invitation/URL. The schedule has moved from the former left block into this continuing useful route, preventing a long return after prose. Planted masses expand below the large Title into the lower left, balancing its authored footprint. Deep plum, sap green, soft ochre and creamy light keep the painted whole specific; typography stays precise and flat.""",
]

whole_relationships = [
    "A full-height left nursery encounter and upper-right detail edit create an L-shaped image; the dominant right Title leads a broad three-line paragraph and locally paired practical rows inside that picture-defined reading entrance.",
    "A dominant upper-left Title and nearby lower-weight schedule identify the market above a substantive full-width botanical horizon; below it, a two-line wide paragraph descends into two generous action rows.",
    "Substantial interlocking planted silhouettes create a central passage whose dominant serif Title, five-line serif prose and locally paired practical rows form one connected reading route.",
    "Two unequal close repotting contact crops enclose central five-line prose; a dominant upper Title introduces the purpose, then body leads directly into paired local practical rows.",
    "A dominant two-line left Title occupies the space above the overhead plant gathering; across actual pot-rim rhythm, right subtitle/five-line prose descends continuously into schedule and actions.",
]

body_handoffs = [
    "Title/subtitle and the three-line paragraph share the right start. A short gap then begins date/hours, venue/access, care, and invitation/URL in locally paired successive rows.",
    "The dominant Title's promise connects through the market horizon to the wide two-line paragraph. Its final line leads directly down to access/care, then invitation/URL. The lower-weight nearby upper schedule is available in that same first market encounter.",
    "Title, subtitle and five-line paragraph share one central start; the final prose line leads directly to date/hours, venue/access, care, invitation and URL without revisiting another region.",
    "The five-line central paragraph descends directly into date/hours on its start, then venue/access, care and invitation/URL. No upper-right-to-lower-left schedule return remains.",
    "The right five-line paragraph ends directly above the date on its own start. Hours/venue, access/care and invitation/URL continue locally; the schedule is no longer a separate left destination.",
]

role_map = {
    "eyebrow": [5], "Title": [1], "English_companion": [2],
    "Subtitle": [3], "bodycopy": [4],
    "footer_visit": [6, 7, 8], "footer_participation": [9, 10],
    "footer_next_action": [11, 12],
}

measurements = []
for ordinal, direction in enumerate(plan["directions"]):
    regions = new_regions[ordinal]
    direction["positive_direction"] = positive_directions[ordinal]
    direction["whole_relationship"] = whole_relationships[ordinal]
    direction["body_end_to_next_info"] = body_handoffs[ordinal]
    direction["text_role_map"] = deepcopy(role_map)
    direction["hierarchy"] = {
        "primary": {"entry": 1, "role": "Immediate recognizable Korean Title; dominant typography with sufficient relative scale, weight, contrast and space."},
        "support": [
            {"entry": 5, "role": "Smaller market eyebrow locally identifying the Title's purpose."},
            {"entry": 2, "role": "Quieter English companion adjoining the Title."},
            {"entry": 3, "role": "Secondary promise subtitle leading into the full explanation."},
        ],
        "explanation": {"entries": [4], "shape": direction["body_line_groups"]},
        "visit": {"entries": [6, 7, 8], "shape": "Coherent local visit group at visibly lower hierarchy than Title."},
        "next_action": {"entries": [9, 10, 11, 12], "shape": "Access/care and invitation/URL remain functionally adjacent and readable."},
    }
    direction["font_system"] = {
        "families": ["Apple SD Gothic Neo"] if ordinal in (1, 3) else ["AppleMyungjo", "Apple SD Gothic Neo"],
        "relation": "One consistent sans system, or a deliberate mature serif Title/body with one consistent compatible sans reading system. No unrelated font mixing.",
        "anatomy": "Open Korean counters, stable syllable proportions, controlled stroke contrast, medium reading strokes, consistent baseline and language-specific optical scale.",
        "weights": "Semibold marks the dominant sans Title or the much smaller supporting eyebrow/subtitle; medium supplies prose and useful lines. Serif Title uses greater body and coherent contrast rather than extra competing fonts.",
        "limits": "Installed-font bytes describe the neutral guide only. Future native output must realize harmonious glyph anatomy; this is not font-file certification or a universal font menu.",
    }
    concept = direction["guide_geometry_concept"]
    concept["text_regions"] = regions
    if ordinal == 3:
        concept["shapes"] = concept["shapes"][:-1]
        concept["image_geometry_concepts"] = concept["image_geometry_concepts"][:2]
        concept["limits"].append("The former bottom work-field shape is omitted in this revision to reserve readable practical rows; close contact crop boundaries retain the major image organization.")
    assert sorted(block["entry"] for block in regions) == list(range(1, 13))
    for block in regions:
        assert " ".join(block["lines"]) == block["copy"]
        font = ImageFont.truetype(block["font"]["path"], block["font"]["size"],
                                 index=block["font"]["index"])
        advances = [font.getlength(line) for line in block["lines"]]
        assert max(advances) <= block["area"]["width"], (direction["role"], block["entry"], advances)
        ascent, _ = font.getmetrics()
        bounds = []
        for index, line in enumerate(block["lines"]):
            box = font.getbbox(line, anchor="ls")
            baseline = block["y"] + ascent + index * block["line_spacing"]
            painted = [block["x"] + box[0], baseline + box[1],
                       block["x"] + box[2], baseline + box[3]]
            assert 0 <= painted[0] <= painted[2] <= 1600
            assert 0 <= painted[1] <= painted[3] <= 900
            bounds.append(painted)
        measurements.append({
            "role": direction["role"], "entry": block["entry"],
            "font_family_style": font.getname(), "font_size": block["font"]["size"],
            "line_advances": advances, "painted_bounds": bounds,
            "planned_area": block["area"], "measurement_only": "No guide or bitmap rendered.",
        })
    direction["guide_spec"] = {
        "canvas": deepcopy(concept["canvas"]),
        "shapes": deepcopy(concept["shapes"]),
        "text_blocks": [{key: deepcopy(value) for key, value in block.items()
                         if key != "entry"} for block in regions],
    }

plan["directions"][0]["nearest_peer"]["structural_distinction"] = "M1 has an L-shaped nursery/detail image and dominant Title, prose and practical rows inside one broad right reading area. M4 encloses central five-line prose between two contact crops, with dominant Title above and paired practical rows below."
plan["directions"][2]["nearest_peer"]["structural_distinction"] = "M3 has one central Title-to-prose-to-practical passage inside interlocking plant silhouettes. M5 has a dominant two-line left Title above overhead plant masses, with five-line prose and practical information continuing on a right axis."
plan["directions"][3]["nearest_peer"]["structural_distinction"] = "M4's two contact crops enclose central five-line prose, upper dominant Title and lower paired practical rows. M1's L-shaped nursery/detail edit places Title, broad three-line prose and useful information in one right reading area."
plan["directions"][4]["nearest_peer"]["structural_distinction"] = "M5's large two-line left Title and central/lower-left overhead plant gathering lead to a right prose/practical route. M3's Title, serif prose and practical rows occupy one central passage inside upright planted silhouettes."
plan["status"] = "NEW hierarchy-v2 prospective five-direction plan following the latest human Title/typographic-role instruction; original plan and authoring script preserved. Native0, guide-render0."
plan["common_constraints"].append(
    "Latest human hierarchy instruction applies: actual Korean Title is immediately recognizable as the primary typographic anchor in all five; eyebrow, Latin companion, subtitle, bodycopy and practical/footer roles are explicit and harmonious. This current authoring choice does not make Title always the largest future runtime element irrespective of user instructions."
)
plan["design_provenance"]["parent_plan"] = "drafts/x-five-design/plan.json"
plan["design_provenance"]["revision_reason"] = "Latest human instruction requires immediate Title recognition and clear harmonious typography hierarchy; current draft choices of market/date-first or modest secondary Title were revised prospectively before any rendering/generation."
plan["design_provenance"]["measurements"] = measurements
plan["design_provenance"]["execution"] = {"native_calls": 0, "guides_rendered": 0, "child_agents": 0}
assert plan["request"] == source["request"] and plan["copy"] == source["copy"]
assert plan["conditions"] == source["conditions"] and plan["assets"] == source["assets"]
assert all(" ".join(d["body_line_groups"]) == copy[3]["text"] for d in plan["directions"])

rationale = """# X 다섯 계획의 Title 위계 수정본

최신 인간 지시가 실제 테스트 포스터에서 제목이 무엇인지 즉시 구분되도록 eyebrow·Title·Subtitle·bodycopy·footer의 위계와 폰트 조화를 명확히 요구했다. 원래 계획·rationale·prepare_plan.py는 보존하고, 이미지·가이드 생성 전에 이 새 전향적 수정본을 작성했다. 지침의 ‘항상 제목 최대 크기/첫 순서를 고정하지 않는다’는 일반 범위를 제목을 작게 두는 기본값으로 해석하지 않는다.

12개 실제 문구의 역할은 다음과 같다. 새 소제목이나 문구는 인쇄하지 않는다.

| 역할 | 원문 항목 |
| --- | --- |
| eyebrow | 성수 주말 식물 마켓 |
| Title | 집 안의 작은 숲 |
| English companion | LEAVES & LIVING |
| Subtitle | 초록을 고르고, 일상을 가꿉니다. |
| bodycopy | 작은 화분부터…식물을 골라보세요. 전체 확정 설명 |
| footer/visit | 날짜, 시간, 장소 |
| footer/participation | 입장 무료·분갈이 시연, 관리 안내 |
| footer/next action | 초대, URL |

모든 방향에서 Title은 가장 명백한 주된 타이포 앵커로 계획했다. 한 줄 제목은 76–82px, M5의 의미 단위 두 줄 제목은 82px이며 본문은 38–40px로 읽을 실제 면적을 유지했다. 이는 현재 1600×900 가이드의 authored 크기 관계이며 새 고객 픽셀 조건이나 영구적인 수치 규칙이 아니다. 영어·날짜·초대·긴 문단이 같은 헤드라인처럼 경쟁하지 않게 더 작은 몸체·무게·명도와 연결된 간격을 사용한다.

| 방향 | 유지한 전체 이미지·카피 관계 | 수정한 위계와 흐름 |
| --- | --- | --- |
| M1 | 왼쪽 가까운 시장 사진과 우상단 불균등 세부 편집의 L자 조직 | 오른쪽 crop 시작에서 eyebrow·큰 명조 Title·English를 묶고 Subtitle→3줄 본문→같은 축의 실용 행 |
| M2 | 실질적인 식물 시장의 가로 지평선과 거의 전체 폭의 2줄 본문 | 위왼쪽 큰 고딕 Title에 eyebrow/English/Subtitle을 붙이고 일정은 가까운 낮은 계층; 이미지 아래 본문→행동 행 |
| M3 | 비대칭 큰 식물 실루엣과 본문의 자투리 공간으로 들어오는 화분 | 중앙의 큰 명조 Title→Subtitle→5줄 명조 본문→날짜/시간·장소/입장·관리·초대/URL로 연속 |
| M4 | 불균등한 두 가까운 분갈이 접촉 크롭이 중앙 5줄 본문을 둘러싸는 조직 | 상단 큰 고딕 Title→중앙 Subtitle/본문→바로 아래 인접 실용 행; 먼 날짜를 되찾는 전환 없음 |
| M5 | 위에서 본 화분 군집이 중앙과 아래왼쪽을 실질적으로 채우는 조직 | 왼쪽 큰 두 줄 명조 Title와 그 eyebrow/English→오른쪽 Subtitle/본문→동일 오른쪽 축의 실용정보; 일정의 왼쪽 되찾기 제거 |

M2/M4는 한 sans 가족에서 Semibold와 Medium 역할을 일관되게 사용했다. M1/M5는 안정된 명조 제목과 한 가지 조화로운 sans 본문·안내를 의도적으로 짝지었다. M3는 명조 제목·본문과 그 골격·광학 크기에 조화되는 한 sans 안내 체계다. 한글 속공간·자소 비례·획 대비, 라틴과 숫자의 광학 크기·폭·기준선, 기능별 굵기와 줄 간격을 역할 전체에 일관되게 적용했다. 무관한 폰트들을 요소마다 바꾸지 않는다. 실제 가이드가 사용한 폰트 바이트를 최종 네이티브 포스터의 폰트 적용 인증으로 주장하지 않는다.

원문·12개 카피·조건·assets[]·5역할·16:9·호출/보정 상한을 그대로 유지했다. 각 guide_spec은 기존 helper용 canvas/shapes/text_blocks만 포함하며 실제 12문구가 정확히 한 번 들어 있다. 메트릭으로 줄 폭·활자 캔버스 범위만 확인했고 가이드 SVG/PNG·이미지 생성·이미지 편집·점수·새 에이전트 실행은 모두 0회다. Title의 존재와 역할을 명확히 하면서 전체 구성·스타일의 차이는 실제 이미지 조직·경계·큰 카피 면적에서 유지한다. 최종 품질과 다섯 실제 결과의 차이는 아직 확인하지 않았다.
"""

for name, value in [
    ("plan-hierarchy-v2.json", json.dumps(plan, ensure_ascii=False, indent=2) + "\n"),
    ("rationale-hierarchy-v2.md", rationale),
]:
    with (OUT / name).open("x", encoding="utf-8") as stream:
        stream.write(value)
print(json.dumps({
    "parent_preserved": "plan.json/rationale.md/prepare_plan.py",
    "revision": "plan-hierarchy-v2.json",
    "Title_primary": "all five", "copy_entries": len(measurements),
    "request_copy_conditions": "exact", "guide_key": "directions[n].guide_spec",
    "native_calls": 0, "guides_rendered": 0,
}, ensure_ascii=False))
