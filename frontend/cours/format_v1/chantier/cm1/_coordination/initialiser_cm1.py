"""Sauvegardes des sources du livre et outillage isolé CM1 ; aucune écriture SQL."""
from pathlib import Path
import json,hashlib,datetime
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent;FRONT=ICI.parents[4]
book=FRONT/'cours/cours_optitab/cm1/sources/livre.json'
source=json.loads(book.read_text(encoding='utf-8'))
base=json.loads((ICI/'inventaire_base_cm1.json').read_text(encoding='utf-8'))
assert len(base['niveaux'])==1 and not base['contextes']
rows=[]
for item in source:
 n=item['numero'];d=ROOT/f"{n:02}_{item['slug']}";d.mkdir(exist_ok=True)
 s=d/'sources_locales';s.mkdir(exist_ok=True)
 data=json.dumps(item,ensure_ascii=False,indent=2)+'\n'
 for name,text in [('chapitre.json',data),('cours.txt','\n\n'.join(item['cours'])),('exercices.txt',json.dumps(item['exercices'],ensure_ascii=False,indent=2))]:
  p=s/name
  if p.exists():assert p.read_text(encoding='utf-8')==text
  else:p.write_text(text,encoding='utf-8')
 hashes={str(book.relative_to(FRONT)):hashlib.sha256(book.read_bytes()).hexdigest()}
 (s/'empreintes_sources.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
 theme=('Nombres et calculs' if n<=10 else 'Grandeurs et mesures' if n<=14 else 'Espace et géométrie' if n<=18 else 'Proportionnalité' if n==19 else 'Organisation de données et probabilités')
 meta={'notion':n,'titre':item['titre'],'theme':theme,'contexte':None,'creation_cm1':True,'cours':[],'fiches':[],'exercices':[]}
 (d/'source_en_ligne').mkdir(exist_ok=True)
 if not (d/'source_en_ligne/meta.json').exists():(d/'source_en_ligne/meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
 if not (d/'etat.json').exists():(d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'a_attribuer','maj':datetime.date.today().isoformat()}),encoding='utf-8')
 (d/'figures/images').mkdir(parents=True,exist_ok=True);(d/'planches_sources').mkdir(exist_ok=True)
 rows.append({'notion':n,'titre':item['titre'],'slug':item['slug'],'dossier':d.name,'theme':theme,'exercices_source':len(item['exercices']),'images_source':0})
for name in ('valider_cm2.py','controle_navigateur_cm2.mjs','planches_relecture_cm2.py'):
 target=ICI/name.replace('cm2','cm1')
 if not target.exists():target.write_text((ROOT.parent/'cm2/_coordination'/name).read_text(encoding='utf-8').replace('cm2','cm1').replace('CM2','CM1'),encoding='utf-8')
(ICI/'inventaire_initial_cm1.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(ICI/'contexte_cm1.json').write_text(json.dumps({'mode':'nouveau_contexte','niveau':base['niveaux'][0]['id'],'matiere':1,'pays':'France','aucune_ecriture_base':True},indent=2),encoding='utf-8')
print(len(rows),'chapitres sauvegardés ;',sum(r['exercices_source'] for r in rows),'exercices sources')
