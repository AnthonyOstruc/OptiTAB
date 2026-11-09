---
{
  "slug": "equivalents-usuels",
  "titre": "Équivalents usuels",
  "titreCourt": "Équivalents usuels",
  "titreSeo": "Équivalents usuels : tableau en 0 et en l’infini, règles de calcul",
  "description": "Le tableau des équivalents usuels en 0 (sin, tan, ln(1 + x), eˣ − 1, 1 − cos x…) et en l’infini, les règles de calcul et les pièges, avec exemples.",
  "chapo": "Les équivalents à connaître en 0 et en l’infini, les opérations autorisées et interdites, et leur usage pour calculer des limites en quelques lignes.",
  "resume": "sin x ~ x, ln(1 + x) ~ x, règles, Stirling",
  "vignette": "sinus_equivalent",
  "theme": "Analyse",
  "niveaux": ["Supérieur"],
  "ordre": 26,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["équivalents usuels", "équivalent en 0", "tableau des équivalents", "sin x équivalent à x", "ln(1+x) équivalent", "règles équivalents", "formule de Stirling", "calcul de limite avec équivalents"],
  "figures": [
    { "nom": "sinus_equivalent", "alt": "Courbes de y = sin x et de y = x : elles se confondent au voisinage de 0, ce qui traduit l’équivalent sin x ~ x en 0, puis s’écartent loin de 0." }
  ],
  "chapitresLies": [
    "terminale/limites-des-fonctions"
  ],
  "faq": [
    ["Que signifie f ~ g ?", "f est équivalente à g en a si le quotient f(x)/g(x) tend vers 1 quand x tend vers a (g ne s’annulant pas près de a). Deux fonctions équivalentes ont alors la même limite."],
    ["Quel est l’équivalent de sin x en 0 ?", "sin x ~ x en 0, car sin x / x tend vers 1. De même tan x ~ x, ln(1 + x) ~ x et eˣ − 1 ~ x."],
    ["Peut-on additionner des équivalents ?", "Non. On peut multiplier, diviser ou élever à une puissance fixe des équivalents, mais pas les additionner : sin x − x n’est pas équivalent à x − x = 0, il est équivalent à −x³/6."],
    ["Comment calculer une limite avec des équivalents ?", "On remplace chaque facteur par un équivalent simple, puis on simplifie. Par exemple, en 0, sin(3x)/ln(1 + 2x) est équivalent à 3x/(2x) = 3/2, qui est donc la limite."]
  ]
}
---
<!-- optitab:1 -->
## I. Définition {Supérieur}

::: definition Fonctions équivalentes
$f$ est équivalente à $g$ en $a$, ce que l’on note $f \underset{a}{\sim} g$, si $g$ ne s’annule pas au voisinage de $a$ (sauf peut-être en $a$) et si :
$$\lim_{x \to a} \frac{f(x)}{g(x)} = 1$$
:::

::: retenir Pourquoi c’est utile
Si $f \underset{a}{\sim} g$ et si $g$ a une limite en $a$, alors $f$ a la même limite. On remplace une expression compliquée par une expression simple.
:::

## II. Équivalents usuels en $0$ {Supérieur}

[IMAGE_1]

| Fonction | Équivalent en $0$ |
|---|---|
| $\sin x$ | $x$ |
| $\tan x$ | $x$ |
| $\arcsin x$ | $x$ |
| $\arctan x$ | $x$ |
| $\operatorname{sh} x$ | $x$ |
| $\ln(1 + x)$ | $x$ |
| $\mathrm{e}^x - 1$ | $x$ |
| $a^x - 1$ ($a > 0$, $a \neq 1$) | $x\ln a$ |
| $(1 + x)^\alpha - 1$ ($\alpha \neq 0$) | $\alpha x$ |
| $\sqrt{1 + x} - 1$ | $\dfrac{x}{2}$ |
| $1 - \cos x$ | $\dfrac{x^2}{2}$ |
| $\operatorname{ch} x - 1$ | $\dfrac{x^2}{2}$ |
| $x - \sin x$ | $\dfrac{x^3}{6}$ |
| $\tan x - x$ | $\dfrac{x^3}{3}$ |

::: propriete Avec une fonction $u$ qui tend vers $0$
Si $u(x) \to 0$ quand $x \to a$, on remplace $x$ par $u(x)$ : par exemple $\sin u(x) \underset{a}{\sim} u(x)$ et $\ln\big(1 + u(x)\big) \underset{a}{\sim} u(x)$.
:::

## III. Équivalents en l’infini {Supérieur}

| Fonction | Équivalent |
|---|---|
| Polynôme $a_p x^p + \dots + a_0$ ($a_p \neq 0$) | $a_p x^p$ |
| Fraction $\dfrac{a_p x^p + \dots}{b_q x^q + \dots}$ | $\dfrac{a_p x^p}{b_q x^q}$ |
| $\ln\left(1 + \dfrac{1}{x}\right)$ | $\dfrac{1}{x}$ |
| $\operatorname{ch} x$ et $\operatorname{sh} x$ (en $+\infty$) | $\dfrac{\mathrm{e}^x}{2}$ |
| $\ln(x + 1)$ | $\ln x$ |

| Suite | Équivalent |
|---|---|
| Formule de Stirling | $n! \sim \sqrt{2\pi n}\left(\dfrac{n}{\mathrm{e}}\right)^n$ |
| Série harmonique | $\displaystyle\sum_{k=1}^{n} \frac{1}{k} \sim \ln n$ |

## IV. Règles de calcul {Supérieur}

| Opération | Autorisée ? |
|---|---|
| Produit : $f_1 f_2 \sim g_1 g_2$ | oui |
| Quotient : $\dfrac{f_1}{f_2} \sim \dfrac{g_1}{g_2}$ | oui |
| Puissance fixe : $f^\alpha \sim g^\alpha$ | oui |
| Somme : $f_1 + f_2 \sim g_1 + g_2$ | **non** |
| Composition : $\mathrm{e}^{f} \sim \mathrm{e}^{g}$ | **non** en général |

::: attention Erreur fréquente
On n’additionne jamais des équivalents. En $0$, $\sin x \sim x$, mais $\sin x - x$ n’est pas équivalent à $0$ : il est équivalent à $-\dfrac{x^3}{6}$. Pour une somme, on passe par les développements limités.
:::

::: attention Exponentielle
$x^2 + x \underset{+\infty}{\sim} x^2$, mais $\mathrm{e}^{x^2 + x}$ n’est pas équivalent à $\mathrm{e}^{x^2}$ : leur quotient $\mathrm{e}^{x}$ tend vers $+\infty$.
:::

## V. Calculer une limite {Supérieur}

::: exemple Limite en $0$ de $\dfrac{\sin(3x)}{\ln(1 + 2x)}$
$\sin(3x) \sim 3x$ et $\ln(1 + 2x) \sim 2x$, donc :
$$\frac{\sin(3x)}{\ln(1 + 2x)} \sim \frac{3x}{2x} = \frac{3}{2}$$
La limite vaut $\dfrac{3}{2}$.
:::

::: exemple Limite en $0$ de $\dfrac{1 - \cos x}{x \tan x}$
$1 - \cos x \sim \dfrac{x^2}{2}$ et $x\tan x \sim x^2$, donc le quotient est équivalent à $\dfrac{1}{2}$ : la limite vaut $\dfrac{1}{2}$.
:::

::: exemple Limite en $+\infty$ de $x\ln\left(1 + \dfrac{1}{x}\right)$
$\ln\left(1 + \dfrac{1}{x}\right) \sim \dfrac{1}{x}$, donc $x\ln\left(1 + \dfrac{1}{x}\right) \sim 1$ : la limite vaut $1$.
:::
