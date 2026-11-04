# Notion 288 (4e) : Translations, agrandissements et réductions

**État : prêt** (claude-288, 2026-11-04). 21 exercices : aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée, 3 exercices remplacés. Aucune écriture en base, aucun git.

Programme de 4e (cycle 4) couvert : translation (construire l'image d'un point ou d'une figure sur quadrillage et à la règle et au compas), propriétés conservées, parallélogramme associé ; rappels des symétries axiale et centrale pour les distinguer ; frises et pavages par translations ; enchaînement de deux translations ; agrandissement et réduction de coefficient $k$ (longueurs × $k$, angles conservés, proportionnalité), échelle d'un plan ou d'une maquette ; effet sur les aires (× $k^2$) **en découverte** seulement. Rotation et homothétie (3e) ne sont pas abordées.

## Cours 287 et fiche 222

- **Titres** inchangés : « Translations, agrandissements et réductions » et « Résumé : Translations, agrandissements et réductions ».
- **Cours réécrit façon manuel.** La conversion avait des puces « • », un objectif en pavé, une seule figure de translation, des remarques qui contenaient la matière, et un renvoi « onglet Fiches ». Nouveau plan :
  - objectifs et prérequis ;
  - I. La translation (définition : direction, sens, longueur ; méthode sur quadrillage ; erreur du point de départ) ;
  - II. Translation et parallélogramme (propriété, ordre des lettres, construction au compas avec figure, cas aplati) ;
  - III. Propriétés conservées et comparaison avec les symétries (figure à trois panneaux, liste, méthode pour reconnaître) ;
  - IV. Frises et pavages (figures neuves, $n - 1$ décalages, enchaînement de deux translations) ;
  - V. Agrandissement et réduction (définition, propriété, méthode pour trouver $k$, exemple, erreurs fréquentes) ;
  - VI. Échelle (définition, exemple, piège des unités) ;
  - VII. Découverte de l'effet sur les aires ($k^2$, renvoi à la 3e) ;
  - « À retenir ».
- **Fiche refaite** : translation et parallélogramme, ce qu'elle conserve (tableau des trois transformations), frises et pavages, agrandissement et réduction (tableau longueurs / angles / aires, échelle), 6 erreurs classiques, réflexe.

## Exercices (21)

- **Progression** dans l'ordre des Id : 7 Découverte (3671-3677), 7 Entraînement (3678-3684), 5 Problème (3685-3689), 2 **Type brevet** (3690-3691 ; il n'y en avait aucun). Les titres « Type - Translations - n. Sujet », qui répétaient le nom du chapitre, deviennent « Type - Sujet » (21).
- **Tous relus et réécrits.** Chaque énoncé a des questions numérotées. Chaque corrigé contient :
  - une méthode (21/21) ;
  - des étapes détaillées ;
  - un résultat encadré à chaque question ;
  - un encadré « Erreur fréquente » (21/21) ;
  - une `Solution:` courte et cohérente.

  Ont été corrigés : les `\displaystyle`, les lignes `Image:`, les « **Erreur fréquente :** » en gras hors encadré, et les étapes cassées par la conversion (formule prise pour titre, étape vide).
- **Remplacés (3)** :
  - 3679 « Translation et coordonnées » (doublon de 3672 et 3686, repère) → « Entraînement - Translation ou symétrie ? ». On construit l'image d'un drapeau par une symétrie axiale, une symétrie centrale et une translation, puis on compare les orientations et les aires. C'est le rappel des symétries demandé.
  - 3683 « La maquette de voiture » (doublon des échelles 3681 et 3689) → « Entraînement - Agrandir et réduire sur quadrillage ». On construit une maison réduite ($k = 0{,}5$) et agrandie ($k = 1{,}5$), avec les côtés obliques, l'angle droit conservé, et des aires × 0,25 et × 2,25.
  - 3684 « Agrandir un triangle » (doublon de 3676) → « Entraînement - Compléter un agrandissement ». Il comprend un tableau de proportionnalité et le test des trois quotients ; le triangle $GHI$ est un piège (deux quotients égaux, pas le troisième) et le triangle $JKL$ est une vraie réduction.
- **Réécrits en partie** :
  - 3671 : questions guidées taille / orientation, puis identification des quatre transformations.
  - 3673 : nature de $ABB'A'$.
  - 3677 : affirmation sur l'aire du carré, à la place d'une affirmation redondante, et suppression de la figure inutile.
  - 3678 : motif 20 et frise de 1 m, à la place d'une question triviale.
  - 3681 : aire du plan × 2 500 = 50², à la place de « 1/50 = 0,02 ».
  - 3685 : translation vers un carreau lointain (5) par enchaînement.
  - 3687 : logo de 75 cm² ⇒ $k = \sqrt{6{,}25} = 2{,}5$, à la place d'une prévision redondante.
  - 3688 : aire du plan × 200², et la pelouse regroupée avec les graines.
  - 3690 et 3691 passés en « Type brevet », avec des rédactions complètes.
- **Erreurs de maths** : aucune dans les résultats en ligne. Un défaut a été corrigé : en 3672 et 3679, la translation était faite par des calculs de coordonnées sans figure ; c'est maintenant une construction sur quadrillage.
- `verif_288.py` : **249 contrôles sympy, tous justes**. Il vérifie chaque calcul du cours et des 21 corrigés, les arrondis, et relit `DONNEES` dans `figures/figures.py` : chaque image de figure est recalculée par la vraie transformation (translation, symétrie, agrandissement), ainsi que les longueurs, les aires, les angles droits et les alignements.

## Figures (style livre, `figures/figures.py`)

- **45 figures neuves** pour **47 positions**. Les **41 images matplotlib en ligne sont toutes remplacées** (0 conservée). Celle de 3677 n'est plus appelée et sera supprimée à l'import.
  - Cours (8) : translation sur quadrillage, parallélogramme codé, construction au compas, trois transformations comparées, frise, pavage de chevrons (deux translations), réduction / départ / agrandissement, aires × 4 et × 9. Fiche : 2 figures du cours.
  - Énoncés : la figure de départ et la flèche (ou le point image donné), **sans l'image**.
  - Corrigés : **image en vert** avec les traits de construction (flèches identiques, codages, arcs de compas, angle droit et milieu pour les symétries, diagonales alignées pour les formats, rayon lumineux et ombre de 40 cm).
- `figures_livre.py` : 0 texte sur un trait, aucune tolérance (`TOLERE` vide). Les seuls avertissements restants viennent des cotes à fond blanc (usage normal) et de la frise, large de 902 px. Toutes les figures sont regardées sur les planches.
- Corrections faites après relecture :
  - longueurs placées à l'extérieur des triangles (3676, 3680, 3684, cours) ;
  - graduations du repère déplacées (une flèche passait sur « −2 ») ;
  - numéros des carreaux de 3685 éloignés des flèches ;
  - étiquettes « 2 2 » du coin rentrant du logo écartées ;
  - cote 330 m de la tour déplacée (elle traversait « 2e étage ») ;
  - lettres collées « FE' » de 3684 séparées ;
  - figure de l'agrandissement du cours passée sur deux rangées, plus lisible sur téléphone ;
  - légendes en texte (« coefficient 2, aire × 4 ») au lieu de formules minuscules.

## Contrôles

- `verifier_notion.py --navigateur` : **OK, 0 problème** (47 nouvelles figures, 0 image en ligne conservée ; notes : 21 titres changés, voulu). Il a été relancé, sans navigateur, après les corrections téléphone : OK.
- `controle_apercu.mjs` avec captures, deux passes : **130 vues sur 130 sans défaut** (cours, fiche, 21 exercices × 3 onglets, téléphone et ordinateur). Chrome restait bloqué à la fermeture une fois toutes les vues écrites (cas connu). Seuls mes propres processus ont été arrêtés : `lualatex` 25144 (bloqué au démarrage), `node` 17912 puis 22740. Mon verrou `chrome_1.lock` a été libéré.
- **Captures téléphone regardées** en deux passes groupées : le cours en entier, la fiche, l'énoncé de 3671, les étapes de 3676, 3679, 3684, 3686, 3690 et 3691. Corrections faites après la première passe :
  - formules doubles réduites ou coupées (« … donc … », deux calculs côte à côte) : 15 découpées, une par ligne ou en `aligned` (3686 Pythagore, 3690, 3691 Thalès, 3676, 3680, 3681, 3683…) ;
  - tableau à trois colonnes du cours III, illisible sur téléphone, transformé en liste ;
  - trois figures du cours rendues plus étroites.
- Sauvegardes : `sauvegardes/288_*_conversion_auto.txt`, `288_exercices_avant_telephone.txt`, `288_cours_avant_telephone.txt`.

## Remarques pour l'orchestrateur

- Titres du cours et de la fiche inchangés ; les 21 titres d'exercices changent.
- Une compilation `lualatex` est restée bloquée au démarrage, sans écrire de journal (probablement une contention avec les autres agents). Je l'ai arrêtée puis la figure a été recompilée. Aucun défaut d'outil durable.
