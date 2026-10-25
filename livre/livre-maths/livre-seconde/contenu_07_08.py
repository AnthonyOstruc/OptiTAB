from modele import *

chapitre(7,'variations','Variations et optimisation','2 · Fonctions',
 'Croissance · Extrémums · Comparaisons · Recherche numérique',
 ['Lire et construire un tableau de variations.','Démontrer un sens de variation dans des cas simples.','Résoudre un problème d’optimisation sans dérivée.'],
 ['Fonctions de référence et identités remarquables.'],[
r'''\essSection{1}{Décrire les variations}
\begin{definition}Sur un intervalle $I$, $f$ est croissante si pour tous $a,b\in I$ tels que $a<b$, on a $f(a)\le f(b)$. Elle est décroissante si $f(a)\ge f(b)$. Avec des inégalités strictes sur les images, on parle de croissance ou décroissance stricte.\end{definition}
\begin{propriete}Pour $f(x)=mx+p$, $f(b)-f(a)=m(b-a)$. Comme $b-a>0$, le signe de la différence est celui de $m$ : croissance stricte pour $m>0$, décroissance stricte pour $m<0$, fonction constante pour $m=0$.\end{propriete}
\begin{definition}Un maximum est une valeur $M=f(c)$ supérieure ou égale à toutes les images de l’intervalle. Le point $c$ est une abscisse où il est atteint. Un minimum se définit en inversant l’ordre.\end{definition}
\begin{attention}Le signe d’une fonction et ses variations sont deux informations différentes. Une fonction peut être négative et croissante, par exemple $f(x)=x$ sur $[-4;-1]$.\end{attention}
\begin{savoirfaire}[Lire un tableau]Une flèche indique une comparaison d’images sur tout un intervalle. Elle ne donne pas les images des valeurs intermédiaires, sauf information supplémentaire sur la fonction.\end{savoirfaire}
\begin{center}\begin{tableau}
\otTab[2.5]{$x$/0.7,$f(x)$/1.5}{$-2$,$0$,$2$,$4$}
\tkzTabVar{-/$1$,+/$3$,-/$-1$,+/$1$}
\end{tableau}\par\legende{Exemple : la fonction monte de 1 à 3, descend à $-1$, puis remonte à 1.}\end{center}''',
r'''\essSection{2}{Chercher et démontrer un optimum}
\begin{savoirfaire}[Faire apparaître un carré]
Pour $A(x)=x(12-x)$, écrire $A(x)=36-(x-6)^2$. Comme le carré est positif, $A(x)\le36$ ; l’égalité est atteinte pour $x=6$. C’est une démonstration d’un maximum, sans calcul de dérivée.
\end{savoirfaire}
\begin{savoirfaire}[Balayer un intervalle]
Calculer les images d’une grille de valeurs, retenir la meilleure, puis affiner la grille. Le balayage propose un candidat ; sa précision dépend du pas. Il ne constitue pas à lui seul une preuve d’optimum sur tous les réels.
\end{savoirfaire}
\begin{exemple}[Dichotomie autour d’un optimum connu par les variations]
Si $f$ augmente jusqu’à une abscisse $c$ puis diminue, on peut réduire un intervalle contenant $c$ en comparant des images selon une procédure justifiée. Un exemple complet est donné dans le chapitre Python. Ne pas confondre recherche de maximum et recherche d’un zéro.
\end{exemple}
\otIntertitre{Rédiger une conclusion}
Nommer la grandeur optimisée, sa valeur avec l’unité, l’abscisse ou les dimensions correspondantes, et vérifier le domaine. « 36 » seul ne dit pas si l’on parle d’une longueur, d’une aire ou d’une valeur de $x$.'''
],[
E('Une pente, un sens, un signe',Q(r"""Donner les variations de $f(x)=4x-7$, $g(x)=-3x+2$ et $h(x)=5$ sur $\mathbb R$.""",r"""Dresser le tableau de signes de $f$ et de $g$."""),
r"""Le signe du coefficient directeur suffit : 4 est positif, donc $f$ est strictement croissante ; $-3$ est négatif, donc $g$ est strictement décroissante ; $h$ a un coefficient nul, donc elle est constante. Le terme ajouté ne change pas le sens de variation. Pour les signes, $f$ s’annule en $\res{7/4}$ : $f(x)$ est négatif pour $x<7/4$ et positif pour $x>7/4$. La fonction $g$ s’annule en $\res{2/3}$ : $g(x)$ est positif pour $x<2/3$ et négatif pour $x>2/3$. Une fonction affine croissante passe du négatif au positif, une décroissante fait l’inverse ; $h$ reste positive.""",
'Repérer la pente pour les variations, puis la valeur qui annule la fonction pour le signe.','assert 4>0 and -3<0 and (5-5)==0 and solve(4*x-7,x)==[Rational(7,4)] and solve(-3*x+2,x)==[Rational(2,3)] and (4*x-7).subs(x,0)<0<(4*x-7).subs(x,2) and (-3*x+2).subs(x,0)>0>(-3*x+2).subs(x,1)'),
E('Lire une ligne brisée',r"""La courbe passe par $(-2;1)$, $(0;3)$, $(2;-1)$ et $(4;1)$ et est affine entre ces points. Donner les intervalles de variation, le minimum et le maximum.""",
r"""La courbe monte de $-2$ à 0, descend de 0 à 2, puis remonte de 2 à 4. Le maximum est $\res3$, atteint en $\res{x=0}$. Le minimum est $\res{-1}$, atteint en $\res{x=2}$. Les valeurs aux deux autres extrémités valent 1 et ne dépassent pas ces extrémums.""",
'Parcourir la courbe de gauche à droite.','assert max([1,3,-1,1])==3 and min([1,3,-1,1])==-1',figure='fonction-morceaux'),
E('Carré sur un intervalle négatif',r"""Donner les variations de $x^2$ sur $[-5;-1]$ et son image minimale et maximale sur cet intervalle.""",
r"""La fonction carré est décroissante sur les réels négatifs. Sur $[-5;-1]$, elle descend de 25 à 1. Le minimum est $\res1$ en $x=-1$ ; le maximum est $\res{25}$ en $x=-5$. La plus petite abscisse donne ici la plus grande image.""",
'Choisir la bonne branche de la fonction carré.','assert (-5)**2==25 and (-1)**2==1'),
E('Un carré décalé',r"""Pour $f(x)=(x-2)^2+3$, déterminer le minimum sur $\mathbb R$ et l’abscisse où il est atteint.""",
r"""Le carré $(x-2)^2$ est toujours positif ou nul. On en déduit $f(x)\ge3$. L’égalité est possible et exige $x-2=0$. Donc le minimum est $\res3$, atteint uniquement en $\res{x=2}$. Il n’existe pas de maximum sur $\mathbb R$, car le carré peut être arbitrairement grand.""",
'Utiliser la positivité du carré et son cas d’annulation.','assert solve((x-2)**2,x)==[2] and ((x-2)**2+3).subs(x,2)==3'),
E('Comparer sans connaître les images',r"""Une fonction est strictement décroissante sur $[1;8]$. Comparer $f(2)$ et $f(7)$. Peut-on comparer $f(2)$ à 0 avec cette seule information ?""",
r"""Comme $2<7$ et que la fonction décroît strictement, $\res{f(2)>f(7)}$. On ne peut rien conclure sur le signe de $f(2)$. Les fonctions $-x$ et $10-x$ sont toutes deux décroissantes, mais elles donnent en 2 les valeurs $-2$ et 8, de signes opposés.""",
'Séparer comparaison d’images et comparaison à zéro.','assert -2<0 and 10-2>0 and (-2)>(-7)'),
E('Un tableau ne donne pas tout',r"""Une fonction est décrite par le tableau de variations ci-dessous : elle croît de $f(0)=1$ à $f(2)=5$ puis décroît jusqu’à $f(6)=-3$. Encadrer $f(1)$ et $f(4)$. Peut-on déterminer exactement ces deux images ?""",
r"""La croissance donne $\res{1\le f(1)\le5}$. La décroissance sur $[2;6]$ donne $\res{-3\le f(4)\le5}$. Ces valeurs ne sont pas déterminées exactement : la fonction peut suivre de nombreuses courbes entre les extrémités, tout en conservant les mêmes variations. Une interpolation linéaire nécessiterait une hypothèse supplémentaire.""",
'Utiliser uniquement les comparaisons garanties par les flèches.','assert 1<5 and -3<5',figure='variations-lecture'),
E('Prouver la croissance d’une affine',r"""Pour $f(x)=\dfrac32x-4$, démontrer que $f$ est strictement croissante en comparant $f(b)-f(a)$ pour $a<b$.""",
r"""On calcule $f(b)-f(a)=(3b/2-4)-(3a/2-4)=\tfrac32(b-a)$. Or $b-a>0$ et $3/2>0$. La différence est donc strictement positive. Ainsi $f(a)<f(b)$ pour tous $a<b$, ce qui est exactement la définition de la croissance stricte.""",
'Démontrer la monotonie par le signe d’une différence d’images.','assert expand((Rational(3,2)*y-4)-(Rational(3,2)*x-4))==Rational(3,2)*(y-x)'),
E('Une symétrie utile',r"""Pour $f(x)=(x-3)^2-2$ sur $[0;7]$, donner les variations et les extrémums.""",
r"""La distance de $x$ à 3 diminue jusqu’à 3 puis augmente. Le carré suit ces variations : $f$ décroît sur $[0;3]$ et croît sur $[3;7]$. Le minimum est $\res{-2}$ en 3. Aux bornes, $f(0)=7$ et $f(7)=14$ ; le maximum sur l’intervalle est donc $\res{14}$ en 7.""",
'Repérer le centre du carré puis comparer les deux extrémités.','assert [(a-3)**2-2 for a in [0,3,7]]==[7,-2,14]',figure='variation-decalee'),
E('Maximum d’un produit',r"""Pour $x\in[0;10]$, montrer que $A(x)=x(10-x)$ ne dépasse pas 25. Quand vaut-il 25 ?""",
r"""On complète le carré : $A(x)=10x-x^2=25-(x-5)^2$. Le carré est positif ou nul, donc $A(x)\le25$. L’égalité se produit seulement en $x=5$, qui appartient au domaine. Ainsi $\res{\max A=25}$, atteint en $\res5$.""",
'Faire apparaître un nombre fixe moins un carré.','assert expand(25-(x-5)**2)==expand(x*(10-x)) and solve((x-5)**2,x)==[5]',figure='aire-produit'),
E('Un balayage et sa limite',r"""Pour $f(x)=4-(x-1{,}3)^2$ sur $[0;3]$, on teste seulement les entiers 0, 1, 2 et 3. Quel maximum trouve-t-on sur cette grille ? Est-ce le maximum réel ?""",
r"""Les images sont 2,31 ; 3,91 ; 3,51 ; 1,11. La grille donne $\res{3{,}91}$ en 1. Mais l’expression montre que le vrai maximum est $\res4$ en $x=1{,}3$. La meilleure valeur d’une grille est seulement un maximum parmi les points testés ; le pas peut manquer l’optimum réel.""",
'Distinguer optimisation discrète et optimisation sur un intervalle.','assert [4-(Rational(a)-Rational(13,10))**2 for a in range(4)]==[Rational(231,100),Rational(391,100),Rational(351,100),Rational(111,100)]'),
E('Un enclos contre un mur',r"""On dispose de 24 m de clôture pour trois côtés d’un rectangle appuyé contre un mur. Si $x$ est la largeur perpendiculaire au mur, exprimer l’aire et trouver ses dimensions maximales.""",
r"""Les deux largeurs utilisent $2x$ mètres ; la longueur vaut $24-2x$. Le domaine est $0<x<12$. L’aire vaut $A(x)=x(24-2x)=72-2(x-6)^2$. Elle ne dépasse pas $\res{72\text{ m}^2}$, atteints pour $\res{x=6\text{ m}}$ et une longueur de $\res{12\text{ m}}$. Ces dimensions utilisent bien $6+12+6=24$ m de clôture.""",
'Écrire la contrainte de périmètre avant la fonction d’aire.','assert expand(72-2*(x-6)**2)==expand(x*(24-2*x)) and 6*(24-12)==72',figure='enclos'),
E('La recette d’une vente',r"""Un modèle prévoit $100-5p$ objets vendus au prix $p$ euros, pour $0\le p\le20$. Exprimer la recette et déterminer son maximum dans ce modèle.""",
r"""La recette est prix fois quantité : $R(p)=p(100-5p)=500-5(p-10)^2$. Le maximum est donc $\res{500\text{ euros}}$, obtenu pour $\res{p=10\text{ euros}}$. Le modèle prévoit alors 50 ventes. Le résultat dépend de l’hypothèse de demande donnée ; ce calcul ne suffit pas à valider le modèle dans une situation réelle.""",
'Modéliser le produit puis établir un majorant atteint.','assert expand(500-5*(x-10)**2)==expand(x*(100-5*x))'),
E('Un minimum de distance au carré',r"""Pour $M(x;0)$ et $A(2;3)$, exprimer $AM^2$ et déterminer la position de $M$ qui rend $AM$ minimale.""",
r"""La formule de distance donne $AM^2=(x-2)^2+9\ge9$. L’égalité est atteinte seulement pour $x=2$. La racine carrée étant croissante sur les positifs, minimiser $AM^2$ revient à minimiser $AM$. Le point cherché est $\res{M(2;0)}$, et la distance minimale vaut $\res3$.""",
'Optimiser le carré de la distance pour éviter la racine.','assert ((x-2)**2+9).subs(x,2)==9 and solve((x-2)**2,x)==[2]',figure='distance-minimale'),
E('Un maximum sur un domaine restreint',r"""La fonction $f(x)=9-(x-4)^2$ est étudiée sur $[0;2]$. Un élève répond que son maximum est 9. Corriger sa démarche et donner les bons extrémums.""",
r"""La valeur 9 serait atteinte en 4, mais 4 n’appartient pas au domaine. Sur $[0;2]$, la distance à 4 diminue : $f$ est croissante. On calcule $f(0)=-7$ et $f(2)=5$. Le minimum est $\res{-7}$ en 0 et le maximum $\res5$ en 2. Un majorant non atteint n’est pas le maximum recherché.""",
'Vérifier l’appartenance du candidat au domaine.','assert [9-(a-4)**2 for a in [0,2,4]]==[-7,5,9]'),
E('Une garantie pour toutes les valeurs',r"""Pour quel plus petit réel $k$ l’inégalité $x(8-x)\le k$ est-elle vraie pour tout $x\in[0;8]$ ? Prouver que toute valeur plus petite échoue.""",
r"""On écrit $x(8-x)=16-(x-4)^2\le16$. La valeur $k=16$ convient donc pour toutes les abscisses. Si $k<16$, le choix $x=4$ donne $x(8-x)=16>k$, et l’inégalité échoue. Le plus petit majorant demandé est ainsi $\res{k=16}$. On a prouvé à la fois qu’il convient et qu’on ne peut l’abaisser.""",
'Démontrer une borne uniforme puis exhiber une valeur qui l’atteint.','assert expand(16-(x-4)**2)==expand(x*(8-x)) and 4*(8-4)==16')
],reperes=['Monotonie et extrémums','Variations des affines','Optimisation sans dérivée','Balayage et preuve algébrique'])

chapitre(8,'vecteurs','Vecteurs du plan','3 · Géométrie',
 'Translations · Coordonnées · Sommes · Déterminants',
 ['Calculer et représenter les coordonnées d’un vecteur.','Utiliser Chasles et les opérations vectorielles.','Démontrer alignement et parallélisme par un déterminant.'],
 ['Repérage du plan et calcul avec les nombres relatifs.'],[
r'''\essSection{1}{Déplacements et coordonnées}
\begin{definition}Le vecteur $\vect{AB}$, appelé vecteur déplacement de $A$ à $B$, décrit la translation qui envoie $A$ sur $B$. Deux vecteurs égaux ont même direction, même sens et même longueur : $\vect{AB}=\vect{CD}$ signifie que $ABDC$ est un parallélogramme, éventuellement aplati. Toutes les flèches $\vect{AB},\vect{CD},\ldots$ qui représentent un même vecteur $\vec u$ en sont des représentants. Le vecteur nul $\vec0=\vect{AA}$ correspond à un déplacement nul. Si $O$ est l’origine, $\vect{OM}$ est le vecteur position de $M$. Dans un repère orthonormé $(O;\vec i,\vec j)$, la base $(\vec i,\vec j)$ est orthonormée et :
\[\vect{AB}=(x_B-x_A\,;\,y_B-y_A),\qquad\|\vec u\|=\sqrt{u_x^2+u_y^2}.\]
\end{definition}
\begin{propriete}La relation de Chasles est $\vect{AB}+\vect{BC}=\vect{AC}$. Si $\vec u=(a;b)$ et $\vec v=(c;d)$, alors $\vec u+\vec v=(a+c;b+d)$ et $k\vec u=(ka;kb)$.\end{propriete}
\begin{savoirfaire}[Construire une somme]À partir d’une même origine, construire le parallélogramme porté par les deux vecteurs : sa diagonale représente leur somme. On peut aussi reporter le second vecteur à l’extrémité du premier.\end{savoirfaire}
\begin{attention}Les coordonnées d’un point décrivent sa position ; celles d’un vecteur décrivent un déplacement. $\vect{AB}$ et $\vect{BA}$ sont opposés.\end{attention}''',
r'''\essSection{2}{Colinéarité et choix d’une méthode}
\begin{definition}Deux vecteurs sont colinéaires si l’un est un multiple de l’autre, ou si l’un est nul. Pour $\vec u=(a;b)$ et $\vec v=(c;d)$, leur déterminant est $\det(\vec u,\vec v)=ad-bc$.\end{definition}
\begin{theoreme}Deux vecteurs du plan sont colinéaires si et seulement si leur déterminant est nul. Des points $A,B,C$ sont alignés si et seulement si $\det(\vect{AB},\vect{AC})=0$. Pour deux droites, choisir des vecteurs directeurs non nuls.\end{theoreme}
\begin{propriete}Un point $I$ est le milieu de $[AB]$ si et seulement si $\vect{AI}=\vect{IB}$, ou encore $\vect{IA}+\vect{IB}=\vec0$.\end{propriete}
\begin{savoirfaire}[Dans une base]Si $\vec i=(1;0)$ et $\vec j=(0;1)$, $\vec u=(a;b)$ s’écrit $a\vec i+b\vec j$. Plus généralement, deux vecteurs non colinéaires permettent de décomposer tous les vecteurs du plan.\end{savoirfaire}
\otIntertitre{En physique}
Le vecteur déplacement s’additionne comme les déplacements successifs ; une durée ou une masse s’additionne comme un nombre. Préciser si une donnée est une grandeur vectorielle ou scalaire évite de confondre sens et longueur.'''
],[
E('Calculer un déplacement',r"""On donne $A(1;2)$ et $B(5;-1)$. Calculer $\vect{AB}$ et $\vect{BA}$.""",
r"""On soustrait les coordonnées de l’origine à celles de l’extrémité : $\vect{AB}=(5-1;-1-2)=\res{(4;-3)}$. Dans l’autre sens, $\vect{BA}=\res{(-4;3)}=-\vect{AB}$. Les deux flèches ont la même longueur mais des sens opposés.""",
'Effectuer arrivée moins départ dans le bon ordre.','assert (5-1,-1-2)==(4,-3) and (1-5,2+1)==(-4,3)',figure='vect-01'),
E('Additionner des vecteurs',r"""Pour $\vec u=(3;1)$ et $\vec v=(-1;2)$, calculer et construire $\vec u+\vec v$.""",
r"""Les coordonnées s’additionnent séparément : $\vec u+\vec v=(3-1;1+2)=\res{(2;3)}$. Sur le schéma, partir de l’origine, suivre $\vec u$, puis reporter $\vec v$ sans le tourner. L’arrivée est le point $(2;3)$ ; la flèche directe représente la somme.""",
'Additionner les déplacements composante par composante.','assert (3-1,1+2)==(2,3)',figure='vect-02'),
E('Multiplier par un réel',r"""Pour $\vec u=(2;-1)$, calculer $3\vec u$ et $-2\vec u$. Décrire leur sens par rapport à celui de $\vec u$.""",
r"""On multiplie chaque coordonnée : $3\vec u=\res{(6;-3)}$, de même sens que $\vec u$ et trois fois plus long. $-2\vec u=\res{(-4;2)}$ a le sens opposé et une norme double. Dans les deux cas, les vecteurs restent colinéaires à $\vec u$.""",
'Interpréter séparément le signe du coefficient et sa valeur absolue.','assert (3*2,3*-1)==(6,-3) and (-2*2,-2*-1)==(-4,2)',figure='vect-03'),
E('Construire une image par translation',r"""L’image de $A(-2;1)$ par la translation de vecteur $(4;2)$ est $B$. Déterminer ses coordonnées.""",
r"""La translation impose $\vect{AB}=(4;2)$. Il faut donc $x_B=-2+4$ et $y_B=1+2$, soit $\res{B(2;3)}$. Vérification : $\vect{AB}=(2-(-2);3-1)=(4;2)$. Ajouter le vecteur ne consiste pas à multiplier les coordonnées du point.""",
'Ajouter le déplacement aux coordonnées du point de départ.','assert (-2+4,1+2)==(2,3)',figure='vect-04'),
E('Une norme',r"""Calculer la norme de $\vec u=(-3;4)$, puis celle de $2\vec u$.""",
r"""Par Pythagore, $\|\vec u\|=\sqrt{(-3)^2+4^2}=\sqrt{25}=\res5$. Le vecteur double vaut $(-6;8)$ et sa norme vaut $\sqrt{36+64}=\res{10}$. On retrouve $\|2\vec u\|=2\|\vec u\|$. Les coordonnées peuvent être négatives, la norme ne l’est pas.""",
'Utiliser la formule de norme dans un repère orthonormé.','assert sqrt((-3)**2+4**2)==5 and sqrt((-6)**2+8**2)==10',figure='vect-05'),
E('La relation de Chasles',r"""Simplifier $\vect{AB}+\vect{BC}+\vect{CD}$, puis $\vect{AB}+\vect{CA}$.""",
r"""Les déplacements successifs de $A$ à $B$, de $B$ à $C$ puis de $C$ à $D$ se regroupent en $\res{\vect{AD}}$. Dans la deuxième somme, on peut permuter les termes : $\vect{CA}+\vect{AB}=\res{\vect{CB}}$. L’ordre d’écriture des lettres doit correspondre à un chemin continu.""",
'Réorganiser la somme pour suivre les déplacements.','assert Matrix([2,1])+Matrix([1,2])+Matrix([-2,1])==Matrix([1,4])',figure='vect-06'),
E('Tester la colinéarité',r"""Les vecteurs $(2;3)$ et $(6;9)$ sont-ils colinéaires ? Même question pour $(2;3)$ et $(4;7)$.""",
r"""Le premier déterminant vaut $2\times9-3\times6=0$ ; les vecteurs sont colinéaires, et le second est trois fois le premier. Le second déterminant vaut $2\times7-3\times4=\res2\ne0$ ; ces deux vecteurs ne sont pas colinéaires. Des coordonnées « presque proportionnelles » ne suffisent pas.""",
'Calculer un déterminant exact plutôt qu’apprécier la pente à l’œil.','assert det(Matrix([[2,6],[3,9]]))==0 and det(Matrix([[2,4],[3,7]]))==2',figure='vect-07'),
E('Trois points alignés ?',r"""On donne $A(1;1)$, $B(3;4)$ et $C(5;7)$. Démontrer leur alignement et préciser la position de $B$.""",
r"""$\vect{AB}=(2;3)$ et $\vect{AC}=(4;6)=2\vect{AB}$ : les vecteurs sont colinéaires, donc les trois points sont alignés. De plus $\vect{BC}=(2;3)=\vect{AB}$, ce qui montre que $\res{B\text{ est le milieu de }[AC]}$. Le coefficient 2 donne ici davantage que le simple alignement.""",
'Comparer les vecteurs de même origine, puis leurs longueurs orientées.','assert Matrix([4,6])==2*Matrix([2,3]) and (3-1,4-1)==(5-3,7-4)',figure='vect-08'),
E('Le quatrième sommet',r"""$A(0;1)$, $B(4;2)$ et $C(5;5)$ sont trois sommets consécutifs d’un parallélogramme $ABCD$. Déterminer $D$.""",
r"""Dans un parallélogramme, $\vect{AD}=\vect{BC}$. Or $\vect{BC}=(1;3)$ ; donc $D=A+(1;3)=\res{(1;4)}$. On peut contrôler avec $\vect{DC}=(4;1)=\vect{AB}$. L’ordre $A,B,C,D$ est nécessaire pour choisir la bonne égalité vectorielle.""",
'Choisir l’égalité de côtés opposés correspondant à l’ordre des sommets.','assert (0+5-4,1+5-2)==(1,4)',figure='vect-09'),
E('Une combinaison',r"""Pour $\vec u=(2;1)$ et $\vec v=(-1;3)$, calculer $2\vec u-\vec v$ puis exprimer $(5;-1)$ avec ces vecteurs.""",
r"""On calcule $2\vec u-\vec v=(4;2)-(-1;3)=\res{(5;-1)}$. L’expression cherchée est donc précisément $\res{2\vec u-\vec v}$. La soustraction d’un vecteur signifie ajouter son opposé ; les deux signes de ses coordonnées changent.""",
'Calculer d’abord les multiples, puis effectuer la soustraction.','assert 2*Matrix([2,1])-Matrix([-1,3])==Matrix([5,-1])',figure='vect-10'),
E('Un paramètre de colinéarité',r"""Pour quelle valeur de $m$ les vecteurs $(m;2)$ et $(3;m-1)$ sont-ils colinéaires ? Factoriser l’équation obtenue.""",
r"""Le déterminant est $m(m-1)-6=m^2-m-6=(m-3)(m+2)$. Il est nul exactement pour $\res{m=3\text{ ou }m=-2}$. Le premier vecteur n’est jamais nul puisque sa deuxième coordonnée est 2 ; le critère s’applique sans ambiguïté. On contrôle les deux couples obtenus par proportionnalité.""",
'Traduire la condition géométrique en une équation factorisable.','assert solveset(x*(x-1)-6,x,domain=S.Reals)==FiniteSet(-2,3)',figure='vect-11'),
E('Un point sur une droite',r"""$A(1;2)$, $B(5;4)$ et $M(t;5)$. Déterminer $t$ pour que $A,B,M$ soient alignés.""",
r"""$\vect{AB}=(4;2)$ et $\vect{AM}=(t-1;3)$. Le déterminant vaut $4\times3-2(t-1)=14-2t$. L’alignement équivaut à $14-2t=0$, d’où $\res{t=7}$. Le point $M(7;5)$ est sur le prolongement de $[AB]$, ce qui est permis : alignement ne signifie pas appartenance au segment.""",
'Utiliser le déterminant sans imposer à tort l’appartenance au segment.','assert solve(4*3-2*(x-1),x)==[7]',figure='vect-12'),
E('Une base non usuelle',r"""On donne $\vec u=(1;1)$ et $\vec v=(1;-1)$. Vérifier qu’ils ne sont pas colinéaires, puis exprimer $\vec w=(4;2)$ comme $a\vec u+b\vec v$.""",
r"""Le déterminant vaut $-1-1=-2\ne0$. Pour la décomposition, il faut $a+b=4$ et $a-b=2$. En ajoutant les équations, $2a=6$ ; ainsi $a=3$ et $b=1$. Donc $\res{\vec w=3\vec u+\vec v}$. La non-colinéarité garantit l’unicité de cette décomposition.""",
'Traduire une combinaison vectorielle par deux équations de coordonnées.','assert Matrix([[1,1],[1,-1]]).det()==-2 and 3*Matrix([1,1])+Matrix([1,-1])==Matrix([4,2])',figure='vect-13'),
E('Les milieux d’un triangle',r"""$A(0;0)$, $B(6;2)$ et $C(2;6)$. On donne $I(3;1)$, milieu de $[AB]$, et $J(1;3)$, milieu de $[AC]$. Montrer vectoriellement que $(IJ)$ est parallèle à $(BC)$.""",
r"""$\vect{IJ}=(-2;2)$ et $\vect{BC}=(-4;4)$. On a $\vect{IJ}=\tfrac12\vect{BC}$ ; les vecteurs sont non nuls et colinéaires. Les droites $(IJ)$ et $(BC)$ sont donc parallèles. La même égalité donne $IJ=BC/2$, ce qui retrouve le théorème des milieux.""",
'Comparer deux vecteurs directeurs des droites visées.','assert Matrix([-2,2])==Rational(1,2)*Matrix([-4,4])',figure='vect-14'),
E('Un déplacement composé',r"""Un robot part de $A(1;1)$ et effectue $n$ déplacements $(2;1)$ puis $n-1$ déplacements $(-1;2)$, avec $n\ge1$ entier. Donner l’arrivée $M_n$. Peut-il atteindre $(8;8)$ ?""",
r"""Le déplacement total est $n(2;1)+(n-1)(-1;2)=(n+1;3n-2)$. Après ajout du point de départ, $\res{M_n(n+2;3n-1)}$. Pour atteindre $(8;8)$, l’abscisse impose $n=6$, mais l’ordonnée vaudrait 17. Il n’existe donc aucun entier $n$ convenable. Les deux coordonnées doivent correspondre au même $n$.""",
'Additionner les déplacements puis tester simultanément les deux coordonnées.','assert 6+2==8 and 3*6-1==17 and all((n+2,3*n-1)!=(8,8) for n in range(1,30))',figure='vect-15')
],reperes=['Coordonnées, norme et opérations vectorielles','Relation de Chasles et milieu','Déterminant et colinéarité','Décomposition dans une base'],deco='vecteursplan')
