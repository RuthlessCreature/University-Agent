"""Render a viewport of the original vector PDF; do not redraw its contents."""
from pathlib import Path
import subprocess, hashlib, json
r=Path(__file__).resolve().parent
pdf=r/'.reference-cache/EP4636367A1.pdf'
exe='C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe'
args=['-f','17','-l','17','-singlefile','-r','220','-x','340','-y','630','-W','1200','-H','1260','-png']
subprocess.run([exe,*args,str(pdf),str(r/'assets/EP4636367A1-fig2')],check=True)
asset=r/'assets/EP4636367A1-fig2.png'
record=dict(source_url='https://data.epo.org/publication-server/rest/v1.2/publication-dates/2025-10-22/patents/EP4636367NWA1/document.pdf',pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),physical_pdf_page=17,figure='FIG. 2',method='Original PDF viewport rasterization with Poppler; no content redrawn',pdftoppm_arguments=args,asset=asset.name,sha256=hashlib.sha256(asset.read_bytes()).hexdigest())
(r/'source-figure.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),'utf-8')
