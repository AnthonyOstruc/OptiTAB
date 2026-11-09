---
{
  "slug": "courbes-fonctions-usuelles",
  "titre": "Courbes des fonctions usuelles",
  "titreCourt": "Courbes des fonctions usuelles",
  "titreSeo": "Courbes des fonctions usuelles : arcsin, arctan, tan, ch, sh",
  "description": "Les courbes des fonctions usuelles et leurs propriétés : carré, inverse, racine, exp, ln, sin, cos, tan, arcsin, arccos, arctan, ch, sh, th, puissances.",
  "chapo": "La courbe de chaque fonction usuelle, avec son ensemble de définition, ses valeurs, sa dérivée, ses asymptotes et les pièges classiques à connaître.",
  "resume": "tan, arcsin, arccos, arctan, ch, sh, th et les autres",
  "vignette": "arcsin_arccos",
  "theme": "Analyse",
  "niveaux": ["Lycée", "Supérieur"],
  "ordre": 12,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["courbes des fonctions usuelles", "fonctions de référence", "courbe arcsin", "courbe arccos", "courbe arctan", "courbe tangente", "fonctions hyperboliques", "fonction partie entière", "ensemble de définition"],
  "figures": [
    { "nom": "carre_cube", "alt": "Courbes de la fonction carré, une parabole symétrique par rapport à l’axe des ordonnées, et de la fonction cube, symétrique par rapport à l’origine." },
    { "nom": "inverse_racine", "alt": "Courbe de la fonction inverse, une hyperbole en deux branches avec les axes comme asymptotes, et courbe de la fonction racine carrée, partant de l’origine." },
    { "nom": "abs_entiere", "alt": "Courbe de la valeur absolue en forme de V, et courbe en escalier de la partie entière, avec un point plein à gauche et un point vide à droite de chaque marche." },
    { "nom": "exp_ln", "alt": "Courbe de l’exponentielle, passant par (0 ; 1), et courbe du logarithme népérien, passant par (1 ; 0) et (e ; 1)." },
    { "nom": "sin_cos", "alt": "Courbes des fonctions sinus et cosinus entre -2π et 2π, comprises entre -1 et 1, de période 2π." },
    { "nom": "tangente", "alt": "Courbe de la fonction tangente : des branches croissantes de période π, séparées par des asymptotes verticales en -3π/2, -π/2, π/2 et 3π/2." },
    { "nom": "arcsin_arccos", "alt": "Courbe de l’arcsinus, de (-1 ; -π/2) à (1 ; π/2), et courbe de l’arccosinus, de (-1 ; π) à (1 ; 0) en passant par (0 ; π/2)." },
    { "nom": "arctan", "alt": "Courbe de l’arctangente, croissante, passant par l’origine, avec deux asymptotes horizontales y = π/2 et y = -π/2." },
    { "nom": "hyperboliques", "alt": "Courbes du cosinus hyperbolique, minimum 1 en 0, du sinus hyperbolique, passant par l’origine, et de la tangente hyperbolique, comprise entre les asymptotes y = -1 et y = 1." },
    { "nom": "puissances", "alt": "Courbes des fonctions puissances x^α sur ]0 ; +∞[ pour α = 2, 1, 1/2 et -1 : toutes passent par le point (1 ; 1)." }
  ],
  "chapitresLies": [
    "seconde/se-constituer-un-repertoire-de-fonctions-de-reference",
    "premiere/fonction-exponentielle",
    "premiere/fonctions-trigonometriques",
    "terminale/fonction-logarithme-neperien",
    "terminale/fonctions-sinus-et-cosinus"
  ],
  "faq": [
    ["Quel est l’ensemble de définition d’arcsin et d’arccos ?", "Les fonctions arcsinus et arccosinus sont définies sur [−1 ; 1]. Arcsin prend ses valeurs dans [−π/2 ; π/2] et arccos dans [0 ; π]. Elles ne sont pas dérivables en −1 et en 1, où leur courbe a une tangente verticale."],
    ["Pourquoi arcsin(sin x) n’est-il pas toujours égal à x ?", "Parce qu’arcsin renvoie toujours un angle de [−π/2 ; π/2]. L’égalité arcsin(sin x) = x n’est vraie que pour x dans cet intervalle. Par exemple, arcsin(sin π) = arcsin 0 = 0, et non π."],
    ["Quelles sont les asymptotes de la fonction arctangente ?", "La courbe de l’arctangente a deux asymptotes horizontales : la droite y = π/2 en +∞ et la droite y = −π/2 en −∞. Elle est croissante sur ℝ et passe par l’origine."],
    ["Comment obtenir la courbe de f(x − a) ?", "On décale la courbe de f horizontalement de a : vers la droite si a > 0, vers la gauche si a < 0. C’est un piège classique : le signe moins correspond à un décalage vers la droite."]
  ]
}
---
<!-- optitab:1 -->
## I. Carré et cube {Lycée}

[IMAGE_1]

| Propriété | $x^2$ | $x^3$ |
|---|---|---|
| Définie sur | $\mathbb{R}$ | $\mathbb{R}$ |
| Valeurs prises | $[0\,;+\infty[$ | $\mathbb{R}$ |
| Parité | paire | impaire |
| Dérivée | $2x$ | $3x^2$ |
| Variations | décroissante sur $]{-\infty}\,;0]$, croissante sur $[0\,;+\infty[$ | croissante sur $\mathbb{R}$ |

La courbe de $x \mapsto x^2$ est une **parabole**, symétrique par rapport à l’axe des ordonnées ; celle de $x \mapsto x^3$ est symétrique par rapport à l’origine.

## II. Inverse et racine carrée {Lycée}

[IMAGE_2]

| Propriété | $\dfrac{1}{x}$ | $\sqrt{x}$ |
|---|---|---|
| Définie sur | $\mathbb{R}^*$ | $[0\,;+\infty[$ |
| Valeurs prises | $\mathbb{R}^*$ | $[0\,;+\infty[$ |
| Parité | impaire | ni paire ni impaire |
| Dérivée | $-\dfrac{1}{x^2}$ | $\dfrac{1}{2\sqrt{x}}$ pour $x > 0$ |
| Variations | décroissante sur $]{-\infty}\,;0[$ et sur $]0\,;+\infty[$ | croissante |
| Asymptotes | les deux axes | aucune |

::: attention Deux pièges
- La fonction inverse est décroissante sur **chacun** des intervalles $]{-\infty}\,;0[$ et $]0\,;+\infty[$, mais pas sur $\mathbb{R}^*$ : $-1 < 1$ et pourtant $\dfrac{1}{-1} < \dfrac{1}{1}$.
- La racine carrée n’est pas dérivable en $0$ : sa courbe y a une tangente verticale.
:::

::: retenir Positions relatives
Sur $[0\,;1]$ : $x^2 \leqslant x \leqslant \sqrt{x}$. Sur $[1\,;+\infty[$ : $\sqrt{x} \leqslant x \leqslant x^2$.
:::

## III. Valeur absolue et partie entière {Lycée}

[IMAGE_3]

| Propriété | $\lvert x \rvert$ | $\lfloor x \rfloor$ |
|---|---|---|
| Définition | $x$ si $x \geqslant 0$, $-x$ sinon | l’entier $n$ tel que $n \leqslant x < n + 1$ |
| Définie sur | $\mathbb{R}$ | $\mathbb{R}$ |
| Valeurs prises | $[0\,;+\infty[$ | $\mathbb{Z}$ |
| Continuité | continue sur $\mathbb{R}$ | discontinue en chaque entier |
| Dérivabilité | pas dérivable en $0$ | dérivée nulle hors des entiers |

::: attention Partie entière d’un nombre négatif
$\lfloor 2{,}7 \rfloor = 2$, mais $\lfloor -2{,}7 \rfloor = -3$ (et non $-2$). Pour tout réel $x$ : $x - 1 < \lfloor x \rfloor \leqslant x$.
:::

## IV. Exponentielle et logarithme {Lycée}

[IMAGE_4]

| Propriété | $\mathrm{e}^x$ | $\ln x$ |
|---|---|---|
| Définie sur | $\mathbb{R}$ | $]0\,;+\infty[$ |
| Valeurs prises | $]0\,;+\infty[$ | $\mathbb{R}$ |
| Dérivée | $\mathrm{e}^x$ | $\dfrac{1}{x}$ |
| Valeurs clés | $\mathrm{e}^0 = 1$ et $\mathrm{e}^1 = \mathrm{e}$ | $\ln 1 = 0$ et $\ln \mathrm{e} = 1$ |
| Limites | $0$ en $-\infty$, $+\infty$ en $+\infty$ | $-\infty$ en $0^+$, $+\infty$ en $+\infty$ |
| Asymptote | $y = 0$ en $-\infty$ | l’axe des ordonnées |
| Convexité | convexe | concave |

::: retenir Inégalités de convexité
$\mathrm{e}^x \geqslant 1 + x$ pour tout réel $x$, et $\ln x \leqslant x - 1$ pour tout $x > 0$ : la courbe est au-dessus (exponentielle) ou en dessous (logarithme) de sa tangente.
:::

## V. Sinus et cosinus {Lycée}

[IMAGE_5]

| Propriété | $\sin$ | $\cos$ |
|---|---|---|
| Définie sur | $\mathbb{R}$ | $\mathbb{R}$ |
| Valeurs prises | $[-1\,;1]$ | $[-1\,;1]$ |
| Période | $2\pi$ | $2\pi$ |
| Parité | impaire | paire |
| Dérivée | $\cos$ | $-\sin$ |
| S’annule en | $k\pi$ | $\dfrac{\pi}{2} + k\pi$ |

Comme $\cos x = \sin\left(x + \dfrac{\pi}{2}\right)$, la courbe du cosinus est celle du sinus décalée de $\dfrac{\pi}{2}$ vers la gauche. Pour tout réel $x$ : $\lvert \sin x \rvert \leqslant \lvert x \rvert$.

## VI. Tangente {Lycée}

[IMAGE_6]

| Propriété | $\tan$ |
|---|---|
| Définie pour | $x \neq \dfrac{\pi}{2} + k\pi$ |
| Valeurs prises | $\mathbb{R}$ |
| Période | $\pi$ |
| Parité | impaire |
| Dérivée | $1 + \tan^2 x = \dfrac{1}{\cos^2 x}$ |
| Asymptotes | les droites verticales $x = \dfrac{\pi}{2} + k\pi$ |
| Valeurs clés | $\tan 0 = 0$ et $\tan\dfrac{\pi}{4} = 1$ |

::: attention
La tangente est croissante sur **chaque** intervalle $\left]-\dfrac{\pi}{2} + k\pi\,;\dfrac{\pi}{2} + k\pi\right[$, mais pas sur son ensemble de définition : sa période est $\pi$, et non $2\pi$.
:::

## VII. Arcsinus et arccosinus {Supérieur}

[IMAGE_7]

| Propriété | $\arcsin$ | $\arccos$ |
|---|---|---|
| Définie sur | $[-1\,;1]$ | $[-1\,;1]$ |
| Valeurs prises | $\left[-\dfrac{\pi}{2}\,;\dfrac{\pi}{2}\right]$ | $[0\,;\pi]$ |
| Parité | impaire | ni paire ni impaire |
| Dérivée sur $]-1\,;1[$ | $\dfrac{1}{\sqrt{1 - x^2}}$ | $-\dfrac{1}{\sqrt{1 - x^2}}$ |
| Valeurs clés | $\arcsin 0 = 0$, $\arcsin 1 = \dfrac{\pi}{2}$ | $\arccos 0 = \dfrac{\pi}{2}$, $\arccos 1 = 0$ |

::: attention Les pièges
- $\sin(\arcsin x) = x$ pour tout $x \in [-1\,;1]$, mais $\arcsin(\sin x) = x$ **seulement** si $x \in \left[-\dfrac{\pi}{2}\,;\dfrac{\pi}{2}\right]$ : par exemple $\arcsin(\sin \pi) = 0$.
- De même, $\arccos(\cos x) = x$ seulement si $x \in [0\,;\pi]$.
- Arcsin et arccos ne sont pas dérivables en $-1$ et en $1$ : tangentes verticales.
:::

::: retenir Relations utiles
- $\arcsin x + \arccos x = \dfrac{\pi}{2}$ pour tout $x \in [-1\,;1]$
- $\arccos(-x) = \pi - \arccos x$
- $\cos(\arcsin x) = \sin(\arccos x) = \sqrt{1 - x^2}$
:::

## VIII. Arctangente {Supérieur}

[IMAGE_8]

| Propriété | $\arctan$ |
|---|---|
| Définie sur | $\mathbb{R}$ |
| Valeurs prises | $\left]-\dfrac{\pi}{2}\,;\dfrac{\pi}{2}\right[$ |
| Parité | impaire |
| Dérivée | $\dfrac{1}{1 + x^2}$ |
| Asymptotes | $y = \dfrac{\pi}{2}$ en $+\infty$ et $y = -\dfrac{\pi}{2}$ en $-\infty$ |
| Valeurs clés | $\arctan 0 = 0$ et $\arctan 1 = \dfrac{\pi}{4}$ |

::: retenir Relations utiles
- $\tan(\arctan x) = x$ pour tout réel $x$, mais $\arctan(\tan x) = x$ seulement si $x \in \left]-\dfrac{\pi}{2}\,;\dfrac{\pi}{2}\right[$.
- $\arctan x + \arctan\dfrac{1}{x} = \dfrac{\pi}{2}$ si $x > 0$, et $-\dfrac{\pi}{2}$ si $x < 0$.
:::

## IX. Fonctions hyperboliques {Supérieur}

[IMAGE_9]

$\operatorname{ch} x = \dfrac{\mathrm{e}^x + \mathrm{e}^{-x}}{2}$, $\operatorname{sh} x = \dfrac{\mathrm{e}^x - \mathrm{e}^{-x}}{2}$ et $\operatorname{th} x = \dfrac{\operatorname{sh} x}{\operatorname{ch} x}$.

| Propriété | $\operatorname{ch}$ | $\operatorname{sh}$ | $\operatorname{th}$ |
|---|---|---|---|
| Valeurs prises | $[1\,;+\infty[$ | $\mathbb{R}$ | $]-1\,;1[$ |
| Parité | paire | impaire | impaire |
| Dérivée | $\operatorname{sh}$ | $\operatorname{ch}$ | $1 - \operatorname{th}^2$ |
| Valeur en $0$ | $1$ | $0$ | $0$ |

::: retenir
$\operatorname{ch}^2 x - \operatorname{sh}^2 x = 1$ et $\operatorname{ch} x + \operatorname{sh} x = \mathrm{e}^x$. Les trois fonctions sont définies sur $\mathbb{R}$ ; la courbe de $\operatorname{th}$ a pour asymptotes les droites $y = 1$ et $y = -1$.
:::

## X. Fonctions puissances {Supérieur}

[IMAGE_10]

Pour $x > 0$ et $\alpha$ réel : $x^\alpha = \mathrm{e}^{\alpha \ln x}$, de dérivée $\alpha\,x^{\alpha - 1}$. Toutes les courbes passent par le point $(1\,;1)$.

| Exposant | Allure sur $]0\,;+\infty[$ |
|---|---|
| $\alpha > 1$ | croissante, convexe, tangente horizontale en $0$ |
| $\alpha = 1$ | la droite $y = x$ |
| $0 < \alpha < 1$ | croissante, concave, tangente verticale en $0$ |
| $\alpha < 0$ | décroissante, les deux axes sont asymptotes |

## XI. Transformations de courbes {Lycée}

| Courbe de | Obtenue à partir de celle de $f$ par |
|---|---|
| $y = f(x) + k$ | une translation verticale de $k$ |
| $y = f(x - a)$ | une translation horizontale de $a$ |
| $y = -f(x)$ | la symétrie par rapport à l’axe des abscisses |
| $y = f(-x)$ | la symétrie par rapport à l’axe des ordonnées |
| $y = \lvert f(x) \rvert$ | le retournement vers le haut des parties sous l’axe des abscisses |
| $y = f^{-1}(x)$ | la symétrie par rapport à la droite $y = x$ |

::: attention Le décalage horizontal
La courbe de $y = f(x - 2)$ est celle de $f$ décalée de $2$ **vers la droite** (et non vers la gauche).
:::
