from pathlib import Path
import json,hashlib
from PIL import Image,ImageChops
r=Path(__file__).resolve().parent
m=json.loads((r/'assembly-manifest.json').read_text('utf-8'));rev=m['revision'];assert rev=='course-r3'
rows=[]
for n in range(1,241):
 before=r/'renders/course-r2'/f'slide-{n:03}.png';after=r/'renders'/rev/f'slide-{n:03}.png'
 with Image.open(before) as a,Image.open(after) as b:
  assert a.size==b.size
  bbox=ImageChops.difference(a.convert('RGB'),b.convert('RGB')).getbbox()
 rows.append(dict(page=n,identical_rgb=bbox is None,changed_bbox=bbox,baseline_sha256=hashlib.sha256(before.read_bytes()).hexdigest(),sha256=hashlib.sha256(after.read_bytes()).hexdigest()))
changed=[q['page'] for q in rows if not q['identical_rgb']]
expected=[41,45,51,181,183,187,189,193,203,205,208];assert changed==expected,changed
record=dict(revision=rev,baseline='course-r2',pages=240,identical_rgb=240-len(changed),changed_pages=changed,rows=rows,scope='逐像素比较实际合并课件渲染；相同页可沿用前版视觉审阅记录，修改页需实际打开审阅。')
(r/'revision-comparison.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n','utf-8',newline='\n')
print('240 pages compared;',240-len(changed),'RGB-identical; changed:',changed)
