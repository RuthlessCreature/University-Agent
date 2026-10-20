"""Render the assembled PPTX itself, in bounded PDF raster batches."""
from pathlib import Path
import subprocess,sys,json,hashlib
from pdf2image import convert_from_path
from pypdf import PdfReader
r=Path(__file__).resolve().parent;rev=sys.argv[1] if len(sys.argv)>1 else 'course-r1'
p=r/'output'/f'高校科研AI培训课程_全课240页_{rev}.pptx';out=r/'renders'/rev;out.mkdir(parents=True,exist_ok=True)
profile=(r/'.build'/('lo-'+rev)).resolve().as_uri()
q=subprocess.run(['C:/Program Files/LibreOffice/program/soffice.exe','-env:UserInstallation='+profile,'--headless','--convert-to','pdf','--outdir',str(out),str(p)],capture_output=True,text=True,timeout=480)
pdf=out/(p.stem+'.pdf');assert pdf.exists(),q.stdout+q.stderr
assert len(PdfReader(pdf).pages)==240
poppler='C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin'
for first in range(1,241,8):
 pages=convert_from_path(pdf,dpi=96,first_page=first,last_page=min(first+7,240),poppler_path=poppler)
 for n,im in enumerate(pages,first):im.save(out/f'slide-{n:03d}.png')
 print('Rendered',min(first+7,240),'/ 240',flush=True)
record={'revision':rev,'pptx_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':240,'images':240,'renderer':'LibreOffice then Poppler 96 dpi','scope':'Actual assembled PPTX rendered, not concatenated prior PDFs; visual comparison recorded separately.'}
(r/'render-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),'utf-8',newline='\n')
