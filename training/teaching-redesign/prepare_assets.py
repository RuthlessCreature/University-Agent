from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parent;A=R/'assets'
im=convert_from_path(str(A/'nsfc-2026-application-rules.pdf'),dpi=280,first_page=14,last_page=14,poppler_path='C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin')[0]
sx,sy=im.width/1064,im.height/1467
box=tuple(round(v*(sx if i%2==0 else sy)) for i,v in enumerate((137,543,932,695)))
im.crop(box).save(A/'nsfc-ai-paragraph.png')
original=Image.open(A/'asreview-fig1.png');original.crop((0,630,1033,1340)).save(A/'asreview-cycle.png')
items=[{'file':'nsfc-ai-paragraph.png','parent':'nsfc-2026-application-rules.pdf','pdf_page_index':13,'printed_page':16,'render_dpi':280,'crop_pixels':box,'change':'paragraph crop only, no text added or redrawn'}, {'file':'asreview-cycle.png','parent':'asreview-fig1.png','crop_pixels':[0,630,1033,1340],'change':'active-learning-cycle crop only, no labels changed; disclosed on slide'}]
for x in items:x['sha256']=hashlib.sha256((A/x['file']).read_bytes()).hexdigest()
(R/'asset-transformations.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared two disclosed source excerpts')
