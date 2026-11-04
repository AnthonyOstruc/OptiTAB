# Notion 265 — Fractions, quotients et comparaisons (5e)

## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-10-exercices-265). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés, 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde des fichiers finaux précédents : `sauvegardes/avant_refonte_20261104/`.

Consigne du propriétaire reçue en cours de travail et appliquée : pas de brevet en 5e. L'exercice de fin s'appelle « Synthèse - … », et le mot « brevet » n'apparaît nulle part (contrôle automatique dans `verif_265.py`). Chaque exercice a été relu pour rester au niveau d'un manuel de 5e : comparaisons limitées aux dénominateurs égaux ou multiples l'un de l'autre, aucune addition de fractions de dénominateurs différents (notion 266).

### Cours et fiche
- **Cours 260 réécrit façon manuel** (titre inchangé), en 5 parties :
  - I. Fraction et quotient : définition, lecture, comparaison à 1, partage de 2 crêpes entre 5, définition du quotient $b \times \frac{a}{b} = a$, écriture décimale, valeur exacte ou approchée ($\frac{5}{6} \approx 0{,}83$), remarque sur l'écriture fractionnaire ;
  - II. Fractions égales : figure 2/3 = 4/6 = 8/12, propriété, simplifier, compléter, même dénominateur, erreur « ajouter le même nombre » ;
  - III. Comparer et ranger : même dénominateur, comparaison à 1, dénominateurs multiples, rangement, erreur « dénominateurs seuls » ;
  - IV. Droite graduée : méthode, fractions supérieures à 1, erreur « traits / intervalles » ;
  - V. Fraction d'une quantité : deux ordres de calcul, fractions d'heure, unité de référence, encadré « À retenir ».
- **Fiche 180 refaite** : 6 parties denses, 2 figures, 5 erreurs classiques.
- Les exemples du cours et de la fiche sont tous différents de ceux des exercices.

### Exercices gardés (10), tous réécrits entièrement
| Id | Titre | Capacités |
|---|---|---|
| 2789 | Découverte - Fraction, partage et quotient | lire des fractions (disque, barre, 5/4) ; 2 tablettes pour 3 enfants ; $b \times \dots = a$ ; écriture décimale, $\frac{2}{3} \neq 0{,}67$ |
| 2803 | Découverte - Prendre une fraction d'une quantité | 3/4 de 24 L (barre), 3 calculs, les deux ordres de calcul, fractions d'heure |
| 2794 | Découverte - Écrire des fractions égales | barres 3/4 = 6/8, compléter, simplifier, même dénominateur, erreur « ajouter 2 » |
| 2790 | Entraînement - Comparer des fractions | même dénominateur, comparaison à 1, dénominateurs multiples, rubans 3/8 et 5/16 |
| 2800 | Entraînement - Ranger et encadrer des fractions | ordre croissant (seizièmes), ordre décroissant (douzièmes), encadrement par deux entiers, intercaler |
| 2801 | Entraînement - Placer des fractions sur une droite graduée | lire des abscisses, placer des points, décomposer 11/4 = 2 + 3/4, ranger avec la droite |
| 2793 | Problème - Des pizzas à partager | quotient (3 pour 4, 5 pour 8), comparaison, écritures décimales, 3/4 de 8 |
| 2808 | Problème - Deux gourdes, deux quantités de départ | 4/5 de 50 cL contre 7/10 de 100 cL : plus grande fraction mais moins d'eau |
| 2807 | Problème - Une réserve d'eau qui diminue | 2/5 puis 1/3 du reste, fraction totale 3/5, erreur de quantité de départ, moitié |
| 2809 | Synthèse - Le cross du collège | 4 parties : fraction d'un effectif, simplification, droite graduée en km, comparaison, 9/8 > 1, quotient 5/8 L = 62,5 cL |

- Progression : 3 Découverte, 3 Entraînement, 3 Problème, 1 Synthèse.
- Chaque corrigé contient la méthode, les étapes détaillées, le résultat encadré et une erreur fréquente. `Solution:` est courte.
- Ensemble, ces 10 exercices couvrent toutes les capacités demandées : fraction et quotient ; fractions égales (simplifier, même dénominateur) ; comparer et ranger (même dénominateur, dénominateurs multiples, comparaison à 1) ; droite graduée ; fraction d'une quantité ; problèmes.

### Exercices retirés (11)
- 2791, 2795, 2796, 2798, 2802, 2805 : « La réserve de jus » / « Une collection à partager ». C'était le même exercice à six questions, avec d'autres valeurs (doublons de 2789 et de 2803).
- 2792, 2797, 2799, 2804, 2806 : « Comparer deux portions de ruban ». Mêmes questions, autres fractions (doublons de 2790).

### Figures (25 neuves, style des livres, `figures/figures.py`)
- Toutes les anciennes figures sont refaites (rubans, droite de 2801, unité du cours). Les 5 images en ligne qui ne sont plus appelées seront supprimées à l'import. Aucune image en ligne n'est conservée.
- **Cours (5)** : unité et 7/4, crêpes, barres égales, droite en tiers, 3/5 de 40 €. **Fiche (2)** : droite et quantité (reprises du cours).
- **Exercices** : énoncé avec la figure vierge, corrigé avec les parts ou les points en vert.
  - Barres et disques : 2789 (lecture, tablettes), 2803 (jus), 2794 (barres A/B), 2790 (rubans), 2793 (pizzas), 2808 (gourdes à l'échelle 50/100), 2807 (réserve en 5 parts de 30 L).
  - Droites graduées : 2800 (seizièmes), 2801 (quarts), 2809 (parcours en km).
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance.
- Après la 1re passe de captures, toutes les figures ont été ramenées entre 460 et 720 px de large. Les figures des corrigés et du cours ont été sorties des cadres, pour s'afficher en pleine largeur sur téléphone.

### Contrôles
- `verif_265.py` : **150 contrôles**, tous justes. Ils portent sur :
  - chaque calcul, refait en fractions exactes `sympy.Rational` ;
  - les positions des figures ;
  - les titres, les types et la progression ;
  - l'absence de « brevet » ;
  - le décompte des exercices : 10 gardés + 11 retirés = 21.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (notes : 10 titres changés, 11 retraits volontaires). Journal : `265_validation.log`.
- `controle_apercu.mjs` avec captures : « Aucun problème détecté », sur téléphone et sur ordinateur (`captures.log`).
- Captures téléphone regardées en deux passes groupées : cours (5 écrans), fiche, exercices 2789 (énoncé et étapes), 2801, 2808, 2809.
- Corrigé après la 1re passe :
  - figures trop larges ;
  - tableau de la fiche qui débordait, remplacé par une liste ;
  - sous-questions a)/b) séparées par une figure ;
  - formule `\text{}` peu lisible dans 2809.

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 265`, lancer `retirer_exercices.py` (11 Id).
- Les comparaisons restent limitées aux dénominateurs égaux ou multiples l'un de l'autre, comme au programme de 5e.

---

## Historique : révision du 30 octobre 2026

État : prêt, révision pédagogique contrôlée le 30 octobre 2026.

Sauvegarde intégrale des contenus et figures antérieurs : `sauvegardes/revision_2026-10-30/`. Les anciens aperçus et preuves restent conservés.

21 identifiants et 21 blocs conservés ; aucun ajout. Six variantes remplacées par des exercices de démarches différentes :
- Id 2793 : Passer d’une écriture à l’autre.
- Id 2794 : Compléter des fractions égales.
- Id 2800 : Construire un dénominateur commun.
- Id 2801 : Placer des fractions supérieures à un.
- Id 2807 : Une réserve et deux unités de référence.
- Id 2808 : Des fractions différentes pour la même quantité.

Les cinq anciens problèmes restants, qui ne changeaient que les valeurs, sont reclassés en entraînement. Répartition : 7 découvertes, 12 entraînements, 2 problèmes. Titres uniques et préfixes cohérents. Couverture détaillée dans `COUVERTURE.md`.

Rédaction : méthodes courtes, étapes aux titres précis, étapes distinctes pour les raisonnements composés, calculs alignés, conclusions courtes et note pédagogique par exercice. Les fiches restent synthétiques. Le cours existant, complet sur ce périmètre, est conservé et relu.

Figures : 9 actives, dont 7 réutilisées et 2 nouvelles ; 3 anciens appels devenus inutiles retirés sans effacer leurs fichiers. Les nouveaux énoncés de lecture/placement ont chacun une correction graphique exacte, réponses en vert. Les PNG nouveaux ont été regardés et contrôlés sans chevauchement.

Mathématiques : 227 contrôles du contenu conservé et 331 contrôles de révision, zéro échec. Calculs exacts rationnels et SymPy, vérifications des contraintes, des listes et des coordonnées graphiques dans les scripts conservés. Les assertions volontairement fausses des questions d’analyse d’erreur sont distinguées des résultats affirmés.

Rendu : vérificateur courant avec navigateur, syntaxe et correspondances OK ; audit complet de 65 vues à 390 px et des mêmes 65 vues à 1 280 px, sans débordement, formule erronée, image manquante ou bloc invalide. Captures du cours entier, fiche et trois nouveaux exercices (découverte, entraînement, problème), énoncés et étapes, regardées sur mobile. Journaux : `validation_revision.log`, `captures_revision.log`, `resultats_controles.json`.

Défaut d’outil Windows déjà établi : le nettoyage du profil temporaire Chrome peut boucler après la fin des contrôles. Le vérificateur courant est repris localement, avec les mêmes contrôles ; seule la fermeture du navigateur est bornée à deux secondes. La passe navigateur inclut directement les captures pour éviter un audit identique répété. Aucun outil partagé ni moteur du site modifié.

Contrôle complémentaire : les 65 panneaux de la notion ont aussi été inspectés après composition MathJax avec les sélecteurs `mjx-merror`, `.mjx-merror`, `[data-mjx-error]` et `.MathJax_Error`, ainsi que le message « Math input error » : zéro anomalie (`controle_mathjax_etendu.json`). Les caractères de contrôle interdits ont été recherchés dans les trois fichiers finaux : aucun trouvé.

Aucun import, aucune écriture en base, aucune modification des sources en ligne. Programme de Cinquième rentrée 2026, BO du 5 mars 2026 vérifié par la coordination.
