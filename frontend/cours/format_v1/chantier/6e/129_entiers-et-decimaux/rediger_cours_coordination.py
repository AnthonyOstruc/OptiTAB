"""Cours et synthèses du lot numérique 6e ; même structure que les niveaux validés."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent.parent
MARK='<!-- optitab:1 -->'
COURS={}
FICHES={}
COURS[129]=r'''
::: objectifs
- Lire et écrire les grands nombres jusqu’aux milliards.
- Distinguer un chiffre, sa valeur et le nombre de parts d’un rang.
- Relier unités, dixièmes, centièmes et millièmes.
- Passer entre écriture décimale, fraction décimale et nombre mixte.
:::

::: prerequis
Savoir lire un entier et connaître les liens entre unités, dizaines et centaines.
:::

## I. Lire les grands nombres

::: definition Chiffres et classes
Les dix chiffres 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 servent à écrire les nombres. La valeur d’un chiffre dépend de son rang. Pour lire un entier, on regroupe les chiffres par classes de trois en partant de la droite : unités, milliers, millions et milliards.
:::

| Milliards | Millions | Milliers | Unités |
|---|---|---|---|
| 7 | 342 | 015 | 608 |

Le nombre $7\,342\,015\,608$ se lit « sept milliards trois cent quarante-deux millions quinze mille six cent huit ». Les zéros de la classe 015 gardent la place des rangs, mais on lit « quinze mille ».

::: propriete Regrouper par dix et par mille
Une dizaine contient 10 unités ; une centaine, 100 unités ; un millier, 1 000 unités. Une classe située à gauche vaut mille fois celle qui la suit.

$$1\,000\,000\,000=1\,000\times1\,000\,000$$

Un milliard correspond à mille millions.
:::

::: methode Décomposer par classes
1. Séparer les groupes de trois depuis la droite.
2. Donner à chaque groupe son unité : milliard, million, millier, unité.
3. Additionner les contributions ; une classe nulle peut être omise dans la somme.
:::

::: exemple
$$
\begin{aligned}
7\,342\,015\,608&=7\times1\,000\,000\,000\\
&\quad+342\times1\,000\,000\\
&\quad+15\times1\,000+608
\end{aligned}
$$
:::

## II. Distinguer chiffre et nombre de parts

Dans $7\,342\,015\,608$, le chiffre des millions est 2. Sa contribution au nombre est $2\,000\,000$. Mais le nombre de millions entiers est $7\,342$ : les 7 milliards contiennent déjà 7 000 millions.

::: attention Trois questions différentes
« Quel chiffre ? » demande un symbole de 0 à 9. « Quelle valeur ? » demande sa contribution au nombre. « Combien de millions entiers ? » demande tous les groupes complets d’un million.
:::

::: exemple Vérifier une retenue
Si un compteur passe de $999\,999\,500$ à $1\,000\,000\,500$ après un ajout de 1 000, la retenue se propage vers les millions puis les milliards. On ne change pas seulement un chiffre : on additionne dans le bon rang.
:::

## III. Partager l’unité en dixièmes, centièmes et millièmes

::: definition Unités de numération
Un dixième est une des dix parts égales d’une unité ; un centième correspond à une part sur cent ; un millième à une part sur mille.

$$1=\frac{10}{10}=\frac{100}{100}=\frac{1\,000}{1\,000}$$
$$\frac1{10}=\frac{10}{100},\qquad\frac1{100}=\frac{10}{1\,000}$$
:::

[IMAGE_1]

| Rang dans $4{,}107$ | Chiffre | Valeur |
|---|---|---|
| Unités | 4 | $4$ |
| Dixièmes | 1 | $0{,}1$ |
| Centièmes | 0 | $0$ |
| Millièmes | 7 | $0{,}007$ |

::: exemple Lire une écriture décimale
$4{,}107$ contient 4 unités, 1 dixième, 0 centième et 7 millièmes. Il contient aussi 41 dixièmes entiers, 410 centièmes entiers ou 4 107 millièmes. Le chiffre des centièmes est 0 ; le nombre de centièmes entiers est 410.
:::

## IV. Reconnaître un nombre décimal

::: definition Nombre décimal
Un nombre décimal peut s’écrire sous la forme d’une fraction dont le numérateur est entier et le dénominateur vaut 1, 10, 100, 1 000… Il possède une écriture à virgule qui se termine.
:::

::: exemple
$7=\frac71=\frac{70}{10}$ : un entier est aussi un nombre décimal. $\frac34=\frac{75}{100}=0{,}75$ est décimal, même si sa première écriture n’est pas une fraction décimale.
:::

::: attention Une fraction n’est pas toujours décimale
$\frac13=0{,}333\ldots$ : les chiffres 3 se poursuivent indéfiniment. $0{,}33$ est une valeur approchée, pas la valeur exacte : $0{,}33\times3=0{,}99$, différent de 1.
:::

## V. Changer d’écriture sans changer de nombre

::: methode De la virgule à la fraction
Lire le dernier rang écrit : si le nombre se termine aux millièmes, l’écrire comme un nombre entier de millièmes. Ajouter des zéros finaux permet de choisir un dénominateur plus grand.
:::

::: exemple
$$0{,}045=\frac{45}{1\,000}$$
$$4{,}107=\frac{4\,107}{1\,000}$$
$$4{,}107=4+\frac{107}{1\,000}$$
La dernière écriture sépare les unités entières et une fraction inférieure à 1 : c’est un nombre mixte.
:::

::: methode De la fraction décimale à la virgule
Un dénominateur 100 signifie que chaque unité est partagée en 100 parts. On place les chiffres en comptant les rangs, en complétant les rangs vides par zéro : $\frac{2\,375}{100}=23{,}75$ et $\frac8{1\,000}=0{,}008$.
:::

::: attention Les zéros n’ont pas tous le même rôle
$2{,}5=2{,}50=2{,}500$. Les zéros ajoutés à droite après la virgule ne changent pas le nombre. En revanche, $2{,}05\ne2{,}5$ : le zéro intérieur réserve le rang des dixièmes.
:::

## VI. Donner du sens avec une mesure

::: exemple Litres et millilitres
Une bouteille contient 2 L et 75 mL. Puisque 1 L vaut 1 000 mL, la contenance vaut $2\,075$ mL, soit $\frac{2\,075}{1\,000}=2{,}075$ L. L’écriture $2{,}75$ L désignerait 2 L et 750 mL : elle ne convient pas.
:::

::: retenir
La position donne la valeur d’un chiffre. Lire les classes pour les grands entiers, les rangs pour les décimaux. Une fraction décimale permet de passer d’une unité de numération à une écriture à virgule. Les zéros intérieurs sont essentiels ; les zéros finaux après la virgule sont facultatifs.
:::
'''
COURS[130]=r'''
::: objectifs
- Lire et placer des abscisses décimales sur une graduation régulière.
- Comparer, ranger, encadrer et intercaler des décimaux.
- Arrondir à l’unité, au dixième et au centième.
- Distinguer une valeur exacte d’une valeur approchée.
:::

::: prerequis
Lire les rangs décimaux et comprendre que $2{,}5=2{,}50$.
:::

## I. Comprendre une demi-droite graduée

::: definition Origine, unité et abscisse
Une demi-droite graduée possède une origine repérée par 0, un sens et une unité de longueur. L’unité est reportée régulièrement. Le nombre qui repère un point est son abscisse. Une représentation agrandie peut ne montrer qu’une portion de cette demi-droite.
:::

[IMAGE_1]

::: methode Calculer le pas d’une graduation
1. Repérer deux valeurs connues.
2. Calculer leur écart.
3. Compter les intervalles égaux qui les séparent.
4. Diviser l’écart par ce nombre d’intervalles.
:::

::: exemple
Entre 2 et 3, dix intervalles égaux valent chacun $(3-2)\div10=0{,}1$. Trois intervalles après 2 donnent $2+3\times0{,}1=2{,}3$.
:::

::: attention Compter les espaces
Dix intervalles ont onze traits d’extrémité. Diviser par le nombre de traits donne un pas faux. Vérifier en multipliant le pas par le nombre d’intervalles : on doit retrouver l’écart total.
:::

Pour placer un point, on part d’une graduation connue, puis on avance du bon nombre d’intervalles. Si le nombre demandé ne tombe pas sur les traits disponibles, on peut affiner la graduation : les traits ne représentent pas tous les nombres possibles.

## II. Comparer deux nombres décimaux

::: propriete Comparaison rang par rang
On compare d’abord les parties entières. Si elles sont égales, on compare les dixièmes, puis les centièmes, puis les millièmes. Le premier rang différent décide de l’ordre.
:::

::: exemple
$12{,}7=12{,}70$ et $12{,}69$ ont la même partie entière. Le chiffre des dixièmes vaut 7 dans le premier nombre et 6 dans le second : $12{,}7\gt12{,}69$.
:::

::: notation Les signes de comparaison
$a\lt b$ signifie que $a$ est strictement inférieur à $b$. $a\le b$ signifie que $a$ est inférieur ou égal à $b$. Les signes $\gt$ et $\ge$ expriment les relations inverses. Ainsi $2{,}5\le2{,}50$ est vrai, car les deux nombres sont égaux.
:::

::: attention Une virgule ne sépare pas deux entiers indépendants
$0{,}8=0{,}80\gt0{,}75$. Comparer 8 et 75 ne convient pas : 8 désigne ici des dixièmes, et 75 des centièmes. Il faut comparer des parts de même taille.
:::

::: methode Ranger plusieurs mesures
Choisir un sens : ordre croissant du plus petit au plus grand, ou décroissant du plus grand au plus petit. Compléter si nécessaire avec des zéros, repérer les égalités, puis vérifier chaque comparaison voisine.
:::

::: exemple
$$3{,}08\lt3{,}8=3{,}80\lt3{,}805$$
Les écritures $3{,}8$ et $3{,}80$ représentent un même nombre et ne doivent pas être séparées par une inégalité stricte.
:::

## III. Encadrer à une précision donnée

::: definition Encadrement
Encadrer un nombre consiste à le situer entre deux bornes. Pour un encadrement à l’unité, on utilise des entiers consécutifs ; au dixième, deux dixièmes consécutifs ; au centième, deux centièmes consécutifs.
:::

::: exemple
Pour $3{,}476$ :

$$3\lt3{,}476\lt4$$
$$3{,}4\lt3{,}476\lt3{,}5$$
$$3{,}47\lt3{,}476\lt3{,}48$$

Chaque nouvel encadrement précise la position du nombre.
:::

::: remarque Cas où le nombre est une borne
Pour $3{,}40$, écrire $3{,}4\le3{,}40\lt3{,}5$ est correct. On ne doit pas imposer une inégalité stricte entre deux écritures égales. Les consignes peuvent aussi demander un encadrement strict : on choisit alors des bornes appropriées.
:::

## IV. Intercaler un autre nombre

::: methode Affiner les rangs
Entre $2{,}30$ et $2{,}31$, il n’existe pas de centième supplémentaire. Mais $2{,}305$ est un millième situé entre eux. Le nombre de chiffres disponibles dans une écriture ne limite pas les nombres qui existent.
:::

::: exemple Prendre le milieu
Le milieu entre deux nombres distincts est leur somme divisée par 2 :

$$\frac{2{,}30+2{,}31}{2}=2{,}305$$

On peut recommencer entre $2{,}30$ et $2{,}305$ : leur milieu est $2{,}3025$.
:::

## V. Choisir l’arrondi le plus proche

::: definition Arrondi
L’arrondi à un rang donné est le nombre le plus proche écrit à ce rang. Lorsque le nombre se trouve exactement au milieu des deux valeurs possibles, on choisit ici la valeur supérieure, convention utilisée dans ce cours pour les nombres positifs.
:::

::: methode Lire le chiffre suivant
- Repérer le rang demandé.
- Regarder le chiffre immédiatement à droite.
- S’il vaut 0, 1, 2, 3 ou 4, conserver la borne inférieure.
- S’il vaut 5, 6, 7, 8 ou 9, choisir la borne supérieure, en effectuant les retenues.
:::

[IMAGE_2]

::: exemple
$7{,}364$ s’arrondit à 7 à l’unité, à $7{,}4$ au dixième et à $7{,}36$ au centième. Pour $2{,}995$, l’arrondi au centième est $3{,}00$ : on ajoute un centième à $2{,}99$.
:::

::: attention Repartir du nombre initial
Pour arrondir à l’unité, ne pas arrondir d’abord au dixième : $2{,}46$ a pour arrondi au dixième $2{,}5$, mais son arrondi à l’unité est 2. Arrondir $2{,}5$ à l’unité donnerait 3 et fausserait le résultat.
:::

## VI. Valeur exacte et décision

::: exemple
$\frac13$ n’a pas d’écriture décimale finie. On écrit $\frac13\approx0{,}33$ au centième, avec le signe d’approximation et non le signe égal. De même, $\pi$ est proche de $3{,}14$, sans être égal à $3{,}14$.
:::

Un arrondi est utile pour communiquer une mesure. Mais un seuil exige parfois la valeur précise : $12{,}495\lt12{,}5$, même si l’arrondi au dixième de la première mesure vaut $12{,}5$.

::: retenir
Identifier le pas, comparer rang par rang, distinguer les égalités. Un encadrement donne deux bornes ; un arrondi donne une valeur proche. Toujours arrondir à partir du nombre initial et conserver la précision nécessaire à la question.
:::
'''
COURS[131]=r'''
::: objectifs
- Additionner, soustraire et multiplier des décimaux en comprenant les rangs.
- Utiliser les multiplications et divisions par 10, 100 ou 1 000.
- Choisir une stratégie de calcul mental.
- Résoudre un problème à plusieurs étapes et contrôler le résultat.
:::

::: prerequis
Connaître les tables, la valeur des chiffres et le sens des quatre opérations.
:::

## I. Choisir le sens de l’opération

Une addition réunit des quantités ; une soustraction cherche un reste, un écart ou un complément. Une multiplication calcule des groupes égaux ou une grandeur obtenue par un produit. Avant de calculer, reformuler ce qui est connu et ce qui est cherché.

::: methode Préparer un calcul
1. Choisir une unité commune pour les quantités qui s’ajoutent ou se comparent.
2. Choisir l’opération en expliquant son sens.
3. Donner un ordre de grandeur.
4. Calculer exactement puis contrôler.
:::

::: attention Les mots ne décident pas tout seuls
« J’ai 7,35 € de moins que 20 € » conduit à une soustraction. Mais « Il me manque 7,35 € pour atteindre 20 € » demande aussi une soustraction pour trouver la somme possédée. Comprendre la relation est plus sûr que repérer un mot isolé.
:::

## II. Additionner et soustraire des décimaux

::: propriete Aligner les rangs
On additionne ou soustrait des unités de même taille : unités avec unités, dixièmes avec dixièmes, centièmes avec centièmes. Pour poser l’opération, on aligne donc les virgules et on complète par des zéros si nécessaire.
:::

::: exemple Addition
$12{,}7+3{,}85=12{,}70+3{,}85=16{,}55$. Pour contrôler, $12{,}7$ est proche de 13 et $3{,}85$ proche de 4 : un total proche de 17 est cohérent.
:::

::: exemple Soustraction et vérification
$$20{,}00-7{,}35=12{,}65$$
$$12{,}65+7{,}35=20{,}00$$
L’addition vérifie le résultat de la soustraction. Dans une soustraction posée, échanger une unité contre dix dixièmes ne modifie pas la quantité totale.
:::

::: attention Garder la même unité
On n’additionne pas directement 2 kg et 75 g. On écrit par exemple $2{,}000+0{,}075=2{,}075$ kg, ou $2\,000+75=2\,075$ g.
:::

## III. Changer la valeur des chiffres

::: propriete Multiplier ou diviser par une puissance de dix
Multiplier par 10 rend la valeur de chaque chiffre dix fois plus grande : un centième devient un dixième, un dixième devient une unité. Diviser par 10 effectue le changement inverse. Pour 100 ou 1 000, on change de deux ou trois rangs.
:::

| Calcul | Résultat | Contrôle |
|---|---|---|
| $4{,}56\times100$ | $456$ | Résultat cent fois plus grand |
| $37{,}2\div100$ | $0{,}372$ | Résultat cent fois plus petit |
| $0{,}008\times1\,000$ | $8$ | Les millièmes deviennent unités |

::: propriete Multiplier par une fraction décimale de l’unité
Multiplier par $0{,}1$ revient à diviser par 10 ; par $0{,}01$, à diviser par 100 ; par $0{,}001$, à diviser par 1 000.
:::

::: exemple
$45\times0{,}1=4{,}5$ et $6{,}2\times0{,}01=0{,}062$. On explique ces résultats avec la valeur des rangs, sans oublier les zéros qui réservent une place.
:::

## IV. Multiplier deux nombres décimaux

::: exemple Une aire pour comprendre
Un rectangle de $2{,}3$ cm sur $1{,}4$ cm se décompose avec $2{,}3=2+0{,}3$ et $1{,}4=1+0{,}4$. Les quatre parties ont pour aires 2 ; $0{,}8$ ; $0{,}3$ et $0{,}12$ centimètre carré. Leur somme vaut $3{,}22\ \mathrm{cm}^2$.
:::

[IMAGE_1]

::: methode Calculer avec des entiers
On calcule d’abord $23\times14=322$. Comme $2{,}3=\frac{23}{10}$ et $1{,}4=\frac{14}{10}$, le produit vaut $\frac{322}{100}=3{,}22$. Le produit des deux dénominateurs explique les deux rangs décimaux.
:::

::: propriete Règle pratique
On multiplie les nombres comme s’il n’y avait pas de virgule, puis on place dans le résultat autant de chiffres après la virgule que les deux facteurs en comportent au total. On peut ensuite retirer les zéros finaux inutiles.
:::

::: exemple Contrôler la virgule
$19{,}8\times5{,}1$ est proche de $20\times5=100$. Le produit entier $198\times51=10\,098$ conduit à $100{,}98$, cohérent avec l’estimation. $10{,}098$ serait beaucoup trop petit.
:::

::: attention Multiplier ne rend pas toujours plus grand
Pour un nombre positif, multiplier par un nombre strictement compris entre 0 et 1 le diminue. $8\times0{,}5=4$ : prendre une moitié donne moins que la quantité entière. Multiplier par 1 conserve la valeur, et par 0 donne 0.
:::

## V. Choisir un calcul mental

::: methode Utiliser des nombres faciles
- Multiplier par 5 : multiplier par 10 puis diviser par 2.
- Multiplier par $0{,}5$ : prendre la moitié.
- Multiplier par 9 : multiplier par 10 puis retirer une fois le nombre.
- Multiplier par $1{,}1$ : ajouter au nombre son dixième.
:::

::: exemple
$12{,}8\times5=64$, car $12{,}8\times10=128$ et $128\div2=64$. Pour $12{,}8\times9$, on calcule $128-12{,}8=115{,}2$. Le choix de la méthode dépend des nombres et doit rester explicable.
:::

## VI. Organiser un problème en plusieurs étapes

::: exemple Une commande livrée
Quatre ateliers reçoivent chacun 3 carnets bleus et 2 verts. Chaque carnet coûte $2{,}50$ € et la livraison coûte 6 € pour toute la commande.

1. Un atelier utilise $3+2=5$ carnets.
2. Il faut $4\times5=20$ carnets.
3. Les carnets coûtent $20\times2{,}50=50$ €.
4. La commande livrée coûte $50+6=56$ €.

Les frais de livraison ne sont ajoutés qu’une fois. L’expression $4\times(3+2)\times2{,}50+6$ traduit l’histoire.
:::

::: conseil Rédiger et contrôler
Écrire une courte phrase pour chaque résultat, garder l’unité et répondre à la question finale. Vérifier le calcul par une opération inverse lorsque c’est possible, et vérifier que sa taille est plausible dans le contexte.
:::

::: retenir
Aligner les rangs pour additionner et soustraire. Justifier le placement de la virgule d’un produit. Utiliser les relations entre nombres pour calculer mentalement. Dans un problème, choisir l’opération d’après son sens puis contrôler le résultat.
:::
'''
COURS[133]=r'''
::: objectifs
- Distinguer partage et recherche d’un nombre de groupes.
- Effectuer et vérifier une division euclidienne.
- Calculer un quotient décimal dans des cas simples.
- Interpréter un reste et choisir entre résultat exact et approché.
:::

::: prerequis
Connaître les tables, les multiples et les écritures décimales.
:::

## I. Deux sens de la division

::: exemple Partager en parts égales
On distribue 24 cartes à 6 joueurs : $24\div6=4$. Le nombre de groupes est connu ; on cherche la taille d’une part. Chaque joueur reçoit 4 cartes.
:::

::: exemple Chercher le nombre de groupes
On range 24 cartes par paquets de 6 : $24\div6=4$. La taille d’un groupe est connue ; on cherche le nombre de groupes. On obtient 4 paquets.
:::

::: attention Nommer le résultat
La même opération peut donner des objets par personne ou un nombre de paquets. La phrase de réponse doit préciser ce qui a été calculé.
:::

## II. Comprendre quotient entier et reste

::: definition Division euclidienne
Diviser un entier naturel par un entier non nul consiste à trouver un quotient entier et un reste tels que :

$$\text{dividende}=\text{diviseur}\times\text{quotient}+\text{reste}$$

Le reste est positif ou nul et strictement inférieur au diviseur.
:::

::: exemple
$$157=12\times13+1$$

Dans la division de 157 par 12, le quotient vaut 13 et le reste 1. La vérification comporte deux points : $12\times13+1=157$ et $0\le1\lt12$.
:::

::: methode Poser une division par un entier à deux chiffres
1. Chercher combien de fois le diviseur entre dans la partie du dividende lue à gauche.
2. Écrire un chiffre du quotient et soustraire le produit correspondant.
3. Abaisser le chiffre suivant du dividende.
4. Continuer jusqu’à avoir utilisé tous les chiffres.
5. Contrôler l’égalité et la taille du reste.
:::

::: exemple Détailler $157\div12$
Dans 15, il y a une fois 12 ; on retire 12 et il reste 3 dizaines. En abaissant 7 unités, on obtient 37 unités. Dans 37, il y a 3 fois 12, soit 36 ; il reste 1. Le quotient comporte donc 1 dizaine et 3 unités : 13.
:::

::: attention Une égalité seule ne suffit pas
$53=8\times5+13$ est une égalité vraie, mais ce n’est pas une division euclidienne terminée : le reste 13 dépasse le diviseur 8. On peut former encore un groupe : $53=8\times6+5$.
:::

## III. Choisir la bonne interprétation du reste

::: exemple Des objets qu’on ne coupe pas
Pour 53 objets et des boîtes de 8, on obtient 6 boîtes pleines et 5 objets restants. Il faut donc 7 boîtes pour tout ranger, et non 6. La dernière boîte possède $8-5=3$ places libres.
:::

::: exemple Des parts qui peuvent être subdivisées
Pour partager 53 L en 8 parts égales, on peut poursuivre après les unités : chaque part vaut exactement $6{,}625$ L. Les objets indivisibles et une quantité liquide ne se traitent pas de la même façon.
:::

::: methode Répondre à la question posée
Si l’on demande les groupes complets, donner le quotient entier. Si tous les objets doivent être rangés, ajouter un groupe lorsque le reste n’est pas nul. Si la grandeur peut être subdivisée, poursuivre le partage en dixièmes, centièmes ou millièmes.
:::

## IV. Poursuivre une division décimale

::: exemple Partager $16{,}8$ € entre 4 amis
On peut raisonner en centimes : $1\,680\div4=420$, donc chacun paie $4{,}20$ €. Ou partager les unités puis les dixièmes : $16\div4=4$ unités et $8\div4=2$ dixièmes. Chaque part vaut $4{,}2$ €.
:::

::: propriete Vérification d’un quotient exact
Multiplier le quotient par le diviseur doit redonner le dividende. Ainsi $4{,}2\times4=16{,}8$.
:::

::: methode Faire apparaître des rangs supplémentaires
Après avoir utilisé tous les chiffres, on peut compléter l’écriture du dividende par des zéros après la virgule : $53=53{,}0$ ou $16{,}8=16{,}80$. Ces zéros ne changent pas sa valeur. On poursuit alors le partage : un reste de 1 unité devient 10 dixièmes, puis un reste de 1 dixième devient 10 centièmes.
:::

## V. Quotient exact et division qui ne se termine pas

::: definition Écriture fractionnaire d’un quotient
Le partage de $a$ unités en $b$ parts égales, avec $b\ne0$, donne le quotient exact $\frac ab$. Cette écriture reste exacte même si l’écriture décimale se prolonge indéfiniment.
:::

::: exemple
Pour $10\div3$, chaque part vaut exactement $\frac{10}{3}$ L. La division donne $3{,}333\ldots$ ; au centième, $3{,}33\lt\frac{10}{3}\lt3{,}34$. Son arrondi est $3{,}33$ L.
:::

::: attention Ne pas transformer une approximation en égalité
$3{,}33\times3=9{,}99$, différent de 10. On écrit $\frac{10}{3}\approx3{,}33$. Si l’on veut effectivement distribuer du liquide par quantités arrondies, il peut rester une petite quantité : c’est une nouvelle question concrète.
:::

## VI. Identifier un partage sans reste

::: definition Divisibilité
Un entier est divisible par un entier non nul lorsque le reste de leur division euclidienne est nul. On dit aussi que le premier est un multiple du second.
:::

| Diviseur | Critère |
|---|---|
| 2 | Chiffre des unités pair : 0, 2, 4, 6 ou 8 |
| 3 | Somme des chiffres divisible par 3 |
| 5 | Chiffre des unités 0 ou 5 |
| 9 | Somme des chiffres divisible par 9 |
| 10 | Chiffre des unités 0 |

::: exemple
126 est divisible par 2 car son dernier chiffre est 6. Il est divisible par 3 et par 9 car $1+2+6=9$. En revanche, il n’est pas divisible par 5, car son dernier chiffre n’est ni 0 ni 5.
:::

::: retenir
Donner un sens au quotient et au reste. Toujours vérifier la division euclidienne par l’égalité et la condition sur le reste. Une fraction peut donner une réponse exacte quand un décimal n’en donne qu’une approximation.
:::
'''
COURS[150]=r'''
::: objectifs
- Exécuter un programme de calcul en notant chaque résultat intermédiaire.
- Traduire une suite d’instructions par une expression.
- Retrouver un nombre initial en remontant les étapes.
- Comparer des programmes et expliquer une régularité.
:::

::: prerequis
Connaître les quatre opérations et lire une expression avec des parenthèses.
:::

## I. Comprendre la notion de programme

::: definition Programme de calcul
Un programme de calcul est une suite ordonnée d’instructions. On choisit un nombre de départ ; chaque instruction agit sur le résultat obtenu à l’étape précédente. Le dernier nombre calculé est le résultat final.
:::

::: exemple
Programme : choisir un nombre, ajouter 3, multiplier le résultat par 2, puis retirer 4. Avec le départ 5 :

$$5+3=8$$
$$8\times2=16$$
$$16-4=12$$

Les nombres successifs sont 5, 8, 16 et 12. Écrire $5=8=16=12$ serait faux : ce sont des étapes successives, pas des nombres égaux.
:::

::: methode Exécuter sans oublier d’étape
Lire toutes les consignes, entourer le nombre initial, puis noter un résultat par instruction. Garder les éventuelles unités dans un problème concret. Vérifier qu’aucune opération n’a été sautée ni appliquée deux fois.
:::

## II. Traduire avec des parenthèses

::: propriete Regrouper ce qui doit être calculé d’abord
Les parenthèses indiquent un groupe à calculer avant de l’utiliser dans la suite. « Ajouter 3 puis multiplier le résultat par 2 » s’écrit $(5+3)\times2$ pour un départ 5.
:::

::: exemple
Le programme précédent se traduit par :

$$(5+3)\times2-4=12$$

Sans les parenthèses, $5+3\times2-4=7$ ne traduit pas la même suite d’instructions.
:::

::: attention Portée d’une instruction
« Multiplier le résultat par 2 » concerne toute la somme déjà obtenue. Ce n’est pas seulement multiplier le dernier nombre ajouté. On peut relire l’expression de l’intérieur des parenthèses vers l’extérieur pour contrôler la traduction.
:::

## III. L’ordre des opérations change le résultat

::: exemple Comparer deux programmes
Programme A : ajouter 3, puis multiplier par 2. Programme B : multiplier par 2, puis ajouter 3. Avec le départ 5 :

$$A:(5+3)\times2=16$$
$$B:5\times2+3=13$$

Les résultats sont différents : dans A, les 3 unités ajoutées sont aussi doublées ; dans B, elles sont ajoutées après le doublement.
:::

::: remarque Justifier la différence
Il ne suffit pas de dire « les résultats sont différents ». On précise quelle quantité est multipliée, quelle quantité est ajoutée et à quel moment. On n’affirme pas non plus que changer l’ordre modifie toujours le résultat : certaines opérations peuvent donner le même résultat dans un autre ordre.
:::

## IV. Retrouver le nombre de départ

::: methode Remonter les instructions
1. Partir du résultat final.
2. Défaire la dernière opération, puis l’avant-dernière, jusqu’au début.
3. Remplacer une addition par une soustraction, et inversement.
4. Remplacer une multiplication par une division, et inversement, avec un nombre non nul.
5. Refaire le programme dans le sens initial pour vérifier.
:::

::: exemple
Programme : multiplier le nombre initial par 3, puis ajouter 7. Le résultat est 19.

On retire d’abord 7 : $19-7=12$. Puis on divise par 3 : $12\div3=4$. Le nombre initial est 4. Vérification : $4\times3+7=19$.
:::

::: exemple Trois opérations à remonter
Programme : ajouter 10, multiplier par 2, puis retirer 6. Le résultat vaut 20. On effectue successivement $20+6=26$, $26\div2=13$, puis $13-10=3$. Vérification : $(3+10)\times2-6=20$.
:::

::: attention Inverser l’ordre aussi
Pour remonter un programme, on inverse les opérations ET leur ordre. Retirer 10 avant de défaire les deux dernières consignes ne retrouve pas le départ du programme précédent. Un programme comportant une multiplication par 0 ne permet pas de retrouver un départ unique : tous les nombres sont alors transformés en 0 à cette étape.
:::

## V. Explorer un programme avec un tableau

::: exemple
Programme : ajouter 3 puis multiplier par 2.

| Départ | Après l’addition | Résultat |
|---|---|---|
| 0 | 3 | 6 |
| 1 | 4 | 8 |
| 2 | 5 | 10 |
| 10 | 13 | 26 |

Quand le départ augmente de 1, la somme augmente de 1, puis la multiplication par 2 transforme cette variation en une augmentation de 2.
:::

::: attention Une régularité à expliquer
Le résultat ne double pas quand le départ double : les départs 1 et 2 donnent 8 et 10, et $2\times8=16\ne10$. Observer une différence constante ne suffit pas à conclure à une proportionnalité.
:::

## VI. Construire un programme qui traduit une situation

::: exemple Prix d’une activité
Une activité coûte 3 € par séance et 5 € d’inscription, payés une fois. Le programme « multiplier le nombre de séances par 3, puis ajouter 5 » calcule le prix. Pour 8 séances, $8\times3+5=29$ €.

Si un élève paie 35 €, on retire l’inscription : $35-5=30$ €, puis on divise par le tarif : $30\div3=10$. Il suit 10 séances.
:::

::: methode Tester puis justifier
Pour vérifier un programme proposé, essayer un départ facile, puis un autre. Un contre-exemple suffit à montrer qu’une règle est fausse. Pour expliquer une règle valable pour tous les départs, analyser ce que chaque opération fait au nombre et aux quantités ajoutées.
:::

::: exemple Raccourcir une suite
« Multiplier par 2, ajouter 6, puis diviser par 2 » revient à ajouter 3 : la première multiplication est annulée par la division, tandis que les 6 unités ajoutées deviennent 3 unités. Cette explication dépasse la simple observation de quelques essais.
:::

::: retenir
Suivre l’ordre, noter les résultats intermédiaires et utiliser des parenthèses adaptées. Pour retrouver le départ, remonter les consignes avec leurs opérations inverses, puis vérifier. Un tableau aide à chercher ; une explication donne le sens de la règle.
:::
'''
COURS[151]=r'''
::: objectifs
- Représenter une quantité inconnue par un symbole ou une barre.
- Résoudre des problèmes de somme, d’écart et de parts égales.
- Repérer la structure d’un motif évolutif.
- Prévoir une étape lointaine et vérifier toutes les conditions.
:::

::: prerequis
Comprendre les quatre opérations et savoir exécuter un programme de calcul.
:::

## I. Décrire une quantité que l’on ne connaît pas encore

::: definition Quantité inconnue
Une quantité inconnue est un nombre à déterminer. On peut ignorer sa valeur tout en connaissant des relations : « trois fois autant », « 14 de plus », « ensemble, ils font 50 ». Un symbole ou une barre permet de représenter cette quantité.
:::

::: exemple Une égalité à trous
Trois boîtes identiques et 4 crayons isolés contiennent au total 19 crayons. On peut écrire $3\times\square+4=19$. Le symbole représente le nombre de crayons dans UNE boîte, identique pour les trois boîtes.
:::

::: methode Isoler puis partager
On retire les crayons isolés : $19-4=15$. Les trois boîtes contiennent 15 crayons ; une boîte contient $15\div3=5$ crayons. On vérifie : $3\times5+4=19$.
:::

::: attention Le même symbole garde sa valeur
Si deux boîtes sont annoncées identiques, on leur attribue le même nombre. On ne peut pas choisir un contenu différent pour chaque boîte afin d’obtenir le total.
:::

## II. Utiliser des schémas en barres

::: exemple Une relation multiplicative
Mia possède une collection. Léo possède trois fois autant d’objets que Mia. Ils en ont ensemble 48. Une barre représente la collection de Mia ; trois barres identiques représentent celle de Léo.
:::

[IMAGE_1]

::: methode Compter les parts du total
Le total contient $1+3=4$ parts égales. Une part vaut $48\div4=12$. Mia possède 12 objets et Léo $3\times12=36$ objets. Vérifier : $12+36=48$ et $36\div12=3$.
:::

::: attention Compter toutes les parts
Diviser 48 par 3 serait une erreur : les trois parts de Léo ne représentent pas le total, car il faut aussi compter la part de Mia. Dire « trois fois autant » indique le rapport, pas le nombre total de parts.
:::

## III. Résoudre un problème de somme et d’écart

::: exemple
Deux collections ont pour somme 50 et pour écart 14. La grande se représente par une barre de la même longueur que la petite, prolongée par une partie valant 14.
:::

::: methode Retirer l’écart pour obtenir deux parts égales
1. Retirer du total ce qui dépasse : $50-14=36$.
2. Partager le reste en deux : $36\div2=18$.
3. Reconstituer la grande quantité : $18+14=32$.
4. Vérifier : $18+32=50$ et $32-18=14$.
:::

::: remarque Vérifier deux conditions
Trouver deux nombres dont la somme vaut 50 ne suffit pas : leur différence doit aussi valoir 14. Les nombres 20 et 30 conviennent pour la somme, mais pas pour l’écart, qui vaut 10.
:::

## IV. Comprendre une égalité avec une balance

::: propriete Conserver l’équilibre
Les deux plateaux d’une balance en équilibre représentent des masses égales. Retirer une même masse des deux côtés ou partager les deux masses en un même nombre de parts conserve cette égalité.
:::

::: exemple
Deux boîtes identiques et 5 g équilibrent une masse de 19 g. Retirer 5 g de chaque côté laisse deux boîtes pour 14 g. Une boîte pèse $14\div2=7$ g. Vérification : $2\times7+5=19$.
:::

::: attention Retirer seulement d’un côté
Si l’on retire une masse sur un seul plateau, l’équilibre est perdu. Le dessin sert à comprendre les relations, pas à deviner une réponse d’après la taille apparente des objets.
:::

## V. Repérer la structure d’un motif évolutif

::: definition Motif évolutif
Un motif évolutif se transforme suivant une règle. On cherche ce qui reste fixe et ce qui s’ajoute à chaque étape. Le rang désigne le numéro de l’étape, pas nécessairement le nombre d’objets.
:::

[IMAGE_2]

::: exemple Des carrés accolés
Un carré demande 4 allumettes. Chaque nouveau carré partage un côté avec le précédent et ajoute seulement 3 allumettes. Pour 2 carrés : $4+3=7$. Pour 3 carrés : $4+2\times3=10$.
:::

::: methode Prévoir une étape lointaine
Pour 10 carrés, on compte le premier carré puis 9 ajouts : $4+9\times3=31$. On peut aussi repérer un côté initial puis trois allumettes par carré : $1+3\times10=31$. Cette seconde lecture explique la règle directement.
:::

::: exemple Chercher le rang
On dispose de 61 allumettes. Après avoir retiré l’allumette initiale, il reste $61-1=60$ allumettes. On peut faire $60\div3=20$ carrés. Contrôle : $1+3\times20=61$.
:::

::: attention Compter les changements de rang
Une frise contient 4 perles au rang 1 et gagne 3 perles à chaque passage. Au rang 10, il y a neuf passages depuis le rang 1 : $4+9\times3=31$. Ajouter dix fois compterait une étape de trop.
:::

## VI. Chercher, tester et expliquer

::: methode Une démarche de recherche
- Dire ce que représente chaque quantité.
- Choisir une barre, un dessin, un tableau ou une égalité à trous.
- Essayer un nombre simple si cela aide à comprendre.
- Utiliser les relations pour calculer.
- Tester la réponse dans TOUTES les informations de départ.
:::

::: exemple Une réponse à rejeter
Pour $3\times\square+8=20$, proposer 5 donne $3\times5+8=23$, qui n’est pas 20. Le nombre 4 donne $3\times4+8=20$ et convient. Un essai faux peut aider, à condition d’expliquer ce qu’il révèle.
:::

::: remarque Vers une règle générale
On peut décrire une règle avec des mots : « une allumette de départ, puis trois par carré ». Une écriture avec une lettre peut ensuite abréger cette phrase, mais la priorité est de comprendre ce que représentent les quantités et pourquoi la règle fonctionne.
:::

::: retenir
Représenter l’inconnu, exploiter les relations connues, compter les parts correctement et vérifier la réponse. Pour un motif, expliquer la partie fixe et les ajouts : cela permet de prévoir sans dessiner toutes les étapes.
:::
'''

FICHES[129]=r'''
::: objectifs
Lire les classes et les rangs, puis changer d’écriture sans changer de nombre.
:::
## I. Classes et rangs
| Classe | Groupe |
|---|---|
| Milliards | 7 |
| Millions | 342 |
| Milliers | 015 |
| Unités | 608 |
Dans $7\,342\,015\,608$ : chiffre des millions = 2 ; valeur = $2\,000\,000$ ; nombre de millions entiers = $7\,342$.

## II. Relier les unités
$$1=\frac{10}{10}=\frac{100}{100}=\frac{1\,000}{1\,000}$$
$$\frac1{10}=0{,}1,\quad\frac1{100}=0{,}01,\quad\frac1{1\,000}=0{,}001$$
Chaque rang vaut dix fois celui de droite.

## III. Changer d’écriture
::: methode
Lire le dernier rang pour choisir le dénominateur : $0{,}045=\frac{45}{1\,000}$. Séparer la partie entière pour un nombre mixte : $4{,}107=4+\frac{107}{1\,000}$. Pour reconstituer une fraction, convertir aussi les unités entières.
:::
::: attention
$2{,}5=2{,}50$, mais $2{,}05\ne2{,}5$. Un entier est aussi décimal. Une fraction n’est pas toujours décimale : $\frac13\approx0{,}33$, sans égalité exacte.
:::
::: retenir
Chiffre, valeur du chiffre et nombre de parts sont trois informations distinctes. Contrôler les rangs et les unités dans chaque réponse.
:::
'''
FICHES[130]=r'''
::: objectifs
Situer, comparer et approcher un nombre décimal.
:::
## I. Lire et comparer
::: methode
Pas d’une graduation = écart des valeurs connues divisé par le nombre d’intervalles. Compter les espaces, pas les traits. Pour comparer, lire la partie entière puis les rangs successifs : $0{,}8=0{,}80\gt0{,}75$.
:::
$a\le b$ autorise l’égalité ; $a\lt b$ l’exclut.

## II. Encadrer et intercaler
$$3{,}4\lt3{,}476\lt3{,}5$$
$$3{,}47\lt3{,}476\lt3{,}48$$
Entre $2{,}30$ et $2{,}31$, on peut intercaler $2{,}305$. Ajouter des rangs permet d’affiner une graduation.

## III. Arrondir
::: methode
Repérer le rang demandé et lire le chiffre suivant : de 0 à 4, choisir la borne inférieure ; de 5 à 9, la supérieure, avec les retenues. $7{,}364$ donne 7 à l’unité, $7{,}4$ au dixième et $7{,}36$ au centième.
:::
::: attention
Toujours repartir du nombre initial. $2{,}995$ s’arrondit à $3{,}00$ au centième. Un arrondi est une approximation : $\frac13\approx0{,}33$. Près d’un seuil, conserver la précision nécessaire.
:::
::: retenir
Encadrement : deux bornes. Arrondi : une valeur proche. Comparaison : une relation exacte entre nombres.
:::
'''
FICHES[131]=r'''
::: objectifs
Choisir l’opération, calculer avec les rangs et contrôler la réponse.
:::
## I. Addition et soustraction
Aligner les virgules et compléter les rangs : $12{,}70+3{,}85=16{,}55$ ; $20{,}00-7{,}35=12{,}65$. Vérification : $12{,}65+7{,}35=20$.

## II. Multiplication
::: methode
Calculer le produit comme avec des entiers, puis justifier la virgule : $23\times14=322$, donc $2{,}3\times1{,}4=3{,}22$. Contrôler par une estimation. Multiplier par 10, 100 ou 1 000 change la valeur de chaque chiffre d’un, deux ou trois rangs.
:::
| Multiplier par | Revient à |
|---|---|
| $0{,}1$ | Diviser par 10 |
| $0{,}01$ | Diviser par 100 |
| $0{,}5$ | Prendre la moitié |
| 5 | Multiplier par 10 puis diviser par 2 |

## III. Problème et contrôle
::: methode
Comprendre ce qui est cherché, choisir une unité commune, estimer, calculer, puis répondre avec l’unité. Les frais fixes ne sont ajoutés qu’une fois.
:::
::: attention
Multiplier un nombre strictement positif par un facteur strictement compris entre 0 et 1 le diminue. La virgule n’est pas un séparateur de deux entiers : les rangs donnent le sens du calcul.
:::
::: retenir
Une opération inverse ou un ordre de grandeur contrôle le calcul ; une phrase de réponse contrôle son sens.
:::
'''
FICHES[133]=r'''
::: objectifs
Donner un sens au quotient, au reste et aux approximations.
:::
## I. Division euclidienne
$$157=12\times13+1$$
Quotient entier 13, reste 1. Toujours vérifier l’égalité et $0\le\text{reste}\lt\text{diviseur}$.

::: methode
Chercher un multiple proche sans dépasser le dividende, soustraire, puis poursuivre la division. Si le reste dépasse le diviseur, un groupe supplémentaire peut encore être formé.
:::

## II. Interpréter la réponse
| Question pour 53 objets par boîtes de 8 | Réponse |
|---|---|
| Boîtes pleines | 6 |
| Objets restants | 5 |
| Boîtes nécessaires pour tout ranger | 7 |

## III. Quotient décimal ou fraction
Partager $16{,}8$ € entre 4 donne $4{,}2$ € : contrôle $4{,}2\times4=16{,}8$. Une quantité divisible peut être partagée en dixièmes, centièmes…
::: attention
La fraction $\frac{10}{3}$ garde le quotient exact. $3{,}33$ est seulement son arrondi au centième : $\frac{10}{3}\approx3{,}33$.
:::
::: retenir
Une divisibilité signifie un reste nul. L’unité et la question déterminent si l’on donne des groupes complets, un nombre suffisant de groupes, ou un quotient fractionnaire.
:::
'''
FICHES[150]=r'''
::: objectifs
Exécuter, traduire, remonter et vérifier un programme de calcul.
:::
## I. Suivre les instructions
Chaque instruction agit sur le résultat précédent. Exemple : ajouter 3, multiplier par 2, retirer 4. Avec le départ 5 : $5+3=8$, puis $8\times2=16$, puis $16-4=12$.

::: methode Traduire
Les parenthèses regroupent ce qui doit être calculé d’abord : $(5+3)\times2-4=12$. Le calcul $5+3\times2-4$ décrit autre chose.
:::

## II. Retrouver le départ
::: methode
Partir du résultat final, défaire la dernière opération puis remonter. Inverser addition et soustraction ; multiplication et division par un nombre non nul. Refaire ensuite le programme dans le bon sens.
:::
Multiplier par 3 puis ajouter 7 donne 19 : $19-7=12$, puis $12\div3=4$. Vérification : $4\times3+7=19$.

## III. Comparer et expliquer
Un tableau aide à chercher une régularité. Un contre-exemple réfute une règle ; une explication du rôle des opérations justifie une règle générale.
::: attention
Inverser l’ordre peut changer le résultat. Multiplier par 0 fait perdre le nombre initial : on ne peut pas diviser par 0 pour le retrouver.
:::
::: retenir
Noter les résultats intermédiaires, respecter l’ordre, traduire les parenthèses et contrôler le retour au départ.
:::
'''
FICHES[151]=r'''
::: objectifs
Représenter l’inconnu et utiliser les relations entre les quantités.
:::
## I. Parts égales
Trois boîtes et 4 crayons isolés font 19 : retirer 4, puis partager par 3. $19-4=15$, puis $15\div3=5$ crayons par boîte. Contrôle : $3\times5+4=19$.

## II. Somme et relation
::: methode
Si l’un possède trois fois autant que l’autre, le total fait quatre parts. Pour un total de 48 : $48\div4=12$, puis $3\times12=36$. Pour une somme de 50 et un écart de 14 : retirer l’écart, partager en deux, puis reconstituer : 18 et 32.
:::

## III. Motif évolutif
Carrés accolés : un premier carré demande 4 allumettes, puis chaque ajout en demande 3. Pour 10 carrés : $4+9\times3=31$, ou $1+3\times10=31$.
::: attention
Du rang 1 au rang 10, il y a neuf changements, pas dix. Une quantité initiale ne doit pas être ajoutée une seconde fois.
:::
::: methode Vérifier
Remplacer l’inconnu par le résultat et tester toutes les conditions : total, écart, rapport ou règle du motif. Le même symbole représente toujours la même quantité.
:::
::: retenir
Une barre, une balance ou un dessin sert à comprendre les relations ; l’explication de la structure permet de prévoir une étape lointaine.
:::
'''

for code,body in COURS.items():
 folder=next(ROOT.glob(str(code)+'_*'));meta=json.loads((folder/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
 # Les chaînes brutes protègent les antislashs ; normaliser le double échappement de cette rédaction.
 body=body.strip()
 path=folder/f'cours_{meta["cours"][0]["id"]}.txt'
 path.write_text('Titre: '+meta['titre']+'\n\n'+MARK+'\n'+body+'\n',encoding='utf-8')
 name=f'fiche_{meta["fiches"][0]["id"]}.txt' if meta['fiches'] else 'fiche_nouvelle.txt'
 (folder/name).write_text('Titre: '+meta['titre']+' — synthèse\n\n'+MARK+'\n'+FICHES[code].strip()+'\n',encoding='utf-8')
 print(code,'cours',len(body),'fiche',len(FICHES[code]),flush=True)
