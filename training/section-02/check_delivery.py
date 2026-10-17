from pathlib import Path
import hashlib,json,re,sys,zipfile
from xml.etree import ElementTree as ET
from pypdf import PdfReader
root=Path(__file__).resolve().parent
rev=sys.argv[1] if len(sys.argv)>1 else 's2-r7'
data=json.loads((root/'lesson.json').read_text('utf-8'));refs=json.loads((root/'sources.json').read_text('utf-8'))
assert len(data)==18 and [d['n'] for d in data]==list(range(1,19))
assert all(k in refs for d in data for k in d['refs'])
assert all('Harness' in data[n-1]['title'] for n in [13,14,15,16])
ppt=root/'output'/f'高校科研AI课程_Section2_Agent与工作流_{rev}.pptx'
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
with zipfile.ZipFile(ppt) as z:
 slides=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
 notes=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)]
 assert len(slides)==len(notes)==18
 texts=[];tables=[]
 for i in range(1,19):
  x=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'));texts.append(' '.join(t.text or '' for t in x.findall('.//a:t',ns)))
  if x.findall('.//a:tbl',ns):tables.append(i)
 assert tables==[6,17]
 diagrams=[i for i in range(1,19) if i not in tables]
 for i in diagrams:
  x=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
  assert len(x.findall('.//p:cxnSp',ns))>=2,f'Missing editable connectors on page {i}'
 for i,d in enumerate(data):assert d['title'] in texts[i]
 assert not any(w in ' '.join(texts) for w in ['课堂练习','小组讨论','请提交','待补充','TODO'])
 assert not any(n.startswith('ppt/media/') for n in z.namelist()),'Unexpected raster source'
 for n in notes:
  assert 'https://' in z.read(n).decode()
pdf=root/'renders'/rev/(ppt.stem+'.pdf');assert len(PdfReader(pdf).pages)==18
images=list((root/'renders'/rev).glob('slide-*.png'));assert len(images)==18
validation=json.loads((root/'.build'/rev/'validation.json').read_text('utf-8'))
assert validation['finalSha256']==hashlib.sha256(ppt.read_bytes()).hexdigest()
assert validation['packageIntegrity']['findingCount']==0
assert validation['presentationLayout']['findingCount']==0
(root/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n','utf-8')
report={'revision':rev,'pptx_pages':18,'pdf_pages':18,'notes':18,'preview_images':len(images),'native_table_pages':tables,'native_diagram_pages':diagrams,'harness_pages':[13,14,15,16],'raster_images':0,'pptx_sha256':validation['finalSha256'],'scope':'文件、页数、原生对象和备注来源核验；不代表科研Agent全系统运行或用户教学验收。'}
(root/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
lines=['# Section 2 讲师稿','', '本节采用学术讲授。页面中的任务情境和框架为课程示例，不是模型执行记录。','']
for d in data:
 lines += [f"## 第 {d['n']} 页：{d['title']}",'',d['thesis'],'',d['notes'],'','详细内容：','']
 lines += [r if isinstance(r,str) else '：'.join(r) for r in (d.get('rows') or d.get('nodes'))]
 lines += ['','来源：']
 lines += [f"- [{refs[k]['title']}]({refs[k]['url']})；定位：{refs[k]['location']}" for k in d['refs']]
 lines += ['']
(root/'讲师稿.md').write_text('\n'.join(lines),'utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
