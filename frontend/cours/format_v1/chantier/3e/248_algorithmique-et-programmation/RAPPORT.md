# Notion 248 (3e) : Algorithmique et programmation

**État : prêt** (agent-3e-248, 2026-11-03).

Programme du cycle 4 (thème « Algorithmique et programmation », programmation par blocs comme au brevet) : variables, entrées et sorties ; séquences ; instructions conditionnelles (conditions composées, reste « modulo ») ; boucles bornées et conditionnelles ; déplacements et stylo du lutin (repère de la scène, orientation) ; blocs personnalisés avec paramètres ; événements et messages entre lutins ; hasard et simulation ; programmes de calcul et tracés de figures.

**Tableur : hors de ce chapitre.** Au cycle 4, le tableur relève des thèmes « Organisation et gestion de données, fonctions » (statistiques, fonctions), pas d'« Algorithmique et programmation ». La partie « VI. Le tableur » du cours, le tableur de la fiche et les deux exercices de tableur (2456, 2462) sont remplacés par du Scratch de type brevet.

## Texte
- **Titres** : cours « Algorithmique et programmation », fiche « Résumé : Algorithmique et programmation » (inchangés, conformes à la notion).
- **Cours 243** : réécrit façon manuel. Objectifs, prérequis ; I. Algorithme, programme, script (palette des familles de blocs, forme des blocs) ; II. Variables, entrées, sorties (programme de calcul avec tableau d'exécution, méthode « exécuter à la main », lecture d'une affectation) ; III. Conditions (« si … alors … sinon », et / ou / non, modulo, valeur frontière) ; IV. Boucles (bornée et conditionnelle, chacune avec son tableau d'exécution, erreurs fréquentes, boucle infinie) ; V. Lutin et stylo (scène, orientation, blocs de mouvement, carré tracé, polygones réguliers, angle extérieur) ; VI. Blocs personnalisés (paramètres, appel) ; VII. Événements, messages, hasard (simulation) ; À retenir.
- **Fiche 163** : réécrite (scripts et variables, conditions, tableau des trois boucles, lutin et stylo, blocs/messages/hasard, 5 erreurs classiques, réflexe brevet).
- **Exercices** : les **21 réécrits** (méthode, étapes détaillées avec **tableau d'exécution pas à pas** dès qu'on suit un script, résultat encadré, erreur fréquente ou à retenir, solution courte). Titres « Type - Sujet » (le « Algorithmique - 1. » répété est supprimé). Progression : 7 Découverte, 7 Entraînement, 5 Problème, 2 Type brevet.
  - **Remplacés (même Id)** :
    - 2444 « Un nombre demandé » (doublon de 2443) → « Compléter un programme de calcul » : **script à trous** (cases A, B, C), essais, expression $3x + 12$, équation, erreur d'ordre des blocs ;
    - 2447 « Doubler plusieurs fois » (doublon des boucles bornées) → « Se repérer sur la scène » : coordonnées, orientation, « ajouter à y », ligne brisée tracée ;
    - 2453 « Une boucle qui dépasse » (doublon de 2450) → « Piloter le lutin au clavier » : **événements** (touches), positions, écrire un 5e script ;
    - 2456 « Formule de tableur recopiée » (hors chapitre) → « Compléter un script de tracé » : rectangle cible, **script à trous** (A à E), sommets, périmètre ;
    - 2462 « Épargne au tableur » (hors chapitre) → **Type brevet** « Une frise de triangles » : bloc personnalisé, variable qui grandit, choix entre trois dessins, longueur tracée, position finale, modification ;
    - 2463 « La somme de deux dés » → **Type brevet** restructuré (lecture du script, 36 issues, fréquence, modifier la condition pour les doubles, somme la plus probable).
  - **Enrichis** : tous les autres (corrigés autrefois réduits à un résultat). Ajouts : 2446 condition « (x < 10) ou (x = 10) » ; 2448 triangle équilatéral tracé ; 2452 tableau des 12 divisions ; 2457 ordre d'exécution des deux lutins ; 2461 partie complète et dichotomie justifiée ($100 \to 50 \to 25 \to 12 \to 6 \to 3 \to 1$).
  - Aucune erreur de calcul trouvée dans les résultats en ligne ; corrigés incomplets complétés.

## Figures
- **Nouveau module `figures/scratch.py`** (réutilisable, notamment pour les sujets brevet 253) : vrais blocs Scratch 3 en TikZ.
  - Formes : chapeau (événements), bloc « définir » avec prototype, blocs à encoche et bosse, blocs C (répéter, répéter jusqu'à, si … alors … sinon, imbrications), ovales (valeurs, variables, opérateurs), hexagones (conditions), menus déroulants, cases blanches, drapeau vert, flèches ↺ / ↻.
  - Couleurs officielles des familles : événements jaune, contrôle orange, opérateurs vert, variables orange foncé, mouvement bleu, apparence violet, capteurs bleu clair, stylo vert foncé, mes blocs rose.
  - Textes mesurés avec les métriques réelles de Montserrat (fontTools) : aucun texte coupé, blocs ajustés au contenu.
  - **Énoncé** : `Trou("A", solution)` = case en pointillés bleus ; **corrigé** (`corrige=True`) : solution en vert, blocs modifiés `hl=True` cerclés de vert.
  - `figure_trace(...)` : repère de la scène, tracé du lutin en vert (ou bleu pour une figure cible), point de départ, flèche orange d'orientation finale.
  - **Exécution** : `traduire(projet)` traduit les scripts en Python (une fonction par script, messages, touches, blocs personnalisés) ; `executer(projet, entrees, touches, tirages)` les exécute et rend les valeurs dites, les variables, les positions et les segments tracés. Les tracés des corrigés sont produits **par cette exécution**.
  - Mode d'emploi en tête du module ; exemple : `figure_scripts([("", [Drapeau(), Mettre("x", 3), Dire(V("x"))])])`.
- **53 figures neuves** pour **55 positions** (cours 11, fiche 2, exercices 42) ; les **32 images en ligne** (matplotlib) sont toutes remplacées ; 0 conservée. Images de tableur retirées.
  - 38 figures de blocs (énoncés, scripts à trous, corrigés complétés ou modifiés en vert) ; 14 repères (tracés en vert, rectangle cible, trajet au clavier en pointillés, pentagone juste en vert et tracé faux à 108° en orange) ; 1 planche « dessins A, B, C ».
- Détecteur texte/trait : 0 erreur sur les repères. Les figures de blocs ont un `TOLERE` (texte blanc sur le fond coloré des blocs, que le détecteur prend pour un trait) **et** un vrai contrôle : `figures/controle_scratch.py` recompile les 38 figures en version fonds blancs / texte noir / contours conservés : **0 texte sur un contour**.
- Largeur : 4 scripts contenant « nombre aléatoire entre … » imbriqué (2455, 2461, 2463 ×2) font 997 à 1 031 px (< 1 100) ; le bloc Scratch est long par nature. Toutes les autres figures ≤ 900 px.

## Contrôles
- `verif_248.py` : **147 contrôles OK**. Les **44 scripts** (cours, exercices, variantes des corrigés) sont traduits en Python et exécutés ; traductions dans `programmes_248.txt`. Expressions vérifiées avec sympy par exécution symbolique ($2n + 6$, $2a + 10$, $3x + 12$, $3x + 4$, résultat constant $2$, $\frac{a}{4}$) ; boucle infinie détectée (2450) ; 100 parties du nombre secret jouées par dichotomie (au plus 7 essais) ; simulations de dés (fréquences proches de $\frac{1}{6}$).
- `figures/controle_scratch.py` : 38 figures de blocs, 0 texte sur un contour.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (55 positions de figures, 0 image en ligne conservée). Après les dernières retouches (scène, palette) : `verifier_notion.py` OK puis `controle_apercu.mjs --rapide`.
- `controle_apercu.mjs` avec captures : **130 vues sur 130 sans défaut** (0 débordement, 0 erreur de formule, 0 image manquante, 0 élément trop large), téléphone et ordinateur. Chrome est resté bloqué à la fermeture (cas connu) : seuls mes processus node (31276, 31436) ont été arrêtés, après la dernière vue.
- Vues regardées sur téléphone : cours (I à V), fiche, exercices 2447, 2450, 2452, 2456, 2457, 2458, 2459, 2461, 2462 (étapes). Corrections faites après ces vues : tableaux de positions et de messages (2447, 2448, 2454, 2456, 2459, 2461, 2462) remplacés par des listes pas à pas (colonnes coupées sur téléphone) ; tableau des 12 divisions de 2452 réduit à 3 colonnes ; tableau des sommes de 2463 transposé ; scène du cours redessinée plus grande (rose des orientations sous la scène) ; palette des familles resserrée ; noms d'axes et graduations du coin bas-gauche qui se touchaient corrigés sur tous les repères.

## Remarques pour l'orchestrateur
- Le module `scratch.py` peut servir à la notion 253 (sujets type brevet) : copier `figures/scratch.py` dans son dossier `figures/` et `from scratch import *`.
