# Rapport : 2nde / 178 « Notion de fonction » (Python)

**État : prêt.** `verifier_notion.py --navigateur` : OK, 0 problème ; `verif_notion_de_fonction.py` : tout est correct.

## Périmètre
Dans la base, la notion 178 appartient au thème 75 « Algorithmique et programmation ». Le cours (220) s’intitule « Notion de fonction en Python ». Le contenu porte donc sur les **fonctions Python** du programme de Seconde 2019 : arguments, valeur renvoyée, fonctions aléatoires, répétition d’expériences, moyenne et écart type sans liste. Image, antécédent et courbe relèvent de la notion 172 : ils n’ont pas été ajoutés ici.

## Texte
- Cours réécrit en 5 parties : I. définir et appeler (`return` / `print`, `None`), II. plusieurs arguments (l’ordre compte, méthode), III. `randint` / `random`, propriété « `random() < p` est vrai avec la probabilité p », IV. fréquence et fluctuation, V. moyenne et écart type sans liste.
- Fiche : refaite avec le code en blocs, les définitions et les 4 pièges classiques.
- Tout le code passe à `from random import randint`. Les lignes de code font au plus 30 caractères, ce qui est vérifié automatiquement, et la syntaxe est compilée.
- **Erreurs corrigées** :
  - 1937 Q4 : `image_affine(4, -1, 3)` donnait 11, comme en Q3, alors que l’énoncé demandait « pourquoi est-ce différent ». La question est remplacée par `affine(-1, 4, 3)`, qui donne 1. Une question « image de 5 par g » est ajoutée.
  - 1941 : la garde `if variance < 0`, consacrée aux arrondis flottants et hors programme, est retirée. Elle est remplacée par une question d’interprétation de la moyenne et de l’écart type, avec une sortie réellement simulée (3,475 ; 1,713).
  - 1939 : π ≈ 3,14 est remplacé par `from math import pi`, et `** 0.5` par `sqrt`.
- Les 8 exercices existants sont réécrits en version pédagogique : pour chaque question, une méthode, des étapes détaillées, un résultat et, au besoin, une erreur fréquente ou un « à retenir ». Les tableaux de suivi et les données sont en tableaux natifs. Les Id et les titres sont inchangés.
- **Ajouts** :
  - `nouveau-1` « Entraînement - Simuler un événement de probabilité p avec random() » : `random()` n’était travaillé dans aucun exercice.
  - `nouveau-2` « Découverte - Repérer et corriger les erreurs classiques » : `print` au lieu de `return`, compteur dans la boucle, `return` dans la boucle, import oublié, priorité opératoire.

## Figures
- 2 images en ligne refaites. Elles étaient au style matplotlib, et l’une contenait du code dans l’image. Elles sont utilisées dans le cours et la fiche :
  - `machine_fonction.png` : schéma argument → fonction → valeur renvoyée ; le code est maintenant en bloc texte ;
  - `frequence_six.png` : la fréquence du 6 en fonction de n se stabilise vers 1/6. Elle remplace le diagramme en barres.
- 1 figure ajoutée : `frequence_tir.png`, dans le corrigé de nouveau-1 ; la fréquence se stabilise vers 0,7.
- 0 image conservée. Les simulations sont reproductibles grâce à des graines fixées dans `figures/figures.py`.

## Contrôles
Captures téléphone regardées : cours (3 vues), fiche, énoncé et étapes de 1942, étapes de 1941 et de nouveau-1. Les formules trop larges ont été passées en formules centrées ou en `aligned`.

## Remarques pour l’orchestrateur
- La consigne de mission évoquait « image, antécédent, ensemble de définition » : ce n’est pas le contenu de cette notion, qui est algorithmique (voir Périmètre).
- Le titre de la notion (« Notion de fonction ») pourrait être précisé en « Notion de fonction (Python) » côté base, pour éviter la confusion avec 172.

## Finition 2026-11-02

**État : prêt** (agent-finition-S3). 10 exercices (aucun ajout) ; **10 sur 10 ont une figure** (9 n'en avaient pas).

### Revérification des 3 figures existantes
- `machine_fonction`, `frequence_six`, `frequence_tir` : recompilées (détecteur : 0 alerte ; un premier essai avait échoué sur un conflit de cache de polices pendant une compilation parallèle, relancé seul : OK), regardées : justes (f(4) = 3 × 4 + 2 = 14 ; fin des courbes proche de 1/6 et de 0,707), lisibles → conservées.

### Figures ajoutées (11), calculées en exécutant le code de l'énoncé
Les données des figures d'exercices sont obtenues dans `figures/figures.py` en **exécutant les blocs Python de `exercices.txt`** (graine fixée quand il y a du hasard) : la figure montre exactement ce que calcule la fonction de l'énoncé.
- Schémas entrée → fonction → sortie : `machine_triple` (1936, triple(4) → 12), `machine_affine` (1937, affine(3, -1, 4) → 11 et affine(-1, 4, 3) → 1 : l'ordre des arguments), `print_return_triple` (1936) et `print_return_double` (3742) : `return` renvoie la valeur, `print` l'affiche et renvoie `None`.
- Courbes tracées à partir d'un tableau de valeurs calculé par la fonction : `points_mystere` (1938, points alignés sur y = 3x + 15, avec la table de valeurs ajoutée au corrigé), `points_f_1939` et `points_g_1939` (1939, x² − 4x + 3 puis décalage de +4).
- Simulations : `somme_deux_des` (1940, 10 000 appels de `deux_des()` : 7 la plus fréquente), `stats_des_1941` (1941, fréquences des faces des 10 000 lancers de `stats_des(10000)`, m ≈ 3,48 et bande m ± σ), `freq_pair_1942` (1942, un appel `frequence_pair(n)` par n), `freq_gagnants_1943` (1943, `nb_gagnants(n) / n` → 0,2).

### Texte
- Cours et fiche : « Notion de fonction en Python » → **« Notion de fonction »** (intitulé officiel du programme, thème Algorithmique et programmation) ; fiche : « Résumé : Notion de fonction ».
- 3742 Q5 : la sortie réelle de `moyenne(4, 6)` (version fausse) est `7.0`, pas « 7 » → corrigé.
- 8 titres d'exercices réécrits (« Algorithmique » et « Maîtrise » supprimés), par exemple : « Entraînement - Fonctions pour un jeu de dé : gain, moyenne et fréquence », « Découverte - Définir et appeler une fonction à un argument », « Découverte - Exécuter une fonction à la main », « Entraînement - Simuler des expériences aléatoires avec randint », « Problème - Simuler une tombola ».

### Contrôles
- `verif_notion_de_fonction.py` : lignes ≤ 30 caractères et syntaxe de tous les blocs, puis **exécution réelle des 61 blocs de code** du cours, de la fiche et des exercices : chaque fonction est appelée et ses résultats **et affichages** comparés au texte (ex. `aire_rectangle(8, 2.5)` → `20.0`, `triple_b(4)` affiche `12` et renvoie `None`, `gains(5)` avec 7, 10, 20, 3, 15 → `(70, 14.0)`, `stats_des(10000)` graine 41 → 3,475 et 1,713 ; les fonctions **fausses** de 3742 produisent bien l'erreur décrite : `TypeError`, compteur remis à 0, `return` dans la boucle, `NameError` sur `randint`, `7.0`). Les données de chaque figure sont recomparées aux appels réels.
- `verifier_notion.py --navigateur` : sur le dossier réel, seuls les Id 3741 et 3742 (absents de `meta.json`) sont signalés ; sur une copie de travail les déclarant : **OK, 0 problème**.
- Captures (`controle_apercu.mjs`, téléphone et ordinateur) : **aucun problème** ; regardées au téléphone : corrigés 1936 (schémas) et 1938. Après relecture : la table de valeurs de 1938 (9 colonnes, qui défilait) est passée en colonnes ; les figures de 1940, 1941, 1942 et 1943 sont sorties des encadrés pour être affichées en pleine largeur.

### Remarque pour l'orchestrateur
- Ré-exporter `meta.json` (Id 3741 et 3742 absents) avant l'import.
- Le titre du cours devient « Notion de fonction » (intitulé officiel) : penser à `titres_docs.py` à l'import.
