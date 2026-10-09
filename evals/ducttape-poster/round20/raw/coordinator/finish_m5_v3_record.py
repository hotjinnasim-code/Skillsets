"""Record already-rendered v3 without rerendering or replacing historical outputs."""
from pathlib import Path
import datetime
import hashlib
import json

ROUND = Path(__file__).resolve().parents[1]
TASK = ROUND.parents[1]
OUT = ROUND / 'coordinator/guides/root-m5'
PLAN = TASK / 'drafts/w-five-design/plan.json'
source = (ROUND / 'coordinator/make_m5_guide.py').read_text()
plan_before = PLAN.read_bytes()
spec_path = OUT / 'm5-guide-v3.spec.json'
outputs = {suffix:OUT / ('m5-guide-v3' + suffix) for suffix in ('.svg','.png','.manifest.json')}
assert all(path.is_file() for path in outputs.values())
record_source = source[source.index('record = {'):source.index('\nwith (OUT/')]
exec(compile(record_source, str(ROUND / 'coordinator/make_m5_guide.py'), 'exec'))
record['record_write_failure_preserved'] = {
    'message':'v3 SVG, PNG and manifest rendered successfully, but writing the old exclusive render-status.json name raised FileExistsError',
    'resolution':'record written under new render-status-v3.json without rerendering; v2 status and all prior files retained',
}
with (OUT / 'render-status-v3.json').open('x',encoding='utf-8') as handle:
    json.dump(record,handle,ensure_ascii=False,indent=2)
    handle.write('\n')
print(json.dumps({'record':str(OUT / 'render-status-v3.json'),'outputs':list(map(str,outputs.values()))}))
