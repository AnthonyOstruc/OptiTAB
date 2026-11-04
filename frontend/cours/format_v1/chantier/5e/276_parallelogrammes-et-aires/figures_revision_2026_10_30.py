# -*- coding: utf-8 -*-
"""Figures pédagogiques des exercices diversifiés ; TikZ uniquement."""
from pathlib import Path
import math
import runpy

ROOT=Path(__file__).resolve().parent.parent
FIG={n:{} for n in range(276,281)}
def tikz(s):return r'\begin{tikzpicture}[line cap=round,line join=round]'+'\n'+s+'\n'+r'\end{tikzpicture}'
def node(x,y,label,anchor='center',color='otInk'):
    return rf'\node[anchor={anchor},text={color}] at ({x},{y}) {{{label}}};'+'\n'
def line(points,color='otNavy',extra=''):
    return rf'\draw[{color},line width=.9pt{","+extra if extra else ""}] '+'--'.join(f'({x},{y})' for x,y in points)+';\n'

# Construction du parallélogramme : même géométrie, informations ajoutées en vert.
for name,level in [('construction_depart',0),('construction_fin',1),('construction_diagonales',2)]:
    s=line([(0,0),(4.6,0),(5.7,2)])
    if level:s+=line([(0,0),(1.1,2),(5.7,2)],'otGreenDark')
    for x,y,l,a in [(0,-.08,'$A$','north east'),(4.68,-.08,'$B$','north west'),(5.78,2.08,'$C$','south west')]:s+=node(x,y,l,a)
    if level:s+=node(1.02,2.08,'$D$','south east','otGreenDark')
    if level==2:
        s+=line([(0,0),(5.7,2)],'otGreenDark','dashed')+line([(1.1,2),(4.6,0)],'otGreenDark','dashed')
        s+=r'\fill[otGreenDark] (2.85,1) circle (1.5pt);'+'\n'+node(3,1.22,'$O$','south west','otGreenDark')
    FIG[276][name]=tikz(s)

for correct,name in [(False,'parcelle'),(True,'parcelle_corrige')]:
    s=r'\fill[otNavy!6] (0,0)--(4.2,0)--(4.9,1.4)--(.7,1.4)--cycle;'+'\n'
    s+=r'\fill[otGreen!12] (.7,1.4)--(4.9,1.4)--(2.8,2.8)--cycle;'+'\n'
    s+=line([(0,0),(4.2,0),(4.9,1.4),(2.8,2.8),(.7,1.4),(0,0)])+line([(.7,1.4),(4.9,1.4)],'otMuted','dashed')
    for x,y,label,anchor in [(-.05,-.08,'$A$','north east'),(4.25,-.08,'$B$','north west'),(5.02,1.55,'$C$','south west'),(.58,1.52,'$D$','south east'),(2.8,2.95,'$E$','south')]:s+=node(x,y,label,anchor)
    s+=r'\draw[cote] (-.65,0)--(-.65,1.4) node[coteTexte,midway] {$2\,\mathrm m$};'+'\n'
    s+=r'\draw[cote] (5.75,1.4)--(5.75,2.8) node[coteTexte,midway] {$2\,\mathrm m$};'+'\n'
    s+=line([(-.8,0),(0,0)],'otMuted','dashed')+line([(-.8,1.4),(.45,1.4)],'otMuted','dashed')
    s+=line([(4.9,1.4),(5.9,1.4)],'otMuted','dashed')+line([(3.05,2.8),(5.9,2.8)],'otMuted','dashed')
    s+=node(2.1,-.25,r'$6\,\mathrm m$','north')
    if correct:s+=node(2.5,.65,r'$12\,\mathrm m^2$','center','otGreenDark')+node(2.8,1.95,r'$6\,\mathrm m^2$','center','otGreenDark')
    FIG[276][name]=tikz(s)

for correct,name in [(False,'terrasse'),(True,'terrasse_corrige')]:
    s=r'\fill[otNavy!5] (0,0) rectangle (4.8,3.2);'+'\n'
    s+=r'\fill[otGreen!20] (1,.8)--(3.4,.8)--(4,2.4)--(1.6,2.4)--cycle;'+'\n'
    s+=line([(0,0),(4.8,0),(4.8,3.2),(0,3.2),(0,0)])+line([(1,.8),(3.4,.8),(4,2.4),(1.6,2.4),(1,.8)],'otGreenDark')
    s+=r'\draw[cote] (-.55,0)--(-.55,3.2) node[coteTexte,midway] {$4\,\mathrm m$};'+'\n'
    s+=r'\draw[cote] (4.3,.8)--(4.3,2.4) node[coteTexte,midway] {$2\,\mathrm m$};'+'\n'
    s+=node(2.4,-.2,r'$6\,\mathrm m$','north')+node(2.2,.57,r'$3\,\mathrm m$','north')
    s+=node(2.5,1.65,r'$6\,\mathrm m^2$' if correct else 'Massif','center','otGreenDark')
    if correct:s+=node(2.4,-.85,r'Surface à daller : $18\,\mathrm m^2$','north','otGreenDark')
    FIG[276][name]=tikz(s)

# Patrons de cube. Le carré central de A est repéré dans la correction.
cross=[(1,0),(0,1),(1,1),(2,1),(1,2),(1,3)]
for correct,name in [(False,'patrons_cube'),(True,'patron_cube_corrige')]:
    s=''
    for x,y in cross:
        color='otGreenDark' if correct else 'otNavy'
        s+=rf'\draw[{color},fill={"otGreen!12" if correct else "otNavy!5"}] ({x},{y}) rectangle ({x+1},{y+1});'+'\n'
    for x in range(3):
        for y in range(2):s+=rf'\draw[otMuted,fill=otRule!30] ({x+4.6},{y+1}) rectangle ({x+5.6},{y+2});'+'\n'
    s+=node(1.5,-.25,'A','north','otGreenDark' if correct else 'otInk')+node(6.1,-.25,'B','north')
    if correct:
        s+=node(1.5,1.5,'Base','center','otGreenDark')
        s+=r'\draw[otOrange,line width=1.2pt] (5.6,2) circle (.13);'+'\n'
        s+=node(6.1,3.3,'4 carrés au même point','south','otMuted')
    FIG[277][name]=tikz(s)

s=r'''\fill[otNavy!5] (0,0) rectangle (4.18879,1.66667);
\draw[geoTrait] (0,0) rectangle (4.18879,1.66667);
\draw[geoTrait] (2.0944,2.33334) circle (.66667);
\draw[geoTrait] (2.0944,-.66667) circle (.66667);
\draw[otOrange] (2.0944,2.33334)--(2.76107,2.33334);
\draw[cote] (4.8,0)--(4.8,1.66667) node[coteTexte,midway] {$5\,\mathrm{cm}$};
\draw[cote] (0,-1.8)--(4.18879,-1.8) node[coteTexte,midway] {$4\pi\,\mathrm{cm}$};
'''+node(2.0944,3.12,r'$r=2\,\mathrm{cm}$','south')
FIG[277]['patron_cylindre_mesure']=tikz(s)
s=''
for x,h in enumerate([3,2,2]):
    for y in range(h):s+=rf'\draw[otGreenDark,fill=otGreen!12] ({x},{y}) rectangle ({x+1},{y+1});'+'\n'
    s+=node(x+.5,-.2,str(x+1),'north')
s+=node(1.5,3.4,'Vue de face','south','otGreenDark')+node(1.5,-.8,'Colonnes','north')
FIG[277]['empilement_face']=tikz(s)

def bars(correct=False):
    s=''
    for value in [0,6,12,18]:
        y=value/6;s+=line([(0,y),(5.8,y)],'otRule')+node(-.16,y,f'${value}$','east')
    s+=line([(0,0),(0,3.5)],'otMuted','-{Stealth[length=1.8mm]}')+line([(0,0),(5.9,0)],'otMuted','-{Stealth[length=1.8mm]}')
    for x,v,label in zip([.8,1.8,2.8,3.8,4.8],[12,18,15,9,6],['Lun','Mar','Mer','Jeu','Ven']):
        s+=rf'\fill[{"otGreenDark" if correct and label in ["Mer","Ven"] else "otNavy"}] ({x-.3},0) rectangle ({x+.3},{v/6});'+'\n'
        s+=node(x,-.18,label,'north')
        if correct:s+=node(x,v/6+.12,f'${v}$','south','otGreenDark')
    return tikz(s+node(0,3.7,'Livres empruntés','south west','otMuted'))
FIG[278]['bibliotheque']=bars();FIG[278]['bibliotheque_corrige']=bars(True)

def pie(angles,labels,colors,letters=False):
    start=0;s='';r=1.4
    for i,(angle,label,color) in enumerate(zip(angles,labels,colors)):
        end=start+angle
        s+=rf'\fill[{color}] (0,0)--({r*math.cos(math.radians(start)):.5f},{r*math.sin(math.radians(start)):.5f}) arc[start angle={start},end angle={end},radius={r}]--cycle;'+'\n'
        for theta in [start]:s+=line([(0,0),(r*math.cos(math.radians(theta)),r*math.sin(math.radians(theta)))],'white')
        if letters:
            mid=math.radians(start+angle/2);s+=node(.83*math.cos(mid),.83*math.sin(mid),label)
        else:s+=node(1.85,.8-i*.8,label,'west')
        start=end
    return tikz(s)
FIG[278]['transports40']=pie([90,162,108],[r'À pied : $25\,\%$',r'Vélo : $45\,\%$',r'Bus : $30\,\%$'],['otNavy!65','otGreen!65','otOrange!75'])
for correct,name in [(False,'temperatures'),(True,'temperatures_corrige')]:
    s=''
    for v in [0,4,8,12,16]:s+=line([(0,v/5),(5.2,v/5)],'otRule')+node(-.15,v/5,f'${v}$','east')
    s+=line([(0,0),(0,3.8)],'otMuted','-{Stealth[length=1.8mm]}')+line([(0,0),(5.4,0)],'otMuted','-{Stealth[length=1.8mm]}')
    points=[(.2+1.2*i,v/5) for i,v in enumerate([8,12,16,14,10])]
    s+=line(points,'otGreenDark' if correct else 'otNavy')
    for (x,y),hour,value in zip(points,[8,10,12,14,16],[8,12,16,14,10]):
        s+=rf'\fill[{"otGreenDark" if correct else "otNavy"}] ({x},{y}) circle (1.7pt);'+'\n'+node(x,-.18,f'${hour}$ h','north')
        if correct:
            if value==14:s+=node(x+.4,y+.05,f'${value}$','west','otGreenDark')
            elif value==10:s+=node(x+.2,y+.05,f'${value}$','west','otGreenDark')
            else:s+=node(x,y+.15,f'${value}$','south','otGreenDark')
    s+=node(0,4.0,'Température (°C)','south west','otMuted')
    FIG[278][name]=tikz(s)

FIG[279]['roue_aabb']=pie([90]*4,['A','A','B','B'],['otNavy!20','otNavy!20','otOrange!30','otOrange!30'],True)
FIG[279]['roue_aabb_corrige']=pie([90]*4,['A','A','B','B'],['otGreen!40','otGreen!40','otRule','otRule'],True)
FIG[279]['roue_inegale']=pie([180,90,90],[r'Rouge : $180^\circ$',r'Bleu : $90^\circ$',r'Vert : $90^\circ$'],['otRed!65','otNavy!50','otGreen!65'])
FIG[279]['roue_egale']=pie([120]*3,[r'Rouge : $120^\circ$',r'Bleu : $120^\circ$',r'Vert : $120^\circ$'],['otRed!65','otNavy!50','otGreen!65'])

def trace(points,labels,closed=False,side1=None,side2=None):
    color='otGreenDark';s='';segments=list(zip(points,points[1:]))
    if closed:segments.append((points[-1],points[0]))
    for a,b in segments:
        s+=line([a,b],color)
        start=(a[0]+.38*(b[0]-a[0]),a[1]+.38*(b[1]-a[1]));end=(a[0]+.62*(b[0]-a[0]),a[1]+.62*(b[1]-a[1]))
        s+=line([start,end],color,'-{Stealth[length=1.8mm,width=1.4mm]}')
    for (x,y),label in zip(points,labels):
        a='north east' if (x,y)==points[0] else ('north west' if y==0 else 'south west')
        s+=node(x+(-.1 if a=='north east' else .1),y+(-.1 if y==0 else .1),f'${label}$',a,color)
    if side1:s+=node((points[0][0]+points[1][0])/2,-.36,side1,'north',color)
    if side2:s+=node(points[1][0]+.3,(points[1][1]+points[2][1])/2,side2,'west',color)
    return tikz(s)
FIG[280]['trajet_l']=trace([(0,0),(3,0),(3,2)],['A','B','C'],side1='30 pas',side2='20 pas')
FIG[280]['rectangle_30_20']=trace([(0,0),(3,0),(3,2),(0,2)],['A','B','C','D'],True,'30 pas','20 pas')
FIG[280]['carre_incomplet']=trace([(0,0),(2.6,0),(2.6,2.6),(0,2.6)],['A','B','C','D'],False,'20 pas','20 pas')
FIG[280]['carre_20']=trace([(0,0),(2.6,0),(2.6,2.6),(0,2.6)],['A','B','C','D'],True,'20 pas','20 pas')
FIG[280]['escalier']=trace([(0,0),(3,0),(3,1.2),(6,1.2),(6,2.4)],['A','B','C','D','E'],False,'50 pas','20 pas')
FIG[280]['rectangle_50_20']=trace([(0,0),(4,0),(4,1.6),(0,1.6)],['A','B','C','D'],True,'50 pas','20 pas')
FIG[280]['rectangle_8_5']=trace([(0,0),(4,0),(4,2.5),(0,2.5)],['A','B','C','D'],True,r'$8\,\mathrm m$',r'$5\,\mathrm m$')
s=trace([(0,0),(4,0),(2,3.4641)],['A','B','C'],True,'40 pas')
s=s.replace(r'\end{tikzpicture}',line([(4,0),(5.3,0)],'otMuted','dashed')+r'\draw[otOrange,line width=.8pt] (4.55,0) arc[start angle=0,end angle=120,radius=.55];'+'\n'+node(4.75,.8,r'$120^\circ$','west','otOrange')+r'\end{tikzpicture}')
FIG[280]['triangle_40']=s

def main():
    for num,figures in FIG.items():
        p=next(ROOT.glob(f'{num}_*'));old=p/'sauvegardes/revision_2026-10-30/figures/figures.py'
        original=old.read_text(encoding='utf8')
        extra='\n\n# Figures pédagogiques ajoutées lors de la révision du 30 octobre 2026.\nFIGURES.update({\n'
        extra+=''.join(repr(n)+': r"""'+code+'""",\n' for n,code in figures.items())+'})\n'
        (p/'figures/figures.py').write_text(original+extra,encoding='utf8')

if __name__=='__main__':main()
