import fs from 'node:fs';
const html=fs.readFileSync(new URL('../src/workbench.html',import.meta.url),'utf8');
fs.writeFileSync(new URL('../src/ui.js',import.meta.url),'// Generated from workbench.html\nexport const HTML='+JSON.stringify(html)+';\n');
console.log('Built workbench UI');
