"""Réutilisation des contrôles validés CE2, sans toucher aux autres niveaux."""
from pathlib import Path
HERE=Path(__file__).resolve().parent;SOURCE=HERE.parent.parent/'ce2/_coordination'
names=['inventorier_base.py','initialiser_ce2.py','commun_redaction.py','valider_ce2.py','controle_navigateur_ce2.mjs','planches_relecture_ce2.py','continuer_controles.py','planches_figures_ce2.py','planches_ensemble.py','verifier_figures_ce2.py','consolider_ce2.py','publier_ce2.py','verifier_publication_ce2.py','cloturer_publication_ce2.py','restaurer_creation_ce2.py']
for name in names:
 target=HERE/name.replace('ce2','ce1');text=(SOURCE/name).read_text(encoding='utf-8').replace('ce2','ce1').replace('CE2','CE1')
 if name=='initialiser_ce2.py':
  a=text.index(' theme=');b=text.index('\n meta=',a)
  text=text[:a]+" theme=('Nombres et calculs' if n<=13 else 'Résolution de problèmes' if n<=17 else 'Fractions' if n<=20 else 'Grandeurs et mesures' if n<=25 else 'Espace et géométrie' if n<=30 else 'Organisation de données')"+text[b:]
 for a,b in [("id=11","id=10"),("'niveau':11","'niveau':10"),("niveau=11","niveau=10"),("['notions']==36","['notions']==32"),("count()==36","count()==32"),("['fiches']==36","['fiches']==32"),("['exercices']>=324","['exercices']>=288"),("==216","==192"),("notions_visibles']==36","notions_visibles']==32"),("36 chapitres visibles","32 chapitres visibles"),("37 sauvegardes","33 sauvegardes"),("'cours':36,'syntheses':36","'cours':32,'syntheses':32"),("216 réponses","192 réponses"),("range(1,37)","range(1,33)"),("rootcodes=set(range(1,37))","rootcodes=set(range(1,33))")]:text=text.replace(a,b)
 if not target.exists():target.write_text(text,encoding='utf-8')
print('Outils CE1 isolés, aucune écriture SQL.')
