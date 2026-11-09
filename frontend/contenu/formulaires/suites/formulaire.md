---
{
  "slug": "suites",
  "titre": "Suites arithmétiques et géométriques",
  "titreCourt": "Suites",
  "titreSeo": "Suites arithmétiques et géométriques : formules et sommes",
  "description": "Toutes les formules des suites : terme général, sommes des suites arithmétiques et géométriques, limites, suites arithmético-géométriques, récurrence.",
  "chapo": "Les formules des suites arithmétiques et géométriques, leurs sommes et leurs limites, puis les suites arithmético-géométriques et les sommes usuelles du supérieur.",
  "resume": "Terme général, somme des termes, limite de qⁿ",
  "vignette": "suites_points",
  "theme": "Suites",
  "niveaux": ["Lycée", "Supérieur"],
  "ordre": 4,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["suite arithmétique formule", "suite géométrique formule", "somme suite géométrique", "somme suite arithmétique", "terme général", "limite q puissance n", "suite arithmético-géométrique", "raisonnement par récurrence"],
  "figures": [
    { "nom": "suites_points", "alt": "Premiers termes d’une suite arithmétique, dont les points sont alignés, et d’une suite géométrique de raison supérieure à 1, dont les points s’écartent de plus en plus vite." }
  ],
  "chapitresLies": [
    "premiere/suites-numeriques-modeles-discrets",
    "terminale/limites-et-convergence-des-suites"
  ],
  "faq": [
    ["Comment savoir si une suite est arithmétique ?", "On calcule la différence u(n+1) − u(n). Si elle est constante, égale à un nombre r qui ne dépend pas de n, la suite est arithmétique de raison r."],
    ["Comment savoir si une suite est géométrique ?", "Si les termes sont non nuls, on calcule le quotient u(n+1) ÷ u(n). S’il est constant, égal à un nombre q qui ne dépend pas de n, la suite est géométrique de raison q. On peut aussi montrer directement que u(n+1) = q × u(n)."],
    ["Quelle est la formule de la somme des termes d’une suite géométrique ?", "Pour une raison q ≠ 1, la somme de N termes consécutifs vaut : premier terme × (1 − q^N) ÷ (1 − q). Par exemple, 5 + 10 + 20 + 40 + 80 = 5 × (1 − 2⁵) ÷ (1 − 2) = 155."],
    ["Quelle est la limite de qⁿ ?", "Si q > 1, qⁿ tend vers +∞. Si −1 < q < 1, qⁿ tend vers 0. Si q = 1, qⁿ vaut toujours 1. Si q ≤ −1, la suite qⁿ n’a pas de limite."]
  ]
}
---
<!-- optitab:1 -->
## I. Suites arithmétiques {Lycée}

| Propriété | Formule |
|---|---|
| Définition (raison $r$) | $u_{n+1} = u_n + r$ |
| Terme général | $u_n = u_0 + nr$ |
| À partir du rang $p$ | $u_n = u_p + (n - p)\,r$ |
| Somme des entiers | $1 + 2 + \cdots + n = \dfrac{n(n + 1)}{2}$ |
| Somme de $N$ termes consécutifs | $N \times \dfrac{\text{premier} + \text{dernier}}{2}$ |

- Si $r > 0$, la suite est strictement croissante ; si $r < 0$, strictement décroissante.
- Les points de coordonnées $(n\,;u_n)$ sont alignés.

::: exemple $u_0 = 3$ et $r = 2$
$u_{10} = 3 + 10 \times 2 = 23$, et $u_0 + u_1 + \cdots + u_{10} = 11 \times \dfrac{3 + 23}{2} = 143$.
:::

## II. Suites géométriques {Lycée}

| Propriété | Formule |
|---|---|
| Définition (raison $q$) | $u_{n+1} = q \times u_n$ |
| Terme général | $u_n = u_0 \times q^n$ |
| À partir du rang $p$ | $u_n = u_p \times q^{\,n - p}$ |
| Somme des puissances ($q \neq 1$) | $1 + q + q^2 + \cdots + q^n = \dfrac{1 - q^{n+1}}{1 - q}$ |
| Somme de $N$ termes consécutifs ($q \neq 1$) | $\text{premier} \times \dfrac{1 - q^N}{1 - q}$ |

Pour $u_0 > 0$ : si $q > 1$, la suite est strictement croissante ; si $0 < q < 1$, strictement décroissante ; si $q < 0$, ses termes changent de signe à chaque rang.

::: exemple $u_0 = 5$ et $q = 2$
$u_4 = 5 \times 2^4 = 80$, et $u_0 + u_1 + \cdots + u_4 = 5 \times \dfrac{1 - 2^5}{1 - 2} = 155$.
:::

[IMAGE_1]

## III. Limites {Lycée}

| Raison $q$ | Limite de $q^n$ |
|---|---|
| $q > 1$ | $\displaystyle\lim_{n \to +\infty} q^n = +\infty$ |
| $q = 1$ | $q^n = 1$ pour tout $n$ |
| $-1 < q < 1$ | $\displaystyle\lim_{n \to +\infty} q^n = 0$ |
| $q \leqslant -1$ | pas de limite |

Si $-1 < q < 1$ : $\displaystyle\lim_{n \to +\infty} \left(1 + q + \cdots + q^n\right) = \frac{1}{1 - q}$.

::: retenir Théorèmes de convergence
- Une suite croissante et majorée converge ; une suite décroissante et minorée converge.
- Une suite croissante et non majorée tend vers $+\infty$.
- **Comparaison** : si $u_n \geqslant v_n$ à partir d’un certain rang et $v_n \to +\infty$, alors $u_n \to +\infty$.
- **Gendarmes** : si $v_n \leqslant u_n \leqslant w_n$ et si $v_n$ et $w_n$ tendent vers $\ell$, alors $u_n \to \ell$.
:::

## IV. Suites arithmético-géométriques {Lycée}

On étudie $u_{n+1} = a\,u_n + b$, avec $a \neq 1$.

| Étape | Formule |
|---|---|
| Point fixe | $\ell = \dfrac{b}{1 - a}$ (solution de $\ell = a\ell + b$) |
| Suite auxiliaire | $v_n = u_n - \ell$ est géométrique de raison $a$ |
| Terme général | $u_n = a^n\,(u_0 - \ell) + \ell$ |

::: exemple $u_{n+1} = 0{,}5\,u_n + 3$ et $u_0 = 2$
$\ell = \dfrac{3}{1 - 0{,}5} = 6$, donc $u_n = 6 - 4 \times 0{,}5^n$. Comme $0{,}5^n \to 0$, la suite converge vers $6$.
:::

## V. Raisonnement par récurrence {Lycée}

::: methode Démontrer qu’une propriété $P(n)$ est vraie pour tout $n \geqslant n_0$
1. **Initialisation** : on vérifie que $P(n_0)$ est vraie.
2. **Hérédité** : on suppose $P(n)$ vraie pour un entier $n \geqslant n_0$, et on démontre $P(n + 1)$.
3. **Conclusion** : $P(n)$ est vraie pour tout entier $n \geqslant n_0$.
:::

## VI. Sommes usuelles et récurrences d’ordre 2 {Supérieur}

| Somme | Formule |
|---|---|
| Somme des entiers | $\displaystyle\sum_{k=1}^{n} k = \frac{n(n + 1)}{2}$ |
| Somme des carrés | $\displaystyle\sum_{k=1}^{n} k^2 = \frac{n(n + 1)(2n + 1)}{6}$ |
| Somme des cubes | $\displaystyle\sum_{k=1}^{n} k^3 = \left(\frac{n(n + 1)}{2}\right)^2$ |
| Somme géométrique ($q \neq 1$) | $\displaystyle\sum_{k=0}^{n} q^k = \frac{1 - q^{n+1}}{1 - q}$ |

::: propriete Suites récurrentes linéaires d’ordre 2
Pour $u_{n+2} = a\,u_{n+1} + b\,u_n$, on résout l’équation caractéristique $r^2 = ar + b$.
- Deux racines réelles distinctes $r_1$ et $r_2$ : $u_n = \lambda r_1^{\,n} + \mu r_2^{\,n}$.
- Une racine double $r$ : $u_n = (\lambda + \mu n)\,r^n$.

Les constantes $\lambda$ et $\mu$ se déterminent avec $u_0$ et $u_1$.
:::
