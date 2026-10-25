"""Figures vectorielles liées aux données ; réponses de construction en vert."""
from math import ceil,floor,sqrt,sin,cos,tan,radians
from modele import FIGURES,figure,tableau
from donnees_figures import SCHEMAS
from donnees_scripts import SCRIPTS

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

def schemas():
    # Les schémas de Pythagore respectent aussi les proportions des données.
    mesures={1:(4,3,5),2:(6,8,10),3:(5,12,13),4:(4,7,sqrt(65)),5:(9,12,15),
      6:(5,7,9),7:(1.4,4.8,5),8:(20,15,25),10:(10,6,8),11:(2.4,3.2,4),12:(1.2,.9,1.5),13:(10,.75,sqrt(100+.75**2))}
    for i,(ab,ac,bc) in mesures.items():
        cx=(ab*ab+ac*ac-bc*bc)/(2*ab);cy=sqrt(max(0,ac*ac-cx*cx))
        SCHEMAS[f'pyth-{i:02}']['points']={'A':(0,0),'B':(ab,0),'C':(cx,cy)}
    SCHEMAS['thales-07']['points']['M']=(5*3/8,0)
    SCHEMAS['thales-07']['points']['N']=(2*5/12,3*5/12)
    SCHEMAS['thales-13']['points']['M']=(5*2/3,0)
    SCHEMAS['thales-13']['points']['N']=(2*2/3,3*2/3)
    mesures_trigo={1:(6,8),2:(6,8),3:(6,8),4:(6,8),
      5:(12*cos(radians(30)),6),6:(9*cos(radians(40)),9*sin(radians(40))),
      7:(7,7*tan(radians(50))),8:(6,8),9:(12,5),10:(9,12),12:(10,.8),
      13:(18*cos(radians(65)),18*sin(radians(65))),15:(7,7*tan(radians(38)))}
    for i,(ab,ac) in mesures_trigo.items():
        SCHEMAS[f'trigo-{i:02}']['points']={'A':(0,0),'B':(ab,0),'C':(0,ac)}
    reponses={
      ('pyth-02','BC'):'10 cm',('pyth-03','AC'):'12 cm',
      ('pyth-04','BC'):r'$\sqrt{65}$ cm',
      ('pyth-07','AC'):'4,8 m',('pyth-08','BC'):'25 cm',
      ('pyth-11','AC'):'3,2 m',('pyth-12','BC'):'1,5 m',
      ('pyth-13','BC'):r'$\approx10{,}03$ m',
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
        for a,b,t in d['labels']:
            if t=='?' and (nom,a+b) in reponses:
                t=r'\geoEnonce{?}\geoSolution{\textcolor{otGreenDark}{'+reponses[(nom,a+b)]+'}}'
            tex+=rf'\path({a})--node[midway,fill=white]{{{t}}}({b});'
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

def arbre(nom,p,q,lab=('R','B','R','B')):
    tex=''
    for node,x,y,l in [('o',0,0,''),('a',2,1.1,lab[0]),('b',2,-1.1,lab[1]),('aa',4.8,1.8,lab[2]),('ab',4.8,.4,lab[3]),('ba',4.8,-.4,lab[2]),('bb',4.8,-1.8,lab[3])]:
        tex+=rf'\node[inner sep=2pt]({node})at({x},{y}){{$ {l} $}};'
    for a,b,w in [('o','a',p[0]),('o','b',p[1]),('a','aa',q[0]),('a','ab',q[1]),('b','ba',q[2]),('b','bb',q[3])]:
        tex+=rf'\draw[otNavy]({a}.east)--node[above,sloped,fill=white,inner sep=1pt,font=\scriptsize]{{$ {w} $}}({b}.west);'
    dessin(nom,tex,'Chaque chemin représente deux résultats successifs ; lire les poids depuis leur nœud de départ.')

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
        tex+=rf'\draw[geoTrait](0,3)--node[above]{{{r}}}(1.5,3);'
    dessin(nom,tex+extra,'Cylindre en perspective ; les dimensions de l’énoncé fixent le modèle.')

def cone(nom,r='4 cm',h='9 cm',cut=False):
    tex=r'\draw[geoTrait](-2,0)--(0,3.5)--(2,0);\draw[geoTrait](-2,0)arc(180:360:2 and .5);\draw[otMuted,dashed](-2,0)arc(180:0:2 and .5) (0,0)--(0,3.5);'
    tex+=rf'\draw[otMuted,<->](2.5,0)--node[right]{{{h}}}(2.5,3.5);\draw[geoTrait](0,0)--node[below]{{{r}}}(2,0);'
    if cut:tex+=r'\draw[otGreenDark](0,1.75)ellipse(1 and .25);\node[left]at(-1.2,1.8){mi-hauteur};'
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

def cond(t):return t.replace('>=',r'$\ge$').replace('==',' = ').replace('>',' > ').replace('%',' mod ')
def script_lines(cmds,depth=0):
    out=[]
    for c in cmds:
        op=c[0];kind='calcul'
        if op=='set':txt=f'mettre {c[1]} à {c[2]}'
        elif op=='input':txt=f'demander un nombre ; mettre {c[1]} à réponse';kind='entree'
        elif op=='add':txt=f'ajouter {c[2]} à {c[1]}'
        elif op=='mul':txt=f'mettre {c[1]} à ({c[1]} × {c[2]})'
        elif op=='addvar':txt=f'ajouter {c[2]} à {c[1]}'
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
        out.append((depth,txt,kind))
    return out
def pile(lines,x=0,width=7.6):
    tex='';colors={'calcul':'otOrange!25','controle':'otOrange!38','entree':'otNavy!14','mouvement':'otNavy!24','evenement':'otGreen!28'}
    for i,(dep,txt,kind) in enumerate(lines):
        txt=txt.replace('×',r'$\times$')
        tex+=rf'\node[anchor=north west,rounded corners=1mm,draw=white,fill={colors[kind]},inner xsep=2mm,inner ysep=1.3mm,font=\scriptsize,text width={width-dep*.3}cm]at({x+dep*.3},{-i*.55}){{{txt}}};'
    return tex

def scripts():
    for nom,cmds in SCRIPTS.items():
        dessin(nom,pile([(0,'quand le drapeau est cliqué','evenement')]+script_lines(cmds)),'Blocs de type Scratch ; indentation et lignes « fin » délimitent les blocs imbriqués.')
    dessin('script-carres',pile([(0,'définir carré(c)','evenement'),(0,'répéter 4 fois','controle'),(1,'avancer de c','mouvement'),(1,'tourner de 90 degrés','mouvement'),(0,'fin de répéter','controle')],width=4.8)+pile([(0,'quand le drapeau est cliqué','evenement'),(0,'stylo baissé','mouvement'),(0,'répéter 3 fois','controle'),(1,'carré(30)','calcul'),(1,'relever le stylo','mouvement'),(1,'avancer de 40','mouvement'),(1,'baisser le stylo','mouvement'),(0,'fin de répéter','controle')],x=5.4,width=4.8),'À gauche, le bloc personnalisé ; à droite, le script qui l’appelle.')
    def trou(v):return r'\geoEnonce{\dots}\geoSolution{\textcolor{otGreenDark}{'+str(v)+'}}'
    dessin('script-simulation',pile([(0,'quand le drapeau est cliqué','evenement'),(0,'mettre succès à '+trou(0),'calcul'),(0,'répéter 600 fois','controle'),(1,'mettre dé à entier aléatoire de 1 à 6','calcul'),(1,'si dé = 6 alors','controle'),(2,'ajouter '+trou(1)+' à succès','calcul'),(1,'fin de si','controle'),(0,'fin de répéter','controle'),(0,'dire succès / '+trou(600),'entree')]),'Compléter les trois valeurs manquantes ; les valeurs sont inscrites en vert au corrigé.')
    dessin('script-parallele',pile([(0,'GUIDE : au clic sur le drapeau','evenement'),(0,'mettre score à 0','calcul'),(0,'envoyer départ et attendre','evenement'),(0,'dire score','entree')],width=4.8)+pile([(0,'JOUEUR : quand je reçois départ','evenement'),(0,'répéter 10 fois','controle'),(1,'ajouter 1 à score','calcul'),(0,'fin de répéter','controle')],x=5.4,width=4.8),'Deux lutins et une variable score partagée. Le message coordonne les scripts.')
    def cellule(v):return r'\geoEnonce{recopier}\geoSolution{\textcolor{otGreenDark}{'+str(v)+'}}'
    figure('script-tableur',tableau(['Ligne','Colonne A','Colonne B'],[['1','—','5'],['2','0',r'=3*A2+\$B\$1'],['3','1',cellule(8)],['4','2',cellule(11)],['5','3',cellule(14)],['6','4',cellule(17)]]),'B1 contient le terme constant. Les références absolues portent deux dollars.')
    dessin('brevet-B-script',pile([(0,'quand le drapeau est cliqué','evenement'),(0,'mettre c à 10','calcul'),(0,'répéter 4 fois','controle'),(1,'carré(c)','calcul'),(1,'relever le stylo','mouvement'),(1,'avancer de c + 5','mouvement'),(1,'baisser le stylo','mouvement'),(1,'ajouter 5 à c','calcul'),(0,'fin de répéter','controle')]),'Le bloc carré(c) revient à son point de départ avec la même orientation.')

def transformations():
    def poly(pts,col='otNavy'):return r'\draw['+col+',line width=.9pt]'+'--'.join(f'({a},{b})' for a,b in pts)+'--cycle;'
    data={1:([(2,1),(4,1),(3,3)],[(-2,1),(-4,1),(-3,3)],(-5,5),(-1,5)),
      2:([(3,2)],[(-3,-2)],(-5,5),(-4,4)),3:([(1,2),(3,2),(2,4)],[(4,3),(6,3),(5,5)],(-1,7),(-1,6)),
      4:([(3,1)],[(-1,3)],(-2,5),(-1,5)),6:([(2,1),(3,0),(1,3)],[(4,2),(6,0),(2,6)],(-1,7),(-1,7)),
      7:([(2,1),(3,0),(1,3)],[(-3,-1.5),(-4.5,0),(-1.5,-4.5)],(-6,4),(-5,4)),
      13:([(1,1),(3,1)],[(3,3),(7,3)],(-2,8),(-2,5))}
    for i,(pts,img,xb,yb) in data.items():
        tex=axes(xb,yb,ortho=True);sol=''
        if i in [2,3,4,6,7]:
            tex=tex.replace(r'\node[below left,font=\tiny]at(0,0){0};','')
        if len(pts)>2:tex+=poly(pts)
        for j,(x,y) in enumerate(pts):tex+=rf'\fill[otNavy]({x},{y})circle(1.8pt)node[above right,geoLabel]{{$ {"ABC"[j]} $}};'
        for j,(x,y) in enumerate(img):sol+=rf'\fill[otGreenDark]({x},{y})circle(1.8pt)node[below left,geoLabel]{{$ {"ABC"[j]}^{{\prime}} $}};'
        if len(img)>2:sol+=poly(img,'otGreenDark')
        if i==13:tex+=sol;sol=r'\fill[otGreenDark](-1,-1)circle(2pt)node[below left]{$O$};\draw[geoAide](-1,-1)--(3,3) (-1,-1)--(7,3);'
        if i==3:tex+=r'\fill[otNavy](0,0)circle(1.5pt)node[below left]{$P$};\fill[otNavy](3,1)circle(1.5pt)node[below right]{$Q$};\draw[geoAide,->](0,0)--(3,1);'
        if i in [2,4,6,7]:tex+=r'\node[below left]at(0,0){$O$};'
        dessin(f'transfo-{i:02}',tex+r'\geoSolution{'+sol+r'}\end{scope}','Repère orthonormé ; la construction cherchée est ajoutée en vert au corrigé.')
    dessin('transfo-05',r'''\draw[geoTrait](0,0)--(3,0)--(1,2)--cycle;
\begin{scope}[shift={(7,1)},rotate=120]\draw[geoAide](0,0)--(3,0)--(1,2)--cycle;\end{scope}
\node[below]at(1.5,-.3){triangle initial};\node[below]at(6,-.3){image par rotation};''','La rotation conserve les longueurs ; les positions sont schématiques.')
    dessin('transfo-09',r'''\begin{scope}[scale=.48]
\draw[geoTrait](1,.5)rectangle(3,3);\draw[geoAide](-3,-1.5)rectangle(-9,-9);
\fill[otNavy](0,0)circle(2pt)node[above]{$O$};\draw[otMuted,dashed](3,3)--(-9,-9);
\node[right]at(3,2){départ};\node[left]at(-9,-5){image};
\end{scope}''','Homothétie de rapport -3 : les côtés sont trois fois plus longs, de l’autre côté du centre.')
    dessin('transfo-14',r'''\draw[geoTrait](0,0)--(2,0)--(0,1.5)--cycle;
\draw[geoAide](4,0)--(9,0)--(4,3.75)--cycle;
\node[below]at(1,0){12 cm$^2$};\node[below]at(6.5,0){75 cm$^2$};''','Deux triangles de tailles comparées ; le centre et la disposition homothétique ne sont pas précisés.')
    dessin('transfo-15',r'''\draw[otMuted](-4.5,-2.25)--(2.5,1.25);
\fill[otNavy](0,0)circle(2pt)node[above left]{$O$};
\fill[otNavy](2,1)circle(2pt)node[below right]{$A$};
\geoSolution{
\fill[otGreenDark](-4,-2)circle(2pt)node[above left]{$A'$};
\node[above left,text=otGreenDark]at(2,1){$A''=A$};
}''','Le corrigé place l’image intermédiaire et l’image finale sur la droite passant par O et A.')
    pave('transfo-10','$L$',r'$\ell$','$h$')
    dessin('transfo-08',r'\draw[otMuted,->](-4,0)--(3,0);\fill[otNavy](0,0)circle(2pt)node[below]{$O$};\fill[otNavy](1.2,0)circle(2pt)node[below]{$A$};\fill[otNavy](-3,0)circle(2pt)node[below]{$A^\prime$};\draw[<->](0,.6)--node[above]{4 cm}(1.2,.6);\draw[<->](-3,1.3)--node[above]{10 cm}(0,1.3);')
    tex=''
    for i in range(6):tex+=rf'\draw[geoTrait]({i*1.7},0)--++(.9,0)--++(-.3,1)--cycle;'
    dessin('transfo-11',tex+r'\draw[<->](0,-.5)--node[below]{4 cm}(1.7,-.5);','Six motifs répétés par translation.')
    tex=''
    for i in range(8):tex+=rf'\begin{{scope}}[rotate={45*i}]\draw[geoTrait](.5,0)--(2.3,.2)--(1.2,.65)--cycle;\end{{scope}}'
    dessin('transfo-12',tex+r'\fill[otNavy](0,0)circle(2pt)node[below]{$O$};','Huit motifs obtenus par rotations.')
    dessin('pavage',r'\foreach\x in{0,1,2,3}{\foreach\y in{0,1,2}{\draw[geoTrait,fill=otNavyTint](\x,\y)rectangle++(1,1);}}','Pavage carré sans trou ni chevauchement.')

def build():
    schemas()
    dessin('dallage',r'\draw[geoTrait](0,0)rectangle(7,5);\geoSolution{\foreach\x in{1,...,6}{\draw[otGreenDark!50](\x,0)--(\x,5);}\foreach\y in{1,...,4}{\draw[otGreenDark!50](0,\y)--(7,\y);}}\node[below]at(3.5,0){252 cm};\node[left]at(0,2.5){180 cm};','Le quadrillage du dallage recherché est ajouté au corrigé.')
    dessin('engrenages',r'\draw[geoTrait](0,0)circle(1.2);\draw[geoTrait](3.2,0)circle(2);\foreach\a in{0,15,...,345}{\draw[otNavy]({1.12*cos(\a)},{1.12*sin(\a)})--({1.3*cos(\a)},{1.3*sin(\a)});}\foreach\a in{0,9,...,351}{\draw[otNavy]({3.2+1.92*cos(\a)},{1.92*sin(\a)})--({3.2+2.08*cos(\a)},{2.08*sin(\a)});}\node at(0,0){24 dents};\node at(3.2,0){40 dents};')
    dessin('bordure',r'\fill[otNavyTint](0,0)rectangle(5,5);\fill[white](1,1)rectangle(4,4);\draw[geoTrait](0,0)rectangle(5,5)(1,1)rectangle(4,4);\node at(2.5,2.5){côté $x$};\draw[<->](0,4.5)--node[above]{2}(1,4.5);\node[below]at(2.5,0){côté extérieur $x+4$};')
    dessin('rectangle-equation',r'\draw[geoTrait](0,0)rectangle(6,3);\node[below]at(3,0){$x+7$};\node[right]at(6,1.5){$x$};\node at(3,1.5){périmètre 58 cm};')
    dessin('aires-egales',r'\draw[geoTrait](0,0)rectangle(3,3);\node[below]at(1.5,0){carré : $x+2$};\draw[geoTrait](5,0)rectangle(10,2.5);\node[below]at(7.5,0){$x+5$};\node[right]at(10,1.2){$x$};')
    graph('fonction-brisee',[],(-4,4),(-2,4),poly=r'\draw[geoTrait](-3,1)--(-1,3)--(1,-1)--(3,1);',sol=r'\draw[geoAide](-3,1)--(3,1);')
    graph('fonction-carre',[(r'\x*\x',-4.5,4.5)],(-5,5),(-1,20),yt=5,caption='$y=x^2$.',sol=r'\draw[geoAide](-5,16)--(5,16);')
    graph('fonction-intersection',[(r'\x+2',-2,5),(r'2*\x-1',-2,5)],(-2,5),(-3,10),yt=2,caption='Bleu : f ; vert : g.')
    cylindre('cuve-hauteur',r'base : $0{,}8$ m$^2$',r'$1{,}5$ m',r'\draw[otGreenDark](0,1.5)ellipse(1.5 and .42);\draw[<->](-1.9,0)--node[left]{$h$}(-1.9,1.5);')
    dessin('rectangle-fonction',r'\draw[geoTrait](0,0)rectangle(6,2.5);\node[below]at(3,0){$20-x$};\node[right]at(6,1.25){$x$};\node at(3,1.25){périmètre 40 cm};')
    graph('promenade',[],(0,25),(0,800),5,200,poly=r'\draw[geoTrait](0,0)--(10,600)--(15,600)--(25,0);',xlabel='min',ylabel='m')
    graph('affine-trace-lineaire',[(r'1.5*\x',-2,5)],(-2,5),(-3,8),blank=True,caption='Repère à compléter.')
    graph('affine-trace',[(r'-\x+4',-1,6)],(-1,6),(-2,6),blank=True,caption='Repère à compléter.')
    graph('affine-deux-points',[],(0,6),(-6,12),yt=3,points=[('A',2,1),('B',5,10)],sol=r'\draw[geoReponse](0,-5)--(5.6667,12);')
    graph('affine-lecture',[(r'-2*\x+3',-2,4)],(-2,4),(-5,7))
    graph('affine-paralleles',[(r'4*\x-1',-2,3),(r'4*\x+6',-2,3)],(-2,3),(-6,14),yt=2,caption='Bleu : f ; vert : g.')
    for nom,a,b,c,d in [('affine-tarifs',20,3,8,5),('brevet-A-tarifs',18,7,0,10)]:
        graph(nom,[(rf'{a}+{b}*\x',0,12),(rf'{c}+{d}*\x',0,12)],(0,12),(0,140 if b==7 else 80),2,20,caption='Bleu : A ; vert : B.',xlabel='$n$',ylabel='euros')
    tex='';angle=0
    for val,col,lab in [(90,'otNavy!80','A'),(162,'otGreen!75','B'),(108,'otOrange!75','C')]:
        tex+=rf'\fill[{col}](0,0)--({angle}:1.8)arc({angle}:{angle+val}:1.8)--cycle;\node[text=white]at({angle+val/2}:1.15){{{lab}}};';angle+=val
    dessin('stat-disque',tex,'Secteurs correspondant aux effectifs 10, 18, 12 sur 40.')
    tex=axes((0,40),(0,10),10,2,'minutes','effectif')
    for a,h in [(0,4),(10,8),(20,6),(30,2)]:tex+=rf'\draw[geoTrait,fill=otNavy!18]({a},0)rectangle({a+10},{h});'
    dessin('stat-histogramme',tex+r'\end{scope}','Classes de largeur 10 min ; les hauteurs représentent les effectifs.')
    dessin('stat-axe-tronque',r'\draw[otMuted,->](0,0)--(0,3.5)node[above]{inscriptions};\draw[otMuted](0,0)--(5,0);\node[left]at(0,0){78};\node[left]at(0,1){80};\node[left]at(0,3){84};\draw[geoTrait,fill=otNavyTint](1,0)rectangle(2,1)(3,0)rectangle(4,3);\node[below]at(1.5,0){A};\node[below]at(3.5,0){B};','L’origine de l’axe vertical est 78 : comparer les nombres, pas les seules hauteurs visibles.')
    arbre('proba-pieces',['1/2','1/2'],['1/2']*4,('P','F','P','F'))
    figure('proba-des',tableau(['Dé 1 / Dé 2']+[str(n) for n in range(1,7)],[[str(i)]+[str(i+j) for j in range(1,7)] for i in range(1,7)]),'Chaque case représente un couple équiprobable et indique sa somme.')
    arbre('proba-remise',['3/5','2/5'],['3/5','2/5','3/5','2/5'])
    arbre('proba-sans-remise',['3/5','2/5'],['2/4','2/4','3/4','1/4'])
    arbre('brevet-A-arbre',['3/4','1/4'],['3/4','1/4','3/4','1/4'])
    arbre('brevet-B-arbre',['3/4','1/4'],['1/2']*4,('A','B','R','B'))
    graph('pyth-repere',[],(0,9),(0,12),1,2,points=[('A',1,2),('B',7,10)],poly=r'\draw[geoTrait](1,2)--(7,10);',sol=r'\draw[geoAide](1,2)--(7,2)--(7,10);',ortho=True)
    dessin('pyth-parc',r'\draw[geoTrait](0,0)rectangle(6.4,4.8);\draw[geoAide](0,0)--(6.4,4.8);\node[below]at(3.2,0){160 m};\node[left]at(0,2.4){120 m};')
    dessin('pyth-iso',r'\draw[geoTrait](-2,0)--(2,0)--(0,4.8)--cycle;\draw[geoAide](0,0)--(0,4.8);\node[below]at(-2,0){$A$};\node[below]at(2,0){$B$};\node[above]at(0,4.8){$C$};\node[below]at(0,0){$H$};\node[left]at(-1.1,2.4){13 cm};\node[right]at(1.1,2.4){13 cm};\node[below=6mm]at(0,0){AB = 10 cm};')
    for nom in ['semblables-angles','semblables-aires']:
        dessin(nom,r'\draw[geoTrait](0,0)node[below]{$A$}--(3,0)node[below]{$B$}--(1,2)node[above]{$C$}--cycle;\draw[geoTrait](5,0)node[below]{$F$}--(9.5,0)node[below]{$D$}--(6.5,3)node[above]{$E$}--cycle;')
    dessin('thales-ombre',r'\draw[otMuted](-.5,0)--(10,0);\draw[geoTrait](0,0)--(0,3.6)--(4.8,0) (6,0)--(6,.9)--(7.2,0);\node[left]at(0,2){arbre};\node[below]at(2.4,0){12 m};\node[above]at(6,.9){1,5 m};\node[below]at(6.6,0){2 m};')
    dessin('thales-milieux',r'\draw[geoTrait](0,0)node[left]{$A$}--(6,0)node[right]{$B$}--(2,4)node[above]{$C$}--cycle;\draw[geoTrait](3,0)node[below]{$M$}--(1,2)node[left]{$N$};\node[above right]at(2,1){7,4 m};')
    dessin('trigo-batiment',r'\draw[otMuted](0,0)--(7,0);\draw[geoTrait](6,0)rectangle(6.7,4.6);\draw[geoTrait](0,0)--(0,.7);\draw[geoAide](0,.7)--(6,.7);\draw[geoTrait](0,.7)--(6,4.6);\node[left]at(0,.35){1,6 m};\node[below]at(3,0){25 m};\node at(1.4,1.15){$32^\circ$};')
    dessin('trigo-toit',r'\draw[geoTrait](-4,0)--(4,0)--(0,2.8)--cycle;\draw[geoAide](0,0)--(0,2.8);\node[below]at(0,0){8 m};\node at(-2.8,.35){$35^\circ$};')
    transformations()
    pave('espace-01');cylindre('espace-02');cylindre('brevet-B-cylindre','4 cm','20 cm')
    dessin('espace-03',r'\draw[geoTrait](-2,0)--(1,-.5)--(2,1)--(0,4)--cycle (0,4)--(1,-.5);\draw[otMuted,dashed](-2,0)--(-1,1.5)--(2,1) (0,4)--(-1,1.5) (0,4)--(0,.5);\node[right]at(.1,2.4){hauteur 9 cm};\node[below]at(-.6,-.3){6 cm};','Pyramide à base carrée ; la hauteur est perpendiculaire à la base.')
    cone('espace-04');sphere('espace-05');sphere('espace-cavite','5 cm',inner=True);sphere('espace-section-sphere',section=(5,3))
    tex=''
    for lab,x,y in [('B',0,0),('C',1,0),('D',2,0),('E',3,0),('A',1,1),('F',1,-1)]:
        tex+=rf'\draw[geoTrait,fill=otNavyTint]({x},{y})rectangle({x+1},{y+1});\node at({x+.5},{y+.5}){{{lab}}};'
    dessin('espace-patron',tex,'Patron de cube ; chaque carré a pour côté 2 cm.')
    dessin('espace-vues',r'\draw[geoTrait](0,0)rectangle(4,1.5);\node[below]at(2,0){face : 8 par 3};\draw[geoTrait](5,0)rectangle(9,2.5);\node[below]at(7,0){dessus : 8 par 5};\draw[geoTrait](10,0)rectangle(12.5,1.5);\node[below]at(11.25,0){côté : 5 par 3};','Trois vues à même échelle, en centimètres.')
    pave('espace-section-pave',H='6 cm',extra=r'\draw[otGreenDark,fill=otGreenTint,fill opacity=.45](0,.87)--(5,.87)--(6.3,2.07)--(1.3,2.07)--cycle;\node[left]at(0,.5){2 cm};')
    pave('espace-repere','6','4','3',r'\node[below left]at(A){$O$};\node[below]at(B){$x$};\node[above left]at(D){$y$};\node[left]at(E){$z$};\fill[otGreenDark](2.642,1.767)circle(2pt)node[right]{$P(2;3;1)$};')
    dessin('espace-sphere',r'''\draw[geoTrait](0,0)circle(2.2);
\draw[otMuted](0,0)ellipse(2.2 and .75244);
\draw[otGreenDark](0,1.18577)ellipse(1.80213 and .61635);
\draw[otMuted,dashed](0,-2.06732)--(0,2.06732);
\foreach\l in{20,-50}{
\draw[otMuted,dashed]plot[domain=-90:90,samples=80]({2.2*cos(\x)*sin(\l)},{2.2*sin(\x)*cos(20)-2.2*cos(\x)*cos(\l)*sin(20)});
}
\fill[otNavy](-1.38052,.78959)circle(2pt)node[above left,geoLabel]{$B$};
\fill[otNavy](.61635,.60662)circle(2pt)node[below right,geoLabel]{$A$};
\fill[otNavy](0,2.06732)circle(1.5pt)node[above]{$N$};
\node[right]at(2.2,0){équateur};\node[right]at(1.8,1.35){$35^\circ$ N};
''','Projection de la sphère : A et B sont sur le parallèle de latitude 35 degrés nord, à des longitudes différentes.')
    cylindre('espace-reservoir','1 m','2 m',r'\draw[otGreenDark](-1.5,3)arc(180:0:1.5);\node[above]at(0,4.5){demi-boule};')
    cone('espace-cone-coupe','6 cm','12 cm',True)
    pave('espace-diagonale','3 cm','4 cm','12 cm',r'\draw[geoAide](A)--(C)--(G);\draw[geoReponse](A)--(G);')
    pave('synthese-bassin','4 m','2,5 m','0,8 m',r'\draw[otGreenDark](0,1.95)--(5,1.95)--(6.3,3.15)--(1.3,3.15)--cycle;')
    scripts()
    dessin('defi-corde',r'\draw[geoTrait](0,0)circle(2.6);\draw[geoTrait](-2.4,1)--(2.4,1);\draw[geoAide](0,0)--(0,1)--(2.4,1)--cycle;\node[below]at(0,0){$O$};\node[above]at(0,1){$H$};\node[above left]at(-2.4,1){$A$};\node[above right]at(2.4,1){$B$};\node[left]at(0,.5){5 cm};\node[below right]at(1.2,.5){13 cm};')
    dessin('defi-visees',r'\draw[geoTrait](0,0)node[below]{$A$}--(8,0)node[below]{pied}--(8,4.6)node[above]{sommet};\draw[geoTrait](0,0)--(8,4.6) (3.4,0)node[below]{$B$}--(8,4.6);\node[below]at(1.7,-.3){10 m};\node at(1.6,.3){$30^\circ$};\node at(4.5,.3){$45^\circ$};')
    sphere('defi-section',section=(10,6))
    dessin('defi-homotheties',r'''\draw[geoTrait](0,0)rectangle(2,1.2);
\draw[geoAide](4,0)rectangle(8,2.4);
\node[below]at(1,0){rectangle initial : 6 sur 10};
\node[below]at(6,0){après le rapport $-2$};
\draw[otMuted,->](8.6,1.2)--node[above]{$r>0$}(10.2,1.2);
\node[right]at(10.2,1.2){?};''','Comparaison des tailles ; les centres peuvent être différents et les positions ne sont pas imposées.')

def write_all(root):
    build()
    for nom,d in FIGURES.items():
        (root/'figures'/f'{nom}.tex').write_text(d['tex']+'\n'+r'{\par\smallskip\fontsize{8}{10}\selectfont\color{otMuted}'+d['legende']+r'\par}'+'\n',encoding='utf8')
