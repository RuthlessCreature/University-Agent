"""Verify assembled native parts against the exact current section decks."""
from pathlib import Path
import json,zipfile,hashlib,re,posixpath,xml.etree.ElementTree as E
from pypdf import PdfReader
r=Path(__file__).resolve().parent;a=r.parents[1]
def load(p):return json.loads(p.read_text('utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
m=load(r/'assembly-manifest.json');rev=m['revision'];p=r/'output'/f'高校科研AI培训课程_全课240页_{rev}.pptx';v=load(r/'validation.json');digest=sha(p.read_bytes())
assert v['finalSha256']==digest and v['packageIntegrity']['findingCount']==v['presentationLayout']['findingCount']==0
progress=load(a/'training/curriculum/section-progress.json');assert len(m['source_sections'])==len(progress['sections'])==15
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
source_zips={};source_native={'charts':0,'tables':0,'images':0,'connectors':0,'notes':0};actual={k:0 for k in source_native};modified=[]
with zipfile.ZipFile(p) as z:
 assert len(z.namelist())==len(set(z.namelist()))
 for src,current in zip(m['source_sections'],progress['sections']):
  assert (src['section'],src['revision'],src['sha256'])==(current['id'],current['revision'],current['sha256'])
  b=(a/src['pptx']).read_bytes();assert sha(b)==src['sha256'];source_zips[src['section']]=zipfile.ZipFile(a/src['pptx'])
  for n in range(1,src['pages']+1):
   old=source_zips[src['section']].read(f'ppt/slides/slide{n}.xml');new=z.read(f'ppt/slides/slide{src["first_page"]+n-1}.xml');assert old==new
   for target,blob in [(source_native,old),(actual,new)]:
    x=E.fromstring(blob);target['charts']+=len(x.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/chart}chart'));target['tables']+=len(x.findall('.//a:tbl',ns));target['images']+=len(x.findall('.//p:pic',ns));target['connectors']+=len(x.findall('.//p:cxnSp',ns))
   oldnotes=source_zips[src['section']].read(f'ppt/notesSlides/notesSlide{n}.xml');newnotes=z.read(f'ppt/notesSlides/notesSlide{src["first_page"]+n-1}.xml');assert oldnotes==newnotes;source_native['notes']+=1;actual['notes']+=1
 for part in m['preserved_parts']:
  b=z.read(part['part']);assert sha(b)==part['sha256']
  source=source_zips[part['section']].read(part['source_part']);assert sha(source)==part['source_sha256']
  if part['byte_preserved']:assert source==b
  else:modified.append((part['section'],part['source_part']))
 assert modified==[(0,'docProps/app.xml')]
 relationship_count=0
 for name in z.namelist():
  if not name.endswith('.rels'):continue
  owner='' if name=='_rels/.rels' else posixpath.join(posixpath.dirname(posixpath.dirname(name)),posixpath.basename(name)[:-5])
  for q in E.fromstring(z.read(name)):
   if q.attrib.get('TargetMode')=='External':continue
   t=q.attrib['Target'];target=t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(owner),t));assert target in z.namelist(),(name,target);relationship_count+=1
 pres=E.fromstring(z.read('ppt/presentation.xml'));ids=pres.findall('./p:sldIdLst/p:sldId',ns);assert len(ids)==240 and len(set(q.attrib['id'] for q in ids))==240
 assert source_native==actual and actual['notes']==240
 source_books=[sha(source_zips[s['section']].read(n)) for s in m['source_sections'] for n in source_zips[s['section']].namelist() if n.startswith('ppt/embeddings/') and n.endswith('.xlsx')]
 books=[sha(z.read(n)) for n in z.namelist() if n.startswith('ppt/embeddings/') and n.endswith('.xlsx')];assert sorted(source_books)==sorted(books)
 app=E.fromstring(z.read('docProps/s00-app.xml'));assert app.find('{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Slides').text=='240'
record=load(r/'render-record.json');assert record['pptx_sha256']==digest and record['pages']==240
pdf=r/'renders'/rev/(p.stem+'.pdf');assert sha(pdf.read_bytes())==record['pdf_sha256'] and len(PdfReader(pdf).pages)==240
assert len(list((pdf.parent).glob('slide-*.png')))==240
checks={'revision':rev,'pages':240,'source_sections':15,'slide_xml_byte_identical':240,'notes_xml_byte_identical':240,'native_objects':actual,'embedded_workbooks_byte_identical':len(books),'copied_parts_verified':len(m['preserved_parts']),'internal_relationships_resolve':relationship_count,'metadata_change_only':modified,'actual_pptx_pdf_pages':240,'preview_images':240,'pptx_sha256':digest,'scope':'Current source deck hashes, complete native slide/note/chart/media/workbook parts, relationship resolution and actual assembled rendering. Does not establish policy completeness, scientific approval, live model execution, timed rehearsal or user teaching acceptance.'}
(r/'checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),'utf-8',newline='\n');print(json.dumps(checks,ensure_ascii=False,indent=2))
