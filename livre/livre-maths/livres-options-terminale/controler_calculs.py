"""Contrôles indépendants : identités symboliques et résultats des situations du manuel."""
from pathlib import Path
import sys,json,math
from fractions import Fraction as F
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
records=[]
def eq(name,got,expected,tol=1e-10):
    delta=s.simplify(got-expected)
    if isinstance(delta,s.MatrixBase):ok=all(s.simplify(v)==0 or abs(float(v))<=tol for v in delta)
    else:ok=delta==0 or abs(float(delta))<=tol
    records.append(dict(controle=name,valide=bool(ok),obtenu=str(got),attendu=str(expected)))
def approx(name,got,expected,decimals):eq(name,got,expected,0.5001*10**(-decimals))
def binom(n,p,a,b):return sum(F(math.comb(n,k))*p**k*(1-p)**(n-k) for k in range(a,b+1))
x,t=s.symbols('x t',real=True)
if sys.argv[1]=='complementaires':
    # Récurrences : substituer la forme annoncée dans la relation, puis vérifier l'initialisation.
    for label,a,b,u0,ell in [('réserve',F(4,5),30,100,150),('équilibre',F(1,2),3,4,6),('épargne',F(51,50),200,1000,-10000),('dette',F(21,20),-600,5000,12000)]:
        aa=s.Rational(a.numerator,a.denominator);n=s.symbols('n',integer=True,nonnegative=True);u=ell+(u0-ell)*aa**n
        eq(label+' : récurrence',u.subs(n,n+1),aa*u+b);eq(label+' : départ',u.subs(n,0),u0)
    eq('Somme 10 termes arithmétiques',sum(3+2*k for k in range(10)),120)
    eq('Somme géométrique finie',sum(2**k for k in range(5)),31)
    for n in [0,1,3,8,20]:eq(f'Somme 6/3^k rang {n}',sum(F(6,3**k) for k in range(n+1)),F(9)*(1-F(1,3**(n+1))))
    approx('Seuil croissance',math.log(1.6)/math.log(1.03),15.901,3)
    approx('Terme 15',250*1.03**15,389.49,2);approx('Terme 16',250*1.03**16,401.18,2)
    approx('Demi-vie',math.log(2)/.2,3.466,3)
    approx('Seuil décroissance',math.log(8)/.2,10.397,3)
    approx('Seuil géométrique',math.log(1/40)/math.log(.9),35.012,3)
    eq('Racine f(0,77)',F(77,100)**3+2*F(77,100)-2,F(-3467,10**6))
    eq('Racine f(0,78)',F(78,100)**3+2*F(78,100)-2,F(34552,10**6))
    approx('Newton deuxième étape',577/408,1.414216,6)
    for expr,expected in [(3*x**4-2*x+7,12*x**3-2),((2*x-1)**2,8*x-4),(x*s.exp(x),(x+1)*s.exp(x)),((x+1)/(x+2),1/(x+2)**2),(s.log(x*x+1),2*x/(x*x+1))]:eq('Dérivée '+str(expr),s.diff(expr,x),expected)
    eq('Volume boîte dérivé',s.diff(x*(12-2*x)**2,x),(12-2*x)*(12-6*x));eq('Volume maximal',2*(12-4)**2,128)
    eq('Bénéfice entier 4',-2*4**2+19*4-20,24);eq('Bénéfice entier 5',-2*5**2+19*5-20,25)
    eq('Seconde dérivée x exp(-x)',s.diff(x*s.exp(-x),x,2),(x-2)*s.exp(-x))
    eq('Seconde dérivée logistique',s.diff(1/(1+s.exp(-x)),x,2),s.exp(-x)*(s.exp(-x)-1)/(1+s.exp(-x))**3)
    for primitive,fun in [(x**3-4*x,3*x*x-4),(s.exp(2*x)/2,s.exp(2*x)),(s.exp(x*x),2*x*s.exp(x*x)),(s.log(x*x+3),2*x/(x*x+3)),((x*x+1)**2,4*x*(x*x+1)),((x*x+1)**3,6*x*(x*x+1)**2)]:eq('Primitive '+str(primitive),s.diff(primitive,x),fun)
    for sol,a,b,y0 in [(4+3*s.exp(-2*t),-2,8,7),(12-10*s.exp(-t/2),-s.Rational(1,2),6,2),(20+60*s.exp(-t/5),-s.Rational(1,5),4,80),(20+80*s.exp(-t/4),-s.Rational(1,4),5,100)]:
        eq('Équation différentielle '+str(sol),s.diff(sol,t),a*sol+b);eq('Condition initiale '+str(sol),sol.subs(t,0),y0)
    y=100/(1+4*s.exp(-t));eq('Logistique : substitution',s.diff(y,t),y*(1-y/100))
    for fun,a,b,val in [(3*x*x,0,2,8),(1/x,1,s.E,1),(s.exp(2*x),0,1,(s.exp(2)-1)/2),(x-2,0,4,0),(x-x*x,0,1,s.Rational(1,6)),(6*s.exp(-x/2),0,4,12*(1-s.exp(-2)))]:eq('Intégrale '+str(fun),s.integrate(fun,(x,a,b)),val)
    eq('Aire géométrique',-s.integrate(x-1,(x,0,1))+s.integrate(x-1,(x,1,3)),s.Rational(5,2))
    eq('Rectangles gauche',sum(F(k,4)**2/4 for k in range(4)),F(7,32));eq('Rectangles droite',sum(F(k,4)**2/4 for k in range(1,5)),F(15,32))
    for power,val in [(2,s.Rational(1,3)),(3,s.Rational(1,2))]:eq('Gini puissance '+str(power),1-2*s.integrate(x**power,(x,0,1)),val)
    eq('Gini modèle B',1-2*s.integrate((x+x**3)/2,(x,0,1)),s.Rational(1,4))
    eq('Bayes test',F(2,100)*F(95,100)/(F(2,100)*F(95,100)+F(98,100)*F(5,100)),F(19,68))
    eq('Bayes défaut B',F(4,10)*F(5,100)/(F(6,10)*F(2,100)+F(4,10)*F(5,100)),F(5,8))
    eq('Bayes deux tests',F(1,10)*F(9,10)**2/(F(1,10)*F(9,10)**2+F(9,10)*F(1,10)**2),F(9,10))
    p=s.symbols('p',positive=True);ss,ff=s.symbols('s f',positive=True);eq('Dérivée valeur prédictive',s.diff(ss*p/(ss*p+ff*(1-p)),p),ss*ff/(ff+(ss-ff)*p)**2)
    eq('Binomiale B(5,.2) masse 2',binom(5,F(1,5),2,2),F(2048,10000))
    eq('Binomiale B(4,.2) cumul 1',binom(4,F(1,5),0,1),F(8192,10000))
    eq('Défauts 20',1-F(98,100)**20,F(332392,10**6),5.001e-7)
    eq('Intervalle B10',binom(10,F(1,2),2,8),F(1002,1024))
    approx('Intervalle B20 r4',float(binom(20,F(1,2),6,14)),.9586105347,10)
    approx('Intervalle B20 r5',float(binom(20,F(1,2),5,15)),.9881820679,10)
    eq('Capacité cumul 2',binom(4,F(4,5),0,2),F(1808,10000));eq('Capacité cumul 3',binom(4,F(4,5),0,3),F(5904,10000))
    eq('Densité kx',s.integrate(x/2,(x,0,2)),1);eq('Espérance kx',s.integrate(x*x/2,(x,0,2)),s.Rational(4,3))
    eq('Variance densité 2x',s.integrate(x*x*2*x,(x,0,1))-s.Rational(2,3)**2,s.Rational(1,18))
    l=s.symbols('lambda',positive=True);tt=s.symbols('t',nonnegative=True)
    eq('Densité exponentielle',s.integrate(l*s.exp(-l*tt),(tt,0,s.oo)),1);eq('Espérance exponentielle',s.integrate(tt*l*s.exp(-l*tt),(tt,0,s.oo)),1/l)
    xs=[F(i) for i in [1,2,3,4]];ys=[F(i) for i in [2,3,5,6]];mx=sum(xs)/4;my=sum(ys)/4
    vx=sum((v-mx)**2 for v in xs)/4;vy=sum((v-my)**2 for v in ys)/4;cv=sum((a-mx)*(b-my) for a,b in zip(xs,ys))/4
    for label,got,exp in [('moyenne x',mx,F(5,2)),('moyenne y',my,4),('variance x',vx,F(5,4)),('variance y',vy,F(5,2)),('covariance',cv,F(7,4)),('pente',cv/vx,F(7,5)),('origine',my-cv/vx*mx,F(1,2))]:eq('Régression '+label,got,exp)
    approx('Corrélation',float(cv)/math.sqrt(float(vx*vy)),.989949,6)
    eq('Surréservation 12',binom(12,F(4,5),11,12),F(274878,10**6),5.001e-7)
    approx('Évaluation défaut au moins un',1-.971**10,.254938,6);approx('Évaluation rang >20',.971**20,.555117,6)
elif sys.argv[1]=='expertes':
    I=s.I
    for label,expr,val in [
        ('produit complexes',(2+3*I)*(1-2*I),8-I),('quotient 1',(1+I)/(2-I),s.Rational(1,5)+s.Rational(3,5)*I),
        ('quotient 2',(3+I)/(1-I),1+2*I),('inverse',1/(3-4*I),(3+4*I)/25),
        ('puissance 3',(1+I)**3,-2+2*I),('puissance 6',(1+I)**6,-8*I),('puissance 8',(1+I)**8,16),('puissance 12',(1+I)**12,-64),
        ('puissance angle pi/6',(s.sqrt(3)+I)**3,8*I),('module complexe',s.Abs(3-4*I),5),
        ('quotient perpendiculaire',(-2+4*I)/(2+I),2*I),('point fixe complexe',1/(1-I/2),s.Rational(4,5)+s.Rational(2,5)*I),
        ('point fixe spirale',1/(1-(1+I)/2),1+I)]:eq(label,expr,val)
    eq('Équation avec conjugué',(1-4*I)+2*s.conjugate(1-4*I),3+4*I)
    a=s.symbols('a',real=True);eq('Quotient paramétrique',(a+I)/(1+I),(a+1)/2+I*(1-a)/2)
    for n in [2,3,4,5,6,8]:
        roots=[s.exp(2*I*s.pi*k/n) for k in range(n)]
        for k,z in enumerate(roots):eq(f'Unité n={n}, k={k}',s.expand_complex(z**n),1)
        eq('Somme racines n='+str(n),s.expand_complex(sum(roots)),0)
    for power,fun in [(2,(1+s.cos(2*x))/2),(3,(s.cos(3*x)+3*s.cos(x))/4),(4,(3+4*s.cos(2*x)+s.cos(4*x))/8)]:
        eq('Linéarisation cos puissance '+str(power),s.trigsimp(s.expand_trig(fun)-s.cos(x)**power),0)
    eq('Intégrale cos^2',s.integrate(s.cos(x)**2,(x,0,s.pi)),s.pi/2)
    eq('Intégrale cos^3',s.integrate(s.cos(x)**3,(x,0,s.pi/2)),s.Rational(2,3))
    eq('Intégrale cos^4',s.integrate(s.cos(x)**4,(x,0,2*s.pi)),3*s.pi/4)
    eq('Cosinus pentagone',s.cos(2*s.pi/5),(s.sqrt(5)-1)/4)
    z=s.symbols('z');
    for poly,fact in [(z**3-2*z*z+z-2,(z-2)*(z*z+1)),(z**3-3*z*z+4*z-2,(z-1)*(z*z-2*z+2)),(z**3-3*z*z+z+5,(z+1)*(z*z-4*z+5)),(z**3-3*z+2,(z-1)**2*(z+2)),(z**4+5*z*z+4,(z*z+1)*(z*z+4)),(z**3-z*z+4*z-4,(z-1)*(z*z+4))]:eq('Factorisation '+str(poly),s.expand(fact),poly)
    for zz in [1+2*I,1-2*I]:eq('Second degré racine '+str(zz),zz**2-2*zz+5,0)
    for zz in [2+I,-2-I]:eq('Racine carrée '+str(zz),zz**2,3+4*I)
    eq('Diviseurs 18',sum(s.divisors(18)),39)
    for a,b,q,r in [(83,7,11,6),(-83,7,-12,1),(-47,6,-8,1)]:
        eq(f'Division {a}/{b}',a,b*q+r);eq(f'Reste {a}/{b}',int(0<=r<b),1)
    eq('Combinaison diviseurs',5*(3*x+2)-3*(5*x+3),1)
    for a,n,m,expected in [(3,100,7,4),(7,2026,10,9),(2,100,13,3),(2,10,341,1),(2,340,341,1)]:eq(f'Puissance modulaire {a}^{n} [{m}]',pow(a,n,m),expected)
    for a,b,g in [(48,18,6),(35,12,1),(-18,30,6),(252,198,18)]:eq(f'PGCD {a},{b}',math.gcd(a,b),g)
    eq('Bézout 252,198',4*252-5*198,18);eq('Bézout 35,12',3*12-35,1)
    for a,inv,mod in [(3,5,7),(12,3,35),(7,15,26),(5,21,26)]:eq(f'Inverse {a} modulo {mod}',(a*inv)%mod,1)
    k=s.symbols('k',integer=True)
    eq('Diophantienne famille 15,21',15*(-1+7*k)+21*(1-5*k),6)
    eq('Diophantienne famille 3,5',3*(2+5*k)+5*(5-3*k),31)
    eq('Solutions positives 3,5',int([j for j in range(-20,20) if 2+5*j>=0 and 5-3*j>=0]==[0,1]),1)
    eq('223 premier',int(s.isprime(223)),1);eq('30031 composé',59*509,30031)
    eq('360 facteurs',2**3*3**2*5,360);eq('84 facteurs',2**2*3*7,84)
    eq('Nombre diviseurs 360',s.divisor_count(360),24);eq('PPCM 360,84',s.ilcm(360,84),2520)
    eq('RSA n55 chiffrement',pow(7,3,55),13);eq('RSA n55 déchiffrement',pow(13,27,55),7)
    eq('RSA n77 chiffrement',pow(2,7,77),51);eq('RSA n77 déchiffrement',pow(51,43,77),2)
    for letter,code in [(12,9),(0,3),(19,6)]:eq('Chiffrement MAT '+str(letter),(7*letter+3)%26,code);eq('Déchiffrement MAT '+str(code),(15*(code-3))%26,letter)
    A=s.Matrix([[1,2],[3,4]]);B=s.Matrix([[0,1],[1,0]])
    eq('Produit AB',A*B,s.Matrix([[2,1],[4,3]]));eq('Produit BA',B*A,s.Matrix([[3,4],[1,2]]))
    C=s.Matrix([[2,1],[1,1]]);eq('Inverse ordre2',C.inv(),s.Matrix([[1,-1],[-1,2]]));eq('Système ordre2',C.inv()*s.Matrix([5,3]),s.Matrix([2,1]))
    T=s.Matrix([[1,1,0],[0,1,1],[0,0,1]]);eq('Inverse ordre3',T.inv(),s.Matrix([[1,-1,1],[0,1,-1],[0,0,1]]));eq('Système ordre3',T.inv()*s.Matrix([3,5,2]),s.Matrix([0,3,2]))
    R=s.Matrix([[0,-1],[1,0]]);S=s.diag(1,-1);eq('Rotation',R*s.Matrix([2,1]),s.Matrix([-1,2]));eq('Rotation carré',R**2,-s.eye(2));eq('RS',R*S,s.Matrix([[0,1],[1,0]]));eq('SR',S*R,s.Matrix([[0,-1],[-1,0]]))
    U=s.Matrix([[1,1],[0,1]]);V=s.Matrix([[3,1],[0,2]]);PP=s.Matrix([[1,-1],[0,1]])
    eq('Décomposition guidée',PP*s.diag(3,2)*PP.inv(),V)
    for n in [0,1,2,4,5,10,20]:
        eq('Cisaillement puissance '+str(n),U**n,s.Matrix([[1,n],[0,1]]))
        eq('Triangulaire puissance '+str(n),V**n,s.Matrix([[3**n,3**n-2**n],[0,2**n]]))
        eq('Ordre3 puissance '+str(n),T**n,s.Matrix([[1,n,n*(n-1)//2],[0,1,n],[0,0,1]]))
    AA=s.diag(s.Rational(1,2),s.Rational(1,4));CC=s.Matrix([1,3]);LL=s.Matrix([2,4]);eq('Équilibre affine colonne',AA*LL+CC,LL)
    for n in [0,1,2,7]:eq('Évolution affine '+str(n),LL-AA**n*LL,s.Matrix([2*(1-s.Rational(1,2)**n),4*(1-s.Rational(1,4)**n)]))
    G=s.Matrix([[0,1,1,0],[1,0,1,0],[1,1,0,1],[0,0,1,0]])
    eq('Adjacence degrés',s.Matrix([sum(G.row(j)) for j in range(4)]),s.Matrix([2,2,3,1]));eq('Parcours A vers D longueur2',(G**2)[0,3],1);eq('Retours A longueur2',(G**2)[0,0],2)
    cyc=s.Matrix([[0,1,0],[0,0,1],[1,0,0]]);eq('Cycle orienté cube',cyc**3,s.eye(3));eq('Chemin orienté longueur4',(cyc**4)[0,1],1)
    route=[0,1,2,0,3,1,4,2,3,4,0];edges={tuple(sorted((a,b))) for a,b in zip(route,route[1:])};eq('Euler K5 toutes arêtes distinctes',len(edges),10)
    P=s.Matrix([[s.Rational(4,5),s.Rational(1,5)],[s.Rational(3,10),s.Rational(7,10)]]);pi=s.Matrix([[s.Rational(3,5),s.Rational(2,5)]])
    eq('Transition P²',P**2,s.Matrix([[s.Rational(7,10),s.Rational(3,10)],[s.Rational(9,20),s.Rational(11,20)]]));eq('Invariant 2états',pi*P,pi)
    P3=s.Matrix([[s.Rational(1,2),s.Rational(1,2),0],[s.Rational(1,4),s.Rational(1,2),s.Rational(1,4)],[0,s.Rational(1,2),s.Rational(1,2)]]);pi3=s.Matrix([[s.Rational(1,4),s.Rational(1,2),s.Rational(1,4)]])
    eq('Invariant 3états',pi3*P3,pi3)
    for n in [0,1,2,5,9,12]:
        a=s.Rational(3,5)+s.Rational(2,5)*s.Rational(1,2)**n
        eq('Distribution 2états '+str(n),s.Matrix([[1,0]])*P**n,s.Matrix([[a,1-a]]))
        if n>=1:eq('Distribution 3états '+str(n),s.Matrix([[1,0,0]])*P3**n,s.Matrix([[s.Rational(1,4)+s.Rational(1,2)**(n+1),s.Rational(1,2),s.Rational(1,4)-s.Rational(1,2)**(n+1)]]))
    RE=s.Matrix([[0,1,0],[s.Rational(1,2),0,s.Rational(1,2)],[0,1,0]]);eq('Ehrenfest invariant',pi3*RE,pi3);eq('Ehrenfest paresseuse',(s.eye(3)+RE)/2,P3)
    PR=s.Matrix([[s.Rational(1,20),s.Rational(19,40),s.Rational(19,40)],[s.Rational(9,10),s.Rational(1,20),s.Rational(1,20)],[s.Rational(9,10),s.Rational(1,20),s.Rational(1,20)]]);pr=s.Matrix([[s.Rational(18,37),s.Rational(19,74),s.Rational(19,74)]])
    eq('Classement invariant',pr*PR,pr)
    for n in [1,2,10]:eq('Classement récurrence '+str(n),(s.Matrix([[1,0,0]])*PR**n)[0,0],s.Rational(18,37)+(1-s.Rational(18,37))*(-s.Rational(17,20))**n)
    eq('Interpolation',s.Matrix([[1,0,0],[1,1,1],[1,2,4]])*s.Matrix([1,0,2]),s.Matrix([1,3,9]))
    approx('Spirale seuil',1+2*math.log(100)/math.log(2),14.288,3)
else:
    raise ValueError('Option non encore implémentée')
target=ROOT/('livre-maths-'+sys.argv[1])/'build/calculs-verifies.json'
target.write_text(json.dumps(dict(controles=len(records),echecs=sum(not r['valide'] for r in records),resultats=records),ensure_ascii=False,indent=2),encoding='utf8')
for r in records:
    if not r['valide']:print('ECHEC',r)
print('Calculs contrôlés :',len(records),'Échecs :',sum(not r['valide'] for r in records))
sys.exit(1 if any(not r['valide'] for r in records) else 0)
