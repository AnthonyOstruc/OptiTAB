"""Sources des nouveaux schémas, exclusivement dans les notions 266–270."""
from pathlib import Path
import re
BASE=Path(__file__).resolve().parent.parent

NEW={266:{},267:{},268:{},269:{},270:{}}

NEW[266]['lecture_bilan']=r'''\begin{tikzpicture}
\fill[otNavy!20] (0,0) rectangle (2.25,.65);
\fill[otGreen!25] (2.25,0) rectangle (4.75,.65);
\fill[otOrange!30] (4.75,0) rectangle (5.25,.65);
\draw[geoTrait] (0,0) rectangle (6,.65);
\draw[otNavy!60] (2.25,0)--(2.25,.65) (4.75,0)--(4.75,.65) (5.25,0)--(5.25,.65);
\node[anchor=south,text=otNavy] at (1.125,.85) {Lundi};
\node[anchor=south,text=otGreenDark] at (3.5,.85) {Mardi};
\node[anchor=south east,text=otOrange!80!black] at (5.45,1.5) {Mercredi};
\draw[otOrange!80!black,line width=.5pt] (5,1.45)--(5,.85);
\node[anchor=north] at (1.125,-.15) {90 pages};
\node[anchor=north] at (3.5,-.15) {100 pages};
\node[anchor=north] at (5,-.75) {20 pages};
\node[anchor=south west] at (5.4,1.5) {Reste};
\draw[otMuted,line width=.5pt] (5.7,1.45)--(5.7,.85);
\node[anchor=north west] at (5.32,-.15) {30 pages};
\node[anchor=north,text=otGreenDark] at (3,-1.35) {210 pages lues sur 240 : $\frac78$ du livre};
\end{tikzpicture}'''

lines=[r'\begin{tikzpicture}',r'\fill[otGreen!10] (0,0) rectangle (3.6,3.6);']
for n in range(10):
    x=n*.4
    lines.append(rf'\draw[otNavy!60,line width=.45pt] ({x:.2f},0)--({x:.2f},3.6) (0,{x:.2f})--(3.6,{x:.2f});')
lines += [r'\draw[geoTrait] (0,0) rectangle (3.6,3.6);',r'\node[anchor=south] at (1.8,3.9) {Terrasse : $4{,}5$ m de côté};',r'\node[anchor=north,text=otGreenDark] at (1.8,-.25) {$9\times9=81$ dalles};',r'\node[anchor=west,align=left] at (4,1.8) {Une dalle :\\$0{,}5$ m de côté};',r'\end{tikzpicture}']
NEW[267]['terrasse_81']='\n'.join(lines)

lines=[r'\begin{tikzpicture}',r'\fill[otGreen!10] (0,0) rectangle (2.4,2.4);']
for j in range(7):
    x=j*.4
    lines.append(rf'\draw[otNavy!55,line width=.4pt] ({x:.2f},0)--({x:.2f},2.4) (0,{x:.2f})--(2.4,{x:.2f});')
lines += [r'\draw[geoTrait] (0,0) rectangle (2.4,2.4);',r'\draw[geoTrait] (0,2.4)--(.8,3.2)--(3.2,3.2)--(3.2,.8)--(2.4,0);',r'\draw[geoTrait] (2.4,2.4)--(3.2,3.2);',r'\draw[geoAide] (0,0)--(.8,.8)--(3.2,.8) (.8,.8)--(.8,3.2);',r'\node[anchor=north] at (1.2,-.25) {$30$ cm};',r'\node[anchor=west,align=left] at (3.6,1.8) {Petits cubes :\\arête $5$ cm};',r'\node[anchor=south,text=otGreenDark] at (1.6,3.5) {$6$ cubes par arête : $6^3=216$ cubes};',r'\end{tikzpicture}']
NEW[267]['cube_216']='\n'.join(lines)

for corrected in (False,True):
    code=[r'\begin{tikzpicture}',r'\fill[otSky] (0,0) rectangle (3,3);',r'\fill[white] (.6,.6) rectangle (2.4,2.4);']
    if corrected:
        code += [r'\fill[otGreen!25] (0,0) rectangle (3,.6);',r'\fill[otGreen!25] (0,2.4) rectangle (3,3);',r'\fill[otNavy!15] (0,.6) rectangle (.6,2.4);',r'\fill[otNavy!15] (2.4,.6) rectangle (3,2.4);']
    for j in range(6):
        x=j*.6
        code.append(rf'\draw[otNavy!55,line width=.45pt] ({x:.1f},0)--({x:.1f},3) (0,{x:.1f})--(3,{x:.1f});')
    code += [r'\draw[geoTrait] (0,0) rectangle (3,3);',r'\draw[geoTrait] (.6,.6) rectangle (2.4,2.4);',r'\node[anchor=south] at (1.5,3.25) {Rang $3$};']
    if corrected:
        code += [r'\node[anchor=west,text=otGreenDark,align=left] at (3.5,2.6) {Haut : $5$\\Bas : $5$};',r'\node[anchor=west,text=otNavy,align=left] at (3.5,1.2) {Gauche : $3$\\Droite : $3$};',r'\node[anchor=north,text=otGreenDark] at (1.5,-.25) {$5+5+3+3=16$ carreaux};']
    else:code += [r'\node[anchor=north,text=otMuted] at (1.5,-.25) {Le carré central est exclu};']
    code.append(r'\end{tikzpicture}')
    NEW[268]['bordure_corrige' if corrected else 'bordure_enonce']='\n'.join(code)

NEW[269]['rectangle_aires_corrige']=r'''\begin{tikzpicture}
\fill[otGreen!12] (0,0) rectangle (3,1.7);
\fill[otGreen!20] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south] at (1.5,1.9) {$x$ cm};
\node[anchor=south] at (3.8,1.9) {$b$ cm};
\node[anchor=east] at (-.2,.85) {$k$ cm};
\node[text=otGreenDark] at (1.5,.85) {$kx$};
\node[text=otGreenDark] at (3.8,.85) {$kb$};
\node[anchor=north,text=otGreenDark] at (2.3,-.25) {$k(x+b)=kx+kb$};
\end{tikzpicture}'''

def main():
    for code,figs in NEW.items():
        if not figs:continue
        d=next(BASE.glob(f'{code}_*'));p=d/'figures/figures.py'
        # Repartir de la source sauvegardée, sans perdre les figures précédentes.
        original=(d/'sauvegardes/revision_2026-10-30/figures/figures.py').read_text(encoding='utf-8')
        source=original+'\n\n# Figures de la révision pédagogique du 30 octobre 2026.\nFIGURES.update({\n'
        source+=''.join(f'{name!r}: r"""{tikz}""",\n' for name,tikz in figs.items())+'})\n'
        p.write_text(source,encoding='utf-8')
        print(code,','.join(figs))

if __name__=='__main__':main()
