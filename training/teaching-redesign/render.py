from pathlib import Path
import subprocess,sys,json
from pdf2image import convert_from_path
R=Path(__file__).resolve().parent
revision=sys.argv[1] if len(sys.argv)>1 else 'r1'
src=R/'output'/f'高校科研教学样课_研究设计_{revision}.pptx'
out=R/'renders'/revision;out.mkdir(parents=True,exist_ok=True)
profile=(R/'.build'/('lo-'+revision)).resolve().as_uri()
cmd=['C:/Program Files/LibreOffice/program/soffice.exe','-env:UserInstallation='+profile,'--headless','--convert-to','pdf','--outdir',str(out),str(src)]
result=subprocess.run(cmd,capture_output=True,text=True,timeout=180)
pdf=out/(src.stem+'.pdf');assert pdf.exists(),result.stdout+result.stderr
pages=convert_from_path(str(pdf),dpi=96,poppler_path='C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin')
assert len(pages)==12
for i,im in enumerate(pages,1):im.save(out/f'slide-{i:02d}.png')
html='<!doctype html><meta charset="utf-8"><title>高校科研教学样课</title><style>body{margin:32px;background:#eee;font:18px system-ui}article{max-width:1440px;margin:32px auto}img{width:100%}p{line-height:1.8}</style>'
for s in json.loads((R/'lesson.json').read_text('utf-8')):html+=f'<article><h2>{s["number"]:02d} {s["title"]}</h2><img src="slide-{s["number"]:02d}.png"><p>{s["notes"]}</p></article>'
(out/'index.html').write_text(html,encoding='utf-8')
print('Rendered 12 final PPTX pages:',out)
