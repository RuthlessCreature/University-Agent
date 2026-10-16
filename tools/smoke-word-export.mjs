// Real execution of the Worker DOCX tool in Node; no model or Cloudflare call.
import fs from 'node:fs';import path from 'node:path';
import {EXAMPLES} from '../src/generated/examples.js';
import {SKILL_PACK} from '../src/generated/skill-pack.js';
import {fillTemplate,digest} from '../src/word-export.js';
const root=path.resolve(import.meta.dirname,'..');const results=[];
for(const [kind,example] of Object.entries(EXAMPLES)){
 const template=Uint8Array.from(Buffer.from(example.template_base64,'base64'));
 const input=example.input,input_sha256=await digest(new TextEncoder().encode(JSON.stringify(input)));
 const docx=fillTemplate(template,input.sections,{title:input.title,material_type:input.material_type,skill_commit:SKILL_PACK.commit,input_sha256,issues:[...(input.issues||[]).map(x=>x.issue),'本次仅执行DOCX工具，模型未调用，未获得科学签核'],sources:input.sources});
 const folder=path.join(root,'training/demos',kind,'worker-tool');fs.mkdirSync(folder,{recursive:true});const filename=kind+'-template-tool-check.docx';fs.writeFileSync(path.join(folder,filename),docx);
 const record={kind,environment:'Node: actual Worker word-export.js function',model_called:false,cloud_called:false,scientific_signoff:false,input_sha256,template_sha256:await digest(template),artifact:filename,artifact_sha256:await digest(docx),bytes:docx.length};fs.writeFileSync(path.join(folder,'run.json'),JSON.stringify(record,null,2)+'\n');results.push(record);
}
fs.writeFileSync(path.join(root,'evidence/worker-word-tool-checks.json'),JSON.stringify(results,null,2)+'\n');console.log('3 actual Worker DOCX tool executions completed in Node; no model or cloud call');
