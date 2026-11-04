# Rapport — 153 Suites numériques (Première spécialité)

**État : prêt** (format v1, figures au style des livres, contrôles passés).

## Programme (2019)

Contenus vérifiés : modes de génération (explicite, récurrence, algorithme, motif, dénombrement), sens de variation, suites arithmétiques et géométriques (terme général, sommes 1 + … + n et 1 + q + … + qⁿ, modélisation linéaire / exponentielle), approche **intuitive** du comportement quand n devient grand (conjecture seulement), algorithmes (termes, sommes, seuil, factorielle, Fibonacci). Retiré partout comme hors programme : notation et calculs de limites, logarithme, raisonnement par récurrence, « monotone et majorée donc convergente », dérivée et caractère attractif/répulsif d'un point fixe, symbole Σ.

## Texte

- **Cours** : restructuré (définitions, théorèmes, 4 démonstrations du programme en encadrés `demonstration`, méthodes « montrer qu'une suite est arithmétique / géométrique », évolutions à taux constant, construction en escalier, algorithmes terme + seuil, partie V en conjecture sans notation de limite).
- **Fiche** : tableau comparatif arithmétique / géométrique, méthodes, sommes, pièges.
- **Exercices** : les 21 corrigés réécrits au format méthode / étapes / résultat (+ « attention » quand utile) ; tout vérifié par `verif_suites.py` (93 contrôles).

### Remplacements (contenu nouveau dans le bloc existant)
- **1351 DS Type 1** : était un doublon de 1349 avec limites → suite explicite (variations), rebonds d'une balle (géométrique, distance totale), seuil en Python.
- **1352 DS Type 2** : doublon de 1350 avec limites → amphithéâtre (arithmétique, somme), ville à −2 %/an (géométrique, seuil), comparaison linéaire / exponentielle.
- **1362 Type examen 2** : portait entièrement sur le second degré (hors notion) → contrats de salaire A (+1 000 €) / B (+4 %), sommes sur 10 ans, seuil Python.
- **1361 Type examen 1** : exercice 2 trivial (v₀ = 2 point fixe : suite constante) et usage de ln → v₀ = 1, suite auxiliaire, variations ; seuil par calcul de puissances et Python.
- **1355** (titre changé : « Comportement quand n devient grand ») : techniques de limites de Terminale → conjectures sur tableaux de valeurs, seuils.
- **1347** : limite, récurrence et convergence monotone → club d'adhérents u_{n+1} = 0,8uₙ + 40 (fonctions `terme`, `liste`, `seuil`) + factorielle.
- **1425** : f'(1) et limites retirés ; u₀ = 1,5 (au lieu de 0,5, dont l'escalier se superposait aux axes) ; seuil u_n > 1 000.
- **1424, 1349, 1350, 1363, 1364** : limites / récurrence / Σ retirés (conjecture, écart à la valeur d'équilibre, suite auxiliaire donnée, seuils) ; tableau d'exécution de 1363 clarifié (u au début, S à la fin du passage).
- **1353** : était un doublon de 1354 → notations u_{n+1} / u_n + 1 / u_{2n}, preuves « arithmétique / géométrique » pour tout n, contre-exemple.

### Ajout
- **nouveau-1 « Découverte - Suites Numériques - Motifs et Dénombrement »** : motif d'allumettes (aₙ = 3n + 1) et poignées de main (pₙ = n(n − 1)/2) — capacité du programme non travaillée jusqu'ici.

## Figures

- 11 figures neuves (`figures/figures.py`), toutes regardées : 3 refaites pour les 3 images du cours (nuage, somme de Gauss, escalier), 2 ajoutées au cours (arithmétique, géométrique), fiche : 3 (réutilisées), 1424 : 2 (énoncé + corrigé, remplace l'image matplotlib), 1425 : 1 (remplace l'image matplotlib), 1349, 1362, nouveau-1 : 1 ajoutée chacun.
- 0 conservée ; les anciennes images (matplotlib, style non livre) sont toutes remplacées.

## Contrôles

- `verif_suites.py` : 93 vérifications OK.
- `verifier_notion.py --navigateur` : OK, aucun problème (0 image en ligne conservée).
- `controle_apercu.mjs` : aucun problème (débordement 0, formules 0). Vues regardées au téléphone : cours (parties I à IV), fiche, exercices 1354 (énoncé), 1351 (étapes), figures une à une. Corrections faites après relecture : code Python sorti des listes (1354, 1347), exemples du cours passés en formule centrée (ponctuation isolée en début de ligne), tableau de la fiche (trop large au téléphone) remplacé par deux encadrés, figure de la somme de Gauss resserrée (légende sous la grille).

## Remarques pour l'orchestrateur

- La construction en escalier (« toile d'araignée ») n'est pas explicitement au programme mais relève du registre graphique ; elle est présentée comme méthode de représentation, sans théorie du point fixe.
- `\gt` / `\lt` n'existent pas dans le préambule TikZ de `figures_livre.py` (macros du site seulement) : utiliser `>` `<` dans les figures.

## Finition 2026-11-02

**État : prêt** (mise en conformité avec les consignes du 2026-11-02 : figures partout où elles aident, titres).

### Titres
- Cours : « Suites numériques, modèles discrets » ; fiche : « Résumé : Suites numériques, modèles discrets ».
- 22 titres d'exercices : nom du chapitre retiré, majuscules abusives supprimées, préfixe de type gardé. Les « Type 1/2/3 » (DS, Type examen) reçoivent un titre qui dit leur contenu (ex. « DS - Variations, rebonds d'une balle et seuil »). 1424 et 1425 : « point fixe répulsif » (vocabulaire hors programme) remplacé par « Construction en escalier : une suite qui se rapproche / qui s'éloigne ».

### Figures (18 nouvelles, toutes regardées, 0 chevauchement)
- Cours V et fiche IV : `cours_seuil` (nuage du capital 1 000 × 1,03ⁿ, seuil 2 000 €, premier rang 24).
- Énoncés : 1351 (rebonds de la balle), 1425 (repère courbe de f et y = x à compléter ; la figure n'existait que dans le corrigé).
- Corrigés : 1342 (quatre « marches » de t₃ à t₇), 1343 (alternance du signe, q = −2), 1344 (somme de Gauss, figure du cours), 1347 (club, seuil 190 atteint en n = 11), 1348 (minimum w₂ = −4), 1350 (deux départs de part et d'autre de l'équilibre 600), 1351 (nuage avec minimum u₃ = −4 ; trajectoire complétée, contacts 1 à 6 et distance D), 1352 (deux villes : seuil n = 12, croisement n = 14), 1355 (tₙ → 2 et (−1)ⁿ), 1356 (rectangle d'aire 2 : il manque 1/16), 1361 (bactéries, seuil 10 000 en n = 7), 1364 (épargne avec / sans intérêts : 14 et 16 mois), nouveau-1 (motif 4 avec les 3 allumettes ajoutées en vert ; poignées de main p₅ = p₄ + 4, demandé : l'énoncé avait une figure, pas le corrigé).
- Sans figure (choix assumé, calcul pur ou programme) : 1354, 1353, 1346, 1345, 1363.

### Exercices réécrits
- 1361, question 1.2 : doublon exact de 1356 Q2 (u₀ = 5, r = 3, S = 220) → raison à partir de u₁ = 4 et u₆ = 19, u₂₀ = 61, S = u₁ + … + u₂₀ = 650 (piège des « pas » signalé).

### Contrôles
- `verif_suites.py` : 121 vérifications justes (28 nouvelles : question réécrite, chaîne 1351 A2, toutes les valeurs écrites sur les figures).
- `verifier_notion.py` : OK, 0 problème (33 nouvelles figures, 0 image en ligne conservée). Avec `--navigateur`, toutes les vues passent mais `controle_apercu.mjs` reste bloqué à la fermeture de Chrome (défaut connu) : contrôle relancé à part avec délai maximal, mon seul processus arrêté et son verrou libéré.
- `controle_apercu.mjs` (captures) : 136 vues sur 136 sans défaut (téléphone et ordinateur : débordement 0, formules 0, images 0).
- Formules coupées (non détectées par l'outil) : contrôle complémentaire au téléphone (largeur des formules mesurée dans Chrome, script de travail hors du dépôt) + captures regardées (cours V, fiche, 1351, 1364). Corrigé : 1351 A2 (chaîne de calcul trop large, redécoupée en deux temps), 1364 B2 et 1363 A1 (tableaux en ligne à 4 et 7 colonnes coupés au téléphone → tableaux en colonnes). Résultat final : 0 formule trop large.

### Remarque pour l'orchestrateur
- L'exercice `nouveau-1` a déjà été créé en production à l'import du matin (Id **4602**, voir `sauvegardes/avant_import_20261102-083531.json`), mais le fichier garde `Id: nouveau-1` et `meta.json` ne le connaît pas : ré-exporter la notion (ou remplacer la clé par 4602 dans `exercices.txt` et `correspondance.json`) **avant** le prochain import, sinon l'exercice sera créé une seconde fois.
