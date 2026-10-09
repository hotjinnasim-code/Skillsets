"""Render only two newly authored planning diagrams; no bitmap inputs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import json

WORK = Path.cwd().resolve()
assert WORK == Path('/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round20')
OUT = WORK / 'coordinator/guides/m1-m2'
PLAN = WORK.parent.parent / 'drafts/w-five-design/plan.json'
RUNTIME = WORK / 'snapshots/candidate-w/scripts/make_layout_guide.py'
plan_bytes = PLAN.read_bytes()
plan = json.loads(plan_bytes)
case = json.loads((WORK / 'planning/single-five-case.json').read_text())['cases'][0]
assert plan['request'] == case['request'] and plan['copy'] == case['copy']

def rect(x, y, w, h, fill):
    return {'type':'rect','x':x,'y':y,'width':w,'height':h,'fill':fill}

def ellipse(x, y, w, h, fill):
    return {'type':'ellipse','x':x,'y':y,'width':w,'height':h,'fill':fill}

def poly(points, fill):
    return {'type':'polygon','points':points,'fill':fill}

def line(x1, y1, x2, y2, stroke='#666963', width=5):
    return {'type':'line','x1':x1,'y1':y1,'x2':x2,'y2':y2,'stroke':stroke,'stroke_width':width}

m1_shapes = [
    rect(64,183,860,215,'#D7D8D2'),
    rect(984,42,552,628,'#DCDDD7'),
    rect(984,554,552,116,'#C9CBC4'),
    # A substantive support contact: forearm enters a palm below the small pot.
    poly([[80,323],[278,324],[369,340],[436,349],[464,359],[520,360],[544,368],[537,378],[508,385],[445,384],[393,378],[333,361],[277,354],[80,354]],'#9B9F95'),
    line(457,374,516,374,'#73796E',3),
    line(479,365,530,369,'#73796E',3),
    # Nursery pot, rim and rooted stems; the hand supports the base.
    poly([[442,267],[558,267],[540,361],[460,361]],'#73796F'),
    ellipse(440,257,120,21,'#ACB0A5'),
    ellipse(449,262,102,11,'#62685E'),
    line(500,268,499,196,'#62685E',5),
    line(499,222,460,208,'#62685E',4),
    line(500,232,548,216,'#62685E',4),
    line(499,249,454,241,'#62685E',4),
    ellipse(415,197,79,23,'#8C9685'),
    ellipse(521,202,72,24,'#8C9685'),
    ellipse(416,229,69,23,'#8C9685'),
    ellipse(487,184,23,48,'#8C9685'),
    # The domestic seat is a cropped physical scale reference, not a blank room.
    poly([[1391,285],[1420,285],[1471,437],[1443,437]],'#A2A69C'),
    rect(1375,430,151,22,'#979D90'),
    line(1388,451,1368,637,'#878F7F',10),
    line(1508,451,1521,635,'#878F7F',10),
    line(1379,579,1519,579,'#9BA18F',7),
    # Larger plant has a visible pot base and a different scale than the near pot.
    poly([[1156,549],[1347,549],[1326,652],[1178,652]],'#858D7C'),
    ellipse(1153,537,197,29,'#A7AF9E'),
    ellipse(1169,543,165,16,'#686F61'),
    line(1251,547,1247,143,'#6A7660',8),
    line(1249,238,1134,188,'#6A7660',5),
    line(1247,289,1353,235,'#6A7660',5),
    line(1248,369,1116,335,'#6A7660',5),
    line(1250,433,1360,397,'#6A7660',5),
    line(1249,489,1160,465,'#6A7660',5),
    ellipse(1055,153,143,73,'#909B82'),
    ellipse(1317,199,169,79,'#909B82'),
    ellipse(1035,301,156,72,'#8A967D'),
    ellipse(1325,362,177,76,'#8A967D'),
    ellipse(1100,438,136,61,'#969F89'),
    ellipse(1209,114,75,104,'#969F89'),
    line(1006,629,1150,629,'#B1B7A9',4),
]

m2_shapes = [
    # Original major polygon; neutral tones preserve one diagonal light field.
    poly([[1090,0],[1600,0],[1600,900],[420,900],[50,570]],'#E1E1D9'),
    poly([[1460,0],[1511,0],[1511,316],[1460,340]],'#9DA39A'),
    poly([[1460,305],[1597,294],[1597,318],[1460,343]],'#8A9286'),
    # Attached shadows belong to the two pots and stay outside actual glyphs.
    poly([[1366,830],[1469,870],[662,890],[512,847]],'#A5ACA0'),
    poly([[214,439],[285,469],[11,548],[4,487]],'#AAB0A3'),
    # Farther pot and connected plant, entirely before the first visit glyph row.
    poly([[189,423],[281,423],[268,463],[202,463]],'#7C8575'),
    ellipse(186,415,98,17,'#A2AA99'),
    ellipse(198,419,74,10,'#626D5C'),
    line(236,422,236,287,'#626D5C',5),
    line(236,325,190,301,'#626D5C',4),
    line(236,356,292,335,'#626D5C',4),
    line(235,389,188,376,'#626D5C',4),
    ellipse(150,278,86,33,'#85927C'),
    ellipse(271,314,89,37,'#85927C'),
    ellipse(143,359,87,32,'#85927C'),
    ellipse(222,258,28,61,'#85927C'),
    # Window-side plant: pot, roots/stems and attached leaves have a readable base.
    poly([[1318,784],[1511,784],[1490,875],[1343,875]],'#7A8371'),
    ellipse(1314,773,201,29,'#9AA58B'),
    ellipse(1331,779,165,15,'#606B55'),
    line(1410,786,1403,351,'#606B55',8),
    line(1404,430,1321,384,'#606B55',5),
    line(1406,486,1493,446,'#606B55',5),
    line(1407,563,1314,528,'#606B55',5),
    line(1408,640,1496,606,'#606B55',5),
    line(1409,701,1316,680,'#606B55',5),
    ellipse(1274,363,95,54,'#859277'),
    ellipse(1453,424,120,54,'#859277'),
    ellipse(1264,505,108,53,'#859277'),
    ellipse(1455,583,121,52,'#859277'),
    ellipse(1266,657,116,50,'#859277'),
    ellipse(1380,329,47,101,'#919E82'),
]

specs = []
adjustments = []
for ordinal, shapes in [(1,m1_shapes),(2,m2_shapes)]:
    d = plan['directions'][ordinal-1]
    assert d['role']==f'R20-C1-M{ordinal}'
    g=d['guide_geometry_concept']
    blocks=[]
    for t in g['text_regions']:
        b={k:v for k,v in t.items() if k!='entry'}
        assert ' '.join(b['lines'])==b['copy']
        if ordinal==2:
            b['color']='#202624'
        blocks.append(b)
    assert sorted(t['entry'] for t in g['text_regions'])==list(range(1,13))
    canvas=dict(g['canvas'])
    if ordinal==2:
        canvas['background']='#BDC1B7'
        adjustments.append({
            'role':d['role'],
            'kind':'Prospective neutral guide tonal mapping only',
            'reason':'The original oblique light plane crosses both cream upper text and dark practical text positions. In this newly authored neutral planning sketch, mid-light gray field, lighter gray beam and uniform dark copy retain contrast without changing any position, actual copy, font/face/size/lines or original plan.',
            'scope':'Guide canvas/text tones only; original plan retains its intended dark/apricot final style, and a native final must resolve the image/copy tonal relationship. Gray guide tones are not the final poster style.',
        })
    spec={'canvas':canvas,'shapes':shapes,'text_blocks':blocks}
    path=OUT / f'm{ordinal}-guide.spec.json'
    with path.open('x',encoding='utf-8') as f:
        json.dump(spec,f,ensure_ascii=False,indent=2)
        f.write('\n')
    specs.append((d['role'],path,f'm{ordinal}-guide'))

loader=importlib.util.spec_from_file_location('round20_guide_renderer_m1m2',RUNTIME)
module=importlib.util.module_from_spec(loader)
loader.loader.exec_module(module)
rows=[]
for role,path,name in specs:
    outputs=module.render(path,OUT,name)
    rows.append({'role':role,'spec':str(path),'outputs':{k:str(v) for k,v in outputs.items()}})

assert PLAN.read_bytes()==plan_bytes
status={
    'status':'Rendered two newly authored planning diagrams; awaiting actual PNG inspection',
    'time_utc':datetime.now(timezone.utc).isoformat(),
    'cwd':str(WORK),
    'plan_path':str(PLAN),
    'plan_sha256_before_after':hashlib.sha256(plan_bytes).hexdigest(),
    'plan_unchanged':True,
    'renderer_path':str(RUNTIME),
    'renderer_sha256':hashlib.sha256(RUNTIME.read_bytes()).hexdigest(),
    'rows':rows,
    'prospective_adjustments':adjustments,
    'actual_copy_conservation':'Twelve distinct original entries once per diagram; every deliberate line array joins exactly to its original copy.',
    'scope_limits':['Newly authored code shapes/text only; no bitmap input, source artwork, generated poster or critic record read.','No native image calls, final poster, image edit, font installation/copy or final typography overlay.','Shapes approximate image contact/scale/light organization. They are plans, not finished image style.','Actual supplied font bytes/face are used for guide PNG only; this does not apply a font file to a future native poster.'],
}
with (OUT/'render-status.json').open('x',encoding='utf-8') as f:
    json.dump(status,f,ensure_ascii=False,indent=2)
    f.write('\n')
print(json.dumps({'rendered_roles':[r['role'] for r in rows],'plan_unchanged':True,'guide_pngs':[r['outputs']['.png'] for r in rows]},ensure_ascii=False))
