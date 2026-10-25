"""Figures vectorielles du CM1, avec réponses conditionnelles et métadonnées de contrôle."""
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

# ---------------------------------------------------------------- demi-droites
def droiteg(nom,lo,hi,pas,labels,points=(),sol=(),minor=None,leg='Les graduations sont régulières ; lire la valeur d’un intervalle avant les positions.'):
    sx=9.0/(hi-lo)
    t=rf'\begin{{scope}}[x={sx}cm]'
    t+=rf'\draw[otMuted,->](0,0)--({hi-lo+0.3/sx},0);'
    if minor:
        k=0
        while lo+k*minor<=hi+1e-9:
            v=lo+k*minor-lo
            t+=rf'\draw[otMuted,line width=.5pt]({v},-.06)--({v},.06);';k+=1
    k=0
    while lo+k*pas<=hi+1e-9:
        v=lo+k*pas-lo
        t+=rf'\draw[otMuted,line width=.9pt]({v},-.1)--({v},.1);';k+=1
    for val,txt in labels:
        t+=rf'\node[below,font=\scriptsize]at({val-lo},-.12){{$ {txt} $}};'
    for lab,val in points:t+=dotpt(val-lo,0,lab,'above')
    if sol:t+=r'\geoSolution{'+''.join(dotpt(v-lo,0,l,'above','otGreenDark') for l,v in sol)+'}'
    dessin(nom,t+r'\end{scope}',leg)
    META[nom]={'type':'droite','bornes':[lo,hi],'points':[v for _,v in points],'solutions':[v for _,v in sol]}

# ---------------------------------------------------------------- fractions
def bande(nom,n,fill=0,solfill=0,w=7.2,h=.85,leg='La bande est partagée en parts égales.',marks=True):
    cw=w/n
    t=''
    for i in range(fill):t+=rf'\fill[otNavy!28]({i*cw:.3f},0)rectangle({(i+1)*cw:.3f},{h});'
    t+=r'\geoSolution{'+''.join(rf'\fill[otGreen!45]({i*cw:.3f},0)rectangle({(i+1)*cw:.3f},{h});' for i in range(fill,fill+solfill))+'}'
    t+=rf'\draw[geoTrait](0,0)rectangle({w},{h});'
    if marks:
        for i in range(1,n):t+=rf'\draw[geoTrait]({i*cw:.3f},0)--({i*cw:.3f},{h});'
    dessin(nom,t,leg)
    META[nom]={'type':'bande','parts':n,'remplies':fill,'sol':solfill}
def disque_parts(nom,n,fill,cx=0,extra='',leg='Le disque est partagé en parts égales.',r=1.35):
    t=''
    for i in range(n):
        a0=90+i*360/n;a1=90+(i+1)*360/n
        f='otNavy!28' if i<fill else 'white'
        t+=rf'\filldraw[draw=otNavy,line width=.8pt,fill={f}]({cx},0)--({a0}:{r})++({cx},0)arc({a0}:{a1}:{r})--cycle;'
    # Les arcs tracés depuis un centre décalé exigent un repère par disque.
    t=rf'\begin{{scope}}[shift={{({cx},0)}}]'
    for i in range(n):
        a0=90+i*360/n;a1=90+(i+1)*360/n
        f='otNavy!28' if i<fill else 'white'
        t+=rf'\filldraw[draw=otNavy,line width=.8pt,fill={f}](0,0)--({a0}:{r})arc({a0}:{a1}:{r})--cycle;'
    t+=extra+r'\end{scope}'
    return t
def horloge(cx,h,m,sol=False,r=1.45):
    t=rf'\begin{{scope}}[shift={{({cx},0)}}]\draw[geoTrait](0,0)circle({r});'
    for k in range(12):
        a=90-k*30
        t+=rf'\draw[otMuted]({a}:{r*.92})--({a}:{r});'
        t+=rf'\node[font=\tiny]at({a}:{r*.78}){{{12 if k==0 else k}}};'
    ah=90-(h%12)*30-m*0.5;am=90-m*6
    hands=rf'\draw[line width=1.6pt,{"otGreenDark" if sol else "otNavy"}](0,0)--({ah}:{r*.5});\draw[line width=1.1pt,{"otGreenDark" if sol else "otNavy"}](0,0)--({am}:{r*.8});\fill[{"otGreenDark" if sol else "otNavy"}](0,0)circle(1.5pt);'
    t+=(r'\geoSolution{'+hands+'}' if sol else hands)
    return t+r'\end{scope}'

# ---------------------------------------------------------------- données
def barres_diag(nom,cats,vals,step,sol=False,wrong=None,unit=4.2,leg=''):
    m=max(vals+( [wrong[1]] if wrong else []))
    sy=unit/m;w=.62;gap=1.15
    t=rf'\draw[otMuted,->](-.3,0)--({len(cats)*gap+.4},0);\draw[otMuted,->](0,-.0)--(0,{unit+.5});'
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
def courbe_fig(nom,xs,ys,xlabels,step,unit=(8.6,4.0),leg='',second=None,names=None,ligne=None):
    xmax=max(xs);m=max(ys+(second or []))
    sx=unit[0]/xmax;sy=unit[1]/m
    t=rf'\draw[otMuted,->](0,0)--({unit[0]+.4},0);\draw[otMuted,->](0,0)--(0,{unit[1]+.5});'
    v=step
    while v<=m+1e-9:
        t+=rf'\draw[otRule!80,line width=.3pt](0,{v*sy:.3f})--({unit[0]+.2},{v*sy:.3f});\node[left,font=\tiny]at(0,{v*sy:.3f}){{{v}}};'
        v+=step
    for xv,xl in xlabels:
        t+=rf'\draw[otRule!80,line width=.3pt]({xv*sx:.3f},0)--({xv*sx:.3f},{unit[1]});\node[below,font=\tiny]at({xv*sx:.3f},0){{{xl}}};'
    if ligne is not None:
        t+=rf'\draw[otOrange,line width=.7pt,dashed](0,{ligne*sy:.3f})--({unit[0]},{ligne*sy:.3f});'
    def trace(data,color):
        pts=' -- '.join(f'({x*sx:.3f},{y*sy:.3f})' for x,y in zip(xs,data))
        s=rf'\draw[{color},line width=1pt] '+pts+';'
        for x,y in zip(xs,data):s+=rf'\fill[{color}]({x*sx:.3f},{y*sy:.3f})circle(1.4pt);'
        return s
    t+=trace(ys,'otNavy')
    if second:
        t+=trace(second,'otGreenDark')
        if names:t+=rf'\node[right,font=\tiny,otNavy]at({xs[-1]*sx:.3f},{ys[-1]*sy:.3f}){{{names[0]}}};\node[right,font=\tiny,otGreenDark]at({xs[-1]*sx:.3f},{second[-1]*sy:.3f}){{{names[1]}}};'
    dessin(nom,t,leg or 'Chaque point se lit avec les deux axes ; la ligne montre l’évolution.')
    META[nom]={'type':'courbe','valeurs':list(ys),'second':second or []}

# ---------------------------------------------------------------- solides
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
def patron(nom,cells,s=.95,labels=None,sol_cells=(),bad_cells=(),leg='Patron à plier le long des arêtes communes.',shift=0):
    t=rf'\begin{{scope}}[shift={{({shift},0)}}]'
    for (c,r) in cells:
        t+=rf'\draw[geoTrait]({c*s:.3f},{r*s:.3f})rectangle({(c+1)*s:.3f},{(r+1)*s:.3f});'
    for (c,r,lab) in (labels or []):
        t+=rf'\node[font=\small]at({(c+.5)*s:.3f},{(r+.5)*s:.3f}){{{lab}}};'
    if sol_cells:
        t+=r'\geoSolution{'+''.join(rf'\filldraw[draw=otGreenDark,fill=otGreen!30,line width=.8pt]({c*s:.3f},{r*s:.3f})rectangle({(c+1)*s:.3f},{(r+1)*s:.3f});'+(rf'\node[otGreenDark,font=\small]at({(c+.5)*s:.3f},{(r+.5)*s:.3f}){{{lab}}};' if lab else '') for (c,r,lab) in sol_cells)+'}'
    if bad_cells:
        t+=r'\geoSolution{'+''.join(rf'\draw[otOrange,line width=.8pt,dashed]({c*s:.3f},{r*s:.3f})rectangle({(c+1)*s:.3f},{(r+1)*s:.3f});\draw[otOrange,line width=.8pt]({c*s+.18:.3f},{r*s+.18:.3f})--({(c+1)*s-.18:.3f},{(r+1)*s-.18:.3f})({(c+1)*s-.18:.3f},{r*s+.18:.3f})--({c*s+.18:.3f},{(r+1)*s-.18:.3f});' for (c,r) in bad_cells)+'}'
    return t+r'\end{scope}'

# ---------------------------------------------------------------- symétrie
def mirror(p,axis):
    o,v=axis
    return (2*v-p[0],p[1]) if o=='v' else (p[0],2*v-p[1])
def symfig(nom,chains,axis,gw,gh,points=None,leg='Quadrillage de principe ; l’axe est tracé en tirets.',cells=None,sol_cells=None,nosol=False,extra=''):
    o,v=axis
    t=grille(gw,gh)
    t+=(rf'\draw[otOrange,dashed,line width=1pt]({v},-.25)--({v},{gh+.25});' if o=='v' else rf'\draw[otOrange,dashed,line width=1pt](-.25,{v})--({gw+.25},{v});')
    orig=[];imgs=[]
    for ch in chains:
        t+=poly(ch,'geoTrait',close=len(ch)>2)
        orig+=list(ch)
    for c,r in (cells or []):
        t+=rf'\fill[otNavy!40]({c},{r})rectangle({c+1},{r+1});'
    sol=''
    for ch in chains:
        mi=[mirror(p,axis) for p in ch]
        imgs+=mi
        sol+=poly(mi,'geoReponse',close=len(ch)>2)
    for c,r in (sol_cells or []):
        sol+=rf'\fill[otGreen!50]({c},{r})rectangle({c+1},{r+1});'
    for lab,x,y in (points or []):
        t+=dotpt(x,y,lab,'above left')
        mx,my=mirror((x,y),axis)
        sol+=dotpt(mx,my,lab+"'",'above right','otGreenDark')
        orig.append((x,y));imgs.append((mx,my))
    if not nosol:t+=r'\geoSolution{'+sol+'}'
    dessin(nom,t+extra,leg)
    META[nom]={'type':'symetrie','axe':[o,v],'originaux':orig,'images':imgs,'grille':[gw,gh]}

def roue(nom,angles,labels,colors=None,leg='La roue est lancée ; le repère fixe désigne le secteur gagnant.'):
    assert sum(angles)==360
    cols=colors or ['otNavy!30','otGreen!40','otOrange!45','otNavy!12','otGreen!20','otOrange!25','otNavy!45','otOrange!60']
    t='';start=90
    for a,lab,col in zip(angles,labels,cols):
        end=start+a;mid=(start+end)/2
        t+=rf'\filldraw[draw=white,line width=.8pt,fill={col}](0,0)--({start}:1.6)arc({start}:{end}:1.6)--cycle;'
        t+=rf'\node[font=\tiny]at({mid}:1.05){{{lab}}};'
        start=end
    t+=r'\draw[otNavy,line width=.9pt](0,0)circle(1.6);\fill[otInk](90:1.78)--(84:1.95)--(96:1.95)--cycle;'
    dessin(nom,t,leg)
    META[nom]={'type':'secteurs','angles':list(angles)}
def urne(nom,items,leg='Les boules sont indiscernables au toucher.'):
    t=r'\draw[otMuted,line width=.9pt](-.5,2.0)--(-.5,-.55)--(4.6,-.55)--(4.6,2.0);'
    for i,lab in enumerate(items):
        color={'R':'otOrange!60','B':'otNavy!32','V':'otGreen!55','N':'otInk!55'}[lab[0]]
        t+=rf'\node[circle,draw=otMuted,fill={color},minimum size=6.6mm,font=\scriptsize]at({i%4*1.25},{1.25-i//4*1.05}){{{lab}}};'
    dessin(nom,t,leg)
    META[nom]={'type':'urne','items':list(items)}

# ================================================================= chapitres 1 à 5
def nombres():
    droiteg('cours-droite-mille',45000,46000,100,[(45000,r'45\,000'),(45500,r'45\,500'),(46000,r'46\,000')],
        points=[(r'45\,670',45670)],leg='Chaque intervalle vaut 100 : le point repère 45 670, entre 45 600 et 45 700.')
    droiteg('num-8',24000,28000,1000,[(24000,r'24\,000'),(25000,r'25\,000'),(26000,r'26\,000'),(27000,r'27\,000'),(28000,r'28\,000')],
        points=[('A',25000),('B',26500),('C',27500)],minor=500)
    # Schémas en barres (modèles de problèmes).
    def barres_modele(nom,total,parts,leg,wsol=None):
        w=8.0;tot=sum(p[1] for p in parts)
        t=rf'\draw[geoTrait](0,1.15)rectangle({w},1.85);\node[font=\small]at({w/2},1.5){{{total}}};'
        x=0.0
        for lab,val,known in parts:
            pw=w*val/tot
            t+=rf'\draw[geoTrait]({x:.3f},0)rectangle({x+pw:.3f},.7);'
            mid=x+pw/2
            if known:t+=rf'\node[font=\small]at({mid:.3f},.35){{{lab}}};'
            else:t+=rf'\node[font=\small]at({mid:.3f},.35){{{answer(wsol)}}};'
            x+=pw
        t+=rf'\draw[otMuted,<->](0,-.3)--({w},-.3);\node[below,font=\tiny]at({w/2},-.35){{même longueur totale : le tout}};'
        dessin(nom,t,leg)
        META[nom]={'type':'modele','total':tot}
    barres_modele('cours-barres','258 élèves',[('136 filles',136,True),('? garçons',122,False)],
        'Le tout (258) est la barre du haut ; les parties s’alignent dessous : la partie manquante se calcule par une soustraction.',wsol='122')
    barres_modele('barres-9','850 places',[('512',512,True),('218',218,True),('?',120,False)],
        'Les parties connues et la partie cherchée recomposent le tout.',wsol='120')
    t=rf'\draw[geoTrait](0,1.15)rectangle(6.5,1.85);\node[font=\small]at(3.25,1.5){{Nina : 325}};'
    t+=rf'\draw[geoTrait](0,0)rectangle(5.14,.7);\node[font=\small]at(2.57,.35){{Marco : {answer("257")}}};'
    t+=r'\draw[otMuted,<->](5.14,.35)--(6.5,.35);\node[below,font=\tiny]at(5.8,.1){68 de plus pour Nina};'
    t+=r'\draw[otRule!80,line width=.4pt,dashed](5.14,-.15)--(5.14,2.0);'
    dessin('barres-12',t,'Comparer, c’est aligner les deux barres : l’écart de 68 se lit entre leurs extrémités.')
    META['barres-12']={'type':'modele','total':325}
    # Produit : rectangle décomposé.
    t=grille(12,4)
    t+=r'\fill[otNavy!22](0,0)rectangle(10,4);\fill[otGreen!35](10,0)rectangle(12,4);'
    t+=grille(12,4)
    t+=r'\draw[geoTrait](0,0)rectangle(12,4);\draw[geoTrait](10,0)--(10,4);'
    t+=r'\draw[otMuted,<->](0,-.35)--(10,-.35);\node[below,font=\tiny]at(5,-.4){10};'
    t+=r'\draw[otMuted,<->](10,-.35)--(12,-.35);\node[below,font=\tiny]at(11,-.4){2};'
    t+=r'\draw[otMuted,<->](-.35,0)--(-.35,4);\node[left,font=\tiny]at(-.4,2){4};'
    t+=r'\node[font=\small]at(5,2){$4\times10=40$};\node[font=\small]at(11,2){$4\times2=8$};'
    dessin('cours-produit',rf'\begin{{scope}}[scale=.62]{t}\end{{scope}}','Le rectangle montre le produit : 4 rangées de 12 carreaux, soit 4 × 10 plus 4 × 2.')
    META['cours-produit']={'type':'libre'}
    # Programmes de calcul en blocs.
    dessin('prog-cours',pile(lignes(SCRIPTS[1])),'Le programme se lit de haut en bas ; chaque étape agit sur le nombre obtenu.')
    dessin('prog-4',pile(lignes(SCRIPTS[1])),'Suivre les étapes dans l’ordre, en notant le nombre obtenu après chacune.')
    META['prog-cours']={'type':'script','numero':1};META['prog-4']={'type':'script','numero':1}
    # Suites de motifs.
    def motif_carres(nom,etapes,leg):
        t='';x0=0.0
        for e in etapes:
            t+=rf'\node[below,font=\tiny]at({x0+e*.45:.2f},-.15){{étape {etapes.index(e)+1}}};'
            for i in range(e):
                t+=rf'\draw[geoTrait]({x0+i*.9:.2f},0)rectangle({x0+i*.9+.9:.2f},.9);'
            x0+=e*.9+.9
        dessin(nom,t,leg)
        META[nom]={'type':'motifs','etapes':etapes}
    motif_carres('motifs-13',[1,2,3],'À chaque étape, un carré de plus : 4 allumettes, puis 7, puis 10. Chaque nouveau carré partage une allumette.')
    t='';x0=0.0
    for n,e in enumerate([1,2,3],1):
        cells=[(0,0)]+[(k,0) for k in range(-e,e+1)]+[(0,k) for k in range(-e,e+1)]
        cells=sorted(set([(0,0)]+[(k,0) for k in range(-e,e+1)]+[(0,k) for k in range(-e,e+1)]))
        for (cx,cy) in cells:
            t+=rf'\draw[geoTrait]({x0+cx*.42:.2f},{cy*.42:.2f})rectangle({x0+cx*.42+.42:.2f},{cy*.42+.42:.2f});'
        t+=rf'\node[below,font=\tiny]at({x0+.2:.2f},{-e*.42-.2:.2f}){{étape {n}}};'
        x0+=e*.42*2+1.5
    dessin('motifs-14',t,'La croix gagne quatre carreaux à chaque étape : un au bout de chaque branche.')
    META['motifs-14']={'type':'motifs','etapes':[5,9,13]}

# ================================================================= chapitres 6 à 10
def fractions():
    dessin('cours-parts',disque_parts('',4,3,cx=1.6)+bandefrag(5.2,0,8,3),'Trois quarts du disque et trois huitièmes de la bande : le dénominateur nomme le partage, le numérateur compte les parts.')
    META['cours-parts']={'type':'libre'}
    dessin('frac-1',disque_parts('',8,3,cx=0),'Le disque est partagé en parts égales ; les parts colorées se comptent depuis le haut.')
    META['frac-1']={'type':'libre'}
    bande('frac-2',5,0,2,leg='La bande compte cinq cases égales ; la réponse coloriée figure en vert au corrigé.')
    t=r'\draw[geoTrait](0,0)rectangle(6,1.3);\draw[geoTrait](3,0)--(3,1.3)(3,0)--(3,1.3);\draw[geoTrait](3,0)--(3,1.3);\draw[geoTrait](4.5,0)--(4.5,1.3);'
    t+=r'\fill[otNavy!28](0,0)rectangle(3,1.3);\draw[geoTrait](0,0)rectangle(6,1.3);\draw[geoTrait](3,0)--(3,1.3)(4.5,0)--(4.5,1.3);'
    dessin('frac-4',t,'Les trois morceaux n’ont pas la même taille : le morceau coloré couvre la moitié de la figure.')
    META['frac-4']={'type':'libre'}
    dessin('frac-5',disque_parts('',4,4,cx=0)+disque_parts('',4,1,cx=3.4),'Deux disques identiques partagés en quarts : cinq quarts sont colorés en tout.')
    META['frac-5']={'type':'libre'}
    t=''
    for i in range(12):
        a0=90+i*30;a1=120+i*30
        f='otNavy!35' if i<5 else ('otNavy!18' if i<9 else 'white')
        t+=rf'\filldraw[draw=otNavy,line width=.8pt,fill={f}](0,0)--({a0}:1.5)arc({a0}:{a1}:1.5)--cycle;'
    dessin('frac-11',t,'Les parts sombres ont été mangées le midi, les parts claires le soir ; les parts blanches restent.')
    META['frac-11']={'type':'libre'}
    bande('frac-12',20,0,5,w=8.6,h=.6,leg='La frise compte vingt carreaux identiques ; le quart colorié figure en vert au corrigé.')
    droiteg('cours-droite-fractions',0,2,0.25,[(0,'0'),(1,'1'),(2,'2')],points=[(r'\frac74',1.75)],
        leg='L’unité est partagée en quarts : le point 7/4 se place trois pas après 1.')
    droiteg('fd-1',0,2,0.25,[(0,'0'),(1,'1'),(2,'2')],points=[('A',0.75),('B',1.75)],
        leg='L’unité est partagée en quarts ; chaque pas vaut un quart.')
    droiteg('fd-2',0,2,1/3,[(0,'0'),(1,'1'),(2,'2')],sol=[('C',2/3),('D',5/3)],
        leg='L’unité est partagée en tiers ; les points demandés figurent en vert au corrigé.')
    droiteg('fd-9',0,2,0.2,[(0,'0'),(1,'1'),(2,'2')],points=[('E',0.8)],sol=[('F',1.4)],
        leg='L’unité est partagée en cinquièmes ; la position de F figure en vert au corrigé.')
    t=bandefrag(0,1.1,3,1)+bandefrag(0,0,4,1)
    t+=r'\draw[otMuted,dashed](0,-.2)--(0,2.1)(7.2,-.2)--(7.2,2.1);'
    dessin('fd-10',t,'Deux bandes de même longueur : partagée en 3 en haut, en 4 en bas. Les parts en tiers sont plus grandes.')
    META['fd-10']={'type':'libre'}
    u=2.6
    t=rf'\draw[geoTrait](0,1.3)rectangle({u},1.9);'
    for k in range(1,4):t+=rf'\draw[otMuted]({k*u/4:.3f},1.3)--({k*u/4:.3f},1.9);'
    t+=rf'\node[right,font=\tiny]at({u+.1},1.6){{bande unité pliée en quarts}};'
    t+=rf'\draw[otNavy,line width=1.3pt](0,.5)--({2.75*u:.3f},.5);'
    t+=rf'\fill[otNavy](0,.5)circle(1.4pt)({2.75*u:.3f},.5)circle(1.4pt);'
    for k in range(1,3):t+=rf'\draw[otMuted,dashed]({k*u:.3f},.3)--({k*u:.3f},.7);'
    dessin('fd-11',t,'Reporter la bande unité le long du segment : deux unités entières, puis des quarts.')
    META['fd-11']={'type':'libre'}
    t=bandefrag(0,1.1,2,1)+bandefrag(0,0,4,2)
    dessin('fd-14',t,'Une part sur deux en haut, deux parts sur quatre en bas : les longueurs prises coïncident.')
    META['fd-14']={'type':'libre'}
    droiteg('cours-droite-dixiemes',2,3,0.1,[(2,'2'),(3,'3')],points=[(r'2+\frac{4}{10}',2.4)],
        leg='Chaque pas vaut un dixième : quatre pas après 2.')
    droiteg('dec-2',2,3,0.1,[(2,'2'),(3,'3')],points=[('A',2.4),('B',2.8)],
        leg='L’unité est partagée en dixièmes.')
    t=grille(10,10)
    k=0
    for r in range(10):
        for c in range(10):
            if k<37:t+=rf'\fill[otNavy!30]({c},{9-r})rectangle({c+1},{10-r});';k+=1
    t+=grille(10,10)+r'\draw[geoTrait](0,0)rectangle(10,10);'
    dessin('dec-13',rf'\begin{{scope}}[scale=.42]{t}\end{{scope}}','La grille compte cent cases égales : chaque case vaut un centième de la grille.')
    META['dec-13']={'type':'libre'}
    droiteg('cours-droite-decimaux',2.4,2.5,0.01,[(2.4,r'2{,}4'),(2.45,r'2{,}45'),(2.5,r'2{,}5')],
        leg='Entre 2,4 et 2,5, la graduation en centièmes fait apparaître les nombres intermédiaires.')
    droiteg('dec9-6',5,6,0.1,[(5,'5'),(6,'6')],points=[('A',5.3),('B',5.8)],sol=[('C',5.45)],minor=0.05,
        leg='Les grandes graduations valent un dixième ; C se place au milieu d’un pas, en vert au corrigé.')

def bandefrag(x0,y0,n,fill,w=7.2,h=.8):
    cw=w/n;t=''
    for i in range(fill):t+=rf'\fill[otNavy!28]({x0+i*cw:.3f},{y0})rectangle({x0+(i+1)*cw:.3f},{y0+h});'
    t+=rf'\draw[geoTrait]({x0},{y0})rectangle({x0+w},{y0+h});'
    for i in range(1,n):t+=rf'\draw[geoTrait]({x0+i*cw:.3f},{y0})--({x0+i*cw:.3f},{y0+h});'
    return t

# ================================================================= grandeurs
def grandeurs():
    t=poly([(0,0),(3.4,0),(4.4,1.9),(1.7,2.9),(-.7,1.7)])
    for (a,b,lab) in [((0,0),(3.4,0),'3 cm'),((3.4,0),(4.4,1.9),r'2{,}1 cm'),((4.4,1.9),(1.7,2.9),r'2{,}9 cm'),((1.7,2.9),(-.7,1.7),r'2{,}7 cm'),((-.7,1.7),(0,0),r'1{,}8 cm')]:
        mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
        cx,cy=1.76,1.3
        dx,dy=mx-cx,my-cy;n=(dx*dx+dy*dy)**.5
        t+=rf'\node[font=\tiny]at({mx+dx/n*.42:.3f},{my+dy/n*.32:.3f}){{{lab}}};'
    dessin('cours-perimetre',t,'Le périmètre est la longueur du contour : la somme des cinq côtés du polygone.')
    META['cours-perimetre']={'type':'libre'}
    t=poly([(0,0),(3,0),(3.9,2.1),(1.2,2.6)])
    for (a,b,lab) in [((0,0),(3,0),'3 cm'),((3,0),(3.9,2.1),r'4{,}5 cm'),((3.9,2.1),(1.2,2.6),r'2{,}5 cm'),((1.2,2.6),(0,0),'4 cm')]:
        mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
        cx,cy=2.0,1.2;dx,dy=mx-cx,my-cy;n=(dx*dx+dy*dy)**.5
        t+=rf'\node[font=\tiny]at({mx+dx/n*.45:.3f},{my+dy/n*.33:.3f}){{{lab}}};'
    dessin('per-5',t,'Schéma à main levée : seules les mesures écrites font foi.')
    META['per-5']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)rectangle(2.6,2.6);\node[below,font=\small]at(1.3,0){7 cm};'
    for (x1,y1,x2,y2) in [(1.2,-.08,1.4,.08),(1.2,2.52,1.4,2.68),(-.08,1.2,.08,1.4),(2.52,1.2,2.68,1.4)]:
        t+=rf'\draw[otNavy]({x1},{y1})--({x2},{y2});'
    dessin('per-6',t,'Les quatre côtés du carré ont la même longueur, codée par les petits traits.')
    META['per-6']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)rectangle(4.6,2.0);\node[below,font=\small]at(2.3,0){8 cm};\node[left,font=\small]at(0,1){3{,}5 cm};'
    dessin('per-7',t,'Rectangle de principe : les mesures écrites font foi.')
    META['per-7']={'type':'libre'}
    pts=[(0,0),(4.8,0),(4.8,1.2),(1.8,1.2),(1.8,3.6),(0,3.6)]
    t=poly(pts)
    lab=[('8 cm',(2.4,-.32)),('2 cm',(5.15,.6)),('5 cm',(3.3,1.52)),(answer('4 cm'),(2.22,2.4)),(answer('3 cm'),(.9,3.92)),('6 cm',(-.5,1.8))]
    for s,(x,y) in lab:t+=rf'\node[font=\tiny]at({x},{y}){{{s}}};'
    dessin('per-10',t,'Figure en L : deux mesures se déduisent des autres avant le calcul du contour.')
    META['per-10']={'type':'libre'}
    t=grille(9,3)+poly([(0,0),(5,0),(5,3),(0,3)])
    t+=poly([(6,0),(9,0),(9,1),(8,1),(8,2),(7,2),(7,3),(6,3)])
    t+=r'\node[below,font=\tiny]at(2.5,-.1){rectangle};\node[below,font=\tiny]at(7.5,-.1){escalier};'
    dessin('per-13',rf'\begin{{scope}}[scale=.8]{t}\end{{scope}}','Chaque carreau mesure 1 cm de côté ; suivre les contours en comptant les déplacements.')
    META['per-13']={'type':'libre'}
    t=r'\draw[otMuted,line width=1pt](-3.1,1.1)--(3.1,1.1);\draw[otMuted](0,1.1)--(0,1.5);\fill[otMuted](-.25,1.5)rectangle(.25,1.6);'
    t+=r'\draw[otMuted](-3.1,1.1)--(-3.1,.9)(3.1,1.1)--(3.1,.9);'
    t+=r'\draw[otNavy,line width=.9pt](-2.9,.9)--(-1.3,.9);\fill[otNavy!20](-2.75,.9)rectangle(-1.45,.3);\draw[otNavy](-2.75,.9)rectangle(-1.45,.3);\node[font=\tiny]at(-2.1,.6){farine};'
    t+=r'\draw[otNavy,line width=.9pt](1.3,.9)--(2.9,.9);'
    for i,m in enumerate(['500 g','200 g','50 g']):
        t+=rf'\fill[otOrange!40]({1.5+i*.5},.3)rectangle({1.9+i*.5},.9);\draw[otNavy]({1.5+i*.5},.3)rectangle({1.9+i*.5},.9);\node[below,font=\tiny]at({1.7+i*.5},.28){{{m}}};'
    dessin('mas-6',t,'La balance est en équilibre : les deux plateaux portent la même masse.')
    META['mas-6']={'type':'libre'}
    # Aires et angles.
    def cellfig(nom,shapes,gw,gh,leg,scale=.55):
        t=grille(gw,gh)
        for cells,col in shapes:
            for (c,r) in cells:t+=rf'\fill[{col}]({c},{r})rectangle({c+1},{r+1});'
        t+=grille(gw,gh)
        dessin(nom,rf'\begin{{scope}}[scale={scale}]{t}\end{{scope}}',leg)
        META[nom]={'type':'cellules','aires':[len(c) for c,_ in shapes]}
    cellfig('aa-1',[([(0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(0,2),(1,2)],'otNavy!35'),([(5,0),(6,0),(7,0),(5,1),(6,1),(5,2),(6,2)],'otGreen!40')],8,3,'Deux figures grisées sur le même quadrillage : compter les carreaux de chacune.')
    cellfig('aa-2',[([(0,0),(1,0),(0,1),(1,1),(0,2),(1,2),(2,2)],'otNavy!35')],4,3,'La figure en L se découpe en morceaux rectangulaires.')
    cellfig('aa-3',[([(0,0),(1,0),(2,0),(0,1),(1,1),(2,1)],'otNavy!35'),([(5,0),(5,1),(5,2),(6,0),(6,1),(6,2)],'otGreen!40')],8,3,'Deux formes différentes : compter les carreaux avant de conclure.')
    t=grille(5,4)+r'\fill[otNavy!30](1,1)rectangle(4,4);'+grille(5,4)+r'\draw[geoTrait](1,1)rectangle(4,4);\node[below,font=\tiny]at(2.5,.9){chaque carreau : 1 cm de côté};'
    dessin('aa-4',rf'\begin{{scope}}[scale=.62]{t}\end{{scope}}','Le rectangle couvre des carreaux d’un centimètre de côté : des centimètres carrés.')
    META['aa-4']={'type':'cellules','aires':[12]}
    def anglefig(nom,specs,leg,r=1.1):
        t=''
        for (x0,lab,a0,a1,named) in specs:
            t+=rf'\draw[geoTrait]({x0},0)--++({a0}:2.1);\draw[geoTrait]({x0},0)--++({a1}:1.7);'
            t+=rf'\draw[otGreenDark,line width=.7pt]([shift={{({x0},0)}}]{a0}:{r*.55})arc({a0}:{a1}:{r*.55});'
            if named:
                t+=rf'\fill[otNavy]({x0},0)circle(1.3pt);'
                for ang,l in named:t+=rf'\node[font=\scriptsize]at([shift={{({x0},0)}}]{ang}:{"2.35" if l not in "ABCDEF" or True else "1"}){{$ {l} $}};'
            t+=rf'\node[below,font=\small]at({x0},-.3){{$ {lab} $}};'
        dessin(nom,t,leg)
        META[nom]={'type':'angles','mesures':[abs(a1-a0) for _,_,a0,a1,_ in specs]}
    t=r'\draw[geoTrait](0,0)--(2.6,0);\draw[geoTrait](0,0)--(55:2.2);\fill[otNavy](0,0)circle(1.4pt);'
    t+=r'\node[below left,font=\small]at(0,0){$ B $};\node[right,font=\small]at(2.6,0){$ C $};\node[above,font=\small]at(55:2.2){$ A $};'
    t+=r'\draw[otGreenDark,line width=.7pt](0:.7)arc(0:55:.7);'
    dessin('aa-5',t,'L’angle est l’écartement entre les deux côtés issus du sommet B.')
    META['aa-5']={'type':'angles','mesures':[55]}
    anglefig('aa-6',[(0,'A',0,52,None),(4.2,'B',10,38,None),(8.0,'C',0,95,None)],'Trois angles à comparer : l’ouverture compte, pas la longueur des côtés dessinés.')
    pts=[(0,0),(3.1,0),(3.4,2.1),(0,2.3)]
    t=poly(pts)
    t+=r'\draw[otNavy](.28,0)--(.28,.28)--(0,.28);\draw[otNavy](0,2.02)--(.28,2.02)--(.28,2.3);'
    for (x,y),l,w in [((0,0),'A','below left'),((3.1,0),'B','below right'),((3.4,2.1),'C','above right'),((0,2.3),'D','above left')]:
        t+=rf'\node[{w},font=\small]at({x},{y}){{$ {l} $}};'
    dessin('aa-7',t,'Les petits carrés codent les angles droits trouvés avec l’équerre.')
    META['aa-7']={'type':'libre'}
    t=grille(4,3)
    t+=r'\fill[otNavy!35](0,0)rectangle(2,2);\fill[otNavy!35](2,0)--(3,0)--(2,1)--cycle;\fill[otNavy!35](2,1)--(3,0)--(3,1)--cycle;'
    t=grille(4,3)+r'\fill[otNavy!35](0,0)rectangle(2,2);\fill[otNavy!35](2,0)--(3,0)--(3,1)--cycle;\fill[otNavy!35](0,2)--(1,2)--(0,3)--cycle;'
    t+=grille(4,3)+r'\draw[geoTrait](0,0)--(3,0)--(3,1)--(2,1)--(2,0)(2,1)--(2,2)--(0,2)(0,2)--(0,3)--(1,2);\draw[geoTrait](0,0)--(0,2)(2,0)--(3,1);'
    t=grille(4,3)
    t+=r'\fill[otNavy!35](0,0)rectangle(2,2);\fill[otNavy!35](2,0)--(3,0)--(2,1)--cycle;\fill[otNavy!35](0,2)--(1,2)--(0,3)--cycle;'
    t+=r'\draw[geoTrait](0,3)--(0,0)--(3,0)--(2,1)--(2,2)--(1,2)--cycle;'
    dessin('aa-8',rf'\begin{{scope}}[scale=.62]{t}\end{{scope}}','La figure contient des carreaux entiers et des demi-carreaux triangulaires.')
    META['aa-8']={'type':'cellules','aires':[5]}
    t=grille(10,4)+poly([(0,0),(5,0),(5,1),(0,1)])+poly([(6,0),(9,0),(9,3),(6,3)])
    t+=r'\node[below,font=\tiny]at(2.5,-.1){5 sur 1};\node[below,font=\tiny]at(7.5,-.1){3 sur 3};'
    dessin('aa-9',rf'\begin{{scope}}[scale=.6]{t}\end{{scope}}','Deux rectangles sur le même quadrillage : comparer le tour, puis la surface.')
    META['aa-9']={'type':'cellules','aires':[5,9]}
    t=r'\draw[otMuted,dashed,line width=.9pt](0,0)--(2.2,0);\draw[otMuted,dashed,line width=.9pt](0,0)--(45:2.2);\node[below,font=\tiny]at(1.1,-.1){calque};'
    for x0,l,a in [(3.4,'D',30),(6.4,'E',45),(9.4,'F',70)]:
        t+=rf'\draw[geoTrait]({x0},0)--++(0:2.0);\draw[geoTrait]({x0},0)--++({a}:2.0);\node[below,font=\small]at({x0+.9},-.25){{$ {l} $}};'
    dessin('aa-10',t,'Le calque en tirets se superpose à l’un des trois angles : même sommet, mêmes côtés.')
    META['aa-10']={'type':'angles','mesures':[45,30,45,70]}
    cellfig('aa-11',[([(0,0),(1,0),(2,0),(3,0),(0,1),(1,1),(2,1),(3,1),(0,2),(1,2),(2,2),(3,2)],'otNavy!35'),([(5,0),(6,0),(7,0),(8,0),(9,0),(5,1),(6,1),(7,1),(8,1),(9,1)],'otGreen!40')],10,3,'Le plan du potager : chaque carreau représente un mètre carré. P à gauche, Q à droite.')
    t=grille(7,2)
    for c in range(7):
        t+=rf'\fill[otNavy!35]({c},0)--({c+1},0)--({c},1)--cycle;\fill[otGreen!40]({c},1)--({c+1},2)--({c},2)--cycle;'
        t+=rf'\draw[geoTrait]({c},0)--({c+1},0)--({c},1)--cycle;\draw[geoTrait]({c},1)--({c+1},2)--({c},2)--cycle;'
    dessin('aa-12',rf'\begin{{scope}}[scale=.62]{t}\end{{scope}}','Quatorze triangles identiques : chacun vaut un demi-carreau.')
    META['aa-12']={'type':'cellules','aires':[7,7]}
    t=grille(8,5)+r'\fill[otNavy!35](0,0)rectangle(2,2);'+r'\fill[otGreen!35](3,0)rectangle(7,4);'+grille(8,5)
    t+=r'\draw[geoTrait](0,0)rectangle(2,2);\draw[geoTrait](3,0)rectangle(7,4);\node[below,font=\tiny]at(1,-.1){côté 2};\node[below,font=\tiny]at(5,-.1){côté 4};'
    dessin('aa-13',rf'\begin{{scope}}[scale=.55]{t}\end{{scope}}','Le côté double, et chaque rangée double aussi : l’aire est multipliée par quatre.')
    META['aa-13']={'type':'cellules','aires':[4,16]}
    t=poly([(0,0),(3.2,0),(0,2.4)])
    t+=r'\draw[otNavy](.3,0)--(.3,.3)--(0,.3);'
    t+=r'\node[below left,font=\small]at(0,0){$ A $};\node[below right,font=\small]at(3.2,0){$ B $};\node[above,font=\small]at(0,2.4){$ C $};'
    dessin('aa-14',t,'Tester chaque sommet avec l’équerre : un seul angle est droit.')
    META['aa-14']={'type':'libre'}
    serp=[(0,0),(1,0),(2,0),(2,1),(2,2),(1,2),(0,2),(0,3),(0,4)]
    t=grille(9,5)
    for c,r in serp:t+=rf'\fill[otNavy!35]({c},{r})rectangle({c+1},{r+1});'
    for c,r in [(5,0),(6,0),(7,0)]+[(5,1),(6,1),(7,1)]+[(5,2),(6,2),(7,2)]:t+=rf'\fill[otGreen!40]({c},{r})rectangle({c+1},{r+1});'
    t+=grille(9,5)
    dessin('aa-15',rf'\begin{{scope}}[scale=.55]{t}\end{{scope}}','Le serpentin et le carré couvrent chacun neuf carreaux ; leurs contours diffèrent.')
    META['aa-15']={'type':'cellules','aires':[9,9]}
    # Horloges.
    dessin('cours-horloge',horloge(0,10,35),'La petite aiguille donne l’heure, la grande les minutes : il est 10 h 35.')
    META['cours-horloge']={'type':'horloge'}
    dessin('hor-1',horloge(0,7,15)+horloge(4.2,10,35),'Deux horloges du matin à lire.')
    META['hor-1']={'type':'horloge'}
    dessin('hor-2',horloge(0,4,45,sol=True),'Le cadran est vide dans l’énoncé ; les aiguilles de 16 h 45 figurent en vert au corrigé.')
    META['hor-2']={'type':'horloge'}
    t=r'\draw[otMuted,line width=1pt](0,0)--(9,0);'
    for x,l in [(0,'8 h 30'),(2.6,'11 h 45'),(4.0,'13 h 30'),(6.4,'16 h 30')]:
        t+=rf'\draw[otNavy]({x},-.12)--({x},.12);\node[below,font=\tiny]at({x},-.15){{{l}}};'
    t+=r'\draw[otNavy,line width=2pt](0,.3)--(2.6,.3);\draw[otGreenDark,line width=2pt](4.0,.3)--(6.4,.3);'
    t+=r'\node[above,font=\tiny]at(1.3,.35){matin};\node[above,font=\tiny]at(5.2,.35){après-midi};'
    dessin('hor-12',t,'La frise des instants : chaque trait est un horaire, chaque segment épais une durée de classe.')
    META['hor-12']={'type':'libre'}

# ================================================================= géométrie plane
def geometrie():
    t=r'\fill[otNavy](0,1.9)circle(1.3pt)node[above,geoLabel]{$ A $};\fill[otNavy](2.2,1.9)circle(1.3pt)node[above,geoLabel]{$ B $};\draw[geoTrait](0,1.9)--(2.2,1.9);'
    t+=r'\fill[otNavy](3.6,1.6)circle(1.3pt)node[above,geoLabel]{$ C $};\fill[otNavy](5.6,2.2)circle(1.3pt)node[above,geoLabel]{$ D $};\draw[geoTrait](3.2,1.48)--(6.2,2.38);'
    t+=r'\fill[otNavy](0,.3)circle(1.3pt)node[above,geoLabel]{$ E $};\fill[otNavy](1.8,.3)circle(1.3pt)node[above,geoLabel]{$ F $};\draw[geoTrait](0,.3)--(3.3,.3);'
    dessin('geo-1',t,'Trois objets : limité des deux côtés, illimité des deux côtés, limité d’un seul côté.')
    META['geo-1']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)--(7,0);\fill[otNavy](0,0)circle(1.5pt)node[below,geoLabel]{$ A $};\fill[otNavy](7,0)circle(1.5pt)node[below,geoLabel]{$ B $};\node[above,font=\tiny]at(3.5,.35){7 cm};'
    t+=r'\geoSolution{\fill[otGreenDark](3.5,0)circle(1.6pt)node[below,geoLabel]{$ M $};\draw[otGreenDark](1.6,-.08)--(1.9,.08)(5.1,-.08)--(5.4,.08);}'
    dessin('geo-2',t,'Le milieu partage le segment en deux longueurs égales, codées au corrigé.')
    META['geo-2']={'type':'libre'}
    t=r'\draw[geoTrait](-.3,.9)--(3.0,.9)node[right,font=\scriptsize]{$ (d_2) $};\draw[geoTrait](1.3,-.4)--(1.3,2.2)node[above,font=\scriptsize]{$ (d_1) $};\draw[otNavy](1.3,.9)++(.26,0)--++(0,.26)--++(-.26,0);'
    t+=r'\draw[geoTrait](4.6,-.3)--(7.6,1.9)node[right,font=\scriptsize]{$ (d_3) $};\draw[geoTrait](4.6,1.7)--(7.6,.1)node[right,font=\scriptsize]{$ (d_4) $};'
    dessin('geo-3',t,'À gauche, l’équerre s’ajuste : angle droit. À droite, les droites se coupent sans angle droit.')
    META['geo-3']={'type':'libre'}
    t=r'\draw[geoTrait](0,1.9)--(7.4,1.9)node[right,font=\scriptsize]{$ (a) $};\draw[geoTrait](0,.7)--(7.4,.7)node[right,font=\scriptsize]{$ (b) $};'
    t+=r'\draw[otMuted,<->](1.2,.7)--(1.2,1.9);\node[right,font=\tiny]at(1.2,1.3){2 cm};\draw[otMuted,<->](5.6,.7)--(5.6,1.9);\node[right,font=\tiny]at(5.6,1.3){2 cm};'
    t+=r'\draw[geoTrait](0,-.4)--(7.4,.45)node[right,font=\scriptsize]{$ (c) $};'
    dessin('geo-4',t,'L’écart entre deux parallèles reste constant ; il change pour la droite oblique.')
    META['geo-4']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)circle(1.6);\fill[otNavy](0,0)circle(1.5pt)node[below left,geoLabel]{$ O $};'
    t+=r'\draw[geoTrait](0,0)--(40:1.6);\fill[otNavy](40:1.6)circle(1.3pt)node[above right,geoLabel]{$ A $};'
    t+=r'\draw[geoTrait](-1.6,0)--(1.6,0);\fill[otNavy](-1.6,0)circle(1.3pt)node[left,geoLabel]{$ B $};\fill[otNavy](1.6,0)circle(1.3pt)node[right,geoLabel]{$ C $};'
    t+=r'\draw[geoTrait](210:1.6)--(300:1.6);\fill[otNavy](210:1.6)circle(1.3pt)node[below left,geoLabel]{$ D $};\fill[otNavy](300:1.6)circle(1.3pt)node[below right,geoLabel]{$ E $};'
    dessin('geo-5',t,'Rayon, diamètre et corde : seul le diamètre passe par le centre.')
    META['geo-5']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)--(6.6,0)node[right,font=\scriptsize]{$ (d) $};\fill[otNavy](2.8,1.7)circle(1.5pt)node[above,geoLabel]{$ A $};'
    t+=r'\geoSolution{\draw[geoReponse](2.8,2.1)--(2.8,-.5);\draw[otGreenDark](2.8,0)++(.24,0)--++(0,.24)--++(-.24,0);}'
    dessin('geo-6',t,'La perpendiculaire passe par A et coupe (d) à angle droit, codé en vert.')
    META['geo-6']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)--(6.6,.9)node[right,font=\scriptsize]{$ (d) $};\fill[otNavy](2.4,2.2)circle(1.5pt)node[above,geoLabel]{$ B $};'
    t+=r'\geoSolution{\draw[geoReponse](-.1,1.87)--(6.4,2.76);}'
    dessin('geo-7',t,'La parallèle garde le même écart avec (d) tout du long.')
    META['geo-7']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)circle(1.5);\fill[otNavy](0,0)circle(1.4pt)node[below,geoLabel]{$ O $};'
    t+=r'\draw[geoTrait](0,0)--(55:1.5);\node[font=\tiny]at(55:.85){\colorbox{white}{4 cm}};'
    t+=r'\draw[otMuted,dashed](-1.5,0)--(1.5,0);'
    dessin('geo-8',t,'Le rayon joint le centre au cercle ; un diamètre traverse en passant par O.')
    META['geo-8']={'type':'libre'}
    t=poly([(0,0),(3.3,0),(0,2.6)])
    t+=r'\node[below left,font=\small]at(0,0){$ A $};\node[below right,font=\small]at(3.3,0){$ B $};\node[above,font=\small]at(0,2.6){$ C $};'
    t+=r'\draw[otNavy](.3,0)--(.3,.3)--(0,.3);'
    t+=r'\draw[otNavy](1.6,-.09)--(1.75,.09);\draw[otNavy](-.09,1.22)--(.09,1.38);'
    dessin('geo-9',t,'Les codes affirment : AB = AC et angle droit en A.')
    META['geo-9']={'type':'libre'}
    t=r'\fill[otNavy](0,0)circle(1.6pt)node[below,geoLabel]{$ O $};\node[font=\tiny]at(1.1,-.75){3 cm : rayon annoncé};'
    t+=r'\geoSolution{\fill[otGreen!16](0,0)circle(1.9);\draw[geoReponse](0,0)circle(1.9);\draw[otGreenDark,<->](0,0)--(35:1.9);\node[font=\tiny,otGreenDark]at(35:1.1){3 cm};}'
    dessin('geo-10',t,'Le cercle vert réunit les points à exactement 3 cm de O ; l’intérieur teinté est à moins de 3 cm.')
    META['geo-10']={'type':'libre'}
    t=r'\draw[otMuted,dashed](0,0)rectangle(4.2,2.5);\node[font=\tiny,otMuted]at(2.1,1.25){croquis à main levée};'
    t+=r'\geoSolution{\draw[geoReponse](0,-3.3)rectangle(4.2,-.8);'
    t+=r'\fill[otGreenDark](0,-3.3)circle(1.4pt)node[below left,geoLabel]{$ A $};\fill[otGreenDark](4.2,-3.3)circle(1.4pt)node[below right,geoLabel]{$ B $};\fill[otGreenDark](4.2,-.8)circle(1.4pt)node[above right,geoLabel]{$ C $};\fill[otGreenDark](0,-.8)circle(1.4pt)node[above left,geoLabel]{$ D $};'
    t+=r'\fill[otGreenDark](2.1,-3.3)circle(1.4pt)node[below,geoLabel]{$ M $};\draw[geoReponse](0,-3.3)circle(2.1);}'
    dessin('geo-11',t,'Le rectangle mesure 5 cm sur 3 cm (échelle réduite) ; le cercle de centre A passe par M, à 2,5 cm.')
    META['geo-11']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)--(2.9,0);\fill[otNavy](0,0)circle(1.5pt)node[below left,geoLabel]{$ A $};\fill[otNavy](2.9,0)circle(1.5pt)node[below right,geoLabel]{$ B $};\node[below,font=\tiny]at(1.45,-.12){4 cm};'
    t+=r'\geoSolution{\draw[geoReponse](0,0)circle(2.15);\draw[geoReponse](2.9,0)circle(2.15);\fill[otGreenDark](1.45,1.586)circle(1.6pt);\fill[otGreenDark](1.45,-1.586)circle(1.6pt);\node[right,font=\tiny,otGreenDark]at(1.5,1.7){à 3 cm de A et de B};}'
    dessin('geo-12',t,'Deux cercles de même rayon : leurs points communs sont à 3 cm des deux centres. Échelle réduite.')
    META['geo-12']={'type':'libre'}
    t=grille(11,4)
    t+=poly([(1,1),(4,1),(4,3),(1,3)])+r'\draw[geoTrait](1,1)--(4,3);'
    t+=r'\geoSolution{'+poly([(6,1),(9,1),(9,3),(6,3)],'geoReponse')+r'\draw[geoReponse](6,1)--(9,3);}'
    dessin('geo-13',rf'\begin{{scope}}[scale=.62]{t}\end{{scope}}','Reproduire, c’est compter les mêmes carreaux : 3 sur 2, puis la diagonale.')
    META['geo-13']={'type':'libre'}
    t=r'\draw[geoTrait](0,.3)--(7,.3)node[right,font=\scriptsize]{$ (d_1) $};'
    t+=r'\geoSolution{\draw[geoReponse](1.6,-.4)--(1.6,2.6)node[above,font=\scriptsize]{$ (d_2) $};\draw[otGreenDark](1.6,.3)++(.22,0)--++(0,.22)--++(-.22,0);'
    t+=r'\draw[geoReponse](.2,1.9)--(6.8,1.9)node[above right,font=\scriptsize]{$ (d_3) $};\draw[otGreenDark](1.6,1.9)++(.22,0)--++(0,-.22)--++(-.22,0);}'
    dessin('geo-14',t,'Deux droites perpendiculaires à une même droite : (d1) et (d3) sont parallèles.')
    META['geo-14']={'type':'libre'}
    t=r'\fill[otNavy!10](0,0)rectangle(8.2,3.4);'
    t+=r'\fill[white](0,.5)rectangle(8.2,1.0);\node[font=\tiny]at(6.9,.75){rue des Lilas};'
    t+=r'\fill[white](0,2.3)rectangle(8.2,2.8);\node[font=\tiny]at(6.9,2.55){rue des Érables};'
    t+=r'\fill[white](2.1,0)rectangle(2.7,3.4);\node[font=\tiny,rotate=90]at(2.4,1.7){avenue du Parc};'
    t+=r'\draw[otNavy](2.7,1.0)++(.2,0)--++(0,.2)--++(-.2,0);'
    t+=r'\fill[otNavy](2.4,1.45)circle(1.4pt)node[right,geoLabel]{$ F $};\fill[otNavy](2.4,2.1)circle(1.4pt)node[right,geoLabel]{$ G $};'
    t+=r'\geoSolution{\draw[geoReponse](2.4,1.45)++(70:1.1)arc(70:110:1.1);\draw[geoReponse](2.4,2.1)++(-70:1.1)arc(-70:-110:1.1);\fill[otGreenDark](2.02,2.48)circle(0pt);\fill[otGreenDark](1.9,1.775)circle(1.7pt)node[left,geoLabel]{fontaine};}'
    dessin('geo-15',t,'Le plan du quartier : rues parallèles, avenue perpendiculaire, et deux arcs pour la fontaine.')
    META['geo-15']={'type':'libre'}

def triangles():
    def tri(pts,labels,codes='',extra=''):
        t=poly(pts)
        for (x,y),l,w in labels:t+=rf'\node[{w},font=\small]at({x},{y}){{$ {l} $}};'
        return t+codes+extra
    t=tri([(0,0),(2.2,0),(0,1.7)],[((1.1,-.3),'1','below')],r'\draw[otNavy](.26,0)--(.26,.26)--(0,.26);')
    t+=rf'\begin{{scope}}[shift={{(3.1,0)}}]'+tri([(0,0),(2.2,0),(1.1,1.8)],[((1.1,-.3),'2','below')],r'\draw[otNavy](.49,.84)--(.65,.99);\draw[otNavy](1.55,.99)--(1.71,.84);')+r'\end{scope}'
    t+=rf'\begin{{scope}}[shift={{(6.2,0)}}]'+tri([(0,0),(2,0),(1,1.732)],[((1,-.3),'3','below')],r'\draw[otNavy](.92,-.09)--(1.08,.09);\draw[otNavy](.42,.78)--(.58,.95);\draw[otNavy](1.42,.95)--(1.58,.78);')+r'\end{scope}'
    t+=rf'\begin{{scope}}[shift={{(9.3,0)}}]'+tri([(0,0),(2.3,0),(1.7,1.6)],[((1.15,-.3),'4','below')])+r'\end{scope}'
    dessin('tri-1',t,'Lire les codes : angle droit, côtés égaux deux à deux ou trois à trois, ou aucun code.')
    META['tri-1']={'type':'libre'}
    t=tri([(0,2.1),(-1.3,0),(1.3,0)],[((0,2.1),'M','above'),((-1.3,0),'N','below left'),((1.3,0),'P','below right')])
    t+=r'\geoSolution{\draw[otGreenDark](-.72,1.0)--(-.58,1.18);\draw[otGreenDark](.58,1.18)--(.72,1.0);}'
    dessin('tri-2',t,'Les codes verts affirment MN = MP : le triangle est isocèle de sommet principal M.')
    META['tri-2']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)--(2.9,0);\fill[otNavy](0,0)circle(1.4pt)node[below left,geoLabel]{$ B $};\fill[otNavy](2.9,0)circle(1.4pt)node[below right,geoLabel]{$ C $};\node[below,font=\tiny]at(1.45,-.14){4 cm};'
    t+=r'\geoSolution{\draw[geoAide]([shift={(0,0)}]52:2.9)arc(52:70:2.9);\draw[geoAide]([shift={(2.9,0)}]110:2.9)arc(110:128:2.9);\draw[geoReponse](0,0)--(1.45,2.511)--(2.9,0);\fill[otGreenDark](1.45,2.511)circle(1.5pt)node[above,geoLabel]{$ A $};}'
    dessin('tri-3',t,'Les deux arcs de rayon 4 cm se croisent en A ; échelle réduite, méthode fidèle.')
    META['tri-3']={'type':'triangle','points':[(0,0),(2.9,0),(1.45,2.511)]}
    q=r'\draw[geoTrait](0,0)rectangle(2.4,1.5);\draw[otNavy](.2,0)--(.2,.2)--(0,.2);\draw[otNavy](2.4,1.3)--(2.2,1.3)--(2.2,1.5);\node[below,font=\small]at(1.2,-.08){$ 1 $};'
    q+=rf'\begin{{scope}}[shift={{(3.4,0)}}]\draw[geoTrait](1,0)--(2,.75)--(1,1.5)--(0,.75)--cycle;'+''.join(rf'\draw[otNavy]({x1},{y1})--({x2},{y2});' for (x1,y1,x2,y2) in [(.42,.28,.58,.47),(1.42,.47,1.58,.28),(.42,1.22,.58,1.03),(1.42,1.03,1.58,1.22)])+r'\node[below,font=\small]at(1,-.08){$ 2 $};\end{scope}'
    q+=rf'\begin{{scope}}[shift={{(6.8,0)}}]\draw[geoTrait](0,0)rectangle(1.5,1.5);\draw[otNavy](.2,0)--(.2,.2)--(0,.2);'+''.join(rf'\draw[otNavy]({x1},{y1})--({x2},{y2});' for (x1,y1,x2,y2) in [(.67,-.09,.83,.09),(.67,1.41,.83,1.59),(-.09,.67,.09,.83),(1.41,.67,1.59,.83)])+r'\node[below,font=\small]at(.75,-.08){$ 3 $};\end{scope}'
    q+=r'\begin{scope}[shift={(9.3,0)}]\draw[geoTrait](0,.2)--(2.2,0)--(1.9,1.4)--(.5,1.6)--cycle;\node[below,font=\small]at(1.1,-.1){$ 4 $};\end{scope}'
    dessin('tri-4',q,'Quatre quadrilatères : lire les codes d’angles droits et de côtés égaux.')
    META['tri-4']={'type':'libre'}
    t=r'\draw[geoTrait](1.4,0)--(2.8,1.05)--(1.4,2.1)--(0,1.05)--cycle;'
    t+=''.join(rf'\draw[otNavy]({x1},{y1})--({x2},{y2});' for (x1,y1,x2,y2) in [(.62,.42,.78,.63),(2.02,.63,2.18,.42),(.62,1.68,.78,1.47),(2.02,1.47,2.18,1.68)])
    dessin('tri-5',t,'Quatre côtés égaux, aucun angle droit codé : l’équerre ne s’ajuste pas aux sommets.')
    META['tri-5']={'type':'libre'}
    t=r'\draw[otMuted,dashed](0,0)--(3.2,0)--(0,1.92)--cycle;\node[font=\tiny,otMuted]at(2.3,1.0){croquis};\node[below,font=\tiny]at(1.6,-.05){AB = 5 cm};\node[left,font=\tiny]at(0,.96){AC = 3 cm};\node[below left,font=\small]at(0,0){$ A $};\node[below right,font=\small]at(3.2,0){$ B $};\node[above,font=\small]at(0,1.92){$ C $};'
    t+=r'\geoSolution{\begin{scope}[shift={(4.6,0)}]\draw[geoReponse](0,0)--(3.2,0)--(0,1.92)--cycle;\draw[otGreenDark](.26,0)--(.26,.26)--(0,.26);\node[below left,font=\small]at(0,0){$ A $};\node[below right,font=\small]at(3.2,0){$ B $};\node[above,font=\small]at(0,1.92){$ C $};\end{scope}}'
    dessin('tri-6',t,'Croquis d’abord, construction exacte ensuite : l’angle droit se trace en premier. Échelle réduite.')
    META['tri-6']={'type':'triangle','points':[(0,0),(3.2,0),(0,1.92)]}
    t=r'\draw[geoTrait](0,0)--(2.2,0);\fill[otNavy](0,0)circle(1.4pt)node[below left,geoLabel]{$ E $};\fill[otNavy](2.2,0)circle(1.4pt)node[below right,geoLabel]{$ F $};\node[below,font=\tiny]at(1.1,-.14){4 cm};'
    t+=r'\geoSolution{\draw[geoAide]([shift={(0,0)}]62:3.3)arc(62:78:3.3);\draw[geoAide]([shift={(2.2,0)}]102:3.3)arc(102:118:3.3);\draw[geoReponse](0,0)--(1.1,3.111)--(2.2,0);\fill[otGreenDark](1.1,3.111)circle(1.5pt)node[above,geoLabel]{$ D $};\draw[otGreenDark](.47,1.48)--(.63,1.63);\draw[otGreenDark](1.57,1.63)--(1.73,1.48);}'
    dessin('tri-7',t,'Les arcs de 6 cm centrés en E et F se croisent en D ; échelle réduite, codes des côtés égaux.')
    META['tri-7']={'type':'triangle','points':[(0,0),(2.2,0),(1.1,3.111)]}
    t=r'\draw[geoTrait](0,0)--(3.6,0);\node[below,font=\tiny]at(1.8,-.1){AB = 6 cm};\fill[otNavy](0,0)circle(1.4pt)node[below left,geoLabel]{$ A $};\fill[otNavy](3.6,0)circle(1.4pt)node[below right,geoLabel]{$ B $};'
    t+=r'\geoSolution{\draw[geoReponse](3.6,0)--(3.6,2.4)--(0,2.4)--(0,0);\draw[otGreenDark](.24,0)--(.24,.24)--(0,.24);\draw[otGreenDark](3.36,0)--(3.36,.24)--(3.6,.24);\draw[otGreenDark](3.6,2.16)--(3.36,2.16)--(3.36,2.4);\fill[otGreenDark](3.6,2.4)circle(1.4pt)node[above right,geoLabel]{$ C $};\fill[otGreenDark](0,2.4)circle(1.4pt)node[above left,geoLabel]{$ D $};\node[right,font=\tiny,otGreenDark]at(3.62,1.2){4 cm};}'
    dessin('tri-8',t,'Perpendiculaires aux deux extrémités, report de 4 cm, puis jonction. Échelle réduite.')
    META['tri-8']={'type':'libre'}
    import math as _m
    a=20;ca,sa=_m.cos(_m.radians(a)),_m.sin(_m.radians(a));L=2.8
    B=(L*ca,L*sa);C=(B[0]-L*sa,B[1]+L*ca);D=(-L*sa,L*ca)
    t=rf'\draw[geoTrait](0,0)--({B[0]:.3f},{B[1]:.3f});\node[below right,font=\tiny]at({B[0]/2:.3f},{B[1]/2:.3f}){{côté donné : 4{{,}}5 cm}};'
    t+=rf'\geoSolution{{\draw[geoReponse]({B[0]:.3f},{B[1]:.3f})--({C[0]:.3f},{C[1]:.3f})--({D[0]:.3f},{D[1]:.3f})--(0,0);\draw[otGreenDark]({ca*.24-sa*0:.3f},{sa*.24:.3f})--++({-sa*.24:.3f},{ca*.24:.3f})--++({-ca*.24:.3f},{-sa*.24:.3f});}}'
    dessin('tri-9',t,'Le carré s’appuie sur le côté incliné : l’orientation ne change pas la nature de la figure.')
    META['tri-9']={'type':'libre'}
    t=r'\draw[otMuted,dashed](0,0)--(2.5,.65)(0,0)--(.65,2.5);\node[font=\tiny,otMuted]at(1.9,1.9){croquis de l’angle en A};\node[below left,font=\small]at(0,0){$ A $};'
    B=(2.42,.63);D=(.63,2.42);C=(B[0]+D[0],B[1]+D[1])
    t+=rf'\geoSolution{{\draw[geoReponse](0,0)--({B[0]},{B[1]})--({C[0]},{C[1]})--({D[0]},{D[1]})--cycle;'
    t+=rf'\fill[otGreenDark]({B[0]},{B[1]})circle(1.4pt)node[below right,geoLabel]{{$ B $}};\fill[otGreenDark]({C[0]},{C[1]})circle(1.4pt)node[above right,geoLabel]{{$ C $}};\fill[otGreenDark]({D[0]},{D[1]})circle(1.4pt)node[above left,geoLabel]{{$ D $}};'
    t+=r'\draw[geoAide]([shift={('+f'{B[0]},{B[1]}'+r')}]100:2.5)arc(100:120:2.5);\draw[geoAide]([shift={('+f'{D[0]},{D[1]}'+r')}]-10:2.5)arc(-10:20:2.5);}'
    dessin('tri-10',t,'Quatre côtés de 5 cm reportés au compas : le losange se ferme en C. Échelle réduite.')
    META['tri-10']={'type':'libre'}
    t=r'\geoSolution{}\draw[geoTrait](0,0)rectangle(4.2,2.1);\fill[otNavy](0,0)circle(1.3pt)node[below left,geoLabel]{$ E $};\fill[otNavy](4.2,0)circle(1.3pt)node[below right,geoLabel]{$ F $};\fill[otNavy](4.2,2.1)circle(1.3pt)node[above right,geoLabel]{$ G $};\fill[otNavy](0,2.1)circle(1.3pt)node[above left,geoLabel]{$ H $};'
    t+=r'\geoSolution{\fill[otGreenDark](2.1,0)circle(1.5pt)node[below,geoLabel]{$ M $};\draw[geoReponse](2.1,0)--(4.2,2.1)(2.1,0)--(0,2.1);}'
    dessin('tri-11',t,'Le rectangle mesure 6 cm sur 3 cm (échelle réduite) ; M est le milieu de [EF].')
    META['tri-11']={'type':'libre'}
    v=[('b',r'\draw[geoTrait](0,.3)--(1.7,.3);\fill[otNavy](0,.3)circle(1.1pt);\fill[otNavy](1.7,.3)circle(1.1pt);'),
       ('d',r'\draw[otMuted](.2,.1)--(1.0,1.3);\draw[otMuted](1.0,1.3)--(1.6,.1);\node[font=\tiny]at(.9,-.05){compas : 4 cm};'),
       ('a',r'\draw[geoTrait](0,0)--(1.7,0);\draw[geoAide](.55,1.3)arc(110:80:1.4);\draw[geoAide](1.15,1.3)arc(70:100:1.4);'),
       ('c',r'\draw[geoTrait](0,0)--(1.7,0)--(.85,1.45)--cycle;')]
    t=''
    for i,(lab,body) in enumerate(v):
        t+=rf'\begin{{scope}}[shift={{({i*2.6},0)}}]\draw[otRule!80,line width=.3pt](-.2,-.5)rectangle(2.1,1.7);{body}\node[below,font=\small]at(.95,-.15){{({lab})}};\end{{scope}}'
    dessin('tri-12',t,'Quatre vignettes en désordre : retrouver l’ordre du programme de construction.')
    META['tri-12']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)--(3.2,0)--(3.5,2.0)--(.2,2.3)--cycle;'
    t+=r'\draw[otNavy](.24,0)--(.24,.24)--(0,.24);\draw[otNavy](3.2,0)--(2.96,.03)--(2.99,.27);'
    t+=r'\node[font=\tiny,otOrange]at(3.1,1.75){l’équerre dépasse ici};\draw[otOrange,->](2.9,1.6)--(3.35,1.95);'
    dessin('tri-13',t,'Trois angles conviennent, le quatrième non : la figure n’est pas un rectangle.')
    META['tri-13']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)rectangle(2.3,2.3);\node[below,font=\tiny]at(1.15,-.05){carré, côté 6 cm};'
    t+=r'\begin{scope}[shift={(3.6,0)}]\draw[geoTrait](0,0)--(2.3,0)--(1.15,1.99)--cycle;\node[below,font=\tiny]at(1.15,-.05){triangle équilatéral, côté 6 cm};\end{scope}'
    dessin('tri-14',t,'Mêmes côtés, nombres de côtés différents : les périmètres diffèrent.')
    META['tri-14']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)rectangle(4.0,3.0);\draw[geoTrait](0,0)--(4.0,3.0)(4.0,0)--(0,3.0);'
    t+=r'\node[below,font=\tiny]at(2,-.08){8 cm};\node[left,font=\tiny]at(0,1.5){6 cm};'
    t+=r'\geoSolution{\node[font=\tiny,otGreenDark]at(2.75,1.9){\colorbox{white}{10 cm}};\node[font=\tiny,otGreenDark]at(1.25,1.9){\colorbox{white}{10 cm}};\fill[otGreenDark](2,1.5)circle(1.4pt);}'
    dessin('tri-15',t,'Les deux diagonales du rectangle ont la même longueur et se coupent en leur milieu.')
    META['tri-15']={'type':'libre'}
    # Figures de cours.
    t=tri([(0,0),(2.1,0),(0,1.6)],[((1.05,-.3),r'\text{rectangle}','below')],r'\draw[otNavy](.24,0)--(.24,.24)--(0,.24);')
    t+=rf'\begin{{scope}}[shift={{(3.2,0)}}]'+tri([(0,0),(2.1,0),(1.05,1.75)],[((1.05,-.3),r'\text{isocèle}','below')],r'\draw[otNavy](.44,.8)--(.61,.95);\draw[otNavy](1.49,.95)--(1.66,.8);')+r'\end{scope}'
    t+=rf'\begin{{scope}}[shift={{(6.4,0)}}]'+tri([(0,0),(2,0),(1,1.732)],[((1,-.3),r'\text{équilatéral}','below')],r'\draw[otNavy](.92,-.09)--(1.08,.09);\draw[otNavy](.42,.78)--(.58,.95);\draw[otNavy](1.42,.95)--(1.58,.78);')+r'\end{scope}'
    dessin('cours-triangles',t,'Trois triangles particuliers et leurs codes : angle droit, deux côtés égaux, trois côtés égaux.')
    META['cours-triangles']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)rectangle(2.5,1.5);\node[below,font=\tiny]at(1.25,-.07){rectangle};\draw[otNavy](.2,0)--(.2,.2)--(0,.2);'
    t+=r'\begin{scope}[shift={(3.5,0)}]\draw[geoTrait](1,0)--(2,.75)--(1,1.5)--(0,.75)--cycle;\node[below,font=\tiny]at(1,-.07){losange};\end{scope}'
    t+=r'\begin{scope}[shift={(6.7,0)}]\draw[geoTrait](0,0)rectangle(1.5,1.5);\node[below,font=\tiny]at(.75,-.07){carré};\draw[otNavy](.2,0)--(.2,.2)--(0,.2);\draw[otNavy](.67,-.09)--(.83,.09);\draw[otNavy](-.09,.67)--(.09,.83);\end{scope}'
    dessin('cours-quadrilateres',t,'Les quadrilatères usuels : angles droits pour le rectangle, côtés égaux pour le losange, les deux pour le carré.')
    META['cours-quadrilateres']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)circle(1.5);\fill[otNavy](0,0)circle(1.4pt)node[below left,geoLabel]{$ O $};\draw[geoTrait](0,0)--(35:1.5);\node[font=\tiny]at(35:.95){\colorbox{white}{rayon}};\draw[geoTrait](145:1.5)--(-35:1.5);'
    t+=r'\node[font=\tiny]at(-.55,-.62){\colorbox{white}{diamètre}};'
    dessin('cours-cercle',t,'Tous les points du cercle sont à la même distance du centre O.')
    META['cours-cercle']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)--(2.6,0);\draw[geoTrait](0,0)--(50:2.2);\fill[otNavy](0,0)circle(1.4pt);'
    t+=r'\node[below left,font=\small]at(0,0){$ B $};\node[right,font=\small]at(2.6,0){$ C $};\node[above,font=\small]at(50:2.2){$ A $};'
    t+=r'\draw[otGreenDark,line width=.8pt](0:.8)arc(0:50:.8);\node[font=\tiny]at(25:1.1){$\widehat{ABC}$};'
    dessin('cours-angles',t,'L’angle de sommet B se note avec la lettre du sommet au milieu.')
    META['cours-angles']={'type':'libre'}

# ================================================================= symétrie et solides
def symetries():
    t=grille(10,4)
    t+=r'\draw[otOrange,dashed,line width=1pt](1.5,-.3)--(1.5,4.3);'
    t+=poly([(0.5,1),(1.5,2.5),(2.5,1),(2,1),(2,0.2),(1,0.2),(1,1)],'geoTrait')
    t+=r'\begin{scope}[shift={(4,0)}]\draw[otOrange,dashed,line width=1pt](1.5,-.3)--(1.5,4.3);'
    t+=poly([(1.5,3.5),(2.5,2),(1.9,2),(2.3,.8),(.7,.8),(1.1,2),(.5,2)],'geoTrait')+r'\end{scope}'
    t+=r'\begin{scope}[shift={(8,0)}]\draw[otOrange,dashed,line width=1pt](.8,-.3)--(.8,4.3);'
    t+=poly([(.8,.4),(.8,3.6),(2.2,2.8),(.8,2.0)],'geoTrait',close=False)+r'\end{scope}'
    dessin('sym-1',rf'\begin{{scope}}[scale=.6]{t}\end{{scope}}','Trois figures et une droite en tirets : imaginer le pliage pour décider.')
    META['sym-1']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)rectangle(2,2);'
    t+=r'\draw[otOrange,dashed](1,-.3)--(1,2.3)(-.3,1)--(2.3,1)(-.25,-.25)--(2.25,2.25)(-.25,2.25)--(2.25,-.25);'
    t+=r'\begin{scope}[shift={(3.4,0)}]\draw[geoTrait](0,.35)rectangle(2.6,1.65);\draw[otOrange,dashed](1.3,.05)--(1.3,1.95)(-.3,1)--(2.9,1);\end{scope}'
    t+=r'\begin{scope}[shift={(7.2,0)}]\draw[geoTrait](0,.1)--(2,.1)--(1,1.83)--cycle;\draw[otOrange,dashed](1,-.2)--(1,1.95)(.28,1.37)--(1.75,.52)?;\draw[otOrange,dashed](1.72,1.37)--(.25,.52);\end{scope}'
    t=t.replace('?','')
    dessin('sym-2',t,'Les axes en tirets : quatre pour le carré, deux pour le rectangle, trois pour le triangle équilatéral.')
    META['sym-2']={'type':'libre'}
    t=r'\draw[geoTrait](0,0)rectangle(3.4,2.1);\draw[otOrange,dashed](0,0)--(3.4,2.1);'
    t+=r'\node[font=\tiny]at(1.1,1.5){pliage ?};'
    dessin('sym-3',t,'Plier le long de la diagonale laisse dépasser deux coins : ce n’est pas un axe.')
    META['sym-3']={'type':'libre'}
    symfig('sym-4',[],('v',4),8,4,points=[('A',2,3),('B',1,1),('C',3,2)],leg='Compter les carreaux jusqu’à l’axe, puis autant de l’autre côté ; images en vert.')
    symfig('sym-5',[[(4,0.5),(2.5,0.5),(2.5,2.5),(4,3.5)]],('v',4),8,4,leg='La demi-maison se reflète sommet par sommet à travers l’axe vertical.')
    symfig('sym-6',[[(1,3),(4,4)]],('h',2),6,5,points=[('A',1,3),('B',4,4)],leg='L’axe est horizontal : chaque point descend sous l’axe à la même distance.')
    symfig('sym-7',[[(1,4),(3,4),(2,6)]],('h',3),7,6,leg='L’aile du papillon se reflète sous l’axe horizontal.')
    t=''
    for i,(l,ax) in enumerate([('A','v'),('B','h'),('H','vh'),('F','')]):
        t+=rf'\begin{{scope}}[shift={{({i*2.6},0)}}]\node[font=\otBold\fontsize{{26}}{{28}}\selectfont,otNavy]at(.9,.9){{{l}}};'
        if 'v' in ax:t+=r'\draw[otOrange,dashed](.9,-.1)--(.9,1.9);'
        if 'h' in ax:t+=r'\draw[otOrange,dashed](-.1,.9)--(1.9,.9);'
        t+=r'\end{scope}'
    dessin('sym-8',t,'Les lettres et leurs axes en tirets : vertical, horizontal, les deux, ou aucun.')
    META['sym-8']={'type':'libre'}
    t=grille(8,4)+r'\draw[otOrange,dashed,line width=1pt](4,-.3)--(4,4.3);'
    t+=poly([(1,1),(3,1),(3,3)])
    t+=r'\node[above,font=\scriptsize]at(3,3){$ B $};'
    t+=poly([(7,1),(5,1),(6,3)],'otNavy!60!white, line width=.8pt')
    t+=r"\node[above,font=\scriptsize]at(6,3){$ B' $ ?};"
    t+=r"\geoSolution{\fill[otGreenDark](5,3)circle(1.8pt)node[above,geoLabel]{$ B' $};"+poly([(7,1),(5,1),(5,3)],'geoReponse')+r'}'
    dessin('sym-9',rf'\begin{{scope}}[scale=.62]{t}\end{{scope}}','Un sommet de l’image proposée est mal placé : les distances à l’axe doivent être égales.')
    META['sym-9']={'type':'libre'}
    symfig('sym-10',[[(3,1),(1,3)]],('v',3),6,4,points=[('B',1,3)],leg='A est sur l’axe : il ne bouge pas ; seul B se reflète.',extra=r'\node[below right,font=\scriptsize]at(3,1){$ A $};')
    cells=[(0,3),(1,3),(1,2),(2,2),(2,1),(0,0)]
    sol=[(2*4-1-c,r) for (c,r) in cells]
    t=grille(8,4)+r'\draw[otOrange,dashed,line width=1pt](4,-.3)--(4,4.3);'
    for c,r in cells:t+=rf'\fill[otNavy!40]({c},{r})rectangle({c+1},{r+1});'
    t+=r'\geoSolution{'+''.join(rf'\fill[otGreen!50]({c},{r})rectangle({c+1},{r+1});' for c,r in sol)+r'}'+grille(8,4)
    dessin('sym-11',rf'\begin{{scope}}[scale=.62]{t}\end{{scope}}','Chaque case colorée a sa jumelle de l’autre côté de l’axe, sur la même ligne.')
    META['sym-11']={'type':'symetrie','axe':['v',4],'originaux':[(c+.5,r+.5) for c,r in cells],'images':[(c+.5,r+.5) for c,r in sol],'grille':[8,4]}
    t=grille(8,6)+r'\draw[otOrange,dashed,line width=1pt](4,-.3)--(4,6.3);\draw[otOrange,dashed,line width=1pt](-.3,3)--(8.3,3);'
    quart=[(3,4),(2,4),(3,5),(1,3)]
    for c,r in quart:t+=rf'\fill[otNavy!40]({c},{r})rectangle({c+1},{r+1});'
    allc=[]
    for c,r in quart:
        allc+=[(7-c,r),(c,5-r),(7-c,5-r)]
    t+=r'\geoSolution{'+''.join(rf'\fill[otGreen!50]({c},{r})rectangle({c+1},{r+1});' for c,r in allc)+r'}'+grille(8,6)
    dessin('sym-12',rf'\begin{{scope}}[scale=.55]{t}\end{{scope}}','Deux axes : on reflète à droite, puis tout le haut se reflète en bas.')
    META['sym-12']={'type':'libre'}
    symfig('sym-13',[[(1,1),(1,5)]],('v',3),6,6,points=[('C',1,1),('D',1,5)],leg='Le segment image garde la même longueur : la symétrie conserve les distances.')
    t=grille(10,5)+r'\draw[otOrange,dashed,line width=1pt](5,-.3)--(5,5.3);'
    t+=poly([(5,1),(2,1),(3,0),(5,0)],'geoTrait')
    t+=poly([(5,2),(3,2),(5,4)],'geoTrait')
    t+=r'\draw[geoTrait](5,0)--(5,4.6);'
    t+=r'\geoSolution{'+poly([(5,1),(8,1),(7,0),(5,0)],'geoReponse')+poly([(5,2),(7,2),(5,4)],'geoReponse')+r'}'
    dessin('sym-14',rf'\begin{{scope}}[scale=.6]{t}\end{{scope}}','Le mât est sur l’axe ; coque et voile se reflètent de l’autre côté.')
    META['sym-14']={'type':'symetrie','axe':['v',5],'originaux':[(2,1),(3,0),(3,2)],'images':[(8,1),(7,0),(7,2)],'grille':[10,5]}
    t=grille(6,4)+r'\draw[otOrange,dashed,line width=1pt](3,-.3)--(3,4.3);'
    t+=dotpt(3,2,'P','above right')+dotpt(1,3,'Q','above left')
    t+=r'\geoSolution{'+dotpt(5,3,"Q'",'above right','otGreenDark')+r'\node[below,font=\tiny,otGreenDark]at(3,1.9){P est son propre symétrique};}'
    dessin('sym-15',rf'\begin{{scope}}[scale=.62]{t}\end{{scope}}','Un point sur l’axe ne bouge pas ; les autres traversent à égale distance.')
    META['sym-15']={'type':'symetrie','axe':['v',3],'originaux':[(1,3)],'images':[(5,3)],'grille':[6,4]}
    t=grille(10,4)+r'\draw[otOrange,dashed,line width=1pt](5,-.3)--(5,4.3);'
    t+=poly([(5,.5),(2,.5),(2,2.5),(3.5,3.5),(5,3.5)],'geoTrait',close=False)
    t+=poly([(5,.5),(8,.5),(8,2.5),(6.5,3.5),(5,3.5)],'geoTrait',close=False)
    dessin('cours-symetrie',rf'\begin{{scope}}[scale=.6]{t}\end{{scope}}','Le pliage le long de l’axe superpose exactement les deux moitiés de la figure.')
    META['cours-symetrie']={'type':'libre'}

def solides():
    def pave3(w=1.6,d=.55,h=1.0,sq=False):
        t=rf'\draw[geoTrait](0,0)rectangle({w},{h});'
        t+=rf'\draw[geoTrait](0,{h})--({d},{h+d*.75})--({w+d},{h+d*.75})--({w},{h});'
        t+=rf'\draw[geoTrait]({w},0)--({w+d},{d*.75})--({w+d},{h+d*.75});'
        t+=rf'\draw[otMuted,dashed](0,0)--({d},{d*.75})--({w+d},{d*.75})({d},{d*.75})--({d},{h+d*.75});'
        return t
    def pyram():
        return r'\draw[geoTrait](0,0)--(1.7,0)--(2.3,.5)--(.6,.5)--cycle;'.replace('geoTrait','otMuted,dashed')+r'\draw[geoTrait](0,0)--(1.7,0);\draw[geoTrait](0,0)--(1.15,1.9)--(1.7,0);\draw[geoTrait](2.3,.5)--(1.15,1.9);\draw[otMuted,dashed](.6,.5)--(1.15,1.9);'
    def cyl():
        return r'\draw[geoTrait](0,.35)--(0,1.7)(1.4,.35)--(1.4,1.7);\draw[geoTrait](.7,1.7)ellipse(.7 and .22);\draw[geoTrait](0,.35)arc(180:360:.7 and .22);\draw[otMuted,dashed](0,.35)arc(180:0:.7 and .22);'
    def cone():
        return r'\draw[geoTrait](0,.3)--(.8,2.0)--(1.6,.3);\draw[geoTrait](0,.3)arc(180:360:.8 and .25);\draw[otMuted,dashed](0,.3)arc(180:0:.8 and .25);'
    def boule():
        return r'\draw[geoTrait](0.8,1.0)circle(.8);\draw[otMuted](0,1.0)arc(180:360:.8 and .25);\draw[otMuted,dashed](0,1.0)arc(180:0:.8 and .25);'
    def prisme():
        return r'\draw[geoTrait](0,0)--(1.6,0)--(.8,1.1)--cycle;\draw[geoTrait](1.6,0)--(2.3,.5)(.8,1.1)--(1.5,1.6)--(2.3,.5)--(2.3,.5);\draw[geoTrait](1.5,1.6)--(.8,1.1);\draw[otMuted,dashed](0,0)--(.7,.5)--(2.3,.5)(.7,.5)--(1.5,1.6);'
    names=[('cube',r'\begin{scope}[scale=.9]'+pave3(1.1,.45,1.1)+r'\end{scope}'),('pavé',pave3()),('cylindre',cyl()),('pyramide',pyram()),('cône',cone()),('boule',boule())]
    t=''
    for i,(lab,body) in enumerate(names):
        t+=rf'\begin{{scope}}[shift={{({(i%6)*2.72},0)}}]{body}\node[below,font=\tiny]at(.95,-.35){{{lab}}};\end{{scope}}'
    dessin('cours-solides',r'\begin{scope}[scale=.82]'+t+r'\end{scope}','Six solides usuels ; les arêtes cachées sont en pointillés.')
    META['cours-solides']={'type':'libre'}
    t=''
    for i,(lab,body) in enumerate(names):
        t+=rf'\begin{{scope}}[shift={{({(i%6)*2.72},0)}}]{body}\node[below,font=\tiny]at(.95,-.35){{({i+1})}};\end{{scope}}'
    dessin('sol-1',r'\begin{scope}[scale=.82]'+t+r'\end{scope}','Six solides numérotés : retrouver le nom de chacun.')
    META['sol-1']={'type':'libre'}
    dessin('sol-2',r'\begin{scope}[scale=1.15]'+pave3(1.3,.5,1.3)+r'\end{scope}','Le cube en perspective : trois faces visibles, trois cachées.')
    META['sol-2']={'type':'libre'}
    dessin('sol-3',r'\begin{scope}[scale=1.15]'+pave3(2.0,.6,1.1)+r'\end{scope}','Le pavé : six faces rectangulaires, faces opposées identiques.')
    META['sol-3']={'type':'libre'}
    dessin('sol-4',pyram(),'Pyramide à base carrée : la base et quatre faces triangulaires.')
    META['sol-4']={'type':'libre'}
    dessin('sol-5',prisme(),'Prisme droit : deux bases triangulaires superposables, reliées par des rectangles.')
    META['sol-5']={'type':'libre'}
    t=patron('p1',[(1,0),(1,1),(0,1),(2,1),(1,2),(1,3)],s=.62)
    t=''
    nets=[([(1,0),(1,1),(0,1),(2,1),(1,2),(1,3)],'(1)'),([(0,0),(1,0),(2,0),(3,0),(1,1),(1,-1)],'(2)'),([(0,0),(1,0),(2,0),(3,0),(0,1),(1,1)],'(3)')]
    for i,(cells,lab) in enumerate(nets):
        miny=min(r for _,r in cells)
        cells=[(c,r-miny) for c,r in cells]
        t+=rf'\begin{{scope}}[shift={{({i*3.3},0)}}]'
        for (c,r) in cells:t+=rf'\draw[geoTrait]({c*.62:.3f},{r*.62:.3f})rectangle({(c+1)*.62:.3f},{(r+1)*.62:.3f});'
        t+=rf'\node[below,font=\small]at(1.2,-.2){{{lab}}};\end{{scope}}'
    dessin('sol-6',t,'Trois dispositions de six carrés : deux se plient en cube, une non.')
    META['sol-6']={'type':'patrons','nets':[c for c,_ in nets]}
    cells=[(1,0),(1,1),(0,1),(2,1),(1,2),(1,3)]
    labels=[(1,3,'A'),(1,2,'B'),(1,1,'C'),(1,0,'D'),(0,1,'E'),(2,1,'F')]
    t=patron('sol-7',cells,s=.8,labels=labels)
    dessin('sol-7',t,'Le patron en croix : les faces opposées sont séparées par une face.')
    META['sol-7']={'type':'patron','cells':cells}
    cells=[(1,0),(1,1),(1,2),(1,3),(0,1)]
    t=patron('sol-8',cells,s=.8,sol_cells=[(2,1,'')],bad_cells=[(0,0)])
    dessin('sol-8',t,'Cinq faces posées : la face verte complète un patron ; la position barrée créerait un bloc carré interdit.')
    META['sol-8']={'type':'patron','cells':cells}
    cubes=[(i,j,0) for i in range(3) for j in range(2)]+[(0,0,1),(1,0,1),(0,1,1)]+[(0,0,2)]
    assemblage('sol-9',cubes,'Compter étage par étage : six cubes, puis trois, puis un.')
    cubes10=[(0,0,0),(0,0,1),(1,0,0),(2,0,0),(2,0,1),(2,0,2)]
    t=''
    for (i,j,k) in sorted(cubes10,key=lambda c:(-c[1],c[2],c[0])):t+=cube3(i,j,k)
    t+=r'\begin{scope}[shift={(3.6,0)}]\fill[otNavy!35](0,0)rectangle(1,1);\fill[otNavy!35](1,0)rectangle(2,2);\fill[otNavy!35](2,0)rectangle(3,3);\draw[otRule!80](0,0)grid(3,3);\node[below,font=\scriptsize]at(1.5,-.1){(1)};\end{scope}'
    t+=r'\begin{scope}[shift={(7.3,0)}]\fill[otNavy!35](0,0)rectangle(1,2);\fill[otNavy!35](1,0)rectangle(2,1);\fill[otNavy!35](2,0)rectangle(3,3);\draw[otRule!80](0,0)grid(3,3);\node[below,font=\scriptsize]at(1.5,-.1){(2)};\end{scope}'
    t+=r'\begin{scope}[shift={(11.0,0)}]\fill[otNavy!35](0,0)rectangle(3,1);\draw[otRule!80](0,0)grid(3,1);\node[below,font=\scriptsize]at(1.5,-.1){(3)};\end{scope}'
    t=r'\begin{scope}[scale=.85]'+t+r'\end{scope}'
    dessin('sol-10',t,'L’assemblage et trois vignettes : vue de face, vue de dessus, et une vue impossible.')
    META['sol-10']={'type':'assemblage','cubes':len(cubes10)}
    cells=[(1,0),(1,1),(0,1),(2,1),(1,2),(1,3)]
    t=r'\geoSolution{'+patron('x',cells,s=.7).replace('geoTrait','geoReponse')+r'\node[font=\tiny,otGreenDark]at(2.6,2.6){carrés de 3 cm};}'
    t+=r'\geoEnonce{\node[font=\tiny,otMuted]at(2,1.2){construction à faire en vraie grandeur};}'
    dessin('sol-11',t,'Six carrés de 3 cm en croix ; le pliage referme le cube. Échelle réduite au corrigé.')
    META['sol-11']={'type':'patron','cells':cells}
    cubes7=[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1)]
    assemblage('sol-12',cubes7,'Sept cubes : il manque un cube au coin supérieur pour fermer le grand cube de côté 2.')
    t=grille(5,4)
    t+=r'\node[font=\tiny]at(.5,3.55){départ};\fill[otNavy](.5,3.3)circle(2pt);\draw[otNavy,->](.5,3.3)--(1.1,3.3);'
    t+=r'\draw[otNavy,line width=1.2pt,->](.5,3.3)--(3.5,3.3)--(3.5,2.3)--(.5,2.3);'
    t+=r'\node[font=\tiny]at(.5,1.95){but};'
    dessin('sol-13',rf'\begin{{scope}}[scale=.72]{t}\end{{scope}}','Le chemin dessiné se code en avancées et quarts de tour, du point de vue du pion.')
    META['sol-13']={'type':'script','numero':9}
    t=grille(5,4)
    t+=r'\node[font=\tiny]at(.5,.2){départ};\fill[otNavy](.5,.5)circle(2pt);\draw[otNavy,->](.5,.5)--(1.1,.5);'
    t+=r'\geoSolution{\draw[geoReponse,line width=1.2pt,->](.5,.5)--(2.5,.5)--(2.5,2.5)--(1.5,2.5);\fill[otGreenDark](1.5,2.5)circle(2pt)node[above,geoLabel]{arrivée};}'
    dessin('sol-14',rf'\begin{{scope}}[scale=.72]{t}\end{{scope}}','Exécuter pas à pas : l’orientation change à chaque quart de tour.')
    META['sol-14']={'type':'script','numero':10}
    cells=[(1,0),(1,1),(0,1),(2,1),(1,2),(1,3)]
    labels=[(1,3,'1'),(1,2,'2'),(0,1,'3')]
    t=patron('sol-15',cells,s=.8,labels=labels,sol_cells=[(1,1,'6'),(1,0,'5'),(2,1,'4')])
    dessin('sol-15',t,'Les faces opposées d’un dé totalisent 7 ; sur le patron, elles sont séparées par une face.')
    META['sol-15']={'type':'patron','cells':cells}
    cells=[(1,0),(1,1),(0,1),(2,1),(1,2),(1,3)]
    t=patron('cp',cells,s=.8,labels=[(1,1,'fond')])
    dessin('cours-patron',t,'Un patron du cube : six carrés qui se replient sans se superposer.')
    META['cours-patron']={'type':'patron','cells':cells}

# ================================================================= données et hasard
def statistiques():
    barres_diag('don-4',['lun','mar','mer','jeu','ven'],[8,12,10,18,14],2,leg='Nombre de livres empruntés chaque jour ; une graduation vaut 2 livres.')
    courbe_fig('don-5',[6,8,10,12,14,16,18],[9,12,16,20,21,19,16],[(6,'6 h'),(8,'8 h'),(10,'10 h'),(12,'12 h'),(14,'14 h'),(16,'16 h'),(18,'18 h')],3,leg='Température au fil de la journée, en degrés Celsius.')
    barres_diag('don-6',['pomme','fraise','cerise','banane'],[7,9,5,4],1,sol=True,leg='Le diagramme à construire figure en vert au corrigé ; une graduation vaut 1 élève.')
    t=r'\draw[otMuted,->](0,0)--(7.6,0)node[below left,font=\tiny]{âge (semaines)};\draw[otMuted,->](0,0)--(0,4.4)node[above,font=\tiny]{masse (kg)};'
    for v in range(1,7):t+=rf'\draw[otRule!80,line width=.3pt]({v*1.1},0)--({v*1.1},4.0);\node[below,font=\tiny]at({v*1.1},0){{{v}}};'
    for v in range(1,6):t+=rf'\draw[otRule!80,line width=.3pt](0,{v*.75})--(7.0,{v*.75});\node[left,font=\tiny]at(0,{v*.75}){{{v}}};'
    for (a,m) in [(1,1),(2,2),(4,3),(6,5)]:t+=rf'\fill[otNavy]({a*1.1},{m*.75})circle(1.7pt);'
    dessin('don-7',t,'Chaque point donne l’âge et la masse : lire l’abscisse puis l’ordonnée.')
    META['don-7']={'type':'points','donnees':[(1,1),(2,2),(4,3),(6,5)]}
    courbe_fig('don-9',list(range(1,13)),[4,5,8,11,15,19,22,21,17,12,8,5],[(1,'J'),(2,'F'),(3,'M'),(4,'A'),(5,'M'),(6,'J'),(7,'J'),(8,'A'),(9,'S'),(10,'O'),(11,'N'),(12,'D')],5,leg='Températures moyennes mensuelles d’une ville, en degrés Celsius.')
    barres_diag('don-10',['lun','mar','mer'],[8,12,6],2,wrong=(1,10),leg='Une barre ne correspond pas au tableau ; la correction figure en vert.')
    courbe_fig('don-13',[0,1,2,3,4,5,6],[0,2,4,6,8,13,16],[(0,'0'),(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6')],5,ligne=10,leg='Hauteur de la plante, en centimètres, semaine après semaine ; la ligne des 10 cm est marquée.')
    courbe_fig('don-14',[1,2,3,4],[7,12,18,10],[(1,'hiver'),(2,'print.'),(3,'été'),(4,'automne')],5,second=[3,14,24,9],names=['Brestel','Lyonnet'],leg='Deux villes sur les mêmes axes : Brestel en bleu, Lyonnet en vert.')
    t=r'\draw[otMuted,->](0,0)--(7.6,0)node[below left,font=\tiny]{nombre de tours};\draw[otMuted,->](0,0)--(0,3.6)node[above,font=\tiny]{distance (m)};'
    dessin('cours-donnees',pile([(0,'enquête : poser une question','entree'),(0,'recueillir les réponses','calcul'),(0,'compter les effectifs','calcul'),(0,'présenter : tableau, barres ou courbe','evenement')]),'De la question au graphique : les étapes d’une enquête.')
    META['cours-donnees']={'type':'libre'}

def probabilites():
    def echelle(nom,sol=(),leg='L’échelle va de l’impossible au certain ; le milieu marque une chance sur deux.'):
        t=r'\draw[otNavy,line width=1.2pt,->](0,0)--(8.4,0);'
        for x,l in [(0,'impossible'),(2.1,'peu probable'),(4.2,'une chance sur deux'),(6.3,'probable'),(8.4,'certain')]:
            t+=rf'\draw[otNavy]({x},-.1)--({x},.1);\node[below,font=\tiny,align=center]at({x},-.15){{{l}}};'
        t+=r'\geoSolution{'+''.join(rf'\fill[otGreenDark]({x},.28)circle(1.6pt)node[above,font=\tiny,otGreenDark]{{{l}}};' for x,l in sol)+r'}'
        dessin(nom,t,leg)
        META[nom]={'type':'echelle'}
    echelle('cours-echelle')
    echelle('pro-5',sol=[(8.4,'janvier'),(1.4,'obtenir 3'),(0,'boule jaune')],leg='Les trois évènements placés en vert : certain, peu probable, impossible.')
    t=''
    for i in range(6):
        t+=rf'\draw[geoTrait]({i*1.1},0)rectangle({i*1.1+.9},.9);\node[font=\small]at({i*1.1+.45},.45){{{i+1}}};'
    t+=r'\geoSolution{'+''.join(rf'\draw[geoReponse]({i*1.1},0)rectangle({i*1.1+.9},.9);' for i in [1,3,5])+r'\node[right,font=\tiny,otGreenDark]at(6.7,.45){trois issues paires};}'
    dessin('pro-6',t,'Les six issues du dé ; celles qui réalisent « obtenir un nombre pair » sont entourées en vert.')
    META['pro-6']={'type':'libre'}
    urne('pro-7',['R','B','B','B'],leg='Quatre boules indiscernables au toucher : les issues sont les boules, pas les couleurs.')
    t=''
    for i,(a,lab) in enumerate([(180,'A'),(120,'B'),(60,'C')]):
        pass
    angles=[180,120,60];labels=['A','B','C']
    roue('pro-8',angles,labels,leg='Les secteurs n’ont pas la même taille : les issues ne sont pas équiprobables.')
    urne('pro-9',['R','R','R','R','R','B','B'],leg='Cinq jetons rouges et deux bleus : sept issues en tout.')
    roue('pro-13',[45]*8,['P','P','P','P','B','B','B','Pe'],colors=['otNavy!25']*4+['otGreen!40']*3+['otOrange!55'],leg='Huit secteurs identiques : P perdu, B bonbon, Pe peluche.')
    urne('pro-15',['R','R','V','V','V','N','N','N','N','N'],leg='Deux rouges, trois vertes et cinq noires : dix issues équiprobables.')

def annexes():
    t=bandefrag(0,0,8,3)
    t+=r'\geoSolution{}'
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
