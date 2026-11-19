---
{
  "slug": "calculer-une-duree",
  "titre": "Calculer une durée : heures et minutes",
  "titreCourt": "Calculer une durée",
  "titreSeo": "Calcul de durée en heures et minutes : calculateur et méthode",
  "description": "Calculateur de durée gratuit et méthode : durée entre deux heures, heure d’arrivée, conversion des heures décimales en heures et minutes, passage de minuit.",
  "chapo": "Un calculateur pour trouver tout de suite une durée ou une heure d’arrivée, et la méthode pas à pas : la méthode des sauts, la soustraction d’heures, les heures décimales et le passage de minuit.",
  "resume": "Entre deux heures, heures décimales",
  "vignette": "carte_duree",
  "theme": "Durées",
  "niveaux": ["Primaire", "Collège"],
  "ordre": 3,
  "outil": "duree",
  "publie": "2026-11-16",
  "modifie": "2026-11-16",
  "motsCles": ["calcul durée", "calculer une durée", "calcul heures minutes", "durée entre deux heures", "calculateur d’heures", "convertir heures décimales en minutes", "heures décimales", "calculer une heure d’arrivée"],
  "figures": [
    { "nom": "duree_sauts", "alt": "Ligne du temps de 8 h 45 à 11 h 20 avec trois sauts : 15 minutes jusqu’à 9 h 00, 2 heures jusqu’à 11 h 00, puis 20 minutes jusqu’à 11 h 20 ; total 2 h 35 min." },
    { "nom": "carte_duree", "alt": "Aperçu : ligne du temps de 8 h 45 à 11 h 20 avec trois sauts, total 2 h 35 min.", "carte": true }
  ],
  "liees": ["methodes/lire-l-heure", "tables/tableau-de-conversion"],
  "chapitresLies": [
    "ce2/calculer-et-comparer-des-durees",
    "cm1/horaires-et-durees",
    "cm2/lire-l-heure-et-calculer-des-durees",
    "6e/horaires-et-durees"
  ],
  "faq": [
    ["Comment calculer une durée entre deux heures ?", "On avance de l’heure de départ jusqu’à l’heure ronde suivante, puis d’heure en heure, puis jusqu’à l’heure d’arrivée, et on additionne les sauts. De 8 h 45 à 11 h 20 : 15 min + 2 h + 20 min = 2 h 35 min."],
    ["Comment soustraire des heures et des minutes ?", "On soustrait les minutes, puis les heures. S’il n’y a pas assez de minutes, on transforme une heure en 60 minutes : 11 h 20 = 10 h 80, donc 11 h 20 − 8 h 45 = 2 h 35."],
    ["Comment convertir des heures décimales en heures et minutes ?", "On garde la partie entière pour les heures et on multiplie la partie décimale par 60 pour les minutes : 2,75 h = 2 h + 0,75 × 60 min = 2 h 45 min."],
    ["Combien font 1,5 heure ?", "1,5 h = 1 h + 0,5 × 60 min = 1 h 30 min. Attention : 1,30 h n’est pas 1 h 30, c’est 1 h 18 min."],
    ["Comment calculer une durée qui passe minuit ?", "On calcule jusqu’à minuit, puis de minuit à l’heure d’arrivée, et on additionne. De 22 h 30 à 1 h 15 : 1 h 30 + 1 h 15 = 2 h 45."]
  ]
}
---
<!-- optitab:1 -->
[OUTIL]

## I. Les unités de temps {Primaire}

| Durée | Égale à |
|---|---|
| $1$ jour | $24$ heures |
| $1$ heure | $60$ minutes |
| $1$ minute | $60$ secondes |
| un quart d’heure | $15$ minutes |
| une demi-heure | $30$ minutes |
| trois quarts d’heure | $45$ minutes |

::: attention On ne compte pas de 10 en 10
Une heure compte $60$ minutes et non $100$ : après $8$ h $59$ vient $9$ h $00$. C’est pour cela qu’on ne pose pas une soustraction d’heures comme une soustraction de nombres.
:::

## II. La méthode des sauts {Primaire}

C’est la méthode la plus sûre pour trouver une durée entre deux horaires : on avance par **sauts** jusqu’aux heures rondes.

[IMAGE_1]

::: methode De $8$ h $45$ à $11$ h $20$
1. De $8$ h $45$ à $9$ h $00$ : $15$ min.
2. De $9$ h $00$ à $11$ h $00$ : $2$ h.
3. De $11$ h $00$ à $11$ h $20$ : $20$ min.
4. On additionne : $15$ min $+ 2$ h $+ 20$ min $= 2$ h $35$ min.
:::

## III. Soustraire des heures et des minutes {Primaire}

On soustrait les minutes, puis les heures. S’il n’y a pas assez de minutes en haut, on **échange une heure contre 60 minutes**.

::: exemple $11$ h $20$ $-$ $8$ h $45$
On ne peut pas retirer $45$ minutes de $20$ minutes. On écrit $11$ h $20$ $= 10$ h $80$, puis :
- minutes : $80 - 45 = 35$ ;
- heures : $10 - 8 = 2$.

La durée est $2$ h $35$ min.
:::

## IV. Trouver une heure d’arrivée {Primaire}

On ajoute les heures aux heures et les minutes aux minutes, puis on convertit si l’on dépasse $60$ minutes.

::: exemple Départ à $14$ h $50$, trajet de $1$ h $25$
$14$ h $50 + 1$ h $25 = 15$ h $75$. Or $75$ min $= 1$ h $15$ min, donc on arrive à $16$ h $15$.
:::

## V. Les heures décimales {Collège}

Une calculatrice ou un tableur donne souvent les durées en **heures décimales** : $2{,}75$ h. Pour les convertir, on multiplie la partie décimale par $60$.

| Heures décimales | Calcul | Heures et minutes |
|---|---|---|
| $0{,}25$ h | $0{,}25 \times 60$ | $15$ min |
| $0{,}5$ h | $0{,}5 \times 60$ | $30$ min |
| $1{,}2$ h | $1$ h $+ 0{,}2 \times 60$ | $1$ h $12$ min |
| $2{,}75$ h | $2$ h $+ 0{,}75 \times 60$ | $2$ h $45$ min |

Dans l’autre sens, on divise les minutes par $60$ : $1$ h $12$ min $= 1 + \dfrac{12}{60} = 1{,}2$ h.

::: attention Erreur fréquente
Lire $1{,}30$ h comme $1$ h $30$. En réalité, $1{,}30$ h $= 1$ h $+ 0{,}3 \times 60$ min $= 1$ h $18$ min, et $1$ h $30$ s’écrit $1{,}5$ h.
:::

## VI. Une durée qui passe minuit {Collège}

On coupe le calcul en deux : jusqu’à minuit, puis après minuit.

::: exemple De $22$ h $30$ à $1$ h $15$
- De $22$ h $30$ à minuit : $1$ h $30$.
- De minuit à $1$ h $15$ : $1$ h $15$.

Au total : $1$ h $30 + 1$ h $15 = 2$ h $45$.
:::
