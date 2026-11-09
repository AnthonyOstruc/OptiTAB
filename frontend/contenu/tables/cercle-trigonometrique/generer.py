# -*- coding: utf-8 -*-
"""Génère formulaire.md « Cercle trigonométrique » (valeurs exactes contrôlées numériquement).

    python frontend/contenu/tables/cercle-trigonometrique/generer.py
"""
import json
from fractions import Fraction
from math import cos, isclose, pi, radians, sin, sqrt
from pathlib import Path

ICI = Path(__file__).resolve().parent
DEGRES = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]

# valeur absolue → écriture exacte (cos et sin)
EXACT = [(0.0, "0"), (0.5, r"\dfrac{1}{2}"), (sqrt(2) / 2, r"\dfrac{\sqrt{2}}{2}"), (sqrt(3) / 2, r"\dfrac{\sqrt{3}}{2}"), (1.0, "1")]
EXACT_TAN = [(0.0, "0"), (sqrt(3) / 3, r"\dfrac{\sqrt{3}}{3}"), (1.0, "1"), (sqrt(3), r"\sqrt{3}")]


def exact(v, table):
    for val, tex in table:
        if isclose(abs(v), val, abs_tol=1e-9):
            return tex if v >= 0 or tex == "0" else "-" + tex
    raise ValueError(v)


def radian(d):
    f = Fraction(d, 180)
    if f == 0:
        return "0"
    num = "" if f.numerator == 1 else str(f.numerator)
    if f.denominator == 1:
        return num + r"\pi"
    return rf"\dfrac{{{num}\pi}}{{{f.denominator}}}"


def ligne(d):
    a = radians(d)
    c, s = cos(a), sin(a)
    t = "non définie" if isclose(c, 0, abs_tol=1e-9) else f"${exact(s / c, EXACT_TAN)}$"
    return f"| ${radian(d)}$ (${d}^\\circ$) | ${exact(c, EXACT)}$ | ${exact(s, EXACT)}$ | {t} |"


assert radian(150) == r"\dfrac{5\pi}{6}" and radian(180) == r"\pi" and radian(30) == r"\dfrac{\pi}{6}"
assert exact(cos(radians(150)), EXACT) == r"-\dfrac{\sqrt{3}}{2}" and exact(sin(radians(210)), EXACT) == r"-\dfrac{1}{2}"
assert exact(sin(radians(225)) / cos(radians(225)), EXACT_TAN) == "1"

INFO = {
    "slug": "cercle-trigonometrique",
    "titre": "Cercle trigonométrique",
    "titreCourt": "Cercle trigonométrique",
    "titreSeo": "Cercle trigonométrique : valeurs remarquables en radians et degrés",
    "description": "Le cercle trigonométrique complet avec ses 16 angles remarquables en radians et en degrés, le tableau des cos, sin et tan de 0 à 2π et les signes par quart.",
    "chapo": "Le cercle trigonométrique complet, en radians et en degrés, le tableau des cosinus, sinus et tangentes des seize angles remarquables, les signes selon le quart de cercle et la mesure principale.",
    "resume": "16 angles, cos, sin, tan, radians et degrés",
    "vignette": "cercle_complet",
    "theme": "Trigonométrie",
    "niveaux": ["Lycée"],
    "ordre": 11,
    "publie": "2026-11-09",
    "modifie": "2026-11-09",
    "motsCles": ["cercle trigonométrique", "cercle trigonométrique valeurs remarquables", "cercle trigonométrique complet", "valeurs remarquables cos sin", "cos pi/3", "sin pi/6", "radians en degrés", "mesure principale"],
    "figures": [
        {"nom": "cercle_complet", "alt": "Cercle trigonométrique complet : les seize angles remarquables de 0 à 11π/6 sont placés sur le cercle, avec leur mesure en radians à l’extérieur et en degrés à l’intérieur."},
        {"nom": "signes_quarts", "alt": "Signes du cosinus et du sinus dans chaque quart du cercle trigonométrique : en haut à droite, cos et sin positifs ; en haut à gauche, cos négatif et sin positif ; en bas à gauche, les deux négatifs ; en bas à droite, cos positif et sin négatif."},
    ],
    "chapitresLies": ["premiere/fonctions-trigonometriques", "terminale/fonctions-sinus-et-cosinus"],
    "faq": [
        ["Comment lire le cercle trigonométrique ?", "À chaque angle x correspond un point M du cercle de rayon 1 : cos x est l’abscisse de M (lecture sur l’axe horizontal) et sin x est son ordonnée (lecture sur l’axe vertical)."],
        ["Combien vaut cos(π/3) ?", "cos(π/3) = 1/2 et sin(π/3) = √3/2. L’angle π/3 correspond à 60°."],
        ["Comment convertir des degrés en radians ?", "On multiplie par π/180. Par exemple, 45° = 45 × π/180 = π/4 rad. Dans l’autre sens, on multiplie par 180/π."],
        ["Qu’est-ce que la mesure principale d’un angle ?", "C’est l’unique mesure de l’angle comprise dans ]−π ; π]. On l’obtient en ajoutant ou en retirant des multiples de 2π. Par exemple, la mesure principale de 17π/6 est 5π/6."],
    ],
}

L = ["<!-- optitab:1 -->"]
L.append("## I. Le cercle complet {Lycée}\n")
L.append("[IMAGE_1]\n")
L.append("::: definition Cercle trigonométrique")
L.append("C’est le cercle de centre $O$ et de rayon $1$, orienté dans le sens inverse des aiguilles d’une montre. Pour le point $M$ associé à l’angle $x$, **$\\cos x$ est l’abscisse** et **$\\sin x$ est l’ordonnée**.")
L.append(":::\n")

L.append("## II. Tableau des valeurs remarquables {Lycée}\n")
L.append("| Angle | $\\cos$ | $\\sin$ | $\\tan$ |")
L.append("|---|---|---|---|")
for d in DEGRES:
    L.append(ligne(d))
L.append("")
L.append("::: conseil Astuce de mémorisation")
L.append("De $0$ à $\\dfrac{\\pi}{2}$, le sinus vaut successivement $\\dfrac{\\sqrt{0}}{2}$, $\\dfrac{\\sqrt{1}}{2}$, $\\dfrac{\\sqrt{2}}{2}$, $\\dfrac{\\sqrt{3}}{2}$ et $\\dfrac{\\sqrt{4}}{2}$ ; le cosinus prend les mêmes valeurs dans l’ordre inverse.")
L.append(":::\n")

L.append("## III. Signes selon le quart de cercle {Lycée}\n")
L.append("[IMAGE_2]\n")
L.append("| Quart de cercle | Signes |")
L.append("|---|---|")
L.append("| Premier : $0 < x < \\dfrac{\\pi}{2}$ | $\\cos x > 0$ et $\\sin x > 0$ |")
L.append("| Deuxième : $\\dfrac{\\pi}{2} < x < \\pi$ | $\\cos x < 0$ et $\\sin x > 0$ |")
L.append("| Troisième : $\\pi < x < \\dfrac{3\\pi}{2}$ | $\\cos x < 0$ et $\\sin x < 0$ |")
L.append("| Quatrième : $\\dfrac{3\\pi}{2} < x < 2\\pi$ | $\\cos x > 0$ et $\\sin x < 0$ |")
L.append("")

L.append("## IV. Degrés et radians {Lycée}\n")
L.append("::: formule Conversion")
L.append("$$x_{\\text{rad}} = x_{\\text{deg}} \\times \\frac{\\pi}{180} \\qquad x_{\\text{deg}} = x_{\\text{rad}} \\times \\frac{180}{\\pi}$$")
L.append(":::\n")
L.append("| Degrés | Radians |")
L.append("|---|---|")
for d in (1, 15, 30, 45, 60, 90, 180, 270, 360):
    L.append(f"| ${d}^\\circ$ | ${radian(d)}$ |")
L.append("")
L.append("Un radian vaut environ $57{,}3^\\circ$.\n")
assert isclose(180 / pi, 57.2958, abs_tol=1e-4)

L.append("## V. Mesure principale {Lycée}\n")
L.append("::: definition Mesure principale")
L.append("Un angle a une infinité de mesures, qui diffèrent d’un multiple de $2\\pi$. Sa **mesure principale** est celle qui appartient à $]{-\\pi}\\,;\\pi]$.")
L.append(":::\n")
L.append("::: exemple Mesure principale de $\\dfrac{17\\pi}{6}$")
L.append("$\\dfrac{17\\pi}{6} - 2\\pi = \\dfrac{5\\pi}{6}$, qui appartient à $]{-\\pi}\\,;\\pi]$ : la mesure principale est $\\dfrac{5\\pi}{6}$.")
L.append(":::\n")
L.append("::: retenir Périodicité")
L.append("$$\\cos(x + 2k\\pi) = \\cos x \\qquad \\sin(x + 2k\\pi) = \\sin x$$")
L.append("pour tout entier relatif $k$.")
L.append(":::\n")

# contrôles numériques
for d in DEGRES:
    a = radians(d)
    assert isclose(cos(a) ** 2 + sin(a) ** 2, 1)
assert isclose(17 * pi / 6 - 2 * pi, 5 * pi / 6)
assert radian(270) == r"\dfrac{3\pi}{2}" and radian(1) == r"\dfrac{\pi}{180}"

texte = "---\n" + json.dumps(INFO, ensure_ascii=False, indent=2) + "\n---\n" + "\n".join(L).rstrip() + "\n"
(ICI / "formulaire.md").write_bytes(texte.encode("utf-8"))
print("formulaire.md écrit :", len(DEGRES), "angles")
