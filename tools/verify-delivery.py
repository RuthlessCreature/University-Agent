"""Inspect delivered bytes, source statistics and local workflow artifacts."""
from pathlib import Path
import csv, hashlib, json, re, statistics, zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / 'training/deck-zh'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

slides = json.loads((DECK/'slides_manifest.json').read_text('utf-8'))
assert len(slides) == 75 and sum(bool(s.get('sample')) for s in slides) == 12
assert sum(s['estimated_time_sec'] for s in slides if not s.get('optional')) == 370*60
assert sum(s['estimated_time_sec'] for s in slides if s.get('optional')) == 110*60
assert all(s['speaker_notes'].strip() and not s['human_review'] for s in slides)
report = {'review_date':'2026-10-17', 'slide_count':75, 'sample_count':12,
          'main_minutes':370, 'extension_minutes':110, 'instructor_accepted':False,
          'model_api_called':False, 'cloud_deployed':False, 'packages':[], 'local_outputs':[]}
for suffix, count in [('12_Sample',12), ('ZH',75)]:
    path=DECK/'dist'/f'University_AI_Research_Training_{suffix}_v7.pptx'
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        names=z.namelist()
        parts=[n for n in names if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
        notes=[n for n in names if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)]
        assert len(parts)==len(notes)==count
        texts=' '.join(' '.join(ET.fromstring(z.read(n)).itertext()) for n in parts)
        assert not any(x in texts for x in ['Click to add', 'Lorem ipsum', '单击此处添加', '待填充'])
        charts=[n for n in names if re.fullmatch(r'ppt/(?:slides/)?charts/chart\d+\.xml',n)]
        workbooks=[n for n in names if n.startswith('ppt/embeddings/') and n.endswith('.xlsx')]
        assert len(charts)==1 and workbooks
        with zipfile.ZipFile(__import__('io').BytesIO(z.read(workbooks[0]))) as w:
            assert w.testzip() is None
    report['packages'].append(dict(file=str(path.relative_to(ROOT)),sha256=sha(path),bytes=path.stat().st_size,
                                   slides=count,notes=count,charts=len(charts),embedded_workbooks=len(workbooks)))
rows=list(csv.DictReader((DECK/'sources/penguins.csv').open(encoding='utf-8')))
stats=json.loads((DECK/'sources/penguins-statistics.json').read_text('utf-8'))
assert len(rows)==344
for species, record in stats['groups'].items():
    values=[float(row['body_mass_g']) for row in rows if row['species']==species and row['body_mass_g']!='NA']
    assert len(values)==record['n']
    assert abs(statistics.mean(values)-record['mean'])<1e-10
    assert abs(statistics.stdev(values)-record['sd'])<1e-10
report['statistics_recomputed']=True
for item in json.loads((DECK/'sources/manifest.json').read_text('utf-8')):
    if item.get('kind')=='public-real-asset':
        asset=DECK/Path(item['local_path'].replace('\\','/'))
        assert sha(asset)==item['sha256']
for kind in ['grant','paper','patent']:
    folder=ROOT/'training/demos'/kind/'output'
    run=json.loads((folder/'run.json').read_text('utf-8'));doc=folder/run['artifact']
    assert zipfile.is_zipfile(doc) and sha(doc)==run['artifact_sha256']
    assert run['external_model_called'] is False and run['human_approved'] is False
    report['local_outputs'].append(dict(kind=kind,sha256=sha(doc),status=run['status']))
(ROOT/'evidence/delivery-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
print('PASS: delivered PPTX/notes/workbook, source data, assets and three actual DOCX outputs')
