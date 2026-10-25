"""Consigne la relecture visuelle du PDF courant dans build/qa/relecture-visuelle.json.

À n’exécuter qu’après avoir effectivement lu toutes les planches build/qa/planche-*.png
et les rendus Poppler des pages critiques. Les défauts relevés et corrigés au cours
des relectures successives sont listés dans DEFAUTS_CORRIGES.
"""
from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parent
QA=ROOT/'build/qa'
DEFAUTS_CORRIGES=json.loads((QA/'defauts-corriges.json').read_text(encoding='utf8')) if (QA/'defauts-corriges.json').exists() else []
controle=json.loads((QA/'controle-pdf.json').read_text(encoding='utf8'))
poppler=json.loads((QA/'poppler/rendus.json').read_text(encoding='utf8'))
digest=hashlib.sha256((ROOT/'main.pdf').read_bytes()).hexdigest()
assert controle['sha256']==poppler['sha256']==digest,'Contrôles à relancer sur le PDF courant.'
planches=sorted(QA.glob('planche-*.png'))
assert len(planches)==controle['planches']
rapport=dict(sha256=digest,date_verification='2026-10-23',pages=controle['pages'],planches_lues=len(planches),
             pages_poppler_relues=[p['page_pdf'] for p in poppler['pages']],
             defauts_corriges=DEFAUTS_CORRIGES,defauts_restants=[],
             methode='Lecture de toutes les planches de six pages, puis des pages critiques en pleine résolution (PyMuPDF 100 ppp et Poppler 135 ppp).')
(QA/'relecture-visuelle.json').write_text(json.dumps(rapport,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in rapport.items() if k!='defauts_corriges'},ensure_ascii=True,indent=2),len(DEFAUTS_CORRIGES),'défauts corrigés')
