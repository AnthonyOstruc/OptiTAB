"""Planches des captures intégrales, pour inspecter les documents et trois corrigés."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
ROOT=Path(__file__).resolve().parent.parent
font=ImageFont.truetype('arial.ttf',16)
def planche(paths,out):
 ims=[Image.open(p).convert('RGB') for p in paths];widths=[im.width for im in ims]
 result=Image.new('RGB',(sum(widths)+16*(len(ims)+1),max(im.height for im in ims)+48),'#e4e9f2');dr=ImageDraw.Draw(result);x=16
 for p,im in zip(paths,ims):
  dr.text((x,8),p.name,fill='#1b3c8e',font=font);result.paste(im,(x,34));x+=im.width+16
 result.save(out)
for code in (129,130,131,133,150,151):
 d=next(ROOT.glob(str(code)+'_*'));shots=d/'captures_relecture_6e'
 docs=sorted(shots.glob('c*.png'))+sorted(shots.glob('f*.png'))
 assert docs
 planche(docs,d/'relecture_documents_6e.png')
 pairs=[]
 for k in (1,10,21):
  files=[shots/f'ex{k}-enonce.png',shots/f'ex{k}-etapes.png'];ims=[Image.open(p).convert('RGB') for p in files]
  both=Image.new('RGB',(max(im.width for im in ims),sum(im.height for im in ims)+24),'white');y=0
  for im in ims:both.paste(im,(0,y));y+=im.height+24
  p=shots/f'ex{k}-complet.png';both.save(p);pairs.append(p)
 planche(pairs,d/'relecture_exercices_6e.png')
 print(code,len(docs),'parties de documents et trois exercices complets')
