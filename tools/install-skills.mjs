#!/usr/bin/env node
/**
 * Install the sibling University-Skills catalog into Codex .agents/skills.
 * Explicit local paths, no remote code execution, no automatic overwrites.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export function installSkills({ source, target, only = [], dryRun = false, force = false }) {
  const root = path.resolve(source);
  const dest = path.resolve(target);
  const manifestPath = path.join(root, "skills-manifest.json");
  if (!fs.existsSync(manifestPath)) throw new Error("Missing skills-manifest.json: " + manifestPath);
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  const requested = new Set(only);
  const records = [];
  const seen = new Set();
  for (const item of manifest.skills ?? []) {
    if (!/^[a-z0-9][a-z0-9-]*$/.test(item.id)) throw new Error("Invalid skill name");
    if (requested.size && !requested.has(item.id)) continue;
    seen.add(item.id);
    const skillFolder = path.resolve(root, path.dirname(item.path));
    if (!skillFolder.startsWith(root + path.sep)) throw new Error("Manifest path outside source");
    const skillMd = path.join(skillFolder, "SKILL.md");
    if (!fs.existsSync(skillMd)) throw new Error("Missing SKILL.md for " + item.id);
    const body = fs.readFileSync(skillMd, "utf8");
    if (!body.split(/\r?\n/).includes("name: " + item.id)) throw new Error("Invalid skill header " + item.id);
    const installed = path.join(dest, item.id);
    if (fs.existsSync(installed) && !force) {
      records.push({id:item.id,status:"exists",target:installed});
      continue;
    }
    if (!dryRun) {
      fs.mkdirSync(dest, {recursive:true});
      if (fs.existsSync(installed)) fs.rmSync(installed,{recursive:true,force:true});
      fs.cpSync(skillFolder,installed,{recursive:true,dereference:false});
    }
    records.push({id:item.id,status:dryRun?"dry-run":"installed",target:installed});
  }
  const missing = [...requested].filter(x => !seen.has(x));
  if (missing.length) throw new Error("Unknown requested skills: " + missing.join(", "));
  return records;
}
const self = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (self) {
  const args = process.argv.slice(2);
  const arg = (name, defaultValue) => {
    const pos = args.indexOf(name);
    return pos >= 0 ? args[pos+1] : defaultValue;
  };
  const source = arg("--source", path.resolve("../University-Skills"));
  const target = arg("--target", path.resolve(".agents/skills"));
  const only = arg("--only", "").split(",").map(x=>x.trim()).filter(Boolean);
  try {
    const result = installSkills({
      source, target, only,
      dryRun: args.includes("--dry-run"),
      force: args.includes("--force")
    });
    process.stdout.write(JSON.stringify({count:result.length,items:result},null,2)+"\n");
  } catch (error) {
    process.stderr.write("Installation failed: " + error.message + "\n");
    process.exitCode = 1;
  }
}
