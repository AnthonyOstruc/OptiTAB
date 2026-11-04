from pathlib import Path
ICI=Path(__file__).resolve().parent;CM1=ICI.parent.parent/'cm1/_coordination'
p=ICI/'commun_redaction.py'
if not p.exists():
 text=(CM1/'commun_redaction.py').read_text(encoding='utf-8').replace('CM1','CE2').replace('len(items)>=15','len(items)>=9').replace("i<=5 else 'medium' if i<=10","i<=3 else 'medium' if i<=6")
 p.write_text(text,encoding='utf-8')
for name in ('publier_cm1.py','verifier_publication_cm1.py','restaurer_creation_cm1.py','cloturer_publication_cm1.py','consolider_cm1.py'):
 text=(CM1/name).read_text(encoding='utf-8').replace('cm1','ce2').replace('CM1','CE2')
 text=text.replace('id=12','id=11').replace("'niveau':12","'niveau':11").replace('niveau=12','niveau=11').replace("['niveau']==12","['niveau']==11")
 text=text.replace("bilan['notions']==21","bilan['notions']==36").replace('count()==21','count()==36').replace("bilan['fiches']==21","bilan['fiches']==36")
 text=text.replace("bilan['exercices']>=315","bilan['exercices']>=324").replace("==126","==216").replace("notions_visibles']==21","notions_visibles']==36").replace('21 chapitres visibles','36 chapitres visibles').replace('22 sauvegardes','37 sauvegardes').replace("'cours':21,'syntheses':21","'cours':36,'syntheses':36").replace('126 réponses','216 réponses')
 text=text.replace('rootcodes={11,12,13,14,20,21}','rootcodes=set(range(24,32))').replace("len(source['exercices'])==15","len(source['exercices'])==9")
 target=ICI/name.replace('cm1','ce2')
 if not target.exists():target.write_text(text,encoding='utf-8')
print('Outils de rédaction et publication isolés CE2 prêts, non exécutés.')
