#!/usr/bin/env python3
"""Create a portable report/gallery from exact archived evidence; never modifies images."""
from pathlib import Path
import argparse,html,json
p=argparse.ArgumentParser(description=__doc__);p.add_argument('archive',type=Path);a=p.parse_args();r=a.archive.resolve()
read=lambda x:json.loads(Path(x).read_text());e=read(r/'raw/planning/final-evidence.json');calls=read(r/'raw/planning/calls-closed.json');index=read(r/'archive-index.json');lookup={x['source_absolute']:x['archive_relative'] for x in index['files']}
link=lambda x:lookup[x];esc=lambda x:html.escape(str(x));dims=['content_form','hierarchy','typography','space','image_material','emotion_control','ai_slop']
names=['내용과 형태','정보 계층','타이포그래피','공간','이미지·재질','정서·제어','AI 슬롭']
lines=['# 덕테이프 포스터: 추가 20장 검증','',f'고정한 메인 커밋: `{e["source_commit"]}`. 새로운 네 요청에서 각 다섯 제작자가 한 장씩 맡은 **20개 역할을 모두 포함**했다. 이전 평가 이미지나 다른 스킬 버전을 섞지 않았다.','',f'최종 사전 선언 핵심·다양성 게이트: **{e["predeclared_core_diversity_gate"]}**. 기록·해시 무결성: **{e["recorded_evidence_integrity"]}**. 이미지 단독 핵심 조건 통과는 최초 **{e["firstpass_image_pass_count"]}/20**, 스킬의 제한된 자기 보정과 실제 선택 후 **{e["final_image_pass_count"]}/20**이다. 세트 다양성은 별도로 모두 통과해야 한다. 이 수치는 네 문맥에 묶인 표본의 관찰값이며 향후 성공률이 아니다.','', '[20장 갤러리](gallery.html) · [전체 원본 평가 자료](raw/planning/final-evidence.json) · [기록 조회 인덱스](archive-index.json)','', '| 요청 | 최초 세트 | 최종 세트 | 최초/최종 이미지 통과 | 최종 다양성: 편집/마감/포트폴리오 |','| --- | --- | --- | --- | --- |']
for cid,s in e['sets'].items():
 rows=[e['images'][x] for x in s['roles']];ip=sum(x['initial_image_gate']=='PASS' for x in rows);fp=sum(x['final_image_gate']=='PASS' for x in rows);ds='/'.join(str(x['diversity']) for x in s['final_reviewers'])
 lines.append(f'| {s["name"]} | {s["initial_case_gate"]} | {s["final_case_gate"]} | {ip}/5 → {fp}/5 | {ds} |')
sections=[]
for cid,s in e['sets'].items():
 rows=[e['images'][x] for x in s['roles']];ip=sum(x['initial_image_gate']=='PASS' for x in rows);fp=sum(x['final_image_gate']=='PASS' for x in rows);ds='/'.join(str(x['diversity']) for x in s['final_reviewers'])
 cards=[]
 for role in s['roles']:
  x=e['images'][role];b=x['binding'];ib=x['initial_binding'];selected=x['selected'];sel=read(r/link(x['ordinary_selection']['path']));lo=[]
  for o in x['reviewers']:
   for dim,n in o['scores'].items():
    if n<4:lo.append(f'{o["profile"]}/{dim}={n}: {o["evidence"][dim]}')
  residuals=[]
  for o in x['reviewers']:residuals.extend(o['residuals']+o['mandatory']['issues']+o['mandatory']['uncertainties'])
  native=link(b['source_native']);qa=link(b['views']['usage720']['path']);ini=link(ib['source_native'])
  score_rows=''.join('<tr><th>'+esc(o['profile'])+'</th>'+''.join('<td>'+str(o['scores'][d])+'</td>' for d in dims)+'</tr>' for o in x['reviewers'])
  observations=''.join('<li>'+esc(t)+'</li>' for t in dict.fromkeys(lo+residuals))
  cards.append(f'<article><h3>{esc(role)} · {esc(x["final_image_gate"])}</h3><a href="{native}"><img src="{qa}" alt="{esc(role)} 선택한 포스터" loading="lazy"></a><p>{selected["width"]} × {selected["height"]} · {esc(selected["stage"])} · {sel["call_count"]}회 호출</p><p><a href="{native}">선택 원본</a> · <a href="{ini}">최초 원본 ({esc(x["initial_image_gate"])})</a> · <a href="{link(x["ordinary_selection"]["path"])}">보정·선택 기록</a></p><details><summary>세 평가자의 7항목 점수와 잔여 문제</summary><table><tr><th>평가자</th>'+''.join('<th>'+esc(n)+'</th>' for n in names)+f'</tr>{score_rows}</table><ul>{observations}</ul></details></article>')
  lines+=['',f'### {role}: {x["initial_image_gate"]} → {x["final_image_gate"]}',f'[{selected["width"]}×{selected["height"]} 선택 원본]({native}) · [최초 원본]({ini}) · [선택·보정 기록]({link(x["ordinary_selection"]["path"])})', '', '| 평가자 | '+' | '.join(names)+' |','| --- | '+' | '.join(['---']*7)+' |']
  for o in x['reviewers']:lines.append('| '+o['profile']+' | '+' | '.join(str(o['scores'][d]) for d in dims)+' |')
  lines+=['','잔여 관찰:']+['- '+t for t in dict.fromkeys(lo+residuals)]
  if not lo and not residuals:lines.append('- 평가자가 기록한 잔여 관찰 없음. 제작 주체나 인쇄 적합성을 보증하지 않는다.')
 sections.append(f'<section id="{esc(cid)}"><h2>{esc(s["name"])} · 최종 세트 {esc(s["final_case_gate"])}</h2><p>다양성 {ds}; 가까운 쌍과 평가자 간 차이는 전체 평가 자료에 보존했습니다.</p><div class="grid">'+''.join(cards)+'</div></section>')
lines+=['','## 검증 방법과 범위','',f'20명의 독립 제작자 역할을 새 문맥으로 실행했다. 환경 한도에 따라 최대 세 제작자가 동시에 작업했고 실제 원본 호출 구간의 최고 동시 수는 {calls["actual_recorded_interval_peak"]}였다. 기본 다섯 역할 구조를 한도 안에서 나누어 실행했으며 다섯 동시 실행을 주장하지 않는다.','',f'새 R6 호출은 {calls["recorded_attempts"]}/60회, 실패한 도구 시도는 {sum(x["kind"]=="failed native attempt" for x in calls["records"])}회였다. 하나의 최초 생성과 이미지당 최대 두 번의 자체 보정만 허용했다. 사용하지 않은 {60-calls["recorded_attempts"]}회는 종료·폐기했으며 이전 R5 128회와 종료된 한도는 다시 열지 않았다.','', '20장 전체의 제작자/중앙 일반 검수와 선택을 닫은 후 독립 평가를 시작했다. 외부 점수로 이미지를 추가 생성하거나 스킬을 바꾸지 않았다. 세 평가자는 제작자명·방향·프롬프트·이력·다른 평가자의 점수를 보지 않고 익명화한 완전한 다섯 장을 평가했다. 최초 세트와 실제 파일이 변경된 최종 세트는 새로운 평가자가 각각 검수했다. 다섯 파일 해시가 모두 동일한 세트만 최초 평가 전체를 재사용하며 대응을 명시했다.','', '모든 이미지는 원본/720px 폭/320px 긴 변으로 실제 열어 보았다. 행사 날짜·장소·마감·URL 및 전시 날짜·장소는 720px에서 제공 문구를 읽기 전에 먼저 전사하고 저장·재조회한 후 전체 카피를 대조했다. 실제 조회와 순서 기록은 평가자의 진술이며 파일 해시만으로 조회나 시각 판단을 증명하지는 못한다.','', '일곱 점수와 구체적 위치, 최저 관찰과 평가자 차이를 그대로 남겼다. 필수 조건 통과, 내용·타이포그래피·이미지/재질·AI 슬롭 각 4 이상을 세 평가자 모두에게 요구하며 세트 다양성도 각 4 이상이어야 한다. 평균 점수로 결함을 상쇄하지 않았다. 계층·공간·정서의 4 미만 점수도 보고서에 포함했다. AI 슬롭 평가는 보이는 상투성·글자·재질 결함에 관한 것이며 인간 제작 판별이 아니다. 지정된 클레이3D/강한 색은 해당 요청에 충실한지를 평가했고 장르만으로 감점하지 않았다.','', '이 표본은 네 요청의 20장이다. 사용자 제공 로고·실제 화면·외부 사진의 정확한 보존, 모든 장르, 후속 부분 수정, 실제 제품 기능, 인쇄 결과와 미래의 보편적 고품질을 검증한 것은 아니다. 이미지 생성 도구에는 최대 지원 해상도를 요청했지만 실제 반환 픽셀만 기록하며 최대 해상도 달성을 보증하지 않는다. 원본은 코드로 수정하지 않았고 QA 축소 보기만 만들었다.','', '참고 조사 원칙은 기존 메인 스킬의 고정된 자료와 앞선 평가에서 검토한 출처를 이어 사용했다. 이 추가 검증에서 새로운 외부 레퍼런스 조사를 수행했다고 주장하지 않는다. 세부 절차·입력 조회 예외·스키마 어댑터는 raw/planning의 원본 기록에 남겼다.','', '아카이브는 모든 최초·보정·미선택 원본과 원시 평가를 보존한다. 원래 절대 경로는 원본 기록 안에 유지하고 archive-index.json이 상대 경로의 동일한 해시 파일에 명시적으로 대응시킨다. [이식성 검증 코드](raw/audit_portable_archive.py)는 원본 작업 폴더 없이 이를 검사한다.']
(r/'report.md').write_text('\n'.join(lines)+'\n')
css='body{font-family:system-ui,sans-serif;margin:0;background:#f4f4f1;color:#222}main{max-width:1540px;margin:auto;padding:32px}h1{font-size:30px}h2{margin-top:50px}.grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:18px}article{background:white;padding:14px;border:1px solid #ddd}article h3{font-size:14px}img{width:100%;height:360px;object-fit:contain;background:#fafafa}p,li,summary{font-size:13px;line-height:1.7}table{font-size:10px;border-collapse:collapse;width:100%}td,th{padding:4px;border:1px solid #ddd}details{overflow:auto}a{color:#16456c}nav a{margin-right:20px}@media(max-width:1100px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:650px){.grid{grid-template-columns:1fr}main{padding:18px}}'
body=f'<h1>덕테이프 포스터 · 추가 20장 검증</h1><p>최종 전체 게이트 {esc(e["predeclared_core_diversity_gate"])} · 최초 단독 통과 {e["firstpass_image_pass_count"]}/20 → 선택 후 {e["final_image_pass_count"]}/20. 세트 다양성 별도. 모든 요청과 실패를 포함했습니다.</p><p><a href="report.md">검증 보고서</a> · <a href="raw/planning/final-evidence.json">평균 없이 전체 원시 점수</a> · <a href="archive-index.json">원본 조회 인덱스</a></p><nav>'+''.join(f'<a href="#{cid}">{esc(s["name"])}</a>' for cid,s in e['sets'].items())+'</nav>'+''.join(sections)
(r/'gallery.html').write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>추가 20장 검증</title><style>'+css+'</style><main>'+body+'</main></html>')
print(json.dumps({'report':str(r/'report.md'),'gallery':str(r/'gallery.html'),'cards':20,'pixel_edits':False}))
