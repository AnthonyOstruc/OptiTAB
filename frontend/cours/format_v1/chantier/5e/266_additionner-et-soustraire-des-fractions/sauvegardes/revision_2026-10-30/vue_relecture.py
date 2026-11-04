"""Vue d'ensemble du cours entier, de la fiche et de trois exercices sur téléphone."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
B=Path(__file__).resolve().parent.parent
font=ImageFont.truetype('arial.ttf',16)
for d in sorted(B.iterdir()):
    if not d.is_dir() or not (d/'captures').exists():continue
    c=d/'captures'
    groups=[('Cours intégral',sorted(c.glob('mobile-c*.png'))),('Fiche',sorted(c.glob('mobile-f*.png')))]
    groups += [(f'Exercice {i} : énoncé + étapes',[c/f'mobile-ex{i:02d}-enonce.png',c/f'mobile-ex{i:02d}-etapes.png']) for i in (1,2,3)]
    if any(not files or any(not p.exists() for p in files) for _,files in groups):continue
    cols=[]
    for label,files in groups:
        images=[]
        for p in files:
            im=Image.open(p).convert('RGB');im=im.resize((240,round(im.height*240/im.width)),Image.Resampling.LANCZOS);images.append(im)
        col=Image.new('RGB',(256,sum(im.height+12 for im in images)+40),'#e2e6ee');draw=ImageDraw.Draw(col)
        draw.text((8,6),label,fill='#1b3c8e',font=font)
        y=36
        for im in images:col.paste(im,(8,y));y+=im.height+12
        cols.append(col)
    out=Image.new('RGB',(1280,max(im.height for im in cols)),'#e2e6ee')
    for i,im in enumerate(cols):out.paste(im,(256*i,0))
    out.save(c/'relecture_ensemble.png')
    print(d.name)
