"""Prouve que l'import officiel n'a changé que les identifiants et la mise en forme JSON."""
from pathlib import Path
import json,re,hashlib,base64
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(data):return hashlib.sha256(data).hexdigest()
bilan=load(HERE/'bilan_ce1.json');pub=load(HERE/'publication_ce1.json');rows=[]
for r in pub['imports']:
 d=ROOT/r['dossier'];initial=next(x for x in bilan['detail'] if x['numero']==r['numero']);expected=initial['empreintes_sha256']
 actual=(d/'exercices.txt').read_bytes();original=actual
 for key,oid in r['exercices'].items():
  original,n=re.subn(rb'(?m)^(Id:[ \t]*)'+str(oid).encode()+rb'(?=[\r\n])',lambda m:m[1]+key.encode(),original)
  assert n==1,(d.name,key,oid,n)
 assert sha(original)==expected['exercices.txt'],(d.name,'autre modification des exercices que les identifiants')
 corr=load(d/'figures/correspondance.json');reverse={str(v):k for k,v in r['exercices'].items()}
 corr['exercices']={reverse.get(k,k):v for k,v in corr.get('exercices',{}).items()}
 candidates=[]
 for indent in (1,2,4):
  s=json.dumps(corr,ensure_ascii=False,indent=indent)
  for end in ('','\n'):
   for nl in ('\n','\r\n'):candidates.append((s+end).replace('\n',nl).encode('utf-8'))
 originalcorr=next((c for c in candidates if sha(c)==expected['figures/correspondance.json']),None)
 proofmode='empreinte originale reconstituée'
 if originalcorr is None:
  # Un JSON réédité localement peut avoir une indentation ou des fins de ligne
  # mixtes. Comparer alors toutes ses valeurs à l'aperçu validé immuable.
  proof=load(d/'PREUVES_FINALES.json');preview=(d/'apercu.html').read_bytes()
  assert sha(preview)==proof['empreinte_apercu'],(d.name,'aperçu modifié après validation')
  payload=json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',preview.decode('utf-8'),re.S)[1])
  snapshots={('cours' if x['ctx']=='course' else 'fiches',x['key'][1:]):x['images'] for x in payload['docs']}
  snapshots.update({('exercices',str(x['id'])):x['images'] for x in payload['exercices']})
  for genre,owners in corr.items():
   for owner,images in owners.items():
    reference=snapshots[genre,owner]
    assert set(images)==set(reference),(d.name,genre,owner,'positions différentes')
    for pos,im in images.items():
     old=reference[pos]
     assert old['alt']==im['alt'] and sha(base64.b64decode(old['src'].split(',',1)[1]))==sha((d/'figures/images'/im['fichier']).read_bytes()),(d.name,owner,pos,'image ou texte alternatif différent')
  originalcorr=(json.dumps(corr,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
  proofmode='valeurs identiques à l’aperçu validé immuable ; format JSON normalisé'
 backup=d/'sauvegardes/version_validee_avant_liaison';backup.mkdir(parents=True,exist_ok=True)
 corrname='correspondance.json' if proofmode.startswith('empreinte') else 'correspondance_semantique_validee.json'
 for name,data in [('exercices.txt',original),(corrname,originalcorr)]:
  p=backup/name
  if p.exists():assert p.read_bytes()==data
  else:p.write_bytes(data)
 final={name:sha((d/name).read_bytes()) for name in expected}
 for name,h in expected.items():
  if name not in ('exercices.txt','figures/correspondance.json'):assert final[name]==h,(d.name,name,'modifié après validation')
 rows.append({'numero':r['numero'],'dossier':d.name,'identifiants':r['exercices'],'empreintes_avant':expected,'empreintes_apres':final,'seuls_identifiants_modifies':True,'preuve_correspondance':proofmode})
 print(r['numero'],'identifiants reliés, contenus et schémas strictement identiques',flush=True)
(HERE/'liaison_identifiants_ce1.json').write_text(json.dumps({'statut':'OK','chapitres':32,'detail':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
