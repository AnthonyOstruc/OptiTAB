# Notion 287 (4e) : Cosinus dans le triangle rectangle

**État : prêt** (claude-287, 2026-11-04). 21 exercices (aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée ; 4 exercices remplacés ou refondus). Aucune écriture en base, aucun git.

Programme de 4e (cycle 4) : hypoténuse et côté adjacent à un angle aigu ; cosinus d'un angle aigu (quotient indépendant de la taille du triangle, justifié par Thalès en triangles emboîtés, notion 286) ; calcul d'une longueur (côté adjacent ou hypoténuse) ou d'un angle à la calculatrice (mode degrés, touche $\cos^{-1}$, arrondis) ; problèmes concrets (échelle, rampe, toboggan, toit, téléphérique…). Le troisième côté s'obtient avec Pythagore. Sinus et tangente (3e) ne sont jamais exigés : une seule mention dans une remarque du cours.

## Cours 286 et fiche 221

- **Titres** inchangés : « Cosinus dans le triangle rectangle » et « Résumé : Cosinus dans le triangle rectangle ».
- **Cours réécrit** façon manuel (l'ancien mettait les exemples dans des encadrés `definition`, utilisait des puces « • », renvoyait à « l'onglet Fiches » et réutilisait les valeurs des exercices 3652-3654) : objectifs et prérequis ; I. vocabulaire (définition, exemple, le côté adjacent change avec l'angle, 2 figures) ; II. propriété « le quotient ne dépend que de l'angle » avec sa **démonstration par Thalès** (triangles emboîtés), définition du cosinus, exemple, propriété $0 < \cos < 1$ et décroissance (figure) ; III. calculatrice (mode degrés, les touches $\cos$ et $\cos^{-1}$ en liste) ; IV. calculer une longueur (méthode en 4 étapes, côté adjacent puis hypoténuse en `aligned`, erreurs fréquentes, remarque Pythagore) ; V. calculer un angle (méthode, exemple, angles complémentaires) ; VI. problèmes concrets (méthode, échelle de 4 m) ; à retenir. Valeurs des exemples différentes de celles des exercices.
- **Fiche réécrite** : vocabulaire (figure), formule encadrée, les trois calculs types (côté adjacent : on multiplie ; hypoténuse : on divise ; angle : $\cos^{-1}$) avec formule et exemple, outils complémentaires, 6 erreurs classiques.

## Exercices (21)

- **Progression** dans l'ordre des Id : 7 Découverte (3650-3656), 7 Entraînement (3657-3663), 5 Problème (3664-3668), **2 Type brevet** (3669-3670 ; il n'y en avait aucun, et 7 « Problème »). Titres « Type - Cosinus - n. Sujet » → « Type - Sujet » (21).
- **Tous relus et réécrits** : 6 questions numérotées ; corrigé avec méthode, étapes détaillées (calculs en `aligned`, valeurs non arrondies gardées), **résultat encadré à chaque question (126/126)**, **« Erreur fréquente » dans 21/21** (encadré `attention`), « À retenir » quand utile ; `Solution:` courte et cohérente. Retirés : `\displaystyle` partout, lignes `Image:`, « **Erreur fréquente :** » en gras hors encadré, « cos⁻¹ » en texte (→ $\cos^{-1}$), titres d'étapes cassés par la conversion (« L'angle droit est en $A$ » coupé en deux), majuscules d'insistance.
- **Remplacés / refondus (même Id)** :
  - 3663 « L'aire d'un triangle » (même structure que 3661 : hauteur dans un triangle quelconque) → « Entraînement - Côté adjacent, hypoténuse ou angle » : trois triangles d'orientations différentes, tableau « connu / cherché », multiplier, diviser ou $\cos^{-1}$ ;
  - 3665 « Le décollage » (même schéma que le cerf-volant et le téléphérique) → « Problème - Une rampe de chargement » (consigne : rampe ; angle ≤ 20°, deux camions, rampe de 3 m puis 4 m, place au sol) ;
  - 3669 « Le losange » → **Type brevet** « Le toboggan d'une aire de jeux » (consigne : toboggan ; parties A, B, C : dimensions, emplacement avec zone libre, second modèle et pente conseillée) ;
  - 3670 « L'escalator » (doublon de la rampe) → **Type brevet** « Réciproque de Pythagore et cosinus » (triangle 9-12-15, angles, hauteur : $BH = 5{,}4$ et $AH = 7{,}2$ exacts, aire de deux façons).
- **Enrichis** : 3664 téléphérique (on donne maintenant la distance horizontale → hypoténuse par division, durée en min s, second téléphérique comparé) ; 3653 (angle 52° au lieu de 50° : avec 50°, $AC = 7{,}1505$ tombait pile sur l'arrondi au millimètre) ; 3656 (affirmation 3 doublon de la 6 → comparaison de deux angles par leurs cosinus) ; 3658 Q6 (doublon de $\cos = 0{,}5$ → $\cos^{-1}(0{,}625)$) ; 3657 Q6 (limites arrondies du côté sûr : $1{,}30$ m et non $1{,}29$ m, qui dépasse 75°) ; 3655 (tableau à compléter en tableau natif au lieu d'une image).
- **Valeurs corrigées** : arrondis intermédiaires faux en ligne (3661 : $HC \approx 4{,}763$, $\widehat{C} \approx 53{,}46^\circ$ ; 3667 : $OH^2 \approx 84{,}50$, $HP^2 \approx 59{,}50$, $\cos \approx 0{,}5859$) ; tous les résultats finaux étaient justes.

## Figures (style livre, `figures/figures.py`)

- **59 figures neuves** pour **61 positions** ; les **44 images matplotlib en ligne sont toutes remplacées ou retirées** (0 conservée ; l'image du tableau de 3655 devient un tableau natif, la capture de calculatrice du cours devient une liste des touches).
  - Cours (8) : vocabulaire pour $\widehat{ABC}$ et pour $\widehat{ACB}$ (hypoténuse et côté adjacent en vert, côté opposé en gris), triangles emboîtés à 40°, décroissance du cosinus (hypoténuse 10 cm à 20°, 45°, 70°), trois exemples (résultat en vert), échelle. Fiche : la figure de vocabulaire.
  - Énoncés : triangles rectangles avec l'angle droit codé, l'angle marqué et les données seules ; schémas concrets sobres (mur et échelle, cerf-volant, téléphérique, camion et rampe, maison et toit, nord/est, pendule, toboggan avec zone libre).
  - Corrigés (21/21 exercices, sauf 3655 qui a la figure de décroissance) : hypoténuse et côté adjacent **tracés en vert et nommés**, résultats en vert ; 3650 a une figure par triangle et une pour l'autre angle, 3651 une par angle, 3663 une par triangle, 3665, 3666, 3669 une par situation.
- `figures_livre.py` : 0 texte sur un trait, aucune tolérance ; avertissements restants = cotes à fond blanc (3666, 3669, 3670 : usage normal) ; toutes ≤ 900 px. Chaque PNG regardé (planches) ; corrigés après relecture : angles étroits dont la mesure touchait un côté (3654, 3663, échelle du cours), libellés posés sur un trait (rectangle, rampe, toit, bateau, pendule), noms de points sous une valeur (3657, 3661), virgules décimales de la figure de décroissance.

## Contrôles

- `verif_287.py` : **229 contrôles sympy justes** (chaque valeur du cours, de la fiche, des figures et des 21 corrigés, résultats intermédiaires et arrondis compris).
- `verifier_notion.py` : **OK** (61 positions de figures, 0 image en ligne conservée ; notes : 21 titres changés, voulu).
- Navigateur : avec `--navigateur`, Chrome est resté bloqué à la fermeture (cas connu ; toutes les vues à 0) → contrôle refait avec `controle_apercu.mjs` et captures sur la version finale : **130 vues (téléphone + ordinateur), 0 débordement, 0 erreur de formule, 0 `$` brut, 0 image manquante, 0 élément trop large**. Même blocage à la fermeture après la dernière vue : seuls mes processus `node` ont été arrêtés et seuls mes verrous (`chrome_0`, puis `chrome_1` et `chrome_2`) retirés ; le verrou de l'agent 286 n'a pas été touché.
- **Captures téléphone regardées** : cours en entier (5 vues), fiche, corrigés 3663 et 3669. Corrections faites après ces vues : tableau de la calculatrice (cours), tableau des trois calculs (fiche) et tableau à 5 colonnes de 3663 coupés sur téléphone → remplacés par des listes / sous-titres avec formules centrées ; figure de décroissance trop petite → triangles en colonne ; « , donc » rejeté en début de ligne (3663) → calcul aligné ; 5 formules longues centrées ; figures 3665 et 3669 rétrécies.
- Méthode dans les 21 corrigés (encadré `methode` ajouté à 3654, 3655, 3656, 3662, 3667, 3668).
- Espaces insécables avant les unités : 226 ajoutées (exercices, cours, fiche).
- Sauvegardes de la conversion automatique : `sauvegardes/287_*_conversion_auto.txt`.

## Remarques pour l'orchestrateur

- Aucune remarque d'outil ou de moteur.
