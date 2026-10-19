"""Verify the teaching plan and drafted material without claiming outreach happened."""
from pathlib import Path
import csv,json,hashlib,statistics,math
P=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
plan=load(P/'plan.json');assets=load(P/'materials.json');facts=load(P/'facts.json')
assert all(sha(P/name)==digest for name,digest in plan['source_files'].items())
assert sha(P/'penguins.csv')==load(P/'data-source.json')['sha256']
rows=list(csv.DictReader((P/'penguins.csv').open(encoding='utf-8')));assert len(rows)==344
ad=[q for q in rows if q['species']=='Adelie'];assert len(ad)==152
clean=[q for q in ad if q['sex'] in ['female','male'] and q['flipper_length_mm'] not in ['','NA']];assert len(clean)==146
means={};edges=facts['histogram']['edges']
for sex in ['female','male']:
 values=[float(q['flipper_length_mm']) for q in clean if q['sex']==sex];assert len(values)==73
 means[sex]=statistics.mean(values);assert math.isclose(means[sex],facts[sex+'_mean_mm'],abs_tol=1e-10,rel_tol=0)
 counts=[sum(lo<=v<hi or (i==len(edges)-2 and v==hi) for v in values) for i,(lo,hi) in enumerate(zip(edges,edges[1:]))];assert counts==facts['histogram']['counts'][sex]
assert f"{means['male']-means['female']:.2f}"=='4.62'
items=plan['items'];assert len(items)==4 and [q['id'] for q in items]==['R1','R2','R3','R4']
for q in items:
 assert sha(P/q['draft_file'])==q['draft_sha256'] and q['state']=='draft_not_published' and not q['published'] and not q['actual_feedback_received']
 body=(P/q['draft_file']).read_text('utf-8');assert len(body)>200 and all(t in body for t in ['146','73','4.62','教学','尚未发布'])
 assert set(q['source_ids'])=={'A01','A02'}
assert all(plan['metrics'][k] is None for k in ['visits','downloads','citations','adoptions'])
assert plan['actual_feedback_records']==[] and not plan['platform_account_accessed'] and not plan['outreach_publication_performed']
with (P/'传播安排.csv').open(encoding='utf-8-sig',newline='') as f:csv_rows=list(csv.DictReader(f))
assert len(csv_rows)==4 and all(all(row[k]==q[k] for k in row) for row,q in zip(csv_rows,items))
assert len(assets)==3 and assets[2]['id']=='H01' and assets[2]['local_file'] is None
for q in assets[:2]:assert sha(P/q['local_file'])==q['sha256']
report={'draft_files_verified':4,'plan_rows':4,'relative_phases':[q['relative_phase'] for q in items],'public_source_rows':344,'analysis_rows':146,'records_per_group':73,'CSV_means_difference_and_histograms_independently_checked':True,'draft_hashes_verified':4,'source_snapshot_hashes_verified':2,'actual_outreach_posts':0,'platform_account_accessed':False,'actual_feedback_records':0,'metrics_measured':False,'scope':'Numerical consistency, exact draft/source files, editable plan, material classification and unpublished outreach status. Does not establish author approval, permission for every use, communication effectiveness or scientific validity.'}
(P/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
