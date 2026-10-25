"""Figures vectorielles liées aux données ; réponses de construction en vert."""
from math import ceil,floor,sqrt,sin,cos,tan,radians
from modele import FIGURES,figure,tableau
from donnees_figures import SCHEMAS
from donnees_scripts import SCRIPTS
from donnees_vecteurs import QUADRILLAGES

def dessin(nom,tex,legende='Schéma de principe sans échelle imposée ; seules les données écrites font foi.'):
    figure(nom,r'\begin{tikzpicture}[font=\small,line cap=round,line join=round]'+tex+r'\end{tikzpicture}',legende)

def num(a):
    """Nombre affiché à la française."""
    s=f'{a:g}'
    return s.replace('.','{,}')

def axes(xb,yb,xt=1,yt=1,xlabel='$x$',ylabel='$y$',ortho=False,sub=None,hauteur=4):
    xmin,xmax=xb;ymin,ymax=yb;sx=9/(xmax-xmin);sy=hauteur/(ymax-ymin)
    if ortho:sx=sy=min(sx,sy)
    tex=rf'\begin{{scope}}[x={sx}cm,y={sy}cm]'
    if sub:
        k=ceil(xmin/sub)
        while k*sub<=xmax+1e-9:
            tex+=rf'\draw[otRule!45,line width=.15pt]({k*sub},{ymin})--({k*sub},{ymax});';k+=1
    for j in range(ceil(xmin/xt),floor(xmax/xt)+1):
        a=j*xt;tex+=rf'\draw[otRule!65,line width=.2pt]({a},{ymin})--({a},{ymax});'
        if a:tex+=rf'\node[below,font=\tiny,fill=white,inner sep=.5pt]at({a},0){{${num(a)}$}};'
    for j in range(ceil(ymin/yt),floor(ymax/yt)+1):
        a=j*yt;tex+=rf'\draw[otRule!65,line width=.2pt]({xmin},{a})--({xmax},{a});'
        if a:tex+=rf'\node[left,font=\tiny,fill=white,inner sep=.5pt]at(0,{a}){{${num(a)}$}};'
    tex+=rf'\draw[otMuted,->]({xmin},0)--({xmax+.15/sx},0)node[right]{{{xlabel}}};\draw[otMuted,->](0,{ymin})--(0,{ymax+.2/sy})node[above]{{{ylabel}}};\node[below left,font=\tiny]at(0,0){{0}};'
    return tex

def graph(nom,curves,xb,yb,xt=1,yt=1,caption='',points=(),sol='',poly='',blank=False,xlabel='$x$',ylabel='$y$',ortho=False,sub=None,hauteur=4):
    tex=axes(xb,yb,xt,yt,xlabel,ylabel,ortho,sub,hauteur)+rf'\begin{{scope}}\clip({xb[0]},{yb[0]})rectangle({xb[1]},{yb[1]});'
    for i,(expr,lo,hi) in enumerate(curves):
        draw=rf'\draw[{"otNavy" if i==0 else "otGreenDark"},line width=1pt]plot[domain={lo}:{hi},samples=90](\x,{{{expr}}});'
        tex+=r'\geoSolution{'+draw+'}' if blank else draw
    tex+=poly
    for lab,x,y in points:tex+=rf'\fill[otNavy]({x},{y})circle(1.7pt)node[above right,geoLabel]{{$ {lab} $}};'
    dessin(nom,tex+r'\geoSolution{'+sol+r'}\end{scope}\end{scope}',caption+(' Repère orthonormé.' if ortho else ' Les axes sont gradués ; leurs échelles peuvent différer.'))

def schemas():
    # Les schémas de Pythagore respectent aussi les proportions des données.
    mesures={1:(4,3,5),2:(6,8,10),3:(5,12,13),4:(4,7,sqrt(65)),5:(9,12,15),
      6:(5,7,9),7:(1.4,4.8,5),10:(10,6,8)}
    for i,(ab,ac,bc) in mesures.items():
        cx=(ab*ab+ac*ac-bc*bc)/(2*ab);cy=sqrt(max(0,ac*ac-cx*cx))
        SCHEMAS[f'pyth-{i:02}']['points']={'A':(0,0),'B':(ab,0),'C':(cx,cy)}
    SCHEMAS['thales-07']['points']['M']=(5*3/8,0)
    SCHEMAS['thales-07']['points']['N']=(2*5/12,3*5/12)
    SCHEMAS['thales-13']['points']['M']=(5*2/3,0)
    SCHEMAS['thales-13']['points']['N']=(2*2/3,3*2/3)
    mesures_trigo={1:(6,8),2:(6,8),3:(6,8),4:(6,8),
      5:(12*cos(radians(30)),6),6:(9*cos(radians(40)),9*sin(radians(40))),
      7:(7,7*tan(radians(50))),8:(6,8),9:(12,5),10:(6,8),12:(10,.8),
      13:(18*cos(radians(65)),18*sin(radians(65))),15:(7,7*tan(radians(38)))}
    for i,(ab,ac) in mesures_trigo.items():
        SCHEMAS[f'trigo-{i:02}']['points']={'A':(0,0),'B':(ab,0),'C':(0,ac)}
    reponses={
      ('pyth-02','BC'):'10 cm',('pyth-03','AC'):'12 cm',
      ('pyth-04','BC'):r'$\sqrt{65}$ cm',('pyth-07','AC'):'4,8 m',
      ('trigo-06','AB'):r'$\approx6{,}9$ cm',('trigo-07','BC'):r'$\approx10{,}9$ cm',
      ('trigo-13','AB'):r'$\approx7{,}6$ m',('trigo-13','AC'):r'$\approx16{,}3$ m',
      ('trigo-15','AC'):r'$\approx5{,}5$ cm'}
    for nom,d in SCHEMAS.items():
        pts=d['points'];xs=[p[0] for p in pts.values()];ys=[p[1] for p in pts.values()]
        scale=min(1.,10/max(1,max(xs)-min(xs)),4/max(1,max(ys)-min(ys)))
        if max(max(xs)-min(xs),max(ys)-min(ys))<3:
            scale=min(6/max(.1,max(xs)-min(xs)),3.5/max(.1,max(ys)-min(ys)))
        tex=rf'\begin{{scope}}[x={scale}cm,y={scale}cm]'
        for a,p in pts.items():tex+=rf'\coordinate ({a})at({p[0]},{p[1]});'
        for a,b in d['segments']:tex+=rf'\draw[geoTrait]({a})--({b});'
        gx=sum(xs)/len(xs);gy=sum(ys)/len(ys)
        for a,b,t in d['labels']:
            if t=='?' and (nom,a+b) in reponses:
                t=r'\geoEnonce{?}\geoSolution{\textcolor{otGreenDark}{'+reponses[(nom,a+b)]+'}}'
            # Étiquette placée à l’extérieur du triangle, perpendiculairement au côté.
            (xa,ya),(xb,yb)=pts[a],pts[b];mx,my=(xa+xb)/2,(ya+yb)/2
            nx,ny=-(yb-ya),xb-xa;l=sqrt(nx*nx+ny*ny);nx,ny=nx/l,ny/l
            if nx*(mx-gx)+ny*(my-gy)<0:nx,ny=-nx,-ny
            if abs(nx)>=abs(ny):ancre='west' if nx>0 else 'east'
            else:ancre='south' if ny>0 else 'north'
            off=.08/scale
            tex+=rf'\node[anchor={ancre},inner sep=1.5pt,fill=white]at({mx+nx*off:.4f},{my+ny*off:.4f}){{{t}}};'
        mark=.18/scale
        for a in d['droits']:tex+=rf'\draw[otMuted]({a})++({mark},0)--++(0,{mark})--++(-{mark},0);'
        cy=sum(ys)/len(ys)
        for a,(x,y) in pts.items():tex+=rf'\fill[otNavy]({a})circle(1.4pt)node[{"above" if y>=cy else "below"},geoLabel]{{$ {a} $}};'
        solution=d['solution']
        # Aux exercices de réciproque, l’angle droit n’est codé qu’après la preuve.
        if nom in ['pyth-05','pyth-10']:
            sommet='A' if nom=='pyth-05' else 'C'
            autres=[k for k in 'ABC' if k!=sommet];v=pts[sommet];u1=pts[autres[0]];u2=pts[autres[1]]
            l1=sqrt((u1[0]-v[0])**2+(u1[1]-v[1])**2);l2=sqrt((u2[0]-v[0])**2+(u2[1]-v[1])**2)
            a=(v[0]+mark*(u1[0]-v[0])/l1,v[1]+mark*(u1[1]-v[1])/l1)
            b=(v[0]+mark*(u2[0]-v[0])/l2,v[1]+mark*(u2[1]-v[1])/l2)
            c=(a[0]+b[0]-v[0],a[1]+b[1]-v[1])
            solution+=rf'\draw[otGreenDark]({a[0]},{a[1]})--({c[0]},{c[1]})--({b[0]},{b[1]});'
        dessin(nom,tex+d['extra']+r'\geoSolution{'+solution+r'}\end{scope}')

def angle_droit(v,u1,u2,m=.25,col='otMuted'):
    l1=sqrt((u1[0]-v[0])**2+(u1[1]-v[1])**2);l2=sqrt((u2[0]-v[0])**2+(u2[1]-v[1])**2)
    a=(v[0]+m*(u1[0]-v[0])/l1,v[1]+m*(u1[1]-v[1])/l1);b=(v[0]+m*(u2[0]-v[0])/l2,v[1]+m*(u2[1]-v[1])/l2)
    c=(a[0]+b[0]-v[0],a[1]+b[1]-v[1])
    return rf'\draw[{col}]({a[0]:.4f},{a[1]:.4f})--({c[0]:.4f},{c[1]:.4f})--({b[0]:.4f},{b[1]:.4f});'

def codage(p,q,n=1,col='otMuted'):
    """Petits traits de codage d’égalité de longueur au milieu de [pq]."""
    mx,my=(p[0]+q[0])/2,(p[1]+q[1])/2;dx,dy=q[0]-p[0],q[1]-p[1];l=sqrt(dx*dx+dy*dy)
    nx,ny=-dy/l*.13,dx/l*.13;ux,uy=dx/l*.07,dy/l*.07;tex=''
    for k in range(n):
        o=(k-(n-1)/2)
        tex+=rf'\draw[{col},line width=.6pt]({mx+o*ux-nx:.4f},{my+o*uy-ny:.4f})--({mx+o*ux+nx:.4f},{my+o*uy+ny:.4f});'
    return tex

def pt(nom,p,pos='above',col='otNavy'):
    return rf'\fill[{col}]({p[0]:.4f},{p[1]:.4f})circle(1.5pt)node[{pos},geoLabel]{{$ {nom} $}};'

def arbre_denombrement(nom,niveau1,niveau2,feuilles):
    tex='';ys=[1.1,-1.1];ys2=[1.8,.4,-.4,-1.8]
    tex+=r'\node[inner sep=2pt](o)at(0,0){};'
    for i,l in enumerate(niveau1):tex+=rf'\node[inner sep=2pt](a{i})at(2,{ys[i]}){{$ {l} $}};\draw[otNavy](o.east)--(a{i}.west);'
    for k,l in enumerate(niveau2*2):
        i=k//2;tex+=rf'\node[inner sep=2pt](b{k})at(4.4,{ys2[k]}){{$ {l} $}};\draw[otNavy](a{i}.east)--(b{k}.west);'
        tex+=rf'\geoSolution{{\node[anchor=west,text=otGreenDark]at(5.2,{ys2[k]}){{{feuilles[k]}}};}}'
    dessin(nom,tex,'Arbre de dénombrement : chaque chemin est une issue ; les issues sont inscrites au corrigé.')

def pave(nom,L='8 cm',D='5 cm',H='3 cm',extra=''):
    tex=r'''\coordinate(A)at(0,0);\coordinate(B)at(5,0);\coordinate(C)at(6.3,1.2);\coordinate(D)at(1.3,1.2);
\coordinate(E)at(0,2.6);\coordinate(F)at(5,2.6);\coordinate(G)at(6.3,3.8);\coordinate(H)at(1.3,3.8);
\draw[geoTrait](A)--(B)--(C)--(G)--(H)--(E)--cycle (E)--(F)--(G) (B)--(F);
\draw[otMuted,dashed](A)--(D)--(C) (D)--(H);'''
    tex+=rf'\path(A)--node[below]{{{L}}}(B);\path(B)--node[below right]{{{D}}}(C);\path(A)--node[left]{{{H}}}(E);'
    dessin(nom,tex+extra,'Perspective cavalière ; les arêtes cachées sont en pointillés.')

def cylindre(nom,r='3 cm',h='10 cm',extra='',legende='Cylindre en perspective ; les dimensions de l’énoncé fixent le modèle.'):
    tex=r'''\draw[geoTrait](-1.5,0)--(-1.5,3) (1.5,0)--(1.5,3);
\draw[geoTrait](0,3)ellipse(1.5 and .42);\draw[geoTrait](-1.5,0)arc(180:360:1.5 and .42);
\draw[otMuted,dashed](-1.5,0)arc(180:0:1.5 and .42);'''
    tex+=rf'\draw[otMuted,<->](1.9,0)--node[right]{{{h}}}(1.9,3);'
    if r.startswith('base'):
        tex+=rf'\node at(0,.8){{{r}}};'
    elif r:
        tex+=rf'\draw[geoTrait](0,3)--node[above]{{{r}}}(1.5,3);'
    dessin(nom,tex+extra,legende)

def cone(nom,r='4 cm',h='9 cm',cut=False):
    tex=r'\draw[geoTrait](-2,0)--(0,3.5)--(2,0);\draw[geoTrait](-2,0)arc(180:360:2 and .5);\draw[otMuted,dashed](-2,0)arc(180:0:2 and .5) (0,0)--(0,3.5);'
    tex+=rf'\draw[otMuted,<->](2.5,0)--node[right]{{{h}}}(2.5,3.5);\draw[geoTrait](0,0)--node[below]{{{r}}}(2,0);'
    if cut:tex+=r'\draw[otMuted,dashed](-1,1.75)--(1,1.75);\node[left]at(-1.2,1.8){mi-hauteur};\geoSolution{\draw[otGreenDark,line width=.9pt](0,1.75)ellipse(1 and .25);\node[below,text=otGreenDark,font=\scriptsize,fill=white,inner sep=1pt]at(0,1.42){rayon 3 cm};}'
    dessin(nom,tex,'Cône en perspective ; la hauteur est perpendiculaire à la base.')

def sphere(nom,r='3 cm',inner=False,section=None):
    tex=r'\draw[geoTrait](0,0)circle(2);\draw[otMuted,dashed](0,0)ellipse(2 and .55);\fill[otNavy](0,0)circle(1.4pt)node[below left]{$O$};'
    if inner:tex+=r'\draw[otGreenDark,dashed](0,0)circle(.8);\node[above,fill=white,inner sep=1pt]at(1,.8){cavité : rayon 2 cm};'
    if section:
        R,d=section; rr=(R*R-d*d)**.5;yy=2*d/R;xx=2*rr/R
        ld=(r'\geoEnonce{?}\geoSolution{\textcolor{otGreenDark}{6 cm}}' if nom=='defi-section' else f'{d} cm')
        lr=r'\geoEnonce{?}\geoSolution{\textcolor{otGreenDark}{'+f'{rr:g} cm'+'}}'
        tex+=rf'\draw[otGreenDark](0,{yy})ellipse({xx} and .28);\draw[geoTrait](0,0)--(0,{yy})node[midway,left,fill=white,inner sep=.5pt]{{{ld}}}--({xx},{yy})node[midway,above,fill=white,inner sep=.5pt]{{{lr}}}--cycle;\node[above left]at(0,{yy}){{$H$}};\node[right]at({xx},{yy}){{$M$}};\node[below right]at({xx/2},{yy/2}){{{R} cm}};'
        tex+=rf'\draw[otMuted](0,{yy-.15})--(.15,{yy-.15})--(.15,{yy});'
    else:tex+=rf'\draw[geoTrait](0,0)--node[above]{{{r}}}(2,0);'
    dessin(nom,tex,'Sphère en perspective ; le cercle de section est représenté par une ellipse.')

def cond(t):
    for a,b in [(' and ',' et '),(' or ',' ou '),('>=',r'$\ge$'),('<=',r'$\le$'),('==',' = '),('>',' > '),('<',' < '),('%',' mod ')]:
        t=t.replace(a,b)
    return t
def script_lines(cmds,depth=0):
    out=[]
    for c in cmds:
        op=c[0];kind='calcul'
        if op=='set':txt=f'mettre {c[1]} à {c[2]}'
        elif op=='input':txt=f'demander un nombre ; mettre {c[1]} à réponse';kind='entree'
        elif op=='add':txt=f'ajouter {c[2]} à {c[1]}'
        elif op=='mul':txt=f'mettre {c[1]} à ({c[1]} × {c[2]})'
        elif op=='addvar':txt=f'ajouter {c[2]} à {c[1]}'
        elif op=='subvar':txt=f'mettre {c[1]} à ({c[1]} − {c[2]})'
        elif op=='say':txt=f'dire {c[1]}';kind='entree'
        elif op=='saytext':txt=f'dire « {c[1]} »';kind='entree'
        elif op=='move':txt=f'avancer de {c[1]}';kind='mouvement'
        elif op=='turn':txt=f'tourner de {c[1]} degrés (sens antihoraire)';kind='mouvement'
        elif op in ['repeat','until']:
            out.append((depth,f'répéter {c[1]} fois' if op=='repeat' else 'répéter jusqu’à '+cond(c[1]),'controle'));out+=script_lines(c[2],depth+1);out.append((depth,'fin de répéter','controle'));continue
        elif op=='if':
            out.append((depth,'si '+cond(c[1])+' alors','controle'));out+=script_lines(c[2],depth+1)
            if c[3]:out.append((depth,'sinon','controle'));out+=script_lines(c[3],depth+1)
            out.append((depth,'fin de si','controle'));continue
        else:raise ValueError(op)
        out.append((depth,txt,kind))
    return out
def pile(lines,x=0,width=7.6):
    tex='';colors={'calcul':'otOrange!25','controle':'otOrange!38','entree':'otNavy!14','mouvement':'otNavy!24','evenement':'otGreen!28','bloc':'otRed!22'}
    for i,(dep,txt,kind) in enumerate(lines):
        txt=txt.replace('×',r'$\times$').replace('−',r'$-$')
        tex+=rf'\node[anchor=north west,rounded corners=1mm,draw=white,fill={colors[kind]},inner xsep=2mm,inner ysep=1.3mm,font=\scriptsize,text width={width-dep*.3}cm]at({x+dep*.3},{-i*.55}){{{txt}}};'
    return tex

def scripts():
    for nom,cmds in SCRIPTS.items():
        dessin(nom,pile([(0,'quand le drapeau est cliqué','evenement')]+script_lines(cmds)),'Blocs de type Scratch ; indentation et lignes « fin » délimitent les blocs imbriqués.')
    dessin('script-carres',pile([(0,'définir carré(c)','bloc'),(0,'répéter 4 fois','controle'),(1,'avancer de c','mouvement'),(1,'tourner de 90 degrés','mouvement'),(0,'fin de répéter','controle')],width=4.8)+pile([(0,'quand le drapeau est cliqué','evenement'),(0,'stylo baissé','mouvement'),(0,'répéter 3 fois','controle'),(1,'carré(30)','bloc'),(1,'relever le stylo','mouvement'),(1,'avancer de 40','mouvement'),(1,'baisser le stylo','mouvement'),(0,'fin de répéter','controle')],x=5.4,width=4.8),'À gauche, le bloc personnalisé ; à droite, le script qui l’appelle.')
    def trou(v):return r'\geoEnonce{\dots}\geoSolution{\textcolor{otGreenDark}{'+str(v)+'}}'
    dessin('script-simulation',pile([(0,'quand le drapeau est cliqué','evenement'),(0,'mettre succès à '+trou(0),'calcul'),(0,'répéter 600 fois','controle'),(1,'mettre dé à nombre aléatoire entre 1 et 6','calcul'),(1,'si dé = 6 alors','controle'),(2,'ajouter '+trou(1)+' à succès','calcul'),(1,'fin de si','controle'),(0,'fin de répéter','controle'),(0,'dire succès / '+trou(600),'entree')]),'Compléter les trois valeurs manquantes ; les valeurs sont inscrites en vert au corrigé.')
    dessin('script-deux-des',pile([(0,'quand le drapeau est cliqué','evenement'),(0,'mettre succès à 0','calcul'),(0,'répéter 1000 fois','controle'),(1,'mettre d1 à nombre aléatoire entre 1 et 6','calcul'),(1,'mettre d2 à nombre aléatoire entre 1 et 6','calcul'),(1,'si d1 = 6 ou d2 = 6 alors','controle'),(2,'ajouter 1 à succès','calcul'),(1,'fin de si','controle'),(0,'fin de répéter','controle'),(0,'dire succès / 1000','entree')]),'Deux variables d1 et d2 pour deux dés indépendants ; une condition composée par « ou ».')
    dessin('script-polygones',pile([(0,'définir polygone(n, c)','bloc'),(0,'répéter n fois','controle'),(1,'avancer de c','mouvement'),(1,'tourner de (360 / n) degrés','mouvement'),(0,'fin de répéter','controle')],width=4.8)+pile([(0,'quand le drapeau est cliqué','evenement'),(0,'stylo baissé','mouvement'),(0,'mettre n à 3','calcul'),(0,'répéter jusqu’à n > 6','controle'),(1,'polygone(n, 30)','bloc'),(1,'ajouter 1 à n','calcul'),(0,'fin de répéter','controle')],x=5.4,width=4.8),'À gauche, le bloc personnalisé et ses deux paramètres ; à droite, le programme principal.')
    dessin('brevet-B-script',pile([(0,'quand le drapeau est cliqué','evenement'),(0,'mettre c à 10','calcul'),(0,'répéter jusqu’à c > 25','controle'),(1,'carré(c)','bloc'),(1,'relever le stylo','mouvement'),(1,'avancer de c + 5','mouvement'),(1,'baisser le stylo','mouvement'),(1,'ajouter 5 à c','calcul'),(0,'fin de répéter','controle'),(0,'dire c','entree')]),'Le bloc carré(c) revient à son point de départ avec la même orientation.')

def vecteurs():
    u=.6
    for nom,d in QUADRILLAGES.items():
        x0,x1,y0,y1=d['cadre'];P=dict(d['points']);P.update(d.get('solution_points',{}))
        tex=rf'\begin{{scope}}[x={u}cm,y={u}cm]\draw[otRule,line width=.25pt]({x0},{y0})grid({x1},{y1});'
        for (a,b,lab) in d.get('droites',[]):
            tex+=rf'\draw[otMuted,line width=.8pt]({a[0]},{a[1]})--({b[0]},{b[1]})node[above]{{$({lab})$}};'
        for poly in d.get('polygones',[]):
            tex+=r'\draw[geoTrait]'+'--'.join(f'({P[p][0]},{P[p][1]})' for p in poly)+'--cycle;'
        for a,b in d.get('segments',[]):
            tex+=rf'\draw[geoTrait]({P[a][0]},{P[a][1]})--({P[b][0]},{P[b][1]});'
        for a,b in d.get('fleches',[]):
            tex+=rf'\draw[geoVecteur]({P[a][0]},{P[a][1]})--({P[b][0]},{P[b][1]});'
        for a,b,lab in d.get('vecteurs_libres',[]):
            tex+=rf'\draw[geoVecteur]({a[0]},{a[1]})--node[above left,geoLabel]{{$\vec {lab}$}}({b[0]},{b[1]});'
        # Étiquette de chaque point placée à l’opposé des traits qui en partent.
        voisins={p:[] for p in P}
        aretes=list(d.get('segments',[]))+list(d.get('fleches',[]))+list(d.get('solution_fleches',[]))
        for poly in d.get('polygones',[])+d.get('solution_polygones',[]):
            aretes+=[(poly[k],poly[(k+1)%len(poly)]) for k in range(len(poly))]
        for a,b in aretes:
            voisins[a].append(P[b]);voisins[b].append(P[a])
        def place(p):
            if not voisins[p]:return 'below left'
            vx=vy=0.
            for q in voisins[p]:
                dx,dy=q[0]-P[p][0],q[1]-P[p][1];l=sqrt(dx*dx+dy*dy);vx-=dx/l;vy-=dy/l
            if abs(vx)<1e-9 and abs(vy)<1e-9:vx,vy=-1.,-1.
            from math import atan2,degrees
            a=degrees(atan2(vy,vx))%360
            return ['right','above right','above','above left','left','below left','below','below right'][int(((a+22.5)%360)//45)]
        for p,c in d['points'].items():
            tex+=rf'\fill[otNavy]({c[0]},{c[1]})circle(1.6pt)node[{place(p)},geoLabel]{{$ {p} $}};'
        sol=''
        for poly in d.get('solution_polygones',[]):
            sol+=r'\draw[geoReponse]'+'--'.join(f'({P[p][0]},{P[p][1]})' for p in poly)+'--cycle;'
        for a,b in d.get('solution_fleches',[]):
            sol+=rf'\draw[otGreenDark,line width=.9pt,-{{Stealth[length=1.8mm]}}]({P[a][0]},{P[a][1]})--({P[b][0]},{P[b][1]});'
        for p,c in d.get('solution_points',{}).items():
            nom_p=p.replace("''",r"^{\prime\prime}").replace("'",r"^{\prime}")
            sol+=rf'\fill[otGreenDark]({c[0]},{c[1]})circle(1.6pt)node[{place(p)},geoLabel]{{$ {nom_p} $}};'
        construit=any(d.get(k) for k in ('solution_points','solution_fleches','solution_polygones'))
        leg='Quadrillage'+(' : '+d['unite'] if 'unite' in d else '')+(' ; la construction cherchée est ajoutée en vert au corrigé.' if construit else ' ; les points sont placés sur les nœuds.')
        dessin(nom,tex+r'\geoSolution{'+sol+r'}\end{scope}',leg)
    tex=''
    for i in range(6):
        tex+=rf'\draw[geoTrait,fill=otNavyTint]({i*1.6},0)--++(.9,0)--++(-.3,.9)--++(-.3,-.35)--cycle;\node[below,font=\scriptsize]at({i*1.6+.45},-.05){{{i+1}}};'
    tex+=r'\draw[geoVecteur](0,1.25)--node[above]{$\vec u$ : 4 cm}(1.6,1.25);'
    dessin('vect-frise',tex,'Six motifs d’une frise ; chaque motif est l’image du précédent par la translation de vecteur $\\vec u$.')

def statistiques():
    def axe(a,b,pas,lab,sx,etiq=None):
        t=rf'\draw[otMuted,->]({a*sx},0)--({b*sx+.4},0)node[right,font=\scriptsize]{{{lab}}};'
        k=a
        while k<=b:
            t+=rf'\draw[otMuted]({k*sx},.07)--({k*sx},-.07);'
            if etiq is None or k%etiq==0:t+=rf'\node[below,font=\tiny]at({k*sx},-.07){{{k}}};'
            k+=pas
        return t
    def boite(v,y,sx,col='geoTrait',h=.32):
        m,q1,me,q3,M=v
        return (rf'\draw[{col}]({m*sx},{y})--({q1*sx},{y}) ({q3*sx},{y})--({M*sx},{y});'
                rf'\draw[{col}]({m*sx},{y-h/2})--({m*sx},{y+h/2}) ({M*sx},{y-h/2})--({M*sx},{y+h/2});'
                rf'\draw[{col}]({q1*sx},{y-h})rectangle({q3*sx},{y+h});\draw[{col},line width=1.4pt]({me*sx},{y-h})--({me*sx},{y+h});')
    sx=.42
    dessin('boite-lecture',axe(0,20,1,'min',sx,2)+boite((4,8,11,14,19),.7,sx),'Boîte à moustaches ; l’axe est gradué de 1 en 1 minute.')
    sx=.4
    dessin('boite-construire',axe(0,22,1,'',sx,2)+r'\geoSolution{'+boite((3,6,10,15,20),.7,sx,'geoReponse')+'}','Axe gradué à compléter ; la boîte cherchée est ajoutée en vert au corrigé.')
    sx=.21
    tex=axe(0,42,1,'min',sx,5)+boite((5,10,15,22,40),1.75,sx)+boite((8,12,14,17,25),.75,sx)
    tex+=r'\node[left]at(0,1.75){A};\node[left]at(0,.75){B};'
    dessin('boites-comparer',tex,'Durées de trajet, en minutes, dans les collèges A et B.')
    tex=axes((0,6),(0,10),1,1,'livres','effectif')
    for v,h in zip(range(1,6),[3,7,9,6,5]):tex+=rf'\fill[otNavy!55]({v-.18},0)rectangle({v+.18},{h});'
    dessin('stat-barres',tex+r'\end{scope}','Nombre de livres lus par élève ; la hauteur de chaque barre est un effectif.')
    dessin('stat-axe-tronque',r'\draw[otMuted,->](0,0)--(0,3.5)node[above]{inscriptions};\draw[otMuted](0,0)--(5,0);\node[left]at(0,0){78};\node[left]at(0,1){80};\node[left]at(0,3){84};\draw[geoTrait,fill=otNavyTint](1,0)rectangle(2,1)(3,0)rectangle(4,3);\node[below]at(1.5,0){A};\node[below]at(3.5,0){B};','L’origine de l’axe vertical est 78 : comparer les nombres, pas les seules hauteurs visibles.')

def probabilites():
    arbre_denombrement('proba-pieces',['P','F'],['P','F'],['PP','PF','FP','FF'])
    figure('proba-des',tableau(['Dé 1 / Dé 2']+[str(n) for n in range(1,7)],[[str(i)]+[str(i+j) for j in range(1,7)] for i in range(1,7)]),'Chaque case représente un couple équiprobable et indique sa somme.')
    noms=['R_1','R_2','R_3','B_1','B_2']
    def case(a,b):
        t=a[0]+b[0]
        return r'\geoEnonce{'+t+r'}\geoSolution{\textcolor{otGreenDark}{\textbf{'+t+'}}}' if t in ('RR','BB') else t
    figure('proba-tableau-boules',tableau(['1\\textsuperscript{er} / 2\\textsuperscript{e}']+[f'${n}$' for n in noms],[[f'${a}$']+[case(a,b) for b in noms] for a in noms]),'Vingt-cinq couples équiprobables ; au corrigé, les couples de même couleur sont en vert.')
    figure('brevet-A-tableau',tableau(['1\\textsuperscript{er} / 2\\textsuperscript{e}']+[f'${n}$' for n in ['R_1','R_2','R_3','B']],[[f'${a}$']+[f'${a}{b}$' for b in ['R_1','R_2','R_3','B']] for a in ['R_1','R_2','R_3','B']]),'Seize couples équiprobables : les trois boules rouges sont numérotées.')
    def gagnant(s,c):
        t=f'{s}-{c}'
        return r'\geoEnonce{'+t+r'}\geoSolution{\textcolor{otGreenDark}{\textbf{'+t+'}}}' if (s[0]=='A' and c=='rouge') or (s=='B' and c=='bleue') else t
    figure('brevet-B-tableau',tableau(['Secteur / boule','rouge','bleue'],[[s]+[gagnant(s,c) for c in ['rouge','bleue']] for s in ['A1','A2','A3','B']]),'Les trois secteurs A sont numérotés : huit issues équiprobables. Au corrigé, les issues gagnantes sont en vert.')

def geometrie_plane():
    s=.42
    B,C,A,O=(0,0),(10,0),(3.6,4.8),(5,0)
    tex=rf'\begin{{scope}}[scale={s}]\draw[geoTrait]({B[0]},{B[1]})--({C[0]},{C[1]})--({A[0]},{A[1]})--cycle;'+angle_droit(A,B,C,.6)+codage(B,O)+codage(O,C)
    tex+=pt('B',B,'below')+pt('C',C,'below')+pt('A',A,'above')+pt('O',O,'below=2pt')+r'\node[below=3mm]at(5,0){$BC=10$ cm};'
    tex+=r'\geoSolution{\draw[geoReponse](5,0)circle(5);\draw[geoAide](5,0)--(3.6,4.8);}\end{scope}'
    dessin('cercle-circonscrit',tex,'Le cercle circonscrit est tracé en vert au corrigé.')
    A,B,C=(1,4),(0,0),(9,0);I=(.5,2);J=(5,2)
    tex=rf'\begin{{scope}}[scale=.55]\draw[geoTrait](1,4)--(0,0)--(9,0)--cycle;\draw[geoTrait](.5,2)--(5,2);'+codage(A,I)+codage(I,B)+codage(A,J,2)+codage(J,C,2)
    tex+=pt('A',A)+pt('B',B,'below')+pt('C',C,'below')+pt('I',I,'left')+pt('J',J,'right')+r'\node[below]at(4.5,0){9 cm};\geoSolution{\draw[geoReponse](.5,2)--node[above,text=otGreenDark]{4,5 cm}(5,2);}\end{scope}'
    dessin('milieux-parallele',tex,'Les traits identiques codent des longueurs égales.')
    A,B,C=(2,5),(0,0),(8,0);I=(1,2.5);J=(5,2.5)
    tex=rf'\begin{{scope}}[scale=.55]\draw[geoTrait](2,5)--(0,0)--(8,0)--cycle;\draw[geoTrait](-.5,2.5)--(7,2.5);'+codage(A,I)+codage(I,B)
    tex+=pt('A',A)+pt('B',B,'below')+pt('C',C,'below')+pt('I',I,'left')+pt('J',J,'above right')+r'\node[right]at(6.6,3.6){$AC=7{,}4$ cm};\node[right,font=\scriptsize]at(7,2.5){parallèle à (BC)};'
    tex+=r'\geoSolution{'+codage(A,J,2,'otGreenDark')+codage(J,C,2,'otGreenDark')+r'}\end{scope}'
    dessin('milieux-milieu',tex,'Au corrigé, le codage vert indique que J est le milieu de [AC].')
    s=.3;A=(-6.5+25/13,60/13)
    tex=rf'\begin{{scope}}[scale={s}]\draw[geoTrait](0,0)circle(6.5);\draw[geoTrait](-6.5,0)--(6.5,0)--({A[0]:.4f},{A[1]:.4f})--cycle;'
    tex+=pt('B',(-6.5,0),'left')+pt('C',(6.5,0),'right')+pt('A',A,'above')+pt('O',(0,0),'below=2pt')+rf'\path(-6.5,0)--node[right=1pt,fill=white,inner sep=1pt]{{5 cm}}({A[0]:.4f},{A[1]:.4f});'
    tex+=r'\geoSolution{'+angle_droit(A,(-6.5,0),(6.5,0),.9,'otGreenDark')+rf'\path({A[0]:.4f},{A[1]:.4f})--node[above right,text=otGreenDark]{{12 cm}}(6.5,0);'+r'}\end{scope}'
    dessin('demi-cercle',tex,'Cercle de centre O et de rayon 6,5 cm ; l’angle droit est codé au corrigé.')
    r=2.5;Bq=(r*cos(radians(60)),r*sin(radians(60)))
    tex=rf'\draw[geoTrait](0,0)circle({r});\draw[geoTrait]({r},0)--(-{r},0) ({Bq[0]:.4f},{Bq[1]:.4f})--({-Bq[0]:.4f},{-Bq[1]:.4f});'
    tex+=pt('A',(r,0),'right')+pt('C',(-r,0),'left')+pt('B',Bq,'above')+pt('D',(-Bq[0],-Bq[1]),'below')+pt('O',(0,0),'below right')
    tex+=r'\geoSolution{'+rf'\draw[geoReponse]({r},0)--({Bq[0]:.4f},{Bq[1]:.4f})--(-{r},0)--({-Bq[0]:.4f},{-Bq[1]:.4f})--cycle;'+angle_droit((r,0),Bq,(-Bq[0],-Bq[1]),.3,'otGreenDark')+angle_droit(Bq,(r,0),(-r,0),.3,'otGreenDark')+'}'
    dessin('rectangle-compas',tex,'Deux diamètres d’un même cercle ; le rectangle obtenu est tracé en vert au corrigé.')
    A,B,C,D=(0,0),(7,1),(8,5),(2,6)
    mil=lambda P,Q:((P[0]+Q[0])/2,(P[1]+Q[1])/2);I,J,K,L=mil(A,B),mil(B,C),mil(C,D),mil(D,A)
    tex=r'\begin{scope}[scale=.55]\draw[geoTrait](0,0)--(7,1)--(8,5)--(2,6)--cycle;\draw[geoAide](0,0)--(8,5);'
    for (P,Q,n) in [(A,I,1),(I,B,1),(B,J,2),(J,C,2),(C,K,3),(K,D,3),(D,L,4),(L,A,4)]:tex+=codage(P,Q,n)
    tex+=pt('A',A,'below left')+pt('B',B,'below right')+pt('C',C,'above right')+pt('D',D,'above left')+pt('I',I,'below')+pt('J',J,'right')+pt('K',K,'above')+pt('L',L,'left')
    tex+=r'\geoSolution{\draw[geoReponse]'+f'({I[0]},{I[1]})--({J[0]},{J[1]})--({K[0]},{K[1]})--({L[0]},{L[1]})--cycle;'+r'}\end{scope}'
    dessin('varignon',tex,'Quadrilatère quelconque et milieux de ses côtés ; la diagonale [AC] est en pointillés.')
    A,B,C,M,N=(0,0),(10,0),(4,6),(6,0),(2.4,3.6)
    tex=r'\begin{scope}[scale=.45]\draw[geoTrait](0,0)--(10,0)--(4,6)--cycle;\draw[geoTrait](6,0)--(2.4,3.6);\draw[otMuted,dashed](6,0)--(4,6) (2.4,3.6)--(10,0);'
    tex+=pt('A',A,'below left')+pt('B',B,'below right')+pt('C',C,'above')+pt('M',M,'below')+pt('N',N,'left')
    tex+=r'\geoSolution{\fill[otGreen,opacity=.25](6,0)--(2.4,3.6)--(10,0)--cycle;\fill[otNavy,opacity=.15](6,0)--(2.4,3.6)--(4,6)--cycle;}\end{scope}'
    dessin('thales-aires',tex,'(MN) est parallèle à (BC). Au corrigé, les triangles MNB et MNC sont colorés.')
    tex=r'\begin{scope}[scale=.42]\draw[otMuted](-.8,0)--(13,0);\draw[geoTrait](2,0)--(2,1.5) (12,0)--(12,9);\draw[otOrange!80!black,line width=.7pt](0,0)--(12,9);'
    tex+=pt('S',(0,0),'below')+r'\node[below]at(2,0){$p$};\node[below]at(12,0){$P$};\node[left]at(2,1.6){$t$};\node[left]at(12,9){$T$};'
    tex+=r'\draw[otMuted,<->](0,-1.3)--node[below,font=\scriptsize]{2 m}(2,-1.3);\draw[otMuted,<->](0,-2.4)--node[below,font=\scriptsize]{12 m}(12,-2.4);\node[right,font=\scriptsize]at(2,.8){1,5 m};\node[right,font=\scriptsize]at(12,4.5){arbre};'
    tex+=r'\geoSolution{\node[right,text=otGreenDark,font=\scriptsize]at(12,6){9 m};}\end{scope}'
    dessin('thales-ombre',tex,'Le rayon de soleil passe par S, par le sommet t du bâton et par le sommet T de l’arbre.')
    dessin('thales-milieux',r'\draw[geoTrait](0,0)node[left]{$A$}--(6,0)node[right]{$B$}--(2,4)node[above]{$C$}--cycle;\draw[geoTrait](3,0)node[below]{$M$}--(1,2)node[left]{$N$};\node[above right]at(2,1){7,4 m};'+codage((0,0),(3,0))+codage((3,0),(6,0))+codage((0,0),(1,2),2)+codage((1,2),(2,4),2))
    tex=axes((0,11),(0,8.5),1,1,ortho=True)
    tex+=r'\draw[geoTrait](0,0)--(11,8.25);\draw[otMuted,dashed](4,0)--(4,3) (10,0)--(10,7.5);'
    tex+=pt('A',(4,3),'above left')+pt('B',(10,7.5),'above left')+pt('H',(4,0),'below right')+pt('K',(10,0),'below right')
    dessin('thales-repere',tex+r'\end{scope}','Repère orthonormé ; O, A et B sont alignés.')
    tex=r'\begin{scope}[scale=.5]\draw[geoTrait](0,0)--(10,0)--(8,5)--(2,5)--cycle;\draw[geoTrait](0,0)--(8,5) (10,0)--(2,5);'
    tex+=pt('D',(0,0),'below left')+pt('C',(10,0),'below right')+pt('B',(8,5),'above right')+pt('A',(2,5),'above left')+pt('O',(5,3.125),'below')
    tex+=r'\node[above]at(5,5){6 cm};\node[below]at(5,0){10 cm};\end{scope}'
    dessin('defi-trapeze',tex,'Trapèze ABCD de bases [AB] et [CD] ; les diagonales se coupent en O.')
    tex=r'\begin{scope}[scale=.55]\draw[geoTrait](0,0)--(6,0)--(2,4)--cycle;'
    tex+=pt('A',(0,0),'below left')+pt('B',(6,0),'below right')+pt('C',(2,4),'above left')
    tex+=r'\geoSolution{\draw[geoAide](6,0)--(8,4)--(2,4);\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm]}](0,0)--(8,4);'+pt('D',(8,4),'above right','otGreenDark')+pt('I',(4,2),'below right','otGreenDark')+r'}\end{scope}'
    dessin('defi-vecteurs',tex,'Le point D et le milieu I de [BC] sont placés au corrigé.')

def espace():
    pave('espace-01');cylindre('espace-02');cylindre('brevet-B-cylindre','4 cm','20 cm')
    dessin('espace-03',r'\draw[geoTrait](-2,0)--(1,-.5)--(2,1)--(0,4)--cycle (0,4)--(1,-.5);\draw[otMuted,dashed](-2,0)--(-1,1.5)--(2,1) (0,4)--(-1,1.5) (0,4)--(0,.5);\draw[otMuted,->](-1.75,3.05)--(-.06,2.35);\node[left,font=\small]at(-1.75,3.05){hauteur 9 cm};\node[below]at(-.6,-.3){6 cm};','Pyramide à base carrée ; la hauteur est perpendiculaire à la base.')
    cone('espace-04');sphere('espace-05');sphere('espace-cavite','5 cm',inner=True);sphere('espace-section-sphere',section=(5,3))
    pave('espace-section-pave',H='6 cm',extra=r'\draw[otMuted,dashed](0,.87)--(5,.87)--(6.3,2.07);\node[left]at(0,.5){2 cm};\geoSolution{\draw[otGreenDark,fill=otGreenTint,fill opacity=.45](0,.87)--(5,.87)--(6.3,2.07)--(1.3,2.07)--cycle;}')
    cylindre('espace-reservoir','1 m','2 m',r'\draw[otGreenDark](-1.5,3)arc(180:0:1.5);\node[above]at(0,4.5){demi-boule};')
    cone('espace-cone-coupe','6 cm','12 cm',True)
    pave('synthese-bassin','4 m','2,5 m','0,8 m',r'\draw[otGreenDark](0,1.95)--(5,1.95)--(6.3,3.15)--(1.3,3.15)--cycle;')
    tex=r'\draw[geoTrait](0,0)circle(2);\draw[otMuted,dashed](0,0)ellipse(2 and .55);'
    tex+=pt('O',(0,0),'below=2pt')+pt('A',(-2,0),'left')+pt('B',(2,0),'right')+pt('C',(1.2,1.6),'above right')+pt('M',(-.6,-.8),'left')+pt('N',(2.4,1.8),'right')
    tex+=r'\draw[otMuted](0,0)--(1.2,1.6);\geoSolution{\draw[geoReponse](-2,0)--(2,0);\draw[otGreenDark](0,0)ellipse(2 and .55);}'
    dessin('espace-sphere-vocab',tex,'Sphère de centre O et de rayon 4 cm, en perspective ; les distances au centre sont données dans l’énoncé.')
    tex=r'''\coordinate(A)at(0,0);\coordinate(B)at(3,0);\coordinate(C)at(3.9,.9);\coordinate(D)at(.9,.9);
\coordinate(E)at(0,3);\coordinate(F)at(3,3);\coordinate(G)at(3.9,3.9);\coordinate(H)at(.9,3.9);
\draw[otMuted](A)--(B)--(C)--(G)--(H)--(E)--cycle (E)--(F)--(G) (B)--(F);
\draw[otMuted,dashed](A)--(D)--(C) (D)--(H);
\draw[geoTrait,line width=1pt](E)--(A)--(B)--(C) (E)--(B) (E)--(C);\draw[otNavy,dashed,line width=.9pt](E)--(D) (A)--(D)--(C);'''
    for p,pos in [('A','below left'),('B','below right'),('C','right'),('D','above left'),('E','left'),('F','above'),('G','above right'),('H','above')]:
        tex+=rf'\node[{pos},font=\scriptsize]at({p}){{${p}$}};'
    tex+=r'\path(A)--node[below]{6 cm}(B);'
    dessin('espace-pyramide-cube',tex,'Cube en perspective cavalière ; la pyramide EABCD est tracée en bleu.')
    tex=r'\begin{scope}[xshift=-2.6cm]\draw[geoTrait](-1.5,0)--(-1.5,3) (1.5,0)--(1.5,3);\draw[geoTrait](0,3)ellipse(1.5 and .42);\draw[geoTrait](-1.5,0)arc(180:360:1.5 and .42);\draw[otMuted,dashed](-1.5,0)arc(180:0:1.5 and .42) (0,0)--(0,3);\draw[otMuted,<->](-1.9,0)--node[left]{10 cm}(-1.9,3);\draw[geoTrait](0,3)--node[above]{3 cm}(1.5,3);'
    tex+=r'\geoSolution{\draw[otGreenDark,fill=otGreenTint,fill opacity=.5](0,1.5)ellipse(1.5 and .42);}\node[below,font=\scriptsize,align=center]at(0,-.5){plan perpendiculaire\\à l’axe};\end{scope}'
    tex+=r'\begin{scope}[xshift=2.6cm]\draw[geoTrait](-1.5,0)--(-1.5,3) (1.5,0)--(1.5,3);\draw[geoTrait](0,3)ellipse(1.5 and .42);\draw[geoTrait](-1.5,0)arc(180:360:1.5 and .42);\draw[otMuted,dashed](-1.5,0)arc(180:0:1.5 and .42) (0,0)--(0,3);'
    tex+=r'\geoSolution{\fill[otGreenTint,opacity=.6](-1.5,0)rectangle(1.5,3);\draw[otGreenDark,line width=.9pt](-1.5,0)rectangle(1.5,3);}\node[below,font=\scriptsize,align=center]at(0,-.5){plan contenant\\l’axe};\end{scope}'
    dessin('espace-section-cylindre',tex,'Deux coupes du même cylindre ; les sections sont colorées en vert au corrigé.')
    S=(2.6,4.5);Ap,Bp,Cp,Dp=(0,0),(4,0),(5.2,1.2),(1.2,1.2)
    k=1/3;red=lambda P:(S[0]+(P[0]-S[0])*k,S[1]+(P[1]-S[1])*k)
    a,b,c,d=red(Ap),red(Bp),red(Cp),red(Dp)
    tex=rf'\draw[geoTrait](0,0)--(4,0)--(5.2,1.2)--(2.6,4.5)--cycle (2.6,4.5)--(4,0);\draw[otMuted,dashed](0,0)--(1.2,1.2)--(5.2,1.2) (1.2,1.2)--(2.6,4.5) (2.6,4.5)--(2.6,.6);'
    tex+=pt('S',S,'above')+r'\node[below left]at(0,0){$A$};\node[below right]at(4,0){$B$};\node[right]at(5.2,1.2){$C$};\node[above left]at(1.2,1.2){$D$};\node[below]at(2,0){6 cm};\fill[otNavy](2.6,.6)circle(1.2pt)node[below,font=\scriptsize]{$O$};'
    tex+=rf'\draw[otMuted,dashed]({a[0]:.3f},{a[1]:.3f})--({b[0]:.3f},{b[1]:.3f})--({c[0]:.3f},{c[1]:.3f})--({d[0]:.3f},{d[1]:.3f})--cycle;\node[left,font=\scriptsize]at({a[0]-.1:.3f},{a[1]+.2:.3f}){{3 cm du sommet}};'
    tex+=r'\geoSolution{'+rf'\draw[otGreenDark,fill=otGreenTint,fill opacity=.6,line width=.9pt]({a[0]:.3f},{a[1]:.3f})--({b[0]:.3f},{b[1]:.3f})--({c[0]:.3f},{c[1]:.3f})--({d[0]:.3f},{d[1]:.3f})--cycle;'+'}'
    dessin('espace-section-pyramide',tex,'Pyramide régulière à base carrée ; le plan de coupe est parallèle à la base.')
    tex=r'\draw[geoTrait](-1.5,0)--(-1.5,3) (1.5,0)--(1.5,3);\draw[geoTrait](0,3)ellipse(1.5 and .42);\draw[geoTrait](-1.5,0)arc(180:360:1.5 and .42);\draw[otMuted,dashed](-1.5,0)arc(180:0:1.5 and .42);'
    tex+=r'\draw[otNavy,line width=.9pt](0,1.5)circle(1.5);\draw[otMuted,dashed](0,1.5)ellipse(1.5 and .4);\fill[otNavy](0,1.5)circle(1.3pt);\draw[otMuted](0,1.5)--node[above,font=\scriptsize]{3 cm}(1.5,1.5);\draw[otMuted,<->](2,0)--node[right]{6 cm}(2,3);'
    dessin('espace-archimede',tex,'Boule posée dans un cylindre qu’elle touche en haut, en bas et sur le côté.')
    sphere('defi-section',section=(10,6))

def build():
    schemas()
    dessin('dallage',r'\draw[geoTrait](0,0)rectangle(7,5);\geoSolution{\foreach\x in{1,...,6}{\draw[otGreenDark!50](\x,0)--(\x,5);}\foreach\y in{1,...,4}{\draw[otGreenDark!50](0,\y)--(7,\y);}}\node[below]at(3.5,0){252 cm};\node[left]at(0,2.5){180 cm};','Le quadrillage du dallage recherché est ajouté au corrigé.')
    dessin('engrenages',r'\draw[geoTrait](0,0)circle(1.2);\draw[geoTrait](3.2,0)circle(2);\foreach\a in{0,15,...,345}{\draw[otNavy]({1.12*cos(\a)},{1.12*sin(\a)})--({1.3*cos(\a)},{1.3*sin(\a)});}\foreach\a in{0,9,...,351}{\draw[otNavy]({3.2+1.92*cos(\a)},{1.92*sin(\a)})--({3.2+2.08*cos(\a)},{2.08*sin(\a)});}\node at(0,0){24 dents};\node at(3.2,0){40 dents};')
    tex=r'\begin{scope}[scale=.36]\draw[otRule!65,line width=.2pt](-6,-6)grid(6,7);\draw[otMuted,->](-6.5,0)--(6.8,0)node[right]{$x$};\draw[otMuted,->](0,-6.5)--(0,7.5)node[above]{$y$};\node[below left,font=\tiny]at(0,0){$O$};'
    for k in [-5,5]:tex+=rf'\node[below,font=\tiny,fill=white,inner sep=.5pt]at({k},0){{${k}$}};'
    tex+=r'\draw[geoTrait](0,0)circle(5);'
    for h in [3,5,6]:tex+=rf'\draw[otMuted,line width=.6pt](-6.3,{h})--(6.3,{h})node[right,font=\scriptsize]{{$y={h}$}};'
    tex+=r'\geoSolution{'+pt('',(-4,3),'above','otGreenDark')+pt('',(4,3),'above','otGreenDark')+pt('',(0,5),'above','otGreenDark')+r'}\end{scope}'
    dessin('cercle-droites',tex,'Repère orthonormé ; le cercle a pour centre O et pour rayon 5. Les intersections sont marquées au corrigé.')
    dessin('bordure',r'\fill[otNavyTint](0,0)rectangle(5,5);\fill[white](1,1)rectangle(4,4);\draw[geoTrait](0,0)rectangle(5,5)(1,1)rectangle(4,4);\node at(2.5,2.5){côté $x$};\draw[<->](0,4.5)--node[above]{2}(1,4.5);\node[below]at(2.5,0){côté extérieur $x+4$};')
    dessin('rectangle-equation',r'\draw[geoTrait](0,0)rectangle(6,3);\node[below]at(3,0){$x+7$};\node[right]at(6,1.5){$x$};\node at(3,1.5){périmètre 58 cm};')
    dessin('aires-egales',r'\draw[geoTrait](0,0)rectangle(3,3);\node[below]at(1.5,0){carré : $x+2$};\draw[geoTrait](5,0)rectangle(10,2.5);\node[below]at(7.5,0){$x+5$};\node[right]at(10,1.2){$x$};')
    tex=''
    for dy,lo,hi,lab,sol in [(0,-1,8,r'$3x\ge12$',4),(-1.3,-8,1,r'$-2x\ge8$',-4)]:
        tex+=rf'\begin{{scope}}[yshift={dy}cm,x=.55cm]\draw[otMuted,->]({lo-.5},0)--({hi+.6},0);\node[left]at({lo-.7},0){{{lab}}};'
        for t in range(lo,hi+1):tex+=rf'\draw[otMuted]({t},.08)--({t},-.08)node[below,font=\tiny]{{${t}$}};'
        if sol>0:tex+=rf'\geoSolution{{\draw[otGreenDark,line width=1.6pt]({sol},0)--({hi+.5},0);\draw[otGreenDark,line width=1.1pt]({sol+.2},.25)--({sol},.25)--({sol},-.25)--({sol+.2},-.25);}}'
        else:tex+=rf'\geoSolution{{\draw[otGreenDark,line width=1.6pt]({lo-.4},0)--({sol},0);\draw[otGreenDark,line width=1.1pt]({sol-.2},.25)--({sol},.25)--({sol},-.25)--({sol-.2},-.25);}}'
        tex+=r'\end{scope}'
    dessin('inequation-droites',tex,'Droites graduées ; les solutions sont représentées en vert au corrigé.')
    graph('inequation-graphique',[(r'1.5*\x',-1,7)],(-1,7),(-2,10),1,2,caption='Droite représentant $x\\mapsto1{,}5x$.',sol=r'\draw[geoAide](-1,6)--(7,6);\draw[otGreenDark,dashed](4,0)--(4,6);\draw[otGreenDark,line width=2pt](4,0)--(7,0);')
    graph('fonction-brisee',[],(-4,4),(-2,4),poly=r'\draw[geoTrait](-3,1)--(-1,3)--(1,-1)--(3,1);',sol=r'\draw[geoAide](-3,1)--(3,1);')
    graph('fonction-carre',[(r'\x*\x',-4.5,4.5)],(-5,5),(-1,20),yt=5,caption='$y=x^2$.',sol=r'\draw[geoAide](-5,16)--(5,16);')
    vals=[-3,-2,-1,-.5,0,.5,1,2,3]
    graph('carre-trace',[(r'\x*\x',-3.1,3.1)],(-3.5,3.5),(-1,10),1,1,caption='Repère à compléter.',blank=True,hauteur=6.5,sol=''.join(rf'\fill[otGreenDark]({a},{a*a})circle(1.8pt);' for a in vals))
    graph('carre-equation',[(r'\x*\x',-3.2,3.2)],(-3.5,3.5),(-3,10),1,1,hauteur=6.5,caption='Courbe de la fonction carré ; quadrillage fin de 0,5 en abscisse.',sub=.5,sol=r'\draw[geoAide](-3.5,5)--(3.5,5);\draw[otGreenDark,dashed](-2.236,0)--(-2.236,5) (2.236,0)--(2.236,5);\fill[otGreenDark](-2.236,5)circle(1.8pt) (2.236,5)circle(1.8pt);\draw[geoAide](-3.5,-2)--(3.5,-2);')
    graph('fonction-intersection',[(r'\x+2',-2,5),(r'2*\x-1',-2,5)],(-2,5),(-3,10),yt=2,caption='Bleu : f ; vert : g.')
    cylindre('cuve-hauteur',r'base : $0{,}8$ m$^2$',r'$1{,}5$ m',r'\draw[otGreenDark](0,1.5)ellipse(1.5 and .42);\draw[<->](-1.9,0)--node[left]{$h$}(-1.9,1.5);')
    dessin('rectangle-fonction',r'\draw[geoTrait](0,0)rectangle(6,2.5);\node[below]at(3,0){$20-x$};\node[right]at(6,1.25){$x$};\node at(3,1.25){périmètre 40 cm};')
    graph('promenade',[],(0,25),(0,800),5,200,poly=r'\draw[geoTrait](0,0)--(10,600)--(15,600)--(25,0);',xlabel='min',ylabel='m')
    graph('affine-trace-lineaire',[(r'1.5*\x',-2,5)],(-2,5),(-3,8),blank=True,caption='Repère à compléter.')
    graph('affine-trace',[(r'-\x+4',-1,6)],(-1,6),(-2,6),blank=True,caption='Repère à compléter.')
    graph('affine-deux-points',[],(0,6),(-6,12),yt=3,points=[('A',2,1),('B',5,10)],sol=r'\draw[geoReponse](0,-5)--(5.6667,12);')
    graph('affine-lecture',[(r'-2*\x+3',-2,4)],(-2,4),(-5,7),sol=r'\draw[otGreenDark,line width=1pt,->](0,3)--(1,3);\draw[otGreenDark,line width=1pt,->](1,3)--(1,1);\node[right,text=otGreenDark,font=\scriptsize]at(1,2){$-2$};\node[above,text=otGreenDark,font=\scriptsize]at(.5,3){$+1$};')
    graph('affine-paralleles',[(r'4*\x-1',-2,3),(r'4*\x+6',-2,3)],(-2,3),(-6,14),yt=2,caption='Bleu : f ; vert : g.')
    for nom,a,b,c,d in [('affine-tarifs',20,3,8,5),('brevet-A-tarifs',18,7,0,10)]:
        graph(nom,[(rf'{a}+{b}*\x',0,12),(rf'{c}+{d}*\x',0,12)],(0,12),(0,140 if b==7 else 80),2,20,caption='Bleu : A ; vert : B.',xlabel='$n$',ylabel='euros')
    statistiques();probabilites();geometrie_plane();vecteurs();espace();scripts()
    dessin('pyth-iso',r'\draw[geoTrait](-2,0)--(2,0)--(0,4.8)--cycle;\draw[geoAide](0,0)--(0,4.8);\node[below]at(-2,0){$A$};\node[below]at(2,0){$B$};\node[above]at(0,4.8){$C$};\node[below]at(0,0){$H$};\node[left]at(-1.1,2.4){13 cm};\node[right]at(1.1,2.4){13 cm};\node[below=6mm]at(0,0){AB = 10 cm};')
    dessin('trigo-batiment',r'\draw[otMuted](0,0)--(7,0);\draw[geoTrait](6,0)rectangle(6.7,4.6);\draw[geoTrait](0,0)--(0,.7);\draw[geoAide](0,.7)--(6,.7);\draw[geoTrait](0,.7)--(6,4.6);\node[left]at(0,.35){1,6 m};\node[below]at(3,0){25 m};\node at(1.4,1.15){$32^\circ$};')
    dessin('trigo-toit',r'\draw[geoTrait](-4,0)--(4,0)--(0,2.8)--cycle;\draw[geoAide](0,0)--(0,2.8);\node[below]at(0,0){8 m};\node at(-2.8,.35){$35^\circ$};')
    dessin('defi-corde',r'\draw[geoTrait](0,0)circle(2.6);\draw[geoTrait](-2.4,1)--(2.4,1);\draw[geoAide](0,0)--(0,1)--(2.4,1)--cycle;\node[below]at(0,0){$O$};\node[above]at(0,1){$H$};\node[above left]at(-2.4,1){$A$};\node[above right]at(2.4,1){$B$};\node[left]at(0,.5){5 cm};\node[below right]at(1.2,.5){13 cm};')
    dessin('defi-visees',r'\draw[geoTrait](0,0)node[below]{$A$}--(8,0)node[below]{pied}--(8,4.6)node[above]{sommet};\draw[geoTrait](0,0)--(8,4.6) (3.4,0)node[below]{$B$}--(8,4.6);\node[below]at(1.7,-.3){10 m};\node at(1.6,.3){$30^\circ$};\node at(4.5,.3){$45^\circ$};')

def write_all(root):
    build()
    for nom,d in FIGURES.items():
        (root/'figures'/f'{nom}.tex').write_text(d['tex']+'\n'+r'{\par\smallskip\fontsize{8}{10}\selectfont\color{otMuted}'+d['legende']+r'\par}'+'\n',encoding='utf8')
