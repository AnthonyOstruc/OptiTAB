# Notion 246 (3e) : Transformations du plan

**État : prêt** (agent-3e-C8-246, 2026-11-03).

Programme du cycle 4, attendus de fin de 3e : symétrie axiale, symétrie centrale, translation, rotation, homothétie (rapport positif ou négatif) et propriétés conservées ; reconnaître la transformation qui envoie une figure sur une autre ; frises, pavages, rosaces ; agrandissement-réduction (longueurs × k, aires × k², volumes × k³).

## Texte
- **Cours 241** : réécrit de zéro, titre = intitulé de la notion (« Transformations du plan », au lieu de « Transformations et homothéties »). L'ancien cours mettait les quatre isométries dans un seul encadré `definition`, s'appuyait sur des formules de coordonnées hors programme ($(x ; y) \to (-y ; x)$…) et ne parlait pas des pavages ni de la reconnaissance d'une transformation.
  - I. Transformer une figure ; II. Symétrie axiale ; III. Symétrie centrale ; IV. Translation (parallélogramme $ABB'A'$) ; V. Rotation (sens) ; chaque fois définition, figure sur quadrillage, méthode de construction en carreaux.
  - VI. Propriétés conservées + **méthode pour reconnaître une transformation** (ajout).
  - VII. Homothétie : définition avec $|k|$, figures $k = 3$ et $k = -2$, méthode sur quadrillage, propriétés, exemple, piège du signe.
  - VIII. Agrandissement-réduction : théorème $k$, $k^2$, $k^3$ (l'ancien tableau disait « volumes × |k|³ » sans parler d'agrandissement), figure carré/cube, exemple de la section de pyramide, méthode pour trouver $k$.
  - IX. Frises, rosaces ($\frac{360^\circ}{n}$), **pavages** (ajout, avec figure) ; `retenir` final.
- **Fiche 161** : réécrite, titre « Résumé : Transformations du plan » (tableau des 4 isométries avec figure, homothétie, tableau $k$/$k^2$/$k^3$, reconnaître une transformation, frises/rosaces/pavages, 4 erreurs classiques, réflexe brevet).
- **Exercices** : les 21 sont réécrits au format complet (méthode, étapes détaillées, résultat encadré, erreur fréquente, solution courte). Titres « Type - Sujet ». Progression : 7 Découverte, 7 Entraînement, 5 Problème, 2 Type brevet.
  - Les exercices de construction (2401, 2402, 2403, 2404, 2408, 2409, 2420) ne passent plus par des formules de coordonnées hors programme : constructions **sur quadrillage**, en comptant les carreaux.
  - **Remplacés** (même Id) :
    - 2406 « Reconnaître la transformation » (5 descriptions en mots) → « Découverte - Reconnaître une transformation » : une figure et ses 5 images sur quadrillage (translation, symétrie axiale, symétrie centrale, quart de tour, homothétie de rapport 0,5) ;
    - 2415 « Retrouver un centre » (coordonnées) → « Problème - Retrouver le centre et le rapport d'une homothétie » sur quadrillage (intersection de $(AA')$ et $(BB')$, vérification avec $(CC')$, $k = 2$, aires × 4) ;
    - 2417 « Deux homothéties successives » (composition, hors attendus) → « Problème - Transformations dans un pavage » (pavages absents de la notion : translations, symétrie centrale ou axiale, aire et nombre de pièces) ;
    - 2420 « Le parallélogramme et la translation » (coordonnées, distance en repère = 2nde) → « Type brevet - Translation et parallélogramme » sur quadrillage (image par translation, parallélogramme, centre de symétrie, longueur par Pythagore $\sqrt{17} \approx 4{,}1$ cm) ;
    - 2421 « La pyramide réduite » → « Type brevet - Section d'une pyramide » enrichi (hauteur par la formule du volume, $k = \frac{1}{3}$, côté de la section, volume de deux façons, pourcentage).
  - **Enrichis** : 2405 (question sur l'angle avec $k = -2$), 2407 (calcul de $OA'$), 2413 (aire du motif, figure corrigée), 2414 (rotation de 180° = symétrie centrale), 2418 (réciproque de Pythagore rédigée, aire de deux façons), 2419 (hauteur de la diapositive donnée pour calculer l'aire).
  - Aucune erreur de calcul dans les anciens résultats ; les défauts étaient le hors-programme (coordonnées), des corrigés réduits à une ligne, l'absence de pavage et de vraie reconnaissance de transformation.
- `verif_246.py` : **79 contrôles sympy OK** (chaque image de chaque figure recalculée par la vraie transformation sympy, alignements, milieux, aires, orientations ; tous les résultats numériques des exercices et du cours).

## Figures
- **41 figures neuves** (figures.py, style des livres, quadrillage) pour 42 positions ; les 12 images en ligne (matplotlib) sont toutes remplacées ; 0 conservée.
  - Cours (10) : axiale (axe oblique, médiatrice codée), centrale, translation, rotation (arc + angle droit), homothéties $k = 3$ et $k = -2$, carré/cube $k = 2$, frise, rosace (60°), pavage. Fiche (2) : les 4 isométries côte à côte, homothétie $k = -2$.
  - Exercices : figure d'énoncé **sans l'image** (figure de départ + axe, centre ou vecteur) et figure de corrigé **avec l'image en vert** et les traits de construction pour 2401, 2402, 2403, 2404, 2406, 2408, 2409, 2413, 2414, 2415, 2417, 2418, 2419, 2420 ; figure de corrigé seule pour 2410 (deux cas de signe), figure d'énoncé pour 2421 (pyramide et section).
- Détecteur texte/trait : 0 erreur ; seules alertes : cotes à fond blanc (2410, 2418, 2419, usage normal). Toutes ≤ 900 px. Chaque PNG regardé ; corrections faites après relecture (étiquettes déplacées sur 2404, 2408, 2415, cours_axiale, cours_homot_neg ; construction allégée sur 2401 ; cote de l'hypoténuse de 2418 mise à l'extérieur ; point $H'$ retiré de la pyramide, il chevauchait la hauteur).

## Contrôles
- `valider_v1.py` : 0 problème. `verifier_notion.py --navigateur` : **OK, 0 problème**.
- `controle_apercu.mjs` avec captures : 0 débordement, 0 erreur de formule, 0 image manquante sur les 132 vues (téléphone et ordinateur : cours, fiche, énoncé / étapes / solution des 21 exercices). Chrome ne se fermait pas à la fin : seul mon propre processus a été arrêté, après l'écriture de toutes les vues.
- Vues regardées sur téléphone : cours en entier (parties I à IX), fiche, exercices 2401, 2417 et 2421 (étapes). Corrections faites après ces vues : figures des corrigés sorties des encadrés « résultat » (elles y étaient rétrécies, 12 cas) ; formule de $k$ du cours VIII (réduite) raccourcie ; calcul de la rosace passé en formule centrée ; figure carré/cube resserrée ; 2421 Q1 (deux égalités côte à côte) passée en `aligned`.

## Remarques pour l'orchestrateur
- Titres du cours et de la fiche changés (intitulé de la notion) : `titres_docs.py` à l'import.
- Les 21 titres d'exercices changent (format « Type - Sujet ») ; 2420 et 2421 sont en « Type brevet ».
