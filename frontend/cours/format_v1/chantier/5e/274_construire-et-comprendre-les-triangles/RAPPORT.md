# Notion 274 (5e) : Construire et comprendre les triangles

## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-5e-274). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés, 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde de l'état de départ : `sauvegardes/avant_refonte_20261104/` (textes, RAPPORT, figures.py, correspondance, anciennes images et planches).

### Programme (BO n° 10 du 5 mars 2026, « Triangles » de 5e)
Vérifié dans `livre/archives/programmes-officiels/cinquieme-audit/` (annexe 2 et exemples Éduscol) : somme des angles (la connaître, la démontrer, calculer le 3e angle) ; triangles isocèle, équilatéral, rectangle reconnus sur un schéma codé ; construire des triangles à partir de données partielles (dont « calculer d'abord l'angle manquant », exemple AUG d'Éduscol) ; médiatrices et cercle circonscrit dans les triangles particuliers (triangle rectangle inscrit dans un demi-cercle : observé, admis, démontré en 4e) ; aire du triangle et hauteurs, hauteurs concourantes (orthocentre, constat) ; médianes, concourantes (centre de gravité, constat), et **démonstration** qu'une médiane partage le triangle en deux aires égales ; raisonner avec l'aire. L'inégalité triangulaire (6e) est reprise pour savoir si une construction est possible. Aucune mention du brevet. Pas de doublon avec la 273 : les alternes-internes ne servent qu'à la démonstration de la somme des angles dans le cours, aucun exercice ne porte dessus.

### Cours et fiche
- **Cours 269 réécrit façon manuel** (titre inchangé) : objectifs ; I. inégalité triangulaire (propriété, cas aplati, méthode « tester la plus grande », exemples, erreur fréquente) ; II. somme des angles avec sa démonstration, méthode, triangles particuliers (tableau, sommet principal et base, réciproques, démonstration des 60° de l'équilatéral, exemples isocèles, erreurs) ; III. les trois constructions (LMN, RST, IJK) + « quand un angle adjacent manque » (XYZ), « à retenir », piège de l'angle compris ; IV. médiatrice (définition, équidistance et réciproque, tracé au compas), cercle circonscrit, cas isocèle / équilatéral / rectangle ; V. hauteurs (définition, orthocentre, hauteur extérieure), aire démontrée comme moitié du rectangle, même base et même hauteur, calcul d'une hauteur à partir de l'aire ; VI. médianes, démonstration du partage de l'aire, centre de gravité, médiane ≠ hauteur ; tableau final des droites remarquables. Exemples tous différents des exercices.
- **Fiche 189 refaite** : existence et angles, triangles particuliers, tableau des constructions, tableau des droites remarquables, aires, 6 erreurs classiques ; 2 figures.

### Exercices gardés (10)
| Id | Titre | Capacités |
|---|---|---|
| 2980 | Découverte - Trois longueurs : triangle possible ou non ? | inégalité (possible, impossible, aplati, équilatéral), construction au compas, deux points C et C', 3e côté possible |
| 2984 | Découverte - Somme des angles et triangles particuliers | 3e angle ; rectangle ; isocèle (sommet connu, base connue) ; démonstration des 60° ; triangles impossibles |
| 2981 | Découverte - Construire avec deux côtés et l'angle compris | angle compris, programme de construction, mesures, isocèle AB = 4 cm et 30° (exemple Éduscol), erreur de sommet |
| 2978 | Entraînement - Calculer un angle avant de construire | un côté et deux angles : AUG (angle en U à calculer), EFG isocèle (angles à la base), 100° + 85° impossible |
| 2991 | Entraînement - Tracer des hauteurs et calculer une aire | tracer une hauteur, aire, hauteur calculée par l'aire (BK = 5,6 cm), orthocentre, hauteur extérieure (triangle obtus) |
| 2987 | Entraînement - Médiatrices et cercle circonscrit | médiatrices au compas, OA = OB = OC, 3e médiatrice, triangle rectangle (centre = milieu de l'hypoténuse), isocèle |
| 2982 | Problème - Partager un champ en parts de même aire | partage par la hauteur (inégal), par la médiane (démonstration), médiane ≠ hauteur, trois parts, centre de gravité |
| 2994 | Problème - Le gazon du jardin rectangulaire | hauteur dans un rectangle, même base et même hauteur, moitié du rectangle, longueur retrouvée par l'aire |
| 2998 | Problème - Un angle extérieur dans un triangle isocèle | angles supplémentaires, isocèle, somme, angle extérieur, cas équilatéral (120°) et rectangle isocèle (135°) |
| 2996 | Synthèse - Construire et étudier un triangle rectangle | construction, mesures et angles complémentaires, cercle circonscrit, aire, hauteur par l'aire, médiane et aires |

Progression 3 Découverte / 3 Entraînement / 3 Problème / 1 Synthèse. Tous les exercices sont réécrits de zéro (contenus de 5e, niveau manuel ; 6 questions, 5 pour 2980) ; titres changés pour 2984, 2978, 2991, 2987, 2982, 2994, 2996 (l'ancien sujet est repris ou mieux couvert ailleurs). Chaque corrigé : méthode, étapes détaillées, résultat encadré par question, erreur fréquente ou « À retenir ». `Solution:` courte. Espaces insécables entre nombres et unités (247).

### Exercices retirés (11)
- 2989, 2979, 2986, 2993 : copies de « Base … m, hauteur … m : médiane et aires » (mêmes six questions, seules les dimensions changeaient) ; repris par 2982, 2994 et 2996.
- 2983, 2985, 2988, 2990, 2992, 2995, 2997 : copies de « Construire : côté … cm et angles … » ; repris par 2978 (avec l'angle à calculer d'abord, et le cas isocèle).

### Figures (46 neuves, style des livres, `figures/figures.py`)
- Outils géométriques repris de la 282 (4e) ; toutes les constructions calculées en vraie grandeur puis réduites ; coordonnées réelles dans `DONNEES`, contrôlées par `verif_274.py`.
- Cours (13) : inégalité (arcs qui se coupent, se touchent, ne se rencontrent pas), démonstration de la somme, triangles particuliers, trois constructions, médiatrice au compas, cercle circonscrit, cas du triangle rectangle, hauteurs (aigu et obtus), aire = moitié du rectangle, médiane et aires, centre de gravité. Fiche : 2 figures du cours.
- Énoncés : **figures à main levée** (trait irrégulier) portant seulement les données (2980, 2981, 2978 ×2, 2987 ×2, 2996), ou schémas codés sans la réponse (2984, 2991, 2982, 2994, 2998).
- Corrigés : **construction complète en vert, arcs de compas visibles** (2980 avec C et C', 2981, 2978, 2987 avec médiatrices au compas, 2996 avec report au compas, perpendiculaire et médiatrice) ; réponses en vert (angles, hauteurs, longueurs, aires).
- Les 24 anciennes images en ligne (3 du cours, 21 des exercices) ne sont plus appelées (supprimées à l'import) : aucune conservée.
- `figures_livre.py` : 46/46, 0 texte sur un trait, aucune tolérance ; avertissements restants = cotes à fond blanc (usage normal) ; toutes ≤ 900 px. Chaque PNG regardé ; corrigé après relecture : étiquettes posées sur des arcs ou des médiatrices (2987, 2996, 2991, 2982), arcs de médiatrice tombant dans le triangle (2987, 2996 : rayons agrandis pour que les points de construction soient hors du triangle), figures agrandies (2991, 2987, 2981).

### Contrôles
- `verif_274.py` : **281 contrôles justes, 0 faux** (sympy : chaque calcul du cours et des 10 corrigés, valeurs arrondies annoncées comme mesures — EF ≈ 4,2 cm, 46°, 84°, AG ≈ 4,7 cm, UG ≈ 3,3 cm, EF ≈ 4,4 cm, rayon ≈ 3,6 cm, 53° et 37° — ; coordonnées des figures : longueurs, angles, pieds de hauteurs, orthocentres, centres de cercles, centres de gravité ; structure : questions = étapes = solutions, un résultat par question, images appelées = déclarées, 10 + 11 = 21 Id, progression, aucune mention du brevet).
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`274_validation.log` ; 48 positions de figures neuves, 0 image en ligne conservée ; notes : titres changés et 11 retraits, voulus).
- `controle_apercu.mjs` : « Aucun problème détecté », 64 vues téléphone et ordinateur sans débordement, erreur de formule, $ brut ni image manquante (`274_captures.log`, captures dans `captures_refonte/`).
- Captures téléphone regardées en deux passes : cours (début, II-III, V-VI), fiche, énoncé 2980, corrigés 2991 et 2996. Corrigé après la 1re passe : trois formules « … , donc … » sur une ligne (2991, 2994, 2996) réduites sur téléphone, découpées en deux lignes.

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 274`, lancer `retirer_exercices.py` (11 Id).

---

## Historique : révision du 30 octobre 2026

21 blocs et leurs identifiants conservés, 105 questions corrigées. 7 exercices remplacés pour diversifier les méthodes. Titres et difficultés : 1 découverte, 18 entraînements, 2 problèmes. Audit exact (229 assertions), 22 figures, 65 vues mobiles et 65 vues ordinateur sans anomalie. Sauvegarde dans `sauvegardes/revision_2026-10-30/`. Le détail complet de cette révision est dans `sauvegardes/avant_refonte_20261104/RAPPORT.md`.
