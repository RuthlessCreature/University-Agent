"""Check teaching inputs and declared execution state; never invoke a model."""
from pathlib import Path
import hashlib,json
from pypdf import PdfReader

R=Path(__file__).resolve().parent
d=json.loads((R/'case.json').read_text('utf-8'))
f=d['common_facts']
for name,digest in d['input_sha256'].items():
    assert hashlib.sha256((R.parent/'sources'/name).read_bytes()).hexdigest()==digest
source=PdfReader(R.parent/'sources/citation-study.pdf')
page=source.pages[3].extract_text()
assert all(x in page for x in ['Table 3.','Table 4.','55% (222)','18% (414)','43% 24%','101 340'])
data=json.loads((R.parent/'sources/citation-data.json').read_text('utf-8'))
assert f['reported_references']==sum(x['n_all_references'] for x in data['chart_data'])==636
assert f['reported_fabrication_proportions']==[x['fabrication_proportion'] for x in data['chart_data']]
assert f['reported_substantive_error_among_real_proportions']==[data['separate_metric'][k] for k in ['GPT-3.5','GPT-4']]
draft=(R/'人工核对示例.md').read_text('utf-8')
assert all(x in draft for x in ['55%','18%','43%','24%','分母','2023','10.1038/s41598-023-41032-5'])
for route in d['routes']:
    assert route['executed'] is False and route['result_file'] is None
    text=(R/route['prompt_file']).read_text('utf-8')
    assert all(x in text for x in ['未在该入口执行','分母','研究年份','缺口'])
lesson=json.loads((R.parent/'lesson.json').read_text('utf-8'))[8]
assert lesson['n']==d['slide']==9 and lesson['kind']=='assistant-choice'
assert len(lesson['routes'])==len(d['routes'])==3
sources=json.loads((R.parent/'sources.json').read_text('utf-8'))
assert all(x in sources for x in lesson['refs'])
result={'source_pdf_pages':len(source.pages),'source_location':'PDF第4页表3、4',
        'input_hashes_verified':len(d['input_sha256']),'reported_references':636,
        'reported_proportions':[0.55,0.18,0.43,0.24],'prompt_files':3,
        'product_runs':0,'product_output_files':0,
        'scope':'输入完整性、原文报告值和教学材料状态对应；不验证模型输出质量、账户功能或三方执行。'}
(R/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
