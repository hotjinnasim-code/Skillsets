"""ROOT-only wrapper from closed evidence; never launch actors or invent scores."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True)
    args = parser.parse_args()
    final = json.loads((ROOT/'planning/final-evidence.json').read_bytes())
    archive = args.archive.resolve(strict=True)
    assert final['poster_calls_closed'] and final['candidate'] == 'L'
    index = json.loads((archive/'archive-index.json').read_bytes())
    assert index['closed_evidence'] == final
    stage_rows = []
    for wave in ('initial', 'selected'):
        stage = final['stages'][wave]
        counts = stage['image_gate_counts']
        stage_rows.append(f"{wave}: PASS {counts['PASS']} / FAIL {counts['FAIL']} / NA {counts['NA']}, 전체 {stage['whole_corpus_gate']}")
    selected = final['stages']['selected']['whole_corpus_gate']
    verdict = '선택본 전체가 이 사례의 기준을 통과했습니다.' if selected == 'PASS' else '선택본 전체는 이 사례의 기준을 통과하지 못했습니다.'
    lines = [
        '# R12 L · 새 내용의 16:9 다섯 스타일 전체 종료', '',
        '새 성인 업사이클링·완성품 나눔 행사 한 요청을 L 지침으로 제작·평가했습니다. 다섯 스타일 전체를 분모로 유지했습니다. '+ '; '.join(stage_rows)+'. '+verdict, '',
        f"실제 포스터 생성 호출 {final['poster_native_attempts']}/{final['poster_attempt_cap']}회, 독립 제작자5명, 새 평가 세션{final['actual_unique_review_sessions']}개입니다. 다섯 선택본은 각각1672×941이며, M1은초안, 나머지 네 방향은repair-2를 선택했습니다. 생성 뒤 카피 합성·원본 크롭·확대를 하지 않았습니다. 생성 호출의 반환 실패0회와 모든 중간 결과의 조건 통과는 별개이며, 미선택 M2 repair-1의1671×941 비율 허용 실패도 보존합니다.", '',
        '[전체 원보고서와 원점수](raw/report.md) · [실제 다섯 선택본 갤러리](raw/gallery.html) · [기계 판독 원점수](raw/raw-score-matrices.json) · [전체 종료 기록](raw/planning/final-evidence.json) · [생성 전 L 고정본](raw/snapshots/candidate-l/SKILL.md) · [모든 반환의 비율](raw/checks/root-all-stage-ratio-observations.json)', '',
        '새 전체 스튜디오 작품과 실제 Canva 템플릿을 이미지 표현·시점·크롭·색·레이아웃·정보·글자·재질·정서에서 관찰하고 현재 내용에 맞춰 설계했습니다. 원작의 카피·구도·서체를 복제하거나 조사 이미지를 고객 자산으로 생성 도구에 전달하지 않았습니다. 실제 제작자 동시 실행은 최대3명으로, 다섯 역할 모두 실행과 실제 동시 실행을 구별합니다.', '',
        '[전체 레퍼런스 관찰](raw/research/whole-reference-note.md) · [제작 종료](raw/planning/single-five-production-closure.json) · [ROOT 실제 보기 기록](raw/checks/root-whole-five-visual-views.json)', '',
        '제작자와 성공한 ROOT 출처 종료가 최초 평가 패킷 준비와 실제 평가자 시작보다 앞섭니다. ROOT가 도움말 지원 여부를 확인하지 않고 실행한 도우미가 제작 중3/5 부분 갤러리를 먼저 만든 오류는 별도 이력에 원바이트로 보존했습니다. 이 부분 갤러리는 평가 입력이나 완전한 세트 증거로 쓰지 않았으며, 정식5/5 갤러리는 성공한 제작 종료 뒤 만들었습니다.', '',
        '[부분 갤러리 준비 오류 이력](raw/checks/gallery-preparation-history/premature-help-invocation.json) · [반환 메타데이터 별칭 교정](raw/checks/source-alias-history/before-critic-result-hints-alias-validation.json)', '',
        '두 단계의 평가자는 원관찰과 호환 출력을 자기 새 세션이 닫히기 전에 기록했습니다. 낮은 점수·원래 FAIL·NA·판독 불확실성을 평균·다수결·평가자 교체로 지우지 않았습니다. 두 단계 모두 예정된 전체 세 평가이며, 평가 피드백 뒤 추가 생성·재선택은 없습니다. 버전명은두 패킷에서anonymous-single-five로 숨겼지만 사례 식별자는 보입니다. 역사적 R11 패킷에는K가 보여 R11을 완전히 버전명을 숨긴 평가라고 주장하지 않습니다.', '',
        '출처는 호출자의 리터럴 반환 식별자·저장 명령·새 CLI 세션·캐시·manifest와 정확한 해시로 연결합니다. 보존한 CLI trace에 직접 native MCP 호출·반환 이벤트가 없어 직접 도구 이벤트 인증까지 주장하지 않습니다. 의미상 이미지 열람은 평가자의 진술입니다. ROOT는 원문·계획을 먼저 알고27개 고유 단계 파일을 실제 보았으며 M1의 동일한3개 보기를 선택 단계에 재사용했습니다. 이것을30회의 새 열람이나 독립 점수로 세지 않습니다.', '',
        '[정확한 바이트와 원본 식별자 색인](archive-index.json) · [보관·두 단계 이식 재검증](checks/archive-replay.json)', '',
        '전체 원본 트리의 파일·숨김·빈 디렉터리를 제외 없이 보관합니다. 보관 재검증은 원래 호스트와 알 수 없는 외부 경로의 읽기·메타데이터 접근을 차단하고 두 실제 단계의 동결 v4·출처·원관찰 연결, 원점수, 전체 raw 인벤토리와 갤러리5이미지·20참조, 보고서의 지역 링크를 확인합니다. 경로·symlink 음성 사례13개도 외부 접근 없이 거부합니다. 새 제작자·평가자·이미지 호출을 실행하지 않습니다.', '',
        '완전히 종료된 R11 뒤의 새 요청 한 건으로 L 지침과 사례별 계획·참고 자료가 함께 달라졌습니다. 이를 L만의 인과 효과, 통계적 성공률, 향후 모든 요청·장르의 품질 또는 AI 제작 주체 인증으로 일반화하지 않습니다. 고객 자산 보존과 지정 이미지 편집은 이번 사례에서 시험하지 않았습니다.', ''
    ]
    with (archive/'report.md').open('x', encoding='utf-8') as handle:
        handle.write('\n'.join(lines)+'\n')
    (archive/'checks').mkdir(exist_ok=True)
    print(json.dumps({'wrapper':str(archive/'report.md'),'selected_set_gate':selected,'new_native_calls_or_critics':0}))


if __name__ == '__main__':
    main()
