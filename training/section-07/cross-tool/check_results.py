from pathlib import Path
import csv,json,math,hashlib
R=Path(__file__).resolve().parent
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def load(p):return json.loads(p.read_text('utf-8-sig'))
hash_input=hashlib.sha256((R/'penguins.csv').read_bytes()).hexdigest()
assert hash_input==load(R.parent/'analysis-packet/source.json')['sha256']
actual=load(R.parent/'results.json')
for lang in ['python','r']:
 out=R/(lang+'-output');record=load(out/'run.json');assert record['actual_execution'] and record['input_sha256']==hash_input
 for entry in record.get('files',[]):
  assert hashlib.sha256((out/entry['name']).read_bytes()).hexdigest()==entry['sha256']
 extension='py' if lang=='python' else 'R';assert record['script_sha256']==hashlib.sha256((R/('analysis.'+extension)).read_bytes()).hexdigest()
 summary=read(out/'summary.csv');assert len(summary)==2
 for i,sex in enumerate(['female','male']):
  row=summary[i];assert int(row['sex_code'])==i and int(row['n'])==actual[sex]['n']==73
  for key,ref in [('mean_mm','mean'),('sd_mm','sd')]:assert math.isclose(float(row[key]),actual[sex][ref],abs_tol=1e-9,rel_tol=0)
 comp=read(out/'comparison.csv');assert len(comp)==1;assert math.isclose(float(comp[0]['male_minus_female_mm']),actual['mean_difference_mm'],abs_tol=1e-9,rel_tol=0)
 rows=read(out/'included_rows.csv');assert len(rows)==146
 if lang=='python':reference=rows
 else:
  assert [int(q['csv_line']) for q in rows]==[int(q['csv_line']) for q in reference]
  assert [int(q['sex_code']) for q in rows]==[int(q['sex_code']) for q in reference]
  assert [float(q['flipper_mm']) for q in rows]==[float(q['flipper_mm']) for q in reference]
assert not list(R.glob('spss-*.csv')),'Do not create apparent SPSS output without an SPSS run'
report={'input_sha256':hash_input,'python_actual_execution':True,'R_actual_execution':True,'R_engine':'WebR 0.6.0 local Node.js / R 4.6.0','R_desktop_application_tested':False,'SPSS_actual_execution':False,'SPSS_status':'Source supplied only; no executable found in PATH or Program Files scan; IBM full documentation requests returned 403, indexed official syntax reviewed.','matched_included_row_ids':146,'matched_groups':2,'comparison_direction':'male minus female','sample_sd_denominator':'n-1','absolute_tolerance':1e-9,'actual_python_and_R_agree':True,'scope':'Descriptive numerical agreement only. Does not validate data independence, scientific interpretation, IBM SPSS syntax execution or all program failures.'}
(R/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
