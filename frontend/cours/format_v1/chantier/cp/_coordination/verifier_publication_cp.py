"""Relecture HTTP locale/publique et téléchargement de chaque image publiée."""
from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
import os,sys,json,re,hashlib,datetime
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent;REPO=ICI.parents[5]
os.chdir(REPO/'backend');sys.path.insert(0,str(REPO/'backend'));os.environ.setdefault('DJANGO_SETTINGS_MODULE','backendAPI.settings')
sys.stdout.reconfigure(encoding='utf-8')
import django
django.setup()
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from pays.models import Niveau
from curriculum.models import MatiereContexte
def load(p):return json.loads(p.read_text(encoding='utf-8'))
pub=load(ICI/'publication_cp.json');assert pub['statut'] in ('importe_et_relu','publie_et_verifie')
assert pub['ecriture'] and pub['creation_niveau'] and pub['niveau']==pub['niveau_cree']
assert len(pub['imports'])==30 and {r['numero'] for r in pub['imports']}==set(range(1,31))
assert sum(len(r['exercices']) for r in pub['imports'])==270
niveau=Niveau.objects.get(id=pub['niveau'],nom='CP',pays__nom='France',ordre=0)
assert niveau.est_actif and MatiereContexte.objects.filter(id=pub['contexte'],niveau=niveau,matiere_id=1,est_actif=True).exists()
user=get_user_model().objects.filter(is_superuser=True,is_active=True).first();assert user
token=str(AccessToken.for_user(user));tasks=[]
previous=load(ICI/'verification_publication_http_cp.json') if '--reprendre' in sys.argv else None
if previous:
 assert previous['niveau']==pub['niveau'] and previous['contexte']==pub['contexte']
 backup=ICI/'verification_publication_http_cp_premier_passage.json'
 if not backup.exists():backup.write_text(json.dumps(previous,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
api_valides={r['url']:r for r in previous['api'] if r['ok']} if previous else {}
images_valides={(r['notion'],r.get('genre'),r['id']):r for r in previous['images'] if r['ok']} if previous else {}
def body(p):
 text=p.read_text(encoding='utf-8');return text[text.index('<!-- optitab:1 -->'):].strip()
for r in pub['imports']:
 d=ROOT/r['dossier']
 for genre,field,prefix,filename in [('cours','contenu','/api/cours/cours/','cours_nouveau.txt'),('fiches','summary','/api/sheets/','fiche_nouvelle.txt')]:
  oid=next(iter(r[genre].values()))
  for base in ('http://localhost:3000','https://optitab-backend.onrender.com'):tasks.append((r['notion'],base+prefix+str(oid)+'/',field,body(d/filename)))
 key=next(iter(r['exercices']));oid=r['exercices'][key]
 b=next(b for b in re.split(r'^===[ \t]*$',(d/'exercices.txt').read_text(encoding='utf-8'),flags=re.M) if re.search(r'^Id:\s*(?:'+re.escape(key)+'|'+str(oid)+r')\s*$',b,re.M))
 expected=b.split('Énoncé:')[1].split('Étapes:')[0].strip()
 for base in ('http://localhost:3000','https://optitab-backend.onrender.com'):tasks.append((r['notion'],base+'/api/exercices/'+str(oid)+'/','question',expected))
assert len(tasks)==180 and len({url for _,url,_,_ in tasks})==180
def check_api(item):
 notion,url,field,expected=item
 if url in api_valides:return api_valides[url]
 try:
  with urlopen(Request(url,headers={'Authorization':'Bearer '+token,'Accept':'application/json'}),timeout=60) as response:data=json.load(response)
  return {'notion':notion,'url':url,'ok':data.get(field)==expected}
 except Exception as e:return {'notion':notion,'url':url,'ok':False,'erreur':type(e).__name__}
with ThreadPoolExecutor(max_workers=4) as pool:api=list(pool.map(check_api,tasks))
print('Contenus conformes',sum(r['ok'] for r in api),'/',len(api),flush=True)
def check_image(im):
 key=(im['notion'],im['genre'],im['id'])
 if key in images_valides:return images_valides[key]
 try:
  with urlopen(im['url'],timeout=60) as response:actual=hashlib.sha256(response.read()).hexdigest()
  return {'notion':im['notion'],'genre':im['genre'],'id':im['id'],'ok':actual==im['sha256']}
 except Exception as e:return {'notion':im['notion'],'id':im['id'],'ok':False,'erreur':type(e).__name__}
with ThreadPoolExecutor(max_workers=4) as pool:images=list(pool.map(check_image,load(ICI/'images_publiees_cp.json')))
navigation=[];expected={r['notion'] for r in pub['imports']}
for base in ('http://localhost:3000','https://optitab-backend.onrender.com'):
 try:
  url=base+f"/api/notions/?contexte={pub['contexte']}&niveau={pub['niveau']}"
  with urlopen(Request(url,headers={'Accept':'application/json'}),timeout=60) as response:items=json.load(response)
  if isinstance(items,dict):items=items['results']
  navigation.append({'serveur':base,'ok':{r['id'] for r in items}==expected,'notions_visibles':len(items)})
 except Exception as e:navigation.append({'serveur':base,'ok':False,'erreur':type(e).__name__})
report={'date':datetime.datetime.now().isoformat(timespec='seconds'),'statut':'OK' if all(r['ok'] for r in api+images+navigation) else 'a_verifier','niveau':pub['niveau'],'contexte':pub['contexte'],'api':api,'images':images,'navigation':navigation,'api_ok':sum(r['ok'] for r in api),'images_ok':sum(r['ok'] for r in images)}
(ICI/'verification_publication_http_cp.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ('statut','api_ok','images_ok','navigation')}),flush=True)
if report['statut']!='OK':
 print(json.dumps({'ecarts':[r for r in api+images+navigation if not r['ok']]}),flush=True)
 raise SystemExit(2)
