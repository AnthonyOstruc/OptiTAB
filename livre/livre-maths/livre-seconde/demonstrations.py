"""Démonstrations de référence : textes originaux, hypothèses explicites."""
PREUVES=[
('Multiples et parité',[
('Somme de deux multiples de 7',r"""Si $a=7m$ et $b=7n$ avec $m,n\in\mathbb Z$, alors $a+b=7(m+n)$. Comme $m+n$ est entier, la somme est un multiple de 7. Le même calcul fonctionne avec tout diviseur fixé."""),
('Carré d’un impair',r"""Pour $n=2k+1$, $n^2=4k^2+4k+1=2(2k^2+2k)+1$. Le nombre $2k^2+2k$ est entier, donc $n^2$ est impair. La contraposée donne : si $n^2$ est pair, alors $n$ est pair."""),
('Pourquoi un tiers n’est pas décimal',r"""Supposons $1/3=N/10^k$ pour un entier $N$ et un entier $k\ge0$. Alors $10^k=3N$ serait divisible par 3. Or $10^k$ a une écriture « 1 suivi de zéros », dont la somme des chiffres vaut 1 ; il n’est pas divisible par 3. La contradiction prouve que $1/3$ n’est pas décimal."""),
]),
('Racines et irrationalité',[
('Irrationalité de la racine de 2',r"""Supposons $\sqrt2=p/q$ avec $p,q$ entiers positifs et la fraction irréductible. En élevant au carré, $p^2=2q^2$, donc $p^2$ est pair. Par la propriété précédente, $p$ est pair : $p=2r$. Alors $4r^2=2q^2$, donc $q^2=2r^2$, et $q$ est pair aussi. Ainsi 2 divise $p$ et $q$, ce qui contredit l’irréductibilité. Le nombre $\sqrt2$ est irrationnel."""),
('Racine d’un produit',r"""Pour $a,b\ge0$, les nombres $\sqrt{ab}$ et $\sqrt a\sqrt b$ sont positifs ou nuls. De plus $(\sqrt a\sqrt b)^2=ab$. Par unicité de la racine carrée positive de $ab$, on obtient $\sqrt{ab}=\sqrt a\sqrt b$. La condition de positivité distingue la racine positive de son opposé."""),
]),
('Vecteurs et équations de droite',[
('Déterminant et colinéarité',r"""Si $\vec v=k\vec u$, alors pour $\vec u=(a;b)$ et $\vec v=(c;d)$, $ad-bc=a(kb)-b(ka)=0$. Réciproquement, supposons $\vec u\ne\vec0$ et $ad-bc=0$. Si $a\ne0$, poser $k=c/a$ ; l’égalité donne $d=bc/a=kb$, donc $\vec v=k\vec u$. Si $a=0$, alors $b\ne0$ et $-bc=0$ impose $c=0$ ; poser $k=d/b$ donne encore $\vec v=k\vec u$. Le cas d’un vecteur nul est colinéaire par convention."""),
('Forme cartésienne d’une droite',r"""Une droite passant par $A(x_0;y_0)$ de directeur non nul $(u;v)$ contient exactement les $M(x;y)$ tels que $u(y-y_0)-v(x-x_0)=0$. Cela s’écrit $-vx+uy+vx_0-uy_0=0$, de la forme $ax+by+c=0$ avec $(a;b)\ne(0;0)$. Réciproquement, pour une telle équation, choisir un point solution $A$ puis utiliser le directeur $(-b;a)$ ; le même calcul décrit une droite. Un point solution existe : si $b\ne0$, prendre $(0;-c/b)$ ; sinon $(-c/a;0)$."""),
]),
('Variations et comparaison',[
('Variations d’une fonction affine',r"""Pour $f(x)=mx+p$ et $a<b$, $f(b)-f(a)=m(b-a)$. Le facteur $b-a$ est positif. La différence a donc le signe de $m$ : positive pour $m>0$, négative pour $m<0$, nulle pour $m=0$. Cela prouve les trois affirmations de variation."""),
('Position du carré par rapport à l’identité',r"""Pour $x\ge0$, $x^2-x=x(x-1)$. Sur $[0;1]$, le produit est négatif ou nul ; sur $[1;+\infty[$, il est positif ou nul. Les deux courbes sont donc dans l’ordre $x^2\le x$ entre 0 et 1, puis dans l’ordre inverse après 1. Les égalités sont obtenues en 0 et 1."""),
]),
('Variations des fonctions de référence',[
('La fonction carré',r"""Pour $0\le a<b$, $b^2-a^2=(b-a)(b+a)>0$ : le carré est strictement croissant sur $[0;+\infty[$. Pour $a<b\le0$, le premier facteur est positif et $a+b<0$, donc $b^2-a^2<0$ : le carré est strictement décroissant sur $]-\infty;0]$. Il faut traiter séparément les deux intervalles."""),
('La fonction inverse',r"""Pour $a<b$ tous deux strictement positifs, ou tous deux strictement négatifs, $ab>0$. On a $1/b-1/a=(a-b)/(ab)<0$. La fonction inverse est donc strictement décroissante sur chacun des deux intervalles de son domaine. L’argument ne vaut pas pour un couple qui traverse 0, car le signe de $ab$ change."""),
]),
('Coordonnées et statistiques',[
('Coordonnées du milieu',r"""Pour un milieu $I$, $\vect{AI}=\vect{IB}$. Les abscisses donnent $x_I-x_A=x_B-x_I$, soit $2x_I=x_A+x_B$. De même, $2y_I=y_A+y_B$. Réciproquement, ces coordonnées donnent l’égalité des deux vecteurs et caractérisent donc le milieu. La formule est ainsi démontrée dans les deux sens."""),
('Deux écritures de la dispersion',r"""En développant et en prenant la moyenne des carrés des écarts, on obtient $\overline{(x-\bar x)^2}=\overline{x^2}-2\bar x\,\overline{x}+\bar x^2$. Comme $\overline{x}=\bar x$, cela donne $\overline{x^2}-\bar x^2$. Les pondérations éventuelles restent les mêmes dans toutes les moyennes. Cette identité justifie la formule utilisée dans les programmes."""),
])
]
