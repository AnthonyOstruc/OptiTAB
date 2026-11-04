"""Mettre en cache et relire les anciennes images du lot, sans les conserver en production."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parent.parent;OUTILS=ROOT.parents[1]/'outils'
sys.path.insert(0,str(OUTILS));import planche
for code in (129,130,131,133,151):
 d=next(ROOT.glob(str(code)+'_*'));items=list(planche.images(d))
 def fetch(item):
  genre,oid,im=item
  return (f'{genre} {oid} position {im["position"]}',planche.telecharger(d,im))
 with ThreadPoolExecutor(max_workers=4) as pool:files=list(pool.map(fetch,items))
 output=d/'planches';output.mkdir(exist_ok=True)
 for k in range(0,len(files),12):planche.composer(files[k:k+12],output/f'planche_{k//12+1:02}.png')
 print(code,len(files),'anciennes images disponibles',flush=True)
