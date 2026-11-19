---
{
  "slug": "formules-physique-chimie-brevet",
  "titre": "Formules de physique-chimie du brevet",
  "titreCourt": "Formules du brevet",
  "titreSeo": "Formules de physique-chimie 3e : le formulaire du brevet",
  "description": "Toutes les formules de physique-chimie du brevet : vitesse, masse volumique, poids, loi d’Ohm, puissance, énergie, pH. Avec unités, exemples et schémas.",
  "chapo": "Les formules de physique-chimie du collège à connaître pour le brevet. Pour chacune : ce que veut dire chaque lettre et son unité, comment retrouver chaque grandeur, un exemple corrigé et le piège à éviter.",
  "resume": "Vitesse, masse volumique, poids, loi d’Ohm, énergie, son, pH",
  "vignette": "triangles_formules",
  "theme": "Brevet",
  "niveaux": ["Collège"],
  "ordre": 1,
  "publie": "2026-11-18",
  "modifie": "2026-11-18",
  "motsCles": ["formules physique chimie brevet", "formulaire physique chimie 3e", "formule de la vitesse", "formule masse volumique", "formule du poids", "loi d'Ohm", "formule puissance électrique", "formule énergie électrique", "énergie cinétique formule", "convertir km/h en m/s", "échelle de pH"],
  "figures": [
    { "nom": "triangles_formules", "alt": "Trois triangles pour retrouver une grandeur : d au-dessus de v et t pour la vitesse, U au-dessus de R et I pour la loi d’Ohm, E au-dessus de P et t pour l’énergie." },
    { "nom": "circuits_serie_derivation", "alt": "À gauche, un circuit en série : une pile et deux lampes L1 et L2 dans une seule boucle, parcourue par le même courant I. À droite, un circuit en dérivation : la pile alimente deux branches, l’une avec la lampe L1 parcourue par I1, l’autre avec la lampe L2 parcourue par I2." },
    { "nom": "echelle_ph", "alt": "Échelle de pH de 0 à 14 : de 0 à 7 la solution est acide (ions H+ majoritaires), à 7 elle est neutre, de 7 à 14 elle est basique (ions OH− majoritaires). Exemples : jus de citron vers 2, eau pure à 7, eau de Javel vers 12." }
  ],
  "liees": [
    "physique-chimie/lois-de-l-electricite",
    "tables/tableau-de-conversion",
    "tables/puissances-de-10-prefixes",
    "formulaires/produit-en-croix-proportionnalite"
  ],
  "faq": [
    ["Quelle est la formule de la vitesse ?", "La vitesse moyenne est la distance parcourue divisée par la durée du parcours : v = d / t. Avec d en mètres et t en secondes, v est en m/s ; avec d en kilomètres et t en heures, v est en km/h. Par exemple, 36 km en 1,5 h donnent 24 km/h."],
    ["Quelle est la différence entre la masse et le poids ?", "La masse, en kilogrammes, mesure la quantité de matière : elle est la même partout. Le poids, en newtons, est la force d’attraction exercée par l’astre : P = m × g. Une masse de 50 kg a un poids de 490 N sur Terre (g = 9,8 N/kg) et de 80 N sur la Lune (g = 1,6 N/kg)."],
    ["Quelle est la formule de la loi d’Ohm ?", "U = R × I, avec la tension U en volts, la résistance R en ohms et l’intensité I en ampères. On en déduit I = U / R et R = U / I. Il faut convertir les milliampères en ampères avant de calculer : 50 mA = 0,050 A."],
    ["Comment calculer l’énergie consommée par un appareil ?", "On multiplie sa puissance par la durée de fonctionnement : E = P × t. Avec P en kilowatts et t en heures, E est en kilowattheures (kWh). Un radiateur de 2 000 W, soit 2 kW, qui fonctionne 3 h consomme 2 × 3 = 6 kWh. Et 1 kWh = 3 600 000 J."],
    ["Comment convertir des km/h en m/s ?", "On divise par 3,6, car 1 km/h correspond à 1 000 m parcourus en 3 600 s. Par exemple, 90 km/h = 90 / 3,6 = 25 m/s. Pour passer des m/s aux km/h, on multiplie par 3,6."],
    ["Quelles formules faut-il apprendre par cœur pour le brevet ?", "Celles de la vitesse (v = d / t), de la masse volumique (ρ = m / V), du poids (P = m × g), de l’énergie cinétique (Ec = ½ × m × v²), de la loi d’Ohm (U = R × I), de la puissance (P = U × I) et de l’énergie (E = P × t), ainsi que les lois des circuits. La formule de la gravitation universelle est donnée dans le sujet : il faut seulement savoir l’utiliser."]
  ]
}
---
<!-- optitab:1 -->
## I. Toutes les formules en un coup d’œil {Collège}

| Grandeur | Formule | Unité du résultat |
|---|---|---|
| Vitesse | $v = \dfrac{d}{t}$ | m/s ou km/h |
| Masse volumique | $\rho = \dfrac{m}{V}$ | kg/m³ ou g/cm³ |
| Poids | $P = m \times g$ | newton (N) |
| Énergie cinétique | $E_c = \dfrac{1}{2} \times m \times v^2$ | joule (J) |
| Loi d’Ohm | $U = R \times I$ | volt (V) |
| Puissance électrique | $P = U \times I$ | watt (W) |
| Énergie | $E = P \times t$ | joule (J) ou kWh |
| Distance parcourue par un signal | $d = v \times t$ | mètre (m) |
| Fréquence | $f = \dfrac{1}{T}$ | hertz (Hz) |

::: conseil Comment lire chaque partie
Chaque formule est présentée de la même façon : la formule encadrée, le sens de chaque lettre avec son unité, la façon de retrouver les autres grandeurs, un exemple corrigé et le piège à éviter.
:::

## II. Retrouver la grandeur cherchée {Collège}

[IMAGE_1]

Dans une formule du type $a = b \times c$, on cache la grandeur cherchée dans le triangle :

- les deux grandeurs qui restent sont côte à côte : on les **multiplie**, par exemple $d = v \times t$ ;
- elles sont l’une au-dessus de l’autre : on **divise** celle du haut par celle du bas, par exemple $v = \dfrac{d}{t}$ ou $t = \dfrac{d}{v}$.

::: attention Les unités d’abord
Avant de remplacer les lettres par des nombres, on convertit chaque valeur dans l’unité attendue par la formule : mètres et secondes, kilogrammes, ampères… C’est la première cause d’erreur au brevet.
:::

## III. La vitesse {Collège}

::: formule Vitesse moyenne
$$v = \dfrac{d}{t}$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $v$ | vitesse moyenne | m/s (ou km/h) |
| $d$ | distance parcourue | m (ou km) |
| $t$ | durée du parcours | s (ou h) |

Pour retrouver les autres grandeurs : $d = v \times t$ et $t = \dfrac{d}{v}$.

::: exemple
Un cycliste parcourt 36 km en 1 h 30 min, soit 1,5 h. Sa vitesse moyenne est $v = \dfrac{36}{1{,}5} = 24$ km/h.
:::

::: attention Passer des km/h aux m/s
On divise par 3,6, car 1 km/h correspond à 1 000 m parcourus en 3 600 s. Ainsi, 24 km/h $= \dfrac{24}{3{,}6} \approx 6{,}7$ m/s. Pour passer des m/s aux km/h, on multiplie par 3,6.
:::

Une vitesse a une **direction**, un **sens** et une **valeur**. Selon l’évolution de sa valeur, le mouvement est :

| Mouvement | La valeur de la vitesse… |
|---|---|
| uniforme | reste la même |
| accéléré | augmente |
| ralenti | diminue |

## IV. La masse volumique {Collège}

::: formule Masse volumique
$$\rho = \dfrac{m}{V}$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $\rho$ (« rho ») | masse volumique | kg/m³ ou g/cm³ |
| $m$ | masse | kg ou g |
| $V$ | volume | m³, cm³ ou L |

Pour retrouver les autres grandeurs : $m = \rho \times V$ et $V = \dfrac{m}{\rho}$.

::: exemple
Un cube de 50 cm³ a une masse de 135 g. Sa masse volumique est $\rho = \dfrac{135}{50} = 2{,}7$ g/cm³, soit 2 700 kg/m³ : c’est de l’aluminium.
:::

| Matière | En kg/m³ | En g/cm³ |
|---|---|---|
| Air | 1,2 | 0,0012 |
| Glace | 920 | 0,92 |
| Eau liquide | 1 000 | 1 |
| Aluminium | 2 700 | 2,7 |
| Fer | 7 870 | 7,87 |
| Or | 19 300 | 19,3 |

Ces valeurs sont arrondies : la masse volumique varie un peu avec la température.

::: retenir
- 1 g/cm³ = 1 000 kg/m³ = 1 kg/L.
- Un objet flotte sur un liquide si sa masse volumique est plus petite que celle du liquide : la glace flotte sur l’eau.
:::

## V. Le poids et la masse {Collège}

::: formule Poids
$$P = m \times g$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $P$ | poids | newton (N) |
| $m$ | masse | kilogramme (kg) |
| $g$ | intensité de la pesanteur | N/kg |

| Lieu | Valeur de $g$ | Poids d’une masse de 50 kg |
|---|---|---|
| Terre | 9,8 N/kg | 490 N |
| Lune | 1,6 N/kg | 80 N |
| Mars | 3,7 N/kg | 185 N |

| Critère | Masse | Poids |
|---|---|---|
| Ce qu’elle mesure | la quantité de matière | l’attraction exercée par l’astre |
| Unité | kilogramme (kg) | newton (N) |
| Appareil de mesure | balance | dynamomètre |
| Change selon le lieu | non | oui |

::: attention Masse ou poids ?
Dans la vie courante, on dit « je pèse 50 kg » : c’est en réalité une masse. Le poids se mesure en newtons : 490 N sur Terre, mais seulement 80 N sur la Lune, pour la même masse.
:::

Une force se représente par une flèche qui indique son **point d’application**, sa **direction**, son **sens** et sa **valeur**. Le poids est vertical, dirigé vers le bas (vers le centre de la Terre).

## VI. La gravitation universelle {Collège}

Cette formule est **donnée dans le sujet** : il faut savoir l’utiliser, pas l’apprendre.

::: formule Force d’attraction gravitationnelle
$$F = G \times \dfrac{m_A \times m_B}{d^2}$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $F$ | force d’attraction entre les deux objets | N |
| $m_A$, $m_B$ | masses des deux objets | kg |
| $d$ | distance entre leurs centres | m |
| $G$ | constante de gravitation : $6{,}67 \times 10^{-11}$ | N·m²/kg² |

::: exemple
La Terre ($m_A = 5{,}97 \times 10^{24}$ kg) et la Lune ($m_B = 7{,}35 \times 10^{22}$ kg) sont à $d = 3{,}84 \times 10^{8}$ m l’une de l’autre. Elles s’attirent avec une force :
$$F = 6{,}67 \times 10^{-11} \times \dfrac{5{,}97 \times 10^{24} \times 7{,}35 \times 10^{22}}{\left(3{,}84 \times 10^{8}\right)^2}$$
soit environ $2{,}0 \times 10^{20}$ N.
:::

::: retenir
- Les deux objets s’attirent avec des forces de même valeur, de sens opposés.
- Plus les masses sont grandes, plus l’attraction est forte.
- Si la distance double, la force est divisée par $2^2 = 4$.
:::

## VII. L’énergie cinétique et la conservation de l’énergie {Collège}

::: formule Énergie cinétique (énergie due au mouvement)
$$E_c = \dfrac{1}{2} \times m \times v^2$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $E_c$ | énergie cinétique | joule (J) |
| $m$ | masse | kg |
| $v$ | vitesse | m/s |

::: exemple
Une voiture de 1 000 kg roule à 45 km/h, soit 12,5 m/s : $E_c = \dfrac{1}{2} \times 1\,000 \times 12{,}5^2 = 78\,125$ J. À 90 km/h, soit 25 m/s : $E_c = \dfrac{1}{2} \times 1\,000 \times 25^2 = 312\,500$ J, quatre fois plus.
:::

::: attention La vitesse en m/s, et au carré
On convertit la vitesse en m/s avant de calculer, et on n’oublie pas le carré. Quand la vitesse double, l’énergie cinétique est multipliée par 4 : c’est pourquoi la distance de freinage augmente très vite avec la vitesse.
:::

| Forme d’énergie | Elle est liée… |
|---|---|
| cinétique | au mouvement |
| potentielle de position | à l’altitude |
| thermique | à la température |
| électrique | au courant électrique |
| chimique | aux transformations chimiques |
| nucléaire | aux noyaux des atomes |
| lumineuse | à la lumière |

::: retenir Conservation de l’énergie
L’énergie ne se crée pas et ne disparaît pas : elle se transfère ou se convertit d’une forme en une autre. Lors d’une chute, l’énergie de position diminue et l’énergie cinétique augmente. Une partie est convertie en énergie thermique à cause des frottements.
:::

## VIII. Les lois des circuits électriques {Collège}

[IMAGE_2]

| Loi | En série | En dérivation |
|---|---|---|
| Intensité | la même partout : $I$ | $I = I_1 + I_2$ |
| Tension | $U = U_1 + U_2$ | la même pour chaque branche : $U = U_1 = U_2$ |

| Grandeur | Unité | Elle se mesure avec… |
|---|---|---|
| Intensité $I$ | ampère (A) | un ampèremètre, branché en série |
| Tension $U$ | volt (V) | un voltmètre, branché en dérivation |
| Résistance $R$ | ohm (Ω) | un ohmmètre, aux bornes du dipôle seul |

::: remarque
En série, si une lampe grille, le circuit est ouvert et l’autre lampe s’éteint. En dérivation, chaque branche fonctionne seule : c’est le montage des prises et des lampes d’une maison.
:::

## IX. La loi d’Ohm {Collège}

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
Une résistance de 220 Ω est traversée par un courant de 50 mA, soit 0,050 A. La tension à ses bornes est $U = 220 \times 0{,}050 = 11$ V.
:::

::: attention Les milliampères
On convertit les milliampères en ampères avant d’utiliser la loi d’Ohm : 50 mA = 0,050 A. La loi d’Ohm ne s’applique qu’à une résistance (un conducteur ohmique) : sa caractéristique, la tension en fonction de l’intensité, est une droite qui passe par l’origine.
:::

## X. La puissance et l’énergie électrique {Collège}

::: formule Puissance électrique
$$P = U \times I$$
:::

::: formule Énergie transférée pendant une durée $t$
$$E = P \times t$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $P$ | puissance | watt (W) |
| $U$ | tension | volt (V) |
| $I$ | intensité | ampère (A) |
| $E$ | énergie | joule (J) ou kWh |
| $t$ | durée | s ou h |

| Puissance $P$ en… | Durée $t$ en… | Énergie $E$ en… |
|---|---|---|
| watts (W) | secondes (s) | joules (J) |
| watts (W) | heures (h) | wattheures (Wh) |
| kilowatts (kW) | heures (h) | kilowattheures (kWh) |

::: exemple
Une lampe alimentée sous 12 V est traversée par 0,5 A : $P = 12 \times 0{,}5 = 6$ W.

Un radiateur de 2 000 W, soit 2 kW, fonctionne pendant 3 h : $E = 2 \times 3 = 6$ kWh, soit $6 \times 3{,}6 \times 10^{6} = 2{,}16 \times 10^{7}$ J. Avec un prix de 0,25 € le kWh (exemple), cela coûte $6 \times 0{,}25 = 1{,}50$ €.
:::

::: retenir
- 1 kWh = 3 600 000 J $= 3{,}6 \times 10^{6}$ J.
- La puissance est l’énergie transférée chaque seconde : 1 W = 1 J/s.
:::

## XI. La lumière et le son {Collège}

| Propriété | Lumière | Son |
|---|---|---|
| Vitesse dans l’air | environ 300 000 km/s, soit $3 \times 10^{8}$ m/s | environ 340 m/s |
| Dans le vide | se propage | ne se propage pas |
| Dans l’eau | environ 225 000 km/s | environ 1 500 m/s |

::: formule Distance parcourue par un signal
$$d = v \times t$$
:::

::: exemple
Pendant un orage, on entend le tonnerre 3 s après avoir vu l’éclair. La lumière arrive presque instantanément ; le son a parcouru $d = 340 \times 3 = 1\,020$ m. L’orage est à environ 1 km.
:::

::: definition L’année-lumière
C’est la distance parcourue par la lumière en une année : 1 al $\approx 9{,}46 \times 10^{12}$ km, près de 10 000 milliards de kilomètres. C’est une distance, pas une durée.
:::

::: formule Fréquence d’un son
$$f = \dfrac{1}{T}$$
:::

La fréquence $f$, en hertz (Hz), est le nombre de vibrations par seconde ; la période $T$, en secondes (s), est la durée d’une vibration. Par exemple, pour $T = 0{,}002$ s, $f = \dfrac{1}{0{,}002} = 500$ Hz.

| Son | Fréquence | Exemple |
|---|---|---|
| Infrason | moins de 20 Hz | séismes, cris des éléphants |
| Son audible par l’être humain | de 20 Hz à 20 000 Hz | voix, musique |
| Ultrason | plus de 20 000 Hz | échographie, sonar, chauves-souris |

## XII. Le pH, les atomes et les ions {Collège}

[IMAGE_3]

| pH | La solution est… | Ions majoritaires |
|---|---|---|
| inférieur à 7 | acide | $\mathrm{H^+}$ |
| égal à 7 | neutre | autant de $\mathrm{H^+}$ que de $\mathrm{OH^-}$ |
| supérieur à 7 | basique | $\mathrm{OH^-}$ |

Diluer une solution acide ou basique dans de l’eau rapproche son pH de 7.

| Particule | Où se trouve-t-elle ? | Charge électrique |
|---|---|---|
| Proton | dans le noyau | positive |
| Neutron | dans le noyau | nulle |
| Électron | autour du noyau | négative |

::: retenir Atome et ion
- Un atome est électriquement neutre : il a autant d’électrons que de protons.
- Un ion est un atome, ou un groupe d’atomes, qui a gagné ou perdu des électrons : $\mathrm{Na^+}$ a perdu un électron, $\mathrm{Cl^-}$ en a gagné un, $\mathrm{Cu^{2+}}$ en a perdu deux.
:::

| Molécule | Formule | Atomes |
|---|---|---|
| Eau | $\mathrm{H_2O}$ | 2 hydrogène, 1 oxygène |
| Dioxyde de carbone | $\mathrm{CO_2}$ | 1 carbone, 2 oxygène |
| Dioxygène | $\mathrm{O_2}$ | 2 oxygène |
| Dihydrogène | $\mathrm{H_2}$ | 2 hydrogène |
| Diazote | $\mathrm{N_2}$ | 2 azote |
| Méthane | $\mathrm{CH_4}$ | 1 carbone, 4 hydrogène |

L’air est composé d’environ 78 % de diazote, 21 % de dioxygène et 1 % d’autres gaz (argon, dioxyde de carbone…).

## XIII. Les transformations chimiques et les tests {Collège}

Au cours d’une transformation chimique, les atomes des réactifs se réarrangent pour former les produits. Les atomes se conservent, donc **la masse totale se conserve**.

::: exemple Combustion du méthane
$$\mathrm{CH_4 + 2\,O_2 \longrightarrow CO_2 + 2\,H_2O}$$
On compte les atomes de chaque côté : 1 carbone, 4 hydrogène et 4 oxygène avant comme après. L’équation est bien équilibrée.
:::

| Espèce recherchée | Test | Résultat si elle est présente |
|---|---|---|
| Eau | sulfate de cuivre anhydre (poudre blanche) | il devient bleu |
| Dioxyde de carbone | eau de chaux | elle se trouble |
| Dioxygène | bûchette incandescente | elle se rallume |
| Dihydrogène | flamme approchée | petite détonation |
| Ion cuivre $\mathrm{Cu^{2+}}$ | quelques gouttes de soude | précipité bleu |
| Ion fer II $\mathrm{Fe^{2+}}$ | quelques gouttes de soude | précipité vert |
| Ion fer III $\mathrm{Fe^{3+}}$ | quelques gouttes de soude | précipité orange, couleur rouille |
| Ion chlorure $\mathrm{Cl^-}$ | nitrate d’argent | précipité blanc qui noircit à la lumière |

Au brevet, la liste des tests est en général fournie dans le sujet : il faut savoir lire le résultat et conclure.

## XIV. Les conversions utiles {Collège}

| Grandeur | Conversions |
|---|---|
| Vitesse | 1 m/s = 3,6 km/h |
| Durée | 1 h = 60 min = 3 600 s |
| Énergie | 1 kWh = 3 600 000 J ; 1 kJ = 1 000 J |
| Masse | 1 kg = 1 000 g ; 1 t = 1 000 kg |
| Volume | 1 L = 1 dm³ = 1 000 cm³ ; 1 mL = 1 cm³ |
| Masse volumique | 1 g/cm³ = 1 000 kg/m³ = 1 kg/L |
| Intensité | 1 A = 1 000 mA |
| Résistance | 1 kΩ = 1 000 Ω |

| Préfixe | Symbole | Il multiplie l’unité par |
|---|---|---|
| méga | M | 1 000 000 |
| kilo | k | 1 000 |
| milli | m | 0,001 |
| micro | µ | 0,000 001 |

::: conseil Le bon réflexe
On convertit toujours les valeurs dans les unités de la formule avant de calculer, puis on écrit l’unité du résultat.
:::
