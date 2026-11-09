---
{
  "slug": "factorisation",
  "titre": "Factorisation",
  "titreCourt": "Factorisation",
  "titreSeo": "Factorisation : méthodes et formules pour factoriser une expression",
  "description": "Comment factoriser une expression : facteur commun, identités remarquables, trinôme du second degré, racine évidente, regroupement, avec exemples corrigés.",
  "chapo": "Les méthodes pour factoriser, dans l’ordre où on les essaie : facteur commun, identités remarquables, trinôme du second degré et polynômes de degré 3, avec des exemples rédigés.",
  "resume": "Facteur commun, identités remarquables, trinôme",
  "vignette": "facteur_commun",
  "theme": "Algèbre",
  "niveaux": ["Collège", "Lycée"],
  "ordre": 5,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["factorisation", "factoriser une expression", "comment factoriser", "facteur commun", "factoriser avec une identité remarquable", "factoriser a²−b²", "factoriser un trinôme", "factorisation formule"],
  "figures": [
    { "nom": "facteur_commun", "alt": "Un rectangle de largeur k et de longueur a + b est partagé en deux rectangles d’aires ka et kb : ka + kb = k(a + b)." },
    { "nom": "difference_carres", "alt": "Un carré de côté a privé d’un carré de côté b : la partie restante, découpée et recollée, forme un rectangle de côtés a − b et a + b, donc a² − b² = (a − b)(a + b)." }
  ],
  "chapitresLies": [
    "4e/calcul-litteral-et-distributivite",
    "3e/calcul-litteral",
    "seconde/utiliser-le-calcul-litteral",
    "premiere/equations-fonctions-polynomes-du-second-degre"
  ],
  "faq": [
    ["Que veut dire factoriser ?", "Factoriser, c’est écrire une somme sous la forme d’un produit. Par exemple, 3x + 6 = 3(x + 2). C’est l’opération inverse du développement."],
    ["Comment factoriser une expression ?", "On cherche d’abord un facteur commun à tous les termes. S’il n’y en a pas, on cherche une identité remarquable : a² + 2ab + b², a² − 2ab + b² ou a² − b². Au lycée, un trinôme se factorise avec ses racines."],
    ["Comment factoriser x² − 9 ?", "C’est une différence de deux carrés : x² − 9 = x² − 3² = (x − 3)(x + 3)."],
    ["Comment factoriser x² + 9 ?", "x² + 9 ne se factorise pas avec des nombres réels : c’est une somme de deux carrés, et son discriminant est négatif."],
    ["À quoi sert la factorisation ?", "À résoudre des équations avec la règle du produit nul, à étudier le signe d’une expression dans un tableau de signes et à simplifier des fractions."]
  ]
}
---
<!-- optitab:1 -->
## I. Factoriser, c’est quoi ? {Collège}

::: definition Factoriser
Factoriser une expression, c’est la transformer en **produit**. C’est l’opération inverse du développement :
$$\underbrace{3x + 6}_{\text{somme}} = \underbrace{3(x + 2)}_{\text{produit}}$$
:::

::: methode Dans quel ordre essayer ?
1. Chercher un **facteur commun**.
2. Chercher une **identité remarquable**.
3. Au lycée, utiliser les **racines** d’un trinôme ou une **racine évidente**.
:::

## II. Facteur commun {Collège}

[IMAGE_1]

::: formule Facteur commun $k$
$$ka + kb = k(a + b) \qquad ka - kb = k(a - b)$$
:::

| Expression | Forme factorisée |
|---|---|
| $6x + 9$ | $3(2x + 3)$ |
| $x^2 + 5x$ | $x(x + 5)$ |
| $4x^2 - 10x$ | $2x(2x - 5)$ |
| $(x + 2)^2 - 3(x + 2)$ | $(x + 2)(x - 1)$ |

::: exemple Rédaction avec un facteur commun entre parenthèses
$$
\begin{aligned}
A &= (x + 1)(2x - 3) + (x + 1)(x + 4) \\
&= (x + 1)\big[(2x - 3) + (x + 4)\big] \\
&= (x + 1)(3x + 1)
\end{aligned}
$$
:::

::: attention Erreur fréquente
Quand un terme est égal au facteur commun lui-même, il reste $1$ : $(2x + 1)(x - 3) - (x - 3)$ s’écrit $(x - 3)\big[(2x + 1) - 1\big]$, soit $2x(x - 3)$.
:::

## III. Identités remarquables {Collège}

On lit les identités remarquables « de droite à gauche ».

| Forme développée | Forme factorisée |
|---|---|
| $a^2 + 2ab + b^2$ | $(a + b)^2$ |
| $a^2 - 2ab + b^2$ | $(a - b)^2$ |
| $a^2 - b^2$ | $(a - b)(a + b)$ |

[IMAGE_2]

| Expression | Forme factorisée |
|---|---|
| $x^2 + 6x + 9$ | $(x + 3)^2$ |
| $4x^2 - 12x + 9$ | $(2x - 3)^2$ |
| $x^2 - 25$ | $(x - 5)(x + 5)$ |
| $9x^2 - 4$ | $(3x - 2)(3x + 2)$ |
| $(x + 1)^2 - 16$ | $(x - 3)(x + 5)$ |

::: exemple Rédaction avec $a^2 - b^2$, où $a = x + 1$ et $b = 4$
$$
\begin{aligned}
(x + 1)^2 - 16 &= (x + 1)^2 - 4^2 \\
&= \big[(x + 1) - 4\big]\big[(x + 1) + 4\big] \\
&= (x - 3)(x + 5)
\end{aligned}
$$
:::

::: conseil Vérifier le double produit
Pour $4x^2 - 12x + 9$ : $a = 2x$ et $b = 3$, et le double produit vaut bien $2 \times 2x \times 3 = 12x$. Sans ce contrôle, on risque de factoriser à tort.
:::

::: attention Une somme de deux carrés ne se factorise pas
$x^2 + 9$ ne se factorise pas dans $\mathbb{R}$ : seule la **différence** $a^2 - b^2$ se factorise.
:::

## IV. Trinôme du second degré {Lycée}

Pour $ax^2 + bx + c$ avec $a \neq 0$, on calcule le discriminant :
$$\Delta = b^2 - 4ac$$

| Discriminant | Forme factorisée |
|---|---|
| $\Delta > 0$ | $a(x - x_1)(x - x_2)$, avec $x_{1,2} = \dfrac{-b \pm \sqrt{\Delta}}{2a}$ |
| $\Delta = 0$ | $a(x - x_0)^2$, avec $x_0 = -\dfrac{b}{2a}$ |
| $\Delta < 0$ | pas de factorisation dans $\mathbb{R}$ |

::: exemple Factoriser $2x^2 - 2x - 12$
$\Delta = (-2)^2 - 4 \times 2 \times (-12) = 4 + 96 = 100$, donc :
$$x_1 = \frac{2 - 10}{4} = -2 \qquad x_2 = \frac{2 + 10}{4} = 3$$
D’où $2x^2 - 2x - 12 = 2(x + 2)(x - 3)$.
:::

::: conseil Racine évidente
Si $1$ est racine, l’autre racine vaut $\dfrac{c}{a}$ (produit des racines). Pour $x^2 - 5x + 4$ : $1 - 5 + 4 = 0$, donc $x^2 - 5x + 4 = (x - 1)(x - 4)$.
:::

## V. Degré 3 et regroupement {Lycée}

::: propriete Racine évidente
Si $P(\alpha) = 0$, alors on peut écrire $P(x) = (x - \alpha)\,Q(x)$, où $Q$ est un polynôme de degré un de moins.
:::

| Formule | Forme factorisée |
|---|---|
| $a^3 - b^3$ | $(a - b)(a^2 + ab + b^2)$ |
| $a^3 + b^3$ | $(a + b)(a^2 - ab + b^2)$ |

::: exemple Factoriser $x^3 - 2x^2 - x + 2$ par regroupement
$$
\begin{aligned}
x^3 - 2x^2 - x + 2 &= x^2(x - 2) - (x - 2) \\
&= (x - 2)(x^2 - 1) \\
&= (x - 2)(x - 1)(x + 1)
\end{aligned}
$$
:::

## VI. À quoi sert la forme factorisée ? {Collège}

| Objectif | Outil |
|---|---|
| Résoudre $A = 0$ | règle du produit nul : $A \times B = 0 \iff A = 0$ ou $B = 0$ |
| Étudier le signe | tableau de signes des facteurs |
| Simplifier une fraction | $\dfrac{x(x + 5)}{x} = x + 5$ pour $x \neq 0$ |

::: exemple Résoudre $x^2 - 9 = 0$
$x^2 - 9 = (x - 3)(x + 3)$, donc $x^2 - 9 = 0$ équivaut à $x - 3 = 0$ ou $x + 3 = 0$ : les solutions sont $3$ et $-3$.
:::
