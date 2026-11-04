## Refonte 10 exercices 2026-11-04

**État : prêt.** Cours, fiche, 10 exercices et 32 figures refaits de zéro au niveau des notions de 3e/4e. Aucune écriture en base, aucun git.

### Programme
Programme de 5e, rentrée 2026 (BO n° 10 du 5 mars 2026), rubrique « Parallélogrammes », vérifié dans `livre/archives/programmes-officiels/cinquieme-audit/` (annexe 2 et exemples Éduscol p. 26) :
- définir le parallélogramme (côtés opposés parallèles), le construire, connaître les propriétés caractéristiques des côtés opposés et des diagonales, justifiées par le demi-tour (centre de symétrie) ;
- démontrer qu'un quadrilatère est un parallélogramme (rédaction « On sait que… Or… Donc… ») ;
- rectangle, losange, carré : définitions Éduscol (parallélogramme avec un angle droit / deux côtés consécutifs égaux / les deux), propriétés des diagonales, reconnaissance par le codage ; exemple Éduscol du quadrilatère DOLE repris (3031) ;
- aire du parallélogramme (découpage en rectangle), du triangle, des figures complexes faites de parallélogrammes et de disques ; aire du disque (« preuve sans les mots » Éduscol : parts tête-bêche) ; longueur du cercle ;
- conversions de longueurs et d'aires (dont are et hectare) ; preuve par les aires (Éduscol : parallélogramme de centre O, triangles de même aire — 3022).
- Symétrie centrale utilisée seulement comme outil (notion 275). Aucune mention du brevet ; rien de 4e (Pythagore, racine, translation, produit en croix : contrôlé par `verif_276.py`).

### Cours (Id 271) et fiche (Id 191)
- Cours façon manuel : objectifs ; I. définition, centre de symétrie, propriétés (côtés, diagonales, angles opposés, angles consécutifs supplémentaires justifiés par la somme 360°), exemple, erreur fréquente ; II. propriétés caractéristiques, méthode de rédaction, exemple, erreur du trapèze ; III. trois constructions (parallèles, compas, diagonales), conseil du croquis ; IV. rectangle, losange, carré (définitions, propriétés, reconnaissance par les diagonales, exemple, erreur) ; V. unités d'aire (tableau vertical lisible sur téléphone, are, hectare), aire du parallélogramme, du triangle (pied sur le prolongement), π, cercle et disque, figures composées, « À retenir ». Exemples tous différents des exercices.
- Fiche dense : 3 parties, 2 tableaux, 2 figures, « 5 erreurs classiques ».

### Les 10 exercices (3 Découverte, 3 Entraînement, 2 Problème, 2 Synthèse)
| Id | Titre | Contenu |
|---|---|---|
| 3020 | Découverte - Les propriétés du parallélogramme | côtés parallèles, longueurs, périmètre, diagonale BD = 7 cm, angles 60°/120°, symétriques par le demi-tour de centre O |
| 3026 | Découverte - Construire un parallélogramme | croquis, triangle ABC (5 cm, 70°, 3,5 cm), D au compas + justification, méthode du milieu, longueurs et angle sans mesurer |
| 3024 | Découverte - Les diagonales des parallélogrammes particuliers | 4 figures codées (diagonales seules) : parallélogramme, rectangle, losange, carré ; erreur « même milieu / même longueur » |
| 3031 | Entraînement - Démontrer qu'un quadrilatère est un parallélogramme | 3 rédactions (côtés égaux, contre-exemple du trapèze, côtés parallèles et égaux), DOLE losange non carré |
| 3021 | Entraînement - Aire d'un parallélogramme et hauteurs | aire 24 cm², erreur « côté oblique », hauteur BK = 4,8 cm, pied hors de la base (12 cm²), conversions mm² / dm² |
| 3033 | Entraînement - Aires de triangles et figure composée | triangle 12 cm², triangle obtus 6 cm², parcelle 15 + 6 = 21 m² = 2 100 dm² |
| 3040 | Problème - Daller une terrasse | 24 − 6 = 18 m², dalle 2 500 cm² = 0,25 m², 72 dalles, marge 10 % → 80, 200 € |
| 3038 | Problème - La pelouse du stade | rectangle + 2 demi-disques : tour 180 + 60π ≈ 368,5 m, aire ≈ 8 227,4 m² ≈ 0,8 ha, 21 sacs |
| 3022 | Synthèse - Partager un terrain en parts égales | parallélogramme par les diagonales, 84 m², triangle ABD 42 m², médiane → 21 m², demi-tour → 4 parcelles de 21 m², 42 sachets |
| 3023 | Synthèse - Un massif de fleurs en losange | losange par les diagonales, aire 12 m² par deux triangles, fontaine π m², 12 − π ≈ 8,86 m² ≈ 886 dm², 35 fleurs, bordure 2π ≈ 6,28 m → 13 éléments |

Chaque corrigé : une méthode et un résultat encadré par question, étapes détaillées, erreur fréquente ; `Solution:` courte et complète. Ancien exercice 3038 (deux rectangles de même périmètre, hors sujet du chapitre) refait de zéro ; Id 3020 à 3023 (anciennes copies du terrain) réutilisés pour des exercices refaits.

### Exercices retirés (11) — `exercices_retires.txt`
3025, 3027, 3028, 3029, 3030, 3032, 3034, 3035, 3036, 3037, 3039 : copies de « Un terrain en parallélogramme » (mêmes six questions, seules les valeurs changeaient).

### Figures (32 neuves, style livre, `figures/figures.py`)
- Toutes les anciennes figures retirées (copie dans `sauvegardes/avant_refonte_20261104/figures/`) ; aucune image en ligne conservée (22 seront supprimées à l'import).
- Cours (6) : propriétés de RSTU, construction au compas, rectangle / losange / carré, découpage du parallélogramme en rectangle, triangle moitié d'un parallélogramme et pied sur le prolongement, disque découpé en parts tête-bêche. Fiche : 2 d'entre elles.
- Exercices (26) : énoncé avec les données (hauteurs données en pointillés bleus), corrigé complété en vert (hauteur trouvée BK, hauteur commune issue de A, côtés et angles trouvés, constructions, aires découpées) ; croquis à main levée pour 3026.
- Coordonnées réelles dans `DONNEES`, toutes recalculées par `verif_276.py`. `figures_livre.py` : 0 texte sur un trait, aucune tolérance ; largeurs ≤ 801 px (lisibles sur téléphone).

### Contrôles
- `verif_276.py` : **252 contrôles** — réponses du cours et des 10 exercices en valeurs exactes (π compris), coordonnées des 32 figures (parallélismes, milieux, perpendicularités, longueurs, aires par la formule de Gauss, positions des pieds de hauteur), **93 égalités numériques** des textes recalculées automatiquement (« ≈ » à la précision affichée), structure (10 exercices, progression, Id 3020 à 3040 gardés ou retirés), absence de « brevet » et de notions de 4e. 0 erreur (`276_verif.log`).
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`276_validation.log`). `controle_apercu.mjs` : **64 vues sur 64** sans problème, téléphone et ordinateur (`276_captures.log`, `captures_refonte/`).
- Captures téléphone regardées en deux passes groupées (`captures_refonte/planches/`). Corrigé après la 1re passe : figures des corrigés sorties des encadrés d'étape (trop réduites dedans), figures larges rétrécies, tableau des unités d'aire et tableau des quadrilatères particuliers remplacés par des formes lisibles sur téléphone, formule du cercle coupée en deux lignes ; données de 3021 changées (AB = 6 cm) pour que le pied K soit bien visible.

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 276`, lancer `retirer_exercices.py` (11 Id).

---

## Historique : révision du 30 octobre 2026

État : prêt — révision pédagogique contrôlée le 30 octobre 2026.

21 blocs et leurs identifiants conservés, 114 questions corrigées. 6 exercices remplacés pour diversifier les méthodes ; 0 doublons exacts supplémentaires corrigés. Les titres et les difficultés correspondent aux démarches : 17 découvertes, 2 entraînements, 2 problèmes. Couverture et Id détaillés dans COUVERTURE.md.

Format : même moteur et même syntaxe optitab:1 que la Terminale. Objectifs, sections romaines, propriétés, méthodes courtes, exemples, points d’attention et récapitulation ; fiche synthétique et corrigés question par question. Les constructions ou lectures de graphiques disposent de figures de correction. Les variantes numériques conservées ne sont plus artificiellement classées comme problèmes.

Modifications :

| Id conservé | Travail proposé | Niveau |
|---|---|---|
| 3024 | Diagonales et centre de symétrie | easy |
| 3026 | Construire le quatrième sommet | easy |
| 3031 | Choisir une propriété caractéristique | medium |
| 3033 | Une parcelle composée de deux figures | medium |
| 3038 | Même périmètre, surfaces différentes | hard |
| 3040 | Choisir la quantité de dalles | hard |

Mathématiques : 356 assertions de l’audit exact OK sur les fichiers finaux ; Id, calculs, conversions et contraintes contrôlés selon la notion. Les propriétés et les arguments qualitatifs ont été relus avec les énoncés et les figures. Preuves : revision_maths_coordination.log, controle_maths_coordination.json, verification_maths.json ; moteur conservé dans la notion 276/verif_notion.py (et correction reportée dans 279/verif_notion.py).

Figures : 10 PNG actifs, sources TikZ et productions précédentes conservées. Toutes les figures actives ont été regardées sur les planches ou individuellement. Compilation et contrôle texte/traits : OK, aucune tolérance ajoutée. Les graduations d’axes emploient le fond blanc autorisé par le guide ; leur ordre de dessin a été corrigé pour éviter que les courbes ou les côtés traversent les chiffres. Les lettres des points restent hors des traits. Preuve : compilation_figures.json.

Rendu final : vérificateur courant et audit renforcé des erreurs MathJax HTML/SVG ; 65 vues mobiles à 390 px et les mêmes 65 vues à 1 280 px, zéro anomalie restante. Absence de caractères de contrôle C0 interdits vérifiée. Journaux : revision_validation.log et revision_navigateur.log ; statut : controles_revision_20261030.json. Les tableaux trop larges des cours ont été compactés quand nécessaire.

Relecture : cours mobile intégral, fiche et exercices 5, 12, 19, 21, énoncés et étapes, regardés dans les captures finales. Preuves : captures_revision_20261030/relecture_documents.png et relecture_revision_1.png, relecture_revision_2.png ; relecture_visuelle_coordination.json.

Outil : copie locale des audits communs, détection MathJax élargie et attente de fermeture Chrome bornée à deux secondes pour le défaut de nettoyage Windows déjà établi. Les audits ne sont pas allégés. Aucun outil commun ou fichier frontend/src modifié.

Sauvegarde antérieure dans sauvegardes/revision_2026-10-30/. Sources exportées conservées, aucun accès ou import en base. Travail limité à la classe de 5e ; programme rentrée 2026 vérifié par la coordination.
