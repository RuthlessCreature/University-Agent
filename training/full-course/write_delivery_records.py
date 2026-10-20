"""Write navigation and records after manual review of all final previews."""
from pathlib import Path
import json, hashlib, csv, html
from datetime import datetime
r=Path(__file__).resolve().parent
root=r.parents[1]
def load(p): return json.loads(p.read_text('utf-8'))
def save(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n','utf-8',newline='\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
m=load(r/'assembly-manifest.json'); sections=m['source_sections']; rev=m['revision']
notes={41:'流程说明换行较碎，待排版微调。',45:'流程说明换行较碎，待排版微调。',51:'流程说明换行较碎，待排版微调。',181:'说明文字换行可再精简。',183:'说明文字换行可再精简。',187:'说明文字换行可再精简。',189:'说明文字换行可再精简。',193:'说明文字换行可再精简。',203:'说明文字换行可再精简。',205:'说明文字换行可再精简。',208:'说明文字换行可再精简。'}
changed=set()
if rev=='course-r3':
 notes={};comparison=load(r/'revision-comparison.json');changed=set(comparison['changed_pages'])
 assert changed=={q['global_page'] for q in load(r/'wrap-review.json')['changed_pages']}
pages=[]
for s in sections:
 for n in range(s['first_page'],s['last_page']+1):
  png=r/'renders'/rev/f'slide-{n:03}.png'
  mode='本轮实际打开查看' if rev!='course-r3' or n in changed else '与course-r2已审阅页面RGB像素相同，沿用原页视觉记录'
  pages.append(dict(page=n,section=s['section'],section_page=n-s['first_page']+1,preview=png.relative_to(r).as_posix(),sha256=sha(png),reviewed_visually=True,review_mode=mode,result='可阅读；有排版待改项' if n in notes else '未见丢图或文字遮挡',note=notes.get(n,'')))
method='实际打开并查看全部240张最终PNG。' if rev!='course-r3' else '本轮实际查看11张修改页；其余229张与course-r2已审阅预览RGB像素相同。前版逐页审阅记录保存在history/course-r2/visual-review.json。'
save(r/'visual-review.json',dict(revision=rev,reviewed_pages=240,review_method=method,scope='合并后的视觉检查；不替代科学审查、逐项来源复核、真人计时或用户教学验收。',open_items=notes,pages=pages))
with (r/'navigation.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['section','内容','全课起页','全课止页','页数','分节版本'])
 for s in sections:w.writerow([s['section'],s['title'],s['first_page'],s['last_page'],s['pages'],s['revision']])
lines=['# 全课页码导航','','PPT右下角保留分节页码；下表为合并文件中的实际页码。PDF另有15个章节书签。','','| Section | 内容 | 全课页码 | 页数 | 分节版本 |','| --- | --- | --- | --- | --- |']
for s in sections:lines.append(f"| {s['section']} | {s['title']} | {s['first_page']}–{s['last_page']} | {s['pages']} | {s['revision']} |")
(r/'NAVIGATION.md').write_text('\n'.join(lines)+'\n','utf-8',newline='\n')
cards=''.join(f'<figure><a href="{q["preview"]}"><img loading="lazy" src="{q["preview"]}" alt="全课第{q["page"]}页"></a><figcaption>全课 {q["page"]} · Section {q["section"]} / {q["section_page"]} {html.escape(q["note"])}</figcaption></figure>' for q in pages)
(r/'preview.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>高校科研AI课程 · 240页预览</title><style>body{font:16px system-ui;margin:32px;background:#edf2f5;color:#183345}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(480px,1fr));gap:24px}figure{margin:0;background:white;padding:12px}img{width:100%}figcaption{padding:10px}</style><h1>高校科研AI课程 · 240页预览</h1><p>点击页面看原尺寸。分节页码与全课页码见 NAVIGATION.md。此版待教学审阅。</p><main>'+cards+'</main></html>','utf-8',newline='\n')
progress=load(root/'training/curriculum/section-progress.json')
ppt=r/'output'/f'高校科研AI培训课程_全课240页_{rev}.pptx'
pdf=r/'output'/f'高校科研AI培训课程_全课240页_{rev}_含章节书签.pdf'
progress['assembled_course']=dict(revision=rev,status='assembled_for_review',user_accepted=False,pages=240,pptx=ppt.relative_to(root).as_posix(),pptx_sha256=sha(ppt),pdf=pdf.relative_to(root).as_posix(),pdf_sha256=sha(pdf),checks='training/full-course/checks.json',visual_review='training/full-course/visual-review.json',navigation='training/full-course/NAVIGATION.md')
save(root/'training/curriculum/section-progress.json',progress)
print('Wrote navigation, gallery, 240-page visual review and assembled-course registration.')
