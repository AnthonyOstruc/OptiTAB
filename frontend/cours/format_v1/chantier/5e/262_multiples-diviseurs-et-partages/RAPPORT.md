# Notion 262 — Multiples, diviseurs et partages (5e)

## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-10-exercices-262). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés, 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée.

### Cours et fiche
- **Cours 257 réécrit façon manuel** (titre inchangé) : I. division euclidienne (situation des jetons, définition avec dividende / diviseur / quotient / reste, méthode pour poser, exemple 158 ÷ 7 posé, erreur « reste trop grand », encadrement) ; II. multiples et diviseurs (définition, exemples, 0 et 1, méthode par paires, rectangles de 24, erreur « inverser les mots ») ; III. critères par 2, 3, **4**, 5, 9, 10 (le critère de 4 manquait), exemple 1 548, erreurs fréquentes ; IV. **nombres premiers** (avant en simple « pour aller plus loin ») : définition, exemples, crible, premiers < 30 à connaître, méthode « premier ou non » (tester 2, 3, 5, 7 sous 100), erreurs ; V. partages et regroupements (interpréter quotient / reste, q + 1 contenants, lots identiques, rendez-vous), « À retenir ».
- **Fiche 177 refaite** : formule et potence annotée, contrôle, multiples / diviseurs, tableau des critères, premiers < 30, tableau « situation → outil », 5 erreurs classiques. Exemples du cours et de la fiche différents de ceux des exercices.

### Exercices gardés (10) — tous réécrits entièrement
| Id | Titre | Capacité |
|---|---|---|
| 2731 | Découverte - Effectuer une division euclidienne | potence 347 ÷ 9 (termes), poser 254 ÷ 6, reste trop grand, en déduire 260 ÷ 6 |
| 2726 | Découverte - Reconnaître des multiples et des diviseurs | vocabulaire, multiples de 8, justification par le reste, vrai / faux (0, 1) |
| 2730 | Découverte - Utiliser les critères de divisibilité | tableau 2/3/4/5/9/10 pour 4 nombres, pair ≠ divisible par 4, plus petit multiple de 2, 5, 9 |
| 2738 | Entraînement - Des rectangles d'aire imposée | diviseurs de 36 par paires, périmètres, 37 premier |
| 2737 | Entraînement - Trouver un chiffre manquant | critères combinés (3, 9, 5, 4) |
| 2728 | Entraînement - Reconnaître des nombres premiers | 1 et 2, crible jusqu'à 50, 51 / 57 / 91 / 97, contre-exemple « impair » |
| 2729 | Problème - Ranger des œufs en boîtes | regroupement : q, q + 1, places vides, partage entre 3 épiceries |
| 2727 | Problème - Préparer des sachets de bonbons | lots identiques : diviseurs communs, maximum, piège du total |
| 2745 | Problème - Deux navettes aux départs décalés | multiples communs, départs décalés, intervalles / départs |
| 2744 | Type brevet - Organiser une kermesse | 3 parties : division posée (minibus), lots avec contrainte, tombola (critères, nombre premier) |

Progression : 3 Découverte, 3 Entraînement, 3 Problème, 1 Type brevet. Chaque corrigé : méthode, étapes détaillées, résultat encadré, erreur fréquente ; `Solution:` courte.

### Exercices retirés (11)
2732, 2733, 2736, 2739, 2740, 2743, 2746 (« Des places pour une sortie » : même exercice que 2729 avec d'autres nombres) ; 2734, 2741 (lots de cartes, doublons de 2727) ; 2735, 2742 (signaux lumineux, doublons de 2745). Raisons détaillées dans `exercices_retires.txt`.

### Figures (17 neuves, style livre, `figures/figures.py`)
- Il n'y avait aucune figure en ligne. Cours (5) : jetons en paquets, potence annotée 158 ÷ 7, rectangles de 24, crible 1-50, lots 12 billes / 18 cubes ; fiche (1) : potence annotée.
- Exercices : 2731 (potence de l'énoncé + corrigé annoté en vert + 254 ÷ 6 en vert), 2738 (rectangles de 36 en vert), 2728 (crible vierge / crible corrigé en vert), 2729 (œufs + boîte vide / 6 boîtes en vert et reste), 2727 (bonbons / 6 sachets en vert), 2745 (frise des départs, rendez-vous en vert), 2744 (213 ÷ 9 en vert).
- Divisions posées générées par calcul (étapes contrôlées dans `verif_262.py`). `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance ; toutes ≤ 900 px. Après captures : jetons en paquets verticaux, potence resserrée, œufs sur 2 rangées, frise réduite (lisibilité téléphone).

### Contrôles
- `verif_262.py` : **144 contrôles** sympy / Python (divisions, diviseurs, critères, crible, primalité, problèmes rejoués, étapes des divisions dessinées), tout juste.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (notes : 10 titres changés, 11 exercices retirés volontairement). `controle_apercu.mjs` avec captures : aucun problème (téléphone et ordinateur). Journal : `262_validation.log`.
- Captures téléphone regardées en deux passes : cours (5 écrans), fiche, exercices 2731, 2730, 2729, 2727, 2744. Corrigé après la 1re passe : figures trop larges (voir ci-dessus), en-tête du tableau des critères raccourci, chaînes de produits de 84, 126 et 30 découpées en lignes alignées (débordaient).

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 262`, lancer `retirer_exercices.py` (11 Id).
- Le critère de divisibilité par 4 et les nombres premiers sont traités comme exigibles (consigne du programme 5e reçue) ; « plus grand diviseur commun » / « plus petit multiple commun » restent en toutes lettres, sans notation.

---

## Historique : révision du 30 octobre 2026

État : prêt, révision pédagogique contrôlée le 30 octobre 2026.

Sauvegarde intégrale des contenus et figures antérieurs : `sauvegardes/revision_2026-10-30/`. Les anciens aperçus et preuves restent conservés.

21 identifiants et 21 blocs conservés ; aucun ajout. Six variantes remplacées par des exercices de démarches différentes :
- Id 2730 : Utiliser les critères de divisibilité.
- Id 2731 : Reconnaître une division euclidienne.
- Id 2737 : Trouver un chiffre inconnu.
- Id 2738 : Des rectangles d’aire imposée.
- Id 2744 : Des lots sous plusieurs contraintes.
- Id 2745 : Deux navettes aux départs décalés.

Les cinq anciens problèmes restants, qui ne changeaient que les valeurs, sont reclassés en entraînement. Répartition : 7 découvertes, 12 entraînements, 2 problèmes. Titres uniques et préfixes cohérents. Couverture détaillée dans `COUVERTURE.md`.

Rédaction : méthodes courtes, étapes aux titres précis, étapes distinctes pour les raisonnements composés, calculs alignés, conclusions courtes et note pédagogique par exercice. Les fiches restent synthétiques. Le cours existant, complet sur ce périmètre, est conservé et relu.

Figures : 0 actives, dont 0 réutilisées et 0 nouvelles ; 0 anciens appels devenus inutiles retirés sans effacer leurs fichiers. Aucune figure nouvelle nécessaire.

Mathématiques : 237 contrôles du contenu conservé et 261 contrôles de révision, zéro échec. Calculs exacts rationnels et SymPy, vérifications des contraintes, des listes et des coordonnées graphiques dans les scripts conservés. Les assertions volontairement fausses des questions d’analyse d’erreur sont distinguées des résultats affirmés.

Rendu : vérificateur courant avec navigateur, syntaxe et correspondances OK ; audit complet de 65 vues à 390 px et des mêmes 65 vues à 1 280 px, sans débordement, formule erronée, image manquante ou bloc invalide. Captures du cours entier, fiche et trois nouveaux exercices (découverte, entraînement, problème), énoncés et étapes, regardées sur mobile. Journaux : `validation_revision.log`, `captures_revision.log`, `resultats_controles.json`.

Défaut d’outil Windows déjà établi : le nettoyage du profil temporaire Chrome peut boucler après la fin des contrôles. Le vérificateur courant est repris localement, avec les mêmes contrôles ; seule la fermeture du navigateur est bornée à deux secondes. La passe navigateur inclut directement les captures pour éviter un audit identique répété. Aucun outil partagé ni moteur du site modifié.

Contrôle complémentaire : les 65 panneaux de la notion ont aussi été inspectés après composition MathJax avec les sélecteurs `mjx-merror`, `.mjx-merror`, `[data-mjx-error]` et `.MathJax_Error`, ainsi que le message « Math input error » : zéro anomalie (`controle_mathjax_etendu.json`). Les caractères de contrôle interdits ont été recherchés dans les trois fichiers finaux : aucun trouvé.

Aucun import, aucune écriture en base, aucune modification des sources en ligne. Programme de Cinquième rentrée 2026, BO du 5 mars 2026 vérifié par la coordination.
