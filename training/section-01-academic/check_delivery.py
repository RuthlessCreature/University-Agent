from pathlib import Path
import hashlib,json,re,sys,zipfile
from xml.etree import ElementTree as ET
from pypdf import PdfReader

root=Path(__file__).resolve().parent
rev=sys.argv[1] if len(sys.argv)>1 else 'a3'
lesson=json.loads((root/'lesson.json').read_text('utf-8'))
sources=json.loads((root/'sources.json').read_text('utf-8'))
assert len(lesson)==12
assert [d['n'] for d in lesson]==list(range(1,13))
assert all(k in sources for d in lesson for k in d['refs'])
data=json.loads((root/'sources/citation-data.json').read_text('utf-8'))
assert sum(x['n_all_references'] for x in data['chart_data'])==636
assert [x['fabrication_proportion'] for x in data['chart_data']]==[0.55,0.18]
pdf=PdfReader(root/'sources/citation-study.pdf')
assert len(pdf.pages)==8
paper_text=' '.join(p.extract_text() for p in pdf.pages)
assert all(x in paper_text for x in ['55%','18%','43%','24%','222','414'])
pptx=root/'output'/f'高校科研AI课程_Section1_学术讲授版_{rev}.pptx'
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
with zipfile.ZipFile(pptx) as z:
    slides=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
    notes=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)]
    charts=[n for n in z.namelist() if re.fullmatch(r'ppt/(?:slides/)?charts/chart\d+\.xml',n)]
    assert len(slides)==len(notes)==12 and len(charts)==1
    all_text=' '.join(' '.join(ET.fromstring(z.read(n)).itertext()) for n in slides)
    assert not any(t in all_text for t in ['课堂练习','组会','阅读笔记','注册账户'])
    for t in ['预训练','后训练','上下文','检索增强生成','预测','作者责任']:
        assert t in all_text,t
    native_tables=[i for i in range(1,13) if ET.fromstring(z.read(f'ppt/slides/slide{i}.xml')).findall('.//a:tbl',ns)]
    assert native_tables==[6,9,11]
    chart=ET.fromstring(z.read(charts[0]))
    values=[float(v.text) for v in chart.findall('.//c:val/c:numRef/c:numCache/c:pt/c:v',ns)]
    if not values:values=[float(v.text) for v in chart.findall('.//c:val/c:numLit/c:pt/c:v',ns)]
    assert values==[0.55,0.18],values
    assert any(n.startswith('ppt/embeddings/') and n.endswith('.xlsx') for n in z.namelist())
    for i in [2,3,4]:
        slide=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
        assert slide.findall('.//p:cxnSp',ns),i
render=root/'renders'/rev
assert len(PdfReader(render/(pptx.stem+'.pdf')).pages)==12
assert len(list(render.glob('slide-*.png')))==12
finalizer=json.loads((root/'.build'/rev/'validation.json').read_text('utf-8'))
assert finalizer['packageIntegrity']['status']=='pass'
assert finalizer['presentationLayout']['finding_count']==0
notes_text='# Section 1 讲师稿\n\n本节采用学术讲授形式。以下列出逐页讲法、概念限定与出处。\n\n'
for d in lesson:
    notes_text+=f'## {d["n"]:02d} {d["title"]}\n\n{d["notes"]}\n\n'
    notes_text+='\n'.join(f'- [{sources[k]["title"]}]({sources[k]["url"]})；{sources[k]["location"]}' for k in d['refs'])+'\n\n'
(root/'讲师稿.md').write_text(notes_text,encoding='utf-8')
result={'revision':rev,'pptx_pages':12,'notes':12,'pdf_pages':12,'preview_images':12,'native_tables':[6,9,11],
        'editable_chart_page':5,'embedded_chart_workbook':True,'chart_values_verified':[0.55,0.18],
        'editable_diagram_pages':[2,3,4],'classroom_exercise_pages':0,
        'research_pdf_pages':8,'source_pdf_sha256':hashlib.sha256((root/'sources/citation-study.pdf').read_bytes()).hexdigest(),
        'pptx_sha256':hashlib.sha256(pptx.read_bytes()).hexdigest(),
        'scope':'文件结构、源数据、可编辑对象和页数核验；不替代科学审查、用户教学验收或PowerPoint实测。'}
(root/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
