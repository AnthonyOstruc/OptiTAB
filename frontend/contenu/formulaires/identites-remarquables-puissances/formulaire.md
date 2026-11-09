---
{
  "slug": "identites-remarquables-puissances",
  "titre": "Identités remarquables, puissances et racines",
  "titreCourt": "Identités remarquables et puissances",
  "titreSeo": "Identités remarquables, puissances, racines carrées : formulaire",
  "description": "Les formules de calcul à connaître : identités remarquables, développement, factorisation, fractions, règles des puissances, racines carrées, valeur absolue.",
  "chapo": "Toutes les règles de calcul à connaître pour développer, factoriser et simplifier, du collège au supérieur, avec des exemples.",
  "resume": "(a + b)², fractions, puissances, racines carrées",
  "vignette": "carre_identite",
  "theme": "Calcul",
  "niveaux": ["Collège", "Lycée", "Supérieur"],
  "ordre": 3,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["identités remarquables", "formules identités remarquables", "règles des puissances", "propriétés des puissances", "racine carrée propriétés", "développer factoriser", "calcul fractions", "binôme de Newton"],
  "figures": [
    { "nom": "carre_identite", "alt": "Carré de côté a + b découpé en un carré a², deux rectangles ab et un carré b² : son aire vaut a² + 2ab + b²." }
  ],
  "chapitresLies": [
    "4e/calcul-litteral-et-distributivite",
    "4e/puissances-et-notation-scientifique",
    "4e/carres-et-racines-carrees",
    "3e/calcul-litteral",
    "3e/puissances-racines-et-ecriture-scientifique",
    "seconde/utiliser-le-calcul-litteral"
  ],
  "faq": [
    ["Quelles sont les trois identités remarquables ?", "(a + b)² = a² + 2ab + b², (a − b)² = a² − 2ab + b² et (a + b)(a − b) = a² − b². Elles servent à développer rapidement et, lues de droite à gauche, à factoriser."],
    ["Comment factoriser a² − b² ?", "C’est la troisième identité remarquable lue à l’envers : a² − b² = (a + b)(a − b). Par exemple, x² − 9 = x² − 3² = (x + 3)(x − 3)."],
    ["Pourquoi a⁰ = 1 ?", "Pour a non nul, a⁰ = aⁿ ÷ aⁿ = 1 : diviser un nombre par lui-même donne 1. Cette convention garde la règle aᵐ ÷ aⁿ = aᵐ⁻ⁿ vraie quand m = n."],
    ["La racine carrée d’une somme est-elle la somme des racines ?", "Non. Par exemple, √(9 + 16) = √25 = 5, alors que √9 + √16 = 3 + 4 = 7. En revanche, la racine d’un produit est le produit des racines : √(ab) = √a × √b pour a et b positifs."]
  ]
}
---
<!-- optitab:1 -->
## I. Développer et factoriser {Collège}

| Propriété | Formule |
|---|---|
| Distributivité simple | $k(a + b) = ka + kb$ |
| Distributivité avec une différence | $k(a - b) = ka - kb$ |
| Double distributivité | $(a + b)(c + d) = ac + ad + bc + bd$ |

::: methode Développer ou factoriser ?
- **Développer**, c’est transformer un produit en somme : $3(x + 2) = 3x + 6$.
- **Factoriser**, c’est transformer une somme en produit, en repérant un facteur commun : $5x + 5y = 5(x + y)$.
:::

## II. Identités remarquables {Collège}

[IMAGE_1]

| Identité | Formule |
|---|---|
| Carré d’une somme | $(a + b)^2 = a^2 + 2ab + b^2$ |
| Carré d’une différence | $(a - b)^2 = a^2 - 2ab + b^2$ |
| Produit d’une somme et d’une différence | $(a + b)(a - b) = a^2 - b^2$ |

::: attention Erreur fréquente
$(a + b)^2 \neq a^2 + b^2$ : il ne faut pas oublier le double produit $2ab$. Par exemple, $(3 + 4)^2 = 49$, alors que $3^2 + 4^2 = 25$.
:::

::: exemple Calcul mental et factorisation
- $102^2 = (100 + 2)^2 = 10\,000 + 400 + 4 = 10\,404$
- $x^2 - 9 = x^2 - 3^2 = (x + 3)(x - 3)$
- $x^2 + 6x + 9 = (x + 3)^2$
:::

## III. Identités du troisième degré {Lycée}

| Identité | Formule |
|---|---|
| Cube d’une somme | $(a + b)^3 = a^3 + 3a^2 b + 3ab^2 + b^3$ |
| Cube d’une différence | $(a - b)^3 = a^3 - 3a^2 b + 3ab^2 - b^3$ |
| Différence de deux cubes | $a^3 - b^3 = (a - b)(a^2 + ab + b^2)$ |
| Somme de deux cubes | $a^3 + b^3 = (a + b)(a^2 - ab + b^2)$ |

## IV. Fractions {Collège}

Pour $b$, $d$ non nuls (et $c$ non nul pour la division) :

| Opération | Formule |
|---|---|
| Même dénominateur | $\dfrac{a}{b} + \dfrac{c}{b} = \dfrac{a + c}{b}$ |
| Somme | $\dfrac{a}{b} + \dfrac{c}{d} = \dfrac{ad + bc}{bd}$ |
| Produit | $\dfrac{a}{b} \times \dfrac{c}{d} = \dfrac{ac}{bd}$ |
| Quotient | $\dfrac{a}{b} \div \dfrac{c}{d} = \dfrac{a}{b} \times \dfrac{d}{c}$ |
| Simplification | $\dfrac{ka}{kb} = \dfrac{a}{b}$ pour $k \neq 0$ |

::: conseil
Diviser par une fraction, c’est multiplier par son inverse. Pour additionner, on réduit d’abord au même dénominateur (le plus petit possible).
:::

## V. Puissances {Collège}

Pour $a$ et $b$ non nuls et $m$, $n$ entiers relatifs :

| Règle | Formule |
|---|---|
| Produit | $a^m \times a^n = a^{m+n}$ |
| Quotient | $\dfrac{a^m}{a^n} = a^{m-n}$ |
| Puissance d’une puissance | $(a^m)^n = a^{m \times n}$ |
| Puissance d’un produit | $(ab)^n = a^n b^n$ |
| Puissance d’un quotient | $\left(\dfrac{a}{b}\right)^n = \dfrac{a^n}{b^n}$ |
| Exposant nul | $a^0 = 1$ |
| Exposant négatif | $a^{-n} = \dfrac{1}{a^n}$ |

::: attention Erreur fréquente
$a^m + a^n \neq a^{m+n}$ : la règle des exposants ne vaut que pour les produits. De même, $(a + b)^n \neq a^n + b^n$.
:::

| Puissances de 10 | Écriture |
|---|---|
| $10^n$ avec $n > 0$ | $1$ suivi de $n$ zéros |
| $10^{-n}$ avec $n > 0$ | $0{,}0\ldots01$ avec $n$ chiffres après la virgule |
| Écriture scientifique | $a \times 10^n$ avec $1 \leqslant a < 10$ |

Par exemple, $45\,000 = 4{,}5 \times 10^4$ et $0{,}003\,2 = 3{,}2 \times 10^{-3}$.

## VI. Racines carrées {Collège}

Pour $a$ et $b$ positifs :

| Règle | Formule |
|---|---|
| Définition | $\sqrt{a}$ est le nombre positif dont le carré est $a$ |
| Carré d’une racine | $\left(\sqrt{a}\right)^2 = a$ |
| Racine d’un carré | $\sqrt{a^2} = a$ |
| Produit | $\sqrt{ab} = \sqrt{a} \times \sqrt{b}$ |
| Quotient ($b \neq 0$) | $\sqrt{\dfrac{a}{b}} = \dfrac{\sqrt{a}}{\sqrt{b}}$ |
| Enlever une racine du dénominateur | $\dfrac{1}{\sqrt{a}} = \dfrac{\sqrt{a}}{a}$ pour $a > 0$ |

::: attention Erreur fréquente
$\sqrt{a + b} \neq \sqrt{a} + \sqrt{b}$ : par exemple $\sqrt{9 + 16} = \sqrt{25} = 5$, alors que $\sqrt{9} + \sqrt{16} = 7$.
:::

::: exemple Simplifier une racine
$\sqrt{12} = \sqrt{4 \times 3} = 2\sqrt{3}$ et $\sqrt{50} = \sqrt{25 \times 2} = 5\sqrt{2}$.
:::

## VII. Valeur absolue {Lycée}

| Propriété | Formule |
|---|---|
| Définition | $\lvert x \rvert = x$ si $x \geqslant 0$, et $\lvert x \rvert = -x$ si $x < 0$ |
| Avec une racine | $\sqrt{x^2} = \lvert x \rvert$ pour tout réel $x$ |
| Produit | $\lvert ab \rvert = \lvert a \rvert \times \lvert b \rvert$ |
| Inégalité triangulaire | $\lvert a + b \rvert \leqslant \lvert a \rvert + \lvert b \rvert$ |
| Distance | $\lvert x - a \rvert \leqslant r \iff a - r \leqslant x \leqslant a + r$ |

## VIII. Binôme de Newton et sommes {Supérieur}

| Résultat | Formule |
|---|---|
| Binôme de Newton | $(a + b)^n = \displaystyle\sum_{k=0}^{n} \binom{n}{k} a^k b^{n-k}$ |
| Coefficient binomial | $\dbinom{n}{k} = \dfrac{n!}{k!\,(n - k)!}$ |
| Relation de Pascal | $\dbinom{n}{k} + \dbinom{n}{k+1} = \dbinom{n+1}{k+1}$ |
| Factorisation de $a^n - b^n$ | $a^n - b^n = (a - b)\displaystyle\sum_{k=0}^{n-1} a^k b^{n-1-k}$ |

::: exemple
$(a + b)^4 = a^4 + 4a^3 b + 6a^2 b^2 + 4ab^3 + b^4$ : les coefficients $1$, $4$, $6$, $4$, $1$ se lisent sur la ligne $n = 4$ du triangle de Pascal.
:::
