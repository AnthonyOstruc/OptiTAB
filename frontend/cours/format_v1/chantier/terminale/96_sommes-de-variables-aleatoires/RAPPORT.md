# Notion 96 — Sommes de variables aléatoires (Terminale)

**État : prêt.** Aucun point en suspens.

## Texte

- **Cours** (id 102) restructuré : prérequis, définition de la somme et de l’indépendance, loi de la
  somme de deux dés, linéarité, variance d’une somme (contre-exemple Y = −X, écarts types), théorème
  binomial avec démonstration complète (variance de Bernoulli détaillée), échantillons (définition,
  propriété, démonstration), retenir.
- **Fiche** (id 75) : formules encadrées, loi binomiale, échantillons, 4 erreurs classiques.
- **Exercices** (5) réécrits au format du pilote ; DS restructuré en `## Partie A…E` + `## Question A1…`.
  Corrections de fond :
  - 1287 Q2 (jeu à 5 dés) : probabilités « admises » fausses (0,05 / 0,35 / 0,60) → valeurs exactes
    P(S ≥ 25) = 7/216 ≈ 0,0324, P(20 ≤ S ≤ 24) = 707/2592 ≈ 0,2728 ; E(G) ≈ **3,38** (et non 4,5),
    E(N) ≈ **−4,62** (et non −3,5). Ajout de a) : E(S) et V(S) par linéarité/additivité (données
    auparavant « admises » et inutilisées) ;
  - 1287 Q4 : « environ 95 % » affirmé sans justification au programme → vérifié par la loi binomiale
    (P(107 ≤ X ≤ 133) ≈ 0,949) + borne de Bienaymé-Tchebychev (≥ 75 %) ;
  - 1287 Q5 : la probabilité que le système fonctionne (évoquée mais jamais demandée) est calculée : 0,972 ;
  - 1288 B2 : énoncé incohérent (« Soit X une variable… V(Y) = 3 ») corrigé ;
  - 1286 Q2 : non-indépendance expliquée sans « covariance » (hors programme) ; erreur V(X) + V(Y) = 155/64 signalée ;
  - 1285 Q5 : variance de Bernoulli démontrée par la définition (plus de König-Huygens).
- Vérification : `verif_sommes-de-variables-aleatoires.py` (lois exactes en fractions, convolutions,
  énumération des 8⁵ tirages pour 1286 Q2) — tout est juste.

## Figures

- **2 images en ligne refaites** (matplotlib) : lois d’un dé / de deux dés (`cours_deux_des`) et
  concentration de la moyenne de n dés (`cours_moyennes`, lois exactes n = 1, 4, 16 au lieu d’une
  « densité × n » peu lisible) ; utilisées dans le cours et la fiche.
- **2 ajoutées** (corrigé 1287) : loi de la somme de 5 dés avec zones de gain, loi de la fréquence
  avec l’intervalle I.
- 0 conservée. ≤ 900 px ; seul avertissement : la cote « I : ≈ 95 % » posée sur sa flèche (normal).

## Contrôles

- `verifier_notion.py --navigateur` : **OK, 0 problème**.
- Vues regardées : cours (téléphone), exercices 1286 et 1287 ; formules trop larges (tableaux
  alignés à 2 colonnes, formule binomiale) scindées après relecture.

## Finition 2026-11-02

**État : prêt** (sauvegardes des trois fichiers avant finition dans `sauvegardes/*_avant_finition_20261102.txt`).

### Titres
- Cours « Sommes de variables aléatoires » et fiche « Résumé : Sommes de variables aléatoires » : déjà l'intitulé officiel, inchangés.
- 5 titres d'exercices sans « Sommes de Variables Aléatoires » ni majuscules abusives : 1285 « Découverte - Variance d'une somme de variables indépendantes », 1284 « Découverte - Linéarité de l'espérance », 1288 « DS - Devoir surveillé complet », 1286 « Entraînement - Espérance et variance d'une somme », 1287 « Problème - Contrôle qualité, jeux et échantillons ».

### Exercices
- Relus en entier : justes et au programme (linéarité, variance d'une somme de variables indépendantes, binomiale comme somme de Bernoulli, échantillon et moyenne) ; aucun à réécrire.
- 1285 Q2 : étape ajoutée « Vérification avec la loi de S » (loi 1/4, 1/2, 1/4, variance recalculée par la définition = 1/2), avec la figure.
- 1284 Q4 : encadré « retenir » ajouté (la moyenne subit la même transformation que les valeurs : linéarité), avec la figure.
- 1286 Q4 : les écarts à l'espérance (5 − 1,5 = 3,5 et −2 − 1,5 = −3,5) sont maintenant écrits avant le calcul de V(Gᵢ) (saut de calcul).

### Figures (11 fichiers, 13 emplacements)
- **Revérifiées (4)** : `ex_fluctuation` conservée (seul avertissement : la cote « I : ≈ 95 % », normal) ; `cours_moyennes` conservée ; **`cours_deux_des` refaite** : les titres des panneaux (« un dé : X », « deux dés : S = X + Y ») étaient coupés par le cadre des axes et n'apparaissaient pas (`clip=false`) ; **`ex_cinq_des` retouchée** : graduation sans étiquette à 17,5 retirée.
- **Ajoutées (7, énoncé + corrigé complété en vert)** : `ex1284_lineaire` / `_corrige` (valeurs de X reliées à celles de 3X + 2 ; en vert 3,5 ↦ 12,5) ; `ex1285_pieces` / `_corrige` (lois de X₁ et X₂ ; en vert loi de S = X₁ + X₂) ; `ex1286_urne` / `_corrige` (3 rouges, 4 bleues, 1 verte ; accolade verte « 7 boules sur 8 ») ; `ex1288_composants_corrige` (loi de N ~ B(4 ; 0,85), barres k = 3 et 4 en vert, P(N ⩾ 3) ≈ 0,890).
- Volontairement sans figure d'énoncé : 1288 (DS, la loi de N donnerait la réponse de E1) et 1287 (la loi de S de 5 dés donnerait la question 2 ; les probabilités sont déjà dans le texte).
- Corrections pendant la fabrication : titres de panneaux coupés (`clip=false`) ; schéma de linéarité trop large (1015 px) → texte latéral raccourci (« × 3 puis + 2 »).
- `figures_livre.py` : 11/11 produites, 0 refus. Chaque PNG regardé.

### Contrôles
- `verif_sommes-de-variables-aleatoires.py` : tout est juste, avec une section sympy « Finition 2026-11-02 » (valeurs de 3X + 2 et 12,5 ; loi de S par énumération, E(S) = 1, V(S) = 1/2 ; 7/8 et 35/64 ; écarts ±3,5 et V(Gᵢ) = 49/4 ; probabilités affichées de B(4 ; 0,85) et P(N ⩾ 3) = 0,890 481 25).
- `verifier_notion.py --navigateur` : OK, 0 problème (13 nouvelles figures, 0 image en ligne conservée, 0 non appelée). Chrome s'est fermé normalement.
- `controle_apercu.mjs` avec captures : aucun problème. Captures téléphone regardées : 1284 (énoncé), 1285, 1286 et 1288 (étapes). Après relecture : formule de V(S) (1285 Q2) réduite au téléphone → découpée sur 4 lignes ; urne resserrée.
- Points restants (mineurs) : au téléphone, les graduations 1/4 et 1/2 de `ex1285_pieces` et le texte de `ex1284_lineaire` sont petits mais lisibles ; à agrandir lors d'une prochaine passe si besoin.

## Enrichissement 2026-11-02

**État : prêt** (non importé). 5 → **11 exercices** : 6 blocs ajoutés à la fin de `exercices.txt` (`Id: nouveau-1` à `nouveau-6`). Les 5 exercices existants sont identiques à l'octet près (comparés à la sauvegarde). Sauvegardes : `sauvegardes/*_avant_enrichissement_20261102.*` (exercices, figures.py, correspondance.json).

### Exercices ajoutés
| Id | Titre | Difficulté | Compétence |
|---|---|---|---|
| nouveau-1 | Découverte - Transformation affine d'une variable aléatoire | easy | E(aX + b), V(aX + b), σ(aX + b) ; loi de Y = 2X − 1 ; mise équitable (jeu de fléchettes) |
| nouveau-2 | Découverte - Loi binomiale et variables de Bernoulli | easy | QCM : N = X₁ + … + X₅ ~ B(5 ; 1/4), E = np, V = np(1 − p) par linéarité et additivité ; note T = 5N − 5 ; P(T > 0) = 47/128 |
| nouveau-3 | Entraînement - Variance d'une somme : indépendance ou non | medium | V(X + Y) = V(X) + V(Y) (dés indépendants) ; contre-exemple face du dessus / du dessous : X + Z = 7, V(X + Z) = 0 ≠ 35/6 ; V(X − Z) = 35/3, V(X − Y) = 35/6 |
| nouveau-4 | Entraînement - Échantillon : somme et moyenne | medium | Temps d'attente : Sₙ, Mₙ, E(Mₙ) = μ, V(Mₙ) = σ²/n, σ(Mₙ) = σ/√n ; plus petit n tel que σ(Mₙ) ≤ 0,25 (n = 64) |
| nouveau-5 | Problème - Assurance et mutualisation des risques | hard | Loi par un arbre, E/V/σ d'un coût, bénéfice B = 100 − X, 1 000 contrats indépendants, mutualisation (σ divisé par √n), n ≥ 10 604 |
| nouveau-6 | Type examen - Chaîne de production | hard | 3 parties : A (loi, E, V, coût affine C = 0,5X + 3) ; B (binomiale comme somme de Bernoulli, B(50 ; 0,04), probabilités, coût d'un lot, linéarité sans indépendance pour E(K + 6D)) ; C (moyenne d'échantillon, n ≥ 196) |

Chaque exercice : énoncé avec contexte et questions numérotées ; corrigé `méthode / étapes / résultat` avec erreurs fréquentes (`attention`) et `retenir` ; solution courte. Hors programme évité : pas de covariance, pas de König-Huygens (variances par la définition), Bienaymé-Tchebychev non utilisé.

### Figures (11 nouvelles, style livre, `figures_livre.py` : 11/11, 0 refus de chevauchement)
- Énoncé + corrigé complété en vert : `n1_forain` / `n1_forain_corrige` (loi de X ; en vert loi de Y = 2X − 1, E(X) = 1,1 et E(Y) = 1,2 seulement dans le corrigé) ; `n2_qcm` / `n2_qcm_corrige` (5 épreuves X₁…X₅ ; en vert p = 1/4 et accolade N ~ B(5 ; 1/4)) ; `n4_attente` (loi de X) / `n4_moyennes_corrige` (lois exactes de M₁, M₄, M₂₅ qui se resserrent, σ = 2 ; 1 ; 0,4) ; `n5_arbre` / `n5_arbre_corrige` (arbre ; en vert coûts et probabilités des chemins).
- Corrigé seul (en énoncé, elles donneraient la réponse) : `n2_loi_corrige` (B(5 ; 1/4), barres k ≥ 2 en vert) ; `n3_des_corrige` (loi de X + Y vs X + Z = 7) ; `n6_defauts_corrige` (B(50 ; 0,04), k ≤ 2 en vert, P(D ≤ 2) ≈ 0,677).
- Retouches après relecture des PNG : E(X) retiré de la figure d'énoncé `n1_forain` (donnait la réponse) ; « 1 : 1/4 » remplacé par « 4 choix » dans `n2_qcm` ; largeurs réduites (`n1_forain_corrige`, `n3_des_corrige`, `n5_arbre_corrige` : 968/1007/1055 px → ≤ 910 px) ; étiquettes 0,130 / 0,090 avec leurs zéros.
- Clés `nouveau-1` à `nouveau-6` ajoutées dans `figures/correspondance.json` (alt descriptifs).

### Contrôles
- `verif_sommes-de-variables-aleatoires.py` : nouvelle section sympy « Enrichissement 2026-11-02 » (une partie par exercice, 83 contrôles : lois exactes par convolution, E et V par la définition, binomiales exactes, valeurs affichées sur les figures, résolutions d'inéquations) — **tout est juste**.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (24 figures, 6 exercices à créer).
- `controle_apercu.mjs` avec captures : 70 vues, aucun problème (débordement 0, formule en erreur 0). Captures téléphone des 6 nouveaux corrigés regardées : formules réduites découpées sur plusieurs lignes (≈ 30 chaînes de calcul), chaîne d'équivalences de nouveau-2 4c et somme P(D ≤ 2) passées en formules centrées, E(K + 6D) qui défilait découpée.
- Chrome est resté bloqué à la fermeture de `controle_apercu.mjs` (captures déjà écrites) : seul mon processus node (lancé sur cette notion) a été arrêté.
- Point mineur : au téléphone, le texte de `n5_arbre_corrige` et des étiquettes de `n4_moyennes_corrige` est petit mais lisible.
