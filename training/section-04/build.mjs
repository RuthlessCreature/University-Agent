import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const R=path.dirname(fileURLToPath(import.meta.url)),rev=process.env.SECTION_REVISION||'s4-r3';
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
function chart(s,d,x,y,w,h,title){const c=s.charts.add('bar',{position:{left:x,top:y,width:w,height:h},title,titleTextStyle:{fontSize:27,typeface:F},categories:d.categories,series:[{name:'比例',values:d.values,fill:C.blue,valuesFormatCode:'0%',points:[{idx:0,fill:C.blue},{idx:1,fill:C.green}]}],hasLegend:false,barOptions:{direction:'column',grouping:'clustered',gapWidth:160},xAxis:{textStyle:{fontSize:20,typeface:F}},yAxis:{min:0,max:1.5,majorUnit:0.5,numberFormatCode:'0%',textStyle:{fontSize:20,typeface:F},majorGridlines:{fill:C.rule,width:1}},dataLabels:{showValue:true,position:'outEnd',numberFormatCode:d.n===6?'0.00%':'0%',textStyle:{fontSize:28,typeface:F}},chartFill:'#FFFFFF',plotAreaFill:'#FFFFFF'});applyPresentationChartFont(c,{fontFamily:F});}
for(const d of data){const s=p.slides.add();s.background.fill='#FFFFFF';T(s,'04  选题与研究问题',80,28,1440,35,20,false,C.muted);T(s,d.title,80,84,1440,82,47,true,C.navy);rule(s,80,184,1440,C.navy,2);T(s,d.thesis,80,213,1440,90,31,false,C.blue);
switch(d.kind){
case 'map':case 'scan':case 'competition':case 'agent':case 'hypothesis':{
 const {step,w}=chain(s,d.nodes,405);d.details.forEach((v,i)=>T(s,v,80+i*step,535,w,140,29));
 const msgs={map:'例：同样讨论AI学习，可以分别研究使用现状、预测风险或帮助方式的效果。',scan:'保留检索记录，才能区分公开证据、模型建议和仍待核查的判断。',competition:'题目变化要写出理由：发现相近工作、获得新数据，或原条件已经不成立。',agent:'研究者复核：来源是否存在？是否遗漏相反结果？当前条件能否取得关键证据？',hypothesis:'主要结果、测量时点和判断规则需要事先说明，结果出来后再按证据解释。'};
 rule(s,80,704,1440);T(s,msgs[d.kind],80,735,1440,65,29);break;}
case 'chart':{
 chart(s,{categories:['GPT Base','GPT Tutor'],values:[.48,1.27],n:3},80,335,820,410,'有AI帮助时，练习成绩相对对照组的提升');
 // Both bars share one outcome and one reference group. Extend axis beyond 100%.

 T(s,'练习阶段',1000,335,520,45,30,true,C.blue);T(s,'Base：常规AI答疑。\nTutor：含教师预设提示。\n均相对无AI对照组比较，\n127%为相对增幅。',1000,390,520,155,28);
 T(s,'撤去资源后的测验',1000,575,520,45,30,true,C.red);T(s,'Base组相对对照低17%。\nTutor组与对照差异未显著。',1000,630,520,110,28);T(s,'选题启发：明确“学会”指什么、在何时测量。',80,760,1440,50,31,true,C.green);break;}
case 'narrow':{
 d.nodes.forEach((v,i)=>{let y=330+i*112;let a=N(s,v,80+i*100,y,670,76,i===3?'#E7F2EF':'#F0F5F8');if(i>0)A(s,s._prev,a,'bottom','top');s._prev=a;T(s,d.details[i],1120,y+12,400,85,28);});break;}
case 'types':{
 d.rows.forEach((r,i)=>{let y=330+i*155;T(s,r[0],80,y,180,65,35,true,C.blue);const a=N(s,r[1],280,y,630,80);const b=N(s,r[2],1060,y,460,80,'#E7F2EF');A(s,a,b);T(s,r[3],1060,y+93,460,48,26);});break;}
case 'causal':{
 const a=N(s,'原有基础',580,330,400,85),b=N(s,'AI使用',180,560,400,85),c=N(s,'后续成绩',1020,560,400,85),e=N(s,'学习投入',580,710,400,75);A(s,a,b,'left','top');A(s,a,c,'right','top');A(s,b,c);A(s,e,b,'left','bottom');A(s,e,c,'right','bottom');T(s,'待估计的影响',650,515,300,60,28,true,C.red);T(s,'可能同时影响使用和成绩',570,430,470,55,28);break;}
case 'gap':{
 d.rows.forEach((r,i)=>{let y=328+i*113;T(s,r[0],80,y+10,230,60,29,true,C.blue);const a=N(s,r[1],350,y,470,78,i===3?'#F8EDE9':'#F0F5F8'),b=N(s,r[2],1010,y,510,78);A(s,a,b);});break;}
case 'dimensions':{
 const mid=N(s,'候选研究问题',80,505,350,90,'#E7F2EF');d.rows.forEach((r,i)=>{let y=330+i*116;let a=N(s,r[0],680,y,260,74);A(s,mid,a,'right','left','elbow');T(s,r[1],1030,y-3,490,53,28,true);T(s,r[2],1030,y+51,490,51,26,false,C.muted);});break;}
case 'decision':{
 let a=N(s,d.nodes[0],80,450,540,100),b=N(s,d.nodes[1],800,335,300,75,'#E7F2EF'),c=N(s,d.nodes[2],1180,335,340,100),e=N(s,d.nodes[3],800,615,300,75,'#F8EDE9'),f=N(s,d.nodes[4],1180,600,340,115);A(s,a,b,'right','left','elbow');A(s,a,e,'right','left','elbow');A(s,b,c);A(s,e,f);T(s,'例：有问卷但缺少成绩和使用记录时，能回答的问题会改变。',80,755,1440,55,29);break;}
case 'table':{
 let t=s.tables.add({rows:4,columns:4,left:80,top:335,width:1440,height:440,values:d.rows,columnWidths:[350,320,440,330]});t.cells.block({row:0,column:0,rowCount:4,columnCount:4}).assign({fill:'#FFFFFF',textStyle:{typeface:F,fontSize:27,color:C.ink},margins:{top:18,left:15,right:15,bottom:10},anchor:'top'});t.borders.assign({fill:C.rule,width:1});t.cells.block({row:0,column:0,rowCount:1,columnCount:4}).assign({fill:C.navy,textStyle:{typeface:F,fontSize:28,bold:true,color:'#FFFFFF'}});break;}
case 'finish':{
 d.nodes.forEach((v,i)=>{let y=330+i*114;let a=N(s,v,80,y,420,75,i===3?'#F8EDE9':'#E7F2EF');T(s,d.details[i],680,y-2,840,90,29);if(i)A(s,s._prev,a,'bottom','top');s._prev=a;});break;}
}
T(s,d.bottom,80,823,1440,48,22,false,C.green);T(s,'来源：'+d.refs.map(k=>refs[k].short).join('；'),80,875,1340,22,15,false,C.muted);T(s,String(d.n).padStart(2,'0'),1450,864,70,34,23,false,C.muted);s.speakerNotes.text=d.notes+'\n\n'+d.refs.map(k=>refs[k].title+'\n'+refs[k].url+'\n定位：'+refs[k].location).join('\n\n');}
const candidate=path.join(stage,'candidate.pptx');await(await PresentationFile.exportPptx(p)).save(candidate);
await finalizePresentation({workspaceDir:R,candidatePath:candidate,finalPath:path.join(R,'output',`高校科研AI课程_Section4_选题与研究问题_${rev}.pptx`),pythonExecutable:PY,integrityValidatorPath:path.join(S,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(S,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-heading-fit','--require-native-table-slide','12'],fontPolicy:{basis:'design',families:[F]},explicitTotalSlideCount:14,requiredNativeTableOwnerSlides:[12],requiredNativeChartOwnerSlides:[3],materializeLiteralChartWorkbooks:true,verifyArtifactToolImport:true,receiptPath:path.join(stage,'validation.json')});console.log('FINAL',rev,'14 slides');
