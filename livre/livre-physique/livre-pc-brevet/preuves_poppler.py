"""Seconde lecture du PDF final avec un moteur de rendu indépendant."""
from pathlib import Path
import subprocess,json,re
from concurrent.futures import ThreadPoolExecutor
HERE=Path(__file__).resolve().parent;QA=HERE.parent/'tmp/pdfs/qa-pc-brevet'
import fitz
doc=fitz.open(HERE/'build/main.pdf');aux=(HERE/'build/main.aux').read_text(encoding='utf8')
def physical(label):
    m=re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^{}]*\}\{(\d+)\}',aux)
    assert m,label
    # One cover page precedes page 1 of the Arabic sequence.
    return int(m[1])+1
PAGES=sorted({1,2,3,*[physical(s) for s in ['corchap-1','corchap-2','corchap-9','corchap-13','corchap-14','bb-2','bb-3','bb-7','cor-bb-1','cor-bb-2','cor-bb-3','cor-bb-4','cor-bb-5','cor-bb-6','cor-bb-7','cor-bb-8','cor-bb-9','cor-bb-10']],*[i+1 for i,p in enumerate(doc) if any(s in p.get_text().replace('\n',' ') for s in ['Deux flèches de 3,92 cm','3 cm et 2,5 cm'])]})
def render(n):
    prefix=QA/f'preuve-{n:03}'
    subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-scale-to','1600','-png','-singlefile',str(HERE/'build/main.pdf'),str(prefix)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return str(prefix.with_suffix('.png'))
if __name__=='__main__':
    QA.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:paths=list(pool.map(render,PAGES))
    (HERE/'build/preuves-poppler.json').write_text(json.dumps(dict(pages=PAGES,fichiers=paths),ensure_ascii=False,indent=2),encoding='utf8')
    print(len(PAGES),'pages critiques rendues avec Poppler.')
