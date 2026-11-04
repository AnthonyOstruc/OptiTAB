"""Mutualise les schémas de principe avec paramètres explicités dans le texte.

Les versions détaillées et tous les PNG existants restent conservés.
"""
from pathlib import Path
import re
import json
import shutil
BASE=Path(__file__).resolve().parent.parent

for code in (269,270):
    d=next(BASE.glob(f'{code}_*')); fd=d/'figures'
    backup=fd/'figures_detaillees.py'
    if not backup.exists():shutil.copyfile(fd/'figures.py',backup)
    namespace={};exec(backup.read_text(encoding='utf-8'),namespace)
    figs={'cours_modele':namespace['FIGURES']['cours_modele']}
    corr=json.loads((fd/'correspondance.json').read_text(encoding='utf-8'))
    t=(d/'exercices.txt').read_text(encoding='utf-8')
    if code==269:
        tex=r'''\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {$b$ cm};
\node[anchor=east] at (-.2,.85) {$k$ cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}'''
    else:
        tex=r'''\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0,0) rectangle (3.8,1.15);
\draw[geoTrait,fill=otGreen!12] (3.8,0) rectangle (5.3,1.15);
\node[text=otNavy,align=center] at (1.9,.575) {$n$ pochettes\\à $x$ euros chacune};
\node[text=otGreenDark] at (4.55,.575) {$b$ euros};
\node[anchor=south] at (2.65,1.4) {Total : $T$ euros};
\node[anchor=north,text=otMuted] at (2.65,-.25) {Schéma non à l'échelle};
\end{tikzpicture}'''
    figs['schema_parametre']=tex
    blocks=re.split(r'^===[ \t]*$',t,flags=re.M)
    out=[]
    for b in blocks:
        if '[IMAGE_1]' not in b:
            out.append(b);continue
        eid=re.search(r'^Id: (\d+)',b,re.M)[1]
        if code==269:
            k,add=re.search(r'hauteur de (\d+) cm.*?x\+(\d+)',b,re.S).groups()
            context=rf'Pour lire le schéma de principe, prendre $k={k}$ et $b={add}$.'
            alt='Rectangle partagé en largeurs x et b, de hauteur k ; paramètres numériques donnés dans l’énoncé.'
        else:
            n,fee,total=re.search(r'achète (\d+) pochettes.*?emballage à (\d+) €.*?totale est de (\d+) €',b,re.S).groups()
            context=rf'Dans le schéma de principe, $n={n}$, $b={fee}$ et $T={total}$.'
            alt='Facture partagée en n pochettes à x euros et frais fixes b ; total T donné dans l’énoncé.'
        if context not in b:b=b.replace('[IMAGE_1]',context+'\n\n[IMAGE_1]',1)
        corr['exercices'][eid]['1']={'fichier':'schema_parametre.png','alt':alt}
        out.append(b)
    (d/'exercices.txt').write_text('\n===\n'.join(out),encoding='utf-8')
    (fd/'correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (fd/'figures.py').write_text('# -*- coding: utf-8 -*-\nFIGURES = {\n'+''.join(f'{n!r}: r"""{v}""",\n' for n,v in figs.items())+'}\n',encoding='utf-8')
    print(code,'2 figures, anciennes sources conservées')
