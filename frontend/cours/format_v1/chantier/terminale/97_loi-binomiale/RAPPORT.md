# Notion 97 — Loi binomiale (Terminale) : rapport

**État : prêt.** Cours 99, fiche 41, 11 exercices (Id, titres et difficultés inchangés).

## Texte

- **Cours réécrit et complété** (structure du pilote) : objectifs et prérequis ; loi de Bernoulli
  (tableau, démonstration de $E$ et $V$) ; schéma de Bernoulli, loi binomiale, théorème
  $P(X=k)$ avec **démonstration au programme** dans un encadré `demonstration` ; méthode
  « rédaction type » ; attention sur l'indépendance (tirage sans remise) ; espérance/variance
  (justification par somme de variables de Bernoulli renvoyée à la notion « Sommes de variables
  aléatoires ») ; allure de la loi ; calculatrice ; probabilités cumulées ; seuil sur $k$
  (programme Python raccourci pour le téléphone) et **seuil sur $n$ avec ln** (ajouté : question
  type bac). Un seul fil conducteur : le QCM $\mathcal{B}(10\,;0{,}25)$ (texte et figures cohérents ;
  l'ancienne figure cumulée utilisait $\mathcal{B}(10\,;0{,}3)$, sans lien avec l'exemple).
- **Fiche** remise au propre (4 points de calcul, pièges, réflexe « au moins un succès »).
- **Exercices** : énoncés reformulés en vraies questions (« Justifier que… » au lieu de
  « Modélisation par la loi binomiale »), $X$ défini dans chaque énoncé ; étapes réécrites
  (méthode / étapes / résultat, calculs alignés, « attention » sur $\ge k$, « plus de $k$ »,
  $P(a\le X\le b)$) ; notation $q$ non définie supprimée ($np(1-p)$ partout).
- **Erreurs de fond corrigées** (toutes les valeurs vérifiées par `verif_loi_binomiale.py`,
  calcul exact + scipy, à garder) :
  - 1114 Q4 : $P(X=3)$, $P(X=4)$, $P(X=5)$ étaient **faux** en ligne (0,2368 ; 0,1686 ; 0,1037 au lieu de
    0,2188 ; 0,1284 ; 0,0581) ; Q2 : somme d'arrondis incohérente (0,082 + 0,214 + 0,270 ≠ 0,565).
  - 1120 Q2 : $P(X=9)$ arrondi faux (0,206 → **0,207**).
  - 1117 Q2 : 0,1745 → **0,1746** ; Q5 : interprétation biologique fausse (« 3:1 mais ici 1:1 ») :
    un croisement d'hybrides donne 3/4 de dominants. Énoncé corrigé en **croisement-test**
    (hybride × ridé, proportion 1 : 1, cohérente avec $p = 0{,}5$) et caractère « forme de la
    graine » (lisse/ridé : caractère de Mendel ; « gousse lisse/ridée » n'en est pas un).
  - 1112 : arrondis intermédiaires accumulés (0,5491 / 0,8160 / 0,1840) → 0,5490 / 0,8159 / 0,1841.
  - 1115 Q5 : « ≈ 200 € » → $= 200$ €.
  - 1119 Q5 : « améliore le taux de tri de 5 % » ambigu → « passe de 25 % à 30 % » ; ajout du seuil
    de rentabilité (500 ménages).
  - 1113 : justification de l'assimilation à des tirages avec remise (25 ≪ 5 000) ; Q5 reformulée
    (probabilité qu'au moins 40 % de l'échantillon soit favorable) ; espérance 8,75 non arrondie à 9.
  - 1118 : « clients potentiels » satisfaits → clients choisis au hasard.

## Figures

- **4 refaites** (images en ligne, style matplotlib, toutes retirées) : arbre du schéma de
  Bernoulli ($n=3$, cas général, chemins à 2 succès en vert), diagramme $\mathcal{B}(10\,;0{,}25)$
  avec $E(X)$, trois lois $\mathcal{B}(20\,;p)$, probabilités cumulées et seuil 0,95 ; la fiche
  réutilise 2 d'entre elles.
- **3 ajoutées** dans les corrigés : 1117 (queue $X>10$), 1114 ($P(3\le X\le5)=P(X\le5)-P(X\le2)$
  en couleurs), 1119 (valeurs 6 à 12).
- 0 conservée ; tableaux de données en tableaux natifs (loi de $X$ en 1111, vérification du seuil en 1121).
- Probabilités tracées calculées dans `figures/figures.py` ; aucun texte sur un trait (contrôle de
  `figures_livre.py`), largeurs ≤ 900 px ; chaque PNG regardé.

## Contrôles

- `verif_loi_binomiale.py` : tous les résultats publiés justes (programme Python du cours exécuté).
- `verifier_notion.py --navigateur` : OK (0 problème).
- Vues regardées (téléphone) : cours (4 captures), fiche, exercices 1114, 1117, 1121 (étapes).

## Remarques pour l'orchestrateur

- `controle_apercu.mjs` signale comme « trop large » un bloc de code plus large que l'écran alors
  que `.otm-code` défile (`overflow-x: auto`) : le sélecteur d'exclusion ne connaît que
  `.otm-scroll`. Contourné en raccourcissant les lignes du programme (≤ 30 caractères).
- Une formule centrée d'une seule ligne trop longue défile sur téléphone et paraît « coupée » ;
  le contrôle ne le signale pas : les formules longues ont été passées en `aligned`.


## Finition 2026-11-02

**État : prêt** (passe de finition, agent finition-T6). Sauvegardes : `sauvegardes/*_avant_finition_20261102.*`.

### Titres
- Cours « Schéma de Bernoulli et loi binomiale » et fiche « Résumé : … » : intitulé officiel, inchangés.
- 11 titres sans rubrique « Biologie : », « Commerce : »… ni majuscules abusives (ex. « Découverte - Tirages de cartes avec remise », « Entraînement - Génétique des pois », « Problème - Contrôle qualité et règle de décision »). « Type Bac » → « Type examen » (1121 : « Démarchage téléphonique et seuil »).

### Exercices
- **1 ajouté** (11 → 12) : `nouveau-1` « Découverte - Trois lancers francs : arbre et loi binomiale » (arbre de Bernoulli à 3 épreuves à compléter, chemins à 2 réussites, loi de B(3 ; 0,7), P(X ≥ 2) = 0,784, E(X) = 2,1).
- **1112 réécrit entièrement** : c’était un deuxième « contrôle qualité » identique à 1114 (mêmes questions). Nouveau contenu : B(50 ; 0,06), **plus petit k tel que P(X ≤ k) ≥ 0,95** (k = 6, compétence « seuil » du programme qu’aucun exercice ne travaillait), règle de décision et risque d’arrêt à tort P(X ≥ 7) ≈ 0,029, lien avec la fonction `seuil` du cours.
- Phrases ajoutées dans les corrigés pour lire les diagrammes (barres vertes / orange).

### Figures (19 fichiers, 21 emplacements)
- **7 existantes revérifiées** (probabilités recalculées) ; **1 retouchée** : `arbre_schema` — deux barres consécutives (S̄S̄) se fondaient en une seule barre longue ; lettres maintenant séparées.
- **12 ajoutées**, toutes calculées dans `figures.py` (barres ET étiquettes, jamais recopiées) : cours `cours_complement` (B(10 ; 0,25), P(X ≤ 4) orange, P(X ≥ 5) vert) ; diagrammes en bâtons coloriés dans les corrigés de 1111, 1120, 1118, 1115, 1113, 1116, 1112 ; 1121 `e1121_seuil_n` (1 − 0,85ⁿ et seuil 0,95) ; nouveau-1 : arbre à compléter (énoncé), arbre complété en vert (corrigé), loi B(3 ; 0,7).
- Les 12 exercices ont une figure (8 sur 11 n’en avaient pas). Étiquettes placées entre les lignes de grille (premier essai refusé par le détecteur texte/trait).

### Contrôles
- `verif_loi_binomiale.py` : **tout est juste** (153 comparaisons exact + scipy ; section « FINITION » : 1112 réécrit, étiquettes de toutes les nouvelles figures, masse négligeable au-delà des fenêtres tracées, code Python du cours **exécuté** : `seuil(10, 0.25, 0.05) = 5`, `seuil(50, 0.06, 0.05) = 6`).
- `verifier_notion.py --navigateur` : **OK, 0 problème** ; `controle_apercu.mjs` : aucun problème. Captures téléphone regardées (nouveau-1, 1112) : l’arbre complété de nouveau-1 était trop petit (883 px) → colonne « issue » retirée du corrigé (774 px).
