"""Figures de géométrie, de données, de hasard et de programmation de Sixième."""
from math import cos,sin,radians,sqrt,tan,pi
from generer_figures import (META,FIGURES,dessin,pile,SCRIPTS,lignes,executer,C,answer,sol,dotpt,P,L,T,grille,points_grille,
    poly,seg,sub,add,mul,dist,unit,direc,polar,mid,foot,reflect,inter_cc,inter_ll,circumcenter,angle_en,ligne,demi,marque,droit,
    arcang,arc_at,arc_cercle,cercle,accolade,cubes_tex,assemblage,vue,s_pave,s_prisme,s_pyramide,s_cylindre,s_cone,s_boule,
    symaxe,symdiag,sym_oblique_meta,quad,chemin,barres_diag,courbe,circulaire_tex,urne_tex,roue_tex,horloge)

def tri(A,B,Cc,labs=('A','B','C'),pos=('below left','below right','above'),style='geoTrait',fill=''):
    t=poly([A,B,Cc],style,fill=fill)
    for p,l,w in zip((A,B,Cc),labs,pos):
        if l:t+=L(p,l,w)
    return t

# ================================================================= chapitre 13 : distances et cercles
def distances():
    A=(1.0,2.25);B=(3.4,2.65);t=ligne(A,B,1.6)+P(A,'A','above')+P(B,'B','above')+T((6.6,2.55),'(AB)','right',r'\scriptsize','otMuted')
    Cc=(.4,1.0);D=(5.6,1.0);M=mid(Cc,D);t+=seg(Cc,D)+P(Cc,'C','below')+P(D,'D','below')+P(M,'M','below')+marque(Cc,M)+marque(M,D)+T((6.6,1.0),'{[CD]}','right',r'\scriptsize','otMuted')
    E=(.4,-.2);F=(2.6,-.2);t+=demi(E,F,3.4)+P(E,'E','below')+P(F,'F','below')+T((6.6,-.2),'{[EF)}','right',r'\scriptsize','otMuted')
    dessin('cours-objets',t,'Une droite, un segment codé avec son milieu M, une demi-droite d’origine E.')
    META['cours-objets']={'type':'libre'}
    O=(0,0);r=1.8;A=polar(O,35,r);B=polar(O,160,r);Cc=polar(O,340,r);D=polar(O,215,r);E=polar(O,295,r)
    t=rf'\fill[otNavy!6]{C(O)}circle({r});'+cercle(O,r)+seg(O,A,'otGreenDark,line width=1pt')+seg(B,Cc,'otOrange!80!black,line width=1pt')+seg(D,E,'otNavy,line width=1pt')
    t+=P(O,'O','below')+P(A,'A','above right')+P(B,'B','left')+P(Cc,'C','right')+P(D,'D','below left')+P(E,'E','below right')
    t+=T(mid(O,A),'rayon','above left',r'\tiny','otGreenDark')+T(polar(O,160,.9),'diamètre','above',r'\tiny','otOrange!80!black')+T(mid(D,E),'corde','above right',r'\tiny','otNavy')
    dessin('cours-cercle',t,'Le disque est la surface colorée, limitée par le cercle de centre O.')
    META['cours-cercle']={'type':'cercle','O':O,'r':r,'diametre':[B,Cc]}
    # dis-1
    A=(.3,1.5);B=(2.3,2.1);t=ligne(A,B,.7)+P(A,'A','below right')+P(B,'B','below right')
    Cc=(4.0,2.2);D=(6.3,1.2);t+=seg(Cc,D)+P(Cc,'C','above')+P(D,'D','below')
    E=(7.2,.9);F=(8.4,1.7);t+=demi(E,F,1.2)+P(E,'E','below')+P(F,'F','below right')
    for n,p in [(1,(-.2,2.2)),(2,(4.9,2.3)),(3,(7.4,2.1))]:t+=rf'\node[circle,draw=otMuted,inner sep=1pt,font=\tiny,text=otMuted]at{C(p)}{{{n}}};'
    dessin('dis-1',t,'Trois objets géométriques numérotés de 1 à 3.')
    META['dis-1']={'type':'libre'}
    A=(0,0);B=(3,0);Cc=(2.6,2.6);D=(0,3)
    t=poly([A,B,Cc,D])+marque(A,B)+marque(A,D)+marque(B,Cc,2)+marque(Cc,D,2)+droit(A,B,D)
    t+=L(A,'A','below left')+L(B,'B','below right')+L(Cc,'C','above right')+L(D,'D','above left')
    dessin('dis-2',t,'Figure à main levée ; seuls les codages renseignent.')
    META['dis-2']={'type':'quadrilatere','points':[A,B,Cc,D]}
    A=(0,0);B=(7,0);M=(3.5,0);N=(3,0)
    t=seg(A,B)+P(A,'A','below')+P(B,'B','below')+P(M,'M','below')+P(N,'N','above')+marque(A,M)+marque(M,B)+rf'\draw[otMuted,<->](0,-.65)--(7,-.65);'+T((3.5,-.65),'7 cm','below',r'\scriptsize')
    dessin('dis-3',t,'Le segment [AB] et son milieu M, codé ; le point N est sur le segment.')
    META['dis-3']={'type':'segment','A':A,'B':B,'M':M,'N':N}
    O=(0,0);r=1.7;A=polar(O,40,r);B=polar(O,150,r);Cc=polar(O,330,r);D=polar(O,200,r);E=polar(O,285,r)
    t=cercle(O,r)+seg(O,A)+seg(B,Cc)+seg(D,E)+P(O,'O','below')+P(A,'A','above right')+P(B,'B','above left')+P(Cc,'C','below right')+P(D,'D','left')+P(E,'E','below')
    dessin('dis-4',t,'Le cercle de centre O et trois segments.')
    META['dis-4']={'type':'cercle','O':O,'r':r,'segments':{'OA':[O,A],'BC':[B,Cc],'DE':[D,E]}}
    O=(0,0);M=polar(O,35,3);N=polar(O,150,2.4);Pp=polar(O,290,3.6)
    t=cercle(O,3)+P(O,'O','below')+P(M,'M','above right')+P(N,'N','above')+P(Pp,'P','right')
    dessin('dis-5',t,'Le cercle de centre O et de rayon 3 cm.')
    META['dis-5']={'type':'distances','O':O,'r':3,'points':{'M':M,'N':N,'P':Pp}}
    O1=(0,0);O2=(4.3,0)
    t=cercle(O1,2.3)+seg(polar(O1,180,2.3),polar(O1,0,2.3))+P(O1,'O_1','below')+T((-.8,0),'4,6 cm','above',r'\scriptsize')+L(polar(O1,125,2.3),r'\mathcal C_1','above left')
    t+=cercle(O2,1.4)+seg(O2,polar(O2,60,1.4))+P(O2,'O_2','below')+T(mid(O2,polar(O2,60,1.4)),'1,4 cm','right',r'\scriptsize')+L(polar(O2,45,1.4),r'\mathcal C_2','above right')
    dessin('dis-6',t,'Les cercles $\\mathcal C_1$ et $\\mathcal C_2$, en vraie grandeur.')
    META['dis-6']={'type':'cercles','rayons':[2.3,1.4]}
    A=(0,0);B=(4,0);I=inter_cc(A,2,B,3)
    t=P(A,'A','below left')+P(B,'B','below right')+rf'\draw[otMuted,<->](0,-.45)--(4,-.45);'+T((2,-.45),'4 cm','below',r'\scriptsize')
    t+=sol(cercle(A,2,'geoAide')+cercle(B,3,'geoAide')+''.join(P(p,'','',' otGreenDark'.strip()) for p in I))
    dessin('dis-7',t,'Les points A et B ; les constructions figurent en vert au corrigé.')
    META['dis-7']={'type':'intersections','centres':[A,B],'rayons':[2,3],'points':I}
    A=(0,0);B=(6,0);M=(3,0)
    t=seg(A,B)+P(A,'A','left')+P(B,'B','right')+sol(P(M,'M','below','otGreenDark')+marque(A,M,1,'otGreenDark')+marque(M,B,1,'otGreenDark')+cercle(M,3,'geoReponse'))
    dessin('dis-8',t,'Le segment [AB] de 6 cm ; le cercle demandé figure en vert au corrigé.')
    META['dis-8']={'type':'cercle','O':M,'r':3,'passe':[A,B]}
    O=(0,0);r=2.5;A=polar(O,170,r);B=polar(O,350,r);Cc=polar(O,123.13,r);D=polar(O,16.87,r);E=polar(O,213.13,r);F=polar(O,286.87,r)
    t=cercle(O,r)+seg(A,B)+seg(Cc,D)+seg(E,F)+P(O,'O','above')+P(A,'A','left')+P(B,'B','right')+P(Cc,'C','above left')+P(D,'D','right')+P(E,'E','below left')+P(F,'F','below')
    dessin('dis-9',t,'Le cercle de centre O et de rayon 2,5 cm, avec trois cordes.')
    META['dis-9']={'type':'cordes','longueurs':{'AB':dist(A,B),'CD':dist(Cc,D),'EF':dist(E,F)},'O':O,'A':A,'B':B}
    A=(0,0);B=polar(A,25,3.6);Cc=(4.3,1.8);D=polar(Cc,-30,3.4);E=(8.9,0);F=polar(E,100,3.8)
    t=seg(A,B)+seg(Cc,D)+seg(E,F)+P(A,'A','left')+P(B,'B','above')+P(Cc,'C','above')+P(D,'D','below')+P(E,'E','below')+P(F,'F','left')
    dessin('dis-10',t,'Trois segments en vraie grandeur, dans trois directions différentes.')
    META['dis-10']={'type':'longueurs','valeurs':{'AB':dist(A,B),'CD':dist(Cc,D),'EF':dist(E,F)}}
    A=(0,0);V={'V1':polar(A,40,2.1),'V2':polar(A,160,3.4),'V3':polar(A,250,2.9),'V4':polar(A,320,3.0)}
    t=sol(rf'\fill[otGreen!18]{C(A)}circle(3);\draw[geoReponse]{C(A)}circle(3);')+rf'\fill[otNavy]{C(A)}circle(2pt);'+T(A,'antenne A','below',r'\tiny')
    for k,p in V.items():t+=rf'\node[draw=otNavy,fill=white,inner sep=1.5pt,font=\tiny]at{C(p)}{{{k}}};'
    t+=T((-3.4,3.1),'1 cm pour 1 km','right',r'\tiny','otMuted')
    dessin('dis-11',t,'Carte des villages ; la zone couverte figure en vert au corrigé.')
    META['dis-11']={'type':'distances','O':A,'r':3,'points':V}
    Pp=(0,0);R=(5,0);Tt=inter_cc(Pp,4,R,3)
    t=rf'\fill[otGreenDark]{C(Pp)}++(-.18,0)--++(.36,0)--++(-.18,.45)--cycle;\fill[otMuted!60]{C(R)}ellipse(.3 and .18);'+L(Pp,'P','below left')+L(R,'R','below right')
    t+=rf'\draw[otMuted,<->](0,-.55)--(5,-.55);'+T((2.5,-.55),'5 m','below',r'\scriptsize')
    s=''
    for p,lab in zip(Tt,['T_1','T_2']):
        s+=arc_cercle(Pp,4,direc(Pp,p))+arc_cercle(R,3,direc(R,p))+P(p,lab,'above right','otGreenDark')
    t+=sol(s)
    dessin('dis-12',t,'Sur le plan, 1 cm représente 1 m ; les arcs de construction figurent en vert au corrigé.')
    META['dis-12']={'type':'intersections','centres':[Pp,R],'rayons':[4,3],'points':Tt}
    O=(0,0);F={'F1':polar(O,30,2),'F2':polar(O,150,2.75),'F3':polar(O,260,2.5)}
    t=sol(rf'\fill[otGreen!18]{C(O)}circle(2.5);\draw[geoReponse]{C(O)}circle(2.5);')+rf'\fill[otInk]{C(O)}circle(2pt);'+L(O,'O','below')
    for k,p in F.items():t+=rf'\fill[otOrange]{C(p)}circle(2.2pt);'+T(p,k,'right',r'\scriptsize')
    dessin('dis-13',t,'Le piquet O et les trois fleurs ; sur le plan, 1 cm représente 2 m.')
    META['dis-13']={'type':'distances','O':O,'r':2.5,'points':F,'echelle':2}
    k=.6;A=(0,0);B=(6,0);M=(3,0)
    t=rf'\begin{{scope}}[scale={k}]'+cercle(A,3)+cercle(B,3)+seg(A,B)+P(A,'A','below')+P(B,'B','below')+P(M,'M','above')+r'\end{scope}'
    dessin('dis-14',t,'Deux cercles de même rayon, 3 cm ; figure réduite.')
    META['dis-14']={'type':'tangence','A':A,'B':B,'r':3,'M':M}
    A=(0,0);B=(4,0);M=(2,sqrt(5));I=(2,0)
    t=seg(A,B)+seg(M,A)+seg(M,B)+marque(M,A)+marque(M,B)+marque(A,I,2,'otOrange!80!black')+marque(I,B,2,'otOrange!80!black')
    t+=P(A,'A','below left')+P(B,'B','below right')+P(M,'M','above')+P(I,'I','below')+T(add(mid(A,M),(-.25,.1)),'3 cm','left',r'\scriptsize')+T(add(mid(B,M),(.25,.1)),'3 cm','right',r'\scriptsize')
    dessin('dis-15',t,'Le point M est à 3 cm de A et à 3 cm de B ; I est le milieu de [AB].')
    META['dis-15']={'type':'equidistance','A':A,'B':B,'M':M,'I':I}

# ================================================================= chapitre 14 : médiatrice
def mediatrices():
    A=(0,0);B=(5,0);I=(2.5,0);E,F=inter_cc(A,3.2,B,3.2)
    t=seg(A,B)+seg((2.5,-2.3),(2.5,2.3))+marque(A,I)+marque(I,B)+droit(I,B,(2.5,1))+P(A,'A','below left')+P(B,'B','below right')+P(I,'I','below right')+L((2.5,2.3),'(d)','right')
    for p in (E,F):t+=arc_cercle(A,3.2,direc(A,p),10,'otGreenDark,line width=.6pt')+arc_cercle(B,3.2,direc(B,p),10,'otGreenDark,line width=.6pt')+rf'\fill[otGreenDark]{C(p)}circle(1.4pt);'
    dessin('cours-mediatrice',t,'La médiatrice (d) de [AB], codée ; les arcs verts montrent la construction au compas.')
    META['cours-mediatrice']={'type':'mediatrice','A':A,'B':B,'points':[E,F]}
    A=(0,0);B=(5,0);M=(2.5,2.2);N=(4.2,1.7)
    t=seg(A,B)+seg((2.5,-.8),(2.5,2.8),'otNavy,line width=.6pt')+L((2.5,2.8),'(d)','right')+marque(A,(2.5,0))+marque((2.5,0),B)+droit((2.5,0),B,(2.5,1),.2)
    t+=seg(M,A,'otGreenDark')+seg(M,B,'otGreenDark')+marque(M,A,2,'otGreenDark')+marque(M,B,2,'otGreenDark')+seg(N,A,'otMuted,dashed')+seg(N,B,'otMuted,dashed')
    t+=P(A,'A','below left')+P(B,'B','below right')+P(M,'M','above left')+P(N,'N','right')
    dessin('cours-equidistance',t,'M est sur la médiatrice : $MA=MB$. N n’y est pas : $NA\\ne NB$.')
    META['cours-equidistance']={'type':'equidistance','A':A,'B':B,'M':M,'N':N}
    A=(0,0);B=(6,0)
    lines={'d_1':((1.8,-1.6),(1.8,1.6),'above'),'d_2':(polar((3,0),235,1.6),polar((3,0),55,1.6),'above right'),'d_3':((3,-1.6),(3,1.6),'above'),'d_4':(polar((5.2,0),250,1.6),polar((5.2,0),70,1.6),'above')}
    t=seg(A,B)+P(A,'A','below left')+P(B,'B','below right')
    for k,(a,b,w) in lines.items():t+=seg(a,b,'otNavy,line width=.6pt')+L(b if w!='below' else b,'('+k+')',w)
    dessin('med-1',t,'Quatre droites qui coupent le segment [AB] de 6 cm.')
    META['med-1']={'type':'mediatrice_choix','A':A,'B':B,'droites':{k:(a,b) for k,(a,b,_) in lines.items()}}
    A=(0,0);B=polar(A,15,5);I=mid(A,B);u=unit(A,B);n=(-u[1],u[0])
    t=seg(A,B)+seg(add(I,mul(n,-1.6)),add(I,mul(n,1.8)))+P(A,'A','below')+P(B,'B','below')+L(add(I,mul(n,1.8)),'(d)','right')
    t+=sol(marque(A,I,1,'otGreenDark')+marque(I,B,1,'otGreenDark')+droit(I,B,add(I,n),.22,'otGreenDark'))
    dessin('med-2',t,'La droite (d) est la médiatrice du segment [AB] ; les codages figurent en vert au corrigé.')
    META['med-2']={'type':'mediatrice','A':A,'B':B,'points':[add(I,mul(n,-1.6)),add(I,mul(n,1.8))]}
    A=(0,0);B=(6,0);I=(3,0)
    t=seg(A,B)+P(A,'A','below left')+P(B,'B','below right')+sol(P(I,'I','below right','otGreenDark')+seg((3,-1.5),(3,1.8),'geoReponse')+marque(A,I,1,'otGreenDark')+marque(I,B,1,'otGreenDark')+droit(I,B,(3,1),.22,'otGreenDark'))
    dessin('med-3',t,'Le segment [AB] de 6 cm ; la construction figure en vert au corrigé.')
    META['med-3']={'type':'mediatrice','A':A,'B':B,'points':[(3,-1.5),(3,1.8)]}
    A=(0,0);B=(4,0);M=(2,sqrt(4.2**2-4))
    t=seg(A,B)+seg((2,-.6),(2,M[1]+.6),'otNavy,line width=.6pt')+marque(A,(2,0))+marque((2,0),B)+droit((2,0),B,(2,1),.2)+L((2,M[1]+.6),'(d)','right')
    t+=seg(M,A)+seg(M,B,'otMuted,dashed')+P(A,'A','below left')+P(B,'B','below right')+P(M,'M','above left')+T(mid(A,M),'4,2 cm','left',r'\scriptsize')+T(mid(M,B),answer('4,2 cm'),'right',r'\scriptsize')
    dessin('med-4',t,'La droite (d) est la médiatrice de [AB] ; M est sur (d).')
    META['med-4']={'type':'equidistance','A':A,'B':B,'M':M,'N':None}
    A=(0,0);B=(4,0);Pp=(2,sqrt(3.5**2-4));Q=inter_cc(A,3,B,4)[1]
    t=seg(A,B)+seg(Pp,A)+seg(Pp,B)+seg(Q,A)+seg(Q,B)+P(A,'A','left')+P(B,'B','right')+P(Pp,'P','above')+P(Q,'Q','below')
    t+=T(mid(A,Pp),'3,5 cm','left',r'\scriptsize')+T(mid(B,Pp),'3,5 cm','right',r'\scriptsize')+T(mid(A,Q),'3 cm','left',r'\scriptsize')+T(mid(B,Q),'4 cm','right',r'\scriptsize')
    t+=sol(seg((2,-3.2),(2,3.6),'geoAide'))
    dessin('med-5',t,'Figure à main levée ; les longueurs indiquées font foi.')
    META['med-5']={'type':'equidistance','A':A,'B':B,'M':Pp,'N':Q}
    Cc=(0,0);D=(5,0);E,F=inter_cc(Cc,4,D,4)
    t=seg(Cc,D)+P(Cc,'C','left')+P(D,'D','right')+sol(''.join(arc_cercle(Cc,4,direc(Cc,p),9,'otGreenDark,line width=.6pt')+arc_cercle(D,4,direc(D,p),9,'otGreenDark,line width=.6pt') for p in (E,F))+P(E,'E','above right','otGreenDark')+P(F,'F','below right','otGreenDark')+ligne(E,F,.3,'geoReponse'))
    dessin('med-6',t,'Le segment [CD] de 5 cm ; la construction au compas figure en vert au corrigé.')
    META['med-6']={'type':'mediatrice','A':Cc,'B':D,'points':[E,F]}
    B=(0,0);Cc=(6,0);A=(3,4)
    t=tri(B,Cc,A,('B','C','A'),('below left','below right','above'))+marque(A,B)+marque(A,Cc)+sol(seg((3,-.8),(3,4.6),'geoAide')+marque(B,(3,0),2,'otGreenDark')+marque((3,0),Cc,2,'otGreenDark')+droit((3,0),Cc,(3,1),.22,'otGreenDark'))
    dessin('med-7',t,'Le triangle ABC, avec $AB=AC=5$ cm et $BC=6$ cm.')
    META['med-7']={'type':'equidistance','A':B,'B':Cc,'M':A,'N':None}
    A=(0,0);Cc=(6,0);B=(3,sqrt(7));D=(3,-sqrt(7))
    t=poly([A,B,Cc,D])+seg(A,Cc,'otNavy,line width=.6pt')+''.join(marque(p,q) for p,q in [(A,B),(B,Cc),(Cc,D),(D,A)])+L(A,'A','left')+L(B,'B','above')+L(Cc,'C','right')+L(D,'D','below')
    t+=sol(ligne(B,D,.5,'geoReponse')+droit((3,0),Cc,B,.22,'otGreenDark')+marque(A,(3,0),2,'otGreenDark')+marque((3,0),Cc,2,'otGreenDark'))
    dessin('med-8',t,'Le losange ABCD : ses quatre côtés ont la même longueur.')
    META['med-8']={'type':'losange','points':[A,B,Cc,D]}
    A=(0,2.2);B=(3,3.2);M=(2.4,0);I=mid(A,B)
    t=seg((-1,0),(7,0))+L((7,0),'(d)','above')+P(A,'A','left')+P(B,'B','above')+sol(ligne(I,M,.8,'geoAide')+P(M,'M','below','otGreenDark')+seg(M,A,'otGreenDark,dashed')+seg(M,B,'otGreenDark,dashed'))
    dessin('med-9',t,'Les points A et B et la droite (d) ; la construction figure en vert au corrigé.')
    META['med-9']={'type':'equidistance','A':A,'B':B,'M':M,'N':None}
    k=.75;A=(0,0);B=(4,0);O1=(2,1);O2=(2,-1.5)
    t=rf'\begin{{scope}}[scale={k}]'+P(A,'A','left')+P(B,'B','right')+rf'\draw[otMuted,<->](0,-.35)--(4,-.35);'+T((2,-.35),'4 cm','below',r'\tiny')
    t+=sol(seg((2,-4.2),(2,3.4),'geoAide')+cercle(O1,dist(O1,A),'geoReponse')+cercle(O2,dist(O2,A),'geoReponse')+P(O1,'O_1','right','otGreenDark')+P(O2,'O_2','right','otGreenDark'))+r'\end{scope}'
    dessin('med-10',t,'Les points A et B ; deux cercles solutions figurent en vert au corrigé (figure réduite).')
    META['med-10']={'type':'cercles_AB','A':A,'B':B,'centres':[O1,O2]}
    A=(1.5,2.2);B=(6,-1.6);I=mid(A,B);u=unit(A,B);S=inter_ll(I,(-u[1],u[0]),(0,0),(1,0))
    t=rf'\fill[otMuted!25](-.5,-.25)rectangle(9,.25);\draw[otMuted](-.5,0)--(9,0);'+L((9,0),'(d)','above')
    for p,lab in [(A,'A'),(B,'B')]:t+=rf'\filldraw[draw=otNavy,fill=otOrange!30]{C(add(p,(-.2,-.15)))}rectangle{C(add(p,(.2,.15)))};'+L(p,lab,'above right')
    t+=sol(ligne(I,S,1.2,'geoAide')+P(S,'S','below right','otGreenDark')+seg(S,A,'otGreenDark,dashed')+seg(S,B,'otGreenDark,dashed'))
    dessin('med-11',t,'La route (d) et les maisons A et B.')
    META['med-11']={'type':'equidistance','A':A,'B':B,'M':S,'N':None}
    A=(0,0);B=(3,1)
    t=sol(r'\fill[otGreen!25](-1.5,-1.5)--(2.1667,-1.5)--(0.8333,2.5)--(-1.5,2.5)--cycle;\draw[geoReponse](2.1667,-1.5)--(0.8333,2.5);')+rf'\draw[otMuted](-1.5,-1.5)rectangle(4.5,2.5);'+P(A,'A','below')+P(B,'B','below')
    dessin('med-12',t,'Le cadre représente une partie du plan ; la zone demandée figure en vert au corrigé.')
    META['med-12']={'type':'demi_plan','A':A,'B':B,'frontiere':[(2.1667,-1.5),(0.8333,2.5)]}
    A=(1.5,1);B=(5,3);I=mid(A,B);u=unit(A,B);n=(-u[1],u[0])
    t=rf'\filldraw[draw=otMuted,fill=otNavy!4](0,0)rectangle(7,4);'+P(A,'A','below')+P(B,'B','above')+rf'\draw[otOrange,->,dashed,line width=.7pt]{C(add(A,(.1,.15)))}to[bend left=35]{C(add(B,(-.15,-.1)))};'
    t+=sol(seg((4.3929,0),(2.1071,4),'geoReponse,dashed'))
    dessin('med-13',t,'On plie la feuille pour amener A sur B ; le pli figure en vert au corrigé.')
    META['med-13']={'type':'mediatrice','A':A,'B':B,'points':[(4.3929,0),(2.1071,4)]}
    k=.6;A=(0,0);B=(4,0);Cc=(2,sqrt(21));D=(2,-sqrt(12.25-4))
    t=rf'\begin{{scope}}[scale={k}]'+seg(A,B)+seg((2,-3.6),(2,5.2),'otNavy,line width=.6pt')+L((2,5.2),'(d)','right')+marque(A,(2,0))+marque((2,0),B)+droit((2,0),B,(2,1),.3)
    t+=seg(Cc,A)+seg(Cc,B,'otMuted,dashed')+seg(D,A)+seg(D,B)+P(A,'A','left')+P(B,'B','right')+P(Cc,'C','left')+P(D,'D','left')
    t+=T(mid(A,Cc),'5 cm','left',r'\scriptsize')+T(mid(B,Cc),answer('5 cm'),'right',r'\scriptsize')+T(mid(A,D),'3,5 cm','below left',r'\scriptsize')+T(mid(B,D),'3,5 cm','below right',r'\scriptsize')+r'\end{scope}'
    dessin('med-14',t,'Figure réduite ; les longueurs indiquées font foi.')
    META['med-14']={'type':'equidistance','A':A,'B':B,'M':Cc,'N':D}
    A=(0,0);B=(4,0);M=(2,2.3);I=(2,0)
    t=seg(A,B)+seg((2,-.7),(2,3.1),'otNavy,dashed,line width=.6pt')+seg(M,A)+seg(M,B)+marque(M,A)+marque(M,B)+marque(A,I,2,'otOrange!80!black')+marque(I,B,2,'otOrange!80!black')
    t+=P(A,'A','below left')+P(B,'B','below right')+P(M,'M','above left')+P(I,'I','below right')
    dessin('med-15',t,'M et I sont tous deux à égale distance de A et de B.')
    META['med-15']={'type':'equidistance','A':A,'B':B,'M':M,'N':None}

# ================================================================= chapitre 15 : angles
def rapporteur(R=3.0):
    t=rf'\fill[otNavy!5]({R},0)arc(0:180:{R})--cycle;\draw[otNavy!55,line width=.5pt]({R},0)arc(0:180:{R})--cycle;'
    t+=rf'\foreach \a in {{0,...,180}}{{\draw[otNavy!45,line width=.15pt](\a:{R})--(\a:{R-.1});}}'
    t+=rf'\foreach \a in {{0,5,...,180}}{{\draw[otNavy!55,line width=.25pt](\a:{R})--(\a:{R-.18});}}'
    t+=rf'\foreach \a in {{0,10,...,180}}{{\draw[otNavy!70,line width=.4pt](\a:{R})--(\a:{R-.28});\node[font=\fontsize{{4.6}}{{5}}\selectfont,text=otNavy]at(\a:{R-.45}){{\a}};\pgfmathtruncatemacro\b{{180-\a}}\node[font=\fontsize{{4.6}}{{5}}\selectfont,text=otMuted]at(\a:{R-.78}){{\b}};}}'
    t+=rf'\draw[otNavy!60,line width=.4pt](-.2,0)--(.2,0) (0,0)--(0,.2);\draw[otNavy!40,line width=.3pt](0,0)circle({R*.2});'
    return t
def angles():
    O=(0,0);t=rapporteur()+seg(O,polar(O,0,3.8),'otNavy,line width=1pt')+seg(O,polar(O,50,3.8),'otNavy,line width=1pt')+arcang(O,0,50,.75,'otGreenDark')
    t+=P(O,'O','below')+L(polar(O,0,3.8),'A','right')+L(polar(O,50,3.8),'B','above')
    dessin('cours-rapporteur',t,'Le centre du rapporteur est sur le sommet O ; le côté [OA) passe par le 0 de la graduation extérieure : $\\widehat{AOB}=50^\\circ$.')
    META['cours-rapporteur']={'type':'angles','mesures':[50]}
    O=(0,0);t=ligne(polar(O,180,2),polar(O,0,2),.2)+ligne(polar(O,220,2),polar(O,40,2),.2)+P(O,'O','below')
    t+=arcang(O,0,40,.55,'otNavy',r'$40^\circ$')+arcang(O,40,180,.7,'otGreenDark',r'$140^\circ$')+arcang(O,180,220,.55,'otNavy',r'$40^\circ$')
    O2=(6.8,-.8);M=polar(O2,0,1.6);N=polar(O2,70,1.6);Pp=[p for p in inter_cc(M,1.5,N,1.5) if dist(p,O2)>1][0]
    t+=seg(O2,polar(O2,0,3))+seg(O2,polar(O2,70,3))+P(O2,'O','below')+arcang(O2,-5,75,1.6,'otGreenDark,line width=.5pt')
    t+=arc_cercle(M,1.5,direc(M,Pp),10,'otGreenDark,line width=.5pt')+arc_cercle(N,1.5,direc(N,Pp),10,'otGreenDark,line width=.5pt')+P(Pp,'P','right','otGreenDark')+demi(O2,Pp,.6,'geoReponse')
    dessin('cours-paires-bissectrice',t,'À gauche : angles opposés égaux et angles supplémentaires. À droite : bissectrice construite au compas.')
    META['cours-paires-bissectrice']={'type':'bissectrice','O':O2,'P':Pp,'angle':70}
    O=(0,0);A=polar(O,0,2.8);B=polar(O,55,2.8)
    t=seg(O,A)+seg(O,B)+arcang(O,0,55,.7,'otGreenDark,line width=1.2pt')+P(O,'O','below left')+P(A,'A','below')+P(B,'B','left')
    dessin('ang-1',t,'L’angle marqué en vert.')
    META['ang-1']={'type':'angles','mesures':[angle_en(O,A,B)]}
    ms=[25,90,130,180,70];xs=[0,2.4,5.2,8.2,10.5];t=''
    for k,(m,x) in enumerate(zip(ms,xs)):
        V=(x,0);r=1.1 if m!=180 else 1.0
        t+=seg(V,polar(V,0,r))+seg(V,polar(V,m,r))+rf'\fill[otNavy]{C(V)}circle(1.2pt);'
        t+=droit(V,(x+1,0),(x,1),.2) if m==90 else arcang(V,0,m,.35,'otGreenDark')
        t+=T((x+(.3 if m<180 else 0),-.15),'abcde'[k],'below',r'\scriptsize')
    dessin('ang-2',t,'Cinq angles, de sommets différents.')
    META['ang-2']={'type':'angles','mesures':ms}
    O=(0,0);t=rapporteur()+seg(O,polar(O,0,3.8),'otNavy,line width=1pt')+seg(O,polar(O,70,3.8),'otNavy,line width=1pt')+P(O,'O','below')+L(polar(O,0,3.8),'A','right')+L(polar(O,70,3.8),'B','above')
    dessin('ang-3',t,'Le rapporteur est posé sur l’angle $\\widehat{AOB}$.')
    META['ang-3']={'type':'angles','mesures':[70]}
    t=rapporteur()+seg(O,polar(O,180,3.8),'otNavy,line width=1pt')+seg(O,polar(O,55,3.8),'otNavy,line width=1pt')+P(O,'O','below')+L(polar(O,180,3.8),'C','left')+L(polar(O,55,3.8),'D','above')
    dessin('ang-4',t,'Le rapporteur est posé sur l’angle $\\widehat{COD}$.')
    META['ang-4']={'type':'angles','mesures':[180-55]}
    t='';specs=[((0,0),10,100,'a'),((3.4,-.3),-20,45,'b'),((6.6,.2),5,160,'c')];ms=[]
    for V,a0,m,lab in specs:
        t+=seg(V,polar(V,a0,1.6))+seg(V,polar(V,a0+m,1.6))+rf'\fill[otNavy]{C(V)}circle(1.2pt);'+arcang(V,a0,a0+m,.4,'otGreenDark')+T(polar(V,a0+m/2,.75),lab,'',r'\scriptsize')
        ms.append(m)
    dessin('ang-5',t,'Trois angles a, b et c, dans des positions différentes.')
    META['ang-5']={'type':'angles','mesures':ms}
    A=(0,0);t=seg(A,(4,0))+P(A,'A','below left')+L((4,0),'x','right')+sol(seg(A,polar(A,65,3.6),'geoReponse')+arcang(A,0,65,.7,'otGreenDark',r'$65^\circ$')+L(polar(A,65,3.6),'y','above'))
    dessin('ang-6',t,'La demi-droite [Ax) ; l’angle construit figure en vert au corrigé.')
    META['ang-6']={'type':'angles','mesures':[65]}
    t=''
    O=(0,0);t+=seg(O,polar(O,0,1.6))+seg(O,polar(O,45,1.6))+seg(O,polar(O,110,1.6))+arcang(O,0,45,.45,'otNavy')+arcang(O,45,110,.55,'otGreenDark')+T((.6,-.2),'1','below',r'\scriptsize')
    O=(4.0,0);t+=seg(O,polar(O,0,1.6))+seg(O,polar(O,35,1.6))+seg(O,polar(O,100,1.6))+arcang(O,0,100,.75,'otNavy')+arcang(O,0,35,.45,'otGreenDark')+T((4.6,-.2),'2','below',r'\scriptsize')
    O1=(7.8,0);O2=(9.4,0);t+=seg(O1,polar(O1,0,2.6))+seg(O1,polar(O1,60,1.6))+seg(O2,polar(O2,120,1.4))+arcang(O1,0,60,.45,'otNavy')+arcang(O2,120,180,.45,'otGreenDark')+T((8.7,-.2),'3','below',r'\scriptsize')
    dessin('ang-7',t,'Dans chaque figure, deux angles sont marqués, l’un en bleu, l’autre en vert.')
    META['ang-7']={'type':'libre'}
    O=(0,0);A=(-3,0);B=(3,0);Cc=polar(O,52,2.8)
    t=seg(A,B)+seg(O,Cc)+P(O,'O','below')+P(A,'A','below')+P(B,'B','below')+P(Cc,'C','above right')+arcang(O,52,180,.6,'otNavy',r'$128^\circ$')+arcang(O,0,52,.95,'otGreenDark',answer(r'$52^\circ$'),1.35)
    dessin('ang-8',t,'Les points A, O et B sont alignés.')
    META['ang-8']={'type':'angles','mesures':[180-52,52]}
    O=(0,0);t=seg((-2.6,0),(2.6,0))+seg(polar(O,227,2.6),polar(O,47,2.6))+P(O,'O','below right')
    t+=arcang(O,0,47,.6,'otNavy',r'$47^\circ$')+arcang(O,47,180,.6,'otGreenDark',answer(r'$133^\circ$'),1.05)+arcang(O,180,227,.6,'otGreenDark',answer(r'$47^\circ$'),1.05)+arcang(O,227,360,.6,'otGreenDark',answer(r'$133^\circ$'),1.05)
    dessin('ang-9',t,'Deux droites sécantes en O.')
    META['ang-9']={'type':'angles','mesures':[47,133,47,133]}
    O=(0,0);t=seg(O,polar(O,0,3.2))+seg(O,polar(O,84,3.2))+arcang(O,0,84,.6,'otNavy',r'$84^\circ$',.95)+P(O,'O','below left')+L(polar(O,0,3.2),'x','right')+L(polar(O,84,3.2),'y','above')
    t+=sol(seg(O,polar(O,42,3.4),'geoReponse')+arcang(O,0,42,1.5,'otGreenDark',r'$42^\circ$',1.9)+arcang(O,42,84,1.5,'otGreenDark',r'$42^\circ$',1.9))
    dessin('ang-10',t,'L’angle $\\widehat{xOy}$ ; la bissectrice figure en vert au corrigé.')
    META['ang-10']={'type':'angles','mesures':[84,42]}
    O=(0,0);rays=[0,110,205,285];t=''.join(seg(O,polar(O,a,2.1)) for a in rays)+P(O,'O','below left')
    for a1,a2,lab,lr in [(0,110,r'$110^\circ$',None),(110,205,r'$95^\circ$',None),(205,285,r'$80^\circ$',None),(285,360,answer(r'$75^\circ$'),1.1)]:t+=arcang(O,a1,a2,.55,'otNavy' if lr is None else 'otGreenDark',lab,lr)
    dessin('ang-11',t,'Quatre angles adjacents autour du point O.')
    META['ang-11']={'type':'angles','mesures':[110,95,80,75]}
    q,ah,am=horloge(0,4,0,r=1.6);t=q+sol(arcang((0,0),ah,am,.45,'otGreenDark')+rf'\draw[otGreenDark,line width=.5pt]{C(polar((0,0),30,.5))}--(2.2,1.0);'+T((2.2,1.0),r'$120^\circ$','right',r'\small','otGreenDark'))
    dessin('ang-12',t,'L’horloge indique 4 h ; l’angle des aiguilles figure en vert au corrigé.')
    META['ang-12']={'type':'angles','mesures':[(am-ah)%360]}
    O=(0,0);M=polar(O,0,1.8);N=polar(O,70,1.8);Pp=[p for p in inter_cc(M,1.6,N,1.6) if dist(p,O)>1][0]
    t=seg(O,polar(O,0,3.6))+seg(O,polar(O,70,3.6))+arcang(O,0,70,.5,'otNavy',r'$70^\circ$',.85)+P(O,'O','below left')+L(polar(O,0,3.6),'x','right')+L(polar(O,70,3.6),'y','above')
    t+=sol(arcang(O,-6,76,1.8,'otGreenDark,line width=.5pt')+P(M,'M','below right','otGreenDark')+P(N,'N','left','otGreenDark')+arc_cercle(M,1.6,direc(M,Pp),10,'otGreenDark,line width=.5pt')+arc_cercle(N,1.6,direc(N,Pp),10,'otGreenDark,line width=.5pt')+P(Pp,'P','right','otGreenDark')+demi(O,Pp,1.0,'geoReponse'))
    dessin('ang-13',t,'L’angle $\\widehat{xOy}$ de $70^\\circ$ ; la construction au compas figure en vert au corrigé.')
    META['ang-13']={'type':'bissectrice','O':O,'P':Pp,'angle':70}
    O=(0,0);A=(-3,0);B=(3,0);Cc=polar(O,50,2.8)
    t=seg(A,B)+seg(O,Cc)+P(O,'O','below')+P(A,'A','below')+P(B,'B','below')+P(Cc,'C','above right')+arcang(O,50,180,.55,'otNavy',r'$130^\circ$')+arcang(O,0,50,.8,'otNavy',r'$50^\circ$',1.15)
    t+=sol(seg(O,polar(O,25,2.7),'geoReponse')+seg(O,polar(O,115,2.7),'geoReponse')+droit(O,polar(O,25,1),polar(O,115,1),.25,'otGreenDark'))
    dessin('ang-14',t,'Les points A, O et B sont alignés ; les bissectrices figurent en vert au corrigé.')
    META['ang-14']={'type':'angles','mesures':[130,50,90]}
    V=(0,0);W=(5.6,0)
    t=seg(V,polar(V,0,4))+seg(V,polar(V,40,4))+arcang(V,0,40,.5,'otGreenDark')+T(polar(V,20,.85),'a','',r'\scriptsize')
    t+=seg(W,polar(W,0,1.3))+seg(W,polar(W,60,1.3))+arcang(W,0,60,.4,'otGreenDark')+T(polar(W,30,.7),'b','',r'\scriptsize')
    dessin('ang-15',t,'Deux angles dessinés avec des côtés de longueurs différentes.')
    META['ang-15']={'type':'angles','mesures':[40,60]}

# ================================================================= chapitre 16 : triangles
def triangles():
    A=(0,0);B=(6,0);Cc=inter_cc(A,4,B,5)[0]
    t=seg(A,B)+seg(A,Cc,'otNavy,line width=.7pt')+seg(B,Cc,'otNavy,line width=.7pt')+arc_cercle(A,4,direc(A,Cc),14,'otGreenDark,line width=.6pt')+arc_cercle(B,5,direc(B,Cc),12,'otGreenDark,line width=.6pt')
    t+=L(A,'A','below left')+L(B,'B','below right')+L(Cc,'C','above')+T((3,0),'6 cm','below',r'\scriptsize')+T(mid(A,Cc),'4 cm','left',r'\scriptsize')+T(mid(B,Cc),'5 cm','right',r'\scriptsize')
    dessin('cours-construction-triangle',t,'Les deux arcs de cercle se coupent en C.')
    META['cours-construction-triangle']={'type':'triangle','points':[A,B,Cc],'cotes':[6,4,5]}
    def coins(A,B,Cc,Q,cols=('otNavy!35','otGreen!45','otOrange!45')):
        a=angle_en(A,B,Cc);b=angle_en(B,A,Cc);c=180-a-b
        t=poly([A,B,Cc],fill='otNavy!5')+arc_at(A,B,Cc,.55,'otNavy',fill=cols[0])+arc_at(B,Cc,A,.55,'otNavy',fill=cols[1])+arc_at(Cc,A,B,.5,'otNavy',fill=cols[2])
        t+=seg((Q[0]-1.6,Q[1]),(Q[0]+1.6,Q[1]),'otMuted')+arcang(Q,0,a,.8,'otNavy',fill=cols[0])+arcang(Q,a,a+c,.8,'otNavy',fill=cols[2])+arcang(Q,a+c,180,.8,'otNavy',fill=cols[1])
        return t,(a,b,c)
    t,abc=coins((0,0),(4,0),(1.2,2.4),(7,.2))
    t+=T((7,1.1),'angle plat : $180^\\circ$','above',r'\scriptsize')
    dessin('cours-somme-angles',t,'Les trois angles du triangle, placés côte à côte, forment un angle plat.')
    META['cours-somme-angles']={'type':'somme','angles':list(abc)}
    A=(0,0);B=(5,0);Cc=(1.5,3);O=circumcenter(A,B,Cc)
    t=tri(A,B,Cc)+''.join(ligne(mid(p,q),O,.9,'otMuted,dashed') for p,q in [(A,B),(B,Cc),(A,Cc)])+cercle(O,dist(O,A),'geoReponse')+P(O,'O','right','otGreenDark')
    dessin('cours-cercle-circonscrit',t,'Les trois médiatrices, en tirets, se coupent en O, centre du cercle circonscrit.')
    META['cours-cercle-circonscrit']={'type':'circonscrit','points':[A,B,Cc],'O':O}
    A=(0,0);B=(5,0);Cc=polar(A,48,5*sin(radians(67))/sin(radians(65)))
    t=tri(A,B,Cc)+arc_at(A,B,Cc,.6,'otNavy',r'$48^\circ$',.95)+arc_at(B,Cc,A,.6,'otNavy',r'$67^\circ$',.95)+arc_at(Cc,A,B,.5,'otGreenDark',answer(r'$65^\circ$'),.95)
    dessin('tri-1',t,'Figure de principe ; les mesures indiquées font foi.')
    META['tri-1']={'type':'triangle','points':[A,B,Cc],'angles':[48,67,65]}
    k=.55;B=(0,0);Cc=(4,0);A=(2,2/tan(radians(20)))
    t=rf'\begin{{scope}}[scale={k}]'+tri(B,Cc,A,('B','C','A'),('below left','below right','above'))+marque(A,B)+marque(A,Cc)+arc_at(A,B,Cc,1.0,'otNavy',r'$40^\circ$',1.65)+arc_at(B,Cc,A,.8,'otGreenDark',answer(r'$70^\circ$'),1.5)+arc_at(Cc,A,B,.8,'otGreenDark',answer(r'$70^\circ$'),1.5)+r'\end{scope}'
    dessin('tri-2',t,'Le triangle ABC est isocèle en A ; figure réduite.')
    META['tri-2']={'type':'triangle','points':[A,B,Cc],'angles':[40,70,70]}
    A=(0,0);B=(4,0);Cc=(2,2*sqrt(3))
    t=tri(A,B,Cc)+marque(A,B)+marque(B,Cc)+marque(A,Cc)+T((2,0),'4 cm','below',r'\scriptsize')+''.join(arc_at(V,p,q,.45,'otGreenDark',answer(r'$60^\circ$'),.9) for V,p,q in [(A,B,Cc),(B,Cc,A),(Cc,A,B)])
    dessin('tri-3',t,'Un triangle équilatéral de 4 cm de côté.')
    META['tri-3']={'type':'triangle','points':[A,B,Cc],'angles':[60,60,60]}
    Cc=(0,0);A=(4,0);B=(0,4*tan(radians(35)))
    t=tri(A,B,Cc,('A','B','C'),('below right','above','below left'))+droit(Cc,A,B,.25)+arc_at(A,B,Cc,.7,'otNavy',r'$35^\circ$',1.15)+arc_at(B,Cc,A,.55,'otGreenDark',answer(r'$55^\circ$'),.95)
    dessin('tri-4',t,'Le triangle ABC est rectangle en C.')
    META['tri-4']={'type':'triangle','points':[A,B,Cc],'angles':[35,55,90]}
    A=(0,0);B=(6,0);Cc=inter_cc(A,4,B,5)[0]
    t=seg(A,B)+L(A,'A','below left')+L(B,'B','below right')+T((3,0),'6 cm','below',r'\scriptsize')
    t+=sol(seg(A,Cc,'geoReponse')+seg(B,Cc,'geoReponse')+arc_cercle(A,4,direc(A,Cc),14,'otGreenDark,line width=.6pt')+arc_cercle(B,5,direc(B,Cc),12,'otGreenDark,line width=.6pt')+P(Cc,'C','above','otGreenDark')+T(mid(A,Cc),'4 cm','left',r'\scriptsize','otGreenDark')+T(mid(B,Cc),'5 cm','right',r'\scriptsize','otGreenDark'))
    dessin('tri-5',t,'Le côté [AB] ; la construction figure en vert au corrigé.')
    META['tri-5']={'type':'triangle','points':[A,B,Cc],'cotes':[6,4,5]}
    k=.55;A=(0,0);B=(8,0)
    t=rf'\begin{{scope}}[scale={k}]'+seg(A,B)+cercle(A,3,'otMuted,dashed')+cercle(B,4,'otMuted,dashed')+L(A,'A','below left')+L(B,'B','below right')+T((4,0),'8 cm','below',r'\scriptsize')+T(polar(A,60,3),'rayon 3 cm','above right',r'\tiny')+T(polar(B,120,4),'rayon 4 cm','above left',r'\tiny')+r'\end{scope}'
    dessin('tri-6',t,'Pour 3 cm, 4 cm et 8 cm, les cercles de construction ne se rencontrent pas (figure réduite).')
    META['tri-6']={'type':'impossible','cotes':[3,4,8],'intersections':len(inter_cc(A,3,B,4))}
    A=(0,0);B=(5,0);Cc=polar(A,60,3)
    t=seg(A,B)+L(A,'A','below left')+L(B,'B','below right')+T((2.5,0),'5 cm','below',r'\scriptsize')
    t+=sol(demi(A,Cc,.9,'geoAide')+seg(A,Cc,'geoReponse')+seg(B,Cc,'geoReponse')+arcang(A,0,60,.6,'otGreenDark',r'$60^\circ$',.95)+P(Cc,'C','above left','otGreenDark')+T(mid(A,Cc),'3 cm','left',r'\scriptsize','otGreenDark'))
    dessin('tri-7',t,'Le côté [AB] ; la construction figure en vert au corrigé.')
    META['tri-7']={'type':'triangle','points':[A,B,Cc],'cotes':[5,3],'angles':[60]}
    B=(0,0);Cc=(6,0);A=polar(B,50,6*sin(radians(60))/sin(radians(70)))
    t=seg(B,Cc)+L(B,'B','below left')+L(Cc,'C','below right')+T((3,0),'6 cm','below',r'\scriptsize')
    t+=sol(seg(B,A,'geoReponse')+seg(Cc,A,'geoReponse')+arcang(B,0,50,.6,'otGreenDark',r'$50^\circ$',.95)+arcang(Cc,120,180,.6,'otGreenDark',r'$60^\circ$',.95)+arc_at(A,B,Cc,.5,'otGreenDark',r'$70^\circ$',.9)+P(A,'A','above','otGreenDark'))
    dessin('tri-8',t,'Le côté [BC] ; la construction figure en vert au corrigé.')
    META['tri-8']={'type':'triangle','points':[A,B,Cc],'angles':[70,50,60]}
    k=.65;B=(0,0);Cc=(3,0);A=(1.5,1.5*tan(radians(72)))
    t=rf'\begin{{scope}}[scale={k}]'+tri(B,Cc,A,('B','C','A'),('below left','below right','above'))+marque(A,B)+marque(A,Cc)+arc_at(B,Cc,A,.6,'otNavy',r'$72^\circ$',1.15)+arc_at(Cc,A,B,.6,'otNavy',r'$72^\circ$',1.15)+arc_at(A,B,Cc,.9,'otGreenDark',answer(r'$36^\circ$'),1.5)+r'\end{scope}'
    dessin('tri-9',t,'Le triangle ABC est isocèle en A ; figure réduite.')
    META['tri-9']={'type':'triangle','points':[A,B,Cc],'angles':[36,72,72]}
    A=(0,0);B=(5,0);Cc=(3.6,3.0);O=circumcenter(A,B,Cc)
    t=tri(A,B,Cc)+sol(''.join(ligne(mid(p,q),O,.8,'geoAide') for p,q in [(A,B),(B,Cc),(A,Cc)])+cercle(O,dist(O,A),'geoReponse')+P(O,'O','right','otGreenDark'))
    dessin('tri-10',t,'Le triangle ABC ; la construction figure en vert au corrigé.')
    META['tri-10']={'type':'circonscrit','points':[A,B,Cc],'O':O}
    A=(0,.6);B=(5.4,0);Cc=(2.2,3.6);O=circumcenter(A,B,Cc)
    t=''
    for p,lab in [(A,'A'),(B,'B'),(Cc,'C')]:t+=rf'\filldraw[draw=otNavy,fill=otOrange!30]{C(add(p,(-.2,-.15)))}rectangle{C(add(p,(.2,.15)))};'+L(add(p,(0,.15)),lab,'above')
    t+=sol(ligne(mid(A,B),O,.8,'geoAide')+ligne(mid(B,Cc),O,.8,'geoAide')+cercle(O,dist(O,A),'geoReponse,dashed')+P(O,'O','right','otGreenDark'))
    dessin('tri-11',t,'Les trois villages vus de dessus.')
    META['tri-11']={'type':'circonscrit','points':[A,B,Cc],'O':O}
    A=(0,0);B=(4,0);Cc=(0,3);O=circumcenter(A,B,Cc)
    t=tri(A,B,Cc,('A','B','C'),('below left','below right','above left'))+droit(A,B,Cc,.25)+sol(seg((2,-.8),(2,2.5),'geoAide')+seg((-.8,1.5),(3.2,1.5),'geoAide')+cercle(O,2.5,'geoReponse')+P(O,'O','above right','otGreenDark'))
    dessin('tri-12',t,'Le triangle ABC est rectangle en A.')
    META['tri-12']={'type':'circonscrit','points':[A,B,Cc],'O':O}
    k=.6;B=(0,0);Cc=(4,0);A=(2,2*tan(radians(65)));D=add(A,(4.714,-.4125))
    D=polar(A,direc(A,Cc)+60,dist(A,Cc))
    t=rf'\begin{{scope}}[scale={k}]'+tri(B,Cc,A,('B','C','A'),('below left','below right','above'))+poly([A,Cc,D])+L(D,'D','right')+marque(A,B)+marque(A,Cc,2)+marque(Cc,D,2)+marque(D,A,2)
    t+=arc_at(B,Cc,A,.7,'otNavy',r'$65^\circ$',1.25)+arc_at(A,B,Cc,.7,'otGreenDark',answer(r'$50^\circ$'),1.3)+arc_at(A,B,D,1.5,'otGreenDark',answer(r'$110^\circ$'),2.3)+r'\end{scope}'
    dessin('tri-13',t,'ABC est isocèle en A ; ACD est équilatéral ; figure réduite.')
    META['tri-13']={'type':'triangles','points':{'A':A,'B':B,'C':Cc,'D':D}}
    B=(0,0);Cc=(4,0);A=(2,2*sqrt(3));H=(2,0)
    t=tri(B,Cc,A,('B','C','A'),('below left','below right','above'))+seg(A,H)+P(H,'H','below')+marque(A,B)+marque(B,Cc)+marque(A,Cc)
    t+=sol(arc_at(A,B,H,.8,'otGreenDark',r'$30^\circ$',1.2)+droit(H,Cc,A,.25,'otGreenDark'))
    dessin('tri-14',t,'Le triangle équilatéral ABC et la bissectrice [AH).')
    META['tri-14']={'type':'triangle','points':[A,B,H],'angles':[30,60,90]}
    A=(0,0);B=(4,0)
    t=seg(A,B)+seg(A,polar(A,100,2.6))+seg(B,polar(B,85,2.6))+L(A,'A','below left')+L(B,'B','below right')+arcang(A,0,100,.5,'otNavy',r'$100^\circ$',.95)+arcang(B,85,180,.5,'otNavy',r'$95^\circ$',.95)
    dessin('tri-15',t,'Les deux côtés tracés à partir de A et de B s’écartent l’un de l’autre.')
    META['tri-15']={'type':'angles','mesures':[100,95]}

# ================================================================= chapitre 17 : symétrie
def symetries():
    a=(-.8,-.29);b=polar((0,0),20,6.5);M=(1.8,2.4);M2=reflect(M,a,b);H=foot(M,a,b)
    t=seg(a,b,'otOrange,dashed,line width=1pt')+L(b,'(d)','right')+seg(M,M2,'otMuted,dashed')+droit(H,M,b,.22)+marque(M,H)+marque(H,M2)+P(M,'M','above')+P(M2,"M'",'below')+P(H,'H','above left')
    dessin('cours-sym-point',t,"La droite (d) est la médiatrice du segment [MM'].")
    sym_oblique_meta('cours-sym-point',a,b,[(M,M2)])
    a=polar((0,0),250,1.8);b=polar((0,0),70,3.0);A=(-2.5,.5);B=(-1,.3);Cc=(-1.8,2.0)
    imgs=[reflect(p,a,b) for p in (A,B,Cc)]
    t=seg(a,b,'otOrange,dashed,line width=1pt')+L(b,'(d)','right')+poly([A,B,Cc])+poly(imgs,'geoReponse')+''.join(seg(p,q,'otMuted,dashed,line width=.4pt') for p,q in zip((A,B,Cc),imgs))
    t+=L(A,'A','left')+L(B,'B','below')+L(Cc,'C','above')+L(imgs[0],"A'",'right')+L(imgs[1],"B'",'below')+L(imgs[2],"C'",'above')
    dessin('cours-sym-triangle',t,'Le triangle ABC et son symétrique par rapport à (d), construit sommet par sommet.')
    sym_oblique_meta('cours-sym-triangle',a,b,list(zip((A,B,Cc),imgs)))
    t='';axes=''
    t+=poly([(0,0),(2,0),(2,1.2),(0,1.2)]);axes+=seg((1,-.3),(1,1.5),'geoReponse')+seg((-.3,.6),(2.3,.6),'geoReponse')
    t+=poly([(2.8,0),(4.2,0),(4.2,1.4),(2.8,1.4)]);axes+=seg((3.5,-.3),(3.5,1.7),'geoReponse')+seg((2.5,.7),(4.5,.7),'geoReponse')+seg((2.6,-.2),(4.4,1.6),'geoReponse')+seg((2.6,1.6),(4.4,-.2),'geoReponse')
    t+=poly([(5,0),(6.6,0),(5.8,1.5)]);axes+=seg((5.8,-.3),(5.8,1.8),'geoReponse')
    t+=poly([(7.2,.7),(8.0,0),(8.8,.7),(8.0,1.4)]);axes+=seg((6.9,.7),(9.1,.7),'geoReponse')+seg((8.0,-.3),(8.0,1.7),'geoReponse')
    t+=poly([(9.5,0),(11.1,.2),(10.0,1.4)])
    for x,lab in [(1,'rectangle'),(3.5,'carré'),(5.8,'isocèle'),(8,'losange'),(10.3,'quelconque')]:t+=T((x,-.35),lab,'below',r'\tiny')
    dessin('sym-1',t+sol(axes),'Cinq figures ; leurs axes de symétrie figurent en vert au corrigé.')
    META['sym-1']={'type':'axes','nombres':[2,4,1,2,0]}
    symaxe('sym-2',[[(2,1),(4,1),(5,3),(3,5),(2,4)]],('v',6),12,6,points=[('A',1,5)])
    symaxe('sym-3',[[(3,5),(3,8)],[(3,8),(6,7),(3,6)]],('h',4),10,8,points=[('B',8,6)],closes=[False,True])
    symdiag('sym-4',[[(1,4),(3,6),(1,6)]],7,points=[('C',0,2)])
    symaxe('sym-5',[[(1,1),(3,1),(4,3),(2,5),(1,3)]],('v',5),10,6,dots=True,leg='Papier pointé : on compte les intervalles entre les points.')
    a=(-.5,-.134);b=polar((0,0),15,6.2);A=(1.2,2.4);A2=reflect(A,a,b);H=foot(A,a,b)
    t=seg(a,b,'otOrange,dashed,line width=1pt')+L(b,'(d)','right')+P(A,'A','above')+sol(seg(A,A2,'geoAide')+droit(H,A,b,.22,'otGreenDark')+marque(A,H,1,'otGreenDark')+marque(H,A2,1,'otGreenDark')+P(H,'H','above left','otGreenDark')+P(A2,"A'",'below','otGreenDark'))
    dessin('sym-6',t,'La droite (d) et le point A ; la construction figure en vert au corrigé.')
    sym_oblique_meta('sym-6',a,b,[(A,A2)])
    a=(-.3,-.46);b=(5.5,.7);A=(.5,1.8);B=add(A,polar((0,0),-10,4));A2=reflect(A,a,b);B2=reflect(B,a,b)
    t=seg(a,b,'otOrange,dashed,line width=1pt')+L(b,'(d)','right')+seg(A,B)+P(A,'A','above')+P(B,'B','above')+T(mid(A,B),'4 cm','above',r'\scriptsize')
    t+=sol(seg(A2,B2,'geoReponse')+P(A2,"A'",'below','otGreenDark')+P(B2,"B'",'below','otGreenDark')+seg(A,A2,'otGreenDark,dashed,line width=.4pt')+seg(B,B2,'otGreenDark,dashed,line width=.4pt'))
    dessin('sym-7',t,'Le segment [AB] et la droite (d).')
    sym_oblique_meta('sym-7',a,b,[(A,A2),(B,B2)])
    P0=(2.2,-1.5);u=unit(P0,add(P0,(1,1.6)));a=add(P0,mul(u,-.5));b=add(P0,mul(u,6));O=(1.5,1.6);O2=reflect(O,a,b)
    t=seg(a,b,'otOrange,dashed,line width=1pt')+L(b,'(d)','right')+cercle(O,1.5)+P(O,'O','below')+sol(cercle(O2,1.5,'geoReponse')+P(O2,"O'",'below','otGreenDark')+seg(O,O2,'otGreenDark,dashed,line width=.4pt'))
    dessin('sym-8',t,'Le cercle de centre O et de rayon 1,5 cm, et la droite (d).')
    sym_oblique_meta('sym-8',a,b,[(O,O2)])
    symaxe('sym-9',[[(4,0),(1,0),(1,4),(4,7)],[(2,1),(3,1),(3,2),(2,2)]],('v',4),8,8,closes=[False,True],leg='La droite en tirets est un axe de symétrie de la maison.')
    P0=(0,-.5);u=(cos(radians(60)),sin(radians(60)));a=add(P0,mul(u,-1));b=add(P0,mul(u,4.6))
    A=(-1.5,.5);B=(-.4,2.2);Cc=(-2.2,2.4);imgs=[reflect(p,a,b) for p in (A,B,Cc)]
    t=poly([A,B,Cc])+poly(imgs)+L(A,'A','below')+L(B,'B','above')+L(Cc,'C','left')+L(imgs[0],"A'",'below')+L(imgs[1],"B'",'above')+L(imgs[2],"C'",'right')
    t+=sol(seg(a,b,'geoReponse')+seg(A,imgs[0],'otGreenDark,dashed,line width=.4pt'))
    dessin('sym-10',t,"Le triangle ABC et son symétrique A'B'C' ; l’axe figure en vert au corrigé.")
    sym_oblique_meta('sym-10',a,b,list(zip((A,B,Cc),imgs)))
    k=.6;B=(-1,0);Cc=(-1-12/(5*sin(radians(40))),0);A=add(B,polar((0,0),140,5));imgs=[(-p[0],p[1]) for p in (A,B,Cc)]
    t=rf'\begin{{scope}}[scale={k}]'+seg((0,-.6),(0,4),'otOrange,dashed,line width=1pt')+poly([A,B,Cc])+poly(imgs)
    t+=L(A,'A','above')+L(B,'B','below')+L(Cc,'C','below')+L(imgs[0],"A'",'above')+L(imgs[1],"B'",'below')+L(imgs[2],"C'",'below')+T(mid(A,B),'5 cm','below left',r'\scriptsize')+arc_at(B,A,Cc,.8,'otNavy',r'$40^\circ$',1.4)
    t+=T(mid(imgs[0],imgs[1]),answer('5 cm'),'below right',r'\scriptsize')+arc_at(imgs[1],imgs[0],imgs[2],.8,'otGreenDark',answer(r'$40^\circ$'),1.4)+r'\end{scope}'
    dessin('sym-11',t,"Le triangle ABC et son symétrique A'B'C' (figure réduite).")
    sym_oblique_meta('sym-11',(0,-1),(0,4),list(zip((A,B,Cc),imgs)))
    P0=(2,-.5);u=unit(P0,add(P0,(.35,1)));a=add(P0,mul(u,-.3));b=add(P0,mul(u,3.6));M=(.6,.4);N=(4.8,2.6)
    I=inter_ll(M,unit(M,N),a,u);M2=reflect(M,a,b);N2=reflect(N,a,b)
    t=seg(a,b,'otOrange,dashed,line width=1pt')+L(b,'(d)','right')+seg(M,N)+P(M,'M','below')+P(N,'N','above')+P(I,'I','below right')
    t+=sol(seg(M2,N2,'geoReponse')+P(M2,"M'",'below','otGreenDark')+P(N2,"N'",'above','otGreenDark'))
    dessin('sym-12',t,'Le segment [MN] coupe la droite (d) en I.')
    sym_oblique_meta('sym-12',a,b,[(M,M2),(N,N2),(I,I)])
    META['sym-12']['alignes']=[M2,I,N2]
    A=(1.5,2.5);B=(7,1.5);A2=(1.5,-2.5);I=(1.5+2.5/4*5.5,0)
    t=rf'\fill[otGreen!25](-.3,-.25)rectangle(9,0);\draw[otNavy,line width=1.2pt](-.3,0)--(9,0);'+L((9,0),'(d)','above')+rf'\fill[otOrange]{C(A)}circle(3pt);\fill[otNavy]{C(B)}circle(3pt);'+L(A,'A','above')+L(B,'B','above')
    t+=sol(P(A2,"A'",'below','otGreenDark')+seg(A,A2,'otGreenDark,dashed,line width=.4pt')+seg(A2,I,'otGreenDark,dashed')+rf'\draw[otGreenDark,line width=1.3pt,-{{Stealth[length=2.6mm]}}]{C(A)}--{C(I)}--{C(B)};'+P(I,'I','below right','otGreenDark'))
    dessin('sym-13',t,'La bande du billard est la droite (d).')
    sym_oblique_meta('sym-13',(-.3,0),(9,0),[(A,A2)])
    META['sym-13']['alignes']=[A2,I,B]
    t='';axes=''
    def lettre(x0,segs):
        return ''.join(rf'\draw[otNavy,line width=2.2pt,line cap=round,line join=round]'+'--'.join(C((x0+x,y)) for x,y in s)+';' for s in segs)
    t+=lettre(0,[[(0,0),(0,1.4)],[(1,0),(1,1.4)],[(0,.7),(1,.7)]]);axes+=seg((.5,-.25),(.5,1.65),'geoReponse')+seg((-.25,.7),(1.25,.7),'geoReponse')
    t+=lettre(1.8,[[(0,0),(.5,1.4),(1,0)],[(.25,.7),(.75,.7)]]);axes+=seg((2.3,-.25),(2.3,1.65),'geoReponse')
    t+=lettre(3.6,[[(1,0),(0,0),(0,1.4),(1,1.4)],[(0,.7),(.8,.7)]]);axes+=seg((3.35,.7),(4.85,.7),'geoReponse')
    t+=lettre(5.4,[[(0,0),(0,1.4),(1,0),(1,1.4)]])
    t+=lettre(7.2,[[(0,0),(1,1.4)],[(0,1.4),(1,0)]]);axes+=seg((7.7,-.25),(7.7,1.65),'geoReponse')+seg((6.95,.7),(8.45,.7),'geoReponse')
    dessin('sym-14',t+sol(axes),'Cinq lettres dessinées en bâtons ; les axes figurent en vert au corrigé.')
    META['sym-14']={'type':'axes','nombres':[2,1,1,0,2]}
    t=seg((3,-.3),(3,2.8),'otOrange,dashed,line width=1pt')+seg((1,0),(1,2.4),'otNavy,line width=1.2pt')+poly([(1,2.4),(2.4,2.0),(1,1.6)],fill='otNavy!30')
    t+=seg((5,0),(5,2.4),'otNavy,line width=1.2pt')+poly([(5,2.4),(3.6,2.0),(5,1.6)],fill='otNavy!30')+T((1,-.05),'drapeau','below',r'\tiny')+T((5,-.05),'image','below',r'\tiny')
    dessin('sym-15',t,'Un drapeau et son symétrique par rapport à l’axe en tirets.')
    META['sym-15']={'type':'symetrie','axe':['v',3],'originaux':[(1,2.4),(2.4,2.0),(1,1.6)],'images':[(5,2.4),(3.6,2.0),(5,1.6)],'grille':[6,3]}

# ================================================================= chapitre 18 : solides
def solides():
    t=s_pave(0,0,.9,.9,.4,.3,'cube')+s_pave(1.9,0,1.3,.75,.45,.3,'pavé droit')+s_prisme(4.1,0,1.1,.9,.5,.3,'prisme droit')+s_pyramide(6.2,0,1.1,.45,.28,1.1,'pyramide')
    t+=s_cylindre(8.7,.2,.5,1.1,'cylindre')+s_cone(10.3,.2,.55,1.3,'cône')+s_boule(11.9,0,.6,'boule')
    dessin('cours-solides',t,'Les solides usuels ; les arêtes cachées sont en pointillés.')
    META['cours-solides']={'type':'libre'}
    cubes=[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1)]
    t=cubes_tex(cubes,s=.6)+vue(3.4,0,[(0,0),(0,1),(1,0)],.45,'de face')+vue(5.1,0,[(0,0),(1,0),(0,1),(1,1)],.45,'de dessus')+vue(6.8,0,[(0,0),(0,1),(1,0)],.45,'de droite')
    dessin('cours-assemblage-vues',t,'Un assemblage de 5 cubes et ses trois vues.')
    META['cours-assemblage-vues']={'type':'assemblage','cubes':5,'ajout':0,'liste':sorted(cubes)}
    t=s_pyramide(0,0,1.1,.45,.28,1.1)+s_cylindre(2.6,.2,.5,1.1)+s_cone(4.1,.2,.55,1.3)+s_prisme(5.3,0,1.1,.9,.5,.3)+s_boule(7.7,0,.6)+s_pave(9.0,0,1.3,.75,.45,.3)
    for n,x in enumerate([.75,2.6,4.1,6.05,7.7,9.85],1):t+=rf'\node[circle,draw=otMuted,inner sep=1pt,font=\tiny]at({x},-.45){{{n}}};'
    dessin('sol-1',t,'Six solides numérotés de 1 à 6.')
    META['sol-1']={'type':'libre'}
    t=s_pave(0,0,2.4,1.4,.9,.6)+s_pyramide(4.4,0,2.2,.9,.55,2.0)
    dessin('sol-2',t,'Un pavé droit et une pyramide à base carrée.')
    META['sol-2']={'type':'polyedres','pave':(6,12,8),'pyramide':(5,8,5)}
    assemblage('sol-3',[(i,j,k) for i in range(2) for j in range(2) for k in range(2)],'Un cube formé de petits cubes de 1 cm d’arête.')
    cubes=[(0,0,0),(1,0,0),(2,0,0),(0,1,0),(0,0,1)]
    t=cubes_tex(cubes,s=.6)
    views={'1':[(0,0),(1,0),(2,0),(2,1)],'2':[(0,0),(1,0),(2,0),(0,1)],'3':[(0,0),(1,0),(2,0),(3,0)]}
    x=3.3
    for k,cells in views.items():t+=vue(x,.1,cells,.4,'vue '+k);x+=2.1
    t+=sol(rf'\draw[otGreenDark,line width=1.2pt,rounded corners=2pt]({3.3+2.1-.15},-.35)rectangle({3.3+2.1+1.35},1.05);')
    dessin('sol-4',t,'L’assemblage et trois propositions de vue de dessus (le haut de chaque vue correspond à l’arrière).')
    META['sol-4']={'type':'vues','dessus':sorted({(i,j) for i,j,k in cubes}),'bonne':sorted(views['2'])}
    assemblage('sol-5',[(0,0,0),(0,0,1),(0,0,2),(1,0,0),(1,0,1),(2,0,0)],'Un escalier de cubes de 1 cm d’arête.')
    cubes=[(i,j,0) for i in range(3) for j in range(3)]+[(i,j,1) for i in range(2) for j in (1,2)]+[(0,1,2)]
    assemblage('sol-6',cubes,'Trois étages pleins, posés les uns sur les autres.')
    cubes=[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1)]
    t=cubes_tex(cubes,s=.6)+r'\node[font=\tiny,text=otMuted]at(.6,-.3){face};\draw[otMuted,->](.6,-.45)--(.6,-.1);\node[font=\tiny,text=otMuted,right]at(1.75,.35){droite};'
    t+=sol(vue(3.6,0,[(0,0),(0,1),(1,0)],.45,'de face',True)+vue(5.3,0,[(0,0),(1,0),(0,1),(1,1)],.45,'de dessus',True)+vue(7.0,0,[(0,0),(0,1),(1,0)],.45,'de droite',True))
    dessin('sol-7',t,'L’assemblage de 5 cubes ; les trois vues figurent en vert au corrigé.')
    META['sol-7']={'type':'assemblage','cubes':5,'ajout':0,'liste':sorted(cubes),'face':[2,1],'droite':[2,1]}
    h={(0,2):3,(1,2):2,(2,2):1,(0,1):2,(1,1):1,(0,0):1}
    t=r'\draw[otRule!80,line width=.3pt](0,0)grid[step=.6](1.8,1.8);'+vue(0,0,list(h),.6,'',False,{k:v for k,v in h.items()})+T((.9,1.85),'arrière','above',r'\tiny','otMuted')+T((.9,-.05),'avant','below',r'\tiny','otMuted')
    dessin('sol-8',t,'Vue de dessus : chaque nombre indique combien de cubes sont empilés sur la case.')
    META['sol-8']={'type':'plan','hauteurs':list(h.values())}
    A=[(i,j,0) for i in range(3) for j in range(2)]+[(i,0,1) for i in range(3)];B=[(i,j,k) for i in range(2) for j in range(2) for k in range(2)]
    t=cubes_tex(A,s=.55)+T((.9,-.05),'A','below')+cubes_tex(B,s=.55,x0=3.4)+T((3.95,-.05),'B','below')
    dessin('sol-9',t,'Deux assemblages de cubes identiques ; les cubes cachés reposent sur le premier étage plein.')
    META['sol-9']={'type':'comparaison','A':len(A),'B':len(B)}
    full=[(i,j,k) for i in range(3) for j in range(3) for k in range(3)]
    cubes=[c for c in full if c[2]<2]+[(0,0,2),(1,0,2)]
    miss=[c for c in full if c not in cubes]
    assemblage('sol-10',cubes,'Deux étages pleins de 3 sur 3 et deux cubes au troisième étage ; les cubes à ajouter figurent en vert au corrigé.',sol_cubes=miss)
    assemblage('sol-11',[(i,j,k) for i in range(4) for j in range(3) for k in range(2)],'Les morceaux de sucre rangés dans la boîte.',s=.5)
    wall=[(i,0,k) for i in range(6) for k in range(4) if (i,k) not in [(2,2),(3,2)]]
    assemblage('sol-12',wall,'Le mur, vu de face ; la fenêtre traverse le mur.',s=.5)
    cube=[(i,j,k) for i in range(3) for j in range(3) for k in range(3)]
    s=.6;nums=''
    for i in range(3):
        for k in range(3):
            n=1+(i in (0,2))+(k in (0,2))
            nums+=rf'\node[font=\scriptsize\bfseries,text=otGreenDark]at({i*s+s/2:.3f},{k*s+s/2:.3f}){{{n}}};'
    dessin('sol-13',cubes_tex(cube,s=s)+sol(nums),'Le grand cube peint ; au corrigé, les nombres verts indiquent les faces peintes des cubes de devant.')
    META['sol-13']={'type':'assemblage','cubes':27,'ajout':0,'liste':sorted(cube)}
    t=vue(0,0,[(0,0),(1,0),(0,1),(1,1)],.45,'de dessus')+vue(1.7,0,[(0,0),(0,1),(1,0)],.45,'de face')+vue(3.4,0,[(0,0),(1,0),(1,1)],.45,'de droite')
    sc=[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,1,1)]
    t+=sol(cubes_tex([],sc,s=.55,x0=5.6))
    dessin('sol-14',t,'Les trois vues de l’assemblage ; au corrigé, l’assemblage reconstitué figure en vert.')
    META['sol-14']={'type':'vues3','cubes':sc}
    A=[(i,j,0) for i in range(3) for j in range(2)];B=[(0,0,0),(0,0,1),(0,0,2),(1,0,0),(2,0,0),(0,1,0)]
    t=cubes_tex(A,s=.55)+T((.9,-.05),'A','below')+cubes_tex(B,s=.55,x0=3.2)+T((3.9,-.05),'B','below')
    dessin('sol-15',t,'Deux assemblages de cubes identiques, de formes différentes.')
    META['sol-15']={'type':'comparaison','A':len(A),'B':len(B)}

# ================================================================= chapitre 19 et 20 : données et hasard
def donnees():
    t=r'\begin{scope}[scale=.8]'
    vals=[9,4,8,3]
    t+=r'\draw[otMuted,->](-.2,0)--(4.2,0);\draw[otMuted,->](0,0)--(0,3.2);'+''.join(rf'\fill[otNavy!35]({.3+i*.95},0)rectangle({.85+i*.95},{v*.3:.2f});' for i,v in enumerate(vals))+T((2,-.1),'barres : comparer','below',r'\tiny')
    t+=r'\end{scope}'+r'\begin{scope}[shift={(5.1,1.2)}]'+circulaire_tex([2,1,1],['',' ',' '],r=1.1)+T((0,-1.2),'disque : parts d’un tout','below',r'\tiny')+r'\end{scope}'
    t+=r'\begin{scope}[shift={(7.4,0)},scale=.8]'
    ys=[3,5,4,7,8];t+=r'\draw[otMuted,->](-.2,0)--(4.2,0);\draw[otMuted,->](0,0)--(0,3.2);\draw[otNavy,line width=1pt]'+' -- '.join(f'({.4+i*.85:.2f},{y*.35:.2f})' for i,y in enumerate(ys))+';'
    t+=''.join(rf'\fill[otNavy]({.4+i*.85:.2f},{y*.35:.2f})circle(1.4pt);' for i,y in enumerate(ys))+T((2,-.1),'courbe : évolution','below',r'\tiny')+r'\end{scope}'
    dessin('cours-graphiques',t,'Trois représentations, trois usages.')
    META['cours-graphiques']={'type':'libre'}
    barres_diag('don-3',['lun','mar','mer','jeu','ven'],[15,20,35,25,30],5,leg='Livres empruntés au CDI chaque jour ; une graduation vaut 5 livres.')
    dessin('don-4',circulaire_tex([2,1,1],['vidéos','jeux','messages']),'Le disque entier représente les 4 heures d’écran.')
    META['don-4']={'type':'secteurs','angles':[180,90,90]}
    t,X,Y=courbe([6,9,12,15,18,21],[8,12,18,21,16,11],6,21,0,25,[(h,f'{h} h') for h in (6,9,12,15,18,21)],5)
    t+=T((0,4.4),'°C','left',r'\tiny')
    dessin('don-5',t,'Température dans la cour, en degrés Celsius, relevée toutes les trois heures.')
    META['don-5']={'type':'courbe','valeurs':[8,12,18,21,16,11],'heures':[6,9,12,15,18,21]}
    t=r'\draw[otMuted,->](-.3,0)--(3.6,0);\draw[otMuted,->](0,0)--(0,4.4);'
    for v in range(100,111,2):t+=rf'\draw[otRule!80,line width=.3pt](0,{(v-100)*.4:.2f})--(3.4,{(v-100)*.4:.2f});\node[left,font=\tiny]at(0,{(v-100)*.4:.2f}){{{v}}};'
    for i,(lab,v) in enumerate([('2025',102),('2026',108)]):t+=rf'\fill[otNavy!40]({.5+i*1.5},0)rectangle({1.3+i*1.5},{(v-100)*.4:.2f});'+T((.9+i*1.5,-.05),lab,'below',r'\tiny')
    t+=T((1.7,4.3),'Nos ventes explosent !','above',r'\scriptsize','otRed')
    dessin('don-9',t,'Diagramme publié par le magasin ; l’axe vertical commence à 100.')
    META['don-9']={'type':'barres','valeurs':[102,108],'origine':100}
    barres_diag('don-10',['foot','danse','judo','natation'],[12,9,5,4],2,sol_=True,leg='Le diagramme à construire figure en vert ; une graduation vaut 2 élèves.')
    tt=[3,4,7,11,15,19,23,22,18,13,8,4];pp=[55,48,45,50,60,40,18,25,52,66,70,62];mois='JFMAMJJASOND'
    t=r'\begin{scope}[scale=.78]'
    q,X,Y=courbe(list(range(1,13)),tt,0,13,0,25,[(i+1,mois[i]) for i in range(12)],5,w=6.2,h=3.4);t+=q+T((0,3.9),'°C','left',r'\tiny')+T((3.1,-.4),'température moyenne','below',r'\tiny')
    t+=r'\end{scope}\begin{scope}[shift={(6.1,0)},scale=.78]'
    t+=r'\draw[otMuted,->](0,0)--(6.6,0);\draw[otMuted,->](0,0)--(0,3.8);'
    for v in (20,40,60):t+=rf'\draw[otRule!80,line width=.3pt](0,{v*.0486:.3f})--(6.4,{v*.0486:.3f});\node[left,font=\tiny]at(0,{v*.0486:.3f}){{{v}}};'
    for i,v in enumerate(pp):t+=rf'\fill[otNavy!35]({i*.5+.15:.2f},0)rectangle({i*.5+.45:.2f},{v*.0486:.3f});\node[below,font=\tiny]at({i*.5+.3:.2f},0){{{mois[i]}}};'
    t+=T((0,3.9),'mm','left',r'\tiny')+T((3.1,-.4),'précipitations','below',r'\tiny')+r'\end{scope}'
    dessin('don-13',t,'Une même ville : température moyenne en courbe et précipitations en barres, mois par mois.')
    META['don-13']={'type':'climat','temperatures':tt,'pluie':pp}
def hasard():
    t=r'\shade[left color=otNavy!8,right color=otNavy!45](0,0)rectangle(10,.35);\draw[geoTrait](0,0)rectangle(10,.35);'
    for x,lab,txt in [(0,'0','impossible'),(5,r'$\frac12=0{,}5$','une chance sur deux'),(10,'1','certain')]:t+=rf'\draw[otNavy,line width=.9pt]({x},-.1)--({x},.45);'+T((x,-.1),lab,'below',r'\scriptsize')+T((x,.45),txt,'above',r'\tiny')
    t+=T((2.5,.45),'peu probable','above',r'\tiny','otMuted')+T((7.5,.45),'probable','above',r'\tiny','otMuted')
    dessin('cours-echelle-proba',t,'Une probabilité se place entre 0 et 1.')
    META['cours-echelle-proba']={'type':'libre'}
    f=[.6,.46,.52,.485,.494,.503];labs=[10,50,100,200,500,1000]
    t=r'\draw[otMuted,->](0,0)--(9.4,0);\draw[otMuted,->](0,0)--(0,4.4);'
    for v,lab in [(0,'0'),(.5,'0{,}5'),(1,'1')]:t+=rf'\draw[otRule!80,line width=.3pt](0,{v*4})--(9,{v*4});\node[left,font=\tiny]at(0,{v*4}){{${lab}$}};'
    t+=r'\draw[otOrange,dashed,line width=.9pt](0,2)--(9,2);'+T((9,2),'probabilité','right',r'\tiny','otOrange!80!black')
    t+=r'\draw[otNavy,line width=1pt]'+' -- '.join(f'({.7+i*1.55:.2f},{v*4:.2f})' for i,v in enumerate(f))+';'+''.join(rf'\fill[otNavy]({.7+i*1.55:.2f},{v*4:.2f})circle(1.5pt);\node[below,font=\tiny]at({.7+i*1.55:.2f},0){{{l}}};' for i,(v,l) in enumerate(zip(f,labs)))
    t+=T((4.6,-.45),'nombre de lancers d’une pièce','below',r'\tiny')+T((0,4.4),'fréquence de pile','right',r'\tiny')
    dessin('cours-frequences',t,'La fréquence de pile se rapproche de 0,5 quand le nombre de lancers augmente.')
    META['cours-frequences']={'type':'frequences','valeurs':f}
    items=['R','R','R','B','B','B','B','B','V','V']
    dessin('hasard-2',urne_tex(items),'Dix boules indiscernables au toucher : R rouge, B bleue, V verte.')
    META['hasard-2']={'type':'urne','items':items}
    dessin('hasard-4',roue_tex([45]*8,[str(k) for k in range(1,9)],colors=['otNavy!25','otGreen!30']*4),'Huit secteurs identiques ; le repère noir désigne le secteur obtenu.')
    META['hasard-4']={'type':'secteurs','angles':[45]*8}
    t='';x1=2.2;x2=4.4
    for i,a in enumerate('PF'):
        y1=.75-i*1.5
        t+=rf'\draw[otMuted](0,0)--({x1},{y1});\node[fill=otNavy!15,rounded corners=1mm,inner sep=2pt,font=\scriptsize]at({x1},{y1}){{{a}}};'
        for j,b in enumerate('PF'):
            y2=y1+(.5-j)*.62
            t+=rf'\draw[otMuted]({x1+.3},{y1})--({x2},{y2:.2f});\node[fill=otNavy!8,rounded corners=1mm,inner sep=2pt,font=\scriptsize]at({x2+.7},{y2:.2f}){{{a}{b}}};'
    t+=T((x1,1.35),'pièce 1','above',r'\tiny','otMuted')+T((x2+.7,1.35),'issues','above',r'\tiny','otMuted')
    dessin('hasard-6',t,'L’arbre des deux lancers : P pour pile, F pour face.')
    META['hasard-6']={'type':'arbre','issues':4}
    t=''
    for a in range(6):
        for b in range(6):
            s=a+b+2
            if s==7:t+=sol(rf'\fill[otGreen!45]({b},{5-a})rectangle({b+1},{6-a});')
            t+=rf'\node[font=\tiny]at({b+.5},{5-a+.5}){{{s}}};'
    t+=grille(6,6)+''.join(rf'\node[font=\scriptsize\bfseries]at({k+.5},6.35){{{k+1}}};\node[font=\scriptsize\bfseries]at(-.35,{5-k+.5}){{{k+1}}};' for k in range(6))
    t+=T((3,6.8),'second dé','above',r'\tiny','otMuted')+rf'\node[rotate=90,font=\tiny,text=otMuted]at(-1.0,3){{premier dé}};'
    dessin('hasard-7',rf'\begin{{scope}}[scale=.55]{t}\end{{scope}}','Le tableau des 36 issues équiprobables : chaque case contient la somme des deux dés.')
    META['hasard-7']={'type':'tableau_des','sommes7':sum(1 for a in range(6) for b in range(6) if a+b+2==7)}
    A=['R','R','N','N','N'];B=['R','R','R','N','N','N','N','N']
    t=urne_tex(A,0,5)+T((2,-.6),'urne A','below',r'\scriptsize')+urne_tex(B,5.6,4)+T((7.1,-.6),'urne B','below',r'\scriptsize')
    dessin('hasard-9',t,'R : boule rouge ; N : boule noire.')
    META['hasard-9']={'type':'urnes','A':A,'B':B}
    dessin('hasard-10',roue_tex([180,90,90],['A','B','C'],colors=['otNavy!30','otGreen!40','otOrange!45']),'Une roue à trois secteurs de tailles différentes.')
    META['hasard-10']={'type':'secteurs','angles':[180,90,90]}
    xs=[50,100,200,400,600,800,1000];ys=[.66,.6,.635,.615,.625,.618,.62]
    t,X,Y=courbe(xs,ys,0,1000,.5,.75,[(x,str(x)) for x in xs],.05,w=8.6,h=3.6,ylabs={.5:'0{,}50',.55:'0{,}55',.6:'0{,}60',.65:'0{,}65',.7:'0{,}70',.75:'0{,}75'})
    t+=sol(rf'\draw[otGreenDark,dashed,line width=.9pt](0,{Y(.62):.3f})--(8.6,{Y(.62):.3f});')+T((4.3,-.45),'nombre de lancers','below',r'\tiny')+T((0,4.0),'fréquence de « pointe en haut »','right',r'\tiny')
    dessin('hasard-13',t,'Fréquence de « pointe en haut » au fil des lancers.')
    META['hasard-13']={'type':'frequences','valeurs':ys}

# ================================================================= chapitre 21 : programmes
def programmes():
    dessin('cours-blocs',pile(lignes(SCRIPTS['cours-blocs']),width=6.4),'Un programme par blocs : une entrée, deux instructions de calcul, une sortie.')
    META['cours-blocs']={'type':'script','nom':'cours-blocs'}
    s=executer(SCRIPTS['cours-chemin'])
    t=pile(lignes(SCRIPTS['cours-chemin']),width=5.2)+r'\begin{scope}[shift={(6.2,-2.4)},scale=.5]'+quad(5,5,start=(0,0))+chemin(s['trace'],(0,0),'otNavy')+r'\end{scope}'
    dessin('cours-chemin',t,'Le programme et le chemin tracé : un carré de 3 cases de côté.')
    META['cours-chemin']={'type':'chemin','trace':s['trace']}
    dessin('ins-2',pile(lignes(SCRIPTS['ins-2']),width=6.4),'Un programme de calcul par blocs, à exécuter de haut en bas.')
    META['ins-2']={'type':'script','nom':'ins-2'}
    s=executer(SCRIPTS['ins-4']);marks={(0,0):'D',(3,2):'P',(5,1):'Q',(5,2):'R'}
    t=quad(7,4,marks=marks,start=(0,0))+sol(chemin(s['trace'],(0,0)))
    dessin('ins-4',rf'\begin{{scope}}[scale=.6]{t}\end{{scope}}','Le robot part de la case D, tourné dans le sens de la flèche orange.')
    META['ins-4']={'type':'chemin','trace':s['trace'],'arrivee':(5,2)}
    s=executer(SCRIPTS['ins-6'])
    t=quad(4,4,start=(0,3),marks={})+sol(chemin(s['trace'],(0,3))+r'\draw[otGreenDark,line width=1.2pt,->](.5,1.3)--(.5,1.9);')
    dessin('ins-6',rf'\begin{{scope}}[scale=.6]{t}\end{{scope}}','Le lutin part de la case marquée par la flèche orange.')
    META['ins-6']={'type':'chemin','trace':s['trace'],'arrivee':(0,-2)}
    s=executer(SCRIPTS['ins-8']);obs=[(3,0),(4,0),(4,1),(1,2),(4,2),(1,4)]
    t=quad(6,5,obstacles=obs,marks={(0,0):'D',(5,3):'A'},start=(0,0))+sol(chemin(s['trace'],(0,0)))
    dessin('ins-8',rf'\begin{{scope}}[scale=.6]{t}\end{{scope}}','Les cases grisées sont interdites.')
    META['ins-8']={'type':'chemin','trace':s['trace'],'obstacles':obs,'arrivee':(5,3)}
    s=executer(SCRIPTS['ins-10'])
    t=quad(6,6,start=(0,0))+sol(chemin(s['trace'],(0,0)))
    dessin('ins-10',rf'\begin{{scope}}[scale=.55]{t}\end{{scope}}','Le lutin part de la case marquée par la flèche orange.')
    META['ins-10']={'type':'chemin','trace':s['trace']}
    s=executer(SCRIPTS['ins-11'])
    t=quad(8,5,marks={(0,0):'D'},start=(0,0))
    for (c,r),lab in [((6,4),'A'),((6,2),'B'),((4,1),'C')]:t+=rf'\filldraw[draw=otNavy,fill=otOrange!35]({c+.15},{r+.1})--({c+.85},{r+.1})--({c+.85},{r+.55})--({c+.5},{r+.85})--({c+.15},{r+.55})--cycle;\node[font=\tiny\bfseries]at({c+.5},{r+.4}){{{lab}}};'
    t+=sol(chemin(s['trace'],(0,0)))
    dessin('ins-11',rf'\begin{{scope}}[scale=.6]{t}\end{{scope}}','Le quartier quadrillé, le départ D et trois maisons.')
    META['ins-11']={'type':'chemin','trace':s['trace'],'maisons':{'A':(6,4),'B':(6,2),'C':(4,1)}}
    lines=[(0,'répéter 6 fois','controle'),(1,'avancer de 3 cm','mouvement'),(1,'tourner de 60° à gauche','mouvement')]
    pts=[(0,0)];h=0
    for k in range(6):
        p=polar(pts[-1],h,1.5);pts.append(p);h+=60
    t=pile(lines,width=5)+sol(rf'\begin{{scope}}[shift={{(6.6,-1.6)}}]'+poly(pts[:-1],'geoReponse')+r'\end{scope}')
    dessin('ins-12',t,'Le programme du lutin ; au corrigé, la figure tracée figure en vert (réduite).')
    META['ins-12']={'type':'polygone_tortue','cotes':6,'retour':dist(pts[0],pts[-1])}
    s=executer(SCRIPTS['ins-14'])
    t=quad(6,6,start=(0,0))+chemin(s['trace'],(0,0),'otNavy')+sol(r'\draw[otGreenDark,dashed,line width=1.4pt](.5,4.5)--(.5,.5);')
    dessin('ins-14',rf'\begin{{scope}}[scale=.55]{t}\end{{scope}}','Le tracé obtenu par le programme de Hugo.')
    META['ins-14']={'type':'chemin','trace':s['trace']}
    s=executer(SCRIPTS['ins-15']);obs=[(0,2),(1,3),(2,4),(3,0),(4,1),(5,2)]
    t=quad(6,6,obstacles=obs,marks={(0,0):'D',(5,5):'A'},start=(0,0))+sol(chemin(s['trace'],(0,0)))
    dessin('ins-15',rf'\begin{{scope}}[scale=.55]{t}\end{{scope}}','Les cases grisées sont interdites ; le robot avance case par case.')
    META['ins-15']={'type':'chemin','trace':s['trace'],'obstacles':obs,'arrivee':(5,5)}

# ================================================================= défis, bilans et preuves
def annexes():
    t=poly([(1,0),(4,1),(3,4),(0,3)],fill='otNavy!25')
    t+=sol(''.join(poly(tr,'geoReponse',fill='otGreen!30') for tr in [[(0,0),(1,0),(0,3)],[(1,0),(4,0),(4,1)],[(4,1),(4,4),(3,4)],[(3,4),(0,4),(0,3)]]))
    t+=''.join(rf'\draw[otNavy!35,line width=.3pt]({k},0)--({k},4) (0,{k})--(4,{k});' for k in range(1,4))+poly([(1,0),(4,1),(3,4),(0,3)])+r'\draw[geoTrait](0,0)rectangle(4,4);'
    dessin('defi-carre',rf'\begin{{scope}}[scale=.75]{t}\end{{scope}}','Le carré penché dans un carré de 4 cm de côté ; un carreau mesure 1 cm de côté.')
    META['defi-carre']={'type':'aires','valeurs':[16-6]}
    k=.4;A=(0,0);B=(6,0)
    t=rf'\begin{{scope}}[scale={k}]'+cercle(A,4,'otNavy,line width=1pt')+P(A,'A','below')+P(B,'B','below')+seg(A,B,'otMuted')
    for r,col in [(2,'otOrange'),(5,'otGreenDark'),(10,'otRed')]:t+=cercle(B,r,col+',dashed,line width=.7pt')+T(polar(B,90,r),f'$r={r}$','above',r'\tiny',col)
    t+=r'\end{scope}'
    dessin('defi-cercles',t,'Le cercle de centre A et de rayon 4 cm, et des cercles de centre B de rayons 2, 5 et 10 cm (figure réduite).')
    META['defi-cercles']={'type':'compte','nombres':[len(inter_cc(A,4,B,r)) for r in (1,2,5,10,11) if True]}
    O=(0,0);r=2.2;A=polar(O,150,r);B=polar(O,60,r);Cc=polar(O,200,r);D=polar(O,300,r)
    t=cercle(O,r)+seg(A,B)+seg(Cc,D)+P(A,'A','left')+P(B,'B','above')+P(Cc,'C','below')+P(D,'D','right')
    t+=sol(ligne(mid(A,B),O,.6,'geoAide')+ligne(mid(Cc,D),O,.6,'geoAide')+P(O,'O','above right','otGreenDark'))
    dessin('defi-centre',t,'Le cercle laissé par l’assiette et deux cordes ; la construction figure en vert au corrigé.')
    META['defi-centre']={'type':'centre','O':O,'cordes':[(A,B),(Cc,D)]}
    t=grille(12,4)+seg((4,-.3),(4,4.3),'otOrange,dashed,line width=1pt')+seg((7,-.3),(7,4.3),'otOrange,dashed,line width=1pt')+L((4,4.3),'(d_1)','above')+L((7,4.3),'(d_2)','above')+P((3,2),'M','below')
    t+=sol(P((5,2),'M_1','below','otGreenDark')+P((9,2),'M_2','below','otGreenDark')+r'\draw[otGreenDark,->](3.1,2.3)to[bend left=30](4.9,2.3);\draw[otGreenDark,->](5.1,2.3)to[bend left=30](8.9,2.3);')
    dessin('defi-miroirs',rf'\begin{{scope}}[scale=.6]{t}\end{{scope}}','Deux droites parallèles distantes de 3 cm ; un carreau mesure 1 cm.')
    META['defi-miroirs']={'type':'symetrie','axe':['v',4],'originaux':[(3,2)],'images':[(5,2)],'grille':[12,4],'second':[(5,2),(9,2)]}
    cubes=[(i,j,0) for i in range(3) for j in range(3)]+[(i,j,1) for i in range(2) for j in (1,2)]+[(0,2,2)]
    dessin('defi-pyramide',cubes_tex(cubes,s=.55),'Une pyramide de 3 étages : 9 cubes, puis 4, puis 1.')
    META['defi-pyramide']={'type':'assemblage','cubes':len(cubes),'ajout':0,'liste':[]}
    x=y=0;pts=[(0,0)];d=[(1,0),(0,1),(-1,0),(0,-1)];k=0
    for Lg in [1,1,2,2,3,3,4,4,5,5]:
        x+=d[k%4][0]*Lg;y+=d[k%4][1]*Lg;pts.append((x,y));k+=1
    t=grille(10,10,-5,-5)+P((0,0),'O','below left')+sol(rf'\draw[otGreenDark,line width=1.3pt,-{{Stealth[length=2.4mm]}}]'+'--'.join(C(p) for p in pts)+';'+P(pts[-1],'','above','otGreenDark'))
    t+=r'\draw[otOrange,line width=1.2pt,->](0,0)--(.6,0);'
    dessin('defi-spirale',rf'\begin{{scope}}[scale=.4]{t}\end{{scope}}','Le quadrillage du robot ; un carreau représente une case.')
    META['defi-spirale']={'type':'spirale','arrivee':pts[-1],'longueur':sum([1,1,2,2,3,3,4,4,5,5])}
    k=.6;A=(0,0);B=(7,0);Cc=polar(A,40,7*sin(radians(60))/sin(radians(80)));O=circumcenter(A,B,Cc);A2=reflect(A,B,Cc)
    t=rf'\begin{{scope}}[scale={k}]'+tri(A,B,Cc)+arc_at(A,B,Cc,.8,'otNavy',r'$40^\circ$',1.4)+arc_at(B,Cc,A,.8,'otNavy',r'$60^\circ$',1.4)+T((3.5,0),'7 cm','below',r'\scriptsize')
    t+=sol(cercle(O,dist(O,A),'geoReponse')+P(O,'O','above left','otGreenDark')+poly([A2,B,Cc],'geoReponse')+P(A2,"A'",'right','otGreenDark')+seg(A,A2,'otGreenDark,dashed,line width=.4pt'))+r'\end{scope}'
    dessin('bilan-triangle',t,'Figure de principe du triangle ABC ; les constructions figurent en vert au corrigé (figure réduite).')
    META['bilan-triangle']={'type':'triangle','points':[A,B,Cc],'angles':[40,60,80]}
    s=.3;t=''
    t+=rf'\fill[otNavy!15](0,0)rectangle({s},{10*s});\fill[otOrange!20](0,0)rectangle({10*s},{s});\fill[otGreen!60](0,0)rectangle({s},{s});'
    for kk in range(11):t+=rf'\draw[otRule,line width=.25pt]({kk*s:.2f},0)--({kk*s:.2f},{10*s:.2f}) (0,{kk*s:.2f})--({10*s:.2f},{kk*s:.2f});'
    t+=rf'\draw[geoTrait](0,0)rectangle({10*s},{10*s});'+T((10*s+.2,.15),r'$0{,}1\times0{,}1=0{,}01$ : un centième de l’unité','right',r'\scriptsize','otGreenDark')
    dessin('preuve-produit',t,'Une bande d’un dixième croisée avec une bande d’un dixième : un petit carré, un centième du grand.')
    META['preuve-produit']={'type':'grille','valeurs':[1]}
    def coins2(A,B,Cc,Q,cols=('otNavy!35','otGreen!45','otOrange!45')):
        a=angle_en(A,B,Cc);b=angle_en(B,A,Cc);c=180-a-b
        t=poly([A,B,Cc],fill='otNavy!5')+arc_at(A,B,Cc,.5,'otNavy',fill=cols[0])+arc_at(B,Cc,A,.5,'otNavy',fill=cols[1])+arc_at(Cc,A,B,.45,'otNavy',fill=cols[2])
        t+=seg((Q[0]-1.5,Q[1]),(Q[0]+1.5,Q[1]),'otMuted')+arcang(Q,0,a,.75,'otNavy',fill=cols[0])+arcang(Q,a,a+c,.75,'otNavy',fill=cols[2])+arcang(Q,a+c,180,.75,'otNavy',fill=cols[1])
        return t,(a,b,c)
    t,abc=coins2((0,0),(5,0),(3.6,1.6),(8.2,.2))
    dessin('preuve-triangle',t,'Les trois coins d’un triangle allongé, rassemblés, forment encore un angle plat.')
    META['preuve-triangle']={'type':'somme','angles':list(abc)}

def tout():
    for f in [distances,mediatrices,angles,triangles,symetries,solides,donnees,hasard,programmes,annexes]:f()
