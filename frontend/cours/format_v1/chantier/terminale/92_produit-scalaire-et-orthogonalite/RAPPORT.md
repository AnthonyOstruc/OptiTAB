# Notion 92 — Produit scalaire et orthogonalité (Terminale)

**État : prêt.** Cours 101, fiche 44 et 11 exercices au format v1 ; tous les résultats vérifiés par
`verif_produit_scalaire.py` (sympy/numpy, 110 égalités + assertions).

## Texte
- Cours remis à niveau (programme de Terminale) : définition, règles de calcul, base orthonormée, calcul
  d'angle, orthogonales ≠ perpendiculaires, vecteur normal, équation cartésienne (démonstration + réciproque),
  positions relatives, plan médiateur, projeté sur un plan **et sur une droite**, démonstration au programme
  « le projeté est le point le plus proche » (l'ancien cours présentait à tort l'équation de plan comme la
  démonstration au programme). Projeté de A sur (BDE) renommé K (H était déjà un sommet du cube).
- Fiche réécrite (4 parties, 4 erreurs classiques).
- Erreurs de fond corrigées :
  - 982 Q3b : la mesure de l'angle orienté (AC, AD) est **négative** (≈ −71,57°), et non +71,57° ;
    orientation justifiée par le signe de xy′ − x′y (règle admise dans l'énoncé), énoncé précisé
    (« rectangle en C et direct ») ; « 3a./3b. » restructurés.
  - 1106 Q3 : (IJ) et (AD) sont **orthogonales** (non coplanaires), pas « perpendiculaires ».
  - 1108 Q3b : raisonnement faux (cos² ∈ ]0;1[ ne donne pas cos > 0) → signe du produit scalaire.
  - 1107 : produit vectoriel (hors programme) remplacé par la résolution du système ; question 2 ajoutée
    (équation du plan (ABC) : 7x − 5y + 8z − 1 = 0).
  - 978 Q3 : distance obtenue par le projeté orthogonal (méthode du programme), formule en « Pour aller plus
    loin » ; Q4 : on constate que Δ = 𝒟.
  - « repère orthonormé » ajouté aux énoncés plans ; résultats en double fusionnés ; 976 : ABD est aussi
    rectangle en A ; 1108 : valeur approchée θmax ≈ 54,7°.

## Figures (20 produites, toutes refaites en TikZ style livre)
- 16 images en ligne remplacées (toutes de style ancien/matplotlib ; 1108 montrait un cube hors sujet).
- Ajoutées : cours ×2 (projection, droites orthogonales), 982 ×1 (triangles), 1105 ×1 (triangle ACG),
  1108 ×2 (courbe de θ, triangle ABM). Aucune conservée, aucune retirée sans remplacement.
- Arêtes cachées en pointillés ; tétraèdre OABC : vue calculée pour que l'angle AMO soit lisible.

## Contrôles
verifier_notion.py --navigateur : **OK, 0 problème** (22 emplacements de figures, 0 image en ligne conservée).
Les 20 PNG ont été relus un par un ; aucun texte n'est posé sur un trait (contrôle automatique passé).

## Remarques pour l'orchestrateur
- `\codage` de figures_livre.py dessine des traits démesurés à l'intérieur d'un `axis` pgfplots
  (décoration) ; remplacé ici par une macro locale `\tic`.
- Les points en `\node` (fond rempli) sont comptés comme du « texte » par le contrôle de chevauchement ;
  utiliser `\fill … circle` ou `geoPoint`.
- Plusieurs exercices sont des rappels de Première en géométrie plane (974, 975, 976, 978, 979, 981, 982).

## Finition 2026-11-02

**État : prêt** (agent-finition-T5). 11 exercices, dont **7 réécrits de zéro**.

### Exercices réécrits (géométrie plane de Première → espace, programme de Terminale)
Les 7 exercices signalés « rappels de Première en géométrie plane » ne travaillaient pas la notion (orthogonalité et distances **dans l’espace**) ; 982 utilisait même des angles orientés de vecteurs (hors programme). Contenu remplacé dans le même bloc (Id, type et difficulté conservés), méthode / étapes / résultat / erreur fréquente :
- 974 « Découverte - Produit scalaire et angle dans un pavé droit » : pavé 4 × 2 × 3, repère orthonormé, $\overrightarrow{AF} \cdot \overrightarrow{AH} = 9$, $\widehat{FAH} \approx 60{,}1°$, $(AE)$ et $(BD)$ orthogonales mais non perpendiculaires ;
- 978 « Découverte - Projeté orthogonal d’un point sur une droite » : $t = \frac{1}{3}$, $H\left(\frac{4}{3}\,;\frac{2}{3}\,;\frac{8}{3}\right)$, distance $\sqrt{26}$, Pythagore ;
- 981 « Découverte - Règles de calcul : longueur, angle et aire » : sans repère, $BC = \sqrt{17}$, angle obtus $\approx 109{,}5°$, médiane $\frac{3}{2}$, pied de hauteur hors du segment ($k = -\frac{1}{2}$), aire $2\sqrt{2}$ ;
- 979 « Découverte - Triangle rectangle et rectangle dans l’espace » : rectangle $ABDC$, aire 9, $\overrightarrow{AD} \cdot \overrightarrow{BC} = 27$ ;
- 976 « Entraînement - Projeté orthogonal sur un plan et distance » : $t = -\frac{7}{3}$, $H\left(\frac{1}{3}\,;\frac{10}{3}\,;\frac{10}{3}\right)$, distance 7, $MB^2 = MH^2 + HB^2$ (point le plus proche) ;
- 975 « Entraînement - Orthogonalité, angle et vecteur normal » : $\theta \approx 103{,}6°$, $k = -1$, $\vec{n}(-2\,;2\,;1)$, plan $-2x + 2y + z = 0$ ;
- 982 « Problème - Plan médiateur d’un segment » : $x + 2y - z - 3 = 0$, $D(0\,;0\,;-3)$, $\widehat{ADB} \approx 56{,}3°$, aire $3\sqrt{14}$.
- Titre aussi revu : 1108 « Type bac - Angle maximal dans un tétraèdre trirectangle ». Cours et fiche : intitulé officiel déjà en place.

### Figures (outil commun `figures/espace.py` : parties cachées calculées, étiquettes hors des traits)
- **Revérifiées** : les 20 existantes.
- **Refaites (5)** : `cours_projection` (« A » collé au nom du plan), `cours_cube_bde` (« D » et « K » sur des traits ; vue un peu plus plongeante), `ex1108_tetra` et `ex1108_milieu` (« M » posé sur l’arête [BC]), `ex1105_repere` (919 px → ≤ 900 px).
- **Retirées (4)** : `ex979_rectangle`, `ex976_points`, `ex982_droites`, `ex982_triangles` (exercices réécrits).
- **Ajoutées (11)** : cours `cours_plan_mediateur`, `cours_projete_droite` ; exercices `n974_pave` (énoncé), `n974_angle`, `n978_projete`, `n981_hauteur`, `n979_rectangle`, `n976_projete`, `n975_normal`, `n982_mediateur`, `n1107_normal` (corrigés, éléments trouvés en vert). Plus aucun exercice sans figure.

### Contrôles
- `verif_produit_scalaire.py` : OK, 139 égalités (contrôles des 7 exercices plans remplacés par ceux des nouveaux).
- `figures_livre.py` : 27/27 figures, 0 erreur, 0 avertissement ; chaque PNG regardé.
- `verifier_notion.py --navigateur` : OK, 0 problème ; `controle_apercu.mjs` avec captures : aucun problème. Captures téléphone des 7 exercices réécrits regardées : 16 formules coupées ou réduites redécoupées (chaînes alignées, « soit » sous la formule, équivalences sorties des `aligned`), 2 lignes qui commençaient par une ponctuation corrigées.

### Pour l’orchestrateur
- La notion s’appelle encore « Produit scalaire et orthogonalité » en base : intitulé officiel « Orthogonalité et distances dans l’espace » (déjà celui du cours) — à renommer en base.
