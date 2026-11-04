# Notion 279 (5e) : Hasard et probabilités

## Refonte 10 exercices 2026-11-04

**État : prêt** (agent-279-refonte-10ex). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés, 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde de l'état de départ : `sauvegardes/avant_refonte_20261104/` (textes, RAPPORT, COUVERTURE, figures.py, correspondance, anciennes images).

### Programme (BO 2026, « Probabilités » de 5e)
Vérifié dans `livre/archives/programmes-officiels/cinquieme-audit/` (annexe 2 et exemples de mise en œuvre) : vocabulaire (expérience aléatoire, issue, événement) ; attribuer des probabilités en équiprobabilité, la justifier par la symétrie et la remettre en cause (dé truqué, objets différents) ; automatismes : placer sur l'échelle des probabilités l'impossible, le certain, pile, une valeur du dé, une couleur d'urne, « ne pas gagner au loto », « dix fois le 1 » ; fraction / décimal / pourcentage ; « une chance sur quatre » = 1/4 ; répéter matériellement une expérience et tenir un tableau d'effectifs et de fréquences. **Écartés car hors programme de 5e** : événement contraire et somme des probabilités (4e : « ne pas obtenir… » est seulement compté directement), notations ensemblistes, deux épreuves (4e), nombres premiers (simple prolongement en 5e). La stabilisation des fréquences est présentée comme un **constat** (introduction du cycle 4), sans formalisme. Aucune mention du brevet. Couverture détaillée : `COUVERTURE.md`.

### Cours et fiche
- **Cours 274 réécrit façon manuel** (titre inchangé) : objectifs ; I. expérience aléatoire, issue, événement, issues favorables (dix cartes, impaires en vert), certain / impossible, « peu probable n'est pas impossible » ; II. probabilité, échelle en figure, trois écritures + tableau des « une chance sur… », valeurs approchées (1/6 ≈ 0,17) ; 1. équiprobabilité (quand la supposer, quand non), formule, méthode, exemples pièce / dé, sac de 8 jetons en figure, erreur « compter les couleurs » ; 2. roue aux secteurs inégaux ramenée à 6 secteurs égaux (figure) ; 3. placer sur l'échelle (figure du sac) ; III. fréquence, méthode « répéter dans les mêmes conditions, avec remise », 40 tirages (tableau effectifs / fréquences / probabilités), constat, courbe de 1 000 tirages, « le hasard n'a pas de mémoire », « À retenir ». L'ancienne version parlait d'événement contraire (4e) : retiré. Exemples tous différents des exercices.
- **Fiche 194 refaite** : tableau du vocabulaire, échelle, formules encadrées, écritures, équiprobabilité, fréquence avec courbe, 5 erreurs classiques, réflexe.

### Exercices gardés (10)
| Id | Titre | Capacités |
|---|---|---|
| 3084 | Découverte - Expériences aléatoires, issues et événements | reconnaître l'aléatoire, issues, issues favorables, certain / impossible, événements réalisés, comparer en comptant |
| 3087 | Découverte - Placer des événements sur l'échelle des probabilités | les 7 événements types du programme (pièce, dé, urne, impossible, certain, loto, dix fois le 1), écritures, une chance sur quatre |
| 3083 | Découverte - Tirer une boule dans une urne | justifier l'équiprobabilité, erreur « trois couleurs donc 1/3 », fraction / décimal / %, impossible, « pas jaune », ranger |
| 3096 | Entraînement - Tirer une carte numérotée | 12 cartes : pairs, multiples de 3, diviseurs de 12, ≥ 10 ; une chance sur… ; ranger ; même probabilité ≠ même événement ; carte retirée (5/11) |
| 3103 | Entraînement - Deux roues de loterie | 8 secteurs égaux ; roue 180° / 90° / 90° partagée en quarts (erreur de Léo) ; comparer deux roues |
| 3089 | Entraînement - Lancer une pièce : effectifs et fréquences | 20 lancers réels : tableau d'effectifs, fréquences, peu d'essais ; 500 lancers de la classe ; hasard sans mémoire |
| 3101 | Problème - Choisir le bon sac | 3 sacs, comparer 3/8, 7/16, 1/2 en seizièmes ; erreur « le plus de jaunes » ; pourcentages ; ajouter / retirer des jetons |
| 3094 | Problème - Le dé de Malik et le dé de Nora | 600 lancers de deux dés, fréquences, courbes de stabilisation, dé truqué, 12 lancers ne suffisent pas, pas d'équiprobabilité pour un dé truqué |
| 3092 | Synthèse - Les jeux de la kermesse | roue de 12, urne de 20, dé ; échelle ; meilleur stand ; fréquence sur 240 parties ; hasard sans mémoire |
| 3102 | Synthèse - Un jeu de dé est-il équitable ? | trois règles (dont diviseurs de 10) ; équitable ≠ 1/2 ; échelle ; fréquence sur 40 parties |

Progression 3 Découverte / 3 Entraînement / 2 Problème / 2 Synthèse. Les 10 exercices sont **réécrits de zéro** (niveau manuel de 5e, 5 ou 6 questions), tous les titres changés. Chaque corrigé : une méthode et un résultat encadré par question, étapes détaillées, au moins une « Erreur fréquente » ou « À retenir ». `Solution:` courte.

### Exercices retirés (11)
- 3097, 3099, 3085, 3090 : copies de « Un tirage dans le sac » (mêmes six questions, seule la composition changeait) ; urne reprise par 3083, sacs comparés par 3101.
- 3086 : copie de « Un dé équilibré et une affirmation » (3084 gardé et refait).
- 3093, 3098, 3091, 3095, 3088, 3100 : copies de « Un dé équilibré : … » (seul l'événement changeait ; elles reposaient sur l'événement contraire, programme de 4e) ; reprises par 3084 et 3102.

### Figures (28 neuves pour 31 emplacements, style des livres, `figures/figures.py`)
- Moteurs repris de la 281 (4e) et adaptés : boules / jetons et urnes, faces de dé, roues (rayons de partage en pointillés), cartes, échelle des probabilités, courbes de fréquences (simulations à graine fixe), diagramme en barres.
- Cours (6) : cartes impaires en vert, échelle avec les mots, sac de jetons, roue partagée en 6 secteurs de 60°, échelle du sac, courbe de 1 000 tirages. Fiche : 2 figures du cours.
- Énoncés sans la réponse : dé (3084, 3102), urne + échelle vide (3087), urne (3083), 12 cartes (3096), deux roues (3103), trois sacs (3101), courbes des deux dés (3094), roue de 12 (3092).
- Corrigés, réponse en vert : faces favorables à A, B, C (3084), échelle placée (3087), boules rouges entourées (3083), cartes de A et de C (3096), secteurs rouges entourés et roue 2 en quarts (3103), barres 20 / 500 lancers avec la probabilité 0,5 (3089), jetons gagnants entourés (3101), courbes avec la droite 1/6 (3094), secteurs 4, 8, 12 et échelle des stands (3092), faces de Zoé (vert) et de Yanis (orange), deux échelles (3102).
- Les 4 anciennes images en ligne (roues de 3087 et 3103) ne sont plus appelées : supprimées à l'import ; aucune conservée.
- `figures_livre.py` : 28/28, 0 texte sur un trait, aucune tolérance, toutes ≤ 900 px. Chaque PNG regardé ; corrigé après relecture : étiquettes posées sur les aplats colorés des roues et des barres (refusées par le contrôle) placées à l'extérieur ; échelles et courbes rétrécies pour rester lisibles sur téléphone ; « vert » de l'échelle du sac remonté d'un niveau.

### Contrôles
- `verif_279.py` : **247 contrôles justes, 0 faux** (sympy `Rational`, chaque probabilité recalculée par dénombrement exhaustif des issues ; écritures décimales, arrondis et pourcentages ; équations des sacs résolues ; tableau des dés de 3094 = simulation de `figures.py`, 4 six dans les 12 premiers lancers de Malik, stabilisation des courbes ; données des figures ; structure : questions = étapes = solutions, une méthode et un résultat par question, images appelées = déclarées, 10 + 11 = 21 Id, progression, ni « brevet », ni « contraire », ni « premier »).
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`279_validation.log` ; 31 emplacements de figures neuves, 0 image en ligne conservée ; notes : 10 titres changés et 11 retraits, voulus).
- `controle_apercu.mjs` : « Aucun problème détecté », 64 vues téléphone et ordinateur (`279_captures.log`, captures dans `captures_refonte/`).
- Captures téléphone regardées en deux passes (cours entier, fiche, énoncés 3084 et 3087, corrigés 3103, 3094, 3102 puis 3092). Corrigé après la 1re passe : 17 formules en chaîne trop longues (coupées ou réduites) découpées sur deux lignes alignées ; deux tableaux du cours trop larges (« En % », colonne « Total » retirée) ; deux formules encadrées de la fiche raccourcies.

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 279`, lancer `retirer_exercices.py` (11 Id).

---

## Historique : révision du 30 octobre 2026

21 blocs et leurs identifiants conservés, 114 questions corrigées, 6 exercices remplacés ; audit exact (370 assertions), 4 figures, 65 vues mobiles et 65 vues ordinateur sans anomalie. Le détail complet est dans `sauvegardes/avant_refonte_20261104/RAPPORT.md`.
