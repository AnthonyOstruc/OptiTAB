from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;out=HERE/'relecture_figures';out.mkdir(exist_ok=True)
font=ImageFont.truetype('arial.ttf',16);items=[]
for d in sorted(ROOT.glob('[0-9][0-9]_*')):
 if sys.argv[1:] and int(d.name[:2]) not in set(map(int,sys.argv[1:])):continue
 corr=json.loads((d/'figures/correspondance.json').read_text(encoding='utf-8'));names=set()
 for mapping in corr.values():
  for positions in mapping.values():
   for spec in positions.values():names.add(spec['fichier'])
 for name in sorted(names):
  p=d/'figures/images'/name
  if not p.exists():continue
  im=Image.open(p).convert('RGB');im.thumbnail((480,650));items.append((d.name[:2]+' / '+name,im,str(p.relative_to(ROOT))))
manifest=[]
for start in range(0,len(items),4):
 group=items[start:start+4];heights=[max((im.height for _,im,_ in group[i:i+2]),default=0)+48 for i in (0,2)];canvas=Image.new('RGB',(1020,sum(heights)+20),'#eef1f6');draw=ImageDraw.Draw(canvas)
 for j,(label,im,src) in enumerate(group):
  x=15+(j%2)*505;y=10+(heights[0] if j>=2 else 0);draw.text((x,y),label,fill='#1b3c8e',font=font);canvas.paste(im,(x,y+28))
 p=out/f'figures_{start//4+1:02}.png';canvas.save(p);manifest.append({'planche':p.name,'figures':[x[2] for x in group]})
(out/'index.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');print(len(items),'figures',len(manifest),'planches')
