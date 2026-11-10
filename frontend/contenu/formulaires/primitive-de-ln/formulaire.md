---
{
  "slug": "primitive-de-ln",
  "titre": "Primitive de ln(x)",
  "titreCourt": "Primitive de ln(x)",
  "titreSeo": "Primitive de ln(x) : formule, démonstration et exemples",
  "description": "La primitive de ln(x) est x ln(x) − x + C : démonstration par intégration par parties, vérification, primitives de ln(ax + b), ln(x)/x, x ln(x) et exemples.",
  "chapo": "La formule de la primitive de ln(x), sa démonstration par intégration par parties, les primitives voisines (ln(ax + b), ln(x)/x, x ln(x), ln²(x)…) et des intégrales calculées pas à pas.",
  "resume": "x ln x − x, démonstration, primitives voisines",
  "vignette": "aire_ln",
  "theme": "Analyse",
  "niveaux": ["Lycée", "Supérieur"],
  "ordre": 18,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["primitive de ln x", "primitive de ln", "primitive logarithme", "intégrale de ln x", "primitive de ln(x)/x", "primitive de x ln x", "primitive de ln(2x+1)", "intégration par parties ln"],
  "figures": [
    { "nom": "aire_ln", "alt": "Courbe de la fonction logarithme népérien ; le domaine coloré sous la courbe, entre x = 1 et x = e, a une aire égale à 1 unité d’aire." }
  ],
  "chapitresLies": [
    "terminale/primitives",
    "terminale/calcul-integral",
    "terminale/fonction-logarithme-neperien"
  ],
  "faq": [
    ["Quelle est la primitive de ln(x) ?", "Sur ]0 ; +∞[, les primitives de ln(x) sont les fonctions x ln(x) − x + C, où C est une constante réelle. On le vérifie en dérivant : (x ln x − x)′ = ln x + 1 − 1 = ln x."],
    ["Comment trouver la primitive de ln(x) ?", "Par intégration par parties, en écrivant ln x = 1 × ln x : on pose u = ln x et v′ = 1, donc u′ = 1/x et v = x. On obtient x ln x − ∫ 1 dx = x ln x − x."],
    ["Quelle est la primitive de ln(x)/x ?", "ln(x)/x est de la forme u′u avec u = ln x : une primitive est (ln x)²/2."],
    ["Quelle est la primitive de ln(2x + 1) ?", "Pour x > −1/2, une primitive est ½ [(2x + 1) ln(2x + 1) − (2x + 1)], d’après la formule de ln(ax + b) avec a = 2 et b = 1."],
    ["Pourquoi la primitive de ln(x) n’est-elle pas 1/x ?", "1/x est la dérivée de ln(x), pas sa primitive. La primitive va dans l’autre sens : c’est une fonction dont la dérivée vaut ln(x), à savoir x ln x − x."]
  ]
}
---
<!-- optitab:1 -->
## I. La formule {Lycée}

::: formule Primitive de $\ln x$ sur $]0\,;+\infty[$
$$\int \ln x \,\mathrm{d}x = x\ln x - x + C$$
:::

$C$ est une constante réelle quelconque : chaque valeur de $C$ donne une primitive. La plus utilisée est $F(x) = x\ln x - x$, que l’on écrit aussi $x(\ln x - 1)$.

::: retenir Vérification par la dérivée
$$(x\ln x - x)' = 1 \times \ln x + x \times \frac{1}{x} - 1 = \ln x$$
:::

::: attention Erreur fréquente
$\dfrac{1}{x}$ est la **dérivée** de $\ln x$, pas sa primitive. À l’inverse, $\ln x$ est une primitive de $\dfrac{1}{x}$.
:::

## II. Démonstration par intégration par parties {Lycée}

On écrit $\ln x = 1 \times \ln x$ et on applique la formule d’intégration par parties :
$$\int u\,v' = u\,v - \int u'\,v$$

| Choix | Dérivée ou primitive |
|---|---|
| $u(x) = \ln x$ | $u'(x) = \dfrac{1}{x}$ |
| $v'(x) = 1$ | $v(x) = x$ |

$$
\begin{aligned}
\int \ln x\,\mathrm{d}x &= x\ln x - \int x \times \frac{1}{x}\,\mathrm{d}x \\
&= x\ln x - \int 1\,\mathrm{d}x \\
&= x\ln x - x + C
\end{aligned}
$$

::: conseil Le réflexe à retenir
Devant un $\ln$ seul ou multiplié par un polynôme, on pose $u = \ln x$ : en le dérivant, le logarithme disparaît.
:::

## III. Primitives voisines {Lycée}

Sur $]0\,;+\infty[$ :

| Fonction | Une primitive |
|---|---|
| $\ln x$ | $x\ln x - x$ |
| $\dfrac{1}{x}$ | $\ln x$ |
| $\dfrac{\ln x}{x}$ | $\dfrac{(\ln x)^2}{2}$ |
| $x\ln x$ | $\dfrac{x^2}{2}\ln x - \dfrac{x^2}{4}$ |
| $(\ln x)^2$ | $x(\ln x)^2 - 2x\ln x + 2x$ |
| $\dfrac{\ln x}{x^2}$ | $-\dfrac{\ln x + 1}{x}$ |
| $\dfrac{1}{x\ln x}$ | $\ln(\ln x)$ |

La dernière ligne n’est valable que pour $x > 1$, car il faut $\ln x > 0$.

::: formule Primitive de $\ln(ax + b)$, avec $a \neq 0$ et $ax + b > 0$
En posant $t = ax + b$ :
$$\int \ln(ax + b)\,\mathrm{d}x = \frac{t\ln t - t}{a} + C$$
:::

::: exemple Primitive de $\ln(2x + 1)$ sur $\left]-\dfrac{1}{2}\,;+\infty\right[$
Avec $a = 2$ et $b = 1$ :
$$F(x) = \frac{1}{2}\Big[(2x + 1)\ln(2x + 1) - (2x + 1)\Big]$$
:::

## IV. Calculer une intégrale de $\ln$ {Lycée}

[IMAGE_1]

::: exemple Aire sous la courbe de $\ln$ entre $1$ et $\mathrm{e}$
$$
\begin{aligned}
\int_1^{\mathrm{e}} \ln x\,\mathrm{d}x &= \big[x\ln x - x\big]_1^{\mathrm{e}} \\
&= (\mathrm{e}\ln \mathrm{e} - \mathrm{e}) - (1 \times \ln 1 - 1) \\
&= (\mathrm{e} - \mathrm{e}) - (0 - 1) = 1
\end{aligned}
$$
Le domaine coloré a donc une aire de $1$ unité d’aire.
:::

::: exemple Intégrale de $\ln$ entre $1$ et $2$
$$
\begin{aligned}
\int_1^{2} \ln x\,\mathrm{d}x &= (2\ln 2 - 2) - (0 - 1) \\
&= 2\ln 2 - 1 \approx 0{,}386
\end{aligned}
$$
:::

::: retenir Valeurs à connaître
$\ln 1 = 0$ et $\ln \mathrm{e} = 1$ : ce sont elles qui simplifient presque tous les calculs.
:::

## V. Généralisations {Supérieur}

| Fonction | Une primitive |
|---|---|
| $\ln\lvert x \rvert$ | $x\ln\lvert x \rvert - x$ |
| $x^n \ln x$ ($n \neq -1$) | $\dfrac{x^{n+1}}{n + 1}\ln x - \dfrac{x^{n+1}}{(n + 1)^2}$ |
| $\log x = \dfrac{\ln x}{\ln 10}$ | $\dfrac{x\ln x - x}{\ln 10}$ |

::: propriete Intégrale généralisée en $0$
$x\ln x \to 0$ quand $x \to 0^+$, donc :
$$\int_0^1 \ln x\,\mathrm{d}x = \big[x\ln x - x\big]_0^1 = -1$$
:::
