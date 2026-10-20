"""Verify recorded artifacts only; this is not a teaching or Agent system acceptance test."""
from pathlib import Path
from xml.etree import ElementTree as ET
import hashlib,json,re,zipfile
root=Path(__file__).resolve().parents[2]
p=Path(__file__).with_name('section-progress.json');d=json.loads(p.read_text('utf-8'))
assert len(d['sections'])==15 and sum(s['page_budget'] for s in d['sections'])==240
count=0;pages=0
for s in d['sections']:
 if s['status']!='produced_for_review':continue
 f=root/s['pptx'];assert f.exists(),f
 assert hashlib.sha256(f.read_bytes()).hexdigest()==s['sha256'],f
 with zipfile.ZipFile(f) as z:
  slides=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
  assert len(slides)==s['page_budget'],f
 check=json.loads((root/s['checks']).read_text('utf-8'));assert check['revision']==s['revision']
 if 'pptx_sha256' in check:assert check['pptx_sha256']==s['sha256']
 count+=1;pages+=len(slides)
assert pages==d['produced_pages']
print(json.dumps({'recorded_sections_verified':count,'recorded_pages':pages,'remaining_sections':[s['id'] for s in d['sections'] if s['status']=='not_started'],'scope':d['scope']},ensure_ascii=False,indent=2))
