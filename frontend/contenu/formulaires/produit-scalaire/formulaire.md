---
{
  "slug": "produit-scalaire",
  "titre": "Produit scalaire et géométrie repérée",
  "titreCourt": "Produit scalaire",
  "titreSeo": "Produit scalaire : formules, équations de droites, cercles, espace",
  "description": "Les formules du produit scalaire et de la géométrie repérée : vecteurs, orthogonalité, Al-Kashi, équations de droites, de cercles et de plans, espace.",
  "chapo": "Les quatre expressions du produit scalaire, ses propriétés, ses applications au triangle et les équations de droites, de cercles et de plans, du plan à l’espace.",
  "resume": "Produit scalaire, vecteur normal, droites, cercles, plans",
  "vignette": "droite_normale",
  "theme": "Géométrie",
  "niveaux": ["Lycée", "Supérieur"],
  "ordre": 15,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["produit scalaire formule", "produit scalaire coordonnées", "vecteurs orthogonaux", "vecteur normal", "équation cartésienne d'une droite", "équation d'un cercle", "équation d'un plan", "projeté orthogonal"],
  "figures": [
    { "nom": "projete_orthogonal", "alt": "Vecteurs AB et AC formant un angle θ, et H, projeté orthogonal de C sur la droite (AB) : le produit scalaire AB · AC est égal à AB · AH." },
    { "nom": "droite_normale", "alt": "Droite d’équation 2x − y − 1 = 0 passant par le point (1 ; 1), avec un vecteur directeur u(1 ; 2) le long de la droite et un vecteur normal n(−2 ; 1) perpendiculaire." }
  ],
  "chapitresLies": [
    "seconde/manipuler-les-vecteurs-du-plan",
    "seconde/representer-et-caracteriser-les-droites-du-plan",
    "premiere/calcul-vectoriel-et-produit-scalaire",
    "premiere/geometrie-reperee-dans-le-plan",
    "terminale/orthogonalite-et-distances-dans-l-espace",
    "terminale/representations-parametriques-et-equations-cartesiennes"
  ],
  "faq": [
    ["Comment calculer un produit scalaire avec les coordonnées ?", "Dans un repère orthonormé, si u a pour coordonnées (x ; y) et v (x′ ; y′), alors u · v = xx′ + yy′. Dans l’espace, on ajoute zz′."],
    ["Comment montrer que deux vecteurs sont orthogonaux ?", "Deux vecteurs sont orthogonaux si et seulement si leur produit scalaire est nul. Par exemple, u(1 ; 2) et v(−2 ; 1) sont orthogonaux car 1 × (−2) + 2 × 1 = 0."],
    ["Comment trouver l’équation d’une droite avec un vecteur normal ?", "Si n(a ; b) est normal à la droite, son équation est de la forme ax + by + c = 0. On trouve c en remplaçant x et y par les coordonnées d’un point de la droite."],
    ["Quelle est l’équation d’un cercle ?", "Le cercle de centre Ω(a ; b) et de rayon r a pour équation (x − a)² + (y − b)² = r² dans un repère orthonormé."]
  ]
}
---
<!-- optitab:1 -->
## I. Vecteurs dans un repère {Lycée}

Dans un repère orthonormé, avec $A(x_A\,;y_A)$ et $B(x_B\,;y_B)$ :

| Notion | Formule |
|---|---|
| Coordonnées de $\overrightarrow{AB}$ | $(x_B - x_A\,;\,y_B - y_A)$ |
| Milieu de $[AB]$ | $\left(\dfrac{x_A + x_B}{2}\,;\,\dfrac{y_A + y_B}{2}\right)$ |
| Norme de $\vec{u}(x\,;y)$ | $\lVert \vec{u} \rVert = \sqrt{x^2 + y^2}$ |
| Distance $AB$ | $\sqrt{(x_B - x_A)^2 + (y_B - y_A)^2}$ |
| Colinéarité de $\vec{u}(x\,;y)$ et $\vec{v}(x'\,;y')$ | $xy' - x'y = 0$ |

## II. Les expressions du produit scalaire {Lycée}

[IMAGE_1]

| Expression | Formule |
|---|---|
| Avec un angle | $\vec{u} \cdot \vec{v} = \lVert \vec{u} \rVert \times \lVert \vec{v} \rVert \times \cos\theta$ |
| Avec les coordonnées (repère orthonormé) | $\vec{u} \cdot \vec{v} = xx' + yy'$ |
| Avec les normes | $\vec{u} \cdot \vec{v} = \dfrac{1}{2}\left(\lVert \vec{u} + \vec{v} \rVert^2 - \lVert \vec{u} \rVert^2 - \lVert \vec{v} \rVert^2\right)$ |
| Avec un projeté orthogonal | $\overrightarrow{AB} \cdot \overrightarrow{AC} = \overrightarrow{AB} \cdot \overrightarrow{AH}$ |

::: retenir Signe avec le projeté orthogonal
$\overrightarrow{AB} \cdot \overrightarrow{AC} = AB \times AH$ si $H$ est du même côté que $B$ par rapport à $A$, et $-AB \times AH$ sinon.
:::

## III. Propriétés {Lycée}

| Propriété | Formule |
|---|---|
| Symétrie | $\vec{u} \cdot \vec{v} = \vec{v} \cdot \vec{u}$ |
| Bilinéarité | $\vec{u} \cdot (\vec{v} + k\vec{w}) = \vec{u} \cdot \vec{v} + k\,\vec{u} \cdot \vec{w}$ |
| Carré scalaire | $\vec{u} \cdot \vec{u} = \lVert \vec{u} \rVert^2$ |
| Orthogonalité | $\vec{u} \perp \vec{v} \iff \vec{u} \cdot \vec{v} = 0$ |
| Identité remarquable | $\lVert \vec{u} + \vec{v} \rVert^2 = \lVert \vec{u} \rVert^2 + 2\,\vec{u} \cdot \vec{v} + \lVert \vec{v} \rVert^2$ |
| Différence de carrés | $(\vec{u} + \vec{v}) \cdot (\vec{u} - \vec{v}) = \lVert \vec{u} \rVert^2 - \lVert \vec{v} \rVert^2$ |

## IV. Applications dans le triangle {Lycée}

Dans un triangle $ABC$, avec $a = BC$, $b = CA$, $c = AB$ et $I$ milieu de $[BC]$ :

| Résultat | Formule |
|---|---|
| Formule d’Al‑Kashi | $a^2 = b^2 + c^2 - 2bc\cos\widehat{A}$ |
| Théorème de la médiane | $AB^2 + AC^2 = 2AI^2 + \dfrac{BC^2}{2}$ |
| Avec le milieu $I$ de $[BC]$ | $\overrightarrow{MB} \cdot \overrightarrow{MC} = MI^2 - \dfrac{BC^2}{4}$ |
| Cercle de diamètre $[AB]$ | $M$ est sur le cercle $\iff \overrightarrow{MA} \cdot \overrightarrow{MB} = 0$ |

## V. Droites et cercles du plan {Lycée}

[IMAGE_2]

| Objet | Équation ou propriété |
|---|---|
| Droite de vecteur normal $\vec{n}(a\,;b)$ | $ax + by + c = 0$ |
| Vecteur directeur de cette droite | $\vec{u}(-b\,;a)$ |
| Droite $y = mx + p$ | vecteur directeur $\vec{u}(1\,;m)$, coefficient directeur $m$ |
| Droites perpendiculaires $y = mx + p$ et $y = m'x + p'$ | $mm' = -1$ |
| Cercle de centre $\Omega(a\,;b)$ et de rayon $r$ | $(x - a)^2 + (y - b)^2 = r^2$ |

::: exemple Droite de la figure
$\vec{n}(2\,;-1)$ est normal à la droite, donc son équation s’écrit $2x - y + c = 0$. Elle passe par $(1\,;1)$ : $2 - 1 + c = 0$, donc $c = -1$. Tout vecteur colinéaire à $\vec{n}$, comme $(-2\,;1)$, est aussi normal.
:::

## VI. Dans l’espace {Lycée}

Dans un repère orthonormé de l’espace, avec $\vec{u}(x\,;y\,;z)$ et $\vec{v}(x'\,;y'\,;z')$ :

| Notion | Formule |
|---|---|
| Produit scalaire | $\vec{u} \cdot \vec{v} = xx' + yy' + zz'$ |
| Norme | $\lVert \vec{u} \rVert = \sqrt{x^2 + y^2 + z^2}$ |
| Plan de vecteur normal $\vec{n}(a\,;b\,;c)$ | $ax + by + cz + d = 0$ |
| Droite passant par $A$, dirigée par $\vec{u}(\alpha\,;\beta\,;\gamma)$ | $x = x_A + t\alpha$, $y = y_A + t\beta$, $z = z_A + t\gamma$ ($t \in \mathbb{R}$) |
| Droite orthogonale à un plan | son vecteur directeur est normal au plan |

## VII. Distances, produit vectoriel {Supérieur}

| Notion | Formule |
|---|---|
| Distance de $M_0(x_0\,;y_0)$ à la droite $ax + by + c = 0$ | $\dfrac{\lvert a x_0 + b y_0 + c \rvert}{\sqrt{a^2 + b^2}}$ |
| Distance de $M_0(x_0\,;y_0\,;z_0)$ au plan $ax + by + cz + d = 0$ | $\dfrac{\lvert a x_0 + b y_0 + c z_0 + d \rvert}{\sqrt{a^2 + b^2 + c^2}}$ |
| Produit vectoriel | $\vec{u} \wedge \vec{v} = (yz' - zy'\,;\,zx' - xz'\,;\,xy' - yx')$ |
| Norme du produit vectoriel | $\lVert \vec{u} \wedge \vec{v} \rVert = \lVert \vec{u} \rVert\,\lVert \vec{v} \rVert\,\lvert \sin\theta \rvert$ |

La norme de $\vec{u} \wedge \vec{v}$ est l’aire du parallélogramme construit sur $\vec{u}$ et $\vec{v}$ ; $\vec{u} \wedge \vec{v}$ est orthogonal à $\vec{u}$ et à $\vec{v}$.
