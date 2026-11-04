# Notion 263 — Découvrir les nombres relatifs (5e)

## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-10-exercices-263). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés, 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde des fichiers finaux et figures d'avant la refonte : `sauvegardes/avant_refonte_20261104/`.

### Cours et fiche
- **Cours 258 réécrit façon manuel** (titre inchangé) : I. des nombres pour aller « sous zéro » (thermomètre, définition, cas de 0, tableau de six situations : température, altitude, profondeur, étage, date avant J.-C., découvert) ; II. droite graduée (origine, sens, unité, abscisse, notation $E(-4)$, méthodes lire / placer, erreur « traits ou intervalles ») ; III. distance à zéro et opposé ; IV. **repère du plan** (absent avant) : axes, coordonnées (abscisse ; ordonnée), méthodes lire / placer, points sur les axes, erreur d'inversion ; V. comparer, ranger (croissant / décroissant), encadrer, erreurs fréquentes, « À retenir ».
- **Fiche 178 refaite** : signe et situations, distance à zéro et opposé, droite graduée et repère, comparaison, 5 erreurs classiques ; 2 figures.
- Exemples du cours et de la fiche différents de ceux des exercices. Aucune mention du brevet (consigne : en 5e, « Synthèse »).

### Exercices gardés (10) — tous réécrits entièrement
| Id | Titre | Capacités |
|---|---|---|
| 2747 | Découverte - Des nombres relatifs dans la vie courante | thermomètre, traduire altitude / profondeur / sous-sol / date, signe, cas de 0, ranger des dates |
| 2752 | Découverte - Lire et placer des points sur une droite graduée | graduation au demi, lire, placer, distance à l'origine |
| 2748 | Découverte - Distance à zéro et opposé | tableau signe / distance / opposé, opposés sur la droite, vrai-faux |
| 2749 | Entraînement - Lire et placer des points dans un repère | lire 6 points (dont 2 sur les axes), placer 3 points, signes des coordonnées, abscisse opposée |
| 2751 | Entraînement - Comparer et ranger des températures | < ou >, ordre croissant / décroissant, erreur « 7 > 4,5 », encadrer, intercaler |
| 2759 | Entraînement - Positions et distances à zéro | deux classements, égalités, opposés, ordre décroissant de décimaux négatifs |
| 2750 | Problème - L'ascenseur de la tour | étages négatifs, ranger, compter les étages de part et d'autre de 0, opposé |
| 2753 | Problème - Altitudes et profondeurs | lire des altitudes, ranger, opposés, écart de part et d'autre du niveau de la mer, intercaler |
| 2765 | Problème - Retrouver un nombre à partir d'indices | encadrements successifs avec distance à zéro, $x = -2{,}45$ (unicité vérifiée) |
| 2754 | Synthèse - Une journée à la station de ski | partie A températures (signe, rang, distance à 0) ; partie B plan (repère, opposé) |

Progression : 3 Découverte, 3 Entraînement, 3 Problème, 1 Synthèse. Chaque corrigé : méthode, étapes détaillées, résultat encadré, erreur fréquente ; `Solution:` courte. Niveau 5e vérifié pour chacun (pas d'addition ni de soustraction de relatifs, réservées à la notion 264 ; les écarts se comptent sur la figure de part et d'autre de 0 ; aucune division par un décimal).

### Exercices retirés (11)
- 2755, 2756, 2757, 2760, 2761, 2762, 2763, 2764, 2767 : le même exercice (« étages / températures / balises », points A, B, C sur une droite, 6 questions identiques) répété avec d'autres nombres.
- 2758 (encadrer −3,47) : capacité reprise dans 2751, 2759 et 2765.
- 2766 (trois critères de classement) : doublon de 2759 et 2765.

### Figures (23 neuves, style livre, `figures/figures.py`)
- Toutes les anciennes images (21 droites matplotlib + 2 de révision) sont supprimées du dossier (copie dans la sauvegarde) ; à l'import, les 9 images en ligne non appelées sont supprimées.
- Cours (5) : thermomètre positifs / négatifs, droite graduée annotée, opposés, repère du plan avec pointillés de lecture, comparer −8 et −3 ; fiche (2) : opposés, repère.
- Exercices : 2747 thermomètre (énoncé / corrigé en vert), 2752 droite au demi (énoncé / corrigé), 2748 opposés (énoncé / corrigé avec distances), 2749 repère (énoncé / corrigé), 2751 thermomètre des 7 villes, 2759 droite des points, 2750 coupe de la tour (énoncé / corrigé avec accolade), 2753 altitudes (énoncé sans valeurs / corrigé), 2765 agrandissement entre −2,7 et −2,3, 2754 thermomètre de la journée et plan de la station (énoncé / corrigé).
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance, toutes ≤ 900 px. Après les captures : droites resserrées (≈ 650 px), températures des villes et de la journée passées en thermomètres, altitudes sur deux lignes, figures larges sorties des étapes (lisibilité téléphone).

### Contrôles
- `verif_263.py` : **113 contrôles** sympy (valeurs exactes) : chaque réponse, rangement, opposé, coordonnée, unicité de $x = -2{,}45$, cohérence figures / textes, absence du mot « brevet », structure de chaque corrigé — tout juste.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (notes : 10 titres changés, 11 exercices retirés volontairement). `controle_apercu.mjs` avec captures : 64 vues sur 64 sans problème (téléphone et ordinateur). Journaux : `263_validation.log`, `captures.log`.
- Captures téléphone regardées en deux passes : cours (4 écrans), fiche, exercices 2747, 2752, 2749, 2751, 2753, 2754. Corrigé après la 1re passe : figures trop petites sur téléphone (voir ci-dessus) ; division par 0,5 remplacée par « 1 unité = 2 intervalles » (niveau 5e).

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 263`, lancer `retirer_exercices.py` (11 Id).
- Le repère du plan est traité ici comme demandé ; la notion 272 (« Repérage et grandeurs en fonction d'une autre ») pourra le reprendre sans doublon d'exemples.

---

## Historique : révision du 30 octobre 2026

État : prêt, révision pédagogique contrôlée le 30 octobre 2026.

Sauvegarde intégrale des contenus et figures antérieurs : `sauvegardes/revision_2026-10-30/`. Les anciens aperçus et preuves restent conservés.

21 identifiants et 21 blocs conservés ; aucun ajout. Six variantes remplacées par des exercices de démarches différentes :
- Id 2751 : Comparer des températures décimales.
- Id 2752 : Lire une graduation au quart.
- Id 2758 : Encadrer et intercaler un décimal.
- Id 2759 : Comparer les positions et les distances.
- Id 2765 : Retrouver un nombre sous contraintes.
- Id 2766 : Distinguer trois critères de classement.

Les cinq anciens problèmes restants, qui ne changeaient que les valeurs, sont reclassés en entraînement. Répartition : 7 découvertes, 12 entraînements, 2 problèmes. Titres uniques et préfixes cohérents. Couverture détaillée dans `COUVERTURE.md`.

Rédaction : méthodes courtes, étapes aux titres précis, étapes distinctes pour les raisonnements composés, calculs alignés, conclusions courtes et note pédagogique par exercice. Les fiches restent synthétiques. Le cours précise comment lire une graduation fine.

Figures : 18 actives, dont 16 réutilisées et 2 nouvelles ; 6 anciens appels devenus inutiles retirés sans effacer leurs fichiers.

Mathématiques : 176 contrôles du contenu conservé et 179 contrôles de révision, zéro échec.

Rendu : vérificateur courant avec navigateur ; audit de 65 vues à 390 px et à 1 280 px. Journaux : `validation_revision.log`, `captures_revision.log`, `resultats_controles.json`.

Aucun import, aucune écriture en base, aucune modification des sources en ligne.
