"""Create a plain review index of the actual selected native posters."""
import html,json
from pathlib import Path
root=Path(__file__).resolve().parent
corpus=json.loads((root/'planning/corpus20.json').read_text())
parts=['<!doctype html><meta charset="utf-8"><title>덕테이프 포스터 추가20 검증</title><style>body{font:16px/1.6 system-ui,sans-serif;background:#f4f3ef;color:#191919;margin:32px auto;padding:0 24px;max-width:1400px}h1{font-size:28px}h2{margin-top:40px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:28px}figure{margin:0;max-width:420px}img{display:block;width:100%;height:360px;object-fit:contain;background:#e9e8e4}figcaption{font-size:13px;margin-top:10px}a{color:inherit}code{font-size:11px}p{max-width:880px}</style><h1>덕테이프 포스터 추가20 검증</h1><p>7개 요청 · 20개 시안. 보정 전후 원본과 실패 기록을 보존했습니다. 아래는 실제 선택된 결과이며 원본 링크에서 내려받을 수 있습니다. 하이엔드 판정은 독립 평가 결과를 확인해야 합니다. 합성 참조 자산3개는 포스터20장에 포함하지 않습니다.</p>']
count=0
for case in corpus['cases']:
 parts.append('<h2>'+html.escape(case['case_id']+' · '+case['copy'][0]['text'])+'</h2><div class="grid">')
 for role in case['roles']:
  d=root/'production'/role['role_id'];s=d/'selection.json'
  if not s.is_file():
   parts.append('<figure><figcaption>'+html.escape(role['role_id'])+' · 최종 파일 없음</figcaption></figure>');continue
  sel=json.loads(s.read_text());native=sel['selected_files']['original'];thumb=sel['selected_files']['usage720'];rel=lambda p:html.escape(str(Path(p).relative_to(root)),quote=True)
  parts.append('<figure><a href="'+rel(native['path'])+'"><img loading="lazy" src="'+rel(thumb['path'])+'" alt="'+html.escape(role['role_id'],quote=True)+'"></a><figcaption>'+html.escape(role['role_id'])+' · '+html.escape(sel['selected_stage'])+' · '+str(native['width'])+' × '+str(native['height'])+'<br><a download href="'+rel(native['path'])+'">원본 다운로드</a> · <a href="'+rel(s)+'">선택 기록</a><br><code>'+native['sha256']+'</code></figcaption></figure>');count+=1
 parts.append('</div>')
parts.append('<p>실제 선택된 원본 '+str(count)+'/20. 사진·3D·흑백 등 장르 자체를 AI 슬롭으로 판정하지 않으며, 내용 연결·글자·구조·재질·마감의 관찰 가능한 결함을 평가합니다.</p>')
out=root/'gallery.html'
with out.open('x') as f:f.write('\n'.join(parts))
print(json.dumps({'gallery':str(out),'selected_count':count,'planned':20}))
