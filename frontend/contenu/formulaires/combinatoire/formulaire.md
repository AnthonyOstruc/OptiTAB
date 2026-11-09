---
{
  "slug": "combinatoire",
  "titre": "Combinatoire et dénombrement",
  "titreCourt": "Combinatoire",
  "titreSeo": "Combinatoire : coefficients binomiaux, arrangements, Pascal",
  "description": "Les formules de dénombrement : listes, arrangements, permutations, combinaisons, coefficients binomiaux, triangle de Pascal, binôme de Newton, exemples.",
  "chapo": "Comment compter sans se tromper : le bon modèle selon que l’ordre compte ou non, les factorielles, les coefficients binomiaux et leurs propriétés, le triangle de Pascal et le binôme de Newton.",
  "resume": "Arrangements, combinaisons, triangle de Pascal",
  "vignette": "triangle_pascal",
  "theme": "Probabilités",
  "niveaux": ["Lycée", "Supérieur"],
  "ordre": 19,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["combinatoire", "dénombrement formules", "coefficient binomial", "k parmi n", "arrangement et combinaison", "triangle de Pascal", "binôme de Newton", "factorielle"],
  "figures": [
    { "nom": "triangle_pascal", "alt": "Triangle de Pascal des lignes 0 à 6 : chaque nombre est la somme des deux nombres situés au-dessus de lui, par exemple 4 + 6 = 10." }
  ],
  "chapitresLies": [
    "terminale/combinatoire-et-denombrement",
    "terminale/schema-de-bernoulli-et-loi-binomiale"
  ],
  "faq": [
    ["Quelle est la formule de k parmi n ?", "Le coefficient binomial « k parmi n » vaut n! / (k! (n − k)!). Il compte le nombre de façons de choisir k éléments parmi n, sans tenir compte de l’ordre."],
    ["Quelle différence entre arrangement et combinaison ?", "Dans un arrangement, l’ordre des éléments choisis compte (un podium) ; dans une combinaison, il ne compte pas (un groupe). Il y a k! fois plus d’arrangements que de combinaisons."],
    ["Combien vaut 0! ?", "Par convention, 0! = 1. Ainsi la formule de « k parmi n » reste valable pour k = 0 et pour k = n."],
    ["À quoi sert le triangle de Pascal ?", "Il donne les coefficients binomiaux ligne par ligne, chaque nombre étant la somme des deux nombres au-dessus. On y lit par exemple les coefficients de (a + b)⁴ : 1, 4, 6, 4, 1."]
  ]
}
---
<!-- optitab:1 -->
## I. Principes de base {Lycée}

On note $\lvert A \rvert$, ou $\operatorname{card}(A)$, le nombre d’éléments de l’ensemble fini $A$.

| Principe | Formule |
|---|---|
| Produit cartésien | $\lvert A \times B \rvert = \lvert A \rvert \times \lvert B \rvert$ |
| Réunion | $\lvert A \cup B \rvert = \lvert A \rvert + \lvert B \rvert - \lvert A \cap B \rvert$ |
| Complémentaire dans $E$ | $\lvert \overline{A} \rvert = \lvert E \rvert - \lvert A \rvert$ |
| Nombre de parties d’un ensemble à $n$ éléments | $2^n$ |

## II. Choisir le bon modèle {Lycée}

On choisit $k$ éléments parmi $n$.

| Situation | Nombre de possibilités |
|---|---|
| L’ordre compte, répétitions permises ($k$-uplets) | $n^k$ |
| L’ordre compte, sans répétition (arrangements) | $\dfrac{n!}{(n - k)!}$ |
| On range les $n$ éléments (permutations) | $n!$ |
| L’ordre ne compte pas, sans répétition (combinaisons) | $\dbinom{n}{k}$ |

| Exemple (modèle) | Résultat |
|---|---|
| Code de $4$ chiffres ($4$-uplets) | $10^4 = 10\,000$ |
| Podium de $3$ parmi $8$ coureurs (arrangements) | $8 \times 7 \times 6 = 336$ |
| Groupe de $3$ parmi $8$ personnes (combinaisons) | $\dbinom{8}{3} = 56$ |
| Anagrammes de MATHS (permutations) | $5! = 120$ |

::: methode Deux questions à se poser
1. **L’ordre compte-t-il ?** Un podium, un code : oui. Une équipe, une main de cartes : non.
2. **Peut-on reprendre le même élément ?** Un code : oui. Des personnes distinctes : non.
:::

::: exemple Anagrammes avec des lettres répétées
ANANAS a $6$ lettres dont $3$ A et $2$ N. On divise par les permutations des lettres identiques :
$$\frac{6!}{3! \times 2!} = \frac{720}{12} = 60$$
:::

## III. Factorielles {Lycée}

$n! = 1 \times 2 \times \dots \times n$, avec $0! = 1$.

| $n$ | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
|---|---|---|---|---|---|---|
| $n!$ | $1$ | $1$ | $2$ | $6$ | $24$ | $120$ |

| $n$ | $6$ | $7$ | $8$ | $9$ | $10$ |
|---|---|---|---|---|---|
| $n!$ | $720$ | $5\,040$ | $40\,320$ | $362\,880$ | $3\,628\,800$ |

## IV. Coefficients binomiaux {Lycée}

::: formule Coefficient binomial « $k$ parmi $n$ » ($0 \leqslant k \leqslant n$)
$$\binom{n}{k} = \frac{n!}{k!\,(n - k)!}$$
:::

| Propriété | Formule |
|---|---|
| Valeurs simples | $\dbinom{n}{0} = \dbinom{n}{n} = 1$ et $\dbinom{n}{1} = n$ |
| $2$ parmi $n$ | $\dbinom{n}{2} = \dfrac{n(n - 1)}{2}$ |
| Symétrie | $\dbinom{n}{k} = \dbinom{n}{n - k}$ |
| Relation de Pascal | $\dbinom{n}{k} + \dbinom{n}{k + 1} = \dbinom{n + 1}{k + 1}$ |
| Somme d’une ligne | $\displaystyle\sum_{k=0}^{n} \binom{n}{k} = 2^n$ |
| Formule du capitaine | $k\dbinom{n}{k} = n\dbinom{n - 1}{k - 1}$ |

## V. Triangle de Pascal {Lycée}

[IMAGE_1]

Valeurs de $\dbinom{n}{k}$ ; la symétrie donne les colonnes suivantes.

| $n$ | $k = 0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
|---|---|---|---|---|---|---|
| $0$ | $1$ | | | | | |
| $1$ | $1$ | $1$ | | | | |
| $2$ | $1$ | $2$ | $1$ | | | |
| $3$ | $1$ | $3$ | $3$ | $1$ | | |
| $4$ | $1$ | $4$ | $6$ | $4$ | $1$ | |
| $5$ | $1$ | $5$ | $10$ | $10$ | $5$ | $1$ |
| $6$ | $1$ | $6$ | $15$ | $20$ | $15$ | $6$ |
| $7$ | $1$ | $7$ | $21$ | $35$ | $35$ | $21$ |
| $8$ | $1$ | $8$ | $28$ | $56$ | $70$ | $56$ |
| $9$ | $1$ | $9$ | $36$ | $84$ | $126$ | $126$ |
| $10$ | $1$ | $10$ | $45$ | $120$ | $210$ | $252$ |

::: formule Binôme de Newton
$$(a + b)^n = \sum_{k=0}^{n} \binom{n}{k} a^k b^{n-k}$$
:::

::: exemple
$$(a + b)^4 = a^4 + 4a^3b + 6a^2b^2 + 4ab^3 + b^4$$
:::

## VI. Dénombrement et probabilités {Lycée}

| Situation | Formule |
|---|---|
| Équiprobabilité | $P(A) = \dfrac{\lvert A \rvert}{\lvert \Omega \rvert}$ |
| Loi binomiale $\mathcal{B}(n, p)$ | $P(X = k) = \dbinom{n}{k} p^k (1 - p)^{n-k}$ |

::: exemple Tirage simultané de $2$ boules parmi $5$ rouges et $3$ noires
Il y a $\dbinom{8}{2} = 28$ tirages possibles, dont $\dbinom{5}{2} = 10$ avec deux boules rouges :
$$P(\text{2 rouges}) = \frac{10}{28} = \frac{5}{14}$$
:::

::: propriete Combinaisons avec répétition (supérieur)
Le nombre de façons de choisir $k$ éléments parmi $n$, sans ordre et avec répétitions possibles, vaut $\dbinom{n + k - 1}{k}$.
:::
