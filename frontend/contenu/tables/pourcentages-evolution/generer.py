# -*- coding: utf-8 -*-
"""Génère formulaire.md « Pourcentages d'évolution » (calculs exacts avec Fraction).

    python frontend/contenu/tables/pourcentages-evolution/generer.py
"""
import json
from fractions import Fraction as F
from pathlib import Path

ICI = Path(__file__).resolve().parent


def nombre(x, dec=2):
    """Écriture française, sans zéros inutiles ; « ≈ » si la valeur est arrondie."""
    s = f"{float(x):.{dec}f}".rstrip("0").rstrip(".")
    exact = F(s) == x
    return ("" if exact else "≈ ") + s.replace(".", ",").replace("-", "−")


def taux(cm):
    """Taux d'évolution en % (signé) correspondant à un coefficient multiplicateur."""
    t = (cm - 1) * 100
    signe = "+" if t > 0 else ""
    v = nombre(t)
    return (v[:2] + signe + v[2:] if v.startswith("≈") else signe + v) + " %"


assert taux(F(121, 100)) == "+21 %" and taux(F(96, 100)) == "−4 %" and taux(1 / F(12, 10)) == "≈ −16,67 %"

INFO = {
    "slug": "pourcentages-evolution",
    "titre": "Pourcentages d’évolution et coefficients multiplicateurs",
    "titreCourt": "Pourcentages d’évolution",
    "titreSeo": "Pourcentage d’augmentation et de baisse : coefficient multiplicateur",
    "description": "Calculer une hausse ou une baisse en pourcentage : coefficients multiplicateurs, évolutions successives, évolution réciproque, taux d’évolution, TVA.",
    "chapo": "Le coefficient multiplicateur de chaque hausse et de chaque baisse, les évolutions successives et réciproques, le calcul d’un taux d’évolution et les applications (TVA, soldes).",
    "resume": "Hausse, baisse, évolutions successives, TVA",
    "vignette": "hausse_retour",
    "theme": "Proportionnalité",
    "niveaux": ["Collège", "Lycée"],
    "ordre": 9,
    "publie": "2026-11-09",
    "modifie": "2026-11-09",
    "motsCles": ["coefficient multiplicateur", "pourcentage d'augmentation", "pourcentage de baisse", "calculer une augmentation en pourcentage", "évolutions successives", "évolution réciproque", "taux d'évolution", "calcul TVA"],
    "figures": [
        {"nom": "hausse_retour", "alt": "Un prix de 100 € augmente de 20 % (multiplié par 1,2) pour atteindre 120 € ; pour revenir à 100 €, on divise par 1,2, soit une baisse d’environ 16,7 %."},
    ],
    "chapitresLies": ["4e/proportionnalite-et-pourcentages", "3e/proportionnalite-et-pourcentages", "seconde/utiliser-l-information-chiffree-et-statistique-descriptive"],
    "faq": [
        ["Comment calculer une augmentation de 15 % ?", "On multiplie par le coefficient multiplicateur 1 + 15/100 = 1,15. Par exemple, 80 € augmentés de 15 % donnent 80 × 1,15 = 92 €."],
        ["Comment calculer une baisse de 30 % ?", "On multiplie par 1 − 30/100 = 0,7. Un article à 50 € soldé à −30 % coûte 50 × 0,7 = 35 €."],
        ["Une hausse de 20 % puis une baisse de 20 % ramènent-elles au prix de départ ?", "Non : 1,2 × 0,8 = 0,96, soit une baisse de 4 % au total. Pour annuler une hausse de 20 %, il faut une baisse d’environ 16,7 % (diviser par 1,2)."],
        ["Comment calculer un taux d’évolution ?", "On calcule (valeur finale − valeur initiale) ÷ valeur initiale × 100. De 80 à 92, le taux vaut (92 − 80) ÷ 80 × 100 = +15 %."],
    ],
}

L = ["<!-- optitab:1 -->"]
L.append("## I. Coefficient multiplicateur {Collège}\n")
L.append("[IMAGE_1]\n")
L.append("| Évolution | Coefficient multiplicateur |")
L.append("|---|---|")
L.append("| Hausse de $t\\,\\%$ | $1 + \\dfrac{t}{100}$ |")
L.append("| Baisse de $t\\,\\%$ | $1 - \\dfrac{t}{100}$ |")
L.append("")
L.append("::: retenir")
L.append("Augmenter ou diminuer une valeur d’un pourcentage, c’est la **multiplier** par son coefficient multiplicateur : valeur finale $=$ valeur initiale $\\times$ coefficient.")
L.append(":::\n")

L.append("## II. Tableau des hausses et des baisses {Collège}\n")
L.append("| Hausse | Coefficient | Baisse | Coefficient |")
L.append("|---|---|---|---|")
hausses = [1, 2, 5, 10, 15, 20, 25, 30, 50, 100]
baisses = [1, 2, 5, 10, 15, 20, 25, 30, 50, 75]
for h, b in zip(hausses, baisses):
    L.append(f"| +{h} % | {nombre(1 + F(h, 100))} | −{b} % | {nombre(1 - F(b, 100))} |")
L.append("")
L.append("::: exemple")
L.append("Un vélo à $250$ € augmente de $8\\,\\%$ : $250 \\times 1{,}08 = 270$ €. Il est ensuite soldé à $-25\\,\\%$ : $270 \\times 0{,}75 = 202{,}50$ €.")
L.append(":::\n")
assert 250 * F(108, 100) == 270 and 270 * F(75, 100) == F(40500, 200)

L.append("## III. Évolutions successives {Collège}\n")
L.append("Pour enchaîner des évolutions, on **multiplie** les coefficients, on n’additionne pas les pourcentages.\n")
L.append("| Évolutions | Calcul | Évolution globale |")
L.append("|---|---|---|")
for e1, e2 in [(10, 10), (20, -20), (-20, 20), (50, -50), (10, -10), (5, 5), (-10, -10)]:
    c = (1 + F(e1, 100)) * (1 + F(e2, 100))
    s1 = f"+{e1} %" if e1 > 0 else f"−{-e1} %"
    s2 = f"+{e2} %" if e2 > 0 else f"−{-e2} %"
    c1, c2 = nombre(1 + F(e1, 100)), nombre(1 + F(e2, 100))
    L.append(f"| {s1} puis {s2} | {c1} × {c2} = {nombre(c, 4)} | {taux(c)} |")
L.append("")
L.append("::: attention Erreur fréquente")
L.append("$+20\\,\\%$ puis $-20\\,\\%$ ne fait pas $0\\,\\%$ : $1{,}2 \\times 0{,}8 = 0{,}96$, soit une **baisse de $4\\,\\%$**.")
L.append(":::\n")

L.append("## IV. Évolution réciproque {Collège}\n")
L.append("Pour revenir à la valeur de départ, on **divise** par le coefficient. Par exemple, après une hausse de 20 %, on divise par $1{,}2$, ce qui correspond à une baisse d’environ $16{,}67\\,\\%$.\n")
L.append("| Évolution | Évolution réciproque |")
L.append("|---|---|")
for e in (10, 20, 25, 50, 100, -10, -20, -25, -50):
    c = 1 + F(e, 100)
    s = f"+{e} %" if e > 0 else f"−{-e} %"
    L.append(f"| {s} | {taux(1 / c)} |")
L.append("")

L.append("## V. Taux d’évolution {Collège}\n")
L.append("::: formule Taux d’évolution entre une valeur initiale $V_i$ et une valeur finale $V_f$")
L.append("$$t = \\frac{V_f - V_i}{V_i} \\times 100$$")
L.append(":::\n")
L.append("::: exemple")
L.append("Un loyer passe de $800$ € à $840$ € : $t = \\dfrac{840 - 800}{800} \\times 100 = +5\\,\\%$.")
L.append(":::\n")

L.append("## VI. TVA, remises et soldes {Collège}\n")
L.append("| Situation | Calcul |")
L.append("|---|---|")
for s, c in [
    ("Prix TTC avec une TVA à 20 %", "prix HT × 1,2"),
    ("Prix HT à partir du prix TTC (TVA à 20 %)", "prix TTC ÷ 1,2"),
    ("TVA à 10 % (restauration…)", "prix HT × 1,1"),
    ("TVA à 5,5 % (alimentation, livres…)", "prix HT × 1,055"),
    ("Remise de 30 %", "prix × 0,7"),
    ("Deux remises de 10 %", "prix × 0,9 × 0,9 = prix × 0,81 (soit −19 %)"),
]:
    L.append(f"| {s} | {c} |")
L.append("")
assert F(9, 10) * F(9, 10) == F(81, 100)

L.append("## VII. Taux d’évolution moyen {Lycée}\n")
L.append("Si une valeur subit $n$ évolutions de coefficient global $C$, le taux moyen par période est $t_m$ tel que :")
L.append("$$(1 + t_m)^n = C \\quad \\text{donc} \\quad 1 + t_m = C^{1/n}$$")
L.append("")
L.append("::: exemple")
L.append("Une hausse de $21\\,\\%$ en deux ans correspond à $1{,}21^{1/2} = 1{,}1$, soit $+10\\,\\%$ par an en moyenne (et non $+10{,}5\\,\\%$).")
L.append(":::\n")

import re
corps = "\n".join(L).rstrip()
# « 10 % » : espace fine insécable entre le nombre et le signe % (jamais de « % » seul en début de ligne).
corps = re.sub(r"(\d) %", "\\1\u202f%", corps)
texte = "---\n" + json.dumps(INFO, ensure_ascii=False, indent=2) + "\n---\n" + corps + "\n"
(ICI / "formulaire.md").write_bytes(texte.encode("utf-8"))
print("formulaire.md écrit")
