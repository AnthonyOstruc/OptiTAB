# -*- coding: utf-8 -*-
"""Complément visuel ciblé : passage entre objet et représentations."""
from pathlib import Path
import json

P = Path(__file__).resolve().parent
def assemblage(piles, legend):
    lines=[r'\begin{tikzpicture}[x={(.85cm,0cm)},y={(.38cm,.28cm)},z={(0cm,.85cm)},line join=round,line cap=round]']
    for x,y,height in sorted(piles,key=lambda p:(-p[1],p[0])):
        for z in range(height):
            def c(a,b,h): return f'({a},{b},{h})'
            polygons=[('otNavy!7',[(x,y,z),(x+1,y,z),(x+1,y,z+1),(x,y,z+1)]),
                      ('otNavy!16',[(x+1,y,z),(x+1,y+1,z),(x+1,y+1,z+1),(x+1,y,z+1)]),
                      ('otNavy!3',[(x,y,z+1),(x+1,y,z+1),(x+1,y+1,z+1),(x,y+1,z+1)])]
            for color,pts in polygons:
                lines.append(r'\filldraw[fill='+color+r',draw=otNavy,line width=.65pt] '+'--'.join(c(*p) for p in pts)+'--cycle;')
    lines += [r'\node[anchor=north] at (1,-1,0) {'+legend+r'};',r'\end{tikzpicture}']
    return '\n'.join(lines)

src=P/'figures/figures.py'
text=src.read_text(encoding='utf8')
if "FIGURES['assemblage_7']" not in text:
    text += "\n\nFIGURES['assemblage_7'] = "+repr(assemblage([(0,1,1),(1,1,2),(0,0,3),(1,0,1)],'Avant'))+'\n'
    text += "FIGURES['piles_241'] = "+repr(assemblage([(0,0,2),(1,0,4),(2,0,1)],'Trois piles alignées, sans vide'))+'\n'
    src.write_text(text,encoding='utf8')
course=P/'cours_146.txt'
text=course.read_text(encoding='utf8')
needle='| Avant | 3 | 1 |\n'
if '[IMAGE_3]' not in text:
    text=text.replace(needle,needle+'\n[IMAGE_3]\n\nLa perspective représente ces quatre piles ; le plan garde aussi la hauteur des piles partiellement cachées.\n')
    course.write_text(text,encoding='utf8')
ex=P/'exercices.txt';text=ex.read_text(encoding='utf8')
needle='Trois piles sans vide sont alignées côte à côte. De face, on lit les hauteurs 2, 4 et 1. De dessus, les trois emplacements sont occupés et aucune autre pile n’existe.'
if needle+'\n\n[IMAGE_1]' not in text:
    text=text.replace(needle,needle+'\n\n[IMAGE_1]')
    ex.write_text(text,encoding='utf8')
p=P/'figures/correspondance.json';data=json.loads(p.read_text(encoding='utf8'))
data['cours']['146']['3']={'fichier':'assemblage_7.png','alt':'Perspective des quatre piles de hauteurs 1 et 2 à l’arrière, 3 et 1 à l’avant'}
data['exercices']['3562']={'1':{'fichier':'piles_241.png','alt':'Trois piles de cubes alignées, de hauteurs respectives 2, 4 et 1'}}
p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
