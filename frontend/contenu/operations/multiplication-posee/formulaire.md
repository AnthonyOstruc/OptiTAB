---
{
  "slug": "multiplication-posee",
  "titre": "Multiplication posée : comment poser une multiplication",
  "titreCourt": "Multiplication posée",
  "titreSeo": "Multiplication posée : par 1, 2 ou 3 chiffres, et per jalousie",
  "description": "Comment poser une multiplication : par un, deux ou trois chiffres, avec les retenues, les nombres décimaux et la méthode par jalousie, avec schémas.",
  "chapo": "La méthode pour poser une multiplication à la main, expliquée ligne par ligne avec des schémas : par un chiffre avec les retenues, par deux et trois chiffres avec le décalage, avec des nombres décimaux, puis la méthode par jalousie.",
  "resume": "Retenues, décalage, virgule, jalousie",
  "vignette": "carte_multiplication",
  "theme": "Multiplication",
  "niveaux": ["Primaire", "Collège"],
  "ordre": 3,
  "publie": "2026-11-16",
  "modifie": "2026-11-16",
  "liees": ["fiches/multiplications-posees-ce2", "fiches/multiplications-posees-cm1"],
  "motsCles": ["multiplication posée", "poser une multiplication", "multiplication à deux chiffres", "multiplication à trois chiffres", "multiplication avec retenue", "multiplication de nombres décimaux", "multiplication per jalousie", "multiplication par jalousie"],
  "figures": [
    { "nom": "multiplication_un_chiffre", "alt": "Multiplication posée de 347 par 6 : les retenues 4 et 2 sont écrites en petit au-dessus des chiffres 4 et 3 ; le résultat est 2 082." },
    { "nom": "multiplication_deux_chiffres", "alt": "Multiplication posée de 347 par 26 : première ligne 2 082 pour 347 × 6, deuxième ligne 6 940 pour 347 × 20, avec un zéro gris de décalage ; la somme des deux lignes donne 9 022." },
    { "nom": "multiplication_trois_chiffres", "alt": "Multiplication posée de 425 par 132 : trois lignes 850, 12 750 et 42 500, décalées d’un puis de deux zéros gris ; leur somme donne 56 100." },
    { "nom": "multiplication_decimaux", "alt": "Multiplication posée de 4,25 par 3,6 alignée à droite sans tenir compte des virgules ; 4,25 a 2 chiffres après la virgule et 3,6 en a 1 ; le produit 15,300 a donc 3 chiffres après la virgule." },
    { "nom": "multiplication_jalousie", "alt": "Multiplication par jalousie de 347 par 26 : une grille de 3 colonnes et 2 lignes, chaque case coupée par une diagonale contient un produit, par exemple 1 et 4 pour 7 × 2 ; on additionne le long des diagonales et on lit 9 022 à gauche puis en bas." },
    { "nom": "carte_multiplication", "alt": "Aperçu : multiplication posée de 347 par 26, lignes 2 082 et 6 940, résultat 9 022.", "carte": true }
  ],
  "chapitresLies": [
    "ce2/multiplier-en-colonnes-par-un-chiffre",
    "ce2/multiplier-en-colonnes-par-deux-chiffres",
    "cm1/multiplier-des-entiers",
    "cm2/calculer-avec-les-nombres-decimaux",
    "6e/calculer-avec-les-decimaux"
  ],
  "faq": [
    ["Comment poser une multiplication à deux chiffres ?", "On écrit le plus long nombre en haut et le plus court en dessous, alignés à droite. On multiplie d’abord le nombre du haut par le chiffre des unités, puis par le chiffre des dizaines sur une deuxième ligne décalée d’un rang (on écrit un 0 à droite). On additionne enfin les deux lignes."],
    ["Pourquoi met-on un zéro dans une multiplication posée ?", "Parce que le chiffre des dizaines vaut dix fois plus : dans 347 × 26, le 2 vaut 20. On calcule donc 347 × 20, qui est 347 × 2 multiplié par 10 : le zéro décale le résultat d’un rang vers la gauche."],
    ["Où écrit-on les retenues dans une multiplication ?", "En petit, au-dessus du chiffre suivant du nombre du haut. On les ajoute au produit suivant, puis on les efface ou on les barre avant de multiplier par le chiffre suivant du nombre du bas, pour ne pas les confondre."],
    ["Comment poser une multiplication avec des virgules ?", "On pose la multiplication sans tenir compte des virgules, en alignant les nombres à droite. On compte ensuite le nombre total de chiffres après la virgule dans les deux facteurs, et on place la virgule du résultat pour qu’il ait autant de chiffres après la virgule."],
    ["Qu’est-ce que la multiplication par jalousie ?", "C’est une méthode ancienne, aussi appelée per gelosia. On écrit les produits de chaque paire de chiffres dans une grille coupée en diagonales, puis on additionne le long des diagonales. Elle évite de garder les retenues en tête pendant les multiplications."],
    ["Comment vérifier une multiplication ?", "On calcule un ordre de grandeur en arrondissant les facteurs : 347 × 26 est proche de 350 × 25 = 8 750. Le résultat 9 022 est vraisemblable ; 90 220 ou 902 ne le seraient pas."]
  ]
}
---
<!-- optitab:1 -->
## I. Multiplier par un nombre à un chiffre {Primaire}

On écrit le plus long nombre en haut et le multiplicateur en dessous, **alignés à droite**. On multiplie chaque chiffre du haut, en commençant par les unités.

[IMAGE_1]

| Chiffre | Calcul | On écrit | On retient |
|---|---|---|---|
| Unités | $7 \times 6 = 42$ | $2$ | $4$ |
| Dizaines | $4 \times 6 + 4 = 28$ | $8$ | $2$ |
| Centaines | $3 \times 6 + 2 = 20$ | $20$ | rien |

Donc $347 \times 6 = 2\,082$.

::: attention Erreur fréquente
Ajouter la retenue **avant** de multiplier : $(4 + 4) \times 6 = 48$ au lieu de $4 \times 6 + 4 = 28$. On multiplie d’abord, puis on ajoute la retenue.
:::

## II. Multiplier par un nombre à deux chiffres {Primaire}

[IMAGE_2]

On décompose le multiplicateur : $26 = 6 + 20$. On fait donc deux multiplications, une par ligne, puis on les additionne.

::: methode $347 \times 26$
1. **Première ligne** : $347 \times 6 = 2\,082$.
2. **Deuxième ligne** : $347 \times 20$. On écrit d’abord un **$0$** dans la colonne des unités, puis on multiplie par $2$ : $347 \times 2 = 694$. La ligne se lit $6\,940$.
3. **Addition** : $2\,082 + 6\,940 = 9\,022$.
:::

::: retenir Le zéro de décalage
Le $2$ de $26$ vaut $2$ **dizaines**. Multiplier par $20$, c’est multiplier par $2$ puis par $10$ : le zéro décale la ligne d’un rang vers la gauche. Certains manuels le remplacent par un point ou une case vide.
:::

::: attention Erreur fréquente
Oublier le zéro de décalage : on trouverait $2\,082 + 694 = 2\,776$, bien trop petit. L’ordre de grandeur, $350 \times 25 = 8\,750$, montre tout de suite l’erreur.
:::

## III. Multiplier par un nombre à trois chiffres {Primaire}

[IMAGE_3]

Même principe, avec une ligne par chiffre du multiplicateur : $132 = 2 + 30 + 100$.

- $425 \times 2 = 850$ ;
- $425 \times 30 = 12\,750$ (un zéro de décalage) ;
- $425 \times 100 = 42\,500$ (deux zéros de décalage).

On additionne les trois lignes : $850 + 12\,750 + 42\,500 = 56\,100$.

::: conseil Choisir le nombre du bas
On place en bas le nombre qui a **le moins de chiffres** (ou des chiffres faciles comme $0$ ou $1$) : il y a moins de lignes à calculer, donc moins de risques d’erreur.
:::

## IV. Multiplier des nombres décimaux {Collège}

[IMAGE_4]

On pose la multiplication **sans tenir compte des virgules**, en alignant les nombres à droite, et on calcule $425 \times 36 = 15\,300$.

On place ensuite la virgule : $4{,}25$ a **$2$** chiffres après la virgule et $3{,}6$ en a **$1$**. Le produit en a donc $2 + 1 = 3$ : $4{,}25 \times 3{,}6 = 15{,}300 = 15{,}3$.

::: retenir La virgule du produit
Le nombre de chiffres après la virgule du produit est **la somme** des nombres de chiffres après la virgule des deux facteurs.
:::

::: attention Erreur fréquente
Aligner les virgules comme pour une addition. En multiplication, on aligne les nombres **à droite** et on ne place la virgule qu’à la fin.
:::

## V. Une autre méthode : la multiplication par jalousie

[IMAGE_5]

Cette méthode très ancienne, aussi appelée **per gelosia**, sépare les multiplications et les additions. Pour $347 \times 26$ :

1. On trace une grille de $3$ colonnes (pour $3$, $4$, $7$) et $2$ lignes (pour $2$ et $6$), et on coupe chaque case par une diagonale.
2. Dans chaque case, on écrit le produit des deux chiffres : les **dizaines** au-dessus de la diagonale, les **unités** en dessous. Par exemple $7 \times 2 = 14$.
3. On additionne les chiffres **le long de chaque diagonale**, en partant d’en bas à droite, et on reporte les retenues sur la diagonale suivante :

| Diagonale | Calcul | On écrit | On retient |
|---|---|---|---|
| 1re | $2$ | $2$ | rien |
| 2e | $4 + 4 + 4 = 12$ | $2$ | $1$ |
| 3e | $8 + 8 + 2 + 1 + 1 = 20$ | $0$ | $2$ |
| 4e | $6 + 1 + 0 + 2 = 9$ | $9$ | rien |
| 5e | $0$ | $0$ | rien |

On lit le résultat de haut en bas, puis de gauche à droite : $347 \times 26 = 9\,022$, comme avec la méthode habituelle.

## VI. Vérifier une multiplication {Primaire}

::: methode L’ordre de grandeur
On arrondit les facteurs pour calculer de tête : $347 \times 26 \approx 350 \times 25 = 8\,750$. Le résultat $9\,022$ est vraisemblable.
:::

On peut aussi changer l’ordre des facteurs, puisque $347 \times 26 = 26 \times 347$, et refaire le calcul : on doit trouver le même produit.
