# Notion 242 (3e) : Statistiques

**État : prêt** (agent-C6-242, 2026-11-03, session à heure limite 11 h 55 ; finition par agent-finition-242 le 2026-11-03 après-midi, voir la dernière section).

Programme du cycle 4 (3e) : effectifs, fréquences, effectifs cumulés ; moyenne simple et pondérée ; médiane ; étendue ; diagrammes en bâtons, histogrammes, diagrammes circulaires ; tableur ; comparaison de séries et lecture critique d'un graphique.

## Texte
- **Titres** : cours « Statistiques et représentations » → « Statistiques » ; fiche → « Résumé : Statistiques » (à appliquer avec `titres_docs.py`).
- **Cours 237** : réécrit et complété. I. Effectifs, fréquences (vocabulaire, propriété, effectif cumulé) ; II. Moyenne simple et pondérée (formule, exemple calculé en `aligned` avec tableau d'effectifs, piège de la moyenne des moyennes) ; III. Médiane (définition, méthode pair/impair, figure de la série rangée) et étendue, erreurs fréquentes ; IV. Bâtons, histogramme (données en classes), diagramme circulaire (méthode des angles) ; V. Tableur (MOYENNE, MEDIANE, MAX-MIN, SOMMEPROD) et comparaison de deux séries (figure) ; lecture critique ; à retenir.
- **Fiche 157** : réécrite (tableau des indicateurs, médiane en pratique avec figure, graphiques, tableur, 4 erreurs classiques).
- **Exercices (21, tous relus)** — progression : 7 Découverte, 7 Entraînement, 5 Problème, 2 Type brevet.
  - Titres « Type - Sujet » (nom du chapitre et numéros retirés).
  - **2337 réécrit** → « Type brevet - Quel joueur sélectionner ? » : données en tableau, calculs détaillés de chaque moyenne et médiane, figure de comparaison des deux séries, conclusion argumentée position + dispersion.
  - **2336** → « Type brevet - Le sondage du collège ».
  - **2334** : tableau de pluie en image → deux tableaux natifs (6 mois chacun, lisibles sur téléphone) ; question 3 (médiane) réécrite avec méthode, rangs, figure de la série rangée et piège de la série non rangée.
  - **2324** : le diagramme circulaire était dans l'énoncé (il donnait la réponse) → déplacé dans le corrigé, angles en vert.
  - **Erreur fréquente** ajoutée à chaque corrigé (encadré `attention` ciblé sur l'exercice, 21/21) ; « À retenir » en gras → encadrés `retenir`.
  - **Deuxième passe (11 h 35 – 11 h 43, demande de l'orchestrateur)** : corrigés développés au niveau de 2334/2337 (méthode, étapes détaillées sans saut de calcul, résultat rédigé, erreur fréquente) pour **toutes les Découverte (2317 à 2323)**, **toutes les Entraînement (2324 à 2330)**, et pour 2331, 2333, 2335, 2336. Solutions courtes harmonisées (formules en `$…$`). 2326 : formules de tableur en code (plus d'entité HTML `&#42;`). Ancienne ligne « **Erreur fréquente :** » en double dans 2332 fusionnée dans l'encadré.
  - Pas de doublon franc : 2317/2318 (série brute / groupe en contexte) et 2328/2335 (note manquante / objectif sur 6 contrôles) travaillent des situations différentes ; conservés.
  - Aucune erreur de calcul dans les résultats en ligne.
- `verif_242.py` : **95 contrôles sympy exacts OK** (cours, fiche, figures et tous les calculs ajoutés dans les corrigés développés).

## Figures
- **16 figures neuves** (TikZ, style livre) pour **20 positions** ; les 11 appels d'images en ligne (matplotlib) sont tous remplacés ; **0 conservée**.
  - Cours (5) : diagramme en bâtons, série rangée avec médiane en vert, histogramme, diagramme circulaire, comparaison de deux séries. Fiche (3) : bâtons, médiane, circulaire.
  - Exercices : 2322 (bâtons, énoncé + corrigé vert), 2323 (tableau d'effectifs + effectifs cumulés en vert), 2324 (circulaire, corrigé), 2325 (histogramme), 2326 (feuille de tableur), 2332 (graphique trompeur, axe à 78 / axe à 0), 2334 (série rangée, médiane en vert), 2336 (tableau à compléter + circulaire en vert), 2337 (comparaison des deux joueurs, étendues en vert).
- Détecteur texte/trait : 0 erreur. Toutes ≤ 900 px. Chaque planche regardée.

## Contrôles
- `verifier_notion.py --navigateur` : **OK, 0 problème** (après correction d'une formule de tableur trop large sur téléphone dans le cours, coupée en deux morceaux de code).
- Captures `controle_apercu.mjs` dans `captures/`. Vues regardées sur téléphone : cours (partie III–IV), exercices 2334 et 2337 (étapes). Corrections faites après ces vues : total de 2334 (somme de 12 termes coupée sur téléphone) découpé en deux semestres ; série rangée de 2334 sur deux lignes ; figures de comparaison (cours, 2337) resserrées, noms des séries au-dessus des points (plus lisibles sur téléphone, 2337 désormais ≤ 900 px).
- Dernier passage `verifier_notion.py --navigateur` à 11 h 34 : **OK, 0 problème**.
- Après la deuxième passe : `verifier_notion.py` sans navigateur **OK** (11 h 46) ; avec `--navigateur`, Chrome est resté bloqué à la fermeture (« contrôle navigateur en échec » avec tous les compteurs à 0, cas connu, 2 autres agents sur Chrome) → contrôle refait avec `controle_apercu.mjs --rapide` (11 h 52) : **130 vues (65 téléphone, 65 ordinateur), 0 débordement, 0 erreur de formule, 0 élément trop large, 0 image manquante**, aucune erreur console. Le script s'est terminé avec le code 1 à la fermeture de Chrome (même blocage), après les 130 vues ; aucun processus de contrôle de cette notion ne tourne encore. Les verrous `chrome_*.lock` sont libérés par le script ou expirent seuls après 15 min.
- Faute de temps, les captures téléphone des corrigés de la deuxième passe n'ont pas été regardées à l'œil (le mode rapide n'en produit pas ; les captures de `captures/` datent de 11 h 29) : à regarder par l'orchestrateur avant import si possible (2323, 2325, 2326 en priorité).

## Remarques pour l'orchestrateur
- Appliquer les nouveaux titres du cours et de la fiche (`titres_docs.py`).
- Corrigés encore à enrichir lors d'une prochaine passe (justes et structurés, mais quelques étapes d'une ligne) : 2332 (graphique trompeur) et les questions 2 et 5 de 2334.
- Scripts et fichiers de travail laissés dans le dossier : `maj_exercices.py`, `ajout_erreurs.py`, `remplacer_bloc.py`, `remplacer_etapes.py`, `nouveau_*.txt`, `etapes_*.txt` (sans effet sur l'import).

## Finition 2026-11-03 (agent-finition-242, après-midi)

Sauvegarde avant travaux : `sauvegardes/242F_exercices_avant_finition.txt`. Aucun bloc supprimé, aucune ligne `Id:` modifiée (21 Id identiques), aucune écriture en base.

**Corrigés demandés**
- **2332 (graphique trompeur)** réécrit : méthode à chaque question, étapes détaillées (hausse 84 − 80 = 4, taux 4/80 = 5 % ; hauteurs visibles 2 et 6 ; rapport visuel 6/2 = 3 comparé au rapport réel 84/80 = 1,05 ; vérification sur le graphique à axe 0), résultats rédigés, erreur fréquente + « À retenir ». **Nouvelle figure de corrigé** `ex2332_corrige.png` (position 2) : les deux graphiques complétés en vert (hauteurs visibles 2 et 6 fléchées, valeurs 80 et 84, « rapport visuel 6 ÷ 2 = 3 » / « rapport réel 84 ÷ 80 = 1,05 »). Solution courte précisée.
- **2334** : questions 2 (moyenne : méthode, rappel du total, division 646/12 = 53,833…), 4 (étendue : méthode, extrêmes juillet/novembre, calcul) et 5 (méthode, liste des 5 mois, 5/12 = 0,416… ≈ 42 %) au niveau de la question 3 ; l'encadré de la question 3 titré « Erreur fréquente ».

**Autres corrigés enrichis (étapes d'une ligne ou questions sans étape)** : 2317 (Q1, Q2, Q5 en liste), 2318 (Q3, Q4), 2320 (Q1, Q4 en deux étapes), 2321 (Q1, Q3 avec positifs/négatifs, Q5), 2322 (Q2 tableau natif, Q3, Q5), 2323 (Q2 : produits en liste), 2324 (Q4), 2325 (Q1, Q3, Q4 en 4 étapes, Q5), 2326 (Q2), 2327 (Q1, Q2, Q4, Q5 avec l'exemple de deux groupes de 15 ; solution harmonisée), 2328 (Q2, Q4, Q5), 2329 (Q4), 2330 (Q1, méthodes Q2–Q4), 2331 (Q4, Q5 en listes), 2333 (Q1, Q4), 2335 (méthodes Q2–Q5), 2336 (Q3, Q5), 2337 (Q1, Q2, Q4 ; erreur fréquente ajoutée, l'ancien encadré de Q2 devient une remarque). Majuscules d'insistance (TOUJOURS, SOMMES, ORDRE…) remplacées par du gras. 21/21 corrigés ont leur encadré « Erreur fréquente ».

**Vue téléphone** (captures `controle_apercu.mjs` régénérées, les 21 corrigés regardés à l'œil, priorité 2323, 2325, 2326 puis Découverte 2317–2323). Défauts trouvés et corrigés :
- formules **coupées** (défilement) : 2330 Q1 (somme de 5 salaires → paires), 2333 Q1 (sommes de 9 et 10 notes → paquets) ; formules **réduites** : 2325 Q4 (moyenne pondérée → 4 étapes), 2337 Q1 (total puis moyenne) ; « = » orphelin en début de ligne dans 2337 Q2 ;
- tableau coupé dans 2325 Q1 (5 colonnes) → tableau vertical ;
- unité « € » isolée en début de ligne dans 2330 → `\text{€}` dans la formule ;
- figures réduites et texte trop petit sur téléphone : tableaux 2323 (énoncé et corrigé) et 2336 (énoncé) resserrés (≤ 680 px, chiffres plus grands, en-têtes sur deux lignes), série rangée de 2334 resserrée (630 px, « rang » au-dessus), diagramme circulaire 2336 (étiquettes sur deux lignes, 597 px) ; angles et pourcentages des diagrammes circulaires (2324, 2336, cours/fiche) et étendues de 2337 écrits dans la police des figures (plus lisibles). Chaque PNG regardé ; détecteur texte/trait : 0 erreur.

**Contrôles**
- `verif_242.py` : **163 contrôles sympy OK** (95 + 68 nouveaux : tous les calculs ajoutés ou modifiés).
- `verifier_notion.py --navigateur` (16 h 42) : **OK, 0 problème** (Chrome ne s'est pas bloqué cette fois). Deux contrôles avec captures (16 h 24 et 16 h 37) : 130 vues, 0 défaut ; ces deux processus étant restés bloqués à la fermeture de Chrome après les 130 vues, seuls mes propres processus ont été arrêtés et leurs verrous libérés.
- Les captures de `captures/` datent de 16 h 37 : les derniers ajustements (hauteur des lignes du tableau 2323, étiquettes du circulaire 2336, méthodes de 2330) sont postérieurs, vérifiés sur les PNG et par le contrôle navigateur de 16 h 42.

**Pour l'orchestrateur** : la notion est déjà en ligne ; ré-importer 242 pour publier la finition (nouvelle position d'image 2 dans 2332 déclarée dans `correspondance.json` ; figures modifiées : ex2323_enonce, ex2323_corrige, ex2324_corrige, ex2332_corrige (nouvelle), ex2334_corrige, ex2336_enonce, ex2336_corrige, ex2337_corrige, cours_circulaire). Le ré-export préalable (fait par `publier_lot.ps1`) est nécessaire : `source_en_ligne/` date d'avant le premier import.
