"""Update user-facing docs from the actual fully closed last five, without rescoring."""
from pathlib import Path
import json
TASK=Path(__file__).resolve().parents[1]
REPO=TASK/'Skillsets'
closure=json.loads((TASK/'work/round21/planning/full-five-closure.json').read_bytes())
assert closure['candidate']=='Y' and closure['all_actors_closed'] and closure['requested_images']==5
p=REPO/'README.md';s=p.read_text();assert '| [R21 / Y]' not in s
old='이 새 보관에는 조사 작품 이미지나 글꼴 바이너리를 복사하지 않았습니다.'
new='[Y 텍스트 위계 개발](evals/ducttape-poster/design-development-y/report.md)은 실제 문구의 역할·명확한 Title·서체 조화를 강화한 일반 지침과 변경 전후 계획, 닫힌 R21 결과를 연결합니다. 이 새 개발·조사 보관에는 조사 작품 이미지나 글꼴 바이너리를 복사하지 않았으며, 과거 원기록의 패키징 범위와는 구별합니다.'
assert old in s;s=s.replace(old,new)
i=closure['waves']['initial'];f=closure['waves']['selected'];c=f['image_gate_counts']
row=f"| [R21 / Y](evals/ducttape-poster/round21/report.md), 같은 식물 마켓의 텍스트 위계·서체 개발 | {c['PASS']} / {c['FAIL']} / {c['NA']} | {f['set_gate']} |"
needle='| [R20 / W](evals/ducttape-poster/round20/report.md), 같은 식물 마켓의 최초 조판 설계 개발 | 0 / 0 / 5 | NA, 통신 오류 |'
assert needle in s;s=s.replace(needle,needle+'\n'+row)
parts=[]
for label,w in [('최초',i),('선택',f)]:
 d=w['image_gate_counts'];div=w.get('diversity_original',{})
 diversity='·'.join(str(div.get(k,'NA')) for k in ['editorial','craft','portfolio'])
 parts.append(f"{label} {d['PASS']} PASS / {d['FAIL']} FAIL / {d['NA']} NA, 절차 {w['procedure_gate']}, 유효 원점수 {w['counts']['valid_integer_1_to_5_score_values']} / 105개, 다양성 {diversity}")
paragraph='R21은 '+'; '.join(parts)+f"입니다. 네이티브 호출은 {closure['native_calls']}회, 보정은 {closure['repair_calls']}회, 최초본 선택과 보정 없이 종료한 최초본은 각각 {closure['initial_selected']}개·{closure['initial_retained_without_repairs']}개입니다. 최초·선택의 새 평가 프로세스는 각각 {i['new_critic_processes']}개·{f['new_critic_processes']}개이며 전체 원점수·불확실성·통신 오류와 해당 단계의 fresh·reuse·UNREADY 상태를 보존합니다. 같은 요청에 대한 개발 관찰이며 새 요청 전반의 품질 보장은 아닙니다."
marker='개별 PASS는 필수 조건';assert marker in s;s=s.replace(marker,paragraph+'\n\n'+marker)
s=s.replace(' 최신 후보의 검증은 완전히 닫은 뒤 추가합니다.','')
p.write_text(s)
body='''작은 제목과 경쟁하는 보조 문구, 흩어진 본문·안내, 매체만 바꾼 같은 구도로 수렴하던 덕테이프 포스터를 개선합니다. 실제 문구를 eyebrow·Title·Subtitle·body copy·footer의 기능으로 설계하고, Title을 즉시 인지되는 주된 타이포그래피 앵커로 만듭니다. 상대적 크기·무게·대비·여백과 한글·라틴·숫자의 서체 조화를 먼저 선택하며 본문에서 다음 안내로 이어지는 관계를 이미지의 큰 형태와 함께 설계합니다.

- 독립 제작자 다섯 역할이 가용 동시 한도 안에서 서로 다른 전체 방향을 제작합니다. 사용자 수량·스타일·비율·구도·자산 보존 조건과 한 장의 후속 수정 범위를 유지합니다.
- 공식 수상 아카이브 200개 이미지와 스튜디오 원본 37개의 실제 관찰을 22개 구성 아이디어와 선택적 출처 색인으로 축적했습니다. 작품·시리즈·관찰 범위·제외 사례를 구별하고 매 제작마다 원작을 다시 읽도록 요구하지 않습니다. Canva는 친숙한 정보 관계의 부분 참고입니다.
- 복잡한 본문과 안내는 기존 글꼴·렌더러가 있을 때 실제 카피와 실질적인 이미지 형태로 새 계획 스케치를 만듭니다. 단순 문구·무문자·런타임이 없는 요청은 네이티브 명세로 생성합니다. 최종 포스터는 내장 이미지 도구로 제작하며 폰트 파일 적용이나 보편적인 품질을 보장하지 않습니다.
- 단색·유사 단색·분할 색 바탕의 큰 고딕 제목·정보판에 부가물을 붙인 기본 템플릿, 클레이·장난감 패키지와 큰 오브젝트·큰 제목·작은 하단 안내의 반복을 기본값에서 제외합니다. 명시적 사용자 표현과 구성은 해당 범위에서 우선합니다.

검증은 한 요청의 다섯 장씩 완전히 종료합니다. 세 독립 평가자 각각의 일곱 항목 모두 4 이상, 전체 다양성 각각 4 이상과 필수 조건이라는 기준을 유지하고 최초/선택 이미지·모든 시도·실패·낮은 원점수·불확실성·실제 세션·입력 해시를 보존했습니다. 평가 뒤 재생성·재선택·평가자 교체를 하지 않았습니다.

'''+paragraph+'''

스킬 구조 검증과 문서·런타임 링크 확인을 완료했습니다. 자체 계획 가이드 렌더러의 기존 27개 테스트는 모두 통과했으며 이 최종 위계 변경은 렌더러 코드를 바꾸지 않습니다. 런타임은 R21 생성 전에 고정한 Y 스냅샷과 일치합니다. 자료량, 계획 가이드의 실제 폰트, 정적 검사와 한 요청의 결과는 보편적인 하이엔드 품질·제작 주체 판별·지침 하나의 인과 효과를 입증하지 않습니다.
'''
(TASK/'drafts/ducttape-poster-final-pr-body.draft.md').write_text(body)
print({'README_updated':True,'PR_body_written':True,'selected_counts':c,'set_gate':f['set_gate']})
