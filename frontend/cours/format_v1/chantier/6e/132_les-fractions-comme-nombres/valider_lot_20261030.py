"""Syntaxe et navigateurs séquentiels, une seule tâche lourde active."""
from pathlib import Path
import subprocess,sys,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
for n in (tuple(map(int,sys.argv[1:])) if len(sys.argv)>1 else (132,134,135,136,137,284,285)):
    d=next(BASE.glob(str(n)+'_*'))
    for name,cmd in [
      ('validation_revision.log',[sys.executable,str(HERE/'verifier_local.py'),str(d),'--navigateur']),
      ('captures_revision.log',['node',str(HERE/'capturer_mobile_20261030.mjs'),str(d)])]:
        with (d/name).open('w',encoding='utf-8') as log:
            result=subprocess.run(cmd,stdout=log,stderr=log,stdin=subprocess.DEVNULL)
        print(n,name,result.returncode,flush=True)
        if result.returncode:print((d/name).read_text(encoding='utf-8')[-3500:],flush=True)
    out=d/'captures_mobile_2026-10-30';from PIL import Image,ImageDraw
    # Planches à largeur réelle : chaque fragment garde ses 390 pixels, aucune réduction du texte.
    groups=[('cours',list(out.glob('mobile-c*-entier.png'))),('fiche_enonces',list(out.glob('mobile-f*-entier.png'))+list(out.glob('*-enonce.png'))),('etapes',list(out.glob('*-etapes.png')))]
    for name,files in groups:
        pieces=[]
        for f in files:
            im=Image.open(f).convert('RGB')
            for y in range(0,im.height,1500):pieces.append((f.name,y,im.crop((0,y,im.width,min(y+1500,im.height)))))
        for k in range(0,len(pieces),3):
            batch=pieces[k:k+3];canvas=Image.new('RGB',(3*410,1540),'#e5eaf3');draw=ImageDraw.Draw(canvas)
            for col,(filename,y,im) in enumerate(batch):
                draw.text((col*410+5,5),filename[:38]+f' y={y}',fill='#1b3c8e');canvas.paste(im,(col*410,35))
            canvas.save(out/f'planche-{name}-{k//3+1}.png')
    print(n,'planches de relecture enregistrées',flush=True)
