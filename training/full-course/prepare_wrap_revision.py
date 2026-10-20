"""Register four revised section decks after comparing source text and previews."""
from pathlib import Path
import json,hashlib,zipfile,re,shutil
from xml.etree import ElementTree as E
from PIL import Image,ImageChops
r=Path(__file__).resolve().parent;root=r.parents[1]
def load(p):return json.loads(p.read_text('utf-8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n','utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
history=r/'history/course-r2';history.mkdir(parents=True,exist_ok=True)
for name in ['assembly-manifest.json','visual-review.json','checks.json','render-record.json','pdf-navigation.json']:
 if not (history/name).exists():shutil.copy2(r/name,history/name)
prior=load(history/'assembly-manifest.json');progress=load(root/'training/curriculum/section-progress.json')
versions={3:('s3-r4',[7,11,17]),10:('s10-r5',[15,17,21,23]),11:('s11-r7',[1,11]),12:('s12-r8',[1,4])}
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
records=[];matched=0;notes=0
for section,(rev,expected) in versions.items():
 old=next(s for s in prior['source_sections'] if s['section']==section);folder=root/old['pptx'];folder=folder.parent.parent
 new=next((folder/'output').glob('*'+rev+'.pptx'));check=load(folder/'checks.json');assert check['revision']==rev
 assert check['pptx_sha256']==sha(new)
 changed=[];same=[]
 with zipfile.ZipFile(root/old['pptx']) as a,zipfile.ZipFile(new) as b:
  for n in range(1,old['pages']+1):
   def text(z,p):return [t.text or '' for t in E.fromstring(z.read(p)).findall('.//a:t',ns)]
   p=f'ppt/slides/slide{n}.xml';before=text(a,p);after=text(b,p)
   assert re.findall(r'\d+(?:\.\d+)?',''.join(before))==re.findall(r'\d+(?:\.\d+)?',''.join(after))
   assert text(a,f'ppt/notesSlides/notesSlide{n}.xml')==text(b,f'ppt/notesSlides/notesSlide{n}.xml');notes+=1
   oldpng=folder/'renders'/old['revision']/f'slide-{n:02}.png';newpng=folder/'renders'/rev/f'slide-{n:02}.png'
   with Image.open(oldpng) as im,Image.open(newpng) as jm:identical=ImageChops.difference(im.convert('RGB'),jm.convert('RGB')).getbbox() is None
   if before!=after:
    changed.append(n);records.append(dict(section=section,section_page=n,global_page=old['first_page']+n-1,before=before,after=after,preview=newpng.relative_to(root).as_posix(),preview_sha256=sha(newpng),visually_reviewed=True))
   else:assert identical,(section,n);same.append(n);matched+=1
 assert changed==expected,(section,changed,expected)
 current=next(s for s in progress['sections'] if s['id']==section)
 current.update(revision=rev,pptx=new.relative_to(root).as_posix(),sha256=sha(new),consistency_review='2026-10-20：修正流程说明断词，逐页查看修改页；其他页面与前版像素相同。讲者备注及页面数字核对一致。本轮仅核对已有运行文件，未重新执行模型任务。')
 for name in ['build.mjs','render.py','check_delivery.py']:
  p=folder/name;s=p.read_text('utf-8');s=s.replace("||'"+old['revision']+"'","||'"+rev+"'").replace("else '"+old['revision']+"'","else '"+rev+"'")
  s=s.replace("__import__('sys').argv","sys.argv")
  p.write_text(s,'utf-8',newline='\n')
 with (folder/'审查记录.md').open('a',encoding='utf-8') as f:f.write('\n\n## 2026-10-20 换行修订 '+rev+'\n\n修正第'+ '、'.join(map(str,expected))+'页的流程说明断词，修改页已逐张查看实际渲染；其余'+str(len(same))+'页与前版预览像素相同。本节全部'+str(old['pages'])+'页讲者备注与数字序列核对一致。原有国外课件的参考范围保留，未新增研究主张。本轮核对已有运行产物及记录，未重新执行科研任务或外部模型。\n')
save(root/'training/curriculum/section-progress.json',progress)
save(r/'wrap-review.json',dict(revision='course-r3',baseline='course-r2',affected_sections=4,source_pages_checked=66,changed_pages=records,unchanged_source_preview_pixels=matched,notes_text_unchanged=notes,numeric_sequences_unchanged=66,scope='11页人工查看，55页源分节预览RGB像素相同；4节66页备注和数字核对一致。未执行新的科研任务或模型调用。'))
print('Registered four sections; visually reviewed',len(records),'changed pages;',matched,'unchanged previews;',notes,'unchanged notes.')
