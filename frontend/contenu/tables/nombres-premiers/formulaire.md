---
{
  "slug": "nombres-premiers",
  "titre": "Nombres premiers et critères de divisibilité",
  "titreCourt": "Nombres premiers",
  "titreSeo": "Liste des nombres premiers jusqu’à 1 000 et critères de divisibilité",
  "description": "La liste des nombres premiers jusqu’à 1 000, le crible d’Ératosthène, les critères de divisibilité et la décomposition en facteurs premiers.",
  "chapo": "Les 168 nombres premiers inférieurs à 1 000, le crible de 1 à 100, les critères de divisibilité à connaître et la décomposition en facteurs premiers, avec le PGCD et le PPCM.",
  "resume": "Liste jusqu’à 1 000, critères de divisibilité",
  "vignette": "crible_100",
  "theme": "Nombres",
  "niveaux": [
    "Primaire",
    "Collège",
    "Lycée"
  ],
  "ordre": 5,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": [
    "nombres premiers",
    "liste des nombres premiers",
    "nombres premiers jusqu'à 100",
    "nombres premiers jusqu'à 1000",
    "critères de divisibilité",
    "décomposition en facteurs premiers",
    "crible d'Ératosthène",
    "PGCD PPCM"
  ],
  "figures": [
    {
      "nom": "crible_100",
      "alt": "Crible d’Ératosthène de 1 à 100 : les 25 nombres premiers 2, 3, 5, 7, 11, … 97 sont surlignés en vert."
    }
  ],
  "chapitresLies": [
    "cm2/multiples-et-diviseurs",
    "5e/multiples-diviseurs-et-partages",
    "4e/fractions-et-nombres-premiers",
    "3e/arithmetique-et-nombres-premiers",
    "seconde/utiliser-les-notions-de-multiple-diviseur-et-de-nombre-premier",
    "terminale/arithmetique"
  ],
  "faq": [
    [
      "Le nombre 1 est-il premier ?",
      "Non. Un nombre premier a exactement deux diviseurs distincts : 1 et lui-même. Le nombre 1 n’a qu’un seul diviseur, il n’est donc pas premier."
    ],
    [
      "Combien y a-t-il de nombres premiers inférieurs à 100 ?",
      "Il y en a 25 : 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89 et 97. Il y en a 168 inférieurs à 1 000."
    ],
    [
      "Comment savoir si un nombre est premier ?",
      "On essaie de le diviser par les nombres premiers 2, 3, 5, 7, 11… jusqu’à sa racine carrée. Si aucune division ne tombe juste, le nombre est premier. Par exemple, pour 97, il suffit de tester 2, 3, 5 et 7, car 11 × 11 = 121 > 97."
    ],
    [
      "Existe-t-il un plus grand nombre premier ?",
      "Non : il y a une infinité de nombres premiers, comme l’a démontré Euclide il y a plus de 2 000 ans."
    ]
  ]
}
---
<!-- optitab:1 -->
## I. Définition {Primaire}

::: definition Nombre premier
Un nombre entier est **premier** s’il a exactement deux diviseurs : $1$ et lui-même. Par exemple, $7$ est premier (diviseurs $1$ et $7$), mais $9$ ne l’est pas ($9 = 3 \times 3$).
:::

::: attention
$1$ n’est **pas** un nombre premier : il n’a qu’un seul diviseur. Le nombre $2$ est le **seul** nombre premier pair.
:::

## II. Les nombres premiers de 1 à 100 {Primaire}

[IMAGE_1]

Il y a **25** nombres premiers inférieurs à $100$ : 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97.

::: methode Le crible d’Ératosthène
On barre $1$, puis on garde $2$ et on barre tous ses multiples ; on garde $3$ et on barre ses multiples ; et ainsi de suite avec $5$ et $7$. Les nombres qui restent sont les nombres premiers.
:::

## III. Liste des nombres premiers jusqu’à 1 000 {Collège}

| Tranche | Nombres premiers |
|---|---|
| De 1 à 100 (25 nombres) | 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97 |
| De 101 à 200 (21 nombres) | 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199 |
| De 201 à 300 (16 nombres) | 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293 |
| De 301 à 400 (16 nombres) | 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397 |
| De 401 à 500 (17 nombres) | 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499 |
| De 501 à 600 (14 nombres) | 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599 |
| De 601 à 700 (16 nombres) | 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691 |
| De 701 à 800 (14 nombres) | 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797 |
| De 801 à 900 (15 nombres) | 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887 |
| De 901 à 1 000 (14 nombres) | 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997 |

Au total, il y a **168** nombres premiers inférieurs à $1\,000$.

## IV. Critères de divisibilité {Primaire}

| Divisible | Critère et exemple |
|---|---|
| Par 2 | si le chiffre des unités est pair (0, 2, 4, 6, 8). Exemple : $1\,358$ |
| Par 3 | si la somme des chiffres est divisible par 3. Exemple : $231$ : $2 + 3 + 1 = 6$ |
| Par 4 | si le nombre formé par les deux derniers chiffres est divisible par 4. Exemple : $1\,524$ : $24$ |
| Par 5 | si le chiffre des unités est 0 ou 5. Exemple : $745$ |
| Par 6 | si il est divisible par 2 et par 3. Exemple : $522$ |
| Par 8 | si le nombre formé par les trois derniers chiffres est divisible par 8. Exemple : $7\,120$ : $120$ |
| Par 9 | si la somme des chiffres est divisible par 9. Exemple : $4\,527$ : $4 + 5 + 2 + 7 = 18$ |
| Par 10 | si le chiffre des unités est 0. Exemple : $3\,470$ |
| Par 11 | si la différence entre la somme des chiffres de rang impair et celle des chiffres de rang pair est divisible par 11. Exemple : $9\,174$ : $(9 + 7) - (1 + 4) = 11$ |
| Par 25 | si le nombre formé par les deux derniers chiffres est 00, 25, 50 ou 75. Exemple : $1\,275$ |

## V. Décomposition en facteurs premiers {Collège}

Tout entier supérieur ou égal à $2$ s’écrit, de façon unique, comme un produit de nombres premiers.

| Nombre | Décomposition |
|---|---|
| $12$ | $2^{2} \times 3$ |
| $18$ | $2 \times 3^{2}$ |
| $36$ | $2^{2} \times 3^{2}$ |
| $60$ | $2^{2} \times 3 \times 5$ |
| $84$ | $2^{2} \times 3 \times 7$ |
| $100$ | $2^{2} \times 5^{2}$ |
| $360$ | $2^{3} \times 3^{2} \times 5$ |
| $1\,001$ | $7 \times 11 \times 13$ |
| $2\,026$ | $2 \times 1\,013$ |

::: methode Décomposer un nombre
On divise successivement par le plus petit nombre premier possible : $360 \div 2 = 180$, $180 \div 2 = 90$, $90 \div 2 = 45$, $45 \div 3 = 15$, $15 \div 3 = 5$. Donc $360 = 2^3 \times 3^2 \times 5$.
:::

## VI. PGCD et PPCM {Collège}

| Notion | Méthode avec les décompositions |
|---|---|
| PGCD (plus grand commun diviseur) | produit des facteurs communs, avec le **plus petit** exposant |
| PPCM (plus petit commun multiple) | produit de tous les facteurs, avec le **plus grand** exposant |
| Relation | $\mathrm{PGCD}(a, b) \times \mathrm{PPCM}(a, b) = a \times b$ |

::: exemple PGCD et PPCM de 60 et 84
$60 = 2^{2} \times 3 \times 5$ et $84 = 2^{2} \times 3 \times 7$, donc $\mathrm{PGCD} = 2^{2} \times 3 = 12$ et $\mathrm{PPCM} = 2^{2} \times 3 \times 5 \times 7 = 420$.
:::
