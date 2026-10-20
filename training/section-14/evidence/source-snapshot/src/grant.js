import {zipSync,strToU8} from 'fflate';
export const GRANT_SOURCE='https://www.nsfc.gov.cn/p1/3381/2821/99242.html';
export const GRANT_SECTIONS=['项目基本信息','中文摘要','立项依据','研究内容','研究基础','其他需要说明的情况'];
export const GRANT_PROSE=`正文的读者是基金同行评审人。以申请人的立场陈述科学问题、论据、研究设想、方法与预期认识，写成申请书，不向操作者讲解怎样写申请书。
文字也应让熟悉科研、但未专门研究这种算法的高校教师读懂。先讲具体问题，再解释方法。句子写清谁、对什么材料、做什么、怎样判断结果。每段只展开一个问题；长句拆开，避免用分号把一串抽象名词连在一起。学术严谨来自条件、依据和检验办法，不来自难词。
正文不得出现“本次检索”“本工作稿”“本节点”“输入材料”“申请人未提供”“建议补充”“需申请人核实”“VERIFIED/PENDING/UNSUPPORTED”等过程说明。不能写“一个尚未证实的假说”反复提醒，直接写研究假说及拟检验的关系。所有操作提醒、资料缺口与证据读取限制放入issues，不能进入摘要、立项依据或研究方案。
立项依据从具体科学矛盾切入，把文献组织成论证，不逐篇罗列工具名字、召回率和百分比，不以“这些结果说明”“上述研究表明”反复收束。只保留论证所需的代表性比较；数据来自不同评价口径时不能横向排名。说明已有认识在哪个条件下不足，以及本项目为什么能进一步回答。
研究内容写清研究对象与关系、方法如何区分不同解释、拟观测什么以及结果如何回答问题。按研究逻辑展开，避免每段套“针对……，通过……，实现……”和整齐的三句口号。预期认识用研究性表述，不承诺尚无依据的性能提升。
删去“研究价值不在于……而在于……”“这为……从……走向……提供……”这类自我评价和升华句，直接写拟得到的科学认识及其适用条件。不用引号给普通词语增加分量，不在每段末尾重复“这说明”“这提示”“这体现”。已有文献与本项目的比较要落在对象、假设、方法或验证条件上。
研究基础只写申请人有材料支撑的积累和条件。缺少前期成果时，只留简短[待补：成果及本人贡献]；不要写长篇清单向评审人解释为什么不能编造。没有材料就缩短，不能靠可行性套话填满。
中文摘要是独立、紧凑的申请书摘要，不写政策、指南、工作流、材料状态或文献检索过程，不堆综述统计数字。基本信息只列已知字段，未知字段以简短待补标记保留，不解释填表后果。
正文不显示NET编号、哈希或系统来源账本。正常使用作者与年份或文献题名引用，source_ids留给后台生成参考文献。issues是单独的作者修改记录，语气可以直接，不能伪装成正文。`;

export const GRANT_SCREENING_GUIDE="本例先说明“AI把可能相关的论文排在前面，但排在后面的论文仍可能包含符合要求的研究，怎样判断何时可以停”。写清实际做法：换主题或年份观察漏检；从剩余论文中随机抽查并人工核对；估计仍可能漏掉多少，检验停止办法。未开展的工作用拟、将、计划等准确时态。\n“分布漂移”首次出现应解释为论文主题、发表时间或相关论文比例发生变化；“概率校准”先解释AI的把握是否与实际筛选结果相符；“审计抽样”写成人工随机抽查；“停止规则”说明达到什么条件才能停止筛选；“风险上界”说明是在规定的统计条件下估计仍可能漏掉多少，不能写成绝不会漏检的保证。能直接用具体表述讲清的地方，不再重复术语。\n不要凭空创造“排序性漏检”“阈值性漏检”“设计型信息”一类未定义名词，也不要列出材料没有给出的数学假设以显得严谨。术语确实是研究必需时，在第一次出现处解释含义，并说明对应的操作或检验。摘要不堆算法名、指标缩写或抽象复合词。“语料”可以直接写成待筛选的论文；“固定预算”说清预先规定阅读多少篇；“区间覆盖率”说清估计范围有多少次包含了真实的漏检情况。不要只列“名义水平、统计性质、可观测特征”等名词，写出具体判断或计算的是什么。摘要先写读者正在面对的问题，接着说明实际怎么研究，不连续塞入技术名称。";
export const GRANT_PLAIN_EXAMPLE=`下面只示范这份文献筛选项目应有的表达清晰度，不是新增事实。正文仍须依照当前材料与文献。摘要不要塞成一个长段，分成几个短段，把多个动作拆成短句。
“做系统综述时，研究者需要从大量论文中找出符合要求的研究。AI可以把可能相关的论文排在前面，但排在后面的论文也可能被漏掉。本项目研究何时可以停止筛选，以及停止后还可能漏掉多少相关论文。

研究将使用已有人工筛选结果的公开数据，重现AI筛选过程。通过改变论文主题、发表年份和相关论文的比例，检查哪些情况下容易漏检。再从剩余论文中随机抽查一部分，请研究者核对，用抽查结果估计还可能漏掉多少。

据此制定停止筛选的条件，再用其他论文数据检验。在同样的漏检要求下，比较不同办法需要人工阅读多少论文，明确这种办法在哪些情况下可靠，在哪些情况下应继续筛选。”
本例摘要尽量使用“论文资料”“预先规定阅读多少篇”“按AI的判断分数决定是否停止”等具体说法。不要用“语料”“固定预算”“概率阈值”“名义水平”“估计量性质”缩写整件事。正文中的专业含义仍应准确，必要统计条件放在方法相应位置讲清。`;
export function grantReaderGuide(input){return GRANT_PROSE+(/(?:文献|论文).*筛|筛.*(?:文献|论文)|systematic review/i.test(input?.title||'')?'\n'+GRANT_SCREENING_GUIDE+'\n'+GRANT_PLAIN_EXAMPLE:'');}

export function validateGrantProse(candidate,input){
 for(const section of candidate.sections){
  if(/本次(?:联网)?检索|此次检索|本工作稿|本节点|本阶段|输入材料|申请人(?:未|尚未)提供|建议(?:申请人|补充|研究者)|需(?:由)?申请人(?:核实|确认|补充)|NET-[0-9a-f]{6,}|VERIFIED|PENDING|UNSUPPORTED|尚未证实的假说/i.test(section.content))throw Error('申请书正文混入了面向操作者的过程说明：'+section.title+'。请将说明移入issues，以申请人的立场重写正文。');
  if(/(?:价值|意义|贡献)不在于[^。！？]*而在于/.test(section.content))throw Error('正文有空泛的价值宣言：'+section.title+'。删除强行对比，直接写具体科学认识。');
  for(const term of ['排序性漏检','阈值性漏检','设计型信息'])if(section.content.includes(term)&&!(input?.research_notes||'').includes(term))throw Error('正文使用了材料没有定义的术语“'+term+'”。请直接说明发生了什么，以及怎样测量。');
  if(section.title==='中文摘要'&&/(?:文献|论文).*筛|筛.*(?:文献|论文)/.test(input?.title||'')&&/语料|概率阈值|固定预算|名义水平|估计量性质/.test(section.content))throw Error('本例摘要仍在用缩写和难词概括做法。请直接写论文资料、阅读多少篇、怎样判断是否停止等具体含义。');
 }
 return candidate;
}
export const GRANT_STEPS=[
 {id:'intake',title:'检查已有材料',skill:'grant-template',section_titles:[],intent:'核对基金类别、年度、研究属性、申请代码、期限与材料。直接给出本项目科学问题的工作表述、可用材料和具体缺口，不编造资格结论或依托单位。'},
 {id:'background',title:'为什么值得研究',skill:'grant-background',section_titles:['立项依据'],intent:'写立项依据正文。先说明研究者遇到的具体困难，已有办法在哪种情况下不够用，本项目要回答什么。用相关文献支持判断，专业词第一次出现时说明意思，不从宏观政策或空泛意义开篇。'},
 {id:'content',title:'准备怎样研究',skill:'grant-research-content',section_titles:['研究内容'],intent:'写清实际怎么做：研究哪些材料，改变哪些条件，与什么办法比较，记录什么结果，怎样判断最初的想法是否成立。说明各项工作如何衔接、每年做什么，以及可能得出什么认识。不列只有名词的方法清单，不把计划写成已经取得的结果。'},
 {id:'foundation',title:'已有研究基础',skill:'grant-technical-route',section_titles:['研究基础'],intent:'依据申请人实际材料写前期工作、与拟研究问题的关系、可行性、实验或计算条件、缺少条件及风险应对。公开论文、他人成果或公开数据可用性不能写成申请人自己的研究积累。资料未提供的地方具体标记待补。'},
 {id:'summary',title:'写摘要与基本信息',skill:'grant-research-content',section_titles:['项目基本信息','中文摘要','其他需要说明的情况'],intent:'根据已写正文提炼中文摘要，包含问题、拟解决的关键点、主要方法和预期贡献；填写已提供的项目基本信息。相关在研项目、已结题项目、申请单位不一致等事项只按申请人提供的事实写，未提供时不得填无或代做声明。'},
 {id:'audit',title:'检查全文',skill:'grant-review',section_titles:GRANT_SECTIONS,intent:'以熟悉科研、但没有专门研究此方法的教师身份通读全文。每句话必须能说清实际意思；抽象名词连续出现时改成具体做法，必要术语补解释。再检查题目、摘要、问题、方法、已有基础和安排是否一致，引用是否支持判断。直接修订正文，保留具体缺口，不打分、不估中标概率、不作签核。'}
];
const escape=value=>String(value).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
export function grantTemplate(){
 const p=(text,heading=false)=>'<w:p><w:pPr>'+(heading?'<w:pStyle w:val="Heading1"/><w:keepNext/>':'<w:spacing w:after="120" w:line="360" w:lineRule="auto"/>')+'</w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="宋体"/><w:sz w:val="24"/>'+(heading?'<w:b/>':'')+'</w:rPr><w:t xml:space="preserve">'+escape(text)+'</w:t></w:r></w:p>';
 const body=p('国家自然科学基金申请书撰写工作稿',true)+p('按2026年面上项目、青年科学基金项目（C类）正文框架整理。此文件为工作台生成的可编辑工作稿，不是基金委官方下载模板。')+GRANT_SECTIONS.map(title=>p(title,true)+p('{{'+title+'}}')).join('');
 return zipSync({'[Content_Types].xml':strToU8('<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'),'_rels/.rels':strToU8('<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'),'word/document.xml':strToU8('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'+body+'<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr></w:body></w:document>')},{level:6,mtime:new Date("2026-01-01T00:00:00Z")});
}
export function prepareGrant(fields,material_type='authorized-user'){
 const get=key=>typeof fields[key]==='string'?fields[key].trim():'';
 if(!['面上项目','青年科学基金项目（C类）'].includes(get('fund_type')))throw Error('请选择面上项目或青年科学基金项目（C类）；其他基金请使用自定义入口。');
 if(get('year')!=='2026')throw Error('内置框架对应2026版；其他年度请提供当年指南和模板并使用自定义入口。');
 if(!get('title')||!get('question')||!get('design'))throw Error('请填写项目名称、科学问题与研究假说、研究内容与方案。');
 if(Object.values(fields).some(x=>typeof x==='string'&&x.length>18000))throw Error('单项材料过长，请控制在18000字以内。');
 const sources=[{id:'NSFC-2026',type:'public-source',locator:GRANT_SOURCE+'；基金委2026年申请书改版说明，正文三部分与篇幅说明。'}];
 const blocks=[['BACKGROUND','立项依据素材与文献',get('background')],['QUESTION','科学问题与研究假说',get('question')],['DESIGN','研究内容与方案',get('design')],['FOUNDATION','前期工作与成果证据',get('foundation')],['CONDITIONS','研究条件与合作分工',get('conditions')],['SCHEDULE','年度安排与预期成果',get('schedule')],['OTHER','相关项目与其他说明',get('other')]];
 for(const [id,label,text] of blocks)if(text)sources.push({id,type:material_type,locator:'申请人输入：'+label,content:text});
 get('sources').split(/\r?\n/).filter(Boolean).forEach((locator,i)=>sources.push({id:'REF-'+(i+1),type:material_type,locator}));
 const profile={framework:'nsfc-2026',writing_style:'plain-academic',fund_type:get('fund_type'),year:'2026',research_attribute:get('attribute')||'待填写',application_code:get('code')||'待填写',period:get('period')||'待填写',funding:get('funding')||'待核对对应类别经费要求',source_url:GRANT_SOURCE,template_origin:'按公开改版说明制作的工作模板，非官方模板'};
 const sections=GRANT_SECTIONS.map(title=>({title,content:'',source_ids:['NSFC-2026'],max_chars:title==='研究内容'?10000:title==='立项依据'||title==='研究基础'?7000:title==='中文摘要'?1000:3000}));
 const goals=[{id:'G1',text:get('question')}];
 const guide={id:'NSFC-2026-WRITING',type:material_type,source_url:GRANT_SOURCE,framework:'nsfc-2026',required_sections:GRANT_SECTIONS,requirements:[],text:'基金委2026年改版适用于面上项目和青年科学基金项目（C类）。正文由立项依据、研究内容、研究基础组成，研究内容可按研究逻辑组织，正文原则上不超过30页。项目基本信息、摘要和其他说明为工作稿的辅助整理部分。'+(get('guide')?'\n申请人补充的指南原文：\n'+get('guide'):''),page_limit_note:'原则上不超过30页；本工具不以字符数冒充最终页数检查。'};
 return {input:{kind:'grant',title:get('title'),material_type,grant_profile:profile,goals,requirements:[],sources,sections,research_notes:blocks.filter(x=>x[2]).map(([id,label,text])=>'['+id+'] '+label+'\n'+text).join('\n\n')},guide,template_base64:btoa(String.fromCharCode(...grantTemplate()))};
}
export function grantInstructions(input,stage){
 if(input.grant_profile?.framework!=='nsfc-2026')return '';
 return '\n'+grantReaderGuide(input)+'\n按2026版三部分正文组织，辅助整理基本信息、中文摘要和其他说明。研究内容内的小标题按项目逻辑安排。申请人研究事实与公开文献分清，不能编造资格、项目编号、前期结果、伦理批准或在研项目声明。\n本步只生成或修订这些sections：'+JSON.stringify(stage.section_titles||[])+'。其他章节由后台保留，不必重写。intake只写summary与issues，sections返回[]。以现有证据决定篇幅，不按统一字数凑齐章节。立项依据与研究内容展开必要论证，摘要精练到约400字；没有申请人前期材料时，研究基础仅保留具体待补位置，不能扩写成情况说明。最后检查节点返回完整六章。';
}
export function mergeGrantCandidate(text,input,previous,stage){
 const candidate=JSON.parse(text.replace(/^```(?:json)?\s*/,'').replace(/\s*```$/,''));
 if(!Array.isArray(candidate.sections))throw Error('申报节点未返回sections数组。');
 const titles=input.sections.map(s=>s.title),seen=new Set();
 for(const section of candidate.sections){if(!titles.includes(section.title)||seen.has(section.title))throw Error('申报节点出现未知或重复章节。');seen.add(section.title);}
 for(const title of stage?.section_titles||[])if(!candidate.sections.some(s=>s.title===title&&typeof s.content==='string'&&s.content.trim()))throw Error('本步没有写出所需正文：'+title);
 const last=previous.at(-1)?.content.sections||input.sections;
 candidate.sections=titles.map(title=>candidate.sections.find(s=>s.title===title)||last.find(s=>s.title===title)||input.sections.find(s=>s.title===title));
 return JSON.stringify(candidate);
}
export const GRANT_EXAMPLE=prepareGrant({fund_type:'面上项目',year:'2026',title:'AI筛选文献时漏检的原因与停止条件研究',attribute:'自由探索类基础研究',period:'示例拟设四年，具体起止年月按申报年度指南填写',background:'【研究设想教学示例】针对系统综述文献筛选，重点研究跨主题、跨时间语料变化后，主动学习依赖的置信度与实际漏检风险不一致的问题。拟检索ASReview、active learning systematic review、stopping criterion、distribution shift等文献。未输入任何申请人自有结果。',question:'【拟研究设想】AI可以把可能相关的论文排在前面，但排在后面的论文中仍可能有符合综述要求的研究。连续几批未找到相关论文，是否足以停止筛选？研究主题、发表年份或相关论文所占比例变化后，同一停止办法是否仍然可靠？拟研究AI的排序和判断把握与实际漏检之间的关系，并通过随机抽查剩余论文来估计还可能漏掉多少。',design:'先在已有人工筛选结果的公开数据上重现AI筛选过程，改变论文主题、发表年份及符合要求的论文比例，比较哪些论文被排到后面或被漏掉。再从尚未筛选的论文中随机抽取一部分，请人核对，据此估计剩余相关论文的数量与估计范围，检查该范围在不同数据上是否可靠。最后据此制定停止筛选的条件，与固定阅读数量、按AI判断把握停止、已有停止办法进行比较。记录实际漏掉多少相关论文、读了多少论文，以及什么情况下估计不可靠，不预填提升比例。',foundation:'未提供申请人代表性论文、前期实验、独立结果或已承担项目。请在研究基础对应位置保留具体待补内容。公开语料可获取不构成申请人的研究基础。',conditions:'拟采用公开且许可允许复用的文献筛选数据。实际计算条件、数据授权、团队分工和合作条件均待申请人提供。',schedule:'第一年：研究对象界定、文献比较、数据与评价方案；第二年：漂移条件下的误差分析；第三年：风险估计与停止方法；第四年：外部验证、失效边界和成果整理。所有安排均为教学设想，不是已完成工作。',other:'申请代码、申请资格、在研项目、已结题项目、单位一致性与相关伦理事项尚未提供，不能据此填写无。',sources:'NSFC改版说明仅用于申请书框架；主题文献由本次联网检索取得，不预填虚构参考文献。'},'teaching-simulation');
