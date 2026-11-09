---
{
  "slug": "limites",
  "titre": "Limites et continuité",
  "titreCourt": "Limites et continuité",
  "titreSeo": "Limites : opérations, formes indéterminées, limites usuelles",
  "description": "Toutes les règles de calcul de limites : opérations, formes indéterminées, limites usuelles, croissances comparées, asymptotes, théorèmes de comparaison.",
  "chapo": "Les tableaux d’opérations sur les limites, les quatre formes indéterminées et les méthodes pour les lever, les limites usuelles, les asymptotes et les théorèmes à connaître.",
  "resume": "Opérations, formes indéterminées, asymptotes",
  "vignette": "asymptotes",
  "theme": "Analyse",
  "niveaux": ["Lycée", "Supérieur"],
  "ordre": 10,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["limites formules", "formes indéterminées", "opérations sur les limites", "limites usuelles", "croissances comparées", "asymptote horizontale verticale", "théorème des gendarmes", "théorème des valeurs intermédiaires"],
  "figures": [
    { "nom": "asymptotes", "alt": "Courbe de f(x) = (2x + 1)/(x − 1) avec une asymptote verticale d’équation x = 1 et une asymptote horizontale d’équation y = 2." }
  ],
  "chapitresLies": [
    "terminale/limites-des-fonctions",
    "terminale/limites-et-convergence-des-suites",
    "terminale/continuite-des-fonctions-d-une-variable-reelle"
  ],
  "faq": [
    ["Quelles sont les formes indéterminées ?", "Il y en a quatre : « ∞ − ∞ », « 0 × ∞ », « ∞/∞ » et « 0/0 ». Dans ces cas, les règles d’opérations ne permettent pas de conclure : il faut transformer l’expression (factoriser, utiliser la quantité conjuguée, un taux d’accroissement ou les croissances comparées)."],
    ["Comment calculer la limite d’un polynôme ou d’une fraction rationnelle en l’infini ?", "En ±∞, un polynôme a la même limite que son terme de plus haut degré, et une fraction rationnelle la même limite que le quotient des termes de plus haut degré du numérateur et du dénominateur. Par exemple, (2x² + 1)/(x² − 3) tend vers 2."],
    ["Comment trouver une asymptote ?", "Si f(x) tend vers ±∞ quand x tend vers a, la droite x = a est asymptote verticale. Si f(x) tend vers un réel ℓ en +∞ ou en −∞, la droite y = ℓ est asymptote horizontale."],
    ["À quoi sert le théorème des gendarmes ?", "Si une fonction est encadrée par deux fonctions qui ont la même limite ℓ, elle a aussi la limite ℓ. Par exemple, −1/x ≤ sin(x)/x ≤ 1/x pour x > 0, donc sin(x)/x tend vers 0 en +∞."]
  ]
}
---
<!-- optitab:1 -->
## I. Limites des fonctions de référence {Lycée}

| Fonction | En $+\infty$ | En $-\infty$ | En $0$ |
|---|---|---|---|
| $x^n$ ($n \geqslant 1$) | $+\infty$ | $+\infty$ si $n$ pair, $-\infty$ si $n$ impair | $0$ |
| $\dfrac{1}{x^n}$ ($n \geqslant 1$) | $0$ | $0$ | $+\infty$ en $0^+$ |
| $\dfrac{1}{x}$ | $0$ | $0$ | $+\infty$ en $0^+$, $-\infty$ en $0^-$ |
| $\sqrt{x}$ | $+\infty$ | non définie | $0$ |
| $\mathrm{e}^x$ | $+\infty$ | $0$ | $1$ |
| $\ln x$ | $+\infty$ | non définie | $-\infty$ en $0^+$ |

## II. Opérations sur les limites {Lycée}

$\ell$ et $\ell'$ désignent des réels. « FI » signale une forme indéterminée.

| $\lim f$ | $\lim g$ | $\lim (f + g)$ |
|---|---|---|
| $\ell$ | $\ell'$ | $\ell + \ell'$ |
| $\ell$ | $+\infty$ | $+\infty$ |
| $\ell$ | $-\infty$ | $-\infty$ |
| $+\infty$ | $+\infty$ | $+\infty$ |
| $-\infty$ | $-\infty$ | $-\infty$ |
| $+\infty$ | $-\infty$ | FI |

| $\lim f$ | $\lim g$ | $\lim (f \times g)$ |
|---|---|---|
| $\ell$ | $\ell'$ | $\ell \times \ell'$ |
| $\ell \neq 0$ | $\pm\infty$ | $\pm\infty$ (règle des signes) |
| $\pm\infty$ | $\pm\infty$ | $\pm\infty$ (règle des signes) |
| $0$ | $\pm\infty$ | FI |

| $\lim f$ | $\lim g$ | $\lim \dfrac{f}{g}$ |
|---|---|---|
| $\ell$ | $\ell' \neq 0$ | $\dfrac{\ell}{\ell'}$ |
| $\ell$ | $\pm\infty$ | $0$ |
| $\pm\infty$ | $\ell'$ | $\pm\infty$ (règle des signes) |
| $\ell \neq 0$ | $0$ (en gardant un signe) | $\pm\infty$ (règle des signes) |
| $0$ | $0$ | FI |
| $\pm\infty$ | $\pm\infty$ | FI |

## III. Lever une forme indéterminée {Lycée}

::: retenir Les quatre formes indéterminées
$\infty - \infty$, $\quad 0 \times \infty$, $\quad \dfrac{\infty}{\infty}$, $\quad \dfrac{0}{0}$
:::

| Méthode | Quand l’utiliser |
|---|---|
| Factoriser par le terme dominant | polynômes et fractions rationnelles en $\pm\infty$ |
| Quantité conjuguée | différence de racines carrées : $\sqrt{a} - \sqrt{b} = \dfrac{a - b}{\sqrt{a} + \sqrt{b}}$ |
| Taux d’accroissement | $\dfrac{0}{0}$ en un point : on reconnaît un nombre dérivé |
| Croissances comparées | produits ou quotients avec $\mathrm{e}^x$, $x^n$ et $\ln x$ |

::: exemple Fraction rationnelle en $+\infty$
$$\lim_{x \to +\infty} \frac{2x^2 + 1}{x^2 - 3} = \lim_{x \to +\infty} \frac{2x^2}{x^2} = 2$$
:::

## IV. Limites usuelles {Lycée}

| Limite | Valeur |
|---|---|
| $\displaystyle\lim_{x \to 0} \frac{\sin x}{x}$ | $1$ |
| $\displaystyle\lim_{x \to 0} \frac{\mathrm{e}^x - 1}{x}$ | $1$ |
| $\displaystyle\lim_{x \to 0} \frac{\ln(1 + x)}{x}$ | $1$ |
| $\displaystyle\lim_{x \to 0} \frac{1 - \cos x}{x^2}$ | $\dfrac{1}{2}$ |
| $\displaystyle\lim_{x \to +\infty} \frac{\mathrm{e}^x}{x^n}$ | $+\infty$ |
| $\displaystyle\lim_{x \to -\infty} x^n\,\mathrm{e}^x$ | $0$ |
| $\displaystyle\lim_{x \to +\infty} \frac{\ln x}{x^n}$ | $0$ |
| $\displaystyle\lim_{x \to 0^+} x^n \ln x$ | $0$ |

Dans ce tableau, $n \geqslant 1$ est un entier. La limite de $\dfrac{1 - \cos x}{x^2}$ s’obtient avec un développement limité (supérieur).

## V. Asymptotes {Lycée}

[IMAGE_1]

| Limite | Asymptote |
|---|---|
| $\displaystyle\lim_{x \to a} f(x) = \pm\infty$ | verticale, d’équation $x = a$ |
| $\displaystyle\lim_{x \to \pm\infty} f(x) = \ell$ | horizontale, d’équation $y = \ell$ |
| $\displaystyle\lim_{x \to \pm\infty} \big(f(x) - (ax + b)\big) = 0$ | oblique, d’équation $y = ax + b$ |

## VI. Théorèmes de comparaison {Lycée}

::: theoreme Comparaison
Si $f(x) \geqslant g(x)$ pour $x$ assez grand et $\displaystyle\lim_{x \to +\infty} g(x) = +\infty$, alors $\displaystyle\lim_{x \to +\infty} f(x) = +\infty$.
:::

::: theoreme Théorème des gendarmes
Si $g(x) \leqslant f(x) \leqslant h(x)$ pour $x$ assez grand et si $g$ et $h$ ont la même limite $\ell$ en $+\infty$, alors $\displaystyle\lim_{x \to +\infty} f(x) = \ell$.
:::

::: propriete Limite d’une composée
Si $\displaystyle\lim_{x \to a} u(x) = b$ et $\displaystyle\lim_{X \to b} v(X) = c$, alors $\displaystyle\lim_{x \to a} v\big(u(x)\big) = c$.
:::

Ces théorèmes valent aussi en $-\infty$, en un réel $a$, et pour les suites.

## VII. Continuité {Lycée}

::: theoreme Théorème des valeurs intermédiaires
Si $f$ est continue sur $[a\,;b]$, alors pour tout réel $k$ compris entre $f(a)$ et $f(b)$, l’équation $f(x) = k$ a au moins une solution dans $[a\,;b]$.
:::

::: retenir Cas d’une fonction strictement monotone
Si, de plus, $f$ est strictement monotone sur $[a\,;b]$, cette solution est **unique**.
:::

::: propriete Suites définies par $u_{n+1} = f(u_n)$
Si $(u_n)$ converge vers $\ell$ et si $f$ est continue en $\ell$, alors $\ell = f(\ell)$ : la limite est un point fixe de $f$.
:::
