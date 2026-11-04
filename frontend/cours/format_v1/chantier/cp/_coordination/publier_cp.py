"""Création contrôlée du seul contexte CP, simulation par défaut.

Réutilise les opérations officielles d'import pour les exercices et leurs images.
L'ensemble de la nouvelle hiérarchie et de ses contenus est transactionnel.
"""
from pathlib import Path
import os,sys,json,hashlib,re,datetime,base64
from urllib.request import urlopen
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent;REPO=ICI.parents[5];OUTILS=ROOT.parents[1]/'outils'
sys.stdout.reconfigure(encoding='utf-8');sys.stderr.reconfigure(encoding='utf-8')
os.chdir(REPO/'backend');sys.path.insert(0,str(REPO/'backend'));os.environ.setdefault('DJANGO_SETTINGS_MODULE','backendAPI.settings')
import django
print('Préparation de la connexion au service de publication.',flush=True)
django.setup()
print('Service de publication chargé ; vérification des contenus et du contexte CP.',flush=True)
from django.db import transaction
from django.core.files import File
from pays.models import Pays,Niveau
from curriculum.models import Matiere,MatiereContexte,Theme,Notion,Exercice
from cours.models import Cours
from synthesis.models import SynthesisSheet
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def title(p):return p.read_text(encoding='utf-8').splitlines()[0].removeprefix('Titre: ').strip()
bilan=load(ICI/'bilan_cp.json');assert bilan['statut']=='pret' and bilan['notions']==30
assert bilan['cours']==bilan['fiches']==30 and bilan['exercices']==270 and bilan['questions']==1350
assert len(bilan['detail'])==30 and {r['numero'] for r in bilan['detail']}==set(range(1,31))
for r in bilan['detail']:
 d=ROOT/r['dossier'];assert load(d/'etat.json')['statut']=='pret'
 for name,h in r['empreintes_sha256'].items():assert sha(d/name)==h,(r['numero'],name,'modifie depuis validation')
assert not (ICI/'publication_cp.json').exists(),'Publication deja executee : ne pas recreer le contexte.'
inventaire=load(ICI/'inventaire_base_cp.json');assert not inventaire['niveaux'] and not inventaire['contextes']
pays=Pays.objects.get(nom='France');matiere=Matiere.objects.get(id=1)
assert matiere.est_actif and matiere.titre.casefold() in ('mathématiques','mathematiques','maths')
assert not Niveau.objects.filter(pays=pays,nom__iexact='CP').exists(),'Un niveau CP est apparu depuis inventaire : relecture necessaire.'
print('Niveau CP à créer ; vérification du moteur public.',flush=True)
# Vérification du moteur effectivement en production, commun à tous les niveaux.
base='https://www.optitab.net/';html=urlopen(base,timeout=45).read().decode()
main=re.search(r'src="(/assets/index-[^\"]+\.js)"',html)[1]
bundle=urlopen(base+main.lstrip('/'),timeout=45).read().decode();renderer=re.search(r'assets/scientificRenderer-[^\"]+?\.js',bundle)[0]
engine=urlopen(base+renderer,timeout=45).read().decode();csspath=re.search(r'href="(/assets/index-[^\"]+\.css)"',html)[1];css=urlopen(base+csspath.lstrip('/'),timeout=45).read().decode()
assert all(s in engine for s in ('optitab','resultat','otm-q-num','otm-box')) and all(s in css for s in ('.otm.otm','otm-box--resultat','otm-box--objectifs'))
save(ICI/'preuve_moteur_public_cp.json',{'site':base,'renderer':renderer,'css':csspath,'moteur_commun_6e_5e_terminale':True})
script=OUTILS/'importer_v1.py';source=script.read_text(encoding='utf-8');assert source.rstrip().endswith('main()')
ns={'__file__':str(script),'__name__':'creation_cp'};sys.path.insert(0,str(OUTILS));exec(compile(source.rstrip()[:-len('main()')],str(script),'exec'),ns)
plans=[]
for r in bilan['detail']:
 d=ROOT/r['dossier'];finaux=ns['exercices_finaux'](d/'exercices.txt');assert len(finaux)==r['exercices'] and all(isinstance(k,str) and k.startswith('nouveau-') for k in finaux)
 plans.append({'numero':r['numero'],'dossier':d.name,'exercices':len(finaux),'images':r['positions_images']})
simulation={'mode':'simulation','contexte_existant':False,'creation_niveau':True,'niveau':None,'niveau_cree':None,'niveau_nom':'CP','niveau_ordre':0,'pays':pays.id,'pays_nom':'France','matiere':matiere.id,'notions':plans,'empreinte_bilan':sha(ICI/'bilan_cp.json'),'ecriture':False}
simulation_path=ICI/'simulation_publication_cp.json'
if '--appliquer' not in sys.argv:
 save(simulation_path,simulation);print(json.dumps({'mode':'simulation','chapitres_prets':len(plans),'creation_niveau':True,'conflits':0}),flush=True)
 raise SystemExit(0)
assert simulation_path.is_file(),'Executer d’abord la simulation sans --appliquer.'
assert load(simulation_path)==simulation,'La simulation doit correspondre au bilan et au contexte actuels.'
backupdir=ICI/'sauvegardes';backupdir.mkdir(exist_ok=True);backup=backupdir/f'avant_creation_cp_{datetime.datetime.now():%Y%m%d-%H%M%S-%f}.json'
states={ROOT/r['dossier']/name:(ROOT/r['dossier']/name).read_bytes() for r in bilan['detail'] for name in ('etat.json','exercices.txt','figures/correspondance.json')}
snapshot={'date':datetime.datetime.now().isoformat(timespec='seconds'),'statut':'creation_en_cours','creation_niveau':True,'niveau':None,'niveau_cree':None,'niveau_existant_avant':False,'pays':pays.id,'niveau_nom':'CP','niveau_ordre':0,'matiere':matiere.id,'contexte_existant_avant':False,'contexte_cree':None,'themes_crees':[],'notions_creees':[],'fichiers_locaux_avant':{str(p):base64.b64encode(data).decode('ascii') for p,data in states.items()}}
save(backup,snapshot);imports=[];images=[]
try:
 with transaction.atomic():
  # Le niveau n’existe pas encore : verrouiller son pays avant de le créer.
  pays=Pays.objects.select_for_update().get(id=pays.id,nom='France')
  assert not Niveau.objects.filter(pays=pays,nom__iexact='CP').exists(),'Un niveau CP est apparu : aucune creation.'
  assert not (ICI/'publication_cp.json').exists(),'Publication concurrente détectée.'
  assert sha(ICI/'bilan_cp.json')==simulation['empreinte_bilan'],'Bilan modifié après simulation.'
  for row in bilan['detail']:
   d=ROOT/row['dossier'];assert load(d/'etat.json')['statut']=='pret'
   for name,h in row['empreintes_sha256'].items():assert sha(d/name)==h,(row['numero'],name,'modifié avant création')
  niveau=Niveau.objects.create(pays=pays,nom='CP',ordre=0,est_actif=True)
  snapshot.update(niveau=niveau.id,niveau_cree=niveau.id);save(backup,snapshot)
  contexte=MatiereContexte.objects.create(niveau=niveau,matiere=matiere,titre='Mathématiques — CP',est_actif=True)
  snapshot['contexte_cree']=contexte.id;save(backup,snapshot)
  themes={}
  for row in bilan['detail']:
   d=ROOT/row['dossier'];theme_title=row['theme']
   if theme_title not in themes:
    theme=Theme.objects.create(contexte=contexte,matiere=matiere,titre=theme_title,ordre=len(themes)+1,est_actif=True);themes[theme_title]=theme
    snapshot['themes_crees'].append(theme.id)
   notion=Notion.objects.create(theme=themes[theme_title],titre=row['titre'],ordre=row['numero'],est_actif=True)
   snapshot['notions_creees'].append(notion.id);save(backup,snapshot)
   corr=load(d/'figures/correspondance.json');finaux=ns['exercices_finaux'](d/'exercices.txt')
   newfigs={k:[(int(p),d/'figures/images'/v['fichier'],v['alt']) for p,v in corr.get('exercices',{}).get(k,{}).items()] for k in finaux}
   prep={'dossier':d,'meta':{'notion':notion.id,'cours':[],'fiches':[],'exercices':[]},'textes':{'cours':{},'fiches':{},'exercices':{}},'plan':{'remplacer':[],'creer':[],'supprimer':[]},'renommer':{},'nouveaux':finaux,'figures_nouveaux':newfigs}
   localbackup,errors=ns['appliquer'](prep);assert not errors;old=load(localbackup);old['documents_crees']=[]
   docs={}
   for genre,Model,field,name,key in [('cours',Cours,'contenu','cours_nouveau.txt','nouveau'),('fiches',SynthesisSheet,'summary','fiche_nouvelle.txt','nouvelle')]:
    obj=Model.objects.create(notion=notion,titre=title(d/name),access_scope='paid',**{field:ns['corps_doc'](d/name)})
    docs[genre]={key:obj.id};old['documents_crees'].append({'genre':genre,'id':obj.id})
    for pos,v in corr.get(genre,{}).get(key,{}).items():
     ModelImage,fk,_=ns['MODELES'][genre];im=ModelImage(**{fk:obj.id,'position':int(pos)});png=d/'figures/images'/v['fichier']
     with png.open('rb') as f:im.image.save(f'v1_n{notion.id}_{genre[:2]}{obj.id}_{pos}_{png.name}',File(f),save=False)
     im.width,im.height=ns['taille_affichage'](png);im.alt_text=v['alt'][:255];im.save();old['images_creees'].append({'modele':ModelImage.__name__,'id':im.id})
   save(localbackup,old);exids={v['cle']:v['id'] for v in old['exercices_crees']};assert len(exids)==row['exercices']
   for key,oid in exids.items():
    obj=Exercice.objects.get(id=oid);expected=finaux[key]
    assert (obj.notion_id,obj.titre,obj.difficulty,obj.est_actif)==(notion.id,expected['titre'],expected['difficulty'],True)
    assert all(getattr(obj,k)==v for k,v in expected['champs'].items()) and obj.contenu==expected['champs']['question']
   for genre,Model,field,name in [('cours',Cours,'contenu','cours_nouveau.txt'),('fiches',SynthesisSheet,'summary','fiche_nouvelle.txt')]:
    obj=Model.objects.get(id=next(iter(docs[genre].values())));assert getattr(obj,field)==ns['corps_doc'](d/name) and obj.notion_id==notion.id
   for genre,mapping in [('cours',docs['cours']),('fiches',docs['fiches']),('exercices',exids)]:
    for key,oid in mapping.items():
     actual=ns['images_en_base'](genre,oid);expected=corr.get(genre,{}).get(key,{})
     assert {im.position for im in actual}==set(map(int,expected)),(row['numero'],genre,key)
     for im in actual:
      spec=expected[str(im.position)];png=d/'figures/images'/spec['fichier'];assert im.alt_text==spec['alt'][:255] and (im.width,im.height)==ns['taille_affichage'](png)
      images.append({'numero':row['numero'],'notion':notion.id,'genre':genre,'id':im.id,'position':im.position,'url':im.image.url,'sha256':sha(png),'fichier':spec['fichier']})
   record={'numero':row['numero'],'notion':notion.id,'dossier':d.name,'titre':row['titre'],'cours':docs['cours'],'fiches':docs['fiches'],'exercices':exids,'sauvegarde':str(localbackup)};imports.append(record)
   print('Création et relecture complètes :',row['numero'],flush=True)
  assert Notion.objects.filter(theme__contexte=contexte,est_actif=True).count()==30
  assert Exercice.objects.filter(notion__theme__contexte=contexte,est_actif=True).count()==bilan['exercices']
  assert Cours.objects.filter(notion__theme__contexte=contexte).count()==30
  assert SynthesisSheet.objects.filter(notion__theme__contexte=contexte).count()==30
except BaseException:
 for p,data in states.items():p.write_bytes(data)
 snapshot['statut']='creation_annulee_transaction_annulee';save(backup,snapshot)
 raise
snapshot['statut']='creation_validee';save(backup,snapshot)
report={**simulation,'mode':'appliquer','statut':'importe_et_relu','ecriture':True,'contexte':contexte.id,'niveau':niveau.id,'niveau_cree':niveau.id,'imports':imports,'sauvegarde_hierarchie':str(backup),'images_a_verifier_http':len(images)}
save(ICI/'publication_cp.json',report);save(ICI/'images_publiees_cp.json',images)
print(json.dumps({'statut':report['statut'],'chapitres':len(imports),'images':len(images)}),flush=True)
