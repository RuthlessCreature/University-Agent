import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const R=path.dirname(fileURLToPath(import.meta.url)),rev=process.env.SECTION_REVISION||'s0-r3';
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
 s.speakerNotes.text='先请学员带入一件自己的科研任务，例如读论文、处理数据或准备项目材料。课程既讲操作，也解释为什么这样做。原理以帮助选择工具、组织任务和检查结果为限。约240页含延伸材料，不能按页数承诺授课效果。培训单位、讲师姓名和日期未获确认，不虚构这些信息。';
}
{
 const s=page('这门课按什么顺序学',2);
 text(s,'基础与研究准备',80,211,690,48,30,true,C.green);text(s,'成果制作与完整流程',850,211,670,48,30,true,C.green);
 const subtitles=['提问、提供材料，理解常见失误','ChatGPT、Codex、Agent 与 Harness','论文、PPT、报告怎样写得自然','比较候选方向，提出具体问题','找到论文，读原文，比较结论','确定对象、比较办法与测量','检查数据，运行代码，解释结果','数据图、示意图与可编辑路线','组织证据，修改段落，回应意见','指南、研究者材料与 Word 文件','已有技术、实施办法与附图','进展、成果与证明材料','组会、答辩、项目汇报与介绍','同一套 Skill，连续执行与恢复'];
 const titles=['科研 AI 上手与基本原理','认识会做事的 AI','Humanizer：把话写清楚','选题与研究问题','文献检索、阅读与综述','研究与实验方案','数据处理与统计分析','科研图表与技术路线','论文写作、投稿与返修','基金申报与 Grant Agent','专利挖掘与技术交底','项目执行与结题','科研汇报与成果传播','本地与云端 Agent 实操'];
 for(let i=0;i<14;i++){const x=i<7?80:850,y=280+(i%7)*73; text(s,String(i+1).padStart(2,'0'),x,y,65,42,29,false,C.red);text(s,titles[i],x+85,y,585,43,31,true);text(s,subtitles[i],x+85,y+43,585,36,24,false,C.muted);}
 text(s,'Agent：能调用工具、分步执行任务的 AI 助手。相关概念会用同一个例子逐步解释。',80,810,1440,33,24,false,C.green);
 s.speakerNotes.text='共14个内容章节，另有本节课程导入。新增的概念与Humanizer分别占独立章节。概念章先用同一任务比较“给建议”和“执行工具得到文件”，再解释Agentic AI、Agent、Workflow、Skill、MCP与Harness。不能把ChatGPT和Codex直接当作两种互斥概念。Harness在第2章解释框架，在第14章结合真实流程讲运行、记录与恢复。此页是全课规划，不表示后续章节已制作或验收。';
}
{
 const s=page('当天怎样安排',3);
 text(s,'09:00–12:00',80,242,445,80,49,true,C.navy);text(s,'科研基本功与研究准备',610,242,905,67,42,true);
 text(s,'AI 的用法与原理、常见概念与 Humanizer；\n选题、文献阅读和研究方案。',610,332,905,110,33);
 rule(s,80,472,1440);
 text(s,'13:30–17:00',80,520,445,80,49,true,C.navy);text(s,'数据分析与科研成果制作',610,520,905,67,42,true);
 text(s,'数据分析、科研图表、论文、申报与专利；\n项目结题、科研汇报和完整 Agent 流程。',610,610,905,110,33);
 text(s,'10:20–10:30、15:00–15:10 休息。12:00–13:30 午间休息。',80,744,1440,45,29,false,C.muted);
 text(s,'正式授课 370 分钟，另备 110 分钟延伸案例与练习，共 8 小时素材。',80,801,1440,38,28,false,C.green);
 s.speakerNotes.text='正式时段上午180分钟，下午210分钟，合计390分钟；扣除两次10分钟短休，授课370分钟。另备110分钟延伸材料，备课总量480分钟。约240页包含备用案例、演示和练习，不把所有页面都算作现场必讲。具体章节边界和演示时长随彩排调整，此页不构成已完成彩排的承诺。';
}
{
 const s=page('今天会跟着做哪些事',4);
 const rows=[['01','读论文，查证一句结论','从论文原文开始','请 AI 找出支持结论的段落，\n自己回到原文核对，\n记下这句话在什么条件下成立。'],['02','处理数据，做一张图','从一份原始数据表开始','先检查缺失值和异常记录，\n再做统计、画图，\n说明图中的差异能支持什么判断。'],['03','对照申报要求，整理材料','从指南与研究者已有材料开始','逐项找出要求，匹配已有内容；\n缺证据的地方明确标出，\n最后整理成可以继续修改的 Word。']];
 for(let i=0;i<3;i++){const r=rows[i],y=224+i*178;text(s,r[0],80,y,80,65,45,false,C.red);text(s,r[1],195,y,575,52,37,true);text(s,r[2],195,y+73,575,43,28,false,C.muted);text(s,r[3],850,y+6,665,130,32);if(i<2)rule(s,195,y+147,1325);}
 text(s,'讲到对应章节时，再介绍案例背景、材料来源，并带着大家操作。',80,781,1440,53,28,false,C.green);
 s.speakerNotes.text='开场用三件具体工作说明课堂怎样学，不要求学员现在打开文件。读论文：核对AI摘出的原文是否支持结论，保留成立条件；处理数据：先检查，再统计和画图，解释差异；整理申报材料：按要求对应研究者已有内容，标出缺口，不凭空补写成果。三件事是全课中的代表任务，不是全部课程。具体案例和材料来源到相应章节再介绍。本项目现有公开论文、公开企鹅数据及TEACH-GRANT-01教学任务可供后续选用，它们彼此不是同一项研究；现有指南与Word模板属于教学模拟，不可称作正式申报材料。Humanizer用于表达修订时必须保留事实、证据和限定。';
}
await (await PresentationFile.exportPptx(p)).save(path.join(stage,'candidate.pptx'));
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const out=path.join(R,'output',`高校科研AI课程_Section0_${rev}.pptx`);
await finalizePresentation({workspaceDir:R,candidatePath:path.join(stage,'candidate.pptx'),finalPath:out,pythonExecutable:PY,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-heading-fit'],fontPolicy:{basis:'design',families:[F]},explicitTotalSlideCount:4,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],verifyArtifactToolImport:true,receiptPath:path.join(stage,'validation.json')});
console.log('FINAL',out);
