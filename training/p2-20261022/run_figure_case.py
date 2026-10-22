"""Actual public-data analysis and editable figure, without provider calls."""
from pathlib import Path
import csv, hashlib, json, random, statistics, sys
from reportlab.graphics.shapes import Drawing, Line, String, Circle, Rect
from reportlab.graphics import renderSVG

ROOT=Path(__file__).resolve().parent
CASE=ROOT/'examples/figure/01-public-data'

def main():
    out=CASE/'output'; out.mkdir(exist_ok=True)
    data=CASE/'input/penguins.csv'
    with data.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    selected=[r for r in rows if r['species']=='Adelie']
    complete=[r for r in selected if r['sex'] in ('female','male') and r['flipper_length_mm'] not in ('','NA')]
    groups={s:[float(r['flipper_length_mm']) for r in complete if r['sex']==s] for s in ('female','male')}
    stats={'all_rows':len(rows),'Adelie_rows':len(selected),'complete_rows':len(complete),'excluded_Adelie_rows':len(selected)-len(complete),'unit':'mm','groups':{s:{'n':len(v),'mean':statistics.mean(v),'min':min(v),'max':max(v)} for s,v in groups.items()},'male_minus_female':statistics.mean(groups['male'])-statistics.mean(groups['female']),'source_sha256':hashlib.sha256(data.read_bytes()).hexdigest(),'interpretation':'Descriptive secondary analysis. No causal effect or new field experiment is claimed.'}
    (out/'statistics.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
    with (out/'clean-data.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['source_csv_line','sex','flipper_length_mm']);w.writeheader()
        for line,r in enumerate(rows,2):
            if r in complete:w.writerow({'source_csv_line':line,'sex':r['sex'],'flipper_length_mm':r['flipper_length_mm']})
    from reportlab.lib.colors import HexColor
    d=Drawing(720,470)
    d.add(Rect(0,0,720,470,fillColor=HexColor('#ffffff'),strokeColor=None))
    ink=HexColor('#172f43'); gray=HexColor('#d9dfe3')
    d.add(String(65,438,'Adelie penguin flipper length by sex',fontName='Helvetica-Bold',fontSize=19,fillColor=ink))
    d.add(String(65,415,'Public-data secondary analysis | points: observations | bar: mean',fontSize=11,fillColor=ink))
    y=lambda v:90+(v-165)*6.0
    for tick in range(170,211,10):
        d.add(Line(80,y(tick),660,y(tick),strokeColor=gray,strokeWidth=.6))
        d.add(String(48,y(tick)-4,str(tick),fontSize=11,fillColor=ink))
    d.add(Line(80,90,80,375,strokeColor=ink));d.add(Line(80,90,660,90,strokeColor=ink))
    d.add(String(19,211,'mm',fontSize=12,fillColor=ink))
    rng=random.Random(20261022)
    for x,(s,values),color in zip([250,490],groups.items(),['#256c98','#b4652c']):
        c=HexColor(color)
        for v in values:d.add(Circle(x+rng.uniform(-47,47),y(v),3,fillColor=c,strokeColor=None,fillOpacity=.65))
        mean=statistics.mean(values)
        d.add(Line(x-57,y(mean),x+57,y(mean),strokeColor=ink,strokeWidth=2.4))
        d.add(String(x-32,66,s.capitalize(),fontSize=13,fillColor=ink))
        d.add(String(x-48,47,f'n = {len(values)}, mean = {mean:.2f} mm',fontSize=10,fillColor=ink))
    d.add(String(80,19,'Source: palmerpenguins | complete sex and flipper length records | no error bars',fontSize=10,fillColor=ink))
    renderSVG.drawToFile(d,str(out/'figure.svg'))
    caption=('Adelie 企鹅鳍肢长度的性别分组分布。使用 palmerpenguins 公开数据副本；344 条原始记录中有 152 条 Adelie，按性别与鳍肢长度完整筛选后纳入 146 条，雌雄各 73 条。'
    '每个点对应一条观察记录，横向抖动仅用于减少重叠，黑线表示组均值；无误差线。雌性均值为 187.79 mm，雄性为 192.41 mm，雄减雌为 4.62 mm。'
    '本图为课程二次分析，组间差异是描述统计，不能据此推断因果或代表本团队新采集数据。数据来源与 SHA256 见 input/data-source.json 和 statistics.json。\n')
    (out/'caption.md').write_text(caption,encoding='utf-8')
    print(json.dumps({'runner':'Codex desktop tool execution','provider_api_called_by_script':False,'output':str(out),'statistics':stats},ensure_ascii=False))

if __name__=='__main__':main()
