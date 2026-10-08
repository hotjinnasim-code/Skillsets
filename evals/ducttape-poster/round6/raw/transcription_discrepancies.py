"""Inventory reported/computed equality disagreement without changing any gate."""
import hashlib, json
from pathlib import Path
r=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text())
collapse=lambda s:' '.join(s.split())
without_space=lambda s:''.join(s.split())
plan=read(r/'cli-reviews/dispatch-plan.json')
done=read(r/'cli-reviews/all-completed.json')
assert done['assignments']==len(plan['jobs'])
rows=[]
for job in plan['jobs']:
    path=r/f'blind-{job["wave"]}'/'reviews'/f'{job["profile"]}.json'
    if not path.is_file():continue
    report=read(path)
    for ident,observation in report.get('images',{}).items():
        for t in observation.get('mandatory',{}).get('transcription',[]):
            required,observed=t.get('required'),t.get('observed')
            if not isinstance(required,str) or not isinstance(observed,str):continue
            computed=collapse(required)==collapse(observed)
            if t.get('equal')!=computed:
                rows.append({**job,'image_id':ident,'raw_report':{'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()},
                  'required':required,'observed':observed,'reported_equal':t.get('equal'),
                  'primary_comparator_equal':computed,
                  'same_non_whitespace_characters':without_space(required)==without_space(observed)})
out={'scope':'Diagnostic distinction only. The primary whitespace-collapse comparator, unchanged raw reports, score observations and NOT_ASSESSABLE treatment remain authoritative. Same non-whitespace characters is not a substitute gate or claim that word spacing/typography is correct.',
 'discrepancy_count':len(rows),'whitespace_only_discrepancy_count':sum(x['same_non_whitespace_characters'] for x in rows),'rows':rows}
with (r/'planning/transcription-discrepancies.json').open('x') as f:json.dump(out,f,ensure_ascii=False,indent=2)
print(json.dumps({k:out[k] for k in ('discrepancy_count','whitespace_only_discrepancy_count')}))
