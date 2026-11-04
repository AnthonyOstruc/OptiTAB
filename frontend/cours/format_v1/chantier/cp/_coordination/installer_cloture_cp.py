from pathlib import Path
HERE=Path(__file__).resolve().parent;SOURCE=HERE.parent.parent/'ce1/_coordination'
for name in ['consolider_ce1.py','publier_ce1.py','verifier_publication_ce1.py','cloturer_publication_ce1.py','verifier_liaison_identifiants.py']:
 s=(SOURCE/name).read_text(encoding='utf-8').replace('ce1','cp').replace('CE1','CP')
 for a,b in [("==32","==30"),("range(21,31)","range(21,29)"),("range(1,33)","range(1,31)"),("['exercices']>=288","['exercices']>=270"),("==192","==180"),("32 chapitres","30 chapitres"),("33 sauvegardes","31 sauvegardes"),("'cours':32,'syntheses':32","'cours':30,'syntheses':30"),("192 réponses","180 réponses")]:s=s.replace(a,b)
 if name=='consolider_ce1.py':s=s.replace("FRONT/'cours/cours_optitab/cp/sources/livre.json'","ICI/'sources/livre.json'")
 p=HERE/name.replace('ce1','cp')
 if not p.exists():p.write_text(s,encoding='utf-8')
print('Contrôles de clôture et publication isolés sous CP.')
