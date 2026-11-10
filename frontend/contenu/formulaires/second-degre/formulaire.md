---
{
  "slug": "second-degre",
  "titre": "Second degré : discriminant et racines",
  "titreCourt": "Second degré",
  "titreSeo": "Second degré : discriminant, racines, forme canonique (formulaire)",
  "description": "Toutes les formules du second degré : discriminant, racines, forme canonique, factorisation, somme et produit des racines, signe et variations du trinôme.",
  "chapo": "Tout le second degré sur une page : les trois formes du trinôme, le discriminant, les racines, le signe et les variations, avec les schémas de la parabole.",
  "resume": "Discriminant Δ, racines, forme canonique, parabole",
  "vignette": "trois_cas",
  "theme": "Algèbre",
  "niveaux": ["Lycée"],
  "ordre": 9,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["second degré formule", "discriminant", "formule discriminant", "racines trinôme", "forme canonique", "équation du second degré", "signe d'un trinôme", "sommet parabole"],
  "figures": [
    { "nom": "trois_cas", "alt": "Trois paraboles tournées vers le haut : si Δ > 0 elle coupe l’axe des abscisses en deux racines x1 et x2, si Δ = 0 elle le touche en une racine x0, si Δ < 0 elle ne le coupe pas." },
    { "nom": "parabole_sommet", "alt": "Parabole de sommet S(α ; β), d’axe de symétrie la droite d’équation x = α, coupant l’axe des abscisses en x1 et x2." }
  ],
  "chapitresLies": [
    "premiere/equations-fonctions-polynomes-du-second-degre",
    "seconde/se-constituer-un-repertoire-de-fonctions-de-reference",
    "terminale/nombres-complexes"
  ],
  "faq": [
    ["Comment calculer le discriminant ?", "Pour ax² + bx + c avec a ≠ 0, le discriminant vaut Δ = b² − 4ac. Par exemple, pour 2x² − 3x − 2, Δ = (−3)² − 4 × 2 × (−2) = 9 + 16 = 25."],
    ["Que faire si le discriminant est négatif ?", "Si Δ < 0, l’équation ax² + bx + c = 0 n’a aucune solution réelle et le trinôme garde le signe de a. Avec les nombres complexes, elle a deux solutions conjuguées : (−b ± i√(−Δ)) / (2a)."],
    ["Comment trouver le sommet d’une parabole ?", "Le sommet a pour abscisse α = −b / (2a) et pour ordonnée β = f(α). C’est le minimum de la fonction si a > 0, le maximum si a < 0."],
    ["Quel est le signe d’un trinôme du second degré ?", "Il est du signe de a, sauf entre ses deux racines quand Δ > 0, où il est du signe opposé. Si Δ ≤ 0, il est du signe de a sur tout ℝ (et nul en la racine double si Δ = 0)."]
  ]
}
---
<!-- optitab:1 -->
## I. Les trois formes d’un trinôme {Lycée}

On étudie $f(x) = ax^2 + bx + c$, avec $a \neq 0$.

| Forme | Écriture |
|---|---|
| Développée | $f(x) = ax^2 + bx + c$ |
| Canonique | $f(x) = a(x - \alpha)^2 + \beta$ |
| Factorisée (si $\Delta \geqslant 0$) | $f(x) = a(x - x_1)(x - x_2)$ |

::: propriete Coordonnées du sommet
$$\alpha = -\frac{b}{2a} \qquad \beta = f(\alpha) = -\frac{\Delta}{4a}$$
:::

## II. Discriminant et racines {Lycée}

::: formule Discriminant
$$\Delta = b^2 - 4ac$$
:::

[IMAGE_1]

| Discriminant | Solutions de $ax^2 + bx + c = 0$ |
|---|---|
| $\Delta > 0$ | deux racines : $x_1 = \dfrac{-b - \sqrt{\Delta}}{2a}$ et $x_2 = \dfrac{-b + \sqrt{\Delta}}{2a}$ |
| $\Delta = 0$ | une racine double : $x_0 = -\dfrac{b}{2a}$ |
| $\Delta < 0$ | aucune racine réelle |

| Discriminant | Factorisation |
|---|---|
| $\Delta > 0$ | $f(x) = a(x - x_1)(x - x_2)$ |
| $\Delta = 0$ | $f(x) = a(x - x_0)^2$ |
| $\Delta < 0$ | pas de factorisation dans $\mathbb{R}$ |

::: exemple Résoudre $2x^2 - 3x - 2 = 0$
$\Delta = (-3)^2 - 4 \times 2 \times (-2) = 25 > 0$, donc deux racines :
$$x_1 = \frac{3 - 5}{4} = -\frac{1}{2} \qquad x_2 = \frac{3 + 5}{4} = 2$$
:::

## III. Somme et produit des racines {Lycée}

Quand $\Delta \geqslant 0$ :

| Relation | Formule |
|---|---|
| Somme des racines | $x_1 + x_2 = -\dfrac{b}{a}$ |
| Produit des racines | $x_1 \times x_2 = \dfrac{c}{a}$ |

::: conseil Racine évidente
- Si $a + b + c = 0$, alors $1$ est racine, et l’autre racine vaut $\dfrac{c}{a}$.
- Exemple : pour $x^2 - 5x + 4$, on a $1 - 5 + 4 = 0$, donc les racines sont $1$ et $4$.
- Deux nombres de somme $S$ et de produit $P$ sont les solutions de $x^2 - Sx + P = 0$.
:::

## IV. Signe du trinôme {Lycée}

::: retenir
$f(x)$ est **du signe de $a$**, sauf entre les racines (quand $\Delta > 0$), où il est du signe de $-a$.
:::

Exemple avec $a > 0$ et $\Delta > 0$ :

::: tableau
x : -\infty, x_1, x_2, +\infty
f(x) : , +, z, -, z, +,
:::

- Si $\Delta = 0$ : $f(x)$ est du signe de $a$ et s’annule seulement en $x_0$.
- Si $\Delta < 0$ : $f(x)$ est du signe de $a$ pour tout réel $x$.

## V. Variations et parabole {Lycée}

[IMAGE_2]

La courbe de $f$ est une **parabole** de sommet $S(\alpha\,;\beta)$ et d’axe de symétrie la droite d’équation $x = \alpha$. Elle est tournée vers le haut si $a > 0$, vers le bas si $a < 0$.

Variations pour $a > 0$ (minimum $\beta$ atteint en $\alpha$) :

::: tableau
x : -\infty, \alpha, +\infty
f(x) : +/+\infty, -/\beta, +/+\infty
:::

Si $a < 0$, les variations sont inversées : $f$ admet un maximum $\beta$ en $\alpha$.

## VI. Équations qui se ramènent au second degré {Lycée}

::: methode Équation bicarrée $ax^4 + bx^2 + c = 0$
On pose $X = x^2$, on résout $aX^2 + bX + c = 0$, puis on garde les solutions $X \geqslant 0$ : chacune donne $x = \sqrt{X}$ ou $x = -\sqrt{X}$.
:::

::: methode Inéquation $ax^2 + bx + c > 0$
On calcule $\Delta$ et les racines, on dresse le tableau de signes, puis on lit les intervalles où le trinôme est strictement positif.
:::

## VII. Racines complexes {Lycée}

En maths expertes, si $\Delta < 0$, l’équation $az^2 + bz + c = 0$ (à coefficients réels) a deux solutions complexes conjuguées :
$$z_1 = \frac{-b - \mathrm{i}\sqrt{-\Delta}}{2a} \qquad z_2 = \frac{-b + \mathrm{i}\sqrt{-\Delta}}{2a}$$
