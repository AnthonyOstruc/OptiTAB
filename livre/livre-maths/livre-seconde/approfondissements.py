"""Parcours facultatif : tous les approfondissements nommés au programme sont traités."""
from dataclasses import dataclass
from modele import Q,tableau

@dataclass
class Defi:
    titre:str
    prerequis:str
    enonce:str
    indices:list
    solutions:list
    controle:str
    figure:str=''

DEFIS=[
Defi('Décimales finies et périodes','Chapitres 1 et 2',
r"""On étudie les écritures décimales de fractions irréductibles positives $p/q$.
"""+Q(r"""Montrer que $p/q$ est décimal si et seulement si $q$ ne contient que des facteurs premiers 2 et 5. On peut utiliser l’unicité de la décomposition en facteurs premiers.""",r"""Effectuer la division de $1$ par 7 jusqu’au retour du premier reste. Donner la période.""",r"""Expliquer pourquoi la division d’un rationnel donne une écriture finie ou une écriture périodique à partir d’un certain rang."""),
[r"""Une écriture décimale finie s’écrit $N/10^k$ ; utiliser $10^k=2^k5^k$.""",r"""Dans une division par $q$, les restes possibles sont $0,1,\ldots,q-1$. Que se passe-t-il si un reste revient ?"""],
[r"""\editionEtape{1. Caractériser les fractions décimales}
Si $p/q=N/10^k$, alors $p10^k=Nq$. Comme $p$ et $q$ sont premiers entre eux, tous les facteurs premiers de $q$ doivent diviser $10^k$ : ce sont 2 et 5. Réciproquement, si $q=2^a5^b$, choisir $k\ge a,b$ permet de multiplier numérateur et dénominateur pour obtenir $10^k$. La fraction a donc une écriture décimale finie.
\editionEtape{2. Calculer une période}
Pour $1/7$, les chiffres produits sont 1, 4, 2, 8, 5, 7 et les restes successifs 3, 2, 6, 4, 5, 1. Le reste initial 1 revient : $\res{1/7=0{,}\overline{142857}}$.
\editionEtape{3. Justifier la répétition}
S’il apparaît un reste nul, la division s’arrête. Sinon, les restes non nuls sont en nombre fini : l’un finit par revenir. À partir d’un même reste, la division produit les mêmes chiffres et les mêmes restes. Le développement devient périodique.
\editionRetenir{Le nombre fini de restes explique la périodicité. Observer six chiffres ne suffit pas sans le retour d’un reste.}"""],
'assert Rational(1,7)==Rational(142857,999999) and [10**k%7 for k in range(1,7)]==[3,2,6,4,5,1]'),
Defi('Deux identités à construire','Chapitre 3',
Q(r"""Développer $(a+b+c)^2$ en faisant apparaître les carrés et les doubles produits.""",r"""Déduire le développement de $(a+b)^3$ en multipliant $(a+b)^2$ par $(a+b)$.""",r"""Utiliser ces identités pour calculer $103^3$ et $(10+2+1)^2$."""),
[r"""Traiter $a+b+c$ comme une somme de trois termes et distribuer chaque terme.""",r"""Dans le cube, regrouper les trois occurrences de $a^2b$ et les trois de $ab^2$."""],
[r"""\editionEtape{1. Compter tous les produits}
La multiplication des deux sommes donne $a^2+b^2+c^2+ab+ba+ac+ca+bc+cb$, soit
\[\res{(a+b+c)^2=a^2+b^2+c^2+2ab+2ac+2bc}.\]
\editionEtape{2. Construire le cube}
On multiplie $a^2+2ab+b^2$ par $a+b$. En regroupant :
\[\res{(a+b)^3=a^3+3a^2b+3ab^2+b^3}.\]
\editionEtape{3. Calculer avec un choix adapté}
Pour $103^3$, choisir $a=100$, $b=3$ : $1000000+90000+2700+27=\res{1092727}$. Pour le carré à trois termes, on obtient $100+4+1+40+20+4=\res{169}$.
\editionRetenir{Les coefficients proviennent du nombre d’occurrences de chaque produit. Une formule se reconstruit si l’on maîtrise la distributivité.}"""],
'a,b,c=symbols("a b c"); assert expand((a+b+c)**2-(a*a+b*b+c*c+2*a*b+2*a*c+2*b*c))==0 and expand((a+b)**3-(a**3+3*a*a*b+3*a*b*b+b**3))==0 and 103**3==1092727'),
Defi('Moyennes et rectangle optimal','Chapitres 3 et 7',
r"""Pour $a,b>0$, on appelle moyenne arithmétique $(a+b)/2$ et moyenne géométrique $\sqrt{ab}$."""+Q(r"""Partir de $(\sqrt a-\sqrt b)^2\ge0$ pour comparer ces deux moyennes et préciser le cas d’égalité.""",r"""Deux côtés d’un rectangle positif ont une somme égale à 18. Déterminer son aire maximale.""",r"""À aire fixée à 36, déterminer le périmètre minimal."""),
[r"""Développer le carré puis isoler $2\sqrt{ab}$.""",r"""Pour la dernière question, $\sqrt{ab}$ est fixe ; l’inégalité donne une borne de $a+b$."""],
[r"""\editionEtape{1. Établir l’inégalité}
Le carré donne $a+b-2\sqrt{ab}\ge0$, donc $\res{\sqrt{ab}\le(a+b)/2}$. L’égalité exige $\sqrt a=\sqrt b$, donc $a=b$.
\editionEtape{2. Maximiser à somme fixée}
Si $a+b=18$, alors $\sqrt{ab}\le9$, donc $ab\le81$. L’égalité est atteinte pour $\res{a=b=9}$ : l’aire maximale vaut $\res{81}$.
\editionEtape{3. Minimiser à produit fixé}
Si $ab=36$, alors $(a+b)/2\ge6$, donc le périmètre $2(a+b)\ge24$. La borne est atteinte pour $\res{a=b=6}$. Le périmètre minimal vaut $\res{24}$.
\editionRetenir{Une inégalité n’établit un optimum qu’après vérification que son cas d’égalité est réalisable sous la contrainte.}"""],
'assert 9*9==81 and 2*(6+6)==24 and 6*6==36','defi-moyennes'),
Defi('Barycentres de deux et trois points','Chapitres 8 et 9',
r"""Pour des points de position $A$ et $B$ et des poids réels $\alpha,\beta$ de somme non nulle, on définit ici $G$ par $\alpha\vect{GA}+\beta\vect{GB}=\vec0$."""+Q(r"""Exprimer les coordonnées de $G$ en fonction des poids et des coordonnées des deux points.""",r"""Pour $A(0;0)$, $B(6;0)$ et les poids 2 et 1, construire $G$. Que devient la position avec les poids 2 et $-1$ ?""",r"""Étendre la formule à trois points de poids $\alpha,\beta,\gamma$ de somme non nulle. Application : $A(0;0)$, $B(6;0)$, $C(0;6)$, poids 1, 1 et 2."""),
[r"""Écrire $\vect{GA}=A-G$ en coordonnées, puis regrouper les termes contenant $G$.""",r"""Des poids positifs donnent un point entre deux points ; un poids négatif peut produire un point extérieur au segment."""],
[r"""\editionEtape{1. Résoudre l’égalité vectorielle}
En coordonnées, $\alpha(A-G)+\beta(B-G)=0$ donne $(\alpha+\beta)G=\alpha A+\beta B$. Ainsi
\[G\left(\frac{\alpha x_A+\beta x_B}{\alpha+\beta};\frac{\alpha y_A+\beta y_B}{\alpha+\beta}\right).\]
Pour les poids 2 et 1, $\res{G(2;0)}$. Pour 2 et $-1$, $\res{G(-6;0)}$ ; le point sort bien du segment.
\editionEtape{2. Étendre à trois points}
Le même regroupement donne $G=(\alpha A+\beta B+\gamma C)/(\alpha+\beta+\gamma)$. Avec les poids 1, 1 et 2, on obtient $\res{G(3/2;3)}$. On contrôle que les trois vecteurs pondérés depuis ce point ont une somme nulle.
\editionRetenir{La somme des poids doit être non nulle pour déterminer ce point par la formule. Le milieu correspond aux deux poids égaux.}"""],
'assert (2*Matrix([0,0])+Matrix([6,0]))/3==Matrix([2,0]) and (2*Matrix([0,0])-Matrix([6,0]))==Matrix([-6,0]) and (Matrix([0,0])+Matrix([6,0])+2*Matrix([0,6]))/4==Matrix([Rational(3,2),3])','defi-barycentres'),
Defi('Pourquoi les médianes se coupent','Chapitres 8 et 9',
r"""Soient trois points non alignés $A,B,C$. On note $G=(A+B+C)/3$ en coordonnées et $I$ le milieu de $[BC]$."""+Q(r"""Montrer $\vect{AG}=\dfrac23\vect{AI}$.""",r"""En déduire que les trois médianes sont concourantes en $G$, l’isobarycentre des trois points.""",r"""Pour $A(0;0)$, $B(6;0)$ et $C(0;6)$, calculer $G$ et vérifier les trois relations."""),
[r"""Remplacer $I$ par $(B+C)/2$ et comparer les expressions de $G-A$ et de $I-A$.""",r"""Le calcul ne privilégie aucun sommet : reprendre le même argument depuis $B$ et $C$."""],
[r"""\editionEtape{1. Comparer les deux déplacements}
On a $G-A=(B+C-2A)/3$ et $I-A=(B+C-2A)/2$. Donc $\res{\vect{AG}=\tfrac23\vect{AI}}$. Cela place $G$ sur la médiane issue de $A$, aux deux tiers depuis le sommet.
\editionEtape{2. Passer aux trois médianes}
Le même calcul en échangeant les lettres place $G$ sur les médianes issues de $B$ et de $C$. Les médianes sont donc concourantes. Deux médianes d’un triangle non aplati sont distinctes, leur intersection est unique.
\editionEtape{3. Contrôler l’exemple}
Pour le triangle proposé, $\res{G(2;2)}$. Les milieux sont $(3;3)$, $(0;3)$ et $(3;0)$. Les déplacements depuis chaque sommet confirment le coefficient $2/3$.
\editionRetenir{L’égalité vectorielle donne à la fois l’appartenance aux médianes et la position précise du point de concours.}"""],
'A=Matrix([0,0]);B=Matrix([6,0]);C=Matrix([0,6]);G=(A+B+C)/3; assert G==Matrix([2,2]) and all(G-P==Rational(2,3)*((Q+R)/2-P) for P,Q,R in [(A,B,C),(B,A,C),(C,A,B)])','defi-medianes'),
Defi('Concours des hauteurs','Chapitre 9 ; parallèles et médiatrices',
r"""Dans un triangle non aplati $ABC$, on construit $A'=B+C-A$, $B'=A+C-B$ et $C'=A+B-C$ en coordonnées. Ces points forment un grand triangle dont les côtés sont parallèles à ceux de $ABC$."""+Q(r"""Montrer que $A$ est le milieu de $[B'C']$, et faire les deux autres calculs analogues.""",r"""Montrer que $(B'C')$ est parallèle à $(BC)$.""",r"""En admettant ou en utilisant la preuve du concours des médiatrices du défi D08, en déduire que les trois hauteurs de $ABC$ sont concourantes."""),
[r"""Additionner les coordonnées de $B'$ et de $C'$, puis diviser par 2.""",r"""La hauteur passant par $A$ devient la médiatrice d’un côté du grand triangle."""],
[r"""\editionEtape{1. Situer les milieux}
$B'+C'=(A+C-B)+(A+B-C)=2A$. Donc $A$ est le milieu de $[B'C']$. De même, $B$ et $C$ sont les milieux des deux autres côtés.
\editionEtape{2. Relier les directions}
$\vect{B'C'}=C'-B'=2(B-C)=-2\vect{BC}$. Les côtés correspondants sont parallèles. La droite passant par $A$ et perpendiculaire à $(BC)$ est donc aussi perpendiculaire à $(B'C')$ en son milieu : c’est sa médiatrice.
\editionEtape{3. Utiliser un concours déjà établi}
Les trois hauteurs de $ABC$ sont les trois médiatrices du triangle $A'B'C'$. Celles-ci sont concourantes par D08 ; les hauteurs le sont donc également. Leur point de concours est appelé orthocentre.
\editionRetenir{Transformer une configuration en une autre peut ramener une preuve à un théorème déjà connu. Le recours à D08 est annoncé, pour éviter une preuve circulaire.}"""],
'A=Matrix([0,0]);B=Matrix([6,0]);C=Matrix([2,4]);Ap=B+C-A;Bp=A+C-B;Cp=A+B-C;assert (Bp+Cp)/2==A and Cp-Bp==-2*(C-B)','defi-hauteurs'),
Defi('Une aire à partir de deux côtés et d’un angle','Chapitre 9 ; trigonométrie du triangle rectangle',
r"""Dans un triangle, les côtés $CA=b$ et $CB=a$ forment l’angle $C$."""+Q(r"""Pour $C$ aigu, utiliser une hauteur pour établir $\mathcal A=\dfrac12ab\sin C$.""",r"""Pour $C$ obtus, on définit dans ce prolongement $\sin C=\sin(180^\circ-C)$. Reprendre la démonstration avec la hauteur extérieure au segment.""",r"""Calculer l’aire pour $a=8$, $b=5$, $C=30^\circ$, puis pour $C=150^\circ$. Les deux triangles ont-ils nécessairement le même troisième côté ?"""),
[r"""Prendre $CB$ comme base et abaisser la hauteur depuis $A$.""",r"""Les angles supplémentaires ont ici le même sinus ; cela ne fixe pas la forme complète du triangle."""],
[r"""\editionEtape{1. Identifier la hauteur}
Avec la base $CB=a$, la hauteur issue de $A$ vaut $h=b\sin C$ lorsque l’angle est aigu. Donc $\mathcal A=ah/2=\res{ab\sin C/2}$.
\editionEtape{2. Étendre au cas obtus}
La hauteur tombe alors sur le prolongement de la base. Dans le triangle rectangle auxiliaire, elle vaut $b\sin(180^\circ-C)$. La définition annoncée du sinus obtus donne la même formule. Le cas droit donne directement $ab/2$.
\editionEtape{3. Appliquer sans surinterpréter}
Pour 30 et 150 degrés, le sinus vaut $1/2$. Les deux aires valent $\res{10}$. Les troisièmes côtés ne sont pas les mêmes : l’angle et la position du sommet changent. Une aire identique ne détermine pas un triangle unique.
\editionRetenir{L’extension du sinus aux angles obtus est explicitée ici ; elle n’est pas supposée acquise dans le cours de base.}"""],
'assert 8*5*sin(pi/6)/2==10 and sin(5*pi/6)==sin(pi/6)','defi-aire-angle'),
Defi('Concours des médiatrices et cercle circonscrit','Chapitre 9',
r"""Dans un triangle non aplati $ABC$, les médiatrices de $[AB]$ et $[AC]$ se coupent en $O$."""+Q(r"""Justifier qu’elles ne sont pas parallèles.""",r"""Montrer que $O$ appartient aussi à la médiatrice de $[BC]$.""",r"""En déduire l’existence et l’unicité du cercle passant par les trois sommets. Illustrer pour $A(0;0)$, $B(6;0)$, $C(2;4)$."""),
[r"""Si deux médiatrices étaient parallèles, leurs côtés perpendiculaires le seraient aussi.""",r"""Utiliser successivement $OA=OB$ et $OA=OC$."""],
[r"""\editionEtape{1. Assurer l’intersection}
Les droites $(AB)$ et $(AC)$ sont sécantes et distinctes puisque le triangle n’est pas aplati. Leurs perpendiculaires ne sont donc pas parallèles. Les deux médiatrices se coupent en un unique point $O$.
\editionEtape{2. Établir le troisième rattachement}
L’appartenance aux deux médiatrices donne $OA=OB$ et $OA=OC$, donc $OB=OC$. Par la caractérisation de la médiatrice, $O$ est aussi sur celle de $[BC]$.
\editionEtape{3. Construire et vérifier le cercle}
Le cercle de centre $O$ et de rayon $OA>0$ passe par $A,B,C$. Tout autre centre possible serait sur les deux premières médiatrices, donc égal à $O$. Dans l’exemple, $x_O=3$. L’égalité $OA^2=OC^2$ donne $9+y^2=1+(y-4)^2$, d’où $\res{O(3;1)}$ et $\res{R=\sqrt{10}}$.
\editionRetenir{Le centre d’un cercle circonscrit n’est pas toujours à l’intérieur du triangle. La preuve repose sur l’équidistance, indépendamment du dessin.}"""],
'assert [(a-3)**2+(b-1)**2 for a,b in [(0,0),(6,0),(2,4)]]==[10,10,10]','defi-circonscrit'),
Defi('Un lieu parabolique','Chapitres 9 et 10',
r"""On cherche les points $M(x;y)$ équidistants du point $F(0;2)$ et de l’axe des abscisses. La distance de $M$ à cet axe est $|y|$."""+Q(r"""Traduire l’équidistance par une égalité de carrés.""",r"""Montrer que le lieu a pour équation $y=1+x^2/4$.""",r"""Justifier la réciproque et déterminer son point le plus bas. Trouver les points de ce lieu sur $y=5$."""),
[r"""La distance au point $F$ est $\sqrt{x^2+(y-2)^2}$.""",r"""Les deux distances sont positives ou nulles : une égalité de leurs carrés est équivalente à leur égalité."""],
[r"""\editionEtape{1. Traduire et simplifier}
$MF^2=x^2+(y-2)^2$ et la distance à l’axe a pour carré $y^2$. L’égalité donne $x^2+y^2-4y+4=y^2$, donc $\res{y=1+x^2/4}$.
\editionEtape{2. Contrôler la réciproque}
Pour un point vérifiant cette équation, le calcul inverse donne $MF^2=y^2$. Les deux distances étant positives, $MF=|y|$. Le point appartient bien au lieu. L’équation obtenue décrit ainsi exactement l’ensemble, sans point parasite.
\editionEtape{3. Exploiter le modèle}
Le carré est positif, donc $y\ge1$, avec égalité pour $x=0$ : le point le plus bas est $\res{(0;1)}$. Sur $y=5$, $x^2=16$ ; les points sont $\res{(-4;5)\text{ et }(4;5)}$.
\editionRetenir{Un ensemble défini par une distance peut devenir une courbe d’équation simple. Il faut prouver les deux sens de l’équivalence.}"""],
'assert expand(x*x+(y-2)**2-y*y)==x*x-4*y+4 and solveset(1+x*x/4-5,x,domain=S.Reals)==FiniteSet(-4,4)','defi-parabole'),
Defi('Des inégalités décrivent une région','Chapitres 4 et 10',
r"""On cherche les couples $(x;y)$ tels que $x\ge0$, $y\ge0$, $x+y\le8$ et $x+2y\le12$."""+Q(r"""Représenter la région et déterminer ses sommets.""",r"""On souhaite maximiser $R=3x+4y$. Démontrer directement que $R\le28$ en combinant deux contraintes.""",r"""Trouver le cas d’égalité. Pourquoi comparer seulement quelques points dessinés n’aurait-il pas suffi à la preuve ?"""),
[r"""Les deux droites obliques se coupent en résolvant $x+y=8$ et $x+2y=12$.""",r"""Chercher des coefficients positifs $a,b$ tels que $a(x+y)+b(x+2y)=3x+4y$."""],
[r"""\editionEtape{1. Construire le domaine}
Les sommets sont $\res{(0;0),(8;0),(4;4),(0;6)}$. Chaque inégalité sélectionne un côté d’une droite ; leur intersection donne le polygone, bords inclus.
\editionEtape{2. Prouver une borne sur toute la région}
On écrit $3x+4y=2(x+y)+(x+2y)$. Avec les deux contraintes, $R\le2\times8+12=\res{28}$. Ce calcul est valable pour tous les points admissibles, pas seulement pour les sommets.
\editionEtape{3. Vérifier l’atteinte}
Pour avoir égalité, il faut $x+y=8$ et $x+2y=12$, d’où $\res{(x;y)=(4;4)}$. Ce point respecte les contraintes de positivité. Le maximum est donc 28 et il est atteint uniquement là.
\editionRetenir{Une combinaison d’inégalités peut prouver un optimum sur une région entière, sans théorème avancé d’optimisation.}"""],
'assert 2*(x+y)+(x+2*y)==3*x+4*y and solve([x+y-8,x+2*y-12],[x,y])=={x:4,y:4} and 3*4+4*4==28','defi-region'),
Defi('Carré et racine, deux courbes liées','Chapitres 5 et 6',
Q(r"""Pour $a\ge0$, montrer que le point $(a;a^2)$ de la courbe carré correspond au point $(a^2;a)$ de la courbe racine.""",r"""Expliquer la symétrie par rapport à $y=x$, en précisant la restriction nécessaire de la courbe carré.""",r"""Déterminer les points d’intersection et comparer $\sqrt x$, $x$ et $x^2$ pour $0<x<1$, puis pour $x>1$."""),
[r"""Échanger l’abscisse et l’ordonnée ; utiliser $\sqrt{a^2}=a$ seulement parce que $a\ge0$.""",r"""Comparer d’abord $x^2$ à $x$, puis appliquer le même raisonnement à la racine."""],
[r"""\editionEtape{1. Échanger les coordonnées}
Pour $a\ge0$, $\sqrt{a^2}=a$. Le point $(a^2;a)$ appartient donc à la courbe racine. Échanger les coordonnées décrit la symétrie par rapport à la droite $y=x$. Il faut restreindre la fonction carré à $[0;+\infty[$ : sa branche négative ne devient pas la courbe de la racine positive.
\editionEtape{2. Trouver les intersections}
$\sqrt x=x^2$ impose $x\ge0$. En élevant au carré, $x=x^4$, donc $x(x^3-1)=0$. La croissance du cube donne $\res{x=0\text{ ou }x=1}$. Les points sont $(0;0)$ et $(1;1)$.
\editionEtape{3. Comparer les trois fonctions}
Pour $0<x<1$, $\res{x^2<x<\sqrt x}$. Pour $x>1$, $\res{\sqrt x<x<x^2}$. Les inégalités sont strictes hors des deux points d’égalité.
\editionRetenir{La symétrie n’est valable qu’après choix de la branche où la fonction carré est inversible.}"""],
'assert solveset(sqrt(x)-x*x,x,domain=S.Reals)==FiniteSet(0,1) and Rational(1,4)<Rational(1,2)<sqrt(Rational(1,2))','defi-racine-carre'),
Defi('Un paramètre et deux extrémums','Chapitres 6 et 7',
r"""Pour $a\in\mathbb R$, on étudie $f_a(x)=(x-a)^2$ sur $[0;4]$."""+Q(r"""Discuter le minimum selon la position de $a$ par rapport à $[0;4]$.""",r"""Déterminer le maximum en comparant les distances aux extrémités.""",r"""Choisir $a$ pour que ce maximum soit le plus petit possible. Donner sa valeur et prouver l’unicité du choix."""),
[r"""Le minimum correspond au point de $[0;4]$ le plus proche de $a$.""",r"""Si les deux extrémités étaient à distance strictement inférieure à 2 de $a$, pourraient-elles rester distantes de 4 ?"""],
[r"""\editionEtape{1. Classer les positions du centre}
Si $a<0$, le plus proche est 0 et le minimum vaut $a^2$. Si $0\le a\le4$, il vaut 0, atteint en $x=a$. Si $a>4$, il vaut $(4-a)^2$, atteint en 4.
\editionEtape{2. Comparer les deux extrémités}
Le maximum est $\max(a^2,(4-a)^2)$. Leur différence vaut $a^2-(4-a)^2=8a-16$. Le premier est plus grand pour $a>2$, le second pour $a<2$, et ils sont égaux pour $a=2$.
\editionEtape{3. Optimiser la pire valeur}
Si $a\le2$, alors $4-a\ge2$, donc le maximum est au moins 4. Si $a\ge2$, alors $a\ge2$, même conclusion. La valeur 4 est atteinte pour $\res{a=2}$ et seulement pour ce choix ; le maximum minimal vaut $\res4$.
\editionRetenir{Un paramètre oblige à distinguer les régimes. Un optimum portant sur une pire valeur se traite encore avec des comparaisons élémentaires.}"""],
'assert expand(x*x-(4-x)**2)==8*x-16 and 2**2==(4-2)**2==4'),
Defi('Optimiser une dispersion','Chapitre 12',
r"""Une série comporte trois valeurs $0,t,6$, où $0\le t\le6$."""+Q(r"""Exprimer la moyenne et la médiane.""",r"""Montrer que la moyenne des carrés des écarts à la moyenne vaut $\dfrac29(t-3)^2+6$.""",r"""Pour quelle valeur de $t$ l’écart type est-il minimal ? Est-ce aussi le choix qui donne une moyenne de 3 ?"""),
[r"""L’ordre des valeurs est connu ; la médiane est donc le terme central $t$.""",r"""Utiliser $\sigma^2=\overline{x^2}-\bar x^2$ puis compléter le carré."""],
[r"""\editionEtape{1. Écrire les indicateurs}
La moyenne est $\bar x=(t+6)/3$ et la médiane est $t$. La moyenne des carrés vaut $(t^2+36)/3$.
\editionEtape{2. Transformer la dispersion}
On calcule $\sigma^2=(t^2+36)/3-(t+6)^2/9=(2t^2-12t+72)/9$, soit
\[\res{\sigma^2=\frac29(t-3)^2+6}.\]
La racine étant croissante, minimiser $\sigma^2$ revient à minimiser $\sigma$.
\editionEtape{3. Conclure avec les conditions}
Le minimum est atteint pour $\res{t=3}$, autorisé par le domaine ; l’écart type vaut alors $\res{\sqrt6}$. L’équation $\bar x=3$ donne aussi $(t+6)/3=3$, donc le même choix.
\editionRetenir{La moyenne, la médiane et l’écart type décrivent des propriétés distinctes. Une forme carrée peut rendre une optimisation statistique accessible.}"""],
'assert simplify((x*x+36)/3-(x+6)**2/9-(Rational(2,9)*(x-3)**2+6))==0 and solve((x+6)/3-3,x)==[3]'),
Defi('Des marges qui ne fixent pas l’intersection','Chapitres 13 et 14',
r"""Dans une population de 100 personnes, 60 pratiquent $A$ et 50 pratiquent $B$. On note $k$ le nombre qui pratiquent les deux."""+Q(r"""Compléter les quatre cases du tableau en fonction de $k$.""",r"""Déterminer toutes les valeurs entières possibles de $k$.""",r"""En déduire l’intervalle possible de la fréquence de $B$ parmi $A$. Les marges suffisent-elles à donner une seule valeur ?"""),
[r"""Les cases sont $k$, $60-k$, $50-k$ et le reste pour arriver à 100.""",r"""Chaque case doit être un entier positif ou nul."""],
[r"""\editionEtape{1. Reconstituer le tableau}
Les quatre cases sont $k$ pour les deux, $60-k$ pour $A$ seul, $50-k$ pour $B$ seul et $k-10$ pour aucun des deux. Leur somme vaut bien 100.
\editionEtape{2. Imposer la faisabilité}
La positivité des cases exige $k\ge10$ et $k\le50$. Toute valeur entière de $\res{10\text{ à }50}$ produit un tableau valide ; ces bornes ne sont pas seulement nécessaires, elles sont réalisables.
\editionEtape{3. Encadrer le conditionnement}
La fréquence cherchée est $k/60$. Elle peut prendre les valeurs discrètes correspondantes entre $\res{1/6\text{ et }5/6}$. Les marges ne permettent donc pas de connaître une unique fréquence conditionnelle.
\editionRetenir{Un tableau n’est pas déterminé par ses seules marges. Vérifier les quatre cases permet aussi de détecter une intersection impossible.}"""],
'assert [k for k in range(101) if min(k,60-k,50-k,k-10)>=0]==list(range(10,51)) and Rational(10,60)==Rational(1,6) and Rational(50,60)==Rational(5,6)'),
Defi('Défauts rares et conditionnement inversé','Chapitres 13 et 14 ; prolongement facultatif',
r"""Un contrôle industriel détecte 90\,\% des défauts et signale à tort 5\,\% des pièces conformes. La proportion de défauts est $p$, avec $0<p<1$. Ce défi prolonge le cours en calculant aussi la proportion globale de signaux positifs."""+Q(r"""Dans une population de taille $N$, exprimer les nombres théoriques de vrais et faux positifs en fonction de $p,N$.""",r"""Montrer que la proportion de défauts parmi les signaux positifs vaut $\dfrac{0{,}9p}{0{,}9p+0{,}05(1-p)}$.""",r"""Pour quelles valeurs de $p$ un signal positif correspond-il à un défaut avec une probabilité d’au moins $1/2$ ? Comparer $p=1\,\%$ et $p=10\,\%$."""),
[r"""Les vrais positifs viennent des $pN$ défauts ; les faux positifs des $(1-p)N$ pièces conformes.""",r"""Le dénominateur est positif. Comparer la fraction à $1/2$ revient à comparer le nombre de vrais positifs à celui de faux positifs."""],
[r"""\editionEtape{1. Organiser les deux origines du signal}
Les vrais positifs sont $0{,}9pN$ ; les faux positifs $0{,}05(1-p)N$. Leur somme donne tous les signaux positifs. Pour un modèle de proportions, ces expressions n’imposent pas que chaque taille arbitraire $N$ donne des effectifs entiers.
\editionEtape{2. Restreindre la référence aux positifs}
Le rapport vrais positifs sur tous les positifs simplifie le facteur $N$ et donne la fraction annoncée.
\editionEtape{3. Établir le seuil}
La fraction est au moins $1/2$ si $0{,}9p\ge0{,}05(1-p)$, soit $0{,}95p\ge0{,}05$. Donc $\res{p\ge1/19\approx5{,}26\,\%}$. Pour $p=1\,\%$, la probabilité inversée vaut $2/13\approx15{,}4\,\%$ ; pour $p=10\,\%$, elle vaut $2/3\approx66{,}7\,\%$.
\editionRetenir{Les performances du contrôle ne suffisent pas à connaître la probabilité inversée : la rareté initiale des défauts intervient aussi.}"""],
'assert solve(Rational(9,10)*x-Rational(5,100)*(1-x),x)==[Rational(1,19)] and Rational(9,10)*Rational(1,100)/(Rational(9,10)*Rational(1,100)+Rational(5,100)*Rational(99,100))==Rational(2,13) and Rational(9,100)/(Rational(9,100)+Rational(45,1000))==Rational(2,3)','defi-test'),
Defi('Trois dés, deux sommes','Chapitres 14 et 15',
r"""On lance trois dés équilibrés indépendants, distingués par leur couleur. Deux personnes pensent que les sommes 9 et 10 ont la même probabilité parce qu’elles se décrivent chacune par six triplets non ordonnés."""+Q(r"""Lister ces six triplets pour chaque somme, avec leurs termes dans l’ordre croissant.""",r"""Compter pour chaque triplet combien d’ordres différents il représente, puis comparer les probabilités.""",r"""Écrire un programme à trois boucles qui vérifie le dénombrement et expliquer le rôle des 216 issues."""),
[r"""Trois nombres distincts donnent six ordres ; deux égaux, trois ordres ; trois égaux, un seul.""",r"""Pour la somme 9, les triplets vont de $(1;2;6)$ à $(3;3;3)$. Pour 10, de $(1;3;6)$ à $(3;3;4)$."""],
[r"""\editionEtape{1. Distinguer les types et les issues}
Pour 9 : $(1,2,6),(1,3,5),(1,4,4),(2,2,5),(2,3,4),(3,3,3)$, avec multiplicités 6, 6, 3, 3, 6, 1 : total 25. Pour 10 : $(1,3,6),(1,4,5),(2,2,6),(2,3,5),(2,4,4),(3,3,4)$, avec 6, 6, 3, 6, 3, 3 : total 27.
\editionEtape{2. Calculer les probabilités}
Les $6^3=216$ triplets ordonnés sont équiprobables. Donc $\res{P(S=9)=25/216}$ et $\res{P(S=10)=27/216=1/8}$. La différence est $\res{1/108}$ en faveur de 10. Les six types non ordonnés n’avaient pas tous la même probabilité.
\editionRetenir{Il faut compter des issues équiprobables, et non des descriptions qui regroupent des nombres différents d’issues.}""",
r"""\editionEtape{3. Vérifier par une énumération exhaustive}
\begin{python}
def effectifs():
    n9, n10 = 0, 0
    for a in range(1, 7):
        for b in range(1, 7):
            for c in range(1, 7):
                s = a + b + c
                if s == 9:
                    n9 += 1
                if s == 10:
                    n10 += 1
    return n9, n10
\end{python}
La fonction renvoie \code{(25, 27)}. Chaque triplet ordonné est visité exactement une fois, car chaque boucle parcourt toutes les valeurs de son dé. Il s’agit d’une énumération exhaustive, pas d’une simulation aléatoire : le dénombrement est donc exact.
\editionRetenir{L’informatique peut servir à prouver un énoncé fini lorsqu’on justifie que tous les cas sont examinés exactement une fois.}"""],
'from itertools import product\nassert [sum(sum(t)==k for t in product(range(1,7),repeat=3)) for k in [9,10]]==[25,27] and Rational(27-25,216)==Rational(1,108)')
]
