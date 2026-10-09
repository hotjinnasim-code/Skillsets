"""New code-only domestic-section planning guide; no bitmap inputs or final edits."""
from pathlib import Path
import hashlib
import importlib.util
import json
import datetime

ROUND = Path(__file__).resolve().parents[1]
TASK = ROUND.parents[1]
PLAN = TASK / 'drafts/w-five-design/plan.json'
OUT = ROUND / 'coordinator/guides/root-m5'
OUT.mkdir(parents=True, exist_ok=True)
plan_before = PLAN.read_bytes()
direction = json.loads(plan_before)['directions'][4]
assert direction['role'] == 'R20-C1-M5'
concept = direction['guide_geometry_concept']
shapes = []

def rect(x,y,w,h,fill,stroke=None,sw=2):
    item = {'type':'rect','x':x,'y':y,'width':w,'height':h,'fill':fill}
    if stroke:
        item.update(stroke=stroke, stroke_width=sw)
    shapes.append(item)

def line(x1,y1,x2,y2,stroke='#A8AEA7',sw=3):
    shapes.append({'type':'line','x1':x1,'y1':y1,'x2':x2,'y2':y2,'stroke':stroke,'stroke_width':sw})

def polygon(points,fill,stroke=None,sw=2):
    item = {'type':'polygon','points':points,'fill':fill}
    if stroke:
        item.update(stroke=stroke,stroke_width=sw)
    shapes.append(item)

def ellipse(x,y,w,h,fill):
    shapes.append({'type':'ellipse','x':x,'y':y,'width':w,'height':h,'fill':fill})

def plant(cx,base,pot_w,pot_h,stem_h,leaf_w):
    # Pot base meets its support. Neutral silhouettes encode connected parts.
    top = base-pot_h
    polygon([[cx-pot_w/2,top],[cx+pot_w/2,top],[cx+pot_w*.36,base],[cx-pot_w*.36,base]],'#C8CCC4','#ADB4A9',2)
    ellipse(cx-pot_w/2,top-5,pot_w,10,'#B5BDB1')
    line(cx,top-2,cx,top-stem_h,'#AAB5A6',4)
    for sign,fraction in ((-1,.38),(1,.65),(-1,.88)):
        sy=top-stem_h*fraction
        lx=cx+sign*leaf_w*.58
        line(cx,sy+15,lx,sy,'#AAB5A6',3)
        ellipse(lx-leaf_w/2,sy-leaf_w*.24,leaf_w,leaf_w*.48,'#BAC3B4')

# Shared section geometry and visible furniture thickness/support.
polygon([[2,446],[700,446],[700,625],[1120,625],[1120,725],[1598,725],[1598,898],[2,898]],'#E1E3DC')
rect(4,446,696,10,'#C9CEC4')
rect(28,456,18,425,'#D0D5CB')
rect(430,456,18,425,'#D0D5CB')
rect(700,625,420,10,'#C6CDC3')
rect(1098,635,18,246,'#D0D5CB')
rect(1120,725,476,13,'#C6CDC3')
line(4,883,1596,883,'#BEC6BA',3)
line(1360,140,1360,728,'#CCD0C8',3)
line(1360,140,1594,140,'#CCD0C8',3)
line(1594,140,1594,883,'#CCD0C8',3)
# Different supports and sizes are the image's organizing relation.
plant(630,446,74,54,89,62)
plant(1220,725,58,43,73,48)
plant(1472,883,138,126,413,115)

blocks = [{key:value for key,value in region.items() if key != 'entry'} for region in concept['text_regions']]
case = json.loads((ROUND/'planning/single-five-case.json').read_bytes())['cases'][0]
assert sorted(block['copy'] for block in blocks) == sorted(entry['text'] for entry in case['copy'])
assert len(blocks) == 12
for block in blocks:
    assert ' '.join(block['lines']) == block['copy']
spec = {'canvas':concept['canvas'],'shapes':shapes,'text_blocks':blocks}
spec_path = OUT/'m5-guide-v4.spec.json'
with spec_path.open('x',encoding='utf-8') as handle:
    json.dump(spec,handle,ensure_ascii=False,indent=2)
    handle.write('\n')
helper = ROUND/'snapshots/candidate-w/scripts/make_layout_guide.py'
module_spec = importlib.util.spec_from_file_location('m5_planning_renderer',helper)
module = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(module)
outputs = module.render(spec_path,OUT,'m5-guide-v4')
assert PLAN.read_bytes() == plan_before
record = {
    'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'role':'R20-C1-M5',
    'kind':'new_code_shapes_actual_font_copy_planning','native_poster_calls':0,'bitmap_inputs':0,
    'spec':str(spec_path),'outputs':{key:str(value) for key,value in outputs.items()},
    'plan_sha256_unchanged':hashlib.sha256(plan_before).hexdigest(),
    'actual_copy_entries':12,'copy_and_line_groups_preserved':True,
    'type_regions_fonts_positions_from_plan':True,
    'prospective_shape_revision': {
        'previous_inputs':['m5-guide.spec.json','m5-guide-v2.spec.json','m5-guide-v3.spec.json'],
        'previous_result':'v1 rejected for a right leaf clipping 4.2px; v2 viewed at original resolution and small plants/table edges intersected slogan, market, venue, service and URL regions',
        'change':'floor plant x remains 1472; first support moved below market to y446 and widened to x700; middle support lowered below URL to y625; small plants placed at (630,446) and (1220,725); v4 moves the first table second leg from x677 to clear gutter x430; copy, fonts and text coordinates unchanged',
        'previous_input_preserved':True,
    },
    'limits':[
        'Authored neutral furniture/plant shapes represent support and scale; they are not final art or a client asset.',
        'Final colors, dry drawn contour density and imagery are specified by the prospective positive direction, not the neutral sketch.',
        'Typed font reference does not certify final native font-file application.',
        'Root visual review and a full all-five freeze are still required before first native generation.',
    ],
}
with (OUT/'render-status-v4.json').open('x',encoding='utf-8') as handle:
    json.dump(record,handle,ensure_ascii=False,indent=2)
    handle.write('\n')
print(json.dumps(record))
