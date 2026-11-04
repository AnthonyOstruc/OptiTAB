# -*- coding: utf-8 -*-
"""Vérification (sympy, valeurs exactes) de tous les calculs de la notion 252
« Puissances et notation scientifique » (4e) : cours, fiche, 21 exercices.

    python verif_252.py
"""
from math import floor, log10, pi as PI_F

from sympy import Integer, Rational as R, pi, N, floor as sfloor

OK = [0]
ERR = []


def chk(nom, a, b, tol=None):
    """a == b exactement (tol=None) ou |a - b| <= tol."""
    a, b = N(a, 30) if tol is not None else a, N(b, 30) if tol is not None else b
    bon = (a == b) if tol is None else abs(a - b) <= tol
    if bon:
        OK[0] += 1
    else:
        ERR.append(f"{nom} : {a} ≠ {b}")


def D(s):
    """Décimal écrit à la française « 3,45 » → Rational exact."""
    return R(s.replace(",", ".").replace(" ", ""))


def sci(x):
    """Notation scientifique (a, n) d'un rationnel positif, a exact."""
    x = R(x)
    n = floor(log10(float(x)))
    a = x / R(10) ** n
    if a >= 10:
        a, n = a / 10, n + 1
    if a < 1:
        a, n = a * 10, n - 1
    return a, n


def og(x):
    """Ordre de grandeur (convention du cours : a < 5 → 10^n, sinon 10^(n+1))."""
    a, n = sci(x)
    return n if a < 5 else n + 1


def og_sans_ambiguite(x):
    """Vrai si le choix est le même avec les conventions « a < 5 », « a < 5,5 » (plus proche) et « a < √10 »."""
    a, n = sci(x)
    return float(a) < 10 ** 0.5 or float(a) >= 5.5


P = lambda n: R(10) ** n  # puissance de 10 exacte

# =============================================================== COURS
chk("cours 2^5", Integer(2) ** 5, 32)
chk("cours (-3)^2", Integer(-3) ** 2, 9)
chk("cours (-2)^3", Integer(-2) ** 3, -8)
chk("cours 0,1^3", D("0,1") ** 3, D("0,001"))
chk("cours (-2)^4", Integer(-2) ** 4, 16)
chk("cours (-2)^5", Integer(-2) ** 5, -32)
chk("cours -3^2", -(Integer(3) ** 2), -9)
chk("cours 5-2*3^2", 5 - 2 * Integer(3) ** 2, -13)
chk("cours 2^-3", Integer(2) ** -3, R(1, 8))
chk("cours 2^-3 déc", Integer(2) ** -3, D("0,125"))
chk("cours 5^-1", Integer(5) ** -1, D("0,2"))
chk("cours (-4)^-2", Integer(-4) ** -2, R(1, 16))
chk("cours 2^3*2^4", Integer(2) ** 3 * Integer(2) ** 4, Integer(2) ** 7)
chk("cours 10^9", P(9), 1000000000)
chk("cours 10^-6", P(-6), D("0,000001"))
chk("cours 10^-9", P(-9), D("0,000000001"))
chk("cours 5,8e3", D("5,8") * P(3), 5800)
chk("cours 5,8e-2", D("5,8") * P(-2), D("0,058"))
chk("cours règle 10^5*10^-8", P(5) * P(-8), P(-3))
chk("cours règle 10^2/10^-4", P(2) / P(-4), P(6))
chk("cours règle (10^3)^2", P(3) ** 2, P(6))
chk("cours règle 1/10^4", 1 / P(4), P(-4))
chk("cours 10^2*10^3", P(2) * P(3), P(5))
chk("cours 10^5/10^2", P(5) / P(2), P(3))
chk("cours B", P(4) * P(-7) / P(-5), P(2))
chk("cours 10^3*10^4", P(3) * P(4), P(7))
chk("cours 10^5/10^-2", P(5) / P(-2), P(7))
chk("cours 10^3+10^2", P(3) + P(2), 1100)
chk("cours 45 µm", 45 * P(-6), D("4,5") * P(-5))
chk("cours 45000", sci(45000), (D("4,5"), 4))
chk("cours 0,00072", sci(D("0,00072")), (D("7,2"), -4))
chk("cours 32e4", sci(32 * P(4)), (D("3,2"), 5))
chk("cours 0,8e3", sci(D("0,8") * P(3)), (8, 2))
chk("cours comparer 1", D("9,8") * P(4) < D("3,1") * P(5), True)
chk("cours comparer 2", D("2,7") * P(-3) < D("6,5") * P(-3), True)
chk("cours produit", 4 * P(3) * 5 * P(-7), 2 * P(-3))
chk("cours quotient", D("1,2") * P(8) / (4 * P(-2)), 3 * P(9))
chk("cours somme", 2 * P(3) + 5 * P(2), D("2,5") * P(3))
chk("cours og tour Eiffel", og(300), 2)
chk("cours og globule", og(7 * P(-6)), -5)
chk("cours og Terre", og(D("1,3") * P(7)), 7)
for x in (300, 7 * P(-6), D("1,3") * P(7)):
    chk(f"cours og sans ambiguïté {x}", og_sans_ambiguite(x), True)
chk("cours cellule/humain", P(0) / P(-5), P(5))
chk("cours contrôle estimation", 4 * 3 * P(-2), D("0,12"))
chk("cours contrôle exact", D("4,1") * P(3) * D("2,9") * P(-5), D("0,1189"))
# objets de l'échelle du cours (ordre de grandeur annoncé, taille réelle approchée)
for nom, taille, n in [("atome", D("1") * P(-10), -10), ("virus", 1 * P(-7), -7), ("cellule", 2 * P(-5), -5),
                       ("fourmi", 2 * P(-3), -3), ("humain", D("1,7"), 0), ("tour Eiffel", 330, 2),
                       ("Terre", D("1,2742") * P(7), 7), ("Terre-Soleil", D("1,5") * P(11), 11),
                       ("année-lumière", D("9,46") * P(15), 16), ("Voie lactée", D("9,5") * P(20), 21)]:
    chk(f"échelle cours {nom}", og(taille), n)

# =============================================================== FICHE
chk("fiche 45µm", 45 * P(-6), D("4,5") * P(-5))
chk("fiche 3,2 GHz", D("3,2") * P(9), 3200000000)
chk("fiche 7e-6 og", og(7 * P(-6)), -5)

# =============================================================== 2527
chk("2527 Q1", Integer(2) ** 5, 32)
chk("2527 Q2 3^4", Integer(3) ** 4, 81)
chk("2527 Q2 5^3", Integer(5) ** 3, 125)
chk("2527 Q2 2^3<3^2", Integer(2) ** 3 < Integer(3) ** 2, True)
chk("2527 Q3", (Integer(-2) ** 3, Integer(-2) ** 4), (-8, 16))
chk("2527 Q4", (-(Integer(3) ** 2), Integer(-3) ** 2), (-9, 9))
chk("2527 Q5", (Integer(7) ** 1, Integer(7) ** 0, Integer(1) ** 100, Integer(0) ** 7), (7, 1, 1, 0))
chk("2527 Q6", (Integer(2) ** -1, Integer(2) ** -3, P(-2)), (D("0,5"), D("0,125"), D("0,01")))

# =============================================================== 2528
e = D("0,1")
chk("2528 Q1", (Integer(2) ** 3, 2 ** 3 * e), (8, D("0,8")))
chk("2528 Q2", (Integer(2) ** 7, 2 ** 7 * e), (128, D("12,8")))
chk("2528 Q3", (Integer(2) ** 10, 2 ** 10 * e), (1024, D("102,4")))
n = next(k for k in range(1, 40) if e * 2 ** k > 1000)
chk("2528 Q5 n", n, 14)
chk("2528 Q5 2^13", Integer(2) ** 13, 8192)
chk("2528 Q5 2^14", Integer(2) ** 14, 16384)
chk("2528 Q5 épaisseur", e * 2 ** 14, D("1638,4"))
chk("2528 Q6 2^42", Integer(2) ** 42, 4398046511104)
chk("2528 Q6 ≈4,4e12", abs(Integer(2) ** 42 - D("4,4") * P(12)) < D("0,01") * P(12), True)
chk("2528 Q6 m", D("4,4") * P(12) * P(-4), D("4,4") * P(8))
chk("2528 Q6 km", D("4,4") * P(8) / P(3), 440000)
chk("2528 Q6 > Lune", 440000 > 384000, True)

# =============================================================== 2529
chk("2529 Q1", (P(3), P(6), P(1), P(0)), (1000, 1000000, 10, 1))
chk("2529 Q2", (P(-1), P(-2), P(-3)), (D("0,1"), D("0,01"), D("0,001")))
chk("2529 Q3", (100000, D("0,00001")), (P(5), P(-5)))
chk("2529 Q4", P(4) * P(3), P(7))
chk("2529 Q5", (P(5) / P(2), P(2) / P(5)), (P(3), P(-3)))
chk("2529 Q6", (P(2) ** 3, P(-3) * P(5)), (P(6), P(2)))

# =============================================================== 2530
chk("2530 Q1", D("3,45") * P(2), 345)
chk("2530 Q2", D("3,45") * P(-2), D("0,0345"))
chk("2530 Q3", 72 * P(-3), D("0,072"))
chk("2530 Q4", D("0,6") * P(4), 6000)
chk("2530 Q5", D("4,7") * P(4), 47000)
chk("2530 Q6", D("2,5") * P(-4), D("0,00025"))

# =============================================================== 2531
for x, ok in [(D("3,2"), True), (32, False), (D("0,8"), False), (1, True), (10, False)]:
    chk(f"2531 Q1 {x}", 1 <= x < 10, ok)
chk("2531 Q1 10e2", 10 * P(2), 1 * P(3))
chk("2531 Q2", sci(45000), (D("4,5"), 4))
chk("2531 Q3", sci(D("0,00072")), (D("7,2"), -4))
chk("2531 Q4", sci(32 * P(4)), (D("3,2"), 5))
chk("2531 Q5", sci(D("0,8") * P(3)), (8, 2))
chk("2531 Q6", sci(D("0,056") * P(-3)), (D("5,6"), -5))
chk("2531 Q6 déc", D("0,056") * P(-3), D("0,000056"))

# =============================================================== 2532
chk("2532 Q1", (P(6 + 3), P(6 - 3), P(0 - 3), P(-3 - 3)), (P(9), P(3), P(-3), P(-6)))
chk("2532 Q2", P(3) / P(-3), P(6))
chk("2532 Q3", 5 * P(9), 5000000000)
chk("2532 Q4", sci(12 * P(6)), (D("1,2"), 7))
chk("2532 Q5", sci(80 * P(-9)), (8, -8))
chk("2532 Q6", P(-3) / (8 * P(-8)), 12500)
chk("2532 Q6 0,125e5", D("0,125") * P(5), 12500)

# =============================================================== 2533
chk("2533 Q1", 3 * P(4) * 2 * P(5), 6 * P(9))
chk("2533 Q2", 4 * P(3) * 5 * P(-7), 2 * P(-3))
chk("2533 Q3", 9 * P(8) / (3 * P(2)), 3 * P(6))
chk("2533 Q4", D("1,2") * P(-3) / (4 * P(5)), 3 * P(-9))
chk("2533 Q5", D("3,1") * P(5) > D("9,8") * P(4), True)
chk("2533 Q5 déc", (D("3,1") * P(5), D("9,8") * P(4)), (310000, 98000))
chk("2533 Q6", sorted([2 * P(-3), 5 * P(-4), D("1,5") * P(-3)]), [5 * P(-4), D("1,5") * P(-3), 2 * P(-3)])

# =============================================================== 2534
chk("2534 A", P(5) * P(-8), P(-3))
chk("2534 B", P(4) / P(-3), P(7))
chk("2534 C", P(6) * P(-2) / P(-5), P(9))
chk("2534 D", P(-2) ** 3 * P(4), P(-2))
chk("2534 D déc", P(-2), D("0,01"))
E = 3 * P(5) * 8 * P(-2) / (6 * P(-4))
chk("2534 E", E, 4 * P(7))
chk("2534 E déc", E, 40000000)
F = D("1,5") * P(-3) * 4 * P(8) / (D("2,5") * P(2))
chk("2534 F", F, D("2,4") * P(3))
chk("2534 F num", D("1,5") * P(-3) * 4 * P(8), 600000)
chk("2534 F déc", F, 2400)

# =============================================================== 2535
c = 3 * P(5)
L, S, Ne, an = D("3,84") * P(5), D("1,5") * P(8), D("4,5") * P(9), D("3,15") * P(7)
chk("2535 Q1", L < S < Ne, True)
chk("2535 Q2", Ne / S, 30)
chk("2535 Q3", S / c, 500)
chk("2535 Q3 min", divmod(500, 60), (8, 20))
chk("2535 Q4", L / c, D("1,28"))
chk("2535 Q5", Ne / c, 15000)
chk("2535 Q5 h", divmod(15000, 3600), (4, 600))
chk("2535 Q6", c * an, D("9,45") * P(12))

# =============================================================== 2536
at, vi, gl, ch = P(-10), D("1,2") * P(-7), 7 * P(-6), 80 * P(-6)
chk("2536 Q1", (sci(gl), sci(ch)), ((7, -6), (8, -5)))
chk("2536 Q2", vi * P(9), 120)
chk("2536 Q3", at < vi < gl < ch, True)
chk("2536 Q4", gl / vi, R(175, 3), )
chk("2536 Q4 ≈58,3", gl / vi, D("58.33"), tol=D("0.01"))
chk("2536 Q5", ch / gl, R(80, 7))
chk("2536 Q5 ≈11,4", ch / gl, D("11.43"), tol=D("0.01"))
chk("2536 Q6", ch / at, 8 * P(5))

# =============================================================== 2537
chk("2537 A", Integer(-3) ** 4, 81)
chk("2537 B", -(Integer(3) ** 4), -81)
chk("2537 C", Integer(-1) ** 15 + Integer(-1) ** 20, 0)
chk("2537 D", 3 * Integer(2) ** 3 - Integer(4) ** 2, 8)
chk("2537 D faux", (3 * 2) ** 3, 216)
chk("2537 E", (5 - Integer(7)) ** 3 * P(2), -800)
chk("2537 F", Integer(2) ** -2 + Integer(4) ** -1, D("0,5"))
chk("2537 G", Integer(-2) ** -3, R(-1, 8))
chk("2537 G déc", Integer(-2) ** -3, D("-0,125"))

# =============================================================== 2538
photo, carte = 4 * P(6), 64 * P(9)
chk("2538 Q1", sci(photo), (4, 6))
chk("2538 Q2", sci(carte), (D("6,4"), 10))
chk("2538 Q3", carte / photo, 16000)
chk("2538 Q4", sfloor(R(64) / D("1,5")), 42)
chk("2538 Q4 ≈42,67", R(64) / D("1,5"), D("42.67"), tol=D("0.005"))
chk("2538 Q5", 2 * P(12) / carte, D("31,25"))
chk("2538 Q5 cartes", sfloor(2 * P(12) / carte) + 1, 32)
chk("2538 Q6", 2 * P(12) / (5 * P(5)), 4 * P(6))

# =============================================================== 2539
fr_p, fr_s = D("6,8") * P(7), D("5,5") * P(5)
in_p, in_s = D("1,44") * P(9), D("3,29") * P(6)
mo_p, mo_s = D("8,1") * P(9), D("1,49") * P(8)
chk("2539 Q1", round(float(mo_p / fr_p)), 119)
chk("2539 Q1 ≈1,191e2", mo_p / fr_p, D("119.1"), tol=D("0.05"))
chk("2539 Q2", round(float(fr_p / fr_s)), 124)
chk("2539 Q2 ≈1,236e2", fr_p / fr_s, D("123.6"), tol=D("0.05"))
chk("2539 Q3", round(float(mo_p / mo_s)), 54)
chk("2539 Q3 ≈5,436e1", mo_p / mo_s, D("54.36"), tol=D("0.005"))
chk("2539 Q4", round(float(in_p / in_s)), 438)
chk("2539 Q4 ≈0,4377e3", in_p / in_s, D("437.7"), tol=D("0.05"))
chk("2539 Q6", fr_p / fr_s * mo_s, D("1.842") * P(10), tol=D("0.0005") * P(10))
chk("2539 Q6 arrondi trop tôt", 100 * mo_s, D("1,49") * P(10))
chk("2539 Q6 écart ≈ 19 %", 1 - 100 * mo_s / (fr_p / fr_s * mo_s), D("0.19"), tol=D("0.01"))

# =============================================================== 2540
chk("2540 Q1", P(3) * P(4), P(7))
chk("2540 Q2", Integer(2) ** 3, 8)
chk("2540 Q3", D("3,5") * P(-2), D("0,035"))
chk("2540 Q4", sci(45000), (D("4,5"), 4))
chk("2540 Q5", Integer(-3) ** 2, 9)
chk("2540 Q6", P(-2), D("0,01"))
chk("2540 Q7", P(5) / P(-2), P(7))
chk("2540 Q7 vérif", 100000 * 100, P(7))

# =============================================================== 2541
v, d = 6 * P(4), 4 * P(13)
chk("2541 Q1", v * 24, D("1,44") * P(6))
chk("2541 Q2", v * 24 * 365, D("5,256") * P(8))
chk("2541 Q3", d / v, R(2, 3) * P(9))
chk("2541 Q3 ≈6,7e8", d / v, D("6.7") * P(8), tol=D("0.05") * P(8))
chk("2541 Q4", d / (v * 24 * 365), D("76103.5"), tol=D("0.1"))
chk("2541 Q4 vérif", d / v / 8760, D("76103.5"), tol=D("0.1"))
chk("2541 Q5", c * 3600, D("1,08") * P(9))
chk("2541 Q5 rapport", c * 3600 / v, 18000)
chk("2541 Q6 h", 50 * 8760, D("4,38") * P(5))
chk("2541 Q6", d / (50 * 8760), D("9.13") * P(7), tol=D("0.005") * P(7))
chk("2541 Q6 ≈1500 Voyager", d / (50 * 8760) / v, 1522, tol=1)

# =============================================================== 2542
objets = {"bactérie": (2 * P(-6), 2, -6, -6), "riz": (7 * P(-3), 7, -3, -2), "girafe": (D("5,8"), D("5,8"), 0, 1),
          "Everest": (8849, D("8,849"), 3, 4), "Jupiter": (139820 * P(3), D("1,3982"), 8, 8),
          "Soleil-Jupiter": (D("7,8") * P(8) * P(3), D("7,8"), 11, 12),
          "Andromède": (2 * P(18) * P(3), 2, 21, 21)}
for nom, (x, a, n, o) in objets.items():
    chk(f"2542 Q1 {nom}", sci(x), (a, n))
    chk(f"2542 Q2 {nom}", og(x), o)
    chk(f"2542 Q2 {nom} sans ambiguïté", og_sans_ambiguite(x), True)
chk("2542 riz plus proche de 10^-2", abs(7 * P(-3) - P(-2)) < abs(7 * P(-3) - P(-3)), True)
chk("2542 Q4 estimation", P(4) / P(1), P(3))
chk("2542 Q4 exact", R(8849) / D("5,8"), 1526, tol=D("0.5"))
chk("2542 Q4 og exact", og(R(8849) / D("5,8")), 3)
chk("2542 Q5 estimation", P(12) / P(8), P(4))
q5 = D("7,8") * P(11) / (D("1,3982") * P(8))
chk("2542 Q5 exact", q5, D("5578.6"), tol=D("0.1"))
chk("2542 Q5 ≈5,58e3", q5, D("5.58") * P(3), tol=D("0.005") * P(3))
chk("2542 Q5 og", og(q5), 4)
chk("2542 Q5 sans ambiguïté", og_sans_ambiguite(q5), True)
chk("2542 Q6", 2 * P(21) / (2 * P(-6)), P(27))

# =============================================================== 2543
goutte = 5 * P(-2) * P(-3)
m = 3 * P(-26)
chk("2543 Q1", goutte, 5 * P(-5))
nb = goutte / m
chk("2543 Q2", nb, R(5, 3) * P(21))
chk("2543 Q2 ≈1,67e21", nb, D("1.67") * P(21), tol=D("0.005") * P(21))
chk("2543 Q3", D("1,67") * P(21) / (8 * P(9)), D("2.09") * P(11), tol=D("0.005") * P(11))
chk("2543 Q3 exact", nb / (8 * P(9)), D("2.08") * P(11), tol=D("0.01") * P(11))
q4 = D("1,67") * P(21) / (D("3,15") * P(7))
chk("2543 Q4", q4, D("5.3") * P(13), tol=D("0.05") * P(13))
chk("2543 Q4 exact", nb / (D("3,15") * P(7)), D("5.3") * P(13), tol=D("0.05") * P(13))
chk("2543 Q5", D("5,3") * P(13) / (D("1,38") * P(10)), D("3.8") * P(3), tol=D("0.05") * P(3))
chk("2543 Q6", D("0,25") / m, D("8.33") * P(24), tol=D("0.005") * P(24))
chk("2543 Q6 gouttes", 250 / D("0,05"), 5000)
chk("2543 Q6 vérif", 5000 * D("1,67") * P(21), D("8.35") * P(24))

# =============================================================== 2544
px = 3840 * 2160
chk("2544 Q1", px, 8294400)
chk("2544 Q1 ≈8,3e6", px, D("8.3") * P(6), tol=D("0.05") * P(6))
chk("2544 Q2", px * 3, 24883200)
chk("2544 Q2 ≈2,5e7", px * 3, D("2.5") * P(7), tol=D("0.05") * P(7))
chk("2544 Q3", px * 3 * 60, 1492992000)
chk("2544 Q3 ≈1,5e9", px * 3 * 60, D("1.5") * P(9), tol=D("0.05") * P(9))
chk("2544 Q4", D("1,5") * P(9) * D("3,6") * P(3), D("5,4") * P(12))
chk("2544 Q4 exact ≈5,4 To", px * 3 * 60 * 3600, D("5.4") * P(12), tol=D("0.05") * P(12))
chk("2544 Q5", D("5,4") * P(12) / P(3), D("5,4") * P(9))
chk("2544 Q6", D("5,4") * P(9) / (D("6,25") * P(6)), 864)
chk("2544 Q6 min", divmod(864, 60), (14, 24))

# =============================================================== 2545
V = 3000 * 50 * 2
chk("2545 Q1", V, 3 * P(5))
chk("2545 Q2", P(-3) ** 3, P(-9))
chk("2545 Q3", V / P(-9), 3 * P(14))
chk("2545 Q4", D("0,6") * 3 * P(14), D("1,8") * P(14))
chk("2545 Q5", D("1,8") * P(14) / (2 * P(11)), 900)
chk("2545 Q6 s", D("1,8") * P(14) / 10, D("1,8") * P(13))
q6 = D("1,8") * P(13) / (D("3,15") * P(7))
chk("2545 Q6 ans", q6, D("5.71") * P(5), tol=D("0.005") * P(5))
chk("2545 Q6 og", og(q6), 6)
chk("2545 Q6 sans ambiguïté", og_sans_ambiguite(q6), True)

# =============================================================== 2546
OS = D("6,4") * P(3) + D("3,6") * P(4)
chk("2546 Q1", OS, D("4,24") * P(4))
orb = 2 * pi * OS
chk("2546 Q2", orb, 266407, tol=1)
chk("2546 Q2 arrondi", round(float(N(orb)) / 1000) * 1000, 266000)
vit = R(266000) / 24
chk("2546 Q3", vit, D("11083.33"), tol=D("0.01"))
chk("2546 Q3 ≈1,11e4", vit, D("1.11") * P(4), tol=D("0.005") * P(4))
chk("2546 Q4", vit * 1000 / 3600, D("3078.7"), tol=D("0.1"))
chk("2546 Q4 calc", D("1,108") * P(7) / (D("3,6") * P(3)), D("3077.8"), tol=D("0.1"))
chk("2546 Q4 centaine", round(float(vit * 1000 / 3600), -2), 3100)
chk("2546 Q5", 2 * D("3,6") * P(4) / c, D("0,24"))
chk("2546 Q6", 2 * D("0,24"), D("0,48"))
chk("2546 faux", (D("6,4") + D("3,6")) * P(4) != OS, True)

# =============================================================== 2547
Pk = D("1,3") * P(9) / P(3)
chk("2547 Q1", Pk, D("1,3") * P(6))
En = Pk * 8760
chk("2547 Q2", En, D("1,1388") * P(10))
chk("2547 Q3", En / (D("4,5") * P(3)), D("2.53") * P(6), tol=D("0.005") * P(6))
chk("2547 Q4", D("4,5") * P(11) / En, D("39.5"), tol=D("0.05"))
chk("2547 Q5 h", 5 * 365, 1825)
chk("2547 Q5", 8 * P(-3) * 1825, D("14,6"))
chk("2547 Q5 Wh", 8 * 1825, 14600)
chk("2547 Q6", D("14,6") * D("0,25"), D("3,65"))

print(f"{OK[0]} contrôles justes, {len(ERR)} erreur(s)")
for e in ERR:
    print("  ✗", e)
raise SystemExit(1 if ERR else 0)
