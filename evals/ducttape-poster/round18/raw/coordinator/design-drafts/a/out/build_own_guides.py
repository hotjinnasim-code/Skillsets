"""Own R18-C1 planning shapes and conserved copy. No bitmap inputs."""
from pathlib import Path
import json
import os
import subprocess
import sys

ROOT = Path.cwd().resolve()
OUT = ROOT / "out"
RENDERER = "/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/drafts/layout-guide-helper/revision-v2/make_layout_guide.py"
NEO = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
MYUNGJO = "/System/Library/Fonts/Supplemental/AppleMyungjo.ttf"
PIL_RUNTIME = "/Users/nahyeonbin/.codex/worktrees/terrain-alignment/NAMOK-Bible-Maps/.cache/terrain-python/lib/python3.9/site-packages"
COPY = [
    "고쳐 쓰는 토요일",
    "REPAIR / TOGETHER",
    "버리는 대신, 함께 고칩니다.",
    "헐거워진 의자와 찢어진 옷을 가져오세요. 이웃 수리자와 도구를 나누며 다시 쓰는 방법을 배웁니다.",
    "마포 생활수리 워크숍",
    "2027.05.22",
    "토요일 14:00–18:00",
    "합정 동네작업실",
    "참가비 5,000원 · 도구 제공",
    "신청 마감 5월 18일",
    "수리할 물건 한 가지를 가져오세요.",
    "repair.example/join",
]


def save_new(path, obj):
    with path.open("x", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def rect(x, y, w, h, fill, stroke=None, sw=2):
    s = dict(type="rect", x=x, y=y, width=w, height=h, fill=fill)
    if stroke:
        s.update(stroke=stroke, stroke_width=sw)
    return s


def ellipse(x, y, w, h, fill, stroke=None, sw=2):
    s = dict(type="ellipse", x=x, y=y, width=w, height=h, fill=fill)
    if stroke:
        s.update(stroke=stroke, stroke_width=sw)
    return s


def poly(points, fill, stroke=None, sw=2):
    s = dict(type="polygon", points=points, fill=fill)
    if stroke:
        s.update(stroke=stroke, stroke_width=sw)
    return s


def line(x1, y1, x2, y2, color="#596369", sw=5):
    return dict(type="line", x1=x1, y1=y1, x2=x2, y2=y2,
                stroke=color, stroke_width=sw)


def block(n, x, y, w, h, size=44, index=0, font=NEO, lines=None, spacing=None,
          color="#202A30", align="left"):
    return dict(copy=COPY[n], lines=lines or [COPY[n]], fixed_newlines=False,
                x=x, y=y, align=align, line_spacing=spacing or size * 1.3,
                area=dict(width=w, height=h),
                font=dict(path=font, index=index, size=size), color=color)


def m1():
    # One continuous scene. The near table connects both repair contacts.
    s = [
        poly([[0, 467], [1130, 302], [1672, 550], [1672, 941], [0, 941]], "#C8CFD1"),
        line(20, 464, 1128, 304, "#A0ABAF", 4),
        line(1130, 304, 1650, 550, "#A0ABAF", 4),
        # Left upper neighbor, bending into chair repair.
        ellipse(154, 51, 148, 166, "#D6DBDC", "#68757B", 3),
        poly([[153, 114], [164, 73], [208, 54], [276, 69], [304, 115], [275, 106], [235, 86], [186, 111]], "#616E75"),
        line(189, 135, 208, 133, "#59666C", 3),
        line(245, 132, 263, 136, "#59666C", 3),
        line(219, 174, 245, 169, "#59666C", 3),
        poly([[86, 245], [180, 204], [280, 210], [369, 292], [452, 370], [408, 426], [283, 344], [212, 476], [34, 387]], "#78878E"),
        poly([[293, 329], [337, 298], [430, 366], [461, 421], [408, 505], [363, 560], [328, 539], [361, 473], [397, 409]], "#A4B0B5"),
        ellipse(331, 532, 55, 48, "#D6DBDC", "#68757B", 2),
        # Left lower neighbor braces the same chair joint.
        ellipse(27, 491, 130, 146, "#D6DBDC", "#68757B", 3),
        poly([[29, 535], [47, 500], [107, 491], [152, 523], [155, 552], [115, 528], [75, 522]], "#66757C"),
        line(76, 568, 94, 566, "#59666C", 3),
        line(116, 568, 134, 573, "#59666C", 3),
        poly([[2, 718], [49, 638], [135, 625], [221, 665], [244, 825], [210, 939], [2, 939]], "#697A83"),
        poly([[154, 680], [196, 646], [281, 614], [337, 584], [366, 602], [340, 633], [282, 653], [205, 699]], "#A4B0B5"),
        ellipse(316, 582, 53, 45, "#D6DBDC", "#68757B", 2),
        # Recognizable loose chair: back, seat, legs, the braced joint.
        line(154, 469, 235, 656, "#56656D", 19),
        line(346, 431, 401, 613, "#56656D", 19),
        line(159, 473, 347, 434, "#56656D", 19),
        line(183, 537, 365, 502, "#56656D", 14),
        line(208, 597, 383, 563, "#56656D", 14),
        poly([[231, 649], [401, 611], [451, 698], [273, 737]], "#8A999F", "#56656D", 7),
        line(279, 737, 281, 906, "#56656D", 16),
        line(445, 702, 403, 878, "#56656D", 16),
        line(233, 655, 169, 831, "#56656D", 15),
        line(186, 816, 406, 849, "#56656D", 10),
        # Two hands really meet chair/tool. One holds, the other turns.
        ellipse(328, 586, 43, 29, "#D6DBDC", "#68757B", 2),
        line(349, 602, 395, 548, "#35454E", 5),
        line(395, 548, 412, 528, "#35454E", 16),
        line(337, 588, 356, 595, "#68757B", 2),
        # Right upper neighbor with a needle over the shared garment.
        ellipse(1424, 72, 153, 174, "#D6DBDC", "#68757B", 3),
        poly([[1428, 134], [1436, 94], [1474, 74], [1538, 81], [1573, 118], [1572, 156], [1541, 133], [1488, 113]], "#596B74"),
        line(1464, 158, 1483, 155, "#59666C", 3),
        line(1520, 156, 1537, 160, "#59666C", 3),
        line(1478, 205, 1516, 199, "#59666C", 3),
        poly([[1379, 256], [1472, 235], [1576, 254], [1654, 361], [1669, 528], [1469, 501], [1326, 385]], "#7C8C93"),
        poly([[1386, 352], [1436, 390], [1376, 478], [1304, 548], [1260, 531], [1291, 493]], "#A4B0B5"),
        ellipse(1248, 522, 61, 42, "#D6DBDC", "#68757B", 2),
        poly([[1538, 410], [1581, 429], [1544, 530], [1438, 598], [1406, 570], [1491, 512]], "#A4B0B5"),
        # Shirt is a whole recognizable repair object, not a color patch.
        poly([[1243, 548], [1320, 523], [1355, 555], [1384, 528], [1460, 552], [1542, 635], [1480, 699], [1433, 652], [1446, 811], [1253, 837], [1239, 663], [1205, 699], [1141, 637]], "#98A8AF", "#56656D", 5),
        poly([[1320, 525], [1334, 550], [1363, 551], [1385, 530], [1374, 568], [1334, 574]], "#C8CFD1", "#56656D", 3),
        line(1274, 654, 1324, 674, "#465961", 4),
        line(1324, 674, 1283, 699, "#465961", 4),
        line(1283, 699, 1330, 720, "#465961", 4),
        # Second garment neighbor holds the cloth against the needle tension.
        ellipse(1520, 654, 132, 148, "#D6DBDC", "#68757B", 3),
        poly([[1523, 695], [1540, 663], [1588, 654], [1637, 677], [1650, 710], [1601, 682], [1560, 684]], "#627680"),
        line(1549, 725, 1567, 723, "#59666C", 3),
        line(1603, 725, 1620, 731, "#59666C", 3),
        poly([[1558, 800], [1658, 798], [1672, 840], [1672, 941], [1425, 941], [1445, 854]], "#6C818C"),
        poly([[1476, 844], [1447, 802], [1389, 754], [1345, 716], [1306, 721], [1348, 766], [1394, 822]], "#A4B0B5"),
        ellipse(1298, 700, 58, 38, "#D6DBDC", "#68757B", 2),
        ellipse(1396, 565, 51, 38, "#D6DBDC", "#68757B", 2),
        line(1410, 591, 1322, 680, "#465961", 3),
        line(1322, 680, 1283, 638, "#68757B", 2),
        line(1283, 638, 1274, 556, "#68757B", 2),
        line(1310, 697, 1322, 708, "#68757B", 2),
    ]
    t = [
        block(0, 579, 40, 660, 103, 82, font=MYUNGJO),
        block(1, 579, 151, 520, 50, 38, index=2),
        block(2, 552, 214, 665, 58, 46, font=MYUNGJO),
        block(3, 521, 292, 730, 174, 44, index=0,
              lines=["헐거워진 의자와 찢어진 옷을", "가져오세요. 이웃 수리자와 도구를", "나누며 다시 쓰는 방법을 배웁니다."], spacing=59),
        block(4, 503, 486, 640, 58, 44, index=2),
        block(5, 484, 547, 285, 64, 52, index=2),
        block(6, 797, 552, 400, 58, 44, index=0),
        block(7, 470, 617, 690, 54, 42, index=0),
        block(8, 452, 675, 690, 54, 42, index=0),
        block(9, 432, 738, 680, 54, 42, index=2),
        block(10, 432, 794, 660, 54, 42, index=0),
        block(11, 432, 851, 650, 56, 43, index=2),
    ]
    return dict(canvas=dict(width=1672, height=941, background="#B5C0C5"), shapes=s, text_blocks=t)


def m2():
    # A distributed relation: upper wood/cloth contacts and lower shared tools.
    # The open horizontal seam between them is the information route.
    s = [
        # Upper-left chair carries a brace rather than a decorative icon.
        line(99, 123, 145, 310, "#53636C", 20),
        line(327, 104, 369, 284, "#53636C", 20),
        line(100, 126, 327, 107, "#53636C", 19),
        line(122, 205, 347, 180, "#53636C", 14),
        poly([[143, 279], [367, 253], [434, 306], [197, 336]], "#91A1A8", "#53636C", 6),
        line(197, 336, 183, 380, "#53636C", 15),
        line(420, 310, 459, 359, "#53636C", 15),
        # Two cropped clothed forearms stabilise the rail and turn a driver.
        poly([[20, 221], [96, 201], [145, 227], [128, 269], [58, 281], [20, 265]], "#6E808B"),
        poly([[126, 229], [170, 222], [226, 234], [235, 258], [199, 270], [138, 267]], "#D2DADC", "#53636C", 2),
        line(188, 239, 210, 243, "#687B85", 2),
        poly([[415, 138], [479, 155], [485, 214], [439, 238], [399, 196]], "#6E808B"),
        poly([[419, 217], [437, 195], [467, 207], [457, 248], [422, 273], [398, 260]], "#D2DADC", "#53636C", 2),
        line(424, 246, 357, 204, "#374D5B", 5),
        line(449, 261, 422, 244, "#374D5B", 16),
        # The long brace is a real wood connection into the seam edge.
        line(457, 338, 619, 386, "#82939A", 13),
        # Shared screwdriver transfer, another large relational node.
        poly([[504, 178], [549, 160], [637, 183], [649, 220], [611, 247], [525, 217]], "#82939C"),
        poly([[625, 194], [661, 194], [700, 212], [705, 236], [672, 250], [637, 229]], "#D2DADC", "#53636C", 2),
        poly([[815, 188], [879, 159], [962, 178], [959, 222], [862, 247], [815, 226]], "#738893"),
        poly([[776, 202], [824, 194], [842, 220], [814, 245], [769, 242], [748, 223]], "#D2DADC", "#53636C", 2),
        line(700, 220, 772, 220, "#374D5B", 7),
        line(725, 220, 763, 220, "#374D5B", 18),
        # Upper-right shirt, damaged hem held by two neighbors.
        poly([[1172, 179], [1242, 169], [1278, 196], [1314, 169], [1384, 180], [1471, 250], [1420, 314], [1372, 280], [1379, 376], [1185, 367], [1180, 280], [1146, 317], [1092, 256]], "#A0AFB5", "#53636C", 5),
        poly([[1243, 170], [1258, 195], [1292, 199], [1315, 170], [1307, 214], [1255, 214]], "#BFCACF", "#53636C", 3),
        line(1263, 293, 1300, 303, "#53636C", 4),
        line(1300, 303, 1268, 324, "#53636C", 4),
        line(1268, 324, 1308, 339, "#53636C", 4),
        poly([[1490, 184], [1571, 162], [1654, 192], [1654, 225], [1530, 254], [1478, 231]], "#728A98"),
        poly([[1439, 220], [1481, 207], [1511, 228], [1478, 258], [1433, 264], [1417, 242]], "#D2DADC", "#53636C", 2),
        poly([[1028, 287], [1068, 260], [1125, 281], [1132, 319], [1089, 336], [1039, 321]], "#738893"),
        poly([[1115, 286], [1143, 282], [1183, 296], [1195, 318], [1168, 339], [1127, 322]], "#D2DADC", "#53636C", 2),
        line(1430, 247, 1300, 303, "#53636C", 3),
        # The actual sewing thread bypasses the information and reaches below.
        line(1308, 339, 1438, 403, "#7E929D", 3),
        line(1438, 403, 1514, 534, "#7E929D", 3),
        line(1514, 534, 1539, 671, "#7E929D", 3),
        line(1539, 671, 1470, 782, "#7E929D", 3),
        # Lower-left chair contact is large and cropped at its real legs.
        line(100, 841, 136, 927, "#53636C", 18),
        line(348, 811, 379, 927, "#53636C", 18),
        line(106, 844, 353, 814, "#53636C", 18),
        poly([[131, 879], [369, 848], [432, 905], [192, 934]], "#91A1A8", "#53636C", 5),
        poly([[24, 807], [75, 788], [131, 827], [110, 868], [52, 854], [24, 832]], "#6E808B"),
        poly([[106, 833], [151, 816], [187, 832], [179, 855], [144, 869], [111, 856]], "#D2DADC", "#53636C", 2),
        poly([[431, 788], [493, 808], [523, 857], [488, 895], [445, 861]], "#6E808B"),
        poly([[414, 828], [440, 831], [465, 856], [447, 881], [412, 860], [397, 842]], "#D2DADC", "#53636C", 2),
        line(430, 851, 371, 869, "#374D5B", 5),
        # Broad lower central cloth is supported jointly, patch under tension.
        poly([[642, 827], [719, 787], [842, 776], [961, 831], [992, 916], [687, 931]], "#98ACB7", "#53636C", 5),
        rect(774, 822, 127, 63, "#BDC8CE", "#53636C", 3),
        line(789, 829, 785, 841, "#53636C", 3),
        line(815, 829, 811, 841, "#53636C", 3),
        line(841, 829, 837, 841, "#53636C", 3),
        line(867, 829, 863, 841, "#53636C", 3),
        poly([[560, 774], [593, 753], [669, 778], [679, 813], [641, 847], [577, 813]], "#738893"),
        poly([[651, 790], [687, 787], [722, 805], [726, 828], [699, 845], [662, 822]], "#D2DADC", "#53636C", 2),
        poly([[960, 790], [1010, 773], [1067, 791], [1072, 826], [1009, 850], [968, 830]], "#738893"),
        poly([[909, 804], [957, 794], [979, 818], [951, 844], [912, 838], [895, 822]], "#D2DADC", "#53636C", 2),
        line(910, 821, 866, 845, "#53636C", 3),
        # Lower-right hand takes the thread/spool: action exit beside URL.
        ellipse(1391, 796, 117, 81, "#BFCAD0", "#53636C", 5),
        ellipse(1410, 808, 78, 58, "#91A5B0", "#53636C", 3),
        poly([[1500, 824], [1551, 790], [1651, 802], [1660, 852], [1570, 879], [1521, 861]], "#738893"),
        poly([[1477, 810], [1512, 810], [1544, 830], [1537, 852], [1507, 865], [1480, 847]], "#D2DADC", "#53636C", 2),
        line(1470, 782, 1444, 821, "#7E929D", 3),
        line(1295, 889, 1413, 848, "#7E929D", 3),
        line(1156, 914, 1295, 889, "#7E929D", 3),
    ]
    t = [
        # Title identifies the cloth-side node; the invitation opens the seam.
        block(0, 994, 49, 626, 110, 88, index=2),
        block(1, 75, 52, 610, 54, 40, index=2),
        block(2, 79, 728, 710, 62, 44, font=MYUNGJO),
        block(3, 89, 413, 1240, 127, 42, font=MYUNGJO,
              lines=["헐거워진 의자와 찢어진 옷을 가져오세요.", "이웃 수리자와 도구를 나누며 다시 쓰는 방법을 배웁니다."], spacing=61),
        block(4, 89, 554, 450, 56, 42, index=2),
        block(5, 575, 551, 279, 61, 48, index=4),
        block(6, 917, 555, 452, 56, 42, index=2),
        block(7, 89, 619, 350, 56, 42, index=0),
        block(8, 486, 619, 502, 56, 42, index=0),
        block(9, 1040, 619, 432, 56, 42, index=2),
        block(10, 89, 338, 800, 58, 46, index=2),
        block(11, 1040, 680, 480, 56, 42, index=2),
    ]
    return dict(canvas=dict(width=1672, height=941, background="#BFCACF"), shapes=s, text_blocks=t)


def main():
    OUT.mkdir(exist_ok=True)
    with (OUT / "runtime-preflight-failure.txt").open("x", encoding="utf-8") as f:
        f.write("Runtime preflight before guide rendering: default python3 could not import PIL.\n")
        f.write("Traceback (most recent call last):\n  File <stdin>, line 1, in <module>\nModuleNotFoundError: No module named 'PIL'\n")
        f.write("No guide spec/render was attempted in this preflight.\n")
        f.write("Resolved using existing Pillow dependency runtime, read only; no installation or network call.\n")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=PIL_RUNTIME)
    outcomes = []
    for role, make in [("R18-C1-M1", m1), ("R18-C1-M2", m2)]:
        stem = role.lower() + "-guide-attempt-01"
        spec_path = OUT / (stem + ".spec.json")
        spec = make()
        assert len(spec["text_blocks"]) == 12
        assert sorted(b["copy"] for b in spec["text_blocks"]) == sorted(COPY)
        assert all(" ".join(b["lines"]) == b["copy"] for b in spec["text_blocks"])
        save_new(spec_path, spec)
        cmd = [sys.executable, RENDERER, str(spec_path), "--output-dir", str(OUT), "--name", stem]
        result = subprocess.run(cmd, cwd=str(ROOT), env=env, text=True, capture_output=True)
        with (OUT / (stem + ".render.log")).open("x", encoding="utf-8") as f:
            f.write("cwd: " + str(ROOT) + "\n")
            f.write("renderer: " + RENDERER + "\n")
            f.write("exit_code: " + str(result.returncode) + "\n")
            f.write(result.stdout)
            f.write(result.stderr)
        outcomes.append(dict(role_id=role, stem=stem, exit_code=result.returncode,
                             spec_path=str(spec_path), log_path=str(OUT / (stem + ".render.log"))))
        print(role, "renderer exit", result.returncode)
        print(result.stdout or result.stderr)
    save_new(OUT / "guide-render-record-01.json", dict(renderer=RENDERER, cwd=str(ROOT), attempts=outcomes))


if __name__ == "__main__":
    main()
