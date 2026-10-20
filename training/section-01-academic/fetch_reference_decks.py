from pathlib import Path
import urllib.request, concurrent.futures, json, hashlib
from pypdf import PdfReader

root = Path(__file__).resolve().parent / '.reference-cache'
root.mkdir(exist_ok=True)
items = [
 ('gwu-foundations','https://docs.google.com/presentation/d/1H4KwDLIjdCLdsPkPWANsnr-qewui19Jal3vDk7v4nBE/export/pdf'),
 ('gwu-introduction','https://docs.google.com/presentation/d/1IO-K33HjwRKBFXELbMcIGp1PJ0nNP9uw5hv_7-Ciets/export/pdf'),
 ('gwu-context','https://docs.google.com/presentation/d/1lj8AXxc5Bv6VC6TzxZX3eD4kMETVTmR_pH7PZn5F-64/export/pdf'),
 ('ijs-introduction','https://ai4science.ijs.si/static/files/1-AIforScience-Introduction.pdf'),
 ('ijs-foundations','https://ai4science.ijs.si/static/files/4-FoundationModels.pdf'),
 ('tcu-foundations','https://docs.google.com/presentation/d/1VHYnxyJhzjihUTrfqhWpa3IbAmMI-mcjDiOTGleKN6I/export/pdf'),
 ('tcu-research','https://docs.google.com/presentation/d/1hwrgkDHtCiDkQMtZXgdbYtc0nf-ArHou4Pxg0frgMo8/export/pdf'),
 ('macerata-foundations','https://www.unimc.it/it/dottorato-di-ricerca/attivita-formative/attivita-didattiche-trasversali/basics-of-generative-ai-for-research-paolo-sernani.pdf'),
 ('ut-austin-foundations','https://docs.google.com/presentation/d/1ZFIxjgcFZGyEfaVOytSsiBPjOVl8RQjH/export/pdf'),
 ('galway-literacy','https://zenodo.org/records/17398118/files/AI%20Literacy%20for%20Researchers.pdf?download=1')
]
def fetch(item):
 name,url=item
 try:
  cached=root/(name+'.pdf')
  data=cached.read_bytes() if cached.exists() else urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=50).read()
  assert data.startswith(b'%PDF'), data[:40]
  dest=root/(name+'.pdf');dest.write_bytes(data)
  pdf=PdfReader(dest)
  text='\n\n'.join(f'PDF PAGE {i+1}\n{p.extract_text()}' for i,p in enumerate(pdf.pages))
  (root/(name+'.txt')).write_text(text,encoding='utf-8')
  print(name,len(pdf.pages),len(data),flush=True)
  return {'id':name,'url':url,'pages':len(pdf.pages),'sha256':hashlib.sha256(data).hexdigest()}
 except Exception as e:
  print(name,type(e).__name__,flush=True)
  return {'id':name,'url':url,'error':type(e).__name__}
result=list(concurrent.futures.ThreadPoolExecutor(4).map(fetch,items))
(root/'reference-downloads.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
