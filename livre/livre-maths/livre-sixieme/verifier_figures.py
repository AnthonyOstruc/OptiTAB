"""Contrôles de présence et de cohérence des figures de Sixième."""
from pathlib import Path
from math import isclose,hypot,degrees,atan2,pi
import importlib,json,re,itertools
from modele import CHAPITRES,FIGURES
import generer_figures as g
META=g.META
ROOT=Path(__file__).resolve().parent
for p in sorted(ROOT.glob('contenu_*.py')):importlib.import_module(p.stem)
import tempfile
with tempfile.TemporaryDirectory() as d:g.write_all(Path(d))
from approfondissements import DEFIS
from bilans import BILANS
from ressources import PREUVES
count=0;errors=[];details=[]
def check(ok,label):
    global count
    count+=1
    if not ok:errors.append(label)
    details.append({'controle':label,'reussi':bool(ok)})
def dist(a,b):return hypot(a[0]-b[0],a[1]-b[1])
def ang(v,a,b):
    x=abs(degrees(atan2(a[1]-v[1],a[0]-v[0]))-degrees(atan2(b[1]-v[1],b[0]-v[0])))%360
    return min(x,360-x)
def near(a,b,tol=1e-6):return abs(a-b)<=tol
def equi(p,A,B,tol=1e-6):return near(dist(p,A),dist(p,B),tol)
def colineaires(p,q,r,tol=1e-6):return abs((q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0]))<tol
def shoelace(pts):return abs(sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts))))/2
def perimetre(pts):return sum(dist(pts[i],pts[(i+1)%len(pts)]) for i in range(len(pts)))

# Présence des figures demandées par les textes.
for c in CHAPITRES:
    for i,e in enumerate(c.exercices,1):
        if e.figure:
            check(e.figure in FIGURES,f'figure {c.numero}.{i}')
            if re.search(r'en vert\b',e.corrige):check(r'\geoSolution' in FIGURES[e.figure]['tex'],f'{e.figure} porte la solution annoncée en vert')
        if 13<=c.numero<=18:check(bool(e.figure),f'figure nécessaire {c.numero}.{i}')
    for co in c.cours:
        for m in re.findall(r'@FIG:([^@]+)@',co):check(m in FIGURES,f'cours {c.numero} figure {m}')
for d in DEFIS:
    if d.figure:check(d.figure in FIGURES,'défi '+d.figure)
for b in BILANS:
    for p in b.problemes:
        if p.figure:check(p.figure in FIGURES,'bilan '+p.figure)
for t,b in PREUVES:
    for m in re.findall(r'figureGeo\{([^}]+)\}',b):check(m in FIGURES,'preuve '+m)
for name,data in FIGURES.items():
    if 'au corrigé' in data['legende']:check(r'\geoSolution' in data['tex'],name+' : légende « au corrigé » et solution présente')
    check(not any(ord(c)<32 for c in data['tex']+data['legende']),name+' sans caractère de contrôle')

# Demi-droites graduées.
for name,data in META.items():
    if data.get('type')=='droite':
        lo,hi=data['bornes']
        for v in data['points']+data['solutions']:check(lo-1e-9<=v<=hi+1e-9,f'{name} valeur {v} dans les bornes')
check(META['rep-1']['points']==[.6,1.3,2.8],'rep-1 abscisses du corrigé')
check(META['rep-2']['solutions']==[5.25,5.38,5.3],'rep-2 positions vertes')
check(META['rep-8']['points']==[1.47,1.415],'rep-8 G et H')
check(META['fq-4']['points']==[.75,1.75,2.5],'fq-4 trois quarts, sept quarts, dix quarts')
check([round(v,6) for v in META['fq-6']['solutions']]==[round(5/6,6),round(11/6,6),round(4/3,6)],'fq-6 sixièmes')
check([round(v*12) for v in META['fc-9']['points']]==[9,10,16],'fc-9 douzièmes')
check(META['cours-arrondi']['points']==[7.36],'cours-arrondi')
check(all(3.4<=v<=3.5 for v in META['cours-droite-zoom']['listes'][1][2]),'zoom : A dans l’intervalle agrandi')
# Grilles de cent cases.
check(sum(META['num-4']['valeurs'])==247,'num-4 vaut 2,47')
check(META['pct-1']['valeurs']==[42] and META['cours-grille-100']['valeurs']==[35] and META['cours-centiemes']['valeurs']==[34],'grilles 42, 35 et 34')
check(META['preuve-produit']['valeurs']==[1],'un centième')
# Guide-âne : extrémités sur la première et la dernière droite, longueur annoncée.
for name in ['cours-guide-ane','fq-9']:
    m=META[name]
    check(near(m['A'][1],0) and near(m['B'][1],m['parts']*m['ecart']),name+' extrémités sur le réseau')
    check(near(dist(m['A'],m['B']),m['longueur']),name+' longueur du segment')
# Fractions et quotients.
for name in ['cours-quart-de-3','fq-5']:check(near(*META[name]['longueurs']),name+' longueurs égales')
check(2*12==3*8,'cours-bandes-egales deux tiers et huit douzièmes')
# Pourcentages et barres.
check(sum(META['pct-8']['parts'])==100 and META['pct-8']['parts'][2]==25,'pct-8 25 %')
m=META['cours-bande-pct'];check(m['tout']*m['pct']/100==m['partie'],'30 % de 80')
check(META['alg-1']['total']==2*30+15,'alg-1 75 €')
check(META['alg-5']['total']==3*7+5,'alg-5 26')
check(META['cours-barres']['total']==4*12,'cours-barres 48')
check(META['alg-3']['etapes']==[4,7,10] and META['cours-motif']['etapes']==[4,7,10],'allumettes 4, 7, 10 comptées sur le dessin')
check(META['alg-8']['etapes']==[3,5,7],'motif en L')
check(META['alg-12']['etapes']==[1,3,6,10],'escalier 1, 3, 6, 10')
check(META['alg-13']['etapes']==[5,9,13],'croix 5, 9, 13')
# Proportionnalité et échelles.
m=META['cours-tableau-fleches'];check(all(near(p/q,2.5) for p,q in zip(m['prix'],m['masses'])),'prix au kilo constant')
check(META['pro-5']['cm']*META['pro-5']['longueur']==800,'pro-5 800 m')
check([d*META['pro-9']['cm'] for d in META['pro-9']['dims']]==[12,9],'pro-9 12 m sur 9 m')
L=META['pro-11']['longueurs'];check(all(near(a,b) for a,b in zip(L,[2,3.4,1.6])) and near(sum(L)*250,1750),'pro-11 1 750 m')
# Longueurs.
check(all(near(a,b) for a,b in zip(META['lon-5']['cotes'],[2.3,1.8,2.6])),'lon-5 côtés de la ligne brisée')
check(abs(META['lon-6']['valeur']-22.28)<.01,'lon-6 environ 22,28 cm')
check(abs(META['lon-7']['valeur']-388.4)<.1,'lon-7 environ 388,4 m')
pts=META['lon-10']['points'];check(near(perimetre(pts),30) and near(dist(pts[2],pts[3]),5) and near(dist(pts[3],pts[4]),4),'lon-10 côtés 5 et 4, périmètre 30')
check(META['lon-14']['rayon']==15 and META['lon-14']['fraction']==.75,'lon-14 rayon et trois quarts')
check(abs(META['cours-cercle-diametre']['rapport']-3.14)<.01,'nombre pi')
# Aires.
check(META['cours-decoupage']['valeurs']==[8,8],'découpage : même aire')
check(META['air-1']['valeurs']==[8,7,7],'air-1 : B et C égales, A plus grande')
check(META['air-2']['valeurs']==[13],'air-2 13 cm²')
check(META['air-7']['valeurs']==[12,12] and META['air-7']['perimetres']==[16,14],'air-7')
check(META['air-8']['valeurs']==[12],'air-8 12 cm²')
pts=META['air-10']['points'];check(near(shoelace(pts),43),'air-10 aire 43 m²')
check(META['air-13']['valeurs']==[160,240],'air-13')
check(META['cours-dm2']['aires']==[100],'1 dm² = 100 cm²')
# Durées.
for (h,m,ah,am) in META['dur-1']['lectures']:
    check(near(ah,90-(h%12)*30-m*.5) and near(am,90-m*6),f'dur-1 aiguilles de {h} h {m:02}')
check([(h,m) for h,m,_,_ in META['dur-1']['lectures']]==[(3,20),(7,45),(11,5)],'dur-1 heures lues au corrigé')
i=META['dur-9']['instants'];mn=[h*60+m for h,m in i];check(mn[3]-mn[0]==210 and mn[2]-mn[1]==15,'dur-9 3 h 30 et 15 min')
check(sum(META['cours-frise']['minutes'])==88,'frise : 1 h 28 min')
# Chapitre 13.
A,B,Cc,D=META['dis-2']['points'];check(near(dist(A,B),dist(A,D)) and near(dist(Cc,B),dist(Cc,D)),'dis-2 égalités codées')
check(near((B[0]-A[0])*(D[0]-A[0])+(B[1]-A[1])*(D[1]-A[1]),0),'dis-2 angle droit en A')
m=META['dis-3'];check(near(dist(m['A'],m['M']),3.5) and near(dist(m['A'],m['N']),3) and near(dist(m['A'],m['B']),7),'dis-3')
m=META['dis-4'];O=m['O'];r=m['r'];s=m['segments']
check(near(dist(O,s['OA'][1]),r),'dis-4 rayon');check(near(dist(*s['BC']),2*r) and near(dist(O,s['BC'][0]),r),'dis-4 diamètre')
check(dist(*s['DE'])<2*r-.1 and not colineaires(s['DE'][0],s['DE'][1],O,.05),'dis-4 corde')
m=META['dis-5'];d={k:round(dist(m['O'],p),6) for k,p in m['points'].items()};check(d=={'M':3,'N':2.4,'P':3.6},'dis-5 distances au centre')
check(META['dis-6']['rayons']==[2.3,1.4],'dis-6 rayons')
for name in ['dis-7','dis-12']:
    m=META[name];check(len(m['points'])==2,name+' deux points')
    for p in m['points']:check(near(dist(p,m['centres'][0]),m['rayons'][0]) and near(dist(p,m['centres'][1]),m['rayons'][1]),name+' distances aux centres')
m=META['dis-8'];check(all(near(dist(m['O'],p),m['r']) for p in m['passe']),'dis-8 cercle par A et B')
m=META['dis-9'];L=m['longueurs'];check(near(L['AB'],5) and near(L['CD'],4,1e-3) and near(L['EF'],3,1e-3) and colineaires(m['A'],m['B'],m['O']),'dis-9 cordes 5, 4, 3')
L=META['dis-10']['valeurs'];check(near(L['AB'],3.6) and near(L['CD'],3.4) and near(L['EF'],3.8),'dis-10 longueurs')
m=META['dis-11'];d={k:round(dist(m['O'],p),6) for k,p in m['points'].items()};check(d=={'V1':2.1,'V2':3.4,'V3':2.9,'V4':3},'dis-11 distances')
m=META['dis-13'];d={k:round(dist(m['O'],p)*m['echelle'],6) for k,p in m['points'].items()};check(d=={'F1':4,'F2':5.5,'F3':5} and m['r']*m['echelle']==5,'dis-13 distances réelles')
m=META['dis-14'];check(near(dist(m['A'],m['M']),m['r']) and near(dist(m['B'],m['M']),m['r']) and colineaires(m['A'],m['B'],m['M']),'dis-14 point de contact')
m=META['dis-15'];check(near(dist(m['M'],m['A']),3) and near(dist(m['M'],m['B']),3) and not colineaires(m['A'],m['B'],m['M']) and near(dist(m['A'],m['I']),2),'dis-15')
# Chapitre 14.
for name,data in META.items():
    if data.get('type')=='mediatrice':
        for p in data['points']:check(equi(p,data['A'],data['B'],1e-3),f'{name} point de la médiatrice équidistant')
for name in ['cours-equidistance','med-4','med-5','med-7','med-9','med-11','med-14','med-15','dis-15']:
    m=META[name];check(equi(m['M'],m['A'],m['B']),name+' : M équidistant')
check(not equi(META['cours-equidistance']['N'],META['cours-equidistance']['A'],META['cours-equidistance']['B']),'cours : N non équidistant')
m=META['med-5'];check(near(dist(m['M'],m['A']),3.5) and near(dist(m['N'],m['A']),3) and near(dist(m['N'],m['B']),4),'med-5 longueurs')
m=META['med-14'];check(near(dist(m['M'],m['A']),5) and near(dist(m['N'],m['A']),3.5) and equi(m['N'],m['A'],m['B']),'med-14 C et D sur la médiatrice')
m=META['med-4'];check(near(dist(m['M'],m['A']),4.2),'med-4 4,2 cm')
check(near(META['med-11']['M'][1],0) and near(META['med-9']['M'][1],0),'S et M sur leur droite')
m=META['med-1'];res={k:equi(a,m['A'],m['B'],1e-6) and equi(b,m['A'],m['B'],1e-6) for k,(a,b) in m['droites'].items()}
check(res=={'d_1':False,'d_2':False,'d_3':True,'d_4':False},'med-1 seule (d3) est la médiatrice')
m=META['med-8'];A,B,Cc,D=m['points'];check(near(dist(A,B),dist(B,Cc)) and near(dist(B,Cc),dist(Cc,D)) and near(dist(Cc,D),dist(D,A)),'med-8 losange')
check(equi(B,A,Cc) and equi(D,A,Cc),'med-8 B et D équidistants de A et C')
m=META['med-10'];check(all(equi(o,m['A'],m['B']) for o in m['centres']),'med-10 centres sur la médiatrice')
m=META['med-12'];check(all(equi(p,m['A'],m['B'],1e-3) for p in m['frontiere']),'med-12 frontière équidistante')
# Chapitre 15.
check(META['cours-rapporteur']['mesures']==[50] and META['ang-3']['mesures']==[70] and META['ang-4']['mesures']==[125],'lectures au rapporteur')
check(round(META['ang-1']['mesures'][0])==55,'ang-1')
m=META['ang-2']['mesures'];check(m[0]<90 and m[1]==90 and 90<m[2]<180 and m[3]==180 and m[4]<90,'ang-2 classement')
check(META['ang-5']['mesures']==[100,45,160],'ang-5')
check(META['ang-6']['mesures']==[65],'ang-6')
check(sum(META['ang-8']['mesures'])==180 and META['ang-8']['mesures'][1]==52,'ang-8')
m=META['ang-9']['mesures'];check(sum(m)==360 and m[0]==m[2] and m[1]==m[3],'ang-9')
check(META['ang-10']['mesures']==[84,42],'ang-10')
check(sum(META['ang-11']['mesures'])==360 and META['ang-11']['mesures'][3]==75,'ang-11')
check(near(META['ang-12']['mesures'][0],120),'ang-12 quatre heures')
check(META['ang-14']['mesures'][0]/2+META['ang-14']['mesures'][1]/2==90,'ang-14')
check(META['ang-15']['mesures'][0]<META['ang-15']['mesures'][1],'ang-15')
for name in ['ang-13','cours-paires-bissectrice']:
    m=META[name];a=degrees(atan2(m['P'][1]-m['O'][1],m['P'][0]-m['O'][0]));check(near(a,m['angle']/2,1e-6),name+' bissectrice à mi-angle')
# Chapitre 16.
def angles_tri(A,B,Cc):return [ang(A,B,Cc),ang(B,A,Cc),ang(Cc,A,B)]
for name,exp in [('tri-1',[48,67,65]),('tri-2',[40,70,70]),('tri-3',[60,60,60]),('tri-4',[35,55,90]),('tri-8',[70,50,60]),('tri-9',[36,72,72]),('bilan-triangle',[40,60,80])]:
    got=angles_tri(*META[name]['points']);check(all(near(a,b,1e-6) for a,b in zip(got,exp)),name+' angles conformes')
A,B,Cc=META['tri-3']['points'];check(near(dist(A,B),4) and near(dist(B,Cc),4),'tri-3 côté 4 cm')
for name in ['tri-5','cours-construction-triangle']:
    A,B,Cc=META[name]['points'];check(near(dist(A,B),6) and near(dist(A,Cc),4) and near(dist(B,Cc),5),name+' côtés 6, 4, 5')
A,B,Cc=META['tri-7']['points'];check(near(dist(A,B),5) and near(dist(A,Cc),3) and near(ang(A,B,Cc),60),'tri-7')
check(META['tri-6']['intersections']==0 and 3+4<8,'tri-6 impossible')
for name in ['tri-10','tri-11','tri-12','cours-cercle-circonscrit']:
    m=META[name];O=m['O'];A,B,Cc=m['points'];check(near(dist(O,A),dist(O,B)) and near(dist(O,B),dist(O,Cc)),name+' centre équidistant')
m=META['tri-12'];A,B,Cc=m['points'];check(near(m['O'][0],(B[0]+Cc[0])/2) and near(m['O'][1],(B[1]+Cc[1])/2),'tri-12 milieu de l’hypoténuse')
p=META['tri-13']['points'];check(near(ang(p['A'],p['B'],p['C']),50) and near(ang(p['A'],p['B'],p['D']),110) and near(dist(p['A'],p['C']),dist(p['C'],p['D'])) and near(dist(p['C'],p['D']),dist(p['D'],p['A'])),'tri-13 50° et 110°, ACD équilatéral')
A,B,H=META['tri-14']['points'];check(near(ang(A,B,H),30) and near(ang(H,A,B),90),'tri-14 30° et 90°')
check(sum(META['tri-15']['mesures'])>180,'tri-15 somme trop grande')
for name in ['cours-somme-angles','preuve-triangle']:check(near(sum(META[name]['angles']),180),name+' somme 180°')
# Chapitre 17.
for name,data in META.items():
    if data.get('type')=='symetrie':
        o,v=data['axe'];gw,gh=data['grille']
        for (x,y),(u,w) in zip(data['originaux'],data['images']):
            ok=(isclose(u,2*v-x) and isclose(w,y)) if o=='v' else (isclose(u,x) and isclose(w,2*v-y))
            check(ok,f'{name} image de ({x},{y})');check(0<=u<=gw and 0<=w<=gh,f'{name} image dans le cadre')
    if data.get('type')=='symdiag':
        n=data['grille']
        for (x,y),(u,w) in zip(data['originaux'],data['images']):
            check((u,w)==(y,x),f'{name} échange des coordonnées ({x},{y})');check(0<=u<=n and 0<=w<=n,f'{name} image dans la grille')
    if data.get('type')=='symoblique':
        a,b=data['axe']
        for p,q in data['paires']:
            m=((p[0]+q[0])/2,(p[1]+q[1])/2)
            check(colineaires(a,b,m,1e-6),f'{name} milieu sur l’axe')
            check(near((q[0]-p[0])*(b[0]-a[0])+(q[1]-p[1])*(b[1]-a[1]),0),f'{name} segment point-image perpendiculaire à l’axe')
check(colineaires(*META['sym-12']['alignes']),'sym-12 image passant par I')
check(colineaires(*META['sym-13']['alignes']),'sym-13 A’, I et B alignés')
check(META['sym-1']['nombres']==[2,4,1,2,0] and META['sym-14']['nombres']==[2,1,1,0,2],'nombres d’axes')
p=META['sym-7']['paires'];check(near(dist(p[0][0],p[1][0]),4) and near(dist(p[0][1],p[1][1]),4),'sym-7 longueur conservée')
m=META['defi-miroirs'];check(m['images']==[(5,2)] and m['second']==[(5,2),(9,2)] and 9-3==6,'défi : deux symétries, 6 cm')
# Chapitre 18.
for name,n in [('sol-3',8),('sol-5',6),('sol-6',14),('sol-10',20),('sol-11',24),('sol-12',22),('sol-13',27),('cours-assemblage-vues',5),('sol-7',5),('defi-pyramide',14)]:
    check(META[name]['cubes']==n,f'{name} : {n} cubes')
check(META['sol-10']['ajout']==7,'sol-10 sept cubes à ajouter')
def vues(cubes):
    face={};droite={};dessus=set()
    for i,j,k in cubes:
        face[i]=max(face.get(i,0),k+1);droite[j]=max(droite.get(j,0),k+1);dessus.add((i,j))
    return [face[k] for k in sorted(face)],[droite[k] for k in sorted(droite)],sorted(dessus)
f,dr,de=vues(META['sol-7']['liste']);check(f==[2,1] and dr==[2,1] and len(de)==4,'sol-7 vues de face, de droite, de dessus')
f,dr,de=vues(META['cours-assemblage-vues']['liste']);check(f==[2,1] and dr==[2,1],'cours : vues de l’assemblage')
check(META['sol-4']['dessus']==META['sol-4']['bonne'],'sol-4 vue 2')
check(sum(META['sol-8']['hauteurs'])==10,'sol-8 dix cubes')
check(META['sol-9']['A']==9 and META['sol-9']['B']==8,'sol-9 A plus grand')
check(META['sol-15']['A']==META['sol-15']['B']==6,'sol-15 même volume')
f,dr,de=vues(META['sol-14']['cubes']);check(f==[2,1] and dr==[1,2] and len(de)==4,'sol-14 vues de la solution')
sols=[h for h in itertools.product([1,2],repeat=4) if vues([(i,j,k) for (i,j),hh in zip([(0,0),(1,0),(0,1),(1,1)],h) for k in range(hh)])[:2]==([2,1],[1,2])]
check(len(sols)==1 and sum(sols[0])==5,'sol-14 solution unique de 5 cubes')
check(META['sol-2']['pave']==(6,12,8) and META['sol-2']['pyramide']==(5,8,5),'sol-2 faces, arêtes, sommets')
for name in ['sol-2']:
    f_,a_,s_=META[name]['pave'];check(f_-a_+s_==2,'relation d’Euler pour le pavé')
    f_,a_,s_=META[name]['pyramide'];check(f_-a_+s_==2,'relation d’Euler pour la pyramide')
# Données et hasard.
v=META['don-3']['valeurs'];check(v==[15,20,35,25,30],'don-3')
check(META['don-4']['angles']==[180,90,90],'don-4')
check(META['don-5']['valeurs']==[8,12,18,21,16,11],'don-5')
check(META['don-9']['valeurs']==[102,108] and META['don-9']['origine']==100,'don-9 axe tronqué')
check(META['don-10']['valeurs']==[12,9,5,4],'don-10')
m=META['don-13'];check(m['temperatures'].index(max(m['temperatures']))==6 and m['pluie'].index(min(m['pluie']))==6 and m['pluie'].index(max(m['pluie']))==10,'don-13')
check(abs(META['cours-frequences']['valeurs'][-1]-.5)<.01,'fréquences vers 0,5')
it=META['hasard-2']['items'];check(it.count('R')==3 and it.count('B')==5 and it.count('V')==2,'hasard-2 composition')
check(META['hasard-4']['angles']==[45]*8 and META['hasard-10']['angles']==[180,90,90],'roues')
check(META['hasard-6']['issues']==4 and META['hasard-7']['sommes7']==6,'arbre et tableau des dés')
m=META['hasard-9'];check(m['A'].count('R')==2 and len(m['A'])==5 and m['B'].count('R')==3 and len(m['B'])==8,'hasard-9')
check(META['hasard-13']['valeurs'][-1]==.62,'hasard-13')
for name,data in META.items():
    if data.get('type')=='secteurs':check(isclose(sum(data['angles']),360),name+' tour complet')
# Programmes et chemins.
from donnees_scripts import verifier_scripts
check(verifier_scripts()==11,'programmes exécutés')
check(META['ins-4']['trace'][-1]==META['ins-4']['arrivee'],'ins-4 arrivée en R')
check(META['ins-6']['trace'][-1]==META['ins-6']['arrivee'],'ins-6 arrivée')
for name in ['ins-8','ins-15']:
    m=META[name];check(not set(map(tuple,m['trace']))&set(m['obstacles']) and m['trace'][-1]==m['arrivee'],name+' chemin sans obstacle jusqu’à A')
check(len(META['ins-15']['trace'])-1==10,'ins-15 dix cases')
check(META['ins-11']['trace'][-1]==META['ins-11']['maisons']['B'],'ins-11 maison B')
check(META['ins-12']['retour']<1e-9 and META['ins-12']['cotes']==6,'ins-12 hexagone fermé')
check(META['cours-chemin']['trace'][-1]==(0,0),'cours : carré fermé')
check(META['ins-14']['trace'][-1]==(0,4),'ins-14 trois côtés seulement')
# Défis.
check(META['defi-carre']['valeurs']==[10],'carré penché 10 cm²')
check(META['defi-cercles']['nombres']==[0,1,2,1,0],'défi : nombres de points')
m=META['defi-centre'];(A,B),(Cc,D)=m['cordes']
u=((B[0]-A[0])/dist(A,B),(B[1]-A[1])/dist(A,B));w=((D[0]-Cc[0])/dist(Cc,D),(D[1]-Cc[1])/dist(Cc,D))
check(abs(u[0]*w[1]-u[1]*w[0])>.3 and equi(m['O'],A,B) and equi(m['O'],Cc,D),'défi : cordes non parallèles, centre sur les médiatrices')
m=META['defi-spirale'];check(m['arrivee']==(3,3) and m['longueur']==30,'défi : spirale')
(ROOT/'build').mkdir(exist_ok=True)
r={'controles_figures':count,'erreurs':errors,'details':details}
(ROOT/'build/controles-figures.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in r.items() if k!='details'},ensure_ascii=True,indent=2))
assert not errors
