from pathlib import Path
import hashlib, json

root = Path(__file__).resolve().parent
items = [
    {'file': 'paper.pdf', 'type': '公开发表材料', 'license': 'CC BY 4.0',
     'source': 'https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0328041',
     'attribution': 'Heinrich et al. (2025). AI-assisted grading and personalized feedback in large political science classes: Results from randomized controlled trials. PLOS ONE 20(8): e0328041.',
     'copied_from': 'training/beginner-lesson/assets/paper.pdf'},
    {'file': 'penguins.csv', 'type': '公开观测数据', 'license': 'CC0',
     'source': 'https://github.com/allisonhorst/palmerpenguins/blob/main/inst/extdata/penguins.csv',
     'attribution': 'palmerpenguins; Horst, Hill and Gorman. Palmer Station penguin observations.',
     'copied_from': 'training/deck-zh/sources/penguins.csv'},
    {'file': 'guide.json', 'type': '教学模拟', 'license': '项目内教学材料',
     'source': 'training/demos/grant/guide.json', 'attribution': 'TEACH-GRANT-01；课程编写的练习要求，不能用于正式申报。',
     'copied_from': 'training/demos/grant/guide.json'},
    {'file': 'template.docx', 'type': '教学模拟', 'license': '项目内教学材料',
     'source': 'training/demos/grant/template.docx', 'attribution': '课程练习模板；不是主管部门的正式模板。',
     'copied_from': 'training/demos/grant/template.docx'},
]
for item in items:
    item['sha256'] = hashlib.sha256((root / 'materials' / item['file']).read_bytes()).hexdigest()
(root / 'materials/materials-manifest.json').write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Recorded source categories and SHA-256 for four material files.')
