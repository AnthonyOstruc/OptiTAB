---
{
  "slug": "lois-de-probabilite",
  "titre": "Lois de probabilité usuelles",
  "titreCourt": "Lois de probabilité",
  "titreSeo": "Lois de probabilité : binomiale, Poisson, géométrique, normale",
  "description": "Toutes les lois de probabilité : Bernoulli, binomiale, géométrique, Poisson, uniforme, exponentielle, normale, intervalles de fluctuation et de confiance.",
  "chapo": "Chaque loi usuelle avec sa situation type, sa formule, son espérance, sa variance et sa représentation, puis les intervalles de fluctuation et de confiance et les approximations.",
  "resume": "Binomiale, Poisson, géométrique, normale, intervalles",
  "vignette": "centree_reduite",
  "theme": "Probabilités et statistiques",
  "niveaux": ["Lycée", "Supérieur"],
  "ordre": 13,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["lois de probabilité", "loi binomiale", "loi de Poisson", "loi géométrique", "loi normale", "loi exponentielle", "intervalle de confiance", "intervalle de fluctuation", "espérance variance loi"],
  "figures": [
    { "nom": "bernoulli_uniforme", "alt": "Diagrammes en barres de la loi de Bernoulli de paramètre 0,3 (0,7 pour 0 et 0,3 pour 1) et de la loi uniforme sur {1, …, 6}, où chaque valeur a la probabilité 1/6." },
    { "nom": "binomiales", "alt": "Diagrammes en barres des lois binomiales de paramètres (10 ; 0,3), maximale vers 3, et (10 ; 0,5), symétrique autour de 5." },
    { "nom": "geometrique", "alt": "Diagramme en barres de la loi géométrique de paramètre 0,3 : les probabilités décroissent à partir de k = 1." },
    { "nom": "poisson", "alt": "Diagrammes en barres des lois de Poisson de paramètres 1 et 4 : la masse se déplace vers la droite quand λ augmente." },
    { "nom": "uniforme_exponentielle", "alt": "Densité de la loi uniforme sur [1 ; 3], constante égale à 1/2, et densité de la loi exponentielle de paramètre 1, avec l’aire P(X ≤ 1) ≈ 63 % colorée." },
    { "nom": "normales", "alt": "Trois courbes en cloche de lois normales centrées en 0, d’écarts types 0,5, 1 et 2 : plus σ est grand, plus la courbe est étalée." },
    { "nom": "centree_reduite", "alt": "Densité de la loi normale centrée réduite : l’aire entre −1,96 et 1,96 vaut 0,95, et chacune des deux queues vaut 0,025." }
  ],
  "chapitresLies": [
    "premiere/variables-aleatoires-reelles",
    "terminale/schema-de-bernoulli-et-loi-binomiale",
    "terminale/sommes-de-variables-aleatoires",
    "terminale/concentration-loi-des-grands-nombres"
  ],
  "faq": [
    ["Quand utiliser la loi binomiale ?", "Quand on répète n fois, de façon indépendante, une même épreuve à deux issues (succès de probabilité p ou échec), et que X compte le nombre de succès. Alors P(X = k) = C(n, k) pᵏ (1 − p)ⁿ⁻ᵏ."],
    ["Quand utiliser la loi de Poisson ?", "Pour compter des événements rares sur une durée ou un espace donné : appels reçus en une heure, pannes dans un mois… Son unique paramètre λ est le nombre moyen d’événements, qui est à la fois l’espérance et la variance."],
    ["Que signifie le nombre 1,96 ?", "Pour la loi normale centrée réduite, P(−1,96 ≤ Z ≤ 1,96) ≈ 0,95. C’est pourquoi il apparaît dans les intervalles de fluctuation et de confiance au niveau 95 %."],
    ["Comment centrer et réduire une loi normale ?", "Si X suit la loi normale d’espérance μ et d’écart type σ, alors Z = (X − μ)/σ suit la loi normale centrée réduite. On se ramène ainsi aux valeurs connues de Z, comme 1,96."]
  ]
}
---
<!-- optitab:1 -->
## I. Rappels sur les variables aléatoires {Lycée}

| Notion | Formule |
|---|---|
| Espérance (loi discrète) | $E(X) = \displaystyle\sum_{k} k\,P(X = k)$ |
| Variance | $V(X) = E\big((X - E(X))^2\big)$ |
| Formule de König-Huygens | $V(X) = E(X^2) - E(X)^2$ |
| Écart type | $\sigma(X) = \sqrt{V(X)}$ |
| Fonction de répartition | $F(x) = P(X \leqslant x)$ |
| Loi à densité $f$ | $P(a \leqslant X \leqslant b) = \displaystyle\int_a^b f(t)\,\mathrm{d}t$ |
| Espérance (loi à densité) | $E(X) = \displaystyle\int t\,f(t)\,\mathrm{d}t$ |

## II. Lois discrètes {Lycée}

### Loi de Bernoulli $\mathcal{B}(p)$

| Élément | Valeur |
|---|---|
| Situation | une épreuve à deux issues : succès ($1$) ou échec ($0$) |
| Probabilités | $P(X = 1) = p$ et $P(X = 0) = 1 - p$ |
| Espérance | $E(X) = p$ |
| Variance | $V(X) = p(1 - p)$ |

### Loi uniforme sur $\{1, \ldots, n\}$

| Élément | Valeur |
|---|---|
| Situation | $n$ issues équiprobables (dé équilibré, tirage au hasard) |
| Probabilités | $P(X = k) = \dfrac{1}{n}$ pour $k \in \{1, \ldots, n\}$ |
| Espérance | $E(X) = \dfrac{n + 1}{2}$ |
| Variance | $V(X) = \dfrac{n^2 - 1}{12}$ |

[IMAGE_1]

### Loi binomiale $\mathcal{B}(n, p)$

| Élément | Valeur |
|---|---|
| Situation | nombre de succès en $n$ répétitions **indépendantes** d’une épreuve de Bernoulli |
| Valeurs prises | $0, 1, \ldots, n$ |
| Probabilités | $P(X = k) = \dbinom{n}{k}\,p^k\,(1 - p)^{n - k}$ |
| Espérance | $E(X) = np$ |
| Variance | $V(X) = np(1 - p)$ |

[IMAGE_2]

::: conseil
Pour $p = 0{,}5$, la loi binomiale est symétrique autour de $\dfrac{n}{2}$. Les calculs du type $P(X \leqslant k)$ se font à la calculatrice (fonction « binomiale cumulée »).
:::

### Loi géométrique $\mathcal{G}(p)$

| Élément | Valeur |
|---|---|
| Situation | rang du **premier** succès dans des épreuves de Bernoulli indépendantes |
| Valeurs prises | $1, 2, 3, \ldots$ |
| Probabilités | $P(X = k) = (1 - p)^{k - 1}\,p$ |
| Queue de la loi | $P(X > k) = (1 - p)^k$ |
| Espérance | $E(X) = \dfrac{1}{p}$ |
| Variance | $V(X) = \dfrac{1 - p}{p^2}$ |

[IMAGE_3]

::: retenir Absence de mémoire
$P_{X > n}(X > n + k) = P(X > k)$ : avoir déjà échoué $n$ fois ne change pas la probabilité d’attendre encore $k$ épreuves.
:::

### Loi de Poisson $\mathcal{P}(\lambda)$

| Élément | Valeur |
|---|---|
| Situation | nombre d’événements rares sur une durée ou un espace donné |
| Valeurs prises | $0, 1, 2, \ldots$ |
| Probabilités | $P(X = k) = \mathrm{e}^{-\lambda}\,\dfrac{\lambda^k}{k!}$ |
| Espérance | $E(X) = \lambda$ |
| Variance | $V(X) = \lambda$ |

[IMAGE_4]

### Loi hypergéométrique

| Élément | Valeur |
|---|---|
| Situation | tirage **sans remise** de $n$ objets parmi $N$, dont $K$ sont « gagnants » |
| Probabilités | $P(X = k) = \dfrac{\dbinom{K}{k}\dbinom{N - K}{n - k}}{\dbinom{N}{n}}$ |
| Espérance | $E(X) = n\,\dfrac{K}{N}$ |

::: attention Avec ou sans remise ?
Avec remise, les tirages sont indépendants : loi binomiale. Sans remise, ils ne le sont plus : loi hypergéométrique. Quand $N$ est grand devant $n$, les deux lois sont très proches.
:::

## III. Lois à densité {Lycée}

[IMAGE_5]

### Loi uniforme sur $[a\,;b]$

| Élément | Valeur |
|---|---|
| Densité | $f(x) = \dfrac{1}{b - a}$ sur $[a\,;b]$, et $0$ ailleurs |
| Probabilités | $P(c \leqslant X \leqslant d) = \dfrac{d - c}{b - a}$ pour $a \leqslant c \leqslant d \leqslant b$ |
| Espérance | $E(X) = \dfrac{a + b}{2}$ |
| Variance | $V(X) = \dfrac{(b - a)^2}{12}$ |

### Loi exponentielle $\mathcal{E}(\lambda)$

| Élément | Valeur |
|---|---|
| Situation | durée de vie sans vieillissement, temps d’attente |
| Densité | $f(x) = \lambda\,\mathrm{e}^{-\lambda x}$ pour $x \geqslant 0$ |
| Probabilités | $P(X \leqslant t) = 1 - \mathrm{e}^{-\lambda t}$ et $P(X > t) = \mathrm{e}^{-\lambda t}$ |
| Espérance | $E(X) = \dfrac{1}{\lambda}$ |
| Variance | $V(X) = \dfrac{1}{\lambda^2}$ |
| Médiane (demi-vie) | $t_{1/2} = \dfrac{\ln 2}{\lambda}$ |

::: retenir Absence de mémoire
$P_{X > s}(X > s + t) = P(X > t)$ : la loi exponentielle est la version continue de la loi géométrique.
:::

### Loi normale $\mathcal{N}(\mu, \sigma^2)$

[IMAGE_6]

| Élément | Valeur |
|---|---|
| Densité | $f(x) = \dfrac{1}{\sigma\sqrt{2\pi}}\exp\left(-\dfrac{(x - \mu)^2}{2\sigma^2}\right)$ |
| Espérance | $E(X) = \mu$ |
| Variance | $V(X) = \sigma^2$ |
| Centrer et réduire | $Z = \dfrac{X - \mu}{\sigma}$ suit la loi $\mathcal{N}(0, 1)$ |
| Symétrie de $\mathcal{N}(0, 1)$ | $P(Z \leqslant -a) = 1 - P(Z \leqslant a)$ |

[IMAGE_7]

| Intervalle | Probabilité |
|---|---|
| $[\mu - \sigma\,;\mu + \sigma]$ | $\approx 0{,}683$ |
| $[\mu - 2\sigma\,;\mu + 2\sigma]$ | $\approx 0{,}954$ |
| $[\mu - 3\sigma\,;\mu + 3\sigma]$ | $\approx 0{,}997$ |
| $[\mu - 1{,}96\,\sigma\,;\mu + 1{,}96\,\sigma]$ | $\approx 0{,}95$ |
| $[\mu - 2{,}58\,\sigma\,;\mu + 2{,}58\,\sigma]$ | $\approx 0{,}99$ |

## IV. Intervalles de fluctuation et de confiance {Lycée}

Pour un échantillon de taille $n$ et une proportion $p$ (ou une fréquence observée $f$), au niveau $95\,\%$ :

Chaque intervalle est centré, de la forme $[c - r\,;c + r]$, noté ci-dessous $c \pm r$.

| Intervalle | Centre $\pm$ demi-largeur |
|---|---|
| Fluctuation de la fréquence | $p \pm 1{,}96\sqrt{\dfrac{p(1 - p)}{n}}$ |
| Confiance pour une proportion | $f \pm 1{,}96\sqrt{\dfrac{f(1 - f)}{n}}$ |
| Confiance (version simplifiée) | $f \pm \dfrac{1}{\sqrt{n}}$ |
| Confiance pour une moyenne ($\sigma$ connu) | $\bar{x} \pm 1{,}96\,\dfrac{\sigma}{\sqrt{n}}$ |

::: exemple Sondage auprès de $n = 400$ personnes
$f = 0{,}52$ : l’intervalle de confiance simplifié est $0{,}52 \pm \dfrac{1}{20}$, soit $[0{,}47\,;0{,}57]$.
:::

::: attention Conditions d’utilisation
$n \geqslant 30$, $np \geqslant 5$ et $n(1 - p) \geqslant 5$ (avec $f$ à la place de $p$ pour un intervalle de confiance).
:::

::: methode Prise de décision
Si la fréquence observée $f$ sort de l’intervalle de fluctuation, on rejette l’hypothèse « la proportion vaut $p$ », avec un risque d’erreur de $5\,\%$.
:::

## V. Sommes et approximations {Supérieur}

| Résultat | Formule |
|---|---|
| Somme de binomiales indépendantes | $\mathcal{B}(n_1, p) + \mathcal{B}(n_2, p)$ suit $\mathcal{B}(n_1 + n_2, p)$ |
| Somme de Poisson indépendantes | $\mathcal{P}(\lambda) + \mathcal{P}(\mu)$ suit $\mathcal{P}(\lambda + \mu)$ |
| Somme de normales indépendantes | $\mathcal{N}(\mu_1, \sigma_1^2) + \mathcal{N}(\mu_2, \sigma_2^2)$ suit $\mathcal{N}(\mu_1 + \mu_2, \sigma_1^2 + \sigma_2^2)$ |
| Binomiale vers Poisson | $\mathcal{B}(n, p) \approx \mathcal{P}(np)$ si $n \geqslant 30$, $p \leqslant 0{,}1$ et $np < 15$ |
| Binomiale vers normale | $\mathcal{B}(n, p) \approx \mathcal{N}\big(np,\,np(1 - p)\big)$ si $n \geqslant 30$, $np \geqslant 5$ et $n(1 - p) \geqslant 5$ |

::: theoreme Théorème central limite
Si $X_1, \ldots, X_n$ sont indépendantes, de même loi, d’espérance $\mu$ et d’écart type $\sigma$, la moyenne $\bar{X}_n$ suit approximativement, pour $n$ grand, la loi $\mathcal{N}\left(\mu, \dfrac{\sigma^2}{n}\right)$.
:::

::: conseil Correction de continuité
Pour approcher une loi discrète par une loi normale $Y$, on écrit $P(X \leqslant k) \approx P(Y \leqslant k + 0{,}5)$.
:::

## VI. Récapitulatif {Lycée}

| Loi | Espérance | Variance |
|---|---|---|
| Bernoulli $\mathcal{B}(p)$ | $p$ | $p(1 - p)$ |
| Binomiale $\mathcal{B}(n, p)$ | $np$ | $np(1 - p)$ |
| Uniforme sur $\{1, \ldots, n\}$ | $\dfrac{n + 1}{2}$ | $\dfrac{n^2 - 1}{12}$ |
| Géométrique $\mathcal{G}(p)$ | $\dfrac{1}{p}$ | $\dfrac{1 - p}{p^2}$ |
| Poisson $\mathcal{P}(\lambda)$ | $\lambda$ | $\lambda$ |
| Uniforme sur $[a\,;b]$ | $\dfrac{a + b}{2}$ | $\dfrac{(b - a)^2}{12}$ |
| Exponentielle $\mathcal{E}(\lambda)$ | $\dfrac{1}{\lambda}$ | $\dfrac{1}{\lambda^2}$ |
| Normale $\mathcal{N}(\mu, \sigma^2)$ | $\mu$ | $\sigma^2$ |
