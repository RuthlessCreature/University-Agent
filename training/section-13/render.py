from pathlib import Path
import subprocess,sys
from pdf2image import convert_from_path
r=Path(__file__).resolve().parent;rev=sys.argv[1] if len(sys.argv)>1 else 's13-r6'
src=r/'output'/f'高校科研AI课程_Section13_科研汇报与成果传播_{rev}.pptx';out=r/'renders'/rev;out.mkdir(parents=True,exist_ok=True)
profile=(r/'.build'/('lo-'+rev)).resolve().as_uri()
q=subprocess.run(['C:/Program Files/LibreOffice/program/soffice.exe','-env:UserInstallation='+profile,'--headless','--convert-to','pdf','--outdir',str(out),str(src)],capture_output=True,text=True,timeout=180)
pdf=out/(src.stem+'.pdf');assert pdf.exists(),q.stdout+q.stderr
pages=convert_from_path(pdf,dpi=96,poppler_path='C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin');assert len(pages)==10
for n,im in enumerate(pages,1):im.save(out/f'slide-{n:02d}.png')
print('Rendered actual final PPTX:',len(pages),'pages')
