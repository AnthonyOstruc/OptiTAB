"""Planche des figures pour la relecture humaine, sans changer les images sources."""
from pathlib import Path
import json
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
FRONT=ROOT.parents[2]


def planche(files,name,cols=4):
    tiles=[]
    for p in files:
        if not p.exists():continue
        with Image.open(p) as src:im=src.convert('RGB')
        im.thumbnail((380,215))
        tile=Image.new('RGB',(400,245),'#edf2f7');tile.paste(im,((400-im.width)//2,8))
        ImageDraw.Draw(tile).text((8,226),p.stem,fill='black')
        tiles.append(tile)
    if not tiles:return
    sheet=Image.new('RGB',(400*cols,245*((len(tiles)+cols-1)//cols)),'white')
    for j,tile in enumerate(tiles):sheet.paste(tile,((j%cols)*400,(j//cols)*245))
    sheet.save(ROOT/'verifications'/name)
    print(name,len(tiles),'figures')


if __name__=='__main__':
    data=json.loads((ROOT/'verifications/manifeste.json').read_text(encoding='utf-8'))
    files=[]
    for e in data:
        if e['niveau']==2 and e['indice']==6:
            files.append(FRONT/'exercices/6e/images'/e['images'][-1])
    planche(files,'planches-exercices.png')
    planche(sorted((ROOT/'images').glob('*.png')),'planches-cours.png')
