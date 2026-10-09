from pathlib import Path
from copy import deepcopy
from PIL import ImageFont
import hashlib
import json
import sys

ROOT = Path('/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster')
OUT = ROOT / 'drafts/z-five-design'
SOURCE = ROOT / 'work/round22/planning/single-five-case.json'
MATCHED_SOURCE = ROOT / 'work/round21/planning/single-five-case-hierarchy.json'
INITIAL_SKILL = ROOT / 'drafts/candidate-style-first'
SKILL = ROOT / 'drafts/candidate-style-first-ideas'
assert SKILL.is_dir(), 'Prospective optional-idea revision must exist before this plan revision.'
GOTHIC = '/System/Library/Fonts/AppleSDGothicNeo.ttc'
MYUNGJO = '/System/Library/Fonts/Supplemental/AppleMyungjo.ttf'
source = json.loads(SOURCE.read_text())['cases'][0]
matched_source = json.loads(MATCHED_SOURCE.read_text())['cases'][0]
copy = deepcopy(source['copy'])
old_sentence = '각각 전체 스타일과 레이아웃이 달랐으면 좋겠어.'
new_sentence = '스타일이 확연히 다르게 느껴지면 좋겠어. 레이아웃은 각 스타일과 읽기 흐름에 맞게 선택하고, 잘 작동하는 구도는 여러 시안에서 공유해도 돼.'
assert matched_source['request'].count(old_sentence) == 1
request = source['request']
assert request == matched_source['request'].replace(old_sentence, new_sentence)
assert copy == matched_source['copy']
conditions = deepcopy(source['conditions'])
body_lines = ['작은 화분부터 오래 키운 나무까지 만납니다.', '재배자의 이야기를 듣고,',
              '우리 집의 빛과 생활에 맞는', '식물을 골라보세요.']
assert ' '.join(body_lines) == copy[3]['text']
catalog = json.loads((SKILL / 'references/reference-catalog.json').read_text())
rows = {r['id']: r for col in catalog['poster_source_collections'].values() for r in col['rows']}

def observation(source_id):
    r = rows[source_id]
    return {'id': source_id,
            'observed_idea': r.get('observation', r.get('transferable_principle')),
            'use': 'Optional accumulated text observation only; no source pixels reopened and no artwork/layout/copy transplanted.'}

def rect(x,y,w,h,color):
    return {'type':'rect','x':x,'y':y,'width':w,'height':h,'fill':color}

def ellipse(x,y,w,h,color):
    return {'type':'ellipse','x':x,'y':y,'width':w,'height':h,'fill':color}

def polygon(points,color):
    return {'type':'polygon','points':points,'fill':color}

def line(x1,y1,x2,y2,color,width=6):
    return {'type':'line','x1':x1,'y1':y1,'x2':x2,'y2':y2,'stroke':color,'stroke_width':width}

def pot(x,y,w,h,color,rim):
    return [polygon([[x,y],[x+w,y],[x+w*0.84,y+h],[x+w*0.16,y+h]],color),
            ellipse(x,y-12,w,24,rim)]

def leaf(x,y,w,h,color):
    return ellipse(x,y,w,h,color)

# These new shapes plan contacts, crop, scale and style-compatible colour areas.
# They are neither source artwork nor final illustration or bitmap editing.
shapes1 = [rect(840,40,710,270,'#C8DCD8'), rect(840,334,710,516,'#A9D7DC'),
           rect(1167,40,18,270,'#E1F2F5'),
           polygon([[842,276],[919,208],[983,196],[1000,224],[937,246],[891,297]],'#C08B73')]
shapes1 += pot(959,203,132,88,'#F9F9F5','#393E35')
shapes1 += [line(1023,205,1020,112,'#386741',6),leaf(987,102,65,38,'#68894B'),
            leaf(1035,129,42,47,'#345E34'),leaf(1230,79,248,183,'#4B7137'),
            line(1245,218,1470,115,'#9BB079',4),
            polygon([[860,751],[1550,698],[1550,850],[860,850]],'#D0E6E4')]
shapes1 += pot(1048,705,315,119,'#7E8C84','#323C31')
shapes1 += [line(1200,706,1278,402,'#425C35',14),line(1196,620,1037,495,'#425C35',10),
            leaf(1211,366,220,103,'#4B723B'),leaf(965,451,219,90,'#6C8749'),
            leaf(1196,505,241,104,'#315C36'),leaf(1410,546,138,62,'#608C50')]

shapes2 = [polygon([[844,747],[1598,647],[1598,898],[844,898]],'#111C5B'),
           polygon([[928,340],[1035,277],[1217,418],[1185,485],[1104,483]],'#D4A56F'),
           polygon([[1110,391],[1246,366],[1275,402],[1162,442]],'#E3B586'),
           polygon([[1196,399],[1328,430],[1304,500],[1176,470]],'#DE4C37'),
           polygon([[1300,474],[1357,453],[1379,474],[1320,500]],'#DE4C37'),
           line(1263,399,1308,380,'#E36745',14),line(1308,380,1336,423,'#E36745',14),
           line(1347,478,1380,528,'#A9D4E5',4),line(1334,486,1355,537,'#A9D4E5',4)]
shapes2 += pot(1282,577,224,166,'#DF8C70','#181D44')
shapes2 += [line(1394,579,1476,350,'#86A76C',10),line(1390,561,1347,413,'#86A76C',7),
            leaf(1425,336,146,72,'#AAC87D'),leaf(1340,399,112,73,'#729861'),
            leaf(1418,434,142,79,'#AAC87D'),leaf(1267,491,136,64,'#537E56'),
            polygon([[962,745],[1244,713],[1190,792],[884,827]],'#0D1548')]

shapes3 = [rect(45,42,690,262,'#333638'),rect(45,326,690,233,'#717374'),
           rect(45,581,690,273,'#242729')]
shapes3 += [polygon([[63,111],[153,87],[357,186],[328,224],[158,169]],'#D8D8D3'),
            polygon([[535,76],[712,111],[703,161],[509,132],[460,183],[423,165]],'#AAAFAE'),
            ellipse(285,143,196,136,'#131719'),line(379,161,354,59,'#9AADA5',10),
            leaf(310,59,79,51,'#C9D1CA'),
            polygon([[65,434],[158,379],[365,431],[380,482],[266,471]],'#D5D6D0'),
            polygon([[558,389],[733,362],[733,416],[514,463],[425,453],[425,424]],'#B6B9B6'),
            ellipse(296,394,157,120,'#272727')]
for j in range(7):
    shapes3.append(line(314+j*17,475,292+j*18,543,'#C6C9BA',3))
shapes3 += pot(251,753,268,96,'#9DA49F','#1D2321')
shapes3 += [line(380,758,479,604,'#A0ACA2',11),line(391,720,279,638,'#A0ACA2',9),
            leaf(436,599,167,69,'#CDD5CD'),leaf(184,625,174,76,'#8E9F91'),
            leaf(379,682,186,77,'#B4C5B6')]

shapes4 = [polygon([[882,835],[1564,744],[1564,861],[882,861]],'#D9BB2A')]
shapes4 += pot(896,610,220,190,'#912743','#4C1831')
shapes4 += pot(1281,646,241,154,'#D66C31','#4C1831')
shapes4 += [line(1001,612,984,354,'#5B1F39',12),line(1398,646,1451,292,'#5B1F39',12),
            leaf(865,344,165,79,'#A02D45'),leaf(953,413,180,91,'#A02D45'),
            leaf(917,529,144,78,'#5B1F39'),
            polygon([[1341,428],[1427,270],[1506,365],[1528,495],[1422,493]],'#67253F'),
            leaf(1290,495,161,101,'#A84353'),
            polygon([[843,284],[923,230],[1028,273],[1020,318],[929,292],[869,333]],'#C76431'),
            polygon([[1539,464],[1443,520],[1422,572],[1467,588],[1504,548],[1558,536]],'#C76431')]
for y in range(373,418,12): shapes4.append(line(1407,y,1464,y+24,'#ECA737',3))
for x in range(1010,1070,13): shapes4.append(line(x,685,x-8,759,'#F0CC31',3))

shapes5 = [polygon([[79,731],[710,657],[739,831],[95,851]],'#CEA8C8'),
           polygon([[247,529],[596,526],[557,767],[294,767]],'#DDAFB4'),
           ellipse(247,510,349,55,'#685260'),
           polygon([[273,551],[568,551],[540,735],[311,735]],'#BA8F8F'),
           line(421,529,438,182,'#683E66',9),line(432,363,238,254,'#683E66',5),
           line(434,333,609,246,'#683E66',5),
           leaf(162,196,216,115,'#B285C5'),leaf(494,187,219,113,'#8B78B1'),
           leaf(255,329,187,102,'#956DAC'),leaf(439,364,258,126,'#B596CE'),
           leaf(346,99,235,133,'#BA9ACB')]
for j in range(9):
    shapes5 += [line(420,550,333+j*20,704,'#6F4666',3)]
for j in range(6):
    shapes5 += [line(201+j*24,218,296+j*15,272,'#624969',2),
                line(505+j*24,218,581+j*15,274,'#624969',2)]
shapes5 += [polygon([[75,593],[180,536],[304,604],[299,647],[198,615],[107,658]],'#C48490'),
            polygon([[104,564],[169,536],[208,558],[157,590]],'#DFB0B8')]

configs = [
 {'name':'빛과 크기를 고르는 컬러 사진 편집','x':80,'w':720,'bg':'#E1F2F5','ink':'#122F37','title_path':GOTHIC,'title_index':6,'title_size':108,
  'body_path':GOTHIC,'body_size':30,'subtitle_size':36,'shapes':shapes1,'reference_ids':['BP2025-035','BP2024-077'],
  'relationship':'Three deliberately edited photographic scales at the right—hand-supported small pot, a close transmitted leaf, and a mature tree with its pot—make the practical choice of scale/light visible. A broad, unboxed reading column at the left remains continuous from Title to body and visiting information.',
  'style':'Luminous, cool full-colour editorial photography with clear cyan daylight, olive natural leaves, a believable warm hand and neutral mineral pots. Use physically credible transmitted leaf veins, surface texture and attached shadows. Crisp close-crop editing, wide photographic tonal range and open bold sans Title create alert freshness; body stays precise regular printing, without simulated camera text.',
  'scene':'A hand genuinely supports a small nursery pot from below; the larger tree has a different scale and established woody stem; a tight leaf crop shows light through living tissue. Join these three selected distances as an intentional editorial comparison, with clean straight crop boundaries rather than a decorative botanical frame.',
  'geometry':['Right upper region x840–1550,y40–310 holds the supported small pot and distinct close-leaf crop.','Right lower region x840–1550,y334–850 holds a mature tree, legible pot and attached floor shadow; branches are cropped with intention.'],
  'emotion':'Fresh, attentive and inviting; a person can imagine choosing the right scale for home.'},
 {'name':'돌봄의 접촉을 그리는 코발트 회화','x':80,'w':720,'bg':'#182A78','ink':'#F5EFD8','title_path':MYUNGJO,'title_index':0,'title_size':100,
  'body_path':GOTHIC,'body_size':30,'subtitle_size':36,'shapes':shapes2,'reference_ids':['east-FNT-04','BP2025-061'],
  'relationship':'A large, articulated forearm and watering vessel lead into a rooted upright plant at the right; the pour terminates in the soil opening, and the planted vessel has an attached painted shadow. The left Title/body/visit column may share M1’s effective order while retaining a wholly different drawn colour world.',
  'style':'Deep ultramarine, warm vermilion and pale ochre form a deliberate gouache painting. Broad matte pigment planes, dry-brush edges inside substantial forms and controlled light/shadow make the caring gesture readable. A large contrast-stroke Korean Title feels painted in rhythm but remains clearly typeset; the body and small information use calm regular sans anatomy, never brush-corrupted glyphs.',
  'scene':'Paint one observable caring action: a mature hand grips a watering vessel and a short stream lands at the exposed soil, beside upward branching houseplant leaves. Warm hand planes and the red vessel cross the cool blue plant shadows. Use weight-bearing contact, credible wrist and grip, a consistent pouring direction and a stable pot opening, with no cute characters or toy rendering.',
  'geometry':['Right x928–1379,y277–537 contains articulated forearm, grip, vessel/spout and short water trajectory.','Right x1267–1571,y336–743 contains connected stems, leaves and rooted pot; a broad dark attached shadow anchors the scene.'],
  'emotion':'Intimate, vivid and affectionate; tending a plant is an everyday pleasure.'},
 {'name':'재배자의 손과 흙을 보는 흑백 다큐멘터리','x':820,'w':700,'bg':'#151A1D','ink':'#E9EEEB','title_path':GOTHIC,'title_index':6,'title_size':108,
  'body_path':GOTHIC,'body_size':30,'subtitle_size':36,'shapes':shapes3,'reference_ids':['BP2024-068','BP2025-009'],
  'relationship':'Three close photographic passages at the left follow supporting a plant, touching its rootball/soil, and an established planted result. The visual rhythm is made by working hands and material contacts rather than leaf decoration. A right-hand readable column links the grower story to the real visit and care offer.',
  'style':'Tactile monochrome documentary photography, silver highlights and deep charcoal shadows. Use deliberately different crop distances, fine controlled grain, real skin creases, soil particles and roots; focus follows contact rather than decorative blur. A large firm modern Korean sans Title and crisp regular body give the photographic sequence a direct, assured voice. Retain midtone detail and clean hand anatomy rather than crushed black silhouettes.',
  'scene':'Edit close observations of plant work: two hands support a small pot/rootball, fingers release soil around roots, and a grown plant sits stably in its pot. Show actual physical contacts and connected roots, not an illustrated hand icon or pseudo-archival stamps. These are three visual moments of the supplied caring theme, without adding a printed timetable or claiming a real person/place.',
  'geometry':['Left x45–735,y42–304 holds hands supporting a small rootball/pot and its attached stem.','Left x45–735,y326–559 contains the root-and-soil contact close-up; x45–735,y581–854 gives the established potted plant.'],
  'emotion':'Grounded, hands-on and trustworthy; care knowledge has substance and contact.'},
 {'name':'고르는 동작을 새기는 시트론 잉크 삽화','x':80,'w':720,'bg':'#F0E740','ink':'#42122B','title_path':GOTHIC,'title_index':6,'title_size':110,
  'body_path':GOTHIC,'body_size':30,'subtitle_size':36,'shapes':shapes4,'reference_ids':['BP2025-046','east-SM-03'],
  'relationship':'Two differently branching plants and two deliberate hands create a comparison by habit, scale and handling. The bright field is occupied by chunky printed plant/hand forms and their weight-bearing pots, not a passive information board. The left Title/body sequence can remain familiar while the image, letter voice and colour rhythm are markedly different.',
  'style':'A vivid citron and aubergine ink world with restrained burnt-orange touch points. Hand-drawn lithographic contours, chunky flat plant masses, sparse directional hatching and precise overprinted silhouettes make a confident graphic illustration. Use real-looking plant habit and adult hands, with irregular but controlled drawn edges. The Title has generous bold Korean sans shape and decisiveness; regular body is sharply printed, separated from the image’s grain.',
  'scene':'A hand gently tests the scale of a compact upright plant while another supports the broad-leaf plant at the edge of its pot. Distinguish the two growing habits and keep hand/pot/stem contact readable. Make the choice feel active through reach and touch, without adding fake comparison labels, arrows, numbers or a cute shopping mascot. The image is an authored ink illustration, not a 3D clay pot or leaf wreath.',
  'geometry':['Right x865–1133,y344–800 forms a compact upright branching plant and a reaching hand.','Right x1281–1558,y270–800 forms a taller broad-leaf plant and supporting hand, with ink hatching tied to leaf/pot surfaces.'],
  'emotion':'Open, energetic and social; exploring the market has the confidence of a lively printed cultural poster.'},
 {'name':'자라는 구조를 살피는 식물 단면 드로잉','x':800,'w':750,'bg':'#EFE0E8','ink':'#4B2852','title_path':MYUNGJO,'title_index':0,'title_size':100,
  'body_path':MYUNGJO,'body_size':29,'subtitle_size':35,'shapes':shapes5,'reference_ids':['BP2025-069','BP2024-093'],
  'relationship':'A large observational drawing at the left connects leaf veins, branching stem, soil and roots in a cutaway pot, with a hand at the rim to establish attentive care and scale. The right Title/body/visit alignment may share M3’s effective reading structure; a fine drawn colour layer and different letter anatomy create its own style.',
  'style':'Precise botanical pen contour with translucent plum, lavender and muted rose wash on a cool pink ground. Let a few large leaves have generous colour depth while root/vein lines remain fine, legible and connected; use restrained crosshatching only where form needs it. A broad, clearly dominant Korean contrast-stroke Title and mature regular serif body create an observant editorial voice. Footer sans supports the serif reading with compatible optical size; no antique labels, distressed paper or decorative seal.',
  'scene':'Draw one substantial living plant through a clean observational cutaway: a coherent stem joins differently oriented leaves above soil, and believable roots branch through the soil below; a grown hand attends the pot rim. Do not add scientific labels, species names, measurements or invented horticultural facts. The pot cutaway is an image device for understanding care, not a technical promise. Show stem/root continuity, hand contact and variation in leaf anatomy, without converting the drawing into toy modelling or ornamental edge foliage.',
  'geometry':['Left x162–713,y99–490 gives connected leaves, midribs and substantial stem.','Left x75–739,y510–851 holds the soil/root cutaway, attached pot shadow and tending hand; vein/root lines have deliberate thin-to-thick hierarchy.'],
  'emotion':'Curious, thoughtful and sensuous; a plant is a living structure to know and tend.'}
]

def text_regions(c):
    x,w,ink=c['x'],c['w'],c['ink']
    # The consistent reading scaffold is deliberately allowed; these are THIS-case choices.
    positions={5:(40,28,GOTHIC,2,38,48),1:(96,c['title_size'],c['title_path'],c['title_index'],130,144),
               2:(243,24,GOTHIC,0,34,40),3:(292,c['subtitle_size'],GOTHIC,2,46,58),
               4:(368,c['body_size'],c['body_path'],0,39,166),
               6:(563,34,MYUNGJO,0,46,46),7:(611,34,MYUNGJO,0,46,46),
               8:(659,30,GOTHIC,0,40,42),9:(711,28,GOTHIC,0,40,42),
               10:(753,28,GOTHIC,0,40,42),11:(807,28,GOTHIC,0,40,42),12:(849,24,GOTHIC,0,34,36)}
    result=[]
    for entry in range(1,13):
        y,size,path,index,spacing,height=positions[entry]
        lines=body_lines if entry==4 else [copy[entry-1]['text']]
        result.append({'entry':entry,'copy':copy[entry-1]['text'],'lines':list(lines),'fixed_newlines':False,
                       'x':x,'y':y,'align':'left','line_spacing':spacing,'area':{'width':w,'height':height},
                       'font':{'path':path,'index':index,'size':size},'color':ink})
    return result

directions=[]
measurements=[]
peer_differences={
 1:'M1 uses luminous cyan daylight, credible photographic texture and a three-distance comparison. M2 uses deep cobalt pigment planes, warm red/ochre hand-and-vessel contact and a broad contrast-stroke Title. Their left reading alignment may be shared.',
 2:'M2 gives the care gesture a continuous cobalt/vermillion gouache world and contrast-stroke Title; M1 has crisp cool photographic crop editing and a firm open sans Title. The distinction is image/colour/letter finish, not a compulsory new text order.',
 3:'M3 uses silver/charcoal photographic hand-and-soil contacts, a fine documentary grain and firm sans Title. M5 uses connected root/vein pen anatomy, plum/lavender translucent colour and a broad contrast-stroke Title with serif prose. A right reading rail may be shared.',
 4:'M4 uses chunky citron/aubergine printed silhouettes, adult reach/support gestures and sparse directional hatch marks. M1 uses cool full-colour lens detail and photographic scale comparison. Both can use a clear left Title/body rail without becoming one style.',
 5:'M5 builds the living structure through fine connected root/vein linework and translucent plum/rose washes, with mature serif prose and a contrast-stroke Title. M3 uses physical documentary photo contacts, silver highlights and a firm sans voice. Their right text alignment need not change.'
}
geometry_bounds={1:[[840,40,710,270],[840,334,710,516]],
                 2:[[928,277,451,260],[962,336,609,491]],
                 3:[[45,42,690,262],[45,326,690,528]],
                 4:[[843,230,290,570],[1281,270,277,530]],
                 5:[[162,99,551,391],[75,510,664,341]]}
for i,c in enumerate(configs,1):
    role=f'R22-C1-M{i}'
    regions=text_regions(c)
    guide={'canvas':{'width':1600,'height':900,'background':c['bg']},
           'shapes':c['shapes'],'text_blocks':[{k:v for k,v in r.items() if k!='entry'} for r in regions]}
    native_brief=(
        'Create one finished opaque flat landscape 16:9 poster. Use the supplied newly authored planning guide for actual copy anatomy, readable areas and substantive image contacts; implement the following completed style rather than reproducing its temporary shapes. '
        + c['style']+' '+c['scene']+' '+c['relationship']+' The intended feeling is '+c['emotion']+' '
        'Make the supplied main Title immediately recognisable through its broad size, weight/contrast and breathing space. Keep the market line as a subordinate eyebrow, the English name as a smaller companion, and the short explanatory sentence as a clear Subtitle. Keep the entire explanatory paragraph as mature regular body text with stable starts, natural Korean word spaces and meaning-led soft lines. Link its ending to the date/hour/place group, then nearby access/care information, invitation and URL along the same optical axis. Keep footer bodies clearly readable, with clean digits and original en-dashes drawn as distinct long midline bars. Choose harmonious Korean, Latin and numeral anatomy; image texture does not damage small text. '
        'All typography is part of the native finished image; do not add a later SVG/font overlay. Respect the supplied roles and all original punctuation without adding labels, numbers, logos, QR, watermarks or other print. This is a complete poster, with content-bearing imagery and precise letter finish. Print only the following twelve entries, each exactly once:\n\n'
        + '\n'.join(item['text'] for item in copy)
    )
    font_relation=(
        'Dominant bold open Korean sans Title, medium Subtitle and regular sans body, with compatible serif numerals for visibly long date/hour en-dashes.'
        if c['title_path']==GOTHIC else
        'Dominant broad contrast-stroke Korean Title; regular body and subordinate companion/footer maintain compatible widths, optical size and baselines. Date/hour serif numerals share the long midline en-dash form.'
    )
    peer = 2 if i==1 else 1 if i==2 else 5 if i==3 else 1 if i==4 else 3
    direction={
        'role':role,'ratio':'16:9','working_name_not_printed':c['name'],
        'whole_relationship':c['relationship'],'positive_direction':c['style']+' '+c['scene'],
        'native_positive_brief':native_brief,
        'hierarchy':{'primary':{'entry':1,'role':'Title; immediate main typographic anchor'},
                     'support':[{'entry':5,'role':'subordinate market eyebrow'},{'entry':2,'role':'subordinate English companion'},
                                {'entry':3,'role':'Subtitle explaining and bridging into body'}],
                     'explanation':{'entries':[4],'shape':body_lines},
                     'visit':{'entries':[6,7,8],'shape':'Date → hours → place, one continuous left-aligned group on the body axis.'},
                     'next_action':{'entries':[9,10,11,12],'shape':'Access/care pair, then nearby invitation/URL pair; same starts with modest functional spacing.'}},
        'body_line_groups':body_lines,
        'body_end_to_next_info':'The whole paragraph ends on the same optical left axis as the following date/hour/place group. A short clear gap changes from explanatory prose to larger, regular practical numerals. Access/care, invitation and URL continue that axis with functional group gaps; no random corner search.',
        'nearest_peer':{'role_id':f'R22-C1-M{peer}',
                        'structural_distinction':'Good reading order/alignment may be shared. Layout difference is optional and is not the claimed basis of style independence.',
                        'style_distinction':peer_differences[i]},
        'guide_geometry_concept':{'status':'Prospective, unrendered authored planning diagram; no image/quality proof.',
                                  'canvas':deepcopy(guide['canvas']),
                                  'image_geometry_concepts':[{'bounds':bounds,'content':s}
                                                             for bounds,s in zip(geometry_bounds[i],c['geometry'])],
                                  'text_regions':regions,'shapes':c['shapes'],
                                  'limits':['Actual copy only; region labels and internal entry numbers are never printed.',
                                            'New own shapes plan contact, scale and image/copy relationships, not source artwork.',
                                            'Colours and letterforms are chosen for this style; temporary geometry is not final image finish.',
                                            'Coordinates/font sizes/line count are planning choices for this case, not preservation conditions or quality gates.',
                                            'Guide fonts are actual measurable files; no claim that native output uses the exact font binary.']},
        'guide_spec':guide,
        'text_role_map':{'eyebrow':[5],'Title':[1],'English_companion':[2],'Subtitle':[3],'bodycopy':[4],
                         'footer_visit':[6,7,8],'footer_participation':[9,10],'footer_next_action':[11,12]},
        'font_system':{'families':['Apple SD Gothic Neo','AppleMyungjo'],'relation':font_relation,
                       'anatomy':'Stable mature Korean syllable proportions and interior spaces; compatible Latin/numeral optical height and baseline; precise word spacing. No arbitrary decorated style is mixed into body/footer.',
                       'weights':f"Title {c['title_size']}px {'Bold' if c['title_path']==GOTHIC else 'Regular contrast stroke'}, Subtitle {c['subtitle_size']}px Medium, body {c['body_size']}px Regular. Date/hour 34px AppleMyungjo Regular, other practical copy 28–30px Regular, English/URL24px Regular. These are this-case planning values only.",
                       'limits':'No fixed global size/font rule, installation or actual native font-file application guarantee.'},
        'optional_observation_ideas':[observation(k) for k in c['reference_ids']]
    }
    assert len(guide['text_blocks'])==12
    assert [b['copy'] for b in guide['text_blocks']]==[c['text'] for c in copy]
    for r in regions:
        assert ' '.join(r['lines'])==r['copy']
        f=ImageFont.truetype(r['font']['path'],r['font']['size'],index=r['font']['index'])
        ascent,descent=f.getmetrics()
        bounds=[];advances=[]
        for j,s in enumerate(r['lines']):
            advance=f.getlength(s);bb=f.getbbox(s,anchor='ls')
            baseline=r['y']+ascent+j*r['line_spacing']
            painted=[r['x']+bb[0],baseline+bb[1],r['x']+bb[2],baseline+bb[3]]
            assert 0<=painted[0] and painted[2]<=1600 and 0<=painted[1] and painted[3]<=900,(role,r['entry'],painted)
            assert advance<=r['area']['width'],(role,r['entry'],advance,r['area'])
            assert painted[1]>=r['y'] and painted[3]<=r['y']+r['area']['height'],(role,r['entry'],painted,r['area'])
            bounds.append(painted);advances.append(advance)
        measurements.append({'role':role,'entry':r['entry'],'font_family_style':list(f.getname()),
                             'font_size':r['font']['size'],'line_advances':advances,'painted_bounds':bounds,
                             'planned_area':r['area'],'measurement_only':'Read-only font metrics and canvas bounds, not a rendered guide or poster quality assessment.'})
    directions.append(direction)

# Static technical schema and simple polygon checks only; no renderer invocation.
def orientation(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def segment_intersects(a,b,c,d):
    if max(a[0],b[0]) < min(c[0],d[0]) or max(c[0],d[0]) < min(a[0],b[0]):return False
    if max(a[1],b[1]) < min(c[1],d[1]) or max(c[1],d[1]) < min(a[1],b[1]):return False
    return orientation(a,b,c)*orientation(a,b,d)<=0 and orientation(c,d,a)*orientation(c,d,b)<=0

polygon_count=0
for direction in directions:
    for s in direction['guide_spec']['shapes']:
        if s['type'] in ['rect','ellipse']:
            assert s['width']>0 and s['height']>0
            assert 0<=s['x'] and 0<=s['y'] and s['x']+s['width']<=1600 and s['y']+s['height']<=900
        elif s['type']=='line':
            pad=s['stroke_width']/2
            for x,y in [(s['x1'],s['y1']),(s['x2'],s['y2'])]:assert pad<=x<=1600-pad and pad<=y<=900-pad
        else:
            ps=s['points'];assert len(ps)==len(set(map(tuple,ps)))
            for x,y in ps:assert 0<=x<=1600 and 0<=y<=900
            area=sum(ps[j][0]*ps[(j+1)%len(ps)][1]-ps[(j+1)%len(ps)][0]*ps[j][1] for j in range(len(ps)))
            assert area!=0
            for a in range(len(ps)):
                for b in range(a+1,len(ps)):
                    if b==a+1 or (a==0 and b==len(ps)-1):continue
                    assert not segment_intersects(ps[a],ps[(a+1)%len(ps)],ps[b],ps[(b+1)%len(ps)]),(direction['role'],ps,a,b)
            polygon_count+=1

font=ImageFont.truetype(MYUNGJO,34,index=0)
dash_fact={'font':'AppleMyungjo Regular','size':34,'en_dash_advance':font.getlength('–'),
           'hyphen_advance':font.getlength('-'),'en_dash_bbox':list(font.getbbox('–')),
           'hyphen_bbox':list(font.getbbox('-')),
           'scope':'Measured font geometry only. Original U+2013 is preserved in both supplied entries; no native pixel verdict.'}
assert dash_fact['en_dash_advance']>dash_fact['hyphen_advance']
plan={
 'schema_version':1,'case_id':'R22-C1','status':'prospective_style_first_plan_unrendered_unfrozen_no_quality_proof',
 'request':request,'copy':copy,'conditions':conditions,'assets':[],'count':5,'ratios':['16:9']*5,'styles':deepcopy(source['styles']),
 'roles':[{**deepcopy(r),'role_id':f'R22-C1-M{i}'} for i,r in enumerate(source['roles'],1)],
 'common_constraints':[
  'Latest human style-first preference supersedes all-five different layout obligations; good reading order/alignment may be shared.',
  'Main Title is immediately recognisable. Market eyebrow, English companion, Subtitle, entire regular body and useful practical roles are distinct and harmonious.',
  'All12 supplied entries once, exact meaningful word spaces/punctuation, no invented print/logo/QR.',
  'Substantive content imagery expresses choosing/caring, not ornamental leaf framing or passive solid-field gothic information templates.',
  'Style identity is the authored whole image expression/editing, colour/contrast, letter voice, material/finish and mood; no fixed five-family menu or unique-value counts.',
  'Plan guides are prospective own shapes and actual-font copy, not source artwork, returned image editing or native final artwork.',
  'The native maker receives only its own actually viewed guide after coordinator rendering and the positive complete style brief; final typography remains native.',
  'Existing attempt/correction limits, assets[] and independent single-poster output conditions remain as supplied.',
  'No new quality gate, scoring, pixel-size preservation requirement, installation or source-artwork re-opening requirement.'
 ],
 'directions':directions,
 'design_provenance':{
  'source_request':str(SOURCE),'source_case_id':'R22-C1','matched_previous_request':str(MATCHED_SOURCE),'instruction_basis':[
   'Latest human styles markedly different, suitable good layouts may be shared.',
   'Latest human Title-only/Title+body and preceding explicit role hierarchy/font harmony.',
   'Z has been adopted by the coordinator after scope audit: candidate-style-first-ideas style-first scope plus optional source-idea memo. This design remains prospective and unrendered.'
  ],'schema_example_only':str(ROOT/'drafts/x-five-design/plan-hierarchy-v3.json'),
  'source_use':'Only schema keys of prior plan inspected; optional accumulated actual-observation text for image editing/material/colour ideas. No old plan content or source raster borrowed.',
  'not_opened':['Source raster artwork','Old poster pixels','Critic scores/raw transcripts','Old plan direction content'],
  'execution':{'native_calls':0,'guides_rendered':0,'child_agents':0,'critics_run':0},
  'font_measurement_only':'Read-only existing fonts through Pillow ImageFont metrics. No guide canvas/render/poster created and no font installed.',
  'measurements':measurements,'date_hour_dash_measurement':dash_fact,
  'case_conservation':'Exact authoritative R22 request,copy,conditions,styles,roles,count,ratios,assets. Relative to R21, only the explicitly supplied style/layout sentence and corresponding style condition are amended; all12 copy and other fields remain exact.',
  'prospective_condition_amendment':{'index':2,'original':matched_source['conditions'][2],'replacement':conditions[2],
                                   'authority':'Authoritative R22 case exact string, replacing the earlier short prospective paraphrase.'},
  'development_limit':'One prospective matched development five after closed R21; not held-out, causal isolation or quality proof.',
  'parent_plan':str(OUT/'plan-prospective-v1.json'),
  'revision_reason':'New five style identities from content and observations; no prior five-plan copy or cream/green/terracotta house style. After R22 case preparation, only authoritative case/provenance metadata was reconciled; directions/guide geometry/actual copy/positive style briefs remain unchanged.',
  'adopted_candidate':'Z',
  'entry_numbering':'1-based internal metadata only; guide_spec text_blocks contain no entry metadata.',
  'candidate_12_file_sha256':{str(p.relative_to(SKILL)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(SKILL.rglob('*')) if p.is_file()},
  'candidate_path':str(SKILL),'initial_style_first_draft':str(INITIAL_SKILL),
  'optional_idea_memo_read':str(SKILL/'references/visual-research.md'),
  'static_checks':{'directions':5,'copy_regions':60,'copy_reconstruction_exact':True,'text_painted_canvas_bounds':True,
                   'text_planned_area_fit':True,'shape_canvas_bounds':True,
                   'simple_polygons_without_nonadjacent_cross_or_touch':True,'polygon_count':polygon_count,
                   'native_final_font_binary_claim':False,'quality_assessed':False}
 }
}
assert plan['copy']==source['copy'] and plan['assets']==source['assets'] and plan['count']==source['count'] and plan['ratios']==source['ratios']
assert len(plan['design_provenance']['candidate_12_file_sha256'])==12
OUT.mkdir(parents=True,exist_ok=True)
target=OUT/'plan.json'
if '--revise-own-unfrozen-plan' in sys.argv:
    existing=json.loads(target.read_text())
    assert existing['status']=='prospective_style_first_plan_unrendered_unfrozen_no_quality_proof'
    assert existing['copy']==copy and existing['request']==request
else:
    assert not target.exists(),'New prospective artifact only; preserve previous versions.'
target.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'plan':str(target),'directions':5,'copy_regions':60,'native_calls':0,'guides_rendered':0,'date_hour_dash_measurement':dash_fact},ensure_ascii=False,indent=2))
