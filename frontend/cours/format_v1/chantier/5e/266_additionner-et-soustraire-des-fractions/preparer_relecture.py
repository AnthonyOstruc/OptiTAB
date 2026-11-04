"""Planches de relecture de toutes les vues mobiles requises, sans toucher aux captures."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
D=Path(__file__).resolve().parent.parent
font=ImageFont.truetype('arial.ttf',16)
for d in sorted(D.iterdir()):
    if not d.is_dir() or not (d/'captures').exists():continue
    captures=d/'captures'
    groups=[('documents',sorted(captures.glob('mobile-c*.png'))+sorted(captures.glob('mobile-f*.png')))]
    groups += [('enonces',[captures/f'mobile-ex{i:02d}-enonce.png' for i in (1,2,3)])]
    groups += [('etapes',[captures/f'mobile-ex{i:02d}-etapes.png' for i in (1,2,3)])]
    for label,files in groups:
        if any(not p.exists() for p in files) or not files:continue
        # À taille d'affichage pour les documents et énoncés. Les corrigés
        # sont découpés en bandes successives de 1400 px, à largeur inchangée.
        if label=='etapes':
            images=[Image.open(p).convert('RGB') for p in files]
            for part,top in enumerate(range(0,max(im.height for im in images),1400),1):
                board=Image.new('RGB',(3*390,1436),'#e2e6ee');draw=ImageDraw.Draw(board)
                for i,(p,im) in enumerate(zip(files,images)):
                    draw.text((i*390+8,6),p.name,fill='#1b3c8e',font=font)
                    if top<im.height:board.paste(im.crop((0,top,im.width,min(top+1400,im.height))),(i*390+8,30))
                board.save(captures/f'relecture_{label}_{part}.png')
        else:
            images=[Image.open(p).convert('RGB') for p in files]
            board=Image.new('RGB',(len(images)*406,max(im.height for im in images)+36),'#e2e6ee');draw=ImageDraw.Draw(board)
            for i,(p,im) in enumerate(zip(files,images)):
                draw.text((i*406+8,6),p.name,fill='#1b3c8e',font=font);board.paste(im,(i*406+8,30))
            board.save(captures/f'relecture_{label}.png')
    print(d.name,'planches disponibles')
