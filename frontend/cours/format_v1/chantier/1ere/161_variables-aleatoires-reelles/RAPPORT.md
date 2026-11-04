# Rapport — notion 161 « Variables aléatoires réelles » (Première spécialité)

**État : prêt.** Le cours, la fiche et les 16 exercices (11 existants et 5 ajoutés) sont au format OptiTAB v1. Les 23 figures sont neuves, au style des livres. Les titres du cours et de la fiche reprennent l’intitulé du programme : « Variables aléatoires réelles ».

## Programme (2019, Première spécialité)

Les points suivants sont vérifiés et couverts :
- variable aléatoire réelle vue comme une fonction de Ω dans ℝ ;
- notations {X = a}, {X ≤ a}, P(X = a), P(X ≤ a), et passage de la langue naturelle aux notations ;
- loi, par dénombrement et par arbre ;
- espérance, variance, écart type et formule de König-Huygens (avec démonstration) ;
- E(aX + b), V(aX + b), σ(aX + b) (avec démonstration) ;
- jeu équitable et mise équitable ;
- algorithme qui calcule E, V et σ ;
- simulation en Python, moyenne d’un échantillon, constat de la loi des grands nombres ;
- expérimentation de la proportion des cas où |m − μ| ≤ 2σ/√n.

**Retiré (hors programme de Première)** :
- les coefficients binomiaux (tirages simultanés de 1333, 1338 ; 5 lancers de pièce de 1340), remplacés par des tirages successifs sans remise traités avec un arbre ;
- le schéma à 4 et 5 lancers, qui est la loi binomiale de Terminale (1336, 1340).

Aucune loi de Bernoulli ni loi binomiale nommée, aucun E(X + Y).

## Texte

- **Cours réécrit de zéro.** Il comporte six parties, avec objectifs et prérequis : définition, notations, loi (méthode, exemple avec un arbre), espérance, jeu équitable, variance et écart type (interprétation en termes de risque), König-Huygens avec démonstration, algorithme Python, transformation affine avec démonstration, mise équitable, échantillon et simulation (`gain`, `moyenne`, `proportion`), erreurs fréquentes, « à retenir ». Un même exemple sert de fil rouge : le jeu de dé.
- **Fiche réécrite** : loi, indicateurs, aX + b, jeu équitable, simulation, 5 pièges, 4 figures.
- **Les 11 exercices existants sont réécrits** au modèle du pilote (méthode, étapes, résultat, erreur fréquente). Les Id et les titres sont conservés. La conversion automatique était cassée (égalités `P(X \\ = 3)` coupées dans les `aligned`, tableaux de solution éclatés en lignes isolées, parties en gras).
  - **Erreurs de maths corrigées** :
    - 1339 : σ(G) = √10,25 était donné égal à 3,2, alors qu’il vaut environ 3,20 (3,2² = 10,24) ;
    - 1336 : la question « C5 » ne correspondait à aucune question C4 dans l’énoncé ;
    - 1339 : la question C4 apparaissait en double ;
    - 1340 Partie C : les règles du jeu de cartes se chevauchaient (un roi rouge relevait à la fois de « rouge » et de « figure »), le jeu était donc mal défini. La partie est remplacée.
  - **Contenus remplacés dans leur bloc** :
    - 1336 Partie A : jetons tirés sans remise avec un arbre, au lieu de 4 lancers de pièce ;
    - 1340 Parties B et C : un jeu de 32 cartes aux catégories disjointes, puis une simulation Python (`partie`, `moyenne`, résultats d’une vraie exécution) ;
    - 1333 Q2 et 1338 B : tirages successifs sans remise avec un arbre, au lieu des combinaisons ;
    - 1332 Q1 : loi à compléter et traduction d’un événement, au lieu d’un exercice trivial ;
    - 1334 : paramètres revus (a = 8 sans mise, a = 14 avec 1 € de mise, au lieu de a = 0 qui n’avait pas de sens) ; ajout de σ et d’une comparaison du risque des tickets.
  - Des questions de variance ou d’écart type sont ajoutées dans 1335 (C2, C4), 1337 (V(3X − 2)) et 1339 (E(max)).
- **Exercices ajoutés** (compétences du programme qui n’étaient pas travaillées) :
  - `nouveau-1` « Découverte - Notations et langage des variables aléatoires » ;
  - `nouveau-2` « Entraînement - Algorithme : espérance, variance et écart type » (lecture et écriture de fonctions, tolérance sur les flottants) ;
  - `nouveau-3` « Entraînement - Simuler un jeu et calculer une moyenne d'échantillon » ;
  - `nouveau-4` « Problème - Fluctuation des moyennes d'échantillons » (2σ/√n, proportion, effet de n) ;
  - `nouveau-5` « Entraînement - Comparer deux jeux : espérance et risque ».
- **Vérification** : `verif_variables_aleatoires.py` (sympy) fait **254 contrôles, 0 erreur** (`verif_log.txt`). Il contrôle toutes les lois, espérances, variances, écarts types et arrondis. Il rejoue aussi les simulations citées (graines fixes, mêmes fonctions que les figures) : 96 sur 100 dans le cours, 194 sur 200 et la position des 6 moyennes hors de la bande, et les sorties `moyenne(n)` de 1340 et de nouveau-3.

## Figures

- **23 figures neuves, 0 image en ligne conservée.** Les 4 images en ligne (style matplotlib) sont remplacées aux mêmes positions.
- **Cours (5)** : diagramme en bâtons de la loi, arbre de l’urne, deux lois de même espérance avec leurs écarts types, moyenne cumulée d’une simulation, nuage de 100 moyennes d’échantillons avec la bande μ ± 2σ/√n.
- **Fiche (4)** : les figures du cours sont réutilisées.
- **Exercices (18)** : selon la consigne du 2026-11-02, il y a une figure dans l’énoncé et dans le corrigé.
  - Arbres : squelette à compléter dans l’énoncé, arbre complété dans le corrigé avec les probabilités et les valeurs en vert (1331, 1333, 1336, 1338).
  - Diagrammes en bâtons : repère vide dans l’énoncé, bâtons verts dans le corrigé (1335, 1332).
  - Nuage de moyennes avec les 6 points hors de la bande entourés en vert (nouveau-4).
  - Lois des deux jeux avec E et ±σ en vert (nouveau-5).
  - Moyennes observées et intervalles 2σ/√n (nouveau-3 et 1340).
- Le contrôle des chevauchements donne 0 erreur. Toutes les largeurs sont ≤ 900 px. Chaque PNG a été regardé.

## Contrôles

- `verifier_notion.py --navigateur` : **OK, 0 problème** (27 placements de figures neuves, 0 image en ligne conservée). Voir `verif_navigateur_log.txt`.
  - Le premier passage avait signalé 8 éléments trop larges : des lignes de code de plus de 40 caractères et un long code en ligne. Les programmes ont été raccourcis (listes `x` et `p`, variable `h` pour 2σ/√n).
- `controle_apercu.mjs` avec captures : 100 vues (téléphone et ordinateur ; cours, fiche, 16 exercices × 3 onglets), toutes à 0. Voir `captures_log.txt`.
- **Captures téléphone regardées à l’œil** : le cours en entier (7 écrans), la fiche (2 écrans), et les étapes de 1331, 1336, 1333, 1334, nouveau-1, nouveau-2 et nouveau-4. Corrections faites après ces relectures :
  - plusieurs formules étaient coupées sans que l’outil le signale : formules centrées trop larges dans les `aligned`, et longues formules en ligne (par exemple $E(X^2) = 0{,}5 \times 0 + \ldots$ dans nouveau-2). Toutes sont maintenant découpées en lignes alignées, un signe = par ligne, les sommes longues étant poursuivies avec « + » ;
  - les listes à puces de calculs (« ; » orphelins) sont passées en `aligned` ;
  - l’arbre à 3 niveaux de 1331 a été resserré (897 → 754 px).

  Nouvelle capture : tout est entier.
- `verif_variables_aleatoires.py` : 254 contrôles, 0 erreur.

## Remarques pour l’orchestrateur

- **Défaut d’outil (détection)** : une formule **en ligne** trop longue est coupée sur téléphone, et le contrôle ne le voit pas (0 élément trop large). Une formule centrée qui défile n’est pas signalée non plus. Exemple avant correction : nouveau-2, étape « König-Huygens », `$E(X^2) = 0{,}5 \times 0 + 0{,}3 \times 100 + 0{,}2 \times 400 = 30 + 80 = 110$`. Il faudrait mesurer la largeur de chaque `.katex` par rapport à son conteneur.
- **Défaut d’outil (blocage)** : comme pour la notion 159, `controle_apercu.mjs` ne rend pas la main après la dernière vue. Je l’ai lancé avec `timeout`, puis j’ai arrêté mes processus restés ouverts (node et python de cette notion seulement).

- Linéarité E(aX + b) et V(aX + b) : traitées comme au programme de Première, selon la consigne du propriétaire. Le texte officiel de 2019 les place plutôt avec les sommes de variables en Terminale ; c’est à confirmer si besoin.
- La loi des grands nombres est présentée comme un **constat de simulation**, conformément aux « expérimentations » du programme de Première. Aucun énoncé formel n’est donné.
