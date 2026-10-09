from pathlib import Path
import json,datetime
ROOT=Path(__file__).resolve().parents[1]
rows=[]
for role in json.loads((ROOT/'planning/production-single-five-case.json').read_bytes())['cases'][0]['roles']:
 d=ROOT/'production'/role['role_id'];s=json.loads((d/'selection.json').read_bytes())
 for stage in ('initial','repair-1','repair-2'):
  p=d/'stages'/stage/'manifest.json'
  if not p.exists():continue
  m=json.loads(p.read_bytes());n=m['files']['original'];w,h=n['width'],n['height'];error=min(abs(w-h*16/9),abs(h-w*9/16))
  rows.append({'role':role['role_id'],'stage':stage,'selected':stage==s['selected_stage'],'native':n,'minimum_single_edge_deviation_pixels':error,'predeclared_rounding_policy_met':error<=0.5+1e-9})
value={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'requested_ratio':'16:9','policy_file':'planning/ratio-policy-before-generation.json','all_returned_stages':rows,'selected_count':sum(r['selected'] for r in rows),'selected_outside_policy':sum(r['selected'] and not r['predeclared_rounding_policy_met'] for r in rows),'unselected_outside_policy':sum(not r['selected'] and not r['predeclared_rounding_policy_met'] for r in rows),'scope':'Native manifest dimensions, no resize/crop/upscale. Actual failures have no invented raster.'}
with (ROOT/'checks/root-all-stage-ratio-observations.json').open('x') as f:json.dump(value,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in value.items() if k!='all_returned_stages'}))
