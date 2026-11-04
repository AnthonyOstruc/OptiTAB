# -*- coding: utf-8 -*-
"""Génère les modules TikZ et les correspondances locales des notions 276–280."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parent.parent
def parallelo(diagonales=False,hauteur=False,couper=False):
    s=r'''\begin{tikzpicture}[line cap=round]
\coordinate (A) at (0,0); \coordinate (B) at (4.6,0);
\coordinate (D) at (1.1,2); \coordinate (C) at (5.7,2);
\fill[otNavy!5] (A)--(B)--(C)--(D)--cycle;
\draw[geoTrait] (A)--(B)--(C)--(D)--cycle;
\node[anchor=north east] at (-.08,-.08) {$A$};
\node[anchor=north west] at (4.68,-.08) {$B$};
\node[anchor=south west] at (5.78,2.08) {$C$};
\node[anchor=south east] at (1.02,2.08) {$D$};
'''
    if diagonales:
        s+=r'''\draw[otGreenDark,dashed,line width=.8pt] (A)--(C) (B)--(D);
\fill[otGreenDark] (2.85,1) circle (1.6pt);
\node[text=otGreenDark,anchor=south west] at (2.95,1.17) {$O$};
'''
    if hauteur:
        s+=r'''\draw[otOrange,dashed,line width=.9pt] (1.1,0)--(D);
\draw[otOrange] (1.1,.2)--(1.3,.2)--(1.3,0);
\node[anchor=west,text=otInk] at (1.32,.85) {$h$};
\node[anchor=north] at (2.6,-.23) {base $b=AB$};
'''
    if couper:
        s+=r'''\fill[otGreen!14] (A)--(C)--(D)--cycle;
\draw[otGreenDark,line width=1pt] (A)--(C);
\node[text=otGreenDark] at (2.1,1.4) {$\frac{\mathcal A}{2}$};
\node[text=otGreenDark] at (3.65,.55) {$\frac{\mathcal A}{2}$};
'''
    return s+r'\end{tikzpicture}'

PAVE=r'''\begin{tikzpicture}[line cap=round]
\fill[otNavy!5] (0,0)--(4,0)--(4,2.2)--(0,2.2)--cycle;
\draw[otMuted,dashed] (0,0)--(.9,.8)--(4.9,.8) (.9,.8)--(.9,3);
\draw[geoTrait] (0,0)--(4,0)--(4,2.2)--(0,2.2)--cycle;
\draw[geoTrait] (0,2.2)--(.9,3)--(4.9,3)--(4,2.2);
\draw[geoTrait] (4.9,3)--(4.9,.8)--(4,0);
\node[anchor=north] at (2,-.25) {$L$};
\node[anchor=north west] at (4.6,.1) {$\ell$};
\node[anchor=west] at (5.1,1.8) {$h$};
\end{tikzpicture}'''

PRISME=r'''\begin{tikzpicture}[line cap=round]
\fill[otNavy!8] (0,0)--(4,0)--(0,2)--cycle;
\draw[otMuted,dashed] (0,0)--(1.3,.9)--(5.3,.9) (1.3,.9)--(1.3,2.9);
\draw[geoTrait] (0,0)--(4,0)--(0,2)--cycle;
\draw[geoTrait] (0,2)--(1.3,2.9)--(5.3,.9)--(4,0);
\draw[otOrange] (0,.2)--(.2,.2)--(.2,0);
\node[anchor=north] at (2,-.2) {$a$};
\node[anchor=east] at (-.2,1) {$b$};
\node[anchor=north west] at (4.85,.25) {$L$};
\end{tikzpicture}'''

CYLINDRE=r'''\begin{tikzpicture}[line cap=round]
\fill[otNavy!5] (-1.3,0) rectangle (1.3,3);
\fill[white] (0,3) ellipse (1.3 and .4);
\draw[geoTrait] (0,3) ellipse (1.3 and .4);
\draw[geoTrait] (-1.3,3)--(-1.3,0) (1.3,3)--(1.3,0);
\draw[otMuted,dashed] (-1.3,0) arc[start angle=180,end angle=0,x radius=1.3,y radius=.4];
\draw[geoTrait] (-1.3,0) arc[start angle=180,end angle=360,x radius=1.3,y radius=.4];
\draw[otOrange,line width=.9pt] (0,3)--(1.3,3);
\fill[otNavy] (0,3) circle (1.2pt);
\node[anchor=south] at (.63,3.48) {$r$};
\draw[cote] (1.85,0)--(1.85,3) node[coteTexte,midway] {$h$};
\end{tikzpicture}'''

PATRON=r'''\begin{tikzpicture}
\fill[otNavy!5] (0,0) rectangle (4.2,1.7);
\draw[geoTrait] (0,0) rectangle (4.2,1.7);
\draw[geoTrait] (2.1,2.37) circle (.67);
\draw[geoTrait] (2.1,-.67) circle (.67);
\draw[otOrange] (2.1,2.37)--(2.77,2.37);
\node[anchor=south] at (2.4,2.47) {$r$};
\draw[cote] (4.65,0)--(4.65,1.7) node[coteTexte,midway] {$h$};
\draw[cote] (0,-1.8)--(4.2,-1.8) node[coteTexte,midway] {$2\pi r$};
\end{tikzpicture}'''

BARRES=r'''\begin{tikzpicture}
\draw[otRule] (0,1)--(5.1,1) (0,2)--(5.1,2) (0,3)--(5.1,3);
\draw[otMuted,->] (0,0)--(0,3.6);
\draw[otMuted,->] (0,0)--(5.3,0);
\node[anchor=south west,text=otMuted] at (0,3.75) {Nombre d'élèves};
\fill[otNavy] (.55,0) rectangle (1.45,3);
\fill[otGreenDark] (2.15,0) rectangle (3.05,1.8);
\fill[otOrange] (3.75,0) rectangle (4.65,1.2);
\node[anchor=south] at (1,3.1) {$10$};
\node[anchor=south] at (2.6,1.9) {$6$};
\node[anchor=south] at (4.2,1.3) {$4$};
\node[anchor=north] at (1,-.18) {À pied};
\node[anchor=north] at (2.6,-.18) {Vélo};
\node[anchor=north] at (4.2,-.18) {Bus};
\node[anchor=east] at (-.15,0) {$0$};
\node[anchor=east] at (-.15,1) {$\frac{10}{3}$};
\node[anchor=east] at (-.15,2) {$\frac{20}{3}$};
\node[anchor=east] at (-.15,3) {$10$};
\end{tikzpicture}'''
# Échelle volontairement entière pour la lecture en cinquième.
BARRES=BARRES.replace(r'(0,1)--(5.1,1) (0,2)--(5.1,2)',r'(0,1.2)--(5.1,1.2) (0,2.4)--(5.1,2.4)')
BARRES=BARRES.replace(r'(-.15,1) {$\frac{10}{3}$}',r'(-.15,1.2) {$4$}').replace(r'(-.15,2) {$\frac{20}{3}$}',r'(-.15,2.4) {$8$}')

SECTEURS=r'''\begin{tikzpicture}
\fill[otNavy!75] (0,0)--(1.6,0) arc[start angle=0,end angle=180,radius=1.6]--cycle;
\fill[otGreen!75] (0,0)--(-1.6,0) arc[start angle=180,end angle=288,radius=1.6]--cycle;
\fill[otOrange!80] (0,0)--({1.6*cos(288)},{1.6*sin(288)}) arc[start angle=288,end angle=360,radius=1.6]--cycle;
\draw[white,line width=.8pt] (0,0)--(1.6,0) (0,0)--(-1.6,0) (0,0)--({1.6*cos(288)},{1.6*sin(288)});
\node[anchor=west] at (2,.8) {À pied : $50\,\%$};
\node[anchor=west] at (2,0) {Vélo : $30\,\%$};
\node[anchor=west] at (2,-.8) {Bus : $20\,\%$};
\end{tikzpicture}'''

def trace(rectangle=False):
    w,h=(4.5,2) if rectangle else (3,3)
    return rf'''\begin{{tikzpicture}}[line cap=round]
\draw[otGreenDark,line width=1pt] (0,0)--({w},0)--({w},{h})--(0,{h})--cycle;
\draw[otGreenDark,->,line width=1pt] (.45,0)--(1.35,0);
\draw[otGreenDark,->,line width=1pt] ({w},.5)--({w},1.4);
\draw[otGreenDark,->,line width=1pt] ({w-.4},{h})--({w-1.3},{h});
\draw[otGreenDark,->,line width=1pt] (0,{h-.4})--(0,{h-1.3});
\node[anchor=north east] at (-.08,-.08) {{$A$}};
\node[anchor=north] at ({w/2},-.2) {{{'$L$' if rectangle else '$c$'}}};
\node[anchor=west] at ({w+.2},{h/2}) {{{'$\ell$' if rectangle else '$c$'}}};
\node[anchor=south] at ({w/2},{h+.2}) {{Sens du parcours}};
\end{{tikzpicture}}'''

def item(name,alt): return {'fichier':name+'.png','alt':alt}

def main():
    for p in sorted(ROOT.iterdir()):
        if p.name[:3] not in {'276','277','278','279','280'}: continue
        num=int(p.name[:3]); meta=json.loads((p/'source_en_ligne/meta.json').read_text(encoding='utf8'))
        corr={'cours':{},'fiches':{},'exercices':{}}; figures={}
        cid=str(meta['cours'][0]['id'])
        if num==276:
            figures={'diagonales':parallelo(diagonales=True),'hauteur':parallelo(hauteur=True),'partage':parallelo(couper=True)}
            corr['cours'][cid]={'1':item('diagonales','Diagonales du parallélogramme ABCD de milieu commun O'),'2':item('hauteur','Base AB et hauteur perpendiculaire h du parallélogramme')}
            for ex in meta['exercices']:
                corr['exercices'][str(ex['id'])]={'1':item('hauteur','Parallélogramme ABCD avec base b et hauteur h'),'2':item('partage','La diagonale AC partage le parallélogramme en deux triangles de même aire')}
        elif num==277:
            figures={'pave':PAVE,'prisme':PRISME,'cylindre':CYLINDRE,'patron':PATRON}
            corr['cours'][cid]={'1':item('pave','Pavé droit de dimensions L, largeur et hauteur h'),'2':item('patron','Patron du cylindre avec deux disques et un rectangle'),'3':item('cylindre','Cylindre de rayon r et de hauteur h')}
            text=(p/'exercices.txt').read_text(encoding='utf8'); blocks=re.split(r'^===[ \t]*$',text,flags=re.M); output=[]
            for b in blocks:
                if not b.strip(): continue
                exid=re.search(r'^Id: (\d+)',b,re.M).group(1)
                if 'Un aquarium' in b:
                    name='pave'; desc='Pavé droit de longueur L, de largeur et de hauteur h'
                    b=b.replace('Schéma de principe :',r'On note $L$ la longueur, $\ell$ la largeur et $h$ la hauteur. Schéma de principe :')
                elif 'cylindrique a un rayon' in b:
                    name='cylindre'; desc='Cylindre de rayon r et de hauteur h'
                    b=b.replace('Schéma de principe :',r'On note $r$ le rayon et $h$ la hauteur. Schéma de principe :')
                else:
                    name='prisme'; desc='Prisme droit de longueur L et de base triangulaire rectangle de côtés a et b'
                    b=b.replace('Schéma de principe :',r'On note $a$ et $b$ les côtés perpendiculaires de la base, et $L$ la longueur du prisme. Schéma de principe :')
                # La seconde image répétait le solide sans aide supplémentaire.
                b=b.replace('[IMAGE_2]','')
                corr['exercices'][exid]={'1':item(name,desc)}
                output.append(b.strip())
            (p/'exercices.txt').write_text('\n\n===\n\n'.join(output)+'\n\n===\n',encoding='utf8')
        elif num==278:
            figures={'barres':BARRES,'secteurs':SECTEURS}
            corr['cours'][cid]={'1':item('barres','Diagramme des transports : 10 élèves à pied, 6 à vélo et 4 en bus'),'2':item('secteurs','Répartition des transports : 50 pour cent à pied, 30 à vélo et 20 en bus')}
            f=next(p.glob('cours_*.txt')); text=f.read_text(encoding='utf8').replace('[IMAGE_1]','[IMAGE_1]\n\n[IMAGE_2]'); f.write_text(text,encoding='utf8')
        elif num==280:
            figures={'carre':trace(),'rectangle':trace(True)}
            corr['cours'][cid]={'1':item('carre','Parcours du carré dans le sens contraire des aiguilles d’une montre, départ A')}
            for b in re.split(r'^===[ \t]*$',(p/'exercices.txt').read_text(encoding='utf8'),flags=re.M):
                if '[IMAGE_2]' not in b: continue
                eid=re.search(r'^Id: (\d+)',b,re.M).group(1); name='carre' if 'répéter 4 fois' in b else 'rectangle'
                corr['exercices'][eid]={'2':item(name,'Sens du parcours fermé depuis A, avec côtés désignés par des lettres')}
            f=p/'exercices.txt'; text=f.read_text(encoding='utf8').replace('[IMAGE_2]',r'Le schéma indique le sens du parcours ; $c$ désigne le côté du carré, ou $L$ et $\ell$ les côtés du rectangle, dans les unités de l’énoncé.'+'\n\n[IMAGE_2]');f.write_text(text,encoding='utf8')
        d=p/'figures';d.mkdir(exist_ok=True)
        module='# -*- coding: utf-8 -*-\n"""Figures TikZ au style des livres ; compiler avec outils/figures_livre.py."""\nFIGURES = {\n'
        module+=''.join(repr(n)+': r"""'+s+'""",\n' for n,s in figures.items())+'}\n'
        (d/'figures.py').write_text(module,encoding='utf8')
        (d/'correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

if __name__=='__main__': main()
