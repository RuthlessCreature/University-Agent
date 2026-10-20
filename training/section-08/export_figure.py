from pathlib import Path
import sys,subprocess
from pypdf import PdfReader,PdfWriter
from pypdf.generic import RectangleObject
from pdf2image import convert_from_path
r=Path(__file__).resolve().parent;rev=sys.argv[1] if len(sys.argv)>1 else 's8-r2';src=next((r/'renders'/rev).glob('*.pdf'));reader=PdfReader(src);page=reader.pages[5]
# Crop the actual rendered native chart page, keeping axis labels, caption and source.
page.cropbox=RectangleObject([45,0,1155,442.5]);page.mediabox=RectangleObject([45,0,1155,442.5]);writer=PdfWriter();writer.add_page(page);pdf=r/'figure-packet/Adelie喙长与鳍长.pdf'
with pdf.open('wb') as f:writer.write(f)
pop='C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin';convert_from_path(pdf,dpi=144,poppler_path=pop)[0].save(r/'figure-packet/Adelie喙长与鳍长.png');subprocess.run(['C:/Program Files/LibreOffice/program/soffice.exe','-env:UserInstallation='+(r/'.build/lo-svg').resolve().as_uri(),'--headless','--convert-to','svg:draw_svg_Export','--outdir',str(r/'figure-packet'),str(pdf)],check=True,capture_output=True,timeout=120)
assert (r/'figure-packet/Adelie喙长与鳍长.svg').exists()
print('Standalone chart PDF/PNG/SVG exported from actual native-chart rendering')
