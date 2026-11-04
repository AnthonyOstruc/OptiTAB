# Notion 273 — Angles et droites parallèles (5e)

## Refonte 10 exercices 2026-11-04

**État : prêt** (agent-273-refonte-10ex). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés et réécrits entièrement, 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde des fichiers finaux et des figures d'avant la refonte : `sauvegardes/avant_refonte_20261104/`.

### Programme (attendus de 5e)
Vocabulaire (adjacents, complémentaires, supplémentaires, opposés par le sommet), angles alternes-internes et correspondants, propriété directe (parallèles → angles égaux) et réciproque (angles égaux → parallèles), démontrer qu'il n'y a pas parallélisme, rédaction « On sait que… Or… Donc… », rapporteur (mesurer, construire un angle, construire une parallèle). La bissectrice (construction de 6e) n'est plus travaillée ici ; la somme des angles du triangle reste à la notion 274 (2971 l'annonce seulement). Aucune mention du brevet. Couverture détaillée : `COUVERTURE.md`.

### Cours et fiche
- **Cours 268 réécrit façon manuel** (titre inchangé) : I. nommer et mesurer un angle (tableau aigu / droit / obtus / plat, méthodes « mesurer » et « construire » au rapporteur, piège des deux graduations) ; II. adjacents, complémentaires, supplémentaires (définitions, propriété, erreurs) ; III. opposés par le sommet (propriété + démonstration courte par les angles supplémentaires) ; IV. sécante : alternes-internes et correspondants (positions, même sans parallèles) ; V. propriété et réciproque, méthode de rédaction, 3 exemples (calculer, démontrer un parallélisme, démontrer un non-parallélisme), construire une parallèle au rapporteur ; erreurs fréquentes ; à retenir. Exemples du cours (128°, 40°, 28°/62°/152°, 50°/130°, 75°/78°, 60°) différents de ceux des exercices.
- **Fiche 188 refaite** : tableau du vocabulaire, sécante, propriété et réciproque, rédaction, rapporteur, 5 erreurs classiques ; 2 figures.

### Exercices gardés (10)
| Id | Titre | Capacités |
|---|---|---|
| 2959 | Découverte - Adjacents, complémentaires, supplémentaires | reconnaître des adjacents (et un contre-exemple), 56° complémentaire, 146° supplémentaire, complément / supplément de 72°, vrai-faux |
| 2957 | Découverte - Angles opposés par le sommet | angle opposé, rédaction « On sait que… Or… Donc… », 38° / 142°, tour complet, cas des droites perpendiculaires |
| 2958 | Découverte - Reconnaître des angles alternes-internes et correspondants | 8 angles numérotés, droites NON parallèles : internes, 2 paires alternes-internes, 4 paires correspondants, opposés, mesures 64° / 52° inégales |
| 2962 | Entraînement - Calculer des angles avec des droites parallèles | huit angles nommés par des points (62° / 118°), alternes-internes et correspondants rédigés, tableau |
| 2961 | Entraînement - Démontrer que deux droites sont parallèles ou non | réciproque (58° = 58°), non-parallélisme (73° ≠ 75°), « ça se voit » réfuté |
| 2960 | Entraînement - Mesurer au rapporteur et construire une parallèle | lire un rapporteur à deux graduations (33°, piège 147°), construire la parallèle en reportant 70°, justifier, 110° |
| 2974 | Problème - Une somme d'angles qui prouve un parallélisme | angles intérieurs du même côté 112° / 68°, passage par le supplémentaire, cas 70°, règle « somme 180° » |
| 2965 | Problème - La rampe d'escalier | poteaux parallèles par angles droits correspondants, 56°, 124°, horizontale et angle complémentaire 34° |
| 2971 | Problème - Une parallèle à un côté du triangle | deux paires d'alternes-internes (48°, 67°), angle plat, 65°, somme 180° |
| 2972 | Synthèse - Un point entre deux droites parallèles | parallèle auxiliaire, deux fois les alternes-internes, 73°, supplémentaire 107°, complémentaire 48° |

Progression : 3 Découverte, 3 Entraînement, 3 Problème, 1 Synthèse. Chaque corrigé : méthode, étapes détaillées (On sait que / Or / Donc), un résultat encadré par question, erreur fréquente ; `Solution:` courte et numérotée.

### Exercices retirés (11)
- 2963, 2964, 2966, 2968, 2970, 2973, 2975 : sept copies de « Sécantes et bissectrice » (même énoncé, six questions identiques, seul l'angle changeait) ; remplacées par 2957 et 2959.
- 2969, 2976 : copies de « Parallèles et sécante » ; remplacées par 2962.
- 2977 (construire une bissectrice au compas) : construction de 6e, hors des capacités du chapitre ; le rapporteur est travaillé dans 2960.
- 2967 (égalité et parallélisme, sans figure) : repris en mieux par 2961 et 2958.

### Figures (29 neuves, style livre, `figures/figures.py`)
- Les 28 anciennes images du dossier sont supprimées (copie dans la sauvegarde) ; à l'import, les 10 images en ligne non appelées sont supprimées.
- Cours (6) : rapporteur à deux graduations, adjacents / complémentaires / supplémentaires, opposés par le sommet, alternes-internes (bande intérieure colorée) et correspondants sur des droites non parallèles, parallèles avec les huit angles (50° orange, 130° bleu), construction d'une parallèle ; fiche (2, reprises du cours).
- Exercices : énoncé (données en orange) + corrigé (angles trouvés ou égaux en vert) pour chacun ; 2958 a deux corrigés (paires alternes-internes en 2 couleurs, paires correspondantes en 4 couleurs) ; 2960 a quatre figures (rapporteur énoncé / corrigé, construction énoncé / corrigé) ; 2961 : angles inégaux en rouge.
- Rapporteur dessiné degré par degré, nombres de 20 en 20 (lisibles sur téléphone), demi-droites placées entre les nombres.
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance ; toutes ≤ 764 px.

### Contrôles
- `verif_273.py` : **475 contrôles** sympy, 0 erreur (`273_verif_math.log`) : 74 arcs de figures recalculés à partir des points dessinés (chaque mesure écrite sur une figure = angle réellement dessiné) ; droites parallèles / non parallèles ; positions alternes-internes, correspondants, opposés reconnues géométriquement (2958, 2962, 2961, 2974, 2965, cours) ; chaque calcul ; 37 égalités numériques des textes et 71 mesures $\widehat{XYZ}$ comparées à la figure de leur exercice ; structure (10 + 11 = 21 Id, progression, difficultés, un résultat par question, erreur fréquente, solution complète, figure dans l'énoncé et le corrigé, images déclarées) ; aucune mention du brevet.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`273_validation.log`). `controle_apercu.mjs` : 64 vues sans problème, téléphone et ordinateur (`273_captures.log`, `captures_refonte/`).
- Captures téléphone regardées en deux passes (planches `captures_refonte/273_planche_*.png`) : cours entier, fiche, exercices 2959, 2957, 2958, 2962, 2961, 2960, 2974, 2965, 2971, 2972. Corrigé après la 1re passe : deux chaînes de calcul réduites sur téléphone (2971 Q4, 2972 Q4) découpées.

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 273`, lancer `retirer_exercices.py` (11 Id).
- `verif_notion.py` (audit du 30/10) est obsolète : il porte sur l'ancienne version ; le contrôle actuel est `verif_273.py`.

---

## Historique : révision du 30 octobre 2026

État : prêt — révision pédagogique contrôlée le 30 octobre 2026.

21 blocs et leurs identifiants conservés, 102 questions corrigées. 8 exercices remplacés pour diversifier les méthodes ; 0 doublons exacts supplémentaires corrigés. Les titres et les difficultés correspondent aux démarches : 9 découvertes, 9 entraînements, 3 problèmes. Couverture et Id détaillés dans COUVERTURE.md.

Format : même moteur et même syntaxe optitab:1 que la Terminale. Objectifs, sections romaines, propriétés, méthodes courtes, exemples, points d’attention et récapitulation ; fiche synthétique et corrigés question par question. Les constructions ou lectures de graphiques disposent de figures de correction. Les variantes numériques conservées ne sont plus artificiellement classées comme problèmes.

Modifications :

| Id conservé | Travail proposé | Niveau |
|---|---|---|
| 2959 | Partager un angle droit | easy |
| 2961 | Prouver que deux droites sont parallèles | medium |
| 2965 | Deux perpendiculaires à une même droite | medium |
| 2967 | Ne pas confondre égalité et parallélisme | medium |
| 2971 | Une droite parallèle à la base d’un triangle | hard |
| 2972 | Deux bissectrices et un angle droit | hard |
| 2974 | Une somme d’angles qui prouve un parallélisme | hard |
| 2977 | Construire une bissectrice au compas | medium |

Mathématiques : 232 assertions de l’audit exact OK sur les fichiers finaux ; Id, calculs, conversions et contraintes contrôlés selon la notion. Les propriétés et les arguments qualitatifs ont été relus avec les énoncés et les figures. Preuves : revision_maths_coordination.log, controle_maths_coordination.json, resultat_verification.json ; moteur conservé dans verif_notion.py.

Figures : 26 PNG actifs, sources TikZ et productions précédentes conservées. Toutes les figures actives ont été regardées sur les planches ou individuellement. Compilation et contrôle texte/traits : OK, aucune tolérance ajoutée. Les graduations d’axes emploient le fond blanc autorisé par le guide ; leur ordre de dessin a été corrigé pour éviter que les courbes ou les côtés traversent les chiffres. Les lettres des points restent hors des traits. Preuve : compilation_figures.json.

Rendu final : vérificateur courant et audit renforcé des erreurs MathJax HTML/SVG ; 65 vues mobiles à 390 px et les mêmes 65 vues à 1 280 px, zéro anomalie restante. Absence de caractères de contrôle C0 interdits vérifiée. Journaux : revision_validation.log et revision_navigateur.log ; statut : controles_revision_20261030.json. Les tableaux trop larges des cours ont été compactés quand nécessaire.

Relecture : cours mobile intégral, fiche et exercices 3, 5, 15, 18, énoncés et étapes, regardés dans les captures finales. Preuves : captures_revision_20261030/relecture_documents.png et relecture_revision_1.png, relecture_revision_2.png ; relecture_visuelle_coordination.json.

Outil : copie locale des audits communs, détection MathJax élargie et attente de fermeture Chrome bornée à deux secondes pour le défaut de nettoyage Windows déjà établi. Les audits ne sont pas allégés. Aucun outil commun ou fichier frontend/src modifié.

Sauvegarde antérieure dans sauvegardes/revision_2026-10-30/. Sources exportées conservées, aucun accès ou import en base. Travail limité à la classe de 5e ; programme rentrée 2026 vérifié par la coordination.
