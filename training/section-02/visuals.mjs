// Editable lecture diagrams. Research situations are explicitly illustrative.
export function drawVisual(s,d,{text,node,arrow,rule,C}){
 const T=(v,x,y,w,h=70,z=28,b=false,c=C.ink)=>text(s,v,x,y,w,h,z,b,c);
 const N=(v,x,y,w=310,h=80,fill='#F0F5F8')=>{const n=node(s,v,x,y,w,h);n.fill=fill;return n;};
 const link=(a,b,from='right',to='left',kind='straight')=>arrow(s,a,b,from,to,kind);
 const doc=(v,x,y,w=260,h=145)=>{const a=N(v,x,y,w,h,'#FFFFFF');rule(s,x+20,y+h-20,w-40);rule(s,x+20,y+h-9,w-80);return a;};
 switch(d.n){
 case 1:{
  const a=doc('申报指南',80,355,260,130),b=N('提取要求',440,380),c=N('组织内容',850,380),e=doc('申报书初稿',1260,355,260,130);
  link(a,b);link(b,c);link(c,e);
  ['条款与附件','要求清单','段落与证据','Word＋问题清单'].forEach((v,i)=>T(v,80+i*395,520,300,60,28,true,C.blue));
  T('人负责判断',80,650,300,60,32,true);T('资格与方向是否匹配；研究问题是否成立；已有结果能否支持方案。',440,650,1080,90,30);
  return true;}
 case 2:{
  N('',80,355,750,410,'none');T('Agent 执行系统',110,380,670,55,34,true,C.blue);
  const a=N('模型\n生成操作请求',120,465,280,135),b=N('工具\n执行并返回结果',510,465,280,135),c=N('状态：已完成、失败、待核实',120,650,670,80,'#E7F2EF');link(a,b);link(b,c,'bottom','top','elbow');
  T('这些系统如何工作',920,318,600,50,30,true,C.blue);T('Agentic AI',920,402,600,55,40,true);T('描述目标导向、多步行动、\n根据反馈调整等特征。',920,470,600,100,31);
  T('ChatGPT / Codex',920,622,600,55,35,true);T('产品实例；能力有重叠，\n不能分别等同于两个概念。',920,682,600,95,29);return true;}
 case 3:{
  T('教学情境：核验一条缺少 DOI 的引文',80,310,1440,45,28,true,C.blue);
  const a=doc('待核验引文',80,440,260,140),b=N('查出版页面',460,465,320),c=N('核对字段',900,465,260),e=doc('核对表',1280,440,240,140);link(a,b);link(b,c);link(c,e);
  T('Agentic 特征',80,370,340,45,31,true);T('发现缺项后继续补查，依据结果决定下一步。',460,370,1060,55,29);
  T('AI Agent 系统',80,655,330,55,32,true);T('承担这一任务的模型、检索工具、文件工具和运行安排。',460,655,1060,105,31);
  return true;}
 case 5:{
  T('预设工作流',80,335,290,60,33,true,C.blue);
  const top=['提取条款','字段检查','填入模板','导出文件'].map((v,i)=>N(v,410+i*285,325,255,85));for(let i=0;i<3;i++)link(top[i],top[i+1]);
  T('步骤和分支预先规定，适合要求稳定、重复处理的任务。',410,440,1110,60,29);
  T('动态补查',80,580,290,60,33,true,C.green);
  const a=N('要求含糊',410,570,255,85),b=N('读附件／说明',790,570,310,85),c=N('确认或登记缺项',1210,570,310,85,'#E7F2EF');link(a,b);link(b,c);
  T('按材料选择下一步；主流程可以固定，局部环节保留动态判断。',410,710,1110,70,29);return true;}
 case 7:{
  const a=N('模型提出\n操作请求',80,385,300,130),b=N('工具实际执行',550,385,410,130,'#E7F2EF'),c=doc('可检查的结果',1130,370,390,160);link(a,b);link(b,c);
  const data=[['检索','查询条件、来源与读取日期'],['计算','数据版本、代码与运行输出'],['写文件','可编辑文件、预览与检查记录']];
  data.forEach((r,i)=>{T(r[0],100,585+i*68,260,50,30,true,C.blue);T(r[1],550,585+i*68,970,60,29);});return true;}
 case 8:{
  const a=N('Skill：文献核验',80,450,320,100,'#E7F2EF');
  const labels=['任务指令','参考规范','可选脚本'];const desc=['核对步骤与缺项处理','字段、模板与来源要求','检索、比对或文件输出'];
  labels.forEach((v,i)=>{const b=doc(v,570,320+i*155,330,120);link(a,b,'right','left','elbow');T(desc[i],1030,350+i*155,490,85,30);});
  return true;}
 case 9:{
  const a=doc('本次任务\nPrompt',80,425,260,140),b=N('Agent 执行系统',500,430,350,130,'#E7F2EF'),c=N('工具／数据服务',1120,430,400,130);link(a,b);link(b,c);T('MCP 可作为连接方式',875,360,645,60,29,true,C.blue);
  const sk=N('Skill：可复用的任务方法',500,650,660,80);link(sk,b,'top','bottom','elbow');
  T('这次要核验什么',80,595,300,70,28);T('查记录、读材料、导出表格',1120,595,400,100,28);
  T('不采用 MCP 的工具，也可被系统调用。',80,740,1440,45,27,false,C.muted);return true;}
 case 11:{
  const a=doc('同一任务与材料',80,445,280,130),e=doc('合并结果\n保留冲突',1230,445,290,130);const tasks=['检索原始来源','处理统计数据','核对引用与论证'];
  tasks.forEach((v,i)=>{const b=N(v,570,320+i*155,420,95,i===2?'#E7F2EF':'#F0F5F8');link(a,b,'right','left','elbow');link(b,e,'right','left','elbow');});
  T('共享输入版本、字段标准和来源记录',80,755,1440,45,29,true,C.blue);return true;}
 case 12:{
  const a=N('当前任务上下文',80,345,470,100),b=doc('状态记录',650,330,330,135),c=N('接续任务',1160,345,360,100,'#E7F2EF');link(a,b);link(b,c);
  const a2=doc('原始材料',80,600,300,135),b2=doc('已完成结果',520,600,330,135),c2=doc('待核实／失败项',1010,600,510,135);
  link(a2,b,'top','bottom','elbow');link(b2,b,'top','bottom','elbow');link(c2,b,'top','bottom','elbow');
  T('摘要用于接续；原文件、来源位置与版本仍需保留。',80,755,1440,45,27,true,C.blue);return true;}
 case 13:{
  N('',450,320,1070,445,'none');T('Harness：组织执行、保存进度、处理异常',485,340,1000,55,32,true,C.blue);
  const a=doc('目标与材料',80,435,280,135),b=N('模型选择下一步\n使用 Skill 中的方法',500,430,360,140),c=N('工具执行\n返回实际结果或错误',1060,430,410,140,'#E7F2EF'),e=N('状态记录与结果检查',500,665,970,80);link(a,b);link(b,c);link(c,e,'bottom','top','elbow');
  T('任务要求\n权限与完成条件',80,625,290,100,29);return true;}
 case 14:{
  const a=doc('输入材料\n来源＋版本',80,360,340,160),b=N('运行中的任务',610,400,380,100,'#E7F2EF'),c=doc('输出文件\n对应输入版本',1180,360,340,160);link(a,b);link(b,c);
  const e=N('进展记录：已完成／待核对／失败',430,610,740,90);link(b,e,'bottom','top');
  T('指南更新',80,735,330,55,31,true,C.blue);T('标记受影响的章节 → 重新核对 → 再更新完成状态',480,735,1040,65,29);return true;}
 case 15:{
  const a=N('读取材料',80,370,400,100),b=N('修改文件',600,370,400,100),c=N('对外提交',1120,370,400,100,'#F8EDE9');link(a,b);link(b,c);
  T('限定文件与外部来源',80,510,400,80,30);T('限定写入位置，保留原件',600,510,400,100,30);T('按授权范围，保留人工确认',1120,510,400,100,30);
  T('研究者确认',80,680,350,55,33,true,C.blue);T('敏感材料的使用；关键文件覆盖；投稿、申报与对外发送。',490,680,1030,100,30);return true;}
 case 18:{
  const a=N('当前科研任务',80,470,290,100,'#E7F2EF');
  const qs=['讨论与解释','步骤稳定、重复处理','需要边查边判断','需要跨会话持续完成'];const choices=['对话协作','预设工作流','Agent＋工具反馈','补充状态与恢复安排'];
  qs.forEach((v,i)=>{const y=310+i*123,b=N(v,550,y,440,77),c=N(choices[i],1150,y,370,77,i===3?'#E7F2EF':'#FFFFFF');link(a,b,'right','left','elbow');link(b,c);});return true;}
 default:return false;
 }
}
