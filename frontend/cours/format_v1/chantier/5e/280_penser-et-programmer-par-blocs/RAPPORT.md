# Notion 280 (5e) : Penser et programmer par blocs

## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-10-exercices-280). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés et réécrits entièrement (même Id, nouveaux titres), 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde de l'état d'avant (textes, figures, build) : `sauvegardes/avant_refonte_20261104/`.

### Programme
Programme de 5e (cycle 4, programme du BO du 5 mars 2026, en vigueur en 5e depuis la rentrée 2026 : « pensée informatique » = instructions simples, programme simple, formules, boucle inconditionnelle simple, variables introduites progressivement ; et repères du programme 2020 : événements, variables, boucles, conditions). Contenu : séquences d'instructions, lire et exécuter un script (tableau d'exécution), variables, entrée / sortie, programmes de calcul et blocs emboîtés, déplacements du lutin et stylo, « répéter n fois », « si … alors » simple (sans « sinon », sans condition composée), événements (drapeau, touches). Pas de boucle « répéter jusqu'à », de bloc personnalisé ni de message entre lutins (4e). Aucune mention du brevet.

### Cours et fiche
- **Cours 275 réécrit façon manuel** (titre inchangé) : objectifs, prérequis ; I. programme, script et blocs (familles de couleurs, méthode « exécuter à la main ») ; II. variables, entrée / sortie, programme de calcul avec tableau d'exécution, « mettre » / « ajouter », blocs opérateurs emboîtés ; III. scène, orientation, blocs de mouvement et de stylo, exemple « lettre L » avec tableau ; IV. boucle « répéter n fois » (carré de 60, tableau des tours), polygone régulier ($360 \div n$), angle de rotation / angle intérieur ; V. « si … alors », valeur frontière ; VI. événements ; À retenir. Exemples différents des exercices.
- **Fiche 195 refaite** : script et variables (tableau d'exécution), lutin et stylo (scène + tableau des blocs), boucles et conditions, 5 erreurs classiques.

### Exercices gardés (10)
| Id | Titre | Capacités |
|---|---|---|
| 3104 | Découverte - Exécuter un programme de calcul | drapeau, demander / réponse, variables, tableau d'exécution, $4x + 6$, remonter le calcul, « mettre » / « ajouter » |
| 3105 | Découverte - Tracer un carré avec une boucle | blocs d'initialisation, « répéter 4 fois », positions et orientations par tour, périmètre, rôle du stylo |
| 3110 | Découverte - Compléter une suite de déplacements | séquence d'instructions, script à trous (A–D), rectangle, tableau bloc par bloc, réécriture avec une boucle |
| 3108 | Entraînement - Des blocs opérateurs emboîtés | priorités / emboîtement, $(n \times 4) + 3$ et $4(n + 3)$, écart de 9, bloc à glisser dans un trou |
| 3117 | Entraînement - Polygones réguliers : choisir l'angle | boucle, angle de rotation ($360 \div n$), triangle équilatéral corrigé, hexagone à trous |
| 3106 | Entraînement - Une condition : le tarif du cinéma | « si … alors », valeur frontière, modifier une condition, second test, total d'une famille |
| 3114 | Problème - Piloter le lutin au clavier | événements (touches), s'orienter / avancer, trajet, plus court retour, script « espace » |
| 3122 | Problème - Un escalier | boucle à 4 blocs, ↺ / ↻, positions par tour, scène (au plus 8 marches), variante qui trace un rectangle |
| 3115 | Synthèse - La tirelire de Lina | variables dans une boucle, tableau des 8 tours, condition frontière (> 149), $30 + 15n$, 12 semaines |
| 3124 | Synthèse - La clôture du potager | deux entrées, périmètre, dessin à l'échelle, blocs à compléter (prix, « si »), deuxième jeu de données |

Progression : 3 Découverte, 3 Entraînement, 2 Problème, 2 Synthèse. Chaque corrigé : méthode, étapes détaillées, **tableau d'exécution** pas à pas dès qu'on suit un script, résultat encadré, erreur fréquente ; `Solution:` courte.

### Exercices retirés (11)
3107, 3109, 3111, 3112, 3113, 3116, 3118, 3119, 3120, 3121, 3123 : trois énoncés recopiés avec d'autres nombres (mêmes six questions) — « lire une donnée et prévoir une sortie », « tracer un rectangle avec une boucle », « programmer le tracé d'un carré ». Les Id 3104, 3105 et 3106 (eux aussi des copies) ont été réutilisés pour le programme de calcul, le carré et la condition ; 3114 pour les événements.

### Figures (48 positions, 47 figures neuves, style livre)
- Module `figures/scratch.py` et `figures/controle_scratch.py` **copiés de la notion 4e 290 sans modification** (mêmes empreintes md5). Ajouts seulement dans `figures.py` (palette des familles, scène).
- 35 figures de **vrais blocs Scratch** : scripts des énoncés, scripts à trous (cases pointillées A, B…), corrigés avec cases complétées et blocs ajoutés ou modifiés en vert. 11 **tracés exécutés** sur le repère de la scène (tracé en vert, départ, flèche orange de l'orientation finale), tous produits par l'exécution des scripts ; 1 figure de la scène et des orientations (cours, fiche).
- Les 10 anciennes images (TikZ du 30/10) et les 7 images en ligne qui ne sont plus appelées sont remplacées (supprimées à l'import) ; 0 image en ligne conservée.
- `figures_livre.py` : 0 texte sur un trait sur les repères ; figures de blocs en `TOLERE` (texte blanc sur fond coloré) **et** contrôlées par `controle_scratch.py` : **35 figures, 0 erreur**. Largeur maximale 970 px (script 3124, < 1 100 px).

### Contrôles
- `verif_280.py` : **132 contrôles OK** (`280_verif.log`). Les **32 scripts** (cours, fiche, énoncés, variantes des corrigés) sont traduits en Python et **exécutés** ; traductions dans `programmes_280.txt`. Contrôlés : nombres dits, chaque ligne des tableaux d'exécution (variables, positions, orientations), longueurs tracées, sommets, retour au départ ; expressions par exécution symbolique sympy ($(x+5) \times 2$, $4x + 6$, $4(n+3) - (4n+3) = 9$, $(n+5) \times 2$, $2(L + \ell)$) ; équation $4x + 6 = 50$ ; écart de 9 vérifié de −5 à 20 ; valeurs frontières (12 / 13 ans, 64 / 65 ans, 150 € ; bloc placé après « dire » : faux) ; touches (trajet, retour en 4 appuis, stylo relevé) ; 8 marches sur la scène, 9 hors scène ; structure (10 exercices, progression, une méthode, un résultat et une solution par question, tableau d'exécution, erreur fréquente) ; absence du mot « brevet ».
- `verifier_notion.py --navigateur` : **OK, 0 problème** (`280_validation.log`). `controle_apercu.mjs` : **64 vues sur 64 sans défaut**, téléphone et ordinateur (`280_captures.log`, `captures_refonte/`).
- Captures téléphone regardées en deux passes : cours (5 écrans), fiche, énoncé 3104, corrigés 3105, 3110, 3108, 3117, 3106, 3114, 3122, 3115, 3124. Corrigé après la 1re passe : tableaux trop larges (3108, 3117, 3122, 3124) refaits en deux colonnes ; « $(50\ ;\ {-50})$ » (signe moins mal espacé) ; blocs ajoutés de 3124 montrés seuls (au lieu du script entier répété) et raccourcis ; calcul de 3124 Q4 mis en liste.

### Pour l'orchestrateur
- Après `publier_lot.ps1 5e 280`, lancer `retirer_exercices.py` (11 Id).
- Aucun outil commun ni fichier `frontend/src` modifié ; aucun accès à la base.

---

## Historique : révision du 30 octobre 2026

État : prêt — révision pédagogique contrôlée le 30 octobre 2026.

21 blocs et leurs identifiants conservés, 114 questions corrigées. 6 exercices remplacés pour diversifier les méthodes ; 0 doublons exacts supplémentaires corrigés. Les titres et les difficultés correspondent aux démarches : 17 découvertes, 2 entraînements, 2 problèmes. Couverture et Id détaillés dans COUVERTURE.md.

Format : même moteur et même syntaxe optitab:1 que la Terminale. Objectifs, sections romaines, propriétés, méthodes courtes, exemples, points d’attention et récapitulation ; fiche synthétique et corrigés question par question. Les constructions ou lectures de graphiques disposent de figures de correction. Les variantes numériques conservées ne sont plus artificiellement classées comme problèmes.

Modifications :

| Id conservé | Travail proposé | Niveau |
|---|---|---|
| 3108 | Déboguer des blocs imbriqués | easy |
| 3110 | Compléter un trajet en rectangle | easy |
| 3115 | Réparer une boucle trop courte | medium |
| 3117 | Choisir l’angle pour un triangle | medium |
| 3122 | Une mauvaise rotation dans le rectangle | hard |
| 3124 | Programmer un projet de clôture | hard |

Mathématiques : 318 assertions de l’audit exact OK sur les fichiers finaux ; Id, calculs, conversions et contraintes contrôlés selon la notion. Les propriétés et les arguments qualitatifs ont été relus avec les énoncés et les figures. Preuves : revision_maths_coordination.log, controle_maths_coordination.json, verification_maths.json ; moteur conservé dans la notion 276/verif_notion.py (et correction reportée dans 279/verif_notion.py).

Figures : 10 PNG actifs, sources TikZ et productions précédentes conservées. Toutes les figures actives ont été regardées sur les planches ou individuellement. Compilation et contrôle texte/traits : OK, aucune tolérance ajoutée. Les graduations d’axes emploient le fond blanc autorisé par le guide ; leur ordre de dessin a été corrigé pour éviter que les courbes ou les côtés traversent les chiffres. Les lettres des points restent hors des traits. Preuve : compilation_figures.json.

Rendu final : vérificateur courant et audit renforcé des erreurs MathJax HTML/SVG ; 65 vues mobiles à 390 px et les mêmes 65 vues à 1 280 px, zéro anomalie restante. Absence de caractères de contrôle C0 interdits vérifiée. Journaux : revision_validation.log et revision_navigateur.log ; statut : controles_revision_20261030.json. Les tableaux trop larges des cours ont été compactés quand nécessaire.

Relecture : cours mobile intégral, fiche et exercices 5, 12, 19, 21, énoncés et étapes, regardés dans les captures finales. Preuves : captures_revision_20261030/relecture_documents.png et relecture_revision_1.png, relecture_revision_2.png ; relecture_visuelle_coordination.json.

Outil : copie locale des audits communs, détection MathJax élargie et attente de fermeture Chrome bornée à deux secondes pour le défaut de nettoyage Windows déjà établi. Les audits ne sont pas allégés. Aucun outil commun ou fichier frontend/src modifié.

Sauvegarde antérieure dans sauvegardes/revision_2026-10-30/. Sources exportées conservées, aucun accès ou import en base. Travail limité à la classe de 5e ; programme rentrée 2026 vérifié par la coordination.
