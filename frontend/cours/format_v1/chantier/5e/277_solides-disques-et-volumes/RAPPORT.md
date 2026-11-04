## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-5e-277). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés, 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde de l'état de départ : `sauvegardes/avant_refonte_20261104/` (textes, figures.py, correspondance, 11 anciennes images).

### Programme (annexe 2 et exemples Éduscol, cycle 4, rentrée 2026, rubrique « Représentation de l'espace » de 5e)
Vérifié dans `livre/archives/programmes-officiels/cinquieme-audit/` : reconnaître pavé, cube, prisme droit, cylindre ; perspective cavalière (arêtes cachées, arêtes de même longueur, faces parallèles) ; vues et dénombrement d'empilements de cubes ; patron du cube, du pavé, du prisme droit (reporter les longueurs) et du cylindre ; volume du cube, du pavé, du prisme droit et du cylindre (aire de la base × hauteur, pavé = prisme particulier) ; unités de volume et de contenance (1 L = 1 dm³). Pyramides et cônes (4e) : une seule mention, en remarque du cours. L'aire du disque (notion 276) sert seulement au volume du cylindre. Pas de Pythagore, aucune mention du brevet (contrôlé par `verif_277.py`).

### Cours et fiche
- **Cours 272 réécrit façon manuel** : I. reconnaître les solides (définitions, hauteur, propriété n + 2 faces / 3n arêtes / 2n sommets, prisme couché) ; II. perspective cavalière (règles, dessin à main levée) et empilements (vues, dénombrement) ; III. patrons (cube, pavé, prisme droit avec périmètre de la base, cylindre 2 × π × r) ; IV. volumes (cm³ par dénombrement, pavé, V = 𝓑 × h, cylindre, deux exemples, deux hauteurs à ne pas confondre) ; V. unités de volume et de contenance (tableau, exemples, erreurs) ; « À retenir ». Exemples tous différents des exercices.
- **Fiche 192 refaite** : tableau des solides, représentations, patrons, tableau des volumes avec figure, unités, 5 erreurs classiques, réflexe.

### Exercices gardés (10), tous réécrits
| Id | Titre | Capacités |
|---|---|---|
| 3050 | Découverte - Reconnaître des solides en perspective cavalière | nommer 5 solides, prismes (pavé particulier), prisme couché, bases et faces latérales, faces / arêtes / sommets, arêtes cachées, arêtes égales, faces parallèles |
| 3054 | Découverte - Compter les cubes d'un empilement | piles, 11 cubes = 11 cm³, vues de face et de droite, cube caché, pavé de cubes 5 × 2 × 3 → formule |
| 3047 | Découverte - Reconnaître des patrons de cube et de pavé | 4 assemblages (2 patrons), faces opposées, patron d'un pavé (a, b, c) |
| 3045 | Entraînement - Convertir des volumes et des contenances | m³/dm³/cm³/mm³, L/cL/mL, volume ↔ contenance, brique de jus 1 080 cm³, ranger |
| 3055 | Entraînement - Calculer le volume de prismes droits | pavé (2 méthodes), prisme debout 90 cm³, prisme couché 120 cm³ (piège des hauteurs), hauteur inconnue |
| 3051 | Entraînement - Calculer le volume d'un cylindre | rayon, diamètre, unités, valeur exacte et arrondie, contenance, affirmation à réfuter |
| 3061 | Problème - Fabriquer une boîte en forme de prisme | patron à compléter, 360 mL, longueur pour 0,6 L, aire du carton 648 cm² |
| 3052 | Problème - L'étiquette d'une boîte de conserve | patron du cylindre, étiquette 10π ≈ 31,4 cm, 275π ≈ 864 cm³ contre 850 mL |
| 3059 | Synthèse - L'aquarium et son décor | pavé, litres, hauteur d'eau, cylindre immergé, montée de l'eau, eau encore possible |
| 3041 | Synthèse - Choisir un emballage | prisme couché et cylindre : éléments, patrons, volumes 300 / 93,75π cm³, contenance |

Progression 3 Découverte / 3 Entraînement / 2 Problème / 2 Synthèse. Chaque corrigé : méthode, étapes détaillées, résultat encadré, erreur fréquente ; `Solution:` courte.

### Exercices retirés (11)
3042, 3044, 3046, 3049, 3053, 3056, 3058, 3060 (copies de « La boîte cylindrique »), 3043, 3057 (copies de « Une boîte en prisme triangulaire »), 3048 (copie de « Un aquarium en pavé droit ») : mêmes questions, seules les dimensions changeaient ; capacités reprises par les exercices gardés.

### Figures (38 neuves pour 39 emplacements, style des livres, `figures/figures.py`)
- Perspective cavalière reprise de la 289 (40°, 0,6) : faces visibles calculées, arêtes cachées en pointillés. L'aquarium transparent a ses arêtes visibles tracées devant le décor. Empilements dessinés du fond vers l'avant. Prismes couchés : la face avant est redessinée à part avec sa hauteur (lisibilité).
- Cours (9), fiche (1, la figure des volumes du cours), exercices (29) : énoncé avec les données en orange, corrigé avec base et hauteur en vert. Aucune image en ligne conservée ; les 11 anciennes, non appelées, seront supprimées à l'import.
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance. Figures larges resserrées après la 1re passe téléphone (≤ 860 px).

### Contrôles
- `verif_277.py` : **188 contrôles**, tous justes (sympy : chaque volume, aire, conversion, arrondi ; géométrie des figures : arêtes cachées calculées, pliage des 4 patrons de cube, vues de l'empilement, triangles 6-8-10 et 6-5-5 ; structure : 10 + 11 = 21 Id, questions énoncé = corrigé = solution, images appelées = déclarées, aucune image orpheline).
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`277_validation.log`).
- `controle_apercu.mjs` : « Aucun problème détecté », téléphone et ordinateur (`277_captures.log`, captures dans `captures_refonte/`).
- Captures téléphone regardées en deux passes : cours entier, fiche, exercices 3050, 3054, 3055, 3061, 3059, 3041, 3045. Corrigé après la 1re passe : unités isolées en début de ligne (espaces insécables), 9 figures trop larges réorganisées (annotations au-dessus ou dessous, solide au-dessus du patron, cylindre sur une 2e ligne).

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 277`, lancer `retirer_exercices.py` (11 Id).

---

## Historique : révision du 30 octobre 2026

État : prêt — révision pédagogique contrôlée le 30 octobre 2026.

21 blocs et leurs identifiants conservés, 114 questions corrigées. 6 exercices remplacés pour diversifier les méthodes ; 0 doublons exacts supplémentaires corrigés. Les titres et les difficultés correspondent aux démarches : 17 découvertes, 2 entraînements, 2 problèmes. Couverture et Id détaillés dans COUVERTURE.md.

Format : même moteur et même syntaxe optitab:1 que la Terminale. Objectifs, sections romaines, propriétés, méthodes courtes, exemples, points d’attention et récapitulation ; fiche synthétique et corrigés question par question. Les constructions ou lectures de graphiques disposent de figures de correction. Les variantes numériques conservées ne sont plus artificiellement classées comme problèmes.

Modifications :

| Id conservé | Travail proposé | Niveau |
|---|---|---|
| 3045 | Relier volumes et capacités | easy |
| 3047 | Reconnaître un patron de cube | easy |
| 3052 | Du patron à la surface d’un cylindre | medium |
| 3054 | Dénombrer un empilement de cubes | medium |
| 3059 | Remplir un aquarium sans déborder | hard |
| 3061 | Adapter une boîte à un produit | hard |

Mathématiques : 386 assertions de l’audit exact OK sur les fichiers finaux ; Id, calculs, conversions et contraintes contrôlés selon la notion. Les propriétés et les arguments qualitatifs ont été relus avec les énoncés et les figures. Preuves : revision_maths_coordination.log, controle_maths_coordination.json, verification_maths.json ; moteur conservé dans la notion 276/verif_notion.py (et correction reportée dans 279/verif_notion.py).

Figures : 8 PNG actifs, sources TikZ et productions précédentes conservées. Toutes les figures actives ont été regardées sur les planches ou individuellement. Compilation et contrôle texte/traits : OK, aucune tolérance ajoutée. Les graduations d’axes emploient le fond blanc autorisé par le guide ; leur ordre de dessin a été corrigé pour éviter que les courbes ou les côtés traversent les chiffres. Les lettres des points restent hors des traits. Preuve : compilation_figures.json.

Rendu final : vérificateur courant et audit renforcé des erreurs MathJax HTML/SVG ; 65 vues mobiles à 390 px et les mêmes 65 vues à 1 280 px, zéro anomalie restante. Absence de caractères de contrôle C0 interdits vérifiée. Journaux : revision_validation.log et revision_navigateur.log ; statut : controles_revision_20261030.json. Les tableaux trop larges des cours ont été compactés quand nécessaire.

Relecture : cours mobile intégral, fiche et exercices 5, 12, 19, 21, énoncés et étapes, regardés dans les captures finales. Preuves : captures_revision_20261030/relecture_documents.png et relecture_revision_1.png, relecture_revision_2.png ; relecture_visuelle_coordination.json.

Outil : copie locale des audits communs, détection MathJax élargie et attente de fermeture Chrome bornée à deux secondes pour le défaut de nettoyage Windows déjà établi. Les audits ne sont pas allégés. Aucun outil commun ou fichier frontend/src modifié.

Sauvegarde antérieure dans sauvegardes/revision_2026-10-30/. Sources exportées conservées, aucun accès ou import en base. Travail limité à la classe de 5e ; programme rentrée 2026 vérifié par la coordination.
