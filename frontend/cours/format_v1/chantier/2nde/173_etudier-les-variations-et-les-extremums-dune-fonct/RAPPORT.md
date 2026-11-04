# Rapport — 2nde, notion 173 « Étudier les variations et les extremums d’une fonction »

**État : prêt.** Aucun point en suspens.

## Texte

- **Cours (225)** remis au niveau du programme 2019 (section « Variations et
  extremums ») : définitions (croissante, décroissante, strictement, monotone ;
  maximum / minimum avec « atteint en »), tableau de variations en `::: tableau`
  natif (l’ancienne image est retirée), méthode « comparer deux images »,
  erreurs fréquentes, fonctions affines avec **démonstration** et taux
  d’accroissement, variations de carré / inverse / racine carrée avec les **trois
  démonstrations du programme** complètes (encadrés `demonstration`) et leurs
  tableaux, balayage Python (lignes ≤ 30 caractères) avec la remarque
  « valeur approchée par défaut ». Pas de dérivation (hors programme de Seconde).
- **Fiche (143)** : tableau de variations en natif (image retirée), tableau
  récapitulatif des variations à connaître ; l’ancien encadré « formule » (qui
  se coupait mal sur téléphone et doublait la figure) remplacé par deux puces.
- Les tableaux de la fonction carré sur ℝ et de la fonction inverse laissent
  les valeurs aux bornes infinies vides (limites hors programme de Seconde,
  `{}` pour les doubles barres).
- `verif_173.py` : 56 contrôles (sympy + exécution du programme Python +
  monotonie des courbes tracées) — tous justes.

## Exercices (13 existants + 2 ajoutés)

- **Remplacé — 2012** « Lire les variations sur une table de valeurs » : faible
  (une table de valeurs ne permet pas de conclure à des variations ni à une
  fonction « constante » ; la capacité « relier courbe et variations » n’était
  travaillée nulle part). Remplacé par « Découverte - Lire variations et
  extremums sur une courbe » (figure d’énoncé + figure de corrigé, tableau,
  extremums sur deux intervalles, comparaison d’images).
- **Retravaillés en profondeur** (même Id, même sujet) :
  - 2015 Racine carrée : valeur intermédiaire `=/\sqrt{5}` **vérifiée** : $r(0)=\sqrt5\approx2{,}24$
    est bien entre $3$ et $0$ et placée sous $x=0$ (justification ajoutée) ; tableau
    « à compléter » cassé (5 éléments pour 3 valeurs) supprimé ; solution
    déstructurée réparée ; inéquation résolue par la décroissance ; titre sans
    « fonction composée » (vocabulaire hors Seconde).
  - 2020 Fonctions de référence : la question « $x^3=-27$ » (racine cubique, hors
    programme, et empiétant sur la notion 171) remplacée par des comparaisons et
    encadrements par les variations (carré sur des négatifs, inverse sur un intervalle).
  - 2014 et 2023 : « compléter le carré » (forme canonique = Première) remplacé
    par « vérifier la forme proposée en développant » ; 2014 ramené sur $[0\,;5]$
    (valeurs $-331$ / $-91$ sans intérêt) ; 2023 avec $x\in{]0\,;10[}$.
  - 2013 ramené sur $[-6\,;2]$ ; inéquation résolue avec le tableau.
  - 2014, 2013, 2022, 2017 : sens de variation **démontré** avec $u \lt v$
    (au lieu de « $x$ se rapproche de 3 »).
  - 2024 Balayage : l’ancien exemple trouvait le maximum exact dès $n=4$ ; nouvelle
    fonction $x(5-x)$ où le balayage donne $6$ au lieu de $6{,}25$, suivi des
    variables, test strict, maximum exact, effet de $n$ ; question « dichotomie »
    (hors sujet) retirée.
  - Tous : chaînes d’équivalences longues mises en `aligned` (lisibles sur
    téléphone), solutions « tableau éclaté en texte » réparées, encadrés `resultat`
    en double supprimés, intervalles $[a\,;b]$, titres d’étapes en texte.
- **Ajoutés** : `nouveau-1` « Entraînement - Démontrer un sens de variation »
  (signe de $f(v)-f(u)$, contre-exemple) ; `nouveau-2` « Entraînement - Fonction
  affine : variations, signe et droite » (capacité du programme « relier sens de
  variation, signe et droite représentative d’une fonction affine », figure).

## Figures

- 9 figures neuves au style des livres (`figures/figures.py`), 10 emplacements :
  cours (sens de variation, courbe avec extremums — reprise aussi dans la fiche),
  exercices 2012 (×2), 2022, 2023 (×2), 2024, nouveau-2.
- 0 conservée ; 3 images en ligne refaites (sens, courbe) ou remplacées par un
  tableau natif (2 images « tableau » retirées, supprimées à l’import).
- Courbes « lues » : splines de Hermite monotones par morceaux, nœuds = valeurs
  du texte (contrôlés dans `verif_173.py`). Graduations déplacées (XLAB / nœuds
  manuels) pour qu’aucune ne touche la courbe ou un pointillé.

## Contrôles

- `verifier_notion.py --navigateur` : OK, 0 problème.
- Captures Chrome regardées : cours en téléphone (toutes les parties), fiche,
  exercices 2015, 2024, nouveau-2 (énoncé + étapes).

## Remarques pour l’orchestrateur

- `valider_v1.py` refuse une double barre sans valeurs (`-D+//`) : pour les
  tableaux où les limites sont hors programme (inverse en Seconde), il faut
  écrire `-D+/{}/{}`. Une forme admise sans valeurs serait plus propre.

## Finition 2026-11-02

**État : prêt** (agent-finition-S3). 15 exercices (aucun ajout) ; **15 sur 15 ont une figure** (10 n'en avaient pas).

### Revérification des 9 figures existantes
- Recompilées avec le détecteur (0 alerte) et regardées une par une ; justesse : courbe du cours = tableau (−3 ; 2), (−1 ; −2), (2 ; 3), (5 ; 0) ; courbe de 2012 (−4 ; 1), (−2 ; 3), (1 ; −2), (4 ; 2) et f(0) ≈ −0,7 ; balayage x(5 − x) ; −(x − 2)² + 5 ; aire x(10 − x) ; droites 0,5x + 1 et −2x + 3 : **aucune erreur**.
- **2 retouchées** : `parabole_2022` et `aire_2023` montraient l'intervalle solution sans ses bornes → bornes pleines et repères verticaux ajoutés (0 et 4 ; 3 et 7). 7 conservées.

### Figures ajoutées (11)
- Cours III : `cours_affine_173` (f(x) = −2x + 5 sur [0 ; 3] : maximum 5 en 0, minimum −1 en 3). Fiche : la courbe du cours est maintenant placée sous le tableau de variations (tableau relié à la courbe).
- Exercices : 2018 `ex_tableau_2018` (**une** courbe compatible avec le tableau, maximum atteint sur tout [4 ; 5] ; le texte précise que la forme exacte n'est pas donnée par le tableau), 2015 `ex_racine_2015` (r(x) ≥ 2 ⇔ x ∈ [−2 ; 1/2]), 2021 `ex_affine_2021` (marche +1 / −3 = taux d'accroissement, extremums aux bornes), 2020 `ex_carre_2020` (carré sur [−3 ; 2]), 2019 `ex_affine_2019` (f(x) ≥ 1 ⇔ x ∈ [−2 ; 1]), 2014 `ex_parabole_2014` (arc [4 ; 5] en vert : max 5, min −1), 2013 `ex_parabole_2013` (f(x) ≤ 8 ⇔ x ∈ [−6 ; 0]), 2016 `ex_abs_2016` (h(x) ≤ 4 ⇔ x ∈ [−1 ; 5]), 2017 `ex_cloche_2017` (1/(x² + 1) : max 1, min 1/10 aux deux bornes), 3746 `ex_contre_3746` (contre-exemple f(−4) > f(−3), croissance sur [−2 ; +∞[ seulement).
- Détecteur : 0 erreur, 0 alerte après déplacement des étiquettes ; chaque PNG regardé.

### Texte
- Cours V : « la fonction renvoie 4 » → « l’appel `maximum(f, 0, 5, 100)` renvoie `4.0` » (sortie réelle).
- 13 titres d'exercices réécrits (« Algorithmique » et « Maîtrise » supprimés, « forme canonique » retiré : vocabulaire de Première), par exemple : « Problème - Approcher un maximum par balayage en Python », « Entraînement - Taux d’accroissement d’une fonction affine », « Entraînement - Minimum d’une parabole et inéquation », « Entraînement - Variations, extremums et inéquation pour une parabole », « Problème - Aire maximale d’un enclos rectangulaire ». 2015 passe de « Découverte » à « Entraînement » (démonstration, difficulté moyenne).

### Contrôles
- `verif_173.py` : **76 contrôles**, dont les points de chaque nouvelle figure, la monotonie de la courbe tracée pour 2018, et l'**exécution réelle** du code du texte (cours : `4.0` ; 2024 : affichages `2.0 6.0` pour n = 4 et `2.5 6.25` pour n = 8).
- `verifier_notion.py --navigateur` : sur le dossier réel, seuls les Id 3746 et 3747 (absents de `meta.json`) sont signalés ; sur une copie de travail les déclarant : **OK, 0 problème**.
- `controle_apercu.mjs` avec captures : voir ci-dessous.
- Captures (`controle_apercu.mjs`, téléphone et ordinateur) : **aucun problème** ; regardées au téléphone : corrigés 2021 (figure du taux d'accroissement) et 2018.

### Remarque pour l'orchestrateur
- Ré-exporter `meta.json` (les Id 3746 et 3747 créés à l'import du 29/10 n'y figurent pas) avant l'import, sinon `verifier_notion.py` les signale comme inconnus.
