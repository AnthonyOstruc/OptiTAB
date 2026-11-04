# -*- coding: utf-8 -*-
"""Vérification des calculs de la notion 265 (5e : fractions, quotients et comparaisons).

Cours, fiche, 10 exercices et figures : chaque résultat est recalculé en
fractions exactes (sympy.Rational). Lancer : python verif_265.py
"""
import re
from pathlib import Path

from sympy import Rational as R, gcd

ICI = Path(__file__).resolve().parent
n_ok = 0


def ok(cond, msg):
    global n_ok
    assert cond, msg
    n_ok += 1


def de(fr, q):
    """fr de la quantité q, par les deux ordres de calcul du cours."""
    a, b = fr.p, fr.q
    r1 = R(q) / b * a
    r2 = R(q) * a / b
    ok(r1 == r2 == fr * q, f"{fr} de {q}")
    return fr * q


def irreductible(fr):
    return gcd(fr.p, fr.q) == 1


def egal_ecrit(a, b, c, d):
    """a/b = c/d écrit (non simplifié)."""
    ok(R(a, b) == R(c, d), f"{a}/{b} = {c}/{d}")


# ================================================================== COURS
ok(R(7, 4) == 1 + R(3, 4) and R(5, 5) == 1, "7/4 = 1 + 3/4, 5/5 = 1")
ok(5 * R(2, 5) == 2, "crêpes : 5 × 2/5 = 2")
ok(4 * R(7, 4) == 7 and R(7, 4) == R(175, 100), "4 × 7/4 = 7 ; 7/4 = 1,75")
ok(9 * R(2, 9) == 2, "9 × 2/9 = 2")
ok(6 * R(83, 100) == R(498, 100) and R(5, 6) != R(83, 100), "6 × 0,83 = 4,98 ≠ 5")
ok(abs(R(5, 6) - R(83, 100)) < R(1, 100), "5/6 ≈ 0,83")
ok(4 * (R(25, 10) / 4) == R(25, 10), "2,5/4")
ok(R(2, 3) == R(4, 6) == R(8, 12), "2/3 = 4/6 = 8/12")
ok(R(8, 12) * 6 == 4, "barres : 8/12 de 6 cm = 4 cm (trait vert)")
ok(R(24, 36) == R(2, 3) and 24 % 12 == 0 and 36 % 12 == 0, "24/36 = 2/3")
ok(R(24, 36) == R(12, 18) == R(6, 9) == R(2, 3), "24/36 par étapes")
egal_ecrit(4, 9, 20, 45)
ok(20 == 5 * 4 and R(3, 5) == R(12, 20), "3/5 = 12/20")
ok(R(1, 3) != R(2, 4) and R(1, 3) < R(1, 2) and R(2, 4) == R(1, 2), "1/3 ≠ 2/4")
ok(R(4, 7) < R(6, 7), "4/7 < 6/7")
ok(R(4, 9) < 1 < R(7, 6), "4/9 < 1 < 7/6")
ok(R(3, 5) < R(13, 20), "3/5 < 13/20")
ok([R(3, 10), R(1, 2), R(2, 5), R(7, 20)] == [R(6, 20), R(10, 20), R(8, 20), R(7, 20)], "ranger en vingtièmes")
ok(sorted([R(3, 10), R(1, 2), R(2, 5), R(7, 20)]) == [R(3, 10), R(7, 20), R(2, 5), R(1, 2)], "ordre croissant cours")
ok(R(1, 8) < R(1, 4), "1/8 < 1/4")
ok(R(7, 3) == R(6, 3) + R(1, 3) == 2 + R(1, 3) and 2 < R(7, 3) < 3, "7/3 = 2 + 1/3")
ok(R(2, 3) < 1 < R(5, 3) < 2 < R(7, 3), "ordre sur la droite des tiers")
ok(de(R(3, 5), 40) == 24 and 40 / 5 == 8, "3/5 de 40 € = 24 €")
ok(de(R(2, 3), 60) == 40, "2/3 h = 40 min")
ok(3 * 40 // 5 == 24 and 3 * 40 == 120, "(3 × 40) ÷ 5 = 24")
ok(de(R(1, 2), 100) == 50 and de(R(3, 4), 50) == R(75, 2) and R(75, 2) == R(375, 10), "1/2 de 1 L et 3/4 de 50 cL")
ok(de(R(1, 2), 100) > de(R(3, 4), 50), "1/2 de 1 L > 3/4 de 50 cL")

# ================================================================== 2789
ok([R(3, 8), R(4, 5), R(5, 4)] == [R(3, 8), R(4, 5), R(4 + 1, 4)], "lire les fractions")
ok(R(5, 4) == 1 + R(1, 4) and R(5, 4) > 1, "5/4 = 1 + 1/4")
ok(3 * R(2, 3) == 2 and R(6, 3) == 2, "3 × 2/3 = 2")
ok(4 * R(5, 4) == 5 and 7 * R(2, 7) == 2 and 9 * R(4, 9) == 4, "compléter les produits")
ok(R(5, 4) == R(125, 100) and R(7, 5) == R(14, 10), "5/4 = 1,25 ; 7/5 = 1,4")
ok(3 * R(67, 100) == R(201, 100) and R(201, 100) != 2, "3 × 0,67 = 2,01")
ok(R(2, 3) != R(67, 100) and abs(R(2, 3) - R(67, 100)) < R(1, 100), "2/3 ≈ 0,67")

# ================================================================== 2803
ok(24 / 4 == 6 and de(R(3, 4), 24) == 18 and 24 - 18 == 6 and de(R(1, 4), 24) == 6, "jus 24 L")
ok(1 - R(3, 4) == R(1, 4), "reste 1/4")
ok(de(R(2, 5), 35) == 14 and 35 / 5 == 7, "2/5 de 35 €")
ok(de(R(5, 6), 30) == 25 and 30 / 6 == 5, "5/6 de 30 min")
ok(de(R(3, 10), 200) == 60 and 200 / 10 == 20, "3/10 de 200 g")
ok(24 * 3 == 72 and 72 / 4 == 18, "24 × 3 ÷ 4")
ok(de(R(3, 4), 60) == 45 and de(R(5, 4), 60) == 75 and 75 == 60 + 15, "3/4 h = 45 min ; 5/4 h = 75 min")
ok(R(3, 4) * 60 != 75, "0,75 h ≠ 75 min")

# ================================================================== 2794
ok(R(3, 4) == R(6, 8) and 3 * 2 == 6, "3/4 = 6/8")
egal_ecrit(2, 3, 10, 15)
egal_ecrit(5, 8, 25, 40)
egal_ecrit(7, 2, 28, 8)
egal_ecrit(36, 48, 3, 4)
ok(36 // 12 == 3 and 48 // 12 == 4, "36/48 ÷ 12")
for a, b, c, d in [(18, 24, 3, 4), (15, 35, 3, 7), (42, 56, 3, 4), (60, 45, 4, 3)]:
    ok(R(a, b) == R(c, d) and irreductible(R(c, d)), f"simplifier {a}/{b}")
ok(R(42, 56) == R(21, 28) and R(60, 45) == R(12, 9), "étapes intermédiaires")
ok(R(1, 2) == R(4, 8) and R(4, 5) == R(8, 10) and R(1, 3) == R(4, 12) and R(5, 6) == R(10, 12), "même dénominateur")
ok(R(1 + 2, 2 + 2) == R(3, 4) and R(1, 2) == R(2, 4) and R(1, 2) != R(3, 4), "Léo")

# ================================================================== 2790
ok(R(7, 9) > R(5, 9) and R(11, 6) < R(13, 6), "même dénominateur")
ok(R(9, 8) > 1 and R(7, 10) < 1 and R(12, 12) == 1 and R(15, 14) > 1 and R(99, 100) < 1, "comparer à 1")
ok(R(5, 6) == R(10, 12) < R(11, 12), "5/6 < 11/12")
ok(R(7, 5) == R(14, 10) > R(13, 10), "7/5 > 13/10")
ok(R(2, 3) == R(6, 9) > R(5, 9), "2/3 > 5/9")
for a, b in [(6, 12), (5, 10), (3, 9)]:
    ok(b % a == 0, f"{a} et {b} multiples")
ok(R(3, 8) == R(6, 16) > R(5, 16), "rubans : Alice")
ok(R(1, 16) * 2 == R(1, 8), "un seizième = moitié d'un huitième")

# ================================================================== 2800
l1 = [R(5, 8), R(3, 4), R(1, 2), R(7, 16), R(9, 8)]
ok([x * 16 for x in l1] == [10, 12, 8, 7, 18], "en seizièmes")
ok(sorted(l1) == [R(7, 16), R(1, 2), R(5, 8), R(3, 4), R(9, 8)], "ordre croissant")
l2 = [R(4, 3), R(5, 6), R(7, 12), R(1), R(3, 2)]
ok([x * 12 for x in l2] == [16, 10, 7, 12, 18], "en douzièmes")
ok(sorted(l2, reverse=True) == [R(3, 2), R(4, 3), R(1), R(5, 6), R(7, 12)], "ordre décroissant")
for n, d, e in [(17, 5, 3), (23, 4, 5), (31, 10, 3)]:
    ok(divmod(n, d)[0] == e and e < R(n, d) < e + 1, f"encadrer {n}/{d}")
ok(17 == 5 * 3 + 2 and 23 == 4 * 5 + 3 and 31 == 10 * 3 + 1, "décompositions")
ok(R(2, 5) == R(8, 20) < R(9, 20) < R(10, 20) == R(1, 2), "intercaler 9/20")
ok([k for k in range(0, 21) if R(2, 5) < R(k, 20) < R(1, 2)] == [9], "9/20 seule solution")
ok(R(3, 4) == R(6, 8) < R(7, 8) < 1 and [k for k in range(9) if R(3, 4) < R(k, 8) < 1] == [7], "intercaler 7/8")
# figure ranger_corrige : abscisses en seizièmes et 1/2 = 8/16
ok([R(7, 16), R(1, 2), R(5, 8), R(3, 4), R(9, 8)] == [R(k, 16) for k in (7, 8, 10, 12, 18)], "figure ranger")
ok(R(20, 16) == R(5, 4), "droite jusqu'à 5/4")

# ================================================================== 2801
A, B, C = R(3, 4), R(6, 4), R(9, 4)
ok(B == R(3, 2), "6/4 = 3/2")
D, E, F = R(5, 4), R(11, 4), R(1, 2)
ok(F == R(2, 4), "1/2 = 2/4")
ok([x * 4 for x in (A, B, C, D, E, F)] == [3, 6, 9, 5, 11, 2], "positions en quarts")
ok(C == 2 + R(1, 4) and E == 2 + R(3, 4) and 2 < E < 3, "décomposer")
ok(sorted([A, B, C, D, E, F]) == [F, A, D, B, C, E], "ordre F, A, D, B, C, E")
ok(max(A, B, C, D, E, F) <= 3, "tous sur la droite 0..3")

# ================================================================== 2793
ok(4 * R(3, 4) == 3 and R(12, 4) == 3, "table A")
ok(8 * R(5, 8) == 5, "table B")
ok(R(3, 4) == R(6, 8) > R(5, 8), "table A > table B")
ok(R(3, 4) == R(75, 100) and R(5, 8) == R(625, 1000) and R(75, 100) > R(625, 1000), "décimales")
ok(de(R(3, 4), 8) == 6 and 8 / 4 == 2 and R(6, 8) == R(3, 4) and 6 - 5 == 1, "6 pizzas, une de plus")

# ================================================================== 2808
ok(R(4, 5) == R(8, 10) > R(7, 10), "4/5 > 7/10")
ok(de(R(4, 5), 50) == 40 and de(R(7, 10), 100) == 70 and 70 > 40, "40 cL, 70 cL")
ok(1 - R(4, 5) == R(1, 5) and de(R(1, 5), 50) == 10, "reste Alice")
ok(1 - R(7, 10) == R(3, 10) and de(R(3, 10), 100) == 30, "reste Bilal")
ok(40 + 10 == 50 and 70 + 30 == 100, "contrôles")
ok(de(R(4, 5), 100) == 80 > 70, "même gourde : Alice")
ok(100 == 2 * 50, "gourde deux fois plus grande")
# figure : u = 0,068 cm par cL
ok(abs(100 * 0.068 - 6.8) < 1e-9 and abs(40 * 0.068 - 2.72) < 1e-9, "figure gourdes à l'échelle")

# ================================================================== 2807
lundi = de(R(2, 5), 150)
ok(lundi == 60 and 150 / 5 == 30, "lundi 60 L")
reste1 = 150 - lundi
ok(reste1 == 90, "reste 90 L")
mardi = de(R(1, 3), reste1)
ok(mardi == 30, "mardi 30 L")
reste2 = reste1 - mardi
ok(reste2 == 60, "reste 60 L")
ok(R(lundi + mardi, 150) == R(90, 150) == R(9, 15) == R(3, 5), "3/5 utilisés")
ok(R(mardi, 150) == R(1, 5) and de(R(1, 3), 150) == 50 and 50 != 30, "Hugo : 1/5 et non 1/3")
ok(R(reste2, 150) == R(2, 5) < R(1, 2) and 150 / 2 == 75 and 60 < 75 and R(75, 150) == R(1, 2), "moins de la moitié")
ok(150 / 5 == 30 and 2 * 30 == 60 and 30 == mardi, "figure : 5 parts de 30 L (2 + 1 + 2)")

# ================================================================== 2809
part = de(R(5, 8), 480)
ok(part == 300 and 480 / 8 == 60, "300 participants")
ok(R(120, 300) == R(12, 30) == R(2, 5) and irreductible(R(2, 5)), "2/5 des participants")
ok(R(3, 2) == R(6, 4) and R(5, 4) < R(3, 2) <= 2, "R et P")
ok(de(R(5, 4), 1000) == 1250 and 1000 / 4 == 250, "1 250 m")
ok(R(3, 4) == R(6, 8) < R(7, 8), "Inès en tête")
ok(de(R(3, 4), 2) == R(3, 2) == R(15, 10), "Hugo à 1,5 km = P")
ok(R(9, 8) > 1 and R(9, 8) == 1 + R(1, 8), "Tom : impossible")
ok(8 * R(5, 8) == 5 and de(R(5, 8), 100) == R(125, 2) and R(125, 2) == R(625, 10), "5/8 L = 62,5 cL")
ok(R(5, 8) == R(625, 1000) and R(5, 8) < 1, "5 ÷ 8 = 0,625 < 1")
ok(R(100, 8) == R(125, 10) and 5 * R(125, 10) == R(625, 10), "100 ÷ 8 = 12,5")

# ================================================================== fiche
ok(R(24, 36) == R(2, 3) and R(4, 9) == R(20, 45) and R(3, 5) == R(12, 20), "tableau de la fiche")
ok(R(12, 20) < R(13, 20) and R(1, 3) != R(2, 4) and R(1, 8) < R(1, 4), "fiche : comparaisons et erreurs")

# ================================================================== contrôle des textes
# Aucune mention du brevet (consigne du propriétaire), titres « Type - Sujet » attendus.
TYPES = ("Découverte - ", "Entraînement - ", "Problème - ", "Synthèse - ")
ex = (ICI / "exercices.txt").read_text(encoding="utf-8")
titres = re.findall(r"^=== (.+)$", ex, re.M)
ok(len(titres) == 10 and len(set(titres)) == 10, "10 titres uniques")
ok(all(t.startswith(TYPES) for t in titres), "types de titres")
ok([t.split(" - ")[0] for t in titres] == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 3 + ["Synthèse"],
   "progression 3 / 3 / 3 / 1")
for nom in ("cours_260.txt", "fiche_180.txt", "exercices.txt"):
    t = (ICI / nom).read_text(encoding="utf-8").lower()
    ok("brevet" not in t, f"pas de « brevet » dans {nom}")
ids = [int(x) for x in re.findall(r"^Id:\s*(\d+)", ex, re.M)]
retires = [int(m) for m in re.findall(r"^(\d+)", (ICI / "exercices_retires.txt").read_text(encoding="utf-8"), re.M)]
ok(len(ids) == 10 and not set(ids) & set(retires) and len(set(ids) | set(retires)) == 21, "10 gardés + 11 retirés = 21")

print(f"verif_265 : {n_ok} contrôles, tous justes.")
