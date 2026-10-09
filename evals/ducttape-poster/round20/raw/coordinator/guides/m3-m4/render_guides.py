from pathlib import Path
import collections
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone

WORK = Path.cwd().resolve()
OUT = WORK / "coordinator/guides/m3-m4"
PLAN_PATH = WORK.parent.parent / "drafts/w-five-design/plan.json"
RENDERER = WORK / "snapshots/candidate-w/scripts/make_layout_guide.py"
CASE_PATH = WORK / "planning/single-five-case.json"
PYTHON = Path(sys.executable)


def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def rect(x, y, width, height, fill):
    return dict(type="rect", x=x, y=y, width=width, height=height, fill=fill)


def ellipse(x, y, width, height, fill):
    return dict(type="ellipse", x=x, y=y, width=width, height=height, fill=fill)


def polygon(points, fill):
    return dict(type="polygon", points=points, fill=fill)


def line(x1, y1, x2, y2, stroke, width):
    return dict(type="line", x1=x1, y1=y1, x2=x2, y2=y2, stroke=stroke, stroke_width=width)


def m3_shapes():
    return [
        # A cropped adult, bent sleeves and two connected working forearms.
        polygon([[0, 193], [132, 118], [218, 151], [339, 316], [407, 494], [354, 652], [203, 756], [0, 756]], "#63706C"),
        ellipse(194, 100, 160, 175, "#B4AAA0"),
        polygon([[190, 235], [220, 294], [285, 340], [315, 288], [279, 228]], "#B4AAA0"),
        polygon([[268, 420], [350, 442], [390, 704], [555, 752], [841, 779], [850, 831], [522, 814], [318, 749], [280, 620]], "#8A918C"),
        polygon([[328, 508], [385, 575], [429, 736], [836, 834], [1106, 809], [1149, 756], [1193, 766], [1140, 854], [830, 884], [394, 782], [325, 670]], "#74827A"),
        polygon([[822, 779], [903, 789], [981, 790], [1023, 807], [1001, 828], [898, 831], [841, 819]], "#B4AAA0"),
        # Rootball rests at the supporting hand; another hand steadies pot rim.
        ellipse(922, 712, 225, 109, "#7B6E60"),
        ellipse(948, 721, 166, 62, "#9C8D76"),
        line(970, 758, 1000, 798, "#4E554D", 4),
        line(1010, 762, 1018, 807, "#4E554D", 4),
        line(1051, 758, 1037, 805, "#4E554D", 4),
        line(1000, 779, 976, 805, "#4E554D", 3),
        line(1052, 778, 1075, 804, "#4E554D", 3),
        polygon([[1163, 747], [1485, 747], [1451, 896], [1200, 896]], "#A49D91"),
        ellipse(1150, 714, 348, 64, "#69756C"),
        ellipse(1174, 727, 299, 30, "#3D4842"),
        polygon([[1106, 809], [1135, 776], [1150, 745], [1190, 730], [1226, 737], [1211, 760], [1178, 762], [1169, 810]], "#B4AAA0"),
        line(1187, 737, 1203, 749, "#5E655C", 3),
        line(1178, 748, 1192, 758, "#5E655C", 3),
        # Attached plant stems and a few deliberate leaf masses.
        line(1028, 720, 1074, 628, "#44564B", 7),
        line(1045, 692, 1112, 661, "#44564B", 5),
        polygon([[1068, 640], [1086, 596], [1143, 606], [1115, 636]], "#66765F"),
        polygon([[1102, 662], [1148, 633], [1203, 658], [1156, 679]], "#66765F"),
        polygon([[1047, 692], [997, 659], [970, 676], [1028, 713]], "#53695A"),
        line(1051, 715, 1101, 690, "#44564B", 5),
        polygon([[1090, 696], [1150, 683], [1168, 702], [1113, 718]], "#7A8A6F"),
    ]


def m4_shapes():
    return [
        # Three authored crop bands; contacts within them carry the action.
        rect(590, 0, 1010, 275, "#BAC3C8"),
        polygon([[590, 70], [747, 108], [949, 186], [1096, 206], [1075, 245], [931, 222], [735, 151], [590, 130]], "#727F84"),
        polygon([[978, 186], [1074, 196], [1194, 197], [1251, 218], [1205, 243], [1074, 238], [991, 226]], "#D4D6CF"),
        ellipse(1050, 67, 240, 158, "#66716B"),
        ellipse(1071, 82, 190, 91, "#929A88"),
        line(1105, 150, 1125, 210, "#364843", 5),
        line(1151, 151, 1147, 216, "#364843", 5),
        line(1196, 151, 1172, 215, "#364843", 5),
        line(1155, 76, 1174, 6, "#354C46", 7),
        polygon([[1171, 34], [1230, 6], [1280, 31], [1212, 61]], "#556E60"),
        polygon([[1154, 53], [1080, 9], [1046, 37], [1139, 82]], "#556E60"),
        polygon([[1381, 126], [1566, 126], [1544, 267], [1406, 267]], "#78838A"),
        ellipse(1369, 108, 209, 46, "#424F54"),
        ellipse(1385, 118, 177, 25, "#A2ADA9"),
        polygon([[1537, 0], [1599, 0], [1599, 99], [1518, 123], [1450, 137], [1421, 118], [1496, 88]], "#D1D5D1"),
        line(1434, 121, 1460, 120, "#596766", 3),
        # Closer roots and soil, with a supported hand and cropped pot edge.
        rect(0, 305, 590, 280, "#C8CECD"),
        polygon([[0, 435], [97, 462], [142, 501], [268, 530], [292, 558], [263, 574], [121, 544], [64, 504], [0, 487]], "#85928E"),
        ellipse(111, 325, 250, 209, "#727A6A"),
        ellipse(139, 350, 195, 100, "#969C80"),
        line(161, 386, 204, 504, "#374D43", 6),
        line(205, 388, 239, 522, "#374D43", 6),
        line(262, 391, 267, 515, "#374D43", 6),
        line(297, 392, 279, 505, "#374D43", 5),
        line(221, 448, 192, 504, "#374D43", 4),
        line(264, 455, 297, 504, "#374D43", 4),
        polygon([[376, 318], [590, 338], [590, 585], [399, 585]], "#71808A"),
        ellipse(362, 318, 222, 58, "#46565C"),
        ellipse(384, 331, 186, 29, "#ADB5AE"),
        polygon([[85, 501], [153, 516], [227, 523], [274, 539], [254, 557], [155, 550], [109, 541]], "#D4D7CE"),
        line(229, 326, 238, 310, "#455C4D", 8),
        # The final seated pot is supported by two visibly attached hands.
        rect(770, 640, 830, 260, "#AAB7BF"),
        polygon([[770, 684], [907, 701], [1060, 748], [1162, 768], [1151, 810], [1047, 787], [893, 743], [770, 728]], "#75848B"),
        polygon([[1159, 764], [1447, 764], [1416, 898], [1192, 898]], "#6F7C83"),
        ellipse(1145, 720, 316, 79, "#3D5053"),
        ellipse(1170, 733, 267, 46, "#747A69"),
        line(1300, 747, 1291, 645, "#345348", 8),
        line(1295, 689, 1219, 659, "#345348", 6),
        polygon([[1226, 667], [1165, 650], [1174, 681], [1247, 701]], "#536E60"),
        polygon([[1294, 672], [1363, 647], [1417, 678], [1335, 703]], "#536E60"),
        polygon([[1060, 748], [1142, 750], [1188, 767], [1199, 784], [1175, 800], [1140, 779], [1090, 782]], "#D0D5D0"),
        polygon([[1599, 693], [1599, 752], [1503, 768], [1452, 802], [1418, 793], [1407, 772], [1442, 745], [1492, 729]], "#D0D5D0"),
        line(1422, 779, 1447, 765, "#64736B", 3),
        line(1168, 768, 1185, 784, "#64736B", 3),
    ]


def main():
    assert WORK.name == "round20" and OUT.is_relative_to(WORK)
    plan = json.loads(PLAN_PATH.read_text())
    corpus = json.loads(CASE_PATH.read_text())
    case = next(c for c in corpus["cases"] if c["case_id"] == "R20-C1")
    assert plan["copy"] == case["copy"]
    expected = collections.Counter(c["text"] for c in case["copy"])
    records = []
    source_pin = pin(PLAN_PATH)
    renderer_pin = pin(RENDERER)
    for role_num, shape_factory in [(3, m3_shapes), (4, m4_shapes)]:
        role = f"R20-C1-M{role_num}"
        direction = next(d for d in plan["directions"] if d["role"] == role)
        geometry = direction["guide_geometry_concept"]
        regions = geometry["text_regions"]
        assert len(regions) == 12 and {r["entry"] for r in regions} == set(range(1, 13))
        assert collections.Counter(r["copy"] for r in regions) == expected
        for region in regions:
            assert " ".join(region["lines"]) == region["copy"]
        spec = {"canvas": geometry["canvas"], "shapes": shape_factory(),
                "text_blocks": [{k: v for k, v in r.items() if k != "entry"} for r in regions]}
        spec_path = OUT / f"m{role_num}-layout.json"
        with spec_path.open("x") as f:
            json.dump(spec, f, ensure_ascii=False, indent=2)
            f.write("\n")
        argv = [str(PYTHON), "-B", str(RENDERER), str(spec_path),
                "--output-dir", str(OUT), "--name", f"m{role_num}-guide"]
        completed = subprocess.run(argv, cwd=WORK, capture_output=True, text=True)
        record = {"role": role, "argv": argv, "cwd": str(WORK), "exit_code": completed.returncode,
                  "stdout": completed.stdout, "stderr": completed.stderr,
                  "spec": pin(spec_path), "technical_adjustments": [],
                  "copy_entries": 12, "copy_occurs_once_in_text_blocks": True,
                  "proposed_text_regions_fonts_positions_lines_preserved": True,
                  "shapes": len(spec["shapes"])}
        if completed.returncode == 0:
            record["outputs"] = [pin(OUT / f"m{role_num}-guide{s}") for s in [".svg", ".png", ".manifest.json"]]
        records.append(record)
        if completed.returncode:
            break
    status = {"recorded_utc": datetime.now(timezone.utc).isoformat(), "kind": "authored_planning_render",
              "plan": source_pin, "renderer": renderer_pin, "case": pin(CASE_PATH), "renders": records,
              "preparation_attempts": [{"attempt": 1, "status": "schema_read_error_before_specs_or_rendering", "error": "KeyError: copy; canonical case file is a corpus with cases, corrected to select R20-C1. No plan/runtime/copy change."}],
              "native_calls": 0, "bitmap_inputs": 0, "poster_scores": None,
              "png_viewed": False,
              "limits": ["New code-only shapes and supplied-font copy are planning references, not final poster artwork.",
                         "Neutral action geometry does not certify rendered anatomical or material finish in a later native image.",
                         "Guide font bytes and positions do not certify final native font-file application or client preservation coordinates.",
                         "The original plan and runtime remain unchanged; all print copy is supplied exactly once."]}
    assert pin(PLAN_PATH) == source_pin and pin(RENDERER) == renderer_pin
    with (OUT / "render-status.json").open("x") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps({"status": str(OUT / "render-status.json"),
                      "renders": [{"role": r["role"], "exit_code": r["exit_code"],
                                   "shapes": r["shapes"], "stderr": r["stderr"]} for r in records]}))


if __name__ == "__main__":
    main()
