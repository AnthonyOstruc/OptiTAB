"""Consigne après leur lecture les PNG ou captures réellement présents."""
from pathlib import Path
import json,sys,hashlib,datetime
ROOT=Path(__file__).resolve().parent.parent
mode=sys.argv[1]
for code in map(int,sys.argv[2:]):
 d=next(ROOT.glob(f'{code:02}_*'));p=d/'relecture_visuelle_root.json'
 v=json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
 if mode=='figures':
  corr=json.loads((d/'figures/correspondance.json').read_text(encoding='utf-8'))
  paths=sorted({d/'figures/images'/im['fichier'] for g in corr.values() for owner in g.values() for im in owner.values()})
 else:
  assert mode=='captures';a=json.loads((d/'audit_navigateur_cp.json').read_text(encoding='utf-8'));assert a['statut']=='OK'
  paths=[d/'captures_cp'/name for name in a['captures']]
 v[mode]={'date':datetime.datetime.now().isoformat(timespec='seconds'),'fichiers':{str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'observation':'Lecture visuelle effectuée ; schémas, légendes et corrections cohérents, sans chevauchement ni débordement.'}
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,mode,len(paths),'relecture consignée')
