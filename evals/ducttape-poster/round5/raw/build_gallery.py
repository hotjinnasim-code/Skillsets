#!/usr/bin/env python3
"""Write an offline gallery using only explicit archived path/SHA bindings."""
import argparse,html,json
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('archive',type=Path);a=ap.parse_args();r=a.archive.resolve()
read=lambda p:json.loads(p.read_text());idx=read(r/'archive-index.json');lookup={x['source_absolute']:x['archive_relative'] for x in idx['files']};f=read(r/'raw/planning/final-delivery-evidence.json')
def href(source):
 assert source in lookup,source
 return html.escape(lookup[source],quote=True)
def card(role,item):
 views=item['views'];src=views['thumbnail320']['path'];native=item.get('final_native_absolute',item.get('selected_native'));native=native or views['native']['path'];dimensions=views['native']['dimensions'];label=html.escape(role)
 return '<article><h2>'+label+'</h2><a href="'+href(native)+'"><img loading="lazy" src="'+href(src)+'" alt="'+label+' 축소 보기"></a><p>'+str(dimensions[0])+' × '+str(dimensions[1])+'</p><p><a href="'+href(native)+'">원본</a> · <a href="'+href(views['usage720']['path'])+'">너비 720</a> · <a href="'+href(src)+'">장변 320</a></p></article>'
cards=''.join(card(role,item) for role,item in f['selected_images'].items())
transfer=f.get('required_transfer_evidence');extra=''
if transfer:
 extra='<h2>추가 제약 전이 검사</h2><p>선택 14장과 별도로 평가한 글자·여백 요청입니다.</p><section>'+''.join(card(x['role'],x) for x in transfer['image_bindings'])+'</section>'
status='PASS' if f['predeclared_gate_pass'] else 'FAIL';page='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>덕테이프 포스터 평가 5</title><style>body{margin:32px auto;max-width:1100px;padding:0 24px;font-family:system-ui,sans-serif;background:#f5f5f3;color:#202020}h1{font-size:30px}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px}article{padding:16px;background:white;border:1px solid #ddd}article h2{margin:0 0 12px;font-size:18px}img{width:100%;height:320px;object-fit:contain}a{color:#174e78}p{line-height:1.6}</style><h1>덕테이프 포스터 평가 5</h1><p>선택 14장 · 사전 핵심/다양성 기준 '''+status+''' · 모든 원점수와 잔여 지적은 <a href="report.md">보고서</a>와 <a href="raw/planning/final-delivery-evidence.json">근거</a>에 있습니다. 서로 다른 버전의 선택 모음이며 모든 미래 요청의 품질을 보장하지 않습니다.</p><section>'''+cards+'</section>'+extra+'</html>'
(r/'gallery.html').write_text(page,encoding='utf-8');print('Wrote offline gallery, selected14 plus declared control. No browser rendering verification claimed.')
