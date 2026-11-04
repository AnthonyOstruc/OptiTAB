"""Planches lisibles : cours et fiche, puis quatre nouveaux exercices complets."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys,json
BASE=Path(__file__).resolve().parent.parent
font=ImageFont.truetype('arial.ttf',17)
for code in map(int,sys.argv[1:] or range(266,271)):
    d=next(BASE.glob(f'{code}_*'));c=d/'captures_revision_20261030'
    selection=json.loads((d/'selection_captures_revision.json').read_text(encoding='utf-8')) if (d/'selection_captures_revision.json').exists() else [3,8,15,21]
    if not all((c/f'mobile-ex{i:02d}-etapes.png').exists() for i in selection):continue
    groups=[('Cours',sorted(c.glob('mobile-c*.png'))),('Fiche',sorted(c.glob('mobile-f*.png')))]
    documents=[p for _,files in groups for p in files]
    ims=[Image.open(p).convert('RGB') for p in documents]
    board=Image.new('RGB',(406*len(ims),max(im.height for im in ims)+36),'#e2e6ee')
    draw=ImageDraw.Draw(board)
    for k,(im,p) in enumerate(zip(ims,documents)):
        draw.text((k*406+8,6),p.name,fill='#1b3c8e',font=font);board.paste(im,(k*406+8,32))
    board.save(c/'relecture_documents.png')
    groups.extend((f'Exercice {i}',[c/f'mobile-ex{i:02d}-enonce.png',c/f'mobile-ex{i:02d}-etapes.png']) for i in selection)
    cols=[]
    for label,files in groups:
        ims=[Image.open(p).convert('RGB') for p in files]
        height=sum(im.height+12 for im in ims)+36
        col=Image.new('RGB',(406,height),'#e2e6ee');draw=ImageDraw.Draw(col);draw.text((8,6),label,fill='#1b3c8e',font=font)
        top=32
        for im in ims:col.paste(im,(8,top));top+=im.height+12
        cols.append(col)
    # Deux planches seulement pour éviter de réduire les textes à la lecture.
    for j,subset in enumerate((cols[:3],cols[3:]),1):
        board=Image.new('RGB',(406*len(subset),max(im.height for im in subset)),'#e2e6ee')
        for k,im in enumerate(subset):board.paste(im,(406*k,0))
        board.save(c/f'relecture_revision_{j}.png')
    print(code,'planches créées',flush=True)
