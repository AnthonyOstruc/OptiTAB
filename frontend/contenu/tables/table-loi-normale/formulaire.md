---
{
  "slug": "table-loi-normale",
  "titre": "Table de la loi normale centrée réduite",
  "titreCourt": "Table de la loi normale",
  "titreSeo": "Table de la loi normale centrée réduite : valeurs de Φ(z)",
  "description": "La table de la loi normale centrée réduite N(0 ; 1) : valeurs de Φ(z) de 0 à 3,99, quantiles usuels (1,645 ; 1,96 ; 2,576) et méthode de lecture.",
  "chapo": "Toutes les valeurs de la fonction de répartition Φ(z) = P(Z ≤ z) de la loi normale centrée réduite, les quantiles à connaître et la méthode pour lire la table.",
  "resume": "Valeurs de Φ(z), quantiles, méthode de lecture",
  "vignette": "aire_phi",
  "theme": "Probabilités et statistiques",
  "niveaux": [
    "Lycée",
    "Supérieur"
  ],
  "ordre": 4,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": [
    "table loi normale",
    "table de la loi normale centrée réduite",
    "table N(0,1)",
    "fonction de répartition loi normale",
    "table de Gauss",
    "quantile loi normale",
    "1,96 loi normale",
    "Φ(z)"
  ],
  "figures": [
    {
      "nom": "aire_phi",
      "alt": "Courbe en cloche de la loi normale centrée réduite : l’aire colorée à gauche de z = 1,2 vaut Φ(1,2) ≈ 0,8849, et l’aire à droite vaut 1 − Φ(1,2)."
    },
    {
      "nom": "symetrie",
      "alt": "Courbe en cloche symétrique : l’aire à gauche de −z est égale à l’aire à droite de z."
    }
  ],
  "chapitresLies": [
    "terminale/concentration-loi-des-grands-nombres",
    "terminale/sommes-de-variables-aleatoires"
  ],
  "faq": [
    [
      "Comment lire la table de la loi normale ?",
      "Pour z = 1,23, on cherche la ligne 1,2 et la colonne 0,03 : la case donne Φ(1,23) = P(Z ≤ 1,23) ≈ 0,8907. La table ne donne que des z positifs : pour un z négatif, on utilise Φ(−z) = 1 − Φ(z)."
    ],
    [
      "Que vaut Φ(1,96) ?",
      "Φ(1,96) ≈ 0,9750. On en déduit P(−1,96 ≤ Z ≤ 1,96) = 2 × 0,975 − 1 = 0,95 : c’est l’origine du nombre 1,96 dans les intervalles à 95 %."
    ],
    [
      "Comment utiliser la table pour une loi normale N(μ ; σ²) ?",
      "On centre et on réduit : si X suit N(μ ; σ²), alors Z = (X − μ)/σ suit N(0 ; 1). Par exemple, pour X de moyenne 100 et d’écart type 15, P(X ≤ 130) = P(Z ≤ 2) = Φ(2) ≈ 0,9772."
    ],
    [
      "Pourquoi la table s’arrête-t-elle vers 4 ?",
      "Dès z = 3,9, Φ(z) dépasse 0,99995 : il vaut 1,0000 à quatre décimales près. Au-delà, la table n’apporte plus d’information."
    ]
  ]
}
---
<!-- optitab:1 -->
## I. Lire la table {Lycée}

[IMAGE_1]

La table donne $\Phi(z) = P(Z \leqslant z)$ pour $Z$ de loi normale $\mathcal{N}(0\,;1)$ : l’aire sous la courbe à gauche de $z$.

::: methode Trouver $\Phi(1{,}23)$
On prend la ligne $1{,}2$ (unités et dixième) et la colonne $0{,}03$ (centième) : $\Phi(1{,}23) \approx 0{,}8907$.
:::

## II. Valeurs de Φ(z) pour z de 0 à 3,99 {Lycée}

**Colonnes 0,00 à 0,04**

| z | 0,00 | 0,01 | 0,02 | 0,03 | 0,04 |
|---|---|---|---|---|---|
| 0,0 | 0,5000 | 0,5040 | 0,5080 | 0,5120 | 0,5160 |
| 0,1 | 0,5398 | 0,5438 | 0,5478 | 0,5517 | 0,5557 |
| 0,2 | 0,5793 | 0,5832 | 0,5871 | 0,5910 | 0,5948 |
| 0,3 | 0,6179 | 0,6217 | 0,6255 | 0,6293 | 0,6331 |
| 0,4 | 0,6554 | 0,6591 | 0,6628 | 0,6664 | 0,6700 |
| 0,5 | 0,6915 | 0,6950 | 0,6985 | 0,7019 | 0,7054 |
| 0,6 | 0,7257 | 0,7291 | 0,7324 | 0,7357 | 0,7389 |
| 0,7 | 0,7580 | 0,7611 | 0,7642 | 0,7673 | 0,7704 |
| 0,8 | 0,7881 | 0,7910 | 0,7939 | 0,7967 | 0,7995 |
| 0,9 | 0,8159 | 0,8186 | 0,8212 | 0,8238 | 0,8264 |
| 1,0 | 0,8413 | 0,8438 | 0,8461 | 0,8485 | 0,8508 |
| 1,1 | 0,8643 | 0,8665 | 0,8686 | 0,8708 | 0,8729 |
| 1,2 | 0,8849 | 0,8869 | 0,8888 | 0,8907 | 0,8925 |
| 1,3 | 0,9032 | 0,9049 | 0,9066 | 0,9082 | 0,9099 |
| 1,4 | 0,9192 | 0,9207 | 0,9222 | 0,9236 | 0,9251 |
| 1,5 | 0,9332 | 0,9345 | 0,9357 | 0,9370 | 0,9382 |
| 1,6 | 0,9452 | 0,9463 | 0,9474 | 0,9484 | 0,9495 |
| 1,7 | 0,9554 | 0,9564 | 0,9573 | 0,9582 | 0,9591 |
| 1,8 | 0,9641 | 0,9649 | 0,9656 | 0,9664 | 0,9671 |
| 1,9 | 0,9713 | 0,9719 | 0,9726 | 0,9732 | 0,9738 |
| 2,0 | 0,9772 | 0,9778 | 0,9783 | 0,9788 | 0,9793 |
| 2,1 | 0,9821 | 0,9826 | 0,9830 | 0,9834 | 0,9838 |
| 2,2 | 0,9861 | 0,9864 | 0,9868 | 0,9871 | 0,9875 |
| 2,3 | 0,9893 | 0,9896 | 0,9898 | 0,9901 | 0,9904 |
| 2,4 | 0,9918 | 0,9920 | 0,9922 | 0,9925 | 0,9927 |
| 2,5 | 0,9938 | 0,9940 | 0,9941 | 0,9943 | 0,9945 |
| 2,6 | 0,9953 | 0,9955 | 0,9956 | 0,9957 | 0,9959 |
| 2,7 | 0,9965 | 0,9966 | 0,9967 | 0,9968 | 0,9969 |
| 2,8 | 0,9974 | 0,9975 | 0,9976 | 0,9977 | 0,9977 |
| 2,9 | 0,9981 | 0,9982 | 0,9982 | 0,9983 | 0,9984 |
| 3,0 | 0,9987 | 0,9987 | 0,9987 | 0,9988 | 0,9988 |
| 3,1 | 0,9990 | 0,9991 | 0,9991 | 0,9991 | 0,9992 |
| 3,2 | 0,9993 | 0,9993 | 0,9994 | 0,9994 | 0,9994 |
| 3,3 | 0,9995 | 0,9995 | 0,9995 | 0,9996 | 0,9996 |
| 3,4 | 0,9997 | 0,9997 | 0,9997 | 0,9997 | 0,9997 |
| 3,5 | 0,9998 | 0,9998 | 0,9998 | 0,9998 | 0,9998 |
| 3,6 | 0,9998 | 0,9998 | 0,9999 | 0,9999 | 0,9999 |
| 3,7 | 0,9999 | 0,9999 | 0,9999 | 0,9999 | 0,9999 |
| 3,8 | 0,9999 | 0,9999 | 0,9999 | 0,9999 | 0,9999 |
| 3,9 | 1,0000 | 1,0000 | 1,0000 | 1,0000 | 1,0000 |

**Colonnes 0,05 à 0,09**

| z | 0,05 | 0,06 | 0,07 | 0,08 | 0,09 |
|---|---|---|---|---|---|
| 0,0 | 0,5199 | 0,5239 | 0,5279 | 0,5319 | 0,5359 |
| 0,1 | 0,5596 | 0,5636 | 0,5675 | 0,5714 | 0,5753 |
| 0,2 | 0,5987 | 0,6026 | 0,6064 | 0,6103 | 0,6141 |
| 0,3 | 0,6368 | 0,6406 | 0,6443 | 0,6480 | 0,6517 |
| 0,4 | 0,6736 | 0,6772 | 0,6808 | 0,6844 | 0,6879 |
| 0,5 | 0,7088 | 0,7123 | 0,7157 | 0,7190 | 0,7224 |
| 0,6 | 0,7422 | 0,7454 | 0,7486 | 0,7517 | 0,7549 |
| 0,7 | 0,7734 | 0,7764 | 0,7794 | 0,7823 | 0,7852 |
| 0,8 | 0,8023 | 0,8051 | 0,8078 | 0,8106 | 0,8133 |
| 0,9 | 0,8289 | 0,8315 | 0,8340 | 0,8365 | 0,8389 |
| 1,0 | 0,8531 | 0,8554 | 0,8577 | 0,8599 | 0,8621 |
| 1,1 | 0,8749 | 0,8770 | 0,8790 | 0,8810 | 0,8830 |
| 1,2 | 0,8944 | 0,8962 | 0,8980 | 0,8997 | 0,9015 |
| 1,3 | 0,9115 | 0,9131 | 0,9147 | 0,9162 | 0,9177 |
| 1,4 | 0,9265 | 0,9279 | 0,9292 | 0,9306 | 0,9319 |
| 1,5 | 0,9394 | 0,9406 | 0,9418 | 0,9429 | 0,9441 |
| 1,6 | 0,9505 | 0,9515 | 0,9525 | 0,9535 | 0,9545 |
| 1,7 | 0,9599 | 0,9608 | 0,9616 | 0,9625 | 0,9633 |
| 1,8 | 0,9678 | 0,9686 | 0,9693 | 0,9699 | 0,9706 |
| 1,9 | 0,9744 | 0,9750 | 0,9756 | 0,9761 | 0,9767 |
| 2,0 | 0,9798 | 0,9803 | 0,9808 | 0,9812 | 0,9817 |
| 2,1 | 0,9842 | 0,9846 | 0,9850 | 0,9854 | 0,9857 |
| 2,2 | 0,9878 | 0,9881 | 0,9884 | 0,9887 | 0,9890 |
| 2,3 | 0,9906 | 0,9909 | 0,9911 | 0,9913 | 0,9916 |
| 2,4 | 0,9929 | 0,9931 | 0,9932 | 0,9934 | 0,9936 |
| 2,5 | 0,9946 | 0,9948 | 0,9949 | 0,9951 | 0,9952 |
| 2,6 | 0,9960 | 0,9961 | 0,9962 | 0,9963 | 0,9964 |
| 2,7 | 0,9970 | 0,9971 | 0,9972 | 0,9973 | 0,9974 |
| 2,8 | 0,9978 | 0,9979 | 0,9979 | 0,9980 | 0,9981 |
| 2,9 | 0,9984 | 0,9985 | 0,9985 | 0,9986 | 0,9986 |
| 3,0 | 0,9989 | 0,9989 | 0,9989 | 0,9990 | 0,9990 |
| 3,1 | 0,9992 | 0,9992 | 0,9992 | 0,9993 | 0,9993 |
| 3,2 | 0,9994 | 0,9994 | 0,9995 | 0,9995 | 0,9995 |
| 3,3 | 0,9996 | 0,9996 | 0,9996 | 0,9996 | 0,9997 |
| 3,4 | 0,9997 | 0,9997 | 0,9997 | 0,9997 | 0,9998 |
| 3,5 | 0,9998 | 0,9998 | 0,9998 | 0,9998 | 0,9998 |
| 3,6 | 0,9999 | 0,9999 | 0,9999 | 0,9999 | 0,9999 |
| 3,7 | 0,9999 | 0,9999 | 0,9999 | 0,9999 | 0,9999 |
| 3,8 | 0,9999 | 0,9999 | 0,9999 | 0,9999 | 0,9999 |
| 3,9 | 1,0000 | 1,0000 | 1,0000 | 1,0000 | 1,0000 |

## III. Quantiles à connaître {Lycée}

| Probabilité | Valeur de z | Utilisation |
|---|---|---|
| $\Phi(z) = 0{,}90$ | 1,282 | risque unilatéral de 10 % |
| $\Phi(z) = 0{,}95$ | 1,645 | risque unilatéral de 5 % |
| $\Phi(z) = 0{,}975$ | 1,960 | intervalle à 95 % |
| $\Phi(z) = 0{,}99$ | 2,326 | risque unilatéral de 1 % |
| $\Phi(z) = 0{,}995$ | 2,576 | intervalle à 99 % |

## IV. Calculer toutes les probabilités {Lycée}

[IMAGE_2]

| Probabilité cherchée | Formule |
|---|---|
| À gauche de $z$ | $P(Z \leqslant z) = \Phi(z)$ |
| À droite de $z$ | $P(Z > z) = 1 - \Phi(z)$ |
| À gauche d’un nombre négatif | $P(Z \leqslant -z) = 1 - \Phi(z)$ |
| Entre deux valeurs | $P(a \leqslant Z \leqslant b) = \Phi(b) - \Phi(a)$ |
| Intervalle centré | $P(-z \leqslant Z \leqslant z) = 2\,\Phi(z) - 1$ |

::: exemple Avec une loi $\mathcal{N}(100\,;15^2)$
$X$ suit la loi normale de moyenne $100$ et d’écart type $15$. On centre et on réduit :
$$P(X \leqslant 130) = P\left(Z \leqslant \frac{130 - 100}{15}\right) = \Phi(2) \approx 0{,}9772$$
:::
