import {unzipSync,zipSync,strFromU8,strToU8} from 'fflate';
const escape=x=>String(x).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
export const digest=async bytes=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),b=>b.toString(16).padStart(2,'0')).join('');
export function fillTemplate(template,sections,metadata){
 if(template.byteLength>120000)throw Error('教学模板限120KB');
 let unpacked=0,entryCount=0;
 const entries=unzipSync(template,{filter:file=>{unpacked+=file.originalSize;entryCount++;if(unpacked>4000000||entryCount>150||file.name.includes('..')||file.name.endsWith('vbaProject.bin'))throw Error('模板包含不支持的内容或解压后过大');return true;}});
 if(!entries['word/document.xml']||!entries['[Content_Types].xml'])throw Error('模板不是受支持的 DOCX');
 let xml=strFromU8(entries['word/document.xml']);
 const grant=!!metadata.grant_profile;
 if(grant){
  xml=xml.replace('国家自然科学基金申请书撰写工作稿',escape((metadata.title||'基金项目申请书')+(metadata.material_type==='teaching-simulation'?'（研究设想示例）':'')));
  xml=xml.replace(/<w:p\b[^>]*>[\s\S]*?<\/w:p>/g,p=>p.includes('此文件为工作台生成的可编辑工作稿')?'':p);
 }
 xml=xml.replace('科研教学文档模板',escape((metadata.title||'科研材料')+' 教学草稿'));
 if(/<w:altChunk\b/.test(xml))throw Error('模板含外部文档嵌入，暂不支持');
 const count=(xml.match(/\{\{[^{}]+\}\}/g)||[]).length;
 if(count!==sections.length)throw Error('模板 CONTENT 标记数量与章节数量不一致；标记需在单个文字片段内');
 sections.forEach((section,index)=>{
  const token='{{'+section.title+'}}';if(!xml.includes(token))throw Error('模板缺少 '+token);
  const text=section.content+(grant?'':'\n来源：'+section.source_ids.join('、'));
  if(grant)xml=xml.replace(/<w:p\b[^>]*>[\s\S]*?<\/w:p>/g,p=>p.includes(token)?text.split(/\n\s*\n/).map(part=>p.replace(token,escape(part).replace(/\n/g,'</w:t><w:br/><w:t xml:space="preserve">'))).join(''):p);
  else xml=xml.replace(token,escape(text).replace(/\n/g,'</w:t><w:br/><w:t xml:space="preserve">'));
 });
 const paragraph=text=>'<w:p><w:pPr><w:spacing w:before="0" w:after="40" w:line="240" w:lineRule="auto"/>'+(['未决问题：','来源定位：'].includes(text)?'<w:keepNext/>':'')+'</w:pPr><w:r><w:rPr><w:rFonts w:ascii="Microsoft YaHei" w:eastAsia="Microsoft YaHei"/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">'+escape(text)+'</w:t></w:r></w:p>';
 const cited=new Set(sections.flatMap(s=>s.source_ids));
 const reference=s=>{const author=s.authors?.filter(Boolean).join(', ')||'',lead=author+(s.year?' ('+s.year+')':''),title=s.title.replace(/[.。]+$/,''),preprint=s.kind==='preprint'||/arxiv\.org|medrxiv\.org|biorxiv\.org|researchsquare\.com/.test(s.url||'');return (lead?lead+'. ':'')+title+(preprint?' [预印本]':'')+'. '+(s.doi?'https://doi.org/'+s.doi:s.url||s.locator);};
 const appendix=grant?[paragraph('参考文献'),...metadata.sources.filter(s=>s.title&&cited.has(s.id)).map(s=>paragraph(reference(s)))].join(''):[paragraph('AI 辅助教学草稿，待研究者核对。材料属性：'+metadata.material_type),paragraph('Skill 版本：'+metadata.skill_commit),paragraph('输入 SHA-256：'+metadata.input_sha256),paragraph('未决问题：'),...metadata.issues.map(x=>paragraph(x)),paragraph('来源定位：'),...metadata.sources.map(s=>paragraph(s.id+'：'+s.locator))].join('');
 xml=xml.replace(/(<w:sectPr\b)/,appendix+'$1');
 if(!xml.includes(appendix))xml=xml.replace('</w:body>',appendix+'</w:body>');
 entries['word/document.xml']=strToU8(xml);
 // Field replacement retains original paragraphs, styles and editable text.
 return zipSync(entries,{level:6});
}
