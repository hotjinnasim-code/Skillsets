"""ROOT-only known-case archive wrapper; no score authorship."""
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parent
def main():
 p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);a=p.parse_args();archive=a.archive.resolve(strict=True)
 f=json.loads((ROOT/'planning/final-evidence.json').read_bytes());idx=json.loads((archive/'archive-index.json').read_bytes());assert idx['closed_evidence']==f and f['candidate']=='N' and f['poster_calls_closed']
 lines=['# R14 N · 사용자 제외 조건을 포함한 다섯 스타일 전체 종료','', '닫힌 R13 뒤 같은 건축 사진전·공간 이야기 16:9 요청에 단색/유사 단색·고딕 제목/안내 중심 템플릿의 제외를 명시해 한 요청·다섯 전체 스타일로 새 실행했습니다. 알려진 내용의 개발 검증이며 다음20장 캠페인이나 모든 요청의 품질 보장은 아닙니다.','']
 for w,s in f['stages'].items():lines.append('%s: PASS %d / FAIL %d / NA %d, 전체 %s.'%(w,s['image_gate_counts']['PASS'],s['image_gate_counts']['FAIL'],s['image_gate_counts']['NA'],s['whole_corpus_gate']))
 lines+=['','실제 생성 %d/15회, 독립 제작자5명, 새 품질 평가 세션%d개. 가용 한도의 최대 동시 제작자3명입니다.'%(f['poster_native_attempts'],f['actual_unique_review_sessions']),'','[전체 원보고서와 원점수](raw/report.md) · [실제 선택본 갤러리](raw/gallery.html) · [전체 종료](raw/planning/final-evidence.json) · [동결 N 지침](raw/snapshots/candidate-n/SKILL.md) · [원점수 행렬](raw/raw-score-matrices.json)','', '[실제 사용자 조건과 원문](raw/planning/literal-landscape-request.txt) · [생성 전 계획과 방법 고정](raw/planning/candidate-n-pre-generation-freeze.json) · [참고 원본과 전체 관계 관찰](raw/research/current-study/whole-reference-note.md) · [N 개발 조언과 채택 범위](raw/development-context/n-adoption/adoption.json)','', '원본을 자르거나 확대하지 않았습니다. 16:9 한 변의 최근접 정수 반올림 허용은 생성 전 선언한 최대0.5픽셀이며 명시적 픽셀 크기 요청에 적용하지 않습니다. 반환 원본 크기와 검수 축소 크기는 별개입니다.','', '[모든 실제 반환 비율](raw/checks/root-all-stage-ratio-observations.json) · [실제 전체 제작 종료](raw/planning/single-five-production-closure.json)','', '세 평가자 각각 필수 조건 PASS, 일곱 점수 각각4 이상과 전체 다양성4 이상을 요구합니다. 모든 다섯 장을 분모로 유지하고 평균·다수결·평가자 교체로 FAIL/NA를 지우지 않습니다. 원점수·원본·미선택 보정·실패를 제외 없이 보관합니다. 평가 뒤 재생성·재선택은 없습니다.','', '[원본 바이트 색인](archive-index.json) · [다른 호스트를 차단한 두 단계 보관 재생](checks/archive-replay.json)','']
 lines+=['- '+x for x in f['limits']]
 with (archive/'report.md').open('x') as h:h.write('\n'.join(lines).rstrip()+'\n')
 (archive/'checks').mkdir(exist_ok=True);print(json.dumps({'wrapper':str(archive/'report.md'),'selected_set_gate':f['stages']['selected']['whole_corpus_gate'],'new_native_calls_or_critics':0}))
if __name__=='__main__':main()
