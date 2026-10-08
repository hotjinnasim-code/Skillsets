#!/usr/bin/env python3
"""Pin a completed ordinary five-maker selection; no scoring or image modification."""
from pathlib import Path
import argparse,datetime,hashlib,json,secrets,subprocess,sys
r=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',required=True);p.add_argument('--root-inspection',required=True,type=Path);a=p.parse_args()
read=lambda x:json.loads(Path(x).read_text());sha=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
c=next(x for x in read(r/'planning/cases.json')['cases'] if x['id']==a.case)
assert a.root_inspection.is_file(),'Actual ordinary inspection record is required'
first,final=[],[]
for slot in c['slots']:
 role=slot['id'];d=r/'production'/role;s=read(d/'selection.json')
 assert s['role']==role and s['case_id']==c['id']
 for stage,rows in [('initial',first),(s['selected_stage'],final)]:
  mp=d/stage/'manifest.json';m=read(mp);fp=Path(m['final']['path'])
  assert sha(fp)==m['final']['sha256'] and (mp.parent/'inspection.json').is_file()
  rows.append(dict(role=role,case_id=c['id'],stage=stage,final_native=str(fp),sha256=sha(fp),width=m['width'],height=m['height'],manifest=str(mp),manifest_sha256=sha(mp)))
changed={x['role']:x['sha256'] for x in first}!={x['role']:x['sha256'] for x in final}
waves={'first':'W'+secrets.token_hex(4).upper()}
waves['final']='W'+secrets.token_hex(4).upper() if changed else waves['first']
for name,rows in [('first',first),('final',final)]:
 path=r/'planning'/f'{name}-{c["id"]}-selection.json'
 with path.open('x') as f:json.dump({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Complete five roles; source manifests pinned after maker FINAL and ordinary root selection close','selected':rows},f,ensure_ascii=False,indent=2)
with (r/'planning'/f'{c["id"]}-ordinary-closed.json').open('x') as f:
 json.dump(dict(closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),case_id=c['id'],external_critics_not_yet_dispatched=True,root_inspection={'path':str(a.root_inspection.resolve()),'sha256':sha(a.root_inspection)},first_selection={'path':str(r/'planning'/f'first-{c["id"]}-selection.json'),'sha256':sha(r/'planning'/f'first-{c["id"]}-selection.json')},final_selection={'path':str(r/'planning'/f'final-{c["id"]}-selection.json'),'sha256':sha(r/'planning'/f'final-{c["id"]}-selection.json')},physical_set_changed=changed,review_waves=waves,final_review='fresh complete three-critic case required' if changed else 'reuse exact complete initial three-critic set; no new review'),f,ensure_ascii=False,indent=2)
for stage in ['first']+(['final'] if changed else []):
 subprocess.run([sys.executable,str(r/'build_packet.py'),'--wave',waves[stage],'--selection',str(r/'planning'/f'{stage}-{c["id"]}-selection.json'),'--case',c['id']],check=True)
print(json.dumps({'case':c['id'],'first_images':5,'final_images':5,'physical_set_changed':changed}))
