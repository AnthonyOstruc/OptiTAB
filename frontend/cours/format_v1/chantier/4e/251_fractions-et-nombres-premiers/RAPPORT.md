# Notion 251 — Fractions et nombres premiers (4e)

**État : prêt** (agent-4e-251, 2026-11-03). 21 exercices (aucun ajout, 2 remplacés).

## Cours et fiche

- **Cours 246 réécrit façon manuel** : objectifs en liste ; I. divisibilité (définition multiple / diviseur, **tableau des critères 2, 3, 4, 5, 9, 10** — absents avant), nombres premiers (définition, premiers < 30 à connaître, crible, erreurs 1 / impairs, méthode « prouver premier ou non », exemple 97) ; II. décomposition (propriété d'unicité, méthode, arbre de 360, calcul aligné, erreur « décomposition non terminée ») ; III. fractions égales et irréductibles (méthode, exemple 84/60 justifié, erreur « simplifier un terme ») ; IV. **comparer** (absent avant : même dénominateur, fractions négatives, droite graduée) ; V. somme et différence (exemples 5/6 + 7/15 et −3/4 + 5/6) ; VI. produit, simplifier avant, **inverse** (définition, 0 sans inverse, inverse ≠ opposé), quotient, **priorités** ; VII. fraction d'une quantité, fraction d'une fraction, retrouver le tout, tout de référence ; « À retenir » final. Les exemples ne sont plus dans des encadrés « définition » ; le renvoi « onglet Fiches » est supprimé.
- **Fiche 166 refaite** : tableau des critères, premiers < 30, test, arbre, tableau des opérations (comparer, +, −, ×, inverse, ÷, fraction de), 5 erreurs classiques, réflexe ; plus de puces « • » ni de `\displaystyle`.
- Titres inchangés (= intitulé de la notion).

## Exercices (21)

- Tous relus et **corrigés réécrits** au format des modèles : méthode, étapes détaillées (calculs alignés), résultat encadré, **erreur fréquente** dans chaque exercice (+ « À retenir » quand utile) ; les étapes vides de la conversion automatique (contenu passé dans le titre) sont refaites ; `\displaystyle` retirés ; « Vérification » en encadré `point`.
- **Titres** « Type - Fractions - n. Sujet » → « Type - Sujet » (21 titres).
- **Remplacés (2)** :
  - 2516 « Des bouquets identiques » (plus grand diviseur commun, doublon de 2526 « Carreler une pièce ») → « Entraînement - Utiliser les critères de divisibilité » (tableau à compléter pour 2 340, 1 485, 7 128, 4 011 ; chiffres manquants ; 9 ⇒ 3 et contre-exemple ; décomposer 2 340) — les critères, au programme, n'étaient travaillés nulle part ;
  - 2520 « Le budget familial » (fraction du total puis du reste, doublon de 2521 « Aménager un jardin ») → « Type brevet - Vrai ou faux sur les fractions et les nombres premiers » (6 affirmations : impair ⇒ premier, 2/3 + 3/4, inverse de −4/5, 3 465 divisible par 9, 126/294 = 3/7, diviser par 1/2).
- **Retravaillés** : 2512 recentré sur le calcul avec des relatifs et les priorités (B et F nouveaux ; la comparaison, doublon de 2518, est retirée) et passé en « Entraînement » ; 2507 : arbre de 504 à compléter (au lieu de 360, déjà dans le cours) et question 6 menée jusqu'à « 211 est premier » ; 2506 : questions 1-2 fusionnées ; 2511 : « 0 a-t-il un inverse ? » ; 2525 : 1 h 30 traitée en 3/2 h (plus de « 1,5/6 ») ; 2526 passé en « Type brevet », question 7 en cm².
- Progression : 6 Découverte, 8 Entraînement, 5 Problème, 2 Type brevet (2520, 2526).
- Aucune erreur de maths dans l'ancien contenu ; `verif_251.py` : **213 contrôles** sympy / Fraction (décompositions, primalité, critères, crible, toutes les fractions, problèmes rejoués), tout juste.

## Figures (27 neuves, style livre, `figures/figures.py`)

- Les **23 images matplotlib en ligne sont toutes remplacées ou retirées** : 0 conservée. Retirées : énoncé décoratif de la piscine (2525, la position 1 reçoit la figure du corrigé) et la figure du budget (2520 remplacé, supprimée à l'import).
- Cours (6) : crible 1-50, arbre de 360, comparaison sur deux droites graduées, somme 1/2 + 1/3 en barres, modèle d'aire 2/3 × 4/5, les 3/4 de 28 ; fiche (2) : arbre de 360, somme en barres.
- Exercices (21 emplacements, 14 exercices) : énoncé + corrigé en vert pour 2507 (arbre de 504), 2509 (barres), 2510 (aire), 2515 (crible 1-60), 2517 (réservoir), 2521 (jardin), 2526 (carrelage) ; corrigés 2511 (verres de 1/8 L), 2513 (gâteau), 2514 (classe), 2518 (droite en 24ᵉ), 2522 (chameaux), 2523 (frise des phares), 2525 (robinets).
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance déclarée ; toutes ≤ 900 px. Après relecture : droite de 2518 élargie (fractions collées), arbre corrigé recoloré (facteurs premiers distinguables), chameaux resserrés (917 px → < 900), étiquette « réservoir plein » retirée de l'énoncé (trompeuse).
- Pas de figure sur les calculs purs (2506, 2508, 2512, 2516, 2519, 2520, 2524).

## Contrôles

- `verifier_notion.py --navigateur` : **OK, 0 problème** (notes : titres changés ; 1 image en ligne non appelée, celle de l'ancien 2520, supprimée à l'import). `controle_apercu.mjs` avec captures : aucun problème (téléphone et ordinateur).
- Captures téléphone regardées : cours (5 écrans), fiche (2 écrans), exercices 2507 (énoncé), 2513, 2516, 2521 (étapes). Corrections faites après relecture : fractions en ligne qui se tassaient d'une ligne à l'autre → formules centrées (cours IV, V, VI inverse, VII ; fiche III) ; tableau de résultat à 7 colonnes de 2516 (défilait) → liste ; double droite graduée du cours resserrée ; figure du jardin réduite (étiquettes sur trois lignes) ; ligne « Inverse » du tableau de la fiche raccourcie ; unité « L » rejetée seule à la ligne.
- Le premier contrôle Chrome a été coupé par un délai trop court que j'avais fixé (500 s) ; relancé sans délai : OK.

## Remarques pour l'orchestrateur

- « Plus grand diviseur commun » et « plus petit multiple commun » sont écrits en toutes lettres comme outils de résolution (2523, 2526), sans notation PGCD / PPCM.
- Puissances ($2^3$) utilisées dans les décompositions, en plus de l'écriture développée (puissances au programme de 4e, notion 252).
