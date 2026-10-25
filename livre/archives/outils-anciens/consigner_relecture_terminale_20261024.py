"""Enregistre la relecture finale après inspection des 36 planches et 25 preuves."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[1]
pdf=root/'livre-pc-terminale/main.pdf'
sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
assert sha=='1b7e00a59a4ef43b99c0e62b63aae0b65773c2c592f725c229349ec2d993676b'
proof=json.loads((root/'tmp/pdfs/audit-physique-20261024/preuves-terminale-finales/preuves.json').read_text(encoding='utf-8'))
assert proof['sha256']==sha
report=dict(date='2026-10-24',valide=True,sha256=sha,pages=709,rendu_integral=True,planches_inspectees=list(range(1,37)),pages_poppler_inspectees=proof['pages'],figures_nouvelles_inspectees=18,figure_ancienne_reparee='12-ex11',observations=['Les 709 pages finales ont été rendues et inspectées par planches pour la mise en page.','Les constructions nouvelles ont été inspectées séparément puis dans les pages critiques finales avec Poppler.','Les légendes du palier et de la courbe catalysée de 12.11 sont distinctes.','Les diagrammes, courbes, tableaux, encadrés et fins de page conservent leurs marges.','Les quinze pages de notes réglées sont intentionnelles ; elles ont un titre et des lignes vectorielles.','Les contrôles numériques ciblés et structurels complètent la relecture ; ils ne prouvent pas automatiquement toutes les phrases.'],defauts_restants=[])
(root/'livre-pc-terminale/build/validation-visuelle-revision.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Relecture finale de Terminale consignée.')
