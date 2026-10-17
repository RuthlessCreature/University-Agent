import {chromium} from 'file:///C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
import fs from 'node:fs/promises';
const r='E:/20261024/University-Agent/training/section-05';await fs.mkdir(r+'/assets',{recursive:true});
const b=await chromium.launch({headless:true});const page=await b.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1});
for(const [name,url] of [['pubmed','https://pubmed.ncbi.nlm.nih.gov/?term=%22generative+AI%22+learning'],['elicit','https://support.elicit.com/en/articles/17220397-where-did-find-papers-extract-data-and-chat-with-papers-go']]){
 try{await page.goto(url,{waitUntil:'domcontentloaded',timeout:45000});await page.screenshot({path:r+'/assets/'+name+'-detail.png',clip:name==='pubmed'?{x:220,y:145,width:1000,height:550}:{x:220,y:310,width:1000,height:290}});await fs.writeFile(r+'/.reference-cache/'+name+'-browser.txt',await page.locator('body').innerText());console.log(name,await page.title());}catch(e){console.log(name,e.message.slice(0,100));}
}
await b.close();
