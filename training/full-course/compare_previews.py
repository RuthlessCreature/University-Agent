from pathlib import Path
import json,sys
from PIL import Image,ImageChops
import numpy as np
r=Path(__file__).resolve().parent;a=r.parents[1];rev=sys.argv[1] if len(sys.argv)>1 else 'course-r2'
assembly=json.loads((r/'assembly-manifest.json').read_text('utf-8'));rows=[]
for sec in assembly['source_sections']:
 source=a/sec['pptx'];folder=source.parent.parent/'renders'/sec['revision']
 for n in range(1,sec['pages']+1):
  global_page=sec['first_page']+n-1;old=folder/f'slide-{n:02d}.png';new=r/'renders'/rev/f'slide-{global_page:03d}.png'
  assert old.exists() and new.exists(),(old,new)
  with Image.open(old) as im:before=im.convert('RGB')
  with Image.open(new) as im:after=im.convert('RGB')
  if before.size!=after.size:raise AssertionError((old,before.size,after.size))
  diff=ImageChops.difference(before,after);bbox=diff.getbbox();fraction=float(np.count_nonzero(np.any(np.asarray(diff)!=0,axis=2))/(before.width*before.height)) if bbox else 0.0
  rows.append({'section':sec['section'],'section_page':n,'global_page':global_page,'identical_pixels':bbox is None,'changed_pixel_fraction':fraction,'changed_bbox':bbox,'source_preview':old.relative_to(a).as_posix(),'combined_preview':new.relative_to(a).as_posix()})
report={'revision':rev,'pages_compared':240,'identical_pixels':sum(x['identical_pixels'] for x in rows),'changed_pages':[x['global_page'] for x in rows if not x['identical_pixels']],'rows':rows,'scope':'Exact RGB pixel comparison of actual assembled PPTX rendering against section previews. Differences require visual review; unchanged content/relationships are checked separately.'}
(r/'preview-comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8',newline='\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['rows']},ensure_ascii=False))
