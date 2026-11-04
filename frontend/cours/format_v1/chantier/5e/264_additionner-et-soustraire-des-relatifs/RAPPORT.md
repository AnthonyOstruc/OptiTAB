# Notion 264 (5e) : Additionner et soustraire des relatifs

## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-10-exercices-264, 2026-11-04). 10 exercices gardés (Id inchangés, tous réécrits), 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`. Base de départ : `source_en_ligne/` (ré-export du 04/11). Sauvegarde de l'état de départ : `sauvegardes/refonte_2026-11-04/`.

Consigne appliquée : pas de « Type brevet » en 5e ; les deux exercices de fin sont des « Synthèse - … ». Aucune mention du brevet (contrôlé par `verif_264.py`).

### Cours et fiche

- **Titres** inchangés : « Additionner et soustraire des relatifs » et « Résumé : Additionner et soustraire des relatifs ».
- **Cours 259 réécrit façon manuel** (l'ancien tenait en 4 encadrés, sans somme algébrique ni écriture simplifiée, une seule figure) : objectifs, prérequis (distance à zéro, opposé) ; I. l'addition comme déplacement (figure), règles même signe / signes contraires / opposés avec exemples entiers et décimaux, méthode, erreur fréquente ; II. soustraire = ajouter l'opposé (figure), exemples, « deux signes, deux rôles », terme manquant ; III. somme algébrique : définition, tableau de l'écriture simplifiée, changer l'ordre des termes, regroupements, parenthèses calculées d'abord, piège $10 - 4 - 3 \ne 10 - (4 - 3)$ ; IV. variation et écart : définitions, thermomètre, altitudes (mouette / poisson), distance sur une droite graduée, méthode de résolution de problème, « valeur, variation ou écart ? » ; « À retenir ». Exemples tous différents des exercices.
- **Fiche 179 refaite** : 4 parties (règles d'addition, soustraction et terme manquant, somme algébrique, variation et écart), 4 erreurs classiques, 2 figures.

### Exercices gardés (10)

| Id | Titre | Contenu |
|---|---|---|
| 2772 | Découverte - Additionner sur une droite graduée | trois additions sur droites graduées, opposés, règles avec décimaux, erreur de Tom |
| 2773 | Découverte - Soustraire, c'est ajouter l'opposé | opposés, transformations, décimaux, déplacements sur droites, $a - b$ et $b - a$ |
| 2768 | Découverte - Les températures d'une journée | lecture d'un thermomètre, hausses et baisses, variation, écart |
| 2779 | Entraînement - Calculer des sommes algébriques | écriture simplifiée, regroupement positifs / négatifs, opposés, erreur de Mila |
| 2780 | Entraînement - Calculer avec des parenthèses | parenthèses calculées d'abord (entiers, décimaux), $15 - 7 - 3$ / $15 - (7 - 3)$, erreur de Lucas |
| 2769 | Entraînement - Pyramides et termes manquants | pyramides additives, case manquante par soustraction, variation du sommet, additions à trous |
| 2787 | Problème - La plongée du sous-marin | altitudes successives, variation de deux façons, distance parcourue, écart avec un goéland |
| 2786 | Problème - Le compte du club de théâtre | soldes successifs (décimaux), solde minimal, variation, versement minimal, objectif de 20 € |
| 2770 | Synthèse - Une semaine à la station de ski | lecture de thermomètre, amplitudes, variations, gel, températures de samedi |
| 2771 | Synthèse - Le jeu de la piste graduée | parcours de pions, somme de cartes, carte cachée, distance, gagnant, ordre des termes |

Progression 3 Découverte / 3 Entraînement / 2 Problème / 2 Synthèse. Chaque corrigé : méthode, étapes détaillées et alignées, résultat encadré, erreur fréquente ou « À retenir ». Niveau vérifié pour chacun : calculs de 5e uniquement (additions, soustractions de relatifs entiers et décimaux), aucune multiplication de relatifs. Couverture : `COUVERTURE.md`.

- 2772, 2773, 2779, 2780, 2786, 2787 : thème gardé, contenu refait et complété (droites graduées, décimaux, analyse d'erreur, tableau d'opérations, distance parcourue).
- 2768 : la « station météo » gardée une seule fois, enrichie (thermomètre, nuit, écart).
- 2769, 2770, 2771 : refaits de zéro (même Id, nouveau titre) : c'étaient des copies de 2768.
- Ancien contenu : pas d'erreur de calcul ; défauts corrigés : 15 exercices sur 21 identiques à des valeurs près, aucune figure, aucun travail sur l'écriture simplifiée ni sur les termes manquants ; l'ancienne question « supprimer la parenthèse précédée de − » (règle de 4e) est remplacée par un calcul de la parenthèse d'abord.

### Exercices retirés (11)

2774, 2775, 2776, 2777, 2778, 2781, 2782, 2783, 2784, 2785, 2788 : copies de « La station météo / La sonde de montagne / Le journal de températures » (mêmes six questions, autres températures).

### Figures (style livre, `figures/figures.py`)

- **19 figures neuves, 21 emplacements** ; l'ancienne image du cours (droite graduée de 2026-10-28) est remplacée ; 0 image en ligne conservée.
- Cours (4) : additions sur droite graduée, soustractions sur droite graduée, thermomètre (variations +12 / −6), altitudes (écart 21 m). Fiche (2) : additions, thermomètre.
- Exercices : droites graduées avec le départ à l'énoncé et déplacement + arrivée en vert au corrigé (2772, 2773) ; thermomètre énoncé / corrigé avec les variations (2768, 2770) ; pyramides vides puis complétées, pyramide modifiée (2769) ; axe des altitudes du sous-marin, trajet et écart en vert (2787) ; piste graduée, parcours en escalier des deux pions (2771).
- Valeurs dessinées calculées dans `figures.py` et revérifiées. `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance ; toutes ≤ 900 px. Après relecture sur téléphone : sous-marin, pyramides et piste rétrécis.

### Contrôles

- `verif_264.py` : **305 contrôles** sympy en fractions exactes (règles des signes recalculées, cours, fiche, chaque question, erreurs analysées, valeurs des figures, solutions écrites, progression et titres), tout juste.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (notes : 10 titres changés, 11 exercices retirés volontairement). Journal : `264_validation.log`.
- `controle_apercu.mjs` avec captures (`captures_refonte/`) : « Aucun problème détecté » (64 vues, téléphone et ordinateur). Journal : `264_captures.log`.
- Captures téléphone regardées en deux passes groupées (cours, fiche, exercices). Corrigé après la 1re passe : calculs côte à côte (`\qquad`) empilés, tableaux larges transposés (soldes, températures, amplitudes, règles de la fiche), chaînes longues découpées, point orphelin, figure du sous-marin resserrée ; après la 2e : sommes des pyramides en liste, pyramides et piste rétrécies.

### Remarques pour l'orchestrateur

- Après `publier_lot.ps1 5e 264` : `retirer_exercices.py` pour les 11 Id de `exercices_retires.txt`.
- Programme : addition / soustraction de relatifs entiers et décimaux, sommes algébriques, variation et écart. La multiplication (4e) et la suppression de parenthèses précédées de « − » dans le calcul littéral (4e) ne sont pas traitées.

---

## Historique : révision du 30 octobre 2026

(Rapport précédent conservé dans `sauvegardes/refonte_2026-11-04/RAPPORT_avant.md`.) 21 identifiants conservés, six variantes remplacées (2772, 2773, 2779, 2780, 2786, 2787), 1 figure de cours, 223 + 228 contrôles. Aucun import, aucune écriture en base.
