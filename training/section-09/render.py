from pathlib import Path
import subprocess,sys
from pdf2image import convert_from_path
root=Path(__file__).resolve().parent
rev=sys.argv[1] if len(sys.argv)>1 else 's9-r7'
src=root/'output'/f'高校科研AI课程_Section9_论文写作投稿与返修_{rev}.pptx'
out=root/'renders'/rev;out.mkdir(parents=True,exist_ok=True)
profile=(root/'.build'/('lo-'+rev)).resolve().as_uri()
r=subprocess.run(['C:/Program Files/LibreOffice/program/soffice.exe','-env:UserInstallation='+profile,'--headless','--convert-to','pdf','--outdir',str(out),str(src)],capture_output=True,text=True,timeout=180)
pdf=out/(src.stem+'.pdf');assert pdf.exists(),r.stdout+r.stderr
pages=convert_from_path(pdf,dpi=96,poppler_path='C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin')
assert len(pages)==22
for n,im in enumerate(pages,1):im.save(out/f'slide-{n:02d}.png')
print('Rendered actual final PPTX:',len(pages),'pages')
