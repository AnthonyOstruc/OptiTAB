"""Relecture HTTP de la publication, sur localhost et le serveur public.

Les jetons temporaires restent en mémoire ; aucune information d'identité ou
d'authentification n'est écrite dans les rapports. Lecture seule de la base.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
import json,os,sys,re,hashlib,datetime,time
sys.stdout.reconfigure(encoding='utf-8')
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent;BACKEND=ICI.parents[5]/'backend'
os.chdir(BACKEND);sys.path.insert(0,str(BACKEND));os.environ.setdefault('DJANGO_SETTINGS_MODULE','backendAPI.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def body(p):
 text=p.read_text(encoding='utf-8');return text[text.index('<!-- optitab:1 -->'):].strip()
pub=load(ICI/'publication_6e.json')
assert pub['statut'] in ('importe_et_relu','publie_et_verifie')
user=get_user_model().objects.filter(is_superuser=True,is_active=True).first();assert user is not None
token=str(AccessToken.for_user(user))
tasks=[]
for r in pub['imports']:
 d=ROOT/r['dossier']
 for genre,field,prefix,filename in [('cours','contenu','/api/cours/cours/','cours_'),('fiches','summary','/api/sheets/','fiche_')]:
  for key,oid in r[genre].items():
   expected=body(d/f'{filename}{key}.txt')
   for base in ('http://localhost:3000','https://optitab-backend.onrender.com'):tasks.append((r['notion'],base+prefix+str(oid)+'/',field,expected))
 first=next(iter(r['exercices']));oid=r['exercices'][first]
 raw=(d/'exercices.txt').read_text(encoding='utf-8')
 b=next(b for b in re.split(r'^===[ \t]*$',raw,flags=re.M) if re.search(r'^Id:\s*'+re.escape(first)+r'\s*$',b,re.M))
 expected=b.split('Énoncé:')[1].split('Étapes:')[0].strip()
 for base in ('http://localhost:3000','https://optitab-backend.onrender.com'):tasks.append((r['notion'],base+'/api/exercices/'+str(oid)+'/','question',expected))
def check_api(item):
 notion,url,field,expected=item
 for attempt in range(2):
  try:
   req=Request(url,headers={'Authorization':'Bearer '+token,'Accept':'application/json'})
   with urlopen(req,timeout=60) as response:data=json.load(response)
   return {'notion':notion,'url':url,'statut':200,'ok':data.get(field)==expected}
  except HTTPError as e:
   if attempt==0 and e.code in (429,500,502,503,504):time.sleep(1);continue
   return {'notion':notion,'url':url,'statut':e.code,'ok':False}
  except Exception as e:
   if attempt==0:time.sleep(1);continue
   return {'notion':notion,'url':url,'erreur':type(e).__name__,'ok':False}
with ThreadPoolExecutor(max_workers=4) as pool:api=list(pool.map(check_api,tasks))
print('Contenus servis conformes :',sum(r['ok'] for r in api),'/',len(api),flush=True)
def check_image(im):
 for attempt in range(2):
  try:
   with urlopen(im['url'],timeout=60) as response:actual=sha(response.read())
   return {'notion':im['notion'],'genre':im['genre'],'id':im['id'],'position':im['position'],'ok':actual==im['sha256']}
  except Exception as e:
   if attempt==0:time.sleep(1);continue
   return {'notion':im['notion'],'id':im['id'],'ok':False,'erreur':type(e).__name__}
with ThreadPoolExecutor(max_workers=4) as pool:images=list(pool.map(check_image,load(ICI/'images_publiees_6e.json')))
report={'date':datetime.datetime.now().isoformat(timespec='seconds'),'statut':'OK' if all(r['ok'] for r in api+images) else 'a_verifier','api':api,'images':images,'api_ok':sum(r['ok'] for r in api),'images_ok':sum(r['ok'] for r in images)}
(ICI/'verification_publication_http_6e.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ('statut','api_ok','images_ok')}),flush=True)
if report['statut']!='OK':
 print(json.dumps({'ecarts_api':[r for r in api if not r['ok']],'ecarts_images':[r for r in images if not r['ok']]}),flush=True)
 raise SystemExit(2)
