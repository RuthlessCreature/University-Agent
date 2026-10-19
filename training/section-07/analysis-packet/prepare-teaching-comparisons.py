"""Calculate two teaching comparisons without changing source or analysis data."""
from pathlib import Path
import csv,hashlib,json,statistics,platform
import numpy as np
R=Path(__file__).resolve().parent
raw=R/'penguins.csv';original_sha=hashlib.sha256(raw.read_bytes()).hexdigest()
with raw.open(encoding='utf-8',newline='') as f:allrows=list(csv.DictReader(f))
rows=[dict(v,source_csv_row=i+2) for i,v in enumerate(allrows)
      if v['species']=='Adelie' and v['sex'] in ['female','male'] and v['flipper_length_mm']!='NA']
q1,q3=np.quantile([float(v['flipper_length_mm']) for v in rows],[.25,.75],method='linear')
lower=float(q1-1.5*(q3-q1));upper=float(q3+1.5*(q3-q1))
flagged=[v for v in rows if not lower<=float(v['flipper_length_mm'])<=upper]
assert [v['source_csv_row'] for v in flagged]==[30,131]
flagged_ids={v['source_csv_row'] for v in flagged}
out=[]
for key,label,data in [('retain_all','保留全部完整记录',rows),('exclude_flagged_scenario','仅作比较：排除标记值',[v for v in rows if v['source_csv_row'] not in flagged_ids])]:
    female=[float(v['flipper_length_mm']) for v in data if v['sex']=='female']
    male=[float(v['flipper_length_mm']) for v in data if v['sex']=='male']
    out.append({'scenario':key,'label':label,'records':len(data),'female_n':len(female),
                'male_n':len(male),'female_mean_mm':statistics.mean(female),
                'male_mean_mm':statistics.mean(male),
                'male_minus_female_mm':statistics.mean(male)-statistics.mean(female)})
assert [v['records'] for v in out]==[146,144]
assert [(v['female_n'],v['male_n']) for v in out]==[(73,73),(72,72)]
with (R/'outlier-sensitivity.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
with (R/'normal-ci-simulation.csv').open(encoding='utf-8',newline='') as f:sim=list(csv.DictReader(f))
assert len(sim)==1000
covered=sum(float(v['lower'])<=100<=float(v['upper']) for v in sim)
assert covered==941
prefix=[dict(repetition=i+1,**v) for i,v in enumerate(sim[:20])]
assert [v['repetition'] for v in prefix if not float(v['lower'])<=100<=float(v['upper'])]==[18]
with (R/'normal-ci-first20.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(prefix[0]));w.writeheader();w.writerows(prefix)
files={name:hashlib.sha256((R/name).read_bytes()).hexdigest() for name in
       ['penguins.csv','normal-ci-simulation.csv','outlier-sensitivity.csv','normal-ci-first20.csv']}
report={'source_hashes':files,'python_version':platform.python_version(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'iqr_thresholds':{'q1':float(q1),'q3':float(q3),'lower':lower,'upper':upper},
        'flagged_records':[{'source_csv_row':v['source_csv_row'],'sex':v['sex'],'flipper_length_mm':float(v['flipper_length_mm'])} for v in flagged],
        'outlier_scenarios':out,'source_records_deleted':0,
        'ci_prefix_selection':'连续前20次；没有跳过或重新挑选模拟次数',
        'ci_prefix_records':prefix,'ci_all_repetitions':1000,'ci_covered':covered,
        'ci_not_covered':1000-covered,'ci_first20_miss_repetitions':[18],
        'scope':'实际读取公开CSV的描述敏感性比较，以及既有正态教学模拟的连续前20次；未查明异常原因，不批准删值，不构成稳健性或科研结论。'}
assert hashlib.sha256(raw.read_bytes()).hexdigest()==original_sha
(R/'teaching-comparisons.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
print(json.dumps({'flagged':report['flagged_records'],'scenarios':out,'ci_covered':covered,
                  'ci_first20_miss_repetitions':[18],'source_records_deleted':0},ensure_ascii=False,indent=2))
