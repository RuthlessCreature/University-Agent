from pathlib import Path
import concurrent.futures, urllib.request, json, hashlib
from html.parser import HTMLParser
from pypdf import PdfReader

root = Path(__file__).resolve().parent / 'sources'
class TextParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]
    def handle_data(self, data):
        self.parts.append(data)
items = [('nature-ai','https://www.nature.com/nature-portfolio/editorial-policies/ai'),
         ('science-policy','https://www.science.org/content/page/science-journals-editorial-policies'),
         ('plos-policy','https://journals.plos.org/plosone/s/ethical-publishing-practice')]
def get(item):
    name, url = item
    try:
        data = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=25).read()
        parser = TextParser(); parser.feed(data.decode('utf-8',errors='replace'))
        text = ' '.join(parser.parts)
        (root / (name+'.txt')).write_text(text, encoding='utf-8')
        print(name, len(data), text.lower().find('artificial intelligence'))
        return {'id':name,'url':url,'bytes':len(data),'retrieved':'2026-10-17'}
    except Exception as exc:
        print(name, type(exc).__name__)
        return {'id':name,'url':url,'error':type(exc).__name__}
records = list(concurrent.futures.ThreadPoolExecutor(3).map(get,items))
pdf = root / 'citation-study.pdf'
reader = PdfReader(pdf)
text = '\n\n'.join(f'PDF PAGE {i+1}\n{page.extract_text()}' for i,page in enumerate(reader.pages))
(root / 'citation-study.txt').write_text(text, encoding='utf-8')
assert all(x in text for x in ['55%', '18%', '636', '222', '414'])
records.append({'id':'citation-study','url':'https://www.nature.com/articles/s41598-023-41032-5.pdf',
                'doi':'10.1038/s41598-023-41032-5','pages':len(reader.pages),
                'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
                'verified_location':'PDF第1页摘要、第4页表3与表4'})
(root / 'retrieval.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
