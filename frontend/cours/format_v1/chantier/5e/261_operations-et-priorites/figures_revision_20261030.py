"""Deux énoncés de lecture/placement et leurs réponses graphiques exactes."""
from pathlib import Path
import json
import runpy
BASE=Path(__file__).resolve().parent.parent

def numberline(quarter=True,corrected=False):
    if quarter:
        lines=[r'\begin{tikzpicture}[x=.78cm,y=1cm]',r'\draw[geoVecteur] (-.3,0)--(8.7,0);']
        for k in range(9): lines.append(rf'\draw[otMuted] ({k},-.06)--({k},.06);')
        for k,label in [(4,'0'),(8,'1')]: lines.append(rf'\node[below=8pt,text=otMuted] at ({k},0) {{${label}$}};')
        for name,k in [('A',1),('B',6),('C',3)]:
            lines += [rf'\fill[otNavy] ({k},0) circle (1.8pt);',rf'\node[above=8pt,text=otNavy] at ({k},0) {{${name}$}};']
        if corrected:
            for k,label in [(1,r'-0{,}75'),(3,r'-0{,}25'),(6,r'0{,}5')]: lines.append(rf'\node[below=8pt,text=otGreenDark] at ({k},0) {{${label}$}};')
            lines += [r'\fill[otGreenDark] (7,0) circle (1.8pt);',r'\node[above=8pt,text=otGreenDark] at (7,0) {$D$};',r'\node[below=8pt,text=otGreenDark] at (7,-.65) {$0{,}75$};']
    else:
        lines=[r'\begin{tikzpicture}[x=.53cm,y=1cm]',r'\draw[geoVecteur] (-.3,0)--(12.7,0);']
        for k in range(13): lines.append(rf'\draw[otMuted] ({k},-.06)--({k},.06);')
        for k,label in [(0,'0'),(4,'1'),(8,'2'),(12,'3')]: lines.append(rf'\node[below=8pt,text=otMuted] at ({k},0) {{${label}$}};')
        if corrected:
            for name,k,frac in [('B',7,r'\frac74'),('A',11,r'\frac{11}4')]:
                lines += [rf'\fill[otGreenDark] ({k},0) circle (1.8pt);',rf'\node[above=8pt,text=otGreenDark] at ({k},0) {{${name}$}};',rf'\node[above=8pt,text=otGreenDark] at ({k},.7) {{${frac}$}};']
    return '\n'.join(lines+[r'\end{tikzpicture}'])

for code,eid,kind in [(263,2752,True),(265,2801,False)]:
    p=next(BASE.glob(f'{code}_*')); fp=p/'figures/figures.py'
    figures=runpy.run_path(str(fp))['FIGURES']
    for corrected in (False,True): figures[f'revision_{eid}_'+('corrige' if corrected else 'enonce')]=numberline(kind,corrected)
    corrpath=p/'figures/correspondance.json'; corr=json.loads(corrpath.read_text(encoding='utf8'))
    corr['exercices'][str(eid)]={str(pos):{'fichier':f'revision_{eid}_{phase}.png','alt': ('Droite au quart : points A, B et C à lire ; origine 0 et abscisse 1.' if kind else 'Droite de 0 à 3, chaque unité est partagée en quatre.') if phase=='enonce' else ('Correction : A(-0,75), B(0,5), C(-0,25) et point opposé D(0,75).' if kind else 'Correction : B est placé à sept quarts et A à onze quarts.')} for pos,phase in [(1,'enonce'),(2,'corrige')]}
    # Seules les sources encore appelées restent dans le dictionnaire de compilation.
    used={v['fichier'].removesuffix('.png') for group in corr.values() for positions in group.values() for v in positions.values()}
    figures={name:tex for name,tex in figures.items() if name in used}
    fp.write_text('# -*- coding: utf-8 -*-\n"""Figures TikZ actives, avec réponses graphiques distinctes."""\nFIGURES = '+repr(figures)+'\n',encoding='utf8')
    corrpath.write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(code,'deux nouvelles figures,',len(figures),'figures actives',flush=True)
