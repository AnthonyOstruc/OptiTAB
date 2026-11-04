from pathlib import Path
import json,hashlib,datetime,os
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;FRONT=HERE.parents[4];REPO=HERE.parents[5]
book=HERE/'sources/livre.json';source=json.loads(book.read_text(encoding='utf-8'))
base=json.loads((HERE/'inventaire_base_cp.json').read_text(encoding='utf-8'));assert not base['contextes']
paths=[book]+[REPO/'livre/livre-maths/livre-cp'/n for n in ['modele.py','contenu_nombres.py','contenu_calcul.py','contenu_mesures_geometrie.py','dessins.py']]
hashes={os.path.relpath(p,FRONT).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
rows=[]
for item in source:
 n=item['numero'];d=ROOT/f"{n:02}_{item['slug']}";d.mkdir(exist_ok=True);s=d/'sources_locales';s.mkdir(exist_ok=True)
 course='\n\n'.join([item['objectif'],item['manipulation'],*item['lecon'],item['exemple'],item['guide'],item['guide_reponse'],item['aide'],item['vigilance']])
 for name,text in [('chapitre.json',json.dumps(item,ensure_ascii=False,indent=2)+'\n'),('cours.txt',course),('exercices.txt',json.dumps(item['exercices'],ensure_ascii=False,indent=2))]:
  p=s/name
  if p.exists():assert p.read_text(encoding='utf-8')==text
  else:p.write_text(text,encoding='utf-8')
 (s/'empreintes_sources.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
 theme=('Nombres et calculs' if n<=16 or n==30 else 'Résolution de problèmes' if n<=20 else 'Grandeurs et mesures' if n<=24 else 'Espace et géométrie' if n<=28 else 'Organisation et gestion de données')
 meta={'notion':n,'titre':item['titre'],'theme':theme,'contexte':None,'creation_cp':True,'cours':[],'fiches':[],'exercices':[]}
 (d/'source_en_ligne').mkdir(exist_ok=True)
 if not (d/'source_en_ligne/meta.json').exists():(d/'source_en_ligne/meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
 if not (d/'etat.json').exists():(d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'a_attribuer','maj':datetime.date.today().isoformat()}),encoding='utf-8')
 (d/'figures/images').mkdir(parents=True,exist_ok=True);(d/'planches_sources').mkdir(exist_ok=True)
 rows.append({'notion':n,'titre':item['titre'],'slug':item['slug'],'dossier':d.name,'theme':theme,'exercices_source':len(item['exercices']),'images_source':0})
(HERE/'inventaire_initial_cp.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'contexte_cp.json').write_text(json.dumps({'mode':'nouveau_niveau_et_contexte' if not base['niveaux'] else 'nouveau_contexte','niveau':base['niveaux'][0]['id'] if base['niveaux'] else None,'matiere':1,'pays':'France','aucune_ecriture_base':True},indent=2),encoding='utf-8')
print(len(rows),'chapitres sauvegardés ;',sum(x['exercices_source'] for x in rows),'exercices sources')
