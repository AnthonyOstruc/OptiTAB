"""Préparation isolée CE2 ; aucun import n'est lancé."""
from pathlib import Path
ICI=Path(__file__).resolve().parent;CM1=ICI.parent.parent/'cm1/_coordination'
for name in ('inventorier_base.py','valider_cm1.py','controle_navigateur_cm1.mjs','planches_relecture_cm1.py'):
 target=ICI/name.replace('cm1','ce2')
 if not target.exists():target.write_text((CM1/name).read_text(encoding='utf-8').replace('cm1','ce2').replace('CM1','CE2'),encoding='utf-8')
print('Outillage CE2 préparé ; aucune écriture en base.')
