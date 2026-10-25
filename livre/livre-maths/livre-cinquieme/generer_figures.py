"""Figures vectorielles et réponses conditionnelles, sans dépendance à un autre livre."""
from pathlib import Path
from math import sqrt,sin,cos,tan,radians,atan2,degrees
from modele import figure,FIGURES,tableau
from outils_figures import dessin,axes,graph,pave,cylindre,pile
from donnees_scripts import SCRIPTS,lignes,executer
META={}
def answer(txt):
    return r'\geoEnonce{?}\geoSolution{\textcolor{otGreenDark}{'+txt+'}}'
def poly(pts,color='otNavy'):
    return rf'\draw[{color},line width=.85pt]'+'--'.join(f'({x},{y})' for x,y in pts)+'--cycle;'
def dot(x,y,lab,where='above right',color='otNavy'):
    return rf'\fill[{color}]({x},{y})circle(1.4pt)node[{where},geoLabel]{{$ {lab} $}};'
def coord(nom,points=(),sol=(),xb=(-5,5),yb=(-4,4),step=1,extra=''):
    t=axes(xb,yb,step,step,ortho=True)
    for lab,x,y in points:t+=dot(x,y,lab)
    t+=extra+r'\geoSolution{'+''.join(dot(x,y,lab,color='otGreenDark') for lab,x,y in sol)+'}'+r'\end{scope}'
    dessin(nom,t,'Repère orthogonal ; suivre les graduations et l’ordre des coordonnées.')
    META[nom]={'type':'repere','points':list(points),'solutions':list(sol),'bornes':[xb,yb]}
def droite(nom,points=(),sol=(),lo=-5,hi=5,pas=1):
    sx=9/(hi-lo);t=rf'\begin{{scope}}[x={sx}cm]\draw[otMuted,->]({lo},0)--({hi+.3/sx},0);'
    for k in range(round((hi-lo)/pas)+1):
        v=lo+k*pas
        t+=rf'\draw[otMuted]({v},-.07)--({v},.07);'
        if abs(v-round(v))<1e-9:t+=rf'\node[below,font=\scriptsize]at({v},-.1){{$ {round(v)} $}};'
    t+=''.join(dot(x,0,lab,'above') for lab,x in points)
    t+=r'\geoSolution{'+''.join(dot(x,0,lab,'above',color='otGreenDark') for lab,x in sol)+'}'+r'\end{scope}'
    dessin(nom,t,'Les graduations sont régulières ; les positions cherchées sont ajoutées au corrigé.')
    META[nom]={'type':'droite','points':points,'solutions':sol,'pas':pas,'bornes':[lo,hi]}
def rect(nom,L,H,extra='',sol='',square=False):
    w=3 if square else 5;h=3 if square else 2.6
    t=rf'\draw[geoTrait](0,0)rectangle({w},{h});\node[below]at({w/2},0){{{L}}};\node[left]at(0,{h/2}){{{H}}};'
    dessin(nom,t+extra+r'\geoSolution{'+sol+'}')
def secteurs(nom,angles,labels,blank=False):
    assert sum(angles)==360
    t='';start=0
    for a,label,col in zip(angles,labels,['otGreen!65','otNavy!45','otOrange!65','otNavy!15','otGreen!25','otOrange!35','otGreen!50','otNavy!25']):
        end=start+a;mid=(start+end)/2
        t+=rf'\filldraw[draw=white,fill={col}](0,0)--({start}:1.7)arc({start}:{end}:1.7)--cycle;\node[font=\scriptsize]at({mid}:1.1){{{label}}};';start=end
    if blank:t=r'\geoEnonce{\draw[geoTrait](0,0)circle(1.7);\node at(0,0){À construire};}\geoSolution{'+t+'}'
    dessin(nom,t,'Le disque est partagé selon les proportions indiquées.')
    META[nom]={'type':'secteurs','angles':angles}
def urne(nom,items):
    t=r'\draw[otMuted](-.5,2.2)--(-.5,-.6)--(5,-.6)--(5,2.2);'
    for i,lab in enumerate(items):
        color={'R':'otOrange!55','B':'otNavy!30','V':'otGreen!55'}[lab[0]]
        t+=rf'\node[circle,draw=otMuted,fill={color},minimum size=7mm,font=\scriptsize]at({i%4*1.3},{1.4-i//4*1.1}){{{lab}}};'
    dessin(nom,t,'Les lettres identifient les boules ou jetons ; les objets sont indiscernables au toucher.')
    META[nom]={'type':'urne','items':items}
def triangle(nom,ab=6,c=(2,4),labels=None,extra='',construction=False):
    pts=[(0,0),(ab,0),c];sx=min(6/max(ab,c[0],1),3.1/max(c[1],.1))
    t=rf'\begin{{scope}}[scale={sx}]'
    if construction:t+=rf'\draw[geoTrait](0,0)--({ab},0);'+r'\geoSolution{'+poly(pts,'otGreenDark')+dot(*c,'C','above','otGreenDark')+'}'
    else:t+=poly(pts)+dot(*c,'C','above')
    t+=dot(0,0,'A','below left')+dot(ab,0,'B','below right')
    center=(sum(x for x,y in pts)/3,sum(y for x,y in pts)/3)
    for (i,j),lab in (labels or {}).items():
        a,b=pts[i],pts[j];mx=(a[0]+b[0])/2;my=(a[1]+b[1])/2
        dx=b[0]-a[0];dy=b[1]-a[1];norm=sqrt(dx*dx+dy*dy);nx=-dy/norm;ny=dx/norm
        if nx*(mx-center[0])+ny*(my-center[1])<0:nx=-nx;ny=-ny
        distance=.95 if (i,j)==(0,1) and '{M}' in extra else .4
        t+=rf'\node[geoLabel,font=\scriptsize]at({mx+nx*distance},{my+ny*distance}){{{lab}}};'
    t+=extra+r'\end{scope}';dessin(nom,t,'Schéma de principe ; les constructions et réponses cherchées sont ajoutées en vert au corrigé.')
    META[nom]={'type':'triangle','points':pts}
def paral(nom,b=6,dx=1.5,h=3,extra='',construction=False):
    pts=[(0,0),(b,0),(b+dx,h),(dx,h)]
    t=poly(pts) if not construction else rf'\draw[geoTrait](0,0)--({b},0)--({b+dx},{h});'+r'\geoSolution{'+poly(pts,'otGreenDark')+'}'
    for (x,y),lab,pos in zip(pts,'ABCD',['below left','below right','above right','above left']):
        mark=dot(x,y,lab,pos)
        t+=r'\geoSolution{'+mark+'}' if construction and lab=='D' else mark
    dessin(nom,t+extra,'Schéma de principe ; seules les mesures et les propriétés données sont à utiliser.')
    META[nom]={'type':'parallelogramme','points':pts}
def nombres():
    droite('cours-relatifs',[('A',-3),('B',3)])
    droite('rel-1',[('A',-3),('B',1),('C',4)])
    droite('rel-2',sol=[('D',-2),('E',3)])
    droite('rel-8',[('F',-.75),('G',1.5)],lo=-2,hi=2,pas=.25)
    droite('rel-15',lo=-7,hi=7)
    FIGURES['rel-15']['tex']=FIGURES['rel-15']['tex'].replace(r'\end{scope}',r'\draw[otNavy,line width=2pt](-6,.3)--(-2,.3);\geoSolution{\draw[otGreenDark,line width=2pt](2,.3)--(6,.3);}\end{scope}')
    droite('cours-addition',[('A',-4),('B',2)],lo=-5,hi=5)
    FIGURES['cours-addition']['tex']=FIGURES['cours-addition']['tex'].replace(r'\end{scope}',r'\draw[otGreenDark,->](-4,.7)--node[above]{$+6$}(2,.7);\end{scope}')
    droite('add-13',[('A',-6.5),('B',2.25)],lo=-7,hi=3,pas=.25)
    droite('cours-fractions',[('P',1.75)],lo=0,hi=3,pas=.25)
    droite('frac-8',sol=[('A',.5),('B',1.25),('C',1.75)],lo=0,hi=2,pas=.25)
    t=r'\draw[geoTrait](0,0)rectangle(6,1);\foreach\x in{1,2,3,4,5}{\draw[otMuted](\x,0)--(\x,1);}\fill[otGreen!35](0,0)rectangle(3,1);\fill[otOrange!40](3,0)rectangle(5,1);\node[above]at(1.5,1){$1/2=3/6$};\node[above]at(4,1){$1/3=2/6$};\node[below]at(3,0){Total : $5/6$};'
    dessin('cours-somme-fractions',t,'Deux partages sont réécrits avec la même unité : un sixième.')
    rect('cours-carre-cube','$c$','$c$',r'\node at(1.5,1.5){$c^2$};',square=True)
    rect('puiss-11','3,2 m','3,2 m',square=True)
    pave('puiss-12','6 cubes','6 cubes','6 couches')
    dessin('puiss-13',r'\draw[geoTrait](0,0)rectangle(1.4,1.4);\draw[geoTrait](3,0)rectangle(5.8,2.8);\node[below]at(.7,0){2 cm};\node[below]at(4.4,0){4 cm};','Deux faces carrées à la même échelle représentent les côtés des deux cubes.')
    dessin('puiss-15',r'\filldraw[fill=otGreen!30,draw=otNavy](0,0)rectangle(4,4);\filldraw[fill=white,draw=otNavy](.4,.4)rectangle(3.6,3.6);\node[below]at(2,0){côté extérieur : '+answer('10 cm')+r'};\node at(2,2){8 cm};\node[right]at(4,3.8){bord : 1 cm};')
    t=''
    for n in [1,2,3]:
        off=(n-1)*3.5
        for k in range(n):t+=rf'\draw[geoTrait]({off+k*.7},0)rectangle++(.7,.7);'
        t+=rf'\node[below]at({off+(n-1)*.35+.35},0){{étape {n}}};'
    dessin('cours-motif',t,'Les côtés communs sont des allumettes partagées par deux carrés.')
    figure('lit-8',FIGURES['cours-motif']['tex'],FIGURES['cours-motif']['legende'])
    rect('lit-4','$x$ cm','5 cm')
    t=r'\draw[geoTrait](0,0)rectangle(3,3);'
    for i in range(5):
        for x,y in [(i*.75,0),(i*.75,3),(0,i*.75),(3,i*.75)]:t+=rf'\fill[otNavy]({x},{y})circle(2pt);'
    dessin('lit-11',t,'Exemple avec cinq points par côté ; les sommets appartiennent à deux côtés.')
    rect('lit-15','$x+2$ cm','3 cm')
    for name,H,left,right in [('cours-distrib',4,'$x$','3'),('dist-12',3,'$x$','5')]:
        rect(name,f'{left} + {right} cm',f'{H} cm',rf'\draw[otMuted,dashed](3,0)--(3,2.6);\node[above]at(1.5,2.6){{{left}}};\node[above]at(4,2.6){{{right}}};',
             rf'\node[text=otGreenDark]at(1.5,1.3){{$ {H}x $}};\node[text=otGreenDark]at(4,1.3){{{H*int(right)}}};')
    FIGURES['cours-distrib']['tex']=FIGURES['cours-distrib']['tex'].replace(r'\geoSolution{',r'\geoSolution{') # Le texte de cours donne les deux aires.
    rect('dist-11','$x+4$ cm','$x+1$ cm')
    dessin('cours-equation',r'\draw[geoTrait](0,0)rectangle(3,1);\node at(1.5,.5){$x$};\draw[geoTrait](3,0)rectangle(5,1);\node at(4,.5){7};\draw[otMuted,|<->|](0,1.4)--node[above]{19}(5,1.4);','Une part inconnue et sept unités donnent dix-neuf unités.')
    rect('eq-13','8 cm',answer('5,75 cm'),r'\node at(2.5,1.3){46 cm$^2$};')
    t=''
    for k in range(3):t+=rf'\draw[geoTrait]({k*1.4},0)rectangle++(1.4,1);\node at({k*1.4+.7},.5){{$x$}};'
    t+=r'\draw[geoTrait](4.2,0)rectangle(5.5,1);\node at(4.85,.5){6};\draw[otMuted,|<->|](0,1.5)--node[above]{45 euros}(5.5,1.5);'
    dessin('eq-14',t,'Les trois premières parts ont la même valeur.')
def graphiques():
    graph('cours-proportion',[('2.4*\\x',0,3.5)],(0,4),(0,10),1,2,xlabel='kg',ylabel='euros')
    graph('cours-dependance',[('3*\\x+5',0,4)],(0,4),(0,18),1,3,xlabel='h',ylabel='euros')
    rect('prop-8','4,8 m réels','',r'\node at(2.5,1.3){échelle $1:100$};')
    graph('prop-11',[],(0,5),(0,12.5),1,2.5,xlabel='tickets',ylabel='euros',points=[('',1,2.5),('',2,5),('',3,7.5),('',4,10)])
    dessin('prop-15',r'\draw[geoTrait](0,0)--(1.5,1)--(3,.5)--(5,1.3);\node[above]at(2.5,1.5){itinéraire : 6,4 cm};\node[below]at(2.5,0){échelle $1:25000$};')
    coord('cours-repere',[('A',3,-2),('B',-2,3)])
    coord('rep-1',[('A',2,3),('B',-3,1)])
    coord('rep-2',sol=[('C',-2,-3)])
    coord('rep-3',sol=[('D',0,3),('E',-4,0)])
    coord('rep-4',sol=[('F',1,3),('G',3,1)])
    graph('rep-5',[('6+2*\\x',0,4)],(0,4),(0,16),1,2,xlabel='h',ylabel=r'$^\circ$C')
    for name,pts,xb,yb in [('rep-6',[('A',0,4),('B',1,6),('C',3,10)],(0,4),(0,12)),('rep-7',[('A',0,0),('B',1,1),('C',2,4),('D',3,9)],(0,4),(0,10))]:
        coord(name,sol=pts,xb=xb,yb=yb)
    coord('rep-8',sol=[('H',-1.5,2.5),('I',2.5,-.5)],xb=(-3,3),yb=(-3,3),step=.5)
    graph('rep-9',[],(0,6),(0,40),1,10,xlabel='min',ylabel='L',poly=r'\draw[geoTrait](0,10)--(2,30)--(4,30)--(6,10);')
    graph('rep-10',[('2*\\x+3',0,4)],(0,4),(0,12),1,3,points=[('',1,5),('',2,7),('',3,9)])
    coord('rep-11',[('A',-3,-1),('B',2,-1),('C',2,3)],[('D',-3,3)],extra=r'\draw[geoTrait](-3,-1)--(2,-1)--(2,3);\geoSolution{\draw[otGreenDark](2,3)--(-3,3)--(-3,-1);}')
    graph('rep-12',[('2*\\x+5',0,5)],(0,5),(0,16),1,2,xlabel='h',ylabel='euros')
    graph('rep-13',[('3*\\x',0,5),('\\x+6',0,5)],(0,5),(0,16),1,2,xlabel='h',ylabel='euros',caption='A : bleu ; B : vert.')
    graph('rep-14',[],(0,5),(0,10),1,1,points=[('',1,2),('',2,5),('',3,5),('',4,8)],xlabel='min',ylabel='mesure')
    graph('rep-15',[('24-3*\\x',0,8)],(0,8),(0,24),1,3,xlabel='min',ylabel='L',blank=True)

def ray(angle,length=2.5):
    return rf'\draw[geoTrait](0,0)--({angle}:{length});'
def arc(start,end,label,r=.65,color='otMuted'):
    mid=(start+end)/2
    return rf'\draw[{color}]({start}:{r})arc({start}:{end}:{r});\node[geoLabel,font=\scriptsize]at({mid}:{r+.38}){{{label}}};'
def angle_fig(nom,angles,labels,bis=None):
    t='';v=0
    for a,lab in zip(angles,labels):
        t+=ray(v)+arc(v,v+a,lab);v+=a
    t+=ray(v)+dot(0,0,'O','below')
    if bis is not None:t+=rf'\draw[otGreenDark](0,0)--({bis}:2.4);'
    dessin(nom,t,'Les arcs et les données indiquées identifient les angles utilisés.')
    META[nom]={'type':'angles','angles':angles}
def paralleles(nom,theta=68,labels=None,parallel=True,bis=False):
    yy=2.5;xx=yy/tan(radians(theta));t=''
    for (x,y),key in [((0,0),'bas'),((xx,yy),'haut')]:
        tilt=3 if not parallel and key=='haut' else 0
        t+=rf'\begin{{scope}}[shift={{({x},{y})}}]\draw[geoTrait](-2,{-2*tan(radians(tilt))})--(2,{2*tan(radians(tilt))});'
        t+=rf'\draw[geoTrait]({theta+180}:1.5)--({theta}:1.5);'
        for quadrant,lab in (labels or {}).get(key,[]):
            start,end={'NE':(0,theta),'NW':(theta,180),'SW':(180,180+theta),'SE':(180+theta,360)}[quadrant]
            if tilt and quadrant=='NE':start=tilt
            t+=arc(start,end,lab,r=.48)
        if bis and key=='bas':t+=rf'\geoSolution{{\draw[otGreenDark](0,0)--({theta/2}:1.6);}}'
        t+=r'\end{scope}'
    if sqrt(xx*xx+yy*yy)>3:t+=rf'\draw[geoTrait](0,0)--({xx},{yy});'
    t+=rf'\node[left]at(-2,0){{$e$}};\node[left]at({xx-2},{yy}){{$d$}};'
    if parallel:t+=r'\node[right]at(4.1,1.25){$(d)\parallel(e)$};'
    dessin(nom,t,'Schéma de la sécante et des deux droites ; les propriétés connues sont écrites dans l’énoncé.')
    META[nom]={'type':'paralleles','theta':theta,'paralleles':parallel}
def angles():
    angle_fig('cours-angles',[40,50,90],[r'$40^\circ$',r'$50^\circ$',r'$90^\circ$'])
    paralleles('cours-paralleles',68,{'bas':[('NE',r'$a$')],'haut':[('SW',r'$a$')]})
    angle_fig('ang-1',[40],[r'$40^\circ$'])
    FIGURES['ang-1']['tex']=FIGURES['ang-1']['tex'].replace(r'\end{tikzpicture}',r'\node[right]at(2.5,0){A};\node[above]at(40:2.5){B};\end{tikzpicture}')
    angle_fig('ang-2',[35,55],[r'$35^\circ$',answer(r'$55^\circ$')])
    angle_fig('ang-3',[128,52],[r'$128^\circ$',answer(r'$52^\circ$')])
    for name,a in [('ang-4',63),('ang-6',47)]:
        angle_fig(name,[a,180-a,a,180-a],[rf'$ {a}^\circ$',answer(rf'$ {180-a}^\circ$'),answer(rf'$ {a}^\circ$'),answer(rf'$ {180-a}^\circ$')])
    angle_fig('ang-5',[37,37],[answer(r'$37^\circ$'),answer(r'$37^\circ$')],bis=37)
    paralleles('ang-7',68,{'bas':[('NE',r'$68^\circ$')],'haut':[('SW',answer(r'$68^\circ$'))]})
    paralleles('ang-8',68,{'bas':[('NW',r'$112^\circ$')],'haut':[('NW',answer(r'$112^\circ$'))]})
    paralleles('ang-9',72,{'bas':[('NE',r'$72^\circ$')],'haut':[('SW',r'$72^\circ$')]})
    FIGURES['ang-9']['tex']=FIGURES['ang-9']['tex'].replace(r'\node[right]at(4.1,1.25){$(d)\parallel(e)$};','')
    paralleles('ang-10',78,{'bas':[('NE',r'$78^\circ$')],'haut':[('NE',r'$75^\circ$')]},False)
    paralleles('ang-11',56,{'bas':[('NE',answer(r'$56^\circ$'))],'haut':[('NW',r'$124^\circ$')]})
    angle_fig('ang-12',[30,45,105],[r'$30^\circ$',r'$45^\circ$',answer(r'$105^\circ$')])
    angle_fig('ang-13',[110,95,75,80],[r'$110^\circ$',r'$95^\circ$',answer(r'$75^\circ$'),r'$80^\circ$'])
    # Deux droites perpendiculaires à la sécante : angles correspondants droits, codés.
    paralleles('ang-14',90)
    tex=FIGURES['ang-14']['tex'].replace(str(2.5/tan(radians(90))),'0')
    FIGURES['ang-14']['tex']=tex.replace(r'\node[right]at(4.1,1.25){$(d)\parallel(e)$};',r'\draw[otMuted](.25,0)--(.25,.25)--(0,.25) (.25,2.5)--(.25,2.75)--(0,2.75);')
    import re
    assert not re.search(r'\de[-+]\d',FIGURES['ang-14']['tex']),'notation scientifique dans ang-14'
    paralleles('ang-15',74,{'bas':[('NE',answer(r'$74^\circ$'))],'haut':[('NW',r'$106^\circ$')]},bis=True)
def triangles():
    triangle('cours-triangle-angles',6,(2,3),extra=r'\draw[otGreenDark](-.5,3)--(6.5,3);\node[above]at(5,3){parallèle à (AB)};\node at(1.1,.35){$\alpha$};\node at(4.7,.3){$\beta$};\node at(2,2.4){$\gamma$};')
    for name,construct in [('cours-cercle-circonscrit',False),('tri-9',True)]:
        extras=r'\draw[otGreenDark,dashed](3,-.8)--(3,4.5) (-.5,2.75)--(5.5,-.25);\draw[otGreenDark](3,1)circle(3.16227766);\node[above right]at(3,1){O};'
        if construct:extras=r'\geoSolution{'+extras+'}'
        triangle(name,6,(2,4),extra=extras)
    triangle('cours-hauteurs',6,(8,3),extra=r'\draw[otMuted,dashed](6,0)--(8.5,0);\draw[otGreenDark](8,3)--(8,0);\draw[otMuted](7.8,0)--(7.8,.2)--(8,.2);\node[below]at(8,0){H};')
    triangle('cours-mediane',8,(3,3),extra=r'\draw[otGreenDark](3,3)--(4,0);\node[below]at(4,0){M};\node[below]at(2,0){4 cm};\node[below]at(6,0){4 cm};')
    ac=6*sin(radians(67))/sin(radians(65))
    triangle('tri-1',6,(ac*cos(radians(48)),ac*sin(radians(48))),extra=r'\node at(.9,.35){$48^\circ$};\node at(4.7,.3){$67^\circ$};\geoSolution{\node[text=otGreenDark]at(3,2.5){$65^\circ$};}')
    hh=3/tan(radians(22))
    triangle('tri-2',6,(3,hh),extra=rf'\node[geoLabel]at(3,{hh-2.1}){{$44^\circ$}};\node at(1.5,.65){{{answer(r"$68^\circ$")}}};\node at(4.5,.65){{{answer(r"$68^\circ$")}}};')
    cx=(6*6+4*4-5*5)/12;cy=sqrt(16-cx*cx)
    triangle('tri-3',6,(cx,cy),{(0,1):'6 cm'},extra=r'\geoSolution{\draw[otGreenDark,dashed](4,0)arc(0:90:4);\draw[otGreenDark,dashed](1,0)arc(180:90:5);}',construction=True)
    triangle('tri-4',9,(3,4),{(0,1):'9 cm'},extra=r'\draw[otMuted,dashed](3,4)--(3,0);\node[right]at(3,2){4 cm};\draw[otMuted](3,0)--(3.2,0)--(3.2,.2)--(3,.2);')
    triangle('tri-5',6,(1,4),extra=r'\draw[geoTrait](1,4)--(3,0);\node[below]at(3,0){M};\node[below]at(1.5,0){3};\node[below]at(4.5,0){3};')
    triangle('tri-6',5,(1.5,3*sin(radians(60))),{(0,1):'5 cm'},extra=r'\geoSolution{\node at(.8,.3){$60^\circ$};\node[left]at(.75,1.3){3 cm};}',construction=True)
    ac=6*sin(radians(60))/sin(radians(70));cx=ac*cos(radians(50));cy=ac*sin(radians(50))
    triangle('tri-7',6,(cx,cy),{(0,1):'6 cm'},extra=r'\geoSolution{\node at(.8,.3){$50^\circ$};\node at(5.1,.3){$60^\circ$};}',construction=True)
    triangle('tri-8',6,(8,3),extra=r'\geoSolution{\draw[otGreenDark,dashed](6,0)--(8.5,0);\draw[otGreenDark](8,3)--(8,0);\node[below]at(8,0){H};\draw[otGreenDark](7.8,0)--(7.8,.2)--(8,.2);}')
    triangle('tri-10',8,(2,6),{(0,1):'8 cm'},extra=r'\draw[otMuted,dashed](2,6)--(2,0);\node[right]at(2,3){'+answer('6 cm')+r'};\node[geoLabel]at(4.4,1.3){aire : 24 cm$^2$};')
    triangle('tri-11',10,(3,7),extra=r'\draw[geoTrait](3,7)--(5,0);\node[below]at(5,0){M};\node[below]at(2.5,0){5 cm};\node[below]at(7.5,0){5 cm};\geoSolution{\node at(3,2){17,5};\node at(6,2){17,5};}')
    # Corrigé : orthocentre en A, médiatrices de [AB] et [AC], centre O milieu de l'hypoténuse.
    triangle('tri-12',3,(0,4),extra=r'\draw[otMuted](.2,0)--(.2,.2)--(0,.2);\geoSolution{\node[anchor=south west,text=otGreenDark,font=\scriptsize,inner sep=1pt]at(.3,.3){H = A};\draw[otGreenDark,dashed](1.5,-.7)--(1.5,4.7) (-.7,2)--(3.7,2);\draw[otGreenDark](1.5,2)circle(2.5);\fill[otGreenDark](1.5,2)circle(1.8pt)node[above right,geoLabel]{O};}')
    # Le cercle agrandit le dessin : échelle réduite pour garder la taille d'origine.
    FIGURES['tri-12']['tex']=FIGURES['tri-12']['tex'].replace(r'\begin{scope}[scale=0.775]',r'\begin{scope}[scale=0.6]',1)
    assert r'[scale=0.6]' in FIGURES['tri-12']['tex']
    META['tri-12']['cercle']=((1.5,2),2.5)
    triangle('tri-13',6,(3,4),extra=r'\draw[geoTrait](3,4)--(3,0);\node[below]at(3,0){M};\node[below]at(1.5,0){3 cm};\node[below]at(4.5,0){3 cm};\geoSolution{\draw[otGreenDark](3,0)--(3.2,0)--(3.2,.2)--(3,.2);}')
    dessin('tri-14',r'\begin{scope}[scale=.55]\draw[geoTrait](0,0)--(8,0);\node[below]at(4,0){8 cm};\draw[otMuted,dashed](0,0)circle(3);\draw[otMuted,dashed](8,0)circle(4);\end{scope}','Pour les côtés 3, 4 et 8, les cercles de construction ne se rencontrent pas.')
    cx=12-sqrt(75)
    triangle('tri-15',12,(cx,5),{(0,1):'12 cm',(1,2):'10 cm'},extra=rf'\draw[otMuted,dashed]({cx},5)--({cx},0);\draw[otMuted,<->](-1,0)--node[left]{{5 cm}}(-1,5);\geoSolution{{\draw[otGreenDark]({cx},5)--(6,0);\node[above right]at(6,0){{M}};}}')
def symetries():
    def sym(nom,pts,kind='centrale',center=(0,0),show=False):
        if kind=='centrale':imgs=[(lab+"'",2*center[0]-x,2*center[1]-y) for lab,x,y in pts];extra=dot(*center,'O','below left','otGreenDark')
        elif kind=='verticale':imgs=[(lab+"'",-x,y) for lab,x,y in pts];extra=r'\draw[otGreenDark,line width=1pt](0,-4)--(0,4);'
        elif kind=='horizontale':imgs=[(lab+"'",x,-y) for lab,x,y in pts];extra=r'\draw[otGreenDark,line width=1pt](-5,0)--(5,0);'
        else:imgs=[(lab+"'",y,x) for lab,x,y in pts];extra=r'\draw[otGreenDark,line width=1pt](-4,-4)--(4,4);'
        if len(pts)>=3:
            extra+=poly([(x,y) for l,x,y in pts])
            t=poly([(x,y) for l,x,y in imgs],'otGreenDark');extra+=t if show else r'\geoSolution{'+t+'}'
        coord(nom,points=pts+(imgs if show else []),sol=[] if show else imgs,extra=extra)
        META[nom].update(type='symetrie',nature=kind,centre=center,originaux=pts,images=imgs)
    sym('cours-axiale',[('A',-3,2)],'verticale',show=True)
    sym('cours-centrale',[('A',-2,1),('B',-3,3),('C',-1,2)],show=True)
    sym('sym-1',[('A',-3,2)],'verticale');sym('sym-2',[('B',2,2)],'horizontale')
    sym('sym-3',[('A',2,1)]);sym('sym-4',[('P',0,0)])
    sym('sym-5',[('A',-3,-1),('B',-1,-1)]);sym('sym-6',[('A',1,3)],'diagonale')
    sym('sym-7',[('A',-3,-1),('B',-1,-1),('C',-2,2)])
    coord('sym-8',[('A',-2,1),("A'",4,3)],[('O',1,2)],extra=r'\draw[geoTrait](-2,1)--(4,3);')
    sym('sym-9',[('A',-3,-1),('B',-1,-1)])
    FIGURES['sym-9']['tex']=FIGURES['sym-9']['tex'].replace(r'\end{scope}',r'\draw[geoTrait](-5,-1)--(5,-1);\geoSolution{\draw[otGreenDark](-5,1)--(5,1);}\end{scope}')
    sym('sym-10',[('C',-2,0)])
    FIGURES['sym-10']['tex']=FIGURES['sym-10']['tex'].replace(r'\end{scope}',r'\draw[geoTrait](-2,0)circle(2);\geoSolution{\draw[otGreenDark](2,0)circle(2);}\end{scope}')
    sym('sym-11',[('A',3,1)]);sym('sym-12',[('A',-3,-1),('B',0,-1),('C',-1,2)])
    rect('sym-13','6 cm','4 cm',r'\node[below left]at(0,0){A};\node[below right]at(5,0){B};\node[above right]at(5,2.6){C};\node[above left]at(0,2.6){D};',r'\draw[otGreenDark](0,0)--(5,2.6) (5,0)--(0,2.6);\node[above]at(2.5,1.3){O};')
    sym('sym-14',[('A',-3,-1),('B',-1,-1),('C',-2,2)])
    coord('sym-15',[('A',-3,1),("A'",3,-1),('B',-1,3),("B'",1,-1)],extra=r'\draw[geoTrait](-3,1)--(3,-1) (-1,3)--(1,-1);\geoSolution{\fill[otGreenDark](0,0)circle(2pt);\fill[otGreenDark](0,1)circle(2pt);}')
def parallelogrammes():
    diag=r'\draw[otMuted,dashed](0,0)--(7.5,3) (6,0)--(1.5,3);\node[above]at(3.75,1.5){O};'
    paral('cours-parallelogramme',extra=diag)
    for n in [1,2,6,7,8,11,12]:
        extra=diag if n in [2,7,8] else ''
        extra+={1:r'\node[below]at(3,0){7 cm};\node[right]at(6.75,1.5){4 cm};',
                2:r'\node at(4.8,2.7){$AC=10$ cm};\node at(1.5,.8){$BD=6$ cm};',
                11:r'\node[below]at(3,0){12 cm};\draw[otMuted,dashed](1.5,3)--(1.5,0);\node[left]at(1.5,1.5){$h$};\node at(4,1.8){54 cm$^2$};',
                12:r'\node[below]at(3,0){1,2 m};\draw[otMuted,dashed](1.5,3)--(1.5,0);\node[right]at(1.5,1.5){35 cm};'}.get(n,'')
        paral('para-'+str(n),extra=extra,construction=n in [6,7])
    paral('para-4',extra=r'\node[below]at(3,0){8 cm};\draw[otMuted,dashed](1.5,3)--(1.5,0);\node[right]at(1.5,1.5){3 cm};')
    paral('cours-aire-parallelogramme',extra=r'\draw[otMuted,dashed](1.5,3)--(1.5,0);\node[below]at(3,0){base $b$};\node[right]at(1.5,1.5){$h$};')
    rect('para-3','', '',r'\draw[otMuted](.2,0)--(.2,.2)--(0,.2);')
    for name,a,b in [('para-5',3,2),('para-9',3,2),('para-10',2.3,2.3),('para-15',5,3)]:
        pts=[(-a,0),(0,-b),(a,0),(0,b)]
        t=poly(pts)+rf'\draw[otMuted,dashed](-{a},0)--({a},0) (0,-{b})--(0,{b});\draw[otMuted](.2,0)--(.2,.2)--(0,.2);'
        for (x,y),lab in zip(pts,'ABCD'):t+=dot(x,y,lab)
        if name=='para-5':t+=r'\node[above left]at(-1.5,1){5 cm};\node[below left]at(-1.5,-1){5 cm};'
        if name=='para-15':t+=r'\node[above]at(2.5,0){5 cm};\node[right]at(0,1.5){3 cm};'
        dessin(name,t);META[name]={'type':'losange','points':pts}
    dessin('para-13',r'\draw[geoTrait](0,0)rectangle(6,3);\draw[geoTrait](0,3)--(3,5.25)--(6,3);\draw[otMuted,dashed](3,3)--(3,5.25);\node[below]at(3,0){8 cm};\node[left]at(0,1.5){4 cm};\node[right]at(3,4){3 cm};')
    dessin('para-14',poly([(-2,0),(0,-1),(2,0),(0,2)])+r'\draw[otMuted,dashed](-2,0)--(2,0) (0,-1)--(0,2);\node[right]at(0,1){2};\node[right]at(0,-.5){1};\node[above]at(-1,0){2};\node[above]at(1,0){2};\draw[otMuted](.15,0)--(.15,.15)--(0,.15);')

def prisme(nom,b='6 cm',ht='4 cm',L='9 cm'):
    t=r'\coordinate(A)at(0,0);\coordinate(B)at(3,0);\coordinate(C)at(0,2.4);\coordinate(D)at(2,1.2);\coordinate(E)at(5,1.2);\coordinate(F)at(2,3.6);\draw[geoTrait](A)--(B)--(C)--cycle (B)--(E)--(F)--(C);\draw[otMuted,dashed](A)--(D)--(E) (D)--(F);'
    t+=rf'\path(A)--node[below]{{{b}}}(B);\path(A)--node[left]{{{ht}}}(C);\path(B)--node[below right]{{{L}}}(E);\draw[otMuted](.18,0)--(.18,.18)--(0,.18);'
    dessin(nom,t,'Prisme droit à base triangulaire ; les arêtes cachées sont en pointillés.')
def net_prisme(nom,solution=True):
    # Bande de rectangles de largeurs 3, 4 et 5, avec deux triangles 3-4-5.
    t=r'\begin{scope}[scale=.48]\draw[geoTrait](0,0)rectangle(12,6);\draw[geoTrait](3,0)--(3,6) (7,0)--(7,6);\draw[geoTrait](0,0)--(0,-4)--(3,0) (0,6)--(0,10)--(3,6);'
    for x,lab in [(1.5,'3 cm'),(5,'4 cm'),(9.5,'5 cm')]:
        node=rf'\node at({x},3){{{lab}}};'
        t+=r'\geoSolution{'+node+'}' if solution else node
    t+=r'\node[right]at(12,3){6 cm};\end{scope}'
    dessin(nom,t,'Deux triangles 3-4-5 et trois rectangles ; les dimensions manquantes sont ajoutées au corrigé.')
def net_cyl(nom,r=3,h=7,sol=True):
    t=r'\draw[geoTrait](0,0)rectangle(5.5,2);\draw[geoTrait](1.1,-1.4)circle(.85);\draw[geoTrait](4.4,-1.4)circle(.85);'
    node=rf'\node[above]at(2.75,2){{$ {2*r}\pi $ cm}};\node[right]at(5.5,1){{{h} cm}};\node at(1.1,-1.4){{$r={r}$ cm}};\node at(4.4,-1.4){{$r={r}$ cm}};'
    t+=r'\geoSolution{'+node+'}' if sol else node
    dessin(nom,t,'Pièces montrées séparément : le bord de chaque disque rejoint un grand bord du rectangle.')
def solides():
    pave('cours-pave','','','')
    prisme('cours-prisme','','','')
    # Un visuel côte à côte, avec les mêmes dessins réutilisés à échelle réduite.
    a=FIGURES.pop('cours-pave')['tex'];b=FIGURES.pop('cours-prisme')['tex']
    figure('cours-solides',r'\resizebox{.92\linewidth}{!}{'+a+r'\hspace{5mm}'+b+'}','A : pavé droit ; B : prisme droit triangulaire.')
    figure('sol-1',FIGURES['cours-solides']['tex'],FIGURES['cours-solides']['legende'])
    net_prisme('cours-patrons',False)
    cylindre('cours-cylindre','3 cm','8 cm')
    pave('sol-2','4 cm','4 cm','4 cm')
    pave('sol-3','7 cm','5 cm','3 cm')
    dessin('sol-4',r'\draw[geoTrait](0,0)circle(1.7);\draw[geoTrait](0,0)--node[above]{4 cm}(1.7,0);')
    pave('sol-5','1 dm','1 dm','1 dm',r'\node at(2.5,1.3){1 dm$^3=1$ L};')
    FIGURES['sol-5']['legende']='Cube unité pour les conversions ; la question porte sur 2,5 fois ce volume.'
    prisme('sol-6','6 cm','4 cm','9 cm')
    cylindre('sol-7','2 cm','10 cm')
    cylindre('sol-8',answer('3 cm'),'5 cm')
    net_prisme('sol-9')
    net_cyl('sol-10')
    t=r'\begin{scope}[x=1.1cm,y=1.1cm]'
    for row,vals in enumerate([[2,1,3],[1,2,0]]):
        for col,val in enumerate(vals):
            t+=rf'\draw[geoTrait]({col},{-row})rectangle++(1,1);\node at({col+.5},{-row+.5}){{{val}}};'
    t+=r'\node[above]at(1.5,1){Vue de dessus : hauteur des piles};\end{scope}'
    dessin('sol-11',t,'Chaque case précise toute la pile, y compris les cubes cachés.')
    pave('sol-12','60 cm','30 cm','25 cm')
    pave('sol-13','10 cm','8 cm','6 cm')
    a=FIGURES['sol-13']['tex'];cylindre('sol-13-b','4 cm','10 cm');b=FIGURES.pop('sol-13-b')['tex']
    FIGURES['sol-13']['tex']=r'\resizebox{.92\linewidth}{!}{'+a+r'\hspace{5mm}'+b+'}'
    # Perspective à compléter : face avant ABC en vraie grandeur et arête fuyante [BE].
    pts={'A':(0,0),'B':(3,0),'C':(0,2.4),'D':(2,1.2),'E':(5,1.2),'F':(2,3.6)}
    t=''.join(rf'\coordinate({k})at({x},{y});' for k,(x,y) in pts.items())
    t+=r'\draw[geoTrait](A)--(B)--(C)--cycle (B)--(E);\draw[otMuted](.18,0)--(.18,.18)--(0,.18);'
    t+=r'\node[below left]at(A){A};\node[below]at(B){B};\node[left]at(C){C};\node[right]at(E){E};'
    t+=r'\geoSolution{\draw[otGreenDark,line width=.85pt](C)--(F)--(E);\draw[otGreenDark,dashed,line width=.75pt](A)--(D)--(E) (D)--(F);\node[above left,text=otGreenDark]at(D){D};\node[above,text=otGreenDark]at(F){F};}'
    dessin('sol-14',t,'Perspective cavalière commencée : face avant ABC en vraie grandeur et arête fuyante [BE].')
    META['sol-14']={'type':'perspective','points':pts}
    t=r'\begin{scope}[scale=.4]\draw[geoTrait](0,0)rectangle(12,8);\draw[geoTrait](0,0)--(0,-5)--(12,-5)--(12,0);\draw[geoTrait](0,8)--(0,13)--(12,13)--(12,8);\draw[geoTrait](0,0)--(-5,0)--(-5,8)--(0,8);\draw[geoTrait](12,0)--(17,0)--(17,8)--(12,8);\node at(6,4){12 cm $\times$ 8 cm};\node at(6,-2.5){5 cm};\node at(-2.5,4){5 cm};\end{scope}'
    dessin('sol-15',t,'Patron sans couvercle, constitué du fond et de quatre faces latérales.')
def statistiques():
    secteurs('cours-statistiques',[180,108,72],['À pied','Vélo','Bus'])
    for name,blank,ang,labs in [('stat-7',True,[180,108,72],['A','B','C']),('stat-8',False,[90,270],[r'$90^\circ$','Autres']),('stat-15',True,[144,108,72,36],['À pied','Bus','Vélo','Autres'])]:
        secteurs(name,ang,labs,blank)
    pol=''.join(rf'\draw[otNavy,line width=3pt]({i},0)--({i},{v});' for i,v in enumerate([2,3,4,1]))
    graph('stat-4',[],(-.5,3.5),(0,5),1,1,xlabel='livres',ylabel='élèves',poly=pol)
    t=r'\draw[otMuted,->](0,0)--(0,3.6);\foreach\y/\v in{0/40,1/44,2/48,3/52}{\draw[otMuted](-.1,\y)--(.1,\y);\node[left]at(0,\y){\v};}\fill[otNavy!45](1,0)rectangle(2,2);\fill[otGreen!55](3,0)rectangle(4,3);\node[below]at(1.5,0){A};\node[below]at(3.5,0){B};\node[left]at(-.3,.2){axe tronqué};'
    dessin('stat-14',t,'L’axe vertical commence à 40 ; la longueur visible des barres ne représente pas les effectifs entiers.')
    urne('cours-probabilites',['R']*3+['B']*2)
    # Échelle de probabilité : repères 0, 1/2 et 1 ; les évènements sont placés au corrigé.
    t=r'\draw[otMuted,line width=.8pt](0,0)--(9,0);'
    for x,lab in [(0,'0'),(4.5,r'$1/2$'),(9,'1')]:
        t+=rf'\draw[otMuted]({x},-.12)--({x},.12);\node[below,font=\scriptsize]at({x},-.15){{{lab}}};'
    t+=r'\node[below,font=\scriptsize,text=otMuted]at(0,-.62){impossible};\node[below,font=\scriptsize,text=otMuted]at(4.5,-.62){une chance sur deux};\node[below,font=\scriptsize,text=otMuted]at(9,-.62){certain};'
    places=[('A',0),('E',.45),('C',4.5),('D',8.55),('B',9)]
    t+=r'\geoSolution{'+''.join(rf'\fill[otGreenDark]({x},0)circle(2pt);\node[above,text=otGreenDark]at({x},.16){{{lab}}};' for lab,x in places)+'}'
    dessin('proba-3',t,'Échelle de probabilité de 0 à 1 ; les évènements sont placés au corrigé.')
    META['proba-3']={'type':'echelle','places':{lab:x/9 for lab,x in places}}
    urne('proba-7',['R']*4+['B']*3+['V'])
    secteurs('proba-8',[45]*8,[str(i) for i in range(1,9)])
    urne('proba-9',['R1','R2','R3','B1','B2','V1'])
    urne('proba-11',['R']*2+['B']*3)
    # Les couleurs à déterminer ne sont pas données dans l'énoncé.
    t=r'\draw[geoTrait](-.5,-.5)rectangle(5,2.5);'
    for i in range(12):
        x=i%4*1.3;y=2-i//4
        t+=rf'\geoEnonce{{\draw[otMuted]({x},{y})circle(.28);}}\geoSolution{{\filldraw[draw=otMuted,fill={"otOrange!50" if i<4 else "otNavy!30"}]({x},{y})circle(.28);}}'
    dessin('proba-13',t,'Douze places à répartir entre boules rouges et bleues ; la répartition est ajoutée au corrigé.')
def programmes():
    for i,code in SCRIPTS.items():
        ls=[(0,'quand le drapeau est cliqué','evenement')]
        if i in [5,7,8,9,10,11,12,13]:ls+=[(0,'aller au départ ; direction vers la droite ; stylo baissé','mouvement')]
        ls+=lignes(code)
        if i==15:
            t=r'\geoEnonce{\node[draw=otMuted,rounded corners,inner sep=4mm]at(3,0){Construire les blocs demandés.};}\geoSolution{'+pile(ls)+'}'
        else:t=pile(ls)
        if i in [6,13]:
            fixed=[('input',),('say','3*r+4')] if i==6 else [('repeat',4,[('move',50),('turn',90)])]
            fixed_lines=ls[:1]+([] if i==6 else ls[1:2])+lignes(fixed)
            t=r'\geoEnonce{'+t+r'}\geoSolution{'+pile(fixed_lines)+'}'
        if i==10:
            common=[ls[0],(0,'départ ; droite ; stylo baissé','mouvement')]
            t=r'\node[above]at(2.5,.3){A};\node[above]at(9,.3){B};'+pile(common+lignes(code),width=5.6)+pile(common+lignes([('turn',90),('move',40)]),x=6.5,width=5.6)
            t+=r'\geoSolution{\draw[otGreenDark,->](1,-4.6)--(2.8,-4.6);\draw[otGreenDark,->](8,-4.6)--(8,-2.8);}'
        if i in [7,8,9,11,12,13]:
            trace=executer(code)['trace']
            if i==13:trace=executer([('repeat',4,[('move',50),('turn',90)])])['trace']
            xs=[x for x,y in trace];ys=[y for x,y in trace];sc=min(2.3/max(max(xs)-min(xs),1),2.3/max(max(ys)-min(ys),1))
            shape=r'\draw[otGreenDark,line width=1pt]'+'--'.join(f'({9+(x-min(xs))*sc},{-1+(y-min(ys))*sc})' for x,y in trace)+';'
            t+=r'\geoSolution{'+shape+'}'
        dessin('prog-'+str(i),t,'Blocs de type Scratch ; les indentations et la ligne « fin » délimitent la répétition.')
        META['prog-'+str(i)]={'type':'programme','script':i}
    figure('cours-programme',FIGURES['prog-2']['tex'],FIGURES['prog-2']['legende'])
    figure('cours-boucle',FIGURES['prog-7']['tex'],FIGURES['prog-7']['legende'])
def annexes():
    triangle('defi-triangle-partages',12,(3,5),{(0,1):'12 cm'},extra=r'\draw[otMuted,dashed](3,5)--(3,0);\draw[otMuted,<->](-1,0)--node[left]{5 cm}(-1,5);\draw[geoTrait](3,5)--(6,0);\node[below]at(6,0){M};\geoSolution{\draw[otGreenDark](3,5)--(3,0);\node[below,text=otGreenDark]at(3,0){N};}')
    triangle('bilan-triangle',10,(3,6),{(0,1):'10 cm'},extra=r'\draw[otMuted,dashed](3,6)--(3,0);\draw[otMuted,<->](-1,0)--node[left]{6 cm}(-1,6);\draw[geoTrait](3,6)--(5,0);\node[below]at(5,0){M};\geoSolution{\draw[otGreenDark](3,6)--(2.5,0);\node[below]at(2.5,0){N};}')
    secteurs('bilan-enquete',[144,108,108],['Vélo','Bus','À pied'],True)
    pave('bilan-bac','40 cm','25 cm','30 cm')
    graph('bilan-tarifs',[('4*\\x',0,4),('6+2*\\x',0,4)],(0,4),(0,16),1,2,xlabel='h',ylabel='euros',blank=True,caption='A : bleu ; B : vert dans le corrigé.')
    rect('bilan-rectangle','8 cm','5 cm',r'\draw[otMuted,dashed](0,0)--(5,2.6) (5,0)--(0,2.6);\node[above]at(2.5,1.3){O};\node[below left]at(0,0){A};\node[below right]at(5,0){B};\node[above right]at(5,2.6){C};\node[above left]at(0,2.6){D};')
    cylindre('bilan-cylindre','3 cm','12 cm')
    code=[('repeat',3,[('move',40),('turn',90)])]
    common=[(0,'quand le drapeau est cliqué','evenement'),(0,'départ ; direction vers la droite ; stylo baissé','mouvement')]
    t=r'\geoEnonce{'+pile(common+lignes(code))+r'}\geoSolution{'+pile(common+lignes([('repeat',4,[('move',40),('turn',90)])]))+'}'
    t+=r'\geoSolution{\draw[otGreenDark](9,-2)--(11,-2)--(11,0)--(9,0)--cycle;}'
    dessin('bilan-script',t,'Le corrigé montre le carré après réparation du nombre de répétitions.')
def write_all(root):
    for f in [nombres,graphiques,angles,triangles,symetries,parallelogrammes,solides,statistiques,programmes,annexes]:f()
    # Le visuel du rectangle doit bien avoir des diagonales de même longueur.
    FIGURES.pop('para-8')
    rect('para-8','','',r'\draw[otMuted,dashed](0,0)--(5,2.6) (5,0)--(0,2.6);\node[above]at(2.5,1.3){O};\node[above]at(3.8,2){8 cm};\node[above]at(1.2,2){8 cm};')
    # Cours : montrer aussi les aires et le tracé explicatifs.
    for name in ['cours-distrib','cours-boucle']:
        FIGURES[name]['tex']=r'\begingroup\otGeoCorrigetrue '+FIGURES[name]['tex']+r'\endgroup'
    # Le patron du pavé complète les patrons de prisme et de cylindre des exercices.
    FIGURES['cours-patrons']['tex']=r'\begin{tikzpicture}[font=\small,scale=.75]\draw[geoTrait](0,0)rectangle(4,2);\draw[geoTrait](0,0)--(0,-1.5)--(4,-1.5)--(4,0);\draw[geoTrait](0,2)--(0,3.5)--(4,3.5)--(4,2);\draw[geoTrait](0,0)--(-1.5,0)--(-1.5,2)--(0,2);\draw[geoTrait](4,0)--(5.5,0)--(5.5,2)--(4,2);\draw[geoTrait](0,3.5)--(0,5.5)--(4,5.5)--(4,3.5);\node at(2,1){fond};\node at(2,4.5){dessus};\node at(2,-.75){côté};\node at(2,2.75){côté};\node[rotate=90]at(-.75,1){côté};\node[rotate=90]at(4.75,1){côté};\end{tikzpicture}'
    FIGURES['cours-patrons']['legende']='Patron d’un pavé droit : six rectangles avec les bords correspondants de même longueur.'
    # Faces frontales carrées pour les cubes en perspective cavalière.
    for nom,label in [('sol-2','4 cm'),('sol-5','1 dm'),('puiss-12','6 cubes')]:
        FIGURES[nom]['tex']=r'\begin{tikzpicture}[font=\small]\draw[geoTrait](0,0)rectangle(3,3);\draw[geoTrait](0,3)--(1,4)--(4,4)--(4,1)--(3,0) (3,3)--(4,4);\draw[otMuted,dashed](0,0)--(1,1)--(4,1) (1,1)--(1,4);\node[below]at(1.5,0){'+label+r'};\node[left]at(0,1.5){'+label+r'};\node[below right]at(3.5,.5){'+label+r'};\end{tikzpicture}'
    for nom in ['sym-5','sym-12']:
        FIGURES[nom]['legende']='Quadrillage de principe sans unité de longueur imposée ; le demi-tour conserve les mesures données dans le texte.'
    # Dans ces exercices le sommet principal s'appelle A et la base est [BC].
    for nom in ['tri-2','tri-5','tri-11','tri-13']:
        import re
        FIGURES[nom]['tex']=re.sub(r'(?<=\$ )([ABC])(?= \$)',lambda m:{'A':'B','B':'C','C':'A'}[m.group(1)],FIGURES[nom]['tex'])
        META[nom]['noms']=['B','C','A']
    FIGURES['tri-13']['tex']=FIGURES['tri-13']['tex'].replace(r'\end{scope}',r'\geoSolution{\fill[otGreenDark](3,.875)circle(1.5pt)node[left,geoLabel]{O};}\end{scope}')
    # Les trois hauteurs du triangle obtus sont visibles et concourent en H.
    FIGURES['cours-hauteurs']['tex']=r'\begin{tikzpicture}[font=\small,scale=.8]\draw[geoTrait](0,0)--(4,0)--(5,2)--cycle;\node[below left]at(0,0){A};\node[below]at(4,0){B};\node[above]at(5,2){C};\draw[otMuted,dashed](4,0)--(5.4,0) (4,0)--(3.1,-1.8);\draw[otGreenDark,dashed](5,2)--(5,-2.5) (0,0)--(5,-2.5) (3.44827586,1.37931034)--(5,-2.5);\fill[otGreenDark](5,-2.5)circle(2pt)node[below]{H};\node[right]at(5,0){K};\draw[otMuted](4.8,0)--(4.8,.2)--(5,.2);\end{tikzpicture}'
    FIGURES['cours-hauteurs']['legende']='Les trois hauteurs vertes se rencontrent en H, extérieur au triangle ; K est le pied de la hauteur issue de C.'
    META['cours-hauteurs']={'type':'triangle','points':[(0,0),(4,0),(5,2)],'orthocentre':(5,-2.5)}
    out=root/'figures';out.mkdir(exist_ok=True)
    for name,data in FIGURES.items():
        content=data['tex']+r'\par\vspace{1.5mm}{\otRegular\fontsize{8}{10}\selectfont\color{otMuted}'+data['legende']+'\\par}\n'
        (out/(name+'.tex')).write_text(content,encoding='utf8')
