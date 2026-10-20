import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {unzipSync,strFromU8} from 'fflate';
import {ResearchProject,validateInput,parseCandidate,stageMessages} from '../src/projects.js';
import {EXAMPLES} from '../src/generated/examples.js';
import {SKILL_PACK} from '../src/generated/skill-pack.js';
import {modelConfig,callModel} from '../src/minimax.js';
import {fillTemplate,digest} from '../src/word-export.js';
const env={MINIMAX_TOKEN_PLAN_KEY:'test-fixture-not-a-live-key',MINIMAX_MODEL:'MiniMax-M3'};
function fixture(provider){
 const db=new Map(),storage={get:async k=>structuredClone(db.get(k)),put:async(k,v)=>db.set(k,structuredClone(v)),transaction:async fn=>fn(storage)};
 return {object:new ResearchProject({storage},env,provider),storage};
}
const post=async(object,b)=>object.fetch(new Request('https://project.test',{method:'POST',body:JSON.stringify(b)}));
const create=async object=>(await post(object,{...EXAMPLES.grant,id:'test-fixture',action:'create'})).json();
test('24 installed Skill files match the exact Worker prompt bytes',()=>{
 assert.equal(Object.keys(SKILL_PACK.skills).length,24);
 for(const [id,skill] of Object.entries(SKILL_PACK.skills)){
  const bytes=fs.readFileSync(new URL('../.agents/skills/'+id+'/SKILL.md',import.meta.url));
  assert.equal(bytes.toString('utf8'),skill.content);
  assert.equal(createHash('sha256').update(bytes).digest('hex'),skill.sha256);
 }
});
test('Token Plan never silently falls back to an ordinary API key',()=>{
 assert.throws(()=>modelConfig({MINIMAX_API_KEY:'payg-fixture'}));
 assert.equal(modelConfig(env).base,'https://api.minimax.cn/v1');
 assert.equal(modelConfig(env).model,'MiniMax-M3');
 assert.throws(()=>modelConfig({...env,MINIMAX_API_BASE:'https://other.invalid/v1'}));
});
test('model transport fixture uses the requested M3 and subscription key',async()=>{
 let request;const provider=async(url,options)=>{request={url,options};return Response.json({choices:[{message:{content:'fixture only'},finish_reason:'stop'}],usage:{total_tokens:9}});};
 const result=await callModel(env,[{role:'user',content:'fixture'}],provider);
 assert.equal(request.url,'https://api.minimax.cn/v1/chat/completions');
 assert.equal(JSON.parse(request.options.body).model,'MiniMax-M3');assert.equal(result.usage.total_tokens,9);
});
test('input rejects changed guidelines and unknown source references',()=>{
 const value=structuredClone(EXAMPLES.grant);value.guide.requirements[0].text='changed';assert.throws(()=>validateInput(value.input,value.guide));
 const other=structuredClone(EXAMPLES.grant);other.input.sections[0].source_ids=['missing'];assert.throws(()=>validateInput(other.input,other.guide));
});
test('candidate rejects omitted template chapters and invented source IDs',()=>{
 assert.throws(()=>parseCandidate(JSON.stringify({summary:'fixture',issues:[],sections:[{title:'wrong',content:'text',source_ids:['INPUT-01']}]}),EXAMPLES.grant.input));
 const candidate={summary:'fixture',issues:[],sections:structuredClone(EXAMPLES.grant.input.sections)};candidate.sections[0].source_ids=['fake'];assert.throws(()=>parseCandidate(JSON.stringify(candidate),EXAMPLES.grant.input));
});
test('stage prompt contains full canonical Skill content',()=>{
 const stage={id:'template',title:'要求映射',skill:'grant-template',intent:'test'};
 const messages=stageMessages(EXAMPLES.grant.input,EXAMPLES.grant.guide,stage,[]);
 assert.ok(messages[0].content.includes(SKILL_PACK.skills['grant-template'].content));
});
test('actual DOCX template export preserves paragraphs and escapes text',()=>{
 const example=structuredClone(EXAMPLES.grant);example.input.sections[0].content='<A&B>\n第二行';
 const bytes=fillTemplate(Uint8Array.from(Buffer.from(example.template_base64,'base64')),example.input.sections,{material_type:'teaching-simulation',skill_commit:SKILL_PACK.commit,input_sha256:'fixture',issues:['未完成科学审查'],sources:example.input.sources});
 const files=unzipSync(bytes),xml=strFromU8(files['word/document.xml']);assert.ok(xml.includes('&lt;A&amp;B&gt;'));assert.ok(xml.includes('第二行'));assert.ok(xml.includes('未完成科学审查'));assert.ok(!xml.includes('{{立项依据}}'));
 assert.throws(()=>fillTemplate(new Uint8Array([1,2,3]),[],{}));
});
test('project blocks export and skipped approval before any model call',async()=>{
 const {object}=fixture(()=>{throw Error('must not call');});await create(object);
 assert.equal((await post(object,{action:'export',version:1})).status,409);
 assert.equal((await post(object,{action:'approve',version:1,reviewer:'fixture'})).status,422);
 assert.equal((await post(object,{action:'execute',version:0})).status,409);
});
test('provider fixture drives actual state writes and Word bytes, without claiming a live model',async()=>{
 const provider=async()=>Response.json({choices:[{message:{content:JSON.stringify({summary:'TEST FIXTURE, NOT LIVE MODEL',sections:EXAMPLES.grant.input.sections,issues:['科研内容尚未完成专业核查']})},finish_reason:'stop'}]});
 const {object}=fixture(provider);let project=await create(object);
 for(let i=0;i<5;i++){
  let response=await post(object,{action:'execute',version:project.version});assert.equal(response.status,200);project=await response.json();assert.equal(project.status,'review_required');
  assert.equal((await post(object,{action:'execute',version:project.version})).status,409);
  assert.equal((await post(object,{action:'approve',version:project.version,reviewer:'fixture',input_sha256:'wrong',output_sha256:project.output.output_sha256})).status,422);
  response=await post(object,{action:'approve',version:project.version,reviewer:'test-fixture',input_sha256:project.input_sha256,output_sha256:project.output.output_sha256});project=await response.json();
 }
 assert.equal(project.status,'export_ready');project=await(await post(object,{action:'export',version:project.version})).json();assert.equal(project.status,'draft_ready');assert.equal(project.scientific_signoff,false);
 const response=await object.fetch(new Request('https://project.test/word'));const bytes=new Uint8Array(await response.arrayBuffer());assert.ok(unzipSync(bytes)['word/document.xml']);assert.equal(await digest(bytes),project.artifact_sha256);
});
