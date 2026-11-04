"""Publication autorisée de la seule 5e, via l'importeur officiel.

Simulation par défaut. Vérifie les empreintes de validation, le moteur public,
la concurrence, puis applique sous une transaction globale avec sauvegardes.
Aucun secret ni jeton n'est imprimé ou enregistré par ce script.
"""
from pathlib import Path
import os,sys,json,hashlib,datetime,contextlib
from urllib.request import urlopen
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

ICI=Path(__file__).resolve().parent
ROOT=ICI.parents[5]
BACKEND=ROOT/'backend'
OUTILS=ICI.parents[2]/'outils'
MODE='appliquer' if '--appliquer' in sys.argv else 'simulation'
os.chdir(BACKEND);sys.path.insert(0,str(BACKEND))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','backendAPI.settings')
import django
django.setup()
from django.db import transaction,connection
from django.core.files.storage import default_storage

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
bilan=load(ICI/'bilan_5e.json')
assert bilan['notions']==20 and bilan['exercices']==420 and bilan['statut']=='pret'
assert {r['notion'] for r in bilan['detail']}==set(range(261,281))
for r in bilan['detail']:
    d=ICI.parent/r['dossier']
    for filename,h in r['empreintes_sha256'].items():assert sha(d/filename)==h,(r['notion'],filename,'modifié depuis validation')

# Contrôle public du moteur commun avant d'envoyer un seul contenu v1.
base='https://www.optitab.net/'
import re
html=urlopen(base,timeout=45).read().decode()
main=re.search(r'src="(/assets/index-[^\"]+\.js)"',html)[1]
bundle=urlopen(base+main.lstrip('/'),timeout=45).read().decode()
renderer=re.search(r'assets/scientificRenderer-[\w-]+\.js',bundle)[0]
engine=urlopen(base+renderer,timeout=45).read().decode()
css_path=re.search(r'href="(/assets/index-[^\"]+\.css)"',html)[1]
css=urlopen(base+css_path.lstrip('/'),timeout=45).read().decode()
assert all(s in engine for s in ('optitab','resultat','otm-q-num','otm-box')) and all(s in css for s in ('.otm.otm','otm-box--resultat','otm-box--objectifs')),'Moteur v1 public absent'
template={'site':base,'renderer':renderer,'css':css_path,'moteur_v1':True,'meme_moteur_pour_tous_les_niveaux':True}
(ICI/'preuve_moteur_public.json').write_text(json.dumps(template,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Charger les fonctions actuelles sans lancer main (les outils communs restent intacts).
script=OUTILS/'importer_v1.py';source=script.read_text(encoding='utf-8')
assert source.rstrip().endswith('main()')
ns={'__file__':str(script),'__name__':'orchestration_publication_5e'}
exec(compile(source.rstrip()[:-len('main()')],str(script),'exec'),ns)
preps=[];records=[];refus=[]
with (ICI/'preparation_import_5e.log').open('w',encoding='utf-8') as log,contextlib.redirect_stdout(log):
    for r in bilan['detail']:
        d=ICI.parent/r['dossier'];prep,errors=ns['preparer'](d)
        if errors:
            refus.append({'notion':r['notion'],'raisons':errors});continue
        assert prep['meta']['notion']==r['notion'] and not prep['nouveaux']
        preps.append(prep)
        records.append({'notion':r['notion'],'cours':list(prep['textes']['cours']),'fiches':list(prep['textes']['fiches']),'exercices':len(prep['textes']['exercices']),'titres_ou_niveaux_corriges':len(prep['renommer']),'images':{k:len(v) for k,v in prep['plan'].items()}})
report={'date':datetime.datetime.now().isoformat(timespec='seconds'),'mode':MODE,'base':'distante' if connection.settings_dict['HOST'] not in ('localhost','127.0.0.1','') else 'locale','stockage':type(default_storage).__name__,'moteur':template,'notions':records,'refus':refus,'ecriture':False}
(ICI/'simulation_import_5e.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'mode':MODE,'notions_pretes':len(preps),'refus':refus,'images':{k:sum(r['images'][k] for r in records) for k in ('remplacer','creer','supprimer')}},ensure_ascii=False),flush=True)
if refus or len(preps)!=20:raise SystemExit(2)
if MODE=='simulation':raise SystemExit(0)

states={p['dossier']/ 'etat.json':(p['dossier']/'etat.json').read_bytes() for p in preps}
imports=[]
try:
    with transaction.atomic():
        for prep in preps:
            # Refaire le contrôle de concurrence à l'instant de l'écriture.
            fresh,errors=ns['preparer'](prep['dossier'])
            if errors:raise RuntimeError(f"Notion {prep['meta']['notion']} modifiée pendant la préparation : {errors}")
            backup,errors=ns['appliquer'](fresh)
            if errors:raise RuntimeError(str(errors))
            imports.append({'notion':prep['meta']['notion'],'sauvegarde':str(backup),'statut':'importe'})
            print('Import contrôlé :',prep['meta']['notion'],flush=True)
except BaseException:
    for path,content in states.items():path.write_bytes(content)
    raise

# Relecture après validation de la transaction, puis preuve de l'ensemble des images.
from cours.models import Cours
from synthesis.models import SynthesisSheet
from curriculum.models import Exercice
images=[]
for prep in preps:
    for cid,t in prep['textes']['cours'].items():assert Cours.objects.get(id=cid).contenu==t
    for fid,t in prep['textes']['fiches'].items():assert SynthesisSheet.objects.get(id=fid).summary==t
    finaux=ns['exercices_finaux'](prep['dossier']/'exercices.txt')
    for eid,expected in finaux.items():
        e=Exercice.objects.get(id=eid)
        assert (e.titre,e.difficulty)==(expected['titre'],expected['difficulty'])
        assert all(getattr(e,k)==v for k,v in expected['champs'].items())
    for genre,items in prep['textes'].items():
        for oid in items:
            for im in ns['images_en_base'](genre,oid):
                assert im.width and im.height and im.alt_text
                assert default_storage.exists(im.image.name)
                images.append({'notion':prep['meta']['notion'],'genre':genre,'id':im.id,'proprietaire':oid,'position':im.position,'url':im.image.url,'width':im.width,'height':im.height})
report.update(ecriture=True,statut='importe_et_relu',sauvegardes=imports,images_verifiees=len(images))
(ICI/'publication_5e.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ICI/'images_publiees_5e.json').write_text(json.dumps(images,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'statut':'importe_et_relu','notions':20,'cours':20,'fiches':20,'exercices':420,'images_verifiees':len(images)},ensure_ascii=False),flush=True)
