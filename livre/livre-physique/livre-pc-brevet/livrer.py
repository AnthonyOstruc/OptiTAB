from pathlib import Path
import json,hashlib,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
pdf=HERE/'build/main.pdf'
report=json.loads((HERE/'build/verification.json').read_text(encoding='utf8'))
visual=json.loads((HERE/'build/validation-visuelle.json').read_text(encoding='utf8'))
revision=json.loads((HERE/'build/audit-revision.json').read_text(encoding='utf8'))
annales=json.loads((HERE/'build/audit-annales.json').read_text(encoding='utf8'))
sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
assert report['echecs']==0 and visual['valide']
assert revision['echecs']==0 and len(revision['entrees'])==308
assert sha==report['sha256']==visual['sha256']
assert annales['echecs']==0 and annales['questions']==45 and annales['sha256']==sha
name='OptiTAB - Physique-chimie - Troisième (3e) - Brevet 2027 - Manuel complet.pdf'
targets=[ROOT/'output/pdf/France/Physique-chimie'/name,Path('C:/Users/SWEELCO-AT/Desktop/Livres OptiTAB - Lycée')/name]
for target in targets:
    target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(pdf,target)
    assert hashlib.sha256(target.read_bytes()).hexdigest()==sha
delivery={k:report[k] for k in ['date','pages','chapitres','exercices','defis','investigations','brevets_blancs','figures','controles','calculs','sha256']}
delivery['livraisons']=[str(t.resolve()) for t in targets]
delivery['revision_figures']={k:revision[k] for k in ['enonces_illustres','corriges_illustres','demarches_chapitres','demarches_brevets','controles','echecs']}
delivery['sujets_supplementaires']={k:annales[k] for k in ['sujets','questions','figures','calculs','controles','echecs']}
out=ROOT/'output/verification/physique-chimie-brevet-livraison.json';out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(delivery,ensure_ascii=True,indent=2))
