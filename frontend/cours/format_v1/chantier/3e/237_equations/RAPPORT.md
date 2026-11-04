# Notion 237 (3e) : Équations

**État : prêt** (agent-3e-C4, 2026-11-03).

Programme du cycle 4 (attendus de fin de 3e) : tester une solution, équations du premier degré (avec parenthèses, fractions, cas sans solution ou avec une infinité de solutions), équation produit nul, équation $x^2 = a$, mise en équation d'un problème, lecture graphique des solutions.

## Texte
- **Titres** : cours « Équations et mise en équation » → « Équations » ; fiche → « Résumé : Équations » (à appliquer avec `titres_docs.py`).
- **Cours 232** : réécrit. I. Équation et solution (tester un nombre) ; II. Règles de la balance (figure), méthode en 4 étapes, deux exemples en `aligned` (un exemple était rangé dans un encadré `definition`), solution non entière, erreurs fréquentes ; III. Produit nul (méthode, exemple, lecture graphique en figure, piège $x^2 = 5x$) et $x^2 = a$ (exemple $\sqrt{12}$ en valeur exacte, lien avec $a^2 - b^2$) ; IV. Mise en équation (méthode en 5 étapes, exemple rédigé des deux tarifs) ; V. Résolution graphique (figure des deux droites).
- **Fiche 152** : réécrite (objectifs inutiles retirés, tableau $x^2 = a$, tableau de traductions, 5 erreurs classiques, réflexe brevet).
- **Exercices** : les 21 réécrits au format complet (méthode, étapes, résultat, erreur fréquente ou à retenir, solution). Progression : 7 Découverte, 7 Entraînement, 5 Problème, 2 Type brevet. Titres « Type - Sujet » sans le nom du chapitre.
  - **Remplacés** (même Id) :
    - 2201 « Des opérations inverses » (doublon de 2202) → « Découverte - La balance en équilibre » (figure de balance, $4x + 3 = x + 12$) ; les opérations inverses sont regroupées dans 2202 ;
    - 2213 « Choisir la méthode » (doublon de 2204, parenthèses) → « Entraînement - Choisir la bonne méthode » (premier degré, produit nul, $x^2 = a$, $(2x + 1)^2 = 9$) ;
    - 2214 « Préparer un produit nul » (doublon de 2210/2211) → « Entraînement - Lecture graphique et produit nul » (courbe de $(x + 1)(x - 3)$, $f(x) = 0$ et $f(x) = -3$) ;
    - 2217 « Retrouver le nombre initial » → « Type brevet - Deux programmes de calcul » ($x + 12$ et $(x + 1)^2 - x^2 = 2x + 1$) ;
    - 2220 « Les deux tarifs » → « Type brevet - Deux tarifs de cinéma » (lecture graphique + calcul).
  - **Correction** : 2211 donnait $\pm 2\sqrt{3}$ (simplification de racine, pas un attendu de 3e) → $\pm\sqrt{12} \approx \pm 3{,}46$. Aucune erreur de calcul dans les autres résultats en ligne.
  - 2206 : question 5 remplacée (test de $-1$ dans une équation du second degré, piège $(-1)^2$).
- `verif_237.py` : **119 contrôles sympy OK** (chaque équation, chaque vérification, chaque contre-exemple des erreurs fréquentes).

## Figures
- **19 figures neuves** (17 fichiers) ; les 4 images en ligne (matplotlib : balance du cours et de la fiche, rectangle 2216, aires 2219) sont remplacées ; 0 conservée.
  - Cours (3) : balance $3x + 2 = x + 8$ puis $2x = 6$, courbe de $(x - 2)(x + 3)$ et ses racines, deux droites de tarifs. Fiche (2) : balance, courbe.
  - Exercices, énoncé **et** corrigé en vert : 2201 (balance), 2214 (courbe), 2215 (schéma en barre des billets), 2216 (rectangle), 2219 (carré et rectangle), 2220 (graphique des tarifs), 2221 (frise des âges).
- Détecteur texte/trait : 0 erreur ; seules alertes : cotes à fond blanc (normal). Toutes ≤ 900 px. Chaque PNG regardé.

## Contrôles
- `verifier_notion.py --navigateur` : **OK, 0 problème**.
- `controle_apercu.mjs` avec captures : 0 débordement, 0 erreur de formule, 0 image manquante.
- Vues regardées sur téléphone : cours (parties I à V), fiche, exercices 2208, 2214 (étapes). Corrections faites après ces vues : double distributivité de 2214 (ligne réduite) découpée ; balance rétrécie (texte trop petit sur téléphone).

## Remarques pour l'orchestrateur
- Appliquer les nouveaux titres du cours et de la fiche (`titres_docs.py`).
