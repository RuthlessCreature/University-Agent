import {test} from 'node:test';
import assert from 'node:assert/strict';
import {unzipSync} from 'fflate';
import {ResearchProject} from '../src/projects.js';
import {EXAMPLES as DOCS} from '../src/generated/examples.js';
import {REPORT_EXAMPLES} from '../src/report-examples.js';
const EXAMPLES={...DOCS,...REPORT_EXAMPLES};
const env={DEEPSEEK_API_KEY:"deepseek-fixture-only",MINIMAX_TOKEN_PLAN_KEY:'automation-test-only',MINIMAX_MODEL:'MiniMax-M3'};
function setup(kind,fail=false){
 const db=new Map();let alarmAt=null,calls=0;
 const storage={get:async key=>structuredClone(db.get(key)),put:async(key,value)=>db.set(key,structuredClone(value)),transaction:async fn=>fn(storage),setAlarm:async time=>alarmAt=time,deleteAlarm:async()=>alarmAt=null};
 const provider=async()=>{calls++;if(fail)throw Error('TEST PROVIDER FAILURE');return Response.json({choices:[{message:{content:JSON.stringify({summary:'TEST FIXTURE node '+calls,sections:EXAMPLES[kind].input.sections,issues:['Test fixture only; not scientific verification'],route:[]})},finish_reason:'stop'}]});};
 const object=new ResearchProject({storage},env,provider);
 return {object,storage,post:body=>object.fetch(new Request('https://project.internal',{method:'POST',body:JSON.stringify(body)})),get:()=>object.fetch(new Request('https://project.internal')).then(r=>r.json()),calls:()=>calls,alarmAt:()=>alarmAt};
}
for(const kind of Object.keys(EXAMPLES))test(kind+' runs all nodes and writes a real artifact without approval requests',async()=>{
 const fixture=setup(kind);
 assert.equal((await fixture.post({...EXAMPLES[kind],id:'test-fixture',action:'create',auto_start:true})).status,201);
 assert(fixture.alarmAt());
 // The platform fires alarms; there are no browser requests or approve actions between nodes.
 for(let i=0;i<12;i++){await fixture.object.alarm();const run=await fixture.storage.get('project');if(run.auto_state==='completed')break;}
 const run=await fixture.get();assert.equal(run.auto_state,'completed');assert.equal(run.status,'draft_ready');assert.equal(run.progress.percent,100);assert(run.progress.nodes.every(node=>node.state==='completed'));assert.equal(fixture.calls(),run.stages.length*2);assert.equal(fixture.alarmAt(),null);assert.equal(run.scientific_signoff,false);
 assert(!run.history.some(item=>item.event==='approved'));
 for(const output of run.outputs){assert.equal(output.completed,true);assert.equal(output.approved,false);assert.equal(output.reviewer,undefined);assert(output.finished_at);}
 const response=await fixture.object.fetch(new Request('https://project.internal/artifact'));assert.equal(response.status,200);const artifact=new Uint8Array(await response.arrayBuffer());
 if(['figures','closeout'].includes(kind)){assert.equal(run.artifact_type,'markdown');assert(new TextDecoder().decode(artifact).includes('节点输出'));}
 else assert(unzipSync(artifact)['word/document.xml']);
});
test('automatic failure retries once then stops, preserving node state',async()=>{
 const fixture=setup('paper',true);await fixture.post({...EXAMPLES.paper,id:'test',action:'create',auto_start:true});
 for(let i=0;i<8;i++)await fixture.object.alarm();
 const run=await fixture.get();assert.equal(fixture.calls(),2);assert.equal(run.auto_state,'failed');assert.equal(run.outputs.length,0);assert(run.progress.nodes.some(node=>node.state==='failed'));assert.equal(fixture.alarmAt(),null);
});
test('an interrupted background node is recovered and completed automatically',async()=>{
 const fixture=setup('paper');await fixture.post({...EXAMPLES.paper,id:'test',action:'create',auto_start:true});
 const first=await fixture.storage.get('project');await fixture.storage.put('project',{...first,status:'running',auto_node:'intake',started_at:new Date(Date.now()-400000).toISOString()});
 for(let i=0;i<15;i++){await fixture.object.alarm();if((await fixture.storage.get('project')).auto_state==='completed')break;}
 assert.equal((await fixture.get()).auto_state,'completed');
});
test('previous manual output can resume automatically without inventing a reviewer',async()=>{
 const fixture=setup('paper');let run=await(await fixture.post({...EXAMPLES.paper,id:'test',action:'create'})).json();
 run=await(await fixture.post({action:'execute',version:run.version})).json();assert.equal(run.status,'review_required');
 assert.equal((await fixture.post({action:'start-auto',version:run.version})).status,200);
 for(let i=0;i<10;i++)await fixture.object.alarm();
 run=await fixture.get();assert.equal(run.auto_state,'completed');assert.equal(run.outputs[0].approved,false);assert.equal(run.outputs[0].reviewer,undefined);
});
