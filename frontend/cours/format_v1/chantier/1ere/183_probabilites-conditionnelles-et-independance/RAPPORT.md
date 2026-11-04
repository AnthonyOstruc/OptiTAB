# Rapport — notion 183 « Probabilités conditionnelles et indépendance » (Première spécialité)

**État : prêt.** Le cours, la fiche et 14 exercices (11 existants réécrits, 3 ajoutés) sont au format OptiTAB v1. Les 52 figures sont neuves, au style des livres. Le titre du cours et celui de la fiche reprennent l’intitulé officiel : « Probabilités conditionnelles et indépendance ».

## Programme (2019, Première spécialité)

Points vérifiés et couverts, dans le cours, la fiche et les exercices :
- probabilité conditionnelle $P_A(B)$, notation, $P(A \cap B) = P(A) \times P_A(B)$, $P_A(\overline{B}) = 1 - P_A(B)$ ;
- tableau croisé d’effectifs (tirage équiprobable d’un individu) ; passage langue naturelle ↔ notations ;
- arbre pondéré et ses trois règles ; partition de l’univers ; formule des probabilités totales (partitions à 2 et à 3 événements) ;
- distinguer $P_A(B)$ et $P_B(A)$ : inversion du conditionnement, tests de dépistage, faux positifs, influence de la prévalence ;
- indépendance de deux événements ; indépendance de $A$ et $\overline{B}$ **avec démonstration** (cours + exercice 1303) ; indépendants ≠ incompatibles ;
- succession de deux épreuves indépendantes, par un arbre ou un tableau à double entrée ;
- simulation en Python (`random() < p`), fréquence observée et probabilité.

**Retiré (hors programme de Première)** :
- le schéma de Bernoulli à 3 épreuves et plus (3 lancers de pièce de 1312 B2 et 1310 Q3, « au moins un 6 en 4 lancers » de 1311 Q5) : loi binomiale de Terminale ;
- les tirages de 3 boules ou 3 cartes (1306, 1308 Q5, 1311 Q2, 1311 Q4) et le dénombrement de combinaisons ;
- la « formule de Bayes » et la notation $P(A|B)$ (1312, 1302, 1305) : remplacées par l’inversion du conditionnement avec la notation $P_A(B)$ du programme.

## Texte

- **Cours réécrit de zéro** (l’ancien tenait en 4 paragraphes) : objectifs, prérequis, 7 parties — définition et tableau croisé, propriétés, traduction d’un énoncé (tableau phrase → notation), arbres pondérés (règles, exemple du bus), partition et probabilités totales, inversion et tests (arbre **et** tableau sur 10 000 personnes, faux positifs), indépendance (démonstration de $A$, $\overline{B}$, incompatibles ≠ indépendants), deux épreuves indépendantes (arbre + tableau), simulation Python, « à retenir ».
- **Fiche réécrite** : formules, arbre, probabilités totales, inversion, indépendance, épreuves indépendantes, simulation, 5 pièges, 4 figures.
- **Les 11 exercices existants sont réécrits entièrement** au modèle du pilote (méthode, étapes, résultat encadré, erreur fréquente) ; la conversion automatique était cassée (questions coupées à l’intérieur des encadrés `resultat`, « arbres » faits de tableaux éclatés, titres de parties en `\underline{\textbf{…}}`). Les Id sont conservés ; contenus remplacés dans leur bloc :
  - 1312 (DS) : tableau croisé + indépendance + $P_{\overline{C}}(B)$ par la propriété ; usine à 2 machines (arbre, probabilités totales, inversion) ; deux prélèvements indépendants ;
  - 1309 : commandes en ligne (traduction, arbre, $P(R)$, $P_R(T)$, $P_{\overline{R}}(\overline{T})$, indépendance) ;
  - 1302 : définition, probabilités composées, deux dés avec tableau des sommes ($P_S(D) \neq P_D(S)$), jeu de 32 cartes ($P_F(C) = P(C)$) ;
  - 1310 : alarme à deux détecteurs indépendants (événement contraire, conditionnement, seuil $p \geqslant 0{,}9$) ;
  - 1303 : tests d’indépendance, tableau de probabilités, dé, **démonstration guidée** de l’indépendance de $A$ et $\overline{B}$, $P(A \cup B)$ ;
  - 1311 : partition à 3 chaînes, inversion pour chaque chaîne, deux pièces indépendantes, seuil d’amélioration ;
  - 1308 : urne sans remise à 2 tirages (arbre justifié, $P(R_2) = P(R_1)$, inversion) ;
  - 1305 : **titre changé** (« Formule de Bayes » → « Tests de dépistage et faux positifs ») : arbre, tableau sur 100 000 personnes, valeur d’un test négatif, population à risque ;
  - 1304 : partition à 3 moyens de transport, inversion, seuil de ponctualité ;
  - 1306 : avec et sans remise comparés (indépendance ou non, même couleur) ;
  - 1307 : **titre changé** (« Synthèse 2 : Arbre de Probabilités » → « Synthèse 2 : Deux tirages avec remise ») : tableau des sommes, arbre de parité, indépendance surprenante de « premier pair » et « somme paire ».
- **Erreurs et défauts corrigés** : notation $P(A|B)$ hors programme ; « formule de Bayes » ; exercices 1305 et 1304 qui renvoyaient à « l’exercice précédent » (contenu non autonome) ; données de 1304 choisies pour que la moyenne simple $\frac{0{,}04 + 0{,}12 + 0{,}06}{3}$ ne donne **pas** par hasard le bon $P(R)$ (le piège est expliqué).
- **Exercices ajoutés** :
  - `nouveau-1` « Découverte - Tableau croisé et traduction d'un énoncé » ;
  - `nouveau-3` « Découverte - Lire et compléter un arbre pondéré » ;
  - `nouveau-2` « Entraînement - Simuler deux épreuves en Python » (lecture de code, fréquences, version indépendante).
- **Vérification** : `verif_probas_conditionnelles.py` (sympy) fait **338 contrôles, 0 erreur** (`verif_log.txt`) : toutes les probabilités, chemins, totaux, inversions, arrondis, inéquations, dénombrements (dés, cartes, jetons). Il **exécute aussi les programmes Python tels qu’ils sont écrits** dans le cours et dans `nouveau-2` (graines fixes) : la sortie citée `(0.7409, 0.7562424078823053)` et la valeur « environ 0,284 » de `freq(100000)` en proviennent ; il contrôle que les lignes de code font au plus 40 caractères.

## Figures

- **52 figures neuves, 0 image en ligne conservée.** Les 14 images en ligne (arbres matplotlib rouge/bleu, figure du cours avec formules minuscules) sont toutes remplacées ; 3 positions de 1304 (3, 4, 5) ne sont plus appelées → supprimées à l’import.
- Probabilités des chemins **calculées par le script des figures** (fractions exactes), jamais recopiées.
- **Cours (6)** : arbre général, arbre du bus (chemins vers $B$ en vert), partition, arbre du dépistage, deux tirages avec remise, courbe de simulation. **Fiche (4)** : figures du cours réutilisées.
- **Exercices (42)** : chaque arbre existe en version **énoncé à compléter** (données de l’énoncé, « … » pour le reste) et en version **corrigé** (valeurs trouvées et probabilité de chaque chemin en vert ; au bout des branches, seule la valeur est écrite, ce qui garde les arbres étroits et lisibles sur téléphone). Tableaux croisés : énoncé en tableau du site avec cases « … », corrigé en figure avec les cases trouvées en vert sur fond vert pâle. Grilles de deux dés / deux jetons : vides dans l’énoncé, complétées en vert dans le corrigé (cases d’événement ombrées ou encadrées, légende). Courbe de fréquence de `nouveau-2` : sans puis avec la valeur théorique.
- Contrôle des chevauchements : 0 erreur ; toutes les largeurs ≤ 900 px (la plus large : partition du cours, 837 px). Chaque planche a été regardée.

## Contrôles

- `verif_probas_conditionnelles.py` : 338 contrôles, 0 erreur.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (52 placements de figures neuves, 0 image en ligne conservée) — `verif_navigateur_log.txt`.
- `controle_apercu.mjs` avec captures : 88 vues (téléphone et ordinateur ; cours, fiche, 14 exercices × 3 onglets), toutes à 0 — `captures_log.txt`.
- **Captures téléphone regardées à l’œil** : le cours en entier (6 écrans), la fiche (2 écrans), les énoncés et étapes de 1312, 1302, 1303, 1305 et nouveau-2. Corrections faites après ces relectures (non signalées par l’outil) :
  - une vingtaine de formules réduites ou suivies d’un point orphelin (« . » ou « ) » seul en début de ligne) : passées en lignes alignées `aligned` (probabilités totales du cours, inversions $P_T(M)$, $P_S(I)$, $P_D(M_2)$…, tests d’indépendance), ou sorties des solutions courtes ;
  - formule d’indépendance de la fiche coupée à droite (encadré `formule` trop large) : réécrite ;
  - arbres des corrigés et tableaux rétrécis (≈ 720 → ≈ 500 px), courbes de simulation rétrécies (862 → 687 px) : leur texte est maintenant à la taille du site sur téléphone.
- Les processus restés ouverts par mes contrôles (node `controle_apercu.mjs`, `timeout`) ont été arrêtés un par un, ceux de cette notion seulement.

## Remarques pour l’orchestrateur

- La « simulation » n’apparaît pas explicitement dans la partie « Probabilités conditionnelles » du texte officiel ; elle est traitée comme demandé par le propriétaire (cours VII, fiche V, exercice `nouveau-2`).
- Les exercices 1305 et 1304 renvoyaient l’un à l’autre (« Reprendre … de l’exercice précédent ») : ils sont maintenant indépendants.
- **Défaut d’outil (détection)**, comme pour la notion 161 : une formule réduite (jusqu’à 70 %) ou suivie d’une ponctuation renvoyée seule à la ligne n’est pas signalée (0 élément trop large). Exemple avant correction : fiche, `$$A \text{ et } B \text{ indépendants} \iff P(A \cap B) = P(A) \times P(B)$$` dans un encadré `formule`, coupée à droite sur téléphone.
- **Défaut d’outil (blocage)** : `controle_apercu.mjs` ne rend pas la main après la dernière vue ; lancé avec `timeout`, puis arrêté à la main.
- Les 3 images en ligne de 1304 (positions 3 à 5, fichiers `prob_total_q3/q4/q5.png`) sont aussi utilisées par 1305 dans la base : à l’import, 1305 reçoit ses nouvelles figures aux positions 1 à 4, donc plus aucun appel ne reste vers ces fichiers.
- Le titre de l’exercice 1312 garde la casse d’origine (« DS - Probabilités Conditionnelles - Devoir Surveillé Complet ») pour ne pas toucher aux titres sans nécessité.
