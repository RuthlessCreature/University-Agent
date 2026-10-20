const put=async(object,update)=>object.ctx.storage.transaction(async storage=>{const run=await storage.get('project');if(!run)return null;const next=update(run);await storage.put('project',next);return next;});
export function progress(run,input,outputs){
 const nodes=[];
 if(input.research_request)nodes.push({id:'research',title:'联网检索',type:'research',state:input.research_evidence?'completed':run.status==='searching'?'running':run.auto_node==='research'&&run.status==='failed'?'failed':'pending',finished_at:input.research_evidence?.retrieved_at,summary:input.research_evidence?'取得 '+input.research_evidence.results.length+' 项资料，已保存来源和读取范围。':null});
 for(const [i,stage] of run.stages.entries()){
  const output=outputs.find(x=>x.stage===stage.id);
  const state=output?'completed':i===run.cursor&&run.status==='running'?'running':i===run.cursor&&run.status==='failed'&&run.auto_node!=='research'?'failed':'pending';
  nodes.push({id:stage.id,title:stage.title,type:'model',index:i,state,started_at:output?.started_at||(state==='running'?run.started_at:null),finished_at:output?.finished_at,summary:output?.content.summary||null});
 }
 nodes.push({id:'artifact',title:run.workflow==='figures'?'整理绘图方案':run.workflow==='closeout'?'导出结题草稿':'生成 Word',type:'artifact',state:run.status==='draft_ready'?'completed':run.auto_node==='artifact'&&run.status==='failed'?'failed':run.auto_node==='artifact'&&run.auto_state==='running'?'running':'pending',summary:run.artifact_sha256?'结果文件已生成，可以下载。':null});
 const done=nodes.filter(n=>n.state==='completed').length;
 return {nodes,completed:done,total:nodes.length,percent:Math.round(done/nodes.length*100),current_node:nodes.find(n=>n.state==='running')?.id||nodes.find(n=>n.state==='failed')?.id||nodes.find(n=>n.state==='pending')?.id||'artifact'};
}

// Every alarm runs one real node. Another alarm continues after the result is persisted.
export async function advanceAutomatic(object){
 const storage=object.ctx.storage;
 try{
  let run=await storage.get('project');
  if(!run?.auto_mode||['completed','failed'].includes(run.auto_state)){await storage.deleteAlarm();return;}
  if(run.status==='draft_ready'){await put(object,r=>({...r,auto_state:'completed',finished_at:new Date().toISOString()}));await storage.deleteAlarm();return;}
  if(['running','searching'].includes(run.status)){
   const wake=Date.parse(run.started_at)+305000;
   if(Date.now()<wake){await storage.setAlarm(wake);return;}
   await object.fetch(new Request('https://project.internal',{method:'POST',body:JSON.stringify({action:'recover',version:run.version})}));
   await storage.setAlarm(Date.now()+250);return;
  }
  if(run.status==='failed'){
   const key=run.auto_node||'stage-'+run.cursor,attempt=run.auto_retries?.[key]||0;
   if(attempt>=1){await put(object,r=>({...r,auto_state:'failed',finished_at:new Date().toISOString()}));await storage.deleteAlarm();return;}
   await put(object,r=>({...r,status:r.cursor===r.stages.length?'export_ready':'ready',auto_retries:{...r.auto_retries,[key]:attempt+1},version:r.version+1,history:[...r.history,{event:'automatic_retry',stage:key,at:new Date().toISOString()}]}));
   await storage.setAlarm(Date.now()+2000);return;
  }
  const materials=await storage.get('input');
  const action=materials.input.research_request&&!materials.input.research_evidence?'research':run.cursor<run.stages.length?'execute':'export';
  const key=action==='research'?'research':action==='export'?'artifact':run.stages[run.cursor].id;
  run=await put(object,r=>({...r,auto_node:key}));
  await storage.setAlarm(Date.now()+305000); // Restart watchdog, without relying on a browser remaining open.
  const response=await object.fetch(new Request('https://project.internal',{method:'POST',body:JSON.stringify({action,version:run.version})}));
  if(!response.ok){const result=await response.json();await put(object,r=>['failed','draft_ready','running','searching'].includes(r.status)?r:{...r,status:'failed',last_error:result.error||'节点执行失败',version:r.version+1});}
  const latest=await storage.get('project');
  if(latest.status==='draft_ready'){await put(object,r=>({...r,auto_state:'completed',finished_at:new Date().toISOString()}));await storage.deleteAlarm();}
  else await storage.setAlarm(Date.now()+250);
 }catch(error){
  await put(object,r=>({...r,status:'failed',auto_state:'failed',last_error:error.message,version:r.version+1,finished_at:new Date().toISOString()}));
  await storage.deleteAlarm();
 }
}
