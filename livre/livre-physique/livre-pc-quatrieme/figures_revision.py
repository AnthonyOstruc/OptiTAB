"""Schémas des exercices et corrections : tracés vectoriels, données explicites."""
from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle,Polygon,FancyArrowPatch
from matplotlib.ticker import FuncFormatter,ScalarFormatter
HERE=Path(__file__).resolve().parent;OUT=HERE/'figures'
N='#1B3C8E';G='#3B8544';R='#B94343';M='#667085';L='#E5EAF3';Y='#C69B42'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':N,'text.color':N,'axes.edgecolor':M,'xtick.color':M,'ytick.color':M})
REGISTRY={}
def cv(height=1.8):
    f,a=plt.subplots(figsize=(6.2,height));f.subplots_adjust(left=.01,right=.99,bottom=.03,top=.97)
    a.set(xlim=(0,16),ylim=(0,4.5));a.axis('off');return f,a
def tx(a,x,y,s,c=N,size=10,ha='center',va='center',**kw):
    a.text(x,y,s,fontsize=size,color=c,ha=ha,va=va,zorder=8,**kw)
def ln(a,pts,c=N,lw=1.3,**kw):a.plot(*zip(*pts),color=c,lw=lw,zorder=2,**kw)
def ar(a,p,q,c=G,label='',off=(0,.35)):
    a.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=11,lw=1.3,color=c,zorder=5))
    if label:tx(a,(p[0]+q[0])/2+off[0],(p[1]+q[1])/2+off[1],label,c,9.5,bbox=dict(facecolor='white',edgecolor='none',pad=.3))
def bx(a,x,y,w,h,s='',fill=L,c=N):
    a.add_patch(Rectangle((x,y),w,h,fc=fill,ec=c,lw=1.1,zorder=3));tx(a,x+w/2,y+h/2,s,size=9.7)
def save(name,f,data=None):
    assert name not in REGISTRY,name
    for ax in f.axes:
        if ax.axison:
            fmt=FuncFormatter(lambda x,pos:f'{x:g}'.replace('.',','))
            for axis in [ax.xaxis,ax.yaxis]:
                if isinstance(axis.get_major_formatter(),ScalarFormatter):axis.set_major_formatter(fmt)
    dest=OUT/(name+'.pdf');f.savefig(dest,metadata={'Title':'OptiTAB - '+name,'Author':'OptiTAB'})
    # Examiner ce qui est réellement écrit dans le PDF ; les ticks Matplotlib
    # préparés hors des limites ne sont pas tous dessinés.
    import fitz
    pdf=fitz.open(dest);page=pdf[0];outside=[]
    for b in page.get_text('dict')['blocks']:
        for line in b.get('lines',[]):
            for span in line['spans']:
                rect=fitz.Rect(span['bbox'])
                if rect.x0<-.7 or rect.y0<-.7 or rect.x1>page.rect.width+.7 or rect.y1>page.rect.height+.7:outside.append(dict(texte=span['text'],bbox=[round(v,1) for v in rect]))
    pdf.close()
    REGISTRY[name]=dict(data or {},textes_hors_cadre=outside);plt.close(f)
def plot(name,x,y,xlabel,ylabel,other=None,annotate=None,ylim=None,xlim=None):
    f,a=plt.subplots(figsize=(6.2,2.0));f.subplots_adjust(left=.13,right=.95,bottom=.26,top=.94)
    a.plot(x,y,'o-',color=N,lw=1.5,ms=3.5)
    if other:
        for xx,yy,label,col in other:a.plot(xx,yy,'o-',color=col,label=label,lw=1.3,ms=3)
        a.legend(fontsize=9,framealpha=.94,loc='best')
    a.set(xlabel=xlabel,ylabel=ylabel)
    if ylim:a.set_ylim(ylim)
    if xlim:a.set_xlim(xlim)
    a.grid(color=L);a.set_axisbelow(True)
    if annotate:annotate(a)
    save(name,f,dict(x=list(map(float,x)),y=list(map(float,y))))
def note(a,s,xy,xytext):
    a.annotate(s,xy=xy,xytext=xytext,color=G,fontsize=9.4,arrowprops=dict(arrowstyle='->',color=G,lw=1),bbox=dict(fc='white',ec='none',pad=1))

def mol(a,x,y,s,k=1):
    atoms={'H2O':[(-.6,0,'H'),(0,.45,'O'),(.6,0,'H')], 'CO':[(-.45,0,'C'),(.45,0,'O')], 'CO2':[(-.8,0,'O'),(0,0,'C'),(.8,0,'O')], 'O2':[(-.4,0,'O'),(.4,0,'O')], 'N2':[(-.4,0,'N'),(.4,0,'N')], 'H2':[(-.4,0,'H'),(.4,0,'H')], 'CH4':[(0,0,'C'),(-.7,0,'H'),(.7,0,'H'),(0,.7,'H'),(0,-.7,'H')]}
    d=atoms[s];pairs=[(0,1),(1,2)] if s in ['H2O','CO2'] else [(0,j) for j in range(1,len(d))]
    for i,j in pairs:ln(a,[(x+d[i][0]*k,y+d[i][1]*k),(x+d[j][0]*k,y+d[j][1]*k)],M)
    colors={'H':'white','O':'#CE5F5F','C':'#596071','N':'#5979B3'}
    for dx,dy,atom in d:
        a.add_patch(Circle((x+dx*k,y+dy*k),.29*k,fc=colors[atom],ec=M,lw=.9,zorder=4));tx(a,x+dx*k,y+dy*k,atom,c=N if atom=='H' else 'white',size=9)

def matiere():
    for corr in [False,True]:
        f,a=cv()
        for x,v,solid in [(2.5,42,False),(11,57,True)]:
            ln(a,[(x,3.65),(x,.7),(x+2,.7),(x+2,3.65)])
            a.add_patch(Rectangle((x+.03,.73),1.94,v/60*2.7,fc='#DDEBF7',ec='none',zorder=1))
            for val in [20,40,60]:
                yy=.7+val/60*2.7;ln(a,[(x+1.55,yy),(x+2,yy)],M,.7);tx(a,x+2.2,yy,str(val),M,9,ha='left')
            if solid:a.add_patch(Polygon([(x+.4,.85),(x+1.2,.9),(x+1.4,1.5),(x+.6,1.7)],fc='#AEB8CB',ec=N,zorder=3))
            tx(a,x+1,4.1,f'{v} mL')
        ar(a,(6.5,2.3),(9.8,2.3),label='immersion')
        if corr:tx(a,8,.25,'Vsolide = 57 − 42 = 15 mL',G)
        save(('cor' if corr else 'ex')+'-immersion',f,dict(Vi=42,Vf=57,Vsolide=15))
        plot(('cor' if corr else 'ex')+'-rho-points',[10,20,30],[9,18,27],'Volume (mL)','Masse (g)',other=[([0,30],[0,27],'Modèle proportionnel',G)] if corr else None,annotate=(lambda a:note(a,'ρ = 0,90 g/mL',(20,18),(4,24))) if corr else None,ylim=(0,32),xlim=(0,35))
        plot(('cor' if corr else 'ex')+'-tare-graphe',[0,10,20,30],[20,29,38,47],'Volume (mL)','Masse pesée (g)',other=[([0,10,20,30],[0,9,18,27],'Après soustraction de 20 g',G)] if corr else None,annotate=(lambda a:note(a,'Masse du récipient : 20 g',(0,20),(4,10))) if corr else None,ylim=(0,55))
    f,a=cv();ln(a,[(1.5,3.9),(1.5,.7),(6,.7),(6,3.9)]);a.add_patch(Rectangle((1.52,.72),4.46,2.1,fc='#DDEBF7',ec='none'));bx(a,2.5,1.1,1.5,1.0,'solide',fill='#C5CBDA');a.add_patch(Circle((4.1,1.8),.24,fc='white',ec=N,zorder=4));ar(a,(8,2.8),(4.3,1.95),label='bulle',off=(.8,.6));tx(a,10.9,1.2,'V apparent trop grand\nρ calculée trop petite',G);save('cor-bulle',f)
    f,a=cv();bx(a,1.3,.8,5.3,2.9,'',fill='#AEB8CB');bx(a,2.1,1.4,3.7,1.6,'cavité',fill='white');tx(a,4,4.0,'Une coque en métal');ar(a,(10,3),(6.2,3),label='métal',off=(.4,.5));tx(a,11,1.2,'Volume extérieur\n= métal + cavité',G);save('cor-coque',f)
    for kind,vi,vf in [('compression',60,40),('detente',20,40)]:
        for corr in [False,True]:
            f,a=cv();widths=[4.4,4.4*vf/vi] if kind=='compression' else [3,6]
            for j,(x,v,w) in enumerate(zip([1,9],[vi,vf],widths)):
                bx(a,x,1,w,2.2,'',fill='white');ln(a,[(x+w,.8),(x+w,3.4)],G,2)
                tx(a,x+w/2,3.9,f'{v} mL')
                if j==0 or corr or kind=='compression':
                    for z in range(12):
                        px=x+.35+(z%4)*(w-.7)/3;py=1.4+(z//4)*.65;a.add_patch(Circle((px,py),.08,fc=N,zorder=4))
                elif not corr:tx(a,x+w/2,2.1,'À compléter',M)
            if corr:tx(a,8,.25,'Même nombre de particules · aucune fuite',G)
            save(('cor' if corr else 'ex')+'-'+kind,f,dict(avant=vi,apres=vf,particules=12))
    f,a=cv();bx(a,3,.8,10,2.8,'',fill='white')
    for i in range(20):a.add_patch(Circle((3.4+i*.45,1.05),.08,fc=N,zorder=4))
    tx(a,8,4.1,'Modèle proposé par l’élève');save('ex-air-incorrect',f)
    f,a=cv();bx(a,1.2,.7,10.5,3,'',fill='white');rng=np.random.default_rng(4015)
    for j in range(100):
        px=1.55+(j%10)*1.0+rng.uniform(-.12,.12);py=1.0+(j//10)*.26+rng.uniform(-.05,.05)
        a.add_patch(Circle((px,py),.055,fc=N if j<78 else R if j<99 else G,zorder=4))
        if j%16==0:ar(a,(px,py),(px+.3,py+.15),c=M)
    tx(a,13.7,3.4,'Diazote',N,9.5);tx(a,13.7,2.6,'Dioxygène',R,9.5);tx(a,13.7,1.8,'Autres gaz',G,9.5);tx(a,8,4.1,'Gaz réparti dans tout le volume · mouvements schématisés');save('cor-air',f)
    for corr in [False,True]:
        plot(('cor' if corr else 'ex')+'-fusion',list(range(7)),[-10,-5,0,0,0,5,10],'Temps (min)','Température (°C)',annotate=(lambda a:note(a,'Solide + liquide',(3,0),(.3,8))) if corr else None,ylim=(-12,14))
        plot(('cor' if corr else 'ex')+'-ebullition',list(range(9)),[20,40,60,80,100,100,100,100,100],'Temps (min)','Température (°C)',annotate=(lambda a:note(a,'Vaporisation',(6,100),(4.4,60))) if corr else None,ylim=(0,115))
        plot(('cor' if corr else 'ex')+'-deux-courbes',list(range(9)),[20,40,60,80,80,80,80,80,95],'Temps (min)','Température (°C)',other=[(list(range(9)),[20,40,60,70,75,80,85,90,100],'B : changement sur une plage',G)],annotate=(lambda a:note(a,'A : palier',(5,80),(.2,95))) if corr else (lambda a:tx(a,6.5,75,'A',N,10)),ylim=(0,115))
    f,a=cv();ln(a,[(.5,1.3),(15.5,1.3)],N,2);bx(a,1.5,1.1,3.5,1.2,'glace flottante',fill='#DDEBF7');a.add_patch(Polygon([(9,1.3),(12,3.8),(15.3,1.3)],fc='#D3D9E3',ec=N));bx(a,11.4,3.0,1.2,.6,'glace',fill='white');ar(a,(12,2.8),(9,1.5),label='eau ajoutée',off=(.5,.3));tx(a,4,3.5,'Banquise');tx(a,12,4.2,'Glacier continental');save('cor-glaces',f)
    for corr in [False,True]:
        f,a=cv()
        for idx,x in enumerate([1.0,9.3]):
            bx(a,x,.7,5.3,2.8,'',fill='white');tx(a,x+2.65,4.0,'Avant' if idx==0 else 'Après chauffage')
            for j in range(12):
                px=x+.6+(j%4)*1.25;py=1.1+(j//4)*.8
                a.add_patch(Circle((px,py),.09 if corr or idx==0 else .20,fc=N,zorder=4))
                if corr and idx:ar(a,(px+.1,py),(px+.45,py+.15),c=G)
        if corr:tx(a,8,.2,'Entités conservées · agitation accrue représentée qualitativement',G,9.5)
        save('cor-particules-chaudes' if corr else 'ex-particules-grosses',f)
    f,a=cv();ln(a,[(6,3.7),(6,.6),(10,.6),(10,3.7)]);a.add_patch(Rectangle((6.02,.62),3.96,1.3,fc='#DDEBF7',ec='none'));a.add_patch(Rectangle((6.02,1.92),3.96,1.2,fc='#F0D69D',ec='none'));tx(a,8,1.25,'Eau');tx(a,8,2.5,'Huile');tx(a,8,4.1,'Après repos : deux phases');save('ex-eau-huile',f)
    f,a=cv();bx(a,.4,1.4,3.4,1.7,'Eau + sable\n+ sel dissous');ar(a,(4.1,2.3),(5.5,2.3));a.add_patch(Polygon([(5.7,3.3),(8.9,3.3),(7.3,1.5)],fc='white',ec=N));ln(a,[(7.3,1.5),(7.3,.8)]);tx(a,7.3,3.9,'Filtre : sable retenu',size=9.5)
    for x,y in [(6.6,3.05),(7.4,2.9),(8,3.05)]:a.add_patch(Circle((x,y),.1,fc=Y,zorder=4))
    ar(a,(9.2,2.3),(10.7,2.3));bx(a,11,1.2,4.5,2,'Filtrat : eau\n+ sel dissous',fill='#DDEBF7');save('cor-filtration',f)
    f,a=cv();a.add_patch(Circle((2.7,2),.85,fc='#DDEBF7',ec=N));ln(a,[(2.4,2.7),(2.4,3.5),(6,3.5),(6,2.9),(11.3,2.0)]);ln(a,[(2.95,2.7),(2.95,3.15),(5.7,3.15),(5.7,2.55),(11.1,1.65)]);bx(a,6.2,2.0,3.8,.85,'refroidissement',fill='#E5F1E4');ln(a,[(11.1,1.65),(11.8,1.4)]);ln(a,[(11.4,1.7),(11.4,.4),(14.2,.4),(14.2,1.7)]);tx(a,12.8,1,'eau recueillie',size=9);tx(a,2.7,.55,'Sel non volatil',size=9);tx(a,2.7,3.95,'Vapeur d’eau',size=9.5);ar(a,(4,3.35),(5.3,3.35));tx(a,7.8,.35,'Vaporiser puis liquéfier',M,9.2);save('cor-distillation',f)
    f,a=cv();bx(a,5.6,.6,4.8,3.4,'',fill='white');tx(a,6.1,3.5,'13',M,10,ha='left');tx(a,8,2.6,'Al',N,22);tx(a,8,1.25,'Aluminium',size=12);save('ex-case-aluminium',f)
    for corr in [False,True]:
        f,a=cv()
        for j in range(6):mol(a,2+(j%3)*6,3.2-(j//3)*1.6,'O2' if j<4 else 'N2',.95)
        if corr:tx(a,8,.15,'4 O₂ → 8 O          2 N₂ → 4 N',G)
        save(('cor' if corr else 'ex')+'-melange-molecules',f)
        f,a=cv();mol(a,8,2.3,'H2O',1.7)
        if corr:tx(a,8,.45,'H₂O : deux H et un O',G,11)
        save('cor-eau-formule' if corr else 'ex-eau-modele',f)
        f,a=cv();tx(a,3.7,4.1,'A : deux molécules d’eau');tx(a,12.2,4.1,'B : deux H₂ et une O₂');mol(a,2,2.6,'H2O');mol(a,5.6,2.6,'H2O');mol(a,9.3,2.6,'H2');mol(a,12,2.6,'H2');mol(a,14.6,2.6,'O2');ln(a,[(7.7,.9),(7.7,3.7)],L)
        if corr:tx(a,8,.35,'A et B : 4 H et 2 O · espèces et assemblages différents',G,10)
        save(('cor' if corr else 'ex')+'-inventaires',f)
    f,a=cv()
    for x in [1.6,4.7,7.8,10.9,14]:mol(a,x,2.6,'CH4',.85)
    tx(a,8,4.1,'Cinq modèles complets de CH₄');a.add_patch(Circle((3,.55),.25,fc='#596071',ec=M,zorder=4));tx(a,3,.55,'C','white',9);tx(a,8,.55,'Un C restant · aucun H restant',G);save('cor-methane-jetons',f)
    f,a=cv();mol(a,1.2,2.5,'H2',1.1);tx(a,2.6,2.5,'+',size=13);mol(a,4,2.5,'H2',1.1);tx(a,5.5,2.5,'+',size=13);mol(a,6.8,2.5,'O2',1.1);ar(a,(8,2.5),(9.3,2.5));mol(a,11.1,2.5,'H2O',1.1);tx(a,12.7,2.5,'+',size=13);mol(a,14.3,2.5,'H2O',1.1);tx(a,8,.4,'Avant : 4 H et 2 O       Après : 4 H et 2 O',G);save('cor-reaction-eau',f)
    f,a=cv();mol(a,1.5,2.6,'CH4',1.0);tx(a,3,2.6,'+',size=13);tx(a,4.0,2.6,'2 ×');mol(a,5.6,2.6,'O2',1.05);ar(a,(7.2,2.6),(8.4,2.6));mol(a,10,2.6,'CO2',1.0);tx(a,11.8,2.6,'+',size=13);tx(a,12.7,2.6,'2 ×');mol(a,14.3,2.6,'H2O',1.0);tx(a,8,.4,'Un C · quatre H · quatre O de chaque côté',G);save('cor-reaction-methane',f)
    for corr in [False,True]:
        f,a=cv()
        for j,x in enumerate([3,11]):
            ln(a,[(x,3.2),(x,.7),(x+1.4,.7),(x+1.4,3.2)]);a.add_patch(Rectangle((x+.03,.73),1.34,1.3,fc='#E5E6E7' if corr and j else '#DDEBF7',ec='none'));tx(a,x+.7,3.8,'Témoin' if j==0 else 'Gaz étudié')
            if corr:tx(a,x+.7,.25,'Limpide' if j==0 else 'Trouble',G,9.5)
        tx(a,8,4.35,'Aucun gaz ajouté au témoin' if not corr else 'Cas illustratif : le gaz étudié contient du CO₂',N,10)
        save(('cor' if corr else 'ex')+'-temoin',f)
    f,a=cv();bx(a,5.6,.7,4.8,3.0,'Bougie\n(partie pesée)',fill='white');ar(a,(.7,2.8),(5.2,2.8),label='O₂ entrant',off=(0,.45));ar(a,(10.8,2.8),(15.3,2.8),label='CO₂ + eau sortants',off=(0,.45));tx(a,8,.2,'Système ouvert : la pesée seule omet des échanges de matière',M,9.5);save('cor-bougie-ouverte',f)
    for name,initial,consumed,rest,product in [('cor-bilan-carbone-6',(6,24),(6,16),'O₂ : 8 g',22),('cor-bilan-carbone-9',(9,20),(7.5,20),'C : 1,5 g',27.5)]:
        f,a=cv();bx(a,.4,1.4,4.4,1.9,f'Avant\nC : {initial[0]} g\nO₂ : {initial[1]} g');ar(a,(5.1,2.4),(7.3,2.4));bx(a,7.7,1.4,3.8,1.9,f'CO₂ formé\n{str(product).replace(".",",")} g');bx(a,12,1.4,3.6,1.9,'Réactif restant\n'+rest);tx(a,8,.35,'Masse totale finale = produit formé + réactif restant',G,9.5);save(name,f,dict(initial=initial,consomme=consumed,produit=product))

def exact_canvas(height_cm=3.5,width_cm=15.0):
    f=plt.figure(figsize=(width_cm/2.54,height_cm/2.54));a=f.add_axes([0,0,1,1]);a.set(xlim=(0,width_cm),ylim=(0,height_cm));a.axis('off');return f,a
def force(a,x,y,length,horizontal=True,sign=1,label='',c=G):
    q=(x+sign*length,y) if horizontal else (x,y+sign*length)
    a.plot([x,q[0]],[y,q[1]],color=c,lw=1.6,zorder=5)
    if horizontal:verts=[q,(q[0]-sign*.22,q[1]+.09),(q[0]-sign*.22,q[1]-.09)]
    else:verts=[q,(q[0]+.09,q[1]-sign*.22),(q[0]-.09,q[1]-sign*.22)]
    a.add_patch(Polygon(verts,fc=c,ec=c,zorder=5));a.add_patch(Circle((x,y),.03,fc=N,zorder=6))
    if label:tx(a,(x+q[0])/2+(0 if horizontal else 1.5),(y+q[1])/2+(.4 if horizontal else 0),label,c,10)
def physique():
    f,a=exact_canvas(3.2);ln(a,[(1,1.5),(7,1.5)]);tx(a,1,2.35,'Soleil',ha='left');tx(a,7,2.35,'150 millions de kilomètres')
    for xx in [1,7]:ln(a,[(xx,1.3),(xx,1.7)])
    tx(a,4,.65,'6 cm');tx(a,11.4,1.4,'Échelle : 1 cm pour\n25 millions de kilomètres',size=9.5);save('cor-distance-bilan',f,dict(longueur_cm=6,echelle=25,distance_millions_km=150,exact=True))
    f,a=exact_canvas(3.2,15.748);ln(a,[(.35,1.4),(15.35,1.4)]);tx(a,.35,2.2,'Soleil',ha='left');
    for xx,value in [(5.35,50),(15.35,150)]:
        ln(a,[(xx,1.2),(xx,1.6)]);tx(a,xx,2.2,f'{value} millions km',ha='right' if value==150 else 'center');tx(a,xx,.55,f'{value/10:g} cm',ha='right' if value==150 else 'center')
    tx(a,8,2.95,'1 cm pour 10 millions de kilomètres',size=10);save('cor-echelle-astronomie',f,dict(cm=[5,15],millions_km=[50,150],echelle_reelle=True))
    for name,maximum,mark,scale in [('cor-frise-750',30,8,25),('cor-frise-salle',900,30,5)]:
        f,a=cv();x0,x1=1,15;ln(a,[(x0,2.1),(x1,2.1)]);tx(a,x0,3.2,'Soleil',ha='left');tx(a,x1,3.2,f'{maximum} cm',ha='right');pos=x0+(x1-x0)*mark/maximum;ln(a,[(pos,1.9),(pos,2.3)],G,2);ar(a,(4,1),(pos,1.9),label=f'{mark} cm',off=(.4,-.3));tx(a,10,.6,f'Échelle de la frise : 1 cm → {scale} millions km',size=9.5);tx(a,8,4.1,'Schéma réduit : les longueurs indiquées sont celles de la frise',M,9.4);save(name,f,dict(longueur_cm=maximum,repere_cm=mark,echelle=scale))
    f,a=cv();ln(a,[(.4,.7),(15.5,.7)],M,2);bx(a,3,1.3,7,1.8,'',fill='white');tx(a,6.5,1.65,'Train');bx(a,5.6,2.1,1.6,.55,'livre');ar(a,(10.5,2.2),(14.7,2.2),label='déplacement vu du sol');tx(a,6.5,3.8,'Livre immobile par rapport au train');tx(a,8,.2,'Par rapport au sol : train et livre se déplacent ensemble',G,9.5);save('cor-referentiels',f)
    for corr in [False,True]:
        f,a=cv();xs=[1,2,3.5,5.5,8,11]
        for j,x in enumerate(xs):a.add_patch(Circle((x,2.3),.10,fc=N));tx(a,x,1.65,str(j),M,9)
        tx(a,8,3.8,'Même durée entre deux positions successives')
        if corr:
            for u,v in zip(xs[:-1],xs[1:]):ar(a,(u,2.7),(v,2.7))
            tx(a,8,.5,'Distances successives croissantes → valeur de vitesse croissante',G,9.5)
        save(('cor' if corr else 'ex')+'-chronophoto',f,dict(positions=xs,dt_constant=True))
        def annot(a):
            a.plot([2,4,4],[3,3,6],'--',color=G,lw=1.2);tx(a,3,2.3,'2 s',G,9);tx(a,4.6,4.6,'3 m',G,9)
        plot(('cor' if corr else 'ex')+'-position',[0,2,4,6],[0,3,6,9],'Temps (s)','Position (m)',annotate=annot if corr else None,ylim=(0,11))
        plot(('cor' if corr else 'ex')+'-position-retour',[0,1,2,3,4],[8,6,4,2,0],'Temps (s)','Position (m)',annotate=(lambda a:note(a,'Même distance chaque seconde',(2,4),(.2,1.2))) if corr else None,ylim=(0,9))
    f,a=cv();a.add_patch(Circle((8,2.3),1.5,fill=False,ec=N,lw=1.2))
    for th in [0,np.pi/2,np.pi,3*np.pi/2]:
        p=(8+1.5*np.cos(th),2.3+1.5*np.sin(th));q=(p[0]-.85*np.sin(th),p[1]+.85*np.cos(th));a.add_patch(Circle(p,.08,fc=N));ar(a,p,q)
    tx(a,3,2.3,'Même valeur\nde vitesse');tx(a,12.8,2.3,'Directions\ndifférentes');save('cor-manege',f)
    f,a=cv();force(a,5,1.2,2.2,False,1,'vers le haut');force(a,11,3.4,2.2,False,-1,'vers le bas');tx(a,8,.25,'Direction verticale commune · sens opposés',G);save('cor-direction-sens',f)
    f,a=exact_canvas(3.3);force(a,1,2.1,3,label='6 N → 3 cm');force(a,10,2.1,.5,label='1 N → 0,5 cm')
    for base,le in [(1,3),(10,.5)]:
        ln(a,[(base,1.2),(base+le,1.2)],M,.8)
        for k in np.arange(0,le+.01,.5):ln(a,[(base+k,1.12),(base+k,1.28)],M,.7)
    tx(a,8,.4,'Échelle : 1 cm pour 2 N · impression à 100 %',size=10);save('cor-forces-echelle',f,dict(longueurs_cm=[3,.5],forces_N=[6,1],exact=True))
    for corr in [False,True]:
        f,a=exact_canvas(3.3);force(a,3,1.8,4,label='2 N' if corr else 'F');ln(a,[(3,.9),(7,.9)],M,.8)
        for k in range(5):ln(a,[(3+k,.8),(3+k,1.0)],M,.7)
        tx(a,11,1.5,'4 cm\n1 cm pour 0,5 N');save(('cor' if corr else 'ex')+'-force-4cm',f,dict(longueur_cm=4,force_N=2,exact=True))
    f,a=cv();bx(a,2.5,2.7,3,1,'Livre');bx(a,.6,.8,3,1,'Table');bx(a,5.2,.8,3,1,'Terre');ln(a,[(3.2,2.7),(2.1,1.8)]);ln(a,[(4.8,2.7),(6.7,1.8)],ls='--');tx(a,4,4.2,'Diagramme des interactions',size=9.5)
    ln(a,[(10,1.5),(15.6,1.5)],M,2);bx(a,10.8,1.55,1.8,.65,'',fill='white');force(a,11.7,1.875,1.1,False,-1);force(a,11.7,1.55,1.1,False,1);tx(a,14.2,1.1,'Poids',G,9.5);tx(a,14.2,2.5,'Support',G,9.5);tx(a,12.5,4.1,'Forces sur le livre',size=9.5);save('cor-livre-forces',f,dict(forces_compensees=True,longueurs=[1.1,1.1]))
    f,a=cv();bx(a,1,1.5,4,1.5,'');bx(a,11,1.5,4,1.5,'');tx(a,3,1.85,'Main');tx(a,13,1.85,'Boîte');force(a,3.5,2.6,2,horizontal=True,sign=-1);force(a,12.5,2.6,2);tx(a,3,3.65,'Boîte sur main',G);tx(a,13,3.65,'Main sur boîte',G);tx(a,8,.5,'Deux forces reçues par deux objets différents',G);save('cor-main-boite',f)
    for kind in ['ex-suspension-incomplete','cor-suspension','ex-objet-suspendu']:
        f,a=cv();ln(a,[(6,4.1),(10,4.1)],M,2);ln(a,[(8,4.1),(8,2.7)],M);bx(a,7.3,1.8,1.4,.8,'',fill='white');tx(a,6.6,2.2,'objet',ha='right',size=9.5)
        if kind!='ex-objet-suspendu':force(a,8,2.2,1.4,False,1,'fil')
        if kind=='cor-suspension':force(a,8,2.2,1.4,False,-1,'poids');tx(a,12.5,2.0,'Même valeur\nsens opposés',G)
        if kind=='ex-objet-suspendu':bx(a,7.4,3.1,1.2,.65,'3 N');tx(a,12,2.0,'Objet immobile')
        save(kind,f)
    f,a=exact_canvas(6.0);tx(a,3,4.9,'Modèle ponctuel\nde l’objet en G',size=10);force(a,8,3,2,False,1,'Fil : 3 N');force(a,8,3,2,False,-1,'Poids : 3 N');tx(a,7.6,3,'G',size=10,ha='right');tx(a,8,.45,'Chaque flèche : 2 cm · échelle 1 cm pour 1,5 N',size=10);save('cor-suspension-3N',f,dict(longueurs_cm=[2,2],forces_N=[3,3],exact=True))
    f,a=cv();bx(a,1,1.4,5,1.6,'Système : objet');bx(a,9.4,1.4,5,1.6,'Système : objet + fil');tx(a,3.5,3.8,'Fil : partenaire extérieur');tx(a,11.9,3.8,'Fil : inclus dans le système');tx(a,8,.45,'Dans le second bilan, rechercher l’action du support extérieur',G,9.5);save('cor-systemes',f)
    for name,mass,pt,pl in [('cor-terre-lune-5kg','5 kg',50,8),('cor-colis-lunaire','0,750 kg',7.35,1.2)]:
        f,a=cv()
        for x,p,label in [(4,pt,'Terre'),(12,pl,'Lune')]:
            a.add_patch(Circle((x,3.2),.10,fc=N));force(a,x,3.2,2.5*p/pt,False,-1);tx(a,x,4.1,label+' · '+mass);tx(a,x+1.8,1.9,str(p).replace('.',',')+' N',G,10)
        save(name,f,dict(masse=mass,poids=[pt,pl]))
    f,a=cv();a.add_patch(Circle((8,3.5),.1,fc=N));force(a,8,3.5,2.3,False,-1,'P = 20 N');tx(a,4,2.2,'Verticale locale');tx(a,12,2.2,'Vers le centre\nde la Terre');save('cor-poids-20N',f)
    for corr in [False,True]:
        plot(('cor' if corr else 'ex')+'-poids-graphe',[.1,.2,.3],[1,2,3],'Masse (kg)','Poids (N)',other=[([0,.45],[0,4.5],'Modèle et prévision : 0,45 kg → 4,5 N',G)] if corr else None,ylim=(0,5),xlim=(0,.5))
        plot(('cor' if corr else 'ex')+'-poids-decale',[0,.1,.2,.3],[.3,1.3,2.3,3.3],'Masse (kg)','Poids affiché (N)',other=[([0,.1,.2,.3],[0,1,2,3],'Après correction du zéro',G)] if corr else None,ylim=(0,4))
    for name,val,scale in [('cor-poids-25N',2.5,1)]:
        f,a=exact_canvas(4.2);force(a,7,3.3,val/scale,False,-1,'P = 2,5 N');tx(a,11,2.4,'m = 0,250 kg\ng = 10 N/kg');tx(a,8,.2,'2,5 cm · échelle 1 cm pour 1 N',size=10);save(name,f,dict(longueur_cm=2.5,force_N=2.5,exact=True))
    f,a=cv();bx(a,6.6,1.8,2.8,.8,'');ln(a,[(5,1.75),(11,1.75)],M,2);force(a,8,2.2,1.6,False,1);force(a,8,2.2,1.6,False,-1);tx(a,12,3.2,'Support : 12 N',G,10);tx(a,12,1.1,'Poids : 12 N',G,10);tx(a,4,2.2,'Caisse',N,10);save('cor-caisse-12N',f,dict(forces_N=[12,12]))
    for name,ei,out1,out2,stock in [('cor-energie-lampe',200,('Lumière',60),('Thermique',140),0),('cor-energie-moteur',500,('Mécanique',350),('Thermique',150),0),('cor-energie-stockage',80,('Sorties',30),None,50),('cor-convertisseur',800,('Mécanique',500),('Thermique',220),80)]:
        f,a=cv();bx(a,5.6,1.4,4.6,1.7,'Système');ar(a,(.5,2.3),(5.2,2.3),label=f'Entrée : {ei} J',off=(0,.6));ar(a,(10.6,2.8),(15.3,3.5),label=f'{out1[0]} : {out1[1]} J',off=(0,.6))
        if out2:ar(a,(10.6,1.7),(15.3,1.0),label=f'{out2[0]} : {out2[1]} J',off=(0,-.6))
        tx(a,7.9,.4,f'Variation de stockage : +{stock} J' if stock else 'Pas de variation du stockage',G,10);save(name,f,dict(entree=ei,sortie1=out1[1],sortie2=out2[1] if out2 else 0,stockage=stock))
    f,a=cv();bx(a,5.5,1.5,4.8,1.6,'Cellule\nphotovoltaïque');ar(a,(.6,2.3),(5.1,2.3),label='Rayonnement reçu',off=(0,.65));ar(a,(10.7,2.7),(15.2,3.3),label='Électrique utile',off=(0,.6));ar(a,(10.7,1.8),(15.2,1.0),label='Autres, dont thermique',off=(0,-.6));save('cor-photovoltaique',f)
    f,a=plt.subplots(figsize=(6.2,2.0));f.subplots_adjust(left=.13,right=.98,bottom=.28,top=.95);a.bar([0,1],[6000,12000],color=[N,G],width=.5);a.set(xticks=[0,1],xticklabels=['A : 100 W × 1 min','B : 10 W × 20 min'],ylabel='Énergie (J)',ylim=(0,14000));a.grid(axis='y',color=L);a.set_axisbelow(True);save('cor-puissance-duree',f,dict(A_J=6000,B_J=12000))

def produire():
    OUT.mkdir(exist_ok=True);matiere();physique()
    from figures_electricite_exercices import produire as elec
    from figures_signaux_exercices import produire as signaux
    elec();signaux()
    from revision_exercices import ILLUSTRATIONS,ANNEXES
    wanted={v[k] for v in ILLUSTRATIONS.values() for k in ['figure','figure_correction'] if v[k]}
    wanted|={fig for entry in ANNEXES.values() for mode in entry.values() for fig,cap,exact in mode.values()}
    assert wanted==set(REGISTRY),dict(manquent=sorted(wanted-set(REGISTRY)),inutilisees=sorted(set(REGISTRY)-wanted))
    (HERE/'build/figures-exercices.json').write_text(json.dumps(dict(nombre=len(REGISTRY),figures=REGISTRY),ensure_ascii=False,indent=2),encoding='utf8')
    print(f'{len(REGISTRY)} figures vectorielles pour les exercices, défis et bilans.')
if __name__=='__main__':
    # Partager le registre avec les modules de figures importés ensuite.
    import sys
    sys.modules['figures_revision']=sys.modules[__name__]
    produire()
