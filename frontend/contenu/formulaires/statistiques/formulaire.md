---
{
  "slug": "statistiques",
  "titre": "Statistiques",
  "titreCourt": "Statistiques",
  "titreSeo": "Formules de statistiques : moyenne, médiane, quartiles, écart type",
  "description": "Toutes les formules de statistiques : moyenne, moyenne pondérée, médiane, quartiles, variance, écart type, diagrammes, boîte à moustaches, droite d’ajustement.",
  "chapo": "Les indicateurs de position et de dispersion, les représentations graphiques et les statistiques à deux variables, avec un exemple entièrement calculé.",
  "resume": "Moyenne, médiane, quartiles, écart type, régression",
  "vignette": "boite_moustaches",
  "theme": "Probabilités et statistiques",
  "niveaux": ["Collège", "Lycée", "Supérieur"],
  "ordre": 14,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["formules statistiques", "calcul moyenne", "moyenne pondérée", "médiane", "quartiles", "écart type", "variance", "boîte à moustaches", "droite des moindres carrés"],
  "figures": [
    { "nom": "boite_moustaches", "alt": "Boîte à moustaches de la série 3, 4, 5, 6, 6, 7, 8, 9 : minimum 3, premier quartile 4, médiane 6, troisième quartile 7, maximum 9." },
    { "nom": "histogramme", "alt": "Histogramme à classes inégales : [0 ; 10[ effectif 4, [10 ; 20[ effectif 10, [20 ; 30[ effectif 6, [30 ; 50[ effectif 8 avec un rectangle deux fois plus large et deux fois moins haut." },
    { "nom": "nuage_ajustement", "alt": "Nuage de sept points presque alignés, son point moyen G et la droite d’ajustement par la méthode des moindres carrés, qui passe par G." }
  ],
  "chapitresLies": [
    "5e/organiser-et-interpreter-des-donnees",
    "4e/statistiques-et-diagrammes",
    "3e/statistiques",
    "seconde/utiliser-l-information-chiffree-et-statistique-descriptive"
  ],
  "faq": [
    ["Quelle est la différence entre la moyenne et la médiane ?", "La moyenne est la somme des valeurs divisée par l’effectif total. La médiane partage la série ordonnée en deux groupes de même effectif. La médiane n’est pas influencée par les valeurs extrêmes, contrairement à la moyenne."],
    ["Comment calculer les quartiles ?", "On range les valeurs dans l’ordre croissant. Q1 est la valeur de rang N/4, arrondi à l’entier supérieur ; Q3 est la valeur de rang 3N/4, arrondi à l’entier supérieur. Au moins 25 % des valeurs sont inférieures ou égales à Q1, et au moins 75 % à Q3."],
    ["Comment calculer une moyenne pondérée ?", "On multiplie chaque valeur par son coefficient (ou son effectif), on additionne ces produits, puis on divise par la somme des coefficients. Par exemple, 12 coefficient 2 et 15 coefficient 1 donnent (24 + 15)/3 = 13."],
    ["Quelle est la différence entre variance et écart type ?", "L’écart type est la racine carrée de la variance. Il s’exprime dans la même unité que les valeurs de la série : c’est lui qu’on interprète comme l’écart moyen à la moyenne."]
  ]
}
---
<!-- optitab:1 -->
## I. Vocabulaire et fréquences {Collège}

On étudie une série de $N$ valeurs $x_1, \ldots, x_p$, d’effectifs $n_1, \ldots, n_p$ (avec $n_1 + \cdots + n_p = N$).

| Notion | Formule |
|---|---|
| Effectif total | $N = n_1 + n_2 + \cdots + n_p$ |
| Fréquence de la valeur $x_i$ | $f_i = \dfrac{n_i}{N}$ |
| Somme des fréquences | $f_1 + f_2 + \cdots + f_p = 1$ |
| Fréquence en pourcentage | $f_i \times 100$ |

## II. Indicateurs de position {Collège}

| Indicateur | Formule ou définition |
|---|---|
| Moyenne | $\bar{x} = \dfrac{x_1 + x_2 + \cdots + x_N}{N}$ |
| Moyenne pondérée par les effectifs | $\bar{x} = \dfrac{n_1 x_1 + n_2 x_2 + \cdots + n_p x_p}{N}$ |
| Moyenne avec les fréquences | $\bar{x} = f_1 x_1 + f_2 x_2 + \cdots + f_p x_p$ |
| Médiane ($N$ impair) | la valeur de rang $\dfrac{N + 1}{2}$ dans la série rangée |
| Médiane ($N$ pair) | la moyenne des valeurs de rangs $\dfrac{N}{2}$ et $\dfrac{N}{2} + 1$ |
| Premier quartile $Q_1$ | la valeur de rang $\dfrac{N}{4}$, arrondi à l’entier supérieur |
| Troisième quartile $Q_3$ | la valeur de rang $\dfrac{3N}{4}$, arrondi à l’entier supérieur |
| Mode | la valeur qui a le plus grand effectif |

::: attention Ranger avant tout
La médiane et les quartiles se lisent dans la série **rangée dans l’ordre croissant**. Pour des valeurs regroupées en classes, on prend le centre de chaque classe pour calculer la moyenne.
:::

## III. Indicateurs de dispersion {Lycée}

| Indicateur | Formule |
|---|---|
| Étendue | $\text{max} - \text{min}$ |
| Écart interquartile | $Q_3 - Q_1$ |
| Variance | $V = \dfrac{1}{N}\displaystyle\sum_{i=1}^{p} n_i\,(x_i - \bar{x})^2$ |
| Variance (autre formule) | $V = \dfrac{1}{N}\displaystyle\sum_{i=1}^{p} n_i\,x_i^2 - \bar{x}^2$ |
| Écart type | $\sigma = \sqrt{V}$ |

::: exemple Série $3, 4, 5, 6, 6, 7, 8, 9$ ($N = 8$, déjà rangée)
- Moyenne : $\bar{x} = \dfrac{48}{8} = 6$ ; médiane : moyenne des 4ᵉ et 5ᵉ valeurs, $\dfrac{6 + 6}{2} = 6$.
- $Q_1$ : rang $\dfrac{8}{4} = 2$, donc $Q_1 = 4$ ; $Q_3$ : rang $6$, donc $Q_3 = 7$.
- Étendue : $9 - 3 = 6$ ; écart interquartile : $7 - 4 = 3$.
- Variance : $V = \dfrac{9 + 4 + 1 + 0 + 0 + 1 + 4 + 9}{8} = 3{,}5$ ; écart type : $\sigma = \sqrt{3{,}5} \approx 1{,}87$.
:::

## IV. Effet d’une transformation affine {Lycée}

Si chaque valeur est transformée en $y_i = a\,x_i + b$ :

| Indicateur | Nouvelle valeur |
|---|---|
| Moyenne | $\bar{y} = a\,\bar{x} + b$ |
| Médiane (pour $a > 0$) | $a \times \mathrm{Me}_x + b$ |
| Variance | $V_y = a^2\,V_x$ |
| Écart type | $\sigma_y = \lvert a \rvert\,\sigma_x$ |

::: exemple
Si toutes les notes augmentent de $2$ points, la moyenne augmente de $2$ mais l’écart type ne change pas. Si elles sont multipliées par $2$, l’écart type est multiplié par $2$.
:::

## V. Représentations graphiques {Collège}

| Diagramme | Règle de construction |
|---|---|
| Diagramme en barres | hauteur proportionnelle à l’effectif |
| Diagramme circulaire | angle du secteur $= 360^\circ \times f_i$ |
| Histogramme | **aire** proportionnelle à l’effectif : hauteur $= \dfrac{\text{effectif}}{\text{amplitude de la classe}}$ |
| Boîte à moustaches | minimum, $Q_1$, médiane, $Q_3$, maximum |

[IMAGE_1]

La boîte à moustaches de l’exemple : la boîte va de $Q_1 = 4$ à $Q_3 = 7$ et contient la moitié centrale des valeurs.

[IMAGE_2]

::: attention Classes inégales
La classe $[30\,;50[$ est deux fois plus large que les autres : pour un effectif de $8$, son rectangle a la même hauteur qu’un effectif de $4$ sur une classe de largeur $10$.
:::

## VI. Statistiques à deux variables {Lycée}

Pour une série de $N$ points $(x_i\,;y_i)$ :

| Notion | Formule |
|---|---|
| Point moyen | $G(\bar{x}\,;\bar{y})$ |
| Covariance | $\operatorname{cov}(x, y) = \dfrac{1}{N}\displaystyle\sum_{i=1}^{N} (x_i - \bar{x})(y_i - \bar{y})$ |
| Droite des moindres carrés | $y = ax + b$ avec $a = \dfrac{\operatorname{cov}(x, y)}{V(x)}$ et $b = \bar{y} - a\,\bar{x}$ |
| Coefficient de corrélation | $r = \dfrac{\operatorname{cov}(x, y)}{\sigma_x\,\sigma_y}$ |

[IMAGE_3]

::: retenir
- La droite des moindres carrés passe toujours par le point moyen $G$.
- $-1 \leqslant r \leqslant 1$ : plus $\lvert r \rvert$ est proche de $1$, plus les points sont proches d’une droite. Sur la figure, $r \approx 0{,}997$.
:::
