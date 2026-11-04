# Rapport : 2nde / 177 « Variables et instructions élémentaires » (Python)

**État : prêt.** `verifier_notion.py --navigateur` : OK, 0 problème ; `controle_apercu.mjs` : aucun problème ; `verif_variables_instructions.py` : 58 blocs Python exécutés, sorties identiques aux blocs `console`, valeurs numériques vérifiées, lignes ≤ 30 caractères (≤ 29 dans les étapes).

## Périmètre
Programme de Seconde 2019 : types (`int`, `float`, `str`, `bool`), affectation, séquence, formule combinant des variables, `if`/`elif`/`else`, boucles `for` et `while`, lire / compléter / modifier un programme. Les fonctions (`def`, `return`, `random`) restent dans la notion 178.

## Texte
- Cours réécrit en 6 parties : I. variables et types (tableau des types, `type`, conversions, pièges point décimal / guillemets, noms) ; II. affectation et séquence, échange de deux variables avec tableau de suivi ; III. opérations, priorités, `from math import pi, sqrt`, parenthèses ; IV. conditionnelle (syntaxe, comparaisons, `and`/`or`/`not`, exemple en trois cas) ; V. `for` (`range` à 1, 2, 3 arguments, méthode de l’accumulateur, tableau de suivi) ; VI. `while` (seuil 2^n > 1 000 avec tableau de suivi, boucle infinie, choisir entre `for` et `while`).
- Fiche refaite : types, opérations, trois codes modèles, tableau `for` / `while`, 5 erreurs classiques.
- Tous les guillemets « » qui étaient dans le code ont été retirés, ainsi que la balise HTML `<code>` dans les titres. Le code n’est plus placé dans les titres d’étapes. Les tableaux de suivi sont des tableaux natifs.
- **Corrections et remplacements** :
  - 1974 Q5 : la suite récurrente $u_{n+1} = 2u_n - 3$ était hors programme de Seconde, car les suites sont au programme de Première. Elle est remplacée par un programme à compléter qui contient deux boucles imbriquées et affiche les nombres premiers jusqu’à 20.
  - 1974 Q4 : l’énoncé « tant que S ≤ 100 » était ambigu. Il devient un vrai seuil, « dépasser 100 », dont le résultat est 11 impairs et une somme de 121.
  - 1974 : la variable `compteur` est renommée `nb` pour que les lignes de code restent courtes.
  - 1970 : `pi = 3.14` est remplacé par `from math import pi`. Les résultats deviennent 25π ≈ 78,54 et 36π ≈ 113,10. Une question Q6 est ajoutée : conversion d’une durée avec `//` et `%`.
  - 1971 : la Q3 « demande un nombre » supposait `input`. Elle est reformulée avec une variable déjà affectée. Une question Q6 est ajoutée : `and`, `or` et l’appartenance à un intervalle.
  - 1968 Q3 : le type de `6 / 2` est ajouté. 1973 Q3 : la correction de la boucle infinie est ajoutée.
- Les 7 exercices existants sont réécrits en version pédagogique (méthode, étapes, résultat, erreur fréquente). Les Id et les titres sont inchangés.
- **Ajouts** :
  - `nouveau-1` « Entraînement - Repérer et corriger les erreurs d'un programme » : cinq erreurs à trouver, à savoir `=` au lieu de `==`, l’accumulateur placé dans la boucle, la borne de `range`, la condition du `while` et le type `str`. La compétence « modifier / corriger un programme » n’était pas travaillée.
  - `nouveau-2` « Problème - Comparer deux tarifs avec un programme » : une modélisation qui utilise `if`/`elif`/`else`, puis une boucle `while` de seuil. Le résultat (11 séances) est confirmé par une inéquation.

## Figures
- 3 images en ligne refaites. Elles étaient d’un style ancien, contenaient du code en image et une légende coupée :
  - `affectation.png` : l’état de la mémoire après chaque affectation. Elle est utilisée dans le cours et dans la fiche.
  - `organigramme_si.png` : l’organigramme de `if` / `else`.
  - `organigramme_tantque.png` : l’organigramme de la boucle `while`. Cette figure est ajoutée à la partie VI.
- Le tableau de suivi qui était en image (cours position 3 et fiche position 2) est remplacé par un tableau natif. L’image de la fiche n’est plus appelée et sera supprimée à l’import.
- 0 image conservée.

## Contrôles
Captures téléphone regardées : cours (vues 1, 3, 4, 5), fiche, étapes de 1974, 1973 et nouveau-2. Trois tableaux trop larges sur téléphone ont été corrigés : le tableau des comparaisons et le tableau de primalité de 1974, qui sont passés à la verticale, et le tableau de suivi de nouveau-2, dont l’en-tête a été raccourci.

## Remarques pour l’orchestrateur
- Sur téléphone, les deux organigrammes (environ 880 px) s’affichent un peu petits, mais restent lisibles. Il n’y a ni débordement ni chevauchement.

## Finition 2026-11-02

**État : prêt** (agent-finition-S4). 9 → **12 exercices**.

### Titres
- Cours et fiche : « Variables et instructions élémentaires (Python) » → intitulé officiel « Utiliser les variables et les instructions élémentaires ».
- 1974 « Approfondissement - … » → « Problème - Diviseurs et nombres premiers : lire et modifier un programme » ; apostrophes typographiques et parenthèses retirées des autres titres.

### Exercices ajoutés (Id nouveau-3 à nouveau-5 : nouveau-1 et nouveau-2 sont déjà 3756 et 3757 en base)
- `nouveau-3` « Découverte - Suivre les cases mémoire d’un programme de caisse » : types, tableau de suivi, affectation non permanente (`cher` reste `True`), remise de 10 % par coefficient (`33.75 True`).
- `nouveau-4` « Entraînement - Boucle while et compteur : la balle qui rebondit » : seuil, cas limite `10 >= 10`, erreur `while h > 10` (affiche 4), for ou while, accumulateur (`5 155.0`).
- `nouveau-5` « Type examen - Le vol de Syracuse : boucles et conditions » : `while` + `if/else`, `//` et types, maximum d’une suite de valeurs, boucles imbriquées (vol le plus long : 9, 19 étapes), conjecture en « Pour aller plus loin ».

### Figures
- **Revérifiées une par une (3)** : `affectation`, `organigramme_si`, `organigramme_tantque` : justes, lisibles, aucun chevauchement → conservées.
- **10 ajoutées** : cases mémoire (1968 types, 1969 échange raté avec la valeur perdue, nouveau-3), 1970 (200 min = 3 × 60 + 20), 1971 (organigramme if/elif/else, chemin de note = 14 en vert), 1972 (`range(2, 8, 2)` sur une droite), 1973 (capital année par année, seuil 1 000 €), 3757 (deux tarifs), nouveau-4 (hauteurs des rebonds), nouveau-5 (vol de 6).
- 10 exercices sur 12 ont une figure ; sans figure : 1974 et 3756 (lecture et correction de code).

### Contrôles
- `verif_variables_instructions.py` : 67 blocs Python exécutés, sorties identiques aux blocs `console` ; en plus, **25 programmes d’énoncés exécutés** et comparés aux réponses des corrigés (dont « il affiche 5 / 45 / 0 » de 3756) ; lignes ≤ 30 caractères.
- Téléphone : étiquettes des nouvelles figures en taille normale ; tableau de suivi de nouveau-5 ramené à 3 colonnes (la dernière colonne était coupée).
- `figures_livre.py` : 0 erreur (aucun texte sur un trait, aucune figure > 1 100 px) ; chaque PNG regardé.
- `verifier_notion.py` : 0 problème de contenu ; seuls signalés : les Id 3756 et 3757, créés en base le 29/10 mais absents de `source_en_ligne/` (export du 29/10 antérieur à leur création) → **ré-export nécessaire avant import** (outil réservé à l’orchestrateur).
- Contrôle navigateur (`controle_apercu.mjs`, téléphone + ordinateur) : 76 vues, aucun problème détecté. Chrome restant parfois bloqué à la fermeture (défaut connu), seul mon processus a été arrêté et son verrou libéré.
- Captures téléphone regardées : cours, fiche et exercices à nouvelles figures.
