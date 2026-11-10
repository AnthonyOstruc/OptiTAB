---
{
  "slug": "pgcd-ppcm",
  "titre": "PGCD et PPCM",
  "titreCourt": "PGCD et PPCM",
  "titreSeo": "PGCD et PPCM : méthodes de calcul, algorithme d’Euclide, exemples",
  "description": "Calculer le PGCD et le PPCM de deux nombres : liste des diviseurs, facteurs premiers, algorithme d’Euclide, relation PGCD × PPCM = a × b, exemples corrigés.",
  "chapo": "Les trois méthodes pour trouver le PGCD, le calcul du PPCM, un tableau d’exemples et les usages concrets : fraction irréductible, dénominateur commun, partages et rendez-vous.",
  "resume": "Diviseurs, facteurs premiers, Euclide, exemples",
  "vignette": "partage_carres",
  "theme": "Arithmétique",
  "niveaux": ["Collège", "Lycée"],
  "ordre": 4,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["PGCD", "PPCM", "calculer le PGCD", "calculer le PPCM", "algorithme d'Euclide", "PGCD et PPCM exemple", "plus grand commun diviseur", "plus petit commun multiple"],
  "figures": [
    { "nom": "partage_carres", "alt": "Un rectangle de 36 sur 24 découpé en 6 carrés identiques de côté 12 : 12 est le PGCD de 36 et de 24, le plus grand côté possible des carrés." },
    { "nom": "euclide_rectangle", "alt": "Algorithme d’Euclide en image : un rectangle de 21 sur 15 est découpé en un carré de côté 15, deux carrés de côté 6, puis deux carrés de côté 3 ; le dernier carré, de côté 3, donne le PGCD de 21 et 15." }
  ],
  "chapitresLies": [
    "cm2/multiples-et-diviseurs",
    "4e/fractions-et-nombres-premiers",
    "3e/arithmetique-et-nombres-premiers",
    "seconde/utiliser-les-notions-de-multiple-diviseur-et-de-nombre-premier",
    "terminale/arithmetique"
  ],
  "faq": [
    ["Comment calculer le PGCD de deux nombres ?", "Avec l’algorithme d’Euclide : on divise le plus grand par le plus petit, puis le diviseur par le reste, et ainsi de suite. Le PGCD est le dernier reste non nul. Pour 252 et 198, on trouve 18."],
    ["Comment calculer le PPCM de deux nombres ?", "On utilise PPCM(a ; b) = a × b ÷ PGCD(a ; b). Par exemple, PPCM(24 ; 36) = 24 × 36 ÷ 12 = 72. On peut aussi prendre chaque facteur premier avec son plus grand exposant."],
    ["Quelle est la différence entre PGCD et PPCM ?", "Le PGCD est le plus grand nombre qui divise les deux nombres ; le PPCM est le plus petit nombre non nul qui est un multiple des deux. Pour 24 et 36 : PGCD = 12 et PPCM = 72."],
    ["À quoi sert le PGCD ?", "À rendre une fraction irréductible (on divise numérateur et dénominateur par le PGCD) et à résoudre les problèmes de partage en parts égales les plus grandes possibles."],
    ["Que veut dire « premiers entre eux » ?", "Deux nombres sont premiers entre eux quand leur PGCD vaut 1 : leur seul diviseur commun positif est 1, comme 7 et 12."]
  ]
}
---
<!-- optitab:1 -->
## I. Définitions {Collège}

::: definition PGCD et PPCM de deux entiers $a$ et $b$ non nuls
- Le **PGCD** (plus grand commun diviseur) est le plus grand entier qui divise à la fois $a$ et $b$.
- Le **PPCM** (plus petit commun multiple) est le plus petit entier strictement positif qui est un multiple de $a$ et de $b$.
:::

[IMAGE_1]

::: exemple Les diviseurs de $24$ et de $36$
- Diviseurs de $24$ : $1$, $2$, $3$, $4$, $6$, $8$, $12$, $24$.
- Diviseurs de $36$ : $1$, $2$, $3$, $4$, $6$, $9$, $12$, $18$, $36$.

Le plus grand diviseur commun est $12$ : $\operatorname{PGCD}(24\,;36) = 12$.
:::

## II. Avec les facteurs premiers {Collège}

::: methode Décomposer, puis comparer les exposants
- **PGCD** : produit des facteurs premiers **communs**, chacun avec son **plus petit** exposant.
- **PPCM** : produit de **tous** les facteurs premiers, chacun avec son **plus grand** exposant.
:::

::: exemple PGCD et PPCM de $24$ et $36$
$24 = 2^3 \times 3$ et $36 = 2^2 \times 3^2$, donc :
$$\operatorname{PGCD}(24\,;36) = 2^2 \times 3 = 12$$
$$\operatorname{PPCM}(24\,;36) = 2^3 \times 3^2 = 72$$
:::

## III. Algorithme d’Euclide {Collège}

::: propriete Principe
Si $a = bq + r$ (division euclidienne de $a$ par $b$), alors $\operatorname{PGCD}(a\,;b) = \operatorname{PGCD}(b\,;r)$. On recommence jusqu’à obtenir un reste nul : **le PGCD est le dernier reste non nul**.
:::

Calcul de $\operatorname{PGCD}(252\,;198)$ :

| Division euclidienne | Reste |
|---|---|
| $252 = 1 \times 198 + 54$ | $54$ |
| $198 = 3 \times 54 + 36$ | $36$ |
| $54 = 1 \times 36 + 18$ | $18$ |
| $36 = 2 \times 18 + 0$ | $0$ |

Le dernier reste non nul est $18$ : $\operatorname{PGCD}(252\,;198) = 18$.

[IMAGE_2]

::: conseil Algorithme des différences
On peut aussi remplacer le plus grand nombre par la différence des deux : $\operatorname{PGCD}(a\,;b) = \operatorname{PGCD}(b\,;a - b)$ si $a > b$. C’est plus long, mais sans division.
:::

## IV. Calculer le PPCM {Collège}

::: formule Relation entre PGCD et PPCM
$$\operatorname{PGCD}(a\,;b) \times \operatorname{PPCM}(a\,;b) = a \times b$$
:::

::: exemple
$\operatorname{PPCM}(252\,;198) = \dfrac{252 \times 198}{18} = 2\,772$.
:::

| $a$ | $b$ | PGCD | PPCM |
|---|---|---|---|
| $8$ | $12$ | $4$ | $24$ |
| $12$ | $18$ | $6$ | $36$ |
| $15$ | $25$ | $5$ | $75$ |
| $14$ | $21$ | $7$ | $42$ |
| $24$ | $36$ | $12$ | $72$ |
| $30$ | $45$ | $15$ | $90$ |
| $36$ | $48$ | $12$ | $144$ |
| $42$ | $56$ | $14$ | $168$ |
| $60$ | $84$ | $12$ | $420$ |
| $7$ | $12$ | $1$ | $84$ |

## V. À quoi ça sert ? {Collège}

| Problème | Outil |
|---|---|
| Rendre une fraction irréductible | on divise par le PGCD |
| Additionner des fractions | dénominateur commun : le PPCM |
| Partager en parts égales les plus grandes possibles | PGCD |
| Trouver quand deux cycles coïncident à nouveau | PPCM |

::: exemple Fraction irréductible
$\operatorname{PGCD}(252\,;198) = 18$, donc $\dfrac{252}{198} = \dfrac{252 \div 18}{198 \div 18} = \dfrac{14}{11}$.
:::

::: exemple Dénominateur commun
$\operatorname{PPCM}(24\,;36) = 72$, donc $\dfrac{1}{24} + \dfrac{1}{36} = \dfrac{3}{72} + \dfrac{2}{72} = \dfrac{5}{72}$.
:::

::: exemple Partage : $252$ roses et $198$ tulipes
Pour faire le plus grand nombre de bouquets identiques en utilisant toutes les fleurs, on calcule $\operatorname{PGCD}(252\,;198) = 18$ : $18$ bouquets de $14$ roses et $11$ tulipes.
:::

::: exemple Rendez-vous : deux bus partent ensemble
Un bus passe toutes les $24$ minutes, un autre toutes les $36$ minutes. Ils repartent ensemble au bout de $\operatorname{PPCM}(24\,;36) = 72$ minutes.
:::

## VI. Nombres premiers entre eux {Lycée}

::: definition Premiers entre eux
$a$ et $b$ sont **premiers entre eux** si $\operatorname{PGCD}(a\,;b) = 1$. Leur PPCM est alors $a \times b$.
:::

| Propriété | Énoncé |
|---|---|
| Multiplication | $\operatorname{PGCD}(ka\,;kb) = k \times \operatorname{PGCD}(a\,;b)$ pour $k > 0$ |
| Diviseur | si $a$ divise $b$, alors $\operatorname{PGCD}(a\,;b) = a$ |
| Théorème de Bézout | $a$ et $b$ premiers entre eux $\iff$ il existe $u$, $v$ entiers avec $au + bv = 1$ |
| Théorème de Gauss | si $a$ divise $bc$ et $\operatorname{PGCD}(a\,;b) = 1$, alors $a$ divise $c$ |

::: exemple Bézout pour $7$ et $12$
$7 \times (-5) + 12 \times 3 = -35 + 36 = 1$ : $7$ et $12$ sont premiers entre eux.
:::
