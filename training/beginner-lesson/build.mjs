import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const R=path.dirname(fileURLToPath(import.meta.url)),revision=process.env.LESSON_REVISION||'b1';
const SKILL='C:/Users/Georgij Xe/.codex/plugins/cache/openai-primary-runtime/presentations/26.1015.12040/skills/presentations';
const PY='C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const stage=path.join(R,'.build',revision);await fs.mkdir(stage,{recursive:true});await fs.mkdir(path.join(R,'output'),{recursive:true});
const out=path.join(R,'output',`高校科研AI入门样课_读懂一篇论文_${revision}.pptx`);
const data=JSON.parse(await fs.readFile(path.join(R,'lesson.json'),'utf8'));
const p=Presentation.create({slideSize:{width:1600,height:900}}),F='Microsoft YaHei';p.theme.defaultFont=F;
const C={ink:'#182E3D',red:'#9C3734',green:'#24675E',muted:'#65747D',rule:'#D7DDE0'};
function text(s,v,x,y,w,h,size=34,bold=false,color=C.ink){
 const t=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});t.text=v;t.text.style={typeface:F,fontSize:size,bold,color,wrap:'word',autoFit:'none',verticalAlignment:'top',insets:0};return t;
}
function rule(s,x,y,w){s.shapes.add({geometry:'line',position:{left:x,top:y,width:w,height:0},line:{fill:C.rule,width:1}});}
async function image(s,file,x,y,w,h,alt){const b=await fs.readFile(path.join(R,file));s.images.add({blob:b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),contentType:'image/png',fit:'contain',alt,position:{left:x,top:y,width:w,height:h}});}
for(const d of data){const s=p.slides.add();s.background.fill='#FFFFFF';text(s,d.title,80,60,1440,85,49,true);rule(s,80,167,1440);
 const footer=d.sources.length?'来源：Heinrich 等，PLOS ONE（2025），10.1371/journal.pone.0328041':'课堂操作示例，提问与回答未经外部模型实测';
 text(s,footer,80,847,1350,30,19,false,C.muted);text(s,String(d.number).padStart(2,'0'),1465,842,55,37,23,false,C.muted);
 s.speakerNotes.text=d.notes+'\n材料：公开论文与课堂操作示例。\n'+d.sources.join('\n')+'\n本课含AI辅助编写，待讲师审阅。';
 if(d.kind==='opening'){
  text(s,d.question,80,262,1440,215,75,true);text(s,d.body,85,590,1410,155,36);
 }else if(d.kind==='paper'){
  await image(s,'assets/paper-title.png',80,205,1440,290,'Original published paper title and authors from PDF page1; crop only, CC BY4.0');
  text(s,d.translation,80,535,1440,60,35,true);
  const facts=text(s,'',80,631,1440,130,32);
  facts.text=[{run:d.facts[0][0]+'：'+d.facts[0][1]+'\n'+d.facts[1][0]+'：'+d.facts[1][1]+'\n'+d.facts[2][0]+'：'},{run:d.facts[2][1],link:{uri:'https://doi.org/10.1371/journal.pone.0328041',isExternal:true},style:{color:C.green,underline:'sng'}}];
  text(s,d.body,80,790,1440,40,28,false,C.muted);
 }else if(d.kind==='question'){
  text(s,d.vague,80,229,1440,65,35,false,C.muted);text(s,d.precise,80,360,1440,180,55,true);
  text(s,d.body,80,640,1440,145,37);
 }else if(d.kind==='prompt'){
  text(s,d.file,80,214,1440,55,30,false,C.muted);
  text(s,d.prompt,80,310,1440,342,35);
  rule(s,80,701,1440);text(s,d.body,80,735,1440,94,31);
 }else if(d.kind==='method'){
  text(s,d.heading,80,215,1440,50,31,true);text(s,d.meaning,80,276,1440,48,29,false,C.muted);
  for(let i=0;i<4;i++){text(s,String(i+1)+'.',80,374+i*74,80,48,35,false,C.green);text(s,d.materials[i],165,374+i*74,800,52,35);}
  s.shapes.add({geometry:'connector',kind:'straight',position:{left:930,top:480,width:105,height:0},line:{fill:C.green,width:2},tail:{type:'arrow'}});
  text(s,d.result,1110,405,410,195,39,true,C.green);
  text(s,d.body,80,733,1440,96,32);
 }else if(d.kind==='difference'){
  for(let i=0;i<2;i++){const y=225+i*222,r=d.rows[i];text(s,r[0],80,y,560,110,39,true,i?C.green:C.ink);text(s,r[1],720,y,795,95,36);text(s,r[2],720,y+110,795,50,32,false,C.muted);if(i===0)rule(s,80,y+184,1440);}
  text(s,d.body,80,723,1440,106,33);
 }else if(d.kind==='evidence'){
  text(s,d.location,80,220,1440,100,33);
  text(s,d.quote,80,355,1440,100,43,false,C.muted);
  text(s,d.translation,80,485,1440,105,44,true);
  text(s,d.answer,80,630,1440,95,37,true,C.green);
  text(s,d.body,80,772,1440,60,29);
 }else if(d.kind==='correction'){
  text(s,'写过头的句子',80,214,1440,45,28,true,C.red);text(s,d.bad,80,281,1440,100,43,false,C.red);
  text(s,d.error,80,397,1440,100,33);
  text(s,'核对原文后可以这样写',80,533,1440,45,28,true,C.green);text(s,d.good,80,600,1440,130,42,true,C.green);
  text(s,d.body,80,780,1440,50,28,false,C.muted);
 }else if(d.kind==='note'){
  const t=s.tables.add({rows:4,columns:2,left:80,top:227,width:1440,height:460,values:d.rows,columnWidths:[305,1135]});
  t.cells.block({row:0,column:0,rowCount:4,columnCount:2}).assign({fill:'#FFFFFF',textStyle:{typeface:F,fontSize:31,color:C.ink},margins:{top:18,left:20,right:20,bottom:16},anchor:'top'});
  t.borders.assign({fill:C.rule,width:1});t.cells.block({row:0,column:0,rowCount:4,columnCount:1}).assign({fill:'#F0F4F4',textStyle:{typeface:F,fontSize:31,bold:true,color:C.ink}});
  text(s,d.body,80,752,1440,78,33);
 }else if(d.kind==='missing'){
  text(s,d.input,80,220,1440,70,36,true);
  text(s,d.wrong,80,350,1440,135,38,false,C.red);
  text(s,d.good,80,535,1440,165,38,false,C.green);
  text(s,d.body,80,761,1440,70,30);
 }else if(d.kind==='word'){
  await image(s,'word-render/page-1.png',75,205,550,625,'Actual rendered editable Word reading note, not a model execution screenshot');
  text(s,'已保存：论文阅读笔记.docx',730,228,785,100,36,true);
  for(let i=0;i<3;i++)text(s,String(i+1)+'. '+d.checks[i],730,391+i*91,785,77,35);
  text(s,d.body,730,733,785,95,33,false,C.green);
 }else if(d.kind==='practice'){
  for(let i=0;i<4;i++){const y=217+i*143; text(s,String(i+1),80,y,80,60,46,false,C.green);text(s,d.steps[i][0],195,y,1315,55,36,true);text(s,d.steps[i][1],195,y+66,1315,62,31);}
  text(s,'找不到依据时，把“还不能回答”留在笔记里。补齐后再改。',195,800,1310,35,27,false,C.green);
 }
 console.log('PAGE',d.number,d.title);
}
await (await PresentationFile.exportPptx(p)).save(path.join(stage,'candidate.pptx'));
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
await finalizePresentation({workspaceDir:R,candidatePath:path.join(stage,'candidate.pptx'),finalPath:out,pythonExecutable:PY,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-heading-fit','--require-native-table-slide','9'],fontPolicy:{basis:'design',families:[F]},explicitTotalSlideCount:12,requiredNativeTableOwnerSlides:[9],requiredNativeChartOwnerSlides:[],verifyArtifactToolImport:true,receiptPath:path.join(stage,'validation.json')});
console.log('FINAL',out);
