# Notion 179 — Probabilités conditionnelles et indépendance (Terminale)

Prêt (agent interrompu à la fin de son travail, clôture par l'orchestrateur le 2026-10-27).

- Texte : cours 166, fiche 76 et 11 exercices au format v1 ; tableaux à cellules fusionnées
  de la source (arbres dessinés en tableau HTML) remplacés par de vrais arbres pondérés.
- Calculs : `verif_probas.py` (fractions exactes) → « TOUT EST JUSTE ».
- Figures : 33 figures style livre (arbres pondérés, partition de l'univers), 40 emplacements
  `[IMAGE_N]` ; détecteur texte/trait : 33/33 sans erreur ni avertissement ; aucune image en
  ligne conservée.
- Contrôles : verifier_notion.py --navigateur → OK (téléphone et ordinateur).


## Finition 2026-11-02

**État : prêt** (passe de finition, agent finition-T6). Sauvegardes : `sauvegardes/*_avant_finition_20261102.*`.

### Doublon avec la Première (notion 1ère 183)
- Exercices : textes tous différents (similarité ≤ 0,22 avec ceux de 183) : pas de doublon d’exercices.
- Cours : les parties I à III recouvrent le programme de Première (183, plus détaillée). Elles sont gardées comme **rappels**, annoncés par un encadré « Place du chapitre ». La partie IV porte la **nouveauté de Terminale**, enrichie : univers produit Ω₁ × … × Ωₙ, épreuves indépendantes (modélisation par le produit), exemple de **tableau croisé** urne × roue, encadré « Lien avec la loi binomiale » (penalties : B(3 ; 0,6), P(X = 2) = 0,432) et mise en garde « indépendantes mais pas identiques ». Fiche : 2 points ajoutés (univers produit, schéma de Bernoulli).
- À décider par le propriétaire : garder les rappels I–III (choix actuel) ou les alléger au profit de la notion de Première.

### Titres
- 11 titres sans « Probabilités Conditionnelles - » ni majuscules abusives (ex. « Entraînement - Indépendance ou incompatibilité », « Problème - Remonter de l’effet à la cause », « Problème - Deux tirages avec remise dans un sac de jetons » — l’ancien titre annonçait un arbre absent). 1279 (difficulté « easy ») : « Problème » → « Découverte - Construire des arbres pondérés ».

### Exercices
- **1 ajouté** (11 → 12) : `nouveau-1` « Type examen - Feux tricolores : épreuves indépendantes et loi binomiale » (trois épreuves indépendantes **non identiques**, arbre à compléter, P = 0,21 ; 0,44 ; 0,94, pourquoi N n’est pas binomiale ; puis 4 feux identiques : B(4 ; 0,6), P(X = 2) = 0,3456, P(X ≥ 1) = 0,9744).
- 1274 Q3 réécrite (doublon de 1281 Q4) : problème inverse, P(B) = 0,4 connaissant P(A ∪ B) = 0,58 et l’indépendance.
- **Tableaux croisés** (natifs) ajoutés dans les corrigés : 1273 Q1, 1274 Q1 (P_A(B) = P(B)), 1280 Q3 (effectifs filles/garçons × sport).

### Figures (39 fichiers, 46 emplacements)
- **33 existantes revérifiées** : recompilées (33/33, 0 avertissement), chaque valeur d’arbre recalculée sur les planches : toutes justes. **1 refaite** : `e1279_q1` (arbre complété : toutes les probabilités complétées en vert).
- **6 ajoutées** : `e1279_q1_enonce` (arbre à compléter dans l’énoncé), `n1_feux_enonce` / `n1_feux_corrige` (arbre à compléter puis complet en vert, chemins à 2 verts en trait épais), `e1273_des` (36 sommes, B coloré, A ∩ B en vert), `e1278_grille` (16 sommes, S et E), `e1274_de` (A et B incompatibles).
- Les 12 exercices ont une figure (3 sur 11 n’en avaient pas).

### Contrôles
- `verif_probas.py` : **TOUT EST JUSTE** (section « FINITION » en fractions exactes + sympy pour l’équation de 1274 Q3 ; tableaux croisés, cases colorées par énumération, 8 feuilles de l’arbre des feux).
- `verifier_notion.py --navigateur` : **OK, 0 problème** ; `controle_apercu.mjs` : aucun problème. Captures téléphone regardées (cours IV, nouveau-1) : arbre des feux resserré (858 → 773 px) pour rester lisible.

### Remarques pour l’orchestrateur
- 1276 garde une ancienne ligne `Image: prob_total_q1.png,…` dans son en-tête (inoffensive pour le vérificateur).
- 1275 et 1276 reprennent volontairement les mêmes quatre situations (probabilités totales puis inversion).
