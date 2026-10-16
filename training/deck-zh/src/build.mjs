import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const SKILL='C:/Users/Georgij Xe/.codex/plugins/cache/openai-primary-runtime/presentations/26.1013.11914/skills/presentations';
const PY='C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const all=JSON.parse(await fs.readFile(path.join(ROOT,'slides_manifest.json'),'utf8'));
const isSample=process.argv.includes('--sample');
const data=isSample?all.filter(s=>s.sample):all;
const tableKinds=['table','mapping','schedule','policy','statistics'];
const tableOwners=data.flatMap((d,i)=>tableKinds.includes(d.visual_type)?[i+1]:[]);
const suffix=isSample?'12_Sample':'ZH';
const out=path.join(ROOT,'dist',`University_AI_Research_Training_${suffix}_v7.pptx`);
const renderDir=path.join(ROOT,'renders',isSample?'sample':'full');
const stage=path.join(ROOT,'.build',suffix+'-v7');await fs.mkdir(stage,{recursive:true});await fs.mkdir(renderDir,{recursive:true});
const p=Presentation.create({slideSize:{width:1600,height:900}});
const F='Microsoft YaHei';p.theme.defaultFont=F;const C={navy:'#17324D',ink:'#243442',muted:'#596A76',blue:'#235F85',pale:'#EDF3F6',rule:'#CED9E0',red:'#91412E'};
const provenance=JSON.parse(await fs.readFile(path.join(ROOT,'sources/manifest.json'),'utf8'));
function text(s,str,x,y,w,h,size=32,bold=false,color=C.ink){
 const t=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});t.text=str;
 t.text.style={typeface:F,fontSize:size,bold,color,verticalAlignment:'top',autoFit:'none',wrap:'word',insets:{top:0,left:0,right:0,bottom:0}};return t;
}
function rect(s,x,y,w,h,fill=C.pale){return s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:'none',width:0}});}
function rule(s,x,y,w){rect(s,x,y,w,1,C.rule);}
function table(s,rows,{x=80,y=205,w=1440,h=540,widths=null,font=28,header=true}={}){
 const cols=rows[0].length;const t=s.tables.add({rows:rows.length,columns:cols,left:x,top:y,width:w,height:h,values:rows,columnWidths:widths||(cols===2?[300,w-300]:Array(cols).fill(w/cols))});
 const range=t.cells.block({row:0,column:0,rowCount:rows.length,columnCount:cols});
 range.assign({fill:'#FFFFFF',textStyle:{typeface:F,fontSize:font,color:C.ink},margins:{top:17,bottom:12,left:18,right:16},anchor:'top'});
 t.borders.assign({fill:C.rule,width:1,style:'solid'});
 if(header)t.cells.block({row:0,column:0,rowCount:1,columnCount:cols}).assign({fill:C.pale,textStyle:{typeface:F,fontSize:font,bold:true,color:C.navy}});
 return t;
}
async function original(s,name,x,y,w,h){const b=await fs.readFile(path.join(ROOT,'assets',name));s.images.add({blob:b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),contentType:'image/png',alt:'Gorman et al. 2014 original published scientific figure, CC BY, unchanged',fit:'contain',position:{left:x,top:y,width:w,height:h}});}
const csv=(await fs.readFile(path.join(ROOT,'sources/penguins.csv'),'utf8')).trim().split(/\r?\n/).map(l=>l.split(','));const head=csv.shift();
const obs=csv.map(r=>Object.fromEntries(head.map((h,i)=>[h,r[i]])));
for(let index=0;index<data.length;index++){
 const d=data[index],s=p.slides.add();s.background.fill='#FFFFFF';
 text(s,d.optional?'延伸备课':d.module,80,42,1370,38,23,true,C.blue);
 text(s,d.title,80,100,1440,90,50,true,C.navy);
 const simulation=['M101','M207','M208','M304','M312','M313','M314','M321','M322','M323','M401','M318'].includes(d.id);
 const source=d.id.startsWith('REF')?'完整链接见本页备注与来源台账':d.source==='teaching'?(simulation?'教学模拟案例':'课程方法讲义'):d.source.split(';').map(k=>provenance.find(x=>x.id===k)?.title||k).join('；');
 text(s,`${source}  ·  ${d.id}`,80,830,1350,45,19,false,C.muted);text(s,String(index+1).padStart(2,'0'),1450,830,70,38,22,false,C.muted);
 s.speakerNotes.text=`教学目标：${d.learning_point}\n讲解预算：${d.estimated_time_sec}秒\n${d.speaker_notes}\n来源：\n${d.source.split(';').map(k=>provenance.find(x=>x.id===k)?.url||'本课程原创教学模拟 / 分析框架').join('\n')}\n材料属性：${d.example_or_data}`;
 if(['table','mapping','schedule','policy'].includes(d.visual_type)){
  const rows=d.visual_type==='schedule'?[['时间','模块','主要材料'],...d.body]:d.visual_type==='policy'?[['使用情境','具体任务','研究者责任'],...d.body]:d.body;
  table(s,rows,{h:d.visual_type==='schedule'?510:550,font:28,widths:rows[0].length===3?[330,560,550]:null});
  if(d.visual_type==='schedule')text(s,'正式授课 370 分钟  /  短休 20 分钟  /  延伸备课 110 分钟',96,746,1380,55,29,true,C.blue);
 }else if(d.visual_type==='compare'){
  const gap=d.body.length===2?255:185;
  for(let i=0;i<d.body.length;i++){const y=215+i*gap;text(s,d.body[i][0],80,y,255,100,30,true,C.blue);text(s,d.body[i][1],365,y,1145,gap-30,34);if(i<d.body.length-1)rule(s,365,y+gap-24,1145);}
 }else if(d.visual_type==='figure'){
  await original(s,d.asset,80,205,850,570);
  let y=225;for(const b of d.body){text(s,b,990,y,520,135,30);y+=137;}
  text(s,'原论文图，未经生成式重绘。Gorman et al. (2014), CC BY',90,782,850,34,19,false,C.muted);
 }else if(d.visual_type==='architecture'){
  text(s,'Agentic AI：具有一定自主性的系统行为与设计',80,200,1420,60,34,true,C.blue);
  const nodes=[];const specs=[['Workflow',80,325,370,180,'预定步骤、条件与人工关口'],['AI Agent',600,325,370,180,'根据工具结果选择下一步'],['Skill',1120,325,390,180,'复用指令、脚本与模板'],['生成式模型',600,630,370,145,'生成候选内容或动作'],['MCP',1120,630,390,145,'连接外部工具与资源']];
  for(const [name,x,y,w,h,note] of specs){const a=rect(s,x,y,w,h,C.pale);nodes.push(a);text(s,name,x+20,y+15,w-40,55,35,true,C.navy);text(s,note,x+20,y+80,w-40,90,27);}
  for(const [a,b] of [[0,1],[1,2],[1,3],[2,4]])s.shapes.connect(nodes[a],nodes[b],{kind:'straight',line:{fill:C.blue,width:2},tail:{type:'arrow'}});
  text(s,'编排',475,350,100,40,24,false,C.blue);text(s,'选用',995,350,100,40,24,false,C.blue);
 }else if(d.visual_type==='lanes'){
  const nodes=[];for(let r=0;r<4;r++){const y=230+r*120;rect(s,80,y,1440,112,r%2===0?'#F1F5F7':'#FFFFFF');text(s,d.body[r][0],95,y+29,240,60,29,true,C.navy);nodes[r]=[];for(let c=1;c<4;c++)nodes[r].push(text(s,d.body[r][c],360+(c-1)*390,y+29,345,72,27));}
  for(let r=0;r<4;r++)for(let c=0;c<2;c++)s.shapes.add({geometry:'connector',kind:'straight',position:{left:700+c*390,top:315+r*120,width:42,height:0},line:{fill:C.blue,width:2},tail:{type:'arrow'}});
  text(s,'本地运行链路与云端设计分别验收；云端联调和部署尚未验证',90,750,1410,60,30,true,C.blue);
 }else if(d.visual_type==='route'){
  const count=d.body.length, ww=count===5?250:320,gg=35;
  for(let i=0;i<count;i++){const x=80+i*(ww+gg);text(s,String(i+1).padStart(2,'0'),x,266,80,75,48,true,C.blue);text(s,d.body[i][0],x,385,ww,130,32,true);text(s,d.body[i][1],x,535,ww,100,29);text(s,d.body[i][2],x,675,ww,100,25,false,C.red);if(i<count-1)text(s,'→',x+ww+4,274,32,45,28,true,C.blue);}
 }else if(d.visual_type==='scatter'){
  const colors=['#235F85','#A55B36','#387A68'],symbols=['circle','triangle','square'];
  const series=['Adelie','Chinstrap','Gentoo'].map((name,i)=>{const a=obs.filter(r=>r.species===name&&r.body_mass_g!=='NA'&&r.flipper_length_mm!=='NA');return {name,xValues:a.map(r=>+r.flipper_length_mm),values:a.map(r=>+r.body_mass_g),fill:colors[i],marker:{symbol:symbols[i],size:6,fill:colors[i]},line:{fill:'none',width:0}};});
  s.charts.add('scatter',{position:{left:80,top:210,width:950,height:540},series,scatterOptions:{style:'marker'},hasLegend:true,legend:{position:'bottom',textStyle:{typeface:F,fontSize:23}},xAxis:{title:{text:'鳍肢长度 (mm)',textStyle:{fontSize:25}},textStyle:{typeface:F,fontSize:23},min:170,max:235},yAxis:{title:{text:'体重 (g)',textStyle:{fontSize:25}},textStyle:{typeface:F,fontSize:23},min:2500,max:6500,majorGridlines:{fill:'#E4EAEE',width:1}},chartFill:'#FFFFFF'});
  for(let i=0;i<d.body.length;i++)text(s,d.body[i],1090,235+i*173,425,155,30);
  text(s,'原始观测，完整配对 n = 342；没有随机采样或生成数据',90,770,970,40,24,false,C.muted);
 }else if(d.visual_type==='statistics'){
  table(s,d.body,{y:215,h:360,widths:[400,260,390,390],font:31});
  text(s,'SD 描述个体离散，SE 描述估计量变动，CI 需要抽样模型',95,625,1390,60,35,true,C.blue);
  text(s,'本页仅为公开数据的描述性复算。缺失体重 2 行；未进行显著性检验。',95,722,1390,70,30);
 }
 console.log('author',index+1,d.id);
}
// Candidate is finalized before delivery. Render the authored object AND final PPTX via LO later.
await (await PresentationFile.exportPptx(p)).save(path.join(stage,'candidate.pptx'));
for(let i=0;i<p.slides.items.length;i++){
 const png=await p.export({slide:p.slides.items[i],format:'png',scale:1});await fs.writeFile(path.join(renderDir,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));console.log('render',i+1);
}
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
await finalizePresentation({workspaceDir:ROOT,candidatePath:path.join(stage,'candidate.pptx'),finalPath:out,pythonExecutable:PY,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-heading-fit',...tableOwners.flatMap(n=>['--require-native-table-slide',String(n)])],fontPolicy:{basis:'design',families:[F]},verifyArtifactToolImport:true,explicitTotalSlideCount:data.length,requiredNativeChartOwnerSlides:data.flatMap((d,i)=>d.visual_type==='scatter'?[i+1]:[]),nativeChartTargetApplication:'portable',materializeLiteralChartWorkbooks:true,requiredNativeTableOwnerSlides:tableOwners,receiptPath:path.join(stage,'validation.json')});
await fs.writeFile(path.join(stage,'authored.json'),JSON.stringify(p.toProto()));
console.log('FINAL',out);
