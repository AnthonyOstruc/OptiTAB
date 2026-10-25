from dataclasses import dataclass
from modele import Q,tableau

@dataclass
class Probleme:
    titre:str
    enonce:str
    corrige:str
    controle:str
    figure:str=''

@dataclass
class Bilan:
    lettre:str
    titre:str
    automatismes:list
    problemes:list

BILANS=[
Bilan('A','Fonctions, géométrie et conditionnement',[
(r"""Calculer $3/4-1/6$.""",r"""$9/12-2/12=\res{7/12}$.""",'assert Rational(3,4)-Rational(1,6)==Rational(7,12)'),
(r"""Simplifier $\sqrt{75}$.""",r"""$\sqrt{25\times3}=\res{5\sqrt3}$.""",'assert sqrt(75)==5*sqrt(3)'),
(r"""Développer $(x-4)^2$.""",r"""$\res{x^2-8x+16}$. Le double produit vaut $-8x$.""",'assert expand((x-4)**2)==x*x-8*x+16'),
(r"""Résoudre $-2x\le6$.""",r"""La division négative renverse l’ordre : $\res{x\ge-3}$.""",'assert solve_univariate_inequality(-2*x<=6,x,relational=False)==Interval(-3,oo)'),
(r"""Écrire $|x-1|\le2$ sous forme d’intervalle.""",r"""Centre 1, rayon 2 : $\res{[-1;3]}$.""",'assert solve_univariate_inequality(Abs(x-1)<=2,x,relational=False)==Interval(-1,3)'),
(r"""Calculer l’image de $-2$ par $f(x)=3x+1$.""",r"""$f(-2)=-6+1=\res{-5}$.""",'assert 3*(-2)+1==-5'),
(r"""Donner le domaine de $1/(x+5)$.""",r"""Le dénominateur ne doit pas s’annuler : $\res{\mathbb R\setminus\{-5\}}$.""",'assert solve(x+5,x)==[-5]'),
(r"""Donner le milieu de $A(0;2)$ et $B(6;4)$.""",r"""Les moyennes de coordonnées donnent $\res{(3;3)}$.""",'assert ((0+6)/2,(2+4)/2)==(3,3)'),
(r"""Une hausse de 10\,\% a quel coefficient multiplicateur ?""",r"""$1+0{,}10=\res{1{,}10}$.""",'assert 1+Rational(1,10)==Rational(11,10)'),
(r"""Pour $P(A)=0{,}35$, calculer $P(\overline A)$.""",r"""$1-0{,}35=\res{0{,}65}$.""",'assert 1-Rational(35,100)==Rational(65,100)')
],[
Probleme('L’aire d’un rectangle',r"""On étudie $f(x)=x(6-x)$ sur $[0;6]$. Pour $0<x<6$, cette fonction est l’aire d’un rectangle de côtés $x$ et $6-x$, en centimètres."""+Q(r"""(1 point) Calculer $f(0)$, $f(2)$ et $f(6)$.""",r"""(1 point) Montrer $f(x)=9-(x-3)^2$.""",r"""(1 point) Donner les variations et le maximum sur $[0;6]$.""",r"""(1 point) Résoudre $f(x)\ge8$.""",r"""(1 point) Conclure sur les dimensions et l’aire maximale du rectangle ; préciser son périmètre."""),
r"""\editionEtape{1. Calculer et changer de forme}
$f(0)=0$, $f(2)=8$ et $f(6)=0$. Le développement de $9-(x-3)^2$ donne $6x-x^2=x(6-x)$.
\editionEtape{2. Exploiter un carré}
La fonction croît de 0 à 3 puis décroît de 3 à 6. Son maximum est $\res9$, atteint en $\res{x=3}$.
\editionEtape{3. Résoudre un seuil}
$9-(x-3)^2\ge8$ équivaut à $(x-3)^2\le1$, donc $\res{x\in[2;4]}$.
\editionEtape{4. Interpréter}
Le rectangle optimal est un carré de côté $\res{3\text{ cm}}$, d’aire $\res{9\text{ cm}^2}$ et de périmètre $\res{12\text{ cm}}$. Les valeurs 0 et 6 décrivaient des rectangles aplatis ; le maximum appartient bien au domaine des rectangles non dégénérés.
\editionRetenir{Le contexte ne dispense pas d’étudier le domaine : les bornes d’un modèle peuvent représenter des situations limites.}""",
'assert expand(9-(x-3)**2)==expand(x*(6-x)) and solve_univariate_inequality(x*(6-x)>=8,x,relational=False)==Interval(2,4)','bilan-A-aire'),
Probleme('Deux médianes se rencontrent',r"""Dans un repère orthonormé, $A(0;0)$, $B(8;0)$ et $C(2;6)$. On note $I$ le milieu de $[BC]$ et $J$ celui de $[AC]$."""+Q(r"""(1 point) Calculer $I$ et $J$.""",r"""(1 point) Donner une équation de $(AI)$.""",r"""(1 point) Donner une équation de $(BJ)$.""",r"""(1 point) Déterminer leur intersection $G$.""",r"""(1 point) Montrer que $\vect{AG}=\dfrac23\vect{AI}$ et expliquer ce que cette égalité apporte."""),
r"""\editionEtape{1. Construire les milieux}
Les formules donnent $\res{I(5;3)}$ et $\res{J(1;3)}$.
\editionEtape{2. Déterminer les droites}
$(AI)$ a pour pente $3/5$ et passe par l’origine : $y=3x/5$. $(BJ)$ a pour pente $3/(1-8)=-3/7$ et passe par $B$ : $y=-3x/7+24/7$.
\editionEtape{3. Résoudre le système}
$3x/5=-3x/7+24/7$ donne $36x=120$, soit $x=10/3$, puis $y=2$. Donc $\res{G(10/3;2)}$.
\editionEtape{4. Contrôler la position}
$\vect{AG}=(10/3;2)=\tfrac23(5;3)=\tfrac23\vect{AI}$. Le point est sur la médiane et aux deux tiers de son trajet depuis $A$. Le résultat concorde avec le défi sur le point de concours des médianes.
\editionRetenir{Une équation de droite se vérifie sur deux points ; une intersection se vérifie dans les deux équations.}""",
'assert solve([y-Rational(3,5)*x,y+Rational(3,7)*x-Rational(24,7)],[x,y])=={x:Rational(10,3),y:2} and Rational(2,3)*Matrix([5,3])==Matrix([Rational(10,3),2])','bilan-A-geometrie'),
Probleme('Une enquête et son arbre',r"""Une enquête construite pour ce bilan porte sur 200 personnes. Le groupe $A$ en compte 80, dont 48 utilisent le service $S$. Le groupe $B$ en compte 120, dont 36 utilisent $S$. On choisit uniformément une personne."""+Q(r"""(1 point) Dresser le tableau complet $A,B$ / $S,\overline S$.""",r"""(1 point) Calculer la fréquence globale de $S$.""",r"""(1 point) Calculer $P_A(S)$ et $P_B(S)$.""",r"""(1 point) Compléter l’arbre et calculer le chemin $A$ puis $S$.""",r"""(1 point) Calculer la part de $A$ parmi les utilisateurs et expliquer pourquoi elle ne vaut pas $P_A(S)$."""),
r"""\editionEtape{1. Reconstituer les cases}
Les effectifs des lignes sont $(48;32;80)$ et $(36;84;120)$. Les colonnes donnent $\res{84\text{ utilisateurs et }116\text{ non-utilisateurs}}$.
\editionEtape{2. Choisir les références}
La fréquence globale est $84/200=\res{0{,}42}$. Les conditionnements valent $P_A(S)=48/80=\res{0{,}6}$ et $P_B(S)=36/120=\res{0{,}3}$.
\editionEtape{3. Relier tableau et chemin}
$P(A)=80/200=0{,}4$ ; le chemin $A$ puis $S$ vaut $0{,}4\times0{,}6=\res{0{,}24}$, comme $48/200$.
\editionEtape{4. Inverser le conditionnement}
Parmi les 84 utilisateurs, 48 sont de $A$, donc $\res{P_S(A)=4/7\approx57{,}1\,\%}$. Le dénominateur 84 diffère du dénominateur 80 de $P_A(S)$.
\editionRetenir{Le tableau donne les effectifs ; l’arbre donne les probabilités de chemins. Les deux représentations doivent rester cohérentes.}""",
'assert Rational(84,200)==Rational(42,100) and Rational(48,80)==Rational(6,10) and Rational(36,120)==Rational(3,10) and Rational(48,84)==Rational(4,7)','bilan-A-arbre')
]),
Bilan('B','Statistiques, configurations et tirages',[
(r"""Rendre $42/63$ irréductible.""",r"""Diviser par 21 : $\res{2/3}$.""",'assert Rational(42,63)==Rational(2,3)'),
(r"""Calculer $2^3\times2^{-5}$.""",r"""$2^{-2}=\res{1/4}$.""",'assert Rational(2)**3*Rational(2)**-5==Rational(1,4)'),
(r"""Factoriser $x^2-9$.""",r"""Différence de carrés : $\res{(x-3)(x+3)}$.""",'assert expand((x-3)*(x+3))==x*x-9'),
(r"""Résoudre $(x-2)(x+1)=0$.""",r"""Un facteur doit s’annuler : $\res{S=\{-1;2\}}$.""",'assert solveset((x-2)*(x+1),x,domain=S.Reals)==FiniteSet(-1,2)'),
(r"""Résoudre $\sqrt x=3$.""",r"""Les membres sont positifs : $\res{x=9}$.""",'assert sqrt(9)==3'),
(r"""Donner la pente de $y=-3x+4$.""",r"""Le coefficient de $x$ est la pente : $\res{-3}$.""",'assert -3<0'),
(r"""Calculer $\det((2;1);(4;3))$.""",r"""$2\times3-1\times4=\res2$.""",'assert 2*3-1*4==2'),
(r"""Une hausse de 25\,\% suivie d’une baisse de 20\,\% donne quel taux global ?""",r"""$1{,}25\times0{,}80=1$ : taux global $\res{0\,\%}$.""",'assert Rational(125,100)*Rational(80,100)==1'),
(r"""Donner la médiane de $1,3,5,9,12$.""",r"""La troisième valeur est $\res5$.""",'assert sorted([1,3,5,9,12])[2]==5'),
(r"""Combien de valeurs parcourt \code{range(2,7)} ?""",r"""2, 3, 4, 5 et 6 : $\res5$ valeurs.""",'assert len(range(2,7))==5')
],[
Probleme('Des durées regroupées',r"""Des durées en minutes sont regroupées en classes."""+tableau(['Classe','$[0;10[$','$[10;20[$','$[20;30]$'],[['Effectif','4','8','8']])+Q(r"""(1 point) Donner l’effectif total et les fréquences cumulées aux bornes 10, 20 et 30.""",r"""(1 point) Estimer la moyenne par les centres, en précisant l’hypothèse.""",r"""(1 point) Déterminer la classe médiane et estimer la médiane sous l’hypothèse uniforme.""",r"""(1 point) Les moyennes réelles de classe sont 6, 14 et 27. Calculer la moyenne exacte.""",r"""(1 point) On ajoute à cette dernière série une durée de 60 minutes. Calculer la nouvelle moyenne et commenter."""),
r"""\editionEtape{1. Cumuler}
$N=20$ ; les cumuls sont 4, 12 et 20, soit $\res{20\,\%,60\,\%,100\,\%}$.
\editionEtape{2. Estimer avec des hypothèses}
Les centres sont 5, 15 et 25 : la moyenne estimée vaut $(20+120+200)/20=\res{17\text{ min}}$. Elle serait exacte sous répartition uniforme dans les classes. La classe médiane est $[10;20[$ ; l’interpolation donne $10+(10-4)\times10/8=\res{17{,}5\text{ min}}$.
\editionEtape{3. Utiliser l’information exacte}
Avec les moyennes réelles, la somme vaut $4\times6+8\times14+8\times27=352$. La moyenne exacte est $\res{17{,}6\text{ min}}$.
\editionEtape{4. Ajouter une observation}
La nouvelle moyenne vaut $(352+60)/21=\res{412/21\approx19{,}6\text{ min}}$. La durée ajoutée est supérieure à l’ancienne moyenne, elle l’augmente. L’effectif est maintenant 21.
\editionRetenir{L’estimation par classes doit être remplacée par le calcul exact quand les moyennes de classes sont disponibles.}""",
'assert Rational(4*5+8*15+8*25,20)==17 and 10+Rational(6,8)*10==Rational(35,2) and 4*6+8*14+8*27==352 and Rational(352,20)==Rational(88,5)','bilan-B-stats'),
Probleme('Un rectangle et son cercle',r"""On donne $A(1;1)$, $B(5;1)$, $C(1;4)$ et $D(5;4)$ dans un repère orthonormé."""+Q(r"""(1 point) Montrer que le quadrilatère $ABDC$ est un rectangle et calculer son aire.""",r"""(1 point) Calculer le milieu $O$ de $[BC]$.""",r"""(1 point) Calculer $OA$, $OB$, $OC$ et $OD$.""",r"""(1 point) Donner le centre et le rayon du cercle passant par les quatre points.""",r"""(1 point) Donner des équations des deux médiatrices de $[AB]$ et $[AC]$ et vérifier leur intersection."""),
r"""\editionEtape{1. Lire les directions}
$AB$ et $CD$ sont horizontaux, $AC$ et $BD$ verticaux. Les côtés consécutifs sont perpendiculaires : $ABDC$ est un rectangle de côtés 4 et 3, d’aire $\res{12}$.
\editionEtape{2. Calculer le centre}
Le milieu de $[BC]$ est $\res{O(3;5/2)}$. Pour chacun des quatre sommets, les écarts de coordonnées ont pour valeurs absolues 2 et $3/2$. Le carré de chaque distance à $O$ vaut $4+9/4=25/4$, donc la distance vaut $\res{5/2}$.
\editionEtape{3. Justifier le cercle}
Les quatre points sont donc sur le cercle de centre $O$ et rayon $\res{2{,}5}$. Les médiatrices de $[AB]$ et $[AC]$ sont $\res{x=3}$ et $\res{y=5/2}$ ; elles se coupent bien en $O$.
\editionRetenir{L’ordre des sommets du rectangle est indiqué : $A,B,D,C$. Un ordre mal choisi peut transformer un quadrilatère simple en un tracé croisé.}""",
'assert [(Rational(a)-3)**2+(Rational(b)-Rational(5,2))**2 for a,b in [(1,1),(5,1),(1,4),(5,4)]]==[Rational(25,4)]*4 and 4*3==12','bilan-B-geometrie'),
Probleme('Une urne sans remise',r"""Une urne contient quatre boules rouges et une bleue. On tire deux boules successivement, sans remise, chaque boule restante ayant la même chance d’être choisie. On note $R_1$ et $B_1$ les couleurs du premier tirage, $R_2$ et $B_2$ celles du second."""+Q(r"""(1 point) Donner les probabilités du premier tirage.""",r"""(1 point) Compléter les branches du second tirage, y compris le chemin impossible.""",r"""(1 point) Calculer $P(R_1\cap R_2)$.""",r"""(1 point) Calculer $P(R_1\cap B_2)$ et $P(B_1\cap R_2)$.""",r"""(1 point) On sait que la seconde boule est bleue. Que peut-on affirmer de la première ? Donner la probabilité conditionnelle correspondante."""),
r"""\editionEtape{1. Décrire les changements de composition}
Au premier tirage, $P(R_1)=4/5$ et $P(B_1)=1/5$. Après rouge, il reste 3 rouges et 1 bleue : branches $3/4$ et $1/4$. Après bleu, il reste 4 rouges et aucune bleue : branches 1 et 0.
\editionEtape{2. Multiplier les chemins}
$P(R_1\cap R_2)=(4/5)(3/4)=\res{3/5}$. Les deux chemins de couleurs différentes valent chacun $\res{1/5}$ : $(4/5)(1/4)$ et $(1/5)\times1$.
\editionEtape{3. Utiliser une impossibilité}
Si la seconde est bleue, la première ne pouvait pas l’être car il n’y avait qu’une boule bleue. Elle est donc rouge avec certitude : $\res{P_{B_2}(R_1)=1}$. La branche de poids nul explicite l’impossibilité de deux bleues.
\editionRetenir{Sans remise, les probabilités du second tirage dépendent du premier. Une branche nulle peut apporter une information certaine après conditionnement.}""",
'assert Rational(4,5)*Rational(3,4)==Rational(3,5) and Rational(4,5)*Rational(1,4)==Rational(1,5) and Rational(1,5)*1==Rational(1,5)','bilan-B-arbre')
])]
