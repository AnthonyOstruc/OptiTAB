"""Cours structurés et fiches de mémorisation compactes, programme de sixième 2025."""
COURSES={}
FICHES={}
COURSES[132]=r'''::: objectifs
- Comprendre une fraction comme un quotient exact.
- Compléter une multiplication et placer une fraction sur une demi-droite.
- Distinguer entier, décimal et nombre non décimal ; partager un segment.
:::

## I. Une fraction est un nombre
::: definition Fraction et quotient
Pour des entiers $a$ et $b$, avec $b\ne0$, la fraction $\frac ab$ désigne le quotient de $a$ par $b$. C’est le nombre qui, multiplié par $b$, donne $a$ :
$$b\times\frac ab=a.$$
$a$ est le **numérateur** ; $b$ est le **dénominateur**. Le dénominateur ne peut jamais être nul.
:::

::: exemple Trois quarts d’une unité ou un quart de trois unités
Partager 3 m de ruban en 4 parts égales donne $\frac34$ m par part. On obtient la même longueur en prenant 3 morceaux de $\frac14$ m.
$$3\div4=\frac34=3\times\frac14.$$
[IMAGE_1]
:::

::: methode Compléter une multiplication
Dans $7\times\square=3$, le nombre cherché est le quotient de 3 par 7 : $\square=\frac37$. On contrôle en multipliant : $7\times\frac37=3$.
:::

## II. Repérer une fraction
::: methode Graduer puis compter
1. Choisir une unité entre 0 et 1.
2. La partager en autant d’intervalles égaux que l’indique le dénominateur.
3. Depuis 0, compter le nombre d’intervalles indiqué par le numérateur.
Pour $\frac74$, chaque intervalle vaut un quart : il faut compter sept intervalles, donc dépasser 1.
[IMAGE_2]
:::

::: propriete Comparer à l’unité et encadrer
Pour des entiers positifs $a$ et $b$, $\frac ab$ est inférieur à 1 si $a<b$, égal à 1 si $a=b$, supérieur à 1 si $a>b$.
On peut regrouper des unités entières :
$$\frac74=\frac44+\frac34=1+\frac34.$$
Donc $1<\frac74<2$.
:::

## III. Une valeur exacte, plusieurs écritures
::: exemple Trois cas à distinguer
| Fraction | Nature et écriture |
|---|---|
| $\frac{12}{4}$ | Entier : $3$ |
| $\frac34$ | Décimal non entier : $0{,}75$ |
| $\frac13$ | Non décimal : la division ne se termine pas |
Pour $\frac13$, les écritures $0{,}3$, $0{,}33$ et $0{,}333$ sont seulement approchées : par exemple $3\times0{,}333=0{,}999\ne1$.
:::

::: retenir Écritures usuelles
$$\frac14=0{,}25,\quad\frac12=0{,}5,\quad\frac34=0{,}75.$$
$$\frac32=1{,}5,\quad\frac42=2,\quad\frac52=2{,}5.$$
Une fraction reste exacte même quand son écriture décimale ne se termine pas.
:::

## IV. Partager un segment avec un guide-âne
::: methode Sept parts égales sans mesurer un quotient approché
Le guide-âne est un réseau de droites parallèles régulièrement espacées. Pour partager un segment en sept parties égales :
1. Poser une extrémité sur une parallèle.
2. Faire pivoter le segment pour que l’autre extrémité soit sur la huitième parallèle : il traverse ainsi **sept intervalles**.
3. Marquer les six intersections intérieures, puis reporter ces marques sur le segment.
Un segment de 3 cm partagé de cette façon donne sept morceaux de $\frac37$ cm exactement.
[IMAGE_3]
:::

::: attention Compter les intervalles
Entre huit droites, il y a sept intervalles. Pour une graduation, compter les espaces, et non seulement les traits.
:::
'''
FICHES[132]=r'''## I. Quotient et sens
::: retenir
$$b\times\frac ab=a\qquad(b\ne0).$$
$\frac ab$ est le quotient exact $a\div b$. Exemple : $\frac34$ est trois quarts d’une unité, mais aussi le quart de 3 unités.
:::

## II. Se repérer
- Dénominateur : nombre d’intervalles égaux dans une unité.
- Numérateur : nombre de ces intervalles depuis 0.
- $\frac74=1+\frac34$ : entre 1 et 2.

## III. À mémoriser
$$\frac14=0{,}25,\quad\frac12=0{,}5,\quad\frac34=0{,}75.$$
$$\frac32=1{,}5,\quad\frac52=2{,}5.$$
::: attention
$\frac13$ n’est pas égal à $0{,}333$ : la fraction est exacte, le décimal est approché. Pour sept parts avec un guide-âne, intercepter sept intervalles, donc huit parallèles.
:::
'''
COURSES[134]=r'''::: objectifs
- Reconnaître une situation de proportionnalité dans un contexte.
- Utiliser multiplication, addition et retour à l’unité.
- Lire une échelle et distinguer longueurs du plan et longueurs réelles.
:::

## I. Reconnaître la proportionnalité
::: definition Deux grandeurs proportionnelles
Deux grandeurs sont proportionnelles quand on obtient les valeurs de l’une en multipliant les valeurs de l’autre par un même nombre. Dans un contexte de prix, cela signifie par exemple que le prix d’un kilogramme reste constant.
Doubler, tripler ou partager une quantité par deux fait alors subir le même changement à l’autre grandeur.
:::

::: exemple Un prix au kilogramme constant
2 kg de pommes coûtent 5 €. Si le prix est proportionnel à la masse, 6 kg coûtent trois fois plus :
$$6=3\times2\qquad15=3\times5.$$
Un prix de 13 € pour 6 kg serait incompatible avec cette proportionnalité.
:::

::: attention Une quantité fixe change la situation
Une livraison à 4 € fixes plus 2 € par colis coûte 6 € pour un colis et 8 € pour deux. Le nombre de colis double, mais le prix ne double pas : le prix total n’est pas proportionnel au nombre de colis.
:::

## II. Choisir une procédure
::: methode Multiplier, diviser ou additionner des quantités correspondantes
Si 4 croissants coûtent 3,60 € :
| Nombre de croissants | Prix (€) |
|---|---|
| 4 | 3,60 |
| 12 | 10,80 |
| 2 | 1,80 |
| 6 | 5,40 |
- De 4 à 12 : multiplier par 3 ; le prix est $3\times3{,}60=10{,}80$ €.
- De 4 à 2 : diviser par 2 ; le prix est $3{,}60\div2=1{,}80$ €.
- Pour 6 : ajouter 4 et 2 ; le prix est $3{,}60+1{,}80=5{,}40$ €.
:::

::: methode Revenir à l’unité
5 cahiers coûtent 7,50 €. Pour calculer le prix de 8 cahiers :
$$\begin{aligned}
\text{prix d’un cahier}&=7{,}50\div5=1{,}50\ \text{€},\\
\text{prix de huit cahiers}&=8\times1{,}50=12\ \text{€}.
\end{aligned}$$
On peut aussi retrouver une quantité : 18 € permettent d’acheter 12 cahiers, car $12\times1{,}50=18$.
:::

## III. Lire un plan à l’échelle
::: definition Échelle
Une échelle 1/100 signifie que **1 cm sur le plan représente 100 cm dans la réalité**. Toutes les longueurs sont réduites dans la même proportion. Les deux longueurs comparées doivent être exprimées dans la même unité.
:::

::: exemple Dans les deux sens
Sur une carte, 1 cm représente 50 m.
- Un trajet de 6,5 cm représente $6{,}5\times50=325$ m.
- Une distance réelle de 400 m occupe $400\div50=8$ cm sur la carte.
- Comme $50\ \mathrm{m}=5\,000\ \mathrm{cm}$, l’échelle est 1/5 000.
[IMAGE_1]
:::

::: retenir Contrôler sa réponse
Nommer chaque grandeur, conserver ses unités et vérifier le sens du changement. Un agrandissement du plan ne change pas la distance réelle ; il change l’échelle.
:::
'''
FICHES[134]=r'''## I. Reconnaître
::: retenir
En proportionnalité, doubler une grandeur double l’autre. Dans un achat au même tarif, le prix unitaire reste constant. Une somme fixe ajoutée empêche en général cette proportionnalité.
:::

## II. Calculer
- Multiplier ou diviser les deux quantités par le même nombre.
- Additionner des quantités correspondantes.
- Revenir à l’unité : $7{,}50\div5=1{,}50$ € par cahier, donc 8 cahiers coûtent $8\times1{,}50=12$ €.

## III. Une échelle
1/100 : 1 cm de plan pour 100 cm réels.
Si 1 cm représente 50 m : 6,5 cm représentent 325 m ; 400 m occupent 8 cm.
::: attention
Écrire les longueurs dans la même unité pour lire une échelle. 1 cm pour 50 m correspond à 1/5 000.
:::
'''
COURSES[135]=r'''::: objectifs
- Choisir et convertir des unités de longueur.
- Calculer les périmètres d’un polygone, d’un rectangle, d’un carré et d’un disque.
- Reconnaître le contour extérieur d’une figure composée et résoudre un problème d’achat.
:::

## I. Mesurer et convertir une longueur
::: definition Les unités usuelles
Du plus grand au plus petit : km, hm, dam, m, dm, cm, mm. Entre deux unités voisines, le nombre qui mesure une même longueur est multiplié ou divisé par 10.
$$1\ \mathrm{km}=1\,000\ \mathrm{m},\quad1\ \mathrm{m}=100\ \mathrm{cm},\quad1\ \mathrm{cm}=10\ \mathrm{mm}.$$
Un crayon se mesure couramment en centimètres, une pièce en mètres et un trajet entre villes en kilomètres.
:::

::: exemple Choisir le bon sens
$$\begin{aligned}
3{,}7\ \mathrm{km}&=3{,}7\times1\,000\ \mathrm{m}=3\,700\ \mathrm{m},\\
45\ \mathrm{cm}&=45\div100\ \mathrm{m}=0{,}45\ \mathrm{m}.
\end{aligned}$$
Passer à une unité plus petite augmente le nombre qui mesure la même longueur.
:::

## II. Le contour d’un polygone
::: definition Périmètre
Le périmètre est la longueur du contour d’une figure plane. Pour un polygone, additionner tous les côtés extérieurs, exprimés dans la même unité. On peut mesurer les côtés avec une règle ou reporter les longueurs au compas pour les additionner sur une ligne.
:::

::: propriete Carré et rectangle
Pour un carré de côté $c$ : $P=4\times c$.
Pour un rectangle de longueur $L$ et de largeur $\ell$ :
$$P=2\times(L+\ell).$$
Un rectangle de 2 m sur 80 cm a une largeur de 0,8 m, donc $P=2\times(2+0{,}8)=5{,}6$ m.
[IMAGE_1]
:::

::: methode Retrouver un côté
Un rectangle de périmètre 22 cm a un demi-périmètre de $22\div2=11$ cm. Si sa longueur est 8 cm, sa largeur vaut $11-8=3$ cm. Contrôle : $2\times(8+3)=22$.
:::

## III. Le périmètre d’un disque
::: propriete Diamètre, rayon et nombre π
Si le rayon est $r$, le diamètre vaut $d=2\times r$. Le périmètre du disque est proportionnel à son diamètre :
$$P=\pi\times d=2\times\pi\times r.$$
Le nombre $\pi$ est un nombre non décimal ; $3{,}14$ en est une valeur approchée.
:::

::: exemple Exact ou approché
Pour un diamètre de 10 cm, $P=10\pi$ cm exactement.
En prenant $\pi\approx3{,}14$, on obtient $P\approx31{,}4$ cm.
[IMAGE_2]
:::

## IV. Figures composées et décisions
::: methode Suivre uniquement le bord extérieur
Un rectangle de 6 cm sur 4 cm prolongé par un demi-disque de diamètre 4 cm a un contour droit de $6+4+6=16$ cm. La partie courbe mesure la moitié de $4\pi$, soit $2\pi$ cm.
$$P=16+2\pi\ \mathrm{cm}\approx22{,}28\ \mathrm{cm}.$$
Le diamètre commun aux deux morceaux est intérieur : on ne l’ajoute pas.
[IMAGE_3]
:::

::: attention Adapter le résultat au contexte
Pour 22 m de bordure vendue en lots de 3 m, 7 lots ne donnent que 21 m. Il faut 8 lots, soit 24 m achetés et 2 m inutilisés. Un nombre de lots est entier.
Le périmètre est une longueur : utiliser m, cm… et non m² ou cm².
:::
'''
FICHES[135]=r'''## I. Unités
$$1\ \mathrm{km}=1\,000\ \mathrm{m},\quad1\ \mathrm{m}=100\ \mathrm{cm},\quad1\ \mathrm{cm}=10\ \mathrm{mm}.$$
Unifier les unités avant toute addition.

## II. Contours à connaître
::: retenir
- Polygone : somme des côtés extérieurs.
- Carré : $P=4\times c$.
- Rectangle : $P=2\times(L+\ell)$.
- Disque : $P=\pi\times d=2\times\pi\times r$.
:::

## III. Contrôles
- $d=2\times r$ : ne pas confondre rayon et diamètre.
- $10\pi$ cm est exact ; 31,4 cm est approché.
- Figure composée : les frontières intérieures ne comptent pas.
- Achat par lots : retenir le premier nombre entier de lots suffisant.
::: attention
Un périmètre se mesure en unités de longueur, jamais en unités carrées.
:::
'''
COURSES[136]=r'''::: objectifs
- Comprendre et calculer la longueur d’un contour.
- Utiliser les formules du carré, du rectangle et du disque.
- Retrouver une dimension, suivre un contour composé et prendre une décision.
:::

## I. Qu’est-ce qu’un périmètre ?
::: definition
Le **périmètre** d’une figure plane est la longueur de son contour. Pour un polygone, parcourir le bord et additionner chacun de ses côtés une seule fois.
Il s’exprime en unités de longueur : mm, cm, m, km…
:::

::: exemple Un contour irrégulier
Un pentagone a des côtés de 4 cm, 5 cm, 6 cm, 4 cm et 7 cm :
$$P=4+5+6+4+7=26\ \mathrm{cm}.$$
On ne multiplie pas un côté par cinq, car les côtés ne sont pas tous égaux.
[IMAGE_1]
:::

::: methode Mesurer et reporter
Avec une règle, mesurer chaque côté dans la même unité. Avec un compas, on peut reporter les longueurs les unes à la suite des autres sur une demi-droite, puis mesurer la longueur totale. Un dessin non annoncé à l’échelle ne doit pas servir à mesurer les données.
:::

## II. Carré, rectangle et unités communes
::: propriete Formules issues du contour
- Carré de côté $c$ : quatre côtés égaux, donc $P=4\times c$.
- Rectangle de longueur $L$ et de largeur $\ell$ : deux longueurs et deux largeurs, donc $P=2\times(L+\ell)$.
:::

::: exemple Deux calculs
$$\begin{aligned}
P_{\mathrm{carré}}&=4\times5=20\ \mathrm{cm},\\
P_{\mathrm{rectangle}}&=2\times(8+3)=22\ \mathrm{cm}.
\end{aligned}$$
Si des côtés sont donnés en unités différentes, convertir avant d’additionner. Exemple : $40\ \mathrm{mm}=4\ \mathrm{cm}$ et $0{,}06\ \mathrm{m}=6\ \mathrm{cm}$ ; avec un troisième côté de 5 cm, le triangle a un périmètre de $4+5+6=15$ cm.
:::

::: methode Retrouver une dimension
Un carré de périmètre 24 cm a un côté de $24\div4=6$ cm.
Un rectangle de périmètre 22 cm a un demi-périmètre de $22\div2=11$ cm. Si sa longueur vaut 8 cm, sa largeur vaut $11-8=3$ cm.
Toujours contrôler en recalculant le périmètre.
:::

## III. Le contour d’un disque
::: propriete
Le diamètre vaut deux fois le rayon. Le périmètre du disque est proportionnel au diamètre :
$$P=\pi\times d=2\times\pi\times r.$$
Pour un rayon de 3 cm, le diamètre est 6 cm et le périmètre vaut $6\pi$ cm. Avec $\pi\approx3{,}14$, on trouve $P\approx18{,}84$ cm.
[IMAGE_2]
:::

::: attention Exactitude
$\pi$ n’est pas égal à 3,14. Écrire $=$ pour la formule exacte avec π et $\approx$ pour l’estimation décimale.
:::

## IV. Contours composés et problèmes
::: methode Suivre un détour
Une encoche de largeur 2 cm et de profondeur 1 cm remplace un bord droit de 2 cm par trois segments de longueurs 1 cm, 2 cm et 1 cm. Le contour gagne donc $1+2+1-2=2$ cm.
Sur un rectangle de 8 cm sur 5 cm, le périmètre passe de $2\times(8+5)=26$ cm à $26+2=28$ cm.
[IMAGE_3]
:::

::: methode Organiser un problème de clôture
Pour entourer un terrain de 9 m sur 6 m avec une entrée de 2 m :
1. Calculer le périmètre : $2\times(9+6)=30$ m.
2. Retirer l’ouverture : $30-2=28$ m à poser.
3. Si un rouleau mesure 5 m, 5 rouleaux donnent seulement 25 m ; il faut 6 rouleaux, soit 30 m achetés.
4. Calculer le reste : $30-28=2$ m.
:::

::: retenir
Le périmètre mesure le bord ; l’aire mesure la surface intérieure. Une encoche peut réduire la surface tout en allongeant le contour. Dans une figure assemblée, une frontière intérieure ne compte pas dans le périmètre.
:::
'''
FICHES[136]=FICHES[135]
COURSES[137]=r'''::: objectifs
- Comparer des surfaces et mesurer une aire avec une unité choisie.
- Utiliser les unités cm², dm² et m² et effectuer des conversions.
- Calculer l’aire d’un rectangle, d’un carré et de surfaces découpées.
:::

## I. Comparer avant de mesurer
::: definition Aire
L’aire mesure l’étendue d’une surface. On peut comparer deux aires sans nombre : par superposition, ou par découpage et recollement sans chevauchement ni perte. Déplacer ou retourner un morceau ne change pas son aire.
:::

::: exemple Découper et recoller
Les mêmes quatre carrés peuvent former un carré plus grand ou une bande : leur aire totale reste celle de quatre petits carrés, même si les contours diffèrent.
[IMAGE_1]
:::

::: methode Compter avec une unité
Choisir un carreau comme unité d’aire et paver la surface sans trou ni chevauchement. Additionner les carreaux entiers et regrouper les demi-carreaux deux par deux. Avec 8 carreaux et 6 demi-carreaux, l’aire vaut $8+6\div2=11$ unités d’aire.
:::

## II. Comprendre les unités carrées
::: definition
1 cm² est l’aire d’un carré de côté 1 cm. De même, 1 dm² est l’aire d’un carré de côté 1 dm et 1 m² celle d’un carré de côté 1 m.
:::

::: propriete Convertir des aires
Un carré de 1 dm de côté mesure 10 cm sur 10 cm et contient 100 carrés de 1 cm de côté.
$$1\ \mathrm{dm}^2=100\ \mathrm{cm}^2.$$
$$1\ \mathrm{m}^2=100\ \mathrm{dm}^2=10\,000\ \mathrm{cm}^2.$$
Donc $1\ \mathrm{cm}^2=0{,}01\ \mathrm{dm}^2$ et $1\ \mathrm{dm}^2=0{,}01\ \mathrm{m}^2$.
[IMAGE_2]
:::

::: exemple Changer d’unité dans les deux sens
$$\begin{aligned}
3{,}5\ \mathrm{dm}^2&=350\ \mathrm{cm}^2,\\
750\ \mathrm{cm}^2&=7{,}5\ \mathrm{dm}^2.
\end{aligned}$$
Entre cm² et dm², le facteur est 100, et non 10 : on convertit une surface, pas un côté.
:::

## III. Rectangle et carré
::: propriete Les formules viennent du pavage
Un rectangle de longueur $L$ et de largeur $\ell$ a pour aire :
$$A=L\times\ell.$$
Un carré de côté $c$ a pour aire $A=c\times c$. Les deux dimensions doivent être dans la même unité ; le résultat est dans l’unité carrée correspondante.
:::

::: exemple Dimensions décimales
Un rectangle de 3,5 m sur 2 m a une aire de $3{,}5\times2=7$ m². Un carré de côté 2,5 m a une aire de $2{,}5\times2{,}5=6{,}25$ m².
:::

## IV. Découper une surface et distinguer les grandeurs
::: methode Ajouter ou retirer des aires
Un rectangle de 8 cm sur 5 cm auquel on retire un coin de 3 cm sur 2 cm a pour aire :
$$\begin{aligned}
A&=8\times5-3\times2\\
&=40-6\\
&=34\ \mathrm{cm}^2.
\end{aligned}$$
On peut aussi découper la surface restante en deux rectangles : $8\times3+5\times2=34$ cm².
[IMAGE_3]
:::

::: attention Aire et périmètre
Un carré de côté 4 cm et un rectangle de 6 cm sur 2 cm ont le même périmètre de 16 cm, mais leurs aires sont 16 cm² et 12 cm². Même périmètre ne signifie pas même aire.
:::
'''
FICHES[137]=r'''## I. Une surface, une unité carrée
Comparer par superposition ou découpage-recollement. Sur un quadrillage, compter les carreaux et réunir les demi-carreaux deux par deux.

## II. Formules et conversions
::: retenir
- Rectangle : $A=L\times\ell$.
- Carré : $A=c\times c$.
- $1\ \mathrm{m}^2=100\ \mathrm{dm}^2=10\,000\ \mathrm{cm}^2$.
- $1\ \mathrm{dm}^2=100\ \mathrm{cm}^2$.
:::
Dimensions dans la même unité avant le produit ; aire exprimée dans l’unité carrée correspondante.

## III. Une surface composée
Ajouter des aires de morceaux sans chevauchement, ou retirer l’aire d’une partie découpée.
::: attention
Une aire n’est pas un périmètre. Entre cm² et dm², multiplier ou diviser par 100, et non par 10.
:::
'''
COURSES[284]=r'''::: objectifs
- Établir des fractions égales, comparer et encadrer des fractions.
- Additionner, soustraire et multiplier une fraction par un entier.
- Appliquer une fraction à une quantité et résoudre ou inventer un problème.
:::

## I. Écrire le même nombre autrement
::: propriete Fractions égales
On conserve une fraction en multipliant ou divisant son numérateur et son dénominateur par un même nombre non nul.
$$\frac23=\frac{2\times4}{3\times4}=\frac8{12}.$$
$$\frac{18}{24}=\frac{18\div6}{24\div6}=\frac34.$$
Simplifier consiste à obtenir des termes plus petits, sans changer le nombre représenté.
[IMAGE_1]
:::

::: attention
Ajouter le même nombre aux deux termes ne conserve pas la fraction : $\frac23\ne\frac45$.
:::

## II. Comparer, encadrer et ranger
::: methode Choisir une comparaison adaptée
- Même dénominateur : comparer les numérateurs. $\frac58<\frac78$.
- Même numérateur positif : des parts plus petites donnent une fraction plus petite. $\frac49<\frac45$.
- Sinon, chercher un dénominateur commun : $\frac56=\frac{10}{12}>\frac7{12}$.
:::

::: exemple Ranger des nombres mixtes
$$\frac74=\frac{14}8,\quad\frac32=\frac{12}8,\quad1+\frac18=\frac98.$$
Donc $1+\frac18<\frac32<\frac74$. Tous ces nombres sont entre 1 et 2 : leurs numérateurs en huitièmes sont entre 8 et 16.
:::

## III. Additionner et soustraire
::: methode Compter des parts de même taille
1. Écrire les fractions avec un même dénominateur.
2. Additionner ou soustraire les numérateurs ; garder le dénominateur commun.
3. Simplifier si c’est utile.
$$\frac3{10}+\frac4{10}=\frac7{10},\qquad\frac78-\frac38=\frac48=\frac12.$$
:::

::: exemple Dénominateurs différents
$$\begin{aligned}
\frac23+\frac14&=\frac8{12}+\frac3{12}\\
&=\frac{11}{12}.
\end{aligned}$$
Pour retrancher une fraction de 1, écrire aussi l’unité avec le bon dénominateur : $1-\frac35=\frac55-\frac35=\frac25$.
:::

## IV. Multiplier par un entier et prendre une fraction
::: propriete
Multiplier une fraction par un entier revient à multiplier son numérateur par cet entier :
$$5\times\frac23=\frac{5\times2}{3}=\frac{10}{3}.$$
On peut lire le produit dans l’autre sens : $\frac23\times5$ est aussi « les deux tiers de 5 ».
:::

::: methode Une fraction d’une quantité
Pour prendre $\frac23$ de 12 œufs, partager 12 en trois parts égales et en prendre deux :
$$12\times\frac23=(12\div3)\times2=8.$$
De même, les $\frac34$ de 10 m valent $(10\div4)\times3=7{,}5$ m.
:::

## V. Donner du sens à un problème
::: exemple Lire puis inventer
Un livre a 120 pages. Lire un tiers du livre le lundi puis un quart du **même livre initial** le mardi, sans relire de pages, revient à lire :
$$\frac13+\frac14=\frac7{12}.$$
Cela représente $120\times\frac7{12}=70$ pages, donc il en reste $120-70=50$.
Pour inventer un problème, préciser le tout de référence, le sens des fractions et la question posée.
:::

::: attention
« Un quart de ce qui reste » n’a pas la même référence que « un quart du total initial ». Avant d’additionner, vérifier que les fractions portent sur le même tout et sur des parties distinctes.
:::
'''
FICHES[284]=r'''## I. Égalité et comparaison
Multiplier ou diviser les deux termes par le même nombre non nul : $\frac23=\frac8{12}$, $\frac{18}{24}=\frac34$.
- Même dénominateur : comparer les numérateurs.
- Même numérateur positif : plus le dénominateur est grand, plus la fraction est petite.
- Sinon, chercher un dénominateur commun.

## II. Opérations
::: retenir
$$\frac23+\frac14=\frac8{12}+\frac3{12}=\frac{11}{12}.$$
$$1-\frac35=\frac25,\qquad5\times\frac23=\frac{10}3.$$
$$\frac23\text{ de }12=(12\div3)\times2=8.$$
:::

::: attention
On n’additionne pas les dénominateurs. Dans un problème, identifier le même tout de référence avant de comparer ou d’additionner des fractions.
:::
'''
COURSES[285]=r'''::: objectifs
- Relier pourcentage, fraction sur 100 et nombre décimal.
- Calculer une proportion simple et appliquer un pourcentage.
- Identifier le total de référence et distinguer pourcentage et effectif.
:::

## I. Comprendre « pour cent »
::: definition
$p\,\%$ signifie $\frac p{100}$. Un pourcentage exprime une proportion, pas un effectif :
$$35\,\%=\frac{35}{100}=0{,}35.$$
100 % représente le tout de référence. 0 % représente aucune part de ce tout.
[IMAGE_1]
:::

::: retenir Repères usuels
| Pourcentage | Fraction |
|---|---|
| 50 % | $\frac12$ |
| 25 % | $\frac14$ |
| 75 % | $\frac34$ |
| 10 % | $\frac1{10}$ |
| 20 % | $\frac15$ |
8 % vaut $\frac8{100}=0{,}08$, et non 0,8.
:::

## II. Calculer une proportion
::: methode Partie sur tout
1. Identifier la partie étudiée et l’effectif total.
2. Écrire la fraction $\frac{\text{partie}}{\text{tout}}$.
3. L’écrire avec un dénominateur 100 dans les cas simples.
:::

::: exemple Neuf élèves sur vingt-cinq
Dans une classe de 25 élèves, 9 viennent à vélo :
$$\frac9{25}=\frac{9\times4}{25\times4}=\frac{36}{100}=36\,\%.$$
Les autres représentent $100-36=64\,\%$, soit $25-9=16$ élèves.
:::

## III. Appliquer un pourcentage
::: methode Une fraction du nombre total
Pour calculer $p\,\%$ d’un nombre, multiplier ce nombre par $\frac p{100}$. Le résultat garde l’unité ou la nature de la quantité initiale.
Pour 30 % de 80 membres :
$$80\times\frac{30}{100}=24.$$
Mentalement : 10 % de 80 vaut 8 ; 30 % vaut $3\times8=24$.
[IMAGE_2]
:::

::: exemple Une remise
Un sac coûte 80 € et sa remise est de 25 %. La remise vaut le quart du prix, soit $80\div4=20$ €. Le prix restant est $80-20=60$ €, soit 75 % du prix initial. Des frais de livraison de 5 € ajoutés ensuite portent le total à 65 €.
:::

## IV. Toujours nommer le tout
::: attention Pourcentage plus grand, quantité parfois plus petite
50 % de 20 élèves représente 10 élèves ; 40 % de 30 élèves représente 12 élèves. Le plus grand pourcentage ne donne pas forcément le plus grand effectif quand les groupes sont différents.
On ne peut pas additionner directement les pourcentages de deux groupes différents : il faut revenir aux quantités.
:::

::: retenir Contrôler
Pour une partie d’un groupe, le pourcentage est entre 0 % et 100 % et l’effectif obtenu ne dépasse pas l’effectif total. Pour une même proportion, doubler le total double la partie.
:::
'''
FICHES[285]=r'''## I. Trois écritures
::: retenir
$$p\,\%=\frac p{100}.$$
$50\,\%=\frac12$, $25\,\%=\frac14$, $75\,\%=\frac34$, $10\,\%=\frac1{10}$, $20\,\%=\frac15$.
:::

## II. Deux questions différentes
- **Calculer une proportion** : partie divisée par tout. Exemple : $\frac9{25}=\frac{36}{100}=36\,\%$.
- **Appliquer un pourcentage** : total multiplié par la proportion. Exemple : 30 % de 80 vaut $80\times\frac{30}{100}=24$.
- Partie complémentaire : $100-p$ pour cent.

::: attention
Toujours nommer le tout de référence. 50 % de 20 donne 10, mais 40 % de 30 donne 12. Un plus grand pourcentage ne signifie pas toujours une plus grande quantité.
:::
'''

for n,d in DIRS.items():
    meta=json.loads((d/'source_en_ligne'/'meta.json').read_text(encoding='utf-8'))
    c=meta['cours'][0]
    (d/f"cours_{c['id']}.txt").write_text('Titre: '+c['titre']+'\n'+MARK+'\n'+COURSES[n],encoding='utf-8')
    filename=f"fiche_{meta['fiches'][0]['id']}.txt" if meta['fiches'] else 'fiche_nouvelle.txt'
    (d/filename).write_text('Titre: '+meta['titre']+'\n'+MARK+'\n'+FICHES[n],encoding='utf-8')
