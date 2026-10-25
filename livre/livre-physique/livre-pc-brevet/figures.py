"""Quarante schémas vectoriels originaux, construits dans un repère commun."""
from pathlib import Path
import json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as _Circle,Rectangle,Polygon,Arc,FancyArrowPatch
from matplotlib.ticker import FuncFormatter

HERE=Path(__file__).resolve().parent
OUT=HERE/'figures';OUT.mkdir(exist_ok=True)
NAVY='#1B3C8E';GREEN='#3B8544';MUTED='#667085';LIGHT='#E5EAF3';INK='#1C2130';RED='#B94343'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':INK,'text.color':INK,'axes.edgecolor':MUTED,'xtick.color':MUTED,'ytick.color':MUTED})
records=[]
def Circle(*args,**kwargs):
    kwargs.setdefault('zorder',3)
    return _Circle(*args,**kwargs)
def canvas():
    f,a=plt.subplots(figsize=(6.5,2.2));f.subplots_adjust(left=.01,right=.99,bottom=.02,top=.97)
    a.set(xlim=(0,16),ylim=(0,5.3),aspect='equal');a.axis('off');return f,a
def text(a,x,y,s,c=INK,size=8.5,ha='center',va='center',**kw):
    return a.text(x,y,s,color=c,fontsize=size,ha=ha,va=va,zorder=6,**kw)
def line(a,points,c=NAVY,lw=1.4,**kw):
    a.plot(*zip(*points),color=c,lw=lw,solid_capstyle='round',**kw)
def arrow(a,p,q,c=NAVY,label='',off=(0,.3)):
    a.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=10,lw=1.3,color=c,zorder=4))
    if label:text(a,(p[0]+q[0])/2+off[0],(p[1]+q[1])/2+off[1],label,c,8,bbox=dict(facecolor='white',edgecolor='none',pad=.4))
def box(a,x,y,w,h,label,fill=LIGHT,c=NAVY):
    a.add_patch(Rectangle((x,y),w,h,fc=fill,ec=c,lw=1.1,zorder=3));text(a,x+w/2,y+h/2,label,c,8)
def save(name,f):
    for ax in f.axes:
        if ax.axison:
            ax.xaxis.set_major_formatter(FuncFormatter(lambda x,pos: f'{x:g}'.replace('.',',')))
            ax.yaxis.set_major_formatter(FuncFormatter(lambda x,pos: f'{x:g}'.replace('.',',')))
    p=OUT/(name+'.pdf');f.savefig(p,metadata={'Title':'OptiTAB - '+name,'Author':'OptiTAB'});plt.close(f);records.append(name)
def graph(name,xlabel,ylabel,series,xlim=None,ylim=None):
    f,a=plt.subplots(figsize=(6.3,2.25));f.subplots_adjust(left=.13,right=.97,bottom=.25,top=.93)
    for x,y,label,c in series:a.plot(x,y,'o-',color=c,lw=1.5,ms=3,label=label)
    a.set(xlabel=xlabel,ylabel=ylabel)
    if xlim:a.set_xlim(xlim)
    if ylim:a.set_ylim(ylim)
    a.grid(color=LIGHT,lw=.7);a.set_axisbelow(True)
    if any(s[2] for s in series):a.legend(fontsize=8,frameon=True,facecolor='white',edgecolor=LIGHT,loc='best')
    save(name,f)
def cylinder(a,x,y,level,label):
    line(a,[(x,y+3),(x,y),(x+1.7,y),(x+1.7,y+3)])
    a.add_patch(Rectangle((x+.03,y+.03),1.64,level,fc='#DDEBF7',ec='none'))
    for j in range(1,6):line(a,[(x+1.25,y+j*.45),(x+1.7,y+j*.45)],MUTED,.6)
    text(a,x+.85,y+3.5,label,NAVY,8)
def molecule(a,x,y,species,scale=.32):
    atoms={'H2O':[(-.6,0,'H'),(0,.35,'O'),(.6,0,'H')], 'CO2':[(-.85,0,'O'),(0,0,'C'),(.85,0,'O')], 'O2':[(-.4,0,'O'),(.4,0,'O')], 'N2':[(-.4,0,'N'),(.4,0,'N')], 'H2':[(-.4,0,'H'),(.4,0,'H')], 'CH4':[(0,0,'C'),(-.7,0,'H'),(.7,0,'H'),(0,.7,'H'),(0,-.7,'H')]}
    data=atoms[species];colors={'H':'#FFFFFF','O':'#CE5F5F','C':'#596071','N':'#5979B3'}
    pairs=[(0,1),(1,2)] if species in ['H2O','CO2'] else [(0,j) for j in range(1,len(data))]
    for i,j in pairs:line(a,[(x+data[i][0],y+data[i][1]),(x+data[j][0],y+data[j][1])],MUTED,1)
    # La composition, plutôt que la géométrie fine, est l’objet du modèle.
    for dx,dy,atom in data:
        a.add_patch(Circle((x+dx,y+dy),scale,fc=colors[atom],ec=MUTED,lw=.9))
        text(a,x+dx,y+dy,atom,'white' if atom!='H' else INK,7)
def wire(a,pts):line(a,pts)
def component(a,x,y,label,kind='R',vertical=False):
    a.add_patch(Circle((x,y),.43,fc='white',ec='none'))
    if kind=='R':
        a.add_patch(Rectangle((x-.55,y-.25),1.1,.5,fc='white',ec=NAVY,lw=1.3,zorder=4));text(a,x,y+.65,label,NAVY,8)
    else:
        a.add_patch(Circle((x,y),.38,fc='white',ec=NAVY,lw=1.3))
        if kind=='L':line(a,[(x-.26,y-.26),(x+.26,y+.26)],zorder=5);line(a,[(x-.26,y+.26),(x+.26,y-.26)],zorder=5)
        else:text(a,x,y,kind,NAVY,8.5)
        if label:text(a,x+( .65 if vertical else 0),y+(0 if vertical else .65),label,NAVY,7.5,ha='left' if vertical else 'center')
    if kind=='G':text(a,x-.6,y+.65,'+',GREEN,10);text(a,x-.6,y-.65,'−',GREEN,10)
def measure_circuit(name,voltmeter=True,ammeter=True):
    f,a=canvas();wire(a,[(2,1),(2,4),(14,4),(14,1),(2,1)])
    component(a,2,2.5,'source','G',True);component(a,9,4,'R','R')
    if ammeter:component(a,5,4,'','A');arrow(a,(3,4),(4,4),GREEN,'I',off=(0,.5))
    if voltmeter:
        wire(a,[(7,4),(7,2.2),(11,2.2),(11,4)]);component(a,9,2.2,'','V')
        for x in [7,11]:a.add_patch(Circle((x,4),.07,fc=NAVY));text(a,x,4.8,'B' if x==7 else 'C',NAVY,8)
        text(a,8,1.55,'V',GREEN,8);text(a,10,1.55,'COM',GREEN,8)
    text(a,12,1.45,'courant continu',MUTED,8)
    save(name,f)

def construire():
    f,a=canvas();cylinder(a,3,.5,1.3,'30,0 mL');cylinder(a,10,.5,2.2,'50,0 mL')
    a.add_patch(Polygon([(10.4,.7),(11.1,.65),(11.4,1.15),(10.9,1.55),(10.45,1.2)],fc='#B1B7C3',ec=NAVY))
    arrow(a,(5.3,2),(8.8,2),label='immersion complète');text(a,8,.35,'V = 50,0 − 30,0 = 20,0 mL',GREEN,9);save('c01-mesure',f)
    graph('c01-rho','Volume (mL)','Masse (g)',[(np.array([0,10,20,30]),np.array([0,10,20,30]),'Eau, 1,00 g/mL',NAVY),(np.array([0,10,20,30]),np.array([0,27,54,81]),'Aluminium, 2,70 g/cm³',GREEN)],(0,32),(0,90))
    f,a=canvas();colors=[NAVY,GREEN,'#DB9A38'];data=[78,21,1];xx=1
    for value,color in zip(data,colors):a.add_patch(Rectangle((xx,2.5),14*value/100,1,fc=color,ec='white'));xx+=14*value/100
    for x,label,color in [(3,'Diazote : 78 %',NAVY),(9,'Dioxygène : 21 %',GREEN),(13,'Autres : 1 %','#A77723')]:text(a,x,1.2,label,color,8.5)
    text(a,8,4.3,'Air sec · proportions en volume',NAVY,10);save('c02-air',f)
    f,a=canvas()
    for x,w,label in [(1,5,'Volume plus grand'),(10,3,'Volume plus petit')]:
        box(a,x,1.4,w,2,'',fill='white');line(a,[(x+w,1.1),(x+w,3.7)],GREEN,3);line(a,[(x+w,2.4),(x+w+1,2.4)],GREEN,2)
        for j in range(12):a.add_patch(Circle((x+.4+(j%4)*(w-.8)/3,1.8+(j//4)*.6),.09,fc=NAVY))
        text(a,x+w/2,4.4,label,NAVY,9)
    arrow(a,(7,2.4),(9,2.4),GREEN,'comprimer',off=(0,.5));text(a,8,.55,'Même nombre de particules · seringue étanche',MUTED,8);save('c02-pression',f)
    f,a=canvas();rng=np.random.default_rng(2026)
    for idx,label in enumerate(['Solide','Liquide','Gaz']):
        x=.5+idx*5.3;box(a,x,1,4.5,3,'',fill='white');text(a,x+2.25,4.6,label,NAVY,10)
        pts=[(x+.8+(j%4)*.85,1.6+(j//4)*.65) for j in range(12)] if idx==0 else [(x+.5+rng.random()*3.5,1.4+rng.random()*(1.4 if idx==1 else 2.2)) for j in range(12)]
        for px,py in pts:a.add_patch(Circle((px,py),.11,fc=NAVY if idx<2 else GREEN))
    save('c03-etats',f)
    graph('c03-courbe','Temps de chauffage (min)','Température (°C)',[(np.arange(0,9),[20,40,60,80,100,100,100,100,100],'Eau pure · pression fixée',NAVY)],(0,8),(0,110))
    f,a=canvas();box(a,1,1.5,3,2,'eau + sel\ndissous',fill='#E2EFF8');arrow(a,(4.5,2.5),(7,2.5),GREEN,'filtration',off=(0,.5));box(a,8,1.5,3,2,'eau + sel\ndissous',fill='#E2EFF8');text(a,13,2.5,'Le filtre ordinaire\nne retient pas\nle sel dissous.',NAVY,9);save('c04-dissolution',f)
    f,a=canvas();cmap=plt.get_cmap('RdYlBu')
    for p in range(15):a.add_patch(Rectangle((.5+p,2),1,.8,fc=cmap(p/14),ec='white'));text(a,1+p,1.5,str(p),INK,8)
    text(a,3.5,3.8,'Acide : pH < 7',RED,9);text(a,8,4.5,'Neutre : pH = 7',GREEN,9);text(a,12.5,3.8,'Basique : pH > 7',NAVY,9)
    text(a,8,.4,'Solutions aqueuses usuelles · vers 25 °C',MUTED,8);save('c04-ph',f)
    f,a=canvas()
    for x,s,label in [(2,'H2O','Eau · H₂O'),(6,'CO2','Dioxyde de carbone · CO₂'),(10,'O2','Dioxygène · O₂'),(14,'CH4','Méthane · CH₄')]:molecule(a,x,2.8,s);text(a,x,1,label,NAVY,7.5)
    save('c05-molecules',f)
    f,a=canvas();els=[('H','Hydrogène',1),('C','Carbone',6),('N','Azote',7),('O','Oxygène',8),('Na','Sodium',11),('Cl','Chlore',17),('Al','Aluminium',13),('Fe','Fer',26)]
    for j,(sym,name,z) in enumerate(els):
        x=.3+(j%4)*4;y=2.8-(j//4)*2.4;box(a,x,y,3.4,2,'');text(a,x+.35,y+1.65,str(z),MUTED,7,ha='left');text(a,x+1.7,y+1.15,sym,NAVY,13);text(a,x+1.7,y+.4,name,INK,8)
    save('c05-tableau',f)
    f,a=canvas();labels=[('CO₂','Eau de chaux\ntroublée'),('O₂','Bûchette\nravivée'),('H₂','Petite détonation\n(test encadré)'),('H₂O','Réactif anhydre\nqui bleuit')]
    for j,(gas,result) in enumerate(labels):
        x=.5+j*4;box(a,x,2.6,3.4,1.3,gas);arrow(a,(x+1.7,2.4),(x+1.7,1.8),GREEN);text(a,x+1.7,1,result,NAVY,8)
    save('c06-tests',f)
    f,a=canvas();molecule(a,1.2,2.8,'H2');text(a,2.6,2.8,'+',NAVY,12);molecule(a,4,2.8,'H2');text(a,5.4,2.8,'+',NAVY,12);molecule(a,6.8,2.8,'O2');arrow(a,(8,2.8),(9.5,2.8),GREEN);molecule(a,11,2.8,'H2O');text(a,12.6,2.8,'+',NAVY,12);molecule(a,14.3,2.8,'H2O');text(a,8,.8,'Avant : 4 H et 2 O                      Après : 4 H et 2 O',NAVY,9);save('c06-reaction',f)
    f,a=canvas();p=[(8,4.6),(3,.7),(13,.7)];line(a,p+[p[0]],NAVY,2)
    text(a,8,4.95,'Énergie d’activation',GREEN,9);text(a,2.5,.25,'Combustible',NAVY,9);text(a,13.5,.25,'Comburant',NAVY,9);text(a,8,2.25,'COMBUSTION',NAVY,11);save('c07-triangle',f)
    f,a=canvas();box(a,.7,2,3.5,1.5,'Carbone\n3 g');text(a,4.8,2.75,'+',NAVY,14);box(a,5.5,2,4,1.5,'Dioxygène\n8 g');arrow(a,(10,2.75),(11.2,2.75),GREEN);box(a,11.7,2,3.6,1.5,'CO₂\n11 g');text(a,8,.8,'3 g + 8 g = 11 g · Bilan matériel complet',GREEN,9);save('c07-bilan',f)
    f,a=canvas();names=['Mercure','Vénus','Terre','Mars','Jupiter','Saturne','Uranus','Neptune'];radii=[.13,.2,.21,.16,.44,.4,.3,.29]
    a.add_patch(Circle((.8,2.8),.55,fc='#DB9A38'));text(a,.8,4.1,'Soleil',NAVY,8)
    for j,(name,r) in enumerate(zip(names,radii)):
        x=2.5+j*1.8;a.add_patch(Circle((x,2.8),r,fc=[MUTED,'#C79B67',NAVY,RED,'#A78A68','#D0B984','#68A9AB','#486FAD'][j]));text(a,x,1.8 if j%2==0 else 3.8,name,INK,7.5)
    text(a,8,.4,'Ordre des planètes · ni tailles ni distances à l’échelle',MUTED,8);save('c08-systeme',f)
    f,a=canvas()
    for j,(label,sub) in enumerate([('Terre','planète'),('Système solaire','une étoile et ses objets'),('Voie lactée','notre galaxie'),('Univers observable','de nombreuses galaxies')]):
        x=.2+j*4;box(a,x,1.7,3.5,2,label+'\n'+sub); 
        if j<3:arrow(a,(x+3.55,2.7),(x+3.98,2.7),GREEN)
    save('c08-echelles',f)
    f,a=canvas()
    for y,xs,label in [(3.6,[1,3,5,7,9,11],'Valeur de vitesse constante'),(1.5,[1,2,3.5,5.5,8,11],'Valeur de vitesse croissante')]:
        line(a,[(.5,y),(13,y)],LIGHT,1)
        for i,x in enumerate(xs):a.add_patch(Circle((x,y),.14,fc=NAVY));text(a,x,y-.45,str(i),MUTED,7)
        text(a,8,y+.65,label,GREEN,8)
    text(a,14.2,2.5,'Même durée\nentre deux\npositions',MUTED,8);save('c09-chrono',f)
    graph('c09-graphique','Temps (s)','Position (m)',[(np.array([0,1,2,3,4]),np.array([0,2,4,6,8]),'2 m/s',NAVY),(np.array([0,1,2,3,4]),np.array([0,1,2,3,4]),'1 m/s',GREEN)],(0,4.2),(0,9))
    f,a=canvas();box(a,6,2,4,1.3,'Livre');box(a,.5,2,3,1.3,'Table');box(a,12.5,2,3,1.3,'Terre');line(a,[(3.5,2.65),(6,2.65)]);line(a,[(10,2.65),(12.5,2.65)],GREEN,1.4,ls='--');text(a,4.7,3.7,'contact',NAVY,8);text(a,11.2,3.7,'distance',GREEN,8);text(a,8,.7,'Système : le livre · air négligé',MUTED,8);save('c10-doi',f)
    f,a=canvas();box(a,6.6,2,2.8,.6,'Livre');line(a,[(3,1.9),(13,1.9)],MUTED,2);arrow(a,(8,2),(8,4.6),GREEN);arrow(a,(8,2.3),(8,.1),NAVY);text(a,10.7,4,'Action de la table',GREEN,8);text(a,10.7,.55,'Action de la Terre',NAVY,8);text(a,3.2,3.2,'Même objet\ndeux actions',MUTED,8);save('c10-forces',f)
    f,a=canvas()
    for x,label,weight,length in [(4,'Terre','6,0 N',2.4),(12,'Lune','0,96 N',.65)]:
        box(a,x-1,3,2,1,'0,600 kg');arrow(a,(x,3),(x,3-length),GREEN);text(a,x+1.6,2,weight,GREEN,9);text(a,x,4.6,label,NAVY,10)
    text(a,8,.15,'Les longueurs sont schématiques ; les valeurs sont indiquées.',MUTED,7.5);save('c11-terrelune',f)
    graph('c11-graphique','Masse (kg)','Poids (N)',[(np.array([0,.2,.4,.6,.8,1]),np.array([0,2,4,6,8,10]),'Terre : g = 10 N/kg',NAVY),(np.array([0,.2,.4,.6,.8,1]),np.array([0,.32,.64,.96,1.28,1.6]),'Lune : g = 1,6 N/kg',GREEN)],(0,1.05),(0,11))
    f,a=canvas();box(a,.4,2.4,3.1,1.2,'Pile');box(a,6.2,2.4,3.3,1.2,'Lampe');box(a,12,3.3,3.5,1.1,'Environnement');box(a,12,.7,3.5,1.1,'Environnement');arrow(a,(3.7,3),(6,3),GREEN,'électrique',off=(0,.6));arrow(a,(9.7,3.2),(11.8,3.85),NAVY,'rayonnement',off=(0,.55));arrow(a,(9.7,2.8),(11.8,1.25),GREEN,'thermique',off=(0,-.5));save('c12-chaine',f)
    f,a=canvas();a.add_patch(Circle((8,2.5),.95,fc=LIGHT,ec=NAVY,lw=1.4));text(a,8,2.5,'Terre +\natmosphère',NAVY,8)
    arrow(a,(.5,4),(6.9,2.9),'#C18A24','solaire reçu',off=(0,.65));arrow(a,(7.6,3.4),(5,5),'#C18A24');text(a,3.2,4.8,'part renvoyée',MUTED,8);arrow(a,(9,2.8),(15.3,4),RED,'infrarouge émis',off=(0,.7));text(a,8,.6,'Comparer les entrées, les sorties et le stockage',MUTED,8);save('c12-terre',f)
    f,a=canvas()
    for offset,parallel in [(0,False),(8,True)]:
        x=offset+.7;wire(a,[(x,1),(x,4),(x+6,4),(x+6,1),(x,1)]);component(a,x,2.5,'','G',True);component(a,x+3,4,'L₁','L')
        if parallel:
            wire(a,[(x+1.3,4),(x+1.3,2),(x+6,2)]);component(a,x+3.4,2,'L₂','L')
            for px,py in [(x+1.3,4),(x+6,2)]:a.add_patch(Circle((px,py),.07,fc=NAVY))
        else:component(a,x+6,2.5,'L₂','L',True)
        text(a,x+3,.35,'Dérivation' if parallel else 'Série',NAVY,9)
    save('c13-circuits',f)
    f,a=canvas();wire(a,[(2,1),(2,4),(14,4),(14,1),(2,1)]);component(a,2,2.5,'','G');component(a,11,4,'Lampe','L');box(a,5.5,3.7,2.2,.6,'Protection');text(a,8,1.8,'Si la protection s’ouvre, le trajet est interrompu.',MUTED,8);text(a,8,.4,'Principe seulement · aucun câblage du secteur',MUTED,8);save('c13-protection',f)
    measure_circuit('c14-amperemetre',False,True)
    f,a=canvas();wire(a,[(1,2.7),(7,2.7),(11,4.2),(15,4.2)]);wire(a,[(7,2.7),(11,1.2),(15,1.2)]);a.add_patch(Circle((7,2.7),.1,fc=NAVY));arrow(a,(2,2.7),(5.5,2.7),GREEN,'I_G');arrow(a,(8.4,3.2),(10.3,3.9),GREEN,'I₁',off=(.1,.4));arrow(a,(8.4,2.2),(10.3,1.5),GREEN,'I₂',off=(.1,-.4));text(a,4,.5,'I_G = I₁ + I₂',NAVY,11);save('c14-noeud',f)
    measure_circuit('c15-voltmetre',True,False)
    f,a=canvas();box(a,.7,2,6,1.8,'Série\nU_G = U₁ + U₂');box(a,8.3,2,7,1.8,'Dérivation sur mêmes nœuds\nU_G = U₁ = U₂');text(a,8,.7,'Avec des polarités cohérentes et des fils idéaux',MUTED,8);save('c15-lois',f)
    measure_circuit('c16-montage',True,True)
    graph('c16-ohm','Intensité (A)','Tension (V)',[(np.array([0,.01,.02,.03]),np.array([0,1,2,3]),'100 Ω',NAVY),(np.array([0,.01,.02,.03]),np.array([0,2,4,6]),'200 Ω',GREEN)],(0,.033),(0,6.5))
    f,a=canvas();box(a,1,3,5,1,'6 W pendant 10 s');box(a,1,1,5,1,'3 W pendant 20 s');arrow(a,(6.3,3.5),(10,2.8),GREEN);arrow(a,(6.3,1.5),(10,2.2),NAVY);box(a,10.5,1.8,4.5,1.5,'Même énergie\n60 J');save('c17-puissance',f)
    graph('c17-energie','Durée (s)','Énergie (J)',[(np.array([0,5,10,15,20]),np.array([0,30,60,90,120]),'6 W',NAVY),(np.array([0,5,10,15,20]),np.array([0,15,30,45,60]),'3 W',GREEN)],(0,21),(0,130))
    f,a=canvas();source=(1,2.7);a.add_patch(Circle(source,.12,fc='#DB9A38'));line(a,[(6,1.8),(6,3.6)],INK,4);line(a,[(14,.2),(14,5.1)],MUTED,2)
    a.add_patch(Polygon([source,(14,.36),(14,5.04)],fc='#F5EDD5',ec='none',zorder=-2));a.add_patch(Polygon([(6,1.8),(6,3.6),(14,5.04),(14,.36)],fc='#C7CDDA',ec='none',zorder=-1))
    for q in [(14,.36),(14,5.04)]:arrow(a,source,q,NAVY)
    text(a,1,1.3,'Source',NAVY,8);text(a,6,.8,'Objet opaque',NAVY,8);text(a,13.1,2.7,'Ombre',INK,8);text(a,14.7,4.8,'Écran',MUTED,8);save('c18-ombre',f)
    f,a=canvas();box(a,.5,1.8,3,1.6,'Émetteur /\nrécepteur');line(a,[(14,.5),(14,4.8)],MUTED,3);arrow(a,(3.8,3.6),(13.6,3.6),NAVY,'aller : d',off=(0,.4));arrow(a,(13.6,1.2),(3.8,1.2),GREEN,'retour : d',off=(0,-.4));text(a,8.5,2.4,'Trajet total : 2d',NAVY,10);text(a,14.5,2.6,'Réflecteur',MUTED,8,ha='left',rotation=90);save('c18-trajet',f)
    t=np.linspace(0,.02,400);f,axes=plt.subplots(2,1,figsize=(6.3,2.5),sharex=True);f.subplots_adjust(left=.13,right=.97,bottom=.21,top=.92,hspace=.48)
    for ax,freq,color in [(axes[0],200,NAVY),(axes[1],400,GREEN)]:ax.plot(t*1000,np.sin(2*np.pi*freq*t),color=color,lw=1.1);ax.set(ylim=(-1.3,1.3),yticks=[],ylabel=str(freq)+' Hz');ax.grid(color=LIGHT)
    axes[1].set_xlabel('Temps (ms)');save('c19-signaux',f)
    f,a=canvas();box(a,.5,1.8,3,1.6,'Sonar');line(a,[(14,.5),(14,4.8)],MUTED,3);arrow(a,(3.8,3.6),(13.6,3.6),NAVY,'aller',off=(0,.4));arrow(a,(13.6,1.2),(3.8,1.2),GREEN,'retour de l’écho',off=(0,-.4));text(a,8.5,2.4,'2d = v Δt',NAVY,12);text(a,14.6,2.5,'Paroi',MUTED,8,ha='left');save('c19-echo',f)
    f,a=canvas();boxes=[(.2,'Émetteur\nlampe'),(6.2,'Propagation\nlumineuse'),(12.2,'Récepteur\ncapteur')]
    for x,label in boxes:box(a,x,2,3.6,1.6,label)
    arrow(a,(4,2.8),(6,2.8),GREEN);arrow(a,(10,2.8),(12,2.8),GREEN);text(a,8,.8,'Un code partagé associe les états du signal au message.',MUTED,8);save('c20-chaine',f)
    f,axes=plt.subplots(1,2,figsize=(6.4,2.2));f.subplots_adjust(left=.07,right=.98,bottom=.24,top=.85,wspace=.35);t=np.linspace(0,4,200)
    axes[0].plot(t,1+.6*np.sin(2*t),color=NAVY);axes[0].set(title='Signal analogique',xlabel='Temps',ylabel='Sortie',ylim=(0,2))
    axes[1].step([0,1,2,3,4],[0,1,1,0,0],where='post',color=GREEN);axes[1].set(title='Code à deux états',xlabel='Temps',yticks=[0,1],ylim=(-.2,1.3))
    for ax in axes:ax.grid(color=LIGHT)
    save('c20-signaux',f)
    (HERE/'build').mkdir(exist_ok=True)
    (HERE/'build/figures.json').write_text(json.dumps(dict(nombre=len(records),figures=records),ensure_ascii=False,indent=2),encoding='utf8')
    print('Figures vectorielles :',len(records))

if __name__=='__main__':construire()
