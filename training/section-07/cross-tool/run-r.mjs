// Run the unchanged .R source in a local WebAssembly R interpreter.
// Set WEBR_MODULE to an installed official webr.mjs; the runtime is not bundled here.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const R=path.dirname(fileURLToPath(import.meta.url));
const modulePath=process.env.WEBR_MODULE||path.join(R,'../.build/webr-runtime/package/dist/webr.mjs');
const {WebR}=await import(pathToFileURL(modulePath).href);
const w=new WebR();await w.init();
const hash=b=>createHash('sha256').update(b).digest('hex');
try{
 await w.FS.mkdir('/course');
 const input=await fs.readFile(path.join(R,'penguins.csv')),script=await fs.readFile(path.join(R,'analysis.R'));
 await w.FS.writeFile('/course/penguins.csv',new Uint8Array(input));
 await w.FS.writeFile('/course/analysis.R',new Uint8Array(script));
 await w.evalRVoid('setwd("/course"); source("analysis.R", encoding="UTF-8")');
 const out=path.join(R,'r-output');await fs.mkdir(out,{recursive:true});
 const files=[];
 for(const name of ['summary.csv','comparison.csv','included_rows.csv','session-info.txt']){
  const b=await w.FS.readFile('/course/r-output/'+name);await fs.writeFile(path.join(out,name),b);files.push({name,sha256:hash(b)});
 }
 const version=await w.evalRString('R.version.string');
 const provenance=JSON.parse(await fs.readFile(path.join(R,'r-runtime-provenance.json'),'utf8'));
 const wasmHash=hash(await fs.readFile(path.join(path.dirname(modulePath),'R.wasm')));
 if(wasmHash!==provenance.R_wasm_sha256)throw Error('R.wasm differs from prepared runtime');
 const report={checked_at:new Date().toISOString(),runtime:version,engine:'official webR 0.6.0 in local Node.js, WebAssembly',desktop_Rscript_used:false,actual_execution:true,remote_model_called:false,input_sha256:hash(input),script_sha256:hash(script),R_wasm_sha256:wasmHash,loader_patch_scope:provenance.patch_scope,files,scope:'Unchanged R source executed in a real local R interpreter; no IBM SPSS execution and no desktop-R application claim.'};
 await fs.writeFile(path.join(out,'run.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({actual_execution:true,version,files:files.length}));
}finally{w.close();}
