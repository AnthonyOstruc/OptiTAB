---
{
  "slug": "derivees",
  "titre": "Dérivées usuelles et formules de dérivation",
  "titreCourt": "Dérivées",
  "titreSeo": "Tableau des dérivées usuelles et formules de dérivation",
  "description": "Le tableau des dérivées usuelles et toutes les formules de dérivation : somme, produit, quotient, fonctions composées, tangente, variations et convexité.",
  "chapo": "Le tableau des dérivées des fonctions usuelles et toutes les règles de dérivation, de la tangente en un point aux fonctions composées et à la convexité.",
  "resume": "Tableau des dérivées, produit, quotient, composées",
  "vignette": "tangente",
  "theme": "Analyse",
  "niveaux": ["Lycée", "Supérieur"],
  "ordre": 7,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["tableau des dérivées", "dérivées usuelles", "formules de dérivation", "dérivée d'un quotient", "dérivée d'un produit", "dérivée de racine de x", "équation de la tangente", "dérivée fonction composée"],
  "figures": [
    { "nom": "tangente", "alt": "Courbe d’une fonction f et sa tangente T au point A d’abscisse a : quand on avance de 1 sur la tangente, on monte de f′(a), le coefficient directeur." }
  ],
  "chapitresLies": [
    "premiere/derivation-variations-et-courbes-representatives",
    "terminale/derivation-et-convexite"
  ],
  "faq": [
    ["Quelle est la dérivée de 1/x ?", "La dérivée de x ↦ 1/x est x ↦ −1/x², pour tout x non nul. Plus généralement, la dérivée de 1/v est −v′/v²."],
    ["Quelle est la dérivée de racine de x ?", "La dérivée de x ↦ √x est x ↦ 1/(2√x), pour x > 0. La fonction racine carrée n’est pas dérivable en 0."],
    ["Comment dériver un quotient ?", "Pour u et v dérivables avec v ≠ 0 : (u/v)′ = (u′v − uv′)/v². Pensez à ne pas développer le dénominateur v², utile pour étudier le signe."],
    ["Comment trouver l’équation de la tangente en un point ?", "La tangente à la courbe de f au point d’abscisse a a pour équation y = f′(a)(x − a) + f(a). Par exemple, pour f(x) = x² en a = 1 : y = 2(x − 1) + 1, soit y = 2x − 1."]
  ]
}
---
<!-- optitab:1 -->
## I. Nombre dérivé et tangente {Lycée}

::: definition Nombre dérivé
$f$ est dérivable en $a$ si le taux d’accroissement a une limite finie quand $h$ tend vers $0$ :
$$f'(a) = \lim_{h \to 0} \frac{f(a + h) - f(a)}{h}$$
:::

[IMAGE_1]

::: formule Équation de la tangente au point d’abscisse $a$
$$y = f'(a)(x - a) + f(a)$$
:::

Le nombre dérivé $f'(a)$ est le **coefficient directeur** de la tangente : quand $x$ augmente de $1$ sur la tangente, $y$ augmente de $f'(a)$.

## II. Dérivées des fonctions usuelles {Lycée}

| Fonction $f(x)$ | Dérivée $f'(x)$ | Pour |
|---|---|---|
| $k$ (constante) | $0$ | $x \in \mathbb{R}$ |
| $x$ | $1$ | $x \in \mathbb{R}$ |
| $ax + b$ | $a$ | $x \in \mathbb{R}$ |
| $x^2$ | $2x$ | $x \in \mathbb{R}$ |
| $x^3$ | $3x^2$ | $x \in \mathbb{R}$ |
| $x^n$ ($n \geqslant 1$ entier) | $nx^{n-1}$ | $x \in \mathbb{R}$ |
| $\dfrac{1}{x}$ | $-\dfrac{1}{x^2}$ | $x \neq 0$ |
| $\dfrac{1}{x^n}$ | $-\dfrac{n}{x^{n+1}}$ | $x \neq 0$ |
| $\sqrt{x}$ | $\dfrac{1}{2\sqrt{x}}$ | $x > 0$ |
| $\mathrm{e}^x$ | $\mathrm{e}^x$ | $x \in \mathbb{R}$ |
| $\ln x$ | $\dfrac{1}{x}$ | $x > 0$ |
| $\sin x$ | $\cos x$ | $x \in \mathbb{R}$ |
| $\cos x$ | $-\sin x$ | $x \in \mathbb{R}$ |
| $\tan x$ | $1 + \tan^2 x$ | $x \neq \dfrac{\pi}{2} + k\pi$ |

La dérivée de la tangente s’écrit aussi $\tan' x = \dfrac{1}{\cos^2 x}$.

## III. Règles de calcul {Lycée}

Pour $u$ et $v$ dérivables et $k$ réel :

| Opération | Dérivée |
|---|---|
| Somme | $(u + v)' = u' + v'$ |
| Produit par un réel | $(ku)' = k\,u'$ |
| Produit | $(uv)' = u'v + uv'$ |
| Inverse ($v \neq 0$) | $\left(\dfrac{1}{v}\right)' = -\dfrac{v'}{v^2}$ |
| Quotient ($v \neq 0$) | $\left(\dfrac{u}{v}\right)' = \dfrac{u'v - uv'}{v^2}$ |

::: attention Erreur fréquente
$(uv)' \neq u'v'$ : la dérivée d’un produit n’est pas le produit des dérivées.
:::

## IV. Fonctions composées {Lycée}

| Fonction | Dérivée |
|---|---|
| $f(ax + b)$ | $a\,f'(ax + b)$ |
| $u^n$ ($n \geqslant 1$ entier) | $n\,u'\,u^{n-1}$ |
| $\sqrt{u}$ (avec $u > 0$) | $\dfrac{u'}{2\sqrt{u}}$ |
| $\mathrm{e}^{u}$ | $u'\,\mathrm{e}^{u}$ |
| $\ln u$ (avec $u > 0$) | $\dfrac{u'}{u}$ |
| $\sin u$ | $u' \cos u$ |
| $\cos u$ | $-u' \sin u$ |
| $g \circ u$ | $u' \times g' \circ u$ |

::: exemple
$f(x) = \mathrm{e}^{x^2}$ : avec $u(x) = x^2$, on a $f'(x) = 2x\,\mathrm{e}^{x^2}$.
:::

## V. Dérivée, variations et convexité {Lycée}

::: retenir Signe de la dérivée et variations
Sur un intervalle $I$ :
- si $f' \geqslant 0$, $f$ est croissante ; si $f' \leqslant 0$, $f$ est décroissante ;
- si $f'$ s’annule en $a$ en changeant de signe, $f$ admet un extremum local en $a$.
:::

::: exemple $f(x) = x^3 - 3x$
$f'(x) = 3x^2 - 3 = 3(x - 1)(x + 1)$.

::: tableau
x : -\infty, -1, 1, +\infty
f'(x) : , +, z, -, z, +,
f(x) : -/-\infty, +/2, -/-2, +/+\infty
:::
:::

| Signe de $f''$ | Conséquence |
|---|---|
| $f'' \geqslant 0$ sur $I$ | $f$ est convexe : sa courbe est au-dessus de ses tangentes |
| $f'' \leqslant 0$ sur $I$ | $f$ est concave : sa courbe est en dessous de ses tangentes |
| $f''$ s’annule en changeant de signe | point d’inflexion |

## VI. Dérivées usuelles du supérieur {Supérieur}

| Fonction | Dérivée | Pour |
|---|---|---|
| $x^\alpha$ ($\alpha$ réel) | $\alpha\,x^{\alpha - 1}$ | $x > 0$ |
| $a^x$ ($a > 0$) | $(\ln a)\,a^x$ | $x \in \mathbb{R}$ |
| $\arctan x$ | $\dfrac{1}{1 + x^2}$ | $x \in \mathbb{R}$ |
| $\arcsin x$ | $\dfrac{1}{\sqrt{1 - x^2}}$ | $-1 < x < 1$ |
| $\arccos x$ | $-\dfrac{1}{\sqrt{1 - x^2}}$ | $-1 < x < 1$ |
| $\operatorname{ch} x$ | $\operatorname{sh} x$ | $x \in \mathbb{R}$ |
| $\operatorname{sh} x$ | $\operatorname{ch} x$ | $x \in \mathbb{R}$ |

::: propriete Formule de Leibniz
Pour $u$ et $v$ dérivables $n$ fois :
$$(uv)^{(n)} = \sum_{k=0}^{n} \binom{n}{k} u^{(k)}\,v^{(n-k)}$$
:::
