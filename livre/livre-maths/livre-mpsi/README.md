# OptiTAB — Mathématiques MPSI (cours et exercices corrigés)

Livre LuaLaTeX bâti sur la charte OptiTAB (`optitab-livre.sty`, adaptée du
livre de Terminale). **Référence officielle** : programme de mathématiques
des classes préparatoires MPSI et MP2I, arrêté du 5 janvier 2021, BO spécial
n°1 du 11 février 2021 — copie de l'annexe dans
`recherche/programme-maths-mpsi-mp2i-2021.pdf`.

## Structure du livre

- 2 parties = les deux semestres officiels, 20 chapitres au total
  (voir `plan.tex`, qui pilote sommaire, tableau de bord et liste des corrigés).
- Chaque chapitre : ouverture (objectifs + prérequis) → **L'essentiel**
  (synthèse de cours étoffée : définitions, théorèmes, démonstrations
  modèles, méthodes, pièges, schémas) → **25 exercices** en quatre rubriques :
  - *Applications* (8, niveau 1) — vérifier le cours ;
  - *Entraînement* (10, niveau 2) — méthodes de colles et de DS ;
  - *Approfondissement* (6, niveau 3) — esprit des écrits de concours
    (CCINP, Mines-Ponts, Centrale-Supélec, X-ENS) ;
  - *Défi* (1, environnement `defi`) — problème de synthèse en parties A/B/C
    vers un résultat célèbre (`chapitres/defis/defi-NN.tex`, corrigé dans
    `corriges/defis/cor-defi-NN.tex`).
- Partie **Évaluations** après le chapitre 20 (`evaluations/`) : page
  « Couverture du programme » (`\planEvaluations`, une ligne par sujet, une
  colonne par chapitre), puis 6 DS, 4 DM, 2 examens (concours blancs) et
  4 sujets type concours (CCINP, Mines-Ponts, Centrale-Supélec avec Python,
  X-ENS). Énoncés `ds-0N`, `dm-0N`, `ex-0N`, `cc-0N` ; corrigés `cor-*.tex`
  (barème par question avec `\pts`, figures insécables avec leur légende),
  placés après les corrigés des chapitres. Macros : `\sujetEval`,
  `\sectionEval`, `\exoEval`, `\corrigeSujetEval`, `\corrigeEval`,
  `\enParties` (pastilles A, B, C… pour les problèmes), `\numero`.
- Corrigés détaillés en fin d'ouvrage, dans le style du livre de Première :
  pleine largeur (pas de colonnes), chaque corrigé dans un bloc insécable
  `blocLivre{cor-N-M}` (erreur de compilation s'il dépasse une page), une
  ligne `\demarche{...}` de stratégie sous chaque titre, étiquettes
  « Méthode », résultats surlignés, schémas quand ils éclairent la solution.

## Compilation

Depuis ce dossier (trois passes, la première crée `build/`) :

```
"$LOCALAPPDATA/Programs/MiKTeX/miktex/bin/x64/lualatex.exe" -synctex=1 \
  -interaction=nonstopmode -file-line-error -aux-directory=build main.tex
```

## Conventions (reprises des autres livres)

- Le nombre d'exercices de chaque chapitre dans `plan.tex` doit correspondre
  au fichier du chapitre.
- Tout résultat calculable est vérifié par un script Python
  (`verifications/chapitre_NN.py`) **avant** d'être imprimé.
- Après toute modification : recompiler puis inspecter les pages rendues
  (pdftoppm) — débordements, lignes veuves, pages quasi vides.
- Les versos laissés libres deviennent automatiquement des pages « Notes ».

## État

- [x] Template, couverture, pages liminaires, sommaire, tableau de bord
- [x] Chapitre 01 — Raisonnement et vocabulaire ensembliste (24 exercices + corrigés)
- [x] Chapitre 02 — Calcul algébrique et trigonométrie (24 exercices + corrigés)
- [x] Chapitre 03 — Nombres complexes (24 exercices + corrigés)
- [x] Chapitre 04 — Techniques de calcul différentiel et intégral (24 exercices + corrigés)
- [x] Chapitre 05 — Nombres réels et suites numériques (24 exercices + corrigés)
- [x] Chapitre 06 — Limites, continuité, dérivabilité, convexité (24 exercices + corrigés)
- [x] Chapitre 07 — Arithmétique des entiers relatifs (24 exercices + corrigés)
- [x] Chapitre 08 — Structures algébriques usuelles (24 exercices + corrigés)
- [x] Chapitre 09 — Calcul matriciel et systèmes linéaires (24 exercices + corrigés)
- [x] Chapitre 10 — Polynômes et fractions rationnelles (24 exercices + corrigés)
- [x] Chapitre 11 — Analyse asymptotique (24 exercices + corrigés)
- [x] Chapitre 12 — Espaces vectoriels et applications linéaires (24 exercices + corrigés)
- [x] Chapitre 13 — Matrices (24 exercices + corrigés)
- [x] Chapitre 14 — Groupe symétrique et déterminants (24 exercices + corrigés)
- [x] Chapitre 15 — Intégration (24 exercices + corrigés)
- [x] Chapitre 16 — Dénombrement (24 exercices + corrigés)
- [x] Chapitre 17 — Probabilités sur un univers fini (24 exercices + corrigés)
- [x] Chapitre 18 — Espaces préhilbertiens réels (24 exercices + corrigés)
- [x] Chapitre 19 — Procédés sommatoires discrets (24 exercices + corrigés)
- [x] Chapitre 20 — Fonctions de deux variables (24 exercices + corrigés)
- [x] Un défi par chapitre (20 défis + corrigés, `verifications/defis_*.py`)
- [x] Partie Évaluations : DS1–DS6, DM1–DM4, EX1–EX2, C1–C4 + corrigés
      (`verifications/eval_ds.py`, `eval_dm.py`, `eval_ex.py`, `eval_cc.py`,
      figure générée par `fig_folium.py`)
- [ ] Page ISBN / éditeur (décision du propriétaire)
