"""Check draft files against actual CSV and the cited abstract requirements.
Scope is selected formatting and numerical consistency, not journal acceptance.
"""
from pathlib import Path
import csv,json,re,hashlib,statistics,difflib
P=Path(__file__).resolve().parent;R=P.parent
def load(p):return json.loads(p.read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
case=load(P/'case.json');a=load(R/'figure-data.json')
assert sha(P/'before-A1.txt')==case['before_sha256']
assert sha(P/'abstract-en.txt')==case['draft_sha256']
source=(R/'writing-packet/manuscript-r1.md').read_text('utf-8')
before=source.split('## 摘要 [A1]\n',1)[1].split('\n## 引言',1)[0].strip()
assert before==(P/'before-A1.txt').read_text('utf-8').strip()
en=(P/'abstract-en.txt').read_text('utf-8');zh=(P/'abstract-zh.txt').read_text('utf-8').strip()
assert zh==case['slide_abstract_zh'] and (P/'prompt.txt').read_text('utf-8').strip()==case['prompt']
tokens=re.findall(r"\d[\d,]*(?:\.\d+)?|[A-Za-z]+(?:[-'][A-Za-z]+)*",en)
assert 0<len(tokens)<=300
assert not re.search(r'https?://|doi:|\[\d+\]|\([A-Z][A-Za-z]+.*?\d{4}\)',en)
assert not re.search(r'\b(?:SD|SE|CI|AI)\b',en)
raw=R/'writing-packet/penguins.csv';assert sha(raw)==a['raw_sha256']
rows=list(csv.DictReader(raw.open(encoding='utf-8')));assert len(rows)==344
ad=[q for q in rows if q['species']=='Adelie'];assert len(ad)==152
included=[q for q in ad if q['sex'] in ['female','male'] and q['flipper_length_mm'] not in ['NA','']];assert len(included)==146
means={}
for sex in ['female','male']:
 values=[float(q['flipper_length_mm']) for q in included if q['sex']==sex];assert len(values)==73
 means[sex]=statistics.mean(values);assert f'{means[sex]:.2f}' in en and f'{means[sex]:.2f}' in zh
assert f"{means['male']-means['female']:.2f}" in en
for value in ['152','146','73','10,000','2.68','6.58']:assert value in en
for q in a['bootstrap']['percentile_95']:assert f'{q:.2f}' in en and f'{q:.2f}' in zh
assert a['bootstrap']['replicates']==10000
assert 'independent records' in en and 'remain unresolved' in en and 'teaching example' in en
expected=''.join(difflib.unified_diff((before+'\n').splitlines(True),en.splitlines(True),fromfile='before-A1.txt',tofile='abstract-en.txt'))
assert (P/'language-revision.diff').read_text('utf-8')==expected
assert case['external_journal_submission'] is False and case['external_model_service_run_claimed'] is False
library=load(P/'journal-prompt-library.json');assert len(library['entries'])==2
assert {q['journal'] for q in library['entries']}=={'PLOS One','Scientific Reports'}
for q in library['entries']:
 assert len(tokens)<=q['adopted_word_ceiling'] and len(q['prompt'])>150
 assert q['draft_file']=='abstract-en.txt' and q['url'].startswith('https://')
assert len([line for line in en.splitlines() if line.strip()])==1 and not re.search(r'^#+|\bFigure\s+\d',en,re.M)
report={'english_word_count':len(tokens),'word_count_method':"Regex: number incl. comma/decimal, or English word incl. internal hyphen/apostrophe; journal counter may differ",'english_word_limit':300,'source_abstract_matches_A1':True,'numerical_comparison_to_public_CSV':True,'source_sha256':sha(raw),'draft_sha256':sha(P/'abstract-en.txt'),'citations_detected_by_pattern_scan':False,'common_abbreviations_detected_by_pattern_scan':False,'actual_text_revision_diff_verified':True,'journal_submission':False,'scope':'Selected abstract formatting, source identity and numerical consistency. Sentence meaning and expression manually reviewed; no journal acceptance, research novelty, independence or full manuscript compliance claim.'}
report['source_based_prompt_templates']=2
report['checked_ceilings']={q['journal']:q['adopted_word_ceiling'] for q in library['entries']}
report['single_paragraph_without_subheadings']=True
(P/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
