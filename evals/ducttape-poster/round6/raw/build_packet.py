#!/usr/bin/env python3
"""Seal anonymous complete five-poster case packets from an explicit selection.

No winner selection, generation, retouching, or critic observations occur here.
Only byte copies and Pillow LANCZOS resizing are used. Existing waves are refused.
"""
import argparse
import datetime as dt
import hashlib
import json
import random
import re
import shutil
import tempfile
from pathlib import Path

from PIL import Image

DIMS = ("content_form", "hierarchy", "typography", "space", "image_material", "emotion_control", "ai_slop")
PROFILES = ("editorial", "craft", "portfolio")
ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def resolve(value, base=ROOT):
    path = Path(value)
    return (path if path.is_absolute() else base / path).resolve()


def write(path, value):
    with path.open("x") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def check(condition, message):
    if not condition:
        raise ValueError(message)


def plan_pins(plan, cases_path):
    """One compact R6 schema: cases and frozen_skill_files pin lists."""
    pin = plan["cases"]
    check(resolve(pin["path"]) == cases_path, "Plan cases pin resolves to another file")
    pins = [dict(pin, kind="cases")]
    skills = plan["frozen_skill_files"]
    check(isinstance(skills, list) and skills, "frozen_skill_files must be a nonempty pin list")
    pins.extend(dict(item, kind="frozen_skill") for item in skills)
    for pin in pins:
        path = resolve(pin["path"])
        check(path.is_file() and sha(path) == pin["sha256"], "Frozen source SHA mismatch: " + str(path))
    review = plan["review"]
    check(review["independent_reviewers"] == 3, "Review must retain three reviewers")
    check(tuple(review["seven_dimensions"]) == DIMS, "Seven dimensions changed")
    gate = review["unchanged_core_gate"]
    check(all(d in gate for d in ("content_form", "typography", "image_material", "ai_slop"))
          and ">=4" in gate and "diversity" in gate, "Core/diversity gate changed")
    return pins


def action_fields(case):
    fields = case.get("action_fields", {})
    check(isinstance(fields, dict), "action_fields must map field names to exact expected readings")
    check(all(isinstance(k, str) and k and isinstance(v, str) and v for k, v in fields.items()), "Invalid action_fields")
    return fields


PROTOCOL = """# Independent anonymous visible-output review

FIRST open preflight.json only. Actually view every listed usage720 image. Save reviews/PROFILE-action-first.json BEFORE opening packet.json or its full copy. Record each requested field from pixels, its uncertainty, and the actual viewed image path. Preserve this initial record unchanged after full-copy cross-check. For a case with no action fields, save readings:[] and viewed:[] before opening the packet. Disclose any order violation.

Then open packet.json and actually view EVERY image at native, usage720, and thumbnail320: five images mean fifteen views. Record actual view_image calls with image_id, view, path. A statement that the images were viewed is insufficient. Read every exact supplied text item manually from the image and cross-check against full copy. Check alteration, ambiguity, omissions and unrequested additions; all required copy must be legible at usage720. Check the request and ratio within 1%. Pixels do not certify authorship, physical mechanics, capacity, or print suitability. Do not inspect private mappings, skills, sources, plans, production files, prompts, maker names, histories, prior or peer reports, or expected score targets.

Give all seven integer scores 1–5 with located visible evidence and residual issues. Assess the requested style faithfully without inventing campaign uniformity, minimalism, handlettering, or material preferences. Familiar fonts, photos, and effects can be well resolved. Preserve low scores and uncertainty; do not average, rewrite a consensus, or presume a generation history. For every case give exact set members, diversity, and the closest pair's two members, integer score, and visible evidence.

각 항목은 실제 보이는 근거를 하나 이상 적는다. 2와 4는 아래 기준 사이이며, 총점을 합산해 결함을 덮지 않는다.

| 항목 | 1: 미해결 | 3: 기능하는 결과 | 5: 매우 잘 해결된 결과 |
| --- | --- | --- | --- |
| 내용과 형태 | 다른 주제에도 그대로 쓸 상투적 구성 | 주제를 반영하지만 일부 선택이 임의적 | 구체적인 발상이 주요 선택을 연결하며 억지 해석이 없음 |
| 정보 계층 | 시선 분산·순서 혼란 | 중심과 읽는 순서가 보임 | 축소의 첫 시선부터 사용 크기의 참여 안내까지 자연스럽게 연결 |
| 타이포그래피 | 글자가 덧붙여진 느낌·불균일한 간격 | 판독과 그룹화가 합리적 | 획·줄 묶음·크기·간격·배치가 이미지와 하나의 구성으로 작동 |
| 공간 | 임의 마진·접촉·죽은 공간 | 전체 균형과 정렬이 일관됨 | 크롭·무게·여백·경계의 큰 관계와 작은 관계가 의도적 |
| 이미지와 재질 | 원근·빛·경계·질감의 혼란 | 표현 체계가 대체로 일관됨 | 원본에서도 재질·형태·마감이 발상에 맞게 정교하거나 의도적으로 거침 |
| 정서와 제어 | 효과·장식의 축적에 의존 | 요청에 맞는 정서와 요소 | 절제든 과잉이든 표현이 정확하고 각 요소가 역할을 가짐 |
| AI 슬롭 방지 | 상투적 패키지·글자·재질의 합성 흔적이 두드러짐 | 기술적으로 일관되지만 범용적인 습관이 남음 | 내용에 특화된 편집·글자·공간·재질이 설득력 있고 눈에 띄는 합성 결함이 없음 |

전체 결과의 다양성은 별도로 판단한다. 1은 색·필터만 다른 반복, 3은 구분되지만 구조적 습관이 남음, 5는 공통 조건 안에서 각 방향의 발상·글자 역할·공간·이미지 표현이 설득력 있게 나뉨이다. 최고 시안뿐 아니라 최저 시안과 전체 분포를 본다.

기본 스타일의 선호와 지정 스타일의 충실도를 나누어 본다. 스타일이 열린 요청에서는 범용 효과 패키지의 근거와 우선순위를 확인하고, 효과를 명시한 요청에서는 실제로 그 표현이 구현됐는지 먼저 확인한다. 둘 다 같은 주제·글자·마감 기준을 적용한다. 크롬을 쓰지 않았거나 아이보리 종이를 썼다는 이유만으로 높은 점수를 주지 않는다.

AI 슬롭 점수는 제작 주체 판별이 아니다. 아래에 함께 제공한 동일한 AI 슬롭 검수 기준을 실제 위치와 근거로 적용하며, 특정 스타일이라는 이유로 감점하지 않는다. 이 항목이 3 이하이거나 평가자에게 구체적인 합성 흔적이 보이면 하이엔드 후보로 단정하지 않고 보정하거나 잔여 문제로 기록한다. 평가 기준이 실행 중 추가되면 어느 버전에 반영됐고 어느 출력에 사후 적용했는지 기록한다.

## Same unchanged AI-slop inspection detail

목표는 생성 도구의 관습이 먼저 보이지 않고, 이 내용을 위해 편집하고 제작한 결과로 보이게 하는 것이다. "AI처럼 보이지 않게"라는 말만 프롬프트에 넣는 것으로 끝내지 않는다. 다음 흔적을 실제 이미지의 위치와 원인으로 판단한다.

- **주제와 무관한 익숙한 패키지:** 제목만 바꾸면 다른 행사에도 맞는 이미지·효과·타이포 조합, 스타일 이름 외에 설명할 수 없는 선택.
- **장식을 위한 정보 흉내:** 의미 없는 숫자·도형·구분선·가짜 로고·미세 문자. 사용자가 제공한 정보와 연결된 표식은 유지한다.
- **글자가 따로 노는 결과:** 이미지와 접점 없는 제목, 불규칙한 한글 획, 어절을 망가뜨리는 간격, 아무 정보나 같은 굵기로 강조한 계층.
- **재질과 제작 논리의 혼란:** 서로 다른 물체가 이유 없이 같은 광택을 띰, 원근·빛이 맞지 않음, 인쇄 질감이 글자·종이·그림자에 무차별로 덮임, 가장자리의 우연한 녹음·후광.
- **보정할수록 쌓이는 효과:** 읽기·정렬·발상이 약한데 빛·질감·소품을 추가해 감춤. 먼저 관계·간격·형태를 고친다.

각 지적은 **보이는 근거 → 전달이나 마감에 미치는 영향 → 구체적인 수정**으로 연결한다. 손그림·거친 인쇄·왜곡·3D·강한 색은 일관된 표현이면 유효하다. 디지털 광택을 종이 질감으로 바꾸는 것만으로 슬롭이 사라지는 것은 아니다.

검수자는 제작자의 설명 없이 결과를 먼저 보고, 필요하면 실제 디자인 자료와 같은 크기에서 비교한다. 원본 출처의 구도와 표면을 복제하는 대신 편집의 정밀도와 제작의 일관성을 기준으로 삼는다. 모호하면 "AI 슬롭 없음"으로 통과시키지 말고 구체적인 잔여 문제나 판단 불확실성을 남긴다. 이미지로 제작 주체를 확정하거나 인간 제작을 보장하지 않는다.

Deliver reviews/PROFILE.md and PROFILE.json. PROFILE is editorial, craft, or portfolio.
Preflight JSON: {reviewer:PROFILE,order_compliant:boolean,method:string,viewed:[{image_id,view:"usage720",path}],readings:[{image_id,path,fields:{FIELD:observed_string},uncertainties:[]}]}. For nonaction cases readings and viewed are [].
Main JSON: {reviewer:PROFILE,order_compliant:boolean,method:"manual visual transcription ...",viewed:[{image_id,view,path}],images:{ID:{mandatory:{pass:boolean,issues:[],uncertainties:[],transcription:[{required:exact_supplied_string,observed:manually_read_string,equal:boolean}],use_readings:{all_required_copy_legible_at720:boolean,observations:string}},scores:{content_form,hierarchy,typography,space,image_material,emotion_control,ai_slop},evidence:{each_same_dimension:located_string},residuals:[]}},sets:{CASE_ID:{members:[exact_IDs],diversity:integer,closest_pair:{members:[ID,ID],score:integer,evidence:string},evidence:string,residuals:[]}}}.
Observed strings remain authoritative even when they differ from supplied copy. Scores must come from actual observations; do not alter them to satisfy a target. Return exact saved paths and the concrete unresolved findings.
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--wave", required=True)
    ap.add_argument("--selection", type=Path, required=True)
    ap.add_argument("--cases", type=Path, default=ROOT / "planning/cases.json")
    ap.add_argument("--plan", type=Path, default=ROOT / "planning/phase-plan.json")
    ap.add_argument("--case", action="append", dest="case_ids", help="Seal only these complete cases; repeatable")
    ap.add_argument("--id-prefix", default="X")
    args = ap.parse_args()
    check(re.fullmatch(r"[A-Za-z0-9_-]+", args.wave), "Unsafe wave name")
    check(re.fullmatch(r"[A-Z]+", args.id_prefix), "ID prefix must be uppercase letters")
    wave = ROOT / ("blind-" + args.wave)
    private = ROOT / "private" / (args.wave + "-mapping.json")
    check(not wave.exists() and not private.exists(), "Existing wave/mapping is immutable; choose a new wave")
    selection_path, cases_path, plan_path = args.selection.resolve(), args.cases.resolve(), args.plan.resolve()
    initial_hashes = {path: sha(path) for path in (selection_path, cases_path, plan_path)}
    selected = read(selection_path)["selected"]
    cases = read(cases_path)["cases"]
    plan = read(plan_path)
    pins = plan_pins(plan, cases_path)
    check(len({c["id"] for c in cases}) == len(cases), "Duplicate case ID")
    rolemap = {}
    for case in cases:
        check(case["expected_final_count"] == 5 and len(case["slots"]) == 5, "Every R6 case must declare five slots")
        check(isinstance(case["request"], str) and case["request"] and isinstance(case["copy"], list)
              and all(isinstance(c, str) and c for c in case["copy"]), "Invalid request/full copy")
        action_fields(case)
        for slot in case["slots"]:
            check(slot["id"] not in rolemap, "Duplicate case role")
            check(re.fullmatch(r"[1-9][0-9]*:[1-9][0-9]*", slot["ratio"]), "Invalid target ratio")
            rolemap[slot["id"]] = (case["id"], slot["ratio"])
    check(isinstance(selected, list) and selected, "Empty selection")
    check(len({s["role"] for s in selected}) == len(selected), "Duplicate selected role")
    for item in selected:
        check(item["role"] in rolemap and item["case_id"] == rolemap[item["role"]][0], "Selected role/case differs from frozen cases")
    included = set(args.case_ids or [item["case_id"] for item in selected])
    check(included <= {c["id"] for c in cases}, "Unknown requested case")
    selected = [s for s in selected if s["case_id"] in included]
    public_cases = {}
    for case in cases:
        if case["id"] in included:
            check({s["role"] for s in selected if s["case_id"] == case["id"]} == {s["id"] for s in case["slots"]}, "Incomplete case selection: " + case["id"])
            public_cases[case["id"]] = {"request": case["request"], "copy": case["copy"], "expected_count": 5}
    ids = random.SystemRandom().sample(range(1000, 10000), len(selected))
    images, mapping, preflight, sets = [], [], [], {cid: {"members": [], "expected_count": 5} for cid in included}
    temporary = Path(tempfile.mkdtemp(prefix=".packet-", dir=ROOT))
    try:
        (temporary / "images").mkdir()
        (temporary / "reviews").mkdir()
        for item, number in zip(selected, ids):
            ident = args.id_prefix + str(number)
            source, manifest = resolve(item["final_native"]), resolve(item["manifest"])
            check(sha(source) == item["sha256"], "Selected native SHA differs: " + item["role"])
            check(sha(manifest) == item["manifest_sha256"], "Selected source manifest SHA differs: " + item["role"])
            m=read(manifest)
            canonical=ROOT/'production'/item['role']/item['stage']
            check(manifest==canonical/'manifest.json' and source==canonical/'final.png', 'Selected canonical stage differs')
            check(m['role']==item['role'] and m['case_id']==item['case_id'] and m['stage']==item['stage'], 'Selected manifest identity differs')
            check(m['final']=={'path':str(source),'sha256':item['sha256']} and (m['width'],m['height'])==(item['width'],item['height']), 'Selected manifest/native association differs')
            names = {"native": ident + "-native.png", "usage720": ident + "-usage720.png", "thumbnail320": ident + "-thumbnail320.png"}
            shutil.copyfile(source, temporary / "images" / names["native"])
            with Image.open(source) as image:
                check(image.format == "PNG", "Native must be a PNG")
                width, height = image.size
                check((width, height) == (item["width"], item["height"]), "Selected native dimensions differ")
                ratio = rolemap[item["role"]][1]
                numerator, denominator = map(int, ratio.split(":"))
                # A faithfully preserved output with a wrong ratio still needs review.
                # Mandatory-condition failures must not prevent packet creation.
                image.resize((720, round(height * 720 / width)), Image.Resampling.LANCZOS).save(temporary / "images" / names["usage720"])
                scale = 320 / max(width, height)
                image.resize((round(width * scale), round(height * scale)), Image.Resampling.LANCZOS).save(temporary / "images" / names["thumbnail320"])
            view_paths = {view: str(wave / "images" / name) for view, name in names.items()}
            image_record = dict(image_id=ident, case_id=item["case_id"], width=width, height=height, target_ratio=ratio, **view_paths)
            images.append(image_record)
            sets[item["case_id"]]["members"].append(ident)
            mapping.append(dict(item, image_id=ident, native_sha256=item["sha256"], qa_hashes={view_paths[v]: sha(temporary / "images" / name) for v, name in names.items()}))
            case = next(c for c in cases if c["id"] == item["case_id"])
            if action_fields(case):
                preflight.append({"image_id": ident, "usage720": view_paths["usage720"], "fields": list(action_fields(case))})
        random.SystemRandom().shuffle(images)
        random.SystemRandom().shuffle(preflight)
        packet = {"scope": "Anonymous complete five-poster cases. Only requests, full copy, mandatory conditions and anonymous images are disclosed.", "cases": public_cases, "images": images, "sets": sets}
        write(temporary / "packet.json", packet)
        write(temporary / "preflight.json", {"instruction": "Open this first. Actually view all listed usage720 images and save PROFILE-action-first.json before opening packet.json/full copy. Transcribe listed action fields from pixels, keep uncertainty and actual paths. Empty images requires an unchanged empty readings/viewed preflight record before packet.", "images": preflight})
        (temporary / "review-protocol.md").write_text(PROTOCOL)
        document = {"created_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "wave": args.wave, "mapping": mapping,
                    "selection": {"path": str(selection_path), "sha256": initial_hashes[selection_path]}, "plan": {"path": str(plan_path), "sha256": initial_hashes[plan_path]},
                    "cases": {"path": str(cases_path), "sha256": initial_hashes[cases_path]}, "frozen_source_pins": pins,
                    "packet_files": {str(wave / name): sha(temporary / name) for name in ("packet.json", "preflight.json", "review-protocol.md")}}
        # Recheck every source immediately before sealing; no partially usable wave remains on failure.
        check(sha(selection_path) == document["selection"]["sha256"] and sha(plan_path) == document["plan"]["sha256"]
              and sha(cases_path) == document["cases"]["sha256"], "Input changed during packet construction")
        plan_pins(plan, cases_path)
        for item in mapping:
            check(sha(resolve(item["final_native"])) == item["sha256"] and sha(resolve(item["manifest"])) == item["manifest_sha256"], "Source changed during packet construction")
        check(not wave.exists() and not private.exists(), "Wave/mapping appeared during construction; refuse overwrite")
        private.parent.mkdir(exist_ok=True)
        write(private, document)
        temporary.rename(wave)
        print(json.dumps({"wave": str(wave), "private_mapping": str(private), "images": len(images), "required_views_per_critic": len(images) * 3, "preflight_images": len(preflight)}, indent=2))
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


if __name__ == "__main__":
    main()
