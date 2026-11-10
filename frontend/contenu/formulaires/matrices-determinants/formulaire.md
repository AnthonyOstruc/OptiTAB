---
{
  "slug": "matrices-determinants",
  "titre": "Matrices et déterminants",
  "titreCourt": "Matrices et déterminants",
  "titreSeo": "Matrices et déterminants : formulaire (produit, inverse, 2×2, 3×3)",
  "description": "Les formules sur les matrices : produit, transposée, déterminant 2×2 et 3×3 (Sarrus), inverse, systèmes linéaires, puissances, graphes et valeurs propres.",
  "chapo": "Le calcul matriciel en une page : produit de matrices, déterminant d’une matrice 2 × 2 et 3 × 3, inverse, résolution de systèmes, puissances de matrices et applications aux suites et aux graphes.",
  "resume": "Produit, déterminant, inverse, systèmes",
  "vignette": "produit_matrices",
  "theme": "Algèbre",
  "niveaux": ["Lycée", "Supérieur"],
  "ordre": 27,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["matrices formules", "produit de matrices", "déterminant 2x2", "déterminant 3x3", "règle de Sarrus", "inverse d'une matrice", "inverse matrice 2x2", "système linéaire matrice"],
  "figures": [
    { "nom": "produit_matrices", "alt": "Produit de deux matrices : la première ligne de A, multipliée terme à terme par la deuxième colonne de B, donne le coefficient c₁₂ de la matrice produit AB." }
  ],
  "chapitresLies": [
    "terminale/graphes-et-matrices"
  ],
  "faq": [
    ["Comment multiplier deux matrices ?", "Le coefficient de la ligne i et de la colonne j du produit AB s’obtient en multipliant terme à terme la ligne i de A par la colonne j de B, puis en additionnant. Le nombre de colonnes de A doit être égal au nombre de lignes de B."],
    ["Comment calculer le déterminant d’une matrice 2 × 2 ?", "Pour la matrice de première ligne (a, b) et de deuxième ligne (c, d), le déterminant vaut ad − bc."],
    ["Comment calculer l’inverse d’une matrice 2 × 2 ?", "Si ad − bc ≠ 0, on échange a et d, on change le signe de b et de c, puis on divise tout par ad − bc."],
    ["Quand une matrice est-elle inversible ?", "Une matrice carrée est inversible si et seulement si son déterminant est non nul."],
    ["Le produit de matrices est-il commutatif ?", "Non : en général AB ≠ BA. L’ordre des facteurs compte, et (AB)⁻¹ = B⁻¹A⁻¹."]
  ]
}
---
<!-- optitab:1 -->
## I. Opérations sur les matrices {Lycée}

Une matrice de taille $n \times p$ a $n$ lignes et $p$ colonnes ; on note $a_{ij}$ le coefficient de la ligne $i$ et de la colonne $j$.

[IMAGE_1]

::: formule Produit de $A$ ($n \times p$) par $B$ ($p \times q$)
$AB$ est de taille $n \times q$ et :
$$
\begin{aligned}
c_{ij} &= \sum_{k=1}^{p} a_{ik}\,b_{kj} \\
&= a_{i1}b_{1j} + a_{i2}b_{2j} + \dots + a_{ip}b_{pj}
\end{aligned}
$$
:::

::: exemple
$$\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} = \begin{pmatrix} 2 & 1 \\ 4 & 3 \end{pmatrix}$$
:::

| Propriété | Formule |
|---|---|
| Associativité | $(AB)C = A(BC)$ |
| Distributivité | $A(B + C) = AB + AC$ |
| Identité | $AI_n = I_n A = A$ |
| Transposée d’un produit | $(AB)^{\mathsf{T}} = B^{\mathsf{T}} A^{\mathsf{T}}$ |
| Inverse d’un produit | $(AB)^{-1} = B^{-1} A^{-1}$ |

::: attention Le produit n’est pas commutatif
En général $AB \neq BA$. Par exemple, $(A + B)^2 = A^2 + AB + BA + B^2$, et non $A^2 + 2AB + B^2$.
:::

## II. Matrices carrées d’ordre 2 {Lycée}

::: formule Déterminant et inverse d’une matrice $2 \times 2$
$$A = \begin{pmatrix} a & b \\ c & d \end{pmatrix} \qquad \det A = ad - bc$$
Si $\det A \neq 0$, $A$ est inversible et :
$$A^{-1} = \frac{1}{ad - bc}\begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$$
:::

::: exemple Inverse d’une matrice $2 \times 2$
Pour $A = \begin{pmatrix} 2 & 1 \\ 5 & 3 \end{pmatrix}$, $\det A = 2 \times 3 - 1 \times 5 = 1$, donc :
$$A^{-1} = \begin{pmatrix} 3 & -1 \\ -5 & 2 \end{pmatrix}$$
:::

::: propriete Polynôme caractéristique
Toute matrice $A$ de taille $2 \times 2$ vérifie :
$$A^2 - \operatorname{tr}(A)\,A + \det(A)\,I_2 = 0$$
où $\operatorname{tr}(A) = a + d$ est la trace.
:::

## III. Déterminant $3 \times 3$ {Supérieur}

::: formule Développement selon la première ligne
$$
\begin{aligned}
\begin{vmatrix} a & b & c \\ d & e & f \\ g & h & i \end{vmatrix} &= a(ei - fh) \\
&\quad - b(di - fg) \\
&\quad + c(dh - eg)
\end{aligned}
$$
:::

::: exemple
$$
\begin{aligned}
\begin{vmatrix} 1 & 2 & 0 \\ 0 & 1 & 3 \\ 2 & 0 & 1 \end{vmatrix} &= 1 \times (1 - 0) - 2 \times (0 - 6) + 0 \\
&= 13
\end{aligned}
$$
:::

| Propriété | Formule |
|---|---|
| Produit | $\det(AB) = \det A \times \det B$ |
| Transposée | $\det(A^{\mathsf{T}}) = \det A$ |
| Multiplication par $\lambda$ ($A$ de taille $n$) | $\det(\lambda A) = \lambda^n \det A$ |
| Inverse | $\det(A^{-1}) = \dfrac{1}{\det A}$ |
| Matrice triangulaire | produit des coefficients diagonaux |
| Échange de deux lignes | le déterminant change de signe |

::: retenir Inversibilité
Une matrice carrée $A$ est inversible si et seulement si $\det A \neq 0$.
:::

## IV. Systèmes linéaires {Lycée}

Le système s’écrit $AX = B$. Si $A$ est inversible, il a une unique solution :
$$X = A^{-1}B$$

::: exemple Résoudre $2x + y = 4$ et $5x + 3y = 11$
$A = \begin{pmatrix} 2 & 1 \\ 5 & 3 \end{pmatrix}$ a pour inverse $\begin{pmatrix} 3 & -1 \\ -5 & 2 \end{pmatrix}$, donc :
$$\begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 3 & -1 \\ -5 & 2 \end{pmatrix}\begin{pmatrix} 4 \\ 11 \end{pmatrix} = \begin{pmatrix} 1 \\ 2 \end{pmatrix}$$
:::

## V. Puissances, suites et graphes {Lycée}

| Situation | Formule |
|---|---|
| Matrice diagonale | $\begin{pmatrix} a & 0 \\ 0 & d \end{pmatrix}^n = \begin{pmatrix} a^n & 0 \\ 0 & d^n \end{pmatrix}$ |
| Diagonalisation $A = PDP^{-1}$ | $A^n = PD^nP^{-1}$ |
| Suite $U_{n+1} = AU_n$ | $U_n = A^n U_0$ |
| Chaîne de Markov $\pi_{n+1} = \pi_n P$ | $\pi_n = \pi_0 P^n$ |

::: propriete Graphes
Si $M$ est la matrice d’adjacence d’un graphe, le coefficient de la ligne $i$ et de la colonne $j$ de $M^n$ est le nombre de chemins de longueur $n$ allant du sommet $i$ au sommet $j$.
:::

## VI. Valeurs propres {Supérieur}

| Notion | Formule |
|---|---|
| Valeur propre $\lambda$ | $\det(A - \lambda I_n) = 0$ |
| Vecteur propre $X \neq 0$ | $AX = \lambda X$ |
| Trace | $\operatorname{tr}(AB) = \operatorname{tr}(BA)$ |
| Matrice $2 \times 2$ | $\lambda_1 + \lambda_2 = \operatorname{tr} A$ et $\lambda_1 \lambda_2 = \det A$ |
