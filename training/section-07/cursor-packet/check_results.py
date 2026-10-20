"""Recalculate from public CSV and compare actual pre/post execution files."""
from pathlib import Path
import csv,hashlib,json,math,statistics
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text('utf-8'))
def csvrows(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
raw=csvrows(R/'penguins.csv');src=load(R/'source.json');e=load(R/'run-evidence.json')
assert sha(R/'penguins.csv')==src['input_sha256']==e['input_sha256']
assert len(raw)==344 and e['cursor_operated'] is False and e['cursor_model_called'] is False
selected=[(i+2,q) for i,q in enumerate(raw) if q['species']=='Adelie' and q['sex'] in ['female','male'] and q['flipper_length_mm'] not in ['','NA']]
assert len(selected)==146
expected=[]
for code,sex in enumerate(['female','male']):
    values=[float(q['flipper_length_mm']) for _,q in selected if q['sex']==sex]
    expected.append({'sex_code':code,'n':len(values),'mean_mm':statistics.mean(values),'sd_mm':statistics.stdev(values)})
assert [v['n'] for v in expected]==[73,73]
assert len(e['runs'])==2
for run,folder,script,key in zip(e['runs'],['baseline-output','modified-output'],['baseline.py','modified.py'],['male_minus_female_mm','female_minus_male_mm']):
    assert run['script']==script and run['exit_code']==0
    assert sha(R/script)==run['script_sha256']
    report=load(R/folder/'run.json')
    assert report['actual_execution'] is True
    assert report['input_sha256']==src['input_sha256'] and report['script_sha256']==sha(R/script)
    assert report['runtime']==e['python_version']
    assert report['source_rows']==344 and report['analysis_rows']==146
    included=csvrows(R/folder/'included_rows.csv')
    assert [(int(v['csv_line']),int(v['sex_code']),float(v['flipper_mm'])) for v in included]==[(i,0 if q['sex']=='female' else 1,float(q['flipper_length_mm'])) for i,q in selected]
    summary=csvrows(R/folder/'summary.csv')
    for got,want in zip(summary,expected):
        for k,v in want.items():assert math.isclose(float(got[k]),v,abs_tol=1e-10,rel_tol=0)
    c=csvrows(R/folder/'comparison.csv');assert len(c)==1 and key in c[0]
    want=expected[1]['mean_mm']-expected[0]['mean_mm']
    if key.startswith('female_'):want=-want
    assert math.isclose(float(c[0][key]),want,abs_tol=1e-10,rel_tol=0)
    assert math.isclose(report['comparison'][key],want,abs_tol=1e-10,rel_tol=0)
for name in ['included_rows.csv','summary.csv']:
    assert (R/'baseline-output'/name).read_bytes()==(R/'modified-output'/name).read_bytes()
b=load(R/'baseline-output/run.json')['comparison']['male_minus_female_mm']
m=load(R/'modified-output/run.json')['comparison']['female_minus_male_mm']
assert b>0 and m<0 and math.isclose(b,-m,abs_tol=1e-10,rel_tol=0)
report={'actual_local_python_runs':2,'cursor_operated':False,'cursor_model_calls':0,
        'source_records':344,'analysis_records':146,'per_group_n':[73,73],
        'included_rows_identical':True,'group_statistics_identical':True,
        'baseline_male_minus_female_mm':b,'modified_female_minus_male_mm':m,
        'independently_recomputed_from_csv':True,'input_and_script_hashes_verified':True,
        'scope':'Two local Python scripts, source-row inclusion and descriptive values; not Cursor execution, scientific acceptance or model evaluation.'}
(R/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
