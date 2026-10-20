import http from 'node:http';import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath} from 'node:url';import {spawn} from 'node:child_process';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const python=process.env.TRAINING_PYTHON||'C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const port=Number(process.env.TRAINING_PORT||8788);
const server=http.createServer(async(req,res)=>{try{
 const url=new URL(req.url,'http://localhost');
 if(req.method==='GET'&&url.pathname==='/'){res.setHeader('content-type','text/html;charset=utf-8');res.end(await fs.readFile(path.join(root,'tools/local-ui.html')));return;}
 if(req.method==='GET'&&url.pathname==='/health'){res.setHeader('content-type','application/json');res.end(JSON.stringify({mode:'local-file-demo',llm_called:false,cloud_deployed:false}));return;}
 const m=url.pathname.match(/^\/api\/local-run\/(grant|paper|patent)$/);
 if(req.method==='POST'&&m){
  const kind=m[1],dir=path.join(root,'training/demos',kind),args=[path.join(root,'tools/run-local-workflow.py'),'--input',path.join(dir,kind+'.json'),'--template',path.join(dir,'template.docx'),'--output',path.join(dir,'http-output')];
  if(kind==='grant')args.push('--guide',path.join(dir,'guide.json'));
  const child=spawn(python,args,{cwd:root,windowsHide:true});let stdout='',stderr='';child.stdout.on('data',x=>stdout+=x);child.stderr.on('data',x=>stderr+=x);
  child.on('error',()=>{res.statusCode=500;res.end(JSON.stringify({error:'local_executor_unavailable'}));});
  child.on('close',code=>{if(res.writableEnded)return;res.statusCode=code===0?200:422;res.setHeader('content-type','application/json;charset=utf-8');res.end(code===0?stdout:JSON.stringify({error:'local_execution_failed',exit_code:code,detail:stderr.slice(0,1500)}));});return;
 }
 const download=url.pathname.match(/^\/artifacts\/(grant|paper|patent)$/);
 if(req.method==='GET'&&download){const kind=download[1],b=await fs.readFile(path.join(root,'training/demos',kind,'http-output',kind+'-draft.docx'));res.setHeader('content-type','application/vnd.openxmlformats-officedocument.wordprocessingml.document');res.setHeader('content-disposition',`attachment; filename="${kind}-draft.docx"`);res.end(b);return;}
 res.statusCode=404;res.end('Local teaching fixture executor: POST /api/local-run/grant, /paper, /patent. GET /artifacts/grant.');
 }catch{res.statusCode=500;res.end('local request failed');}});
server.listen(port,'127.0.0.1',()=>console.log('Local teaching fixture server http://127.0.0.1:'+port));
