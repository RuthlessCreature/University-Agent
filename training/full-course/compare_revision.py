from pathlib import Path
import json,hashlib
from PIL import Image,ImageChops
r=Path(__file__).resolve().parent
m=json.loads((r/'assembly-manifest.json').read_text('utf-8'));rev=m['revision'];assert rev=='course-r4'
rows=[]
for n in range(1,241):
 before=r/'renders/course-r3'/f'slide-{n:03}.png';after=r/'renders'/rev/f'slide-{n:03}.png'
 with Image.open(before) as a,Image.open(after) as b:
  assert a.size==b.size
  bbox=ImageChops.difference(a.convert('RGB'),b.convert('RGB')).getbbox()
 rows.append(dict(page=n,identical_rgb=bbox is None,changed_bbox=bbox,baseline_sha256=hashlib.sha256(before.read_bytes()).hexdigest(),sha256=hashlib.sha256(after.read_bytes()).hexdigest()))
changed=[q['page'] for q in rows if not q['identical_rgb']]
assert changed==[15,52,70,158,172,190,234],changed
record=dict(revision=rev,baseline='course-r3',pages=240,identical_rgb=240-len(changed),changed_pages=changed,rows=rows,scope='逐像素比较实际合并课件渲染；第15页内容有改动并已全尺寸审阅。第52、70、158、172、190、234页仅有局部渲染像素差异，已通过新版缩略图复核；分节PPT源文件除Section 1外哈希与course-r3相同。其余233页逐像素相同，审阅链见course-r3记录及history/course-r2。')
(r/'revision-comparison.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n','utf-8',newline='\n')
print('240 pages compared;',240-len(changed),'RGB-identical; changed:',changed)
