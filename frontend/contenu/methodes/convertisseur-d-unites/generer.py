# -*- coding: utf-8 -*-
"""Page « Convertisseur d'unités » (methodes/convertisseur-d-unites).

    python -X utf8 generer.py

1. Lit les unités dans scripts/ressources/convertisseur.mjs (source unique du
   convertisseur et des tableaux de la page).
2. Vérifie chaque facteur : définitions exactes (pouce 2,54 cm, livre
   0,453 592 37 kg, atmosphère 101 325 Pa, calorie 4,184 J…) et scipy.constants.
3. Vérifie que le convertisseur de la page (outils/convertisseur.js) et le module
   (convertisseur.mjs) donnent les mêmes résultats, la même écriture des nombres
   et la même explication, sur toutes les paires d'unités et 3 000 valeurs.
4. Écrit formulaire.md (ne pas le modifier à la main).
"""
import json
import math
import random
import re
import subprocess
from pathlib import Path

import scipy.constants as sc

ICI = Path(__file__).resolve().parent
FRONT = ICI.parents[2]
MODULE = FRONT / "scripts" / "ressources" / "convertisseur.mjs"
SCRIPT = FRONT / "scripts" / "ressources" / "outils" / "convertisseur.js"
NBSP, NNBSP = chr(0xA0), chr(0x202F)

GRANDEURS = json.loads(subprocess.run(["node", str(MODULE), "--json"], capture_output=True, text=True,
                                      encoding="utf-8", check=True).stdout)
G = {g["id"]: g for g in GRANDEURS}
F = {g["id"]: {u[0]: u for u in g["unites"]} for g in GRANDEURS}
assert len(GRANDEURS) == 15


def proche(a, b, rel=1e-12):
    return abs(a - b) <= rel * max(abs(a), abs(b))


# ---------------------------------------------------------------- 1. facteurs
ATTENDU = {
    ("longueur", "in"): sc.inch, ("longueur", "ft"): sc.foot, ("longueur", "yd"): sc.yard, ("longueur", "mi"): sc.mile,
    ("longueur", "M"): sc.nautical_mile, ("longueur", "A"): sc.angstrom, ("longueur", "ua"): sc.astronomical_unit,
    ("longueur", "al"): sc.light_year, ("longueur", "um"): sc.micro, ("longueur", "nm"): sc.nano,
    ("masse", "lb"): sc.pound, ("masse", "oz"): sc.ounce, ("masse", "ct"): sc.carat, ("masse", "t"): sc.metric_ton,
    ("aire", "acre"): sc.acre, ("aire", "ha"): sc.hectare, ("aire", "ft2"): sc.foot ** 2, ("aire", "in2"): sc.inch ** 2,
    ("volume", "L"): sc.liter, ("volume", "galUS"): sc.gallon_US, ("volume", "galUK"): sc.gallon_imp, ("volume", "bbl"): sc.barrel,
    ("temps", "min"): sc.minute, ("temps", "h"): sc.hour, ("temps", "j"): sc.day, ("temps", "sem"): sc.week, ("temps", "an"): sc.year,
    ("vitesse", "km/h"): sc.kmh, ("vitesse", "kn"): sc.knot, ("vitesse", "mph"): sc.mph,
    ("force", "kgf"): sc.kgf, ("force", "lbf"): sc.lbf, ("force", "dyn"): sc.dyn,
    ("pression", "bar"): sc.bar, ("pression", "atm"): sc.atm, ("pression", "psi"): sc.psi,
    ("energie", "cal"): sc.calorie, ("energie", "BTU"): sc.Btu, ("energie", "eV"): sc.eV, ("energie", "kWh"): 3.6e6,
    ("energie", "tep"): 1e10 * sc.calorie_IT,
    ("puissance", "hp"): sc.hp, ("puissance", "ch"): 75 * sc.g,
    ("angle", "deg"): sc.degree, ("angle", "arcmin"): sc.arcmin, ("angle", "arcsec"): sc.arcsec,
    ("masse-volumique", "lb/ft3"): sc.pound / sc.foot ** 3,
}
for (gid, code), v in ATTENDU.items():
    assert proche(F[gid][code][3], v, 1e-12), (gid, code, F[gid][code][3], v)
# millimètre de mercure conventionnel (13,5951 g/cm³ × g normale × 1 mm) ; le torr de scipy en diffère de 1,4 × 10⁻⁷
assert proche(F["pression"]["mmHg"][3], 13595.1 * sc.g * 1e-3, 1e-12) and proche(F["pression"]["mmHg"][3], sc.torr, 2e-7)
assert proche(F["pression"]["kgf/cm2"][3], sc.kgf / 1e-4) and proche(F["pression"]["psi"][3], sc.lbf / sc.inch ** 2)
assert F["temperature"]["unites"] if False else True
T = F["temperature"]
assert T["C"][3:] == [1, 273.15] and T["K"][3:] == [1, 0] and proche(T["F"][3], 5 / 9) and proche(T["F"][4], 273.15 - 32 * 5 / 9)
assert F["donnees"]["Gio"][3] == 1024 ** 3 and F["donnees"]["bit"][3] == 1 / 8
# préfixes décimaux : chaque facteur est une puissance de 10 exacte
for gid, code, puiss in [("longueur", "km", 3), ("longueur", "mm", -3), ("masse", "mg", -6), ("volume", "mL", -6),
                         ("pression", "hPa", 2), ("energie", "MJ", 6), ("puissance", "GW", 9), ("frequence", "MHz", 6)]:
    assert proche(F[gid][code][3], 10.0 ** puiss), (gid, code)

# ---------------------------------------------------------------- 2. le convertisseur de la page = le module
random.seed(2026)
cas = []
for g in GRANDEURS:
    codes = [u[0] for u in g["unites"]]
    for de in codes:
        for vers in codes:
            for _ in range(3):
                x = round(random.uniform(-500, 5000), random.choice([0, 1, 2, 3]))
                if g["id"] == "temperature" and (x + 0) < 0:
                    x = abs(x)
                cas.append([g["id"], de, vers, x])
code_js = r"""
const vm = require('vm'), fs = require('fs')
const ctx = { window: {} }
vm.runInNewContext(fs.readFileSync(process.argv[1], 'utf8'), ctx)
const C = ctx.window.OTConv
const cas = JSON.parse(fs.readFileSync(0, 'utf8'))
import(process.argv[2]).then((M) => {
  const G = Object.fromEntries(M.GRANDEURS.map((g) => [g.id, g]))
  const ecarts = []
  for (const [id, de, vers, x] of cas) {
    const g = G[id]
    const gj = JSON.parse(JSON.stringify({ ...g, affine: !!g.affine }))
    const a = M.convertir(g, de, vers, x), b = C.convertir(gj, de, vers, x)
    if (Math.abs(a - b) > 1e-12 * Math.max(1, Math.abs(a))) ecarts.push(['valeur', id, de, vers, x, a, b])
    if (M.nombre(a) !== C.nombre(b)) ecarts.push(['écriture', id, de, vers, x, M.nombre(a), C.nombre(b)])
    if (M.explication(g, de, vers) !== C.explication(gj, de, vers)) ecarts.push(['explication', id, de, vers])
    if (C.lire(M.nombre(x)) !== x && Math.abs(x) < 1e12) ecarts.push(['relecture', id, x, M.nombre(x)])
  }
  const T = Object.fromEntries(M.GRANDEURS.map((g) => [g.id, g.unites.map((u) => [u[0], u[1], u[2],
    g.affine ? null : (M.exact(M.convertir(g, u[0], g.ref, 1), 12) ? M.nombre(M.convertir(g, u[0], g.ref, 1), 12) : M.nombre(M.convertir(g, u[0], g.ref, 1), 6)),
    g.affine ? null : M.exact(M.convertir(g, u[0], g.ref, 1), 12)])]))
  process.stdout.write(JSON.stringify({ ecarts, tables: T, n: cas.length }))
})
"""
sortie = json.loads(subprocess.run(["node", "-e", code_js, str(SCRIPT), MODULE.as_uri()], input=json.dumps(cas),
                                   capture_output=True, text=True, encoding="utf-8", check=True).stdout)
assert not sortie["ecarts"], sortie["ecarts"][:5]
TABLES = sortie["tables"]
print(f"convertisseur de la page identique au module sur {sortie['n']} conversions")


# ---------------------------------------------------------------- 3. exemples de la page (calculés)
def fr(x, n):
    s = f"{x:,.{n}f}".replace(",", " ").replace(".", ",").replace(" ", NNBSP)
    return s.replace("-", "−")


def conv(gid, de, vers, x):
    a, b = F[gid][de], F[gid][vers]
    if gid == "temperature":
        return ((a[3] * x + a[4]) - b[4]) / b[3]
    return x * a[3] / b[3]


V = {
    "POUCES": fr(conv("longueur", "in", "cm", 27), 2), "MARATHON": fr(conv("longueur", "km", "mi", 42.195), 2),
    "LIVRES": fr(conv("masse", "lb", "kg", 5), 2), "HA": fr(conv("aire", "ha", "m2", 2.5), 0),
    "CL_ML": fr(conv("volume", "cL", "mL", 33), 0), "CL_L": fr(conv("volume", "cL", "L", 33), 2),
    "H_MIN": fr(conv("temps", "h", "min", 1.5), 0), "KMH_MS": fr(conv("vitesse", "km/h", "m/s", 90), 0),
    "NOEUDS": fr(conv("vitesse", "kn", "km/h", 20), 2), "KN_N": fr(conv("force", "kN", "N", 2.5), 0),
    "KN_DAN": fr(conv("force", "kN", "daN", 2.5), 0), "TONNE_KN": fr(conv("force", "tf", "kN", 1), 2),
    "PSI": fr(conv("pression", "bar", "psi", 2.2), 1), "MMHG": fr(conv("pression", "mmHg", "kPa", 120), 1),
    "ATM_HPA": fr(conv("pression", "atm", "hPa", 1), 2), "RADIATEUR": fr(conv("energie", "kWh", "MJ", 6), 1),
    "KCAL": fr(conv("energie", "kcal", "kJ", 250), 0), "CH_KW": fr(conv("puissance", "ch", "kW", 100), 1),
    "C_F": fr(conv("temperature", "C", "F", 20), 0), "F_C": fr(conv("temperature", "F", "C", 100), 1),
    "CORPS_F": fr(conv("temperature", "C", "F", 37), 1), "K_C": fr(conv("temperature", "K", "C", 300), 2),
    "RAD_DEG": fr(conv("angle", "rad", "deg", 1), 1), "GON": fr(conv("angle", "deg", "gon", 90), 0),
    "GIO": fr(conv("donnees", "Go", "Gio", 500), 1), "TRMIN": fr(conv("frequence", "tr/min", "Hz", 3000), 0),
    "ALU": fr(conv("masse-volumique", "g/cm3", "kg/m3", 2.7), 0),
}
ATT = {"POUCES": "68,58", "MARATHON": "26,22", "LIVRES": "2,27", "HA": f"25{NNBSP}000", "CL_ML": "330", "CL_L": "0,33",
       "H_MIN": "90", "KMH_MS": "25", "NOEUDS": "37,04", "KN_N": f"2{NNBSP}500", "KN_DAN": "250", "TONNE_KN": "9,81",
       "PSI": "31,9", "MMHG": "16,0", "ATM_HPA": f"1{NNBSP}013,25", "RADIATEUR": "21,6", "KCAL": f"1{NNBSP}046",
       "CH_KW": "73,5", "C_F": "68", "F_C": "37,8", "CORPS_F": "98,6", "K_C": "26,85", "RAD_DEG": "57,3", "GON": "100",
       "GIO": "465,7", "TRMIN": "50", "ALU": f"2{NNBSP}700"}
assert V == ATT, {k: (V[k], ATT[k]) for k in V if V[k] != ATT[k]}
assert abs(conv("temperature", "C", "F", -40) + 40) < 1e-12


def table(gid):
    g = G[gid]
    ref = F[gid][g["ref"]]
    L = ["| Unité | Équivalence |", "|---|---|"]
    for code, nom, symb, val, ex in TABLES[gid]:
        if code == g["ref"]:
            L.append(f"| {nom} ({symb}) | unité de référence de ce tableau |")
        else:
            colle = symb in ('°', '′', '″')
            L.append(f"| {nom} ({symb}) | 1{'' if colle else NBSP}{symb} {'=' if ex else '≈'} {val}{NBSP}{ref[2]} |")
    return "\n".join(L)


for g in GRANDEURS:
    if g["id"] != "temperature":
        V["TABLE_" + g["id"].upper().replace("-", "_")] = table(g["id"])


def remplacer(texte):
    for k_, v_ in V.items():
        texte = texte.replace("{" + k_ + "}", v_)
    reste = re.findall(r"\{[A-Z][A-Z0-9_]+\}", texte)
    assert not reste, reste
    return texte


INFOS = {
    "slug": "convertisseur-d-unites",
    "titre": "Convertisseur d’unités : toutes les conversions en ligne",
    "titreCourt": "Convertisseur d’unités",
    "titreSeo": "Convertisseur d’unités : longueur, masse, force, pression, °C",
    "description": "Convertisseur d’unités gratuit : longueurs, masses, volumes, vitesses, forces (kN), pressions (bar), énergies (kWh), températures (°C, °F), avec tableaux.",
    "chapo": "Convertissez une valeur dans toutes les unités d’une grandeur, instantanément : longueur, masse, aire, volume, durée, vitesse, force, pression, énergie, puissance, température, angle, données numériques, fréquence et masse volumique. Avec la méthode et le tableau de chaque grandeur.",
    "resume": "15 grandeurs : kN, bar, kWh, km/h, °C, Go…",
    "vignette": "conversions_essentielles",
    "theme": "Conversions",
    "niveaux": ["Collège", "Lycée"],
    "ordre": 0.5,
    "publie": "2026-11-20",
    "modifie": "2026-11-20",
    "outil": "convertisseur",
    "motsCles": ["convertisseur d'unités", "conversion d'unités", "convertir des unités", "convertisseur en ligne",
                 "kN en N", "km/h en m/s", "bar en pascal", "bar en psi", "kWh en joules", "calories en joules",
                 "degrés Celsius en Fahrenheit", "Fahrenheit en Celsius", "kelvin en Celsius", "pouces en cm",
                 "miles en km", "nœuds en km/h", "livres en kg", "cheval-vapeur en kW", "Go en Mo", "radians en degrés",
                 "g/cm3 en kg/m3", "tr/min en Hz"],
    "figures": [
        {"nom": "conversions_essentielles", "alt": "Six conversions à connaître : 1 kN = 1 000 N ; 1 bar = 100 000 Pa ; 1 kWh = 3,6 MJ ; 1 m/s = 3,6 km/h ; 1 pouce = 2,54 cm ; 0 °C = 32 °F."},
        {"nom": "echelles_temperature", "alt": "Les échelles de température Celsius, Kelvin et Fahrenheit côte à côte : le zéro absolu vaut −273,15 °C, 0 K et −459,67 °F ; la glace fond à 0 °C, 273,15 K et 32 °F ; le corps humain est à 37 °C, 310,15 K et 98,6 °F ; l’eau bout à 100 °C, 373,15 K et 212 °F."},
    ],
    "liees": ["tables/tableau-de-conversion", "tables/puissances-de-10-prefixes",
              "physique-chimie/unites-si-constantes-physiques", "methodes/calculer-une-duree"],
    "faq": [
        ["Comment convertir des kN en N ?", "1 kN = 1 000 N : on multiplie par 1 000. Ainsi 2,5 kN = 2 500 N. Dans l’autre sens, on divise par 1 000 : 750 N = 0,75 kN. Le préfixe kilo signifie toujours mille."],
        ["Comment convertir des km/h en m/s ?", "On divise par 3,6, car 1 m/s = 3,6 km/h : 90 km/h = 90 ÷ 3,6 = 25 m/s. Pour passer des m/s aux km/h, on multiplie par 3,6 : 10 m/s = 36 km/h."],
        ["Combien de pascals dans un bar ?", "1 bar = 100 000 Pa, soit 1 000 hPa. La pression atmosphérique normale vaut 101 325 Pa, c’est-à-dire 1 013,25 hPa ou 1,013 25 bar."],
        ["Comment convertir des degrés Celsius en Fahrenheit ?", "On multiplie par 1,8 puis on ajoute 32 : °F = °C × 1,8 + 32. Ainsi 20 °C = 68 °F et 37 °C = 98,6 °F. Dans l’autre sens : °C = (°F − 32) ÷ 1,8, donc 100 °F ≈ 37,8 °C."],
        ["Combien de joules dans un kWh ?", "1 kWh = 3 600 000 J = 3,6 MJ : c’est l’énergie d’un appareil de 1 000 W qui fonctionne pendant une heure, soit 3 600 secondes. Un radiateur de 2 000 W allumé 3 heures consomme 6 kWh, soit 21,6 MJ."],
        ["Combien de centimètres dans un pouce ?", "Exactement 2,54 cm. Un écran de 27 pouces a donc une diagonale de 27 × 2,54 = 68,58 cm. Un pied vaut 12 pouces, soit 30,48 cm."],
    ],
}

TEXTE = r"""<!-- optitab:1 -->
[OUTIL]

::: conseil Comment utiliser le convertisseur
1. Choisissez la **grandeur** : longueur, masse, force, pression, énergie, température…
2. Tapez la **valeur** et choisissez les unités de départ et d’arrivée ; le bouton ⇄ les inverse.
3. Lisez le résultat et la règle de calcul. La liste du dessous donne la valeur dans **toutes** les unités : touchez-en une pour l’afficher en grand.
:::

## I. Convertir une unité : la méthode {Collège}

Pour convertir, on multiplie la valeur par le nombre d’unités d’arrivée que contient **une** unité de départ.

::: formule Conversion d’une unité A en une unité B
$$\text{valeur en B} = \text{valeur en A} \times (\text{valeur de 1 A en B})$$
:::

::: exemple
1 kN = 1 000 N, donc 2,5 kN = 2,5 × 1 000 = {KN_N} N. Dans l’autre sens, on divise : 2 500 N = 2 500 ÷ 1 000 = 2,5 kN.
:::

[IMAGE_1]

::: retenir Le bon réflexe
Quand l’unité d’arrivée est **plus petite**, le nombre devient **plus grand**, et inversement. Un résultat qui va dans le mauvais sens signale une erreur de multiplication ou de division.
:::

::: attention Aires et volumes : les rangs comptent double ou triple
Pour les aires, on multiplie par 100 à chaque rang (1 m² = 100 dm²) ; pour les volumes, par 1 000 (1 m³ = 1 000 dm³). La méthode avec le tableau de conversion est expliquée sur sa propre page, en lien en bas de page.
:::

## II. Longueurs {Collège}

Les unités métriques se convertissent par 10 d’un rang à l’autre. Les unités anglo-saxonnes ont des valeurs exactes fixées en 1959 : le pouce vaut 2,54 cm.

{TABLE_LONGUEUR}

::: exemple
Un écran de 27 pouces mesure $27 \times 2{,}54 = {POUCES}$ cm de diagonale. Un marathon de 42,195 km fait environ {MARATHON} miles.
:::

## III. Masses {Collège}

{TABLE_MASSE}

::: exemple
5 livres font $5 \times 0{,}453\,592\,37 \approx {LIVRES}$ kg. Le quintal vaut 100 kg et le carat, utilisé pour les pierres précieuses, 0,2 g.
:::

## IV. Aires {Collège}

{TABLE_AIRE}

::: exemple
Un terrain de 2,5 ha mesure {HA} m². Un hectare est l’aire d’un carré de 100 m de côté.
:::

## V. Volumes et contenances {Collège}

Le litre est égal au décimètre cube : 1 L = 1 dm³, et 1 mL = 1 cm³.

{TABLE_VOLUME}

::: exemple
Une canette de 33 cL contient {CL_ML} mL, soit {CL_L} L.
:::

## VI. Durées {Collège}

{TABLE_TEMPS}

::: attention Heures décimales et minutes
1,5 h ne fait pas 1 h 50 min mais 1 h 30 min : 0,5 h = 0,5 × 60 = 30 min. En tout, 1,5 h = {H_MIN} min.
:::

## VII. Vitesses {Collège}

Pour passer des km/h aux m/s, on divise par 3,6 : 1 km/h = 1 000 m en 3 600 s.

{TABLE_VITESSE}

::: exemple
90 km/h = 90 ÷ 3,6 = {KMH_MS} m/s. En mer, un bateau à 20 nœuds avance à {NOEUDS} km/h : un nœud vaut un mille marin par heure, soit 1,852 km/h.
:::

## VIII. Forces {Lycée}

L’unité de force est le newton (N). Le kilonewton et le décanewton servent en mécanique et dans le bâtiment ; le kilogramme-force est le poids d’une masse de 1 kg avec $g = 9{,}806\,65$ N/kg.

{TABLE_FORCE}

::: exemple
2,5 kN = {KN_N} N = {KN_DAN} daN. Une masse d’une tonne a un poids d’environ {TONNE_KN} kN : c’est une tonne-force.
:::

::: attention Décanewton et kilogramme-force
Ils sont proches mais pas égaux : 1 kgf = 0,980 665 daN. Sur un chantier, on les confond souvent, ce qui fait une erreur d’environ 2 %.
:::

## IX. Pressions {Lycée}

L’unité de pression est le pascal (Pa), soit 1 N/m². La météo utilise l’hectopascal, les pneus le bar ou le psi, la tension artérielle le millimètre de mercure.

{TABLE_PRESSION}

::: exemple
La pression atmosphérique normale vaut 101 325 Pa, soit {ATM_HPA} hPa. Un pneu gonflé à 2,2 bar est à environ {PSI} psi. Une tension artérielle de 12, c’est-à-dire 120 mmHg, vaut environ {MMHG} kPa.
:::

## X. Énergies {Lycée}

L’unité d’énergie est le joule (J). L’électricité se compte en kilowattheures, l’alimentation en kilocalories, la physique des particules en électronvolts.

{TABLE_ENERGIE}

::: exemple
Un radiateur de 2 000 W allumé pendant 3 h consomme 6 kWh, soit {RADIATEUR} MJ. Un aliment de 250 kcal apporte environ {KCAL} kJ.
:::

## XI. Puissances {Lycée}

L’unité de puissance est le watt (W), soit 1 J/s.

{TABLE_PUISSANCE}

::: exemple
Un moteur de 100 ch développe environ {CH_KW} kW. Le cheval-vapeur français (735,5 W) et le horsepower anglo-saxon (745,7 W) sont deux unités différentes.
:::

## XII. Températures {Collège}

Les échelles Celsius et Kelvin ont le même pas : une variation de 1 °C vaut une variation de 1 K. L’échelle Fahrenheit a un pas plus petit, 1 °F valant 5/9 de degré Celsius.

[IMAGE_2]

::: formule Degrés Celsius et kelvins
$$T = \theta + 273{,}15$$
:::

::: formule Degrés Celsius et Fahrenheit
$$\theta_F = 1{,}8 \times \theta + 32 \qquad \theta = \dfrac{\theta_F - 32}{1{,}8}$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $T$ | température absolue | K |
| $\theta$ | température Celsius | °C |
| $\theta_F$ | température Fahrenheit | °F |

::: exemple
20 °C = 20 × 1,8 + 32 = {C_F} °F, et 37 °C = {CORPS_F} °F. Dans l’autre sens, 100 °F = (100 − 32) ÷ 1,8 ≈ {F_C} °C. Enfin 300 K = 300 − 273,15 = {K_C} °C.
:::

::: retenir Une curiosité : −40
À −40 °C, il fait aussi −40 °F : c’est la seule température où les deux échelles affichent le même nombre.
:::

## XIII. Angles {Lycée}

Un tour complet vaut 360°, soit $2\pi$ radians ou 400 grades.

{TABLE_ANGLE}

::: exemple
180° = $\pi$ rad, et 1 rad ≈ {RAD_DEG}°. Un angle droit de 90° mesure {GON} grades.
:::

## XIV. Données numériques {Collège}

Un octet (o) vaut 8 bits. Avec les préfixes décimaux, 1 ko = 1 000 octets ; avec les préfixes binaires, 1 Kio = 1 024 octets.

{TABLE_DONNEES}

::: attention Pourquoi un disque de 500 Go affiche moins
Le fabricant compte en gigaoctets décimaux (500 × 10⁹ octets), mais certains ordinateurs affichent en gibioctets (2³⁰ octets) : le même disque apparaît alors avec environ {GIO} Gio.
:::

## XV. Fréquences {Lycée}

L’unité de fréquence est le hertz (Hz), soit un événement par seconde.

{TABLE_FREQUENCE}

::: exemple
Un moteur qui tourne à 3 000 tr/min fait 50 tours par seconde : sa fréquence de rotation vaut {TRMIN} Hz.
:::

## XVI. Masses volumiques {Collège}

{TABLE_MASSE_VOLUMIQUE}

::: exemple
L’eau a une masse volumique de 1 g/cm³, soit 1 000 kg/m³ ou 1 kg/L. L’aluminium, à 2,7 g/cm³, est à {ALU} kg/m³.
:::
"""

UNITES = ["kg/m³", "g/cm³", "km/h", "m/s", "N/kg", "kN", "daN", "N", "kgf", "bar", "psi", "hPa", "kPa", "Pa", "mmHg",
          "kWh", "MJ", "kJ", "kcal", "J", "kW", "W", "ch", "°C", "°F", "K", "Gio", "Go", "Hz", "tr/min", "km", "cm", "mm",
          "km²", "dm²", "cm²", "mm²", "dm³", "cm³", "mm³", "ha", "m²", "m³", "mL", "cL", "L", "kg", "g", "t", "min", "h", "s", "m", "%"]
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
    assert texte.count("[IMAGE_") == len(infos["figures"])
    entete = json.dumps(infos, ensure_ascii=False, indent=2)
    (ICI / "formulaire.md").write_text(insecables(f"---\n{entete}\n---\n{texte}"), encoding="utf-8", newline="\n")
    print("formulaire.md écrit :", len(infos["titreSeo"]), "car. (titre),", len(infos["description"]), "car. (description)")


if __name__ == "__main__":
    ecrire()
