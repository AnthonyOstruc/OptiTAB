from math import ceil,floor,sqrt,sin,cos,tan,radians
from modele import figure

def dessin(nom,tex,legende='Schéma de principe sans échelle imposée ; seules les données écrites font foi.'):
    figure(nom,r'\begin{tikzpicture}[font=\small,line cap=round,line join=round]'+tex+r'\end{tikzpicture}',legende)

def axes(xb,yb,xt=1,yt=1,xlabel='$x$',ylabel='$y$',ortho=False):
    xmin,xmax=xb;ymin,ymax=yb;sx=9/(xmax-xmin);sy=4/(ymax-ymin)
    if ortho:sx=sy=min(sx,sy)
    tex=rf'\begin{{scope}}[x={sx}cm,y={sy}cm]'
    for j in range(ceil(xmin/xt),floor(xmax/xt)+1):
        a=j*xt;tex+=rf'\draw[otRule!65,line width=.2pt]({a},{ymin})--({a},{ymax});'
        if a:tex+=rf'\node[below,font=\tiny,fill=white,inner sep=.5pt]at({a},0){{{a}}};'
    for j in range(ceil(ymin/yt),floor(ymax/yt)+1):
        a=j*yt;tex+=rf'\draw[otRule!65,line width=.2pt]({xmin},{a})--({xmax},{a});'
        if a:tex+=rf'\node[left,font=\tiny,fill=white,inner sep=.5pt]at(0,{a}){{{a}}};'
    tex+=rf'\draw[otMuted,->]({xmin},0)--({xmax+.15/sx},0)node[right]{{{xlabel}}};\draw[otMuted,->](0,{ymin})--(0,{ymax+.2/sy})node[above]{{{ylabel}}};\node[below left,font=\tiny]at(0,0){{0}};'
    return tex

def graph(nom,curves,xb,yb,xt=1,yt=1,caption='',points=(),sol='',poly='',blank=False,xlabel='$x$',ylabel='$y$',ortho=False):
    tex=axes(xb,yb,xt,yt,xlabel,ylabel,ortho)+rf'\begin{{scope}}\clip({xb[0]},{yb[0]})rectangle({xb[1]},{yb[1]});'
    for i,(expr,lo,hi) in enumerate(curves):
        draw=rf'\draw[{"otNavy" if i==0 else "otGreenDark"},line width=1pt]plot[domain={lo}:{hi},samples=90](\x,{{{expr}}});'
        tex+=r'\geoSolution{'+draw+'}' if blank else draw
    tex+=poly
    for lab,x,y in points:tex+=rf'\fill[otNavy]({x},{y})circle(1.7pt)node[above right,geoLabel]{{$ {lab} $}};'
    dessin(nom,tex+r'\geoSolution{'+sol+r'}\end{scope}\end{scope}',caption+(' Repère orthonormé.' if ortho else ' Les axes sont gradués ; leurs échelles peuvent différer.'))

def pave(nom,L='8 cm',D='5 cm',H='3 cm',extra=''):
    tex=r'''\coordinate(A)at(0,0);\coordinate(B)at(5,0);\coordinate(C)at(6.3,1.2);\coordinate(D)at(1.3,1.2);
\coordinate(E)at(0,2.6);\coordinate(F)at(5,2.6);\coordinate(G)at(6.3,3.8);\coordinate(H)at(1.3,3.8);
\draw[geoTrait](A)--(B)--(C)--(G)--(H)--(E)--cycle (E)--(F)--(G) (B)--(F);
\draw[otMuted,dashed](A)--(D)--(C) (D)--(H);'''
    tex+=rf'\path(A)--node[below]{{{L}}}(B);\path(B)--node[below right]{{{D}}}(C);\path(A)--node[left]{{{H}}}(E);'
    dessin(nom,tex+extra,'Perspective cavalière ; les arêtes cachées sont en pointillés.')

def cylindre(nom,r='3 cm',h='10 cm',extra=''):
    tex=r'''\draw[geoTrait](-1.5,0)--(-1.5,3) (1.5,0)--(1.5,3);
\draw[geoTrait](0,3)ellipse(1.5 and .42);\draw[geoTrait](-1.5,0)arc(180:360:1.5 and .42);
\draw[otMuted,dashed](-1.5,0)arc(180:0:1.5 and .42);'''
    tex+=rf'\draw[otMuted,<->](1.9,0)--node[right]{{{h}}}(1.9,3);'
    if r.startswith('base'):
        tex+=rf'\node at(0,.8){{{r}}};'
    else:
        # Étiquette sur fond blanc : elle ne doit pas être barrée par le bord de l'ellipse.
        tex+=rf'\draw[geoTrait](0,3)--node[above,geoLabel,inner sep=.6pt]{{{r}}}(1.5,3);'
    dessin(nom,tex+extra,'Cylindre en perspective ; les dimensions de l’énoncé fixent le modèle.')

def cone(nom,r='4 cm',h='9 cm',cut=False):
    tex=r'\draw[geoTrait](-2,0)--(0,3.5)--(2,0);\draw[geoTrait](-2,0)arc(180:360:2 and .5);\draw[otMuted,dashed](-2,0)arc(180:0:2 and .5) (0,0)--(0,3.5);'
    tex+=rf'\draw[otMuted,<->](2.5,0)--node[right]{{{h}}}(2.5,3.5);\draw[geoTrait](0,0)--node[below]{{{r}}}(2,0);'
    if cut:tex+=r'\draw[otGreenDark](0,1.75)ellipse(1 and .25);\node[left]at(-1.2,1.8){mi-hauteur};'
    dessin(nom,tex,'Cône en perspective ; la hauteur est perpendiculaire à la base.')

def pile(lines,x=0,width=7.6):
    tex='';colors={'calcul':'otOrange!25','controle':'otOrange!38','entree':'otNavy!14','mouvement':'otNavy!24','evenement':'otGreen!28'}
    for i,(dep,txt,kind) in enumerate(lines):
        txt=txt.replace('×',r'$\times$')
        tex+=rf'\node[anchor=north west,rounded corners=1mm,draw=white,fill={colors[kind]},inner xsep=2mm,inner ysep=1.3mm,font=\scriptsize,text width={width-dep*.3}cm]at({x+dep*.3},{-i*.55}){{{txt}}};'
    return tex
