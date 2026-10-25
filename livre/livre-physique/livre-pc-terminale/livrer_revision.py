"""Livre le PDF de Terminale dont l’audit et la relecture portent la même empreinte."""
from pathlib import Path
import json,hashlib,shutil
import fitz
here=Path(__file__).resolve().parent
pdf=here/'main.pdf'
audit=json.loads((here/'build/audit-revision.json').read_text(encoding='utf-8'))
visual=json.loads((here/'build/validation-visuelle-revision.json').read_text(encoding='utf-8'))
sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
assert audit['echecs']==0 and visual['valide'] and not visual['defauts_restants']
assert sha==audit['sha256']==visual['sha256']
assert len(visual['planches_inspectees'])==36 and len(visual['pages_poppler_inspectees'])==25
with fitz.open(pdf) as d:assert len(d)==audit['pages']==visual['pages']==709
name='OptiTAB - Physique-chimie - Terminale spécialité - Manuel complet.pdf'
targets=[here.parent/'output/pdf/France/Physique-chimie'/name,Path('C:/Users/SWEELCO-AT/Desktop/Livres OptiTAB - Lycée')/name]
for dest in targets:
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(pdf,dest)
    assert hashlib.sha256(dest.read_bytes()).hexdigest()==sha
report={k:v for k,v in audit.items() if k!='details'}
report.update(date='2026-10-24',livraisons=[str(p.resolve()) for p in targets],relecture=visual)
out=here.parent/'output/verification/physique-chimie-terminale-livraison.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(pages=709,sha256=sha,livraisons=[str(p) for p in targets]),ensure_ascii=True))
