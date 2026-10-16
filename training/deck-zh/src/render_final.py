import pathlib,subprocess,sys,os
from pdf2image import convert_from_path
R=pathlib.Path(__file__).resolve().parents[1]
for name in sys.argv[1:]:
    inp=pathlib.Path(name).resolve();out=R/'renders'/('lo-sample' if 'Sample' in name else 'lo-full');out.mkdir(parents=True,exist_ok=True)
    profile=(R/'.build'/('lo-'+inp.stem)).resolve().as_uri()
    cmd=['C:/Program Files/LibreOffice/program/soffice.exe','-env:UserInstallation='+profile,'--headless','--convert-to','pdf','--outdir',str(out),str(inp)]
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=180);print(r.stdout,r.stderr)
    pdf=out/(inp.stem+'.pdf')
    if not pdf.exists():raise RuntimeError('LibreOffice conversion failed')
    pop=pathlib.Path('C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin')
    imgs=convert_from_path(str(pdf),dpi=96,poppler_path=str(pop))
    for i,img in enumerate(imgs,1):img.save(out/f'slide-{i:02d}.png')
    print('LibreOffice final file rendered',len(imgs),out)
