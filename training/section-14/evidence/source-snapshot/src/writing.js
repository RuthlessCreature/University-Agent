// Apply to every node, including intake and review, not only the polishing step.
export const WRITING_GUIDE=`面向正在写论文或申报材料的研究者，直接给他能读懂、能使用的内容。先写具体问题和做法；必要术语第一次出现时用一句普通话解释。不要用抽象名词堆出专业感，不给普通操作创造新名词。
summary 是本步成果正文，按内容写成自然段或简短条目，长度由信息决定，通常80至250字；不要汇报执行过程。
不要用“本步/本节点/本阶段已对……进行……”“已完成准入/冻结/闭环”“以下是”“综上所述”开头或结尾。不要列一串VERIFIED、PENDING等机器标签。把这些状态写成普通话，例如“论文摘要提到了这一点，具体实验条件还需查正文”。
材料审查直接写现有材料能回答什么、缺什么；要求核对直接列具体要求和对应材料；证据审查直接写哪条结论有哪份依据、哪一处还不够；审稿直接指出具体段落的问题和修订办法。不要把每项都写成同样长的三段或三条。
sections 是最终读者会看到的学术正文，不能夹带JSON字段名、流程状态、输入哈希、检索时间和操作提示。出处放入source_ids；重要事实可在正文引用作者、年份或DOI。缺失内容在正文对应位置简短标明[待补：具体内容]，细节集中到issues，不在每段重复免责声明。
issues 每项只写一个有位置、有影响的问题，能自行修订的直接修订；最多6项，没有则返回[]。不要每节点重复同一套通用提醒。
不得为了写得流畅而增加数据、实验、许可、全文阅读或已核验的说法。原材料自述不等于工具实测：只有本次运行实际执行了计算或读取文件，才可说“已复算”“已读取本地文件”；只有摘要时，只能据摘要判断。检索服务的summary是机器摘要，不能当成原文。
写完自查空话、夸大、强行对比、同义反复和机械排比，重写不自然的句子；保留数字、术语、引用、条件与不确定性。`;

export function editingMessages(candidate,readerGuide=''){
 return [{role:'system',content:'你是科研文字编辑。仅返回合法JSON，顶层仍为summary、sections、issues、route。只修改文字表达，不增加事实、数字或结论强度，不删除待补事项。sections的title、source_ids逐项原样保留，route原样保留。不要编写执行报告。\n'+WRITING_GUIDE+(readerGuide?'\n本次编辑专用于基金申请书：允许删除重复、枝节数字及过程解释，科学限定不得删除；操作性说明移到issues。\n'+readerGuide:'\n保留原文全部数字与证据限制。')},{role:'user',content:'请编辑下面的完整JSON。'+(readerGuide?'sections直接给同行评审人阅读，以申请人的立场成文。':'文字直接交给研究者。')+'只返回完整JSON：\n'+JSON.stringify(candidate)}];
}
export function validateEdit(before,after,{allowOmissions=false}={}){
 if(JSON.stringify(before.sections.map(s=>[s.title,s.source_ids]))!==JSON.stringify(after.sections.map(s=>[s.title,s.source_ids])))throw Error('文字修订改变了章节或来源编号。');
 const numbers=text=>[...new Set(String(text).match(/\d+(?:[.,]\d+)*/g)||[])].sort();
 for(let i=0;i<before.sections.length;i++){const prior=numbers(before.sections[i].content),next=numbers(after.sections[i].content);if(allowOmissions?next.some(n=>!prior.includes(n)):JSON.stringify(prior)!==JSON.stringify(next))throw Error('文字修订改变了正文数字，需要重新修订。');}
 if(before.issues.length&&!after.issues.length)throw Error('文字修订遗漏了未决问题。');
 return after;
}
