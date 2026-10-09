from pathlib import Path
import json
R=Path(__file__).resolve().parent
case=json.loads((R.parents[2]/'planning/single-five-case.json').read_text())['cases'][0]
C=[x['text'] for x in case['copy']]
serif='/System/Library/Fonts/Supplemental/AppleMyungjo.ttf'
sans='/System/Library/Fonts/AppleSDGothicNeo.ttc'
def block(i,x,y,w,h,size,lines=None,face=serif,index=0,spacing=None):
 return {'copy':C[i],'lines':lines or [C[i]],'fixed_newlines':False,'x':x,'y':y,'align':'left','line_spacing':spacing or size*1.32,'area':{'width':w,'height':h},'font':{'path':face,'index':index,'size':size},'color':'#243139'}
shapes=[]
def poly(points,fill):shapes.append({'type':'polygon','points':points,'fill':fill})
def line(x1,y1,x2,y2,stroke,width):shapes.append({'type':'line','x1':x1,'y1':y1,'x2':x2,'y2':y2,'stroke':stroke,'stroke_width':width})
def ellipse(x,y,w,h,fill):shapes.append({'type':'ellipse','x':x,'y':y,'width':w,'height':h,'fill':fill})
# A single diagonal repair image: two arms brace the chair while the garment
# traverses its lower joint. These shapes indicate subject scale/crop only.
poly([[745,0],[1672,0],[1672,941],[790,941],[834,631],[720,319]],'#9EADB3')
poly([[931,20],[1147,35],[1230,400],[1063,421],[965,219]],'#596B75')
poly([[1422,21],[1672,69],[1668,273],[1443,327],[1335,224]],'#6D7E88')
poly([[819,245],[1050,181],[1188,233],[1181,315],[1012,316],[866,357]],'#D7DEE1')
poly([[1391,240],[1256,300],[1170,331],[1126,268],[1285,229]],'#D7DEE1')
line(947,343,1367,399,'#3C505C',30)
line(965,339,924,720,'#3C505C',27)
line(1329,383,1302,779,'#3C505C',30)
line(955,450,1330,491,'#3C505C',25)
line(951,506,1340,542,'#3C505C',25)
poly([[926,627],[1321,642],[1464,758],[1030,743]],'#657882')
line(1033,737,975,921,'#3C505C',28)
line(1428,753,1505,922,'#3C505C',28)
poly([[1160,603],[1226,558],[1328,587],[1390,553],[1510,607],[1603,756],[1519,811],[1434,715],[1416,918],[1159,916],[1153,705],[1062,748],[1000,666]],'#BFCACF')
poly([[1244,723],[1344,709],[1360,816],[1242,831]],'#657882')
for j in range(5):line(1252+j*19,723,1250+j*19,738,'#E7ECEE',3)
poly([[750,753],[895,706],[1106,765],[1183,748],[1212,799],[1125,838],[964,810],[824,874]],'#596B75')
ellipse(1166,746,81,71,'#D7DEE1')
line(1197,773,1288,784,'#3C505C',7)
text=[block(5,54,26,660,90,72),block(6,58,116,650,54,39,face=sans),
 block(0,54,190,650,80,65),block(1,58,277,630,48,31,face=sans),
 block(2,58,332,650,54,39),
 block(3,58,407,660,182,42,lines=['헐거워진 의자와 찢어진 옷을','가져오세요. 이웃 수리자와 도구를','나누며 다시 쓰는 방법을 배웁니다.'],spacing=55),
 block(4,58,602,650,49,38,face=sans,index=2),block(7,58,658,645,45,37,face=sans),
 block(8,58,710,650,46,36,face=sans),block(9,58,766,650,46,36,face=sans,index=2),
 block(10,58,817,660,44,36,face=sans),block(11,58,882,650,42,34,face=sans)]
spec={'canvas':{'width':1672,'height':941,'background':'#E4E9EC'},'shapes':shapes,'text_blocks':text}
p=R/'guide-v1.spec.json'
with p.open('x') as f:json.dump(spec,f,ensure_ascii=False,indent=2);f.write('\n')
with (R/'direction-draft.json').open('x') as f:json.dump({'role':'R18-C1-M5','ratio':'16:9','name':'날짜에서 시작하는 수리 인쇄면','organization':'Date and time are the upper-left entry of a single continuous left information column. A full-height diagonal chair-joint and garment-repair linocut image occupies the other half, with hands and textiles reaching into the column edge. No twin footer groups or center-title island.','concept':'Useful repair is a shared physical gesture: two hands brace a chair joint while another stitches a garment draped across its seat.','image_grammar':'Two-color confident flat linocut/woodcut image with large angular cuts and bounded tactile grain, dark petrol and oxidized red against warm ivory. Graphic cropped action fills the entire right half and intersects the information boundary at deliberate intervals. No toy render, friendly blob clipart, glassy objects, passive blank room or tiny accessory.','body_flow':'Date/time lead to a moderate single-line serif Korean title, then companion identification and the proposition. Three generous serif sentence lines meet the diagonal chair rails at their right edge; the next stable left start belongs to the event/place and participation sequence beneath. Practical information is one continuous spine, not two footer cards. The large date is a functional entry, not a decorative calendar sticker.','type':'Calm Korean serif body with open mature counters, thin-thick distinction that survives 720px usage; sturdy exact sans for the practical list, proportional Latin and numerals. Guide serif is AppleMyungjo only as shape reference, not final file-application claim.','distinctness':'Nearest single-spine direction M1 is centered within a continuous scene and title-led. Here date is entry, all usable information remains in one side spine, and the cropped graphic action is one diagonal whole with a deliberate shared edge; neither a full-body photo scene nor a multi-frame montage.','guide_role':'Owned new code-native diagram only, optional supporting layout/type reference, not a client asset or fixed geometry'},f,ensure_ascii=False,indent=2);f.write('\n')
print(p)
