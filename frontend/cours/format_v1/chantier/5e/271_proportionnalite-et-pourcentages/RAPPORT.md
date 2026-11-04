# Notion 271 (5e) — Proportionnalité et pourcentages

## Refonte 10 exercices 2026-11-04

**État : prêt.** Cours, fiche, 10 exercices et 20 figures refaits de zéro au niveau des notions de 3e/4e. Aucune écriture en base, aucun git.

### Programme
Programme de mathématiques de 5e, rentrée 2026 (BO du 5 mars 2026), partie « Proportionnalité, fonctions » :
- reconnaître une situation de proportionnalité (tableau : quotients égaux ; contre-exemples à montant fixe) ;
- quatrième proportionnelle par passage à l'unité, coefficient, propriétés de linéarité (multiplicative et additive) — **pas de produit en croix** (4e) ;
- proportion (fraction, décimal, pourcentage), comparer deux proportions, appliquer un pourcentage (part, remise, augmentation) ;
- échelles d'un plan et d'une carte (dans les deux sens, trouver l'échelle) ;
- représentation graphique seulement en découverte (points alignés avec l'origine : cours et exercice 2920).
- **Ratio : non traité.** Le nouveau programme de cycle 4 (BO du 5 mars 2026) supprime la notion de ratio (« disparition de la notion de ratio », présentation académique des programmes de 5e). Le vérificateur interdit le mot « ratio » dans les trois fichiers.
- Aucune mention du brevet.

### Cours (Id 266) et fiche (Id 186)
- Cours façon manuel : objectifs ; I. Reconnaître (définition, méthode des quotients, exemple, erreur fréquente taxi/âge, représentation graphique) ; II. Quatrième proportionnelle (unité, coefficient, linéarité, allure régulière, erreur « +3 sur les deux lignes ») ; III. Proportions et pourcentages (définitions, exprimer / comparer des proportions, appliquer un pourcentage, calcul mental, remise et augmentation, erreurs) ; IV. Échelles (définition, plan ↔ réalité, trouver l'échelle, erreur de conversion) ; à retenir. Exemples tous différents des exercices.
- Fiche dense : 4 parties, tableau des 4 procédures, deux formules encadrées, 2 figures, « 5 erreurs classiques ».
- Unités liées à leur nombre par une espace insécable (le moteur les garde sur la même ligne : plus de « € » seul en début de ligne sur téléphone).

### Les 10 exercices gardés (3 Découverte, 3 Entraînement, 2 Problème, 2 Synthèse)
| Id | Titre | Contenu |
|---|---|---|
| 2920 | Découverte - Reconnaître une situation de proportionnalité | 3 tableaux (clémentines, livraison à forfait, taille/âge), coefficient, 4e proportionnelle, forfait 2 € + 3 €/kg, points alignés avec l'origine |
| 2921 | Découverte - Adapter une recette de crêpes | passage à l'unité (62,5 g), ×2, addition de colonnes (12 = 8 + 4), coefficient, 1 kg → 16 personnes |
| 2917 | Découverte - Calculer et appliquer un pourcentage | 14 sur 40 = 7/20 = 35 %, complément 65 %, 30 % et 25 % de 40 |
| 2915 | Entraînement - Compléter un tableau de proportionnalité | gazole : ×2, ÷2, 20 + 5, prix d'un litre (coefficient 1,8), 42 L, 54 € → 30 L, erreur de Tom |
| 2927 | Entraînement - Remises et augmentations | 10/5/50/25/75 % de 80 €, soldes −30 %, hausse +12 %, puis baisse de 12 % ≠ retour au prix (49,28 €) |
| 2924 | Entraînement - Le plan d'une chambre | échelle 1/50 : chambre 4 m × 3 m, lit 2 m × 90 cm, bureau 2,4 cm, trouver l'échelle 1/80 |
| 2934 | Problème - Choisir le meilleur lot | prix unitaires, 30 cahiers, remise de 10 %, achat avec 20 € par lots entiers |
| 2918 | Problème - Préparer une randonnée | carte 1/25 000 : 1 cm = 250 m, boucle de 4 km, allure régulière 3 km/h → 1 h 20 min, retour à 11 h 35, 2 km → 8 cm |
| 2935 | Synthèse - Le goûter de fin d'année | recette 600 g pour 8 → 20 élèves, sachets entiers, 25 % payés par le foyer, 80 % des élèves |
| 2931 | Synthèse - L'enquête sur le petit déjeuner | proportions 75 % / 70 %, comparaison, non-proportionnalité, 72 % de 150, remise de 20 % |

Chaque corrigé : une méthode et un résultat encadré par question, étapes détaillées, erreur fréquente ; `Solution:` courte et complète. Les Id 2915 et 2918 (anciennes copies de la recette) et 2931 (ancien graphique des pommes, au-delà de la découverte) sont réutilisés pour des exercices refaits de zéro.

### Exercices retirés (11) — `exercices_retires.txt`
2916, 2919, 2922, 2923, 2925, 2926, 2928, 2929, 2930, 2932, 2933 : toutes des copies de « Recette : g de farine pour n personnes » (mêmes six questions, seules les valeurs changeaient). La recette reste traitée par 2921 et 2935.

### Figures (20 neuves, style livre, `figures/figures.py`)
- L'ancienne figure en ligne (`r30_pommes_corrige`, cours et 2931) est retirée (copie dans `sauvegardes/avant_refonte_20261104/figures/`) ; aucune image en ligne conservée.
- Cours (5) : tableau du tissu avec flèche ×6 ; graphiques tissu / taxi (droite par l'origine ou non) ; tableau des baguettes avec flèches ÷5, ×8 et ×0,9 ; barre de pourcentage (30 % de 60 €) ; plan du terrain de handball à 1/1 000 avec échelle graphique. Fiche : 2 de ces figures.
- Exercices (15) : 2920 repère énoncé / corrigé (droites en vert et orange) ; 2921 fiche recette + tableau à flèches (réponses en vert) ; 2917 et 2927 barres de pourcentage ; 2915 et 2935 tableaux à flèches ; 2924 plan de la chambre énoncé / corrigé ; 2934 étiquettes des lots + barres comparatives ; 2918 carte énoncé / corrigé ; 2931 barres des proportions.
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance ; toutes ≤ 746 px (lisibles sur téléphone).

### Contrôles
- `verif_271.py` : **297 contrôles** sympy exacts — chaque réponse du cours, de la fiche, des exercices et des valeurs écrites sur les figures ; **169 égalités numériques** des textes recalculées automatiquement (fractions, pourcentages et conversions d'unités compris ; détection d'une erreur volontaire testée) ; structure (10 exercices, progression, une méthode et un résultat par question, erreur fréquente, solution complète, Id 2915 à 2935 tous gardés ou retirés) ; absence de « brevet », « ratio », « produit en croix ». 0 erreur.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`271_validation.log`). `controle_apercu.mjs` : **64 vues sur 64** sans problème, téléphone et ordinateur (`271_captures.log`, `captures_refonte/`).
- Captures téléphone regardées en deux passes groupées (`captures_refonte/planches/`) : cours entier, fiche, les 10 exercices (énoncés 2920 et 2921, toutes les étapes). Corrigé après la 1re passe : quotients de 2920 sur deux lignes (formule trop large), durées de 2918 reformulées, unités liées par espaces insécables, étiquettes de la figure 2931 agrandies.

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 271`, lancer `retirer_exercices.py` (11 Id).
- Incident sans conséquence : la copie de sauvegarde des trois fichiers texte d'avant-refonte a été écrasée par erreur pendant le travail ; elle a été rétablie à partir de `source_en_ligne/` (état en ligne, identique au contenu du 30/10) — voir `sauvegardes/avant_refonte_20261104/LISEZMOI.txt`.

---

## Historique : révision du 30 octobre 2026

État : prêt — révision pédagogique contrôlée le 30 octobre 2026.

21 blocs et leurs identifiants conservés, 105 questions corrigées. 7 exercices remplacés pour diversifier les méthodes ; 0 doublons exacts supplémentaires corrigés. Les titres et les difficultés correspondent aux démarches : 16 découvertes, 3 entraînements, 2 problèmes. Couverture et Id détaillés dans COUVERTURE.md.

Format : même moteur et même syntaxe optitab:1 que la Terminale. Objectifs, sections romaines, propriétés, méthodes courtes, exemples, points d’attention et récapitulation ; fiche synthétique et corrigés question par question. Les constructions ou lectures de graphiques disposent de figures de correction. Les variantes numériques conservées ne sont plus artificiellement classées comme problèmes.

Modifications :

| Id conservé | Travail proposé | Niveau |
|---|---|---|
| 2917 | Pourcentage d’un effectif | easy |
| 2920 | Un tableau trompeur | easy |
| 2924 | Lire une échelle de randonnée | medium |
| 2927 | Augmenter puis réduire un prix | medium |
| 2931 | Représenter le prix des pommes | medium |
| 2934 | Choisir le meilleur lot | hard |
| 2935 | Une recette et un budget à respecter | hard |

Mathématiques : 242 assertions de l’audit exact OK sur les fichiers finaux ; Id, calculs, conversions et contraintes contrôlés selon la notion. Les propriétés et les arguments qualitatifs ont été relus avec les énoncés et les figures. Preuves : revision_maths_coordination.log, controle_maths_coordination.json, resultat_verification.json ; moteur conservé dans verif_notion.py.

Figures : 1 PNG actifs, sources TikZ et productions précédentes conservées. Compilation et contrôle texte/traits : OK. Preuve : compilation_figures.json.

Rendu final : 65 vues mobiles à 390 px et les mêmes 65 vues à 1 280 px, zéro anomalie restante. Journaux : revision_validation.log et revision_navigateur.log.

Sauvegarde antérieure dans sauvegardes/revision_2026-10-30/. Aucun accès ou import en base.
