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
capture=json.loads((R/'google-scholar-capture.json').read_text('utf-8'))
scholar=json.loads((R/'google-scholar-records.json').read_text('utf-8'))
state=(R/'google-scholar-actual-state.txt').read_text('utf-8')
assert len(scholar)==10
assert [v['result_position'] for v in scholar]==list(range(1,11))
assert [v['cited_by_count'] for v in scholar]==[204,65,47,31,17,32,17,17,16,12]
assert [v['result_position'] for v in scholar if v['primary_checked']]==[1,2,4]
for v in scholar:
    assert v['title'] in state and v['result_url'].removeprefix('https://') in state
    assert v['citation_source']=='Google Scholar' and v['captured_date']=='2026-10-19'
for name,sha in capture['files'].items():
    assert hashlib.sha256((R/name).read_bytes()).hexdigest()==sha
assert capture['years']==[2024,2025]
assert capture['bulk_export_performed'] is False and capture['full_systematic_review'] is False
with (R/'GoogleScholar前10条.csv').open(encoding='utf-8-sig',newline='') as f:
    exported=list(csv.DictReader(f))
assert len(exported)==10
for row,rec in zip(exported,scholar):
    assert row['title']==rec['title'] and int(row['cited_by_count'])==rec['cited_by_count']
checks=json.loads((R/'原文回查.json').read_text('utf-8'))
assert [v['result_position'] for v in checks]==[1,2,4]
with Image.open(R/'google-scholar-actual.png') as im:assert im.size==(737,874)
report={'google_scholar_actual_result_rows':10,'primary_reading_positions':[1,2,4],
        'scholar_snapshot_hashes_verified':True,'scholar_csv_matches_snapshot_records':True,
        'bulk_export_performed':False,'full_systematic_review':False,
        'selected_records':3,'material_categories':3,'public_event_window':[str(start),str(end)],
        'patent_application_and_publication_separated':True,'preprint_published_version_link_retained':True,
        'journal_online_and_issue_dates_separated':True,'figure_source_sha256':asset['sha256'],
        'quantitative_field_trend_estimated':False,'model_search_pipeline_executed':False,
        'scope':'所选材料登记、日期语义、CSV对应和原图哈希；不验证领域覆盖、科研结论、专利法律状态或创新性。'}
(R/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
