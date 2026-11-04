# Notion 240 — Notion de fonction (3e)

**État : prêt** (agent-3e-C5, 2026-11-03).

## Cours et fiche

- **Titres** : « Fonctions : images et antécédents » → « Notion de fonction » (cours) et « Résumé : Notion de fonction » (fiche). `importer_v1.py` ne met à jour que le corps : `titres_docs.py` s'en charge à la publication.
- **Cours réécrit** : objectifs en liste ; I. définition, notation $f : x \longmapsto f(x)$, schéma « nombre → fonction → image », image / antécédent, à retenir (une image, 0, 1 ou plusieurs antécédents), erreurs ($f(3) \neq f \times 3$, « l'image » / « un antécédent ») ; II. méthodes image (substitution avec parenthèses) et antécédent (équation, vérification), exemple 0 / 1 / 2 antécédents avec $x^2$ ; III. tableau de valeurs (exemple, formule de tableur, tableau incomplet) ; IV. courbe représentative, propriété du point sur la courbe, méthodes de lecture d'image et d'antécédents, figure avec lectures en vert, lecture approchée / calcul exact ; V. modéliser (méthode en 3 points, exemple de la cuve, domaine).
- **Fiche refaite** : formule clé, tableau « on cherche / méthode » + exemples, figure de lecture, tableau de valeurs, tableur, modélisation, 4 erreurs classiques.

## Exercices (21)

- Tous relus et **réécrits** : énoncés à questions numérotées, corrigés avec méthode, étapes détaillées (calculs alignés), résultat encadré et **erreur fréquente** dans chacun ; `\displaystyle` retirés, fractions en `\dfrac` (lisibles sur téléphone).
- **Titres** « Type - Fonctions - n. Sujet » → « Type - Sujet » (21).
- **Remplacés (3)** :
  - 2280 « La fonction carrée plus un » (doublon du cours et de 2284) → « Découverte - Lire images et antécédents sur une courbe » (courbe en énoncé, lectures vertes au corrigé) ;
  - 2286 « Antécédents en série » (doublon de 2279) → « Entraînement - Du tableau de valeurs à la courbe » ($4 - x^2$ : tableau, tableur, tracé, pourquoi une courbe arrondie) ;
  - 2288 « Ce que ne dit pas un tableau » (doublon de 2276) → « Entraînement - Lecture graphique puis calcul exact » ($x^2 - 2x - 3$ : lecture, vérification, factorisation).
- **Retravaillés** : 2276 (tableau natif au lieu d'une image, question des deux antécédents de 5) ; 2277 (question « deux images ? ») ; 2278 (point $C(-3\ ;\ 7)$) ; 2279 (antécédent fractionnaire) ; 2281 (exemples qui justifient chaque réponse) ; 2282 (antécédents de 25) ; 2283 (vérification par la formule) ; 2287 (points de même abscisse / ordonnée) ; 2290 (tableau, antécédents de 10 et de 7) ; 2292 (retour à 50 m/min, instants à 300 m, conversion en km/h) ; 2293 (forme adaptée, antécédents de −12) ; 2294 (tableau de valeurs) ; 2295 (contexte réel, budget de 15 €).
- Progression : 7 Découverte, 7 Entraînement, 5 Problème, 2 **Type brevet** (2294, 2295).

## Figures (16 PNG, style livre, aucune ancienne image conservée)

- **Refaites (5 images en ligne)** : cours et fiche (lecture graphique), 2283 (ligne brisée), 2285 (deux droites), 2292 (promenade) ; l'image de 2288 (tableau) est remplacée par la courbe du nouvel exercice.
- **Retirée (1)** : 2276, tableau de valeurs en image → tableau natif (image supprimée à l'import).
- **Ajoutées** : schéma de fonction (cours) ; corrigés en vert de 2280, 2283, 2285, 2288, 2292 (droite $d = 300$, vitesses) ; programme de calcul 2282 (énoncé + corrigé avec expressions vertes) ; courbe de $4 - x^2$ (corrigé 2286) ; énoncés 2280 et 2288.
- Graduations placées à la main (`XLAB`) et graduations d'ordonnées coupées par une courbe retirées ; `figures_livre.py` : 0 chevauchement, 0 refus.

## Contrôles

- `verif_240.py` : **48 contrôles** sympy, tout juste.
- `verifier_notion.py --navigateur` : **OK, 0 problème**.
- `controle_apercu.mjs` (version finale, captures téléphone + ordinateur) : **130 vues, toutes à 0** (débordement, formules, `$` bruts, images, blocs, largeur). Une seconde passe `--navigateur` est restée bloquée à la fermeture de Chrome : vérificateur sans navigateur (OK) + `controle_apercu.mjs` seul, puis arrêt de mes seuls processus et verrous. Captures regardées : cours (parties I à IV), fiche, exercices 2282, 2286, 2292. Corrigé après captures : tableau du cours et de la fiche trop larges sur téléphone (resserrés), tableau de 2286 en colonne, schéma de fonction agrandi, figure de 2292 complétée pour la question 3.

## Remarques pour l'orchestrateur

- Exercice 2293 (produit nul) et 2288 Q4 recoupent la notion 237 « Équations » : gardés car classiques au brevet.
