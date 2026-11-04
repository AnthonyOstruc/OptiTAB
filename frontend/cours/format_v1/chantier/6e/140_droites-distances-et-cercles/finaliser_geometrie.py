# -*- coding: utf-8 -*-
"""Corrections ciblées du lot existant ; ne régénère jamais les textes."""
from pathlib import Path
import runpy,re,json,math
BASE=Path(__file__).resolve().parent.parent

def node(x,y,t,anchor='south',color='otInk'):
    return rf'\node[anchor={anchor},text={color},inner sep=4pt] at ({x},{y}) {{$ {t} $}};'

def protractor(a):
    z=r'\begin{tikzpicture}\draw[geoTrait] (-3,0)--(3,0);\draw[geoTrait] (3,0) arc (0:180:3);'
    for t in range(0,181,10):
        z+=rf'\draw[geoTrait] ({t}:2.86)--({t}:3);'
        if t%30==0:
            # Graduations : seul cas où le fond blanc est légitime.
            z+=rf'\node[font=\small,fill=white,inner sep=2pt] at ({t}:3.34) {{{t}}};'
            z+=rf'\node[font=\small,text=otMuted,fill=white,inner sep=2pt] at ({t}:2.48) {{{180-t}}};'
    # Le rayon passe entre les deux bandes de nombres : pas sous les chiffres.
    z+=rf'\draw[geoReponse] (0,0)--({a}:2.13) ({a}:2.76)--({a}:3.09) ({a}:3.58)--({a}:3.85);'
    z+=node(0,-.1,'O','north')+node(3.8,0,'A','west')
    z+=node(4.02*math.cos(math.radians(a)),4.02*math.sin(math.radians(a)),'B','south')
    return z+r'\end{tikzpicture}'

def patch_figures():
    for n in range(140,146):
        d=next(BASE.glob(f'{n}_*'));p=d/'figures/figures.py';figs=runpy.run_path(str(p))['FIGURES']
        if n==141:
            for j,a in enumerate((30,60,120),1):figs[f'angle_2_{j}']=protractor(a)
        if n==145:
            for k,z in list(figs.items()):
                if k.startswith(('symetrie_1_','symetrie_2_','symetrie_3_')):
                    # Les noms restent hors de la grille, au-dessus/en dessous.
                    z=re.sub(r'\(-([0-9.]+),-1\) grid \(([0-9.]+),([0-9.]+)\)',
                             lambda m:f'(-{m[1]},0) grid ({m[2]},{float(m[3])-1:g})',z)
                if k.startswith('symetrie_4_'):
                    x,y=((1,3),(1,4),(2,4))[int(k[-1])-1];lim=max(x,y)+1
                    z=rf'\begin{{tikzpicture}}\draw[step=1,otRule,thin] (0,0) grid ({lim},{lim});\draw[otOrange,thick] (-.2,-.2)--({lim+.2},{lim+.2});'
                    z+=rf'\draw[geoReponse] ({x},{y})--({y},{x});\draw[geoAide] (-.15,{y})--({x},{y}) ({y},{x})--({lim+.15},{x});'
                    z+=rf'\fill[otNavy] ({x},{y}) circle (1.6pt);\fill[otGreenDark] ({y},{x}) circle (1.6pt);'
                    z+=node(-.25,y,'P','east')+node(lim+.25,x,"P'",'west','otGreenDark')+node(lim+.2,lim+.2,'(d)')+r'\end{tikzpicture}'
                if k.startswith('symetrie_5_'):
                    z=z.replace('at (2.5,-0.4)','at (0,-0.8)')
                figs[k]=z
        # Un seul PNG par figure identique ; toutes les correspondances suivent.
        canonical={};aliases={};unique={}
        for name,z in figs.items():
            if z in canonical:aliases[name]=canonical[z]
            else:canonical[z]=name;unique[name]=z
        cp=d/'figures/correspondance.json';corr=json.loads(cp.read_text(encoding='utf-8'))
        for genre in corr.values():
            for items in genre.values():
                for im in items.values():
                    old=Path(im['fichier']).stem
                    if old in aliases:im['fichier']=aliases[old]+'.png'
        cp.write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        p.write_text('# -*- coding: utf-8 -*-\n# Figures finales ; doublons mutualisés.\nFIGURES = '+repr(unique)+'\n',encoding='utf-8')
        print(n,len(unique),'figures uniques')

def enrichir_constructions():
    for n in (140,144):
        d=next(BASE.glob(f'{n}_*'));p=d/'figures/figures.py';figs=runpy.run_path(str(p))['FIGURES']
        for name,z in list(figs.items()):
            if name=='contraintes' or name.startswith('mediatrice_'):
                j=int(name[-1])-1 if name[-1].isdigit() else 0
                L,r=((6,5) if n==140 else ((6,5),(8,5),(10,7))[j]);h=math.sqrt(r*r-L*L/4)
                a=math.degrees(math.atan2(h,L/2));delta=10
                arcs=''
                # Deux arcs par centre, à chaque intersection : le tracé au
                # compas reste visible sans agrandir inutilement la figure.
                for cx,theta in ((-L/2,a),(L/2,180-a)):
                    for theta2 in (theta,-theta):
                        start=theta2-delta;end=theta2+delta
                        arcs+=rf'\draw[geoAide] ({cx+r*math.cos(math.radians(start))},{r*math.sin(math.radians(start))}) arc ({start}:{end}:{r});'
                arcs+=rf'\draw[geoReponse] ({-L/4},-.12)--({-L/4},.12) ({L/4},-.12)--({L/4},.12);'
                z=z.replace(r'\begin{scope}',r'\begin{scope}',1)
                # Insérer dans le même repère que les données.
                z=z.replace(r'\end{scope}',arcs+r'\end{scope}')
                figs[name]=z
        p.write_text('# -*- coding: utf-8 -*-\nFIGURES = '+repr(figs)+'\n',encoding='utf-8')
    d=next(BASE.glob('143_*'));p=d/'figures/figures.py';figs=runpy.run_path(str(p))['FIGURES']
    figs['quadrilatere_diagonales']=figs['quadrilatere_02'].replace(r'\end{tikzpicture}',r'\draw[geoAide] (0,0)--(5,3) (5,0)--(0,3);\end{tikzpicture}')
    p.write_text('# -*- coding: utf-8 -*-\nFIGURES = '+repr(figs)+'\n',encoding='utf-8')
    cp=d/'figures/correspondance.json';corr=json.loads(cp.read_text(encoding='utf-8'))
    corr['cours']['nouveau']['1']['fichier']='quadrilatere_diagonales.png'
    corr['exercices']['nouveau-9']['1']['fichier']='quadrilatere_diagonales.png'
    cp.write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def enrichir_textes():
    d=next(BASE.glob('141_*'));p=next(d.glob('cours_*.txt'));t=p.read_text(encoding='utf-8')
    t=t.replace('Deux angles supplémentaires ont une somme',r'Deux angles complémentaires ont une somme de $90^\circ$. Deux angles supplémentaires ont une somme')
    p.write_text(t,encoding='utf-8')
    d=next(BASE.glob('143_*'));p=d/'cours_nouveau.txt';t=p.read_text(encoding='utf-8')
    old='Tracer un premier côté. Choisir un troisième sommet à la bonne distance du second ; deux arcs de même rayon permettent de trouver le quatrième sommet. Vérifier les quatre longueurs ; ne pas imposer des angles droits qui ne sont pas donnés.'
    new='Pour une diagonale $AC=6$ cm et des côtés de 5 cm : tracer $[AC]$, puis deux cercles de centres $A$ et $C$, de rayon 5 cm. Leurs deux intersections sont $B$ et $D$, de part et d’autre de $(AC)$. Relier $A$, $B$, $C$, $D$ dans cet ordre. Les quatre côtés sont des rayons de construction ; ils mesurent donc tous 5 cm.'
    t=t.replace(old,new);p.write_text(t,encoding='utf-8')

def ajuster_cercles_symetrie():
    d=next(BASE.glob('145_*'));p=d/'figures/figures.py';figs=runpy.run_path(str(p))['FIGURES']
    for k in ('symetrie_6_2','symetrie_6_3'):
        z=figs[k];factor=.8 if k.endswith('2') else .6
        figs[k]=z.replace(r'\begin{tikzpicture}',rf'\begin{{tikzpicture}}\begin{{scope}}[x={factor}cm,y={factor}cm]').replace(r'\end{tikzpicture}',r'\end{scope}\end{tikzpicture}')
    p.write_text('# -*- coding: utf-8 -*-\nFIGURES = '+repr(figs)+'\n',encoding='utf-8')

def conserver_types():
    for n in (140,141,142,144,145):
        d=next(BASE.glob(f'{n}_*'));meta=json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
        types={str(e['id']):e['titre'].split(' - ')[0] for e in meta['exercices']}
        p=d/'exercices.txt';raw=p.read_text(encoding='utf-8')
        raw=re.sub(r'(?<!\n)===\s*\n','\n\n===\n',raw)
        blocks=re.split(r'^===[ \t]*$',raw,flags=re.M)
        for i,b in enumerate(blocks):
            m=re.search(r'^Id:\s*(\d+)',b,re.M)
            if not m:continue
            lines=b.splitlines();first=next(j for j,l in enumerate(lines) if l.strip())
            lines[first]=re.sub(r'^(?:===\s*)?(Découverte|Entraînement|Approfondissement|Problème)\s*[—-]\s*',types[m[1]]+' — ',lines[first])
            for j,line in enumerate(lines):
                if line.startswith('Difficulté:'):lines[j]='Difficulté: '+{'Découverte':'easy','Entraînement':'medium','Problème':'hard'}[types[m[1]]]
            blocks[i]='\n'.join(lines)
        out='=== '+'\n\n===\n\n'.join(b.strip().removeprefix('=== ').strip() for b in blocks if b.strip())+'\n'
        p.write_text(out,encoding='utf-8')

def deplacer_noms_compas():
    for n in (140,144):
        d=next(BASE.glob(f'{n}_*'));p=d/'figures/figures.py';figs=runpy.run_path(str(p))['FIGURES']
        for name,z in list(figs.items()):
            if name!='contraintes' and not name.startswith('mediatrice_'):continue
            j=int(name[-1])-1 if name[-1].isdigit() else 0
            L,r=(6,5) if n==140 else ((6,5),(8,5),(10,7))[j];h=math.sqrt(r*r-L*L/4)
            for label,y,anchor in [('P',h+.55,'south'),('Q',-h-.55,'north')]:
                z=re.sub(r'\\node\[[^\]]+\] at \([^)]*\) \{\$ '+label+r' \$\};',lambda m:node(0,y,label,anchor,'otGreenDark'),z)
            figs[name]=z
        p.write_text('# -*- coding: utf-8 -*-\nFIGURES = '+repr(figs)+'\n',encoding='utf-8')

if __name__=='__main__':patch_figures()
