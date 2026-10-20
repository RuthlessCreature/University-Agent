import pathlib,urllib.request,json,hashlib,csv,statistics,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCES=[
 ('nature-ai','https://www.nature.com/nature-portfolio/editorial-policies/ai','Nature Portfolio AI policy','Official policy; paraphrase only; last-update date not displayed'),
 ('agents','https://www.anthropic.com/engineering/building-effective-agents','Building effective agents','Official engineering article; paraphrase only'),
 ('mcp','https://modelcontextprotocol.io/docs/getting-started/intro','MCP introduction','Official documentation; paraphrase only'),
 ('skills','https://agentskills.io/what-are-skills','Agent Skills specification','Official specification'),
 ('penguins','https://allisonhorst.github.io/palmerpenguins/','palmerpenguins','Data CC0; Horst Hill Gorman 2020'),
 ('gorman','https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0090081','Gorman Williams Fraser 2014 PLOS ONE 9 e90081','CC BY; figures reproduced unchanged with attribution'),
 ('minimax','https://platform.minimax.io/docs/api-reference/text-openai-api','MiniMax OpenAI compatibility','Official API documentation; account access untested'),
 ('codex','https://developers.openai.com/codex/skills','Codex Skills','Official documentation; local CLI version 0.124.0'),
 ('scipy','https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html','Independent samples t test','Official statistical reference'),
 ('icmje','https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html','IMRAD manuscript preparation','Official recommendations'),
 ('orcid','https://info.orcid.org/what-is-orcid/','ORCID','Official documentation'),
 ('crossref','https://www.crossref.org/documentation/retrieve-metadata/rest-api/','Crossref REST API','Metadata verifies identity, not truth of claims')]
manifest=[]
for sid,url,title,license in SOURCES:
    row=dict(id=sid,url=url,title=title,usage=license,retrieved='2026-10-16',kind='public-real-source')
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 University Research Teaching'})
        with urllib.request.urlopen(req,timeout=25) as r:data=r.read()
        p=ROOT/'sources'/f'{sid}.html';p.write_bytes(data);row.update(local_path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(data).hexdigest(),download='ok')
    except Exception as e:row.update(download='failed',error=str(e))
    manifest.append(row)
for p in list((ROOT/'assets').glob('*'))+list((ROOT/'sources').glob('*.csv')):
    manifest.append(dict(id=('penguins-data' if p.suffix=='.csv' else p.stem),local_path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),kind='public-real-asset',usage='Gorman et al. 2014 CC BY, figures; palmerpenguins data CC0, CSV'))
(ROOT/'sources'/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf-8')
rows=list(csv.DictReader((ROOT/'sources'/'penguins.csv').open(encoding='utf-8')))
groups=collections.defaultdict(list)
for r in rows:
    if r['body_mass_g']!='NA': groups[r['species']].append(float(r['body_mass_g']))
stats={k:dict(n=len(v),mean=statistics.mean(v),sd=statistics.stdev(v),min=min(v),max=max(v)) for k,v in groups.items()}
(ROOT/'sources'/'penguins-statistics.json').write_text(json.dumps({'rows':len(rows),'missing_body_mass':sum(r['body_mass_g']=='NA' for r in rows),'groups':stats,'method':'all observed body_mass_g; descriptive statistics; no random sampling; no causal inference'},ensure_ascii=False,indent=2),'utf-8')
print(json.dumps(stats,ensure_ascii=False,indent=2))
