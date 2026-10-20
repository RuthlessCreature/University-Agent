import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const R=path.dirname(fileURLToPath(import.meta.url));
const SKILL='C:/Users/Georgij Xe/.codex/plugins/cache/openai-primary-runtime/presentations/26.1015.12040/skills/presentations';
const PY='C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const revision=process.env.LESSON_REVISION||'r1';
const stage=path.join(R,'.build',revision),out=path.join(R,'output',`高校科研教学样课_研究设计_${revision}.pptx`);
await fs.mkdir(stage,{recursive:true});await fs.mkdir(path.dirname(out),{recursive:true});
const data=JSON.parse(await fs.readFile(path.join(R,'lesson.json'),'utf8'));
const p=Presentation.create({slideSize:{width:1600,height:900}}),F='Microsoft YaHei';
p.theme.defaultFont=F;
const C={ink:'#162B3A',red:'#8D3538',blue:'#216C7A',muted:'#617079',rule:'#D8D9D5',paper:'#FAFAF7',pale:'#EDF2F2'};
function txt(s,v,x,y,w,h,size=32,bold=false,color=C.ink){
 const t=s.shapes.add({geometry:'textbox',name:String(v).slice(0,30),position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});t.text=v;
 t.text.style={typeface:F,fontSize:size,bold,color,wrap:'word',autoFit:'none',verticalAlignment:'top',insets:0};return t;
}
function line(s,x,y,w,color=C.rule){s.shapes.add({geometry:'line',position:{left:x,top:y,width:w,height:0},fill:'none',line:{fill:color,width:1}});}
async function img(s,name,x,y,w,h,alt){let b=await fs.readFile(path.join(R,name));return s.images.add({blob:b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),contentType:'image/png',fit:'contain',alt,position:{left:x,top:y,width:w,height:h}});}
function arrow(s,x,y,w,h=0){s.shapes.add({geometry:'connector',kind:'straight',position:{left:x,top:y,width:w,height:h},line:{fill:C.blue,width:2},tail:{type:'arrow'}});}
function node(s,a,x,y,w,h){const z=s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill:'#FFFFFF',line:{fill:C.ink,width:1.3}});txt(s,a,x+20,y+18,w-40,h-24,29,true);return z;}
function page(s,d){
 s.background.fill=C.paper;
 txt(s,d.title,80,58,1420,87,50,true);
 line(s,80,166,1440,C.ink);
 const foot=d.number===2?'来源：2026 年度国家自然科学基金项目指南，申请规定第 16 页':d.number===3?'来源：国家自然科学基金委《关注！！！2026 年申请书改版》，2025-12-30':d.number===5?'van de Schoot et al. (2021), Fig. 1. DOI: 10.1038/s42256-020-00287-7. CC BY 4.0':d.number===11?'方法依据：van de Schoot et al. (2021)。研究问题与方案为课堂示例，尚未实验或完成查新。':'课堂研究设计案例，无实测结果';
 txt(s,foot,80,841,1355,32,19,false,C.muted);txt(s,String(d.number).padStart(2,'0'),1460,837,60,36,23,false,C.muted);
 s.speakerNotes.text=`本页讲解预算：${d.minutes}分钟，含讨论。\n${d.notes}\n材料属性：${d.material}\n来源：\n${d.sources.join('\n')||'本课程编写的教学情境、方法推演与算例。无真实实验结果。'}\n本课程含AI辅助编写，待讲师审阅。`;
}
for(const d of data){const s=p.slides.add();page(s,d);
 if(d.kind==='opening'){
  // A teaching opening, without an agenda grid or a decorative cover image.
  txt(s,d.lead,80,255,1430,225,70,true);
  txt(s,d.context,85,583,1400,120,33,false,C.muted);
  txt(s,'基金申报中的研究论证与 AI 辅助核查',85,753,1400,48,30,false,C.red);
 }else if(d.kind==='policy'){
  await img(s,'assets/nsfc-ai-paragraph.png',82,205,1435,275,'2026 NSFC application rules printed page 16, section 4.2 item 8, unchanged paragraph crop');
  for(let i=0;i<3;i++){let y=515+i*96;txt(s,d.sections[i][0],85,y,290,64,28,true,C.red);txt(s,d.sections[i][1],400,y,1110,80,29);}
 }else if(d.kind==='structure'){
  for(let i=0;i<3;i++){const r=d.rows[i],y=220+i*173;txt(s,r[0],80,y,85,75,44,false,C.red);txt(s,r[1],195,y,255,60,37,true);txt(s,r[2],500,y,440,105,31);txt(s,r[3].replace('案例落点：',''),1000,y,510,120,28,false,C.muted);if(i<2)line(s,195,y+142,1320);}
  txt(s,d.caption,195,759,1315,65,26,false,C.red);
 }else if(d.kind==='annotation'){
  txt(s,'原稿',80,216,110,45,27,true,C.muted);
  const t=txt(s,d.bad,80,280,915,205,40);
  t.text=[{run:'本项目拟构建智能文献筛选系统，'},{run:'①显著提升筛选效率，',style:{color:C.red,underline:'sng'}},{run:'②保证筛选准确性，',style:{color:C.red,underline:'sng'}},{run:'③形成可推广的方法，',style:{color:C.red,underline:'sng'}},{run:'④为科研工作提供有力支撑。',style:{color:C.red,underline:'sng'}}];
  for(let i=0;i<4;i++){const y=216+i*119;txt(s,d.comments[i][0],1080,y,435,38,27,true,C.red);txt(s,d.comments[i][1],1080,y+43,435,70,27);}
  line(s,80,720,1440);txt(s,d.revision,80,745,1440,83,29);
 }else if(d.kind==='paper'){
  txt(s,'人工判读与标签反馈（原图局部）',80,213,850,42,27,false,C.muted);
  await img(s,'assets/asreview-cycle.png',80,270,850,545,'Cropped active learning cycle from Figure 1, van de Schoot et al. 2021. CC BY4.0. Original labels unchanged; crop disclosed.');
  for(let i=0;i<3;i++){let y=220+i*200;txt(s,d.points[i][0],1000,y,520,48,31,true,i===2?C.red:C.ink);txt(s,d.points[i][1],1000,y+61,520,132,28);}
 }else if(d.kind==='design'){
  txt(s,d.lead,80,210,1440,80,31);
  node(s,'同一文献集合\n独立参考标签',80,350,330,130);
  node(s,d.baseline,540,300,940,106);node(s,d.treatment,540,455,940,106);
  arrow(s,425,370,95);arrow(s,425,470,95);
  txt(s,d.outcome,80,612,1440,65,34,true,C.red);
  txt(s,d.safeguards.map((x,i)=>`${i+1}. ${x}`).join('\n'),80,702,1440,120,28);
 }else if(d.kind==='measures'){
  const rows=[['评价问题','怎样观测','解释所需条件'],...d.rows];
  const t=s.tables.add({rows:5,columns:3,left:80,top:225,width:1440,height:450,values:rows,columnWidths:[265,600,575]});
  t.cells.block({row:0,column:0,rowCount:5,columnCount:3}).assign({fill:C.paper,textStyle:{typeface:F,fontSize:28,color:C.ink},margins:{top:14,bottom:12,left:18,right:18},anchor:'top'});
  t.borders.assign({fill:C.rule,width:1});
  t.cells.block({row:0,column:0,rowCount:1,columnCount:3}).assign({fill:C.pale,textStyle:{typeface:F,fontSize:28,bold:true,color:C.ink}});
  txt(s,d.caption,85,727,1425,85,31,false,C.red);
 }else if(d.kind==='arithmetic'){
  txt(s,d.scenario,80,205,1435,86,32);
  s.charts.add('bar',{position:{left:65,top:330,width:870,height:355},categories:['已筛选 300 条','未筛选 700 条'],series:[{name:'相关',values:[95,5],fill:C.red,dataLabels:{showValue:false,showCategoryName:false,showSeriesName:false}},{name:'不相关',values:[205,695],fill:'#B9C7CC'}],barOptions:{direction:'bar',grouping:'stacked',gapWidth:80},hasLegend:true,legend:{position:'bottom',textStyle:{typeface:F,fontSize:24}},xAxis:{textStyle:{typeface:F,fontSize:23}},yAxis:{title:{text:'记录数',textStyle:{typeface:F,fontSize:24}},min:0,max:750,textStyle:{typeface:F,fontSize:25},majorGridlines:{fill:'#E2E6E5',width:1}},dataLabels:{showValue:true,showCategoryName:false,showSeriesName:false,position:'center',textStyle:{typeface:F,fontSize:22}},chartFill:C.paper});
  for(let i=0;i<4;i++){let y=325+i*94;txt(s,d.metrics[i][0],1010,y,505,38,25,false,C.muted);txt(s,d.metrics[i][1],1010,y+37,505,53,34,true,i===0?C.red:C.ink);}
  txt(s,'相关记录：已筛 95 条，未筛 5 条（教学设定）',85,700,850,43,24,false,C.muted);
  txt(s,d.caption,80,755,1435,72,29,false,C.red);
 }else if(d.kind==='stopping'){
  txt(s,d.lefttitle,80,230,675,55,36,true);txt(s,d.left,80,322,650,330,34);
  txt(s,d.righttitle,860,230,660,55,36,true,C.red);txt(s,d.right,860,322,650,330,34);
  line(s,80,705,1440);txt(s,d.question,80,744,1440,82,32,true,C.red);
 }else if(d.kind==='route'){
  const xs=[80,590,1100];
  for(let i=0;i<3;i++){const x=xs[i],r=d.phases[i];txt(s,String(i+1).padStart(2,'0'),x,225,90,65,46,false,C.red);txt(s,r[0],x,315,420,55,36,true);txt(s,r[1],x,411,420,116,31);txt(s,r[2],x,566,420,100,28,false,C.blue);if(i<2)arrow(s,x+430,340,65);}
  line(s,80,699,1440);txt(s,d.human,80,735,1435,45,29,true);txt(s,d.machine,80,785,1435,42,28,false,C.muted);
 }else if(d.kind==='argument'){
  for(let i=0;i<3;i++){let y=225+i*164;txt(s,d.paragraphs[i][0],80,y,260,55,32,true,i===2?C.red:C.blue);txt(s,d.paragraphs[i][1],385,y,1125,115,34);if(i<2)line(s,385,y+138,1125);}
  txt(s,d.caption,80,760,1440,68,27,false,C.red);
 }else if(d.kind==='worksheet'){
  await img(s,'word-render/page-1.png',75,205,550,620,'Actual rendered Word research design worksheet, teaching example, not a grant application or Agent execution screenshot');
  for(let i=0;i<4;i++){let y=228+i*122;txt(s,d.checks[i][0],730,y,780,45,32,true);txt(s,d.checks[i][1],730,y+51,780,70,30);}
  txt(s,d.exercise,730,742,780,87,30,false,C.red);
 }
 console.log('AUTHORED',d.number,d.kind);
}
await (await PresentationFile.exportPptx(p)).save(path.join(stage,'candidate.pptx'));
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
await finalizePresentation({workspaceDir:R,candidatePath:path.join(stage,'candidate.pptx'),finalPath:out,pythonExecutable:PY,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-heading-fit','--require-native-table-slide','7'],fontPolicy:{basis:'design',families:[F]},verifyArtifactToolImport:true,explicitTotalSlideCount:12,requiredNativeChartOwnerSlides:[8],nativeChartTargetApplication:'portable',materializeLiteralChartWorkbooks:true,requiredNativeTableOwnerSlides:[7],receiptPath:path.join(stage,'validation.json')});
console.log('FINAL',out);
