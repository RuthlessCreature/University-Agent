from pathlib import Path
import json,zipfile,hashlib,xml.etree.ElementTree as ET,re,shutil
from pypdf import PdfReader
R=Path(__file__).resolve().parent
src=R/'output/高校科研教学样课_研究设计_r3.pptx'; pdf=R/'renders/r3/高校科研教学样课_研究设计_r3.pdf'
with zipfile.ZipFile(src) as z:
    assert z.testzip() is None
    names=z.namelist();parts=[n for n in names if re.fullmatch(r'ppt/slides/slide\d+.xml',n)]
    notes=[n for n in names if re.fullmatch(r'ppt/notesSlides/notesSlide\d+.xml',n)]
    assert len(parts)==len(notes)==12
    chart=[n for n in names if re.fullmatch(r'ppt/(?:slides/)?charts/chart\d+\.xml',n)]
    books=[n for n in names if n.startswith('ppt/embeddings/') and n.endswith('.xlsx')]
    assert len(chart)==len(books)==1
    c=ET.fromstring(z.read(chart[0]));ns={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
    vals=[[int(float(v.text)) for v in ser.findall('.//c:val//c:numCache/c:pt/c:v',ns)] for ser in c.findall('.//c:ser',ns)]
    assert vals==[[95,5],[205,695]],vals
    assert sum(sum(row) for row in vals)==1000 and 95/(95+5)==.95
    text=' '.join(' '.join(ET.fromstring(z.read(n)).itertext()) for n in parts)
    assert not any(x in text for x in ['Lorem ipsum','Click to add','单击此处添加'])
assert len(PdfReader(pdf).pages)==12 and len(list((R/'renders/r3').glob('slide-*.png')))==12
with zipfile.ZipFile(R/'output/研究设计工作底稿.docx') as z:
    assert z.testzip() is None
    xml=z.read('word/document.xml').decode();assert 'AI 辅助编写' in xml and '不是基金申请书' in xml
    assert '<w:pBdr' not in xml and '<w:pBdr' not in z.read('word/styles.xml').decode()
assert len(PdfReader(R/'word-render/研究设计工作底稿.pdf').pages)==1
for record in json.loads((R/'sources.json').read_text('utf-8')):
    asset=R/record['file']
    if asset.exists():assert hashlib.sha256(asset.read_bytes()).hexdigest()==record['sha256']
report={'date':'2026-10-17','revision':'r3','pptx_slides':12,'speaker_notes':12,'pdf_pages':12,'editable_charts':1,'embedded_workbooks':1,'native_tables':1,'diagram_pages':[6,10],'classroom_counts':vals,'count_total':1000,'source_hashes_checked':True,'word_pages':1,'instructor_accepted':False,'powerpoint_native_open_checked':False,'cloud_or_model_called':False,'pptx_sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
(R/'delivery-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copyfile(R/'.build/r3/validation.json',R/'native-validation.json')
print(json.dumps(report,ensure_ascii=False,indent=2))
