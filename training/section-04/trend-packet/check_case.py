"""Offline consistency of selected records, date semantics and original figure."""
from pathlib import Path
import csv,datetime,hashlib,json
from PIL import Image
R=Path(__file__).resolve().parent
case=json.loads((R/'case.json').read_text('utf-8'));records=json.loads((R/'records.json').read_text('utf-8'))
assert [v['id'] for v in records]==case['included_record_ids']
assert len(records)==3 and len({v['work_id'] for v in records})==3
start=datetime.date.fromisoformat(case['window_start']);end=datetime.date.fromisoformat(case['window_end'])
assert start==datetime.date(2024,1,1) and end==datetime.date(2025,12,31)
for r in records:
    assert start<=datetime.date.fromisoformat(r['public_date'])<=end
    assert all(r[k] for k in ['date_kind','source_location','contribution','limit','url','identifier'])
pat=next(v for v in records if v['id']=='patent')
assert pat['earlier_provisional_date']=='2023-02-14'
assert pat['application_date']=='2024-02-14' and pat['public_date']=='2024-08-15'
assert pat['application_date']!=pat['public_date']
pre=next(v for v in records if v['id']=='preprint')
assert pre['public_date']=='2024-05-23' and pre['related_published_doi']=='10.1145/3657604.3664694'
j=next(v for v in records if v['id']=='journal')
assert j['public_date']=='2025-06-25' and j['issue_date']=='2025-07-01'
with (R/'材料比较.csv').open(encoding='utf-8-sig',newline='') as f:
    table=list(csv.DictReader(f))
assert len(table)==3
for row,rec in zip(table,records):
    assert row['public_date']==rec['public_date'] and row['identifier']==rec['identifier']
asset=case['asset'];raw=(R/asset['file']).read_bytes()
assert hashlib.sha256(raw).hexdigest()==asset['sha256']
with Image.open(R/asset['file']) as im:assert im.size==(3970,1570)
assert case['quantitative_field_trend_estimated'] is False
assert case['model_search_pipeline_executed'] is False
report={'selected_records':3,'material_categories':3,'public_event_window':[str(start),str(end)],
        'patent_application_and_publication_separated':True,'preprint_published_version_link_retained':True,
        'journal_online_and_issue_dates_separated':True,'figure_source_sha256':asset['sha256'],
        'quantitative_field_trend_estimated':False,'model_search_pipeline_executed':False,
        'scope':'所选材料登记、日期语义、CSV对应和原图哈希；不验证领域覆盖、科研结论、专利法律状态或创新性。'}
(R/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
