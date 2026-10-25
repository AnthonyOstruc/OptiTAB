"""Rayons, trajets et signaux construits pour les données de chaque exercice."""
from figures_revision import *

def eye(a,x,y):
    a.add_patch(Polygon([(x-.45,y),(x,y+.28),(x+.45,y),(x,y-.28)],closed=True,fc='white',ec=N,lw=1.1,zorder=4));a.add_patch(Circle((x,y),.10,fc=N,zorder=5))
def echo(name,v,dt,unit='m',correct=False,dist=None,medium='air',retard=0,label='Paroi'):
    f,a=cv();bx(a,.4,1.3,3.7,1.7,'Émetteur /\nrécepteur');ln(a,[(14.1,.6),(14.1,3.7)],M,2)
    ar(a,(4.5,3.15),(13.7,3.15),label=f'Aller : d = {fr(dist)} {unit}' if correct else 'aller : d',off=(0,.45))
    ar(a,(13.7,1.15),(4.5,1.15),c=N,label=f'Retour : d = {fr(dist)} {unit}' if correct else 'retour : d',off=(0,-.45))
    tx(a,14.7,2.2,label,M,9.3,ha='left',rotation=90)
    txt=f'Δt total = {fr(dt)} s'
    if retard:txt=f'Δt corrigé = {fr(dt+retard)} − {fr(retard)} = {fr(dt)} s'
    tx(a,8,4.25,txt,N,10)
    tx(a,8,.12,f'{medium} · v = {fr(v)} {unit}/s'+(f' · trajet total : {fr(2*dist)} {unit}' if correct else ''),G if correct else M,9.3)
    save(name,f,dict(vitesse=v,duree=dt,unite=unit,distance=dist,retard=retard,aller_retour=True))
def fr(v):
    if v is None:return '?'
    if float(v).is_integer() and abs(v)>=1000:return f'{v:,.0f}'.replace(',',' ')
    return f'{v:g}'.replace('.',',')

def produire():
    for correct in [False,True]:
        f,a=cv();a.add_patch(Circle((1.5,3.25),.25,fc=Y,ec=N));bx(a,5.5,1.6,1.1,1.3,'',fill='#E8EFE3');eye(a,13.2,2.2);ar(a,(1.9,3.1),(5.3,2.5),label='lumière reçue',off=(0,.5))
        if correct:ar(a,(6.8,2.2),(12.6,2.2),label='lumière diffusée vers l’œil',off=(0,.5))
        else:ln(a,[(6.8,2.2),(12.6,2.2)],M)
        tx(a,1.5,4.0,'Lampe',size=9.5);tx(a,6.1,.8,'Feuille',size=9.5);tx(a,13.2,1.2,'Œil',size=9.5);save('cor-vision' if correct else 'ex-vision',f)
    f,a=cv();source=(1.1,2.2);xobj=5;half=.6;screen=13.5;hs=half*(screen-source[0])/(xobj-source[0]);a.add_patch(Circle(source,.08,fc=Y));ln(a,[(xobj,2.2-half),(xobj,2.2+half)],N,3);ln(a,[(screen,.15),(screen,4.3)],M,2)
    a.add_patch(Polygon([(xobj,2.2-half),(screen,2.2-hs),(screen,2.2+hs),(xobj,2.2+half)],fc=L,ec='none',zorder=1))
    for sg in [-1,1]:ar(a,source,(screen,2.2+sg*hs),c=N)
    tx(a,1.3,.6,'Source\nponctuelle',size=9);tx(a,5,.6,'Objet opaque',size=9);tx(a,10,2.2,'Zone d’ombre',size=10);tx(a,14,4.05,'Écran',M,9,ha='left');save('cor-ombre',f)
    for correct in [False,True]:
        f,a=cv();source=(1,2.2);a.add_patch(Circle(source,.08,fc=Y));ln(a,[(5,1.7),(5,2.7)],N,3);tx(a,5,.7,'Objet fixe',size=9.5)
        for x,label in [(10,'Écran proche'),(14,'Écran éloigné')]:ln(a,[(x,.4),(x,4.0)],M,1.5);tx(a,x,4.3,label,size=9.1)
        if correct:
            for sg in [-1,1]:ar(a,source,(14,2.2+sg*.5*13/4),c=N)
            for x in [10,14]:ln(a,[(x,2.2-.5*(x-1)/4),(x,2.2+.5*(x-1)/4)],G,3)
            tx(a,8,.15,'La section de l’ombre augmente avec l’éloignement',G,9.4)
        save('cor-ecrans' if correct else 'ex-ecrans',f)
    f,a=cv();ln(a,[(.7,3),(15.2,3)],N,1.5);bx(a,.3,2.55,1.5,.9,'Source');eye(a,9,.8)
    for x in [5,7,9,11,13]:a.add_patch(Circle((x,3),.055,fc=Y,zorder=4))
    ar(a,(7,3),(8.7,1.2),label='lumière diffusée',off=(2.2,.1));tx(a,6,4,'Trajet vu grâce aux particules diffusantes',size=10);tx(a,12,.8,'Œil de côté',size=9.5);save('cor-diffusion',f)
    echo('cor-lune-trajets',300000,2.56,'km',True,384000,'vide',label='Lune')
    for name,v,dt,unit,d,medium,label in [
        ('echo-lumineux',300000,.004,'km',600,'vide','Réflecteur'),
        ('echo-sonore',340,.50,'m',85,'air','Paroi'),
        ('sonar',1500,.20,'m',150,'eau','Fond')]:
        echo('ex-'+name,v,dt,unit,False,None,medium,label=label)
        echo('cor-'+name,v,dt,unit,True,d,medium,label=label)
    echo('cor-miroir-spatial',300000,2.4,'km',True,360000,'vide',label='Réflecteur')
    echo('cor-echo-030',340,.3,'m',True,51)
    echo('cor-echo-retard',340,.2,'m',True,34,retard=.01)
    echo('cor-echo-060',340,.6,'m',True,102)
    echo('cor-echo-0080',340,.08,'m',True,13.6)
    f,a=cv()
    for y,medium,v,d in [(2.65,'Air',340,17),(.7,'Eau',1500,75)]:
        bx(a,.5,y,5.3,1.2,f'{medium} : {v} m/s');ar(a,(6.1,y+.6),(9.2,y+.6),label='0,10 s',off=(0,.35));bx(a,9.6,y,5.9,1.2,f'd = {d} m')
    tx(a,8,4.3,'Même durée d’aller-retour · deux vitesses différentes',size=10);save('cor-deux-milieux',f,dict(air=dict(v=340,d=17),eau=dict(v=1500,d=75),duree=.1))
    for correct in [False,True]:
        t=np.linspace(0,.025,1501);f,a=plt.subplots(figsize=(6.2,2));f.subplots_adjust(left=.10,right=.95,bottom=.26,top=.95)
        a.plot(t*1000,np.sin(2*np.pi*400*t),color=N,lw=1.3);a.set(xlabel='Temps (ms)',ylabel='Signal',xlim=(0,25),ylim=(-1.65,1.65),yticks=[],xticks=[0,5,10,15,20,25]);a.grid(color=L)
        if correct:
            a.plot([0,0,2.5,2.5],[1.1,1.3,1.3,1.1],color=G,lw=1);tx(a,1.25,1.5,'1 motif',G,9);tx(a,14,-1.4,'10 motifs en 25 ms',G,10)
        save('cor-dix-motifs' if correct else 'ex-dix-motifs',f,dict(frequence_Hz=400,motifs=10,duree_s=.025))
    for correct in [False,True]:
        t=np.linspace(0,.020,1201);f,a=plt.subplots(figsize=(6.2,2.0));f.subplots_adjust(left=.10,right=.98,bottom=.26,top=.96);a.plot(t*1000,np.sin(2*np.pi*400*t),color=N,lw=1.3);a.set(xlabel='Temps (ms)',ylabel='Signal',xlim=(0,20),ylim=(-1.65,1.65),yticks=[]);a.grid(color=L)
        if correct:
            a.plot([0,0,2.5,2.5],[1.1,1.3,1.3,1.1],color=G,lw=1);tx(a,1.25,1.5,'1 motif',G,9);tx(a,11.5,-1.4,'8 motifs en 20 ms',G,10)
        save('cor-huit-motifs' if correct else 'ex-huit-motifs',f,dict(frequence_Hz=400,motifs=8,duree_s=.02))
        t=np.linspace(0,.008,801);f,a=plt.subplots(figsize=(6.2,2.0));f.subplots_adjust(left=.10,right=.98,bottom=.26,top=.95)
        for amp,col,label in [(1,N,'A'),(.45,G,'B')]:a.plot(t*1000,amp*np.sin(2*np.pi*500*t),color=col,label=label,lw=1.3)
        a.set(xlabel='Temps (ms)',ylabel='Signal · même échelle',xlim=(0,8),ylim=(-1.5,1.75),yticks=[-1,0,1]);a.grid(color=L);a.legend(loc='lower right',fontsize=9)
        if correct:a.plot([.5,.5,2.5,2.5],[1.1,1.3,1.3,1.1],color=G,lw=1);tx(a,1.5,1.55,'Même T : 2 ms',G,9.5)
        save('cor-meme-periode' if correct else 'ex-meme-periode',f,dict(frequences_Hz=[500,500],amplitudes=[1,.45],periode_s=.002))
    for name,marker in [('ex-etalonnage',None),('cor-etalonnage',(20,.9)),('cor-etalonnage-lecture',(40,1.3))]:
        def mark(a,point=marker):
            if point:
                x,y=point;a.plot([0,x,x],[y,y,0],'--',color=G,lw=1);a.plot([x],[y],'o',color=G);note(a,f'{fr(x)} °C ; {fr(y)} V',point,(5,1.5))
        plot(name,[0,10,20,30,40,50],[.5,.7,.9,1.1,1.3,1.5],'Température (°C)','Tension (V)',annotate=mark,ylim=(0,1.75),xlim=(0,55))
    for correct in [False,True]:
        f,a=plt.subplots(figsize=(6.2,2.0));f.subplots_adjust(left=.12,right=.98,bottom=.26,top=.94);a.axvspan(0,50,color='#E5F1E4');a.plot([0,10,20,30,40,50],[.5,.7,.9,1.1,1.3,1.5],'o-',color=N,lw=1.5);a.plot([50,150],[1.5,3.5],'--',color=R,lw=1.3);a.set(xlabel='Température (°C)',ylabel='Tension (V)',xlim=(0,155),ylim=(0,4));a.grid(color=L)
        tx(a,25,2.5,'Domaine\nétalonné',G,9.5)
        if correct:a.plot([125],[3],'x',color=R,ms=7);note(a,'Calcul : 125 °C, hors plage',(125,3),(52,3.65))
        save('cor-hors-plage' if correct else 'ex-hors-plage',f,dict(domaine_C=[0,50],calcul_C=125,tension_V=3))
    f,axs=plt.subplots(1,2,figsize=(6.2,2.0));f.subplots_adjust(left=.08,right=.98,bottom=.27,top=.82,wspace=.3)
    x=np.linspace(0,4,300);y=1+.7*np.sin(x*1.6);axs[0].plot(x,y,color=N);xs=np.arange(0,4.01,.5);ys=np.round((1+.7*np.sin(xs*1.6))/.5)*.5;axs[1].step(xs,ys,where='mid',color=G);axs[1].plot(xs,ys,'o',color=G,ms=3)
    for ax,title in zip(axs,['Signal continu','Valeurs prélevées et arrondies']):ax.set(title=title,xlabel='Temps (unité)',ylim=(0,2));ax.grid(color=L);ax.title.set_fontsize(9.5)
    save('cor-analogique-numerique',f,dict(pas_temporel=.5,pas_arrondi=.5))
    f,a=plt.subplots(figsize=(6.2,2.0));f.subplots_adjust(left=.16,right=.95,bottom=.27,top=.92);a.step([0,3,4,5,6],[1,0,0,1,0],where='post',color=N,lw=1.6);a.set(xlabel='Temps (s)',yticks=[0,1],yticklabels=['Éteinte','Allumée'],xlim=(0,6.15),ylim=(-.25,1.65));a.grid(color=L)
    for x,lab in [(1.5,'Début : 3 s'),(3.5,'Séparation'),(4.5,'0'),(5.5,'1')]:tx(a,x,1.4,lab,N,9)
    a.axvspan(4,6,color='#E5F1E4',alpha=.65);tx(a,5,-.14,'Message : 2 s',G,9);save('cor-protocole-phare',f,dict(debut_s=3,separation_s=1,bits='01',duree_bit_s=1,duree_message_s=2))
