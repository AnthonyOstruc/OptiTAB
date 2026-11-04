# Notion 283 (4e) : Théorème de Pythagore

**État : prêt** (claude-283, 2026-11-04). 21 exercices (aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée ; 3 exercices remplacés). Aucune écriture en base, aucun git.

Programme de 4e (cycle 4) : théorème de Pythagore pour calculer une longueur (hypoténuse ou côté de l'angle droit), valeur exacte avec une racine carrée puis valeur arrondie ; réciproque (démontrer qu'un triangle est rectangle) ; contraposée (démontrer qu'il ne l'est pas) ; rédaction modèle ; problèmes concrets (échelle, rampe, écran, diagonales, terrain, voilier). Rien de 3e (pas de trigonométrie, pas de simplification de racines).

## Cours et fiche

- **Titres** inchangés : « Théorème de Pythagore » et « Résumé : Théorème de Pythagore ».
- **Cours 278 réécrit façon manuel** (la conversion avait des exemples rangés dans des encadrés `definition`, la réciproque et la contraposée dans un même encadré `definition`, un renvoi « onglet Fiches », un objectif en pavé) : objectifs et prérequis en liste ; I. hypoténuse (définition, figure, propriété « plus long côté », conseil) ; II. théorème, carrés construits sur les côtés, **preuve par découpage sans calcul littéral** (deux rangements des quatre mêmes triangles dans le carré de côté $a + b$) ; III. méthode (additionner / soustraire), trois exemples rédigés en `aligned` avec figures (hypoténuse $12$-$16$-$20$, côté $7$-$25$-$24$, valeur exacte $\sqrt{34} \approx 5{,}8$), erreurs fréquentes, contrôle ; IV. réciproque (théorème), contraposée (propriété justifiée), méthode, **deux rédactions modèles** (rectangle : $4{,}5$ ; $6$ ; $7{,}5$ avec figure ; non rectangle : $5$ ; $6$ ; $8$), pièges de rédaction ; V. situations concrètes (figure des quatre situations : mur et sol, rectangle, triangle isocèle, losange ; quadrillage), « À retenir ».
- Les exemples du cours sont **nouveaux** : les anciens ($9$-$12$-$15$, $8$-$15$-$17$, $20$-$21$-$29$, $6$-$7$-$9$) étaient ceux des exercices 3189, 3190, 3192 et 3193.
- **Fiche 199 refaite** (puces « • » et symbole « ⟹ » de la conversion supprimés) : théorème + figure du vocabulaire, tableau additionner / soustraire avec exemples, méthode « rectangle ou non ? » avec deux exemples, où trouver un angle droit (figure), 5 erreurs classiques, réflexe.

## Exercices (21)

- **Progression** dans l'ordre des Id : 7 Découverte (3188-3194), 7 Entraînement (3195-3201), 5 Problème (3202-3206), 2 **Type brevet** (3207-3208 ; il n'y en avait aucun). Titres « Type - Pythagore - n. Sujet » → « Type - Sujet » (21).
- **Tous relus et réécrits** : questions numérotées ; corrigé avec méthode, étapes détaillées (chaque calcul de Pythagore en `aligned`, une égalité par ligne), résultat encadré à chaque question, encadré « Erreur fréquente » (ou « À retenir ») dans les 21 exercices ; `Solution:` courte et cohérente. `\displaystyle`, « **Erreur fréquente :** » en gras hors encadré, lignes `Image:` et majuscules d'insistance retirés ; étapes cassées par la conversion (formule prise pour titre d'étape, étape vide) refaites. Questions de remplissage supprimées (périmètres sans intérêt, vitesse du joueur, « vérifier » sans contenu) et regroupées en 4 ou 5 vraies questions.
- **Remplacés (3)** :
  - 3194 « Les triplets pythagoriciens » (sept vérifications du même type, déjà faites en 3192, 3193 et 3200) → « Découverte - Choisir la bonne propriété et rédiger » : théorème, réciproque ou contraposée selon les données, **rédaction à trous** puis rédactions complètes ($5$-$12$-$13$ ; $10$-$24$-$26$ rectangle ; $4$-$7$-$8$ non rectangle, $64 \neq 65$).
  - 3196 « Couper par la diagonale » (terrain de handball : doublon de 3203, terrain de football, même déroulé diagonale / économie / vitesse) → « Entraînement - Additionner ou soustraire ? » : trois triangles, hypoténuse cherchée ou connue, valeurs exactes $\sqrt{52}$, $\sqrt{51}$, résultat entier $6$ avec des décimaux.
  - 3202 « Deux toboggans » → « Problème - Construire une rampe d'accès » (contexte demandé par le programme de lot) : longueur de la rampe, pente en %, norme de $5$ %, avancée minimale $10$ m.
- **Réécrits en partie** : 3189 (la hauteur issue de $A$ par l'aire, avec figure) ; 3190 (contrôle au lieu d'une seconde hauteur) ; 3191 (un second triangle où l'on soustrait : $\sqrt{65}$) ; 3192 (second triangle à décimaux $1{,}6$ ; $3$ ; $3{,}4$) ; 3193 (centré sur la contraposée, avec un cas final qui est rectangle pour obliger à calculer) ; 3197 (axe de symétrie rappelé dans l'énoncé) ; 3198 (méthode des déplacements horizontal / vertical, $CD = \sqrt{97}$) ; 3203 (valeur exacte $\sqrt{15\,649}$) ; 3205 (pavé renommé proprement : fond $ABCD$ de $24 \times 18$, hauteur $16$, diagonales $30$ et $34$ cm ; l'ancien parlait d'une face $ABFE$ « au fond ») ; 3206 (relation pas à pas, sans formule générale imposée) ; 3207 (Type brevet : affirmation du skipper à vérifier, conversion $5{,}25$ h $= 5$ h $15$ min) ; 3208 (Type brevet : dimensions données, diagonale en pouces, format $16/9$, écran $4/3$ de même diagonale par $5k$, comparaison des aires ; l'ancien imposait $k^2 = 139{,}7^2/337$).
- **Erreurs corrigées** : aucune erreur de calcul dans les résultats en ligne ; défauts de rédaction : réciproque et contraposée présentées comme une « définition », conclusions sans la propriété citée.
- `verif_283.py` : **236 contrôles sympy**, tous justes (chaque carré, racine, arrondi, aire, pente, pourcentage, durée, conversion du cours, de la fiche et des 21 corrigés ; preuve par découpage ; données des figures relues dans `figures/figures.py` : longueurs des triangles tracés, spirale $OA_n = \sqrt{n}$).

## Figures (style livre, `figures/figures.py`)

- **50 figures neuves** pour **52 positions** ; les **24 images matplotlib en ligne sont toutes remplacées** (0 conservée, 0 non appelée).
  - Cours (7) : vocabulaire, carrés sur les côtés, preuve par découpage, exemple hypoténuse, exemple côté de l'angle droit, réciproque (angle droit en vert), quatre situations concrètes. Fiche (2, mêmes fichiers).
  - Exercices : figure d'énoncé (données, sans la réponse) **et** figure de corrigé (hypoténuse repérée en vert, longueur trouvée en vert) pour 20 exercices ; 3201 (erreurs à corriger, sans figure d'énoncé) a une figure de corrigé ; 3189 et 3198 ont deux figures de corrigé (hauteur ; triangles d'aide en orange).
  - Schémas concrets sobres : échelle et mur, rampe et porte (hauteur exagérée, signalée), terrain, tente en perspective puis sa section, pavé en perspective cavalière (arêtes cachées en pointillés), spirale, trajet du voilier, téléviseur.
- `figures_livre.py` : 0 chevauchement texte / trait, **aucune tolérance** (`TOLERE` vide). Toutes ≤ 900 px. Chaque PNG regardé (planches). Corrections après relecture : étiquette verticale du vocabulaire passée en deux lignes horizontales ; triangle 3 de 3188 agrandi et redressé ; lettres collées (« CS », « CD », « FG », « MV ») séparées ; longueurs sans unité + « longueurs en cm » pour les figures à trois triangles (3194, 3196) ; graduation « 5 » barrée par un trait d'aide retirée (3198) ; tirets cachés de la tente écartés du codage ; perspective du pavé à 45° (le point $D$ tombait sur la diagonale $[AG]$).

## Contrôles

- `verif_283.py` : 236 contrôles justes.
- `verifier_notion.py` : OK (52 nouvelles images, 0 conservée, 0 non appelée ; notes : 21 titres changés).
- Contrôle Chrome : avec `--navigateur`, Chrome est resté bloqué (cas connu, § 3 de la consigne de lot) → procédure de repli : vérificateur sans navigateur OK + `controle_apercu.mjs` avec captures, deux fois (avant et après les corrections téléphone) : **130 vues sur 130 sans défaut** (cours, fiche, 21 exercices × 3 onglets, téléphone et ordinateur). Seuls mes propres processus Node bloqués ont été arrêtés (32780 et son parent 15140, puis 22516 et 5456 après la fin des vues) et leurs verrous `chrome_*.lock` libérés.
- **Captures téléphone regardées** (deux passes groupées) : cours (4 vues), fiche (2), énoncé 3188, corrigés 3192, 3193, 3194, 3198, 3208. Corrections faites après la première passe : les sommes « D'autre part » trop longues (réduites, point final seul sur une ligne) passées en calcul aligné, une égalité par ligne (cours : deux rédactions modèles ; 3192, 3193, 3194) ; formule « côté² = hypoténuse² − autre côté² » de 3190 et diagonale du fond de 3205 en formule centrée ; figure de la preuve resserrée. Vérifié sur les nouvelles captures.
- Sauvegardes de travail : `sauvegardes/283_*_conversion_auto.txt`, `sauvegardes/283_exercices_avant_telephone.txt`, `sauvegardes/283_cours_avant_telephone.txt`.

## Remarques pour l'orchestrateur

- Aucune remarque d'outil ou de moteur.
