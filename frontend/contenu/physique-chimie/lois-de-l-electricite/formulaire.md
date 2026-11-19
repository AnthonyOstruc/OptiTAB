---
{
  "slug": "lois-de-l-electricite",
  "titre": "Électricité : toutes les lois et formules",
  "titreCourt": "Lois de l’électricité",
  "titreSeo": "Lois de l’électricité : formules, schémas et exemples",
  "description": "Toutes les lois de l’électricité, du collège à la Terminale : série et dérivation, loi d’Ohm, nœuds, mailles, puissance, effet Joule, condensateur RC.",
  "chapo": "Toutes les lois de l’électricité expliquées une à une, du collège à la Terminale. Pour chacune : l’énoncé, le schéma, le sens de chaque lettre avec son unité, un exemple corrigé et le piège à éviter.",
  "resume": "Série, dérivation, loi d’Ohm, nœuds et mailles, puissance, effet Joule, RC",
  "vignette": "noeud_maille",
  "theme": "Électricité",
  "niveaux": ["Collège", "Lycée"],
  "ordre": 2,
  "publie": "2026-11-18",
  "modifie": "2026-11-18",
  "motsCles": ["lois de l'électricité", "formules électricité", "loi des nœuds", "loi des mailles", "loi d'Ohm", "circuit en série", "circuit en dérivation", "loi d'additivité des tensions", "puissance électrique", "effet Joule", "rendement", "source réelle de tension", "condensateur", "circuit RC", "symboles électriques"],
  "figures": [
    { "nom": "symboles_electriques", "alt": "Symboles normalisés : pile (générateur), lampe, résistance, moteur, interrupteur ouvert, interrupteur fermé, diode, DEL, ampèremètre et voltmètre." },
    { "nom": "circuits_serie_derivation", "alt": "À gauche, un circuit en série : une pile et deux lampes L1 et L2 dans une seule boucle, avec la tension U du générateur, les tensions U1 et U2 des lampes et le même courant I partout. À droite, un circuit en dérivation : deux branches, l’une avec L1 parcourue par I1, l’autre avec L2 parcourue par I2, et le courant principal I." },
    { "nom": "mesures_ampere_volt", "alt": "Circuit avec une pile et une lampe L : l’ampèremètre A est branché en série dans la boucle, le voltmètre V est branché en dérivation aux bornes de la lampe." },
    { "nom": "noeud_maille", "alt": "À gauche, un nœud où arrive le courant I1 et d’où partent I2 et I3 : I1 = I2 + I3. À droite, une maille avec un générateur PN et deux résistances R1 et R2, les flèches de tension UPN, U1 et U2 : UPN = U1 + U2." },
    { "nom": "caracteristiques", "alt": "Caractéristiques tension-courant : celle d’une résistance est une droite qui passe par l’origine, celle d’une lampe est une courbe." },
    { "nom": "source_reelle", "alt": "Caractéristique d’une source réelle : une droite qui descend depuis E, la tension à vide. Elle coupe la droite d’une résistance au point de fonctionnement F, à 1 A et 3 V." },
    { "nom": "charge_condensateur", "alt": "Tension aux bornes d’un condensateur en fonction du temps : à la charge, elle monte vers E et atteint 63 % de E au bout de τ ; à la décharge, elle descend de E vers 0. La tangente à l’origine de la charge coupe la valeur E à t = τ." }
  ],
  "liees": [
    "physique-chimie/formules-physique-chimie-brevet",
    "physique-chimie/electrocinetique",
    "tables/puissances-de-10-prefixes"
  ],
  "faq": [
    ["Quelle est la loi des nœuds ?", "En un nœud d’un circuit, la somme des intensités des courants qui arrivent est égale à la somme des intensités des courants qui en partent. Par exemple, si 0,40 A arrive dans un nœud et que 0,15 A part dans une branche, l’autre branche emporte 0,25 A."],
    ["Quelle est la loi des mailles ?", "Dans une maille (une boucle fermée), la somme algébrique des tensions est nulle. En pratique, la tension du générateur est égale à la somme des tensions des récepteurs de la maille : UPN = U1 + U2."],
    ["Quelle est la différence entre un circuit en série et un circuit en dérivation ?", "En série, les dipôles forment une seule boucle : l’intensité est la même partout et les tensions s’additionnent. En dérivation, il y a plusieurs boucles : la tension est la même aux bornes de chaque branche et les intensités des branches s’additionnent."],
    ["Qu’est-ce que l’effet Joule ?", "C’est l’échauffement d’un conducteur traversé par un courant : l’énergie électrique est convertie en énergie thermique. Pour une résistance R parcourue par un courant I, la puissance dissipée vaut P = R × I². Il est utile dans un radiateur, mais c’est une perte dans un moteur ou un câble."],
    ["Comment calculer le rendement d’un appareil électrique ?", "On divise la puissance utile par la puissance reçue : η = Putile / Preçue. Un moteur qui reçoit 120 W et fournit 90 W de puissance mécanique a un rendement de 90 / 120 = 0,75, soit 75 %. Le rendement est toujours inférieur à 1."],
    ["Que représente la constante de temps τ = RC ?", "C’est la durée caractéristique de la charge ou de la décharge d’un condensateur à travers une résistance. Au bout de τ, le condensateur est chargé à 63 % ; au bout de 5τ, il est chargé à plus de 99 %. Avec R = 10 kΩ et C = 100 µF, τ = 1 s."]
  ]
}
---
<!-- optitab:1 -->
::: conseil Par où commencer ?
- **Au collège** : parties I à VI.
- **En Seconde** : ajoute les parties VII et VIII.
- **En Première** : parties IX à XI.
- **En Terminale** : partie XII.
- **En prépa ou en école d’ingénieur** : le formulaire d’électrocinétique (lien en bas de page).
:::

## I. Les grandeurs électriques et les symboles {Collège}

| Grandeur | Unité | Se mesure avec |
|---|---|---|
| Intensité $I$ | ampère (A) | un ampèremètre |
| Tension $U$ | volt (V) | un voltmètre |
| Résistance $R$ | ohm (Ω) | un ohmmètre |
| Puissance $P$ | watt (W) | un wattmètre |
| Énergie $E$ | joule (J) ou kWh | un compteur |

[IMAGE_1]

::: definition Le sens conventionnel du courant
À l’extérieur du générateur, le courant va de la borne $+$ vers la borne $-$. Les électrons, eux, se déplacent dans le sens inverse.
:::

## II. Circuit en série et circuit en dérivation {Collège}

[IMAGE_2]

| Loi | En série (une seule boucle) | En dérivation (plusieurs boucles) |
|---|---|---|
| Intensité | **unicité** : la même partout | **additivité** : $I = I_1 + I_2$ |
| Tension | **additivité** : $U = U_1 + U_2$ | **unicité** : $U = U_1 = U_2$ |

::: exemple
- En série, un générateur de 9,0 V alimente deux lampes. La tension aux bornes de la première vaut 5,5 V, donc celle de la seconde vaut $9{,}0 - 5{,}5 = 3{,}5$ V.
- En dérivation, le courant principal vaut 0,80 A et celui de la branche 1 vaut 0,30 A, donc celui de la branche 2 vaut $0{,}80 - 0{,}30 = 0{,}50$ A.
:::

::: remarque
En série, si une lampe grille, le circuit est ouvert : tout s’éteint. En dérivation, chaque branche fonctionne seule : c’est le montage des prises et des lampes d’une maison.
:::

## III. Mesurer une intensité et une tension {Collège}

[IMAGE_3]

| Appareil | Branchement | Bornes |
|---|---|---|
| Ampèremètre (intensité) | en série, dans la boucle | A (ou mA) et COM |
| Voltmètre (tension) | en dérivation, aux bornes du dipôle | V et COM |

::: conseil Bien utiliser un multimètre
- On commence par le plus grand calibre, puis on descend jusqu’au plus petit calibre supérieur à la valeur mesurée.
- La borne COM est reliée du côté de la borne $-$ du générateur. Si la valeur affichée est négative, les branchements sont inversés.
:::

## IV. La loi d’Ohm {Collège}

::: formule Loi d’Ohm (pour une résistance)
$$U = R \times I$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $U$ | tension aux bornes de la résistance | volt (V) |
| $R$ | résistance | ohm (Ω) |
| $I$ | intensité du courant qui la traverse | ampère (A) |

Pour retrouver les autres grandeurs : $I = \dfrac{U}{R}$ et $R = \dfrac{U}{I}$.

::: exemple
Une résistance de 47 Ω est soumise à une tension de 4,7 V. L’intensité du courant vaut $I = \dfrac{4{,}7}{47} = 0{,}10$ A, soit 100 mA.
:::

::: attention Les bonnes unités
On convertit les mA en A et les kΩ en Ω avant de calculer. La loi d’Ohm ne s’applique qu’à un conducteur ohmique (une résistance), pas à une lampe ni à une diode.
:::

::: remarque Associer des résistances
Ces formules découlent des lois des circuits : en série, les résistances s’ajoutent, $R = R_1 + R_2$ ; en dérivation, $1/R = 1/R_1 + 1/R_2$, soit $R = \dfrac{R_1 \times R_2}{R_1 + R_2}$. Avec 100 Ω et 220 Ω : 320 Ω en série, environ 69 Ω en dérivation.
:::

## V. La puissance et l’énergie électriques {Collège}

::: formule Puissance électrique
$$P = U \times I$$
:::

::: formule Énergie électrique
$$E = P \times t$$
:::

| Puissance $P$ en… | Durée $t$ en… | Énergie $E$ en… |
|---|---|---|
| watts (W) | secondes (s) | joules (J) |
| kilowatts (kW) | heures (h) | kilowattheures (kWh) |

::: exemple
Un écran branché sur le secteur (230 V) est traversé par 0,20 A : $P = 230 \times 0{,}20 = 46$ W.

Un four de 2 500 W, soit 2,5 kW, fonctionne pendant 1 h 30 min, soit 1,5 h : $E = 2{,}5 \times 1{,}5 = 3{,}75$ kWh, soit $3{,}75 \times 3{,}6 \times 10^{6} = 1{,}35 \times 10^{7}$ J.
:::

| Appareil | Puissance (ordre de grandeur) |
|---|---|
| Ampoule à DEL | 10 W |
| Ordinateur portable | 50 W |
| Bouilloire | 2 000 W |
| TGV | 10 MW |
| Réacteur de centrale nucléaire | 1 000 MW |

::: retenir
- 1 kWh = 3 600 000 J $= 3{,}6 \times 10^{6}$ J.
- La puissance est l’énergie transférée chaque seconde : 1 W = 1 J/s.
:::

## VI. La sécurité électrique {Collège}

| Danger ou protection | À savoir |
|---|---|
| Court-circuit | Deux bornes reliées par un fil sans dipôle : l’intensité devient très grande, les fils chauffent, risque d’incendie. |
| Fusible et disjoncteur | Ils ouvrent le circuit quand l’intensité dépasse une valeur fixée : ils protègent l’installation. |
| Disjoncteur différentiel | Il coupe le courant dès qu’une partie du courant fuit, par exemple à travers une personne : il protège les personnes. |
| Prise de terre | Elle évacue vers le sol le courant de fuite d’un appareil à carcasse métallique. |
| Tension dangereuse | Au-delà d’environ 50 V (25 V en milieu humide), une tension peut être dangereuse pour le corps humain. Le secteur délivre 230 V. |

## VII. La loi des nœuds et la loi des mailles {Lycée}

*Programme de Seconde.*

[IMAGE_4]

::: definition Tension et flèche de tension
La tension entre deux points A et B est la différence de leurs potentiels : $U_{AB} = V_A - V_B$. On la représente par une flèche dirigée de B vers A. Pour un récepteur, la flèche de tension est opposée au sens du courant ; pour un générateur, elle est dans le même sens.
:::

::: formule Loi des nœuds
$$\sum I_{\text{arrivent}} = \sum I_{\text{partent}}$$
:::

::: formule Loi des mailles
$$\sum U = 0 \quad \text{en parcourant la maille}$$
:::

On parcourt la maille dans un sens choisi : une tension dont la flèche est dans le sens du parcours est comptée positivement, une tension de sens contraire négativement. Dans la maille du schéma : $U_{PN} - U_1 - U_2 = 0$, soit $U_{PN} = U_1 + U_2$.

::: exemple
- Nœud : $I_1 = 0{,}40$ A arrive, $I_2 = 0{,}15$ A part, donc $I_3 = 0{,}40 - 0{,}15 = 0{,}25$ A.
- Maille : $U_{PN} = 12$ V et $U_1 = 7{,}5$ V, donc $U_2 = 12 - 7{,}5 = 4{,}5$ V.
:::

## VIII. La caractéristique d’un dipôle et les capteurs {Lycée}

*Programme de Seconde.*

La **caractéristique** d’un dipôle est la courbe de la tension à ses bornes en fonction de l’intensité qui le traverse, $U = f(I)$.

[IMAGE_5]

| Dipôle | Caractéristique | Comportement |
|---|---|---|
| Résistance | droite qui passe par l’origine | ohmique : $U = R \times I$ |
| Lampe | courbe | non ohmique : sa résistance augmente quand le filament chauffe |

Pour une résistance, le **coefficient directeur** de la droite $U = f(I)$ est égal à $R$.

| Capteur résistif | Sa résistance… |
|---|---|
| Thermistance (CTN) | diminue quand la température augmente |
| Photorésistance | diminue quand la lumière augmente |

On les trouve par exemple dans les thermomètres électroniques et les éclairages automatiques.

On relie la grandeur mesurée à la résistance du capteur grâce à une **courbe d’étalonnage**, tracée à partir de mesures.

## IX. L’intensité, un débit de charges {Lycée}

*Programme de Première.*

::: formule Intensité d’un courant continu
$$I = \dfrac{Q}{\Delta t}$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $I$ | intensité | ampère (A) |
| $Q$ | charge électrique qui traverse une section du circuit | coulomb (C) |
| $\Delta t$ | durée | seconde (s) |

La charge d’un électron vaut $-e$, avec $e = 1{,}6 \times 10^{-19}$ C. Le nombre d’électrons qui transportent la charge $Q$ est $N = \dfrac{Q}{e}$.

::: exemple
Un courant de 0,50 A circule pendant 1 min, soit 60 s : $Q = 0{,}50 \times 60 = 30$ C, ce qui correspond à $N = 30/(1{,}6 \times 10^{-19}) \approx 1{,}9 \times 10^{20}$ électrons.
:::

::: remarque
La capacité d’une batterie s’exprime souvent en milliampères-heures : 1 mAh = 0,001 A × 3 600 s = 3,6 C.
:::

## X. La source réelle de tension {Lycée}

*Programme de Première.*

Une source réelle se modélise par une source idéale de tension $E$ en série avec une résistance $r$.

::: formule Tension aux bornes d’une source réelle
$$U = E - r \times I$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $E$ | tension à vide (force électromotrice) | volt (V) |
| $r$ | résistance interne | ohm (Ω) |
| $I$ | intensité débitée | ampère (A) |

[IMAGE_6]

Le **point de fonctionnement** F est l’intersection de la caractéristique de la source et de celle du dipôle qu’elle alimente. Ici, avec une résistance de 3 Ω : $4{,}5 - 1{,}5\,I = 3\,I$, donc $I = 1$ A et $U = 3$ V.

::: exemple
Une pile de tension à vide $E = 4{,}5$ V et de résistance interne $r = 1{,}5$ Ω débite 0,20 A : $U = 4{,}5 - 1{,}5 \times 0{,}20 = 4{,}2$ V. Plus la pile débite, plus la tension à ses bornes baisse.
:::

## XI. Le bilan de puissance, l’effet Joule et le rendement {Lycée}

*Programme de Première.*

::: formule Effet Joule (puissance dissipée par une résistance)
$$P_J = R \times I^2$$
:::

Cette formule vient de $P = U \times I$ avec $U = R \times I$. L’énergie dissipée pendant $\Delta t$ vaut $E_J = R \times I^2 \times \Delta t$.

::: formule Bilan de puissance d’une source réelle
$$E \times I = U \times I + r \times I^2$$
:::

La source idéale fournit $E \times I$ ; le circuit reçoit $U \times I$ ; la résistance interne dissipe $r \times I^2$ par effet Joule.

::: formule Rendement d’un convertisseur
$$\eta = \dfrac{P_u}{P_r}$$
:::

$P_u$ est la puissance utile (celle qui sert), $P_r$ la puissance reçue. Le rendement $\eta$ (« êta ») n’a pas d’unité. Il est toujours inférieur à 1 : une partie de l’énergie est perdue, le plus souvent sous forme thermique.

::: exemple
- Pour la pile de la partie X ($E = 4{,}5$ V, $r = 1{,}5$ Ω, $I = 0{,}20$ A) : $E \times I = 0{,}90$ W ; $U \times I = 0{,}84$ W ; $r \times I^2 = 0{,}06$ W. On vérifie que $0{,}90 = 0{,}84 + 0{,}06$.
- Un moteur reçoit 120 W et fournit 90 W de puissance mécanique : $\eta = \dfrac{90}{120} = 0{,}75$, soit 75 %. Les 30 W restants sont perdus, surtout par effet Joule.
:::

## XII. Le condensateur et le circuit RC {Lycée}

*Programme de Terminale.*

::: formule Intensité en régime variable
$$i = \dfrac{\mathrm{d}q}{\mathrm{d}t}$$
:::

::: formule Charge d’un condensateur
$$q = C \times u_C$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $q$ | charge de l’armature | coulomb (C) |
| $C$ | capacité | farad (F) |
| $u_C$ | tension aux bornes du condensateur | volt (V) |

Les capacités usuelles vont du picofarad (pF) au millifarad (mF) ; les supercondensateurs atteignent plusieurs centaines de farads.

En charge par une source idéale de tension $E$ à travers une résistance $R$ (loi des mailles et $i = C\,\dfrac{\mathrm{d}u_C}{\mathrm{d}t}$) :

$$RC\,\dfrac{\mathrm{d}u_C}{\mathrm{d}t} + u_C = E$$

Avec $\tau = RC$ :

::: formule Charge (le condensateur part de 0)
$$\begin{aligned}
&\tau\,\dfrac{\mathrm{d}u_C}{\mathrm{d}t} + u_C = E \\
&u_C(t) = E\left(1 - \mathrm{e}^{-t/\tau}\right)
\end{aligned}$$
:::

::: formule Décharge (le condensateur part de E)
$$\begin{aligned}
&\tau\,\dfrac{\mathrm{d}u_C}{\mathrm{d}t} + u_C = 0 \\
&u_C(t) = E\,\mathrm{e}^{-t/\tau}
\end{aligned}$$
:::

[IMAGE_7]

::: retenir Le temps caractéristique
- $\tau = R \times C$, en secondes quand $R$ est en ohms et $C$ en farads.
- Au bout de $\tau$, le condensateur est chargé à 63 % ; au bout de $5\tau$, à plus de 99 % : on considère la charge terminée.
- La tangente à l’origine de la courbe de charge (en pointillés orange) atteint la valeur $E$ à l’instant $t = \tau$ : c’est une façon de lire $\tau$ sur une courbe.
:::

::: exemple
Avec $R = 10$ kΩ $= 1{,}0 \times 10^{4}$ Ω et $C = 100$ µF $= 1{,}0 \times 10^{-4}$ F : $\tau = 1{,}0 \times 10^{4} \times 1{,}0 \times 10^{-4} = 1{,}0$ s. Avec $E = 5{,}0$ V, la tension vaut environ $0{,}63 \times 5{,}0 \approx 3{,}2$ V au bout d’une seconde.
:::

Les **capteurs capacitifs** (écrans tactiles, accéléromètres des téléphones, détecteurs de niveau) mesurent une variation de capacité.

## XIII. Les conversions utiles {Collège}

| Grandeur | Conversions |
|---|---|
| Intensité | 1 A = 1 000 mA ; 1 mA = 1 000 µA |
| Résistance | 1 kΩ = 1 000 Ω ; 1 MΩ = 1 000 000 Ω |
| Capacité | 1 µF $= 10^{-6}$ F ; 1 nF $= 10^{-9}$ F ; 1 pF $= 10^{-12}$ F |
| Énergie | 1 kWh = 3 600 000 J |
| Charge | 1 mAh = 3,6 C |
| Durée | 1 h = 3 600 s ; 1 min = 60 s |

::: conseil Le bon réflexe
On convertit toujours dans les unités de base (A, V, Ω, F, s) avant de calculer, puis on écrit l’unité du résultat.
:::
