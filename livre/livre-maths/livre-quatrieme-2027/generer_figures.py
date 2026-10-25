"""Figures vectorielles originales ; les réponses sont ajoutées au corrigé.

Édition 2027-2028 (programme 2026). Les figures géométriques enregistrent
leurs données dans GEOMETRIE (milieux, parallélismes, perpendicularités,
cercles) pour les contrôles de verifier_figures.py.
"""
from pathlib import Path
from math import sqrt,sin,cos,radians,atan2,degrees,acos,hypot
from modele import FIGURES,figure,tableau
from outils_figures import dessin,axes,graph,pave,cylindre,cone,pile
from donnees_scripts import SCRIPTS
GEOMETRIE={};SECTEURS={}

def reponse(txt):
    return r'\geoEnonce{?}\geoSolution{\textcolor{otGreenDark}{'+txt+'}}'

def polygone(pts,color='otNavy'):
    return r'\draw['+color+',line width=.85pt]'+'--'.join(f'({x:.3f},{y:.3f})' for x,y in pts)+'--cycle;'

# ---------------------------------------------------------------------
# Outils de géométrie : points, codages, droites prolongées
# ---------------------------------------------------------------------
def c(p):return f'({p[0]:.3f},{p[1]:.3f})'
def mil(p,q):return ((p[0]+q[0])/2,(p[1]+q[1])/2)
def vec(p,q):return (q[0]-p[0],q[1]-p[1])
def unit(v):
    n=hypot(*v);return (v[0]/n,v[1]/n)
def add(p,v,k=1):return (p[0]+k*v[0],p[1]+k*v[1])
def echelle(P,k,dx=0,dy=0):return {n:(x*k+dx,y*k+dy) for n,(x,y) in P.items()}

def points(P,noms,anchors,color='otNavy'):
    tex=''
    for n in noms:
        lab=n.replace("'",r"^{\prime}")
        tex+=rf'\fill[{color}]{c(P[n])}circle(1.3pt)node[{anchors.get(n,"above")},geoLabel,font=\small]{{$ {lab} $}};'
    return tex

def seg(P,chemin,style='geoTrait'):
    return r'\draw['+style+']'+'--'.join(c(P[n]) for n in chemin.split('-'))+';'

def coche(p,q,n=1,color='otNavy'):
    m=mil(p,q);u=unit(vec(p,q));nr=(-u[1],u[0]);tex=''
    for k in range(n):
        o=(k-(n-1)/2)*.075;ce=add(m,u,o)
        tex+=rf'\draw[{color},line width=.7pt]{c(add(ce,nr,-.11))}--{c(add(ce,nr,.11))};'
    return tex

def droit(a,b,cc,color='otMuted',s=.17):
    u=unit(vec(b,a));v=unit(vec(b,cc))
    p1=add(b,u,s);p3=add(b,v,s);p2=add(p1,v,s)
    return rf'\draw[{color},line width=.6pt]{c(p1)}--{c(p2)}--{c(p3)};'

def droite(p,q,t1=.25,t2=.25,style='geoDonnee'):
    v=vec(p,q)
    return rf'\draw[{style}]{c(add(p,v,-t1))}--{c(add(q,v,t2))};'

def arc_angle(b,a,cc,r=.45,label='',color='otMuted',lr=None,font=r'\scriptsize'):
    t1=degrees(atan2(a[1]-b[1],a[0]-b[0]));t2=degrees(atan2(cc[1]-b[1],cc[0]-b[0]))
    if t2<t1:t1,t2=t2,t1
    if t2-t1>180:t1,t2=t2,t1+360
    tex=rf'\draw[{color}]{c(add(b,(cos(radians(t1)),sin(radians(t1))),r))}arc({t1:.2f}:{t2:.2f}:{r});'
    if label:
        tm=radians((t1+t2)/2);rr=lr or r+.32
        tex+=rf'\node[font={font},text={color}]at{c(add(b,(cos(tm),sin(tm)),rr))}{{{label}}};'
    return tex

def texte_seg(p,q,txt,d=.3,side=1,font=r'\scriptsize',color='otInk',t=.5):
    m=add(p,vec(p,q),t);u=unit(vec(p,q));nr=(-u[1]*side,u[0]*side)
    return rf'\node[geoLabel,font={font},text={color}]at{c(add(m,nr,d))}{{{txt}}};'

def registre(nom,P,**donnees):
    GEOMETRIE[nom]=dict(points=dict(P),**donnees)

# ---------------------------------------------------------------------
# Triangles et figures numériques reprises de l’édition précédente
# ---------------------------------------------------------------------
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
    GEOMETRIE[nom]={'points':{'A':pts[0],'B':pts[1],'C':pts[2]},'triangle':pts,'longueurs':lengths,'rectangle':right or proof_right}
    dessin(nom,tex+extra)

def carre(nom,side='?',inside='',opening=False):
    t=r'\draw[geoTrait](0,0)rectangle(3,3);'
    t+=rf'\node[below]at(1.5,0){{{side}}};\node[align=center]at(1.5,1.5){{{inside}}};'
    if opening:t+=r'\draw[white,line width=2pt](.8,0)--(1.5,0);\draw[otMuted,|<->|](.8,-.55)--node[below]{2 m}(1.5,-.55);'
    dessin(nom,t)

def rectangles(nom,L,H,extra='',answer=''):
    tex=r'\draw[geoTrait](0,0)rectangle(5,2.5);'+rf'\node[below]at(2.5,0){{{L}}};\node[left]at(0,1.25){{{H}}};'+extra
    if answer:tex+=r'\geoSolution{'+rf'\node[text=otGreenDark]at(2.5,1.25){{{answer}}};'+'}'
    dessin(nom,tex)

def secteurs(nom,angles,labels,legende='Les angles des secteurs représentent leurs parts respectives du total.',extra=''):
    assert abs(sum(angles)-360)<1e-8
    SECTEURS[nom]=angles
    colors=['otGreen!65','otNavy!45','otOrange!65','otGreen!25','otNavy!15']
    t='';start=0
    for i,(a,lab) in enumerate(zip(angles,labels)):
        end=start+a;mid=(start+end)/2
        rr=1.05 if a>=40 else 1.85
        t+=rf'\filldraw[draw=white,line width=1pt,fill={colors[i%len(colors)]}](0,0)--({start}:1.55)arc({start}:{end}:1.55)--cycle;\node[font=\scriptsize,align=center]at({mid}:{rr}){{{lab}}};'
        start=end
    dessin(nom,t+extra,legende)

def urs(nom,items):
    tex=r'\draw[otMuted,line width=.8pt](-.6,2.1)--(-.6,-.6)--(5,-.6)--(5,2.1);'
    colors={'R':'otOrange!70','B':'otNavy!40','V':'otGreen!60'}
    for i,l in enumerate(items):
        x=(i%4)*1.3;y=1.3-(i//4)*1.3
        tex+=rf'\node[circle,draw=otMuted,fill={colors[l[0]]},minimum size=8mm,font=\small]at({x},{y}){{{l}}};'
    dessin(nom,tex,'Les objets sont supposés indiscernables au toucher ; les lettres identifient leur couleur.')

def barres_ratio(nom,parts,valeur,total,unite,noms,blank):
    """Schéma en barres d’un partage selon un ratio."""
    tex='';w=.85
    for r,(k,n) in enumerate(zip(parts,noms)):
        y=-r*.85
        tex+=rf'\node[anchor=east,font=\small]at(-.15,{y+.3:.2f}){{{n}}};'
        for i in range(k):
            tex+=rf'\draw[otNavy,fill=otGreen!{30 if r==0 else 15}]({i*w:.2f},{y:.2f})rectangle++({w},.6);'
            val=rf'\node[font=\scriptsize]at({i*w+w/2:.3f},{y+.3:.2f}){{{valeur}}};'
            tex+=r'\geoSolution{'+val+'}' if blank else val
        res=rf'\node[anchor=west,font=\scriptsize,text=otGreenDark]at({k*w+.15:.2f},{y+.3:.2f}){{{k*valeur} {unite}}};'
        tex+=r'\geoSolution{'+res+'}' if blank else res.replace('otGreenDark','otInk')
    hauteur=len(parts)*.85-.25
    xmax=max(parts)*w+1.6;bas=.6-hauteur
    tex+=rf'\draw[otMuted,decorate,decoration={{brace,amplitude=4pt}}]({xmax:.2f},.6)--({xmax:.2f},{bas:.2f});\node[anchor=west,font=\small]at({xmax+.25:.2f},{(.6+bas)/2:.2f}){{total : {total} {unite}}};'
    dessin(nom,tex,'Chaque case représente une part ; toutes les parts sont égales.')

def nombres_modeles():
    for name,area,sol in [('carre-121',121,'11 cm'),('carre-18',18,r'$\sqrt{18}$ m'),('jardin-72',72,r'$\sqrt{72}$ m'),('carre-45',45,r'$\sqrt{45}$ cm'),('plaque-50',50,r'$\sqrt{50}$ cm')]:
        unit_='m' if name in ['carre-18','jardin-72'] else 'cm'
        carre(name,reponse(sol),f'Aire : {area} {unit_}$^2$',opening=name=='jardin-72')
    for name in ['cours-distributivite','aire-distrib']:
        rectangles(name,'$x+3$ cm','4 cm',r'\draw[otMuted,dashed](3,0)--(3,2.5);\node at(1.5,1.25){$4x$};\node at(4,1.25){12};\node[above]at(1.5,2.5){$x$};\node[above]at(4,2.5){3};')
    FIGURES['aire-distrib']['tex']=FIGURES['aire-distrib']['tex'].replace(r'\node at(1.5,1.25){$4x$};\node at(4,1.25){12};',r'\geoSolution{\node[text=otGreenDark]at(1.5,1.25){$4x$};\node[text=otGreenDark]at(4,1.25){12};}')
    rectangles('rectangle-litteral','$2x+1$ cm','$x+3$ cm')
    rectangles('eq-rectangle','$x+5$ cm','$x$ cm',answer='$7$ cm sur $12$ cm')
    dessin('eq-deux-figures',r'\draw[geoTrait](0,0)rectangle(2.6,2.6);\node[below]at(1.3,0){$x$};\draw[geoTrait](4,0)--(7.2,0)--(5.6,2.771)--cycle;\node[below]at(5.6,0){$x+2$};')
    dessin('cours-equilibre',r'\draw[geoTrait](0,1.6)--(6,1.6) (3,1.6)--(3,0) (2,0)--(4,0);\node[draw=otMuted,fill=otGreenTint,minimum width=2cm]at(1,2.1){$3x+5$};\node[draw=otMuted,fill=otGreenTint,minimum width=2cm]at(5,2.1){17};\node at(3,2.4){$=$};','Une même opération sur les deux membres conserve l’équilibre de l’égalité.')
    graph('proportion-prix',[('2.5*\\x',0,4)],(0,4),(0,10),1,2.5,xlabel='kg',ylabel='euros',caption='Prix proportionnel à la masse.')
    graph('cours-location',[('6+2*\\x',0,4)],(0,4),(0,14),1,2,xlabel='$t$ (h)',ylabel='$P(t)$ (€)',points=[('',0,6),('',1,8),('',2,10),('',3,12)])
    graph('graph-non-proportion',[('2+2*\\x',0,4)],(0,4),(0,10),1,2)
    graph('graph-corde',[('1.5*\\x',0,6)],(0,6),(0,9),1,1.5,blank=True,xlabel='m',ylabel='euros')
    graph('graph-carre',[('\\x*\\x',0,4)],(0,4),(0,16),1,4,xlabel='$c$ (cm)',ylabel='$A(c)$ (cm$^2$)')
    graph('four',[],(0,12),(0,120),2,20,xlabel='min',ylabel=r'$T$ ($^\circ$C)',poly=r'\draw[geoTrait](0,20)--(4,100)--(6,100)--(12,40);',caption='Les segments du modèle relient les températures indiquées.')
    graph('graph-tarifs',[('4+2*\\x',0,4),('4*\\x',0,4)],(0,4),(0,16),1,4,xlabel='$t$ (h)',ylabel='euros',sol=r'\fill[otGreenDark](2,8)circle(2pt);',caption='A : tracé bleu ; B : tracé vert.')
    graph('graph-reserve',[('120-8*\\x',0,15)],(0,15),(0,120),3,20,xlabel='$t$ (min)',ylabel='$V(t)$ (L)')
    figure('tableur-prix',tableau(['Ligne','A : durée','B : prix'],[['2','0',r'\texttt{=5+3*A2}'],['3','2',r'\geoEnonce{à recopier}\geoSolution{11}'],['4','4',r'\geoEnonce{à recopier}\geoSolution{17}']]),'Recopier la formule de B2 vers B3 et B4.')
    lignes=[]
    for a in range(7):
        b,cc=5*a-7,2*a+5
        row=[str(a+2),str(a),f'${b}$',f'${cc}$']
        if a==4:row=[r'\geoSolution{\color{otGreenDark}}'+v for v in row]
        lignes.append(row)
    figure('tableur-equation',tableau(['Ligne','A : $x$',r'B : \texttt{=5*A2-7}',r'C : \texttt{=2*A2+5}'],lignes),'Valeurs affichées par le tableur ; au corrigé, la ligne où B et C sont égales est en vert.')
    rectangles('coins-retires','18 cm','10 cm',r'\foreach\x in{0,4}{\foreach\y in{0,1.5}{\filldraw[draw=otNavy,fill=otGreen!25](\x,\y)rectangle++(1,1);}}\node at(2.5,1.25){aire restante};\node[above]at(.5,2.5){$x$};')
    t=r'\draw[geoTrait](0,0)circle(1.6);\draw[geoTrait](0,0)--(1.6,0)node[midway,below]{6 cm};\draw[otGreenDark,line width=2pt](1.6,0)arc(0:75:1.6);\draw[otMuted](0,0)--(75:1.6);\draw[otMuted](.55,0)arc(0:75:.55)node[midway,right]{$75^\circ$};'
    dessin('arc-75',t)
    # Fraction d’une fraction : carré unité partagé en 5 colonnes et 3 lignes.
    t=''
    for i in range(5):
        for j in range(3):
            fill='otGreen!55' if (i<4 and j<2) else ('otGreen!18' if i<4 else 'white')
            t+=rf'\filldraw[draw=otNavy!60,fill={fill}]({i*.6:.2f},{j*1.0:.2f})rectangle++(.6,1);'
    t+=r'\draw[geoTrait](0,0)rectangle(3,3);\draw[otMuted,decorate,decoration={brace,amplitude=4pt,mirror}](0,-.08)--(2.4,-.08)node[midway,below=3pt,font=\scriptsize]{$\frac45$ du carré};'
    t+=r'\draw[otMuted,decorate,decoration={brace,amplitude=4pt}](-.08,0)--(-.08,2)node[midway,left=3pt,font=\scriptsize]{$\frac23$};\node[anchor=west,font=\scriptsize,align=left]at(3.2,1.5){8 cases foncées\\sur 15 : $\frac8{15}$};'
    dessin('cours-fraction-fraction',t,'Les quatre colonnes colorées forment les $\\frac45$ du carré unité ; les cases foncées en sont les $\\frac23$.')
    t=r'\draw[geoTrait](0,0)rectangle(3.6,2.7);'
    for i in range(1,4):t+=rf'\draw[otNavy!50]({i*.9},0)--({i*.9},2.7);'
    for j in range(1,3):t+=rf'\draw[otNavy!50](0,{j*.9})--(3.6,{j*.9});'
    sol=r'\fill[otGreen!20](0,0)rectangle(2.7,2.7);\fill[otGreen!60](0,0)rectangle(2.7,1.8);'
    for i in range(1,4):sol+=rf'\draw[otNavy!50]({i*.9},0)--({i*.9},2.7);'
    for j in range(1,3):sol+=rf'\draw[otNavy!50](0,{j*.9})--(3.6,{j*.9});'
    sol+=r'\draw[geoTrait](0,0)rectangle(3.6,2.7);\node[anchor=west,font=\scriptsize,text=otGreenDark,align=left]at(3.8,1.35){6 cases foncées\\sur 12 : $\frac12$};'
    dessin('fraction-rectangle',r'\geoEnonce{'+t+r'}\geoSolution{'+sol+'}','Rectangle de 4 colonnes et 3 lignes ; au corrigé, les trois colonnes colorées en forment les $\\frac34$, les cases foncées les $\\frac23$ de cette partie.')
    barres_ratio('cours-ratio',[3,5],7,56,'',['A','B'],False)
    barres_ratio('ratio-72',[4,5],8,72,'€',['Ana','Ben'],True)

def barres(nom,cats,series,ymax,ystep,ylabel,legende,ligne=None,dec=False,sol_etiquettes=None):
    """Diagramme en barres groupées ; une série « cachée » n’apparaît qu’au corrigé."""
    sy=3.4/ymax;tex=''
    n=int(round(ymax/ystep))
    for k in range(n+1):
        v=k*ystep;y=v*sy
        lab=f'{v:.1f}'.replace('.','{,}') if dec else f'{v:g}'
        tex+=rf'\draw[otRule!65,line width=.2pt](0,{y:.3f})--({len(cats)*1.7+.3:.2f},{y:.3f});\node[left,font=\tiny]at(0,{y:.3f}){{${lab}$}};'
    tex+=rf'\draw[otMuted,->](0,0)--(0,{3.4+.4:.2f})node[above,font=\scriptsize]{{{ylabel}}};\draw[otMuted](0,0)--({len(cats)*1.7+.3:.2f},0);'
    ns=len(series);w=.42
    for i,cat in enumerate(cats):
        x0=1+i*1.7
        tex+=rf'\node[below,font=\scriptsize]at({x0:.2f},0){{{cat}}};'
        for j,(vals,color,_,cache,etiquettes) in enumerate(series):
            x=x0+(j-(ns-1)/2)*(w+.05)
            bar=rf'\fill[{color}]({x-w/2:.3f},0)rectangle({x+w/2:.3f},{vals[i]*sy:.3f});'
            if etiquettes:bar+=rf'\node[above,font=\tiny,text={"otGreenDark" if cache else "otInk"}]at({x:.3f},{vals[i]*sy:.3f}){{{etiquettes[i]}}};'
            tex+=r'\geoSolution{'+bar+'}' if cache else bar
            if j==0 and sol_etiquettes:
                tex+=r'\geoSolution{'+rf'\node[above,font=\scriptsize,text=otGreenDark]at({x:.3f},{vals[i]*sy+.3:.3f}){{{sol_etiquettes[i]}}};'+'}'
    if ligne:
        v,txt=ligne
        tex+=rf'\draw[otOrange,dashed,line width=.8pt](0,{v*sy:.3f})--({len(cats)*1.7+.3:.2f},{v*sy:.3f})node[right,font=\scriptsize,text=otInk]{{{txt}}};'
    leg=''
    for j,(_,color,nomserie,cache,_) in enumerate(series):
        item=rf'\fill[{color}]({len(cats)*1.7+.6:.2f},{3.2-j*.45:.2f})rectangle++(.3,.25);\node[anchor=west,font=\scriptsize]at({len(cats)*1.7+.95:.2f},{3.32-j*.45:.2f}){{{nomserie}}};'
        leg+=r'\geoSolution{'+item+'}' if cache else item
    dessin(nom,tex+leg,legende)

def statistiques_hasard():
    poly=''.join(rf'\draw[otNavy,line width=2pt]({i},0)--({i},{v});\node[above,font=\scriptsize]at({i},{v}){{{v}}};' for i,v in enumerate([2,4,3,2,1]))
    graph('stat-livres',[],(-.5,4.5),(0,5),1,1,xlabel='livres',ylabel='élèves',poly=poly)
    secteurs('stat-fratrie',[90,144,72,36,18],['0','1','2','3','5'],'Nombre de frères et sœurs de 40 élèves ; chaque secteur porte la valeur correspondante.',
             extra=r'\node[anchor=west,font=\scriptsize,align=left]at(2.4,0){Angles des secteurs :\\0 : $90^\circ$ ; 1 : $144^\circ$ ;\\2 : $72^\circ$ ; 3 : $36^\circ$ ; 5 : $18^\circ$};')
    urs('urne-431',['R']*4+['B']*3+['V']);urs('jetons-numerotes',['R1','R2','R3','B1','B2','V1'])
    # Arbre de deux pièces (cours et exercice).
    def arbre(nom,vide):
        t=r'\coordinate(R)at(0,0);'
        t+=r'\node[font=\scriptsize,text=otMuted]at(1.6,1.75){1re pièce};\node[font=\scriptsize,text=otMuted]at(3.6,1.75){2e pièce};\node[font=\scriptsize,text=otMuted]at(5.4,1.75){issue};'
        for i,a in enumerate('PF'):
            y1=.8-1.6*i
            t+=rf'\draw[otNavy!65,line width=.6pt](0,0)--(1.5,{y1});'
            t+=(rf'\node[fill=white,font=\small]at(1.6,{y1}){{${a}$}};' if not vide else rf'\node[fill=white,font=\small]at(1.6,{y1}){{\geoEnonce{{?}}\geoSolution{{\textcolor{{otGreenDark}}{{${a}$}}}}}};')
            for j,b in enumerate('PF'):
                y2=y1+.4-.8*j
                t+=rf'\draw[otNavy!65,line width=.6pt](1.8,{y1})--(3.4,{y2});'
                t+=(rf'\node[fill=white,font=\small]at(3.6,{y2}){{${b}$}};' if not vide else rf'\node[fill=white,font=\small]at(3.6,{y2}){{\geoEnonce{{?}}\geoSolution{{\textcolor{{otGreenDark}}{{${b}$}}}}}};')
                lab=rf'$({a}\,;{b})$'
                t+=(rf'\node[anchor=west,font=\scriptsize]at(4.9,{y2}){{{lab}}};' if not vide else rf'\geoSolution{{\node[anchor=west,font=\scriptsize,text=otGreenDark]at(4.9,{y2}){{{lab}}};}}')
        dessin(nom,t,'Arbre des issues : chaque chemin de la racine à une feuille est une issue.')
    arbre('cours-arbre-pieces',False);arbre('arbre-deux-pieces',True)
    # Tableau pièce puis dé.
    t='';w=1.0;h=.55
    t+=r'\node[font=\scriptsize]at(-.5,.85){};'
    for j in range(6):t+=rf'\node[font=\small]at({(j+.5)*w:.2f},{2*h+.3:.2f}){{{j+1}}};'
    for i,a in enumerate('PF'):
        y=(1-i)*h
        t+=rf'\node[font=\small]at(-.35,{y+h/2:.3f}){{{a}}};'
        for j in range(6):
            fav=(a=='P' and (j+1)%2==0)
            t+=rf'\draw[otNavy!60]({j*w:.2f},{y:.3f})rectangle++({w},{h});'
            sol=(rf'\fill[otGreen!35]({j*w+.02:.2f},{y+.02:.3f})rectangle++({w-.04},{h-.04});' if fav else '')+rf'\node[font=\scriptsize,text=otGreenDark]at({(j+.5)*w:.2f},{y+h/2:.3f}){{$({a}\,;{j+1})$}};'
            t+=r'\geoSolution{'+sol+'}'
    t+=r'\node[font=\scriptsize,text=otMuted]at(3,1.75){dé};\node[font=\scriptsize,text=otMuted,rotate=90]at(-.8,.55){pièce};'
    dessin('tableau-piece-de',t,'Tableau à double entrée ; au corrigé, les issues « pile et pair » sont surlignées.')
    # Tableau des sommes de deux dés.
    t='';w=.72;h=.42
    for j in range(6):t+=rf'\node[font=\small,text=otNavy]at({(j+.5)*w:.3f},{6*h+.25:.3f}){{{j+1}}};'
    for i in range(6):
        y=(5-i)*h
        t+=rf'\node[font=\small,text=otOrange!80!black]at(-.3,{y+h/2:.3f}){{{i+1}}};'
        for j in range(6):
            s=i+j+2
            t+=rf'\draw[otNavy!60]({j*w:.3f},{y:.3f})rectangle++({w},{h});'
            fill='otGreen!40' if s==7 else ('otOrange!30' if s>=10 else '')
            sol=(rf'\fill[{fill}]({j*w+.02:.3f},{y+.02:.3f})rectangle++({w-.04:.2f},{h-.04:.2f});' if fill else '')+rf'\node[font=\scriptsize]at({(j+.5)*w:.3f},{y+h/2:.3f}){{{s}}};'
            if i==0 and j==0:t+=sol
            else:t+=r'\geoSolution{'+sol+'}'
    t+=r'\node[font=\scriptsize,text=otNavy]at(2.16,3.15){dé bleu};\node[font=\scriptsize,text=otOrange!80!black,rotate=90]at(-.75,1.26){dé rouge};'
    t+=r'\geoSolution{\node[anchor=west,font=\scriptsize,align=left]at(4.6,1.6){\textcolor{otGreenDark}{vert : somme 7}\\\textcolor{otOrange!80!black}{orange : au moins 10}};}'
    dessin('somme-deux-des',t,'Tableau des 36 issues ; une case donne la somme des deux dés. La première case est remplie.')
    # Diagramme de Venn des événements A et B.
    t=r'\draw[otMuted,rounded corners=2mm](-2.6,-1.5)rectangle(2.9,1.6);\node[anchor=north west,font=\scriptsize,text=otMuted]at(-2.6,1.6){univers};'
    t+=r'\draw[otNavy,line width=.8pt,fill=otNavy!8](-.55,0)circle(1.15);\draw[otGreenDark,line width=.8pt](.75,0)circle(1.15);\node[font=\small,text=otNavy]at(-1.65,1.05){$A$};\node[font=\small,text=otGreenDark]at(1.85,1.05){$B$};'
    t+=r'\geoSolution{\node[font=\small]at(-1.15,0){2};\node[font=\small]at(.1,.35){4};\node[font=\small]at(.1,-.35){6};\node[font=\small]at(1.35,0){5};\node[font=\small]at(-2.2,-1.15){1};\node[font=\small]at(2.5,-1.15){3};}'
    dessin('venn-de',t,'Au corrigé, chaque issue du dé est placée dans la bonne région.')
    barres('fluctuation-pieces',['groupe 1','groupe 2','groupe 3','groupe 4'],
           [([23,28,25,31],'otNavy!60','piles sur 50 lancers',False,['23','28','25','31'])],
           50,10,'piles','Nombre de piles obtenus par chaque groupe ; au corrigé, les fréquences sont indiquées en vert.',ligne=(25,'25 : moitié'),
           sol_etiquettes=['$0{,}46$','$0{,}56$','$0{,}50$','$0{,}62$'])
    barres('distribution-deux-pieces',['0 pile','1 pile','2 piles'],
           [([13/60,32/60,15/60],'otNavy!60','fréquence observée',True,['$0{,}22$','$0{,}53$','$0{,}25$']),
            ([.25,.5,.25],'otGreen!70','probabilité',True,[r'$\frac14$',r'$\frac12$',r'$\frac14$'])],
           .6,.1,'fréquence','Diagramme à compléter : fréquences observées et probabilités du modèle, côte à côte.',dec=True)

# ---------------------------------------------------------------------
# Chapitre 12 : droites remarquables et raisonnement
# ---------------------------------------------------------------------
def raisonnement():
    # Cours : quatre vignettes.
    t='';base={'B':(0,0),'C':(2.4,0),'A':(.75,1.75)}
    titres=['médiatrice de $[BC]$','hauteur issue de A','médiane issue de A','bissectrice de $\\widehat{A}$']
    for k,titre in enumerate(titres):
        P=echelle(base,1,3.55*k,0);A,B,C=P['A'],P['B'],P['C'];I=mil(B,C)
        t+=seg(P,'A-B-C-A')+points(P,'ABC',{'A':'above','B':'below left','C':'below right'})
        if k==0:t+=droite((I[0],-.2),(I[0],2.0),0,0,'otGreenDark,line width=.9pt')+coche(B,I)+coche(I,C)+droit(B,I,(I[0],1))
        if k==1:
            H=(A[0],0);t+=rf'\draw[otGreenDark,line width=.9pt]{c(A)}--{c(H)};'+droit(A,H,C)
        if k==2:t+=rf'\draw[otGreenDark,line width=.9pt]{c(A)}--{c(I)};'+coche(B,I)+coche(I,C)
        if k==3:
            u=unit(vec(A,B));v=unit(vec(A,C));d=(u[0]+v[0],u[1]+v[1])
            s=-A[1]/d[1];D=add(A,d,s)
            t+=rf'\draw[otGreenDark,line width=.9pt]{c(A)}--{c(D)};'+arc_angle(A,B,D,.42)+arc_angle(A,D,C,.52)
        t+=rf'\node[font=\scriptsize,text=otInk]at({1.2+3.55*k:.2f},-.55){{{titre}}};'
    dessin('cours-droites-remarquables',t,'Les codages indiquent les angles droits, les milieux et les angles de même mesure.')
    # Exercice 1 : reconnaître trois droites.
    P0={'A':(2,4),'B':(0,0),'C':(7,0)};k=.62;P=echelle(P0,k)
    A,B,C=P['A'],P['B'],P['C'];I=mil(B,C);J=mil(A,C)
    u=unit(vec(A,B));H=add(A,u,((C[0]-A[0])*u[0]+(C[1]-A[1])*u[1]))
    P.update(I=I,J=J,H=H)
    t=seg(P,'A-B-C-A')+droite((I[0],-.3),(I[0],2.75),0,0)+coche(B,I)+coche(I,C)+droit(B,I,(I[0],1))
    t+=droite(C,H,.08,.35)+droit(C,H,A)+droite(B,J,0,.45)+coche(A,J,2)+coche(J,C,2)
    t+=points(P,'ABCIJH',{'A':'above','B':'below left','C':'below right','I':'below right','J':'above right','H':'left'})
    t+=rf'\node[font=\scriptsize]at({I[0]+.32:.2f},2.75){{$(d_1)$}};\node[font=\scriptsize]at{c(add(H,vec(C,H),.45))}{{$(d_2)$}};\node[font=\scriptsize,anchor=west]at{c(add(J,vec(B,J),.5))}{{$(d_3)$}};'
    registre('rem-01',P,milieux=[('I','B','C'),('J','A','C')],perpendiculaires=[(('I',(I[0],1)),('B','C')),(('C','H'),('A','B'))],alignes=[('A','H','B')])
    dessin('rem-01',t)
    # Exercice 2 : rectangle, puis trapèze isocèle au corrigé.
    P=echelle({'A':(0,0),'B':(5,0),'C':(5,3),'D':(0,3)},.75)
    t=seg(P,'A-B-C-D-A')+seg(P,'A-C','otNavy,line width=.6pt')+seg(P,'B-D','otNavy,line width=.6pt')+points(P,'ABCD',{'A':'below left','B':'below right','C':'above right','D':'above left'})
    for (a,b,cc) in [('D','A','B'),('A','B','C'),('B','C','D'),('C','D','A')]:t+=droit(P[a],P[b],P[cc])
    Q=echelle({'E':(0,0),'F':(6,0),'G':(4.5,3),'H':(1.5,3)},.7,5.4,0)
    sol=seg(Q,'E-F-G-H-E','otGreenDark,line width=.85pt')+seg(Q,'E-G','otGreenDark,dashed')+seg(Q,'F-H','otGreenDark,dashed')+points(Q,'EFGH',{'E':'below left','F':'below right','G':'above right','H':'above left'},'otGreenDark')
    sol+=rf'\node[font=\scriptsize,text=otGreenDark]at({Q["E"][0]+2.1:.2f},-.45){{$EG=FH$, sans angle droit}};'
    registre('rem-02',dict(**P,**Q),egalites=[(('E','G'),('F','H')),(('A','C'),('B','D'))])
    dessin('rem-02',t+r'\geoSolution{'+sol+'}','Au corrigé, un trapèze isocèle sert de contre-exemple.')
    triangle('rem-03',8,5,5,labels={},extra=r'\draw[geoDonnee](3.2,2.4)--(3.2,0);\node[right]at(3.2,1.2){3 cm};\node[below]at(3.2,0){$H$};\draw[otMuted](3.05,0)--(3.05,.15)--(3.2,.15);\draw[otMuted,|<->|](0,-.65)--node[fill=white,font=\scriptsize]{8 cm}(6.4,-.65);')
    # Exercice 4 : médiatrice et deux points.
    P={'A':(0,0),'B':(4,0)};I=(2,0);M=(2,1.6);N=(2,-1.35);P.update(I=I,M=M)
    t=seg(P,'A-B')+droite((2,-1.8),(2,2.2),0,0)+coche(P['A'],I)+coche(I,P['B'])+droit(P['A'],I,(2,1))
    t+=seg(dict(A=P['A'],M=M),'A-M','otNavy,dashed')+texte_seg(P['A'],M,'4,5 cm',.3,1)+seg(dict(B=P['B'],M=M),'B-M','otNavy,dashed')+texte_seg(M,P['B'],reponse('4,5 cm'),.3,1)
    t+=points(P,'ABM',{'A':'below left','B':'below right','M':'above right'})+r'\node[font=\scriptsize]at(2.35,2.15){$(d)$};'
    t+=r'\geoSolution{'+rf'\fill[otGreenDark]{c(N)}circle(1.4pt)node[right,font=\small]{{$N$}};\draw[otGreenDark,dashed]{c(P["A"])}--{c(N)}--{c(P["B"])};'+'}'
    registre('rem-04',dict(P,N=N),milieux=[('I','A','B')],egalites=[(('M','A'),('M','B')),(('N','A'),('N','B'))])
    dessin('rem-04',t,'$(d)$ est la médiatrice de $[AB]$ ; au corrigé, N est placé sur cette droite.')
    triangle('rem-05',5,5,angle=74,labels={(0,1):r'\geoSolution{\textcolor{otGreenDark}{base}}',(0,2):'5 cm'},extra=r'\node at(.65,.45){$74^\circ$};\geoSolution{\node[text=otGreenDark,font=\scriptsize]at(2.6,.24){$53^\circ$};\node[text=otGreenDark,font=\scriptsize]at(1.02,2.5){$53^\circ$};}')
    # Exercice 6 : contre-exemple de deux triangles de même aire.
    T1={'A':(0,0),'B':(4*.55,0),'C':(0,3*.55)};T2={'D':(3.2,0),'E':(3.2+6*.55,0),'F':(3.2+2*.55,2*.55)}
    sol=seg(T1,'A-B-C-A','otGreenDark,line width=.85pt')+droit(T1['B'],T1['A'],T1['C'],'otGreenDark')+texte_seg(T1['A'],T1['B'],'4 cm',.25,-1)+texte_seg(T1['C'],T1['A'],'3 cm',.3,1)
    sol+=seg(T2,'D-E-F-D','otGreenDark,line width=.85pt')+rf'\draw[otGreenDark,dashed]{c(T2["F"])}--({T2["F"][0]:.3f},0);'+texte_seg(T2['D'],T2['E'],'6 cm',.25,-1)+rf'\node[font=\scriptsize,anchor=west]at({T2["F"][0]+.05:.3f},.5){{2 cm}};'
    sol+=r'\node[font=\scriptsize,text=otGreenDark]at(3.5,-.85){deux aires de 6 cm$^2$, côtés différents};'
    dessin('rem-06',r'\geoEnonce{\node[draw=otMuted,rounded corners=1mm,inner sep=4mm,font=\small]{Chercher deux triangles de même aire.};}\geoSolution{'+sol+'}','Le contre-exemple est construit au corrigé.')
    registre('rem-06',dict(T1,**T2),aires=[(('A','B','C'),('D','E','F'))])
    # Exercice 7 : médiane et aires.
    P=echelle({'B':(0,0),'C':(6,0),'A':(.9,3)},.85);B,C,A=P['B'],P['C'],P['A'];I=mil(B,C);H=(A[0],0);P.update(I=I,H=H)
    t=seg(P,'A-B-C-A')+seg(P,'A-I','otNavy,line width=.7pt')+seg(P,'A-H','geoDonnee')+droit(A,H,C)+coche(B,I)+coche(I,C)
    t+=r'\geoSolution{'+rf'\fill[otGreen!25]{c(A)}--{c(B)}--{c(I)}--cycle;\fill[otNavy!12]{c(A)}--{c(I)}--{c(C)}--cycle;\node[font=\scriptsize,text=otGreenDark]at{c(((A[0]+B[0]+I[0])/3+.15,(A[1]+B[1]+I[1])/3))}{{15}};\node[font=\scriptsize,text=otGreenDark]at{c(((A[0]+I[0]+C[0])/3,(A[1]+I[1]+C[1])/3))}{{15}};'+'}'
    t+=seg(P,'A-B-C-A')+points(P,'ABCIH',{'A':'above','B':'below left','C':'below right','I':'below','H':'below'})
    registre('rem-07',P,milieux=[('I','B','C')],perpendiculaires=[(('A','H'),('B','C'))])
    dessin('rem-07',t,'Aires en cm$^2$ au corrigé.')
    # Exercice 8 : contraposée.
    P={'A':(0,0),'B':(2,0),'P':(.3125,2.48)};I=(1,0)
    t=seg(P,'A-B')+droite((1,-.6),(1,2.8),0,0)+coche(P['A'],I)+coche(I,P['B'])+droit(P['A'],I,(1,1))+seg(P,'P-A','otNavy,dashed')+seg(P,'P-B','otNavy,dashed')
    t+=texte_seg(P['A'],P['P'],'5 cm',.32,1)+texte_seg(P['P'],P['B'],'6 cm',.3,1)+points(P,'ABP',{'A':'below left','B':'below right','P':'above left'})+r'\node[font=\scriptsize]at(1.4,2.75){$(d)$};'
    dessin('rem-08',t,'$(d)$ est la médiatrice de $[AB]$ ; les longueurs écrites sont des données.')
    # Exercice 9 : losange, puis cerf-volant au corrigé.
    P={'A':(0,1.4),'B':(2.2,0),'C':(4.4,1.4),'D':(2.2,2.8)};O=(2.2,1.4)
    t=seg(P,'A-B-C-D-A')+seg(P,'A-C','otNavy,line width=.6pt')+seg(P,'B-D','otNavy,line width=.6pt')+droit(P['A'],O,P['D'])+coche(P['A'],P['B'])+coche(P['B'],P['C'])+coche(P['C'],P['D'])+coche(P['D'],P['A'])
    t+=points(P,'ABCD',{'A':'left','B':'below','C':'right','D':'above'})
    Q=echelle({'E':(0,0),'F':(2,-2),'G':(7,0),'H':(2,2)},.55,5.6,1.4);Oq=(Q['F'][0],1.4)
    sol=seg(Q,'E-F-G-H-E','otGreenDark,line width=.85pt')+seg(Q,'E-G','otGreenDark,dashed')+seg(Q,'F-H','otGreenDark,dashed')+droit(Q['E'],Oq,Q['H'],'otGreenDark')+points(Q,'EFGH',{'E':'left','F':'below','G':'right','H':'above'},'otGreenDark')
    sol+=r'\node[font=\scriptsize,text=otGreenDark]at(7.7,-.2){diagonales perpendiculaires, pas un losange};'
    registre('rem-09',dict(**P,**Q),perpendiculaires=[(('A','C'),('B','D')),(('E','G'),('F','H'))])
    dessin('rem-09',t+r'\geoSolution{'+sol+'}','Le losange ABCD est codé ; le contre-exemple EFGH est ajouté au corrigé.')
    # Exercice 10 : triangle isocèle.
    P=echelle({'A':(3,4),'B':(0,0),'C':(6,0)},.6);I=mil(P['B'],P['C']);P['I']=I
    t=seg(P,'A-B-C-A')+coche(P['A'],P['B'],2)+coche(P['A'],P['C'],2)+coche(P['B'],I)+coche(I,P['C'])+points(P,'ABCI',{'A':'above','B':'below left','C':'below right','I':'below'})
    t+=r'\geoSolution{'+rf'\draw[otGreenDark,line width=.9pt]{c(P["A"])}--{c(I)};'+droit(P['A'],I,P['C'],'otGreenDark')+'}'
    registre('rem-10',P,milieux=[('I','B','C')],egalites=[(('A','B'),('A','C'))],perpendiculaires=[(('A','I'),('B','C'))])
    dessin('rem-10',t)
    # Exercice 11 : hauteurs concourantes.
    P=echelle({'A':(0,0),'B':(7,0),'C':(3,5)},.6);A,B,C=P['A'],P['B'],P['C']
    def pied(M,U,V):
        u=unit(vec(U,V));s=(M[0]-U[0])*u[0]+(M[1]-U[1])*u[1];return add(U,u,s)
    HA=pied(A,B,C);HB=pied(B,A,C);H=(C[0],2.4*.6);K=(C[0],0);P.update(H=H)
    t=seg(P,'A-B-C-A')+rf'\draw[geoDonnee]{c(A)}--{c(HA)};\draw[geoDonnee]{c(B)}--{c(HB)};'+droit(A,HA,C)+droit(B,HB,C)+points(P,'ABCH',{'A':'below left','B':'below right','C':'above','H':'left'})
    t+=r'\geoSolution{'+rf'\draw[otGreenDark,line width=.9pt]{c(C)}--{c(K)};'+droit(C,K,B,'otGreenDark')+'}'
    registre('rem-11',dict(P,HA=HA,HB=HB,K=K),perpendiculaires=[(('A','HA'),('B','C')),(('B','HB'),('A','C')),(('C','K'),('A','B'))],alignes=[('A','H','HA'),('B','H','HB'),('C','H','K')])
    dessin('rem-11',t,'Les deux hauteurs tracées se coupent en H ; la troisième est ajoutée au corrigé.')
    # Exercice 12 : deux angles droits impossibles.
    t=r'\draw[geoTrait](0,0)--(4,0);\draw[geoDonnee](0,0)--(0,2.4);\draw[geoDonnee](4,0)--(4,2.4);\draw[otMuted](0,.17)--(.17,.17)--(.17,0);\draw[otMuted](4,.17)--(3.83,.17)--(3.83,0);'
    t+=r'\fill[otNavy](0,0)circle(1.3pt)node[below left]{$B$};\fill[otNavy](4,0)circle(1.3pt)node[below right]{$C$};\node[font=\small]at(2,2.2){$A$ ?};'
    t+=r'\geoSolution{\node[font=\scriptsize,text=otGreenDark,align=center]at(2,1.1){deux perpendiculaires à $(BC)$\\sont parallèles : pas de point A};}'
    dessin('rem-12',t,'Si les angles en B et en C étaient droits, les côtés issus de B et de C ne se rencontreraient pas.')
    # Exercice 13 : le puits.
    k=.8;P=echelle({'A':(0,0),'B':(6,0),'C':(2,4)},k);O=(3*k,1*k);P['O']=O
    t=''
    for n in 'ABC':
        x,y=P[n];t+=rf'\filldraw[draw=otNavy,fill=otOrange!25]({x-.22:.3f},{y:.3f})rectangle({x+.22:.3f},{y+.3:.3f});\filldraw[draw=otNavy,fill=otOrange!55]({x-.3:.3f},{y+.3:.3f})--({x:.3f},{y+.55:.3f})--({x+.3:.3f},{y+.3:.3f})--cycle;'
    t+=points(P,'ABC',{'A':'below','B':'below','C':'below'})
    sol=droite((O[0],-.5),(O[0],2.6),0,0,'otGreenDark,dashed')
    mb=mil(P['B'],P['C']);v=vec(P['B'],P['C']);nv=(-v[1],v[0])
    sol+=droite(add(mb,nv,-.55),add(mb,nv,.55),0,0,'otGreenDark,dashed')+rf'\draw[otGreenDark]{c(O)}circle({hypot(*vec(O,P["A"])):.3f});\fill[otGreenDark]{c(O)}circle(1.5pt)node[below right,font=\small]{{$O$}};'
    registre('rem-13',P,cercles=[('O',['A','B','C'])])
    dessin('rem-13',t+r'\geoSolution{'+sol+'}','Au corrigé : deux médiatrices et le cercle de centre O passant par les trois maisons.')
    # Exercice 14 : vrai ou faux.
    t=r'\draw[geoTrait](0,0)--(4.4,0)node[right,font=\scriptsize]{$(\Delta)$};\draw[geoDonnee](1,-.4)--(1,2.2)node[above,font=\scriptsize]{$(d_1)$};\draw[geoDonnee](3.2,-.4)--(3.2,2.2)node[above,font=\scriptsize]{$(d_2)$};\draw[otMuted](1,.17)--(1.17,.17)--(1.17,0);\draw[otMuted](3.2,.17)--(3.37,.17)--(3.37,0);\node[font=\scriptsize]at(2.1,-.55){énoncé a};'
    tri,_,_=triangle_tex(5,5,angle=74,names='EFG',shift=6.2,scale_override=.45)
    sol=tri.replace('otNavy','otGreenDark')+r'\node[font=\scriptsize,text=otGreenDark]at(6.55,.25){$74^\circ$};\node[font=\scriptsize,text=otGreenDark]at(8.1,.25){$53^\circ$};\node[font=\scriptsize,text=otGreenDark]at(7.3,-.55){contre-exemple pour b};'
    dessin('rem-14',t+r'\geoSolution{'+sol+'}','Au corrigé, un triangle isocèle non équilatéral réfute l’énoncé b.')
    # Exercice 15 : médiane dans une médiane.
    P=echelle({'B':(0,0),'C':(6,0),'A':(2,4)},.75);I=mil(P['B'],P['C']);J=mil(P['A'],I);P.update(I=I,J=J)
    t=r'\geoSolution{'+rf'\fill[otGreen!35]{c(P["A"])}--{c(P["B"])}--{c(J)}--cycle;\node[font=\scriptsize,text=otGreenDark]at{c(((P["A"][0]+P["B"][0]+J[0])/3,(P["A"][1]+P["B"][1]+J[1])/3))}{{9}};'+'}'
    t+=seg(P,'A-B-C-A')+seg(P,'A-I','otNavy,line width=.7pt')+seg(P,'B-J','otNavy,line width=.7pt')+coche(P['B'],I)+coche(I,P['C'])+coche(P['A'],J,2)+coche(J,I,2)+points(P,'ABCIJ',{'A':'above','B':'below left','C':'below right','I':'below','J':'right'})
    registre('rem-15',P,milieux=[('I','B','C'),('J','A','I')])
    dessin('rem-15',t,'Aire de ABJ en cm$^2$ au corrigé.')

# ---------------------------------------------------------------------
# Chapitre 13 : translations et parallélogrammes
# ---------------------------------------------------------------------
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

def drapeau(mat,pts,color='otNavy',fill='otGreen!45'):
    (a,b),(p,q,r)=mat,pts
    return rf'\draw[{color},line width=1pt]{c(a)}--{c(b)};\filldraw[draw={color},fill={fill}]{c(p)}--{c(q)}--{c(r)}--cycle;'

def translations():
    trans_grid('trans-01',[(1,2)],(3,1),'A',[(0,0),(3,1)])
    trans_grid('cours-translation',[(1,1),(3,1),(2,3)],(3,2),known=[(0,0),(3,2)])
    FIGURES['cours-translation']['tex']=r'\otGeoCorrigetrue'+FIGURES['cours-translation']['tex']
    trans_grid('trans-02',[(1,1),(3,1),(2,3)],(3,2))
    trans_grid('trans-03',[(2,3)],(-4,-1),'B')
    triangle('trans-04',5,18/(5*sin(radians(42))),angle=42,labels={(0,1):'5 cm'},extra=r'\node[anchor=west,font=\scriptsize]at(5,2.4){$42^\circ$ ; aire 9 cm$^2$};')
    # Exercice 5 : trois transformations d’un drapeau.
    F=[(4.8,0),(4.8,2),(6.0,1.6),(4.8,1.2)]
    sym=lambda p:(7.8-p[0],p[1]);dem=lambda p:(13-p[0],2-p[1]);tra=lambda p:(p[0]-5.2,p[1]-.4)
    def dr(f,img=lambda p:p,color='otNavy',fill='otGreen!45'):
        q=[img(p) for p in f];return drapeau((q[0],q[1]),(q[1],q[2],q[3]),color,fill)
    t=dr(F)+dr(F,tra,fill='otNavy!20')+dr(F,sym,fill='otNavy!20')+dr(F,dem,fill='otNavy!20')
    t+=r'\node[font=\small]at(5.1,-.45){F};\node[font=\small]at(-.1,-.85){1};\node[font=\small]at(2.7,-.45){2};\node[font=\small]at(7.9,-.45){3};'
    t+=r'\geoSolution{\draw[otGreenDark,dashed,line width=.8pt](3.9,-.6)--(3.9,2.5);\fill[otGreenDark](6.5,1)circle(1.8pt)node[above,font=\scriptsize]{centre};\draw[otGreenDark,->,line width=.8pt](4.8,-.15)--(-.4,-.55);}'
    GEOMETRIE['trans-05']={'transformations':{'F':F,'translation':[tra(p) for p in F],'symetrie':[sym(p) for p in F],'demi-tour':[dem(p) for p in F],'axe_x':3.9,'centre':(6.5,1),'deplacement':(-5.2,-.4)}}
    dessin('trans-05',t,'Le drapeau F et trois images ; au corrigé, l’axe, le centre et le glissement sont tracés en vert.')
    dessin('trans-06',r'\draw[geoTrait](0,0)--(3,0)--(5,2)--(2,2)--cycle;\node[below left]at(0,0){A};\node[below right]at(3,0){B};\node[above right]at(5,2){B’};\node[above left]at(2,2){A’};\draw[geoVecteur](.4,.4)--(2.4,2.4);')
    # Exercice 7 : trois quadrilatères codés par leurs diagonales.
    t=''
    def quad(P,sh,titre,code):
        Q=echelle(P,1,sh,0);O=mil(Q['A'],Q['C']);Q['O']=O
        s=seg(Q,'A-B-C-D-A')+seg(Q,'A-C','otNavy,line width=.6pt')+seg(Q,'B-D','otNavy,line width=.6pt')
        if code=='para':s+=coche(Q['A'],O)+coche(O,Q['C'])+coche(Q['B'],O,2)+coche(O,Q['D'],2)
        if code=='los':s+=coche(Q['A'],O)+coche(O,Q['C'])+coche(Q['B'],O,2)+coche(O,Q['D'],2)+droit(Q['A'],O,Q['D'])
        if code=='rect':s+=coche(Q['A'],O)+coche(O,Q['C'])+coche(Q['B'],O)+coche(O,Q['D'])
        s+=points(Q,'ABCDO',{'A':'below left','B':'below right','C':'above right','D':'above left','O':'right'})
        s+=rf'\node[font=\scriptsize]at({sh+1.4:.2f},-.6){{{titre}}};'
        return s,Q
    s1,q1=quad({'A':(0,0),'B':(2.2,0),'C':(3,1.6),'D':(.8,1.6)},0,'Figure 1','para')
    s2,q2=quad({'A':(0,.9),'B':(1.4,0),'C':(2.8,.9),'D':(1.4,1.8)},4,'Figure 2','los')
    s3,q3=quad({'A':(0,0),'B':(2.8,0),'C':(2.8,1.6),'D':(0,1.6)},8,'Figure 3','rect')
    registre('trans-07',{**{k+'1':v for k,v in q1.items()},**{k+'2':v for k,v in q2.items()},**{k+'3':v for k,v in q3.items()}},milieux=[('O1','A1','C1'),('O1','B1','D1'),('O2','A2','C2'),('O2','B2','D2'),('O3','A3','C3'),('O3','B3','D3')],perpendiculaires=[(('A2','C2'),('B2','D2'))],egalites=[(('A3','C3'),('B3','D3'))])
    dessin('trans-07',s1+s2+s3,'Les codages des diagonales sont des données ; le dessin ne doit pas être mesuré.')
    tex=''
    for i in range(5):tex+=polygone([(i*1.8,0),(i*1.8+1.0,0),(i*1.8+.4,1)])
    dessin('trans-08',tex+r'\draw[|<->|](0,-.5)--node[below]{4 cm}(1.8,-.5);\geoSolution{\draw[otGreenDark,->,line width=.8pt](0,1.35)--node[above,font=\scriptsize]{16 cm}(7.2,1.35);}')
    # Exercice 9 : image de deux droites.
    O=(0,0);d=(1,0);e=(cos(radians(35)),sin(radians(35)));V=(5,.9);O2=add(O,V)
    t=rf'\draw[geoTrait]{c(add(O,d,-1))}--{c(add(O,d,2.6))}node[right,font=\scriptsize]{{$(d)$}};\draw[geoTrait]{c(add(O,e,-.8))}--{c(add(O,e,2.3))}node[above,font=\scriptsize]{{$(\Delta)$}};'
    t+=arc_angle(O,(1,0),e,.6,r'$35^\circ$',lr=.95)
    t+=rf'\draw[otNavy!70,line width=.8pt]{c(add(O2,d,-1))}--{c(add(O2,d,2.6))}node[right,font=\scriptsize]{{$(d^{{\prime}})$}};\draw[otNavy!70,line width=.8pt]{c(add(O2,e,-.8))}--{c(add(O2,e,2.3))}node[above,font=\scriptsize]{{$(\Delta^{{\prime}})$}};'
    t+=rf'\draw[geoVecteur]{c(add(O,(-.5,-1.3)))}--{c(add(O2,(-.5,-1.3)))}node[midway,below=2pt,sloped,font=\scriptsize]{{translation}};'
    t+=r'\geoSolution{'+arc_angle(O2,add(O2,(1,0)),add(O2,e),.6,r'$35^\circ$','otGreenDark',.95)+'}'
    GEOMETRIE['trans-09']={'translation':{'points':[O,add(O,d),add(O,e)],'images':[O2,add(O2,d),add(O2,e)],'deplacement':V}}
    dessin('trans-09',t,'Les droites images sont parallèles aux droites de départ.')
    dessin('trans-10',r'\draw[geoVecteur](0,0)--node[below,sloped]{5 à droite, 2 en haut}(5,2);\draw[geoVecteur](5,2)--node[right]{3 à gauche, 4 en haut}(2,6);\geoSolution{\draw[geoReponse,->](0,0)--node[left]{2 à droite, 6 en haut}(2,6);}')
    FIGURES['trans-10']['tex']=FIGURES['trans-10']['tex'].replace(']'+r'\draw[geoVecteur](0,0)',r']\begin{scope}[scale=.62]\draw[geoVecteur](0,0)',1).replace(r'\end{tikzpicture}',r'\end{scope}\end{tikzpicture}')
    # Exercice 11 : construction sans quadrillage.
    P={'E':(0,0),'F':(2,-1),'G':(1.5,1.5),'K':(4,1)};V=vec(P['E'],P['K']);F2=add(P['F'],V);G2=add(P['G'],V)
    t=seg(P,'E-F-G-E')+rf'\draw[geoVecteur]{c(P["E"])}--{c(P["K"])};'+points(P,'EFGK',{'E':'left','F':'below','G':'above','K':'below right'})
    sol=rf'\draw[otGreenDark,line width=.85pt]{c(P["K"])}--{c(F2)}--{c(G2)}--cycle;\draw[otGreenDark,dashed]{c(P["F"])}--{c(F2)} {c(P["G"])}--{c(G2)};'+points({"F'":F2,"G'":G2},["F'","G'"],{"F'":'below right',"G'":'above right'},'otGreenDark')
    GEOMETRIE['trans-11']={'translation':{'points':[P['E'],P['F'],P['G']],'images':[P['K'],F2,G2],'deplacement':V}}
    dessin('trans-11',t+r'\geoSolution{'+sol+'}','Construction au compas et à la règle ; au corrigé, les parallélogrammes EFF’K et EGG’K.')
    # Exercice 12 : parallélogramme et translation.
    P=echelle({'A':(0,0),'B':(5,0),'C':(6.5,2.5),'D':(1.5,2.5)},.7)
    t=seg(P,'A-B-C-D-A')+rf'\draw[geoVecteur]{c(add(P["A"],(.1,-.35)))}--{c(add(P["B"],(-.1,-.35)))};'+points(P,'ABCD',{'A':'below left','B':'below right','C':'above right','D':'above left'})
    t+=r'\geoSolution{'+rf'\draw[geoReponse,->]{c(add(P["D"],(.1,.35)))}--{c(add(P["C"],(-.1,.35)))};'+'}'
    GEOMETRIE['trans-12']={'translation':{'points':[P['A'],P['D']],'images':[P['B'],P['C']],'deplacement':vec(P['A'],P['B'])}}
    dessin('trans-12',t,'La flèche indique la translation qui transforme A en B.')
    tex=''
    for i in range(6):
        for j in range(4):tex+=rf'\draw[draw=otNavy,fill=otGreen!{15 if (i+j)%2 else 30}]({i*.8},{j*.8})rectangle++(.8,.8);'
    dessin('trans-13',tex+r'\draw[|<->|](0,-.5)--node[below]{2 cm}(.8,-.5);\geoSolution{\draw[otGreenDark,->,line width=1pt](.4,.4)--(2,1.2);}','Pavage de six colonnes et quatre lignes ; chaque case est un motif.')
    # Exercice 14 : deux parterres.
    P=echelle({'A':(0,0),'B':(6,0),'C':(0,8),'D':(8.5,-3),'E':(14.5,-3),'F':(8.5,5)},.32)
    t=seg(P,'A-B-C-A')+seg(P,'D-E-F-D','otNavy!70,line width=.85pt')+droit(P['B'],P['A'],P['C'])+droit(P['E'],P['D'],P['F'])+rf'\draw[geoVecteur]{c(P["A"])}--{c(P["D"])};'
    t+=texte_seg(P['A'],P['B'],'6 m',.22,1,t=.6)+texte_seg(P['C'],P['A'],'8 m',.3,-1)+texte_seg(P['B'],P['C'],'10 m',.32,-1)+points(P,'ABCDEF',{'A':'left','B':'below','C':'above','D':'below left','E':'below right','F':'above'})
    t+=r'\geoSolution{'+rf'\draw[otGreenDark,dashed,line width=.8pt]{c(P["A"])}--{c(P["B"])}--{c(P["E"])}--{c(P["D"])}--cycle;'+'}'
    GEOMETRIE['trans-14']={'translation':{'points':[P['A'],P['B'],P['C']],'images':[P['D'],P['E'],P['F']],'deplacement':vec(P['A'],P['D'])}}
    dessin('trans-14',t,'DEF est l’image de ABC par la translation qui transforme A en D.')
    # Exercice 15 : un angle transporté.
    B=(0,0);C=(3.4,0);A=(2.6*cos(radians(70)),2.6*sin(radians(70)));E=add(A,vec(B,C));X=(4.6,0)
    P={'A':A,'B':B,'C':C}
    t=seg(P,'A-B-C-A')+arc_angle(B,C,A,.45,r'$70^\circ$')+rf'\draw[geoVecteur]{c(add(B,(0,-.4)))}--{c(add(C,(0,-.4)))};'+points(P,'ABC',{'A':'above','B':'below left','C':'below'})
    sol=rf'\draw[otGreenDark,line width=.85pt]{c(A)}--{c(E)}--{c(C)};\draw[otGreenDark,dashed]{c(C)}--{c(X)};'+arc_angle(C,X,E,.42,r'$70^\circ$','otGreenDark')+arc_angle(C,E,B,.62,r'$110^\circ$','otGreenDark',.98)+points({'E':E},'E',{'E':'above'},'otGreenDark')
    GEOMETRIE['trans-15']={'translation':{'points':[B,A],'images':[C,E],'deplacement':vec(B,C)}}
    dessin('trans-15',t+r'\geoSolution{'+sol+'}','La flèche indique la translation qui transforme B en C.')

# ---------------------------------------------------------------------
# Chapitre 14 : droite des milieux
# ---------------------------------------------------------------------
def tri_milieux(P,a='A',b='B',cc='C',m1='I',m2='J',coches=True,nb=(1,2)):
    """Triangle avec deux milieux codés de [ab] et [acc]."""
    I=mil(P[a],P[b]);J=mil(P[a],P[cc]);P[m1]=I;P[m2]=J
    t=seg(P,f'{a}-{b}-{cc}-{a}')
    if coches:t+=coche(P[a],I,nb[0])+coche(I,P[b],nb[0])+coche(P[a],J,nb[1])+coche(J,P[cc],nb[1])
    return t

def milieux():
    base={'A':(1.6,3.4),'B':(0,0),'C':(6,0)}
    P=echelle(base,.8);t=tri_milieux(P)+seg(P,'I-J','otGreenDark,line width=1pt')
    t+=points(P,'ABCIJ',{'A':'above','B':'below left','C':'below right','I':'left','J':'right'})+r'\node[anchor=west,font=\scriptsize]at(5,2.4){$(IJ)\parallel(BC)$};\node[anchor=west,font=\scriptsize]at(5,1.9){$IJ=\frac12BC$};'
    registre('cours-milieux',P,milieux=[('I','A','B'),('J','A','C')],paralleles=[(('I','J'),('B','C'))],moities=[(('I','J'),('B','C'))])
    dessin('cours-milieux',t,'I et J sont les milieux codés de $[AB]$ et de $[AC]$.')
    def simple(nom,lab_bc,lab_ij,sol_bc='',sol_ij='',noms='ABCIJ',base_=base,k=.75,leg=None):
        P=echelle(base_,k);t=tri_milieux(P,*noms[:3],noms[3],noms[4])+seg(P,f'{noms[3]}-{noms[4]}','otNavy,line width=.8pt')
        t+=points(P,noms,{noms[0]:'above',noms[1]:'below left',noms[2]:'below right',noms[3]:'left',noms[4]:'right'})
        if lab_bc:t+=texte_seg(P[noms[1]],P[noms[2]],lab_bc,.28,-1)
        if lab_ij:t+=texte_seg(P[noms[3]],P[noms[4]],lab_ij,.25,1)
        registre(nom,P,milieux=[(noms[3],noms[0],noms[1]),(noms[4],noms[0],noms[2])],paralleles=[((noms[3],noms[4]),(noms[1],noms[2]))])
        dessin(nom,t,leg) if leg else dessin(nom,t)
    simple('mil-01','7,4 cm',reponse('3,7 cm'))
    simple('mil-02','',r'\geoSolution{\textcolor{otGreenDark}{$(MN)\parallel(FG)$}}',noms='EFGMN',base_={'E':(2,4),'F':(0,0),'G':(6,0)})
    simple('mil-03',reponse('10,4 cm'),'5,2 cm')
    # Exercices 4 et 7 : parallèle passant par un milieu.
    def parallele(nom,lab_ac,lab_bc,sol):
        P=echelle(base,.75);A,B,C=P['A'],P['B'],P['C'];I=mil(A,B);J=mil(A,C);P.update(I=I,J=J)
        t=seg(P,'A-B-C-A')+coche(A,I)+coche(I,B)+droite(I,J,.35,.6)+points(P,'ABCIJ',{'A':'above','B':'below left','C':'below right','I':'left','J':'right'})
        t+=rf'\node[font=\scriptsize,anchor=west]at{c(add(J,vec(I,J),.65))}{{$(d)\parallel(BC)$}};'
        if lab_ac:t+=texte_seg(A,C,lab_ac,.3,1,t=.3)
        if lab_bc:t+=texte_seg(B,C,lab_bc,.28,-1)
        t+=r'\geoSolution{'+coche(A,J,2,'otGreenDark')+coche(J,C,2,'otGreenDark')+sol+'}'
        registre(nom,P,milieux=[('I','A','B'),('J','A','C')],paralleles=[(('I','J'),('B','C'))])
        dessin(nom,t,'$(d)$ est la parallèle à $(BC)$ passant par I ; elle coupe $[AC]$ en J.')
    parallele('mil-04','9 cm','',r'\node[font=\scriptsize,text=otGreenDark]at(3.4,2.75){$AJ=4{,}5$ cm};')
    # Exercice 5 : choisir le théorème.
    t='';Ps={}
    for k,(titre,code) in enumerate([('Figure 1','deux'),('Figure 2','par'),('Figure 3','long')]):
        P=echelle({'E':(1.2,2.6),'F':(0,0),'G':(3.2,0)},1,k*4,0);E_,F,G=P['E'],P['F'],P['G'];M=mil(E_,F);N=mil(E_,G);P.update(M=M,N=N)
        t+=seg(P,'E-F-G-E')+seg(P,'M-N','otNavy,line width=.8pt')+coche(E_,M)+coche(M,F)
        if code in ('deux','long'):t+=coche(E_,N,2)+coche(N,G,2)
        if code=='par':t+=rf'\node[font=\scriptsize]at({k*4+2.4:.2f},2.1){{$(MN)\parallel(FG)$}};'+r'\geoSolution{'+coche(E_,N,2,'otGreenDark')+coche(N,G,2,'otGreenDark')+'}'
        if code=='long':t+=texte_seg(F,G,'8 cm',.28,-1)+texte_seg(M,N,reponse('4 cm'),.25,1)
        if code=='deux':t+=r'\geoSolution{'+rf'\node[font=\scriptsize,text=otGreenDark]at({k*4+2.5:.2f},2.1){{$(MN)\parallel(FG)$}};'+'}'
        t+=points(P,'EFGMN',{'E':'above','F':'below left','G':'below right','M':'left','N':'right'})+rf'\node[font=\scriptsize]at({k*4+1.6:.2f},-.6){{{titre}}};'
        Ps.update({kk+str(k+1):v for kk,v in P.items()})
    registre('mil-05',Ps,milieux=[(f'M{k}',f'E{k}',f'F{k}') for k in (1,2,3)]+[(f'N{k}',f'E{k}',f'G{k}') for k in (1,2,3)],paralleles=[((f'M{k}',f'N{k}'),(f'F{k}',f'G{k}')) for k in (1,2,3)])
    dessin('mil-05',t,'Les codages sont des données de l’énoncé.')
    # Exercice 6 : triangle des milieux.
    P=echelle({'A':(0,0),'B':(6,0),'C':(0,8)},.48);I=mil(P['A'],P['B']);J=mil(P['A'],P['C']);K=mil(P['B'],P['C']);P.update(I=I,J=J,K=K)
    t=seg(P,'A-B-C-A')+seg(P,'I-J-K-I','otNavy,dashed')+texte_seg(P['A'],P['B'],'6 cm',.27,-1,t=.25)+texte_seg(P['C'],P['A'],'8 cm',.42,-1,t=.25)+texte_seg(P['B'],P['C'],'10 cm',.42,-1,t=.25)
    t+=points(P,'ABCIJK',{'A':'below left','B':'below right','C':'above','I':'below','J':'left','K':'above right'})
    t+=r'\geoSolution{'+texte_seg(I,J,'5',.2,-1,color='otGreenDark')+texte_seg(J,K,'3',.2,1,color='otGreenDark')+texte_seg(K,I,'4',.2,1,color='otGreenDark')+'}'
    registre('mil-06',P,milieux=[('I','A','B'),('J','A','C'),('K','B','C')],moities=[(('I','J'),('B','C')),(('J','K'),('A','B')),(('I','K'),('A','C'))])
    dessin('mil-06',t,'Les milieux sont donnés par l’énoncé ; au corrigé, les côtés de IJK en cm.')
    parallele('mil-07','','9 cm',r'\node[font=\scriptsize,text=otGreenDark]at(3.4,2.75){$IJ=4{,}5$ cm};')
    # Exercice 8 : une rédaction incomplète.
    P=echelle({'A':(0,0),'B':(6,0),'C':(2,4)},.7);I=mil(P['A'],P['B']);J=add(P['A'],vec(P['A'],P['C']),.75);K=mil(P['A'],P['C']);P.update(I=I,J=J)
    t=seg(P,'A-B-C-A')+coche(P['A'],I)+coche(I,P['B'])+seg(P,'I-J','otNavy,line width=.8pt')+points(P,'ABCIJ',{'A':'below left','B':'below right','C':'above','I':'below','J':'left'})
    t+=r'\geoSolution{'+droite(I,K,.2,.4,'otGreenDark,dashed')+rf'\fill[otGreenDark]{c(K)}circle(1.3pt)node[left,font=\scriptsize]{{milieu}};\node[font=\scriptsize,text=otGreenDark,anchor=west]at(3.2,2.3){{$(IJ)$ non parallèle à $(BC)$}};'+'}'
    registre('mil-08',dict(P,K=K),milieux=[('I','A','B'),('K','A','C')],non_paralleles=[(('I','J'),('B','C'))],paralleles=[(('I','K'),('B','C'))],alignes=[('A','J','C')])
    dessin('mil-08',t,'J est un point de $[AC]$ ; au corrigé, la parallèle passant par le milieu de $[AC]$.')
    # Exercice 9 : dans un rectangle.
    P=echelle({'A':(0,0),'B':(8,0),'C':(8,6),'D':(0,6)},.45);I=mil(P['A'],P['B']);J=mil(P['B'],P['C']);P.update(I=I,J=J)
    t=seg(P,'A-B-C-D-A')+seg(P,'A-C','otNavy,line width=.6pt')+seg(P,'I-J','otNavy,line width=.8pt')+coche(P['A'],I)+coche(I,P['B'])+coche(P['B'],J,2)+coche(J,P['C'],2)
    for (a,b,cc) in [('D','A','B'),('A','B','C'),('B','C','D'),('C','D','A')]:t+=droit(P[a],P[b],P[cc])
    t+=texte_seg(P['A'],P['C'],'10 cm',.28,1)+points(P,'ABCDIJ',{'A':'below left','B':'below right','C':'above right','D':'above left','I':'below','J':'right'})+texte_seg(I,J,reponse('5 cm'),.28,-1)
    registre('mil-09',P,milieux=[('I','A','B'),('J','B','C')],paralleles=[(('I','J'),('A','C'))],moities=[(('I','J'),('A','C'))])
    dessin('mil-09',t)
    # Exercice 10 : AIKJ.
    P=echelle({'A':(0,0),'B':(7,0),'C':(1.5,sqrt(22.75))},.6);I=mil(P['A'],P['B']);J=mil(P['A'],P['C']);K=mil(P['B'],P['C']);P.update(I=I,J=J,K=K)
    t=r'\geoSolution{'+rf'\fill[otGreen!25]{c(P["A"])}--{c(I)}--{c(K)}--{c(J)}--cycle;'+'}'+seg(P,'A-B-C-A')+seg(P,'I-K-J','otNavy,dashed')
    t+=coche(P['A'],I)+coche(I,P['B'])+coche(P['A'],J,2)+coche(J,P['C'],2)+coche(P['B'],K,3)+coche(K,P['C'],3)
    t+=texte_seg(P['A'],P['B'],'7 cm',.27,-1)+texte_seg(P['C'],P['A'],'5 cm',.3,1)+points(P,'ABCIJK',{'A':'below left','B':'below right','C':'above','I':'below','J':'left','K':'right'})
    registre('mil-10',P,milieux=[('I','A','B'),('J','A','C'),('K','B','C')],paralleles=[(('I','K'),('A','C')),(('J','K'),('A','B'))])
    dessin('mil-10',t,'Au corrigé, le parallélogramme AIKJ est coloré.')
    # Exercice 11 : milieux de milieux.
    P=echelle(base,1.0);A,B,C=P['A'],P['B'],P['C'];I=mil(A,B);J=mil(A,C);M=mil(A,I);N=mil(A,J);P.update(I=I,J=J,M=M,N=N)
    t=seg(P,'A-B-C-A')+seg(P,'I-J','otNavy,line width=.7pt')+seg(P,'M-N','otNavy,line width=.7pt')+texte_seg(B,C,'12 cm',.28,-1)+texte_seg(M,N,reponse('3 cm'),.22,1)
    t+=points(P,'ABCIJMN',{'A':'above','B':'below left','C':'below right','I':'left','J':'right','M':'left','N':'right'})
    registre('mil-11',P,milieux=[('I','A','B'),('J','A','C'),('M','A','I'),('N','A','J')],paralleles=[(('M','N'),('B','C'))])
    dessin('mil-11',t,'Les milieux sont donnés par l’énoncé et ne sont pas codés.')
    # Exercice 12 : trapèze.
    P=echelle({'A':(0,3),'B':(6,3),'C':(9,0),'D':(-1,0)},.55);A,B,C,D=P['A'],P['B'],P['C'],P['D'];I=mil(A,D);J=mil(B,D);K=mil(B,C);P.update(I=I,J=J,K=K)
    t=seg(P,'A-B-C-D-A')+seg(P,'B-D','otNavy,dashed')+droite(I,K,.12,.12)+coche(A,I)+coche(I,D)+texte_seg(A,B,'6 cm',.25,1)+texte_seg(D,C,'10 cm',.27,-1)
    t+=points(P,'ABCDIJK',{'A':'above left','B':'above right','C':'below right','D':'below left','I':'left','J':'below','K':'right'})
    t+=r'\geoSolution{'+coche(B,J,2,'otGreenDark')+coche(J,D,2,'otGreenDark')+coche(B,K,3,'otGreenDark')+coche(K,C,3,'otGreenDark')+'}'
    registre('mil-12',P,milieux=[('I','A','D'),('J','B','D'),('K','B','C')],paralleles=[(('A','B'),('D','C')),(('I','K'),('A','B'))],alignes=[('I','J','K')])
    dessin('mil-12',t,'La droite tracée passe par I, parallèlement à $(AB)$.')
    # Exercice 13 : Varignon.
    P=echelle({'A':(0,0),'B':(2,-2.4),'C':(8,0),'D':(4.6,3)},.6);A,B,C,D=P['A'],P['B'],P['C'],P['D']
    I=mil(A,B);J=mil(B,C);K=mil(C,D);L=mil(D,A);P.update(I=I,J=J,K=K,L=L)
    t=r'\geoSolution{'+rf'\fill[otGreen!25]{c(I)}--{c(J)}--{c(K)}--{c(L)}--cycle;'+'}'+seg(P,'A-B-C-D-A')+seg(P,'A-C','otNavy,dashed')+seg(P,'I-J-K-L-I','otNavy,line width=.8pt')
    t+=coche(A,I)+coche(I,B)+coche(B,J,2)+coche(J,C,2)+coche(C,K,3)+coche(K,D,3)+coche(D,L,4)+coche(L,A,4)
    t+=points(P,'ABCDIJKL',{'A':'left','B':'below','C':'right','D':'above','I':'below left','J':'below right','K':'above right','L':'above left'})
    registre('mil-13',P,milieux=[('I','A','B'),('J','B','C'),('K','C','D'),('L','D','A')],paralleles=[(('I','J'),('A','C')),(('L','K'),('A','C')),(('I','L'),('B','D'))])
    dessin('mil-13',t,'Quadrilatère quelconque et ses quatre milieux ; diagonale $[AC]$ en pointillés.')
    # Exercice 14 : le point de concours des médianes.
    P=echelle({'A':(1,5),'B':(0,0),'C':(7,0)},.62);A,B,C=P['A'],P['B'],P['C'];I=mil(B,C);J=mil(A,C);G=((A[0]+B[0]+C[0])/3,(A[1]+B[1]+C[1])/3);K=mil(A,G);L=mil(B,G);P.update(I=I,J=J,G=G,K=K,L=L)
    t=seg(P,'A-B-C-A')+seg(P,'A-I','otNavy,line width=.7pt')+seg(P,'B-J','otNavy,line width=.7pt')+coche(B,I)+coche(I,C)+coche(A,J,2)+coche(J,C,2)
    t+=r'\geoSolution{'+rf'\draw[otGreenDark,line width=.9pt]{c(K)}--{c(L)}--{c(I)}--{c(J)}--cycle;'+'}'
    t+=points(P,'ABCIJGKL',{'A':'above','B':'below left','C':'below right','I':'below','J':'above right','G':'right','K':'left','L':'below'})
    registre('mil-14',P,milieux=[('I','B','C'),('J','A','C'),('K','A','G'),('L','B','G'),('G','K','I'),('G','L','J')],paralleles=[(('K','L'),('J','I'))])
    dessin('mil-14',t,'Au corrigé, le parallélogramme KLIJ.')
    # Exercice 15 : milieu de l’hypoténuse.
    P=echelle({'A':(0,0),'B':(6,0),'C':(0,8)},.36);A,B,C=P['A'],P['B'],P['C'];I=mil(B,C);J=mil(A,B);P.update(I=I,J=J)
    t=seg(P,'A-B-C-A')+droit(B,A,C)+seg(P,'I-J','otNavy,line width=.8pt')+coche(B,I)+coche(I,C)+coche(A,J,2)+coche(J,B,2)
    t+=r'\geoSolution{'+droite(J,I,.6,.35,'otGreenDark,dashed')+droit(A,J,I,'otGreenDark')+rf'\draw[otGreenDark,line width=.8pt]{c(A)}--{c(I)};\draw[otGreenDark,dashed]{c(I)}circle({hypot(*vec(I,A)):.3f});'+'}'
    t+=points(P,'ABCIJ',{'A':'below left','B':'below right','C':'above','I':'right','J':'below'})
    registre('mil-15',P,milieux=[('I','B','C'),('J','A','B')],perpendiculaires=[(('A','B'),('A','C')),(('I','J'),('A','B'))],cercles=[('I',['A','B','C'])])
    dessin('mil-15',t,'Au corrigé : la médiatrice de $[AB]$ et le cercle de centre I.')

# ---------------------------------------------------------------------
# Chapitre 15 : Pythagore
# ---------------------------------------------------------------------
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
    for i,(a,cc,b,r,p,l) in enumerate(dat,1):
        extra=''
        if i==6:extra=r'\geoSolution{\node[anchor=west,font=\scriptsize,text=otGreenDark]at(4.4,2.4){$49\ne41$ : pas rectangle};}'
        if i==7:extra=r'\draw[otMuted,dashed](0,3)--(4,3)--(4,0);'
        if i==10:
            cx=6.3**2/10.5;cy=sqrt(6.3**2-cx**2);sc=min(6.4/10.5,3/cy)
            vx,vy=cx*sc,cy*sc;u=(-cx/6.3,-cy/6.3);v=((10.5-cx)/8.4,-cy/8.4)
            p1=(vx+.18*u[0],vy+.18*u[1]);p2=(p1[0]+.18*v[0],p1[1]+.18*v[1]);p3=(vx+.18*v[0],vy+.18*v[1])
            extra=r'\geoSolution{\draw[otGreenDark]'+f'({p1[0]},{p1[1]})--({p2[0]},{p2[1]})--({p3[0]},{p3[1]});'+'}'
        triangle(f'pyth-{i:02}',a,cc,b,labels=l,right=r,proof_right=p,extra=extra)
    triangle('cours-pythagore',3,4,5,right=True,labels={(0,1):'$AB$',(0,2):'$AC$',(1,2):'$BC$'})
    FIGURES.pop('pyth-09');GEOMETRIE.pop('pyth-09')
    tex=axes((-1,7),(-1,9),2,2,ortho=True)
    tex=tex.replace(r'\node[below left,font=\tiny]at(0,0){0};','')
    tex+=polygone([(0,0),(6,0),(0,8)])
    for lab,x,y in [('A',0,0),('B',6,0),('C',0,8)]:tex+=rf'\fill[otNavy]({x},{y})circle(1.3pt)node[above right,geoLabel]{{$ {lab} $}};'
    tex+=r'\geoSolution{\node[text=otGreenDark,above right]at(3,4){10 cm};}\end{scope}'
    dessin('pyth-09',tex,'Repère orthonormé ; une unité représente 1 cm.')
    dessin('pyth-11',r'\draw[geoTrait](0,0)--(3,1.25)--(0,2.5)--(-3,1.25)--cycle;\draw[otMuted,dashed](-3,1.25)--(3,1.25) (0,0)--(0,2.5);\node[below]at(0,0){10 cm : diagonale verticale};\node[above]at(0,2.5){24 cm : diagonale horizontale};\draw[otMuted](0,1.4)--(.15,1.4)--(.15,1.25);\geoSolution{\node[text=otGreenDark,font=\scriptsize]at(2.1,2.15){13 cm};}')
    rectangles('pyth-12',reponse('12 cm'),'5 cm',r'\draw[geoTrait](0,0)--(5,2.5)node[midway,above,sloped,fill=white]{13 cm};')
    dessin('pyth-13',r'\draw[geoTrait](0,0)rectangle(3.2,2.4);\draw[otGreenDark](0,0)--(3.2,2.4);\node[below]at(1.6,0){8 m};\node[left]at(0,1.2){6 m};\begin{scope}[shift={(5,0)}]\draw[geoTrait](0,0)rectangle(1.4,3.36);\draw[otGreenDark](0,0)--(1.4,3.36);\node[below]at(.7,0){10 m};\node[right]at(1.4,1.68){24 m};\end{scope}')
    triangle('pyth-14',4,7,right=True,labels={(0,1):'4 cm',(0,2):'7 cm',(1,2):reponse(r'$\sqrt{65}$ cm')})
    rectangles('pyth-15','12 m','5 m',r'\draw[geoTrait](0,0)--(5,2.5)node[midway,above,sloped,fill=white]{'+reponse('13 m')+'};')

# ---------------------------------------------------------------------
# Chapitre 16 : triangle rectangle et cercle circonscrit
# ---------------------------------------------------------------------
def tri_cercle(nom,r,ang,labels=(),sol_cercle=True,code_droit=True,extra='',sol='',coches=False,legende=None,noms='ABCO',centre_visible=False):
    """Triangle de sommet a inscrit dans le cercle de diamètre [b cc] et de centre o."""
    a,b,cc,o=noms
    P={b:(-r,0),cc:(r,0),a:(r*cos(radians(ang)),r*sin(radians(ang))),o:(0,0)}
    cer=rf'\draw[{"otGreenDark" if sol_cercle else "otNavy"},line width=.8pt](0,0)circle({r});'
    centre=rf'\fill[{{col}}](0,0)circle(1.4pt)node[below,font=\small,text={{col}}]{{${o}$}};'
    t=(r'\geoSolution{'+cer+'}' if sol_cercle else cer)
    if centre_visible:t+=centre.replace('{col}','otNavy')
    else:t+=r'\geoSolution{'+centre.replace('{col}','otGreenDark')+'}'
    t+=seg(P,f'{a}-{b}-{cc}-{a}')+(droit(P[b],P[a],P[cc]) if code_droit else '')
    for (p,q,txt,side) in labels:t+=texte_seg(P[p],P[q],txt,.3,side)
    if coches:t+=coche(P[b],P[o])+coche(P[o],P[cc])
    t+=points(P,a+b+cc,{a:'above',b:'left',cc:'right'})+extra+(r'\geoSolution{'+sol+'}' if sol else '')
    registre(nom,P,cercles=[(o,[a,b,cc])],perpendiculaires=[((a,b),(a,cc))],milieux=[(o,b,cc)])
    dessin(nom,t,legende) if legende else dessin(nom,t)
    return P

def cercle():
    r=1.7
    A=(r*cos(radians(115)),r*sin(radians(115)))
    tri_cercle('cours-cercle',r,115,sol_cercle=False,coches=True,noms='ABCI',centre_visible=True,
               extra=seg({'A':A,'I':(0,0)},'A-I','otNavy,line width=.6pt')+coche(A,(0,0)),
               legende='Le cercle circonscrit au triangle ABC, rectangle en A, a pour diamètre l’hypoténuse $[BC]$.')
    tri_cercle('cer-01',r,62,[('B','C','9 cm',-1)],sol=r'\node[font=\scriptsize,text=otGreenDark]at(.85,-.55){rayon 4,5 cm};')
    A=(r*cos(radians(130)),r*sin(radians(130)))
    tri_cercle('cer-02',r,130,[('B','C','13 cm',-1)],coches=True,noms='ABCI',centre_visible=True,
               extra=rf'\draw[geoDonnee]{c(A)}--(0,0);',sol=texte_seg(A,(0,0),r'\textcolor{otGreenDark}{6,5 cm}',.3,1))
    A=(r*cos(radians(58)),r*sin(radians(58)))
    tri_cercle('cer-03',r,58,code_droit=False,sol_cercle=False,centre_visible=True,sol=droit((-r,0),A,(r,0),'otGreenDark'),
               legende='$[BC]$ est un diamètre du cercle de centre O.')
    tri_cercle('cer-04',r,127,[('A','B','6 cm',1),('A','C','8 cm',1)],sol=r'\node[font=\scriptsize,text=otGreenDark]at(0,-.6){$BC=10$ cm, rayon 5 cm};')
    # Exercice 5 : triangle équilatéral inscrit au corrigé.
    E=[(1.6*cos(radians(90+120*k)),1.6*sin(radians(90+120*k))) for k in range(3)]
    t=r'\draw[geoTrait](0,0)circle(1.6);\fill[otNavy](0,0)circle(1.3pt)node[below]{$O$};\geoEnonce{\node[font=\scriptsize]at(0,-2.05){Chercher un contre-exemple.};}'
    t+=r'\geoSolution{'+polygone(E,'otGreenDark')+r'\node[font=\scriptsize,text=otGreenDark]at(0,-2.05){triangle équilatéral : angles de $60^\circ$};}'
    GEOMETRIE['cer-05']={'points':{'O':(0,0),'E1':E[0],'E2':E[1],'E3':E[2]},'cercles':[('O',['E1','E2','E3'])],'egalites':[(('E1','E2'),('E2','E3'))]}
    dessin('cer-05',t,'Au corrigé, un triangle inscrit qui n’est pas rectangle.')
    A=(r*cos(radians(70)),r*sin(radians(70)))
    tri_cercle('cer-06',r,70,[('B','I','3,5 cm',-1)],code_droit=False,coches=True,noms='ABCI',centre_visible=True,
               extra=seg({'A':A,'I':(0,0)},'A-I','otNavy,line width=.7pt')+coche(A,(0,0)),sol=droit((-r,0),A,(r,0),'otGreenDark'),
               legende='I est le milieu de $[BC]$ ; les codages indiquent $IA=IB=IC$.')
    # Exercice 7 : C sur le cercle de diamètre [AB], angle de 32 degrés en B.
    C=(r*cos(radians(116)),r*sin(radians(116)));A,B=(-r,0),(r,0)
    tri_cercle('cer-07',r,116,code_droit=False,sol_cercle=False,noms='CABO',centre_visible=True,
               extra=arc_angle(B,A,C,.5,'$32^\\circ$'),sol=droit(A,C,B,'otGreenDark')+arc_angle(A,C,B,.55,'$58^\\circ$','otGreenDark'))
    # Exercice 8 : rectangle sans équerre.
    P={'A':(r*cos(radians(200)),r*sin(radians(200))),'C':(r*cos(radians(20)),r*sin(radians(20))),'B':(r*cos(radians(-50)),r*sin(radians(-50))),'D':(r*cos(radians(130)),r*sin(radians(130))),'O':(0,0)}
    t=rf'\draw[geoTrait](0,0)circle({r});'+seg(P,'A-C','otNavy,line width=.7pt')+seg(P,'B-D','otNavy,line width=.7pt')+points(P,'ABCDO',{'A':'left','B':'below right','C':'right','D':'above left','O':'below'})
    t+=r'\geoSolution{'+rf'\draw[otGreenDark,line width=.9pt]{c(P["A"])}--{c(P["B"])}--{c(P["C"])}--{c(P["D"])}--cycle;'+droit(P['A'],P['B'],P['C'],'otGreenDark')+'}'
    registre('cer-08',P,cercles=[('O',['A','B','C','D'])],milieux=[('O','A','C'),('O','B','D')],perpendiculaires=[(('B','A'),('B','C'))])
    dessin('cer-08',t,'Deux diamètres d’un même cercle ; au corrigé, le rectangle ABCD.')
    # Exercice 9 : lieu des points M.
    P={'A':(-1.6,0),'B':(1.6,0)}
    t=seg(P,'A-B')+points(P,'AB',{'A':'left','B':'right'})+texte_seg(P['A'],P['B'],'6 cm',.28,-1)
    sol=r'\draw[otGreenDark,dashed](0,0)circle(1.6);'
    Ms={}
    for k,a in enumerate([60,135,-110]):
        M=(1.6*cos(radians(a)),1.6*sin(radians(a)));Ms[f'M{k+1}']=M
        sol+=rf'\draw[otGreenDark]{c(P["A"])}--{c(M)}--{c(P["B"])};'+droit(P['A'],M,P['B'],'otGreenDark')+rf'\fill[otGreenDark]{c(M)}circle(1.3pt);'
    registre('cer-09',dict(P,O=(0,0),**Ms),cercles=[('O',['A','B']+list(Ms))],perpendiculaires=[((m,'A'),(m,'B')) for m in Ms])
    dessin('cer-09',t+r'\geoSolution{'+sol+'}','Au corrigé : le cercle de diamètre $[AB]$ et trois positions de M.')
    C=(r*cos(radians(48)),r*sin(radians(48)));A,B=(-r,0),(r,0)
    tri_cercle('cer-10',r,48,[('A','C','6 cm',1)],code_droit=False,sol_cercle=False,noms='CABO',centre_visible=True,
               sol=droit(A,C,B,'otGreenDark')+texte_seg(C,B,r'\textcolor{otGreenDark}{8 cm}',.3,1))
    # Exercice 11 : perpendiculaire au compas.
    k=.75;P={'O':(1*k,2*k),'A':(0,0),'B':(2*k,0),'C':(0,4*k)};R=hypot(*vec(P['O'],P['A']))
    t=rf'\draw[otMuted](-1.4,0)--(2.6,0)node[right,font=\scriptsize]{{$(d)$}};\draw[geoTrait]{c(P["O"])}circle({R:.3f});'+seg(P,'B-C','geoDonnee')+points(P,'OABC',{'O':'right','A':'below left','B':'below right','C':'above left'})
    t+=r'\geoSolution{'+rf'\draw[otGreenDark,line width=.9pt]{c(P["A"])}--{c(P["C"])};'+droit(P['B'],P['A'],P['C'],'otGreenDark')+'}'
    registre('cer-11',P,cercles=[('O',['A','B','C'])],milieux=[('O','B','C')],perpendiculaires=[(('A','C'),('A','B'))])
    dessin('cer-11',t,'$[BC]$ est un diamètre du cercle de centre O passant par A.')
    # Exercice 12 : demi-cercle.
    r2=1.9;P={'A':(-r2,0),'B':(r2,0),'C':(0,r2),'O':(0,0)}
    t=rf'\draw[geoTrait]({r2},0)arc(0:180:{r2});'+seg(P,'A-B')+seg(P,'A-C-B')+coche(P['A'],P['C'],2)+coche(P['C'],P['B'],2)+points(P,'ABCO',{'A':'left','B':'right','C':'above','O':'below'})+texte_seg(P['A'],P['B'],'10 cm',.3,-1,t=.78)
    t+=r'\geoSolution{'+droit(P['A'],P['C'],P['B'],'otGreenDark')+texte_seg(P['A'],P['C'],r'\textcolor{otGreenDark}{$\sqrt{50}$ cm}',.35,1)+'}'
    registre('cer-12',P,cercles=[('O',['A','B','C'])],egalites=[(('A','C'),('C','B'))],perpendiculaires=[(('C','A'),('C','B'))])
    dessin('cer-12',t)
    # Exercice 13 : distance du centre à un côté.
    P=echelle({'A':(0,0),'B':(5,0),'C':(0,12)},.3);O=mil(P['B'],P['C']);J=mil(P['A'],P['B']);P.update(O=O,J=J)
    t=seg(P,'A-B-C-A')+droit(P['B'],P['A'],P['C'])+texte_seg(P['A'],P['B'],'5 cm',.55,-1)+texte_seg(P['C'],P['A'],'12 cm',.45,-1)+coche(P['A'],J)+coche(J,P['B'])
    t+=r'\geoSolution{'+rf'\draw[otGreenDark,dashed]{c(O)}circle({hypot(*vec(O,P["A"])):.3f});\draw[otGreenDark,line width=.9pt]{c(O)}--{c(J)};'+droit(P['A'],J,O,'otGreenDark')+'}'
    t+=points(P,'ABCOJ',{'A':'below left','B':'below right','C':'above','O':'right','J':'below'})
    registre('cer-13',P,milieux=[('O','B','C'),('J','A','B')],perpendiculaires=[(('O','J'),('A','B'))],cercles=[('O',['A','B','C'])])
    dessin('cer-13',t,'Au corrigé : le cercle circonscrit et le segment $[OJ]$.')
    # Exercice 14 : rectangle inscrit.
    k=.3;P={'A':(-6*k,-2.5*k),'B':(-6*k,2.5*k),'C':(6*k,2.5*k),'D':(6*k,-2.5*k),'O':(0,0)}
    t=rf'\draw[geoTrait](0,0)circle({6.5*k:.3f});'+seg(P,'A-B-C-D-A')+droit(P['B'],P['A'],P['D'])+points(P,'ABCDO',{'A':'below left','B':'above left','C':'above right','D':'below right','O':'below'})+texte_seg(P['A'],P['B'],'5 cm',.3,-1)
    t+=r'\geoSolution{'+rf'\draw[otGreenDark,line width=.8pt]{c(P["A"])}--{c(P["C"])};'+texte_seg(P['B'],P['C'],r'\textcolor{otGreenDark}{12 cm}',.25,1)+'}'+r'\node[font=\scriptsize,anchor=west]at(2.2,-1.4){rayon : 6,5 cm};'
    registre('cer-14',P,cercles=[('O',['A','B','C','D'])],milieux=[('O','A','C'),('O','B','D')],perpendiculaires=[(('A','B'),('A','D'))])
    dessin('cer-14',t)
    # Exercice 15 : sans mesurer d’angle.
    k=.45;r3=4*k;phi=acos(5/8);B=(-r3,0);A=add(B,(cos(phi),sin(phi)),5*k);P={'A':A,'B':B,'C':(r3,0),'O':(0,0)}
    t=rf'\draw[geoTrait](0,0)circle({r3:.3f});'+seg(P,'A-B-C-A')+points(P,'ABCO',{'A':'above','B':'left','C':'right','O':'below'})+texte_seg(P['B'],P['A'],'5 cm',.3,1)+r'\node[font=\scriptsize,anchor=west]at(2.0,-1.3){rayon : 4 cm};'
    t+=r'\geoSolution{'+droit(P['B'],P['A'],P['C'],'otGreenDark')+texte_seg(P['A'],P['C'],r'\textcolor{otGreenDark}{$\sqrt{39}$ cm}',.3,1)+'}'
    registre('cer-15',P,cercles=[('O',['A','B','C'])],milieux=[('O','B','C')],perpendiculaires=[(('A','B'),('A','C'))])
    dessin('cer-15',t)

# ---------------------------------------------------------------------
# Chapitre 17 : solides
# ---------------------------------------------------------------------
def pyramide(nom,base='6 cm',h='8 cm',extra='',legende='Perspective cavalière ; SH est la hauteur perpendiculaire au plan de base.',nomH='H'):
    tex=r'\coordinate(A)at(0,0);\coordinate(B)at(4,0);\coordinate(C)at(5.3,1.2);\coordinate(D)at(1.3,1.2);\coordinate(S)at(2.65,4);\coordinate(H)at(2.65,.6);\draw[geoTrait](S)--(A)--(B)--(C)--(S)--(B);\draw[otMuted,dashed](A)--(D)--(C) (D)--(S)(S)--(H);'
    for p,pos in [('A','below left'),('B','below right'),('C','right'),('D','left'),('S','above'),('H','below')]:tex+=rf'\node[{pos},font=\scriptsize]at({p}){{$ {nomH if p=="H" else p} $}};'
    if base:tex+=rf'\path(A)--node[below]{{{base}}}(B);'
    if h:tex+=rf'\node[right,fill=white,font=\scriptsize]at(2.65,2.4){{{h}}};'
    tex+=r'\draw[otMuted](2.65,.85)--(2.9,.85)--(2.9,.6);'
    dessin(nom,tex+extra,legende)

def solides():
    pyramide('sol-01','','')
    pyramide('sol-02')
    cone('sol-03','3 cm','5 cm');cone('sol-04',reponse('4 cm'),'9 cm')
    # Exercice 5 : quatre solides.
    t=r'\begin{scope}[scale=.82]'
    t+=r'\draw[geoTrait](0,0)--(2.2,0)--(1,1.6)--cycle;\draw[geoTrait](1,1.6)--(2,2.3)--(3.2,.7)--(2.2,0) (2,2.3);\draw[otMuted,dashed](0,0)--(1,.7)--(3.2,.7) (1,.7)--(2,2.3);\draw[geoTrait](1,1.6)--(2,2.3);'
    t+=r'\begin{scope}[shift={(4.3,0)},scale=.62]\draw[geoTrait](2.65,4)--(0,0)--(4,0)--(5.3,1.2)--(2.65,4)--(4,0);\draw[otMuted,dashed](0,0)--(1.3,1.2)--(5.3,1.2) (1.3,1.2)--(2.65,4);\end{scope}'
    t+=r'\begin{scope}[shift={(9.6,0)}]\draw[geoTrait](-1,0)--(-1,2.3) (1,0)--(1,2.3);\draw[geoTrait](0,2.3)ellipse(1 and .3);\draw[geoTrait](-1,0)arc(180:360:1 and .3);\draw[otMuted,dashed](-1,0)arc(180:0:1 and .3);\end{scope}'
    t+=r'\begin{scope}[shift={(13.4,0)}]\draw[geoTrait](-1.2,0)--(0,2.5)--(1.2,0);\draw[geoTrait](-1.2,0)arc(180:360:1.2 and .32);\draw[otMuted,dashed](-1.2,0)arc(180:0:1.2 and .32);\end{scope}'
    for i,x in enumerate([1.5,5.7,9.6,13.4],1):t+=rf'\node[font=\small]at({x},-.85){{{i}}};'
    t+=r'\end{scope}'
    dessin('sol-05',t,'Perspectives cavalières ; les arêtes cachées sont en pointillés.')
    # Exercice 6 : un cône par rotation.
    P={'A':(0,0),'B':(0,2.8),'C':(2.1,0)}
    t=seg(P,'A-B-C-A')+droit(P['C'],P['A'],P['B'])+r'\draw[otMuted,dash dot](0,-.5)--(0,3.3);\draw[otMuted,dash dot](-.5,0)--(2.8,0);'+texte_seg(P['A'],P['B'],'4 cm',.3,1)+texte_seg(P['A'],P['C'],'3 cm',.25,-1)+points(P,'ABC',{'A':'below left','B':'above left','C':'below right'})
    sol=r'\begin{scope}[shift={(4.9,0)}]\draw[otGreenDark](-1.5,0)--(0,2)--(1.5,0);\draw[otGreenDark](-1.5,0)arc(180:360:1.5 and .35);\draw[otGreenDark,dashed](-1.5,0)arc(180:0:1.5 and .35) (0,0)--(0,2);\node[font=\scriptsize,text=otGreenDark]at(0,-.75){autour de $(AB)$ : $12\pi$ cm$^3$};\end{scope}'
    sol+=r'\begin{scope}[shift={(9.3,0)}]\draw[otGreenDark](-2,0)--(0,1.5)--(2,0);\draw[otGreenDark](-2,0)arc(180:360:2 and .45);\draw[otGreenDark,dashed](-2,0)arc(180:0:2 and .45) (0,0)--(0,1.5);\node[font=\scriptsize,text=otGreenDark]at(0,-.75){autour de $(AC)$ : $16\pi$ cm$^3$};\end{scope}'
    dessin('sol-06',t+r'\geoSolution{'+sol+'}','Le triangle tourne autour d’un côté de l’angle droit ; au corrigé, les deux cônes obtenus.')
    dessin('sol-07',r'\coordinate(A)at(0,0);\coordinate(B)at(5,0);\coordinate(C)at(1.2,1.5);\coordinate(S)at(2,4);\draw[geoTrait](S)--(A)--(B)--(S)--(C)--(B);\draw[otMuted,dashed](A)--(C) (S)--(2,.55);\node[below]at(2.5,0){8 cm};\node[right]at(2,2.4){hauteur : 10 cm};\draw[otGreenDark,dashed](1.2,1.5)--(1.2,0);\node[left,font=\scriptsize,fill=white]at(1.2,.75){3 cm};\draw[otMuted](1.2,.15)--(1.35,.15)--(1.35,0);\node[above]at(S){S};','Pyramide à base triangulaire ; les deux hauteurs concernent des plans différents.')
    pyramide('sol-08','base : 45 cm$^2$',reponse('10 cm'),r'\node[anchor=west,font=\scriptsize]at(5.7,2){$V=150$ cm$^3$};')
    tex=r'\draw[geoTrait](0,0)rectangle(2,2);'
    hh=sqrt(25-4)*.5
    for pts in [[(0,0),(2,0),(1,-hh)],[(2,0),(2,2),(2+hh,1)],[(2,2),(0,2),(1,2+hh)],[(0,2),(0,0),(-hh,1)]]:
        tex+=r'\geoSolution{'+polygone(pts,'otGreenDark')+'}'
    tex+=r'\node at(1,1){4 cm};\geoEnonce{\node[above]at(1,2.5){Construire les faces latérales.};}\geoSolution{\node[above]at(1,4.5){Arêtes latérales : 5 cm};}'
    dessin('sol-09',tex,'Le carré est fourni ; les quatre triangles latéraux sont ajoutés au corrigé.')
    dessin('sol-10',r'\geoEnonce{\draw[otMuted](0,0)circle(1.5);\node at(0,0){disque : $r=3$ cm};\node[anchor=west]at(2,0){Secteur à construire, rayon 5 cm.};}\geoSolution{\begin{scope}[scale=.55]\filldraw[fill=otGreen!15,draw=otNavy](0,0)--(0:5)arc(0:216:5)--cycle;\draw[otMuted](1,0)arc(0:216:1);\node at(-1.2,1.1){$216^\circ$};\node[above]at(2.5,0){5 cm};\draw[geoTrait](9,0)circle(3);\node at(9,0){$r=3$ cm};\draw[geoTrait](-14,0)--(-11,4)--(-8,0);\draw[geoTrait](-14,0)arc(180:360:3 and .65);\draw[otMuted,dashed](-14,0)arc(180:0:3 and .65) (-11,0)--(-11,4);\draw[geoTrait](-11,0)--node[below]{3 cm}(-8,0);\node[right,fill=white,font=\scriptsize]at(-9.5,2){5 cm};\node[above,font=\scriptsize]at(-11,4){Perspective};\end{scope}}','Les deux pièces sont présentées séparément ; le bord du secteur rejoint le cercle de base.')
    cone('sol-11','5 cm','12 cm')
    FIGURES['sol-11']['tex']=FIGURES['sol-11']['tex'].replace(r'\end{tikzpicture}',r'\geoSolution{\node[text=otGreenDark,above left,font=\scriptsize]at(-1,1.75){13 cm};}\end{tikzpicture}')
    cylindre('sol-12','4 cm','6 cm')
    cone('sol-13','40 cm','1,2 m')
    pave('sol-14','8 cm','6 cm','4 cm',r'\draw[geoTrait](0,2.6)--(3.15,5.2)--(5,2.6) (3.15,5.2)--(6.3,3.8);\draw[otMuted,dashed](1.3,3.8)--(3.15,5.2);\node[right]at(6.7,4.6){hauteur du toit : 3 cm};')
    cone('sol-15','6 cm','10 cm')
    pyramide('cours-solides','côté de base','$h$',r'\node[anchor=west,font=\scriptsize]at(5.8,2.5){Base polygonale};')

# ---------------------------------------------------------------------
# Chapitre 18 : scripts
# ---------------------------------------------------------------------
CONDITIONS={'x>9':'x > 9','x%2==0':'reste de x divisé par 2 = 0','contact==1':'touche le lutin Guide ?','3*x+5>0':'3 × x + 5 > 0','alea==6':'nombre aléatoire entre 1 et 6 = 6','n%2==0':'reste de n divisé par 2 = 0'}
EXPRESSIONS={'3*n+1':'3 × n + 1'}

def script_lines(cmds,depth=0):
    out=[]
    for c_ in cmds:
        op=c_[0];kind='calcul'
        if op=='set':txt=f'mettre {c_[1]} à {c_[2]}'
        elif op=='input':
            if c_[1]=='contact':continue
            txt=f'demander {c_[1]} et mémoriser la réponse';kind='entree'
        elif op=='add':txt=f'ajouter {c_[2]} à {c_[1]}'
        elif op=='mul':txt=f'mettre {c_[1]} à ({c_[1]} × {c_[2]})'
        elif op=='div':txt=f'mettre {c_[1]} à ({c_[1]} / {c_[2]})'
        elif op=='setexpr':txt=f'mettre {c_[1]} à ({EXPRESSIONS[c_[2]]})'
        elif op=='say':txt=f'dire {c_[1]}';kind='entree'
        elif op=='saytext':txt=f'dire « {c_[1]} »';kind='entree'
        elif op in ['move','movevar']:txt=f'avancer de {c_[1]}';kind='mouvement'
        elif op=='turn':txt=f'tourner de {c_[1]} degrés (sens antihoraire)';kind='mouvement'
        elif op=='repeat':
            out.append((depth,f'répéter {c_[1]} fois','controle'));out+=script_lines(c_[2],depth+1);out.append((depth,'fin de répéter','controle'));continue
        elif op=='if':
            out.append((depth,'si '+CONDITIONS[c_[1]]+' alors','controle'));out+=script_lines(c_[2],depth+1)
            if c_[3]:out.append((depth,'sinon','controle'));out+=script_lines(c_[3],depth+1)
            out.append((depth,'fin de si','controle'));continue
        else:raise ValueError(op)
        out.append((depth,txt,kind))
    return out

def scripts():
    for nom,cmds in SCRIPTS.items():
        if nom.startswith('defi'):continue
        event='quand la touche espace est pressée' if nom=='script-10' else 'quand le drapeau est cliqué'
        lines=[(0,event,'evenement')]+script_lines(cmds)
        if nom in ['script-07','script-08','script-11','script-13']:lines.insert(1,(0,'stylo baissé ; départ (0 ; 0), vers la droite','mouvement'))
        tex=pile(lines)
        if nom=='script-14':
            tex=r'\geoEnonce{'+tex+'}'+r'\geoSolution{'+pile([(0,'quand le drapeau est cliqué','evenement'),(0,'mettre s à 0','calcul'),(0,'répéter 4 fois','controle'),(1,'ajouter 3 à s','calcul'),(0,'fin de répéter','controle'),(0,'dire s','entree')])+'}'
        if nom=='script-15':tex=r'\geoEnonce{\node[draw=otMuted,rounded corners=1mm,inner sep=5mm]{Construire les blocs : entrée, condition, affichages.};}\geoSolution{'+tex+'}'
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

# ---------------------------------------------------------------------
# Défis, bilans et démonstrations
# ---------------------------------------------------------------------
def annexes():
    triangle('defi-pyth',9,12,right=True,labels={(0,1):'9 m',(0,2):'12 m',(1,2):reponse('15 m')})
    # D04 : carré d’aire 2 dans un carré 2 x 2.
    t=r'\draw[otNavy!40](0,0)grid[step=1.2](2.4,2.4);\filldraw[fill=otGreen!25,draw=otNavy,line width=.9pt](1.2,0)--(2.4,1.2)--(1.2,2.4)--(0,1.2)--cycle;\draw[otGreenDark,line width=1.1pt](1.2,0)--(2.4,1.2);'
    t+=r'\node[font=\scriptsize]at(1.2,1.2){aire 2};\node[font=\scriptsize,anchor=west]at(2.5,.45){$\sqrt2$ : diagonale};\node[font=\scriptsize,anchor=west]at(2.5,.0){d’un carré unité};\node[font=\scriptsize]at(.6,-.3){1};'
    dessin('defi-racine',t,'Le carré coloré occupe la moitié de quatre carrés unités : son aire vaut 2.')
    dessin('defi-litteral',r'\draw[geoTrait](0,0)rectangle(4,2.4);\draw[geoTrait](6,0)rectangle(11,1.6);\node at(2,1.2){A};\node at(8.5,.8){B};\node[below]at(2,0){$x+4$ cm};\node[below]at(8.5,0){$x+6$ cm};\node[left]at(0,1.2){3 cm};\node[left]at(6,.8){2 cm};')
    # D11 : tableau des parités.
    t='';w=.62;h=.4
    for j in range(6):t+=rf'\node[font=\scriptsize,text=otNavy]at({(j+.5)*w:.3f},{6*h+.22:.3f}){{{j+1}}};'
    for i in range(6):
        y=(5-i)*h;t+=rf'\node[font=\scriptsize,text=otOrange!80!black]at(-.25,{y+h/2:.3f}){{{i+1}}};'
        for j in range(6):
            p=(i+1)*(j+1)
            t+=rf'\draw[otNavy!60]({j*w:.3f},{y:.3f})rectangle++({w},{h});'
            if p%2==0:t+=r'\geoSolution{'+rf'\fill[otGreen!45]({j*w+.02:.3f},{y+.02:.3f})rectangle++({w-.04:.2f},{h-.04:.2f});'+'}'
            t+=r'\geoSolution{'+rf'\node[font=\tiny]at({(j+.5)*w:.3f},{y+h/2:.3f}){{{p}}};'+'}'
    t+=r'\geoSolution{\node[anchor=west,font=\scriptsize,text=otGreenDark,align=left]at(4,1.2){vert : produit pair\\27 issues sur 36};}'
    dessin('defi-des',t,'Tableau des produits : dé rouge en ligne, dé bleu en colonne.')
    # D12 : six triangles.
    P=echelle({'A':(1.6,4.2),'B':(0,0),'C':(6.4,0)},.8);A,B,C=P['A'],P['B'],P['C'];I=mil(B,C);J=mil(C,A);K=mil(A,B);G=((A[0]+B[0]+C[0])/3,(A[1]+B[1]+C[1])/3);P.update(I=I,J=J,K=K,G=G)
    t=seg(P,'A-B-C-A')+seg(P,'A-I','otNavy,line width=.6pt')+seg(P,'B-J','otNavy,line width=.6pt')+seg(P,'C-K','otNavy,line width=.6pt')
    t+=coche(B,I)+coche(I,C)+coche(C,J,2)+coche(J,A,2)+coche(A,K,3)+coche(K,B,3)+points(P,'ABCIJKG',{'A':'above','B':'below left','C':'below right','I':'below','J':'above right','K':'above left','G':'right'})
    sol=''
    for (p,q,lab) in [(B,I,'a'),(I,C,'a'),(C,J,'b'),(J,A,'b'),(A,K,'c'),(K,B,'c')]:
        sol+=rf'\node[font=\scriptsize,text=otGreenDark]at{c(((p[0]+q[0]+G[0])/3,(p[1]+q[1]+G[1])/3))}{{${lab}$}};'
    registre('defi-medianes',P,milieux=[('I','B','C'),('J','C','A'),('K','A','B')],alignes=[('A','G','I'),('B','G','J'),('C','G','K')])
    dessin('defi-medianes',t+r'\geoSolution{'+sol+'}','Au corrigé, les aires des six petits triangles sont notées $a$, $b$, $c$.')
    # D13 : le pont.
    k=.8;A=(0,0);B=(6*k,5*k);B2=(6*k,4*k);M=(3*k,2*k);N=(3*k,3*k)
    t=rf'\fill[otNavy!12](-.4,{2*k:.3f})rectangle({7*k:.3f},{3*k:.3f});\draw[otNavy!60](-.4,{2*k:.3f})--({7*k:.3f},{2*k:.3f}) (-.4,{3*k:.3f})--({7*k:.3f},{3*k:.3f});\node[font=\scriptsize,text=otNavy]at({5.6*k:.3f},{2.5*k:.3f}){{rivière}};\node[left,font=\scriptsize]at(-.4,{2*k:.3f}){{$y=2$}};\node[left,font=\scriptsize]at(-.4,{3*k:.3f}){{$y=3$}};'
    t+=points({'A':A,'B':B},'AB',{'A':'below left','B':'above right'})
    sol=rf'\draw[otGreenDark,dashed]{c(B)}--{c(B2)};\draw[otGreenDark,line width=.9pt]{c(A)}--{c(M)}--{c(N)}--{c(B)};\draw[otGreenDark,dashed]{c(M)}--{c(B2)};'+points({'M':M,'N':N,"B'":B2},['M','N',"B'"],{'M':'below right','N':'above left',"B'":'right'},'otGreenDark')
    GEOMETRIE['defi-pont']={'points':{'A':A,'B':B,"B'":B2,'M':M,'N':N},'translation':{'points':[N,B],'images':[M,B2],'deplacement':(0,-k)},'alignes':[('A','M',"B'")]}
    dessin('defi-pont',t+r'\geoSolution{'+sol+'}','Repère d’unité 1 km, réduit ; au corrigé, le trajet le plus court.')
    # D14 : Varignon et les aires.
    P=echelle({'A':(0,0),'B':(9,-1),'C':(10,5),'D':(1,6)},.5);A,B,C,D=P['A'],P['B'],P['C'],P['D'];I=mil(A,B);J=mil(B,C);K=mil(C,D);L=mil(D,A);P.update(I=I,J=J,K=K,L=L)
    t=r'\geoSolution{'+''.join(rf'\fill[otOrange!25]{c(a)}--{c(b)}--{c(d_)}--cycle;' for a,b,d_ in [(A,I,L),(B,J,I),(C,K,J),(D,L,K)])+'}'
    t+=seg(P,'A-B-C-D-A')+seg(P,'I-J-K-L-I','otNavy,line width=.9pt')+seg(P,'B-D','otNavy,dashed')+coche(A,I)+coche(I,B)+coche(B,J,2)+coche(J,C,2)+coche(C,K,3)+coche(K,D,3)+coche(D,L,4)+coche(L,A,4)
    t+=points(P,'ABCDIJKL',{'A':'left','B':'below','C':'right','D':'above','I':'below','J':'right','K':'above','L':'left'})
    registre('defi-varignon',P,milieux=[('I','A','B'),('J','B','C'),('K','C','D'),('L','D','A')],paralleles=[(('I','J'),('L','K')),(('I','L'),('J','K'))])
    dessin('defi-varignon',t,'Au corrigé, les quatre triangles des coins sont colorés.')
    # D16 : plus grand triangle du demi-cercle.
    r=2.0;O=(0,0);M=(r*cos(radians(125)),r*sin(radians(125)));H=(M[0],0);P={'A':(-r,0),'B':(r,0),'O':O,'M':M,'H':H}
    t=rf'\draw[geoTrait]({r},0)arc(0:180:{r});'+seg(P,'A-B')+seg(P,'A-M-B')+seg(P,'M-H','geoDonnee')+droit(M,H,P['B'])+seg(P,'O-M','otNavy,dashed')+points(P,'ABOMH',{'A':'left','B':'right','O':'below','M':'above left','H':'below'})+texte_seg(P['A'],P['B'],'10 cm',.3,-1,t=.78)
    t+=r'\geoSolution{'+rf'\draw[otGreenDark,line width=.9pt](-{r},0)--(0,{r})--({r},0);\draw[otGreenDark,dashed](0,0)--(0,{r});\fill[otGreenDark](0,{r})circle(1.4pt)node[above,font=\scriptsize]{{aire maximale : 25 cm$^2$}};'+'}'
    registre('defi-cercle',P,cercles=[('O',['A','B','M'])],perpendiculaires=[(('M','H'),('A','B')),(('M','A'),('M','B'))])
    dessin('defi-cercle',t,'La hauteur MH est au plus égale au rayon OM.')
    # D17 : pyramide de verre.
    pyramide('defi-pyramide','',r'21 m',r'\coordinate(M)at(2,0);\draw[geoDonnee](S)--(M) (H)--(M);\fill[otNavy](M)circle(1.2pt)node[below,font=\scriptsize]{$M$};\node[below,font=\scriptsize]at(3.3,-.35){côté : 35 m};','Modèle aux dimensions arrondies ; O, centre de la base, est le pied de la hauteur ; M est le milieu de $[AB]$.',nomH='O')
    dessin('defi-script',pile([(0,'quand le drapeau est cliqué','evenement')]+script_lines(SCRIPTS['defi-syracuse'])),'Une seule variable, n, est modifiée à chaque tour.')
    # Bilans.
    P=tri_cercle('bilan-a-geometrie',1.9,110,[('A','B','6 m',1),('A','C','8 m',1)],sol=r'\node[font=\scriptsize,text=otGreenDark]at(0,-.55){arroseur au milieu de $[BC]$, portée 5 m};')
    cone('bilan-a-cone','3 cm','12 cm')
    P=echelle({'A':(2,4.2),'B':(0,0),'C':(7.2,0)},.7);A,B,C=P['A'],P['B'],P['C'];I=mil(A,B);J=mil(A,C);K=mil(B,C);P.update(I=I,J=J,K=K)
    t=r'\geoSolution{'+rf'\fill[otGreen!25]{c(I)}--{c(B)}--{c(K)}--{c(J)}--cycle;'+'}'+seg(P,'A-B-C-A')+seg(P,'I-J','otNavy,line width=.8pt')+seg(P,'J-K','otNavy,dashed')+coche(A,I)+coche(I,B)+coche(A,J,2)+coche(J,C,2)+coche(B,K,3)+coche(K,C,3)
    t+=texte_seg(A,B,'7 cm',.3,1)+texte_seg(C,A,'9 cm',.3,1)+texte_seg(B,C,'12 cm',.28,-1)+points(P,'ABCIJK',{'A':'above','B':'below left','C':'below right','I':'left','J':'right','K':'below'})
    registre('bilan-b-milieux',P,milieux=[('I','A','B'),('J','A','C'),('K','B','C')],paralleles=[(('I','J'),('B','C'))])
    dessin('bilan-b-milieux',t,'Au corrigé, le parallélogramme IBKJ est coloré.')
    dessin('bilan-b-script',pile([(0,'quand le drapeau est cliqué','evenement'),(0,'mettre x à 2','calcul'),(0,'répéter 4 fois','controle'),(1,'mettre x à (x × 3)','calcul'),(0,'fin de répéter','controle'),(0,'dire x','entree')]),'La valeur initiale n’est pas un tour supplémentaire.')
    dessin('preuve-pythagore',r'\begin{scope}[scale=.6]\draw[geoTrait](0,0)rectangle(7,7);\coordinate(P)at(3,0);\coordinate(Q)at(7,3);\coordinate(R)at(4,7);\coordinate(S)at(0,4);\filldraw[fill=otGreen!20,draw=otNavy](P)--(Q)--(R)--(S)--cycle;\node[below]at(1.5,0){$a$};\node[below]at(5,0){$b$};\node[above,sloped]at(5,1.5){$c$};\end{scope}','Quatre triangles rectangles identiques entourent un carré central.')
    P=echelle({'A':(1.6,3.4),'B':(0,0),'C':(6,0)},.7);A,B,C=P['A'],P['B'],P['C'];I=mil(A,B);J=mil(A,C);K=add(J,vec(I,J));P.update(I=I,J=J,K=K)
    t=seg(P,'A-B-C-A')+seg(P,'I-K','otNavy,line width=.8pt')+seg(P,'C-K','otGreenDark,dashed')+seg(P,'A-K','otGreenDark,dashed')+coche(A,I)+coche(I,B)+coche(A,J,2)+coche(J,C,2)+coche(I,J,3)+coche(J,K,3)
    t+=points(P,'ABCIJK',{'A':'above','B':'below left','C':'below right','I':'left','J':'below','K':'above right'})
    registre('preuve-milieux',P,milieux=[('I','A','B'),('J','A','C'),('J','I','K')],paralleles=[(('I','K'),('B','C')),(('C','K'),('A','B'))])
    dessin('preuve-milieux',t,'K est l’image de I par le demi-tour de centre J ; AICK et IBCK sont des parallélogrammes.')

def write_all(root):
    nombres_modeles();statistiques_hasard();raisonnement();translations();milieux();pythagore();cercle();solides();scripts();annexes()
    root=Path(root);(root/'figures').mkdir(exist_ok=True)
    for nom,d in FIGURES.items():
        (root/'figures'/(nom+'.tex')).write_text(d['tex']+r'\par\vspace{1mm}{\fontsize{8}{10}\selectfont\color{otMuted}'+d['legende']+'}',encoding='utf8')
