from pathlib import Path
import json,zipfile,re,hashlib,xml.etree.ElementTree as ET,shutil
from pypdf import PdfReader
R=Path(__file__).resolve().parent;revision='b2';ppt=R/'output'/f'高校科研AI入门样课_读懂一篇论文_{revision}.pptx'
with zipfile.ZipFile(ppt) as z:
    assert z.testzip() is None
    slides=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
    notes=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)]
    assert len(slides)==len(notes)==12
    text=' '.join(' '.join(ET.fromstring(z.read(n)).itertext()) for n in slides)
    assert 'Ctrl+F' in text and 'learning outcomes' in text and '固定编号' in text
    assert not any(term in text for term in ['主动学习','召回率','标签','Lorem ipsum','单击此处添加'])
    rels=[n for n in z.namelist() if n.endswith('.rels')]
    assert any('https://doi.org/10.1371/journal.pone.0328041' in z.read(n).decode() for n in rels)
    assert b'<a:tbl>' in z.read('ppt/slides/slide9.xml')
pdf=R/'renders'/revision/(ppt.stem+'.pdf');assert len(PdfReader(pdf).pages)==12
assert len(list((R/'renders'/revision).glob('slide-*.png')))==12
original=PdfReader(R/'assets/paper.pdf');second=' '.join(original.pages[1].extract_text().split())
assert 'does not directly assess student learning outcomes' in second
third=' '.join(original.pages[2].extract_text().split());assert 'The prompt template for grading SAQs contains five parts' in third
for src in json.loads((R/'sources.json').read_text('utf-8')):
    p=R/src['file']
    if p.exists():assert hashlib.sha256(p.read_bytes()).hexdigest()==src['sha256']
doc=R/'output/论文阅读笔记.docx'
with zipfile.ZipFile(doc) as z:
    assert z.testzip() is None
    t=z.read('word/document.xml').decode();assert 'learning outcomes' in t and '第 2 页' in t and 'AI 辅助编写' in t
    assert '<w:pBdr' not in t and '<w:pBdr' not in z.read('word/styles.xml').decode()
assert len(PdfReader(R/'word-render/论文阅读笔记.pdf').pages)==1
report=dict(date='2026-10-17',revision=revision,slides=12,notes=12,pdf_pages=12,word_pages=1,doi_hyperlink=True,source_pdf_locations_checked=[2,3],native_table_page=9,instructor_accepted=False,beginner_user_test_completed=False,native_powerpoint_open_checked=False,external_model_called=False,pptx_sha256=hashlib.sha256(ppt.read_bytes()).hexdigest())
(R/'delivery-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copyfile(R/'.build'/revision/'validation.json',R/'native-validation.json')
print(json.dumps(report,ensure_ascii=False,indent=2))
