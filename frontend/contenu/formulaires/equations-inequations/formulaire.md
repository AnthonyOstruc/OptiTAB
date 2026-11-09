---
{
  "slug": "equations-inequations",
  "titre": "Équations et inéquations",
  "titreCourt": "Équations et inéquations",
  "titreSeo": "Résoudre une équation ou une inéquation : règles et méthodes",
  "description": "Les règles pour résoudre équations et inéquations : premier degré, produit nul, quotient, x² = a, intervalles, exponentielle, logarithme, systèmes.",
  "chapo": "Les règles de calcul, puis chaque type d’équation et d’inéquation avec sa méthode : premier degré, produit nul, quotient nul, carrés, valeur absolue, exponentielle et logarithme, systèmes.",
  "resume": "Premier degré, produit nul, intervalles, systèmes",
  "vignette": "intervalles",
  "theme": "Algèbre",
  "niveaux": ["Collège", "Lycée"],
  "ordre": 5,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["résoudre une équation", "résoudre une inéquation", "équation produit nul", "équation du premier degré", "inéquation changement de sens", "équation quotient", "système d'équations", "intervalles solution"],
  "figures": [
    { "nom": "intervalles", "alt": "Deux droites graduées : les solutions de x < 3 forment l’intervalle ]−∞ ; 3[, crochet ouvert en 3 ; celles de −2 ≤ x ≤ 1 forment l’intervalle [−2 ; 1], crochets fermés." }
  ],
  "chapitresLies": [
    "5e/inconnues-et-equations-simples",
    "4e/equations-et-resolution-de-problemes",
    "3e/equations",
    "seconde/utiliser-le-calcul-litteral",
    "premiere/equations-fonctions-polynomes-du-second-degre"
  ],
  "faq": [
    ["Comment résoudre une équation du premier degré ?", "On regroupe les termes en x d’un côté et les nombres de l’autre, en faisant la même opération des deux côtés, puis on divise par le coefficient de x. Par exemple, 3x − 7 = 2x + 5 donne x = 12."],
    ["Quand change-t-on le sens d’une inéquation ?", "Quand on multiplie ou qu’on divise les deux membres par un nombre strictement négatif. Par exemple, −2x > −6 donne x < 3."],
    ["Qu’est-ce que la règle du produit nul ?", "Un produit est nul si et seulement si l’un au moins de ses facteurs est nul : A × B = 0 équivaut à A = 0 ou B = 0."],
    ["Comment résoudre x² = 16 ?", "x² = 16 a deux solutions : x = 4 et x = −4. En général, x² = a a deux solutions √a et −√a si a > 0, une seule (0) si a = 0, et aucune si a < 0."],
    ["Comment résoudre un système de deux équations ?", "Par substitution (on exprime une inconnue en fonction de l’autre et on remplace) ou par combinaison (on additionne ou soustrait les équations pour éliminer une inconnue)."]
  ]
}
---
<!-- optitab:1 -->
## I. Les règles de calcul {Collège}

::: retenir Équations
On obtient une équation équivalente en ajoutant ou en soustrayant un même nombre aux deux membres, ou en les multipliant ou divisant par un même nombre **non nul**.
:::

| Sur une inéquation, on… | Le sens |
|---|---|
| ajoute ou soustrait un même nombre | ne change pas |
| multiplie ou divise par un nombre strictement positif | ne change pas |
| multiplie ou divise par un nombre strictement négatif | **change** |

::: attention Erreur fréquente
$-2x > -6$ donne $x < 3$ : en divisant par $-2$, le symbole $>$ devient $<$.
:::

## II. Équations du premier degré {Collège}

::: formule Équation $ax + b = 0$ avec $a \neq 0$
$$x = -\frac{b}{a}$$
:::

::: exemple Résoudre $3x - 7 = 2x + 5$
$$
\begin{aligned}
3x - 2x &= 5 + 7 \\
x &= 12
\end{aligned}
$$
Vérification : $3 \times 12 - 7 = 29$ et $2 \times 12 + 5 = 29$.
:::

## III. Produit nul et quotient nul {Collège}

::: propriete Règle du produit nul
$$A \times B = 0 \iff A = 0 \text{ ou } B = 0$$
:::

::: exemple Résoudre $(2x - 3)(x + 5) = 0$
$2x - 3 = 0$ ou $x + 5 = 0$, donc $x = \dfrac{3}{2}$ ou $x = -5$.
:::

::: propriete Quotient nul
$$\frac{A}{B} = 0 \iff A = 0 \text{ et } B \neq 0$$
:::

::: exemple Résoudre $\dfrac{x - 2}{x + 1} = 0$
On a $x - 2 = 0$ et $x \neq -1$ : la seule solution est $x = 2$.
:::

## IV. Équations $x^2 = a$ {Collège}

| Cas | Solutions |
|---|---|
| $a > 0$ | $x = \sqrt{a}$ ou $x = -\sqrt{a}$ |
| $a = 0$ | $x = 0$ |
| $a < 0$ | aucune solution réelle |

::: exemple
$x^2 = 16$ a deux solutions, $4$ et $-4$. $x^2 = -9$ n’a pas de solution réelle, car un carré est toujours positif.
:::

## V. Inéquations et intervalles {Collège}

[IMAGE_1]

| Inéquation | Intervalle |
|---|---|
| $x > a$ | $]a\,;+\infty[$ |
| $x \geqslant a$ | $[a\,;+\infty[$ |
| $x < a$ | $]{-\infty}\,;a[$ |
| $x \leqslant a$ | $]{-\infty}\,;a]$ |
| $a \leqslant x \leqslant b$ | $[a\,;b]$ |
| $a < x \leqslant b$ | $]a\,;b]$ |

Le crochet est **tourné vers l’extérieur** quand la borne est exclue. Du côté de l’infini, il est toujours ouvert.

::: exemple Résoudre $-2x + 6 > 0$
$-2x > -6$, donc $x < 3$ (on divise par $-2$ et on change le sens). L’ensemble des solutions est $]{-\infty}\,;3[$.
:::

::: methode Inéquation produit ou quotient
On étudie le signe de chaque facteur, puis on regroupe tout dans un **tableau de signes**. Par exemple, $(x - 1)(x + 2) \leqslant 0$ a pour ensemble de solutions $[-2\,;1]$.
:::

## VI. Valeur absolue {Lycée}

$\lvert x - a \rvert$ est la distance entre $x$ et $a$ sur la droite graduée ($r > 0$).

| Équation ou inéquation | Solutions |
|---|---|
| $\lvert x - a \rvert = r$ | $x = a - r$ ou $x = a + r$ |
| $\lvert x - a \rvert \leqslant r$ | $[a - r\,;a + r]$ |
| $\lvert x - a \rvert > r$ | $]{-\infty}\,;a - r[\,\cup\,]a + r\,;+\infty[$ |

## VII. Second degré {Lycée}

Pour $ax^2 + bx + c = 0$ ($a \neq 0$), on calcule $\Delta = b^2 - 4ac$.

| Discriminant | Solutions |
|---|---|
| $\Delta > 0$ | $x_1 = \dfrac{-b - \sqrt{\Delta}}{2a}$ et $x_2 = \dfrac{-b + \sqrt{\Delta}}{2a}$ |
| $\Delta = 0$ | $x_0 = -\dfrac{b}{2a}$ |
| $\Delta < 0$ | aucune solution réelle |

Le trinôme est du signe de $a$, sauf entre ses racines.

## VIII. Exponentielle et logarithme {Lycée}

| Équation ou inéquation | Équivaut à |
|---|---|
| $\mathrm{e}^{A} = \mathrm{e}^{B}$ | $A = B$ |
| $\mathrm{e}^{A} < \mathrm{e}^{B}$ | $A < B$ |
| $\mathrm{e}^{x} = k$ ($k > 0$) | $x = \ln k$ |
| $\ln A = \ln B$ ($A, B > 0$) | $A = B$ |
| $\ln A < \ln B$ ($A, B > 0$) | $A < B$ |
| $\ln x = k$ | $x = \mathrm{e}^{k}$ |

::: attention Domaine de définition
Avec un logarithme, on cherche d’abord où l’expression est définie. Pour $\ln(x - 1) = 2$, il faut $x > 1$, puis $x - 1 = \mathrm{e}^2$, donc $x = 1 + \mathrm{e}^2$.
:::

## IX. Systèmes de deux équations {Collège}

::: exemple Par combinaison : $x + y = 10$ et $x - y = 4$
En additionnant les deux équations, $2x = 14$, donc $x = 7$. Puis $y = 10 - 7 = 3$.
:::

::: exemple Par substitution : $y = 2x - 1$ et $3x + y = 9$
On remplace $y$ : $3x + 2x - 1 = 9$, donc $5x = 10$ et $x = 2$. Puis $y = 2 \times 2 - 1 = 3$.
:::

::: propriete Nombre de solutions de $ax + by = c$, $a'x + b'y = c'$
Si $ab' - a'b \neq 0$, le système a une **unique** solution. Sinon, il n’en a aucune ou une infinité : les deux droites sont parallèles ou confondues.
:::
