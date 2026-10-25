"""Documents vectoriels originaux pour les exercices de Cinquième."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch

ROOT=Path(__file__).resolve().parent
DEST=ROOT/'template-terminale/figures'
N='#203e77'; G='#19896d'; R='#c8573b'; M='#596676'; B='#eef4fa'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9.5,'pdf.fonttype':42})

def canvas(h=1.65):
    f,a=plt.subplots(figsize=(6.0,h));f.subplots_adjust(0,0,1,1)
    a.set(xlim=(0,15),ylim=(0,4.1));a.axis('off');return f,a
def tx(a,x,y,s,c=N,**kw):return a.text(x,y,s,ha='center',va='center',color=c,**kw)
def ln(a,p,q,c=N,**kw):a.plot([p[0],q[0]],[p[1],q[1]],color=c,lw=kw.pop('lw',1.15),**kw)
def ar(a,p,q,c=G):a.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=10,lw=1.3,color=c))
def box(a,x,y,w,h,s,c=N):
    a.add_patch(Rectangle((x,y),w,h,facecolor=B,edgecolor=c,lw=1));tx(a,x+w/2,y+h/2,s,c)

def circuit(a,mode):
    # Deux nœuds de dérivation ; aucun trait ne traverse le symbole de pile.
    ln(a,(2,1),(13,1));ln(a,(13,1),(13,3));ln(a,(2,1),(2,1.8));ln(a,(2,2.2),(2,3));ln(a,(2,3),(13,3))
    ln(a,(1.6,2.2),(2.4,2.2));ln(a,(1.76,1.8),(2.24,1.8));tx(a,1.2,2.3,'+');tx(a,1.2,1.6,'−')
    def lamp(x,y,label):
        a.add_patch(Circle((x,y),.24,facecolor='white',edgecolor=N,zorder=4))
        ln(a,(x-.16,y-.16),(x+.16,y+.16),zorder=5);ln(a,(x-.16,y+.16),(x+.16,y-.16),zorder=5);tx(a,x,y+.58,label)
    def switch(x,y):
        ln(a,(x-.35,y),(x+.35,y),'white',lw=4)
        ln(a,(x-.35,y),(x+.28,y+.35))
        a.plot([x-.35,x+.35],[y,y],'o',ms=3,mfc='white',mec=N,zorder=6)
        tx(a,x,y+.65,'K')
    parallel=mode in ['branche-commande','commande-commune','court-circuit']
    if parallel:
        ln(a,(4,3),(4,2));ln(a,(4,2),(13,2));lamp(9,3,'L₁');lamp(9,2,'L₂')
        a.plot([4,13],[3,2],'o',color=N,ms=4)
    else:lamp(9,3,'L')
    if mode in ['commande','serie-ouverte']:switch(6,3)
    if mode=='serie-ouverte':lamp(12,3,'L₂');tx(a,9,.38,'Une seule boucle, interrompue.',M)
    if mode=='branche-commande':switch(6,3);tx(a,8,.38,'K agit uniquement sur la branche de L₁.',M)
    if mode=='commande-commune':switch(3,3);tx(a,8,.38,'K coupe le fil commun aux deux lampes.',M)
    if mode=='court-circuit':
        ln(a,(6,3),(6,1),R,lw=2);tx(a,7.5,.35,'Montage dangereux à analyser sur papier uniquement.',R,fontsize=8.4)
    if mode=='commande':tx(a,8,.38,'Pile, lampe et interrupteur en série.',M)

def make(name):
    f,a=canvas()
    if name=='air-100':
        rng=np.random.default_rng(52);codes=np.array([0]*78+[1]*21+[2]);rng.shuffle(codes)
        for k,value in enumerate(codes):
            a.plot(1+(k%20)*.67,1+(k//20)*.4,'o',color=[N,G,R][value],ms=4)
        tx(a,7.5,3.6,'100 jetons mélangés · proportions arrondies')
        tx(a,7.5,.35,'78 diazote (bleu) · 21 dioxygène (vert) · 1 autres gaz (orange)',M,fontsize=8.5)
    elif name.startswith('air-'):
        box(a,2,1,11,2,'')
        codes=np.array([0]*16+[1]*4);np.random.default_rng(42).shuffle(codes)
        for j in range(4):
            for i in range(5):
                color=N if name=='air-faux' or codes[j*5+i]==0 else G
                a.plot(3+i*2,1.4+j*.4,'o',color=color,ms=5)
        tx(a,7.5,3.6,'Modèle à discuter' if name=='air-faux' else 'Modèle approché des deux gaz principaux')
        tx(a,7.5,.45,'Une seule sorte de points' if name=='air-faux' else 'Bleu : diazote (~80 %) · vert : dioxygène (~20 %)',M,fontsize=8.5)
    elif name in ['dissolution','filtration-sel','separation','stockage','chaine-incomplete','promenade','moyenne']:
        data={
         'dissolution':(['Solide ajouté\n22 g','Dissous\n18 g','Dépôt\n4 g'],'Solution : 50 g d’eau + 18 g dissous = 68 g'),
         'filtration-sel':(['Eau + sel\ndissous','Filtre','Filtrat : eau\n+ sel dissous'],'Le sel dissous n’est pas retenu par le filtre.'),
         'separation':(['Eau salée\n+ sable','Filtration','Évaporation\ndu filtrat'],'Filtre : sable retenu · Après évaporation du filtrat : sel récupéré'),
         'stockage':(['Entrée\n50 J','Sortie\n35 J','Stockage\n15 J'],'50 J = 35 J + 15 J · même durée d’étude'),
         'chaine-incomplete':(['Pile','→','Mouvement'],'Chaîne proposée par l’élève : à compléter.'),
         'promenade':(['Marche\n45 min','Arrêt\n15 min','Sortie\n60 min'],'Distance totale : 3 km · durée totale : 1 h'),
         'moyenne':(['Étape 1\n1 h · 10 km','Étape 2\n2 h · 8 km','Total\n3 h · 18 km'],'Vitesse moyenne : 18 km ÷ 3 h = 6 km/h'),
        }
        labels,foot=data[name]
        for i,s in enumerate(labels):box(a,.6+i*5,1.25,3.8,1.5,s)
        if name in ['filtration-sel','separation']:
            ar(a,(4.45,2),(5.5,2));ar(a,(9.45,2),(10.5,2))
        tx(a,7.5,.48,foot,M,fontsize=8.8)
    elif name=='test-eau':
        box(a,1.3,1,4.5,2,'Poudre anhydre\nblanche')
        box(a,9.2,1,4.5,2,'Après contact\navec le liquide',G)
        a.add_patch(Rectangle((10,1.2),2.8,.35,facecolor='#45a4dc',edgecolor=N));ar(a,(6.1,2),(8.9,2))
        tx(a,7.5,.4,'Observation : la poudre devient bleue.',M)
    elif name=='ballon':
        a.add_patch(Rectangle((6.6,.8),1.8,1.5,facecolor=B,edgecolor=N));a.add_patch(Circle((7.5,2.95),.64,facecolor='#d9f1e8',edgecolor=G))
        ln(a,(7.2,2.3),(7.2,2.5));ln(a,(7.8,2.3),(7.8,2.5));tx(a,3.1,2.9,'Ballon souple\nqui recueille le gaz');ar(a,(4.8,2.9),(6.8,2.9));tx(a,11.7,1.6,'Récipient et ballon :\nensemble pesé fermé')
        tx(a,7.5,.3,'Expérience encadrée · montage adapté fourni par le professeur',M,fontsize=8.4)
    elif name=='distances':
        ar(a,(1,2),(14,2),N)
        for x,label in [(2,'Soleil'),(8,'Terre'),(11.12,'Mars')]:
            a.plot(x,2,'o',color=G,ms=5);tx(a,x,2.65,label)
        tx(a,5,1.4,'3 cm');tx(a,6.56,.7,'4,56 cm');tx(a,7.5,3.6,'Longueurs calculées sur la maquette')
        tx(a,7.5,.2,'Schéma explicatif sans échelle : ne pas mesurer sur ce dessin.',M,fontsize=8.5)
    elif name in ['sens','positions','accelere']:
        rows=[(2.5,[2,4,6,8,10,12])]
        if name=='sens':
            ar(a,(2,2.8),(12,2.8));ar(a,(12,1.5),(2,1.5));tx(a,7.5,3.6,'Même droite, sens opposés')
        else:
            xs=[2,3,4.5,6.5,9,12] if name=='accelere' else [2,4,6,8,10,12]
            a.plot(xs,[2]*len(xs),'o-',color=N,ms=6);ar(a,(2,3),(12,3));tx(a,7.5,.8,'Positions relevées toutes les 0,5 s · sens vers la droite',M,fontsize=8.7)
    elif name in ['livre-interactions','balle-interactions','main-avant','main-apres']:
        center='Balle' if name=='balle-interactions' else 'Livre'
        left='Air' if center=='Balle' else 'Table'
        box(a,5.5,1.5,4,1.1,center,G);box(a,.3,1.5,3.2,1.1,left);box(a,11.5,1.5,3.2,1.1,'Terre')
        ln(a,(3.5,2.05),(5.5,2.05));ln(a,(9.5,2.05),(11.5,2.05),ls='--')
        if name=='main-avant':box(a,5.5,3,4,.8,'Main');ln(a,(7.5,2.6),(7.5,3))
        tx(a,7.5,.5,'Trait plein : contact · pointillés : interaction à distance',M,fontsize=8.5)
    elif name=='bilan-branche-ouverte':
        circuit(a,'branche-commande');a.texts[-1].remove()
        a.plot([2.7,3.3],[3,3],'o',ms=3,mfc='white',mec=N,zorder=6);tx(a,3,3.65,'Kg',fontsize=8)
        tx(a,8,.38,'Kg fermé : L₂ conserve sa boucle ; K est ouvert dans la branche de L₁.',M,fontsize=8)
    elif name=='trois-commandes':
        circuit(a,'commande-commune')
        a.texts[-1].remove()
        # Commandes fermées de branche, distinctes de la commande générale ouverte.
        for y,label in [(3,'K₁'),(2,'K₂')]:
            a.plot([5.7,6.3],[y,y],'o',ms=3,mfc='white',mec=N,zorder=6);tx(a,6,y+.4,label,fontsize=8)
        tx(a,8,.38,'K général et deux commandes de branche.',M)
    elif name in ['commande','serie-ouverte','branche-commande','commande-commune','court-circuit']:
        circuit(a,name)
    elif name=='equivalents':
        for x in [1,8]:
            for p,q in [((x,1),(x+5,1)),((x+5,1),(x+5,2.8)),((x+5,2.8),(x,2.8)),((x,1),(x,1.7)),((x,2.1),(x,2.8))]:ln(a,p,q)
            ln(a,(x-.4,2.1),(x+.4,2.1));ln(a,(x-.23,1.7),(x+.23,1.7));tx(a,x-.55,2.5,'+')
            cx,cy=(x+2.5,2.8) if x==1 else (x+5,1.9)
            a.add_patch(Circle((cx,cy),.25,facecolor='white',edgecolor=N,zorder=3));ln(a,(cx-.16,cy-.16),(cx+.16,cy+.16),zorder=4);ln(a,(cx-.16,cy+.16),(cx+.16,cy-.16),zorder=4)
            tx(a,x+2.5,3.6,'Circuit A' if x==1 else 'Circuit B')
        tx(a,7.5,.35,'Comparer les composants et leurs connexions.',M,fontsize=8.7)
    elif name=='jonctions':
        for x in [4,11]:ln(a,(x-2,2),(x+2,2));ln(a,(x,.9),(x,3.3))
        a.plot(4,2,'o',color=N,ms=7)
        ln(a,(10.65,2),(11.35,2),'white',lw=5)
        th=np.linspace(0,np.pi,60);a.plot(11+.35*np.cos(th),2+.35*np.sin(th),color=N,lw=1.2)
        tx(a,4,.35,'Jonction : fils connectés',M,fontsize=8.8);tx(a,11,.35,'Pont : fils sans contact',M,fontsize=8.8)
    elif name=='deux-obstacles':
        for row,where,label in [(2.9,4.5,'A : éclairage bloqué'),(1.2,10.5,'B : regard masqué')]:
            for x,s in [(1.5,'Source'),(7.5,'Objet'),(13.5,'Œil')]:box(a,x-1.1,row-.32,2.2,.64,s)
            ar(a,(2.7,row),(4.4 if where==4.5 else 6.3,row))
            if where==10.5:ar(a,(8.7,row),(10.4,row))
            ln(a,(where,row-.55),(where,row+.55),R,lw=3)
            tx(a,7.5,row+.7,label,fontsize=8.8)
        tx(a,7.5,.25,'Un écran opaque interrompt un trajet ; on teste les deux positions séparément.',M,fontsize=8)
    elif name.startswith('vision'):
        for x,s in [(1.5,'Source'),(7.5,'Objet'),(13.5,'Œil')]:box(a,x-1.1,1.3,2.2,1.4,s)
        if name=='vision-fausse':ar(a,(12.3,2),(8.7,2),R)
        else:
            ar(a,(2.7,2),(6.3,2))
            if name=='vision-masquee':
                ar(a,(8.7,2),(10.4,2));ln(a,(10.5,1),(10.5,3),R,lw=4)
        tx(a,7.5,.4,'Dessin proposé : à corriger.' if name=='vision-fausse' else 'Écran opaque : le trajet objet–œil est interrompu.',M,fontsize=8.4)
    elif name=='ombre-fausse':
        a.plot(1.5,2,'o',color=R);a.add_patch(Rectangle((7,1.1),1,1.8,facecolor=N));ln(a,(13,1),(13,3));ar(a,(1.7,2),(12.8,2),R)
        tx(a,1.5,3,'S');tx(a,7.5,3.5,'Objet opaque');tx(a,13,3.5,'Écran');tx(a,7.5,.4,'Construction proposée par l’élève : à discuter.',M)
    elif name=='ombres-comparaison':
        for offset,d,label in [(0,2.8,'Avant'),(7.5,1.5,'Objet rapproché de S')]:
            sx=offset+.7;ox=sx+d;screen=sx+6;cy=2.1
            a.plot(sx,cy,'o',color=R,ms=4);tx(a,sx,cy-.45,'S',fontsize=8)
            a.add_patch(Rectangle((ox-.035,cy-.3),.07,.6,facecolor=N))
            extent=.3*6/d
            for sign in [-1,1]:ln(a,(sx,cy),(screen,cy+sign*extent),R)
            ln(a,(screen,.7),(screen,3.5),M);ln(a,(screen,cy-extent),(screen,cy+extent),G,lw=3)
            tx(a,offset+3.6,3.8,label,fontsize=8.8)
        tx(a,7.5,.25,'Même source ponctuelle, même objet, même écran · schémas sans échelle',M,fontsize=8.4)
    elif name.startswith('echo-'):
        d=int(name.split('-')[1])
        box(a,.5,1,3.3,2,'Émetteur /\nrécepteur');ln(a,(13,.8),(13,3.3),N,lw=3)
        ar(a,(4,2.6),(12.7,2.6));ar(a,(12.7,1.4),(4,1.4));tx(a,8.3,3.3,f'Aller : {d} m');tx(a,8.3,.65,f'Retour : {d} m');tx(a,13,3.8,'Obstacle')
    elif name=='traces-durees':
        for x,d in [(1,1),(8,2)]:
            t=np.linspace(0,d,300);a.plot(x+5*t/d,2+.6*np.sin(4*np.pi*t/d),color=G)
            ln(a,(x,1),(x+5,1));tx(a,x, .6,'0');tx(a,x+5,.6,f'{d} s');tx(a,x+2.5,3.4,'Deux oscillations')
    elif name.startswith('code-'):
        seq={'code-lecture':'10110010','code-dab':'001001','code-baca':'01101110'}[name]
        for i,s in enumerate(seq):box(a,1+i*1.6,1.3,1.4,1.5,s)
        tx(a,7.5,3.5,{'code-lecture':'10 | 11 | 00 | 10','code-dab':'D : 00   |   A : 10   |   B : 01','code-baca':'B : 01 | A : 10 | C : 11 | A : 10'}[name])
        tx(a,7.5,.5,'Début → fin · un état par intervalle',M)
    elif name=='soleil-signal':
        box(a,.8,1.4,3,1.3,'Soleil');box(a,11.2,1.4,3,1.3,'Terre');ar(a,(4,2),(11,2));tx(a,7.5,3.3,'150 000 000 km');tx(a,7.5,.6,'500 s = 8 min 20 s · modèle de distance moyenne',M,fontsize=8.7)
    elif name=='cour-solaire':
        ln(a,(1,2),(14,2))
        for d,label,lx,y in [(0,'Soleil',1,3.1),(1.5,'Terre',2,1),(2.28,'Mars',4.1,3.1),(7.8,'Jupiter',6,1),(45,'Neptune',13.5,3.1)]:
            x=1+13*d/45;a.plot(x,2,'o',color=G);ln(a,(x,2),(lx,y-.4 if y>2 else y+.4),M);tx(a,lx,y,label+'\n'+str(d).replace('.',',')+' m',fontsize=8)
        tx(a,7.5,.25,'Repères dans la cour · dessins des astres et longueurs réduits.',M,fontsize=8.5)
    elif name=='trois-interactions':
        for i,(title,contact) in enumerate([('Tenu','Main'),('En chute','Air'),('Posé','Sol')]):
            x=.25+i*5
            box(a,x+1.1,1.7,2.8,.8,'Ballon',G);box(a,x+1.1,2.95,2.8,.7,contact);ln(a,(x+2.5,2.5),(x+2.5,2.95))
            box(a,x+1.1,.25,2.8,.7,'Terre');ln(a,(x+2.5,.95),(x+2.5,1.7),ls='--');tx(a,x+.45,2.1,title,rotation=90,fontsize=8.3)
    else:raise ValueError(name)
    return f,a

def produire():
    from revision_exercices import ILLUSTRATIONS,DEFIS_CORRIGES,BILANS_CORRIGES
    DEST.mkdir(parents=True,exist_ok=True)
    specs=[s for pair in ILLUSTRATIONS.values() for s in pair]+list(DEFIS_CORRIGES.values())+list(BILANS_CORRIGES.values())
    names=sorted({s[1] for s in specs if s and s[0]=='revision'})
    for name in names:
        f,a=make(name);f.canvas.draw();renderer=f.canvas.get_renderer()
        for obj in a.texts:
            bb=obj.get_window_extent(renderer)
            assert bb.x0>=-1 and bb.y0>=-1 and bb.x1<=f.bbox.width+1 and bb.y1<=f.bbox.height+1,(name,obj.get_text(),bb)
        f.savefig(DEST/('revision-'+name+'.pdf'),metadata={'Title':'OptiTAB · '+name,'Author':'OptiTAB'});plt.close(f)
    return names

if __name__=='__main__':print(json.dumps(produire(),ensure_ascii=False))
