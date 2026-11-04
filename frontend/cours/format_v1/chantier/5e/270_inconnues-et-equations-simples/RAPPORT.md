# Notion 270 (5e) : Inconnues et équations simples

## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-5e-270). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés, 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde de l'état de départ : `sauvegardes/avant_refonte_20261104/` (textes, RAPPORT, figures.py, correspondance, 2 anciennes images).

### Programme (BO n° 10 du 5 mars 2026, « Calcul littéral et algébrique » de 5e)
Vérifié dans `livre/archives/programmes-officiels/cinquieme-audit/` (annexe 2 et exemples Éduscol) : donner à la lettre le statut d'inconnue ; tester si une égalité est vraie ou fausse ; modéliser des problèmes d'opérations à trou par $ax = c$ ou $x + b = c$ ; les résoudre par les opérations inverses (décimaux, fractions simples, $\frac{x}{3} = 1$, cas $2x = 0$ et $\frac{x}{2} = 0$ explicités), avec schémas en barres et balances, et vérifier. Prolongement : al-Khwarizmi (« la chose »). **La résolution de $ax + b = c$ est un objectif de 4e** : elle n'est traitée ici que par le raisonnement (remonter deux opérations, ou par essais), avec une remarque « Pour aller plus loin » ; aucune technique de transposition, rien sur $ax + b = cx + d$ sauf pour **tester** une valeur.

### Cours et fiche
- **Cours 265 réécrit façon manuel** (titre inchangé) : I. équation, inconnue, membres, solution ; méthode « tester une égalité » ($5x - 3 = 2x + 9$ avec 4 et 2) ; II. opérations inverses : $x + b = c$ (balance, décimaux, solution négative, fraction), $x - b = c$, $ax = c$ (balance, décimal, division par un décimal, quotient $\frac{2}{3}$), $\frac{x}{a} = c$, cas avec zéro, 3 erreurs fréquentes ; III. méthode en 4 étapes, deux exemples avec schéma en barres (livre, étagères), « la réponse doit avoir un sens », remonter deux opérations (cahiers et règle, par essais aussi), al-Khwarizmi, « À retenir ». Exemples tous différents des exercices.
- **Fiche 185 refaite** : vocabulaire, test, tableau des opérations inverses, méthode, 2 figures, 5 erreurs classiques.

### Exercices gardés (10)
| Id | Titre | Capacités |
|---|---|---|
| 2897 | Découverte - Tester si un nombre est solution | tester une valeur, lettre dans les deux membres, $0$ solution ou non |
| 2896 | Découverte - Additions à trou et balances | balances A et B, $x + b = c$ (décimaux, $27 + x$), solution négative, $x - b = c$ |
| 2898 | Découverte - Multiplications et divisions à trou | balance $4x = 18$, $ax = c$ (décimal, quotient $\frac{3}{7}$), $\frac{x}{a} = c$, cas avec zéro, erreur « soustraire 3 » |
| 2903 | Entraînement - Décimaux, relatifs et fractions | relatifs, division par un décimal, fractions ($\frac{7}{12}$), encadrer $\frac{7}{3}$ par essais |
| 2901 | Entraînement - Mettre en équation des situations simples | 5 situations (distance, ruban, prix, température, partage), choix de l'équation, schémas en barres |
| 2908 | Entraînement - Vérifier et corriger des résolutions | 6 résolutions fausses à tester et corriger (une par opération inverse) |
| 2914 | Problème - Remplir des flacons | $m + 1{,}2 = 4{,}8$ puis $8x = 3{,}6$, conversion, comparaison |
| 2904 | Problème - Billes et ruban en schémas | $t + 3t = 4t = 64$ ; ruban $2x + 0{,}6 = 2{,}4$ en remontant (schémas en barres) |
| 2900 | Problème - Retrouver le nombre de départ d'un programme | programmes à une étape ($6x = 45$, $x + 2{,}5 = 1$) puis à deux étapes : essais et opérations inverses dans l'ordre inverse |
| 2902 | Synthèse - Organiser une sortie au musée | $18n = 540$, tester $36$ dans $15n = 540$, $30e = 165$, $r + 20 = 23{,}5$, $8p = 60$ interprété (nombre entier de paquets) |

Progression 3 Découverte / 3 Entraînement / 3 Problème / 1 Synthèse. Tous les exercices sont réécrits de zéro (contenus de 5e, niveau manuel). Chaque corrigé : méthode, étapes détaillées, résultat encadré par question, erreur fréquente ou « À retenir ». `Solution:` courte. Aucune mention du brevet.

### Exercices retirés (11)
- 2894, 2895, 2899, 2911, 2909, 2910, 2906, 2913 : copies de « n pochettes pour T € » (mêmes six questions, seuls les prix changeaient) ; capacités reprises par 2898, 2901, 2904, 2900.
- 2905, 2912, 2907 : copies de « Retrouver le nombre partagé » ($\frac{x}{a} = c$, seul le diviseur changeait) ; repris par 2898 (questions 3 et 4) et 2901 (question 5).
- L'Id 2897 (ancienne copie « 2 pochettes pour 14 € ») est réutilisé pour l'exercice « Tester si un nombre est solution », capacité absente auparavant.

### Figures (23 neuves, style des livres, `figures/figures.py`)
- Les 2 anciennes figures (schémas « pochettes » génériques avec $n$, $b$, $T$) sont abandonnées ; les 10 images en ligne non appelées seront supprimées à l'import. Aucune image en ligne conservée.
- Balances (machinerie de la 256, 4e) : cours $x + 5 = 12$ et $3x = 12$ (étape « on enlève / on garde le tiers », solution en vert) ; 2896 (A, B, énoncé et corrigé) ; 2898 (énoncé et corrigé).
- Schémas en barres (données dans l'énoncé, valeur trouvée en vert dans le corrigé) : cours (livre, étagères, cahiers), 2901 (randonnée, ruban), 2914 (bidon puis 8 flacons), 2904 (billes, ruban).
- Programme de calcul à l'endroit / à l'envers : 2900 (énoncé et corrigé).
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance ; largeurs 507 à 708 px (toutes ≤ 900 px, aucune réduite sur téléphone).

### Contrôles
- `verif_270.py` : **225 contrôles**, tous justes (sympy : chaque équation résolue en nombres exacts, chaque vérification et calcul intermédiaire du cours, de la fiche, des exercices ; valeurs écrites sur les figures ; structure, titres, progression, nombre de questions = étapes = solutions, 10 + 11 = 21 Id, images appelées = déclarées).
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`270_validation.log`).
- `controle_apercu.mjs` : « Aucun problème détecté », téléphone et ordinateur (`270_captures.log`, captures dans `captures_refonte/`).
- Captures téléphone regardées en deux passes : cours (4 écrans), fiche (2), exercices 2896 (énoncé, étapes), 2901, 2903, 2904, 2900, 2902. Corrigé après la 1re passe : trois figures de corrigé trop larges (programme, billes, ruban) resserrées ; unités collées aux nombres par une espace insécable (104 endroits ; « 40 » et « € » étaient séparés en fin de ligne).

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 270`, lancer `retirer_exercices.py` (11 Id).

---

## Historique : révision du 30 octobre 2026

État : prêt — révision pédagogique du 30 octobre 2026.

21 exercices et leurs Id conservés ; 115 questions corrigées. 6 variantes remplacées par des démarches différentes. Les variantes simples autrefois classées en problèmes sont reclassées en entraînements. Titres uniques et préfixes cohérents : 7 découvertes, 12 entraînements, 2 problèmes.

Couverture : Addition, multiplication et division à trous ; opérations inverses ; solution nulle ou négative ; décimaux et fractions simples ; contraintes entières ; mise en équation d’une relation simple ; unités et problèmes à étapes. Détail des exercices repères dans COUVERTURE.md. Même moteur et même format optitab:1 que la Terminale : objectifs, sections romaines, méthodes, propriétés, exemples, erreurs et points à retenir. Fiche condensée, étapes nommées selon le raisonnement, résultat par question et solution courte. Relecture indépendante des trente premiers nouveaux exercices du lot ; formulation ambiguë sur le triple corrigée. Sept doublons exacts du chapitre carrés/cubes ont ensuite été remplacés par des questions distinctes, recalculées et relues.

Les anciennes factures sont recentrées sur ax=c ; l’emballage est calculé à part, par arithmétique. L’extension ax+b=c du cours est explicitement signalée comme prolongement de 4e.

Modifications documentées :
- Id 2894 : Découverte - Inconnues - 2 pochettes pour 8 € (recentrage équation à une opération).
- Id 2895 : Découverte - Inconnues - 3 pochettes pour 15 € (recentrage équation à une opération).
- Id 2896 : Découverte - Inconnues - Retrouver le terme d’une addition (diversification).
- Id 2897 : Découverte - Inconnues - 2 pochettes pour 14 € (recentrage équation à une opération).
- Id 2898 : Découverte - Inconnues - Multiplication et division à trous (diversification).
- Id 2899 : Découverte - Inconnues - 4 pochettes pour 36 € (recentrage équation à une opération).
- Id 2901 : Entraînement - Inconnues - Modéliser une distance et un prix (diversification).
- Id 2902 : Entraînement - Inconnues - 3 pochettes pour 18 € (recentrage équation à une opération).
- Id 2903 : Entraînement - Inconnues - Fractions simples et opérations inverses (diversification).
- Id 2904 : Entraînement - Inconnues - 2 pochettes pour 16 € (recentrage équation à une opération).
- Id 2906 : Entraînement - Inconnues - 4 pochettes pour 40 € (recentrage équation à une opération).
- Id 2908 : Problème - Inconnues - Détecter les fausses résolutions (diversification).
- Id 2909 : Entraînement - Inconnues - 3 pochettes pour 21 € (recentrage équation à une opération).
- Id 2910 : Entraînement - Inconnues - 4 pochettes pour 32 € (recentrage équation à une opération).
- Id 2911 : Entraînement - Inconnues - 2 pochettes pour 18 € (recentrage équation à une opération).
- Id 2912 : Entraînement - Inconnues et équations simples - 5. Retrouver le nombre partagé — Consolidation (difficulté rendue cohérente).
- Id 2913 : Entraînement - Inconnues - 4 pochettes pour 44 € (recentrage équation à une opération).
- Id 2914 : Problème - Inconnues - Préparer huit flacons (diversification).

Mathématiques : ancien audit exact réexécuté sur la version sauvegardée ; égalité des calculs conservés avec cette version contrôlée. 6 nouveaux contextes recalculés indépendamment ; 114 égalités numériques évaluées exactement dans les étapes et résultats courants. Les propositions volontairement fausses des questions d’analyse d’erreur restent distinguées des affirmations des corrigés. Preuves : verifier_revision_20261030.py dans la notion 266, verification_revision_20261030.json et verification_math_avant_revision.json dans chaque notion.

Figures : 2 PNG actifs, sources TikZ conservées ; compilation et contrôle texte/traits OK. Toutes les six figures nouvelles du lot ont été regardées individuellement. Les corrigés de dénombrement, pavage, volume et distributivité présentent la figure résolue ou annotée ; les paramètres des dessins communs sont définis dans le texte. Anciens fichiers conservés.

Rendu : vérificateur courant OK, 130 vues Chrome (390 et 1 280 px), zéro débordement, formule invalide, image absente, bloc en erreur ou élément trop large. Contrôle local renforcé aux erreurs MathJax HTML et SVG et aux caractères de contrôle ; les fractions mal encodées détectées à la relecture ont été corrigées puis la passe complète relancée. Journaux : revision_validation.log, revision_navigateur.log ; statut : controles_revision_20261030.json.

Relecture visuelle : cours mobile entier, fiche et quatre nouveaux exercices (3, 8, 15, 21), énoncés et étapes regardés. Captures et planches dans captures_revision_20261030/. Une fiche en tableau a été réduite à deux colonnes pour rester lisible sur téléphone ; chaînes de calculs et conversions alignées quand nécessaire.

Outil : copie locale du contrôle courant, audits conservés, attente de fermeture Chrome bornée à deux secondes pour contourner le nettoyage temporaire Windows déjà identifié. Aucun outil commun ni moteur frontend modifié.

Sauvegarde préalable : sauvegardes/revision_2026-10-30/. Sources en ligne intactes. Aucun import ni accès en base. Programme de 5e rentrée 2026, BO du 5 mars 2026 vérifié par la coordination ; prolongements identifiés.
