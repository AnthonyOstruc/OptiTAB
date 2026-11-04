"""Réemploi isolé du processus validé CM2 ; ne lance aucune publication."""
from pathlib import Path
ICI=Path(__file__).resolve().parent;old=ICI.parent.parent/'cm2/_coordination'
for name in ('publier_cm2.py','verifier_publication_cm2.py','restaurer_creation_cm2.py'):
 text=(old/name).read_text(encoding='utf-8').replace('cm2','cm1').replace('CM2','CM1')
 text=text.replace('id=13','id=12').replace("'niveau':13","'niveau':12").replace('niveau=13','niveau=12')
 text=text.replace("assert len(finaux)==21 and", "assert len(finaux)==r['exercices'] and")
 text=text.replace('assert len(exids)==21',"assert len(exids)==row['exercices']")
 text=text.replace('count()==441',"count()==bilan['exercices']")
 # Contexte CM1 destiné aux nouveaux contenus ; niveau12 conservé dans la sauvegarde.
 target=ICI/name.replace('cm2','cm1')
 assert not target.exists(),target
 target.write_text(text,encoding='utf-8')
print('Scripts de simulation, publication, vérification et restauration préparés ; aucune écriture SQL.')
