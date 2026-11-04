# Rapport — notion 159 « Géométrie repérée dans le plan » (Première spécialité)

**État : prêt.** Cours, fiche et 19 exercices au format OptiTAB v1 ; 18 figures neuves au style des livres.

## Programme (2019, Première spécialité)

Vérifié et couvert : vecteur normal, équation cartésienne $ax + by + c = 0$ (normal $(a;b)$, directeur $(-b;a)$), droite par un point et un vecteur normal, projeté orthogonal d’un point sur une droite et distance (via le projeté), équation de cercle (centre-rayon, reconnaissance par complétion des carrés), parabole $y = ax^2 + bx + c$ (axe, sommet), utilisation d’un repère pour étudier une configuration. La formule $|ax_0 + by_0 + c| / \sqrt{a^2 + b^2}$ (hors programme de Première) n’apparaît plus que dans une remarque « Pour aller plus loin » du cours. La tangente à un cercle est traitée comme application du vecteur normal.

## Texte

- **Cours réécrit entièrement** : prérequis, définitions, théorème + démonstration (équation cartésienne et vecteur normal ; équation du cercle ; axe de symétrie par la forme canonique ; distance minimale par Pythagore), méthodes, exemples, erreurs fréquentes, « à retenir ». Exemple de cercle unifié (Ω(1 ; −1), r = 5, tangente en A(4 ; 3)).
- **Fiche réécrite** (formules, méthode du projeté, cercle, parabole, 5 pièges).
- **Exercices** : les 18 exercices existants réécrits au modèle du pilote (méthode / étapes / résultat / erreur fréquente), Id et titres conservés.
  - Corrections de fond :
    - 1409, 1413, 1417, 1419, 1421, 1422 : la distance point-droite était calculée par la formule hors programme. Elle passe désormais par le projeté orthogonal.
    - 1421 : la conclusion « triangle non rectangle » ne testait qu’un sommet. Les trois sommets sont maintenant vérifiés.
    - 1410 : deux cas dégénérés identiques ; l’un est remplacé par un cas d’ensemble vide.
    - 1408 : la question de colinéarité, redondante, est remplacée par le calcul d’un point d’intersection, et Δ₄ est modifiée pour obtenir K(1 ; 1).
    - 1414 : le point A(5 ; 3) donne une tangente oblique au lieu d’une tangente verticale triviale.
    - 1417 : la droite x + y − 6 = 0 donne des points d’intersection exacts E(1 ; 5) et F(4 ; 2), et H est le milieu de [EF].
    - 1419 : le projeté de B est le centre, ce qui fait découvrir un losange.
    - 1418 : tableau de variations natif.
  - **Remplacés** (contenu neuf, même Id et même titre) :
    - 1422 « DS - Configurations géométriques dans un repère » : l’ancien doublonnait 1412 et sa parabole avait des coefficients 25/84 et 37/84. Le nouveau DS porte sur un triangle rectangle en C, son cercle circonscrit, la hauteur et le projeté, et la parabole y = x² − 4x.
    - 1423 « Type Examen - Synthèse » : l’ancien avait une question sans objet (« D ne passe pas par Ω… »). Le nouveau sujet porte sur le cercle x² + y² − 6x − 8y = 0, le diamètre [AB], les tangentes parallèles en O et en H(6 ; 8) et la parabole y = −x² + 6x de sommet sur le cercle.
  - **Ajouté** : `nouveau-1` « Entraînement - Retrouver l'équation d'une parabole » (lecture du sommet, forme a(x − α)² + β, symétrie). Cette compétence « sommet → équation » n’était pas travaillée.
- Toutes les valeurs sont vérifiées par `verif_geometrie.py` (176 contrôles, sympy) : OK.

## Figures

- **18 refaites ou ajoutées**, aucune conservée. Les 14 images en ligne (style matplotlib par défaut, légendes minuscules, cercle du cours sans rapport avec l’exemple) ne sont plus appelées.
- Cours : 4 (normal, projeté, cercle + tangente, parabole). Fiche : 2 (réutilisent celles du cours).
- Exercices : 13 refaites (1409, 1411, 1412, 1413, 1414, 1416, 1417, 1418, 1419, 1420, 1421, 1422, 1423), placées dans les corrigés, plus 1 dans l’énoncé de nouveau-1.
- Repère tracé en TikZ (fonction `repere`) ; les graduations qui tombaient sous un trait sont omises. Contrôle des chevauchements à 0 erreur et chaque PNG a été vérifié à l’œil. Largeurs de 431 à 823 px.

## Contrôles

- `verifier_notion.py` : **OK, 0 problème** (20 placements de figures neuves, 0 image en ligne conservée).
- Contrôle navigateur (`controle_apercu.mjs`) : 118 vues (téléphone + ordinateur ; cours, fiche, 19 exercices × 3 onglets), toutes à 0 (débordement, formules, `$` bruts, images, blocs, largeur). Voir `captures_log.txt`.
- Captures téléphone regardées : cours (5 parties), fiche, étapes de 1422, 1413, 1420 et 1421.
- Corrections faites après ces captures :
  - deux formules centrées coupées (démonstration du cours, aire dans 1422) ont été passées en `aligned` ;
  - les longues égalités en ligne ont été découpées ;
  - l’étiquette $T$ de la figure du cercle a été écartée de la tangente.

  Nouvelle capture : tout est entier.

## Remarques pour l’orchestrateur

- **Défaut d’outil** : `controle_apercu.mjs` ne rend pas la main en fin de contrôle (après la dernière vue « desktop exercice 19 », sans afficher « Aucun problème détecté »). Le processus node reste bloqué en consommant du CPU. Le même blocage touchait le contrôle de la notion 158, lancé en parallèle. `verifier_notion.py --navigateur` restait donc suspendu jusqu’à son délai de 1800 s. J’ai arrêté ce processus, puis lancé `verifier_notion.py` sans navigateur (OK) et `controle_apercu.mjs` directement avec `timeout` : les 118 vues sont propres.
- Le contrôle automatique ne détecte pas une formule en ligne ou centrée coupée sur téléphone. Seule la relecture des captures l’a révélé (cas corrigés).
- La notion 158 (produit scalaire) traite le cercle de diamètre [AB] (MA·MB = 0) : ici, seulement une remarque dans 1423.


## Finition 2026-11-02

**État : prêt.** Mise en conformité avec les deux consignes du 2026-11-02 (figures partout où elles aident, titres).

**Titres.** Cours : « Géométrie repérée dans le plan » ; fiche : « Résumé : Géométrie repérée dans le plan ». Exercices : 1407 « Découverte - Équation de droite à partir d'un vecteur normal » ; 1410 « Découverte - Équations de cercles » ; 1421 « DS - Droites, cercles et triangles » (nom du chapitre retiré) ; 1423 « Type examen - Cercle, tangentes et parabole » (nom du chapitre et majuscule retirés).

**Figures : 16 nouvelles**, 0 refus du détecteur de chevauchement.
- Corrigé de nouveau-1 « Retrouver l'équation d'une parabole » : parabole complétée (axe x = −1, B(−3 ; 0), C(0 ; 3), C′(−2 ; 3) en vert).
- Corrigés des 5 exercices qui n’avaient aucune figure : 1407 (Δ1, vecteur normal, point E ; perpendiculaire à d par M), 1410 (cercle C1 et son rayon), 1408 (droites sécantes en K(1 ; 1) ; droites perpendiculaires et vecteurs normaux), 1406 (vecteur directeur et vecteur normal de Δ), 1415 (parabole, sommet, axe, points symétriques, racines).
- Énoncés (données seules : repère, points, droites, cercle) : 1409, 1413, 1417, 1412, 1416, 1420, 1419, 1422.
- Les 18 exercices ont maintenant au moins une figure ; les exercices de configuration en ont une dans l’énoncé et une, complétée, dans le corrigé.

**Contrôle de qualité.** Relecture des 18 énoncés et corrigés : aucun exercice faux ou hors programme. Données des nouvelles figures vérifiées dans `verif_geometrie.py` : **189 vérifications justes**.

**Contrôles.** `verifier_notion.py` : OK. Le contrôle Chrome est resté bloqué à la fermeture de Chrome, une fois toutes les vues faites (défaut déjà signalé). J’ai arrêté mon seul processus, puis lancé `controle_apercu.mjs` directement : 118 vues (téléphone et ordinateur), 0 débordement, 0 erreur de formule, 0 élément trop large. Après la dernière retouche de figure, j’ai régénéré l’aperçu et refait le contrôle rapide : 118 vues propres. Captures téléphone regardées : 1407, 1408 et nouveau-1 (corrigés complets). Corrigé après capture : dans 1408 (perpendicularité), les vecteurs normaux étaient tracés exactement sur l’autre droite (n₂ est parallèle à d₁). C’était juste mais illisible : je les ai retirés et j’ai gardé l’angle droit en vert. J’ai aussi retiré une graduation que d₂ traversait.

**Remarques pour l’orchestrateur.**
- nouveau-1 est **déjà en ligne** (Id 4932, sauvegarde d’import) : avant réimport, nouvel export et remplacement de `Id: nouveau-1` et de la clé `"nouveau-1"` de `correspondance.json`, sinon doublon.
