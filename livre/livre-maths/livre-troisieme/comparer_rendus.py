"""Compare les rendus finaux aux 313 pages déjà relues, puis isole les changements."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
QA=ROOT/'build/qa'
baseline=json.loads((QA/'baseline-rendus.json').read_text(encoding='utf8'))
controle=json.loads((QA/'controle-pdf.json').read_text(encoding='utf8'))
identiques=[];modifiees=[]
for n in range(1,controle['pages']+1):
    nom=f'page-{n:03}.png'
    digest=hashlib.sha256((QA/nom).read_bytes()).hexdigest()
    (identiques if baseline['pages'].get(nom)==digest else modifiees).append(n)
for start in range(0,len(modifiees),12):
    planche=Image.new('RGB',(1200,1290),'white')
    for j,n in enumerate(modifiees[start:start+12]):
        im=Image.open(QA/f'page-{n:03}.png').convert('RGB');im.thumbnail((280,400))
        tile=Image.new('RGB',(300,430),'#e6e8eb');tile.paste(im,((300-im.width)//2,20))
        ImageDraw.Draw(tile).text((8,4),str(n),fill='black')
        planche.paste(tile,((j%4)*300,(j//4)*430))
    planche.save(QA/f'modifications-{start//12+1:02}.png')
report=dict(sha256=controle['sha256'],baseline_sha256=baseline['pdf_sha256'],pages_identiques=identiques,pages_modifiees=modifiees)
(QA/'comparaison-rendus.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(pages_identiques=len(identiques),pages_modifiees=modifiees),indent=2))
