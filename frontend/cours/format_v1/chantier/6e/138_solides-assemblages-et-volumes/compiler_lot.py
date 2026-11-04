# -*- coding: utf-8 -*-
from pathlib import Path
import sys,json,shutil,importlib.util
P=Path(__file__).resolve().parent;R=P.parent;O=P.parents[2]/'outils'
sys.path.insert(0,str(O));import figures_livre as fl
cache={};allok=True
for n in (138,139,146,147,148,149,152):
 d=next(R.glob(f'{n}_*'));m=fl.charger(d);log=[]
 for name,body in m.FIGURES.items():
  key=(name,body);fig=d/'figures';build=fig/'build';out=fig/'images'
  if key in cache:
   src=cache[key];build.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
   shutil.copy2(src/'images'/f'{name}.png',out/f'{name}.png')
   for suffix in ('.tex','__sans_texte.png','__sans_texte.tex'):
    if (src/'build'/f'{name}{suffix}').exists():shutil.copy2(src/'build'/f'{name}{suffix}',build/f'{name}{suffix}')
   ok=True;msgs=['Figure identique déjà compilée et contrôlée, fichiers copiés.']
  else:
   existing=out/f'{name}.png';sans=build/f'{name}__sans_texte.png';tex=build/f'{name}.tex'
   expected=fl.PREAMBULE+'\n\\begin{document}\n'+body+'\n\\end{document}\n'
   if existing.exists() and sans.exists() and tex.exists() and tex.read_text(encoding='utf8')==expected:
    errs,warn=fl.chevauchements(existing,sans);ok=not errs;msgs=errs+warn
   else:ok,msgs=None,None
   if ok is not True:
    _,ok,msgs=fl.compiler_un(name,body,build,out,None,'',None)
   if ok:cache[key]=fig
  log.append({'figure':name,'ok':ok,'messages':msgs});allok &= ok
  (d/'compilation_figures.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf8')
  print(n,name,ok,' | '.join(msgs),flush=True)
 # Planche de comparaison sans suppression des planches précédentes.
 from PIL import Image,ImageDraw
 ims=[(x,Image.open(fig/'images'/f'{x}.png').convert('RGB')) for x in m.FIGURES if (fig/'images'/f'{x}.png').exists()]
 for k in range(0,len(ims),6):
  cells=[]
  for name,im in ims[k:k+6]:
   im=im.resize((im.width//2,im.height//2));cells.append((name,im))
  w=max(im.width for _,im in cells)+30;h=max(im.height for _,im in cells)+45
  sheet=Image.new('RGB',(w*2,h*3),'#e8edf4');dr=ImageDraw.Draw(sheet)
  for j,(name,im) in enumerate(cells):
   x=(j%2)*w+10;y=(j//2)*h+10;dr.text((x,y),name,fill='#12315a');sheet.paste(im,(x,y+25))
  sheet.save(fig/f'relecture_{k//6+1:02}.png')
sys.exit(0 if allok else 1)
