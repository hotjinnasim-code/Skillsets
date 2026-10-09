import json
from pathlib import Path

ROOT=Path.cwd().resolve()
GUIDES=ROOT/'guides'
GUIDES.mkdir(exist_ok=True)
GOTHIC='/System/Library/Fonts/AppleSDGothicNeo.ttc'
MYUNGJO='/System/Library/Fonts/Supplemental/AppleMyungjo.ttf'
request_path=Path('/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/planning/single-five-case.json')
case=json.loads(request_path.read_text(encoding='utf-8'))['cases'][0]
C=[x['text'] for x in case['copy']]


def rect(x,y,w,h,fill,stroke=None,sw=2):
    d=dict(type='rect',x=x,y=y,width=w,height=h,fill=fill)
    if stroke: d.update(stroke=stroke,stroke_width=sw)
    return d

def ellipse(x,y,w,h,fill,stroke=None,sw=2):
    d=dict(type='ellipse',x=x,y=y,width=w,height=h,fill=fill)
    if stroke:d.update(stroke=stroke,stroke_width=sw)
    return d

def poly(points,fill,stroke=None,sw=2):
    d=dict(type='polygon',points=points,fill=fill)
    if stroke:d.update(stroke=stroke,stroke_width=sw)
    return d

def line(x1,y1,x2,y2,color,sw):
    return dict(type='line',x1=x1,y1=y1,x2=x2,y2=y2,stroke=color,stroke_width=sw)

def text(i,x,y,w,h,size,spacing,lines=None,font=GOTHIC,index=2,color='#252B30'):
    return dict(copy=C[i],lines=lines or [C[i]],fixed_newlines=False,x=x,y=y,align='left',line_spacing=spacing,area=dict(width=w,height=h),font=dict(path=font,index=index,size=size),color=color)

# M3: asymmetric photographic edit, shown only by direct gray shapes.
s=[]
# Matched damage detail crops across the upper edge.
s += [rect(0,0,496,316,'#B1B8BD'),rect(520,0,445,316,'#C6CBCE')]
# Right action image widens and recesses around the paragraph's measured rag.
s += [poly([[986,0],[1672,0],[1672,941],[1346,941],[1346,596],[1320,523],[1284,446],[1284,346],[986,346]],'#ADB7BD')]
# Lower left close crop of garment, distinct from the top chair crop.
s += [poly([[0,338],[494,338],[494,941],[0,941]],'#BFC7CB')]
# Chair detail: rails, loosened tenon and the same split at hand scale.
s += [poly([[30,164],[315,150],[326,199],[38,213]],'#707D86'),poly([[319,137],[381,126],[431,312],[361,314]],'#849097'),rect(315,166,28,19,'#E5E7E8'),line(341,174,365,166,'#434F58',4),line(362,193,377,215,'#E2E5E6',5)]
s += [line(42,244,243,316,'#697780',24),line(288,230,317,316,'#7F8C95',31)]
# Clothing condition close crop with a real seam and displaced cloth edges.
s += [poly([[548,128],[763,100],[929,169],[910,310],[550,306]],'#949FA6'),poly([[665,180],[705,178],[690,214],[728,237],[697,270],[668,244],[635,227]],'#DCE0E2'),line(663,144,649,174,'#6F7C84',3),line(640,247,627,277,'#6F7C84',3)]
for x,y in [(633,215),(646,202),(659,192),(685,255),(706,245)]:s.append(line(x,y,x+13,y+5,'#56636B',2))
# Large shared chair repair contact, above the paragraph: two hands steady and turn.
s += [poly([[1030,254],[1087,227],[1166,254],[1170,291],[1121,311],[1079,279]],'#737F87'),poly([[1394,250],[1347,226],[1245,253],[1240,290],[1305,309],[1359,275]],'#89959D')]
s += [ellipse(1132,253,85,47,'#D3D8DB'),ellipse(1192,252,84,47,'#E0E3E5'),line(1178,273,1191,316,'#43515C',8),rect(1143,311,132,20,'#707D85'),line(1169,317,1175,339,'#E2E5E6',4)]
# Repeated chair rail at the lower right, extending beyond the photo opening.
s += [poly([[1419,385],[1505,364],[1538,706],[1455,727]],'#75838D'),poly([[1392,592],[1608,558],[1651,619],[1425,656]],'#64747E'),line(1480,688,1440,877,'#65747D',33),line(1589,636,1622,889,'#7B8891',32)]
s += [ellipse(1454,489,99,62,'#D3D9DC'),poly([[1642,420],[1642,475],[1555,535],[1516,508],[1541,479]],'#959FA6'),ellipse(1510,478,81,53,'#C8D0D4'),line(1520,528,1507,580,'#3C4C58',8),rect(1500,573,21,39,'#A9B2B8')]
# Lower left cuff crop frames the title without a page or prop staging.
s += [poly([[0,365],[151,349],[355,408],[456,526],[384,604],[206,501],[0,515]],'#88969F'),poly([[377,518],[447,496],[479,560],[409,594]],'#CED5D9'),line(408,529,434,558,'#4C5C67',4)]
s += [poly([[356,778],[423,740],[494,782],[494,941],[365,941]],'#8E9DA6'),line(411,795,433,887,'#D6DCDF',4)]
# Needle contact on the same coat crop continues from the action invitation.
s += [poly([[1336,786],[1482,742],[1647,779],[1672,890],[1498,930],[1346,892]],'#8B9CA7'),ellipse(1453,777,93,57,'#D3DADC'),ellipse(1540,802,92,58,'#DDE2E5'),line(1526,823,1560,803,'#3B4E5B',3),line(1536,818,1576,846,'#596C79',2)]
for x,y in [(1481,855),(1496,864),(1511,873),(1526,882)]:s.append(line(x,y,x+8,y-16,'#DDE3E6',3))

b=[
text(1,54,42,820,74,50,60,index=4),
text(2,1000,42,610,168,66,78,['버리는 대신,','함께 고칩니다.'],font=MYUNGJO,index=0),
text(3,560,362,760,208,44,64,['헐거워진 의자와 찢어진 옷을','가져오세요. 이웃 수리자와 도구를','나누며 다시 쓰는 방법을 배웁니다.'],font=MYUNGJO,index=0),
text(4,560,594,750,66,44,55,index=4),
text(5,560,660,406,70,54,64,index=2),
text(6,560,732,520,59,42,52,index=0),
text(7,560,787,520,59,42,52,index=2),
text(8,560,842,620,59,42,52,index=0),
text(0,54,655,455,206,78,100,['고쳐 쓰는','토요일'],font=MYUNGJO,index=0),
text(9,1000,665,598,63,44,55,index=4),
text(10,1000,741,610,119,44,59,['수리할 물건 한 가지를','가져오세요.'],index=2),
text(11,1000,866,610,59,42,51,index=2),
]
m3=dict(canvas=dict(width=1672,height=941,background='#E0E3E5'),shapes=s,text_blocks=b)

# M4: a single expressive human story, with a curved contact route, no panels.
s=[]
# Flow of coats and bodies creates a wide, shallow S without an arrow.
s += [poly([[571,46],[699,42],[841,188],[942,350],[989,578],[951,777],[776,920],[570,925],[675,803],[782,670],[796,488],[701,332],[587,214]],'#C2C9CD')]
# Entering neighbour: face and long expressive sleeve carry the loose chair toward contact.
s += [ellipse(714,112,97,115,'#A1ADB5'),poly([[734,220],[811,215],[907,388],[881,566],[770,581],[681,438],[664,328]],'#8C9BA5'),poly([[688,263],[640,230],[544,204],[513,235],[622,292],[683,325]],'#8798A4'),ellipse(492,203,69,52,'#D2DADD')]
s += [poly([[782,552],[864,546],[906,814],[865,925],[805,925],[816,801]],'#82939F'),poly([[727,542],[795,554],[765,764],[655,918],[571,918],[681,721]],'#97A6AF')]
# Partner leans in from right, wearing a coat whose open cuff is being mended.
s += [ellipse(966,221,94,113,'#BDC6CC'),poly([[995,333],[1075,354],[1123,446],[1048,628],[944,614],[901,438]],'#A8B5BD'),poly([[918,404],[972,387],[990,524],[899,637],[855,621],[934,505]],'#879AA8')]
s += [poly([[991,611],[1080,599],[1093,923],[1003,923]],'#8F9EAA'),poly([[935,600],[1003,624],[958,815],[906,923],[839,923],[886,776]],'#A5B0B8')]
# Readable chair structure: slats, seat, loose right rail, and legs.
s += [poly([[622,361],[651,353],[716,657],[685,670]],'#6E828F'),poly([[765,376],[794,369],[854,657],[825,665]],'#6E828F')]
for yy in [410,459,508]:s.append(poly([[650+(yy-410)*0.2,yy],[774+(yy-410)*0.2,yy-4],[780+(yy-410)*0.2,yy+16],[654+(yy-410)*0.2,yy+20]],'#94A5AF'))
s += [poly([[663,654],[850,628],[939,697],[749,742]],'#768C9B'),line(725,738,672,923,'#718797',24),line(879,726,911,922,'#7F929E',23),line(840,647,846,687,'#DBE0E3',9)]
# Two hands visibly share the same screwdriver while one steadies the loosened joint.
s += [poly([[788,559],[828,543],[863,608],[840,644],[809,605]],'#95A6B1'),ellipse(812,602,84,47,'#D0D9DD'),ellipse(857,597,76,50,'#E0E5E8'),line(864,627,853,681,'#344C5C',7),rect(843,673,18,30,'#AFBDC5'),ellipse(847,661,51,32,'#CBD6DC')]
# Repaired clothing on a lap: cuff opening, patch, thread and a second shared hand contact.
s += [poly([[554,642],[674,614],[761,686],[758,801],[676,842],[543,778]],'#9BAEBB'),poly([[538,710],[583,698],[612,764],[573,785]],'#CBD5DB'),poly([[615,729],[683,714],[704,773],[639,790]],'#C2CDD5')]
s += [ellipse(506,727,89,49,'#D4DDE2'),ellipse(586,761,85,48,'#E0E5E8'),line(589,766,631,754,'#334F62',3)]
for x,y in [(632,739),(650,734),(668,729),(681,749),(686,767)]:s.append(line(x,y,x+8,y+14,'#5A7485',3))
# Thread stays in image space, leads toward the registration pair at the left.
thread_pts=[(630,754),(603,789),(557,809),(527,806),(504,778),(485,731),(469,692),(439,656),(401,641)]
for a,z in zip(thread_pts,thread_pts[1:]):s.append(line(*a,*z,'#879AA8',3))
# A few strong hand/cloth contours replace surface dressing.
s += [line(756,157,790,169,'#637C8D',3),line(993,269,1025,276,'#78909F',3),line(571,715,589,750,'#687F90',3)]

b=[
text(10,54,50,657,160,60,76,['수리할 물건 한 가지를','가져오세요.'],index=2),
text(3,54,260,568,246,46,61,['헐거워진 의자와 찢어진','옷을 가져오세요.','이웃 수리자와 도구를 나누며','다시 쓰는 방법을 배웁니다.'],index=2),
text(4,54,526,600,68,46,58,index=4),
text(0,1140,75,478,205,80,98,['고쳐 쓰는','토요일'],font=MYUNGJO,index=0),
text(2,1140,294,478,136,48,63,['버리는 대신,','함께 고칩니다.'],font=MYUNGJO,index=0),
text(1,735,48,411,62,40,51,index=0),
text(5,1140,497,478,74,54,65,index=2),
text(6,1140,571,478,61,42,53,index=0),
text(7,1140,632,478,61,42,53,index=2),
text(8,1140,693,478,61,42,53,index=0),
text(9,54,773,495,64,44,54,index=4),
text(11,54,841,495,64,44,54,index=2),
]
m4=dict(canvas=dict(width=1672,height=941,background='#E2E6E9'),shapes=s,text_blocks=b)

for role,spec in [('m3',m3),('m4',m4)]:
    assert len(spec['text_blocks'])==12
    assert sorted(x['copy'] for x in spec['text_blocks'])==sorted(C)
    for x in spec['text_blocks']:assert ' '.join(x['lines'])==x['copy']
    p=GUIDES/f'r18-c1-{role}-guide-v1.spec.json'
    with p.open('x',encoding='utf-8') as f:json.dump(spec,f,ensure_ascii=False,indent=2);f.write('\n')
    print(p.name,len(spec['shapes']),len(spec['text_blocks']))
