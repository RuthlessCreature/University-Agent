"""Check the exported OOXML, not just the builder's in-memory projections."""
from pathlib import Path
from xml.etree import ElementTree as E
import csv, hashlib, json, re, zipfile

R=Path(__file__).resolve().parent
B=R/'writing-packet'
W=B/'word-r1'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
manifest=json.loads((W/'export-manifest.json').read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert manifest['source_hash_method']=='SHA256 of UTF-8 text with LF newlines; independent of checkout CRLF conversion'
for name,h in manifest['sources'].items():assert hashlib.sha256((B/name).read_text('utf-8').encode('utf-8')).hexdigest()==h
for name,h in manifest['exports'].items():assert sha(W/name)==h
def paragraphs(name):
 with zipfile.ZipFile(W/name) as z:
  x=E.fromstring(z.read('word/document.xml'))
  assert not x.findall('.//w:ins',ns) and not x.findall('.//w:del',ns), 'This export must not claim native tracked changes'
  return x.findall('.//w:body/w:p',ns)
def text(p):return ''.join(t.text or '' for t in p.findall('.//w:t',ns))
expected_new=[s.lstrip('#').strip() for s in (B/'manuscript-r1.md').read_text('utf-8').splitlines() if s.strip()]
expected_old=[s.lstrip('#').strip() for s in (B/'manuscript-r0.md').read_text('utf-8').splitlines() if s.strip()]
clean=[text(p) for p in paragraphs('修订稿_清稿.docx')][2:]
assert clean==expected_new
accepted=[];rejected=[];deleted=inserted=0
for p in paragraphs('修订稿_改动标记.docx')[2:]:
 a=[];b=[]
 for run in p.findall('w:r',ns):
  t=text(run);strike=run.find('w:rPr/w:strike',ns);under=run.find('w:rPr/w:u',ns);color=run.find('w:rPr/w:color',ns)
  if strike is not None:
   assert color is not None and color.get('{'+ns['w']+'}val')=='963F3C'
   b.append(t);deleted+=1
  elif under is not None:
   assert color is not None and color.get('{'+ns['w']+'}val')=='246A52'
   a.append(t);inserted+=1
  else:a.append(t);b.append(t)
 if ''.join(a):accepted.append(''.join(a))
 if ''.join(b):rejected.append(''.join(b))
assert accepted==expected_new and rejected==expected_old
reply='\n'.join(text(p) for p in paragraphs('逐条审稿回复.docx'))
matrix=list(csv.DictReader((B/'response-matrix.csv').open(encoding='utf-8-sig')))
for q in matrix:
 assert q['comment'] in reply and q['response'] in reply and q['status'] in reply
 for anchor in re.findall(r'\[[A-Z][0-9]+\]',q['anchor']):assert anchor in reply and any(anchor in s for s in clean)
assert '新增研究未完成' in reply and '未新增独立样本' in reply
out={'docx_files':3,'actual_clean_text_equals_markdown':True,'actual_marked_accept_projection_equals_r1':True,'actual_marked_reject_projection_equals_r0':True,'marked_deleted_runs':deleted,'marked_inserted_runs':inserted,'review_ids':[q['id'] for q in matrix],'uncompleted_research_explicit':True,'native_track_changes':False,'scope':'Actual DOCX text, run formatting, source hashes and reply anchors; no scientific acceptance or journal submission.'}
(W/'checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
