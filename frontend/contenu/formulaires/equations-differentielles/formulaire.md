---
{
  "slug": "equations-differentielles",
  "titre": "Équations différentielles",
  "titreCourt": "Équations différentielles",
  "titreSeo": "Équations différentielles : formules et méthodes de résolution",
  "description": "Résoudre une équation différentielle : y′ = ay, y′ = ay + b, second membre, variation de la constante, équations du second ordre à coefficients constants.",
  "chapo": "Les solutions des équations différentielles à connaître, de y′ = ay + b en Terminale aux équations du second ordre du supérieur, avec les méthodes et des exemples de modélisation.",
  "resume": "y′ = ay + b, second membre, équations d’ordre 2",
  "vignette": "famille_solutions",
  "theme": "Analyse",
  "niveaux": ["Lycée", "Supérieur"],
  "ordre": 18,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["équations différentielles", "équation différentielle y'=ay+b", "résoudre une équation différentielle", "solution particulière", "variation de la constante", "équation caractéristique", "équation différentielle du second ordre", "équation différentielle terminale"],
  "figures": [
    { "nom": "famille_solutions", "alt": "Courbes des solutions de l’équation y′ = −y + 2 : toutes se rapprochent de la droite y = 2, solution constante ; la solution telle que y(0) = 4,2 est mise en évidence." },
    { "nom": "oscillations_amorties", "alt": "Solution d’une équation différentielle du second ordre dont l’équation caractéristique a des racines complexes : une oscillation amortie, comprise entre les courbes ± e^(−0,3t)." }
  ],
  "chapitresLies": [
    "terminale/equations-differentielles",
    "terminale/primitives",
    "terminale/fonction-exponentielle"
  ],
  "faq": [
    ["Quelle est la solution de y′ = ay ?", "Les solutions de y′ = ay sont les fonctions x ↦ C e^(ax), où C est une constante réelle. Avec une condition initiale y(0) = y₀, la solution est unique : y(x) = y₀ e^(ax)."],
    ["Comment résoudre y′ = ay + b ?", "Pour a ≠ 0, on cherche d’abord la solution constante y = −b/a, puis on ajoute les solutions de y′ = ay. Les solutions sont donc y(x) = C e^(ax) − b/a, et une condition initiale fixe la valeur de C."],
    ["Qu’est-ce qu’une solution particulière ?", "C’est une solution précise de l’équation complète, souvent cherchée de la même forme que le second membre (constante, polynôme, exponentielle). Toutes les solutions s’obtiennent en lui ajoutant les solutions de l’équation sans second membre."],
    ["Comment résoudre une équation différentielle du second ordre ?", "Pour ay″ + by′ + cy = 0, on résout l’équation caractéristique ar² + br + c = 0. Selon le signe de son discriminant, les solutions s’écrivent avec deux exponentielles, avec (λx + μ)e^(rx), ou avec un cosinus et un sinus."]
  ]
}
---
<!-- optitab:1 -->
## I. Vocabulaire {Lycée}

::: definition
Une **équation différentielle** relie une fonction inconnue $y$ et ses dérivées. Une **solution** sur un intervalle $I$ est une fonction dérivable qui vérifie l’équation en tout point de $I$. Une **condition initiale** $y(x_0) = y_0$ permet de choisir une solution unique.
:::

Dans toute la page, $C$, $\lambda$ et $\mu$ désignent des constantes réelles.

## II. Équation $y' = ay$ {Lycée}

| Équation | Solutions |
|---|---|
| $y' = ay$ | $y(x) = C\,\mathrm{e}^{ax}$ |
| $y' = ay$ et $y(0) = y_0$ | $y(x) = y_0\,\mathrm{e}^{ax}$ |
| $y' = ay$ et $y(x_0) = y_0$ | $y(x) = y_0\,\mathrm{e}^{a(x - x_0)}$ |

## III. Équation $y' = ay + b$ {Lycée}

[IMAGE_1]

| Étape | Résultat (avec $a \neq 0$) |
|---|---|
| Solution constante | $y = -\dfrac{b}{a}$ |
| Toutes les solutions | $y(x) = C\,\mathrm{e}^{ax} - \dfrac{b}{a}$ |
| Condition initiale | elle fixe la valeur de $C$ |

Si $a < 0$, toutes les solutions tendent vers la solution constante $-\dfrac{b}{a}$ quand $x \to +\infty$ (droite $y = 2$ sur la figure).

::: exemple $y' = 2y - 6$ et $y(0) = 5$
La solution constante est $y = \dfrac{6}{2} = 3$, donc $y(x) = C\,\mathrm{e}^{2x} + 3$. Avec $y(0) = C + 3 = 5$, on trouve $C = 2$ :
$$y(x) = 2\,\mathrm{e}^{2x} + 3$$
:::

## IV. Équation avec second membre $y' = ay + f$ {Lycée}

::: theoreme Structure des solutions
Si $y_p$ est une solution particulière de $y' = ay + f$, les solutions sont :
$$y(x) = y_p(x) + C\,\mathrm{e}^{ax}$$
:::

::: methode Chercher une solution particulière
On la cherche de la même forme que $f$ : une constante si $f$ est constante, un polynôme de même degré si $f$ est un polynôme, $A\,\mathrm{e}^{mx}$ si $f(x) = \mathrm{e}^{mx}$ (avec $m \neq a$).
:::

::: exemple $y' = y + x$
On cherche $y_p(x) = \alpha x + \beta$ : $\alpha = \alpha x + \beta + x$ pour tout $x$, donc $\alpha = -1$ et $\beta = -1$. Les solutions sont :
$$y(x) = C\,\mathrm{e}^{x} - x - 1$$
:::

## V. Ordre 1 à coefficients variables {Supérieur}

On résout $y' + a(x)\,y = b(x)$, avec $a$ et $b$ continues et $A$ une primitive de $a$.

| Étape | Résultat |
|---|---|
| Équation homogène $y' + a(x)\,y = 0$ | $y(x) = C\,\mathrm{e}^{-A(x)}$ |
| Variation de la constante | on pose $y(x) = C(x)\,\mathrm{e}^{-A(x)}$ |
| Condition sur $C$ | $C'(x) = b(x)\,\mathrm{e}^{A(x)}$ |

## VI. Ordre 2 à coefficients constants {Supérieur}

Pour $ay'' + by' + cy = 0$ (avec $a \neq 0$), on résout l’**équation caractéristique** $ar^2 + br + c = 0$, de discriminant $\Delta = b^2 - 4ac$.

| Discriminant | Solutions réelles |
|---|---|
| $\Delta > 0$, racines $r_1$ et $r_2$ | $y(x) = \lambda\,\mathrm{e}^{r_1 x} + \mu\,\mathrm{e}^{r_2 x}$ |
| $\Delta = 0$, racine double $r$ | $y(x) = (\lambda x + \mu)\,\mathrm{e}^{rx}$ |
| $\Delta < 0$, racines $\alpha \pm \mathrm{i}\beta$ | $y(x) = \mathrm{e}^{\alpha x}\big(\lambda \cos(\beta x) + \mu \sin(\beta x)\big)$ |

[IMAGE_2]

::: retenir Deux cas à connaître par cœur ($\omega > 0$)
- $y'' + \omega^2 y = 0$ : $y(x) = \lambda \cos(\omega x) + \mu \sin(\omega x)$ (oscillateur harmonique)
- $y'' - \omega^2 y = 0$ : $y(x) = \lambda\,\mathrm{e}^{\omega x} + \mu\,\mathrm{e}^{-\omega x}$
:::

::: methode Avec un second membre $A\,\mathrm{e}^{mx}$
Les solutions sont $y_p + {}$solutions de l’équation homogène. On cherche $y_p$ sous la forme :
- $B\,\mathrm{e}^{mx}$ si $m$ n’est pas racine de l’équation caractéristique ;
- $Bx\,\mathrm{e}^{mx}$ si $m$ est racine simple ;
- $Bx^2\,\mathrm{e}^{mx}$ si $m$ est racine double.

Deux conditions initiales, $y(x_0)$ et $y'(x_0)$, fixent $\lambda$ et $\mu$.
:::

## VII. Exemples de modélisation {Lycée}

| Situation | Équation et solution |
|---|---|
| Décroissance radioactive | $N' = -\lambda N$, donc $N(t) = N_0\,\mathrm{e}^{-\lambda t}$ |
| Demi-vie | $t_{1/2} = \dfrac{\ln 2}{\lambda}$ |
| Refroidissement (loi de Newton) | $T' = -k(T - T_a)$, donc $T(t) = T_a + (T_0 - T_a)\,\mathrm{e}^{-kt}$ |
| Charge d’un condensateur | $RC\,u' + u = E$ et $u(0) = 0$, donc $u(t) = E\left(1 - \mathrm{e}^{-t/(RC)}\right)$ |
