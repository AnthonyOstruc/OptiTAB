"""Planches de relecture des seuls fichiers référencés, sans suppression."""
from pathlib import Path
import importlib.util,math
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parent.parent
for n in range(271,276):
 d=next(BASE.glob(f'{n}_*'));fd=d/'figures';spec=importlib.util.spec_from_file_location('figs',fd/'figures.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 imgs=[]
 for name in m.FIGURES:
  p=fd/'images'/f'{name}.png'
  if p.is_file():
   im=Image.open(p).convert('RGB');im=im.resize((im.width//2,im.height//2));imgs.append((name,im))
 if not imgs:continue
 try:font=ImageFont.truetype('arial.ttf',14)
 except OSError:font=ImageFont.load_default()
 for k in range(0,len(imgs),9):
  batch=imgs[k:k+9];w=max(im.width for _,im in batch)+30;h=max(im.height for _,im in batch)+55;sheet=Image.new('RGB',(w*3,h*math.ceil(len(batch)/3)),(230,235,244));draw=ImageDraw.Draw(sheet)
  for j,(name,im) in enumerate(batch):x=(j%3)*w+10;y=(j//3)*h+10;draw.text((x,y),name,fill=(20,40,80),font=font);sheet.paste(im,(x,y+30))
  sheet.save(fd/f'planche_revision_30_{k//9+1:02d}.png')
 print(n,len(imgs),'PNG en planches',flush=True)
