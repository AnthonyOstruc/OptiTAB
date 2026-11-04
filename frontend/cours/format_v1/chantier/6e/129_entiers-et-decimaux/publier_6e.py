"""Publication contrôlée de la seule 6e, simulation par défaut.

Réutilise l'importeur officiel sans modifier les outils communs. Les cours et
fiches manquants sont créés dans la même transaction, après sauvegarde. Les
exports source restent immuables, y compris les clés provisoires nouveau-N.
"""
from pathlib import Path
import os,sys,json,hashlib,datetime,contextlib,re
from urllib.request import urlopen
sys.stdout.reconfigure(encoding='utf-8');sys.stderr.reconfigure(encoding='utf-8')
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent;BACKEND=ICI.parents[5]/'backend';OUTILS=ROOT.parents[1]/'outils'
os.chdir(BACKEND);sys.path.insert(0,str(BACKEND));os.environ.setdefault('DJANGO_SETTINGS_MODULE','backendAPI.settings')
import django
django.setup()
from django.db import transaction
from django.core.files import File
from cours.models import Cours
from synthesis.models import SynthesisSheet
from curriculum.models import Exercice
MODE='appliquer' if '--appliquer' in sys.argv else 'simulation'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
bilan=load(ICI/'bilan_6e.json')
assert bilan['statut']=='pret' and bilan['notions']==26
for r in bilan['detail']:
 d=ROOT/r['dossier'];assert load(d/'etat.json')['statut']=='pret'
 for name,h in r['empreintes_sha256'].items():assert sha(d/name)==h,(r['notion'],name,'modifie depuis validation')

# Vérifier le moteur réellement déployé, commun à la Terminale et aux autres niveaux.
site='https://www.optitab.net/'
html=urlopen(site,timeout=45).read().decode()
main=re.search(r'src="(/assets/index-[^\"]+\.js)"',html)[1]
bundle=urlopen(site+main.lstrip('/'),timeout=45).read().decode()
renderer=re.search(r'assets/scientificRenderer-[^\"]+?\.js',bundle)[0]
engine=urlopen(site+renderer,timeout=45).read().decode()
csspath=re.search(r'href="(/assets/index-[^\"]+\.css)"',html)[1]
css=urlopen(site+csspath.lstrip('/'),timeout=45).read().decode()
assert all(x in engine for x in ('optitab','resultat','otm-q-num','otm-box'))
assert all(x in css for x in ('.otm.otm','otm-box--resultat','otm-box--objectifs'))
template={'site':site,'renderer':renderer,'css':csspath,'moteur_v1':True,'moteur_commun_avec_terminale_et_5e':True}
save(ICI/'preuve_moteur_public_6e.json',template)

# L'adaptation du vérificateur inclut les deux nouveaux cours et cinq fiches.
def charger_meta(d):
 m=load(d/'source_en_ligne/meta.json')
 if (d/'cours_nouveau.txt').exists():m['cours'].append({'id':'nouveau','titre':m['titre'],'images':[]})
 if (d/'fiche_nouvelle.txt').exists():m['fiches'].append({'id':'nouvelle','titre':m['titre'],'images':[]})
 if (d/'exercices.txt').exists():
  for b in re.split(r'^===[ \t]*$',(d/'exercices.txt').read_text(encoding='utf-8'),flags=re.M):
   ident=re.search(r'^Id:\s*(nouveau-\d+)\s*$',b,re.M)
   if ident:m['exercices'].append({'id':ident[1],'titre':b.strip().splitlines()[0].replace('=== ','',1),'images':[]})
 return m
vs=(OUTILS/'verifier_notion.py').read_text(encoding='utf-8')
vs=vs.replace('meta = json.loads((dossier / "source_en_ligne" / "meta.json").read_text(encoding="utf-8"))','meta = charger_meta(dossier)')
vn={'__file__':str(OUTILS/'verifier_notion.py'),'__name__':'verification_nouveaux_documents_6e','charger_meta':charger_meta}
sys.path.insert(0,str(OUTILS));exec(compile(vs,str(OUTILS/'verifier_notion.py'),'exec'),vn)
import subprocess
original_run=subprocess.run
def local_run(args,*a,**kw):
 if isinstance(args,list) and len(args)>1 and Path(args[1]).name=='apercu_notion.mjs':
  args=[args[0],str(ICI/'apercu_6e_local.mjs'),*args[2:]]
 return original_run(args,*a,**kw)
vn['subprocess'].run=local_run
script=OUTILS/'importer_v1.py';source=script.read_text(encoding='utf-8')
assert source.rstrip().endswith('main()')
ns={'__file__':str(script),'__name__':'orchestration_6e'}
exec(compile(source.rstrip()[:-len('main()')],str(script),'exec'),ns)
ns['verifier_notion'].verifier=vn['verifier']

preps=[];rows=[];refus=[]
def guard_new_docs(prep):
 m=prep['meta'];d=prep['dossier']
 if (d/'cours_nouveau.txt').exists():assert not m['cours'] and not Cours.objects.filter(notion_id=m['notion']).exists(),'cours cree depuis export'
 if (d/'fiche_nouvelle.txt').exists():assert not m['fiches'] and not SynthesisSheet.objects.filter(notion_id=m['notion']).exists(),'fiche creee depuis export'
 if not m['exercices']:assert not Exercice.objects.filter(notion_id=m['notion']).exists(),'exercices crees depuis export'
with (ICI/'preparation_publication_6e.log').open('w',encoding='utf-8') as log,contextlib.redirect_stdout(log):
 for r in bilan['detail']:
  prep,errors=ns['preparer'](ROOT/r['dossier'])
  if errors:refus.append({'notion':r['notion'],'erreurs':errors});continue
  guard_new_docs(prep);preps.append(prep)
  rows.append({'notion':r['notion'],'anciens_exercices':len(prep['textes']['exercices']),'nouveaux_exercices':len(prep['nouveaux']),'images':{k:len(v) for k,v in prep['plan'].items()}})
report={'date':datetime.datetime.now().isoformat(timespec='seconds'),'mode':MODE,'notions':rows,'refus':refus,'ecriture':False,'moteur':template}
save(ICI/'simulation_publication_6e.json',report)
print(json.dumps({'mode':MODE,'notions_pretes':len(preps),'refus':refus},ensure_ascii=False),flush=True)
if refus or len(preps)!=26:raise SystemExit(2)
if MODE=='simulation':raise SystemExit(0)

states={p['dossier']/'etat.json':(p['dossier']/'etat.json').read_bytes() for p in preps}
imports=[];images=[]
try:
 with transaction.atomic():
  for prep in preps:
   d=prep['dossier'];nid=prep['meta']['notion']
   with (ICI/'preparation_publication_6e.log').open('a',encoding='utf-8') as log,contextlib.redirect_stdout(log):
    fresh,errors=ns['preparer'](d)
   assert not errors,(nid,errors);guard_new_docs(fresh)
   backup,errors=ns['appliquer'](fresh);assert not errors,(nid,errors)
   sauvegarde=load(backup);sauvegarde['documents_crees']=[]
   docs={'cours':{str(i):i for i in fresh['textes']['cours']},'fiches':{str(i):i for i in fresh['textes']['fiches']}}
   for genre,Model,field,filename,key in [('cours',Cours,'contenu','cours_nouveau.txt','nouveau'),('fiches',SynthesisSheet,'summary','fiche_nouvelle.txt','nouvelle')]:
    if not (d/filename).exists():continue
    text=ns['corps_doc'](d/filename)
    obj=Model.objects.create(notion_id=nid,titre=fresh['meta']['titre'],access_scope='paid',**{field:text})
    docs[genre][key]=obj.id
    sauvegarde['documents_crees'].append({'genre':genre,'id':obj.id,'fichier':filename,'sha256':sha(d/filename)})
    corr=load(d/'figures/correspondance.json')
    for pos,v in corr.get(genre,{}).get(key,{}).items():
     ModelImage,fk,leg=ns['MODELES'][genre];png=d/'figures/images'/v['fichier'];im=ModelImage(**{fk:obj.id,'position':int(pos)})
     with png.open('rb') as f:im.image.save(f'v1_n{nid}_{genre[:2]}{obj.id}_{pos}_{png.name}',File(f),save=False)
     im.width,im.height=ns['taille_affichage'](png);im.alt_text=v['alt'][:255];im.save()
     sauvegarde['images_creees'].append({'modele':ModelImage.__name__,'id':im.id})
   save(backup,sauvegarde)
   exids={str(e['id']):e['id'] for e in fresh['meta']['exercices']}
   exids.update({e['cle']:e['id'] for e in sauvegarde['exercices_crees']})
   record={'notion':nid,'dossier':d.name,'sauvegarde':str(backup),'cours':docs['cours'],'fiches':docs['fiches'],'exercices':exids}
   # Relecture exhaustive avant validation de la transaction globale.
   for genre,Model,field,prefix in [('cours',Cours,'contenu','cours_'),('fiches',SynthesisSheet,'summary','fiche_')]:
    for key,oid in docs[genre].items():assert getattr(Model.objects.get(id=oid),field)==ns['corps_doc'](d/f'{prefix}{key}.txt')
   final=ns['exercices_finaux'](d/'exercices.txt')
   for key,oid in exids.items():
    expect=final[int(key) if key.isdigit() else key];obj=Exercice.objects.get(id=oid)
    assert (obj.titre,obj.difficulty)==(expect['titre'],expect['difficulty'])
    assert all(getattr(obj,k)==v for k,v in expect['champs'].items())
   corr=load(d/'figures/correspondance.json')
   for genre,mapping in [('cours',docs['cours']),('fiches',docs['fiches']),('exercices',exids)]:
    for key,oid in mapping.items():
     for im in ns['images_en_base'](genre,oid):
      assert im.width and im.height and im.alt_text
      expected=corr.get(genre,{}).get(key,{}).get(str(im.position))
      assert expected,(nid,genre,oid,im.position,'image non remplacee')
      png=d/'figures/images'/expected['fichier']
      images.append({'notion':nid,'dossier':d.name,'genre':genre,'proprietaire':oid,'cle':key,'id':im.id,'position':im.position,'url':im.image.url,'fichier':expected['fichier'],'sha256':sha(png),'width':im.width,'height':im.height})
   imports.append(record);print('Import et relecture complete :',nid,flush=True)
except BaseException:
 for p,content in states.items():p.write_bytes(content)
 raise
report.update(ecriture=True,statut='importe_et_relu',imports=imports,images_a_verifier_http=len(images))
save(ICI/'publication_6e.json',report);save(ICI/'images_publiees_6e.json',images)
print(json.dumps({'statut':report['statut'],'notions':len(imports),'images_a_verifier_http':len(images)},ensure_ascii=False),flush=True)
