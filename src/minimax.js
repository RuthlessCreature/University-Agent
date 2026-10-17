export function modelConfig(env){
 const mode=env.MINIMAX_BILLING_MODE||'token-plan';
 const key=mode==='token-plan'?(env.MINIMAX_TOKEN_PLAN_KEY||(env.MINIMAX_API_KEY?.startsWith('sk-cp')?env.MINIMAX_API_KEY:null)):env.MINIMAX_API_KEY;
 if(!key)throw Error(mode==='token-plan'?'请配置 MiniMax Token Plan 订阅 Key':'请配置 MiniMax API Key');
 const base=(env.MINIMAX_API_BASE||'https://api.minimax.cn/v1').replace(/\/$/,'');
 const u=new URL(base);
 if(u.protocol!=='https:'||!['api.minimax.cn','api.minimaxi.com','api.minimax.io'].includes(u.hostname)||u.pathname!=='/v1')throw Error('MiniMax 接口地址不在官方兼容地址范围');
 return {key,base,model:env.MINIMAX_MODEL||'MiniMax-M3',billing_mode:mode};
}
export async function callModel(env,messages,fetcher=fetch){
 const config=modelConfig(env),controller=new AbortController();const timer=setTimeout(()=>controller.abort(),90000);
 try{
  const response=await fetcher(config.base+'/chat/completions',{method:'POST',headers:{'content-type':'application/json',Authorization:'Bearer '+config.key},body:JSON.stringify({model:config.model,messages,max_completion_tokens:8192,temperature:0.2,reasoning_split:true}),signal:controller.signal});
  if(!response.ok)throw Error('MiniMax 请求失败 HTTP '+response.status+'，请检查订阅 Key、额度与访问权限');
  const data=await response.json(),choice=data.choices?.[0];
  if(choice?.finish_reason==='length')throw Error('生成达到长度上限，本阶段未完成，可缩短输入后重试');
  const content=choice?.message?.content;
  if(typeof content!=='string'||!content.trim())throw Error('模型没有返回可用正文');
  return {text:content,model:config.model,billing_mode:config.billing_mode,usage:data.usage||null};
 }finally{clearTimeout(timer);}
}
