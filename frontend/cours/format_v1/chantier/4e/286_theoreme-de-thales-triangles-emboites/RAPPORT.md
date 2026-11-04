# Notion 286 (4e) : Théorème de Thalès (triangles emboîtés)

**État : prêt** (claude-286, 2026-11-04). 21 exercices (aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée ; 3 exercices remplacés). Aucune écriture en base, aucun git.

Programme de 4e (cycle 4) : théorème de Thalès dans la configuration des triangles emboîtés (égalité des trois rapports, calcul de longueurs par quatrième proportionnelle), lien avec l'agrandissement et la réduction (longueurs, périmètre, angles conservés), problèmes concrets (ombre, hauteur d'un arbre, plan, distance inaccessible). La configuration papillon et la réciproque ne sont qu'**une mention** (« Pour aller plus loin », 3e). Les aires × k² (3e) ne sont pas abordées.

## Cours et fiche

- **Titres** inchangés : « Théorème de Thalès (triangles emboîtés) » et « Résumé : Théorème de Thalès (triangles emboîtés) ».
- **Cours 285 réécrit façon manuel** (la conversion avait la méthode et les calculs dans des encadrés `definition`, des « **1.** » en gras, un renvoi « onglet Fiches », et des exemples **identiques** aux exercices 3631 et 3636) : objectifs en liste ; I. définition, codage des parallèles (petite flèche), trois conditions, propriété « deux perpendiculaires à une même droite sont parallèles » ; II. théorème, « À retenir » sur les côtés correspondants (figure en couleur), mention 3e ; III. méthode en 4 étapes, **nouvel exemple** ($AM = 4$, $AB = 6$, $AC = 9$, $BC = 7{,}5$ → $AN = 6$, $MN = 5$) avec rédaction, tableau de proportionnalité, piège $MB$/$AB$, contrôles ; IV. réduction de coefficient $k$ et agrandissement de coefficient $1/k$, exemple, périmètre ; V. méthode des problèmes concrets, **nouvel exemple d'ombre** (bâton 1 m, ombres 0,8 m et 6 m → 7,5 m) ; VI. rédaction modèle ; « À retenir ».
- **Fiche 220 refaite** : théorème + figure des côtés appariés, méthode et exemple, tableau réduction / agrandissement + figure, 5 erreurs classiques, réflexe.

## Exercices (21)

- **Progression** dans l'ordre des Id : 7 Découverte (3629-3635), 7 Entraînement (3636-3642), 4 Problème (3643-3646), 3 **Type brevet** (3647-3649 ; il n'y en avait aucun). Titres « Type - Thalès - n. Sujet » → « Type - Sujet » (21 titres changés, sans le nom du chapitre).
- **Tous relus et réécrits** : questions numérotées ; corrigé avec méthode, étapes détaillées, **résultat encadré à chaque question (121/121)**, encadré « Erreur fréquente » dans **21/21** exercices, « À retenir » ou « Vérification » quand utile ; `Solution:` courte et cohérente. `\displaystyle`, `**À retenir :**` en gras et lignes `Image:` retirés ; étapes cassées par la conversion (phrase prise pour titre) reconstruites ; tableau de 3634 en vrai tableau (plus d'image).
- **Remplacés (même Id)** :
  - 3635 « Vrai ou faux » (mêmes données que 3633 : $AM$, $MB$, $AN$, $MN$ ; périmètre × k déjà dans 3632) → « Découverte - Choisir les bons rapports » : six égalités à juger (morceau $HF$, mauvais côté correspondant, rapports tous retournés, un seul retourné), puis $HK = 3{,}6$ cm et $EK = 4{,}2$ cm.
  - 3644 « Le panneau danger » (même déroulé que le toit 3639 : hauteur par Pythagore puis Thalès dans $ABH$) → « Problème - Une clôture sur un plan » : plan au 1/1 000, longueurs réelles, Thalès sur le plan, prix de la clôture, position de $M$ pour une clôture de 36 m (compétence « plan » du programme, absente).
  - 3641 « Corriger des erreurs » : l'erreur $MB$ au lieu de $AB$ (déjà dans 3633 et 3635) remplacée par deux erreurs nouvelles : $[MN]$ associé à $[AC]$ (Zoé) et produit en croix inversé repéré par $AN > AC$ (Sami) ; contrôle final des trois rapports.
- **Enrichis / restructurés** : 3629 (figure c : sommet commun $S$ en bas à gauche, côté parallèle oblique), 3630 ($VT$), 3632 (coefficient d'agrandissement 2,5), 3637 (périmètres en double retirés, périmètre de $MBCN$), 3639 (questions 3 et 4 fusionnées), 3647, 3648, 3649 passés en **Type brevet** en deux parties ; 3648 B3 ajoutée (longueur horizontale minimale 16 m pour une pente de 5 %), 3649 B2 (passerelle). 3636 : phrase ambiguë corrigée (« qui mesure 12 m » se rapportait à l'arbre).
- **Erreurs de maths** : aucune dans l'ancien contenu. `verif_286.py` : **417 contrôles sympy** (valeurs exactes, arrondis, équations, triangles constructibles) tous justes, dont les **coordonnées de 48 configurations dessinées** : $M$ sur $[AB]$, $N$ sur $[AC]$, $(MN) \parallel (BC)$, rapport dessiné = rapport de l'énoncé, côtés du grand triangle proportionnels aux vraies longueurs.

## Figures (style livre, `figures/figures.py`)

- **46 figures neuves pour 48 emplacements** ; les **46 images matplotlib en ligne sont toutes remplacées** (0 conservée ; 1 image non appelée, l'ancien tableau-image de 3634, supprimée à l'import).
- Conventions : petite flèche identique sur $[MN]$ et $[BC]$ = parallèles ; **énoncé** = données seules ; **corrigé** = côtés correspondants appariés en couleur (orange $AM$/$AB$, bleu $AN$/$AC$, violet $MN$/$BC$), petit triangle teinté en vert, **longueurs trouvées en vert**.
- Cours (4) : configuration, côtés appariés, réduction / agrandissement (×1,5 et ×2/3), ombre. Fiche (2, mêmes fichiers).
- Exercices : énoncé + corrigé pour les 21 ; schémas concrets sobres : ombre (3636), visée (3643), toit sur ses murs (3639), plan encadré (3644), étang (3645), rectangle inscrit (3646), escabeau avec cote de hauteur (3647), rampe et porte (échelle verticale exagérée, signalée) (3648), rivière vue de dessus (3649).
- `figures_livre.py` : **0 chevauchement texte / trait**, aucune tolérance (`TOLERE` vide) ; toutes ≤ 900 px. Chaque PNG regardé (planches) ; corrections : noms $M$/$N$ placés entre le côté et la cote, cotes écartées, longueur trouvée sur $[BC]$ écrite sous la flèche, flèches de parallélisme retirées des objets verticaux (confondues avec des vecteurs ; l'angle droit suffit), étiquettes « bâton », « Hugo », « arbre », « autre rive » déplacées hors des traits.

## Contrôles

- `verif_286.py` : 417 contrôles justes.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (48 nouvelles images, 0 conservée ; notes : 21 titres changés).
- `controle_apercu.mjs` avec captures : **aucun problème détecté** (cours, fiche, 21 exercices × 3 onglets, téléphone et ordinateur).
- **Captures téléphone regardées** (deux passes groupées) : cours en entier, fiche, énoncé 3629, étapes 3639, 3644, 3647. Corrections faites après ces vues : 21 calculs en chaîne (Pythagore, « … donc … ») réduits ou défilants → `aligned` sur plusieurs lignes ; 10 formules côte à côte (`\qquad`) et deux égalités de trois rapports « donc » séparées ; tableaux à 4 colonnes (cours, 3634) coupés → tableaux à 3 colonnes ; figure réduction / agrandissement resserrée (texte trop petit).
- Espaces insécables entre formule et unité : 328 dans les exercices, 17 dans le cours.
- Sauvegardes de travail : `sauvegardes/286_*_conversion_auto.txt`, `286_exercices_avant_decoupe.txt`, `286_exercices_avant_telephone.txt`.

## Remarques pour l'orchestrateur

- Aucune remarque d'outil ou de moteur. Détail utile pour les autres agents : `figures_livre.py` refuse une cote horizontale dont le texte est écrit en vert (`\textcolor` dans le nœud de cote), alors qu'il l'accepte sur une cote oblique ; contournement : texte vert écrit sous la flèche.
