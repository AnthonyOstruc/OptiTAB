"""Figures vectorielles du CM2, avec réponses conditionnelles et métadonnées de contrôle."""
from pathlib import Path
from math import cos,sin,radians
from modele import figure,FIGURES
from outils_figures import dessin,pile
from donnees_scripts import SCRIPTS,lignes,executer
META={}

def answer(txt):
    return r'\geoEnonce{\textcolor{otMuted}{?}}\geoSolution{\textcolor{otGreenDark}{'+txt+'}}'
def dotpt(x,y,lab='',where='above',color='otNavy'):
    t=rf'\fill[{color}]({x},{y})circle(1.6pt)'
    if lab:t+=rf'node[{where},geoLabel]{{$ {lab} $}}'
    return t+';'
def grille(w,h):
    return rf'\draw[otRule!75,line width=.25pt](0,0)grid({w},{h});'
def poly(pts,style='geoTrait',close=True,fill=''):
    core='--'.join(f'({x},{y})' for x,y in pts)+('--cycle' if close else '')
    t=''
    if fill:t+=rf'\fill[{fill}]'+core+';'
    return t+rf'\draw[{style}]'+core+';'
def droiteg(nom,lo,hi,pas,labels,points=(),sol=(),minor=None,leg='Les graduations sont régulières ; lire la valeur d’un intervalle avant les positions.'):
    def X(val):return f'{(val-lo)*9.0/(hi-lo):.4f}'
    t=r'\begin{scope}'
    t+=r'\draw[otMuted,->](0,0)--(9.3,0);'
    if minor:
        k=0
        while lo+k*minor<=hi+1e-9:
            t+=rf'\draw[otMuted,line width=.5pt]({X(lo+k*minor)},-.06)--({X(lo+k*minor)},.06);';k+=1
    k=0
    while lo+k*pas<=hi+1e-9:
        t+=rf'\draw[otMuted,line width=.9pt]({X(lo+k*pas)},-.1)--({X(lo+k*pas)},.1);';k+=1
    for val,txt in labels:
        t+=rf'\node[below,font=\scriptsize]at({X(val)},-.12){{$ {txt} $}};'
    for lab,val in points:t+=dotpt(X(val),0,lab,'above')
    if sol:t+=r'\geoSolution{'+''.join(dotpt(X(v),0,l,'above','otGreenDark') for l,v in sol)+'}'
    dessin(nom,t+r'\end{scope}',leg)
    META[nom]={'type':'droite','bornes':[lo,hi],'points':[v for _,v in points],'solutions':[v for _,v in sol]}
def bande(nom,n,fill=0,solfill=0,w=7.2,h=.85,leg='La bande est partagée en parts égales.'):
    cw=w/n;t=''
    for i in range(fill):t+=rf'\fill[otNavy!28]({i*cw:.3f},0)rectangle({(i+1)*cw:.3f},{h});'
    if solfill:t+=r'\geoSolution{'+''.join(rf'\fill[otGreen!45]({i*cw:.3f},0)rectangle({(i+1)*cw:.3f},{h});' for i in range(fill,fill+solfill))+'}'
    t+=rf'\draw[geoTrait](0,0)rectangle({w},{h});'
    for i in range(1,n):t+=rf'\draw[geoTrait]({i*cw:.3f},0)--({i*cw:.3f},{h});'
    dessin(nom,t,leg)
    META[nom]={'type':'bande','parts':n,'remplies':fill,'sol':solfill}
def barres_diag(nom,cats,vals,step,sol=False,wrong=None,unit=4.2,leg=''):
    m=max(vals+([wrong[1]] if wrong else []))
    sy=unit/m;w=.62;gap=1.15
    t=rf'\draw[otMuted,->](-.3,0)--({len(cats)*gap+.4},0);\draw[otMuted,->](0,0)--(0,{unit+.5});'
    v=step
    while v<=m+1e-9:
        t+=rf'\draw[otRule!80,line width=.3pt](0,{v*sy:.3f})--({len(cats)*gap+.2},{v*sy:.3f});\node[left,font=\tiny]at(0,{v*sy:.3f}){{{v}}};'
        v+=step
    for i,(c,val) in enumerate(zip(cats,vals)):
        x=.35+i*gap
        if wrong and wrong[0]==i:
            t+=rf'\fill[otNavy!35]({x},0)rectangle({x+w},{wrong[1]*sy:.3f});'
            t+=rf'\geoSolution{{\draw[otGreenDark,line width=1.1pt]({x-.06},{val*sy:.3f})--({x+w+.06},{val*sy:.3f});\node[right,font=\tiny,otGreenDark]at({x+w},{val*sy:.3f}){{{val}}};}}'
        elif sol:
            t+=rf'\geoSolution{{\fill[otGreen!45]({x},0)rectangle({x+w},{val*sy:.3f});\draw[otGreenDark]({x},0)rectangle({x+w},{val*sy:.3f});}}'
        else:
            t+=rf'\fill[otNavy!35]({x},0)rectangle({x+w},{val*sy:.3f});\draw[otNavy]({x},0)rectangle({x+w},{val*sy:.3f});'
        t+=rf'\node[below,font=\tiny]at({x+w/2},0){{{c}}};'
    dessin(nom,t,leg or 'La hauteur de chaque barre se lit sur l’axe gradué.')
    META[nom]={'type':'barres','valeurs':list(vals),'pas':step}
def courbe_fig(nom,xs,ys,xlabels,step,unit=(8.6,4.0),leg='',marks=()):
    xmax=max(xs);m=max(ys)
    sx=unit[0]/xmax;sy=unit[1]/m
    t=rf'\draw[otMuted,->](0,0)--({unit[0]+.4},0);\draw[otMuted,->](0,0)--(0,{unit[1]+.5});'
    v=step
    while v<=m+1e-9:
        t+=rf'\draw[otRule!80,line width=.3pt](0,{v*sy:.3f})--({unit[0]+.2},{v*sy:.3f});\node[left,font=\tiny]at(0,{v*sy:.3f}){{{v}}};'
        v+=step
    for xv,xl in xlabels:
        t+=rf'\draw[otRule!80,line width=.3pt]({xv*sx:.3f},0)--({xv*sx:.3f},{unit[1]});\node[below,font=\tiny]at({xv*sx:.3f},0){{{xl}}};'
    pts=' -- '.join(f'({x*sx:.3f},{y*sy:.3f})' for x,y in zip(xs,ys))
    t+=rf'\draw[otNavy,line width=1pt] '+pts+';'
    for x,y in zip(xs,ys):t+=rf'\fill[otNavy]({x*sx:.3f},{y*sy:.3f})circle(1.4pt);'
    for lab,x,y in marks:t+=rf'\node[above,font=\tiny,otGreenDark]at({x*sx:.3f},{y*sy:.3f}){{{lab}}};'
    dessin(nom,t,leg or 'Chaque point se lit avec les deux axes ; la ligne montre l’évolution.')
    META[nom]={'type':'courbe','valeurs':list(ys)}
def cube3(i,j,k,s=.72,dx=.3,dy=.22):
    x=i*s+j*dx;y=k*s+j*dy
    t=rf'\filldraw[draw=otNavy,fill=white,line width=.7pt]({x:.3f},{y:.3f})rectangle({x+s:.3f},{y+s:.3f});'
    t+=rf'\filldraw[draw=otNavy,fill=otNavy!14,line width=.7pt]({x:.3f},{y+s:.3f})--({x+dx:.3f},{y+s+dy:.3f})--({x+s+dx:.3f},{y+s+dy:.3f})--({x+s:.3f},{y+s:.3f})--cycle;'
    t+=rf'\filldraw[draw=otNavy,fill=otNavy!26,line width=.7pt]({x+s:.3f},{y:.3f})--({x+s+dx:.3f},{y+dy:.3f})--({x+s+dx:.3f},{y+s+dy:.3f})--({x+s:.3f},{y+s:.3f})--cycle;'
    return t
def assemblage(nom,cubes,leg='Les cubes cachés portent les étages supérieurs.',extra=''):
    t=''
    for (i,j,k) in sorted(cubes,key=lambda c:(-c[1],c[2],c[0])):
        t+=cube3(i,j,k)
    dessin(nom,t+extra,leg)
    META[nom]={'type':'assemblage','cubes':len(cubes)}
def patron(cells,s=.9,labels=None,sol_cells=(),bad_cells=(),shift=(0,0)):
    t=rf'\begin{{scope}}[shift={{({shift[0]},{shift[1]})}}]'
    for (c,r) in cells:
        t+=rf'\draw[geoTrait]({c*s:.3f},{r*s:.3f})rectangle({(c+1)*s:.3f},{(r+1)*s:.3f});'
    for (c,r,lab) in (labels or []):
        t+=rf'\node[font=\small]at({(c+.5)*s:.3f},{(r+.5)*s:.3f}){{{lab}}};'
    if sol_cells:
        t+=r'\geoSolution{'+''.join(rf'\filldraw[draw=otGreenDark,fill=otGreen!30,line width=.8pt]({c*s:.3f},{r*s:.3f})rectangle({(c+1)*s:.3f},{(r+1)*s:.3f});'+(rf'\node[otGreenDark,font=\small]at({(c+.5)*s:.3f},{(r+.5)*s:.3f}){{{lab}}};' if lab else '') for (c,r,lab) in sol_cells)+'}'
    if bad_cells:
        t+=r'\geoSolution{'+''.join(rf'\draw[otOrange,line width=.8pt,dashed]({c*s:.3f},{r*s:.3f})rectangle({(c+1)*s:.3f},{(r+1)*s:.3f});\draw[otOrange,line width=.8pt]({c*s+.18:.3f},{r*s+.18:.3f})--({(c+1)*s-.18:.3f},{(r+1)*s-.18:.3f})({(c+1)*s-.18:.3f},{r*s+.18:.3f})--({c*s+.18:.3f},{(r+1)*s-.18:.3f});' for (c,r) in bad_cells)+'}'
    return t+r'\end{scope}'
def angle_ray(x0,y0,a0,a1,r1=2.2,r2=1.8,arc=.6,style='geoTrait',arcstyle='otGreenDark'):
    return (rf'\draw[{style}]({x0},{y0})--++({a0}:{r1});\draw[{style}]({x0},{y0})--++({a1}:{r2});'
            +rf'\fill[otNavy]({x0},{y0})circle(1.2pt);'
            +rf'\draw[{arcstyle},line width=.7pt]([shift={{({x0},{y0})}}]{a0}:{arc})arc({a0}:{a1}:{arc});')
def horloge(cx,h,m,r=1.35):
    t=rf'\begin{{scope}}[shift={{({cx},0)}}]\draw[geoTrait](0,0)circle({r});'
    for k in range(12):
        a=90-k*30
        t+=rf'\draw[otMuted]({a}:{r*.9})--({a}:{r});'
        t+=rf'\node[font=\tiny]at({a}:{r*.75}){{{12 if k==0 else k}}};'
    ah=90-(h%12)*30-m*0.5;am=90-m*6
    t+=rf'\draw[line width=1.5pt,otNavy](0,0)--({ah}:{r*.5});\draw[line width=1pt,otNavy](0,0)--({am}:{r*.8});\fill[otNavy](0,0)circle(1.4pt);'
    return t+r'\end{scope}'
def mirror_d(p):
    return (p[1],p[0])
def symdiag(nom,chains,g,points=None,cells=None,sol_cells=None,leg='L’axe suit la diagonale du quadrillage ; les écarts s’échangent de part et d’autre.',extra='',wrong=''):
    t=grille(g,g)+rf'\draw[otOrange,dashed,line width=1pt](-.3,-.3)--({g+.3},{g+.3});'
    orig=[];imgs=[];sol=''
    for ch in chains:
        t+=poly(ch,'geoTrait',close=len(ch)>2)
        mi=[mirror_d(p) for p in ch]
        sol+=poly(mi,'geoReponse',close=len(ch)>2)
        orig+=list(ch);imgs+=mi
    for c,r in (cells or []):
        t+=rf'\fill[otNavy!40]({c},{r})rectangle({c+1},{r+1});'
    for c,r in (sol_cells or []):
        sol+=rf'\fill[otGreen!50]({c},{r})rectangle({c+1},{r+1});'
    for lab,x,y in (points or []):
        t+=dotpt(x,y,lab,'above left')
        mx,my=mirror_d((x,y))
        sol+=dotpt(mx,my,lab+"'",'below right','otGreenDark')
        orig.append((x,y));imgs.append((mx,my))
    t+=wrong
    t+=r'\geoSolution{'+sol+'}'
    dessin(nom,rf'\begin{{scope}}[scale=.62]{t}{extra}\end{{scope}}',leg)
    META[nom]={'type':'symdiag','originaux':orig,'images':imgs,'grille':g}
def symaxe(nom,chains,axis,gw,gh,points=None,leg='Quadrillage de principe ; l’axe est en tirets.',extra=''):
    o,v=axis
    t=grille(gw,gh)
    t+=(rf'\draw[otOrange,dashed,line width=1pt]({v},-.25)--({v},{gh+.25});' if o=='v' else rf'\draw[otOrange,dashed,line width=1pt](-.25,{v})--({gw+.25},{v});')
    orig=[];imgs=[];sol=''
    for ch in chains:
        t+=poly(ch,'geoTrait',close=len(ch)>2)
        mi=[(2*v-x,y) if o=='v' else (x,2*v-y) for (x,y) in ch]
        sol+=poly(mi,'geoReponse',close=len(ch)>2)
        orig+=list(ch);imgs+=mi
    for lab,x,y in (points or []):
        t+=dotpt(x,y,lab,'above left')
        mx,my=(2*v-x,y) if o=='v' else (x,2*v-y)
        sol+=dotpt(mx,my,lab+"'",'above right','otGreenDark')
        orig.append((x,y));imgs.append((mx,my))
    t+=r'\geoSolution{'+sol+'}'
    dessin(nom,rf'\begin{{scope}}[scale=.62]{t}{extra}\end{{scope}}',leg)
    META[nom]={'type':'symetrie','axe':[o,v],'originaux':orig,'images':imgs,'grille':[gw,gh]}
def urne(nom,items,leg='Les boules sont indiscernables au toucher.'):
    t=r'\draw[otMuted,line width=.9pt](-.5,2.0)--(-.5,-.55)--(5.1,-.55)--(5.1,2.0);'
    for i,lab in enumerate(items):
        color={'R':'otOrange!60','B':'otNavy!32','V':'otGreen!55','N':'otInk!55'}[lab[0]]
        t+=rf'\node[circle,draw=otMuted,fill={color},minimum size=6.6mm,font=\scriptsize]at({i%5*1.15},{1.25-i//5*1.05}){{{lab}}};'
    dessin(nom,t,leg)
    META[nom]={'type':'urne','items':list(items)}
def roue(nom,angles,labels,colors=None,leg='Le repère fixe désigne le secteur gagnant.',shift=0):
    assert sum(angles)==360
    cols=colors or ['otNavy!30','otGreen!40','otOrange!45','otNavy!12','otGreen!20','otOrange!25','otNavy!45','otOrange!60']
    t=rf'\begin{{scope}}[shift={{({shift},0)}}]';start=90
    for a,lab,col in zip(angles,labels,cols):
        end=start+a;mid=(start+end)/2
        t+=rf'\filldraw[draw=white,line width=.8pt,fill={col}](0,0)--({start}:1.5)arc({start}:{end}:1.5)--cycle;'
        t+=rf'\node[font=\tiny]at({mid}:1.0){{{lab}}};'
        start=end
    t+=r'\draw[otNavy,line width=.9pt](0,0)circle(1.5);\fill[otInk](90:1.65)--(84:1.82)--(96:1.82)--cycle;\end{scope}'
    return t
def arbre2(nom,n1,n2,lab1,lab2,leg='Chaque chemin de la racine à une feuille est une issue.',sol_idx=()):
    t='';dy1=1.5;x1=2.2;x2=4.4
    for i,a in enumerate(lab1):
        y1=(len(lab1)-1)*dy1/2-i*dy1
        t+=rf'\draw[otMuted](0,0)--({x1},{y1});\node[fill=otNavy!15,rounded corners=1mm,inner sep=2pt,font=\scriptsize]at({x1},{y1}){{{a}}};'
        for j,b in enumerate(lab2):
            y2=y1+( (len(lab2)-1)*0.55-j*1.1 )/2
            y2=y1+((len(lab2)-1)/2-j)*0.62
            idx=i*len(lab2)+j
            col='otGreen!35' if idx in sol_idx else 'otNavy!8'
            t+=rf'\draw[otMuted]({x1+.35},{y1})--({x2},{y2:.2f});\node[fill={col},rounded corners=1mm,inner sep=2pt,font=\scriptsize]at({x2+.75},{y2:.2f}){{{a}{b}}};'
    dessin(nom,t,leg)
    META[nom]={'type':'arbre','issues':len(lab1)*len(lab2)}
def circulaire(nom,parts,labels,leg='Le disque entier représente le total ; chaque secteur, une part du tout.'):
    t='';start=90
    cols=['otNavy!35','otGreen!40','otOrange!45','otNavy!15']
    total=sum(parts)
    for p,lab,col in zip(parts,labels,cols):
        a=360*p/total;end=start+a;mid=(start+end)/2
        t+=rf'\filldraw[draw=white,line width=1pt,fill={col}](0,0)--({start}:1.7)arc({start}:{end:.2f}:1.7)--cycle;'
        t+=rf'\node[font=\tiny]at({mid:.2f}:1.12){{{lab}}};'
        start=end
    t+=r'\draw[otNavy,line width=.9pt](0,0)circle(1.7);'
    dessin(nom,t,leg)
    META[nom]={'type':'secteurs','angles':[360*p/total for p in parts]}

# ================================================================= nombres et programmes
def nombres():
    droiteg('cours-droite-millions',3000000,6000000,1000000,[(3000000,r'3\,000\,000'),(4000000,r'4\,000\,000'),(5000000,r'5\,000\,000'),(6000000,r'6\,000\,000')],
        minor=200000,points=[(r'4\,600\,000',4600000)],leg='Chaque petit intervalle vaut 200 000 : cinq pas séparent deux millions voisins.')
    droiteg('num-7',3000000,6000000,1000000,[(3000000,r'3\,000\,000'),(4000000,r'4\,000\,000'),(5000000,r'5\,000\,000'),(6000000,r'6\,000\,000')],
        minor=200000,points=[('A',3200000),('B',4600000),('C',5800000)])
    dessin('prog-cours',pile(lignes(SCRIPTS[1])),'Le programme se lit de haut en bas ; chaque étape agit sur le nombre obtenu.')
    META['prog-cours']={'type':'script','numero':1}
    dessin('prog-2',pile(lignes(SCRIPTS[1])),'Suivre les étapes dans l’ordre, en notant le nombre après chacune.')
    META['prog-2']={'type':'script','numero':1}
    t='';x0=0.0
    for n,e in enumerate([1,2,3],1):
        cells=sorted(set([(k,0) for k in range(-e,e+1)]+[(0,k) for k in range(-e,e+1)]))
        for (cx,cy) in cells:
            t+=rf'\draw[geoTrait]({x0+cx*.42:.2f},{cy*.42:.2f})rectangle({x0+cx*.42+.42:.2f},{cy*.42+.42:.2f});'
        t+=rf'\node[below,font=\tiny]at({x0+.2:.2f},{-e*.42-.2:.2f}){{étape {n}}};'
        x0+=e*.42*2+1.5
    dessin('motifs-11',t,'La croix gagne quatre carreaux à chaque étape, un au bout de chaque branche : 5, 9, 13, …')
    META['motifs-11']={'type':'motifs','etapes':[5,9,13]}

# ================================================================= fractions et décimaux
def fractions():
    droiteg('cours-droite-sixiemes',0,4,1/6,[(0,'0'),(1,'1'),(2,'2'),(3,'3'),(4,'4')],
        points=[(r'\frac{19}6',19/6)],leg='L’unité est partagée en sixièmes : 19 sixièmes, c’est un pas après 3.')
    droiteg('fd-6',0,4,1/6,[(0,'0'),(1,'1'),(2,'2'),(3,'3'),(4,'4')],points=[('A',8/6),('B',19/6)],
        leg='L’unité est partagée en sixièmes ; chaque pas vaut un sixième.')
    droiteg('fd-7',0,3,1/5,[(0,'0'),(1,'1'),(2,'2'),(3,'3')],sol=[('C',8/5),('D',13/5)],
        leg='L’unité est partagée en cinquièmes ; les positions demandées figurent en vert.')
    droiteg('fd-8',0,1,1/12,[(0,'0'),(1,'1'),(0.5,r'\frac12')],points=[(r'\frac6{12}',0.5)],
        leg='Six douzièmes tombent exactement sur un demi : deux écritures, un seul point.')
    bande('frac-2',12,0,5,leg='La bande compte douze parts égales ; les cinq douzièmes coloriés figurent en vert au corrigé.')
    droiteg('dec-10',4.2,4.3,0.01,[(4.2,r'4{,}2'),(4.25,r'4{,}25'),(4.3,r'4{,}3')],minor=0.005,
        points=[('A',4.21),('B',4.27)],sol=[('C',4.235)],
        leg='Les grandes graduations valent un centième ; C se place au milieu d’un pas, en vert au corrigé.')

# ================================================================= aires
def grandeurs():
    t=grille(7,4)+r'\fill[otNavy!25](0,0)rectangle(7,4);'+grille(7,4)+r'\draw[geoTrait](0,0)rectangle(7,4);'
    t+=r'\node[below,font=\tiny]at(3.5,-.1){7 carreaux de 1 cm};\node[left,font=\tiny,rotate=90]at(-.25,2){4 rangées};'
    dessin('aire-1',rf'\begin{{scope}}[scale=.6]{t}\end{{scope}}','Quatre rangées de sept centimètres carrés : le produit résume le comptage.')
    META['aire-1']={'type':'cellules','aires':[28]}
    t=grille(10,10)+r'\draw[geoTrait](0,0)rectangle(10,10);'
    t+=r'\fill[otGreen!40](0,9)rectangle(1,10);\node[font=\tiny]at(3.3,9.5){1 cm$^2$};'
    t+=r'\node[below,font=\tiny]at(5,-.15){1 dm = 10 cm};'
    dessin('aire-5',rf'\begin{{scope}}[scale=.42]{t}\end{{scope}}','Le carré de 1 dm de côté contient dix rangées de dix centimètres carrés.')
    META['aire-5']={'type':'cellules','aires':[100]}
    t=grille(10,10)+r'\fill[otNavy!18](0,0)rectangle(10,10);'+grille(10,10)+r'\draw[geoTrait](0,0)rectangle(10,10);'
    t+=r'\fill[otGreen!45](0,9)rectangle(1,10);\draw[otGreenDark,line width=.8pt](0,9)rectangle(1,10);'
    t+=r'\draw[otMuted,<->](0,-.6)--(10,-.6);\node[below,font=\tiny]at(5,-.7){1 dm = 10 cm};'
    t+=r'\draw[otGreenDark,->](1.2,9.5)--(2.6,9.5);\node[right,font=\tiny,otGreenDark]at(2.6,9.5){1 cm$^2$};'
    dessin('cours-dm2',rf'\begin{{scope}}[scale=.38]{t}\end{{scope}}','Un décimètre carré : dix rangées de dix centimètres carrés, soit 100 cm$^2$.')
    META['cours-dm2']={'type':'cellules','aires':[100]}
    pts=[(0,0),(8,0),(8,2),(3,2),(3,6),(0,6)]
    t=poly([(p[0]*.55,p[1]*.55) for p in pts])
    t+=r'\node[below,font=\tiny]at(2.2,-.08){8 m};\node[left,font=\tiny]at(0,1.65){6 m};\node[right,font=\tiny]at(4.4,.55){2 m};\node[above,font=\tiny]at(.82,3.3){3 m};'
    t+=r'\node[above,font=\tiny]at(3.02,1.1){5 m};\node[right,font=\tiny]at(1.65,2.2){4 m};'
    t+=r'\geoSolution{\draw[geoAide](0,1.1)--(1.65,1.1);\node[font=\tiny,otGreenDark]at(2.2,.55){8 sur 2};\node[font=\tiny,otGreenDark]at(.82,2.2){3 sur 4};}'
    dessin('aire-7',t,'La pièce en L : compléter le grand rectangle ou découper en deux rectangles.')
    META['aire-7']={'type':'libre'}
    # Angles.
    t=angle_ray(0,0,0,50)+r'\node[below left,font=\small]at(0,0){$ B $};\node[right,font=\small]at(2.2,0){$ C $};\node[above,font=\small]at(50:1.8){$ A $};\node[font=\tiny]at(25:1.0){$\widehat{ABC}$};'
    dessin('ang-1',t,'L’angle de sommet B : la lettre du sommet s’écrit au milieu de la notation.')
    META['ang-1']={'type':'angles','mesures':[50]}
    t=angle_ray(0,0,0,50)+r'\node[below,font=\small]at(.9,-.3){$ A $};'
    t+=angle_ray(4.2,0,10,35)+r'\node[below,font=\small]at(5.1,-.3){$ B $};'
    t+=angle_ray(8.2,0,0,105)+r'\node[below,font=\small]at(9.1,-.3){$ C $};'
    dessin('ang-2',t,'Trois angles à comparer au calque : l’ouverture seule compte.')
    META['ang-2']={'type':'angles','mesures':[50,25,105]}
    t=angle_ray(0,0,15,70)+r'\node[below,font=\tiny]at(1.0,-.35){angle à reproduire};'
    t+=r'\draw[geoTrait](5.2,.2)--(8.2,.2);\fill[otNavy](5.6,.2)circle(1.3pt)node[below,geoLabel]{sommet};'
    t+=r'\geoSolution{\draw[geoReponse](5.6,.2)--++(55:2.1);\draw[otGreenDark,line width=.7pt]([shift={(5.6,.2)}]0:.55)arc(0:55:.55);}'
    dessin('ang-3',t,'Le calque transporte l’angle sur la demi-droite ; la reproduction figure en vert.')
    META['ang-3']={'type':'angles','mesures':[55]}
    pts=[(0,0),(3.1,0),(3.5,2.0),(0,2.3)]
    t=poly(pts)
    t+=r'\draw[otNavy](.28,0)--(.28,.28)--(0,.28);\draw[otNavy](0,2.02)--(.28,2.02)--(.28,2.3);'
    for (x,y),l,w in [((0,0),'A','below left'),((3.1,0),'B','below right'),((3.5,2.0),'C','above right'),((0,2.3),'D','above left')]:
        t+=rf'\node[{w},font=\small]at({x},{y}){{$ {l} $}};'
    dessin('ang-4',t,'Les petits carrés codent les angles droits confirmés par l’équerre.')
    META['ang-4']={'type':'libre'}
    t=angle_ray(0,0,0,55)+r'\node[below,font=\tiny]at(1.0,-.3){premier angle};'
    t+=angle_ray(4.0,0,0,45)+r'\node[below,font=\tiny]at(5.0,-.3){second angle};'
    t+=r'\geoSolution{\begin{scope}[shift={(8.2,0)}]'+angle_ray(0,0,0,55,style='geoReponse')+angle_ray(0,0,55,100,style='geoReponse',arcstyle='otOrange')+r'\node[below,font=\tiny,otGreenDark]at(.9,-.3){somme : plus qu’un droit};\end{scope}}'
    dessin('ang-6',t,'Les deux angles mis bout à bout, sommets superposés : la somme figure en vert.')
    META['ang-6']={'type':'angles','mesures':[55,45]}
    t=angle_ray(0,0,0,35)+r'\node[below,font=\tiny]at(1.0,-.3){angle donné};'
    t+=r'\geoSolution{\begin{scope}[shift={(5.2,0)}]'+angle_ray(0,0,0,35,style='geoReponse')+angle_ray(0,0,35,70,style='geoReponse',arcstyle='otOrange')+r'\node[below,font=\tiny,otGreenDark]at(1.0,-.3){le double};\end{scope}}'
    dessin('ang-7',t,'L’angle reporté deux fois côte à côte donne son double.')
    META['ang-7']={'type':'angles','mesures':[35,35]}
    t=angle_ray(0,0,0,90)+r'\node[below,font=\tiny]at(1.0,-.35){angle droit};'
    t+=r'\geoSolution{\draw[geoAide](0,0)--(45:2.0);\node[font=\tiny,otGreenDark]at(45:2.3){pli : 45^\circ};}'
    t=t.replace(r'pli : 45^\circ',r'pli : $45^\circ$')
    dessin('ang-8',t,'Le pliage côté sur côté partage l’angle droit en deux angles de 45 degrés.')
    META['ang-8']={'type':'angles','mesures':[90]}
    t=r'\geoSolution{'+angle_ray(0,0,0,90,style='geoReponse')+angle_ray(0,0,90,135,style='geoReponse',arcstyle='otOrange')+r'\node[font=\tiny,otGreenDark]at(60:2.3){90 + 45 = 135 degrés};}'
    t+=r'\geoEnonce{\draw[geoTrait](0,0)--(2.4,0);\fill[otNavy](0,0)circle(1.3pt);\node[below,font=\tiny]at(1.2,-.15){demi-droite de départ};}'
    dessin('ang-9',t,'Un angle droit, puis sa moitié contre lui : l’angle total mesure 135 degrés.')
    META['ang-9']={'type':'angles','mesures':[90,45]}
    t=angle_ray(0,0,0,40)+r'\node[below,font=\small]at(.9,-.3){$ D $};'
    t+=angle_ray(3.6,0,0,90)+r'\node[below,font=\small]at(4.5,-.3){$ A $};'
    t+=angle_ray(7.2,0,0,120,r1=1.9)+r'\node[below,font=\small]at(8.1,-.3){$ C $};'
    t+=angle_ray(10.6,0,0,170,r1=1.7,r2=1.7)+r'\node[below,font=\small]at(11.3,-.3){$ B $};'
    dessin('ang-10',rf'\begin{{scope}}[scale=.82]{t}\end{{scope}}','Quatre angles : l’angle droit sert de repère pour les classer.')
    META['ang-10']={'type':'angles','mesures':[40,90,120,170]}
    dessin('ang-11',horloge(0,3,0)+horloge(4.2,6,0),'À 3 h, les aiguilles forment un angle droit ; à 6 h, un angle plat.')
    META['ang-11']={'type':'horloge'}
    t=r'\draw[geoTrait](0,0)--(3.2,0);\draw[geoTrait](0,0)--(180:3.2);'
    for a in [45,90,135]:
        t+=rf'\draw[geoTrait](0,0)--({a}:3.0);'
    t+=r'\draw[otGreenDark,line width=.7pt](0:.8)arc(0:45:.8);\node[font=\tiny,otGreenDark]at(22:1.15){$45^\circ$};'
    t+=r'\draw[otMuted,line width=.5pt](0:2.6)arc(0:180:2.6);'
    dessin('ang-13',t,'L’angle plat de l’éventail, partagé en quatre secteurs identiques de 45 degrés.')
    META['ang-13']={'type':'angles','mesures':[45,45,45,45]}
    t=r'\draw[geoTrait](-2.6,0)--(2.6,0);\draw[geoTrait](0,0)--(-2.0,2.0)(0,0)--(2.0,2.0);'
    t+=r'\draw[otNavy]([shift={(0,0)}]45:.4)arc(45:135:.4);\node[font=\tiny]at(90:.75){angle droit};'
    t+=r'\geoSolution{\draw[otGreenDark,line width=.7pt]([shift={(0,0)}]0:.9)arc(0:45:.9);\node[font=\tiny,otGreenDark]at(22:1.25){$45^\circ$};}'
    dessin('ang-14',t,'Les deux pans également inclinés partagent l’angle droit du faîte : 45 degrés chacun.')
    META['ang-14']={'type':'angles','mesures':[90]}
    t=angle_ray(0,0,0,30,r1=3.1,r2=2.9)+r'\node[below,font=\small]at(1.4,-.3){$ E $};'
    t+=angle_ray(5.2,0,0,60,r1=1.5,r2=1.3)+r'\node[below,font=\small]at(5.9,-.3){$ F $};'
    dessin('ang-15',t,'Côtés longs mais petite ouverture pour E ; l’angle F, plus ouvert, est le plus grand.')
    META['ang-15']={'type':'angles','mesures':[30,60]}
    t=angle_ray(0,0,10,65)+r'\node[below,font=\tiny]at(1.1,-.3){l’angle et son calque};\draw[otMuted,dashed](0,0)--++(10:2.3);\draw[otMuted,dashed](0,0)--++(65:1.9);'
    dessin('cours-angle-calque',t,'Le calque décalqué se superpose : sommet sur sommet, côté sur côté.')
    META['cours-angle-calque']={'type':'libre'}

# ================================================================= géométrie plane
def geometrie():
    t=r'\fill[otNavy](0,1.9)circle(1.3pt)node[above,geoLabel]{$ R $};\fill[otNavy](2.2,1.9)circle(1.3pt)node[above,geoLabel]{$ S $};\draw[geoTrait](0,1.9)--(2.2,1.9);'
    t+=r'\fill[otNavy](3.6,1.6)circle(1.3pt)node[above,geoLabel]{$ T $};\fill[otNavy](5.6,2.2)circle(1.3pt)node[above,geoLabel]{$ U $};\draw[geoTrait](3.2,1.48)--(6.2,2.38);'
    t+=r'\draw[otMuted,<->](0,1.45)--(2.2,1.45);\node[below,font=\tiny]at(1.1,1.4){longueur RS};'
    dessin('geo-1',t,'Segment, droite et longueur : trois notations pour trois objets différents.')
    META['geo-1']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)--(6.6,0)node[right,font=\scriptsize]{$ (d) $};\fill[otNavy](2.6,1.6)circle(1.5pt)node[above,geoLabel]{$ M $};'
    t+=r'\geoSolution{\draw[geoReponse](2.6,2.0)--(2.6,-.5);\draw[otGreenDark](2.6,0)++(.24,0)--++(0,.24)--++(-.24,0);}'
    dessin('geo-2',t,'La perpendiculaire passe par M et coupe (d) à angle droit, codé en vert.')
    META['geo-2']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)--(6.6,.8)node[right,font=\scriptsize]{$ (d) $};\fill[otNavy](2.2,2.1)circle(1.5pt)node[above,geoLabel]{$ N $};'
    t+=r'\geoSolution{\draw[geoReponse](-.1,1.82)--(6.4,2.6);}'
    dessin('geo-3',t,'La parallèle garde le même écart avec (d) sur toute sa longueur.')
    META['geo-3']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)circle(1.5);\fill[otNavy](0,0)circle(1.4pt)node[below left,geoLabel]{$ O $};'
    t+=r'\draw[geoTrait](0,0)--(50:1.5);\node[font=\tiny]at(50:.9){\colorbox{white}{3,5 cm}};\draw[otMuted,dashed](-1.5,0)--(1.5,0);'
    dessin('geo-4',t,'Le rayon joint le centre au cercle ; le diamètre, deux fois plus long, traverse par O.')
    META['geo-4']={'type':'libre'}
    t=r'\geoSolution{}\draw[otMuted,dashed](0,0)rectangle(4.2,2.5);\node[font=\tiny,otMuted]at(2.1,1.4){croquis : rectangle 5 sur 3};'
    t+=r'\geoSolution{\begin{scope}[shift={(0,-3.6)}]\draw[geoReponse](0,0)rectangle(4.2,2.5);'
    t+=r'\fill[otGreenDark](0,0)circle(1.3pt)node[below left,geoLabel]{$ A $};\fill[otGreenDark](4.2,0)circle(1.3pt)node[below right,geoLabel]{$ B $};\fill[otGreenDark](4.2,2.5)circle(1.3pt)node[above right,geoLabel]{$ C $};\fill[otGreenDark](0,2.5)circle(1.3pt)node[above left,geoLabel]{$ D $};'
    t+=r'\fill[otGreenDark](2.1,0)circle(1.4pt)node[below,geoLabel]{$ M $};\draw[geoReponse](2.1,0)circle(2.1);\end{scope}}'
    dessin('geo-5',t,'Le cercle de centre M passe par A et par B : MA = MB, la moitié de AB. Échelle réduite.')
    META['geo-5']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)--(3.4,0);\fill[otNavy](0,0)circle(1.4pt)node[below left,geoLabel]{$ E $};\fill[otNavy](3.4,0)circle(1.4pt)node[below right,geoLabel]{$ F $};\node[below,font=\tiny]at(1.7,-.14){5 cm};'
    t+=r'\geoSolution{\draw[geoAide]([shift={(0,0)}]35:2.72)arc(35:75:2.72);\draw[geoAide]([shift={(3.4,0)}]105:2.72)arc(105:145:2.72);\draw[geoReponse](0,0)--(1.7,2.125)--(3.4,0);\fill[otGreenDark](1.7,2.125)circle(1.5pt)node[above,geoLabel]{$ G $};\draw[otGreenDark](.72,1.15)--(.9,1.3);\draw[otGreenDark](2.5,1.3)--(2.68,1.15);}'
    dessin('geo-6',t,'Les deux arcs de rayon 4 cm se croisent en G : GE = GF, triangle isocèle. Échelle réduite.')
    META['geo-6']={'type':'triangle','points':[(0,0),(3.4,0),(1.7,2.125)]}
    v=[('b',r'\draw[geoTrait](.1,.2)rectangle(1.8,1.3);'),
       ('c',r'\draw[geoTrait](.1,.2)rectangle(1.8,1.3);\draw[geoTrait](.1,.2)--(1.8,1.3)(1.8,.2)--(.1,1.3);'),
       ('d',r'\draw[geoTrait](.1,.2)rectangle(1.8,1.3);\draw[geoTrait](.1,.2)--(1.8,1.3)(1.8,.2)--(.1,1.3);\fill[otNavy](.95,.75)circle(1.5pt)node[above,font=\tiny]{O};'),
       ('a',r'\draw[geoTrait](.1,.2)rectangle(1.8,1.3);\draw[otMuted](.1,.2)--(1.8,1.3)(1.8,.2)--(.1,1.3);\draw[geoReponse](.95,.75)circle(.98);')]
    t=''
    for i,(lab,body) in enumerate(v):
        t+=rf'\begin{{scope}}[shift={{({i*2.7},0)}}]\draw[otRule!80,line width=.3pt](-.15,-.35)rectangle(2.15,1.6);{body}\node[below,font=\small]at(1.0,-.05){{({lab})}};\end{{scope}}'
    dessin('geo-7',t,'Les quatre étapes en désordre : chaque tracé a besoin des objets précédents.')
    META['geo-7']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)circle(1.3);\fill[otNavy](0,0)circle(1.4pt)node[below,geoLabel]{$ O $};'
    t+=r'\draw[geoTrait](0,0)--(40:1.3);\node[font=\tiny]at(40:.8){\colorbox{white}{3 cm}};'
    t+=r'\fill[otOrange](2.2,.9)circle(1.5pt)node[right,geoLabel]{$ P $};\draw[otMuted,dashed](0,0)--(2.2,.9);\node[font=\tiny]at(1.35,.75){\colorbox{white}{5 cm}};'
    dessin('geo-8',t,'P est à 5 cm du centre : plus loin que le rayon, donc à l’extérieur du cercle.')
    META['geo-8']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)rectangle(2.6,2.6);\draw[geoTrait](0,0)--(2.6,2.6);'
    t+=r'\fill[otNavy](0,0)circle(1.3pt)node[below left,geoLabel]{$ R $};\fill[otNavy](2.6,0)circle(1.3pt)node[below right,geoLabel]{$ S $};\fill[otNavy](2.6,2.6)circle(1.3pt)node[above right,geoLabel]{$ T $};\fill[otNavy](0,2.6)circle(1.3pt)node[above left,geoLabel]{$ U $};'
    t+=r'\node[below,font=\tiny]at(1.3,-.08){3 cm};\draw[otNavy](.24,0)--(.24,.24)--(0,.24);'
    dessin('geo-9',t,'La figure à décrire : un carré et sa diagonale [RT]. Échelle réduite.')
    META['geo-9']={'type':'libre'}
    t=r'\fill[otNavy](0,0)circle(1.5pt)node[below left,geoLabel]{$ O $};\fill[otNavy](1.9,.7)circle(1.5pt)node[above,geoLabel]{$ A $};'
    t+=r'\geoSolution{\draw[geoReponse](0,0)circle(2.02);\draw[otGreenDark,<->](0,0)--(1.9,.7);\node[font=\tiny,otGreenDark]at(.8,.65){rayon OA};}'
    dessin('geo-10',t,'Pointe en O, ouverture jusqu’à A : le cercle passe exactement par A.')
    META['geo-10']={'type':'libre'}
    t=r'\draw[geoTrait](1.25,0)--(2.5,.9)--(1.25,1.8)--(0,.9)--cycle;\node[below,font=\tiny]at(1.25,-.1){losange 1};'
    t+=r'\begin{scope}[shift={(3.9,0)}]\draw[geoTrait](1.6,0)--(3.2,.9)--(1.6,1.8)--(0,.9)--cycle;\node[below,font=\tiny]at(1.6,-.1){losange 2};\end{scope}'
    t+=r'\node[font=\tiny,otMuted]at(3.4,2.1){mêmes côtés, ouvertures différentes};'
    dessin('geo-11',t,'Deux losanges de même côté mais d’angles différents : la consigne ne suffisait pas.')
    META['geo-11']={'type':'libre'}
    t=r'\fill[otNavy](0,0)circle(1.4pt)node[below left,geoLabel]{$ O $};'
    t+=r'\geoSolution{\draw[geoReponse](0,0)circle(.7);\draw[geoReponse](0,0)circle(1.4);\draw[geoReponse](0,0)circle(2.1);\node[font=\tiny,otGreenDark]at(55:2.4){anneaux réguliers};}'
    dessin('geo-12',t,'Trois cercles de même centre : des cercles concentriques. Échelle réduite.')
    META['geo-12']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)circle(.6)(0,0)circle(1.2)(0,0)circle(1.8);\fill[otNavy](0,0)circle(1.3pt);'
    t+=r'\node[font=\tiny]at(0,.3){10};\node[font=\tiny]at(0,.9){5};\node[font=\tiny]at(0,1.5){2};'
    dessin('geo-13',t,'La cible : trois cercles concentriques de rayons 2, 4 et 6 cm. Échelle réduite.')
    META['geo-13']={'type':'libre'}
    t=r'\geoSolution{}\draw[otMuted,dashed](0,0)rectangle(3.0,3.0);\node[font=\tiny,otMuted]at(1.5,1.5){carré ABCD à construire};'
    t+=r'\geoSolution{\begin{scope}[shift={(4.6,0)}]\draw[geoReponse](0,0)rectangle(3.0,3.0);\fill[otGreenDark](1.5,3.0)circle(1.3pt)node[below,geoLabel]{$ M $};\draw[geoReponse](1.5,3.0)--(1.5,4.5);\fill[otGreenDark](1.5,4.5)circle(1.4pt)node[above,geoLabel]{$ T $};\draw[geoReponse](0,3.0)--(1.5,4.5)--(3.0,3.0);\node[below,font=\tiny,otGreenDark]at(1.5,-.08){la maison : carré et toit isocèle};\end{scope}}'
    dessin('geo-14',t,'Le toit isocèle s’appuie sur le milieu du côté haut du carré. Échelle réduite.')
    META['geo-14']={'type':'libre'}
    t=r'\draw[geoTrait](0,1.2)--(3.2,1.2);\fill[otNavy](0,1.2)circle(1.2pt)node[left,geoLabel]{$ A $};\fill[otNavy](3.2,1.2)circle(1.2pt)node[right,geoLabel]{$ B $};'
    t+=r'\node[font=\tiny,otOrange]at(1.6,2.2){« place le milieu M de [AB] » avant « trace [AB] » ?};\draw[otOrange,->](1.6,1.95)--(1.6,1.4);'
    dessin('geo-15',t,'Échanger deux instructions dépendantes rend le programme inexécutable.')
    META['geo-15']={'type':'libre'}

def triangles():
    t=poly([(0,0),(2.1,0),(1.0,1.6)])+r'\node[below,font=\small]at(1.05,-.1){(1)};'
    t+=r'\begin{scope}[shift={(3.0,0)}]'+poly([(0,.2),(2.2,0),(2.4,1.5),(.3,1.7)])+r'\node[below,font=\small]at(1.2,-.1){(2)};\end{scope}'
    t+=r'\begin{scope}[shift={(6.3,0)}]'+poly([(0,.5),(1.0,0),(2.2,.4),(2.0,1.5),(.6,1.7)])+r'\node[below,font=\small]at(1.1,-.1){(3)};\end{scope}'
    t+=r'\begin{scope}[shift={(9.4,0)}]'+poly([(.55,0),(1.65,0),(2.2,.95),(1.65,1.9),(.55,1.9),(0,.95)])+r'\node[below,font=\small]at(1.1,-.1){(4)};\end{scope}'
    dessin('tri-1',t,'Compter les côtés : trois, quatre, cinq ou six.')
    META['tri-1']={'type':'libre'}
    t=poly([(0,0),(2.1,0),(0,1.6)])+r'\draw[otNavy](.24,0)--(.24,.24)--(0,.24);\node[below,font=\small]at(1.05,-.12){(1)};'
    t+=r'\begin{scope}[shift={(3.1,0)}]'+poly([(0,0),(2.1,0),(1.05,1.7)])+r'\draw[otNavy](.44,.78)--(.6,.93);\draw[otNavy](1.5,.93)--(1.66,.78);\node[below,font=\small]at(1.05,-.12){(2)};\end{scope}'
    t+=r'\begin{scope}[shift={(6.2,0)}]'+poly([(0,0),(2,0),(1,1.732)])+r'\draw[otNavy](.92,-.09)--(1.08,.09);\draw[otNavy](.42,.78)--(.58,.95);\draw[otNavy](1.42,.95)--(1.58,.78);\node[below,font=\small]at(1,-.12){(3)};\end{scope}'
    t+=r'\begin{scope}[shift={(9.3,0)}]'+poly([(0,0),(2.3,0),(1.8,1.5)])+r'\node[below,font=\small]at(1.15,-.12){(4)};\end{scope}'
    dessin('tri-2',t,'Les codes tranchent : angle droit, côtés égaux deux à deux ou trois à trois, ou rien.')
    META['tri-2']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)--(2.2,0);\fill[otNavy](0,0)circle(1.3pt);\fill[otNavy](2.2,0)circle(1.3pt);\node[below,font=\tiny]at(1.1,-.12){base 4 cm};'
    t+=r'\geoSolution{\draw[geoAide]([shift={(0,0)}]55:3.3)arc(55:80:3.3);\draw[geoAide]([shift={(2.2,0)}]100:3.3)arc(100:125:3.3);\draw[geoReponse](0,0)--(1.1,3.111)--(2.2,0);\draw[otGreenDark](.47,1.48)--(.63,1.63);\draw[otGreenDark](1.57,1.63)--(1.73,1.48);}'
    dessin('tri-3',t,'Les arcs de rayon 6 cm, centrés aux extrémités de la base, se croisent au sommet. Échelle réduite.')
    META['tri-3']={'type':'triangle','points':[(0,0),(2.2,0),(1.1,3.111)]}
    q=r'\draw[geoTrait](0,0)--(2.6,0)--(2.0,1.4)--(.4,1.4)--cycle;\draw[otNavy](.26,0)--(.26,.26)--(0,.26);'
    q=r'\draw[geoTrait](0,0)--(2.6,0)--(1.9,1.4)--(0,1.4)--cycle;\draw[otNavy](.24,0)--(.24,.24)--(0,.24);\draw[otNavy](0,1.16)--(.24,1.16)--(.24,1.4);\node[below,font=\small]at(1.3,-.1){(1)};'
    q+=r'\begin{scope}[shift={(3.6,0)}]\draw[geoTrait](0,.4)--(2.2,0)--(2.5,1.4)--(.6,1.5)--cycle;\node[below,font=\small]at(1.25,-.1){(2)};\end{scope}'
    q+=r'\begin{scope}[shift={(7.2,0)}]\draw[geoTrait](0,0)--(2.8,0)--(2.1,1.4)--(.7,1.4)--cycle;\node[below,font=\small]at(1.4,-.1){(3)};\end{scope}'
    q+=r'\begin{scope}[shift={(10.6,0)}]\draw[geoTrait](0,.2)--(2.0,0)--(1.7,1.5)--(.2,1.2)--cycle;\node[below,font=\small]at(1.0,-.1){(4)};\end{scope}'
    dessin('tri-4',rf'\begin{{scope}}[scale=.85]{q}\end{{scope}}','Chercher une paire de côtés parallèles : l’écart constant la révèle.')
    META['tri-4']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)--(3.2,0)--(2.3,1.6)--(0,1.6)--cycle;'
    t+=r'\draw[otNavy](.24,0)--(.24,.24)--(0,.24);\draw[otNavy](0,1.36)--(.24,1.36)--(.24,1.6);'
    t+=r'\node[below,font=\tiny]at(1.6,-.08){grande base};\node[above,font=\tiny]at(1.15,1.62){petite base};'
    dessin('tri-5',t,'Le trapèze rectangle : deux angles droits sur le même côté, deux bases parallèles.')
    META['tri-5']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)rectangle(3.5,2.0);\draw[geoTrait](0,0)--(3.5,2.0)(3.5,0)--(0,2.0);'
    t+=r'\node[below,font=\tiny]at(1.75,-.08){7 cm};\node[left,font=\tiny]at(0,1.0){4 cm};'
    t+=r'\geoSolution{\node[font=\tiny,otGreenDark]at(2.45,1.35){\colorbox{white}{même longueur}};\fill[otGreenDark](1.75,1.0)circle(1.3pt);}'
    dessin('tri-6',t,'Les diagonales du rectangle : même longueur, coupées en leur milieu. Échelle réduite.')
    META['tri-6']={'type':'libre'}
    import math as _m
    a=18;ca,sa=_m.cos(_m.radians(a)),_m.sin(_m.radians(a));L=2.6
    B=(L*ca,L*sa);C=(B[0]-L*sa,B[1]+L*ca);D=(-L*sa,L*ca)
    t=rf'\draw[geoTrait](0,0)--({B[0]:.3f},{B[1]:.3f});\node[below right,font=\tiny]at({B[0]/2:.3f},{B[1]/2:.3f}){{côté donné : 5 cm}};'
    t+=rf'\geoSolution{{\draw[geoReponse]({B[0]:.3f},{B[1]:.3f})--({C[0]:.3f},{C[1]:.3f})--({D[0]:.3f},{D[1]:.3f})--(0,0);\draw[otGreenDark]({ca*.24:.3f},{sa*.24:.3f})--++({-sa*.24:.3f},{ca*.24:.3f})--++({-ca*.24:.3f},{-sa*.24:.3f});}}'
    dessin('tri-7',t,'Le carré s’appuie sur son côté incliné : l’orientation ne change pas sa nature.')
    META['tri-7']={'type':'libre'}
    t=r'\draw[otMuted,dashed](0,0)--(2.4,.6)(0,0)--(.6,2.4);\node[font=\tiny,otMuted]at(2.1,1.9){croquis de l’angle};\node[below left,font=\small]at(0,0){$ A $};'
    B=(2.3,.58);D=(.58,2.3);C=(B[0]+D[0],B[1]+D[1])
    t+=rf'\geoSolution{{\draw[geoReponse](0,0)--({B[0]},{B[1]})--({C[0]},{C[1]})--({D[0]},{D[1]})--cycle;\draw[geoAide]([shift={{({B[0]},{B[1]})}}]95:2.37)arc(95:125:2.37);\draw[geoAide]([shift={{({D[0]},{D[1]})}}]-15:2.37)arc(-15:15:2.37);\fill[otGreenDark]({C[0]},{C[1]})circle(1.4pt)node[above right,geoLabel]{{$ C $}};}}'
    dessin('tri-8',t,'Quatre côtés égaux reportés au compas : le losange se ferme au croisement des arcs.')
    META['tri-8']={'type':'libre'}
    pts=[(cos(radians(a))*1.8,sin(radians(a))*1.8) for a in range(0,360,60)]
    t=r'\draw[geoTrait](0,0)circle(1.8);\fill[otNavy](0,0)circle(1.2pt);\fill[otNavy](1.8,0)circle(1.4pt)node[right,geoLabel]{$ A $};'
    t+=r'\geoSolution{'+poly(pts,'geoReponse')+''.join(rf'\fill[otGreenDark]({x:.3f},{y:.3f})circle(1.3pt);' for x,y in pts)
    t+=r'\draw[geoAide]([shift={(1.8,0)}]95:1.8)arc(95:145:1.8);\node[font=\tiny,otGreenDark]at(0,-2.25){le rayon reporté six fois};}'
    dessin('tri-9',t,'Le rayon, reporté six fois sur le cercle, dessine l’hexagone régulier. Échelle réduite.')
    META['tri-9']={'type':'hexagone','points':pts}
    pts=[(cos(radians(90+a*72))*1.5,sin(radians(90+a*72))*1.5) for a in range(5)]
    t=poly(pts)+''.join(rf'\draw[otNavy]({(pts[i][0]+pts[(i+1)%5][0])/2-0.07:.2f},{(pts[i][1]+pts[(i+1)%5][1])/2-0.07:.2f})--({(pts[i][0]+pts[(i+1)%5][0])/2+0.07:.2f},{(pts[i][1]+pts[(i+1)%5][1])/2+0.07:.2f});' for i in range(5))
    t+=r'\node[below,font=\small]at(0,-1.8){(1)};'
    t+=r'\begin{scope}[shift={(4.6,-1.0)}]'+poly([(0,.3),(1.3,0),(2.4,.7),(1.9,1.9),(.4,1.7)])+r'\node[below,font=\small]at(1.2,-.3){(2)};\end{scope}'
    dessin('tri-10',t,'Deux pentagones : côtés codés égaux pour le régulier, côtés quelconques pour l’autre.')
    META['tri-10']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)--(3.6,0)--(2.4,1.8)--(0,1.8)--cycle;'
    t+=r'\node[below,font=\tiny]at(1.8,-.08){6 cm};\node[above,font=\tiny]at(1.2,1.82){4 cm};\node[left,font=\tiny]at(0,.9){3 cm};'
    t+=r'\draw[otNavy](.22,0)--(.22,.22)--(0,.22);\draw[otNavy](0,1.58)--(.22,1.58)--(.22,1.8);'
    t+=r'\geoSolution{\draw[geoAide](2.4,0)--(2.4,1.8);\draw[otGreenDark](2.4,.22)--(2.18,.22)(2.18,0)--(2.18,.22);\node[font=\tiny,otGreenDark]at(1.2,.9){rectangle};\node[font=\tiny,otGreenDark]at(2.95,.55){triangle};}'
    dessin('tri-11',t,'La perpendiculaire abaissée découpe le trapèze rectangle en un rectangle et un triangle rectangle.')
    META['tri-11']={'type':'libre'}
    t=r'\geoEnonce{\node[font=\tiny,otMuted]at(2.4,1.0){écrire le programme, puis l’exécuter en vraie grandeur};}'
    pts=[(cos(radians(a))*1.5,sin(radians(a))*1.5) for a in range(0,360,60)]
    t+=r'\geoSolution{\begin{scope}[shift={(2.4,0)}]\draw[geoReponse](0,0)circle(1.5);'+poly(pts,'geoReponse')+r'\node[below,font=\tiny,otGreenDark]at(0,-1.85){cercle de 3 cm, rayon reporté six fois};\end{scope}}'
    dessin('tri-12',t,'Le programme : un cercle, six reports du rayon, six segments. Échelle réduite au corrigé.')
    META['tri-12']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)--(4.5,0)--(3.6,1.6)--(.9,1.6)--cycle;'
    t+=r'\node[below,font=\tiny]at(2.25,-.08){90 cm};\node[above,font=\tiny]at(2.25,1.62){60 cm};\node[font=\tiny]at(.18,.85){40 cm};\node[font=\tiny]at(4.3,.85){40 cm};'
    dessin('tri-13',t,'Le plateau en trapèze : additionner les quatre côtés pour la baguette de chant.')
    META['tri-13']={'type':'libre'}
    t=''
    import math as _m2
    def hexat(cx,cy,r=.62):
        ps=[(cx+r*_m2.cos(_m2.radians(30+60*k)),cy+r*_m2.sin(_m2.radians(30+60*k))) for k in range(6)]
        return poly(ps)
    w=1.08
    t+=r'\fill[otGreen!35]'+'--'.join(f'({1.62+0.62*_m2.cos(_m2.radians(30+60*k)):.3f},{0.93+0.62*_m2.sin(_m2.radians(30+60*k)):.3f})' for k in range(6))+'--cycle;'
    for row in range(3):
        for col in range(4):
            cx=col*w+(0 if row%2==0 else w/2);cy=row*.93
            t+=hexat(cx,cy)
    dessin('tri-14',t,'Le pavage des alvéoles : chaque hexagone partage ses six côtés avec ses voisines.')
    META['tri-14']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)rectangle(1.6,1.6);\draw[otNavy](.18,0)--(.18,.18)--(0,.18);\node[below,font=\tiny]at(.8,-.1){carré};'
    t+=r'\begin{scope}[shift={(2.8,0)}]\draw[geoTrait](.8,0)--(1.6,.8)--(.8,1.6)--(0,.8)--cycle;\node[below,font=\tiny]at(.8,-.1){losange};\end{scope}'
    t+=r'\begin{scope}[shift={(5.6,0)}]\draw[geoTrait](0,0)rectangle(2.2,1.3);\draw[otNavy](.18,0)--(.18,.18)--(0,.18);\node[below,font=\tiny]at(1.1,-.1){rectangle};\end{scope}'
    dessin('tri-15',t,'Trois figures pour trancher les affirmations : définitions avant impressions.')
    META['tri-15']={'type':'libre'}
    t=poly([(0,0),(2.1,0),(0,1.6)],'geoTrait')+r'\draw[otNavy](.24,0)--(.24,.24)--(0,.24);\node[below,font=\tiny]at(1.05,-.1){rectangle};'
    t+=r'\begin{scope}[shift={(3.1,0)}]'+poly([(0,0),(2.1,0),(1.05,1.7)])+r'\draw[otNavy](.44,.78)--(.6,.93);\draw[otNavy](1.5,.93)--(1.66,.78);\node[below,font=\tiny]at(1.05,-.1){isocèle};\end{scope}'
    t+=r'\begin{scope}[shift={(6.2,0)}]'+poly([(0,0),(2,0),(1,1.732)])+r'\draw[otNavy](.92,-.09)--(1.08,.09);\draw[otNavy](.42,.78)--(.58,.95);\draw[otNavy](1.42,.95)--(1.58,.78);\node[below,font=\tiny]at(1,-.1){équilatéral};\end{scope}'
    dessin('cours-triangles',t,'Les trois triangles particuliers et leurs codes.')
    META['cours-triangles']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)--(3.2,0)--(2.4,1.5)--(.8,1.5)--cycle;\node[below,font=\tiny]at(1.6,-.1){trapèze};'
    t+=r'\begin{scope}[shift={(4.4,0)}]\draw[geoTrait](0,0)--(3.0,0)--(2.2,1.5)--(0,1.5)--cycle;\draw[otNavy](.22,0)--(.22,.22)--(0,.22);\draw[otNavy](0,1.28)--(.22,1.28)--(.22,1.5);\node[below,font=\tiny]at(1.5,-.1){trapèze rectangle};\end{scope}'
    dessin('cours-trapeze',t,'Deux côtés opposés parallèles : le trapèze ; deux angles droits en plus : le trapèze rectangle.')
    META['cours-trapeze']={'type':'libre'}
    pts=[(cos(radians(a))*1.5,sin(radians(a))*1.5) for a in range(0,360,60)]
    t=r'\draw[otMuted](0,0)circle(1.5);'+poly(pts)+r'\fill[otNavy](0,0)circle(1.2pt);\draw[otMuted](0,0)--(1.5,0);\node[below,font=\tiny]at(.75,0){rayon};'
    dessin('cours-hexagone',t,'L’hexagone régulier : six côtés égaux au rayon du cercle qui le porte.')
    META['cours-hexagone']={'type':'libre'}

# ================================================================= symétrie et solides
def symetries():
    t=grille(10,4)+r'\draw[otOrange,dashed,line width=1pt](5,-.3)--(5,4.3);'
    t+=poly([(5,.5),(2,.5),(3,1.5),(2,2.5),(5,3.5)],'geoTrait',close=False)
    t+=poly([(5,.5),(8,.5),(7,1.5),(8,2.5),(5,3.5)],'geoTrait',close=False)
    dessin('cours-symetrie',rf'\begin{{scope}}[scale=.6]{t}\end{{scope}}','Le pliage le long de l’axe superpose exactement les deux moitiés.')
    META['cours-symetrie']={'type':'libre'}
    t=grille(6,6)+r'\draw[otOrange,dashed,line width=1pt](-.3,-.3)--(6.3,6.3);'
    t+=dotpt(4,1,'P','below right')+r'\geoSolution{'+dotpt(1,4,"P'",'above left','otGreenDark')+r'\draw[otMuted,dashed](4,1)--(1,4);}'
    dessin('cours-diagonale',rf'\begin{{scope}}[scale=.62]{t}\end{{scope}}','L’axe en diagonale échange les deux écarts : le point (4 ; 1) se reflète en (1 ; 4).')
    META['cours-diagonale']={'type':'symdiag','originaux':[(4,1)],'images':[(1,4)],'grille':6}
    t=r'\draw[geoTrait](0,0)rectangle(2,2);\draw[otOrange,dashed](1,-.3)--(1,2.3)(-.3,1)--(2.3,1)(-.25,-.25)--(2.25,2.25)(-.25,2.25)--(2.25,-.25);\node[below,font=\tiny]at(1,-.45){carré : 4 axes};'
    t+=r'\begin{scope}[shift={(3.6,0)}]\draw[geoTrait](0,.35)rectangle(2.6,1.65);\draw[otOrange,dashed](1.3,.05)--(1.3,1.95)(-.3,1)--(2.9,1);\node[below,font=\tiny]at(1.3,-.45){rectangle : 2 axes};\end{scope}'
    t+=r'\begin{scope}[shift={(7.4,0)}]\draw[geoTrait](0,.1)--(2,.1)--(1,1.83)--cycle;\draw[otOrange,dashed](1,-.2)--(1,1.95);\draw[otOrange,dashed](1.72,1.37)--(.25,.52);\draw[otOrange,dashed](.28,1.37)--(1.75,.52);\node[below,font=\tiny]at(1,-.45){équilatéral : 3 axes};\end{scope}'
    t+=r'\begin{scope}[shift={(11.0,0)}]\draw[geoTrait](1,1)circle(1);\draw[otOrange,dashed](0,1)--(2,1)(1,0)--(1,2)(.3,.3)--(1.7,1.7);\node[below,font=\tiny]at(1,-.45){cercle : une infinité};\end{scope}'
    dessin('sym-1',rf'\begin{{scope}}[scale=.85]{t}\end{{scope}}','Les axes des figures usuelles, à vérifier par pliage mental.')
    META['sym-1']={'type':'libre'}
    symaxe('sym-2',[[(3,1),(1,1),(1,3),(2,4),(3,3)]],('v',3),6,5,leg='Axe vertical : chaque sommet traverse à même distance, sur sa ligne.')
    symaxe('sym-3',[[(1,3),(1,6),(4,5),(1,4)]],('h',3),6,6,leg='Axe horizontal : le drapeau se reflète vers le bas ; le pied du mât, posé sur l’axe, ne bouge pas.')
    symdiag('sym-4',[],6,points=[('A',3,1),('B',5,2),('C',4,0)],leg='L’axe diagonal échange les deux écarts de chaque point.')
    symdiag('sym-5',[[(2,0),(3,2)]],6,points=[('A',2,0),('B',3,2)],leg='Chaque extrémité échange ses écarts ; le segment image a la même longueur.')
    cells=[(3,0),(4,0),(4,1),(5,0)]
    sol=[(0,3),(0,4),(1,4),(0,5)]
    symdiag('sym-6',[],6,cells=cells,sol_cells=sol,leg='Chaque case colorée se reflète en échangeant ses deux coordonnées.')
    t=grille(6,6)+r'\draw[otOrange,dashed,line width=1pt](-.3,-.3)--(6.3,6.3);'
    t+=poly([(2,0),(5,0),(5,1)])+r'\node[right,font=\scriptsize]at(5,1){$ C $};'
    t+=poly([(0,2),(0,5),(2,5)],'otNavy!60!white,line width=.8pt')
    t+=r"\node[above,font=\scriptsize]at(2,5){$ C' $ ?};"
    t+=r'\geoSolution{'+poly([(0,2),(0,5),(1,5)],'geoReponse')+r"\fill[otGreenDark](1,5)circle(1.8pt)node[above,geoLabel]{$ C' $};}"
    dessin('sym-7',rf'\begin{{scope}}[scale=.62]{t}\end{{scope}}','Le sommet fautif n’a pas échangé ses écarts : (5 ; 1) se reflète en (1 ; 5).')
    META['sym-7']={'type':'libre'}
    t=''
    for i,l in enumerate(['N','S','Z']):
        t+=rf'\begin{{scope}}[shift={{({i*2.4},0)}}]\node[font=\otBold\fontsize{{26}}{{28}}\selectfont,otNavy]at(.9,.9){{{l}}};\node[font=\tiny,otMuted]at(.9,-.15){{demi-tour, pas de pli}};\end{{scope}}'
    dessin('sym-8',t,'N, S et Z se retrouvent après un demi-tour, mais aucun pliage ne les superpose.')
    META['sym-8']={'type':'libre'}
    t=grille(8,6)+r'\draw[otOrange,dashed,line width=1pt](4,-.3)--(4,6.3);\draw[otOrange,dashed,line width=1pt](-.3,3)--(8.3,3);'
    quart=[(3,4),(2,3),(3,5)]
    for c,r in quart:t+=rf'\fill[otNavy!40]({c},{r})rectangle({c+1},{r+1});'
    allc=[]
    for c,r in quart:allc+=[(7-c,r),(c,5-r),(7-c,5-r)]
    t+=r'\geoSolution{'+''.join(rf'\fill[otGreen!50]({c},{r})rectangle({c+1},{r+1});' for c,r in allc)+r'}'+grille(8,6)
    dessin('sym-9',rf'\begin{{scope}}[scale=.6]{t}\end{{scope}}','Deux axes : on reflète à droite, puis tout le haut se reflète en bas.')
    META['sym-9']={'type':'libre'}
    symdiag('sym-10',[[(2,0),(2,4)]],6,points=[('R',2,0),('S',2,4)],leg='Le segment vertical de 4 carreaux se reflète en segment horizontal de 4 carreaux.')
    cells=[(4,2),(5,2),(5,3),(3,1),(5,4)]
    sol=[(2,4),(2,5),(3,5),(1,3),(4,5)]
    symdiag('sym-11',[],6,cells=cells,sol_cells=sol,leg='Le logo se complète case par case, écarts échangés à travers la diagonale.')
    t=grille(12,4)
    for s0,flip in [(0,False),(4,True),(8,False)]:
        pts=[(s0+1,1),(s0+3,1),(s0+3,3),(s0+2,2),(s0+1,3)] if not flip else [(s0+3,1),(s0+1,1),(s0+1,3),(s0+2,2),(s0+3,3)]
        if s0<8:t+=poly(pts)
        else:t+=r'\geoSolution{'+poly(pts,'geoReponse')+r'}'
    for x in [4,8]:
        t+=rf'\draw[otOrange,dashed,line width=1pt]({x},-.25)--({x},4.25);'
    dessin('sym-12',rf'\begin{{scope}}[scale=.6]{t}\end{{scope}}','La frise alterne le motif et son reflet à chaque axe ; le motif suivant figure en vert.')
    META['sym-12']={'type':'libre'}
    t=grille(6,6)
    pts=[(0,0),(3,1),(4,0),(5,5),(0,4),(1,3)]
    t+=poly(pts)
    t+=r'\geoSolution{\draw[otGreenDark,dashed,line width=1pt](-.3,-.3)--(6.3,6.3);\node[font=\tiny,otGreenDark]at(5.2,5.6){l’axe : la diagonale};}'
    dessin('sym-13',rf'\begin{{scope}}[scale=.62]{t}\end{{scope}}','Chercher le pli qui superpose exactement les deux moitiés de la figure.')
    META['sym-13']={'type':'libre'}
    t=grille(8,8)+r'\draw[otOrange,dashed,line width=1pt](4,-.3)--(4,8.3);\draw[otOrange,dashed,line width=1pt](-.3,4)--(8.3,4);'
    quart=[(3,4),(2,5),(3,6),(1,4),(3,5),(2,6)]
    for c,r in quart:t+=rf'\fill[otNavy!40]({c},{r})rectangle({c+1},{r+1});'
    allc=[]
    for c,r in quart:allc+=[(7-c,r),(c,7-r),(7-c,7-r)]
    t+=r'\geoSolution{'+''.join(rf'\fill[otGreen!50]({c},{r})rectangle({c+1},{r+1});' for c,r in allc)+r'}'+grille(8,8)
    dessin('sym-14',rf'\begin{{scope}}[scale=.5]{t}\end{{scope}}','Le quart de rosace se reflète trois fois : la rosace complète compte quatre quarts identiques.')
    META['sym-14']={'type':'libre'}
    t=grille(6,4)+r'\draw[otOrange,dashed,line width=1pt](3,-.25)--(3,4.25);'
    t+=poly([(1,1),(2,1),(2,2),(1,2)])
    t+=r'\geoSolution{'+poly([(4,1),(5,1),(5,2),(4,2)],'geoReponse')+r'\node[font=\tiny,otGreenDark]at(4.5,2.5){un carré, encore};}'
    t+=dotpt(3,3,'P','above right')
    dessin('sym-15',rf'\begin{{scope}}[scale=.62]{t}\end{{scope}}','L’image d’un carré reste un carré ; le point P, sur l’axe, est son propre symétrique.')
    META['sym-15']={'type':'libre'}

def solides():
    def pave3(w=1.6,d=.55,h=1.0):
        t=rf'\draw[geoTrait](0,0)rectangle({w},{h});'
        t+=rf'\draw[geoTrait](0,{h})--({d},{h+d*.75})--({w+d},{h+d*.75})--({w},{h});'
        t+=rf'\draw[geoTrait]({w},0)--({w+d},{d*.75})--({w+d},{h+d*.75});'
        t+=rf'\draw[otMuted,dashed](0,0)--({d},{d*.75})--({w+d},{d*.75})({d},{d*.75})--({d},{h+d*.75});'
        return t
    def pyram():
        return r'\draw[otMuted,dashed](0,0)--(1.7,0)--(2.3,.5)--(.6,.5)--cycle;\draw[geoTrait](0,0)--(1.7,0);\draw[geoTrait](0,0)--(1.15,1.9)--(1.7,0);\draw[geoTrait](2.3,.5)--(1.15,1.9);\draw[otMuted,dashed](.6,.5)--(1.15,1.9);'
    def cyl():
        return r'\draw[geoTrait](0,.35)--(0,1.7)(1.4,.35)--(1.4,1.7);\draw[geoTrait](.7,1.7)ellipse(.7 and .22);\draw[geoTrait](0,.35)arc(180:360:.7 and .22);\draw[otMuted,dashed](0,.35)arc(180:0:.7 and .22);'
    def cone():
        return r'\draw[geoTrait](0,.3)--(.8,2.0)--(1.6,.3);\draw[geoTrait](0,.3)arc(180:360:.8 and .25);\draw[otMuted,dashed](0,.3)arc(180:0:.8 and .25);'
    def boule():
        return r'\draw[geoTrait](0.8,1.0)circle(.8);\draw[otMuted](0,1.0)arc(180:360:.8 and .25);\draw[otMuted,dashed](0,1.0)arc(180:0:.8 and .25);'
    def prisme():
        return r'\draw[geoTrait](0,0)--(1.6,0)--(.8,1.1)--cycle;\draw[geoTrait](1.6,0)--(2.3,.5)(.8,1.1)--(1.5,1.6)--(2.3,.5);\draw[geoTrait](1.5,1.6)--(.8,1.1);\draw[otMuted,dashed](0,0)--(.7,.5)--(2.3,.5)(.7,.5)--(1.5,1.6);'
    names=[('cube',r'\begin{scope}[scale=.9]'+pave3(1.1,.45,1.1)+r'\end{scope}'),('pavé',pave3()),('cylindre',cyl()),('pyramide',pyram()),('cône',cone()),('boule',boule())]
    t=''
    for i,(lab,body) in enumerate(names):
        t+=rf'\begin{{scope}}[shift={{({(i%6)*2.72},0)}}]{body}\node[below,font=\tiny]at(.95,-.35){{{lab}}};\end{{scope}}'
    dessin('cours-solides',r'\begin{scope}[scale=.82]'+t+r'\end{scope}','Six solides usuels ; les arêtes cachées sont en pointillés.')
    META['cours-solides']={'type':'libre'}
    t=''
    for i,(lab,body) in enumerate(names):
        t+=rf'\begin{{scope}}[shift={{({(i%6)*2.72},0)}}]{body}\node[below,font=\tiny]at(.95,-.35){{({i+1})}};\end{{scope}}'
    dessin('sol-1',r'\begin{scope}[scale=.82]'+t+r'\end{scope}','Six solides numérotés : nommer chacun, puis trier les polyèdres.')
    META['sol-1']={'type':'libre'}
    dessin('sol-2',r'\begin{scope}[scale=1.1]'+pave3(1.3,.5,1.3)+r'\end{scope}'+r'\begin{scope}[shift={(3.4,0)},scale=1.1]'+pave3(1.9,.55,1.0)+r'\end{scope}','Le cube et le pavé : mêmes comptes de faces, d’arêtes et de sommets.')
    META['sol-2']={'type':'libre'}
    dessin('sol-3',prisme(),'Le prisme droit à base triangulaire : deux bases jumelles reliées par des rectangles.')
    META['sol-3']={'type':'libre'}
    dessin('sol-4',pyram(),'La pyramide à base carrée : la base et quatre faces triangulaires.')
    META['sol-4']={'type':'libre'}
    nets=[([(1,0),(1,1),(0,1),(2,1),(1,2),(1,3)],'(1)'),([(0,0),(1,0),(2,0),(3,0),(1,1),(1,-1)],'(2)'),([(0,0),(1,0),(2,0),(3,0),(0,1),(1,1)],'(3)')]
    t=''
    for i,(cells,lab) in enumerate(nets):
        miny=min(r for _,r in cells)
        cells2=[(c,r-miny) for c,r in cells]
        t+=rf'\begin{{scope}}[shift={{({i*3.3},0)}}]'
        for (c,r) in cells2:t+=rf'\draw[geoTrait]({c*.6:.3f},{r*.6:.3f})rectangle({(c+1)*.6:.3f},{(r+1)*.6:.3f});'
        t+=rf'\node[below,font=\small]at(1.2,-.22){{{lab}}};\end{{scope}}'
    dessin('sol-5',t,'Trois dispositions de six carrés : deux patrons, un contre-exemple.')
    META['sol-5']={'type':'patrons','nets':[c for c,_ in nets]}
    cells=[(1,0),(1,1),(0,1),(2,1),(1,2),(1,3)]
    labels=[(1,3,'A'),(1,2,'B'),(1,1,'C'),(1,0,'D'),(0,1,'E'),(2,1,'F')]
    dessin('sol-6',patron(cells,s=.8,labels=labels),'Sur le patron en croix, les faces opposées sont séparées par une face.')
    META['sol-6']={'type':'patron','cells':cells}
    def bande_pave(x0,mauvais=False):
        s=rf'\begin{{scope}}[shift={{({x0},0)}}]'
        s+=r'\draw[geoTrait](0,.7)rectangle(1.4,1.6);\draw[geoTrait](1.4,.7)rectangle(2.1,1.6);\draw[geoTrait](2.1,.7)rectangle(3.5,1.6);\draw[geoTrait](3.5,.7)rectangle(4.2,1.6);'
        s+=r'\draw[geoTrait](0,1.6)rectangle(1.4,2.3);'
        s+=(r'\draw[geoTrait](1.4,0)rectangle(2.8,.7);' if mauvais else r'\draw[geoTrait](0,0)rectangle(1.4,.7);')
        return s+r'\end{scope}'
    t=bande_pave(0)+r'\node[below,font=\small]at(2.1,-.1){(1)};'
    t+=bande_pave(5.0,True)+r'\node[below,font=\small]at(7.1,-.1){(2)};'
    dessin('sol-7',t,'Deux dispositions de six rectangles : les bords pliés ensemble doivent coïncider.')
    META['sol-7']={'type':'libre'}
    cells=[(1,0),(1,1),(0,1),(2,1),(1,2),(1,3)]
    labels=[(1,3,'1'),(1,2,'2'),(0,1,'3')]
    dessin('sol-8',patron(cells,s=.8,labels=labels,sol_cells=[(1,1,'6'),(1,0,'5'),(2,1,'4')]),'Les paires opposées d’un dé totalisent 7 ; les valeurs ajoutées figurent en vert.')
    META['sol-8']={'type':'patron','cells':cells}
    t=r'\geoEnonce{\node[font=\tiny,otMuted]at(2.6,1.2){tracer le patron en vraie grandeur};}'
    t+=r'\geoSolution{\begin{scope}[scale=.52]'
    t+=r'\draw[geoReponse](0,2)rectangle(4,4);\draw[geoReponse](4,2)rectangle(5,4);\draw[geoReponse](5,2)rectangle(9,4);\draw[geoReponse](9,2)rectangle(10,4);'
    t+=r'\draw[geoReponse](0,4)rectangle(4,5);\draw[geoReponse](0,1)rectangle(4,2);'
    t+=r'\node[font=\tiny,otGreenDark]at(2,3){4 sur 2};\node[font=\tiny,otGreenDark]at(2,4.5){4 sur 1};\node[font=\tiny,otGreenDark]at(2,1.5){4 sur 1};\node[font=\tiny,otGreenDark]at(4.5,3){1·2};\node[font=\tiny,otGreenDark]at(7,3){4 sur 2};\node[font=\tiny,otGreenDark]at(9.5,3){1·2};'
    t+=r'\end{scope}}'
    dessin('sol-9',t,'Un patron du pavé 4 sur 2 sur 1 : trois paires de rectangles, bords communs égaux. Échelle réduite.')
    META['sol-9']={'type':'libre'}
    cubes=[(i,j,0) for i in range(4) for j in range(2)]+[(i,0,1) for i in range(4)]+[(0,0,2),(1,0,2)]
    assemblage('sol-10',cubes,'Huit cubes au sol, quatre au deuxième étage, deux au sommet : compter étage par étage.')
    cubes11=[(0,0,0),(0,0,1),(1,0,0),(2,0,0),(2,0,1),(2,0,2),(3,0,0)]
    t=''
    for (i,j,k) in sorted(cubes11,key=lambda c:(-c[1],c[2],c[0])):t+=cube3(i,j,k)
    t+=r'\begin{scope}[shift={(4.0,0)}]\fill[otNavy!35](0,0)rectangle(4,1);\draw[otRule!80](0,0)grid(4,1);\node[below,font=\scriptsize]at(2,-.1){(1)};\end{scope}'
    t+=r'\begin{scope}[shift={(8.6,0)}]\fill[otNavy!35](0,0)rectangle(1,2);\fill[otNavy!35](1,0)rectangle(2,1);\fill[otNavy!35](2,0)rectangle(3,3);\fill[otNavy!35](3,0)rectangle(4,1);\draw[otRule!80](0,0)grid(4,3);\node[below,font=\scriptsize]at(2,-.1){(2)};\end{scope}'
    t+=r'\begin{scope}[shift={(13.2,0)}]\fill[otNavy!35](0,0)rectangle(3,1);\fill[otNavy!35](1,1)rectangle(2,3);\draw[otRule!80](0,0)grid(3,3);\node[below,font=\scriptsize]at(1.5,-.1){(3)};\end{scope}'
    t=r'\begin{scope}[scale=.8]'+t+r'\end{scope}'
    dessin('sol-11',t,'L’assemblage et trois vignettes : vue de dessus, vue de face, et une vue impossible.')
    META['sol-11']={'type':'assemblage','cubes':len(cubes11)}
    cubes12=[(i,j,0) for i in range(3) for j in range(3)]+[(i,j,1) for i in range(3) for j in range(3)]+[(0,0,2),(1,0,2)]
    assemblage('sol-12',cubes12,'Vingt cubes posés : il en manque sept pour fermer le grand cube de côté 3.')
    t=grille(6,4)
    t+=r'\node[font=\tiny]at(.5,.15){départ};\fill[otNavy](.5,.5)circle(2pt);\draw[otNavy,->](.5,.5)--(1.1,.5);'
    t+=r'\draw[otNavy,line width=1.2pt,->](.5,.5)--(3.5,.5)--(3.5,2.5)--(5.5,2.5)--(5.5,.5);'
    t+=r'\node[font=\tiny]at(5.5,.15){but};'
    dessin('sol-13',rf'\begin{{scope}}[scale=.72]{t}\end{{scope}}','Le chemin se code en avancées et quarts de tour, du point de vue du pion.')
    META['sol-13']={'type':'script','numero':7}
    t=grille(6,4)
    t+=r'\node[font=\tiny]at(.5,.15){départ};\fill[otNavy](.5,.5)circle(2pt);\draw[otNavy,->](.5,.5)--(1.1,.5);'
    t+=r'\geoSolution{\draw[geoReponse,line width=1.2pt,->](.5,.5)--(4.5,.5)--(4.5,2.5)--(.5,2.5)--(.5,.5);\fill[otGreenDark](.5,.5)circle(2.3pt);\node[font=\tiny,otGreenDark]at(2.5,2.9){retour à la case de départ};}'
    dessin('sol-14',rf'\begin{{scope}}[scale=.72]{t}\end{{scope}}','Le programme dessine un rectangle de 4 sur 2 : le pion revient à son point de départ.')
    META['sol-14']={'type':'script','numero':9}
    cubes15=[(i,j,k) for i in range(3) for j in range(3) for k in range(3)]
    t=''
    for (i,j,k) in sorted(cubes15,key=lambda c:(-c[1],c[2],c[0])):t+=cube3(i,j,k,s=.55,dx=.23,dy=.17)
    dessin('sol-15',t,'Le cube 3 sur 3 sur 3 : coins, arêtes, centres de faces et cube central.')
    META['sol-15']={'type':'assemblage','cubes':27}
    cells=[(0,0),(1,0),(2,0),(3,0),(0,1),(0,-1)]
    t=patron([(c,r+1) for c,r in cells],s=.7)
    t=r''
    t+=r'\draw[geoTrait](0,.7)rectangle(1.4,1.6);\draw[geoTrait](1.4,.7)rectangle(2.1,1.6);\draw[geoTrait](2.1,.7)rectangle(3.5,1.6);\draw[geoTrait](3.5,.7)rectangle(4.2,1.6);'
    t+=r'\draw[geoTrait](0,1.6)rectangle(1.4,2.3);\draw[geoTrait](0,0)rectangle(1.4,.7);'
    t+=r'\node[font=\tiny]at(.7,1.15){devant};\node[font=\tiny]at(2.8,1.15){derrière};\node[font=\tiny]at(.7,1.95){dessus};\node[font=\tiny]at(.7,.35){dessous};'
    dessin('cours-patron-pave',t,'Un patron du pavé : six rectangles, identiques deux à deux, aux bords compatibles.')
    META['cours-patron-pave']={'type':'libre'}

# ================================================================= données et hasard
def statistiques():
    circulaire('cours-circulaire',[2,1,1],['moitié','quart','quart'],leg='La moitié du disque représente la moitié du total ; chaque quart, un quart.')
    barres_diag('don-3',['lun','mar','mer','jeu','ven'],[15,20,25,35,30],5,leg='Livres empruntés chaque jour ; une graduation vaut 5.')
    courbe_fig('don-4',list(range(1,13)),[3,4,7,11,15,19,23,22,18,13,8,4],[(1,'J'),(2,'F'),(3,'M'),(4,'A'),(5,'M'),(6,'J'),(7,'J'),(8,'A'),(9,'S'),(10,'O'),(11,'N'),(12,'D')],5,leg='Températures moyennes mensuelles, en degrés Celsius.')
    circulaire('don-5',[2,1,1],['plat A','plat B','plat C'],leg='Soixante élèves en tout : la moitié pour A, un quart pour B, un quart pour C.')
    barres_diag('don-6',['foot','danse','judo','natation'],[12,9,5,4],2,sol=True,leg='Le diagramme à construire figure en vert ; une graduation vaut 2.')
    t=r'\draw[otMuted,->](0,0)--(7.6,0)node[below left,font=\tiny]{semaine};\draw[otMuted,->](0,0)--(0,4.4)node[above,font=\tiny]{taille (cm)};'
    for v in range(1,6):t+=rf'\draw[otRule!80,line width=.3pt]({v*1.35},0)--({v*1.35},4.0);\node[below,font=\tiny]at({v*1.35},0){{{v}}};'
    for v in [10,20,30,40]:t+=rf'\draw[otRule!80,line width=.3pt](0,{v*.1})--(7.0,{v*.1});\node[left,font=\tiny]at(0,{v*.1}){{{v}}};'
    for (a,m) in [(1,8),(2,14),(3,18),(4,30),(5,38)]:t+=rf'\fill[otNavy]({a*1.35},{m*.1})circle(1.7pt);'
    dessin('don-8',t,'Chaque point donne la taille du plant à une semaine donnée.')
    META['don-8']={'type':'points','donnees':[(1,8),(2,14),(3,18),(4,30),(5,38)]}
    courbe_fig('don-10',[8,10,12,14,16,18],[6,20,48,58,70,76],[(8,'8 h'),(10,'10 h'),(12,'12 h'),(14,'14 h'),(16,'16 h'),(18,'18 h')],10,
        leg='Pains vendus depuis l’ouverture, en cumulé : 48 à midi, 76 à la fermeture.',marks=[('48',12,48),('76',18,76)])
    barres_diag('don-11',['CP','CE1','CE2'],[22,26,24],2,wrong=(1,22),leg='Une barre contredit le tableau ; la correction figure en vert.')
    t=r'\begin{scope}[scale=.78]'
    t+=r'\draw[otMuted,->](0,0)--(6.6,0);\draw[otMuted,->](0,0)--(0,3.4);'
    xs=list(range(1,13));ys=[3,4,7,11,15,19,23,22,18,13,8,4]
    for x,y in zip(xs,ys):t+=rf'\fill[otNavy]({x*.5},{y*.12:.2f})circle(1.1pt);'
    t+=r'\draw[otNavy,line width=.8pt] '+' -- '.join(f'({x*.5},{y*.12:.2f})' for x,y in zip(xs,ys))+';'
    t+=r'\node[below,font=\tiny]at(3.5,-.05){températures (courbe)};'
    t+=r'\end{scope}\begin{scope}[shift={(6.4,0)},scale=.78]'
    pr=[55,48,45,50,60,40,18,25,52,66,70,62]
    t+=r'\draw[otMuted,->](0,0)--(6.6,0);\draw[otMuted,->](0,0)--(0,3.4);'
    for i,v in enumerate(pr):t+=rf'\fill[otNavy!35]({i*.5+.1},0)rectangle({i*.5+.4},{v*.045:.2f});'
    t+=r'\node[below,font=\tiny]at(3.3,-.05){précipitations (barres)};\end{scope}'
    dessin('don-13',t,'Deux documents pour la même ville : température en courbe, pluie en barres, mois par mois.')
    META['don-13']={'type':'libre'}

def probabilites():
    urne('pro-2',['R','R','V','V','V','N','N','N','N','N'],leg='Dix boules indiscernables : deux rouges, trois vertes, cinq noires.')
    t=roue('',[45]*8,['1','2','3','4','5','6','7','8'],colors=['otNavy!25']*8)+r'\node[below,font=\tiny]at(0,-1.9){roue A};'
    t+=roue('',[180,90,45,45],['1','2','3','4'],colors=['otOrange!40','otNavy!25','otGreen!35','otNavy!12'],shift=4.6)+r'\node[below,font=\tiny]at(4.6,-1.9){roue B};'
    dessin('pro-4',t,'Huit secteurs identiques pour A ; des secteurs inégaux pour B : seules les issues de A sont équiprobables.')
    META['pro-4']={'type':'secteurs','angles':[180,90,45,45],'roue_a':[45]*8}
    arbre2('pro-7',2,2,['P','F'],['P','F'],leg='Deux pièces : quatre chemins équiprobables, PF et FP compris.',sol_idx=(1,2))
    t=grille(6,6)
    for a in range(6):
        for b in range(6):
            if a+b+2==7:t+=rf'\fill[otGreen!45]({b},{5-a})rectangle({b+1},{6-a});'
    t+=grille(6,6)
    for k in range(6):
        t+=rf'\node[font=\tiny]at({k+.5},6.3){{{k+1}}};\node[font=\tiny]at(-.3,{5-k+.5}){{{k+1}}};'
    dessin('pro-8',rf'\begin{{scope}}[scale=.52]{t}\end{{scope}}','Les 36 cases du tableau des deux dés ; les sommes égales à 7 sont en vert.')
    META['pro-8']={'type':'cellules','aires':[6]}
    arbre2('pro-11',2,2,['R','B'],['R','B'],leg='Tirage avec remise : quatre chemins, RB et BR donnent deux couleurs différentes.',sol_idx=(1,2))
    arbre2('cours-arbre',2,2,['P','F'],['P','F'],leg='L’arbre recense les issues : deux branches, puis deux branches au bout de chacune.')

def annexes():
    t=''
    for i in range(8):t+=rf'\fill[otNavy!28]({i*.9:.3f},0)rectangle({i*.9+.9:.3f},.8);' if i<3 else ''
    t+=r'\fill[otGreen!45](2.7,0)rectangle(4.5,.8);\draw[geoTrait](0,0)rectangle(7.2,.8);'
    for i in range(1,8):t+=rf'\draw[geoTrait]({i*.9:.3f},0)--({i*.9:.3f},.8);'
    t+=r'\node[below,font=\tiny]at(1.35,-.05){3 huitièmes};\node[below,font=\tiny]at(3.6,-.05){2 huitièmes};'
    dessin('preuve-fractions',t,'Trois huitièmes puis deux huitièmes : cinq parts identiques en tout.')
    META['preuve-fractions']={'type':'libre'}

def write_all(root):
    for f in [nombres,fractions,grandeurs,geometrie,triangles,symetries,solides,statistiques,probabilites,annexes]:f()
    out=root/'figures';out.mkdir(exist_ok=True)
    for name,data in FIGURES.items():
        content=data['tex']+r'\par\vspace{1.5mm}{\otRegular\fontsize{8}{10}\selectfont\color{otMuted}'+data['legende']+'\\par}\n'
        (out/(name+'.tex')).write_text(content,encoding='utf8')

if __name__=='__main__':
    write_all(Path(__file__).resolve().parent)
    print(len(FIGURES),'figures écrites')
