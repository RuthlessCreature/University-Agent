// Repackage the current Artifact Tool section decks without re-authoring slides.
// Native slide XML, charts, workbooks and assets remain byte-identical.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
const HERE=path.dirname(fileURLToPath(import.meta.url)),A=path.resolve(HERE,'../..');
const skill='C:/Users/Georgij Xe/.codex/plugins/cache/openai-primary-runtime/presentations/26.1015.12040/skills/presentations';
const {requireRuntimeModule}=await import(pathToFileURL(path.join(skill,'container_tools/runtime_helpers.mjs')));
const JSZip=await requireRuntimeModule('jszip'),XML=await requireRuntimeModule('xml-js');
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')));
const REV=process.env.COURSE_REVISION||'course-r2',R=path.join(A,'training/full-course'),stage=path.join(R,'.build',REV);
await fs.mkdir(stage,{recursive:true});await fs.mkdir(path.join(R,'output'),{recursive:true});
const progress=JSON.parse(await fs.readFile(path.join(HERE,'section-progress.json'),'utf8'));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const parse=b=>XML.xml2js(b.toString('utf8'),{compact:false});
const encode=o=>Buffer.from(XML.js2xml(o,{compact:false,spaces:0}));
const root=o=>o.elements.find(e=>e.type==='element');
const child=(name,attributes={},elements=[])=>({type:'element',name,attributes,elements});
const relpath=p=>path.posix.join(path.posix.dirname(p),'_rels',path.posix.basename(p)+'.rels');
const resolve=(owner,target)=>target.startsWith('/')?target.slice(1):path.posix.normalize(path.posix.join(path.posix.dirname(owner),target));
const relative=(owner,target)=>path.posix.relative(path.posix.dirname(owner),target);
const merged=new JSZip(),sources=[],maps=[],manifest=[],defaults=new Map(),overrides=new Map();
const counters=new Map();let offset=0;
for(const sec of progress.sections){
 const source=await fs.readFile(path.join(A,sec.pptx));if(sha(source)!==sec.sha256)throw Error('Source changed: '+sec.id);
 const zip=await JSZip.loadAsync(source),map=new Map([['ppt/presentation.xml','ppt/presentation.xml']]);
 const parts=Object.keys(zip.files).filter(n=>!zip.files[n].dir&&n!=='[Content_Types].xml'&&!n.endsWith('.rels')&&n!=='ppt/presentation.xml');
 for(const old of parts){
  const slide=old.match(/^ppt\/slides\/slide(\d+)\.xml$/),note=old.match(/^ppt\/notesSlides\/notesSlide(\d+)\.xml$/);
  let dest;
  if(slide)dest=`ppt/slides/slide${offset+Number(slide[1])}.xml`;
  else if(note)dest=`ppt/notesSlides/notesSlide${offset+Number(note[1])}.xml`;
  else{
   const canonical=old.match(/^(ppt\/(?:charts|slideMasters|slideLayouts|notesMasters|theme)\/)(chart|slideMaster|slideLayout|notesMaster|theme)(\d+)\.xml$/);
   if(canonical){const key=canonical[1]+canonical[2],n=(counters.get(key)||0)+1;counters.set(key,n);dest=key+n+'.xml';}
   else dest=path.posix.join(path.posix.dirname(old),`s${String(sec.id).padStart(2,'0')}-`+path.posix.basename(old));
  }
  map.set(old,dest);
 }
 for(const [old,dest] of map){if(old==='ppt/presentation.xml')continue;
  const original=await zip.file(old).async('nodebuffer');let b=original;
  if(sec.id===0&&old==='docProps/app.xml'){
   const metadata=parse(b);for(const e of root(metadata).elements??[]){if(['Slides','Notes'].includes(e.name?.split(':').pop()))e.elements=[{type:'text',text:'240'}];}b=encode(metadata);
  }
  if(merged.file(dest))throw Error('Part collision: '+dest);merged.file(dest,b);
  manifest.push({section:sec.id,source_part:old,part:dest,source_sha256:sha(original),sha256:sha(b),byte_preserved:sha(original)===sha(b),bytes:b.length});
  const rel=zip.file(relpath(old));if(rel){const tree=parse(await rel.async('nodebuffer'));
   for(const item of root(tree).elements??[]){if(item.type!=='element'||item.attributes.TargetMode==='External')continue;
    const target=resolve(old,item.attributes.Target);if(!map.has(target))throw Error('Unmapped relationship '+old+' -> '+target);
    item.attributes.Target=relative(dest,map.get(target));
   }
   merged.file(relpath(dest),encode(tree));
  }
 }
 const ct=root(parse(await zip.file('[Content_Types].xml').async('nodebuffer')));
 for(const e of ct.elements??[]){if(e.type!=='element')continue;
  if(e.name==='Default'){const key=e.attributes.Extension,type=e.attributes.ContentType;if(defaults.has(key)&&defaults.get(key)!==type)throw Error('Conflicting default '+key);defaults.set(key,type);}
  if(e.name==='Override'){const old=e.attributes.PartName.slice(1);if(map.has(old))overrides.set('/'+map.get(old),e.attributes.ContentType);}
 }
 sources.push({section:sec.id,title:sec.title,revision:sec.revision,pptx:sec.pptx,sha256:sec.sha256,first_page:offset+1,last_page:offset+sec.page_budget,pages:sec.page_budget,zip});maps.push(map);offset+=sec.page_budget;
}
if(offset!==240)throw Error('Expected 240 slides');
const pres=parse(await sources[0].zip.file('ppt/presentation.xml').async('nodebuffer')),pr=root(pres);
pr.attributes['xmlns:r']='http://schemas.openxmlformats.org/officeDocument/2006/relationships';
const relationships=[],masterIds=[],noteIds=[],slideIds=[];let rid=0,masterId=2147483648;
for(let i=0;i<sources.length;i++){
 const src=sources[i],map=maps[i];const rs=root(parse(await src.zip.file('ppt/_rels/presentation.xml.rels').async('nodebuffer')));
 const oldToNew=new Map();
 for(const e of rs.elements??[]){if(e.type!=='element')continue;
  const type=e.attributes.Type,isSlide=type.endsWith('/slide'),isMaster=type.endsWith('/slideMaster'),isNote=type.endsWith('/notesMaster');
  if(i!==0&&!isSlide&&!isMaster&&!isNote)continue;
  const id='rId'+(++rid);oldToNew.set(e.attributes.Id,id);
  const attrs={...e.attributes,Id:id};if(attrs.TargetMode!=='External'){const target=resolve('ppt/presentation.xml',attrs.Target);if(!map.has(target))throw Error('Unmapped presentation target '+target);attrs.Target=relative('ppt/presentation.xml',map.get(target));}
  relationships.push(child('Relationship',attrs));
  if(isMaster)masterIds.push(child('p:sldMasterId',{id:String(masterId++),'r:id':id}));
  if(isNote)noteIds.push(child('p:notesMasterId',{'r:id':id}));
 }
 const sp=root(parse(await src.zip.file('ppt/presentation.xml').async('nodebuffer')));
 const list=sp.elements.find(e=>e.name==='p:sldIdLst');
 for(const e of list.elements??[]){if(e.name!=='p:sldId')continue;slideIds.push(child('p:sldId',{id:String(256+slideIds.length),'r:id':oldToNew.get(e.attributes['r:id'])}));}
 if(i===0){for(const e of pr.elements??[]){if(!['p:sldMasterIdLst','p:notesMasterIdLst','p:sldIdLst'].includes(e.name)&&e.attributes?.['r:id'])e.attributes['r:id']=oldToNew.get(e.attributes['r:id']);}}
}
for(const [name,items] of [['p:sldMasterIdLst',masterIds],['p:notesMasterIdLst',noteIds],['p:sldIdLst',slideIds]]){
 const el=pr.elements.find(e=>e.name===name);if(el)el.elements=items;else if(items.length)pr.elements.splice(name==='p:notesMasterIdLst'?1:0,0,child(name,{},items));
}
merged.file('ppt/presentation.xml',encode(pres));
merged.file('ppt/_rels/presentation.xml.rels',encode({elements:[child('Relationships',{xmlns:'http://schemas.openxmlformats.org/package/2006/relationships'},relationships)]}));
const rootrels=parse(await sources[0].zip.file('_rels/.rels').async('nodebuffer'));
for(const e of root(rootrels).elements??[]){if(e.type!=='element'||e.attributes.TargetMode==='External')continue;e.attributes.Target=maps[0].get(e.attributes.Target.replace(/^\//,''));if(!e.attributes.Target)throw Error('Unmapped root target');}
merged.file('_rels/.rels',encode(rootrels));
merged.file('[Content_Types].xml',encode({elements:[child('Types',{xmlns:'http://schemas.openxmlformats.org/package/2006/content-types'},[...defaults].map(([Extension,ContentType])=>child('Default',{Extension,ContentType})).concat([...overrides].map(([PartName,ContentType])=>child('Override',{PartName,ContentType}))))]}));
// All source slide, note, chart, workbook and media bytes are still untouched.
const candidate=path.join(stage,'candidate.pptx');await fs.writeFile(candidate,await merged.generateAsync({type:'nodebuffer',compression:'DEFLATE'}));
const sourceSummary=sources.map(({zip,...s})=>s);
await fs.writeFile(path.join(stage,'assembly-manifest.json'),JSON.stringify({revision:REV,source_sections:sourceSummary,slides:240,preserved_parts:manifest,scope:'Repackage current section decks; slide XML, notes, charts and workbooks are copied, internal relationship targets are renamed. No scientific revalidation or model execution.'},null,2));
await finalizePresentation({workspaceDir:R,candidatePath:candidate,finalPath:path.join(R,'output',`高校科研AI培训课程_全课240页_${REV}.pptx`),pythonExecutable:'C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-heading-fit'],fontPolicy:{basis:'design',families:['Microsoft YaHei']},explicitTotalSlideCount:240,verifyArtifactToolImport:true,receiptPath:path.join(stage,'validation.json')});
await fs.copyFile(path.join(stage,'assembly-manifest.json'),path.join(R,'assembly-manifest.json'));
await fs.copyFile(path.join(stage,'validation.json'),path.join(R,'validation.json'));
console.log('FINAL',REV,'240 native editable slides');
