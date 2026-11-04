# Notion 175 — Modéliser le hasard, calculer des probabilités (Seconde)

**État : prêt.** Contrôle du programme de Seconde (2019) : univers, événements,
réunion / intersection / contraire, loi de probabilité, $P(\overline{A})$,
$P(A\cup B)+P(A\cap B)=P(A)+P(B)$, dénombrement par arbres et tableaux (2 ou
3 épreuves), modèle a priori et modèle construit à partir de fréquences.
Aucune probabilité conditionnelle, aucun arbre pondéré (programme de Première).

## Texte
- **Cours** remis à niveau : objectifs, 6 parties ; ajout de l’événement
  certain/impossible, d’un exemple réunion/intersection/contraire, des propriétés
  $0\le P(A)\le 1$, de deux démonstrations (contraire, formule de la réunion),
  d’une méthode arbre, d’une méthode tableau (tableau des sommes de deux dés en
  tableau natif), de la méthode « au moins un », de trois épreuves et d’une partie
  VI « Modèle et réalité » (absente auparavant alors qu’elle est au programme).
  Notation unifiée $P$ et $\overline{A}$ (les exercices mélangeaient $A^c$ et $\overline{A}$).
- **Fiche** : 4 parties (vocabulaire, calcul, dénombrement, modèle et réalité),
  formules encadrées, erreurs classiques.
- **Exercices** — remplacements (Id conservés) :
  - 1999 : arbre **pondéré** sans remise (hors programme de Seconde) → arbre de
    **dénombrement** avec jetons numérotés (20 issues équiprobables) ; mêmes
    résultats, titre « Arbre de dénombrement ».
  - 2003 : jeu à arbre pondéré (produit des probabilités, hors programme) →
    problème « Trois lancers d’une pièce » (3 épreuves, contraire, réunion /
    intersection, modèle et fréquence observée).
  - 1993 Q5 : symboles perdus dans la conversion (ensemble vide affiché) →
    nouvelle question (jours de la semaine).
  - 1996 : loi sous forme de tableau, mention « axiomes de Kolmogorov » retirée,
    Q5 remplacée par « la roue est-elle équiprobable ? ».
  - 1994 : ajout des probabilités demandées par le titre (« Traduire et calculer »).
  - Tous : étapes complétées (méthode, étapes, résultat, erreurs fréquentes).
- **Ajouts** : `nouveau-1` (construire un modèle à partir de fréquences, dé truqué),
  `nouveau-2` (tableau croisé d’effectifs, réunion/intersection, erreur
  $P(F)+P(D)\gt 1$).
- Erreurs de maths : aucune erreur numérique dans la source ; tout est vérifié par
  `verif_probas.py` (96 contrôles, fractions exactes).

## Figures
- 3 images en ligne refaites (Venn, arbre, tableau : style matplotlib) ; le tableau
  des sommes devient un tableau natif (cours) ; la fiche reprend Venn et arbre.
- 8 figures produites (`figures/figures.py`) : Venn, contraire/incompatibles,
  arbre de deux lancers, arbre sans remise (20 issues), Venn des effectifs (1997),
  arbres de trois lancers (neutre et chemins verts), diagramme des fréquences.
- 0 image en ligne conservée.

## Contrôles
- `verifier_notion.py --navigateur` : OK (0 problème).
- `controle_apercu.mjs` : aucun problème détecté (téléphone + ordinateur).
- Captures téléphone regardées : cours, fiche, exercices 1999, 2003, nouveau-1,
  nouveau-2 ; corrigés après lecture : formules trop longues avec `\text{…}`
  (notées $E$, $U$), tableau de 7 colonnes transposé, points finaux isolés
  après une formule dans des lignes « méthode ».

## Remarques pour l’orchestrateur
- Rien à signaler sur les outils.

## Finition 2026-11-02

**État : prêt** (agent-finition-S4). 13 exercices (aucun ajout).

### Titres
- Cours et fiche : intitulé officiel, conservés.
- 13 titres « Type - Chapitre - Sujet » → « Type - Sujet » (types « Algorithmique » et « Maîtrise » remplacés), par exemple « Découverte - Réunion, intersection et contraire d’événements », « Entraînement - Deux dés différents dans un tableau à double entrée », « Problème - Trois lancers d’une pièce : probabilité de gagner ».

### Exercices
- Contenu déjà au programme et juste (vérifié) : aucune réécriture nécessaire ; `\displaystyle` retirés.

### Figures
- **Revérifiées une par une (8)** : `n1_frequences` refaite (graduations en police serif, légende noire démesurée, style différent des autres diagrammes → style des diagrammes de la notion 174, sans étiquettes posées sur la droite 1/6) ; les 4 arbres refaits (« 1er / 2e lancer » → exposants typographiques, arbre 1999 resserré). Conservées : `cours_venn`, `cours_contraire_incompatibles`, `e1997_venn`.
- **7 ajoutées** : cours `cours_au_moins_un6` (tableau des deux dés, 11 cases de « au moins un 6 ») ; 1994 (Venn de trois événements avec les 15 nombres placés), 1996 (roue à l’échelle), 1998 (deux tableaux à double entrée, cases favorables en vert : somme ≥ 8, au moins un 1), 2000 (axe des fréquences et du modèle), 3755 (Venn des effectifs).
- 9 exercices sur 13 ont une figure ; sans figure : 2002 (code), 1993, 1995, 2001 (vocabulaire, calculs immédiats).

### Contrôles
- `verif_probas.py` : **118 contrôles** (fractions exactes ; zones du Venn de 1994 recalculées ; code de 2002 exécuté avec graine fixe), tout juste.
- Téléphone : étiquettes des nouvelles figures en taille normale après relecture des captures.
- `figures_livre.py` : 0 erreur (aucun texte sur un trait, aucune figure > 1 100 px) ; chaque PNG regardé.
- `verifier_notion.py` : 0 problème de contenu ; seuls signalés : les Id 3754 et 3755, créés en base le 29/10 mais absents de `source_en_ligne/` (export du 29/10 antérieur à leur création) → **ré-export nécessaire avant import** (outil réservé à l’orchestrateur).
- Contrôle navigateur (`controle_apercu.mjs`, téléphone + ordinateur) : 82 vues, aucun problème détecté. Chrome restant parfois bloqué à la fermeture (défaut connu), seul mon processus a été arrêté et son verrou libéré.
- Captures téléphone regardées : cours, fiche et exercices à nouvelles figures.
