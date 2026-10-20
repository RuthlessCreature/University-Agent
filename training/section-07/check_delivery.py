"""Check source calculations and delivery scope; not scientific acceptance."""
from pathlib import Path
from xml.etree import ElementTree as ET
import csv,hashlib,json,math,re,statistics,subprocess,sys,zipfile
import numpy as np
from pypdf import PdfReader
r=Path(__file__).resolve().parent;rev=sys.argv[1] if len(sys.argv)>1 else 's7-r9'
p=r/'output'/f'高校科研AI课程_Section7_数据处理与统计分析_{rev}.pptx'
a=json.loads((r/'results.json').read_text('utf-8'));d=json.loads((r/'lesson.json').read_text('utf-8'));refs=json.loads((r/'sources.json').read_text('utf-8'))
raw=r/'analysis-packet/penguins.csv';src=json.loads((r/'analysis-packet/source.json').read_text('utf-8'));assert hashlib.sha256(raw.read_bytes()).hexdigest()==src['sha256']==a['raw_sha256']
rows=list(csv.DictReader(raw.open(encoding='utf-8')));assert len(rows)==344
ad=[(i+2,q) for i,q in enumerate(rows) if q['species']=='Adelie'];clean=[(i,q) for i,q in ad if q['sex'] in ['male','female'] and q['flipper_length_mm']!='NA'];assert len(ad)==152 and len(clean)==146
assert [i for i,q in ad if (i,q) not in clean]==a['excluded_rows']
for sex in ['female','male']:
 x=[float(q['flipper_length_mm']) for i,q in clean if q['sex']==sex];v=a[sex];assert len(x)==73==v['n'];assert math.isclose(statistics.mean(x),v['mean'],abs_tol=1e-10);assert math.isclose(statistics.stdev(x),v['sd'],abs_tol=1e-10)
assert math.isclose(a['male']['mean']-a['female']['mean'],a['mean_difference_mm'],abs_tol=1e-10)
boot=np.loadtxt(r/'analysis-packet/bootstrap-differences.csv',skiprows=1);assert len(boot)==10000;assert np.allclose(np.quantile(boot,[.025,.975]),a['bootstrap']['percentile_95'],atol=1e-10,rtol=0)
assert sum(a['histogram']['female'])==sum(a['histogram']['male'])==73 and sum(a['bootstrap']['histogram_counts'])==10000
prob=sum(math.comb(20,k) for k in list(range(6))+list(range(15,21)))/2**20;assert prob==a['coin_teaching']['two_sided_p']
sim=list(csv.DictReader((r/'analysis-packet/normal-ci-simulation.csv').open()));assert len(sim)==1000;assert sum(float(q['lower'])<=100<=float(q['upper']) for q in sim)==a['ci_simulation']['covered']
cmp=json.loads((r/'analysis-packet/teaching-comparisons.json').read_text('utf-8'))
assert hashlib.sha256((r/'analysis-packet/prepare-teaching-comparisons.py').read_bytes()).hexdigest()==cmp['script_sha256']
for name,sha in cmp['source_hashes'].items():assert hashlib.sha256((r/'analysis-packet'/name).read_bytes()).hexdigest()==sha
assert cmp['source_records_deleted']==0 and cmp['ci_first20_miss_repetitions']==[18]
assert [v['repetition'] for v in cmp['ci_prefix_records']]==list(range(1,21))
assert [v['records'] for v in cmp['outlier_scenarios']]==[146,144]
assert [x['n'] for x in d]==list(range(1,23)) and all(k in refs for x in d for k in x['refs'])
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
diagrams=[];tables=[];chartpages=[];texts=[];chart_values=[]
with zipfile.ZipFile(p) as z:
 slides=[x for x in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',x)];notes=[x for x in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',x)];assert len(slides)==len(notes)==22
 for i in range(1,23):
  x=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'));txt=' '.join(t.text or '' for t in x.findall('.//a:t',ns));texts.append(txt);assert d[i-1]['title'] in txt
  if len(x.findall('.//p:cxnSp',ns))>=2:diagrams.append(i)
  if x.findall('.//a:tbl',ns):tables.append(i)
  if x.findall('.//c:chart',ns):chartpages.append(i)
 assert tables==[3,4,7,12,22] and chartpages==[5,8,14,17,18,19]
 charts=sorted([n for n in z.namelist() if re.fullmatch(r'ppt/(?:slides/)?charts/chart\d+\.xml',n)],key=lambda s:int(re.search(r'chart(\d+)\.xml',s).group(1)))
 assert len(charts)==6
 for name in charts:
  x=ET.fromstring(z.read(name));vals=[]
  for ser in x.findall('.//c:ser',ns):
   v=ser.findall('.//c:val/c:numRef/c:numCache/c:pt/c:v',ns) or ser.findall('.//c:yVal/c:numRef/c:numCache/c:pt/c:v',ns) or ser.findall('.//c:val/c:numLit/c:pt/c:v',ns) or ser.findall('.//c:yVal/c:numLit/c:pt/c:v',ns)
   vals.append([float(t.text) for t in v])
  chart_values.append(vals)
 assert chart_values[0]==[[2,2,2,2,11]]
 assert chart_values[1]==[a['histogram']['female'],a['histogram']['male']]
 assert np.allclose(chart_values[2][0],a['coin_teaching']['probabilities'],atol=1e-12)
 coin_xml=ET.fromstring(z.read(charts[2]));red=[]
 for point in coin_xml.findall('.//c:dPt',ns):
  color=point.find('.//a:srgbClr',ns)
  if color is not None and color.get('val','').upper()=='963F3C':red.append(int(point.find('c:idx',ns).get('val')))
 assert red==list(range(6))+list(range(15,21)),red
 assert all(v in texts[6] for v in ['4.616','4.153','172','210'])
 assert '前20次' in texts[12] and '59次未覆盖' in texts[12]
 assert chart_values[3]==[a['bootstrap']['histogram_counts']]
 assert [len(v) for v in chart_values[4]]==[151,68,123]
 for got,expected in zip(chart_values[4],a['scatter']):assert got==expected['y']
 for got,sex in zip(chart_values[5],['female','male']):assert np.allclose(got,[q[sex+'_mean'] for q in a['yearly']],atol=1e-9,rtol=0)
 assert 'noFill' in z.read(charts[4]).decode(),'Scatter lines must be explicitly disabled'
 books=[n for n in z.namelist() if n.startswith('ppt/embeddings/') and n.endswith('.xlsx')];assert len(books)==6
 assert all('http' in z.read(n).decode() or 'local:' in z.read(n).decode() for n in notes)
 assert not any(t in ' '.join(texts) for t in ['课堂练习','请提交','TODO','占位'])
pdf=r/'renders'/rev/(p.stem+'.pdf');assert len(PdfReader(pdf).pages)==22 and len(list((r/'renders'/rev).glob('slide-*.png')))==22
subprocess.run([sys.executable,str(r/'cross-tool/check_results.py')],check=True,capture_output=True)
cross=json.loads((r/'cross-tool/checks.json').read_text('utf-8'))
assert cross['actual_python_and_R_agree'] and not cross['SPSS_actual_execution']
for value in ['146','73','187.79','192.41','5.60','6.60','4.62']:
 assert value in texts[21],f'Missing actual result in slide 22: {value}'
assert '未执行' in texts[20] and '尚未运行' in texts[21]
subprocess.run([sys.executable,str(r/'cursor-packet/check_results.py')],check=True,capture_output=True)
cursor_case=json.loads((r/'cursor-packet/checks.json').read_text('utf-8'))
assert cursor_case['actual_local_python_runs']==2 and cursor_case['cursor_operated'] is False
assert cursor_case['included_rows_identical'] and cursor_case['group_statistics_identical']
assert all(s in texts[20] for s in ['Cursor','Python','+4.616438','−4.616438','146','73'])
prior=r/'output/高校科研AI课程_Section7_数据处理与统计分析_s7-r7.pptx'
unchanged=[];same_previews=[]
with zipfile.ZipFile(prior) as old,zipfile.ZipFile(p) as new:
 for i in range(1,21):
  name=f'ppt/slides/slide{i}.xml'
  old_text=[t.text for t in ET.fromstring(old.read(name)).findall('.//a:t',ns)]
  new_text=[t.text for t in ET.fromstring(new.read(name)).findall('.//a:t',ns)]
  if i in [7,13,14]:continue
  assert old_text==new_text,f'Unexpected content change on slide {i}'
  unchanged.append(i)
  before=r/'renders/s7-r7'/f'slide-{i:02d}.png';after=r/'renders'/rev/f'slide-{i:02d}.png'
  if before.read_bytes()==after.read_bytes():same_previews.append(i)
v=json.loads((r/'.build'/rev/'validation.json').read_text('utf-8'));sha=hashlib.sha256(p.read_bytes()).hexdigest();assert v['finalSha256']==sha and v['packageIntegrity']['findingCount']==v['presentationLayout']['findingCount']==0
(r/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),'utf-8')
report={'revision':rev,'pages':22,'pdf_pages':22,'notes':22,'preview_images':22,'editable_connector_diagram_pages':diagrams,'native_table_pages':tables,'native_chart_pages':chartpages,'embedded_workbooks':len(books),'source_records':len(rows),'analysis_records':len(clean),'mean_difference_mm':a['mean_difference_mm'],'bootstrap_95_percentile':a['bootstrap']['percentile_95'],'exact_coin_teaching_p':prob,'normal_simulation_coverage_count':a['ci_simulation']['covered'],'pptx_sha256':sha,'cross_tool':cross,'unchanged_slide_text_vs_s7_r7':unchanged,'identical_preview_bytes_vs_s7_r7':same_previews,'scope':'文件结构、源CSV独立复算、样本与缺失、图表缓存及最终器工作簿检查；Python和本地WebR实际描述统计一致，SPSS未执行。科学假设、独立性和外推未获证明，不代表科研Agent全系统已运行。'}
report['cursor_case']=cursor_case
report['teaching_comparisons']={'ci_displayed_consecutive_repetitions':20,'ci_first20_misses':[18],'source_records_deleted':0,'outlier_sensitivity_difference_mm':[v['male_minus_female_mm'] for v in cmp['outlier_scenarios']]}
(r/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
