# Notion 255 — Calcul littéral et distributivité (4e)

**État : prêt** (claude-255, 2026-11-03). 21 exercices (aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée).

## Cours et fiche

- **Titres** inchangés : « Calcul littéral et distributivité » et « Résumé : Calcul littéral et distributivité » (intitulé de la notion).
- **Cours 250 réécrit façon manuel** (il tenait en 4 pavés) : objectifs en liste ; I. expressions littérales (définition, conventions d'écriture, méthode « dernière opération » pour traduire une phrase avec l'exemple $3x - 5$ / $3(x - 5)$, méthode de substitution, exemple aligné, pièges $(-2)^2$ / $-2^2$ et $3x$ pour $x = 5$) ; II. réduire (termes, réduire une somme et un produit, 3 erreurs) ; III. simple distributivité (définition de développer, propriété, figure d'aire, 3 exemples alignés, suppression des parenthèses, exemple, 2 erreurs) ; IV. factoriser (définition, méthode en 3 points, 3 exemples, « il reste 1 », plus grand facteur commun) ; V. double distributivité (propriété, figure d'aire, **démonstration** par deux simples distributivités, méthode, exemple $(3x + 2)(x - 4)$, contrôle par une valeur, erreurs) ; VI. programmes de calcul et preuves (méthode, programme en schéma avec expressions en vert, vrai / faux / contre-exemple, écriture des entiers, somme de deux consécutifs impaire, exemples ≠ preuve) ; « À retenir ». Emojis, HTML, `\displaystyle`, faux encadrés « définition » et renvoi « onglet Fiches » supprimés.
- Exemples du cours changés pour ne plus doubler les exercices : $5x^2 - 3x + 1$ pour $x = -2$ (au lieu de $A$ de 2580), $18x - 24$ (au lieu de $12a - 18$ de 2584), somme de deux consécutifs (au lieu de trois, traité dans 2592), $x^2 + 2 = 3x$ (au lieu de $3x + 2x = 5x^2$, traité dans 2585).
- Les identités remarquables (3e) ne sont pas au cours : $(x + 4)^2$, $(n - 1)^2$, $(x + 3)^2$, $(10n + 5)^2$ ne sont développés dans les exercices que par la double distributivité.
- **Fiche 170 refaite** : 5 parties (écrire et calculer, tableau « réduire », développer avec 2 formules encadrées et 2 figures, factoriser, prouver), 6 erreurs classiques, réflexe ; plus de puces « • ».

## Exercices (21)

- **Tous relus et réécrits** au format des modèles : questions numérotées ; corrigé avec méthode, étapes détaillées (calculs alignés, « les quatre produits » écrits avant de réduire), résultat encadré, et une erreur fréquente ou un « À retenir » dans chaque exercice ; vérifications en encadré `point` ; `Solution:` courte cohérente. Titres « Type - Calcul littéral - n. Sujet » → « Type - Sujet » (21 titres changés).
- **Progression** : 7 Découverte (2579–2585), 7 Entraînement (2586–2592), 4 Problème (2593–2596), 3 **Type brevet** (2597–2599), dans l'ordre des Id.
- **Erreur de maths corrigée** : 2579 Q6 donnait « le quadruple de $x$ diminué de $2$ » comme traduction de $4(x - 2)$ (c'est $4x - 2$). La question compare désormais les deux expressions ($12 \neq 18$ pour $x = 5$). 2599 (ancien) avait une solution tronquée « A si x 18 ».
- **Remplacés (4)** :
  - 2589 « La bordure du tapis » (doublon de 2593 « piscine et margelle » : aire d'une bordure de 1 m) → « Entraînement - Corriger des erreurs de calcul littéral » (6 erreurs typiques : contre-exemple puis calcul juste ; $x = 1$ qui ne suffit pas pour $2x \times 4x = 8x$ ; figure d'aire de $(x + 4)(x + 1)$).
  - 2591 « Les tables alignées » (doublon de 2582 « allumettes » : même démarche $2n + 2$ / $4n - 2(n - 1)$) → « Entraînement - Associer des expressions égales » (5 expressions à développer, association, intrus réfuté par contre-exemple puis factorisé).
  - 2596 « Du calcul mental » (fondé sur $(a + b)(a - b) = a^2 - b^2$, $(a \pm 1)^2$ : identités remarquables de 3e) → « Problème - Calculer mentalement grâce à la distributivité » ($37 \times 101$, $56 \times 99$, factorisations $17 \times 23 + 17 \times 77$ et $4{,}7 \times 13 - 4{,}7 \times 3$, $21 \times 32$ par double distributivité avec figure, règle des carrés terminés par 5 démontrée avec $(10n + 5)^2 = 100n(n + 1) + 25$).
  - 2599 « Choisir le bon tarif » (comparaison de tarifs, sans distributivité, relève des fonctions) → « Type brevet - Vrai ou faux en calcul littéral » (6 affirmations : substitution, double distributivité, factorisation, contre-exemple, programme de calcul avec division, somme de 3 consécutifs multiple de 6 réfutée).
- **Retravaillés** : 2580 (Q6 : retrouver l'erreur de signe de Léo), 2581 (produit $5 \times (-4x)$), 2584 (Q1 par le modèle d'aire : retrouver les longueurs), 2587 (« doubler » : comparaison avec $88$ au lieu d'un quotient approché), 2588 (programmes en schéma), 2595 (erreur fréquente sans le mot « double produit »), 2597 (passé en Type brevet ; tableau natif des volumes pour $x$ de 1 à 9, ce qui justifie vraiment le maximum ; question des valeurs possibles avant le tableau), 2598 (passé en Type brevet, figure découpée au corrigé).
- `verif_255.py` : **185 contrôles** sympy / fractions exactes (cours, fiche, chaque question des 21 exercices, carré magique complet, tableau des volumes, programmes rejoués), tout juste.

## Figures (style livre, `figures/figures.py`)

- **31 figures neuves, 33 emplacements** ; les **16 images matplotlib en ligne sont toutes remplacées ou retirées** (0 conservée ; 2 non appelées, supprimées à l'import : 2589 position 2 et 2591 position 1, exercices remplacés).
  - Cours (3) : modèle d'aire de $k(a + b)$, de $(a + b)(c + d)$, programme de calcul avec expressions en vert. Fiche (2) : les deux modèles d'aire.
  - Exercices (28 emplacements, 15 exercices) : énoncé + corrigé en vert pour 2582 (allumettes : 1 + 3 par carré), 2583, 2584, 2586, 2587 (modèles d'aire), 2588 (programmes A et B, un corrigé par programme), 2593 (margelle découpée en bandes et coins), 2594 (carré magique, corrigé $x = 5$), 2595 (tour du magicien), 2597 (plaque, fond $30 - 2x$ sur $20 - 2x$), 2598 (rectangle et carré, un corrigé découpé par question), 2599 (programme) ; corrigés seuls 2589 ($(x + 4)(x + 1)$) et 2596 ($21 \times 32$).
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance (`TOLERE`) ; toutes ≤ 900 px. Après relecture : têtes d'allumettes qui se touchaient aux coins → allumettes écartées des coins ; programmes de calcul, plaque (2597), piscine (2593) et rectangle / carré (2598) rétrécis pour rester lisibles sur téléphone ; corrigé de 2598 séparé en deux figures (rectangle $A$ à la question 4, carré $B$ à la question 5).

## Contrôles

- `verifier_notion.py --navigateur` : **OK, 0 problème** (notes : 21 titres changés ; 2 images en ligne non appelées).
- `controle_apercu.mjs` avec captures : « Aucun problème détecté » (téléphone et ordinateur, cours, fiche, 21 exercices). Captures regardées : cours en téléphone (5 vues), fiche, exercices 2580 (énoncé), 2579, 2586, 2588, 2589, 2591, 2593, 2595, 2596, 2597, 2598, 2599 (étapes).
- Corrigé après captures : exemples du cours (développer, factoriser) et propriétés qui étaient réduits → un calcul aligné par exemple, formules sur deux lignes ; chaînes « $x \to \dots$ » des programmes (2588, 2599) qui laissaient un point seul en début de ligne → listes ; calculs en ligne trop longs (2586 Q6, 2591 Q6, 2597 Q5, 2598 Q6, 2599 Q3) → calculs alignés ; tableau des volumes de 2597 à 10 colonnes (défilait) → tableau en 2 colonnes, énoncé et corrigé.
- Une compilation de figure a échoué une fois (moteur LaTeX occupé par les autres agents) : relancée seule, OK.

## Remarques pour l'orchestrateur

- Programme : identités remarquables non exigées ; elles n'apparaissent qu'en découverte par le calcul (double distributivité). Les petites équations ($3n + 1 = 61$, $6x + 6 = 42$) sont résolues en « remontant les calculs », sans technique d'équation (notion 256).
- Le titre de la notion côté cours / fiche est inchangé (rien à renommer en base).
