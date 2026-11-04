# Notion 102 — Nombres complexes (Terminale, option Mathématiques expertes)

**État : prêt.** Cours 108, fiche 47 et 11 exercices au format v1, remis à niveau
complète (cours ancien), programme officiel de Mathématiques expertes.

## Texte

- **Cours réécrit de zéro** (6 parties + erreurs fréquentes) : forme algébrique,
  binôme, conjugué/inverse, équations `az = b` et avec `z̄` ; plan complexe
  (affixes, module, 𝕌, cercles/médiatrices) ; arguments et forme trigonométrique ;
  formules d'addition, exponentielle imaginaire, forme exponentielle, Moivre, Euler
  (linéarisation) ; équations polynomiales ; géométrie (quotient `(c−a)/(b−a)`) et
  racines n-ièmes de l'unité.
- **Démonstrations du programme rédigées en entier** : conjugué d'un produit, d'une
  puissance, d'un inverse ; `|z|² = z z̄`, module d'un produit ; formules d'addition
  (produit scalaire) ; relation fonctionnelle ; Moivre, Euler ; factorisation de
  `zⁿ − aⁿ`, de `P` par `z − a` ; au plus n racines ; détermination de 𝕌n ;
  binôme ; second degré (Δ < 0) ; module/argument de `(c−a)/(b−a)`.
- **Corrections de fond** (ancienne version) : `√−16 = 4i` (écriture interdite)
  supprimé partout (cours, exercice 958) ; `arctan` (hors programme) supprimé
  (exercices 956, 962, fiche) ; fiche : barycentre (hors programme) retiré,
  « arg(z − a) = θ [π] → demi-droite » faux (c'est une droite privée d'un point)
  retiré, notation `Im` corrigée ; démonstrations incomplètes (« on obtient… »)
  complétées ; conversions cassées (« x = −1 0 », sous-questions a)/b) mal placées
  dans les solutions) réparées.
- **Exercice 962 (Angles orientés)** : données modifiées, `z_C = −1 + i` → `z_C = −i`.
  L'ancien énoncé donnait un argument `−arctan(1/3)` (hors programme) et un triangle
  « quelconque » ; désormais quotient `−i = e^{−iπ/2}`, triangle rectangle isocèle
  en A (question 5 inchangée, même réponse). Titre, Id, difficulté inchangés.
- Exercice 958 : questions 4 et 5 portent sur les trois équations (tableau natif).
  Exercice 961 : question 4 « à l'aide de la formule de Moivre » (c'est ce qui est
  utilisé). Exercice 1133 : sous-questions et solution restructurées.
- Fiche réécrite (≈ 2 écrans) : formules clés, tableau des trois formes, tableau
  géométrie, 5 pièges.
- **Vérification** : `verif_nombres-complexes.py` (sympy) — 123 contrôles, tous justes
  (chaque calcul du cours, de la fiche et des 11 exercices).

## Figures

- 25 figures TikZ style livres (`figures/figures.py`), contrôle « aucun texte sur
  un trait » passé, largeur ≤ 900 px.
- **9 images en ligne refaites/remplacées** (toutes de style matplotlib) : cours
  positions 1 à 7 (dont doublons 2/3 et 4/5), exercice 1133 et exercice 959.
  Les « quadrants » (images 2/3) ne sont plus utilisés : remplacés par la figure
  module/argument et la méthode cos/sin.
- **Ajoutées** : cours 8 figures (affixe et conjugué, lieux, module-argument,
  formules d'addition, produit, racines d'un polynôme, quotient, racines de
  l'unité) ; fiche 1 ; exercices 963 (×4), 958, 961, 956 (×2), 960 (×3),
  962 (×2), 959 (×2), 1133 (×2), avec les éléments de réponse en vert.
- Conservées : 0. Retirées sans remplacement : 0.

## Contrôles

- `verifier_notion.py --navigateur` : 0 problème ; `controle_apercu.mjs` : aucun problème.
- Captures téléphone regardées : formules centrées longues coupées en chaînes
  `aligned` (une égalité par ligne) pour qu'aucune ne soit tronquée ni trop réduite.

## Remarques pour l'orchestrateur

- Outil `figures_livre.py` : dans une figure en `x=0.7cm` par exemple, `grid`
  utilise un pas de 1 cm par défaut (grille décalée des graduations) ; j'ai ajouté
  `step=1` dans mon style `grille`. À signaler aux autres notions qui changent
  d'unité.
- Une compilation a échoué une fois par « TeX capacity exceeded » (compilations
  simultanées) ; relancée sans modification, elle passe.

## Finition 2026-11-02

**État : prêt** (agent-finition-T8). 11 exercices, tous avec au moins une figure.

### Figures
- **Revérifiées** : les 25 existantes (détecteur + chaque PNG regardé ; valeurs conformes aux énoncés : points, modules, arguments, racines de l'unité).
- **Refaites (2)** : `second_degre_sol` (graduation « 1 » collée au pointillé vertical $x = 1$, décalée) et `transfo_cercle_med` (graduation « 1 » presque touchée par la droite $\Delta$, passée au-dessus de l'axe).
- **Ajoutées (5)**, dans les corrigés, éléments de réponse en vert :
  - 955 : `ex955_module` (module = distance $OM$, $|z_1| = 5$, $|z_2| = \sqrt{5}$) et `ex955_conjugues` (conjugués symétriques par rapport à l'axe réel) ;
  - 954 : `ex954_somme` (règle du parallélogramme, $z_1 + z_2 = 1 + 7\mathrm{i}$) et `ex954_parties` (parties réelle et imaginaire, $z_4$ imaginaire pur) ;
  - 957 : `ex957_puissances` ($1 + \mathrm{i}$, $2\mathrm{i}$, $-2 + 2\mathrm{i}$, $-4$ : module $\times\sqrt{2}$, argument $+\frac{\pi}{4}$).
- Chaque figure ajoutée est introduite par un encadré « Lecture géométrique ». 0 retirée.

### Titres
Les 11 titres sans majuscules abusives, au format « Type - Sujet » ; le « DS- » de 1133 devient « Type examen - Transformation du plan complexe » (l'option n'a pas d'épreuve de bac). Cours et fiche : « Nombres complexes » / « Résumé : Nombres complexes » (le titre en base reste « Nombres Complexes » : à renommer si souhaité, l'importeur ne change pas les titres de cours).

### Contrôles
- `verif_nombres-complexes.py` : 144 vérifications, toutes justes (+ 21 pour les valeurs des nouvelles figures).
- `figures_livre.py` : 30/30, 0 erreur, 0 avertissement.
- `verifier_notion.py --navigateur` : OK, 0 problème. Aucune chaîne `aligned` cassée (contrôle des parenthèses ligne à ligne sur cours, fiche, exercices).
