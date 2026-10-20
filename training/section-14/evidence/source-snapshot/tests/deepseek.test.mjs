import {test} from 'node:test';
import assert from 'node:assert/strict';
import {modelConfig,callModel} from '../src/model.js';
import {validateEdit,editingMessages} from '../src/writing.js';
import {selectRelevant} from '../src/research-providers.js';
test('active provider requires DeepSeek and cannot fall back to retained MiniMax secrets',()=>{
 assert.throws(()=>modelConfig({MINIMAX_TOKEN_PLAN_KEY:'retained'}),/DEEPSEEK_API_KEY/);assert.throws(()=>modelConfig({MODEL_PROVIDER:'minimax',DEEPSEEK_API_KEY:'fixture'}),/停用/);assert.equal(modelConfig({DEEPSEEK_API_KEY:'fixture'}).model,'deepseek-flash');assert.throws(()=>modelConfig({DEEPSEEK_API_KEY:'fixture',DEEPSEEK_API_BASE:'https://other.invalid'}));
});
test('DeepSeek requests official Flash with reasoning and JSON, without MiniMax parameters',async()=>{
 let call;const result=await callModel({DEEPSEEK_API_KEY:'fixture'},[{role:'user',content:'JSON fixture'}],async(url,options)=>{call={url,options};return Response.json({choices:[{message:{content:'{}'},finish_reason:'stop'}]});},{json:true});
 const body=JSON.parse(call.options.body);assert.equal(call.url,'https://api.deepseek.com/chat/completions');assert.equal(body.model,'deepseek-flash');assert.equal(body.reasoning_effort,'high');assert.equal(body.response_format.type,'json_object');assert(!('reasoning_split'in body));assert.equal(result.provider,'deepseek');
});
test('editing preserves numeric facts, template chapters, and citations',()=>{
 const before={summary:'本节点已完成审查',sections:[{title:'Results',content:'342条记录，均值3700.7 g。',source_ids:['D1']}],issues:['缺少标准差'],route:[]};const after=structuredClone(before);after.summary='还缺标准差。';assert.equal(validateEdit(before,after),after);after.sections[0].content='343条记录，均值3700.7 g。';assert.throws(()=>validateEdit(before,after),/数字/);after.sections=structuredClone(before.sections);after.sections[0].source_ids=['D2'];assert.throws(()=>validateEdit(before,after),/来源/);assert(editingMessages(before)[0].content.includes('不要汇报执行过程'));
});
test('relevance selection can only reorder and select supplied records',async()=>{
 const items=[{title:'Related method',content:'Screening',url:'https://example.org/1'},{title:'Unrelated education',content:'Learning',url:'https://example.org/2'},{title:'Direct study',content:'Screening',url:'https://example.org/3'}];
 const result=await selectRelevant(items,{query:'active learning review screening',mode:'papers'},{DEEPSEEK_API_KEY:'fixture'},async()=>Response.json({choices:[{message:{content:'{"indices":[2,0]}'}}]}));
 assert.deepEqual(result.items,[items[2],items[0]]);assert.equal(result.method,'deepseek-relevance-selection');
 const invalid=await selectRelevant(items,{query:'topic'},{DEEPSEEK_API_KEY:'fixture'},async()=>Response.json({choices:[{message:{content:'{"indices":[999]}'}}]}));assert.deepEqual(invalid.items,items);assert.match(invalid.note,/未知编号/);
});
