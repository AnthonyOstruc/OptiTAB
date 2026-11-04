# Rapport — 2nde / 176 Échantillonnage

**État : prêt** (verifier_notion.py --navigateur : OK, 0 problème ; controle_apercu : aucun problème).

## Programme (Seconde 2019)
Couvert : échantillon et fréquence, fluctuation, loi des grands nombres (observée),
écart $\frac{1}{\sqrt{n}}$ (au moins 95 % des cas environ), proportion de N échantillons
sur simulation, principe d'estimation, fonctions Python (fréquence, nombre de succès,
proportion de cas proches).

## Texte
- Cours 216 réécrit et complété : objectifs, définitions, loi des grands nombres,
  méthode « juger un modèle », exemple du dé refait en fractions (900 lancers),
  nouvelle partie IV « Estimer une proportion inconnue » (principe d'estimation,
  exemple de sondage), Python en lignes ≤ 30 caractères, résultats de simulation
  réellement exécutés.
- Énoncé « 95 % des cas » corrigé en « au moins 95 % des cas environ » (calcul exact
  binomial : 95,7 % à 99,2 % selon n et p).
- Fiche 146 : puces corrigées, tableau des écarts $\frac{1}{\sqrt{n}}$, deux méthodes, code.
- Exercices : aucune erreur de résultat dans l'ancien contenu, mais plusieurs faiblesses.
  - 2009 remplacé (titre ajusté) : lecture + suivi en tableau + écriture de `nb_six` avec `randint`.
  - 2010 remplacé : code raccourci, questions sur les boucles imbriquées et l'interprétation.
  - 2005 remplacé (nouveau titre « Une fréquence observée est-elle compatible avec le modèle ? ») :
    il faisait doublon avec 2006 (même cas $p=0{,}65$, $n=225$). Il propose maintenant des situations
    en contexte (dé en fractions, jury, pièce) et la nuance « compatible ≠ prouvé ».
  - 2007 : bornes arrondies vers l'extérieur ([0,486 ; 0,554]) et précision discutée.
  - 2008 : calcul exact $\frac{10\,000}{9}$, vérification de 1 111 / 1 112 et question 6 ajoutée ($\times 25$).
  - 2004, 2006 et 2011 : remis en forme, avec les pièges et l'interprétation ajoutés.
- Ajouts : **nouveau-1** « Découverte - Observer la stabilisation des fréquences » (punaise,
  estimation) ; **nouveau-2** « Entraînement - Lire le nuage des fréquences de N échantillons »
  (compétence du programme : proportion de cas où |f − p| ≤ 1/√n).
- `verif_echantillonnage.py` : 109 contrôles (simulations à graine fixe, probabilités binomiales
  exactes, toutes les réponses en fractions, lignes de code ≤ 30 caractères).

## Figures
- 2 refaites (style livre) : stabilisation (3 simulations), nuage de 100 échantillons avec la bande.
  Les anciennes figures matplotlib ne sont plus utilisées.
- Fiche : position 2 refaite, position 1 retirée (doublon : la fiche reste courte).
- 3 ajoutées : nuage de nouveau-2 (énoncé et corrigé), intervalles des séries A et B (corrigé de 2011).
- 0 conservée.

## Contrôles
Captures téléphone regardées : cours (parties II à V), fiche, exercices 2009 et 2011 (étapes).
Les formules ne sont pas coupées.

## Remarques pour l'orchestrateur
Le chantier n'avait pas d'`etat.json` au départ ; je l'ai créé.

## Finition 2026-11-02

**État : prêt** (agent-finition-S4). 10 exercices (aucun ajout).

### Titres
- Cours et fiche : « Échantillonnage et simulation » → intitulé officiel « Échantillonnage » (« Résumé : Échantillonnage »).
- Titres : types « Algorithmique » et « Maîtrise » remplacés, par exemple « Entraînement - Simuler N échantillons et compter les fréquences proches de p », « Problème - Choisir la taille d’un échantillon ».

### Code Python exécuté pour de vrai
- Cours : les six sorties de `proche(1000, 100, 0.5)` sont celles du code du cours exécuté avec la graine 5 (contrôlé).
- **2010** : les valeurs 0,964 et 0,971 ; 0,963 ; 0,979 ne sortaient pas du code de l’énoncé → remplacées par les sorties réelles (graine 3) : `0.966` (483 échantillons) et `0.97`, `0.975`, `0.971`.
- 2009 : `freq(10, 0.3)` exécuté avec les dix nombres de l’énoncé (renvoie 0.5) ; essai réel ajouté en Q5 : `nb_six(600)` a renvoyé `106` (graine 2009).

### Figures
- **Revérifiées une par une (5)** : `n2_nuage` (énoncé de 3753) refaite : elle affichait p = 0,4 et p ± 1/√n = 0,3 et 0,5, réponses de la question 1 → version sans ces valeurs. Conservées : `cours_stabilisation`, `cours_fluctuation`, `n2_nuage_corrige`, `e2011_intervalles` (justes, données de simulation à graine fixe).
- **6 ajoutées** : 2009 (les dix tirages sur [0 ; 1[, succès en vert), 2007 (quatre intervalles d’estimation et p = 0,20), 2006 (bilan des cinq cas, intervalles normalisés), 2005 (écart |f − p| comparé à 1/√n), 2008 (courbe de 1/√n et n = 100, 400, 1 112), 3752 (stabilisation de la fréquence).
- 8 exercices sur 10 ont une figure ; sans figure : 2004 (calculs de fréquences) et 2010 (code).

### Contrôles
- `verif_echantillonnage.py` : **129 contrôles** ; chaque bloc Python du cours, de la fiche et des exercices est exécuté ; sorties affichées = sorties obtenues.
- Téléphone : étiquettes des nouvelles figures en taille normale après relecture des captures.
- `figures_livre.py` : 0 erreur (aucun texte sur un trait, aucune figure > 1 100 px) ; chaque PNG regardé.
- `verifier_notion.py` : 0 problème de contenu ; seuls signalés : les Id 3752 et 3753, créés en base le 29/10 mais absents de `source_en_ligne/` (export du 29/10 antérieur à leur création) → **ré-export nécessaire avant import** (outil réservé à l’orchestrateur).
- Contrôle navigateur (`controle_apercu.mjs`, téléphone + ordinateur) : 64 vues, aucun problème détecté. Chrome restant parfois bloqué à la fermeture (défaut connu), seul mon processus a été arrêté et son verrou libéré.
- Captures téléphone regardées : cours, fiche et exercices à nouvelles figures.
