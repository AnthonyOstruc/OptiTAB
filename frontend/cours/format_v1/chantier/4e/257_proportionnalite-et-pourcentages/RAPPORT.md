# Notion 257 (4e) : Proportionnalité et pourcentages

**État : prêt** (claude-257, 2026-11-03). 21 exercices (aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée ; 2 exercices remplacés).

Programme de 4e (cycle 4) : reconnaître la proportionnalité (tableau, graphique), quatrième proportionnelle (produit en croix justifié), appliquer et calculer un pourcentage, augmentation / réduction, échelles, vitesse moyenne (distance proportionnelle à la durée). Les évolutions successives (3e) n'apparaissent qu'en découverte (2625 Q6) et dans une mise en garde du cours.

## Cours et fiche

- **Titres** inchangés : « Proportionnalité et pourcentages » et « Résumé : Proportionnalité et pourcentages ».
- **Cours 252 réécrit façon manuel** (la conversion avait des puces « • », un exemple sans corps, un renvoi « onglet Fiches ») : objectifs en liste ; I. reconnaître (méthode des quotients, exemple, piège « l'un augmente, l'autre aussi » avec la taille d'un enfant, propriété graphique et ses deux conditions) ; II. quatrième proportionnelle (passage à l'unité, linéarité, **produit en croix énoncé et démontré**, calcul aligné, mise en garde : seulement si la proportionnalité est justifiée) ; III. pourcentages (appliquer, calcul mental, **calculer un taux** avec le total de référence, hausse / baisse et coefficient, prix avant réduction par un tableau de proportionnalité, hausse puis baisse de 10 % renvoyée à la 3e) ; IV. échelles (définition, propriété $1/n$, conversions, échelle > 1) ; V. **vitesse moyenne** ($d = v \times t$, conversion des durées, cas d'un arrêt) ; « À retenir ».
- **Fiche 172 refaite** : tableau natif « Je veux… / Je calcule » pour les pourcentages, échelles et vitesse, 5 erreurs classiques, réflexe.

## Exercices (21)

- **Tous réécrits** au format des modèles : questions numérotées ; corrigé avec méthode, étapes détaillées, résultat encadré à chaque question, au moins une erreur fréquente ou un « À retenir » par exercice ; `Solution:` courte et cohérente ; `\displaystyle` et `Image:` de la conversion retirés ; titres « Type - Sujet » (« Proportionnalité - n. » retiré, 21 titres changés).
- **Progression** : 7 Découverte (2621-2627), 7 Entraînement (2628-2634), 4 Problème (2635-2638), 3 **Type brevet** (2639-2641, il n'y en avait aucun), dans l'ordre des Id.
- **Remplacés (évolutions successives, programme de 3e, en doublon avec 2625 Q6)** :
  - 2632 « Évolutions successives » → « Entraînement - Calculer un taux en pourcentage » (compétence « calculer un taux » peu travaillée : partie / total, tableau de proportionnalité, taux de réduction et d'augmentation, comparer deux classes d'effectifs différents).
  - 2636 « Les soldes successives » → « Problème - Comparer les résultats de deux collèges » (taux de réussite, pourcentage d'un pourcentage avec changement de référence, objectif, hauteurs d'un diagramme en barres proportionnelles aux taux).
- **Réécrits en partie** : 2638 « L'évolution d'une population » (+4 % deux années, 3e) → « Problème - Comparer deux cyclistes sur un graphique » (lecture, proportionnalité distance / durée, pause, rattrapage $18t = 24$, vitesse moyenne pause comprise) ; 2623 (le calcul de taux part dans 2632 : calcul mental 50 %, 25 %, 10 % et effectif de demi-pensionnaires) ; 2625 (prix avant réduction par tableau de proportionnalité) ; 2629 (question sur les aires × 10 000, effet d'un agrandissement sur les aires = 3e, retirée) ; 2630 (question 6 incohérente « 11 yaourts » → 24 yaourts en lots de 3 ou de 8) ; 2633 (prix HT par tableau de proportionnalité) ; 2634 (question « doubler le rayon » fondue dans la 4, tableau natif côté / périmètre / aire) ; 2640 (aire × 6,25 retirée ; largeur pour 45 cm de haut, pourcentage rogné) ; 2639 (vérification en fractions exactes, équation alignée) ; 2635, 2637, 2641 restructurés (Type brevet pour 2639-2641).
- **Erreur corrigée** : aucune erreur de calcul dans l'ancien contenu. `verif_257.py` : **193 contrôles sympy** (rationnels exacts, arrondis, conversions de durées, équations, valeurs lues sur les figures), tous justes.

## Figures (style livre, `figures/figures.py`)

- **27 figures neuves pour 30 emplacements** ; les **12 images matplotlib en ligne sont toutes remplacées** (0 conservée, 0 non appelée).
  - Cours (7) : tableau × 3,5 ; graphique proportionnel / non proportionnel ; produit en croix (cases en croix colorées, sans trait sur le texte) ; barre de pourcentage (15 % de 240 €) ; coefficients multiplicateurs ; échelle graphique 1/25 000 ; distance / durée à 90 km/h.
  - Fiche (3) : graphique, produit en croix, coefficients.
  - Exercices (20 emplacements, 15 exercices) : énoncé + corrigé en vert pour 2624 (trois graphiques, lectures 9,6 € et 7,5 kg), 2629 (plan au 1/100, dimensions réelles), 2637 (carte cohérente avec l'échelle : sentier de 18 unités, vol d'oiseau de 11, échelle de 4), 2638 (cyclistes), 2640 (photos, papier 13 × 18 avec 1,5 cm qui dépasse) ; corrigés : 2621 (tableau complété), 2622 (produit en croix), 2625 (coefficients), 2627 (droite 90 km/h), 2628 (droite du carburant), 2633 (tableau HT / TTC), 2634 (périmètre droite / aire courbe, contre-exemple), 2636 (diagramme en barres des taux), 2639 (volumes de jus du mélange), 2641 (diagramme du prix d'une journée).
- `figures_livre.py` : 0 chevauchement texte / trait, **aucune tolérance** (`TOLERE` vide) ; toutes ≤ 900 px sauf ex2640_corrige (962 px, sous la limite de 1100). Chaque PNG regardé ; corrections après relecture : étiquette $A$ qui touchait $\mathcal{G}_2$ puis $\mathcal{G}_1$, lectures vertes de 2624 déplacées hors des courbes, étiquette « périmètre » qui coupait l'axe, légende du sentier sortie de la carte (elle croisait le tracé), sentier en lacets lissés, plan, photos et mélange resserrés.

## Contrôles

- `verifier_notion.py` : **OK, 0 problème** (notes : 21 titres changés ; 0 image en ligne conservée).
- `verif_257.py` : 193 contrôles sympy justes.
- Contrôle Chrome : `controle_apercu.mjs` avec captures, sur les fichiers finaux : **130 vues sur 130 sans défaut** (cours, fiche, 21 exercices × 3 onglets, téléphone et ordinateur). Comme pour les notions précédentes, Chrome ne s'est pas refermé après la dernière vue : seuls mes propres processus Node (PID 17712 puis 5496) ont été arrêtés et leur verrou `chrome_0.lock` libéré (le verrou `chrome_1.lock` d'un autre agent n'a pas été touché).
- Captures téléphone regardées : cours (parties I à V), fiche, exercices 2621 (énoncé), 2638 (étapes) et d'autres. Corrections faites après relecture : démonstration du produit en croix réduite sur téléphone → formule seule puis phrase ; tableau des pourcentages de la fiche qui se coupait → colonne « Je multiplie par » et ligne « pourcentage » sortie du tableau ; figure de l'échelle trop large (texte trop petit) → texte placé sous la barre ; figures de 2625 et 2629 déplacées vers la question qu'elles illustrent.

## Remarques pour l'orchestrateur

- Les vitesses sont traitées comme grandeur proportionnelle à la durée (programme de 4e) ; la notion 258 « Grandeurs composées » reprendra les conversions km/h ↔ m/s.
- 2639 (mélange) utilise une équation du premier degré (notion 256 de 4e).
