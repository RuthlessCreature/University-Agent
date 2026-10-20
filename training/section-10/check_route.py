"""Check native PPT connector endpoints, editable graph files and embedded Word media."""
from pathlib import Path
from xml.etree import ElementTree as E
import hashlib,json,zipfile,re,html,sys
R=Path(__file__).resolve().parent
rev=sys.argv[1] if len(sys.argv)>1 else 's10-r4'
B=R/'grant-packet';D=B/'diagrams'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((D/'source-manifest.json').read_text('utf-8'))
for name,h in manifest['files'].items():assert sha(D/name)==h
route=json.loads((D/'route.json').read_text('utf-8'));assert sha(D/'protocol.json')==route['protocol_sha256']
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','s':'http://www.w3.org/2000/svg'}
def normalized(s):return re.sub(r'\s+','',s)
with zipfile.ZipFile(next((R/'output').glob('*'+rev+'.pptx'))) as z:
 x=E.fromstring(z.read('ppt/slides/slide13.xml'))
 shapes={}
 for n in x.findall('.//p:sp',ns):
  props=n.find('p:nvSpPr/p:cNvPr',ns)
  if props is not None:shapes[props.get('id')]=normalized(''.join(t.text or '' for t in n.findall('.//a:t',ns)))
 actual=[]
 for c in x.findall('.//p:cxnSp',ns):
  a=c.find('.//a:stCxn',ns);b=c.find('.//a:endCxn',ns)
  assert a is not None and b is not None
  actual.append((shapes[a.get('id')],shapes[b.get('id')]))
 nodes={n['id']:normalized(n['label']) for n in route['nodes']}
 expected=[(nodes[e['source']],nodes[e['target']]) for e in route['edges']]
 assert sorted(actual)==sorted(expected) and len(actual)==8
for name,stem in [('route.json','研究技术路线'),('decision.json','材料核对与返工')]:
 q=json.loads((D/name).read_text('utf-8'));pairs=sorted((e['source'],e['target']) for e in q['edges'])
 svg=E.parse(D/(stem+'.svg')).getroot()
 assert sorted((e.get('data-source'),e.get('data-target')) for e in svg.findall('.//s:polyline',ns))==pairs
 draw=E.parse(D/(stem+'.drawio')).getroot()
 assert sorted((e.get('source'),e.get('target')) for e in draw.findall('.//mxCell') if e.get('edge')=='1')==pairs
 for n in q['nodes']:
  element=next(e for e in draw.findall('.//mxCell') if e.get('id')==n['id'])
  assert normalized(re.sub('<[^>]*>','',html.unescape(element.get('value'))))==normalized(n['label'])
run=json.loads((B/'output/run.json').read_text('utf-8'));assert len(run['diagram_assets'])==2
with zipfile.ZipFile(B/'output/grant-draft.docx') as z:
 media=[z.read(n) for n in z.namelist() if n.startswith('word/media/')]
 assert len(media)==2
 for d in run['diagram_assets']:
  assert sha(B/d['file'])==d['sha256'] and (B/d['file']).read_bytes() in media
protocol=json.loads((D/'protocol.json').read_text('utf-8'))
assert protocol['primary_outcome']['time']=='一周后' and protocol['execution_status']=='未实施，未招募，未获批准'
report={'revision':rev,'native_route_nodes':8,'native_route_connector_endpoints':8,'matching_drawio_and_svg_edges':True,'word_embedded_png_files':2,'word_media_equals_source_files':True,'protocol_sha256_verified':True,'status':'教学拟议，未实施；无科学核验或正式申报判断'}
(B/'route-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
