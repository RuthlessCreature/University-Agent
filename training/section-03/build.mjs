import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const R=path.dirname(fileURLToPath(import.meta.url)),rev=process.env.SECTION_REVISION||'s3-r3';
const S='C:/Users/Georgij Xe/.codex/plugins/cache/openai-primary-runtime/presentations/26.1015.12040/skills/presentations';
const PY='C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(path.join(S,'container_tools/artifact_tool_utils.mjs')).href);
const data=JSON.parse(await fs.readFile(path.join(R,'lesson.json'),'utf8')),refs=JSON.parse(await fs.readFile(path.join(R,'sources.json'),'utf8'));
const stage=path.join(R,'.build',rev);await fs.mkdir(stage,{recursive:true});await fs.mkdir(path.join(R,'output'),{recursive:true});
const p=Presentation.create({slideSize:{width:1600,height:900}}),F='Microsoft YaHei';p.theme.defaultFont=F;
const C={navy:'#132F43',ink:'#263D4A',blue:'#245B77',muted:'#627681',green:'#2C6D68',red:'#963F3C',rule:'#CAD6DC'};
function T(s,v,x,y,w,h=70,z=29,b=false,c=C.ink){const t=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});t.text=v;t.text.style={typeface:F,fontSize:z,bold:b,color:c,autoFit:'none',wrap:'word',insets:0,verticalAlignment:'top'};return t;}
function rule(s,x,y,w,color=C.rule,width=1){s.shapes.add({geometry:'line',position:{left:x,top:y,width:w,height:0},line:{fill:color,width}});}
function N(s,v,x,y,w=320,h=85,fill='#F0F5F8'){const a=s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:C.blue,width:1.5}});a.text=v;a.text.style={typeface:F,fontSize:31,bold:true,color:C.navy,autoFit:'none',wrap:'word',insets:12,verticalAlignment:'middle'};return a;}
function A(s,a,b,from='right',to='left',kind='straight'){s.shapes.connect(a,b,{kind,fromSide:from,toSide:to,line:{fill:C.blue,width:2},tail:{type:'arrow',width:'med',length:'med'}});}
function chain(s,labels,y=420){const count=labels.length,step=count===4?380:510,w=count===4?300:420;const ns=labels.map((v,i)=>N(s,v,80+i*step,y,w,90,i===count-1?'#E7F2EF':'#F0F5F8'));for(let i=0;i<count-1;i++)A(s,ns[i],ns[i+1]);return {ns,step,w};}
function pair(s,d,y=370){T(s,'原句',80,y-50,620,45,28,true,C.red);T(s,'修订稿',900,y-50,620,45,28,true,C.green);T(s,d.before,80,y,620,180,31);T(s,d.after,900,y,620,180,31);T(s,'→',740,y+75,100,70,45,true,C.blue);chain(s,['同一数据集','两种方法分别处理','比较差异'],570);if(d.reason)T(s,d.reason,80,715,1440,85,29,false,C.blue);}
function chart(s,d,x,y,w,h,title){const c=s.charts.add('bar',{position:{left:x,top:y,width:w,height:h},title,titleTextStyle:{fontSize:27,typeface:F},categories:d.categories,series:[{name:'比例',values:d.values,fill:C.blue,valuesFormatCode:'0%',points:[{idx:0,fill:C.blue},{idx:1,fill:C.green}]}],hasLegend:false,barOptions:{direction:'column',grouping:'clustered',gapWidth:160},xAxis:{textStyle:{fontSize:20,typeface:F}},yAxis:{min:0,max:1,majorUnit:0.2,numberFormatCode:'0%',textStyle:{fontSize:20,typeface:F},majorGridlines:{fill:C.rule,width:1}},dataLabels:{showValue:true,position:'outEnd',numberFormatCode:d.n===6?'0.00%':'0%',textStyle:{fontSize:28,typeface:F}},chartFill:'#FFFFFF',plotAreaFill:'#FFFFFF'});applyPresentationChartFont(c,{fontFamily:F});}
for(const d of data){const s=p.slides.add();s.background.fill='#FFFFFF';T(s,'03  Humanizer 与各类科研产物的表达',80,28,1440,35,20,false,C.muted);T(s,d.title,80,84,1440,82,47,true,C.navy);rule(s,80,184,1440,C.navy,2);T(s,d.thesis,80,213,1440,85,31,false,C.blue);
 switch(d.kind){
 case 'finish':{
  const a=N(s,'修订交付',80,470,350,105,'#E7F2EF');d.nodes.forEach((v,i)=>{const y=330+i*150,b=N(s,v,650,y,350,85);A(s,a,b,'right','left','elbow');T(s,d.details[i],1110,y+5,410,110,28);});
  T(s,'读者能看懂正文；作者能核对变化，并处理仍未解决的问题。',80,755,1440,50,29,true,C.blue);break;}
 case 'opening':case 'workflow':case 'disclosure':{
  const {step,w}=chain(s,d.nodes,385);d.details.forEach((v,i)=>T(s,v,80+i*step,510,w,120,29));
  const label=d.kind==='opening'?'作者判断':d.kind==='workflow'?'修订记录':d.kind==='disclosure'?'使用说明':'阅读与复核';
  const msg=d.kind==='opening'?'作者能解释句子里的对象、方法、结果和限制。':d.kind==='workflow'?'原句、改句、修改理由，以及不能自行补写的内容。':d.kind==='disclosure'?'自然表达、事实核对和透明使用需要同时保留。':'读者能看懂正文；作者能核对变化，并处理仍未解决的问题。';
  T(s,label,80,685,300,60,34,true,C.blue);T(s,msg,450,685,1070,95,31);break;}
 case 'annotate':{
  T(s,d.before,80,322,1440,155,34);d.marks.forEach((r,i)=>{const y=515+i*86;T(s,r[0],80,y,360,60,30,true,C.red);rule(s,80,y+49,280,C.red,2);T(s,r[1],500,y,1020,73,30);});break;}
 case 'decision':{
  const a=N(s,d.nodes[0],80,440,510,100),b=N(s,d.nodes[1],900,350,620,100,'#E7F2EF'),c=N(s,d.nodes[2],900,560,620,100,'#F8EDE9');A(s,a,b,'right','left','elbow');A(s,a,c,'right','left','elbow');T(s,d.example,80,710,1440,80,30);break;}
 case 'qualifier':{
  T(s,'原意：保留可能性',80,335,1440,50,30,true,C.green);T(s,d.before,80,405,1440,65,38,true);rule(s,308,459,76,C.green,3);T(s,'润色后的风险：判断更肯定',80,535,1440,50,30,true,C.red);T(s,d.after,80,605,1440,65,38,true);T(s,d.explain,80,724,1440,70,29);break;}
 case 'locks':{
  T(s,d.fact,80,330,1440,120,33);const top=N(s,'保持含义不变',80,580,320,100,'#E7F2EF');d.rows.forEach((r,i)=>{const y=478+i*106,b=N(s,r[0],560,y,350,76);A(s,top,b,'right','left','elbow');T(s,r[1],1030,y+12,490,70,29);});break;}
 case 'detector':{
  chart(s,d,80,345,820,400,'人工作文被判为 AI 文本的平均比例');d.points.forEach((v,i)=>T(s,v,1000,360+i*130,520,113,30,i===0));break;}
 case 'pair':pair(s,d);break;
 case 'proposal':case 'status':case 'feedback':{
  T(s,'原句',80,320,250,45,27,true,C.red);T(s,d.before,330,320,1190,115,29);rule(s,80,450,1440);
  T(s,'修订稿',80,478,250,45,27,true,C.green);T(s,d.after,330,478,1190,150,30);
  const {step,w}=chain(s,d.nodes,650);d.details.forEach((v,i)=>T(s,v,80+i*step,752,w,55,23));break;}
 case 'slide':{
  T(s,'文字堆在一起',80,320,1440,45,27,true,C.red);T(s,d.before,80,375,1440,110,30);
  T(s,'用步骤和依据组织页面',80,500,1440,45,27,true,C.green);const {step,w}=chain(s,d.nodes,570);d.details.forEach((v,i)=>T(s,v,80+i*step,690,w,99,27));break;}
 case 'caption':{
  chart(s,d,80,330,720,395,'虚构文献占所引文献的比例');T(s,'评价性图注',900,330,620,45,28,true,C.red);T(s,d.bad,900,390,620,110,30);T(s,'说明对象、分母和来源',900,530,620,45,28,true,C.green);T(s,d.caption,900,590,620,195,28);break;}
 case 'translation':{
  d.rows.forEach((r,i)=>{let y=337+i*149;const a=N(s,r[0],80,y,610,78),b=N(s,r[1],900,y,620,78,'#E7F2EF');A(s,a,b);T(s,r[2],900,y+91,620,55,27,false,C.red);});break;}
 case 'prompt':{
  T(s,d.prompt,80,325,1440,285,31);const {ns}=chain(s,d.nodes,680);break;}
 case 'audit':{
  const rows=[['核对项','风险改动示例','处理办法'],...d.rows];const t=s.tables.add({rows:5,columns:3,left:80,top:330,width:1440,height:440,values:rows,columnWidths:[260,520,660]});t.cells.block({row:0,column:0,rowCount:5,columnCount:3}).assign({fill:'#FFFFFF',textStyle:{typeface:F,fontSize:28,color:C.ink},margins:{top:17,left:17,right:17,bottom:12},anchor:'top'});t.borders.assign({fill:C.rule,width:1});t.cells.block({row:0,column:0,rowCount:1,columnCount:3}).assign({fill:C.navy,textStyle:{typeface:F,fontSize:29,bold:true,color:'#FFFFFF'}});break;}
 }
 T(s,d.bottom,80,817,1440,48,23,false,C.green);T(s,'来源：'+d.refs.map(k=>refs[k].short).join('；'),80,874,1340,22,15,false,C.muted);T(s,String(d.n).padStart(2,'0'),1450,862,70,34,23,false,C.muted);
 s.speakerNotes.text=d.notes+'\n\n'+d.refs.map(k=>refs[k].title+'\n'+refs[k].url+'\n定位：'+refs[k].location).join('\n\n');
}
const candidate=path.join(stage,'candidate.pptx');await(await PresentationFile.exportPptx(p)).save(candidate);
await finalizePresentation({workspaceDir:R,candidatePath:candidate,finalPath:path.join(R,'output',`高校科研AI课程_Section3_Humanizer_${rev}.pptx`),pythonExecutable:PY,integrityValidatorPath:path.join(S,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(S,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-heading-fit','--require-native-table-slide','16'],fontPolicy:{basis:'design',families:[F]},explicitTotalSlideCount:18,requiredNativeTableOwnerSlides:[16],requiredNativeChartOwnerSlides:[6,12],materializeLiteralChartWorkbooks:true,verifyArtifactToolImport:true,receiptPath:path.join(stage,'validation.json')});
console.log('FINAL',rev,'18 slides');
