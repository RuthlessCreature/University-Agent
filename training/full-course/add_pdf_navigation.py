from pathlib import Path
import json,hashlib
from pypdf import PdfReader,PdfWriter
r=Path(__file__).resolve().parent;m=json.loads((r/'assembly-manifest.json').read_text('utf-8'));rev=m['revision'];stem=f'高校科研AI培训课程_全课240页_{rev}'
source=r/'renders'/rev/(stem+'.pdf');reader=PdfReader(source);writer=PdfWriter();writer.append_pages_from_reader(reader)
for s in m['source_sections']:writer.add_outline_item('Section '+str(s['section'])+'　'+s['title'],s['first_page']-1)
writer.add_metadata({'/Title':'高校科研AI培训课程 全课240页','/Subject':'15节中文课件合并核对版，含章节书签'})
target=r/'output'/(stem+'_含章节书签.pdf')
with target.open('wb') as f:writer.write(f)
result=PdfReader(target);assert len(result.pages)==240 and len(result.outline)==15
for a,b in zip(reader.pages,result.pages):assert a.get_contents().get_data()==b.get_contents().get_data()
record={'file':target.relative_to(r).as_posix(),'pages':240,'section_bookmarks':15,'page_content_streams_unchanged':240,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'scope':'Chapter navigation added to actual assembled-PPTX PDF; page content streams unchanged.'}
(r/'pdf-navigation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),'utf-8',newline='\n');print(json.dumps(record,ensure_ascii=False,indent=2))
