// Active transport. MiniMax remains in minimax.js for an explicit future switch only.
export function modelConfig(env){
 const provider=env.MODEL_PROVIDER||'deepseek';
 if(provider!=='deepseek')throw Error('当前工作台只启用 DeepSeek，MiniMax 已停用。');
 if(!env.DEEPSEEK_API_KEY)throw Error('请先用命令行配置 DEEPSEEK_API_KEY，然后重新开始任务。');
 const base=(env.DEEPSEEK_API_BASE||'https://api.deepseek.com').replace(/\/$/,'');
 if(!['https://api.deepseek.com','https://api.deepseek.com/v1'].includes(base))throw Error('DeepSeek 接口地址必须使用官方地址。');
 const model=env.DEEPSEEK_MODEL||'deepseek-flash';
 if(model!=='deepseek-flash')throw Error('当前工作台使用 DeepSeek-V4.1-Flash（deepseek-flash）。');
 return {provider,key:env.DEEPSEEK_API_KEY,base,model,billing_mode:'deepseek-api'};
}
export async function callModel(env,messages,fetcher=fetch,options={}){
 const config=modelConfig(env);
 const response=await fetcher(config.base+'/chat/completions',{method:'POST',headers:{'content-type':'application/json',Authorization:'Bearer '+config.key},body:JSON.stringify({model:config.model,messages,max_tokens:options.max_tokens||12000,thinking:{type:options.planning?'disabled':'enabled'},reasoning_effort:options.planning?'none':'high',...(options.json?{response_format:{type:'json_object'}}:{})}),signal:AbortSignal.timeout(options.timeout_ms||(options.planning?25000:150000))});
 if(!response.ok)throw Error('DeepSeek 请求失败（HTTP '+response.status+'），请检查 Key、余额或服务状态。');
 const data=await response.json(),choice=data.choices?.[0];
 if(choice?.finish_reason==='length')throw Error('生成达到长度上限，该节点将重新尝试。');
 const content=choice?.message?.content;
 if(typeof content!=='string'||!content.trim())throw Error('DeepSeek 未返回正文。');
 return {text:content,model:config.model,provider:config.provider,billing_mode:config.billing_mode,usage:data.usage||null};
}
