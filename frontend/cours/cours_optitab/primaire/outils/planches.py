"""Planches de relecture des figures et des vues de téléphone."""
import json
import re
from PIL import Image,ImageOps,ImageDraw,ImageFont
from config import ROOT,FRONT,GRADE,chapters
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)

def sheet(items,name):
    cols=3;tw=490;th=280
    for part in range(0,len(items),12):
        chunk=items[part:part+12];page=Image.new('RGB',(cols*tw,((len(chunk)+cols-1)//cols)*th),'#e5edf5');d=ImageDraw.Draw(page)
        for j,(title,path) in enumerate(chunk):
            im=Image.open(path).convert('RGB');im.thumbnail((tw-24,th-55));x=(j%cols)*tw;y=(j//cols)*th
            page.paste(im,(x+(tw-im.width)//2,y+35+(th-55-im.height)//2))
            d.text((x+10,y+9),title[:59],font=font,fill='#183d61')
        page.save(ROOT/f'verifications/{name}-{part//12+1}.jpg',quality=90)

cs=chapters();manifest=json.loads((ROOT/'verifications/manifeste.json').read_text(encoding='utf-8'))
courses=[];corrections=[];supplements=[]
for c in cs:
    raw=(ROOT/f'cours_{c.slug}_{GRADE}.txt').read_text(encoding='utf-8');names=re.search(r'^Images: (.+)$',raw,re.M)[1].split(', ')
    for name in names:courses.append((f'{c.numero:02} {c.titre}',ROOT/'images'/name))
    selected=[e for e in manifest if e['slug']==c.slug and e['niveau']==2][-1]
    corrections.append((f'{c.numero:02} {c.titre}',FRONT/f'exercices/{GRADE}/images'/selected['images'][1]))
    if len(selected['images'])>2:supplements.append((f'{c.numero:02} Question complémentaire',FRONT/f'exercices/{GRADE}/images'/selected['images'][2]))
sheet(courses,'planches-cours');sheet(corrections,'planches-corrections');sheet(supplements,'planches-complements')
print(f'{len(courses)} figures de cours, {len(corrections)} corrections et {len(supplements)} compléments mis en planches.')
