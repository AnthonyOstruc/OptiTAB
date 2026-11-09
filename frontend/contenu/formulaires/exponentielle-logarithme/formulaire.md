---
{
  "slug": "exponentielle-logarithme",
  "titre": "Exponentielle et logarithme",
  "titreCourt": "Exponentielle et logarithme",
  "titreSeo": "Exponentielle et logarithme népérien : propriétés et limites",
  "description": "Toutes les propriétés de l’exponentielle et du logarithme népérien : règles de calcul, équations, dérivées, limites et croissances comparées. Avec courbes.",
  "chapo": "Les règles de calcul de l’exponentielle et du logarithme népérien, les équations, les dérivées, les limites et les croissances comparées, avec les courbes.",
  "resume": "Propriétés de eˣ et ln x, limites, croissances comparées",
  "vignette": "exp_ln",
  "theme": "Analyse",
  "niveaux": ["Lycée", "Supérieur"],
  "ordre": 10,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["propriétés logarithme", "propriétés exponentielle", "logarithme népérien", "ln formules", "limite exponentielle", "croissances comparées", "dérivée ln", "dérivée exponentielle"],
  "figures": [
    { "nom": "exp_ln", "alt": "Courbes de la fonction exponentielle et de la fonction logarithme népérien, symétriques par rapport à la droite d’équation y = x, passant par (0 ; 1), (1 ; e), (1 ; 0) et (e ; 1)." }
  ],
  "chapitresLies": [
    "premiere/fonction-exponentielle",
    "terminale/fonction-exponentielle",
    "terminale/fonction-logarithme-neperien",
    "terminale/limites-des-fonctions"
  ],
  "faq": [
    ["Quelles sont les propriétés du logarithme népérien ?", "Pour a et b strictement positifs : ln(ab) = ln a + ln b, ln(a/b) = ln a − ln b, ln(1/a) = −ln a et ln(aⁿ) = n ln a. De plus, ln 1 = 0 et ln e = 1."],
    ["Comment résoudre l’équation eˣ = k ?", "Si k > 0, l’équation a une unique solution : x = ln k. Si k ≤ 0, elle n’a aucune solution, car une exponentielle est toujours strictement positive."],
    ["Que signifie « croissances comparées » ?", "Ce sont des limites qui comparent l’exponentielle, les puissances de x et le logarithme. En +∞, eˣ l’emporte sur toute puissance de x, qui l’emporte sur ln x : par exemple eˣ/x tend vers +∞ et ln x / x tend vers 0."],
    ["Quel est le lien entre exponentielle et logarithme ?", "Ce sont des fonctions réciproques : pour x > 0, e^(ln x) = x, et pour tout réel x, ln(eˣ) = x. Leurs courbes sont symétriques par rapport à la droite d’équation y = x."]
  ]
}
---
<!-- optitab:1 -->
## I. Fonction exponentielle {Lycée}

::: definition
La fonction exponentielle est l’unique fonction $f$ dérivable sur $\mathbb{R}$ telle que $f' = f$ et $f(0) = 1$. On note $f(x) = \mathrm{e}^x$, avec $\mathrm{e} \approx 2{,}718$.
:::

| Propriété | Formule |
|---|---|
| Valeurs | $\mathrm{e}^0 = 1$ et $\mathrm{e}^1 = \mathrm{e}$ |
| Signe | $\mathrm{e}^x > 0$ pour tout réel $x$ |
| Produit | $\mathrm{e}^{a+b} = \mathrm{e}^a \times \mathrm{e}^b$ |
| Quotient | $\mathrm{e}^{a-b} = \dfrac{\mathrm{e}^a}{\mathrm{e}^b}$ |
| Inverse | $\mathrm{e}^{-a} = \dfrac{1}{\mathrm{e}^a}$ |
| Puissance | $\left(\mathrm{e}^a\right)^n = \mathrm{e}^{na}$ |

## II. Logarithme népérien {Lycée}

::: definition
Pour $x > 0$, $\ln x$ est l’unique réel $y$ tel que $\mathrm{e}^y = x$. La fonction $\ln$ est définie sur $]0\,;+\infty[$.
:::

Pour $a > 0$, $b > 0$ et $n$ entier relatif :

| Propriété | Formule |
|---|---|
| Valeurs | $\ln 1 = 0$ et $\ln \mathrm{e} = 1$ |
| Fonctions réciproques | $\mathrm{e}^{\ln a} = a$ et $\ln\left(\mathrm{e}^x\right) = x$ |
| Produit | $\ln(ab) = \ln a + \ln b$ |
| Quotient | $\ln\left(\dfrac{a}{b}\right) = \ln a - \ln b$ |
| Inverse | $\ln\left(\dfrac{1}{a}\right) = -\ln a$ |
| Puissance | $\ln\left(a^n\right) = n \ln a$ |
| Racine carrée | $\ln \sqrt{a} = \dfrac{1}{2} \ln a$ |

::: attention Erreur fréquente
$\ln(a + b) \neq \ln a + \ln b$ : le logarithme transforme les **produits** en sommes, pas les sommes.
:::

[IMAGE_1]

Les deux courbes sont symétriques par rapport à la droite d’équation $y = x$, car les fonctions $\exp$ et $\ln$ sont réciproques.

## III. Équations et inéquations {Lycée}

| Égalité ou inégalité | Équivaut à |
|---|---|
| $\mathrm{e}^a = \mathrm{e}^b$ | $a = b$ |
| $\mathrm{e}^a < \mathrm{e}^b$ | $a < b$ |
| $\ln a = \ln b$ (avec $a, b > 0$) | $a = b$ |
| $\ln a < \ln b$ (avec $a, b > 0$) | $a < b$ |
| $\mathrm{e}^x = k$ (avec $k > 0$) | $x = \ln k$ |
| $\ln x = k$ | $x = \mathrm{e}^k$ |

- $\ln x < 0$ pour $0 < x < 1$, et $\ln x > 0$ pour $x > 1$.
- Si $k \leqslant 0$, l’équation $\mathrm{e}^x = k$ n’a pas de solution.

::: exemple
- $\mathrm{e}^{2x} = 3 \iff 2x = \ln 3 \iff x = \dfrac{\ln 3}{2}$
- Pour $x > 0$ : $\ln x > 2 \iff x > \mathrm{e}^2$
:::

## IV. Dérivées {Lycée}

| Fonction | Dérivée |
|---|---|
| $\mathrm{e}^x$ | $\mathrm{e}^x$ |
| $\mathrm{e}^{ax+b}$ | $a\,\mathrm{e}^{ax+b}$ |
| $\mathrm{e}^{u}$ | $u'\,\mathrm{e}^{u}$ |
| $\ln x$ (pour $x > 0$) | $\dfrac{1}{x}$ |
| $\ln u$ (pour $u > 0$) | $\dfrac{u'}{u}$ |

Les fonctions $\exp$ et $\ln$ sont strictement croissantes sur leur ensemble de définition.

## V. Limites et croissances comparées {Lycée}

| Limite | Valeur |
|---|---|
| $\displaystyle\lim_{x \to +\infty} \mathrm{e}^x$ | $+\infty$ |
| $\displaystyle\lim_{x \to -\infty} \mathrm{e}^x$ | $0$ |
| $\displaystyle\lim_{x \to +\infty} \ln x$ | $+\infty$ |
| $\displaystyle\lim_{x \to 0^+} \ln x$ | $-\infty$ |

Croissances comparées, pour tout entier $n \geqslant 1$ :

| Limite | Valeur |
|---|---|
| $\displaystyle\lim_{x \to +\infty} \frac{\mathrm{e}^x}{x^n}$ | $+\infty$ |
| $\displaystyle\lim_{x \to -\infty} x^n\,\mathrm{e}^x$ | $0$ |
| $\displaystyle\lim_{x \to +\infty} \frac{\ln x}{x^n}$ | $0$ |
| $\displaystyle\lim_{x \to 0^+} x^n \ln x$ | $0$ |

Limites en $0$ (taux d’accroissement) :

| Limite | Valeur |
|---|---|
| $\displaystyle\lim_{x \to 0} \frac{\mathrm{e}^x - 1}{x}$ | $1$ |
| $\displaystyle\lim_{x \to 0} \frac{\ln(1 + x)}{x}$ | $1$ |

::: retenir
En $+\infty$, l’exponentielle l’emporte sur toute puissance de $x$, et toute puissance de $x$ l’emporte sur le logarithme.
:::

## VI. Puissances réelles et logarithme décimal {Lycée}

| Notion | Formule |
|---|---|
| Puissance réelle ($a > 0$) | $a^x = \mathrm{e}^{x \ln a}$ |
| Logarithme décimal | $\log x = \dfrac{\ln x}{\ln 10}$ pour $x > 0$ |
| Puissances de 10 | $\log\left(10^n\right) = n$ |

## VII. Fonctions hyperboliques {Supérieur}

| Fonction | Définition et dérivée |
|---|---|
| Cosinus hyperbolique | $\operatorname{ch} x = \dfrac{\mathrm{e}^x + \mathrm{e}^{-x}}{2}$ et $\operatorname{ch}' = \operatorname{sh}$ |
| Sinus hyperbolique | $\operatorname{sh} x = \dfrac{\mathrm{e}^x - \mathrm{e}^{-x}}{2}$ et $\operatorname{sh}' = \operatorname{ch}$ |
| Relation fondamentale | $\operatorname{ch}^2 x - \operatorname{sh}^2 x = 1$ |
