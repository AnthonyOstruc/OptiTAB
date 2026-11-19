# -*- coding: utf-8 -*-
"""Page « Unités du Système international et constantes physiques »
(physique-chimie/unites-si-constantes-physiques).

    python -X utf8 generer.py

1. Contrôle : chaque constante écrite ici est comparée à la valeur CODATA 2022
   de scipy.constants (valeur et incertitude-type), et les valeurs exactes de
   la définition du SI (20 mai 2019, Brochure sur le SI, BIPM, 9e édition) sont
   recalculées (R = NA·k, F = NA·e, ħ = h/2π, σ, b de Wien, Vm…).
2. Données astronomiques : recoupées par les constantes GM de l'UAI et de l'IERS
   (Terre, Soleil, Lune) divisées par G ; année-lumière = c × 365,25 jours.
3. Écrit formulaire.md (ne pas le modifier à la main).
"""
import json
import re
from math import pi
from pathlib import Path

import scipy.constants as sc

ICI = Path(__file__).resolve().parent
NBSP, NNBSP = chr(0xA0), chr(0x202F)
PC = sc.physical_constants


def cod(nom):
    return PC[nom][0], PC[nom][2]


# ---------------------------------------------------------------- mise en forme des nombres
def grouper(chiffres):
    """« 6.62607015 » → « 6,626 070 15 » (groupes de 3 de part et d'autre de la virgule)."""
    ent, _, dec_ = chiffres.partition(".")
    g_ent = []
    while len(ent) > 3:
        g_ent.insert(0, ent[-3:])
        ent = ent[:-3]
    g_ent.insert(0, ent)
    g_dec = [dec_[i:i + 3] for i in range(0, len(dec_), 3)]
    if len(g_dec) > 1 and len(g_dec[-1]) == 1:          # pas de chiffre isolé : 8,854 187 8188 (comme le CODATA)
        g_dec[-2:] = [g_dec[-2] + g_dec[-1]]
    return " ".join(g_ent) + ("," + " ".join(g_dec) if dec_ else "")


def tex(chiffres, exp=None, incert=None, suite=False):
    """Nombre au format TeX : 6{,}626\\,070\\,15 \\times 10^{-34}, avec (15) et … éventuels."""
    s = grouper(chiffres).replace(",", "{,}").replace(" ", "\\,")
    if incert:
        s += f"({incert})"
    if suite:
        s += "\\ldots"
    if exp is not None:
        s += f" \\times 10^{{{exp}}}"
    return s


def nombre(chiffres, exp=None, incert=None):
    """Valeur numérique de l'écriture (pour la comparer à CODATA)."""
    return float(f"{chiffres}e{exp}" if exp is not None else chiffres)


def incert_valeur(chiffres, exp, incert):
    """(15) sur 6.67430 → 0.00015 ; renvoie l'incertitude-type absolue."""
    nb_dec = len(chiffres.partition(".")[2])
    return int(incert) * 10.0 ** (-nb_dec) * (10.0 ** exp if exp is not None else 1.0)


def proche(a, b, rel=1e-12):
    return abs(a - b) <= rel * max(abs(a), abs(b))


# ---------------------------------------------------------------- 1. les 7 constantes de définition
DEFINITION = [
    # (libellé, symbole, chiffres, exposant, unité, unité définie, clé scipy, valeur au lycée (TeX) ou None)
    ("fréquence de la transition hyperfine du césium 133", r"\Delta\nu_{\mathrm{Cs}}", "9192631770", None, "Hz", "la seconde",
     "hyperfine transition frequency of Cs-133", None),
    ("vitesse de la lumière dans le vide", "c", "299792458", None, "m/s", "le mètre", "speed of light in vacuum", r"3{,}00 \times 10^{8}"),
    ("constante de Planck", "h", "6.62607015", -34, "J·s", "le kilogramme", "Planck constant", r"6{,}63 \times 10^{-34}"),
    ("charge élémentaire", "e", "1.602176634", -19, "C", "l’ampère", "elementary charge", r"1{,}60 \times 10^{-19}"),
    ("constante de Boltzmann", r"k_{\mathrm{B}}", "1.380649", -23, "J/K", "le kelvin", "Boltzmann constant", r"1{,}38 \times 10^{-23}"),
    ("constante d’Avogadro", r"N_{\mathrm{A}}", "6.02214076", 23, "mol⁻¹", "la mole", "Avogadro constant", r"6{,}02 \times 10^{23}"),
    (r"efficacité lumineuse d’un rayonnement de fréquence $540 \times 10^{12}$ Hz", r"K_{\mathrm{cd}}", "683", None, "lm/W", "la candela",
     "luminous efficacy", None),
]
for _, _, ch, ex, _, _, cle, _ in DEFINITION:
    v, u = cod(cle)
    assert u == 0 and v == nombre(ch, ex), (cle, v)

# ---------------------------------------------------------------- 2. constantes exactes déduites
h, c, e, kB, NA = sc.h, sc.c, sc.e, sc.k, sc.N_A
DEDUITES = [
    # (libellé, symbole, chiffres affichés (tronqués), exposant, unité, valeur recalculée, clé scipy, au lycée)
    ("constante de Planck réduite, $\\hbar = \\dfrac{h}{2\\pi}$", None, "1.054571817", -34, "J·s", h / (2 * pi), "reduced Planck constant", None),
    ("constante des gaz parfaits, $R = N_{\\mathrm{A}}\\,k_{\\mathrm{B}}$", None, "8.314462618", None, "J·mol⁻¹·K⁻¹", NA * kB, "molar gas constant", r"8{,}314"),
    ("constante de Faraday, $\\mathcal{F} = N_{\\mathrm{A}}\\,e$", None, "96485.33212", None, "C/mol", NA * e, "Faraday constant", r"9{,}65 \times 10^{4}"),
    ("constante de Stefan-Boltzmann, $\\sigma$", None, "5.670374419", -8, "W·m⁻²·K⁻⁴", 2 * pi ** 5 * kB ** 4 / (15 * h ** 3 * c ** 2), "Stefan-Boltzmann constant", None),
    ("constante de la loi de Wien, $b$ (avec $\\lambda_{\\max}\\,T = b$)", None, "2.897771955", -3, "m·K", None, "Wien wavelength displacement law constant", r"2{,}90 \times 10^{-3}"),
    ("volume molaire d’un gaz parfait à 0 °C et 101 325 Pa", None, "22.41396954", None, "L/mol", NA * kB * 273.15 / 101325 * 1000, "molar volume of ideal gas (273.15 K, 101.325 kPa)", r"22{,}4"),
]
for lib, _, ch, ex, _, val, cle, _ in DEDUITES:
    v, u = cod(cle)
    if "molar volume" in cle:
        v *= 1000                                  # m³/mol → L/mol
    assert u == 0, cle
    if val is not None:
        assert proche(val, v, 1e-12), (cle, val, v)
    # affichage = troncature des chiffres exacts
    affiche = nombre(ch, ex)
    assert 0 <= v - affiche < 10.0 ** (ex if ex is not None else 0) * 10.0 ** (-len(ch.partition(".")[2])), (cle, v, affiche)

# ---------------------------------------------------------------- 3. constantes mesurées (CODATA 2022)
MESUREES = [
    # (libellé, symbole, chiffres, exposant, incertitude (derniers chiffres), unité, clé scipy, au lycée)
    ("constante de gravitation universelle", "G", "6.67430", -11, "15", "m³·kg⁻¹·s⁻²", "Newtonian constant of gravitation", r"6{,}67 \times 10^{-11}"),
    ("permittivité diélectrique du vide", r"\varepsilon_0", "8.8541878188", -12, "14", "F/m", "vacuum electric permittivity", r"8{,}85 \times 10^{-12}"),
    ("perméabilité magnétique du vide", r"\mu_0", "1.25663706127", -6, "20", "N/A²", "vacuum mag. permeability", r"4\pi \times 10^{-7}"),
    ("masse de l’électron", r"m_e", "9.1093837139", -31, "28", "kg", "electron mass", r"9{,}11 \times 10^{-31}"),
    ("masse du proton", r"m_p", "1.67262192595", -27, "52", "kg", "proton mass", r"1{,}67 \times 10^{-27}"),
    ("masse du neutron", r"m_n", "1.67492750056", -27, "85", "kg", "neutron mass", r"1{,}67 \times 10^{-27}"),
    ("unité de masse atomique (dalton)", r"u", "1.66053906892", -27, "52", "kg", "atomic mass constant", r"1{,}66 \times 10^{-27}"),
    ("constante de structure fine", r"\alpha", "7.2973525643", -3, "11", "(sans unité)", "fine-structure constant", None),
    ("rayon de Bohr", r"a_0", "5.29177210544", -11, "82", "m", "Bohr radius", None),
    ("constante de Rydberg", r"R_\infty", "10973731.568157", None, "12", "m⁻¹", "Rydberg constant", None),
]
for _, _, ch, ex, inc, _, cle, _ in MESUREES:
    v, u = cod(cle)
    assert proche(nombre(ch, ex), v, 1e-12), (cle, nombre(ch, ex), v)
    assert proche(incert_valeur(ch, ex, inc), u, 1e-9), (cle, incert_valeur(ch, ex, inc), u)
eps0 = cod("vacuum electric permittivity")[0]
K_COUL = 1 / (4 * pi * eps0)
assert proche(K_COUL, 8.9875517862e9, 1e-10)
assert proche(1 / cod("fine-structure constant")[0], 137.035999177, 1e-11)
assert abs(cod("vacuum mag. permeability")[0] / (4e-7 * pi) - 1) < 1e-9       # µ0 ≈ 4π × 10⁻⁷ à 10⁻⁹ près

# ---------------------------------------------------------------- 4. données astronomiques
G = cod("Newtonian constant of gravitation")[0]
GM_TERRE, GM_SOLEIL, GM_LUNE = 3.986004418e14, 1.32712440041e20, 4.9028e12    # IERS 2010, UAI 2015 (m³/s²)
M_TERRE, M_SOLEIL, M_LUNE = GM_TERRE / G, GM_SOLEIL / G, GM_LUNE / G
assert (f"{M_TERRE:.3e}", f"{M_SOLEIL:.3e}", f"{M_LUNE:.2e}") == ("5.972e+24", "1.988e+30", "7.35e+22")
AL = sc.c * 365.25 * 86400
assert AL == 9460730472580800.0
UA = 149597870700.0
assert sc.astronomical_unit == UA
g_lune = GM_LUNE / 1.7374e6 ** 2
assert f"{g_lune:.2f}" == "1.62"
JOUR_SIDERAL = 86164.0905
assert round(JOUR_SIDERAL) == 23 * 3600 + 56 * 60 + 4

# ---------------------------------------------------------------- 5. autres contrôles de la page
assert sc.physical_constants["standard acceleration of gravity"][0] == 9.80665
assert sc.atm == 101325.0 and sc.bar == 1e5 and sc.calorie == 4.184
# mmHg conventionnel (13,5951 g/cm³ × 9,806 65 m/s² × 1 mm) et torr (atm/760) : tous deux 133,322 Pa à l'affichage
assert f"{13595.1 * 9.80665 * 1e-3:.3f}" == f"{sc.torr:.3f}" == "133.322"
assert cod("electron volt")[0] == 1.602176634e-19
Vm20 = NA * kB * 293.15 / 101325 * 1000
assert f"{Vm20:.2f}" == "24.06"

UNITES_DERIVEES = [
    ("radian (rad)", "angle plan : 1 rad = 1 m/m"),
    ("stéradian (sr)", "angle solide : 1 sr = 1 m²/m²"),
    ("hertz (Hz)", "fréquence : 1 Hz = 1 s⁻¹"),
    ("newton (N)", "force : 1 N = 1 kg·m·s⁻²"),
    ("pascal (Pa)", "pression : 1 Pa = 1 N/m² = 1 kg·m⁻¹·s⁻²"),
    ("joule (J)", "énergie, travail, chaleur : 1 J = 1 N·m = 1 kg·m²·s⁻²"),
    ("watt (W)", "puissance : 1 W = 1 J/s = 1 kg·m²·s⁻³"),
    ("coulomb (C)", "charge électrique : 1 C = 1 A·s"),
    ("volt (V)", "tension électrique : 1 V = 1 W/A = 1 kg·m²·s⁻³·A⁻¹"),
    ("farad (F)", "capacité : 1 F = 1 C/V"),
    ("ohm (Ω)", "résistance : 1 Ω = 1 V/A"),
    ("siemens (S)", "conductance : 1 S = 1 A/V = 1 Ω⁻¹"),
    ("weber (Wb)", "flux magnétique : 1 Wb = 1 V·s"),
    ("tesla (T)", "champ magnétique : 1 T = 1 Wb/m²"),
    ("henry (H)", "inductance : 1 H = 1 Wb/A"),
    ("degré Celsius (°C)", "température Celsius : θ = T − 273,15"),
    ("lumen (lm)", "flux lumineux : 1 lm = 1 cd·sr"),
    ("lux (lx)", "éclairement lumineux : 1 lx = 1 lm/m²"),
    ("becquerel (Bq)", "activité d’une source radioactive : 1 Bq = 1 s⁻¹"),
    ("gray (Gy)", "dose absorbée : 1 Gy = 1 J/kg"),
    ("sievert (Sv)", "dose équivalente : 1 Sv = 1 J/kg"),
    ("katal (kat)", "activité catalytique : 1 kat = 1 mol/s"),
]
assert len(UNITES_DERIVEES) == 22          # les 22 unités dérivées ayant un nom spécial


def ligne(*cellules):
    return "| " + " | ".join(cellules) + " |"


def table_definition():
    L = [ligne("Constante", "Valeur exacte"), ligne("---", "---")]
    for lib, sym, ch, ex, unite, definit, _, lyc in DEFINITION:
        val = f"${tex(ch, ex)}$ {unite}"
        if lyc:
            val += f". Au lycée : ${lyc}$ {unite}"
        L.append(ligne(f"{lib}, ${sym}$ : définit {definit}", val))
    return "\n".join(L)


def table_deduites():
    L = [ligne("Constante", "Valeur exacte"), ligne("---", "---")]
    for lib, _, ch, ex, unite, _, _, lyc in DEDUITES:
        val = f"${tex(ch, ex, suite=True)}$ {unite}"
        if lyc:
            val += f". Arrondie : ${lyc}$ {unite}"
        L.append(ligne(lib, val))
    return "\n".join(L)


def table_mesurees():
    L = [ligne("Constante", "Valeur CODATA 2022"), ligne("---", "---")]
    for lib, sym, ch, ex, inc, unite, cle, lyc in MESUREES:
        val = f"${tex(ch, ex, inc)}$ {unite}"
        if cle == "fine-structure constant":
            val += ", soit $1/\\alpha \\approx 137{,}036$"
        if lyc:
            val += f". Arrondie : ${lyc}$" + (f" {unite}" if unite != "(sans unité)" else "")
        L.append(ligne(f"{lib}, ${sym}$", val))
        if cle == "vacuum electric permittivity":
            L.append(ligne("constante de la loi de Coulomb, $k = \\dfrac{1}{4\\pi\\varepsilon_0}$",
                           f"${tex('8.987551786', 9, suite=False)}$ N·m²·C⁻² environ. Arrondie : $8{{,}}99 \\times 10^{{9}}$ N·m²·C⁻²"))
    return "\n".join(L)


def table_derivees():
    return "\n".join([ligne("Unité (symbole)", "Grandeur et expression"), ligne("---", "---")]
                     + [ligne(u, d) for u, d in UNITES_DERIVEES])


V = {
    "TABLE_DEFINITION": table_definition(),
    "TABLE_DEDUITES": table_deduites(),
    "TABLE_MESUREES": table_mesurees(),
    "TABLE_DERIVEES": table_derivees(),
    "M_TERRE": tex(f"{M_TERRE / 1e24:.3f}", 24),
    "M_SOLEIL": tex(f"{M_SOLEIL / 1e30:.3f}", 30),
    "M_LUNE": tex(f"{M_LUNE / 1e22:.2f}", 22),
    "AL": tex("9.4607304725808", 15),
    "AL_ARR": tex("9.461", 15),
    "UA": tex("149597870700"),
    "UA_ARR": tex("1.496", 11),
    "G_LUNE": tex(f"{g_lune:.2f}"),
    "VM20": "24,06",
}


def remplacer(texte):
    for k_, v_ in V.items():
        texte = texte.replace("{" + k_ + "}", v_)
    reste = re.findall(r"(?<!overrightarrow)\{[A-Z][A-Z0-9_]+\}", texte)
    assert not reste, reste
    return texte


INFOS = {
    "slug": "unites-si-constantes-physiques",
    "titre": "Unités du Système international et constantes physiques",
    "titreCourt": "Unités SI et constantes physiques",
    "titreSeo": "Unités SI et constantes physiques : tableau complet et valeurs",
    "description": "Les 7 unités de base du Système international, les unités dérivées, les règles d’écriture et les constantes physiques (c, h, e, NA, G…) avec leurs valeurs.",
    "chapo": "Le tableau complet des unités du Système international (unités de base, unités dérivées, unités en usage) et des constantes physiques, avec les valeurs officielles CODATA 2022 et les valeurs arrondies utilisées dans les exercices, du collège à l’université.",
    "resume": "7 unités de base, unités dérivées, constantes c, h, e, NA, G",
    "vignette": "unites_de_base",
    "theme": "Données",
    "niveaux": ["Collège", "Lycée", "Supérieur"],
    "ordre": 2,
    "publie": "2026-11-19",
    "modifie": "2026-11-19",
    "motsCles": ["unités du système international", "unités SI", "tableau des unités", "7 unités de base", "unités dérivées",
                 "constantes physiques", "constantes fondamentales", "constante de Planck", "constante d'Avogadro",
                 "constante de Boltzmann", "vitesse de la lumière", "charge élémentaire", "constante de gravitation",
                 "constante des gaz parfaits", "masse de l'électron", "CODATA 2022", "analyse dimensionnelle",
                 "degré Celsius en kelvin", "électronvolt en joule"],
    "figures": [
        {"nom": "unites_de_base", "alt": "Les 7 unités de base du Système international et la constante qui définit chacune depuis 2019 : la seconde (s) par la fréquence du césium Δν(Cs), le mètre (m) par la vitesse de la lumière c, le kilogramme (kg) par la constante de Planck h, l’ampère (A) par la charge élémentaire e, le kelvin (K) par la constante de Boltzmann kB, la mole (mol) par la constante d’Avogadro NA et la candela (cd) par l’efficacité lumineuse Kcd."},
    ],
    "liees": ["tables/puissances-de-10-prefixes", "tables/tableau-de-conversion",
              "physique-chimie/quantite-de-matiere-concentration", "physique-chimie/formules-de-mecanique"],
    "faq": [
        ["Quelles sont les 7 unités de base du Système international ?", "Le mètre (m) pour les longueurs, le kilogramme (kg) pour les masses, la seconde (s) pour le temps, l’ampère (A) pour l’intensité du courant, le kelvin (K) pour la température, la mole (mol) pour la quantité de matière et la candela (cd) pour l’intensité lumineuse. Toutes les autres unités s’en déduisent : par exemple 1 N = 1 kg·m·s⁻²."],
        ["Quelle est la valeur de la constante de Planck ?", "Depuis le 20 mai 2019, elle vaut exactement h = 6,626 070 15 × 10⁻³⁴ J·s : cette valeur fixée sert à définir le kilogramme. Dans les exercices du lycée, on utilise h = 6,63 × 10⁻³⁴ J·s."],
        ["Quelle est la valeur de la constante d’Avogadro ?", "NA = 6,022 140 76 × 10²³ mol⁻¹, valeur exacte depuis 2019 : c’est le nombre d’entités dans une mole. Au lycée, on arrondit à 6,02 × 10²³ mol⁻¹."],
        ["Comment convertir des degrés Celsius en kelvins ?", "On ajoute 273,15 : T (en K) = θ (en °C) + 273,15. Ainsi 20 °C = 293,15 K et le zéro absolu, 0 K, vaut −273,15 °C. Une variation de 1 °C est égale à une variation de 1 K."],
        ["Quelle est la vitesse de la lumière ?", "Dans le vide, c = 299 792 458 m/s exactement : cette valeur définit le mètre. On l’arrondit souvent à 3,00 × 10⁸ m/s, soit environ 300 000 km/s."],
        ["Comment écrire correctement une unité ?", "Le symbole ne prend ni « s » au pluriel ni point final, et il est séparé du nombre par une espace : 5 kg, 20 °C, 3 m/s. Le nom s’écrit en minuscules (newton, ampère), mais le symbole d’une unité qui porte le nom d’un savant prend une majuscule (N, A, Pa). Le préfixe se colle au symbole : km, mA, µs."],
    ],
}

TEXTE = r"""<!-- optitab:1 -->
::: conseil Par où commencer ?
- **Au collège** : les parties I (les unités de base) et IV (écrire correctement une unité).
- **Au lycée** : les parties II, III, V et VII, avec les valeurs arrondies utilisées dans les exercices.
- **En prépa et à l’université** : les parties VI (constantes CODATA 2022) et VIII (analyse dimensionnelle).
- Les préfixes (kilo, milli…) et les conversions de longueurs, de masses ou de volumes ont leurs propres pages, en lien en bas de page.
:::

## I. Les 7 unités de base du SI {Collège}

Le **Système international d’unités** (SI) est utilisé dans le monde entier pour les sciences. Il repose sur sept unités de base :

| Grandeur | Unité | Symbole |
|---|---|---|
| longueur | mètre | m |
| masse | kilogramme | kg |
| temps | seconde | s |
| intensité du courant électrique | ampère | A |
| température | kelvin | K |
| quantité de matière | mole | mol |
| intensité lumineuse | candela | cd |

[IMAGE_1]

Depuis le **20 mai 2019**, chacune de ces unités est définie à partir d’une constante de la physique dont la valeur est fixée exactement (partie V). Le kilogramme n’est plus défini par le cylindre de platine iridié conservé à Sèvres, mais par la constante de Planck.

::: attention Le kilogramme, une unité de base avec un préfixe
L’unité de masse du SI est le **kilogramme**, et non le gramme. Dans une formule écrite en unités SI, les masses s’expriment en kg et les températures en kelvins.
:::

## II. Les unités dérivées {Lycée}

*De la Seconde à la Terminale.*

Toutes les autres unités s’obtiennent en multipliant ou en divisant les unités de base. Vingt-deux d’entre elles ont un nom spécial :

{TABLE_DERIVEES}

::: exemple Retrouver une unité dérivée
L’énergie cinétique vaut $E_c = \dfrac{1}{2}\,m\,v^2$ : son unité est kg·(m/s)² = kg·m²·s⁻², c’est-à-dire le joule. De même, $P = \dfrac{E}{t}$ donne J/s, c’est-à-dire le watt.
:::

D’autres unités n’ont pas de nom spécial :

| Grandeur | Unité SI |
|---|---|
| vitesse | m/s |
| accélération | m/s² |
| masse volumique | kg/m³ |
| concentration en quantité de matière | mol/m³ (en pratique mol/L) |
| masse molaire | kg/mol (en pratique g/mol) |
| moment d’une force | N·m |
| champ électrique | V/m |
| capacité thermique massique | J·kg⁻¹·K⁻¹ |
| vitesse angulaire | rad/s |

## III. Les unités en usage et les conversions utiles {Lycée}

*De la Seconde à la Terminale.*

Certaines unités ne font pas partie du SI, mais elles sont acceptées avec lui :

| Unité (symbole) | Valeur en unités SI |
|---|---|
| minute (min) | 60 s |
| heure (h) | 3 600 s |
| jour (d ou j) | 86 400 s |
| litre (L) | 1 dm³ = $10^{-3}$ m³ |
| tonne (t) | 1 000 kg |
| hectare (ha) | 10 000 m² |
| degré d’angle (°) | $\dfrac{\pi}{180}$ rad |
| électronvolt (eV) | $1{,}602\,176\,634 \times 10^{-19}$ J, exactement |
| dalton (Da), ou unité de masse atomique (u) | $1{,}660\,539\,068\,92 \times 10^{-27}$ kg |
| unité astronomique (au, souvent notée ua) | ${UA}$ m, exactement |

Et des unités hors SI que l’on rencontre souvent :

| Unité (symbole) | Valeur en unités SI |
|---|---|
| bar | $10^{5}$ Pa |
| atmosphère normale (atm) | 101 325 Pa |
| millimètre de mercure (mmHg) | 133,322 Pa |
| kilowattheure (kWh) | $3{,}6 \times 10^{6}$ J |
| calorie (cal) | 4,184 J |
| année-lumière (al) | ${AL}$ m, exactement |
| angström (Å) | $10^{-10}$ m |
| kilomètre par heure (km/h) | $\dfrac{1}{3{,}6}$ m/s |

::: formule Degrés Celsius et kelvins
$$T = \theta + 273{,}15$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $T$ | température absolue | K |
| $\theta$ | température Celsius | °C |

::: exemple
20 °C correspondent à $T = 20 + 273{,}15 = 293{,}15$ K. Le zéro absolu, 0 K, vaut −273,15 °C : aucune température ne peut être plus basse.
:::

::: attention Une variation de 1 °C vaut une variation de 1 K
Les deux échelles ont le même pas : pour un écart de température, $\Delta T = \Delta\theta$. Une eau qui passe de 20 °C à 30 °C s’est réchauffée de 10 K.
:::

## IV. Écrire correctement une unité {Collège}

- Le **symbole** est invariable : pas de « s » au pluriel, pas de point final. On écrit 5 kg, et non 5 kgs ou 5 kg.
- Une **espace** sépare le nombre du symbole : 20 °C, 50 %, 3 m/s. Seuls les degrés d’angle se collent au nombre : 45°.
- Le **nom** d’une unité s’écrit en minuscules, même s’il vient d’un savant : un newton, des ampères. Son **symbole** prend alors une majuscule : N, A, Pa, Hz, J, W, V, Ω.
- Le litre se note L ou l ; la lettre L évite la confusion avec le chiffre 1.
- Un **préfixe** se colle au symbole, sans espace, et on n’en met qu’un seul : km, mA, µs, mais jamais mµs.
- Un produit s’écrit avec un point ou une espace : N·m. Un quotient avec une barre ou une puissance négative : m/s ou m·s⁻¹. Une seule barre par unité : J/(kg·K), et non J/kg/K.

::: attention Majuscule ou minuscule : le sens change
m signifie mètre ou milli, M signifie méga. Ainsi ms est une milliseconde, mais mS est un millisiemens et Ms une mégaseconde. Recopier une unité sans respecter la casse peut changer la valeur d’un facteur un milliard.
:::

## V. Les 7 constantes qui définissent le SI {Lycée}

*De la Seconde à la Terminale.*

Depuis le 20 mai 2019, ces constantes ont une valeur **fixée exactement**, sans aucune incertitude. Ce sont elles qui définissent les unités : le mètre, par exemple, est la distance parcourue par la lumière dans le vide en 1/299 792 458 seconde.

{TABLE_DEFINITION}

## VI. Les autres constantes fondamentales {Supérieur}

Certaines constantes se déduisent des précédentes : elles sont donc **exactes** aussi, mais leur écriture décimale ne s’arrête pas.

{TABLE_DEDUITES}

À 20 °C et 101 325 Pa, le volume molaire d’un gaz parfait vaut {VM20} L/mol : c’est la valeur de 24 L/mol utilisée au lycée.

Les autres constantes sont **mesurées**. Valeurs recommandées par le CODATA (Committee on Data of the International Science Council) en 2022 :

{TABLE_MESUREES}

::: remarque Lire une incertitude entre parenthèses
Le nombre entre parenthèses est l’incertitude-type sur les derniers chiffres : $6{,}674\,30(15)$ signifie $6{,}674\,30 \pm 0{,}000\,15$. La constante de gravitation $G$ est la constante fondamentale la moins bien connue.
:::

Deux valeurs **conventionnelles** complètent le tableau : l’accélération normale de la pesanteur, $g_n = 9{,}806\,65$ m/s², et l’atmosphère normale, 101 325 Pa.

## VII. Données astronomiques et terrestres {Lycée}

*De la Seconde à la Terminale.*

| Donnée | Valeur |
|---|---|
| intensité de la pesanteur en France | $g \approx 9{,}81$ N/kg |
| intensité de la pesanteur sur la Lune | ${G_LUNE}$ N/kg |
| masse de la Terre | ${M_TERRE}$ kg |
| rayon moyen de la Terre | 6 371 km (6 378 km à l’équateur) |
| période de rotation de la Terre (jour sidéral) | 86 164 s, soit 23 h 56 min 4 s |
| masse de la Lune | ${M_LUNE}$ kg |
| rayon de la Lune | 1 737 km |
| distance moyenne Terre-Lune | 384 400 km |
| masse du Soleil | ${M_SOLEIL}$ kg |
| rayon du Soleil | 695 700 km |
| unité astronomique (distance moyenne Terre-Soleil) | ${UA_ARR}$ m |
| année-lumière | ${AL_ARR}$ m |

Ces données varient un peu d’une source à l’autre selon les arrondis : dans un exercice, on utilise toujours les valeurs données par l’énoncé.

## VIII. L’analyse dimensionnelle {Supérieur}

Chaque grandeur a une **dimension**, qui s’exprime avec les sept dimensions de base :

| Grandeur de base | Dimension |
|---|---|
| longueur | L |
| masse | M |
| temps | T |
| intensité du courant électrique | I |
| température | Θ |
| quantité de matière | N |
| intensité lumineuse | J |

::: formule Dimensions de quelques grandeurs
$$\begin{aligned}
[v] &= \mathrm{L \cdot T^{-1}} \qquad [a] = \mathrm{L \cdot T^{-2}} \\
[F] &= \mathrm{M \cdot L \cdot T^{-2}} \\
[E] &= \mathrm{M \cdot L^{2} \cdot T^{-2}}
\end{aligned}$$
:::

::: retenir Les règles de l’homogénéité
- Les deux membres d’une égalité ont la même dimension.
- On n’additionne que des grandeurs de même dimension.
- L’argument d’une exponentielle, d’un logarithme ou d’une fonction trigonométrique est sans dimension.
:::

::: exemple Vérifier une formule
Pour la période du pendule simple, $T_0 = 2\pi\sqrt{\dfrac{\ell}{g}}$ : $\left[\dfrac{\ell}{g}\right] = \dfrac{\mathrm{L}}{\mathrm{L \cdot T^{-2}}} = \mathrm{T^2}$, donc la racine a bien la dimension d’un temps. En revanche, $E = m\,v$ est forcément fausse : $[m\,v] = \mathrm{M \cdot L \cdot T^{-1}}$ n’est pas la dimension d’une énergie.
:::

::: exemple Retrouver l’unité d’une constante
De $F = G\,\dfrac{m_A\,m_B}{d^2}$, on tire $[G] = \dfrac{[F]\,[d]^2}{[m]^2} = \mathrm{M^{-1} \cdot L^{3} \cdot T^{-2}}$ : $G$ s’exprime en m³·kg⁻¹·s⁻², comme dans le tableau de la partie VI.
:::
"""

UNITES = ["J·mol⁻¹·K⁻¹", "N·m²·C⁻²", "m³·kg⁻¹·s⁻²", "W·m⁻²·K⁻⁴", "m/s²", "km/h", "km/s", "m/s", "N/kg", "L/mol", "C/mol",
          "J/K", "lm/W", "J·s", "N/A²", "F/m", "m·K", "mol⁻¹", "m⁻¹", "kg", "km", "min", "Pa", "Hz", "N", "J", "K",
          "°C", "s", "m", "%", "h", "C", "L",
          "W", "V", "Ω", "A", "S", "Wb", "Bq", "kat", "mol", "sr", "dm", "lm", "lx", "Gy", "Sv", "rad", "kWh", "eV", "Pa", "T"]
# Un exposant peut suivre le symbole (m², s⁻¹, Ω⁻¹) : il fait partie de l'unité.
UNITE = "(?:" + "|".join(re.escape(u) for u in sorted(UNITES, key=len, reverse=True)) + ")"
NOMBRE_UNITE = re.compile(r"(\d) (?=" + UNITE + r"(?![A-Za-zÀ-ÿ0-9’]))")
APRES_FORMULE = re.compile(r"^ (?=" + UNITE + r"(?![A-Za-zÀ-ÿ0-9’]))")
MILLIERS = re.compile(r"(\d) (?=\d{3}(?![\d,]))")
MATHS = re.compile(r"(\$\$[\s\S]*?\$\$|\$[^$\n]+\$)")


def insecables(texte):
    morceaux = MATHS.split(texte)
    for i in range(0, len(morceaux), 2):
        m = MILLIERS.sub(lambda x: x.group(1) + NNBSP, morceaux[i])
        m = NOMBRE_UNITE.sub(lambda x: x.group(1) + NBSP, m)
        if i and not morceaux[i - 1].startswith("$$"):
            m = APRES_FORMULE.sub(NBSP, m)
        morceaux[i] = m
    return "".join(morceaux)


def ecrire():
    infos = json.loads(json.dumps(INFOS, ensure_ascii=False))
    assert len(infos["titreSeo"]) <= 65 and 140 <= len(infos["description"]) <= 160, (len(infos["titreSeo"]), len(infos["description"]))
    for q, r in infos["faq"]:
        assert "$" not in r and "\\" not in r, q
    texte = remplacer(TEXTE)
    assert "\\text{" not in texte
    assert texte.count("[IMAGE_") == len(infos["figures"])
    entete = json.dumps(infos, ensure_ascii=False, indent=2)
    (ICI / "formulaire.md").write_text(insecables(f"---\n{entete}\n---\n{texte}"), encoding="utf-8", newline="\n")
    print("valeurs conformes à CODATA 2022 ; formulaire.md écrit :", len(infos["titreSeo"]), "car. (titre),",
          len(infos["description"]), "car. (description)")


if __name__ == "__main__":
    ecrire()
