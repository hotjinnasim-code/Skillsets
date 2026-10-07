#!/usr/bin/env python3
"""Create a blinded QA package from an explicit physical selection, never choose winners."""
from pathlib import Path
import argparse,datetime,hashlib,json,random,shutil
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--wave',required=True);p.add_argument('--selection',type=Path,required=True);p.add_argument('--cases',type=Path,help='Explicit predeclared cases file; defaults to the original three cases.');p.add_argument('--id-prefix',default='X');p.add_argument('--complete-case-subset',action='store_true',help='Explicitly review only complete cases, e.g. product and invitation, without reselecting other closed cases.');a=p.parse_args();r=Path(__file__).resolve().parent;b=r/('blind-'+a.wave)
assert not b.exists(),'Blind wave already exists; preserve closed package.'
(b/'images').mkdir(parents=True);(b/'reviews').mkdir()
selected=json.loads(a.selection.read_text())['selected'];assert len({x['role'] for x in selected})==len(selected)
if not a.complete_case_subset:assert len(selected)==9
cases_path=(a.cases or r/'planning/cases.json').resolve();cases=json.loads(cases_path.read_text())['cases'];cmap={};rolemaps={}
for case in cases:
 cid={'garden-title-only':'title-only','foln-product-mixed-copy':'product','heldout-repair-cafe-dense':'invitation'}.get(case['id'],case.get('review_case_id'))
 assert cid in {'title-only','product','invitation','type-only-control'},'Unknown review case'
 assert cid not in cmap,'Duplicate review case'
 cmap[cid]={'request':case['request'],'copy':case['copy'],'expected_count':case['expected_final_count']}
 if cid=='type-only-control':
  assert a.cases is not None and case['id']=='constrained-type-only-transfer' and case['expected_final_count']==1 and case['slots']==[{'id':'T01','ratio':'2:3'}],'Only the explicit T01 singleton control is supported'
  cmap[cid].update({'source_case_id':case['id'],'review_case_id':cid,'singleton_diversity':'not_applicable'})
 for slot in case['slots']:
  assert slot['id'] not in rolemaps,'Duplicate case role'
  rolemaps[slot['id']]=(cid,slot['ratio'])
included={rolemaps[x['role']][0] for x in selected};cmap={k:v for k,v in cmap.items() if k in included}
for cid,case in cmap.items():assert sum(rolemaps[x['role']][0]==cid for x in selected)==case['expected_count'],'Only complete case sets can be independently reviewed'
ids=random.SystemRandom().sample(range(100,999),len(selected));mapping=[];images=[];sets={cid:[] for cid in cmap};action=[]
for slot,n in zip(selected,ids):
 role=slot['role'];cid,ratio=rolemaps[role];iid=a.id_prefix+str(n);src=Path(slot['final_native']);assert src.is_file();h=hashlib.sha256(src.read_bytes()).hexdigest();assert h==slot['sha256']
 native=b/'images'/f'{iid}-native.png';shutil.copyfile(src,native)
 im=Image.open(native);w,ht=im.size;usage=b/'images'/f'{iid}-usage720.png';thumb=b/'images'/f'{iid}-thumbnail320.png'
 im.resize((720,round(ht*720/w)),Image.Resampling.LANCZOS).save(usage)
 scale=320/max(w,ht);im.resize((round(w*scale),round(ht*scale)),Image.Resampling.LANCZOS).save(thumb)
 images.append({'image_id':iid,'case_id':cid,'native':str(native),'usage720':str(usage),'thumbnail320':str(thumb),'width':w,'height':ht,'target_ratio':ratio});sets[cid].append(iid)
 mapping.append({'image_id':iid,**slot,'case_id':cid,'native_sha256':h,'qa_hashes':{str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in [native,usage,thumb]}})
 if cid=='invitation':action.append({'image_id':iid,'usage720':str(usage),'read_before_copy':'Record observed event date, application deadline, full URL, location and uncertainty. No suppliedcopy available yet.'})
random.SystemRandom().shuffle(images)
packet={'scope':f'Anonymous {len(selected)} independent posters from exact given briefs. No version/prompt/style/explanation/history disclosed. Physical/authorship/print certification is outside scope.','cases':cmap,'images':images,'sets':{k:{'members':v,'expected_count':cmap[k]['expected_count']} for k,v in sets.items()},'comparison_pairs':[]}
case_source={'path':str(cases_path),'sha256':hashlib.sha256(cases_path.read_bytes()).hexdigest()} if a.cases else None
(b/'packet.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
(b/'action-first.json').write_text(json.dumps({'instruction':'View these actual720 invitation images and save PROFILE-action-first.json before openingpacket/fullcopy. Retain readings unchanged when fullcopy crosschecked.','images':action},ensure_ascii=False,indent=2)+'\n')
shutil.copyfile(r/'planning/review-protocol-template.md',b/'review-protocol.md')
mapping_doc={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mapping':mapping,'packet':str(b/'packet.json'),'action_first':str(b/'action-first.json'),'quality_gate_claim':None}
if case_source:mapping_doc['predeclared_cases']=case_source
(r/'planning'/f'{a.wave}-blind-mapping.json').write_text(json.dumps(mapping_doc,ensure_ascii=False,indent=2)+'\n')
print(f'Created immutable blind-{a.wave}:{len(selected)}images,{len(selected)*3}views,{len(action)}action-first images.')
