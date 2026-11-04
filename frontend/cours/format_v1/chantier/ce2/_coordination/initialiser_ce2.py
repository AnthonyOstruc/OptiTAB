"""Sauvegardes du livre CE2 avant rédaction, sans mutation de la base."""
from pathlib import Path
import json,hashlib,datetime
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent;FRONT=ICI.parents[4]
book=FRONT/'cours/cours_optitab/ce2/sources/livre.json';source=json.loads(book.read_text(encoding='utf-8'))
base=json.loads((ICI/'inventaire_base_ce2.json').read_text(encoding='utf-8'));assert len(base['niveaux'])==1 and not base['contextes']
rows=[]
for item in source:
 n=item['numero'];d=ROOT/f"{n:02}_{item['slug']}";d.mkdir(exist_ok=True);s=d/'sources_locales';s.mkdir(exist_ok=True)
 course='\n\n'.join([item['objectif'],item['manipulation'],*item['lecon'],item['exemple'],item['guide'],item['guide_reponse'],item['aide'],item['vigilance']])
 for name,text in [('chapitre.json',json.dumps(item,ensure_ascii=False,indent=2)+'\n'),('cours.txt',course),('exercices.txt',json.dumps(item['exercices'],ensure_ascii=False,indent=2))]:
  p=s/name
  if p.exists():assert p.read_text(encoding='utf-8')==text
  else:p.write_text(text,encoding='utf-8')
 hashes={str(book.relative_to(FRONT)):hashlib.sha256(book.read_bytes()).hexdigest()}
 (s/'empreintes_sources.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
 theme=('Nombres et calculs' if n<=14 else 'Résolution de problèmes' if n<=19 else 'Fractions' if n<=23 else 'Grandeurs et mesures' if n<=31 else 'Espace et géométrie' if n<=35 else 'Organisation de données')
 meta={'notion':n,'titre':item['titre'],'theme':theme,'contexte':None,'creation_ce2':True,'cours':[],'fiches':[],'exercices':[]}
 (d/'source_en_ligne').mkdir(exist_ok=True)
 if not (d/'source_en_ligne/meta.json').exists():(d/'source_en_ligne/meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
 if not (d/'etat.json').exists():(d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'a_attribuer','maj':datetime.date.today().isoformat()}),encoding='utf-8')
 (d/'figures/images').mkdir(parents=True,exist_ok=True);(d/'planches_sources').mkdir(exist_ok=True)
 rows.append({'notion':n,'titre':item['titre'],'slug':item['slug'],'dossier':d.name,'theme':theme,'exercices_source':len(item['exercices']),'images_source':0})
(ICI/'inventaire_initial_ce2.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(ICI/'contexte_ce2.json').write_text(json.dumps({'mode':'nouveau_contexte','niveau':base['niveaux'][0]['id'],'matiere':1,'pays':'France','aucune_ecriture_base':True},indent=2),encoding='utf-8')
print(len(rows),'chapitres sauvegardés ;',sum(x['exercices_source'] for x in rows),'exercices sources')
