# -*- coding: utf-8 -*-
"""Vérification des résultats de la notion 243 (3e, probabilités) : python verif_243.py"""
from fractions import Fraction as F
from itertools import product
from sympy import symbols, solve, Eq, Rational

ok = 0


def v(nom, a, b):
    global ok
    assert a == b, (nom, a, b)
    ok += 1


D = range(1, 7)
# cours / fiche
v("cours rouge", F(5, 10), F(1, 2)); v("cours verte", F(2, 10), F(1, 5)); v("bleue ou verte", F(3, 10) + F(2, 10), F(1, 2))
v("somme7", F(sum(a + b == 7 for a, b in product(D, D)), 36), F(1, 6))
v("RR avec", F(3, 5) ** 2, F(9, 25)); v("diff avec", 2 * F(3, 5) * F(2, 5), F(12, 25))
v("RR sans", F(3, 5) * F(2, 4), F(3, 10)); v("pique ou as", F(8 + 3, 32), F(11, 32))
# 2338
v("pair", F(3, 6), F(1, 2)); v("mult3", F(2, 6), F(1, 3)); v("premiers", F(len([n for n in D if n in (2, 3, 5)]), 6), F(1, 2)); v(">4", F(2, 6), F(1, 3))
# 2340
C12 = range(1, 13)
A = {n for n in C12 if n % 2 == 0}; B = {n for n in C12 if n % 5 == 0}; C = {n for n in C12 if n % 3 == 0}
v("PA", F(len(A), 12), F(1, 2)); v("PB", F(len(B), 12), F(1, 6)); v("PC", F(len(C), 12), F(1, 3))
v("A∩B", A & B, {10}); v("B∩C", B & C, set()); v("BouC", F(len(B | C), 12), F(1, 2))
# 2341
v("roue mult3", F(2, 8), F(1, 4)); v("roue ≤6", F(6, 8), F(3, 4)); v("angle", 360 // 8, 45)
# 2342
pcs = list(product("PF", repeat=2))
v("une F", F(sum(i.count("F") == 1 for i in pcs), 4), F(1, 2)); v("au moins F", F(sum("F" in i for i in pcs), 4), F(3, 4))
# 2344
v("coeur", F(8, 32), F(1, 4)); v("as", F(4, 32), F(1, 8)); v("figures", F(12, 32), F(3, 8)); v("rouge", F(16, 32), F(1, 2))
# 2345
v("s2", F(sum(a + b == 2 for a, b in product(D, D)), 36), F(1, 36)); v("s>=10", F(sum(a + b >= 10 for a, b in product(D, D)), 36), F(1, 6))
# 2346
v("BB avec", F(2, 5) ** 2, F(4, 25)); v("total avec", F(9, 25) + F(12, 25) + F(4, 25), 1)
# 2347 (simulation exhaustive sans remise)
sac = "RRRBB"
tir = [(sac[i], sac[j]) for i in range(5) for j in range(5) if i != j]
v("RR sans exh", F(sum(t == ("R", "R") for t in tir), 20), F(3, 10)); v("BB sans", F(sum(t == ("B", "B") for t in tir), 20), F(1, 10))
v("diff sans", F(sum(t[0] != t[1] for t in tir), 20), F(3, 5))
# 2348
v("aucun6", F(sum(6 not in (a, b) for a, b in product(D, D)), 36), F(25, 36)); v("au moins 6", F(11, 36), 1 - F(25, 36))
v("exactement un 6", F(sum((a == 6) != (b == 6) for a, b in product(D, D)), 36), F(5, 18))
# 2349
b, r = symbols("b r")
v("b", solve(Eq(Rational(6) / (6 + b), Rational(2, 5)), b), [9]); v("r", solve(Eq((6 + r) / (15 + r), Rational(1, 2)), r), [3])
# 2350
C4 = range(4)
v("codes diff", F(sum(a != b for a, b in product(C4, C4)), 16), F(3, 4)); v("somme3", F(sum(a + b == 3 for a, b in product(C4, C4)), 16), F(1, 4))
# 2351
v("as ou roi", F(8, 32), F(1, 4))
# 2352
v("Tom", F(sum(a * b % 2 == 1 for a, b in product(D, D)), 36), F(1, 4)); v("somme paire", F(sum((a + b) % 2 == 0 for a, b in product(D, D)), 36), F(1, 2))
# 2353
v("BB", F(2, 5) * F(4, 5), F(8, 25)); v("NN", F(3, 5) * F(1, 5), F(3, 25)); v(">=1B", 1 - F(3, 25), F(22, 25)); v("même", F(11, 25), F(8, 25) + F(3, 25))
# 2354
v("ecart1", round(abs(0.327 - 1 / 3), 3), 0.006); v("ecart2", round(abs(0.3354 - 1 / 3), 3), 0.002); v("600", 600 * F(1, 3), 200)
# 2355
v("lot", F(20, 200), F(1, 10)); v("livre/stylo", F(19, 200), F(19, 200)); v("1/4", 200 * F(1, 4), 50)
# 2356
v("poisson", 3 * F(1, 3) * F(1, 2), F(1, 2)); v("pas melon", 1 - F(1, 3), F(2, 3)); v("dessert", 6 * 4, 24)
# 2357
autre = (1 - F(1, 4)) / 5
v("autre", autre, F(3, 20)); v("pair truqué", 2 * autre + F(1, 4), F(11, 20)); v("total", 5 * autre + F(1, 4), 1); v("98/400", F(98, 400), F(49, 200))
# 2358
J, R = range(1, 4), range(1, 5)
v("kermesse 5", F(sum(a + b == 5 for a, b in product(J, R)), 12), F(1, 4)); v("kermesse 7", F(sum(a + b == 7 for a, b in product(J, R)), 12), F(1, 12))
v("46/200", F(46, 200), F(23, 100))
print(f"{ok} contrôles OK")
