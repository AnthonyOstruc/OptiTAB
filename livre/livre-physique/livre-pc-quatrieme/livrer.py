from pathlib import Path
import json,hashlib,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
pdf=HERE/'build/main.pdf'
report=json.loads((HERE/'build/verification.json').read_text(encoding='utf8'))
visual=json.loads((HERE/'build/validation-visuelle.json').read_text(encoding='utf8'))
proof=json.loads((HERE/'build/preuves-revision.json').read_text(encoding='utf8'))
sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
assert report['echecs']==0 and visual['valide']
assert sha==report['sha256']==visual['sha256']==proof['sha256']
assert all(item['valide'] for item in proof['echelles'])
name='OptiTAB - Physique-chimie - Quatrième (4e) - Manuel complet.pdf'
targets=[ROOT/'output/pdf/France/Physique-chimie'/name,Path('C:/Users/SWEELCO-AT/Desktop/Livres OptiTAB - Lycée')/name]
for target in targets:
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(pdf,target)
    assert hashlib.sha256(target.read_bytes()).hexdigest()==sha
delivery=dict(date='2026-10-24',revision='Figures des exercices et corrigés ; explications pédagogiques',pages=report['pages'],chapitres=20,exercices=300,defis=20,figures=report['figures'],figures_cours=report['figures_cours'],figures_exercices=report['figures_exercices'],enonces_illustres=report['enonces_illustres'],corriges_illustres=report['corriges_illustres'],demarches_ajoutees=report['demarches_ajoutees'],bilans=4,evaluations=2,sha256=sha,livraisons=[str(t.resolve()) for t in targets],controles=report['controles'],calculs=report['calculs'])
out=ROOT/'output/verification/physique-chimie-quatrieme-livraison.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(delivery,ensure_ascii=True,indent=2))
