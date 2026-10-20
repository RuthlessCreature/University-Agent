// Required editable teaching diagrams, exported from shared node/edge sources.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
const root=path.dirname(fileURLToPath(import.meta.url));
const esc=v=>String(v).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const side={left:[0,.5],right:[1,.5],top:[.5,0],bottom:[.5,1]};
const pt=(n,k)=>[n.x+n.w*side[k][0],n.y+n.h*side[k][1]];
for(const [name,stem] of [['flow.json','教学方案流程']]){
 const q=JSON.parse(await fs.readFile(path.join(root,'patent-packet/diagrams',name),'utf8'));
 const nodes=Object.fromEntries(q.nodes.map(v=>[v.id,v]));
 const cells=['<mxCell id="0"/>','<mxCell id="1" parent="0"/>'];
 const svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="700" viewBox="0 0 1600 700">','<defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="8" refY="3" orient="auto"><path d="M0 0L8 3L0 6" fill="#245B77"/></marker></defs>','<rect width="1600" height="700" fill="white"/>',`<text x="80" y="55" font-family="Microsoft YaHei" font-size="34" fill="#132F43">${esc(q.title)}</text>`,`<text x="80" y="102" font-family="Microsoft YaHei" font-size="24" fill="#627681">${esc(q.caption)}</text>`];
 for(const n of q.nodes){
  const label=esc(n.label.split('\n').join('<br>'));
  cells.push(`<mxCell id="${n.id}" value="${label}" style="rounded=0;whiteSpace=wrap;html=1;fontFamily=Microsoft YaHei;fontSize=28;fillColor=#F0F5F8;strokeColor=#245B77;" vertex="1" parent="1"><mxGeometry x="${n.x}" y="${n.y}" width="${n.w}" height="${n.h}" as="geometry"/></mxCell>`);
  const lines=n.label.split('\n'),y=n.y-200;
  svg.push(`<g data-node="${n.id}"><rect x="${n.x}" y="${y}" width="${n.w}" height="${n.h}" fill="#F0F5F8" stroke="#245B77" stroke-width="1.5"/>`);
  lines.forEach((line,i)=>svg.push(`<text x="${n.x+15}" y="${y+n.h/2-(lines.length-1)*18+10+i*36}" font-family="Microsoft YaHei" font-size="29" fill="#132F43">${esc(line)}</text>`));svg.push('</g>');
 }
 for(const [i,e] of q.edges.entries()){
  const start=pt(nodes[e.source],e.from),end=pt(nodes[e.target],e.to);
  let points;
  if(e.points)points=[start,...e.points,end];
  else if(e.kind==='elbow'){const mid=(start[0]+end[0])/2;points=[start,[mid,start[1]],[mid,end[1]],end];}
  else points=[start,end];
  const [ex,ey]=side[e.from],[ix,iy]=side[e.to];
  const intermediate=points.slice(1,-1).map(([x,y])=>`<mxPoint x="${x}" y="${y}"/>`).join('');
  cells.push(`<mxCell id="edge${i}" value="${esc(e.label||'')}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;strokeColor=#245B77;exitX=${ex};exitY=${ey};entryX=${ix};entryY=${iy};fontFamily=Microsoft YaHei;fontSize=22;" edge="1" parent="1" source="${e.source}" target="${e.target}"><mxGeometry relative="1" as="geometry">${intermediate?'<Array as="points">'+intermediate+'</Array>':''}</mxGeometry></mxCell>`);
  svg.push(`<polyline data-source="${e.source}" data-target="${e.target}" points="${points.map(([x,y])=>x+','+(y-200)).join(' ')}" fill="none" stroke="#245B77" stroke-width="2" marker-end="url(#arrow)"/>`);
  if(e.label&&e.label_x!==undefined)svg.push(`<text x="${e.label_x}" y="${e.label_y-200+25}" font-family="Microsoft YaHei" font-size="24" fill="#263D4A">${esc(e.label)}</text>`);
 }
 for(const [i,n] of (q.annotations||[]).entries()){
  cells.push(`<mxCell id="annotation${i}" value="${esc(n.text.split('\n').join('<br>'))}" style="text;html=1;fontFamily=Microsoft YaHei;fontSize=24;" vertex="1" parent="1"><mxGeometry x="${n.x}" y="${n.y}" width="${n.w}" height="${n.h}" as="geometry"/></mxCell>`);
  n.text.split('\n').forEach((line,k)=>svg.push(`<text x="${n.x}" y="${n.y-200+28+k*32}" font-family="Microsoft YaHei" font-size="24" fill="#263D4A">${esc(line)}</text>`));
 }
 cells.push(`<mxCell id="title" value="${esc(q.title+'；'+q.status)}" style="text;html=1;fontFamily=Microsoft YaHei;fontSize=30;" vertex="1" parent="1"><mxGeometry x="80" y="220" width="1440" height="70" as="geometry"/></mxCell>`);
 const mx=`<?xml version="1.0" encoding="UTF-8"?><mxfile host="app.diagrams.net"><diagram id="${name}" name="${esc(q.title)}"><mxGraphModel page="1" pageWidth="1600" pageHeight="1000"><root>${cells.join('')}</root></mxGraphModel></diagram></mxfile>`;
 svg.push('</svg>');await fs.writeFile(path.join(root,'patent-packet/diagrams',stem+'.drawio'),mx);await fs.writeFile(path.join(root,'patent-packet/diagrams',stem+'.svg'),svg.join(''));
 console.log(stem,q.nodes.length,'nodes',q.edges.length,'edges');
}
const profile=path.join(root,'.build/lo-diagram-preview');await fs.mkdir(profile,{recursive:true});
execFileSync(process.env.LIBREOFFICE_EXE||'C:/Program Files/LibreOffice/program/soffice.exe',[
 '-env:UserInstallation='+pathToFileURL(profile).href,'--headless','--convert-to','png',
 '--outdir',path.join(root,'patent-packet/diagrams'),
 path.join(root,'patent-packet/diagrams/教学方案流程.svg')
],{timeout:60000,stdio:'pipe'});
for(const stem of ['教学方案流程']){
 if((await fs.stat(path.join(root,'patent-packet/diagrams',stem+'.png'))).size<1000)throw Error('Missing rendered PNG: '+stem);
}
