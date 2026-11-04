# Notion 256 (4e) : Équations et résolution de problèmes

**État : prêt** (claude-256, 2026-11-03). 21 exercices (aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée ; 3 exercices remplacés).

Programme de 4e (cycle 4) : tester si un nombre est solution, résoudre une équation du premier degré $ax + b = cx + d$ (avec parenthèses à développer, coefficients décimaux ou fractionnaires), mettre un problème en équation (inconnue, équation, résolution, vérification, phrase). Équations produit et inéquations (3e) non exigées ; seul un **test** de valeur dans $x^2 = 9$ figure (2600).

## Cours et fiche

- **Titres** inchangés : « Équations et résolution de problèmes » et « Résumé : Équations et résolution de problèmes » (intitulé de la notion).
- **Cours 251 réécrit façon manuel** (la conversion avait mis l'exemple rédigé dans un encadré « définition », la méthode en ligne, des emojis et le renvoi « onglet Fiches ») : objectifs en liste ; I. équation, inconnue, membres, solution (définitions, méthode « tester », un exemple oui et un exemple non, remarque test / résolution) ; II. balance de Roberval (figure en trois étapes $3x + 2 = x + 10$, règles de transformation, tableau de cinq équations en une opération) ; III. premier degré (définition $ax + b = cx + d$, méthode en 5 étapes, exemples en `aligned` : inconnue des deux côtés, parenthèses, coefficient négatif ; solution non entière ; décimaux / fractions ; cas « aucune solution » / « tous les nombres » ; 4 erreurs fréquentes) ; IV. mise en équation (méthode en 5 étapes, exemple des trois frères rédigé étape par étape avec schéma en barres, tableau de traduction, conseil, « une solution doit avoir un sens ») ; « À retenir ».
- Exemples du cours changés pour ne plus doubler les exercices (ancien $5x - 3 = 2x + 9$ = exercice 2603 ; anciens cas particuliers = 2603 ; $\frac{x}{4} = \frac{x}{6} + 1$ = 2605).
- **Fiche 171 refaite** : solution et test, balance, méthode + exemple, tableau « une solution / aucune / tous les nombres », mise en équation + schéma + tableau de traduction, 5 erreurs classiques, réflexe ; plus de puces « • » ni d'emojis.

## Exercices (21)

- **Tous réécrits** au format des modèles : questions numérotées ; corrigé avec méthode, étapes détaillées (calculs alignés), résultat encadré à chaque question, vérification systématique, erreur fréquente et/ou « À retenir » dans chaque exercice ; `Solution:` courte et cohérente. Titres « Type - Sujet » (« Équations - n. » retiré, 21 titres changés). Lignes `Image:` de la conversion retirées (images déclarées dans `correspondance.json`).
- **Progression** dans l'ordre des Id : 7 Découverte (2600-2606), 7 Entraînement (2607-2613), 4 Problème (2614-2617), 3 **Type brevet** (2618-2620 ; il n'y en avait aucun).
- **Remplacés (3)** :
  - 2609 « La carte de cinéma » (doublon de 2614 forfaits : deux offres « fixe + prix unitaire ») → « Entraînement - Deux programmes de calcul » ($4(x + 3) = 6x - 2$, obtenir $30$, programme C sans solution commune) ;
  - 2617 « Le mélange de cafés » (même structure $x$ / $10 - x$ que la tirelire 2618) → « Problème - La note à obtenir pour une moyenne » (moyenne simple puis coefficient $2$, $x = 20{,}5$ impossible, meilleure moyenne $14{,}8$) ;
  - 2619 « Même périmètre » (doublon de 2608, périmètres donnés) → « Type brevet - Un carré et un triangle sur un segment » (classique de brevet : $4x = 36 - 3x$, $x = \frac{36}{7}$, valeur exacte puis arrondi, vérification exacte, périmètre double).
- **Réécrits en partie** : 2600 (question 6 $x(x - 4) = 0$, équation produit de 3e, remplacée par un test en tableau ; ajout du test de $-2$) ; 2606 (deux énigmes avaient la même réponse $8$ et deux autres $18$ : nombres changés) ; 2607 (question 1 « combien de fois plus âgé » remplacée par un test dans $5$ ans) ; 2610 (question 6 fraction du gain remplacée par l'usage de l'expression $6x + 20$) ; 2613 (résolutions fautives présentées ligne à ligne, vérification de la réponse de l'élève) ; 2614 (question 6 complétée par le seuil A = C à $120$ min) ; 2618 passée en Type brevet avec une feuille de tableur (formules `=40-A2`, `=2*A2+0,5*B2`) ; 2620 passée en Type brevet.
- **Erreurs corrigées** : `Solution:` de 2614 question 6 fausse (« A (360 min) ») ; figure en ligne de 2608 fausse (triangle isocèle dessiné avec les côtés $x$, $x + 3$, $x$ : la base était $x$) ; étapes tronquées de la conversion (2601, 2603). Aucune autre erreur de calcul dans l'ancien contenu.
- `verif_256.py` : **222 contrôles** sympy (chaque équation du cours, de la fiche et des exercices résolue avec `solveset`, cas « aucune / toutes », chaque vérification, développements, zones des forfaits, tableur, valeurs exactes et arrondis), tout juste.

## Figures (style livre, `figures/figures.py`)

- **24 figures neuves, 26 emplacements** ; les **15 images matplotlib en ligne sont toutes remplacées** (0 conservée, 0 non appelée).
  - Cours (2) et fiche (2, mêmes fichiers) : balance de Roberval en trois étapes (opérations écrites entre les plateaux, dernière étape en vert), schéma en barres du partage des trois frères (remplace l'ancien organigramme décoratif « 1. Choisir l'inconnue… »).
  - Exercices, énoncé **et** corrigé en vert : 2601 (deux balances, puis chaque résolution comme opérations sur les deux plateaux), 2607 (frise des âges : aujourd'hui / dans $x$ années, puis il y a 5 ans / dans 16 ans), 2608 (triangle isocèle et rectangle, puis 11, 11, 14 cm et 7 × 21 cm), 2611 (angles $2x$, $x$, $x + 20$, puis 80°, 40°, 60°), 2612 (carré et rectangle, puis $x = 4$ : 16 cm² chacun), 2615 (situation à 14 h 30 avec avance inconnue, puis rattrapage à 18,75 km), 2616 (terrain et clôture, puis 80 m / 40 m et les aires), 2619 (carré et triangle sur $[AB]$, puis $\frac{36}{7}$ et $\frac{48}{7}$ cm) ; corrigés seuls : 2610 (schéma en barres des parts, puis valeurs), 2614 (axe des minutes : forfait le moins cher A / B / C), 2620 (frise de la vie de Diophante).
- `figures_livre.py` : 0 chevauchement texte / trait, **aucune tolérance** (`TOLERE` vide) ; seules alertes : cotes à fond blanc (normal). Toutes ≤ 830 px. Après relecture : réponses vertes des cotes écrites sous la flèche (macro `\coteSous` ; le vert sur le gris du trait déclenchait le détecteur), étiquette $M$ décalée (elle touchait le trait de rappel de la cote), « clôture » placée contre la clôture, frise de Diophante allégée ; après les captures téléphone, balances, schéma en barres, frise des âges, triangle et rectangle, forfaits, route et segment resserrés (texte trop petit sur téléphone).

## Contrôles

- `verifier_notion.py` : **OK, 0 problème** (notes : 21 titres changés ; 0 image en ligne conservée). `verif_256.py` : 222 contrôles justes.
- Contrôle Chrome : avec `--navigateur`, le contrôle n'a pas abouti (Node bloqué, défaut connu de fermeture de Chrome) ; procédure de repli : vérificateur sans navigateur OK + `controle_apercu.mjs` avec captures, **130 vues sur 130 sans défaut** (cours, fiche, 21 exercices × 3 onglets, téléphone et ordinateur), deux fois (avant et après les dernières retouches). Seuls mes propres processus (verifier_notion et Node de la notion 256) ont été arrêtés, et seul mon verrou `chrome_1.lock` libéré (`chrome_0.lock` appartient à la notion 255 : laissé).
- Captures téléphone regardées : cours (4 écrans), fiche, exercices 2604, 2618 et 2619 (étapes). Corrections après relecture : figures trop larges resserrées (voir ci-dessus) ; espace insécable avant les unités (€, cm, g, km, ans, h, min… : 392 occurrences), car « € » passait seul à la ligne après une formule.

## Remarques pour l'orchestrateur

- 2612 utilise la double distributivité $(x + 4)(x - 2)$ : elle est au programme de 4e sur le site (notion 255, partie V), et les $x^2$ s'éliminent.
- Les cas « aucune solution » et « tous les nombres » sont présentés en remarque (cours) et travaillés en Découverte (2603) : extension naturelle du premier degré, sans exigence supplémentaire.
