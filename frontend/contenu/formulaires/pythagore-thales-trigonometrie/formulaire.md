---
{
  "slug": "pythagore-thales-trigonometrie",
  "titre": "Pythagore, Thalès et trigonométrie",
  "titreCourt": "Pythagore, Thalès, trigonométrie",
  "titreSeo": "Pythagore, Thalès et trigonométrie : formulaire du collège",
  "description": "Les formules de Pythagore, de Thalès et de la trigonométrie (cos, sin, tan, SOH CAH TOA) pour calculer longueurs et angles, avec schémas et exemples.",
  "chapo": "Le théorème de Pythagore et sa réciproque, le théorème de Thalès dans ses deux configurations, le cosinus, le sinus et la tangente dans le triangle rectangle, avec la rédaction attendue.",
  "resume": "Pythagore, Thalès, SOH CAH TOA",
  "vignette": "pythagore_carres",
  "theme": "Géométrie",
  "niveaux": ["Collège"],
  "ordre": 3,
  "publie": "2026-11-09",
  "modifie": "2026-11-09",
  "motsCles": ["théorème de Pythagore", "formule de Pythagore", "réciproque de Pythagore", "théorème de Thalès", "formule de Thalès", "SOH CAH TOA", "cosinus sinus tangente", "trigonométrie triangle rectangle"],
  "figures": [
    { "nom": "pythagore_carres", "alt": "Triangle ABC rectangle en A avec un carré construit sur chaque côté : l’aire du grand carré BC² est égale à la somme des aires AB² et AC²." },
    { "nom": "thales_configurations", "alt": "Les deux configurations de Thalès : triangles emboîtés, avec M sur [AB] et N sur [AC], et configuration papillon, avec M et N de l’autre côté de A ; dans les deux cas, (MN) est parallèle à (BC)." },
    { "nom": "triangle_trigo", "alt": "Triangle ABC rectangle en B avec l’angle α en A : l’hypoténuse [AC], le côté adjacent à α [AB] et le côté opposé à α [BC]." }
  ],
  "chapitresLies": [
    "4e/theoreme-de-pythagore",
    "3e/theoreme-de-pythagore",
    "4e/theoreme-de-thales-triangles-emboites",
    "3e/theoreme-de-thales-et-triangles-semblables",
    "4e/cosinus-dans-le-triangle-rectangle",
    "3e/trigonometrie-du-triangle-rectangle"
  ],
  "faq": [
    ["Quelle est la formule de Pythagore ?", "Dans un triangle ABC rectangle en A, le carré de l’hypoténuse est égal à la somme des carrés des deux autres côtés : BC² = AB² + AC²."],
    ["Quand utiliser Pythagore ou la trigonométrie ?", "Pythagore relie les trois côtés d’un triangle rectangle : on l’utilise quand on connaît deux côtés. La trigonométrie relie un angle et deux côtés : on l’utilise dès qu’un angle est donné ou demandé."],
    ["Quelle est la formule de Thalès ?", "Si M est sur (AB), N sur (AC) et (MN) parallèle à (BC), alors AM/AB = AN/AC = MN/BC."],
    ["Que signifie SOH CAH TOA ?", "C’est un moyen de retenir les formules : Sinus = Opposé / Hypoténuse, Cosinus = Adjacent / Hypoténuse, Tangente = Opposé / Adjacent."],
    ["Comment montrer qu’un triangle est rectangle ?", "On calcule le carré du plus grand côté et la somme des carrés des deux autres. S’ils sont égaux, le triangle est rectangle, d’après la réciproque du théorème de Pythagore."]
  ]
}
---
<!-- optitab:1 -->
## I. Théorème de Pythagore {Collège}

[IMAGE_1]

::: theoreme Théorème de Pythagore
Si le triangle $ABC$ est rectangle en $A$, alors :
$$BC^2 = AB^2 + AC^2$$
L’hypoténuse $[BC]$ est le côté opposé à l’angle droit : c’est le plus long.
:::

| Je cherche | Formule |
|---|---|
| L’hypoténuse | $BC = \sqrt{AB^2 + AC^2}$ |
| Un côté de l’angle droit | $AB = \sqrt{BC^2 - AC^2}$ |

::: exemple $ABC$ rectangle en $A$, avec $AB = 6$ cm et $AC = 8$ cm
$BC^2 = 6^2 + 8^2 = 36 + 64 = 100$, donc $BC = \sqrt{100} = 10$ cm.
:::

::: propriete Réciproque et contraposée
- Si $BC^2 = AB^2 + AC^2$, alors le triangle $ABC$ est rectangle en $A$.
- Si $BC^2 \neq AB^2 + AC^2$, où $[BC]$ est le plus grand côté, alors le triangle n’est pas rectangle.
:::

Les **triplets pythagoriciens** donnent des triangles rectangles à côtés entiers :

| Côtés de l’angle droit | Hypoténuse | Vérification |
|---|---|---|
| $3$ et $4$ | $5$ | $9 + 16 = 25$ |
| $5$ et $12$ | $13$ | $25 + 144 = 169$ |
| $8$ et $15$ | $17$ | $64 + 225 = 289$ |
| $7$ et $24$ | $25$ | $49 + 576 = 625$ |
| $20$ et $21$ | $29$ | $400 + 441 = 841$ |

Tous leurs multiples conviennent aussi : $6$, $8$ et $10$, ou $9$, $12$ et $15$.

| Longueur utile | Formule |
|---|---|
| Diagonale d’un carré de côté $a$ | $a\sqrt{2}$ |
| Diagonale d’un rectangle $L \times \ell$ | $\sqrt{L^2 + \ell^2}$ |
| Hauteur d’un triangle équilatéral de côté $a$ | $\dfrac{a\sqrt{3}}{2}$ |
| Diagonale d’un cube d’arête $a$ | $a\sqrt{3}$ |

## II. Théorème de Thalès {Collège}

[IMAGE_2]

::: theoreme Théorème de Thalès
Les points $A$, $M$, $B$ sont alignés, ainsi que $A$, $N$, $C$. Si les droites $(MN)$ et $(BC)$ sont parallèles, alors :
$$\frac{AM}{AB} = \frac{AN}{AC} = \frac{MN}{BC}$$
:::

::: exemple $AM = 3$, $AB = 5$, $AN = 4{,}2$ et $BC = 6$, avec $(MN) \parallel (BC)$
D’après le théorème de Thalès :
$$\frac{3}{5} = \frac{4{,}2}{AC} = \frac{MN}{6}$$
Donc $AC = \dfrac{5 \times 4{,}2}{3} = 7$ et $MN = \dfrac{3 \times 6}{5} = 3{,}6$.
:::

::: propriete Réciproque
Si $\dfrac{AM}{AB} = \dfrac{AN}{AC}$ et si les points $A$, $M$, $B$ et $A$, $N$, $C$ sont dans le même ordre, alors $(MN)$ et $(BC)$ sont parallèles.
:::

::: attention Erreur fréquente
On n’écrit les rapports de Thalès qu’après avoir justifié le parallélisme. Chaque rapport compare un côté du petit triangle au côté correspondant du grand triangle, toujours dans le même ordre.
:::

## III. Trigonométrie dans le triangle rectangle {Collège}

[IMAGE_3]

| Rapport | Sur la figure | En mots |
|---|---|---|
| Cosinus | $\cos \alpha = \dfrac{AB}{AC}$ | adjacent sur hypoténuse |
| Sinus | $\sin \alpha = \dfrac{BC}{AC}$ | opposé sur hypoténuse |
| Tangente | $\tan \alpha = \dfrac{BC}{AB}$ | opposé sur adjacent |

::: retenir SOH CAH TOA
**S**inus $=$ **O**pposé sur **H**ypoténuse, **C**osinus $=$ **A**djacent sur **H**ypoténuse, **T**angente $=$ **O**pposé sur **A**djacent.
:::

| Angle | $30°$ | $45°$ | $60°$ |
|---|---|---|---|
| $\cos$ | $\dfrac{\sqrt{3}}{2}$ | $\dfrac{\sqrt{2}}{2}$ | $\dfrac{1}{2}$ |
| $\sin$ | $\dfrac{1}{2}$ | $\dfrac{\sqrt{2}}{2}$ | $\dfrac{\sqrt{3}}{2}$ |
| $\tan$ | $\dfrac{\sqrt{3}}{3}$ | $1$ | $\sqrt{3}$ |

::: exemple Calculer une longueur
Dans le triangle de la figure, $AC = 10$ cm et $\alpha = 35°$ :
$$AB = AC \times \cos \alpha = 10 \times \cos 35° \approx 8{,}19 \text{ cm}$$
:::

::: exemple Calculer un angle
Si $AB = 4$ cm et $AC = 5$ cm, alors $\cos \alpha = \dfrac{4}{5} = 0{,}8$. Avec la touche $\cos^{-1}$ de la calculatrice (en degrés), $\alpha \approx 36{,}9°$.
:::

::: propriete Relations à connaître
$$\cos^2 \alpha + \sin^2 \alpha = 1 \qquad \tan \alpha = \frac{\sin \alpha}{\cos \alpha}$$
Pour un angle aigu, $\cos \alpha$ et $\sin \alpha$ sont compris entre $0$ et $1$.
:::

## IV. Quel outil choisir ? {Collège}

| Situation | Outil |
|---|---|
| Triangle rectangle, deux côtés connus, on cherche le troisième | Pythagore |
| Prouver qu’un triangle est rectangle (ou non) | réciproque ou contraposée de Pythagore |
| Deux droites parallèles coupées par deux sécantes | Thalès |
| Prouver que deux droites sont parallèles | réciproque de Thalès |
| Triangle rectangle avec un angle connu ou cherché | cosinus, sinus ou tangente |

::: conseil Agrandissement et réduction
Dans un agrandissement ou une réduction de rapport $k$, les longueurs sont multipliées par $k$, les aires par $k^2$ et les volumes par $k^3$. Les angles ne changent pas.
:::
