# Notion 90 — Équations différentielles (Terminale)

**État : prêt.** Aucun point en suspens.

## Texte

- **Cours** (id 92) restructuré : objectifs, prérequis, I à V ; preuves en encadrés `demonstration`
  (y' = ay au programme, y' = ay + b, y' = ay + f), méthode en 4 étapes, encadrés `attention`
  (signe de a, solution constante −b/a, condition initiale sur la solution complète),
  propriété y' = f (primitives), exemple y' = 2y − 4x complété par une condition initiale,
  modèles usuels (Newton, condensateur, croissance), exemple du café détaillé (calculs alignés).
- **Fiche** (id 38) : tableau des équations et solutions, méthode, modélisation (demi-vie ajoutée),
  4 erreurs classiques.
- **Exercices** (10) : tous réécrits au format du pilote (méthode / étapes / résultat, retenir,
  attention), virgules décimales `{,}`, unités insécables. Corrections de fond :
  - 1127 : t = 50 ln(9/7) ≈ **12,57** ans (en ligne : 12,59, faux à cause d’arrondis intermédiaires) ;
  - 1126 : demi-vie 50 ln 2 ≈ **34,66** min (en ligne : 34,65) ;
  - 1128 : u(0,02) ≈ **4,32** V (en ligne : 4,3235 ; valeur exacte 4,3233) ; condition initiale u(0) = 0
    absente de l’énoncé : ajoutée ; constante notée K (C désignait déjà la capacité) ;
  - 1129 : condition initiale absente (calcul fait avec « 1000 atomes » sorti de nulle part) → N(0) = N0
    et proportion restante 85,7 % ; la demi-vie n’est plus donnée dans l’énoncé avant d’être demandée ;
  - 1126, 1129, 1130, 1131 : « séparation des variables » (hors programme) remplacée par le théorème
    du cours ; remarque « pour aller plus loin » dans 1130 (titre conservé) ; logistique 1131 traitée
    par le changement de fonction z = 1/P (méthode du bac) ;
  - 1132 Q4 (« expliquer pourquoi la vérification est importante ») remplacée par une vraie
    vérification (z = e^{2x} + 1 n’est pas solution), comme dans le livre Terminale.
- Vérification : `verif_equations-differentielles.py` (sympy dsolve + valeurs) — tout est juste.

## Figures

- **2 images en ligne refaites** (style matplotlib, texte minuscule) : famille de solutions de
  y' = −0,5y + 2 (`cours_ayb`) et refroidissement du café (`cours_newton`), utilisées dans le cours et la fiche.
- **6 ajoutées** : solutions de y' = 0,5y (`cours_ay`) ; corrigés de 1128 (charge RC), 1126 (demi-vie),
  1124 (mélange), 1125 (Newton), 1131 (courbe logistique), réponses en vert.
- 0 conservée, 0 retirée sans remplacement. Toutes ≤ 900 px, aucun texte sur un trait (contrôle OK).

## Contrôles

- `verifier_notion.py --navigateur` : **OK, 0 problème**.
- Vues regardées (captures/) : cours complet en téléphone, fiche, exercices 1132, 1128 (énoncé + étapes) et 1131.
  Le tableau à 3 colonnes des modèles défilait sur téléphone : remplacé par une liste.

## Remarques pour l’orchestrateur

- Exercice 1124 : concentration 0,5 kg/L conservée (comme dans le livre), physiquement au-delà de la
  saturation du sel (≈ 0,36 kg/L) ; sans incidence mathématique.

## Finition 2026-11-02

**État : prêt** (passe de finition, agent finition-T4).

### Titres
- Cours « Équations différentielles » et fiche « Résumé : Équations différentielles » : inchangés (intitulé du programme ; les primitives sont la notion 88).
- 10 titres d'exercices sans « Équations Différentielles » répété (ex. « Découverte - Vérifier qu'une fonction est solution », « Entraînement - Charge d'un condensateur dans un circuit RC ») ; 1130 « Séparation des variables (Température) », titre devenu faux depuis la réécriture, → « Entraînement - Refroidissement d'un objet dans une pièce à 25 °C ».

### Exercices
- **2 ajoutés** (10 → 12), sur des compétences jusque-là non travaillées : `nouveau-1` « Découverte - Famille de solutions et solution passant par un point » (y′ = −0,5y + 1 : solution constante, famille, condition en x₀ = 0 et en x₀ = 2, limite) ; `nouveau-2` « Type examen - Solution particulière et étude d'une fonction » (y′ + y = 2e^(−x), solution particulière 2xe^(−x), équivalence avec (E₀), f(x) = (2x+1)e^(−x), tableau de variations natif, limite).
- Les 10 exercices existants relus : justes, au programme ; aucun à réécrire.
- Cours IV : remarque « Lecture de la figure » (solution particulière = droite, solutions qui s'en rapprochent en −∞).

### Figures (17 fichiers, 20 emplacements)
- **Revérifiées à l'œil : les 8 existantes** ; **1 retouchée** : `ex_rc` (étiquette u(5τ) ≈ 4,97 éloignée de son point → placée à côté).
- **9 ajoutées** : cours `cours_ayf` (famille de y′ = 2y − 4x et solution particulière affine, légende)  ; exercices `ex_verif` (1132, famille et solution constante y = −2), `ex_population` (1123), `ex_immigration` (1127), `ex_uranium` (1129, proportion en milliards d'années), `ex_temperature` (1130), `en1_famille` (énoncé : famille + points A, B, sans la réponse) et `en1_famille_corr` (corrigé : f, g et y = 2 en vert), `en2_etude`.
- Fiche : `cours_ay` (famille et solution passant par un point) ajoutée en I.
- `figures_livre.py` : 17/17, 0 erreur, 0 avertissement.

### Contrôles
- `verif_equations-differentielles.py` : tout est juste (122 contrôles, dont chaque courbe tracée vérifiée comme solution).
- Formules au téléphone : 4 formules qui défilaient (1126, 1127, 1131, nouveau-2) et 6 très réduites redécoupées → 0 formule qui défile.
- `verifier_notion.py --navigateur` : OK, 0 problème.
- Captures téléphone regardées : cours partie IV (figure de la solution particulière), exercice nouveau-1 (étapes) ; une ponctuation isolée corrigée dans nouveau-1.
- controle_apercu.mjs (captures) bloqué à la fermeture de Chrome (défaut connu) : seul mon processus a été arrêté et son verrou libéré.
