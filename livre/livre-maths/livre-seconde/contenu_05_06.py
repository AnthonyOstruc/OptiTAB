from modele import *

chapitre(5,'fonctions','Fonctions et représentations','2 · Fonctions',
 'Images · Antécédents · Domaines · Modèles',
 ['Passer d’une formule à un tableau ou à une courbe.','Déterminer images, antécédents et domaine.','Choisir un modèle continu ou discret.'],
 ['Calcul littéral et résolution d’équations.'],[
r'''\essSection{1}{Une dépendance entre deux grandeurs}
\begin{definition}Une fonction $f$ associe à chaque nombre $x$ de son ensemble de définition $D_f$ un unique nombre $f(x)$, appelé image de $x$. Un antécédent de $y$ est un nombre $x\in D_f$ tel que $f(x)=y$. Un nombre peut avoir plusieurs antécédents, un seul, ou aucun.\end{definition}
\begin{exemple}Pour $f(x)=x^2-1$, $f(3)=8$. Le nombre 8 a deux antécédents : $-3$ et 3. Le nombre $-2$ n’en a aucun, car $x^2\ge0$.\end{exemple}
\begin{savoirfaire}[Déterminer le domaine]
Pour un quotient, le dénominateur doit être non nul. Pour une racine carrée, l’expression sous la racine doit être positive ou nulle. Cumuler les contraintes si plusieurs opérations sont présentes.
\end{savoirfaire}
\begin{exemple}$f(x)=\sqrt{x-2}$ est définie sur $[2;+\infty[$ ; $g(x)=1/(x+3)$ sur $\mathbb R\setminus\{-3\}$.\end{exemple}
\begin{attention}L’image d’un nombre est unique. Chercher les antécédents demande de résoudre une équation et d’en conserver toutes les solutions autorisées.\end{attention}''',
r'''\essSection{2}{Courbes et changements de registre}
\begin{definition}La courbe $\mathcal C_f$ est l’ensemble des points $(x;y)$ tels que $x\in D_f$ et $y=f(x)$. Ainsi $A(a;b)\in\mathcal C_f$ si et seulement si $a\in D_f$ et $b=f(a)$.\end{definition}
\begin{savoirfaire}[Lire sur une courbe]
Pour lire $f(a)$, partir de $a$ sur l’axe horizontal et rejoindre la courbe verticalement. Pour les antécédents de $b$, chercher toutes les intersections avec la droite horizontale $y=b$, puis lire leurs abscisses.
\end{savoirfaire}
\begin{propriete}Les solutions de $f(x)=g(x)$ sont les abscisses des intersections des deux courbes. Pour $f(x)<g(x)$, repérer les abscisses où la courbe de $f$ est en dessous de celle de $g$.\end{propriete}
\begin{exemple}[Un modèle discret]Le nombre de places occupées après $n$ réservations peut être décrit par $u(n)=2n+5$, avec $n\in\mathbb N$. Les points sont isolés : on ne doit pas attribuer un sens à « 2,4 réservations ».\end{exemple}
\otIntertitre{Avec un tableur}
Pour $f(x)=x^2-1$, placer les abscisses en colonne A ; écrire \code{=A2*A2-1} en B2 et recopier. Le tableau aide à tracer et conjecturer. Il ne prouve pas à lui seul qu’il n’existe aucune autre solution.'''
],[
E('Calculer des images',r"""Pour $f(x)=2x^2-3x+1$, calculer $f(0)$, $f(2)$ et $f(-1)$.""",
r"""On remplace chaque occurrence de $x$ en respectant les parenthèses. $f(0)=\res1$ ; $f(2)=2\times4-6+1=\res3$ ; $f(-1)=2\times1+3+1=\res6$. En particulier $-3(-1)=+3$, ce qui explique le signe dans le dernier calcul.""",
'Substituer une valeur à toutes les occurrences de la variable.','assert [(2*x*x-3*x+1).subs(x,a) for a in [0,2,-1]]==[1,3,6]'),
E('Lire un tableau',r"""On donne les valeurs suivantes. Indiquer l’image de $-1$, puis les antécédents de 4 présents dans ce tableau."""+tableau(['$x$','$-2$','$-1$','$0$','$1$','$2$'],[['$f(x)$','$4$','$1$','$0$','$1$','$4$']]),
r"""La colonne d’abscisse $-1$ donne $\res{f(-1)=1}$. Les colonnes où la deuxième ligne vaut 4 ont pour abscisses $-2$ et 2. Ce sont les deux antécédents visibles dans le tableau. Sans autre information sur la fonction, on ne peut pas exclure d’autres antécédents hors de ces cinq valeurs.""",
'Lire les colonnes dans le sens correspondant à la question.','assert (-1)**2==1 and [a for a in [-2,-1,0,1,2] if a*a==4]==[-2,2]'),
E('Antécédent d’une fonction affine',r"""Pour $f(x)=3x-5$, déterminer l’antécédent de 7.""",
r"""On cherche $x$ tel que $3x-5=7$. Cela donne $3x=12$, donc $\res{x=4}$. Comme le coefficient 3 est non nul, il n’y a qu’un antécédent. Contrôle : $f(4)=12-5=7$.""",
'Traduire le mot antécédent par une équation.','assert solve(3*x-5-7,x)==[4]'),
E('Appartenir à une courbe',r"""Pour $f(x)=x^2+2$, les points $A(1;3)$, $B(-2;6)$ et $C(3;10)$ appartiennent-ils à $\mathcal C_f$ ?""",
r"""On compare l’ordonnée annoncée à l’image de l’abscisse. $f(1)=3$, donc $A$ appartient à la courbe ; $f(-2)=6$, donc $B$ aussi. Mais $f(3)=11\ne10$, donc $C$ n’y appartient pas. Une proximité sur un dessin ne remplacerait pas ces égalités exactes.""",
'Tester l’égalité y = f(x) point par point.','assert 1**2+2==3 and (-2)**2+2==6 and 3**2+2!=10',figure='fonction-appartenance'),
E('Le domaine d’un quotient',r"""Déterminer le domaine de $g(x)=\dfrac{5}{2x-6}$, puis calculer $g(4)$.""",
r"""Il faut $2x-6\ne0$, donc $x\ne3$. Le domaine est $\res{D_g=\mathbb R\setminus\{3\}}$. À $x=4$, le dénominateur vaut 2 et $\res{g(4)=5/2}$. Il n’existe aucune image de 3 par cette formule.""",
'Rechercher les zéros du dénominateur avant de calculer.','assert solve(2*x-6,x)==[3] and Rational(5,2*4-6)==Rational(5,2)'),
E('Un domaine avec deux contraintes',r"""Déterminer le domaine de $h(x)=\dfrac{\sqrt{x+1}}{x-2}$.""",
r"""La racine impose $x+1\ge0$, soit $x\ge-1$. Le dénominateur impose $x\ne2$. On réunit ces deux contraintes : $\res{D_h=[-1;2[\cup]2;+\infty[}$. La valeur $-1$ est autorisée puisque la racine de 0 existe et que le dénominateur vaut alors $-3$.""",
'Prendre l’intersection des conditions de chaque opération.','assert Complement(Interval(-1,oo),FiniteSet(2))==Union(Interval.Ropen(-1,2),Interval.open(2,oo))'),
E('Plusieurs antécédents',r"""Pour $f(x)=(x-1)^2$, chercher les antécédents de 9, de 0 et de $-1$.""",
r"""$(x-1)^2=9$ donne $x-1=-3$ ou 3, donc $\res{x=-2\text{ ou }4}$. Pour 0, il faut $x-1=0$, d’où l’unique antécédent 1. Pour $-1$, il n’y a aucun antécédent réel puisqu’un carré ne peut être négatif.""",
'Ramener chaque recherche à une équation de carré.','assert solveset((x-1)**2-9,x,domain=S.Reals)==FiniteSet(-2,4) and solveset((x-1)**2+1,x,domain=S.Reals)==S.EmptySet',figure='antecedents-parabole'),
E('Formule et programme de calcul',r"""Un programme multiplie l’entrée par 4, soustrait 6 puis divise le résultat par 2. Donner sa fonction. Quelle entrée produit 11 ?""",
r"""En notant $x$ l’entrée, le résultat est $(4x-6)/2=\res{2x-3}$. Pour produire 11, on résout $2x-3=11$, donc $\res{x=7}$. Faire fonctionner le programme avec 7 donne $(28-6)/2=11$. L’ordre des opérations est décrit par les parenthèses.""",
'Transformer les étapes du programme en une seule expression.','assert expand((4*x-6)/2)==2*x-3 and solve(2*x-3-11,x)==[7]'),
E('Intersections de deux courbes',r"""Comparer $f(x)=x^2$ et $g(x)=x+2$ : trouver leurs intersections, puis les abscisses où $f(x)\le g(x)$.""",
r"""Les intersections satisfont $x^2-x-2=0$, soit $(x-2)(x+1)=0$. Elles sont $\res{(-1;1)\text{ et }(2;4)}$. Le produit est négatif entre les racines ; ainsi $\res{f(x)\le g(x)\iff x\in[-1;2]}$. Le graphique confirme que la parabole est alors sous la droite.""",
'Résoudre l’égalité, puis étudier le signe de la différence.','assert solveset(x*x-x-2,x,domain=S.Reals)==FiniteSet(-1,2) and solve_univariate_inequality(x*x<=x+2,x,relational=False)==Interval(-1,2)',figure='intersection-fonctions'),
E('Une lecture graphique précise',r"""La ligne brisée représente une fonction affine sur chaque morceau et passe par $(-2;1)$, $(0;3)$, $(2;-1)$ et $(4;1)$. Lire $f(0)$ et tous les antécédents de 1.""",
r"""Le sommet d’abscisse 0 donne $\res{f(0)=3}$. La droite $y=1$ coupe la ligne en $x=-2$, $x=1$ et $x=4$. Sur le segment central, l’ordonnée descend de 3 à $-1$ en deux unités : elle vaut bien 1 à $x=1$. Les antécédents sont donc $\res{-2,1,4}$.""",
'Explorer tous les morceaux de la courbe, y compris les extrémités.','assert 3-2*1==1 and [-2,1,4]==sorted([-2,1,4])',figure='fonction-morceaux'),
E('Un tarif avec plafond',r"""Un service facture 3 euros par heure, sans dépasser 15 euros pour la journée. Pour $0\le t\le8$, exprimer le coût $C(t)$ et trouver toutes les durées qui coûtent 12 euros puis 15 euros.""",
r"""Jusqu’à 5 h, $C(t)=3t$ ; ensuite $C(t)=15$. Le coût de 12 euros est obtenu seulement pour $t=4$. Le coût de 15 euros est atteint pour toutes les durées $\res{t\in[5;8]}$. Le modèle est continu si les fractions d’heure sont facturées proportionnellement, ce que l’énoncé suppose ici.""",
'Décrire séparément la partie proportionnelle et le plafond.','assert 3*4==12 and all(min(3*t,15)==15 for t in [5,6,7,8])',figure='tarif-plafond'),
E('Une quantité discrète',r"""Une salle contient 18 chaises avant l’installation de rangées de 6 chaises. On note $u(n)$ le total après $n$ rangées supplémentaires, $n\in\mathbb N$. Donner $u(n)$ ; 75 chaises sont-elles possibles ?""",
r"""Chaque rangée ajoute 6 : $\res{u(n)=18+6n}$. Obtenir 75 demanderait $n=(75-18)/6=9{,}5$, qui n’est pas entier. Ce total est donc impossible dans ce modèle. Les totaux voisins sont $u(9)=72$ et $u(10)=78$. Le domaine discret est essentiel pour conclure.""",
'Préciser le domaine avant d’accepter une solution algébrique.','assert Rational(75-18,6)==Rational(19,2) and 18+6*9==72 and 18+6*10==78'),
E('Deux formules, un même domaine ?',r"""Comparer les fonctions $f(x)=\dfrac{x^2-1}{x-1}$ et $g(x)=x+1$. Ont-elles le même domaine ? Leurs courbes sont-elles identiques ?""",
r"""$f$ est définie pour $x\ne1$ ; $g$ l’est pour tout réel. Sur le domaine de $f$, on simplifie $(x-1)(x+1)/(x-1)$, donc $f(x)=g(x)$. La courbe de $f$ est la droite de $g$ privée du point $(1;2)$. Les formules coïncident là où toutes deux sont définies, mais les fonctions n’ont pas le même domaine.""",
'Distinguer égalité des valeurs et égalité des fonctions.','assert cancel((x*x-1)/(x-1))==x+1 and (x-1).subs(x,1)==0'),
E('Concevoir un modèle de volume',r"""Un réservoir cylindrique de rayon 2 m contient une hauteur d’eau $h$ comprise entre 0 et 3 m. Donner $V(h)$, son domaine et la hauteur correspondant à $6\pi$ m$^3$.""",
r"""Le volume d’un cylindre est aire de base fois hauteur : $\res{V(h)=4\pi h}$, pour $\res{h\in[0;3]}$. L’équation $4\pi h=6\pi$ donne $\res{h=1{,}5\text{ m}}$. Cette hauteur appartient au domaine. La capacité totale est $12\pi$ m$^3$, donc le volume demandé est la moitié de la capacité.""",
'Associer une formule géométrique au domaine physique de la variable.','assert solve(4*pi*x-6*pi,x)==[Rational(3,2)]',figure='cylindre'),
E('Une conjecture issue d’un tableau',r"""Pour $f(x)=x^2-4x+3$, un tableau aux entiers $0,1,2,3,4$ suggère que $f(x)\ge-1$. Démontrer cette inégalité pour tout réel et déterminer le cas d’égalité.""",
r"""On réécrit $f(x)=(x-2)^2-1$. Un carré est positif ou nul, donc $f(x)\ge-1$ pour tout réel. L’égalité exige $(x-2)^2=0$, soit $\res{x=2}$. Le tableau proposait une piste ; la transformation algébrique prouve que l’inégalité reste vraie entre les valeurs testées et au-delà.""",
'Transformer une observation numérique en preuve par un carré.','assert expand((x-2)**2-1)==x*x-4*x+3 and solve((x-2)**2,x)==[2]')
],reperes=['Images, antécédents et courbes','Ensembles de définition','Équations et inéquations graphiques','Modèles continus et discrets'])

chapitre(6,'fonctions-reference','Les fonctions de référence','2 · Fonctions',
 'Affine · Carré · Cube · Inverse · Racine · Valeur absolue',
 ['Reconnaître les courbes et leurs domaines.','Comparer des images avec une fonction adaptée.','Résoudre des équations et inéquations de référence.'],
 ['Images, antécédents, ordre et racines.'],[
r'''\essSection{1}{Un répertoire de fonctions}
\begin{definition}Une fonction affine est de la forme $f(x)=mx+p$. Elle est linéaire si $p=0$. Sa courbe est une droite, de pente $m$ et d’ordonnée à l’origine $p=f(0)$. Pour $a\ne b$, le taux d’accroissement $\dfrac{f(b)-f(a)}{b-a}$ vaut toujours $m$ : quand $x$ augmente de 1, $f(x)$ varie de $m$.\end{definition}
\begin{propriete}
\begin{tabularx}{\linewidth}{@{}lYY@{}}\toprule
Fonction & Domaine & Repère utile\\\midrule
$x\mapsto x^2$ & $\mathbb R$ & Positive ; $(-x)^2=x^2$ : courbe symétrique par rapport à l’axe des ordonnées.\\
$x\mapsto x^3$ & $\mathbb R$ & Signe de $x$ ; $(-x)^3=-x^3$.\\
$x\mapsto1/x$ & $\mathbb R\setminus\{0\}$ & Signe de $x$ ; ne vaut jamais 0.\\
$x\mapsto\sqrt x$ & $[0;+\infty[$ & Positive ou nulle ; carré égal à $x$.\\
$x\mapsto|x|$ & $\mathbb R$ & Distance à 0 ; courbe en V.\\\bottomrule
\end{tabularx}
\end{propriete}
\begin{savoirfaire}[Valeur absolue]Pour $x\ge0$, $|x|=x$ ; pour $x\le0$, $|x|=-x$. La fonction est décroissante avant 0 et croissante après 0. Son minimum vaut 0.\end{savoirfaire}
\begin{attention}$\sqrt{x^2}=|x|$, et non toujours $x$. L’inverse n’est pas défini en 0 ; une racine carrée réelle n’est pas définie pour une entrée négative.\end{attention}''',
r'''\essSection{2}{Utiliser les courbes et les variations}
\begin{propriete}
La fonction carré est décroissante sur $]-\infty;0]$ et croissante sur $[0;+\infty[$. La fonction inverse est décroissante sur chacun des intervalles $]-\infty;0[$ et $]0;+\infty[$. Les fonctions cube et racine carrée sont croissantes sur leur domaine.
\end{propriete}
\begin{propriete}[Signe d’une fonction affine]
Si $m\ne0$, $f(x)=mx+p$ s’annule seulement en $x_0=-p/m$ ; $f(x)$ est du signe de $m$ pour $x>x_0$ et du signe contraire pour $x<x_0$. La droite est au-dessus de l’axe des abscisses exactement là où $f(x)>0$. Si $m=0$, $f$ garde le signe de $p$.
\begin{center}\renewcommand{\arraystretch}{1.25}\begin{tabular}{l|ccccc}\toprule
$x$ & $-\infty$ & & $-p/m$ & & $+\infty$\\\midrule
$mx+p$ avec $m>0$ (croissante) & & $-$ & $0$ & $+$ & \\
$mx+p$ avec $m<0$ (décroissante) & & $+$ & $0$ & $-$ & \\\bottomrule
\end{tabular}\end{center}
\end{propriete}
\begin{savoirfaire}[Comparer des images]
Identifier un intervalle sur lequel la fonction est monotone. Pour $0<a<b$, $a^2<b^2$, $\sqrt a<\sqrt b$ et $1/a>1/b$. Pour deux nombres négatifs, la comparaison des carrés se renverse.
\end{savoirfaire}
\begin{exemple}$-5<-2$ mais $25>4$. Pour $x\ge0$, $x^2-x=x(x-1)$ : la courbe du carré est sous la droite $y=x$ entre 0 et 1, et au-dessus pour $x>1$.\end{exemple}
\begin{savoirfaire}[Résoudre]
Pour $a\ge0$, $x^2\le a$ donne $-\sqrt a\le x\le\sqrt a$. Pour $b\ge0$, $\sqrt x\le b$ donne $0\le x\le b^2$. Avec un quotient, utiliser un tableau de signes plutôt que multiplier par une expression dont le signe est inconnu.
\end{savoirfaire}
\otIntertitre{Images mentales}
Retenir l’allure de chaque courbe, puis l’associer à son domaine, son signe et ses variations. Les planches d’exercices permettent de les tracer avec des échelles explicites.'''
],[
E('Une fonction affine',r"""Pour $f(x)=-2x+3$, donner la pente, l’ordonnée à l’origine et l’image de 4. Tracer la droite à l’aide de deux points.""",
r"""La pente est $\res{-2}$, l’ordonnée à l’origine est $\res3$. On a $f(4)=-8+3=\res{-5}$. Pour tracer, utiliser par exemple $(0;3)$ et $(1;1)$. Lorsque l’abscisse augmente de 1, l’ordonnée diminue de 2, conformément à la pente.""",
'Lire les coefficients puis utiliser deux points distincts.','assert -2*4+3==-5 and -2*1+3==1',figure='reference-affine'),
E('Comparer des carrés',r"""Comparer sans calculatrice $(-7)^2$ et $(-3)^2$, puis $0{,}4^2$ et $0{,}7^2$.""",
r"""Les distances à 0 valent 7 et 3, donc $\res{(-7)^2>(-3)^2}$. Sur les nombres positifs, la fonction carré est croissante : $0{,}4<0{,}7$ entraîne $\res{0{,}4^2<0{,}7^2}$. Les variations dépendent du côté de 0 où se trouvent les nombres.""",
'Localiser les entrées sur un intervalle de monotonie.','assert (-7)**2>(-3)**2 and Rational(4,10)**2<Rational(7,10)**2'),
E('La fonction inverse',r"""Calculer les images de $-4$, $1/2$ et 5 par la fonction inverse. Le nombre 0 a-t-il un antécédent ?""",
r"""Les images sont respectivement $\res{-1/4}$, $\res2$ et $\res{1/5}$. Le nombre 0 n’a aucun antécédent, car $1/x=0$ impliquerait $1=0$ après multiplication par un $x$ non nul. Attention : 0 n’a pas non plus d’image, puisque la fonction n’y est pas définie.""",
'Distinguer absence d’image et absence d’antécédent.','assert 1/Rational(-4)==-Rational(1,4) and 1/Rational(1,2)==2 and solveset(1/x,x,domain=S.Reals)==S.EmptySet',figure='reference-inverse'),
E('Racine et domaine',r"""Résoudre $\sqrt x=5$, puis $\sqrt x=-2$.""",
r"""Le domaine est $x\ge0$. Dans la première équation, les deux membres sont positifs : on peut élever au carré, ce qui donne $\res{x=25}$. Dans la seconde, le membre de gauche est positif ou nul et celui de droite négatif : il n’y a aucune solution. Élever au carré trop tôt aurait créé la fausse solution 4.""",
'Examiner les signes avant de mettre au carré.','assert sqrt(25)==5 and solveset(sqrt(x)+2,x,domain=S.Reals)==S.EmptySet',figure='reference-racine'),
E('La courbe en V',r"""Calculer $|-3|$, $|0|$ et $|2{,}5|$. Résoudre $|x|\le4$.""",
r"""Les trois valeurs sont $\res3$, $\res0$ et $\res{2{,}5}$. L’inégalité demande les nombres à distance au plus 4 de 0 : $\res{x\in[-4;4]}$. On retrouve sur la courbe en V les abscisses pour lesquelles l’ordonnée ne dépasse pas 4.""",
'Interpréter la valeur absolue comme distance à zéro.','assert abs(-3)==3 and solve_univariate_inequality(Abs(x)<=4,x,relational=False)==Interval(-4,4)',figure='reference-absolue'),
E('Une équation de cube',r"""Résoudre $x^3=-27$, puis comparer $(-1{,}2)^3$ et $(-1{,}1)^3$.""",
r"""Comme $(-3)^3=-27$ et que la fonction cube est strictement croissante, l’unique solution est $\res{x=-3}$. La même croissance donne $-1{,}2<-1{,}1\Rightarrow\res{(-1{,}2)^3<(-1{,}1)^3}$. Il n’y a pas de changement de sens pour le cube sur les négatifs.""",
'Utiliser la croissance de la fonction cube sur toute la droite réelle.','assert (-3)**3==-27 and (-Rational(12,10))**3<(-Rational(11,10))**3',figure='reference-cube'),
E('Une inéquation de carré',r"""Résoudre $x^2<9$ et $x^2\ge9$.""",
r"""Les valeurs frontières sont $-3$ et 3. Le carré est inférieur à 9 entre ces bornes : $\res{]-3;3[}$. Il est supérieur ou égal à 9 à l’extérieur : $\res{]-\infty;-3]\cup[3;+\infty[}$. Les solutions négatives sont aussi nécessaires que les positives.""",
'Lire les deux branches de la parabole.','assert solve_univariate_inequality(x*x<9,x,relational=False)==Interval.open(-3,3) and solve_univariate_inequality(x*x>=9,x,relational=False)==Union(Interval(-oo,-3),Interval(3,oo))',figure='reference-carre'),
E('Comparer des inverses',r"""Comparer $1/3$ et $1/7$, puis $1/(-5)$ et $1/(-2)$. Expliquer pourquoi on traite les deux paires séparément.""",
r"""Sur $]0;+\infty[$, l’inverse est décroissante : $3<7$ donne $\res{1/3>1/7}$. Sur $]-\infty;0[$, elle l’est aussi : $-5<-2$ donne $\res{-1/5>-1/2}$. On traite les paires séparément car 0 coupe le domaine ; on ne peut pas annoncer une décroissance sur toute la réunion des deux intervalles.""",
'Utiliser la monotonie sur un intervalle où la fonction est définie.','assert Rational(1,3)>Rational(1,7) and -Rational(1,5)>-Rational(1,2)'),
E('Carré et identité',r"""Pour $x\ge0$, résoudre $x^2\le x$ et préciser les cas d’égalité.""",
r"""On factorise $x^2-x=x(x-1)$. Sur $x\ge0$, ce produit est négatif ou nul exactement pour $0\le x\le1$. La réponse est $\res{[0;1]}$. Les deux égalités sont obtenues en $\res{x=0\text{ et }x=1}$. Le dessin illustre les positions relatives des deux courbes.""",
'Comparer par différence, puis exploiter la contrainte x positif.','assert solve_univariate_inequality(x*x<=x,x,relational=False)==Interval(0,1)',figure='carre-identite'),
E('Une inéquation d’inverse',r"""Résoudre dans $\mathbb R$ l’inéquation $1/x\ge2$.""",
r"""On impose $x\ne0$ puis on écrit $(1-2x)/x\ge0$. Les valeurs à examiner sont 0, interdite, et $1/2$, zéro du numérateur. Le quotient est positif sur $]0;1/2[$ et nul en $1/2$. Ainsi $\res{S=]0;1/2]}$. Les négatifs ne conviennent pas car leur inverse est négatif.""",
'Ramener le quotient à zéro et étudier les signes.','assert solve_univariate_inequality(1/x>=2,x,relational=False)==Interval.Lopen(0,Rational(1,2))'),
E('Une distance minimale',r"""On considère $f(x)=|x-3|$ sur $[0;8]$. Déterminer son minimum et son maximum et préciser où ils sont atteints.""",
r"""$f(x)$ mesure la distance de $x$ à 3. Elle est minimale en 3, avec $\res{f(3)=0}$. Les distances aux extrémités sont 3 et 5 ; le point le plus éloigné est 8, donc le maximum est $\res5$, atteint en $\res{x=8}$. Sur cet intervalle, la fonction décroît jusqu’à 3 puis croît.""",
'Lire la formule comme une distance, puis comparer les extrémités.','assert abs(0-3)==3 and abs(8-3)==5 and abs(3-3)==0'),
E('Un problème de surface',r"""Une plaque carrée a une aire comprise entre 25 et 81 cm$^2$. Donner l’intervalle possible pour son côté, puis pour son périmètre.""",
r"""Notons $c\ge0$ le côté. $25\le c^2\le81$ donne $\res{c\in[5;9]}$ cm par croissance de la racine. Le périmètre vaut $4c$, donc $\res{P\in[20;36]}$ cm. Les deux bornes sont atteignables avec des carrés d’aires 25 et 81 cm$^2$.""",
'Passer d’une aire à une longueur par la racine, pas par une division.','assert sqrt(25)==5 and sqrt(81)==9 and [4*5,4*9]==[20,36]'),
E('Une équation mixte',r"""Résoudre $\sqrt x=x$ dans $\mathbb R$. Justifier que les transformations n’introduisent pas de solution parasite.""",
r"""Le domaine impose $x\ge0$ ; les deux membres sont alors positifs ou nuls. L’égalité équivaut à $x=x^2$, soit $x(x-1)=0$. On obtient $\res{S=\{0;1\}}$. Les deux valeurs respectent le domaine et satisfont l’équation initiale. La condition de signe rendait l’élévation au carré réversible.""",
'Fixer le domaine et les signes avant de comparer les carrés.','assert solveset(sqrt(x)-x,x,domain=S.Reals)==FiniteSet(0,1)'),
E('Une affirmation sur les fonctions',r"""« Si $a<b$, alors $a^2<b^2$ et $1/a>1/b$. » Pour chaque conclusion, donner un contre-exemple et un domaine sur lequel elle est correcte.""",
r"""Pour les carrés, $-3<-2$ mais $9>4$ : la phrase est fausse sur tous les réels ; elle est vraie pour $0\le a<b$. Pour les inverses, $-1<1$ mais $-1<1$ aussi après inversion : le sens annoncé échoue lorsque l’on traverse 0. Il est correct si $a,b$ appartiennent tous deux à $]0;+\infty[$ ou tous deux à $]-\infty;0[$.""",
'Vérifier les hypothèses de monotonie au lieu de retenir une règle sans domaine.','assert -3<-2 and (-3)**2>(-2)**2 and -1<1 and Rational(1,-1)<Rational(1,1)'),
E('Un encadrement transformé',r"""On sait $2\le x\le5$. Encadrer $x^2$, $\sqrt x$ et $1/x$. Les bornes obtenues sont-elles atteignables ?""",
r"""Sur les positifs, carré et racine sont croissantes : $\res{4\le x^2\le25}$ et $\res{\sqrt2\le\sqrt x\le\sqrt5}$. L’inverse est décroissante : $\res{1/5\le1/x\le1/2}$. Chaque borne est atteinte pour $x=2$ ou $x=5$ ; ces encadrements sont donc les plus précis possibles à partir de l’information donnée.""",
'Appliquer la monotonie et vérifier l’atteinte des bornes.','assert 2**2==4 and 5**2==25 and Rational(1,5)<Rational(1,2)')
],reperes=['Fonctions affine, valeur absolue, carré, cube, inverse et racine','Domaines, signes et variations','Équations et inéquations de référence','Position de x et de son carré'])
