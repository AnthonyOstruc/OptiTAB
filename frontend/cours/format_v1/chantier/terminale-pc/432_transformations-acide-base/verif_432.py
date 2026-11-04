# -*- coding: utf-8 -*-
"""Vérification (sympy) des calculs de la notion 432 « Transformations acide-base ».

    python verif_432.py

Contrôle : conservation des éléments et des charges de chaque demi-équation et
équation écrite, charges formelles, décompte des électrons de Lewis, valeurs de pH
et de concentrations (avec la règle : décimales du pH = chiffres significatifs).
"""
import re
from collections import Counter

import sympy as sp

ok = 0
erreurs = []


def check(cond, msg):
    global ok
    if cond:
        ok += 1
    else:
        erreurs.append(msg)


# ------------------------------------------------------------------ formules
def atomes(formule):
    """Composition élémentaire et charge d'une formule mhchem simple (parenthèses, tirets)."""
    f = formule
    charge = 0
    m = re.search(r"(\^\d+)?([+-])$", f)   # « NH4+ » : charge +1 ; « CO3^2- » : charge -2
    corps = f
    if m:
        n = (m.group(1) or "").lstrip("^")
        charge = (int(n) if n else 1) * (1 if m.group(2) == "+" else -1)
        corps = f[: m.start()]
    corps = corps.replace("-", "")  # liaisons des formules semi-développées
    def lire(s):
        c, i = Counter(), 0
        while i < len(s):
            if s[i] == "(":
                prof, j = 1, i + 1
                while prof:
                    prof += {"(": 1, ")": -1}.get(s[j], 0)
                    j += 1
                k = j
                while k < len(s) and s[k].isdigit():
                    k += 1
                mult = int(s[j:k]) if k > j else 1
                for e, n in lire(s[i + 1: j - 1]).items():
                    c[e] += n * mult
                i = k
                continue
            m2 = re.match(r"([A-Z][a-z]?)(\d*)", s[i:])
            c[m2.group(1)] += int(m2.group(2)) if m2.group(2) else 1
            i += len(m2.group(0))
        return c
    return lire(corps), charge


def membre(s):
    tot, q = Counter(), 0
    for t in s.split(" + "):
        t = t.strip()
        m = re.match(r"^(\d+) (.+)$", t)
        k, t = (int(m.group(1)), m.group(2)) if m else (1, t)
        t = re.sub(r"\((aq|l|g|s)\)", "", t)
        if t == "H+":
            c, z = Counter({"H": 1}), 1
        elif t == "CO2,H2O":
            c, z = Counter({"C": 1, "O": 3, "H": 2}), 0
        else:
            c, z = atomes(t)
        for e, n in c.items():
            tot[e] += k * n
        q += k * z
    return tot, q


def equilibree(eq):
    g, d = re.split(r" (?:=|->|<=>) ", eq)
    return membre(g) == membre(d)


EQUATIONS = [
    # cours
    "CH3COOH = CH3COO- + H+", "NH4+ = NH3 + H+", "H2O = HO- + H+",
    "NH3 + H+ = NH4+", "CH3COOH + NH3 -> CH3COO- + NH4+",
    "CH3COOH + H2O <=> CH3COO- + H3O+",
    "CO2,H2O(aq) -> CO2(g) + H2O(l)",
    "HCl(g) + H2O(l) -> H3O+(aq) + Cl-(aq)",
    "H3O+ = H2O + H+", "CO2,H2O = HCO3- + H+", "HCO3- = CO3^2- + H+",
    "CH3-COOH = CH3-COO- + H+", "CH3-NH3+ = CH3-NH2 + H+",
    # exercice
    "CH3CH2NH2 + H+ = CH3CH2NH3+", "CH3CH2NH2 + H2O <=> CH3CH2NH3+ + HO-",
    "CH3CH2NH2(aq) + H2O(l) <=> CH3CH2NH3+(aq) + HO-(aq)",
    "C2H5NH2 + H+ = C2H5NH3+", "C2H5NH2 + H2O <=> C2H5NH3+ + HO-",
]
for eq in EQUATIONS:
    check(equilibree(eq), f"équation non équilibrée : {eq}")

# décomptes écrits dans le texte
g, _ = membre("CH3COOH + NH3")
check(g == Counter({"C": 2, "H": 7, "O": 2, "N": 1}), "cours : « 2 C, 7 H, 2 O et 1 N »")
g, _ = membre("CH3CH2NH2 + H2O")
check(g == Counter({"C": 2, "H": 9, "N": 1, "O": 1}), "exercice : « 2 C, 9 H, 1 N et 1 O »")
# fiche : H2SO4 et SO4^2- diffèrent de deux H+ (pas un couple)
a, qa = atomes("H2SO4"); b, qb = atomes("SO4^2-")
check(a["H"] - b["H"] == 2 and qa - qb == 2, "H2SO4/SO4^2- : deux H+ d'écart")

# ------------------------------------------------------------------ Lewis
VALENCE = {"H": 1, "C": 4, "N": 5, "O": 6}
def charge_formelle(e, non_liants, liaisons):
    return VALENCE[e] - non_liants - liaisons
check(charge_formelle("O", 6, 1) == -1, "O du carboxylate : 6 - 6 - 1 = -1")
check(charge_formelle("N", 0, 4) == +1, "N de l'ammonium : 5 - 0 - 4 = +1")
# éthylamine C2H7N : 20 électrons, 10 doublets, 9 liaisons, 1 doublet non liant
ne = 2 * 4 + 7 * 1 + 5
a, _ = atomes("C2H5NH2"); b, _ = atomes("CH3-CH2-NH2")
check(a == b == Counter({"C": 2, "H": 7, "N": 1}), "C2H5NH2 = CH3-CH2-NH2 = C2H7N")
check(ne == 20 and ne // 2 == 10, "éthylamine : 20 électrons de valence, 10 doublets")
liaisons = 1 + 5 + 1 + 2
check(liaisons == 9 and ne // 2 - liaisons == 1, "éthylamine : 9 liaisons, 1 doublet non liant")
# ion éthylammonium C2H8N+ : 20 électrons, 10 liaisons, 0 doublet non liant
ne2 = 2 * 4 + 8 * 1 + 5 - 1
check(ne2 // 2 == 1 + 5 + 1 + 3, "éthylammonium : 10 liaisons, aucun doublet non liant")
# octet de l'azote si le doublet restait : 4 liaisons + 1 doublet = 10 électrons
check(2 * 4 + 2 == 10, "azote avec 4 liaisons et 1 doublet : 10 électrons")


# ------------------------------------------------------------------ pH
def ph(h):
    return -sp.log(sp.nsimplify(h), 10)


def arrondi(x, n):
    return round(float(x), n)


def cs(x, n):
    """Arrondi à n chiffres significatifs."""
    x = float(x)
    return float(f"{x:.{n - 1}e}")


check(arrondi(ph("2.5e-4"), 2) == 3.60, "pH(2,5e-4) = 3,60")
check(cs(sp.Float(10) ** sp.Float(-8.20), 2) == 6.3e-9, "10^-8,20 = 6,3e-9")
check(arrondi(sp.log(2, 10), 1) == 0.3, "log 2 ≈ 0,3")
for c, attendu in ((1e-1, 1.00), (1e-2, 2.00), (1e-3, 3.00), (1e-4, 4.00)):
    check(arrondi(ph(c), 2) == attendu, f"pH attendu pour c = {c}")
# exercice, question 4
h = sp.Float(10) ** sp.Float(-11.8)
check(abs(float(h) - 1.58e-12) < 0.005e-12, "10^-11,8 ≈ 1,58e-12")
check(cs(h, 1) == 2e-12, "[H3O+] = 2e-12 (un chiffre significatif)")
check(11.8 > 7, "pH 11,8 : solution basique")

print(f"{ok} contrôles justes, {len(erreurs)} erreur(s)")
for e in erreurs:
    print("  ✗", e)
print("TOUT EST JUSTE" if not erreurs else "ERREURS À CORRIGER")
