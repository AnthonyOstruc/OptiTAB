---
{
  "slug": "developpements-limites",
  "titre": "Développements limités usuels",
  "titreCourt": "Développements limités",
  "titreSeo": "Développements limités usuels en 0 : formulaire (DL)",
  "description": "Les développements limités usuels en 0 : exponentielle, logarithme, (1 + x) puissance α, sinus, cosinus, tangente, arctangente, opérations, équivalents.",
  "chapo": "Les DL usuels en 0, avec leurs premiers termes et leur forme générale, les règles de calcul sur les développements limités et les équivalents usuels.",
  "resume": "DL en 0 de eˣ, ln(1 + x), sin, cos, équivalents",
  "vignette": "dl_exp",
  "theme": "Analyse",
  "niveaux": ["Supérieur"],
  "ordre": 14,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["développements limités usuels", "DL usuels", "développement limité en 0", "formule de Taylor-Young", "DL exponentielle", "DL ln(1+x)", "DL sinus cosinus", "équivalents usuels"],
  "figures": [
    { "nom": "dl_exp", "alt": "Courbe de l’exponentielle et ses approximations près de 0 : la droite y = 1 + x (ordre 1) et la parabole y = 1 + x + x²/2 (ordre 2), de plus en plus proches de la courbe au voisinage de 0." }
  ],
  "chapitresLies": [
    "terminale/limites-des-fonctions"
  ],
  "faq": [
    ["Qu’est-ce qu’un développement limité ?", "Un développement limité de f à l’ordre n en 0 est une écriture f(x) = a₀ + a₁x + … + aₙxⁿ + o(xⁿ) : un polynôme de degré au plus n qui approche f près de 0, avec une erreur négligeable devant xⁿ."],
    ["Comment retenir les développements limités usuels ?", "Ils viennent de la formule de Taylor-Young : le coefficient de xᵏ est f⁽ᵏ⁾(0)/k!. La parité aide : sin, tan, arctan et sh n’ont que des puissances impaires, cos et ch que des puissances paires. On retrouve aussi ln(1 + x) et arctan x en intégrant les DL de 1/(1 + x) et 1/(1 + x²)."],
    ["Quelle est la différence entre un développement limité et un équivalent ?", "L’équivalent en 0 est le premier terme non nul du développement limité. Par exemple, cos x = 1 − x²/2 + o(x²) donne 1 − cos x ∼ x²/2."],
    ["Peut-on additionner des équivalents ?", "Non : les équivalents se multiplient et se divisent, mais ne s’additionnent pas. Pour une somme ou une différence, on utilise les développements limités."]
  ]
}
---
<!-- optitab:1 -->
## I. Formule de Taylor-Young {Supérieur}

::: definition Petit o
$f(x) = o(x^n)$ en $0$ signifie que $\dfrac{f(x)}{x^n} \to 0$ quand $x \to 0$ : $f(x)$ est négligeable devant $x^n$.
:::

::: theoreme Formule de Taylor-Young
Si $f$ est de classe $\mathcal{C}^n$ au voisinage de $0$ :
$$f(x) = \sum_{k=0}^{n} \frac{f^{(k)}(0)}{k!}\,x^k + o(x^n)$$
:::

[IMAGE_1]

Plus l’ordre augmente, plus le polynôme colle à la courbe au voisinage de $0$.

## II. DL usuels en 0 : premiers termes {Supérieur}

| Fonction | Développement limité en $0$ |
|---|---|
| $\mathrm{e}^x$ | $1 + x + \dfrac{x^2}{2} + \dfrac{x^3}{6} + o(x^3)$ |
| $\ln(1 + x)$ | $x - \dfrac{x^2}{2} + \dfrac{x^3}{3} + o(x^3)$ |
| $\dfrac{1}{1 - x}$ | $1 + x + x^2 + x^3 + o(x^3)$ |
| $\dfrac{1}{1 + x}$ | $1 - x + x^2 - x^3 + o(x^3)$ |
| $\sqrt{1 + x}$ | $1 + \dfrac{x}{2} - \dfrac{x^2}{8} + o(x^2)$ |
| $\dfrac{1}{\sqrt{1 + x}}$ | $1 - \dfrac{x}{2} + \dfrac{3x^2}{8} + o(x^2)$ |
| $(1 + x)^\alpha$ | $1 + \alpha x + \dfrac{\alpha(\alpha - 1)}{2}x^2 + o(x^2)$ |
| $\sin x$ | $x - \dfrac{x^3}{6} + \dfrac{x^5}{120} + o(x^5)$ |
| $\cos x$ | $1 - \dfrac{x^2}{2} + \dfrac{x^4}{24} + o(x^4)$ |
| $\tan x$ | $x + \dfrac{x^3}{3} + \dfrac{2x^5}{15} + o(x^5)$ |
| $\arctan x$ | $x - \dfrac{x^3}{3} + \dfrac{x^5}{5} + o(x^5)$ |
| $\arcsin x$ | $x + \dfrac{x^3}{6} + \dfrac{3x^5}{40} + o(x^5)$ |
| $\operatorname{sh} x$ | $x + \dfrac{x^3}{6} + \dfrac{x^5}{120} + o(x^5)$ |
| $\operatorname{ch} x$ | $1 + \dfrac{x^2}{2} + \dfrac{x^4}{24} + o(x^4)$ |

## III. DL usuels à l’ordre n {Supérieur}

| Fonction | Développement limité en $0$ |
|---|---|
| $\mathrm{e}^x$ | $\displaystyle\sum_{k=0}^{n} \frac{x^k}{k!} + o(x^n)$ |
| $\ln(1 + x)$ | $\displaystyle\sum_{k=1}^{n} \frac{(-1)^{k+1}}{k}\,x^k + o(x^n)$ |
| $\dfrac{1}{1 - x}$ | $\displaystyle\sum_{k=0}^{n} x^k + o(x^n)$ |
| $(1 + x)^\alpha$ | $\displaystyle\sum_{k=0}^{n} \binom{\alpha}{k} x^k + o(x^n)$ |
| $\sin x$ | $\displaystyle\sum_{k=0}^{n} \frac{(-1)^k}{(2k + 1)!}\,x^{2k+1} + o(x^{2n+2})$ |
| $\cos x$ | $\displaystyle\sum_{k=0}^{n} \frac{(-1)^k}{(2k)!}\,x^{2k} + o(x^{2n+1})$ |
| $\arctan x$ | $\displaystyle\sum_{k=0}^{n} \frac{(-1)^k}{2k + 1}\,x^{2k+1} + o(x^{2n+2})$ |
| $\operatorname{sh} x$ | $\displaystyle\sum_{k=0}^{n} \frac{x^{2k+1}}{(2k + 1)!} + o(x^{2n+2})$ |
| $\operatorname{ch} x$ | $\displaystyle\sum_{k=0}^{n} \frac{x^{2k}}{(2k)!} + o(x^{2n+1})$ |

Avec $\dbinom{\alpha}{k} = \dfrac{\alpha(\alpha - 1)\cdots(\alpha - k + 1)}{k!}$ pour $\alpha$ réel.

## IV. Opérations sur les DL {Supérieur}

| Opération | Règle |
|---|---|
| Somme | On ajoute les DL écrits au même ordre. |
| Produit | On multiplie, puis on ne garde que les termes de degré au plus $n$. |
| Composition | Si $u(x) \to 0$, on remplace dans le DL de $f$, puis on tronque. |
| Quotient | On écrit $\dfrac{1}{1 + u}$ avec $u \to 0$ et on utilise le DL de $\dfrac{1}{1 + u}$. |
| Primitive | On intègre terme à terme, sans oublier la constante $f(0)$. |
| DL au point $a$ | On pose $x = a + h$ et on fait un DL en $h = 0$. |

::: exemple DL de $\mathrm{e}^x \sin x$ à l’ordre 3
$$
\begin{aligned}
\mathrm{e}^x \sin x &= \left(1 + x + \frac{x^2}{2}\right)\left(x - \frac{x^3}{6}\right) + o(x^3) \\
&= x + x^2 + \frac{x^3}{3} + o(x^3)
\end{aligned}
$$
:::

## V. Équivalents usuels en 0 {Supérieur}

| Fonction | Équivalent en $0$ |
|---|---|
| $\sin x$, $\tan x$, $\arctan x$, $\operatorname{sh} x$ | $x$ |
| $\ln(1 + x)$ | $x$ |
| $\mathrm{e}^x - 1$ | $x$ |
| $1 - \cos x$ | $\dfrac{x^2}{2}$ |
| $(1 + x)^\alpha - 1$ ($\alpha \neq 0$) | $\alpha x$ |

::: attention Règles des équivalents
On peut multiplier, diviser et élever à une puissance des équivalents, mais **pas les additionner** ni les composer par une fonction comme $\ln$ ou $\exp$. Pour une somme, on passe aux développements limités.
:::

::: exemple Calculer $\displaystyle\lim_{x \to 0} \frac{\sin x - x}{x^3}$
$\sin x - x = -\dfrac{x^3}{6} + o(x^3)$, donc la limite vaut $-\dfrac{1}{6}$.
:::
