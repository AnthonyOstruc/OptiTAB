# Notion 275 (5e) : Symétries et demi-tour

## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-5e-275). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés, 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde de l'état de départ : `sauvegardes/avant_refonte_20261104/` (textes, RAPPORT, COUVERTURE, figures.py, correspondance, 25 anciennes images). Aucune écriture en base, aucun git.

### Programme (BO n° 10 du 5 mars 2026, « Transformations » de 5e)
Vérifié dans `livre/archives/programmes-officiels/cinquieme-audit/` (annexe 2 et exemples Éduscol) : automatismes « symétrique par symétrie axiale sur quadrillage, axe vertical, horizontal ou en diagonale » et « sur feuille blanche » ; objectifs « définir le demi-tour (symétrie centrale) » et « connaître ses propriétés » (conservation de l'alignement, du parallélisme, des longueurs, des angles, admises et utilisées) ; lien avec le parallélogramme ; symétries dans les frises, pavages, rosaces. L'ancienne version travaillait tout en **coordonnées dans un repère** ((x ; y) → (−x ; −y)), ce qui n'est pas la démarche du programme : tout est refait sur quadrillage et sur papier blanc. Les deux symétries successives (ancien 3019) ne sont pas au programme : retirées.

### Cours et fiche
- **Cours 270 réécrit façon manuel** (titre inchangé) : objectifs, prérequis ; I. symétrie axiale (définition par la médiatrice, quadrillage axe vertical, axe en diagonale, papier blanc à l'équerre et au compas seul, avec justification) ; II. demi-tour (définition par le milieu, « demi-tour » sur un demi-cercle, méthode du « même chemin » sur quadrillage, règle et compas, erreurs fréquentes) ; III. propriétés (conservations, image d'une droite = droite parallèle, image d'un cercle, exemple « sans mesurer », remarque sur le parallélogramme) ; IV. axes et centres de symétrie d'une figure (définitions, tableau des figures usuelles, frises/rosaces) ; V. comparer les deux symétries (tableau, méthode pour reconnaître) ; « À retenir ». 9 figures. Exemples différents des exercices.
- **Fiche 190 refaite** : tableau court des deux symétries, méthodes de construction (4 cas), propriétés, tableau axes/centres, 3 erreurs classiques, 2 figures.

### Exercices gardés (10)
| Id | Titre | Capacités |
|---|---|---|
| 3000 | Découverte - Symétrie axiale sur quadrillage | axes vertical, horizontal, en diagonale ; point de l'axe ; angle droit et longueur conservés |
| 2999 | Découverte - Symétrique d'un point par demi-tour | chemin vers O puis même chemin ; symétrique de O ; retrouver H tel que G soit son image ; O milieu |
| 3006 | Découverte - Image d'un drapeau par demi-tour | image d'une figure, « tête en bas », longueur et aire conservées, pas un miroir |
| 3003 | Entraînement - Symétrie axiale sur papier blanc | équerre, compas seul, longueurs et angle, alignement (les droites se coupent sur l'axe) |
| 3001 | Entraînement - Demi-tour sur papier blanc | règle et compas, longueurs et angle, droite parallèle, image d'un cercle |
| 3008 | Entraînement - Symétrie axiale ou demi-tour ? | reconnaître 4 transformations, tracer l'axe, placer le centre, cas « ni l'une ni l'autre » |
| 3005 | Problème - Déduire des mesures grâce au demi-tour | longueurs, angle droit, aire 12 cm², périmètre ≈ 17,2 cm, M' sur [A'B'], parallélisme |
| 3015 | Problème - Axes et centres de symétrie | lettres H N E X T Z, mots « NON » / « TOT », compléter une figure de centre O, aire 17 carreaux, aucun axe |
| 3012 | Synthèse - Comparer les deux symétries | les deux images d'un pentagone, aire 7 carreaux (demi-carreaux), parallélisme seulement pour le demi-tour, points fixes |
| 3019 | Synthèse - Le carreau de la terrasse | carrelage complété par axe puis demi-tour, 2 axes et un centre, 75 cm², fraction 3/16 |

Progression 3 Découverte / 3 Entraînement / 2 Problème / 2 Synthèse. Tous réécrits de zéro (contenu de 5e, niveau manuel, aucune mention du brevet). Chaque corrigé : méthode, étapes détaillées, résultat encadré par question, « Erreur fréquente » (10/10), « À retenir » quand utile ; `Solution:` courte. Unités collées aux nombres par une espace insécable (164 endroits).

### Exercices retirés (11)
3007, 3014, 3002, 3009, 3016, 3004, 3011, 3018 (copies de « Axe vertical : triangle de sommet A(x ; y) ») et 3013, 3010, 3017 (copies de « Demi-tour : triangle de sommet A(x ; y) ») : mêmes six questions, seules les coordonnées changeaient. Capacités reprises par 3000, 2999, 3006 et 3012.

### Figures (35 neuves, style des livres, `figures/figures.py`)
- Machinerie de la 288 (4e) adaptée : quadrillage pâle, départ en bleu marine, image en vert avec traits de construction (perpendiculaires, angles droits, codages des distances égales, arcs de compas, chemins fléchés jusqu'au centre). Énoncés : figure de départ et axe ou centre, **sans l'image** ; corrigés : image en vert.
- Cours 9, fiche 2 (reprises du cours), exercices 26 (énoncé + corrigé pour chacun ; 3 panneaux séparés pour 3000, lisibles sur téléphone).
- Les 25 anciennes images (repères à coordonnées) sont abandonnées ; aucune image en ligne conservée ; les 11 non appelées seront supprimées à l'import.
- `figures_livre.py` : 35/35, 0 texte sur un trait, `TOLERE` vide ; toutes regardées sur les planches puis une à une pour les plus chargées (3001, 3003, 3005, 3000c, 2999).
- `verif_275.py` relit `DONNEES` et recalcule chaque image avec sympy.

### Contrôles
- `verif_275.py` : **401 contrôles, tous justes** (`275_verif.log`) : chaque image recalculée (symétries verticale, horizontale, diagonale, oblique, demi-tours), milieux, perpendicularité, alignements, parallélismes ; chaque nombre du cours et des corrigés (carreaux, chemins, AB = 4 cm, angle 60°, 70°, aire 12, BC ≈ 7,2, périmètre 17,2, aires 3, 7, 8,5, 17, 12 carreaux, 75 cm², 3/16) ; symétries des lettres et des figures par recherche exhaustive (le L sans axe, la figure de 3015 sans axe avec centre, le carreau de 3019 à 2 axes et un centre) ; structure (10 + 11 = 21 Id, titres, progression, questions = parties = solutions, images appelées = déclarées).
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`275_validation.log`) ; `controle_apercu.mjs` : « Aucun problème détecté », téléphone et ordinateur (`275_captures.log`, captures dans `captures_refonte/`).
- Captures téléphone regardées en deux passes groupées (`captures_refonte/275_relecture_*.png`) : cours (5 écrans), fiche (2), exercices 3000 (énoncé et corrigé), 2999, 3003, 3005, 3012. Corrigé après la 1re passe : tableau « Figure / Axes / Centre » du cours trop large (3e colonne coupée) → réduit à des réponses courtes, détails en liste ; 4 figures larges resserrées (cours_comparer, cours_centres, cours_droites, 3005 : largeurs 690 à 790 px) pour que leur texte reste lisible.

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 275`, lancer `retirer_exercices.py` (11 Id).
- **Défaut trouvé dans la 288 (4e, en ligne)** : `\draw[grille] (0,0) grid (12,8)` avec `x=.55cm` trace un quadrillage au pas de **1 cm** (pas par défaut de TikZ), pas au pas de l'unité : les sommets ne tombent pas sur les nœuds du quadrillage (visible sur `chantier/4e/288_*/figures/images/ex3679_corrige.png`, cours_translation, etc.). Correction : ajouter `step=1` au style `grille` puis recompiler et republier la 288. Corrigé ici dès le départ. À vérifier dans les autres notions qui ont copié cette machinerie.

---

## Historique : révision du 30 octobre 2026

(Ancien rapport, conservé dans `sauvegardes/avant_refonte_20261104/RAPPORT_ancien.md`.) 21 blocs conservés, 105 questions corrigées, exercices en repère à coordonnées, 21 figures de repère, 248 assertions d'audit, 65 vues Chrome. Remplacé par la refonte ci-dessus.
