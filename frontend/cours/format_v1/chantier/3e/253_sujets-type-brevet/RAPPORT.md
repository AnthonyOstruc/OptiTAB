# Rapport — notion 253 « Sujets type brevet » (3e, thème « Préparation au brevet »)

**État : PRÊT** (03/11/2026). Partie A (cours, fiche, sujets 01 à 05) et partie B (sujets 06 à 10, Id 2553 à 2557, puis contrôle final de toute la notion) finies. Rien n'a été écrit en base, aucune commande git, seul ce dossier a été modifié. ⚠ Publication : la fiche a changé de titre → `titres_docs.py` (lancé par `publier_lot.ps1`).

---

## Partie A (cours, fiche, sujets 01 à 05) — compte rendu et passation

### A1. Format officiel de l'épreuve (vérifié sur les textes)

**Texte de référence** : note de service du 2-9-2025, NOR **MENE2515977N**, « Modalités d'attribution du diplôme national du brevet à compter de la session 2026 », BO n° 33 du 4 septembre 2025, § 3.1.2 (lu en PDF, copie académique d'Orléans-Tours : `pedagogie.ac-orleans-tours.fr/documents/pdf/dnb_2026_modalites_d_attribution_bo_no33_du_04-09-2025.pdf`). Il dit, pour l'épreuve écrite de mathématiques :
- durée **2 heures**, **coefficient 2**, note sur **20** ; brouillon autorisé ; calculatrice **seulement en partie 2** ;
- **Partie 1 — Automatismes : 6 points, 20 minutes**, sans calculatrice ;
- **Partie 2 — Raisonnement et résolution de problèmes : 14 points, 1 h 40** ; « la clarté et la précision des raisonnements ainsi que, plus largement, la qualité de la rédaction […] **évaluée sur 2 points** » ; essais et démarches non aboutis pris en compte ; « toutes les réponses doivent être justifiées sauf indication contraire » ; exercices indépendants, « toutes les modalités possibles » ;
- programme : cycle 4, « **sur le programme de la classe de troisième à partir de la session 2027** » ;
- note finale du DNB : épreuves terminales 60 %, moyenne de l'année de 3e 40 %, diplôme à 10/20 (même note).

**Sujets réels de la session 2026** (education.gouv.fr, `diplome-national-du-brevet-2026-mathematiques-serie-generale-518132.pdf` et `-517553.pdf` ; Amérique du Nord 2026) : en-tête « Partie 1 – Automatismes 6 points, 20 min (calculatrice interdite) / Partie 2 – 14 points, 1 h 40 (calculatrice autorisée) ; à l'issue de la partie 1, les copies sont ramassées ; calculatrice avec mode examen actif ou sans mémoire type collège ; dictionnaire interdit ». Partie 1 : **8 ou 9 questions**, « recopier le numéro et la réponse ; aucune justification ; **pour les QCM, une seule réponse est exacte** » (QCM et questions ouvertes mélangés). Partie 2 : 3 ou 4 exercices dont les points totalisent **12** (ex. 4 + 3,5 + 4,5 ; 2,5 + 3 + 4 + 2,5), **+ 2 points de rédaction = 14**.

**Autres sources** : BO n° 13 du 27 mars 2026 (NOR MENE2607843N : « les épreuves de mathématiques du DNB […] comportent désormais une première partie consacrée aux automatismes » ; sujets zéro et liste indicative sur Éduscol) ; **liste indicative d'automatismes**, Éduscol, octobre 2025 (`eduscol.education.fr/document/67781/download`) : nombres et calculs, espace et géométrie, données et probabilités, proportionnalité et fonctions, algorithmique (interpréter une suite d'instructions). Nouveau programme de cycle 4 (BO n° 10 du 5 mars 2026) : en 3e seulement à la rentrée 2028 → la session 2027 reste sur le programme actuel.
Les pages HTML d'education.gouv.fr et d'eduscol (403 aux robots) n'ont pas pu être lues directement ; les PDF officiels, si.

**Corrections apportées par rapport à la version en ligne** (qui annonçait 4 exercices × 3,5 = 14) :
- partie 2 = **exercices sur 12 points + 2 points de rédaction** (tableau de barème dans chaque énoncé, rubrique « Rédaction (2 points) » dans chaque corrigé) ;
- la phrase « la seconde partie ne comporte pas de QCM » (non officielle) est supprimée ; la partie 1 contient désormais des **QCM** (2 ou 3 par sujet), comme les sujets réels ;
- les **inéquations** (sujet 05 : « résoudre 20 + 10n < 15n ») sont **hors programme de 3e** (aucune notion de 3e du site n'en contient) : remplacées par une équation + lecture graphique / raisonnement sur les valeurs ;
- en-tête : « sujet conforme au format officiel, en vigueur depuis la session 2026 » (le format 2026 vaut pour 2027 : aucun texte contraire).
- Barème de la partie 1 : les sujets officiels ne détaillent pas les points par question ; j'indique « 0,6 point par question (barème indicatif) » pour 10 questions.

### A2. Cours 248 et fiche 168

- **Cours « Méthode : réussir l'épreuve de mathématiques du brevet »** (titre inchangé), réécrit : I. l'épreuve en bref (définition, tableau, frise) ; II. automatismes par thème (6 encadrés d'exemples tirés des sujets) ; III. méthode de résolution en 5 temps + figure « données → propriété → conclusion » + tableau « repérer l'outil » ; IV. rédactions modèles (Pythagore, Thalès avec figure, trigonométrie) + attentes du correcteur ; V. gestion du temps ; VI. dix pièges ; VII. check-list du jour J.
- **Fiche** : titre changé en **« Résumé : l'essentiel pour le jour du brevet »** (comme la fiche bac 308). ⚠ `importer_v1.py` n'importe pas les titres : lancer `titres_docs.py` (fait par `publier_lot.ps1`). Contenu : nombres, calcul littéral (identités), proportionnalité/pourcentages (tableau), fonctions, géométrie plane (Pythagore, Thalès + figure, trigonométrie + figure), volumes (tableau), statistiques et probabilités, Scratch et rédaction.

### A3. Sujets 01 à 05 (Id 2548 à 2552, titres inchangés)

Tous réécrits (la conversion automatique était inutilisable : partie 2 indentée de 3 espaces, encadrés mal fermés, corrigés de 1 ligne). Thèmes conservés, données vérifiées, questions complétées.

| Sujet | Partie 2 (12 pts) | Scratch |
|---|---|---|
| 01 | carnets (arithmétique, 3) ; voile (Pythagore, Thalès, aires k², 3,5) ; loueurs (fonctions, 3) ; scores et tirage avec remise (2,5) | non |
| 02 | abri (Pythagore, tangente, %, 3) ; bouteille (cylindre, k³, 3) ; script de carrés (3) ; jeu roue + sac (3) | oui (bloc perso + tracé) |
| 03 | budget (%, 3) ; trajet (lecture graphique, vitesses, 3) ; statue (Thalès, Pythagore, tangente, 3,5) ; tableur, fréquences, probabilités (2,5) | non |
| 04 | jardin (Pythagore, aires, arrondis, 3) ; citerne (cylindre, fonction linéaire, 3) ; charpente (médiatrice, sinus, cosinus, angles, 3) ; programme de calcul (3) | oui (programme de calcul) |
| 05 | billetterie (fonctions + question algorithmique à trou, 3,5) ; scène (échelle, aires ÷ 50², Pythagore, tangente, 3) ; fréquentation (statistiques, %, 2,5) ; tombola (probabilités, équation, 3) | oui (case A à compléter) |

Partie 1 : 10 automatismes par sujet, pris dans la liste Éduscol (priorités, fractions, puissances, écriture scientifique, arithmétique, développer/factoriser, équations, %, conversions, image/antécédent, Pythagore, cosinus, transformation, médiane, étendue, moyenne, probabilité).
Non couverts par 01–05 (à placer dans 06–10) : **boule, cône, pyramide**, homothétie / agrandissement d'une figure, triangles semblables, réciproque de Thalès, développement d'un carré (a + b)², tableur avec formule de calcul, Scratch avec « si … alors » ou « répéter jusqu'à ».

**Structure type d'un énoncé** (à reprendre telle quelle) :
1. `::: remarque Consignes de l'épreuve` (durée, 2 parties, ramassage, calculatrice, « format officiel en vigueur depuis la session 2026 ») ;
2. tableau `| Partie | Contenu | Points |` : Partie 1 = 6, Exercices (somme 12), Rédaction = 2, **Total** = 20 ;
3. `## Partie 1 : Automatismes (6 points, 20 minutes)` + consigne officielle + `### Question 1` … `### Question 10` (QCM : liste `- **A.** …`) ;
4. `## Partie 2 : Raisonnement et résolution de problèmes (14 points, 1 h 40)` + consigne officielle (justifier, 2 points de rédaction, trace de recherche) ;
5. `### Exercice N : Titre (x points)` + contexte + questions `1.` `2.` (sous-questions `   - a)`) ; figures de données `[IMAGE_n]`.

**Structure type d'un corrigé** (`Étapes:`) :
- `::: conseil Comment utiliser ce corrigé` ;
- `## Partie 1 : Automatismes (6 points)` + `::: point Barème` (« $0{,}6$ point par question (barème indicatif) ») ; puis `## Question k : …` avec `::: methode`, `::: etape`, `::: resultat` (QCM : « Réponse **B** : … »), `::: attention` (distracteur expliqué) ;
- `## Exercice N : Titre (x points)` + `::: point Barème` (« Q1 : $0{,}75$ point ; Q2 : … » ou « $0{,}5$ point par question ») ; `## Question k : …` (numérotation **reprise à 1 dans chaque exercice** : le moteur n'accepte pas « Question 2.3 ») ; rédaction attendue au brevet dans les étapes (« Dans le triangle … rectangle en …, d'après le théorème de … ») ; `::: attention` ou `::: retenir` ; figure de corrigé entre l'étape et le résultat ;
- `## Rédaction (2 points)` + `::: retenir Ce qui est évalué sur 2 points`.
- `Solution:` : `**Partie 1**` + liste 1–10, puis `**Exercice N**` + liste des réponses courtes.

### A4. Figures (`figures/figures.py`, 45 placements, 43 PNG, 0 image en ligne conservée sur 01–05)

- **Toutes les anciennes images matplotlib des sujets 01–05 et du cours sont remplacées** (19 images en ligne → 43 figures neuves) ; tableaux de scores et tableur passés en tableaux natifs.
- **Nommage** : `brevet_3e_sNN_<objet>.png` (énoncé, données seules) et `brevet_3e_sNN_<objet>_corrige.png` (réponses en vert otGreenDark) ; cours/fiche : `cours_…`, `fiche_…`. verif_253.py contrôle le préfixe `brevet_3e_sNN_` de chaque figure de sujet.
- **Aides réutilisables** dans figures.py (docstring) : `tri_rect` (triangle rectangle, côtés nommés, angle marqué), `lseg`/`cote_seg` (étiquettes et cotes ; `cote_a_cote=True` pour une cote verte écrite à côté de la flèche), `arc`, `angle_droit`, `arbre`/`deux_etapes` (arbres, repris de 243), `cylindre` (repris de 247, option `eau=` pour un niveau d'eau), `barres`, `camembert` (repris de 242), `graphe` (pgfplots ; style `Q1` = graduations des ordonnées centrées, pour un premier quadrant), `roue_lettres`.
- **Scratch** : `figures/scratch.py` = **copie** du module de la notion 248 (`chantier/3e/248_*/figures/scratch.py`, version du 03/11 après-midi, empreinte md5 d902667…) — l'original n'a pas été modifié. Vrais blocs Scratch 3 (formes, couleurs, encoches, trous « A » pointillés, solution verte au corrigé) ; `executer()` exécute chaque script dans verif_253.py ; `figure_trace()` dessine le tracé du lutin issu de l'exécution. `figures/controle_scratch.py` (copie du 248) recompile les figures de blocs en fonds blancs : **0 texte sur un trait** (`python controle_scratch.py brevet_3e_s02_script …`). Les figures de blocs sont dans `TOLERE` (même raison écrite que dans 248) ; `scripts_fig(nom, scripts)` les enregistre.
- `TOLERE` aussi pour `brevet_3e_s03_symetrie(_corrige)` : pastilles ① ② et nom de O sur fond blanc posés sur le quadrillage clair.
- **Largeurs** : pour la lisibilité sur téléphone, les graphiques ont été réduits à `width=6.4cm` et les figures de texte (frise, démarche) à ≤ 7 cm : au-delà de ~750 px, l'aperçu téléphone les rétrécit nettement.

### A5. Contrôles

- `verif_253.py` : **406 contrôles, 0 erreur** (`verif_log.txt`) — sympy pour chaque calcul des sujets, du cours et de la fiche ; arrondis recalculés ; **scripts Scratch exécutés** (S02 : 16 côtés, c = 30, position (90 ; 0), distance stylo relevé déduite des positions ; S04 : entrées 5, −3, 3, 7, −7 ; S05 : entrées 7, 3, 0) ; **barème relu dans le texte** (tableau = 6 + 12 + 2 = 20, titres d'exercices de l'énoncé et du corrigé, blocs Barème question par question, nombre de questions posées = corrigées, 10 automatismes) ; cohérence figures/texte (positions, angles, H sur le rayon, hauteur d'eau…) ; absence d'indentation de conversion.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (toute la notion ; les 14 images en ligne conservées sont celles des sujets 06–10, inchangés).
- Captures téléphone regardées : cours (8 écrans), fiche (4), sujet 01 énoncé (5) et corrigé (13), sujets 02 à 05 énoncés et corrigés. Corrections faites après relecture : tableau du cours à 3 colonnes, figures trop larges réduites, identités et formules trigonométriques de la fiche sur une ligne chacune, tableau des volumes dédoublé, 8 formules de corrigés trop larges découpées (équivalences « ⟺ » remplacées par des lignes alignées), tableau de suivi Scratch simplifié, espaces insécables (« 1 h 40 », « $90$ »)…
- Le module `scratch.py` copié est identique (md5) à la version finale de la notion 248 (importée à 15 h 22).
- Sujets 06–10 : **strictement inchangés** (comparaison octet par octet avec l'export converti).

### A6. Pour l'agent de la partie B (sujets 06 à 10)

1. Ne pas relancer `convertir_notion.py`. Travailler directement dans `exercices.txt` (blocs Id 2553 à 2557) ; ne pas toucher aux blocs 2548–2552.
2. Reprendre la structure type A3 (copier un sujet de la partie A comme gabarit) et le barème 6 + 12 + 2.
3. **Pièges de la conversion** : partie 2 indentée de 3 espaces (rend les lignes en bloc de code ou texte décalé) ; `**Partie 1 — Question 1**` en gras au lieu de titres ; encadrés `::: resultat` fermés après le titre suivant ; `::: etape $…$` (formule en titre d'étape) ; questions numérotées « 1.2 » (le moteur lit « Question 1 » puis « .2 ») ; « À retenir » en gras hors encadré.
4. Figures : ajouter les fonctions dans `figures.py` (sections `SUJET 06`…), noms `brevet_3e_s06_…` ; compléter `figures/correspondance.json` ; scripts Scratch avec `scripts_fig` ; contrôle `python figures/controle_scratch.py <noms>`.
5. `verif_253.py` : ajouter `sujet_06()` … `sujet_10()` sur le modèle (appeler `bareme(Id)` en premier) et les ajouter à la liste du `__main__`.
6. Hors programme à éviter : inéquations ; à couvrir : voir la liste « non couverts » en A3.
7. Fin : `verifier_notion.py --navigateur` = 0 problème, captures téléphone, `etat.json` → « pret », section « Partie B » de ce rapport.

### A7. Remarques pour l'orchestrateur

- **Titre de la fiche** changé (voir A2) : appliqué par `titres_docs.py`.
- Les images en ligne du cours (`raisonner_3e_demarche.png`) et des sujets 01–05 seront remplacées à l'import (aucune n'est conservée).
- Outil : le titre `## Question 2.3` n'est pas reconnu par le moteur (regex `Question\s+([A-Z]?\d+[a-z]?)`) ; d'où la numérotation 1, 2, 3… reprise dans chaque exercice.

---

## Partie B (sujets 06 à 10 et contrôle final) — compte rendu

### B1. Sujets 06 à 10 (Id 2553 à 2557, titres inchangés)

Les cinq sujets sont **réécrits en entier** sur le gabarit de la partie A (consignes officielles, tableau 6 + 12 + 2 = 20, 10 automatismes dont 2 QCM, 4 exercices, corrigé « méthode / étapes / résultat / attention ou à retenir », barème question par question, rubrique « Rédaction (2 points) », solution courte par partie). La conversion automatique (partie 2 indentée, encadrés cassés, corrigés d'une ligne, « Question 1.2 ») est entièrement remplacée ; les lignes `Image:` (anciennes images matplotlib) sont supprimées.

| Sujet | Partie 2 (12 pts) | Scratch |
|---|---|---|
| 06 Aquarium et laboratoire | aquarium (pavé, %, masse, hauteur d'eau, **boule** qui fait monter l'eau, 3,5) ; bactéries (puissances de 2, proportionnalité ?, écriture scientifique, 3) ; microscope (**agrandissement**, aires × k², µm, 2,5) ; simulation de la croissance (3) | oui : **« répéter jusqu'à »** (suivi des variables, changement de seuil, culture qui triple) |
| 07 Le parc d'attractions | grande roue (périmètre, vitesses, **rotation** de 60°, cosinus, 3) ; grand huit (fonction non affine, lectures graphiques, antécédents, 3) ; glaces (**cône + demi-boule**, réduction k³, 3) ; pêche aux canards (probabilités, équation, fréquence et fluctuation, 3) | non |
| 08 La course solidaire | parcours (**réciproque de Pythagore**, durées, heure, tangente, 3,5) ; dons (fonction affine, équation, non-proportionnalité, 3) ; temps de course (médiane, moyenne, étendue, 2,5) ; script de chronométrage (3) | oui : **« si … alors … sinon »** (condition stricte, « non (v < 12) ») |
| 09 L'énergie à la maison | panneaux solaires (sinus, cosinus, aire, rentabilité, 3) ; deux offres (fonctions affines, équation, graphique, 3) ; combles (**pyramide**, Pythagore, pourcentage, isolant, 3) ; relevé de consommation (**tableur avec formules** `=B2*0,25`, `=SOMME(B2:B13)`, moyenne, médiane, %, 3) | non |
| 10 En mer | phare (tangente, deux angles, vitesse, nœuds, 3,5) ; traversée de l'Atlantique (**sphère**, latitude, longitude, arc d'équateur, volume de la Terre, 3) ; voile (Pythagore, **réciproque de Thalès**, Thalès, **triangles semblables / réduction**, aires × k², 3) ; marée (lecture graphique, seuil, 2,5) | non |

Automatismes (partie 1) nouveaux par rapport à 01–05 : **(a + b)²** et (a − b)², équation produit nul, x² = 49, puissances (quotient, puissance d'une puissance), fraction irréductible, nombres premiers, PGCD, critère de divisibilité par 9, échelle, énergie (kWh), conversions de durées et de vitesses, coefficient d'une fonction affine, **rotation de 90°** (S07) et **homothétie de rapport −2** (S10) sur quadrillage.
Couverture de la liste « à couvrir » de A3 : boule, cône, pyramide, homothétie / agrandissement, triangles semblables, réciproque de Thalès, (a + b)², tableur avec formule, Scratch « si … alors » et « répéter jusqu'à » : **tout est couvert**. Avec 01–05, les 10 sujets couvrent tout le programme de 3e ; 5 sujets sur 10 contiennent du Scratch (02, 04, 05, 06, 08).

**Corrections par rapport à l'ancienne version** (outre la remise au format) :
- S10 : la traversée « de 10° O à 20° E sur l'équateur » passait au milieu de l'Afrique (Gabon, Congo) → **de 40° O à 10° O** (océan Atlantique), écart toujours 30°.
- S08 : l'ancienne question « pour quelles durées l'objectif est-il atteint ? » demandait une **inéquation** (hors programme de 3e) → raisonnement « plus courte ou plus longue que 54 min ? ».
- S08 : le script calcule `648 / t` (et non `10,8 / t * 60`) : avec les nombres à virgule, `10,8 / 54 * 60` vaut 12,000 000 000 000 002 en machine et Scratch afficherait « Objectif atteint » — le calcul est exact avec 648.
- S09 : « écrire √50 sous la forme a√2 » (hors programme de 3e) supprimé ; la question « ballon d'eau chaude » (cylindre, déjà vu en 02 et 04) remplacée par les combles en pyramide.
- S07 : l'exercice de tarifs (pourcentages, déjà très présents) remplacé par les glaces (cône, boule) ; ajout de probabilités (pêche aux canards).

### B2. Figures (35 neuves pour 06–10 ; 80 au total dans la notion, 0 image en ligne conservée)

- Toutes au style des livres, nommées `brevet_3e_s06_…` à `brevet_3e_s10_…`, énoncé = données seules, corrigé = réponses en vert : aquarium (eau à 36 cm), carré agrandi (aires × 9), rotation et homothétie sur quadrillage (pastilles ① ② centrées dans une case : aucun texte sur le quadrillage, pas de `TOLERE`), grande roue (H, 12,5 m, 14,5 m), grand huit, cornet et mini-cornet, parcours fléché (angle droit et 37° au corrigé), droite des dons, toit (sinus/cosinus), offres A et B, maison + pyramide (au corrigé, triangle SOM **en vraie grandeur** 3-4-5), diagramme de consommation (hiver en vert, moyenne), phare (cotes 152 / 168 / 320 m), globe (arc d'équateur en vert), voile (TRS en vert), marée (seuil 2,25 m, 4 h–8 h).
- Aides ajoutées dans `figures.py` (section « PARTIE B ») : `P3`, `pave_cav`, `cornet_glace`, `globe_t` (repris de la notion 247), `quadrillage`, `pastille`, `triangle_grille` ; styles `hauteur`, `rep`, `repc` ajoutés au préambule (sans effet sur les figures de la partie A).
- Scratch : 4 figures de blocs (S06, S08, énoncé et corrigé avec blocs modifiés entourés en vert) ; `controle_scratch.py` : **0 texte sur un trait**. Largeurs ≤ 730 px pour rester lisibles sur téléphone (condition du corrigé S08 écrite « non (v < 12) »).

### B3. Contrôles

- `verif_253.py` : **939 contrôles, 0 erreur** (406 de la partie A + 533 nouveaux) : barème relu pour chaque sujet, tous les calculs sympy et arrondis, **scripts exécutés** (S06 : seuils 10⁶ et 10⁷, 1 à 3 passages, culture qui triple ; S08 : t = 45, 50, 54, 60 et script corrigé ; toutes les durées de 1 à 199 min), isométries de la question de transformation testées une à une, tableaux de l'énoncé relus et comparés aux données des figures, géométrie des figures (points alignés, longueurs, angles) ; `partie_b_figures` : plus aucune ligne `Image:`, chaque image appelée est une figure neuve.
- `verifier_notion.py --navigateur` sur **toute la notion** : OK, 0 problème (80 figures neuves, 0 image en ligne conservée).
- Captures téléphone regardées : énoncés et corrigés des 5 sujets (≈ 90 écrans). Corrections faites : une vingtaine de formules trop larges découpées (chaînes de puissances, Pythagore, h(8), volume du mini-cornet, AB du phare, −2(3x − 5)…), fractions empilées dans le texte remplacées par des formules centrées, sommes longues regroupées (par paquets, par trimestres), espaces insécables entre nombre et unité, diagramme de consommation rétréci.
- Sujets 01–05 : **non modifiés** (contrôle par empreinte à chaque assemblage) ; aucune erreur trouvée en les relisant.

### B4. Pour l'orchestrateur

- Notion **prête** : cours 248, fiche 168, 10 sujets (2548 à 2557).
- **Publication** : la fiche a changé de titre (« Résumé : l'essentiel pour le jour du brevet ») → `titres_docs.py` (fait par `publier_lot.ps1`).
- Les anciennes images en ligne des sujets 06–10 (`brevet_3e_s06_aquarium.png`, … `brevet_3e_s10_marees.png`) sont remplacées position par position à l'import.
- Fichiers de travail de la partie B : dossier `253B/` du répertoire temporaire de la session (aucun dans ce dossier).
