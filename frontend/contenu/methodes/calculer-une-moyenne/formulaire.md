---
{
  "slug": "calculer-une-moyenne",
  "titre": "Calculer une moyenne : notes et coefficients",
  "titreCourt": "Calculer une moyenne",
  "titreSeo": "Calcul de moyenne avec coefficients : calculateur gratuit",
  "description": "Calculateur de moyenne gratuit avec coefficients et méthode : moyenne simple, moyenne pondérée, note sur 20, note à obtenir pour atteindre une moyenne.",
  "chapo": "Un calculateur pour obtenir tout de suite la moyenne de vos notes, avec ou sans coefficients, et la méthode pas à pas : moyenne simple, moyenne pondérée, notes sur 10 ou sur 40, et la note qu’il faut pour atteindre une moyenne.",
  "resume": "Calculateur de notes, coefficients",
  "vignette": "carte_moyenne",
  "theme": "Moyennes",
  "niveaux": ["Collège"],
  "ordre": 2,
  "outil": "moyenne",
  "publie": "2026-11-16",
  "modifie": "2026-11-16",
  "motsCles": ["calcul moyenne", "calculer une moyenne", "calcul moyenne avec coefficient", "moyenne pondérée", "calculateur de moyenne", "moyenne de notes", "calculer sa moyenne", "quelle note pour avoir 10 de moyenne"],
  "figures": [
    { "nom": "moyenne_barres", "alt": "Diagramme en barres de quatre notes, 9 en maths, 16 en français, 8 en anglais et 17 en histoire, avec une ligne en pointillés à 12,5 : la moyenne." },
    { "nom": "carte_moyenne", "alt": "Aperçu : quatre barres de notes et la ligne de la moyenne 12,5.", "carte": true }
  ],
  "liees": ["formulaires/statistiques"],
  "chapitresLies": [
    "6e/statistiques-tres-simples",
    "4e/statistiques-et-diagrammes",
    "3e/statistiques"
  ],
  "faq": [
    ["Comment calculer une moyenne ?", "On additionne toutes les valeurs, puis on divise par le nombre de valeurs. Pour les notes 9, 16, 8 et 17 : (9 + 16 + 8 + 17) ÷ 4 = 50 ÷ 4 = 12,5."],
    ["Comment calculer une moyenne avec des coefficients ?", "On multiplie chaque note par son coefficient, on additionne ces produits, puis on divise par la somme des coefficients. Pour 12 (coefficient 2), 15 (coefficient 1) et 9 (coefficient 3) : (24 + 15 + 27) ÷ 6 = 66 ÷ 6 = 11."],
    ["Comment mettre une note sur 20 ?", "On divise la note par le barème, puis on multiplie par 20. Un 7 sur 10 vaut 7 ÷ 10 × 20 = 14 sur 20 ; un 30 sur 40 vaut 15 sur 20."],
    ["Quelle note faut-il pour avoir une moyenne donnée ?", "On calcule le total de points nécessaire, puis on retire les points déjà obtenus. Avec 8 et 11, pour avoir 12 de moyenne sur trois notes de même coefficient, il faut 3 × 12 = 36 points, donc 36 − 19 = 17 à la dernière note."],
    ["Quelle est la différence entre la moyenne et la médiane ?", "La moyenne tient compte de toutes les valeurs ; la médiane est la valeur du milieu quand on les range dans l’ordre. Pour 5, 12, 13, 14 et 16, la moyenne vaut 12 et la médiane 13 : la note de 5 fait baisser la moyenne, pas la médiane."]
  ]
}
---
<!-- optitab:1 -->
[OUTIL]

## I. La moyenne simple {Collège}

::: formule Moyenne
$$\text{moyenne} = \frac{\text{somme des valeurs}}{\text{nombre de valeurs}}$$
:::

::: exemple Les notes $9$, $16$, $8$ et $17$
$$\frac{9 + 16 + 8 + 17}{4} = \frac{50}{4} = 12{,}5$$
:::

[IMAGE_1]

La moyenne est la note qu’on aurait eue partout si toutes les notes avaient été égales : $4$ notes de $12{,}5$ font aussi $50$ points.

## II. La moyenne avec coefficients {Collège}

Quand une note compte plus qu’une autre, on lui donne un **coefficient**. On parle de moyenne **pondérée**.

::: methode Les trois étapes
1. On multiplie chaque note par son coefficient.
2. On additionne ces produits.
3. On divise par **la somme des coefficients**.
:::

| Note | Coefficient | Note × coefficient |
|---|---|---|
| $12$ | $2$ | $24$ |
| $15$ | $1$ | $15$ |
| $9$ | $3$ | $27$ |
| Total | $6$ | $66$ |

La moyenne vaut $66 \div 6 = 11$.

::: attention Erreur fréquente
Diviser par le nombre de notes au lieu de la somme des coefficients : $66 \div 3 = 22$, une moyenne impossible sur $20$. On divise par $2 + 1 + 3 = 6$.
:::

## III. Ramener une note sur 20 {Collège}

On divise la note par son barème, puis on multiplie par $20$.

| Note obtenue | Calcul | Note sur 20 |
|---|---|---|
| $7$ sur $10$ | $7 \div 10 \times 20$ | $14$ |
| $30$ sur $40$ | $30 \div 40 \times 20$ | $15$ |
| $18$ sur $25$ | $18 \div 25 \times 20$ | $14{,}4$ |

::: conseil Dans le calculateur
Ramenez d’abord chaque note sur $20$, puis saisissez-la avec son coefficient.
:::

## IV. Quelle note pour atteindre une moyenne ? {Collège}

::: methode Calculer la note manquante
1. On calcule le **total de points** qu’il faut : moyenne visée $\times$ somme des coefficients.
2. On retire les points déjà obtenus.
3. On divise par le coefficient de la note qui manque.
:::

::: exemple Avec $8$ et $11$, quelle troisième note pour avoir $12$ de moyenne ?
Trois notes de même coefficient : il faut $3 \times 12 = 36$ points. On en a déjà $8 + 11 = 19$. Il faut donc $36 - 19 = 17$.
:::

## V. Moyenne ou médiane ? {Collège}

La **médiane** est la valeur du milieu quand on range les valeurs dans l’ordre. Pour $5$, $12$, $13$, $14$ et $16$ :

- la moyenne vaut $\dfrac{5 + 12 + 13 + 14 + 16}{5} = \dfrac{60}{5} = 12$ ;
- la médiane vaut $13$, la valeur du milieu.

Une seule note très basse fait baisser la moyenne, mais presque pas la médiane. Les autres indicateurs (quartiles, étendue, écart type) sont dans le formulaire de statistiques, en bas de page.
