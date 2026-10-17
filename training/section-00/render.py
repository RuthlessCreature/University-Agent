from pathlib import Path
import subprocess, sys
from pdf2image import convert_from_path

root = Path(__file__).resolve().parent
revision = sys.argv[1] if len(sys.argv) > 1 else 's0-r3'
source = root / 'output' / f'高校科研AI课程_Section0_{revision}.pptx'
out = root / 'renders' / revision
out.mkdir(parents=True, exist_ok=True)
profile = (root / '.build' / ('lo-' + revision)).resolve().as_uri()
result = subprocess.run([
    'C:/Program Files/LibreOffice/program/soffice.exe',
    '-env:UserInstallation=' + profile, '--headless', '--convert-to', 'pdf',
    '--outdir', str(out), str(source)
], capture_output=True, text=True, timeout=180)
pdf = out / (source.stem + '.pdf')
assert pdf.exists(), result.stdout + result.stderr
pages = convert_from_path(str(pdf), dpi=96, poppler_path=
    'C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin')
assert len(pages) == 4, len(pages)
for number, page in enumerate(pages, 1):
    page.save(out / f'slide-{number:02d}.png')
print(f'Rendered {len(pages)} pages from final PPTX: {out}')
