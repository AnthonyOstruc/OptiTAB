# Notion 241 — Fonctions linéaires et affines (3e)

**État : prêt** (agent-3e-C6, 2026-11-03).

## Cours et fiche

- **Titres** inchangés (déjà l'intitulé de la notion) : « Fonctions linéaires et affines » et « Résumé : Fonctions linéaires et affines ».
- **Cours réécrit** : objectifs en liste ; I. fonction linéaire (définition, lien proportionnalité, méthode « une image suffit »), pourcentages = coefficients multiplicateurs (hausse / baisse, retrouver un prix initial) ; II. fonction affine (coefficient directeur, ordonnée à l'origine, cas linéaire et constant, erreur « affine = proportionnelle ») ; III. représentation graphique (propriété, méthode de lecture de $a$ et $b$, figure avec lectures en vert, sens de la droite, droites parallèles) ; IV. accroissements proportionnels, méthode des deux points, exemple rédigé et contrôlé, erreur d'ordre ; V. comparer deux tarifs (méthode en 4 points, point d'intersection, exemple, erreur fréquente) ; à retenir.
- **Fiche refaite** : tableau des deux familles, figure de lecture, tableau des pourcentages, formule des deux points, comparaison de tarifs, 4 erreurs classiques. `\displaystyle` retirés.

## Exercices (21)

- Tous relus et **réécrits** : questions numérotées, corrigés avec méthode, étapes détaillées (calculs alignés), résultat encadré et **erreur fréquente** dans chacun ; titres « Type - Fonctions… - n. » → « Type - Sujet ».
- **Remplacés (3)** :
  - 2301 « Un tableau de valeurs » (calculs d'images, doublon de 2298) → « Découverte - Proportionnalité et fonction linéaire » (prix du carburant, tableau, coefficient, droite par l'origine en figure) ;
  - 2308 « Par deux points, encore » (doublon de 2304) → « Entraînement - Pourcentages et fonctions linéaires » (hausse 20 %, baisse 15 %, prix initial, évolutions successives) ;
  - 2315 « La course de taxis » (3e comparaison de tarifs, doublon de 2310/2316) → « Type brevet - Soldes et coefficients multiplicateurs » (remise 30 %, prix initial, deux remises successives = 44 %).
- **Retravaillés** : 2297 (question « point sur la droite » au lieu d'une question vague) ; 2299/2300 (tracé + contrôle, figure au corrigé) ; 2306 (droite à lire en énoncé, lectures vertes au corrigé) ; 2307 (erreur de signe sur la parenthèse) ; 2309 (tableau de valeurs en image → tableau natif, nouvelles valeurs cohérentes, piège « régulier ≠ proportionnel ») ; 2311 (conversion en min/s) ; 2312 (longueur linéaire / aire en $k^2$) ; 2313 (ajout de la seconde image pour conclure) ; 2314 (arrondi à l'entier inférieur, cas d'égalité $d = 5$) ; 2316 (vélos, version brevet avec graphique en énoncé et lecture graphique + calcul).
- Progression : 7 Découverte, 7 Entraînement, 5 Problème, 2 **Type brevet** (2315, 2316).

## Figures (11 PNG, style livre, aucune ancienne image conservée)

- **Refaites (7 images en ligne)** : cours et fiche (droite $2x - 3$ avec $b$ et le pas « +1, +2 » en vert), 2299 (droite linéaire, déplacée dans le corrigé), 2300 (droite affine, corrigé), 2306 (énoncé + corrigé vert), 2307 (droites parallèles, déplacée dans le corrigé pour ne pas donner la réponse), 2310 (deux abonnements, intersection $(6\ ;\ 38)$ en vert, au corrigé).
- **Retirée (1)** : 2309, tableau en image → tableau natif (image supprimée à l'import).
- **Ajoutées** : 2301 (proportionnalité, points du tableau sur une droite par l'origine), 2308 (pourcentages $1{,}2x$ et $0{,}85x$, lectures vertes), 2316 énoncé (graphique des deux formules) et corrigé (intersection $(5\ ;\ 20)$ et droite du budget de 22 € en vert).
- `figures_livre.py` : 11/11 produites, 0 refus ; un avertissement résiduel (fond blanc d'une étiquette de 2308 près d'un pointillé, normal pour une valeur lue). Graduations coupées par une droite retirées (repères lisibles par le quadrillage).

## Contrôles

- `verif_241.py` : **32 contrôles** sympy (cours, fiche, 21 exercices), tout juste.
- `verifier_notion.py` (sans navigateur, version finale) : **OK, 0 problème** ; 12 placements de figures neuves, 0 image en ligne conservée, 1 image non appelée (tableau de 2309) supprimée à l'import ; 21 titres changés.
- `controle_apercu.mjs` (version finale, captures téléphone + ordinateur) : **130 vues, toutes à 0** (débordement, formules, `$` bruts, images, blocs, largeur). Comme pour la notion 240, Chrome est resté bloqué à la fermeture après la dernière vue : arrêt de mes seuls processus et de mon seul verrou (`chrome_1.lock`). Une première passe `--navigateur` lancée avant les dernières retouches a été arrêtée (périmée).
- Captures regardées : cours (partie III–IV, figure de lecture), fiche, exercice 2316 (étapes avec figure). Retouches faites après relecture des figures : graduations coupées par une droite retirées (cours, 2300, 2306, 2307), étiquettes déplacées (2306, 2308, 2316), étiquette ambiguë « (5 ; 20) » retirée de 2316 (les pointillés verts suffisent, la valeur est dans le texte).

## Remarques pour l'orchestrateur

- 2312 (agrandissement) touche aussi la notion « Grandeurs et mesures » : gardé car il illustre « linéaire / non linéaire ».
