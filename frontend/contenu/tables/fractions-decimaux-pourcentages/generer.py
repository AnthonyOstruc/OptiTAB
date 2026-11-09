# -*- coding: utf-8 -*-
"""Génère formulaire.md « Fractions, décimaux et pourcentages » (calculs exacts).

    python frontend/contenu/tables/fractions-decimaux-pourcentages/generer.py
"""
import json
from fractions import Fraction
from pathlib import Path

ICI = Path(__file__).resolve().parent


def finie(f):
    """Vrai si l'écriture décimale de f s'arrête (dénominateur fait de 2 et de 5)."""
    d = f.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return d == 1


def tronque(f, n):
    """Les n premières décimales de f (troncature, jamais d'arrondi devant « … »)."""
    entier = f.numerator * 10 ** n // f.denominator
    s = str(entier).rjust(n + 1, "0")
    return s[:-n] + "{,}" + s[-n:]


def decimal(f):
    """Écriture décimale exacte, ou les premières décimales suivies de « … » si elle est illimitée."""
    if finie(f):
        s = f"{float(f):.6f}".rstrip("0").rstrip(".")
        return s.replace(".", "{,}")
    return tronque(f, 4) + "\\ldots"


def pourcent(f):
    p = f * 100
    if finie(p):
        s = f"{float(p):.6f}".rstrip("0").rstrip(".")
        return s.replace(".", "{,}") + "\\,\\%"
    return "\\approx " + f"{float(p):.1f}".replace(".", "{,}") + "\\,\\%"


FRACTIONS = ["1/2", "1/3", "2/3", "1/4", "3/4", "1/5", "2/5", "3/5", "4/5", "1/6", "5/6",
             "1/8", "3/8", "5/8", "7/8", "1/10", "3/10", "1/20", "1/25", "1/50", "1/100"]
assert decimal(Fraction(3, 8)) == "0{,}375" and pourcent(Fraction(1, 8)) == "12{,}5\\,\\%"
assert decimal(Fraction(1, 6)) == "0{,}1666\\ldots" and decimal(Fraction(2, 3)) == "0{,}6666\\ldots"
assert pourcent(Fraction(1, 3)) == "\\approx 33{,}3\\,\\%" and pourcent(Fraction(1, 2)) == "50\\,\\%"

INFO = {
    "slug": "fractions-decimaux-pourcentages",
    "titre": "Fractions, décimaux et pourcentages",
    "titreCourt": "Fractions et pourcentages",
    "titreSeo": "Tableau d’équivalence : fractions, nombres décimaux et pourcentages",
    "description": "Le tableau d’équivalence entre fractions, nombres décimaux et pourcentages (1/2, 1/4, 3/4, 1/3, 1/8…), les méthodes de conversion et le calcul d’un pourcentage.",
    "chapo": "Les fractions les plus courantes avec leur écriture décimale et leur pourcentage, les méthodes pour passer de l’une à l’autre et le calcul mental des pourcentages.",
    "resume": "1/2 = 0,5 = 50 %, conversions, calcul mental",
    "vignette": "disques_fractions",
    "theme": "Nombres",
    "niveaux": ["Primaire", "Collège"],
    "ordre": 8,
    "publie": "2026-11-09",
    "modifie": "2026-11-09",
    "motsCles": ["fraction en pourcentage", "fraction en décimal", "tableau fraction décimal pourcentage", "1/4 en pourcentage", "1/3 en décimal", "convertir un pourcentage en fraction", "calculer un pourcentage", "pourcentage d'un nombre"],
    "figures": [
        {"nom": "disques_fractions", "alt": "Quatre disques partagés : la moitié colorée (1/2 = 0,5 = 50 %), un quart (1/4 = 0,25 = 25 %), trois quarts (3/4 = 0,75 = 75 %) et un tiers (1/3 ≈ 33 %)."},
    ],
    "chapitresLies": ["cm1/fractions-decimales-et-ecriture-a-virgule", "cm2/prendre-une-fraction-d-une-quantite", "6e/proportions-et-pourcentages", "5e/proportionnalite-et-pourcentages", "4e/proportionnalite-et-pourcentages"],
    "faq": [
        ["Comment transformer une fraction en pourcentage ?", "On divise le numérateur par le dénominateur, puis on multiplie par 100. Par exemple, 3/8 = 3 ÷ 8 = 0,375, soit 37,5 %."],
        ["Comment transformer un pourcentage en fraction ?", "On écrit le pourcentage sur 100, puis on simplifie : 75 % = 75/100 = 3/4, et 40 % = 40/100 = 2/5."],
        ["Combien font 25 % d’un nombre ?", "25 % = 1/4 : on divise le nombre par 4. Par exemple, 25 % de 80 = 80 ÷ 4 = 20."],
        ["Pourquoi 1/3 n’a-t-il pas d’écriture décimale exacte ?", "Parce que 1 ÷ 3 = 0,3333… ne s’arrête jamais : le chiffre 3 se répète à l’infini. On écrit 1/3 ≈ 0,33, soit environ 33,3 %."],
    ],
}

L = ["<!-- optitab:1 -->"]
L.append("## I. Tableau d’équivalence {Primaire}\n")
L.append("[IMAGE_1]\n")
L.append("| Fraction | Nombre décimal | Pourcentage |")
L.append("|---|---|---|")
for s in FRACTIONS:
    n, d = map(int, s.split("/"))
    f = Fraction(n, d)
    L.append(f"| $\\dfrac{{{n}}}{{{d}}}$ | ${decimal(f)}$ | ${pourcent(f)}$ |")
L.append("")
L.append("Les écritures terminées par « … » sont illimitées : $\\dfrac{1}{3} = 0{,}3333\\ldots$\n")

L.append("## II. Passer d’une écriture à l’autre {Primaire}\n")
L.append("| Conversion | Méthode et exemple |")
L.append("|---|---|")
for c, m in [
    ("Fraction → décimal", "on divise le numérateur par le dénominateur : $\\dfrac{3}{4} = 3 \\div 4 = 0{,}75$"),
    ("Décimal → pourcentage", "on multiplie par $100$ : $0{,}75 = 75\\,\\%$"),
    ("Pourcentage → décimal", "on divise par $100$ : $8\\,\\% = 0{,}08$"),
    ("Pourcentage → fraction", "on écrit sur $100$ et on simplifie : $40\\,\\% = \\dfrac{40}{100} = \\dfrac{2}{5}$"),
    ("Décimal → fraction", "on écrit une fraction décimale et on simplifie : $0{,}125 = \\dfrac{125}{1\\,000} = \\dfrac{1}{8}$"),
]:
    L.append(f"| {c} | {m} |")
L.append("")

L.append("## III. Calculer un pourcentage de tête {Primaire}\n")
L.append("| Pourcentage | On calcule | Exemple avec 80 |")
L.append("|---|---|---|")
for p, calc, ex in [
    ("1 %", "on divise par 100", "0,8"),
    ("10 %", "on divise par 10", "8"),
    ("20 %", "on divise par 5", "16"),
    ("25 %", "on divise par 4", "20"),
    ("50 %", "on divise par 2", "40"),
    ("75 %", "on divise par 4, puis on multiplie par 3", "60"),
    ("100 %", "le nombre lui-même", "80"),
]:
    L.append(f"| {p} | {calc} | {ex} |")
L.append("")
L.append("::: retenir Pourcentage d’une quantité")
L.append("Prendre $t\\,\\%$ d’une quantité $Q$, c’est calculer :")
L.append("$$Q \\times \\frac{t}{100}$$")
L.append("Par exemple, $15\\,\\%$ de $60$ font $60 \\times 0{,}15 = 9$.")
L.append(":::\n")
L.append("::: retenir Calculer un pourcentage")
L.append("La part, en pourcentage, que représente $A$ dans $B$ vaut :")
L.append("$$\\frac{A}{B} \\times 100$$")
L.append("Par exemple, $12$ élèves sur $30$ représentent $12 \\div 30 \\times 100 = 40\\,\\%$ de la classe.")
L.append(":::\n")

texte = "---\n" + json.dumps(INFO, ensure_ascii=False, indent=2) + "\n---\n" + "\n".join(L).rstrip() + "\n"
(ICI / "formulaire.md").write_bytes(texte.encode("utf-8"))
print("formulaire.md écrit :", len(FRACTIONS), "fractions")
