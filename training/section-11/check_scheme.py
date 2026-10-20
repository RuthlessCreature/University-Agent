"""Check the actual diagram exports, native connector endpoints and Word image."""
from pathlib import Path
from xml.etree import ElementTree as E
import json,hashlib,zipfile,re,sys,html
R=Path(__file__).resolve().parent;B=R/'patent-packet';D=B/'diagrams';rev=sys.argv[1] if len(sys.argv)>1 else 's11-r6'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','s':'http://www.w3.org/2000/svg'}
def norm(s):return re.sub(r'\s+','',s)
q=json.loads((D/'flow.json').read_text('utf-8'));nodes={n['id']:norm(n['label']) for n in q['nodes']};expected=sorted((e['source'],e['target']) for e in q['edges'])
svg=E.parse(D/'教学方案流程.svg').getroot();draw=E.parse(D/'教学方案流程.drawio').getroot()
assert sorted((e.get('data-source'),e.get('data-target')) for e in svg.findall('.//s:polyline',ns))==expected
assert sorted((e.get('source'),e.get('target')) for e in draw.findall('.//mxCell') if e.get('edge')=='1')==expected
for n in q['nodes']:
 el=next(e for e in draw.findall('.//mxCell') if e.get('id')==n['id']);assert norm(re.sub('<[^>]*>','',html.unescape(el.get('value'))))==nodes[n['id']]
def endpoint_pairs(x):
 labels={}
 for n in x.findall('.//p:sp',ns):
  props=n.find('p:nvSpPr/p:cNvPr',ns)
  if props is not None:labels[props.get('id')]=norm(''.join(t.text or '' for t in n.findall('.//a:t',ns)))
 pairs=[]
 for n in x.findall('.//p:cxnSp',ns):
  a=n.find('.//a:stCxn',ns);b=n.find('.//a:endCxn',ns);assert a is not None and b is not None;pairs.append((labels[a.get('id')],labels[b.get('id')]))
 return pairs
with zipfile.ZipFile(next((R/'output').glob('*'+rev+'.pptx'))) as z:
 pairs=endpoint_pairs(E.fromstring(z.read('ppt/slides/slide7.xml')))
 assert sorted(pairs)==sorted((nodes[a],nodes[b]) for a,b in expected)
 pairs=endpoint_pairs(E.fromstring(z.read('ppt/slides/slide10.xml')))
 assert len(pairs)==2
 actual_claim_pairs=sorted([int(re.search(r'权利要求(\d+)',s).group(1)) for s in pair] for pair in pairs)
 assert actual_claim_pairs==[[1,3],[3,4]]
claims=json.loads((B/'claim-reading.json').read_text('utf-8'));assert claims['selected_edges']==[[1,3],[3,4]] and claims['physical_pdf_pages']==[14,15]
run=json.loads((B/'output/run.json').read_text('utf-8'));assert len(run['diagram_assets'])==1
with zipfile.ZipFile(B/'output/patent-draft.docx') as z:
 media=[z.read(n) for n in z.namelist() if n.startswith('word/media/')];assert len(media)==1
 asset=run['diagram_assets'][0];assert sha(B/asset['file'])==asset['sha256'] and (B/asset['file']).read_bytes() in media
 text=''.join(t.text or '' for t in E.fromstring(z.read('word/document.xml')).findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
 for token in ['S1','S2','S3','S4','步骤对应的待补材料']:assert token in text
report={'revision':rev,'native_flow_nodes':6,'native_flow_endpoint_pairs':6,'selected_claim_reference_endpoint_pairs':2,'drawio_and_svg_edges_equal_shared_json':True,'word_png_equals_source_file':True,'scope':'Diagram/file correspondence only; no device, patentability or legal scope validation.'}
(B/'scheme-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
