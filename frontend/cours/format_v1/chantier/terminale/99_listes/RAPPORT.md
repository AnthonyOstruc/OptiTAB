# Rapport : Terminale, notion 99 « Listes »

## Finition 2026-11-02

**État : prêt.** Le cours 105, la fiche 37 et **11 exercices** (les 5 existants réécrits de zéro, 6 ajoutés) sont au format v1. Le cours et la fiche s'intitulent « Notion de liste » et « Résumé : Notion de liste », d'après l'intitulé du programme. L'aperçu affiche encore « Listes », qui est le nom en base.

L'ancien rapport du 28/10 est dans `sauvegardes/finition_20261102/RAPPORT_ancien.md`.

### Programme (Terminale 2019, « Algorithmique et programmation »)

Le BO ne demande que de consolider la Première : générer une liste (en extension, par ajouts successifs, en compréhension), manipuler ses éléments (« ajouter, supprimer… ») et ses indices, la parcourir et itérer sur ses éléments. Il précise aussi : compréhension ↔ notion d'ensemble ; conditions ↔ logique ; « on se limite aux listes ».

- **Couvert** :
  - indices et rangs ;
  - les trois façons de générer une liste ;
  - compréhension et ensembles (`and` pour ∩, `or` pour ∪, `not` pour le complémentaire, formule du cardinal) ;
  - `append`, `pop` et `remove` (tirages sans remise) ;
  - parcours ; liste de listes ;
  - usages de Terminale : termes d'une suite et seuil, sommes partielles et limite, simulation d'une loi binomiale (effectifs et fréquences), échantillons et loi des grands nombres, Bienaymé-Tchebychev, marche aléatoire (citée par le programme), k-uplets, couples distincts et parties à 2 et 3 éléments.
- **Retiré** car purement informatique ou hors du programme de Terminale : `insert`, `index`, `sort` et `sorted`, `reverse`, `copy` et l'affectation de listes, les tranches, les listes de courses et de fruits.
- **itertools** : il n'est que cité dans une remarque « Pour aller plus loin ». Il produit des tuples, et le programme dit « on se limite aux listes » ; les listes en compréhension suffisent et montrent mieux le lien avec les ensembles.

### Texte
- **Cours réécrit de zéro** en 8 parties : rappels, générer, ajouter et supprimer, parcourir, listes et suites, listes et probabilités, listes et dénombrement, erreurs fréquentes avec « À retenir ».
- **Fiche réécrite** : indices, génération, ajout et suppression, parcours, puis les usages de Terminale (seuil, simulation, dénombrement) et 5 pièges.
- **Exercices existants réécrits** (Id conservés, titres changés) :
  - 836 : « Découverte - Indices et termes d'une suite »
  - 838 : « Entraînement - Listes en compréhension et ensembles »
  - 837 : « Entraînement - Ajouter et supprimer : tirages sans remise »
  - 840 : « Entraînement - Termes d'une suite et seuil avec une liste »
  - 839 : « Entraînement - Sommes partielles et limite »
- **Exercices ajoutés** :
  - nouveau-1 : « Découverte - Lister les k-uplets d'un ensemble »
  - nouveau-2 : « Entraînement - Lister les combinaisons d'un petit ensemble »
  - nouveau-3 : « Entraînement - Simuler une loi binomiale avec des listes »
  - nouveau-4 : « Type examen - Sondage, échantillons et inégalité de Bienaymé-Tchebychev »
  - nouveau-5 : « Entraînement - Fréquences successives et loi des grands nombres »
  - nouveau-6 : « Problème - Marche aléatoire avec une liste des positions »
- Les niveaux sont répartis ainsi : 2 Découverte, 7 Entraînement, 1 Problème, 1 Type examen. Chaque corrigé est complet : méthode, étapes, résultat encadré, erreur fréquente si utile.

### Code exécuté (`verif_listes.py`, moteur `moteur_verif.py`, journal `verif_log.txt`)
- **54 programmes exécutés pour de vrai et 45 affichages identiques à l'exécution.** Un seul programme à compléter (840) n'est pas exécuté ; sa version complète l'est.
- **Graine fixe** : toutes les simulations contiennent `seed(2026)`, avec une explication pour les élèves, et le script refuse toute simulation sans graine.
- Dans le cours, les simulations portent sur **10 000 tirages**. Avec 1 000 tirages, la fréquence de X = 3 valait 0,275 pour une probabilité de 0,3125 : la démonstration n'était pas convaincante.
- Le texte qui commente les simulations (fréquences, moyennes, proportions) a été accordé aux valeurs réelles. Exemples : sondages dans la bande, 92,5 % ; tirages de somme 5, 0,1959.
- **30 contrôles mathématiques** (sympy, valeurs exactes) :
  - termes et formes explicites, seuils et logarithmes, somme des intérêts égale à u₈ − 1 800 ;
  - S_n = 2 − 1/2ⁿ ;
  - cardinaux de A, B, A ∩ B, A ∪ B, diviseurs ;
  - dénombrements : 8 triplets, 20 tirages ordonnés et 10 parties, C(5,2) = C(5,3) ;
  - lois binomiales ; majorant de Bienaymé-Tchebychev 0,2496 et n = 1 997 ;
  - marche aléatoire : P(X₂₀ = 0) = C(20,10)/2²⁰ ≈ 0,176.
- Le script vérifie aussi les largeurs des lignes de code sur téléphone.

### Figures (25 neuves, 28 emplacements)
- Les 4 anciennes figures sont supprimées : indices de notes, insertion, copie, fruits. La notion n'avait aucune image en ligne.
- **Cours (6)** :
  - liste avec indices et rangs ;
  - diagramme de Venn de A ∩ B ;
  - évolution des listes `urne` et `t` avec `remove` et `append` ;
  - termes et seuil ;
  - histogramme binomial, lu dans l'affichage réel ;
  - grille des couples, avec les parties en vert.
- **Fiche (2)** : la liste avec ses indices et la grille des couples.
- **Exercices** : une figure dans l'énoncé et sa version complétée en vert dans le corrigé pour 838 (Venn), 840 (seuil), 839 (sommes et limite), nouveau-1 (arbre de 3 lancers), nouveau-2 (grille 5 × 5), nouveau-3 (histogramme), nouveau-4 (200 sondages et bande [0,47 ; 0,57]), nouveau-5 (fréquence → 1/6), nouveau-6 (marche aléatoire).
- 836 et 837 ont une figure dans le corrigé seulement. Pour 836, la figure de l'énoncé aurait donné la réponse.
- Les figures de simulation exécutent le programme du texte avec la même graine.
- Le détecteur ne signale aucun texte sur un trait. Toutes les figures font au plus 900 px.
- **Chaque PNG a été regardé.** Ont été refaits : le Venn (nombres sur les cercles), les grilles (trop étroites), la marche (étiquettes sur le trajet) et la largeur du schéma de l'urne.

### Contrôles
- `verifier_notion.py --navigateur` : **OK, 0 problème**.
- `controle_apercu.mjs` avec captures : aucun problème. Les deux outils se sont terminés normalement.
- **Captures téléphone regardées** : le cours en entier, la fiche, et les étapes de nouveau-4.
- **Corrections faites après relecture et contrôle** :
  - 17 codes en ligne trop longs : le code en ligne est non sécable, et le contrôleur les avait signalés dans les exercices ;
  - tableau « ensemble ↔ liste » du cours tronqué, non détecté : passé en liste ;
  - 5 formules longues passées en formules centrées.

### Remarques pour l'orchestrateur
- **À renommer en base** (suggestion) : la notion « Listes » devient « Notion de liste », intitulé officiel, comme la notion 164 de Première.
- **6 exercices à créer** à l'import (`nouveau-1` à `nouveau-6`) ; leurs figures sont dans `correspondance.json`.
- **Défaut du contrôleur** : un tableau dont une cellule contient du code (`white-space: nowrap`) est tronqué sur téléphone sans alerte dans le cours. Le même code est signalé dans les exercices.
- Un fichier temporaire abandonné du 28/10, `etat.json.tmp.3604…`, a été supprimé (dans ce dossier).
