# Rapport — 1ère / 158 Calcul vectoriel et produit scalaire

**État : prêt.** Aucune écriture en base, aucun `manage.py`, aucun `git`.

## Programme (Première spécialité, 2019)

Couvert : produit scalaire dans le plan par normes et angle, par projection
orthogonale, par les normes seules (polarisation) et par coordonnées en repère
orthonormé ; symétrie, bilinéarité, identités remarquables ; caractérisation de
l’orthogonalité ; calcul d’angles et de longueurs ; formule d’Al-Kashi
(démonstration) ; formule de la médiane ; ensemble des points $M$ tels que
$\overrightarrow{MA} \cdot \overrightarrow{MB} = 0$ (démonstration) et
$\overrightarrow{MA} \cdot \overrightarrow{MB} = k$. Rien dans l’espace (Terminale).
Retiré : l’ancienne figure « loi des sinus » (cercle circonscrit, hors programme).

## Texte

- **Cours réécrit de zéro** (l’ancien tenait en quelques encadrés, sans
  projection démontrée ni médiane) : objectifs, prérequis, 5 parties
  (définition et orthogonalité ; projection avec démonstration ; règles de calcul,
  identités, polarisation avec démonstration ; repère orthonormé avec démonstration
  de $xx' + yy'$ ; Al-Kashi, médiane, ensembles de points, chacun démontré),
  méthodes, exemples, erreurs fréquentes. Plus de `\displaystyle`.
- **Fiche réécrite** : tableau des quatre méthodes, règles, orthogonalité, angle,
  Al-Kashi, médiane, ensembles de points, 5 pièges.
- **Exercices** : les 13 blocs réécrits au format v1 (méthode / étapes /
  résultat / erreur fréquente), Ids inchangés, « Partie A / Question A1 » structurés.
  - **Erreur corrigée** (1402) : $\widehat{C} \approx 73{,}8°$ obtenu par soustraction
    d’arrondis → $73{,}7°$ (calcul direct, $\cos\widehat{C} = \frac{7}{25}$), avec une note
    « attention ».
  - 1401 **remplacé** (doublon de 1403/1404, figure fausse : C(4 ; 7) au lieu de
    C(3 ; 8)) par « DS - Projection et orthogonalité dans un rectangle et un carré »
    (projection, Chasles, orthogonalité par décomposition et par repère).
  - Doublons supprimés : 1404 Partie B (mêmes vecteurs que 1403) → nouveau triangle
    rectangle isocèle avec angle exact de $45°$ ; 1403 Partie C (même calcul que
    1398) → angle $\frac{2\pi}{3}$ ($BC = \sqrt{109}$).
  - Questions faibles remplacées : 1393 Q6 (distributivité), 1394 Q4 (cas non
    orthogonal) + Q6 ($m^2 = 16$, deux solutions), 1395 Q5 (angle obtus),
    1397 Q2 (droites perpendiculaires) et Q4 (triangle rectangle), 1398 Q5 (angle
    obtus) ; questions de cours de 1402/1404 avec de vraies réponses (plus de
    « voir étapes »).
- **Ajouts** : nouveau-1 « Entraînement - Produit scalaire par projection
  orthogonale » (quadrillage, projetés des deux côtés, triangle équilatéral) ;
  nouveau-2 « Entraînement - Trois longueurs et formule de la médiane » ;
  nouveau-3 « Problème - Distance inaccessible et formule d'Al-Kashi » (situation
  concrète, distance d’un point à une droite par projection).
- Tous les résultats vérifiés : `verif_158.py` (138 vérifications sympy, tout juste).

## Figures (`figures/figures.py`, 50 figures, 54 emplacements)

- 28 images en ligne (matplotlib, style ancien) : **toutes refaites** ;
  0 conservée ; 1 seule position n’est plus appelée (1399 pos. 5, ensemble vide :
  pas de figure utile). La « loi des sinus » (1398) est remplacée.
- Consigne « figure partout où elle aide » appliquée : cours (projection en deux
  cas superposés pour le téléphone, Al-Kashi, médiane, cercle), fiche (projection,
  Al-Kashi, cercle) ; chaque énoncé de géométrie a sa figure (sans réponse) et
  chaque corrigé montre la figure complétée, éléments de réponse en vert
  (1405, 1401, 1403, 1397, 1398, 1399, 1400, 1402, 1404, nouveau-1 à 3).
  Exception assumée : 1397 et 1399 donnent des points par coordonnées ou
  demandent un ensemble à trouver, donc la figure est dans le corrigé seulement ;
  1393 à 1396 sont des calculs de vecteurs sans configuration.
- Contrôle texte/trait du compilateur : OK ; étiquettes revues à l’œil (aucune
  sur un trait oblique), toutes les figures ≤ 900 px.

## Contrôles

- `verifier_notion.py --navigateur` : **OK, 0 problème**.
- `controle_apercu.mjs` : aucun problème (16 exercices × 3 onglets, téléphone et
  ordinateur). Captures regardées : cours en téléphone (toutes les parties),
  fiche, exercices 1405, nouveau-1 et nouveau-3. Corrigé après capture :
  formules coupées (démonstration de la médiane, formules côte à côte de la fiche,
  « … donc … » sur une ligne) découpées en lignes ou en `aligned`, puis recapture.
- Titres : cours « Calcul vectoriel et produit scalaire », fiche « Résumé : Calcul
  vectoriel et produit scalaire » (intitulé du programme).

## Remarques pour l’orchestrateur

- Le titre de l’Id 1401 change (exercice remplacé).
