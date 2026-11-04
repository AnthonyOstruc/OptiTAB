# Notion 266 — Additionner et soustraire des fractions (5e)

## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-10-exercices-266). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés, 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde des fichiers finaux précédents (import du 30/10) : `sauvegardes/avant_refonte_20261104/`.

Programme de 5e respecté : additions et soustractions de fractions de même dénominateur ou dont un dénominateur est multiple de l'autre, simplification, problèmes de partage (fraction d'un tout, part restante). Aucune multiplication ni division de fractions, aucun dénominateur quelconque (4e). Aucune mention du brevet. Le contrôle automatique vérifie les 166 sommes et différences écrites dans les trois fichiers : dénominateurs toujours égaux ou multiples.

### Erreurs de programme corrigées
L'ancienne version en ligne était hors programme de 5e à plusieurs endroits :
- cours : $\frac34 + \frac56$ ;
- fiche : $\frac34 - \frac16$ ;
- 2814 : $\frac12 + \frac13$ ;
- 2817 : dénominateurs quelconques ;
- 2819 et 2824 : dénominateurs 4 et 6, 8 et 12, 8 et 5.

Ces calculs sont tous remplacés.

### Cours et fiche
- **Cours 261 réécrit façon manuel** (titre inchangé) : objectifs, prérequis et 4 parties.
  - I. Même dénominateur : figure, propriété, exemples, nombre entier, erreur « additionner les dénominateurs ».
  - II. Dénominateur multiple de l'autre : figure 2/3 + 1/6, méthode en 4 étapes, 2 exemples, erreur « ne changer que le dénominateur ».
  - III. Simplifier et contrôler : méthode, écriture entier + fraction, contrôles de vraisemblance.
  - IV. Problèmes de partage : fraction d'un tout et part restante (gâteau, disque), méthode du schéma en barres (terrain de 300 m²), « le même tout », encadré « À retenir ».
- **Fiche 181 refaite** : 5 parties denses, 2 figures, 5 erreurs classiques.
- Les exemples du cours sont tous différents de ceux des exercices.

### Exercices gardés (10), tous réécrits entièrement
| Id | Titre | Capacités |
|---|---|---|
| 2812 | Découverte - Additionner des parts de même taille | barre en neuvièmes, 4 calculs à simplifier, $1 - \frac{3}{10}$, erreur de Lina |
| 2814 | Découverte - Quand un dénominateur est multiple de l'autre | barres A/B : $\frac14 = \frac28$, $\frac14 + \frac38$, 4 calculs (dont $2 - \frac34$) |
| 2810 | Découverte - Le réservoir du jardin | fraction d'un tout ($\frac14 + \frac{5}{12} = \frac23$), part restante, litres, vérification |
| 2817 | Entraînement - Calculer et simplifier | 10 calculs (même dénominateur, multiples, 3 fractions, entiers), résultats > 1 en entier + fraction |
| 2818 | Entraînement - Compléter et enchaîner les calculs | termes manquants, calculs en chaîne $A$ et $B$, pyramide de fractions |
| 2819 | Entraînement - Relire une copie et corriger | 5 copies (dénominateurs additionnés ou soustraits, numérateur oublié, comparaison à 1, un calcul juste) |
| 2830 | Problème - La bouteille de jus | $\frac32$ L : volume servi, reste, nombre de verres de $\frac14$ L, conversion en cL |
| 2824 | Problème - Trois jours de lecture | comparer, fraction lue, pages, 40 pages = $\frac16$, reste $\frac{1}{12}$ = 20 pages |
| 2815 | Problème - Les activités du club | diagramme circulaire en huitièmes, part restante, effectifs, différence $\frac12 - \frac14$ |
| 2811 | Synthèse - La randonnée de la classe | Partie A (parcours de 18 km en neuvièmes) et Partie B (gourde, dixièmes, cL) |

- Progression : 3 Découverte, 3 Entraînement, 3 Problème, 1 Synthèse.
- Chaque corrigé contient la méthode, les étapes détaillées, le résultat encadré, et une erreur fréquente ou un « À retenir ». `Solution:` est courte.
- Questions, corrigés et solutions sont en nombre égal (contrôle automatique).

### Exercices retirés (11)
- 2813, 2816, 2820, 2821, 2823, 2825, 2827, 2828 : « Le réservoir du jardin / L'eau des serres ». C'était le même énoncé à six questions avec d'autres valeurs (doublons). La capacité est reprise par 2810.
- 2822, 2826, 2829 : « Une fraction du reste » (bibliothèque), le même énoncé avec d'autres nombres. La fraction du reste est déjà travaillée en 265 (Id 2807) : pas de doublon.

### Figures (20 neuves, style des livres, `figures/figures.py`)
- Les 2 anciennes figures (`cours_modele`, `lecture_bilan`) sont refaites : celle du cours montrait $\frac34$ et $\frac56$ (hors programme). Elles sont supprimées du dossier (copie dans la sauvegarde). Aucune image en ligne n'est conservée.
- **Cours (4)** : barre 3/8 + 2/8, barres 2/3 + 1/6, gâteau (disque en sixièmes), schéma en barres du terrain. **Fiche (2)** : reprises du cours.
- **Exercices (8 × 2)** : énoncé avec les données seules, corrigé avec les parts additionnées en vert et la part restante en blanc.
  - Barres : 2812, 2814.
  - Schémas en barres de problème : 2810, 2830, 2824, 2811.
  - Disque : 2815 (diagramme circulaire).
  - Pyramide : 2818.
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance.
- Après la 1re passe de captures, toutes les figures ont été ramenées entre 480 et 750 px de large (pas de réduction sur téléphone). Les étiquettes longues sont passées sur trois lignes (nom, fraction, quantité).

### Contrôles
- `verif_266.py` : **580 contrôles**, tous justes (journal `266_mathematiques.log`) :
  - chaque calcul refait en fractions exactes `sympy.Rational` ;
  - lecture automatique de 232 égalités des trois fichiers, les erreurs d'élèves citées volontairement étant listées à part ;
  - dénominateurs égaux ou multiples dans 166 sommes et différences ;
  - données des figures ;
  - titres, progression, absence de « brevet », structure de chaque corrigé ;
  - correspondance des images ;
  - 10 + 11 = 21 Id en ligne.
- Test du contrôleur : une erreur injectée dans une copie temporaire est bien détectée.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (journal `266_validation.log`). Notes : 10 titres changés, 11 retraits volontaires, 22 figures placées, 0 image en ligne conservée.
- `controle_apercu.mjs` avec captures : « Aucun problème détecté », sur téléphone et sur ordinateur (`captures.log`).
- Captures téléphone regardées en deux passes groupées : cours (4 écrans), fiche, exercices 2812 (énoncé et étapes), 2830 et 2811 (étapes). Les anciennes captures du 28/10 ont été retirées du dossier `captures/`.

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 266`, lancer `retirer_exercices.py` (11 Id).
- Le dossier de la notion contient aussi des fichiers de coordination de l'ancien lot 5e (BILAN_5E.md, publier_5e.py…). Ils n'ont pas été touchés.

---

## Historique : révision du 30 octobre 2026

Le rapport complet de la révision du 30/10 est sauvegardé dans `sauvegardes/avant_refonte_20261104/RAPPORT.md`. Cette révision gardait 21 exercices (7 découvertes, 12 entraînements, 2 problèmes), dont plusieurs avec des dénominateurs quelconques.
