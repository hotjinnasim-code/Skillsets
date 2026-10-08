#!/usr/bin/env python3
"""Create an honest portable report/gallery, including partial review evidence.

Image links can use sealed selection metadata when review records are absent;
such metadata is never represented as an accepted critic viewing or image PASS.
"""
import argparse
import html
import json
from pathlib import Path

DIMS = ("content_form", "hierarchy", "typography", "space", "image_material", "emotion_control", "ai_slop")
NAMES = ("내용과 형태", "정보 계층", "타이포그래피", "공간", "이미지·재질", "정서·제어", "AI 슬롭")


def read(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError, TypeError):
        return {} if default is None else default


def values(value):
    return value if isinstance(value, list) else []


def mapping(value):
    return value if isinstance(value, dict) else {}


def unique_text(items):
    return list(dict.fromkeys(str(x) for x in items))


def build(archive):
    root = Path(archive).resolve()
    evidence = read(root / "raw/planning/final-evidence.json")
    calls = read(root / "raw/planning/calls-closed.json")
    registry = read(root / "raw/planning/production-closed-registry.json")
    index = read(root / "archive-index.json")
    lookup = {x["source_absolute"]: x["archive_relative"] for x in values(index.get("files")) if isinstance(x, dict)}

    def link(path):
        return lookup.get(path) if isinstance(path, str) else None

    def anchor(path, label):
        target = link(path)
        return f'<a href="{html.escape(target, quote=True)}">{html.escape(label)}</a>' if target else html.escape(label + " (자료 없음)")

    def md_link(path, label):
        target = link(path)
        return f'[{label}]({target})' if target else label + " (자료 없음)"

    images, sets = evidence.get("images", {}), evidence.get("sets", {})
    expected = evidence.get("expected_image_count", len(images))
    selected_count = evidence.get("selected_image_count", sum(isinstance(x.get("selected"), dict) for x in images.values()))
    initial_count = evidence.get("initial_returned_image_count", sum(isinstance(x.get("initial_selection"), dict) for x in images.values()))
    targeted_native_hashes = {row.get("sha256") for image in images.values() for row in (image.get("initial_selection"), image.get("selected")) if isinstance(row, dict) and row.get("sha256")}
    first_pass, final_pass = evidence.get("firstpass_image_pass_count", 0), evidence.get("final_image_pass_count", 0)
    final_counts = {gate: sum(x.get("final_image_gate") == gate for x in images.values()) for gate in ("PASS", "FAIL", "NOT_ASSESSABLE")}
    resumed = unique_text(values(registry.get("fresh_context_exception_roles")) + [x.get("role") for x in values(registry.get("roles")) if isinstance(x, dict) and x.get("resumed_worker_name")])
    accepted_sessions = set()
    available_sessions = set()
    for case in sets.values():
        for procedures in case.get("review_procedure", {}).values():
            if not isinstance(procedures, dict):
                continue
            for proc in procedures.values():
                if not isinstance(proc, dict):
                    continue
                session = proc.get("cli_session_id")
                if isinstance(session, str) and session:
                    available_sessions.add(session)
                    if proc.get("cli_assignment_valid") is True:
                        accepted_sessions.add(session)
    terminal_gate = evidence.get("predeclared_core_diversity_gate", "NOT_ASSESSABLE")
    integrity = evidence.get("recorded_evidence_integrity", "FAIL")
    title = f"덕테이프 포스터: 추가 {expected}장 검증"
    lines = ["# " + title, "", f'고정한 메인 커밋: `{evidence.get("source_commit", "자료 없음")}`. 네 요청의 모든 예정 역할을 포함한다. 선택 원본은 {selected_count}/{expected}장, 반환된 최초 원본은 {initial_count}/{expected}장이다. 이전 평가 이미지나 다른 스킬 버전을 새 표본에 섞지 않았다.', "",
        f'최종 사전 선언 핵심·다양성 게이트: **{terminal_gate}**. 기록·해시 무결성: **{integrity}**. 유효한 전체 평가에서 확인된 이미지 단독 통과는 최초 **{first_pass}/{expected}**, 제한된 자체 보정과 선택 후 **{final_pass}/{expected}**이다. **NOT_ASSESSABLE은 평가 절차·자료가 부족하거나 무효인 경우이며 통과로 세지 않는다.** 세트 다양성은 별도로 모두 통과해야 한다. 이 수치는 요청 문맥에 묶인 관찰값이며 향후 성공률이 아니다.', "",
        f'최종 이미지 판정은 **통과 {final_counts["PASS"]}장 · 품질 미통과 {final_counts["FAIL"]}장 · 판정 불가 {final_counts["NOT_ASSESSABLE"]}장**이다. 판정 불가를 이미지 품질 실패로 합치지 않는다. 개별 원점수와 미수락 이유는 모든 이미지에 남겼다.', "",
        f'보존된 이미지·평가자 기록은 최초 {evidence.get("firstpass_image_critic_records", 0)}개, 최종 {evidence.get("final_image_critic_records", 0)}개다. 점수 관찰은 각각 {evidence.get("firstpass_score_observations", 0)}개와 {evidence.get("final_score_observations", 0)}개이며, 부분 자료를 완전한 60개 기록으로 채우지 않는다.', "",
        f'최초·최종의 완전한 세트에 배정한 서로 다른 네이티브 바이트는 {len(targeted_native_hashes)}개다. 같은 선택 원본이 두 단계에 포함되는 경우도 있다. 모든 미선택 보정본까지 외부 평가자가 검토했다고 주장하지 않으며, 해당 원본과 제작 검수·선택 이력은 별도로 보존한다.', "",
        '[전체 갤러리](gallery.html) · [전체 결합 평가 자료](raw/planning/final-evidence.json) · [기록 조회 인덱스](archive-index.json)', "",
        '| 요청 | 최초 세트 | 최종 세트 | 최초/최종 이미지 통과 | 기록된 최종 다양성 |', '| --- | --- | --- | --- | --- |']
    for cid, case in sets.items():
        rows = [images.get(role, {}) for role in case.get("roles", [])]
        ip = sum(x.get("initial_image_gate") == "PASS" for x in rows)
        fp = sum(x.get("final_image_gate") == "PASS" for x in rows)
        diversity = "/".join(str(x.get("diversity", "자료 없음")) for x in values(case.get("final_reviewers"))) or "자료 없음"
        lines.append(f'| {case.get("name", cid)} | {case.get("initial_case_gate", "NOT_ASSESSABLE")} | {case.get("final_case_gate", "NOT_ASSESSABLE")} | {ip}/{len(rows)} → {fp}/{len(rows)} | {diversity} |')
    sections = []
    cards_count = 0
    for cid, case in sets.items():
        cards = []
        for role in case.get("roles", []):
            cards_count += 1
            item = images.get(role, {})
            selected = item.get("selected") or {}
            initial = item.get("initial_selection") or {}
            binding = item.get("binding") or {}
            initial_binding = item.get("initial_binding") or {}
            ordinary_pin = item.get("ordinary_selection") or {}
            ordinary_link = link(ordinary_pin.get("path"))
            ordinary = mapping(read(root / ordinary_link)) if ordinary_link else {}
            observations = values(item.get("reviewers"))
            initial_gate = item.get("initial_image_gate", "NOT_ASSESSABLE")
            final_gate = item.get("final_image_gate", "NOT_ASSESSABLE")
            assessable = item.get("binding_assessable") is True and final_gate != "NOT_ASSESSABLE"
            observation_status = "유효한 평가 기록" if assessable else "미수락·부분 관찰: 통과 판정에 사용하지 않음"
            native_path = binding.get("source_native") or selected.get("final_native")
            initial_path = initial_binding.get("source_native") or initial.get("final_native")
            qa_path = binding.get("views", {}).get("usage720", {}).get("path")
            qa_link, native_link = link(qa_path), link(native_path)
            preview = f'<a href="{html.escape(native_link or qa_link, quote=True)}"><img src="{html.escape(qa_link, quote=True)}" alt="{html.escape(role, quote=True)} 선택 포스터" loading="lazy"></a>' if qa_link else '<p>축소 보기 자료 없음. 선택 원본 링크를 확인하세요.</p>'
            located, residuals = [], []
            for record in observations:
                if not isinstance(record, dict):
                    residuals.append(str(record))
                    continue
                for dimension, score in mapping(record.get("scores")).items():
                    if type(score) is int and score < 4:
                        located.append(f'{record.get("profile", "평가자 미상")}/{dimension}={score}: {mapping(record.get("evidence")).get(dimension, "위치 자료 없음")}')
                mandatory = mapping(record.get("mandatory"))
                residuals.extend(values(record.get("residuals")) + values(mandatory.get("issues")) + values(mandatory.get("uncertainties")))
            residuals.extend(values(ordinary.get("residuals")))
            if not assessable:
                for error in values(case.get("review_integrity_errors", {}).get("final")):
                    residuals.append("절차·무결성: " + str(error))
            notes = unique_text(located + residuals)
            score_rows = ""
            for record in observations:
                if not isinstance(record, dict):
                    continue
                score_rows += '<tr><th>' + html.escape(str(record.get("profile", "자료 없음"))) + '</th>' + ''.join('<td>' + html.escape(str(mapping(record.get("scores")).get(d, "—"))) + '</td>' for d in DIMS) + '</tr>'
            if not score_rows:
                score_rows = '<tr><td colspan="8">평가 기록 없음 — NOT_ASSESSABLE</td></tr>'
            evidence_list = ''.join('<li>' + html.escape(t) + '</li>' for t in notes) or '<li>기록된 잔여 관찰 없음. 제작 주체·인쇄 적합성을 보증하지 않는다.</li>'
            dimensions = f'{selected.get("width", "?")} × {selected.get("height", "?")}'
            provenance = "봉인 선택 메타데이터로 표시하며 평가자의 조회를 뜻하지 않는다." if item.get("binding_provenance") == "sealed_selection_metadata_only" else "선택본과 평가 바인딩의 경로·해시 연결을 검사했다."
            cards.append(f'<article><h3>{html.escape(role)} · {html.escape(final_gate)}</h3>{preview}<p>{dimensions} · {html.escape(str(selected.get("stage", "자료 없음")))} · {ordinary.get("call_count", "자료 없음")}회 호출</p><p>{anchor(native_path, "선택 원본")} · {anchor(initial_path, "최초 원본 (" + initial_gate + ")")} · {anchor(ordinary_pin.get("path"), "보정·선택 기록")}</p><p>{html.escape(provenance)}</p><details><summary>{html.escape(observation_status)}</summary><table><tr><th>평가자</th>' + ''.join('<th>' + html.escape(n) + '</th>' for n in NAMES) + f'</tr>{score_rows}</table><ul>{evidence_list}</ul></details></article>')
            lines.extend(["", f'### {role}: {initial_gate} → {final_gate}', md_link(native_path, dimensions + " 선택 원본") + " · " + md_link(initial_path, "최초 원본") + " · " + md_link(ordinary_pin.get("path"), "선택·보정 기록"), "", observation_status + ". " + provenance, "", '| 평가자 | ' + ' | '.join(NAMES) + ' |', '| --- | ' + ' | '.join(['---'] * 7) + ' |'])
            for record in observations:
                if isinstance(record, dict):
                    lines.append('| ' + str(record.get("profile", "자료 없음")) + ' | ' + ' | '.join(str(mapping(record.get("scores")).get(d, "—")) for d in DIMS) + ' |')
            if not observations:
                lines.append('| 자료 없음 | ' + ' | '.join(['—'] * 7) + ' |')
            lines.extend(["", "잔여 관찰:"] + ["- " + t for t in notes])
            if not notes:
                lines.append('- 기록된 잔여 관찰 없음. 제작 주체·인쇄 적합성을 보증하지 않는다.')
        sections.append(f'<section id="{html.escape(cid, quote=True)}"><h2>{html.escape(case.get("name", cid))} · 최종 세트 {html.escape(case.get("final_case_gate", "NOT_ASSESSABLE"))}</h2><p>가까운 쌍·낮은 점수·절차 실패·평가자 간 차이는 전체 결합 자료에 보존했습니다.</p><div class="grid">' + ''.join(cards) + '</div></section>')
    exceptions = ", ".join(resumed) if resumed else "등록된 예외 없음"
    attempts = calls.get("recorded_attempts", len(values(calls.get("records"))))
    failed_attempts = sum(x.get("kind") == "failed native attempt" for x in values(calls.get("records")) if isinstance(x, dict))
    lines.extend(["", "## 검증 방법과 범위", "",
        f'제작은 {registry.get("logical_roles", expected)}개 역할로 수행했다. 모든 제작자가 새 문맥이었다고 주장하지 않는다. 제작 폐쇄 레지스트리에 기록된 기존 작업자 재개 예외는 **{exceptions}**다. 이 역할들은 이전 작업의 문맥을 지울 수 없는 상태에서 새 역할을 맡았다. [제작 폐쇄 레지스트리](raw/planning/production-closed-registry.json)에 역할·재개 작업자·선택 핀이 남아 있다. 환경 한도 안에서 나누어 작업했으며 실제 호출 구간의 최고 동시 수는 {calls.get("actual_recorded_interval_peak", "자료 없음")}였다.', "",
        f'새 R6 네이티브 도구 시도는 {attempts}/60회, 실패한 도구 시도는 {failed_attempts}회였다. 최초 생성 1회와 이미지당 최대 자체 보정 2회만 허용했다. 사용하지 않은 잔여 한도는 종료했으며 이전 라운드의 닫힌 한도를 재개하지 않았다.', "",
        f'모든 일반 제작 검수와 선택을 닫은 뒤 독립 평가를 진행한다. 계획된 **24개 독립 평가는 이전 문맥을 전달하지 않는 새 CLI 세션**으로 실행하며 재개·포크를 사용하지 않는다. 현재 증거에 남은 고유 CLI 세션은 {len(available_sessions)}개, 런타임 배정 유효성이 확인된 세션은 {len(accepted_sessions)}개다. 제작자의 재개 예외와 새 평가 세션은 별개다. 완전한 최초 세트와 실제 바이트가 바뀐 최종 세트에는 각각 세 평가자가 필요하며, 변경된 최종 세션 ID는 최초 세 개와 모두 달라야 한다. 다섯 역할의 원본 SHA가 모두 같은 경우에만 최초 평가 전체를 재사용한다. 외부 점수로 이미지를 추가 생성하거나 스킬을 수정하지 않는다.', "",
        '증거 연결은 폐쇄 기록의 최초·최종 선택 핀, 정확한 다섯 역할과 단계, 원본·매니페스트·원천 파일 해시, 평가 요약과 수락된 CLI 세션을 대조한다. 기록 개수만으로 평가를 수락하지 않는다. 누락·무효 평가의 낮은 점수와 원시 실패는 보존하지만 이미지 PASS나 통과 수에 넣지 않는다.', "",
        '원본/720px 폭/320px 긴 변의 조회 기록과 720px 행동 정보의 카피 제공 전 전사 절차를 검증 대상으로 삼았다. **파일 해시와 세션 출처 검증은 자료의 연결을 입증하며, 실제 시각 조회·전사·읽는 순서는 별도의 평가자 진술이다.** CLI 흔적에 기계적으로 드러난 사건 이외의 시각 판단이나 순서를 파일 해시만으로 증명하지 않는다. 메타데이터로 만든 갤러리 링크도 평가자가 그 이미지를 실제 봤다는 뜻은 아니다.', "",
        '게이트는 변경하지 않았다. 필수 조건 통과와 내용·타이포그래피·이미지/재질·AI 슬롭 각 4 이상을 유효한 세 평가자 모두에게 요구하며 세트 다양성도 각각 4 이상이어야 한다. 일곱 점수, 4 미만 비핵심 점수, 구체적인 위치와 평가자 차이를 평균 없이 남겼다. 생성한 이미지로 인간 제작을 판별하지 않으며 클레이 3D와 강한 색의 요청은 실제 구현으로 평가한다.', "",
        '이 표본은 네 요청에 묶인 20장이다. 사용자 제공 로고·실제 화면·외부 사진 보존, 모든 장르, 후속 부분 수정, 실제 제품 기능, 인쇄 결과, 미래의 보편적 품질을 검증하지 않았다. 최대 지원 해상도는 요청했지만 실제 반환 픽셀만 기록한다. 원본은 코드로 바꾸지 않았고 QA 축소 보기만 만들었다. 새 외부 레퍼런스 조사를 수행했다는 주장도 하지 않는다.', "",
        '모든 최초·보정·미선택 원본과 이용 가능한 원시 실패·평가 자료를 아카이브에 보존한다. 원래 절대 경로는 원본 기록에 남고 archive-index.json이 상대 경로의 해시 파일에 대응한다. 평가 자료가 부분적이어도 기대한 이미지 역할을 갤러리에서 삭제하지 않는다. 현재 라운드는 최초 20장이 모두 반환되었으며, 일반 유틸리티의 실패한 최초 생성 봉인 분기는 지원하지 않는다. 해당 분기를 이후 선택 이미지로 메우지 않는다.', ""])
    (root / "report.md").write_text("\n".join(lines) + "\n")
    css = 'body{font-family:system-ui,sans-serif;margin:0;background:#f4f4f1;color:#222}main{max-width:1540px;margin:auto;padding:32px}h1{font-size:30px}h2{margin-top:50px}.grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:18px}article{background:white;padding:14px;border:1px solid #ddd}article h3{font-size:14px}img{width:100%;height:360px;object-fit:contain;background:#fafafa}p,li,summary{font-size:13px;line-height:1.7}table{font-size:10px;border-collapse:collapse;width:100%}td,th{padding:4px;border:1px solid #ddd}details{overflow:auto}a{color:#16456c}nav a{margin-right:20px}@media(max-width:1100px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:650px){.grid{grid-template-columns:1fr}main{padding:18px}}'
    body = f'<h1>{html.escape(title)}</h1><p>최종 전체 게이트 {html.escape(terminal_gate)} · 최초 단독 통과 {first_pass}/{expected} → 선택 후 {final_pass}/{expected}. 세트 다양성 별도. 선택 원본 {selected_count}장, 최초 원본 {initial_count}장.</p><p>통과 {final_counts["PASS"]}장 · 품질 미통과 {final_counts["FAIL"]}장 · 판정 불가 {final_counts["NOT_ASSESSABLE"]}장. 판정 불가를 통과 또는 품질 실패로 합치지 않습니다.</p><p><a href="report.md">검증 보고서</a> · <a href="raw/planning/final-evidence.json">전체 결합 증거</a> · <a href="archive-index.json">원본 조회 인덱스</a></p><nav>' + ''.join(f'<a href="#{html.escape(cid, quote=True)}">{html.escape(case.get("name", cid))}</a>' for cid, case in sets.items()) + '</nav>' + ''.join(sections)
    (root / "gallery.html").write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(title) + '</title><style>' + css + '</style><main>' + body + '</main></html>')
    return {"report": str(root / "report.md"), "gallery": str(root / "gallery.html"), "cards": cards_count, "pixel_edits": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.archive)))


if __name__ == "__main__":
    main()
