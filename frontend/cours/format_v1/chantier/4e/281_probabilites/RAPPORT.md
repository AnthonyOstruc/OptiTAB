# Notion 281 (4e) : Probabilités

**État : prêt** (claude-281, 2026-11-04). 21 exercices (aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée ; 8 exercices remplacés).

Programme de 4e (cycle 4) : vocabulaire (expérience aléatoire, issue, événement, certain, impossible, contraire), probabilité en situation d'équiprobabilité (dé, urne, roue, cartes), somme des probabilités égale à 1, $P(\text{non } A) = 1 - P(A)$, fréquence et probabilité (stabilisation, estimation d'une probabilité inconnue), simulation au tableur et avec Scratch. Les expériences à deux épreuves (3e) ne figurent qu'en **découverte** : partie V du cours et exercice 3131 (deux pièces, arbre de dénombrement).

## Cours et fiche

- **Titres** inchangés : « Probabilités » et « Résumé : Probabilités ».
- **Cours 276 réécrit façon manuel** (la conversion avait un objectif en pavé, une phrase hors encadré, le renvoi « onglet Fiches », un tableau de deux dés en image et pas de simulation) : objectifs en liste ; I. expérience aléatoire, issue, événement, certain / impossible, contraire (exemples sur le dé, mise en garde « gagner / perdre / nul ») ; II. probabilité (définition, échelle des probabilités en figure, écritures fraction / décimal / pourcentage, équiprobabilité, méthode en 3 points, urne en figure, erreur « compter les couleurs », somme égale à 1, roue à secteurs inégaux $P = \frac{\text{angle}}{360°}$) ; III. événement contraire (propriété, exemples, « quand passer par le contraire », piège $0{,}4 + 0{,}5$) ; IV. fréquence (définition, stabilisation avec courbe simulée, estimer une probabilité inconnue, simulation tableur `=ALEA.ENTRE.BORNES(1;6)` / `=NB.SI` et script Scratch, trois mises en garde) ; V. découverte des deux épreuves (arbre des deux pièces) ; « À retenir ».
- **Fiche 196 refaite** : tableau du vocabulaire, échelle, 3 formules encadrées, réflexes, fréquences avec courbe, simulation, 5 erreurs classiques, réflexe.

## Exercices (21)

- **Tous relus et réécrits** au format des modèles : questions numérotées ; corrigé avec méthode, étapes détaillées, résultat encadré à chaque question et **au moins une « Erreur fréquente » dans chacun des 21** (plus des « À retenir ») ; `Solution:` courte et cohérente ; `\displaystyle`, lignes `Image:` et « **À retenir :** » en gras libre retirés ; titres « Type - Probabilités - n. Sujet » → « Type - Sujet » (21).
- **Progression** dans l'ordre des Id : 7 Découverte (3125-3131), 7 Entraînement (3132-3138), 4 Problème (3139-3142), 3 **Type brevet** (3143-3145 ; il n'y en avait aucun).
- **Remplacés (8)** :
  - 3129 « Placer sur l'échelle » (même dé que 3126, doublon) → « Découverte - Placer des événements sur l'échelle des probabilités » : six expériences différentes (pièce, dé, sac, cartes), impossible / certain, contraire, rangement, placement sur l'échelle ;
  - 3131 « Les lettres d'un mot » (3e variante de « compter les objets ») → « Découverte - Lancer deux pièces » (seule découverte des deux épreuves : arbre, issues, « au moins un pile » par le contraire, erreur de Léo 1/3) ;
  - 3132 « La somme de deux dés » (deux épreuves, 3e) → « Entraînement - Simuler des lancers de dé avec Scratch » (vrai script, fréquences de quatre exécutions, passage à 6 000 lancers en vert) ;
  - 3136 « Lancer deux pièces » (déplacé en 3131) → « Entraînement - Des cartes numérotées de 1 à 20 » (multiples, nombres premiers, diviseurs, carrés : lien avec l'arithmétique de 4e) ;
  - 3137 « Le dé est-il équilibré ? » (doublon de 3142) → « Entraînement - Estimer la probabilité d'une punaise » (probabilité inconnue estimée par la fréquence) ;
  - 3139 « Le stand de la kermesse » (deux dés) → « Problème - La roue de la kermesse » (roue à 12 secteurs, gains, bilan estimé sur 600 parties, fréquence observée, roue modifiée) ;
  - 3141 « Le code du cadenas » (dénombrement par produit, hors programme du collège) → « Problème - Retrouver le contenu d'un sac » (somme des probabilités, modèle en barre, équation de 4e) ;
  - 3144 « Pierre, feuille, ciseaux » (deux épreuves) → « Type brevet - Le distributeur de boules de gomme » (contraire, affirmation à vérifier, tirage après retrait d'une boule, équation, fréquence).
- **Réécrits en partie** : 3125 (urne de 12 boules, différente de l'exemple du cours) ; 3126 (événements A, B, C, nombre premier, contraire calculé de deux façons) ; 3133 (pièce simulée au tableur, `=SOMME` pour compter les « pile ») ; 3138 (jeux à une seule épreuve : dé, sac, roue ; « équitable » ≠ « probabilité 1/2 ») ; 3140 (comparaison exacte des fractions au dénominateur 45, équation pour l'urne B) ; 3143 (tableau à compléter, pourcentage, question conditionnelle « parmi les filles » retirée car hors programme, « fille ou demi-pensionnaire » = contraire de « garçon externe ») ; 3145 (zones nommées « petit disque » / « couronne » pour pouvoir colorier en vert).
- **Aucune erreur de calcul** dans l'ancien contenu ; trois points hors programme retirés (dénombrement du cadenas, probabilité « parmi les filles », expériences à deux épreuves en entraînement / problème).
- Espaces insécables avant les unités (€, cm, cm²) : 42.

## Figures (style livre, `figures/figures.py`)

- **39 figures neuves pour 42 emplacements** ; les **20 images matplotlib en ligne sont toutes remplacées** (0 conservée). L'image du tableau d'élèves (3143) et le tableau de deux dés de la fiche ne sont plus appelés (données en tableau natif / sans objet) : supprimés à l'import.
  - Cours (6) : échelle des probabilités, urne, roue à secteurs inégaux, courbe de fréquence du 6 (2 000 lancers simulés, graine choisie pour une stabilisation nette), script Scratch, arbre des deux pièces. Fiche (2) : échelle, courbe.
  - Exercices : énoncé + corrigé en vert pour 3125 (urne, rouges entourées), 3126 (faces du dé, paires en vert), 3127 (roue colorée, secteurs « rouge ou pair » entourés), 3128 (32 cartes, figures en vert), 3129 (échelle vide / événements placés), 3131 (arbre / chemins PF, FP), 3132 (script / nombres modifiés en vert), 3135 (roue à angles / secteurs pairs), 3136 (20 cartes / premiers), 3138 (roue / Ana en vert, Ben en orange), 3139 (roue de kermesse / secteurs gagnants), 3140 (trois urnes / rouges entourées et fractions sur 45), 3142 (diagramme / hauteur attendue 83 en vert), 3144 (distributeur / rouges entourées), 3145 (cible / petit disque puis couronne en vert) ; corrigés seuls : 3133 et 3137 (fréquences qui se stabilisent), 3141 (bande des douzièmes : 1 part = 2 boules).
- Scratch : module `scratch.py` copié de 248 sans modification ; `controle_scratch.py` : 0 erreur ; les 3 scripts font 998 px (comme 2455 en 3e : le bloc « nombre aléatoire entre 1 et 6 » imbriqué), sous la limite de 1 100 px.
- `figures_livre.py` : 0 chevauchement texte / trait ; tolérances seulement pour les blocs Scratch (texte sur fond coloré, contrôlé à part) ; seules alertes : cote « 40 cm » à fond blanc (normal). Toutes les autres figures ≤ 900 px. Chaque PNG regardé ; corrections après relecture : échelles trop larges, étiquette « issue » collée dans l'arbre (retirée), cible agrandie (cote 10 cm trop près du cercle), distributeur aéré, courbe du cours qui restait au-dessus de 1/6.

## Contrôles

- `verif_281.py` : **187 contrôles** (sympy `Rational`, dénombrements exhaustifs, équations résolues par sympy, données des figures relues dans `figures.py`, script Scratch exécuté sur 15 graines), tous justes.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (42 nouvelles figures, 0 image en ligne conservée, 1 non appelée → supprimée à l'import ; notes : 21 titres changés). Après les dernières retouches : `verifier_notion.py` relancé (OK) + `controle_apercu.mjs` avec captures : **aucun problème détecté** (cours, fiche, 21 exercices × 3 onglets, téléphone et ordinateur).
- Captures téléphone regardées : cours (parties II, IV, V), fiche, exercices 3125, 3127, 3128, 3132, 3133, 3137, 3139, 3140, 3141, 3142, 3143, 3144, 3145 (étapes). Corrigé après captures : formule de la fiche coupée (« P(certain) = 1 » hors écran) → formule + ligne ; tableaux trop larges dans les corrigés de 3142 (7 colonnes) et 3143 (résultat) → calculs alignés / liste ; formules réduites (« $1 - P(A) = \dots$ » dans 3125, 3126, 3131 ; 3141 Q1 ; 3143 Q6) → raccourcies ou alignées sur plusieurs lignes ; fractions en ligne qui se touchaient sur deux lignes (3127, 3129, 3134, 3135, 3136, 3138, 3139, 3141) → listes ; listes de fréquences (3133, 3137, 3142) → calculs alignés ; « € » seul en début de ligne (3139) ; fractions minuscules sous les urnes de 3140 → retirées de la figure (elles sont dans le texte).
- Chrome : seul mon processus lancé par les outils ; verrous `outils/.verrous` respectés (gérés par les outils, un autre agent les utilisait en même temps).

## Remarques pour l'orchestrateur

- 3139 et 3144 utilisent « nombre de parties × probabilité » pour estimer des effectifs (fréquence ≈ probabilité, programme de 4e), sans notion d'espérance.
- 3145 (cible) : probabilité = quotient d'aires, admise dans l'énoncé (aire du disque connue depuis la 6e / 5e).
- Les 3 scripts Scratch font 998 px de large (texte un peu petit sur téléphone, comme 2455 en 3e) : le bloc « mettre dé à nombre aléatoire entre 1 et 6 » imbriqué dans « répéter » ne peut pas être plus étroit sans modifier `scratch.py`.
- Sauvegarde de la conversion automatique : `sauvegardes/exercices_conversion_auto.txt`.
