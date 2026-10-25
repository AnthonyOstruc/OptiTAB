"""Figures vectorielles calculées pour les défis et les sujets originaux."""
from pathlib import Path
from fractions import Fraction
import math

ROOT=Path(__file__).resolve().parent
FIGURES={}
def asset(key,body,caption):
    FIGURES[key]=body+'\n'+r'\par\smallskip\legende{'+caption+'}\n'

def graph(body,bounds,xticks,yticks,width=105,height=52):
    a,b,c,d=bounds
    return rf'''\begin{{tikzpicture}}\begin{{axis}}[otLivreGraphe,width={width}mm,height={height}mm,
xmin={a},xmax={b},ymin={c},ymax={d},xtick={{{xticks}}},ytick={{{yticks}}},scaled ticks=false,
tick label style={{/pgf/number format/use comma}},clip=true]
{body}
\end{{axis}}\end{{tikzpicture}}'''

asset('fr-d01',graph(r'''
\addplot[otNavy,thick,domain=-.2:2.2,samples=90]{x^2-x+.5};
\addplot[otGreenDark,thick,domain=-.2:2.2,samples=90]{x^2-2.4*x+1.2};
\addplot[otMuted,dashed,domain=-.2:2.2,samples=90]{x^2-3*x+1.5};
''',[-.2,2.2,-1,3],'0,1,2','-1,0,1,2,3'),
r'Exemples : bleu $m=1/2$ ; vert $m=6/5$ ; pointillés $m=3/2$. Les positions se démontrent par le calcul.')

asset('fr-d03',graph(r'''
\addplot[otNavy,thick,domain=-1.5:2,samples=100]{x^3-3*x};
\addplot[only marks,otNavy]coordinates{(1,-2.5)};\node[below left,font=\small]at(axis cs:1,-2.5){$P_{-5/2}$};
\geoSolution{\addplot[otGreenDark,thick,domain=-1.5:2]{-2.25*x-.25};
\addplot[otGreenDark,dashed,domain=-1.5:2]{2.598076211*(x-1)-2.5};
\addplot[otGreenDark,dotted,thick,domain=-1.5:2]{-2.598076211*(x-1)-2.5};
\addplot[only marks,otGreenDark]coordinates{(-.3660254,1.0490381)(.5,-1.375)(1.3660254,-1.5490381)};}
''',[-1.5,2.1,-5,3],'-1,0,1,2','-4,-2,0,2',height=57),
r'Bleu : $f(x)=x^3-3x$. Au corrigé, les trois tangentes passant par $P_{-5/2}$ sont ajoutées en vert.')

asset('fr-d04',r'''
\begin{tikzpicture}[x=8mm,y=8mm,font=\small]
\fill[otNavyTint](0,0)--(4,0)--(4,2)arc(0:180:2)--cycle;
\draw[otNavy,thick](0,2)--(0,0)--node[below]{$2r$}(4,0)--node[right]{$h$}(4,2)arc(0:180:2);
\draw[otMuted,dashed](0,2)--(4,2);
\draw[otGreenDark](2,2)--node[above]{$r$}(4,2);\fill[otGreenDark](2,2)circle(1pt);
\end{tikzpicture}''',r'Le diamètre en pointillés est intérieur ; il ne fait pas partie du contour extérieur. Schéma sans échelle imposée.')

asset('fr-d06',r'''
\begin{tikzpicture}[x=27mm,y=27mm,font=\small]
\draw[otMuted,->](-1.3,0)--(1.35,0)node[right]{$x$};\draw[otMuted,->](0,-1.2)--(0,1.35)node[above]{$y$};
\draw[otNavy,thick](0,0)circle(1);\node[below left]at(0,0){$O$};
\draw[otGreenDark](-.7,1.2)--(1.2,-.7)node[below right]{$x+y=1/2$};
\geoSolution{\fill[otGreenDark](.9114378,-.4114378)circle(1.4pt)node[right]{$M$};
\fill[otGreenDark](-.4114378,.9114378)circle(1.4pt)node[above left]{$N$};}
\node[below]at(1,0){$1$};\node[left]at(0,1){$1$};
\end{tikzpicture}''',r'Exemple $k=1/2$ : le problème porte sur les intersections d’une droite de pente $-1$ et du cercle unité.')

asset('fr-d07',r'''
\begin{tikzpicture}[x=12mm,y=12mm,font=\small]
\draw[otMuted,->](-2.5,0)--(2.6,0)node[right]{$x$};\draw[otMuted,->](0,-2.4)--(0,2.5)node[above]{$y$};
\draw[otNavy](0,0)circle(2);\draw[otMuted,dashed](1,-2.2)--(1,2.2);
\fill[otNavy](-2,0)circle(1.2pt)node[below left]{$A$};\fill[otNavy](2,0)circle(1.2pt)node[below right]{$B$};
\fill[otNavy](1,1.7320508)circle(1.2pt)node[above right]{$M_+$};
\fill[otNavy](1,-1.7320508)circle(1.2pt)node[below right]{$M_-$};
\geoSolution{\draw[otGreenDark](-2,0)--(1,1.7320508)--(2,0);
\draw[otGreenDark](-2,0)--(1,-1.7320508)--(2,0);
\draw[otGreenDark](.8700962,1.6570508)--(.9450962,1.5271470)--(1.075,1.6021470);
\draw[otGreenDark](.8700962,-1.6570508)--(.9450962,-1.5271470)--(1.075,-1.6021470);}
\node[below left]at(0,0){$O$};
\end{tikzpicture}''',r'Le cercle de diamètre $[AB]$ et une droite verticale ; l’exemple représenté correspond à $k=20$.')

asset('fr-d08-ex',graph(r'''
\addplot[otNavy,thick,domain=-.2:6.2]{6-x};\node[above right,font=\small]at(axis cs:4,2){$d$};
\addplot[only marks,otNavy]coordinates{(0,0)(4,0)};
\node[above left,font=\small]at(axis cs:0,0){$A$};\node[above right,font=\small]at(axis cs:4,0){$B$};
''',[-.5,6.5,-.5,6.5],'0,2,4,6','0,2,4,6',width=65,height=65),r'Les points fixes $A$ et $B$ et la droite $d:x+y=6$.')

circles=[r'\begin{tikzpicture}[font=\small]']
for j,sgn in enumerate((1,-1)):
    m=-4+sgn*2*math.sqrt(6);radius=math.sqrt(4+m*m);hx=4-m/2;hy=2+m/2
    scale=.67 if j==0 else .22
    circles.append(rf'\begin{{scope}}[xshift={j*73}mm,x={scale}cm,y={scale}cm]')
    circles.append(rf'\draw[otNavy](2,{m:.9f})circle({radius:.9f});')
    circles.append(rf'\draw[otGreenDark,thick]({hx-2:.9f},{hy+2:.9f})--({hx+2:.9f},{hy-2:.9f})node[right]{{$d$}};')
    circles.append(rf'\draw[otGreenDark,dashed](2,{m:.9f})--({hx:.9f},{hy:.9f});')
    for x,y,label,anchor in [(0,0,'A','above left'),(4,0,'B','above right'),(2,m,r'\Omega','below'),(hx,hy,'H','above right')]:
        circles.append(rf'\fill[otNavy]({x:.9f},{y:.9f})circle(1.1pt)node[{anchor}]{{${label}$}};')
    # Angle droit : les deux directions sont (1,-1) et (1,1).
    v=.16/scale
    circles.append(rf'\draw[otGreenDark]({hx+v:.9f},{hy-v:.9f})--({hx:.9f},{hy-2*v:.9f})--({hx-v:.9f},{hy-v:.9f});')
    label=r'm_+=-4+2\sqrt6' if j==0 else r'm_-=-4-2\sqrt6'
    bottom=min(m-radius,-1.5)-.5/scale
    circles.append(rf'\node[below]at(2,{bottom:.9f}){{${label}$}};\end{{scope}}')
circles.append(r'\end{tikzpicture}')
asset('fr-d08-cor','\n'.join(circles),r'Les deux configurations de tangence, dessinées à des échelles différentes. Dans chaque figure, $\Omega H$ est perpendiculaire à $d$.')

def frac(q):
    q=Fraction(q)
    return str(q.numerator) if q.denominator==1 else rf'\frac{{{q.numerator}}}{{{q.denominator}}}'

lines=[r'\begin{tikzpicture}[x=1cm,y=1cm,font=\fontsize{8.5}{10}\selectfont]',
       r'\node[text=otMuted]at(2,3.35){État};\node[text=otMuted]at(4,3.35){Test 1};\node[text=otMuted]at(6,3.35){Test 2};']
leaves=[]
for i in range(8):leaves.append(2.8-i*.8)
lines.append(r'\coordinate (O)at(0,0);')
for g in range(2):
    group=r'D' if g==0 else r'\overline D';prior=Fraction(1,10) if g==0 else Fraction(9,10)
    p=Fraction(9,10) if g==0 else Fraction(1,5)
    gy=sum(leaves[g*4:g*4+4])/4
    lines.append(rf'\node[fill=white,inner sep=1pt](G{g})at(2,{gy:.3f}){{${group}$}};')
    lines.append(rf'\draw[otNavy](O)--node[above,sloped,fill=white,inner sep=1pt]{{${frac(prior)}$}}(G{g});')
    for s in range(2):
        yy=sum(leaves[g*4+s*2:g*4+s*2+2])/2;ps=p if s==0 else 1-p;symbol='+' if s==0 else '-'
        lines.append(rf'\node[fill=white,inner sep=1pt](S{g}{s})at(4,{yy:.3f}){{${symbol}$}};')
        lines.append(rf'\draw[otNavy](G{g})--node[above,sloped,fill=white,inner sep=1pt]{{${frac(ps)}$}}(S{g}{s});')
        for t in range(2):
            y=leaves[g*4+s*2+t];pt=p if t==0 else 1-p;symbol2='+' if t==0 else '-';mass=prior*ps*pt
            lines.append(rf'\node[fill=white,inner sep=1pt](L{g}{s}{t})at(6,{y:.3f}){{${symbol2}$}};')
            lines.append(rf'\draw[otNavy](S{g}{s})--node[above,sloped,fill=white,inner sep=1pt]{{\geoSolution{{${frac(pt)}$}}}}(L{g}{s}{t});')
            lines.append(rf'\geoSolution{{\node[anchor=west,text=otGreenDark]at(6.3,{y:.3f}){{$P={frac(mass)}$}};}}')
lines.append(r'\end{tikzpicture}')
asset('fr-d09','\n'.join(lines),r'Groupes, premier test, second test. Au corrigé, les poids du dernier niveau et les probabilités des huit chemins sont ajoutés.')

asset('fr-d10',r'''
\begingroup\renewcommand{\arraystretch}{1.35}\begin{tabular}{@{}lccc@{}}\toprule
Issue & $I_1$ & $I_2$ & $I_3$\\\midrule
Probabilité & $1/4$ & $1/2$ & $1/4$\\
Lot $L_a$ & $2a$ & $2-a$ & $6$\\
\geoSolution{Gain $G_a$ & $2a-5/2$ & $-a-1/2$ & $7/2$\\}
\bottomrule\end{tabular}\endgroup''',r'Les colonnes désignent les issues. Si deux valeurs du lot coïncident, leurs probabilités se regroupent dans la loi.')

asset('fr-d11',graph(r'''
\addplot[only marks,otNavy]coordinates{(0,2)(2,2)(8,1)(10,1)(0,0)(2,0)(8,0)(10,0)};
\geoSolution{\draw[otGreenDark,dashed](axis cs:1,1.75)--(axis cs:1,2.25);
\draw[otGreenDark,dashed](axis cs:9,.75)--(axis cs:9,1.25);
\draw[otGreenDark,dashed](axis cs:5,-.25)--(axis cs:5,.25);}
''',[-1,11,-.5,2.6],'0,2,4,6,8,10','0,1,2',width=110,height=42).replace('ytick={0,1,2},','ytick={0,1,2},yticklabels={Réunion,B,A},ylabel={},axis lines=left,every axis x label/.style={at={(axis description cs:1,0)},anchor=north east,yshift=-4mm,font=\\small,text=otMuted},'),
r'Mêmes valeurs, présentées dans leurs groupes et dans la réunion. Au corrigé, les traits verts repèrent les moyennes.')

asset('fr-d12',graph(r'''
\addplot[otNavy,thick,domain=0:1,samples=90]{x^3+x-1};
\draw[otGreenDark,dashed](axis cs:.682327804,0)--(axis cs:.682327804,-1);
\node[above left,font=\small]at(axis cs:.682327804,0){$\alpha$};
''',[-.05,1.1,-1.1,1.1],'0,.5,1','-1,0,1',width=95,height=47),r'Le graphique situe la racine ; les signes aux bornes et la largeur de l’intervalle donnent l’encadrement garanti.')

def binary_tree(key,p,first='D',second='D',caption=''):
    p=Fraction(p);body=[r'\begin{tikzpicture}[x=1cm,y=1cm,font=\small]\coordinate(O)at(0,0);']
    for a in range(2):
        q=p if a==0 else 1-p;y=1.1 if a==0 else -1.1
        name=first if a==0 else r'\overline{'+first+'}'
        body.append(rf'\node[fill=white,inner sep=1pt](A{a})at(2.5,{y}){{${name}$}};')
        body.append(rf'\draw[otNavy](O)--node[above,sloped,fill=white]{{${frac(q)}$}}(A{a});')
        for b in range(2):
            w=p if b==0 else 1-p;yy=y+(.45 if b==0 else -.45);nm=second if b==0 else r'\overline{'+second+'}'
            body.append(rf'\node[fill=white,inner sep=1pt](B{a}{b})at(5,{yy}){{${nm}$}};')
            body.append(rf'\draw[otNavy](A{a})--node[above,sloped,fill=white]{{${frac(w)}$}}(B{a}{b});')
            body.append(rf'\node[anchor=west,text=otGreenDark]at(5.35,{yy}){{$P={frac(q*w)}$}};')
    body.append(r'\end{tikzpicture}');asset(key,'\n'.join(body),caption)
binary_tree('fr-d14','1/10','D_1','D_2',r'Deux articles indépendants au réglage optimal ; $D_i$ désigne le défaut de l’article $i$.')

asset('fr-sa-fonction',graph(r'''
\addplot[otNavy,thick,domain=0:4,samples=90]{x^3-6*x^2+9*x+2};
\addplot[otGreenDark,domain=0:4]{-3*x+10};
\addplot[only marks,otNavy]coordinates{(0,2)(1,6)(3,2)(4,6)};
''',[-.2,4.2,-1,11],'0,1,2,3,4','0,2,4,6,8,10',height=53),r'La tangente en 2 traverse la courbe ; le signe de $(x-2)^3$ justifie la position relative.')

asset('fr-sa-arbre',r'''
\begin{tikzpicture}[x=1cm,y=1cm,font=\small]\coordinate(O)at(0,0);
\node[fill=white](A)at(2.5,1){$A$};\node[fill=white](B)at(2.5,-1){$B$};
\draw[otNavy](O)--node[above,sloped,fill=white]{$3/5$}(A);
\draw[otNavy](O)--node[above,sloped,fill=white]{$2/5$}(B);
\node[fill=white](AD)at(5,1.45){$D$};\node[fill=white](AN)at(5,.55){$\overline D$};
\node[fill=white](BD)at(5,-.55){$D$};\node[fill=white](BN)at(5,-1.45){$\overline D$};
\draw[otNavy](A)--node[above,sloped,fill=white]{$1/20$}(AD);
\draw[otNavy](A)--node[above,sloped,fill=white]{\geoSolution{$19/20$}}(AN);
\draw[otNavy](B)--node[above,sloped,fill=white]{$1/10$}(BD);
\draw[otNavy](B)--node[above,sloped,fill=white]{\geoSolution{$9/10$}}(BN);
\end{tikzpicture}''',r'$A$ et $B$ sont les ateliers ; $D$ signifie que l’article présente un défaut.')

asset('fr-sb-geometrie',graph(r'''
\addplot[otNavy,thick]coordinates{(0,0)(4,0)(1,3)(0,0)};
\addplot[only marks,otNavy]coordinates{(0,0)(4,0)(1,3)(5,4)};
\node[below left,font=\small]at(axis cs:0,0){$A$};\node[below right,font=\small]at(axis cs:4,0){$B$};
\node[above left,font=\small]at(axis cs:1,3){$C$};\node[below right,font=\small]at(axis cs:5,4){$M$};
\geoSolution{\addplot[otGreenDark,domain=0:360,samples=100]({2+sqrt(5)*cos(x)},{1+sqrt(5)*sin(x)});
\addplot[otGreenDark,domain=-.5:6]{(x+5)/2};
\draw[otGreenDark,dashed](axis cs:2,1)--(axis cs:1,3);
\draw[otGreenDark,dashed](axis cs:5,4)--(axis cs:4.6,4.8);
\addplot[only marks,otGreenDark]coordinates{(2,1)(4.6,4.8)};
\draw[otGreenDark](axis cs:1.178885,3.089443)--(axis cs:1.268328,2.910557)--(axis cs:1.089443,2.821115);
\draw[otGreenDark](axis cs:4.778885,4.889443)--(axis cs:4.868328,4.710557)--(axis cs:4.689443,4.621115);
\node[below,font=\small]at(axis cs:2,1){$\Omega$};\node[above,font=\small]at(axis cs:4.6,4.8){$H$};}
''',[-.6,6,-1.5,5.8],'0,1,2,3,4,5','-1,0,1,2,3,4,5',width=82,height=88),r'Au corrigé : cercle circonscrit, tangente en $C$ et projeté $H$ de $M$. Le repère est orthonormé.')
for key in ('fr-sb-geometrie','fr-d08-ex'):
    FIGURES[key]=FIGURES[key].replace('scaled ticks=false,','unit vector ratio=1 1,scaled ticks=false,')

# Automatismes des sujets : lectures graphiques sur quadrillage, valeurs lisibles aux nœuds.
def panneau(titre,body,bounds,xticks,yticks,width=74,height=47):
    a,b,c,d=bounds
    return rf'''\begin{{tikzpicture}}[baseline=(current bounding box.center)]\begin{{axis}}[otLivreGraphe,width={width}mm,height={height}mm,
xmin={a},xmax={b},ymin={c},ymax={d},xtick={{{xticks}}},ytick={{{yticks}}},scaled ticks=false,
tick label style={{/pgf/number format/use comma}},clip=true,
title={{{titre}}},title style={{at={{(0.5,0)}},anchor=north,yshift=-1.5mm,font=\otMedium\fontsize{{8}}{{10}}\selectfont,text=otMuted}}]
{body}
\end{{axis}}\end{{tikzpicture}}'''

asset('fr-sa-auto',panneau('Figure 1',r'''
\addplot[otNavy,thick,domain=-2:4,samples=90]{(x^2-2*x-1)/2};
\node[otEtiquette,text=otNavy]at(axis cs:-0.75,3.3){$\mathcal C_f$};
\geoSolution{\addplot[otGreenDark,dashed,domain=-2.5:4.5]{1};
\addplot[otGreenDark,line width=1.6pt]coordinates{(-1,0)(3,0)};
\draw[otGreenDark,dotted](axis cs:-1,1)--(axis cs:-1,0) (axis cs:3,1)--(axis cs:3,0);
\addplot[only marks,otGreenDark]coordinates{(-1,1)(3,1)};}
''',[-2.5,4.5,-1.5,4],'-2,-1,0,1,2,3,4','-1,0,1,2,3,4')+r'\hspace{6mm}'+panneau('Figure 2',r'''
\addplot[otNavy,thick,domain=-1.5:7.5]{-x/2+3};
\node[otEtiquette,text=otNavy]at(axis cs:5.6,1.25){$d$};
\geoSolution{\draw[otGreenDark,thick](axis cs:0,3)--(axis cs:2,3)--(axis cs:2,2);
\node[above,font=\small,text=otGreenDark]at(axis cs:1,3){$+2$};
\node[right,font=\small,text=otGreenDark]at(axis cs:2,2.5){$-1$};
\addplot[only marks,otGreenDark]coordinates{(0,3)(2,2)};}
''',[-1.5,7.5,-1.5,4.5],'-1,0,1,2,3,4,5,6,7','-1,0,1,2,3,4'),
r'\geoEnonce{Repères quadrillés : les points utiles sont situés sur des nœuds du quadrillage.}'
r'\geoSolution{Figure 1 : la courbe est sous la droite $y=1$ entre $-1$ et 3. Figure 2 : ordonnée à l’origine 3 et pente $-1/2$.}')

asset('fr-sb-auto',panneau('Figure 1',r'''
\addplot[otNavy,thick,domain=-2:4,samples=90]{-(x+1)*(x-3)/2};
\node[otEtiquette,text=otNavy]at(axis cs:3.2,1.6){$\mathcal C_g$};
\geoSolution{\addplot[otGreenDark,line width=1.6pt,domain=-1:3,samples=60]{-(x+1)*(x-3)/2};
\addplot[only marks,otGreenDark]coordinates{(-1,0)(3,0)};}
''',[-2.5,4.5,-3,2.5],'-2,-1,0,1,2,3,4','-3,-2,-1,0,1,2')+r'\hspace{6mm}'+r'''\begin{tikzpicture}[baseline=(current bounding box.center),x=3mm,y=1mm,font=\small]
\node[font=\otMedium\fontsize{8}{10}\selectfont,text=otMuted,anchor=north]at(11.5,-6){Figure 2};
\draw[otMuted,->](0,0)--(23,0);
\foreach \t in {0,2,...,22}{\draw[otMuted](\t,1)--(\t,-1)node[below,font=\fontsize{7}{8}\selectfont,text=otMuted]{$\t$};}
\foreach \t in {1,3,...,21}{\draw[otMuted](\t,.6)--(\t,-.6);}
\draw[otNavy,thick](4,14)--(9,14) (15,14)--(20,14) (4,10)--(4,18) (20,10)--(20,18);
\draw[otNavy,thick,fill=otNavyTint](9,8)rectangle(15,20);
\draw[otNavy,thick](12,8)--(12,20);
\geoSolution{\draw[otGreenDark,<->](9,23)--node[above,font=\small]{$6$}(15,23);
\node[below,font=\small,text=otGreenDark]at(9,7.6){$Q_1$};
\node[below,font=\small,text=otGreenDark]at(12,7.6){$\mathrm{Me}$};
\node[below,font=\small,text=otGreenDark]at(15,7.6){$Q_3$};}
\end{tikzpicture}''',
r'\geoEnonce{Les points utiles sont sur des nœuds du quadrillage ; les moustaches de la boîte vont du minimum au maximum.}'
r'\geoSolution{Figure 1 : $g$ est positive sur la partie verte, entre ses zéros $-1$ et 3. Figure 2 : $Q_1=9$, médiane 12, $Q_3=15$.}')

def ecrire_figures():
    for key,text in FIGURES.items():
        (ROOT/'figures'/f'{key}.tex').write_text(text,encoding='utf-8')
