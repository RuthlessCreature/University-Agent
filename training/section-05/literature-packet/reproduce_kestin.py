"""Reproduce reported descriptive statistics from the authors' public Stata file.

No model call. Raw student-level public data stays in the ignored source cache.
The file hash is pinned after inspecting the authors' original repository.
"""
from pathlib import Path
import csv,hashlib,json,subprocess
import pandas as pd

R=Path(__file__).resolve().parent
C=R.parent/'.reference-cache'
URL='https://raw.githubusercontent.com/HarvardAItutor/Study-Data-v4/main/Harvard_AI_Tutor_Study_Data.dta'
EXPECTED_SHA256='362b26d84d01024e3c77e172d929e2bf8cbb3c7b09a9acd64757b9c0c1bd117e'
SOURCE_BLOB='2ad104a44b64acd98f4951ab92955ba85d2400cf'
C.mkdir(exist_ok=True)
p=C/'Harvard_AI_Tutor_Study_Data.dta'
if not p.exists():
    subprocess.run(['curl.exe','-L','--fail','--max-time','30',URL,'-o',str(p)],check=True,capture_output=True)
sha=hashlib.sha256(p.read_bytes()).hexdigest()
assert sha==EXPECTED_SHA256,'Author data changed; review the source before updating the pin.'
raw=p.read_bytes()
assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==SOURCE_BLOB
df=pd.read_stata(p)
assert set(df['lect_AI'].dropna().unique())=={0.0,1.0}
assert not df[['rid','lect_AI','post_score','pre_score']].isna().any().any()
assert not df.duplicated(['rid','lect_AI']).any()
groups=[]
for code,label in [(0,'课堂主动学习'),(1,'定制AI辅导')]:
    part=df.loc[df['lect_AI']==code]
    groups.append({'condition_code':code,'condition':label,'record_count':len(part),
                   'unique_student_ids':int(part['rid'].nunique()),
                   'post_score_median':float(part['post_score'].median()),
                   'post_score_mean':float(part['post_score'].mean()),
                   'post_score_min_observed':float(part['post_score'].min()),
                   'post_score_max_observed':float(part['post_score'].max())})
assert [v['record_count'] for v in groups]==[174,142]
assert [v['post_score_median'] for v in groups]==[3.5,4.5]
assert df['rid'].nunique()==194 and len(df)==316
assert df['pre_score'].median()==2.75
counts=df.groupby('rid').size().value_counts().to_dict()
assert counts=={2:122,1:72}
out={'source_url':URL,'source_repository':'https://github.com/HarvardAItutor/Study-Data-v4',
     'source_blob_sha1':SOURCE_BLOB,'source_file_sha256':sha,
     'checked_date':'2026-10-19','doi':'10.1038/s41598-025-97652-6',
     'rows':316,'unique_student_ids':194,'students_with_two_records':122,
     'students_with_one_record':72,'combined_pre_score_median':2.75,
     'groups':groups,'chart_metric':'post_score median; original score units',
     'verification_scope':'本地Python读取作者公开dta，复算记录数、唯一编号数及描述统计；不代表重新实施实验或复现全部回归。',
     'unresolved':'正文资格段提到参与两种教学且完成全部测验；公开文件有72个编号仅一条记录。未取得逐步筛选日志，不推断缺行或排除原因。',
     'not_independent_participants':True,'raw_records_redistributed':False}
(R/'kestin-reproduction.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n','utf-8')
with (R/'kestin-summary.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(groups[0]));w.writeheader();w.writerows(groups)
print(json.dumps(out,ensure_ascii=False,indent=2))
