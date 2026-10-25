"""Connexions électriques cohérentes entre énoncés et solutions."""
from figures_revision import *

def symbol(a,x,y,kind='L',label='',value='',r=.28):
    a.add_patch(Circle((x,y),r+.06,fc='white',ec='none',zorder=3))
    if kind=='R':a.add_patch(Rectangle((x-.5,y-.23),1,.46,fc='white',ec=N,lw=1.2,zorder=4))
    else:
        a.add_patch(Circle((x,y),r,fc='white',ec=N,lw=1.2,zorder=4))
        if kind=='L':
            a.plot([x-.18,x+.18],[y-.18,y+.18],color=N,lw=1.2,zorder=6)
            a.plot([x-.18,x+.18],[y+.18,y-.18],color=N,lw=1.2,zorder=6)
        else:tx(a,x,y,kind,N,9.5)
    if label or value:tx(a,x,y+.55,' · '.join(p for p in [label,value] if p),N,9.5)
def switch(a,x,y,opened=False,label='K'):
    a.add_patch(Rectangle((x-.47,y-.15),.94,.7,fc='white',ec='none',zorder=3))
    for xx in [x-.38,x+.38]:a.add_patch(Circle((xx,y),.045,fc=N,zorder=5))
    a.plot([x-.6,x-.38],[y,y],color=N,lw=1.3,zorder=5)
    a.plot([x+.38,x+.6],[y,y],color=N,lw=1.3,zorder=5)
    a.plot([x-.38,x+.38],[y,y+.4 if opened else y],color=N,lw=1.3,zorder=5)
    tx(a,x,y-.50,label,N,9)
def circuit(name,parallel=False,two=False,source='',switches=(),opened=(),currents=None,volts=None,ammeter=False,voltmeter=False,inverseA=False,inverseV=False,short=False,wire_open=False,same_node=False,resistor=False,branch_ammeter=False,comment=''):
    f,a=cv();top,bot,mid=3.6,.55,1.8
    ln(a,[(2,bot),(2,top),(14,top),(14,bot),(2,bot)])
    symbol(a,2,2.075,'G');tx(a,1.35,2.65,'+',G,12);tx(a,1.35,1.5,'−',G,12)
    if source:tx(a,.7,2.05,source,N,9.3)
    if parallel:
        ln(a,[(5,top),(5,mid),(14,mid)])
        for xx in [5,14]:a.add_patch(Circle((xx,top),.055,fc=N,zorder=5))
        symbol(a,10,top,'L','L₁',volts[0] if volts else '')
        symbol(a,10,mid,'L','' if voltmeter else 'L₂','' if voltmeter else volts[1] if volts else '')
        if voltmeter:tx(a,10,mid-.55,'L₂'+(' · '+volts[1] if volts else ''),N,9.3)
        if 'L1' in switches:switch(a,7.0,top,'L1' in opened,'K₁')
        if 'L2' in switches:switch(a,7.0,mid,'L2' in opened,'K₂')
        if 'G' in switches:switch(a,3.7,top,'G' in opened,'Kcommun')
        if branch_ammeter:
            symbol(a,7,mid,'A');tx(a,6.4,mid-.55,'A',G,9);tx(a,7.7,mid-.55,'COM',G,9)
        if currents:
            for y,x,value,branch in [(top,3.6,currents[0],'G'),(top,7.0,currents[1],'L1'),(mid,7.0,currents[2],'L2')]:
                if branch_ammeter and branch=='L2':x=12
                if branch in opened:
                    tx(a,12.1,y-.55,value,G,9.5)
                else:
                    ar(a,(x-.45,y),(x+.4,y),G)
                    tx(a,x,y+(.6 if x<5 else -.55),value,G,9.5)
    else:
        symbol(a,9,top,'R' if resistor else 'L','R' if resistor else 'L₁' if two else 'L',volts[0] if volts else '')
        if two:symbol(a,14,2.05,'L');tx(a,13.35,2.05,'L₂'+(' · '+volts[1] if volts else ''),N,9.2,ha='right')
        if 'G' in switches:switch(a,5.0,top,'G' in opened)
        if ammeter or inverseA:
            symbol(a,5.2,top,'A');tx(a,4.65,2.95,'COM' if inverseA else 'A',G,9);tx(a,5.9,2.95,'A' if inverseA else 'COM',G,9)
            if inverseA:tx(a,5.2,2.15,'Affichage : −0,15 A',R,9.5)
        if currents:
            ar(a,(3.1,top),(4.1,top));tx(a,3.6,4.2,currents[0],G,9.5)
            if len(currents)>1:ar(a,(12,bot),(11,bot));tx(a,11.5,1.1,currents[1],G,9.5)
    if voltmeter:
        if same_node:left,right,center,yy=3.4,6.4,4.9,2.0
        elif parallel:left,right,center,yy=8.5,11.5,10,2.6
        else:left,right,center,yy=7.1,10.9,9,1.95
        ln(a,[(left,top),(left,yy),(right,yy),(right,top)]);symbol(a,center,yy,'V')
        tx(a,center-.62,yy-.55,'COM' if inverseV else 'V',G,9);tx(a,center+.75,yy-.55,'V' if inverseV else 'COM',G,9)
        if same_node:
            ln(a,[(left,top),(right,top)],G,2);tx(a,4.9,4.22,'Même nœud',G,9.5)
    if short:
        ln(a,[(7.1,top),(7.1,2.0),(10.9,2.0),(10.9,top)],R,1.7);tx(a,9,1.45,'Fil ajouté',R,9.5)
    if wire_open:switch(a,3.7,top,True,'Fil commun coupé')
    if comment:tx(a,8,.12,comment,R if 'pas réaliser' in comment else G,9.1)
    save(name,f,dict(parallele=parallel,source=source,courants=currents,tensions=volts,interrupteurs=list(switches),ouverts=list(opened),amperemetre=ammeter,voltmetre=voltmeter))

def paired(name,mode='equivalent',correct=False,voltage=9):
    f,a=cv()
    ln(a,[(1,.7),(1,3.5),(7,3.5),(7,.7),(1,.7)])
    symbol(a,1,2.1,'G',r=.25);tx(a,.45,2.8,'+',G,10);tx(a,.45,1.45,'−',G,10)
    symbol(a,4,3.5,'L',r=.25);tx(a,4,3.94,'L₁'+(f' · {3 if voltage==9 else 6} V' if mode!='equivalent' else ''),size=9.3)
    symbol(a,7,2.1,'L',r=.25);tx(a,6.35,2.1,'L₂'+(' : 6 V' if mode!='equivalent' else ''),N,9,ha='right')
    tx(a,4,.15,'A · série incompatible' if mode!='equivalent' and voltage==6 else 'A · série' if mode!='equivalent' else 'A',R if voltage==6 and mode!='equivalent' else N,9.3)
    if mode=='equivalent':
        ln(a,[(9.1,.7),(9.1,3.5),(15.2,3.5),(15.2,.7),(9.1,.7)])
        symbol(a,12.1,.7,'G',r=.25);tx(a,11.35,1.1,'+',G,10);tx(a,12.85,1.1,'−',G,10);symbol(a,9.1,2.1,'L',r=.25);tx(a,9.8,2.1,'L₁',N,9,ha='left');symbol(a,12.1,3.5,'L','L₂',r=.25);tx(a,12.1,2.5,'Même succession\nde dipôles' if correct else 'B',G if correct else N,9.3)
    else:
        ln(a,[(9.3,.7),(9.3,3.5),(15.2,3.5),(15.2,.7),(9.3,.7)]);ln(a,[(10.2,3.5),(10.2,1.8),(15.2,1.8)])
        symbol(a,9.3,2.1,'G',r=.25);tx(a,8.75,2.8,'+',G,10);tx(a,8.75,1.45,'−',G,10);symbol(a,12.8,3.5,'L',r=.25);tx(a,12.8,3.94,f'L₁ · {voltage} V',size=9.3);symbol(a,12.8,1.8,'L','L₂',f'{voltage} V',r=.25);tx(a,12.2,.15,'B · dérivation')
        tx(a,4,4.35,f'Source : {voltage} V',size=9.4);tx(a,12.2,4.35,f'Source : {voltage} V',size=9.4)
    save(name,f,dict(mode=mode,source=voltage))

def node(name,ins,outs):
    f,a=cv();center=(8,2.3);a.add_patch(Circle(center,.10,fc=N,zorder=5))
    for p,val in ins:
        ln(a,[p,center]);ar(a,p,center);tx(a,p[0]+1,p[1]+.35,val,G,10)
    for p,val in outs:
        ln(a,[center,p]);ar(a,center,p);tx(a,p[0]-1,p[1]+.35,val,G,10)
    save(name,f,dict(entrees=[v for p,v in ins],sorties=[v for p,v in outs]))

def ohmmetre():
    f,a=cv();symbol(a,8,2.9,'R','Résistance isolée');bx(a,6.5,.45,3,1.2,'Ω',fill='white')
    ln(a,[(6.5,1.05),(4.5,1.05),(4.5,2.9),(7.5,2.9)])
    ln(a,[(9.5,1.05),(11.5,1.05),(11.5,2.9),(8.5,2.9)])
    tx(a,8,4.1,'Aucune alimentation connectée');tx(a,8,.13,'Autres branches déconnectées',M,9);save('cor-ohmmetre',f)

def produire():
    circuit('ex-circuit-ouvert',switches=('G',),opened=('G',))
    circuit('cor-circuit-ouvert',switches=('G',),opened=('G',),comment='Unique boucle ouverte : pas de courant permanent')
    circuit('cor-sens-courant',currents=['I : de + vers −','I vers la borne −'])
    circuit('ex-circuit-serie',two=True,switches=('G',))
    circuit('cor-serie-ouverte',two=True,switches=('G',),opened=('G',),comment='L’ouverture interrompt les deux lampes')
    circuit('ex-circuit-parallele',parallel=True)
    circuit('cor-branches',parallel=True,comment='Trois branches entre les deux nœuds : G, L₁ et L₂')
    circuit('cor-commandes',parallel=True,switches=('G','L1'),comment='K₁ : L₁ seulement · Kcommun : les deux lampes')
    circuit('cor-refuge',parallel=True,switches=('L2',),comment='L₁ directe · L₂ commandée par K₂')
    circuit('cor-commandes-independantes',parallel=True,switches=('L1','L2'),comment='K₁ et K₂ commandent chacun leur lampe')
    circuit('cor-branche-ouverte',parallel=True,switches=('L1',),opened=('L1',),comment='L₁ ouverte · L₂ garde un trajet fermé vers G')
    paired('ex-circuits-equivalents');paired('cor-circuits-equivalents',correct=True)
    circuit('ex-lampe-court-circuitee',short=True,comment='Montage à ne pas réaliser')
    circuit('cor-lampe-court-circuitee',short=True,comment='L₁ contournée par le fil : risque de surintensité')
    circuit('cor-fil-commun',parallel=True,wire_open=True,comment='La coupure commune interrompt les deux trajets')
    circuit('cor-courants-paralleles',parallel=True,currents=['I_G','I₁','I₂'])
    circuit('cor-amperemetre',ammeter=True,currents=['I'])
    circuit('cor-serie-012',currents=['0,12 A','0,12 A'])
    node('ex-noeud',[((1,3.5),'0,10 A'),((1,1.0),'0,20 A')],[((15,2.3),'I ?')])
    node('cor-noeud',[((1,3.5),'0,10 A'),((1,1.0),'0,20 A')],[((15,2.3),'0,30 A')])
    circuit('ex-courants-050',parallel=True,currents=['0,50 A','0,18 A','I₂ ?'])
    circuit('cor-courants-050',parallel=True,currents=['0,50 A','0,18 A','0,32 A'])
    circuit('cor-amperemetre-inverse',inverseA=True,currents=['Sens de I'])
    f,a=cv();ln(a,[(2,.7),(2,3.5),(13.5,3.5),(13.5,.7),(2,.7)]);symbol(a,2,2.1,'G');tx(a,1.4,2.8,'+',G,11);tx(a,1.4,1.4,'−',G,11);symbol(a,9,3.5,'A');tx(a,8,1.8,'Aucun récepteur limitant le courant',R,10);tx(a,8,.15,'Montage incorrect : ne pas réaliser ce branchement',R,9.5);save('ex-amperemetre-danger',f)
    circuit('cor-courant-branche-ouverte',parallel=True,switches=('L2',),opened=('L2',),currents=['I_G = I₁','I₁','I₂ = 0 A'])
    for cor in [False,True]:
        node(('cor' if cor else 'ex')+'-trois-courants',[((1,2.3),'0,80 A')],[((15,3.7),'0,220 A' if cor else '220 mA'),((15,2.3),'0,35 A'),((15,.9),'0,23 A' if cor else 'I₃ ?')])
    circuit('ex-bilan-intensites',parallel=True,currents=['0,40 A','260 mA','0,24 A'])
    circuit('cor-bilan-intensites',parallel=True,currents=['Attendu : 0,50 A','0,260 A','0,24 A'],comment='Le relevé principal de 0,40 A est à vérifier, avec le protocole')
    circuit('cor-voltmetre',voltmeter=True)
    f,a=cv();ln(a,[(4,1.0),(4,3.5),(7,3.5)]);ln(a,[(4,1.0),(7,1.0)]);symbol(a,4,2.1,'G');tx(a,3.4,2.8,'+',G,11);tx(a,3.4,1.4,'−',G,11)
    for p in [(7,3.5),(7,1)]:a.add_patch(Circle(p,.06,fc=N))
    ar(a,(9,1.1),(9,3.4),label='U peut être non nulle',off=(2.2,0));tx(a,8,.35,'Pas de branche de récepteur fermée : courant extérieur nul',G,9.5);save('cor-pile-isolee',f)
    circuit('ex-tensions-45',parallel=True,source='4,5 V')
    circuit('cor-tensions-45',parallel=True,source='4,5 V',volts=['4,5 V','4,5 V'])
    circuit('ex-tensions-serie',two=True,source='9 V',volts=['4 V','U₂ ?'])
    circuit('cor-tensions-serie',two=True,source='9 V',volts=['4 V','5 V'])
    circuit('cor-voltmetre-inverse',voltmeter=True,inverseV=True,comment='Pointes inversées : affichage −3,0 V au lieu de +3,0 V')
    f,a=cv();ln(a,[(2,.6),(2,3.6),(14,3.6),(14,.6),(2,.6)]);symbol(a,2,2.1,'G');symbol(a,10,3.6,'L','L');switch(a,5,3.6,label='K fermé');ln(a,[(3.8,3.6),(3.8,1.8),(6.2,1.8),(6.2,3.6)]);symbol(a,5,1.8,'V');tx(a,5,1.15,'0 V',G);ar(a,(11.5,3.6),(12.6,3.6),label='I possible');save('cor-interrupteur-ferme',f)
    circuit('cor-tensions-18-42',two=True,source='6 V',volts=['1,8 V','4,2 V'])
    circuit('ex-voltmetre-meme-noeud',voltmeter=True,same_node=True)
    circuit('cor-voltmetre-meme-noeud',voltmeter=True,same_node=True,comment='Différence de potentiel du même nœud : environ 0 V')
    paired('cor-serie-derivation-6V',mode='serie-parallele',correct=True,voltage=6)
    paired('cor-serie-derivation-9V',mode='serie-parallele',correct=True,voltage=9)
    circuit('cor-voltmetre-6V',parallel=True,source='6 V',voltmeter=True,volts=['6 V','6 V'])
    circuit('cor-montage-150',resistor=True,source='6 V',ammeter=True,voltmeter=True,volts=['150 Ω'],currents=['0,040 A'])
    circuit('cor-circuit-evaluation',parallel=True,source='6 V',currents=['0,30 A','0,12 A','0,18 A'])
    circuit('cor-amperemetre-branche',parallel=True,branch_ammeter=True,currents=['0,50 A','0,18 A','0,32 A'],comment='A mesure I₂ en série dans la branche L₂')
    ohmmetre()
    for cor in [False,True]:
        f,a=plt.subplots(figsize=(6.2,2));f.subplots_adjust(left=.13,right=.95,bottom=.26,top=.93)
        a.set(xlabel='Intensité I',ylabel='Tension U',xlim=(0,1.1),ylim=(0,1.1),xticks=[0],yticks=[])
        if cor:
            a.plot([0,1],[0,1],color=N,lw=1.5);note(a,'Droite passant par l’origine',(.45,.45),(.12,.93))
        save(('cor' if cor else 'ex')+'-ohm-modele',f,dict(modele_qualitatif=True))
        plot(('cor' if cor else 'ex')+'-ohm-150',[.01,.02,.03],[1.5,3,4.5],'Intensité (A)','Tension (V)',other=[([0,.04],[0,6],'Modèle et prévision : 6 V à 0,040 A',G)] if cor else None,ylim=(0,7),xlim=(0,.045))
        plot(('cor' if cor else 'ex')+'-lampe-courbe',[0,.05,.1,.15,.2],[0,.5,1.5,3,5],'Intensité (A)','Tension (V)',annotate=(lambda a:note(a,'U/I n’est pas constant',(.15,3),(.012,4.2))) if cor else None,ylim=(0,5.5))
        def suspect(a):
            a.plot([.03],[5],'x',color=R,ms=8,mew=1.5);tx(a,.03,5.6,'Relevé : 5 V',R,9.5)
            if cor:note(a,'Modèle : 3 V',(.03,3),(.007,4.3))
        plot(('cor' if cor else 'ex')+'-ohm-point-suspect',[0,.01,.02,.03],[0,1,2,3],'Intensité (A)','Tension (V)',annotate=suspect,ylim=(0,6.2),xlim=(0,.04))
        plot(('cor' if cor else 'ex')+'-ohm-boite',[.01,.02,.03],[2,4,6],'Intensité (A)','Tension (V)',annotate=(lambda a:note(a,'5 V → 0,025 A',(.025,5),(.001,5.8))) if cor else None,ylim=(0,7),xlim=(0,.035))
