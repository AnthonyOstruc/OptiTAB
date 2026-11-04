"""Prouve que l'import officiel n'a changé que les identifiants et la mise en forme JSON."""
from pathlib import Path
import json,re,hashlib,base64
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(data):return hashlib.sha256(data).hexdigest()
bilan=load(HERE/'bilan_cp.json');pub=load(HERE/'publication_cp.json');rows=[]
snapshot=load(Path(pub['sauvegarde_hierarchie']))
assert snapshot['statut']=='creation_validee' and snapshot['creation_niveau'] and snapshot['niveau_cree']==pub['niveau']
assert len(pub['imports'])==bilan['notions']==30
assert {r['numero'] for r in pub['imports']}==set(range(1,31))
assert len({oid for r in pub['imports'] for oid in r['exercices'].values()})==270
for r in pub['imports']:
 d=ROOT/r['dossier'];initial=next(x for x in bilan['detail'] if x['numero']==r['numero']);expected=initial.get('empreintes_validation',initial['empreintes_sha256'])
 actual=(d/'exercices.txt').read_bytes();original=actual
 for key,oid in r['exercices'].items():
  original,n=re.subn(rb'(?m)^(Id:[ \t]*)'+str(oid).encode()+rb'(?=[\r\n])',lambda m:m[1]+key.encode(),original)
  assert n==1,(d.name,key,oid,n)
 assert sha(original)==expected['exercices.txt'],(d.name,'autre modification des exercices que les identifiants')
 corr=load(d/'figures/correspondance.json');reverse={str(v):k for k,v in r['exercices'].items()}
 corr['exercices']={reverse.get(k,k):v for k,v in corr.get('exercices',{}).items()}
 # Comparer à la vraie sauvegarde antérieure à la création, y compris tous
 # les propriétaires, noms de fichiers, positions et textes alternatifs.
 originalcorr=base64.b64decode(snapshot['fichiers_locaux_avant'][str(d/'figures/correspondance.json')])
 assert sha(originalcorr)==expected['figures/correspondance.json'],(d.name,'sauvegarde non conforme à la validation')
 assert json.loads(originalcorr)==corr,(d.name,'autre modification de correspondance que les identifiants')
 proofmode='empreinte originale sauvegardée ; seules les clés des exercices ont changé'
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
(HERE/'liaison_identifiants_cp.json').write_text(json.dumps({'statut':'OK','chapitres':30,'detail':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
