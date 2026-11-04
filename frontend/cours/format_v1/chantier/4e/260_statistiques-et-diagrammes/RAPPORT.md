# Notion 260 (4e) : Statistiques et diagrammes

**État : prêt** (claude-260, 2026-11-04). 21 exercices (aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée ; 4 exercices remplacés). Aucune écriture en base, aucun git.

Programme de 4e (cycle 4) : effectifs, fréquences (décimal, pourcentage) ; moyenne simple et pondérée (effectifs, coefficients) ; médiane (introduite en 4e) ; étendue ; lire et construire des diagrammes en bâtons / en barres, circulaires, un histogramme simple, une courbe ; interpréter et comparer deux séries ; tableur. Quartiles absents (non exigés). Les « rangs » d'un tableau d'effectifs sont présentés en comptant les effectifs, sans le vocabulaire « effectif cumulé » exigible.

## Cours et fiche

- **Titres** inchangés : « Statistiques et diagrammes » et « Résumé : Statistiques et diagrammes ».
- **Cours 255 réécrit façon manuel** (la conversion avait des puces « • », un exemple dans un encadré `definition`, le renvoi « onglet Fiches », aucun tableur, ni histogramme ni courbe) : objectifs en liste ; I. vocabulaire, fréquence, propriété, exemple « livres lus » en tableau (effectifs + fréquences), méthode pourcentage ; II. moyenne simple, moyenne pondérée (formule, calcul aligné 51/25 = 2,04, coefficients), propriété « somme = moyenne × effectif », erreurs fréquentes ; III. médiane (définition, méthode impair / pair, figure des deux cas, médiane d'un tableau par les rangs), étendue, « moyenne ou médiane ? », erreurs ; IV. diagrammes : bâtons (méthode de construction), circulaire (méthode, tableau effectif / angle, figure), histogramme (classes, figure, médiane située / moyenne estimée), courbe (figure des températures, lectures) ; V. tableur (SOMME, MOYENNE, MEDIANE, MAX−MIN, moyenne pondérée par une colonne de produits), comparaison de deux séries (figure), lecture critique, « À retenir ».
- Tous les exemples du cours sont **nouveaux** : les anciens doublaient les exercices (coefficients de Sarah = 2688, transport = 2689, série 5 ; 7 ; 9… = 2687, fratrie = 2685).
- **Fiche 175 refaite** : tableau des indicateurs, exemple complet, médiane en pratique (figure + méthode), les quatre diagrammes (figures bâtons et circulaire), tableur et comparaison, 5 erreurs classiques, réflexe de contrôle.

## Exercices (21)

- **Progression** dans l'ordre des Id : 7 Découverte (2684-2690), 7 Entraînement (2691-2697), 4 Problème (2698-2701), 3 **Type brevet** (2702-2704 ; il n'y en avait aucun). Titres « Type - Statistiques - n. Sujet » → « Type - Sujet » (21).
- **Tous relus et réécrits** au format des modèles : questions numérotées ; corrigé avec méthode, étapes détaillées (calculs alignés, aucun saut), résultat encadré à **chaque** question (128/128), encadré « Erreur fréquente » dans **21/21** exercices, « À retenir » quand utile ; `Solution:` courte et cohérente. `\displaystyle` (276), « **À retenir :** » en gras, majuscules d'insistance et lignes `Image:` retirés. Toutes les données en **vrais tableaux** (sports, pointures, coefficients, transport, salaires, feuille de tableur, collèges, notes de Hugo, âges, trajets en deux tableaux pour le téléphone) ; formules de tableur en code.
- **Remplacés (4)** :
  - 2692 « Les notes d'un contrôle » (même déroulé que 2690 et 2704 : tableau → moyenne → médiane) → « Entraînement - Du relevé des notes au diagramme en bâtons » : liste brute de 25 notes → tableau d'effectifs à compléter → **construction** du diagramme en bâtons → moyenne, médiane, « +1 point pour tous ».
  - 2698 « Choisir un coureur » (doublon de 2691 et 2703 : même moyenne, choix par l'étendue) → « Problème - Comparer deux collèges avec les fréquences » : effectifs ≠ fréquences quand les groupes n'ont pas la même taille, diagramme en barres comparatif, angle d'un secteur, fréquence des deux collèges réunis (≠ moyenne des fréquences).
  - 2699 « Le sondage sur les vacances » (doublon de 2689 : fréquences → angles) → « Problème - Lire un diagramme circulaire » : sens inverse, angle → fréquence → effectif, extrapolation à la ville, regard critique sur un titre.
  - 2704 « Les âges d'un club de sport » (troisième « tableau → moyenne → médiane ») → « Type brevet - Les âges d'un club de sport » en trois parties : indicateurs, comparaison avec un autre club par des affirmations vrai / faux (médiane, dispersion, moyenne de deux groupes), nouveaux membres.
- **Enrichis** : 2684 (construction d'un diagramme en barres), 2689 (construction du diagramme circulaire, angle de « bus ou vélo »), 2700 (mise en équation $62 + 3x = 108$, arrondi par excès justifié), 2701 (rapport réel 1,04 comparé au rapport visuel 3), 2702 (formules de tableur, affirmation à vérifier avec la médiane), 2703 (lecture du graphique, tableaux), 2697 (rangs des classes).
- **Erreurs corrigées** : aucune erreur de calcul dans les résultats en ligne ; la conversion avait cassé des étapes (formule ou début de phrase pris pour titre d'étape, résultats sans phrase) ; les tableaux de données (sports, pointures, âges, tableur) n'existaient qu'en image ; 2689 et 2699 montraient le diagramme circulaire dans le corrigé sans le faire construire ou lire.
- `verif_260.py` : **277 contrôles sympy** (valeurs exactes), tous justes : chaque résultat du cours, de la fiche et des 21 corrigés (arrondis compris), et les données des figures relues dans `figures/figures.py` (`DONNEES`) et comparées aux énoncés (comptage des 25 notes brutes de 2692, angles du diagramme de 2699, séries rangées, rangs, médianes).

## Figures (style livre, `figures/figures.py`)

- **33 figures neuves** (TikZ) pour **36 positions** ; les **20 images matplotlib en ligne sont toutes remplacées** (0 conservée, 0 non appelée).
  - Cours (6) : séries rangées impair / pair avec médiane en vert, bâtons, circulaire, histogramme, courbe avec maximum et minimum en vert, comparaison de deux séries sur une droite graduée. Fiche (3, mêmes fichiers).
  - Énoncés (données, sans la réponse) : bâtons 2685, barres doubles 2691, histogramme 2697, circulaire 2699 (angles), graphique trompeur 2701, pluie 2702, courbes 2703.
  - Corrigés (réponses en vert) : constructions 2684 (barres), 2689 (circulaire), 2692 (bâtons), 2698 (barres comparatives) ; lectures 2685 (« au moins 2 »), 2699 (pourcentages et effectifs), 2701 (hauteurs visibles / axe à 0), 2702 (mois au-dessus de la moyenne), 2703 (retards entourés) ; **médiane illustrée sur la série rangée** dans 2686, 2687, 2693, 2695, 2702, 2703 et, pour les tableaux d'effectifs, par les **rangs** occupés par chaque valeur (2690, 2692, 2697, 2704) ; dispersion 2691.
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance. Toutes ≤ 900 px. Chaque PNG regardé (planches).

## Contrôles

- `verif_260.py` : 277 contrôles justes.
- `verifier_notion.py` : OK (36 nouvelles images, 0 conservée, 0 non appelée ; notes : 21 titres changés). Avec `--navigateur`, Chrome est resté bloqué à la fermeture (cas connu, tous les compteurs à 0) → contrôle refait avec `controle_apercu.mjs` et captures, deux fois : **130 vues (téléphone + ordinateur), aucun problème détecté**.
- **Captures téléphone regardées** : cours (5 vues), fiche, corrigés 2690, 2691, 2692, 2697, 2698, 2704 et énoncé 2684. Corrections faites après ces vues : tableaux de 6 à 8 colonnes coupés (sports, fratrie, transport, températures, notes, salaires, classes, collèges, pluie, trajets, âges ; cours : livres, activités) → tableaux en 2 à 4 colonnes ; longues sommes de produits réduites ou coupées (2685, 2688, 2690, 2692, 2695, 2697, 2704 ; cours) → tableau « valeur × effectif » avec ligne Total, comme dans un tableur ; sommes de 7 ou 8 nombres (2687, 2691, 2693) et formules doubles (2689, 2695, 2699, 2700, 2701, 2704) découpées ; formules du cours (moyenne pondérée, étendue, angle) raccourcies. Vérifié sur les nouvelles captures.
- Sauvegardes de travail : `sauvegardes/260_exercices_avant_telephone.txt`, `sauvegardes/260_cours_avant_telephone.txt`.
- Espaces insécables avant les unités (°C, €, mm, min, h, ans, cm) : 144 dans les exercices, 8 dans le cours.
- Sauvegarde de la conversion automatique : `sauvegardes/260_exercices_conversion_auto.txt`.

## Remarques pour l'orchestrateur

- Aucune remarque d'outil ou de moteur.
