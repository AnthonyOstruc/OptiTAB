"""Planche de chaque source image, séquentiellement ; aucun contenu source modifié."""
from pathlib import Path
import subprocess,sys
base=Path(__file__).resolve().parent.parent
tool=base.parent.parent/'outils'/'planche.py'
with (Path(__file__).parent/'planches_sources.log').open('w',encoding='utf-8') as log:
    for n in (132,134,135,136,137,284,285):
        d=next(base.glob(str(n)+'_*'))
        log.write(f'NOTION {n}\n');log.flush()
        p=subprocess.run([sys.executable,str(tool),str(d),'--par','24'],stdout=log,stderr=log,stdin=subprocess.DEVNULL)
        print(n,p.returncode,flush=True)
