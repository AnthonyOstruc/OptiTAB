# Notion 259 (4e) : Relier des grandeurs et lire des graphiques

**État : prêt** (claude-259, 2026-11-03). 21 exercices (aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée ; 4 exercices remplacés).

Programme de 4e (cycle 4) : exprimer une grandeur en fonction d'une autre (formule, tableau de valeurs), tableur (formules simples, recopie vers le bas), représenter dans un repère, lire un graphique (lire une valeur, trouver pour quelle valeur on obtient un résultat, sens de variation, maximum / minimum), reconnaître la proportionnalité sur un graphique. Le vocabulaire « fonction, image, antécédent » et la notation $V(3)$ (3e) n'apparaissent qu'en remarque « Pour aller plus loin (3e) » dans le cours ; aucun exercice ne les utilise.

## Cours et fiche

- **Titres** inchangés : « Relier des grandeurs et lire des graphiques » et « Résumé : Relier des grandeurs et lire des graphiques » (intitulé de la notion).
- **Cours 254 réécrit façon manuel** (la conversion avait des puces « • », la méthode en ligne, le renvoi « onglet Fiches », un encadré « rappel » mal choisi et aucun tableur) : objectifs en liste ; I. grandeur qui dépend d'une autre (définition, exemple du carré, méthode « exprimer en fonction de », exemple de la piscine $V = 5 + 2t$) ; II. tableau de valeurs et **tableur** (méthode, formule `=5+2*A2`, feuille en tableau natif, erreurs : `=` oublié, `2A2`) ; III. représenter (définition du repère, méthode en 4 étapes, figure, points isolés quand la variable est entière, graduations régulières) ; IV. lire un graphique (marée $h = 3 - 2\cos$ : lire une valeur, chercher quand une valeur est atteinte — deux réponses —, variations, maximum / minimum ; 3 erreurs fréquentes) ; V. proportionnalité (propriété, figure des trois cas, exemples carré / piscine) ; VI. allure d'une courbe (palier, rectiligne = régulier, raide = rapide, sommet / creux) ; « Pour aller plus loin (3e) » ; « À retenir ».
- Exemples du cours changés pour ne plus doubler les exercices (ancienne température = 2663, ancien taxi = 2667).
- **Fiche 174 refaite** : tableau « formule / tableau / tableur / graphique », méthode tableur, construction, figure de lecture, tableau « on cherche / méthode / exemple », proportionnalité avec figure, allure d'une courbe, 5 erreurs classiques, réflexe.

## Exercices (21)

- **Tous réécrits** au format des modèles : questions numérotées ; corrigé avec méthode, étapes détaillées (calculs alignés), résultat encadré à chaque question, erreur fréquente et/ou « À retenir » dans chaque exercice ; `Solution:` courte et cohérente. `\displaystyle` retirés ; lignes `Image:` de la conversion retirées (images déclarées dans `correspondance.json`). Titres « Type - Graphiques - n. Sujet » → « Type - Sujet » (21).
- **Progression** dans l'ordre des Id : 7 Découverte (2663-2669), 7 Entraînement (2670-2676), 4 Problème (2677-2680), 3 **Type brevet** (2681-2683 ; il n'y en avait aucun).
- **Remplacés (4)** :
  - 2668 « Associer situations et graphiques » (son graphique du ballon était exactement la fonction de 2675) → « Découverte - Associer des situations et des graphiques » : 4 situations (cycliste, bougie, randonneur, bouilloire), 4 graphiques gradués, lectures et proportionnalité ;
  - 2676 « La courbe de croissance d'un bébé » (même compétence que la plante 2665 : croissance qui ralentit) → « Entraînement - Construire le graphique de la distance de freinage » ($d = \frac{v^2}{200}$ : calculs, tableur `=A2^2/200`, construction dans un repère fourni, non-proportionnalité malgré l'origine, lecture inverse, « deux fois plus vite = quatre fois plus de distance ») ;
  - 2678 « Trois vases à remplir » (doublon de 2670 récipients) → « Problème - La pression en plongée » ($P = 1 + 0{,}1d$ : tableur, lecture, droite qui ne passe pas par l'origine, pression due à l'eau proportionnelle, équation $1 + 0{,}1d = 2{,}2$) ;
  - 2680 « L'enclos le long d'un mur » (même structure que 2673 : aire maximale par un tableau) → « Problème - Le volume d'une boîte sans couvercle » (patron, $V = x(20 - 2x)^2$, valeurs possibles, tableur `=20-2*A2`, `=A2*B2^2`, maximum entre deux valeurs du tableau, $V = 500$ deux fois).
- **Réécrits en profondeur** : 2664 (repère vide à compléter, proportionnalité par tableau et graphique) ; 2666 (données rendues lisibles sur la grille : bain de 12 à 24 min ; question nouvelle « 15 cm atteint deux fois ») ; 2667 (l'énoncé demandait une lecture sur un graphique absent : repère fourni, construction par l'élève) ; 2672 (données entières lisibles sur la grille, une seule décennie de plus forte hausse) ; 2673 (feuille de tableur à compléter + courbe de l'aire) ; 2675 (formule de tableur) ; 2679 (refroidissement modélisé, lectures exactes 110 °C et 65 °C, comparaison sur deux périodes égales) ; 2681, 2682, 2683 passés en Type brevet (2681 avec feuille de tableur et bénéfice).
- **Erreurs corrigées** : `Solution:` de 2674 question 5 tronquée par la conversion (« A si $h 5$ ») ; 2667 lecture demandée sur un graphique absent de l'énoncé ; 2682 question 5 réponse imprécise (sortie de zone calculée : $21{,}25$ min) ; 2679 réponses incohérentes avec la courbe en ligne (passage sous 100 °C).
- `verif_259.py` : **280 contrôles** sympy, tous justes (chaque résultat des exercices, du cours et de la fiche ; chaque donnée des figures relue depuis `figures/figures.py` et comparée aux valeurs des énoncés et corrigés : lectures, intersections, maximums, solutions d'équations, tableurs).

## Figures (style livre, `figures/figures.py`)

- **47 figures neuves** ; les **29 images matplotlib en ligne sont toutes remplacées** (0 conservée, 0 retirée).
  - Cours (3) et fiche (3, mêmes fichiers) : marée avec lectures en vert, piscine (points du tableau, droite ne passant pas par l'origine), trois graphiques « proportionnelles / non proportionnelles » (nouvelle).
  - Exercices : énoncé = courbe seule (ou repère vide gradué pour 2664, 2667, 2676) ; corrigé = même figure avec les lectures en vert (pointillés vers les deux axes, points verts, valeurs lues). Schémas : récipients (2670), patron et boîte (2680) ; 4 petits graphiques gradués (2668).
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance (`TOLERE` absent). Toutes ≤ 900 px de large après resserrage. Seules alertes : cotes à fond blanc (patron) et deux étiquettes à fond blanc sur le quadrillage clair.
- Vérification courbe ↔ énoncé : les données des figures (`DONNEES`) sont celles que relit `verif_259.py`.

## Contrôles

- `verif_259.py` : 280 contrôles justes.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (50 nouvelles images, 0 image en ligne conservée, 0 non appelée ; notes : 21 titres changés). Après les dernières retouches (2680, fiche, figure de proportionnalité) : vérificateur relancé (OK) + `controle_apercu.mjs` avec captures : **aucun problème détecté** (cours, fiche, 21 exercices × 3 onglets, téléphone et ordinateur).
- Captures téléphone regardées : cours (parties I à V), fiche, exercices 2675 et 2680 (étapes, recadrées à taille réelle). Corrigé après captures : figure « proportionnelles / non proportionnelles » refaite en colonne (trop petite sur téléphone en trois panneaux) ; « m³ » qui passait seul à la ligne après une formule (unité mise dans la formule) ; tableau « on cherche / méthode / exemple » de la fiche passé de 3 à 2 colonnes (trop serré).
- Espaces insécables avant les unités (€, cm, m, h, min, s, °C, km/h, bar…) : 668 dans les exercices, plus le cours et la fiche.
- Seuls mes propres processus ont été lancés ; verrous `outils/.verrous` respectés (gérés par les outils).

## Remarques pour l'orchestrateur

- 2675 et 2683 utilisent des formules du second degré, seulement pour **calculer** des valeurs (substitution, priorités) et lire la courbe : au programme de 4e (calcul littéral), sans résolution.
- 2679 : la courbe de refroidissement est exponentielle (moitié de l'écart tous les 15 min) ; l'élève ne fait que lire et comparer.
