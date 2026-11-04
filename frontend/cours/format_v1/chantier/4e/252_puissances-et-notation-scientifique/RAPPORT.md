# Notion 252 (4e) : Puissances et notation scientifique

**État : prêt** (claude-252, 2026-11-03). 21 exercices (aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée).

## Cours et fiche

- **Titres** inchangés : « Puissances et notation scientifique » et « Résumé : Puissances et notation scientifique ».
- **Cours 247 réécrit façon manuel**, au programme de 4e : objectifs en liste ; I. puissances d'un relatif (définition, conventions $a^1$ et $a^0$, signe selon la parité, parenthèses et priorités avec exemple, **exposant négatif $a^{-n} = \frac{1}{a^n}$**, remarque de découverte $2^3 \times 2^4 = 2^7$ en comptant les facteurs : les règles générales sont renvoyées à la 3e) ; II. puissances de 10 (écriture décimale, tableau milliard → milliardième, déplacement de la virgule + figure, **règles exigibles** en tableau, démonstration par comptage des facteurs, exemple enchaîné, erreurs fréquentes) ; III. préfixes de nano à giga (tableau, figure de l'échelle « × 1 000 », méthode de conversion) ; IV. notation scientifique (définition, méthode, correction du premier facteur, **comparaison**, produit et quotient, piège de la somme) ; V. **ordres de grandeur** (définition avec la règle $a \lt 5$ / $a \geq 5$, exemples, échelle des tailles de l'atome à la Voie lactée, comparer, contrôler un calcul) ; « À retenir ». Emojis, `\displaystyle`, renvoi « onglet Fiches » et définitions mal typées (exemples dans des encadrés « définition ») supprimés.
- **Fiche 167 refaite** : 6 parties (puissances, puissances de 10 avec tableau des règles, préfixes, notation scientifique, ordres de grandeur, 5 pièges), 2 figures, conseil « Réflexe ».

## Exercices (21)

- **Tous réécrits** au format des modèles : questions numérotées ; corrigé avec méthode, étapes détaillées (calculs alignés), résultat encadré, et au moins une erreur fréquente ou un « à retenir » par exercice ; `Solution:` courte et cohérente. Titres « Type - Sujet » (« Puissances - n. » retiré).
- **Progression** : 7 Découverte (2527–2533), 7 Entraînement (2534–2540), 4 Problème (2541–2544), 3 **Type brevet** (2545 plage, 2546 satellite, 2547 réacteur), en fin de liste.
- **Remplacés** (doublons ou exercices faibles) :
  - 2534 « Les grains de riz sur l'échiquier » (troisième exercice de doublement, avec 2528 et 2542) → **« Entraînement - Calculer avec des puissances de 10 »** : produits, quotients, puissance de puissance, exposants négatifs, deux calculs type brevet en notation scientifique (aucun exercice d'entraînement ne travaillait les règles exigibles).
  - 2542 « La croissance des bactéries » (doublement, déjà vu) → **« Problème - De la bactérie à la galaxie : ordres de grandeur »** : conversions avec préfixes, ordres de grandeur, placement sur une échelle, estimations contrôlées par le calcul (compétence du programme absente des exercices).
  - 2535 : les questions sur Proxima du Centaure doublaient 2541 → remplacées par « combien de fois plus loin » et l'année-lumière ; tableau de données en image → tableau natif.
- **En partie réécrits** : 2527 (question 6 sur les exposants négatifs $2^{-1}$, $2^{-3}$, $10^{-2}$), 2537 (doublait 2527 : nouvelles expressions, $(-1)^n$, exposants négatifs, $(-2)^{-3}$), 2532 (tableau natif à compléter au lieu d'une image ; téra remplacé par une éolienne de $12$ MW ; nombre de mm dans un km), 2545 (ordre des questions : correction des vides avant la comparaison aux étoiles, ordre de grandeur final), 2546 (vitesse recalculée avec la longueur arrondie, cohérente d'une question à l'autre).
- Aucune erreur de maths dans l'ancien contenu. La conversion automatique avait cassé une ligne de l'ancien 2542 (« $2^{19} = 524\,288 10^6$ » : les signes `<` et `>` étaient perdus) ; ce bloc est entièrement réécrit, et tous les fichiers finaux utilisent `\lt` et `\gt`.
- `verif_252.py` : **272 contrôles** sympy en valeurs exactes (cours, fiche, chaque question des 21 exercices), tout juste ; les ordres de grandeur sont choisis pour ne dépendre d'aucune convention (premier facteur hors de la zone ambiguë $3{,}16$ – $5{,}5$).

## Figures (style livre, `figures/figures.py`)

- **14 figures neuves, 16 emplacements** ; les **13 images matplotlib en ligne sont toutes remplacées ou retirées** (0 conservée ; 3 images en ligne non appelées, supprimées à l'import : 2532 position 2, 2534 échiquier, 2535 tableau).
  - Cours (3) : déplacement de la virgule ($5{,}8 \times 10^{3}$ et $5{,}8 \times 10^{-2}$, zéros ajoutés en gris), échelle des préfixes nano → giga avec les sauts « × 1 000 », échelle des tailles de l'atome à la Voie lactée (repères 1 nm, 1 µm, 1 mm, 1 m, 1 km).
  - Fiche (2) : virgule, préfixes.
  - Exercices (11) : feuille pliée 2528 (énoncé avec « ? » + corrigé $2^3 = 8$ couches en vert), virgule 2530 (corrigé), préfixes complétés en vert 2532, axe microscopique 2536 (énoncé vide + corrigé), échelle bactérie → Andromède 2542 (énoncé vide + corrigé), plage en pavé droit et grain cubique 2545, satellite à l'échelle 2546 (énoncé + corrigé avec la cote $OS$ en vert).
- `figures_livre.py` : toutes ≤ 900 px. Une tolérance déclarée (`TOLERE`) : la cote verte inclinée de 2546 (le cadre horizontal du texte incliné englobe le rayon orange parallèle ; vérifié à l'œil, aucun trait sous le texte). Avertissement normal : la cote « 3 km » de la plage coupe sa flèche grâce à son fond blanc.

## Contrôles

- `verifier_notion.py --navigateur` : **OK, 0 problème** (notes : titres changés).
- `controle_apercu.mjs` avec captures : aucun problème détecté (téléphone et ordinateur). Vues regardées : cours en téléphone (5 vues), fiche (2 vues), exercices 2528 (énoncé), 2534, 2542 et 2546 (étapes, avec agrandissements).
- Corrigé après relecture des captures : tableau des règles de calcul (exemples coupés) remplacé par une liste ; démonstration du quotient, exemple de la somme, chaînes « corriger le premier facteur », produit et quotient, contrôle par ordre de grandeur : formules trop larges découpées en lignes alignées ; dans les exercices, 25 formules d'une ligne à trois membres ou plus passées en chaînes alignées (plus de formule réduite) ; énoncé de 2534 : une expression par ligne ; fiche : ligne « Contrôler » réécrite.
- Chrome s'est refermé normalement ; aucun processus arrêté.

## Remarques pour l'orchestrateur

- Programme : $a^{-n}$ pour une base quelconque est défini (demande de la consigne) ; les règles $a^m \times a^n$ ne sont exigées que pour les puissances de 10 (base quelconque en remarque de découverte et dans les exercices de découverte uniquement).
- 2528 (pliage) garde les puissances de 2 comme découverte de la notion de puissance.
