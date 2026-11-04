"""Recompose seulement certains types de figures déjà décrits dans le manifeste."""
import json
import sys
from modele_6e import ROOT,FRONT
from figures_6e import draw

types=set(sys.argv[1:])
specs=json.loads((ROOT/'verifications/figures.json').read_text(encoding='utf-8'))
manifest=json.loads((ROOT/'verifications/manifeste.json').read_text(encoding='utf-8'))
count=0
for e in manifest:
    spec=specs[e['code']]
    if types and spec['type'] not in types:continue
    for name in e['images']:
        draw(spec,FRONT/'exercices/6e/images'/name,'_corrige' in name)
        count+=1
print(count,'figures recomposées.')
