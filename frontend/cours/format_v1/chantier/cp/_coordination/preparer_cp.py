"""Sauvegarder les sources CP originales et installer les contrôles locaux éprouvés."""
from pathlib import Path
import sys,json,dataclasses,re,unicodedata
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;REPO=HERE.parents[5];SOURCE=ROOT.parent/'ce1/_coordination'
bookdir=REPO/'livre/livre-maths/livre-cp';sys.path.insert(0,str(bookdir))
import modele,contenu_nombres,contenu_calcul,contenu_mesures_geometrie
items=[]
for item in modele.CHAPITRES:
 row=dataclasses.asdict(item)
 row['slug']=re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',row['titre']).encode('ascii','ignore').decode().lower()).strip('-')
 items.append(row)
(HERE/'sources').mkdir(exist_ok=True)
p=HERE/'sources/livre.json';text=json.dumps(items,ensure_ascii=False,indent=2)+'\n'
if p.exists():assert p.read_text(encoding='utf-8')==text
else:p.write_text(text,encoding='utf-8')
names=['inventorier_base.py','commun_redaction.py','valider_ce1.py','controle_navigateur_ce1.mjs','planches_relecture_ce1.py','continuer_controles.py','planches_figures_ce1.py','planches_ensemble.py','verifier_figures_ce1.py']
for name in names:
 target=HERE/name.replace('ce1','cp');s=(SOURCE/name).read_text(encoding='utf-8').replace('ce1','cp').replace('CE1','CP').replace('range(1,33)','range(1,31)')
 if not target.exists():target.write_text(s,encoding='utf-8')
print(len(items),'chapitres et',sum(len(x['exercices']) for x in items),'exercices sources :')
for item in items:print(f"{item['numero']:02} {item['titre']} [{item['domaine']}] {item['figure'][0]}")
