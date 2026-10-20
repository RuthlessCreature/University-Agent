from pathlib import Path
import urllib.request,re,json,hashlib,concurrent.futures
R=Path(__file__).resolve().parent;A=R/'assets';A.mkdir(parents=True,exist_ok=True)
sources=[('nsfc-2026-application-rules.pdf','https://www.nsfc.gov.cn/u/cms/www/202601/190844586k0w.pdf'),('nsfc-structure.html','https://www.nsfc.gov.cn/p1/3381/2821/99242.html'),('nsfc-faq.html','https://www.nsfc.gov.cn/p1/2961/2962/3642/sqs.html'),('asreview-2021.html','https://www.nature.com/articles/s42256-020-00287-7')]
def get(pair):
    name,url=pair
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    data=urllib.request.urlopen(req,timeout=60).read();(A/name).write_bytes(data)
    return {'file':'assets/'+name,'url':url,'retrieved':'2026-10-17','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:records=list(ex.map(get,sources))
html=(A/'asreview-2021.html').read_text('utf-8')
urls=re.findall(r'https://[^\s"<>]+',html)
figs=[u.replace('&amp;','&') for u in urls if '42256_2020_287_Fig1' in u]
assert figs,'Original published Figure 1 URL missing'
url=next((u for u in figs if '/full/' in u),figs[0])
records.append(get(('asreview-fig1.png',url)))
records[-1].update({'attribution':'van de Schoot et al. Nature Machine Intelligence 3, 125–133 (2021), Fig.1','doi':'10.1038/s42256-020-00287-7','license':'CC BY 4.0','transformation':'none; image kept in original proportions'})
(R/'sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(records,ensure_ascii=False,indent=2))
