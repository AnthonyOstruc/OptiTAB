from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,sys,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;out=HERE/'relecture_mobile';out.mkdir(exist_ok=True)
font=ImageFont.truetype('arial.ttf',15)
def stack(paths):
 ims=[Image.open(p).convert('RGB') for p in paths];pic=Image.new('RGB',(390,sum(i.height for i in ims)),'white');y=0
 for im in ims:pic.paste(im,(0,y));y+=im.height
 pic=pic.resize((240,round(pic.height*240/390)));return pic
for code in map(int,sys.argv[1:]):
 d=next(ROOT.glob(f'{code:02}_*'));a=json.loads((d/'audit_navigateur_ce1.json').read_text(encoding='utf-8'));shots=d/'captures_ce1';names=a['captures'];groups=[]
 for key,label in [('cnouveau','Cours complet'),('fnouvelle','Synthèse')]:groups.append((label,stack([shots/n for n in names if n.startswith('mobile-'+key+'-')])))
 for i in [1,5,9]:groups.append((f'Ex{i} énoncé + étapes',stack([shots/f'mobile-ex{i}-{k}.png' for k in ['enonce','etapes']])))
 canvas=Image.new('RGB',(1260,max(im.height for _,im in groups)+48),'#e4e9f2');draw=ImageDraw.Draw(canvas)
 for i,(label,im) in enumerate(groups):x=10+i*250;draw.text((x,5),str(code)+' / '+label,fill='#1b3c8e',font=font);canvas.paste(im,(x,32))
 canvas.save(out/f'{code:02}.png')
 print(code,'vue complète',flush=True)
