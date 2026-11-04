# Notion 232 (3e) : Théorème de Thalès et triangles semblables

**État : prêt** (agent-3e-C1, 2026-11-03).

Programme du cycle 4, attendus de fin de 3e : théorème de Thalès (configurations emboîtée et papillon), réciproque, triangles semblables (angles égaux, côtés proportionnels), effet d'un agrandissement ou d'une réduction sur les longueurs, les aires et les volumes.

## Texte
- **Cours 227** : réécrit. La conversion avait cassé le théorème (énoncé coupé en deux encadrés, la formule dans un encadré `definition`), la méthode et les exemples étaient rangés dans des encadrés `definition`.
  - I. Les deux configurations (figures), théorème complet, `retenir` sur la correspondance des côtés.
  - II. Méthode en 4 étapes, exemples emboîté et papillon, `attention` sur $MB$ et $NC$.
  - III. Réciproque (avec l'ordre des points), méthode, exemple, propriété « rapports différents », pièges (arrondis, ordre, $\frac{MN}{BC}$ inutile).
  - IV. Triangles semblables : définition, propriété (côtés proportionnels et réciproque), méthode d'association des sommets, exemple ; **ajout** : lien avec Thalès et sa démonstration (angles correspondants) ; tableau longueurs, aires, volumes ($k^3$ ajouté), angles.
  - V. Hauteur par les ombres ; VI. Rédaction au brevet ; `retenir` final.
- **Fiche 147** : réécrite (théorème, méthode, réciproque, semblables, tableau $k$, $k^2$, $k^3$, 5 erreurs classiques, réflexe brevet).
- **Exercices** : les 21 sont réécrits au format complet (méthode, étapes détaillées, résultat encadré, erreur fréquente ou à retenir, solution courte). Titres « Type - Sujet ». Progression : 7 Découverte, 7 Entraînement, 5 Problème, 2 Type brevet.
  - **Remplacés** (même Id) :
    - 2089 « Calculer la petite base » (doublon de 2088) → « Découverte - Reconnaître une configuration de Thalès » (3 figures : emboîtée, papillon, parallélisme non donné ; calcul en papillon) ;
    - 2223 « Compléter les rapports » (doublon de 2087 et 2088) → « Découverte - Triangles semblables reconnus par leurs angles » ;
    - 2227 « Reconnaître des triangles semblables » (doublon de 2225) → « Entraînement - Triangles semblables reconnus par leurs côtés » (caractérisation par les côtés proportionnels, piège du 3e quotient) ;
    - 2228 « Côtés, périmètres et aires » (doublon de 2226) → « Entraînement - Réciproque en configuration papillon » ;
    - 2229 « Une largeur inaccessible » (simple théorème des milieux) → « Problème - Largeur d'une rivière » (équation $\frac{x}{x+6} = \frac{12}{15}$, $x = 24$ m) ;
    - 2232 → « Type brevet - Démontrer un parallélisme puis calculer » : réciproque de Thalès, Thalès, réciproque de Pythagore, perpendiculaire et parallèle, rapport des aires $= k^2$.
  - **Questions corrigées** : 2230 Q5 était un texte erroné (« le bâton restant à 39 m... du phare ? Non : ... ») → distance œil-sommet par Pythagore ($\sqrt{2\,197} \approx 46{,}9$ m) ; 2091 Q5 (explication vague sur l'ordre) → test d'un point $P$ ($\frac{9}{15} \neq \frac{6}{15}$) ; 2092 : piège des arrondis ajouté ; 2224 Q4 : contre-exemple chiffré et dessiné ; 2226 Q5 : coefficient retrouvé à partir des aires.
  - Aucune erreur de calcul dans les résultats en ligne ; les défauts étaient des doublons, des questions faibles et le texte cassé de 2230.
- `verif_232.py` : **90 contrôles sympy OK** (chaque longueur, rapport, aire, équation ; coordonnées de la figure de 2232).

## Figures
- **46 figures neuves** (figures.py, style des livres) pour **49 positions** ; les 29 images en ligne (style matplotlib) sont toutes remplacées ; 0 conservée, 0 retirée sans remplacement.
  - Cours (5) : emboîtée, papillon, réciproque cotée, triangles semblables (angles codés, $\times k$), ombres. La fiche reprend emboîtée, papillon et semblables.
  - Exercices : figure d'énoncé (données seules) **et** figure de corrigé (réponses en vert) pour les 20 exercices géométriques ; 2224 (vrai ou faux) a une figure de contre-exemple dans le corrigé. Figures ajoutées là où il n'y en avait pas : 2223, 2225, 2226, 2227, 2228, 2231.
- Détecteur texte/trait : 0 erreur ; seules alertes : cotes à fond blanc (usage normal). Toutes ≤ 900 px sauf ex2089_enonce (923 px, trois figures côte à côte, sous la limite de 1100 px). Chaque PNG regardé.

## Contrôles
- `verifier_notion.py --navigateur` : **OK, 0 problème** (toutes les vues téléphone et ordinateur sans débordement ni erreur de formule).
- `controle_apercu.mjs` avec captures : « Aucun problème détecté ». Vues regardées sur téléphone : cours en entier (parties I à VI), fiche, exercice 2232 (étapes). Corrections faites après ces vues : formules côte à côte (`\qquad`, 17 cas) passées sur deux lignes ; calcul de Pythagore de 2232 Q3 (réduit) passé en `aligned` ; aires de 2232 Q5 (coupées) séparées ; formule de $k$ du cours IV (point final seul sur sa ligne) passée en formule centrée.

## Remarques pour l'orchestrateur
- Titres de cours et fiche inchangés (déjà l'intitulé de la notion).
- Le type « Type brevet » est utilisé pour 2230 et 2232, comme demandé par la consigne de lot.
