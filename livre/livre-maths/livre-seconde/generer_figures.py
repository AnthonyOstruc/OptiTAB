"""Figures vectorielles issues des données des exercices, sans image générative."""
from pathlib import Path
from math import ceil,floor,sqrt,tan,pi
from modele import FIGURES,figure,tableau

def number(a):
    return f'{float(a):.8g}'

def geo(name,points,segments=(),vectors=(),solpoints=(),solsegments=(),circles=(),lines=(),extra='',caption='Repère orthonormé ; les graduations fixent les unités.',frame=()):
    # Les points ajoutés au corrigé participent au cadrage dès l’énoncé.
    allp=list(points)+list(solpoints)
    xs=[float(p[1]) for p in allp]+[0]+[p[0] for p in frame]
    ys=[float(p[2]) for p in allp]+[0]+[p[1] for p in frame]
    for cx,cy,r in circles: xs.extend([cx-r,cx+r]);ys.extend([cy-r,cy+r])
    xmin,xmax=floor(min(xs))-1,ceil(max(xs))+1
    ymin,ymax=floor(min(ys))-1,ceil(max(ys))+1
    scale=min(.62,12.8/(xmax-xmin),5.9/(ymax-ymin))
    start=rf'\begin{{tikzpicture}}[x={scale:.5f}cm,y={scale:.5f}cm,font=\scriptsize]'+'\n'
    start+=rf'\draw[otRule!65,line width=.25pt,step=1] ({xmin},{ymin}) grid ({xmax},{ymax});'+'\n'
    start+=rf'\draw[otMuted,->] ({xmin},0)--({xmax+.35},0) node[right] {{$x$}};\draw[otMuted,->] (0,{ymin})--(0,{ymax+.35}) node[above] {{$y$}};'+'\n'
    stepx=max(1,ceil((xmax-xmin)/10));stepy=max(1,ceil((ymax-ymin)/9))
    for v in range(xmin+1,xmax,stepx):
        if v: start+=rf'\node[below,text=otMuted,font=\fontsize{{6}}{{7}}\selectfont] at ({v},0) {{{v}}};'
    for v in range(ymin+1,ymax,stepy):
        if v: start+=rf'\node[left,text=otMuted,font=\fontsize{{6}}{{7}}\selectfont] at (0,{v}) {{{v}}};'
    coords={p[0]:(float(p[1]),float(p[2])) for p in allp}
    for a,b in segments:
        start+=rf'\draw[geoTrait] ({number(coords[a][0])},{number(coords[a][1])})--({number(coords[b][0])},{number(coords[b][1])});'
    for a,b in vectors:
        start+=rf'\draw[geoVecteur] ({number(coords[a][0])},{number(coords[a][1])})--({number(coords[b][0])},{number(coords[b][1])});'
    start+=rf'\begin{{scope}}\clip ({xmin},{ymin}) rectangle ({xmax},{ymax});'
    for a,b,c in lines:
        if abs(b)>1e-10:
            start+=rf'\draw[geoTrait] ({xmin},{number((-a*xmin-c)/b)})--({xmax},{number((-a*xmax-c)/b)});'
        else:
            start+=rf'\draw[geoTrait] ({number(-c/a)},{ymin})--({number(-c/a)},{ymax});'
    for cx,cy,r in circles: start+=rf'\draw[geoTrait] ({number(cx)},{number(cy)}) circle ({number(r)});'
    start+=r'\end{scope}'
    for point in points:
        lab,xx,yy,*pos=point;anchor=pos[0] if pos else 'above right'
        start+=rf'\fill[otNavy] ({number(xx)},{number(yy)}) circle (1.7pt) node[{anchor},geoLabel] {{${lab}$}};'
    solution=''
    for a,b in solsegments:
        solution+=rf'\draw[geoAide] ({number(coords[a][0])},{number(coords[a][1])})--({number(coords[b][0])},{number(coords[b][1])});'
    for point in solpoints:
        lab,xx,yy,*pos=point;anchor=pos[0] if pos else 'above right'
        solution+=rf'\fill[otGreenDark] ({number(xx)},{number(yy)}) circle (2pt) node[{anchor},geoLabel,text=otGreenDark] {{${lab}$}};'
    start+=r'\geoSolution{'+solution+'}'+extra+r'\end{tikzpicture}'
    return figure(name,start,caption)

def graph(name,curves,xb,yb,caption,points=(),sol=''):
    xmin,xmax=xb;ymin,ymax=yb;sx=11/(xmax-xmin);sy=4.8/(ymax-ymin)
    tex=rf'\begin{{tikzpicture}}[x={sx:.6f}cm,y={sy:.6f}cm,font=\scriptsize]'
    # Échelles explicites, éventuellement différentes sur les deux axes.
    stepx=max(1,ceil((xmax-xmin)/10));stepy=max(1,ceil((ymax-ymin)/7))
    for a in range(ceil(xmin),floor(xmax)+1,stepx): tex+=rf'\draw[otRule!70,line width=.25pt] ({a},{ymin})--({a},{ymax});'
    for a in range(ceil(ymin),floor(ymax)+1,stepy): tex+=rf'\draw[otRule!70,line width=.25pt] ({xmin},{a})--({xmax},{a});'
    tex+=rf'\draw[otMuted,->] ({xmin},0)--({xmax+.15},0) node[right] {{$x$}};\draw[otMuted,->] (0,{ymin})--(0,{ymax+.15}) node[above] {{$y$}};'
    for a in range(ceil(xmin),floor(xmax)+1,stepx):
        if a: tex+=rf'\node[below,fill=white,inner sep=.5pt,font=\fontsize{{6.5}}{{7}}\selectfont,text=otMuted] at ({a},0) {{{a}}};'
    for a in range(ceil(ymin),floor(ymax)+1,stepy):
        if a: tex+=rf'\node[left,fill=white,inner sep=.5pt,font=\fontsize{{6.5}}{{7}}\selectfont,text=otMuted] at (0,{a}) {{{a}}};'
    tex+=rf'\begin{{scope}}\clip ({xmin},{ymin}) rectangle ({xmax},{ymax});'
    for k,(expr,lo,hi) in enumerate(curves):
        color='otNavy' if k==0 else 'otGreenDark'
        dash=',dashed' if k>=2 else ''
        tex+=rf'\draw[{color},line width=.9pt{dash}] plot[domain={lo}:{hi},samples=91] (\x,{{{expr}}});'
    for lab,a,b in points: tex+=rf'\fill[otNavy] ({a},{b}) circle (1.7pt) node[above right,geoLabel] {{${lab}$}};'
    tex+=r'\geoSolution{'+sol+r'}\end{scope}\end{tikzpicture}'
    return figure(name,tex,caption+' Les graduations donnent l’échelle de chaque axe.')

def tree(name,first,second,lab=('A',r'\overline A','B',r'\overline B'),caption='Les poids se lisent à partir du nœud de départ ; les feuilles représentent des intersections.',blank=False):
    tex=r'\begin{tikzpicture}[x=1cm,y=1cm,font=\small]'
    nodes=[('o',0,0,''),('a',2,1,lab[0]),('b',2,-1,lab[1]),('aa',4.4,1.55,lab[2]),('ab',4.4,.45,lab[3]),('ba',4.4,-.45,lab[2]),('bb',4.4,-1.55,lab[3])]
    for node,x,y,label in nodes:tex+=rf'\node[inner sep=2pt] ({node}) at ({x},{y}) {{${label}$}};'
    edges=[('o','a',first[0]),('o','b',first[1]),('a','aa',second[0]),('a','ab',second[1]),('b','ba',second[2]),('b','bb',second[3])]
    for a,b,w in edges:
        weight=r'\geoSolution{$'+w+'$}' if blank else '$'+w+'$'
        tex+=rf'\draw[otNavy!70] ({a}.east)--node[above,sloped,fill=white,inner sep=1pt,font=\scriptsize,text=otGreenDark] {{{weight}}} ({b}.west);'
    return figure(name,tex+r'\end{tikzpicture}',caption)

def build():
    # Droite réelle et intervalles : bornes ouvertes ou fermées explicitement codées.
    figure('intervalles',r'''\begin{tikzpicture}[x=.8cm,y=1cm,font=\small]
\draw[otMuted,->](-4,0)--(6,0);\foreach \x in {-3,0,2,5}{\draw(\x,-.06)--(\x,.06)node[below=2mm]{$\x$};}
\draw[otNavy,line width=1.4pt](-3,.55)--(2,.55);\fill[otNavy](-3,.55)circle(2pt);\fill[otNavy](2,.55)circle(2pt);\node[left]at(-3,.55){$I$};
\draw[otGreenDark,line width=1.4pt](0,1.1)--(5,1.1);\draw[otGreenDark,fill=white](0,1.1)circle(2pt);\fill[otGreenDark](5,1.1)circle(2pt);\node[left]at(0,1.1){$J$};
\end{tikzpicture}''','Un disque plein inclut la borne ; un disque vide l’exclut.')
    figure('intervalle-centre',r'''\begin{tikzpicture}[x=.9cm,y=1cm,font=\small]
\draw[otMuted,->](-2,0)--(6,0);\foreach \x in {-1,2,5}{\draw(\x,-.08)--(\x,.08)node[below=2mm]{$\x$};}
\fill[otNavy](2,0)circle(2pt);\draw[otNavy,<->](-1,.7)--node[above]{$3$}(2,.7);\draw[otNavy,<->](2,.7)--node[above]{$3$}(5,.7);
\geoSolution{\draw[otGreenDark,line width=2pt](-1,0)--(5,0);\foreach \x in {-1,5}{\fill[otGreenDark](\x,0)circle(2pt);}}
\end{tikzpicture}''','Distance au centre 2 ; le corrigé complète l’intervalle admissible.')
    figure('bordure',r'''\begin{tikzpicture}[x=.8cm,y=.8cm,font=\small]
\fill[otNavyTint](0,0)rectangle(6,6);\fill[white](1,1)rectangle(5,5);
\draw[geoTrait](0,0)rectangle(6,6);\draw[geoTrait](1,1)rectangle(5,5);
\draw[<->](1,3)--node[above]{$x$}(5,3);\draw[<->](0,-.3)--node[below]{$x+4$}(6,-.3);
\draw[<->](0,5.5)--node[above]{$2$}(1,5.5);\end{tikzpicture}''','Schéma de principe de la bordure, sans échelle imposée.')
    for name,critical,rows in [
      ('signes-produit',[-3,1],[('$x+3$','-','0','+','','+'),('$x-1$','-','','-','0','+'),('Produit','+','0','-','0','+')]),
      ('signes-quotient',[-1,2],[('$x+1$','-','0','+','','+'),('$x-2$','-','','-','0','+'),('Quotient','+','interdit','-','0','+')])]:
        # Les cases de signes sont à compléter dans l’énoncé.
        head=['$x$',r'$-\infty$','$'+str(critical[0])+'$','', '$'+str(critical[1])+'$',r'$+\infty$']
        tabrows=[]
        for row in rows:
            tabrows.append([row[0]]+[r'\geoSolution{'+('$'+v+'$' if v in '+-0' and v else v)+r'}\geoEnonce{\phantom{+}}' for v in row[1:]])
        figure(name,tableau(head,tabrows),'Tableau à compléter dans l’énoncé ; signes et valeurs interdites au corrigé.')
    figure('rectangle-equation',r'\begin{tikzpicture}[x=1cm,y=1cm]\draw[geoTrait](0,0)rectangle(6,2.5);\node[below]at(3,0){$x+3$};\node[right]at(6,1.25){$x-1$};\end{tikzpicture}','Rectangle de dimensions indiquées ; schéma sans échelle imposée.')
    graph('fonction-appartenance',[(r'\x*\x+2',-2.5,3.2)],(-3,4),(-1,13),'Courbe de $f(x)=x^2+2$ et points proposés.',[('A',1,3),('B',-2,6),('C',3,10)])
    graph('antecedents-parabole',[(r'(\x-1)^2',-3,5)],(-3,5),(-1,11),'La parabole $y=(x-1)^2$ ; droite $y=9$ au corrigé.',sol=r'\draw[geoAide](-3,9)--(5,9);\fill[otGreenDark](-2,9)circle(2pt);\fill[otGreenDark](4,9)circle(2pt);')
    graph('intersection-fonctions',[(r'\x*\x',-2.5,3),(r'\x+2',-2.5,3)],(-2.5,3),(-1,7),'Parabole bleue : $y=x^2$ ; droite verte : $y=x+2$.')
    figure('fonction-morceaux',r'''\begin{tikzpicture}[x=1.3cm,y=.8cm,font=\small]
\draw[otRule!70,step=1](-3,-2)grid(5,4);\draw[otMuted,->](-3,0)--(5.3,0)node[right]{$x$};\draw[otMuted,->](0,-2)--(0,4.3)node[above]{$y$};
\foreach \x in {-2,-1,1,2,3,4}{\node[below,fill=white,inner sep=1pt]at(\x,0){$\x$};}\foreach \y in {-1,1,2,3}{\node[left,fill=white,inner sep=1pt]at(0,\y){$\y$};}
\draw[geoTrait](-2,1)--(0,3)--(2,-1)--(4,1);\foreach \x/\y in {-2/1,0/3,2/-1,4/1}{\fill[otNavy](\x,\y)circle(2pt);}
\end{tikzpicture}''','Entre deux sommets, la fonction est affine. Les deux axes sont gradués.')
    graph('tarif-plafond',[(r'3*\x',0,5),('15',5,8)],(0,8),(-1,17),'Abscisse : durée en heures ; ordonnée : coût en euros.')
    figure('cylindre',r'''\begin{tikzpicture}[x=.9cm,y=.9cm,font=\small]
\draw[geoTrait](-2,0)--(-2,3.5)arc(180:0:2 and .5)--(2,0);
\draw[geoTrait](0,0)ellipse(2 and .5);\draw[geoTrait](0,3.5)ellipse(2 and .5);
\draw[geoAide](0,0)--node[right]{$h$}(0,2);\draw[geoTrait](0,2)ellipse(2 and .5);
\draw[<->](0,0)--node[below]{$2\text{ m}$}(2,0);\end{tikzpicture}''','Vue en perspective ; $h$ varie entre 0 et 3 m. Le dessin n’est pas à l’échelle.')
    graph('reference-affine',[(r'-2*\x+3',-1,4)],(-1,4),(-6,5),'Droite $y=-2x+3$.')
    graph('reference-inverse',[(r'1/\x',-5,-.2),(r'1/\x',.2,5)],(-5,5),(-4,4),'Les deux branches de $y=1/x$ ; 0 est exclu du domaine.')
    graph('reference-racine',[(r'sqrt(\x)',0,9)],(-1,9),(-1,4),r'Courbe $y=\sqrt x$, définie pour $x\ge0$.')
    graph('reference-absolue',[(r'abs(\x)',-5,5)],(-5,5),(-1,6),'Courbe $y=|x|$ ; la droite $y=4$ apparaît au corrigé.',sol=r'\draw[geoAide](-5,4)--(5,4);')
    graph('reference-cube',[(r'\x*\x*\x',-2,2)],(-2,2),(-8,8),'Courbe $y=x^3$.')
    graph('reference-carre',[(r'\x*\x',-4,4)],(-4,4),(-1,12),'Courbe $y=x^2$ ; la droite $y=9$ est ajoutée au corrigé.',sol=r'\draw[geoAide](-4,9)--(4,9);')
    graph('carre-identite',[(r'\x*\x',0,2.3),(r'\x',0,2.3)],(0,2.3),(-.3,5),'Parabole bleue : $y=x^2$ ; droite verte : $y=x$.')
    graph('variation-decalee',[(r'(\x-3)^2-2',0,7)],(0,7),(-3,15),'Courbe $y=(x-3)^2-2$ sur $[0;7]$.')
    graph('aire-produit',[(r'\x*(10-\x)',0,10)],(0,10),(-2,27),'Aire $A(x)=x(10-x)$ sur $[0;10]$.')
    figure('enclos',r'''\begin{tikzpicture}[x=.6cm,y=.6cm,font=\small]
\draw[otMuted,line width=3pt](-1,5)--(13,5);\node[above]at(6,5){Mur};
\draw[geoTrait](0,5)--node[left]{$x$}(0,0)--node[below]{$24-2x$}(12,0)--node[right]{$x$}(12,5);\end{tikzpicture}''','Trois côtés sont clôturés. Le schéma indique les expressions, sans imposer les dimensions optimales.')
    geo('distance-minimale',[('O',0,0),('A',2,3)],solpoints=[('H',2,0)],solsegments=[('A','H')],extra=r'\geoEnonce{\draw[geoTrait](2,3)--(4,0);\node[below]at(4,0){$M$};}')
    # Vecteurs : les points inconnus sont ajoutés en vert uniquement dans la solution.
    geo('vect-01',[('A',1,2),('B',5,-1)],vectors=[('A','B')],extra=r'\geoSolution{\draw[geoReponse,-{Stealth[length=1.8mm]}](5,-1)--(1,2);}')
    geo('vect-02',[('O',0,0),('U',3,1),('V',-1,2)],vectors=[('O','U'),('O','V')],solpoints=[('S',2,3)],solsegments=[('U','S'),('V','S')],extra=r'\geoSolution{\draw[geoReponse,-{Stealth[length=1.8mm]}](0,0)--(2,3);}',caption=r'$\vec u=\vect{OU}$ et $\vec v=\vect{OV}$ ; au corrigé, $\vect{OS}$ représente leur somme.')
    geo('vect-03',[('O',0,0),('U',2,-1)],vectors=[('O','U')],solpoints=[('P',6,-3),('Q',-4,2)],extra=r'\geoSolution{\draw[geoReponse,-{Stealth[length=1.8mm]}](0,0)--(6,-3);\draw[geoReponse,-{Stealth[length=1.8mm]}](0,0)--(-4,2);}',caption=r'$\vec u=\vect{OU}$ ; au corrigé, $\vect{OP}=3\vec u$ et $\vect{OQ}=-2\vec u$.')
    geo('vect-04',[('A',-2,1)],solpoints=[('B',2,3)],extra=r'\geoSolution{\draw[geoReponse,-{Stealth[length=1.8mm]}](-2,1)--(2,3);}',caption='Le corrigé ajoute le point image et le déplacement de vecteur $(4;2)$.')
    geo('vect-05',[('O',0,0),('U',-3,4)],vectors=[('O','U')],solpoints=[('V',-6,8)],extra=r'\geoSolution{\draw[geoReponse,-{Stealth[length=1.8mm]}](0,0)--(-6,8);}',caption=r'$\vec u=\vect{OU}$ ; le corrigé ajoute $\vect{OV}=2\vec u$.')
    geo('vect-06',[('A',0,0),('B',2,1),('C',3,3),('D',1,4)],vectors=[('A','B'),('B','C'),('C','D')],extra=r'\geoSolution{\draw[geoReponse,-{Stealth[length=1.8mm]}](0,0)--(1,4);\draw[geoReponse,-{Stealth[length=1.8mm]}](3,3)--(2,1);}')
    geo('vect-07',[('O',0,0),('U',2,3),('V',6,9),('W',4,7)],vectors=[('O','U'),('O','V'),('O','W')])
    geo('vect-08',[('A',1,1),('B',3,4),('C',5,7)],segments=[('A','C')])
    geo('vect-09',[('A',0,1),('B',4,2),('C',5,5)],segments=[('A','B'),('B','C')],solpoints=[('D',1,4)],solsegments=[('A','D'),('D','C')])
    geo('vect-10',[('O',0,0),('U',2,1),('V',-1,3)],vectors=[('O','U'),('O','V')],solpoints=[('W',5,-1)],extra=r'\geoSolution{\draw[geoReponse,-{Stealth[length=1.8mm]}](0,0)--(5,-1);}',caption=r'Au corrigé, $\vect{OW}=2\vect{OU}-\vect{OV}$.')
    figure('vect-11',tableau(['Vecteur','Abscisse','Ordonnée'],[[r'$\vec u$','$m$','$2$'],[r'$\vec v$','$3$','$m-1$']]),'Les coordonnées dépendent du paramètre ; le déterminant décide de la colinéarité.')
    geo('vect-12',[('A',1,2),('B',5,4)],segments=[('A','B')],solpoints=[('M',7,5)],solsegments=[('B','M')],extra=r'\draw[otMuted,dotted](0,5)--(8,5);\node[above]at(4,5){$y=5$};')
    geo('vect-13',[('O',0,0),('U',1,1,'above left'),('V',1,-1),('W',4,2)],vectors=[('O','U'),('O','V'),('O','W')])
    geo('vect-14',[('A',0,0),('B',6,2),('C',2,6),('I',3,1,'below'),('J',1,3,'left')],segments=[('A','B'),('B','C'),('C','A'),('I','J')])
    geo('vect-15',[('A',1,1),('U',3,2),('V',0,3),('T',8,8)],vectors=[('A','U'),('A','V')],caption='$U$ et $V$ sont les extrémités des deux déplacements depuis $A$ ; $T(8;8)$ est la cible.')
    # Configurations repérées.
    geo('conf-01',[('A',-1,2),('B',3,5)],segments=[('A','B')],solpoints=[('H',3,2)],solsegments=[('A','H'),('H','B')])
    geo('conf-02',[('A',-2,5),('B',6,-1)],segments=[('A','B')],solpoints=[('I',2,2)])
    geo('conf-03',[('A',-1,4),('I',2,1)],segments=[('A','I')],solpoints=[('B',5,-2)],solsegments=[('I','B')])
    geo('conf-04',[('A',0,0,'below left'),('B',4,0,'below right'),('C',4,3)],segments=[('A','B'),('B','C'),('C','A')],extra=r'\geoSolution{\draw[geoReponse](3.7,0)--(3.7,.3)--(4,.3);}')
    geo('conf-05',[('A',-2,0,'below'),('B',4,0,'below'),('M',1,3)],segments=[('A','B')],solpoints=[('I',1,0,'below')],extra=r'\geoSolution{\draw[geoAide](1,-1)--(1,4);}')
    geo('conf-06',[('A',0,0,'below'),('B',4,0,'below'),('C',2,3)],segments=[('A','B'),('B','C'),('C','A')],solpoints=[('H',2,0,'below')],solsegments=[('C','H')])
    geo('conf-07',[('A',0,0,'below left'),('B',9,0),('C',0,12,'left'),('M',6,0,'below'),('N',0,8,'left')],segments=[('A','B'),('B','C'),('C','A'),('M','N')],caption=r'Configuration illustrative de Thalès : $(MN)\parallel(BC)$, $AB=9$, $AC=12$, $AM=6$.')
    figure('conf-08',r'\begin{tikzpicture}[x=.35cm,y=.35cm,font=\small]\draw[geoTrait](0,0)node[below]{$P$}--node[below]{$20\text{ m}$}(20,0)node[below]{$B$}--(20,14)node[above]{$S$}--cycle;\draw[otMuted](4,0)arc(0:35:4);\node at(6,1.7){$35^\circ$};\draw[geoTrait](19,0)--(19,1)--(20,1);\end{tikzpicture}','Tour verticale et terrain horizontal ; schéma de principe, sans échelle imposée.')
    figure('conf-09',r'''\begin{tikzpicture}[x=.66cm,y=.66cm,font=\scriptsize]
\draw[geoTrait](-3,0)--(0,8)--(3,0);\draw[geoTrait](0,0)ellipse(3 and .5);\draw[geoTrait](0,4)ellipse(1.5 and .25);
\draw[geoAide](0,0)--node[right]{$8$}(0,8);\draw[<->](-3,-.8)--node[below]{Diamètre $6$}(3,-.8);
\draw[geoTrait](7,0)--(11,0)--(12,1.5)--(8,1.5)--cycle;
\draw[geoTrait](7,0)--(9.5,5)--(11,0);\draw[geoTrait](12,1.5)--(9.5,5);
\draw[geoAide](9.5,5)--node[right]{$8$}(9.5,.75);\node[below]at(9.5,-.5){Base : $27\text{ cm}^2$};
\draw[geoTrait](16,3)circle(2.2);\draw[geoAide](16,3)ellipse(2.2 and .5);
\draw[geoTrait](16,3)--node[above]{$3$}(18.2,3);\node[below]at(16,.2){Boule};
\end{tikzpicture}''','Cône coupé à mi-hauteur, pyramide et boule ; schémas en perspective sans échelle commune. Longueurs en cm.')
    geo('conf-10',[('A',0,0),('B',4,1),('C',5,4),('D',1,3)],segments=[('A','B'),('B','C'),('C','D'),('D','A')],solpoints=[('O',2.5,2)],solsegments=[('A','C'),('B','D')])
    geo('conf-11',[('A',0,0,'below'),('B',4,2),('C',3,4),('D',-1,2,'left')],segments=[('A','B'),('B','C'),('C','D'),('D','A')],solsegments=[('A','C')],extra=r'\geoSolution{\draw[geoReponse](3.73167,1.86584)--(3.59751,2.13416)--(3.86584,2.26833);}')
    geo('conf-12',[('A',-1,0,'below'),('B',3,0,'below')],solpoints=[('C',1,2)],solsegments=[('A','C'),('B','C')],extra=r'\draw[otMuted,dotted](-2,2)--(4,2);\node[above]at(3,2){$y=2$};')
    geo('conf-13',[('A',0,0,'below left'),('B',4,0,'below'),('C',0,6,'left')],segments=[('A','B'),('B','C'),('C','A')],solpoints=[('O',2,3)],extra=r'\geoSolution{\draw[geoAide](2,-.5)--(2,6.5);\draw[geoAide](-.5,3)--(4.5,3);\draw[geoReponse](2,3)circle(3.6055513);}',frame=[(2-sqrt(13),3-sqrt(13)),(2+sqrt(13),3+sqrt(13))])
    geo('conf-14',[('O',0,0,'below left')],solpoints=[('M_1',-3,4),('M_2',3,4)],circles=[(0,0,5)],extra=r'\draw[geoTrait](-6,4)--(6,4);\node[above]at(4,4){$y=4$};')
    figure('conf-15',r'''\begin{tikzpicture}[x=.55cm,y=.55cm,font=\small]
\coordinate(A)at(0,0);\coordinate(B)at(8,0);\coordinate(C)at(11,2);\coordinate(D)at(3,2);
\foreach \P/\Q in {A/B,B/C,C/D,D/A}{\draw[geoTrait](\P)--(\Q);\draw[geoTrait]($(\P)+(0,5)$)--($(\Q)+(0,5)$);\draw[geoTrait](\P)--($(\P)+(0,5)$);}
\node[below]at(4,0){$8$};\node[right]at(10,1){$6$};\node[left]at(0,2.5){$5$};
\geoSolution{\draw[geoAide](A)--(C);\draw[geoReponse](A)--($(C)+(0,5)$);}\end{tikzpicture}''','Pavé droit en perspective ; les longueurs sont en centimètres. Diagonales ajoutées au corrigé.')
    # Droites.
    records=[
      ([('A',1,5),('B',2,6)],[(2,-1,3)],[],[]),
      ([('A',0,3),('B',-2,0)],[(3,-2,6)],[],[]),
      ([],[(1,0,-2)],[],[]),
      ([('A',0,-1),('B',3,5)],[(2,-1,-1)],[],[]),
      ([('A',1,3)],[],[('B',2,1)],[]),
      ([('A',2,1)],[],[('B',5,-1)],[]),
      ([('A',-1,4),('B',3,-2)],[(3,2,-5)],[],[]),
      ([],[(2,-1,-1),(2,-1,3)],[],[]),
      ([],[(2,-1,1),(-1,-1,7)],[('I',2,5)],[]),
      ([],[(1,0,2),(3,2,-8)],[('I',-2,7)],[]),
      ([],[(2,-1,5),(1,-1,11)],[('I',6,17)],[]),
      ([],[(0,-1,2),(1,-1,1),(3,-1,-1)],[('P',1,2)],[]),
      ([('A',-2,1),('B',2,3),('C',6,5)],[(1,-2,4)],[],[]),
      ([],[(1,2,-4),(1,2,-5)],[],[]),
      ([('A',0,4),('B',-2,0),('C',4,0)],[],[('I',1,0),('K',.5,2)],[('A','I')]),
    ]
    for i,(pts,ls,sp,ss) in enumerate(records,1):
        extras=''
        if i==3:pts=[('P',2,0),('Q',2,3)]
        if i==5:extras=r'\geoSolution{\draw[geoAide](-1,7)--(4,-3);}'
        if i==6:extras=r'\geoSolution{\draw[geoAide](-1,3)--(8,-3);}'
        if i==15:extras=r'\geoSolution{\draw[geoAide](-1,8)--(2,-4);}\draw[otMuted,dotted](-3,2)--(5,2);'
        # Donner un cadrage utile même quand les intersections seules sont inconnues.
        if not pts and i in [8,9,12,14]:pts=[('' if False else 'O',0,0)]
        if i==8:sp=sp+[('Q',3,5)]
        if i==12:sp=sp+[('Q',3,4)]
        if i==14:sp=sp+[('Q',4,0),('R',0,3)]
        geo(f'droite-{i:02d}',pts,lines=ls,solpoints=sp,solsegments=ss,extra=extras)
    # Statistiques et diagrammes.
    figure('proportions-emboitees',r'\begin{tikzpicture}[font=\small]\draw[geoTrait](0,0)rectangle(10,3);\node[above]at(5,3){Lycée : 800};\fill[otNavyTint](.3,.3)rectangle(6.5,2.4);\draw[geoTrait](.3,.3)rectangle(6.5,2.4);\node at(3.4,2){Option : $45\,\%$ du lycée};\fill[otGreenTint](.6,.6)rectangle(4.3,1.5);\node at(2.45,1.05){Théâtre : $40\,\%$ de l’option};\end{tikzpicture}','Ensembles emboîtés ; les aires du schéma ne sont pas proportionnelles aux effectifs.')
    figure('stats-barres',r'\begin{tikzpicture}[x=1cm,y=.7cm,font=\small]\draw[otMuted,->](0,0)--(9,0)node[right]{Valeur};\draw[otMuted,->](0,0)--(0,5)node[above]{Effectif};\foreach \x/\n in {2/1,4/3,6/4,8/2}{\draw[otNavy,line width=4pt](\x,0)--(\x,\n);\node[below]at(\x,0){$\x$};\node[above]at(\x,\n){$\n$};}\end{tikzpicture}','Diagramme en barres de la série d’effectifs.')
    figure('stats-secteur',r'''\begin{tikzpicture}[font=\small]
\fill[otNavyTint](0,0)--(2.2,0)arc(0:120:2.2)--cycle;\draw[geoTrait](0,0)circle(2.2);
\draw[geoTrait](0,0)--(2.2,0);\draw[geoTrait](0,0)--(120:2.2);\draw[otMuted](.6,0)arc(0:120:.6);\node at(60:1.2){$120^\circ$};
\node[below]at(0,-2.4){Cercle : 60 élèves};
\begin{scope}[shift={(6,0)}]
\fill[otGreenTint](0,0)--(2.2,0)arc(0:120:2.2)--cycle;\draw[geoTrait](-2.2,0)--(2.2,0)arc(0:180:2.2);
\draw[geoTrait](0,0)--(120:2.2);\draw[otMuted](.6,0)arc(0:120:.6);\node at(60:1.2){$120^\circ$};
\node[below]at(0,-2.4){Demi-cercle : 60 élèves};
\end{scope}\end{tikzpicture}''','Le même angle doit être rapporté à 360 ou à 180 degrés selon la représentation du total.')
    figure('stats-dispersion',r'\begin{tikzpicture}[x=1cm,y=1cm,font=\small]\draw[otMuted,->](0,0)--(8,0);\foreach \x in {1,...,7}{\node[below]at(\x,0){$\x$};}\node[left]at(0,.7){$A$};\node[left]at(0,1.5){$B$};\foreach \y in {.4,.65,.9,1.15}{\fill[otNavy](4,\y)circle(2pt);}\foreach \x in {1,3,5,7}{\fill[otGreenDark](\x,1.5)circle(2pt);}\end{tikzpicture}','Chaque point représente une observation ; les quatre points de $A$ sont empilés à l’abscisse 4.')
    figure('stats-nuage',r'''\begin{tikzpicture}[x=.18cm,y=.38cm,font=\small]
\foreach \x in {0,10,...,50}{\draw[otRule!70,line width=.25pt](\x,0)--(\x,10);}
\foreach \y in {0,2,...,10}{\draw[otRule!70,line width=.25pt](0,\y)--(50,\y);}
\draw[otMuted,->](0,0)--(54,0);\draw[otMuted,->](0,0)--(0,10.6);
\foreach \x in {10,20,...,50}{\node[below]at(\x,0){$\x$};}
\foreach \y in {2,4,...,10}{\node[left]at(0,\y){$\y$};}
\node[below left]at(0,0){$0$};\node[above right]at(0,10.6){Distance (km)};
\node[below]at(28,-.95){Durée (min)};
\foreach \x/\y in {10/2,20/3,20/5,30/6,40/7,50/9}{\fill[otNavy](\x,\y)circle(2.3pt);}
\end{tikzpicture}''','Six trajets : les points sont des observations distinctes, sans segment entre eux.')
    histogram('stats-histogramme',[0,10,20,30,40],[4,8,6,2])
    figure('stats-cumuls',r'''\begin{tikzpicture}[x=.23cm,y=4cm,font=\small]
\draw[otMuted,->](0,0)--(43,0)node[right]{min};\draw[otMuted,->](0,0)--(0,1.1)node[above]{Fréquence};
\foreach \x in {10,20,30,40}{\node[below]at(\x,0){$\x$};}\foreach \y/\s in {.2/20,.5/50,1/100}{\node[left]at(0,\y){$\s\,\%$};\draw[otRule](0,\y)--(40,\y);}
\draw[geoTrait](0,0)--(10,.2)--(20,.6)--(30,.9)--(40,1);
\geoSolution{\draw[geoAide](0,.5)--(17.5,.5)--(17.5,0);}\end{tikzpicture}''','Interpolation linéaire des fréquences cumulées sous l’hypothèse uniforme dans chaque classe.')
    figure('stats-boites',r'''\begin{tikzpicture}[x=.7cm,y=.9cm,font=\small]
\draw[otMuted,->](-1,0)--(13,0);\foreach \x in {0,2,...,12}{\node[below]at(\x,0){$\x$};}
\draw[geoTrait](0,1)--(4,1)(8,1)--(12,1);\draw[geoTrait](4,.65)rectangle(8,1.35);\draw[geoTrait](6,.65)--(6,1.35);\foreach \x in {0,12}{\draw[geoTrait](\x,.8)--(\x,1.2);}
\draw[geoReponse](2,2)--(5,2)(7,2)--(10,2);\draw[geoReponse](5,1.65)rectangle(7,2.35);\draw[geoReponse](6,1.65)--(6,2.35);\foreach \x in {2,10}{\draw[geoReponse](\x,1.8)--(\x,2.2);}
\node[left]at(-.5,1){$A$};\node[left]at(-.5,2){$B$};\end{tikzpicture}''','Boîtes suivant les cinq indicateurs donnés ; aucune information sur les moyennes n’est ajoutée.')
    figure('croise-venn',r'''\begin{tikzpicture}[font=\small]
\draw[geoTrait](-3,-1.6)rectangle(3,1.8);\draw[geoTrait](-.8,0)circle(1.25);\draw[geoTrait](.8,0)circle(1.25);\node at(-1.7,1.2){$A$};\node at(1.7,1.2){$C$};
\geoSolution{\node at(-1.3,0){24};\node at(0,0){36};\node at(1.3,0){24};\node at(2.4,-1){36};}\end{tikzpicture}''','Les quatre régions du diagramme correspondent aux quatre cases du tableau.')
    tree('proba-arbre-01',['0{,}4','0{,}6'],['0{,}7','0{,}3','0{,}2','0{,}8'])
    tree('proba-arbre-02',['0{,}3','0{,}7'],['0{,}8','0{,}2','0{,}4','0{,}6'],blank=True)
    tree('proba-remise',['3/5','2/5'],['3/5','2/5','3/5','2/5'],lab=('R_1','B_1','R_2','B_2'))
    tree('proba-sans-remise',['3/5','2/5'],['2/4','2/4','3/4','1/4'],lab=('R_1','B_1','R_2','B_2'))
    tree('proba-usine',['0{,}4','0{,}6'],['0{,}02','0{,}98','?','?'],lab=('A',r'\overline A','D',r'\overline D'),caption='Les branches non données restent marquées « ? » ; le calcul demandé utilise le chemin $A$ puis $D$ et la valeur globale fournie.')
    cells=[]
    for a in range(1,7):cells.append([str(a)]+[rf'\geoSolution{{\color{{otGreenDark}}}}{a+b}' for b in range(1,7)])
    figure('proba-des',tableau(['Dé 1 / Dé 2']+list(map(str,range(1,7))),cells),'Chaque case représente un couple ordonné ; son nombre est la somme des deux dés.')
    graph('courbe-longueur',[(r'\x*\x',0,1)],(0,1.1),(0,1.1),'La courbe $y=x^2$ et la ligne polygonale à deux segments.',sol=r'\draw[geoReponse](0,0)--(.5,.25)--(1,1);')
    figure('synthese-rectangle',r'\begin{tikzpicture}[x=.75cm,y=.75cm]\draw[geoTrait](0,0)rectangle(8,4);\node[below]at(4,0){$x$};\node[right]at(8,2){$14-x$};\end{tikzpicture}','Schéma de rectangle de périmètre 28 cm ; les dimensions dessinées ne préjugent pas de l’optimum.')
    geo('synthese-mediatrice',[('A',0,0,'below left'),('B',4,0,'below')],lines=[(1,-1,1)],solpoints=[('M',2,3)],extra=r'\geoSolution{\draw[geoAide](2,-1)--(2,4);}')
    # Approfondissements : constructions et codages.
    figure('defi-moyennes',r'\begin{tikzpicture}[x=.7cm,y=.7cm]\draw[geoTrait](0,0)rectangle(6,3);\node[below]at(3,0){$a$};\node[right]at(6,1.5){$b$};\node[above]at(3,3){$a+b$ fixé ou $ab$ fixé};\end{tikzpicture}','Le calcul compare les rectangles ; ce schéma ne fixe pas un rapport de côtés.')
    geo('defi-barycentres',[('A',0,0,'below'),('B',6,0,'below'),('C',0,6,'left')],segments=[('A','B'),('A','C')],solpoints=[('G_+',2,0,'above'),('G_-',-6,0,'above'),('G_3',1.5,3)])
    geo('defi-medianes',[('A',0,0,'below left'),('B',6,0,'below'),('C',0,6,'left')],segments=[('A','B'),('B','C'),('C','A')],solpoints=[('I',3,3),('J',0,3,'left'),('K',3,0,'below'),('G',2,2)],solsegments=[('A','I'),('B','J'),('C','K')])
    geo('defi-hauteurs',[('A',0,0,'below'),('B',6,0,'below'),('C',2,4),("A'",8,4),("B'",-4,4,'left'),("C'",4,-4,'below')],segments=[('A','B'),('B','C'),('C','A'),("A'","B'"),("B'","C'"),("C'","A'")],solpoints=[('H',2,2)],extra=r'''\geoSolution{
\draw[geoAide](0,0)--(3,3);\draw[geoAide](6,0)--(1.2,2.4);\draw[geoAide](2,4)--(2,0);
\draw[geoReponse](1.75,0)--(1.75,.25)--(2,.25);
\draw[geoReponse](3.14142,2.85858)--(3,2.71716)--(2.85858,2.85858);
\draw[geoReponse](1.28944,2.57889)--(1.46833,2.48945)--(1.37889,2.31056);
}''',caption='Les hauteurs du petit triangle sont les médiatrices du grand ; leurs angles droits sont codés au corrigé.')
    figure('defi-aire-angle',r'''\begin{tikzpicture}[x=.7cm,y=.7cm,font=\small]
\draw[geoTrait](0,0)node[below]{$C$}--node[below]{$a$}(7,0)node[below]{$B$}--(3,4)node[above]{$A$}--node[left]{$b$}cycle;
\draw[geoAide](3,4)--node[right]{$h$}(3,0)node[below]{$H$};\draw[geoReponse](2.7,0)--(2.7,.3)--(3,.3);\draw[otMuted](1,0)arc(0:53.13:1);\node at(1.3,.6){$C$};\end{tikzpicture}''','Une hauteur donne la formule de l’aire ; schéma d’un angle aigu, sans échelle imposée.')
    geo('defi-circonscrit',[('A',0,0,'below'),('B',6,0,'below'),('C',2,4)],segments=[('A','B'),('B','C'),('C','A')],solpoints=[('O',3,1)],extra=r'\geoSolution{\draw[geoReponse](3,1)circle(3.16227766);\draw[geoAide](3,-3)--(3,5);\draw[geoAide](-1,3)--(5,0);\draw[geoReponse](3.25,0)--(3.25,.25)--(3,.25);\draw[geoReponse](1.1,2.2)--(1.3,2.1)--(1.2,1.9);}',frame=[(3-sqrt(10),1-sqrt(10)),(3+sqrt(10),1+sqrt(10))])
    graph('defi-parabole',[(r'1+\x*\x/4',-4.5,4.5)],(-5,5),(-.5,7),'Lieu équidistant de $F(0;2)$ et de l’axe horizontal.',points=[('F',0,2)],sol=r'\draw[geoAide](4,5)--(4,0);\draw[geoAide](4,5)--(0,2);\fill[otGreenDark](4,5)circle(2pt);')
    graph('defi-region',[(r'8-\x',0,9),(r'6-\x/2',0,9)],(0,9),(0,9),'Frontières $x+y=8$ (bleu), $x+2y=12$ (vert) dans le quadrant positif.',sol=r'\fill[otGreen,opacity=.16](0,0)--(8,0)--(4,4)--(0,6)--cycle;\fill[otGreenDark](4,4)circle(2pt);')
    graph('defi-racine-carre',[(r'\x*\x',0,2.2),(r'sqrt(\x)',0,4.4),(r'\x',0,4.4)],(0,4.4),(0,4.4),r'Carré en bleu ; racine et droite $y=x$ en vert. La branche du carré est restreinte à $x\ge0$.')
    tree('defi-test',['p','1-p'],['0{,}9','0{,}1','0{,}05','0{,}95'],lab=('D',r'\overline D','+', '-'))
    graph('bilan-A-aire',[(r'\x*(6-\x)',0,6)],(0,6),(-1,10),'Aire en fonction de $x$ ; le corrigé repère le maximum.',sol=r'\fill[otGreenDark](3,9)circle(2pt);\draw[geoAide](3,9)--(3,0);')
    geo('bilan-A-geometrie',[('A',0,0,'below left'),('B',8,0,'below'),('C',2,6)],segments=[('A','B'),('B','C'),('C','A')],solpoints=[('I',5,3),('J',1,3,'left'),('G',10/3,2)],solsegments=[('A','I'),('B','J')])
    tree('bilan-A-arbre',['0{,}4','0{,}6'],['0{,}6','0{,}4','0{,}3','0{,}7'],lab=('A','B','S',r'\overline S'),blank=True)
    histogram('bilan-B-stats',[0,10,20,30],[4,8,8])
    geo('bilan-B-geometrie',[('A',1,1,'below left'),('B',5,1,'below right'),('C',1,4,'above left'),('D',5,4)],segments=[('A','B'),('B','D'),('D','C'),('C','A')],solpoints=[('O',3,2.5)],extra=r'\geoSolution{\draw[geoReponse](3,2.5)circle(2.5);\draw[geoAide](3,0)--(3,5);\draw[geoAide](0,2.5)--(6,2.5);}')
    tree('bilan-B-arbre',['4/5','1/5'],['3/4','1/4','1','0'],lab=('R_1','B_1','R_2','B_2'),blank=True)

def histogram(name,bounds,counts):
    tex=r'\begin{tikzpicture}[x=.25cm,y=.45cm,font=\small]'
    tex+=rf'\draw[otMuted,->](0,0)--({bounds[-1]+4},0)node[right]{{min}};\draw[otMuted,->](0,0)--(0,{max(counts)+2})node[above]{{Effectif}};'
    for a,b,n in zip(bounds,bounds[1:],counts):tex+=rf'\filldraw[fill=otNavyTint,draw=otNavy]({a},0)rectangle({b},{n});\node[above]at({(a+b)/2},{n}){{{n}}};'
    for a in bounds:tex+=rf'\node[below]at({a},0){{{a}}};'
    return figure(name,tex+r'\end{tikzpicture}','Classes de même amplitude ; la hauteur de chaque rectangle est ici l’effectif de sa classe.')

def enrichir_variations():
    figure('variations-lecture',r'''\begin{tableau}
\otTab[3]{$x$/0.7,$f(x)$/1.5}{$0$,$2$,$6$}
\tkzTabVar{-/$1$,+/$5$,-/$-3$}
\end{tableau}''','Les flèches décrivent les variations sur tout l’intervalle, sans fixer les images intermédiaires.')
    for nom,bornes,variations in [
        ('variation-decalee',r'{$0$,$3$,$7$}',r'{+/$7$,-/$-2$,+/$14$}'),
        ('aire-produit',r'{$0$,$5$,$10$}',r'{-/$0$,+/$25$,-/$0$}')]:
        fonction='A(x)' if nom=='aire-produit' else 'f(x)'
        FIGURES[nom]['tex']+=r'\geoSolution{\par\medskip\begin{tableau}\otTab[3]{$x$/0.7,$'+fonction+r'$/1.5}'+bornes+r'\tkzTabVar'+variations+r'\end{tableau}}'
        FIGURES[nom]['legende']+=' Le corrigé associe la courbe à son tableau de variations.'

def write_all(root):
    build()
    enrichir_variations()
    for name,data in FIGURES.items():
        assert not any(ord(c)<32 and c not in '\n\r\t' for c in data['tex']),name
        text=data['tex']+'\n\\par\\legende{'+data['legende']+'}\n'
        (root/'figures'/f'{name}.tex').write_text(text,encoding='utf-8')
    return FIGURES
