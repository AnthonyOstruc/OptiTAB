# -*- coding: utf-8 -*-
"""Rédaction du lot géométrie 6e 140–145, sans accès à la base."""
from pathlib import Path
import re,json,math,hashlib
BASE=Path(__file__).resolve().parent.parent
PROGRAMME='https://www.education.gouv.fr/sites/default/files/ensel620_annexe2-v2.pdf'
def fmt(x):return f'{x:g}'.replace('.','{,}')
def box(kind,body,title=''):return f'::: {kind}'+(' '+title if title else '')+'\n'+body+'\n:::\n'
def q(question,method,one,two,result):return (question,method,one.split('|',1),two.split('|',1),result)
def pic(body):return '\\begin{tikzpicture}\n'+body+'\n\\end{tikzpicture}'
def node(x,y,label,anchor='south',color='otInk'):
 return rf'\node[anchor={anchor},text={color},inner sep=4pt] at ({x},{y}) {{$ {label} $}};'+'\n'
COURSES={
140:r'''::: objectifs
Nommer les objets de géométrie, construire un milieu et décrire des points par leurs distances à un centre.
:::

## I. Des objets et des notations précis

::: definition
Par deux points distincts $A$ et $B$ passe une unique droite, notée $(AB)$. Elle se prolonge sans limite des deux côtés.
Le segment $[AB]$ est la partie comprise entre $A$ et $B$. La demi-droite $[AB)$ commence en $A$, passe par $B$ et se prolonge de ce côté.
:::

::: notation
$[AB]$ désigne un **objet** ; $AB$ désigne sa **longueur**, un nombre accompagné d’une unité. On peut écrire $AB=6$ cm, mais pas « $[AB]=6$ cm ».
:::

[IMAGE_1]

::: propriete Positions de droites
Deux droites sécantes se coupent en un point. Si elles forment des angles droits, elles sont perpendiculaires ; l’équerre permet de le vérifier. Deux droites parallèles distinctes n’ont aucun point commun.
:::

::: methode Tracer une perpendiculaire
Placer un côté de l’angle droit de l’équerre sur la droite donnée. Faire glisser l’équerre jusqu’au point imposé, puis tracer le long de l’autre côté. Coder l’angle droit avec un petit carré.
:::

## II. Distance et milieu

::: definition
La distance entre $A$ et $B$ est la longueur du segment $[AB]$. Le milieu $M$ de $[AB]$ est le point **du segment** pour lequel $AM=MB$.
:::

::: formule
$$AM=MB=\frac{AB}{2}$$
:::

::: exemple
Si $AB=7$ cm, les deux moitiés mesurent $7\div2=3{,}5$ cm. On place $M$ sur le segment à $3{,}5$ cm de $A$, puis on code $AM=MB$.
:::

::: attention
Une égalité $PA=PB$ ne suffit pas à faire de $P$ le milieu : il faut aussi que $P$ appartienne au segment $[AB]$.
:::

## III. Cercle et disque

::: definition
Le cercle de centre $O$ et de rayon $r$ est l’ensemble des points à une distance **exactement égale** à $r$ de $O$.
Le disque de même centre et de même rayon contient les points dont la distance à $O$ est **inférieure ou égale** à $r$ : le cercle et tout son intérieur.
:::

[IMAGE_2]

| Distance au centre | Position |
|---|---|
| $OP<r$ | À l’intérieur du disque |
| $OP=r$ | Sur le cercle, donc aussi dans le disque |
| $OP>r$ | À l’extérieur du disque |

::: definition Rayons, cordes et diamètres
Un rayon est un segment joignant le centre à un point du cercle. Une corde joint deux points du cercle. Une corde passant par le centre est un diamètre. Tous les rayons ont la même longueur ; un diamètre mesure deux fois le rayon.
$$d=2r\qquad r=\frac d2$$
:::

## IV. Résoudre une condition de distance

::: methode Une ou deux conditions
« Être à 3 cm de $A$ » signifie appartenir au cercle de centre $A$ et de rayon 3 cm. « Être à 3 cm de $A$ et à 4 cm de $B$ » impose d’appartenir aux deux cercles : chercher leurs points communs. Selon les données, il peut n’y avoir aucun point, un point ou deux points.
:::

::: retenir
Lire les mots **exactement**, **au plus**, **à l’intérieur**, **sur**. Choisir l’instrument adapté et contrôler les longueurs avec leur unité.
:::
''',
141:r'''::: objectifs
Nommer, comparer, mesurer et construire des angles ; expliquer une mesure ; construire une bissectrice.
:::

## I. Nommer et reconnaître

::: definition
Un angle est formé de deux demi-droites de même origine. Dans $\widehat{AOB}$, le sommet est $O$ et les côtés sont $[OA)$ et $[OB)$. La lettre du sommet est toujours au milieu.
:::

| Angle | Mesure |
|---|---|
| Nul | $0^\circ$ |
| Aigu | Strictement entre $0^\circ$ et $90^\circ$ |
| Droit | $90^\circ$ |
| Obtus | Strictement entre $90^\circ$ et $180^\circ$ |
| Plat | $180^\circ$ |
| Plein | $360^\circ$ |

::: attention
Allonger les côtés du dessin ne change pas l’ouverture de l’angle. Un quart de tour vaut $90^\circ$, un demi-tour $180^\circ$ et un tour complet $360^\circ$.
:::

## II. Utiliser le rapporteur

::: methode Mesurer
1. Estimer si l’angle est aigu ou obtus.
2. Poser le centre du rapporteur sur le sommet.
3. Aligner le zéro d’une graduation sur l’un des côtés.
4. Lire la mesure à la rencontre de l’autre côté, sur **la graduation qui commence à ce zéro**.
:::

::: exemple Deux graduations
Le même trait peut porter les nombres 35 et 145. Si l’angle est aigu et que la lecture part du bon zéro, sa mesure est $35^\circ$, pas $145^\circ$.
:::

::: methode Construire $65^\circ$
Tracer une première demi-droite. Placer le rapporteur au sommet avec son zéro sur ce côté. Faire un repère à $65^\circ$, puis tracer la seconde demi-droite passant par le repère. Contrôler l’ouverture et la mesure.
:::

## III. Calculer avec des angles

::: definition
Deux angles adjacents ont le même sommet, un côté commun et des intérieurs disjoints. Deux angles supplémentaires ont une somme de $180^\circ$ ; ils ne sont pas obligatoirement adjacents.
:::

::: propriete
Deux angles adjacents formant un angle plat sont supplémentaires. Deux angles opposés par le sommet, formés par deux droites sécantes, ont la même mesure.
:::

[IMAGE_1]

::: exemple
Si un angle mesure $65^\circ$, son supplémentaire mesure $180^\circ-65^\circ=115^\circ$. Son opposé par le sommet mesure encore $65^\circ$.
:::

## IV. Partager un angle en deux

::: definition Bissectrice
Pour un angle saillant non nul, inférieur à $180^\circ$, la bissectrice est la droite qui partage l’angle en deux angles adjacents de même mesure. On trace souvent seulement sa demi-droite située à l’intérieur de l’angle. Elle est un axe de symétrie de l’angle.
:::

[IMAGE_2]

::: methode Au rapporteur ou par pliage
Mesurer l’angle puis diviser sa mesure par 2. Pour $70^\circ$, chaque moitié mesure $35^\circ$. Tracer la demi-droite correspondante. Par pliage, superposer les deux côtés : le pli donne la bissectrice.
:::

::: retenir
Identifier les positions avant de calculer. Un angle plat donne une somme de $180^\circ$ ; une bissectrice donne **deux mesures égales**.
:::
''',
142:r'''::: objectifs
Construire des triangles, reconnaître leurs propriétés, calculer leurs angles et construire leur cercle circonscrit.
:::

## I. Préparer une construction

::: definition
Un triangle est un polygone à trois côtés. Dans le triangle $ABC$, les côtés sont $[AB]$, $[BC]$ et $[CA]$ ; les sommets sont $A$, $B$, $C$. Faire d’abord un schéma et y inscrire les données.
:::

::: methode Trois longueurs
Pour $AB=6$ cm, $AC=4$ cm et $BC=5$ cm : tracer le segment $[AB]$ de 6 cm. Tracer un arc de centre $A$, rayon 4 cm, puis un arc de centre $B$, rayon 5 cm. Une intersection des arcs donne $C$. Relier les sommets et contrôler les trois longueurs.
:::

[IMAGE_1]

::: attention Existence
Les arcs ne se rencontrent pas toujours. Avec 3 cm, 4 cm et 8 cm, le triangle est impossible : les deux petits côtés totalisent seulement 7 cm. Si la plus grande longueur est égale à la somme des deux autres, les trois points sont alignés : ce n’est pas un triangle non aplati.
:::

::: methode Avec des angles
Avec deux côtés et l’angle qu’ils forment, tracer d’abord cet angle, puis reporter chaque longueur sur son côté. Avec un côté et les deux angles à ses extrémités, tracer les deux demi-droites dans le même demi-plan ; leur intersection est le troisième sommet.
:::

## II. Reconnaître un triangle particulier

| Triangle | Propriété utile |
|---|---|
| Rectangle | Un angle droit ; les deux autres angles sont aigus. |
| Isocèle en $A$ | $AB=AC$ ; les angles en $B$ et $C$ sont égaux. |
| Équilatéral | Trois côtés égaux ; trois angles de $60^\circ$. |

::: attention
« Isocèle en $A$ » désigne le sommet commun aux deux côtés égaux. Un dessin penché peut être un triangle rectangle ; son orientation ne change pas ses propriétés.
:::

## III. Somme des angles

::: propriete
La somme des mesures des trois angles d’un triangle vaut $180^\circ$.
:::

::: exemple
Deux angles mesurent $48^\circ$ et $67^\circ$.
$$
\begin{aligned}
\text{Troisième angle}&=180^\circ-(48^\circ+67^\circ)\\
&=180^\circ-115^\circ\\
&=65^\circ
\end{aligned}
$$
Dans un triangle rectangle, les deux angles aigus ont donc une somme de $90^\circ$.
:::

## IV. Cercle circonscrit

::: propriete
Les trois médiatrices des côtés d’un triangle se rencontrent en un même point $O$. Ce point est le centre du cercle passant par les trois sommets : le cercle **circonscrit**.
:::

[IMAGE_2]

::: demonstration Pourquoi deux médiatrices suffisent
Si $O$ est sur la médiatrice de $[AB]$, alors $OA=OB$. S’il est aussi sur celle de $[AC]$, alors $OA=OC$. Ainsi $OA=OB=OC$ : le cercle de centre $O$ et de rayon $OA$ passe par $A$, $B$, $C$. Comme $OB=OC$, $O$ est aussi sur la troisième médiatrice.
:::

::: methode
Construire deux médiatrices à l’équerre et à la règle, ou au compas. Nommer leur intersection $O$. Tracer le cercle de centre $O$ passant par un sommet, puis vérifier les deux autres. Le centre peut être à l’extérieur du triangle.
:::

::: retenir
Les côtés et les angles donnés guident la construction ; les propriétés permettent de la justifier. Le cercle circonscrit **passe par** les sommets.
:::
''',
143:r'''::: objectifs
Réinvestir les figures du cours moyen : décrire, classer et construire des quadrilatères ; justifier avec les côtés et les angles.
:::

## I. Nommer dans le bon ordre

::: definition
Un quadrilatère est un polygone à quatre côtés. Dans $ABCD$, on suit le contour dans cet ordre : les côtés sont $[AB]$, $[BC]$, $[CD]$ et $[DA]$. Ses diagonales sont $[AC]$ et $[BD]$, qui joignent des sommets opposés.
:::

[IMAGE_1]

::: attention
Une diagonale n’est pas un côté. Pour nommer une figure, faire le tour de son contour sans sauter de sommet.
:::

## II. Reconnaître les figures usuelles

| Figure | Définition |
|---|---|
| Rectangle | Quadrilatère ayant quatre angles droits. |
| Losange | Quadrilatère ayant quatre côtés de même longueur. |
| Carré | Quadrilatère ayant quatre angles droits et quatre côtés de même longueur. |

::: propriete
Dans un rectangle, les côtés opposés sont parallèles et de même longueur. Un carré est à la fois un rectangle et un losange. Tous les rectangles ne sont pas des carrés ; tous les losanges non plus.
:::

::: remarque Trapèze : convention utilisée
On appelle ici trapèze un quadrilatère ayant au moins une paire de côtés opposés parallèles. Un trapèze rectangle possède deux angles droits. Ces figures servent à réinvestir le parallélisme et la perpendicularité étudiés au cours moyen.
:::

## III. Construire avec les instruments

::: methode Un rectangle de 5 cm sur 3 cm
Tracer $[AB]$ de 5 cm. En $A$ et en $B$, tracer les perpendiculaires à $(AB)$, du même côté. Placer $D$ à 3 cm de $A$ et $C$ à 3 cm de $B$. Relier $C$ et $D$ ; vérifier les angles droits et les longueurs.
:::

[IMAGE_2]

::: methode Un carré
Utiliser la même construction avec deux dimensions égales. Contrôler les quatre angles droits **et** les quatre côtés : une seule de ces conditions ne suffit pas.
:::

::: methode Un losange
Tracer un premier côté. Choisir un troisième sommet à la bonne distance du second ; deux arcs de même rayon permettent de trouver le quatrième sommet. Vérifier les quatre longueurs ; ne pas imposer des angles droits qui ne sont pas donnés.
:::

## IV. Calculer et justifier

::: formule
$$P_{\text{rectangle}}=2\times(L+\ell)\qquad P_{\text{carré}}=4\times c$$
:::

::: exemple
Pour 5 cm sur 3 cm : $P=2\times(5+3)=16$ cm. Pour un carré de côté 4 cm : $P=4\times4=16$ cm. Deux figures de même périmètre peuvent avoir des formes et des dimensions différentes.
:::

::: retenir
Le nom d’une figure se justifie avec les données et les codages, pas avec son orientation. Coder un angle droit ou des longueurs égales donne un renseignement précis.
:::
''',
144:r'''::: objectifs
Construire une médiatrice, utiliser l’équidistance dans les deux sens et rédiger un raisonnement court.
:::

## I. Deux conditions à respecter

::: definition
La médiatrice d’un segment est la droite **perpendiculaire** à ce segment qui passe par son **milieu**. Ces deux conditions sont indispensables.
:::

[IMAGE_1]

::: attention
Passer par le milieu ne suffit pas. Être perpendiculaire ne suffit pas non plus. La médiatrice est une droite entière ; elle n’a pas pour extrémité le milieu du segment.
:::

## II. Construire une médiatrice

::: methode Règle graduée et équerre
Mesurer $AB$, puis placer le milieu $M$ sur $[AB]$ avec $AM=MB=AB\div2$. Tracer la perpendiculaire à $(AB)$ passant par $M$ avec l’équerre. Coder le milieu et l’angle droit.
:::

::: methode Compas et règle
Choisir un écartement **plus grand que la moitié de $AB$**. Sans le changer, tracer deux arcs de centre $A$, puis deux arcs de centre $B$, de part et d’autre du segment. Appeler $P$ et $Q$ leurs intersections et tracer la droite $(PQ)$. Conserver les arcs comme traces de construction.
:::

::: remarque
Un rayon trop petit ne donne aucune intersection. Un rayon égal à la moitié de $AB$ donne seulement le milieu ; il ne fournit pas deux points pour tracer la droite.
:::

## III. Une propriété dans les deux sens

::: propriete
Un point appartient à la médiatrice de $[AB]$ **si et seulement s’il** est à égale distance de $A$ et de $B$.
:::

[IMAGE_2]

::: methode De la position vers les distances
Je sais que $P$ est sur la médiatrice de $[AB]$. Or tout point de cette droite est équidistant de $A$ et de $B$. Donc $PA=PB$. Si $PA=4$ cm, alors $PB=4$ cm, sans mesurer.
:::

::: methode Des distances vers la position
Je sais que $QA=QB$. Or un point équidistant des extrémités d’un segment appartient à sa médiatrice. Donc $Q$ est sur la médiatrice de $[AB]$.
:::

::: attention
Le milieu est un point de la médiatrice, mais il y en a une infinité d’autres. Un point équidistant de $A$ et $B$ n’est donc pas nécessairement le milieu de $[AB]$.
:::

## IV. Résoudre un problème

::: exemple Un lieu à construire
Pour placer une borne à la même distance de deux maisons $A$ et $B$, chercher sur la médiatrice de $[AB]$. Si la borne doit aussi être sur un chemin, chercher le point commun entre le chemin et la médiatrice. Vérifier ensuite toutes les contraintes.
:::

::: retenir
Dans une justification, séparer la **donnée**, la **propriété** et la **conclusion**. Un dessin aide à chercher ; les propriétés expliquent pourquoi la réponse est juste.
:::
''',
145:r'''::: objectifs
Construire une image par symétrie axiale sur quadrillage ou papier uni ; reconnaître un axe ; utiliser les longueurs et les angles conservés.
:::

## I. L’axe est une médiatrice

::: definition
Si $A$ n’est pas sur l’axe $(d)$, son symétrique $A'$ est le point tel que $(d)$ soit la médiatrice de $[AA']$. Ainsi le segment joignant les deux points est perpendiculaire à l’axe et son milieu appartient à l’axe.
Un point situé sur $(d)$ est sa propre image.
:::

[IMAGE_1]

::: propriete
Si $A'$ est l’image de $A$, alors $A$ est l’image de $A'$. Faire deux fois la même symétrie ramène au point initial.
:::

## II. Construire sur différents supports

::: methode Quadrillage, axe horizontal ou vertical
Compter les carreaux de $A$ jusqu’à l’axe **perpendiculairement** à celui-ci. Reporter le même nombre de carreaux de l’autre côté, sur la même perpendiculaire. Marquer l’image puis vérifier les deux distances.
:::

::: attention Axe oblique
Pour une diagonale du quadrillage, les trajets horizontaux ne mesurent pas la distance à l’axe. Repérer la perpendiculaire à cette diagonale, puis placer les points de part et d’autre à distances égales. Utiliser l’équerre ou le pliage pour contrôler.
:::

::: methode Papier uni : équerre et compas
Tracer la perpendiculaire à $(d)$ passant par $A$ ; nommer $H$ son intersection avec l’axe. Au compas, reporter $HA$ sur cette droite de l’autre côté de $H$ pour obtenir $A'$. Vérifier $HA'=HA$ et l’angle droit en $H$.
:::

[IMAGE_2]

## III. Transformer une figure

::: propriete
La symétrie axiale conserve les longueurs, les angles, l’alignement et les aires. L’image d’un segment est le segment joignant les images de ses extrémités. L’image d’un cercle est un cercle de même rayon, dont le centre est l’image du centre initial.
:::

::: methode Polygone et cercle
Construire chaque sommet image, puis les relier dans le même ordre. Pour un cercle, construire l’image du centre et garder le même écartement de compas.
:::

::: exemple
Un rectangle de 2 carreaux sur 3 carreaux reste un rectangle de 2 sur 3. Son périmètre reste $2\times(2+3)=10$ unités et son aire reste $2\times3=6$ unités d’aire.
:::

## IV. Axes d’une figure

::: definition
Un axe de symétrie d’une figure est une droite pour laquelle l’image de la figure se superpose exactement à la figure initiale.
:::

| Figure | Nombre d’axes |
|---|---|
| Rectangle non carré | 2 |
| Carré | 4 |
| Triangle isocèle non équilatéral | 1 |
| Triangle équilatéral | 3 |
| Cercle | Une infinité : toutes les droites passant par son centre |

::: retenir
Une symétrie n’est pas un simple décalage. Pour contrôler une construction, chercher le milieu, l’angle droit et les distances conservées.
:::
'''}

FICHES={
140:r'''::: objectifs
Employer les bons mots et comparer les bonnes distances.
:::
## I. Objets et milieu
- Droite $(AB)$ : illimitée ; segment $[AB]$ : deux extrémités ; demi-droite $[AB)$ : origine $A$.
- $AB$ est une longueur, avec une unité.
::: retenir
$M$ est le milieu de $[AB]$ si $M$ est sur le segment et $AM=MB=AB\div2$.
:::
## II. Cercle ou disque ?
| Condition | Position |
|---|---|
| $OP=r$ | Sur le cercle et dans le disque |
| $OP<r$ | À l’intérieur du disque |
| $OP>r$ | À l’extérieur du disque |
- Rayon : du centre au cercle. Corde : entre deux points du cercle.
- Diamètre : corde passant par le centre ; $d=2r$ et $r=d\div2$.
::: attention
Le disque contient son bord. « À 3 cm » impose une égalité ; « à au plus 3 cm » autorise toutes les distances plus petites.
:::
''',
141:r'''::: objectifs
Mesurer, construire et partager un angle.
:::
## I. Repères
| Mesure | Angle |
|---|---|
| $0^\circ$, $90^\circ$, $180^\circ$, $360^\circ$ | Nul, droit, plat, plein |
| Entre $0^\circ$ et $90^\circ$ | Aigu |
| Entre $90^\circ$ et $180^\circ$ | Obtus |
::: methode Rapporteur
Centre sur le sommet, zéro sur un côté, lecture sur la graduation qui part de ce zéro. Estimer l’ouverture avant de lire.
:::
## II. Calculs utiles
- Angles supplémentaires : somme $180^\circ$.
- Angles opposés par le sommet : mesures égales.
- Bissectrice : deux angles adjacents de même mesure ; calculer la moitié.
::: attention
Dans $\widehat{AOB}$, le sommet est $O$. Allonger les côtés ne change pas la mesure. Ne pas choisir la mauvaise graduation du rapporteur.
:::
''',
142:r'''::: objectifs
Construire puis justifier un triangle.
:::
## I. Constructions et angles
- Trois côtés : un segment, puis deux arcs de compas ; vérifier qu’ils se rencontrent.
- Un côté et deux angles : deux demi-droites du même côté de la base.
::: formule
$$\widehat A+\widehat B+\widehat C=180^\circ$$
:::
- Isocèle en $A$ : $AB=AC$, angles en $B$ et $C$ égaux.
- Équilatéral : trois angles de $60^\circ$.
- Rectangle : les deux angles aigus totalisent $90^\circ$.
## II. Cercle circonscrit
::: methode
Construire deux médiatrices. Leur intersection $O$ est équidistante des trois sommets. Tracer le cercle de centre $O$ et de rayon $OA$, puis vérifier $B$ et $C$.
:::
::: attention
Le cercle circonscrit passe par les sommets. Son centre n’est pas toujours à l’intérieur du triangle. Un dessin n’est pas à mesurer à l’écran.
:::
''',
143:r'''::: objectifs
Classer les quadrilatères à partir de leurs propriétés.
:::
## I. Définitions
| Figure | Condition |
|---|---|
| Rectangle | Quatre angles droits |
| Losange | Quatre côtés égaux |
| Carré | Quatre angles droits et quatre côtés égaux |
::: retenir
Un carré est aussi un rectangle et un losange. Les diagonales joignent des sommets opposés : dans $ABCD$, ce sont $[AC]$ et $[BD]$.
:::
## II. Construire et calculer
- Rectangle : tracer un côté, les perpendiculaires à ses extrémités, puis reporter la largeur du même côté.
- Carré : appliquer la même méthode avec deux dimensions égales.
$$P_{\text{rectangle}}=2\times(L+\ell),\qquad P_{\text{carré}}=4c.$$
::: attention
Quatre côtés égaux ne donnent pas forcément des angles droits. Quatre angles droits ne donnent pas forcément quatre côtés égaux. L’orientation du dessin ne change pas sa nature.
:::
''',
144:r'''::: objectifs
Utiliser la médiatrice dans les deux sens.
:::
## I. Définition et construction
::: definition
La médiatrice est la droite perpendiculaire au segment passant par son milieu.
:::
- Règle et équerre : milieu, puis perpendiculaire.
- Compas : même rayon, plus grand que la moitié du segment ; tracer les arcs de centres $A$ et $B$, puis la droite passant par leurs deux intersections.
## II. Raisonner
::: propriete
$P$ est sur la médiatrice de $[AB]$ si et seulement si $PA=PB$.
:::
::: methode
Donnée → propriété → conclusion. Une position sur la médiatrice donne des longueurs égales ; des longueurs égales permettent de prouver l’appartenance à la médiatrice.
:::
::: attention
Un point équidistant n’est pas forcément le milieu. Une droite seulement perpendiculaire, ou passant seulement par le milieu, ne suffit pas.
:::
''',
145:r'''::: objectifs
Contrôler une image par symétrie axiale.
:::
## I. Construire
::: definition
L’axe est la médiatrice du segment joignant un point à son image. Tout point de l’axe reste à sa place.
:::
::: methode
Tracer la perpendiculaire à l’axe, puis reporter la même distance de l’autre côté. Sur un quadrillage, compter perpendiculairement à l’axe. Relier les images des sommets dans le même ordre.
:::
## II. Propriétés
- Longueurs, angles, alignement et aires sont conservés.
- Cercle image : image du centre, même rayon.
- Deux applications de la même symétrie ramènent à la figure initiale.
| Figure | Axes |
|---|---|
| Rectangle non carré / carré | 2 / 4 |
| Triangle isocèle non équilatéral / équilatéral | 1 / 3 |
| Cercle | Une infinité |
::: attention
Pour un axe oblique, un déplacement horizontal ne convient pas. La symétrie inverse le côté de l’axe ; elle ne déplace pas simplement toute la figure dans le même sens.
:::
'''}

FIGURES={};EXERCISES={};CHECKS={};COVERAGE={}
def fig(n,name,code):FIGURES.setdefault(n,{})[name]=code;return name
def add(n,eid,title,level,intro,questions,tests,figure=None):
 EXERCISES.setdefault(n,[]).append({'id':eid,'titre':title,'difficulte':level,'intro':intro,'questions':questions,'figure':figure})
 CHECKS.setdefault(n,{})[str(eid)]=tests

def point(x,y,label,anchor='south',color='otInk'):
 return rf'\fill[{color}] ({x},{y}) circle (1.6pt);'+'\n'+node(x,y,label,anchor,color)
def caption(y,text,color='otInk'):
 return rf'\node[anchor=north,text={color},inner sep=4pt] at (2.5,{y}) {{{text}}};'+'\n'
def segment(L=6,mid=True):
 s=5/L
 z=rf'\begin{{scope}}[x={s}cm,y={s}cm]\draw[geoTrait] (0,0)--({L},0);'
 z+=point(0,0,'A','north')+point(L,0,'B','north')
 if mid:z+=point(L/2,0,'M','south','otGreenDark')+rf'\draw[geoReponse] ({L/4},-.12)--({L/4},.12) ({3*L/4},-.12)--({3*L/4},.12);'
 z+=r'\end{scope}'
 return pic(z)
def circlefigure():
 return pic(r'''\draw[geoTrait] (0,0) circle (2);
\draw[geoTrait] (-2,0)--(2,0);
\draw[geoReponse] (0,0)--(1,1.732);
\fill[otNavy] (0,0) circle (1.6pt);
\fill[otNavy] (1,1.732) circle (1.6pt);
\fill[otNavy] (-2,0) circle (1.6pt);
\fill[otNavy] (2,0) circle (1.6pt);
'''+node(0,-.12,'O','north')+node(1,1.82,'A','south')+node(-2.05,0,'D','east')+node(2.05,0,'B','west'))
def anglefigure(a,bis=True):
 z=rf'\draw[geoTrait] (0,0)--(4,0);\draw[{"geoTrait" if bis else "geoReponse"}] (0,0)--({a}:4);'
 z+=point(0,0,'O','north east')+node(4,0,'A','west')+node(4*math.cos(math.radians(a)),4*math.sin(math.radians(a)),'B','south')
 z+=rf'\draw[geoTrait] (1,0) arc (0:{a}:1);'
 if bis:
  z+=rf'\draw[geoReponse] (0,0)--({a/2}:4.2);'
  z+=node(4.2*math.cos(math.radians(a/2)),4.2*math.sin(math.radians(a/2)),'C','west','otGreenDark')
 z+=rf'\node[anchor=north,inner sep=6pt] at (2,-.3) {{$\widehat{{AOB}}={a}^\circ$}};'
 return pic(z)
def trianglefigure(L,a,b,circ=False):
 x=(a*a-b*b+L*L)/(2*L);y=math.sqrt(a*a-x*x);s=5/L
 oy=(a*a-L*x)/(2*y);r=math.hypot(L/2,oy)
 z=rf'\begin{{scope}}[x={s}cm,y={s}cm]'
 if circ:z+=rf'\draw[geoReponse] ({L/2},{oy}) circle ({r});\draw[geoAide] ({L/2},-.7)--({L/2},{max(y,oy+r)+.3});'
 z+=rf'\draw[{"geoTrait" if circ else "geoReponse"}] (0,0)--({L},0)--({x},{y})--cycle;'
 z+=point(0,0,'A','north east')+point(L,0,'B','north west')+point(x,y,'C','south')
 if circ:z+=point(L/2,oy,'O','north east','otGreenDark')
 z+=r'\end{scope}'
 bottom=min(0,oy-r) if circ else 0
 z+=caption(s*bottom-.45,rf'$AB={fmt(L)}$ cm ; $AC={fmt(a)}$ cm ; $BC={fmt(b)}$ cm')
 return pic(z)
def mediatricefigure(L=6,r=5):
 h=math.sqrt(r*r-(L/2)**2);s=5/L
 z=rf'\begin{{scope}}[x={s}cm,y={s}cm]\draw[geoTrait] ({-L/2},0)--({L/2},0);\draw[geoReponse] (0,{-h-.4})--(0,{h+.4});\draw[geoAide] ({-L/2},0)--(0,{h})--({L/2},0);\draw[geoReponse] (0,.3)--(.3,.3)--(.3,0);'
 for x,y,t,a in [(-L/2,0,'A','east'),(L/2,0,'B','west'),(0,0,'M','north west'),(0,h,'P','south east'),(0,-h,'Q','north west')]:z+=point(x,y,t,a,'otGreenDark' if t in 'MPQ' else 'otInk')
 z+=r'\end{scope}'
 return pic(z)
def rectfigure(w=5,h=3,kind='rectangle'):
 z=rf'\draw[geoReponse] (0,0)--({w},0)--({w},{h})--(0,{h})--cycle;'
 for x,y,t,a in [(0,0,'A','north east'),(w,0,'B','north west'),(w,h,'C','south west'),(0,h,'D','south east')]:z+=point(x,y,t,a)
 if kind=='rectangle':
  for x,y,sx,sy in [(0,0,1,1),(w,0,-1,1),(w,h,-1,-1),(0,h,1,-1)]:z+=rf'\draw[geoTrait] ({x+sx*.22},{y})--({x+sx*.22},{y+sy*.22})--({x},{y+sy*.22});'
 return pic(z)
def symmetryfigure(d=1,w=2,h=3):
 lim=d+w+1;s=min(.72,7/(2*lim))
 z=rf'\begin{{scope}}[x={s}cm,y={s}cm]\draw[step=1,otRule,thin] ({-lim},-1) grid ({lim},{h+1});\draw[otOrange,thick] (0,-1.2)--(0,{h+1.5});'
 z+=rf'\node[anchor=south,text=otOrange] at (0,{h+1.5}) {{$(d)$}};'
 for sign,color,prime in [(1,'otNavy',''),(-1,'otGreenDark',"'")]:
  z+=rf'\draw[{color},line width=1pt] ({sign*d},0)--({sign*(d+w)},0)--({sign*(d+w)},{h})--({sign*d},{h})--cycle;'
  for x,y,t,anc in [(d,0,'A','north'),(d+w,0,'B','north'),(d+w,h,'C','south'),(d,h,'D','south')]:z+=point(sign*x,y,t+prime,anc,color)
 z+=r'\end{scope}'
 return pic(z)

# Chaque famille constitue une situation complète ; ses trois exercices ont
# des demandes différentes, sur les mêmes données exactes et la même figure.
def family(n,idx,titles,intro,rows,figure,tests,levels=('easy','medium','medium')):
 ids=sorted(e['id'] for e in json.loads((next(BASE.glob(str(n)+'_*'))/'source_en_ligne/meta.json').read_text(encoding='utf-8'))['exercices']) if n!=143 else [f'nouveau-{i}' for i in range(1,13)]
 for k,title in enumerate(titles):
  add(n,ids[idx*3+k],title,levels[k],intro,rows[k*3:k*3+3],tests,figure)

def Q(question,method,title1,body1,title2,body2,result):
 return q(question,method,title1+'|'+body1,title2+'|'+body2,result)

def ids_for(n):
 return sorted(e['id'] for e in json.loads((next(BASE.glob(str(n)+'_*'))/'source_en_ligne/meta.json').read_text(encoding='utf-8'))['exercices'])

def secants(a):
 z=rf'\draw[geoTrait] (-3.4,0)--(3.4,0) ({a+180}:3.2)--({a}:3.2);\draw[geoTrait] (.8,0) arc (0:{a}:.8);'
 for x,y,t,anc in [(3.4,0,'A','west'),(-3.4,0,'C','east'),(3.2*math.cos(math.radians(a)),3.2*math.sin(math.radians(a)),'B','south'),(-3.2*math.cos(math.radians(a)),-3.2*math.sin(math.radians(a)),'D','north')]:z+=node(x,y,t,anc)
 z+=point(0,0,'O','south east')+caption(-3,rf'Donnée : $\widehat{{AOB}}={a}^\circ$')
 z+=rf'\draw[geoReponse] ({a}:.65) arc ({a}:180:.65) (180:.85) arc (180:{a+180}:.85);'
 z+=caption(-3.65,rf'$\widehat{{BOC}}={180-a}^\circ$ ; $\widehat{{COD}}={a}^\circ$','otGreenDark')
 return pic(z)

def protractor(a):
 z=r'\draw[geoTrait] (-3,0)--(3,0);\draw[geoTrait] (3,0) arc (0:180:3);'
 for t in range(0,181,10):
  z+=rf'\draw[geoTrait] ({t}:2.86)--({t}:3);'
  if t%30==0:
   z+=rf'\node[font=\small,inner sep=1pt] at ({t}:3.32) {{{t}}};\node[font=\small,text=otMuted,inner sep=1pt] at ({t}:2.48) {{{180-t}}};'
 z+=rf'\draw[geoReponse] (0,0)--({a}:3.7);'
 z+=point(0,0,'O','north')+node(3.8,0,'A','west')+node(3.7*math.cos(math.radians(a)),3.7*math.sin(math.radians(a)),'B','south')
 z+=caption(-.65,'Graduations extérieures : départ à droite.')
 return pic(z)

for i,eid in enumerate(ids_for(141)):
 k,j=divmod(i,3);a=([35,90,125],[30,60,120],[45,65,110],[60,70,100],[40,55,75],[35,65,120],[25,35,40])[k][j]
 name=f'angle_{k+1}_{j+1}';tests=[]
 if k==0:
  title=f'Classer un angle de {a} degrés';intro=rf'Un angle $\widehat{{AOB}}$ mesure ${a}^\circ$.';image=None
  nature='aigu' if a<90 else ('droit' if a==90 else 'obtus')
  rows=[Q('Nommer son sommet et ses côtés.','Lire les trois lettres dans le bon ordre.','Repérer le sommet','La lettre centrale est $O$.','Nommer les demi-droites','Les côtés partent du sommet et passent par $A$ et $B$.','Sommet $O$ ; côtés $[OA)$ et $[OB)$.'),Q('Classer cet angle.','Comparer à un angle droit.','Fixer la référence',r'Un angle droit mesure $90^\circ$.','Comparer la mesure',rf'${a}^\circ$ est '+('inférieur à' if a<90 else 'égal à' if a==90 else 'supérieur à')+r' $90^\circ$'+(r' et inférieur à $180^\circ$.' if a>90 else '.'),f'L’angle est {nature}.'),Q('Un agrandissement du dessin change-t-il sa mesure ?','Distinguer ouverture et longueur des côtés.','Agrandir les côtés','Un agrandissement conserve les directions des demi-droites.','Observer l’ouverture','Elle reste la même entre les deux côtés.',rf'Non ; l’angle mesure toujours ${a}^\circ$.')];tests=[f'{0<a<180}']
 elif k==1:
  title=f'Choisir la bonne graduation pour {a} degrés';intro=r'Le dessin représente un rapporteur à deux échelles. Le côté $[OA)$ part vers la droite. Chaque petit intervalle vaut $10^\circ$.';image=fig(141,name,protractor(a))
  rows=[Q('Quelle échelle utiliser ?','Partir du zéro situé sur le premier côté.','Repérer le côté initial','$[OA)$ pointe vers la droite.','Choisir le zéro','L’échelle extérieure commence à $0$ à droite.','Lire l’échelle extérieure.'),Q(r'Lire la mesure de $\widehat{AOB}$.','Suivre les graduations depuis le bon zéro.','Compter les intervalles',rf'Le rayon $[OB)$ arrive à la graduation ${a}$.','Donner l’unité','La mesure d’un angle s’exprime en degrés.',rf'$\widehat{{AOB}}={a}^\circ$.'),Q(rf'Un élève lit ${180-a}^\circ$. Expliquer son erreur.','Comparer les deux échelles.','Identifier la lecture','Cette valeur est sur l’échelle qui commence à gauche.','Revenir au côté initial','Il faut partir du zéro à droite, sur $[OA)$.','Il a utilisé l’autre échelle.')];tests=[f'{a}+{180-a}==180']
 elif k==2:
  title=f'Construire un angle de {a} degrés';intro=rf'Tracer une demi-droite $[OA)$ puis construire un angle $\widehat{{AOB}}={a}^\circ$, au-dessus de cette demi-droite. La figure du corrigé donne le résultat attendu.';image=fig(141,name,anglefigure(a,False))
  rows=[Q('Comment positionner le rapporteur ?','Faire coïncider centre et zéro avec les données.','Placer le centre','Le centre du rapporteur doit être exactement en $O$.','Aligner le zéro','La ligne $0$–$180$ suit $[OA)$, avec le bon zéro sur ce côté.','Centre en $O$, zéro sur $[OA)$.'),Q('Construire le second côté.','Reporter la mesure puis tracer à la règle.','Marquer la graduation',rf'Placer une marque à ${a}^\circ$ depuis le zéro de droite.','Tracer la demi-droite','Tracer depuis $O$ vers la marque et choisir $B$ dessus.',rf'$\widehat{{AOB}}={a}^\circ$.'),Q('Donner deux contrôles de la construction.','Vérifier origine et ouverture.','Contrôler le sommet','Les deux demi-droites doivent partir du même point $O$.','Relire l’angle',rf'Le rapporteur correctement replacé doit indiquer ${a}^\circ$.','Même sommet et bonne mesure, du côté demandé.')];tests=[f'{0<a<180}']
 elif k==3:
  title=f'Partager un angle de {a} degrés';intro=rf'$\widehat{{AOB}}={a}^\circ$. Construire sa bissectrice ; $C$ sera sur la demi-droite intérieure portée par cette bissectrice.';image=fig(141,name,anglefigure(a))
  rows=[Q('Calculer la mesure de chaque moitié.','Partager l’angle en deux angles égaux.','Écrire le partage',rf'$\widehat{{AOC}}=\widehat{{COB}}$ et leur somme vaut ${a}^\circ$.','Calculer',rf'${a}\div2={fmt(a/2)}$.',rf'Chaque moitié mesure ${fmt(a/2)}^\circ$.'),Q('Construire la bissectrice au rapporteur.','Placer une direction à la moitié de l’angle.','Reporter la moitié',rf'À partir de $[OA)$, marquer ${fmt(a/2)}^\circ$ à l’intérieur de l’angle.','Tracer la droite','Tracer la droite par $O$ et la marque ; sa partie intérieure est $[OC)$.','La droite $(OC)$ est la bissectrice.'),Q('Comment vérifier par pliage ?','Superposer les deux côtés.','Plier depuis le sommet','Faire coïncider $[OA)$ avec $[OB)$ en gardant $O$ sur le pli.','Comparer au tracé','Le pli suit la bissectrice et partage l’ouverture en deux.','Le pli doit suivre $(OC)$.')];tests=[f'{a}/2=={a/2}']
 elif k==4:
  title=f'Compléter un angle plat à partir de {a} degrés';intro=rf'$A$, $O$, $C$ sont alignés, $O$ entre $A$ et $C$. $B$ est hors de cette droite et $\widehat{{AOB}}={a}^\circ$.';image=fig(141,name,secants(a))
  rows=[Q(r'Quelle est la mesure de $\widehat{AOC}$ ?','Reconnaître deux demi-droites opposées.','Utiliser l’alignement','$[OA)$ et $[OC)$ sont opposées.','Nommer l’angle','Elles forment un angle plat.',r'$\widehat{AOC}=180^\circ$.'),Q(r'Calculer $\widehat{BOC}$.','Retirer l’angle connu de l’angle plat.','Écrire la somme',r'$\widehat{AOB}+\widehat{BOC}=180^\circ$.','Soustraire',rf'$180-{a}={180-a}$.',rf'$\widehat{{BOC}}={180-a}^\circ$.'),Q('Ces deux angles sont-ils complémentaires ou supplémentaires ?','Comparer leur somme aux références.','Calculer la somme',rf'${a}+{180-a}=180$.','Nommer la relation',r'Deux angles de somme $180^\circ$ sont supplémentaires.','Ils sont supplémentaires.')];tests=[f'{a}+{180-a}==180']
 elif k==5:
  title=f'Raisonner sur deux droites sécantes à {a} degrés';intro=rf'Les droites $(AC)$ et $(BD)$ se coupent en $O$, entre $A$ et $C$, et entre $B$ et $D$. On donne $\widehat{{AOB}}={a}^\circ$.';image=fig(141,name,secants(a))
  rows=[Q(r'Quel angle est opposé par le sommet à $\widehat{AOB}$ ?','Chercher les côtés opposés.','Remplacer chaque côté','$[OC)$ est opposée à $[OA)$ ; $[OD)$ à $[OB)$.','Nommer l’angle',r'Ces côtés forment $\widehat{COD}$.',r'L’angle $\widehat{COD}$.'),Q('Donner sa mesure.','Utiliser l’égalité des angles opposés par le sommet.','Identifier la propriété','Les deux angles opposés par le sommet ont même mesure.','Reporter la donnée',rf'$\widehat{{AOB}}={a}^\circ$.',rf'$\widehat{{COD}}={a}^\circ$.'),Q('Calculer les deux autres angles.','Compléter l’angle plat.','Calculer un angle adjacent',rf'$\widehat{{BOC}}=180-{a}={180-a}^\circ$.','Utiliser l’opposition',r'$\widehat{DOA}=\widehat{BOC}$.',rf'$\widehat{{BOC}}=\widehat{{DOA}}={180-a}^\circ$.')];tests=[f'2*{a}+2*{180-a}==360']
 else:
  b=90-a;title=f'Décomposer un angle droit avec {a} degrés';intro=rf'$\widehat{{AOB}}=90^\circ$ et $[OC)$ est à l’intérieur. On donne $\widehat{{AOC}}={a}^\circ$.'
  z=anglefigure(90,False).replace(r'\end{tikzpicture}',rf'\draw[geoReponse] (0,0)--({a}:3.8);'+node(3.8*math.cos(math.radians(a)),3.8*math.sin(math.radians(a)),'C','west','otGreenDark')+r'\end{tikzpicture}')
  image=fig(141,name,z)
  rows=[Q(r'Les angles $\widehat{AOC}$ et $\widehat{COB}$ sont-ils adjacents ?','Vérifier sommet, côté commun et positions.','Lire les éléments communs','Ils ont le sommet $O$ et le côté $[OC)$.','Comparer les intérieurs','Leurs intérieurs sont de part et d’autre de $[OC)$, sans se recouvrir.','Oui, ils sont adjacents.'),Q(r'Calculer $\widehat{COB}$.','Compléter l’angle droit.','Écrire la somme',r'$\widehat{AOC}+\widehat{COB}=90^\circ$.','Soustraire',rf'$90-{a}={b}$.',rf'$\widehat{{COB}}={b}^\circ$.'),Q(r'$[OC)$ porte-t-elle la bissectrice de $\widehat{AOB}$ ?','Comparer les deux parties.','Calculer les deux mesures',rf'Les parties mesurent ${a}^\circ$ et ${b}^\circ$.','Tester l’égalité',rf'${a}\ne{b}$.','Non ; les deux angles ne sont pas égaux.')];tests=[f'{a}+{b}==90',f'{a}!={b}']
 add(141,eid,title,'easy' if k<2 else 'medium',intro,rows,tests,image)

def asafigure(L,alpha,beta):
 gamma=180-alpha-beta
 a=L*math.sin(math.radians(beta))/math.sin(math.radians(gamma))
 x=a*math.cos(math.radians(alpha));y=a*math.sin(math.radians(alpha));s=5/L
 z=rf'\begin{{scope}}[x={s}cm,y={s}cm]\draw[geoReponse] (0,0)--({L},0)--({x},{y})--cycle;'
 z+=point(0,0,'A','north east')+point(L,0,'B','north west')+point(x,y,'C','south')+r'\end{scope}'
 z+=caption(-.4,rf'$AB={fmt(L)}$ cm ; $\widehat{{A}}={alpha}^\circ$ ; $\widehat{{B}}={beta}^\circ$')
 return pic(z)

for i,eid in enumerate(ids_for(142)):
 k,j=divmod(i,3);name=f'triangle_{k+1}_{j+1}';image=None;tests=[]
 if k==0:
  L,a,b=[(6,4,5),(7,5,6),(8,6,7)][j];p=L+a+b
  title=f'Construire avec trois côtés : {L}, {a}, {b}';intro=rf'Construire $ABC$ avec $AB={L}$ cm, $AC={a}$ cm et $BC={b}$ cm, $C$ au-dessus de $(AB)$.';image=fig(142,name,trianglefigure(L,a,b))
  rows=[Q('Quel segment commencer à tracer ?','Choisir un côté connu comme base.','Lire les données',rf'Le côté $[AB]$ mesure ${L}$ cm.','Tracer précisément','Utiliser la règle graduée puis nommer les extrémités.',rf'Tracer $[AB]$ de ${L}$ cm.'),Q('Comment placer $C$ ?','Croiser les deux contraintes de distance.','Tracer deux arcs',rf'Un arc de centre $A$, rayon ${a}$ cm ; un autre de centre $B$, rayon ${b}$ cm.','Choisir l’intersection','Nommer $C$ celle située au-dessus de la base, puis relier aux extrémités.','La figure corrigée respecte les trois longueurs.'),Q('Calculer le périmètre.','Additionner les trois côtés.','Écrire la somme',rf'$P=AB+AC+BC={L}+{a}+{b}$.','Calculer et contrôler l’unité',rf'$P={p}$ cm ; on additionne des longueurs.',rf'$P={p}$ cm.')];tests=[f'{L}+{a}+{b}=={p}',f'{a}+{b}>{L}']
 elif k==1:
  a,b,L=[(3,4,8),(2,5,9),(4,5,10)][j];title=f'Déceler une construction impossible : {a}, {b}, {L}';intro=rf'On tente de construire $ABC$ avec $AB={L}$ cm, $AC={a}$ cm et $BC={b}$ cm.'
  rows=[Q('Quelle est la longueur maximale que peuvent couvrir les deux petits côtés mis bout à bout ?','Comparer les longueurs avant de tracer.','Additionner les deux longueurs',rf'${a}+{b}={a+b}$ cm.','Comparer à la base',rf'${a+b}<{L}$.',rf'Ils couvrent seulement ${a+b}$ cm, moins que la base.'),Q('Pourquoi les deux arcs de construction ne peuvent-ils pas se croiser ?','Interpréter les distances.','Partir de $A$ et de $B$',rf'Les rayons des arcs valent ${a}$ cm et ${b}$ cm.','Constater l’écart','Même dirigés l’un vers l’autre, ils n’atteignent pas la longueur de la base.','Les arcs restent séparés ; aucun point $C$ ne convient.'),Q(rf'Remplacer $AB$ par ${a+b-1}$ cm rend-il la construction possible ?','Tester les longueurs puis les arcs.','Comparer à la somme',rf'${a+b-1}<{a+b}$ ; les arcs peuvent se croiser.','Comparer à la différence',rf'${a+b-1}>|{a}-{b}|={abs(a-b)}$ ; aucun cercle n’est entièrement trop loin à l’intérieur de l’autre.','Oui ; deux intersections donnent deux triangles symétriques.')];tests=[f'{a}+{b}<{L}',f'abs({a}-{b})<{a+b-1}<{a}+{b}']
 elif k==2:
  L,a=[(6,5),(8,6),(10,7)][j];title=f'Construire un triangle isocèle de base {L} cm';intro=rf'$AB={L}$ cm et $AC=BC={a}$ cm. Construire $C$ au-dessus de la base.';image=fig(142,name,trianglefigure(L,a,a))
  rows=[Q('Préciser la nature du triangle et son sommet principal.','Repérer les côtés égaux.','Lire les égalités','$AC=BC$.','Repérer leur sommet commun','Les deux côtés égaux se rencontrent en $C$.','$ABC$ est isocèle en $C$.'),Q('Construire $C$.','Utiliser deux arcs de même rayon.','Ouvrir le compas',rf'Régler le rayon à ${a}$ cm ; tracer des arcs centrés en $A$ puis $B$.','Choisir et relier','Choisir l’intersection supérieure et tracer $[AC]$, $[BC]$.','La figure corrigée est le triangle demandé.'),Q('Pourquoi $C$ appartient-il à la médiatrice de $[AB]$ ?','Utiliser la propriété d’équidistance.','Comparer les distances',rf'$CA=CB={a}$ cm.','Appliquer la réciproque','Tout point à même distance de $A$ et $B$ appartient à leur médiatrice.','$C$ est sur la médiatrice de $[AB]$.')];tests=[f'2*{a}>{L}',f'{a}=={a}']
 elif k==3:
  L,alpha,beta=[(6,45,60),(5,50,70),(7,35,65)][j];gamma=180-alpha-beta;title=f'Construire avec un côté et deux angles : {alpha} et {beta} degrés';intro=rf'$AB={L}$ cm, $\widehat{{CAB}}={alpha}^\circ$ et $\widehat{{ABC}}={beta}^\circ$. Construire le triangle au-dessus de $(AB)$.';image=fig(142,name,asafigure(L,alpha,beta))
  rows=[Q('Calculer le troisième angle.','Utiliser la somme des angles du triangle.','Écrire la somme',rf'$\widehat{{ACB}}=180-({alpha}+{beta})$.','Calculer',rf'$180-{alpha+beta}={gamma}$.',rf'$\widehat{{ACB}}={gamma}^\circ$.'),Q('Décrire la construction de $C$.','Croiser deux directions issues des extrémités.','Tracer la base et le premier rayon',rf'Tracer $AB={L}$ cm puis, en $A$, un rayon formant ${alpha}^\circ$ avec $[AB)$.','Tracer le second rayon',rf'En $B$, partir de $[BA)$ vers le haut avec ${beta}^\circ$ ; l’intersection des rayons est $C$.','La figure corrigée représente la construction.'),Q('Quelle erreur faire en partant de $[AB)$ au lieu de $[BA)$ pour l’angle en $B$ ?','Identifier le sommet et le côté initial.','Revenir à la notation',r'$\widehat{ABC}$ a son sommet en $B$ et un côté dirigé vers $A$.','Corriger l’orientation','Le côté initial est $[BA)$, qui pointe vers la gauche sur le dessin.','Il faut aligner le zéro du rapporteur sur $[BA)$.')];tests=[f'{alpha}+{beta}+{gamma}==180']
 elif k==4:
  kind=['équilatéral','rectangle isocèle en A','isocèle en C'][j];alpha,beta=[(60,60),(90,45),(50,50)][j];gamma=180-alpha-beta
  title='Déduire les angles d’un triangle '+kind;intro=['Le triangle $ABC$ est équilatéral.','Le triangle $ABC$ est rectangle en $A$ et $AB=AC$.',r'Le triangle $ABC$ est isocèle en $C$ et $\widehat{CAB}=50^\circ$.'][j];image=fig(142,name,asafigure(5,alpha,beta))
  rows=[Q('Quelles égalités d’angles peut-on utiliser ?','Relier côtés égaux et angles opposés.','Identifier la nature',intro,'Écrire les angles égaux',[r'$\widehat A=\widehat B=\widehat C$.',r'$\widehat B=\widehat C$.',r'$\widehat A=\widehat B$.'][j],[r'Les trois angles sont égaux.',r'Les angles en $B$ et $C$ sont égaux.',r'Les angles en $A$ et $B$ sont égaux.'][j]),Q('Calculer les trois angles.',r'Répartir la somme de $180^\circ$.','Utiliser la somme',[r'$180\div3=60$.',r'$180-90=90$ pour les deux angles égaux.',r'$180-50-50=80$.'][j],'Terminer le calcul',[r'Chaque angle vaut $60^\circ$.',r'$90\div2=45^\circ$ pour chacun.',r'Le troisième angle est en $C$.'][j],rf'$\widehat A={alpha}^\circ$, $\widehat B={beta}^\circ$, $\widehat C={gamma}^\circ$.'),Q('Vérifier le résultat par la somme des angles.','Additionner toutes les mesures.','Calculer la somme',rf'${alpha}+{beta}+{gamma}=180$.','Comparer à la propriété','La somme est bien celle des angles d’un triangle.',r'Le résultat est cohérent : $180^\circ$.')];tests=[f'{alpha}+{beta}+{gamma}==180']
 elif k==5:
  L,a,b=[(6,4,5),(6,5,5),(5,3,4)][j];title=f'Tracer un cercle circonscrit : triangle {L}, {a}, {b}';intro=rf'Construire $ABC$ avec $AB={L}$ cm, $AC={a}$ cm, $BC={b}$ cm, puis son cercle circonscrit. $C$ est au-dessus de la base.';image=fig(142,name,trianglefigure(L,a,b,True))
  rows=[Q('Comment trouver le centre $O$ du cercle ?','Croiser deux médiatrices.','Construire deux droites','Tracer les médiatrices de $[AB]$ et $[AC]$.','Nommer l’intersection','Leur intersection est le point $O$.','$O$ est le centre cherché.'),Q('Justifier $OA=OB=OC$.','Utiliser deux fois la propriété de la médiatrice.','Première médiatrice','$O$ sur la médiatrice de $[AB]$ donne $OA=OB$.','Deuxième médiatrice','$O$ sur celle de $[AC]$ donne $OA=OC$.','$OA=OB=OC$.'),Q('Décrire le tracé final et sa vérification.','Choisir un centre et une seule ouverture.','Régler le rayon','Piquer le compas en $O$ et l’ouvrir jusqu’à $A$.','Tracer et contrôler','Tracer le cercle et vérifier qu’il passe aussi par $B$ et $C$.','Le cercle vert passe par les trois sommets.')];tests=[f'{a}+{b}>{L}']
 else:
  r=[3,4,5][j];title=f'Contrôler un centre proposé avec un rayon {r} cm';intro=rf'Pour un triangle non aplati $ABC$, un candidat $X$ vérifie $XA=XB={r}$ cm mais $XC={r+1}$ cm. Un autre candidat $O$ vérifie $OA=OB=OC={r+2}$ cm.'
  rows=[Q('$X$ peut-il être le centre du cercle circonscrit ?','Vérifier les trois distances.','Comparer les premières','$XA=XB$ signifie seulement que $X$ est sur la médiatrice de $[AB]$.','Comparer la troisième',rf'$XC={r+1}$ cm est différent de ${r}$ cm.','Non ; le même cercle ne passerait pas par les trois sommets.'),Q('$O$ est-il le bon centre ? Préciser le rayon.','Vérifier une ouverture commune.','Lire les trois distances',rf'$OA=OB=OC={r+2}$ cm.','Choisir le cercle',rf'Le cercle de centre $O$, rayon ${r+2}$ cm, contient les trois sommets.',rf'Oui, avec un rayon de ${r+2}$ cm.'),Q('Pourquoi deux médiatrices suffisent-elles pour construire ce centre ?','Relier les égalités de distances.','Première égalité','La médiatrice de $[AB]$ donne $OA=OB$.','Seconde égalité','Celle de $[AC]$ donne $OA=OC$ ; donc aussi $OB=OC$.','Leur intersection appartient également à la troisième médiatrice.')];tests=[f'{r}!={r+1}',f'{r+2}=={r+2}']
 add(142,eid,title,'easy' if k==4 else 'hard' if k==5 else 'medium',intro,rows,tests,image)

for i,eid in enumerate(ids_for(144)):
 k,j=divmod(i,3);L=[6,8,10][j];half=L/2;r=[5,5,7][j];image=None;tests=[f'{L}/2=={half}'];name=f'mediatrice_{k+1}_{j+1}'
 if k in (0,2,3,5):image=fig(144,name,mediatricefigure(L,r))
 if k==0:
  title=f'Construire à l’équerre : segment de {L} cm';intro=rf'Construire la médiatrice de $[AB]$ avec $AB={L}$ cm. La figure corrigée ajoute des points $P$ et $Q$ sur cette droite.'
  rows=[Q('Calculer la position du milieu $M$.','Partager la longueur en deux.','Utiliser la définition',r'$M\in[AB]$ et $AM=MB$.','Calculer',rf'$AM={L}\div2={fmt(half)}$ cm.',rf'$AM=MB={fmt(half)}$ cm.'),Q('Décrire la construction avec règle graduée et équerre.','Associer milieu et angle droit.','Placer le milieu',rf'Marquer $M$ à ${fmt(half)}$ cm de $A$ sur $[AB]$.','Tracer la perpendiculaire','Placer l’équerre sur $(AB)$, son angle droit en $M$, puis tracer.','La médiatrice est la droite verte perpendiculaire en $M$.'),Q('Quels codages ajouter ?','Rendre visibles les deux conditions.','Coder l’égalité','Mettre le même trait sur $[AM]$ et $[MB]$.','Coder l’angle droit','Ajouter un carré à l’intersection.','Deux moitiés égales et un angle droit en $M$.')]
 elif k==1:
  title=f'Déduire une distance à partir de {r} cm, segment {L}';intro=rf'$P$ appartient à la médiatrice de $[AB]$ et $PA={r}$ cm. $Q$ appartient aussi à cette médiatrice, avec $QA={r+1}$ cm.'
  rows=[Q('Calculer $PB$.','Appliquer la propriété d’équidistance.','Utiliser l’appartenance','$P$ sur la médiatrice donne $PA=PB$.','Reporter la donnée',rf'$PA={r}$ cm.',rf'$PB={r}$ cm.'),Q('Calculer $QB$.','Appliquer la même propriété à un autre point.','Écrire l’égalité','$QA=QB$.','Utiliser la longueur donnée',rf'$QA={r+1}$ cm.',rf'$QB={r+1}$ cm.'),Q('Peut-on conclure $PA=QA$ parce que $P$ et $Q$ sont sur la même médiatrice ?','Distinguer égalités au sein de chaque paire et entre points.','Comparer les données',rf'$PA={r}$ cm et $QA={r+1}$ cm.','Interpréter la propriété','Chaque point est à même distance de $A$ et de $B$, mais les distances varient le long de la droite.','Non ; les deux valeurs sont différentes.')];tests += [f'{r}!={r+1}']
 elif k==2:
  title=f'Construire la médiatrice au compas : {L} cm';intro=rf'$AB={L}$ cm. Utiliser une ouverture de compas de ${r}$ cm pour construire les intersections $P$, $Q$ puis la médiatrice.'
  rows=[Q('Cette ouverture est-elle suffisante ?','Comparer au demi-segment.','Calculer la moitié',rf'$AB/2={fmt(half)}$ cm.','Comparer',rf'${r}>{fmt(half)}$ ; les deux cercles se coupent en deux points.','Oui, l’ouverture est supérieure à la moitié de $AB$.'),Q('Rédiger les tracés au compas puis à la règle.','Garder une même ouverture pour les deux centres.','Tracer les arcs',rf'Tracer des arcs centrés en $A$ et $B$, de rayon ${r}$ cm, des deux côtés de $(AB)$.','Joindre les intersections','Nommer les intersections $P$ et $Q$, puis tracer $(PQ)$.','La droite $(PQ)$ est la médiatrice.'),Q('Justifier le tracé sans mesurer d’angle.','Utiliser l’équidistance de deux points.','Comparer les rayons',rf'$PA=PB={r}$ cm et $QA=QB={r}$ cm.','Conclure sur la droite','Les deux points distincts sont sur la médiatrice de $[AB]$ ; leur droite est cette médiatrice.','$(PQ)$ est la médiatrice de $[AB]$.')];tests += [f'{r}>{half}']
 elif k==3:
  title=f'Distinguer milieu et médiatrice pour {L} cm';intro=rf'$AB={L}$ cm, $M$ est son milieu et $P$ est un point de sa médiatrice avec $PA=PB={r}$ cm. $P$ n’est pas sur $(AB)$.'
  rows=[Q('Pourquoi $P$ n’est-il pas le milieu de $[AB]$ ?','Vérifier la position en plus des distances.','Lire l’hypothèse','$P$ n’est pas sur la droite $(AB)$.','Appliquer la définition du milieu','Un milieu doit appartenir au segment.','$P$ est sur la médiatrice, mais ce n’est pas le milieu.'),Q('Pourquoi $M$ est-il sur la médiatrice ?','Combiner les définitions.','Utiliser le milieu',rf'$MA=MB={fmt(half)}$ cm.','Appliquer la propriété réciproque','Un point équidistant des extrémités est sur la médiatrice.','$M$ appartient à la médiatrice.'),Q('Combien de points la médiatrice possède-t-elle ?','Distinguer une droite d’un point particulier.','Identifier l’objet','La médiatrice est une droite, pas le seul point $M$.','Prolonger','Elle se prolonge indéfiniment de part et d’autre de $M$.','Une infinité de points, dont un seul milieu de $[AB]$.')]
 elif k==4:
  title=f'Placer une borne équidistante de deux maisons : {L} cm';intro=rf'Les maisons $A$ et $B$ sont séparées de ${L}$ cm sur le plan. Une route $(r)$ coupe la médiatrice de $[AB]$ en un seul point $S$. On veut une borne sur la route à même distance des maisons.'
  z=mediatricefigure(L,r).replace(r'\end{tikzpicture}',r'\draw[geoTrait] (-2,-1)--(2,1);'+point(0,0,'S=M','south east','otGreenDark')+node(2,1,'(r)','west')+r'\end{tikzpicture}')
  # Le schéma choisi place la route par M ; ne pas superposer deux noms.
  z=z.replace(node(0,0,'M','north west','otGreenDark'),'')
  image=fig(144,name,z)
  rows=[Q('Quel ensemble contient tous les points équidistants des maisons ?','Traduire l’égalité de distances.','Écrire la condition','$XA=XB$.','Nommer le lieu','Cette égalité caractérise la médiatrice de $[AB]$.','La médiatrice de $[AB]$.'),Q('Décrire la construction de la borne.','Croiser les deux contraintes.','Construire le lieu','Construire la médiatrice de $[AB]$.','Respecter la route','Placer $S$ à son intersection avec $(r)$.','La borne se place en $S$.'),Q('Pourquoi y a-t-il une seule solution ?','Utiliser l’intersection donnée.','Vérifier les conditions','$S$ est sur la route et sur la médiatrice.','Compter les intersections','L’énoncé donne une seule intersection.','Un seul point satisfait les deux conditions.')]
 elif k==5:
  title=f'Imposer une distance en plus de l’équidistance : {r} cm, base {L}';intro=rf'$AB={L}$ cm. Chercher les points équidistants de $A$, $B$ et situés à ${r}$ cm de $A$. La figure corrigée montre les candidats $P$, $Q$.'
  rows=[Q('Quels deux objets faut-il croiser ?','Traduire chaque contrainte séparément.','Traduire l’équidistance','Les points doivent appartenir à la médiatrice de $[AB]$.','Traduire la distance fixe',rf'Ils doivent aussi appartenir au cercle de centre $A$, rayon ${r}$ cm.','La médiatrice et ce cercle.'),Q('Décrire les solutions et justifier leur distance à $B$.','Utiliser les intersections et la propriété.','Identifier les intersections','Le cercle coupe la médiatrice en $P$ et $Q$.','Appliquer l’équidistance',rf'$PB=PA={r}$ cm et $QB=QA={r}$ cm.','Les deux points $P$ et $Q$ conviennent.'),Q('Pourquoi le milieu ne convient-il pas ?','Comparer la distance au rayon imposé.','Calculer au milieu',rf'$MA={fmt(half)}$ cm.','Comparer à la contrainte',rf'${fmt(half)}\ne{r}$.','Le milieu est équidistant mais sa distance à $A$ est trop petite.')];tests += [f'{half}<{r}']
 else:
  title=f'Trier des distances candidates avec AB égal à {L} cm';intro=rf'$AB={L}$ cm. Des mesures exactes donnent $XA={r}$ cm, $XB={r+1}$ cm ; $YA=YB={r}$ cm ; $ZA=ZB={fmt(half)}$ cm.'
  rows=[Q('Le point $X$ est-il sur la médiatrice ?','Tester l’égalité des deux distances.','Lire les valeurs',rf'$XA={r}$ cm et $XB={r+1}$ cm.','Comparer','Les distances sont différentes.',r'Non ; $XA\ne XB$.'),Q('Que peut-on affirmer pour $Y$ ?','Utiliser la propriété réciproque.','Lire l’égalité',rf'$YA=YB={r}$ cm.','Conclure avec la propriété','Tout point à même distance des extrémités appartient à la médiatrice.','$Y$ est sur la médiatrice, sans être forcément le milieu.'),Q('Que représente $Z$ ?','Utiliser la moitié exacte de la distance entre les extrémités.','Additionner les distances',rf'$ZA+ZB={fmt(half)}+{fmt(half)}={L}$ cm, exactement $AB$.','Interpréter la position','Le trajet $A$–$Z$–$B$ atteint la distance directe : $Z$ est entre les extrémités, à leur moitié.','$Z$ est le milieu de $[AB]$.')];tests += [f'{r}!={r+1}',f'{half}+{half}=={L}']
 add(144,eid,title,'easy' if k==1 else 'hard' if k==5 else 'medium',intro,rows,tests,image)

def obliquefigure(x,y):
 lim=max(x,y)+1
 z=rf'\draw[step=1,otRule,thin] (0,0) grid ({lim},{lim});\draw[otOrange,thick] (-.2,-.2)--({lim+.2},{lim+.2});\draw[geoReponse] ({x},{y})--({y},{x});'
 z+=point(x,y,'P','south','otNavy')+point(y,x,"P'",'north','otGreenDark')+node(lim+.2,lim+.2,'(d)','south')
 return pic(z)
def circleimage(d,r):
 z=rf'\draw[otOrange,thick] (0,{-r-1})--(0,{r+1});\draw[geoTrait] ({d},0) circle ({r});\draw[geoReponse] ({-d},0) circle ({r});\draw[geoAide] ({-d},0)--({d},0);'
 z+=point(d,0,'O','south')+point(-d,0,"O'",'south','otGreenDark')+node(0,r+1,'(d)','south')
 return pic(z)

for i,eid in enumerate(ids_for(145)):
 k,j=divmod(i,3);d=[1,2,3][j];w=[2,3,2][j];h=[3,2,4][j];name=f'symetrie_{k+1}_{j+1}';image=None;tests=[]
 if k in (0,1,2):image=fig(145,name,symmetryfigure(d,w,h))
 if k==0:
  title=f'Placer l’image d’un point à {d} carreau(x) de l’axe';intro=rf'L’axe $(d)$ est vertical. Sur un quadrillage d’unité $1$ cm, $A$ se trouve à ${d}$ carreau(x) à droite de l’axe. Construire son image $A\prime$. La figure corrigée comporte aussi un rectangle pour contrôler les alignements.'
  rows=[Q(r'Où placer $A\prime$ ?','Compter perpendiculairement à l’axe.','Fixer la hauteur','L’image est sur la même ligne horizontale que $A$.','Reporter la distance',rf'Compter ${d}$ carreau(x) à gauche de l’axe.',rf'$A\prime$ est à ${d}$ carreau(x) de l’autre côté, à la même hauteur.'),Q(r'Calculer $AA\prime$.','Doubler la distance à l’axe.','Décomposer au pied',r'Le pied est le milieu de $[AA\prime]$.','Additionner',rf'${d}+{d}={2*d}$ cm.',rf'$AA\prime={2*d}$ cm.'),Q('Quelle propriété définit l’axe pour ce segment ?','Relier image et médiatrice.','Observer la perpendicularité',r'Le segment $[AA\prime]$ est horizontal et l’axe vertical.','Observer le milieu','Les deux côtés du pied ont la même longueur.',r'L’axe est la médiatrice de $[AA\prime]$.')];tests=[f'2*{d}=={2*d}']
 elif k==1:
  title=f'Reproduire un rectangle de {w} cm sur {h} cm';intro=rf'Sur un quadrillage de côté $1$ cm, $ABCD$ est un rectangle situé à droite de l’axe vertical : $A$ est à ${d}$ carreau(x) de l’axe, $AB={w}$ cm et $AD={h}$ cm. Construire son image.'
  rows=[Q('Construire les images des quatre sommets.','Reporter les distances sur des perpendiculaires.','Placer chaque image','Pour chaque sommet, rester sur sa ligne horizontale et compter autant de carreaux de l’autre côté.','Relier dans l’ordre',r'Relier $A\prime$, $B\prime$, $C\prime$, $D\prime$, puis revenir à $A\prime$.','Le rectangle vert est l’image demandée.'),Q('Donner les dimensions du rectangle image.','Utiliser la conservation des longueurs.','Associer les côtés',r'$[A\prime B\prime]$ est l’image de $[AB]$, et $[A\prime D\prime]$ celle de $[AD]$.','Conserver les mesures',rf'Les longueurs restent ${w}$ cm et ${h}$ cm.',rf'$A\prime B\prime={w}$ cm et $A\prime D\prime={h}$ cm.'),Q('Calculer son périmètre.','Utiliser les dimensions conservées.','Écrire le calcul',rf'$P=2\times({w}+{h})$.','Effectuer',rf'$P=2\times{w+h}={2*(w+h)}$ cm.',rf'Le périmètre vaut ${2*(w+h)}$ cm.')];tests=[f'2*({w}+{h})=={2*(w+h)}']
 elif k==2:
  title=f'Contrôler un point fixe et une image : distance {d}';intro=rf'La figure représente un rectangle et son image. On ajoute $H$, pied de la perpendiculaire de $A$ à l’axe vertical ; $AH={d}$ cm. $H$ appartient à l’axe.'
  image=fig(145,name,symmetryfigure(d,w,h).replace(r'\end{tikzpicture}',point(0,0,'H','north east')+r'\end{tikzpicture}'))
  rows=[Q('Quelle est l’image de $H$ ?','Reconnaître les points de l’axe.','Utiliser l’appartenance','$H$ est sur l’axe.','Appliquer la propriété','Un point de l’axe reste fixe.','L’image de $H$ est $H$.'),Q(r'Que donne une seconde symétrie de $A\prime$ par rapport au même axe ?','Revenir sur la même perpendiculaire.','Identifier le premier échange',r'$A$ et $A\prime$ sont à même distance, de part et d’autre.','Échanger à nouveau','Le second report ramène au point de départ.',r'L’image de $A\prime$ est $A$.'),Q('Pourquoi un point placé à droite de l’axe ne peut-il pas être sa propre image ?','Utiliser le milieu du segment d’images.','Observer sa distance','Un point hors de l’axe a une distance strictement positive à celui-ci.','Reporter de l’autre côté','Son image est distincte, dans l’autre demi-plan.','Seuls les points de l’axe sont fixes.')];tests=[f'{d}>0']
 elif k==3:
  x,y=[(1,3),(1,4),(2,4)][j];title=f'Construire avec un axe oblique : {x} et {y} carreaux';intro=rf'Un quadrillage carré est repéré par son coin inférieur gauche. L’axe est la diagonale montante du quadrillage. $P$ se trouve à ${x}$ carreau(x) vers la droite et ${y}$ vers le haut à partir de ce coin.';image=fig(145,name,obliquefigure(x,y))
  rows=[Q(r'Placer l’image $P\prime$ sur le quadrillage.','Utiliser le pliage suivant la diagonale.','Échanger les deux décomptes','Le pli échange la direction horizontale avec la direction verticale.','Placer le point',rf'Compter ${y}$ carreaux à droite et ${x}$ vers le haut.',rf'$P\prime$ est à ${y}$ carreaux à droite et ${x}$ vers le haut.'),Q(r'Dans quelle direction est le segment $[PP\prime]$ ?','Contrôler la perpendicularité.','Relier les deux points','Le segment descend vers la droite tandis que l’axe monte.','Vérifier à l’équerre','Les deux directions diagonales d’un carré sont perpendiculaires.',r'$[PP\prime]$ est perpendiculaire à l’axe.'),Q('Pourquoi garder la même hauteur serait-il une erreur ?','Tenir compte de l’orientation de l’axe.','Comparer les axes','Un report horizontal convient à un axe vertical.','Adapter à l’axe oblique','Ici il faut reporter sur une perpendiculaire oblique, pas horizontalement.','La même hauteur ne respecte pas la perpendicularité imposée.')];tests=[f'{x}!={y}',f'math.isclose(({x}-{y})+({y}-{x}),0)']
 elif k==4:
  a,b,c=[(3,4,5),(6,8,10),(9,12,15)][j];s=4/b
  z=rf'\begin{{scope}}[x={s}cm,y={s}cm]\draw[otOrange,thick] (0,-1)--(0,{b+1});\draw[geoTrait] (1,0)--({a+1},0)--(1,{b})--cycle;\draw[geoReponse] (-1,0)--({-a-1},0)--(-1,{b})--cycle;'
  for x,y,t,anc in [(1,0,'A','north'),(a+1,0,'B','north'),(1,b,'C','south')]:z+=point(x,y,t,anc)+point(-x,y,t+"'",anc,'otGreenDark')
  z+=r'\end{scope}'+caption(-.4,rf'$AB={a}$ cm ; $AC={b}$ cm ; $BC={c}$ cm')
  image=fig(145,name,pic(z));title=f'Utiliser les propriétés d’un triangle image : {a}, {b}, {c}';intro=rf'$ABC$ est rectangle en $A$, avec $AB={a}$ cm, $AC={b}$ cm et $BC={c}$ cm. Construire son image par rapport à l’axe vertical donné. Le dessin corrigé est réduit.'
  rows=[Q('Construire le triangle image.','Construire les trois points avant de relier.','Reporter les sommets','Tracer les perpendiculaires à l’axe et reporter les mêmes distances de l’autre côté.','Relier les images',r'Relier $A\prime$, $B\prime$, $C\prime$.','Le triangle vert est l’image de $ABC$.'),Q('Donner sa nature et ses trois longueurs.','Conserver les angles et les distances.','Conserver l’angle droit',r'L’angle en $A$ devient l’angle en $A\prime$.','Conserver les côtés',rf'Les trois longueurs restent ${a}$, ${b}$ et ${c}$ cm.',rf'Il est rectangle en $A\prime$ ; ses côtés mesurent ${a}$, ${b}$, ${c}$ cm.'),Q('Calculer son périmètre.','Additionner les longueurs conservées.','Écrire la somme',rf'$P={a}+{b}+{c}$.','Calculer',rf'$P={a+b+c}$ cm.',rf'Le périmètre vaut ${a+b+c}$ cm.')];tests=[f'{a}+{b}+{c}=={a+b+c}',f'{a}**2+{b}**2=={c}**2']
 elif k==5:
  rr=[1,1.5,2][j];image=fig(145,name,circleimage(d+1,rr));title=f'Tracer l’image d’un cercle de rayon {fmt(rr)} cm';intro=rf'Un cercle a pour centre $O$, situé à ${d+1}$ cm à droite d’un axe vertical, et pour rayon ${fmt(rr)}$ cm. Construire son image.'
  rows=[Q(r'Construire le centre image $O\prime$.','Construire d’abord l’image du centre.','Tracer une perpendiculaire','Tracer par $O$ une horizontale, perpendiculaire à l’axe.','Reporter la distance',rf'Placer $O\prime$ à ${d+1}$ cm à gauche de l’axe.',rf'$O\prime$ est à ${d+1}$ cm de l’axe, à la même hauteur.'),Q('Quel rayon utiliser pour le cercle image ?','Conserver les distances au centre.','Choisir un point du cercle','Sa distance au centre est le rayon.','Conserver cette distance',rf'Elle reste égale à ${fmt(rr)}$ cm après symétrie.',rf'Tracer le cercle de centre $O\prime$, rayon ${fmt(rr)}$ cm.'),Q('Calculer son diamètre.','Doubler le rayon.','Écrire le calcul',rf'$D=2\times {fmt(rr)}$.','Calculer',rf'$D={fmt(2*rr)}$ cm.',rf'Le diamètre vaut ${fmt(2*rr)}$ cm.')];tests=[f'2*{rr}=={2*rr}']
 else:
  kind=['rectangle non carré','carré','triangle isocèle non équilatéral'][j];count=[2,4,1][j];title='Chercher les axes d’un '+kind
  if j<2:
   ww,hh=[(5,3),(4,4)][j];z=rectfigure(ww,hh).replace(r'\end{tikzpicture}',rf'\draw[geoAide] ({ww/2},-.5)--({ww/2},{hh+.5}) (-.5,{hh/2})--({ww+.5},{hh/2});'+(rf'\draw[geoAide] (-.4,-.4)--({ww+.4},{hh+.4}) (-.4,{hh+.4})--({ww+.4},-.4);' if j==1 else '')+r'\end{tikzpicture}')
  else:z=trianglefigure(6,5,5).replace(r'\end{tikzpicture}',r'\draw[geoAide] (2.5,-.5)--(2.5,3.8);'+r'\end{tikzpicture}')
  image=fig(145,name,z);intro='On considère un '+kind+'. Les traits pointillés verts du corrigé sont les axes de symétrie.'
  rows=[Q('Donner le nombre d’axes de symétrie.','Chercher les pliages qui superposent toute la figure.','Identifier les échanges','Un axe doit échanger les côtés et les sommets sans déformer la figure.','Compter les directions',[r'Les deux médiatrices des côtés conviennent.',r'Les deux médiatrices des côtés et les deux diagonales conviennent.',r'La droite passant par le sommet principal et le milieu de la base convient.'][j],f'La figure possède {count} axe(s).'),Q('Décrire précisément ces axes.','Nommer chaque droite par sa construction.','Repérer les points fixes',[r'Les milieux de côtés opposés restent fixes.',r'Les milieux de côtés opposés ou deux sommets opposés restent fixes.',r'Le sommet principal et le milieu de la base restent fixes.'][j],'Tracer les droites',[r'Joindre les milieux de côtés opposés.',r'Joindre les milieux de côtés opposés, puis tracer les deux diagonales.',r'Joindre le sommet principal au milieu de la base.'][j],'Les droites vertes réalisent ces pliages.'),Q('Un axe doit-il passer par un sommet ?','Examiner les exemples.','Considérer les médiatrices des côtés','Dans un rectangle, elles passent par les milieux des côtés.','Comparer aux diagonales','Dans un carré, certains axes passent par des sommets, d’autres non.','Non ; un axe peut passer par des milieux de côtés.')];tests=[f'{count} in [1,2,4]']
 add(145,eid,title,'easy' if k==0 else 'hard' if k==3 else 'medium',intro,rows,tests,image)

def diamondfigure():
 return pic(r'\draw[geoReponse] (0,0)--(3,4)--(6,0)--(3,-4)--cycle;'+point(0,0,'A','east')+point(3,4,'B','south')+point(6,0,'C','west')+point(3,-4,'D','north'))
def trapfigure(right=False):
 pts=[(0,0),(5,0),(3,3),(0 if right else 1,3)]
 z='\\draw[geoReponse] '+ '--'.join(f'({x},{y})' for x,y in pts)+'--cycle;'
 for (x,y),t,anc in zip(pts,'ABCD',['north east','north west','south west','south east']):z+=point(x,y,t,anc)
 if right:z+=r'\draw[geoTrait] (.3,0)--(.3,.3)--(0,.3) (0,2.7)--(.3,2.7)--(.3,3);'
 return pic(z)

QUADS=[
('Classer une figure à quatre côtés égaux et quatre angles droits',r'Un quadrilatère possède quatre côtés de $4$ cm et quatre angles droits.',rectfigure(4,4),[
Q('Quel est son nom le plus précis ?','Croiser les deux propriétés.','Lire les longueurs','Les quatre côtés sont égaux.','Lire les angles','Les quatre angles sont droits.','C’est un carré.'),Q('Est-ce aussi un rectangle et un losange ?','Vérifier les définitions sans exclure les cas particuliers.','Tester rectangle','Il possède quatre angles droits.','Tester losange','Il possède quatre côtés égaux.','Oui, un carré est aussi un rectangle et un losange.'),Q('Calculer son périmètre.','Additionner quatre côtés égaux.','Écrire le produit',r'$P=4\times4$.','Calculer','$P=16$ cm.','$16$ cm.')],['4*4==16']),
('Construire un rectangle de 5 cm sur 3 cm',r'Construire un rectangle $ABCD$ avec $AB=5$ cm et $AD=3$ cm, $D$ au-dessus de $(AB)$.',rectfigure(5,3),[
Q('Comment commencer la construction ?','Fixer une base et un angle droit.','Tracer la base','Tracer $[AB]$ de $5$ cm.','Tracer la première perpendiculaire','En $A$, tracer la perpendiculaire à $(AB)$ vers le haut.','La base et la direction de $[AD]$ sont fixées.'),Q('Placer $C$ et $D$ puis terminer.','Utiliser la même distance sur deux perpendiculaires.','Reporter les hauteurs','Placer $D$ à $3$ cm de $A$ et $C$ à $3$ cm de $B$, sur les perpendiculaires du même côté.','Fermer et contrôler','Relier $C$ à $D$ ; vérifier les quatre angles droits.','La figure verte est le rectangle demandé.'),Q('Quelles longueurs doivent avoir $BC$ et $CD$ ?','Utiliser les côtés opposés du rectangle.','Associer les côtés','$BC=AD$ et $CD=AB$.','Reporter les données','$AD=3$ cm ; $AB=5$ cm.','$BC=3$ cm et $CD=5$ cm.')],['5==5','3==3']),
('Construire un carré de côté 3 cm',r'Construire un carré $ABCD$ de côté $3$ cm au-dessus de la base $[AB]$.',rectfigure(3,3),[
Q('Quelle longueur choisir pour $AD$ et $BC$ ?','Utiliser l’égalité des quatre côtés.','Fixer la base','$AB=3$ cm.','Reporter le même côté','$AD=BC=3$ cm.','Les deux côtés mesurent $3$ cm.'),Q('Décrire la construction complète.','Construire un rectangle dont tous les côtés sont égaux.','Tracer base et perpendiculaires','Tracer $AB=3$ cm puis les perpendiculaires en $A$ et $B$, vers le haut.','Reporter et fermer','Placer $D$ et $C$ à $3$ cm sur ces droites, puis relier $C$ à $D$.','On obtient quatre côtés égaux et quatre angles droits.'),Q('Calculer son périmètre et son aire.','Distinguer longueur du contour et surface.','Calculer le contour',r'$P=4\times3=12$ cm.','Calculer la surface',r'$\mathcal A=3\times3=9$ cm².','Périmètre : $12$ cm ; aire : $9$ cm².')],['4*3==12','3*3==9']),
('Construire un losange à partir d’une diagonale',r'Construire un losange $ABCD$ tel que $AC=6$ cm et chaque côté mesure $5$ cm. $B$ et $D$ sont de part et d’autre de $(AC)$.',diamondfigure(),[
Q('Comment placer les deux sommets manquants ?','Croiser deux cercles de même rayon.','Tracer les données','Tracer $AC=6$ cm puis deux cercles de centres $A$, $C$, rayon $5$ cm.','Nommer les intersections','Nommer $B$ celle du haut, $D$ celle du bas, puis relier dans l’ordre $A,B,C,D$.','Les quatre côtés mesurent $5$ cm.'),Q('Pourquoi la figure est-elle un losange ?','Lire les rayons de construction.','Premiers côtés','$AB=AD=5$ cm car $B$ et $D$ sont sur le cercle de centre $A$.','Autres côtés','$CB=CD=5$ cm car ils sont aussi sur le cercle de centre $C$.','Les quatre côtés sont égaux : c’est un losange.'),Q('Calculer le périmètre.','Additionner quatre côtés égaux.','Écrire le produit',r'$P=4\times5$.','Calculer','$P=20$ cm.','$20$ cm.')],['math.hypot(3,4)==5','4*5==20']),
('Décrire un trapèze',r'Construire $ABCD$ ainsi : $AB=5$ cm horizontal ; $D$ est à $1$ cm à droite et $3$ cm au-dessus de $A$ ; $C$ est à $3$ cm à droite et $3$ cm au-dessus de $A$.',trapfigure(),[
Q('Décrire le placement des sommets.','Utiliser une grille ou des perpendiculaires graduées.','Placer la base','Tracer $[AB]$ de $5$ cm horizontalement.','Placer les sommets du haut','Reporter les deux déplacements indiqués et relier $A,B,C,D$.','La figure verte donne le quadrilatère demandé.'),Q('Quelles droites sont parallèles ?','Comparer les hauteurs.','Observer les deux sommets supérieurs','$C$ et $D$ sont à la même hauteur de $3$ cm.','Comparer les directions','$[CD]$ est horizontal comme $[AB]$.',r'$(AB)\parallel(CD)$.'),Q('Pourquoi peut-on appeler ce quadrilatère un trapèze ?','Vérifier une paire de côtés opposés parallèles.','Repérer les côtés opposés','$[AB]$ et $[CD]$ ne sont pas consécutifs.','Utiliser le parallélisme','Leurs droites sont parallèles.','Il possède deux côtés opposés parallèles : c’est un trapèze.')],['3==3','3-1==2']),
('Construire un trapèze rectangle',r'Tracer $AB=5$ cm horizontal, $AD=3$ cm perpendiculaire à $(AB)$ vers le haut, puis $DC=3$ cm parallèle à $[AB]$ vers la droite. Relier $C$ à $B$.',trapfigure(True),[
Q('Réaliser le programme de construction.','Suivre les directions dans l’ordre.','Tracer les deux premiers côtés','Tracer $AB=5$ cm puis $AD=3$ cm avec l’équerre.','Tracer le haut puis fermer','Par $D$, tracer la parallèle à $(AB)$, placer $C$ à $3$ cm de $D$, puis relier à $B$.','La figure verte est la construction attendue.'),Q('Nommer les deux angles droits.','Lire les perpendicularités.','Premier angle',r'$(AD)\perp(AB)$ donne un angle droit en $A$.','Second angle',r'$(DC)\parallel(AB)$ et $(AD)\perp(AB)$ donnent un angle droit en $D$.',r'$\widehat{DAB}=\widehat{ADC}=90^\circ$.'),Q('Est-ce un rectangle ?','Vérifier les quatre angles, pas seulement deux.','Comparer les bases','$AB=5$ cm mais $DC=3$ cm.','Utiliser les propriétés du rectangle','Dans un rectangle, les côtés opposés ont même longueur.','Non ; c’est un trapèze rectangle.')],['5!=3']),
('Comparer deux périmètres',r'Un rectangle mesure $5$ cm sur $3$ cm. Un carré a pour côté $4$ cm.',rectfigure(5,3),[
Q('Calculer le périmètre du rectangle.','Additionner ses quatre côtés.','Regrouper les côtés opposés',r'$P=2\times(5+3)$.','Calculer','$P=16$ cm.','$16$ cm.'),Q('Calculer le périmètre du carré.','Multiplier un côté par quatre.','Écrire la formule',r'$P=4\times4$.','Calculer','$P=16$ cm.','$16$ cm.'),Q('Ces figures ont-elles nécessairement la même forme ?','Distinguer une mesure d’une forme.','Comparer les périmètres','Ils sont égaux à $16$ cm.','Comparer les côtés','Le rectangle a deux longueurs de côtés différentes ; le carré n’en a qu’une.','Non ; un même périmètre ne détermine pas une forme unique.')],['2*(5+3)==16','4*4==16']),
('Retrouver une largeur manquante',r'Un rectangle $ABCD$ a pour périmètre $22$ cm et $AB=7$ cm. Chercher $AD$.',rectfigure(7,4),[
Q('Calculer la somme $AB+AD$.','Partager le périmètre en deux paires égales.','Écrire la relation',r'$P=2\times(AB+AD)$.','Diviser par deux',r'$AB+AD=22\div2=11$ cm.','$AB+AD=11$ cm.'),Q('Calculer $AD$.','Retirer la longueur connue.','Écrire la différence','$AD=11-7$.','Calculer','$AD=4$ cm.','$AD=4$ cm.'),Q('Vérifier le périmètre trouvé.','Recalculer avec les dimensions obtenues.','Additionner une paire','$7+4=11$ cm.','Doubler',r'$2\times11=22$ cm.','Le périmètre est bien $22$ cm.')],['22/2==11','11-7==4','2*(7+4)==22']),
('Nommer côtés et diagonales',r'Les sommets du rectangle $ABCD$ sont nommés dans l’ordre du contour. Utiliser le schéma du corrigé pour contrôler les notations.',rectfigure(5,3),[
Q('Lister les côtés du quadrilatère.','Joindre des sommets consécutifs.','Suivre le contour',r'$A\to B\to C\to D\to A$.','Écrire les segments','Chaque passage joint deux voisins.','$[AB]$, $[BC]$, $[CD]$, $[DA]$.'),Q('Nommer les deux diagonales.','Joindre les sommets non consécutifs.','Partir de $A$','Son sommet opposé est $C$.','Partir de $B$','Son sommet opposé est $D$.','$[AC]$ et $[BD]$.'),Q('$[AD]$ est-il une diagonale ?','Vérifier le caractère consécutif.','Lire le retour du contour','$D$ est le voisin de $A$ lors de la fermeture.','Classer le segment','Il fait partie du contour.','Non ; $[AD]$ est un côté.')],['True']),
('Ne pas confondre aire et périmètre',r'Un carré a pour côté $3$ cm. On colle des petits carrés de côté $1$ cm pour le couvrir sans dépasser.',rectfigure(3,3),[
Q('Combien de petits carrés faut-il ?','Compter lignes et colonnes.','Compter une ligne','Il y a $3$ petits carrés par ligne.','Compter les lignes',r'$3$ lignes donnent $3\times3=9$.','Il faut $9$ petits carrés.'),Q('Donner l’aire avec son unité.','Mesurer une surface.','Utiliser le pavage','Chaque petit carré représente $1$ cm².','Additionner les unités d’aire',r'$9\times1=9$ cm².','L’aire est $9$ cm².'),Q('Calculer la longueur d’un ruban qui suit le contour.','Mesurer la frontière.','Compter les quatre côtés','Chacun mesure $3$ cm.','Additionner','$3+3+3+3=12$ cm.','Le ruban doit mesurer $12$ cm.')],['3*3==9','4*3==12']),
('Un losange est-il forcément un carré ?',r'On construit $ABCD$ avec $AC=6$ cm et $AB=BC=CD=DA=5$ cm, $B$ et $D$ de part et d’autre de $(AC)$.',diamondfigure(),[
Q('Quel nom est garanti par les données ?','Utiliser les longueurs des quatre côtés.','Comparer les côtés','Les quatre mesurent $5$ cm.','Appliquer la définition','Un quadrilatère à quatre côtés égaux est un losange.','La figure est un losange.'),Q('Les longueurs seules prouvent-elles que les quatre angles sont droits ?','Distinguer égalité et perpendicularité.','Relever ce qui est connu','Les quatre côtés sont égaux.','Identifier la condition manquante','Aucune donnée ne donne quatre angles droits.','Non ; il faut vérifier les angles pour conclure carré.'),Q('Quel contrôle permet de distinguer le dessin d’un carré ?','Utiliser l’équerre.','Placer l’outil','Placer les côtés de l’équerre sur deux côtés consécutifs.','Comparer l’ouverture','Sur cette construction, les côtés ne forment pas un angle droit.','L’absence d’angle droit montre que ce losange n’est pas un carré.')],['math.isclose(math.hypot(3,4),5)','3*3-4*4!=0']),
('Corriger un programme de rectangle',r'Un programme annonce : « Tracer $AB=6$ cm ; tracer $AD=3$ cm et $BC=3$ cm perpendiculaires à $(AB)$ du même côté ; relier $D$ à $C$ et écrire $DC=5$ cm. »',rectfigure(6,3),[
Q('Quelle donnée finale est erronée ?','Utiliser les côtés opposés du rectangle construit.','Identifier les côtés opposés','$[DC]$ est opposé à $[AB]$.','Reporter la bonne longueur','$DC=AB=6$ cm.','Il faut écrire $DC=6$ cm, pas $5$ cm.'),Q('Pourquoi les hauteurs doivent-elles être placées du même côté de $(AB)$ ?','Suivre l’ordre des sommets.','Respecter la forme','Le rectangle se ferme au-dessus ou au-dessous de sa base.','Éviter un croisement','Placer les sommets de part et d’autre ne donne pas le rectangle annoncé dans cet ordre.','Les deux perpendiculaires doivent être parcourues du même côté.'),Q('Calculer le périmètre correct.','Utiliser les dimensions de la construction.','Regrouper',r'$P=2\times(6+3)$.','Calculer','$P=18$ cm.','$18$ cm.')],['6!=5','2*(6+3)==18'])]
for i,(title,intro,code,rows,tests) in enumerate(QUADS,1):
 image=fig(143,f'quadrilatere_{i:02}',code)
 add(143,f'nouveau-{i}',title,'easy' if i in (1,7,9,10) else 'medium',intro,rows,tests,image)

def generate():
 course_figs={140:['objets','cercle'],141:['cours_secantes','angle_4_2'],142:['triangle_1_1','triangle_6_1'],143:['quadrilatere_09','quadrilatere_02'],144:['mediatrice_3_1','mediatrice_2_cours'],145:['symetrie_1_1','symetrie_2_1']}
 fig(141,'cours_secantes',secants(65));fig(144,'mediatrice_2_cours',mediatricefigure(6,5))
 for n in range(140,146):
  folder=next(BASE.glob(str(n)+'_*'));meta=json.loads((folder/'source_en_ligne/meta.json').read_text(encoding='utf-8'));fdir=folder/'figures';fdir.mkdir(exist_ok=True)
  courseid=str(meta['cours'][0]['id']) if meta['cours'] else 'nouveau';ficheid=str(meta['fiches'][0]['id']) if meta['fiches'] else 'nouvelle'
  corr={'cours':{courseid:{}},'fiches':{},'exercices':{}}
  for pos,name in enumerate(course_figs[n],1):corr['cours'][courseid][str(pos)]={'fichier':name+'.png','alt':f'Géométrie de sixième : {meta["titre"]}, construction précise et annotations lisibles, figure {pos}.'}
  for genre,key,text in [('cours',courseid,COURSES[n]),('fiche',ficheid,FICHES[n])]:
   (folder/f'{genre}_{key}.txt').write_text('Titre: '+meta['titre']+'\n<!-- optitab:1 -->\n'+text.strip()+'\n',encoding='utf-8')
  parts=[]
  for e in EXERCISES[n]:
   eid=e['id'];image=e['figure'];qs=e['questions'];assert len(qs)==3
   enonce='<!-- optitab:1 -->\n'+e['intro']+'\n\n'
   if n==140 and eid in ids_for(140)[:3] or n==141 and eid in ids_for(141)[3:6]:enonce+='[IMAGE_1]\n\n'
   enonce+='\n'.join(f'{i}. {row[0]}' for i,row in enumerate(qs,1))
   steps='<!-- optitab:1 -->\n'
   for i,(question,method,one,two,result) in enumerate(qs,1):
    steps+=f'\n## Question {i} : '+question+'\n\n'+box('methode',method)+box('etape',one[1],one[0])+box('etape',two[1],two[0])+box('resultat',result)
   if image:
    steps+='\n### Figure de contrôle\n\n[IMAGE_1]\n\nLe tracé vert montre les éléments construits ou la figure obtenue. Les dessins peuvent être réduits ; utiliser les données écrites pour construire sur papier.\n'
    corr['exercices'][str(eid)]={'1':{'fichier':image+'.png','alt':e['titre']+' : configuration exacte des points et éléments de réponse en vert.'}}
   warning={140:'Distinguer l’objet géométrique de sa mesure ; une impression visuelle ne remplace pas une donnée ou une construction.',141:'Toujours identifier le sommet et le côté de départ. L’ouverture de l’angle ne dépend pas de la longueur des traits.',142:'Contrôler les trois côtés ou les angles imposés. Un dessin convaincant ne suffit pas à justifier une propriété.',143:'Un nom de figure exige toutes ses conditions. Un côté égal ne garantit pas un angle droit.',144:'La médiatrice est une droite ; le milieu est un point. L’égalité des distances et l’appartenance se lisent dans les deux sens.',145:'Reporter perpendiculairement à l’axe, à la même distance de l’autre côté. Un point situé sur l’axe reste fixe.'}[n]
   steps+='\n'+box('attention',warning)
   solution='<!-- optitab:1 -->\n'+ '\n'.join(f'{i}. {row[-1]}' for i,row in enumerate(qs,1))
   prefix={'easy':'Découverte','medium':'Entraînement','hard':'Approfondissement'}[e['difficulte']]
   parts.append(f'{prefix} — {e["titre"]}\nId: {eid}\nDifficulté: {e["difficulte"]}\n'+('Image: '+image+'.png\n' if image else '')+'\nÉnoncé:\n'+enonce+'\n\nÉtapes:\n'+steps+'\nSolution:\n'+solution)
  (folder/'exercices.txt').write_text('=== '+('\n\n===\n\n'.join(parts))+'\n',encoding='utf-8')
  used={Path(v['fichier']).stem for genre in corr.values() for obj in genre.values() for v in obj.values()}
  selected={k:v for k,v in FIGURES[n].items() if k in used};assert used==set(selected),(n,used-set(selected))
  (fdir/'figures.py').write_text('# -*- coding: utf-8 -*-\n# Figures TikZ exactes ; unités identiques sur les deux directions.\nFIGURES = '+repr(selected)+'\n',encoding='utf-8')
  (fdir/'correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  sourcehash={str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (folder/'source_en_ligne').rglob('*') if p.is_file()}
  manifest={'notion':n,'programme':PROGRAMME,'source_hashes':sourcehash,'checks':CHECKS[n],'question_count':len(EXERCISES[n])*3,'figures':sorted(selected)}
  (folder/'verification_math.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  (folder/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'geometrie','maj':'2026-10-30','phase':'rédaction achevée, contrôles et relecture en cours'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print(n,len(EXERCISES[n]),'exercices,',len(selected),'figures')

f140={
'objets':pic(r'''\draw[geoTrait] (-.7,2)--(5.7,2);\draw[geoReponse] (0,0)--(5,0);\draw[geoTrait,-{Stealth}] (0,-2)--(5.7,-2);'''+''.join(point(x,y,t,'south') for x,y,t in [(0,2,'A'),(5,2,'B'),(0,0,'C'),(5,0,'D'),(0,-2,'E'),(5,-2,'F')])),
'segment':segment(),
'droites':pic(r'''\draw[geoTrait] (-.7,0)--(5.7,0) (-.7,2)--(5.7,2);\draw[geoReponse] (2,-1)--(2,3);\draw[geoReponse] (2,.3)--(2.3,.3)--(2.3,0);\draw[geoReponse] (2,2.3)--(2.3,2.3)--(2.3,2);'''+node(5.7,0,'(d)','west')+node(5.7,2,'(e)','west')+node(2,3,'(f)','south')+point(2,0,'A','north east')+point(2,2,'B','south east')),
'trajet':pic(r'''\draw[geoTrait] (0,0)--(5,0);\draw[geoReponse] (0,0)--(1.8,2.4)--(5,0);'''+point(0,0,'A','north east')+point(5,0,'B','north west')+point(1.8,2.4,'C','south')+node(.5,1.4,'3\;\mathrm{cm}','east')+node(3.7,1.5,'4\;\mathrm{cm}','west')+node(2.5,-.15,'5\;\mathrm{cm}','north')),
'milieu':segment(8),
'cercle':circlefigure(),
'contraintes':mediatricefigure(6,5)}
for name,code in f140.items():fig(140,name,code)

family(140,0,['Lire les trois objets','Choisir une notation','Corriger un message géométrique'],
r'La figure distingue trois objets : la première ligne se prolonge sans limite des deux côtés ; la deuxième s’arrête en $C$ et $D$ ; la troisième commence en $E$ et se prolonge au-delà de $F$.',[
Q('Nommer le premier objet.','Repérer les prolongements.','Deux directions illimitées','La ligne traverse $A$ et $B$ et continue des deux côtés.','Écrire avec des parenthèses','Une droite se note avec deux parenthèses.','La droite $(AB)$.'),
Q('Nommer le deuxième objet.','Chercher les deux extrémités.','Deux arrêts','Le tracé s’arrête en $C$ et en $D$.','Écrire avec des crochets','Le segment comprend ses deux extrémités.','Le segment $[CD]$.'),
Q('Nommer le troisième objet.','Identifier l’origine et le sens.','Une origine','Le tracé commence en $E$ et passe par $F$.','Ouvrir du côté prolongé','Le crochet est du côté de l’origine.','La demi-droite $[EF)$.'),
Q('Laquelle de ces notations désigne une longueur : $CD$, $[CD]$, $(CD)$ ?','Distinguer nombre et objet.','Lire les signes','Les crochets et parenthèses désignent des ensembles de points.','Isoler la mesure','$CD$ est la distance entre les deux points.','$CD$ désigne une longueur.'),
Q('Peut-on remplacer $(AB)$ par $(BA)$ ?','Comparer les ensembles de points.','Inverser les noms','Les deux écritures désignent la droite passant par les mêmes points.','Vérifier les directions','Les deux côtés restent illimités.','Oui : $(AB)=(BA)$.'),
Q('Peut-on remplacer $[EF)$ par $[FE)$ ?','Comparer les origines.','Identifier le départ','$[EF)$ commence en $E$ ; $[FE)$ commence en $F$.','Comparer les prolongements','Les deux demi-droites partent dans des directions opposées.','Non : les demi-droites sont différentes.'),
Q('Corriger « $[CD]=5$ cm ».','Réserver la mesure à la longueur.','Repérer l’erreur','$[CD]$ est un segment, pas un nombre.','Retirer les crochets','La longueur du segment se note $CD$.','On écrit $CD=5$ cm.'),
Q('Un élève dit : « Une droite possède deux extrémités. » Corriger.','Revenir à la définition.','Repérer le caractère illimité','Une droite se prolonge des deux côtés.','Nommer le bon objet','C’est un segment qui a deux extrémités.','Une droite n’a pas d’extrémité.'),
Q('Pourquoi le dessin ne montre-t-il jamais toute une droite ?','Distinguer dessin et objet.','Observer la feuille','La feuille et l’écran ont une taille limitée.','Interpréter la convention','Un trait limité représente un objet illimité lorsque l’énoncé le précise.','La droite est illimitée ; le dessin ne l’est pas.')], 'objets',['True'])

family(140,1,['Lire un alignement','Comparer des segments','Rédiger un placement'],r'$A$, $M$ et $B$ sont alignés dans cet ordre. On donne $AB=6$ cm et $AM=3$ cm. La figure corrigée code les longueurs égales.',[
Q('Calculer $MB$.','Soustraire la partie connue du tout.','Décomposer le segment','$AB=AM+MB$.','Calculer la partie restante','$MB=6-3=3$ cm.','$MB=3$ cm.'),
Q('Le point $M$ est-il le milieu de $[AB]$ ?','Vérifier les deux conditions.','Contrôler la position','$M$ appartient au segment $[AB]$.','Comparer les distances','$AM=MB=3$ cm.','Oui, $M$ est le milieu de $[AB]$.'),
Q(r'Quelles notations conviennent : $M\in[AB]$, $M\in(AB)$ ?','Comparer segment et droite.','Lire l’ordre des points','$M$ est entre $A$ et $B$.','Utiliser l’inclusion','Le segment est une partie de la droite.','Les deux notations conviennent.'),
Q('Comparer $AM$ et $AB$.','Une partie est plus courte que le segment complet.','Lire les valeurs','$AM=3$ cm et $AB=6$ cm.','Comparer les nombres','$3<6$.','$AM<AB$.'),
Q('Que désigne $[AM]$ ?','Décrire un objet par ses extrémités.','Lire les crochets','Les deux crochets indiquent un segment.','Nommer les extrémités','Il commence en $A$ et s’arrête en $M$.','Le segment d’extrémités $A$ et $M$.'),
Q('Un point $N$ de la droite vérifie $AN=9$ cm. Est-il forcément dans $[AB]$ ?','Comparer à la longueur du segment.','Encadrer les distances sur le segment',r'Pour $N\in[AB]$, on aurait $AN\leq6$ cm.','Confronter la donnée','$9>6$.','Non ; il est forcément hors du segment.'),
Q('Décrire comment construire cette figure à la règle graduée.','Tracer le tout puis placer le milieu.','Tracer $[AB]$','Tracer un segment de longueur $6$ cm.','Placer $M$','Marquer $M$ à $3$ cm de $A$, sur le segment.','On obtient $AM=MB=3$ cm.'),
Q('Comment vérifier le placement de $M$ ?','Contrôler position et longueurs.','Vérifier l’alignement','Placer le bord de la règle sur $A$ et $B$ : $M$ doit être dessus.','Mesurer les deux parties','Lire $3$ cm pour chaque partie.',r'Vérifier $M\in[AB]$ et $AM=MB$.'),
Q('Peut-on déduire le milieu d’un segment à partir d’une simple impression visuelle ?','Séparer observation et preuve.','Observer la limite du dessin','Un dessin peut être imprécis ou réduit.','Exiger une donnée','Utiliser une mesure ou un codage d’égalité.','Non ; il faut vérifier les deux conditions.')], 'segment',['6-3==3','3+3==6'])

family(140,2,['Identifier des droites particulières','Construire avec l’équerre','Justifier des positions de droites'],r'La figure donne $(d)\perp(f)$ en $A$ et $(e)\perp(f)$ en $B$, avec $A\ne B$. Les petits carrés codent les angles droits.',[
Q('Nommer les droites perpendiculaires en $A$.','Lire le carré d’angle droit.','Repérer le sommet','Le carré est placé à l’intersection en $A$.','Nommer les droites','Ses côtés suivent $(d)$ et $(f)$.',r'$(d)\perp(f)$.'),
Q('Quel est le point commun de $(e)$ et $(f)$ ?','Lire l’intersection.','Repérer le croisement','Les deux droites se coupent au point nommé $B$.','Écrire l’intersection','Le point est sur les deux droites.','Le point $B$.'),
Q('Quelle est la mesure de l’angle codé en $B$ ?','Reconnaître le codage.','Lire le petit carré','Il désigne un angle droit.','Associer la mesure',r'Un angle droit mesure $90^\circ$.',r'$90^\circ$.'),
Q('Décrire le tracé de $(f)$ perpendiculaire à $(d)$ passant par $A$.','Utiliser les côtés de l’angle droit de l’équerre.','Aligner l’outil','Placer un côté de l’équerre sur $(d)$, son sommet en $A$.','Tracer et coder','Tracer le long de l’autre côté et ajouter le carré.','$(f)$ passe par $A$ et forme un angle droit avec $(d)$.'),
Q('Comment tracer par $B$ une perpendiculaire à $(f)$ ?','Faire glisser l’équerre sans la tourner.','Positionner l’équerre','Placer un côté sur $(f)$, puis faire glisser jusqu’à $B$.','Tracer l’autre côté','Le second côté donne la droite voulue.','La droite obtenue est $(e)$.'),
Q('Pourquoi une règle seule ne garantit-elle pas un angle droit ?','Distinguer alignement et perpendicularité.','Fonction de la règle','Son bord permet de tracer droit.','Contrôle de l’angle','L’angle droit doit être construit avec une équerre ou un autre procédé justifié.',r'Le tracé droit ne suffit pas à garantir $90^\circ$.'),
Q('Comparer la direction de $(d)$ et de $(e)$.','Utiliser la perpendicularité à une même droite.','Relever les deux angles droits','$(d)$ et $(e)$ sont perpendiculaires à $(f)$.','Appliquer la propriété','Deux droites distinctes perpendiculaires à une même droite sont parallèles.',r'$(d)\parallel(e)$.'),
Q('Les droites $(d)$ et $(e)$ peuvent-elles se rencontrer sur la feuille prolongée ?','Utiliser le sens de parallèle.','Identifier leur position','Elles sont distinctes et parallèles.','Prolonger mentalement','Leur direction reste la même, quel que soit le prolongement.','Non ; elles n’ont aucun point commun.'),
Q('Le fait de ne pas voir d’intersection suffit-il à prouver le parallélisme ?','Distinguer absence visible et propriété.','Limiter l’observation','Une intersection peut être hors de la feuille.','Chercher une preuve','Ici, les deux codages d’angles droits permettent la conclusion.','Non ; il faut une propriété ou une construction contrôlée.')], 'droites',['90==90'])

family(140,3,['Comparer deux itinéraires','Prévoir un aller-retour','Interpréter la distance'],r'Un trajet direct suit $[AB]$ : $AB=5$ cm sur un plan. Un autre passe par $C$ : $AC=3$ cm et $CB=4$ cm. Toutes les réponses concernent les longueurs sur ce plan.',[
Q('Calculer la longueur du trajet par $C$.','Additionner les deux portions.','Identifier les portions','$AC=3$ cm et $CB=4$ cm.','Faire la somme','$3+4=7$ cm.','Le trajet par $C$ mesure $7$ cm.'),
Q('Quel trajet est le plus court ?','Comparer les longueurs totales.','Relever les longueurs','Le trajet direct mesure $5$ cm ; celui par $C$ mesure $7$ cm.','Comparer','$5<7$.','Le trajet direct est plus court.'),
Q('Quelle longueur supplémentaire représente le passage par $C$ ?','Calculer un écart.','Choisir la soustraction','Retirer la longueur directe de celle du détour.','Calculer','$7-5=2$ cm.','Le détour ajoute $2$ cm.'),
Q('Calculer l’aller-retour direct.','Doubler la distance aller.','Identifier les deux parties','Aller et retour mesurent chacun $5$ cm.','Additionner','$5+5=10$ cm.','$10$ cm sur le plan.'),
Q('Calculer un aller par $C$ et un retour direct.','Additionner des trajets différents.','Relever chaque longueur','Aller : $7$ cm ; retour : $5$ cm.','Calculer','$7+5=12$ cm.','$12$ cm sur le plan.'),
Q('Comparer deux allers-retours, l’un direct, l’autre par $C$.','Comparer les sommes complètes.','Calculer les totaux',r'Direct : $2\times5=10$ cm ; détour : $2\times7=14$ cm.','Calculer l’écart','$14-10=4$ cm.','L’aller-retour par $C$ ajoute $4$ cm.'),
Q('Quelle est la distance entre les points $A$ et $B$ ?','Utiliser la définition de distance.','Choisir le segment','La distance est la longueur de $[AB]$, pas celle d’une ligne brisée.','Lire la donnée','$AB=5$ cm.','La distance est $5$ cm.'),
Q('Peut-on écrire $AB=AC+CB$ ici ?','Vérifier la position et les valeurs.','Comparer les calculs','$AB=5$ cm, mais $AC+CB=7$ cm.','Examiner le point $C$','$C$ n’est pas entre $A$ et $B$ sur la même droite.',r'Non : $5\ne7$.'),
Q('Un élève donne la distance réelle en ville en lisant $5$ cm. Pourquoi est-ce insuffisant ?','Distinguer plan et réalité.','Repérer l’unité donnée','Les centimètres mesurent le dessin.','Chercher l’information manquante','Il faudrait connaître l’échelle du plan.','La distance réelle ne peut pas être calculée sans échelle.')], 'trajet',['3+4==7','7-5==2','2*5==10','7+5==12','2*7-2*5==4','5!=3+4'])

family(140,4,['Partager un segment','Contrôler un milieu','Utiliser une distance double'],r'On considère un segment $[AB]$ de longueur $8$ cm. $M$ désigne son milieu. Le dessin corrigé n’est pas un gabarit à mesurer.',[
Q('Calculer $AM$.','Partager la longueur en deux parts égales.','Écrire l’égalité','$AM=MB$ et $AM+MB=8$ cm.','Diviser par deux',r'$AM=8\div2=4$ cm.','$AM=4$ cm.'),
Q('Construire $M$ à la règle graduée.','Placer le point à la moitié du segment.','Tracer le segment','Tracer $[AB]$ de longueur $8$ cm.','Reporter la moitié','Marquer $M$ à $4$ cm de $A$, sur $[AB]$.','$M$ est à $4$ cm de chaque extrémité.'),
Q('Coder la figure.','Marquer les égalités utiles.','Repérer les deux parties','Les segments $[AM]$ et $[MB]$ ont même longueur.','Choisir un même signe','Placer le même petit trait sur chaque segment.','Un même codage sur $[AM]$ et $[MB]$.'),
Q('Un point $N$ est sur $[AB]$ avec $AN=3$ cm. Est-ce le milieu ?','Calculer l’autre partie.','Soustraire','$NB=8-3=5$ cm.','Comparer',r'$3\ne5$.',r'Non, car $AN\ne NB$.'),
Q('Un point $P$ est hors de $(AB)$ avec $PA=PB$. Est-ce le milieu ?','Vérifier aussi l’appartenance au segment.','Utiliser l’égalité','Elle garantit une même distance aux deux extrémités.','Vérifier la position','$P$ n’est pas sur $[AB]$.','Non ; l’égalité seule ne suffit pas.'),
Q('Quel contrôle manque dans « $AM=MB$, donc $M$ est le milieu » ?','Énoncer la définition complète.','Lister les conditions','Il faut l’égalité et l’appartenance au segment.','Compléter la justification',r'Écrire aussi $M\in[AB]$.','Vérifier que $M$ est sur $[AB]$.'),
Q('On connaît seulement $AM=4$ cm et $M$ milieu de $[AB]$. Retrouver $AB$.','Doubler une moitié.','Utiliser le milieu','$MB=AM=4$ cm.','Additionner','$AB=4+4=8$ cm.','$AB=8$ cm.'),
Q('Placer le milieu $I$ de $[AM]$. Calculer $AI$.','Partager une moitié en deux.','Relever la longueur','$AM=4$ cm.','Diviser',r'$AI=4\div2=2$ cm.','$I$ est sur $[AM]$, à $2$ cm de $A$.'),
Q('Donner la longueur $IB$.','Décomposer sur la droite.','Lire l’ordre','$A$, $I$, $M$, $B$ sont dans cet ordre.','Calculer','$IB=AB-AI=8-2=6$ cm.','$IB=6$ cm.')], 'milieu',['8/2==4','8-3==5','4+4==8','4/2==2','8-2==6'])

family(140,5,['Reconnaître les éléments du cercle','Classer des balises','Rédiger une construction de cercle'],r'Le cercle a pour centre $O$ et rayon $3$ cm. $A$, $B$ et $D$ sont sur le cercle ; $B$, $O$, $D$ sont alignés, $O$ étant entre $B$ et $D$.',[
Q('Nommer un rayon représenté.','Joindre le centre à un point du cercle.','Identifier le centre','$O$ est le centre et $A$ appartient au cercle.','Nommer le segment','$[OA]$ joint ces deux points.','$[OA]$ est un rayon ; $OA=3$ cm.'),
Q('Pourquoi $[BD]$ est-il un diamètre ?','Vérifier extrémités et passage par le centre.','Repérer les extrémités','$B$ et $D$ appartiennent au cercle.','Repérer le centre','$O$ appartient à $[BD]$.','$[BD]$ est une corde qui passe par le centre : un diamètre.'),
Q('Calculer $BD$.','Doubler le rayon.','Décomposer le diamètre','$BD=BO+OD$.','Calculer','$BD=3+3=6$ cm.','$BD=6$ cm.'),
Q('Une balise $E$ vérifie $OE=2$ cm. Est-elle sur le cercle ?','Comparer au rayon.','Comparer les distances','$2<3$.','Interpréter','La balise est à l’intérieur du disque.','Non ; elle est à l’intérieur du disque.'),
Q('Une balise $F$ vérifie $OF=3$ cm. La classer.','Chercher l’égalité avec le rayon.','Lire la distance','$OF$ est égal au rayon.','Appliquer la définition','Les points à $3$ cm de $O$ sont sur le cercle.','$F$ est sur le cercle et appartient aussi au disque.'),
Q('Une balise $G$ vérifie $OG=5$ cm. La classer.','Comparer au rayon.','Comparer','$5>3$.','Interpréter','La distance dépasse le rayon.','$G$ est à l’extérieur du disque.'),
Q('Décrire la construction du cercle au compas.','Fixer centre et ouverture.','Régler l’ouverture','Écarter le compas de $3$ cm à l’aide de la règle.','Tracer sans changer l’ouverture','Piquer en $O$ et faire un tour complet.','Le cercle contient exactement les points à $3$ cm de $O$.'),
Q('Tous les points du disque sont-ils à $3$ cm de $O$ ?','Distinguer frontière et intérieur.','Définir le disque','Ses points ont une distance à $O$ inférieure ou égale à $3$ cm.','Choisir un contre-exemple','$O$ appartient au disque et $OO=0$.','Non ; seuls les points du cercle sont exactement à $3$ cm.'),
Q('Une corde est-elle toujours un diamètre ?','Vérifier le passage par le centre.','Définir une corde','Ses deux extrémités sont sur le cercle.','Ajouter la condition du diamètre','Elle doit aussi passer par le centre.','Non ; par exemple $[AB]$ ne passe pas par $O$.')], 'cercle',['2*3==6','2<3','5>3','0<=3'])

family(140,6,['Localiser un point par deux distances','Expliquer deux solutions','Choisir une balise sur une droite'],r'$AB=6$ cm. On cherche les points à $5$ cm de $A$ et à $5$ cm de $B$. La figure corrigée montre les deux solutions $P$ et $Q$, de part et d’autre de $(AB)$. $M$ est le milieu de $[AB]$.',[
Q('Quel objet contient tous les points à $5$ cm de $A$ ?','Traduire une distance fixe.','Identifier le centre','Le point de référence est $A$.','Fixer le rayon','La distance imposée est $5$ cm.','Le cercle de centre $A$ et de rayon $5$ cm.'),
Q('Quel second cercle tracer ?','Traduire la seconde condition.','Identifier le centre','$B$ est le second point de référence.','Reporter la distance','Garder une ouverture de $5$ cm.','Le cercle de centre $B$ et de rayon $5$ cm.'),
Q('Pourquoi les intersections conviennent-elles ?','Vérifier les deux conditions.','Premier cercle','Un point commun est à $5$ cm de $A$.','Second cercle','Il est aussi à $5$ cm de $B$.','Chaque intersection vérifie les deux distances.'),
Q('Décrire une construction des deux solutions.','Croiser les deux lieux de points.','Tracer les cercles','Tracer les deux cercles de rayon $5$ cm, centrés en $A$ et $B$.','Nommer les intersections','Nommer $P$ au-dessus de $(AB)$ et $Q$ en dessous.','Les solutions sont $P$ et $Q$.'),
Q('Pourquoi ne faut-il pas garder seulement $P$ ?','Chercher tous les points communs.','Observer les deux côtés','Les deux cercles se coupent aussi en $Q$.','Vérifier $Q$','$QA=QB=5$ cm.','Les deux points satisfont la consigne.'),
Q('Que change la consigne « au-dessus de $(AB)$ » ?','Ajouter une contrainte de position.','Lister les candidats','$P$ et $Q$ vérifient les distances.','Appliquer la position','Seul $P$ est du côté demandé sur la figure.','On garde uniquement $P$.'),
Q('Calculer $AM$ et $MB$.','Partager le segment en deux.','Utiliser le milieu','$AM=MB$.','Calculer',r'$6\div2=3$ cm.','$AM=MB=3$ cm.'),
Q('Le milieu $M$ est-il une solution des deux distances imposées ?','Comparer ses distances à $5$ cm.','Calculer au milieu','$MA=MB=3$ cm.','Comparer au rayon demandé',r'$3\ne5$.','Non ; $M$ est équidistant mais pas à $5$ cm.'),
Q('Quelle condition supplémentaire permet de choisir $P$ plutôt que $Q$ ?','Sélectionner un seul côté.','Comparer les distances','Les deux solutions ont les mêmes distances à $A$ et $B$.','Ajouter une position','Préciser le côté de la droite $(AB)$ où placer la balise.','Par exemple : le point situé au-dessus de $(AB)$ sur le plan.')], 'contraintes',['6/2==3','3!=5','math.isclose(math.hypot(3,4),5)'],('medium','medium','medium'))
