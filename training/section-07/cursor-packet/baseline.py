"""同一CSV的描述统计；只用Python标准库，不作因果或显著性判断。"""
from pathlib import Path
import csv,json,hashlib,statistics,datetime,sys,platform
R=Path(__file__).resolve().parent
source=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else R/'penguins.csv'
out=R/'baseline-output';out.mkdir(exist_ok=True)
raw=list(csv.DictReader(source.open(encoding='utf-8')))
assert len(raw)==344,'本例应使用配套344条公开记录'
selected=[(i+2,q) for i,q in enumerate(raw) if q['species']=='Adelie' and q['sex'] in ['female','male'] and q['flipper_length_mm'] not in ['','NA']]
groups=[]
for code,sex in enumerate(['female','male']):
 values=[float(q['flipper_length_mm']) for _,q in selected if q['sex']==sex]
 groups.append(dict(sex_code=code,n=len(values),mean_mm=statistics.mean(values),sd_mm=statistics.stdev(values)))
assert len(selected)==146 and [q['n'] for q in groups]==[73,73]
comparison=[{'female_n':groups[0]['n'],'male_n':groups[1]['n'],'female_mean_mm':groups[0]['mean_mm'],'male_mean_mm':groups[1]['mean_mm'],'male_minus_female_mm':groups[1]['mean_mm']-groups[0]['mean_mm']}]
for name,rows in [('summary',groups),('comparison',comparison),('included_rows',[{'csv_line':i,'sex_code':0 if q['sex']=='female' else 1,'flipper_mm':float(q['flipper_length_mm'])} for i,q in selected])]:
 with (out/(name+'.csv')).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runtime':platform.python_version(),'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'actual_execution':True,'source_rows':len(raw),'analysis_rows':len(selected),'group_code':{'0':'female','1':'male'},'groups':groups,'comparison':comparison[0],'standard_deviation':'sample, denominator n-1','scope':'公开数据二次描述统计；未证明观测独立、抽样代表性或因果关系。'}
(out/'run.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
print(json.dumps({'actual_execution':True,'analysis_rows':len(selected),'groups':groups,'male_minus_female_mm':comparison[0]['male_minus_female_mm']},ensure_ascii=False))
