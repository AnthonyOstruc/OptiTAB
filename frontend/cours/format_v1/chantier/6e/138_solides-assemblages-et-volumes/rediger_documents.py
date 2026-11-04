# -*- coding: utf-8 -*-
from pathlib import Path
import json
R=Path(__file__).resolve().parent.parent
DOCS={}
DOCS[138]=(r'''::: objectifs
- Reconnaître les solides usuels.
- Passer d’un assemblage de cubes à un plan ou à une vue.
- Dénombrer les cubes, comparer et mesurer des volumes en cm³.
:::

::: prerequis
Compter des groupes identiques ; lire un tableau ; reconnaître cubes et pavés droits.
:::

## I. Décrire un solide
::: definition Du plan à l’espace
Un solide occupe une partie de l’espace. Une face plane est une surface qui le limite ; une arête est un segment où se rencontrent deux faces ; un sommet est une extrémité d’arête.
:::
Le cube possède six faces carrées identiques. Le pavé droit a six faces rectangulaires. Un prisme droit possède deux bases polygonales identiques et des faces latérales rectangulaires. Une pyramide possède une base et des triangles qui rejoignent un même sommet. Cylindre, cône et boule présentent des surfaces courbes.

[IMAGE_1]

::: attention Dessin et objet
Une représentation en perspective peut cacher des arêtes ou des cubes. Des segments parallèles sur le solide peuvent sembler obliques sur le dessin. Les arêtes cachées sont souvent en pointillés.
:::

## II. Comprendre un assemblage de cubes
### 1. Compter par rangées et par couches
::: methode Un dénombrement organisé
Identifier une couche. Compter ses rangées et le nombre de cubes de chaque rangée. Si toutes les couches sont identiques, multiplier leur contenu par le nombre de couches ; sinon, additionner leurs contenus.
:::
::: exemple Un bloc plein
Une couche comporte quatre rangées de trois cubes ; deux couches identiques sont empilées.
$$
\begin{aligned}
\text{Cubes d’une couche}&=4\times3=12\\
\text{Cubes du bloc}&=2\times12=24
\end{aligned}
$$
:::
### 2. Lire les hauteurs et les vues
Un plan de hauteurs représente chaque pile par une case contenant son nombre de cubes. On suppose les piles sans vide. La somme des hauteurs donne alors le nombre total de cubes.

| Rangée | Gauche | Droite |
|---|---|---|
| Arrière | 1 | 2 |
| Avant | 3 | 1 |

::: exemple Relier le plan et la vue
Le total vaut $1+2+3+1=7$ cubes. En regardant depuis l’avant, la hauteur visible à gauche est 3 et celle de droite est 2 : on garde la plus haute pile de chaque alignement.
:::

[IMAGE_2]

::: attention Une vue ne dit pas tout
De dessus, on repère les emplacements occupés, mais pas leurs hauteurs. De face, une pile haute peut en cacher une autre. Plusieurs assemblages peuvent avoir la même vue.
:::

## III. Mesurer et comparer des volumes
::: definition Le centimètre cube
Le volume mesure l’espace occupé par un solide. Un centimètre cube, noté cm³, est le volume d’un cube de 1 cm d’arête.
:::
::: propriete Dénombrer les unités de volume
Un assemblage de cubes de 1 cm d’arête, sans recouvrement, a un volume en cm³ égal à son nombre de cubes. Les cubes cachés sont compris dans ce nombre.
:::
::: exemple Ajouter ou retirer
Un assemblage de 24 cubes unités occupe 24 cm³. Si on enlève trois cubes, il reste $24-3=21$ cm³. Réorganiser ces 21 cubes sans en ajouter ni en retirer conserve ce volume.
:::
::: methode Comparer deux volumes
Utiliser la même unité de cube. Compter les cubes de chaque solide, puis comparer les nombres obtenus. La hauteur seule ne suffit pas.
:::
::: attention Longueur, aire et volume
Une arête se mesure en cm ; une face en cm² ; un solide en cm³. Une arête de 2 cm n’indique pas un volume de 2 cm³ : deux couches de deux rangées de deux cubes unités contiennent huit cubes.
:::
::: retenir
Compter tous les cubes, y compris les cachés ; exploiter les couches et les plans de hauteurs ; associer 1 cm³ à chaque cube unité. Une même quantité de cubes peut former plusieurs solides.
:::
''',r'''## I. Solides et représentations
Le cube a 6 faces carrées. Le pavé droit a 6 faces rectangulaires. Les pointillés représentent des arêtes cachées.

::: methode Compter un assemblage
- Par couches identiques : contenu d’une couche × nombre de couches.
- Par piles sans vide : somme des hauteurs.
- Vue de face : plus grande hauteur de chaque alignement.
:::

## II. Volume
::: definition
1 cm³ est le volume d’un cube de 1 cm d’arête. Avec des cubes unités sans recouvrement, le volume en cm³ est le nombre total de cubes.
:::

::: attention
Compter les cubes cachés. Une vue du dessus ne donne pas toutes les hauteurs. Ne pas confondre cm, cm² et cm³.
:::
::: retenir
Réorganiser les mêmes cubes conserve leur volume. Pour comparer, utiliser la même unité.
:::
''',('cube','vues_corrige'))
DOCS[139]=(r'''::: objectifs
- Distinguer horaire et durée ; lire une horloge.
- Convertir jours, heures, minutes et secondes.
- Calculer un début, une fin ou un temps écoulé, y compris avec des heures décimales.
:::

## I. Se repérer dans le temps
::: definition Instant et intervalle
Un horaire désigne un instant : « départ à 8 h 20 ». Une durée mesure le temps entre deux instants : « trajet de 45 min ».
:::
### 1. Lire une horloge
La petite aiguille indique les heures et avance progressivement entre deux nombres. La grande indique les minutes ; chaque intervalle entre deux nombres vaut 5 min. La trotteuse, si elle existe, indique les secondes.

[IMAGE_1]

::: exemple Après midi
À 15 h 25, la grande aiguille pointe le 5. La petite est entre 3 et 4. L’affichage sur 24 heures distingue 3 h 25 et 15 h 25.
:::
### 2. Connaître les unités
::: propriete Relations à mémoriser
$$
\begin{aligned}
1\ \text{jour}&=24\ \text{h}\\
1\ \text{h}&=60\ \text{min}\\
1\ \text{min}&=60\ \text{s}\\
1\ \text{h}&=3600\ \text{s}
\end{aligned}
$$
Une demi-heure vaut 30 min ; un quart d’heure 15 min ; trois quarts d’heure 45 min. Une année compte 365 jours, ou 366 si elle est bissextile. Un siècle compte 100 ans et un millénaire 1 000 ans.
:::

## II. Calculer sur les horaires et durées
::: methode Trouver une durée
Avancer de l’horaire de début à celui de fin en passant par les heures rondes. Additionner les intervalles. On peut aussi convertir les deux horaires en minutes depuis une même origine.
:::
::: exemple De 14 h 15 à 15 h 05
De 14 h 15 à 15 h, il s’écoule $60-15=45$ min ; puis encore 5 min. La durée totale est $45+5=50$ min.
:::
::: methode Trouver la fin ou le début
Pour trouver la fin, ajouter la durée au départ. Pour trouver le début, retirer la durée de l’arrivée. Contrôler le résultat dans le sens inverse.
:::
::: exemple Une fin après changement d’heure
10 h 45 + 35 min : avancer de 15 min jusqu’à 11 h, puis des $35-15=20$ min restantes. La fin est à 11 h 20.
:::
::: attention Passage de minuit
L’horaire repart à 0 h après 24 h. Pour une durée, compter le temps avant minuit puis celui du lendemain.
:::

[IMAGE_2]

De 23 h 35 à 0 h 20 le lendemain, la durée est $25+20=45$ min.

## III. Convertir des durées
::: methode Unité plus petite ou plus grande
Pour passer des heures aux minutes, multiplier par 60. Pour passer des minutes aux heures décimales, diviser par 60. Pour écrire des heures et minutes, chercher des groupes complets de 60 minutes et le reste.
:::
::: exemple Deux écritures d’une même durée
$$
\begin{aligned}
1\ \text{h}\ 30\ \text{min}&=90\ \text{min}\\
90\div60&=1{,}5
\end{aligned}
$$
Ainsi 1 h 30 min = 1,5 h. Inversement, $0{,}75\times60=45$, donc 2,75 h = 2 h 45 min.
:::
::: attention La base 60
1,30 h ne signifie pas 1 h 30 min : $0{,}30\times60=18$ min. Les centièmes d’heure ne sont pas des minutes.
:::
::: methode Résoudre un problème de planning
Mettre les durées dans une unité commune ; inclure pauses, marges et retards ; effectuer les calculs ; comparer à l’heure limite ; écrire une conclusion avec son unité.
:::
::: retenir
Additionner une durée à un horaire donne un horaire. Comparer deux horaires donne une durée. Minutes et secondes se regroupent par 60.
:::
''',r'''## I. Les repères
Un horaire indique **quand** ; une durée indique **combien de temps**.

| Relation | À retenir |
|---|---|
| Jour → heures | × 24 |
| Heure → minutes | × 60 |
| Minute → secondes | × 60 |
| Demi-heure | 30 min |
| Quart d’heure | 15 min |

## II. Les méthodes
::: methode
- Fin = départ auquel on ajoute la durée.
- Début = arrivée dont on retire la durée.
- Temps écoulé : passer par les heures rondes ; à minuit, poursuivre le lendemain.
- Minutes → heures décimales : diviser par 60.
:::

::: exemple
1 h 30 min = 90 min = 1,5 h.
:::
::: attention
1,30 h = 1 h 18 min. Inclure les pauses et les marges dans un planning.
:::
''',('horloge_1525','minuit_corrige'))
DOCS[146]=(r'''::: objectifs
- Reconnaître les solides usuels et décrire leurs faces.
- Relier un solide à un patron ; construire un patron de cube ou de pavé droit.
- Contrôler les raccords et le pliage, sans superposition.
:::

::: prerequis
Utiliser règle et équerre ; construire carrés et rectangles. Ce chapitre réactive les patrons étudiés au cours moyen et prépare la vision dans l’espace de sixième.
:::

## I. Reconnaître et décrire les solides
::: definition Face, arête et sommet
Une face plane est une surface polygonale qui limite le solide. Une arête est un segment commun à deux faces ; un sommet est une extrémité d’arête. Les solides peuvent aussi avoir des surfaces courbes.
:::

[IMAGE_1]

### 1. Les polyèdres usuels
Le cube possède 6 faces carrées identiques, 12 arêtes et 8 sommets. Le pavé droit possède 6 faces rectangulaires, associées par paires de faces opposées identiques. Un cube est un pavé droit particulier.

Un prisme droit possède deux bases polygonales identiques et parallèles ; ses faces latérales sont des rectangles. Une pyramide possède une base polygonale et des triangles qui rejoignent un sommet principal.
::: exemple Compter des faces
Un prisme droit à base triangulaire possède deux bases et trois faces latérales : $2+3=5$ faces. Une pyramide à base carrée possède une base et quatre triangles : $1+4=5$ faces. Le même nombre de faces ne signifie pas le même solide.
:::
### 2. Les surfaces courbes
Un cylindre fermé possède deux bases en forme de disques et une surface latérale courbe. Un cône possède une base en forme de disque et un sommet principal. La boule n’a pas de face plane.

## II. Comprendre un patron
::: definition Du dessin à la maquette
Un patron d’un solide est une figure plane constituée de ses faces, que l’on peut replier pour reconstruire le solide sans trou ni superposition de faces.
:::
::: methode Contrôler un patron
1. Vérifier le nombre et la forme des faces.
2. Vérifier les longueurs des côtés qui se raccorderont.
3. Imaginer le pliage ou découper une maquette.
4. Vérifier que chaque face occupe sa place, sans recouvrement.
:::

[IMAGE_2]

::: exemple Le patron en croix
Quatre carrés forment une bande ; un carré est attaché au-dessus du deuxième et un autre au-dessous. La bande ferme les quatre côtés ; les deux autres carrés ferment le dessus et le dessous. Les six carrés ont la même taille.
:::
::: attention Six carrés ne suffisent pas
Un rectangle de deux rangées de trois carrés n’est pas un patron de cube : certains sommets intérieurs réunissent quatre carrés, alors que trois faces seulement se rencontrent à un sommet du cube.
:::

## III. Construire et vérifier
::: methode Patron d’un cube
Choisir la longueur de l’arête. À la règle et à l’équerre, tracer la bande de quatre carrés identiques, puis les deux carrés de fermeture. Contrôler les angles droits et les longueurs avant de découper.
:::
::: exemple Arête de 2 cm
Chaque carré mesure 2 cm de côté. La bande de quatre carrés mesure $4\times2=8$ cm de long ; la croix complète mesure $3\times2=6$ cm de haut.
:::
::: methode Patron d’un pavé droit
Pour une boîte de dimensions 5 cm, 3 cm et 2 cm, prévoir deux rectangles de 5 cm sur 3 cm, deux de 5 cm sur 2 cm et deux de 3 cm sur 2 cm. Les bords raccordés doivent avoir exactement la même longueur.
:::

[IMAGE_3]

::: attention Languettes et perspective
Une languette sert à coller : ce n’est pas une face supplémentaire. Un dessin en perspective est une représentation du solide, pas son patron ; les arêtes cachées peuvent y être en pointillés.
:::
::: retenir
Reconnaître les faces ; comparer les côtés qui se rejoignent ; vérifier le pliage. Le nombre de faces seul ne permet pas de valider un patron.
:::
''',r'''## I. Reconnaître
| Solide | Repère |
|---|---|
| Cube | 6 carrés identiques |
| Pavé droit | 6 rectangles |
| Prisme droit | 2 bases identiques ; rectangles latéraux |
| Pyramide | 1 base ; triangles vers un sommet |
| Cylindre | 2 disques de base |
| Cône | 1 disque de base ; 1 sommet principal |
| Boule | Surface courbe sans face plane |

## II. Vérifier un patron
::: methode
Contrôler les faces, les dimensions des bords raccordés, puis le pliage : aucun trou et aucune superposition.
:::
::: retenir
Cube : 6 faces, 12 arêtes, 8 sommets. Pour construire un patron, tracer de vrais carrés ou rectangles à la règle et à l’équerre.
:::
::: attention
Six carrés quelconquement disposés ne forment pas forcément un patron. Les languettes ne sont pas des faces.
:::
''',('cube','patron_croix_corrige','patron_pave'))
DOCS[147]=(r'''::: objectifs
- Préparer une enquête et recueillir des réponses ou des mesures fiables.
- Construire un tableau simple ou croisé et contrôler ses totaux.
- Filtrer des données pour faire un choix et justifier une conclusion prudente.
:::

## I. Préparer la collecte
::: definition Une enquête statistique
Une enquête recueille des informations sur un groupe de personnes ou d’objets. Le caractère étudié est ce que l’on observe : moyen de transport, activité préférée, hauteur d’une plante… Une donnée est une réponse ou une mesure obtenue.
:::
::: methode Planifier une enquête
1. Définir la question à laquelle on veut répondre.
2. Préciser qui ou quoi observer, à quel moment et dans quel périmètre.
3. Préparer une question neutre ou un protocole de mesure commun.
4. Choisir si une ou plusieurs réponses sont autorisées.
5. Prévoir comment noter toutes les réponses, y compris les non-réponses.
:::
::: exemple Choisir un atelier
Pour connaître les préférences de tous les élèves de sixième, interroger seulement un club sportif ne suffit pas. On peut proposer à tous le même choix entre jardinage, théâtre et échecs, à raison d’une réponse par élève.
:::
::: attention Mesures comparables
Préciser l’unité, les points de départ et d’arrivée d’une mesure, la date et les conditions. « Non renseigné » ne veut pas dire zéro.
:::

## II. Organiser et contrôler les données
::: definition Effectif
L’effectif d’une catégorie est le nombre de réponses qui appartiennent à cette catégorie. Si chaque personne fournit exactement une réponse, la somme des effectifs est le nombre de répondants.
:::
::: methode Construire un tableau
Prévoir des colonnes clairement nommées ; ajouter l’unité des mesures. Regrouper les réponses identiques, compter une seule fois chaque réponse, puis vérifier le total avec les documents de collecte.
:::

| Classe | Théâtre | Dessin |
|---|---|---|
| 6A | 8 | 12 |
| 6B | 11 | 9 |

::: exemple Lire un tableau croisé
L’intersection de la ligne 6B et de la colonne Théâtre donne 11 élèves. La colonne Dessin compte $12+9=21$ élèves. La classe 6A compte $8+12=20$ répondants.
:::
::: attention Réponses multiples
Si une personne peut citer plusieurs loisirs, la somme des citations peut dépasser le nombre de personnes. Indiquer clairement l’unité de comptage.
:::

## III. Représenter et choisir
Des barres comparent des catégories. Une courbe ou un ensemble de points montre une évolution dans le temps. Un diagramme circulaire représente des parts d’un même ensemble. Donner un titre, des libellés et une échelle lisible.

[IMAGE_1]

::: methode Filtrer selon plusieurs critères
Lire le sens des contraintes : « au moins » inclut la borne basse ; « au plus » inclut la borne haute. Pour chaque ligne, vérifier toutes les contraintes. Ne retenir que les lignes qui les respectent simultanément.
:::
::: exemple Choisir une sortie
Un groupe de 28 élèves dispose de 250 €. Un musée offre 30 places pour 240 € : il reste $30-28=2$ places et $250-240=10$ €. Un lieu moins cher mais limité à 25 places ne convient pas.
:::

## IV. Interpréter avec prudence
::: methode Conclure à partir des données
Répondre à la question initiale ; citer les nombres utiles ; préciser le groupe et la période concernés ; signaler les données manquantes et les limites de la collecte.
:::
::: attention Observation et cause
Une baisse observée ne prouve pas qu’une seule action l’a causée. Deux relevés peuvent différer à cause de la météo, du nombre de présents ou du protocole de mesure. Un résultat d’une classe ne décrit pas automatiquement tout le collège.
:::
::: retenir
Une enquête complète comporte préparation, collecte, tableau contrôlé, représentation utile et conclusion argumentée. Les nombres prennent leur sens dans leur contexte.
:::
''',r'''## I. Mener une enquête
::: methode
Définir la question et le groupe ; recueillir les données avec un protocole commun ; construire un tableau ; contrôler les totaux ; représenter ; conclure.
:::

## II. Lire et décider
- **Effectif** : nombre de réponses d’une catégorie.
- Tableau croisé : lire ensemble le nom de la ligne et de la colonne.
- Filtrer : tester toutes les conditions, pas seulement une.
- « Au moins » et « au plus » incluent la valeur limite.

::: attention
Une absence de donnée n’est pas zéro. Des réponses multiples comptent des citations. Une enquête locale ne permet pas une conclusion sur toute une population.
:::
::: retenir
Noter les unités, les dates et le périmètre de collecte ; justifier chaque choix avec les données utiles.
:::
''',('emprunts_corrige',))
DOCS[148]=(r'''::: objectifs
- Lire des effectifs, des tableaux et plusieurs types de graphiques.
- Calculer des totaux, des écarts et des parts simples.
- Comparer des groupes et critiquer une interprétation trompeuse.
:::

## I. Donner du sens aux données
::: definition Valeur et effectif
Une série de données rassemble des réponses ou des mesures. La valeur est ce qu’on observe ; l’effectif compte combien de fois cette valeur apparaît. Le total des effectifs est l’effectif total.
:::

| Livres lus | Effectif d’élèves |
|---|---|
| 0 | 3 |
| 1 | 7 |
| 2 | 5 |

::: exemple Deux dénombrements différents
Le tableau concerne $3+7+5=15$ élèves. Le nombre de livres lus est $3\times0+7\times1+5\times2=17$ livres. Additionner les effectifs et compter les objets ne répond pas à la même question.
:::
::: methode Contrôler une lecture
Lire le titre, les libellés et les unités. Dans un tableau croisé, chercher l’intersection de la bonne ligne et de la bonne colonne. Vérifier si un total porte sur une ligne, une colonne ou tout le tableau.
:::

## II. Lire plusieurs représentations
### 1. Diagramme en barres
Chaque barre correspond à une catégorie. Sa hauteur donne l’effectif selon l’axe gradué ; toutes les barres ont la même largeur.

[IMAGE_1]

::: exemple Totaliser des emprunts
Lundi : 4, mardi : 6, mercredi : 3. Le total vaut $4+6+3=13$ emprunts. Mardi est le jour le plus fréquenté, mais ses 6 emprunts ne représentent pas plus de la moitié du total.
:::
### 2. Courbe ou points dans le temps
Repérer le moment sur l’axe horizontal, puis la valeur sur l’axe vertical. Des valeurs successives peuvent augmenter ou diminuer.

[IMAGE_2]

::: attention Valeur lue et valeur estimée
Une mesure à 10 cm lundi et à 14 cm vendredi ne prouve pas une hauteur exacte de 12 cm mercredi. Un point non mesuré reste inconnu sans hypothèse supplémentaire.
:::
### 3. Diagramme circulaire
Le disque entier représente le total ; chaque secteur en représente une part. Une moitié correspond à 50 %, un quart à 25 %.

[IMAGE_3]

## III. Traiter les données
::: methode Effectif manquant et écart
Pour une catégorie manquante, retirer du total les catégories connues, à condition qu’elles ne se recouvrent pas. Pour un écart, soustraire les deux valeurs dans la même unité.
:::
::: exemple Une case manquante
Sur 40 ventes, 16 jus et 11 eaux sont connus ; il reste $40-16-11=13$ compotes.
:::
::: methode Former une proportion
Diviser l’effectif de la catégorie par l’effectif total. Une fraction comme $6/24=1/4$ peut aussi s’écrire 0,25 ou 25 %.
:::
::: attention Effectif et proportion
10 marcheurs sur 20 représentent 50 %, alors que 12 sur 30 représentent 40 %. Le deuxième groupe contient davantage de marcheurs, mais leur part est plus petite.
:::

## IV. Argumenter et critiquer
Avant de conclure, vérifier les unités, l’origine des axes, la période et la taille des groupes. Un axe coupé peut exagérer visuellement une petite différence. La valeur la plus fréquente n’est pas nécessairement choisie par plus de la moitié des personnes.
::: retenir
Lire avec le contexte ; vérifier les totaux ; distinguer nombres de personnes, nombres d’objets et proportions. Justifier une comparaison par des valeurs précises.
:::
''',r'''## I. Lire
- **Valeur** : réponse ou mesure observée.
- **Effectif** : nombre de réponses de cette valeur.
- **Total** : somme des effectifs.
- Barres : lire les hauteurs avec l’échelle.
- Courbe : associer un moment et une valeur.
- Disque : le cercle entier représente le total.

## II. Calculer
::: methode
Effectif manquant : total moins les effectifs connus. Écart : différence des valeurs. Part d’une catégorie : effectif de la catégorie divisé par le total.
:::
::: exemple
$6/24=1/4=0{,}25$, soit 25 %.
:::
::: attention
Lire les unités et l’origine de l’axe. Pour comparer des groupes de tailles différentes, préciser si l’on compare des effectifs ou des proportions.
:::
''',('emprunts_corrige','temperatures','transports'))
DOCS[149]=(r'''::: objectifs
- Reconnaître le hasard et distinguer possible, impossible et certain.
- Calculer une probabilité dans des cas simples d’équiprobabilité.
- Comparer la probabilité calculée aux proportions observées lors d’essais.
:::

## I. Décrire les chances
::: definition Une expérience aléatoire
On connaît les résultats possibles, mais on ne peut pas prévoir avec certitude celui qui va se produire. Lancer un dé ou tirer un jeton dans un sac mélangé en sont des exemples.
:::
::: propriete Une échelle entre 0 et 1
La probabilité mesure une chance de réalisation. Elle est comprise entre 0 et 1 : 0 pour un résultat impossible ; 1 pour un résultat certain ; 1/2 pour une chance sur deux.
:::
::: exemple Avec un dé usuel
Obtenir 7 est impossible. Obtenir un nombre inférieur à 7 est certain. Obtenir 4 est possible, mais pas certain.
:::

## II. Compter lorsque les résultats ont la même chance
::: definition Équiprobabilité
Des résultats sont équiprobables lorsqu’ils ont la même chance de se produire. On utilise ce modèle pour un dé équilibré, ou des jetons de même forme et même masse bien mélangés et tirés sans regarder.
:::
::: methode Dénombrer puis diviser
1. Lister les résultats élémentaires de même chance.
2. Compter ceux qui conviennent à la question.
3. Diviser ce nombre favorable par le nombre total.
4. Vérifier que le quotient est entre 0 et 1.
:::
$$
\text{Probabilité}=\frac{\text{nombre de cas favorables}}{\text{nombre de cas possibles}}
$$
::: exemple Obtenir un nombre pair
Avec un dé équilibré, 2, 4 et 6 conviennent. Il y a trois faces favorables parmi six : $3/6=1/2=0{,}5$, soit 50 %.
:::

[IMAGE_1]

::: attention Deux couleurs ne font pas forcément deux chances égales
Un sac contenant un rouge et trois bleus donne une chance sur quatre de rouge et trois sur quatre de bleu. Pour une roue, les secteurs doivent avoir le même angle pour être équiprobables.
:::

## III. Deux étapes et répétitions
::: methode Recenser deux lancers
Pour deux lancers d’une pièce équilibrée dans les mêmes conditions, associer chaque premier résultat à chacun des deux seconds résultats. L’ordre compte.
:::

[IMAGE_2]

::: exemple Exactement un pile
Les quatre couples équiprobables sont PP, PF, FP et FF. Les deux couples PF et FP conviennent : la probabilité vaut $2/4=1/2$.
:::
::: attention Le lancer suivant
Une pièce équilibrée ne se souvient pas des résultats précédents. Après quatre piles, la probabilité de pile au prochain lancer reste 1/2. Il n’y a pas de compensation obligatoire.
:::

## IV. Comparer calcul et essais
::: definition Proportion observée
Sur une série d’essais, on divise le nombre de réussites par le nombre total d’essais. Cette proportion décrit la série réalisée.
:::
::: exemple Un résultat qui fluctue
Sur 20 lancers d’une pièce équilibrée, 12 piles donnent $12/20=0{,}6$, soit 60 %. La probabilité théorique reste 50 % ; une autre série peut donner une autre proportion. Des séries plus longues tendent à stabiliser les proportions, sans imposer une égalité exacte.
:::
::: attention Le protocole compte
Remettre un jeton et mélanger conserve la composition du sac. Sans remise, les effectifs restants peuvent changer et il faut recalculer avec le nouvel état.
:::
::: retenir
Vérifier l’équiprobabilité avant de diviser ; compter les résultats élémentaires ; distinguer probabilité du modèle et proportion d’une série observée. Une probabilité ne promet pas un résultat exact.
:::
''',r'''## I. Les repères
Impossible : 0 ; une chance sur deux : 1/2 ; certain : 1. Une probabilité reste entre 0 et 1.

## II. Calculer
::: methode Cas de même chance
Lister les cas possibles, compter ceux qui conviennent, puis calculer :
$$\frac{\text{cas favorables}}{\text{cas possibles}}$$
:::
::: exemple
Avec un dé équilibré, les pairs sont 2, 4, 6 : $3/6=1/2=50\,\%$.
:::

::: attention
Deux couleurs ne sont pas toujours équiprobables. Les résultats précédents n’imposent pas le suivant. Une proportion observée sur quelques essais peut différer de la probabilité théorique.
:::
::: retenir
Pour deux étapes, lister les couples dans un tableau ou un arbre ; l’ordre peut compter.
:::
''',('roue_reguliere_corrige','deux_lancers_corrige'))
DOCS[152]=(r'''::: objectifs
- Identifier une instruction, une séquence, une entrée et une sortie.
- Exécuter ou produire un programme simple, avec ou sans machine.
- Utiliser une répétition ; programmer et vérifier un chemin.
:::

## I. Lire des instructions dans l’ordre
::: definition Instruction et séquence
Une instruction est un ordre élémentaire : avancer, tourner, ajouter un nombre ou afficher un résultat. Une séquence est une liste d’instructions exécutées dans l’ordre indiqué.
:::
::: attention L’ordre fait partie du programme
« Ajouter 3 puis doubler » diffère de « doubler puis ajouter 3 ». Pour l’entrée 5, le premier donne $5+3=8$, puis $8\times2=16$ ; le second donne $5\times2=10$, puis $10+3=13$.
:::

## II. Entrée, calculs et sortie
::: definition Suivre les données
Une entrée est une donnée fournie au programme. Une sortie est une information qu’il affiche ou produit. Un calcul intermédiaire peut être utilisé par l’instruction suivante.
:::
```console
demander un nombre
ajouter 2 au nombre saisi
multiplier le résultat par 2
afficher le résultat final
```
::: exemple Un test
Avec l’entrée 6, on obtient $6+2=8$, puis $8\times2=16$. La sortie est 16. Afficher un résultat ne modifie pas automatiquement l’entrée ; il faut respecter ce que le programme indique.
:::
::: methode Tester une séquence
Noter l’entrée ; exécuter une seule instruction à la fois ; conserver le résultat intermédiaire ; continuer jusqu’à la sortie ; comparer à un résultat attendu.
:::

## III. Répéter un bloc
::: definition Répétition
Une répétition exécute un même bloc un nombre donné de fois. Le bloc peut contenir plusieurs instructions. La répétition porte sur toutes les instructions qu’il contient.
:::
```console
partir de 2
répéter 3 fois :
    ajouter 4 au résultat courant
```
::: exemple Suivre les passages
Les résultats successifs sont 6, 10 et 14. Le nombre initial 2 existe avant le premier passage : trois répétitions produisent trois nouveaux résultats.
:::
::: methode Écrire plus court
Repérer un bloc identique qui se répète ; compter ses occurrences ; l’écrire une seule fois dans une boucle ; tester que la séquence obtenue garde les mêmes actions.
:::

## IV. Programmer un chemin
### 1. Deux codages à distinguer
Dans un codage global, « haut » signifie toujours le haut de la feuille. Dans un codage relatif, « avancer » dépend de l’orientation actuelle ; « tourner à gauche » change cette orientation, sans déplacement.

[IMAGE_1]

::: exemple Déplacement global
Depuis A1, avec colonnes vers la droite et lignes vers le haut, « droite de 3 ; haut de 2 » mène à D3. Le trajet compte $3+2=5$ cases.
:::
### 2. Construire un carré
```console
partir orienté vers la droite, crayon baissé
répéter 4 fois :
    avancer de 3 cases
    tourner d’un quart de tour à gauche
```

[IMAGE_2]

::: exemple Vérifier le tracé
Les quatre déplacements tracent les quatre côtés du carré. La distance parcourue vaut $4\times3=12$ cases. Le robot revient au départ ; le dernier virage lui rend son orientation initiale.
:::
::: methode Déboguer un programme
Préciser la position et l’orientation initiales. Exécuter ligne par ligne ; repérer le premier écart avec le chemin voulu ; corriger l’instruction ou la répétition ; refaire le test depuis le début.
:::
::: attention
Tourner ne fait pas avancer. Le nombre de répétitions n’est pas toujours le nombre total d’instructions. Le chemin doit respecter les obstacles et pas seulement atteindre l’arrivée.
:::
::: retenir
Une instruction doit être précise. Respecter l’ordre et les résultats intermédiaires ; distinguer entrée et sortie ; vérifier une boucle par ses passages et un chemin par ses positions successives.
:::
''',r'''## I. Les mots clés
- Instruction : ordre élémentaire.
- Séquence : instructions dans un ordre précis.
- Entrée : donnée fournie ; sortie : résultat produit.
- Répétition : même bloc exécuté plusieurs fois.

## II. Exécuter et vérifier
::: methode
Noter l’état initial ; exécuter une instruction à la fois ; garder les résultats intermédiaires ; contrôler la sortie ou le point d’arrivée.
:::

::: retenir
Pour un carré : répéter 4 fois « avancer d’un côté ; tourner d’un quart de tour ». Pour un chemin, préciser le sens des déplacements ou l’orientation initiale.
:::
::: attention
Tourner ne déplace pas. « Ajouter puis doubler » n’est pas « doubler puis ajouter ». Une boucle répète toutes les instructions de son bloc.
:::
''',('chemin_L','carre'))

for n,(cours,fiche,figs) in DOCS.items():
    d=next(R.glob(f'{n}_*'));meta=json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf8'))
    titre=meta['titre'];cid=str(meta['cours'][0]['id']) if meta['cours'] else 'nouveau';fid=str(meta['fiches'][0]['id']) if meta['fiches'] else 'nouvelle'
    (d/f'cours_{cid}.txt').write_text('Titre: '+titre+'\n\n<!-- optitab:1 -->\n'+cours,encoding='utf8')
    (d/f'fiche_{fid}.txt').write_text('Titre: Résumé : '+titre+'\n\n<!-- optitab:1 -->\n'+fiche,encoding='utf8')
    p=d/'figures/correspondance.json';cor=json.loads(p.read_text(encoding='utf8'))
    cor['cours'][cid]={str(i+1):{'fichier':nom+'.png','alt':titre+' : '+nom.replace('_',' ')} for i,nom in enumerate(figs)}
    p.write_text(json.dumps(cor,ensure_ascii=False,indent=2),encoding='utf8')
