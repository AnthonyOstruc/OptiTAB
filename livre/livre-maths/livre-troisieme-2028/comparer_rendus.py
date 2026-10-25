"""Compare les rendus de pages à ceux d’une relecture précédente.

python comparer_rendus.py --enregistrer : mémorise les empreintes des pages relues.
python comparer_rendus.py : liste les pages modifiées depuis et prépare leurs planches.
"""
from pathlib import Path
import json,hashlib,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
QA=ROOT/'build/qa'
controle=json.loads((QA/'controle-pdf.json').read_text(encoding='utf8'))
empreintes={f'page-{n:03}.png':hashlib.sha256((QA/f'page-{n:03}.png').read_bytes()).hexdigest() for n in range(1,controle['pages']+1)}
if '--enregistrer' in sys.argv:
    (QA/'baseline-rendus.json').write_text(json.dumps(dict(pdf_sha256=controle['sha256'],pages=empreintes),indent=2),encoding='utf8')
    print('Empreintes enregistrées :',len(empreintes));sys.exit()
baseline=json.loads((QA/'baseline-rendus.json').read_text(encoding='utf8'))
identiques=[];modifiees=[]
for n in range(1,controle['pages']+1):
    nom=f'page-{n:03}.png'
    (identiques if baseline['pages'].get(nom)==empreintes[nom] else modifiees).append(n)
for old in QA.glob('modifications-*.png'):old.unlink()
for start in range(0,len(modifiees),6):
    planche=Image.new('RGB',(1260,1200),'white')
    for j,n in enumerate(modifiees[start:start+6]):
        im=Image.open(QA/f'page-{n:03}.png').convert('RGB');im.thumbnail((400,566))
        tile=Image.new('RGB',(420,600),'#e6e8eb');tile.paste(im,((420-im.width)//2,26))
        ImageDraw.Draw(tile).text((8,6),str(n),fill='black')
        planche.paste(tile,((j%3)*420,(j//3)*600))
    planche.save(QA/f'modifications-{start//6+1:02}.png')
report=dict(sha256=controle['sha256'],baseline_sha256=baseline['pdf_sha256'],pages_identiques=identiques,pages_modifiees=modifiees)
(QA/'comparaison-rendus.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(pages_identiques=len(identiques),pages_modifiees=modifiees),indent=2))
