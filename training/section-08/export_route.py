from pathlib import Path
from xml.etree import ElementTree as E
import json,html
r=Path(__file__).resolve().parent;p=r/'figure-packet';q=json.loads((p/'route.json').read_text('utf-8'));mx=E.Element('mxfile',host='app.diagrams.net');dg=E.SubElement(mx,'diagram',id='research-route',name='拟议技术路线');model=E.SubElement(dg,'mxGraphModel',page='1',pageWidth='1600',pageHeight='1000');root=E.SubElement(model,'root');E.SubElement(root,'mxCell',id='0');E.SubElement(root,'mxCell',id='1',parent='0')
for n in q['nodes']:
 c=E.SubElement(root,'mxCell',id=n['id'],value=n['label'],style='rounded=0;whiteSpace=wrap;html=1;fontFamily=Microsoft YaHei;fontSize=28;fillColor=#F0F5F8;strokeColor=#245B77;',vertex='1',parent='1');E.SubElement(c,'mxGeometry',x=str(n['x']),y=str(n['y']),width=str(n['w']),height=str(n['h']),attrib={'as':'geometry'})
coords={'left':(0,.5),'right':(1,.5),'top':(.5,0),'bottom':(.5,1)}
for i,e in enumerate(q['edges']):
 ex,ey=coords[e['from']];ix,iy=coords[e['to']];style=f'edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;strokeColor=#245B77;exitX={ex};exitY={ey};entryX={ix};entryY={iy};'
 c=E.SubElement(root,'mxCell',id='e'+str(i),style=style,edge='1',parent='1',source=e['source'],target=e['target']);E.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
c=E.SubElement(root,'mxCell',id='title',value=q['title']+'（教学模拟，未实施）',style='text;html=1;fontFamily=Microsoft YaHei;fontSize=32;',vertex='1',parent='1');E.SubElement(c,'mxGeometry',x='80',y='220',width='1440',height='70',attrib={'as':'geometry'});E.indent(mx);E.ElementTree(mx).write(p/'研究技术路线.drawio',encoding='utf-8',xml_declaration=True)
nodes={n['id']:n for n in q['nodes']}
def pt(n,side):
 dx,dy=coords[side];return n['x']+n['w']*dx,n['y']-200+n['h']*dy
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="700" viewBox="0 0 1600 700">','<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L9,3 L0,6" fill="none" stroke="#245B77" stroke-width="1.5"/></marker></defs>','<rect width="1600" height="700" fill="white"/>',f'<text x="80" y="65" font-family="Microsoft YaHei" font-size="35" fill="#132F43">{html.escape(q["title"])}</text>','<text x="80" y="110" font-family="Microsoft YaHei" font-size="25" fill="#627681">教学模拟，未实施。分配、样本、授权与评分标准待明确。</text>']
for e in q['edges']:
 a,b=pt(nodes[e['source']],e['from']),pt(nodes[e['target']],e['to']);mid=(a[0]+b[0])/2;points=[a,b] if e.get('kind')!='elbow' else [a,(mid,a[1]),(mid,b[1]),b];ps=' '.join(str(x)+','+str(y) for x,y in points);svg.append(f'<polyline data-source="{e["source"]}" data-target="{e["target"]}" points="{ps}" fill="none" stroke="#245B77" stroke-width="2" marker-end="url(#arrow)"/>')
for n in q['nodes']:
 x,y,w,h=n['x'],n['y']-200,n['w'],n['h'];svg.append(f'<g data-node="{n["id"]}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#F0F5F8" stroke="#245B77" stroke-width="1.5"/><text x="{x+15}" y="{y+h/2+10}" font-family="Microsoft YaHei" font-size="30" fill="#132F43">{html.escape(n["label"])}</text></g>')
svg.append('</svg>');(p/'研究技术路线.svg').write_text(''.join(svg),'utf-8');print('draw.io and SVG exported from route.json')
