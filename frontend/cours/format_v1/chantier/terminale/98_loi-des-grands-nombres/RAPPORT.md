# Rapport — Terminale, notion 98 « Loi des grands nombres »

## État
**Prêt.** `verifier_notion.py --navigateur` : OK (0 problème) ; aucune formule centrée réduite ni coupée sur téléphone
(contrôle complémentaire de chaque formule à 390 px).

## Texte
- **Cours 98** complété, conforme au programme officiel (BO 2026, « Concentration, loi des grands nombres ») :
  Bienaymé-Tchebychev (forme équivalente, écarts en kσ, exemple binomial avec la valeur exacte) ; nouvelle partie
  « Échantillon et variable moyenne » (E(Mₙ), V(Mₙ), σ/√n, fréquence) ; concentration avec démonstration ; loi
  faible avec démonstration (gendarmes) ; taille d'échantillon, majoration p(1−p) ≤ 1/4 démontrée, exemple de sondage ;
  estimation signalée « Pour aller plus loin » (approfondissement du programme) ; simulation Python (exemple
  d'algorithme du programme).
- Correction : l'inégalité de concentration était présentée comme « démonstration au programme » (le programme
  n'en liste pas) → simple démonstration.
- **Fiche 42** réécrite (formules, méthode de taille d'échantillon, 4 pièges).
- **Exercices** (titres, Id, difficultés inchangés), virgules décimales `{,}` partout, corrigés restructurés :
  - 824 Q2 (roulette) : **erreur corrigée** — l'intervalle [0,024 ; 0,031] n'est pas centré sur p = 1/37 ; δ = 0,004
    était faux → δ = 1/37 − 0,024 ≈ 0,003 03, minoration 0,713 (et non 0,836) ; valeur exacte binomiale ≈ 0,965 signalée ;
  - 825 Q1/Q5 et 824 Q5 : bornes d'intervalles arrondies **vers l'extérieur** (sinon la garantie est perdue) ;
  - 825 Q3 : formulation fausse (« probabilité que le poids moyen réel soit… », μ n'est pas aléatoire) → reformulée ;
  - 825 Q4 : variance estimée par p̂ (non rigoureux) → majoration p(1−p) ≤ 1/4 : intervalle [0,55 ; 0,65] ;
  - 823 Q3 : variance exacte 35/12 (au lieu de 2,92 arrondi) ; 822 Q3 : traduction de l'événement corrigée ;
    822 Q4 : « inégalité de concentration » employée à tort → forme équivalente de Bienaymé-Tchebychev ;
  - 821 Q3 : justification par l'inégalité de concentration (au lieu de « écart acceptable »).
- Piège trouvé à la vérification : un test sur des fréquences décimales (`abs(f - 0.5) >= 0.1`) excluait les cas limites
  (0.6 − 0.5 = 0.0999…) ; programme du cours écrit avec des entiers, et encadré « attention » ajouté.

## Vérifications
`verif_lgn.py` : tous les résultats (fractions exactes, lois binomiales exactes via scipy), tailles minimales d'échantillon
par recherche entière, simulation du cours exécutée 200 fois (moyenne 0,057 = valeur exacte), données des figures. OK.

## Figures
2 refaites (anciennes images matplotlib, texte minuscule) : `bt_binomiale`, `lgn_convergence` (cours ; la fiche réutilise
la seconde, l'ancienne image 1 de la fiche n'est plus appelée → supprimée à l'import). 1 ajoutée dans un corrigé :
`roulette_intervalle` (exercice 824). Aucun texte sur un trait, largeurs ≤ 900 px, chaque PNG relu.

## Vues regardées
Cours en téléphone (parties 2 et 4), étapes de l'exercice 823 ; corrigé puis recontrôlé.

## Remarques pour l'orchestrateur
- `controle_apercu.mjs` ne signale pas les formules centrées qui défilent (`mjx-container.mjx-scrollable` est exclu) :
  14 chaînes d'équivalences étaient coupées sur téléphone dans les étapes sans aucune alerte. Elles sont désormais
  écrites en `aligned` (une équivalence par ligne). Ce contrôle mériterait d'être ajouté à l'outil.

## Finition 2026-11-02

**État : prêt** (sauvegardes des trois fichiers avant finition dans `sauvegardes/*_avant_finition_20261102.txt`).

### Titres
- Cours « Concentration, loi des grands nombres » et fiche « Résumé : Concentration, loi des grands nombres » (intitulé officiel ; était « Concentration et loi des grands nombres »).
- 5 titres d'exercices sans « Loi des Grands Nombres » ni majuscules abusives : 821 « Découverte - Fréquences et moyennes qui se stabilisent », 822 « Entraînement - Inégalité de Bienaymé-Tchebychev », 825 « Entraînement - Encadrer une moyenne ou une proportion inconnue » (l'ancien « Intervalles de confiance » annonçait une notion hors programme), 823 « Entraînement - Taille d'échantillon suffisante », 824 « Problème - Production, roulette et mesures ».

### Exercices
- **821 Q4 réécrite** : l'ancienne question (moyenne « théorique » d'un élève sur 5 puis 50 contrôles) était faible et peu rigoureuse (notes non indépendantes). Remplacée par la lecture d'une simulation de 1 000 lancers (figure) + majorants de P(|Fₙ − 0,5| ≥ 0,1) par l'inégalité de concentration : 0,5 pour n = 50 et 0,025 pour n = 1 000, comparés à la figure ; encadré « attention » (une simulation illustre, ne démontre pas).
- 822 Q3 : on montre que [4,5 ; 5,5] est centré en μ = 5 (δ = 0,5) avant de traduire l'événement.
- 823 Q1 : contrôle graphique ajouté (courbe de n ↦ 25/n sous la droite y = 0,05 dès n = 500). 823 Q3 : E(X²) mis en formule centrée (un « . Donc » commençait une ligne au téléphone).
- 825 Q4 : étape « Pourquoi p(1−p) ≤ 1/4 » (p(1−p) = 1/4 − (p − 1/2)²) avec la parabole.
- Formules réduites au téléphone découpées en `aligned` : 825 Q2 et Q5, 824 Q1, Q2 et Q5.
- Les autres questions sont justes et au programme : inchangées.

### Figures (11 fichiers, 12 emplacements)
- **Revérifiées (3)** : `bt_binomiale` et `roulette_intervalle` conservées telles quelles (justes, aucun chevauchement) ; `lgn_convergence` retouchée : l'étiquette « p = 0,5 » collait presque à la fin des courbes → décalée.
- **Ajoutées (8, énoncé + corrigé complété en vert)** : `ex821_simulation` / `_corrige` (fréquence d'une simulation, graine 2 ; bande verte ]0,4 ; 0,6[) ; `ex822_boulons` / `_corrige` (droite graduée, zones orange L < 4,5 et L > 5,5 ; μ = 5 et δ = 0,5 en vert) ; `ex823_majorant` / `_corrige` (25/n et y = 0,05 ; point (500 ; 0,05) et n ⩾ 500 en vert) ; `ex825_parabole` / `_corrige` (y = p(1−p) sous y = 1/4 ; sommet (1/2 ; 1/4) en vert).
- Corrections pendant la fabrication : 2 étiquettes sur une courbe refusées par le détecteur (« n ⩾ 500 », « y = p(1−p) ») → déplacées ; « y » collé à la graduation 0,15 → graduation retirée ; figure des boulons trop large (texte trop petit au téléphone) → resserrée, phrase du bas retirée (elle est dans le texte).
- 824 : pas de figure dans l'énoncé, volontairement : elle donnerait la réponse de la question 2 (intervalle non centré).
- `figures_livre.py` : 11/11, 0 refus. Chaque PNG regardé.

### Contrôles
- `verif_lgn.py` : tout est vérifié, avec en plus des contrôles sympy pour chaque calcul nouveau (majorants 0,5 et 0,025 ; 25/n ⩽ 0,05 ⟺ n ⩾ 500 ; p(1−p) = 1/4 − (p − 1/2)², sommet ; δ = 0,5) et la lecture de la simulation (dernière sortie de la bande avant n = 100, début entre 0,27 et 0,53, f₁₀₀₀ ≈ 0,5).
- `verifier_notion.py --navigateur` : OK, 0 problème (12 nouvelles figures, 0 image en ligne conservée, 1 ancienne image de fiche non appelée → supprimée à l'import). Chrome s'est fermé normalement.
- `controle_apercu.mjs` avec captures : aucun problème. Captures téléphone regardées : 821 (énoncé, étapes), 822, 823, 824 et 825 (étapes).
- Point restant (mineur) : `roulette_intervalle` (824) est large ; au téléphone son texte est petit mais lisible. À resserrer lors d'une prochaine passe si besoin.

## Enrichissement 2026-11-02

**État : prêt** (non importé). 5 → **11 exercices** : 6 blocs ajoutés à la fin de `exercices.txt` (`Id: nouveau-1` à `nouveau-6`). Les 5 exercices existants sont identiques à l'octet près (comparés à `sauvegardes/exercices_avant_enrichissement_20261102.txt`). Sauvegardes : `sauvegardes/*_avant_enrichissement_20261102.*` (exercices, figures.py, correspondance.json, verif_lgn.py).

**Attention (corrigé pendant l'enrichissement)** : le dernier exercice existant (824) n'était pas fermé par une ligne `===`. Le premier bloc ajouté était donc lu comme la suite de 824. Une ligne `===` a été ajoutée après la solution de 824 (son contenu n'a pas changé).

### Exercices ajoutés
| Id | Titre | Difficulté | Compétence |
|---|---|---|---|
| nouveau-1 | Découverte - Bienaymé-Tchebychev pour une loi connue | easy | E, V, σ par les définitions ; majorants 0,525 et 7/30 comparés aux valeurs exactes 0,3 et 0,1 ; minoration P(1 < X < 5) ≥ 0,475 (exacte 0,7) ; δ = 1 < σ : majorant 2,1, aucune information |
| nouveau-2 | Entraînement - Inégalité de concentration pour un gain moyen | medium | Gain journalier (E = 0,3, V = 3,61) ; E(Mₙ), V(Mₙ) ; majorants 0,401 (n = 100) et 0,040 (n = 1 000) ; inclusion (M ≤ 0) ⊂ (\|M − 0,3\| ≥ 0,3) ; δ = 0,27 et gain total entre 30 et 570 euros à 95 % |
| nouveau-3 | Entraînement - Simulation et loi faible des grands nombres | medium | Programme Python (roue p = 0,2) ; test entier \|20s − 4n\| ≥ n et piège des décimaux ; tableau simulé comparé aux majorants 64/n ; loi faible des grands nombres ; roue suspecte (254 rouges sur 1 000) |
| nouveau-4 | Problème - Taille d'échantillon et coût d'un sondage | hard | p(1 − p) ≤ 1/4 ; n ≥ 2 000 (6 000 €), n ≥ 8 000 pour une précision deux fois meilleure ; budget 4 500 € → δ = 0,058 ; information p ≤ 0,1 : p(1 − p) ≤ 0,09, n ≥ 4 500 au lieu de 12 500 |
| nouveau-5 | Problème - Bienaymé-Tchebychev face à la loi binomiale | hard | X ~ B(50 ; 0,2) : majorant 0,32 contre valeur exacte ≈ 0,109 ; intervalle à 95 % : 0 ≤ X ≤ 22 (Bienaymé-Tchebychev, δ = 13) contre 5 ≤ X ≤ 15 (binomiale, δ = 6) ; intérêt d'une inégalité universelle |
| nouveau-6 | Type examen - Jeu en ligne : binomiale et concentration | hard | Sujet type bac en 3 parties : arbre, probabilités totales P(G) = 0,3, P_G(F) = 0,8 ; B(20 ; 0,3), P(X = 6) ≈ 0,192, P(X ≥ 10) ≈ 0,048, minoration 0,737 5 contre 0,917, T = 6X − 20 ; E(Y) = 0,8, V(Y) = 7,56, n ≥ 237 parties |

Chaque exercice : énoncé avec contexte et questions numérotées ; corrigé « méthode / étapes / résultat » avec erreurs fréquentes (`attention`) et `retenir` ; solution courte. Toutes les valeurs binomiales sont calculées (scipy) dans `verif_lgn.py`, jamais recopiées.

### Figures (11 nouvelles, style livre, `figures_livre.py` : 11/11, 0 refus)
- Énoncé (ne donnent pas la réponse) : `n1_loi` (loi des colis), `n2_loi` (loi du gain), `n5_loi` (B(50 ; 0,2)).
- Corrigé, complétées en vert : `n1_ecarts_corrige` (écarts ≥ 2 en orange, P = 0,3 ≤ 0,525) ; `n2_intervalle_corrige` (M ≤ 0 et intervalle ]0,03 ; 0,57[) ; `n3_comparaison_corrige` (simulation et majorants 64/n) ; `n4_parabole_corrige` (p(1 − p) ≤ 0,09 si p ≤ 0,1) ; `n5_ecarts_corrige` (P ≈ 0,109 contre 0,32) ; `n5_intervalles_corrige` (0 ≤ X ≤ 22 contre 5 ≤ X ≤ 15) ; `n6_arbre_corrige` (arbre et chemins vers G) ; `n6_loi_corrige` (B(20 ; 0,3), P(3 ≤ X ≤ 9) ≈ 0,917).
- Retouches après les captures téléphone : diagrammes resserrés (6 à 6,4 cm) et notes en 10,5 pt pour rester lisibles ; droite graduée de n2 ramenée sous 900 px ; étiquettes décollées des axes.
- Clés `nouveau-1` à `nouveau-6` ajoutées dans `figures/correspondance.json` (alt descriptifs).

### Contrôles
- `verif_lgn.py` : nouvelle section « Enrichissement 2026-11-02 » (une partie par exercice + données des figures), 56 contrôles (fractions exactes, sympy, scipy). Le programme Python de nouveau-3 est extrait de `exercices.txt` et exécuté avec la graine 1 : il redonne exactement le tableau de l'énoncé. **OK : tout est vérifié**. Erreur trouvée par ce script et corrigée : la valeur exacte pour n = 50 vaut 0,376 (et non 0,377).
- `verifier_notion.py --navigateur` : **OK, 0 problème** (23 figures, 6 exercices à créer).
- `controle_apercu.mjs` avec captures : aucun problème. Captures téléphone des 6 nouveaux énoncés et corrigés regardées. Corrections : chaînes de calcul réduites découpées (E(X), V(X), sommes de probabilités), tableaux larges passés en colonnes (loi des colis, tableaux de simulation), équivalence de nouveau-1 Q4 en formule centrée, phrases réécrites là où « : » tombait seul en début de ligne.

### Remarque pour l'orchestrateur (moteur)
Même limite que pour la notion 83 : `$x$ :` ou `$x$ ;` (avec l'espace français) peut faire passer la ponctuation seule à la ligne au téléphone ; contourné en reformulant.
