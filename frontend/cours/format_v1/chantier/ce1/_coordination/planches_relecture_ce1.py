"""Compose les captures réellement listées par l'audit, sans réduire leur largeur."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,sys,re
ROOT=Path(__file__).resolve().parent.parent
font=ImageFont.truetype('arial.ttf',15)
def assemble(items,out):
 canvas=Image.new('RGB',(sum(im.width for _,im in items)+16*(len(items)+1),max(im.height for _,im in items)+50),'#e4e9f2')
 draw=ImageDraw.Draw(canvas);x=16
 for title,im in items:draw.text((x,8),title,fill='#1b3c8e',font=font);canvas.paste(im,(x,34));x+=im.width+16
 canvas.save(out)
for code in map(int,sys.argv[1:]):
 d=next(ROOT.glob(f'{code:02}_*'));a=json.loads((d/'audit_navigateur_ce1.json').read_text(encoding='utf-8'));shots=d/'captures_ce1'
 docs=[p for p in a['captures'] if '-ex' not in p];items=[]
 for p in docs:items.append((p,Image.open(shots/p).convert('RGB')))
 for start in range(0,len(items),4):assemble(items[start:start+4],d/f'relecture_documents_{start//4+1:02}.png')
 exitems=[]
 for k in sorted({int(re.search(r'mobile-ex(\d+)-',p)[1]) for p in a['captures'] if '-ex' in p}):
  parts=[Image.open(shots/f'mobile-ex{k}-{name}.png').convert('RGB') for name in ('enonce','etapes')]
  pair=Image.new('RGB',(max(p.width for p in parts),sum(p.height for p in parts)+12),'white');y=0
  for p in parts:pair.paste(p,(0,y));y+=p.height+12
  for start in range(0,pair.height,2200):exitems.append((f'ex{k} partie {start//2200+1}',pair.crop((0,start,pair.width,min(start+2200,pair.height)))))
 for start in range(0,len(exitems),4):assemble(exitems[start:start+4],d/f'relecture_exercices_{start//4+1:02}.png')
 print(code,'documents',len(items),'fragments exercices',len(exitems))
