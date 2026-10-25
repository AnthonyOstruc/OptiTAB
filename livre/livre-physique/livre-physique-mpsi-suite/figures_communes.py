"""Figures originales ; orientations explicites et courbes calculées."""
from math import sqrt,pi,exp,cos,sin

def common(ch):
    ch.f('conventions',r'''
\draw (0,0) to[R,l=$R$] (4,0);\draw[-{Stealth},otNavy,thick](.3,.65)--(1.4,.65)node[midway,above]{$i$};
\draw[-{Stealth},otGreenDark,thick](3,-.65)--(1,-.65)node[midway,below]{$u=V_A-V_B$};
\node[lab,left]at(0,0){$A$};\node[lab,right]at(4,0){$B$};
\node[lab]at(2,1.5){Convention récepteur : $p_{\rm reçue}=ui$};
\draw (7,0) to[V,l=$E$] (11,0);\draw[-{Stealth},otNavy,thick](7.3,.65)--(8.4,.65)node[midway,above]{$i$};
\draw[-{Stealth},otGreenDark,thick](8,-.65)--(10,-.65)node[midway,below]{$u$};
\node[lab]at(9,1.5){Générateur : $p_{\rm fournie}=ui$};
''')
    ch.f('thevenin',r'''
\draw (0,0) to[V] (0,3) to[R,l=$r$] (5,3) to[R,l=$R$] (5,0)--(0,0);
\draw[-{Stealth},otGreenDark,thick](-.8,.3)--(-.8,2.7)node[midway,left]{$E$};
\draw[-{Stealth},otNavy,thick](2,3.6)--(3.4,3.6)node[midway,above]{$i$};
\draw[-{Stealth},otGreenDark,thick](6,.3)--(6,2.7)node[midway,right]{$u$};
\node[lab,text width=4.5cm,align=left]at(10,1.5){Source réelle : $u=E-ri$.\\La résistance $r$ appartient à la source ; $R$ est la charge.};
''')
    ch.f('diviseur',r'''
\draw (0,0) to[V] (0,4)--(3,4) to[R,l=$R_1$] (3,2) to[R,l=$R_2$] (3,0)--(0,0);
\draw[-{Stealth},otGreenDark,thick](-.8,.3)--(-.8,3.7)node[midway,left]{$E$};
\fill[otNavy](3,2)circle(2pt)node[left=3mm]{$A$};\draw(3,2)--(7,2)to[R,l=$R_e$](7,0)--(3,0);
\draw[-{Stealth},otGreenDark,thick](8,.2)--(8,1.8)node[midway,right]{$u$};
\node[lab,text width=3cm,align=left]at(10,3.2){À vide : retirer $R_e$.\\En charge : $R_2$ et $R_e$ sont en parallèle.};
''')
    ch.f('noeud',r'''
\fill[otNavy](5,2)circle(3pt);\draw[-{Stealth},otNavy,thick](0,2)--(4.8,2)node[midway,above]{$i_1$};
\draw[-{Stealth},otNavy,thick](5,5)--(5,2.2)node[midway,right]{$i_2$};
\draw[-{Stealth},otGreenDark,thick](5.2,2)--(10,2)node[midway,above]{$i_3$};
\draw[-{Stealth},otGreenDark,thick](5,1.8)--(5,-.5)node[midway,right]{$i_4$};
\node[lab]at(9,4){$i_1+i_2=i_3+i_4$};
''')
    for kind,device,label in [('rc','C','C'),('rl','L','L'),('lc','C','C'),('rlc','C','C')]:
        top=r'to[L,l=$L$]' if kind=='lc' else r'to[R,l=$R$]'
        left=r'to[short]' if kind in ['lc','rlc'] else r'to[V]'
        body=rf'\draw (0,0) {left} (0,3) {top} (4,3)'
        if kind=='rlc':body+=r' to[L,l=$L$] (8,3)';x=8
        else:x=4
        body+=rf' to[{device},l=${label}$] ({x},0)--(0,0);'
        body+=rf'\draw[-{{Stealth}},otNavy,thick](1,3.6)--(2.5,3.6)node[midway,above]{{$i$}};\draw[-{{Stealth}},otGreenDark,thick]({x+1},.2)--({x+1},2.8)node[midway,right]{{$u_{label}$}};'
        if kind in ['rc','rl']:body+=r'\draw[-{Stealth},otGreenDark,thick](-.8,.3)--(-.8,2.7)node[midway,left]{$e(t)$};'
        if kind=='lc':body+=r'\node[lab,text width=4.5cm,align=left]at(9,1.5){$i=C\dot u_C$\\$u_L+u_C=0$\\Circuit fermé, sans source.};'
        ch.f(kind,body)
    ch.f('rc-parallele',r'''
\draw (0,0)to[V](0,4)--(3,4)to[R,l=$R_1$](3,2)to[R,l=$R_2$](3,0)--(0,0);
\draw(3,2)--(7,2)to[C,l=$C$](7,0)--(3,0);\fill[otNavy](3,2)circle(2pt)node[left=3mm]{$A$};
\draw[-{Stealth},otGreenDark,thick](-.8,.3)--(-.8,3.7)node[midway,left]{$E$};
\draw[-{Stealth},otGreenDark,thick](8,.2)--(8,1.8)node[midway,right]{$u$};
\node[lab,text width=3cm,align=left]at(10,3.2){Au nœud A :\\$i_1=i_2+i_C$.};
''')
    ch.f('ressort',r'''
\fill[pattern=north east lines,pattern color=otMuted](-.3,-.7)rectangle(0,1.7);\draw[thick](0,-.7)--(0,1.7);
\draw[decorate,decoration={coil,aspect=.5,segment length=4mm,amplitude=3mm},thick,otNavy](0,.5)--(5,.5);
\draw[fill=otNavyTint](5,-.1)rectangle(6.4,1.1);\node at(5.7,.5){$m$};
\draw[otMuted](-.2,-.3)--(8,-.3);\draw[axis](3,-1.2)--(9,-1.2)node[right]{$x$};
\draw[dashed,otMuted](4.5,-.5)--(4.5,-1.5);\node[lab,below]at(4.5,-1.5){Équilibre $x=0$};
\draw[-{Stealth},otGreenDark,thick](5.5,1.6)--(3.8,1.6)node[midway,above]{$F_x=-kx$ pour $x>0$};
''')

def plot(ch,name,curves,xmax=6,ymin=-1.2,ymax=1.2,xlabel=r'$t/\tau$',ylabel='$s$',extra=''):
    body=rf'''\begin{{axis}}[width=13.4cm,height=5.8cm,xmin=0,xmax={xmax},ymin={ymin},ymax={ymax},xlabel={{{xlabel}}},ylabel={{{ylabel}}},axis lines=left,grid=major,grid style={{otRule!60}},tick label style={{font=\small}},label style={{font=\small}},legend columns=2,legend style={{font=\small,draw=none,at={{(.5,1.04)}},anchor=south,column sep=3mm}}]
'''
    for formula,label,color in curves:
        body+=rf'\addplot[{color},thick,domain=0:{xmax},samples=220] {{{formula}}};\addlegendentry{{{label}}}'+'\n'
    body+=extra+'\n\\end{axis}'
    ch.f(name,body)
