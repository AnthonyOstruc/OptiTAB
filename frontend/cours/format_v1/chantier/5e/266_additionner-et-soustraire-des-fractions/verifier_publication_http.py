"""Relecture HTTP des contenus publiés et de chaque image, sans écriture en base.

Jeton de lecture temporaire conservé uniquement en mémoire ; jamais imprimé.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
import os,sys,json,hashlib,re,datetime
sys.stdout.reconfigure(encoding='utf-8')
ICI=Path(__file__).resolve().parent;BACKEND=ICI.parents[5]/'backend'
os.chdir(BACKEND);sys.path.insert(0,str(BACKEND));os.environ.setdefault('DJANGO_SETTINGS_MODULE','backendAPI.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
bilan=load(ICI/'bilan_5e.json');pub=load(ICI/'publication_5e.json')
assert pub['statut']=='importe_et_relu'
user=get_user_model().objects.filter(is_superuser=True,is_active=True).first()
assert user is not None,'Compte de vérification absent'
token=str(AccessToken.for_user(user))
tasks=[]
for r in bilan['detail']:
    d=ICI.parent/r['dossier'];meta=load(d/'source_en_ligne/meta.json')
    for category,field,prefix in [('cours','contenu','/api/cours/cours/'),('fiches','summary','/api/sheets/')]:
        for item in meta[category]:
            filename=('cours_' if category=='cours' else 'fiche_')+str(item['id'])+'.txt'
            t=(d/filename).read_text(encoding='utf-8');expected=t[t.index('<!-- optitab:1 -->'):].strip()
            for base in ('http://localhost:3000','https://optitab-backend.onrender.com'):
                tasks.append((base+prefix+str(item['id'])+'/',field,expected,r['notion']))
    extext=(d/'exercices.txt').read_text(encoding='utf-8')
    b=next(b for b in re.split(r'^===[ \t]*$',extext,flags=re.M) if 'Id:' in b)
    eid=re.search(r'^Id: (\d+)',b,re.M)[1];expected=b.split('Énoncé:')[1].split('Étapes:')[0].strip()
    for base in ('http://localhost:3000','https://optitab-backend.onrender.com'):
        tasks.append((base+'/api/exercices/'+eid+'/', 'question',expected,r['notion']))

def check_api(item):
    url,field,expected,notion=item
    try:
        req=Request(url,headers={'Authorization':'Bearer '+token,'Accept':'application/json'})
        with urlopen(req,timeout=60) as r:data=json.load(r)
        return {'notion':notion,'url':url,'ok':data.get(field)==expected,'statut':200}
    except HTTPError as e:return {'notion':notion,'url':url,'ok':False,'statut':e.code}
    except Exception as e:return {'notion':notion,'url':url,'ok':False,'erreur':type(e).__name__}
with ThreadPoolExecutor(max_workers=4) as pool:api=list(pool.map(check_api,tasks))
print('Relecture API :',sum(r['ok'] for r in api),'/',len(api),flush=True)

imtasks=[]
for im in load(ICI/'images_publiees_5e.json'):
    d=next(ICI.parent.glob(str(im['notion'])+'_*'));corr=load(d/'figures/correspondance.json')
    expected=corr[im['genre']][str(im['proprietaire'])][str(im['position'])]['fichier']
    imtasks.append((im,sha((d/'figures/images'/expected).read_bytes())))
def check_image(item):
    im,expected=item
    try:
        with urlopen(im['url'],timeout=60) as r:actual=sha(r.read())
        return {'notion':im['notion'],'id':im['id'],'position':im['position'],'ok':actual==expected}
    except Exception as e:return {'notion':im['notion'],'id':im['id'],'ok':False,'erreur':type(e).__name__}
with ThreadPoolExecutor(max_workers=4) as pool:images=list(pool.map(check_image,imtasks))
report={'date':datetime.datetime.now().isoformat(timespec='seconds'),'api':api,'images':images,'api_ok':sum(r['ok'] for r in api),'images_ok':sum(r['ok'] for r in images),'statut':'OK' if all(r['ok'] for r in api+images) else 'a_verifier'}
(ICI/'verification_publication_http.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ('statut','api_ok','images_ok')},ensure_ascii=False),flush=True)
if report['statut']!='OK':
    print(json.dumps({'api_en_ecart':[r for r in api if not r['ok']],'images_en_ecart':[r for r in images if not r['ok']]},ensure_ascii=False),flush=True)
    raise SystemExit(2)
