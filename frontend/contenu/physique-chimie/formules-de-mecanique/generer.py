# -*- coding: utf-8 -*-
"""Page « Formules de mécanique » (physique-chimie/formules-de-mecanique).

    python -X utf8 generer.py

Calcule et vérifie (assert) toutes les valeurs des exemples, puis écrit
formulaire.md. Ne pas modifier formulaire.md à la main : modifier ce script et
le relancer.

Programmes officiels de physique-chimie (BO spécial n° 1 du 22 janvier 2019 pour
la Seconde, BO spécial n° 8 du 25 juillet 2019 pour la Première et la Terminale
de spécialité), thème « Mouvement et interactions » :
- Seconde : référentiel, vecteur vitesse approché MM'/Δt, forces (poids,
  gravitation, actions réciproques), principe d'inertie, chute libre à une dimension ;
- Première : loi de Coulomb, champs de gravitation et électrostatique,
  relation approchée m Δv/Δt = ΣF ;
- Terminale : vecteurs vitesse et accélération (dérivées), repère de Frenet,
  deuxième loi de Newton, mouvement dans un champ uniforme (pesanteur,
  condensateur plan), satellites et lois de Kepler.
Les données (G, masse et rayon de la Terre…) sont celles des manuels et des sujets de bac.
"""
import json
import re
from math import cos, pi, radians, sin, sqrt
from pathlib import Path

ICI = Path(__file__).resolve().parent
NBSP, NNBSP = chr(0xA0), chr(0x202F)

# ---------------------------------------------------------------- constantes (données usuelles)
g_T, g_L = 9.81, 1.62                 # N/kg
G = 6.67e-11                          # N·m²·kg⁻²
M_T, R_T = 5.97e24, 6.371e6           # kg, m (rayon moyen)
M_L, D_TL = 7.35e22, 3.84e8           # kg, m
k_C, e = 8.99e9, 1.60e-19             # N·m²·C⁻², C
m_e, m_p = 9.11e-31, 1.67e-27         # kg


def dec(x, n):
    """x avec n décimales, virgule décimale, espace fine insécable pour les milliers."""
    s = f"{x:,.{n}f}".replace(",", " ").replace(".", ",")
    return s.replace(" ", NNBSP)


def sci_parts(x, n):
    """(mantisse avec n décimales, exposant) : 1,98 et 20 pour 1,98e20."""
    m, ex = f"{x:.{n}e}".split("e")
    return m.replace(".", ","), int(ex)


def sci_tex(x, n):
    m, ex = sci_parts(x, n)
    return f"{m} \\times 10^{{{ex}}}"


SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def sci_txt(x, n):
    m, ex = sci_parts(x, n)
    return f"{m} × 10{str(ex).translate(SUP)}"


# ---------------------------------------------------------------- exemples (calculés ici)
V = {}
# I. vitesse
v_cycl = 18 / 0.75
V["CYCL_KMH"] = dec(v_cycl, 0)
V["CYCL_MS"] = dec(v_cycl / 3.6, 2)
assert (V["CYCL_KMH"], V["CYCL_MS"]) == ("24", "6,67")
V["V3"] = dec(0.024 / 0.040, 2)
assert V["V3"] == "0,60"
assert dec(90 / 3.6, 0) == "25"

# II. forces
V["P_TERRE"] = dec(65 * g_T, 0)
V["P_LUNE"] = dec(65 * g_L, 0)
assert (V["P_TERRE"], V["P_LUNE"]) == ("638", "105")
F_TL = G * M_T * M_L / D_TL ** 2
V["F_TL"] = sci_tex(F_TL, 2)
V["F_TL_TXT"] = sci_txt(F_TL, 2)
assert V["F_TL"] == "1,98 \\times 10^{20}"
g0 = G * M_T / R_T ** 2
g400 = G * M_T / (R_T + 4e5) ** 2
V["G_SOL"], V["G_ISS"] = dec(g0, 2), dec(g400, 2)
V["G_ISS_PC"] = dec(100 * g400 / g0, 0)
assert (V["G_SOL"], V["G_ISS"], V["G_ISS_PC"]) == ("9,81", "8,69", "89")
F_coul = k_C * e ** 2 / 5.3e-11 ** 2
F_grav = G * m_e * m_p / 5.3e-11 ** 2
V["F_COUL"], V["F_GRAV"] = sci_tex(F_coul, 1), sci_tex(F_grav, 1)
assert (V["F_COUL"], V["F_GRAV"]) == ("8,2 \\times 10^{-8}", "3,6 \\times 10^{-47}")
assert 1e39 < F_coul / F_grav < 3e39          # « environ 2 × 10³⁹ fois plus grande »
V["RAPPORT_COUL"] = sci_tex(F_coul / F_grav, 0)
assert V["RAPPORT_COUL"] == "2 \\times 10^{39}"

# III. variation de vitesse
V["F_SKATE"] = sci_tex(50 * (3.2 - 3.0) / 0.10, 1)
assert V["F_SKATE"] == "1,0 \\times 10^{2}"
V["DV_CHUTE"] = dec(g_T * 0.10, 2)
assert V["DV_CHUTE"] == "0,98"

# IV. accélération
v100 = 100 / 3.6
a_voit = v100 / 10.0
V["V100"] = dec(v100, 1)
V["A_VOIT"] = dec(a_voit, 2)
V["X_VOIT"] = dec(0.5 * a_voit * 10.0 ** 2, 0)
assert (V["V100"], V["A_VOIT"], V["X_VOIT"]) == ("27,8", "2,78", "139")
V["A_ROND"] = dec(10.0 ** 2 / 20, 1)
assert V["A_ROND"] == "5,0"

# V. deuxième loi de Newton
V["A_CHARIOT"] = dec(5.0 / 2.0, 1)
assert V["A_CHARIOT"] == "2,5"

# VI. champ uniforme (mêmes valeurs que la figure tir_parabolique)
v0, al = 10.0, radians(45)
t_S = v0 * sin(al) / g_T
h = (v0 * sin(al)) ** 2 / (2 * g_T)
D = v0 ** 2 * sin(2 * al) / g_T
V["T_S"], V["H_MAX"], V["PORTEE"] = dec(t_S, 3), dec(h, 2), dec(D, 1)
assert (V["T_S"], V["H_MAX"], V["PORTEE"]) == ("0,721", "2,55", "10,2")
# contrôle : z(t_S) = h et z(2 t_S) = 0, x(2 t_S) = D
z = lambda t: -0.5 * g_T * t * t + v0 * sin(al) * t
x = lambda t: v0 * cos(al) * t
assert abs(z(t_S) - h) < 1e-12 and abs(z(2 * t_S)) < 1e-12 and abs(x(2 * t_S) - D) < 1e-12
E_cond = 200 / 0.020
F_el = e * E_cond
V["E_COND"] = sci_tex(E_cond, 1)
V["F_EL"] = sci_tex(F_el, 1)
V["A_EL"] = sci_tex(F_el / m_e, 1)
V["P_EL"] = sci_tex(m_e * g_T, 1)
assert (V["E_COND"], V["F_EL"], V["A_EL"], V["P_EL"]) == (
    "1,0 \\times 10^{4}", "1,6 \\times 10^{-15}", "1,8 \\times 10^{15}", "8,9 \\times 10^{-30}")

# VII. satellites
GM = G * M_T
r_iss = R_T + 4.0e5
v_iss = sqrt(GM / r_iss)
T_iss = 2 * pi * r_iss / v_iss
V["V_ISS"] = sci_tex(v_iss, 2)
V["V_ISS_KMS"] = dec(v_iss / 1000, 2)
V["V_ISS_KMH"] = dec(round(v_iss * 3.6, -2), 0)
V["T_ISS"] = sci_tex(T_iss, 2)
V["T_ISS_MIN"] = dec(T_iss / 60, 1)
assert (V["V_ISS"], V["V_ISS_KMH"], V["T_ISS"], V["T_ISS_MIN"]) == (
    "7,67 \\times 10^{3}", f"27{NNBSP}600", "5,55 \\times 10^{3}", "92,5")
assert abs(T_iss ** 2 / r_iss ** 3 - 4 * pi ** 2 / GM) < 1e-25          # 3e loi de Kepler
T_geo = 23 * 3600 + 56 * 60 + 4
r_geo = (GM * T_geo ** 2 / (4 * pi ** 2)) ** (1 / 3)
V["R_GEO"] = sci_tex(r_geo, 2)
V["R_GEO_KM"] = dec(round(r_geo / 1000, -1), 0)
V["H_GEO_KM"] = dec(round((r_geo - R_T) / 1000, -2), 0)
assert (V["R_GEO"], V["R_GEO_KM"], V["H_GEO_KM"]) == ("4,21 \\times 10^{7}", f"42{NNBSP}150", f"35{NNBSP}800")


def remplacer(texte):
    for k_, v_ in V.items():
        texte = texte.replace("{" + k_ + "}", v_)
    reste = re.findall(r"(?<!overrightarrow)\{[A-Z][A-Z0-9_]+\}", texte)
    assert not reste, reste
    return texte


INFOS = {
    "slug": "formules-de-mecanique",
    "titre": "Formules de mécanique : mouvement, forces et lois de Newton",
    "titreCourt": "Formules de mécanique",
    "titreSeo": "Formules de mécanique : vitesse, forces, lois de Newton, Kepler",
    "description": "Les formules de mécanique du lycée expliquées : vitesse, poids, gravitation, lois de Newton, chute libre, satellites et lois de Kepler, avec exemples corrigés.",
    "chapo": "Toutes les formules de mécanique de la Seconde à la Terminale, expliquées une à une : le sens de chaque lettre avec son unité, un exemple corrigé, un schéma quand il aide et le piège à éviter.",
    "resume": "Vitesse, forces, lois de Newton, chute libre, satellites",
    "vignette": "tir_parabolique",
    "theme": "Mécanique",
    "niveaux": ["Lycée"],
    "ordre": 6,
    "publie": "2026-11-19",
    "modifie": "2026-11-19",
    "motsCles": ["formules de mécanique", "formulaire mécanique", "formulaire de physique terminale", "formule vitesse",
                 "vecteur vitesse", "formule accélération", "deuxième loi de Newton", "principe fondamental de la dynamique",
                 "principe d'inertie", "troisième loi de Newton", "formule du poids", "force gravitationnelle formule",
                 "champ de gravitation", "loi de Coulomb", "chute libre formule", "équations horaires",
                 "mouvement parabolique", "mouvement circulaire uniforme", "repère de Frenet", "vitesse d'un satellite",
                 "période de révolution", "troisième loi de Kepler", "satellite géostationnaire"],
    "figures": [
        {"nom": "chronophotographie", "alt": "Chronophotographie d’une balle lancée : sept positions M0 à M6 prises à intervalles de temps égaux sur une trajectoire en arc de parabole. Les vecteurs vitesse v2 et v4 sont tangents à la trajectoire ; au point M3, le vecteur variation de vitesse Δv = v4 − v2 est vertical et dirigé vers le bas, comme le poids."},
        {"nom": "actions_reciproques", "alt": "Deux corps A et B, de masses mA et mB, séparés par la distance d entre leurs centres. La force exercée par B sur A part du centre de A vers B ; la force exercée par A sur B part du centre de B vers A. Les deux forces ont la même valeur et des sens opposés."},
        {"nom": "mouvement_circulaire", "alt": "Mouvement circulaire de centre O et de rayon R, parcouru dans le sens inverse des aiguilles d’une montre. Au point M1, le vecteur vitesse est tangent au cercle et le vecteur accélération est dirigé vers le centre. Au point M2, le repère de Frenet : le vecteur ut tangent dans le sens du mouvement, le vecteur un dirigé vers le centre."},
        {"nom": "tir_parabolique", "alt": "Tir d’un projectile depuis l’origine O avec une vitesse initiale v0 inclinée d’un angle α au-dessus de l’axe horizontal x, l’axe z étant vertical vers le haut. La trajectoire est une parabole. Au sommet S, à la hauteur h, la vitesse est horizontale et le poids P est vertical vers le bas. La portée D est la distance horizontale entre le départ et le retour au sol."},
        {"nom": "satellite", "alt": "Satellite sur une orbite circulaire autour de la Terre, de rayon r égal au rayon de la Terre RT plus l’altitude h. La force de gravitation F exercée par la Terre est dirigée vers le centre O de la Terre ; la vitesse v du satellite est tangente à l’orbite."},
    ],
    "liees": ["physique-chimie/formulaire-mecanique-prepa", "physique-chimie/formules-physique-chimie-brevet",
              "formulaires/derivees", "formulaires/pythagore-thales-trigonometrie", "tables/puissances-de-10-prefixes"],
    "faq": [
        ["Quelle est la formule de la vitesse ?", "La vitesse moyenne est la distance parcourue divisée par la durée du parcours : v = d / Δt. Avec des mètres et des secondes, elle s’exprime en m/s ; avec des kilomètres et des heures, en km/h. Un cycliste qui parcourt 18 km en 0,75 h roule à {CYCL_KMH} km/h, soit environ {CYCL_MS} m/s : on divise par 3,6."],
        ["Que dit la deuxième loi de Newton ?", "Dans un référentiel galiléen, la somme des forces appliquées à un système est égale au produit de sa masse par l’accélération de son centre de masse : ΣF = m × a, en vecteurs. L’accélération a donc la direction et le sens de la somme des forces. Un chariot de 2,0 kg tiré par une force de 5,0 N, sans frottement, a une accélération de {A_CHARIOT} m/s²."],
        ["Quelle est la formule du poids ?", "P = m × g, avec P en newtons, m en kilogrammes et g l’intensité de la pesanteur : 9,81 N/kg sur Terre et 1,62 N/kg sur la Lune. Une personne de 65 kg a un poids d’environ {P_TERRE} N sur Terre et {P_LUNE} N sur la Lune, mais sa masse reste 65 kg."],
        ["Quelle est la formule de la force gravitationnelle ?", "F = G × mA × mB / d², avec G = 6,67 × 10⁻¹¹ N·m²·kg⁻², les masses en kilogrammes et d la distance entre les centres des deux corps, en mètres. La Terre et la Lune s’attirent ainsi avec une force d’environ {F_TL_TXT} N."],
        ["Comment calculer la vitesse d’un satellite ?", "Sur une orbite circulaire, v = √(G × M / r), où M est la masse de l’astre et r la distance au centre de l’astre, c’est-à-dire son rayon plus l’altitude. Pour la Station spatiale internationale, à 400 km d’altitude, r = 6 771 km et v ≈ {V_ISS_KMS} km/s, soit environ {V_ISS_KMH} km/h : elle fait le tour de la Terre en {T_ISS_MIN} minutes environ."],
        ["Quelles sont les équations horaires d’un mouvement de chute libre ?", "Avec un axe z vertical vers le haut et un lancer depuis l’origine à la vitesse v0, inclinée d’un angle α : x(t) = v0 × cos α × t et z(t) = −½ × g × t² + v0 × sin α × t. La seule force est le poids, donc l’accélération vaut g, verticale vers le bas. À 10 m/s et 45°, le projectile monte à {H_MAX} m et retombe à {PORTEE} m de son point de départ."],
    ],
}

TEXTE = r"""<!-- optitab:1 -->
::: conseil Par où commencer ?
- **En Seconde** : parties I, II (poids, gravitation, actions réciproques) et III.
- **En Première** : la partie II (champ de gravitation, loi de Coulomb) et la partie III (variation de la vitesse).
- **En Terminale** : parties IV à VII, avec les constantes de la partie VIII.
- **Au collège** : le formulaire de physique-chimie du brevet (lien en bas de page).
- **En prépa et à l’université** : le formulaire de mécanique du supérieur (lien en bas de page).
:::

## I. La vitesse et le vecteur vitesse {Lycée}

*Programme de Seconde.*

Un mouvement se décrit toujours dans un **référentiel** : un objet de référence, muni d’un repère et d’une horloge. La trajectoire et la vitesse d’un même objet changent quand on change de référentiel.

::: formule Vitesse moyenne
$$v = \dfrac{d}{\Delta t}$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $v$ | vitesse moyenne | m/s (ou km/h) |
| $d$ | distance parcourue | m (ou km) |
| $\Delta t$ | durée du parcours | s (ou h) |

::: exemple
Un cycliste parcourt 18 km en 45 min, soit 0,75 h : $v = \dfrac{18}{0,75} = {CYCL_KMH}$ km/h. En mètres par seconde : $v = {CYCL_KMH} \div 3,6 \approx {CYCL_MS}$ m/s.
:::

::: attention Passer des km/h aux m/s
1 m/s = 3,6 km/h. On **divise** par 3,6 pour passer des km/h aux m/s, et on multiplie par 3,6 dans l’autre sens : 90 km/h = 25 m/s.
:::

Sur une **chronophotographie**, les positions $M_0$, $M_1$, $M_2$… sont enregistrées à intervalles de temps égaux $\Delta t$. Le vecteur vitesse au point $M_i$ s’obtient à partir du déplacement jusqu’à la position suivante :

::: formule Vecteur vitesse (approché)
$$\vec{v}_i \approx \dfrac{\overrightarrow{M_iM_{i+1}}}{\Delta t}$$
:::

- Sa **direction** est tangente à la trajectoire, et son **sens** est celui du mouvement.
- Sa **valeur** est $v_i \approx \dfrac{M_iM_{i+1}}{\Delta t}$, en m/s.

[IMAGE_1]

::: exemple
Les images sont prises toutes les 40 ms, et la distance réelle entre $M_3$ et $M_4$ est de 2,4 cm : $v_3 \approx \dfrac{0,024}{0,040} = {V3}$ m/s.
:::

::: retenir Le mouvement rectiligne uniforme
La trajectoire est une droite et la vitesse est constante : les points de la chronophotographie sont alignés et également espacés, le vecteur vitesse ne change pas. Si les écarts augmentent, le mouvement est accéléré ; s’ils diminuent, il est ralenti.
:::

## II. Les forces à connaître {Lycée}

*Programme de Seconde et de Première.*

Une action mécanique est modélisée par une **force**, représentée par un vecteur : un point d’application, une direction, un sens et une valeur en newtons (N).

::: formule Le poids
$$P = m \times g$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $P$ | poids | N |
| $m$ | masse | kg |
| $g$ | intensité de la pesanteur : 9,81 sur Terre | N/kg |

Le poids est une force **verticale**, dirigée **vers le bas** et appliquée au centre de gravité $G$ de l’objet : $\vec{P} = m\,\vec{g}$.

::: exemple
Une personne de 65 kg a un poids $P = 65 \times 9,81 \approx {P_TERRE}$ N sur Terre. Sur la Lune, où $g = 1,62$ N/kg : $P = 65 \times 1,62 \approx {P_LUNE}$ N.
:::

::: attention Masse ou poids ?
La masse, en kilogrammes, est la même partout. Le poids, en newtons, dépend de l’astre : sur la Lune, la même personne a toujours une masse de 65 kg.
:::

::: formule Interaction gravitationnelle
$$F = G \times \dfrac{m_A \times m_B}{d^2}$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $F$ | valeur de la force | N |
| $G$ | constante de gravitation : $6,67 \times 10^{-11}$ | N·m²·kg⁻² |
| $m_A$, $m_B$ | masses des deux corps | kg |
| $d$ | distance entre leurs centres | m |

Les deux corps s’attirent : chacun subit une force dirigée vers l’autre.

[IMAGE_2]

::: formule Principe des actions réciproques (troisième loi de Newton)
$$\vec{F}_{A/B} = -\,\vec{F}_{B/A}$$
:::

Les deux forces ont la même droite d’action et la même valeur, mais des sens opposés. Elles s’appliquent à deux corps différents : $\vec{F}_{A/B}$ s’exerce sur $B$, $\vec{F}_{B/A}$ sur $A$.

::: exemple
Pour la Terre et la Lune, avec $m_T = 5,97 \times 10^{24}$ kg, $m_L = 7,35 \times 10^{22}$ kg et $d = 3,84 \times 10^{8}$ m : $F \approx {F_TL}$ N. La Lune attire la Terre avec exactement la même force.
:::

::: attention La distance se mesure entre les centres, en mètres
Pour un objet à l’altitude $h$ au-dessus d’une planète de rayon $R$, la distance vaut $d = R + h$, et non $h$. Et les kilomètres se convertissent en mètres avant le calcul.
:::

Le poids d’un objet est, à peu de chose près, la force de gravitation exercée par l’astre. On en déduit le **champ de gravitation** (programme de Première) :

::: formule Champ de gravitation créé par un astre
$$g = G \times \dfrac{M}{d^2}$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $g$ | valeur du champ de gravitation | N/kg |
| $M$ | masse de l’astre | kg |
| $d$ | distance au centre de l’astre | m |

::: exemple
À la surface de la Terre, $M = 5,97 \times 10^{24}$ kg et $d = R_T = 6,371 \times 10^{6}$ m, d’où $g \approx {G_SOL}$ N/kg. À 400 km d’altitude, à bord de la Station spatiale internationale, $d = 6,771 \times 10^{6}$ m et $g \approx {G_ISS}$ N/kg : encore {G_ISS_PC} % de la valeur au sol. Les astronautes flottent parce qu’ils tombent en même temps que la station, pas parce que la gravité a disparu.
:::

Entre deux charges électriques, l’interaction est décrite par la **loi de Coulomb** (programme de Première), qui ressemble beaucoup à la loi de gravitation :

::: formule Loi de Coulomb
$$F = k \times \dfrac{|q_A \times q_B|}{d^2}$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $F$ | valeur de la force | N |
| $k$ | constante : $8,99 \times 10^{9}$ | N·m²·C⁻² |
| $q_A$, $q_B$ | charges électriques | C |
| $d$ | distance entre les charges | m |

Deux charges de même signe se repoussent, deux charges de signes contraires s’attirent. Une charge $q$ placée dans un champ électrique $\vec{E}$ (en V/m) subit la force $\vec{F} = q\,\vec{E}$.

::: exemple
Dans l’atome d’hydrogène, le proton et l’électron, de charges $+e$ et $-e$ avec $e = 1,60 \times 10^{-19}$ C, sont distants de $5,3 \times 10^{-11}$ m : $F \approx {F_COUL}$ N. La force de gravitation entre eux ne vaut que ${F_GRAV}$ N, environ ${RAPPORT_COUL}$ fois moins.
:::

## III. Le principe d’inertie et la variation de la vitesse {Lycée}

*Programme de Seconde et de Première.*

::: retenir Le principe d’inertie (première loi de Newton)
Dans un référentiel galiléen (le sol, pour les mouvements courants), si les forces qui s’exercent sur un système **se compensent**, ce système est **immobile** ou en **mouvement rectiligne uniforme**. Et réciproquement.
:::

Par contraposée : si la vitesse d’un système change, en valeur **ou** en direction, les forces qui s’exercent sur lui ne se compensent pas. La **relation approchée** du programme de Première relie cette variation aux forces :

::: formule Variation du vecteur vitesse
$$m \times \dfrac{\Delta\vec{v}}{\Delta t} \approx \sum \vec{F}$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $m$ | masse du système | kg |
| $\Delta\vec{v}$ | variation du vecteur vitesse | m/s |
| $\Delta t$ | durée, courte, de la variation | s |
| $\sum \vec{F}$ | somme des forces | N |

Le vecteur $\Delta\vec{v} = \vec{v}_{i+1} - \vec{v}_i$ a la direction et le sens de la somme des forces. Sur la chronophotographie de la partie I, la balle ne subit que son poids, les frottements étant négligés : $\Delta\vec{v}$ est vertical et dirigé vers le bas.

::: exemple
Un skateur de 50 kg, en ligne droite, passe de 3,0 à 3,2 m/s en 0,10 s : $\sum F \approx 50 \times \dfrac{0,20}{0,10} = {F_SKATE}$ N, dans le sens du mouvement. Dans l’autre sens : une balle en chute libre ne subit que son poids, donc $\Delta v \approx g \times \Delta t = 9,81 \times 0,10 \approx {DV_CHUTE}$ m/s toutes les 0,10 s, vers le bas.
:::

::: attention Pas besoin de force pour avancer
Un objet en mouvement rectiligne uniforme n’a besoin d’aucune force pour continuer : il faut une force pour **changer** son mouvement. Et plus la masse est grande, plus la vitesse varie lentement pour les mêmes forces.
:::

## IV. Les vecteurs vitesse et accélération {Lycée}

*Programme de Terminale.*

::: formule Vitesse et accélération : des dérivées
$$\vec{v} = \dfrac{\mathrm{d}\overrightarrow{OM}}{\mathrm{d}t} \qquad \vec{a} = \dfrac{\mathrm{d}\vec{v}}{\mathrm{d}t}$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $\overrightarrow{OM}$ | vecteur position | m |
| $\vec{v}$ | vecteur vitesse | m/s |
| $\vec{a}$ | vecteur accélération | m/s² |

En coordonnées : $v_x = \dfrac{\mathrm{d}x}{\mathrm{d}t}$ et $a_x = \dfrac{\mathrm{d}v_x}{\mathrm{d}t}$, et de même selon $y$ et $z$.

**Mouvement rectiligne uniformément accéléré** : l’accélération $a$ est constante.

::: formule Mouvement rectiligne uniformément accéléré
$$\begin{aligned}
v(t) &= a\,t + v_0 \\
x(t) &= \tfrac{1}{2}\,a\,t^2 + v_0\,t + x_0
\end{aligned}$$
:::

::: exemple
Une voiture part de l’arrêt et atteint 100 km/h, soit {V100} m/s, en 10,0 s : $a = \dfrac{{V100}}{10,0} \approx {A_VOIT}$ m/s². Distance parcourue : $x = \tfrac{1}{2} \times {A_VOIT} \times 10,0^2 \approx {X_VOIT}$ m.
:::

**Mouvement circulaire** : on utilise le **repère de Frenet**, lié au point mobile : $\vec{u}_t$ est tangent à la trajectoire, dans le sens du mouvement, et $\vec{u}_n$ est dirigé vers le centre du cercle.

[IMAGE_3]

::: formule Accélération dans le repère de Frenet
$$\vec{a} = \dfrac{\mathrm{d}v}{\mathrm{d}t}\,\vec{u}_t + \dfrac{v^2}{R}\,\vec{u}_n$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $v$ | valeur de la vitesse | m/s |
| $R$ | rayon du cercle | m |
| $a$ | valeur de l’accélération | m/s² |

Si le mouvement circulaire est **uniforme**, la vitesse garde la même valeur : $\dfrac{\mathrm{d}v}{\mathrm{d}t} = 0$. L’accélération est alors dirigée vers le centre, comme au point $M_1$ du schéma :

::: formule Mouvement circulaire uniforme
$$a = \dfrac{v^2}{R}$$
:::

::: exemple
Une voiture tourne dans un rond-point de rayon 20 m à 36 km/h, soit 10 m/s : $a = \dfrac{10^2}{20} = {A_ROND}$ m/s², vers le centre du rond-point.
:::

Le vecteur accélération selon le type de mouvement :

| Mouvement | Vecteur accélération |
|---|---|
| rectiligne uniforme | nul |
| rectiligne uniformément accéléré | constant, parallèle à la trajectoire |
| circulaire uniforme | vers le centre, de valeur $\dfrac{v^2}{R}$ |

::: attention Un mouvement circulaire uniforme est accéléré
La valeur de la vitesse ne change pas, mais sa **direction** change à chaque instant : l’accélération n’est pas nulle.
:::

## V. La deuxième loi de Newton {Lycée}

*Programme de Terminale.*

::: formule Deuxième loi de Newton
$$\sum \vec{F} = m\,\vec{a}$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $\sum \vec{F}$ | somme des forces | N |
| $m$ | masse du système | kg |
| $\vec{a}$ | accélération du centre de masse | m/s² |

Elle s’applique dans un **référentiel galiléen** : le référentiel terrestre pour les mouvements de courte durée, le référentiel géocentrique pour les satellites de la Terre. Quand $\vec{a} = \vec{0}$, on retrouve le principe d’inertie.

::: methode Appliquer la deuxième loi de Newton
1. Définir le **système** et le **référentiel**, supposé galiléen.
2. Faire le **bilan des forces** et les représenter sur un schéma.
3. Écrire $\sum \vec{F} = m\,\vec{a}$.
4. **Projeter** sur des axes choisis pour obtenir les coordonnées de $\vec{a}$.
:::

::: exemple
Un chariot de 2,0 kg roule sur un sol horizontal, tiré par une force horizontale de 5,0 N ; les frottements sont négligés. Le poids et la réaction du sol se compensent, donc $a = \dfrac{5,0}{2,0} = {A_CHARIOT}$ m/s², dans le sens de la traction.
:::

::: attention L’accélération suit les forces, pas la vitesse
$\vec{a}$ a la direction et le sens de la somme des forces, pas forcément ceux de $\vec{v}$. Au sommet d’un tir (partie VI), la vitesse est horizontale mais l’accélération est verticale, vers le bas.
:::

## VI. Le mouvement dans un champ uniforme {Lycée}

*Programme de Terminale.*

**Dans le champ de pesanteur.** Un projectile qui ne subit que son poids est en **chute libre** : $\sum \vec{F} = m\,\vec{g} = m\,\vec{a}$, donc $\vec{a} = \vec{g}$, quelle que soit sa masse. Le mouvement a lieu dans un plan.

[IMAGE_4]

On choisit un axe $x$ horizontal et un axe $z$ vertical **vers le haut**, l’origine au point de départ, et l’instant $t = 0$ au lancer, à la vitesse $v_0$ inclinée de l’angle $\alpha$. En intégrant deux fois $\vec{a} = \vec{g}$ :

::: formule Équations horaires
$$\begin{aligned}
x(t) &= v_0 \cos\alpha \; t \\
z(t) &= -\tfrac{1}{2}\,g\,t^2 + v_0 \sin\alpha \; t
\end{aligned}$$
:::

La vitesse a pour coordonnées $v_x = v_0 \cos\alpha$, constante, et $v_z = -g\,t + v_0 \sin\alpha$. En éliminant $t$ entre $x$ et $z$, on obtient une parabole :

::: formule Équation de la trajectoire
$$z = -\dfrac{g}{2\,v_0^2 \cos^2\alpha}\,x^2 + x\tan\alpha$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $g$ | intensité de la pesanteur : 9,81 | m/s² |
| $v_0$ | vitesse initiale | m/s |
| $\alpha$ | angle de tir | degré |
| $x$, $z$ | coordonnées du projectile | m |

::: exemple
Avec $v_0 = 10,0$ m/s et $\alpha = 45°$, depuis le sol. Au sommet, $v_z = 0$ : $t_S = \dfrac{v_0 \sin\alpha}{g} \approx {T_S}$ s, et la hauteur atteinte est $h = z(t_S) \approx {H_MAX}$ m. Le projectile revient au sol à $t = 2\,t_S$, à la distance $D = \dfrac{v_0^2 \sin(2\alpha)}{g} \approx {PORTEE}$ m.
:::

::: attention Les signes, et ce qu’il faut savoir retrouver
Avec un axe $z$ vers le haut, $a_z = -g$ : le signe moins vient du choix de l’axe. Si le lancer part d’une hauteur $z_0$, on ajoute $z_0$ à $z(t)$. Les formules de la hauteur et de la portée ne sont pas à apprendre : elles se retrouvent à partir des équations horaires.
:::

**Dans un champ électrique uniforme.** Entre les deux armatures d’un condensateur plan, le champ électrique est uniforme :

::: formule Champ dans un condensateur plan
$$E = \dfrac{U}{d}$$
:::

::: formule Force et accélération d’une particule chargée
$$\vec{F} = q\,\vec{E} \qquad \vec{a} = \dfrac{q\,\vec{E}}{m}$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $E$ | valeur du champ électrique | V/m |
| $U$ | tension entre les armatures | V |
| $d$ | distance entre les armatures | m |
| $q$ | charge de la particule | C |

::: exemple
Avec $U = 200$ V et $d = 2,0$ cm : $E = \dfrac{200}{0,020} = {E_COND}$ V/m. Un électron y subit une force de valeur $F = e \times E = {F_EL}$ N, d’où $a = \dfrac{F}{m_e} \approx {A_EL}$ m/s². Son poids, ${P_EL}$ N, est tout à fait négligeable.
:::

::: attention Le signe de la charge
Pour un électron, $q = -e$ est négative : la force est **opposée** au champ $\vec{E}$, et l’électron est attiré par l’armature positive.
:::

## VII. Les satellites et les planètes {Lycée}

*Programme de Terminale.*

::: retenir Les trois lois de Kepler
1. Les planètes décrivent des **ellipses** dont le Soleil occupe un foyer.
2. **Loi des aires** : le segment Soleil-planète balaie des aires égales pendant des durées égales ; la planète va plus vite près du Soleil.
3. Le rapport $\dfrac{T^2}{a^3}$ est le même pour toutes les planètes du Soleil, avec $T$ la période de révolution et $a$ le demi-grand axe de l’orbite.

Les mêmes lois s’appliquent aux satellites d’une planète.
:::

Pour une **orbite circulaire** de rayon $r = R_T + h$, la seule force est la gravitation, dirigée vers le centre de la Terre. D’après la deuxième loi de Newton, l’accélération est donc dirigée vers le centre : sa composante tangentielle est nulle, le mouvement est **circulaire uniforme**. En écrivant que $a = v^2/r$ est égale à $G\,M/r^2$, on obtient la vitesse, puis la période.

[IMAGE_5]

::: formule Vitesse d’un satellite en orbite circulaire
$$v = \sqrt{\dfrac{G\,M}{r}}$$
:::

::: formule Période de révolution
$$\begin{aligned}
T &= \dfrac{2\pi\,r}{v} \\
&= 2\pi\sqrt{\dfrac{r^3}{G\,M}}
\end{aligned}$$
:::

::: formule Troisième loi de Kepler (orbite circulaire)
$$\dfrac{T^2}{r^3} = \dfrac{4\pi^2}{G\,M}$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $v$ | vitesse du satellite | m/s |
| $T$ | période de révolution | s |
| $r$ | rayon de l’orbite, depuis le centre de l’astre | m |
| $M$ | masse de l’astre attracteur | kg |

La vitesse et la période **ne dépendent pas de la masse du satellite**.

::: exemple
La Station spatiale internationale tourne à 400 km d’altitude : $r = 6 371 + 400 = 6 771$ km, soit $6,771 \times 10^{6}$ m. Avec $G = 6,67 \times 10^{-11}$ et $M_T = 5,97 \times 10^{24}$ kg : $v \approx {V_ISS}$ m/s, environ {V_ISS_KMH} km/h, et $T = \dfrac{2\pi\,r}{v} \approx {T_ISS}$ s, soit {T_ISS_MIN} min.
:::

::: exemple Le satellite géostationnaire
Il reste toujours au-dessus du même point de l’équateur : il tourne dans le plan de l’équateur, dans le même sens que la Terre, avec la même période qu’elle, $T = 23$ h 56 min 4 s = 86 164 s. La troisième loi de Kepler donne $r = \sqrt[3]{\dfrac{G\,M_T\,T^2}{4\pi^2}} \approx {R_GEO}$ m, soit environ {R_GEO_KM} km du centre de la Terre : une altitude d’environ {H_GEO_KM} km.
:::

::: attention Rayon de l’orbite et altitude
Dans ces formules, $r$ est la distance au **centre** de l’astre, pas l’altitude : $r = R + h$. $M$ est la masse de l’astre attracteur, pas celle du satellite, et $T$ s’exprime en secondes.
:::

## VIII. Les constantes et les données utiles {Lycée}

| Grandeur | Valeur |
|---|---|
| Intensité de la pesanteur sur Terre | $g = 9,81$ N/kg, soit 9,81 m/s² |
| Intensité de la pesanteur sur la Lune | 1,62 N/kg |
| Constante de gravitation | $G = 6,67 \times 10^{-11}$ N·m²·kg⁻² |
| Masse de la Terre | $5,97 \times 10^{24}$ kg |
| Rayon moyen de la Terre | 6 371 km |
| Masse de la Lune | $7,35 \times 10^{22}$ kg |
| Distance moyenne Terre-Lune | $3,84 \times 10^{5}$ km |
| Constante de la loi de Coulomb | $k = 8,99 \times 10^{9}$ N·m²·C⁻² |
| Charge élémentaire | $e = 1,60 \times 10^{-19}$ C |
| Masse de l’électron | $9,11 \times 10^{-31}$ kg |
| Masse du proton | $1,67 \times 10^{-27}$ kg |

::: conseil Les conversions qui reviennent tout le temps
- 1 m/s = 3,6 km/h.
- 1 h = 3 600 s et 1 km = 1 000 m.
- 1 cm = $10^{-2}$ m et 1 ms = $10^{-3}$ s.
- Toujours convertir en unités du Système international (m, s, kg) avant d’appliquer une formule.
:::
"""

# ---------------------------------------------------------------- typographie
UNITES = ["m/s²", "km/h", "km/s", "m/s", "N/kg", "V/m", "kg", "km", "cm", "ms", "min", "N", "V", "C", "s", "h", "m", "%"]
UNITE = "(?:" + "|".join(re.escape(u) for u in sorted(UNITES, key=len, reverse=True)) + ")"
NOMBRE_UNITE = re.compile(r"(\d) (?=" + UNITE + r"(?![A-Za-zÀ-ÿ0-9’²]))")
MILLIERS = re.compile(r"(\d) (?=\d{3}(?![\d,]))")
MATHS = re.compile(r"(\$\$[\s\S]*?\$\$|\$[^$\n]+\$)")


APRES_FORMULE = re.compile(r"^ (?=" + UNITE + r"(?![A-Za-zÀ-ÿ0-9’²]))")


def insecables(texte):
    morceaux = MATHS.split(texte)
    for i in range(0, len(morceaux), 2):
        m = MILLIERS.sub(lambda x: x.group(1) + NNBSP, morceaux[i])
        m = NOMBRE_UNITE.sub(lambda x: x.group(1) + NBSP, m)
        if i and not morceaux[i - 1].startswith("$$"):
            m = APRES_FORMULE.sub(NBSP, m)          # « $… = 0,60$ m/s » : l'unité reste avec la formule
        morceaux[i] = m
    return "".join(morceaux)


def virgules_maths(texte):
    """Dans les formules : 6,67 → 6{,}67 (sinon une espace s'ajoute après la virgule)."""
    return MATHS.sub(lambda m: re.sub(r"(\d),(\d)", r"\1{,}\2", m.group(0)), texte)


def ecrire():
    infos = json.loads(remplacer(json.dumps(INFOS, ensure_ascii=False)))
    assert len(infos["titreSeo"]) <= 65 and 140 <= len(infos["description"]) <= 160, (len(infos["titreSeo"]), len(infos["description"]))
    for q, r in infos["faq"]:
        assert "$" not in r and "\\" not in r, q
    entete = json.dumps(infos, ensure_ascii=False, indent=2)
    texte = virgules_maths(remplacer(TEXTE))
    # milliers dans les formules : « 6 771 » → 6\,771
    texte = MATHS.sub(lambda m: re.sub(r"(\d) (\d{3})(?!\d)", r"\1\\,\2", m.group(0)), texte)
    assert texte.count("[IMAGE_") == len(infos["figures"])
    (ICI / "formulaire.md").write_text(insecables(f"---\n{entete}\n---\n{texte}"), encoding="utf-8", newline="\n")
    print("formulaire.md écrit :", len(infos["titreSeo"]), "car. (titre),", len(infos["description"]), "car. (description)")


if __name__ == "__main__":
    ecrire()
