"""Cours, entraînements et brevets blancs : conserver les seules figures utilisées."""
import json
import numpy as np
from matplotlib.patches import Rectangle
from figures import *
from donnees import charger
from brevets import SUJETS

def produire():
    construire()
    f,a=canvas()
    for k,label in enumerate(['Solide','Liquide','Gaz']):
        x=.3+k*5.3;box(a,x,1,4.7,3,'',fill='white');text(a,x+2.35,4.65,label,NAVY,10)
        for j in range(12):
            if k==0:px=x+.8+j%4*.9;py=1.55+j//4*.8
            elif k==1:px=x+.6+j%4*.98+(j//4%2)*.15;py=1.45+j//4*.55
            else:px=x+.4+(j*1.07)%3.9;py=1.3+(j*.73)%2.45
            a.add_patch(Circle((px,py),.11,fc=NAVY))
    save('b01-etats',f)
    graph('b01-rho','Volume (mL)','Masse (g)',[(np.array([0,10,20,30]),np.array([0,10,20,30]),'Eau : 1,00 g/mL',NAVY),(np.array([0,10,20,30]),np.array([0,27,54,81]),'Aluminium : 2,70 g/cm³',GREEN)],(0,32),(0,90))
    f,a=canvas()
    a.add_patch(Circle((3.5,2.7),1.65,fc=LIGHT,ec=NAVY,lw=1,alpha=.65))
    for j,(dx,dy) in enumerate([(-.22,.2),(.22,.2),(-.22,-.2),(.22,-.2),(0,.4),(0,-.4)]):a.add_patch(Circle((3.5+dx,2.7+dy),.18,fc=GREEN if j%2 else RED,ec='white'))
    for ang in [0,2.1,4.2]:
        x=3.5+1.35*np.cos(ang);y=2.7+1.35*np.sin(ang);a.add_patch(Circle((x,y),.12,fc=NAVY));text(a,x,y,'−','white',7)
    text(a,3.5,.45,'Nuage électronique (schématique)',NAVY,8)
    arrow(a,(5.1,2.8),(7.2,2.8),GREEN,'constituants',off=(0,.55))
    box(a,8,1.1,7.3,3.3,'Proton : charge positive\nNeutron : charge nulle\nÉlectron : charge négative',fill='white')
    text(a,11.65,.55,'Atome neutre : autant de protons que d’électrons',NAVY,8)
    save('b02-atome',f)
    f,a=canvas()
    for x,top,bot in [(1,'Atome Na','11 protons · 11 électrons'),(10,'Ion Na⁺','11 protons · 10 électrons')]:
        box(a,x,1.7,5,2,top);text(a,x+2.5,1,bot,NAVY,8)
    arrow(a,(6.3,2.7),(9.6,2.7),GREEN,'perte de 1 électron',off=(0,.65));text(a,8,4.7,'Le noyau conserve le même Z',NAVY,10);save('b02-ions',f)
    f,a=canvas()
    for j,(gas,obs) in enumerate([('CO₂','Eau de chaux\ntroublée'),('O₂','Bûchette\nravivée'),('H₂','Petite détonation\n(test encadré)'),('H₂O','Réactif anhydre\nqui bleuit')]):
        x=.25+j*4;box(a,x,2.8,3.5,1.2,gas);arrow(a,(x+1.75,2.6),(x+1.75,1.8),GREEN);text(a,x+1.75,1,obs,NAVY,8)
    save('b03-tests',f)
    f,a=canvas();molecule(a,1.5,3,'CH4');text(a,3,3,'+',NAVY,12);molecule(a,4.2,3,'O2');text(a,5.2,3,'+',NAVY,12);molecule(a,6.2,3,'O2');arrow(a,(7.4,3),(8.5,3),GREEN);molecule(a,10.2,3,'CO2');text(a,12.0,3,'+',NAVY,12);text(a,13.0,3,'2 ×',NAVY,10);molecule(a,14.4,3,'H2O');text(a,7.5,.8,'Un C · quatre H · quatre O avant et après',NAVY,9);save('b03-bilan',f)
    f,a=canvas();box(a,.5,1.5,3.4,2,'Cristal ionique\nNaCl');arrow(a,(4.2,2.5),(6.8,2.5),GREEN,'eau',off=(0,.5));box(a,7.2,.9,7.8,3.4,'',fill='#E4EEF8')
    for x,y,sym,col in [(8,3.4,'Na⁺',NAVY),(10.7,3.6,'Cl⁻',GREEN),(13.5,3.2,'Na⁺',NAVY),(8.7,1.6,'Cl⁻',GREEN),(11.3,1.8,'Na⁺',NAVY),(13.7,1.5,'Cl⁻',GREEN)]:
        a.add_patch(Circle((x,y),.44,fc='white',ec=col,lw=1.2));text(a,x,y,sym,col,8)
    text(a,11.1,4.75,'Ions dispersés dans la solution',NAVY,9);text(a,8,.35,'Même nombre de charges + et − dans ce modèle',MUTED,8);save('b04-solution',f)
    f,a=canvas();cmap=plt.get_cmap('RdYlBu')
    for p in range(15):a.add_patch(Rectangle((.5+p,2),1,.8,fc=cmap(p/14),ec='white'));text(a,1+p,1.5,str(p),INK,8)
    text(a,3.4,4.4,'Acide : H⁺ prédomine',RED,9);text(a,12.3,4.4,'Basique : OH⁻ prédomine',NAVY,9);text(a,8,3.45,'Neutre : pH 7',GREEN,9);text(a,8,.45,'Solutions aqueuses usuelles · vers 25 °C',MUTED,8);save('b04-ph',f)
    f,a=canvas()
    box(a,.4,2,3.2,1.7,'Zn + 2 H⁺');arrow(a,(4,2.8),(6.5,2.8),GREEN);box(a,7,2,3.6,1.7,'Zn²⁺ + H₂')
    text(a,13,3.2,'Avant : charge +2\nAprès : charge +2',NAVY,9);text(a,8,.9,'Atomes et charge totale conservés',NAVY,9);save('b05-reaction',f)
    f,a=canvas()
    for j,(title,cond,result) in enumerate([('A','Air sec','Pas de rouille'),('B','Eau + air','Rouille'),('C','Eau salée + air','Rouille'),('D','Eau désaérée\nsans O₂','Pas de rouille')]):
        x=.3+j*4;box(a,x,1.7,3.5,2.1,'',fill='white');text(a,x+1.75,4.6,title,NAVY,10);text(a,x+1.75,2.75,cond,NAVY,8);text(a,x+1.75,.8,result,GREEN if j in [0,3] else RED,8)
    save('b05-corrosion',f)
    f,a=canvas();box(a,5.5,2,5,1.5,'Balle (système)');box(a,.5,2,3,1.5,'Fil');box(a,12.3,2,3,1.5,'Terre');line(a,[(3.5,2.75),(5.5,2.75)]);line(a,[(10.5,2.75),(12.3,2.75)],ls='--');text(a,4.5,3.7,'contact',NAVY,8);text(a,11.4,3.7,'distance',NAVY,8);text(a,8,.7,'Le diagramme recense les interactions, pas leurs valeurs',MUTED,8);save('b09-doi',f)
    f,a=canvas()
    for x,label,g in [(2,'Terre','10 N/kg'),(10,'Lune','1,6 N/kg')]:
        a.add_patch(Circle((x+1.5,3),.20,fc=LIGHT,ec=NAVY));arrow(a,(x+1.5,3),(x+1.5,1 if x==2 else 2.68),GREEN)
        text(a,x+1.5,4.4,label,NAVY,10);text(a,x+1.5,.6,'g = '+g,NAVY,9);text(a,x+3.1,2.9,'m',NAVY,10)
    text(a,8,4.95,'Même masse · poids différents',NAVY,10);text(a,8,1,'P = mg',GREEN,11);save('b09-poids',f)
    f,a=canvas()
    a.add_patch(Circle((2.5,2.8),.7,fc=LIGHT,ec=NAVY));a.add_patch(Circle((13.5,2.8),.45,fc=LIGHT,ec=NAVY))
    arrow(a,(2.5,2.8),(5.1,2.8),GREEN);arrow(a,(13.5,2.8),(10.9,2.8),GREEN)
    text(a,2.5,4.2,'A · mA',NAVY,10);text(a,13.5,4.2,'B · mB',NAVY,10)
    line(a,[(2.5,1.2),(13.5,1.2)],MUTED,.8);text(a,8,1.65,'d : distance entre les centres',NAVY,9)
    text(a,8,4.6,'Même valeur · deux objets différents',NAVY,9);save('b10-forces',f)
    d=np.array([1,1.5,2,2.5,3,4]);graph('b10-distance','Distance / distance initiale','Force / force initiale',[(d,1/d**2,'Masses fixées',NAVY)],(0,4.2),(0,1.1))
    v=np.arange(0,11);graph('b11-ec','Vitesse (m/s)','Énergie cinétique (J)',[(v,.5*2*v**2,'Masse : 2 kg',NAVY)],(0,10.3),(0,110))
    f,a=canvas()
    for j,(top,ep,ec) in enumerate([('Départ',40,0),('En cours',15,25),('Niveau de référence',0,40)]):
        x=.3+j*5.3;box(a,x,1.6,4.6,2.2,f'Ep = {ep} J\nEc = {ec} J');text(a,x+2.3,4.5,top,NAVY,9)
    text(a,8,.55,'Sans frottement : Ep + Ec = 40 J',GREEN,10);save('b11-chute',f)
    f,a=canvas()
    for x,label,parallel in [(.7,'Série',False),(8.7,'Dérivation',True)]:
        wire(a,[(x,1),(x,4),(x+5.8,4),(x+5.8,1),(x,1)]);component(a,x,2.5,'','G',True);component(a,x+3,4,'L₁','L')
        if parallel:wire(a,[(x+1.4,4),(x+1.4,2),(x+5.8,2)]);component(a,x+3,2,'L₂','L')
        else:component(a,x+5.8,2.5,'L₂','L',True)
        text(a,x+2.8,.25,label,NAVY,9)
    save('b13-circuits',f)
    measure_circuit('b13-mesures');measure_circuit('b14-montage')
    cur=np.array([0,.01,.02,.03,.04,.05]);graph('b14-ohm','Intensité (A)','Tension (V)',[(cur,100*cur,'R = 100 Ω',NAVY)],(0,.052),(0,5.4))
    graph('bb01-velo','Temps (s)','Position (m)',[(np.array([0,10,20,30,40]),np.array([0,50,100,150,200]),'',NAVY)],(0,42),(0,210))
    f,a=canvas();wire(a,[(1.5,1),(1.5,4),(14,4),(14,1),(1.5,1)]);component(a,1.5,2.5,'12 V','G',True)
    wire(a,[(4,4),(4,2),(14,2)]);component(a,9,4,'L₁ · 0,30 A','L');component(a,9,2,'L₂ · 0,20 A','L');text(a,8,.4,'Interrupteurs fermés, représentés par leur fil de connexion',MUTED,8);save('bb03-refuge',f)
    f,a=canvas();box(a,.5,1.9,3.7,1.6,'Terre');box(a,11.8,1.9,3.7,1.6,'Lune');arrow(a,(4.5,3.5),(11.5,3.5),GREEN,'trajet simple',off=(0,.5));arrow(a,(11.5,1.8),(4.5,1.8),NAVY,'retour',off=(0,-.45));text(a,8,.35,'d = 3,84 × 10⁸ m · distances non à l’échelle',MUTED,8);save('bb04-radio',f)
    f,a=canvas();line(a,[(.5,4.6),(15.5,4.6)],MUTED,1);line(a,[(.5,.7),(15.5,.7)],NAVY,2);box(a,6,3.9,4,.65,'Sonar',fill=LIGHT)
    arrow(a,(7,3.8),(7,.85),GREEN,'aller',off=(-1,0));arrow(a,(9,.85),(9,3.8),NAVY,'retour',off=(1,0));text(a,13,2.5,'Durée totale\n0,080 s',NAVY,9);text(a,3,2.5,'Même trajet,\nflèches séparées\npour la lecture',MUTED,8);text(a,12,.3,'Fond',NAVY,8);save('bb06-sonar',f)
    f,a=canvas();cylinder(a,2,.5,1.1,'Avant immersion');cylinder(a,10,.5,2,'Après immersion');a.add_patch(Rectangle((10.4,.7),.8,.55,fc=MUTED,ec=NAVY));arrow(a,(5.5,2.4),(8.5,2.4),GREEN,'bloc : 54,0 g',off=(0,.55));text(a,8,.25,'Hausse du volume lu : 20,0 mL',NAVY,9);save('bb07-metaux',f)
    f,a=plt.subplots(figsize=(6.3,2.25));f.subplots_adjust(left=.13,right=.97,bottom=.25,top=.93)
    a.step([8,10,14,18],[0,200,0,0],where='post',color=NAVY,lw=1.7);a.set(xlabel='Heure de la journée (h)',ylabel='Puissance (W)',xticks=[8,10,12,14,16,18],yticks=[0,100,200],ylim=(-10,230));a.grid(color=LIGHT);save('bb08-solaire',f)
    f,a=canvas();a.add_patch(Circle((1.5,3),.65,fc='#E2B157',ec=NAVY));a.add_patch(Circle((8.5,2.5),.45,fc=LIGHT,ec=NAVY));box(a,12.5,1.8,3,1.4,'Observateur');arrow(a,(2.3,3),(7.9,2.55),GREEN,'lumière reçue',off=(0,.5));arrow(a,(9.1,2.5),(12.3,2.5),NAVY,'diffusion',off=(0,.5));text(a,1.5,4.5,'Étoile',NAVY,9);text(a,8.5,4.2,'Planète',NAVY,9);text(a,8,.6,'Schéma de principe · aucune taille ni distance à l’échelle',MUTED,8);save('bb09-etoile',f)
    cur=np.array([0,.005,.01,.015,.02,.025]);graph('bb10-ohm','Intensité (A)','Tension (V)',[(cur,200*cur,'Mesures compatibles avec le modèle',NAVY)],(0,.026),(0,5.4))
    from figures_brevet_exercices import produire as completer
    from revision_brevets import CORRIGES
    completer()
    from figures_annales import produire as produire_annales
    from annales_originales import figures_utilisees
    produire_annales()
    wanted={l[2] for c in charger() for l in c.lecons if l[2]}
    wanted|={e.figure for c in charger() for e in c.exercices+[c.defi] if e.figure}
    wanted|={p.exercice.figure for s in SUJETS for p in s.parties if p.exercice.figure}
    wanted|={e.figure_correction for c in charger() for e in c.exercices+[c.defi] if e.figure_correction}
    wanted|={fig for entry in CORRIGES.values() for fig,cap in entry.values()}
    wanted|=figures_utilisees()
    for p in OUT.glob('*.pdf'):
        assert p.resolve().is_relative_to(OUT.resolve())
        if p.stem not in wanted:p.unlink()
    assert len(list(OUT.glob('*.pdf')))==len(wanted) and all((OUT/(n+'.pdf')).exists() for n in wanted)
    (HERE/'build/figures.json').write_text(json.dumps(dict(nombre=len(wanted),figures=sorted(wanted)),ensure_ascii=False,indent=2),encoding='utf8')
    print(len(wanted),'figures finales, toutes utilisées.')
if __name__=='__main__':produire()
