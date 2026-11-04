"""Documents du lot mesures, aires, durées, données et probabilités CM2."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
DOCS={
11:('Longueurs, masses, contenances et périmètres',r'''::: objectifs
Choisir une unité adaptée, estimer puis comparer des mesures, expliquer une conversion et calculer la longueur d'un contour.
:::

## I. Quelle grandeur mesure-t-on ?

::: definition Trois grandeurs différentes
Une **longueur** mesure une distance ; une **masse** se mesure avec une balance ; une **contenance** indique ce qu'un récipient peut contenir. Avant de calculer, identifier la grandeur et son unité.
:::

| Objet ou situation | Unité adaptée |
|---|---|
| Longueur d'un crayon | centimètre (cm) |
| Distance entre deux villes | kilomètre (km) |
| Masse d'une pomme | gramme (g) |
| Masse d'un camion | tonne (t) |
| Contenance d'une gourde | millilitre (mL) ou litre (L) |

::: conseil Estimer avant de mesurer
Une règle d'écolier mesure environ 30 cm ; une bouteille peut contenir 1 L ; un paquet de farine pèse souvent 1 kg. Ces repères aident à repérer un résultat impossible.
:::

## II. Convertir en expliquant la relation

::: propriete Relations utiles
- $1\text{ km}=1\,000\text{ m}$ ; $1\text{ m}=100\text{ cm}$ ; $1\text{ m}=1\,000\text{ mm}$.
- $1\text{ t}=1\,000\text{ kg}$ ; $1\text{ kg}=1\,000\text{ g}$ ; $1\text{ g}=1\,000\text{ mg}$.
- $1\text{ L}=10\text{ dL}$ ; $1\text{ L}=100\text{ cL}$ ; $1\text{ L}=1\,000\text{ mL}$.
:::

::: methode Changer d'unité
Écrire la relation connue entre les deux unités. Compter les petites unités contenues dans la mesure, ou regrouper les petites unités pour obtenir des grandes unités. Le nombre change ; la grandeur reste la même.
:::

::: exemple De mètres en centimètres
Chaque mètre contient 100 cm. Ainsi :
$$3{,}5\times100=350$$
Donc 3,5 m = 350 cm. Dans l'autre sens, 250 cm = 2,5 m car 250 cm représentent deux mètres et un demi-mètre.
:::

::: exemple Comparer des masses
2 kg et 80 g = 2 000 g + 80 g = 2 080 g. Cette masse est inférieure à 2 100 g. On ne compare pas directement 2 et 2 100 : les unités sont différentes.
:::

## III. Mesurer et calculer

::: methode Lire une règle
Placer une extrémité sur la graduation zéro, puis lire l'autre. Si le segment ne commence pas à zéro, soustraire les deux lectures.
:::

[IMAGE_1]

::: exemple Une graduation décalée
Un segment commence à 15 mm et finit à 68 mm. Sa longueur est :
$$68-15=53$$
Il mesure 53 mm, soit 5,3 cm.
:::

::: methode Additionner ou soustraire des mesures
Choisir une unité commune, convertir, effectuer le calcul puis écrire l'unité du résultat.
:::

::: exemple Découper un ruban
Dans un ruban de 2 m, on coupe 75 cm. Comme 2 m = 200 cm :
$$200-75=125$$
Il reste 125 cm, soit 1 m et 25 cm.
:::

## IV. Le périmètre : faire le tour

::: definition
Le **périmètre** d'une figure est la longueur de son contour. Pour un polygone, additionner les longueurs de tous les côtés du bord extérieur, une seule fois chacun.
:::

[IMAGE_2]

::: exemple Un rectangle de 5 cm sur 3 cm
Son contour comporte deux côtés de 5 cm et deux côtés de 3 cm :
$$5+3+5+3=16$$
Son périmètre est 16 cm. Le produit $5\times3$ sert à une autre question : la surface occupée.
:::

::: attention Deux erreurs fréquentes
Ne pas mélanger les unités dans une addition. Ne pas compter un trait intérieur comme une partie du contour extérieur. Si une clôture possède une ouverture de 2 m, retirer ces 2 m de la longueur de clôture à acheter.
:::

::: retenir
Identifier la grandeur ; estimer ; choisir une unité commune ; expliquer la conversion ; calculer ; conclure avec une unité. Pour un périmètre, suivre tout le bord extérieur.
:::
''',r'''## I. Les relations à connaître

| Grandeur | Relations utiles |
|---|---|
| Longueurs | $1\text{ m}=100\text{ cm}$ ; $1\text{ cm}=10\text{ mm}$ ; $1\text{ km}=1\,000\text{ m}$ |
| Masses | $1\text{ kg}=1\,000\text{ g}$ ; $1\text{ g}=1\,000\text{ mg}$ ; $1\text{ t}=1\,000\text{ kg}$ |
| Contenances | $1\text{ L}=100\text{ cL}$ ; $1\text{ L}=1\,000\text{ mL}$ ; $1\text{ cL}=10\text{ mL}$ |

## II. Une méthode en quatre actions

::: methode
Choisir une unité adaptée, écrire la relation de conversion, calculer dans une unité commune, vérifier l'ordre de grandeur.
:::

::: exemple
2 m et 35 cm = 235 cm. Une masse de 1,5 kg vaut 1 500 g, car chaque kilogramme contient 1 000 g.
:::

## III. Le contour

::: retenir
Le périmètre est une longueur : additionner les côtés du bord extérieur. Pour un rectangle de 5 cm sur 3 cm : $5+3+5+3=16$ cm.
:::

::: attention
Sur une règle, soustraire les lectures si le segment ne commence pas à zéro. Une mesure sans unité est incomplète. Un périmètre s'exprime en cm ou m, une aire en cm² ou m².
:::
'''),
12:('Comparer et mesurer des aires',r'''::: objectifs
Comparer des surfaces, compter des unités d'aire, calculer l'aire d'un rectangle ou d'un carré et convertir entre cm², dm² et m².
:::

## I. L'aire est une mesure de surface

::: definition
L'**aire** indique la surface occupée par une figure. Pour comparer deux surfaces, on peut les superposer, les découper puis les réassembler, ou les recouvrir avec la même unité sans trou ni chevauchement.
:::

::: exemple Compter sur un quadrillage
Une surface couvre 8 carreaux entiers et 4 demi-carreaux. Deux demi-carreaux forment un carreau entier : son aire vaut $8+2=10$ unités d'aire.
:::

## II. Du centimètre carré au mètre carré

::: definition
Un **centimètre carré**, noté cm², est l'aire d'un carré de côté 1 cm. Un dm² correspond à un carré de côté 1 dm, et un m² à un carré de côté 1 m.
:::

[IMAGE_1]

::: propriete Cent petits carrés
Dans un carré de côté 1 dm, soit 10 cm, on place dix rangées de dix carrés de 1 cm² :
$$10\times10=100$$
Donc 1 dm² = 100 cm². De même, 1 m² = 100 dm² = 10 000 cm².
:::

::: methode Convertir une aire
Utiliser la relation entre les unités de surface, puis multiplier ou diviser par le nombre de petites unités contenues dans une grande unité.
:::

::: exemple
2,5 dm² = 250 cm² car $2{,}5\times100=250$. Inversement, 350 cm² = 3,5 dm² car $350\div100=3{,}5$.
:::

::: attention
1 dm = 10 cm, mais 1 dm² = 100 cm². La largeur **et** la longueur sont chacune multipliées par dix.
:::

## III. L'aire du rectangle et du carré

[IMAGE_2]

::: methode Compter des rangées
Un rectangle de 4 cm sur 3 cm contient 3 rangées de 4 carrés de 1 cm². Son aire vaut $4\times3=12$ cm². Les deux dimensions doivent être exprimées dans la même unité.
:::

::: propriete
L'aire d'un rectangle se calcule en multipliant sa longueur par sa largeur. Pour un carré, les deux dimensions sont égales : un carré de côté 5 cm a une aire de $5\times5=25$ cm².
:::

::: exemple Deux unités différentes
Un rectangle mesure 2 m sur 50 cm. Comme 50 cm = 0,5 m, son aire est $2\times0{,}5=1$ m². On peut aussi calculer $200\times50=10\,000$ cm² : c'est la même surface.
:::

## IV. Décomposer une surface

::: methode Additionner ou retirer des rectangles
Partager la surface en rectangles qui ne se recouvrent pas, puis additionner leurs aires. Autre possibilité : calculer l'aire d'un grand rectangle puis retirer la partie absente.
:::

::: exemple Une surface avec un coin retiré
Dans un rectangle de 8 m sur 6 m, un coin rectangulaire de 3 m sur 2 m est retiré :
$$
\begin{aligned}
8\times6&=48\\
3\times2&=6\\
48-6&=42
\end{aligned}
$$
La surface restante mesure 42 m².
:::

## V. Aire et périmètre répondent à deux questions

[IMAGE_3]

::: attention
Un rectangle de 8 cm sur 1 cm et un rectangle de 4 cm sur 2 cm ont la même aire, 8 cm². Leurs périmètres sont pourtant 18 cm et 12 cm. Une même aire n'impose donc pas un même contour.
:::

::: retenir
Compter avec une même unité ; convertir les deux dimensions avant de multiplier ; distinguer la surface et son contour ; écrire une unité carrée pour une aire.
:::
''',r'''## I. Surface et unité

::: definition
L'aire mesure la surface occupée. Un cm² est l'aire d'un carré de côté 1 cm. Deux demi-carreaux représentent un carreau entier.
:::

## II. Les relations essentielles

$$1\text{ dm}^2=100\text{ cm}^2$$
$$1\text{ m}^2=100\text{ dm}^2=10\,000\text{ cm}^2$$

::: methode
Rectangle : multiplier longueur et largeur exprimées dans la même unité. Carré : multiplier le côté par lui-même. Surface composée : additionner des parties sans recouvrement, ou retirer la partie absente.
:::

::: exemple
Un rectangle de 6 cm sur 4 cm mesure $6\times4=24$ cm².
:::

::: attention
Une conversion entre deux unités d'aire voisines utilise un facteur 100. Le périmètre mesure le contour, en cm ou m ; l'aire mesure la surface, en cm² ou m².
:::
'''),
18:('Lire l’heure et calculer des durées',r'''::: objectifs
Lire une horloge avec secondes, convertir des durées, trouver une durée écoulée, un horaire d'arrivée ou un horaire de départ.
:::

## I. Distinguer un instant et une durée

::: definition
Un **horaire** indique un instant, par exemple 14 h 30 min. Une **durée** mesure le temps entre deux instants, par exemple 25 min. Une activité qui commence à 14 h 30 et dure 25 min finit à 14 h 55.
:::

::: propriete Les unités de temps
1 min = 60 s ; 1 h = 60 min = 3 600 s ; 1 jour = 24 h. Les regroupements se font par soixante entre secondes et minutes, puis entre minutes et heures.
:::

## II. Lire une horloge à aiguilles

[IMAGE_1]

::: methode
Lire d'abord la petite aiguille des heures. La grande aiguille indique les minutes : une petite graduation vaut 1 min et l'écart entre deux nombres vaut 5 min. La trotteuse indique les secondes : un tour vaut 60 s.
:::

::: exemple
À 10 h 10 min 30 s, la trotteuse est sur le 6 ; la grande aiguille a un peu dépassé le 2 ; la petite aiguille a un peu dépassé le 10. Les aiguilles se déplacent progressivement.
:::

::: attention Matin ou après-midi ?
Le cadran recommence après douze heures. La même position peut représenter 4 h du matin ou 16 h l'après-midi : le contexte permet de choisir.
:::

## III. Convertir et comparer

::: exemple De minutes en heures et minutes
Pour 135 min, on regroupe deux paquets de 60 min :
$$135=2\times60+15$$
Donc 135 min = 2 h 15 min. De même, 125 s = 2 min 5 s.
:::

::: methode Comparer deux durées
Les exprimer dans la même unité, puis comparer les nombres obtenus. Par exemple, 1 h 20 min = 80 min : c'est plus long que 75 min.
:::

::: attention
1,5 h signifie une heure et une demi-heure : 1 h 30 min. Ce n'est pas 1 h 50 min.
:::

## IV. Calculer une durée entre deux instants

[IMAGE_2]

::: methode Avancer par étapes
Pour aller de 13 h 45 à 15 h 20, avancer jusqu'à 14 h, puis jusqu'à 15 h, puis jusqu'à 15 h 20. Additionner les durées de ces trois étapes.
:::

::: exemple
De 13 h 45 à 14 h : 15 min. De 14 h à 15 h : 1 h. De 15 h à 15 h 20 : 20 min. La durée totale est 1 h 35 min.
:::

::: exemple Passer minuit
De 23 h 50 à 0 h 15 le lendemain : 10 min pour atteindre minuit, puis 15 min. La durée est $10+15=25$ min.
:::

## V. Trouver un horaire

::: methode
Pour trouver l'arrivée, ajouter la durée au départ. Pour retrouver le départ, reculer depuis l'arrivée de la durée prévue. Regrouper 60 s en 1 min et 60 min en 1 h dès que nécessaire.
:::

::: exemple Addition avec secondes
Un exercice commence à 9 h 58 min 45 s et dure 2 min 30 s. Après 15 s, il est 9 h 59 ; il reste 2 min 15 s. Il finit à 10 h 1 min 15 s.
:::

::: retenir
Identifier si l'on cherche un instant ou une durée. Employer les relations de base soixante, vérifier le passage à l'heure suivante ou au jour suivant, puis donner un résultat avec ses unités.
:::
''',r'''## I. Les repères

$$1\text{ min}=60\text{ s}$$
$$1\text{ h}=60\text{ min}=3\,600\text{ s}$$
$$1\text{ jour}=24\text{ h}$$

::: methode Lire un cadran
Petite aiguille : heure. Grande aiguille : minutes, cinq minutes entre deux nombres. Trotteuse : secondes. Le contexte distingue matin et après-midi.
:::

## II. Trois recherches

| Ce qu'on cherche | Comment faire |
|---|---|
| Durée écoulée | Avancer du départ à l'arrivée et additionner les étapes |
| Arrivée | Départ + durée |
| Départ | Reculer depuis l'arrivée |

::: exemple
De 13 h 45 à 15 h 20 : 15 min + 1 h + 20 min = 1 h 35 min.
:::

::: attention
135 min = 2 h 15 min. 1,5 h = 1 h 30 min. Après 23 h 59, on passe au jour suivant : une soustraction directe des horaires ne suffit pas.
:::
'''),
19:('Organiser, représenter et lire des données',r'''::: objectifs
Organiser une enquête, lire un tableau ou un graphique, choisir une échelle adaptée et résoudre un problème en justifiant les informations prélevées.
:::

## I. Recueillir et organiser

::: definition
Une **donnée** est une information recueillie. L'**effectif** d'une catégorie est le nombre d'éléments qui lui appartiennent. Une enquête précise qui est interrogé, quelle question est posée et quelles réponses sont possibles.
:::

::: methode Une enquête claire
Poser la même question à chaque personne, ne compter chaque réponse qu'une fois, regrouper les réponses par catégorie puis vérifier que leur somme correspond au nombre de personnes interrogées.
:::

| Fruit préféré | Effectif |
|---|---:|
| Pomme | 6 |
| Poire | 4 |
| Banane | 8 |
| Total | 18 |

::: exemple
La banane est la réponse la plus fréquente. Elle n'a pas été choisie par la majorité des 18 personnes : une majorité demanderait plus de 9 réponses. Être la catégorie la plus fréquente ne signifie pas forcément dépasser la moitié du total.
:::

## II. Lire un tableau à double entrée

::: methode Croiser une ligne et une colonne
Lire les deux en-têtes, puis chercher la cellule à leur intersection. Vérifier si l'on demande une seule case, une somme de ligne ou une somme de colonne.
:::

| Classe | À pied | À vélo |
|---|---:|---:|
| CM1 | 7 | 3 |
| CM2 | 5 | 5 |

::: exemple
Il y a 5 élèves de CM2 à vélo. Le total à vélo est $3+5=8$ élèves. Ces deux questions ne demandent pas la même information.
:::

## III. Un diagramme en barres

[IMAGE_1]

::: methode Lire puis représenter
Lire le titre, les catégories, l'unité et la valeur d'une graduation. La hauteur de chaque barre représente un effectif. Pour construire un diagramme, conserver une même échelle, une même largeur de barre et des catégories identifiables.
:::

::: exemple
Le diagramme représente 4 prêts le lundi, 8 le mardi et 6 le mercredi. Le total est $4+8+6=18$ prêts. Le mardi compte 4 prêts de plus que le lundi.
:::

## IV. Une évolution au cours du temps

[IMAGE_2]

::: methode Lire une courbe
Repérer la date sur l'axe horizontal, rejoindre le point de la courbe puis lire la mesure sur l'axe vertical. Des points plus hauts représentent ici une plante plus grande ; l'écart entre deux mesures donne la croissance entre ces deux dates.
:::

::: exemple
Une plante mesure 6 cm en semaine 1, 10 cm en semaine 2, 12 cm en semaine 3 et 18 cm en semaine 4. Elle a grandi de $18-6=12$ cm entre les semaines 1 et 4. Le graphique ne renseigne pas précisément sa taille chaque jour.
:::

## V. Lire un diagramme circulaire

[IMAGE_3]

::: definition
Le disque entier représente tout l'effectif. Une moitié de disque représente la moitié du total ; un quart représente un quart du total. La légende indique à quelle catégorie correspond chaque secteur.
:::

::: exemple
Sur 24 réponses, une moitié correspond à $24\div2=12$ réponses. Chaque quart correspond à $24\div4=6$ réponses. On peut lire ces parts sans mesurer les angles.
:::

## VI. Contrôler une représentation

::: attention
Vérifier l'origine et la graduation des axes avant de comparer. Un dessin plus haut n'est pas une preuve sans échelle. Ne pas inventer une donnée absente. Les nombres de ce cours sont des données fictives d'entraînement.
:::

::: retenir
Lire les en-têtes, les unités et la légende ; prélever la bonne information ; effectuer le calcul demandé ; donner une réponse reliée à la situation. Choisir un tableau, des barres ou des points selon les données à présenter.
:::
''',r'''## I. Organiser

::: methode
Poser une question précise, recueillir les réponses, compter les effectifs et vérifier le total. Dans un tableau à double entrée, croiser la bonne ligne avec la bonne colonne.
:::

## II. Lire un graphique

| Représentation | Ce qu'il faut regarder |
|---|---|
| Barres | Catégories, hauteur, unité et graduation |
| Courbe ou points | Dates et mesures sur les deux axes |
| Disque | Part du total et légende |

::: retenir
Une moitié représente le total divisé par 2 ; un quart, le total divisé par 4. Une différence se calcule en soustrayant deux mesures ; un total, en additionnant les effectifs concernés.
:::

::: attention
La catégorie la plus fréquente ne représente pas toujours une majorité. Ne pas confondre l'effectif d'une case avec un total, ni supposer une valeur non fournie par le document.
:::
'''),
20:('Comprendre et comparer des chances',r'''::: objectifs
Décrire une expérience aléatoire, recenser ses issues, exprimer des chances dans une situation équilibrée et étudier deux étapes sans oublier l'ordre des résultats.
:::

## I. Possible, impossible ou certain ?

::: definition
Une **expérience aléatoire** est une expérience dont on ne peut pas prévoir avec certitude le résultat avant de la réaliser. Une **issue** est un résultat possible. Un **évènement** regroupe les issues qui vérifient une condition.
:::

::: exemple Un dé classique
Les issues sont 1, 2, 3, 4, 5 et 6. Obtenir 8 est impossible. Obtenir un nombre inférieur à 7 est certain. Obtenir un nombre pair est possible, mais pas certain : les issues favorables sont 2, 4 et 6.
:::

## II. Compter des chances

::: definition Équiprobabilité
Les issues sont **équiprobables** lorsqu'elles ont toutes la même chance de se produire. Un dé équilibré et des jetons identiques tirés au hasard sans regarder peuvent fournir de telles situations. Il faut préciser les conditions de l'expérience.
:::

::: methode « a chances sur b »
Lister toutes les issues également possibles, puis celles qui réalisent l'évènement. Le premier nombre compte les issues favorables ; le second compte toutes les issues.
:::

::: exemple
Un sac contient 3 jetons verts et 5 jetons orange, identiques au toucher. Chaque jeton a la même chance d'être tiré. Il y a $3+5=8$ jetons : obtenir vert a **3 chances sur 8**, obtenir orange a **5 chances sur 8**.
:::

::: attention
Deux couleurs ne signifient pas une chance sur deux pour chaque couleur. Dans ce sac, orange est plus probable que vert, car les jetons orange sont plus nombreux.
:::

## III. Comparer des probabilités

::: methode Comparer avec une chance sur deux
Comparer les issues favorables à la moitié de toutes les issues. Sur 8 issues : 4 chances sur 8 correspondent à une chance sur deux ; 3 chances sur 8 sont moins probables ; 5 chances sur 8 sont plus probables.
:::

[IMAGE_1]

::: exemple Une roue équilibrée
Cette roue comporte quatre secteurs superposables numérotés de 1 à 4. Chaque numéro a 1 chance sur 4. Obtenir un numéro pair a 2 chances sur 4, soit une chance sur deux.
:::

## IV. Répéter ne change pas la chance suivante

::: propriete Indépendance
Quand on répète la même expérience dans les mêmes conditions, les résultats précédents ne changent pas les chances du résultat suivant. Après trois « pile », une pièce équilibrée conserve une chance sur deux de donner « face » au lancer suivant.
:::

::: attention
La pièce ne doit pas « rattraper » les résultats précédents. Une chance sur deux n'impose pas une alternance pile, face, pile, face.
:::

## V. Deux étapes : ne rien oublier

[IMAGE_2]

::: methode Recenser avec un arbre ou un tableau
Pour deux lancers successifs d'une pièce équilibrée, examiner chaque premier résultat, puis les deux résultats possibles au second lancer. Conserver l'ordre : pile puis face n'est pas la même issue que face puis pile.
:::

::: exemple
Les quatre issues sont (pile ; pile), (pile ; face), (face ; pile) et (face ; face). Elles sont équiprobables : chacune a 1 chance sur 4. Obtenir exactement une fois face correspond à deux issues, donc à 2 chances sur 4.
:::

::: retenir
Préciser l'expérience et ses conditions ; lister les issues ; compter les issues favorables et toutes les issues ; comparer les chances. Pour deux étapes, noter les couples dans l'ordre et utiliser un arbre ou un tableau.
:::
''',r'''## I. Les mots

::: definition
Une issue est un résultat possible ; un évènement est une condition sur le résultat. Impossible : aucune issue favorable. Certain : toutes les issues sont favorables. Équiprobables : les issues ont la même chance.
:::

## II. Compter et comparer

::: methode
Si les issues sont équiprobables, compter les issues favorables puis toutes les issues. Exemple : 3 jetons verts sur 8 jetons identiques donnent 3 chances sur 8 d'obtenir vert.
:::

::: retenir
Comparer le nombre favorable à la moitié du nombre total pour décider si l'évènement a moins, autant ou plus d'une chance sur deux de se produire.
:::

## III. Deux étapes

::: methode
Faire un arbre ou un tableau pour lister les couples. Pour deux lancers d'une pièce : (P ; P), (P ; F), (F ; P), (F ; F), soit quatre issues équiprobables.
:::

::: attention
Deux couleurs n'impliquent pas une chance sur deux chacune. L'ordre compte dans un couple. Une pièce équilibrée garde une chance sur deux de donner face à chaque nouveau lancer, quels que soient les résultats précédents.
:::
''')}
if __name__=='__main__':
 for code,(title,course,sheet) in DOCS.items():
  d=next(ROOT.glob(f'{code:02}_*'))
  for filename,body in [('cours_nouveau.txt',course),('fiche_nouvelle.txt',sheet)]:
   (d/filename).write_text('Titre: '+title+'\n\n<!-- optitab:1 -->\n'+body.strip()+'\n',encoding='utf-8')
  print(code,'documents rédigés')
