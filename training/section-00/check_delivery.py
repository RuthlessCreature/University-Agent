"""Check deliverable files; teaching quality is recorded separately after visual review."""
from pathlib import Path
import hashlib, json, re, sys, zipfile
from xml.etree import ElementTree as ET
from pypdf import PdfReader

root = Path(__file__).resolve().parent
revision = sys.argv[1] if len(sys.argv) > 1 else 's0-r4'
plan = json.loads((root.parent / 'curriculum/course_structure_240.json').read_text('utf-8'))
assert sum(s['pages'] for s in plan['sections']) == 240
assert [s['id'] for s in plan['sections'] if 'harness' in s] == [2, 14]
assert 'Humanizer' in plan['sections'][3]['title']
materials = root / 'materials'
manifest = json.loads((materials / 'materials-manifest.json').read_text('utf-8'))
for item in manifest:
    assert hashlib.sha256((materials / item['file']).read_bytes()).hexdigest() == item['sha256']
pptx = root / 'output' / f'高校科研AI课程_Section0_{revision}.pptx'
ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
with zipfile.ZipFile(pptx) as archive:
    slides = [n for n in archive.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)]
    notes = [n for n in archive.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', n)]
    assert len(slides) == len(notes) == 4
    content = '\n'.join(' '.join(ET.fromstring(archive.read(n)).itertext()) for n in slides)
    for text in ['Harness', 'Humanizer', '370', '110', '讲师演示中的材料、动作与结果']:
        assert text in content, text
    page4 = ' '.join(ET.fromstring(archive.read('ppt/slides/slide4.xml')).itertext())
    for filename in ['paper.pdf', 'penguins.csv', 'guide.json', 'template.docx']:
        assert filename not in page4, filename
    for n,minimum in [(2,3),(4,6)]:
        xml=ET.fromstring(archive.read(f'ppt/slides/slide{n}.xml'))
        assert len(xml.findall('.//{http://schemas.openxmlformats.org/presentationml/2006/main}cxnSp'))>=minimum
    notes_text='\n'.join(' '.join(ET.fromstring(archive.read(n)).itertext()) for n in notes)
    assert 'berkeley.edu/agentic-ai/slides/introduction_25.pdf' in notes_text
    for stale in ['延伸案例与练习','今天会跟着做哪些事','带着大家操作','此页是全课规划，不表示后续章节已制作']:
        assert stale not in content+notes_text
render = root / 'renders' / revision
assert len(PdfReader(render / (pptx.stem + '.pdf')).pages) == 4
assert len(list(render.glob('slide-*.png'))) == 4
result = {'revision': revision, 'slides': 4, 'notes': 4, 'pdf_pages': 4,
          'preview_images': 4, 'material_hashes_verified': len(manifest),
          'course_page_budget': 240, 'harness_sections': [2, 14],
          'editable_diagram_pages': [2,4], 'frontier_reference_pages_viewed':[6,10,19],
          'pptx_sha256':hashlib.sha256(pptx.read_bytes()).hexdigest(),
          'scope': '文件、页数、材料哈希与课程安排检查；不代表用户已接受教学内容或版式。'}
(root / 'checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
