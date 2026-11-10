---
{
  "slug": "primitives",
  "titre": "Primitives et intégrales",
  "titreCourt": "Primitives et intégrales",
  "titreSeo": "Tableau des primitives usuelles et formules d’intégration",
  "description": "Le tableau des primitives usuelles et des fonctions composées, les propriétés de l’intégrale, l’intégration par parties, les équations différentielles.",
  "chapo": "Le tableau des primitives usuelles et des fonctions composées, puis le calcul intégral : propriétés, valeur moyenne, intégration par parties et équations différentielles.",
  "resume": "Tableau des primitives, intégrales, intégration par parties",
  "vignette": "aire_integrale",
  "theme": "Analyse",
  "niveaux": ["Lycée", "Supérieur"],
  "ordre": 17,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["tableau des primitives", "primitives usuelles", "primitive de 1/x", "formules d'intégration", "intégration par parties", "propriétés intégrale", "valeur moyenne", "équation différentielle y'=ay+b"],
  "figures": [
    { "nom": "aire_integrale", "alt": "Courbe d’une fonction positive f ; l’aire du domaine coloré entre la courbe, l’axe des abscisses et les droites x = a et x = b est l’intégrale de a à b de f(x) dx." }
  ],
  "chapitresLies": [
    "terminale/primitives",
    "terminale/calcul-integral",
    "terminale/equations-differentielles"
  ],
  "faq": [
    ["Quelle est la primitive de 1/x ?", "Sur ]0 ; +∞[, une primitive de 1/x est ln x. Sur ]−∞ ; 0[, c’est ln(−x). Les deux cas s’écrivent ln|x|."],
    ["Quelle est la différence entre une primitive et une intégrale ?", "Une primitive F de f est une fonction telle que F′ = f. L’intégrale de a à b de f est un nombre : F(b) − F(a). Si f est positive, elle mesure l’aire sous la courbe entre a et b."],
    ["Comment calculer une intégrale ?", "On cherche une primitive F de la fonction à intégrer, puis on calcule F(b) − F(a). Par exemple, l’intégrale de 0 à 1 de x² vaut 1³/3 − 0³/3 = 1/3."],
    ["Quand utiliser l’intégration par parties ?", "Quand on intègre un produit dont un facteur se simplifie en le dérivant (un polynôme, ln x) et dont l’autre se primitive facilement (eˣ, cos x, sin x). Par exemple pour x eˣ ou x cos x."]
  ]
}
---
<!-- optitab:1 -->
## I. Définition {Lycée}

::: definition Primitive
$F$ est une primitive de $f$ sur un intervalle $I$ si $F$ est dérivable sur $I$ et $F' = f$.
:::

::: retenir
- Si $F$ est une primitive de $f$, les autres primitives sont les fonctions $F + C$, avec $C$ réel.
- Il existe une seule primitive de $f$ qui prend une valeur donnée en un point donné.
:::

## II. Primitives usuelles {Lycée}

$C$ désigne une constante réelle, que l’on peut ajouter à chaque primitive.

| Fonction $f(x)$ | Primitive $F(x)$ | Sur |
|---|---|---|
| $a$ (constante) | $ax$ | $\mathbb{R}$ |
| $x$ | $\dfrac{x^2}{2}$ | $\mathbb{R}$ |
| $x^n$ ($n \geqslant 0$ entier) | $\dfrac{x^{n+1}}{n + 1}$ | $\mathbb{R}$ |
| $\dfrac{1}{x^2}$ | $-\dfrac{1}{x}$ | $]0\,;+\infty[$ |
| $\dfrac{1}{x^n}$ ($n \geqslant 2$) | $-\dfrac{1}{(n - 1)\,x^{n-1}}$ | $]0\,;+\infty[$ |
| $\dfrac{1}{\sqrt{x}}$ | $2\sqrt{x}$ | $]0\,;+\infty[$ |
| $\dfrac{1}{x}$ | $\ln x$ | $]0\,;+\infty[$ |
| $\mathrm{e}^x$ | $\mathrm{e}^x$ | $\mathbb{R}$ |
| $\mathrm{e}^{ax}$ ($a \neq 0$) | $\dfrac{\mathrm{e}^{ax}}{a}$ | $\mathbb{R}$ |
| $\cos x$ | $\sin x$ | $\mathbb{R}$ |
| $\sin x$ | $-\cos x$ | $\mathbb{R}$ |
| $\dfrac{1}{\cos^2 x}$ | $\tan x$ | $\left]-\dfrac{\pi}{2}\,;\dfrac{\pi}{2}\right[$ |

Les fonctions $\dfrac{1}{x^2}$, $\dfrac{1}{x^n}$ et $\dfrac{1}{x}$ ont aussi des primitives sur $]{-\infty}\,;0[$ : les mêmes formules, avec $\ln(-x)$ pour $\dfrac{1}{x}$.

::: conseil Vérifier une primitive
On dérive la primitive trouvée : on doit retrouver exactement la fonction de départ.
:::

## III. Primitives des fonctions composées {Lycée}

Pour $u$ dérivable sur $I$ :

| Fonction | Primitive | Condition |
|---|---|---|
| $u'\,u^n$ ($n \geqslant 0$ entier) | $\dfrac{u^{n+1}}{n + 1}$ | |
| $\dfrac{u'}{u^2}$ | $-\dfrac{1}{u}$ | $u \neq 0$ |
| $\dfrac{u'}{\sqrt{u}}$ | $2\sqrt{u}$ | $u > 0$ |
| $\dfrac{u'}{u}$ | $\ln u$ | $u > 0$ |
| $u'\,\mathrm{e}^{u}$ | $\mathrm{e}^{u}$ | |
| $u' \cos u$ | $\sin u$ | |
| $u' \sin u$ | $-\cos u$ | |
| $f(ax + b)$ | $\dfrac{1}{a}\,F(ax + b)$ | $a \neq 0$ |

::: exemple
$f(x) = 2x\,\mathrm{e}^{x^2}$ est de la forme $u'\,\mathrm{e}^u$ avec $u(x) = x^2$ : une primitive est $F(x) = \mathrm{e}^{x^2}$.
:::

## IV. Intégrales {Lycée}

::: formule Calcul d’une intégrale ($F$ primitive de $f$)
$$\int_a^b f(x)\,\mathrm{d}x = \big[F(x)\big]_a^b = F(b) - F(a)$$
:::

[IMAGE_1]

Si $f$ est positive sur $[a\,;b]$, l’intégrale est l’aire, en unités d’aire, du domaine compris entre la courbe, l’axe des abscisses et les droites d’équations $x = a$ et $x = b$.

| Propriété | Formule |
|---|---|
| Linéarité | $\displaystyle\int_a^b (\alpha f + \beta g) = \alpha\int_a^b f + \beta\int_a^b g$ |
| Relation de Chasles | $\displaystyle\int_a^b f + \int_b^c f = \int_a^c f$ |
| Positivité ($a \leqslant b$) | si $f \geqslant 0$ sur $[a\,;b]$, alors $\displaystyle\int_a^b f \geqslant 0$ |
| Croissance ($a \leqslant b$) | si $f \leqslant g$ sur $[a\,;b]$, alors $\displaystyle\int_a^b f \leqslant \int_a^b g$ |
| Valeur moyenne | $\mu = \dfrac{1}{b - a}\displaystyle\int_a^b f(x)\,\mathrm{d}x$ |
| Aire entre deux courbes ($f \geqslant g$) | $\displaystyle\int_a^b \big(f(x) - g(x)\big)\,\mathrm{d}x$ |

::: exemple
$$\int_0^1 x^2\,\mathrm{d}x = \left[\frac{x^3}{3}\right]_0^1 = \frac{1}{3} - 0 = \frac{1}{3}$$
:::

## V. Intégration par parties {Lycée}

::: formule Pour $u$ et $v$ dérivables, de dérivées continues
$$\int_a^b u\,v' = \big[u\,v\big]_a^b - \int_a^b u'\,v$$
:::

::: exemple Calculer $\displaystyle\int_0^1 x\,\mathrm{e}^x\,\mathrm{d}x$
On pose $u(x) = x$ et $v'(x) = \mathrm{e}^x$, donc $u'(x) = 1$ et $v(x) = \mathrm{e}^x$ :
$$
\begin{aligned}
\int_0^1 x\,\mathrm{e}^x\,\mathrm{d}x &= \big[x\,\mathrm{e}^x\big]_0^1 - \int_0^1 \mathrm{e}^x\,\mathrm{d}x \\
&= \mathrm{e} - (\mathrm{e} - 1) = 1
\end{aligned}
$$
:::

## VI. Équations différentielles {Lycée}

$C$ désigne une constante réelle.

| Équation | Solutions |
|---|---|
| $y' = ay$ | $y(x) = C\,\mathrm{e}^{ax}$ |
| $y' = ay + b$ ($a \neq 0$) | $y(x) = C\,\mathrm{e}^{ax} - \dfrac{b}{a}$ |
| $y' = ay + f$ | $y = y_p + C\,\mathrm{e}^{ax}$, où $y_p$ est une solution particulière |

La condition initiale $y(x_0) = y_0$ fixe la valeur de $C$.

## VII. Primitives du supérieur {Supérieur}

| Fonction | Primitive | Sur |
|---|---|---|
| $\dfrac{1}{x}$ | $\ln\lvert x \rvert$ | $]{-\infty}\,;0[$ ou $]0\,;+\infty[$ |
| $\dfrac{1}{1 + x^2}$ | $\arctan x$ | $\mathbb{R}$ |
| $\dfrac{1}{\sqrt{1 - x^2}}$ | $\arcsin x$ | $]-1\,;1[$ |
| $\ln x$ | $x\ln x - x$ | $]0\,;+\infty[$ |
| $\tan x$ | $-\ln(\cos x)$ | $\left]-\dfrac{\pi}{2}\,;\dfrac{\pi}{2}\right[$ |

::: propriete Changement de variable
Pour $\varphi$ dérivable, de dérivée continue sur $[a\,;b]$, et $f$ continue :
$$\int_a^b f\big(\varphi(t)\big)\,\varphi'(t)\,\mathrm{d}t = \int_{\varphi(a)}^{\varphi(b)} f(x)\,\mathrm{d}x$$
:::
