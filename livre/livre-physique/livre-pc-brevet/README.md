# Physique-chimie — Troisième et Brevet 2027

Manuel complet dans la charte du livre de Terminale : A4, texte et mathématiques natifs, schémas vectoriels, sommaire et renvois cliquables. Édition France 2026-2027, série générale.

18 chapitres, 270 exercices à trois niveaux (540 questions), 18 investigations corrigées, 18 défis (54 questions), 239 figures et quinze brevets blancs originaux (115 questions). Les énoncés et les solutions portent les figures nécessaires à leur exploitation. Chaque question des sujets blancs possède une démarche expliquée et un barème. Fiches de méthodes, relations, unités, tests, éléments, diagnostic, lexique et concordance du programme.

## Révision des exercices et corrigés du 24 octobre 2026

Les 288 exercices et défis, ainsi que les 20 parties des dix sujets blancs, ont été relus : 308 entrées sont tracées dans `build/audit-revision.json`. Le livre comporte 38 énoncés illustrés et 155 corrigés illustrés (un corrigé de partie de brevet peut comporter plusieurs figures), 66 compléments de démarche dans les chapitres et 70 démarches de brevet. Les questions de vocabulaire, calcul ou argumentation autonomes restent sans dessin décoratif.

La livraison révisée compte **327 pages**. Les 3 240 contrôles du PDF, dont 241 calculs enregistrés, les 533 contrôles de l’audit des exercices et les 208 contrôles des cinq nouveaux sujets passent sans échec. La relecture visuelle couvre le livre rendu par planches, avec reprise des pages modifiées et des nouvelles pages après retouches. Les pages critiques sont également inspectées avec Poppler. La grille de bilan et les renvois de remédiation des dix premiers sujets restent sur une page contenant des réponses. Les pistes d’investigation restent avec leur défi corrigé.

Les cinq sujets supplémentaires (11 à 15) comportent 45 questions, 28 schémas originaux et 22 calculs vérifiés indépendamment. Ils proposent des volets de physique-chimie complets de 30 minutes sur un monte-charge, un détecteur de fumée, une station météo, un colis réfrigéré et un dirigeable. Documents, questions, constructions corrigées, démarches et barèmes sont créés pour le manuel. Le journal `recherche/creation-sujets-11-15-2026-10-24.md` explique les compétences retenues après lecture des documents officiels de 2025, 2026 et du sujet de référence 2027. Un contrôle textuel ne trouve aucune séquence identique de douze mots dans les nouveaux documents et questions par rapport aux trois archives ; ce contrôle ciblé complète la rédaction originale et ne constitue pas une preuve universelle d’originalité.

Les modèles représentent les données propres aux exercices : immersion et tare, inventaires d’atomes et d’ions, molécules, tests et pH, bilans de matière et d’énergie, montages électriques, caractéristiques, forces et gravitation, lumière et échos. Les deux constructions de forces à l’échelle sont insérées sans redimensionnement et leurs longueurs sont mesurées dans le PDF final. La caisse suspendue porte bien une force du fil. Une ancienne formule de neutralité contenant une tabulation à la place de `\\times` est corrigée ; les textes chargés sont désormais contrôlés contre ces échappements corrompus.

L’ancienne édition et les données initiales sont conservées dans `archives/avant-revision-figures-2026-10-24/`. Aucun exercice n’est supprimé ; une consigne du défi 9 demande explicitement le tracé des forces et le sujet 7 précise les deux lectures de volume cohérentes avec son déplacement de 20 mL. Les figures fournies aux élèves ne dévoilent pas les résultats qu’ils doivent calculer.

## Cadre documentaire

Le programme de physique-chimie du cycle 4 publié au BO du 30 juillet 2020 est confirmé par Éduscol pour 2026-2027. Le découpage annuel est éditorial ; les notions de Cinquième et de Quatrième utiles au DNB sont reprises.

Le format de sciences est vérifié dans la note de service du 11 septembre 2026, NOR MENE2623228N, partie I.4 : une heure, deux disciplines parmi trois, 10 points par discipline et 1 point de langue par discipline. Les quinze sujets sont des **volets PC de 30 minutes**, avec 9 points scientifiques et 1 point de langue, sans présumer les disciplines retenues pour la session. Ils ne constituent pas à eux seuls l’épreuve complète de sciences. La subdivision du point de langue en quatre quarts est une proposition d’autoévaluation OptiTAB.

Les sources primaires et le journal de recherche sont dans `recherche/`. Les trois PDF officiels consultés pour analyser les attendus sont archivés. La page du BO a été lue avec l’outil web ; son téléchargement direct a renvoyé 403, consigné dans `archives.json`. Les cours, documents d’étude et sujets blancs sont originaux ; les révisions sont harmonisées avec les autres volumes de la collection. Aucun exercice ou visuel d’annale n’est reproduit. Aucun agrément ou ISBN n’est inventé.

## Construction

Depuis la racine du projet :

```powershell
python livre-pc-brevet/generer_figures.py
python livre-pc-brevet/construire.py
python livre-pc-brevet/auditer_revision.py
python livre-pc-brevet/compiler.py
python livre-pc-brevet/verifier.py
python livre-pc-brevet/auditer_annales.py
python livre-pc-brevet/preuves_poppler.py
```

`revisions.json` contient les huit chapitres de révision adaptés ; `chimie.py` et `physique.py`, dix chapitres nouveaux ; `brevets.py`, les dix premiers sujets ; `annales_originales.py` et `figures_annales.py`, les cinq dossiers supplémentaires ; `annexes.py`, les fiches et la concordance. `revision_exercices.py`, `revision_heritage.json` et `revision_brevets.py` portent les enrichissements et placements. `figures_brevet_exercices.py` produit les schémas nouveaux avec les primitives locales ; les figures harmonisées de la collection sont conservées dans `figures/` et tracées dans `build/figures-reprises.json`. `generer_figures.py` conserve les seules figures effectivement utilisées, recensées dans `build/figures.json`. Aucun autre livre n’est modifié ni requis pour générer les figures de cette révision. Python nécessite NumPy, Matplotlib, PyMuPDF et Pillow. LuaLaTeX utilise les polices et paquets de la charte existante. Aucun texte de page n’est réduit ou transformé en image pour faire entrer le contenu.

## Contrôles et livraison

Les contrôles vérifient la structure, les réponses, les calculs enregistrés, des conservations atomiques et ioniques indépendantes, les liens, la concordance, les caractères, le format et les débordements. Le rapport `build/verification.json` distingue calculs et contrôles structurels. Ces calculs ciblés complètent une relecture scientifique ; ils ne constituent pas une preuve automatique de toutes les phrases du livre.

Toutes les pages sont rendues dans `tmp/pdfs/qa-pc-brevet/` et relues par planches. Des pages critiques sont également rendues avec Poppler et inspectées à plus grande résolution. La validation visuelle enregistre l’empreinte exacte du PDF.

```powershell
python livre-pc-brevet/livrer.py
python outils/organiser_pdf.py
```

Le script de livraison exige un rapport sans échec et une validation visuelle portant sur la même empreinte. Il copie le PDF dans la bibliothèque `output/pdf/France/Physique-chimie/` et dans le dossier des livres du Bureau, puis contrôle les deux empreintes. Le rapport final est dans `output/verification/physique-chimie-brevet-livraison.json`.
