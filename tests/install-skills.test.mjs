import {test} from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {installSkills} from "../tools/install-skills.mjs";
test("copies valid Skills to Codex directory",()=>{
 const temp=fs.mkdtempSync(path.join(os.tmpdir(),"skills-test-"));
 try {
   const root=path.join(temp,"source");
   const folder=path.join(root,"skills/core/test-skill");
   fs.mkdirSync(folder,{recursive:true});
   fs.writeFileSync(path.join(folder,"SKILL.md"),"---\nname: test-skill\n---\n# test");
   fs.writeFileSync(path.join(root,"skills-manifest.json"),JSON.stringify({
     skills:[{id:"test-skill",path:"skills/core/test-skill/SKILL.md"}]
   }));
   const target=path.join(temp,"dest");
   const dry=installSkills({source:root,target,dryRun:true});
   assert.equal(dry[0].status,"dry-run");
   assert.equal(fs.existsSync(target),false);
   const real=installSkills({source:root,target});
   assert.equal(real[0].status,"installed");
   assert.equal(fs.existsSync(path.join(target,"test-skill/SKILL.md")),true);
   assert.equal(installSkills({source:root,target})[0].status,"exists");
   assert.throws(()=>installSkills({source:root,target,only:["missing"]}));
 } finally {fs.rmSync(temp,{recursive:true,force:true});}
});
