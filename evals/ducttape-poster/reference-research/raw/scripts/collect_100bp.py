"""One image per archive work; downloads are candidates, never observations."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw
import datetime, hashlib, io, json, re

ROOT = Path('/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/research/reference-expansion/archive')
PAGES = Path('/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/research/reference-expansion/root/pages')
for part in ('pages', 'images', 'sheets'):
    (ROOT/part).mkdir(parents=True, exist_ok=True)

def get(url):
    return urlopen(Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=40).read()

class Article(HTMLParser):
    def __init__(self):
        super().__init__(); self.data={}; self.field=None; self.images=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if tag=='a' and 'href' in d: self.data.setdefault('page_url',d['href'])
        if tag in ('h2','p'):
            self.field={'PostPosters-names':'author','PostPosters-country':'country','PostPosters-year':'year','PostPosters-title':'title'}.get(d.get('class'))
        if tag=='img' and 'data-srcset' in d: self.images.append(d)
    def handle_endtag(self, tag):
        if tag in ('h2','p'): self.field=None
    def handle_data(self, text):
        if self.field: self.data[self.field]=self.data.get(self.field,'')+text

html2025=(PAGES/'100bp-2025.html').read_text()
# The archive DOM exposes the prior-year filter value. Verify the derived page.
assert 'data-Posts-filter-value=2024' in html2025
url2024='https://100-beste-plakate.de/plakate/filter/jahr:2024/'
source2024=ROOT/'pages'/'2024.html'
if not source2024.exists(): source2024.write_bytes(get(url2024))
(ROOT/'pages'/'2025.html').write_text(html2025)
candidates=[]
for year,html in [('2025',html2025),('2024',source2024.read_text())]:
    for n,raw in enumerate(re.findall(r'<article.*?</article>',html,re.S),1):
        p=Article();p.feed(raw)
        if not p.images: continue
        choices=[]
        for part in p.images[0]['data-srcset'].split(','):
            v=part.strip().split()
            if len(v)>=2: choices.append((int(v[1].rstrip('w')),v[0]))
        width,url=max(choices)
        candidates.append({'id':f'BP{year}-{n:03}',**{k:v.strip() for k,v in p.data.items()},'archive_url':f'https://100-beste-plakate.de/plakate/filter/jahr:{year}/','image_url':url,'series_images_available':len(p.images),'series_images_selected':1,'status':'unviewed candidate'})

def download(row):
    p=ROOT/'images'/(row['id']+'.jpg')
    try:
        data=p.read_bytes() if p.exists() else get(row['image_url'])
        im=Image.open(io.BytesIO(data));im.load();p.write_bytes(data)
        return {**row,'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'width':im.width,'height':im.height,'actual_viewed':False}
    except Exception as e: return {**row,'status':'unavailable','error':str(e)[:200]}

with ThreadPoolExecutor(max_workers=4) as pool:
    rows=list(pool.map(download,candidates))
with (ROOT/'downloaded.json').open('x') as f: json.dump({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selection':'first image per archive article; no color/mockup multiplication','rows':rows},f,ensure_ascii=False,indent=2)
valid=[r for r in rows if 'path' in r]
for n in range(0,len(valid),8):
    group=valid[n:n+8]; sheet=Image.new('RGB',(1600,1250),'#eeeeee');draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(group):
        im=Image.open(r['path']).convert('RGB');im.thumbnail((390,570))
        ox=(i%4)*400;oy=(i//4)*625
        sheet.paste(im,(ox+(400-im.width)//2,oy+45+(570-im.height)//2))
        draw.text((ox+5,oy+5),r['id'],fill='black')
        draw.text((ox+5,oy+20),r['title'][:45],fill='black')
    sheet.save(ROOT/'sheets'/f'{n//8+1:02}.png')
print(json.dumps({'downloaded':len(valid),'unavailable':len(rows)-len(valid),'author_labels':len({r.get('author') for r in valid}),'actual_observed':0,'sheets':str(ROOT/'sheets')},ensure_ascii=False))
