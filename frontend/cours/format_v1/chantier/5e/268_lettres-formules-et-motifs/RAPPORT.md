## Refonte 10 exercices 2026-11-04

**État : prêt** (agent-268-refonte-10ex). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés et réécrits entièrement, 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde des fichiers finaux et figures d'avant la refonte : `sauvegardes/avant_refonte_20261104/`.

### Cours et fiche
- **Cours 263 réécrit façon manuel** (titre inchangé) : I. une lettre pour désigner un nombre (expression littérale, tableau de traductions) ; II. conventions d'écriture ($\times$ sous-entendu, $a^2$, $a^3$, erreurs $47$ / $a^2 \neq 2a$ / $3a^2$) ; III. produire une formule (rectangle et carré, prix fixe + variable, motif qui grandit avec la méthode « découper puis vérifier ») ; IV. remplacer une lettre par un nombre, tester une égalité, contre-exemple ; V. programmes de calcul (parenthèses) ; VI. formules de tableur (`=`, `*`, recopie vers le bas) ; « À retenir ».
- **Fiche 183 refaite** : tableau des conventions, formules, calculer et tester, programme et tableur, 5 erreurs classiques ; 2 figures.
- Pas de développement ni de réduction (notion 269), pas de résolution d'équation au sens de la notion 270 (les « à quelle étape ? » se traitent en remontant le calcul puis en vérifiant). Exemples du cours différents des exercices. Aucune mention du brevet.

### Exercices gardés (10)
| Id | Titre | Capacités |
|---|---|---|
| 2854 | Découverte - Écrire avec des lettres | traduire des phrases, supprimer / rétablir les $\times$, $4 \times 7 \neq 47$, $2(x+5)$ et $2x+5$ |
| 2861 | Découverte - Remplacer une lettre par un nombre | substituer (entier, décimal, priorités), erreur $(5x)^2$, tester $3x+5 = x^2+1$, contre-exemple |
| 2852 | Découverte - Un motif de triangles en allumettes | étapes 1-3, tableau, formule $2n+1$ par découpage, rang double |
| 2856 | Entraînement - Formules de périmètre et d'aire | carré, rectangle, triangle équilatéral, hexagone régulier ; calculs ; $4c = c^2$ testé ; unités |
| 2853 | Entraînement - Traduire un programme de calcul | deux programmes ($4x+3$ / $4(x+3)$), expression → programme, $x^2+6$ |
| 2859 | Entraînement - Des formules dans un tableur | `=3*A2+4`, `=A2*A2`, recopie, valeurs, égalité lue sur la feuille, erreur `=3A2+4` |
| 2872 | Problème - Comparer deux tarifs | produire $5n$ et $3n+12$, tableau, égalité pour $n=6$, contre-exemple, économie |
| 2866 | Problème - Une bordure de carreaux | formule $4n+4$ par découpage, étapes 10 et 25, 64 carreaux → étape 15, 50 impossible |
| 2867 | Synthèse - Les tables de la cantine | motif $2n+2$, programme faux $2(n+2)$ réfuté, formule de tableur, 30 tables, 50 chaises |
| 2868 | Synthèse - Le potager de Léo | côtés littéraux $x$ et $x+5$, $P$ et $A$, tableur, égalité pour $x=6$, affirmation réfutée |

Progression : 3 Découverte, 3 Entraînement, 2 Problème, 2 Synthèse. Chaque corrigé : méthode, étapes détaillées, résultat encadré, erreur fréquente ; `Solution:` courte.

### Exercices retirés (11)
2855, 2857, 2858, 2860, 2862, 2863, 2864, 2865, 2869, 2870, 2871 : le même exercice « frise d'allumettes, n au rang 1 puis +k par rang » (six questions identiques), seules les valeurs changeaient. Les Id 2853, 2867 et 2868, eux aussi des copies, ont été réutilisés pour le programme de calcul et les deux synthèses.

### Figures (23 neuves, style livre, `figures/figures.py`)
- Les 3 anciennes images (`cours_modele`, `bordure_enonce`, `bordure_corrige`) sont supprimées du dossier (copie dans la sauvegarde) et remplacées.
- Cours (4) : rectangle et carré à côtés littéraux, carrés d'allumettes étapes 1-3 avec comptage en vert, programme de calcul en schéma, feuille de tableur `=3*A2+1` ; fiche (2) : motif et tableur.
- Exercices : 2852 triangles (étapes 1-3 / étape 3 comptée en vert), 2856 quatre figures (énoncé / formules en vert), 2853 programmes A et B (énoncé / deux corrigés), 2859 tableur (vide / complété en vert), 2866 bordures (étapes 1-3 / côtés en vert, coins en orange), 2867 tables et chaises (étapes / comptage) + programme du cuisinier (énoncé / corrigé), 2868 potager (énoncé / corrigé pour $x = 4$) + tableur (énoncé / corrigé).
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance ; toutes ≤ 680 px (lisibles sur téléphone sans réduction).

### Contrôles
- `verif_268.py` : **251 contrôles** sympy (valeurs exactes) — chaque réponse ; formules des motifs comparées à un **comptage direct** des allumettes, carreaux et chaises jusqu'à l'étape 79 ; formules de tableur exécutées (recopie comprise, `=3A2+4` refusé) ; 129 égalités numériques des textes recalculées automatiquement ; structure (10 exercices, progression, une méthode et un résultat par question, erreur fréquente, solution complète) ; absence du mot « brevet ». 0 erreur.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`268_validation.log`). `controle_apercu.mjs` : 64 vues sur 64 sans problème, téléphone et ordinateur (`268_captures.log`, `captures_refonte/`).
- Captures téléphone regardées en deux passes : cours (4 écrans), fiche, exercices 2861, 2852, 2856, 2859, 2872, 2866, 2867, 2868. Corrigé après la 1re passe : formules trop larges du cours mises en liste, figures resserrées (motif du cours en colonnes, programme, rectangle, quatre figures, bordure), tableau de 2852 et calculs alignés de 2866 / 2868 découpés.

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 268`, lancer `retirer_exercices.py` (11 Id).

---

## Historique : révision du 30 octobre 2026

État : prêt — révision pédagogique du 30 octobre 2026.

21 exercices et leurs Id conservés ; 118 questions corrigées. 6 variantes remplacées par des démarches différentes. Les variantes simples autrefois classées en problèmes sont reclassées en entraînements. Titres uniques et préfixes cohérents : 7 découvertes, 12 entraînements, 2 problèmes.

Couverture : Traduction des mots ; formules de périmètre et aire ; substitution et tableur ; test d’égalité ; motif évolutif et formule expliquée par un dénombrement ; comparaison de tarifs et contre-exemple. Détail des exercices repères dans COUVERTURE.md. Même moteur et même format optitab:1 que la Terminale : objectifs, sections romaines, méthodes, propriétés, exemples, erreurs et points à retenir. Fiche condensée, étapes nommées selon le raisonnement, résultat par question et solution courte. Relecture indépendante des trente premiers nouveaux exercices du lot ; formulation ambiguë sur le triple corrigée. Sept doublons exacts du chapitre carrés/cubes ont ensuite été remplacés par des questions distinctes, recalculées et relues.

Modifications documentées :
- Id 2854 : Découverte - Lettres et formules - Traduire des phrases (diversification).
- Id 2856 : Découverte - Lettres et formules - Périmètre ou aire (diversification).
- Id 2859 : Entraînement - Lettres et formules - Substituer et utiliser un tableur (diversification).
- Id 2861 : Entraînement - Lettres et formules - Tester une égalité (diversification).
- Id 2866 : Problème - Lettres et formules - Une bordure de carreaux (diversification).
- Id 2867 : Entraînement - Lettres, formules et motifs - 2. La frise du collège — Consolidation (difficulté rendue cohérente).
- Id 2868 : Entraînement - Lettres, formules et motifs - 3. Une construction par étapes — Consolidation (difficulté rendue cohérente).
- Id 2869 : Entraînement - Lettres, formules et motifs - 4. Les allumettes du motif — Consolidation (difficulté rendue cohérente).
- Id 2870 : Entraînement - Lettres, formules et motifs - 5. La frise du collège — Consolidation (difficulté rendue cohérente).
- Id 2871 : Entraînement - Lettres, formules et motifs - 6. Une construction par étapes — Consolidation (difficulté rendue cohérente).
- Id 2872 : Problème - Lettres et formules - Comparer deux tarifs (diversification).

Mathématiques : ancien audit exact réexécuté sur la version sauvegardée ; égalité des calculs conservés avec cette version contrôlée. 6 nouveaux contextes recalculés indépendamment ; 177 égalités numériques évaluées exactement dans les étapes et résultats courants. Les propositions volontairement fausses des questions d’analyse d’erreur restent distinguées des affirmations des corrigés. Preuves : verifier_revision_20261030.py dans la notion 266, verification_revision_20261030.json et verification_math_avant_revision.json dans chaque notion.

Figures : 3 PNG actifs, sources TikZ conservées ; compilation et contrôle texte/traits OK. Toutes les six figures nouvelles du lot ont été regardées individuellement. Les corrigés de dénombrement, pavage, volume et distributivité présentent la figure résolue ou annotée ; les paramètres des dessins communs sont définis dans le texte. Anciens fichiers conservés.

Rendu : vérificateur courant OK, 130 vues Chrome (390 et 1 280 px), zéro débordement, formule invalide, image absente, bloc en erreur ou élément trop large. Contrôle local renforcé aux erreurs MathJax HTML et SVG et aux caractères de contrôle ; les fractions mal encodées détectées à la relecture ont été corrigées puis la passe complète relancée. Journaux : revision_validation.log, revision_navigateur.log ; statut : controles_revision_20261030.json.

Relecture visuelle : cours mobile entier, fiche et quatre nouveaux exercices (3, 8, 15, 21), énoncés et étapes regardés. Captures et planches dans captures_revision_20261030/. Une fiche en tableau a été réduite à deux colonnes pour rester lisible sur téléphone ; chaînes de calculs et conversions alignées quand nécessaire.

Outil : copie locale du contrôle courant, audits conservés, attente de fermeture Chrome bornée à deux secondes pour contourner le nettoyage temporaire Windows déjà identifié. Aucun outil commun ni moteur frontend modifié.

Sauvegarde préalable : sauvegardes/revision_2026-10-30/. Sources en ligne intactes. Aucun import ni accès en base. Programme de 5e rentrée 2026, BO du 5 mars 2026 vérifié par la coordination ; prolongements identifiés.
