"""Prépare le chantier CM2 depuis les sources locales, sans base ni altération des originaux."""
from pathlib import Path
import json,re,hashlib,datetime,sys
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent;FRONT=ICI.parents[4];OUTILS=ROOT.parents[1]/'outils'
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,str(OUTILS))
import planche
PLAN=[('grands-nombres','Nombres et calculs'),('multiples-diviseurs','Nombres et calculs'),('fractions','Nombres et calculs'),('comparer-fractions','Nombres et calculs'),('fraction-quantite','Nombres et calculs'),('decimaux','Nombres et calculs'),('operations-entiers','Nombres et calculs'),('division','Nombres et calculs'),('calculs-decimaux','Nombres et calculs'),('proportionnalite','Proportionnalité et résolution de problèmes'),('mesures','Grandeurs et mesures'),('aires','Grandeurs et mesures'),('angles','Espace et géométrie'),('polygones','Espace et géométrie'),('constructions','Espace et géométrie'),('symetrie','Espace et géométrie'),('solides','Espace et géométrie'),('durees','Grandeurs et mesures'),('donnees','Organisation et gestion de données et probabilités'),('probabilites','Organisation et gestion de données et probabilités'),('regularites','Régularités et pensée informatique')]
rows=[]
for numero,(slug,theme) in enumerate(PLAN,1):
 d=ROOT/f'{numero:02}_{slug}';d.mkdir(exist_ok=True)
 sources=d/'sources_locales';sources.mkdir(exist_ok=True)
 originals=[('cours',FRONT/f'cours/cours_optitab/cm2/cours_{slug}_cm2.txt'),('fiche',FRONT/f'cours/resume/cm2/resume_{slug}_cm2.txt'),('exercices',FRONT/f'exercices/cm2/exercice_{slug}_cm2.txt')]
 images=[];hashes={}
 for genre,p in originals:
  assert p.is_file(),p
  content=p.read_bytes();target=sources/f'{genre}.txt'
  if target.exists():assert target.read_bytes()==content
  else:target.write_bytes(content)
  hashes[str(p.relative_to(FRONT))]=hashlib.sha256(content).hexdigest()
  raw=content.decode('utf-8')
  for line in re.findall(r'^Images?:[ \t]*(.+)$',raw,re.M):
   for filename in map(str.strip,line.split(',')):
    candidates=[p.parent/'images'/filename,FRONT/'cours/cours_optitab/cm2/images'/filename,FRONT/'exercices/cm2/images'/filename]
    image=next((x for x in candidates if x.is_file()),None)
    assert image,(p,filename)
    if any(x['chemin']==str(image) for x in images):continue
    images.append({'genre':genre,'fichier':filename,'chemin':str(image),'sha256':hashlib.sha256(image.read_bytes()).hexdigest()})
 titre=re.search(r'^Titre:[ \t]*(.+)$',(sources/'cours.txt').read_text(encoding='utf-8'),re.M)[1]
 meta={'notion':numero,'titre':titre,'theme':theme,'contexte':None,'creation_cm2':True,'cours':[],'fiches':[],'exercices':[]}
 export=d/'source_en_ligne';export.mkdir(exist_ok=True)
 mp=export/'meta.json'
 if not mp.exists():mp.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,obj in [('inventaire_images.json',images),('empreintes_sources.json',hashes)]:
  p=sources/name
  if p.exists():assert json.loads(p.read_text(encoding='utf-8'))==obj
  else:p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 etat=d/'etat.json'
 if not etat.exists():etat.write_text(json.dumps({'statut':'en_cours','agent':'a_attribuer','maj':datetime.date.today().isoformat()},indent=2),encoding='utf-8')
 (d/'figures/images').mkdir(parents=True,exist_ok=True)
 (d/'planches_sources').mkdir(exist_ok=True)
 for k in range(0,len(images),12):
  png=d/'planches_sources'/f'planche_{k//12+1:02}.png'
  if not png.exists():planche.composer([(f"{x['genre']} · {x['fichier']}",Path(x['chemin'])) for x in images[k:k+12]],png)
 row={'notion':numero,'titre':titre,'theme':theme,'slug':slug,'dossier':d.name,'cours':0,'fiches':0,'exercices':0,'exercices_source':len(re.findall(r'^=== .+', (sources/'exercices.txt').read_text(encoding='utf-8'),re.M)),'images_source':len(images)}
 rows.append(row);print(numero,slug,row['exercices_source'],row['images_source'],flush=True)
(ICI/'inventaire_initial_cm2.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ICI/'contexte_cm2.json').write_text(json.dumps({'mode':'nouveau_contexte','niveau':13,'matiere':1,'pays':'France','aucune_ecriture_base':True},indent=2),encoding='utf-8')
print('TOTAL',len(rows),'chapitres',sum(r['exercices_source'] for r in rows),'exercices sources',sum(r['images_source'] for r in rows),'images sources')
