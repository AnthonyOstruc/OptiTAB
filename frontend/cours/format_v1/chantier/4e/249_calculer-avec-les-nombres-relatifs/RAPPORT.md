# Notion 249 (4e) : Calculer avec les nombres relatifs

**État : prêt** (agent-4e-249, 2026-11-03). 21 exercices (aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée).

## Cours et fiche

- **Titres** inchangés : « Calculer avec les nombres relatifs » et « Résumé : Calculer avec les nombres relatifs » (intitulé de la notion).
- **Cours 244 réécrit façon manuel** : objectifs en liste ; I. rappels (définition relatif / opposé, propriétés d'addition et de soustraction, exemples, droite graduée des déplacements) ; II. multiplication (règle des signes en propriété + tableau natif, exemples, remarque « pourquoi moins par moins donne plus », multiplication par $-1$, produit de plusieurs facteurs : propriété, méthode en 3 points, exemple, regroupement aligné, erreurs fréquentes) ; III. division (définition du quotient, règle des signes et écritures fractionnaires $\frac{-a}{b} = \frac{a}{-b} = -\frac{a}{b}$, division par zéro, méthode de contrôle) ; IV. priorités (propriété, schéma, une ligne par étape, crochets et trait de fraction, piège « de gauche à droite », substitution d'une valeur négative) ; V. problèmes (valeur finale / variation / écart, températures, altitudes, compte bancaire) ; « À retenir ». Emojis, HTML, `\displaystyle` et renvoi « onglet Fiches » supprimés.
- Exemples du cours changés pour ne plus doubler les exercices : $(-50) \times 13 \times (-2)$ (au lieu de 2472 Q1), $-36 : 4 \times (-3)$ (au lieu de 2469 Q5), $4 - 3x$ pour $x = -2$ (au lieu de 2477 Q1).
- **Fiche 164 refaite** : 5 parties (addition/soustraction, multiplication/division avec tableau des signes natif, priorités, problèmes, pièges), 3 figures, conseil « Réflexe ».

## Exercices (21)

- **Tous réécrits** au format des modèles : questions numérotées ; corrigé avec méthode, étapes détaillées (calculs alignés), résultat encadré, et au moins une erreur fréquente ou un « à retenir » par exercice ; `Solution:` courte cohérente. Titres « Type - Sujet » (21 titres changés, « Relatifs - n. » retiré).
- **Progression** : 7 Découverte (2464–2470), 7 Entraînement (2471–2477), 4 Problème (2478–2481), 3 **Type brevet** (2482 programme de calcul, 2483 profil de randonnée, 2484 fuseaux horaires), en fin de liste.
- **Doublons remplacés** :
  - 2471 : la question B (« déplacer les parenthèses », déjà travaillée dans 2469) → calcul avec **trait de fraction** $\frac{-3 \times 4 - 9}{2 - 9} = 3$ ; titre « Enchaîner des calculs avec crochets et traits de fraction ».
  - 2473 : la question 3 reprenait exactement $24 : (-6) \times 2$ (2469 et cours) → $40 : (-5) \times 2 = -16$.
- **Améliorés** : 2465 (tableau natif à compléter + figure de la régularité « $+2$ »), 2475 (opérations en tableau, diagramme du solde, erreur sur les 3 abonnements), 2476 (tableau natif au lieu d'une image), 2482 (questions de type brevet, tableau de conjecture, démonstration par division terme à terme), 2474 (erreur fréquente dénivelé / altitude).
- Aucune erreur de maths dans l'ancien contenu. `verif_249.py` : **194 contrôles** sympy en fractions exactes (cours, fiche, chaque question des 21 exercices, programme, pyramides, carré magique, conversions °F), tout juste.

## Figures (style livre, `figures/figures.py`)

- **29 figures neuves, 32 emplacements** ; les **22 images matplotlib en ligne sont toutes remplacées ou retirées** (0 conservée ; 1 image en ligne non appelée, supprimée à l'import : 2465 position 2).
  - Cours (5) : opposés, déplacements sur la droite graduée, schéma des priorités, thermomètre ($3$ °C → $-5$ °C, variation en vert), altitudes (goéland / plongeuse, écart 53 m).
  - Fiche (3) : déplacements, priorités, thermomètre.
  - Exercices (24) : thermomètre 2464 (énoncé sans valeurs + corrigé avec l'écart en vert), tableau $a \times (-2)$ 2465, deux déplacements depuis $-8$ 2468, montagne 2474 (énoncé + corrigé : 0 °C à 2 400 m, −3 °C, −4,8 °C), solde 2475, droite des températures 2476, sous-marin et drone 2478 (énoncé + corrigé), échelles °C / °F 2479, carré magique 2480 (énoncé + corrigé), 5 pyramides 2481 (2 énoncés, 3 corrigés dont la pyramide modifiée), programme de calcul 2482 (énoncé + corrigé), profil 2483 (énoncé + corrigé), fuseaux 2484 (énoncé + corrigé).
  - Règle des signes : ancienne image remplacée par un **tableau natif** (cours et fiche).
- `figures_livre.py` : 0 chevauchement texte/trait, aucune tolérance (`TOLERE`) ; toutes ≤ 900 px. Après relecture sur téléphone : droites resserrées (−5 à 5), schéma des priorités réduit aux trois étapes (il était trop réduit), programme et diagramme du solde rétrécis.

## Contrôles

- `verifier_notion.py --navigateur` : **OK, 0 problème** (notes : titres changés).
- `controle_apercu.mjs` avec captures : téléphone et ordinateur, cours, fiche et 21 exercices. Captures regardées : cours en téléphone (4 vues), fiche (2 vues), exercices 2464 (énoncé), 2465 (énoncé), 2475, 2478 et 2482 (étapes).
- Chrome ne s'est pas refermé seul à la fin du premier `controle_apercu.mjs` (captures toutes produites) : seul mon processus Node a été arrêté.

## Remarques pour l'orchestrateur

- Les rappels d'addition/soustraction (programme de 5e) sont gardés en partie I et dans 2 exercices de découverte (2464, 2468) : prérequis indispensable à la règle des signes.
- 2479 (degrés Fahrenheit) et 2482 (démonstration avec $x$) touchent au calcul littéral de 4e ; niveau conforme.
