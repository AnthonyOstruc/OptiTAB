# Notion 258 (4e) : Grandeurs composées et unités

**État : prêt** (claude-258, 2026-11-03). 21 exercices (aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée ; 3 exercices remplacés, 1 réorienté).

Programme de 4e (cycle 4) : grandeurs quotients (vitesse en km/h et m/s, débit, masse volumique, consommation, densité de population, prix unitaire) et grandeurs produits (énergie en kWh, passagers-kilomètres) ; calculs et conversions d'unités composées (km/h ↔ m/s, L/min ↔ m³/h, g/cm³ ↔ kg/m³) ; durées en heures et minutes ; problèmes concrets.

## Cours et fiche

- **Titres** inchangés : « Grandeurs composées et unités » et « Résumé : Grandeurs composées et unités ».
- **Cours 253 réécrit façon manuel** (l'ancien mélangeait des exemples dans des encadrés « définition », des puces « • », un renvoi « onglet Fiches », et ne parlait ni de grandeur produit/quotient en tant que telles, ni de consommation, densité, passagers-km, conversion L/min ↔ m³/h) : I. grandeurs quotients et produits (définitions, « lire une unité ») ; II. durées en base 60 (frise, deux méthodes, erreur $2{,}3$ h) ; III. vitesse moyenne ($v$, $d$, $t$, schéma de trajet, unités cohérentes, conversion km/h ↔ m/s justifiée, vitesse moyenne ≠ moyenne des vitesses) ; IV. débit, masse volumique, consommation, densité de population, tableau récapitulatif ; V. énergie (kWh) et passagers-km ; VI. volumes et contenances (tableau de conversion), convertir une grandeur quotient (méthode « haut et bas séparément » en `aligned`) ; contrôle d'un résultat ; à retenir.
- Exemples du cours choisis pour ne pas doubler les exercices.
- **Fiche 173 refaite** : tableau des 7 grandeurs (formule, unités), durées, conversions, 5 erreurs classiques, réflexe.
- Espace insécable entre chaque nombre et son unité (comme 256), pour qu'une unité ne passe jamais seule à la ligne.

## Exercices (21)

- **Tous réécrits** : questions numérotées ; corrigé avec méthode, étapes détaillées, résultat encadré à chaque question, erreur fréquente et/ou « À retenir » dans chaque exercice ; `Solution:` courte et cohérente. Titres « Type - Sujet » (« Grandeurs - n. » retiré, 21 titres changés). `\displaystyle` et lignes `Image:` de la conversion retirés.
- **Progression** dans l'ordre des Id : 7 Découverte (2642-2648), 7 Entraînement (2649-2655), 4 Problème (2656-2659), 3 **Type brevet** (2660-2662 ; il n'y en avait aucun).
- **Remplacés (3)** :
  - 2655 « Le prix au kilogramme » (proportionnalité, déjà vue en 257) → « Entraînement - Densité de population » (Paris, France métropolitaine, Lozère ; retrouver une population, une aire) : la densité n'était travaillée nulle part ;
  - 2658 « Les records d'Usain Bolt » (doublon des conversions de 2643, 2645 et du marathon 2651) → « Problème - Les passagers-kilomètres d'une ligne de bus » (grandeur produit tronçon par tronçon, consommation L/100 km, CO₂ par passager-km, comparaison avec la voiture, vitesse moyenne) ;
  - 2662 « La vitesse de la Terre » (surtout notation scientifique et périmètre, trop loin de la notion) → « Type brevet - Un trajet en voiture » (compteurs kilométriques, horaires, durée en heures et minutes avec pause, deux vitesses moyennes, consommation et coût, distance parcourue en 2 s à 130 km/h).
- **Réorienté** : 2654 « Le débit d'un fleuve » → « Entraînement - Convertir des débits » (L/min → L/h → m³/h, m³/h → L/min, L/s → L/min, Seine en m³/h, comparer deux tuyaux) : la conversion L/min ↔ m³/h du programme n'était pas travaillée.
- **Réécrits en partie** : 2643 (question 6 « scooter / guépard » doublon de 2645 → vitesse d'un train en $2$ h $15$ min) ; 2644 (questions 5-6 sur l'orage, doublon de 2657 → TGV en $1$ h $12$ min, piéton en minutes) ; 2647 (ajout de la conversion en m³/h) ; 2648 (ajout de la masse volumique en kg/m³) ; 2649 (données changées : les deux parties roulées étaient à 60 km/h, peu instructif → 60 puis 70 km/h, moyennes 55 et 66 km/h) ; 2653 (ajout d'un compteur électrique à compléter) ; 2660 et 2661 passés en Type brevet (piscine : jour et heure de fin du remplissage, filtration en h min, baisse du niveau ; glace : rédaction brevet) ; 2651 (le record de Berlin 2022 n'est plus le record du monde : formulation corrigée).
- **Erreurs corrigées** : conversion cassée (2648 question 5 « $0{,}6 1$ » : signe « < » perdu) ; résultats sans étapes ni méthode (conversion automatique) ; 2661 volume total recalculé avec la valeur exacte ($97\,619$ m³, environ $98\,000$ m³).
- `verif_258.py` : **217 contrôles** sympy en valeurs exactes (Rational) : chaque calcul, conversion, arrondi, durée en h min s, jour et heure de fin, du cours, de la fiche et des 21 exercices, tous justes.

## Figures (style livre, `figures/figures.py`)

- **34 figures neuves, 38 emplacements** ; les **13 images matplotlib en ligne sont toutes remplacées** (0 conservée).
  - Cours (5) : frise heures décimales / minutes ; schéma de trajet ($210$ km, $3$ h, $70$ km/h) ; conversion m/s ⇄ km/h ($\times 3{,}6$ / $\div 3{,}6$) ; robinet et cuve (débit) ; tableau de conversion des volumes et contenances (vrai tableau, trois colonnes par unité, zéros ajoutés en vert). Fiche (2) : conversion des vitesses et tableau des volumes.
  - Exercices, énoncé **et** corrigé (réponses en vert) : 2644 (trajet), 2646 (tableau vide, puis rempli), 2647 (robinet et baignoire), 2648 (trois cubes, puis masses volumiques), 2649 (graphique distance-durée, puis vitesses et arrêt), 2650 (aller-retour, puis durées), 2652 (aquarium), 2653 (compteur électrique, puis index de fin de mois), 2657 (orage, puis deux éclairs et le rapprochement), 2658 (ligne de bus, puis passagers-km), 2659 (baignoire avec bonde, puis débit réel), 2660 (piscine), 2661 (iceberg, puis pourcentages), 2662 (compteurs kilométriques et horaires, puis trajet avec distance, durée et vitesses) ; corrigés seuls : 2642 (frise $1{,}75$ h $= 1$ h $45$ min), 2645 (schéma de conversion).
- `figures_livre.py` : 0 chevauchement texte / trait, **aucune tolérance** (`TOLERE` vide), 0 alerte ; toutes entre 434 et 862 px. Après relecture : cotes vertes des trajets remplacées par un texte au-dessus de la cote (le vert sur la cote déclenchait le détecteur), masses des cubes écrites sous les cubes, réponses des bassins sous la figure (elles croisaient une arête cachée), étiquettes « heures / minutes » des frises retirées (elles touchaient « 0 h »), « surface de la mer » déplacée (elle coupait l'iceberg), texte de la baignoire raccourci ; après les captures téléphone, 21 figures resserrées (frises, trajets, conversion, tableau des volumes, graphique, aller-retour, bassins, cubes, orage, ligne de bus, compteurs) pour ne plus être réduites à l'écran.

## Contrôles

- `verif_258.py` : 217 contrôles justes.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (notes : 21 titres changés ; 0 image en ligne conservée, 0 non appelée), avant et après le resserrement des figures.
- `controle_apercu.mjs` avec captures (téléphone et ordinateur, cours, fiche, 21 exercices × 3 onglets) : **aucun problème détecté**. Captures regardées : cours (4 écrans), fiche, exercices 2660 (étapes) et autres. Seuls mes processus ont tourné ; le verrou `chrome_0.lock` d'un autre agent a été laissé.

## Remarques pour l'orchestrateur

- **Défaut du moteur** (déjà signalé dans le commentaire de `optitabDoc.js`) : le navigateur peut couper la ligne juste après une formule même devant une espace insécable ; on voit donc parfois « $1\,000$ » en fin de ligne et « L » au début de la suivante (fiche, partie III). Correctif possible dans le moteur : ajouter les unités usuelles (h, min, s, km, m, L, kg, g, €, %, kWh…) au `trail` de la regex qui crée `otm-nb` (ligne ~466), comme pour la ponctuation. Je n'ai pas modifié `frontend/src/`.

- 2649 (graphique distance-durée) recoupe un peu la notion 259 « Relier des grandeurs et lire des graphiques » : ici l'accent est mis sur le calcul des vitesses.
- Les données de 2655 (densités) sont des valeurs arrondies, annoncées comme telles dans l'énoncé.
