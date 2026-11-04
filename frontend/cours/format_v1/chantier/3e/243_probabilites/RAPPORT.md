# Notion 243 — Probabilités (3e)

**État : prêt** (agent-3e-243, 2026-11-03).

## Cours et fiche

- **Titres** : « Probabilités » (cours) et « Résumé : Probabilités » (fiche), au lieu de « … et expériences à deux étapes » (= intitulé de la notion).
- **Cours réécrit** au programme du cycle 4 : objectifs en liste ; I. vocabulaire (expérience aléatoire, issue, événement, issue favorable, **événement contraire**, **événements incompatibles**, avec exemples sur le dé) ; II. calcul (définition, 0 ≤ P ≤ 1, impossible / certain, équiprobabilité, méthode en 3 points, sac de boules avec figure, erreur « compter les couleurs », P(non A) = 1 − P(A), **P(A ou B) = P(A) + P(B) pour des incompatibles**, contre-exemple pique / as) ; III. deux épreuves : tableau à double entrée (somme de deux dés, cases vertes) et arbre (règles produit / somme, avec remise, sans remise, contrôle « total = 1 ») ; IV. fréquence et probabilité (définition, stabilisation, courbe simulée, « le hasard n'a pas de mémoire ») ; encadré « À retenir ».
- **Fiche** refaite dense : tableau du vocabulaire, 3 formules encadrées, réflexes, arbre avec remise, tableau avec / sans remise, fréquences, 4 erreurs classiques, réflexe brevet.
- Rien hors programme : pas de probabilités conditionnelles (les arbres n'ont que des tirages avec / sans remise ou des urnes indépendantes).

## Exercices (21, tous relus et réécrits)

- Chaque corrigé : méthode, étapes détaillées, résultat encadré, **erreur fréquente** (ou « À retenir ») en encadré ; `\displaystyle` et « À retenir » en gras libre supprimés.
- Titres « Type - Chapitre - n. Sujet » → « Type - Sujet ».
- **Remplacés (3)** :
  - 2340 « Impossible, certain ou entre les deux ? » (doublon du dé de 2338) → « Découverte - Issues, événements et contraires » (12 cartes : issues, contraire, **incompatibles**, P(B ou C), impossible / certain) — le vocabulaire « incompatibles » n'était travaillé nulle part ;
  - 2352 « Un jeu à points » (gain moyen = espérance, hors programme de 3e) → « Problème - Le jeu est-il équitable ? » (produit de deux dés, tableau, nouvelle règle équitable) ;
  - 2358 « Le parcours du labyrinthe » (arbre à probabilités différentes selon la branche = conditionnelles, lycée) → « Type brevet - Le stand de la kermesse » (jeton + roue, tableau, fréquence observée).
- **Retravaillés** : 2342 arbre à compléter ; 2345 tableau donné puis cases vertes ; 2346 / 2347 arbres à compléter (composition du sac après chaque tirage) ; 2348 comptage dans le tableau (11 cases, double comptage) ; 2350 tableau des codes, question « code 32 » gardée, question doublon retirée ; 2351 recentré sur contraire et incompatibilité ; 2355 question 5 (deux billets sans remise, calcul lourd) remplacée par « combien de billets gagnants pour 1/4 » ; 2339 question 4 avec contrôle par comptage.
- Progression : 7 Découverte, 7 Entraînement, 4 Problème, 3 Type brevet (2356, 2357, 2358 en fin de liste).

## Figures (22 fichiers, 27 emplacements, style livre, aucune ancienne image conservée)

- **Refaites (6 images en ligne)** : arbre des deux pièces (cours → remplacé par l'arbre avec remise ; exercice 2342 en version énoncé « … » + corrigé vert), tableau des sommes de deux dés (2345), arbres avec / sans remise (2346, 2347) — tous en version énoncé à compléter + version corrigé en vert. L'image de la fiche est remplacée par l'arbre avec remise.
- **Ajoutées** : sac de boules (cours, 2339), roue à 8 secteurs (2341 énoncé + secteurs pairs en vert au corrigé), roue à 4 secteurs (2358), courbes de fréquences qui se stabilisent (cours, 2343, 2354), tableaux à cases vertes (somme 7, somme ≥ 10, au moins un six, codes, produits pairs, kermesse), arbres des urnes (2353, énoncé + corrigé), arbre des menus (2356).
- `figures_livre.py` : 0 chevauchement texte / trait ; toutes ≤ 900 px.

## Contrôles

- `verif_243.py` : **64 contrôles** (fractions exactes, dénombrements exhaustifs par `itertools.product`, équations sympy), tout juste.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (après les dernières corrections). `controle_apercu.mjs` : 130 vues (téléphone + ordinateur, cours, fiche, 21 exercices × 3 onglets) : 0 débordement, 0 erreur de formule, 0 image manquante. Chrome ne se ferme pas seul : seul mon processus arrêté, mon verrou `chrome_0.lock` retiré.
- Captures téléphone regardées : cours (parties II à IV), fiche, exercices 2340, 2345, 2347, 2352, 2357. Corrections faites : calcul aligné de l'exemple « avec remise » du cours coupé à droite → deux formules séparées ; fractions en ligne qui se touchaient sur deux lignes (2346, 2347, 2352, 2357, 2340) → formules centrées ou liste ; 16 formules seules sur leur ligne suivies d'un point isolé → formules centrées ; arbre des menus aéré ; étiquette « 1/3 » de la courbe agrandie.

## Remarques pour l'orchestrateur

- Trois exercices passent en « Type brevet » (2356, 2357, 2358), conformément à la progression de la consigne.
- 2357 (dé truqué) est gardé : probabilités non équiprobables dont la somme vaut 1, c'est au programme ; aucune probabilité conditionnelle dans la notion.
- Les 6 images matplotlib en ligne (cours, fiche, 2342, 2345, 2346, 2347) ne sont plus appelées : elles sont remplacées par les nouvelles figures et seront supprimées à l'import.
