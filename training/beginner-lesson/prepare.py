from pathlib import Path
import urllib.request,hashlib,json,re
from pypdf import PdfReader
R=Path(__file__).resolve().parent;A=R/'assets';A.mkdir(parents=True,exist_ok=True)
items=[('paper.html','https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0328041'),('paper.pdf','https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0328041&type=printable')]
records=[]
for name,url in items:
    data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read()
    if name.endswith('.pdf'):assert data.startswith(b'%PDF-')
    (A/name).write_bytes(data);records.append(dict(file='assets/'+name,url=url,sha256=hashlib.sha256(data).hexdigest(),retrieved='2026-10-17',license='CC BY 4.0',attribution='Heinrich et al. PLOS ONE 20(8): e0328041 (2025)'))
reader=PdfReader(A/'paper.pdf');locations=[]
for i,p in enumerate(reader.pages,1):
    text=' '.join(p.extract_text().split())
    for phrase in ['does not directly assess','prompt template for grading']:
        pos=text.lower().find(phrase)
        if pos>=0:locations.append(dict(phrase=phrase,pdf_page=i,context=text[max(0,pos-150):pos+300]))
assert len(locations)==2,locations
from pdf2image import convert_from_path
convert_from_path(str(A/'paper.pdf'),first_page=1,last_page=1,dpi=130,poppler_path='C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin')[0].save(A/'page1.png')
(R/'sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'source-locations.json').write_text(json.dumps(locations,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(locations,ensure_ascii=False,indent=2))
