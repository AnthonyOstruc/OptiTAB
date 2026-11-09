---
{
  "slug": "tableaux-de-signes-et-variations",
  "titre": "Tableaux de signes et de variations",
  "titreCourt": "Tableaux de signes et variations",
  "titreSeo": "Tableau de signes et tableau de variations : méthode et exemples",
  "description": "Construire un tableau de signes (ax + b, produit, quotient, trinôme) et un tableau de variations à partir de la dérivée, avec les fonctions de référence.",
  "chapo": "Comment dresser un tableau de signes, puis un tableau de variations à partir du signe de la dérivée : règles, exemples complets, fonctions de référence et ligne de convexité.",
  "resume": "Signe de ax + b, produit, quotient, dérivée",
  "vignette": "courbe_variations",
  "theme": "Analyse",
  "niveaux": ["Lycée"],
  "ordre": 8,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["tableau de signes", "tableau de variations", "faire un tableau de signe", "signe de ax+b", "tableau de signe produit", "tableau de signe quotient", "dérivée et variations", "étudier le signe d'une fonction"],
  "figures": [
    { "nom": "courbe_variations", "alt": "Courbe de f(x) = x³ − 3x : elle monte jusqu’au maximum local 2 en x = −1, descend jusqu’au minimum local −2 en x = 1, puis remonte ; les tangentes y sont horizontales." }
  ],
  "chapitresLies": [
    "seconde/etudier-les-variations-et-les-extremums-d-une-fonction",
    "premiere/derivation-variations-et-courbes-representatives",
    "premiere/equations-fonctions-polynomes-du-second-degre",
    "terminale/derivation-et-convexite"
  ],
  "faq": [
    ["Comment faire un tableau de signes ?", "On cherche les valeurs qui annulent chaque facteur, on les range dans l’ordre sur la première ligne, on écrit le signe de chaque facteur sur une ligne, puis on applique la règle des signes sur la dernière ligne."],
    ["Quel est le signe de ax + b ?", "ax + b s’annule en x = −b/a. Il est du signe de a à droite de cette valeur et du signe contraire à gauche."],
    ["Comment faire un tableau de variations ?", "On calcule la dérivée f′, on étudie son signe, puis on en déduit les variations : f est croissante là où f′ > 0 et décroissante là où f′ < 0. On complète avec les images des extremums et les limites."],
    ["Que signifie la double barre dans un tableau ?", "Elle indique une valeur interdite : la fonction n’est pas définie en ce point, par exemple x = 0 pour la fonction inverse."]
  ]
}
---
<!-- optitab:1 -->
## I. Signe de $ax + b$ {Lycée}

$ax + b$ s’annule en $x = -\dfrac{b}{a}$ : il est **du signe de $a$ à droite** de cette valeur, et du signe contraire à gauche.

Exemple avec $a > 0$ : signe de $2x - 6$, qui s’annule en $3$.

::: tableau
x : -\infty, 3, +\infty
2x - 6 : , -, z, +,
:::

Exemple avec $a < 0$ : signe de $-x + 4$, qui s’annule en $4$.

::: tableau
x : -\infty, 4, +\infty
-x + 4 : , +, z, -,
:::

## II. Produit et quotient {Lycée}

| Règle des signes | Résultat |
|---|---|
| $(+) \times (+)$ ou $(-) \times (-)$ | $+$ |
| $(+) \times (-)$ ou $(-) \times (+)$ | $-$ |

La même règle vaut pour un quotient.

::: methode Dresser un tableau de signes
1. Chercher la valeur qui annule chaque facteur.
2. Ranger ces valeurs dans l’ordre croissant sur la ligne des $x$.
3. Écrire une ligne de signes par facteur.
4. Conclure sur la dernière ligne avec la règle des signes.
:::

Signe du produit $P(x) = (x - 1)(x + 2)$ :

::: tableau
x : -\infty, -2, 1, +\infty
x + 2 : , -, z, +, t, +,
x - 1 : , -, t, -, z, +,
P(x) : , +, z, -, z, +,
:::

Donc $(x - 1)(x + 2) \leqslant 0$ pour $x \in [-2\,;1]$.

Signe du quotient $\dfrac{x - 1}{x + 2}$ : la valeur $-2$ est **interdite** (double barre).

::: tableau
x : -\infty, -2, 1, +\infty
x + 2 : , -, z, +, t, +,
x - 1 : , -, t, -, z, +,
\dfrac{x - 1}{x + 2} : , +, d, -, z, +,
:::

## III. Signe du trinôme $ax^2 + bx + c$ {Lycée}

| Discriminant | Signe |
|---|---|
| $\Delta > 0$ | signe de $a$ à l’extérieur des racines, signe contraire entre elles |
| $\Delta = 0$ | signe de $a$, nul en $x_0 = -\dfrac{b}{2a}$ |
| $\Delta < 0$ | signe de $a$ pour tout réel $x$ |

Exemple : $f(x) = 2x^2 - 2x - 12 = 2(x + 2)(x - 3)$, avec $a = 2 > 0$.

::: tableau
x : -\infty, -2, 3, +\infty
f(x) : , +, z, -, z, +,
:::

## IV. Tableau de variations {Lycée}

::: propriete Signe de la dérivée et variations
- Si $f' > 0$ sur un intervalle, $f$ y est **croissante**.
- Si $f' < 0$ sur un intervalle, $f$ y est **décroissante**.
- Si $f'$ s’annule en changeant de signe en $a$, $f$ admet un **extremum local** en $a$.
:::

::: exemple $f(x) = x^3 - 3x$ sur $\mathbb{R}$
$f'(x) = 3x^2 - 3 = 3(x - 1)(x + 1)$, qui s’annule en $-1$ et en $1$. On calcule $f(-1) = 2$ et $f(1) = -2$.
:::

::: tableau
x : -\infty, -1, 1, +\infty
f'(x) : , +, z, -, z, +,
f(x) : -/-\infty, +/2, -/-2, +/+\infty
:::

[IMAGE_1]

::: methode Les étapes
1. Domaine de définition de $f$.
2. Calcul de $f'(x)$, si possible sous forme factorisée.
3. Signe de $f'(x)$ dans un tableau de signes.
4. Flèches de variation, images des extremums et limites aux bornes.
:::

## V. Fonctions de référence {Lycée}

Fonction carré $x \mapsto x^2$ :

::: tableau
x : -\infty, 0, +\infty
x^2 : +/+\infty, -/0, +/+\infty
:::

Fonction inverse $x \mapsto \dfrac{1}{x}$ (non définie en $0$) :

::: tableau
x : -\infty, 0, +\infty
\dfrac{1}{x} : +/0, -D+/-\infty/+\infty, -/0
:::

Fonction racine carrée $x \mapsto \sqrt{x}$ :

::: tableau
x : 0, +\infty
\sqrt{x} : -/0, +/+\infty
:::

Fonction exponentielle :

::: tableau
x : -\infty, +\infty
\mathrm{e}^x : -/0, +/+\infty
:::

Fonction logarithme népérien :

::: tableau
x : 0, +\infty
\ln x : D-/-\infty, +/+\infty
:::

## VI. Ligne de convexité {Lycée}

Le signe de la dérivée seconde $f''$ donne la convexité : $f$ est **convexe** là où $f'' \geqslant 0$ et **concave** là où $f'' \leqslant 0$. Un changement de convexité est un **point d’inflexion**.

Pour $f(x) = x^3 - 3x$ : $f''(x) = 6x$.

::: tableau
x : -\infty, 0, +\infty
f''(x) : , -, z, +,
Convexité : , concave, t, convexe,
:::

Le point $(0\,;0)$ est un point d’inflexion de la courbe.
