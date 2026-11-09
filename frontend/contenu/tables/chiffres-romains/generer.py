# -*- coding: utf-8 -*-
"""Génère formulaire.md des chiffres romains (conversions faites par le script).

    python frontend/contenu/tables/chiffres-romains/generer.py
"""
import json
from pathlib import Path

ICI = Path(__file__).resolve().parent

VALEURS = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
           (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def romain(n):
    s = ""
    for v, r in VALEURS:
        while n >= v:
            s += r
            n -= v
    return s


def arabe(s):
    t = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    for i, c in enumerate(s):
        v = t[c]
        total += -v if i + 1 < len(s) and t[s[i + 1]] > v else v
    return total


# Contrôle : aller-retour exact de 1 à 3 999.
for n in range(1, 4000):
    assert arabe(romain(n)) == n, n

INFO = {
    "slug": "chiffres-romains",
    "titre": "Chiffres romains",
    "titreCourt": "Chiffres romains",
    "titreSeo": "Chiffres romains : tableau de 1 à 100, règles et convertisseur",
    "description": "Les chiffres romains : les 7 symboles, les règles d’écriture, le tableau de 1 à 100, les centaines, les milliers et les années, avec la méthode pour convertir.",
    "chapo": "Les sept symboles, les règles pour écrire et lire un nombre en chiffres romains, le tableau de 1 à 100 et les années les plus recherchées.",
    "resume": "Tableau de 1 à 100, règles, années",
    "vignette": "cadran_horloge",
    "theme": "Nombres",
    "niveaux": ["Primaire", "Collège"],
    "ordre": 3,
    "publie": "2026-11-09",
    "modifie": "2026-11-09",
    "motsCles": ["chiffres romains", "chiffre romain", "tableau chiffres romains", "chiffres romains de 1 à 100", "convertir chiffres romains", "2026 en chiffres romains", "siècle en chiffres romains", "nombres romains"],
    "figures": [
        {"nom": "cadran_horloge", "alt": "Cadran d’horloge en chiffres romains de I à XII, où 4 heures est écrit IIII, comme sur la plupart des horloges."},
    ],
    "chapitresLies": ["cm1/les-nombres-entiers-jusqu-a-999-999", "cm2/les-grands-nombres-entiers"],
    "faq": [
        ["Comment écrire 2026 en chiffres romains ?", f"2026 s’écrit {romain(2026)} : 2000 = MM, 20 = XX et 6 = VI."],
        ["Comment écrire 4 et 9 en chiffres romains ?", "4 s’écrit IV (5 − 1) et 9 s’écrit IX (10 − 1) : un symbole plus petit placé avant un plus grand se soustrait. Sur les horloges, 4 est souvent écrit IIII par tradition."],
        ["Quel est le plus grand nombre en chiffres romains ?", "Avec les sept symboles et la règle des trois répétitions au plus, le plus grand nombre est 3 999 = MMMCMXCIX. Pour aller au-delà, les Romains surmontaient un symbole d’une barre, qui le multipliait par 1 000."],
        ["Le zéro existe-t-il en chiffres romains ?", "Non : la numération romaine n’a pas de symbole pour zéro. Elle n’est pas une numération de position, contrairement à nos chiffres."],
    ],
}

L = ["<!-- optitab:1 -->"]
L.append("## I. Les sept symboles {Primaire}\n")
L.append("| Symbole | Valeur |")
L.append("|---|---|")
for sym, val in [("I", "1"), ("V", "5"), ("X", "10"), ("L", "50"), ("C", "100"), ("D", "500"), ("M", "1 000")]:
    L.append(f"| **{sym}** | {val} |")
L.append("")
L.append("[IMAGE_1]\n")

L.append("## II. Les règles d’écriture {Primaire}\n")
L.append("| Règle | Exemple |")
L.append("|---|---|")
for r, ex in [
    ("Un symbole suivi d’un symbole plus petit ou égal s’ajoute", "VI = 5 + 1 = 6 ; XXV = 25"),
    ("I, X ou C placé avant un symbole plus grand se soustrait", "IV = 4 ; IX = 9 ; XL = 40 ; XC = 90 ; CD = 400 ; CM = 900"),
    ("Un même symbole n’est jamais répété plus de trois fois", "30 = XXX, mais 40 = XL"),
    ("V, L et D ne sont jamais répétés ni soustraits", "10 = X (et non VV) ; 45 = XLV"),
    ("On écrit les milliers, puis les centaines, les dizaines et les unités", "1 987 = M + CM + LXXX + VII = MCMLXXXVII"),
]:
    L.append(f"| {r} | {ex} |")
L.append("")
L.append("::: attention Le 4 des horloges")
L.append("Sur la plupart des cadrans, 4 heures est écrit IIII et non IV : c’est une tradition d’horlogerie, pas la règle d’écriture.")
L.append(":::\n")

L.append("## III. Unités, dizaines, centaines, milliers {Primaire}\n")
L.append("| Chiffre | Unités | Dizaines | Centaines | Milliers |")
L.append("|---|---|---|---|---|")
for c in range(1, 10):
    L.append(f"| {c} | {romain(c)} | {romain(10 * c)} | {romain(100 * c)} | {romain(1000 * c) if c <= 3 else '—'} |")
L.append("")
L.append("::: methode Convertir un nombre en chiffres romains")
L.append(f"On décompose le nombre et on lit chaque morceau dans le tableau : $1\\,987 = 1\\,000 + 900 + 80 + 7$, soit M + CM + LXXX + VII = **{romain(1987)}**.")
L.append(":::\n")
L.append("::: methode Lire un nombre en chiffres romains")
L.append(f"On lit de gauche à droite en regroupant les soustractions : MCMXCIX = M + CM + XC + IX = $1\\,000 + 900 + 90 + 9 = 1\\,999$.")
L.append(":::\n")

L.append("## IV. Tableau de 1 à 100 {Primaire}\n")
for debut in (1, 51):
    L.append("| Nombre | Romain | Nombre | Romain |")
    L.append("|---|---|---|---|")
    for n in range(debut, debut + 25):
        L.append(f"| {n} | {romain(n)} | {n + 25} | {romain(n + 25)} |")
    L.append("")

L.append("## V. Grands nombres et années {Collège}\n")
L.append("| Nombre | Chiffres romains |")
L.append("|---|---|")
for n in (200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 3000, 3999):
    L.append(f"| {n:,}".replace(",", " ") + f" | {romain(n)} |")
L.append("")
L.append("| Année | Chiffres romains |")
L.append("|---|---|")
for n in (1515, 1789, 1900, 1945, 1999, 2000, 2010, 2020, 2024, 2025, 2026, 2027, 2030):
    L.append(f"| {n} | {romain(n)} |")
L.append("")

L.append("## VI. Les siècles {Collège}\n")
L.append("| Siècle | Années | Siècle | Années |")
L.append("|---|---|---|---|")
for s in range(1, 12):
    s2 = s + 11
    d1, f1 = (s - 1) * 100 + 1, s * 100
    d2, f2 = (s2 - 1) * 100 + 1, s2 * 100
    L.append(f"| {romain(s)}ᵉ | {d1} à {f1} | {romain(s2)}ᵉ | {d2} à {f2} |")
L.append("")
L.append("::: retenir")
L.append(f"Nous sommes au **{romain(21)}ᵉ siècle** (années 2001 à 2100). Le numéro du siècle est le nombre de centaines plus un : l’année 1789 est au {romain(18)}ᵉ siècle.")
L.append(":::\n")

texte = "---\n" + json.dumps(INFO, ensure_ascii=False, indent=2) + "\n---\n" + "\n".join(L).rstrip() + "\n"
(ICI / "formulaire.md").write_bytes(texte.encode("utf-8"))
print("formulaire.md écrit ; contrôle aller-retour 1 → 3 999 réussi")
