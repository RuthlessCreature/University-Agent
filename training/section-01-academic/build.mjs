import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const R=path.dirname(fileURLToPath(import.meta.url)),rev=process.env.SECTION_REVISION||'a4';
const SKILL='C:/Users/Georgij Xe/.codex/plugins/cache/openai-primary-runtime/presentations/26.1015.12040/skills/presentations';
const PY='C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const data=JSON.parse(await fs.readFile(path.join(R,'lesson.json'),'utf8')),refs=JSON.parse(await fs.readFile(path.join(R,'sources.json'),'utf8'));
const stage=path.join(R,'.build',rev);await fs.mkdir(stage,{recursive:true});await fs.mkdir(path.join(R,'output'),{recursive:true});
const p=Presentation.create({slideSize:{width:1600,height:900}}),F='Microsoft YaHei';p.theme.defaultFont=F;
const C={navy:'#132F43',ink:'#263D4A',blue:'#245B77',muted:'#627681',red:'#963F3C',green:'#2C6D68',rule:'#CAD6DC',light:'#F1F5F7'};
const shortRefs={ijs:'IJS / SLAIF（2026）',gwu:'GWU MAE-6291（2026）',nist:'NIST AI 600-1（2024）',concepts:'OpenAI：Key concepts',context:'OpenAI：Conversation state',prompt:'OpenAI：Prompt engineering',optimization:'OpenAI：Model optimization',tools:'OpenAI：Using tools',walters:'Walters & Wilder（2023），表3、4',nature:'Nature Portfolio AI policy',plos:'PLOS AI policy',elicit:'Elicit',consensus:'Consensus',connected:'Connected Papers'};
function text(s,v,x,y,w,h,size=31,bold=false,color=C.ink){const t=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});t.text=v;t.text.style={typeface:F,fontSize:size,bold,color,autoFit:'none',wrap:'word',insets:0,verticalAlignment:'top'};return t;}
function rule(s,x,y,w,color=C.rule,width=1){return s.shapes.add({geometry:'line',position:{left:x,top:y,width:w,height:0},line:{fill:color,width}});}
function node(s,v,x,y,w,h,size=30){const t=s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill:'#FFFFFF',line:{fill:C.blue,width:1.5}});t.text=v;t.text.style={typeface:F,fontSize:size,bold:true,color:C.navy,autoFit:'none',wrap:'word',insets:12,verticalAlignment:'middle'};return t;}
function connect(s,a,b){s.shapes.connect(a,b,{kind:'straight',fromSide:'right',toSide:'left',line:{fill:C.blue,width:2},tail:{type:'arrow',width:'med',length:'med'}});}
function table(s,rows,widths,y,h,size=28){const t=s.tables.add({rows:rows.length,columns:widths.length,left:80,top:y,width:1440,height:h,values:rows,columnWidths:widths});t.cells.block({row:0,column:0,rowCount:rows.length,columnCount:widths.length}).assign({fill:'#FFFFFF',textStyle:{typeface:F,fontSize:size,color:C.ink},margins:{top:17,left:18,right:18,bottom:13},anchor:'top'});t.borders.assign({fill:C.rule,width:1});t.cells.block({row:0,column:0,rowCount:1,columnCount:widths.length}).assign({fill:C.navy,textStyle:{typeface:F,fontSize:size,bold:true,color:'#FFFFFF'}});return t;}
for(const d of data){
 const s=p.slides.add();s.background.fill='#FFFFFF';text(s,'01  科研 AI：能力、原理与学术边界',80,28,1360,32,20,false,C.muted);text(s,d.title,80,84,1440,82,49,true,C.navy);rule(s,80,184,1440,C.navy,2);
 if(d.thesis)text(s,d.thesis,80,213,1440,85,32,false,C.blue);
 switch(d.kind){
 case 'research-map':{
  text(s,'科研环节',80,317,280,45,28,true);text(s,'AI 可以辅助的工作',450,317,540,45,28,true);text(s,'需要保留的学术判断',1050,317,470,45,28,true);
  for(let i=0;i<5;i++){const y=390+i*76; text(s,d.stages[i][0],80,y,280,48,31,true);text(s,d.stages[i][1],450,y,540,48,30);text(s,d.stages[i][2],1050,y,470,48,30,false,C.green);if(i<4)rule(s,80,y+57,1440);}
  break;}
 case 'scope':{
  const a=node(s,'面向科学研究的 AI 方法与系统',80,319,1440,70,34);const b=node(s,d.domains[0][0],80,444,660,70,33);const c=node(s,d.domains[1][0],860,444,660,70,33);
  s.shapes.connect(a,b,{kind:'elbow',fromSide:'bottom',toSide:'top',line:{fill:C.blue,width:1.5},tail:{type:'arrow',width:'med',length:'med'}});s.shapes.connect(a,c,{kind:'elbow',fromSide:'bottom',toSide:'top',line:{fill:C.blue,width:1.5},tail:{type:'arrow',width:'med',length:'med'}});
  for(let i=0;i<2;i++){const x=80+i*780;text(s,d.domains[i][1],x,539,660,45,30,true);text(s,d.domains[i][2],x,601,660,100,29);}
  text(s,d.layers,80,718,1440,76,28);break;}
 case 'learning':{
  const nodes=d.stages.map((a,i)=>node(s,a[0],80+i*510,330,420,77,36));connect(s,nodes[0],nodes[1]);connect(s,nodes[1],nodes[2]);
  for(let i=0;i<3;i++){const x=80+i*510;text(s,d.stages[i][1],x,445,420,107,32,true);text(s,d.stages[i][2],x,580,420,132,29);}
  text(s,d.distinction,80,731,1440,74,28,false,C.green);break;}
 case 'context':{
  const nodes=d.nodes.map((a,i)=>node(s,a[0],80+i*380,330,300,77,30));for(let i=0;i<3;i++)connect(s,nodes[i],nodes[i+1]);
  for(let i=0;i<4;i++)text(s,d.nodes[i][1],80+i*380,432,300,80,26,false,C.muted);
  for(let i=0;i<3;i++){const y=540+i*77;text(s,d.points[i][0],80,y,350,69,29,true);text(s,d.points[i][1],470,y,1050,74,28);}break;}
 case 'citation-chart':{
  text(s,d.study,80,309,1440,86,30);
  const ch=s.charts.add('bar',{position:{left:80,top:420,width:780,height:338},title:d.chart.metric,titleTextStyle:{fontSize:27,typeface:F},categories:d.chart.categories,series:[{name:'虚构文献比例',values:d.chart.values,fill:C.blue,valuesFormatCode:'0%',points:[{idx:0,fill:C.blue},{idx:1,fill:C.green}]}],hasLegend:false,barOptions:{direction:'column',grouping:'clustered',gapWidth:170},xAxis:{textStyle:{fontSize:23,typeface:F}},yAxis:{min:0,max:1,majorUnit:0.2,numberFormatCode:'0%',textStyle:{fontSize:21,typeface:F},majorGridlines:{fill:C.rule,width:1}},dataLabels:{showValue:true,position:'outEnd',numberFormatCode:'0%',textStyle:{fontSize:28,typeface:F}},chartFill:'#FFFFFF',plotAreaFill:'#FFFFFF'});applyPresentationChartFont(ch,{fontFamily:F});
  for(let i=0;i<3;i++){let y=422+i*112;text(s,d.points[i][0],940,y,580,40,28,true,C.blue);text(s,d.points[i][1],940,y+45,580,90,26);}break;}
 case 'capabilities':table(s,d.rows,[240,575,625],225,425,29);text(s,d.argument,80,690,1440,101,31);break;
 case 'decomposition':{
  for(let i=0;i<5;i++){let y=321+i*87;text(s,String(i+1).padStart(2,'0'),80,y,80,55,35,false,C.red);text(s,d.rows[i][0],190,y,230,55,32,true);text(s,d.rows[i][1],470,y,525,65,29);text(s,d.rows[i][2],1050,y,470,65,29,false,C.green);if(i<4)rule(s,190,y+66,1330);}break;}
 case 'prompt-structure':{
  text(s,d.lead,80,215,1440,78,32,false,C.blue);text(s,d.example,80,340,1000,412,31);
  for(let i=0;i<4;i++){let y=338+i*104;text(s,d.labels[i][0],1180,y,340,43,29,true,C.blue);text(s,d.labels[i][1],1180,y+47,340,58,26);}break;}
 case 'tool-map':table(s,d.rows,[295,615,530],228,420,28);text(s,d.selection,80,697,1440,105,30);break;
 case 'inference':{
  for(let i=0;i<3;i++){let y=325+i*128;text(s,d.levels[i][0],80,y,240,55,39,true,C.blue);text(s,d.levels[i][1],370,y,1150,45,32,true);text(s,d.levels[i][2],370,y+51,1150,70,28);if(i<2)rule(s,80,y+120,1440);}
  text(s,d.example,80,733,1440,76,28,false,C.green);break;}
 case 'policy':text(s,d.lead,80,215,1440,75,32,false,C.blue);table(s,d.rows,[290,555,595],325,337,28);text(s,d.record,80,709,1440,98,29);break;
 case 'credibility':{
  for(let i=0;i<4;i++){let y=327+i*111;text(s,d.conditions[i][0],80,y,280,52,34,true,C.blue);text(s,d.conditions[i][1],430,y,1090,49,32,true);text(s,d.conditions[i][2],430,y+55,1090,50,28,false,C.muted);if(i<3)rule(s,80,y+93,1440);}break;}
 }
 const footerY=['scope','learning','inference','tool-map','policy'].includes(d.kind)?818:802;
 text(s,d.bottom,80,footerY,1440,47,24,false,C.green);
 const credit=d.refs.map(k=>shortRefs[k]).join('；');text(s,'来源：'+credit,80,871,1310,25,16,false,C.muted);text(s,String(d.n).padStart(2,'0'),1440,862,80,34,23,false,C.muted);
 s.speakerNotes.text=d.notes+'\n\n'+d.refs.map(k=>`${refs[k].title}\n${refs[k].url}\n定位：${refs[k].location}`).join('\n\n');
}
const candidate=path.join(stage,'candidate.pptx');await (await PresentationFile.exportPptx(p)).save(candidate);
const tableOwners=[6,9,11];
await finalizePresentation({workspaceDir:R,candidatePath:candidate,finalPath:path.join(R,'output',`高校科研AI课程_Section1_学术讲授版_${rev}.pptx`),pythonExecutable:PY,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-heading-fit',...tableOwners.flatMap(n=>['--require-native-table-slide',String(n)])],fontPolicy:{basis:'design',families:[F]},explicitTotalSlideCount:12,requiredNativeTableOwnerSlides:tableOwners,requiredNativeChartOwnerSlides:[5],materializeLiteralChartWorkbooks:true,verifyArtifactToolImport:true,receiptPath:path.join(stage,'validation.json')});
console.log('FINAL',rev,'12 slides');
