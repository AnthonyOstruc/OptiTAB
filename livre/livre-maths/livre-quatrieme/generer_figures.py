"""Figures vectorielles originales ; les réponses sont ajoutées au corrigé."""
from pathlib import Path
from math import sqrt,sin,cos,radians,atan2,degrees,acos
from modele import FIGURES,figure,tableau
from outils_figures import dessin,axes,graph,pave,cylindre,cone,pile
from donnees_scripts import SCRIPTS
GEOMETRIE={};SECTEURS={}

def reponse(txt):
    return r'\geoEnonce{?}\geoSolution{\textcolor{otGreenDark}{'+txt+'}}'

def polygone(pts,color='otNavy'):
    return r'\draw['+color+',line width=.85pt]'+'--'.join(f'({x},{y})' for x,y in pts)+'--cycle;'

def triangle_tex(ab,ac,bc=None,angle=None,labels=None,right=False,proof_right=False,names='ABC',shift=0,scale_override=None):
    if angle is not None:cx=ac*cos(radians(angle));cy=ac*sin(radians(angle));bc=sqrt((ab-cx)**2+cy**2)
    elif right:cx=0.;cy=ac;bc=sqrt(ab*ab+ac*ac)
    else:
        assert bc is not None
        cx=(ab*ab+ac*ac-bc*bc)/(2*ab);cy=sqrt(max(0,ac*ac-cx*cx))
    pts=[(0,0),(ab,0),(cx,cy)]
    scale=min(6.4/max(ab,cx,1),3.0/max(cy,.1))
    if shift:scale=min(scale,.62)
    if scale_override is not None:scale=scale_override
    p=[(shift+x*scale,y*scale) for x,y in pts]
    tex=polygone(p)
    for i,((x,y),name) in enumerate(zip(p,names)):
        anchor=['below left','below right','above'][i]
        tex+=rf'\fill[otNavy]({x},{y})circle(1.3pt)node[{anchor},geoLabel]{{$ {name} $}};'
    center=(sum(x for x,y in p)/3,sum(y for x,y in p)/3)
    for (i,j),txt in (labels or {}).items():
        a,b=p[i],p[j];mx=(a[0]+b[0])/2;my=(a[1]+b[1])/2
        dx=b[0]-a[0];dy=b[1]-a[1];norm=sqrt(dx*dx+dy*dy);nx=-dy/norm;ny=dx/norm
        if nx*(mx-center[0])+ny*(my-center[1])<0:nx=-nx;ny=-ny
        tex+=rf'\node[geoLabel,font=\scriptsize]at({mx+nx*.31},{my+ny*.31}){{{txt}}};'
    if right or proof_right:
        mark=rf'\draw[{"otGreenDark" if proof_right else "otMuted"}]({shift+.16},0)--({shift+.16},.16)--({shift},.16);'
        tex+=r'\geoSolution{'+mark+'}' if proof_right else mark
    return tex,pts,(ab,ac,bc)

def triangle(nom,ab,ac,bc=None,angle=None,labels=None,right=False,proof_right=False,extra=''):
    tex,pts,lengths=triangle_tex(ab,ac,bc,angle,labels,right,proof_right)
    GEOMETRIE[nom]={'points':pts,'longueurs':lengths,'rectangle':right or proof_right}
    dessin(nom,tex+extra)

def carre(nom,side='?',inside='',opening=False):
    t=r'\draw[geoTrait](0,0)rectangle(3,3);'
    t+=rf'\node[below]at(1.5,0){{{side}}};\node[align=center]at(1.5,1.5){{{inside}}};'
    if opening:t+=r'\draw[white,line width=2pt](.8,0)--(1.5,0);\draw[otMuted,|<->|](.8,-.55)--node[below]{2 m}(1.5,-.55);'
    dessin(nom,t)

def rectangles(nom,L,H,extra='',answer='',second=None):
    tex=r'\draw[geoTrait](0,0)rectangle(5,2.5);'+rf'\node[below]at(2.5,0){{{L}}};\node[left]at(0,1.25){{{H}}};'+extra
    if answer:tex+=r'\geoSolution{'+rf'\node[text=otGreenDark]at(2.5,1.25){{{answer}}};'+'}'
    dessin(nom,tex)

def secteurs(nom,angles,labels,blank=False):
    assert abs(sum(angles)-360)<1e-8
    SECTEURS[nom]=angles
    colors=['otGreen!65','otNavy!45','otOrange!65','otGreen!25','otNavy!15']
    t='';start=0
    for i,(a,lab) in enumerate(zip(angles,labels)):
        end=start+a;mid=(start+end)/2
        part=rf'\filldraw[draw=white,line width=1pt,fill={colors[i%len(colors)]}](0,0)--({start}:1.55)arc({start}:{end}:1.55)--cycle;\node[font=\scriptsize,align=center]at({mid}:1.05){{{lab}}};'
        t+=r'\geoSolution{'+part+'}' if blank else part;start=end
    if blank:t+=r'\geoEnonce{\draw[geoTrait](0,0)circle(1.55);\node at(0,0){À construire};}'
    dessin(nom,t,'Les angles des secteurs représentent leurs parts respectives du total.')

def urs(nom,items):
    tex=r'\draw[otMuted,line width=.8pt](-.6,2.1)--(-.6,-.6)--(5,-.6)--(5,2.1);'
    colors={'R':'otOrange!70','B':'otNavy!40','V':'otGreen!60'}
    for i,l in enumerate(items):
        x=(i%4)*1.3;y=1.3-(i//4)*1.3
        tex+=rf'\node[circle,draw=otMuted,fill={colors[l[0]]},minimum size=8mm,font=\small]at({x},{y}){{{l}}};'
    dessin(nom,tex,'Les objets sont supposés indiscernables au toucher ; les lettres identifient leur couleur.')

def nombres_modeles():
    for name,area,sol in [('carre-121',121,'11 cm'),('carre-18',18,r'$\sqrt{18}$ m'),('jardin-72',72,r'$\sqrt{72}$ m'),('carre-45',45,r'$\sqrt{45}$ cm'),('plaque-50',50,r'$\sqrt{50}$ cm')]:
        unit='m' if name in ['carre-18','jardin-72'] else 'cm'
        carre(name,reponse(sol),f'Aire : {area} {unit}$^2$',opening=name=='jardin-72')
    carre('carre-4','$c$','')
    for name in ['cours-distributivite','aire-distrib']:
        rectangles(name,'$x+3$ cm','4 cm',r'\draw[otMuted,dashed](3,0)--(3,2.5);\node at(1.5,1.25){$4x$};\node at(4,1.25){12};\node[above]at(1.5,2.5){$x$};\node[above]at(4,2.5){3};')
    FIGURES['aire-distrib']['tex']=FIGURES['aire-distrib']['tex'].replace(r'\node at(1.5,1.25){$4x$};\node at(4,1.25){12};',r'\geoSolution{\node[text=otGreenDark]at(1.5,1.25){$4x$};\node[text=otGreenDark]at(4,1.25){12};}')
    rectangles('rectangle-litteral','$2x+1$ cm','$x+3$ cm')
    rectangles('eq-rectangle','$x+5$ cm','$x$ cm',answer='$7$ cm sur $12$ cm')
    dessin('eq-deux-figures',r'\draw[geoTrait](0,0)rectangle(2.6,2.6);\node[below]at(1.3,0){$x$};\draw[geoTrait](4,0)--(7.2,0)--(5.6,2.771)--cycle;\node[below]at(5.6,0){$x+2$};')
    dessin('cours-equilibre',r'\draw[geoTrait](0,1.6)--(6,1.6) (3,1.6)--(3,0) (2,0)--(4,0);\node[draw=otMuted,fill=otGreenTint,minimum width=2cm]at(1,2.1){$3x+5$};\node[draw=otMuted,fill=otGreenTint,minimum width=2cm]at(5,2.1){17};\node at(3,2.4){$=$};','Une même opération sur les deux membres conserve l’équilibre de l’égalité.')
    graph('proportion-prix',[('2.5*\\x',0,4)],(0,4),(0,10),1,2.5,xlabel='kg',ylabel='euros',caption='Prix proportionnel à la masse.')
    graph('cours-location',[('6+2*\\x',0,4)],(0,4),(0,14),1,2,xlabel='h',ylabel='euros')
    graph('graph-non-proportion',[('2+2*\\x',0,4)],(0,4),(0,10),1,2)
    graph('graph-corde',[('1.5*\\x',0,6)],(0,6),(0,9),1,1.5,blank=True,xlabel='m',ylabel='euros')
    graph('graph-carre',[('\\x*\\x',0,4)],(0,4),(0,16),1,4,xlabel='cm',ylabel='cm$^2$')
    graph('four',[],(0,12),(0,120),2,20,xlabel='min',ylabel=r'$^\circ$C',poly=r'\draw[geoTrait](0,20)--(4,100)--(6,100)--(12,40);',caption='Les segments du modèle relient les températures indiquées.')
    graph('graph-tarifs',[('4+2*\\x',0,4),('4*\\x',0,4)],(0,4),(0,16),1,4,xlabel='h',ylabel='euros',sol=r'\fill[otGreenDark](2,8)circle(2pt);',caption='A : tracé bleu ; B : tracé vert.')
    graph('graph-reserve',[('120-8*\\x',0,15)],(0,15),(0,120),3,20,xlabel='min',ylabel='L')
    figure('tableur-prix',tableau(['Ligne','A : durée','B : prix'],[['2','0',r'\texttt{=5+3*A2}'],['3','2',r'\geoEnonce{à recopier}\geoSolution{11}'],['4','4',r'\geoEnonce{à recopier}\geoSolution{17}']]),'Recopier la formule de B2 vers B3 et B4.')
    rectangles('coins-retires','18 cm','10 cm',r'\foreach\x in{0,4}{\foreach\y in{0,1.5}{\filldraw[draw=otNavy,fill=otGreen!25](\x,\y)rectangle++(1,1);}}\node at(2.5,1.25){aire restante};\node[above]at(.5,2.5){$x$};')
    t=r'\draw[geoTrait](0,0)circle(1.6);\draw[geoTrait](0,0)--(1.6,0)node[midway,below]{6 cm};\draw[otGreenDark,line width=2pt](1.6,0)arc(0:75:1.6);\draw[otMuted](0,0)--(75:1.6);\draw[otMuted](.55,0)arc(0:75:.55)node[midway,right]{$75^\circ$};'
    dessin('arc-75',t)
    # Arbre de facteurs : représentation d’un produit, sans calcul de probabilités à deux étapes.
    dessin('facteurs-180',r'\node(a)at(0,2){180};\node(b)at(-1,1){18};\node(c)at(1,1){10};\node(d)at(-1.7,0){2};\node(e)at(-.5,0){9};\node(f)at(.5,0){2};\node(g)at(1.5,0){5};\node(h)at(-1,-1){3};\node(i)at(0,-1){3};\draw[otMuted](a)--(b)(a)--(c)(b)--(d)(b)--(e)(c)--(f)(c)--(g)(e)--(h)(e)--(i);','Chaque nœud se décompose en un produit ; les feuilles sont des nombres premiers.')
    for pos,val in [('(-1.7,0)',2),('(-.5,0)',9),('(.5,0)',2),('(1.5,0)',5),('(-1,-1)',3),('(0,-1)',3)]:
        FIGURES['facteurs-180']['tex']=FIGURES['facteurs-180']['tex'].replace('at'+pos+'{'+str(val)+'}', 'at'+pos+'{'+reponse(str(val))+'}')

def statistiques_hasard():
    secteurs('cours-camembert',[180,108,72],['50\\,\\%','30\\,\\%','20\\,\\%'])
    secteurs('stat-sports',[180,108,72],['Football','Basket','Tennis'],True)
    secteurs('stat-secteur-a',[144,216],['A : $144^\\circ$','Autres'])
    poly=''.join(rf'\draw[otNavy,line width=2pt]({i},0)--({i},{v});\node[above,font=\scriptsize]at({i},{v}){{{v}}};' for i,v in enumerate([2,4,3,2,1]))
    graph('stat-livres',[],(-.5,4.5),(0,5),1,1,xlabel='livres',ylabel='élèves',poly=poly)
    urs('cours-urne',['R','R','R','B','B']);urs('urne-431',['R']*4+['B']*3+['V']);urs('jetons-numerotes',['R1','R2','R3','B1','B2','V1'])
    secteurs('roue-8',[45]*8,[str(i) for i in range(1,9)])
    secteurs('roue-inegale',[90,120,150],['$90^\\circ$','$120^\\circ$','$150^\\circ$'])
    dessin('cible-carree',r'\draw[geoTrait](0,0)rectangle(3.5,3.5);\filldraw[fill=otGreen!35,draw=otNavy](1,1)rectangle(2.4,2.4);\node[below]at(1.75,0){10 cm};\node at(1.7,1.7){4 cm};')
    dessin('cible-couronne',r'\filldraw[fill=otGreen!30,draw=otNavy](0,0)circle(1.8);\filldraw[fill=white,draw=otNavy](0,0)circle(.9);\draw[geoTrait](0,0)--node[above]{6 cm}(1.8,0);\draw[otMuted](0,0)--node[left]{3 cm}(0,.9);')

def triangles_egaux():
    triangle('tri-01',6,5,4,labels={(0,1):'6 cm',(0,2):'5 cm',(1,2):'4 cm'})
    dessin('tri-02',r'\draw[geoTrait](0,0)--(6,0);\node[below]at(0,0){A};\node[below]at(6,0){B};\node[below]at(3,0){6 cm};\draw[otMuted,dashed](0,0)circle(2);\draw[otMuted,dashed](6,0)circle(3);','Cercles de rayons 2 et 3 autour des extrémités : ils ne se coupent pas.')
    triangle('tri-03',5,4,angle=60,labels={(0,1):'5 cm',(0,2):'4 cm'},extra=r'\node at(.8,.45){$60^\circ$};')
    ac=6*sin(radians(60))/sin(radians(70))
    triangle('tri-04',6,ac,angle=50,labels={(0,1):'6 cm'},extra=r'\node at(.65,.3){$50^\circ$};\node at(4.8,.3){$60^\circ$};')
    pairs=[('cours-triangles-egaux',4,5,6,None),('tri-05',4,5,6,None),('tri-06',5,3,None,40),('tri-07',6,ac,None,50),('tri-13',7,4,5,None)]
    for name,ab,a,b,ang in pairs:
        l={(0,1):f'{ab} cm',(0,2):f'{a:.2g} cm'} if ang!=50 else {(0,1):'6 cm'}
        if b:l[(1,2)]=f'{b} cm'
        l2=dict(l)
        if name=='tri-13':
            l={(0,1):'7 cm',(0,2):reponse('4 cm'),(1,2):reponse('5 cm')}
            l2={(0,1):reponse('7 cm'),(0,2):'4 cm',(1,2):'5 cm'}
        one,_,_=triangle_tex(ab,a,b,ang,l,scale_override=.7)
        two,_,_=triangle_tex(ab,a,b,ang,l2,names='DEF',shift=7,scale_override=.7)
        if name=='tri-06':
            one+=r'\node at(.65,.2){$40^\circ$};';two+=r'\node at(7.65,.2){$40^\circ$};'
        if name=='tri-07':one+=r'\node at(.55,.25){$50^\circ$};\node at(3.65,.25){$60^\circ$};';two+=r'\node at(7.55,.25){$50^\circ$};\node at(10.65,.25){$60^\circ$};'
        # Deux dessins côte à côte : même échelle et taille suffisante.
        dessin(name,r'\begin{scope}[scale=.72]'+one+two+r'\end{scope}')
    one,_,_=triangle_tex(5,4,angle=60,labels={(0,1):'5',(0,2):'4'},scale_override=.7)
    two,_,_=triangle_tex(5,4,angle=90,labels={(0,1):'5',(0,2):'4'},names='DEF',shift=7,scale_override=.7)
    dessin('tri-08',r'\begin{scope}[scale=.72]'+one+two+r'\end{scope}')
    triangle('tri-09',5,5,angle=74,labels={(0,1):'5 cm',(0,2):'5 cm'},extra=r'\node at(.65,.45){$74^\circ$};')
    dessin('tri-10',r'\coordinate(A)at(0,0);\coordinate(B)at(5,0);\coordinate(C)at(6.5,2.5);\coordinate(D)at(1.5,2.5);\draw[geoTrait](A)--(B)--(C)--(D)--cycle (A)--(C);\foreach\p/\pos in{A/below left,B/below right,C/above right,D/above left}{\node[\pos]at(\p){$\p$};}')
    x=(25+36-16)/12;y=sqrt(25-x*x)
    t=polygone([(0,0),(x,y),(6,0),(x,-y)])
    t+=r'\draw[otMuted](0,0)--(6,0);\node[left]at(0,0){B};\node[right]at(6,0){C};'+rf'\node[above]at({x},{y}){{A}};\node[below]at({x},{-y}){{D}};\node[above left]at({x/2},{y/2}){{5 cm}};\node[above right]at({(6+x)/2},{y/2}){{4 cm}};'
    dessin('tri-11',r'\begin{scope}[scale=.65]'+t+r'\end{scope}')
    triangle('tri-12',8,5,5,labels={(0,1):'8 cm'},extra=r'\draw[geoAide](3.2,2.4)--(3.2,0);\node[right]at(3.2,1.2){3 cm};\node[below]at(3.2,0){H};\draw[otMuted](3.05,0)--(3.05,.15)--(3.2,.15);')
    triangle('tri-14',6,4,angle=35,labels={(0,1):'6 cm',(0,2):'4 cm'},extra=r'\node at(.8,.2){$35^\circ$};')
    triangle('tri-15',6,5,5,labels={(0,2):'5 cm',(1,2):'5 cm'},extra=r'\draw[geoTrait](3.2,0)--(3.2,3);\node[above]at(3.2,3){A};\node[below]at(3.2,0){M};')
    # Remplacement du dernier dessin : A au sommet, B et C à la base.
    FIGURES.pop('tri-15')
    dessin('tri-15',r'\coordinate(A)at(3,4);\coordinate(B)at(0,0);\coordinate(C)at(6,0);\coordinate(M)at(3,0);\draw[geoTrait](A)--(B)--(C)--cycle (A)--(M);\foreach\p/\pos in{A/above,B/below left,C/below right,M/below}{\node[\pos]at(\p){$\p$};}\path(A)--node[left]{5 cm}(B);\path(A)--node[right]{5 cm}(C);\node[below]at(1.5,0){3 cm};\node[below]at(4.5,0){3 cm};\geoSolution{\draw[otGreenDark](3.17,0)--(3.17,.17)--(3,.17);}')
    FIGURES['tri-15']['tex']=FIGURES['tri-15']['tex'].replace(']'+r'\coordinate(A)',r']\begin{scope}[scale=.75]\coordinate(A)',1).replace(r'\end{tikzpicture}',r'\end{scope}\end{tikzpicture}')

def pythagore():
    dat=[
    (6,8,None,True,False,{(0,1):'6 cm',(0,2):'8 cm',(1,2):reponse('10 cm')}),
    (5,12,13,True,False,{(0,1):'5 cm',(0,2):reponse('12 cm'),(1,2):'13 cm'}),
    (7,9,None,True,False,{(0,1):'7 cm',(0,2):'9 cm',(1,2):reponse(r'$\sqrt{130}$ cm')}),
    (15,8,17,True,False,{(0,1):'15 cm',(0,2):reponse('8 cm'),(1,2):'17 cm'}),
    (9,12,15,False,True,{(0,1):'9 cm',(0,2):'12 cm',(1,2):'15 cm'}),
    (4,5,7,False,False,{(0,1):'4 cm',(0,2):'5 cm',(1,2):'7 cm'}),
    (8,6,None,True,False,{(0,1):'8 cm',(0,2):'6 cm',(1,2):reponse('10 cm')}),
    (.8,sqrt(5.61),2.5,True,False,{(0,1):'0,8 m',(0,2):reponse(r'$\approx2{,}37$ m'),(1,2):'2,5 m'}),
    (6,8,10,True,False,{(0,1):'6 cm',(0,2):'8 cm',(1,2):reponse('10 cm')}),
    (10.5,6.3,8.4,False,False,{(0,1):'10,5 cm',(0,2):'6,3 cm',(1,2):'8,4 cm'}),
    ]
    for i,(a,c,b,r,p,l) in enumerate(dat,1):
        extra=''
        if i==7:extra=r'\draw[otMuted,dashed](0,3)--(4,3)--(4,0);'
        if i==10:
            cx=6.3**2/10.5;cy=sqrt(6.3**2-cx**2);sc=min(6.4/10.5,3/cy)
            # Marque d’angle droit tournée selon les deux côtés réels, uniquement après preuve.
            vx,vy=cx*sc,cy*sc;u=(-cx/6.3,-cy/6.3);v=((10.5-cx)/8.4,-cy/8.4)
            p1=(vx+.18*u[0],vy+.18*u[1]);p2=(p1[0]+.18*v[0],p1[1]+.18*v[1]);p3=(vx+.18*v[0],vy+.18*v[1])
            extra=r'\geoSolution{\draw[otGreenDark]'+f'({p1[0]},{p1[1]})--({p2[0]},{p2[1]})--({p3[0]},{p3[1]});'+'}'
        triangle(f'pyth-{i:02}',a,c,b,labels=l,right=r,proof_right=p,extra=extra)
    triangle('cours-pythagore',3,4,5,right=True,labels={(0,1):'$AB$',(0,2):'$AC$',(1,2):'$BC$'})
    FIGURES.pop('pyth-09')
    tex=axes((-1,7),(-1,9),2,2,ortho=True)
    tex=tex.replace(r'\node[below left,font=\tiny]at(0,0){0};','')
    tex+=polygone([(0,0),(6,0),(0,8)])
    for lab,x,y in [('A',0,0),('B',6,0),('C',0,8)]:tex+=rf'\fill[otNavy]({x},{y})circle(1.3pt)node[above right,geoLabel]{{$ {lab} $}};'
    tex+=r'\geoSolution{\node[text=otGreenDark,above right]at(3,4){10 cm};}\end{scope}'
    dessin('pyth-09',tex,'Repère orthonormé ; une unité représente 1 cm.')
    dessin('pyth-11',r'\draw[geoTrait](0,0)--(3,1.25)--(0,2.5)--(-3,1.25)--cycle;\draw[otMuted,dashed](-3,1.25)--(3,1.25) (0,0)--(0,2.5);\node[below]at(0,0){10 cm : diagonale verticale};\node[above]at(0,2.5){24 cm : diagonale horizontale};\draw[otMuted](0,1.4)--(.15,1.4)--(.15,1.25);')
    rectangles('pyth-12',reponse('12 cm'),'5 cm',r'\draw[geoTrait](0,0)--(5,2.5)node[midway,above,sloped,fill=white]{13 cm};')
    dessin('pyth-13',r'\draw[geoTrait](0,0)rectangle(3.2,2.4);\draw[otGreenDark](0,0)--(3.2,2.4);\node[below]at(1.6,0){8 m};\node[left]at(0,1.2){6 m};\begin{scope}[shift={(5,0)}]\draw[geoTrait](0,0)rectangle(1.4,3.36);\draw[otGreenDark](0,0)--(1.4,3.36);\node[below]at(.7,0){10 m};\node[right]at(1.4,1.68){24 m};\end{scope}')
    triangle('pyth-14',4,7,right=True,labels={(0,1):'4 cm',(0,2):'7 cm',(1,2):reponse(r'$\sqrt{65}$ cm')})
    rectangles('pyth-15','12 m','5 m',r'\draw[geoTrait](0,0)--(5,2.5)node[midway,above,sloped,fill=white]{'+reponse('13 m')+'};')

def thales(nom,ab,ac,am,an,bc=None,labels=None,parallel=True,extra='',points2=None):
    if bc is None:cx=ac*cos(radians(55));cy=ac*sin(radians(55));bc=sqrt((ab-cx)**2+cy**2)
    else:cx=(ab*ab+ac*ac-bc*bc)/(2*ab);cy=sqrt(ac*ac-cx*cx)
    pts={'A':(0,0),'B':(ab,0),'C':(cx,cy),'M':(am,0),'N':(cx*an/ac,cy*an/ac)}
    scale=min(6.5/max(ab,cx),3.3/cy)
    pp={k:(x*scale,y*scale) for k,(x,y) in pts.items()}
    tex=''
    for k,(x,y) in pp.items():tex+=rf'\coordinate({k})at({x},{y});\fill[otNavy]({k})circle(1.2pt);'
    tex+=r'\draw[geoTrait](A)--(B)--(C)--cycle (M)--(N);'
    for k,where in [('A','below left'),('B','below right'),('C','above'),('M','above right'),('N','above left')]:tex+=rf'\node[{where},geoLabel]at({k}){{$ {k} $}};'
    pos={'AB':('below',-.55),'AC':('above',.0)}
    for seg,txt in (labels or {}).items():
        a,b=seg;xa,ya=pp[a];xb,yb=pp[b];mx=(xa+xb)/2;my=(ya+yb)/2
        if seg=='AB':my-=.78
        elif seg in ['AM','MB']:my-=.26
        elif seg=='AC':mx-=.9
        elif seg in ['AN','NC']:mx-=.5
        elif seg in ['BC','MN']:mx+=.40
        tex+=rf'\node[geoLabel,font=\scriptsize]at({mx},{my}){{{txt}}};'
    if parallel:tex+=r'\node[anchor=west,font=\scriptsize]at(6.8,2.3){$(MN)\parallel(BC)$};'
    else:tex+=r'\geoSolution{\node[anchor=west,text=otGreenDark,font=\scriptsize]at(6.8,2.3){'+('parallèles' if abs(am/ab-an/ac)<1e-8 else 'non parallèles')+'};}'
    tex+=extra
    GEOMETRIE[nom]={'points':list(pts.values()),'emboites':pts,'paralleles':abs(am/ab-an/ac)<1e-8}
    dessin(nom,tex)

def tous_thales():
    vals=[
    (8,10,4,5,6,{'AB':'8 cm','AC':'10 cm','AM':'4 cm','AN':reponse('5 cm')},True),
    (12,15,8,10,9,{'AB':'12 cm','AM':'8 cm','BC':'9 cm','MN':reponse('6 cm')},True),
    (9,15,3,5,12,{'AB':'9 cm','AM':'3 cm','MN':'4 cm','BC':reponse('12 cm')},True),
    (10,8,6,4.8,6,{'AB':'10 cm','AM':'6 cm','AC':'8 cm','AN':'4,8 cm'},False),
    (9,12,6,8,10,{'AB':'9 cm','AM':'6 cm','AC':'12 cm','AN':'8 cm'},False),
    (10,15,6,8,12,{'AB':'10 cm','AM':'6 cm','AC':'15 cm','AN':'8 cm'},False),
    (12,8,9,6,10,{'AB':'12 cm','MB':'3 cm','AC':'8 cm','AN':reponse('6 cm')},True),
    (10,20,4,8,15,{'AB':'10 cm','AM':'4 cm','AC':'20 cm','BC':'15 cm','AN':reponse('8 cm'),'MN':reponse('6 cm')},True),
    (9,12,3,4,None,{'AB':'9 cm','AM':'3 cm','AC':'12 cm','AN':reponse('4 cm')},True),
    (7,9,2.5,45/14,14,{'AB':'7 cm','AM':reponse('2,5 cm'),'BC':'14 cm','MN':'5 cm'},True),
    (10,12.5,2,2.5,7.5,{'AB':'10 m','AM':'2 m','MN':'1,5 m','BC':reponse('7,5 m')},True),
    (8,10,3,3.75,8,{'AB':'8 cm','AM':'3 cm','AC':'10 cm','AN':reponse('3,75 cm'),'NC':reponse('6,25 cm')},True),
    (10,15,4,6,12,{'AB':'10 cm','AM':'4 cm','AC':'15 cm','AN':'6 cm','BC':'12 cm','MN':reponse('4,8 cm')},False),
    ]
    for i,v in enumerate(vals,1):thales(f'th-{i:02}',*v[:5],labels=v[5],parallel=v[6])
    thales('cours-thales',8,10,4,5,6,labels={'AM':'$AM$','AB':'$AB$','AN':'$AN$','AC':'$AC$','MN':'$MN$','BC':'$BC$'})
    dessin('th-14',r'\coordinate(A)at(0,0);\coordinate(B)at(6,0);\coordinate(C)at(4,3);\coordinate(M)at(2.4,1.8);\coordinate(N)at(3.6,0);\draw[geoTrait](A)--(B)--(C)--cycle (M)--(N);\foreach\i in{1,2,3,4,5}{\fill[otNavy](.8*\i,.6*\i)circle(1.4pt);}\foreach\p/\pos in{A/below left,B/below right,C/above,M/above left,N/below}{\node[\pos]at(\p){$\p$};}\node[below]at(3,-.6){$AB=10$ cm};\node[right]at(6,1.8){$(MN)\parallel(CB)$};','La demi-droite auxiliaire comporte cinq intervalles égaux ; M est au troisième.')
    dessin('th-15',r'\coordinate(A)at(0,0);\coordinate(B)at(5,0);\coordinate(C)at(0,6.667);\coordinate(M)at(1.25,0);\coordinate(N)at(0,1.667);\coordinate(P)at(3.75,0);\coordinate(Q)at(0,5);\fill[otGreen!15](M)--(N)--(Q)--(P)--cycle;\draw[geoTrait](A)--(B)--(C)--cycle (M)--(N)(P)--(Q);\foreach\p/\pos in{A/below left,B/below right,C/above,M/below,N/left,P/below,Q/left}{\node[\pos,geoLabel]at(\p){$\p$};}\draw[otMuted](.2,0)--(.2,.2)--(0,.2);\node[right]at(4,4){$AB=12$ cm};\node[right]at(4,3.4){$AC=16$ cm};\node[right]at(4,2.8){$AM=3$ cm};\node[right]at(4,2.2){$AP=9$ cm};','Les droites MN, PQ et BC sont parallèles ; la zone colorée est la bande cherchée.')
    FIGURES['th-15']['tex']=FIGURES['th-15']['tex'].replace(']'+r'\coordinate(A)',r']\begin{scope}[scale=.6]\coordinate(A)',1).replace(r'\end{tikzpicture}',r'\end{scope}\end{tikzpicture}')

def cosinus():
    triangle('cours-cosinus',6,8,right=True,labels={(0,1):'adjacent à B',(1,2):'hypoténuse'},extra=r'\node at(1.5,.25){angle B};')
    dat=[
    (6,8,10,{(0,1):'$AB$',(0,2):'$AC$',(1,2):'$BC$'},None),
    (6,8,10,{(0,1):'6 cm',(1,2):'10 cm'},None),
    (6,8,10,{(0,2):'8 cm',(1,2):'10 cm'},None),
    (6,sqrt(108),12,{(0,1):reponse('6 cm'),(1,2):'12 cm'},60),
    (8*cos(radians(35)),8*sin(radians(35)),8,{(0,1):reponse(r'$\approx6{,}55$ cm'),(1,2):'8 cm'},35),
    (7,7*sin(radians(40))/cos(radians(40)),7/cos(radians(40)),{(0,1):'7 cm',(1,2):reponse(r'$\approx9{,}14$ cm')},40),
    (5,12,13,{(0,1):'5 cm',(1,2):'13 cm'},None),
    (9,12,15,{(0,1):'9 cm',(1,2):'15 cm'},None),
    (10*sin(radians(50)),10*cos(radians(50)),10,{(0,2):reponse(r'$\approx6{,}43$ cm'),(1,2):'10 cm'},None),
    (6,7,10,{(0,1):'6 cm',(1,2):'10 cm'},None),
    (1.5,sqrt(16-2.25),4,{(0,1):'1,5 m',(0,2):reponse(r'$\approx3{,}71$ m'),(1,2):'4 m'},None),
    (5.7,sqrt(36-5.7**2),6,{(0,1):'5,7 m',(1,2):'6 m'},None),
    (3.2*cos(radians(27)),3.2*sin(radians(27)),3.2,{(0,1):reponse(r'$\approx2{,}85$ km'),(1,2):'3,2 km'},27),
    (10*cos(radians(30)),5,10,{(0,1):reponse(r'$\approx8{,}66$ cm'),(1,2):'10 cm'},30),
    (9,9*sin(radians(58))/cos(radians(58)),9/cos(radians(58)),{(0,1):'9 m',(0,2):reponse(r'$\approx14{,}4$ m'),(1,2):reponse(r'$\approx17{,}0$ m')},58)
    ]
    for i,(ab,ac,bc,l,angle) in enumerate(dat,1):
        extra=''
        if angle:extra=rf'\node[geoLabel,font=\scriptsize]at({min(6.4/ab,3/ac)*ab-.5},.22){{$ {angle}^\circ $}};'
        if i==9:extra=r'\node[geoLabel]at(.25,2.45){$50^\circ$};'
        if i in [7,8,11,12]:
            rep={7:r'67^\circ',8:r'53{,}1^\circ',11:r'68^\circ',12:r'18{,}2^\circ'}[i]
            extra+=r'\geoSolution{\node[anchor=west,text=otGreenDark,font=\scriptsize]at(6.8,1.5){$\widehat B\approx '+rep+r'$};}'
            if i==8:extra+=r'\geoSolution{\node[anchor=west,text=otGreenDark,font=\scriptsize]at(6.8,.9){$\widehat C\approx36{,}9^\circ$};}'
        triangle(f'cos-{i:02}',ab,ac,bc,labels=l,right=i!=10,extra=extra)
    FIGURES.pop('cos-14')
    one,_,_=triangle_tex(10*cos(radians(30)),5,right=True,labels={(0,1):reponse(r'$\approx8{,}66$ cm'),(1,2):'10 cm'},scale_override=.5)
    two,_,_=triangle_tex(5,10*sin(radians(60)),right=True,labels={(0,1):reponse('5 cm'),(1,2):'10 cm'},names='DEF',shift=7,scale_override=.5)
    dessin('cos-14',r'\begin{scope}[scale=.85]'+one+two+r'\node at(3.7,.2){$30^\circ$};\node at(8.9,.2){$60^\circ$};\end{scope}')

def trans_grid(nom,pts,delta,labels='ABC',known=(),caption=''):
    img=[(x+delta[0],y+delta[1]) for x,y in pts]
    allp=pts+img+list(known)
    xb=(min(0,min(x for x,y in allp)-1),max(x for x,y in allp)+1);yb=(min(0,min(y for x,y in allp)-1),max(y for x,y in allp)+1)
    tex=axes(xb,yb,ortho=True)
    if len(pts)>2:tex+=polygone(pts)
    for (x,y),lab in zip(pts,labels):tex+=rf'\fill[otNavy]({x},{y})circle(1.4pt)node[above left,geoLabel]{{$ {lab} $}};'
    if known:
        for (x,y),lab in zip(known,['P','Q']):tex+=rf'\fill[otNavy]({x},{y})circle(1.4pt)node[below left,geoLabel]{{$ {lab} $}};'
        tex+=rf'\draw[geoVecteur]({known[0][0]},{known[0][1]})--({known[1][0]},{known[1][1]});'
    sol=polygone(img,'otGreenDark') if len(img)>2 else ''
    for (x,y),lab in zip(img,labels):sol+=rf'\fill[otGreenDark]({x},{y})circle(1.4pt)node[below right,geoLabel]{{$ {lab}^{{\prime}} $}};'
    tex+=r'\geoSolution{'+sol+r'}\end{scope}'
    GEOMETRIE[nom]={'translation':{'points':pts,'images':img,'deplacement':delta}}
    dessin(nom,tex,caption or 'Repère orthonormé ; les images cherchées sont ajoutées en vert au corrigé.')

def translations():
    trans_grid('trans-01',[(1,2)],(3,1),'A',[(0,0),(3,1)])
    trans_grid('cours-translation',[(1,1),(3,1),(2,3)],(3,2),known=[(0,0),(3,2)])
    FIGURES['cours-translation']['tex']=r'\otGeoCorrigetrue'+FIGURES['cours-translation']['tex']
    trans_grid('trans-02',[(1,1),(3,1),(2,3)],(3,2))
    trans_grid('trans-03',[(2,3)],(-4,-1),'B')
    triangle('trans-04',5,3,angle=42,labels={(0,1):'5 cm'},extra=r'\node[anchor=west]at(5,2.4){$42^\circ$ ; aire 9 cm$^2$};')
    # L’aire donnée est une donnée abstraite cohérente : ajuster le côté non nommé pour qu’elle soit 9.
    FIGURES.pop('trans-04');triangle('trans-04',5,18/(5*sin(radians(42))),angle=42,labels={(0,1):'5 cm'},extra=r'\node[anchor=west,font=\scriptsize]at(5,2.4){$42^\circ$ ; aire 9 cm$^2$};')
    tex=''
    for i in range(5):tex+=polygone([(i*1.8,0),(i*1.8+1.0,0),(i*1.8+.4,1)])
    dessin('trans-05',tex+r'\draw[|<->|](0,-.5)--node[below]{4 cm}(1.8,-.5);')
    dessin('trans-06',r'\draw[geoTrait](0,0)--(3,0)--(5,2)--(2,2)--cycle;\node[below left]at(0,0){A};\node[below right]at(3,0){B};\node[above right]at(5,2){B’};\node[above left]at(2,2){A’};\draw[geoVecteur](.4,.4)--(2.4,2.4);')
    rectangles('trans-07','6 cm','4 cm',r'\node[right]at(5.7,1.25){$k=1{,}5$};',answer='9 cm sur 6 cm')
    triangle('trans-08',5,7,8,labels={(0,1):'5 cm',(0,2):'7 cm',(1,2):'8 cm'},extra=r'\node[right]at(6.9,2.5){$k=2/5$};')
    rectangles('trans-09','$L$',r'$\ell$',r'\node at(2.5,1.25){18 cm$^2$};\node[right]at(5.7,1.25){$k=3$};')
    pave('trans-10','8 cm','6 cm','5 cm',r'\node[right]at(6.7,2){$k=1/2$};')
    dessin('trans-11',r'\draw[geoTrait](0,0)rectangle(2,1.4);\draw[geoTrait](4,0)rectangle(7,2.1);\node at(1,.7){20 cm$^2$};\node at(5.5,1.05){45 cm$^2$};\node[below]at(1,0){8 cm};\node[below]at(5.5,0){'+reponse('12 cm')+'};')
    pave('trans-12','12 cm','8 cm','6 cm',r'\node[right]at(6.7,2){$k=1/3$};')
    dessin('trans-13',r'\draw[geoVecteur](0,0)--node[below,sloped]{5 à droite, 2 en haut}(5,2);\draw[geoVecteur](5,2)--node[right]{3 à gauche, 4 en haut}(2,6);\geoSolution{\draw[geoReponse,->](0,0)--node[left]{2 à droite, 6 en haut}(2,6);}')
    rectangles('trans-14','maquette','',r'\node at(2.5,1.25){0,8 m$^2$};\node[right]at(5.7,1.25){$k=2{,}5$};')
    tex=''
    for i in range(6):
        for j in range(4):tex+=rf'\draw[draw=otNavy,fill=otGreen!{15 if (i+j)%2 else 30}]({i*.8},{j*.8})rectangle++(.8,.8);'
    dessin('trans-15',tex+r'\draw[|<->|](0,-.5)--node[below]{2 cm}(.8,-.5);','Pavage de six colonnes et quatre lignes ; chaque case est un motif.')

def pyramide(nom,base='6 cm',h='8 cm',extra=''):
    tex=r'\coordinate(A)at(0,0);\coordinate(B)at(4,0);\coordinate(C)at(5.3,1.2);\coordinate(D)at(1.3,1.2);\coordinate(S)at(2.65,4);\coordinate(H)at(2.65,.6);\draw[geoTrait](S)--(A)--(B)--(C)--(S)--(B);\draw[otMuted,dashed](A)--(D)--(C) (D)--(S)(S)--(H);'
    for p,pos in [('A','below left'),('B','below right'),('C','right'),('D','left'),('S','above'),('H','below')]:tex+=rf'\node[{pos},font=\scriptsize]at({p}){{$ {p} $}};'
    if base:tex+=rf'\path(A)--node[below]{{{base}}}(B);'
    if h:tex+=rf'\node[right,fill=white,font=\scriptsize]at(2.65,2.4){{{h}}};'
    tex+=r'\draw[otMuted](2.65,.85)--(2.9,.85)--(2.9,.6);'
    dessin(nom,tex+extra,'Perspective cavalière ; SH est la hauteur perpendiculaire au plan de base.')

def repere_espace(nom,point=False):
    t=r'\coordinate(O)at(0,0);\coordinate(X)at(6,0);\coordinate(Y)at(1.6,1.4);\coordinate(Z)at(0,3);\draw[geoTrait](O)--(X)--(7.6,1.4)--(7.6,4.4)--(1.6,4.4)--(Z)--cycle (X)--(6,3)--(Z) (6,3)--(7.6,4.4);\draw[otMuted,dashed](O)--(Y)--(7.6,1.4)(Y)--(1.6,4.4);\draw[geoVecteur](O)--(6.8,0)node[right]{$x$};\draw[geoVecteur](O)--(2,1.75)node[above]{$y$};\draw[geoVecteur](O)--(0,3.8)node[above]{$z$};\node[below left]at(O){O};\node[below]at(6,0){6};\node[right]at(1.6,1.4){4};\node[left]at(0,3){3};\node[above right]at(7.6,4.4){G};\node[above left]at(1.6,4.4){H};'
    if point:t+=r'\geoSolution{\draw[otGreenDark,dashed](2,0)--(3.2,1.05)--(3.2,2.05);\fill[otGreenDark](3.2,2.05)circle(2pt)node[right]{$M(2;3;1)$};}'
    dessin(nom,t,'Axes gradués selon les dimensions 6, 4, 3 ; perspective cavalière, non orthonormée sur la feuille.')

def solides():
    pyramide('sol-01','','')
    pyramide('sol-02')
    cone('sol-03','3 cm','5 cm');cone('sol-04',reponse('4 cm'),'9 cm')
    repere_espace('sol-05');repere_espace('sol-06',True)
    pyramide('sol-07','base triangulaire','10 cm',r'\node[anchor=west,font=\scriptsize]at(5.7,2){$\mathcal B=(8\times3)/2$ cm$^2$};')
    # Véritable base triangulaire pour cet exercice.
    FIGURES.pop('sol-07')
    dessin('sol-07',r'\coordinate(A)at(0,0);\coordinate(B)at(5,0);\coordinate(C)at(1.2,1.5);\coordinate(S)at(2,4);\draw[geoTrait](S)--(A)--(B)--(S)--(C)--(B);\draw[otMuted,dashed](A)--(C) (S)--(2,.55);\node[below]at(2.5,0){8 cm};\node[right]at(2,2.4){hauteur : 10 cm};\node[above right]at(3,1){hauteur de base : 3 cm};\node[above]at(S){S};','Pyramide à base triangulaire ; les deux hauteurs concernent des plans différents.')
    FIGURES['sol-07']['tex']=FIGURES['sol-07']['tex'].replace(r'\node[above right]at(3,1){hauteur de base : 3 cm};',r'\draw[otGreenDark,dashed](1.2,1.5)--(1.2,0);\node[left,font=\scriptsize,fill=white]at(1.2,.75){3 cm};\draw[otMuted](1.2,.15)--(1.35,.15)--(1.35,0);')
    pyramide('sol-08','base : 45 cm$^2$',reponse('10 cm'),r'\node[anchor=west,font=\scriptsize]at(5.7,2){$V=150$ cm$^3$};')
    tex=r'\draw[geoTrait](0,0)rectangle(2,2);'
    hh=sqrt(25-4)*.5
    for pts in [[(0,0),(2,0),(1,-hh)],[(2,0),(2,2),(2+hh,1)],[(2,2),(0,2),(1,2+hh)],[(0,2),(0,0),(-hh,1)]]:
        tex+=r'\geoSolution{'+polygone(pts,'otGreenDark')+'}'
    tex+=r'\node at(1,1){4 cm};\geoEnonce{\node[above]at(1,2.5){Construire les faces latérales.};}\geoSolution{\node[above]at(1,4.5){Arêtes latérales : 5 cm};}'
    dessin('sol-09',tex,'Le carré est fourni ; les quatre triangles latéraux sont ajoutés au corrigé.')
    dessin('sol-10',r'\geoEnonce{\draw[otMuted](0,0)circle(1.5);\node at(0,0){disque : $r=3$ cm};\node[anchor=west]at(2,0){Secteur à construire, rayon 5 cm.};}\geoSolution{\begin{scope}[scale=.55]\filldraw[fill=otGreen!15,draw=otNavy](0,0)--(0:5)arc(0:216:5)--cycle;\draw[otMuted](1,0)arc(0:216:1);\node at(-1.2,1.1){$216^\circ$};\node[above]at(2.5,0){5 cm};\draw[geoTrait](9,0)circle(3);\node at(9,0){$r=3$ cm};\end{scope}}','Les deux pièces sont présentées séparément ; le bord du secteur rejoint le cercle de base.')
    FIGURES['sol-10']['tex']=FIGURES['sol-10']['tex'].replace(r'\end{scope}}',r'\draw[geoTrait](-14,0)--(-11,4)--(-8,0);\draw[geoTrait](-14,0)arc(180:360:3 and .65);\draw[otMuted,dashed](-14,0)arc(180:0:3 and .65) (-11,0)--(-11,4);\draw[geoTrait](-11,0)--node[below]{3 cm}(-8,0);\node[right,fill=white,font=\scriptsize]at(-9.5,2){5 cm};\node[above,font=\scriptsize]at(-11,4){Perspective};\end{scope}}')
    cone('sol-11','5 cm','12 cm')
    FIGURES['sol-11']['tex']=FIGURES['sol-11']['tex'].replace(r'\end{tikzpicture}',r'\geoSolution{\node[text=otGreenDark,above left,font=\scriptsize]at(-1,1.75){13 cm};}\end{tikzpicture}')
    cylindre('sol-12','4 cm','6 cm')
    cone('sol-13','40 cm','1,2 m')
    pave('sol-14','8 cm','6 cm','4 cm',r'\draw[geoTrait](0,2.6)--(3.15,5.2)--(5,2.6) (3.15,5.2)--(6.3,3.8);\draw[otMuted,dashed](1.3,3.8)--(3.15,5.2);\node[right]at(6.7,4.6){hauteur du toit : 3 cm};')
    cone('sol-15','6 cm','10 cm')
    pyramide('cours-solides','côté de base','$h$',r'\node[anchor=west,font=\scriptsize]at(5.8,2.5){Base polygonale};')

def script_lines(cmds,depth=0):
    out=[]
    def cond(s):
        return {'x>=10':r'x $\ge$ 10','x%2==0':'reste de x divisé par 2 = 0','contact==1':'touche le lutin Guide ?','y>0':'y > 0'}.get(s,s)
    for c in cmds:
        op=c[0];kind='calcul'
        if op=='set':txt=f'mettre {c[1]} à {c[2]}'
        elif op=='input':
            if c[1]=='contact':continue
            txt=f'demander {c[1]} et mémoriser la réponse';kind='entree'
        elif op=='add':txt=f'ajouter {c[2]} à {c[1]}'
        elif op=='mul':txt=f'mettre {c[1]} à ({c[1]} × {c[2]})'
        elif op=='addvar':txt=f'ajouter {c[2]} à {c[1]}'
        elif op=='setexpr':txt=f'mettre {c[1]} à (3 × x + 5)'
        elif op=='say':txt=f'dire {c[1]}';kind='entree'
        elif op=='saytext':txt=f'dire « {c[1]} »';kind='entree'
        elif op in ['move','movevar']:txt=f'avancer de {c[1]}';kind='mouvement'
        elif op=='turn':txt=f'tourner de {c[1]} degrés (sens antihoraire)';kind='mouvement'
        elif op=='repeat':
            out.append((depth,f'répéter {c[1]} fois','controle'));out+=script_lines(c[2],depth+1);out.append((depth,'fin de répéter','controle'));continue
        elif op=='if':
            out.append((depth,'si '+cond(c[1])+' alors','controle'));out+=script_lines(c[2],depth+1)
            if c[3]:out.append((depth,'sinon','controle'));out+=script_lines(c[3],depth+1)
            out.append((depth,'fin de si','controle'));continue
        out.append((depth,txt,kind))
    return out

def scripts():
    for nom,cmds in SCRIPTS.items():
        event='quand la touche espace est pressée' if nom=='script-10' else 'quand le drapeau est cliqué'
        lines=[(0,event,'evenement')]+script_lines(cmds)
        if nom in ['script-07','script-08','script-11','script-13']:lines.insert(1,(0,'stylo baissé ; départ (0 ; 0), vers la droite','mouvement'))
        tex=pile(lines)
        if nom=='script-14':
            tex=r'\geoEnonce{'+tex+'}'+r'\geoSolution{'+pile([(0,'quand le drapeau est cliqué','evenement'),(0,'mettre s à 0','calcul'),(0,'répéter 4 fois','controle'),(1,'ajouter 3 à s','calcul'),(0,'fin de répéter','controle'),(0,'dire s','entree')])+'}'
        if nom=='script-15':tex=r'\geoEnonce{\node[draw=otMuted,rounded corners=1mm,inner sep=5mm]{Construire les blocs : entrée, calcul, condition, affichage.};}\geoSolution{'+tex+'}'
        if nom in ['script-07','script-08','script-11','script-13']:
            if nom=='script-08':
                shape=polygone([(9,-2.5),(12,-2.5),(12,-1.3),(9,-1.3)],'otGreenDark')+r'\node[below]at(10.5,-2.5){50 pixels};\node[right]at(12,-1.9){20 pixels};'
            elif nom=='script-11':
                shape=polygone([(9,-3),(12,-3),(10.5,-.402)],'otGreenDark')+r'\node[below]at(10.5,-3){40 pixels};'
            else:
                label='30 pixels' if nom=='script-07' else 'c pixels'
                shape=polygone([(9,-3),(12,-3),(12,0),(9,0)],'otGreenDark')+rf'\node[below]at(10.5,-3){{{label}}};'
            ydep=-2.5 if nom=='script-08' else -3
            shape+=rf'\fill[otGreenDark](9,{ydep})circle(1.5pt);\node[below,font=\scriptsize]at(10.5,-3.7){{Figure tracée}};'
            tex+=r'\geoSolution{'+shape+'}'
        dessin(nom,tex,'Blocs de type Scratch ; indentation et lignes « fin » montrent les blocs imbriqués.')

def annexes():
    # Les figures partagées sont réutilisées seulement lorsque les données correspondent.
    triangle('defi-pyth',9,12,right=True,labels={(0,1):'9 cm',(0,2):'12 cm',(1,2):reponse('15 cm')})
    thales('defi-thales',12,16,3,4,20,labels={'AB':'12 cm','AC':'16 cm','AM':'3 cm','AN':reponse('4 cm')})
    triangle('defi-cosinus',6,8,right=True,labels={(0,1):'6 m',(1,2):'10 m'})
    carre('defi-racine',reponse(r'$\sqrt{72}$ cm'),'72 cm$^2$')
    FIGURES['defi-racine']['tex']=FIGURES['defi-racine']['tex'].replace(r'\node[align=center]at(1.5,1.5){72 cm$^2$};',r'\draw[otMuted,dashed](1.5,0)--(1.5,3) (0,1.5)--(3,1.5);\foreach\x in{.75,2.25}{\foreach\y in{.75,2.25}{\node[font=\scriptsize]at(\x,\y){18 cm$^2$};}}')
    dessin('defi-litteral',r'\draw[geoTrait](0,0)rectangle(4,2.4);\draw[geoTrait](6,0)rectangle(11,1.6);\node at(2,1.2){A};\node at(8.5,.8){B};\node[below]at(2,0){$x+4$ cm};\node[below]at(8.5,0){$x+6$ cm};\node[left]at(0,1.2){3 cm};\node[left]at(6,.8){2 cm};')
    secteurs('defi-stat',[180,120,60],['A','B','C'])
    dessin('defi-cible',r'\draw[geoTrait](0,0)rectangle(4,4);\filldraw[fill=otGreen!30,draw=otNavy](2,2)circle(1);\node[below]at(2,0){8 cm};\draw[otMuted](2,2)--node[above]{2 cm}(3,2);')
    pave('defi-volume','6 cm','4 cm','3 cm')
    dessin('defi-triangles',r'\draw[geoTrait](0,0)--(6,0)--(3,3)--cycle (3,3)--(3,0);\node[above]at(3,3){A};\node[below left]at(0,0){B};\node[below right]at(6,0){C};\node[below]at(3,0){M};\node[above left]at(1.5,1.5){$AB=AC$};')
    tex=axes((-1,7),(-2,7),ortho=True)+polygone([(0,1),(2,1),(1,3)])
    for label,(x,y) in zip('ABC',[(0,1),(2,1),(1,3)]):tex+=rf'\node[above left,geoLabel]at({x},{y}){{$ {label} $}};'
    sol=''
    for points,prime,color in [([(4,-1),(6,-1),(5,1)],r'\prime','otMuted'), ([(3,4),(5,4),(4,6)],r'\prime\prime','otGreenDark')]:
        sol+=polygone(points,color)
        for lab,(x,y) in zip('ABC',points):sol+=rf'\node[above right,geoLabel,text={color}]at({x},{y}){{$ {lab}^{{{prime}}} $}};'
    dessin('defi-translation',tex+r'\geoSolution{'+sol+r'}\end{scope}','Repère orthonormé ; première image grise et seconde image verte dans le corrigé.')
    GEOMETRIE['defi-translation']={'translation':{'points':[(0,1),(2,1),(1,3)],'images':[(3,4),(5,4),(4,6)],'deplacement':(3,3)}}
    pyramide('defi-pyramide','6 cm','8 cm')
    dessin('defi-script',pile([(0,'quand le drapeau est cliqué','evenement'),(0,'mettre s à 0 ; mettre n à 1','calcul'),(0,'répéter 10 fois','controle'),(1,'ajouter n à s','calcul'),(1,'ajouter 1 à n','calcul'),(0,'fin de répéter','controle'),(0,'dire s','entree')]),'Suivre simultanément la somme s et le prochain entier n.')
    triangle('bilan-a-geometrie',6,8,10,right=True,labels={(0,1):'6 m',(0,2):'8 m',(1,2):reponse('10 m')})
    cone('bilan-a-cone','3 cm','12 cm')
    thales('bilan-b-thales',10,15,4,6,12,labels={'AB':'10 cm','AC':'15 cm','AM':'4 cm','AN':'6 cm','BC':'12 cm'},parallel=False)
    dessin('bilan-b-script',pile([(0,'quand le drapeau est cliqué','evenement'),(0,'mettre x à 2','calcul'),(0,'répéter 4 fois','controle'),(1,'mettre x à (x × 3)','calcul'),(0,'fin de répéter','controle'),(0,'dire x','entree')]),'La valeur initiale n’est pas un tour supplémentaire.')
    dessin('preuve-pythagore',r'\begin{scope}[scale=.6]\draw[geoTrait](0,0)rectangle(7,7);\coordinate(P)at(3,0);\coordinate(Q)at(7,3);\coordinate(R)at(4,7);\coordinate(S)at(0,4);\filldraw[fill=otGreen!20,draw=otNavy](P)--(Q)--(R)--(S)--cycle;\draw[otMuted](P)--(3,0) (Q)--(7,3);\node[below]at(1.5,0){$a$};\node[below]at(5,0){$b$};\node[above,sloped]at(5,1.5){$c$};\end{scope}','Quatre triangles rectangles identiques entourent un carré central.')

def write_all(root):
    nombres_modeles();statistiques_hasard();triangles_egaux();pythagore();tous_thales();cosinus();translations();solides();scripts();annexes()
    root=Path(root);(root/'figures').mkdir(exist_ok=True)
    for nom,d in FIGURES.items():
        body=r'\resizebox{\ifdim\width>\linewidth\linewidth\else\width\fi}{!}{'+d['tex']+'}'
        # Les dessins sont déjà bornés en largeur ; évite toute mise à l’échelle inutile du texte.
        body=d['tex']
        (root/'figures'/(nom+'.tex')).write_text(body+r'\par\vspace{1mm}{\fontsize{8}{10}\selectfont\color{otMuted}'+d['legende']+'}',encoding='utf8')
