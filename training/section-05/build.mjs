import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const R=path.dirname(fileURLToPath(import.meta.url)),rev=process.env.SECTION_REVISION||'s5-r3';
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
async function pic(s,name){const b=await fs.readFile(path.join(R,'assets',name));s.images.add({blob:b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),contentType:'image/png',alt:'公开网页真实截图：'+name,fit:'contain',position:{left:80,top:310,width:960,height:490}});}
function table(s,rows,top=335,height=440,widths=[300,650,490]){let t=s.tables.add({rows:rows.length,columns:rows[0].length,left:80,top,width:1440,height,values:rows,columnWidths:widths});t.cells.block({row:0,column:0,rowCount:rows.length,columnCount:rows[0].length}).assign({fill:'#FFFFFF',textStyle:{typeface:F,fontSize:27,color:C.ink},margins:{top:17,left:15,right:15,bottom:10},anchor:'top'});t.borders.assign({fill:C.rule,width:1});t.cells.block({row:0,column:0,rowCount:1,columnCount:rows[0].length}).assign({fill:C.navy,textStyle:{typeface:F,fontSize:28,bold:true,color:'#FFFFFF'}});}
for(const d of data){const s=p.slides.add();s.background.fill='#FFFFFF';T(s,'05  文献检索、阅读与综述',80,28,1440,35,20,false,C.muted);T(s,d.title,80,84,1440,82,47,true,C.navy);rule(s,80,184,1440,C.navy,2);T(s,d.thesis,80,213,1440,90,31,false,C.blue);
switch(d.kind){
case 'flow':case 'record':{
 const{step,w}=chain(s,d.nodes,400);d.details.forEach((v,i)=>T(s,v,80+i*step,535,w,140,29));
 const more={1:'研究者需要能解释：为什么选这些研究，哪些判断来自原文，哪些仍是推断。',6:'记录实例：原始查询、网页实录与候选材料可以相互对应；预设查询另标待试查。',10:'核对顺序：先看引用了哪篇，再看原文是否包含该判断，最后检查条件有没有被省略。',15:'阅读笔记中把原文事实和自己的解释分开，避免写综述时找不到依据。',21:'引文真实性与主张支持分别检查，不能用DOI可解析代替原文核查。'};rule(s,80,710,1440);T(s,more[d.n]||'',80,742,1440,65,29);break;}
case 'rows':{table(s,[['类别','主要内容','需要检查'],...d.rows]);break;}
case 'concept':{
 d.nodes.forEach((v,i)=>{let y=340+i*155,a=N(s,v,80,y,450,85),b=N(s,d.details[i],750,y,770,85);A(s,a,b);});break;}
case 'query':{
 T(s,d.query,80,330,1440,180,35,true,C.navy);const{step,w}=chain(s,d.nodes,590);d.details.forEach((v,i)=>T(s,v,80+i*step,715,w,70,29,true,C.blue));break;}
case 'screenshot':{await pic(s,d.image);d.labels.forEach((v,i)=>{T(s,String(i+1).padStart(2,'0'),1110,335+i*145,80,50,32,true,C.blue);T(s,v,1110,390+i*145,410,100,28);});break;}
case 'network':{
 const a=N(s,'种子论文',80,475,330,95,'#E7F2EF'),b=N(s,'论文甲',650,335,330,75),c=N(s,'论文乙',650,630,330,75),e=N(s,'论文丙',1190,475,330,75);for(const [u,v] of [[a,b],[a,c],[b,e],[c,e]])s.shapes.connect(u,v,{kind:'straight',fromSide:'right',toSide:'left',line:{fill:C.blue,width:2}});T(s,'相似关系',80,675,460,55,30,true,C.blue);T(s,'邻近表示关联线索，\n不能据此判定互相引用。',80,735,540,75,28);T(s,'实际引用另核',1130,675,390,50,30,true,C.red);T(s,'参考文献和被引记录\n用于查明引用方向。',1060,735,460,75,28);break;}
case 'branch':{
 const a=N(s,d.nodes[0],80,500,420,95,'#E7F2EF');d.nodes.slice(1).forEach((v,i)=>{let y=330+i*153,b=N(s,v,770,y,750,80);A(s,a,b,'right','left','elbow');T(s,d.details[i+1],770,y+94,750,50,26);});T(s,d.details[0],80,635,420,100,29);break;}
case 'decision':{
 let a=N(s,d.nodes[0],80,465,440,100),b=N(s,d.nodes[1],740,335,400,85,'#E7F2EF'),c=N(s,d.nodes[2],1200,335,320,115),e=N(s,d.nodes[3],740,625,400,85,'#F8EDE9'),f=N(s,d.nodes[4],1200,610,320,115);A(s,a,b,'right','left','elbow');A(s,a,e,'right','left','elbow');A(s,b,c);A(s,e,f);break;}
case 'screen':{
 const ns=d.nodes.map((v,i)=>N(s,v,80+i*380,360,300,90,i===3?'#E7F2EF':'#F0F5F8'));for(let i=0;i<3;i++)A(s,ns[i],ns[i+1]);d.details.forEach((v,i)=>T(s,v,80+i*380,490,300,100,28));const a=N(s,'全文缺失／范围不符／信息不清',500,690,690,85,'#F8EDE9');T(s,'分别记录原因和下一步处理',80,720,360,70,27);break;}
case 'extract':{
 d.rows.forEach((r,i)=>{let y=330+i*115;T(s,r[0],80,y,200,55,30,true,C.blue);const a=N(s,r[1],300,y,730,78),b=N(s,r[2],1180,y,340,78);A(s,a,b);});break;}
case 'matrix':{table(s,d.rows,330,450,[300,570,570]);break;}
case 'compare':{
 d.nodes.forEach((v,i)=>{let y=330+i*114,a=N(s,v,80,y,560,78),b=N(s,d.details[i],860,y,660,78,i===1?'#E7F2EF':'#F0F5F8');A(s,a,b);});break;}
case 'prose':{
 T(s,'逐篇列举，信息停留在主题',80,330,1440,50,29,true,C.red);T(s,d.before,80,395,1440,100,31);rule(s,80,525,1440);T(s,'围绕比较条件组织证据',80,555,1440,50,29,true,C.green);T(s,d.after,80,620,1440,180,30);break;}
case 'claim':{
 const a=N(s,d.nodes[0],80,350,380,80),b=N(s,d.nodes[1],610,350,380,80),c=N(s,d.nodes[2],1140,350,380,80,'#E7F2EF');A(s,a,b);A(s,b,c);T(s,d.details[0],80,495,380,130,32,true,C.red);T(s,d.details[1],610,495,380,130,30);T(s,d.details[2],1140,495,380,190,30);T(s,'反证检索：同义表达、前后引文、近期论文和预印本都要考虑。',80,745,1440,60,30);break;}
case 'agent':case 'finish':{
 d.nodes.forEach((v,i)=>{let y=330+i*114,a=N(s,v,80,y,500,78,i===3?'#E7F2EF':'#F0F5F8');if(i)A(s,s._prev,a,'bottom','top');s._prev=a;T(s,d.details[i],790,y+8,730,85,30);});break;}
}
T(s,d.bottom,80,824,1440,43,22,false,C.green);T(s,'来源：'+d.refs.map(k=>refs[k].short).join('；'),80,875,1340,22,15,false,C.muted);T(s,String(d.n).padStart(2,'0'),1450,864,70,34,23,false,C.muted);s.speakerNotes.text=d.notes+'\n\n'+d.refs.map(k=>refs[k].title+'\n'+refs[k].url+'\n定位：'+refs[k].location).join('\n\n');}
const candidate=path.join(stage,'candidate.pptx');await(await PresentationFile.exportPptx(p)).save(candidate);
await finalizePresentation({workspaceDir:R,candidatePath:candidate,finalPath:path.join(R,'output',`高校科研AI课程_Section5_文献检索阅读与综述_${rev}.pptx`),pythonExecutable:PY,integrityValidatorPath:path.join(S,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(S,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-heading-fit',...['2','7','17','19'].flatMap(x=>['--require-native-table-slide',x])],fontPolicy:{basis:'design',families:[F]},explicitTotalSlideCount:24,requiredNativeTableOwnerSlides:[2,7,17,19],requiredNativeChartOwnerSlides:[],verifyArtifactToolImport:true,receiptPath:path.join(stage,'validation.json')});console.log('FINAL',rev,'24 slides');
