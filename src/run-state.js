// Durable Object stores workflow state only. It does not parse files or execute Python.
const reply=(x,status=200)=>Response.json(x,{status});
export class ResearchRun {
 constructor(ctx){this.ctx=ctx;}
 async fetch(req){
  if(req.method==='GET'){const run=await this.ctx.storage.get('run');return run?reply(run):reply({error:'run_not_found'},404);}
  let b;try{b=await req.json();}catch{return reply({error:'invalid_json'},400);}
  return this.ctx.storage.transaction(async storage=>{
   const current=await storage.get('run');
   if(!current){
    if(b.action!=='create'||!['grant','paper','patent','figures','closeout'].includes(b.workflow))return reply({error:'invalid_create'},422);
    if(typeof b.input_sha256!=='string'||!/^[0-9a-f]{64}$/.test(b.input_sha256))return reply({error:'input_hash_required'},422);
    const run={id:b.id,workflow:b.workflow,input_sha256:b.input_sha256,status:'received',version:1,history:[{action:'create',at:new Date().toISOString()}],execution:'state-only; no tool executed'};
    await storage.put('run',run);return reply(run,201);
   }
   if(b.version!==current.version)return reply({error:'version_conflict',version:current.version},409);
   const allowed={received:['running','failed'],running:['review_required','failed'],review_required:['approved','failed'],approved:['draft_ready','failed'],failed:['received'],draft_ready:[]};
   if(!allowed[current.status]?.includes(b.status))return reply({error:'invalid_transition'},422);
   if(b.status==='approved'&&(!b.reviewer||b.reviewed_input_sha256!==current.input_sha256))return reply({error:'reviewer_and_matching_hash_required'},422);
   if(b.status==='draft_ready'&&(!b.artifact_sha256||!/^[0-9a-f]{64}$/.test(b.artifact_sha256)))return reply({error:'artifact_hash_required'},422);
   const next={...current,status:b.status,version:current.version+1,history:[...current.history,{action:b.status,at:new Date().toISOString(),reviewer:b.reviewer||null}]};
   if(b.artifact_sha256)next.artifact_sha256=b.artifact_sha256;
   await storage.put('run',next);return reply(next);
  });
 }
}
export async function runStateRoute(req,env){
 if(!env.WORKSHOP_ACCESS_TOKEN)return reply({error:'WORKSHOP_ACCESS_TOKEN required'},503);
 if(req.headers.get('X-Workshop-Key')!==env.WORKSHOP_ACCESS_TOKEN)return reply({error:'unauthorized'},401);
 if(!env.RUNS)return reply({error:'Durable Object RUNS binding unavailable; not deployed'},503);
 const path=new URL(req.url).pathname;
 if(path==='/api/runs'&&req.method==='POST'){
  let b;try{b=await req.json();}catch{return reply({error:'invalid_json'},400);}
  const id=crypto.randomUUID();const stub=env.RUNS.get(env.RUNS.idFromName(id));
  return stub.fetch(new Request('https://run.internal',{method:'POST',body:JSON.stringify({...b,id,action:'create'})}));
 }
 const id=path.slice('/api/runs/'.length);
 if(!/^[0-9a-f-]{36}$/.test(id))return reply({error:'invalid_run_id'},422);
 return env.RUNS.get(env.RUNS.idFromName(id)).fetch(req);
}
