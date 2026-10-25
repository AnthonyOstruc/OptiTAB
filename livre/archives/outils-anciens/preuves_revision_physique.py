"""Rend les pages critiques des versions finales avec Poppler."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess, sys, json, hashlib

pdf=Path(sys.argv[1]).resolve()
dest=Path(sys.argv[2]).resolve()
pages=sorted(set(map(int,sys.argv[3].split(','))))
dest.mkdir(parents=True,exist_ok=True)

def render(n):
    prefix=dest/f'p{n:03}'
    subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-scale-to','1800','-png','-singlefile',str(pdf),str(prefix)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return str(prefix.with_suffix('.png'))

with ThreadPoolExecutor(max_workers=4) as pool:
    files=list(pool.map(render,pages))
report=dict(pdf=str(pdf),sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),pages=pages,fichiers=files,moteur='Poppler pdftoppm')
(dest/'preuves.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(pages=len(pages),sha256=report['sha256'])))
