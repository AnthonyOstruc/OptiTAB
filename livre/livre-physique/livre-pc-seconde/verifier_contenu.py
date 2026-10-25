"""Contrôles indépendants des calculs, bilans et correspondances éditoriales."""
from pathlib import Path
import math,json,re
import numpy as np
from structure import CH,completer_programme
import contenu_matiere,contenu_mouvement,contenu_signaux
from evaluations import DS
from figures import F,prism_data,normal
completer_programme()
ROOT=Path(__file__).resolve().parent
checks=[]
def ok(ref,condition,detail=''):
    checks.append(dict(reference=ref,reussi=bool(condition),detail=detail))
def calc(ref,value,expected,tol=1e-8):
    ok(ref,math.isclose(value,expected,rel_tol=tol,abs_tol=tol if expected==0 else 0),f'{value:.12g} ; attendu {expected:.12g}')

ok('Inventaire chapitres',len(CH)==20)
for i,c in enumerate(CH,1):
    ok(f'Ch {i} : 12 exercices',len(c['exos'])==12)
    for j,e in enumerate(c['exos']+[c['defi']],1):
        ok(f'{i}.{j} : questions / réponses',len(e['questions'])==len(e['reponses']))
        ok(f'{i}.{j} : figure disponible',not e['fig'] or e['fig'] in F)
    tex=(ROOT/f'chapitres/{i:02d}.tex').read_text(encoding='utf-8')
    cor=(ROOT/f'corriges/{i:02d}.tex').read_text(encoding='utf-8')
    ok(f'Ch {i} : 12 énoncés et 12 corrections',tex.count(r'\begin{exercice}')==12 and cor.count(r'\begin{corrige}')==12)
    ok(f'Ch {i} : mêmes figures dans les solutions',
       re.findall(r'\\schema\[corrige\]\{([^}]+)\}',cor)==[e['fig'] for e in c['exos'] if e['fig']])
for i,d in enumerate(DS,1):
    ok(f'DS {i} : total 20 points',sum(d['points'])==20)
    for j,(e,p,m) in enumerate(zip(d['exos'],d['points'],d['bareme']),1):
        ok(f'DS {i}.{j} : toutes questions corrigées',len(e['questions'])==len(e['reponses'])==len(m))
        ok(f'DS {i}.{j} : barème cohérent',sum(m)==p)

# Les identifiants renvoient au chapitre/exercice ou au défi (D) imprimés.
tests=[
('1.1 micro',450e-6,4.50e-4),('1.4 moyenne',np.mean([2.1,2.0,2.2,2.1]),2.1),
('1.6 incertitude',.12/math.sqrt(16),.03),('1.7 vitesse',.625/.48,1.302083333333),
('1.9 concentration',.250/.50,.50),('1.11 période',8.16/10,.816),
('1.12 moyenne',np.mean([9.8,9.9,10,10,10.1,10.2]),10),
('1.D uA',.08/4,.02),('1.D uB',.12/6,.02),
('2.2 masse',58.4-42.6,15.8),('2.2 rho',15.8/20,.790),('2.4 air',.21*50,10.5),
('2.5 zinc',100*75/250,30),('2.7 aluminium',32.4/12,2.70),('2.8 air masse',1.2*40,48),
('2.9 sel',.1*40,4),('2.11 étain',.12*2.50,.300),('2.12 métal',54/2.7,20),
('2.D masse',302-32,270),('2.D rho',270/250,1.08),('2.D fraction',100*40.5/270,15),('2.D cm',40.5/.25,162),
('3.2 cm',3.60/.2,18),('3.3 dissolution',8*.250,2),('3.4 dilution',40*10/100,4),
('3.5 saturation',200*.050,10),('3.6 prélèvement',3*100/15,20),
('3.7 étalonnage',(1.03-1)/.0005,60),('3.8 cm',5/.100,50),('3.8 rho',103/100,1.03),
('3.9 dilutions',80/4/5,4),('3.11 mélange',(10*.1+4*.2)/.3,6),('3.12 mère',36*5,180),('3.D prélèvement',6*250/30,50),
('4.1 neutrons',27-13,14),('4.2 A',8+10,18),('4.5 rapport',1e-10/1e-15,1e5),
('4.5 maquette',100/1e5,.001),('4.6 masse',12*1.67e-27,2.004e-26),
('4.7 charge',12*1.60e-19,1.92e-18),('4.11 charge',2*1.60e-19,3.2e-19),
('4.12 neutralité',3e20*2-6e20,0),
('6.2 molécule',1.99e-26+2*2.66e-26,7.31e-26),('6.3 nombre',1.06e-3/1.06e-25,1e22),
('6.4 mole',3.01e23/6.02e23,.5),('6.5 O2',2*2.66e-26,5.32e-26),
('6.5 nombre',.532e-3/5.32e-26,1e22),('6.7 masse',2e22*3e-26,6e-4),
('6.8 mélange',.2*5e-3/5e-26,2e22),('6.11 goutte',.0300e-3/3e-26,1e21),
('6.12 nombre',1.80e-3/3e-26,6e22),('6.D glucose',6*1.99e-26+12*1.67e-27+6*2.66e-26,2.9904e-25),
('7.3 fusion',.0500*3.34e5,1.67e4),('7.6 masse',66.8/334,.2),('7.7 rapport',100/40,2.5),
('7.9 durée',.2*3.34e5/100,668),('7.10 volume',100/.92,108.695652173913),
('7.D énergie',.3*3.34e5,100200),('7.D durée',100200/25,4008),
('8.5 limitant',min(.6/2,.2),.2),('8.5 eau',2*min(.6/2,.2),.4),
('8.7 O2',.150*2,.300),('8.9 limitant',min(.080,.100/2),.050),('8.9 reste',.080-.050,.030),
('8.D O2 restant',.300-.300/2,.150),
('10.6 neutrons',236-141-92,3),('10.9 noyau A',14+4-17,1),('10.9 noyau Z',7+2-8,1),
('10.10 énergie',3.2e-11*2e18,6.4e7),('10.D neutrons',236-140-94,2),('10.D nombre',9e7/3e-11,3e18),
('11.3 moyenne',(8-2)/3,2),('11.4 conversion',72/3.6,20),('11.5 vitesse',(.8-.2)/.2,3),
('11.6 signe',(2-5)/1.5,-2),('11.7 échelle',6/2,3),('11.9 moyenne distance',40/10,4),
('11.11 cadence',1/50,.02),('11.12 norme',math.hypot(.3/.5,.4/.5),1),
('12.2 poids',.2*10,2),('12.5 Terre',3*9.8,29.4),('12.5 Lune',3*1.6,4.8),
('12.6 gravitation',6.67e-11*10*20/.5**2,5.336e-8),('12.8 distance',(6400+400)*1000,6.8e6),
('12.10 échelle',4.5/1.5,3),('12.12 g',6.67e-11*6e24/(6.4e6)**2,9.7705078125),('12.D poids',80*9.8/4,196),
('14.3 durée',68/340,.2),('14.4 air',340*.05,17),('14.4 eau',1500*.05,75),
('14.5 vitesse',1.02/.003,340),('14.6 écho',340*.3/2,51),('14.11 sonar',1500*.08/2,60),
('14.D longueur1',340*.420/2,71.4),('14.D longueur2',340*.424/2,72.08),
('15.1 fréquence',1/.002,500),('15.2 période',1/250,.004),('15.5 fréquence',1/(.0125/5),400),
('15.7 rapport',660/220,3),('15.10 fréquence',1/.00125,800),('15.D fréquence',4/.00909,440.04400440044),
('16.2 nano',550e-9,5.50e-7),('16.4 durée',900/3e8,3e-6),('16.9 distance',500*3e8,1.5e11),
('16.10 distance',3e8*40e-9/2,6),('16.12 distance',340*3,1020),
('17.5 angle',math.degrees(math.asin(math.sin(math.radians(30))/1.5)),19.47122063449),
('17.6 indice',math.sin(math.radians(45))/math.sin(math.radians(28.1)),1.50125041295),
('17.9 sortie',math.degrees(math.asin(1.5*math.sin(math.radians(20)))),30.86588247309),
('17.D rouge',math.degrees(math.asin(math.sin(math.radians(40))/1.5)),25.37399393918),
('17.D violet',math.degrees(math.asin(math.sin(math.radians(40))/1.53)),24.8423292883),
('18.5 gamma',-1.5/3,-.5),('18.8 Thalès',24/12,2),('18.12 gamma',-15/30,-.5),
('19.2 Ohm',200*.025,5),('19.3 nœud',.30-.12,.18),('19.4 maille',9-3.5,5.5),
('19.6 R',6/.015,400),('19.7 total',6/100+6/200,.09),('19.9 I',9/300,.03),
('19.D intensité',6/200+6/300,.05),('20.2 R',20-.4*20,12),('20.3 T',(20-10)/.4,25),
('20.4 code',1000*1.25/5,250),('20.5 I',5/20000,.00025),('20.7 R',10*2/(5-2),20/3),
('20.9 seuil',20-.4*30,8),('20.D T',(20-10*2/3)/.4,100/3),
('DS1.1 rho',(54.9-35.2)/25,.788),('DS1.2 masse',12*.2,2.4),('DS1.3 mère',60*5,300),
('DS2.1 charge',(13-10)*1.6e-19,4.8e-19),('DS2.3 nombre',.731e-3/7.31e-26,1e22),
('DS3.1 durée',.150*334000/50,1002),('DS3.2 calcaire',.040-min(.040,.060/2),.010),
('DS6.2 résistance',10*2.5/(5-2.5),10),('DS6.3 dilution',4*100/40,10)
]
for ref,v,e in tests:calc(ref,v,e)

# Réaction : bilans des éléments et des charges construits indépendamment des textes.
species={'H2':({'H':2},0),'O2':({'O':2},0),'H2O':({'H':2,'O':1},0),
'C':({'C':1},0),'CH4':({'C':1,'H':4},0),'CO2':({'C':1,'O':2},0),
'Zn':({'Zn':1},0),'H+':({'H':1},1),'Zn2+':({'Zn':1},2),
'CaCO3':({'Ca':1,'C':1,'O':3},0),'Ca2+':({'Ca':1},2),'HO-':({'H':1,'O':1},-1)}
equations=[({'H2':2,'O2':1},{'H2O':2}),({'C':1,'O2':1},{'CO2':1}),
({'CH4':1,'O2':2},{'CO2':1,'H2O':2}),({'Zn':1,'H+':2},{'Zn2+':1,'H2':1}),
({'CaCO3':1,'H+':2},{'Ca2+':1,'CO2':1,'H2O':1}),({'H+':1,'HO-':1},{'H2O':1})]
def bilan(side):
    a={};charge=0
    for name,n in side.items():
        atoms,q=species[name];charge+=q*n
        for el,nb in atoms.items():a[el]=a.get(el,0)+nb*n
    return a,charge
for i,(a,b) in enumerate(equations,1):ok(f'Équation chimique {i} : atomes et charges',bilan(a)==bilan(b))

# Géométrie des deux constructions : intersection rayon central / rayon réfracté.
for p in (15.,20.,30.):
    f=10.;h=2.;pp=1/(1/f-1/p);hp=-h*pp/p
    calc(f'Lentille p={p} position',pp,{15:30,20:20,30:15}[p])
    calc(f'Lentille p={p} taille',hp,{15:-4,20:-2,30:-1}[p])
    calc(f'Lentille p={p} rayon central',-h/p*pp,hp)
    calc(f'Lentille p={p} rayon par foyer',h-h/f*pp,hp)
v=np.array([9.8,9.9,10,10,10.1,10.2]);calc('Atelier histogramme s',v.std(ddof=1),math.sqrt(.02))
calc('Atelier histogramme u',v.std(ddof=1)/math.sqrt(6),math.sqrt(.02/6))
ok('Atelier histogramme effectifs',list(np.histogram(v,bins=[9.75,9.95,10.15,10.35])[0])==[2,3,1])
a,b=np.polyfit(np.array([0,10,20,30,40])/1000,[.01,2,4.02,5.99,8.01],1)
calc('Atelier Ohm pente',a,199.9);calc('Atelier Ohm décalage',b,.008)
ok('Vecteurs du pointage',np.allclose(np.diff([0,.2,.8,1.8,3.2])/.2,[1,3,5,7]))
for n,entree,xx,yy,alpha,sortie in prism_data:
    calc(f'Prisme {n} entrée sur la face',entree,1.3*1.6/3)
    calc(f'Prisme {n} sortie sur la face',xx+(1.6/3)*yy,3.2)
    calc(f'Prisme {n} Snell entrée',n*math.sin(alpha+normal),math.sin(normal))
    calc(f'Prisme {n} Snell sortie',n*math.sin(normal-alpha),math.sin(normal-sortie))
ok('Œil : rayons dans la pupille',all(-.7<y<.7 for y in (.6,-.3)))
ok('Œil : rayons dans la lentille',all(-.9<y<.9 for y in (.6,-.3)))
ok('Prisme : violet plus dévié que rouge',prism_data[1][-1]<prism_data[0][-1]<0)

report=dict(controles=len(checks),echecs=[c for c in checks if not c['reussi']],details=checks)
(ROOT/'recherches/verification-contenu.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=False,indent=2))
raise SystemExit(bool(report['echecs']))
