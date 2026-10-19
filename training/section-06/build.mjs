import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const R=path.dirname(fileURLToPath(import.meta.url)),rev=process.env.SECTION_REVISION||'s6-r5';
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
function table(s,rows,top=335,height=440,widths=[300,570,570],dense=false){let t=s.tables.add({rows:rows.length,columns:rows[0].length,left:80,top,width:1440,height,values:rows,columnWidths:widths});t.cells.block({row:0,column:0,rowCount:rows.length,columnCount:rows[0].length}).assign({fill:'#FFFFFF',textStyle:{typeface:F,fontSize:dense?26:28,color:C.ink},margins:{top:dense?7:17,left:15,right:15,bottom:dense?6:10},anchor:'top'});t.borders.assign({fill:C.rule,width:1});t.cells.block({row:0,column:0,rowCount:1,columnCount:rows[0].length}).assign({fill:C.navy,textStyle:{typeface:F,fontSize:dense?27:29,bold:true,color:'#FFFFFF'}});}
for(const d of data){const s=p.slides.add();s.background.fill='#FFFFFF';T(s,'06  研究与实验方案',80,28,1440,35,20,false,C.muted);T(s,d.title,80,84,1440,82,47,true,C.navy);rule(s,80,184,1440,C.navy,2);T(s,d.thesis,80,213,1440,90,31,false,C.blue);
switch(d.kind){
case 'flow':case 'timeline':case 'sample':case 'audit':{
 const{step,w}=chain(s,d.nodes,400);d.details.forEach((v,i)=>T(s,v,80+i*step,535,w,145,28));const msgs={1:'例如：比较两种提示方式，需要先统一内容和测验，再说明分配与实施差异。',8:'编号、隐藏分组和解码由谁负责，应写入方案；盲法无法实施时说明原因。',11:'效应、波动与相关性需要材料依据，模型不能凭空补数。',12:'指标与测量质量先核查，再确定排除及缺失处理，保留计划和修订记录。',15:'检查实例：同一试样的重复读数，是否被误算成独立样本？'};rule(s,80,710,1440);T(s,msgs[d.n],80,742,1440,65,29);break;}
case 'proposed-trial':{
 T(s,'第0天：学习前测量',80,350,350,55,29,true,C.blue);const a=N(s,'学生随机1∶1分配',80,470,350,90,'#E7F2EF');
 const b=N(s,'逐步提示\n计划50人',620,335,350,110),c=N(s,'完整解答\n计划50人',620,600,350,110),e=N(s,'一周后无AI新题\n主要结果0—100分',1160,460,360,115,'#E7F2EF');A(s,a,b,'right','left','elbow');A(s,a,c,'right','left','elbow');A(s,b,e,'right','left','elbow');A(s,c,e,'right','left','elbow');
 T(s,'同类内容与时间规则；补充记录当场表现、用时及额外帮助。',80,755,1440,50,29);break;}
case 'sample-power':{
 const raw=(await fs.readFile(path.join(R,'design-packet/r-output/sample-size.csv'),'utf8')).trim().split(/\r?\n/).slice(1).map(v=>v.split(','));
 const c=s.charts.add('bar',{position:{left:80,top:335,width:880,height:425},title:'所需人数（每组，向上取整）',titleTextStyle:{fontSize:27,typeface:F},categories:raw.map(v=>'差'+v[0]+'分'),series:[{name:'每组人数',values:raw.map(v=>Number(v[6])),fill:C.blue,valuesFormatCode:'0',points:[{idx:0,fill:C.blue},{idx:1,fill:C.green},{idx:2,fill:C.muted}]}],hasLegend:false,barOptions:{direction:'column',grouping:'clustered',gapWidth:140},xAxis:{textStyle:{fontSize:25,typeface:F}},yAxis:{min:0,max:120,majorUnit:20,numberFormatCode:'0',textStyle:{fontSize:21,typeface:F},majorGridlines:{fill:C.rule,width:1}},dataLabels:{showValue:true,position:'outEnd',numberFormatCode:'0',textStyle:{fontSize:30,typeface:F}},chartFill:'#FFFFFF',plotAreaFill:'#FFFFFF'});applyPresentationChartFont(c,{fontFamily:F});
 T(s,'差异与波动要有依据',1050,340,470,55,30,true,C.blue);T(s,'标准差描述分数的分散。\n10分和目标差都是教学假设。',1050,410,470,105,28);rule(s,1050,535,470);T(s,'45人/组的适用条件',1050,565,470,55,30,true,C.green);T(s,'只对应本例“差6分”情景。\n改为班级分配需重新计算。',1050,635,470,120,28);T(s,'功效80%：若设定差异存在且前提成立，重复研究中约80%能检出。',80,775,1440,40,24,false,C.blue);break;}
case 'trial':{
 const a=N(s,'班级随机分配',80,470,320,100,'#E7F2EF');const labels=['无生成式AI资源','常规AI答疑\n（Base）','教师预设提示\n（Tutor）'];const out=N(s,'按组条件完成练习',1080,465,440,100);labels.forEach((v,i)=>{let y=330+i*155,b=N(s,v,570,y,350,110);A(s,a,b,'right','left','elbow');A(s,b,out,'right','left','elbow');});const exam=N(s,'统一无资源测验',1080,675,440,85,'#E7F2EF');A(s,out,exam,'bottom','top');T(s,'对照组仍可用课本和笔记',80,720,430,80,28);break;}
case 'mapping':case 'variables':{
 d.nodes.forEach((v,i)=>{let y=340+i*155,a=N(s,v,80,y,440,85),b=N(s,d.details[i],760,y,760,85,i===0?'#E7F2EF':'#F0F5F8');A(s,a,b);});break;}
case 'control':{table(s,d.rows,335,440,[320,560,560]);break;}
case 'blocks':{
 ['第1天','第2天'].forEach((v,i)=>{let y=330+i*245,a=N(s,v,80,y+45,260,85,'#E7F2EF'),q=N(s,'日内随机安排',500,y+45,340,85),b=N(s,'处理A',1110,y,410,75),c=N(s,'处理B',1110,y+115,410,75);A(s,a,q);A(s,q,b,'right','left','elbow');A(s,q,c,'right','left','elbow');});break;}
case 'replicates':{
 const a=N(s,'独立制备',80,490,270,95,'#E7F2EF');['试样1','试样2','试样3'].forEach((v,i)=>{let y=335+i*155,b=N(s,v,570,y,300,85),c=N(s,'读数1    读数2    读数3',1060,y,460,85);A(s,a,b,'right','left','elbow');A(s,b,c);});T(s,'独立试样数：3',80,740,460,55,31,true,C.blue);T(s,'总读数：3 × 3 = 9',1060,740,460,55,31,true,C.red);break;}
case 'factor-table':{table(s,d.rows,318,474,[160,340,340,300,300],true);break;}
case 'interaction':{
 const c=s.charts.add('line',{position:{left:80,top:340,width:860,height:425},title:'固定浓度C=20%时的响应y',titleTextStyle:{fontSize:28,typeface:F},categories:['160°C','180°C'],series:[{name:'催化剂A',values:[60,72],dataLabels:{showValue:false,position:'top'},line:{fill:C.blue,width:3},marker:{symbol:'circle',size:9,fill:C.blue}},{name:'催化剂B',values:[52,83],dataLabels:{showValue:false,position:'bottom'},line:{fill:C.green,width:3},marker:{symbol:'square',size:9,fill:C.green}}],hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:23,typeface:F}},lineOptions:{smooth:false},xAxis:{textStyle:{fontSize:23,typeface:F}},yAxis:{min:0,max:100,majorUnit:20,numberFormatCode:'0',textStyle:{fontSize:22,typeface:F},majorGridlines:{fill:C.rule,width:1}},dataLabels:{showValue:false,position:'top',numberFormatCode:'0',textStyle:{fontSize:27,typeface:F}},chartFill:'#FFFFFF',plotAreaFill:'#FFFFFF'});applyPresentationChartFont(c,{fontFamily:F});T(s,'温度变化的响应增量',1040,340,480,65,31,true,C.blue);T(s,'催化剂A：72 − 60 = 12\n催化剂B：83 − 52 = 31',1040,435,480,120,30);T(s,'增量差：31 − 12 = 19',1040,600,480,65,31,true,C.green);T(s,'无原始重复读数，\n不据此判断统计显著。',1040,690,480,100,29);break;}
case 'resource':{table(s,d.rows,325,480,[300,610,530]);break;}
case 'planb':{
 const a=N(s,d.nodes[0],80,470,430,95),b=N(s,d.nodes[1],740,335,400,85,'#F8EDE9'),c=N(s,d.nodes[2],1220,320,300,130),e=N(s,d.nodes[3],740,625,400,85,'#F8EDE9'),f=N(s,d.nodes[4],1220,610,300,130);A(s,a,b,'right','left','elbow');A(s,a,e,'right','left','elbow');A(s,b,c);A(s,e,f);break;}
case 'finish':{
 d.nodes.forEach((v,i)=>{let y=330+i*114,a=N(s,v,80,y,500,78,i===3?'#E7F2EF':'#F0F5F8');if(i)A(s,s._prev,a,'bottom','top');s._prev=a;T(s,d.details[i],790,y+8,730,85,30);});break;}
}
T(s,d.bottom,80,824,1440,43,22,false,C.green);T(s,'来源：'+d.refs.map(k=>refs[k].short).join('；'),80,875,1340,22,15,false,C.muted);T(s,String(d.n).padStart(2,'0'),1450,864,70,34,23,false,C.muted);s.speakerNotes.text=d.notes+'\n\n'+d.refs.map(k=>refs[k].title+'\n'+refs[k].url+'\n定位：'+refs[k].location).join('\n\n');}
const candidate=path.join(stage,'candidate.pptx');await(await PresentationFile.exportPptx(p)).save(candidate);
await finalizePresentation({workspaceDir:R,candidatePath:candidate,finalPath:path.join(R,'output',`高校科研AI课程_Section6_研究与实验方案_${rev}.pptx`),pythonExecutable:PY,integrityValidatorPath:path.join(S,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(S,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-heading-fit',...['5','9','13'].flatMap(x=>['--require-native-table-slide',x])],fontPolicy:{basis:'design',families:[F]},explicitTotalSlideCount:16,requiredNativeTableOwnerSlides:[5,9,13],requiredNativeChartOwnerSlides:[10,11],materializeLiteralChartWorkbooks:true,verifyArtifactToolImport:true,receiptPath:path.join(stage,'validation.json')});console.log('FINAL',rev,'16 slides');
