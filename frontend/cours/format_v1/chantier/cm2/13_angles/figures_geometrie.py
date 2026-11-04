from pathlib import Path
import json,math,importlib.util
BASE=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('redaction',Path(__file__).with_name('rediger_geometrie.py'));mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
F={d:{} for d in mod.DIRS}
def fig(d,n,s): F[d][n]=r'\begin{tikzpicture}[line cap=round,font=\large]'+s+r'\end{tikzpicture}'
def node(x,y,t,anchor='center',color='otInk'):return rf'\node[anchor={anchor},text={color},inner sep=4pt] at ({x},{y}) {{{t}}};'
def path(pts,style='geoTrait',close=True):return '\\draw['+style+'] '+'--'.join(f'({x},{y})' for x,y in pts)+('--cycle;' if close else ';')
d=mod.DIRS[0]
fig(d,'angle',r'\draw[geoTrait] (0,2)--(0,0)--(3,0);\draw[otGreenDark] (.5,0) arc(0:90:.5);'+node(0,2,'$A$','south')+node(0,0,'$B$','north east')+node(3,0,'$C$','north')+node(2,1.3,r'$\widehat{ABC}$'))
s=''
for i,(deg,label) in enumerate([(40,'A'),(90,'B'),(130,'C')]):
    x=i*2.7;dx=1.5*math.cos(math.radians(deg));dy=1.5*math.sin(math.radians(deg));s+=path([(x+1.5,0),(x,0),(x+dx,dy)],close=False)+node(x+.6,-.45,label)
    if deg==90:s+=rf'\draw[geoTrait] ({x+.25},0)--({x+.25},.25)--({x},.25);'
fig(d,'types',s)
fig(d,'somme',r'\draw[geoTrait] (2.5,0)--(0,0)--(0,2.5);\draw[geoReponse] (0,0)--(-1.77,1.77);\draw[otNavy] (.6,0) arc(0:90:.6);\draw[otGreenDark] (0,.9) arc(90:135:.9);'+node(1,1,r'$90^\circ$')+node(-.65,1.65,r'$45^\circ$','center','otGreenDark'))
fig(d,'pliage',r'\draw[geoTrait] (2.6,0)--(0,0)--(0,2.6);\draw[geoReponse,dashed] (0,0)--(2,2);\draw[otGreenDark] (.65,0) arc(0:45:.65);\draw[otGreenDark] (.95,.95) arc(45:90:1.3435);'+node(1.45,.5,r'$45^\circ$')+node(.5,1.7,r'$45^\circ$')+node(2,2,'pli','south','otGreenDark'))
d=mod.DIRS[1];s=''
for i,n in enumerate([3,4,5,6]):
    cx=(i%2)*3.6;cy=-(i//2)*3
    pts=[(cx+1.1*math.cos(math.pi/2+2*math.pi*j/n),cy+1.1*math.sin(math.pi/2+2*math.pi*j/n)) for j in range(n)]
    s+=path(pts)+node(cx,cy-1.55,str(n)+' côtés')
fig(d,'polygones',s)
s=path([(0,0),(2,0),(0,1.5)])+r'\draw[geoTrait] (.22,0)--(.22,.22)--(0,.22);'+node(1,-.5,'rectangle')
s+=path([(3,0),(5,0),(4,1.8)])+node(4,-.5,'isocèle')+r'\draw[geoTrait] (3.43,.95)--(3.59,.87) (4.41,.87)--(4.57,.95);'
s+=path([(0,-3),(2,-3),(1,-1.26795)])+node(1,-3.5,'équilatéral')+r'\draw[geoTrait] (1,-3.1)--(1,-2.9) (.42,-2.1)--(.59,-2.2) (1.41,-2.2)--(1.58,-2.1);'
fig(d,'triangles',s)
s=''
for x,y,pts,label in [(0,0,[(0,0),(2.4,0),(2.4,1.4),(0,1.4)],'rectangle'),(4,0,[(0,0),(1.4,.8),(0,1.6),(-1.4,.8)],'losange'),(0,-3,[(0,0),(1.7,0),(1.7,1.7),(0,1.7)],'carré')]:
    s+=path([(a+x,b+y) for a,b in pts])+node(x+.7,y-.55,label)
    if label!='losange':s+=rf'\draw[geoTrait] ({x+.22},{y})--({x+.22},{y+.22})--({x},{y+.22});'
fig(d,'quadrilateres',s)
fig(d,'trapeze',path([(0,0),(4,0),(2.7,2),(0,2)])+r'\draw[geoTrait] (.25,0)--(.25,.25)--(0,.25) (.25,2)--(.25,1.75)--(0,1.75);'+node(0,0,'$A$','north east')+node(4,0,'$B$','north west')+node(2.7,2,'$C$','south west')+node(0,2,'$D$','south east')+node(2,-.6,'bases parallèles'))
d=mod.DIRS[2]
fig(d,'droites',r'\draw[geoTrait] (-.2,0)--(4.5,0) (-.2,1.6)--(4.5,1.6) (1,-.5)--(1,2.5);\draw[geoTrait] (1.25,0)--(1.25,.25)--(1,.25);'+node(4.5,0,'$(d)$','west')+node(4.5,1.6,'$(e)$','west')+node(1,2.5,'$(f)$','south')+node(3,2.5,r'$(d)\parallel(e)$')+node(3,-.9,r'$(f)\perp(d)$'))
fig(d,'cercle',r'\fill[otSky] (0,0) circle(1.7);\draw[geoTrait] (0,0) circle(1.7);\draw[geoTrait] (-1.7,0)--(1.7,0);\fill[otNavy] (0,0) circle(1.8pt);\draw[geoReponse] (0,0)--(0,1.7);'+node(.05,-.05,'$O$','north west')+node(-1.7,0,'$A$','east')+node(1.7,0,'$B$','west')+node(-.2,.8,'rayon','east','otGreenDark')+node(0,-2.1,'[AB] : diamètre')+node(0,2.2,'disque : intérieur et bord'))
fig(d,'rectangle',path([(0,0),(4,0),(4,2.4),(0,2.4)])+r'\draw[geoTrait] (.25,0)--(.25,.25)--(0,.25) (3.75,0)--(3.75,.25)--(4,.25) (3.75,2.4)--(3.75,2.15)--(4,2.15) (.25,2.4)--(.25,2.15)--(0,2.15);'+node(0,0,'$A$','north east')+node(4,0,'$B$','north west')+node(4,2.4,'$C$','south west')+node(0,2.4,'$D$','south east')+node(2,-.55,'5 cm')+node(4.6,1.2,'3 cm'))
fig(d,'compas',r'\draw[geoTrait] (0,0)--(3,0);\draw[geoAide] (0,0) ++(35:3) arc(35:85:3);\draw[geoAide] (3,0) ++(95:3) arc(95:145:3);\draw[geoReponse] (0,0)--(1.5,2.598076211)--(3,0);'+node(0,0,'$A$','north east')+node(3,0,'$B$','north west')+node(1.5,2.598076211,'$C$','south')+node(1.5,-.95,'même ouverture de compas'))
d=mod.DIRS[3]
def sym(n,pts,axis,fn):
    s=r'\draw[step=.5,otRule,thin] (-2,-2) grid (2,2);'+path(axis,'otOrange,thick',False)+path(pts,'geoTrait',False)+path([fn(*p) for p in pts],'geoReponse',False)
    s+=node(0,-2.6,'bleu : figure ; vert : symétrique')
    fig(d,n,s)
sym('vertical',[(-1.5,-1),(-.5,-1),(-.5,1)],[(0,-2.2),(0,2.2)],lambda x,y:(-x,y))
sym('horizontal',[(-1.5,1.5),(-1.5,.5),(1,.5)],[(-2.2,0),(2.2,0)],lambda x,y:(x,-y))
sym('diagonal',[(1.5,.5),(1.5,-.5),(.5,-.5)],[(-2.2,-2.2),(2.2,2.2)],lambda x,y:(y,x))
fig(d,'vertical_point',r'\draw[step=.5,otRule,thin] (-1.5,-1) grid (1.5,1);\draw[otOrange,thick] (0,-1.2)--(0,1.2);\fill[otNavy] (-1,0) circle(2pt);\fill[otGreenDark] (1,0) circle(2pt);\draw[geoAide] (-1,0)--(1,0);'+node(-1,1.4,'$A$')+node(1,1.4,"$A'$",color='otGreenDark')+node(0,-1.7,'2 carreaux de chaque côté'))
fig(d,'horizontal_point',r'\draw[step=.5,otRule,thin] (-1,-1) grid (1,1);\draw[otOrange,thick] (-1.2,0)--(1.2,0);\fill[otNavy] (0,.5) circle(2pt);\fill[otGreenDark] (0,-.5) circle(2pt);\draw[geoAide] (0,-.5)--(0,.5);\draw[otNavy,thin] (0,.5)--(1.35,.5);\draw[otGreenDark,thin] (0,-.5)--(1.35,-.5);'+node(1.4,.5,'$B$','west')+node(1.4,-.5,"$B'$",'west','otGreenDark')+node(0,-1.6,'1 carreau de chaque côté'))
fig(d,'diagonal_point',r'\draw[step=.5,otRule,thin] (0,0) grid (2,2);\draw[otOrange,thick] (-.2,-.2)--(2.2,2.2);\fill[otNavy] (1.5,.5) circle(2pt);\fill[otGreenDark] (.5,1.5) circle(2pt);\draw[otNavy,thin] (1.5,.5)--(2.35,.5);\draw[otGreenDark,thin] (.5,1.5)--(-.35,1.5);'+node(2.4,.5,'$A$','west')+node(-.4,1.5,"$A'$",'east','otGreenDark')+node(0,0,'$O$','north east')+node(1,-.7,'3 et 1 deviennent 1 et 3'))
fig(d,'axes',path([(0,0),(2,0),(2,2),(0,2)])+r'\draw[otOrange,dashed] (-.2,-.2)--(2.2,2.2) (-.2,2.2)--(2.2,-.2) (1,-.3)--(1,2.3) (-.3,1)--(2.3,1);'+node(1,-.85,'4 axes du carré'))
d=mod.DIRS[4]
def pave():
    # Avant ABCD, arrière EFGH ; E (arrière-bas-gauche) est le seul sommet caché.
    s=path([(0,0),(3,0),(3,2),(0,2)])+path([(0,2),(.9,2.7),(3.9,2.7),(3,2)],close=False)+path([(3,0),(3.9,.7),(3.9,2.7)],close=False)
    s+=path([(0,0),(.9,.7),(3.9,.7)],'geoTrait,dashed',False)+path([(.9,.7),(.9,2.7)],'geoTrait,dashed',False)
    return s+node(1.8,-.65,'pointillés : arêtes cachées')
fig(d,'pave',pave())
fig(d,'cube',pave().replace('(3,','(2,').replace('(3.9,','(2.9,'))
# Prisme triangulaire : base avant, base arrière décalée ; arêtes invisibles pointillées.
s=path([(0,0),(2,0),(1,1.7)])+path([(2,0),(3,.8),(2,2.5),(1,1.7)],close=False)+path([(2,2.5),(1,.8)],'geoTrait,dashed',False)+path([(0,0),(1,.8),(3,.8)],'geoTrait,dashed',False)+node(1.5,-.6,'prisme droit')
s+=path([(4.5,0),(6.8,0),(7.6,.7),(5.9,2.5),(4.5,0)],close=False)+path([(6.8,0),(5.9,2.5)],close=False)+path([(4.5,0),(5.3,.7),(7.6,.7)],'geoTrait,dashed',False)+path([(5.3,.7),(5.9,2.5)],'geoTrait,dashed',False)+node(6,-.6,'pyramide')
fig(d,'familles',s)
s=''
for x,y,n in [(0,0,1),(1,0,2),(2,0,3),(3,0,4),(1,1,5),(1,-1,6)]:s+=path([(x,y),(x+1,y),(x+1,y+1),(x,y+1)])+node(x+.5,y+.5,str(n))
fig(d,'patron_cube',s+node(2,-1.6,'six carrés égaux'))
s=''
# Patron à échelle 0,55 : bande 4x2,3x2,4x2,3x2 et deux bases 4x3.
for x,y,w,h in [(0,0,4,2),(4,0,3,2),(7,0,4,2),(11,0,3,2),(0,2,4,3),(0,-3,4,3)]:
    s+=path([(x*.5,y*.5),((x+w)*.5,y*.5),((x+w)*.5,(y+h)*.5),(x*.5,(y+h)*.5)])+node((x+w/2)*.5,(y+h/2)*.5,f'{w} × {h}')
fig(d,'patron_pave',s+node(3.5,-2,'dimensions en cm'))
if __name__=='__main__':
    names=[['angle','types','somme','pliage'],['polygones','triangles','quadrilateres','trapeze'],['droites','cercle','rectangle','compas'],['vertical','horizontal','diagonal','axes'],['pave','familles','patron_cube','patron_pave']]
    for d,ns in zip(mod.DIRS,names):
        mod.write(d,'figures/figures.py','# -*- coding: utf-8 -*-\nFIGURES = '+repr(F[d])+'\n')
        cor={'cours':{'nouveau':{}},'fiches':{'nouvelle':{}},'exercices':{}}
        for i,n in enumerate(ns,1):cor['cours']['nouveau'][str(i)]={'fichier':n+'.png','alt':'Figure géométrique : '+n.replace('_',' ')}
        for i,e in enumerate(mod.EX[d],1):
            if e['fig']:
                nom=e['fig']+('_point' if d=='16_symetrie' and e['fig'] in ('vertical','horizontal','diagonal') else '')
                cor['exercices']['nouveau-'+str(i)]={'1':{'fichier':nom+'.png','alt':'Schéma du corrigé : '+nom.replace('_',' ')}}
        mod.write(d,'figures/correspondance.json',json.dumps(cor,ensure_ascii=False,indent=2))
    print('20 figures TikZ et correspondances écrites.')
