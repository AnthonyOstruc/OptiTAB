# Rapport — Terminale, notion 104 « Graphes et matrices » (Maths expertes)

**État : prêt.**

## Texte
- **Cours (112) réécrit en entier** d’après le programme officiel (BO n° 8 du 25/07/2019) : matrices, produit, inverse (démonstration de la formule d’ordre 2), systèmes, puissances, suites $U_{n+1}=AU_n$ et $U_{n+1}=AU_n+C$, transformations du plan, vocabulaire des graphes (ordre, degré, complet, chaîne, cycle, connexe, orienté, pondéré), matrice d’adjacence et **démonstration du comptage des chemins**, **chaînes de Markov** (absentes avant : matrice de transition, graphe associé, $\pi_n=\pi_0P^n$ démontré, interprétation de $P^n$, distribution invariante, exemples à 2 et 3 états, code Python). Déterminant d’ordre 3 / Sarrus conservé en « Pour aller plus loin (hors programme) ».
- **Erreurs corrigées** (ancien cours) : figures « orienté » et « non orienté » inversées ; exemple $A^2$ fait sur un autre graphe que « le graphe précédent », avec une interprétation fausse (« 1 chemin de chaque sommet vers chaque sommet ») ; critère de forte connexité faux (« $A+\dots+A^{n-1}$ sans zéro » : faux pour un cycle) → remplacé par $I+A+\dots+A^{p-1}$.
- **Fiche (49) refaite** (2 écrans) ; l’encadré de couleur inconnue signalé (schéma Sarrus en HTML coloré, converti en bloc de code incohérent) a disparu avec la réécriture.
- **Exercices (9)** remis au format du pilote, tous les résultats vérifiés (`verif_graphes_matrices.py`, sympy, énumération des chemins) :
  - 1138 : chemin faux corrigé ($B\to C\to D\to E\to A$ est de longueur 4) → $B\to D\to E\to A$ ; « calculs similaires… » remplacés par le calcul complet (méthode des sommes de lignes).
  - 1142 / 1138 : « fortement connexe » défini dans l’énoncé, justifié par un circuit passant par tous les sommets (+ contrôle matriciel).
  - 1135 : le déterminant 3×3 (hors programme) de $B$ remplacé par le calcul $BB'=I_3$ (inverse d’ordre 3, au programme).
  - 1137 : $M_0=\binom{1}{0}$ (suite triviale $\binom{2^n}{0}$) remplacé par $M_0=\binom11$ pour exploiter la formule de $A^n$ : $M_n=\binom{(n+2)2^{n-1}}{2^n}$.
  - 1140 (Sarrus) : conservé, signalé « Pour aller plus loin » (titre imposé).
  - 1136 : interprétation graphique ajoutée (droites sécantes, confondues, parallèles) ; vérification générale de la Q2.

## Figures (TikZ, style livre)
- **24 positions, 20 figures neuves** : 17 images en ligne remplacées/retirées, toutes refaites (anciennes images bleues avec matrices en image, orienté/non orienté inversés). 0 conservée.
- Cours : 12 (produit ligne×colonne, Sarrus, rotation, graphe $G$, $K_4$/$K_5$, connexe/non connexe, graphe pondéré, graphe orienté, chemins en vert, Markov 2 et 3 états, convergence). Fiche : 2 (réutilisées). Exercices : 10 (graphes 1142/1138 + chemins en vert dans les corrigés, rotation et composée 1139, 3 droites 1136, Sarrus numérique 1140).
- 3 images en ligne non appelées (fiche, positions 3–5) → supprimées à l’import.
- Aucune étiquette sur un trait (contrôle automatique), largeurs ≤ 900 px.

## Contrôles
- `verifier_notion.py --navigateur` : OK, 0 problème. Captures regardées (cours en téléphone, exercices) ; formules larges recoupées en lignes alignées (outil `largeur_formules.py`).

## Remarques pour l’orchestrateur
- Les titres en base restent « Matrices » / « Résumé : Matrices » : à renommer « Graphes et matrices » si souhaité.
- Aucun exercice sur les chaînes de Markov dans cette notion (le cours les traite) : à ajouter plus tard.
- 1140 (déterminants 3×3, Sarrus) est hors programme par son titre même.

## Finition 2026-11-02

**État : prêt** (agent-finition-T8). **12 exercices** (9 avant) : 1 réécrit, 3 ajoutés.

### Exercices
- **1140 réécrit** (Sarrus / déterminant d'ordre 3 hors programme) : « Entraînement - Marche aléatoire et état stable » — trois refuges $A$, $B$, $C$, graphe probabiliste, matrice de transition, $\pi_1 = (0{,}7\ \ 0{,}3\ \ 0)$, $\pi_2 = (0{,}55\ \ 0{,}3\ \ 0{,}15)$, $(P^2)_{AC} = 0{,}15$ vérifié sur le graphe, $P(X_n = B) = 0{,}3$ pour $n \geq 1$ (colonne constante), distribution invariante $(0{,}2\ \ 0{,}3\ \ 0{,}5)$, interprétation.
- **nouveau-1** « Découverte - Graphe probabiliste à deux états » (météo) : $P$, $\pi_1$, $\pi_2$, $P^2$ et $(P^2)_{MB} = 0{,}6$ vérifié par les chemins, invariante $(0{,}8\ \ 0{,}2)$.
- **nouveau-2** « Entraînement - Graphe non orienté : degrés, connexité et chaînes » : ordre, degrés, somme des degrés $= 2 \times 6$ arêtes, complet / connexe, matrice symétrique, $M^2$ (diagonale = degrés, 2 chaînes $A$–$D$), $(M^3)_{AE} = 2$ et les chaînes citées.
- **nouveau-3** « Problème - Suite de matrices colonnes et état stable » : deux antennes d'une association, $U_{n+1} = AU_n + C$, $L = (30\,;20)$, $V_n = A^nV_0$, $A = PDP^{-1}$ et récurrence, $a_n = 30 - 15 \times 0{,}8^n - 5 \times 0{,}4^n$, $b_n = 20 - 15 \times 0{,}8^n + 5 \times 0{,}4^n$, limites.
- Le programme est maintenant couvert : graphes orientés **et** non orientés, chaînes de longueur $n$, puissances, suites $U_{n+1} = AU_n (+ C)$, marches aléatoires, état stable.

### Cours
- Démonstration de $\pi_{n+1} = \pi_nP$ (partie VIII) : la formule avait été **cassée** par un découpage automatique en chaîne alignée (« $P(X_n \\ &= k)$… », des « = » pris à l'intérieur des parenthèses). Réécrite (phrase + une formule courte). Recherche systématique dans les trois notions (contrôle des parenthèses ligne à ligne dans les `aligned`) : aucun autre cas ; aucune liste de matrices transformée en chaîne.
- Titres : « Graphes et matrices » / « Résumé : Graphes et matrices » (à renommer aussi en base : l'importeur ne change pas les titres de cours et fiche).

### Titres d'exercices
« Matrices - » retiré des 9 anciens titres ; « DS - » → « Type examen - » (1142 « Graphe orienté et nombre de chemins », 1141 « Puissances d'une matrice triangulaire et suite »).

### Figures
- **Revérifiées** : les 22 existantes. **Refaite (1)** : `ex1139_composee` (graduation « 1 » écrite sur le pointillé $x = 1$, et $N_1$ collé à la droite verte).
- **Retirée (1)** : `ex1140_sarrus` (exercice réécrit ; `cours_sarrus` reste dans le « Pour aller plus loin » du cours).
- **Ajoutées (8)** : `ex1134_produit` (ligne × colonne dans le corrigé), `ex1140_graphe` (graphe probabiliste 3 états), `ex1140_convergence` (état stable), `n1_graphe`, `n2_graphe`, `n2_chaines` (chaînes en vert), `n3_convergence`.
- Sans figure, par choix : 1135, 1141, 1137 (calcul matriciel pur).

### Contrôles
- `verif_graphes_matrices.py` : TOUT EST JUSTE (1140 réécrit, nouveaux 1 à 3, figure 1134 ; chemins et chaînes énumérés).
- `figures_livre.py` : 28/28, 0 erreur, 0 avertissement.
- `verifier_notion.py --navigateur` : OK, 0 problème ; `controle_apercu.mjs` : « Aucun problème détecté ».
- Captures téléphone regardées (1140, nouveaux 1 à 3, cours VIII) : 8 formules réduites ou coupées redécoupées ($P^2$ coefficient par coefficient, deux systèmes séparés, $b_{n+1}$, $(M^3)_{AE}$, vérifications de distributions invariantes, chaînes d'équivalences) ; graphes et courbes de 1140 / nouveau-3 rétrécis pour rester lisibles sur téléphone.

### Pour l'orchestrateur
- 3 exercices à créer (`nouveau-1` à `nouveau-3`, figures déclarées dans `correspondance.json`) : `relier_nouveaux` avant l'import.
