"""Figures vectorielles de Sixième, avec réponses conditionnelles et métadonnées de contrôle."""
from pathlib import Path
from math import cos,sin,radians,atan2,degrees,hypot,sqrt,tan,pi
from modele import figure,FIGURES
from outils_figures import dessin,pile
from donnees_scripts import SCRIPTS,lignes,executer
META={}

# ================================================================= outils généraux
def C(p):return f'({p[0]:.3f},{p[1]:.3f})'
def answer(txt):
    return r'\geoEnonce{\textcolor{otMuted}{?}}\geoSolution{\textcolor{otGreenDark}{'+txt+'}}'
def sol(t):return r'\geoSolution{'+t+'}'
def dotpt(x,y,lab='',where='above',color='otNavy'):
    t=rf'\fill[{color}]({float(x):.3f},{float(y):.3f})circle(1.6pt)'
    if lab:t+=rf'node[{where},geoLabel]{{$ {lab} $}}'
    return t+';'
def P(p,lab='',where='above',color='otNavy'):return dotpt(p[0],p[1],lab,where,color)
def L(p,t,where='above',size=r'\small',color='otInk'):
    return rf'\node[{where},font={size},inner sep=1.5pt,text={color}]at{C(p)}{{$ {t} $}};'
def T(p,t,where='',size=r'\scriptsize',color='otInk'):
    opt=(where+',' if where else '')+rf'font={size},inner sep=1.2pt,text={color}'
    return rf'\node[{opt}]at{C(p)}{{{t}}};'
def grille(w,h,x0=0,y0=0):
    t=''
    for i in range(w+1):t+=rf'\draw[otRule!75,line width=.25pt]({x0+i},{y0})--({x0+i},{y0+h});'
    for j in range(h+1):t+=rf'\draw[otRule!75,line width=.25pt]({x0},{y0+j})--({x0+w},{y0+j});'
    return t
def points_grille(w,h):
    return ''.join(rf'\fill[otMuted!70]({i},{j})circle(.9pt);' for i in range(w+1) for j in range(h+1))
def poly(pts,style='geoTrait',close=True,fill=''):
    core='--'.join(C(p) for p in pts)+('--cycle' if close else '')
    t=''
    if fill:t+=rf'\fill[{fill}]'+core+';'
    return t+rf'\draw[{style}]'+core+';'
def seg(a,b,style='geoTrait'):return rf'\draw[{style}]{C(a)}--{C(b)};'
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(a,k):return (a[0]*k,a[1]*k)
def dist(a,b):return hypot(a[0]-b[0],a[1]-b[1])
def unit(a,b):
    d=dist(a,b);return ((b[0]-a[0])/d,(b[1]-a[1])/d)
def direc(a,b):return degrees(atan2(b[1]-a[1],b[0]-a[0]))
def polar(o,ang,r):return (o[0]+r*cos(radians(ang)),o[1]+r*sin(radians(ang)))
def mid(a,b):return ((a[0]+b[0])/2,(a[1]+b[1])/2)
def foot(p,a,b):
    u=unit(a,b);v=sub(p,a);k=v[0]*u[0]+v[1]*u[1];return add(a,mul(u,k))
def reflect(p,a,b):
    h=foot(p,a,b);return (2*h[0]-p[0],2*h[1]-p[1])
def inter_cc(o1,r1,o2,r2):
    d=dist(o1,o2);x=(r1*r1-r2*r2+d*d)/(2*d);h2=r1*r1-x*x
    if h2<-1e-9:return []
    h=sqrt(max(h2,0));u=unit(o1,o2);n=(-u[1],u[0]);p=add(o1,mul(u,x))
    return [add(p,mul(n,h)),add(p,mul(n,-h))] if h>1e-9 else [p]
def inter_ll(p,u,q,v):
    det=u[0]*(-v[1])+v[0]*u[1]
    t=((q[0]-p[0])*(-v[1])+v[0]*(q[1]-p[1]))/det
    return add(p,mul(u,t))
def circumcenter(a,b,c):
    d=2*(a[0]*(b[1]-c[1])+b[0]*(c[1]-a[1])+c[0]*(a[1]-b[1]))
    ux=((a[0]**2+a[1]**2)*(b[1]-c[1])+(b[0]**2+b[1]**2)*(c[1]-a[1])+(c[0]**2+c[1]**2)*(a[1]-b[1]))/d
    uy=((a[0]**2+a[1]**2)*(c[0]-b[0])+(b[0]**2+b[1]**2)*(a[0]-c[0])+(c[0]**2+c[1]**2)*(b[0]-a[0]))/d
    return (ux,uy)
def angle_en(v,a,b):
    x=abs(direc(v,a)-direc(v,b))%360
    return min(x,360-x)
def ligne(a,b,ext=1.0,style='geoTrait'):
    u=unit(a,b);return seg(add(a,mul(u,-ext)),add(b,mul(u,ext)),style)
def demi(a,b,ext=1.0,style='geoTrait'):
    u=unit(a,b);return seg(a,add(b,mul(u,ext)),style)
def marque(a,b,n=1,color='otNavy',s=.12):
    m=mid(a,b);u=unit(a,b);nn=(-u[1],u[0]);t=''
    for k in range(n):
        c0=add(m,mul(u,(k-(n-1)/2)*.08))
        t+=rf'\draw[{color},line width=.6pt]{C(add(c0,mul(nn,s)))}--{C(add(c0,mul(nn,-s)))};'
    return t
def droit(v,a,b,s=.22,color='otNavy'):
    u=unit(v,a);w=unit(v,b)
    p1=add(v,mul(u,s));p3=add(v,mul(w,s));p2=add(p1,mul(w,s))
    return rf'\draw[{color},line width=.5pt]{C(p1)}--{C(p2)}--{C(p3)};'
def arcang(v,a1,a2,r=.6,color='otGreenDark',label='',lr=None,fill=''):
    sweep=(a2-a1)%360
    t=''
    if fill:t+=rf'\fill[{fill}]{C(v)}--([shift={{{C(v)}}}]{a1:.2f}:{r})arc({a1:.2f}:{a1+sweep:.2f}:{r})--cycle;'
    t+=rf'\draw[{color},line width=.6pt]([shift={{{C(v)}}}]{a1:.2f}:{r})arc({a1:.2f}:{a1+sweep:.2f}:{r});'
    if label:
        p=polar(v,a1+sweep/2,lr if lr else r+.34)
        t+=rf'\node[font=\scriptsize,inner sep=.5pt]at{C(p)}{{{label}}};'
    return t
def arc_at(v,a,b,r=.6,color='otGreenDark',label='',lr=None,fill=''):
    a1=direc(v,a);a2=direc(v,b)
    if (a2-a1)%360>180:a1,a2=a2,a1
    return arcang(v,a1,a2,r,color,label,lr,fill)
def arc_cercle(o,r,ac,half=14,style='geoAide'):
    return rf'\draw[{style}]([shift={{{C(o)}}}]{ac-half:.2f}:{r:.3f})arc({ac-half:.2f}:{ac+half:.2f}:{r:.3f});'
def cercle(o,r,style='geoTrait'):return rf'\draw[{style}]{C(o)}circle({r:.3f});'
def accolade(a,b,txt,where='above',color='otMuted'):
    return rf'\draw[decorate,decoration={{brace,amplitude=4pt}},{color}]{C(a)}--{C(b)}node[midway,{where}=4pt,font=\scriptsize,text=otInk]{{{txt}}};'
def echelle(nom,tex,scale,leg):
    dessin(nom,rf'\begin{{scope}}[scale={scale}]'+tex+r'\end{scope}',leg)

# ================================================================= droites graduées
def axe(lo,hi,pas,labels,y=0,x0=0,w=9.0,minor=None,mid_=None,points=(),sol_=()):
    X=lambda v:x0+(v-lo)*w/(hi-lo)
    t=rf'\draw[otMuted,->]({x0:.3f},{y:.3f})--({x0+w+.35:.3f},{y:.3f});'
    for step,hgt,lw in [(minor,.06,.45),(mid_,.09,.6),(pas,.13,.9)]:
        if not step:continue
        k=0
        while lo+k*step<=hi+1e-9:
            xv=X(lo+k*step);t+=rf'\draw[otMuted,line width={lw}pt]({xv:.3f},{y-hgt:.3f})--({xv:.3f},{y+hgt:.3f});';k+=1
    for val,txt in labels:t+=rf'\node[below,font=\scriptsize]at({X(val):.3f},{y-.14:.3f}){{$ {txt} $}};'
    for lab,val in points:t+=dotpt(X(val),y,lab,'above')
    if sol_:t+=sol(''.join(dotpt(X(v),y,l,'above','otGreenDark') for l,v in sol_))
    return t,X
def droiteg(nom,lo,hi,pas,labels,points=(),sol_=(),minor=None,mid_=None,leg='Les graduations sont régulières ; lire la valeur d’un petit intervalle avant les positions.'):
    t,X=axe(lo,hi,pas,labels,minor=minor,mid_=mid_,points=points,sol_=sol_)
    dessin(nom,t,leg)
    META[nom]={'type':'droite','bornes':[lo,hi],'points':[v for _,v in points],'solutions':[v for _,v in sol_]}

# ================================================================= représentations
def grille100(x0,cols,extra,s=.3,col='otNavy!35'):
    t=''
    for i in range(cols):t+=rf'\fill[{col}]({x0+i*s:.3f},0)rectangle({x0+(i+1)*s:.3f},{10*s:.3f});'
    for j in range(extra):t+=rf'\fill[{col}]({x0+cols*s:.3f},{j*s:.3f})rectangle({x0+(cols+1)*s:.3f},{(j+1)*s:.3f});'
    for k in range(1,10):
        t+=rf'\draw[otRule,line width=.25pt]({x0+k*s:.3f},0)--({x0+k*s:.3f},{10*s:.3f});'
        t+=rf'\draw[otRule,line width=.25pt]({x0:.3f},{k*s:.3f})--({x0+10*s:.3f},{k*s:.3f});'
    return t+rf'\draw[geoTrait]({x0:.3f},0)rectangle({x0+10*s:.3f},{10*s:.3f});'
def bande_parts(x0,y,w,n,h=.6,fills=None,txt=None,lines='geoTrait'):
    t='';cw=w/n
    for i,col in (fills or {}).items():t+=rf'\fill[{col}]({x0+i*cw:.3f},{y:.3f})rectangle({x0+(i+1)*cw:.3f},{y+h:.3f});'
    t+=rf'\draw[geoTrait]({x0:.3f},{y:.3f})rectangle({x0+w:.3f},{y+h:.3f});'
    for i in range(1,n):t+=rf'\draw[{lines}]({x0+i*cw:.3f},{y:.3f})--({x0+i*cw:.3f},{y+h:.3f});'
    for i,s in (txt or {}).items():t+=rf'\node[font=\scriptsize]at({x0+(i+.5)*cw:.3f},{y+h/2:.3f}){{{s}}};'
    return t
def barre(x,y,w,txt='',h=.5,fill='otNavy!15'):
    return rf'\filldraw[draw=otNavy,fill={fill},line width=.6pt]({x:.3f},{y:.3f})rectangle({x+w:.3f},{y+h:.3f});'+(rf'\node[font=\scriptsize]at({x+w/2:.3f},{y+h/2:.3f}){{{txt}}};' if txt else '')
def barres_diag(nom,cats,vals,step,sol_=False,unit=4.2,leg='',ylab=''):
    m=max(vals);sy=unit/m;w=.62;gap=1.15
    t=rf'\draw[otMuted,->](-.3,0)--({len(cats)*gap+.4},0);\draw[otMuted,->](0,0)--(0,{unit+.5});'
    if ylab:t+=rf'\node[above right,font=\tiny]at(0,{unit+.5}){{{ylab}}};'
    v=step
    while v<=m+1e-9:
        t+=rf'\draw[otRule!80,line width=.3pt](0,{v*sy:.3f})--({len(cats)*gap+.2},{v*sy:.3f});\node[left,font=\tiny]at(0,{v*sy:.3f}){{{v}}};'
        v+=step
    for i,(c,val) in enumerate(zip(cats,vals)):
        x=.35+i*gap
        if sol_:t+=sol(rf'\fill[otGreen!45]({x},0)rectangle({x+w},{val*sy:.3f});\draw[otGreenDark]({x},0)rectangle({x+w},{val*sy:.3f});')
        else:t+=rf'\fill[otNavy!35]({x},0)rectangle({x+w},{val*sy:.3f});\draw[otNavy]({x},0)rectangle({x+w},{val*sy:.3f});'
        t+=rf'\node[below,font=\tiny]at({x+w/2},0){{{c}}};'
    dessin(nom,t,leg or 'La hauteur de chaque barre se lit sur l’axe gradué.')
    META[nom]={'type':'barres','valeurs':list(vals),'pas':step}
def courbe(xs,ys,xmin,xmax,ymin,ymax,xlabels,ystep,w=8.6,h=4.0,ylabs=None,color='otNavy',dots=True,x0=0,y0=0):
    sx=w/(xmax-xmin);sy=h/(ymax-ymin)
    X=lambda v:x0+(v-xmin)*sx;Y=lambda v:y0+(v-ymin)*sy
    t=rf'\draw[otMuted,->]({x0},{y0})--({x0+w+.4:.3f},{y0});\draw[otMuted,->]({x0},{y0})--({x0},{y0+h+.4:.3f});'
    v=ymin
    while v<=ymax+1e-9:
        lab=(ylabs or {}).get(round(v,4),f'{v:g}'.replace('.','{,}'))
        t+=rf'\draw[otRule!80,line width=.3pt]({x0},{Y(v):.3f})--({x0+w:.3f},{Y(v):.3f});\node[left,font=\tiny]at({x0},{Y(v):.3f}){{${lab}$}};'
        v+=ystep
    for xv,xl in xlabels:t+=rf'\draw[otRule!80,line width=.3pt]({X(xv):.3f},{y0})--({X(xv):.3f},{y0+h:.3f});\node[below,font=\tiny]at({X(xv):.3f},{y0}){{{xl}}};'
    t+=rf'\draw[{color},line width=1pt]'+' -- '.join(f'({X(x):.3f},{Y(y):.3f})' for x,y in zip(xs,ys))+';'
    if dots:
        for x,y in zip(xs,ys):t+=rf'\fill[{color}]({X(x):.3f},{Y(y):.3f})circle(1.4pt);'
    return t,X,Y
def circulaire_tex(parts,labels,r=1.7,cols=None,x0=0):
    t='';start=90;total=sum(parts)
    cols=cols or ['otNavy!35','otGreen!40','otOrange!45','otNavy!15']
    for p,lab,col in zip(parts,labels,cols):
        a=360*p/total;end=start-a;midv=(start+end)/2
        t+=rf'\filldraw[draw=white,line width=1pt,fill={col}]({x0},0)--([shift={{({x0},0)}}]{start}:{r})arc({start}:{end:.2f}:{r})--cycle;'
        t+=rf'\node[font=\tiny]at([shift={{({x0},0)}}]{midv:.2f}:{r*.6:.2f}){{{lab}}};'
        start=end
    return t+rf'\draw[otNavy,line width=.9pt]({x0},0)circle({r});'
def urne_tex(items,x0=0,per_row=5):
    rows=(len(items)+per_row-1)//per_row
    w=per_row*1.0
    t=rf'\draw[otMuted,line width=.9pt]({x0-.5},{rows*1.0-.1})--({x0-.5},-.55)--({x0+w-.4},-.55)--({x0+w-.4},{rows*1.0-.1});'
    for i,lab in enumerate(items):
        color={'R':'otOrange!60','B':'otNavy!32','V':'otGreen!55','N':'otInk!45'}[lab[0]]
        t+=rf'\node[circle,draw=otMuted,fill={color},minimum size=6.2mm,font=\scriptsize]at({x0+i%per_row*1.0},{(rows-1)*1.0-i//per_row*1.0}){{{lab}}};'
    return t
def roue_tex(angles,labels,colors=None,shift=0,r=1.5):
    assert sum(angles)==360
    cols=colors or ['otNavy!30','otGreen!40','otOrange!45','otNavy!12','otGreen!20','otOrange!25','otNavy!45','otOrange!60']
    t=rf'\begin{{scope}}[shift={{({shift},0)}}]';start=90
    for a,lab,col in zip(angles,labels,cols):
        end=start+a;midv=(start+end)/2
        t+=rf'\filldraw[draw=white,line width=.8pt,fill={col}](0,0)--({start}:{r})arc({start}:{end}:{r})--cycle;'
        t+=rf'\node[font=\scriptsize]at({midv}:{r*.66:.2f}){{{lab}}};'
        start=end
    return t+rf'\draw[otNavy,line width=.9pt](0,0)circle({r});\fill[otInk](90:{r+.15})--(84:{r+.32})--(96:{r+.32})--cycle;\end{{scope}}'
def horloge(cx,h,m,r=1.35,cy=0):
    t=rf'\begin{{scope}}[shift={{({cx},{cy})}}]\draw[geoTrait](0,0)circle({r});'
    for k in range(60):
        a=90-k*6
        t+=rf'\draw[otMuted,line width={".6" if k%5==0 else ".25"}pt]({a}:{r*(.86 if k%5==0 else .93):.3f})--({a}:{r});'
    for k in range(12):
        a=90-k*30;t+=rf'\node[font=\tiny]at({a}:{r*.72:.3f}){{{12 if k==0 else k}}};'
    ah=90-(h%12)*30-m*0.5;am=90-m*6
    t+=rf'\draw[line width=1.6pt,otNavy](0,0)--({ah}:{r*.5:.3f});\draw[line width=1pt,otNavy](0,0)--({am}:{r*.8:.3f});\fill[otNavy](0,0)circle(1.4pt);'
    return t+r'\end{scope}',ah,am

# ================================================================= cubes et solides
def cube3(i,j,k,s=.55,dx=.25,dy=.18,green=False):
    x=i*s+j*dx;y=k*s+j*dy
    d,f1,f2,f3=('otGreenDark','otGreen!12','otGreen!30','otGreen!45') if green else ('otNavy','white','otNavy!14','otNavy!26')
    t=rf'\filldraw[draw={d},fill={f1},line width=.6pt]({x:.3f},{y:.3f})rectangle({x+s:.3f},{y+s:.3f});'
    t+=rf'\filldraw[draw={d},fill={f2},line width=.6pt]({x:.3f},{y+s:.3f})--({x+dx:.3f},{y+s+dy:.3f})--({x+s+dx:.3f},{y+s+dy:.3f})--({x+s:.3f},{y+s:.3f})--cycle;'
    t+=rf'\filldraw[draw={d},fill={f3},line width=.6pt]({x+s:.3f},{y:.3f})--({x+s+dx:.3f},{y+dy:.3f})--({x+s+dx:.3f},{y+s+dy:.3f})--({x+s:.3f},{y+s:.3f})--cycle;'
    return t
def cubes_tex(cubes,sol_cubes=(),s=.55,dx=.25,dy=.18,x0=0,y0=0):
    allc=[(c,False) for c in cubes]+[(c,True) for c in sol_cubes]
    t=rf'\begin{{scope}}[shift={{({x0},{y0})}}]'
    for (i,j,k),g in sorted(allc,key=lambda c:(-c[0][1],c[0][2],c[0][0])):
        q=cube3(i,j,k,s,dx,dy,g)
        t+=sol(q) if g else q
    return t+r'\end{scope}'
def assemblage(nom,cubes,leg='Les cubes cachés portent les étages supérieurs.',sol_cubes=(),extra='',s=.55):
    dessin(nom,cubes_tex(cubes,sol_cubes,s=s)+extra,leg)
    META[nom]={'type':'assemblage','cubes':len(cubes),'ajout':len(sol_cubes),'liste':sorted(cubes)}
def vue(x0,y0,cells,s=.4,label='',green=False,nums=None):
    col,fill=('otGreenDark','otGreen!35') if green else ('otNavy','otNavy!20')
    t=''
    for (c,r) in cells:t+=rf'\filldraw[draw={col},fill={fill},line width=.6pt]({x0+c*s:.3f},{y0+r*s:.3f})rectangle({x0+(c+1)*s:.3f},{y0+(r+1)*s:.3f});'
    for (c,r),n in (nums or {}).items():t+=rf'\node[font=\scriptsize]at({x0+(c+.5)*s:.3f},{y0+(r+.5)*s:.3f}){{{n}}};'
    if label:t+=rf'\node[below,font=\tiny]at({x0+max(c for c,_ in cells)*s/2+s/2:.3f},{y0-.05:.3f}){{{label}}};'
    return t
def s_pave(x0,y0,w=1.2,h=.8,dx=.45,dy=.33,lab=''):
    A=(x0,y0);B=(x0+w,y0);Cc=(x0+w,y0+h);D=(x0,y0+h)
    a,b,c,d=[add(p,(dx,dy)) for p in (A,B,Cc,D)]
    t=poly([A,B,Cc,D])+poly([D,d,c,Cc],close=False)+poly([B,b,c],close=False)
    t+=rf'\draw[otMuted,dashed,line width=.5pt]{C(A)}--{C(a)}--{C(b)} {C(a)}--{C(d)};'
    return t+(T((x0+(w+dx)/2,y0-.12),lab,'below',r'\tiny') if lab else '')
def s_prisme(x0,y0,b=1.1,h=.9,dx=.55,dy=.32,lab=''):
    F1=(x0,y0);F2=(x0+b,y0);F3=(x0+b/2,y0+h)
    B1,B2,B3=[add(p,(dx,dy)) for p in (F1,F2,F3)]
    t=poly([F1,F2,F3])+seg(F3,B3)+seg(F2,B2)+seg(B2,B3)+seg(B3,B1)
    t+=rf'\draw[otMuted,dashed,line width=.5pt]{C(F1)}--{C(B1)}--{C(B2)};'
    return t+(T((x0+(b+dx)/2,y0-.12),lab,'below',r'\tiny') if lab else '')
def s_pyramide(x0,y0,w=1.2,dx=.5,dy=.32,h=1.2,lab=''):
    A=(x0,y0);B=(x0+w,y0);Cc=(x0+w+dx,y0+dy);D=(x0+dx,y0+dy);S=(x0+(w+dx)/2,y0+dy/2+h)
    t=poly([A,B,Cc],close=False)+seg(S,A)+seg(S,B)+seg(S,Cc)
    t+=rf'\draw[otMuted,dashed,line width=.5pt]{C(A)}--{C(D)}--{C(Cc)} {C(D)}--{C(S)};'
    return t+(T((x0+(w+dx)/2,y0-.12),lab,'below',r'\tiny') if lab else '')
def s_cylindre(x0,y0,r=.55,h=1.1,lab=''):
    t=rf'\draw[geoTrait]({x0-r:.3f},{y0:.3f})--({x0-r:.3f},{y0+h:.3f}) ({x0+r:.3f},{y0:.3f})--({x0+r:.3f},{y0+h:.3f});'
    t+=rf'\draw[geoTrait]({x0:.3f},{y0+h:.3f})ellipse({r} and {r*.32:.3f});\draw[geoTrait]({x0-r:.3f},{y0:.3f})arc(180:360:{r} and {r*.32:.3f});'
    t+=rf'\draw[otMuted,dashed,line width=.5pt]({x0-r:.3f},{y0:.3f})arc(180:0:{r} and {r*.32:.3f});'
    return t+(T((x0,y0-r*.32-.1),lab,'below',r'\tiny') if lab else '')
def s_cone(x0,y0,r=.6,h=1.3,lab=''):
    t=rf'\draw[geoTrait]({x0-r:.3f},{y0:.3f})--({x0:.3f},{y0+h:.3f})--({x0+r:.3f},{y0:.3f});\draw[geoTrait]({x0-r:.3f},{y0:.3f})arc(180:360:{r} and {r*.32:.3f});'
    t+=rf'\draw[otMuted,dashed,line width=.5pt]({x0-r:.3f},{y0:.3f})arc(180:0:{r} and {r*.32:.3f});'
    return t+(T((x0,y0-r*.32-.1),lab,'below',r'\tiny') if lab else '')
def s_boule(x0,y0,r=.65,lab=''):
    t=rf'\shade[ball color=otNavy!18,opacity=.6]({x0:.3f},{y0+r:.3f})circle({r});\draw[geoTrait]({x0:.3f},{y0+r:.3f})circle({r});'
    t+=rf'\draw[geoTrait]({x0-r:.3f},{y0+r:.3f})arc(180:360:{r} and {r*.3:.3f});\draw[otMuted,dashed,line width=.5pt]({x0-r:.3f},{y0+r:.3f})arc(180:0:{r} and {r*.3:.3f});'
    return t+(T((x0,y0-.1),lab,'below',r'\tiny') if lab else '')

# ================================================================= symétries sur supports
def symaxe(nom,chains,axis,gw,gh,points=None,leg='Quadrillage de principe ; l’axe est en tirets.',closes=None,scale=.5,dots=False,image_visible=False):
    o,v=axis
    t=points_grille(gw,gh) if dots else grille(gw,gh)
    t+=(rf'\draw[otOrange,dashed,line width=1pt]({v},-.3)--({v},{gh+.3});' if o=='v' else rf'\draw[otOrange,dashed,line width=1pt](-.3,{v})--({gw+.3},{v});')
    orig=[];imgs=[];s=''
    for n,ch in enumerate(chains):
        cl=closes[n] if closes else len(ch)>2
        t+=poly(ch,'geoTrait',close=cl)
        mi=[(2*v-x,y) if o=='v' else (x,2*v-y) for (x,y) in ch]
        s+=poly(mi,'geoReponse',close=cl)
        orig+=list(ch);imgs+=mi
    for lab,x,y in (points or []):
        t+=dotpt(x,y,lab,'above left')
        mx,my=(2*v-x,y) if o=='v' else (x,2*v-y)
        s+=dotpt(mx,my,lab+"'",'above right','otGreenDark')
        orig.append((x,y));imgs.append((mx,my))
    t+=sol(s)
    dessin(nom,rf'\begin{{scope}}[scale={scale}]{t}\end{{scope}}',leg)
    META[nom]={'type':'symetrie','axe':[o,v],'originaux':orig,'images':imgs,'grille':[gw,gh]}
def symdiag(nom,chains,g,points=None,leg='L’axe suit les diagonales des carreaux ; les écarts horizontaux et verticaux s’échangent.',scale=.55):
    t=grille(g,g)+rf'\draw[otOrange,dashed,line width=1pt](-.3,-.3)--({g+.3},{g+.3});'
    orig=[];imgs=[];s=''
    for ch in chains:
        t+=poly(ch,'geoTrait',close=len(ch)>2)
        mi=[(y,x) for (x,y) in ch];s+=poly(mi,'geoReponse',close=len(ch)>2)
        orig+=list(ch);imgs+=mi
    for lab,x,y in (points or []):
        t+=dotpt(x,y,lab,'above left');s+=dotpt(y,x,lab+"'",'below right','otGreenDark')
        orig.append((x,y));imgs.append((y,x))
    t+=sol(s)
    dessin(nom,rf'\begin{{scope}}[scale={scale}]{t}\end{{scope}}',leg)
    META[nom]={'type':'symdiag','originaux':orig,'images':imgs,'grille':g}
def sym_oblique_meta(nom,a,b,pairs):
    META[nom]={'type':'symoblique','axe':[a,b],'paires':pairs}

# ================================================================= programmes et quadrillages
def quad(w,h,s=.5,obstacles=(),marks=None,start=None,cap='E'):
    t=grille(w,h)
    for (c,r) in obstacles:t+=rf'\fill[otMuted!45]({c},{r})rectangle({c+1},{r+1});'
    if obstacles:t+=grille(w,h)
    for (c,r),txt in (marks or {}).items():t+=rf'\node[font=\scriptsize\bfseries,text=otNavy]at({c+.5},{r+.5}){{{txt}}};'
    if start:
        c,r=start;d={'E':(1,0),'N':(0,1),'O':(-1,0),'S':(0,-1)}[cap]
        t+=rf'\draw[otOrange,line width=1.2pt,-{{Stealth[length=2.2mm]}}]({c+.5-d[0]*.3},{r+.5-d[1]*.3})--({c+.5+d[0]*.35},{r+.5+d[1]*.35});'
    return t
def chemin(trace,start,color='otGreenDark',arrow=True):
    pts=[(start[0]+x+.5,start[1]+y+.5) for x,y in trace]
    return rf'\draw[{color},line width=1.4pt,{"-{Stealth[length=2.6mm]}" if arrow else ""}]'+'--'.join(f'({x:.2f},{y:.2f})' for x,y in pts)+';'

# ================================================================= chapitre 1 à 4
def nombres():
    t=grille100(0,3,4,s=.26)
    t+=T((3.0,2.1),r'3 colonnes : 3 dixièmes, $0{,}3$','right')+T((3.0,1.4),r'4 petits carrés : 4 centièmes, $0{,}04$','right')+T((3.0,.7),r'en tout : $0{,}34=\frac{34}{100}$','right')
    dessin('cours-centiemes',t,'L’unité est le grand carré, partagé en cent petits carrés.')
    META['cours-centiemes']={'type':'grille','valeurs':[3*10+4]}
    t=grille100(0,10,0)+grille100(3.5,10,0)+grille100(7.0,4,7)
    dessin('num-4',t,'Chaque grand carré représente une unité ; une colonne représente un dixième.')
    META['num-4']={'type':'grille','valeurs':[100,100,47]}
    # Repérage.
    t1,X1=axe(3,4,1,[(3,'3'),(3.4,'3{,}4'),(3.5,'3{,}5'),(4,'4')],y=1.7,minor=.1,points=[('A',3.47)])
    t2,X2=axe(3.4,3.5,.1,[(3.4,'3{,}4'),(3.45,'3{,}45'),(3.5,'3{,}5')],y=0,minor=.01,mid_=.05,points=[('A',3.47)])
    t=t1+t2+rf'\draw[otOrange,dashed]({X1(3.4):.3f},1.55)--({X2(3.4):.3f},.2) ({X1(3.5):.3f},1.55)--({X2(3.5):.3f},.2);'
    dessin('cours-droite-zoom',t,'En haut, l’unité est partagée en dixièmes ; en bas, on agrandit l’intervalle de 3,4 à 3,5, partagé en centièmes.')
    META['cours-droite-zoom']={'type':'droites','listes':[[3,4,[3.47]],[3.4,3.5,[3.47]]]}
    t,X=axe(7.3,7.4,.1,[(7.3,'7{,}3'),(7.35,'7{,}35'),(7.4,'7{,}4')],minor=.01,mid_=.05,points=[(r'7{,}36',7.36)])
    t+=rf'\draw[otGreenDark,->,line width=.8pt]({X(7.36)+.1:.3f},.62)to[bend left=20]({X(7.4)-.05:.3f},.62);'+T(((X(7.36)+X(7.4))/2,.95),'plus proche de 7,4','above',r'\scriptsize','otGreenDark')
    dessin('cours-arrondi',t,'7,36 est à 4 centièmes de 7,4 et à 6 centièmes de 7,3.')
    META['cours-arrondi']={'type':'droite','bornes':[7.3,7.4],'points':[7.36],'solutions':[]}
    droiteg('rep-1',0,3,1,[(0,'0'),(1,'1'),(2,'2'),(3,'3')],points=[('A',.6),('B',1.3),('C',2.8)],minor=.1,mid_=.5)
    droiteg('rep-2',5.2,5.4,.1,[(5.2,'5{,}2'),(5.3,'5{,}3'),(5.4,'5{,}4')],sol_=[('D',5.25),('E',5.38),('F',5.3)],minor=.01,mid_=.05,leg='Les petites graduations valent un centième ; les points demandés figurent en vert au corrigé.')
    droiteg('rep-8',1.4,1.5,.1,[(1.4,'1{,}4'),(1.45,'1{,}45'),(1.5,'1{,}5')],points=[('G',1.47),('H',1.415)],minor=.01,mid_=.05,leg='Entre 1,4 et 1,5, dix intervalles d’un centième.')
    # Calcul décimal.
    cols=['centaines','dizaines','unités','dixièmes','centièmes']
    t=''.join(T((i*1.5,1.05),c,'',r'\tiny','otMuted') for i,c in enumerate(cols))
    for i in range(6):t+=rf'\draw[otRule,line width=.4pt]({i*1.5-.75},1.3)--({i*1.5-.75},-1.65);'
    t+=rf'\draw[otOrange,line width=1.4pt](3.75,1.3)--(3.75,-1.65);'
    for x,d in [(3,'4'),(4.5,'5'),(6,'6')]:t+=T((x,0),rf'\large {d}')
    for x,d in [(0,'4'),(1.5,'5'),(3,'6')]:t+=T((x,-1.2),rf'\large {d}')
    t+=T((3.55,-.15),r'\large ,','','','otOrange')
    for x in [3,4.5,6]:t+=rf'\draw[otGreenDark,->,line width=.7pt]({x-.12},-.25)--({x-2.85},-.95);'
    t+=T((-1.3,0),r'$4{,}56$','',r'\small')+T((-1.3,-1.2),r'$456$','',r'\small')+T((7.2,-.6),r'$\times100$','right',r'\small','otGreenDark')
    dessin('cours-glisse',t,'Glisse-nombre : multiplier par 100 décale chaque chiffre de deux rangs vers la gauche ; la virgule reste en place.')
    META['cours-glisse']={'type':'libre'}
    k=2.0
    t=rf'\fill[otNavy!25](0,0)rectangle({2*k},{1*k});\fill[otNavy!12]({2*k},0)rectangle({2.3*k},{1*k});\fill[otGreen!25](0,{1*k})rectangle({2*k},{1.4*k});\fill[otOrange!35]({2*k},{1*k})rectangle({2.3*k},{1.4*k});'
    t+=rf'\draw[geoTrait](0,0)rectangle({2.3*k},{1.4*k});\draw[geoTrait]({2*k},0)--({2*k},{1.4*k}) (0,{1*k})--({2.3*k},{1*k});'
    t+=T((k,k/2),r'$2\times1=2$')+T((2.15*k,k/2),r'$0{,}3$','',r'\tiny')+T((k,1.2*k),r'$2\times0{,}4=0{,}8$')+T((2.15*k+.75,1.2*k),r'$0{,}12$','right',r'\tiny')
    t+=rf'\draw[otMuted,->,line width=.4pt]({2.15*k+.75},{1.2*k})--({2.15*k+.05},{1.2*k});'
    t+=T((k,-.05),'2 cm','below')+T((2.15*k,-.05),'0,3','below',r'\tiny')+T((-.05,k/2),'1 cm','left')+T((-.05,1.2*k),'0,4','left',r'\tiny')
    dessin('cours-rectangle-produit',t,'Le rectangle de 2,3 cm sur 1,4 cm découpé en quatre parties : $2+0{,}8+0{,}3+0{,}12=3{,}22$.')
    META['cours-rectangle-produit']={'type':'produit','parts':[2,.8,.3,.12],'total':3.22}
    k=1.2
    t=rf'\fill[otNavy!20](0,0)rectangle({3*k},{2.5*k});\fill[otOrange!35]({3*k},0)rectangle({3.2*k},{2.5*k});\draw[geoTrait](0,0)rectangle({3.2*k},{2.5*k});\draw[geoTrait]({3*k},0)--({3*k},{2.5*k});'
    t+=T((1.5*k,-.05),'3 cm','below')+T((3.1*k+.6,-.35),'0,2 cm','',r'\scriptsize')+rf'\draw[otMuted,line width=.4pt]({3.1*k},-.05)--({3.1*k+.35},-.3);'+T((-.05,1.25*k),'2,5 cm','left')
    t+=T((1.5*k,1.25*k),answer(r'$7{,}5\ \mathrm{cm}^2$'))+T((3.2*k+.45,1.25*k),answer(r'$0{,}5\ \mathrm{cm}^2$'),'right')+rf'\draw[otMuted,->,line width=.4pt]({3.2*k+.45},{1.25*k})--({3.1*k},{1.25*k});'
    dessin('cal-6',t,'Le rectangle est découpé en une partie de 3 cm de large et une bande de 0,2 cm.')
    META['cal-6']={'type':'produit','parts':[7.5,.5],'total':8}

def potence(entries,lines,div,quot,ncol,rows,xs=.36,ys=.52,notes=None):
    t=''
    for col,row,txt,ans in entries:
        t+=rf'\node[font=\small]at({col*xs:.3f},{-row*ys:.3f}){{{answer(txt) if ans else txt}}};'
    for row,c0,c1 in lines:t+=rf'\draw[otMuted,line width=.5pt]({(c0-.5)*xs:.3f},{-row*ys-.26:.3f})--({(c1+.5)*xs:.3f},{-row*ys-.26:.3f});'
    xb=(ncol-.4)*xs
    t+=rf'\draw[otNavy,line width=.8pt]({xb:.3f},.3)--({xb:.3f},{-rows*ys-.1:.3f});\draw[otNavy,line width=.8pt]({xb:.3f},-.26)--({xb+1.7:.3f},-.26);'
    t+=rf'\node[font=\small,anchor=west]at({xb+.2:.3f},0){{{div}}};\node[font=\small,anchor=west]at({xb+.2:.3f},{-ys:.3f}){{{quot}}};'
    for row,txt in (notes or []):t+=rf'\node[font=\scriptsize,text=otMuted,anchor=west]at({xb+2.2:.3f},{-row*ys:.3f}){{{txt}}};'
    return t
def division():
    t=r'\begin{scope}[shift={(0,1.6)}]'
    t+=r'\node[left,font=\scriptsize]at(-.2,.3){Partage};'+bande_parts(0,0,9,6,.6,txt={i:'?' for i in range(6)})+accolade((0,.7),(9,.7),'84 bonbons')+T((4.5,-.02),'6 parts égales : combien dans une part ?','below',r'\tiny','otMuted')
    t+=r'\end{scope}'
    cw=9*6/84
    t+=r'\node[left,font=\scriptsize]at(-.2,.3){Groupement};'+rf'\draw[geoTrait](0,0)rectangle(9,.6);'
    for i in range(1,4):t+=rf'\draw[geoTrait]({i*cw:.3f},0)--({i*cw:.3f},.6);'
    for i in range(3):t+=T(((i+.5)*cw,.3),'6','',r'\tiny')
    t+=T((3*cw+.6,.3),r'\dots','',r'\scriptsize')+accolade((0,.7),(9,.7),'84 bonbons')+T((4.5,-.02),'paquets de 6 : combien de paquets ?','below',r'\tiny','otMuted')
    dessin('cours-partage',t,'Le même nombre, 84, partagé en 6 parts ou groupé par paquets de 6.')
    META['cours-partage']={'type':'libre'}
    e=[(0,0,'2',0),(1,0,'3',0),(-1,1,'$-$',0),(0,1,'2',0),(1,1,'0',0),(1,2,'3',0),(2,2,'0',0),(0,3,'$-$',0),(1,3,'2',0),(2,3,'8',0),(2,4,'2',0),(3,4,'0',0),(1,5,'$-$',0),(2,5,'2',0),(3,5,'0',0),(3,6,'0',0)]
    t=potence(e,[(1,-1,1),(3,0,2),(5,1,3)],'$4$',r'$5{,}75$',4,6,notes=[(2,'5 unités, reste 3 unités'),(4,'7 dixièmes, reste 2 dixièmes'),(6,'5 centièmes, reste 0')])
    dessin('cours-potence',t,'Division posée de 23 par 4 : chaque reste est converti dans l’unité suivante.')
    META['cours-potence']={'type':'division','dividende':23,'diviseur':4,'quotient':5.75}
    e=[(0,0,'3',0),(1,0,'6',0),(2,0,'5',0),(-.6,1,'$-$',0),(.5,1,'32',1),(1.5,2,'45',1),(.4,3,'$-$',0),(1.5,3,'40',1),(2,4,'5',1)]
    t=potence(e,[(1,-1,1),(3,0,2)],'$8$',answer('$45$'),3,4)
    dessin('div-6',t,'Recopier la division et remplacer chaque point d’interrogation.')
    META['div-6']={'type':'division','dividende':365,'diviseur':8,'quotient':45,'reste':5}

# ================================================================= fractions
def fractions():
    t=r'\begin{scope}[shift={(0,1.5)}]'+bande_parts(0,0,3,4,.55,fills={0:'otNavy!30',1:'otNavy!30',2:'otNavy!30'})
    t+=rf'\draw[otMuted,line width=.8pt](0,-.12)--(0,0) (3,-.12)--(3,0);'+T((0,-.12),'0','below',r'\tiny')+T((3,-.12),'1','below',r'\tiny')
    t+=r'\node[left,font=\scriptsize]at(-.2,.27){trois quarts de 1};\end{scope}'
    t+=rf'\fill[otGreen!40](0,0)rectangle(2.25,.55);\draw[geoTrait](0,0)rectangle(9,.55);'
    for x in (2.25,4.5,6.75):t+=rf'\draw[geoTrait]({x},0)--({x},.55);'
    for u in range(4):t+=rf'\draw[otMuted,line width=.8pt]({3*u},-.12)--({3*u},0);'+T((3*u,-.12),str(u),'below',r'\tiny')
    t+=r'\node[left,font=\scriptsize]at(-.2,.27){le quart de 3};'+rf'\draw[otOrange,dashed,line width=.8pt](2.25,-.1)--(2.25,2.2);'
    dessin('cours-quart-de-3',t,'En haut, l’unité mesure 3 cm ; en bas, une bande de 3 unités partagée en 4. Les deux parties colorées ont la même longueur.')
    META['cours-quart-de-3']={'type':'quotient','longueurs':[3*.75,9/4]}
    droiteg('cours-droite-quarts',0,3,1,[(0,'0'),(1,'1'),(2,'2'),(3,'3')],points=[(r'\frac74',1.75)],minor=.25,leg=r'L’unité est partagée en quarts : sept pas d’un quart mènent à $\frac74$.')
    A=(.8,0);B=(.8+sqrt(36-3.15**2),3.15);t=''
    for k in range(8):t+=rf'\draw[otMuted!70,line width=.4pt](-.3,{k*.45:.3f})--(7.6,{k*.45:.3f});'
    t+=seg(A,B,'otNavy,line width=1.1pt')
    pts=[add(A,mul(sub(B,A),k/7)) for k in range(8)]
    t+=''.join(rf'\fill[otGreenDark]{C(p)}circle(1.5pt);' for p in pts[1:-1])+P(A,'A','below right')+P(B,'B','above left')
    dessin('cours-guide-ane',t,'Huit droites parallèles également espacées découpent le segment [AB] en sept parts égales.')
    META['cours-guide-ane']={'type':'guide','A':A,'B':B,'parts':7,'ecart':.45,'longueur':6}
    droiteg('fq-4',0,3,1,[(0,'0'),(1,'1'),(2,'2'),(3,'3')],points=[('A',.75),('B',1.75),('C',2.5)],minor=.25)
    t=bande_parts(0,0,9,4,.7)+sol(r'\fill[otGreen!40](0,0)rectangle(2.25,.7);\draw[geoTrait](0,0)rectangle(2.25,.7);')
    for u in range(4):t+=rf'\draw[otMuted,line width=.9pt]({3*u},-.15)--({3*u},0);'+T((3*u,-.15),str(u),'below',r'\scriptsize')
    t+=T((1.125,.75),answer(r'$\frac34$'),'above')
    dessin('fq-5',t,'La bande mesure 3 unités ; elle est partagée en 4 parts égales.')
    META['fq-5']={'type':'quotient','longueurs':[9/4,3*.75]}
    droiteg('fq-6',0,2,1,[(0,'0'),(1,'1'),(2,'2')],sol_=[('D',5/6),('E',11/6),('F',4/3)],minor=1/6,leg='L’unité est partagée en sixièmes ; les points demandés figurent en vert au corrigé.')
    A=(.5,0);B=(.5+sqrt(25-1.8**2),1.8);t=''
    for k in range(4):t+=rf'\draw[otMuted!70,line width=.4pt](-.3,{k*.6:.3f})--(6.2,{k*.6:.3f});'
    t+=seg(A,B,'otNavy,line width=1.1pt')+P(A,'A','below right')+P(B,'B','above left')
    pts=[add(A,mul(sub(B,A),k/3)) for k in range(4)]
    t+=sol(''.join(rf'\fill[otGreenDark]{C(p)}circle(1.7pt);' for p in pts[1:3])+''.join(marque(pts[k],pts[k+1],1,'otGreenDark') for k in range(3)))
    dessin('fq-9',t,'Réseau de quatre droites parallèles également espacées ; le segment [AB] relie la première à la dernière.')
    META['fq-9']={'type':'guide','A':A,'B':B,'parts':3,'ecart':.6,'longueur':5}
    t=r'\begin{scope}[shift={(0,1.0)}]'+bande_parts(0,0,9,3,.55,fills={0:'otNavy!30',1:'otNavy!30'})+r'\node[left]at(-.2,.27){$\frac23$};\end{scope}'
    t+=bande_parts(0,0,9,12,.55,fills={i:'otGreen!40' for i in range(8)})+r'\node[left]at(-.2,.27){$\frac8{12}$};'+rf'\draw[otOrange,dashed,line width=.8pt](6,-.15)--(6,1.75);'
    dessin('cours-bandes-egales',t,'Deux tiers de la bande et huit douzièmes de la même bande ont la même longueur.')
    META['cours-bandes-egales']={'type':'fractions','egales':[[2,3],[8,12]]}
    droiteg('fc-9',0,2,1,[(0,'0'),(1,'1'),(2,'2')],points=[('A',9/12),('B',10/12),('C',16/12)],minor=1/12,leg='L’unité est partagée en douzièmes.')

# ================================================================= pourcentages, barres, motifs
def allumettes(n,x0,s=.55):
    t='';segs=set()
    for i in range(n):
        x=x0+i*s
        segs|={((x,0),(x+s,0)),((x,s),(x+s,s)),((x,0),(x,s)),((x+s,0),(x+s,s))}
    for a,b in sorted(segs):
        t+=rf'\draw[otOrange!70!black,line width=1.6pt]{C(a)}--{C(b)};'
        head=b
        t+=rf'\fill[otRed]{C(head)}circle(1.5pt);'
    return t,len(segs)
def modeles():
    t=grille100(0,3,5,s=.34)+T((3.8,2.4),'35 cases sur 100 :','right')+T((3.8,1.6),r'$\frac{35}{100}=0{,}35=35\,\%$','right')
    dessin('cours-grille-100',t,'Une grille de cent cases : chaque case représente 1 % du tout.')
    META['cours-grille-100']={'type':'grille','valeurs':[35]}
    t=bande_parts(0,0,10,10,.6,fills={0:'otGreen!40',1:'otGreen!40',2:'otGreen!40'})
    for i in range(11):t+=T((i,.62),rf'{8*i}~€','above',r'\tiny','otMuted')
    for i in (0,1,2,3,5,10):t+=T((i,-.02),rf'{10*i}\,\%','below',r'\tiny')
    t+=accolade((3,-.45),(0,-.45),r'30\,\% de 80 € : 24 €','below','otGreenDark')
    dessin('cours-bande-pct',t,'La bande représente 80 € ; chaque dixième de la bande représente 10 %, soit 8 €.')
    META['cours-bande-pct']={'type':'pourcentage','tout':80,'pct':30,'partie':24}
    dessin('pct-1',grille100(0,4,2,s=.34),'La grille compte cent cases identiques.')
    META['pct-1']={'type':'grille','valeurs':[42]}
    t=rf'\fill[otNavy!25](0,0)rectangle(4.5,.8);\fill[otGreen!30](4.5,0)rectangle(7.5,.8);\fill[otOrange!30](7.5,0)rectangle(10,.8);\draw[geoTrait](0,0)rectangle(10,.8);\draw[geoTrait](4.5,0)--(4.5,.8) (7.5,0)--(7.5,.8);'
    t+=T((2.25,.4),r'bus : 45\,\%')+T((6,.4),r'vélo : 30\,\%')+T((8.75,.4),r'à pied : '+answer(r'25\,\%'))
    dessin('pct-8',t,'La bande entière représente les 240 élèves, soit 100 %.')
    META['pct-8']={'type':'pourcentage','parts':[45,30,25]}
    u=1.5
    t=r'\node[left,font=\scriptsize]at(-.15,1.0){Mia};'+barre(0,.75,u,'12')+r'\node[left,font=\scriptsize]at(-.15,.25){Léo};'+''.join(barre(i*u,0,u,'12') for i in range(3))
    t+=accolade((4.75,1.25),(4.75,0),'48 billes','right')
    dessin('cours-barres',t,'Mia : une barre ; Léo : trois barres identiques. Les quatre barres valent 48.')
    META['cours-barres']={'type':'barres-modele','unites':4,'total':48}
    k=.1
    t=r'\node[left,font=\scriptsize]at(-.15,1.0){Lina};'+barre(0,.75,30*k,answer('30 €'))+r'\node[left,font=\scriptsize]at(-.15,.25){Marc};'+barre(0,0,30*k,answer('30 €'))+barre(30*k,0,15*k,'15 €',fill='otOrange!25')
    t+=accolade((4.75,1.25),(4.75,0),'75 €','right')
    dessin('alg-1',t,'Les deux barres de même longueur représentent la même somme.')
    META['alg-1']={'type':'barres-modele','unites':2,'total':75,'ecart':15}
    t='';x=0;cnt=[]
    for n in (1,2,3):
        q,c=allumettes(n,x);t+=q+T((x+n*.275,-.1),f'étape {n}','below',r'\tiny');cnt.append(c);x+=n*.55+1.0
    dessin('alg-3',t,'Les carrés d’allumettes sont alignés et partagent leurs côtés.')
    META['alg-3']={'type':'motifs','etapes':cnt}
    t='';x=0;cnt2=[]
    for n in (1,2,3):
        q,c=allumettes(n,x);t+=q+T((x+n*.275,-.1),f'étape {n} : {c} allumettes','below',r'\tiny');cnt2.append(c);x+=n*.55+1.8
    dessin('cours-motif',t,'À chaque étape, on ajoute un carré : trois allumettes de plus.')
    META['cours-motif']={'type':'motifs','etapes':cnt2}
    k=.2
    t=''.join(barre(i*7*k,.75,7*k,answer('7')) for i in range(3))+barre(21*k,.75,5*k,'5',fill='otOrange!25')+barre(0,0,26*k,'26',fill='otNavy!8')
    dessin('alg-5',t,'Les deux lignes ont la même longueur.')
    META['alg-5']={'type':'barres-modele','unites':3,'total':26,'morceau':5}
    s=.32;t='';x=0;cnt=[]
    for n in (1,2,3):
        cells=[(0,0)]+[(i,0) for i in range(1,n+1)]+[(0,j) for j in range(1,n+1)]
        for (c,r) in cells:t+=rf'\filldraw[draw=otNavy,fill=otNavy!20,line width=.6pt]({x+c*s:.3f},{r*s:.3f})rectangle({x+(c+1)*s:.3f},{(r+1)*s:.3f});'
        t+=T((x+(n+1)*s/2,-.1),f'étape {n}','below',r'\tiny');cnt.append(len(cells));x+=(n+1)*s+1.0
    dessin('alg-8',t,'Le motif en L grandit d’un carreau sur chaque branche à chaque étape.')
    META['alg-8']={'type':'motifs','etapes':cnt}
    s=.3;t='';x=0;cnt=[]
    for n in (1,2,3,4):
        c=0
        for col in range(n):
            for r in range(col+1):t+=rf'\filldraw[draw=otNavy,fill=otNavy!20,line width=.6pt]({x+col*s:.3f},{r*s:.3f})rectangle({x+(col+1)*s:.3f},{(r+1)*s:.3f});';c+=1
        t+=T((x+n*s/2,-.1),f'étape {n}','below',r'\tiny');cnt.append(c);x+=n*s+.9
    dessin('alg-12',t,'À l’étape $n$, l’escalier compte $n$ colonnes, de hauteurs 1, 2, 3…')
    META['alg-12']={'type':'motifs','etapes':cnt}
    t='';x0=0.0;cnt=[]
    for n,e in enumerate([1,2,3],1):
        cells=sorted(set([(k,0) for k in range(-e,e+1)]+[(0,k) for k in range(-e,e+1)]))
        for (cx,cy) in cells:t+=rf'\filldraw[draw=otNavy,fill=otNavy!20,line width=.6pt]({x0+cx*.36:.3f},{cy*.36:.3f})rectangle({x0+cx*.36+.36:.3f},{cy*.36+.36:.3f});'
        t+=T((x0+.18,-e*.36-.1),f'étape {n}','below',r'\tiny');cnt.append(len(cells));x0+=e*.36*2+1.4
    dessin('alg-13',t,'La croix gagne un carreau au bout de chaque branche à chaque étape.')
    META['alg-13']={'type':'motifs','etapes':cnt}

# ================================================================= proportionnalité
def proportion():
    cw=1.6;hw=2.4;h=.6
    t=rf'\draw[geoTrait](0,0)rectangle({hw+3*cw},{2*h});\draw[geoTrait](0,{h})--({hw+3*cw},{h});'
    for i in range(4):t+=rf'\draw[geoTrait]({hw+i*cw},0)--({hw+i*cw},{2*h});'
    t+=rf'\fill[otNavy!8](0,0)rectangle({hw},{2*h});\draw[geoTrait](0,0)rectangle({hw+3*cw},{2*h});'
    t+=T((hw/2,1.5*h),'Masse (kg)')+T((hw/2,.5*h),'Prix (€)')
    for i,(a,b) in enumerate([('1','2,50'),('2','5'),('6','15')]):t+=T((hw+(i+.5)*cw,1.5*h),a)+T((hw+(i+.5)*cw,.5*h),b)
    for y0,sgn,where in [(2*h+.05,1,'above'),(-.05,-1,'below')]:
        for i,lab in [(0,r'$\times2$'),(1,r'$\times3$')]:
            x1=hw+(i+.5)*cw;x2=hw+(i+1.5)*cw
            t+=rf'\draw[otGreenDark,->,line width=.7pt]({x1+.15},{y0})to[bend {"left" if sgn>0 else "right"}=35]({x2-.15},{y0});'+T(((x1+x2)/2,y0+sgn*.3),lab,where,r'\scriptsize','otGreenDark')
    dessin('cours-tableau-fleches',t,'Le prix est proportionnel à la masse : on multiplie les deux lignes par le même nombre.')
    META['cours-tableau-fleches']={'type':'proportion','masses':[1,2,6],'prix':[2.5,5,15]}
    t=''
    for i in range(3):t+=rf'\filldraw[draw=otNavy,fill={"otNavy!30" if i%2==0 else "white"},line width=.6pt]({i},0)rectangle({i+1},.22);'
    for i,lab in enumerate(['0','50 m','100 m','150 m']):t+=T((i,-.02),lab,'below',r'\tiny')
    t+=T((1.5,.3),'1 cm représente 50 m','above',r'\tiny','otMuted')
    dessin('cours-echelle',t,'Une échelle graphique : chaque centimètre du plan représente 50 m.')
    META['cours-echelle']={'type':'echelle','cm':50}
    t=rf'\filldraw[draw=otNavy,fill=otNavy!30,line width=.6pt](0,1.2)rectangle(1,1.42);'+T((0,1.18),'0','below',r'\tiny')+T((1,1.18),'200 m','below',r'\tiny')
    E=(0,0);G=(4,0);t+=seg(E,G,'otNavy,line width=1pt')+P(E,'','above')+P(G,'','above')+T(E,'école','left',r'\scriptsize')+T(G,'gymnase','right',r'\scriptsize')
    t+=rf'\draw[otMuted,<->](0,-.35)--(4,-.35);'+T((2,-.35),'4 cm','below',r'\scriptsize')+T((2,.05),answer('800 m'),'above')
    dessin('pro-5',t,'Plan du quartier, avec son échelle graphique.')
    META['pro-5']={'type':'echelle','cm':200,'longueur':4}
    t=rf'\filldraw[draw=otNavy,fill=otGreen!12,line width=.8pt](0,0)rectangle(6,4.5);'+T((3,2.25),'jardin')+T((3,-.05),'6 cm','below')+T((-.05,2.25),'4,5 cm','left')
    t+=T((3,4.55),answer('12 m'),'above')+T((6.05,2.25),answer('9 m'),'right')+T((6,4.9),'1 cm pour 2 m','left',r'\tiny','otMuted')
    dessin('pro-9',t,'Le plan du jardin, à l’échelle indiquée.')
    META['pro-9']={'type':'echelle','cm':2,'dims':[6,4.5]}
    S=(0,0);P1=polar(S,20,2);P2=polar(P1,-15,3.4);P3=polar(P2,50,1.6)
    t=poly([S,P1,P2,P3],'otNavy,line width=1.2pt',close=False)+P(S)+P(P1)+P(P2)+P(P3)+T(S,'départ','below',r'\scriptsize')+T(P3,'refuge','above',r'\scriptsize')
    for a,b,lab in [(S,P1,'2 cm'),(P1,P2,'3,4 cm'),(P2,P3,'1,6 cm')]:t+=T(mid(a,b),lab,'above left' if b!=P2 else 'below',r'\scriptsize')
    t+=rf'\filldraw[draw=otNavy,fill=otNavy!30,line width=.6pt](0,-1.2)rectangle(1,-.98);'+T((0,-1.22),'0','below',r'\tiny')+T((1,-1.22),'250 m','below',r'\tiny')
    dessin('pro-11',t,'Le chemin de randonnée sur la carte, avec l’échelle.')
    META['pro-11']={'type':'chemin','longueurs':[dist(S,P1),dist(P1,P2),dist(P2,P3)]}

# ================================================================= longueurs et aires
def grandeurs():
    t=cercle((1,1),1)+seg((0,1),(2,1),'otGreenDark,line width=1pt')+T((1,1),'$d$','above',r'\scriptsize')
    t+=seg((3,.4),(3+2*pi,.4),'otNavy,line width=1.2pt')
    for i in range(4):t+=rf'\draw[otGreenDark,line width=.8pt]({3+2*i},.25)--({3+2*i},.55);'
    for i in range(3):t+=T((4+2*i,.25),'$d$','below',r'\scriptsize','otGreenDark')
    t+=rf'\draw[otOrange,line width=2pt](9,.4)--({3+2*pi:.3f},.4);'+T((3+pi,.5),'le contour déroulé : un peu plus de 3 diamètres','above',r'\tiny')
    dessin('cours-cercle-diametre',t,'Déroulé, le contour d’un disque mesure environ 3,14 fois son diamètre.')
    META['cours-cercle-diametre']={'type':'pi','rapport':pi}
    A=(0,1.0);B=polar(A,25,2.3);Cc=polar(B,-35,1.8);D=polar(Cc,15,2.6)
    t=poly([A,B,Cc,D],'geoTrait',close=False)+P(A,'A','left')+P(B,'B','above')+P(Cc,'C','below')+P(D,'D','right')
    O=(0,-.9);t+=seg(O,(7.6,-.9),'otMuted,line width=.8pt')+P(O,'O','left')
    xs=[0,2.3,4.1,6.7]
    s=''.join(rf'\draw[otGreenDark,line width=1.3pt]({xs[k]},-.9)--({xs[k+1]},-.9);\draw[otGreenDark]({xs[k+1]},-1.05)--({xs[k+1]},-.75);' for k in range(3))+T((6.7,-1.0),'6,7 cm','below',r'\scriptsize','otGreenDark')
    t+=sol(s)
    dessin('lon-5',t,'La ligne brisée ABCD et la demi-droite d’origine O.')
    META['lon-5']={'type':'longueurs','cotes':[dist(A,B),dist(B,Cc),dist(Cc,D)]}
    k=.7
    t=rf'\begin{{scope}}[scale={k}]\fill[otNavy!8](0,0)--(6,0)arc(-90:90:2)--(0,4)--cycle;\draw[geoTrait](6,0)--(0,0)--(0,4)--(6,4);\draw[geoTrait](6,0)arc(-90:90:2);\draw[otMuted,dashed](6,0)--(6,4);'
    t+=T((3,0),'6 cm','below')+T((0,2),'4 cm','left')+r'\end{scope}'
    dessin('lon-6',t,'Un rectangle prolongé par un demi-disque ; le segment intérieur est en tirets.')
    META['lon-6']={'type':'perimetre','valeur':6+4+6+pi*4/2}
    t=rf'\fill[otGreen!15](0,0)--(5,0)arc(-90:90:1.5)--(0,3)arc(90:270:1.5);\draw[otOrange!70!black,line width=1.6pt](0,0)--(5,0)arc(-90:90:1.5)--(0,3)arc(90:270:1.5);'
    t+=rf'\draw[otMuted,dashed](0,0)--(0,3);'+T((2.5,0),'100 m','below')+T((0,1.5),'60 m','right')
    dessin('lon-7',t,'La piste : deux lignes droites et deux demi-cercles.')
    META['lon-7']={'type':'perimetre','valeur':200+pi*60}
    k=.5;pts=[(0,0),(8,0),(8,3),(3,3),(3,7),(0,7)]
    t=rf'\begin{{scope}}[scale={k}]'+poly(pts,fill='otNavy!8')
    for v,a,b in [((0,0),(1,0),(0,1)),((8,0),(7,0),(8,1)),((8,3),(8,2),(7,3)),((3,7),(2,7),(3,6)),((0,7),(0,6),(1,7))]:t+=droit(v,a,b,.45)
    t+=T((4,0),'8 cm','below')+T((8,1.5),'3 cm','right')+T((5.5,3),answer('5 cm'),'above')+T((3,5),answer('4 cm'),'right')+T((1.5,7),'3 cm','above')+T((0,3.5),'7 cm','left')+r'\end{scope}'
    dessin('lon-10',t,'Figure de principe : tous ses angles sont droits.')
    META['lon-10']={'type':'polygone','points':pts}
    t=rf'\fill[otNavy!6](0,0)circle(3);\draw[otMuted,line width=6pt,opacity=.25](0,0)circle(3);\filldraw[draw=otGreenDark,fill=otGreen!25](0,0)circle(1.1);'
    t+=seg((0,0),(3,0),'otNavy')+T((1.9,0),'15 m','above',r'\scriptsize')+P((0,-3),'','below')+T((0,-3),'entrée','below',r'\tiny')
    t+=sol(r'\draw[otGreenDark,line width=1.4pt,-{Stealth[length=2.6mm]}]([shift={(0,0)}]270:2.6)arc(270:540:2.6);')+T((2.2,2.6),'1 cm pour 5 m','right',r'\tiny','otMuted')
    dessin('lon-14',t,'Le rond-point vu de dessus ; la voiture entre en bas et tourne dans le sens des flèches du code de la route.')
    META['lon-14']={'type':'cercle','rayon':15,'fraction':.75}
    # Aires.
    k=.5
    t=rf'\begin{{scope}}[scale={k}]'+grille(13,3)
    t+=poly([(0,0),(4,0),(5,2),(1,2)],fill='otNavy!20')+poly([(0,0),(1,0),(1,2)],fill='otOrange!45')
    t+=rf'\draw[otOrange!80!black,->,line width=.8pt](.6,2.4)to[bend left=30](4.4,2.4);'
    t+=poly([(8,0),(11,0),(12,2),(8,2)],'geoTrait',fill='otNavy!20')+poly([(11,0),(12,0),(12,2)],fill='otOrange!45')+poly([(8,0),(12,0),(12,2),(8,2)])
    t+=r'\end{scope}'
    dessin('cours-decoupage',t,'Le triangle découpé à gauche se recolle à droite : même aire, autre forme.')
    META['cours-decoupage']={'type':'aires','valeurs':[8,8]}
    t=r'\fill[otNavy!18](0,0)rectangle(10,10);'+''.join(rf'\draw[white,line width=.6pt]({k},0)--({k},10) (0,{k})--(10,{k});' for k in range(1,10))+r'\draw[geoTrait](0,0)rectangle(10,10);'
    t+=r'\fill[otGreen!45](0,9)rectangle(1,10);\draw[otGreenDark,line width=.8pt](0,9)rectangle(1,10);'
    t+=r'\draw[otMuted,<->](0,-.7)--(10,-.7);\node[below,font=\tiny]at(5,-.8){1 dm = 10 cm};'
    t+=r'\draw[otGreenDark,->](1.2,9.5)--(2.6,9.5);\node[right,font=\tiny,otGreenDark]at(2.6,9.5){1 cm$^2$};'
    dessin('cours-dm2',rf'\begin{{scope}}[scale=.34]{t}\end{{scope}}','Un décimètre carré : dix rangées de dix centimètres carrés, soit 100 cm$^2$.')
    META['cours-dm2']={'type':'cellules','aires':[100]}
    k=.45
    A=[(i,j) for i in range(4) for j in range(2)];B=[(5,0),(6,0),(7,0),(8,0),(5,1),(5,2),(5,3)];Cc=[(10,0),(11,0),(12,0),(10,1),(11,1),(12,1)]
    t=grille(15,4)
    for (c,r) in A+B+Cc:t+=rf'\fill[otNavy!25]({c},{r})rectangle({c+1},{r+1});'
    t+=r'\fill[otNavy!25](13,0)--(14,0)--(13,1)--cycle;\fill[otNavy!25](10,2)--(11,2)--(10,3)--cycle;'+grille(15,4)
    t+=poly([(0,0),(4,0),(4,2),(0,2)])+poly([(5,0),(9,0),(9,1),(6,1),(6,4),(5,4)])+poly([(10,0),(14,0),(13,1),(13,2),(11,2),(10,3)])
    t+=T((2,-.1),'A','below')+T((7,-.1),'B','below')+T((12,-.1),'C','below')
    dessin('air-1',rf'\begin{{scope}}[scale={k}]{t}\end{{scope}}','Trois surfaces tracées sur un même quadrillage.')
    META['air-1']={'type':'aires','valeurs':[len(A),len(B),len(Cc)+1]}
    t=grille(6,4)+poly([(0,0),(5,0),(5,2),(3,2),(3,3),(0,3)],fill='otNavy!25')
    dessin('air-2',rf'\begin{{scope}}[scale=.55]{t}\end{{scope}}','Chaque carreau du quadrillage a des côtés de 1 cm.')
    META['air-2']={'type':'aires','valeurs':[13]}
    t=grille(13,4)+poly([(0,0),(6,0),(6,2),(0,2)],fill='otNavy!25')+poly([(8,0),(12,0),(12,3),(8,3)],fill='otGreen!25')
    t+=T((3,0),'6 cm','below')+T((0,1),'2 cm','left')+T((10,0),'4 cm','below')+T((12,1.5),'3 cm','right')
    dessin('air-7',rf'\begin{{scope}}[scale=.45]{t}\end{{scope}}','Deux rectangles ; un carreau du quadrillage représente 1 cm$^2$.')
    META['air-7']={'type':'aires','valeurs':[12,12],'perimetres':[16,14]}
    t=grille(7,4)+poly([(0,0),(4,0),(5,3),(1,3)],fill='otNavy!20')+poly([(0,0),(1,3),(1,0)],fill='otMuted!45')
    t+=sol(poly([(4,0),(5,3),(5,0)],'geoReponse',fill='otGreen!40')+poly([(1,0),(5,0),(5,3),(1,3)],'geoReponse'))
    dessin('air-8',rf'\begin{{scope}}[scale=.55]{t}\end{{scope}}','Un carreau du quadrillage représente 1 cm$^2$ ; le triangle grisé est à déplacer.')
    META['air-8']={'type':'aires','valeurs':[12]}
    pts=[(0,0),(9,0),(9,3),(4,3),(4,7),(0,7)]
    t=poly(pts,fill='otNavy!8')+T((4.5,0),'9 m','below')+T((9,1.5),'3 m','right')+T((6.5,3),'5 m','above')+T((4,5),'4 m','right')+T((2,7),'4 m','above')+T((0,3.5),'7 m','left')
    t+=sol(r'\draw[geoAide](0,3)--(4,3);')
    dessin('air-10',rf'\begin{{scope}}[scale=.45]{t}\end{{scope}}','Plan de la pièce ; tous ses angles sont droits.')
    META['air-10']={'type':'polygone','points':pts}
    t=rf'\filldraw[draw=otNavy,fill=otGreen!12,line width=.8pt](0,0)rectangle(4,4);\filldraw[draw=otNavy,fill=otOrange!25,line width=.8pt](0,0)rectangle(4,1.6);'
    t+=T((2,.8),'potager')+T((2,2.8),'pelouse')+T((2,0),'20 m','below')+T((4,2),'20 m','right')+T((0,.8),'8 m','left')
    dessin('air-13',t,'Le jardin vu de dessus.')
    META['air-13']={'type':'aires','valeurs':[160,240]}
    # Durées.
    X=lambda h,m:(h+m/60-9.5)*4.5
    t=rf'\draw[otMuted,->](0,0)--(9.4,0);'
    for k in range(9):t+=rf'\draw[otMuted]({k*1.125:.3f},-.07)--({k*1.125:.3f},.07);'
    for h in (10,11):t+=rf'\draw[otMuted,line width=.9pt]({X(h,0):.3f},-.13)--({X(h,0):.3f},.13);'+T((X(h,0),-.15),f'{h} h','below',r'\scriptsize')
    t+=P((X(9,47),0),'','below')+T((X(9,47),-.15),'9 h 47','below',r'\scriptsize','otNavy')+P((X(11,15),0),'','below')+T((X(11,15),-.15),'11 h 15','below',r'\scriptsize','otNavy')
    for a,b,lab in [(X(9,47),X(10,0),'13 min'),(X(10,0),X(11,0),'1 h'),(X(11,0),X(11,15),'15 min')]:
        t+=rf'\draw[otGreenDark,->,line width=.8pt]({a+.05:.3f},.2)to[bend left=40]({b-.05:.3f},.2);'+T(((a+b)/2,.55 if b-a>2 else .45),lab,'above',r'\scriptsize','otGreenDark')
    dessin('cours-frise',t,'On avance jusqu’aux heures rondes : 13 min, puis 1 h, puis 15 min.')
    META['cours-frise']={'type':'duree','minutes':[13,60,15]}
    t=r'\fill[otNavy!25](0,0)--(90:1.6)arc(90:0:1.6)--cycle;\fill[otGreen!30](0,0)--(0:1.6)arc(0:-90:1.6)--cycle;\fill[otOrange!30](0,0)--(-90:1.6)arc(-90:-180:1.6)--cycle;\fill[otNavy!10](0,0)--(180:1.6)arc(180:90:1.6)--cycle;'
    t+=r'\draw[geoTrait](0,0)circle(1.6);'
    for k in range(12):t+=rf'\draw[otMuted]({90-k*30}:1.45)--({90-k*30}:1.6);'
    t+=T((1.7,0),'15 min $=0{,}25$ h','right')+T((0,-1.7),'30 min $=0{,}5$ h','below')+T((-1.7,0),'45 min $=0{,}75$ h','left')+T((0,1.7),'60 min $=1$ h','above')
    dessin('cours-cadran',t,'Chaque quart du cadran représente un quart d’heure, soit 15 minutes.')
    META['cours-cadran']={'type':'duree','quarts':[15,30,45,60]}
    t='';hs=[]
    for i,(h,m) in enumerate([(3,20),(7,45),(11,5)]):
        q,ah,am=horloge(i*3.6,h,m);t+=q+T((i*3.6,-1.4),'abc'[i],'below',r'\scriptsize');hs.append((h,m,ah,am))
    dessin('dur-1',t,'Trois horloges à aiguilles ; la petite aiguille indique l’heure.')
    META['dur-1']={'type':'horloges','lectures':hs}
    X=lambda h,m:(h+m/60-8)*2.4
    t=rf'\draw[otMuted,->](0,0)--(9.9,0);'
    for k in range(17):t+=rf'\draw[otMuted]({k*.6:.2f},-.06)--({k*.6:.2f},.06);'
    for h in range(8,13):t+=rf'\draw[otMuted,line width=.9pt]({X(h,0):.2f},-.12)--({X(h,0):.2f},.12);'+T((X(h,0),-.14),f'{h} h','below',r'\scriptsize')
    t+=rf'\fill[otOrange!40]({X(10,5):.3f},-.1)rectangle({X(10,20):.3f},.1);'
    for (h,m),lab,y in [((8,25),'arrivée : 8 h 25',.75),((10,5),'récréation : 10 h 05 à 10 h 20',1.25),((11,55),'sortie : 11 h 55',.75)]:
        t+=rf'\draw[otNavy,line width=.5pt]({X(h,m):.3f},.12)--({X(h,m):.3f},{y-.05});'+T((X(h,m),y),lab,'above',r'\tiny')+P((X(h,m),0))
    dessin('dur-9',t,'La matinée de Maya, de 8 h à 12 h ; chaque petite graduation vaut 15 minutes.')
    META['dur-9']={'type':'frise','instants':[(8,25),(10,5),(10,20),(11,55)]}

def write_all(root):
    import figures_suite
    for f in [nombres,division,fractions,modeles,proportion,grandeurs]:f()
    figures_suite.tout()
    out=root/'figures';out.mkdir(exist_ok=True)
    import re
    for name,data in FIGURES.items():
        assert not any(ord(c)<32 for c in data['tex']+data['legende']),name
        legende=re.sub(r'(?<!\\)%',r'\\%',data['legende'])
        content=data['tex']+r'\par\vspace{1.5mm}{\otRegular\fontsize{8}{10}\selectfont\color{otMuted}'+legende+r'\par}'+'\n'
        (out/(name+'.tex')).write_text(content,encoding='utf8')

if __name__=='__main__':
    import generer_figures as g
    g.write_all(Path(__file__).resolve().parent)
    print(len(FIGURES),'figures écrites')
