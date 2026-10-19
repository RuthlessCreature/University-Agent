from pathlib import Path
from xml.etree import ElementTree as E
import csv,hashlib,json,math,re,statistics,sys,zipfile
import numpy as np
from pypdf import PdfReader
r=Path(__file__).resolve().parent;rev=sys.argv[1] if len(sys.argv)>1 else 's8-r4';p=r/'output'/f'高校科研AI课程_Section8_科研图表与技术路线_{rev}.pptx';a=json.loads((r/'figure-data.json').read_text('utf-8'));d=json.loads((r/'lesson.json').read_text('utf-8'))
raw=r/'figure-packet/penguins.csv';src=json.loads((r/'figure-packet/source.json').read_text('utf-8'));assert hashlib.sha256(raw.read_bytes()).hexdigest()==src['sha256']==a['source_sha256']
rows=list(csv.DictReader(raw.open(encoding='utf-8')));assert len(rows)==344;ad=[q for q in rows if q['species']=='Adelie' and q['sex'] in ['female','male'] and q['flipper_length_mm']!='NA'];assert len(ad)==146
for g in a['groups']:
 vals=[float(q['flipper_length_mm']) for q in ad if q['sex']==g['sex']];assert len(vals)==73==g['n'];assert math.isclose(statistics.mean(vals),g['mean'],abs_tol=1e-10);assert math.isclose(statistics.stdev(vals),g['sd'],abs_tol=1e-10)
 assert math.isclose(g['sd']/math.sqrt(73),g['se_iid'],abs_tol=1e-10)
assert sum(a['histogram']['series'][0]['values'])==sum(a['histogram']['series'][1]['values'])==73
route=json.loads((r/'figure-packet/route.json').read_text('utf-8'));assert len(route['nodes'])==len(route['edges'])==8
mx=E.parse(r/'figure-packet/研究技术路线.drawio');cells=mx.findall('.//mxCell');ids={n.attrib['id'] for n in cells if n.attrib.get('vertex')=='1'};assert all(n['id'] in ids for n in route['nodes']);assert {(n.attrib['source'],n.attrib['target']) for n in cells if n.attrib.get('edge')=='1'}=={(n['source'],n['target']) for n in route['edges']}
svg=E.parse(r/'figure-packet/研究技术路线.svg');assert len(svg.findall('.//{http://www.w3.org/2000/svg}polyline'))==8
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart'};diagram=[];chartpages=[];chartvalues=[];texts=[]
with zipfile.ZipFile(p) as z:
 slides=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)];notes=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)];assert len(slides)==len(notes)==16
 for i in range(1,17):
  x=E.fromstring(z.read(f'ppt/slides/slide{i}.xml'));txt=' '.join(t.text or '' for t in x.findall('.//a:t',ns));texts.append(txt);assert d[i-1]['title'] in txt
  if len(x.findall('.//p:cxnSp',ns))>=2:diagram.append(i)
  if x.findall('.//c:chart',ns):chartpages.append(i)
  assert not any(w in txt for w in ['课堂练习','TODO','请提交','占位'])
 assert diagram==[1,2,10,11,12,13,14,15,16] and chartpages==[3,4,6,8]
 x=E.fromstring(z.read('ppt/slides/slide14.xml'));assert len([e for e in x.findall('.//a:prstDash',ns) if e.attrib.get('val')=='dash'])==2
 x=E.fromstring(z.read('ppt/slides/slide11.xml'));assert len(x.findall('.//p:cxnSp',ns))==8
 charts=sorted([n for n in z.namelist() if re.fullmatch(r'ppt/(?:slides/)?charts/chart\d+\.xml',n)],key=lambda s:int(re.search(r'chart(\d+)\.xml',s).group(1)));assert len(charts)==7
 for n in charts:
  x=E.fromstring(z.read(n));vals=[]
  for ser in x.findall('.//c:ser',ns):
   vv=ser.findall('.//c:val/c:numRef/c:numCache/c:pt/c:v',ns) or ser.findall('.//c:yVal/c:numRef/c:numCache/c:pt/c:v',ns)
   vals.append([float(t.text) for t in vv])
  chartvalues.append(vals)
 means=[g['mean'] for g in a['groups']]
 for i in [0,2,3]:assert np.allclose(chartvalues[i][0],means,rtol=0,atol=1e-9)
 hist=[q['values'] for q in a['histogram']['series']];assert chartvalues[1]==hist==chartvalues[5]
 assert chartvalues[4]==[q['y'] for q in a['scatter']] and [len(q) for q in chartvalues[4]]==[73,73]
 scatter=E.fromstring(z.read(charts[4]));assert [n.attrib['val'] for n in scatter.findall('.//c:marker/c:symbol',ns)]==['circle','square'];assert 'noFill' in z.read(charts[4]).decode()
 for got,sex in zip(chartvalues[6],['female','male']):assert np.allclose(got,[q[sex] for q in a['years']],rtol=0,atol=1e-9)
 books=[n for n in z.namelist() if n.startswith('ppt/embeddings/') and n.endswith('.xlsx')];assert len(books)==7
 assert all('http' in z.read(n).decode() or 'local:' in z.read(n).decode() for n in notes)
assert len(PdfReader(r/'renders'/rev/(p.stem+'.pdf')).pages)==16 and len(list((r/'renders'/rev).glob('slide-*.png')))==16
brief=json.loads((r/'prompt-packet/mechanism-brief.json').read_text('utf-8'));execution=json.loads((r/'prompt-packet/执行状态.json').read_text('utf-8'))
assert len(brief['nodes'])==3 and len(brief['edges'])==2 and all(q['status']=='PENDING' and q['line']=='dashed' for q in brief['edges'])
assert not any(brief['execution'].values()) and execution['image_models_called']==[] and not execution['Nano_Banana_connected']
assert brief['openai_prompt'] in texts[13]
assert brief['midjourney_prompt'] in texts[15].replace('\n',' ')
assert '2026-05-12' in texts[13] and 'Nano Banana' in texts[15] and all('未执行' in texts[i] for i in [13,15])
mx=E.parse(r/'prompt-packet/机制假说示意.drawio');cells=mx.findall('.//mxCell');nodes={q.attrib['id']:q.attrib.get('value') for q in cells if q.attrib.get('vertex')=='1'}
assert all(nodes[q['id']]==q['label'] and q['label'] in texts[13] for q in brief['nodes'])
edges=[q for q in cells if q.attrib.get('edge')=='1'];assert {(q.attrib['source'],q.attrib['target']) for q in edges}=={(q['source'],q['target']) for q in brief['edges']} and all('dashed=1' in q.attrib['style'] for q in edges)
unchanged=[];same_previews=[]
prior=r/'output/高校科研AI课程_Section8_科研图表与技术路线_s8-r2.pptx'
with zipfile.ZipFile(prior) as old,zipfile.ZipFile(p) as new:
 for i in [n for n in range(1,17) if n not in [14,16]]:
  name=f'ppt/slides/slide{i}.xml';old_text=[t.text for t in E.fromstring(old.read(name)).findall('.//a:t',ns)];new_text=[t.text for t in E.fromstring(new.read(name)).findall('.//a:t',ns)];assert old_text==new_text;unchanged.append(i)
  if (r/'renders/s8-r2'/f'slide-{i:02d}.png').read_bytes()==(r/'renders'/rev/f'slide-{i:02d}.png').read_bytes():same_previews.append(i)
for stem in ['研究技术路线','Adelie喙长与鳍长']:
 for ext in ['svg','png']:assert (r/'figure-packet'/f'{stem}.{ext}').stat().st_size>1000
assert len(PdfReader(r/'figure-packet/Adelie喙长与鳍长.pdf').pages)==1
v=json.loads((r/'.build'/rev/'validation.json').read_text('utf-8'));sha=hashlib.sha256(p.read_bytes()).hexdigest();assert v['finalSha256']==sha and v['packageIntegrity']['findingCount']==v['presentationLayout']['findingCount']==0
(r/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),'utf-8');q={'revision':rev,'pages':16,'notes':16,'pdf_pages':16,'preview_images':16,'editable_connector_diagram_pages':diagram,'native_chart_pages':chartpages,'native_charts':7,'embedded_workbooks':7,'source_records':344,'scatter_records':146,'route_nodes':8,'route_edges':8,'mechanism_dashed_connectors':2,'pptx_sha256':sha,'unchanged_slide_text_vs_s8_r2':unchanged,'identical_preview_bytes_vs_s8_r2':same_previews,'prompt_examples':['GPT Image','Midjourney'],'image_models_called':execution['image_models_called'],'Nano_Banana_connected':False,'hypothesis_editable_nodes':3,'hypothesis_dashed_edges':2,'scope':'源CSV复算、原生图缓存、编辑源节点连接、虚线符号和导出文件检查。并有逐页视觉审查；不证明研究实施、机制或科研Agent全系统运行。'};(r/'checks.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),'utf-8');print(json.dumps(q,ensure_ascii=False,indent=2))
