from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys,json
ROOT=Path(__file__).resolve().parent.parent
font=ImageFont.truetype('arial.ttf',20)
for code in map(int,sys.argv[1:]):
 assert code in [21,22,23,24]
 d=next(ROOT.glob(f'{code:02}_*'));files=sorted((d/'figures/images').glob('*.png'));out=d/'planches';out.mkdir(exist_ok=True);manifest=[]
 for start in range(0,len(files),4):
  group=files[start:start+4];imgs=[Image.open(p).convert('RGB') for p in group]
  col=max(im.width for im in imgs)+25;row=max(im.height for im in imgs)+55
  canvas=Image.new('RGB',(col*2+20,row*2+20),'#eef1f6');draw=ImageDraw.Draw(canvas)
  for k,(p,im) in enumerate(zip(group,imgs)):
   x=10+k%2*col;y=10+k//2*row;draw.text((x,y),f'{code:02} / {p.name}',font=font,fill='#1b3c8e');canvas.paste(im,(x,y+35))
  name=f'figures_vue_{start//4+1:02}.png';canvas.save(out/name);manifest.append({'planche':name,'figures':[p.name for p in group]})
 (out/'index_figures_vues.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
 print(code,len(files),'figures',len(manifest),'planches')
