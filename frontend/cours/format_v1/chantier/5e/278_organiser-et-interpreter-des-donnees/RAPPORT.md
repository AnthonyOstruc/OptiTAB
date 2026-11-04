# Notion 278 (5e) — Organiser et interpréter des données

## Refonte 10 exercices 2026-11-04

**État : prêt.** Cours, fiche, 10 exercices et 24 figures refaits de zéro au niveau des notions de 3e/4e. Référence : `source_en_ligne/` (ré-export du 04/11). Aucune écriture en base, aucun git, aucune ligne `Id:` modifiée, aucun `nouveau-N`. Sauvegarde des fichiers et figures d'avant la refonte : `sauvegardes/avant_refonte_20261104/`.

### Programme
Programme de 5e du BO du 5 mars 2026 (texte officiel lu : annexe 2, cycle 4, « Cinquième — Statistiques ») : recueillir et organiser des données ; effectifs et fréquences (fraction, décimal, pourcentage) ; lire et interpréter tableaux, diagrammes, graphiques ; représenter (papier ou tableur-grapheur) par un tableau, un diagramme en barres, un diagramme circulaire ou un graphique cartésien ; choisir une représentation adaptée ; moyenne simple ; prolongement : diagrammes de Florence Nightingale.
- **Médiane, étendue, moyenne pondérée** : programme de 4e → absentes (le vérificateur interdit ces mots).
- **Histogramme** : ne figure pas dans le programme 2026 de 5e → non traité (à signaler au propriétaire, qui le citait « en principe »).
- **Semi-circulaire** : variante du diagramme circulaire, traitée (cours + 3073).
- Aucune mention du brevet. Couverture détaillée : `COUVERTURE.md`.

### Cours (Id 273) et fiche (Id 193)
- **Cours réécrit** : objectifs ; I. recueillir et organiser (vocabulaire population / individu / caractère qualitatif-quantitatif / effectif, méthode de dépouillement par bâtonnets) ; II. effectifs et fréquences (3 écritures, passage au pourcentage, propriétés, erreur effectif/fréquence) ; III. représenter (barres et bâtons, circulaire et semi-circulaire avec tableau des angles, graphique cartésien, choisir une représentation, graphique trompeur, tableur-grapheur) ; IV. moyenne (définition, moyenne non observée, interprétation « partage égal », total = moyenne × nombre, erreurs, tableur, remarque historique) ; à retenir. Exemples : boissons, buts de football, club de judo, colis — tous différents des exercices.
- **Fiche refaite** : 4 parties, 2 formules encadrées, tableau « quel diagramme pour quoi », 1 figure, 5 erreurs classiques.

### Les 10 exercices gardés (3 Découverte, 3 Entraînement, 2 Problème, 2 Synthèse) — tous réécrits
| Id | Titre | Contenu |
|---|---|---|
| 3062 | Découverte - Dépouiller une enquête | 24 réponses brutes (fruits) → tableau d'effectifs par bâtonnets, population/caractère qualitatif, « plus d'un tiers » |
| 3071 | Découverte - Calculer des fréquences | 40 élèves, fréquence en fraction/décimal/%, somme 100 %, regrouper deux catégories, 40 % de 25, effectif ≠ proportion |
| 3066 | Découverte - Lire un diagramme en barres | CDI : lecture (pas de 3), extrêmes, total 60, fréquence 1/4, « plus de la moitié » (exactement la moitié) |
| 3063 | Entraînement - Construire un diagramme en bâtons | animaux de compagnie (quantitatif), construction, « au moins 2 » (32 %), « au plus 1 » (68 %) |
| 3073 | Entraînement - Construire un diagramme circulaire et semi-circulaire | transports : %, 9° par élève, 90/162/108°, quart de disque, semi-circulaire 45/81/54° |
| 3072 | Entraînement - Calculer et interpréter une moyenne | notes de Yanis (12), comparaison avec Inès (même moyenne, régularité), note à obtenir (18), `=MOYENNE(B2:F2)` |
| 3075 | Problème - La fréquentation de la piscine | graphique cartésien : lectures (pas de 200), évolution, moyenne 1 500, mois au-dessus, « trois fois plus », choix du graphique |
| 3065 | Problème - Les ventes de gâteaux au tableur | `=SOMME(B2:B6)`, `=B2/B7`, piège de la recopie, format %, `=MOYENNE(B2:B6)`, choisir barres ou secteurs |
| 3064 | Synthèse - Le vote pour la sortie de fin d'année | dépouillement de 30 bulletins, fréquences, majorité, diagramme circulaire, comparaison de deux classes (fréquences) |
| 3082 | Synthèse - Le diagramme trompeur de la cantine | axe commençant à 270, titre « six fois plus » faux, moyenne 300, 27,5 %, diagramme honnête, choix du graphique |

Chaque corrigé : une méthode et un résultat encadré par question, étapes détaillées, erreur fréquente (ou « à retenir ») ; `Solution:` courte et complète. Ids réutilisés pour des exercices refaits de zéro : 3062, 3063, 3064, 3065, 3071, 3072 (anciennes copies « trajets » / « suivi des lectures ») et 3082 (ancien « Réunir deux classes », de niveau 4e).

### Exercices retirés (11) — `exercices_retires.txt`
- 3067, 3070, 3074, 3077, 3079, 3081 : copies de « Le suivi des lectures » (mêmes six questions, autres nombres).
- 3069, 3076, 3078 : copies de « L'enquête sur les trajets ».
- 3068 « Deux séries de même moyenne » : idée reprise dans 3072 (Yanis / Inès).
- 3080 « Exploiter des données regroupées » : moyenne d'un tableau d'effectifs = moyenne pondérée, programme de 4e.

### Figures (24 neuves, style livre, `figures/figures.py`)
- Les 7 anciennes images (matplotlib, alt génériques) sont remplacées ; aucune image en ligne conservée (copie dans la sauvegarde).
- Cours (7) : dépouillement par bâtonnets, diagramme en barres, diagramme en bâtons, circulaire, semi-circulaire, graphique cartésien, feuille de tableur. Fiche (1) : le diagramme circulaire du cours.
- Exercices (17) : énoncé = données seules (3066 barres, 3075 courbe, 3065 tableur + deux graphiques du grapheur, 3082 diagramme trompeur) ; corrigé = construction ou lecture en vert (3062 et 3071 dépouillement / barre des 100 %, 3066 valeurs lues, 3063 bâtons, 3073 circulaire et semi-circulaire, 3072 notes et moyenne, 3075 lectures et moyenne, 3065 tableur complété, 3064 circulaire et barres des deux classes, 3082 diagramme honnête).
- Les données des figures (`DONNEES`) sont relues par `verif_278.py`. `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance ; toutes ≤ 828 px.
- Tableaux de données : vrais tableaux, présentés en colonnes étroites (2 ou 3 colonnes) pour le téléphone.

### Contrôles
- `verif_278.py` : **312 contrôles** sympy exacts, 0 erreur (`278_verif_math.log`) — chaque réponse ; dépouillements recomptés depuis les relevés bruts ; angles, fréquences, moyennes, lectures confrontés aux données des figures ; **138 égalités numériques** des textes recalculées automatiquement (détection d'une erreur volontaire testée) ; structure (10 exercices, progression, méthode et résultat par question, solution complète, Id 3062 à 3082 tous gardés ou retirés) ; absence de « brevet », « médiane », « étendue », « pondérée », « histogramme ».
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`278_validation.log`). `controle_apercu.mjs` : **64 vues sur 64** sans problème, téléphone et ordinateur (`278_captures.log`, `captures_refonte/`).
- Captures téléphone regardées en deux passes groupées (`captures_refonte/planches/`, `planches2/`) : cours entier, fiche, les 10 exercices. Corrigé après la 1re passe : formule « total = moyenne × nombre » trop réduite (mise en texte), fractions en ligne qui se chevauchaient (mises en formule centrée), feuille de tableur de 3065 passée en colonnes (trop large), barre des pourcentages de 3071 et figures larges resserrées, somme de 3075 coupée en lignes, tableau de la fiche simplifié.

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 278`, lancer `retirer_exercices.py` (11 Id).
- Histogramme : absent du programme 2026 de 5e, donc non traité ; si le propriétaire le veut quand même, il faudrait un exercice « Pour aller plus loin ».

---

## Historique : révision du 30 octobre 2026

État : prêt — révision pédagogique contrôlée le 30 octobre 2026.

21 blocs et leurs identifiants conservés, 114 questions corrigées. 6 exercices remplacés pour diversifier les méthodes ; 2 doublons exacts supplémentaires corrigés. Les titres et les difficultés correspondent aux démarches : 17 découvertes, 2 entraînements, 2 problèmes. Couverture et Id détaillés dans COUVERTURE.md.

Format : même moteur et même syntaxe optitab:1 que la Terminale. Objectifs, sections romaines, propriétés, méthodes courtes, exemples, points d’attention et récapitulation ; fiche synthétique et corrigés question par question. Les constructions ou lectures de graphiques disposent de figures de correction. Les variantes numériques conservées ne sont plus artificiellement classées comme problèmes.

Modifications :

| Id conservé | Travail proposé | Niveau |
|---|---|---|
| 3066 | Lire les emprunts à la bibliothèque | easy |
| 3068 | Deux séries de même moyenne | easy |
| 3073 | Construire un diagramme circulaire | medium |
| 3075 | Suivre une température | medium |
| 3080 | Exploiter des données regroupées | hard |
| 3082 | Réunir deux classes | hard |
| 3069 | Répartition des trajets distincte ; tableaux, étapes et réponses recalculés. | easy |
| 3076 | Répartition des trajets distincte ; tableaux, étapes et réponses recalculés. | easy |

Mathématiques : 444 assertions de l’audit exact OK sur les fichiers finaux ; Id, calculs, conversions et contraintes contrôlés selon la notion. Les propriétés et les arguments qualitatifs ont été relus avec les énoncés et les figures. Preuves : revision_maths_coordination.log, controle_maths_coordination.json, verification_maths.json ; moteur conservé dans la notion 276/verif_notion.py (et correction reportée dans 279/verif_notion.py).

Figures : 7 PNG actifs, sources TikZ et productions précédentes conservées. Toutes les figures actives ont été regardées sur les planches ou individuellement. Compilation et contrôle texte/traits : OK, aucune tolérance ajoutée. Les graduations d’axes emploient le fond blanc autorisé par le guide ; leur ordre de dessin a été corrigé pour éviter que les courbes ou les côtés traversent les chiffres. Les lettres des points restent hors des traits. Preuve : compilation_figures.json.

Rendu final : vérificateur courant et audit renforcé des erreurs MathJax HTML/SVG ; 65 vues mobiles à 390 px et les mêmes 65 vues à 1 280 px, zéro anomalie restante. Absence de caractères de contrôle C0 interdits vérifiée. Journaux : revision_validation.log et revision_navigateur.log ; statut : controles_revision_20261030.json. Les tableaux trop larges des cours ont été compactés quand nécessaire.

Relecture : cours mobile intégral, fiche et exercices 5, 12, 19, 21, énoncés et étapes, regardés dans les captures finales. Preuves : captures_revision_20261030/relecture_documents.png et relecture_revision_1.png, relecture_revision_2.png ; relecture_visuelle_coordination.json.

Outil : copie locale des audits communs, détection MathJax élargie et attente de fermeture Chrome bornée à deux secondes pour le défaut de nettoyage Windows déjà établi. Les audits ne sont pas allégés. Aucun outil commun ou fichier frontend/src modifié.

Sauvegarde antérieure dans sauvegardes/revision_2026-10-30/. Sources exportées conservées, aucun accès ou import en base. Travail limité à la classe de 5e ; programme rentrée 2026 vérifié par la coordination.
