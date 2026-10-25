"""Vérifications indépendantes des résultats des 210 exercices et des blocs Python."""
from pathlib import Path
from itertools import product
from collections import defaultdict
import json,math,re,statistics
import sympy as S
q=S.Rational
R=Path(__file__).resolve().parent
(R/'build').mkdir(exist_ok=True)
x,n,m,h,a=S.symbols('x n m h a',real=True)
results=defaultdict(list)
def eq(u,v): return S.simplify(u-v)==0
def close(u,v,tol=1e-6): return abs(float(u)-float(v))<=tol
def case(c,e,label,*conditions):
    assert all(bool(t) for t in conditions),(c,e,label,conditions)
    results[f'{c}.{e}'].append(label)
def roots(p): return set(S.solve(p,x))
def dot(u,v): return sum(S.sympify(i)*j for i,j in zip(u,v))
def norm2(u): return dot(u,u)
def moments(v,p):
    p=[S.Rational(str(pi)) for pi in p]; mu=sum(S.sympify(vi)*pi for vi,pi in zip(v,p))
    return mu,S.simplify(sum(S.sympify(vi)**2*pi for vi,pi in zip(v,p))-mu**2)

# Chapitres 1 à 5 : calculs exacts, domaines et seuils.
case(1,1,'degrés et coefficients',S.Poly(3*x*x-2*x+5,x).all_coeffs()==[3,-2,5],S.Poly((x-2)**2,x).all_coeffs()==[1,-4,4])
case(1,2,'développements et facteurs',eq((x-3)*(x+2),x*x-x-6),eq(2*(x-1)**2-8,2*x*x-4*x-6),eq(x*x-25,(x-5)*(x+5)),eq(3*x*x-12*x,3*x*(x-4)))
case(1,3,'sommet et racines',roots(2*(x-3)**2-8)=={1,5},eq((2*(x-3)**2-8).subs(x,0),10))
case(1,4,'trois discriminants',roots(x*x-5*x+6)=={2,3},roots(x*x+4*x+4)=={-2},S.discriminant(2*x*x+x+2,x)==-15)
case(1,5,'signes aux intervalles séparés par les racines',[-2*(k+1)*(k-4)>0 for k in [-2,0,5]]==[False,True,False])
case(1,6,'formes et trois résolutions',eq(x*x-6*x+5,(x-3)**2-4),roots(x*x-6*x)=={0,6},roots(x*x-6*x+8)=={2,4})
case(1,7,'intersections et position',roots((x*x-4*x+3)-(-x*x+2*x+3))=={0,3},eq(2*x*x-6*x,2*x*(x-3)))
case(1,8,'quotient et changements de signe',eq((x*x-5*x+6)/(x-1),(x-2)*(x-3)/(x-1)),[S.sign(((x-2)*(x-3)/(x-1)).subs(x,k)) for k in [0,S.Rational(3,2),S.Rational(5,2),4]]==[-1,1,-1,1])
case(1,9,'parabole reconstruite',eq((x+2)*(x-4),(x-1)**2-9),roots((x+2)*(x-4)+5)=={-1,3})
case(1,10,'sommes et produits des racines',roots(x*x-7*x+10)=={2,5},S.discriminant(x*x-4*x+5,x)==-4,eq(x*x+x-12,(x+4)*(x-3)))
case(1,11,'paramètre et minimum',eq(x*x-4*x+m,(x-2)**2+m-4),S.discriminant(x*x-4*x+m,x)==16-4*m)
case(1,12,'jardin, maximum et seuil',eq(x*(40-2*x),-2*(x-10)**2+200),roots(x*(40-2*x)-150)=={5,15})
case(1,13,'recette, bénéfice et seuils',eq(x*(50-x/5)-(10*x+500),-(x-100)**2/5+1500),roots(-x*x/5+40*x-500)=={100-50*S.sqrt(3),100+50*S.sqrt(3)})
case(1,14,'trajectoire, sol et filet',eq(-5*x*x+10*x+1,-5*(x-1)**2+6),roots(-5*x*x+10*x+1)=={1-S.sqrt(30)/5,1+S.sqrt(30)/5},eq((-5*x*x+10*x+1).subs(x,S.Rational(3,2)),S.Rational(19,4)),roots(-5*x*x+10*x-3)=={1-S.sqrt(10)/5,1+S.sqrt(10)/5})
case(1,15,'famille et point commun',eq(S.discriminant(x*x-2*m*x+m+2,x),4*(m-2)*(m+1)),eq((x*x-2*m*x+m+2).subs(x,S.Rational(1,2)),S.Rational(9,4)),roots(x*x-6*x+5)=={1,5})

case(2,1,'termes et différence',[(k*k-3*k+2) for k in [0,1,2,5]]==[2,0,0,12],eq(((n+1)**2-3*(n+1)+2)-(n*n-3*n+2),2*n-2))
v=2; seq=[v]
for k in range(4): v=3*v-1;seq.append(v)
case(2,2,'récurrence',seq==[2,5,14,41,122])
case(2,3,'arithmétique et premier rang',7-3*8==-17,7-3*8>-20>=7-3*9)
case(2,4,'géométrique et somme',5*2**4==80,5*2**6==320,sum(5*2**k for k in range(5))==155)
case(2,5,'évolution réciproque de valeur',eq(800*S.Rational(85,100)**2,578),eq(1-S.Rational(85,100)**2,S.Rational(2775,10000)))
case(2,6,'paramètres de deux suites',4*3-1==11,4*8-1==31,3*2**2==12,3*2**5==96)
case(2,7,'trois sommes et nombres de termes',sum(range(4,62,3))==650,len(range(4,62,3))==20,sum(3*2**k for k in range(8))==765,sum(2*k+1 for k in range(3,11))==112)
case(2,8,'variations et fraction simplifiée',eq((n+1)**2-4*(n+1)-(n*n-4*n),2*n-3),eq((n+2)/(n+3)-(n+1)/(n+2),1/((n+2)*(n+3))),eq((n+1)/(n+2),1-1/(n+2)))
case(2,9,'nuage et seuil',16*.5**7>=.1>16*.5**8)
case(2,10,'quatre transitions et onze termes', [2**(k+2)-1 for k in range(5)]==[3,7,15,31,63],len(range(11))==11)
case(2,11,'épargne et premier seuil',1000*1.05**8<1500<=1000*1.05**9)
case(2,12,'capacité, recette et extension',sum(2*k+16 for k in range(1,21))==740,9*270+12*470==8070,24*(24+17)<1000<=25*(25+17))
case(2,13,'transformation et seuil du traitement',eq(S.Rational(4,5)*(x+30)+6-30,S.Rational(4,5)*x),30-20*.8**10<28<=30-20*.8**11)
case(2,14,'salaires, totaux et premier dépassement',close(24000*1.04**5,29199.6696576),sum(24000+1000*k for k in range(10))==285000,close(sum(24000*1.04**k for k in range(10)),288146.570951),all(24000*1.04**k<=24000+1000*k for k in range(1,4)),24000*1.04**4>28000)
case(2,15,'allumettes et somme totale',3*33+1==100,3*34+1>100,sum(3*k+1 for k in range(1,26))==1000,sum(3*k+1 for k in range(1,27))==1079)

f=x*x-2*x
case(3,1,'taux de variation',eq((f.subs(x,3)-f.subs(x,1))/2,2),eq(f.subs(x,2)-f.subs(x,1),1),eq((f.subs(x,1+h)-f.subs(x,1))/h,h))
case(3,2,'pente et tangente',S.Rational(7-3,4-2)==2,eq((2*x-1).subs(x,2),3))
case(3,3,'dérivées de référence',eq(S.diff(5*x**4-3*x*x+7*x-8,x),20*x**3-6*x+7),eq(S.diff(3/x,x),-3/x**2),eq(S.diff(S.sqrt(x)+2*x,x),1/(2*S.sqrt(x))+2),eq(S.diff(x**-3,x),-3/x**4))
case(3,4,'tangente en un point',eq(S.diff(x*x+3*x-1,x).subs(x,1),5),eq((5*x-2).subs(x,1),3))
case(3,5,'règles du produit et du quotient',eq(S.diff((2*x+1)*(x*x-3),x),6*x*x+2*x-6),eq(S.diff((x+1)/(x-2),x),-3/(x-2)**2))
case(3,6,'définition et pentes des sécantes',eq(((a+h)**2-a*a)/h,2*a+h),[close(4+k,v) for k,v in [(1,5),(.1,4.1),(-.1,3.9),(.01,4.01)]]==[True]*4)
case(3,7,'trois produits',eq(S.diff((x*x+1)*(3*x-2),x),9*x*x-4*x+3),eq(S.diff(x*x*S.sqrt(x),x),S.Rational(5,2)*x*S.sqrt(x)),eq(S.diff((x-1)**2*(x+2),x),3*x*x-3))
case(3,8,'trois quotients',eq(S.diff((2*x-1)/(x+3),x),7/(x+3)**2),eq(S.diff((x*x+1)/x,x),1-1/x**2),eq(S.diff(x/(x*x+1),x),(1-x*x)/(x*x+1)**2))
f=x**3-3*x+1
case(3,9,'tangentes de pente imposée',roots(S.diff(f,x)-9)=={-2,2},eq(9*(x-2)+f.subs(x,2),9*x-15),eq(9*(x+2)+f.subs(x,-2),9*x+17))
case(3,10,'approximation affine et erreur',close(math.sqrt(4.08),2.0199009876724),close(abs(2.02-math.sqrt(4.08)),.0000990123276,1e-12))
case(3,11,'taux à gauche, à droite et à zéro',S.limit(S.Abs(h)/h,h,0,dir='+')==1,S.limit(S.Abs(h)/h,h,0,dir='-')==-1,S.limit(1/S.sqrt(h),h,0,dir='+')==S.oo)
case(3,12,'tangentes passant par un point',S.solve(a*a-1,a)==[-1,1],(2*x-1).subs(x,0)==-1,(-2*x-1).subs(x,0)==-1,S.diff(x*x,x).subs(x,1)==2,S.diff(x*x,x).subs(x,-1)==-2)
case(3,12,'extrémités des tangentes dessinées',all(eq(y0,2*x0-1) for x0,y0 in [(-q(1,10),-q(12,10)),(2,3)]),all(eq(y0,-2*x0-1) for x0,y0 in [(-2,3),(q(1,10),-q(12,10))]))
s=x**3-6*x*x+12*x
case(3,13,'vitesse moyenne et instantanée',eq((s.subs(x,3)-s.subs(x,1))/2,1),eq(S.diff(s,x),3*(x-2)**2),s.subs(x,2)==8)
f=S.Rational(3,2)*x*x-2*x+1
case(3,14,'reconstruction et position relative',f.subs(x,0)==1,f.subs(x,2)==3,S.diff(f,x).subs(x,2)==4,eq(f-(4*x-5),S.Rational(3,2)*(x-2)**2))
C=x**3/50-3*x*x/5+10*x+100
case(3,15,'coût marginal et erreur exacte',S.diff(C,x).subs(x,20)==10,eq(C.subs(x,21)-C.subs(x,20),S.Rational(1062,100)),eq(C.subs(x,20+h)-C.subs(x,20),10*h+3*h*h/5+h**3/50))

case(4,1,'comparaison des valeurs aux bornes',max([2,7,-1])==7,min([2,7,-1])==-1)
f=x*x-4*x+1
case(4,2,'valeurs et sommet sur segment',[f.subs(x,k) for k in [-1,2,5]]==[6,-3,6],roots(S.diff(f,x))=={2})
case(4,3,'croissance stricte et bornes',eq(S.diff(x**3+3*x,x),3*x*x+3),(-1)**3+3*(-1)==-4,2**3+3*2==14)
case(4,4,'quotient et bornes',eq(S.diff((x+1)/(x+2),x),1/(x+2)**2),eq(((x+1)/(x+2)).subs(x,0),S.Rational(1,2)),eq(((x+1)/(x+2)).subs(x,4),S.Rational(5,6)))
case(4,5,'zéro isolé de la dérivée',eq(S.diff(x**3,x),3*x*x),S.diff(x**3,x).subs(x,0)==0,(-S.Rational(1,10))**3<0<S.Rational(1,10)**3)
f=x**3-3*x*x-9*x+5
case(4,6,'dérivée et quatre valeurs clés',eq(S.diff(f,x),3*(x+1)*(x-3)),[f.subs(x,k) for k in [-3,-1,3,5]]==[-22,10,-22,10])
case(4,7,'minimum et preuve algébrique',eq(S.diff(x+4/x,x),(x-2)*(x+2)/x**2),eq(x+4/x-4,(x-2)**2/x))
f=x**4-4*x*x;g=x**3-3*x
case(4,8,'parités et extremums',eq(f.subs(x,-x),f),eq(g.subs(x,-x),-g),f.subs(x,0)==0,f.subs(x,3)==45,eq(f.subs(x,S.sqrt(2)),-4))
case(4,9,'position par rapport à la tangente',eq(x**3-(3*x-2),(x-1)**2*(x+2)))
case(4,10,'racine et bornes',eq(S.diff(S.sqrt(x)-x/2,x),(1-S.sqrt(x))/(2*S.sqrt(x))),eq((S.sqrt(x)-x/2).subs(x,1),S.Rational(1,2)),eq((S.sqrt(x)-x/2).subs(x,9),-S.Rational(3,2)))
case(4,11,'maximum entier',max(range(21),key=lambda k:-2*k*k+27*k-40)==7,-2*7**2+27*7-40==51)
case(4,12,'boîte et conversion en litres',eq(S.diff(x*(24-2*x)**2,x),12*(x-4)*(x-12)),4*16**2==1024)
case(4,13,'rectangle sous une parabole',eq(S.diff(2*x*(9-x*x),x),18-6*x*x),eq((2*x*(9-x*x)).subs(x,S.sqrt(3)),12*S.sqrt(3)))
case(4,14,'cylindre et volume exact',eq(S.diff(S.pi*x*x*(20-x),x),S.pi*x*(40-3*x)),eq((S.pi*x*x*(20-x)).subs(x,S.Rational(40,3)),32000*S.pi/27),close(32000*math.pi/27,3723.369070921))
case(4,15,'distance et minimum',eq(x*x+(x*x-2)**2,x**4-3*x*x+4),eq((x**4-3*x*x+4).subs(x,S.sqrt(S.Rational(3,2))),S.Rational(7,4)))

case(5,1,'propriétés algébriques',eq(S.exp(2*x)*S.exp(3-x),S.exp(x+3)),eq(S.exp(5*x)/S.exp(2*x-1),S.exp(3*x+1)),eq(S.exp(-x)**3*S.exp(2*x),S.exp(-x)))
case(5,2,'équations et positivité',S.solve(2*x-1-3,x)==[2],S.solve(x+2,x)==[-2],S.exp(x).is_positive)
case(5,3,'comparaison des exposants',S.solve_univariate_inequality(3*x+1<=x+5,x)==(x<=2),S.solve_univariate_inequality(-2*x>0,x)==(x<0))
case(5,4,'dérivées exponentielles',eq(S.diff(S.exp(2*x),x),2*S.exp(2*x)),eq(S.diff(3*S.exp(-x),x),-3*S.exp(-x)),eq(S.diff(S.exp(x+1)-4,x),S.exp(x+1)))
case(5,5,'tangente et approximation',S.exp(0)==1,eq(1+S.Rational(3,100),S.Rational(103,100)))
case(5,6,'factorisations et racines',eq(S.exp(2*x)-S.exp(x),S.exp(x)*(S.exp(x)-1)),roots(x-2)=={2},eq(x*x-3*x+2,(x-1)*(x-2)))
f=(x+1)*S.exp(-x)
case(5,7,'variations, bornes et tangente',eq(S.diff(f,x),-x*S.exp(-x)),eq(f.subs(x,-2),-S.exp(2)),f.subs(x,0)==1,eq(-S.exp(-1)*(x-1)+f.subs(x,1),(3-x)/S.E))
case(5,8,'minimum par deux méthodes',eq(S.diff(S.exp(2*x)-2*S.exp(x),x),2*S.exp(x)*(S.exp(x)-1)),eq(S.exp(2*x)-2*S.exp(x),(S.exp(x)-1)**2-1))
case(5,9,'quotient, dérivée et milieu',eq(S.diff(S.exp(x)/(1+S.exp(x)),x),S.exp(x)/(1+S.exp(x))**2),eq((S.exp(x)/(1+S.exp(x))).subs(x,0),S.Rational(1,2)))
case(5,10,'population et taux annuel',round(500*math.e)==1359,round(100*(math.exp(.2)-1),1)==22.1)
case(5,11,'Euler et deux tailles',close(1.5**2,2.25),close(1.1**10,2.5937424601))
case(5,12,'refroidissement et seuil entier',20+70==90,20+70*math.exp(-1.2)>40>=20+70*math.exp(-1.3))
case(5,13,'concentration et taux moyen',eq(S.diff(8*x*S.exp(-x/2),x),4*(2-x)*S.exp(-x/2)),close(24*math.exp(-1.5)-16/math.e,-.53094721518))
case(5,14,'inégalité et bornes numériques',eq(S.diff(S.exp(x)-1-x,x),S.exp(x)-1),S.Rational(11,10)<S.exp(S.Rational(1,10))<S.Rational(10,9),eq(S.Rational(10,9)-S.Rational(11,10),S.Rational(1,90)))
case(5,15,'campagne et conversion monétaire',eq(S.diff(100*(x+1)*S.exp(-x/2),x),50*(1-x)*S.exp(-x/2)),close(20000/math.sqrt(math.e),12130.6131942527),[k for k in range(1,7) if 100*(k+1)*math.exp(-k/2)>100]==[1,2])

q=S.Rational
pi=S.pi
# Trigonométrie : valeurs exactes, arcs et coordonnées.
case(6,1,'conversions',all(eq(k*pi/180,v) for k,v in [(30,pi/6),(45,pi/4),(120,2*pi/3),(270,3*pi/2)]),all(eq(k*180/pi,v) for k,v in [(pi/3,60),(5*pi/6,150),(7*pi/4,315)]))
case(6,2,'angles de même point-image',eq(S.cos(pi/3),S.cos(13*pi/3)),eq(S.sin(-pi/2),S.sin(3*pi/2)),not eq(S.cos(pi/4),S.cos(5*pi/4)))
case(6,3,'valeurs remarquables',eq(S.cos(pi/6),S.sqrt(3)/2),eq(S.sin(pi/4),S.sqrt(2)/2),S.cos(pi)==-1,S.sin(pi)==0,S.cos(3*pi/2)==0,S.sin(3*pi/2)==-1)
case(6,4,'symétries',eq(S.cos(-pi/3),q(1,2)),eq(S.sin(-pi/3),-S.sqrt(3)/2),eq(S.cos(2*pi/3),-q(1,2)),eq(S.sin(2*pi/3),S.sqrt(3)/2))
case(6,5,'longueurs d’arcs',eq(6*pi/3,2*pi),eq(6*3*pi/4,9*pi/2),eq(6*2*pi,12*pi))
angles=[17*pi/6,-11*pi/4,29*pi/3];reduced=[5*pi/6,-3*pi/4,-pi/3]
case(6,6,'réduction et coordonnées',all(eq(S.cos(u),S.cos(v)) and eq(S.sin(u),S.sin(v)) for u,v in zip(angles,reduced)),all(-pi<t<=pi for t in reduced))
case(6,7,'coordonnée retrouvée et angles associés',eq(1-q(9,25),q(16,25)),eq(q(3,5)**2+q(4,5)**2,1))
case(6,8,'valeurs et expression combinée',eq(S.cos(5*pi/4),-S.sqrt(2)/2),eq(S.sin(7*pi/6),-q(1,2)),eq(2*S.cos(5*pi/4)+S.sqrt(2)*S.sin(7*pi/6),-3*S.sqrt(2)/2))
case(6,9,'angles lus sur le cercle',all(eq(S.cos(t),q(1,2)) for t in [pi/3,5*pi/3]),all(eq(S.sin(t),-S.sqrt(2)/2) for t in [5*pi/4,7*pi/4]),all(S.cos(t)==0 for t in [pi/2,3*pi/2]))
case(6,10,'secteur de disque',eq((2*pi/5)/(2*pi),q(1,5)),eq(100*pi/5,20*pi),eq(20+10*2*pi/5,20+4*pi))
case(6,11,'identité trigonométrique',S.trigsimp((S.cos(x)+S.sin(x))**2+(S.cos(x)-S.sin(x))**2)==2)
case(6,12,'grande roue et durée',[(12*S.cos(t),14+12*S.sin(t)) for t in [0,pi/2,pi,3*pi/2]]==[(12,14),(0,26),(-12,14),(0,2)],14+12*S.sin(pi/6)==20,14+12*S.sin(7*pi/6)==8,eq(48*(5*pi/6)/(2*pi),20))
case(6,13,'hexagone : côté, périmètre et aire',eq((1-q(1,2))**2+(S.sqrt(3)/2)**2,1),eq(6*S.sqrt(3)/4,3*S.sqrt(3)/2))
case(6,14,'intersection des arcs et longueur',2*pi/3<pi<4*pi/3,eq(pi-2*pi/3,pi/3),eq(S.cos(2*pi/3),-q(1,2)))
case(6,15,'polygones inscrits',eq(12*S.sin(pi/6),6),eq(24*S.sin(pi/12),6*(S.sqrt(6)-S.sqrt(2))),eq(S.sqrt(2-S.sqrt(4-1)),(S.sqrt(6)-S.sqrt(2))/2),eq(2-S.sqrt(4-(2*S.sin(pi/12))**2),(2*S.sin(pi/24))**2))

# Produit scalaire et géométrie repérée.
case(7,1,'vecteur, distance et milieu',(4-1,6-2)==(3,4),norm2((3,4))==25,((1+4)/2,(2+6)/2)==(2.5,4))
case(7,2,'produits et normes',dot((2,-1),(3,4))==2,norm2((2,-1))==5,norm2((3,4))==25)
case(7,3,'produits avec des angles', [S.simplify(30*S.cos(t)) for t in [pi/3,pi/2,2*pi/3]]==[15,0,-15])
case(7,4,'orthogonalité et colinéarité',dot((3,2),(2,-3))==0,dot((3,2),(-6,-4))==-26,(-6,-4)==(-2*3,-2*2))
case(7,5,'projection et produit',dot((6,0),(2,3))==12,dot((0,3),(6,0))==0)
case(7,6,'carrés de normes',9+16+12==37,9+16-12==13,37+13==2*9+2*16)
case(7,7,'angle et triangle rectangle',dot((4,0),(1,S.sqrt(3)))==4,norm2((1,S.sqrt(3)))==4,norm2((-3,S.sqrt(3)))==12,eq(4/(4*S.sqrt(4)),q(1,2)))
case(7,8,'paramètre et angle',S.solve(3*m-2,m)==[q(2,3)],S.solve(-m-6,m)==[-6],eq(dot((0,2),(3,-1))/(2*S.sqrt(10)),-1/S.sqrt(10)))
case(7,9,'rectangle et diagonales',dot((6,4),(-6,4))==-20,dot((6,0),(6,4))==36)
case(7,10,'parallélogramme',eq(3*4*S.cos(pi/3),6),9+16+12==37,9+16-12==13)
case(7,11,'hauteur et Al-Kashi',eq(8*5*S.cos(pi/3),20),eq(q(5,2)**2+(5*S.sqrt(3)/2)**2,25),eq(64+25-2*8*5*S.cos(pi/3),49))
case(7,12,'triangle, pied de hauteur et aire',dot((-1,-3),(3,-1))==0,dot((4,2),(1,3))==10,dot((1,-2),(4,2))==0,eq(S.sqrt(20)*S.sqrt(5)/2,5))
case(7,13,'lieu, intérieur et frontière',eq((-2-x)*(2-x)+h*h,x*x+h*h-4),0**2+2**2-4==0,1**2+1**2-4==-2)
case(7,14,'travail et déplacement optimal',dot((30,40),(6,0))==180,norm2((30,40))==2500,eq(dot((30,40),(3*S.sqrt(3),3)),90*S.sqrt(3)+120),norm2((q(18,5),q(24,5)))==36,dot((30,40),(q(18,5),q(24,5)))==300)
case(7,15,'identité du milieu et minimum',eq((0-x)*(6-x)+h*h,(x-3)**2+h*h-9),eq((x-3)**2+h*h-9-5,(x-3)**2+h*h-14))

case(8,1,'normaux et appartenance',dot((3,-2),(2,3))==0,3*1-2*4+5==0,3*0-2*2+5!=0)
case(8,2,'droite par un point',3*2+4*(-1)-2==0,dot((3,4),(-4,3))==0)
case(8,3,'cercle et trois points',norm2((5-2,-1+1))==9,norm2((2-2,2+1))==9,norm2((-2,1))==5)
case(8,4,'carrés et cercle',eq(x*x+h*h-4*x+6*h-12,(x-2)**2+(h+3)**2-25),roots((x+3)**2-25)=={2,-8})
case(8,5,'projections sur deux axes',norm2((0,4))==16,dot((-1,1),(1,1))==0,norm2((-1,1))==2)
case(8,6,'projeté et distance exacte',2*q(8,5)+q(9,5)-5==0,dot((q(8,5)-4,q(9,5)-3),(-1,2))==0,norm2((q(8,5)-4,q(9,5)-3))==q(36,5))
case(8,7,'directions et perpendiculaire',6==2*3,-4==2*(-2),-7!=2*1,dot((3,-2),(2,3))==0,2*1+3*2-8==0)
case(8,8,'intersections de cercle',roots((x-1)**2+9-25)=={-3,5},roots((x+2)**2-25)=={3,-7})
case(8,9,'paramètre et rayon',eq(x*x+h*h-2*x+4*h+m,(x-1)**2+(h+2)**2-(5-m)),S.sqrt(5-1)==2)
case(8,10,'tangente au cercle',norm2((3,4))==25,3*4+4*6-36==0,dot((3,4),(-4,3))==0)
case(8,11,'médiatrice et distances',3*1+2-5==0,norm2((2,-4))==20,norm2((4,-2))==20,3*0+5-5==0)
case(8,12,'hauteurs, centre et cercle circonscrit',dot((2,2),(-4,4))==0,dot((0,-2),(6,0))==0,dot((3,3),(-4,4))==0,3+2*1-5==0,norm2((3,1))==10,norm2((3-6,1))==10,norm2((3-2,1-4))==10)
case(8,13,'intersections et pied de projection',roots((x-2)**2+(3-x)**2-5)=={1,4},q(5,2)+q(3,2)==4,norm2((q(1,2),q(1,2)))==q(1,2))
case(8,14,'droites horizontales et tangences',roots(9-(x-3)**2)=={0,6},roots((x-1)**2-8)=={1-2*S.sqrt(2),1+2*S.sqrt(2)})
case(8,15,'parabole-lieu et tangente',eq(x*x+(h-2)**2-h*h,x*x-4*h+4),roots(x*x/4+1-5)=={-4,4},S.diff(x*x/4+1,x).subs(x,4)==2,norm2((4,3))==25)

# Probabilités calculées par fractions et par énumération des petites issues.
case(9,1,'conditionnement et complément',q(1,10)/q(2,5)==q(1,4),q(2,5)-q(1,10)==q(3,10))
case(9,2,'tableau croisé',50+70+30+50==200,q(120,200)==q(3,5),q(50,120)==q(5,12),q(50,80)==q(5,8))
case(9,3,'intersection et réunion',q(3,10)*q(1,2)==q(15,100),q(3,10)+q(1,2)-q(15,100)==q(65,100))
case(9,4,'incompatibilité sans indépendance',q(2,10)*q(3,10)==q(6,100),q(6,100)!=0)
case(9,5,'arbre et condition inverse',q(6,10)*q(2,10)+q(4,10)*q(5,10)==q(32,100),q(12,100)/q(32,100)==q(3,8))
case(9,6,'défauts de deux ateliers',q(7,10)*q(2,100)+q(3,10)*q(5,100)==q(29,1000),q(15,1000)/q(29,1000)==q(15,29))
case(9,7,'partition à trois machines',q(1,2)*q(1,100)+q(3,10)*q(2,100)+q(1,5)*q(4,100)==q(19,1000),q(8,1000)/q(19,1000)==q(8,19))
case(9,8,'test fictif et probabilités inverses',100*.95==95,9900*.04==396,q(95,95+396)==q(95,491))
case(9,9,'deux Bernoulli',q(2,5)**2==q(16,100),2*q(2,5)*q(3,5)==q(48,100),1-q(3,5)**2==q(64,100))
case(9,10,'tirages sans remise',q(3,5)*q(2,4)==q(3,10),q(2,5)*q(3,4)==q(3,10),q(2,5)*q(1,4)==q(1,10),q(2,4)!=q(3,5))
case(9,11,'tirages avec remise',q(3,5)**2==q(9,25),2*q(3,5)*q(2,5)==q(12,25))
paths3=list(product([0,1],repeat=3));p=q(7,10)
prob2=sum(p**sum(t)*(1-p)**(3-sum(t)) for t in paths3 if sum(t)==2)
case(9,12,'énumération de trois épreuves',prob2==q(441,1000),1-(1-p)**3==q(973,1000),(1-p)**2*p==q(63,1000))
paths4=list(product([0,1],repeat=4));p=q(1,4)
case(9,13,'énumération de quatre épreuves',len([t for t in paths4 if sum(t)==2])==6,sum(p**sum(t)*(1-p)**(4-sum(t)) for t in paths4 if sum(t)==2)==q(27,128),1-(1-p)**4==q(175,256),sum(p**sum(t)*(1-p)**(4-sum(t)) for t in paths4 if sum(t)<=1)==q(189,256))
case(9,14,'mélange et proportion inconnue',S.solve(q(1,10)*x+q(4,10)*(1-x)-q(22,100),x)==[q(3,5)],q(6,100)/q(22,100)==q(3,11))
case(9,15,'taux pondérés et renversement',q(19,20)>q(90,100),q(18,60)>q(20,100),q(110,200)==q(55,100),q(37,80)==q(4625,10000),q(100,200)==q(1,2),q(20,80)==q(1,4))

case(10,1,'indicatrice et loi',moments([0,1],[.5,.5])==(q(1,2),q(1,4)))
case(10,2,'loi et premiers moments',moments([-1,0,2],[.2,.5,.3])==(q(2,5),q(31,25)),q(1,5)+q(1,2)==q(7,10))
case(10,3,'probabilité manquante et variance',1-q(1,10)-q(2,10)-q(4,10)==q(3,10),moments([0,1,2,3],[.1,.2,.3,.4])==(2,1))
case(10,4,'Bernoulli et écart type',moments([0,1],[.7,.3])==(q(3,10),q(21,100)))
case(10,5,'équité et variance',moments([5,-1],[q(1,6),q(5,6)])==(0,5))
case(10,6,'deux calculs de variance',moments([-1,0,2],[q(1,5),q(1,2),q(3,10)])==(q(2,5),q(31,25)),eq(q(49,25)*q(1,5)+q(4,25)*q(1,2)+q(64,25)*q(3,10),q(31,25)))
case(10,7,'transformation affine',moments([-5,-2,4],[.2,.5,.3])==(-q(4,5),q(279,25)))
case(10,8,'moyennes et risques',moments([-2,2],[.5,.5])==(0,4),moments([-1,1],[.5,.5])==(0,1))
case(10,9,'linéarité de variables dépendantes',sum(range(1,7))/6==3.5,all(k+(7-k)==7 for k in range(1,7)),q(1,6)!=q(1,36))
z=[sum(t)-2*t[0] for t in product([0,1],repeat=2)]
case(10,10,'table des quatre issues',sorted(z)==[-1,0,0,1],moments(z,[q(1,4)]*4)==(0,q(1,2)))
mu,var=moments([-1,1,3],[.25,.5,.25])
case(10,11,'erreur quadratique et minimum',mu==1,var==2,eq(3-2*a+a*a,(a-1)**2+2))
mu,var=moments([20,5,0],[.03,.1,.87])
case(10,12,'loterie, prix et dispersion',mu==q(11,10),var==q(1329,100),moments([18,3,-2],[.03,.1,.87])==(-q(9,10),q(1329,100)),q(3,100)+q(1,10)==q(13,100))
mu,var=moments([0,1,2,3],[q(1,8),q(3,8),q(3,8),q(1,8)])
case(10,13,'trois pièces et gain affine',mu==q(3,2),var==q(3,4),4*mu-5==1,16*var==12)
case(10,14,'garantie et total espéré',moments([15,-485],[.98,.02])==(5,4900),100*5==500)
mu,var=moments([q(1,2),1,2],[.5,.25,.25])
case(10,15,'aire aléatoire et prévision',mu==1,var==q(3,8),eq(q(11,8)-2*a+a*a,(a-1)**2+q(3,8)))

# Statistiques descriptives, représentations et expériences.
data=[0]*2+[1]*3+[2]*4+[3]
case(11,1,'tableau et indicateurs',len(data)==10,statistics.mean(data)==1.4,statistics.median(data)==1.5,max(data)-min(data)==3)
data=[10]*2+[12]*4+[14]*3+[16]
case(11,2,'barres, moyenne et quartiles',statistics.mean(data)==12.6,statistics.median(data)==12,data[math.ceil(len(data)/4)-1]==12,data[math.ceil(3*len(data)/4)-1]==14)
data=[1,2,2,3,4,4,5,7]
case(11,3,'boîte et convention des quartiles',statistics.median(data)==3.5,data[1]==2,data[5]==4,data[5]-data[1]==2)
sample=[0,1,0,0,1,1,0,0,0,1]
case(11,4,'moyenne observée et écart',sum(sample)/len(sample)==.4,close(abs(.4-.3),.1))
case(11,5,'ensemble des moyennes possibles',{sum(t)/4 for t in product([0,1],repeat=4)}=={0,.25,.5,.75,1})
case(11,6,'aires de l’histogramme',q(2,10)/10==q(2,100),q(5,10)/20==q(25,1000),q(3,10)/30==q(1,100))
case(11,7,'effets d’une transformation affine',2*12+5==29,12-12==0,2**2*3**2==36)
case(11,8,'estimation et erreur exacte',q(137,400)-q(1,3)==q(11,1200))
case(11,9,'estimation de pi',close(4*786/1000,3.144),round(abs(3.144-math.pi),5)==.00241)
means=[sum(t)/5 for t in [[0,0,2,0,2],[2,2,2,0,2],[0,0,0,0,0],[2,0,2,2,0]]]
case(11,10,'critère sur quatre échantillons',means==[.8,1.6,0,1.2],sum(abs(t-1)<=2/math.sqrt(5) for t in means)==3,moments([0,2],[.5,.5])==(1,1))
case(11,11,'taille et seuil',2*2/math.sqrt(16)==1,2*2/math.sqrt(64)==.5,abs(2.2-1)>1,abs(1.4-1)<=.5,close(math.sqrt(9),3))
case(11,12,'moments de la loi simulée',moments([-1,2,5],[.5,.3,.2])==(q(11,10),q(549,100)))
case(11,13,'seuil expérimental',close(2*math.sqrt(.24)/5,.195959179422654))
A=[4,5,5,6];B=[1,5,5,9];data=sorted(A+B)
case(11,14,'séries regroupées',statistics.mean(A)==statistics.mean(B)==5,statistics.pvariance(A)==.5,statistics.pvariance(B)==8,statistics.pvariance(data)==4.25,statistics.median(data)==5,data[1]==4,data[5]==5)
case(11,15,'lettres, loi et fréquences',[(c,'BANANE'.count(c)) for c in 'ABEN']==[('A',2),('B',1),('E',1),('N',2)],'ANANAS'.count('A')==3,sum(c in 'AEIOUY' for c in 'BANANE')==3,moments([0,1],[.5,.5])==(q(1,2),q(1,4)))

# Exécution de chaque bloc Python présent dans les énoncés et les corrigés.
import random
scopes={}
code_report=[]
for folder,env in [('chapitres','exercice'),('corriges','corrige')]:
    for path in sorted((R/folder).glob('*.tex')):
        ch=int(path.name[:2]); text=path.read_text(encoding='utf-8')
        pattern=(r'\\begin\{exercice\}\[\d\]\{[^\n]+\}(.*?)\\end\{exercice\}' if env=='exercice' else r'\\begin\{corrige\}\{\d+\}\{[^\n]+\}(.*?)\\end\{corrige\}')
        bodies=re.findall(pattern,text,re.S)
        assert len(bodies)==15,(path,len(bodies))
        for ex,body in enumerate(bodies,1):
            snippets=re.findall(r'\\begin\{python\}\s*(.*?)\\end\{python\}',body,re.S)
            for index,source in enumerate(snippets):
                scope={};random.seed(2026)
                exec(compile(source,f'{path.name}:{ex}:{index}','exec'),scope)
                scopes[(ch,ex)]=scope
                code_report.append(dict(chapitre=ch,exercice=ex,fichier=folder+'/'+path.name,bloc=index+1))
case(12,1,'échange exécuté',scopes[12,1]['a']==5,scopes[12,1]['b']==3)
fn=scopes[12,2]['traitement']
case(12,2,'test de parité exécuté',[fn(k) for k in [7,8,0]]==[22,4,0])
fn=scopes[12,3]['f'];case(12,3,'fonction évaluée',[fn(k) for k in [0,2,5]]==[2,0,12])
case(12,4,'modifications de liste exécutées',scopes[12,4]['L']==[5,4,2])
case(12,5,'compréhensions exécutées',scopes[12,5]['L']==[0,1,4,9,16,25],scopes[12,5]['P']==[0,4,16])
fn=scopes[12,6]['factorielle'];case(12,6,'factorielle et cas zéro',all(fn(k)==math.factorial(k) for k in range(16)))
fn=scopes[12,7]['somme'];case(12,7,'somme et cas zéro',all(fn(k)==k*(k+1)//2 for k in range(51)))
case(12,8,'boucle de seuil exécutée',scopes[12,8]['seuil']()==(14,520))
flow=(R/'chapitres/12-algorithmique.tex').read_text(encoding='utf-8')
case(12,8,'schéma de boucle : retour au test',r'\coordinate (reprise) at ([yshift=4mm]b.north)' in flow,r'(c.north)|-(reprise)' in flow,r'(c.north)|-(a.east)' not in flow)
fn=scopes[12,9]['somme_geometrique'];case(12,9,'somme de termes et bornes',all(fn(k)==3**k-1 for k in range(11)))
fn=scopes[12,10]['frequence'];case(12,10,'fréquence de lettres exécutée',close(fn('BANANE','A'),1/3),close(fn('BANANE','B'),1/6),fn('BANANE','Z')==0)
fn=scopes[12,11]['moments'];mu,var=fn([-1,0,2],[.2,.5,.3])
case(12,11,'moments programmés et cas constant',close(mu,.4),close(var,1.24),fn([3],[1])==(3,0))
fn=scopes[12,12]['fibonacci'];case(12,12,'Fibonacci et premier dépassement',fn(0)==[0],fn(7)==[0,1,1,2,3,5,8,13],fn(16)[-1]==987,fn(17)[-1]==1597)
fn=scopes[12,13]['syracuse'];case(12,13,'Syracuse et garde d’itérations',fn(6)==[6,3,10,5,16,8,4,2,1],fn(1)==[1],len(fn(27,2))==3)
fn=scopes[12,14]['newton'];case(12,14,'Newton exécuté',close(fn(1),1.5),close(fn(2),17/12),close(fn(5),math.sqrt(2),1e-14),fn(0)==1)
case(12,14,'tangente de Newton',eq(S.solve(2*a*(x-a)+a*a-2,x)[0],(a+2/a)/2))
fn=scopes[3,6]['secantes'];case(3,6,'liste des pentes des sécantes',fn(0.5,4)==[0.5,1.5,2.5,3.5],all(close(v,2*k*0.1+0.1,1e-12) for k,v in enumerate(fn(0.1,10))),fn(1,0)==[])
fn=scopes[6,15]['archimede'];case(6,15,'méthode d’Archimède exécutée',fn(0)==3,all(close(fn(k),6*2**k*math.sin(math.pi/(6*2**k)),1e-9) for k in range(6)),3+10/71<fn(4)<math.pi,round(fn(4),5)==3.14103)
fn=scopes[12,15]['monte_carlo'];est=fn(10000,2026)
case(12,15,'Monte-Carlo exécuté et reproductible',0<=est[0]<=1,0<=est[1]<=4,est==fn(10000,2026),abs(est[0]-1/3)<.03,abs(est[1]-math.pi)<.06)
scope=scopes[11,12]
for u,want in [(0,-1),(.49,-1),(.5,2),(.79,2),(.8,5),(.99,5)]:
    scope['random']=lambda u=u:u
    case(11,12,f'branche simulée pour u={u}',scope['tirage']()==want,scope['moyenne'](3)==want)
case(11,13,'programme de répétition exécuté',0<=scopes[11,13]['proportion']<=1,scopes[11,13]['compteur']==round(scopes[11,13]['proportion']*500))

# Logique : opérations ensemblistes et identités des preuves générales.
A={2,4,6};B={1,2,3};E=set(range(1,7))
case(13,1,'opérations sur les ensembles',A&B=={2},A|B=={1,2,3,4,6},E-A=={1,3,5},{2}<=A,2 in A)
case(13,2,'intervalles et bornes',S.Intersection(S.Interval(-2,3),S.Interval.open(1,5))==S.Interval.Lopen(1,3),S.Union(S.Interval(-2,3),S.Interval.open(1,5))==S.Interval.Ropen(-2,5),S.Complement(S.S.Reals,S.Interval(-2,3))==S.Union(S.Interval.open(-S.oo,-2),S.Interval.open(3,S.oo)))
case(13,3,'produit cartésien',len(list(product(['a','b'],[0,1,2])))==6,(1,'a') not in set(product(['a','b'],[0,1,2])),(1,'a') in set(product([0,1,2],['a','b'])))
case(13,4,'deux contre-exemples',q(1,2)**2<q(1,2),(-2)**2==4,-2!=2)
case(13,5,'négation de propositions',S.solveset(x*x<0,x,domain=S.S.Reals)==S.EmptySet,roots(x*x+1)==set())
case(13,6,'implication et réciproque réfutée',eq(x*x-4,(x-2)*(x+2)),(-3)**2>4,-3<=2)
case(13,7,'nécessité et suffisance',eq(4*n,2*(2*n)),6%2==0,6%4!=0)
case(13,8,'identité et équation',eq(x*x-1,(x-1)*(x+1)),roots(x*x-1)=={-1,1})
E=set(range(1,9));A={2,4,6,8};B={1,2,3,4}
case(13,9,'loi de De Morgan',E-(A|B)==(E-A)&(E-B)=={5,7})
case(13,10,'contre-exemple et preuve de croissance',(-2)**2>(-1)**2,eq(h*h-a*a,(h-a)*(h+a)))
case(13,11,'preuve par cas et valeur absolue',eq((2*n)*(2*n+1),2*(n*(2*n+1))),eq((2*n+1)*(2*n+2),2*((2*n+1)*(n+1))),all(abs(v)>=v for v in [-3,0,2]))
case(13,12,'identités de parité',eq((2*n)**2,2*(2*n*n)),eq((2*n+1)**2,2*(2*n*n+2*n)+1))
case(13,13,'preuve d’irrationalité : conséquences algébriques',eq((2*n)**2/2,2*n*n),S.sqrt(2).is_rational is False)
case(13,14,'équation avec solution interdite',eq((x*x-1)/(x-1),x+1),roots(x+1-2)=={1},(roots(x+1-2)-{1})==set())
case(13,15,'quantification et minimum du trinôme',eq(x*x-2*m*x+1,(x-m)**2+1-m*m),S.solve_univariate_inequality(1-m*m>=0,m).as_set()==S.Interval(-1,1),S.solve_univariate_inequality(1-m*m>0,m).as_set()==S.Interval.open(-1,1))

# Automatismes et synthèses.
case(14,1,'coefficients réciproques',eq(80*q(5,4)*q(4,5),80),eq(1/q(4,5)-1,q(1,4)))
case(14,2,'valeur initiale et taux',eq(84/q(7,10),120),eq(q(54-45,45),q(1,5)),eq(q(11,10)*q(12,10)-1,q(32,100)))
case(14,3,'identités et produit nul',eq((2*x-3)**2,4*x*x-12*x+9),eq(9*x*x-25,(3*x-5)*(3*x+5)),roots((x-2)*(x+1))=={2,-1})
case(14,4,'signes et intersection',S.solve_univariate_inequality(3-2*x>=0,x).as_set()==S.Interval(-S.oo,q(3,2)),S.solve_univariate_inequality((x+2)*(x-3)<0,x).as_set()==S.Interval.open(-2,3))
case(14,5,'pente et équations',q(7-3,3-1)==2,2*1+1==3,2*3+1==7,-q(8,2)+4==0)
case(14,6,'lecture de segments',-(-2)-1==1,2*1-1==1,-4+5==1,[-1,3]==[2*0-1,2*2-1])
case(14,7,'fréquences et indépendance',q(20+30,100)==q(1,2),q(20,50)==q(2,5),q(2,5)!=q(1,2))
case(14,8,'trigonométrie et arc',eq(S.cos(5*pi/3),q(1,2)),eq(S.sin(5*pi/3),-S.sqrt(3)/2),eq(S.cos(11*pi/3),S.cos(5*pi/3)),eq(3*2*pi/3,2*pi))
f=x**3-6*x*x+9*x
case(14,9,'variations et valeurs clés',eq(S.diff(f,x),3*(x-1)*(x-3)),[f.subs(x,k) for k in [0,1,3,4]]==[0,4,0,4])
case(14,10,'secteurs et effectifs',40+24+16==80,[360*q(k,80) for k in [40,24,16]]==[180,108,72],40-24==16)
g=(2*x-1)*S.exp(-x)
case(14,11,'exponentielle et maximum',roots(2*x-(x+3))=={3},eq(S.diff(g,x),(3-2*x)*S.exp(-x)),eq(g.subs(x,q(3,2)),2*S.exp(-q(3,2))),g.subs(x,0)==-1)
V=x*x*(6-x)
case(14,12,'volume, tangente et seuil',eq(S.diff(V,x),3*x*(4-x)),V.subs(x,4)==32,V.subs(x,2)==16,S.diff(V,x).subs(x,2)==12,eq(V-16,-(x-2)*(x*x-4*x-8)),roots(V-16)=={2,2-2*S.sqrt(3),2+2*S.sqrt(3)})
case(14,13,'triangle, cercle et arc',dot((-2,-2),(2,-2))==0,norm2((2,2))==8,norm2((-2,0))==4,norm2((0,2))==4,eq(2*pi/2,pi))
case(14,14,'mélange, gain et quatre essais',q(6,10)*q(1,100)+q(4,10)*q(4,100)==q(22,1000),q(16,1000)/q(22,1000)==q(8,11),moments([8,-22],[.978,.022])==(q(734,100),q(193644,10000)),close(1-.978**4,.085138357744))
case(14,15,'comparaison des modèles et des seuils',eq(q(9,10)*(x+500)+50-500,q(9,10)*x),500+500*.9**15>600>=500+500*.9**16,500+500*math.exp(-1.6)>600>=500+500*math.exp(-1.7),math.exp(-.1)>.9)

expected={f'{c}.{e}' for c in range(1,15) for e in range(1,16)}
assert set(results)==expected,(expected-set(results),set(results)-expected)
report={
    'exercices_controles':len(results),
    'groupes_de_controles':sum(map(len,results.values())),
    'blocs_python_executes':len(code_report),
    'methode':'Calculs symboliques et exacts, énumération des petites issues, calculs numériques, cas limites des algorithmes ; preuves relues dans les sources.',
    'limite':'Les contrôles informatiques soutiennent la relecture mathématique ; ils ne constituent pas une preuve formelle automatique de tout le texte.',
    'experiences_reproductibles':{'monte_carlo_10000_graine_2026':est,'proportion_500_echantillons':scopes[11,13]['proportion']},
    'controles_par_exercice':dict(sorted(results.items(),key=lambda kv:tuple(map(int,kv[0].split('.'))))),
    'programmes':code_report}
(R/'build/audit-exercices.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['controles_par_exercice','programmes']},ensure_ascii=False,indent=2))
