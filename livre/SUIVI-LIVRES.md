# 📚 OptiTAB — Suivi des livres

> **Dernière mise à jour : 25 octobre 2026**
>
> **Statut** : ✅ Terminé · 🟧 En cours · ⬜ À faire
> Un livre est « Terminé » quand son PDF final est livré dans `output/<Matière>/<NN - Niveau>/` (catalogue : `output/README.md`) **et** dans `Desktop/Livres OptiTAB - Lycée/`.
>
> **Rangement (25/10/2026)** : tous les livres sont dans le dossier `livre/` : sources des maths dans `livre-maths/`, de physique-chimie dans `livre-physique/`, puis `livre-anglais/` et `livre-python/` (la colonne « Dossier » donne le nom du dossier dans sa matière). Les PDF sont dans `livre/output/`, un dossier par livre ; après une livraison, lancer `python -X utf8 outils/ranger_pdf.py`. Anciennes versions, sources zippées et rapports : `archives/`.
>
> **Version Excel** : `OptiTAB - Suivi des livres.xlsx` (même dossier) — tableau de bord, un onglet par matière, mises à jour, décisions à prendre, programmes officiels.
>
> **Colonne « Revérifié »** : réservée à votre validation personnelle. Quand vous avez relu et validé un livre,
> remplacez ☐ par ✅ sur sa ligne. Claude ne touche jamais à cette colonne.

## Vue d'ensemble

| Matière | ✅ Terminés | 🟧 En cours | ⬜ À faire | Total |
|---|---:|---:|---:|---:|
| Mathématiques | 18 | 0 | 30 | **48** |
| Physique-chimie | 6 | 0 | 18 | **24** |
| **Total** | **24** | **0** | **48** | **72** |

## Ce qui reste (au 25/10/2026)

**Anglais — Tome 1 « Premiers pas » livré** le 25/10/2026 (458 pages, 20 unités, 5 bilans, 272 pistes audio vérifiées ; reste à mettre les audios en ligne et à fournir l'ISBN).

**Python (livre en anglais, 5 volumes) — Volume 1 « First Steps » démarré** le 25/10/2026 : gabarit, couverture, pages d'introduction et chapitres 1 à 3 (avec solutions et glossaire) envoyés pour validation (PDF sur le Bureau, 96 pages) ; suite après votre accord. Voir §7.

**Toute la scolarité en maths est faite**, de la Petite Section à la Terminale, options Mathématiques complémentaires et Mathématiques expertes comprises (17 livres livrés).
**Physique-chimie Terminale livrée et révisée** le 24/10/2026 (709 pages, figures complétées et chevauchement de légendes corrigé ; PDF classé et copie du Bureau identiques).
**Physique-chimie Quatrième livrée et révisée** le 24/10/2026 (289 pages, 300 exercices corrigés, 209 figures dont 169 ajoutées aux exercices et corrigés, 71 démarches pédagogiques enrichies, 20 défis, quatre bilans et deux évaluations ; PDF classé et copie du Bureau remplacés après contrôle).
**Physique-chimie Troisième / Brevet 2027 livrée et révisée** le 24/10/2026 (327 pages, 239 figures et 15 sujets originaux PC de 30 minutes, dont cinq nouveaux dossiers au format des annales avec documents et corrigés pédagogiques ; copies classée et du Bureau identiques).
**Maths MPSI (prépa, 1re année) livré** le 24/10/2026 (552 pages : les 20 chapitres du programme officiel 2021, 500 exercices corrigés dont 20 défis, et une partie Évaluations de 16 sujets inédits — 6 DS, 4 DM, 2 examens, 4 sujets type concours CCINP / Mines-Ponts / Centrale-Supélec / X-ENS — tous corrigés avec barème ; près de 63 000 vérifications Python ; copies `output` et Bureau identiques).

**Physique-chimie Seconde générale et technologique livrée** le 25/10/2026 (266 pages ; 20 chapitres, 240 exercices, 20 défis et six évaluations corrigés ; programme, calculs, schémas et mise en page contrôlés ; PDF classé et copie du Bureau identiques).

**Physique-chimie Première spécialité livrée** le 24/10/2026 (539 pages : 21 chapitres du programme BO 2019, 315 exercices inspirés des DS et DM avec figures dans les énoncés et les corrigés, corrigés pédagogiques « À retenir » / « Erreur fréquente », 21 défis avec indications, 6 devoirs surveillés de 2 h corrigés avec barèmes, méthode du devoir, fiches expérimentales, données utiles et repères du programme ; toutes les valeurs vérifiées par programme ; copies `output` et Bureau identiques).

1. **En cours** : aucun livre de physique-chimie de lycée en cours (la Première est livrée, voir ci-dessus) ;
2. **Mises à jour pour les nouveaux programmes** (voir §3) — ✅ **les 6 sont faites (23/10/2026)** :
   - 5e, Seconde, Première : audit terminé et PDF relivré (anciennes versions dans `archives/anciennes-versions/`) ;
   - 4e (programme 2027), 3e (programme 2028), Terminale (programme 2027) : **nouvelle édition livrée** dans un dossier séparé ; l’édition actuelle reste valable cette année ;
   - reste pour vous : page ISBN/éditeur de la Terminale (et un nouvel ISBN pour l’édition 2027), et quelques choix éditoriaux signalés dans les rapports (barèmes des sujets blancs, notions gardées en révision).
3. **Maths à faire (30)** :
   - prépa scientifique : 1re année (4 restants ; MPSI livré le 24/10/2026) et 2e année (6) ;
   - prépa économique ECG (4) ;
   - concours : enseignement (5), post-bac (2), écoles d’ingénieurs et ENS (6), écoles de commerce (2), concours lycéens (1).
4. **Physique-chimie à faire (18)** :
   - prépa (9) ;
   - concours de l’enseignement (3) et concours d’écoles d’ingénieurs et ENS (6).

---

# 1. MATHÉMATIQUES

## 1.1 Maternelle

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| Maths — Petite Section (PS) | `livre-maternelle/` (`ps.py`) | ✅ Terminé | ☐ | Livré le 23/10/2026 — 67 pages, 40 activités illustrées + guide de l’adulte, programme 2025 (« avant 4 ans ») |
| Maths — Moyenne Section (MS) | `livre-maternelle/` (`ms.py`) | ✅ Terminé | ☐ | Livré le 23/10/2026 — 85 pages, 53 activités illustrées + guide de l’adulte, programme 2025 (« à partir de 4 ans ») |
| Maths — Grande Section (GS) | `livre-maternelle/` (`gs.py`) | ✅ Terminé | ☐ | Livré le 23/10/2026 — 88 pages, 56 activités illustrées + guide de l’adulte, programme 2025 (« à partir de 5 ans ») |

## 1.2 École élémentaire

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| Maths — CP | `livre-cp/` | ✅ Terminé | ☐ | Livré le 23/10/2026 — 262 pages, 30 chapitres, 270 exercices corrigés, 5 bilans, 360 problèmes oraux, programme du cycle 2 (BO du 31/10/2024) |
| Maths — CE1 | `livre-ce1/` | ✅ Terminé | ☐ | Livré le 23/10/2026 — 277 pages, 32 chapitres, 288 exercices corrigés, 5 bilans, 360 problèmes oraux, programme du cycle 2 (BO du 31/10/2024) |
| Maths — CE2 | `livre-ce2/` | ✅ Terminé | ☐ | Livré le 23/10/2026 — 311 pages, 36 chapitres, 324 exercices corrigés, 5 bilans, 360 problèmes oraux, programme du cycle 2 (BO du 31/10/2024) |
| Maths — CM1 | `livre-cm1/` | ✅ Terminé | ☐ | Livré le 23/10/2026 — 328 pages, 21 chapitres + 21 défis + 2 bilans, programme 2025 |
| Maths — CM2 | `livre-cm2/` | ✅ Terminé | ☐ | Livré le 23/10/2026 — 319 pages, 21 chapitres + 21 défis + 2 bilans, programme 2026 |

## 1.3 Collège

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| Maths — Sixième | `livre-sixieme/` | ✅ Terminé | ☐ | Livré le 23/10/2026 — 342 pages, 21 chapitres (84 sections de cours) + 21 défis + 2 bilans, programme 2025 du cycle 3 |
| Maths — Cinquième | `livre-cinquieme/` | ✅ Terminé | ☐ | Livré le 22/10/2026 ; audit de conformité au programme 2026 (BO n°10 du 05/03/2026) le 23/10/2026 : 117 attendus vérifiés, 14 corrigés, PDF relivré (328 pages, 300 exercices) — ancienne version dans `archives/anciennes-versions/` |
| Maths — Quatrième | `livre-quatrieme/` | ✅ Terminé | ☐ | Livré le 22/10/2026 (édition 2026-2027). **Nouvelle édition programme 2027** livrée le 23/10/2026 : `livre-quatrieme-2027/`, 319 pages, 18 chapitres dont 3 nouveaux (droites remarquables, droite des milieux, triangle rectangle et cercle circonscrit) ; Thalès, cosinus et puissances négatives passent en 3e |
| Maths — Troisième | `livre-troisieme/` | ✅ Terminé | ☐ | Livré le 22/10/2026 — inclut la préparation au Brevet 2027 ; correctif du 23/10/2026 (15 signes % qui coupaient des énoncés au chapitre 6) relivré. **Nouvelle édition programme 2028 / Brevet 2029** livrée le 23/10/2026 : `livre-troisieme-2028/`, 316 pages, nouveau chapitre « Translations et vecteurs » |

## 1.4 Lycée général

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| Maths — Seconde | `livre-seconde/` | ✅ Terminé | ☐ | Livré le 21/10/2026 (+ édition France) ; audit de conformité au programme 2026 (BO n°14 du 02/04/2026) le 23/10/2026 : 178 attendus vérifiés, lacunes comblées, 40 questions flash d’automatismes ajoutées, défaut d’affichage des tableaux corrigé — PDF relivré (285 pages), ancienne version dans `archives/anciennes-versions/` |
| Maths — Première spécialité | `livre-premiere/` | ✅ Terminé | ☐ | Livré le 21/10/2026 (+ édition France, relecture complète) ; audit de conformité au programme 2026 (BO n°14 du 02/04/2026) et à l’épreuve anticipée (note du 11/09/2026) le 23/10/2026 : sujets blancs refaits au format officiel, guide de l’épreuve complété, cours et exercices précisés — PDF relivré (319 pages), ancienne version dans `archives/anciennes-versions/` |
| Maths — Terminale spécialité | `livre-terminale/` | ✅ Terminé | ☐ | 22 chapitres (Analyse, Géométrie, Probabilités, Algorithmique) + 10 sujets type bac corrigés — page ISBN/éditeur à compléter. **Nouvelle édition programme 2027** (BO n°14 du 02/04/2026, bac 2028) livrée le 23/10/2026 : `livre-terminale-2027/`, 398 pages, 23 chapitres (sinus/cosinus, plans perpendiculaires, nouveau chapitre « Ensembles, logique et raisonnement »), sujets avec 2 points de langue — nouvel ISBN à prévoir |
| Maths expertes (option Terminale) | `livre-maths-expertes/` | ✅ Terminé | ☐ | Livré le 23/10/2026 — 126 pages, 12 chapitres, 144 exercices corrigés, 19 figures vectorielles, 9 dossiers et 3 évaluations corrigées avec barèmes ; programme BO 2019, concordance des attendus ; 173 contrôles de calculs clés et relecture visuelle ; PDF classé et copié sur le Bureau |
| Maths complémentaires (option Terminale) | `livre-maths-complementaires/` | ✅ Terminé | ☐ | Livré le 23/10/2026 — 133 pages, 13 chapitres, 156 exercices corrigés, 18 figures vectorielles, 9 dossiers et 3 évaluations corrigées avec barèmes ; programme BO 2019 pour 2026-2027 et concordance avec le programme applicable en 2027 ; 90 contrôles de calculs clés et relecture visuelle ; PDF classé et copié sur le Bureau |

## 1.5 Prépa — CPGE scientifiques, 1re année

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| Maths — MPSI | `livre-mpsi/` | ✅ Terminé | ☐ | Livré le 24/10/2026 — 552 pages, programme officiel 2021 (arrêté du 05/01/2021, BO spécial n°1 du 11/02/2021, annexe MPSI/MP2I) : 20 chapitres (L'essentiel + 25 exercices en 4 rubriques : Applications, Entraînement, Approfondissement, Défi), 500 exercices corrigés pleine largeur avec figures ; partie Évaluations : page « Couverture du programme », 6 DS, 4 DM, 2 examens (semestre 1, fin d'année), 4 sujets type concours (CCINP, Mines-Ponts, Centrale-Supélec avec Python, X-ENS), corrigés avec barème question par question ; ~62 900 vérifications Python (28 scripts) ; PDF `output/Mathématiques/` + Bureau ; reste l'ISBN (décision du propriétaire) |
| Maths — MP2I | — | ⬜ À faire | ☐ | |
| Maths — PCSI | — | ⬜ À faire | ☐ | |
| Maths — PTSI | — | ⬜ À faire | ☐ | |
| Maths — BCPST 1 | — | ⬜ À faire | ☐ | |

## 1.6 Prépa — CPGE scientifiques, 2e année

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| Maths — MP | — | ⬜ À faire | ☐ | |
| Maths — MPI | — | ⬜ À faire | ☐ | |
| Maths — PC | — | ⬜ À faire | ☐ | |
| Maths — PSI | — | ⬜ À faire | ☐ | |
| Maths — PT | — | ⬜ À faire | ☐ | |
| Maths — BCPST 2 | — | ⬜ À faire | ☐ | |

## 1.7 Prépa — CPGE économiques (ECG)

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| Maths approfondies — ECG 1 | — | ⬜ À faire | ☐ | |
| Maths appliquées — ECG 1 | — | ⬜ À faire | ☐ | |
| Maths approfondies — ECG 2 | — | ⬜ À faire | ☐ | |
| Maths appliquées — ECG 2 | — | ⬜ À faire | ☐ | |

## 1.8 Concours et examens

### Concours de l'enseignement

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| CRPE — maths (professeur des écoles) | — | ⬜ À faire | ☐ | |
| CAPES — maths | — | ⬜ À faire | ☐ | |
| CAPLP — maths-sciences | — | ⬜ À faire | ☐ | Couvre maths + physique-chimie (lycée professionnel) |
| Agrégation externe — maths | — | ⬜ À faire | ☐ | |
| Agrégation interne — maths | — | ⬜ À faire | ☐ | |

### Concours post-bac (entrée en école après le bac)

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| Concours ingénieurs post-bac (Avenir, Puissance Alpha, GEIPI-Polytech) | — | ⬜ À faire | ☐ | |
| Concours commerce post-bac (Sésame, Accès) | — | ⬜ À faire | ☐ | |

### Concours CPGE — écoles d'ingénieurs et ENS

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| X-ENS — maths | — | ⬜ À faire | ☐ | Polytechnique + ENS (Ulm, Lyon, Paris-Saclay, Rennes) |
| Mines-Ponts — maths | — | ⬜ À faire | ☐ | |
| Centrale-Supélec — maths | — | ⬜ À faire | ☐ | |
| CCINP — maths | — | ⬜ À faire | ☐ | |
| e3a-Polytech & Banque PT — maths | — | ⬜ À faire | ☐ | |
| Agro-Véto & G2E — maths (BCPST) | — | ⬜ À faire | ☐ | |

### Concours CPGE — écoles de commerce (ECG)

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| BCE & Ecricome — maths approfondies | — | ⬜ À faire | ☐ | |
| BCE & Ecricome — maths appliquées | — | ⬜ À faire | ☐ | |

### Concours lycéens

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| Concours général & Olympiades — maths | — | ⬜ À faire | ☐ | Concours général des lycées, Olympiades nationales de Première |

> Le Brevet est déjà couvert par le livre de Troisième, le Bac par les 10 sujets du livre de Terminale.

---

# 2. PHYSIQUE-CHIMIE

## 2.1 Collège (cycle 4)

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| Physique-chimie — Cinquième | `livre-pc-cinquieme/` | ✅ Terminé | ☐ | Livré et révisé le 24/10/2026 — 346 pages, 20 chapitres, 300 exercices, 20 défis et quatre bilans ; 194 figures vectorielles distinctes, 61 énoncés et 85 corrigés d’exercices illustrés, figures complémentaires dans les défis et bilans utiles, 27 démarches enrichies ; 763 contrôles du PDF et 471 contrôles de révision sans échec ; 29 planches et 18 preuves Poppler finales inspectées ; PDF classé et copie du Bureau identiques |
| Physique-chimie — Quatrième | `livre-pc-quatrieme/` | ✅ Terminé | ☐ | Livré et révisé le 24/10/2026 — 289 pages, 20 chapitres, 300 exercices corrigés (600 questions), 209 figures vectorielles dont 169 nouvelles pour exercices, défis et bilans ; 54 énoncés et 111 corrigés illustrés, 71 démarches supplémentaires et trois explications de bilans/évaluations ajoutées ; 20 investigations et 20 défis corrigés, 4 bilans et 2 évaluations avec barèmes ; programme cycle 4 BO 2020 vérifié pour 2026-2027, progression annuelle explicitée ; 1 419 contrôles réussis dont 209 calculs, 25 planches et 21 preuves Poppler relues, longueurs à l’échelle mesurées dans le PDF ; PDF classé et copie du Bureau remplacés, ancienne édition de 236 pages archivée |
| Physique-chimie — Troisième | `livre-pc-brevet/` | ✅ Terminé | ☐ | Livré et révisé le 24/10/2026 — 327 pages, 18 chapitres, 270 exercices corrigés, 18 investigations et 18 défis, 239 figures ; 15 sujets originaux PC de 30 min, dont cinq nouveaux dossiers au format des annales, avec 45 questions et 28 figures supplémentaires ; corrigés expliqués, barèmes /10 et remédiation ; 3 240 contrôles du PDF dont 241 calculs, 533 contrôles de révision et 208 contrôles des nouveaux sujets sans échec ; programme cycle 4 et format DNB vérifiés sur sources officielles ; PDF classé et copie du Bureau identiques |

## 2.2 Lycée général

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| Physique-chimie — Seconde | `livre-pc-seconde/` | ✅ Terminé | ☐ | Livré le 25/10/2026 — 266 pages, programme BO 2019 vérifié sur Éduscol en 2026 ; 20 chapitres, 240 exercices corrigés, 20 défis avec indications, 6 évaluations de 90 min avec barèmes, 4 ateliers numériques ; 48 sources de figures et 180 insertions dans le cours, les énoncés et les solutions ; 795 contrôles de contenu, relecture des pages et contrôles de débordement ; PDF classé et copie du Bureau identiques |
| Physique-chimie — Première spécialité | `livre-pc-premiere/` | ✅ Terminé | ☐ | Livré le 24/10/2026 — 539 pages, programme BO spécial n°1 du 22/01/2019 (inchangé en 2026) : 21 chapitres, 315 exercices corrigés (figures dans les énoncés et les corrigés, notes « À retenir » et « Erreur fréquente »), 21 défis avec indications, 6 devoirs surveillés de 2 h corrigés avec barèmes, méthode du devoir, capacités expérimentales et 4 fiches, données utiles et repères du programme ; toutes les valeurs vérifiées par programme. PDF : `output/Physique-chimie/` et Bureau (`Livres OptiTAB - Lycée`) |
| Physique-chimie — Terminale spécialité | `livre-pc-terminale/` | ✅ Terminé | ☐ | Livré le 23/10 et révisé le 24/10/2026 — 709 pages, 27 chapitres, 405 exercices corrigés, 27 défis et six sujets type bac ; 18 constructions nouvelles, 23 corrigés et trois énoncés enrichis de figures, légendes de 12.11 réajustées, explications RC précisées ; 28 scripts numériques et 54 contrôles complémentaires réussis ; 36 planches et 25 preuves Poppler finales inspectées ; PDF classé et copie du Bureau identiques |

## 2.3 Prépa — CPGE scientifiques

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| Physique-chimie — MPSI | — | ⬜ À faire | ☐ | |
| Physique-chimie — PCSI | — | ⬜ À faire | ☐ | |
| Physique-chimie — PTSI | — | ⬜ À faire | ☐ | |
| Physique-chimie — BCPST 1 | — | ⬜ À faire | ☐ | |
| Physique — MP / MPI | — | ⬜ À faire | ☐ | |
| Physique-chimie — PC | — | ⬜ À faire | ☐ | |
| Physique — PSI | — | ⬜ À faire | ☐ | |
| Physique — PT | — | ⬜ À faire | ☐ | |
| Physique-chimie — BCPST 2 | — | ⬜ À faire | ☐ | |

## 2.4 Concours

### Concours de l'enseignement

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| CAPES — physique-chimie | — | ⬜ À faire | ☐ | |
| Agrégation externe — physique | — | ⬜ À faire | ☐ | |
| Agrégation externe — chimie | — | ⬜ À faire | ☐ | |

### Concours CPGE — écoles d'ingénieurs et ENS

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| X-ENS — physique | — | ⬜ À faire | ☐ | |
| Mines-Ponts — physique-chimie | — | ⬜ À faire | ☐ | |
| Centrale-Supélec — physique-chimie | — | ⬜ À faire | ☐ | |
| CCINP — physique-chimie | — | ⬜ À faire | ☐ | |
| e3a-Polytech & Banque PT — physique | — | ⬜ À faire | ☐ | |
| Agro-Véto & G2E — physique-chimie (BCPST) | — | ⬜ À faire | ☐ | |

---

# 3. Points de vigilance — programmes officiels (au 24/10/2026)

- **Maternelle** : programme publié au BO n°41 du 31/10/2024 (rentrée 2025), version consolidée du BO n°19 du 07/05/2026. → Les cahiers PS, MS et GS sont alignés.
- **CP, CE1, CE2** : programme du cycle 2 publié au BO du 31/10/2024, applicable depuis la rentrée 2025. → Les livres CP, CE1 et CE2 sont alignés.
- **CM1, CM2** : programmes 2025 (arrêté du 10/04/2025, BO n°16 du 17/04/2025) — CM1 appliqué depuis la rentrée 2025, CM2 depuis la rentrée 2026. → Les livres CM1 et CM2 sont déjà alignés.
- **Sixième** : programme 2025 du cycle 3 en vigueur depuis la rentrée 2025. → Le livre de 6e (livré le 23/10/2026) le suit.
- **Collège (cycle 4)** : nouveau programme de maths (arrêté du 18/02/2026, BO n°10 du 05/03/2026), applicable en **5e à la rentrée 2026**, en 4e à la rentrée 2027, en 3e à la rentrée 2028. → Livre de 5e audité et relivré le 23/10/2026 ; nouvelles éditions de 4e (programme 2027) et de 3e (programme 2028) livrées le 23/10/2026.
- **Lycée** : nouveaux programmes de maths de Seconde et Première (BO n°14 du 02/04/2026), applicables depuis la **rentrée 2026** ; Terminale à la rentrée 2027. Nouvelle **épreuve anticipée de maths** en fin de Première. → Seconde et Première audités et relivrés le 23/10/2026 ; le programme de Terminale (NOR MENE2602919A, même BO) est publié : nouvelle édition de Terminale livrée le 23/10/2026.
- **Options de Terminale** : Mathématiques complémentaires suit le programme BO 2019 pour 2026-2027 ; le nouveau programme (BO du 02/04/2026, NOR MENE2902920A) s'applique à la rentrée 2027 et fait l'objet d'une concordance dans le manuel. Mathématiques expertes conserve le programme BO 2019. → Les deux manuels complets sont livrés le 23/10/2026.
- **Physique-chimie cycle 4** : les pages Éduscol consultées le 24/10/2026 confirment le programme du BO du 30/07/2020 pour 2026-2027. La répartition entre 5e, 4e et 3e relève de la progression choisie. → Manuels de Quatrième et de Troisième / Brevet 2027 livrés le 24/10/2026. Les sujets blancs de 3e suivent la note du 11/09/2026, NOR MENE2623228N : volet PC de 30 min, /10 dont 1 point de langue ; l’épreuve complète de sciences comporte deux disciplines en une heure.
- **Physique-chimie Terminale** : programme de 2019 (BO spécial n°8 du 25/07/2019) toujours en vigueur ; épreuve de la session 2027 cadrée par la note de service du 11/09/2026. Avant d'écrire la PC de Seconde/Première, vérifier si le BO du 02/04/2026 les concerne aussi.

---

# 4. Extensions possibles (non comptées dans le suivi, à décider plus tard)

- Lycée technologique : maths STI2D / STL / STMG ; physique-chimie STI2D / STL
- Lycée professionnel : CAP et Bac pro (maths – sciences)
- Enseignement scientifique Première / Terminale ; Sciences et technologie 6e
- CPGE à petits effectifs : TSI 1 & 2, TPC, TB, ATS ; ECT 1 & 2 ; B/L 1 & 2 ; D1 / D2
- Concours ludiques et divers : Kangourou, Castor informatique, concours administratifs avec épreuves de maths
- Supérieur : BTS, BUT, Licence L1–L3

---

# 5. Collection « L'essentiel » — fiches de révision (en plus des 72 livres)

Une fiche de 3 à 4 pages par chapitre : cours, formules, schémas, méthodes, pièges, rédaction type bac et check-list. Gabarit propre à la collection (`optitab-fiches.sty`), même charte que les livres.

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| L'essentiel — Maths Terminale spécialité | `livre-fiches-terminale/` | 🟧 En cours | ☐ | Démarré le 24/10/2026 — 23 fiches prévues (même numérotation que le livre de Terminale, + fiche 23 logique) ; gabarit, couverture, sommaire, mode d'emploi et fiche 1 « Suites numériques » (4 pages, 5 schémas, 48 vérifications Python) livrés pour validation : PDF sur le Bureau « OptiTAB - L'essentiel - Mathématiques Terminale (fiche 1 pour validation).pdf » ; suite après votre accord |

---

# 6. Collection « Anglais » — méthode complète pour apprendre de zéro (en plus des 72 livres)

Méthode pour francophones débutants, avec audio (un QR code à côté de chaque activité, pistes en version lente et normale), fil rouge : Léa, graphiste lyonnaise installée à New York. Gabarit propre à la collection (`livre-anglais/optitab-anglais.sty`), même charte que les livres. Voix de synthèse neuronales (Kokoro, licence Apache 2.0, usage commercial autorisé), chaque piste réécoutée et comparée au texte par reconnaissance vocale.

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| Anglais — Tome 1 « Premiers pas » (A1, débutant) | `livre-anglais/` (`tome-1.tex`) | ✅ Terminé | ☐ | Livré le 25/10/2026 — 458 pages : 20 unités en 5 parties (2 dialogues bilingues, vocabulaire avec phonétique, grammaire, prononciation, culture américaine, 12 exercices corrigés et un test express par unité), 5 bilans notés sur 20, corrigés pédagogiques et transcriptions de tout le tome, mémento de grammaire, 60 verbes irréguliers, lexique de 553 mots. 272 pistes audio (2 h 41), chacune réécoutée par reconnaissance vocale ; 1 428 vérifications de contenu. PDF dans output/Anglais et sur le Bureau, avec le dossier d'audios. Audios à mettre en ligne sur optitab.net/audio/anglais/t1 pour activer les QR codes ; ISBN à fournir |
| Anglais — Tome 2 « Les bases solides » (A2) | — | ⬜ À faire | ☐ | Après le tome 1 |
| Anglais — Tome 3 « Communiquer avec aisance » (B1) | — | ⬜ À faire | ☐ | |
| Anglais — Tome 4 « Parler couramment » (B2) | — | ⬜ À faire | ☐ | |
| Anglais — Tome 5 « Maîtriser l'anglais » (C1) | — | ⬜ À faire | ☐ | |

---

# 7. Collection « Python » — la méthode complète, en anglais (en plus des 72 livres)

Livre rédigé **en anglais** pour apprendre à programmer en Python de zéro jusqu'au niveau professionnel, en 5 volumes (Beginner → Expert). Gabarit propre à la collection (`livre-python/optitab-python.sty`), même charte OptiTAB que les autres livres. Chaque programme imprimé est exécuté et sa sortie comparée caractère par caractère à celle de Python 3.13, telle qu'IDLE l'affiche (`livre-python/outils/verifier_code.py`). Code téléchargeable par QR code (dossier `tome-1/code/`, à mettre en ligne sur optitab.net/python/t1).

| Livre | Dossier | Statut | Revérifié | Notes |
|---|---|---|---|---|
| Python — Volume 1 « First Steps » (Beginner) | `livre-python/` (`tome-1.tex`) | 🟧 En cours | ☐ | Démarré le 25/10/2026 — plan complet (20 chapitres en 5 parties, 5 projets guidés, 5 checkpoints) ; gabarit, couvertures, pages d'introduction, chapitres 1 à 3 avec 36 exercices, solutions pédagogiques et glossaire (96 pages, 529 vérifications de code) envoyés pour validation : PDF sur le Bureau « OptiTAB - Python - Volume 1 (chapitres 1 à 3 pour validation).pdf » ; suite après votre accord |
| Python — Volume 2 « Solid Foundations » (Elementary) | — | ⬜ À faire | ☐ | Modules, bibliothèque standard, tests, outils professionnels (VS Code, Git, venv) |
| Python — Volume 3 « Thinking in Objects » (Intermediate) | — | ⬜ À faire | ☐ | Programmation orientée objet, code « pythonique », grands projets |
| Python — Volume 4 « Python at Work » (Advanced) | — | ⬜ À faire | ☐ | Automatisation, données (pandas, NumPy, Matplotlib), SQL, API et applications web |
| Python — Volume 5 « Mastering Python » (Expert) | — | ⬜ À faire | ☐ | Performance, concurrence, architecture, packaging, CI, algorithmique |
