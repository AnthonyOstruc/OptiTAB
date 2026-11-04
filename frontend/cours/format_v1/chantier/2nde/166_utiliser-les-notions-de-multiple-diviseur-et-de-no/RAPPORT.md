# Notion 166 — Multiples, diviseurs et nombres premiers (Seconde)

**État : prêt.**

## Texte

- Tous les résultats (cours, fiche, 12 exercices) vérifiés dans `verif_166.py` : aucune erreur de maths trouvée.
- **Cours** : les deux démonstrations du programme (somme de deux multiples, carré d’un impair) passent dans des encadrés `demonstration` (calcul aligné) ; critères de divisibilité en liste ; « Tester si $n$ est premier » devient une `methode` ; exemple de décomposition de 360 ajouté avant l’arbre ; fraction irréductible et problème des bouquets en `exemple` (la fraction était dans un encadré « définition ») ; algorithme `est_multiple` ajouté à côté de `est_premier` (deux algorithmes du programme).
- **Fiche** : puces « • » → vraie liste ; liste des 25 nombres premiers < 100 en texte (le crible en image est retiré de la fiche, trop haut pour une fiche) ; liste numérotée non coupée par l’image.
- **Exercices** : `\displaystyle` retirés partout (fractions en `\dfrac`) ; 1923 restructuré (questions en liste, `## Question N`, résultats qui contenaient le titre de la question suivante) et code réécrit en lignes ≤ 30 caractères (boucle `while i * i <= n`, mêmes réponses) ; 1914 rappels de notation aux guillemets cassés réécrits ; 1918 Q3/Q4 justifications ajoutées (chiffre entre 0 et 9, seul multiple de 9 entre 8 et 17) ; 1919 « Primes » → « Nombres premiers », tests justifiés par $p^2 \le n$ ; 1924 Q3 : ensemble de 10 couples trop large pour un téléphone → tableau + liste des 10 nombres, lettre $n$ de Q1 renommée $p$ (conflit avec Q4) ; 1921/1922/1925 : PGCD et PPCM définis dans l’énoncé ou la méthode ; résultats réduits à « $$64$$ », « $$252$$ »… remplacés par des phrases.

## Figures

- 3 refaites (cours : rectangles de 36, crible des nombres premiers, arbre de 360 ; anciennes images matplotlib, texte minuscule pour les rectangles) ;
- 2 ajoutées dans des corrigés : arbre de 120 (1920, Q2), frise des guirlandes 0–180 s (1925, Q4) ;
- 0 conservée ; 1 image en ligne retirée (crible de la fiche, position 2).

## Contrôles

- `verifier_notion.py --navigateur` : OK, 0 problème ; `controle_apercu.mjs` : aucun problème.
- Captures téléphone regardées : cours (3 parties), fiche, exercices 1923 (énoncé), 1920, 1924, 1925 (étapes). Corrigé après captures : liste des nombres premiers de la fiche (formule coupée → nombres séparés), calcul de 1924 Q4 coupé → aligné, figures rectangles/arbres/frise resserrées pour garder un texte lisible sur téléphone.

## Remarques pour l’orchestrateur

- PGCD, PPCM et division euclidienne ne sont pas nommés dans le programme de Seconde (qui parle de « problèmes mobilisant multiple, diviseur, nombre premier » et de fractions irréductibles) ; les exercices 1916, 1921 et 1922 (titres inchangeables) les utilisent comme vocabulaire de modélisation, avec définition dans l’énoncé. À garder ou à marquer « Pour aller plus loin » selon votre choix.

## Vérification des figures 2026-11-02

- **5 figures vues** (diviseurs de 36, crible des nombres premiers < 100, arbre de 360 — cours et fiche —, arbre de 120 et frise des guirlandes dans les corrigés 1920 et 1925), à l'œil et avec le détecteur texte/trait : 5/5 sans chevauchement.
- Contrôles : 25 nombres premiers exacts dans le crible ; décompositions 360 = 2³ × 3² × 5 et 120 = 2³ × 3 × 5 ; frise à 12 s / 18 s, clignotements communs toutes les 36 s jusqu'à 180 s (énoncé : 3 min) ; style des livres.
- **Défauts trouvés : aucun. Figures refaites : aucune.** Notion inchangée : statut remis à « importe ».

## Finition 2026-11-02

**État : prêt** (agent-finition-S1). 12 exercices (aucun ajout : le nombre est suffisant).

### Titres
- Cours et fiche : « Multiples, diviseurs et nombres premiers » → intitulé officiel « Utiliser les notions de multiple, diviseur et de nombre premier » (fiche : « Résumé : … »). **Attention** : `importer_v1.py` ne met à jour que le corps des cours et fiches, pas leur titre → renommer en base si souhaité.
- 11 titres « Type - Chapitre - Sujet » → « Type - sujet » (types « Algorithmique » et « Maîtrise » remplacés) : « Entraînement - Tester en Python multiples et nombres premiers », « Découverte - Division euclidienne et plus grand multiple », « Découverte - Reconnaître un multiple et lister des diviseurs », « Entraînement - Utiliser les critères de divisibilité », « Entraînement - Décomposer un entier en facteurs premiers », « Entraînement - Démontrer des propriétés de divisibilité », « Entraînement - Reconnaître un nombre premier », « Entraînement - Démontrer avec des nombres pairs et impairs », « Entraînement - Rendre une fraction irréductible », « Problème - Phénomènes périodiques et multiples communs », « Problème - Organiser une kermesse avec diviseurs et multiples ».

### Exercices
- **1914 réécrit de zéro** : « Ensembles N et Z - Appartenance » relevait de la notion 165 et était faible → « Découverte - La somme de deux multiples est un multiple » (démonstration du programme : cas 7, cas général, application 7 007 ± 140, contre-exemple 3 + 4 pour la réciproque).
- **1923 : question 6 ajoutée** : troisième algorithme du programme, `plus_grand_multiple(a, b)` (exécuté : 64 pour (8, 70)) ; la même fonction est ajoutée au cours (remarque Algorithmes).
- Les autres exercices relus : justes, au programme (PGCD/PPCM restent définis dans les énoncés, cf. remarque du 29/10).

### Figures (7 nouvelles)
- Corrigés : `ex_somme_multiples` (1914 : 5 + 8 colonnes de 7 carreaux), `ex_multiples_8` (1916 Q4 et 1923 Q6 : 64 ≤ 70 < 72), `ex_diviseurs_24` (1915 : rectangles de 24), `ex_crible_20_39` (1919 : crible, 7² > 39), `ex_somme_impairs` (1917 : les points isolés de deux impairs forment une paire), `ex_feux` (1922 : frise 45 s / 60 s, ensemble à 180 s).
- Cours : `ex_somme_multiples` réutilisée après la démonstration « somme de deux multiples » ; `parite_cours` (8 = 2 × 4, 9 = 2 × 4 + 1) en II.
- 9 exercices sur 12 ont une figure ; sans figure : 1918 (critères), 1921 (fractions), 1924 (preuves littérales) — une figure y serait décorative.
- `figures_livre.py` : 0 erreur, 0 avertissement ; `ex_multiples_8` resserrée (40 à 72) après capture téléphone (texte trop petit).

### Contrôles
- `verif_166.py` : **75 contrôles**, tout juste (fonction Python exécutée sur 1 680 couples).
- `verifier_notion.py --navigateur` : OK ; `controle_apercu.mjs` avec captures : aucun problème.
- Captures téléphone regardées : 1914, 1923 (étapes) ; corrigé : 1914 Q4 (somme et différence sur une ligne, réduite) découpée en deux étapes alignées.
