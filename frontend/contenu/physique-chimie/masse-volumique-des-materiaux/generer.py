# -*- coding: utf-8 -*-
"""Page « Masse volumique des matériaux » (physique-chimie/masse-volumique-des-materiaux).

    python -X utf8 generer.py

Écrit materiaux.json (données de l'outil de recherche et de calcul, lues par
scripts/ressources/masses-volumiques.mjs) et formulaire.md (ne pas les modifier
à la main).

Sources et contrôles :
- Poids volumiques de construction : EN 1991-1-1:2002 (Eurocode 1), annexe A
  informative, tableaux A.1 (béton, mortier), A.2 (pierres naturelles), A.3
  (bois), A.4 (métaux), A.5 (verre), A.6 (matériaux de pont), A.7 (matériaux
  stockés), valeurs relevées dans le texte de la norme le 20/11/2026 (en kN/m³,
  matériaux secs). Contrôle : chaque valeur physique de la page multipliée par
  g = 9,81 N/kg tombe dans la fourchette de l'Eurocode à 3 % près (l'Eurocode
  arrondit avec g ≈ 10).
- Métaux purs : comparés aux masses volumiques de PubChem (sources/pubchem.csv),
  écart maximal 1 %.
- Gaz : calculés par la loi des gaz parfaits (ρ = P M / R T, R exacte) avec les
  masses molaires de PubChem ; contrôle à 0 °C contre les valeurs de PubChem.
- Acier : 7 850 kg/m³ (EN 1993-1-1, § 3.2.6) ; acier inoxydable 7 900 à 8 000 kg/m³ (EN 1993-1-4).
- Liquides, bois, sols et autres matériaux : valeurs de référence usuelles
  (ordre de grandeur), présentées en fourchettes quand elles varient.
"""
import csv
import json
import re
import unicodedata
from pathlib import Path

ICI = Path(__file__).resolve().parent
NBSP, NNBSP = chr(0xA0), chr(0x202F)
G = 9.81
R = 8.314462618
P0 = 101325.0

PUBCHEM = {r["Symbol"]: r for r in csv.DictReader((ICI / "sources" / "pubchem.csv").open(encoding="utf-8"))}


def masse_molaire(formule):
    """Masse molaire (g/mol) d'une formule simple : « CO2 », « CH4 », « H2O »."""
    total = 0.0
    for sym, n in re.findall(r"([A-Z][a-z]?)(\d*)", formule):
        total += float(PUBCHEM[sym]["AtomicWeight"]) * (int(n) if n else 1)
    return total


M_AIR = 28.965          # air sec (g/mol), masse molaire moyenne usuelle


def rho_gaz(M, T):
    return P0 * M / 1000 / (R * T)


# contrôle des gaz à 0 °C contre PubChem (valeurs en g/L = kg/m³)
for sym, formule in [("H", "H2"), ("He", "He"), ("N", "N2"), ("O", "O2")]:
    calc = rho_gaz(masse_molaire(formule), 273.15)
    ref = float(PUBCHEM[sym]["Density"]) * 1000
    assert abs(calc / ref - 1) < 0.003, (formule, calc, ref)
assert abs(rho_gaz(M_AIR, 273.15) - 1.293) < 0.001 and abs(rho_gaz(M_AIR, 293.15) - 1.204) < 0.001

# ---------------------------------------------------------------- données
# Chaque ligne : (nom, valeur ou (min, max)) ; masses volumiques en kg/m³, poids volumiques en kN/m³.
LIQUIDES = [
    ("eau pure à 4 °C", 1000), ("eau à 20 °C", 998), ("eau de mer", (1020, 1030)), ("lait", (1028, 1035)),
    ("huile d’olive", (910, 920)), ("huile de tournesol", (915, 925)), ("miel", (1380, 1450)),
    ("éthanol (alcool)", 789), ("acétone", 784), ("glycérine", 1261), ("essence (SP95, SP98)", (720, 775)),
    ("gazole", (820, 845)), ("kérosène", (775, 840)), ("mercure", 13546),
]
GAZ = [  # (nom, formule ou None pour l'air)
    ("air", None), ("dihydrogène", "H2"), ("hélium", "He"), ("méthane", "CH4"), ("diazote", "N2"),
    ("dioxygène", "O2"), ("argon", "Ar"), ("dioxyde de carbone", "CO2"),
]
METAUX = [  # (nom, valeur, symbole PubChem pour un métal pur)
    ("magnésium", 1740, "Mg"), ("aluminium", 2700, "Al"), ("titane", 4510, "Ti"), ("zinc", 7130, "Zn"),
    ("fonte", (7100, 7300), None), ("chrome", 7190, "Cr"), ("étain", 7290, "Sn"), ("acier", 7850, None),
    ("fer", 7870, "Fe"), ("acier inoxydable", (7900, 8000), None), ("laiton", (8400, 8700), None),
    ("bronze", (8700, 8900), None), ("nickel", 8910, "Ni"), ("cuivre", 8960, "Cu"), ("argent", 10500, "Ag"),
    ("plomb", 11340, "Pb"), ("or", 19300, "Au"), ("tungstène", 19300, "W"), ("platine", 21450, "Pt"),
    ("osmium", 22590, "Os"),
]
for nom, v, sym in METAUX:
    if sym:
        ref = float(PUBCHEM[sym]["Density"]) * 1000
        assert abs(v / ref - 1) <= 0.01, (nom, v, ref)
assert max(float(r["Density"] or 0) for r in PUBCHEM.values() if r["StandardState"] == "Solid") == float(PUBCHEM["Os"]["Density"])

EC_BETON = [  # EN 1991-1-1, tableaux A.1 et A.2 (kN/m³)
    ("béton de masse volumique normale, non armé", 24.0), ("béton armé ou précontraint", 25.0),
    ("béton léger (classes LC 1,0 à LC 2,0)", (9.0, 20.0)), ("mortier de ciment", (19.0, 23.0)),
    ("mortier bâtard (chaux et ciment)", (18.0, 20.0)), ("mortier de chaux", (12.0, 18.0)),
    ("mortier de plâtre", (12.0, 18.0)), ("granit", (27.0, 30.0)), ("basalte", (27.0, 31.0)),
    ("grès", (21.0, 27.0)), ("calcaire dense", (20.0, 29.0)), ("ardoise", 28.0), ("gneiss", 30.0),
]
EC_AUTRES = [  # EN 1991-1-1, tableaux A.4 à A.7 (kN/m³)
    ("acier", (77.0, 78.5)), ("aluminium", 27.0), ("cuivre", (87.0, 89.0)), ("fonte", (71.0, 72.5)),
    ("laiton, bronze", (83.0, 85.0)), ("plomb", (112.0, 114.0)), ("zinc", (71.0, 72.0)), ("verre en plaques", 25.0),
    ("enrobé bitumineux (chaussée)", (24.0, 25.0)), ("asphalte coulé", (18.0, 22.0)), ("sable sec", (15.0, 16.0)),
    ("gravier, ballast (en vrac)", (15.0, 16.0)), ("ciment en vrac", 16.0), ("ciment en sacs", 15.0),
    ("gypse broyé (plâtre en poudre)", 15.0), ("chaux", 13.0), ("eau douce", 10.0),
]
EC_BOIS = [  # EN 1991-1-1, tableau A.3 (kN/m³)
    ("bois massif, classe C18 (résineux)", 3.8), ("bois massif, classe C24 (résineux)", 4.2),
    ("bois massif, classe C30 (résineux)", 4.6), ("bois massif, classe D30 (feuillus)", 6.4),
    ("bois massif, classe D40 (feuillus)", 7.0), ("lamellé-collé GL24h", 3.7), ("lamellé-collé GL28h", 4.0),
    ("lamellé-collé GL32h", 4.2), ("contreplaqué de résineux", 5.0), ("contreplaqué de bouleau", 7.0),
    ("panneau OSB", 7.0), ("panneau de particules", (7.0, 8.0)), ("panneau de fibres MDF", 8.0),
]
BOIS = [  # bois sec à l'air (environ 12 % d'humidité), valeurs moyennes
    ("balsa", (100, 200)), ("peuplier", (400, 500)), ("épicéa", (400, 500)), ("sapin", (400, 500)),
    ("pin sylvestre", (500, 550)), ("douglas", (500, 550)), ("mélèze", (550, 650)), ("châtaignier", (550, 650)),
    ("noyer", (600, 700)), ("teck", (600, 700)), ("chêne", (650, 750)), ("frêne", (650, 750)),
    ("hêtre", (650, 750)), ("ébène", (1100, 1300)),
]
SOLS = [
    ("neige fraîche", (50, 200)), ("neige tassée", (200, 400)), ("neige mouillée", (400, 600)),
    ("tourbe humide", (600, 900)), ("glace", 917), ("terre sèche (en vrac)", (1200, 1500)),
    ("gravier (en vrac)", (1500, 1700)), ("sable sec", (1500, 1600)), ("terre humide tassée", (1600, 1900)),
    ("sable humide", (1700, 1900)), ("argile humide", (1800, 2000)), ("grave compactée (tout-venant)", (1900, 2000)),
]
AUTRES = [
    ("polystyrène expansé", (10, 35)), ("liège", (120, 250)), ("papier", (700, 1150)), ("polyéthylène", (910, 960)),
    ("caoutchouc", (920, 1200)), ("plexiglas (PMMA)", 1190), ("PVC rigide", (1350, 1450)), ("PET (bouteilles)", 1380),
    ("sucre en cristaux", 1590), ("brique pleine (terre cuite)", (1700, 2000)), ("sel en cristaux", 2165),
    ("béton ordinaire", (2300, 2400)), ("béton armé", 2500), ("verre", 2500), ("diamant", 3515),
]

# ---------------------------------------------------------------- contrôles de cohérence
def bornes(v):
    return (v, v) if not isinstance(v, tuple) else v


def coherent(rho, gamma, tol=0.03):
    """ρ × g dans la fourchette de l'Eurocode, à tol près."""
    a, b = bornes(rho)
    ga, gb = bornes(gamma)
    return a * G / 1000 >= ga * (1 - tol) and b * G / 1000 <= gb * (1 + tol)


PHYS = dict(LIQUIDES + [(n, v) for n, v, _ in METAUX] + BOIS + SOLS + AUTRES)
for nom_phys, nom_ec, liste in [("acier", "acier", EC_AUTRES), ("aluminium", "aluminium", EC_AUTRES), ("cuivre", "cuivre", EC_AUTRES),
                                ("fonte", "fonte", EC_AUTRES), ("plomb", "plomb", EC_AUTRES), ("zinc", "zinc", EC_AUTRES),
                                ("verre", "verre en plaques", EC_AUTRES), ("sable sec", "sable sec", EC_AUTRES),
                                ("béton armé", "béton armé ou précontraint", EC_BETON)]:
    assert coherent(PHYS[nom_phys], dict(liste)[nom_ec]), (nom_phys, PHYS[nom_phys], dict(liste)[nom_ec])
# l'eau douce « 10,0 kN/m³ » de l'Eurocode correspond à g ≈ 10 : 1 000 × 9,81 = 9,81 kN/m³
assert abs(1000 * G / 1000 - 10.0) / 10.0 < 0.02

# ---------------------------------------------------------------- écriture des nombres
def fr(x, n=0):
    s = f"{x:,.{n}f}".replace(",", " ").replace(".", ",")
    return s.replace(" ", NNBSP)


def sig(x, chiffres=3):
    """3 chiffres significatifs, sans zéro inutile : 0,998 ; 1,03 ; 13,5 ; 7,85."""
    if x == 0:
        return "0"
    from math import floor, log10
    n = max(0, chiffres - 1 - int(floor(log10(abs(x)))))
    s = f"{round(x, n):.{n}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", ",")


def plage(v, f):
    a, b = bornes(v)
    return f(a) if a == b else f"{f(a)} à {f(b)}"


def ent(x):
    return fr(x, 0)


def kn(x):
    return fr(x, 1)


def table_phys(lignes, titre="Matériau"):
    L = [f"| {titre} | Masse volumique (kg/m³) | Densité |", "|---|---|---|"]
    for nom, v, *_ in lignes:
        L.append(f"| {nom} | {plage(v, ent)} | {plage(tuple(x / 1000 for x in bornes(v)) if isinstance(v, tuple) else v / 1000, sig)} |")
    return "\n".join(L)


def table_ec(lignes):
    L = ["| Matériau | Poids volumique (kN/m³) |", "|---|---|"]
    for nom, v in lignes:
        L.append(f"| {nom} | {plage(v, kn)} |")
    return "\n".join(L)


GAZ_CALC = []
for nom, formule in GAZ:
    M = M_AIR if formule is None else masse_molaire(formule)
    GAZ_CALC.append((nom, formule, M, rho_gaz(M, 293.15)))
GAZ_CALC.sort(key=lambda g: g[3])


def table_gaz():
    L = ["| Gaz | Masse volumique (kg/m³) | Densité par rapport à l’air |", "|---|---|---|"]
    for nom, formule, M, rho in GAZ_CALC:
        lib = nom if formule is None else f"{nom} ({formule.replace('2', '₂').replace('4', '₄')})"
        L.append(f"| {lib} | {fr(rho, 3) if rho < 1 else fr(rho, 2)} | {sig(M / M_AIR, 2) if M / M_AIR < 1 else sig(M / M_AIR, 3)} |")
    return "\n".join(L)


assert dict((g[0], round(g[3], 3)) for g in GAZ_CALC)["air"] == 1.204
assert round(dict((g[0], g[3]) for g in GAZ_CALC)["dioxyde de carbone"], 2) == 1.83


# ---------------------------------------------------------------- données de l'outil (materiaux.json)
def slug(s):
    s = unicodedata.normalize("NFD", s.replace("’", "-").replace("'", "-")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


CATEGORIES = [
    ("liquides", "Eau et liquides", "rho", LIQUIDES),
    ("metaux", "Métaux et alliages", "rho", [(n, v) for n, v, _ in METAUX]),
    ("bois", "Bois", "rho", BOIS),
    ("sols", "Terre, sable, gravier et neige", "rho", SOLS),
    ("autres", "Autres matériaux", "rho", AUTRES),
    ("gaz", "Gaz (20 °C, 1 013 hPa)", "rho", [(g[0], round(g[3], 4)) for g in GAZ_CALC]),
    ("eurocode", "Construction (Eurocode, kN/m³)", "gamma", EC_BETON + EC_AUTRES + EC_BOIS),
]
materiaux = []
vus = set()
for cid, cnom, sorte, lignes in CATEGORIES:
    for nom, v in lignes:
        a, b = bornes(v)
        mid = slug(f"{cid}-{nom}")
        assert mid not in vus, mid
        vus.add(mid)
        materiaux.append({"id": mid, "nom": nom, "cat": cid, sorte: [a, b]})
DONNEES = {"g": G, "categories": [{"id": c[0], "nom": c[1]} for c in CATEGORIES], "materiaux": materiaux,
           "defaut": slug("autres-béton armé")}
assert DONNEES["defaut"] in vus

# ---------------------------------------------------------------- exemples de la page
V = {
    "TABLE_LIQUIDES": table_phys(LIQUIDES, "Liquide"),
    "TABLE_GAZ": table_gaz(),
    "TABLE_METAUX": table_phys(METAUX, "Métal ou alliage"),
    "TABLE_EC_BETON": table_ec(EC_BETON),
    "TABLE_EC_AUTRES": table_ec(EC_AUTRES),
    "TABLE_BOIS": table_phys(BOIS, "Essence"),
    "TABLE_EC_BOIS": table_ec(EC_BOIS),
    "TABLE_SOLS": table_phys(SOLS),
    "TABLE_AUTRES": table_phys(AUTRES),
    "AIR_0": fr(rho_gaz(M_AIR, 273.15), 3),
    "AIR_20": fr(rho_gaz(M_AIR, 293.15), 3),
    "POIDS_BA": fr(2500 * G / 1000, 1),
    "DALLE": fr(0.20 * 25.0, 1),
    "POUTRE_ACIER": fr(7850 * 0.01 * 6 , 0),
    "POUTRE_KN": fr(7850 * 0.01 * 6 * G / 1000, 2),
}
assert (V["AIR_20"], V["POIDS_BA"], V["DALLE"], V["POUTRE_ACIER"], V["POUTRE_KN"]) == ("1,204", "24,5", "5,0", "471", "4,62")


def remplacer(texte):
    for k_, v_ in V.items():
        texte = texte.replace("{" + k_ + "}", v_)
    reste = re.findall(r"\{[A-Z][A-Z0-9_]+\}", texte)
    assert not reste, reste
    return texte


INFOS = {
    "slug": "masse-volumique-des-materiaux",
    "titre": "Masse volumique des matériaux : le tableau complet",
    "titreCourt": "Masse volumique des matériaux",
    "titreSeo": "Masse volumique des matériaux : tableau (acier, béton, eau, bois)",
    "description": "Masse volumique et densité d’une centaine de matériaux : eau, gaz, métaux, bois, terre, sable, béton… avec les poids volumiques de l’Eurocode en kN/m³.",
    "chapo": "La masse volumique et la densité d’une centaine de matériaux, classés par famille : eau et liquides, gaz, métaux, bois, terre et sable, plastiques… avec les poids volumiques de l’Eurocode pour la construction et un outil pour calculer la masse et le poids d’un volume.",
    "resume": "Eau, métaux, béton, bois, terre, gaz : kg/m³ et kN/m³",
    "vignette": "flotte_coule",
    "theme": "Données",
    "niveaux": ["Collège", "Lycée", "Supérieur"],
    "ordre": 3,
    "publie": "2026-11-20",
    "modifie": "2026-11-20",
    "outil": "masses-volumiques",
    "motsCles": ["masse volumique", "tableau des masses volumiques", "masse volumique des matériaux", "densité",
                 "masse volumique de l'eau", "masse volumique de l'acier", "masse volumique du béton", "poids d'un m3 de béton",
                 "masse volumique de l'aluminium", "masse volumique du cuivre", "densité de l'huile", "masse volumique de l'air",
                 "masse volumique du bois", "densité du chêne", "masse volumique du sable", "poids de la terre au m3",
                 "poids volumique", "poids volumique Eurocode", "kN/m3", "métal le plus dense"],
    "figures": [
        {"nom": "flotte_coule", "alt": "Masses volumiques comparées à celle de l’eau (1 000 kg/m³), en échelle logarithmique : le liège (200), le bois de pin (520), la glace (917) et l’huile (920) flottent sur l’eau ; le béton (2 400), l’aluminium (2 700), l’acier (7 850), le plomb (11 340) et l’or (19 300) coulent."},
    ],
    "liees": ["physique-chimie/quantite-de-matiere-concentration", "methodes/convertisseur-d-unites",
              "physique-chimie/unites-si-constantes-physiques", "physique-chimie/formules-physique-chimie-brevet"],
    "faq": [
        ["Quelle est la masse volumique de l’eau ?", "Environ 1 000 kg/m³, soit 1 kg par litre ou 1 g/cm³. Elle vaut exactement 999,97 kg/m³ à 4 °C, où elle est la plus grande, et environ 998 kg/m³ à 20 °C. Un mètre cube d’eau pèse donc une tonne."],
        ["Quelle est la masse volumique de l’acier ?", "7 850 kg/m³, la valeur retenue par l’Eurocode 3 pour l’acier de construction. Un mètre cube d’acier a donc une masse de 7,85 tonnes, et un poids d’environ 77 kN. L’acier inoxydable est un peu plus dense : 7 900 à 8 000 kg/m³."],
        ["Combien pèse un m³ de béton ?", "Environ 2 400 kg pour un béton ordinaire et 2 500 kg pour un béton armé. Pour le calcul des structures, l’Eurocode 1 retient un poids volumique de 24 kN/m³ pour le béton non armé et 25 kN/m³ pour le béton armé : une dalle de 20 cm pèse ainsi 5 kN/m²."],
        ["Quelle est la différence entre masse volumique et densité ?", "La masse volumique est la masse d’un mètre cube de matière, en kg/m³. La densité compare cette masse volumique à celle de l’eau : elle n’a pas d’unité. L’huile, de masse volumique 920 kg/m³, a une densité de 0,92 : elle flotte sur l’eau. Pour un gaz, la densité se calcule par rapport à l’air."],
        ["Qu’est-ce que le poids volumique ?", "C’est le poids d’un mètre cube de matière, en newtons par mètre cube (N/m³) ou en kN/m³ : γ = ρ × g. Pour l’acier, 7 850 × 9,81 ≈ 77 000 N/m³, soit 77 kN/m³. Les ingénieurs et l’Eurocode l’utilisent pour calculer le poids propre des structures."],
        ["Quel est le métal le plus dense ?", "L’osmium, avec environ 22 590 kg/m³, juste devant l’iridium et le platine (21 450 kg/m³). L’or (19 300 kg/m³) est presque deux fois plus dense que le plomb (11 340 kg/m³). Le plus léger des métaux courants est le magnésium, avec 1 740 kg/m³."],
    ],
}

TEXTE = r"""<!-- optitab:1 -->
[OUTIL]

::: conseil Comment lire ces tableaux
- La **masse volumique** est en kg/m³. Le même nombre divisé par 1 000 donne la **densité**, qui est aussi la masse volumique en g/cm³ ou en kg/L.
- Les fourchettes (« 720 à 775 ») indiquent des matériaux dont la composition varie.
- Pour la construction, les parties V à VII donnent les **poids volumiques de l’Eurocode**, en kN/m³.
:::

## I. Masse volumique, densité et poids volumique {Collège}

::: formule Masse volumique
$$\rho = \dfrac{m}{V}$$
:::

| Lettre | Grandeur | Unité |
|---|---|---|
| $\rho$ (rhô) | masse volumique | kg/m³ |
| $m$ | masse | kg |
| $V$ | volume | m³ |

::: formule Densité d’un solide ou d’un liquide
$$d = \dfrac{\rho}{\rho_{\text{eau}}}$$
:::

La densité n’a pas d’unité. Un corps de densité inférieure à 1 flotte sur l’eau, un corps de densité supérieure à 1 coule.

[IMAGE_1]

::: formule Poids volumique
$$\gamma = \rho \times g$$
:::

$\gamma$ (gamma) est le poids d’un mètre cube, en N/m³ ou en kN/m³, avec $g = 9{,}81$ N/kg. C’est la grandeur qu’utilisent les ingénieurs et les Eurocodes.

::: exemple
Un mètre cube de béton armé a une masse d’environ 2 500 kg et un poids $\gamma = 2\,500 \times 9{,}81 \approx {POIDS_BA}$ kN. Une poutre en acier de 6 m de long et de section 100 cm², soit un volume de 0,06 m³, a une masse de $7\,850 \times 0{,}06 = {POUTRE_ACIER}$ kg et un poids d’environ {POUTRE_KN} kN.
:::

::: attention Masse volumique ou poids volumique ?
La masse volumique s’exprime en kg/m³ et ne dépend pas du lieu ; le poids volumique s’exprime en kN/m³ et dépend de $g$. Diviser un poids volumique en kN/m³ par 9,81 puis multiplier par 1 000 redonne la masse volumique en kg/m³.
:::

## II. L’eau et les liquides {Collège}

{TABLE_LIQUIDES}

L’eau est la plus dense à 4 °C. La glace, moins dense que l’eau liquide, flotte : c’est pourquoi un lac gèle d’abord en surface.

## III. Les gaz {Lycée}

À 20 °C et sous 1 013 hPa. La densité d’un gaz se calcule par rapport à l’air : $d = \dfrac{M}{29}$, avec $M$ la masse molaire en g/mol.

{TABLE_GAZ}

::: remarque Ce qui change avec la température
Un gaz se dilate quand il chauffe : l’air a une masse volumique de {AIR_0} kg/m³ à 0 °C et de {AIR_20} kg/m³ à 20 °C. Les valeurs du tableau sont calculées avec la loi des gaz parfaits.
:::

## IV. Les métaux et les alliages {Collège}

Du moins dense au plus dense :

{TABLE_METAUX}

## V. Béton, mortier et pierres : les poids volumiques de l’Eurocode {Supérieur}

Valeurs de l’annexe A de l’Eurocode 1 (NF EN 1991-1-1), pour des matériaux secs. Elles servent à calculer le **poids propre** des ouvrages.

{TABLE_EC_BETON}

::: exemple Le poids d’une dalle
Une dalle en béton armé de 20 cm d’épaisseur pèse $0{,}20 \times 25 = {DALLE}$ kN par mètre carré de plancher.
:::

::: attention Béton frais
Pour le béton frais, encore non durci, l’Eurocode ajoute 1 kN/m³. La masse volumique réelle d’un béton armé est d’environ 2 500 kg/m³ : les poids volumiques de l’Eurocode sont des valeurs de calcul arrondies.
:::

## VI. Métaux, verre, enrobés et matériaux en vrac : l’Eurocode {Supérieur}

{TABLE_EC_AUTRES}

## VII. Les bois {Collège}

Bois sec à l’air, à environ 12 % d’humidité. Un bois humide ou fraîchement coupé est nettement plus lourd, parfois presque deux fois plus.

{TABLE_BOIS}

Pour la construction, l’Eurocode donne le poids volumique selon la **classe de résistance** du bois (NF EN 338) :

{TABLE_EC_BOIS}

## VIII. Terre, sable, gravier et neige {Collège}

Valeurs indicatives : la masse volumique d’un sol dépend de son tassement et de sa teneur en eau. Pour un projet de construction, elle se mesure sur place.

{TABLE_SOLS}

## IX. Les autres matériaux courants {Collège}

{TABLE_AUTRES}
"""

UNITES = ["kg/m³", "kN/m³", "kN/m²", "g/cm³", "kg/L", "N/kg", "N/m³", "hPa", "cm²", "kg", "kN", "cm", "m³", "°C", "m", "%"]
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
    n = len(materiaux)
    assert 100 <= n <= 140, n
    (ICI / "materiaux.json").write_text(json.dumps(DONNEES, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    entete = json.dumps(infos, ensure_ascii=False, indent=2)
    (ICI / "formulaire.md").write_text(insecables(f"---\n{entete}\n---\n{texte}"), encoding="utf-8", newline="\n")
    print(f"{n} matériaux ; materiaux.json et formulaire.md écrits :", len(infos["titreSeo"]), "car. (titre),",
          len(infos["description"]), "car. (description)")


if __name__ == "__main__":
    ecrire()
