from commun import e,c
NOM='expertes'
CHAPTERS=[]
DIAGNOSTIC=r'''
\begin{questions}
\item Développer $(x+2)^3$ et factoriser $x^3-1$.
\item Donner $\cos(\pi/3)$, $\sin(\pi/3)$ et $\cos(\pi/2)$.
\item Résoudre $2x+3y=7$, $x-y=1$.
\item Écrire la division euclidienne de $47$ par $6$ ; donner le PGCD de $18$ et $30$.
\item Une probabilité de transition de $A$ vers $B$ vaut $0{,}3$. Quel est le poids de $A$ vers $A$ s'il n'y a que deux états ?
\item Pour $u_0=1$, $u_{n+1}=2u_n+1$, donner les quatre premiers termes.
\end{questions}
\begin{savoirfaire}[Réponses et orientation]
1. $x^3+6x^2+12x+8$ ; $(x-1)(x^2+x+1)$.
2. $1/2$, $\sqrt3/2$, $0$.
3. $x=2,y=1$.
4. $47=6\times7+5$, PGCD $6$.
5. $0{,}7$ : les transitions sortant de $A$ totalisent $1$.
6. $1,3,7,15$.
Les chapitres 1 à 5 prolongent l'algèbre et la trigonométrie ; les chapitres 6 à 8 structurent l'arithmétique ; les chapitres 9 à 12 développent matrices, graphes et chaînes de Markov.
\end{savoirfaire}
Les mathématiques expertes s'articulent avec la spécialité de Terminale. Les rappels sont fournis lorsqu'ils servent les nouveaux objets, mais le manuel de spécialité reste utile pour les suites, l'analyse et les probabilités.
'''

CHAPTERS.append(c('Calculer dans les complexes','Nombres complexes',r'Forme algébrique · Conjugaison · Binôme',
'Calculer avec $\mathrm i^2=-1$.@@Utiliser la conjugaison et l’inverse.@@Résoudre des équations avec $z$ et son conjugué.@@Appliquer et démontrer la formule du binôme.',
'Calcul littéral, coefficients binomiaux et systèmes de deux équations.',r'''
\essSection{1}{Un nombre à deux coordonnées}
\begin{definition}
Tout nombre complexe s'écrit de manière unique $z=x+\mathrm iy$, avec $x,y\in\R$ et $\mathrm i^2=-1$.
$x=\Re(z)$ est la partie réelle et $y=\Im(z)$ la partie imaginaire : toutes deux sont des nombres réels.
Deux complexes sont égaux si leurs parties réelles et imaginaires sont égales.
\end{definition}
Les réels s'identifient aux complexes de partie imaginaire nulle. Les imaginaires purs ont une partie réelle nulle, y compris zéro.
L'addition et le produit suivent les règles usuelles de distributivité avec $\mathrm i^2=-1$.
\begin{exemple}
$(2+3\mathrm i)(1-2\mathrm i)=2-4\mathrm i+3\mathrm i-6\mathrm i^2=8-\mathrm i$.
Les puissances de $\mathrm i$ se répètent par période $4$ : $1,\mathrm i,-1,-\mathrm i$.
\end{exemple}
\essSection{2}{La conjugaison}
\begin{definition}
Le conjugué de $z=x+\mathrm iy$ est $\bar z=x-\mathrm iy$.
On a $\overline{\bar z}=z$, $z+\bar z=2\Re(z)$ et $z-\bar z=2\mathrm i\Im(z)$.
\end{definition}
\begin{propriete}
$\overline{z+w}=\bar z+\bar w$, $\overline{zw}=\bar z\bar w$ et $\overline{z^n}=\bar z^{\,n}$ pour $n\in\N$.
Un complexe est réel si et seulement si $z=\bar z$ ; il est imaginaire pur si et seulement si $z=-\bar z$.
\end{propriete}
\begin{demonstration}
Pour $z=x+\mathrm iy$, $w=u+\mathrm iv$, le produit vaut $(xu-yv)+\mathrm i(xv+yu)$. Son conjugué est précisément $(x-\mathrm iy)(u-\mathrm iv)$. La règle des puissances suit par récurrence sur $n$, à partir de $n=0$.
\end{demonstration}
\figurelivre{e01-conjugaison.pdf}{Dans le plan complexe, $z=2+3\mathrm i$ et $\bar z=2-3\mathrm i$ sont symétriques par rapport à l'axe réel. L'ordonnée représente $\Im(z)$, pas $\mathrm i\Im(z)$.}
\essSection{3}{Diviser et résoudre une équation}
Pour $z=x+\mathrm iy\ne0$, $z\bar z=x^2+y^2>0$, donc
$1/z=\bar z/(x^2+y^2)$.
Pour mettre un quotient sous forme algébrique, multiplier le numérateur et le dénominateur par le conjugué du dénominateur.
\begin{exemple}
$\dfrac{1+\mathrm i}{2-\mathrm i}=\dfrac{(1+\mathrm i)(2+\mathrm i)}5=\dfrac15+\dfrac35\mathrm i$.
Pour résoudre $z+2\bar z=3+4\mathrm i$, poser $z=x+\mathrm iy$ : $3x-\mathrm iy=3+4\mathrm i$, donc $x=1,y=-4$.
\end{exemple}
L'équation $az=b$ a une unique solution $b/a$ si $a\ne0$. Si $a=0$, elle a toutes les solutions lorsque $b=0$, et aucune sinon.
Conjuguer $z(1/z)=1$ donne $\bar z\,\overline{1/z}=1$, donc $\overline{1/z}=1/\bar z$.
\essSection{4}{Le binôme reste valable}
\begin{theoreme}
Pour $a,b\in\C$ et $n\in\N$,
$\displaystyle(a+b)^n=\sum_{k=0}^n\binom nk a^{n-k}b^k$.
\end{theoreme}
\begin{demonstration}
L'identité vaut pour $n=0$. Supposer l'identité au rang $n$, multiplier par $a+b$ et regrouper les coefficients d'une même puissance de $b$. L'identité de Pascal $\binom nk+\binom n{k-1}=\binom{n+1}k$ donne la formule au rang $n+1$. Les facteurs complexes commutent, donc le regroupement est valide.
\end{demonstration}
\begin{attention}
Il n'existe pas d'ordre sur $\C$ permettant de comparer tous les complexes comme des réels tout en conservant les règles usuelles des inégalités. On ne résout pas « $z>0$ » pour un complexe arbitraire. Les conditions de réalité se traduisent en revanche par des équations sur $x,y$.
\end{attention}
''',[
e('Parties réelle et imaginaire',1,'',r'Donner les parties réelle et imaginaire de $3-5\mathrm i$.@@Calculer $(2+\mathrm i)+(4-3\mathrm i)$.@@Résoudre $x+2\mathrm iy=3-4\mathrm i$ avec $x,y$ réels.',r'$\Re=3$, $\Im=-5$.@@$6-2\mathrm i$.@@L’unicité de la forme algébrique donne $x=3$ et $2y=-4$, donc $y=-2$.'),
e('Produits',1,'',r'Calculer $(1+\mathrm i)^2$.@@Calculer $(2+3\mathrm i)(1-2\mathrm i)$.@@Calculer $\mathrm i^{2026}$.',r'$1+2\mathrm i+\mathrm i^2=2\mathrm i$.@@$8-\mathrm i$.@@$2026=4\times506+2$, donc $\mathrm i^{2026}=\mathrm i^2=-1$.'),
e('Conjuguer',1,'',r'Conjuguer $-2+7\mathrm i$.@@Calculer $z+\bar z$ pour $z=4-3\mathrm i$.@@Calculer $z\bar z$ pour ce même $z$.',r'$-2-7\mathrm i$.@@$8$.@@$(4-3\mathrm i)(4+3\mathrm i)=16+9=25$.'),
e('Inverses',1,'',r'Mettre $1/(1+\mathrm i)$ sous forme algébrique.@@Faire de même pour $1/(3-4\mathrm i)$.@@Vérifier l’un des résultats par multiplication.',r'$(1-\mathrm i)/2$.@@$(3+4\mathrm i)/25$.@@$(1+\mathrm i)(1-\mathrm i)/2=(1-\mathrm i^2)/2=1$.'),
e('Équation linéaire',2,'',r'Résoudre $(1+\mathrm i)z=2$.@@Résoudre $2z-3=\mathrm i$.@@Discuter $0z=b$ suivant $b$.',r'$z=2/(1+\mathrm i)=1-\mathrm i$.@@$z=(3+\mathrm i)/2$.@@Si $b=0$, tout complexe convient ; si $b\ne0$, aucune solution.'),
e('Un quotient',2,'',r'Calculer $(3+\mathrm i)/(1-\mathrm i)$.@@Vérifier en remultipliant par $1-\mathrm i$.@@En déduire le conjugué du quotient.',r'$(3+\mathrm i)(1+\mathrm i)/2=1+2\mathrm i$.@@$(1+2\mathrm i)(1-\mathrm i)=3+\mathrm i$.@@$1-2\mathrm i$ ; il vaut également $(3-\mathrm i)/(1+\mathrm i)$.'),
e('Avec le conjugué',2,'',r'Résoudre $z+2\bar z=3+4\mathrm i$.@@Résoudre $z-\bar z=6\mathrm i$.@@Pourquoi la seconde équation a-t-elle une infinité de solutions ?',r'Poser $z=x+\mathrm iy$ : $3x-\mathrm iy=3+4\mathrm i$, donc $z=1-4\mathrm i$.@@$2\mathrm iy=6\mathrm i$ donne $y=3$, donc $z=x+3\mathrm i$ avec $x\in\R$.@@Elle fixe seulement la partie imaginaire et laisse la partie réelle libre.'),
e('Binôme',2,'',r'Développer $(1+\mathrm i)^3$ par le binôme.@@Calculer $(1+\mathrm i)^4$.@@En déduire $(1+\mathrm i)^8$.',r'$1+3\mathrm i+3\mathrm i^2+\mathrm i^3=-2+2\mathrm i$.@@Le carré de $2\mathrm i$ vaut $-4$.@@$(-4)^2=16$.'),
e('Réalité d’un quotient',3,r'$z=(x+\mathrm i)/(1+\mathrm i)$ avec $x\in\R$.',r'Mettre $z$ sous forme algébrique.@@Pour quelle valeur de $x$ est-il réel ?@@Pour quelle valeur est-il imaginaire pur ?',r'$z=[x+1+\mathrm i(1-x)]/2$.@@$1-x=0$, donc $x=1$, donnant $z=1$.@@$x+1=0$, donc $x=-1$, donnant $z=\mathrm i$.'),
e('Conjugaison et puissance',3,'',r'Prouver $\overline{z^2}=\bar z^2$.@@Étendre la propriété par récurrence à tout entier naturel.@@L’étendre aux puissances entières négatives lorsque $z\ne0$.',r'Appliquer la conjugaison du produit à $z\times z$.@@Au rang zéro, les deux membres valent $1$. Si l’identité vaut pour $n$, conjuguer $z^{n+1}=z^nz$ donne $\bar z^n\bar z=\bar z^{n+1}$.@@Utiliser $z^{-m}=1/z^m$ et la conjugaison de l’inverse : $\overline{z^{-m}}=1/\bar z^m$.'),
e('Une équation à analyser',3,r'$z\bar z=2z$.',r'Poser $z=x+\mathrm iy$ et comparer les parties.@@Résoudre.@@Vérifier les solutions dans l’équation initiale.',r'$x^2+y^2=2x+2\mathrm iy$ donne $y=0$ et $x^2=2x$.@@$x(x-2)=0$, donc $z\in\{0,2\}$.@@Pour $0$, les deux membres sont nuls ; pour $2$, ils valent $4$.'),
e('Une somme binomiale',3,'',r'Exprimer $(1+\mathrm i)^6$ avec les coefficients binomiaux.@@Calculer sa forme algébrique par une méthode plus courte.@@En déduire la somme des termes réels du développement.',r'$\sum_{k=0}^6\binom6k\mathrm i^k$.@@$(1+\mathrm i)^2=2\mathrm i$, donc la puissance six vaut $(2\mathrm i)^3=-8\mathrm i$.@@La partie réelle est nulle : $1-\binom62+\binom64-\binom66=1-15+15-1=0$.')
], 'courbe'))

CHAPTERS.append(c('Module, arguments et plan complexe','Nombres complexes',r'Affixes · Distances · Cercle unité · Forme trigonométrique',
'Passer d’un point à son affixe et inversement.@@Calculer modules et arguments.@@Utiliser les propriétés multiplicatives du module.@@Reconnaître des ensembles de points simples.',
'Coordonnées, distance euclidienne et cercle trigonométrique.',r'''
\essSection{1}{L'affixe encode un point ou un vecteur}
Dans un repère orthonormé direct, le point $M(x,y)$ a pour affixe $z=x+\mathrm iy$.
Si $A,B$ ont pour affixes $a,b$, le vecteur $\vect{AB}$ a pour affixe $b-a$ et le milieu de $[AB]$ a pour affixe $(a+b)/2$.
Le conjugué correspond à la symétrie par rapport à l'axe réel ; l'opposé à la symétrie de centre $O$.
\begin{definition}[Module]
$|z|=\sqrt{x^2+y^2}$ est la distance $OM$.
En particulier $AB=|b-a|$ et $|z|=0$ si et seulement si $z=0$.
\end{definition}
\figurelivre{e02-module.pdf}{Pour $z=3+2\mathrm i$, le module est la longueur $OM=\sqrt{13}$. Un argument est l'angle orienté du demi-axe réel positif vers $\vect{OM}$.}
\essSection{2}{Les identités du module}
\begin{propriete}
$|z|^2=z\bar z$, $|zw|=|z||w|$, $|z^n|=|z|^n$.
Pour $z\ne0$, $|1/z|=1/|z|$ ; pour $w\ne0$, $|z/w|=|z|/|w|$.
\end{propriete}
\begin{demonstration}
$z\bar z=(x+\mathrm iy)(x-\mathrm iy)=x^2+y^2=|z|^2$.
Donc $|zw|^2=zw\bar z\bar w=(z\bar z)(w\bar w)=|z|^2|w|^2$. Les modules étant positifs ou nuls, prendre la racine donne la règle du produit.
Une récurrence donne la puissance ; le produit $z(1/z)=1$ donne la règle de l'inverse.
\end{demonstration}
\essSection{3}{L'argument est défini modulo $2\pi$}
\begin{definition}
Si $z\ne0$, un argument $\theta$ vérifie $z=|z|(\cos\theta+\mathrm i\sin\theta)$.
Tous les arguments sont $\theta+2k\pi$, $k\in\Z$.
Le nombre $0$ n'a pas d'argument.
\end{definition}
Pour identifier un angle, utiliser simultanément $\cos\theta=x/|z|$ et $\sin\theta=y/|z|$. La tangente seule perd l'information sur le quadrant.
\begin{exemple}
$z=-1+\mathrm i\sqrt3$ a pour module $2$, avec cosinus $-1/2$ et sinus $\sqrt3/2$ : un argument est $2\pi/3$.
Ainsi $z=2(\cos(2\pi/3)+\mathrm i\sin(2\pi/3))$.
\end{exemple}
\essSection{4}{Le cercle unité et les lieux}
L'ensemble $\mathbb U=\{z\in\C:|z|=1\}$ est stable par produit et par inverse, car les modules restent $1$.
Sur $\mathbb U$, $1/z=\bar z$.
$|z-a|=R$ décrit un cercle de centre d'affixe $a$ et de rayon $R>0$ ; $|z-a|\leq R$ décrit le disque fermé.
L'égalité $|z-a|=|z-b|$, pour $a\ne b$, décrit la médiatrice de $[AB]$.
\figurelivre{e02-lieux.pdf}{À gauche : $|z-(1+\mathrm i)|=2$. À droite : $|z+1|=|z-1|$, médiatrice de $[-1,1]$ sur l'axe réel.}
\essSection{5}{Une inégalité géométrique, en approfondissement}
L'inégalité triangulaire $|z+w|\leq|z|+|w|$ traduit que la distance directe ne dépasse pas la longueur d'un trajet brisé.
Algébriquement, $|z+w|^2=|z|^2+|w|^2+2\Re(z\bar w)$ et $\Re(z\bar w)\leq|z\bar w|=|z||w|$.
L'égalité correspond à des vecteurs de même direction et de même sens, avec les cas où l'un est nul.
''',[
e('Affixes',1,'',r'Donner l’affixe de $M(-2,3)$.@@Donner les coordonnées du point d’affixe $4-\mathrm i$.@@Si $a=1+\mathrm i$, $b=3+4\mathrm i$, donner l’affixe de $\vect{AB}$.',r'$-2+3\mathrm i$.@@$(4,-1)$.@@$b-a=2+3\mathrm i$.'),
e('Modules',1,'',r'Calculer $|3-4\mathrm i|$.@@Calculer $|2\mathrm i|$ et $|-5|$.@@Calculer $|(1+\mathrm i)^5|$.',r'$\sqrt{9+16}=5$.@@$2$ et $5$.@@$|1+\mathrm i|^5=(\sqrt2)^5=4\sqrt2$.'),
e('Arguments remarquables',1,'',r'Donner les arguments de $1$, puis de $\mathrm i$.@@Donner ceux de $-1$.@@Pourquoi zéro n’en a-t-il pas ?',r'$2k\pi$ pour $1$ ; $\pi/2+2k\pi$ pour $\mathrm i$, avec $k\in\Z$.@@$\pi+2k\pi$, $k\in\Z$.@@Le vecteur nul ne définit pas de direction ; la forme trigonométrique ne sélectionne aucun angle.'),
e('Forme trigonométrique',1,'',r'Mettre $1+\mathrm i$ sous forme trigonométrique.@@Faire de même pour $-\sqrt3+\mathrm i$.@@Revenir à la forme algébrique de $2(\cos(\pi/6)+\mathrm i\sin(\pi/6))$.',r'$\sqrt2(\cos(\pi/4)+\mathrm i\sin(\pi/4))$.@@$2(\cos(5\pi/6)+\mathrm i\sin(5\pi/6))$.@@$\sqrt3+\mathrm i$.'),
e('Distances et milieu',2,r'$a=1+2\mathrm i$ et $b=5-\mathrm i$.',r'Calculer $AB$.@@Donner l’affixe du milieu.@@Donner l’affixe du symétrique de $A$ par rapport à ce milieu.',r'$|4-3\mathrm i|=5$.@@$(a+b)/2=3+\mathrm i/2$.@@$2m-a=b=5-\mathrm i$, comme attendu.'),
e('Le cercle unité',2,r'$z=(3+4\mathrm i)/5$.',r'Vérifier $z\in\mathbb U$.@@Calculer $1/z$.@@Justifier que $z^{10}\in\mathbb U$ sans développer.',r'$|z|=5/5=1$.@@$1/z=\bar z=(3-4\mathrm i)/5$.@@$|z^{10}|=|z|^{10}=1$.'),
e('Décrire des lieux',2,'',r'Décrire $|z-2+\mathrm i|=3$.@@Décrire $|z|\leq2$.@@Décrire $|z-1|=|z+1|$.',r'Cercle de centre d’affixe $2-\mathrm i$ et de rayon $3$.@@Disque fermé de centre $O$ et de rayon $2$.@@Médiatrice des points d’affixes $1$ et $-1$, donc axe imaginaire.'),
e('Un argument mal choisi',2,r'Un élève dit que $-1-\mathrm i$ a pour argument $\pi/4$ car le quotient des coordonnées vaut $1$.',r'Calculer le module.@@Donner un argument correct.@@Expliquer l’erreur.',r'$\sqrt2$.@@$-3\pi/4$, ou $5\pi/4$ modulo $2\pi$.@@La tangente seule ne distingue pas deux angles séparés de $\pi$. Les signes du cosinus et du sinus doivent être tous deux négatifs.'),
e('Démontrer le produit',3,'',r'Écrire $|zw|^2$ à l’aide des conjugués.@@Regrouper les facteurs.@@Pourquoi peut-on prendre la racine sans ambiguïté de signe ?',r'$|zw|^2=zw\overline{zw}=zw\bar z\bar w$.@@Par commutativité, $(z\bar z)(w\bar w)=|z|^2|w|^2$.@@Les deux modules sont positifs ou nuls, donc l’unique racine positive est $|z||w|$.'),
e('Médiatrice par le calcul',3,r'$a=-1$, $b=3$ et $z=x+\mathrm iy$.',r'Écrire l’égalité $|z-a|=|z-b|$ avec $x,y$.@@La simplifier.@@Relier la réponse à la géométrie.',r'$\sqrt{(x+1)^2+y^2}=\sqrt{(x-3)^2+y^2}$.@@Élever au carré donne $x^2+2x+1=x^2-6x+9$, donc $x=1$.@@La droite verticale $x=1$ passe par le milieu du segment réel $[-1,3]$ et lui est perpendiculaire.'),
e('Triangle et égalité',3,r'$z=1+\mathrm i$ et $w=2+2\mathrm i$.',r'Comparer $|z+w|$ et $|z|+|w|$.@@Expliquer géométriquement l’égalité.@@Que se passe-t-il si l’on remplace $w$ par $-z$ ?',r'$|3+3\mathrm i|=3\sqrt2$ et $\sqrt2+2\sqrt2=3\sqrt2$.@@$w=2z$ : les vecteurs ont même direction et même sens.@@$|z+w|=0$ mais $|z|+|w|=2\sqrt2$ ; l’inégalité est alors stricte.'),
e('Module constant ?',3,r'$z=(x-\mathrm i)/(x+\mathrm i)$ avec $x\in\R$.',r'Vérifier que le dénominateur est non nul.@@Prouver $|z|=1$.@@Le point d’affixe $1$ peut-il être obtenu pour un réel $x$ ?',r'Sa partie imaginaire est $1$, donc il ne peut être nul.@@Le numérateur et le dénominateur sont conjugués et ont même module $\sqrt{x^2+1}$.@@Non : $x-\mathrm i=x+\mathrm i$ imposerait $-\mathrm i=\mathrm i$, impossible. Le lieu est contenu dans le cercle unité privé de ce point.')
], 'trigo'))

CHAPTERS.append(c('Divisibilité et congruences','Arithmétique',r'Entiers relatifs · Division euclidienne · Restes',
'Manipuler la divisibilité dans $\Z$.@@Effectuer une division euclidienne, y compris d’un entier négatif.@@Calculer avec les congruences.@@Établir des critères de divisibilité.',
'Calcul entier, multiples et puissances.',r'''
\essSection{1}{Diviser dans les entiers}
\begin{definition}
Pour $a,b\in\Z$, $a\mid b$ signifie qu'il existe $k\in\Z$ tel que $b=ak$.
Si $a$ divise $b$ et $c$, il divise toute combinaison $ub+vc$ avec $u,v\in\Z$.
\end{definition}
Si $b=ak$ et $c=a\ell$, alors $ub+vc=a(uk+v\ell)$, ce qui prouve la propriété.
Un diviseur non nul de $n\ne0$ a une valeur absolue au plus $|n|$. Pour trouver les diviseurs positifs d'un entier positif, on peut tester jusqu'à sa racine carrée et associer $d$ à $n/d$.
\essSection{2}{La division euclidienne}
\begin{theoreme}
Pour $a\in\Z$ et $b\in\N^*$, il existe un unique couple $(q,r)\in\Z^2$ tel que
$a=bq+r$, avec $0\leq r<b$.
\end{theoreme}
\begin{exemple}
$47=6\times7+5$. Pour $-47$, l'écriture euclidienne est $-47=6\times(-8)+1$, et non $6\times(-7)-5$, car le reste doit être positif ou nul.
En Python, pour un diviseur positif, \code{a//b} et le reste de \code{a} modulo \code{b} donnent quotient et reste.
\end{exemple}
L'unicité vient de $b(q-q')=r'-r$ : le second membre est de valeur absolue strictement inférieure à $b$, et le seul multiple de $b$ dans cette situation est zéro.
\figurelivre{e06-division.pdf}{La droite des entiers repère les multiples de $6$. Le nombre $-47$ se place une unité après $-48=6\times(-8)$, ce qui explique le quotient négatif et le reste positif.}
\essSection{3}{Raisonner modulo un entier}
\begin{definition}
Pour $n\geq1$, $a\equiv b\pmod n$ signifie $n\mid(a-b)$. Cela équivaut à dire que $a$ et $b$ ont le même reste dans la division par $n$.
\end{definition}
Les congruences sont compatibles avec l'addition, la soustraction, le produit et les puissances entières naturelles.
Si $a\equiv b\pmod n$ et $c\equiv d\pmod n$, alors $ac-bd=c(a-b)+b(c-d)$ est divisible par $n$.
\begin{attention}
On ne divise pas librement une congruence : $2\times1\equiv2\times4\pmod6$, mais $1\not\equiv4\pmod6$.
La simplification exige des hypothèses, précisées avec le théorème de Gauss au chapitre suivant.
\end{attention}
\figurelivre{e06-modulo.pdf}{Les classes modulo $7$ se lisent sur un cycle : ajouter $1$ au reste $6$ ramène au reste $0$. Le calcul concerne les restes, pas une égalité ordinaire entre entiers.}
\essSection{4}{Calculer de grandes puissances}
On réduit la base puis on cherche un cycle ou on utilise des carrés successifs. Par exemple $3^2\equiv2\pmod7$, $3^4\equiv4\pmod7$ et $3^6\equiv1\pmod7$.
Donc $3^{100}= (3^6)^{16}3^4\equiv4\pmod7$.
La fonction Python \code{pow(a, n, m)} calcule efficacement le reste de $a^n$ modulo $m$ pour $n\geq0,m>0$.
\essSection{5}{Construire un test de divisibilité}
Si $N=\sum a_k10^k$, alors $10\equiv1\pmod9$ donne $N\equiv\sum a_k\pmod9$ : somme des chiffres.
Comme $10\equiv-1\pmod{11}$, $N\equiv\sum(-1)^ka_k\pmod{11}$ : somme alternée, en partant des unités.
Ces résultats sont des preuves de critères, pas seulement des recettes expérimentales.
''',[
e('Diviseurs',1,'',r'Donner les diviseurs positifs de $18$.@@$-3$ divise-t-il $18$ ?@@Zéro divise-t-il un entier non nul ?',r'$1,2,3,6,9,18$.@@Oui : $18=(-3)(-6)$.@@Non : $0k=0$ pour tout entier $k$. En revanche tout entier divise zéro.'),
e('Division euclidienne',1,'',r'Diviser $83$ par $7$.@@Diviser $-83$ par $7$.@@Vérifier la contrainte sur les restes.',r'$83=7\times11+6$.@@$-83=7\times(-12)+1$.@@Les restes $6$ et $1$ sont dans $\{0,\ldots,6\}$.'),
e('Lire une congruence',1,'',r'Verifier $29\equiv1\pmod7$.@@Donner le reste de $-3$ modulo $7$.@@Donner tous les entiers congrus à $2$ modulo $5$.',r'$29-1=28$ est divisible par $7$.@@$4$, car $-3=7(-1)+4$.@@$2+5k$, avec $k\in\Z$.'),
e('Calcul de restes',1,'',r'Calculer le reste de $24+35$ modulo $6$.@@Calculer celui de $24\times35$.@@Calculer celui de $5^2$ modulo $6$.',r'$24\equiv0$, $35\equiv5$, donc reste $5$.@@$0\times5\equiv0$.@@$25\equiv1\pmod6$.'),
e('Combinaison entière',2,r'$d$ divise $3n+2$ et $5n+3$.',r'Montrer que $d$ divise $5(3n+2)-3(5n+3)$.@@En déduire les valeurs possibles de $d>0$.@@Que peut-on dire de ces deux entiers ?',r'Un diviseur commun divise toute combinaison entière.@@La combinaison vaut $1$, donc $d=1$.@@Ils sont premiers entre eux, quel que soit l’entier $n$.'),
e('Puissance modulo $7$',2,'',r'Calculer les restes de $3^2,3^4,3^6$ modulo $7$.@@En déduire celui de $3^{100}$.@@Vérifier avec \code{pow(3, 100, 7)}.',r'$2,4,1$.@@$100=6\times16+4$, donc reste $4$.@@La fonction rend $4$ ; le calcul modulaire explique le résultat.'),
e('Critère modulo $9$',2,'',r'Prouver le critère de la somme des chiffres.@@Tester $7\,326$.@@Le critère distingue-t-il le reste $0$ du chiffre zéro ?',r'$10^k\equiv1\pmod9$, donc le nombre et la somme de ses chiffres ont même reste modulo $9$.@@$7+3+2+6=18$, donc le nombre est divisible par $9$.@@Il établit une congruence, pas une égalité au chiffre zéro. Un nombre non nul peut avoir reste zéro.'),
e('Critère modulo $11$',2,'',r'Utiliser $10\equiv-1\pmod{11}$ pour énoncer un test.@@Tester $1\,331$.@@Tester $1\,234$.',r'La somme alternée des chiffres, depuis les unités, doit être divisible par $11$.@@$1-3+3-1=0$ : divisible par $11$.@@$4-3+2-1=2$ : non divisible par $11$.'),
e('Ne pas diviser sans condition',3,'',r'Vérifier $2\equiv8\pmod6$.@@Pourquoi ne peut-on diviser par $2$ en conservant le module $6$ ?@@Quelle congruence correcte obtient-on modulo $3$ ?',r'$8-2=6$.@@Cela donnerait $1\equiv4\pmod6$, faux puisque $6$ ne divise pas $3$.@@$6\mid2(1-4)$ implique $3\mid1-4$, donc $1\equiv4\pmod3$.'),
e('Reste d’un polynôme',3,r'$N=n^3-n$.',r'Étudier $N$ modulo $2$.@@Étudier $N$ modulo $3$.@@En déduire une divisibilité par $6$.',r'$n^3-n=n(n-1)(n+1)$ contient deux entiers consécutifs, donc un facteur pair.@@Parmi trois entiers consécutifs, l’un est multiple de $3$.@@Le produit est divisible par $2$ et $3$, qui sont premiers entre eux ; donc par $6$ (ou repérer directement les facteurs $2$ et $3$ dans le produit).'),
e('Un cycle décimal',3,'',r'Montrer que $7^4\equiv1\pmod{10}$.@@Donner le dernier chiffre de $7^{2026}$.@@Expliquer le rôle de la division de $2026$ par $4$.',r'$7^2\equiv9$, donc $7^4\equiv81\equiv1$.@@$2026\equiv2\pmod4$, donc $7^{2026}\equiv7^2\equiv9\pmod{10}$.@@Elle réduit l’exposant grâce au cycle de longueur $4$, et non parce qu’on pourrait réduire arbitrairement un exposant modulo $10$.'),
e('Deux nombres consécutifs',3,'',r'Montrer que tout diviseur commun de $n$ et $n+1$ divise $1$.@@En déduire leur PGCD.@@Cette méthode permet-elle de traiter $n$ et $n+2$ ?',r'Le diviseur commun divise leur différence $(n+1)-n=1$.@@Le PGCD positif est $1$.@@Il divise alors $2$, donc il peut valoir $1$ ou $2$ ; la parité de $n$ les distingue.')
], 'denombrement'))

CHAPTERS.append(c('PGCD, Bézout et Gauss','Arithmétique',r'Euclide · Inverse modulaire · Équations entières',
'Calculer un PGCD et un couple de Bézout.@@Démontrer et utiliser Gauss.@@Résoudre une congruence linéaire.@@Résoudre une équation diophantienne simple.',
'Division euclidienne et congruences.',r'''
\essSection{1}{Le PGCD et Euclide}
Le PGCD de deux entiers non tous deux nuls est leur plus grand diviseur commun positif. On utilise leurs valeurs absolues ; $\operatorname{PGCD}(a,0)=|a|$.
Si $a=bq+r$, les diviseurs communs de $a,b$ sont exactement ceux de $b,r$.
En répétant les divisions, les restes positifs décroissent strictement : l'algorithme s'arrête ; le dernier reste non nul est le PGCD.
\figurelivre{e07-euclide.pdf}{Euclide pour $252$ et $198$ : $252=198+54$, $198=3\times54+36$, $54=36+18$, $36=2\times18$. Le PGCD est $18$.}
En remontant les égalités, $18=54-36=54-(198-3\times54)=4\times252-5\times198$.
\essSection{2}{L'identité de Bézout}
\begin{theoreme}
Pour des entiers $a,b$ non tous deux nuls, il existe $u,v\in\Z$ tels que $au+bv=d$, où $d=\operatorname{PGCD}(a,b)$.
En particulier $a,b$ sont premiers entre eux si et seulement si $au+bv=1$ possède une solution entière.
\end{theoreme}
\begin{demonstration}[Construction et réciproque]
Dans Euclide, chaque reste est une combinaison entière des deux restes précédents, donc, par substitutions successives, une combinaison de $a,b$. Le dernier reste non nul fournit $d=au+bv$.
Si une combinaison vaut $1$, tout diviseur commun de $a,b$ divise $1$ : le PGCD est $1$. La réciproque découle de la construction.
\end{demonstration}
\begin{python}
def bezout(a, b):
    r0, r1 = a, b
    u0, u1, v0, v1 = 1, 0, 0, 1
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q*r1
        u0, u1 = u1, u0 - q*u1
        v0, v1 = v1, v0 - q*v1
    return r0, u0, v0
\end{python}
On utilise ici $a,b$ positifs, ou $a>0,b=0$. L'invariant $r_j=au_j+bv_j$ explique la sortie.
\essSection{3}{Le théorème de Gauss}
\begin{theoreme}
Si $a\mid bc$ et $\operatorname{PGCD}(a,b)=1$, alors $a\mid c$.
\end{theoreme}
\begin{demonstration}
Bézout donne $au+bv=1$. Multiplier par $c$ donne $auc+bvc=c$.
Le premier terme est divisible par $a$ ; le second aussi puisque $a\mid bc$. Donc $a\mid c$.
\end{demonstration}
Une conséquence : si $a,b$ sont premiers entre eux et divisent tous deux $n$, alors $ab\mid n$.
\essSection{4}{Inverse modulaire et congruence}
Si $\operatorname{PGCD}(a,n)=1$, Bézout donne $au+nv=1$, donc $au\equiv1\pmod n$ : $u$ est un inverse de $a$ modulo $n$.
Alors $ax\equiv b\pmod n$ équivaut à $x\equiv ub\pmod n$.
Si $d=\operatorname{PGCD}(a,n)$ ne divise pas $b$, aucune solution n'existe.
Si $d\mid b$, diviser $a,n,b$ par $d$ ramène à un coefficient inversible modulo $n/d$.
\begin{exemple}
$3x\equiv4\pmod7$. Comme $3\times5\equiv1$, $x\equiv20\equiv6\pmod7$.
En revanche $6x\equiv5\pmod9$ est impossible, car $3\nmid5$.
\end{exemple}
\essSection{5}{Équations diophantiennes}
Pour $ax+by=c$, une condition nécessaire et suffisante est $d=\operatorname{PGCD}(a,b)\mid c$.
Après division par $d$, si $(x_0,y_0)$ est une solution et si $a'=a/d,b'=b/d$, toutes les solutions sont
$x=x_0+b'k$, $y=y_0-a'k$, avec $k\in\Z$.
En soustrayant une solution particulière, on obtient $a'(x-x_0)=-b'(y-y_0)$. Gauss impose $b'\mid x-x_0$, ce qui justifie la paramétrisation.
Pour une situation concrète, imposer ensuite les contraintes de positivité ou les bornes ; elles ne sont pas automatiques.
''',[
e('Calculer un PGCD',1,'',r'Calculer $\operatorname{PGCD}(48,18)$ par Euclide.@@Calculer $\operatorname{PGCD}(35,12)$.@@Donner $\operatorname{PGCD}(-18,30)$.',r'$48=2\times18+12$, $18=12+6$, $12=2\times6$ : PGCD $6$.@@$35=2\times12+11$, $12=11+1$ : PGCD $1$.@@On prend les valeurs absolues : PGCD $6$.'),
e('Vérifier Bézout',1,'',r'Verifier $4\times252-5\times198=18$.@@Pourquoi cette identité seule ne suffit-elle pas encore à affirmer que le PGCD est $18$ ?@@Compléter la preuve.',r'$1008-990=18$.@@Elle prouve que le PGCD divise $18$, mais il faut aussi vérifier que $18$ divise les deux nombres.@@$252=14\times18$ et $198=11\times18$ ; $18$ est un diviseur commun et tout diviseur commun divise $18$, donc c’est le PGCD.'),
e('Un inverse',1,'',r'Verifier $3\times5\equiv1\pmod7$.@@Résoudre $3x\equiv4\pmod7$.@@Donner la solution dans $\{0,\ldots,6\}$.',r'$15=2\times7+1$.@@Multiplier par $5$ : $x\equiv20\equiv6\pmod7$.@@$x=6$.'),
e('Équation impossible',1,'',r'Calculer le PGCD de $6$ et $9$.@@L’équation $6x+9y=5$ a-t-elle une solution entière ?@@Et l’équation $6x+9y=3$ ?',r'$3$.@@Non, car le membre de gauche est toujours divisible par $3$.@@Oui : $x=-1,y=1$ donne $-6+9=3$.'),
e('Remonter Euclide',2,r'On travaille avec $35$ et $12$.',r'Effectuer les divisions utiles.@@Trouver un couple de Bézout.@@En déduire un inverse de $12$ modulo $35$.',r'$35=2\times12+11$, $12=11+1$.@@$1=12-(35-2\times12)=3\times12-35$.@@$3$ est un inverse de $12$ modulo $35$.'),
e('Gauss en action',2,'',r'Si $7\mid15n$, montrer que $7\mid n$.@@Si $6\mid4n$, peut-on conclure $6\mid n$ ?@@Quelle divisibilité de $n$ peut-on néanmoins obtenir ?',r'$\operatorname{PGCD}(7,15)=1$ ; Gauss s’applique.@@Non : $n=3$ fournit un contre-exemple.@@$6\mid4n$ implique $3\mid2n$ ; comme $3$ et $2$ sont premiers entre eux, $3\mid n$.'),
e('Congruence avec PGCD non trivial',2,'',r'Résoudre $6x\equiv3\pmod9$.@@Donner les solutions modulo $9$.@@Pourquoi y a-t-il plusieurs classes modulo $9$ ?',r'Diviser par $3$ donne $2x\equiv1\pmod3$ ; donc $x\equiv2\pmod3$.@@Les représentants sont $2,5,8$.@@Le module réduit est $3$ ; trois classes modulo $9$ correspondent à la même classe modulo $3$.'),
e('Toutes les solutions entières',2,r'$15x+21y=6$.',r'Réduire l’équation.@@Trouver une solution particulière.@@Paramétrer toutes les solutions.',r'Diviser par $3$ : $5x+7y=2$.@@$(x_0,y_0)=(-1,1)$.@@$x=-1+7k$, $y=1-5k$, $k\in\Z$, d’après Gauss après soustraction de la solution particulière.'),
e('Une contrainte positive',3,r'$3x+5y=31$, avec $x,y$ entiers naturels.',r'Trouver les solutions entières générales.@@Imposer $x,y\geq0$.@@Interpréter le nombre de solutions admissibles.',r'Une solution est $(2,5)$ ; toutes sont $x=2+5k,y=5-3k$.@@$k\geq0$ et $k\leq1$, donc $k=0$ ou $1$.@@Deux solutions : $(2,5)$ et $(7,2)$. Les contraintes ont réduit une famille infinie à deux couples.'),
e('Inverser modulo $26$',3,'',r'Trouver un inverse de $7$ modulo $26$.@@Résoudre $7x\equiv5\pmod{26}$.@@Vérifier le représentant choisi.',r'$7\times15=105=4\times26+1$, donc inverse $15$.@@$x\equiv75\equiv23\pmod{26}$.@@$7\times23=161=6\times26+5$.'),
e('Deux congruences, problème guidé',3,r'$x\equiv2\pmod3$ et $x\equiv3\pmod5$.',r'Poser $x=2+3k$ et résoudre pour $k$ modulo $5$.@@Donner toutes les solutions.@@Vérifier que la période $15$ est cohérente.',r'$2+3k\equiv3$ donne $3k\equiv1\pmod5$, donc $k\equiv2\pmod5$.@@$k=2+5t$, donc $x=8+15t$, $t\in\Z$.@@Ajouter $15$ conserve les restes modulo $3$ et $5$ ; la différence de deux solutions est divisible par ces deux entiers premiers entre eux, donc par $15$.'),
e('Prouver Gauss',3,'',r'Écrire une identité de Bézout pour $a,b$ premiers entre eux.@@La multiplier par $c$.@@Utiliser $a\mid bc$ pour conclure.',r'Il existe $u,v\in\Z$ tels que $au+bv=1$.@@$auc+bvc=c$.@@Les deux termes de gauche sont divisibles par $a$, donc $a\mid c$. Le caractère premier entre eux est l’hypothèse qui permet l’identité égale à $1$.')
], 'denombrement'))

CHAPTERS.append(c('Nombres premiers et petit théorème de Fermat','Arithmétique',r'Décomposition · Primalité · Crible · Chiffrement',
'Étudier la primalité et décomposer un entier.@@Démontrer l’infinitude des nombres premiers.@@Utiliser le petit théorème de Fermat.@@Comprendre un chiffrement modulaire sur un exemple.',
'PGCD, Bézout, Gauss et congruences.',r'''
\essSection{1}{Les briques multiplicatives des entiers}
Un nombre premier est un entier $p\geq2$ dont les seuls diviseurs positifs sont $1$ et $p$. Le nombre $1$ n'est pas premier.
Si $n\geq2$ est composé, $n=ab$ avec $2\leq a\leq b$ ; alors $a\leq\sqrt n$ et $a$ possède un diviseur premier. Pour tester la primalité, il suffit donc de chercher un diviseur premier au plus égal à $\sqrt n$.
\begin{theoreme}
Tout entier $n\geq2$ se décompose en produit de nombres premiers ; cette décomposition est unique à l'ordre des facteurs près.
\end{theoreme}
L'existence se prouve par récurrence forte : un entier est premier ou produit de deux entiers plus petits, que l'on décompose.
Pour l'unicité, Gauss implique qu'un premier divisant un produit divise un facteur. En comparant deux décompositions, on identifie puis simplifie un premier commun, et on poursuit.
\essSection{2}{Il y en a une infinité}
\begin{demonstration}[Preuve d'Euclide]
Supposer une liste finie $p_1,\ldots,p_r$ contenant tous les nombres premiers.
L'entier $N=p_1\cdots p_r+1>1$ possède un diviseur premier $q$.
Aucun $p_i$ ne divise $N$, car le reste serait $1$. Ainsi $q$ n'est pas dans la liste : contradiction.
On ne prétend pas que $N$ est toujours premier ; son diviseur premier suffit.
\end{demonstration}
\figurelivre{e08-crible.pdf}{Crible d'Ératosthène jusqu'à $50$ : garder chaque premier rencontré et éliminer ses multiples à partir de son carré. Les nombres conservés sont les nombres premiers.}
\begin{python}
def crible(n):
    premiers = [True]*(n+1)
    premiers[0] = False
    if n >= 1: premiers[1] = False
    p = 2
    while p*p <= n:
        if premiers[p]:
            for k in range(p*p, n+1, p):
                premiers[k] = False
        p += 1
    return [k for k in range(n+1) if premiers[k]]
\end{python}
On suppose $n\in\N$. Chaque composé possède un facteur premier au plus sa racine carrée, ce qui explique l'arrêt.
\essSection{3}{Fermat : une implication à respecter}
\begin{theoreme}[Petit théorème de Fermat]
Si $p$ est premier et $p\nmid a$, alors $a^{p-1}\equiv1\pmod p$.
Pour tout entier $a$, $a^p\equiv a\pmod p$.
\end{theoreme}
Une preuve possible : lorsque $p\nmid a$, les restes de $a,2a,\ldots,(p-1)a$ permutent les restes non nuls modulo $p$.
Le produit donne $a^{p-1}(p-1)!\equiv(p-1)!$ ; ce dernier facteur est inversible modulo $p$, donc on simplifie.
\begin{attention}
La réciproque est fausse. Si $a^{n-1}\not\equiv1\pmod n$ avec $a$ premier à $n$, on sait que $n$ est composé. Si la congruence vaut $1$, cela ne prouve pas que $n$ est premier.
Par exemple $341=11\times31$ et $2^{10}\equiv1\pmod{341}$, donc $2^{340}\equiv1$ bien que $341$ soit composé.
\end{attention}
\essSection{4}{Décomposer par un algorithme}
\begin{python}
def facteurs(n):
    resultat = []
    d = 2
    while d*d <= n:
        while n % d == 0:
            resultat.append(d)
            n //= d
        d += 1
    if n > 1: resultat.append(n)
    return resultat
\end{python}
On suppose $n\geq2$. Chaque facteur retiré est premier, car les plus petits facteurs possibles ont déjà été retirés. À la sortie, le dernier facteur éventuel est premier.
\essSection{5}{Un chiffrement affine, exemple pédagogique}
Coder les lettres de $0$ à $25$ ; chiffrer par $y\equiv ax+b\pmod{26}$.
Le déchiffrement est possible si $\operatorname{PGCD}(a,26)=1$ : avec un inverse $u$, $x\equiv u(y-b)\pmod{26}$.
Ces petits systèmes servent à comprendre l'arithmétique ; ils ne constituent pas une protection moderne. Le dossier RSA étudie un autre principe sur des nombres volontairement petits.
''',[
e('Premiers ou composés',1,'',r'Classer $1,2,21,29$.@@Pourquoi suffit-il de tester $2,3,5$ pour $29$ ?@@Décomposer $84$.',r'$1$ n’est ni premier ni composé ; $2,29$ sont premiers ; $21$ est composé.@@$\sqrt{29}<6$ : tout diviseur premier d’un composé serait parmi $2,3,5$. Aucun ne divise $29$.@@$84=2^2\times3\times7$.'),
e('Décomposition et diviseurs',1,r'$360=2^3\times3^2\times5$.',r'Combien a-t-il de diviseurs positifs ?@@Donner le PGCD de $360$ et $84$.@@Donner leur PPCM.',r'$(3+1)(2+1)(1+1)=24$, en choisissant indépendamment chaque exposant.@@Les exposants minimaux donnent $2^2\times3=12$.@@Les maximaux donnent $2^3\times3^2\times5\times7=2520$.'),
e('Fermat direct',1,'',r'Calculer $2^{12}$ modulo $13$ par Fermat.@@En déduire $2^{100}$ modulo $13$.@@Pourquoi $a=13$ ne permet-il pas d’utiliser la première forme du théorème modulo $13$ ?',r'$1$, car $13$ est premier et ne divise pas $2$.@@$100=12\times8+4$, donc $2^{100}\equiv2^4\equiv3$.@@L’hypothèse $13\nmid a$ échoue ; $13^{12}\equiv0$, pas $1$.'),
e('Un chiffrement',1,r'$y\equiv5x+8\pmod{26}$, avec A codé $0$, B codé $1$.',r'Chiffrer A et B.@@Vérifier que $21$ est l’inverse de $5$.@@Écrire la formule de déchiffrement.',r'A donne $8$, soit I ; B donne $13$, soit N.@@$5\times21=105\equiv1\pmod{26}$.@@$x\equiv21(y-8)\pmod{26}$.'),
e('Primalité de $223$',2,'',r'Jusqu’à quelle borne faut-il chercher un diviseur premier ?@@Tester les nombres premiers concernés.@@Conclure.',r'$\sqrt{223}\simeq14{,}93$.@@Tester $2,3,5,7,11,13$. Les restes sont respectivement $1,1,3,6,3,2$.@@Aucun ne divise $223$, donc $223$ est premier.'),
e('Crible',2,'',r'Pourquoi éliminer les multiples de $p$ à partir de $p^2$ ?@@Donner les nombres premiers au plus $20$.@@Tester le programme pour $n=0$ et $n=1$.',r'Les multiples $kp$ avec $2\leq k<p$ ont déjà un facteur premier plus petit que $p$ et ont été éliminés.@@$2,3,5,7,11,13,17,19$.@@Dans les deux cas, la liste rendue est vide ; zéro et un sont marqués faux.'),
e('Décomposition algorithmique',2,'',r'Appliquer \code{facteurs} à $180$.@@Reconstituer le produit.@@Pourquoi le dernier facteur résiduel, s’il est supérieur à $1$, est-il premier ?',r'La liste est $[2,2,3,3,5]$.@@$2^2\times3^2\times5=180$.@@Sinon il posséderait un diviseur au plus sa racine, déjà testé avant l’arrêt ; contradiction.'),
e('Un inverse par Fermat',2,'',r'Utiliser Fermat pour exprimer un inverse de $a$ modulo un premier $p$ lorsque $p\nmid a$.@@Calculer un inverse de $3$ modulo $7$.@@Comparer à Bézout.',r'$a^{p-2}$ convient car $a\times a^{p-2}=a^{p-1}\equiv1$.@@$3^5\equiv5\pmod7$, donc inverse $5$.@@Bézout donne aussi $3\times5-7\times2=1$. Fermat suppose le module premier ; Bézout fonctionne pour tout module premier avec $a$.'),
e('Un faux test de primalité',3,r'$341=11\times31$.',r'Verifier $2^{10}\equiv1\pmod{341}$.@@En déduire $2^{340}\equiv1$.@@Quelle conclusion erronée faut-il éviter ?',r'$2^{10}=1024=3\times341+1$.@@$2^{340}=(2^{10})^{34}\equiv1$.@@On ne doit pas conclure que $341$ est premier. Une congruence de Fermat vérifiée est une condition nécessaire dans ce cadre, pas suffisante.'),
e('L’infinité, sans faux raccourci',3,'',r'Former $N=2\times3\times5\times7\times11\times13+1$.@@Montrer qu’il peut être composé.@@Pourquoi la preuve d’infinitude reste-t-elle valide ?',r'$N=30031$.@@$30031=59\times509$.@@La preuve exige un diviseur premier de $N$, pas que $N$ lui-même soit premier. Aucun premier de la liste initiale ne divise $N$.'),
e('RSA miniature, guidé',3,r'On prend $p=5,q=11,n=55$ et $e=3$. Pour le message $m=7$, on chiffre $c\equiv m^3\pmod{55}$.',r'Calculer $c$.@@Vérifier $3\times27\equiv1\pmod{40}$.@@Calculer \code{pow(13, 27, 55)} et commenter.',r'$7^3=343\equiv13\pmod{55}$.@@$81=2\times40+1$ ; l’exposant de déchiffrement proposé est $27$.@@Le calcul rend $7$, le message initial. Ce petit exemple illustre le mécanisme ; ses nombres sont trop petits pour une sécurité réelle.'),
e('Racine rationnelle, prolongement',3,r'$P(x)=a_nx^n+\cdots+a_0$ a des coefficients entiers. Une racine est $p/q$, fraction irréductible avec $q>0$.',r'Multiplier $P(p/q)=0$ par $q^n$.@@Montrer que $q\mid a_n$.@@Montrer que $p\mid a_0$ si $p\ne0$.',r'$a_np^n+a_{n-1}p^{n-1}q+\cdots+a_0q^n=0$.@@Les autres termes sont divisibles par $q$, donc $q\mid a_np^n$ ; comme $q$ est premier à $p^n$, Gauss donne $q\mid a_n$.@@Isoler le dernier terme : $p\mid a_0q^n$ ; $p$ et $q^n$ sont premiers entre eux, donc Gauss donne $p\mid a_0$.')
], 'denombrement'))

CHAPTERS.append(c('Exponentielle imaginaire et trigonométrie','Nombres complexes',r'Addition · Euler · Moivre · Puissances',
'Passer entre les trois formes d’un complexe.@@Utiliser la relation fonctionnelle de l’exponentielle imaginaire.@@Démontrer une formule d’addition.@@Transformer des expressions avec Euler et Moivre.',
'Cercle trigonométrique, module et arguments.',r'''
\essSection{1}{Les formules d'addition}
Pour tous réels $a,b$,
\[\cos(a-b)=\cos a\cos b+\sin a\sin b,\quad
\cos(a+b)=\cos a\cos b-\sin a\sin b,\]
\[\sin(a+b)=\sin a\cos b+\cos a\sin b.\]
\begin{demonstration}[Une formule issue du produit scalaire]
Les vecteurs unitaires $u=(\cos a,\sin a)$ et $v=(\cos b,\sin b)$ ont un produit scalaire égal à $\cos(a-b)$ par la formule géométrique, et à $\cos a\cos b+\sin a\sin b$ par les coordonnées. L'égalité des expressions prouve la première identité ; remplacer $b$ par $-b$ donne celle du cosinus d'une somme. L'identité du sinus s'obtient en utilisant $\sin t=\cos(\pi/2-t)$.
\end{demonstration}
En prenant $a=b$, on retrouve $\cos2a=\cos^2a-\sin^2a=2\cos^2a-1$ et $\sin2a=2\sin a\cos a$.
\essSection{2}{La notation exponentielle}
\begin{definition}
Pour $\theta\in\R$, on note $\mathrm e^{\mathrm i\theta}=\cos\theta+\mathrm i\sin\theta$.
Si $z\ne0$, sa forme exponentielle est $z=r\mathrm e^{\mathrm i\theta}$ avec $r=|z|>0$.
\end{definition}
Les formules d'addition donnent
$\mathrm e^{\mathrm ia}\mathrm e^{\mathrm ib}=\mathrm e^{\mathrm i(a+b)}$.
Ainsi le produit multiplie les modules et additionne les arguments ; le quotient divise les modules et soustrait les arguments.
\figurelivre{e03-produit.pdf}{Multiplier deux complexes non nuls additionne leurs angles et multiplie leurs longueurs. Exemple : arguments $\pi/6$ et $\pi/3$, argument du produit $\pi/2$.}
\begin{savoirfaire}[Choisir la forme adaptée]
La forme algébrique convient aux sommes et à l'identification des parties réelle et imaginaire. La forme exponentielle convient aux produits, quotients et puissances.
Par exemple $(1+\mathrm i)^8=(\sqrt2)^8\mathrm e^{2\mathrm i\pi}=16$.
Le module s'impose positif ; un signe négatif peut être absorbé en ajoutant $\pi$ à l'argument.
\end{savoirfaire}
\essSection{3}{Moivre et Euler}
\begin{theoreme}[Moivre]
Pour tout entier $n$ et tout réel $\theta$,
$(\cos\theta+\mathrm i\sin\theta)^n=\cos(n\theta)+\mathrm i\sin(n\theta)$.
\end{theoreme}
La relation fonctionnelle prouve l'identité pour les entiers naturels ; l'inverse donne les entiers négatifs.
\begin{propriete}[Euler]
\[\cos\theta=\frac{\mathrm e^{\mathrm i\theta}+\mathrm e^{-\mathrm i\theta}}2,
\qquad \sin\theta=\frac{\mathrm e^{\mathrm i\theta}-\mathrm e^{-\mathrm i\theta}}{2\mathrm i}.\]
\end{propriete}
Ces formules suivent de l'addition et de la soustraction des écritures de $\mathrm e^{\mathrm i\theta}$ et de son conjugué.
\essSection{4}{Linéariser ou développer}
\begin{exemple}[Une puissance de cosinus]
Avec Euler, $\cos^2x=(\mathrm e^{2\mathrm ix}+2+\mathrm e^{-2\mathrm ix})/4=(1+\cos2x)/2$.
Donc $\int_0^{\pi/2}\cos^2x\,\mathrm dx=\pi/4$.
Avec Moivre au cube, identifier les parties réelles donne $\cos3x=4\cos^3x-3\cos x$.
\end{exemple}
La linéarisation remplace une puissance trigonométrique par une somme d'expressions d'angles multiples. Elle sert à intégrer ou à étudier une suite trigonométrique. À l'inverse, Moivre exprime certains angles multiples comme des polynômes en sinus et cosinus.
\essSection{5}{Conserver la périodicité}
Les angles représentent une classe modulo $2\pi$ : $\mathrm e^{\mathrm ia}=\mathrm e^{\mathrm ib}$ si et seulement si $a-b\in2\pi\Z$.
Pour résoudre une équation d'arguments, ne garder qu'une égalité d'angles ordinaires peut faire perdre des solutions. On précise ensuite l'intervalle d'angles ou les points distincts demandés.
''',[
e('Passages de formes',1,'',r'Mettre $2\mathrm e^{\mathrm i\pi/3}$ sous forme algébrique.@@Mettre $-2\mathrm i$ sous forme exponentielle.@@Donner une forme exponentielle de $1-\mathrm i$.',r'$1+\mathrm i\sqrt3$.@@$2\mathrm e^{-\mathrm i\pi/2}$.@@$\sqrt2\mathrm e^{-\mathrm i\pi/4}$.'),
e('Produits et quotients',1,r'$z=2\mathrm e^{\mathrm i\pi/6}$, $w=3\mathrm e^{\mathrm i\pi/3}$.',r'Calculer $zw$.@@Calculer $z/w$.@@Donner le module de $w/z$.',r'$6\mathrm e^{\mathrm i\pi/2}=6\mathrm i$.@@$\tfrac23\mathrm e^{-\mathrm i\pi/6}$.@@$3/2$.'),
e('Puissances',1,'',r'Calculer $(\mathrm e^{\mathrm i\pi/3})^6$.@@Calculer $(1+\mathrm i)^8$.@@Calculer $(\sqrt3+\mathrm i)^3$.',r'$\mathrm e^{2\mathrm i\pi}=1$.@@$16$.@@$\sqrt3+\mathrm i=2\mathrm e^{\mathrm i\pi/6}$, donc le cube vaut $8\mathrm e^{\mathrm i\pi/2}=8\mathrm i$.'),
e('Duplication',1,'',r'Exprimer $\cos2x$ à l’aide de $\cos x$.@@Exprimer $\sin2x$.@@Calculer $\cos(\pi/6+\pi/3)$.',r'$2\cos^2x-1$.@@$2\sin x\cos x$.@@L’angle vaut $\pi/2$, donc le cosinus vaut $0$ ; les formules d’addition donnent aussi $\sqrt3/4-\sqrt3/4=0$.'),
e('Angle $\pi/12$',2,'',r'Écrire $\pi/12$ comme différence de deux angles remarquables.@@Calculer son cosinus.@@Calculer son sinus.',r'$\pi/4-\pi/6$.@@$\cos(\pi/12)=(\sqrt6+\sqrt2)/4$.@@$\sin(\pi/12)=(\sqrt6-\sqrt2)/4$, par la formule de différence.'),
e('Euler au carré',2,'',r'Retrouver $\cos^2x=(1+\cos2x)/2$.@@En déduire une primitive de $\cos^2x$.@@Calculer son intégrale sur $[0,\pi]$.',r'Développer le carré de $(\mathrm e^{\mathrm ix}+\mathrm e^{-\mathrm ix})/2$ et regrouper les exponentielles opposées.@@$x/2+\sin2x/4$.@@$\pi/2$, car le sinus s’annule aux bornes.'),
e('Moivre au cube',2,'',r'Développer $(\cos x+\mathrm i\sin x)^3$.@@Identifier la partie réelle pour retrouver $\cos3x$.@@En déduire $\cos^3x$ comme somme de cosinus.',r'La partie réelle vaut $\cos^3x-3\cos x\sin^2x$ ; l’imaginaire vaut $3\cos^2x\sin x-\sin^3x$.@@$\cos3x=\cos^3x-3\cos x(1-\cos^2x)=4\cos^3x-3\cos x$.@@$\cos^3x=(\cos3x+3\cos x)/4$.'),
e('Une équation exponentielle',2,'',r'Résoudre $\mathrm e^{2\mathrm ix}=1$ pour $x\in\R$.@@Résoudre $\mathrm e^{2\mathrm ix}=-1$.@@Donner les solutions de la seconde équation dans $[0,2\pi[$.',r'$2x\in2\pi\Z$, donc $x=k\pi$.@@$2x=\pi+2k\pi$, donc $x=\pi/2+k\pi$.@@$\pi/2$ et $3\pi/2$.'),
e('Linéariser une puissance quatre',3,'',r'À partir de la duplication, linéariser $\cos^4x$.@@Donner une primitive.@@Calculer $\int_0^{2\pi}\cos^4x\,\mathrm dx$.',r'$\cos^4x=(3+4\cos2x+\cos4x)/8$.@@$3x/8+\sin2x/4+\sin4x/32$.@@$3\pi/4$ ; les termes sinus sont nuls aux bornes.'),
e('Une suite complexe',3,r'$z_n=(1+\mathrm i)^n$.',r'Donner son module et un argument.@@Pour quels $n\in\N$ est-il réel ?@@Pour quels $n$ est-il imaginaire pur ?',r'$|z_n|=2^{n/2}$ ; un argument est $n\pi/4$.@@Lorsque $n\pi/4\in\pi\Z$, soit $n$ multiple de $4$.@@Lorsque $n\pi/4=\pi/2$ modulo $\pi$, soit $n\equiv2\pmod4$.'),
e('Une preuve par le produit scalaire',3,'',r'Choisir deux vecteurs unitaires d’angles $a,b$.@@Calculer leur produit scalaire de deux façons.@@Retrouver le cosinus d’une somme.',r'Prendre $(\cos a,\sin a)$ et $(\cos b,\sin b)$.@@Le calcul par coordonnées vaut $\cos a\cos b+\sin a\sin b$ ; la formule géométrique donne $\cos(a-b)$.@@Remplacer $b$ par $-b$ et utiliser les parités de cosinus et sinus : $\cos(a+b)=\cos a\cos b-\sin a\sin b$.'),
e('Une somme oscillante',3,r'$q=\mathrm e^{\mathrm i\pi/3}$.',r'Calculer $q^6$ et vérifier $q\ne1$.@@Calculer $1+q+\cdots+q^5$.@@En déduire les sommes des cosinus et des sinus des six angles $k\pi/3$.',r'$q^6=1$ et $q\ne1$ car son argument n’est pas nul modulo $2\pi$.@@La somme géométrique vaut $(1-q^6)/(1-q)=0$.@@En prenant les parties réelle et imaginaire, les deux sommes, pour $k=0,\ldots,5$, valent zéro.')
], 'trigo'))

CHAPTERS.append(c('Équations polynomiales','Nombres complexes',r'Second degré · Racines · Factorisation · Degré',
'Résoudre un second degré à coefficients réels dans $\C$.@@Factoriser à partir d’une racine connue.@@Résoudre un troisième degré guidé.@@Démontrer la borne du nombre de racines.',
'Second degré réel, division et identités remarquables.',r'''
\essSection{1}{Le second degré dans $\C$}
Pour $az^2+bz+c=0$ avec $a,b,c\in\R$ et $a\ne0$, poser $\Delta=b^2-4ac$.
Si $\Delta\geq0$, les solutions réelles usuelles restent valables.
\begin{propriete}[Discriminant négatif]
Si $\Delta<0$, les deux solutions sont
$z_1=(-b+\mathrm i\sqrt{-\Delta})/(2a)$ et $z_2=\bar z_1$.
Le polynôme se factorise en $a(z-z_1)(z-z_2)$.
\end{propriete}
\begin{exemple}
Pour $z^2-2z+5=0$, $\Delta=-16$, donc $z=1\pm2\mathrm i$.
Le produit $(z-1-2\mathrm i)(z-1+2\mathrm i)=(z-1)^2+4$ retrouve le polynôme.
\end{exemple}
La complétion du carré $a[(z+b/(2a))^2-\Delta/(4a^2)]$ explique les formules.
\essSection{2}{Une identité de factorisation}
\begin{theoreme}
Pour $n\geq1$,
$z^n-a^n=(z-a)(z^{n-1}+az^{n-2}+\cdots+a^{n-1})$.
\end{theoreme}
\begin{demonstration}
Développer le produit : les termes intermédiaires se compensent deux à deux, ne laissant que $z^n-a^n$.
Si $P(z)=\sum_{k=0}^np_kz^k$ et $P(a)=0$, alors
$P(z)=P(z)-P(a)=\sum_{k=1}^np_k(z^k-a^k)$.
Chaque terme est divisible par $z-a$, donc $P(z)=(z-a)Q(z)$, avec $Q$ de degré $n-1$ si $P$ est de degré $n$.
\end{demonstration}
\essSection{3}{Une racine connue fait baisser le degré}
\begin{savoirfaire}
Pour $P(z)=z^3-2z^2+z-2$, vérifier $P(2)=0$.
Écrire $P(z)=(z-2)(z^2+uz+v)$ ; développer et identifier les coefficients.
On obtient $u=0,v=1$, donc $P(z)=(z-2)(z^2+1)$ et les solutions sont $2,\mathrm i,-\mathrm i$.
La vérification des coefficients et des solutions sécurise le calcul.
\end{savoirfaire}
\figurelivre{e04-racines.pdf}{Les trois racines $2,\mathrm i,-\mathrm i$ de $z^3-2z^2+z-2$ dans le plan complexe. Les coefficients réels rendent les racines non réelles conjuguées deux à deux.}
\essSection{4}{Combien de racines au maximum ?}
\begin{theoreme}
Un polynôme non nul de degré $n$ possède au plus $n$ racines distinctes dans $\C$.
\end{theoreme}
\begin{demonstration}
Une constante non nulle n'a aucune racine. Supposer le résultat vrai au degré $n-1$.
Au degré $n$, si aucune racine n'existe, la borne est respectée. Sinon choisir une racine $a$ et écrire $P=(z-a)Q$.
Toute autre racine est une racine de $Q$, de degré $n-1$ ; il y en a au plus $n-1$. Avec $a$, cela donne au plus $n$.
\end{demonstration}
Ce résultat borne le nombre de racines ; il ne démontre pas à lui seul qu'il y en a exactement $n$. Le théorème fondamental de l'algèbre n'est pas requis pour cette preuve.
Le polynôme nul, dont tous les coefficients sont nuls, est exclu : il s'annule partout.
\essSection{5}{Approfondir sans changer de méthode}
Si un polynôme est à coefficients réels, $P(\bar z)=\overline{P(z)}$ : toute racine non réelle entraîne sa conjuguée.
Pour un trinôme $a(z-z_1)(z-z_2)$, l'identification donne $z_1+z_2=-b/a$ et $z_1z_2=c/a$.
Des équations à coefficients complexes peuvent être étudiées sur des exemples, en cherchant d'abord une racine carrée d'un complexe. Cette extension est un problème possible, distinct de la formule du second degré réel exigible.
''',[
e('Un second degré',1,'',r'Résoudre $z^2+1=0$.@@Résoudre $z^2+4=0$.@@Factoriser $z^2+4$ dans $\C$.',r'$z=\pm\mathrm i$.@@$z=\pm2\mathrm i$.@@$(z-2\mathrm i)(z+2\mathrm i)$.'),
e('Discriminant',1,'',r'Résoudre $z^2-2z+5=0$.@@Donner la somme et le produit des racines.@@Vérifier les coefficients par ces deux valeurs.',r'$1\pm2\mathrm i$.@@Somme $2$, produit $5$.@@$(z-z_1)(z-z_2)=z^2-(z_1+z_2)z+z_1z_2=z^2-2z+5$.'),
e('Différence de puissances',1,'',r'Factoriser $z^3-1$.@@Factoriser $z^4-16$ par $z-2$.@@Quel est le degré du quotient dans ce second cas ?',r'$(z-1)(z^2+z+1)$.@@$(z-2)(z^3+2z^2+4z+8)$.@@$3$, un degré de moins que le polynôme initial.'),
e('Vérifier une racine',1,r'$P(z)=z^3-3z^2+4z-2$.',r'Calculer $P(1)$.@@Vérifier $P(z)=(z-1)(z^2-2z+2)$.@@Résoudre $P(z)=0$.',r'$1-3+4-2=0$.@@Le développement donne $z^3-3z^2+4z-2$.@@$z=1$ ou $z^2-2z+2=0$ ; les solutions sont $1,1+\mathrm i,1-\mathrm i$.'),
e('Troisième degré',2,r'$P(z)=z^3-2z^2+z-2$.',r'Vérifier que $2$ est racine.@@Trouver le quotient par $z-2$.@@Donner toutes les racines.',r'$8-8+2-2=0$.@@$P=(z-2)(z^2+1)$ par développement ou identification.@@$2,\mathrm i,-\mathrm i$.'),
e('Coefficient dominant',2,r'$2z^2+4z+10=0$.',r'Calculer le discriminant.@@Résoudre.@@Écrire la factorisation avec son coefficient dominant.',r'$\Delta=16-80=-64$.@@$z=(-4\pm8\mathrm i)/4=-1\pm2\mathrm i$.@@$2(z+1-2\mathrm i)(z+1+2\mathrm i)$ ; le facteur $2$ ne doit pas disparaître.'),
e('Racines conjuguées',2,r'Un polynôme réel admet $2+\mathrm i$ comme racine.',r'Quelle autre racine est imposée ?@@Calculer le produit des deux facteurs associés.@@S’il est de degré $3$ et admet aussi $-1$, donner un polynôme unitaire possible.',r'$2-\mathrm i$, par conjugaison.@@$(z-2-\mathrm i)(z-2+\mathrm i)=z^2-4z+5$.@@$(z+1)(z^2-4z+5)=z^3-3z^2+z+5$.'),
e('Une équation bicarrée',2,'',r'Résoudre $z^4+5z^2+4=0$ en posant $w=z^2$.@@Résoudre les deux équations obtenues sur $z$.@@Vérifier le nombre maximal de solutions.',r'$w^2+5w+4=(w+1)(w+4)=0$, donc $w=-1$ ou $w=-4$.@@$z=\pm\mathrm i$ ou $z=\pm2\mathrm i$.@@Il y a quatre racines distinctes, ce qui atteint la borne du degré $4$.'),
e('Racine double',3,r'$P(z)=(z-1)^2(z+2)$.',r'Développer $P$.@@Combien a-t-il de racines distinctes ?@@Pourquoi cela ne contredit-il pas le théorème sur le degré ?',r'$P(z)=z^3-3z+2$.@@Deux : $1$ et $-2$ ; $1$ est répété dans la factorisation.@@Le théorème donne au plus trois racines distinctes, et non nécessairement trois.'),
e('Une identité de polynômes',3,r'Deux polynômes de degré au plus $2$ prennent les mêmes valeurs en trois points distincts.',r'Considérer leur différence.@@Justifier qu’elle est nulle.@@En déduire une méthode pour vérifier une identité de degré au plus $2$.',r'La différence est un polynôme de degré au plus $2$ possédant trois racines distinctes.@@Si elle était non nulle, elle aurait au plus deux racines. Elle est donc le polynôme nul.@@Vérifier l’égalité en trois points distincts suffit lorsqu’on connaît effectivement la borne de degré.'),
e('Carrée d’un complexe, guidée',3,r'On cherche les $w=x+\mathrm iy$ tels que $w^2=3+4\mathrm i$.',r'Écrire les équations sur $x,y$.@@Utiliser $|w|^2=|3+4\mathrm i|$ pour trouver $x^2,y^2$.@@Donner les deux solutions.',r'$x^2-y^2=3$ et $2xy=4$.@@$x^2+y^2=5$ ; addition et soustraction donnent $x^2=4,y^2=1$.@@La contrainte $xy=2$ impose les mêmes signes : $w=2+\mathrm i$ ou $w=-2-\mathrm i$.'),
e('Preuve par le degré',3,'',r'Pourquoi une constante non nulle n’a-t-elle pas de racine ?@@Si $P=(z-a)Q$, pourquoi toute racine différente de $a$ annule-t-elle $Q$ ?@@Conclure l’étape de récurrence sur le degré.',r'Sa valeur ne change jamais et reste différente de zéro.@@Pour une racine $b\ne a$, $0=(b-a)Q(b)$ avec $b-a\ne0$, donc $Q(b)=0$.@@Si $P$ a degré $n$, $Q$ a degré $n-1$ ; il possède au plus $n-1$ racines distinctes. En ajoutant $a$, on obtient la borne $n$.')
], 'courbe'))

CHAPTERS.append(c('Géométrie et racines de l’unité','Nombres complexes',r'Quotient · Angles · Alignement · Polygones',
'Interpréter module et argument d’un quotient.@@Prouver un alignement ou une orthogonalité.@@Déterminer les racines $n$-ièmes de l’unité.@@Utiliser les complexes dans une configuration géométrique.',
'Affixes, distances, forme exponentielle et équations.',r'''
\essSection{1}{Le bon quotient pour le bon angle}
Pour des points $A,B,C$ d'affixes $a,b,c$, avec $A\ne B$ et $A\ne C$, poser $q=(c-a)/(b-a)$.
\[|q|=AC/AB,\qquad \arg(q)=(\vect{AB},\vect{AC})\pmod{2\pi}.\]
Le numérateur correspond au vecteur d'arrivée et le dénominateur au vecteur de départ de l'angle. Inverser le quotient change le signe de l'angle.
\begin{propriete}
$A,B,C$ sont alignés si et seulement si $q\in\R$.
Les droites $(AB)$ et $(AC)$ sont perpendiculaires si et seulement si $q$ est imaginaire pur, les vecteurs étant non nuls.
\end{propriete}
\figurelivre{e05-quotient.pdf}{Avec $a=1$, $b=3$ et $c=1+2\mathrm i$, le quotient $(c-a)/(b-a)=\mathrm i$ a module $1$ et argument $\pi/2$ : triangle rectangle isocèle en $A$.}
\begin{savoirfaire}[Une preuve géométrique courte]
Écrire les affixes des vecteurs ; vérifier les dénominateurs non nuls ; calculer le quotient ; interpréter réalité, caractère imaginaire pur, module ou argument ; conclure avec les points de la figure.
\end{savoirfaire}
\essSection{2}{Les racines de l'unité}
\begin{theoreme}
Pour $n\geq1$, les solutions de $z^n=1$ sont les $n$ nombres distincts
$\omega_k=\mathrm e^{2\mathrm ik\pi/n}$, pour $k=0,\ldots,n-1$.
Ils forment un polygone régulier sur le cercle unité lorsque $n\geq3$.
\end{theoreme}
\begin{demonstration}
Si $z^n=1$, $|z|^n=1$ impose $|z|=1$. Écrire $z=\mathrm e^{\mathrm i\theta}$ ; alors $n\theta\in2\pi\Z$, soit $\theta=2k\pi/n$.
Les indices se ramènent modulo $n$ à $0,\ldots,n-1$ ; ces angles donnent des points distincts car leurs différences sont strictement inférieures à $2\pi$ en valeur absolue. La réciproque se vérifie en élevant à la puissance $n$.
\end{demonstration}
\figurelivre{e05-unite.pdf}{Racines de l'unité pour $n=3,4,6$. Les points sont espacés d'un angle $2\pi/n$ ; le premier est toujours le point d'affixe $1$.}
Pour $n=2$, on obtient $1,-1$. Pour $n=3$, on note souvent $j=\mathrm e^{2\mathrm i\pi/3}$ : $1+j+j^2=0$ et $\bar j=j^2$.
\essSection{3}{Des longueurs et des sommes}
Pour $n\geq2$, la somme des racines $n$-ièmes de l'unité vaut zéro : avec $q=\mathrm e^{2\mathrm i\pi/n}\ne1$, la somme géométrique donne $(1-q^n)/(1-q)=0$.
La longueur d'un côté d'un polygone régulier inscrit dans un cercle de rayon $R$ vaut $2R\sin(\pi/n)$ : le triangle formé par le centre et deux sommets voisins se partage en deux triangles rectangles.
\essSection{4}{Transformations et suites, en problème guidé}
Une application $z\mapsto az+b$ avec $a\ne0$ multiplie les longueurs par $|a|$ et ajoute $\arg a$ aux directions. Si $a\ne1$, son point fixe a pour affixe $\ell=b/(1-a)$.
La suite $z_{n+1}=az_n+b$ vérifie $z_n-\ell=a^n(z_0-\ell)$.
Pour $|a|<1$, les points s'approchent de $\ell$ ; leur trajectoire peut tourner si $a$ n'est pas réel positif.
Ce prolongement fait travailler ensemble récurrence, modules et arguments ; la démonstration reprend le décalage de l'équilibre des suites réelles.
''',[
e('Un quotient géométrique',1,r'$a=0,b=2,c=2\mathrm i$.',r'Calculer $(c-a)/(b-a)$.@@Donner son module et un argument.@@Décrire le triangle.',r'$\mathrm i$.@@Module $1$, argument $\pi/2$ modulo $2\pi$.@@$AB=AC$ et l’angle en $A$ est droit : triangle rectangle isocèle en $A$.'),
e('Alignement',1,r'$a=1+\mathrm i,b=3+2\mathrm i,c=5+3\mathrm i$.',r'Calculer $b-a$ et $c-a$.@@Calculer leur quotient.@@Conclure et préciser l’ordre des points.',r'$b-a=2+\mathrm i$, $c-a=4+2\mathrm i$.@@$(c-a)/(b-a)=2$, réel positif.@@Les points sont alignés et $B$ est le milieu de $[AC]$.'),
e('Racines quatrièmes',1,'',r'Résoudre $z^4=1$.@@Placer les solutions.@@Calculer leur somme.',r'$1,\mathrm i,-1,-\mathrm i$.@@Les quatre points sont aux intersections des axes et du cercle unité : ils forment un carré.@@$1+\mathrm i-1-\mathrm i=0$.'),
e('Racines cubiques',1,'',r'Écrire $j=\mathrm e^{2\mathrm i\pi/3}$ sous forme algébrique.@@Donner $j^2$ et $j^3$.@@Vérifier $1+j+j^2=0$.',r'$j=-1/2+\mathrm i\sqrt3/2$.@@$j^2=-1/2-\mathrm i\sqrt3/2$ et $j^3=1$.@@Les parties imaginaires se compensent et les parties réelles donnent $1-1/2-1/2=0$.'),
e('Perpendicularité',2,r'$a=1+\mathrm i,b=3+2\mathrm i,c=-1+5\mathrm i$.',r'Calculer le quotient $(c-a)/(b-a)$.@@En déduire la perpendicularité.@@Comparer les longueurs $AC$ et $AB$.',r'$(-2+4\mathrm i)/(2+\mathrm i)=2\mathrm i$.@@Ce quotient est imaginaire pur non nul : les droites sont perpendiculaires.@@Son module vaut $2$, donc $AC=2AB$.'),
e('Un angle orienté',2,r'$a=0,b=1+\mathrm i,c=\sqrt3+\mathrm i$.',r'Donner les arguments de $b$ et $c$.@@Calculer l’angle orienté $(\vect{AB},\vect{AC})$.@@Donner le rapport des longueurs.',r'$\arg b=\pi/4$, $\arg c=\pi/6$ modulo $2\pi$.@@$\pi/6-\pi/4=-\pi/12$ modulo $2\pi$.@@$AC/AB=2/\sqrt2=\sqrt2$.'),
e('Un hexagone',2,'',r'Donner les racines sixièmes de l’unité sous forme exponentielle.@@Donner la longueur de ses côtés.@@Calculer la somme de ses sommets sous forme complexe.',r'$\mathrm e^{\mathrm ik\pi/3}$ pour $k=0,\ldots,5$.@@$2\sin(\pi/6)=1$ dans le cercle unité.@@La somme vaut zéro, par somme géométrique ou par paires de sommets opposés.'),
e('Un lieu d’angle',2,r'$a=0,b=2$, et l’on cherche les $c$ tels que $(c-a)/(b-a)$ soit imaginaire pur.',r'Traduire avec $c=x+\mathrm iy$.@@Décrire le lieu si $c\ne a$.@@Que signifie l’absence de condition sur le module ?',r'$c/2=x/2+\mathrm iy/2$ est imaginaire pur si et seulement si $x=0$.@@L’axe imaginaire privé de l’origine.@@La distance $AC$ est libre ; seule la direction est imposée.'),
e('Racines d’un autre complexe',3,r'On cherche $z^3=8\mathrm i$.',r'Déterminer le module des solutions.@@Déterminer leurs arguments.@@Donner les trois solutions sous forme exponentielle.',r'$|z|^3=8$, donc $|z|=2$.@@$3\theta=\pi/2+2k\pi$, donc $\theta=\pi/6+2k\pi/3$.@@$2\mathrm e^{\mathrm i\pi/6}$, $2\mathrm e^{5\mathrm i\pi/6}$, $2\mathrm e^{3\mathrm i\pi/2}$ ; il suffit de $k=0,1,2$.'),
e('Spirale convergente',3,r'$z_0=1$, $z_{n+1}=(\mathrm i/2)z_n$.',r'Exprimer $z_n$.@@Donner son module et un argument.@@Décrire le comportement géométrique.',r'$z_n=(\mathrm i/2)^n$.@@$|z_n|=2^{-n}$ et un argument vaut $n\pi/2$.@@Chaque étape tourne de $\pi/2$ et divise la distance à l’origine par $2$ ; les points tendent vers $O$.'),
e('Avec un point fixe',3,r'$z_{n+1}=(\mathrm i/2)z_n+1$ et $z_0=0$.',r'Trouver le point fixe $\ell$.@@Exprimer $z_n-\ell$.@@En déduire la limite.',r'$\ell=1/(1-\mathrm i/2)=4/5+2\mathrm i/5$.@@$z_{n+1}-\ell=(\mathrm i/2)(z_n-\ell)$, donc $z_n-\ell=-\ell(\mathrm i/2)^n$.@@Le module de l’écart vaut $|\ell|2^{-n}\to0$ ; $z_n\to\ell$.'),
e('La somme et le polygone',3,r'$n\geq3$ et $\omega=\mathrm e^{2\mathrm i\pi/n}$.',r'Prouver $1+\omega+\cdots+\omega^{n-1}=0$.@@Interpréter le point moyen des sommets.@@Cette preuve fonctionne-t-elle pour $n=1$ ?',r'$\omega\ne1$ et $\omega^n=1$ ; la somme géométrique vaut zéro.@@L’affixe du point moyen est la somme divisée par $n$, donc zéro : le centre est le point moyen des sommets.@@Non : le dénominateur $1-\omega$ s’annule et la somme vaut $1$. Il faut conserver l’hypothèse $n\geq2$ pour cette identité.')
], 'trigo'))
