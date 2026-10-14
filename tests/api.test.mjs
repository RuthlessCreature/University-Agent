import { test } from "node:test";
import assert from "node:assert/strict";
import {validate,handle} from "../src/index.js";
const env={MINIMAX_API_KEY:"mock",WORKSHOP_ACCESS_TOKEN:"classroom",MINIMAX_MODEL:"MiniMax-M3"};
test("workflow catalog",async()=>{const r=await handle(new Request("https://example.test/api/workflows"),env);assert.equal(r.status,200);assert.equal(Object.keys((await r.json()).workflows).length,5)});
test("input check",()=>{assert.ok(validate({workflow:"grant",step:"intake",material:"short"}));assert.equal(validate({workflow:"grant",step:"intake",material:"合法脱敏的科研材料".repeat(12)}),null)});
test("token required",async()=>{const r=await handle(new Request("https://example.test/api/run",{method:"POST",body:"{}"}),env);assert.equal(r.status,401)});
test("model response mock",async()=>{const body={workflow:"grant",step:"intake",material:"经过授权的科研项目描述，现根据本年度指南整理项目申报书结构和已有团队研究成果，并检查材料完整性。"};const fake=async()=>new Response(JSON.stringify({choices:[{message:{content:"缺少申报指南，需要补齐"}}]}),{status:200});const r=await handle(new Request("https://example.test/api/run",{method:"POST",headers:{"X-Workshop-Key":"classroom"},body:JSON.stringify(body)}),env,fake);assert.equal(r.status,200)});
