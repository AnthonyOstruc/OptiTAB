# Rapport — Terminale, notion 95 « Combinatoire et dénombrement »

## État

**Prêt.** Cours 94, fiche 39 et 10 exercices au format v1 ; `verifier_notion.py --navigateur` : OK (0 problème).

## Texte

- **Vérification** : `verif_combinatoire.py` (à garder) recalcule 132 résultats (cours, fiche, exercices), par formule (`math.comb`, `math.perm`) et par énumération (`itertools`) chaque fois que c'est faisable : comités « au moins », boules identiques, appariements du tournoi, triplets $(r ; b ; v)$, table ronde à rotation près… Tous les résultats numériques en ligne étaient justes.
- **Erreurs de fond corrigées** :
  - 1269 Q1 : la partie vide était écrite $\{\varnothing\}$ (ensemble à un élément) → $\varnothing$, avec une remarque « Attention » ;
  - 1270 Q3 : « nombre de combinaisons de chiffres » pour des $3$-uplets avec répétition → vocabulaire corrigé ;
  - 1271 Q3 : « équation diophantienne » (hors programme) → dénombrement organisé des triplets dans un tableau natif ; énoncé précisé (« seul compte le nombre de boules de chaque couleur ») ;
  - énoncés ambigus précisés : dés distingués (1263), répétitions et ordre quelconque des mots de passe (1268, 1272), équipes non distinguées (1267), polygone convexe (1267), $n \ge 2$ (1266, 1268), $1 \le p \le n$ (1265) ;
  - 1272 E2 c) : remarque ajoutée (si les 4 matchs sont fixés, seulement $2^4 = 16$ groupes de demi-finalistes) ;
  - 1267 : bloc « Étape bis » cassé par la conversion → étapes réécrites.
- **Cours** : remise à niveau complète sur le programme (cardinal, principes additif/multiplicatif, $k$-uplets, factorielle, arrangements, permutations, combinaisons, formule de $\binom{n}{k}$, symétrie, relation et triangle de Pascal, somme $2^n$, mots et chemins). Les trois démonstrations du programme sont rédigées en encadrés `demonstration` (nombre de parties, expression de $\binom{n}{k}$, relation de Pascal). Ajouts : tableau « Choisir le bon modèle », méthodes (tirages, « au moins », dénombrement et probabilités, objets identiques), bloc Python.
- **Fiche** : tableau des modèles natif, formules, pièges ; puces « • » de la conversion remplacées par de vraies listes.
- **Exercices** : DS restructuré (`## Partie A : …` + `## Question A1 : …`, réponses qui débordaient dans les blocs `resultat` réparées) ; objets identiques traités par choix des positions (méthode du programme), la formule $\frac{n!}{n_1!\,n_2!\,n_3!}$ gardée en vérification ; vérifications par le complémentaire ajoutées ; démonstrations (Pascal, symétrie, $2^n$) rendues complètes ; rappels en encadré `rappel`.

## Figures (style des livres, `figures/figures.py`)

- **3 refaites** (style matplotlib, polices DejaVu, couleurs criardes) : arbre des couples (`arbre_arrangements`), triangle de Pascal (`triangle_pascal`), organigramme « quel modèle ? » (`organigramme_modele`), réutilisés dans la fiche.
- **4 ajoutées** : arbre des parties de $\{a ; b ; c\}$ (`arbre_parties`, cours II et corrigé 1270 Q5), chemin sur quadrillage (`chemin_quadrillage`, cours IV « mots et chemins »), table ronde (`table_ronde`, corrigé 1264 Q5), hexagone et ses diagonales (`hexagone_diagonales`, corrigé 1267 Q5).
- **0 conservée, 0 retirée** (les 5 positions en ligne sont remplacées). Aucun texte sur un trait (contrôle de `figures_livre.py` sans erreur ni avertissement), largeurs de 669 à 842 px. Chaque PNG regardé.

## Contrôles

- `verifier_notion.py --navigateur` : OK (un bloc Python trop large sur téléphone a été raccourci).
- Captures `controle_apercu.mjs` dans `captures/` ; vues regardées sur téléphone : le cours en entier, la fiche, les étapes de 1271 et d'autres exercices. Corrigé après relecture : triangle de Pascal et organigramme refaits plus étroits (615 et 657 px) pour que leur texte reste lisible sur téléphone ; tableau du cours V (trop large) remplacé par un encadré d'exemples ; colonne trop large du tableau de la fiche raccourcie ; formule trop large de 1271 Q3 passée en liste ; démonstration III réécrite (une virgule tombait en début de ligne).

## Remarques pour l'orchestrateur

- `figures_livre.py` : lancé avec un chemin relatif, `pdftocairo` échouait (chemin de sortie résolu depuis `build/`) ; corrigé depuis côté outil d'après le message reçu, contourné ici par un chemin absolu.
- Un titre `## Question A1 : …` n'a pas de pastille numérotée (le moteur n'accepte que `Question 2` ou `Question 2a`) : rendu en titre simple, comme dans la notion 179.
- Moteur : une ligne peut se couper entre une formule et le tiret qui la suit (« un $n$ / -uplet », vu sur téléphone dans la démonstration du cours II). Il faudrait coller le « - » qui suit une formule, comme on le fait déjà pour la ponctuation.
- Notation $A_n^k$ conservée dans les exercices (usuelle mais non officielle) ; le cours la présente comme « parfois notée ».


## Finition 2026-11-02

**État : prêt** (passe de finition, agent finition-T6). Sauvegardes avant finition : `sauvegardes/*_avant_finition_20261102.*`.

### Titres
- Cours « Combinatoire et dénombrement » et fiche « Résumé : Combinatoire et dénombrement » : intitulé officiel, inchangés.
- 10 titres d’exercices sans « Dénombrement » répété ni majuscules abusives (ex. « Découverte - Arrangements : podiums, codes et bureaux », « Entraînement - Délégués, anagrammes, nombres et diagonales », « Problème - Chemins sur un quadrillage, bureaux et symétrie », « DS - Devoir surveillé complet »). Types inchangés.

### Exercices
- **2 ajoutés** (10 → 12) : `nouveau-1` « Type examen - Prélèvements simultanés ou successifs » (lot de 20 composants dont 4 défectueux : combinaisons, « au moins un » par le contraire, puis 3-uplets avec remise et lien avec B(3 ; 0,2)) ; `nouveau-2` « Problème - Triangle de Pascal en Python » (ligne 7 à compléter, fonctions `suivante` et `ligne` exécutées pas à pas, somme 2¹⁰, QCM et `ligne(10)[3]`), compétence algorithmique du programme jusque-là absente.
- **3 questions réécrites (doublons)** : 1267 Q3 (3ᵉ « menus » du chapitre → nombres de 3 chiffres distincts, 9 × 9 × 8 = 648, case contrainte d’abord) ; 1271 Q1 (3ᵉ « mot de passe » → chemins de O(0 ; 0) à B(5 ; 4) : 126 chemins, 60 par C(2 ; 2), 66 l’évitent) ; 1269 Q4 (3ᵉ « boules identiques » → anagrammes de BANANE, 180). Renvoi de 1271 Q4 vers le nouveau titre de 1267 mis à jour.
- Compléments de corrigés pour accompagner les figures : 1266 Q1 (comptage ordonné puis division par 3!), 1263 Q1/Q2, 1265 Q1, 1268 Q5, 1270 Q1.

### Figures (24 fichiers, 29 emplacements)
- **7 existantes revérifiées à l’œil** ; **1 refaite** : `chemin_quadrillage` — le quadrillage (pas de 1 cm) n’était pas aligné sur le chemin (unité 1,05 cm) : le chemin ne suivait pas les lignes. Les 6 autres sont justes et propres.
- **17 ajoutées** (style livre, réponses en vert) : cours `cases_podium` (cases à remplir) et `combinaison_ordres` (les 3! triplets d’une même partie) ; exercices `cases_menu`, `tableau_des` (36 couples), `symetrie_10_3`, `urne_tirage`, `positions_mdp`, `positions_boules`, `positions_banane`, `cases_nombre`, `complementaire_comites`, `chemins_enonce` (énoncé) / `chemins_corrige`, `lot_composants`, `prelevement_positions`, `pascal_a_completer` (énoncé) / `pascal_complete` (corrigé). Triangle de Pascal généré par `math.comb`.
- Les 12 exercices ont désormais une figure (7 sur 10 n’en avaient pas). `lot_composants` refaite plus compacte après lecture de la capture téléphone (trop petite).
- `figures_livre.py` : 0 erreur, largeurs ≤ 900 px.

### Contrôles
- `verif_combinatoire.py` : **178 résultats vérifiés, tout est juste** (section « FINITION » : énumérations itertools des nombres, chemins, anagrammes, prélèvements ; code Python de nouveau-2 **exécuté** et comparé à `math.comb` pour n < 30).
- `verifier_notion.py --navigateur` : **OK, 0 problème** (un code en ligne trop large au téléphone dans nouveau-2 — la liste affichée par `print` — remplacé par du texte).
- `controle_apercu.mjs` : aucun problème ; captures téléphone regardées (nouveau-1, nouveau-2, 1271). Après lecture : tableau d’exécution de nouveau-2 (qui défilait) resserré à 3 colonnes courtes.
