import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const R=path.dirname(fileURLToPath(import.meta.url)),rev=process.env.SECTION_REVISION||'s0-r4';
const SKILL='C:/Users/Georgij Xe/.codex/plugins/cache/openai-primary-runtime/presentations/26.1015.12040/skills/presentations';
const PY='C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const plan=JSON.parse(await fs.readFile(path.join(R,'../curriculum/course_structure_240.json'),'utf8'));
if(plan.sections.reduce((a,x)=>a+x.pages,0)!==240)throw Error('Course page budget must sum to 240');
const stage=path.join(R,'.build',rev);await fs.mkdir(stage,{recursive:true});await fs.mkdir(path.join(R,'output'),{recursive:true});
const p=Presentation.create({slideSize:{width:1600,height:900}}),F='Microsoft YaHei';p.theme.defaultFont=F;
const C={navy:'#142D40',ink:'#203746',muted:'#5F707A',red:'#94423B',green:'#286D66',rule:'#D3DDE1'};
function text(s,v,x,y,w,h,size=34,bold=false,color=C.ink){const t=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});t.text=v;t.text.style={typeface:F,fontSize:size,bold,color,autoFit:'none',wrap:'word',insets:0,verticalAlignment:'top'};return t;}
function rule(s,x,y,w,color=C.rule){s.shapes.add({geometry:'line',position:{left:x,top:y,width:w,height:0},line:{fill:color,width:1}});}
function page(title,n){const s=p.slides.add();s.background.fill='#FFFFFF';text(s,title,80,60,1440,86,51,true);rule(s,80,168,1440);text(s,'课程导入',80,844,1320,30,20,false,C.muted);text(s,'0 / '+String(n).padStart(2,'0'),1420,839,105,36,23,false,C.muted);return s;}
{
 const s=p.slides.add();s.background.fill=C.navy;
 text(s,'高校科研',85,190,1430,140,112,true,'#FFFFFF');
 text(s,'AI 实务',85,340,1430,140,112,true,'#FFFFFF');
 text(s,'文献、数据、论文与项目材料',90,565,1420,80,44,false,'#DDE8ED');
 text(s,'面向高校教师与科研人员',90,745,1350,55,30,false,'#DDE8ED');
 text(s,'SECTION 0',1250,750,270,40,24,false,'#DDE8ED');
 s.speakerNotes.text='以高校教师常见的文献、数据和项目材料介绍课程。全程讲授和讲师演示，不安排学员操作或提交。课程既讲操作，也解释为什么这样做。原理以帮助选择工具、组织任务和检查结果为限。约240页含延伸材料，不能按页数承诺授课效果。培训单位、讲师姓名和日期未获确认，不虚构这些信息。';
}
function node(s,v,x,y,w,h=90,z=30){const n=s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill:'#F0F5F8',line:{fill:'#245B77',width:1.5}});n.text=v;n.text.style={typeface:F,fontSize:z,bold:true,color:C.navy,autoFit:'none',wrap:'word',insets:12,verticalAlignment:'middle'};return n;}
function arrow(s,a,b){s.shapes.connect(a,b,{kind:'straight',fromSide:'right',toSide:'left',line:{fill:'#245B77',width:2},tail:{type:'arrow',width:'med',length:'med'}});}
const ref='参考：Dawn Song，UC Berkeley CS294/194-196 Agentic AI，Fall 2025，Introduction，物理页6、10、19。\nhttps://rdi.berkeley.edu/agentic-ai/slides/introduction_25.pdf\n借鉴主题分组、动作反馈与可复查过程的组织；未采用旧产品状态、排名、预测、作业或考核。中文安排为本课程编写。';
{
 const s=page('课程顺序与四个模块',2);
 text(s,'先理解用法与限制，再沿科研过程展开，最后查看完整文件流程。',80,215,1440,90,32,false,'#245B77');
 const labels=['一  AI科研基本功','二  科研全流程','三  论文与项目产出','四  结题与影响力'];const ns=labels.map((v,i)=>node(s,v,80+i*380,345,300,95,28));for(let i=0;i<3;i++)arrow(s,ns[i],ns[i+1]);
 const groups=[['01  能力、原理与边界','02  Agent与工作流','03  Humanizer'],['04  选题与研究问题','05  文献检索与综述','06  研究与实验方案','07  数据处理与统计','08  科研图表与路线'],['09  论文、投稿与返修','10  基金申报','11  专利与技术交底'],['12  项目执行与结题','13  科研汇报与传播','14  本地与云端演示']];groups.forEach((ls,i)=>text(s,ls.join('\n'),80+i*380,485,320,260,28));
 text(s,'Harness在第2节解释执行管理，在第14节结合输入、运行记录和文件演示。',80,775,1440,55,27,false,C.green);
 s.speakerNotes.text='四个模块对应客户原课程。第一模块解释AI能力、常见失误、Agent概念和Humanizer。第二模块沿选题、文献、方案、数据和图表展开。第三模块将证据组织成论文、申报材料和技术交底。第四模块讲项目执行、结题、汇报和传播，再用本地与云端流程贯通前面的内容。这里只介绍课程位置，不逐项念标题。Humanizer单独成章，也用于其他章节的文字；Harness指任务执行管理，第2节讲框架，第14节看实际记录。箭头表示本课程讲授顺序，不表示科学研究不能返回修订。\n\n'+ref;
}
{
 const s=page('当天时段与八小时备课素材',3);
 text(s,'现场时段按09:00–12:00、13:30–17:00安排；延伸内容供讲师按进度选讲。',80,215,1440,90,31,false,'#245B77');
 node(s,'09:00–12:00',80,340,360,90,37);node(s,'13:30–17:00',80,540,360,90,37);
 text(s,'科研基本功与研究准备',545,340,975,58,38,true);text(s,'原理与常见概念、Humanizer；选题、文献与研究方案。',545,425,975,90,30);
 text(s,'数据分析与科研成果制作',545,540,975,58,38,true);text(s,'数据与图表、论文、申报、专利、结题、传播与完整流程。',545,625,975,90,30);
 text(s,'短休：10:20–10:30、15:00–15:10；午间：12:00–13:30。',80,735,1440,50,28,false,C.muted);
 text(s,'正式授课370分钟 ＋ 延伸讲授110分钟 ＝ 480分钟备课素材',80,790,1440,45,30,true,C.green);
 s.speakerNotes.text='上午180分钟，下午210分钟，合计390分钟。扣除两次10分钟短休，正式授课370分钟；午间90分钟不计入授课。另备110分钟延伸讲授，包括补充案例解释、图表读解和讲师演示，合计480分钟素材。不安排课堂练习、分组任务、账户操作或学员提交。240页包括正式讲授和延伸材料，现场按讲师节奏选择深度。分钟分配是备课安排，不能当作真人彩排记录。\n\n依据：客户指定时段和8小时备课要求；本课程安排两次10分钟短休，分钟按时段计算。';
}
{
 const s=page('讲师演示中的材料、动作与结果',4);
 text(s,'每个演示都说明材料来自哪里、工具实际做了什么，以及结果怎样检查。',80,215,1440,80,31,false,'#245B77');
 const rows=[['论文原文','定位支持结论的段落','摘录、原文位置与适用条件'],['公开数据表','检查数据、计算与绘图','可复算结果与可编辑数据图'],['指南、材料与模板','逐项对应并整理章节','Word草稿、来源与缺口']];rows.forEach((row,i)=>{const y=350+i*150,a=node(s,row[0],80,y,360,85),b=node(s,row[1],550,y,420,85),c=node(s,row[2],1080,y,440,85,28);arrow(s,a,b);arrow(s,b,c);});
 text(s,'公开原件、教学模拟和AI草稿分别注明；生成文件后，仍需核对科学内容。',80,795,1440,45,27,false,C.green);
 s.speakerNotes.text='用三条材料到结果的路径说明讲师会展示什么。文献演示回到原文，判断摘录能否支持结论。数据演示从公开CSV开始，检查缺失、比较对象和方法，再算结果、做图。申报演示从适用指南、已有研究材料和模板开始，将要求对应到内容，保留缺口。三条路径不是同一项研究，也不要求学员现场打开材料。案例到对应章节再介绍背景和来源。公开论文、公开企鹅数据和自编指南分别登记；TEACH-GRANT-01不是官方基金指南。AI编写与修订的文字另注明属性。图表示演示组织，不冒充执行截图；实际运行情况看对应章节记录和文件。\n\n'+ref;
}
await (await PresentationFile.exportPptx(p)).save(path.join(stage,'candidate.pptx'));
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const out=path.join(R,'output',`高校科研AI课程_Section0_${rev}.pptx`);
await finalizePresentation({workspaceDir:R,candidatePath:path.join(stage,'candidate.pptx'),finalPath:out,pythonExecutable:PY,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-heading-fit'],fontPolicy:{basis:'design',families:[F]},explicitTotalSlideCount:4,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],verifyArtifactToolImport:true,receiptPath:path.join(stage,'validation.json')});
console.log('FINAL',out);
