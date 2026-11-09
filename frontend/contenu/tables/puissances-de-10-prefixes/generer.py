# -*- coding: utf-8 -*-
"""Génère formulaire.md « Puissances de 10 et préfixes » (valeurs calculées).

    python frontend/contenu/tables/puissances-de-10-prefixes/generer.py
"""
import json
import re
from pathlib import Path

ICI = Path(__file__).resolve().parent
NB = " "


def millier(n):
    return f"{n:,}".replace(",", NB)


def decimal_puissance(e):
    """Écriture décimale de 10^e, avec espaces fines (milliers et décimales par 3)."""
    if e >= 0:
        return millier(10 ** e)
    dec = "0" * (-e - 1) + "1"
    groupes = [dec[i:i + 3] for i in range(0, len(dec), 3)]
    return "0," + NB.join(groupes)


assert decimal_puissance(6) == f"1{NB}000{NB}000" and decimal_puissance(-3) == "0,001" and decimal_puissance(-6) == f"0,000{NB}001"

INFO = {
    "slug": "puissances-de-10-prefixes",
    "titre": "Puissances de 10 et préfixes",
    "titreCourt": "Puissances de 10 et préfixes",
    "titreSeo": "Puissances de 10 et préfixes : kilo, méga, giga, micro, nano",
    "description": "Le tableau des puissances de 10 et des préfixes (téra, giga, méga, kilo, milli, micro, nano, pico), l’écriture scientifique et les puissances de 2.",
    "chapo": "Chaque puissance de 10 avec son écriture décimale et son nom, les préfixes des unités du pico au téra, l’écriture scientifique et les puissances de 2 utilisées en informatique.",
    "resume": "kilo, méga, giga, micro, nano, écriture scientifique",
    "vignette": "echelle_prefixes",
    "theme": "Nombres",
    "niveaux": ["Collège", "Lycée"],
    "ordre": 10,
    "publie": "2026-11-09",
    "modifie": "2026-11-09",
    "motsCles": ["puissances de 10", "préfixes", "tableau des préfixes", "kilo méga giga", "micro nano pico", "écriture scientifique", "puissances de 2", "conversion octet ko Mo Go"],
    "figures": [
        {"nom": "echelle_prefixes", "alt": "Échelle des préfixes, de pico (10 puissance −12) à téra (10 puissance 12) en passant par nano, micro, milli, l’unité, kilo, méga et giga : on multiplie par 1 000 à chaque case vers la droite."},
    ],
    "chapitresLies": ["4e/puissances-et-notation-scientifique", "3e/puissances-racines-et-ecriture-scientifique", "4e/grandeurs-composees-et-unites"],
    "faq": [
        ["Combien vaut un giga ?", "Le préfixe giga (G) signifie 10⁹, soit un milliard. Un gigaoctet (Go) vaut donc 1 000 000 000 octets selon le Système international."],
        ["Quelle est la différence entre micro et nano ?", "Micro (µ) vaut 10⁻⁶, un millionième ; nano (n) vaut 10⁻⁹, un milliardième. Un nanomètre est donc 1 000 fois plus petit qu’un micromètre."],
        ["Comment écrire un nombre en écriture scientifique ?", "On l’écrit a × 10ⁿ avec 1 ≤ a < 10. Par exemple, 45 000 = 4,5 × 10⁴ et 0,000 32 = 3,2 × 10⁻⁴."],
        ["Pourquoi dit-on parfois qu’un kilooctet vaut 1 024 octets ?", "Parce que les ordinateurs comptent en puissances de 2 et que 2¹⁰ = 1 024 est proche de 1 000. La norme recommande d’écrire kibioctet (Kio) pour 1 024 octets et de garder kilooctet (ko) pour 1 000 octets."],
    ],
}

L = ["<!-- optitab:1 -->"]
L.append("## I. Puissances de 10 {Collège}\n")
L.append("| Puissance | Écriture décimale | Nom |")
L.append("|---|---|---|")
noms = {12: "mille milliards", 9: "un milliard", 6: "un million", 3: "mille", 2: "cent", 1: "dix", 0: "un",
        -1: "un dixième", -2: "un centième", -3: "un millième", -6: "un millionième", -9: "un milliardième", -12: "un billionième"}
for e in (9, 6, 3, 2, 1, 0, -1, -2, -3, -6, -9):
    L.append(f"| $10^{{{e}}}$ | {decimal_puissance(e)} | {noms[e]} |")
L.append("")
L.append("::: retenir")
L.append("$10^n$ s’écrit avec un $1$ suivi de $n$ zéros ; $10^{-n}$ s’écrit avec $n$ chiffres après la virgule, le dernier étant $1$.")
L.append(":::\n")

L.append("## II. Les préfixes des unités {Collège}\n")
L.append("[IMAGE_1]\n")
L.append("| Préfixe | Symbole | Puissance | Exemple |")
L.append("|---|---|---|---|")
for nom, sym, e, ex in [
    ("téra", "T", 12, "1 To = 10¹² octets"),
    ("giga", "G", 9, "1 GHz = 10⁹ Hz"),
    ("méga", "M", 6, "1 MW = 10⁶ W"),
    ("kilo", "k", 3, "1 km = 10³ m"),
    ("hecto", "h", 2, "1 hL = 100 L"),
    ("déca", "da", 1, "1 dam = 10 m"),
    ("déci", "d", -1, "1 dm = 0,1 m"),
    ("centi", "c", -2, "1 cL = 0,01 L"),
    ("milli", "m", -3, "1 mg = 10⁻³ g"),
    ("micro", "µ", -6, "1 µm = 10⁻⁶ m"),
    ("nano", "n", -9, "1 ns = 10⁻⁹ s"),
    ("pico", "p", -12, "1 pF = 10⁻¹² F"),
]:
    L.append(f"| {nom} | {sym} | $10^{{{e}}}$ | {ex} |")
L.append("")

L.append("## III. Écriture scientifique {Collège}\n")
L.append("::: definition")
L.append("L’écriture scientifique d’un nombre est $a \\times 10^n$, avec $1 \\leqslant a < 10$ et $n$ entier relatif.")
L.append(":::\n")
L.append("| Grandeur | Valeur | Écriture scientifique |")
L.append("|---|---|---|")
for g, v, s in [
    ("Vitesse de la lumière", f"300{NB}000{NB}000 m/s", "$3 \\times 10^{8}$ m/s"),
    ("Distance Terre-Soleil", f"150{NB}000{NB}000 km", "$1{,}5 \\times 10^{8}$ km"),
    ("Population mondiale (2025)", "environ 8,2 milliards", "$\\approx 8{,}2 \\times 10^{9}$"),
    ("Épaisseur d’un cheveu", "0,08 mm", "$8 \\times 10^{-2}$ mm"),
    ("Taille d’un virus", "0,000 1 mm", "$10^{-4}$ mm"),
]:
    L.append(f"| {g} | {v} | {s} |")
L.append("")
L.append("::: methode Écrire un nombre en écriture scientifique")
L.append("On place la virgule après le premier chiffre non nul et on compte de combien de rangs elle s’est déplacée : $45\\,000 = 4{,}5 \\times 10^{4}$ (4 rangs vers la gauche) et $0{,}000\\,32 = 3{,}2 \\times 10^{-4}$ (4 rangs vers la droite).")
L.append(":::\n")

L.append("## IV. Puissances de 2 et informatique {Lycée}\n")
L.append("| $n$ | $2^n$ | $n$ | $2^n$ |")
L.append("|---|---|---|---|")
for n in range(0, 11):
    m = n + 11
    L.append(f"| {n} | {millier(2 ** n)} | {m} | {millier(2 ** m)} |")
L.append("")
L.append("| Unité | Système international | Puissance de 2 |")
L.append("|---|---|---|")
for u, si, b in [
    ("kilooctet", f"1 ko = 1{NB}000 octets", f"1 Kio = 2¹⁰ = 1{NB}024 octets"),
    ("mégaoctet", "1 Mo = 10⁶ octets", f"1 Mio = 2²⁰ = 1{NB}048{NB}576 octets"),
    ("gigaoctet", "1 Go = 10⁹ octets", "1 Gio = 2³⁰ octets"),
]:
    L.append(f"| {u} | {si} | {b} |")
L.append("")
L.append("Un octet vaut $8$ bits.\n")
assert 2 ** 20 == 1048576

texte = "---\n" + json.dumps(INFO, ensure_ascii=False, indent=2) + "\n---\n" + "\n".join(L).rstrip() + "\n"
(ICI / "formulaire.md").write_bytes(texte.encode("utf-8"))
print("formulaire.md écrit")
