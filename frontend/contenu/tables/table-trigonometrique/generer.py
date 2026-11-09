# -*- coding: utf-8 -*-
"""Génère formulaire.md de la table trigonométrique (valeurs calculées, 4 décimales).

    python frontend/contenu/tables/table-trigonometrique/generer.py
"""
import json
from math import cos, radians, sin, tan
from pathlib import Path

ICI = Path(__file__).resolve().parent


def f4(x):
    return f"{x:.4f}".replace(".", ",")


assert f4(sin(radians(30))) == "0,5000" and f4(cos(radians(60))) == "0,5000" and f4(tan(radians(45))) == "1,0000"

INFO = {
    "slug": "table-trigonometrique",
    "titre": "Table trigonométrique de 0° à 90°",
    "titreCourt": "Table trigonométrique",
    "titreSeo": "Table trigonométrique : sinus, cosinus, tangente de 0° à 90°",
    "description": "Les valeurs du sinus, du cosinus et de la tangente des angles de 0° à 90°, degré par degré, avec les valeurs exactes et la méthode pour trouver un angle.",
    "chapo": "Le sinus, le cosinus et la tangente de chaque angle de 0° à 90°, degré par degré, les valeurs exactes de 30°, 45° et 60°, et la méthode pour retrouver un angle.",
    "resume": "sin, cos, tan de 0° à 90°, degré par degré",
    "vignette": "cercle_cos_sin_tan",
    "theme": "Géométrie",
    "niveaux": ["Collège", "Lycée"],
    "ordre": 7,
    "publie": "2026-11-09",
    "modifie": "2026-11-09",
    "motsCles": ["table trigonométrique", "tableau sinus cosinus tangente", "valeurs sinus", "valeurs cosinus", "table de cosinus", "sin 30", "cos 60", "tan 45"],
    "figures": [
        {"nom": "cercle_cos_sin_tan", "alt": "Quart de cercle de rayon 1 et angle α : cos α se lit sur l’axe horizontal, sin α sur l’axe vertical et tan α sur la tangente verticale au cercle."},
    ],
    "chapitresLies": ["4e/cosinus-dans-le-triangle-rectangle", "3e/trigonometrie-du-triangle-rectangle", "premiere/fonctions-trigonometriques"],
    "faq": [
        ["Combien vaut sin 30° ?", "sin 30° = 0,5 exactement (soit 1/2). De même, cos 60° = 0,5 et tan 45° = 1."],
        ["Comment trouver un angle avec la table ?", "On cherche dans la colonne du rapport connu la valeur la plus proche. Par exemple, si cos α = 0,8, la table donne cos 37° ≈ 0,7986 et cos 36° ≈ 0,8090 : l’angle vaut environ 37° (36,9° à la calculatrice, touche cos⁻¹ ou Arccos)."],
        ["Pourquoi la tangente de 90° n’existe-t-elle pas ?", "tan α = sin α / cos α, et cos 90° = 0 : on ne peut pas diviser par 0. Plus l’angle se rapproche de 90°, plus la tangente devient grande."],
        ["Ma calculatrice ne donne pas les mêmes valeurs, pourquoi ?", "Elle est sans doute réglée en radians. Pour un angle en degrés, passez-la en mode « Degré » (DEG) : sin 30 doit afficher 0,5."],
    ],
}

L = ["<!-- optitab:1 -->"]
L.append("## I. Lire la table {Collège}\n")
L.append("[IMAGE_1]\n")
L.append("Dans un triangle rectangle, pour un angle aigu $\\alpha$ :\n")
L.append("| Rapport | Définition |")
L.append("|---|---|")
L.append("| Cosinus | côté adjacent ÷ hypoténuse |")
L.append("| Sinus | côté opposé ÷ hypoténuse |")
L.append("| Tangente | côté opposé ÷ côté adjacent |")
L.append("")

L.append("## II. Table de 0° à 45° {Collège}\n")
L.append("| Angle | sin | cos | tan |")
L.append("|---|---|---|---|")
for a in range(0, 46):
    r = radians(a)
    L.append(f"| {a}° | {f4(sin(r))} | {f4(cos(r))} | {f4(tan(r))} |")
L.append("")

L.append("## III. Table de 46° à 90° {Collège}\n")
L.append("| Angle | sin | cos | tan |")
L.append("|---|---|---|---|")
for a in range(46, 91):
    r = radians(a)
    t = "non définie" if a == 90 else f4(tan(r))
    L.append(f"| {a}° | {f4(sin(r))} | {f4(cos(r))} | {t} |")
L.append("")

L.append("## IV. Valeurs exactes à connaître {Collège}\n")
L.append("| Angle | $\\sin$ | $\\cos$ | $\\tan$ |")
L.append("|---|---|---|---|")
L.append("| $30^\\circ$ | $\\dfrac{1}{2}$ | $\\dfrac{\\sqrt{3}}{2}$ | $\\dfrac{\\sqrt{3}}{3}$ |")
L.append("| $45^\\circ$ | $\\dfrac{\\sqrt{2}}{2}$ | $\\dfrac{\\sqrt{2}}{2}$ | $1$ |")
L.append("| $60^\\circ$ | $\\dfrac{\\sqrt{3}}{2}$ | $\\dfrac{1}{2}$ | $\\sqrt{3}$ |")
L.append("")
L.append("::: retenir Angles complémentaires")
L.append("$\\sin(90^\\circ - \\alpha) = \\cos\\alpha$ et $\\cos(90^\\circ - \\alpha) = \\sin\\alpha$ : la colonne sin de $30^\\circ$ est la colonne cos de $60^\\circ$.")
L.append(":::\n")

L.append("## V. Trouver un angle {Collège}\n")
L.append("::: methode Retrouver un angle à partir d’un rapport")
L.append("Si $\\cos\\alpha = 0{,}8$ : la table donne $\\cos 36^\\circ \\approx " + f4(cos(radians(36))).replace(",", "{,}") + "$ et $\\cos 37^\\circ \\approx " + f4(cos(radians(37))).replace(",", "{,}") + "$, donc $\\alpha \\approx 37^\\circ$. À la calculatrice, en mode degré : $\\alpha = \\cos^{-1}(0{,}8) \\approx 36{,}9^\\circ$.")
L.append(":::\n")
L.append("::: attention Mode de la calculatrice")
L.append("Pour un angle en degrés, la calculatrice doit être en mode **Degré** (DEG). En mode radian, $\\sin 30$ ne donne pas $0{,}5$.")
L.append(":::\n")

texte = "---\n" + json.dumps(INFO, ensure_ascii=False, indent=2) + "\n---\n" + "\n".join(L).rstrip() + "\n"
(ICI / "formulaire.md").write_bytes(texte.encode("utf-8"))
print("formulaire.md écrit ; cos 36° =", f4(cos(radians(36))), "; cos 37° =", f4(cos(radians(37))))
