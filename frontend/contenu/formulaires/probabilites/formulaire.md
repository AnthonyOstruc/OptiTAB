---
{
  "slug": "probabilites",
  "titre": "Probabilités et dénombrement",
  "titreCourt": "Probabilités",
  "titreSeo": "Formules de probabilités : conditionnelles, binomiale, espérance",
  "description": "Toutes les formules de probabilités : probabilités conditionnelles, arbres, indépendance, espérance, variance, loi binomiale, dénombrement, loi normale.",
  "chapo": "Les formules de probabilités du collège au supérieur : calculs de base, probabilités conditionnelles et arbres pondérés, variables aléatoires, lois usuelles et dénombrement.",
  "resume": "Arbres, conditionnelles, espérance, loi binomiale",
  "vignette": "arbre_pondere",
  "theme": "Probabilités et statistiques",
  "niveaux": ["Collège", "Lycée", "Supérieur"],
  "ordre": 18,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["formules probabilités", "probabilité conditionnelle formule", "formule des probabilités totales", "loi binomiale formule", "espérance variance", "arbre pondéré", "combinaisons dénombrement", "loi normale"],
  "figures": [
    { "nom": "arbre_pondere", "alt": "Arbre pondéré à deux niveaux : A et non A, puis B et non B ; les probabilités conditionnelles P_A(B), P_A(non B)… sont écrites sur les branches." },
    { "nom": "loi_binomiale", "alt": "Diagramme en barres de la loi binomiale de paramètres n = 10 et p = 0,3 : les probabilités P(X = k) sont maximales autour de k = 3." },
    { "nom": "loi_normale", "alt": "Courbe en cloche de la loi normale : environ 68 % de la probabilité entre μ − σ et μ + σ, et 13,6 % entre μ − 2σ et μ − σ." }
  ],
  "chapitresLies": [
    "3e/probabilites",
    "seconde/modeliser-le-hasard-calculer-des-probabilites",
    "premiere/probabilites-conditionnelles-et-independance",
    "premiere/variables-aleatoires-reelles",
    "terminale/schema-de-bernoulli-et-loi-binomiale",
    "terminale/combinatoire-et-denombrement"
  ],
  "faq": [
    ["Quelle est la formule d’une probabilité conditionnelle ?", "Si P(A) ≠ 0, la probabilité de B sachant A est P_A(B) = P(A ∩ B) / P(A). On en déduit P(A ∩ B) = P(A) × P_A(B) : on multiplie les probabilités le long d’un chemin de l’arbre."],
    ["Comment calculer une probabilité avec la loi binomiale ?", "Si X suit la loi binomiale de paramètres n et p, alors P(X = k) = C(n, k) × pᵏ × (1 − p)ⁿ⁻ᵏ, où C(n, k) est le nombre de combinaisons. Son espérance vaut np et sa variance np(1 − p)."],
    ["Quelle est la différence entre événements incompatibles et indépendants ?", "Deux événements sont incompatibles s’ils ne peuvent pas se produire en même temps : P(A ∩ B) = 0. Ils sont indépendants si la réalisation de l’un ne change pas la probabilité de l’autre : P(A ∩ B) = P(A) × P(B)."],
    ["Comment calculer l’espérance d’une variable aléatoire ?", "On multiplie chaque valeur xᵢ par sa probabilité pᵢ et on additionne : E(X) = x₁p₁ + x₂p₂ + … + xₙpₙ. C’est la moyenne des valeurs obtenues sur un très grand nombre de répétitions."]
  ]
}
---
<!-- optitab:1 -->
## I. Calculs de base {Collège}

| Propriété | Formule |
|---|---|
| Probabilité d’un événement | $0 \leqslant P(A) \leqslant 1$ |
| Événement certain | $P(\Omega) = 1$ |
| Équiprobabilité | $P(A) = \dfrac{\text{nombre de cas favorables}}{\text{nombre de cas possibles}}$ |
| Événement contraire | $P(\overline{A}) = 1 - P(A)$ |

::: exemple
On lance un dé équilibré à six faces. $A$ : « obtenir un nombre pair ». Il y a $3$ cas favorables sur $6$ : $P(A) = \dfrac{3}{6} = \dfrac{1}{2}$.
:::

## II. Réunion et intersection {Lycée}

| Propriété | Formule |
|---|---|
| Réunion (« $A$ ou $B$ ») | $P(A \cup B) = P(A) + P(B) - P(A \cap B)$ |
| Événements incompatibles | $A \cap B = \varnothing$, donc $P(A \cup B) = P(A) + P(B)$ |

## III. Probabilités conditionnelles et indépendance {Lycée}

[IMAGE_1]

| Propriété | Formule |
|---|---|
| Probabilité de $B$ sachant $A$ ($P(A) \neq 0$) | $P_A(B) = \dfrac{P(A \cap B)}{P(A)}$ |
| Intersection | $P(A \cap B) = P(A) \times P_A(B)$ |
| Probabilités totales | $P(B) = P(A \cap B) + P(\overline{A} \cap B)$ |
| Événements indépendants | $P(A \cap B) = P(A) \times P(B)$ |

::: retenir Règles de l’arbre pondéré
- La somme des probabilités des branches issues d’un même nœud vaut $1$.
- La probabilité d’un chemin est le **produit** des probabilités de ses branches.
- La probabilité d’un événement est la **somme** des probabilités des chemins qui y mènent.
:::

::: attention Incompatibles ou indépendants ?
Deux événements **incompatibles** ne se produisent jamais ensemble ($P(A \cap B) = 0$). Deux événements **indépendants** vérifient $P(A \cap B) = P(A) \times P(B)$. Ce n’est pas la même chose.
:::

::: propriete Formule de Bayes
Si $P(B) \neq 0$ : $P_B(A) = \dfrac{P(A) \times P_A(B)}{P(B)}$.
:::

## IV. Variables aléatoires {Lycée}

Pour une variable aléatoire $X$ prenant les valeurs $x_1, \ldots, x_n$ avec les probabilités $p_1, \ldots, p_n$ :

| Notion | Formule |
|---|---|
| Espérance | $E(X) = \displaystyle\sum_{i=1}^{n} p_i\,x_i$ |
| Variance | $V(X) = \displaystyle\sum_{i=1}^{n} p_i\,\big(x_i - E(X)\big)^2$ |
| Formule de König-Huygens | $V(X) = E(X^2) - E(X)^2$ |
| Écart type | $\sigma(X) = \sqrt{V(X)}$ |
| Transformation affine | $E(aX + b) = aE(X) + b$ et $V(aX + b) = a^2\,V(X)$ |
| Somme | $E(X + Y) = E(X) + E(Y)$ |
| Somme de variables indépendantes | $V(X + Y) = V(X) + V(Y)$ |

## V. Lois discrètes usuelles {Lycée}

| Loi | Probabilités |
|---|---|
| Bernoulli $\mathcal{B}(p)$ | $P(X = 1) = p$ et $P(X = 0) = 1 - p$ |
| Binomiale $\mathcal{B}(n, p)$ | $P(X = k) = \dbinom{n}{k} p^k (1 - p)^{n-k}$ |
| Uniforme sur $\{1, \ldots, n\}$ | $P(X = k) = \dfrac{1}{n}$ |
| Géométrique $\mathcal{G}(p)$ | $P(X = k) = (1 - p)^{k-1}\,p$ pour $k \geqslant 1$ |
| Poisson $\mathcal{P}(\lambda)$ | $P(X = k) = \mathrm{e}^{-\lambda}\,\dfrac{\lambda^k}{k!}$ |

| Loi | Espérance | Variance |
|---|---|---|
| Bernoulli $\mathcal{B}(p)$ | $p$ | $p(1 - p)$ |
| Binomiale $\mathcal{B}(n, p)$ | $np$ | $np(1 - p)$ |
| Uniforme sur $\{1, \ldots, n\}$ | $\dfrac{n + 1}{2}$ | $\dfrac{n^2 - 1}{12}$ |
| Géométrique $\mathcal{G}(p)$ | $\dfrac{1}{p}$ | $\dfrac{1 - p}{p^2}$ |
| Poisson $\mathcal{P}(\lambda)$ | $\lambda$ | $\lambda$ |

Les lois géométrique et de Poisson sont étudiées dans le supérieur.

[IMAGE_2]

::: retenir Loi binomiale
$X$ compte le nombre de succès dans $n$ répétitions **indépendantes** d’une même épreuve de Bernoulli de paramètre $p$. Sur la figure, $n = 10$ et $p = 0{,}3$ : $E(X) = 3$.
:::

## VI. Dénombrement {Lycée}

Pour un ensemble à $n$ éléments :

| On choisit $k$ éléments… | Nombre de possibilités |
|---|---|
| ordonnés, avec répétition ($k$-uplets) | $n^k$ |
| ordonnés, sans répétition (arrangements) | $\dfrac{n!}{(n - k)!}$ |
| tous, dans un ordre (permutations) | $n!$ |
| sans ordre, sans répétition (combinaisons) | $\dbinom{n}{k} = \dfrac{n!}{k!\,(n - k)!}$ |
| toutes les parties de l’ensemble | $2^n$ |

::: retenir Propriétés des coefficients binomiaux
$\dbinom{n}{k} = \dbinom{n}{n - k}$ et $\dbinom{n}{k} + \dbinom{n}{k + 1} = \dbinom{n + 1}{k + 1}$ (triangle de Pascal).
:::

## VII. Inégalités et loi des grands nombres {Lycée}

| Résultat | Formule |
|---|---|
| Inégalité de Bienaymé-Tchebychev | $P\big(\lvert X - E(X) \rvert \geqslant \delta\big) \leqslant \dfrac{V(X)}{\delta^2}$ |
| Inégalité de concentration (moyenne $M_n$) | $P\big(\lvert M_n - \mu \rvert \geqslant \delta\big) \leqslant \dfrac{V(X)}{n\,\delta^2}$ |
| Inégalité de Markov ($X \geqslant 0$, $a > 0$) | $P(X \geqslant a) \leqslant \dfrac{E(X)}{a}$ |

**Loi des grands nombres** : la moyenne $M_n$ de $n$ variables indépendantes de même loi, d’espérance $\mu$, se rapproche de $\mu$ quand $n$ devient grand.

## VIII. Lois à densité {Supérieur}

| Loi | Probabilités |
|---|---|
| Uniforme sur $[a\,;b]$ | $P(c \leqslant X \leqslant d) = \dfrac{d - c}{b - a}$ pour $a \leqslant c \leqslant d \leqslant b$ |
| Exponentielle $\mathcal{E}(\lambda)$ | $P(X \leqslant t) = 1 - \mathrm{e}^{-\lambda t}$ pour $t \geqslant 0$ |
| Normale $\mathcal{N}(\mu, \sigma^2)$ | voir la courbe en cloche ci-dessous |

| Loi | Espérance | Variance |
|---|---|---|
| Uniforme sur $[a\,;b]$ | $\dfrac{a + b}{2}$ | $\dfrac{(b - a)^2}{12}$ |
| Exponentielle $\mathcal{E}(\lambda)$ | $\dfrac{1}{\lambda}$ | $\dfrac{1}{\lambda^2}$ |
| Normale $\mathcal{N}(\mu, \sigma^2)$ | $\mu$ | $\sigma^2$ |

[IMAGE_3]

::: retenir Intervalles de la loi normale
$P(\mu - \sigma \leqslant X \leqslant \mu + \sigma) \approx 0{,}683$, $P(\mu - 2\sigma \leqslant X \leqslant \mu + 2\sigma) \approx 0{,}954$ et $P(\mu - 3\sigma \leqslant X \leqslant \mu + 3\sigma) \approx 0{,}997$.
:::
