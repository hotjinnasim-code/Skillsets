"""ROOT-only closed archive wrapper. No actors or score authorship."""
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parent
def main():
 p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);a=p.parse_args();archive=a.archive.resolve(strict=True)
 f=json.loads((ROOT/'planning/final-evidence.json').read_bytes());idx=json.loads((archive/'archive-index.json').read_bytes());assert idx['closed_evidence']==f and f['candidate']=='M' and f['poster_calls_closed']
 stages=['%s: PASS %d / FAIL %d / NA %d, 전체 %s'%(w,s['image_gate_counts']['PASS'],s['image_gate_counts']['FAIL'],s['image_gate_counts']['NA'],s['whole_corpus_gate']) for w,s in f['stages'].items()]
 views=json.loads((ROOT/'checks/root-whole-five-visual-views.json').read_bytes());ratio=json.loads((ROOT/'checks/root-all-stage-ratio-observations.json').read_bytes())
 lines=['# R13 M · 새 내용의 16:9 다섯 스타일 전체 종료','',
 '새 성인 건축 사진전·공간 이야기 한 요청을 고정한 M 지침으로 제작·평가했습니다. 다섯 스타일을 전체 분모로 유지합니다. '+'; '.join(stages)+'.','',
 '실제 포스터 생성 호출 %d/%d회, 독립 제작자5명, 실제 새 품질 평가 세션%d개입니다. 보정 한도는 상한이며 실제 결함과 전후 장점 변화에 따라 선택합니다. 선택 단계와 반환 크기는 아래 원보고서에 있습니다.'%(f['poster_native_attempts'],f['poster_attempt_cap'],f['actual_unique_review_sessions']),'',
 '[전체 원보고서와 원점수](raw/report.md) · [실제 다섯 선택본 갤러리](raw/gallery.html) · [기계 판독 원점수](raw/raw-score-matrices.json) · [전체 종료 기록](raw/planning/final-evidence.json) · [생성 전 M 고정본](raw/snapshots/candidate-m/SKILL.md)','',
 '16:9 원본은 사전 선언한 한 변의 최근접 정수 반올림 최대0.5픽셀 기준으로 측정합니다. 선택본 허용 밖 %d개, 미선택 반환 허용 밖 %d개입니다. 생성 뒤 카피 합성·원본 크롭·확대를 하지 않았으며 검수 축소를 생성 해상도로 세지 않습니다.'%(ratio['selected_outside_policy'],ratio['unselected_outside_policy']),'',
 '[모든 실제 반환 비율](raw/checks/root-all-stage-ratio-observations.json) · [ROOT 실제 보기 기록](raw/checks/root-whole-five-visual-views.json)','',
 '스튜디오 작품과 실제 Canva 평면 템플릿의 이미지·시점·크롭·색·레이아웃·정보·글자·재질·정서를 함께 관찰했습니다. 실제로 본 원본 파일과 원작 자체의 크롭·가림을 구별합니다. 참고 이미지를 고객 자산으로 생성 도구에 넘기거나 원작 브랜드·사람·건물을 복제하는 지시를 하지 않았습니다. 실제 동시 제작자는 가용 한도 최대3명입니다.','',
 '[전체 레퍼런스 관찰](raw/research/whole-reference-note.md) · [전체 제작 종료](raw/planning/single-five-production-closure.json)','',
 '계획 파일 작성 뒤 설계 세션 종료 확인 전에 사전 계획 검토를 시작한 ROOT 오류가 있었고, 입력 변경 때문에 해당 비품질 감사는 중단했습니다. 종료·변경 기록과 원 trace를 보존했습니다. 최종 계획을 고정한 뒤 새 계획 감사가 종료했고 실제 제작 전 모두 고정했습니다. 이 중단 감사는 이미지 품질 평가나 좋은 점수로 대체한 평가자가 아닙니다.','',
 '[사전 계획 검토 오류 이력](raw/planning/preplan-review-launch-history.json) · [M 일반화 변경 근거](raw/planning/m-runtime-change-record.json)','',
 '다섯 실제 제작 선택과 성공한 ROOT 출처 종료가 최초 품질 평가 패킷 준비·평가자 시작보다 앞섭니다. 최초와 선택본 전체 세트를 평가하며 완전히 동일한 전체 맥락·원본만 최초 세 평가 전체를 재사용합니다. 실제 새 세션 수와 재사용은 원기록에 있습니다. 낮은 점수·FAIL·NA·판독 불확실성을 평균·다수결·평가자 교체로 지우지 않고, 품질 피드백 뒤 추가 생성·재선택을 하지 않습니다. 두 패킷은 anonymous-single-five로 버전명을 숨겼지만 사례·경로 식별자는 보입니다.','',
 'ROOT는 case/계획을 먼저 알고 실제 보기를 기록했으므로 독립 블라인드 점수가 아닙니다. 동일 파일을 두 단계에서 쓴 경우 새 열람·점수로 중복 세지 않습니다. 출처는 호출자의 리터럴 반환 식별자·저장 명령·새 CLI 세션·캐시·manifest·해시 연결입니다. 보존 trace에 직접 native MCP 호출/반환 이벤트가 없어 직접 도구 이벤트 인증이나 제작 주체 증명을 주장하지 않습니다.','',
 '[원본 바이트와 식별자 색인](archive-index.json) · [두 단계 이식·보관 재검증](checks/archive-replay.json)','',
 '전체 원본 파일·숨김·빈 디렉터리를 제외 없이 보관하며 원래 호스트/알 수 없는 외부 경로의 읽기·메타데이터 접근을 차단한 두 단계 재생, 원점수·raw 인벤토리·갤러리와 지역 링크를 확인합니다. 경로·symlink 음성 사례13개도 외부 접근 없이 거부합니다. 보관 검사로 새 제작자·평가자·이미지를 실행하지 않습니다.','',
 '닫힌 R12 뒤 M 일반 지침, 새 내용·계획·레퍼런스가 함께 달라졌습니다. 단일 제한된 전이 사례이며 M만의 인과 효과·통계적 성공률·향후 모든 요청·장르의 품질을 보장하지 않습니다. 고객 자산 보존과 지정 한 장의 후속 편집은 이번 사례에서 시험하지 않았습니다.']
 with (archive/'report.md').open('x') as h:h.write('\n'.join(lines).rstrip()+'\n')
 (archive/'checks').mkdir(exist_ok=True);print(json.dumps({'wrapper':str(archive/'report.md'),'selected_set_gate':f['stages']['selected']['whole_corpus_gate'],'new_native_calls_or_critics':0}))
if __name__=='__main__':main()
