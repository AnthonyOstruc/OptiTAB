# -*- coding: utf-8 -*-
"""Vérification des résultats de la notion 234 (puissances, racines, écriture scientifique, 3e)."""
from fractions import Fraction as F
from decimal import Decimal as D
from sympy import sqrt, Rational, Integer, nsimplify

ok = 0


def chk(c, msg):
    global ok
    assert c, msg
    ok += 1


def sci(x):
    """Notation scientifique exacte (mantisse Decimal, exposant)."""
    x = D(str(x))
    e = x.adjusted()
    return (x.scaleb(-e).normalize(), e)


# ---------- cours / fiche
chk(7 ** 4 == 2401 and F(2) ** -3 == F(1, 8), "cours puissances")
chk((-5) ** 2 == 25 and -5 ** 2 == -25 and (-2) ** 3 == -8 and (-2) ** 4 == 16, "signes")
chk(3 ** 4 * 3 ** 2 == 3 ** 6 and F(5 ** 7, 5 ** 3) == 5 ** 4 and (2 ** 3) ** 4 == 2 ** 12 and (2 * 5) ** 3 == 2 ** 3 * 5 ** 3, "règles")
chk(2 ** 3 + 2 ** 2 == 12 and 2 ** 5 == 32, "somme")
chk(sci(74000000) == (D("7.4"), 7) and sci("0.000056") == (D("5.6"), -5) and sci(3450) == (D("3.45"), 3), "notation sci")
chk(3 * 10 ** 5 * D("4E-2") == D("1.2E4"), "produit sci")
chk(D("0.5E4") == D("5E3"), "0,5e4")
chk(sqrt(49) == 7 and sqrt(Rational(81, 100)) == Rational(9, 10) and sqrt(Rational(9, 16)) == Rational(3, 4), "racines")
chk(abs(float(sqrt(45)) - 6.708) < 1e-3 and round(float(sqrt(45)), 2) == 6.71, "racine 45")
chk([n * n for n in range(1, 13)] == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144], "carrés parfaits")
chk(D("6.1") ** 2 == D("37.21") and 6 < float(sqrt(37)) < 6.1, "encadrer 37")
chk(sqrt(9 + 16) == 5 and sqrt(9) + sqrt(16) == 7 and sqrt((-4) ** 2) == 4, "pièges racines")
chk(sqrt(36 * 25) == 30, "pour aller plus loin")
# ordres de grandeur (cours) : virus ~1e-7, cellule ~1e-5, fourmi ~5e-3, humain ~1,7, tour Eiffel 330, Everest 8849, Terre 1,27e7
for v, n in [(1e-7, -7), (2e-5, -5), (3e-3, -3), (1.7, 0), (330, 2), (8849, 4), (1.2742e7, 7)]:
    plus_proche = min(range(-12, 12), key=lambda k: abs(v - 10.0 ** k))
    chk(plus_proche == n, "ordre %s" % v)

# ---------- 2118
chk(5 ** 3 == 125 and (-3) ** 4 == 81 and 9 ** 0 == 1 and F(10) ** -1 == F(1, 10) and F(5) ** -2 == F(1, 25), "2118")
# ---------- 2119
chk((-1) ** 10 == 1 and (-1) ** 15 == -1, "2119")
# ---------- 2120
chk(F(7) ** 5 * F(7) ** -2 == 7 ** 3 and (3 * 5) ** 2 == 225 == 9 * 25, "2120")
# ---------- 2121
chk(sci("0.000092") == (D("9.2"), -5) and sci("0.06") == (D("6"), -2) and 25 * 10 ** 3 == D("2.5E4"), "2121")
# ---------- 2122
chk(sqrt(144) == 12 and sqrt(Rational(81, 100)) == Rational(9, 10) and sqrt(Rational(49, 64)) == Rational(7, 8)
    and sqrt(225) == 15 and sqrt(1) == 1 and sqrt(0) == 0 and sqrt(10 ** 4) == 100, "2122")
chk(D("0.09") ** 2 == D("0.0081"), "2122 erreur")
# ---------- 2123
chk(D("0.0000001") == D("1E-7") and D("0.000001") == D("1E-6") and D("0.0001") == D("1E-4") and 100 == 10 ** 2, "2123 puissances")
chk(sci(400000) == (D("4"), 5) and F(10 ** 2) / F(10) ** -6 == 10 ** 8, "2123")
# ---------- 2124
chk(sqrt(5) ** 2 == 5 and sqrt(5 ** 2) == 5 and sqrt((-5) ** 2) == 5 and sqrt(16) + sqrt(9) == 7 and sqrt(25) == 5, "2124")
# ---------- 2186
chk(D("6E8") * D("4E-5") == D("2.4E4") == 24000, "2186 Q1-2")
chk(D("2E3") * D("3.5E4") == D("7E7") and D("5E-2") ** 2 == D("2.5E-3"), "2186 Q3-4")
# ---------- 2187
chk(D("8.4E-3") / D("2.1E5") == D("4E-8") and D("9E4") / D("3E-2") == D("3E6") and D("4E-8") == D("0.00000004"), "2187")
# ---------- 2188
r37, r90 = sqrt(37), sqrt(90)
chk(6 < r37 < 7 and D("6.05") ** 2 == D("36.6025") and float(r37) > 6.05 and round(float(r37), 1) == 6.1, "2188 racine 37")
chk(9 < r90 < 10 and D("9.4") ** 2 == D("88.36") and D("9.5") ** 2 == D("90.25"), "2188 racine 90 dixièmes")
chk(D("9.45") ** 2 == D("89.3025") and round(float(r90), 1) == 9.5, "2188 arrondi 90")
# ---------- 2128
chk(250 * D("1E-3") == D("2.5E-1") and 12 * D("1E-6") == D("1.2E-5") and 45 * D("1E-9") == D("4.5E-8"), "2128 Q1-3")
chk(64 * 10 ** 9 == D("6.4E10") and (64 * 10 ** 9) // (4 * 10 ** 6) == 16000, "2128 Q4-5")
# ---------- 2189
chk(sqrt(36 + 64) == 10 and sqrt(36) + sqrt(64) == 14, "2189 Q2")
chk(sqrt(4 * 9) == sqrt(4) * sqrt(9) == 6 and sqrt(16 * 25) == 20 == sqrt(16) * sqrt(25) and 30 ** 2 == 36 * 25, "2189")
# ---------- 2130
chk(2 ** 10 == 1024 and 3 ** 4 == 81 and 4 ** 3 == 64 == 2 ** 6 and (2 ** 2) ** 3 == 2 ** 6 and 5 ** 0 == 1 and 0 ** 5 == 0, "2130")
# ---------- 2131
chk(sqrt(169) == 13 and 4 * 13 == 52 and sqrt(7) ** 2 == 7 and D("1.5") ** 2 == D("2.25"), "2131 Q1-4")
chk(5 < sqrt(32) < 6 and D("5.6") ** 2 == D("31.36") and D("5.7") ** 2 == D("32.49") and D("5.65") ** 2 == D("31.9225")
    and round(float(sqrt(32)), 1) == 5.7, "2131 Q5")
# ---------- 2132
chk(120 // 20 == 6 and 800 * 2 ** 6 == 51200 and 800 * 2 ** 9 == 409600, "2132")
chk(800 * 2 ** 6 < 100000 < 800 * 2 ** 7 == 102400 and 7 * 20 == 140, "2132 Q4")
# ---------- 2133 (globules rouges)
n = 5 * D("5E12")
chk(n == D("2.5E13"), "2133 Q2")
L = n * D("7E-6")
chk(L == D("1.75E8") and L / 1000 == 175000 and D(175000) / 40000 == D("4.375"), "2133 Q3-5")
# ---------- 2190
chk(8 * 60 + 20 == 500 and D("3E5") * 500 == D("1.5E8") and D("1.5E8") * 1000 == D("1.5E11"), "2190 Q1-3")
chk(D("3E5") * D("1.28") == D("3.84E5") and D("3E5") * D("3.15E7") == D("9.45E12"), "2190 Q4-5")
# ---------- 2135
chk(round(float(sqrt(2)), 3) == 1.414 and D("1.4") ** 2 == D("1.96") and round(float(sqrt(8)), 2) == 2.83, "2135 Q1-4")
chk((2 * sqrt(2)) ** 2 == 8 and sqrt(8) == 2 * sqrt(2) and abs(4 * 1.414 - 5.656) < 1e-9 and round(5.656 ** 2) == 32, "2135 Q5")
# ---------- 2136
t = D("6.4E9") / D("8E6")
chk(t == 800 and divmod(800, 60) == (13, 20) and F(800, 600) == F(4, 3), "2136 Q1-3")
deb = D("6.4E9") / 600
chk(abs(deb - D("1.07E7")) < D("5E4"), "2136 Q4")
chk(D("8E6") * 3600 == D("2.88E10") and D("2.88E10") / D("1E9") == D("28.8"), "2136 Q5")
# ---------- 2137
chk(2 ** 10 == 1024 and D("0.1") * 1024 == D("102.4") and D("0.1") * 2 ** 20 == D("104857.6"), "2137 Q1-4")
chk(2 ** 21 < 3300000 < 2 ** 22 and min(k for k in range(60) if D("0.1") * 2 ** k > 330000) == 22, "2137 Q5")
chk(min(k for k in range(60) if D("0.1") * 2 ** k > 330) == 12, "2137 erreur fréquente")
# ---------- 2138
chk(5 ** 2 == 25 and 7 < sqrt(50) < 8 and D("7.1") ** 2 == D("50.41") and D("7.05") ** 2 == D("49.7025")
    and round(float(sqrt(50)), 1) == 7.1, "2138 Q1-3")
chk(5 ** 2 + 5 ** 2 == 50 and 10 ** 2 // 25 == 4, "2138 Q4-5")

print("verif_234 :", ok, "contrôles, tout est juste.")
