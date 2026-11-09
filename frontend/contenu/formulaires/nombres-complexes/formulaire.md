---
{
  "slug": "nombres-complexes",
  "titre": "Nombres complexes",
  "titreCourt": "Nombres complexes",
  "titreSeo": "Nombres complexes : formulaire complet (module, argument, Euler)",
  "description": "Toutes les formules des nombres complexes : forme algébrique, conjugué, module, argument, forme exponentielle, Euler, Moivre, racines n-ièmes, géométrie.",
  "chapo": "Les formules des nombres complexes réunies : forme algébrique et conjugué, module et argument, forme exponentielle, formules d’Euler et de Moivre, équations, racines de l’unité et géométrie.",
  "resume": "Module, argument, exponentielle, Euler, Moivre",
  "vignette": "plan_complexe",
  "theme": "Algèbre",
  "niveaux": ["Lycée", "Supérieur"],
  "ordre": 23,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["nombres complexes formules", "formulaire nombres complexes", "module et argument", "forme exponentielle", "formule d'Euler", "formule de Moivre", "conjugué d'un nombre complexe", "racines n-ièmes de l'unité"],
  "figures": [
    { "nom": "plan_complexe", "alt": "Point M d’affixe z = a + ib dans le plan complexe, à la distance r = |z| de l’origine, l’angle θ = arg z étant mesuré depuis l’axe des réels ; son conjugué est le symétrique de M par rapport à cet axe." },
    { "nom": "racines_unite", "alt": "Les six racines sixièmes de l’unité, placées sur le cercle de rayon 1 aux angles 0, π/3, 2π/3, π, 4π/3 et 5π/3, forment un hexagone régulier." }
  ],
  "chapitresLies": [
    "terminale/nombres-complexes",
    "premiere/equations-fonctions-polynomes-du-second-degre"
  ],
  "faq": [
    ["Comment calculer le module d’un nombre complexe ?", "Pour z = a + ib, le module vaut |z| = √(a² + b²). C’est la distance entre l’origine et le point d’affixe z. Par exemple, |3 + 4i| = √(9 + 16) = 5."],
    ["Comment trouver l’argument d’un nombre complexe ?", "On calcule r = |z|, puis on cherche θ tel que cos θ = a/r et sin θ = b/r. Par exemple, pour 1 + i, r = √2 et cos θ = sin θ = √2/2, donc θ = π/4."],
    ["Quelle est la formule d’Euler ?", "e^{iθ} = cos θ + i sin θ. On en déduit cos θ = (e^{iθ} + e^{−iθ})/2 et sin θ = (e^{iθ} − e^{−iθ})/(2i), ainsi que e^{iπ} = −1."],
    ["À quoi sert le conjugué ?", "Il permet d’écrire un quotient sous forme algébrique : on multiplie le numérateur et le dénominateur par le conjugué du dénominateur, car z × z̄ = a² + b² est un réel."]
  ]
}
---
<!-- optitab:1 -->
## I. Forme algébrique {Lycée}

::: definition Forme algébrique
Tout nombre complexe s’écrit de façon unique $z = a + \mathrm{i}b$, avec $a$ et $b$ réels et $\mathrm{i}^2 = -1$. On note $a = \operatorname{Re}(z)$ (partie réelle) et $b = \operatorname{Im}(z)$ (partie imaginaire).
:::

| Opération | Formule |
|---|---|
| Somme | $(a + \mathrm{i}b) + (c + \mathrm{i}d) = (a + c) + \mathrm{i}(b + d)$ |
| Produit | $(a + \mathrm{i}b)(c + \mathrm{i}d) = (ac - bd) + \mathrm{i}(ad + bc)$ |
| Conjugué | $\overline{z} = a - \mathrm{i}b$ |
| Produit par le conjugué | $z\,\overline{z} = a^2 + b^2$ |
| Inverse ($z \neq 0$) | $\dfrac{1}{z} = \dfrac{\overline{z}}{a^2 + b^2}$ |

::: exemple Écrire $\dfrac{1 + 2\mathrm{i}}{3 - \mathrm{i}}$ sous forme algébrique
On multiplie en haut et en bas par le conjugué $3 + \mathrm{i}$ :
$$\frac{(1 + 2\mathrm{i})(3 + \mathrm{i})}{(3 - \mathrm{i})(3 + \mathrm{i})} = \frac{1 + 7\mathrm{i}}{10} = \frac{1}{10} + \frac{7}{10}\,\mathrm{i}$$
:::

| Puissances de $\mathrm{i}$ | Valeur |
|---|---|
| $\mathrm{i}^2$ | $-1$ |
| $\mathrm{i}^3$ | $-\mathrm{i}$ |
| $\mathrm{i}^4$ | $1$ |
| $\mathrm{i}^{4k + r}$ | $\mathrm{i}^{r}$ |

## II. Conjugué {Lycée}

| Propriété | Formule |
|---|---|
| Somme et produit | $\overline{z + w} = \overline{z} + \overline{w}$ et $\overline{z w} = \overline{z}\;\overline{w}$ |
| Quotient et puissance | $\overline{\left(\dfrac{z}{w}\right)} = \dfrac{\overline{z}}{\overline{w}}$ et $\overline{z^n} = \overline{z}^{\,n}$ |
| Partie réelle | $z + \overline{z} = 2\operatorname{Re}(z)$ |
| Partie imaginaire | $z - \overline{z} = 2\mathrm{i}\operatorname{Im}(z)$ |
| $z$ réel | $\overline{z} = z$ |
| $z$ imaginaire pur | $\overline{z} = -z$ |

## III. Module et argument {Lycée}

[IMAGE_1]

::: formule Module et argument de $z = a + \mathrm{i}b \neq 0$
$$r = \lvert z \rvert = \sqrt{a^2 + b^2}$$
$$\cos\theta = \frac{a}{r} \qquad \sin\theta = \frac{b}{r}$$
:::

| Module | Formule |
|---|---|
| Produit | $\lvert zw \rvert = \lvert z \rvert\,\lvert w \rvert$ |
| Quotient | $\left\lvert \dfrac{z}{w} \right\rvert = \dfrac{\lvert z \rvert}{\lvert w \rvert}$ |
| Puissance | $\lvert z^n \rvert = \lvert z \rvert^n$ |
| Conjugué | $\lvert \overline{z} \rvert = \lvert z \rvert$ |

| Argument (à $2\pi$ près) | Formule |
|---|---|
| Produit | $\arg(zw) = \arg z + \arg w$ |
| Quotient | $\arg\dfrac{z}{w} = \arg z - \arg w$ |
| Puissance | $\arg(z^n) = n\arg z$ |
| Conjugué | $\arg \overline{z} = -\arg z$ |

::: propriete Inégalité triangulaire
$$\lvert z + w \rvert \leqslant \lvert z \rvert + \lvert w \rvert$$
:::

## IV. Forme exponentielle {Lycée}

::: definition Notation exponentielle
$$\mathrm{e}^{\mathrm{i}\theta} = \cos\theta + \mathrm{i}\sin\theta \qquad z = r\,\mathrm{e}^{\mathrm{i}\theta}$$
:::

| Règle | Formule |
|---|---|
| Produit | $r\,\mathrm{e}^{\mathrm{i}\theta} \times r'\,\mathrm{e}^{\mathrm{i}\theta'} = r r'\,\mathrm{e}^{\mathrm{i}(\theta + \theta')}$ |
| Quotient | $\dfrac{r\,\mathrm{e}^{\mathrm{i}\theta}}{r'\,\mathrm{e}^{\mathrm{i}\theta'}} = \dfrac{r}{r'}\,\mathrm{e}^{\mathrm{i}(\theta - \theta')}$ |
| Puissance | $\left(r\,\mathrm{e}^{\mathrm{i}\theta}\right)^n = r^n\,\mathrm{e}^{\mathrm{i}n\theta}$ |
| Conjugué | $\overline{r\,\mathrm{e}^{\mathrm{i}\theta}} = r\,\mathrm{e}^{-\mathrm{i}\theta}$ |

| Nombre | Forme exponentielle |
|---|---|
| $1 + \mathrm{i}$ | $\sqrt{2}\,\mathrm{e}^{\mathrm{i}\pi/4}$ |
| $1 - \mathrm{i}$ | $\sqrt{2}\,\mathrm{e}^{-\mathrm{i}\pi/4}$ |
| $\sqrt{3} + \mathrm{i}$ | $2\,\mathrm{e}^{\mathrm{i}\pi/6}$ |
| $1 + \mathrm{i}\sqrt{3}$ | $2\,\mathrm{e}^{\mathrm{i}\pi/3}$ |
| $\mathrm{i}$ | $\mathrm{e}^{\mathrm{i}\pi/2}$ |
| $-1$ | $\mathrm{e}^{\mathrm{i}\pi}$ |

::: retenir Formules d’Euler et de Moivre
$$\cos\theta = \frac{\mathrm{e}^{\mathrm{i}\theta} + \mathrm{e}^{-\mathrm{i}\theta}}{2} \qquad \sin\theta = \frac{\mathrm{e}^{\mathrm{i}\theta} - \mathrm{e}^{-\mathrm{i}\theta}}{2\mathrm{i}}$$
$$(\cos\theta + \mathrm{i}\sin\theta)^n = \cos(n\theta) + \mathrm{i}\sin(n\theta)$$
:::

## V. Équations {Lycée}

| Équation | Solutions dans $\mathbb{C}$ |
|---|---|
| $z^2 = a$, $a > 0$ | $\sqrt{a}$ et $-\sqrt{a}$ |
| $z^2 = a$, $a < 0$ | $\mathrm{i}\sqrt{-a}$ et $-\mathrm{i}\sqrt{-a}$ |
| $az^2 + bz + c = 0$, $\Delta < 0$ | $\dfrac{-b - \mathrm{i}\sqrt{-\Delta}}{2a}$ et $\dfrac{-b + \mathrm{i}\sqrt{-\Delta}}{2a}$ |

Les coefficients $a$, $b$, $c$ sont réels. Pour $\Delta < 0$, les deux solutions sont conjuguées.

::: exemple Résoudre $z^2 - 2z + 5 = 0$
$\Delta = 4 - 20 = -16$, donc $z = \dfrac{2 \pm 4\mathrm{i}}{2}$, soit $z = 1 - 2\mathrm{i}$ ou $z = 1 + 2\mathrm{i}$.
:::

[IMAGE_2]

::: propriete Racines $n$-ièmes de l’unité
Les solutions de $z^n = 1$ sont les $n$ nombres $\mathrm{e}^{2\mathrm{i}k\pi/n}$, pour $k$ allant de $0$ à $n - 1$. Leur somme est nulle (pour $n \geqslant 2$) et leurs points forment un polygone régulier.
:::

## VI. Géométrie {Lycée}

$A$, $B$, $C$, $D$ ont pour affixes $z_A$, $z_B$, $z_C$, $z_D$.

| Objet | Formule |
|---|---|
| Distance $AB$ | $\lvert z_B - z_A \rvert$ |
| Milieu de $[AB]$ | $\dfrac{z_A + z_B}{2}$ |
| Angle $\left(\vec{u}, \overrightarrow{AB}\right)$ | $\arg(z_B - z_A)$ |
| Angle $\left(\overrightarrow{AB}, \overrightarrow{CD}\right)$ | $\arg\dfrac{z_D - z_C}{z_B - z_A}$ |

| Propriété | Condition |
|---|---|
| $A$, $B$, $C$ alignés | $\dfrac{z_C - z_A}{z_B - z_A}$ réel |
| $(AB) \perp (AC)$ | $\dfrac{z_C - z_A}{z_B - z_A}$ imaginaire pur |

| Transformation | Écriture complexe |
|---|---|
| Translation de vecteur d’affixe $b$ | $z' = z + b$ |
| Rotation de centre $\Omega(\omega)$, d’angle $\theta$ | $z' - \omega = \mathrm{e}^{\mathrm{i}\theta}(z - \omega)$ |
| Homothétie de centre $\Omega(\omega)$, de rapport $k$ | $z' - \omega = k(z - \omega)$ |
