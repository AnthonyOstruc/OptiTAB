# Notion 267 (5e) : Carrés et cubes

## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-10-exercices-267). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés, 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde de l'état de départ : `sauvegardes/avant_refonte_20261104/` (textes, figures.py, correspondance, 12 anciennes images).

### Programme (BO n° 10 du 5 mars 2026, rubrique « Puissances » de 5e)
Vérifié dans `livre/archives/programmes-officiels/cinquieme-audit/` (annexe 2 et exemples Éduscol) : notion de puissance, carré et cube d'un décimal positif, lien aire du carré / volume du cube (cm², cm³) ; carrés de 0 à 12 et cube de 10 ; écrire un nombre sous la forme $a^2$ ou $a^3$ ($64 = 8^2 = 4^3$) ; expressions avec puissances simples ($3 \times 5^2 - 7$ contre $(3 \times 5)^2 - 7$) ; expression littérale avec $x^2$ ou $x^3$, tester une égalité ; contre-exemple (somme de deux carrés parfaits). **Hors programme de 5e, donc absents** : $(-3)^2$ (le produit de relatifs est en 4e), racine carrée et puissances de 10 (4e) ; seule une remarque du cours annonce $2^4$ en 4e. Contrôle automatique dans `verif_267.py` (aucun « \sqrt », « racine » ni « (− »).

### Cours et fiche
- **Cours 262 réécrit façon manuel** (titre inchangé) : I. carré et cube d'un nombre (figures carré 5 × 5 et cube 4 × 4 × 4 couche par couche, définitions, exemples décimaux, vocabulaire exposant / puissance, erreur « l'exposant n'est pas un facteur ») ; II. carrés de 0 à 12, cubes usuels et $10^3$, carré parfait, méthode « écrire comme carré ou cube », encadrement ; III. priorités avec puissances, carré d'une somme, expression littérale ($2x^2$ / $(2x)^2$), tester une égalité et contre-exemple ; IV. aire, volume, aire du disque $\pi \times r^2$, conversions (figure 1 dm³ = 1 000 cm³), effet d'un agrandissement ×10, « À retenir ». Exemples tous différents des exercices.
- **Fiche 182 refaite** : 5 parties denses, 1 figure, 5 erreurs classiques.

### Exercices gardés (10), tous réécrits
| Id | Titre | Capacités |
|---|---|---|
| 2831 | Découverte - Des carreaux et des petits cubes | carrés quadrillés 1 à 4, $n^2$ ; cubes empilés couche par couche, $n^3$ ; $10^3$ ; cm² et cm³ |
| 2833 | Découverte - Écrire et calculer des carrés et des cubes | notation, décimaux ($0{,}3^2 = 0{,}09$), carré/double, cube/triple, erreur $3^2 = 6$, cadenas $10^3$ codes |
| 2835 | Découverte - Carrés parfaits et motifs de points | motif de points, carrés de 0 à 12, retrouver l'étape, 50 n'est pas un carré |
| 2842 | Entraînement - Reconnaître des carrés et des cubes | carrés parfaits, compléter $\dots^2$ / $\dots^3$, $64 = 8^2 = 4^3$, contre-exemple $4 + 9$, ranger des puissances |
| 2838 | Entraînement - Calculer avec des carrés, des cubes et des priorités | $2 \times 6^2 - 9$ / $(2 \times 6)^2 - 9$, $(2+4)^2 \neq 2^2 + 4^2$, cubes dans une expression |
| 2840 | Entraînement - Remplacer une lettre dans une expression avec un carré | $5x^2 - 4$ / $(5x)^2 - 4$, $x = 1{,}5$, tester $x^2 = 2x$, aire du disque |
| 2845 | Problème - Paver une terrasse carrée | $9^2 = 81$ dalles, aires en m², boîtes, agrandissement (19 dalles) |
| 2851 | Problème - Remplir une boîte cubique de petits cubes | $6^2$, $6^3 = 216$, $30^3$ cm³ = 27 L, couche retirée |
| 2849 | Problème - Agrandir un carré et un cube | côté doublé : aire × 4, volume × 8 ; triplé : × 9 et × 27 ; retrouver côté et arête |
| 2847 | Synthèse - Deux programmes de calcul | $3x^2 - 7$ et $(3x)^2 - 7$, décimaux, contre-exemple 0, remonter un programme |

Progression 3 Découverte / 3 Entraînement / 3 Problème / 1 Synthèse. Chaque corrigé : méthode, étapes détaillées et alignées, résultat encadré, erreur fréquente. `Solution:` courte. Aucune mention du brevet.

### Exercices retirés (11)
- 2832, 2834, 2836, 2837, 2839, 2841, 2844 : copies de « Une mosaïque et des cubes » (mêmes six questions, seul le côté changeait) ; capacité reprise par 2831 et 2849.
- 2843 (comparer des puissances), 2846 (trois écritures), 2848 (deux confusions), 2850 (cubes de 6 à 9, non exigibles) : questions utiles reprises dans 2842, 2838 et 2833.

### Figures (18 neuves, style des livres, `figures/figures.py`)
- Toutes les anciennes figures sont refaites : les « cubes fil de fer » sans petits cubes visibles sont remplacés par de vrais empilements en perspective cavalière. Les 7 images en ligne non appelées seront supprimées à l'import. Aucune image en ligne conservée.
- Cours (4) : carré 5 × 5, cube 4 × 4 × 4 (une couche en vert), schéma carré/cube, cube de 1 dm³. Fiche (1) : schéma carré/cube.
- Exercices : énoncé sans réponse, corrigé avec les éléments comptés en vert : 2831 (carrés et cubes), 2835 (motif, points ajoutés en vert), 2845 (terrasse 9 × 9), 2851 (boîte, couche du haut), 2849 (4 carrés, 8 cubes), 2847 (programmes avec 5).
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance ; largeurs 448 à 754 px.

### Contrôles
- `verif_267.py` : **188 contrôles**, tous justes (sympy : chaque calcul du cours, de la fiche, des exercices et des figures ; solutions d'égalités ; structure, titres, progression, 10 + 11 = 21 Id, images appelées = déclarées).
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`267_validation.log`).
- `controle_apercu.mjs` : « Aucun problème détecté », téléphone et ordinateur (`267_captures.log`, captures dans `captures_refonte/`).
- Captures téléphone regardées en deux passes : cours (4 écrans), fiche, exercices 2831, 2840, 2849, 2847. Corrigé après la 1re passe : tableau des cubes et tableaux de deux corrigés coupés (transposé / remplacé par une liste), chaîne $0{,}2^3$ trop longue, texte de la figure du dm³ trop petit, figure corrigée des cubes trop large, « L » isolés en fin de ligne.

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 267`, lancer `retirer_exercices.py` (11 Id).

---

## Historique : révision du 30 octobre 2026

État : prêt — révision pédagogique du 30 octobre 2026.

21 exercices et leurs Id conservés ; 95 questions corrigées. 13 variantes remplacées par des démarches différentes. Les variantes simples autrefois classées en problèmes sont reclassées en entraînements. Titres uniques et préfixes cohérents : 7 découvertes, 12 entraînements, 2 problèmes.

Couverture : Sens des exposants ; carrés de 0 à 12 ; reconnaissance de carrés et cubes ; priorités ; substitution décimale ; aire, volume, conversions et résolution de problèmes de pavage/remplissage. Détail des exercices repères dans COUVERTURE.md. Même moteur et même format optitab:1 que la Terminale : objectifs, sections romaines, méthodes, propriétés, exemples, erreurs et points à retenir. Fiche condensée, étapes nommées selon le raisonnement, résultat par question et solution courte. Relecture indépendante des trente premiers nouveaux exercices du lot ; formulation ambiguë sur le triple corrigée. Sept doublons exacts du chapitre carrés/cubes ont ensuite été remplacés par des questions distinctes, recalculées et relues.

Modifications documentées :
- Id 2833 : Découverte - Carrés et cubes - Lire les exposants (diversification).
- Id 2835 : Découverte - Carrés et cubes - Mémoriser et reconnaître (diversification).
- Id 2838 : Entraînement - Carrés et cubes - Priorités de calcul (diversification).
- Id 2840 : Entraînement - Carrés et cubes - Décimaux et substitution (diversification).
- Id 2842 : Entraînement - Carrés et cubes - Retrouver la base (diversification).
- Id 2843 : Entraînement - Carrés et cubes - Comparer les puissances (diversification).
- Id 2845 : Problème - Carrés et cubes - Paver une terrasse carrée (diversification).
- Id 2846 : Entraînement - Carrés et cubes - Distinguer trois écritures (diversification).
- Id 2847 : Entraînement - Carrés et cubes - Entre deux carrés consécutifs (diversification).
- Id 2848 : Entraînement - Carrés et cubes - Corriger deux confusions (diversification).
- Id 2849 : Entraînement - Carrés et cubes - Retrouver une longueur (diversification).
- Id 2850 : Entraînement - Carrés et cubes - Calculer et reconnaître des cubes (diversification).
- Id 2851 : Problème - Carrés et cubes - Remplir puis vider un grand cube (diversification).

Mathématiques : ancien audit exact réexécuté sur la version sauvegardée ; égalité des calculs conservés avec cette version contrôlée. 13 nouveaux contextes recalculés indépendamment ; 182 égalités numériques évaluées exactement dans les étapes et résultats courants. Les propositions volontairement fausses des questions d’analyse d’erreur restent distinguées des affirmations des corrigés. Preuves : verifier_revision_20261030.py dans la notion 266, verification_revision_20261030.json et verification_math_avant_revision.json dans chaque notion.

Figures : 11 PNG actifs, sources TikZ conservées ; compilation et contrôle texte/traits OK. Toutes les six figures nouvelles du lot ont été regardées individuellement. Les corrigés de dénombrement, pavage, volume et distributivité présentent la figure résolue ou annotée ; les paramètres des dessins communs sont définis dans le texte. Anciens fichiers conservés.

Rendu : vérificateur courant OK, 130 vues Chrome (390 et 1 280 px), zéro débordement, formule invalide, image absente, bloc en erreur ou élément trop large. Contrôle local renforcé aux erreurs MathJax HTML et SVG et aux caractères de contrôle ; les fractions mal encodées détectées à la relecture ont été corrigées puis la passe complète relancée. Journaux : revision_validation.log, revision_navigateur.log ; statut : controles_revision_20261030.json.

Relecture visuelle : cours mobile entier, fiche et quatre nouveaux exercices (3, 8, 15, 21), énoncés et étapes regardés. Captures et planches dans captures_revision_20261030/. Une fiche en tableau a été réduite à deux colonnes pour rester lisible sur téléphone ; chaînes de calculs et conversions alignées quand nécessaire.

Outil : copie locale du contrôle courant, audits conservés, attente de fermeture Chrome bornée à deux secondes pour contourner le nettoyage temporaire Windows déjà identifié. Aucun outil commun ni moteur frontend modifié.

Sauvegarde préalable : sauvegardes/revision_2026-10-30/. Sources en ligne intactes. Aucun import ni accès en base. Programme de 5e rentrée 2026, BO du 5 mars 2026 vérifié par la coordination ; prolongements identifiés.
