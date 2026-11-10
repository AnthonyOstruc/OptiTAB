---
{
  "slug": "trigonometrie",
  "titre": "Formulaire de trigonométrie",
  "titreCourt": "Trigonométrie",
  "titreSeo": "Formulaire de trigonométrie : toutes les formules à connaître",
  "description": "Toutes les formules de trigonométrie : cercle trigonométrique, valeurs remarquables, angles associés, addition, duplication, équations. Gratuit, à imprimer.",
  "chapo": "Toutes les formules de trigonométrie réunies sur une seule page, du triangle rectangle du collège aux formules de transformation du supérieur, avec les schémas pour les retrouver.",
  "resume": "Cercle trigonométrique, valeurs remarquables, cos, sin, tan",
  "vignette": "cercle_complet",
  "theme": "Analyse et géométrie",
  "niveaux": ["Collège", "Lycée", "Supérieur"],
  "ordre": 14,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["formulaire trigonométrie", "formules de trigonométrie", "valeurs remarquables cos sin", "cercle trigonométrique", "formules d'addition", "formules de duplication", "angles associés", "trigonométrie lycée"],
  "figures": [
    { "nom": "triangle_rectangle", "alt": "Triangle ABC rectangle en B avec l’angle alpha en A : l’hypoténuse [AC], le côté adjacent [AB] et le côté opposé [BC] à l’angle alpha." },
    { "nom": "cercle_valeurs", "alt": "Quart du cercle trigonométrique avec les points associés à 0, π/6, π/4, π/3 et π/2 ; leurs cosinus 1/2, √2/2, √3/2 sont lus sur l’axe horizontal et leurs sinus sur l’axe vertical." },
    { "nom": "cercle_complet", "alt": "Cercle trigonométrique complet avec les seize angles remarquables entre -π et π : 0, ±π/6, ±π/4, ±π/3, ±π/2, ±2π/3, ±3π/4, ±5π/6 et π." },
    { "nom": "angles_associes", "alt": "Cercle trigonométrique montrant les points associés à x, -x, π - x, π + x et π/2 - x, symétriques les uns des autres par rapport aux axes, à l’origine et à la droite d’équation y = x." },
    { "nom": "courbes_sin_cos", "alt": "Courbes des fonctions sinus et cosinus entre -2π et 2π, comprises entre -1 et 1, de période 2π." },
    { "nom": "triangle_quelconque", "alt": "Triangle quelconque ABC : le côté a est opposé au sommet A, le côté b au sommet B, le côté c au sommet C, avec les angles A, B et C marqués." }
  ],
  "chapitresLies": [
    "3e/trigonometrie-du-triangle-rectangle",
    "premiere/fonctions-trigonometriques",
    "premiere/calcul-vectoriel-et-produit-scalaire",
    "terminale/fonctions-sinus-et-cosinus",
    "terminale/nombres-complexes"
  ],
  "faq": [
    ["Quelles formules de trigonométrie faut-il connaître par cœur au lycée ?", "La relation cos²x + sin²x = 1, les valeurs remarquables (0, π/6, π/4, π/3, π/2), les angles associés (-x, π - x, π + x, π/2 - x), les dérivées de sinus et cosinus et la résolution de cos x = cos a et sin x = sin a. Les formules d’addition et de duplication se retrouvent vite à partir de cos(a - b)."],
    ["Comment retenir les valeurs remarquables du sinus et du cosinus ?", "Pour 0, π/6, π/4, π/3 et π/2, le sinus vaut successivement √0/2, √1/2, √2/2, √3/2 et √4/2, c’est-à-dire 0, 1/2, √2/2, √3/2 et 1. Le cosinus suit le même tableau dans l’ordre inverse."],
    ["Comment retrouver une formule d’angle associé sans l’apprendre ?", "Placez le point associé à x sur le cercle trigonométrique, puis le point associé à l’angle cherché : ils sont symétriques par rapport à un axe, à l’origine ou à la droite y = x. Le cosinus est l’abscisse et le sinus l’ordonnée : il suffit de lire les signes et d’échanger éventuellement les deux coordonnées."],
    ["Quelle est la différence entre degrés et radians ?", "Ce sont deux unités de mesure des angles : un tour complet mesure 360° ou 2π radians. Pour convertir, on multiplie une mesure en degrés par π/180. Au lycée, la trigonométrie se fait en radians, et la calculatrice doit être réglée en conséquence."],
    ["Ce formulaire est-il gratuit et imprimable ?", "Oui. Le formulaire est en libre accès, sans inscription. Le bouton « Imprimer le formulaire » en donne une version papier propre, sans menus ni publicités."]
  ]
}
---
<!-- optitab:1 -->
## I. Trigonométrie dans le triangle rectangle {Collège}

Dans un triangle rectangle, chaque angle aigu définit trois rapports de longueurs. On repère d’abord l’hypoténuse (le côté opposé à l’angle droit), puis le côté adjacent et le côté opposé à l’angle étudié.

[IMAGE_1]

| Rapport | Définition | Sur la figure |
|---|---|---|
| $\cos\alpha$ | côté adjacent ÷ hypoténuse | $\cos\alpha = \dfrac{AB}{AC}$ |
| $\sin\alpha$ | côté opposé ÷ hypoténuse | $\sin\alpha = \dfrac{BC}{AC}$ |
| $\tan\alpha$ | côté opposé ÷ côté adjacent | $\tan\alpha = \dfrac{BC}{AB}$ |

::: conseil Moyen mnémotechnique : SOH CAH TOA
- **SOH** : **S**inus = **O**pposé sur **H**ypoténuse ;
- **CAH** : **C**osinus = **A**djacent sur **H**ypoténuse ;
- **TOA** : **T**angente = **O**pposé sur **A**djacent.
:::

::: retenir
Pour un angle aigu $\alpha$ : $0 < \cos\alpha < 1$, $0 < \sin\alpha < 1$, et
$$\cos^2\alpha + \sin^2\alpha = 1 \qquad \tan\alpha = \frac{\sin\alpha}{\cos\alpha}$$
:::

## II. Cercle trigonométrique et radians {Lycée}

::: definition Cercle trigonométrique
C’est le cercle de centre $O$ et de rayon $1$, parcouru dans le sens direct (sens inverse des aiguilles d’une montre). À tout réel $x$ est associé un point $M$ du cercle : **$\cos x$ est l’abscisse de $M$** et **$\sin x$ est son ordonnée**.
:::

| Propriété | Formule |
|---|---|
| Relation fondamentale | $\cos^2 x + \sin^2 x = 1$ |
| Encadrement | $-1 \leqslant \cos x \leqslant 1$ et $-1 \leqslant \sin x \leqslant 1$ |
| Tangente | $\tan x = \dfrac{\sin x}{\cos x}$, pour $x \neq \dfrac{\pi}{2} + k\pi$ |
| Autre écriture | $1 + \tan^2 x = \dfrac{1}{\cos^2 x}$ |
| Degrés → radians | un angle de $d$ degrés mesure $d \times \dfrac{\pi}{180}$ radians |
| Un tour complet | $360^\circ = 2\pi$ rad et $180^\circ = \pi$ rad |

Dans tout le formulaire, $k$ désigne un entier relatif : $k \in \mathbb{Z}$.

## III. Valeurs remarquables {Lycée}

[IMAGE_2]

| Degrés | Radians | $\cos x$ | $\sin x$ | $\tan x$ |
|---|---|---|---|---|
| $0^\circ$ | $0$ | $1$ | $0$ | $0$ |
| $30^\circ$ | $\dfrac{\pi}{6}$ | $\dfrac{\sqrt{3}}{2}$ | $\dfrac{1}{2}$ | $\dfrac{\sqrt{3}}{3}$ |
| $45^\circ$ | $\dfrac{\pi}{4}$ | $\dfrac{\sqrt{2}}{2}$ | $\dfrac{\sqrt{2}}{2}$ | $1$ |
| $60^\circ$ | $\dfrac{\pi}{3}$ | $\dfrac{1}{2}$ | $\dfrac{\sqrt{3}}{2}$ | $\sqrt{3}$ |
| $90^\circ$ | $\dfrac{\pi}{2}$ | $0$ | $1$ | non définie |
| $180^\circ$ | $\pi$ | $-1$ | $0$ | $0$ |

::: conseil Astuce de mémorisation
Pour $0$, $\dfrac{\pi}{6}$, $\dfrac{\pi}{4}$, $\dfrac{\pi}{3}$ et $\dfrac{\pi}{2}$, le sinus vaut successivement
$$\frac{\sqrt{0}}{2},\quad \frac{\sqrt{1}}{2},\quad \frac{\sqrt{2}}{2},\quad \frac{\sqrt{3}}{2},\quad \frac{\sqrt{4}}{2}.$$
Le cosinus prend les mêmes valeurs dans l’ordre inverse.
:::

Les autres angles remarquables se déduisent par symétrie : par exemple $\cos\dfrac{2\pi}{3} = -\dfrac{1}{2}$ et $\sin\left(-\dfrac{\pi}{4}\right) = -\dfrac{\sqrt{2}}{2}$.

[IMAGE_3]

## IV. Angles associés, parité et périodicité {Lycée}

[IMAGE_4]

| Angle $\theta$ | $\cos\theta$ | $\sin\theta$ | $\tan\theta$ |
|---|---|---|---|
| $-x$ | $\cos x$ | $-\sin x$ | $-\tan x$ |
| $\pi - x$ | $-\cos x$ | $\sin x$ | $-\tan x$ |
| $\pi + x$ | $-\cos x$ | $-\sin x$ | $\tan x$ |
| $\dfrac{\pi}{2} - x$ | $\sin x$ | $\cos x$ | $\dfrac{1}{\tan x}$ |
| $\dfrac{\pi}{2} + x$ | $-\sin x$ | $\cos x$ | $-\dfrac{1}{\tan x}$ |

Exemple de lecture : la ligne $\pi - x$ donne $\cos(\pi - x) = -\cos x$ et $\sin(\pi - x) = \sin x$.

::: retenir Parité et périodicité
- $\cos$ est **paire**, $\sin$ et $\tan$ sont **impaires** ;
- $\cos(x + 2k\pi) = \cos x$ et $\sin(x + 2k\pi) = \sin x$ : période $2\pi$ ;
- $\tan(x + k\pi) = \tan x$ : période $\pi$.
:::

::: methode Retrouver une formule sans l’apprendre
Placer les points associés à $x$ et à l’angle cherché sur le cercle : ils sont symétriques par rapport à un axe, à l’origine ou à la droite $y = x$. On lit alors les signes des coordonnées, et on échange cosinus et sinus pour la symétrie par rapport à $y = x$.
:::

## V. Formules d’addition {Lycée}

| Expression | Formule |
|---|---|
| Cosinus d’une somme | $\cos(a + b) = \cos a\cos b - \sin a\sin b$ |
| Cosinus d’une différence | $\cos(a - b) = \cos a\cos b + \sin a\sin b$ |
| Sinus d’une somme | $\sin(a + b) = \sin a\cos b + \cos a\sin b$ |
| Sinus d’une différence | $\sin(a - b) = \sin a\cos b - \cos a\sin b$ |

::: attention Erreur fréquente
$\cos(a + b) \neq \cos a + \cos b$. Par exemple, $\cos(\pi + \pi) = \cos 2\pi = 1$, alors que $\cos\pi + \cos\pi = -2$.
:::

::: exemple Valeur exacte de $\cos\dfrac{\pi}{12}$
$$
\begin{aligned}
\cos\frac{\pi}{12} &= \cos\left(\frac{\pi}{3} - \frac{\pi}{4}\right) \\
&= \frac{1}{2}\times\frac{\sqrt{2}}{2} + \frac{\sqrt{3}}{2}\times\frac{\sqrt{2}}{2} \\
&= \frac{\sqrt{6} + \sqrt{2}}{4}
\end{aligned}
$$
:::

## VI. Duplication et linéarisation {Lycée}

| Expression | Formule |
|---|---|
| Cosinus de l’angle double | $\cos 2a = \cos^2 a - \sin^2 a$ |
| (avec $\sin^2 a = 1 - \cos^2 a$) | $\cos 2a = 2\cos^2 a - 1$ |
| (avec $\cos^2 a = 1 - \sin^2 a$) | $\cos 2a = 1 - 2\sin^2 a$ |
| Sinus de l’angle double | $\sin 2a = 2\sin a\cos a$ |
| Linéarisation de $\cos^2 a$ | $\cos^2 a = \dfrac{1 + \cos 2a}{2}$ |
| Linéarisation de $\sin^2 a$ | $\sin^2 a = \dfrac{1 - \cos 2a}{2}$ |

::: conseil Quand les utiliser ?
Les formules de duplication servent à résoudre des équations comme $\cos 2x = \cos x$. La linéarisation sert à calculer des intégrales, par exemple :
$$\int_0^{\pi} \sin^2 x \, \mathrm{d}x = \int_0^{\pi} \frac{1 - \cos 2x}{2} \, \mathrm{d}x = \frac{\pi}{2}$$
:::

## VII. Fonctions sinus, cosinus et tangente {Lycée}

[IMAGE_5]

| Fonction | Période | Parité | Dérivée |
|---|---|---|---|
| $\sin$ | $2\pi$ | impaire | $\cos$ |
| $\cos$ | $2\pi$ | paire | $-\sin$ |
| $\tan$ | $\pi$ | impaire | $1 + \tan^2$ |

Les fonctions sinus et cosinus sont définies sur $\mathbb{R}$ ; la fonction tangente est définie pour $x \neq \dfrac{\pi}{2} + k\pi$, et sa dérivée s’écrit aussi $\tan' x = \dfrac{1}{\cos^2 x}$.

| Résultat | Formule |
|---|---|
| Dérivée de $\sin(ax + b)$ | $a\cos(ax + b)$ |
| Dérivée de $\cos(ax + b)$ | $-a\sin(ax + b)$ |
| Primitives | $\cos$ a pour primitive $\sin$ ; $\sin$ a pour primitive $-\cos$ |
| Limite en $0$ | $\displaystyle\lim_{x \to 0} \frac{\sin x}{x} = 1$ |
| Limite en $0$ | $\displaystyle\lim_{x \to 0} \frac{\cos x - 1}{x} = 0$ |

## VIII. Équations trigonométriques {Lycée}

| Équation | Solutions dans $\mathbb{R}$ (avec $k \in \mathbb{Z}$) |
|---|---|
| $\cos x = \cos a$ | $x = a + 2k\pi$ ou $x = -a + 2k\pi$ |
| $\sin x = \sin a$ | $x = a + 2k\pi$ ou $x = \pi - a + 2k\pi$ |
| $\tan x = \tan a$ | $x = a + k\pi$ |
| $\cos x = 0$ | $x = \dfrac{\pi}{2} + k\pi$ |
| $\sin x = 0$ | $x = k\pi$ |
| $\cos x = 1$ | $x = 2k\pi$ |
| $\sin x = 1$ | $x = \dfrac{\pi}{2} + 2k\pi$ |

::: exemple Résoudre $\cos x = \dfrac{1}{2}$ dans $]-\pi\,;\pi]$
Comme $\dfrac{1}{2} = \cos\dfrac{\pi}{3}$, on a $x = \dfrac{\pi}{3} + 2k\pi$ ou $x = -\dfrac{\pi}{3} + 2k\pi$. Dans $]-\pi\,;\pi]$, les solutions sont $-\dfrac{\pi}{3}$ et $\dfrac{\pi}{3}$.
:::

## IX. Trigonométrie dans un triangle quelconque {Lycée}

[IMAGE_6]

Dans un triangle $ABC$, on note $a = BC$, $b = CA$ et $c = AB$ : chaque côté porte le nom du sommet qui lui fait face.

| Résultat | Formule |
|---|---|
| Somme des angles | $\widehat{A} + \widehat{B} + \widehat{C} = \pi$ |
| Formule d’Al‑Kashi | $a^2 = b^2 + c^2 - 2bc\cos\widehat{A}$ |
| Loi des sinus | $\dfrac{a}{\sin\widehat{A}} = \dfrac{b}{\sin\widehat{B}} = \dfrac{c}{\sin\widehat{C}}$ |
| Aire du triangle | $\mathcal{A} = \dfrac{1}{2}\,bc\sin\widehat{A}$ |

La formule d’Al‑Kashi généralise le théorème de Pythagore : si $\widehat{A}$ est droit, $\cos\widehat{A} = 0$ et $a^2 = b^2 + c^2$. Elle s’écrit de la même façon pour les deux autres côtés.

## X. Lien avec les nombres complexes {Lycée}

| Résultat | Formule |
|---|---|
| Notation exponentielle | $\mathrm{e}^{\mathrm{i}x} = \cos x + \mathrm{i}\sin x$ |
| Formules d’Euler | $\cos x = \dfrac{\mathrm{e}^{\mathrm{i}x} + \mathrm{e}^{-\mathrm{i}x}}{2}$ et $\sin x = \dfrac{\mathrm{e}^{\mathrm{i}x} - \mathrm{e}^{-\mathrm{i}x}}{2\mathrm{i}}$ |
| Formule de Moivre | $(\cos x + \mathrm{i}\sin x)^n = \cos(nx) + \mathrm{i}\sin(nx)$ |

::: remarque
Les formules d’addition se retrouvent en une ligne : $\mathrm{e}^{\mathrm{i}(a+b)} = \mathrm{e}^{\mathrm{i}a}\,\mathrm{e}^{\mathrm{i}b}$, puis on identifie parties réelles et parties imaginaires.
:::

## XI. Formules en tangente {Supérieur}

| Expression | Formule |
|---|---|
| Tangente d’une somme | $\tan(a + b) = \dfrac{\tan a + \tan b}{1 - \tan a\tan b}$ |
| Tangente d’une différence | $\tan(a - b) = \dfrac{\tan a - \tan b}{1 + \tan a\tan b}$ |
| Tangente de l’angle double | $\tan 2a = \dfrac{2\tan a}{1 - \tan^2 a}$ |

Ces formules sont valables dès que les tangentes écrites existent.

Pour $a \neq \pi + 2k\pi$, on pose $t = \tan\dfrac{a}{2}$. Alors :

| Expression | En fonction de $t$ |
|---|---|
| Cosinus | $\cos a = \dfrac{1 - t^2}{1 + t^2}$ |
| Sinus | $\sin a = \dfrac{2t}{1 + t^2}$ |
| Tangente (si $t^2 \neq 1$) | $\tan a = \dfrac{2t}{1 - t^2}$ |

## XII. Transformations produit ↔ somme {Supérieur}

| Produit | Somme |
|---|---|
| $\cos a\cos b$ | $\dfrac{1}{2}\big[\cos(a - b) + \cos(a + b)\big]$ |
| $\sin a\sin b$ | $\dfrac{1}{2}\big[\cos(a - b) - \cos(a + b)\big]$ |
| $\sin a\cos b$ | $\dfrac{1}{2}\big[\sin(a + b) + \sin(a - b)\big]$ |

| Somme | Produit |
|---|---|
| $\cos p + \cos q$ | $2\cos\dfrac{p + q}{2}\cos\dfrac{p - q}{2}$ |
| $\cos p - \cos q$ | $-2\sin\dfrac{p + q}{2}\sin\dfrac{p - q}{2}$ |
| $\sin p + \sin q$ | $2\sin\dfrac{p + q}{2}\cos\dfrac{p - q}{2}$ |
| $\sin p - \sin q$ | $2\cos\dfrac{p + q}{2}\sin\dfrac{p - q}{2}$ |

::: propriete Écriture $a\cos x + b\sin x$
Pour $(a, b) \neq (0, 0)$, on pose $R = \sqrt{a^2 + b^2}$ et on choisit $\varphi$ tel que $\cos\varphi = \dfrac{a}{R}$ et $\sin\varphi = \dfrac{b}{R}$. Alors
$$a\cos x + b\sin x = R\cos(x - \varphi)$$
:::
