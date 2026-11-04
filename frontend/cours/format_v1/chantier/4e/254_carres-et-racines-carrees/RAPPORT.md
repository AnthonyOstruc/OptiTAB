# Notion 254 (4e) : Carrés et racines carrées

**État : prêt** (agent-4e-254, 2026-11-03). 21 exercices (aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée ; 2 exercices remplacés).

## Cours et fiche

- **Titres** inchangés : « Carrés et racines carrées » et « Résumé : Carrés et racines carrées » (intitulé de la notion).
- **Cours 249 réécrit façon manuel** (la conversion automatique avait perdu la moitié du contenu et mis des exemples dans un encadré « définition ») : objectifs en liste ; I. carré d'un nombre (définition, exemples entier / décimal / fraction / négatif, signe d'un carré, piège $(-6)^2$ / $-6^2$ et priorités, carrés parfaits en quadrillage, tableaux natifs $1^2$ à $12^2$ + $13^2$, $14^2$, $15^2$) ; II. racine carrée (définition, exemples dont $\sqrt{0{,}25}$ et $\sqrt{9/16}$, propriété $\sqrt{a^2} = a$ et $(\sqrt{a})^2 = a$, côté d'un carré d'aire $A$, erreurs : $\sqrt{-4}$, « racine = moitié », racine d'une somme) ; III. encadrer et approcher (propriété « mêmes ordres que les carrés », méthodes entier puis dixième, valeur exacte / valeur approchée, ne pas écrire $=$, comparer $\sqrt{30}$ et $5{,}5$) ; IV. équation $x^2 = a$ (trois cas, exemples, méthode $3x^2 = 75$, une longueur est positive) ; V. vers Pythagore (carrés construits sur un triangle 3-4-5) ; « À retenir ». Emojis, HTML, `\displaystyle` et renvoi « onglet Fiches » supprimés.
- **Programme** : $\sqrt{ab}$ et les simplifications ne sont plus présentés (non exigibles en 4e) ; l'ancien exercice 2562 en tirait une règle générale à partir d'un seul exemple, il est réécrit.
- L'exemple « chute de 44,1 m » du cours (doublon de l'exercice 2567) est remplacé par l'équation $3x^2 = 75$.
- **Fiche 169 refaite** : carrés (pièges, tableaux des carrés parfaits), racine carrée (définition encadrée), encadrer / approcher / comparer, tableau natif des solutions de $x^2 = a$, 5 erreurs classiques, réflexe ; plus de puces « • ».

## Exercices (21)

- **Tous réécrits** au format des modèles : questions numérotées ; corrigé avec méthode, étapes détaillées, résultat encadré à chaque question, au moins une erreur fréquente par exercice (+ « À retenir » dans 15 exercices) ; `Solution:` courte et cohérente ; titres « Type - Sujet » (« Racines - n. » retiré, 21 titres changés). Les étapes vides ou tronquées de la conversion automatique (inégalités coupées : « $4{,}4^2 = 19{,}36 20$ », « $7^2 = 49 150$ ») sont refaites.
- **Progression** : 7 Découverte (2558-2564), 7 Entraînement (2565-2571), 4 Problème (2572-2575), 3 **Type brevet** (2576-2578), dans l'ordre des Id.
- **Remplacés (2 doublons)** :
  - 2568 « La distance de freinage » (formule avec un carré, même déroulé que 2567 chute libre) → « Entraînement - Comparer et ranger des racines carrées » (compétence du programme absente : comparer par les carrés, ranger $\sqrt{10}$ ; $3$ ; $\sqrt{8}$ ; $3{,}2$ ; $\sqrt{12}$, entiers entre $\sqrt{20}$ et $\sqrt{70}$, $\sqrt{0{,}36} > 0{,}36$) ;
  - 2574 « Le pendule » (formule avec une racine, même déroulé que 2577 tsunami) → « Problème - Construire une mosaïque carrée » (carrés parfaits en quadrillage, plus grand carré avec 500 carreaux, $(n+1)^2 - n^2 = 2n + 1$ lu sur la figure, carreaux du bord de deux façons).
- **Réécrits en partie** : 2562 (racine d'une somme, contre-exemple, cas $b = 0$ ; plus de règle du produit) ; 2564 (calculs de carrés avec $(-5)^2$ / $-5^2$, décimaux, fractions ; les racines de sommes de carrés, doublon de 2562 et 2575, retirées) ; 2558 (comptage sur quadrillage, tableaux natifs au lieu d'images, $0{,}3^2$ déplacé dans 2564) ; 2559 ($\sqrt{4/9}$, affirmation « $\sqrt{25} = -5$ ») ; 2563 ($x^2 = 0{,}36$ au lieu d'un second $x^2 = 64$) ; 2571 (énigmes 3 et 5 changées : deux réponses « 7 » et doublon de $n^2 < 500 < (n+1)^2$ avec la mosaïque) ; 2570 (carré nommé $BDEF$, construction justifiée par les diagonales qui se coupent en $C$) ; 2573 (coefficient $\sqrt{2}$ justifié par $(\sqrt{72}/6)^2 = 2$).
- 2576, 2577, 2578 passés en « Type brevet » (achat avec pourcentage et boîtes ; formule, conversions, durée en h min ; aires de disques et prix au cm²).
- **Erreur corrigée** : aucune erreur de maths dans l'ancien contenu, mais des inégalités tronquées par la conversion (voir plus haut). `verif_254.py` : **161 contrôles** sympy (valeurs exactes, arrondis, encadrements, équations, géométrie de la figure de Socrate), tout juste.

## Figures (style livre, `figures/figures.py`)

- **30 figures neuves, 33 emplacements** ; les **17 images matplotlib en ligne sont toutes remplacées** (0 conservée, 0 non appelée).
  - Cours (4) : carrés parfaits en quadrillage ($1^2$ à $5^2$), carrés d'aire 25 et 20 cm² et leurs côtés, encadrement de $\sqrt{20}$ par zoom (entiers puis dixièmes, en vert), carrés construits sur un triangle 3-4-5.
  - Fiche (2) : carrés d'aire donnée, encadrement de $\sqrt{20}$.
  - Exercices (27 emplacements, 17 exercices) : énoncé + corrigé en vert pour 2558 (quadrillage), 2559 (carré de 49 cm²), 2560 (trois carrés), 2561 (droite graduée vierge puis placée), 2565 (deux potagers), 2566 (rectangle et carré), 2570 (carré de Socrate sur la diagonale), 2572 (allée en quatre rectangles), 2574 (mosaïques, puis équerre « colonne + rangée + coin » et bord) et 2575 (puzzle, puis triangle 3-4-5) ; corrigés seuls : 2567 (courbe $d = 4{,}9t^2$), 2568 (rangement sur une droite), 2569 (trois zooms sur $\sqrt{2}$), 2573 (photo de côté doublé = 4 photos), 2576 (pièce de 15 × 15 carreaux) ; énoncé seul : 2578 (pizzas).
  - Les tableaux de carrés parfaits (anciennes images) sont des **tableaux natifs**.
- `figures_livre.py` : 0 chevauchement texte / trait, **aucune tolérance** (`TOLERE` vide) ; toutes ≤ 900 px. Après relecture : cotes contenant une racine écrites **sous** la flèche (la barre du radical prolongeait la flèche) ; zooms de $\sqrt{2}$ resserrés (pointillés qui touchaient les textes, « 1,414 » et « 1,415 » collés) ; courbe de chute sans quadrillage, coordonnées raccourcies (une étiquette touchait un pointillé) ; longueurs du triangle 3-4-5 desserrées ; diagonales de $BDEF$ tracées seulement hors du carré $ABCD$.

## Contrôles

- `verifier_notion.py` : **OK, 0 problème** (notes : 21 titres changés ; 0 image en ligne conservée). `verif_254.py` : 161 contrôles justes.
- Contrôle Chrome : avec `--navigateur`, toutes les vues ont été contrôlées sans défaut, mais Chrome ne s'est pas refermé (défaut connu, § 3 de la consigne de lot) ; procédure de repli appliquée : vérificateur sans navigateur OK + `controle_apercu.mjs` avec captures, **130 vues sur 130 sans défaut** (cours, fiche, 21 exercices × 3 onglets, téléphone et ordinateur). Seuls mes propres processus Node bloqués ont été arrêtés, et leurs verrous `chrome_*.lock` libérés.
- Captures téléphone regardées : cours (4 écrans), fiche, exercices 2558 (énoncé), 2560, 2568, 2569, 2570, 2574 (étapes). Corrections faites après relecture : tableaux de carrés parfaits à 7 colonnes coupés (« 144 » invisible) → 3 tableaux de 4 valeurs (cours, fiche, 2558) ; tableau à 6 colonnes de 2568 → tableau vertical ; formules à deux membres réduites (encadrements du cours, carrés de 2569, 2559, 2561, 2562, 2567) → une formule par ligne ; figures trop larges (texte trop petit sur téléphone) resserrées : quadrillage du cours (4 carrés), encadrement de $\sqrt{20}$, droites de 2561 et 2568, zooms de 2569, courbe de 2567, trois carrés de 2560, photos de 2573, pizzas de 2578, potagers de 2565, rectangle de 2566, triangle 3-4-5.

## Remarques pour l'orchestrateur

- La propriété « deux nombres positifs sont rangés dans le même ordre que leurs carrés » est énoncée et utilisée (comparer, encadrer), sans démonstration (niveau 4e).
- Le cours et 2 exercices (2562, 2575) préparent Pythagore par les aires sans énoncer le théorème (notion 283).
