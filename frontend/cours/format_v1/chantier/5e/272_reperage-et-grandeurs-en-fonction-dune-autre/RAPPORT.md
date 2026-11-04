# Notion 272 — Repérage et grandeurs en fonction d'une autre (5e)

## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-10-exercices-272). Référence : `source_en_ligne/` (ré-export du 04/11, même contenu que l'import du 30/10). 10 exercices gardés, 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde des fichiers finaux et des figures d'avant la refonte : `sauvegardes/avant_refonte_20261104/`.

Programme vérifié : programme de 5e du BO n° 10 du 5 mars 2026 (rentrée 2026) — « en fonction de », formule, tableau de valeurs, graphique cartésien, lien avec la proportionnalité, tableur. Pas de notation $f(x)$ ni de fonction affine (3e). Le repère du plan est traité dans la notion 263 : ici, seul un rappel d'une phrase (coordonnées « valeur de départ ; valeur obtenue »). Aucune mention du brevet.

### Cours et fiche
- **Cours 267 réécrit** (titre inchangé) : I. une grandeur en fonction d'une autre (définition, grandeur de départ, trois représentations, ressort $L = 12 + 3m$ de la formule au tableau) ; II. lire un graphique (axes et graduations, lire une valeur, chercher pour quelle valeur — plusieurs réponses —, variations, maximum, minimum, sur l'exemple d'un ascenseur panoramique) ; III. construire un graphique (méthode, relier ou non) ; IV. tableur (formule, recopie, nuage de points) ; V. graphique et proportionnalité ; erreurs fréquentes ; à retenir. Ancien cours centré sur le repère (doublon de 263) remplacé.
- **Fiche 187 refaite** : les cinq parties en résumé, 2 figures, 5 erreurs classiques.
- Exemples du cours (ressort, ascenseur, pommes) différents de ceux des exercices.

### Exercices gardés (10) — tous réécrits entièrement
| Id | Titre | Capacités |
|---|---|---|
| 2940 | Découverte - Le remplissage d'une cuve | « en fonction de », graduations différentes, lecture, lecture inverse, graphique → tableau, proportionnalité |
| 2938 | Découverte - Les températures d'une journée | lecture, deux antécédents, maximum / minimum, variations, écart, estimation entre deux relevés |
| 2937 | Découverte - Le prix d'un parc de loisirs | formule $P = 3 + 2n$ → tableau → points dans un repère vide, ne pas relier, budget |
| 2946 | Entraînement - L'aire d'un carré en fonction de son côté | tableau → courbe, lectures approchées (2,5 cm ; 20 cm²), non-proportionnalité (×4) |
| 2949 | Entraînement - La sortie à vélo de Lou | distance parcourue en fonction du temps : lectures, pause, comparer deux allures |
| 2944 | Entraînement - Le périmètre d'un rectangle avec un tableur | $P = 2L + 6$, formule `=2*A2+6`, recopie, nuage de points aligné mais pas par l'origine |
| 2954 | Problème - Choisir une location de kayak | deux droites, identification, proportionnalité, intersection (5 h ; 30 €), budget, règle de choix |
| 2956 | Problème - Le trajet de Tom pour aller au collège | associer 4 situations / 4 graphiques, distance à la maison, trois instants à 200 m, distance totale |
| 2945 | Synthèse - La bougie qui se consume | construire, lire, formule $h = 15 - 2t$, tableur et résultat $-1$ sans sens, non-proportionnalité |
| 2952 | Synthèse - Une randonnée en montagne | profil (axe qui commence à 1 100 m), sommet, variations, deux lectures à 1 600 m, $D = 20d$, heure d'arrivée |

Progression : 3 Découverte, 3 Entraînement, 2 Problème, 2 Synthèse. Chaque corrigé : méthode, étapes détaillées, résultat encadré, erreur fréquente ou à retenir ; `Solution:` courte. Couverture détaillée par capacité : `COUVERTURE.md`.

### Exercices retirés (11)
- 2936, 2942, 2943, 2947, 2950 : le même exercice « jardin rectangulaire dans un repère » (6 questions identiques) répété avec d'autres nombres ; c'est le repère du plan, déjà traité dans 263. (Les Id 2945 et 2952 de cette série sont réutilisés pour les deux synthèses.)
- 2939, 2941, 2948, 2951, 2953, 2955 : le même exercice « tarif : entrée + prix par activité » que 2937, avec d'autres nombres.

### Figures (29 neuves, style livre, `figures/figures.py`)
- Toutes les anciennes images (16) supprimées du dossier (copie dans la sauvegarde) ; à l'import, les images en ligne non appelées sont supprimées.
- Cours (4) : ascenseur avec lectures en vert, graphique du ressort, tableur, deux graphiques « proportionnelles / non proportionnelles » ; fiche (2, reprises du cours).
- Exercices : courbe seule ou repère vide dans l'énoncé, lectures en vert avec pointillés vers les axes dans le corrigé (2940, 2938, 2937, 2946, 2949, 2954, 2956 trajet, 2945, 2952) ; tableurs énoncé / corrigé (2944, 2945) ; nuage de points du tableur (2944) ; 4 petits graphiques à associer, énoncé / corrigé (2956).
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance, toutes ≤ 900 px. Après les captures : les figures des corrigés sont placées entre les encadrés (pleine largeur sur téléphone).

### Contrôles
- `verif_272.py` : **268 contrôles** sympy, 0 échec (`272_verif_math.log`) : chaque réponse ; chaque figure confrontée aux valeurs de l'énoncé (données `DONNEES`, formules et lectures du code TikZ : lignes brisées interpolées exactement, antécédents, intersections, $\sqrt{20}$) ; structure de chaque corrigé ; 10 Id + 11 retirés = les 21 Id d'origine ; absence du mot « brevet ».
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`272_validation.log`). `controle_apercu.mjs` : 64 vues sur 64 sans problème, téléphone et ordinateur (`272_captures.log`, `captures_refonte/`).
- Captures téléphone regardées en deux passes : cours (4 écrans), fiche (2), exercices 2940, 2937, 2944, 2954, 2956, 2945, 2952. Corrigé après la 1re passe : figures sorties des étapes (réduites sur téléphone), calcul sur deux colonnes du 2944 mis sur une colonne, tableaux larges des corrigés 2937 (passé à la verticale) et 2940 (sorti de l'encadré) qui défilaient.

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 272`, lancer `retirer_exercices.py` (11 Id).
- L'ancien script `verif_notion.py` (révision du 30/10) vérifiait l'ancien contenu : il est remplacé par `verif_272.py`.

---

## Historique : révision du 30 octobre 2026

État : prêt — révision pédagogique contrôlée le 30 octobre 2026.

21 blocs et leurs identifiants conservés, 105 questions corrigées. 7 exercices remplacés pour diversifier les méthodes ; 0 doublons exacts supplémentaires corrigés. Les titres et les difficultés correspondent aux démarches : 9 découvertes, 10 entraînements, 2 problèmes. Couverture et Id détaillés dans COUVERTURE.md.

Format : même moteur et même syntaxe optitab:1 que la Terminale. Objectifs, sections romaines, propriétés, méthodes courtes, exemples, points d’attention et récapitulation ; fiche synthétique et corrigés question par question. Les constructions ou lectures de graphiques disposent de figures de correction. Les variantes numériques conservées ne sont plus artificiellement classées comme problèmes.

Modifications :

| Id conservé | Travail proposé | Niveau |
|---|---|---|
| 2938 | Placer des points sur les axes | easy |
| 2940 | Lire des graduations différentes | easy |
| 2944 | Un périmètre dépend d’une longueur | medium |
| 2946 | Une aire n’est pas un périmètre | medium |
| 2949 | Une promenade avec une pause | medium |
| 2954 | Comparer deux tarifs sur un graphique | hard |
| 2956 | Retrouver une donnée avec un budget | hard |

Mathématiques : 232 assertions de l’audit exact OK sur les fichiers finaux ; Id, calculs, conversions et contraintes contrôlés selon la notion. Les propriétés et les arguments qualitatifs ont été relus avec les énoncés et les figures. Preuves : revision_maths_coordination.log, controle_maths_coordination.json, resultat_verification.json ; moteur conservé dans verif_notion.py.

Figures : 15 PNG actifs, sources TikZ et productions précédentes conservées. Toutes les figures actives ont été regardées sur les planches ou individuellement. Compilation et contrôle texte/traits : OK, aucune tolérance ajoutée. Les graduations d’axes emploient le fond blanc autorisé par le guide ; leur ordre de dessin a été corrigé pour éviter que les courbes ou les côtés traversent les chiffres. Les lettres des points restent hors des traits. Preuve : compilation_figures.json.

Rendu final : vérificateur courant et audit renforcé des erreurs MathJax HTML/SVG ; 65 vues mobiles à 390 px et les mêmes 65 vues à 1 280 px, zéro anomalie restante. Absence de caractères de contrôle C0 interdits vérifiée. Journaux : revision_validation.log et revision_navigateur.log ; statut : controles_revision_20261030.json. Les tableaux trop larges des cours ont été compactés quand nécessaire.

Relecture : cours mobile intégral, fiche et exercices 3, 9, 19, 21, énoncés et étapes, regardés dans les captures finales. Preuves : captures_revision_20261030/relecture_documents.png et relecture_revision_1.png, relecture_revision_2.png ; relecture_visuelle_coordination.json.

Outil : copie locale des audits communs, détection MathJax élargie et attente de fermeture Chrome bornée à deux secondes pour le défaut de nettoyage Windows déjà établi. Les audits ne sont pas allégés. Aucun outil commun ou fichier frontend/src modifié.

Sauvegarde antérieure dans sauvegardes/revision_2026-10-30/. Sources exportées conservées, aucun accès ou import en base. Travail limité à la classe de 5e ; programme rentrée 2026 vérifié par la coordination.
