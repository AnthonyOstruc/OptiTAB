# Notion 130 — Repérer, comparer et arrondir (6e)

## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-10-exercices-130). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés, 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde des fichiers finaux et des figures d'avant la refonte : `sauvegardes/avant_refonte_20261104/`.

Programme vérifié : programme du cycle 3 (BO n° 16 du 17 avril 2025) et exemples de réussite de 6e (Eduscol) : placer et repérer un décimal sur une demi-droite graduée (graduation adaptée aux nombres) ; comparer, ordonner, signes ⩽ et ⩾ ; arrondi à l'unité, au dixième, au centième d'un décimal et de certains nombres non décimaux (1/3 ≈ 0,33 ; π ≈ 3,14) ; encadrer, intercaler ; ordre de grandeur pour contrôler un résultat. Rien des classes suivantes ; aucune mention du brevet. Écriture des décimaux et numération laissées à la notion 129 (pas de doublon).

### Cours et fiche
- **Cours 133 réécrit façon manuel** (titre inchangé) : I. demi-droite graduée (origine, unité, abscisse, lire / placer, erreur traits-intervalles, zoom dixièmes → centièmes) ; II. comparer et ranger (méthode rang par rang, figure 6,25 < 6,3, pièges, symboles <, >, ⩽, ⩾, ordre croissant / décroissant) ; III. encadrer (unité, dixième, centième) et intercaler (infinité de nombres) ; IV. arrondi (définition, règle du chiffre qui suit, retenues, nombres non décimaux 1/7 et π, erreur de l'arrondi en cascade) ; V. ordre de grandeur (estimer, contrôler, limite d'un budget) ; « À retenir ».
- **Fiche 200 refaite** : 5 parties denses, 2 figures, 5 erreurs classiques.
- Exemples du cours et de la fiche tous différents de ceux des exercices.

### Exercices gardés (10) — tous réécrits entièrement
| Id | Titre | Capacités |
|---|---|---|
| 3209 | Découverte - Lire et placer des nombres sur une demi-droite graduée | unité en 10, lire, placer, 1,05 au milieu d'un intervalle, ranger |
| 3210 | Découverte - Comparer deux nombres décimaux | <, >, = (2,5 / 2,15 ; 12,09 / 12,1…), erreur « 15 > 5 » sur la demi-droite, vrai-faux avec ⩽ et ⩾ |
| 3213 | Découverte - Arrondir un nombre décimal | arrondis unité / dixième / centième (retenues 9,96 et 0,295), milieu 4,75, 1/3, 2/3, 5/6, arrondi en cascade |
| 3216 | Entraînement - Zoomer sur une demi-droite graduée | encadrer au dixième, zoom en centièmes, lire, placer 5,35 et 5,325, arrondi sur la figure |
| 3217 | Entraînement - Ranger des temps et des longueurs | ordre croissant avec égalité, classement ex æquo, condition ⩽ 31,45, ordre décroissant |
| 3211 | Entraînement - Encadrer et intercaler des nombres décimaux | encadrer 23,186 à trois précisions, intercaler, infinité, les 9 centièmes entre 4,6 et 4,7 |
| 3215 | Problème - Partager une addition en trois | 47 ÷ 3 = 15,666…, arrondis, 3 × 15,67 = 47,01, partage exact 15,67 + 15,67 + 15,66 |
| 3214 | Problème - Estimer le prix des fournitures | ordre de grandeur, virgule mal placée, limite 22 € (valeur exacte nécessaire), majoration |
| 3212 | Problème - Le nombre mystère | encadrements et arrondis successifs, 19 → 10 → 5 → 1 candidat (6,48, unicité vérifiée) |
| 3229 | Synthèse - Le concours de saut en longueur | lecture en centièmes, rangement décroissant, arrondis au dixième qui cachent le gagnant, intercaler, encadrer |

Progression : 3 Découverte, 3 Entraînement, 3 Problème, 1 Synthèse. Chaque corrigé : méthode, étapes détaillées, résultat encadré, erreur fréquente ; `Solution:` courte.

### Exercices retirés (11)
Les 21 exercices en ligne étaient 7 énoncés répétés 3 fois (« Parcours 1, 2, 3 »), avec des corrigés génériques (« Raisonnement et calcul »). On garde un Id par capacité, réécrit de zéro ; les copies sont retirées : 3220, 3227 (arrondir), 3221, 3228 (comparaisons fausses), 3218, 3225 (encadrer), 3223 (graduation), 3224 (ranger), 3219, 3226 (intercaler), 3222 (seuil, idée reprise dans 3214 et 3215).

### Figures (16 neuves, style livre, `figures/figures.py`)
- Les 4 anciennes images (3 graduations identiques, arrondi de 7,364) sont supprimées du dossier (copie dans la sauvegarde) ; aucune image en ligne conservée ; 1 image en ligne non appelée sera supprimée à l'import.
- Cours (5) : demi-droite en dixièmes, zoom 2,64, comparer 6,25 et 6,3, encadrer 8,463, arrondi de 3,47 ; fiche (2) : zoom et arrondi.
- Exercices : 3209 (énoncé / corrigé), 3210 (énoncé / corrigé), 3213 (arrondi de 4,738), 3216 (zoom énoncé / corrigé), 3211 (encadrement illustré en deux niveaux), 3212 (zones des indices), 3229 (décamètre énoncé / corrigé). Réponses en vert ; énoncés sans réponse (contrôlé).
- Positions calculées en fractions exactes. `figures_livre.py` : 0 chevauchement, aucune tolérance ; largeurs 657 à 783 px (resserrées après la 1re passe téléphone).

### Contrôles
- `verif_130.py` : **143 contrôles** sympy, 0 échec (chaque réponse, arrondis, unicité du nombre mystère, textes des figures, énoncés sans réponse, structure des corrigés, progression, 10 + 11 = 21, absence de « brevet »). Journal : `130_verification.log`.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`130_validation.log`). `controle_apercu.mjs` : 64 vues sur 64 sans problème (`captures.log`).
- Captures téléphone regardées en deux passes : cours (5 écrans), fiche, exercices 3209, 3216, 3213, 3215, 3229. Corrigé après la 1re passe : figures trop petites (ramenées vers 660 px), tableaux larges transposés (3213, 3217, 3229, 3214), tableau des symboles et des arrondis du cours passés en listes ; étiquette « 7 centièmes » éloignée du trait du milieu.

### Pour l'orchestrateur
- Après `publier_lot.ps1 6e 130`, lancer `retirer_exercices.py` (11 Id).
- Les anciens fichiers de l'autre session (captures_6e, verif_math_6e.py, revision_pedagogique_6e.json…) concernent l'ancienne version : laissés en place, non utilisés.

---

## Historique
Notion 130 — prête le 1er novembre 2026 (autre session) : cours réécrit, 21 exercices en 7 familles × 3 parcours, 4 figures. Remplacé par la refonte ci-dessus.
