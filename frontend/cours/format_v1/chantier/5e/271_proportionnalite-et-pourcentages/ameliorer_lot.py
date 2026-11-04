# -*- coding: utf-8 -*-
"""Outil ponctuel du lot 271–275. Aucun accès à la base ni aux sources en écriture."""
from pathlib import Path
import re, json, math, hashlib

ROOT = Path(__file__).resolve().parent.parent
MARK = '<!-- optitab:1 -->'
def tex(n):
    return f'{n:g}'.replace('.', '{,}')
def box(kind, content, title=''):
    return f'::: {kind}' + (f' {title}' if title else '') + f'\n{content}\n:::\n'
def doc(title, content):
    return f'Titre: {title}\n\n{MARK}\n{content.strip()}\n'

COURS = {
271: r'''::: objectifs
Reconnaître une proportionnalité, compléter un tableau, appliquer un pourcentage et utiliser une échelle.
:::

## I. Reconnaître une proportionnalité

::: definition Coefficient de proportionnalité
Deux grandeurs sont proportionnelles quand on obtient les valeurs de la seconde en multipliant celles de la première par **un même nombre**. Ce nombre est le coefficient de proportionnalité, dans le sens choisi.
:::

| Masse (kg) | 1 | 2 | $3{,}5$ |
|---|---|---|---|
| Prix (€) | $2{,}4$ | $4{,}8$ | $8{,}4$ |

::: exemple Vérifier les quotients
$$\frac{2{,}4}{1}=\frac{4{,}8}{2}=\frac{8{,}4}{3{,}5}=2{,}4$$
On passe de la masse au prix en multipliant par $2{,}4$ : le prix est de $2{,}40$ € par kilogramme.
:::

::: attention
Deux grandeurs qui augmentent ensemble ne sont pas nécessairement proportionnelles. Un droit d’entrée de 5 € puis 3 € par activité donne 8 € pour une activité et 11 € pour deux : le prix ne double pas.
:::

## II. Compléter un tableau

::: methode Revenir à l’unité
Une recette pour 4 personnes utilise 200 g de farine. On cherche la masse pour 6 personnes.
$$
\begin{aligned}
200\div4&=50\quad\text{(g par personne)}\\
6\times50&=300\quad\text{(g pour 6 personnes)}
\end{aligned}
$$
On peut aussi multiplier 200 par $6\div4=1{,}5$.
:::

::: propriete Autres procédures
Dans un tableau de proportionnalité, on peut additionner deux colonnes ou multiplier les deux nombres d’une colonne par un même nombre. On applique **la même opération aux deux lignes**.
:::

## III. Utiliser un pourcentage

::: definition
$p\,\%$ signifie $\frac{p}{100}$. Pour calculer $p\,\%$ d’une quantité, on multiplie cette quantité par $\frac{p}{100}$.
:::

::: exemple Remise sur un prix
Un sac coûte 80 €. La remise est de $15\,\%$ du prix initial.
$$
\begin{aligned}
\text{Remise}&=80\times\frac{15}{100}=12\text{ €}\\
\text{Prix payé}&=80-12=68\text{ €}
\end{aligned}
$$
La remise et le prix final sont deux montants différents.
:::

::: methode Exprimer une proportion en pourcentage
7 élèves sur 20 représentent $\frac{7}{20}=\frac{35}{100}$, soit $35\,\%$ des élèves. Toujours préciser la quantité qui représente $100\,\%$.
:::

## IV. Échelles et grandeurs

::: definition Échelle d’un plan
L’échelle est le quotient « longueur sur le plan / longueur réelle », **dans la même unité**. À l’échelle $1:200$, 1 cm sur le plan représente 200 cm, soit 2 m, en réalité.
:::

::: exemple
À cette échelle, 3 cm représentent $3\times200=600$ cm, soit 6 m. Réciproquement, 10 m représentent $1\,000\div200=5$ cm sur le plan.
:::

::: exemple Déplacement à vitesse constante
À 60 km/h, en $2{,}5$ h on parcourt $60\times2{,}5=150$ km. Pour utiliser des heures, 30 min valent $30\div60=0{,}5$ h.
:::

::: propriete Reconnaissance graphique
Dans un repère, les points représentant un tableau de proportionnalité sont alignés avec l’origine. Des points seulement alignés ne suffisent pas. Des valeurs discrètes se représentent par des points ; on ne les relie que si les valeurs intermédiaires ont un sens.
:::

::: retenir
Un même multiplicateur ; une référence claire pour les pourcentages ; une même unité pour les échelles. Vérifier que le résultat est plausible.
:::
''',
272: r'''::: objectifs
Lire et placer des points dans un repère orthogonal ; passer d’une formule à un tableau ; comprendre comment une grandeur dépend d’une autre.
:::

## I. Lire un couple de coordonnées

::: definition Repère orthogonal
Deux axes perpendiculaires se coupent à l’origine $O$. L’axe horizontal est celui des **abscisses** ; l’axe vertical, celui des **ordonnées**. Les unités choisies sur les deux axes peuvent être différentes.
:::

::: notation L’ordre compte
Dans $A(3\,;-2)$, l’abscisse est 3 et l’ordonnée est $-2$ : on lit d’abord l’horizontale, puis la verticale.
:::

[IMAGE_1]

::: methode Placer ou lire un point
1. Lire les unités et les pas des graduations.
2. Partir de l’origine et repérer l’abscisse sur l’axe horizontal.
3. Suivre une parallèle à l’axe vertical jusqu’à l’ordonnée demandée.
Pour lire un point, suivre les parallèles aux axes en sens inverse.
:::

::: propriete Points sur les axes
Sur l’axe horizontal, l’ordonnée vaut 0. Sur l’axe vertical, l’abscisse vaut 0. L’origine a pour coordonnées $O(0\,;0)$.
:::

::: attention
$A(3\,;-2)$ et $B(-2\,;3)$ sont deux points différents. Un signe négatif indique la gauche ou le bas, selon l’axe.
:::

## II. Une grandeur dépend d’une autre

::: definition
Exprimer « le prix en fonction de la durée » signifie que la durée est la donnée de départ et que le prix dépend de cette durée. On peut utiliser une formule, un tableau ou un graphique.
:::

::: exemple Un tarif
Le tarif est de 5 € au départ puis 3 € par heure. Pour une durée $t$ en heures, le prix $P$ en euros est donné par $P=3t+5$.
:::

| Durée $t$ (h) | 0 | 1 | 2 | 4 |
|---|---|---|---|---|
| Prix $P$ (€) | 5 | 8 | 11 | 17 |

::: methode Remplacer la lettre
Pour $t=4$, remplacer $t$ par 4 et effectuer la multiplication avant l’addition :
$$P=3\times4+5=12+5=17\text{ €}.$$
Le point représentant cette situation a pour coordonnées $(4\,;17)$ : durée en premier, prix en second.
:::

## III. Lire un graphique avec soin

::: methode
Lire d’abord le nom et l’unité de chaque axe. Depuis une valeur de la grandeur horizontale, rejoindre le point ou la courbe puis lire la grandeur verticale. Un graphique donne parfois seulement une valeur approchée.
:::

::: attention Proportionnalité
Avec le tarif $P=3t+5$, zéro heure coûte 5 € : il n’y a pas proportionnalité. Des points alignés ne suffisent pas : leur droite doit passer par l’origine.
:::

::: retenir
Coordonnées = (abscisse ; ordonnée). Tableau = valeurs calculées à partir des données. Les points d’un nombre entier d’activités ne sont pas à relier : une demi-activité n’a pas de sens ici.
:::
''',
273: r'''::: objectifs
Reconnaître des angles, calculer des mesures et justifier un parallélisme à l’aide d’angles.
:::

## I. Nommer et reconnaître un angle

::: definition
Dans $\widehat{ABC}$, la lettre centrale $B$ désigne le sommet ; les côtés sont les demi-droites $[BA)$ et $[BC)$.
:::

| Angle | Mesure |
|---|---|
| Nul | $0^\circ$ |
| Aigu | Strictement entre $0^\circ$ et $90^\circ$ |
| Droit | $90^\circ$ |
| Obtus | Strictement entre $90^\circ$ et $180^\circ$ |
| Plat | $180^\circ$ |
| Plein | $360^\circ$ |

::: definition
Deux angles **adjacents** ont le même sommet, un côté commun et des intérieurs disjoints. Deux angles **supplémentaires** ont une somme de $180^\circ$ ; ils ne sont pas nécessairement adjacents. La **bissectrice** partage un angle en deux angles de même mesure.
:::

## II. Deux droites sécantes

[IMAGE_1]

::: propriete
Deux angles adjacents formant un angle plat sont supplémentaires. Deux angles opposés par le sommet ont la même mesure.
:::

::: demonstration Angles opposés
Si $\widehat{AOC}=40^\circ$, alors $\widehat{BOC}=180^\circ-40^\circ=140^\circ$. L’angle $\widehat{BOD}$ est supplémentaire de $\widehat{BOC}$, donc vaut $180^\circ-140^\circ=40^\circ$.
:::

::: exemple Bissectrice
Si $[OE)$ est la bissectrice de $\widehat{AOC}=40^\circ$, alors $\widehat{AOE}=\widehat{EOC}=40^\circ\div2=20^\circ$.
:::

## III. Deux droites coupées par une sécante

::: definition
Les angles **alternes internes** sont entre les deux droites, de part et d’autre de la sécante, à des sommets différents. Les angles **correspondants** occupent la même position autour des deux intersections.
:::

[IMAGE_2]

::: propriete Utiliser un parallélisme connu
Si les deux droites sont parallèles, deux angles alternes internes ont la même mesure ; deux angles correspondants aussi.
:::

::: propriete Démontrer un parallélisme
Réciproquement, si deux angles alternes internes ont la même mesure, les deux droites sont parallèles. C’est aussi vrai pour deux angles correspondants de même mesure.
:::

::: methode Rédiger une justification
1. Repérer les deux angles et préciser leur position.
2. Dire ce qui est connu : parallélisme ou égalité d’angles.
3. Citer la propriété dans le sens adapté et conclure.
:::

::: exemple Angles droits
Deux droites perpendiculaires à une même droite sont parallèles : leurs angles correspondants sont droits, donc égaux.
:::

::: attention
Une figure qui semble avoir deux parallèles ne prouve rien. Les angles opposés par le sommet sont toujours égaux ; les angles alternes internes ne le sont que sous une hypothèse adaptée.
:::

::: retenir
Angle plat : $180^\circ$ ; tour complet : $360^\circ$ ; bissectrice : moitié de l’angle. Toujours justifier l’égalité de deux angles.
:::
''',
274: r'''::: objectifs
Construire un triangle, calculer ses angles, distinguer hauteur, médiane et médiatrice et utiliser une hauteur pour calculer une aire.
:::

## I. Angles d’un triangle

::: propriete
La somme des trois angles d’un triangle vaut $180^\circ$.
:::

::: demonstration
Tracer par un sommet la parallèle au côté opposé. Les angles alternes internes permettent d’y reporter les angles des deux autres sommets. Les trois angles forment alors un angle plat.
:::

[IMAGE_1]

::: exemple
Si $\widehat{A}=35^\circ$ et $\widehat{B}=45^\circ$, alors
$$\widehat{C}=180^\circ-(35^\circ+45^\circ)=100^\circ.$$
Le triangle est obtusangle, car il possède un angle supérieur à $90^\circ$.
:::

::: propriete Triangles particuliers
Dans un triangle rectangle, les deux angles aigus ont une somme de $90^\circ$. Dans un triangle isocèle, les deux angles à la base sont égaux. Dans un triangle équilatéral, chaque angle vaut $60^\circ$.
:::

## II. Construire un triangle

::: methode Trois longueurs
Pour construire $AB=7$ cm, $AC=4$ cm et $BC=5$ cm : tracer $[AB]$, puis un arc de centre $A$, de rayon 4 cm, et un arc de centre $B$, de rayon 5 cm. Leur intersection choisie donne $C$ ; relier les sommets.
:::

::: propriete Inégalité triangulaire
Un triangle non aplati est constructible si son plus grand côté est **strictement inférieur** à la somme des deux autres. Avec 4, 5 et 7 cm : $7<4+5$. Avec 2, 3 et 6 cm : $6>2+3$, impossible. Si l’égalité est vérifiée, les trois points sont alignés.
:::

::: methode Un côté et deux angles
Tracer le côté donné à la règle graduée. À chaque extrémité, tracer au rapporteur la demi-droite formant l’angle demandé, du même côté du segment. Leur intersection est le troisième sommet. Avec deux côtés et l’angle compris entre eux, tracer d’abord cet angle puis reporter les deux longueurs sur ses côtés.
:::

## III. Trois droites à distinguer

| Droite | Définition |
|---|---|
| Hauteur | Passe par un sommet et est perpendiculaire à la droite portant le côté opposé. |
| Médiane | Passe par un sommet et le milieu du côté opposé. |
| Médiatrice d’un côté | Est perpendiculaire à ce côté et passe par son milieu. |

[IMAGE_2]

::: definition Médiatrice et distances
Un point appartient à la médiatrice de $[BC]$ si et seulement s’il est à la même distance de $B$ et de $C$.
:::

::: propriete Cercle circonscrit
Les trois médiatrices d’un triangle se coupent en un même point $O$, équidistant de ses sommets. Le cercle de centre $O$ et de rayon $OA$ passe donc par $A$, $B$ et $C$. Pour construire son centre, deux médiatrices suffisent ; contrôler la troisième distance.
:::

::: attention
Une hauteur peut rencontrer le **prolongement** d’un côté. Une médiane n’est pas en général perpendiculaire au côté. La médiatrice ne passe pas nécessairement par le sommet opposé.
:::

## IV. Calculer une aire

::: formule
$$\mathcal A=\frac{\text{base}\times\text{hauteur correspondante}}{2}$$
:::

::: exemple
Une base de 8 m et sa hauteur de 3 m donnent $\mathcal A=8\times3\div2=12$ m$^2$. La médiane issue du sommet partage la base en deux segments de 4 m. Les deux triangles ont la même hauteur de 3 m : chacun a une aire de $4\times3\div2=6$ m$^2$.
:::

::: retenir
Hauteur : perpendicularité ; médiane : milieu ; médiatrice : milieu **et** perpendicularité. Les longueurs doivent être dans la même unité avant de calculer une aire.
:::

::: remarque Pour aller plus loin
On peut observer la rencontre des trois hauteurs (orthocentre) ou des trois médianes (centre de gravité). Ces noms et propriétés ne sont pas nécessaires pour les constructions et calculs de ce chapitre.
:::
''',
275: r'''::: objectifs
Construire une image par symétrie axiale ou centrale, reconnaître un demi-tour et utiliser les propriétés de conservation.
:::

## I. Symétrie axiale : un axe

::: definition
Deux points distincts $A$ et $A'$ sont symétriques par rapport à une droite $(d)$ quand $(d)$ est la médiatrice de $[AA']$. Un point situé sur l’axe reste à sa place.
:::

[IMAGE_1]

::: methode Construire $A'$
1. Tracer la perpendiculaire à $(d)$ passant par $A$ ; elle rencontre l’axe en $H$.
2. Reporter la longueur $HA$ de l’autre côté de $(d)$ sur cette perpendiculaire.
3. Vérifier $HA'=HA$ et le codage de l’angle droit en $H$.
:::

::: attention
On mesure la distance à l’axe **perpendiculairement**. Pour un axe oblique sur un quadrillage, compter seulement les carreaux horizontaux peut donner une image fausse.
:::

## II. Symétrie centrale : un centre

::: definition
Le symétrique $A'$ de $A$ par rapport à $O$ est le point tel que $O$ soit le milieu de $[AA']$. C’est un **demi-tour**, d’angle $180^\circ$. Le centre $O$ reste à sa place.
:::

[IMAGE_2]

::: methode Construire $A'$
Tracer la droite $(AO)$ puis reporter $OA$ de l’autre côté de $O$. Contrôler les deux conditions : $A$, $O$, $A'$ alignés et $OA=OA'$.
:::

::: exemple Dans un repère
Pour le centre $O(0\,;0)$, le point $A(2\,;1)$ a pour image $A'(-2\,;-1)$ : les deux coordonnées changent de signe. Pour la symétrie d’axe vertical passant par $O$, son image est $A'(-2\,;1)$ : seule l’abscisse change de signe.
:::

## III. Construire l’image d’une figure

::: methode
Construire séparément l’image de chaque sommet, puis relier les points images dans le même ordre. L’image de $[AB]$ est $[A'B']$ ; celle du triangle $ABC$ est le triangle $A'B'C'$.
:::

::: propriete Conservation
Les deux symétries conservent les longueurs, les mesures d’angles, l’alignement et les aires. L’image d’un cercle est un cercle de même rayon dont le centre est l’image du centre initial.
:::

::: propriete Demi-tour et droites
Par symétrie centrale, l’image d’une droite est une droite parallèle à la droite initiale. Si cette droite passe par le centre, son image est confondue avec elle.
:::

::: exemple Calculer sans remesurer
Si $AB=AC=2$ unités et $ABC$ est rectangle en $A$, alors $A'B'=A'C'=2$ unités et son aire vaut aussi $2\times2\div2=2$ unités d’aire.
:::

::: attention
Un axe est une **droite** ; un centre est un **point**. Répéter deux fois la même symétrie ramène chaque point à sa position initiale.
:::

::: retenir
Axiale : axe médiatrice du segment joignant un point à son image. Centrale : centre milieu de ce segment. Les longueurs et les aires restent identiques.
:::
'''
}

FICHES = {
271:r'''::: objectifs
Choisir la bonne procédure de proportionnalité.
:::
## I. Proportionnalité
::: definition
Un **même coefficient** multiplie les valeurs de la première grandeur pour donner celles de la seconde. Préciser le sens du passage.
:::
::: methode
Revenir à l’unité : 200 g pour 4 personnes donnent $200\div4=50$ g par personne, puis $6\times50=300$ g pour 6 personnes. On peut aussi additionner les colonnes ou multiplier une colonne entière.
:::
## II. Pourcentages et échelles
::: formule
$$p\,\%\text{ d’une quantité}=\frac{p}{100}\times\text{quantité}$$
:::
- Remise de $15\,\%$ sur 80 € : $80\times15\div100=12$ € ; prix payé : $80-12=68$ €.
- 7 sur 20 : $7/20=35/100$, soit $35\,\%$.
- Échelle $1:200$ : 1 cm représente 200 cm, soit 2 m. Convertir dans la même unité.
::: attention
Un coût fixe peut rompre la proportionnalité. Des points alignés doivent aussi l’être **avec l’origine**. Une remise est un montant à soustraire, pas le prix final.
:::
''',
272:r'''::: objectifs
Lire les coordonnées et calculer une grandeur à partir d’une formule.
:::
## I. Repère
::: retenir
$(x\,;y)$ : **abscisse horizontale d’abord**, ordonnée verticale ensuite. Origine : $O(0\,;0)$. Sur l’axe horizontal, $y=0$ ; sur l’axe vertical, $x=0$.
:::
## II. Formule, tableau, graphique
::: methode
Pour $P=3t+5$ et $t=4$ : $P=3\times4+5=17$. Le point représentatif est $(4\,;17)$. Lire les noms, unités et graduations des axes avant toute lecture graphique.
:::
| $t$ (h) | 0 | 1 | 2 | 4 |
|---|---|---|---|---|
| $P$ (€) | 5 | 8 | 11 | 17 |
::: attention
Ne pas inverser les coordonnées ni perdre les signes. Pour une proportionnalité, les points doivent être alignés **avec l’origine**. Ici, pour $t=0$, $P=5$ : ce tarif n’est pas proportionnel.
:::
''',
273:r'''::: objectifs
Identifier les angles avant de calculer.
:::
## I. Mesures utiles
| Situation | Règle |
|---|---|
| Angle droit / plat / plein | $90^\circ$ / $180^\circ$ / $360^\circ$ |
| Angles supplémentaires | Somme de $180^\circ$ |
| Angles opposés par le sommet | Mesures égales |
| Bissectrice | Partage en deux angles égaux |
## II. Parallèles et sécante
::: propriete
Deux droites parallèles coupées par une sécante donnent des angles alternes internes égaux et des angles correspondants égaux. Réciproquement, l’égalité d’une de ces paires prouve le parallélisme.
:::
::: methode
Repérer la paire → citer l’hypothèse connue → choisir la propriété → conclure. Pour un angle supplémentaire de $40^\circ$, calculer $180^\circ-40^\circ=140^\circ$.
:::
::: attention
Dans $\widehat{ABC}$, le sommet est $B$. Un dessin ne prouve ni égalité d’angles ni parallélisme. Deux angles supplémentaires ne sont pas nécessairement adjacents.
:::
''',
274:r'''::: objectifs
Construire et raisonner avec les données du triangle.
:::
## I. Angles et construction
::: formule
$$\widehat A+\widehat B+\widehat C=180^\circ$$
:::
- Isocèle : angles à la base égaux. Équilatéral : trois angles de $60^\circ$.
- Trois côtés : le plus grand doit être **strictement inférieur** à la somme des deux autres ; tracer un segment et deux arcs de compas.
- Un côté et deux angles : règle, puis deux demi-droites au rapporteur, du même côté du segment.
## II. Droites et aire
| Droite | Condition |
|---|---|
| Hauteur | Sommet + perpendicularité au côté opposé |
| Médiane | Sommet + milieu du côté opposé |
| Médiatrice | Milieu d’un côté + perpendicularité |
::: retenir
Deux médiatrices permettent de construire le centre du cercle circonscrit, équidistant des trois sommets.
$$\mathcal A=\frac{\text{base}\times\text{hauteur correspondante}}2$$
Une médiane partage l’aire en deux parts égales.
:::
::: attention
La hauteur peut tomber sur le prolongement du côté. Une médiane n’est pas en général une hauteur. Convertir les longueurs dans la même unité ; donner l’aire en unité **carrée**.
:::
''',
275:r'''::: objectifs
Ne plus confondre axe et centre.
:::
## I. Deux constructions
| Symétrie | Condition pour $A$ et son image $A'$ |
|---|---|
| Axiale d’axe $(d)$ | $(d)$ est la médiatrice de $[AA']$ |
| Centrale de centre $O$ | $O$ est le milieu de $[AA']$ |
::: methode
Axiale : perpendiculaire à l’axe, puis même distance de l’autre côté. Centrale : droite passant par le centre, puis même distance de l’autre côté.
:::
## II. Propriétés
::: retenir
Les deux symétries conservent longueurs, angles, alignement et aires. Construire l’image de chaque sommet, puis les relier dans le même ordre. Deux applications de la même symétrie ramènent à la figure de départ.
:::
- Centre $O(0\,;0)$ : $(x\,;y)$ devient $(-x\,;-y)$.
- Axe vertical passant par $O$ : $(x\,;y)$ devient $(-x\,;y)$.
- Un demi-tour transforme une droite en une parallèle, confondue avec elle si elle passe par le centre.
::: attention
Le centre est un point ; l’axe est une droite. Le centre et les points de l’axe restent à leur place.
:::
'''
}

def picture(body): return '\\begin{tikzpicture}\n'+body+'\n\\end{tikzpicture}'
def node(x,y,label,anchor='south west',color='otInk'):
    return rf'\node[anchor={anchor},text={color},inner sep=3pt] at ({x},{y}) {{$ {label} $}};'+'\n'
def grid(xmin,xmax,ymin,ymax,xx=0.4,yy=0.4):
    # Distances on the two axes are explicitly defined: no global text scaling.
    b=rf'\begin{{scope}}[x={xx}cm,y={yy}cm]'+'\n'
    b+=rf'\draw[otRule,line width=.25pt,step=1] ({xmin},{ymin}) grid ({xmax},{ymax});'+'\n'
    b+=rf'\draw[geoVecteur] ({xmin},0)--({xmax+0.4},0);\draw[geoVecteur] (0,{ymin})--(0,{ymax+0.5});'+'\n'
    for x in range(xmin,xmax+1):
        if x and (xmax-xmin<=14 or x%2==0):
            b+=rf'\node[coteTexte,anchor=north,font=\small] at ({x},0) {{$ {x} $}};'+'\n'
    for y in range(ymin,ymax+1):
        if y: b+=rf'\node[coteTexte,anchor=east,font=\small] at (0,{y}) {{$ {y} $}};'+'\n'
    b+=node(0,0,'O','north east')
    return b

def repere_point():
    b=grid(-3,4,-3,4,.58,.58)
    b+=r'\draw[geoAide] (3,0)--(3,-2)--(0,-2);\fill[otNavy] (3,-2) circle (2pt);'
    b+=node(3,-2,'A','south west')
    b+=node(-2,3,'B','south west')+r'\fill[otGreenDark] (-2,3) circle (2pt);'
    return picture(b+'\n\\end{scope}')

def jardin(a,b):
    sx=min(.55,6.2/(2*a+2)); sy=.44
    s=grid(-a-1,a+1,-b-1,b+1,sx,sy)
    s+=rf'\draw[geoTrait,fill=otSky,fill opacity=.32] ({-a},{b})--({a},{b})--({a},{-b})--({-a},{-b})--cycle;'+'\n'
    for x,y,l,an in [(-a,b,'A','south east'),(a,b,'B','south west'),(a,-b,'C','north west'),(-a,-b,'D','north east')]:s+=node(x,y,l,an)
    return picture(s+'\\end{scope}')

def rosace(a,corr=False):
    # Orient OA to the left; OC is below left. This makes angle AOC exactly a.
    s=r'\coordinate(O) at (0,0);\coordinate(A) at (-3,0);\coordinate(B) at (3,0);'+ '\n'
    s+=rf'\coordinate(C) at ({180+a}:2.6);\coordinate(D) at ({a}:2.6);\coordinate(E) at ({180+a/2}:2.8);'+'\n'
    s+=r'\draw[geoTrait] (A)--(B) (C)--(D);\draw[geoAide] (O)--(E);'
    s+=rf'\draw[otOrange,line width=.8pt] (-.8,0) arc[start angle=180,end angle={180+a},radius=.8];'+'\n'
    s+=rf'\node[anchor=east,text=otOrange,inner sep=4pt] at ({180+a/2}:1.15) {{$ {a}^\circ $}};'+'\n'
    for x,y,l,an in [(-3,0,'A','south east'),(3,0,'B','south west'),(0,0,'O','south east')]:s+=node(x,y,l,an)
    s+=rf'\node[anchor=north east,inner sep=4pt] at (C) {{$C$}};\node[anchor=south west,inner sep=4pt] at (D) {{$D$}};\node[anchor=north west,inner sep=4pt,text=otGreenDark] at (E) {{$E$}};'+'\n'
    if corr:
        s+=rf'\draw[geoReponse] (.7,0) arc[start angle=0,end angle={a},radius=.7];'
        s+=rf'\node[text=otGreenDark,anchor=west,inner sep=4pt] at ({a/2}:1.05) {{$ {a}^\circ $}};'
    return picture(s)

def paralleles(a,corr=False):
    # Fixed diagram proportions, exact angle a using an explicit slope.
    dx=2/math.tan(math.radians(a)); ax=dx/2; bx=-dx/2
    s=rf'\coordinate(A) at ({ax},1);\coordinate(B) at ({bx},-1);'+'\n'
    s+=r'\draw[geoTrait] (-3.3,1)--(3.3,1) (-3.3,-1)--(3.3,-1);'
    s+=rf'\draw[geoTrait] ({bx-.5/math.tan(math.radians(a))},-1.5)--({ax+.7/math.tan(math.radians(a))},1.7);'+'\n'
    s+=node(-3.3,1,'(d)','south west')+node(-3.3,-1,'(e)','south west')
    s+=node(ax,1,'A','north west')+node(bx,-1,'B','north west')
    s+=rf'\draw[otOrange] ({ax+.6},1) arc[start angle=0,end angle={a},radius=.6];'
    s+=rf'\node[anchor=south west,text=otOrange,inner sep=3pt] at ({ax+.88},1.18) {{$ {a}^\circ $}};'
    s+=r'\node[anchor=north west,text=otMuted] at (-3.3,-1.8) {$(d)\parallel(e)$};'
    if corr:
        s+=rf'\draw[geoReponse] ({bx+.6},-1) arc[start angle=0,end angle={a},radius=.6];'
        s+=rf'\node[anchor=south west,text=otGreenDark,inner sep=3pt] at ({bx+.85},-.82) {{$ {a}^\circ $}};'
    return picture(s)

def triangle(L,a,b,corr=False):
    x=5*math.tan(math.radians(b))/(math.tan(math.radians(a))+math.tan(math.radians(b)))
    y=x*math.tan(math.radians(a))
    s=rf'\coordinate(A) at (0,0);\coordinate(B) at (5,0);\coordinate(C) at ({x},{y});'+'\n'
    s+=r'\draw[geoTrait] (A)--(B)--(C)--cycle;'
    s+=node(0,0,'A','north east')+node(5,0,'B','north west')+node(x,y,'C','south')
    s+=rf'\draw[otOrange] (.7,0) arc[start angle=0,end angle={a},radius=.7];'
    s+=rf'\draw[otOrange] (4.3,0) arc[start angle=180,end angle={180-b},radius=.7];'
    s+=node(1.0,.12,rf'{a}^\circ','south west','otOrange')+node(4,.12,rf'{b}^\circ','south east','otOrange')
    s+=node(2.5,-.35,rf'{L}\text{{ cm}}','north')
    if corr:s+=node(x,y+.4,rf'180^\circ-{a}^\circ-{b}^\circ={180-a-b}^\circ','south','otGreenDark')
    return picture(s)

def aire(base,h,corr=False):
    s=r'\coordinate(B) at (0,0);\coordinate(C) at (6,0);\coordinate(A) at (2,2.6);\coordinate(H) at (2,0);\coordinate(M) at (3,0);'
    s+=r'\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoAide] (A)--(H);\draw[geoReponse] (A)--(M);\angledroit{A}{H}{C}\codage{B}{M}\codage{M}{C}'
    for x,y,l,an in [(0,0,'B','north east'),(6,0,'C','north west'),(2,2.6,'A','south'),(2,0,'H','north'),(3,0,'M','north')]:s+=node(x,y,l,an)
    s+=node(3,-.7,rf'BC={base}\text{{ m}}','north')
    s+=node(1.65,1.15,rf'{h}\text{{ m}}','east')
    if corr:s+=node(4.5,2.4,rf'\mathcal A={tex(base*h/2)}\text{{ m}}^2','south','otGreenDark')
    return picture(s)

def symetrie(x,y,central,corr=False):
    # Figure shown as a geometric sketch with coordinates in the accompanying table.
    # Constant physical dimensions preserve readability for all coordinate values.
    b=grid(-x-3,x+3,-y-3,y+3, min(.5,6.7/(2*x+6)),.42)
    b+=rf'\draw[geoTrait,fill=otSky] ({x},{y})--({x+2},{y})--({x},{y+2})--cycle;'
    for px,py,l,an in [(x,y,'A','north east'),(x+2,y,'B','south west'),(x,y+2,'C','south east')]:b+=node(px,py,l,an)
    if not central:b+=rf'\draw[otOrange,line width=1pt] (0,{-y-3})--(0,{y+3});'
    if corr:
        s=-1 if central else 1
        b+=rf'\draw[geoReponse,fill=otGreen!12] ({-x},{s*y})--({-x-2},{s*y})--({-x},{s*(y+2)})--cycle;'
        for px,py,l,an in [(-x,s*y,"A'",'south west' if central else 'north west'),(-x-2,s*y,"B'",'south east'),(-x,s*(y+2),"C'",'north west' if central else 'south west')]:b+=node(px,py,l,an,'otGreenDark')
    return picture(b+'\\end{scope}')

def parse_blocks(text):
    return [b.strip() for b in re.split(r'^===\s*$',text,flags=re.M) if b.strip()]

for d in sorted(ROOT.iterdir()):
    if not d.is_dir() or not d.name[:3].isdigit() or not 271<=int(d.name[:3])<=275: continue
    n=int(d.name[:3]); meta=json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
    (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'geometrie','maj':'2026-10-28'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (d/'source_en_ligne').iterdir() if p.is_file()}
    figures={}; mapping={'cours':{},'fiches':{},'exercices':{}}
    def fig(name,code): figures[name]=code;return name
    def mapfig(kind,id,pos,name,alt):
        mapping[kind].setdefault(str(id),{})[str(pos)]={'fichier':name+'.png','alt':alt}
    if n==272:
        fn=fig('cours_repere',repere_point());mapfig('cours',meta['cours'][0]['id'],1,fn,'Repère orthogonal : A a pour coordonnées (3 ; −2), B a pour coordonnées (−2 ; 3).')
    if n==273:
        for pos,name,code,alt in [(1,'cours_secantes',rosace(40),'Deux droites sécantes en O et la bissectrice OE de l’angle AOC de 40 degrés.'),(2,'cours_paralleles',paralleles(45,True),'Deux parallèles coupées par une sécante : angles correspondants de 45 degrés.')]:
            fig(name,code);mapfig('cours',meta['cours'][0]['id'],pos,name,alt)
    if n==274:
        for pos,name,code,alt in [(1,'cours_angles',triangle(5,35,45,True),'Triangle ABC : angles de 35, 45 et 100 degrés ; somme de 180 degrés.'),(2,'cours_hauteur_mediane',aire(8,3),'Triangle ABC avec la hauteur AH perpendiculaire à BC et la médiane AM passant par le milieu M.')]:
            fig(name,code);mapfig('cours',meta['cours'][0]['id'],pos,name,alt)
    if n==275:
        for pos,name,central in [(1,'cours_axiale',False),(2,'cours_centrale',True)]:
            fig(name,symetrie(2,1,central,True));mapfig('cours',meta['cours'][0]['id'],pos,name,'Triangle ABC et son image A′B′C′ par symétrie '+('centrale de centre O.' if central else 'd’axe vertical passant par O.'))
    for c in meta['cours']:(d/f"cours_{c['id']}.txt").write_text(doc(c['titre'],COURS[n]),encoding='utf-8')
    for f in meta['fiches']:(d/f"fiche_{f['id']}.txt").write_text(doc(f['titre'],FICHES[n]),encoding='utf-8')
    out=[]; verif=[]
    text=(d/'exercices.txt').read_text(encoding='utf-8')
    for b in parse_blocks(text):
        head,enonce=b.split('Énoncé:',1);enonce,rest=enonce.split('Étapes:',1);steps,solution=rest.split('Solution:',1)
        eid=int(re.search(r'^Id:\s*(\d+)',head,re.M)[1]); title=head.splitlines()[0].replace('===','',1).strip()
        assert title==next(e['titre'] for e in meta['exercices'] if e['id']==eid)
        head=re.sub(r'^Image:.*\n?','',head,flags=re.M)
        original_enonce=enonce
        details=[];nums={};fig_name=None;fig_corr=None
        if n==271:
            enonce=re.sub(r'\[IMAGE_\d+\]','',enonce);steps=re.sub(r'\[IMAGE_\d+\]','',steps)
            if 'Une recette' in enonce:
                p,m=map(int,re.search(r'pour (\d+) personnes demande (\d+) g',enonce).groups()); k=m/p
                q=int(re.search(r'pour (\d+) personnes \?',enonce)[1]); stock=int(re.search(r'Avec (\d+) g',enonce)[1])
                details=[rf'La masse totale est partagée entre {p} personnes : ${m}\div{p}={tex(k)}$ g pour une personne.',rf'Chaque personne reçoit {tex(k)} g, donc ${q}\times{tex(k)}={tex(q*k)}$ g.',rf'Dans le sens « personnes vers grammes », le coefficient vaut ${m}\div{p}={tex(k)}$.',rf'On cherche combien de parts de {tex(k)} g sont contenues dans {stock} g : ${stock}\div{tex(k)}={tex(stock/k)}$.',rf'Le doublement donne ${2*p}$ personnes et $2\times{m}={2*m}$ g. Les deux grandeurs ont été multipliées par 2.',rf'Avec la base fixe, 1 personne demande $100+{tex(k)}={tex(100+k)}$ g ; 2 demandent $100+2\times{tex(k)}={tex(100+2*k)}$ g. Or $2\times{tex(100+k)}={tex(200+2*k)}$, ce qui est différent.']
                enonce=enonce.replace('1. Quelle quantité',f'| Personnes | {p} | 1 | {q} |\n|---|---|---|---|\n| Farine (g) | {m} | À calculer | À calculer |\n\n1. Quelle quantité',1)
                nums={'personnes':p,'masse':m,'cible':q,'stock':stock,'coefficient':k,'masse_cible':q*k,'parts':stock/k}
            else:
                price,taux=map(int,re.search(r'coûte (\d+) €.*remise de (\d+) %',enonce).groups());r=price*taux/100;paid=price-r
                details=[f'La référence est le prix avant réduction : {price} € représentent 100 %.',rf'$1\,\%$ représente un centième : ${price}\div100={tex(price/100)}$ €.',rf'$\text{{Remise}}={price}\times\frac{{{taux}}}{{100}}={tex(r)}$ €.',rf'$\text{{Prix payé}}={price}-{tex(r)}={tex(paid)}$ €.',rf'On paie $100\,\%-{taux}\,\%={100-taux}\,\%$ du prix initial.',rf'Première méthode : $2\times{tex(paid)}={tex(2*paid)}$ €. Seconde méthode : prix initial ${2*price}$ €, remise ${2*price}\times\frac{{{taux}}}{{100}}={tex(2*r)}$ €, puis ${2*price}-{tex(2*r)}={tex(2*paid)}$ €.']
                nums={'prix':price,'taux':taux,'remise':r,'paye':paid,'deux':2*paid}
        elif n==272:
            if 'jardin rectangulaire' in enonce:
                a,h=map(int,re.search(r'A\(-([0-9]+) ; ([0-9]+)\)',enonce).groups());name=f'jardin_{a}_{h}';fig_name=fig(name,jardin(a,h));fig_corr=fig_name
                details=[rf'Les coordonnées de $A$ se lisent dans l’ordre : $A(-{a}\,;{h})$. Donc $x_A=-{a}$ et $y_A={h}$.',rf'Être au-dessus de l’axe horizontal signifie avoir une ordonnée positive. $A$ et $B$ ont pour ordonnée ${h}>0$ ; $C$ et $D$ ont pour ordonnée $-{h}<0$.',rf'$A$ et $B$ sont à la même hauteur : $y_A=y_B={h}$. La droite $(AB)$ est donc parallèle à l’axe horizontal.',rf'De $-{a}$ à $0$, il y a {a} unités ; de 0 à {a}, encore {a}. Donc $AB={a}+{a}={2*a}$ m.',rf'De $-{h}$ à {h}, on compte ${h}+{h}={2*h}$ unités. Donc $BC={2*h}$ m et $\mathcal A=AB\times BC={2*a}\times{2*h}={4*a*h}$ m$^2$.',rf'Les abscisses opposées $-{a}$ et {a} sont à égale distance de 0 ; de même pour les ordonnées $-{h}$ et {h}. Les diagonales ont donc pour milieu commun $O(0\,;0)$.']
                nums={'a':a,'h':h,'AB':2*a,'BC':2*h,'aire':4*a*h}
            else:
                fixe,k=map(int,re.search(r'coûte (\d+) €.*puis (\d+) €',enonce).groups()); q=int(re.search(r'prix de (\d+) activités',enonce)[1]);budget=int(re.search(r'avec (\d+) €',enonce)[1])
                enonce=re.sub(r'\[IMAGE_1\]',f'| Activités $n$ | 0 | 1 | 2 |\n|---|---|---|---|\n| Prix $P$ (€) | À calculer | À calculer | À calculer |',enonce)
                steps=re.sub(r'\[IMAGE_2\]','',steps)
                details=[rf'Les activités coûtent ${k}\times n$ euros, auxquels s’ajoute une seule fois le droit d’entrée de {fixe} €. Donc $P={k}n+{fixe}$.',rf'Pour $n=0$, $P={k}\times0+{fixe}={fixe}$. Pour $n=1$, $P={k}+{fixe}={k+fixe}$. Pour $n=2$, $P={k}\times2+{fixe}={2*k+fixe}$.',rf'On remplace $n$ par {q} : $P={k}\times{q}+{fixe}={k*q}+{fixe}={k*q+fixe}$ €.',rf'Le nombre d’activités se place en abscisse et le prix en ordonnée. Pour deux activités, $P={k}\times2+{fixe}={2*k+fixe}$ ; le point est $(2\,;{2*k+fixe})$.',f'Pour 0 activité, on paie {fixe} €, alors qu’une proportionnalité imposerait un prix nul. Le droit d’entrée empêche donc la proportionnalité.',rf'On paie d’abord l’entrée : ${budget}-{fixe}={budget-fixe}$ €. Chaque activité coûte {k} € : $({budget}-{fixe})\div{k}={tex((budget-fixe)/k)}$. Vérification : ${k}\times{tex((budget-fixe)/k)}+{fixe}={budget}$ €.']
                nums={'fixe':fixe,'k':k,'q':q,'budget':budget,'prix':k*q+fixe,'activites':(budget-fixe)/k}
        elif n==273:
            a=int(re.search(r'mesure (\d+)°',enonce)[1]); supp=180-a
            if 'rosace' in title:
                fig_name=fig(f'rosace_{a}',rosace(a));fig_corr=fig(f'rosace_{a}_corrige',rosace(a,True))
                details=[r'Les points $A$, $O$, $B$ sont alignés dans cet ordre : les demi-droites $[OA)$ et $[OB)$ sont opposées. Leur angle est donc plat.',rf'Les angles $\widehat{{AOC}}$ et $\widehat{{BOC}}$ forment l’angle plat $\widehat{{AOB}}$. Donc $\widehat{{BOC}}=180^\circ-{a}^\circ={supp}^\circ$.',rf'$\widehat{{BOD}}$ et $\widehat{{AOC}}$ sont opposés par le sommet $O$. Ils ont la même mesure : ${a}^\circ$.',rf'$\widehat{{AOD}}$ et $\widehat{{BOC}}$ sont opposés par le sommet, donc $\widehat{{AOD}}={supp}^\circ$.',rf'La bissectrice $[OE)$ partage $\widehat{{AOC}}$ en deux angles égaux : ${a}^\circ\div2={tex(a/2)}^\circ$ chacun.',rf'En parcourant les quatre secteurs dans l’ordre, on obtient ${a}+{supp}+{a}+{supp}=360$. Les quatre angles couvrent donc un tour complet.']
            else:
                fig_name=fig(f'paralleles_{a}',paralleles(a));fig_corr=fig(f'paralleles_{a}_corrige',paralleles(a,True))
                enonce=enonce.replace('situé sur la même demi-droite de d','situé au-dessous de d et à droite de la sécante')
                details=[rf'Un angle aigu mesure strictement entre $0^\circ$ et $90^\circ$. Or $0<{a}<90$.',rf'Les angles opposés par le sommet sont égaux, indépendamment du parallélisme : l’angle opposé mesure ${a}^\circ$.',rf'L’angle donné et l’angle au-dessous de $(d)$, à droite de la sécante, forment un angle plat : $180^\circ-{a}^\circ={supp}^\circ$.',rf'Les angles au-dessus des droites et à droite de la sécante sont correspondants. Comme $(d)\parallel(e)$, celui en $B$ mesure ${a}^\circ$.',rf'En $A$, l’angle intérieur en bas à gauche mesure ${a}^\circ$, car il est opposé par le sommet à l’angle donné. Son alterne-interne, en $B$, est au-dessus de $(e)$ et à droite de la sécante. Les droites étant parallèles, il mesure aussi ${a}^\circ$.',r'Sans hypothèse de parallélisme, les propriétés sur les angles opposés ou supplémentaires restent valables à chaque intersection, mais elles ne relient plus les angles de sommets $A$ et $B$. Il faut une information supplémentaire.']
            nums={'angle':a,'supplement':supp,'demi':a/2,'tour':2*a+2*supp}
        elif n==274:
            if 'On veut construire' in enonce:
                L,a,bb=map(int,re.search(r'AB = (\d+) cm.*BAC = (\d+)°.*ABC = (\d+)°',enonce).groups());c=180-a-bb
                fig_name=fig(f'triangle_{L}_{a}_{bb}',triangle(L,a,bb));fig_corr=fig(f'triangle_{L}_{a}_{bb}_corrige',triangle(L,a,bb,True))
                details=[rf'La somme des trois angles est $180^\circ$. Donc $\widehat{{ACB}}=180^\circ-({a}^\circ+{bb}^\circ)=180^\circ-{a+bb}^\circ={c}^\circ$.',rf'Les trois mesures sont ${a}^\circ$, ${bb}^\circ$ et ${c}^\circ$. On les compare à $90^\circ$ : '+(f'{c}° est supérieur à 90°, donc le triangle possède un angle obtus.' if c>90 else 'aucune ne dépasse 90°, donc le triangle ne possède pas d’angle obtus.'),rf'À la règle graduée, tracer le segment $[AB]$ de longueur {L} cm. Garder une place suffisante du côté choisi pour le sommet $C$.',rf'Au rapporteur, tracer en $A$ une demi-droite faisant ${a}^\circ$ avec $[AB)$, puis en $B$ une demi-droite faisant ${bb}^\circ$ avec $[BA)$, du même côté de $(AB)$. Leur intersection donne $C$.',r'Construire à l’équerre et au compas les médiatrices de deux côtés, par exemple $[AB]$ et $[AC]$. Leur intersection $O$ vérifie $OA=OB$ et $OA=OC$. Le cercle de centre $O$ et de rayon $OA$ passe ainsi par les trois sommets.',rf'Le schéma indique les données mais sa taille à l’écran dépend du support. Sur la construction réalisée à la règle et au rapporteur, contrôler $AB={L}$ cm, puis les angles de ${a}^\circ$, ${bb}^\circ$ et ${c}^\circ$.']
                nums={'L':L,'a':a,'b':bb,'c':c,'somme':a+bb+c}
            else:
                base,h=map(int,re.search(r'BC de (\d+) m.*mesure (\d+) m',enonce).groups());ar=base*h/2
                fig_name=fig(f'aire_{base}_{h}',aire(base,h));fig_corr=fig(f'aire_{base}_{h}_corrige',aire(base,h,True))
                details=[r'Une hauteur issue de $A$ passe par $A$ et est perpendiculaire à la droite $(BC)$. Son pied $H$ est sur cette droite : $(AH)\perp(BC)$.',rf'La base et la hauteur correspondante sont toutes deux en mètres : $\mathcal A_{{ABC}}=\frac{{BC\times AH}}{{2}}=\frac{{{base}\times{h}}}{{2}}={tex(ar)}$ m$^2$.',rf'$M$ est le milieu de $[BC]$, donc $BM=MC=BC\div2={base}\div2={tex(base/2)}$ m.',r'La droite $(AM)$ passe par le sommet $A$ et le milieu $M$ du côté opposé $[BC]$ : c’est la médiane issue de $A$.',rf'Les bases $BM$ et $MC$ mesurent toutes deux {tex(base/2)} m et sont portées par $(BC)$. Les deux triangles ont donc la même hauteur $AH={h}$ m. Chacune des aires vaut $\frac{{{tex(base/2)}\times{h}}}{{2}}={tex(ar/2)}$ m$^2$ ; leur somme vaut bien {tex(ar)} m$^2$.',r'La définition du milieu impose seulement $BM=MC$ et l’alignement de $B$, $M$, $C$. Elle ne donne aucun angle droit avec $(AM)$. La médiane ne serait aussi une hauteur que dans une configuration particulière, par exemple un triangle isocèle de sommet principal $A$.']
                nums={'base':base,'h':h,'aire':ar,'moitie_base':base/2,'moitie_aire':ar/2}
        else:
            x,y=map(int,re.search(r'A\((\d+) ; (\d+)\)',enonce).groups());central='centrale' in enonce;s=-1 if central else 1
            fig_name=fig(f'motif_{x}_{y}_enonce',symetrie(x,y,central));fig_corr=fig(f'motif_{x}_{y}_corrige',symetrie(x,y,central,True))
            enonce=enonce.replace('repère orthogonal,','repère orthogonal dont les deux axes ont la même unité de longueur,')
            details=[(r'Pour le demi-tour, tracer $(AO)$ puis reporter $OA$ de l’autre côté de $O$. On doit avoir $A$, $O$, $A\prime$ alignés et $OA\prime=OA$.' if central else r'Tracer la perpendiculaire à l’axe vertical passant par $A$. Son pied est $H(0\,;y_A)$. Reporter $HA$ de l’autre côté de l’axe pour que $H$ soit le milieu de $[AA\prime]$.'),rf'La symétrie '+('centrale change les deux signes' if central else 'd’axe vertical change le signe de l’abscisse et garde l’ordonnée')+rf' : $A({x}\,;{y})$ devient $A\prime(-{x}\,;{s*y})$.',rf'On applique la même règle à chaque sommet : $B({x+2}\,;{y})$ devient $B\prime(-{x+2}\,;{s*y})$ et $C({x}\,;{y+2})$ devient $C\prime(-{x}\,;{s*(y+2)})$.',rf'Les coordonnées donnent $AB={x+2}-{x}=2$ et $AC={y+2}-{y}=2$ unités. La symétrie conserve les longueurs : $A\prime B\prime=A\prime C\prime=2$ unités.',r'Le triangle est rectangle en $A$ car ses côtés $[AB]$ et $[AC]$ suivent les deux axes perpendiculaires. Son aire est $2\times2\div2=2$ unités d’aire. La symétrie conserve cette aire.',r'La même symétrie échange chaque point et son image. Une seconde application donne donc $A\prime\mapsto A$, $B\prime\mapsto B$ et $C\prime\mapsto C$ : on retrouve le triangle de départ.']
            nums={'x':x,'y':y,'central':central,'imageA':[-x,s*y],'imageB':[-x-2,s*y],'imageC':[-x,s*(y+2)],'AB':2,'AC':2,'aire':2}
        # Rebuild all six detailed reasoning sections, retaining the original method and result.
        sections=re.split(r'^## Question ',steps,flags=re.M)[1:]; assert len(sections)==6,(n,eid,len(sections))
        rebuilt=[]
        for i,sec in enumerate(sections):
            heading=sec.splitlines()[0]
            if n==273:heading=heading.replace('situé sur la même demi-droite de d','situé au-dessous de d et à droite de la sécante')
            method=re.search(r'::: methode[^\n]*\n(.*?)\n:::',sec,re.S)[1]
            result=re.search(r'::: resultat[^\n]*\n(.*?)\n:::',sec,re.S)[1]
            rebuilt.append('## Question '+heading+'\n\n'+box('methode',method.strip())+'\n'+box('etape',details[i],'Mise en œuvre')+'\n'+box('resultat',result.strip()))
        steps=MARK+'\n'+'\n'.join(rebuilt)
        if fig_name:
            mapfig('exercices',eid,1,fig_name,f'Figure de l’exercice {eid} : '+('coordonnées du jardin rectangulaire.' if n==272 else 'configuration géométrique et données de l’énoncé.'))
            mapfig('exercices',eid,2,fig_corr,f'Correction géométrique de l’exercice {eid}, à comparer aux calculs détaillés.')
            steps+='\n[IMAGE_2]\n'
        # Native data replace decorative recipe/price/fee images; no old image survives.
        enonce=re.sub(r'\n{3,}','\n\n',enonce).strip()
        out.append(head.strip()+'\n\nÉnoncé:\n'+enonce+'\n\nÉtapes:\n'+steps.strip()+'\n\nSolution:\n'+solution.strip())
        verif.append({'id':eid,'famille':title.split('. ',1)[-1],'donnees':nums,'source_enonce_sha256':hashlib.sha256(original_enonce.encode()).hexdigest()})
    (d/'exercices.txt').write_text('\n\n===\n\n'.join(out)+'\n',encoding='utf-8')
    fd=d/'figures';fd.mkdir(exist_ok=True)
    (fd/'figures.py').write_text('# -*- coding: utf-8 -*-\n"""Figures TikZ de la notion, préambule partagé par figures_livre.py."""\nFIGURES = {\n'+''.join(repr(k)+': r"""\n'+v+'\n""",\n' for k,v in figures.items())+'}\n',encoding='utf-8')
    (fd/'correspondance.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (d/'donnees_verification.json').write_text(json.dumps({'notion':n,'sources_sha256':source_hashes,'exercices':verif},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(n,len(out),'exercices',len(figures),'figures')
