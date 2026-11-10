---
{
  "slug": "fonctions-affines-equation-de-droite",
  "titre": "Fonctions affines et équations de droites",
  "titreCourt": "Fonctions affines, droites",
  "titreSeo": "Coefficient directeur et équation de droite : fonctions affines",
  "description": "Fonctions linéaires et affines, calcul du coefficient directeur, équation réduite et cartésienne d’une droite, droites parallèles et perpendiculaires, exemples.",
  "chapo": "Les formules des fonctions affines et des droites : coefficient directeur, ordonnée à l’origine, équation d’une droite passant par deux points, lecture graphique, parallélisme et intersection.",
  "resume": "Coefficient directeur, équation de droite",
  "vignette": "droite_affine",
  "theme": "Fonctions",
  "niveaux": ["Collège", "Lycée"],
  "ordre": 8,
  "publie": "2026-11-10",
  "modifie": "2026-11-10",
  "motsCles": ["coefficient directeur", "calculer le coefficient directeur", "équation de droite", "équation réduite d'une droite", "fonction affine", "fonction linéaire", "ordonnée à l'origine", "droite passant par deux points"],
  "figures": [
    { "nom": "droite_affine", "alt": "Droite d’équation y = 2x + 1 : elle coupe l’axe des ordonnées en 1, l’ordonnée à l’origine ; quand on avance de 1 vers la droite, elle monte de 2, le coefficient directeur." }
  ],
  "chapitresLies": [
    "3e/notion-de-fonction",
    "3e/fonctions-lineaires-et-affines",
    "seconde/representer-et-caracteriser-les-droites-du-plan",
    "seconde/se-constituer-un-repertoire-de-fonctions-de-reference",
    "premiere/geometrie-reperee-dans-le-plan"
  ],
  "faq": [
    ["Comment calculer le coefficient directeur d’une droite ?", "Avec deux points A et B de la droite : a = (y_B − y_A) ÷ (x_B − x_A). Pour A(1 ; 3) et B(4 ; 9), a = (9 − 3) ÷ (4 − 1) = 2."],
    ["Comment trouver l’équation d’une droite passant par deux points ?", "On calcule le coefficient directeur a, puis l’ordonnée à l’origine b en remplaçant x et y par les coordonnées d’un des points dans y = ax + b. Pour A(1 ; 3) et B(4 ; 9) : a = 2, puis 3 = 2 × 1 + b donne b = 1, donc y = 2x + 1."],
    ["Quelle est la différence entre fonction linéaire et fonction affine ?", "Une fonction affine s’écrit f(x) = ax + b. Une fonction linéaire est le cas particulier b = 0 : f(x) = ax. Sa droite passe par l’origine et elle traduit une situation de proportionnalité."],
    ["Quand deux droites sont-elles parallèles ?", "Deux droites non verticales sont parallèles si et seulement si elles ont le même coefficient directeur, comme y = 2x + 1 et y = 2x − 5."]
  ]
}
---
<!-- optitab:1 -->
## I. Fonctions linéaires et affines {Collège}

| Fonction | Expression | Courbe |
|---|---|---|
| Linéaire | $f(x) = ax$ | droite passant par l’origine |
| Affine | $f(x) = ax + b$ | droite coupant l’axe des ordonnées en $b$ |
| Constante | $f(x) = b$ | droite horizontale |

- $a$ est le **coefficient directeur** (ou pente) ;
- $b$ est l’**ordonnée à l’origine** : $f(0) = b$.

::: exemple $f(x) = 2x + 1$
L’image de $3$ est $f(3) = 2 \times 3 + 1 = 7$. L’antécédent de $9$ vérifie $2x + 1 = 9$, soit $x = 4$.
:::

::: retenir Linéaire et proportionnalité
Une fonction linéaire $f(x) = ax$ traduit une situation de **proportionnalité** de coefficient $a$.
:::

## II. Coefficient directeur {Collège}

[IMAGE_1]

::: formule Coefficient directeur de la droite passant par $A$ et $B$ ($x_A \neq x_B$)
$$a = \frac{y_B - y_A}{x_B - x_A}$$
:::

::: methode Lecture graphique
- On lit $b$ là où la droite coupe l’axe des ordonnées.
- Quand on avance de $1$ vers la droite, la droite monte de $a$ (ou descend si $a < 0$).
:::

::: propriete Variations et signe
- Si $a > 0$, $f$ est **croissante** ; si $a < 0$, elle est **décroissante** ; si $a = 0$, elle est constante.
- $ax + b$ s’annule en $x = -\dfrac{b}{a}$ et il est du signe de $a$ à droite de cette valeur.
:::

## III. Équation d’une droite {Lycée}

::: exemple Droite passant par $A(1\,;3)$ et $B(4\,;9)$
1. Coefficient directeur : $a = \dfrac{9 - 3}{4 - 1} = \dfrac{6}{3} = 2$.
2. Ordonnée à l’origine : $A$ est sur la droite, donc $3 = 2 \times 1 + b$, d’où $b = 1$.
3. Équation : $y = 2x + 1$. Vérification avec $B$ : $2 \times 4 + 1 = 9$.
:::

| Droite | Équation |
|---|---|
| De coefficient $m$, passant par $A(x_A\,;y_A)$ | $y = m(x - x_A) + y_A$ |
| Non verticale (équation réduite) | $y = mx + p$ |
| Verticale | $x = c$ |
| Équation cartésienne | $ax + by + c = 0$ |
| Vecteur directeur de $ax + by + c = 0$ | $\vec{u}\begin{pmatrix} -b \\ a \end{pmatrix}$ |
| Vecteur directeur de $y = mx + p$ | $\vec{u}\begin{pmatrix} 1 \\ m \end{pmatrix}$ |

::: exemple Droite de coefficient $-3$ passant par $A(2\,;-1)$
$$y = -3(x - 2) - 1 = -3x + 5$$
:::

## IV. Positions de deux droites {Lycée}

$d$ a pour équation $y = mx + p$ et $d'$ a pour équation $y = m'x + p'$.

| Position | Condition |
|---|---|
| Parallèles | $m = m'$ |
| Confondues | $m = m'$ et $p = p'$ |
| Sécantes | $m \neq m'$ |
| Perpendiculaires (repère orthonormé) | $m \times m' = -1$ |

::: exemple Point d’intersection de $y = 2x + 1$ et $y = -x + 7$
On résout $2x + 1 = -x + 7$ : $3x = 6$, donc $x = 2$, puis $y = 2 \times 2 + 1 = 5$. Les droites se coupent en $(2\,;5)$.
:::

::: conseil Appartenance d’un point
Un point appartient à la droite si ses coordonnées vérifient l’équation. $C(5\,;11)$ est sur $y = 2x + 1$, car $2 \times 5 + 1 = 11$.
:::
