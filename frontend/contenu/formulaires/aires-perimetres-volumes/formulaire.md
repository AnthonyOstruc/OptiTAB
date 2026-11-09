---
{
  "slug": "aires-perimetres-volumes",
  "titre": "Aires, périmètres et volumes",
  "titreCourt": "Aires, périmètres et volumes",
  "titreSeo": "Formules d’aire, de périmètre et de volume : formulaire",
  "description": "Formules d’aire, de périmètre et de volume : carré, rectangle, triangle, disque, trapèze, cube, pavé, cylindre, cône, pyramide, boule. Avec schémas.",
  "chapo": "Les formules de périmètre, d’aire et de volume des figures et des solides usuels, chacune avec son schéma, et les conversions d’unités.",
  "resume": "Carré, rectangle, triangle, disque, cube, cylindre, cône, boule",
  "vignette": "pave_cylindre",
  "theme": "Grandeurs et mesures",
  "niveaux": ["Collège"],
  "ordre": 1,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["formule aire", "formule périmètre", "formule volume", "aire d'un disque", "volume d'un cylindre", "volume d'un cône", "volume d'une boule", "aire d'un trapèze", "conversion d'unités"],
  "figures": [
    { "nom": "carre_rectangle_disque", "alt": "Un carré de côté c, un rectangle de longueur L et de largeur ℓ, et un disque de centre O et de rayon r." },
    { "nom": "triangle_parallelogramme", "alt": "Un triangle et un parallélogramme de base b, avec leur hauteur h tracée en pointillés, perpendiculaire à la base." },
    { "nom": "trapeze_losange", "alt": "Un trapèze de grande base B, de petite base b et de hauteur h, et un losange avec ses diagonales D et d en pointillés." },
    { "nom": "pave_cylindre", "alt": "Un pavé droit de longueur L, de largeur ℓ et de hauteur h, et un cylindre de rayon r et de hauteur h, arêtes cachées en pointillés." },
    { "nom": "pyramide_cone", "alt": "Une pyramide à base carrée et un cône de rayon r, chacun avec sa hauteur h tracée en pointillés depuis le sommet." },
    { "nom": "prisme_boule", "alt": "Un prisme droit à base triangulaire de hauteur h, et une boule de centre O et de rayon r." }
  ],
  "chapitresLies": [
    "6e/perimetres",
    "6e/comparer-et-mesurer-des-aires",
    "5e/parallelogrammes-et-aires",
    "5e/solides-disques-et-volumes",
    "4e/pyramides-cones-et-volumes",
    "3e/geometrie-dans-l-espace"
  ],
  "faq": [
    ["Quelle est la formule de l’aire d’un disque ?", "L’aire d’un disque de rayon r est π × r². Par exemple, pour un rayon de 3 cm, l’aire vaut π × 9, soit environ 28,3 cm²."],
    ["Comment calculer le volume d’un cylindre ?", "On multiplie l’aire de la base, π × r², par la hauteur h : V = π × r² × h. Pour r = 2 cm et h = 5 cm, on obtient V = 20π, soit environ 62,8 cm³."],
    ["Quelle est la différence entre le périmètre et l’aire ?", "Le périmètre est la longueur du contour d’une figure (en cm, en m…). L’aire mesure la surface à l’intérieur (en cm², en m²…). Un carré de 3 cm de côté a un périmètre de 12 cm et une aire de 9 cm²."],
    ["Pourquoi divise-t-on par 3 pour une pyramide ou un cône ?", "Le volume d’une pyramide est le tiers du volume du prisme qui a la même base et la même hauteur. De même, le volume d’un cône est le tiers de celui du cylindre de même base et de même hauteur."]
  ]
}
---
<!-- optitab:1 -->
## I. Carré, rectangle et disque {Collège}

[IMAGE_1]

| Figure | Périmètre | Aire |
|---|---|---|
| Carré de côté $c$ | $4 \times c$ | $c \times c = c^2$ |
| Rectangle de longueur $L$ et de largeur $\ell$ | $2 \times (L + \ell)$ | $L \times \ell$ |
| Disque de rayon $r$ | $2 \times \pi \times r$ | $\pi \times r^2$ |

::: remarque
Le périmètre du disque est la longueur du cercle qui le borde. Avec le diamètre $d = 2r$, elle vaut aussi $\pi \times d$. On utilise souvent $\pi \approx 3{,}14$.
:::

## II. Triangle et parallélogramme {Collège}

[IMAGE_2]

| Figure | Périmètre | Aire |
|---|---|---|
| Triangle de base $b$ et de hauteur $h$ | somme des côtés | $\dfrac{b \times h}{2}$ |
| Triangle rectangle de côtés de l’angle droit $a$ et $b$ | somme des côtés | $\dfrac{a \times b}{2}$ |
| Parallélogramme de base $b$ et de hauteur $h$ | somme des côtés | $b \times h$ |

::: attention La hauteur n’est pas un côté
La hauteur $h$ est perpendiculaire à la base (en pointillés sur la figure). Pour l’aire d’un parallélogramme, on multiplie la base par la hauteur, pas par l’autre côté.
:::

## III. Trapèze et losange {Collège}

[IMAGE_3]

| Figure | Périmètre | Aire |
|---|---|---|
| Trapèze de bases $B$ et $b$, de hauteur $h$ | somme des côtés | $\dfrac{(B + b) \times h}{2}$ |
| Losange de côté $c$ et de diagonales $D$ et $d$ | $4 \times c$ | $\dfrac{D \times d}{2}$ |

## IV. Volumes des solides {Collège}

Dans ce tableau, $\mathcal{B}$ désigne l’aire de la base du solide.

[IMAGE_4]

| Solide | Volume |
|---|---|
| Cube d’arête $a$ | $a \times a \times a = a^3$ |
| Pavé droit de dimensions $L$, $\ell$ et $h$ | $L \times \ell \times h$ |
| Cylindre de rayon $r$ et de hauteur $h$ | $\pi \times r^2 \times h$ |

[IMAGE_5]

| Solide | Volume |
|---|---|
| Pyramide de hauteur $h$ | $\dfrac{\mathcal{B} \times h}{3}$ |
| Cône de rayon $r$ et de hauteur $h$ | $\dfrac{\pi \times r^2 \times h}{3}$ |

[IMAGE_6]

| Solide | Volume |
|---|---|
| Prisme droit de hauteur $h$ | $\mathcal{B} \times h$ |
| Boule de rayon $r$ | $\dfrac{4}{3} \times \pi \times r^3$ |

::: retenir
- Prisme droit et cylindre : volume $=$ aire de la base $\times$ hauteur.
- Pyramide et cône : volume $=$ (aire de la base $\times$ hauteur) $\div\ 3$, soit le tiers du prisme ou du cylindre de même base et de même hauteur.
:::

## V. Aires des solides {Collège}

| Solide | Aire |
|---|---|
| Cube d’arête $a$ | $6 \times a^2$ |
| Pavé droit de dimensions $L$, $\ell$ et $h$ | $2 \times (L\ell + Lh + \ell h)$ |
| Cylindre : aire latérale | $2 \times \pi \times r \times h$ |
| Cylindre : aire totale | $2\pi r h + 2\pi r^2$ |
| Sphère de rayon $r$ | $4 \times \pi \times r^2$ |

La sphère est la surface qui borde la boule : on calcule l’aire de la sphère et le volume de la boule.

## VI. Conversions d’unités {Collège}

| Grandeur | Correspondances |
|---|---|
| Longueurs | 1 km = 1 000 m ; 1 m = 10 dm = 100 cm = 1 000 mm |
| Aires | 1 m² = 100 dm² = 10 000 cm² ; 1 km² = 1 000 000 m² |
| Volumes | 1 m³ = 1 000 dm³ ; 1 dm³ = 1 000 cm³ |
| Contenances | 1 L = 1 dm³ ; 1 mL = 1 cm³ ; 1 m³ = 1 000 L |
| Surfaces agricoles | 1 ha = 10 000 m² ; 1 a = 100 m² |

::: conseil Le bon facteur
D’une unité à la suivante, on multiplie par $10$ pour les longueurs, par $100$ pour les aires et par $1\,000$ pour les volumes.
:::

## VII. Agrandissement et réduction {Collège}

Dans un agrandissement ou une réduction de rapport $k$ :

| Grandeur | Elle est multipliée par |
|---|---|
| Longueurs | $k$ |
| Aires | $k^2$ |
| Volumes | $k^3$ |
| Angles | $1$ (ils sont conservés) |

::: exemple
Si l’on double toutes les longueurs ($k = 2$), l’aire est multipliée par $2^2 = 4$ et le volume par $2^3 = 8$.
:::
