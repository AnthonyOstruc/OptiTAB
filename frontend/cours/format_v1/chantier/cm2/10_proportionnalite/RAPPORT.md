# Rapport — 10_proportionnalite

État : prêt. Contenus nouveaux destinés à une création CM2 ; aucune écriture ni aucun import en base.

## Contenus et programme

Le cours et la fiche ont été entièrement réécrits au format OptiTAB v1. La banque contient 21 exercices nouveaux (`nouveau-1` à `nouveau-21`), 7 familles et 3 niveaux, soit 63 questions. Chaque question possède méthode, raisonnement, résultat et réponse courte cohérente. Les textes sources locaux sont conservés sans modification.

Deux grandeurs toujours contextualisées. Raisonnements en phrases : double, triple, moitié, assemblage et retour à une unité. Situations non proportionnelles justifiées. Aucun tableau de proportionnalité, coefficient ou produit en croix.

Références officielles consultées : [BO cycle 3, annexe 2](https://www.education.gouv.fr/sites/default/files/ensel620_annexe2-v2.pdf) et [exemples Eduscol CM2](https://eduscol.education.gouv.fr/sites/default/files/document/exemplesmiseenoeuvrecm2-mathpdf-111537.pdf). Le programme de CM2 entre en application à la rentrée 2026. Les précisions CM2 sur les opérations sont aux pages 9 à 11 du BO, la proportionnalité page 27 et la pensée informatique page 28.

## Figures

Quatre planches sources examinées. L'ancienne banque d'images (43 entrées d'inventaire, souvent répétitives) n'est pas réutilisée. 1 figure(s) nouvelle(s) en TikZ, style des livres ; aucune image ancienne conservée. Tous les PNG finaux ont été regardés : légendes lisibles, aucun texte sur un trait, valeurs cohérentes, largeur maximale 693 px. La correspondance utilise `cours/nouveau` et `fiches/nouvelle` ; aucun appel d'image absent dans les exercices.

## Contrôles finaux

- Validation statique et aperçu : OK, zéro problème.
- Chrome mobile et ordinateur : 130 vues distinctes, zéro anomalie.
- Relecture visuelle du cours mobile entier (2 captures), de la fiche entière et des exercices 1, 11 et 21 (énoncé et étapes) : 9 captures examinées.
- `verif_math.py` : 71 égalités numériques du texte final contrôlées, solutions comparées aux résultats détaillés ; aucun calcul erroné. Les propositions volontairement fausses des questions d'analyse d'erreur sont exclues du contrôle des affirmations, puis corrigées dans les étapes.
- Les contenus intégrés à `apercu.html` sont comparés intégralement aux textes finaux par `finaliser_calculs.py`.

Les corrections de relecture comprennent les séparateurs d'exercices requis, les fermetures de formules et les virgules décimales hors formule. Le garde-fou local contrôle ces virgules, que l'audit de mise en page seul ne signalait pas. Pour les régularités, le dénombrement des croix et six chemins/orientations sont également vérifiés. Aucun point restant.

## Clôture de coordination — 2026-11-01

État : prêt pour création du CM2. Aucun import effectué par les rédacteurs.

Proportionnalité contextualisée, raisonnée en phrases par linéarité et retour à l’unité ; aucun coefficient, produit en croix ou tableau de proportionnalité.

21 exercices, 63 questions corrigées : chaque question possède méthode, étapes et résultat ; réponses courtes contrôlées. Les sources locales sont conservées intégralement. Les anciennes illustrations (43 entrées d’inventaire) ont été examinées sur les planches ; aucune n’est réutilisée. 1 PNG actifs refaits au style des livres, inspectés à l’écran ; aucune tolérance de chevauchement ajoutée par la coordination.

Contrôles : vérificateur mathématique final réussi ; validation officielle adaptée localement réussie ; 130 vues distinctes, téléphone 390 px et ordinateur 1280 px, sans anomalie. Le cours mobile entier, la fiche et les exercices 1, 11 et 21 (énoncé et étapes) ont été relus. Les empreintes des fichiers finaux, images et correspondance sont figées dans PREUVES_FINALES.json. Les aperçus utilisent le moteur et les feuilles de style réels du site.

Les retouches de coordination corrigent les accords au singulier, six doublons en géométrie, une légende de compas trop proche de A, l’échelle d’une frise horaire, les couleurs des arbres selon l’évènement étudié et les tableaux de numération/conversion sur téléphone. Les noms visibles de chapitre sont repris des cours finaux ; les sources restent intactes. Aucun point restant.

## Publication CM2 vérifiée

Cours, fiche, exercices et images importés et relus. Accès local et public contrôlés ; les sauvegardes des textes et illustrations d’origine sont conservées.
