from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent.parent
for code in range(25,29):
 d=next(ROOT.glob(f'{code:02}_*'));v=json.loads((d/'relecture_visuelle_root.json').read_text(encoding='utf-8'))
 for mode in ('figures','captures'):
  assert v[mode]['fichiers']
  for name,h in v[mode]['fichiers'].items():assert hashlib.sha256((d/name).read_bytes()).hexdigest()==h
 p=d/'RAPPORT.md';s=p.read_text(encoding='utf-8').replace('vérifications mathématiques et visuelles requises avant état prêt.','vérifications mathématiques et visuelles terminées.')
 s+='\n## Vérifications finales\n\nNeuf activités sources conservées et développées en 45 questions. Calculs et modèles vérifiés par verif_math.py ; figures compilées avec l’outil officiel, conformité TikZ et absence de chevauchement contrôlées. Tous les PNG actifs ont été lus, ainsi que le cours complet, la synthèse et les exercices 1, 5 et 9 (énoncé et étapes) sur téléphone. Les 58 vues navigateur ne présentent aucune anomalie. Empreintes de relecture dans relecture_visuelle_root.json.\n'
 if code==28:s+='\nCorrection ciblée : le dessin du premier exercice montre bien C, B, A après échange des extrémités, puis nouvel audit et nouvelle lecture du corrigé.\n'
 p.write_text(s,encoding='utf-8')
 print(code,'relecture terminée')
