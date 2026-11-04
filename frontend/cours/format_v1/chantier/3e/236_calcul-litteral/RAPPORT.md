# Notion 236 — Calcul littéral (3e)

**État : prêt** (agent-3e-C3, 2026-11-03).

## Cours et fiche

- **Titres** : « Développer, factoriser et prouver » → « Calcul littéral » (cours) et « Résumé : Calcul littéral » (fiche), intitulé de la notion. **Attention** : `importer_v1.py` ne met à jour que le corps des cours et fiches (cf. rapport 166) → renommer en base si souhaité.
- **Cours réécrit** : objectifs en liste ; I. expressions littérales (définitions réduire / développer / factoriser, méthode de substitution avec parenthèses, exemple aligné, 3 erreurs fréquentes dont $(-2)^2$ / $-2^2$) ; II. développer (propriétés simple et double distributivité, deux figures d'aires, exemple aligné, contrôle par une valeur) ; III. factoriser (méthode en 3 points, exemples, erreur $5x + 5$) ; IV. identités remarquables (théorème, **démonstration** par double distributivité, figure d'aires de $(a + b)^2$, exemples développer / factoriser / calcul astucieux, erreur du double produit) ; V. démontrer (méthode, programme de calcul avec figure, écritures des entiers pairs / impairs / consécutifs, carré d'un impair, exemples ≠ démonstration). Les exemples ne sont plus dans des encadrés « définition ».
- **Fiche** refaite : tableau de vocabulaire, formules encadrées, figure de la double distributivité, factorisation, démonstration, 4 erreurs classiques.

## Exercices (21)

- Tous relus, **corrigés réécrits** : méthode, étapes détaillées (calculs alignés), résultat encadré, **erreur fréquente** dans chaque exercice ; `\displaystyle` retirés.
- **Titres** « Type - Calcul littéral - n. Sujet » → « Type - Sujet » (21).
- **Remplacé (1)** : 2199 « Tester des conjectures » (doublon : $(x + 2)^2 - x^2$ et $(x + 3)^2 - x^2$ déjà dans 2175 et 2177) → « Entraînement - Développer à l'aide d'une figure » (rectangle $(2x + 3)(x + 5)$ découpé en 4 aires).
- **Retravaillés** : 2174 (programmes en schéma, conjecture puis démonstration, question « obtenir 100 ») ; 2175 (question 3 nouvelle : découpage de la bordure) ; 2178 (question 4 nouvelle : $1\,001^2 - 1\,000 \times 1\,002$ sans calculatrice) ; 2176 (démonstration par cas pour $n(n + 1)$) ; 2162 (contrôle avec deux valeurs) ; 2197 (contre-exemple : pourquoi $x = 1$ ne suffit pas).
- Progression : 7 Découverte, 7 Entraînement, 5 Problème, 2 **Type brevet** (2179 « Choisir la forme adaptée », 2200 « Sommes d'entiers consécutifs », en fin de liste).

## Figures (10, style livre, aucune ancienne image conservée)

- **Refaites (2)** : distributivité simple $k(a + b)$ (cours ; ancienne image matplotlib) ; bordure (énoncé 2175).
- **Ajoutées (8)** : double distributivité (cours + fiche), carré $(a + b)^2$ (cours), programme de calcul avec expressions en vert (cours), carré $(x + 6)^2$ (corrigé 2198), rectangle $(2x + 3)(x + 5)$ énoncé + corrigé (2199), programmes A et B (énoncé 2174), bordure découpée $8x + 16$ (corrigé 2175).
- `figures_livre.py` : 0 chevauchement texte/trait, 0 avertissement.

## Contrôles

- `verif_236.py` : **95 contrôles** sympy (développements, factorisations, valeurs, équations, démonstrations), tout juste.
- `verifier_notion.py` : OK, 0 problème. Avec `--navigateur`, Chrome ne se ferme pas seul (code de sortie anormal, aucune ligne en défaut) → contrôle refait avec `controle_apercu.mjs` seul : **130 vues (téléphone + ordinateur, cours, fiche, 21 exercices × 3 onglets), toutes à 0** (débordement, formules, `$` bruts, images, blocs, largeur) ; mes processus Chrome/Node bloqués arrêtés un par un.
- Captures téléphone regardées : cours (parties II à V), fiche, exercices 2163, 2174, 2175, 2199 (étapes). Corrigé après captures : démonstration de $(a + b)^2$ **coupée** → calcul aligné ; exemples d'identités et de calcul astucieux réduits → alignés sur deux lignes ; tableau de vocabulaire de la fiche coupé → 2 colonnes + exemples en liste ; 2169 (5 calculs) et 2200 Q5 alignés ; figure du programme de calcul resserrée.

## Remarques pour l'orchestrateur

- Programme : seule l'identité $(a + b)(a - b) = a^2 - b^2$ est explicitement exigible en cycle 4 ; $(a + b)^2$ et $(a - b)^2$ sont présentées comme conséquences de la double distributivité (démonstration dans le cours). La factorisation par $a^2 + 2ab + b^2$ (2173, questions 4–5) est guidée dans l'énoncé.
- L'équation produit nul (2179) relève aussi de la notion 237 « Équations » : gardée car classique au brevet.
