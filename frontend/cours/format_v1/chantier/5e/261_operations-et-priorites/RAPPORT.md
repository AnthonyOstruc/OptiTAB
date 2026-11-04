# Notion 261 (5e) : Opérations et priorités

## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-10-exercices-261, 2026-11-04). 10 exercices gardés (Id inchangés, tous réécrits), 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`. Base de départ : `source_en_ligne/` (ré-export du 04/11), identique sur le fond aux fichiers du 30/10.

### Cours et fiche

- **Titres** inchangés : « Opérations et priorités » et « Résumé : Opérations et priorités ».
- **Cours 256 réécrit façon manuel** (il tenait en 4 parties courtes, sans arbre, sans crochets, sans calculatrice) : objectifs ; I. vocabulaire (définition, tableau natif, nature d'une expression = dernière opération) ; II. priorités (propriété, méthode de rédaction, exemple aligné, piège « de gauche à droite ») ; III. parenthèses et crochets (schéma des priorités, deux exemples alignés) ; IV. arbre de calcul (définition, figure, méthode pour traduire une phrase, exemples dans les deux sens) ; V. calcul mental (regrouper, distributivité avec modèle d'aire, factoriser, piège $13 \times 99$) ; VI. ordre de grandeur, calculatrice et parenthèses (trait de fraction), division par un décimal avec division posée ; VII. problèmes à étapes (méthode, schéma en barres) ; « À retenir ». Exemples tous différents des exercices.
- **Fiche 176 refaite** : 6 parties (vocabulaire en tableau, priorités et crochets, arbre, calcul mental, estimer / calculatrice / division décimale, problèmes), 5 erreurs classiques, réflexe ; 2 figures.

### Exercices gardés (10)

| Id | Titre | Contenu |
|---|---|---|
| 2709 | Découverte - Calculer dans le bon ordre | priorités, gauche à droite, arbre de $E$ à compléter, erreur de Léa |
| 2710 | Découverte - Utiliser des parenthèses et des crochets | parenthèses, crochets, de l'arbre à l'expression, placer des parenthèses |
| 2716 | Découverte - Le vocabulaire des opérations | termes, facteurs, nature d'une expression, phrase ↔ calcul, deux arbres au corrigé |
| 2717 | Entraînement - Calculer mentalement avec des astuces | regrouper, modèle d'aire, distributivité, facteur commun, ×0,5 et ×0,25, erreur d'Inès |
| 2706 | Entraînement - Diviser par un nombre décimal | diviseur rendu entier, division posée, interprétation du quotient (bouteilles) |
| 2714 | Entraînement - Ordres de grandeur et calculatrice | choisir un résultat, estimer un achat, saisies avec parenthèses, virgule mal placée |
| 2705 | Problème - Les fournitures des ateliers | une seule expression avec crochets, ordre de grandeur, erreur, budget |
| 2723 | Problème - Comparer deux tarifs de sortie | forfait + prix par personne, tableau, seuil de 19 personnes, maximum entier |
| 2724 | Type brevet - Vérifier une facture | expression, arbre commencé, remise mal placée, cinquième boîte, prix maximal |
| 2707 | Type brevet - Organiser une sortie de fin d'année | tableau de tarifs, ordre de grandeur, distributivité, traduction, partage, calculatrice |

Progression 3 Découverte / 3 Entraînement / 2 Problème / 2 Type brevet. Chaque corrigé : méthode, étapes détaillées et alignées, résultat encadré, et une erreur fréquente ou un « À retenir ». Couverture détaillée dans `COUVERTURE.md`.

- 2705, 2706, 2723, 2724 : thème gardé, contenu refait et complété (crochets, ordre de grandeur, tableau, arbre, prix maximal) ; 2706 passe de « bouteilles » seul à la division par un décimal posée.
- 2709, 2710, 2716, 2717 : refaits et enrichis (3 questions → 5 ou 6, arbres, crochets, phrase ↔ calcul dans les deux sens).
- 2707 et 2714 : refaits de zéro (même Id, nouveau titre) : ils étaient des copies d'autres exercices.
- Aucune erreur de maths dans l'ancien contenu ; défauts corrigés : 15 exercices sur 21 étaient le même énoncé avec d'autres nombres, et des titres d'étapes copiés d'un autre exercice (« Évaluer le prix des carnets » dans l'exercice des bouteilles).

### Exercices retirés (11)

2708, 2711, 2712, 2713, 2715, 2718, 2719, 2720, 2721, 2722, 2725 : variantes de « Les fournitures des ateliers », « Le budget du club » et « Remplir des bouteilles sans gaspiller » (mêmes questions, autres valeurs).

### Figures (style livre, `figures/figures.py`)

- **21 figures neuves, 23 emplacements** ; il n'y avait aucune image en ligne (0 conservée, 0 supprimée).
- Cours (5) : schéma des priorités, arbre de $2 \times (9 - 4) + 6$, modèle d'aire de $7 \times 102$, division posée de $75{,}6 \div 6$, schéma en barres des places de cinéma. Fiche (2) : priorités, arbre.
- Exercices : arbres vides à l'énoncé et complétés en vert au corrigé (2709, 2710), arbre commencé (case $24$ donnée) puis complété (2724), deux arbres comparés (2716), modèle d'aire énoncé / corrigé (2717), division posée et bouteilles (2706), écrans de calculatrice (2714), schéma en barres énoncé / corrigé (2705), schéma du coût et du partage (2707).
- Les valeurs des arbres sont calculées dans `figures.py` (fractions exactes). `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance ; toutes ≤ 900 px. Après relecture sur téléphone : 6 figures rétrécies (aire, cinéma, ateliers, bouteilles, sortie, deux arbres) pour ne plus être réduites.

### Contrôles

- `verif_261.py` : **242 contrôles** sympy en fractions exactes (cours, fiche, chaque question des 10 exercices, mauvais calculs analysés, valeurs dessinées dans les figures), tout juste.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (notes : 10 titres changés, 11 exercices retirés volontairement).
- `controle_apercu.mjs` avec captures (`captures_refonte/`) : « Aucun problème détecté ». Captures téléphone regardées en deux passes groupées (cours, fiche, 10 exercices). Corrigé après la première passe : distributivité et chaînes de calcul trop longues (cours, 2705, 2717, 2723, 2724, 2707) découpées en calculs alignés, virgule orpheline (2707), point orphelin (cours), unités « € » et « L » collées aux nombres par une espace insécable, tableau du vocabulaire allégé.

### Remarques pour l'orchestrateur

- Après l'import : `retirer_exercices.py` pour les 11 Id de `exercices_retires.txt`.
- Programme : division par un décimal et calcul posé gardés (5e) ; distributivité seulement numérique (le calcul littéral est dans la notion 269).

## Historique : révision du 30 octobre 2026

État : prêt, révision pédagogique contrôlée le 30 octobre 2026.

Sauvegarde intégrale des contenus et figures antérieurs : `sauvegardes/revision_2026-10-30/`. Les anciens aperçus et preuves restent conservés.

21 identifiants et 21 blocs conservés ; aucun ajout. Six variantes remplacées par des exercices de démarches différentes :
- Id 2709 : Calculer dans le bon ordre.
- Id 2710 : Choisir les parenthèses.
- Id 2716 : Du vocabulaire à l’expression.
- Id 2717 : Calculer mentalement avec la distributivité.
- Id 2723 : Comparer deux tarifs de sortie.
- Id 2724 : Vérifier une facture avec remise.

Les cinq anciens problèmes restants, qui ne changeaient que les valeurs, sont reclassés en entraînement. Répartition : 7 découvertes, 12 entraînements, 2 problèmes. Titres uniques et préfixes cohérents. Couverture détaillée dans `COUVERTURE.md`.

Rédaction : méthodes courtes, étapes aux titres précis, étapes distinctes pour les raisonnements composés, calculs alignés, conclusions courtes et note pédagogique par exercice. Les fiches restent synthétiques. Le cours existant, complet sur ce périmètre, est conservé et relu.

Figures : 0 actives, dont 0 réutilisées et 0 nouvelles ; 0 anciens appels devenus inutiles retirés sans effacer leurs fichiers. Aucune figure nouvelle nécessaire.

Mathématiques : 287 contrôles du contenu conservé et 237 contrôles de révision, zéro échec. Calculs exacts rationnels et SymPy, vérifications des contraintes, des listes et des coordonnées graphiques dans les scripts conservés. Les assertions volontairement fausses des questions d’analyse d’erreur sont distinguées des résultats affirmés.

Rendu : vérificateur courant avec navigateur, syntaxe et correspondances OK ; audit complet de 65 vues à 390 px et des mêmes 65 vues à 1 280 px, sans débordement, formule erronée, image manquante ou bloc invalide. Captures du cours entier, fiche et trois nouveaux exercices (découverte, entraînement, problème), énoncés et étapes, regardées sur mobile. Journaux : `validation_revision.log`, `captures_revision.log`, `resultats_controles.json`.

Défaut d’outil Windows déjà établi : le nettoyage du profil temporaire Chrome peut boucler après la fin des contrôles. Le vérificateur courant est repris localement, avec les mêmes contrôles ; seule la fermeture du navigateur est bornée à deux secondes. La passe navigateur inclut directement les captures pour éviter un audit identique répété. Aucun outil partagé ni moteur du site modifié.

Contrôle complémentaire : les 65 panneaux de la notion ont aussi été inspectés après composition MathJax avec les sélecteurs `mjx-merror`, `.mjx-merror`, `[data-mjx-error]` et `.MathJax_Error`, ainsi que le message « Math input error » : zéro anomalie (`controle_mathjax_etendu.json`). Les caractères de contrôle interdits ont été recherchés dans les trois fichiers finaux : aucun trouvé.

Aucun import, aucune écriture en base, aucune modification des sources en ligne. Programme de Cinquième rentrée 2026, BO du 5 mars 2026 vérifié par la coordination.
