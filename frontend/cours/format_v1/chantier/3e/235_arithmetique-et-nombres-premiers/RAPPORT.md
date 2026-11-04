# Notion 235 — Arithmétique et nombres premiers (3e)

**État : prêt** (agent-3e-C3, 2026-11-03).

## Cours et fiche

- **Cours réécrit** : objectifs en liste ; I. multiples, diviseurs (définition complète, méthode « lister tous les diviseurs » par paires, figure des rectangles de 36) + **division euclidienne** (propriété, exemple, erreur « reste trop grand ») + critères de divisibilité ; II. nombres premiers (définition, **liste des premiers < 30 à connaître**, crible, méthode « prouver premier / pas premier », exemple 43) ; III. décomposition (théorème d'unicité, méthode, arbre de 360, calcul aligné complet, erreur « décomposition non terminée ») ; IV. fractions irréductibles (définition, méthode en 2 points, exemple 84/150 avec justification) ; V. partages / rencontres (méthodes, exemples, justification de l'optimalité, tableur `=MOD` et Python `%`). Les exemples ne sont plus dans des encadrés « définition ».
- **Fiche** : refaite dense (formule de la division euclidienne, tableau des critères, premiers < 30, arbre, tableau « situation → outil », exemples, 4 erreurs classiques).
- Titres inchangés (= intitulé de la notion).

## Exercices (21)

- Tous relus et **corrigés réécrits** : méthode, étapes détaillées (calculs alignés), résultat encadré, **erreur fréquente** dans chaque exercice ; `\displaystyle` retirés ; « À retenir » en gras libre → encadrés.
- **Titres** « Type - Chapitre - n. Sujet » → « Type - Sujet » (21 titres).
- **Remplacés (2)** :
  - 2145 « Décomposer et recomposer » (doublon de 2141 et 2194) → « Découverte - Effectuer une division euclidienne » (sachets de billes, 1 000 par 13, reste trop grand) — la division euclidienne n'était travaillée nulle part ;
  - 2158 « Une rencontre de coureurs » (4e problème de rencontres périodiques, doublon de 2154/2196/2157) → « Type brevet - Vrai ou faux en arithmétique » (5 affirmations : somme de premiers, 1 001, 4 et 6 → 24, fraction 2 310/3 465, carré parfait).
- **Retravaillés** : 2146 passe de 72 à 48 (pour illustrer par les rectangles) avec diviseurs communs de 48 et 60 ; 2159 enrichi (décomposition de 144, carré parfait) et passé en « Type brevet » ; 2153 : question « 8 lots ? 6 lots ? » ; 2150 : tableau de la feuille de calcul ; 2194 : définition du carré parfait dans l'énoncé.
- Progression : 7 Découverte, 7 Entraînement, 5 Problème, 2 Type brevet (2158, 2159 en fin de liste).

## Figures (10, style livre, aucune ancienne image conservée)

- **Refaites (3)** : arbre de 360 (cours + fiche), dallage 252 × 180 (énoncé sans la réponse), engrenages 24/40 dents (énoncé).
- **Ajoutées (7)** : rectangles de 36 (cours), crible des nombres < 100 (cours), arbre de 420 (corrigé 2141), billes 47 = 6 × 7 + 5 (corrigé 2145), rectangles de 48 (corrigé 2146), frise des bus 12/18 min (corrigé 2196), dallage complété 7 × 5 dalles de 36 cm (corrigé 2155).
- `figures_livre.py` : 0 chevauchement texte/trait ; figures rectangles et dallage resserrées après capture téléphone.

## Contrôles

- `verif_235.py` : **103 contrôles** sympy/Python (décompositions, diviseurs, fractions, PGCD/PPCM, restes, listes), tout juste.
- `verifier_notion.py --navigateur` : OK, 0 problème. `controle_apercu.mjs` : captures produites (Chrome ne se ferme pas seul : processus arrêté par moi après les captures).
- Captures téléphone regardées : cours (partie I), exercice 2155 (étapes) ; corrections faites : tableau des critères réduit à 2 colonnes (colonne « Critère » écrasée), rectangles et dallage moins larges, question 1 de 2155 restructurée ; décomposition de 144 (2159) alignée sur trois lignes (formule trop longue pour un téléphone).

## Remarques pour l'orchestrateur

- PGCD / PPCM ne sont pas exigibles en 3e : ils sont écrits en toutes lettres (« plus grand diviseur commun », « plus petit multiple commun ») comme outils de résolution, sans notation exigée.
- Deux exercices passent du type « Problème » au type « Type brevet » (2158, 2159), conformément à la progression de la consigne de lot.
