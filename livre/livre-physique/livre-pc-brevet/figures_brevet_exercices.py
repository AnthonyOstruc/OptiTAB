"""Figures vectorielles propres aux données de Troisième et aux dix sujets DNB."""
from figures_revision import *
from figures_electricite_exercices import circuit,symbol,switch,node

def chain(name,items,footer='',correct=True):
    f,a=cv();w=14.8/len(items)
    for j,(title,body) in enumerate(items):
        x=.6+j*w;bx(a,x,1.15,w-.65,2.25,title+'\n'+body,fill='#E8F2E6' if correct and j==len(items)-1 else L)
    if footer:tx(a,8,.35,footer,G if correct else M,9.5)
    save(name,f,dict(blocs=items,conclusion=footer))

def inventory(name,rows,footer=''):
    f,a=cv();w=14.8/len(rows)
    for j,(title,p,n,e,charge) in enumerate(rows):
        x=.6+j*w
        bx(a,x,1.65,w-.55,1.65,f'{title}\nNoyau : {p} p⁺'+(' ; '+str(n)+' n' if n is not None else ''),fill=L)
        tx(a,x+(w-.55)/2,3.95,'Inventaire symbolique',M,9)
        tx(a,x+(w-.55)/2,1.05,f'Cortège : {e} e⁻',G,10)
        tx(a,x+(w-.55)/2,.48,f'Charge : {charge}',G,10)
    if footer:tx(a,8,4.4,footer,size=9.3)
    save(name,f,dict(constituants=rows))

def atome_brevet7():
    f,a=cv(1.0)
    bx(a,.7,1.1,7,2.6,'Noyau : 13 p⁺ et 14 n',fill=L)
    bx(a,8.3,1.1,7,2.6,'Cortège : 13 e⁻\nAtome Al neutre',fill='#E8F2E6')
    tx(a,8,.35,'Z = 13 ; A = 13 + 14 = 27',G,9.5)
    save('rev-bb7-atome',f,dict(protons=13,neutrons=14,electrons=13,Z=13,A=27))

def immersion(name,vi,vf,mass,corr=False):
    f,a=cv();maximum=60
    for x,v,solid in [(2,vi,False),(11,vf,True)]:
        ln(a,[(x,3.6),(x,.7),(x+1.8,.7),(x+1.8,3.6)])
        a.add_patch(Rectangle((x+.02,.72),1.76,v/maximum*2.7,fc='#DDEBF7',ec='none',zorder=1))
        for val in range(10,61,10):
            yy=.7+val/maximum*2.7;ln(a,[(x+1.45,yy),(x+1.8,yy)],M,.7);tx(a,x+2,yy,str(val),M,8.8,ha='left')
        if solid:a.add_patch(Polygon([(x+.3,.8),(x+1.2,.85),(x+1.35,1.4),(x+.45,1.45)],fc='#ADB8CB',ec=N,zorder=3))
        tx(a,x+.9,4.08,f'{v:g} mL')
    ar(a,(5.6,2.8),(9.7,2.8),label=f'Solide : {mass:g} g'.replace('.',','),off=(0,.5))
    tx(a,8,1.3,'Immersion complète\nSans bulle · solide insoluble',M,9.3)
    if corr:tx(a,8,.25,f'V = {vf:g} − {vi:g} = {vf-vi:g} cm³ ; ρ = {mass/(vf-vi):.2f} g/cm³'.replace('.',','),G,10)
    save(name,f,dict(Vi_mL=vi,Vf_mL=vf,masse_g=mass,volume_cm3=vf-vi,rho=mass/(vf-vi),corrige=corr))

def ph():
    for key,vals,labels in [('acide',[2,4],['Départ','Après dilution']),('base',[12,10],['Départ','Après dilution']),('classement',[4,7,9],['A : acide','B : neutre','C : basique']),('solutions',[3,10],['A : acide','B : basique'])]:
        f,a=cv();ln(a,[(1,2.3),(15,2.3)],M)
        for value in range(15):
            xx=1+value;ln(a,[(xx,2.15),(xx,2.45)],M,.7);tx(a,xx,1.82,str(value),size=9)
        tx(a,4,4.2,'Acide : pH < 7',R);tx(a,8,4.2,'Neutre : 7',M);tx(a,12,4.2,'Basique : pH > 7',N)
        for val,label in zip(vals,labels):
            a.plot([val+1],[2.3],'o',color=G,ms=5,zorder=5);tx(a,val+1,3.45,label,G,9.4)
        if key in ['acide','base']:ar(a,(vals[0]+1,2.8),(vals[1]+1,2.8),label='dilution',off=(3,.1))
        tx(a,8,.55,'Classement par rapport à 7, vers 25 °C',M,9.4)
        save('rev-cor-ph-'+key,f,dict(valeurs=vals,neutre=7))
    f,a=cv();ln(a,[(2,2),(14,2)],M)
    for x,label in [(3,'7 : neutre'),(9,'8,0 : après'),(11,'8,2 : avant')]:
        ln(a,[(x,1.8),(x,2.2)],G);tx(a,x,.95 if x==9 else 1.45,label,size=9.5)
    ar(a,(11,2.8),(9,2.8),label='pH diminue',off=(0,.4));tx(a,8,4.1,'Zoom schématique : 8,2 → 8,0, toujours pH > 7',size=10);tx(a,8,.35,'Acidification ne signifie pas nécessairement solution acide',G,9.5)
    save('rev-cor-ph-ocean',f,dict(valeurs=[8.2,8.0],neutre=7,zoom_schematique=True))

def iontests(name,results=True):
    f,a=cv();tx(a,8,4.18,'Banque de tests sur des prélèvements séparés',size=10)
    for x,reagent,result,col in [(1.2,'Nitrate d’argent','Blanc : Cl⁻','#E6E7E8'),(6.5,'Soude','Bleu : Cu²⁺','#93BBDF'),(11.8,'Soude','Vert : Fe²⁺','#9BC4A1')]:
        ln(a,[(x,3.1),(x,.85),(x+1.25,.85),(x+1.25,3.1)])
        a.add_patch(Rectangle((x+.02,.87),1.21,1.,fc=col,ec='none'));ar(a,(x+.62,3.6),(x+.62,2.9))
        tx(a,x+1.7,3.7,reagent,size=9.3);tx(a,x+1.9,2.3,result,G,9.4)
    tx(a,8,.25,'Choisir le réactif adapté ; témoins, protections et limites de détection',M,9.3)
    save(name,f,dict(principe='prelevements separes',resultats=results))

def test_bb2(name,corr=False):
    f,a=cv();tx(a,8,4.12,'Résultats observés sur deux prélèvements',size=10)
    for x,reagent,result,col in [(2.0,'Nitrate d’argent','Précipité blanc','#DFE1E3'),(10.2,'Soude','Pas de précipité bleu','#DDEBF7')]:
        ln(a,[(x,3.15),(x,.8),(x+1.5,.8),(x+1.5,3.15)])
        a.add_patch(Rectangle((x+.02,.82),1.46,1.2,fc=col,ec='none'));tx(a,x+2.9,3.1,reagent,size=9.5)
        tx(a,x+2.9,1.5,result,G,9.4)
    tx(a,8,.28,'Cl⁻ détecté ; Cu²⁺ non mis en évidence dans les conditions du test' if corr else 'Banque de tests et pH = 6 dans le document',G if corr else M,9.3)
    save(name,f,dict(chlorure='positif',cuivre='negatif',corrige=corr))

def corrosion():
    f,a=cv()
    for j,(title,body,obs) in enumerate([('A','Air sec','Pas de rouille'),('B','Eau + air','Rouille'),('C','Eau salée + air','Rouille'),('D','Eau sans O₂','Pas de rouille')]):
        x=.4+4*j;bx(a,x,.95,3.2,2.45,'',fill='white');a.plot([x+1.6,x+1.6],[2.9,1.3],color=M,lw=3,zorder=4)
        if j in [1,2]:a.plot([x+1.6],[1.9],'o',color='#AE7047',ms=6,zorder=4)
        tx(a,x+1.6,4.1,title+' · '+body,size=9.1);tx(a,x+1.6,.45,obs,G if j in [0,3] else R,9.3)
    tx(a,8,3.63,'Clous comparables · même durée · autres conditions contrôlées',M,9.2)
    save('rev-cor-corrosion',f,dict(conditions=['air sec','eau air','eau salee air','eau sans O2'],rouille=[False,True,True,False]))

def gravity(name,numeric='',corr=True):
    f,a=cv();xs=[3,13]
    for x,lab,r in [(3,'A',.7),(13,'B',.45)]:
        a.add_patch(Circle((x,2.3),r,fc=L,ec=N,zorder=3));tx(a,x,2.3,lab)
    ln(a,[(3,3.6),(13,3.6)],M);tx(a,8,4.04,'d : distance entre les centres'+(' = '+numeric if numeric else ''),size=9.4)
    for x in xs:ln(a,[(x,3.4),(x,3.8)],M)
    if corr:
        force(a,3,2.3,2.9,label='B agit sur A');force(a,13,2.3,2.9,sign=-1,label='A agit sur B')
        tx(a,8,.45,'Même valeur · sens opposés · deux systèmes différents',G,9.5)
    else:tx(a,8,.6,'Tailles et distances représentées sans échelle commune',M,9.3)
    save(name,f,dict(distance=numeric,forces_opposees=corr,systemes_distincts=True))

def weights(name,value=19.2,exact=False):
    if exact:
        f,a=exact_canvas(10.2);x,y,le=6.0,5.1,value/10
        tx(a,11,5.1,'Modèle ponctuel\nde la caisse en G',size=10)
    else:
        f,a=cv();x,y,le=6,2.3,1.55
        tx(a,11.3,2.3,'Objet immobile\nModèle à deux forces',size=10)
    force(a,x,y,le,False,1,('Fil : ' if exact else 'Support : ')+f'{value:g} N'.replace('.',','))
    force(a,x,y,le,False,-1,f'Poids : {value:g} N'.replace('.',','))
    tx(a,x-.3,y,'G',ha='right',size=10)
    tx(a,7.5,.45,'1 cm pour 10 N · impression à 100 %' if exact else 'Direction verticale locale · sens opposés',M,9.5)
    save(name,f,dict(poids_N=value,support_N=value,longueurs_cm=[le,le] if exact else [],exact=exact))

def energy(name,total,useful,other,unit='J',device='Convertisseur'):
    f,a=cv();bx(a,5.7,1.35,4.3,1.8,device,fill='white')
    ar(a,(.65,2.3),(5.4,2.3),label=f'Entrée : {total:g} {unit}'.replace('.',','),off=(0,.55))
    ar(a,(10.2,2.8),(15.4,2.8),label=f'Utile : {useful:g} {unit}'.replace('.',','),off=(0,.52))
    ar(a,(10.2,1.6),(15.4,1.6),c=R,label=f'Milieu : {other:g} {unit}'.replace('.',','),off=(0,-.52))
    tx(a,8,.3,'Sans variation de stockage : entrée = somme des sorties',M,9.3)
    save(name,f,dict(entree=total,utile=useful,milieu=other,unite=unit,conservation=total==useful+other))

def echo(name,corr=False,light=False,delay=.080,speed=1500):
    f,a=cv();bx(a,.6,1.4,3.1,1.7,'Terre\németteur' if light else 'Sonar\nbateau',fill='white')
    ln(a,[(13.4,.6),(13.4,3.8)],M,2);tx(a,14.5,2.3,'Lune' if light else 'Fond',size=9.5)
    ar(a,(4.1,3.1),(13.2,3.1),label='Aller'+(' : '+f'{speed*delay/2:g}'.replace('.',',')+(' km' if light else ' m') if corr else ''),off=(0,.42))
    ar(a,(13.2,1.35),(4.1,1.35),c=N,label='Retour : même distance',off=(0,-.4))
    tx(a,8,2.3,f'Durée totale : {delay:g} s'.replace('.',','),size=10)
    tx(a,8,.25,('d = vΔt / 2 = '+f'{speed*delay/2:g}'.replace('.',',')+(' km' if light else ' m')) if corr else 'Flèches séparées pour la lecture ; même trajet physique',G if corr else M,9.4)
    save(name,f,dict(aller_retour_s=delay,vitesse=speed,distance=speed*delay/2,unite='km' if light else 'm',corrige=corr))

def parallel_resistors(name,voltage=6,values=(100,200),corr=True):
    f,a=cv();top,mid,bot=3.55,1.8,.5
    ln(a,[(2,bot),(2,top),(14,top),(14,bot),(2,bot)]);ln(a,[(5,top),(5,mid),(14,mid)])
    symbol(a,2,2.0,'G');tx(a,.6,2.0,f'{voltage} V',size=9.2);tx(a,1.3,2.7,'+',G);tx(a,1.3,1.4,'−',G)
    for j,(yy,r) in enumerate(zip([top,mid],values),1):
        symbol(a,10,yy,'R',f'R{j} = {r} Ω')
        tx(a,11.6,yy-.55,f'U{j} = {voltage} V',G,9.4)
        if corr:ar(a,(6,yy),(7,yy),label=f'I{j} = {voltage/r:.3f} A'.replace('.',','),off=(0,-.55))
    tx(a,8,.13,'Même tension aux bornes de chaque résistance',M,9.3)
    save(name,f,dict(tension=voltage,resistances=list(values),courants=[voltage/r for r in values]))

def refuge(name,corr=False):
    f,a=cv();top,mid,bot=3.55,1.8,.5
    ln(a,[(2,bot),(2,top),(14,top),(14,bot),(2,bot)]);ln(a,[(5,top),(5,mid),(14,mid)])
    symbol(a,2,2.0,'G');tx(a,.65,2.,'12 V',size=9.2);tx(a,1.3,2.7,'+',G);tx(a,1.3,1.4,'−',G)
    for yy,la,cur in [(top,'L₁','0,30 A'),(mid,'L₂','0,20 A')]:
        switch(a,6.6,yy,label='K₁' if yy==top else 'K₂');symbol(a,10,yy,'L',la if not corr or yy==top else '')
        if corr and yy==mid:tx(a,10,1.18,'L₂',size=9.4)
        if not corr:tx(a,12,yy-.53,cur,G,9.4)
    if corr:
        # V on L1, A inserted in L2; neither meter bypasses the source.
        ln(a,[(8.6,top),(8.6,2.65),(11.4,2.65),(11.4,top)]);symbol(a,10,2.65,'V')
        tx(a,9.35,2.23,'V',G,8.8);tx(a,10.75,2.23,'COM',G,8.8)
        symbol(a,12.4,mid,'A');tx(a,11.8,1.22,'A',G,8.8);tx(a,13.1,1.22,'COM',G,8.8)
        tx(a,8,.12,'U₁ = U₂ = 12 V ; IG = 0,30 + 0,20 = 0,50 A',G,9.4)
    else:tx(a,8,.12,'Interrupteurs K₁ et K₂ fermés pendant les mesures',M,9.4)
    save(name,f,dict(U=12,I1=.3,I2=.2,IG=.5,voltmeter_L1=corr,ammeter_L2=corr))

def montage9(name,corr=False):
    f,a=cv();top,mid,bot=3.55,1.45,.45
    ln(a,[(2,bot),(2,top),(14,top),(14,bot),(2,bot)]);ln(a,[(4.5,top),(4.5,mid),(14,mid)])
    symbol(a,2,2.0,'G');tx(a,.65,2.0,'9 V',size=9.2);tx(a,1.3,2.7,'+',G);tx(a,1.3,1.4,'−',G)
    symbol(a,9,top,'L','L₁ · 4 V');symbol(a,12,top,'L','L₂ · 5 V');symbol(a,9,mid,'R','R')
    if corr:
        symbol(a,6,top,'A');tx(a,6,2.95,'150 mA',G,9.1)
        ln(a,[(7.4,mid),(7.4,2.5),(10.6,2.5),(10.6,mid)]);symbol(a,9,2.5,'V')
        tx(a,12.2,1.0,'UR = 9 V',G,9.3);tx(a,5.3,.12,'IG = 210 mA',G,9.4)
    else:tx(a,8,.12,'Branche des lampes : 150 mA ; branche de R : 60 mA',M,9.3)
    save(name,f,dict(U=9,U1=4,U2=5,I1=.15,I2=.06,IG=.21,correction=corr))

def produire():
    OUT.mkdir(exist_ok=True)
    atome_brevet7()
    immersion('rev-ex-immersion',28,43,40.5);immersion('rev-cor-immersion',28,43,40.5,True)
    immersion('rev-bb7-enonce',30,50,54);immersion('rev-bb7-corrige',30,50,54,True)
    for corr in [False,True]:
        plot('rev-'+('cor' if corr else 'ex')+'-ebullition',[0,1,2,3,4,5,6],[20,50,80,100,100,100,100],'Temps (min)','Température (°C)',annotate=(lambda a:note(a,'Palier : 3 min',(4.5,100),(.3,105))) if corr else None,ylim=(0,125))
        plot('rev-'+('cor' if corr else 'ex')+'-poids-graphe',[.1,.2],[1,2],'Masse (kg)','Poids (N)',other=[([0,.25],[0,2.5],'Modèle : P = 10 m',G)] if corr else None,ylim=(0,2.8),xlim=(0,.27))
        plot('rev-'+('cor' if corr else 'ex')+'-ohm-100',[.01,.02,.03],[1,2,3],'Intensité (A)','Tension (V)',other=[([0,.035],[0,3.5],'Modèle : R = 100 Ω',G)] if corr else None,ylim=(0,4),xlim=(0,.04))
        plot('rev-'+('cor' if corr else 'ex')+'-ohm-inverse',[0,1,2,3],[0,.01,.02,.03],'Tension (V)','Intensité (A)',annotate=(lambda a:note(a,'R = U/I = 100 Ω',(2,.02),(.2,.032))) if corr else None,ylim=(0,.04),xlim=(0,3.5))
    chain('rev-cor-separation',[('Mélange','Eau + sel + sable'),('Filtration','Sable dans le filtre'),('Distillation du filtrat','Eau recueillie ; sel reste')],'Le sel dissous traverse le filtre ordinaire')
    f,a=cv();ln(a,[(2,2.2),(14,2.2)],M);ln(a,[(3.8,2.2),(12.2,2.2)],G,4)
    for x,label in [(3.8,'2,63'),(9.68,'2,70 : référence Al'),(12.2,'2,73')]:
        ln(a,[(x,1.9),(x,2.5)],G);tx(a,x,3.2,label,size=9.5)
    tx(a,8,1.2,'Intervalle : 2,68 ± 0,05 g/cm³',G);save('rev-cor-intervalle',f,dict(min=2.63,max=2.73,reference=2.7))
    chain('rev-cor-tare',[('Flacon rempli','109 g'),('Flacon vide','45 g'),('Liquide seul','109 − 45 = 64 g')],'ρ = 64 / 80 = 0,80 g/mL')
    for key,rows in [('na',[('Na',11,12,11,'0')]),('cu',[('Cu',29,None,29,'0'),('Cu²⁺',29,None,27,'+2')]),('cl',[('Cl',17,None,17,'0'),('Cl⁻',17,None,18,'−1')]),('al',[('Al',13,14,13,'0'),('Al³⁺',13,14,10,'+3')]),('mg',[('Mg²⁺',12,None,10,'+2')]),('isotopes',[('Carbone 12',6,6,6,'0'),('Carbone 14',6,8,6,'0')]),('fe3',[('Fe³⁺',26,30,23,'+3')]),('fe2',[('Fe',26,None,26,'0'),('Fe²⁺',26,None,24,'+2')])]:inventory('rev-cor-atome-'+key,rows)
    f,a=cv()
    for x in [3,8,13]:mol(a,x,2.7,'H2O',1.3)
    tx(a,8,.6,'3 × H₂O : 3 × 2 = 6 H ; 3 × 1 = 3 O',G);save('rev-cor-trois-eaux',f,dict(H=6,O=3,molecules=3))
    chain('rev-cor-ions',[('Na → Na⁺','11 e⁻ → 10 e⁻'),('Cl → Cl⁻','17 e⁻ → 18 e⁻')],'Noyaux inchangés ; seuls les électrons sont gagnés ou perdus')
    chain('rev-cor-coefficients',[('2 CH₄','C : 2 × 1 = 2\nH : 2 × 4 = 8'),('3 N₂O','N : 3 × 2 = 6\nO : 3 × 1 = 3')],'L’indice appartient à la formule ; le coefficient multiplie tout')
    chain('rev-cor-oxygene',[('O','Un atome neutre'),('O₂','Deux atomes liés'),('O²⁻','Un ion : 2 e⁻ en plus')],'Ne pas confondre indice et charge')
    chain('rev-cor-echelles-atome',[('Échelle réelle','Atome : environ 10⁻¹⁰ m\nNoyau : environ 10⁻¹⁵ m'),('Maquette','Atome : 10 m\nNoyau : 0,1 mm')],'Deux indications de taille ; aucun dessin des deux objets à la même échelle')
    chain('rev-cor-neutralite',[('Un Ca²⁺','+2 ; deux Cl⁻ : −2\nSomme : 0'),('Deux Ca²⁺','+4 ; quatre Cl⁻ : −4\nSomme : 0')],'Le nombre d’ions chlorure dépend du nombre d’ions calcium')
    for name,items,foot in [
        ('masse-gaz',[('Avant','150,0 g pesés'),('Après','147,8 g pesés'),('Gaz sorti','2,2 g')],'147,8 + 2,2 = 150,0 g'),
        ('masse-carbone',[('Réactifs consommés','C : 6 g ; O₂ : 16 g'),('Produit formé','CO₂ : 22 g')],'6 + 16 = 22 g'),
        ('reactif-restant',[('Avant','10 g + 25 g = 35 g'),('Après','Produits : 30 g\nRéactif restant : 5 g')],'30 + 5 = 35 g'),
        ('masse-fer',[('Fer consommé','2,1 g'),('Milieu incorporé','Oxygène : 0,8 g'),('Produit','2,9 g')],'2,1 + 0,8 = 2,9 g'),
        ('masse-methane',[('Avant','CH₄ : 8 g ; O₂ : 40 g'),('Produits','CO₂ : 22 g ; eau : 18 g'),('Réactif restant','O₂ : 8 g')],'8 + 40 = 22 + 18 + 8 = 48 g'),
        ('masse-corrosion',[('Métal','5,6 g'),('Matière du milieu','2,4 g'),('Produits','8,0 g')],'La matière incorporée explique l’augmentation de masse')]:chain('rev-cor-'+name,items,foot)
    chain('rev-cor-ethanol',[('C₂H₆O + 3 O₂','C : 2 ; H : 6\nO : 1 + 6 = 7'),('2 CO₂ + 3 H₂O','C : 2 ; H : 6\nO : 4 + 3 = 7')],'Chaque élément a le même nombre d’atomes des deux côtés')
    chain('rev-cor-temoin',[('Témoin','Trouble sans gaz ajouté'),('Test','Trouble aussi'),('Conclusion','Le gaz n’est pas\nla seule cause possible')],'Contrôler réactifs, propreté et conditions avant de conclure')
    chain('rev-cor-ions-filtre',[('Solution saline','Na⁺ et Cl⁻ dissous'),('Filtre ordinaire','Les ions traversent'),('Filtrat','Contient encore les ions')],'Des grains en suspension peuvent être retenus ; le sel dissous reste')
    iontests('rev-cor-tests-ions');ph()
    chain('rev-cor-acide-base',[('Avant','H⁺ + HO⁻'),('Après','H₂O')],'Charge : +1 − 1 = 0 ; atomes : deux H et un O conservés')
    f,a=cv();bx(a,1,1.3,5.5,2,'Métal : électrons');ar(a,(5.7,2.1),(2,2.1),label='e⁻',off=(0,.5));bx(a,9,1.3,6,2,'Solution : ions',fill='white');ar(a,(10,2.8),(14,2.8),label='cations +',off=(0,.35));ar(a,(14,1.7),(10,1.7),label='anions −',off=(0,-.35));tx(a,8,.5,'Déplacements schématisés sous l’action d’un champ électrique',M,9.2);save('rev-cor-conduction',f)
    chain('rev-cor-zinc',[('Réactifs','Zn + 2 H⁺\nCharge totale : +2'),('Produits','Zn²⁺ + H₂\nCharge totale : +2')],'Un Zn et deux H de chaque côté ; le noyau de Zn ne change pas')
    f,a=cv();bx(a,1,1.2,14,1.1,'Métal',fill='#C4CDDB');ln(a,[(1,2.4),(7,2.4)],G,4);ln(a,[(8.2,2.4),(15,2.4)],G,4);ar(a,(7.6,3.7),(7.6,2.2),R,label='rayure',off=(2,.0));tx(a,4,3.3,'Peinture intacte',G);tx(a,11.5,3.3,'Air et eau accessibles',R,9.2);tx(a,8,.45,'Comparer avec une pièce intacte dans le même milieu',M,9.4);save('rev-cor-protection',f)
    corrosion()
    chain('rev-cor-pixels',[('Calibration','200 pixels ↔ 1 m'),('Déplacement','80 pixels ↔ 0,40 m'),('Vitesse','0,40 / 0,20 = 2 m/s')],'Calibrer l’image avant de calculer la vitesse')
    plot('rev-cor-bus',[0,20,30],[0,12,12],'Temps depuis le départ (min)','Distance\nparcourue (km)',annotate=lambda a:note(a,'Arrêt : 10 min',(25,12),(8,5)),ylim=(0,14),xlim=(0,32))
    chain('rev-cor-trajets',[('Trajet A','1,2 km / 4 km/h\n0,30 h = 18 min'),('Trajet B','1,5 km / 6 km/h\n15 min + 3 min = 18 min')],'La vitesse moyenne dépend de toute la durée, y compris l’arrêt')
    f,a=cv();a.add_patch(Circle((6,3.5),.07,fc=N));force(a,6,3.5,2.4,False,-1,'P');tx(a,11,2.3,'Direction : verticale locale\nSens : vers le bas',size=10);tx(a,5.5,3.5,'G',ha='right');save('rev-cor-poids',f)
    f,a=cv()
    for x,p,label in [(4,600,'Terre'),(12,96,'Lune')]:
        force(a,x,3.3,2.5*p/600,False,-1);tx(a,x,4.05,label+' · 60 kg');tx(a,x+1.65,1.8,f'{p} N',G)
    tx(a,8,.3,'Même masse ; poids lunaire = 0,16 × poids terrestre',M,9.5);save('rev-cor-poids-lune',f,dict(masse=60,poids=[600,96]))
    f,a=exact_canvas(3.3);force(a,1,2.1,3,label='12 N → 3 cm');force(a,9,2.1,2.5,label='10 N → 2,5 cm');tx(a,7.5,.55,'Échelle : 1 cm pour 4 N · impression à 100 %',size=10);save('rev-cor-force-echelle',f,dict(longueurs_cm=[3,2.5],forces_N=[12,10],exact=True))
    f,a=cv();bx(a,7,1.3,2,1.7,'',fill='white');tx(a,8,2.72,'Objet',size=9.3);force(a,8,2.05,3,True,1,'5 N');force(a,8,2.05,3,True,-1,'5 N',c=N);tx(a,8,.45,'Deux forces sur le même objet ; résultante nulle dans ce modèle',M,9.3);save('rev-cor-forces-5N',f,dict(forces=[5,5]))
    weights('rev-cor-caisse',39.2,True);gravity('rev-cor-gravitation');gravity('rev-cor-centres',corr=False);gravity('rev-cor-satellite','7,0 × 10⁶ m')
    xx=np.linspace(1,3,101);plot('rev-cor-inverse-carre',xx,1/xx**2,'Facteur appliqué à la distance','Rapport F / F initiale',annotate=lambda a:note(a,'Distance × 2 → force / 4',(2,.25),(1.2,.8)),ylim=(0,1.1),xlim=(.8,3.2))
    f,a=cv();a.add_patch(Circle((4.2,2.3),1.4,fc=L,ec=N));a.add_patch(Circle((4.2,2.3),.05,fc=N));ln(a,[(4.2,2.3),(6.7,2.3)]);a.add_patch(Circle((6.7,2.3),.10,fc=G));tx(a,4.9,3.85,'R = 6 400 km',size=9.6);tx(a,8,2.9,'h = 400 km',G,9.6);tx(a,11.5,1.6,'d = R + h\n= 6 800 km',G,11);tx(a,8,.45,'Distances schématisées, pas de proportion avec les rayons dessinés',M,9.2);save('rev-cor-altitude',f,dict(R=6400,h=400,d=6800))
    f,a=cv();a.add_patch(Circle((5,2.4),1.1,fc=L,ec=N));tx(a,5,2.4,'Terre');a.add_patch(Circle((5,2.4),1.8,fill=False,ec=M,ls='--'));a.add_patch(Rectangle((6.5,2.1),.6,.6,fc='white',ec=N,zorder=3));ar(a,(6.8,2.4),(5.7,2.4),label='attraction',off=(1.7,-.7));ar(a,(6.8,2.4),(6.8,3.6),c=N,label='vitesse',off=(1.3,.2));tx(a,12,2.2,'Satellite et contenu\nen chute commune',size=10);tx(a,8,.16,'Schéma de principe : force et vitesse ont des rôles différents',M,9.3);save('rev-cor-orbite',f)
    xx=np.linspace(0,3,101)
    plot('rev-cor-ec-facteurs',xx,xx**2,'Rapport des vitesses v / v₀','Rapport d’énergie\nEc / Ec₀',annotate=lambda a:note(a,'Vitesse × 2 → énergie × 4',(2,4),(.15,7.5)),ylim=(0,10),xlim=(0,3.2))
    chain('rev-cor-freinage',[('Avant freinage','Énergie cinétique\n3 000 J'),('Après freinage','Énergie cinétique\n750 J'),('Transferts / conversions','Notamment thermiques\n2 250 J')],'3 000 = 750 + 2 250 J : l’énergie totale est conservée')
    chain('rev-cor-chute',[('Au départ','Ec = 0 J ; Ep = 40 J'),('Plus bas','Ec = 25 J ; Ep = 15 J')],'Énergie mécanique : 40 J dans les deux états, sans frottements')
    chain('rev-cor-chute-reelle',[('Au départ','Énergie mécanique\n100 J'),('À l’arrivée','Énergie mécanique\n85 J'),('Autres formes / milieu','Notamment thermique\n15 J')],'Une baisse d’énergie mécanique ne détruit pas l’énergie totale')
    chain('rev-cor-vehicules',[('A','800 kg ; 20 m/s\nEc = 160 000 J'),('B','1 600 kg ; 10 m/s\nEc = 80 000 J')],'Le carré de la vitesse change la comparaison des masses')
    circuit('rev-cor-mesures',ammeter=True,voltmeter=True)
    circuit('cor-voltmetre-inverse',inverseV=True,voltmeter=True,comment='Pointes inversées : −4,5 V au lieu de +4,5 V')
    circuit('rev-cor-serie-018',currents=['0,18 A','0,18 A'])
    circuit('rev-cor-parallele-12',parallel=True,source='UG',volts=['U₁ = UG','U₂ = UG'])
    circuit('rev-cor-serie-9V',two=True,source='9 V',voltmeter=True,volts=['3,5 V','5,5 V'])
    # The voltmeter is moved below from L1 to L2 in this dedicated figure.
    # Replace generic series illustration with a precise separate construction.
    REGISTRY.pop('rev-cor-serie-9V');f,a=cv();ln(a,[(2,.6),(2,3.5),(14,3.5),(14,.6),(2,.6)]);symbol(a,2,2,'G');tx(a,.6,2,'9 V',size=9);tx(a,1.3,2.7,'+',G);tx(a,1.3,1.3,'−',G);symbol(a,7,3.5,'L','L₁ · 3,5 V');symbol(a,11.5,3.5,'L','L₂ · 5,5 V');ln(a,[(10,3.5),(10,1.9),(13,1.9),(13,3.5)]);symbol(a,11.5,1.9,'V');tx(a,10.85,1.3,'V',G,9);tx(a,12.2,1.3,'COM',G,9);tx(a,8,.2,'UG = U₁ + U₂ = 9 V',G);save('rev-cor-serie-9V',f,dict(UG=9,U1=3.5,U2=5.5,voltmeter_L2=True))
    parallel_resistors('rev-cor-resistances-12',12);parallel_resistors('rev-cor-resistances-6',6)
    circuit('rev-cor-eclairage-6V',parallel=True,source='6 V',volts=['6 V','6 V'],currents=['0,30 A','0,10 A','0,20 A'])
    for suffix,inval,known,result in [('035','0,35 A',['0,10 A','0,25 A'],'0,35 A'),('080','0,80 A',['0,250 A','?'],'0,550 A'),('090','0,90 A',['0,20 A','0,35 A','?'],'0,35 A')]:
        for corr in [False,True]:
            vals=known[:]
            if corr:vals=[result if s=='?' else s for s in vals]
            if suffix=='035':incoming=inval if corr else '?'
            else:incoming=inval
            ys=[3.7,1.1] if len(vals)==2 else [3.8,2.3,.8]
            node('rev-'+('cor' if corr else 'ex')+'-noeud-'+suffix,[((1.2,2.3),incoming)],[((14.6,yy),v) for yy,v in zip(ys,vals)])
    montage9('rev-ex-montage-9V');montage9('rev-cor-montage-9V',True)
    circuit('rev-cor-montage-ohm',source='6 V',resistor=True,ammeter=True,voltmeter=True,volts=['220 Ω'],currents=['≈ 0,0273 A'])
    plot('rev-cor-lampe-reelle',[0,.1,.2],[0,2,7],'Intensité (A)','Tension (V)',annotate=lambda a:note(a,'Exemple : U/I passe de 20 à 35 Ω',(.2,7),(.008,7.7)),ylim=(0,9),xlim=(0,.23))
    # Documents et constructions des dix brevets blancs.
    plot('rev-bb1-corrige',[0,10,20,30,40],[0,50,100,150,200],'Temps (s)','Position (m)',annotate=lambda a:note(a,'200 m / 40 s = 5 m/s',(40,200),(3,165)),ylim=(0,230),xlim=(0,44))
    chain('rev-bb1-comparaison',[('Solution A','20 kWh\n50 g de CO₂ / kWh'),('Solution B','4 000 g de CO₂')],'Même trajet et indicateur fourni ; données fictives',False)
    chain('rev-bb1-carbone',[('A','20 × 50 = 1 000 g\n1,0 kg de CO₂'),('B','4 000 g\n4,0 kg de CO₂')],'A : quatre fois moins sur cet indicateur ; autres impacts à étudier')
    for corr in [False,True]:
        chain('rev-bb2-'+('masse-cor' if corr else 'masse-ex'),[('Récipient vide','32,0 g'),('Récipient rempli','82,0 g ; 50,0 mL'),('Liquide seul','50,0 g ; ρ = 1,00 g/mL' if corr else 'Masse à déterminer')],'La transparence et la masse volumique ne prouvent pas la potabilité' if corr else 'Pesées dans les mêmes conditions ; volume de liquide fourni',corr)
        test_bb2('rev-bb2-tests-'+('cor' if corr else 'ex'),corr)
        refuge('rev-bb3-'+('cor' if corr else 'ex'),corr)
    chain('rev-bb3-batterie',[('Réserve utilisable','36 Wh'),('Après 4 h à 6 W','24 Wh utilisés\n12 Wh encore disponibles')],'Autonomie théorique : 36 / 6 = 6 h')
    weights('rev-bb4-forces',19.2)
    echo('rev-bb4-radio-cor',True,True,2.56,300000)
    chain('rev-bb5-reaction',[('Réactifs','Fe + 2 H⁺'),('Produits','Fe²⁺ + H₂'),('Ion fer(II)','26 p⁺ ; 24 e⁻\nCharge +2')],'Le pH augmente de 2 à 4 ; le liquide reste acide')
    echo('rev-bb6-sonar-ex');echo('rev-bb6-sonar-cor',True)
    chain('rev-bb6-energie',[('Puissance','12 × 0,50 = 6 W'),('Durée','20 × 60 = 1 200 s'),('Énergie','6 × 1 200 = 7 200 J')],'Choisir W et s donne une énergie en J')
    energy('rev-bb7-bilan',5,3.5,1.5,'MJ','Atelier\nde recyclage')
    for corr in [False,True]:
        f,a=plt.subplots(figsize=(6.2,2));f.subplots_adjust(left=.13,right=.95,bottom=.26,top=.94)
        a.step([8,10,14,18],[0,200,0,0],where='post',color=N,lw=1.5);a.set(xlabel='Heure de la journée (h)',ylabel='Puissance (W)',xticks=[8,10,12,14,16,18],yticks=[0,100,200],ylim=(-10,250));a.grid(color=L)
        if corr:a.fill_between([10,14],0,200,color='#DCEBD7',zorder=0);note(a,'E = 200 × 4 = 800 Wh',(12,140),(8.5,225))
        save('rev-bb8-solaire-'+('cor' if corr else 'ex'),f,dict(P=200,duree=4,E_Wh=800,correction=corr))
    chain('rev-bb8-lampes',[('Ancienne lampe','40 W × 500 h\n20 kWh'),('Nouvelle lampe','8 W × 500 h\n4 kWh'),('Économie','16 kWh\n4,00 € au prix fourni')],'Mêmes durée et service d’éclairage ; comparaison limitée au poste énergie')
    gravity('rev-bb9-grav-ex','1,0 × 10⁶ m',False);gravity('rev-bb9-grav-cor','1,0 × 10⁶ m',True)
    chain('rev-bb9-lumiere',[('Étoile à 4 al','Source primaire\nÉmission il y a ≈ 4 ans'),('Observateur','Réception aujourd’hui')],'4 al = 3,784 × 10¹³ km ; la planète diffuse la lumière reçue')
    f,a=plt.subplots(figsize=(6.2,2));f.subplots_adjust(left=.13,right=.95,bottom=.26,top=.94)
    ii=np.array([0,.005,.01,.015,.02,.025]);a.plot(ii,200*ii,'o-',color=N,ms=3.5);a.set(xlabel='Intensité (A)',ylabel='Tension (V)',xlim=(0,.028),ylim=(0,6));a.grid(color=L);a.plot([.02,.02,0],[0,4,4],'--',color=G);note(a,'R = 4 / 0,020 = 200 Ω',(.02,4),(.001,5.4));save('rev-bb10-ohm-cor',f,dict(R=200,I=.02,U=4,P=.08))
    for corr in [False,True]:
        chain('rev-bb10-transfos-'+('cor' if corr else 'ex'),[('A : eau qui bout','Bulles de vapeur d’eau' if corr else 'Apparition de bulles'),('B : carbonate + acide','CO₂ identifié' if corr else 'Gaz : eau de chaux troublée')],'A : changement d’état ; B : nouvelles espèces ; les bulles seules ne suffisent pas' if corr else 'Pesée de B : 120,0 g avant ; 118,9 g après ; système ouvert',corr)
    (HERE/'build/figures-nouvelles.json').write_text(json.dumps(REGISTRY,ensure_ascii=False,indent=2),encoding='utf8')
    outside={n:d['textes_hors_cadre'] for n,d in REGISTRY.items() if d['textes_hors_cadre']}
    assert not outside,outside
    print(len(REGISTRY),'figures nouvelles ; textes dans le cadre')

if __name__=='__main__':produire()
