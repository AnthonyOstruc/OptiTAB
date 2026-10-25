"""Questions flash d’automatismes (partie transversale « Automatismes » du programme 2026).

Chaque question : (énoncé, corrigé, contrôle exécutable, bloc du programme, repères officiels).
Repères officiels (annexe du BO n° 14 du 2 avril 2026, partie « Automatismes ») :
C1 comparer par différence ou quotient ; C2 fractions simples ; C3 puissances ;
C4 changements d’écriture ; C5 ordre de grandeur ; C6 vraisemblance ; C7 conversions ;
C8 calcul littéral élémentaire ; C9 développer, factoriser ; C10 équations et inéquation ;
C11 isoler une variable ; C12 application numérique ; P1 proportion sous plusieurs formes ;
P2 partie et tout ; E1 formulation additive et multiplicative ; F1 images et antécédents
graphiques ; F2 équation de courbe ; F3 fonctions linéaires et affines ; G1 droite graduée ;
G2 coordonnées dans un repère ; G3 périmètres, aires, volumes ; G4 Pythagore et Thalès ;
G5 trigonométrie ; S1 graphiques usuels ; S2 indicateurs ; S3 boîtes à moustaches ;
R1 probabilité entre 0 et 1 ; R2 événement contraire ; R3 somme des issues ; R4 Card(A)/Card(Ω).
"""

REPERES_AUTOMATISMES = {
 'C1':'Comparer deux nombres par leur différence ou, s’ils sont strictement positifs, par leur quotient',
 'C2':'Opérations et comparaisons entre fractions simples',
 'C3':'Opérations sur les puissances',
 'C4':'Passer d’une écriture d’un nombre à une autre (décimale, fractionnaire, pourcentage)',
 'C5':'Estimer un ordre de grandeur',
 'C6':'S’assurer de la vraisemblance, de la cohérence d’un résultat',
 'C7':'Conversions d’unités : longueurs, aires, volumes, contenances, durées, vitesses, masses',
 'C8':'Calcul littéral élémentaire (expressions additives et multiplicatives)',
 'C9':'Développer, factoriser, réduire une expression algébrique simple',
 'C10':'Résoudre x² = a, ax + b = cx + d, a/x = b ou une inéquation du premier degré',
 'C11':'Isoler une variable dans une égalité qui en comporte plusieurs',
 'C12':'Effectuer une application numérique d’une formule',
 'P1':'Calculer, appliquer, exprimer une proportion sous différentes formes',
 'P2':'Calculer une partie connaissant le tout, ou le tout connaissant une partie',
 'E1':'Passer d’une formulation additive à une formulation multiplicative',
 'F1':'Déterminer graphiquement des images et des antécédents',
 'F2':'Exploiter une équation de courbe (appartenance d’un point, calcul de coordonnées)',
 'F3':'Reconnaître une fonction linéaire, affine ; leur représentation est une droite',
 'G1':'Sur une droite graduée, repérer ou placer un point d’abscisse relative',
 'G2':'Dans un repère orthogonal, lire ou placer un point de coordonnées données',
 'G3':'Calculer des périmètres, des aires et des volumes',
 'G4':'Application simple du théorème de Pythagore, du théorème de Thalès',
 'G5':'Lignes trigonométriques dans le triangle rectangle : cosinus, sinus, tangente',
 'S1':'Lire et commenter des graphiques usuels',
 'S2':'Calculer et interpréter moyenne, médiane, quartiles selon la présentation des données',
 'S3':'Comparer des distributions à l’aide de boîtes à moustaches',
 'R1':'Savoir qu’une probabilité est un nombre entre 0 et 1',
 'R2':'Calculer la probabilité de l’événement contraire',
 'R3':'Probabilité d’un événement comme somme des probabilités de ses issues',
 'R4':'Utiliser P(A) = Card(A)/Card(Ω) dans le cas de l’équiprobabilité',
}

DROITE_GRADUEE = r'''\par\smallskip\begin{tikzpicture}[x=1.75cm,font=\small]
\draw[otMuted,->](-2.3,0)--(1.35,0);
\foreach \k in {-8,...,4}{\draw[otMuted](\k/4,-.06)--(\k/4,.06);}
\foreach \x in {-2,-1,0,1}{\draw[otMuted](\x,-.11)--(\x,.11);\node[below=1.5mm,inner sep=1pt]at(\x,0){$\x$};}
\fill[otNavy](-1.25,0)circle(1.8pt)node[above=1mm]{$A$};\fill[otNavy](.75,0)circle(1.8pt)node[above=1mm]{$B$};
\end{tikzpicture}'''

COURBE_FLASH = r'''\begin{center}\begin{tikzpicture}[x=.62cm,y=.42cm,font=\small]
\draw[otRule!70,step=1](-3,-3)grid(5,4);\draw[otMuted,->](-3,0)--(5.3,0)node[right]{$x$};\draw[otMuted,->](0,-3)--(0,4.3)node[above]{$y$};
\foreach \x in {-2,-1,0,1,2,3,4}{\node[below,inner sep=1.5pt]at(\x,-3){$\x$};}\foreach \y in {-2,-1,0,1,2,3}{\node[left,inner sep=1.5pt]at(-3,\y){$\y$};}
\draw[geoTrait](-2,3)--(0,-1)--(4,3);\node[otNavy,above right]at(4,3){$\mathcal C_f$};
\fill[otGreenDark](3,-2)circle(2pt)node[right]{$M$};
\end{tikzpicture}\par\legende{Courbe de $f$ formée de deux segments, et point $M$. Repère orthogonal, graduations lues sur les bords.}\end{center}'''

SERIES = [
('A', 'Nombres, calculs et grandeurs', [
(r"""Calculer $\dfrac23+\dfrac34$, puis comparer $\dfrac58$ et $\dfrac35$.""",
 r"""$\dfrac8{12}+\dfrac9{12}=\res{\dfrac{17}{12}}$ ; $\dfrac{25}{40}>\dfrac{24}{40}$, donc $\res{\dfrac58>\dfrac35}$.""",
 'assert Rational(2,3)+Rational(3,4)==Rational(17,12) and Rational(5,8)>Rational(3,5)', 'Calcul', ['C2', 'C1']),
(r"""Écrire $\dfrac{2^5\times2^{-2}}{2^4}$ sous la forme $2^n$.""",
 r"""$2^{5-2-4}=\res{2^{-1}}=0{,}5$.""",
 'assert Rational(2**5)*Rational(2)**-2/2**4==Rational(2)**-1', 'Calcul', ['C3']),
(r"""Écrire $0{,}35$ sous forme de fraction irréductible, puis de pourcentage.""",
 r"""$0{,}35=\dfrac{35}{100}=\res{\dfrac7{20}}=\res{35\,\%}$.""",
 'assert Rational(35,100)==Rational(7,20)', 'Calcul', ['C4', 'P1']),
(r"""Donner un ordre de grandeur de $49{,}7\times0{,}21$.""",
 r"""$50\times0{,}2=\res{10}$ ; le produit exact vaut 10,437.""",
 'assert abs(Rational(497,10)*Rational(21,100)-10)<1 and Rational(497,10)*Rational(21,100)==Rational(10437,1000)', 'Calcul', ['C5']),
(r"""Comparer $a=\dfrac{1001}{1000}$ et $b=\dfrac{1000}{999}$ par leur quotient.""",
 r"""$\dfrac ab=\dfrac{1001\times999}{1000^2}=\dfrac{999\,999}{1\,000\,000}<1$ et $b>0$, donc $\res{a<b}$.""",
 'assert Rational(1001,1000)/Rational(1000,999)==Rational(999999,1000000) and Rational(1001,1000)<Rational(1000,999)', 'Calcul', ['C1']),
(r"""Convertir 90~km/h en m/s, puis $2{,}5$~m$^2$ en cm$^2$.""",
 r"""$90\,000/3600=\res{25\text{ m/s}}$ ; $2{,}5\times10\,000=\res{25\,000\text{ cm}^2}$.""",
 'assert Rational(90000,3600)==25 and Rational(25,10)*10000==25000', 'Calcul', ['C7']),
(r"""Simplifier $-(3-x)$ et $\dfrac2{3/4}$.""",
 r"""$-(3-x)=\res{x-3}$ ; diviser par $\dfrac34$ revient à multiplier par $\dfrac43$ : $\res{\dfrac83}$.""",
 'assert expand(-(3-x))==x-3 and 2/Rational(3,4)==Rational(8,3)', 'Calcul', ['C8']),
(r"""« Diminuer de 8\,\% » revient à multiplier par quel nombre ? Que signifie « multiplier par 1,15 » ?""",
 r"""$1-0{,}08=\res{0{,}92}$ ; multiplier par 1,15, c’est $\res{\text{augmenter de }15\,\%}$.""",
 'assert 1-Rational(8,100)==Rational(92,100) and Rational(115,100)-1==Rational(15,100)', 'Évolutions', ['E1']),
(r"""Un calcul de probabilité donne $1{,}2$. Que conclure ?""",
 r"""C’est $\res{\text{impossible}}$ : une probabilité est comprise entre 0 et 1. Il faut reprendre le calcul.""",
 'assert not (0<=Rational(12,10)<=1)', 'Probabilités', ['R1', 'C6']),
(r"""$ABC$ est rectangle en $A$, avec $AB=4$ et $BC=8$. Calculer $\cos\widehat{ABC}$ et en déduire l’angle.""",
 r"""$\cos\widehat{ABC}=\dfrac{AB}{BC}=\res{\dfrac12}$, donc $\res{\widehat{ABC}=60^\circ}$.""",
 'assert Rational(4,8)==Rational(1,2) and cos(pi/3)==Rational(1,2)', 'Géométrie', ['G5']),
]),
('B', 'Calcul littéral, équations et proportions', [
(r"""Développer $(2x+3)^2$.""",
 r"""$\res{4x^2+12x+9}$ ; le double produit vaut $12x$.""",
 'assert expand((2*x+3)**2)==4*x**2+12*x+9', 'Calcul', ['C9']),
(r"""Factoriser $5x^2-15x$, puis $x^2-49$.""",
 r"""$\res{5x(x-3)}$ ; $\res{(x-7)(x+7)}$.""",
 'assert expand(5*x*(x-3))==5*x**2-15*x and expand((x-7)*(x+7))==x**2-49', 'Calcul', ['C9']),
(r"""Résoudre $x^2=36$.""",
 r"""$\res{S=\{-6;6\}}$ : un nombre et son opposé ont le même carré.""",
 'assert solveset(x**2-36,x,domain=S.Reals)==FiniteSet(-6,6)', 'Calcul', ['C10']),
(r"""Résoudre $3x-4=x+6$.""",
 r"""$2x=10$, donc $\res{x=5}$.""",
 'assert solve(3*x-4-(x+6),x)==[5]', 'Calcul', ['C10']),
(r"""Résoudre $\dfrac6x=2$ pour $x\ne0$.""",
 r"""$6=2x$, donc $\res{x=3}$, valeur autorisée.""",
 'assert solveset(6/x-2,x,domain=S.Reals)==FiniteSet(3)', 'Calcul', ['C10']),
(r"""Résoudre $-2x+5>1$.""",
 r"""$-2x>-4$ ; diviser par $-2$ renverse le sens : $\res{x<2}$.""",
 'assert solve_univariate_inequality(-2*x+5>1,x,relational=False)==Interval.open(-oo,2)', 'Calcul', ['C10']),
(r"""Isoler $R$ dans $U=RI$ ($I\ne0$), puis $h$ dans $V=\dfrac13Bh$ ($B>0$).""",
 r"""$\res{R=\dfrac UI}$ ; $\res{h=\dfrac{3V}B}$.""",
 'assert solve(y-p*x,p)==[y/x] and solve(y-Rational(1,3)*p*x,x)==[3*y/p]', 'Calcul', ['C11']),
(r"""Calculer $E=\dfrac12mv^2$ pour $m=2$~kg et $v=3$~m/s.""",
 r"""$\dfrac12\times2\times3^2=\res{9\text{ J}}$.""",
 'assert Rational(1,2)*2*3**2==9', 'Calcul', ['C12']),
(r"""9 élèves représentent 30\,\% d’une classe. Combien d’élèves compte la classe ?""",
 r"""$9/0{,}30=\res{30\text{ élèves}}$.""",
 'assert 9/Rational(30,100)==30', 'Proportions', ['P2']),
(r"""Calculer 15\,\% de 240, puis écrire 15\,\% sous forme décimale et fractionnaire.""",
 r"""$0{,}15\times240=\res{36}$ ; $15\,\%=0{,}15=\res{\dfrac3{20}}$.""",
 'assert Rational(15,100)*240==36 and Rational(15,100)==Rational(3,20)', 'Proportions', ['P2', 'P1']),
]),
('C', 'Géométrie et mesures', [
(r"""Lire les abscisses des points $A$ et $B$."""+DROITE_GRADUEE,
 r"""Chaque unité est partagée en 4 : un pas vaut $0{,}25$. $\res{A(-1{,}25)}$ et $\res{B(0{,}75)}$.""",
 'assert -2+3*Rational(1,4)==Rational(-5,4) and 0+3*Rational(1,4)==Rational(3,4)', 'Géométrie', ['G1']),
(r"""Périmètre et aire d’un disque de rayon 3~cm.""",
 r"""$\res{6\pi\text{ cm}}$ et $\res{9\pi\text{ cm}^2}$.""",
 'assert 2*pi*3==6*pi and pi*3**2==9*pi', 'Géométrie', ['G3']),
(r"""Aire d’un triangle de base 7~cm et de hauteur 4~cm.""",
 r"""$7\times4/2=\res{14\text{ cm}^2}$.""",
 'assert Rational(7*4,2)==14', 'Géométrie', ['G3']),
(r"""Volume d’un pavé de 2~cm sur 3~cm sur 5~cm ; d’une pyramide de même base et même hauteur.""",
 r"""$\res{30\text{ cm}^3}$, puis $30/3=\res{10\text{ cm}^3}$.""",
 'assert 2*3*5==30 and Rational(30,3)==10', 'Géométrie', ['G3']),
(r"""Volume d’un cylindre, puis d’un cône, de rayon 2~cm et de hauteur 5~cm.""",
 r"""$\pi\times2^2\times5=\res{20\pi\text{ cm}^3}$ ; $\res{\dfrac{20\pi}3\text{ cm}^3}$.""",
 'assert pi*2**2*5==20*pi and pi*2**2*5/3==20*pi/3', 'Géométrie', ['G3']),
(r"""Volume d’un prisme droit de base 6~cm$^2$ et de hauteur 10~cm ; d’une boule de rayon 3~cm.""",
 r"""$\res{60\text{ cm}^3}$ ; $\dfrac43\pi\times3^3=\res{36\pi\text{ cm}^3}$.""",
 'assert 6*10==60 and Rational(4,3)*pi*3**3==36*pi', 'Géométrie', ['G3']),
(r"""Les côtés de l’angle droit d’un triangle rectangle mesurent 6~cm et 8~cm. Hypoténuse ?""",
 r"""$\sqrt{36+64}=\res{10\text{ cm}}$ (Pythagore).""",
 'assert sqrt(6**2+8**2)==10', 'Géométrie', ['G4']),
(r"""$M\in[AB]$, $N\in[AC]$, $(MN)\parallel(BC)$, $AM=2$, $AB=6$, $BC=9$. Calculer $MN$.""",
 r"""Thalès : $\dfrac{MN}{BC}=\dfrac{AM}{AB}=\dfrac13$, donc $\res{MN=3}$.""",
 'assert Rational(2,6)*9==3', 'Géométrie', ['G4']),
(r"""Triangle rectangle d’hypoténuse 10 et d’angle aigu $30^\circ$ : longueur du côté opposé ?""",
 r"""$10\sin30^\circ=10\times\dfrac12=\res5$.""",
 'assert 10*sin(pi/6)==5', 'Géométrie', ['G5']),
(r"""Convertir $1{,}5$~L en cm$^3$, puis 2~h~15~min en heures.""",
 r"""$\res{1500\text{ cm}^3}$ ; $2+\dfrac{15}{60}=\res{2{,}25\text{ h}}$.""",
 'assert Rational(15,10)*1000==1500 and 2+Rational(15,60)==Rational(9,4)', 'Calcul', ['C7']),
]),
('D', 'Fonctions, statistiques et probabilités', [
(r"""Lire sur la courbe l’image de 0 par $f$.""",
 r"""Le point de $\mathcal C_f$ d’abscisse 0 est $(0;-1)$ : $\res{f(0)=-1}$.""",
 'f=Piecewise((-2*x-1,x<=0),(x-1,True))\nassert [f.subs(x,a) for a in [-2,0,4]]==[3,-1,3] and f.subs(x,0)==-1', 'Fonctions', ['F1']),
(r"""Lire les antécédents de 1 par $f$.""",
 r"""La droite $y=1$ coupe $\mathcal C_f$ en $x=-1$ et $x=2$ : $\res{-1\text{ et }2}$.""",
 'assert solveset(-2*x-1-1,x,Interval(-2,0))==FiniteSet(-1) and solveset(x-1-1,x,Interval(0,4))==FiniteSet(2)', 'Fonctions', ['F1']),
(r"""Lire les coordonnées du point $M$.""",
 r"""$\res{M(3;-2)}$ : abscisse d’abord, ordonnée ensuite.""",
 'M=Point(3,-2)\nassert (M.x,M.y)==(3,-2)', 'Géométrie', ['G2']),
(r"""$A(2;7)$ est-il sur la courbe d’équation $y=x^2+3$ ? Ordonnée du point d’abscisse $-1$ ?""",
 r"""$2^2+3=7$ : $\res{\text{oui}}$. Pour $x=-1$ : $\res{y=4}$.""",
 'assert 2**2+3==7 and (-1)**2+3==4', 'Fonctions', ['F2']),
(r"""Parmi $f(x)=3x$, $g(x)=2x-1$ et $h(x)=x^2$, lesquelles sont affines ? linéaires ?""",
 r"""$f$ est $\res{\text{linéaire}}$ (donc affine), $g$ est $\res{\text{affine}}$ ; leurs courbes sont des droites. $h$ n’est pas affine.""",
 'assert (3*x).subs(x,0)==0 and expand(x**2).as_poly(x).degree()==2', 'Fonctions', ['F3']),
(r"""Dans un diagramme semi-circulaire, quelle proportion représente un secteur de $45^\circ$ ?""",
 r"""Le demi-disque vaut $180^\circ$ : $\dfrac{45}{180}=\res{\dfrac14=25\,\%}$.""",
 'assert Rational(45,180)==Rational(1,4)', 'Statistiques', ['S1']),
(r"""Moyenne et médiane de la série $3$ ; $5$ ; $6$ ; $10$.""",
 r"""Moyenne $24/4=\res6$ ; médiane $(5+6)/2=\res{5{,}5}$.""",
 'assert Rational(3+5+6+10,4)==6 and Rational(5+6,2)==Rational(11,2)', 'Statistiques', ['S2']),
(r"""Classes $[0;10[$ d’effectif 3 et $[10;20[$ d’effectif 7 : estimer la moyenne avec les centres.""",
 r"""$\dfrac{3\times5+7\times15}{10}=\res{12}$.""",
 'assert Rational(3*5+7*15,10)==12', 'Statistiques', ['S2']),
(r"""Boîtes à moustaches (min ; $Q_1$ ; médiane ; $Q_3$ ; max) : $A=(2;6;9;12;15)$ et $B=(4;7;9;10;14)$. Comparer.""",
 r"""Même médiane 9. Écarts interquartiles 6 et 3 : $\res{B\text{ est moins dispersée}}$ autour de sa médiane.""",
 'assert 12-6==6 and 10-7==3', 'Statistiques', ['S3']),
(r"""On tire au hasard une carte parmi dix cartes numérotées de 1 à 10. Probabilité d’un multiple de 3 ? de l’événement contraire ?""",
 r"""Issues 3, 6, 9, chacune de probabilité $\dfrac1{10}$ : $P(A)=\dfrac{\operatorname{Card}(A)}{\operatorname{Card}(\Omega)}=\res{\dfrac3{10}}$ ; contraire : $1-\dfrac3{10}=\res{\dfrac7{10}}$.""",
 'assert len([n for n in range(1,11) if n%3==0])==3 and 1-Rational(3,10)==Rational(7,10)', 'Probabilités', ['R4', 'R3', 'R2']),
]),
]

FIGURES_SERIES = {'D': COURBE_FLASH}
