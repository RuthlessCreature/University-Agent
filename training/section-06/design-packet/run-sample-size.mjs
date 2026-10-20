// Run the complete R source in the already prepared local official WebR runtime.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const R=path.dirname(fileURLToPath(import.meta.url));
const localModule=path.join(R,'../.build/webr-runtime/package/dist/webr.mjs');
const localExists=await fs.access(localModule).then(()=>true,()=>false);
const modulePath=process.env.WEBR_MODULE||(localExists?localModule:path.join(R,'../../section-07/.build/webr-runtime/package/dist/webr.mjs'));
const provenancePath=path.join(R,'r-runtime-provenance.json');
const provenance=JSON.parse(await fs.readFile(provenancePath,'utf8'));
const hash=b=>createHash('sha256').update(b).digest('hex');
const wasm=hash(await fs.readFile(path.join(path.dirname(modulePath),'R.wasm')));
if(wasm!==provenance.R_wasm_sha256)throw Error('R runtime hash differs');
const {WebR}=await import(pathToFileURL(modulePath).href);
const w=new WebR();await w.init();
try{
 const script=await fs.readFile(path.join(R,'sample-size.R'));
 await w.FS.mkdir('/design');await w.FS.writeFile('/design/sample-size.R',new Uint8Array(script));
 await w.evalRVoid('setwd("/design"); source("sample-size.R",encoding="UTF-8")');
 const out=path.join(R,'r-output');await fs.mkdir(out,{recursive:true});const files=[];
 for(const name of ['sample-size.csv','resource-capacity.csv','session-info.txt']){
  const b=await w.FS.readFile('/design/r-output/'+name);await fs.writeFile(path.join(out,name),b);files.push({name,sha256:hash(b)});
 }
 const result={executed_at:new Date().toISOString(),actual_execution:true,engine:'official WebR 0.6.0 in local Node.js',runtime:await w.evalRString('R.version.string'),R_wasm_sha256:wasm,script_sha256:hash(script),assumptions_status:'教学假设；没有预研究估计依据',participant_data_used:false,desktop_R_or_RStudio_used:false,model_called:false,files,scope:'实际运行独立等样本双侧t检验功效计算、独立数值积分核对及工作量算术；不证明拟议研究已获批准、可招募或参数真实。'};
 await fs.writeFile(path.join(out,'run.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
}finally{w.close();}
