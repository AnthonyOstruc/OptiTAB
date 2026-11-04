from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parent.parent
for d in sorted(ROOT.glob('[0-9][0-9]_*')):
 def load(name):
  p=d/name;return json.loads(p.read_text(encoding='utf-8')) if p.is_file() else {}
 p=d/'figures/figures.py';count=len(runpy.run_path(str(p)).get('FIGURES',{})) if p.is_file() else 0
 print(d.name[:2],load('etat.json').get('statut'),'navigateur',load('audit_navigateur_cp.json').get('statut'),'preuves',load('PREUVES_FINALES.json').get('statut'),'PNG',len(list((d/'figures/images').glob('*.png'))),'/',count)
