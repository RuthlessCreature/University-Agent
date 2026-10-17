import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const R=path.dirname(fileURLToPath(import.meta.url)),rev=process.env.SECTION_REVISION||'s2-r2';
const SKILL='C:/Users/Georgij Xe/.codex/plugins/cache/openai-primary-runtime/presentations/26.1015.12040/skills/presentations';
const PY='C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const data=JSON.parse(await fs.readFile(path.join(R,'lesson.json'),'utf8')),refs=JSON.parse(await fs.readFile(path.join(R,'sources.json'),'utf8'));
const stage=path.join(R,'.build',rev);await fs.mkdir(stage,{recursive:true});await fs.mkdir(path.join(R,'output'),{recursive:true});
const p=Presentation.create({slideSize:{width:1600,height:900}}),F='Microsoft YaHei';p.theme.defaultFont=F;
const C={navy:'#132F43',ink:'#263D4A',blue:'#245B77',muted:'#627681',green:'#2C6D68',rule:'#CAD6DC'};
function text(s,v,x,y,w,h,size=30,bold=false,color=C.ink){const t=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});t.text=v;t.text.style={typeface:F,fontSize:size,bold,color,autoFit:'none',wrap:'word',insets:0,verticalAlignment:'top'};return t;}
function rule(s,x,y,w,color=C.rule,width=1){s.shapes.add({geometry:'line',position:{left:x,top:y,width:w,height:0},line:{fill:color,width}});}
function node(s,v,x,y,w,h){const t=s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill:'#FFFFFF',line:{fill:C.blue,width:1.5}});t.text=v;t.text.style={typeface:F,fontSize:31,bold:true,color:C.navy,autoFit:'none',wrap:'word',insets:12,verticalAlignment:'middle'};return t;}
function arrow(s,a,b,fromSide='right',toSide='left',kind='straight'){s.shapes.connect(a,b,{kind,fromSide,toSide,line:{fill:C.blue,width:2},tail:{type:'arrow',width:'med',length:'med'}});}
function table(s,rows){const widths=[260,590,590];const t=s.tables.add({rows:rows.length,columns:3,left:80,top:320,width:1440,height:450,values:rows,columnWidths:widths});t.cells.block({row:0,column:0,rowCount:rows.length,columnCount:3}).assign({fill:'#FFFFFF',textStyle:{typeface:F,fontSize:27,color:C.ink},margins:{top:16,left:16,right:16,bottom:12},anchor:'top'});t.borders.assign({fill:C.rule,width:1});t.cells.block({row:0,column:0,rowCount:1,columnCount:3}).assign({fill:C.navy,textStyle:{typeface:F,fontSize:28,bold:true,color:'#FFFFFF'}});}
for(const d of data){const s=p.slides.add();s.background.fill='#FFFFFF';text(s,'02  Agentic AI、AI Agent 与科研工作流',80,28,1400,32,20,false,C.muted);text(s,d.title,80,84,1440,82,47,true,C.navy);rule(s,80,184,1440,C.navy,2);text(s,d.thesis,80,213,1440,85,31,false,C.blue);
 if(d.kind==='compare')table(s,d.rows);
 else if(d.kind==='rows'){
  const xs=[80,430,1010],ws=[305,530,510];d.heads.forEach((v,i)=>text(s,v,xs[i],322,ws[i],43,28,true,C.blue));
  d.rows.forEach((r,i)=>{const y=390+i*96;r.forEach((v,j)=>text(s,v,xs[j],y,ws[j],80,j===0?30:28,j===0));if(i<3)rule(s,80,y+83,1440);});
 }else if(d.kind==='layers'){
  d.rows.forEach((r,i)=>{const y=324+i*114;text(s,r[0],80,y,335,75,32,true,C.blue);text(s,r[1],450,y,1070,47,30,true);text(s,r[2],450,y+52,1070,54,27,false,C.muted);if(i<3)rule(s,80,y+100,1440);});
 }else if(d.kind==='skill'){
  d.rows.forEach((r,i)=>{const y=330+i*104;text(s,r[0],80,y,220,48,31,true,C.blue);text(s,r[1],330,y,610,82,28);if(i<3)rule(s,80,y+86,860);});
  text(s,'文献核验 Skill 的课程示例',1050,330,470,78,30,true,C.blue);
  const ex=[['输入','参考文献列表及已有 DOI'],['过程','查出版记录，逐项比对'],['输出','已核实、存在差异、\n尚未核实的记录']];
  ex.forEach((r,i)=>{text(s,r[0],1050,433+i*100,470,40,27,true);text(s,r[1],1050,472+i*100,470,80,27);});
 }else{
  const n=d.nodes.length,step=n===4?380:510,w=n===4?300:420;
  const nodes=d.nodes.map((v,i)=>node(s,v,80+i*step,326,w,78));for(let i=0;i<n-1;i++)arrow(s,nodes[i],nodes[i+1]);
  d.details.forEach((v,i)=>text(s,v,80+i*step,423,w,88,27,false,C.muted));
  if(d.kind==='loop'){
   const joint=(x,y)=>s.shapes.add({geometry:'rect',position:{left:x,top:y,width:1,height:1},fill:'none',line:{fill:'none',width:0}});
   const a=joint(1540,365),b=joint(1540,527),c=joint(420,527),e=joint(420,365);
   const segment=(u,v,fromSide='right',toSide='left')=>s.shapes.connect(u,v,{kind:'straight',fromSide,toSide,line:{fill:C.green,width:1.5}});
   segment(nodes[3],a);segment(a,b,'bottom','top');segment(b,c,'left','right');segment(c,e,'top','bottom');arrow(s,e,nodes[1]);
   text(s,'反馈用于选择下一步；完成或受阻时停止',465,541,1030,40,25,false,C.green);
  }
  const start=d.kind==='loop'?598:555;d.rows.forEach((r,i)=>{const y=start+i*66;text(s,r[0],80,y,300,55,29,true,C.blue);text(s,r[1],430,y,1090,61,28);});
 }
 text(s,d.bottom,80,812,1440,52,23,false,C.green);text(s,'来源：'+d.refs.map(k=>refs[k].short).join('；'),80,872,1340,24,16,false,C.muted);text(s,String(d.n).padStart(2,'0'),1455,861,65,34,23,false,C.muted);
 s.speakerNotes.text=d.notes+'\n\n'+d.refs.map(k=>`${refs[k].title}\n${refs[k].url}\n定位：${refs[k].location}`).join('\n\n');
}
const candidate=path.join(stage,'candidate.pptx');await(await PresentationFile.exportPptx(p)).save(candidate);
const tables=data.filter(d=>d.kind==='compare').map(d=>d.n);
await finalizePresentation({workspaceDir:R,candidatePath:candidate,finalPath:path.join(R,'output',`高校科研AI课程_Section2_Agent与工作流_${rev}.pptx`),pythonExecutable:PY,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-heading-fit',...tables.flatMap(n=>['--require-native-table-slide',String(n)])],fontPolicy:{basis:'design',families:[F]},explicitTotalSlideCount:18,requiredNativeTableOwnerSlides:tables,verifyArtifactToolImport:true,receiptPath:path.join(stage,'validation.json')});
console.log('FINAL',rev,'18 slides');
