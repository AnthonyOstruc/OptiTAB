---
{
  "slug": "arrondir-un-nombre",
  "titre": "Arrondir un nombre : à l’unité, au dixième, au centième",
  "titreCourt": "Arrondir un nombre",
  "titreSeo": "Arrondir un nombre au dixième, au centième : règle et calculateur",
  "description": "Comment arrondir un nombre à l’unité, au dixième ou au centième : la règle, des exemples, troncature et encadrement, avec un calculateur d’arrondi gratuit.",
  "chapo": "La règle pour arrondir un nombre, expliquée avec une droite graduée et des exemples, la différence entre arrondi et troncature, les encadrements, et un calculateur pour vérifier.",
  "resume": "Règle, troncature, encadrement",
  "vignette": "carte_arrondi",
  "theme": "Arrondis",
  "niveaux": ["Primaire", "Collège"],
  "ordre": 5,
  "outil": "arrondi",
  "publie": "2026-11-16",
  "modifie": "2026-11-16",
  "motsCles": ["arrondir un nombre", "arrondi au dixième", "arrondi au centième", "arrondir à l’unité", "arrondi au millième", "troncature", "valeur approchée", "calculateur d’arrondi"],
  "figures": [
    { "nom": "arrondi_droite", "alt": "Droite graduée de 3,14 à 3,15 avec un point à 3,14159, placé avant le milieu : il est plus proche de 3,14." },
    { "nom": "carte_arrondi", "alt": "Aperçu : 3,14159 placé sur une droite graduée entre 3,14 et 3,15, plus proche de 3,14.", "carte": true }
  ],
  "chapitresLies": [
    "cm1/comparer-encadrer-et-arrondir-les-decimaux",
    "6e/reperer-comparer-et-arrondir"
  ],
  "faq": [
    ["Comment arrondir un nombre ?", "On repère le chiffre du rang demandé, puis on regarde le chiffre juste à sa droite. S’il vaut 0, 1, 2, 3 ou 4, on garde le chiffre ; s’il vaut 5, 6, 7, 8 ou 9, on l’augmente de 1. On supprime ensuite les chiffres suivants."],
    ["Comment arrondir au dixième ?", "On garde un seul chiffre après la virgule, en regardant le deuxième : 3,14159 arrondi au dixième donne 3,1 (le chiffre suivant est 4), et 7,96 donne 8,0 (le chiffre suivant est 6)."],
    ["Comment arrondir au centième ?", "On garde deux chiffres après la virgule, en regardant le troisième : 3,14159 arrondi au centième donne 3,14, et 2,675 donne 2,68."],
    ["Quelle est la différence entre arrondi et troncature ?", "La troncature coupe simplement les chiffres en trop ; l’arrondi choisit la valeur la plus proche. 2,68 tronqué au dixième donne 2,6, mais arrondi au dixième il donne 2,7."],
    ["Faut-il arrondir 2,5 à 2 ou à 3 ?", "À l’école, on arrondit 2,5 à l’unité à 3 : quand le chiffre suivant est 5, on arrondit au-dessus."]
  ]
}
---
<!-- optitab:1 -->
[OUTIL]

## I. La règle de l’arrondi {Primaire}

Arrondir un nombre, c’est le remplacer par **la valeur la plus proche** au rang demandé.

[IMAGE_1]

::: retenir La règle
On regarde le chiffre **juste après** le rang demandé :
- s’il vaut $0$, $1$, $2$, $3$ ou $4$, on garde le chiffre du rang ;
- s’il vaut $5$, $6$, $7$, $8$ ou $9$, on ajoute $1$ au chiffre du rang.

Puis on supprime tous les chiffres suivants.
:::

## II. Des exemples à chaque rang {Primaire}

| Nombre | Arrondi à | Chiffre suivant | Résultat |
|---|---|---|---|
| $3{,}14159$ | l’unité | $1$ | $3$ |
| $3{,}14159$ | au dixième | $4$ | $3{,}1$ |
| $3{,}14159$ | au centième | $1$ | $3{,}14$ |
| $2{,}675$ | au centième | $5$ | $2{,}68$ |
| $7{,}96$ | au dixième | $6$ | $8{,}0$ |
| $1\,247$ | à la centaine | $4$ | $1\,200$ |
| $1\,250$ | à la centaine | $5$ | $1\,300$ |

::: attention Garder le zéro
$7{,}96$ arrondi au dixième s’écrit $8{,}0$ : le zéro montre que la précision est le dixième.
:::

## III. Arrondi ou troncature ? {Collège}

La **troncature** coupe les chiffres en trop sans regarder le suivant. L’arrondi, lui, choisit la valeur la plus proche.

| Nombre | Troncature au dixième | Arrondi au dixième |
|---|---|---|
| $2{,}64$ | $2{,}6$ | $2{,}6$ |
| $2{,}68$ | $2{,}6$ | $2{,}7$ |

## IV. Encadrer un nombre {Primaire}

Encadrer, c’est donner deux valeurs entre lesquelles le nombre se trouve. Au centième : $3{,}14 < 3{,}14159 < 3{,}15$.

- $3{,}14$ est la valeur approchée **par défaut** (en dessous) ;
- $3{,}15$ est la valeur approchée **par excès** (au-dessus) ;
- l’arrondi est celle des deux qui est la plus proche : ici $3{,}14$.

## V. L’erreur des arrondis en cascade {Collège}

::: attention Erreur fréquente
Arrondir plusieurs fois de suite. Pour $2{,}346$ au dixième, on regarde directement le chiffre des centièmes, $4$ : le résultat est $2{,}3$. Passer par $2{,}35$ puis arrondir à $2{,}4$ est faux.
:::

::: conseil Dans un calcul
On garde tous les chiffres pendant le calcul et on n’arrondit **qu’à la fin**, au rang demandé par l’énoncé.
:::
