# Rapport — notion 369 « Sujets type bac » (Terminale, thème « Préparation au bac »)

**État : prêt.** La notion contient un sujet type bac complet (un seul exercice, `Id: nouveau-1`, difficulté `hard`), un cours de méthode et une fiche. Tout est au format OptiTAB v1. Rien n'a été écrit en base, aucune commande git n'a été lancée et seul ce dossier a été modifié.

## 1. Format de l'épreuve, vérifié sur source officielle

Le texte lu est le **BO spécial n° 4 du 17 septembre 2026**, téléchargé en PDF sur education.gouv.fr (`/sites/default/files/document/20260917boenjsspe4pdf-520753.pdf`, p. 111-112). Il s'agit de la note de service du 11-9-2026, NOR MENE2622642N, « Épreuve terminale de l'enseignement de spécialité mathématiques » :
- épreuve écrite de **4 heures** ;
- elle porte sur le programme de spécialité de Terminale, et les notions de Première peuvent être mobilisées ;
- le sujet comporte **4 exercices indépendants**, chacun noté **de 4 à 8 points**, pour une note globale sur 20 ;
- **la maîtrise de la langue compte pour 2 points sur 20** (orthographe, syntaxe, vocabulaire, organisation), selon une grille annexée ;
- c'est le sujet qui précise si la calculatrice est autorisée ;
- l'oral de contrôle dure 20 minutes, après 20 minutes de préparation.

Dans le même BO, la note MENE2623195N (« Exigences en matière de maîtrise de la langue… à compter de la session 2027 ») demande de **limiter les QCM et les réponses courtes**.

**Session 2026 et session 2027.**
- La session 2026 (juin 2026) est déjà passée. Elle relevait du texte antérieur (note de 2020 modifiée, version consolidée eduscol de mai 2024) : 4 h, 4 exercices notés de 4 à 8 points, **sans** les 2 points de langue. Les pages BO de 2020 sont protégées contre les robots et je n'ai pas pu les lire directement : ce point vient du résumé de la version consolidée trouvé en recherche.
- Les élèves qui s'entraînent aujourd'hui passeront la **session 2027**. Le sujet et le cours suivent donc le texte de septembre 2026. Les autres notes du même BO disent explicitement « à compter de la session 2027 ». Dans l'extrait de la note de mathématiques, je n'ai pas trouvé cette phrase en clair ; la note transversale sur la langue, elle, fixe bien la session 2027.

**Barème retenu** : 4 + 4 + 4 + 6 = 18 points pour les exercices, plus 2 points de langue, soit 20. Le BO ne dit pas si les 2 points s'ajoutent aux exercices ou s'y intègrent : c'est mon interprétation, signalée dans l'énoncé. Pour revenir à 5/4/5/6 sans points de langue, il suffit de modifier le tableau de l'énoncé et les blocs « Barème ».

**Non vérifié sur une source officielle** : le coefficient 16, cité dans le cours. Il est connu et confirmé par des sites secondaires. Aucune date d'épreuve n'est écrite dans les contenus. Aucun énoncé officiel n'a été repris.

## 2. Le sujet (`exercices.txt`, bloc `nouveau-1`)

Titre : « Type bac - Sujet 01 : Loi binomiale, vrai-faux, espace, exponentielle et suite ».

**Source.** Le point de départ est le **sujet 01 du livre** (`livre/livre-maths/livre-terminale/bac/sujet-01.tex` et `corrige-01.tex`). C'est le plus proche d'une session récente : probabilités conditionnelles et loi binomiale, cube, étude d'exponentielle avec convexité et intégration par parties, suite récurrente avec Python.

**Améliorations apportées :**
- **Ex. 1 (4 pts), Probabilités** (livraison point relais / domicile) :
  - arbre « à recopier et compléter » ;
  - formule des probabilités totales, Bayes ;
  - loi B(50 ; 0,071), calcul de P(X ≤ 2) **et ajout de P(X ≥ 3)**, espérance ;
  - n minimal avec ln (63).
- **Ex. 2 (4 pts), Vrai ou faux justifié** : exercice **nouveau** et original. Il remplace un format QCM, conformément aux consignes de 2026. Quatre affirmations :
  - dénombrement (210 comités, vraie) ;
  - équation différentielle y' = −2y + 2 (fausse ; la bonne solution est 3e^(−2x) + 1) ;
  - inéquation avec ln (fausse : l'ensemble est ]2 ; 3] et non [−1 ; 3]) ;
  - Bienaymé-Tchebychev sur une moyenne (vraie).
- **Ex. 3 (4 pts), Espace** (tétraèdre régulier BDEG dans le cube) :
  - **erreur corrigée** : dans le livre, le point d'intersection s'appelle **H**, alors que H est déjà un sommet du cube, cité à la question 6. Il est renommé **K** ;
  - les tétraèdres « de coin » sont nommés explicitement (ABDE, CBDG, FBEG, HDEG) ;
  - remarque ajoutée : Δ est la diagonale (DF).
- **Ex. 4 (6 pts), Fonction, suite, intégrale** : les ex. 3 et 4 du livre sont fusionnés en une étude de **f(x) = xe^(−x)**. La fonction (x + 1)e^(−x) du livre ne permettait pas une suite u(n+1) = f(u(n)) monotone. L'exercice couvre :
  - limites par croissance comparée, dérivée, tableau de variations ;
  - TVI (0,35 < α < 0,36) ;
  - convexité et point d'inflexion I(2 ; 2e^(−2)) ;
  - tangente y = x et position de la courbe par concavité ;
  - suite u0 = 1 : construction en escalier, récurrence, convergence vers 0 (point fixe) ;
  - fonction Python `seuil` (seuil(0.1) = 8) ;
  - intégration par parties (I = 1 − 2/e) et aire entre T et la courbe (2/e − 1/2 ≈ 0,24).

**En-tête** : durée 4 h, calculatrice en mode examen, 4 exercices, 5 pages papier, tableau du barème sur 20.

**Corrigé** : chaque question donne la méthode, des étapes détaillées, le résultat encadré, l'erreur fréquente et le **barème** (bloc « Barème », total contrôlé par programme). La rubrique Solution donne des réponses courtes, exercice par exercice.

**Couverture** : tout le programme principal y figure, sauf sinus/cosinus. Un seul sujet ne peut pas tout couvrir ; ils sont traités dans le cours et la fiche. Rien des mathématiques expertes.

## 3. Cours et fiche

- **Cours 370 « Méthode : réussir l'épreuve de mathématiques du bac »**, réécrit de zéro, en huit parties :
  1. l'épreuve en bref (format 2027, tableau du programme évalué) ;
  2. gestion des 4 h (frise) ;
  3. lecture du sujet et tableau des mots de consigne ;
  4. rédaction : les trois temps d'une réponse, une rédaction modèle, le vocabulaire juste, les 2 points de langue ;
  5. calculatrice : usages et limites ;
  6. **onze questions types avec leur méthode et un exemple** : limite, TVI, convexité, récurrence, suites et seuil, intégrale et IPP, équation différentielle, loi binomiale, concentration, espace (projeté orthogonal), ln et exp ;
  7. dix pièges classiques ;
  8. check-list du jour J.
- **Fiche 308** : formules et réflexes, partie par partie. Elle contient les tableaux des suites, des dérivées, de exp/ln, des primitives et du dénombrement, plus les probabilités, l'espace et les réflexes de rédaction.
  - **Titre demandé** : « Résumé : l'essentiel pour le jour du bac ». Il est écrit dans `fiche_308.txt`, mais en base le titre est « … pour le bac ». **`importer_v1.py` n'importe pas les titres** : il faut renommer la fiche à part.

## 4. Figures (`figures/figures.py`, compilées par `figures_livre.py`)

- **18 figures neuves, 21 placements, 0 image en ligne conservée** (la notion n'en avait aucune). Toutes ont été regardées à l'œil. Le contrôle des chevauchements texte/trait donne 0 erreur. Les largeurs vont de 498 à 781 px.
- **Sujet : 13 placements.**
  - Énoncé (4) : arbre à compléter, cube avec tétraèdre, courbe de f, zoom de la courbe avec y = x.
  - Corrigé (9), éléments de réponse en vert :
    - arbre complété ;
    - loi B(50 ; 0,071) avec P(X ≤ 2) ;
    - courbes de l'équation différentielle ;
    - droite graduée de l'inéquation avec ln ;
    - cube avec Δ et K ;
    - figure de α ;
    - tangente et point d'inflexion ;
    - escalier u0, u1, u2 ;
    - aires I et A.
- **Cours (5)** : frise des 4 h, TVI, convexité, loi B(10 ; 0,3), projeté orthogonal. **Fiche (3)** : elle réutilise convexité, binomiale et projeté.
- Toutes les valeurs tracées sont calculées dans `figures.py`, puis recontrôlées par `verif_bac.py`.

## 5. Contrôles

- **`verif_bac.py` (sympy) : 143 contrôles, 0 erreur** (`verif_log.txt`). Il vérifie :
  - les probabilités et la loi binomiale, **calculées avec math.comb** et non recopiées ;
  - le n minimal, les quatre affirmations (dont `dsolve` et `solveset`) ;
  - toute la géométrie (longueurs, normale, K, volumes par déterminant) ;
  - l'analyse : limites, f', f'', α, inflexion, x − f(x), suite, IPP, aire ;
  - la **fonction Python du corrigé, extraite du texte et exécutée** ;
  - le **barème relu dans le texte** (4/4/4/6 + 2 = 20, un barème par question) ;
  - les exemples du cours (dont `seuil` exécutée) ;
  - les tableaux de dérivées et de primitives de la fiche ;
  - la cohérence entre figures et texte.
- **`valider_v1.py`** : aucune erreur de syntaxe. Il reste seulement les messages « [IMAGE_N] utilisée mais 0 déclarée », que `verifier_notion` filtre, comme pour tout bloc `nouveau-N`.
- **`verifier_notion.py --navigateur`** :
  - **sur le dossier réel**, il signale 13 « problèmes » du type « nouvelle figure jamais appelée ». C'est un **défaut de l'outil** (voir § 6) ;
  - **sur une copie de travail** dont le `meta.json` déclare `nouveau-1`, le résultat est **« OK », 0 problème**, contrôle Chrome compris.
- **Formules et tableaux coupés** : un script de contrôle à 390 px recherche les formules qui défilent ou dépassent, les tableaux et le code qui défilent, les images qui dépassent. Résultat : **0 coupure** (cours, fiche, énoncé, étapes, solution).
- **Captures téléphone regardées à l'œil** :
  - le cours en entier (11 écrans), la fiche (5), l'énoncé (6), **toutes les étapes du corrigé (21)** ;
  - corrections faites après relecture :
    - figures sorties des encadrés « étape » (elles y étaient trop réduites) et rétrécies ;
    - chaînes d'équivalences réécrites avec « ⟺ » en début de ligne ;
    - affirmations du vrai-faux séparées du contexte ;
    - « ; » orphelins supprimés ;
    - écriture ]−∞ ; a] sans espace parasite ;
    - un tableau de la fiche qui défilait, scindé.
- **`controle_apercu.mjs` avec captures** : **10 vues (téléphone et ordinateur ; cours, fiche, énoncé, étapes, solution), 0 problème**, et l'outil s'est terminé normalement, sans blocage à la fermeture de Chrome. Voir `captures_log.txt` et `captures/` (laissé en place). Le journal du vérificateur sur le dossier réel est dans `verif_navigateur_log.txt` : ce sont les 13 faux positifs décrits au § 6.

## 6. Remarques pour l'orchestrateur

1. **Défaut de `verifier_notion.py`** : quand `meta.json` a `"exercices": []` (notion sans exercice en base), le fichier `exercices.txt` est entièrement ignoré (`if meta["exercices"]:`). Ni sa syntaxe ni ses images ne sont alors contrôlées, et chaque figure `nouveau-N` est déclarée « jamais appelée ». Il faudrait parcourir aussi les blocs `nouveau-N` dans ce cas. `importer_v1.py`, lui, traite bien les `nouveau-N` même sans exercice en base.
2. **Titre de la fiche** à renommer à part (voir § 3). L'**activation de la notion** (est_actif) reste à faire, comme prévu.
3. **Livre** : `livre-terminale/bac/sujet-01.tex` et `corrige-01.tex` gardent le conflit de nom « H » (sommet du cube et point d'intersection). Je n'y ai pas touché : c'est hors de mon dossier, mais c'est à corriger dans le livre.
4. Les chiffres « 5 pages » et le barème 18 + 2 sont des choix de présentation, expliqués au § 1.
