---
{
  "slug": "methodes-d-integration",
  "titre": "Méthodes d’intégration",
  "titreCourt": "Méthodes d’intégration",
  "titreSeo": "Intégration par parties et changement de variable : formules",
  "description": "Les méthodes pour calculer une intégrale : intégration par parties (IPP), changement de variable, fractions rationnelles, parité, sommes de Riemann et exemples.",
  "chapo": "Comment calculer une intégrale quand aucune primitive ne saute aux yeux : intégration par parties, changement de variable, décomposition des fractions rationnelles et propriétés qui simplifient les calculs.",
  "resume": "IPP, changement de variable, fractions rationnelles",
  "vignette": "quart_disque",
  "theme": "Analyse",
  "niveaux": ["Lycée", "Supérieur"],
  "ordre": 19,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["intégration par parties", "formule intégration par parties", "IPP", "changement de variable intégrale", "calcul d'intégrale", "méthodes d'intégration", "intégrale de x e^x", "sommes de Riemann"],
  "figures": [
    { "nom": "quart_disque", "alt": "Quart de disque de rayon 1 sous la courbe y = √(1 − x²) entre 0 et 1 : son aire vaut π/4, ce que confirme le changement de variable x = sin t." },
    { "nom": "riemann", "alt": "Rectangles d’une somme de Riemann sous une courbe croissante : quand le nombre de rectangles augmente, la somme de leurs aires tend vers l’intégrale." }
  ],
  "chapitresLies": [
    "terminale/calcul-integral",
    "terminale/primitives"
  ],
  "faq": [
    ["Quelle est la formule de l’intégration par parties ?", "Pour u et v dérivables à dérivées continues sur [a ; b] : l’intégrale de a à b de u v′ est égale à [u v] de a à b moins l’intégrale de a à b de u′ v."],
    ["Comment choisir u et v′ dans une intégration par parties ?", "On choisit pour u le facteur qui se simplifie en le dérivant (ln x, un polynôme, arctan x) et pour v′ celui qui se primitive facilement (eˣ, cos x, sin x)."],
    ["Comment faire un changement de variable ?", "On pose x = φ(t), on remplace dx par φ′(t) dt et on change les bornes : si x va de a à b, t va de φ⁻¹(a) à φ⁻¹(b). On calcule ensuite l’intégrale en t."],
    ["Quelle est la primitive de x eˣ ?", "Par intégration par parties, avec u = x et v′ = eˣ, une primitive de x eˣ est (x − 1) eˣ."],
    ["L’intégration par parties est-elle au programme de Terminale ?", "Oui, l’intégration par parties fait partie du programme de Terminale spécialité maths. Le changement de variable et les fractions rationnelles relèvent du supérieur."]
  ]
}
---
<!-- optitab:1 -->
## I. Avant tout : reconnaître une forme {Lycée}

Avant une méthode plus longue, on vérifie si la fonction est une dérivée connue.

| Forme | Une primitive |
|---|---|
| $u'\,u^n$ ($n \neq -1$) | $\dfrac{u^{n+1}}{n + 1}$ |
| $\dfrac{u'}{u}$ ($u > 0$) | $\ln u$ |
| $u'\,\mathrm{e}^{u}$ | $\mathrm{e}^{u}$ |
| $\dfrac{u'}{\sqrt{u}}$ ($u > 0$) | $2\sqrt{u}$ |

::: exemple
$$\int_0^1 \frac{\mathrm{e}^x}{1 + \mathrm{e}^x}\,\mathrm{d}x = \Big[\ln(1 + \mathrm{e}^x)\Big]_0^1 = \ln(1 + \mathrm{e}) - \ln 2$$
:::

## II. Intégration par parties {Lycée}

::: formule Intégration par parties ($u$, $v$ de dérivées continues)
$$\int_a^b u\,v' = \Big[u\,v\Big]_a^b - \int_a^b u'\,v$$
:::

::: methode Choisir $u$ et $v'$
- $u$ : le facteur qui **se simplifie en le dérivant** ($\ln x$, un polynôme, $\arctan x$) ;
- $v'$ : le facteur qui **se primitive facilement** ($\mathrm{e}^x$, $\cos x$, $\sin x$).
:::

Les intégrations par parties classiques :

| Intégrande | Une primitive |
|---|---|
| $x\,\mathrm{e}^x$ | $(x - 1)\,\mathrm{e}^x$ |
| $x\cos x$ | $x\sin x + \cos x$ |
| $x\sin x$ | $\sin x - x\cos x$ |
| $\ln x$ | $x\ln x - x$ |
| $x\ln x$ | $\dfrac{x^2}{2}\ln x - \dfrac{x^2}{4}$ |
| $x^2\,\mathrm{e}^x$ | $(x^2 - 2x + 2)\,\mathrm{e}^x$ |
| $\mathrm{e}^x \cos x$ | $\dfrac{\mathrm{e}^x(\cos x + \sin x)}{2}$ |
| $\arctan x$ | $x\arctan x - \dfrac{1}{2}\ln(1 + x^2)$ |

Pour $\ln x$ et $\arctan x$, on pose $v' = 1$. Pour $x^2\,\mathrm{e}^x$ et $\mathrm{e}^x\cos x$, on fait deux intégrations par parties successives.

::: exemple Calculer $\displaystyle\int_0^{\pi} x\sin x\,\mathrm{d}x$
On pose $u(x) = x$ et $v'(x) = \sin x$, donc $u'(x) = 1$ et $v(x) = -\cos x$ :
$$
\begin{aligned}
\int_0^{\pi} x\sin x\,\mathrm{d}x &= \Big[-x\cos x\Big]_0^{\pi} + \int_0^{\pi} \cos x\,\mathrm{d}x \\
&= \pi + \Big[\sin x\Big]_0^{\pi} = \pi
\end{aligned}
$$
:::

::: conseil Vérifier le résultat
On dérive la primitive obtenue : $\big((x - 1)\,\mathrm{e}^x\big)' = \mathrm{e}^x + (x - 1)\,\mathrm{e}^x = x\,\mathrm{e}^x$.
:::

## III. Changement de variable {Supérieur}

::: formule Changement de variable ($\varphi$ de classe $C^1$, $f$ continue)
$$\int_{\varphi(\alpha)}^{\varphi(\beta)} f(x)\,\mathrm{d}x = \int_{\alpha}^{\beta} f\big(\varphi(t)\big)\,\varphi'(t)\,\mathrm{d}t$$
:::

::: methode Les trois remplacements
1. On pose $x = \varphi(t)$.
2. On remplace $\mathrm{d}x$ par $\varphi'(t)\,\mathrm{d}t$.
3. On change les bornes : $t$ va de $\alpha$ à $\beta$ quand $x$ va de $\varphi(\alpha)$ à $\varphi(\beta)$.
:::

[IMAGE_1]

::: exemple Aire du quart de disque : $\displaystyle\int_0^1 \sqrt{1 - x^2}\,\mathrm{d}x$
On pose $x = \sin t$, avec $t$ de $0$ à $\dfrac{\pi}{2}$, et $\mathrm{d}x = \cos t\,\mathrm{d}t$ :
$$
\begin{aligned}
\int_0^1 \sqrt{1 - x^2}\,\mathrm{d}x &= \int_0^{\pi/2} \cos^2 t\,\mathrm{d}t \\
&= \int_0^{\pi/2} \frac{1 + \cos 2t}{2}\,\mathrm{d}t = \frac{\pi}{4}
\end{aligned}
$$
:::

| On voit | On pose |
|---|---|
| $\sqrt{1 - x^2}$ | $x = \sin t$ |
| $\sqrt{1 + x^2}$ | $x = \operatorname{sh} t$ |
| $\dfrac{1}{1 + x^2}$ dans une fraction | $x = \tan t$ |
| $\sqrt{ax + b}$ | $t = \sqrt{ax + b}$ |
| une fraction en $\mathrm{e}^x$ | $t = \mathrm{e}^x$ |
| une fraction en $\cos x$ et $\sin x$ | $t = \tan\dfrac{x}{2}$ |

::: propriete Avec $t = \tan\dfrac{x}{2}$
$$\cos x = \frac{1 - t^2}{1 + t^2} \qquad \sin x = \frac{2t}{1 + t^2}$$
$$\mathrm{d}x = \frac{2\,\mathrm{d}t}{1 + t^2}$$
:::

## IV. Fractions rationnelles {Supérieur}

On décompose la fraction en **éléments simples**, puis on intègre chaque morceau.

| Fraction | Décomposition |
|---|---|
| $\dfrac{1}{x(x + 1)}$ | $\dfrac{1}{x} - \dfrac{1}{x + 1}$ |
| $\dfrac{1}{x^2 - 1}$ | $\dfrac{1}{2}\left(\dfrac{1}{x - 1} - \dfrac{1}{x + 1}\right)$ |

| Élément simple | Une primitive |
|---|---|
| $\dfrac{1}{x - a}$ | $\ln\lvert x - a \rvert$ |
| $\dfrac{1}{(x - a)^n}$ ($n \geqslant 2$) | $-\dfrac{1}{(n - 1)(x - a)^{n-1}}$ |
| $\dfrac{1}{x^2 + a^2}$ ($a > 0$) | $\dfrac{1}{a}\arctan\dfrac{x}{a}$ |

::: exemple
$$\int \frac{\mathrm{d}x}{x^2 - 1} = \frac{1}{2}\ln\left\lvert \frac{x - 1}{x + 1} \right\rvert + C$$
:::

## V. Propriétés qui simplifient les calculs {Lycée}

| Propriété | Formule |
|---|---|
| Fonction paire | $\displaystyle\int_{-a}^{a} f = 2\int_0^{a} f$ |
| Fonction impaire | $\displaystyle\int_{-a}^{a} f = 0$ |
| Fonction $T$-périodique | $\displaystyle\int_a^{a + T} f = \int_0^{T} f$ |
| Valeur absolue ($a \leqslant b$) | $\displaystyle\left\lvert \int_a^b f \right\rvert \leqslant \int_a^b \lvert f \rvert$ |
| Encadrement ($m \leqslant f \leqslant M$) | $m(b - a) \leqslant \displaystyle\int_a^b f \leqslant M(b - a)$ |

[IMAGE_2]

::: theoreme Sommes de Riemann ($f$ continue sur $[a\,;b]$)
Avec le pas $h = \dfrac{b - a}{n}$ :
$$\lim_{n \to +\infty} h\sum_{k=0}^{n-1} f(a + kh) = \int_a^b f(x)\,\mathrm{d}x$$
:::

::: exemple Une limite de somme
$$\frac{1}{n}\sum_{k=0}^{n-1} \frac{1}{1 + k/n} \xrightarrow[n \to +\infty]{} \int_0^1 \frac{\mathrm{d}x}{1 + x} = \ln 2$$
:::
