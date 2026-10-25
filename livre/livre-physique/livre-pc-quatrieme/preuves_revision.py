"""Contrôle des longueurs imprimées et seconde lecture du PDF avec Poppler."""
from pathlib import Path
import json,math,subprocess,hashlib
import fitz
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
pdf=HERE/'build/main.pdf';doc=fitz.open(pdf)
qa=ROOT/'tmp/pdfs/qa-pc-quatrieme-revision';qa.mkdir(parents=True,exist_ok=True)
cases=[('Flèche de 4 cm',[4]),('Longueurs à mesurer',[3,.5,4]),('Chaque flèche mesure 2 cm',[2,2]),('Flèche de 2,5 cm',[2.5]),('Segment de 6 cm',[6])]
results=[]
for marker,expected in cases:
    pages=[i for i,p in enumerate(doc) if marker in p.get_text()]
    assert len(pages)==1,(marker,pages)
    p=doc[pages[0]];lengths=[]
    for drawing in p.get_drawings():
        for item in drawing['items']:
            if item[0]=='l':
                a,b=item[1:3]
                if abs(a.x-b.x)<.05 or abs(a.y-b.y)<.05:lengths.append(math.hypot(a.x-b.x,a.y-b.y)*2.54/72)
    found=[];pool=lengths[:]
    for cm in expected:
        nearest=min(pool,key=lambda x:abs(x-cm));pool.remove(nearest)
        assert abs(nearest-cm)<.01,(marker,cm,nearest)
        found.append(round(nearest,4))
    results.append(dict(page=pages[0]+1,repere=marker,longueurs_attendues_cm=expected,longueurs_mesurees_cm=found,valide=True))
proofs=[12,87,137,177,198,209,212,217,224,230,239,242,252,268,269,270,272,273,274,275,289]
for n in proofs:
    subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-scale-to','1600','-png','-singlefile',str(pdf),str(qa/f'preuve-{n:03}')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
report=dict(sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),echelles=results,preuves_poppler=proofs)
(HERE/'build/preuves-revision.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=True,indent=2))
