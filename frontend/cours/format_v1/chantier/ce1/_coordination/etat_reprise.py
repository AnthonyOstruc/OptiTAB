from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
for d in sorted(ROOT.glob('[0-9][0-9]_*')):
 def load(name):
  p=d/name;return json.loads(p.read_text(encoding='utf-8')) if p.is_file() else {}
 print(d.name[:2],load('etat.json').get('statut'), 'math',load('verification_math.json').get('statut'),'validation',load('validation_ce1.json').get('statut'),'navigateur',load('audit_navigateur_ce1.json').get('statut'),'preuves',load('PREUVES_FINALES.json').get('statut'),'PNG',len(list((d/'figures/images').glob('*.png'))))
