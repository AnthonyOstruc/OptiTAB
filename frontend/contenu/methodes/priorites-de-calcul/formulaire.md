---
{
  "slug": "priorites-de-calcul",
  "titre": "Priorités de calcul : dans quel ordre calculer",
  "titreCourt": "Priorités de calcul",
  "titreSeo": "Priorités opératoires : les règles, des exemples et les pièges",
  "description": "Les priorités de calcul expliquées pas à pas : parenthèses, puissances, multiplications et divisions, additions et soustractions, avec exemples et pièges.",
  "chapo": "Dans quel ordre effectuer les opérations d’un calcul : les règles des priorités, un exemple résolu étape par étape, les calculs de gauche à droite, les crochets, la barre de fraction et le piège du signe moins.",
  "resume": "Parenthèses, puissances, ×, ÷, +, −",
  "vignette": "carte_priorites",
  "theme": "Priorités",
  "niveaux": ["Primaire", "Collège"],
  "ordre": 6,
  "publie": "2026-11-16",
  "modifie": "2026-11-16",
  "motsCles": ["priorités de calcul", "priorités opératoires", "ordre des opérations", "priorité multiplication addition", "calcul avec parenthèses", "règles de priorité", "priorités calcul exemple"],
  "figures": [
    { "nom": "priorites_etapes", "alt": "Le calcul 7 + 3 × (8 − 2)² effectué en quatre étapes soulignées : parenthèses (6), puissance (36), multiplication (108), addition (115)." },
    { "nom": "carte_priorites", "alt": "Aperçu : le calcul 7 + 3 × (8 − 2)² effectué étape par étape jusqu’à 115.", "carte": true }
  ],
  "chapitresLies": [
    "ce2/combiner-les-operations",
    "5e/operations-et-priorites",
    "6e/programmes-de-calcul"
  ],
  "faq": [
    ["Quel est l’ordre des priorités de calcul ?", "On calcule d’abord ce qui est entre parenthèses, puis les puissances, puis les multiplications et les divisions de gauche à droite, et enfin les additions et les soustractions de gauche à droite."],
    ["Combien font 2 + 3 × 4 ?", "2 + 3 × 4 = 2 + 12 = 14. La multiplication passe avant l’addition ; trouver 20 est une erreur fréquente."],
    ["La multiplication est-elle prioritaire sur la division ?", "Non, elles ont la même priorité : on les effectue dans l’ordre, de gauche à droite. 24 ÷ 4 × 2 = 6 × 2 = 12."],
    ["Combien font −3² ?", "−3² = −9, car la puissance porte seulement sur 3. En revanche, (−3)² = 9, car la puissance porte sur −3 tout entier."],
    ["Comment taper un calcul avec une fraction à la calculatrice ?", "On met des parenthèses autour du numérateur et du dénominateur : (8 + 4) ÷ (5 − 2) = 12 ÷ 3 = 4. Sans parenthèses, la calculatrice ferait 8 + 4 ÷ 5 − 2."]
  ]
}
---
<!-- optitab:1 -->
## I. Les règles des priorités {Collège}

::: retenir L’ordre des opérations
1. Les calculs **entre parenthèses**, en commençant par les plus intérieures.
2. Les **puissances**.
3. Les **multiplications et les divisions**, de gauche à droite.
4. Les **additions et les soustractions**, de gauche à droite.
:::

::: attention Erreur fréquente
Calculer dans l’ordre de lecture : $2 + 3 \times 4$ ne fait pas $5 \times 4 = 20$. La multiplication passe d’abord : $2 + 3 \times 4 = 2 + 12 = 14$.
:::

## II. Un calcul étape par étape {Collège}

[IMAGE_1]

À chaque ligne, on souligne l’opération prioritaire, on l’effectue et on recopie tout le reste sans le changer.

## III. De gauche à droite {Primaire}

Les multiplications et les divisions ont **la même priorité** : on les fait dans l’ordre où elles apparaissent. C’est la même chose pour les additions et les soustractions.

| Calcul | Juste | Faux |
|---|---|---|
| $24 \div 4 \times 2$ | $6 \times 2 = 12$ | $24 \div 8 = 3$ |
| $10 - 4 + 3$ | $6 + 3 = 9$ | $10 - 7 = 3$ |

## IV. Parenthèses et crochets {Collège}

Quand il y a des parenthèses dans des parenthèses, on écrit souvent des **crochets**, et on commence par l’intérieur.

$$
\begin{aligned}
2 \times [5 + (6 - 2) \times 3] &= 2 \times [5 + 4 \times 3] \\
&= 2 \times [5 + 12] \\
&= 2 \times 17 = 34
\end{aligned}
$$

## V. La barre de fraction {Collège}

Une barre de fraction joue le rôle de parenthèses : on calcule le numérateur et le dénominateur avant de diviser.

$$\frac{8 + 4}{5 - 2} = \frac{12}{3} = 4$$

::: conseil À la calculatrice
On tape $(8 + 4) \div (5 - 2)$. Sans parenthèses, la calculatrice ferait $8 + 4 \div 5 - 2$ et donnerait $6{,}8$.
:::

## VI. Le piège du signe moins {Collège}

La puissance passe avant le signe moins placé devant un nombre.

| Calcul | Ce qu’on calcule | Résultat |
|---|---|---|
| $-3^2$ | $-(3 \times 3)$ | $-9$ |
| $(-3)^2$ | $(-3) \times (-3)$ | $9$ |
