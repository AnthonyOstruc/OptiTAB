"""Schémas et documents inédits des sujets 11 à 15 ; aucun visuel d'annale repris."""
from pathlib import Path
import json,math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle,Ellipse
from figures_revision import cv,tx,ln,ar,bx,save,plot,REGISTRY,N,G,R,M,L
from figures_electricite_exercices import circuit,symbol,switch

def boxes(name,labels,footer=''):
    f,a=cv(1.6)
    count=len(labels);w=14/count
    for i,s in enumerate(labels):bx(a,1+i*w,1.25,w-.4,1.8,s)
    if footer:tx(a,8,.48,footer,M,9)
    save(name,f)

def optics(name,correct=False):
    f,a=cv(1.8)
    bx(a,.6,1.8,2.8,1.3,'DEL');bx(a,11.6,.55,3.5,1.2,'Capteur')
    ln(a,[(3.5,2.45),(14.5,2.45)],N)
    for x,y in [(7,2.1),(8,2.45),(8.7,2.1),(7.7,1.9)]:a.add_patch(Circle((x,y),.11,fc=M,ec=M,zorder=5))
    tx(a,8,3.8,'Particules de fumée',size=10)
    tx(a,12.9,3.1,'Faisceau direct',M,9)
    if correct:
        ar(a,(3.5,2.45),(8,2.45),G)
        ar(a,(8,2.45),(12.5,1.75),G)
        tx(a,7.8,.6,'Lumière diffusée vers le capteur',G,9.1)
    else:tx(a,8,.25,'Ajouter les flèches de propagation sur la copie.',M,9)
    save(name,f)

def atom(name,label,p,n,e):
    # Inventaire symbolique, sans prétendre représenter des trajectoires électroniques.
    boxes(name,[f'Noyau\n{p} protons\n{n} neutrons',f'Autour du noyau\n{e} électrons'],label+' · inventaire, sans échelle')

def produire():
    plot('ann11-positions',[0,1,2,3],[0,.6,1.2,1.8],'Temps (s)','Altitude (m)',ylim=(0,2),xlim=(0,3.2))
    f,a=cv(1.8);a.add_patch(Circle((7.6,2.3),.05,fc=N,zorder=6));tx(a,8.2,2.3,'G')
    ar(a,(7.6,2.3),(7.6,4.0),G);ar(a,(7.6,2.3),(7.6,.6),N)
    tx(a,10.4,3.5,'Force du câble : 490 N',G,10);tx(a,10.4,1.0,'Poids : 490 N',N,10)
    tx(a,3.8,2.3,'Modèle ponctuel\nForces sans échelle',M,9.2);save('ann11-forces',f)
    boxes('ann11-autonomie',['1 cycle\n7,2 Wh','2 cycles\n14,4 Wh','3 cycles\n21,6 Wh'],'Réserve utilisable : 18 Wh · maximum : 2 cycles complets')
    boxes('ann11-pesees',['Récipient vide\n28,5 g','Avec 100,0 mL\nde liquide\n102,5 g'],'Même récipient · même balance · données de laboratoire')
    optics('ann12-optique');optics('ann12-optique-cor',True)
    boxes('ann12-molecules',['Propane\nC₃H₈','Dioxygène\nO₂','Dioxyde de\ncarbone · CO₂','Eau\nH₂O'],'Formules des espèces présentes dans l’équation du document')
    boxes('ann12-bilan',['Propane consommé\n+ dioxygène consommé','Dioxyde de carbone formé\n+ eau formée'],'Conservation : masse de tous les réactifs = masse de tous les produits')
    f,axes=plt.subplots(2,1,figsize=(6.2,2.0));f.subplots_adjust(left=.12,right=.96,bottom=.23,top=.83,hspace=.55)
    t=np.linspace(0,4,500)
    for ax,n,label in zip(axes,[2,4],['A','B']):
        ax.plot(t,np.sin(2*np.pi*n*t/4),color=N,lw=1.2);ax.set(xlim=(0,4),ylim=(-1.25,1.25),xticks=[0,1,2,3,4],yticks=[-1,0,1]);ax.grid(color=L);ax.text(-.07,.5,label,transform=ax.transAxes,ha='right',va='center',fontsize=10,color=N)
    axes[1].set_xlabel('Temps (ms)');axes[0].set_title('Même échelle verticale : signal (unité arbitraire)',fontsize=9.3,color=M)
    save('ann12-son',f)
    boxes('ann12-son-cor',['Trajet simple\n51 m','Vitesse\n340 m/s','Durée\n0,15 s'],'A : 2 oscillations en 4 ms · B : 4 oscillations en 4 ms, plus aigu')
    f,a=plt.subplots(figsize=(6.2,1.9));f.subplots_adjust(left=.17,right=.96,bottom=.28,top=.95)
    a.barh(['Diazote','Dioxygène','Autres gaz'],[78,21,1],color=[N,G,M]);a.set(xlim=(0,100),xlabel='Proportion en volume (%)',xticks=[0,20,40,60,80,100]);a.grid(axis='x',color=L);a.set_axisbelow(True)
    save('ann13-air',f)
    atom('ann13-atome','Atome neutre d’azote 14',7,7,7)
    plot('ann13-ohm',[0,10,20,30,40],[0,2,4,6,8],'Intensité (mA)','Tension (V)',ylim=(0,8.5),xlim=(0,42))
    circuit('ann13-mesures',resistor=True,ammeter=True,voltmeter=True,comment='Ampèremètre en série · voltmètre aux bornes de R')
    boxes('ann13-code',['11','10','00','01'],'Début → fin · un groupe par symbole · chaque valeur dure 2 ms')
    boxes('ann13-radio',['Station','120 km','Relais'],'Propagation d’un front : 0,40 ms · émission du message : 16 ms')
    plot('ann14-fusion',[0,2,4,6,8],[-4,0,0,0,4],'Temps (min)','Température (°C)',ylim=(-5,5),xlim=(0,8.4))
    def plateau(a):
        a.axvspan(2,6,color=G,alpha=.12);a.annotate('Fusion : 4 min',xy=(4,0),xytext=(4,2.5),ha='center',color=G,fontsize=10,arrowprops=dict(arrowstyle='->',color=G))
    plot('ann14-fusion-cor',[0,2,4,6,8],[-4,0,0,0,4],'Temps (min)','Température (°C)',annotate=plateau,ylim=(-5,5),xlim=(0,8.4))
    f,a=cv(1.7)
    for x,label,color in [(3.5,'Prélèvement\navant test','white'),(12,'Après ajout\ndu réactif',L)]:
        a.add_patch(Rectangle((x-1,1),2,2.0,fc=color,ec=N));tx(a,x,3.75,label,size=9.5)
    for x in np.linspace(11.3,12.7,8):a.add_patch(Circle((x,1.15),.08,fc='white',ec=M,zorder=5))
    ar(a,(5,2),(10.4,2),G);tx(a,8,2.8,'Nitrate d’argent',G,9.3);tx(a,12,.5,'Précipité blanc',M,9.5)
    save('ann14-test',f)
    # Le nombre de neutrons du chlore n'est pas fourni : ne pas inventer d'isotope.
    boxes('ann14-ion',['Noyau\n17 protons','Autour\n18 électrons'],'Charge : 17 − 18 = −1 · aucun isotope imposé')
    f,a=cv(1.6)
    ln(a,[(1,1.3),(15,1.3)],N,lw=2);bx(a,4,1.35,3,1.1,'Colis');ar(a,(8,2),(13.5,2),G)
    tx(a,11,2.8,'Sens du déplacement',G,9.5);tx(a,8,.55,'Masse : 2,0 kg · trajectoire rectiligne',M,9.5);save('ann14-convoyeur',f)
    boxes('ann14-energies',['0,50 m/s\n0,25 J','Vitesse × 2','1,0 m/s\n1,0 J'],'À masse fixée, l’énergie cinétique est multipliée par 4')
    f,a=cv(1.7)
    bx(a,1,1,5,2.3,'');bx(a,10.2,1.8,4.8,1.5,'Z = 2\nA = 4')
    for x,y in [(1.7,1.5),(3.9,2.7),(4.9,1.5),(2.6,2.2),(5.3,2.9),(3.2,1.3)]:a.add_patch(Circle((x,y),.13,fc=G,ec=G,zorder=5))
    tx(a,3.5,3.9,'Modèle du gaz');tx(a,8,.5,'Chaque point code un atome d’hélium · modèle sans échelle',M,9.2);save('ann15-helium',f)
    f,a=cv(1.7)
    original=[(.6,.5),(1.6,1.7),(2.7,.5),(.9,1.5),(2.2,1.2),(3.1,1.8)]
    for x0,w,label in [(1,5,'Avant'),(10,3,'Après compression')]:
        bx(a,x0,1,w,2.3,'')
        for x,y in original:a.add_patch(Circle((x0+.4+x*(w-.8)/3.7,1.1+y),.10,fc=G,ec=G,zorder=5))
        tx(a,x0+w/2,3.9,label,size=9.5)
    tx(a,8,.5,'Même nombre de points, même taille ; volume occupé plus petit.',M,9.2);save('ann15-compression',f)
    for correct,name in [(False,'ann15-forces-enonce'),(True,'ann15-forces-cor')]:
        f,a=cv(1.8)
        a.add_patch(Ellipse((6,2.5),4.5,1.6,fc=L,ec=N,zorder=3));tx(a,6,2.5,'Maquette',size=10)
        ln(a,[(6,1.7),(6,.5)],M);ln(a,[(4.5,.5),(7.5,.5)],N,lw=2)
        tx(a,3,1.1,'Fil ancré\nau sol',M,9)
        if correct:
            bx(a,10,.9,5,2.6,'Air : ↑ 3,4 N\nPoids : ↓ 3,0 N\nFil : ↓ 0,4 N')
            ar(a,(8,2.9),(8,4.1),G);ar(a,(8,2.9),(8,1.9),N);ar(a,(8.5,2.9),(8.5,2.35),R)
        else:tx(a,12,2.5,'Air : 3,4 N vers le haut\nPoids : à calculer',N,9.5)
        tx(a,8,.12,'Schéma sans échelle · les flèches de forces sont séparées pour la lecture.' if correct else 'Repères de la maquette et du fil · schéma sans échelle',M,8.8)
        save(name,f)
    # Circuit propre à ces données ; symboles de moteur et de lampe distincts.
    for opened,name in [(False,'ann15-circuit'),(True,'ann15-circuit-cor')]:
        f,a=cv(1.8);top,mid,bot=3.6,1.8,.55
        ln(a,[(2,bot),(2,top),(14,top),(14,bot),(2,bot)]);ln(a,[(5,top),(5,mid),(14,mid)])
        symbol(a,2,2.05,'G');tx(a,.75,2.1,'6,0 V',size=9);tx(a,1.4,2.8,'+',G);tx(a,1.4,1.3,'−',G)
        symbol(a,10,top,'M','Moteur','0,20 A');symbol(a,10,mid,'L','Éclairage','0,10 A' if not opened else '0 A')
        for x,y in [(5,top),(14,mid)]:a.add_patch(Circle((x,y),.06,fc=N,zorder=5))
        if opened:switch(a,7,mid,True,'Ouverture');ar(a,(6,top),(7.4,top),G)
        tx(a,8,.1,'Deux branches entre les mêmes nœuds' if not opened else 'La boucle du moteur reste fermée',M,9)
        save(name,f)
    data={k:v for k,v in REGISTRY.items() if k.startswith('ann')}
    (Path(__file__).resolve().parent/'build/figures-annales.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(len(data),'figures originales des sujets 11 à 15')

if __name__=='__main__':produire()
