# Notion 269 (5e) : Développer, réduire et démontrer

## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-10-exercices-269). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés, 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde de l'état de départ : `sauvegardes/avant_refonte_20261104/` (cours, fiche, exercices, rapport, figures.py, correspondance, anciennes images).

### Programme (BO n° 10 du 5 mars 2026, « Calcul littéral et algébrique » de 5e)
Vérifié dans `livre/archives/programmes-officiels/cinquieme-audit/annexe2.txt` (p. 8-9) : somme ou produit ; $k(a + b) = ka + kb$ et $k(a - b) = ka - kb$ pour développer et factoriser ; réduire $ax + b$ avec $a$, $b$ décimaux ; tester une égalité ; démontrer une propriété générale par le calcul littéral ; contre-exemple ; conjecturer. Attendus de fin de 5e (Éduscol) : distributivité simple pour réduire $ax + bx$, lettre pour démontrer une propriété générale, substitution pour tester une égalité. **Absents car hors 5e** : double distributivité (4e), produit par un relatif (4e). Pas de doublon avec la 268 (traduire, formules, substitution, tableur, motifs) : ici l'égalité est testée pour savoir si elle est **toujours** vraie.

### Cours et fiche
- **Cours 264 réécrit façon manuel** (titre inchangé) : I. somme ou produit (termes, facteurs, dernière opération) ; II. distributivité simple (modèle d'aire général, exemple numérique), développer (modèle d'aire $3(x + 5)$), factoriser (méthode en 4 temps, erreur du « 1 » oublié), calcul mental ($8 \times 103$, $12 \times 99$, $45 \times 7 + 45 \times 3$, $2{,}6 \times 15 - 2{,}6 \times 5$) ; III. réduire (barres $3x + 5x = 8x$, $ax + bx = (a + b)x$, décimaux, développer puis réduire, $x + x$ / $x \times x$) ; IV. tester une égalité ; V. démontrer (programme de calcul en schéma, nombres pairs, démonstration « somme de deux pairs ») et contre-exemple ; « À retenir ». Exemples tous différents des exercices.
- **Fiche 184 refaite** : 4 parties denses, 1 figure, 5 erreurs classiques.

### Les 10 exercices (tous réécrits)
| Id | Titre | Contenu |
|---|---|---|
| 2875 | Découverte - Compter les carreaux de deux façons | quadrillage $4 \times (6 + 3)$, distributivité numérique, somme / différence / produit |
| 2873 | Découverte - L'aire d'un rectangle découpé | $4(x + 3) = 4x + 12$ par les aires, test $x = 5$, erreur de Tom, développer |
| 2877 | Découverte - Réduire une somme | $3x + 5x$, $2a + 3 + 4a$, décimaux, $x + x$ / $x \times x$, périmètre d'un triangle, contre-exemple |
| 2880 | Entraînement - Développer, puis réduire | 5 développements (dont décimal et différence), 4 « développer puis réduire », copie à corriger, contrôle |
| 2882 | Entraînement - Factoriser une somme | factorisation lue sur un rectangle, 5 factorisations, réduire puis factoriser, le « 1 » oublié |
| 2881 | Entraînement - Calculer mentalement avec la distributivité | $7 \times 102$, $15 \times 99$, facteur commun ($37 \times 6 + 37 \times 4$, $99 \times 5 + 5$), achat, erreur |
| 2874 | Problème - Vrai pour toutes les valeurs ? | 5 égalités testées, contre-exemples, 2 démontrées, 2 corrigées, un test ne suffit pas |
| 2893 | Problème - Deux programmes équivalents ? | essais, conjecture, démonstration $6x + 8$, contre-exemple pour un 3e programme, remonter |
| 2887 | Problème - La somme de trois entiers consécutifs | conjecture, $3(n + 1)$, somme 141, somme 100 impossible, contre-exemple à 4 entiers |
| 2888 | Synthèse - Le jardin partagé | longueur, aire $5(2x + 3) = 10x + 15$, périmètre $4x + 16 = 4(x + 4)$, contre-exemple, preuve |

Progression 3 Découverte / 3 Entraînement / 3 Problème / 1 Synthèse. Chaque corrigé : méthode, étapes détaillées et alignées (une égalité par ligne), résultat encadré, erreur fréquente ou à retenir. `Solution:` courte. Aucune mention du brevet.

### Exercices retirés (11)
2876, 2878, 2879, 2883, 2884, 2885, 2886, 2889, 2890, 2891, 2892 : onze copies du même « rectangle découpé » $k(x + b)$ (mêmes six questions, seuls $k$ et $b$ changeaient). Capacité reprise par 2873, 2882, 2881 et 2888.

### Figures (20 neuves, style des livres, `figures/figures.py`)
- Toutes les anciennes figures sont remplacées (le « schéma de principe » avec $k$ et $b$ à remplacer mentalement est supprimé). Les 24 images en ligne non appelées seront supprimées à l'import. Aucune image en ligne conservée.
- Cours (4) : modèle d'aire $k(a + b)$, modèle d'aire $3(x + 5)$, barres $3x + 5x = 8x$, programme de calcul. Fiche (1) : modèle d'aire $k(a + b)$.
- Exercices, énoncé sans réponse et corrigé avec les morceaux en vert : 2875 (quadrillage), 2873 et 2882 (rectangles découpés), 2877 (triangle et périmètre), 2881 (deux modèles d'aire du calcul mental), 2893 (programmes A et B en schéma, puis chaque programme avec ses expressions), 2887 (preuve en barres : on déplace une unité, tout devient $n + 1$), 2888 (jardin, aires $5x$, $5x$, $15$).
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance ; largeurs 469 à 777 px.

### Contrôles
- `verif_269.py` : **197 contrôles**, tous justes (sympy : chaque développement, réduction, factorisation, test d'égalité, calcul mental et démonstration du cours, de la fiche, des exercices et des figures ; programmes de calcul exécutés ; structure, titres, progression, difficultés, nombre de questions énoncé = corrigé = solution, 10 + 11 = 21 Id, images appelées = déclarées, pas de double distributivité ni de relatif).
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`269_validation.log`).
- `controle_apercu.mjs` : « Aucun problème détecté », téléphone et ordinateur (`269_captures.log`, captures dans `captures_refonte/`).
- Captures téléphone regardées en deux passes : cours (4 écrans), fiche, exercices 2875, 2873, 2877, 2880, 2882, 2881, 2893, 2887, 2888. Corrigé après la 1re passe : 34 chaînes de calcul trop longues (coupées ou réduites) découpées en calculs alignés, exemples du cours découpés, figure en barres resserrée (894 → 707 px).

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 269`, lancer `retirer_exercices.py` (11 Id).
- Moteur (à signaler, non bloquant) : dans la fiche, sur téléphone, la ligne « $ax + bx = (a + b)x$ : $3x + 5x = 8x$ ; … » affichait le second $x$ de $5x$ presque invisible (reproductible, pas sur ordinateur) ; contourné en scindant la ligne en deux puces.

---

## Historique : révision du 30 octobre 2026

État : prêt — révision pédagogique du 30 octobre 2026.

21 exercices et leurs Id conservés ; 116 questions corrigées. 6 variantes remplacées par des démarches différentes. Les variantes simples autrefois classées en problèmes sont reclassées en entraînements. Titres uniques et préfixes cohérents : 7 découvertes, 12 entraînements, 2 problèmes.

Couverture : Structure somme/produit ; distributivité ; réduction ; facteur commun ; calculs décimaux ; aire décomposée ; démonstrations générales et contre-exemples ; programmes de calcul équivalents. Détail des exercices repères dans COUVERTURE.md. Même moteur et même format optitab:1 que la Terminale : objectifs, sections romaines, méthodes, propriétés, exemples, erreurs et points à retenir. Fiche condensée, étapes nommées selon le raisonnement, résultat par question et solution courte. Relecture indépendante des trente premiers nouveaux exercices du lot ; formulation ambiguë sur le triple corrigée. Sept doublons exacts du chapitre carrés/cubes ont ensuite été remplacés par des questions distinctes, recalculées et relues.

Modifications documentées :
- Id 2875 : Découverte - Calcul littéral - Somme ou produit (diversification).
- Id 2877 : Découverte - Calcul littéral - Réduire sans mélanger (diversification).
- Id 2880 : Entraînement - Calcul littéral - Développer puis réduire (diversification).
- Id 2882 : Entraînement - Calcul littéral - Retrouver un facteur commun (diversification).
- Id 2887 : Problème - Calcul littéral - Démontrer et réfuter (diversification).
- Id 2888 : Entraînement - Développer, réduire et démontrer - 2. La banderole de l’atelier — Consolidation (difficulté rendue cohérente).
- Id 2889 : Entraînement - Développer, réduire et démontrer - 3. Deux méthodes pour une aire — Consolidation (difficulté rendue cohérente).
- Id 2890 : Entraînement - Développer, réduire et démontrer - 4. Les rectangles découpés — Consolidation (difficulté rendue cohérente).
- Id 2891 : Entraînement - Développer, réduire et démontrer - 5. La banderole de l’atelier — Consolidation (difficulté rendue cohérente).
- Id 2892 : Entraînement - Développer, réduire et démontrer - 6. Deux méthodes pour une aire — Consolidation (difficulté rendue cohérente).
- Id 2893 : Problème - Calcul littéral - Deux programmes équivalents (diversification).

Mathématiques : ancien audit exact réexécuté sur la version sauvegardée ; égalité des calculs conservés avec cette version contrôlée. 6 nouveaux contextes recalculés indépendamment ; 126 égalités numériques évaluées exactement dans les étapes et résultats courants. Les propositions volontairement fausses des questions d’analyse d’erreur restent distinguées des affirmations des corrigés. Preuves : verifier_revision_20261030.py dans la notion 266, verification_revision_20261030.json et verification_math_avant_revision.json dans chaque notion.

Figures : 3 PNG actifs, sources TikZ conservées ; compilation et contrôle texte/traits OK. Toutes les six figures nouvelles du lot ont été regardées individuellement. Les corrigés de dénombrement, pavage, volume et distributivité présentent la figure résolue ou annotée ; les paramètres des dessins communs sont définis dans le texte. Anciens fichiers conservés.

Rendu : vérificateur courant OK, 130 vues Chrome (390 et 1 280 px), zéro débordement, formule invalide, image absente, bloc en erreur ou élément trop large. Contrôle local renforcé aux erreurs MathJax HTML et SVG et aux caractères de contrôle ; les fractions mal encodées détectées à la relecture ont été corrigées puis la passe complète relancée. Journaux : revision_validation.log, revision_navigateur.log ; statut : controles_revision_20261030.json.

Relecture visuelle : cours mobile entier, fiche et quatre nouveaux exercices (3, 8, 15, 21), énoncés et étapes regardés. Captures et planches dans captures_revision_20261030/. Une fiche en tableau a été réduite à deux colonnes pour rester lisible sur téléphone ; chaînes de calculs et conversions alignées quand nécessaire.

Outil : copie locale du contrôle courant, audits conservés, attente de fermeture Chrome bornée à deux secondes pour contourner le nettoyage temporaire Windows déjà identifié. Aucun outil commun ni moteur frontend modifié.

Sauvegarde préalable : sauvegardes/revision_2026-10-30/. Sources en ligne intactes. Aucun import ni accès en base. Programme de 5e rentrée 2026, BO du 5 mars 2026 vérifié par la coordination ; prolongements identifiés.
