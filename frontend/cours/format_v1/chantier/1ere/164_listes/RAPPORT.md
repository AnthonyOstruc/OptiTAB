# Rapport : Première, notion 164 « Notion de liste »

**État : prêt.** Le cours 152, la fiche 62 et les 9 exercices (les 5 existants, réécrits, et 4 ajoutés) sont au format OptiTAB v1. Les titres du cours et de la fiche sont « Notion de liste » et « Résumé : Notion de liste ». Aucune écriture en base, aucune commande git.

## Programme (2019, Première spécialité, « Algorithmique et programmation »)

Couvert, et seulement cela :
- génération d’une liste en extension, par ajouts successifs (`append`) et en compréhension (avec un filtre `if`) ;
- manipulation des éléments et des indices : `L[i]`, `L[-1]`, `len`, `L[i] = v`, erreur `IndexError`, correspondance indice/rang d’une suite ;
- parcours par les éléments et par les indices ; accumulateur, compteur, maximum et son indice ;
- usages en maths : termes d’une suite (et nuage de points), tableau de valeurs d’une fonction, simulation (liste de résultats, effectifs, fréquences, moyenne), coefficients directeurs des sécantes vers le nombre dérivé.

Les conditions et les boucles (Seconde) servent sans être réenseignées : elles figurent en prérequis.

**Retiré (hors programme ou purement informatique)** : `insert`, `remove`, `pop`, `index`, `count`, `sort`, `sorted`, `reverse`, les tranches et les listes de chaînes sans lien avec les maths.

## Texte

- **Cours réécrit de zéro.** Il a six parties : définition et longueur ; indices (avec un schéma), modification, lien indice/rang ; trois façons de générer une liste et comment choisir ; deux parcours et trois algorithmes de référence ; les listes en mathématiques (suite et nuage, tableau de valeurs, simulation d’un dé, sécantes de x² en 1 avec le calcul 2 + h) ; erreurs fréquentes et « à retenir ».
- **Fiche réécrite** : indices, génération, parcours, tableau des usages en maths, 4 pièges, 2 figures.
- **Exercices existants**. Les 5 étaient faibles ou hors programme (méthodes `index`, `count`, `insert`, `remove`, tri). Ils sont **remplacés** dans leur bloc ; les Id sont conservés et les titres changés :
  - 1063 « Découverte - Indices et éléments d'une liste » (températures d’une semaine) ;
  - 1065 « Entraînement - Générer une liste de trois façons » (extension, `append`, compréhension, choix selon formule explicite ou récurrence) ;
  - 1064 « Découverte - Suivre des ajouts successifs avec append » (tableau de suivi, suite associée, u₁₀ = 93) ;
  - 1067 « Entraînement - Parcourir une liste : moyenne, fréquence, maximum » (précipitations) ;
  - 1066 « Entraînement - Liste des termes d'une suite » (uₙ₊₁ = 2uₙ − 3, formule explicite, somme, nuage).
- **Défauts de l’ancienne version** : le convertisseur avait mis des « » à la place des guillemets dans le code, une sortie était tronquée (« 3 12 → max = 15 ») et plusieurs solutions restaient vagues (« affiche les trois étapes »).
- **Exercices ajoutés** (compétences « usages en maths » non travaillées) :
  - `nouveau-1` « Entraînement - Tableau de valeurs d'une fonction avec deux listes » (x² − 4x + 3, pas de 0,5, minimum conjecturé puis démontré par la forme canonique) ;
  - `nouveau-2` « Problème - Simuler des lancers de deux dés avec une liste » (fréquence de 7 comparée à 1/6, moyenne comparée à 7, liste des effectifs avec l’indice s − 2) ;
  - `nouveau-3` « Problème - Coefficients directeurs des sécantes et nombre dérivé » (x² − 3x en 2, taux 1 + h, g′(2) = 1, tangente y = x − 4) ;
  - `nouveau-4` « Entraînement - Parcours par indices et sens de variation d'une suite » (liste des différences, uₙ₊₁ − uₙ = 2n − 6).
- Chaque corrigé suit le modèle méthode, étapes, résultat encadré, avec une erreur fréquente quand elle est utile.

## Code exécuté (consigne 4)

- `verif_listes.py` **exécute réellement les 49 programmes** : 13 dans le cours, 1 dans la fiche et 35 dans les exercices. Les 38 affichages annoncés sont **identiques** aux affichages réels. Les programmes à compléter (`...`) s’exécutent sans erreur. Un bloc commençant par `# suite du programme` reprend les variables du programme précédent.
- Les simulations ont des graines fixes (`seed(1)`, `seed(2)`), et le texte explique ce rôle aux élèves. Les fonctions de `figures/figures.py` produisent les mêmes données que les programmes, et le script vérifie qu’elles concordent.
- 60 assertions supplémentaires portent sur les valeurs du texte et des figures, ainsi que sur l’algèbre (sympy) : taux de variation, formes canonique et explicite, différences, tangente, probabilités.
- Le script vérifie aussi la largeur des lignes de code sur téléphone : au plus 35, 31 ou 29 caractères selon l’encadré. Tout est **OK** (`verif_log.txt`).

## Figures (consigne 5)

- **15 figures neuves au style des livres, aux 21 emplacements prévus.** Les 4 images en ligne (style matplotlib) sont toutes remplacées, et aucune n’est conservée.
- **Cours (5)** : schéma des indices, liste qui grandit avec `append`, nuage d’une suite avec y = 4, histogramme de la simulation avec 1/6, sécante (AM) avec h, f(1 + h) − f(1) et la tangente.
- **Fiche (2)** : les deux premières figures du cours.
- **Exercices** :
  - 1063 : indices en vert dans le corrigé ;
  - 1064 : ajouts successifs dans le corrigé ;
  - 1066 et nouveau-1 : repère vide dans l’énoncé, points en vert dans le corrigé ;
  - nouveau-2 : fréquences et probabilités ;
  - nouveau-3 : schéma de la sécante dans l’énoncé, sécantes et tangente dans le corrigé ;
  - nouveau-4 : nuage avec le minimum en vert.
- Le détecteur ne signale aucun texte sur un trait. Toutes les figures font 636 à 830 px de large. Chaque PNG a été regardé et retouché : légendes déplacées, graduation 3 posée à droite du point M, sécante raccourcie qui frôlait une graduation, largeurs réduites pour le téléphone.

## Contrôles

- `verifier_notion.py --navigateur` : **OK, 0 problème** (`verif_navigateur_log.txt`). L’outil s’est terminé normalement.
- `controle_apercu.mjs` avec captures : 58 vues, toutes à 0 (`captures_log.txt`).
- **Captures téléphone regardées à l’œil** : le cours en entier (6 écrans), la fiche (2 écrans) et les étapes des exercices 1063, 1064, nouveau-1 et nouveau-2. Corrections faites après relecture :
  - le tableau de la fiche, avec du code dans les cellules, était coupé (non détecté par l’outil) : il est remplacé par une liste ;
  - le tableau de valeurs à 8 colonnes du cours est remplacé par une phrase ;
  - le tableau à 10 colonnes de l’énoncé de nouveau-1 est mis en 2 colonnes.
- **Mesure complémentaire** dans Chrome à 390 px (script personnel, hors du dossier) : aucun bloc de code, tableau, formule ou code en ligne ne déborde de son cadre.

## Remarques pour l’orchestrateur

- **Défaut du contrôleur** : un tableau dont les cellules contiennent du code peut être coupé sur téléphone sans être signalé. Exemple : l’ancienne fiche, ligne `[k**2 for k in range(6)]`. Il faudrait comparer `scrollWidth` et `clientWidth` du conteneur de chaque tableau et de chaque `.otm-code`.
- **Titre de la notion** : l’aperçu affiche encore « Listes » (meta.json de l’export). Le cours et la fiche portent « Notion de liste ».
- **4 exercices à créer** à l’import (`nouveau-1` à `nouveau-4`) ; leurs figures sont déclarées dans `correspondance.json`.

## Enrichissement 2026-11-03

**État : prêt** (non importé). La notion passe de 9 à **12 exercices** : 3 blocs ont été ajoutés à la fin de `exercices.txt` (`Id: nouveau-1` à `nouveau-3`). Aucun bloc n’a été supprimé et aucune ligne `Id:` n’a été modifiée. Aucune écriture en base, aucune commande git. Sauvegardes : `sauvegardes/164E_*_avant_enrichissement_20261103.*`.

Les 9 exercices existants ont été relus. Ils sont complets (méthode, étapes, résultat, solution) et justes. Un seul était incomplet : **4948** (sécantes) n’avait pas d’erreur fréquente. J’ai ajouté un encadré « attention » : `taux(0)` provoque `ZeroDivisionError`, d’où la liste de valeurs de h qui se rapprochent de 0. Les 8 autres sont identiques à l’octet près.

### Exercices ajoutés

| Id | Titre | Difficulté | Compétences |
|---|---|---|---|
| nouveau-1 | Entraînement - Moyenne, médiane et écart type d'une série de notes | medium | deux listes parallèles (notes, effectifs) et parcours par indices ; génération par ajouts successifs (boucles imbriquées) ; indices et rangs (médiane = moyenne de `L[9]` et `L[10]`) ; moyenne 12,5, variance 4,75, écart type ≈ 2,18 ; compréhension avec filtre : 19 notes sur 20 dans [m − 2s ; m + 2s] |
| nouveau-2 | Problème - Suite de Syracuse : la liste des termes d'un vol | hard | liste des termes d’une suite (exemple cité par le programme) ; `while` et `append` sur `L[-1]` ; temps de vol `len(vol(N)) - 1` ; algorithme du maximum, puis indice du maximum (vol de 7 : 16 étapes, altitude 52 au rang 5) ; liste en compréhension des temps de vol ; 27 a le plus long vol jusqu’à 30 (111 étapes, altitude 9 232) |
| nouveau-3 | Type examen - Deux placements : suites et listes | hard | Partie A : suites arithmétique (aₙ = 1 000 + 60n) et géométrique (bₙ = 1 000 × 1,04ⁿ). Partie B : compréhension ou ajouts successifs selon la définition ; parcours de deux listes au même indice, avec bₙ > aₙ pour la première fois au rang 21 ; liste des intérêts, bₙ₊₁ − bₙ = 40 × 1,04ⁿ > 60 dès la 12e année ; retard maximal ≈ 120,55 € au rang 11 |

Les niveaux sont maintenant répartis ainsi : 2 Découverte, 6 Entraînement, 3 Problème et 1 Type examen (il n’y en avait aucun). Les compétences visées étaient peu travaillées : statistiques avec des listes, liste de termes d’une suite de longueur inconnue, comparaison de deux suites par les indices. Les exercices sur l’espérance et l’échantillonnage ont été écartés, car ils existent déjà dans les notions 161 et 163.

Chaque exercice comporte un énoncé à questions numérotées et un corrigé : méthode, étapes détaillées, programmes avec leur affichage, résultat encadré et au moins une erreur fréquente par question délicate. Exemples de ces erreurs : `L[10]` pris pour la 10e valeur, division par `len(X)`, `X[i] - m**2`, `u / 2` qui donne des décimaux, `len(vol(N))` pris pour le temps de vol, `imax` pris pour l’entier cherché, `while B[n] < A[n]` qui s’arrête à n = 0, `I[11]` pris pour la 11e année. La solution courte suit le corrigé.

### Figures (4 nouvelles, style des livres, `figures_livre.py` : 4/4, aucun refus de chevauchement)
- `exn5_liste` (nouveau-1, corrigé Q2) : les 20 notes de `L` sur deux lignes, avec les indices 0 à 19 ; `L[9]` et `L[10]` sont en vert.
- `exn5_batons` (nouveau-1, corrigé Q5) : bâtons des effectifs, moyenne m en pointillés et intervalle [m − 2s ; m + 2s] en vert ; les notes qu’il contient sont en vert, la note 8, hors de l’intervalle, en bleu.
- `exn6_vol` (nouveau-2, corrigé Q4) : nuage du vol de 7, avec le maximum u₅ = 52 en vert et u₁₆ = 1.
- `exn7_placements` (nouveau-3, corrigé Q5) : nuages de aₙ et bₙ pour n de 0 à 30, avec le croisement n = 21 en vert.
- Pas de figure dans les énoncés, car elle donnerait la réponse. Largeurs de 726 à 880 px. Chaque PNG a été regardé ; une retouche : l’étiquette u₁₆ = 1, trop près du tracé, a été remontée. Les données des figures sont calculées par du vrai Python dans `figures.py`, et `verif_listes.py` les compare au texte.

### Contrôles
- `verif_listes.py` : **54/54 programmes exécutés réellement**, dont 37 avec l’affichage annoncé identique à l’affichage réel. **111 contrôles de valeurs**, dont 51 nouveaux. Ils portent sur la moyenne, la variance, les bornes et la proportion (sympy, valeurs exactes), sur les vols de Syracuse et sur les suites aₙ, bₙ et leurs différences (sympy, rationnels exacts : rang 21, rang 11, retard maximal). Ils couvrent aussi `taux(0)` et les erreurs fréquentes annoncées. La largeur des lignes de code pour le téléphone est vérifiée. Résultat : **OK** (`verif_log.txt`).
- `verifier_notion.py --navigateur` : **contrôle Chrome sans aucun défaut** (téléphone et ordinateur). Les 4 seules alertes, « Id d’exercice inconnu en ligne : 4946 à 4949 », viennent de `source_en_ligne/meta.json`. Cet export date du 29/10, avant l’import du 02/11 qui a créé ces Id. Le même contenu, vérifié dans une copie temporaire dont le `meta.json` connaît ces 4 Id, donne **OK, 0 problème** (`verif_navigateur_log.txt`). `publier_lot.ps1` ré-exporte avant l’import, donc rien n’est à faire de ce côté.
- Un premier passage signalait des `code.otm-c` trop larges : c’étaient des codes en ligne de plus de 35 caractères dans mes solutions (le code en ligne ne se coupe pas). Ils sont réécrits ou passés en blocs.
- `controle_apercu.mjs` avec captures : toutes les vues à 0 (`captures_log.txt`). Chrome est resté bloqué à la fermeture, après l’écriture des captures. Seul mon processus node (aperçu 164) a été arrêté, et son verrou `chrome_0.lock` a été libéré. Les verrous des autres sessions n’ont pas été touchés.
- **Captures téléphone regardées à l’œil** (énoncé, étapes et solution des 3 nouveaux exercices) : aucun code ne déborde. Corrections faites après relecture :
  - « 11e » coupé en fin de ligne : nombres ordinaux écrits en texte ;
  - « 40 » et « € » séparés : espace insécable ;
  - « = 12 » ou « = bₙ » seuls en début de ligne après un code en ligne : « vaut » ;
  - formule de retard réduite : découpée ;
  - « b) » ou « c) » orphelins dans les solutions : sous-listes.

### Remarques pour l’orchestrateur
- 3 exercices à créer à l’import (`nouveau-1` à `nouveau-3`), avec leurs figures déclarées dans `correspondance.json`.
- `optitabDoc.js` a été modifié aujourd’hui (16 h 20) par une autre session. Les contrôles ci-dessus ont été faits avec cette version.
