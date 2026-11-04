# -*- coding: utf-8 -*-
"""Vérification de tous les résultats numériques de la notion « Suites numériques » (Première)."""
from fractions import Fraction as F
import math
import sympy as sp

n = sp.symbols("n", integer=True, nonnegative=True)
ok = 0


def eq(a, b, msg, tol=None):
    global ok
    if tol is None:
        assert a == b, f"{msg}: {a} != {b}"
    else:
        assert abs(a - b) < tol, f"{msg}: {a} != {b}"
    ok += 1


def rec(u0, f, k):
    L = [u0]
    for _ in range(k):
        L.append(f(L[-1]))
    return L


def premier(cond, start=0):
    k = start
    while not cond(k):
        k += 1
    return k


# ---------------------------------------------------------------- cours
eq(9 - 12, -3, "cours u3")
eq(rec(2, lambda v: 3 * v - 1, 2), [2, 5, 14], "cours v")
eq(sp.expand((n + 1) ** 2 - 4 * (n + 1) - (n ** 2 - 4 * n)), 2 * n - 3, "cours diff")
eq([k * k - 4 * k for k in range(7)], [0, -3, -4, -3, 0, 5, 12], "nuage cours")
eq(sp.expand(5 - 2 * (n + 1) - (5 - 2 * n)), -2, "cours arith ex")
eq(sum(range(1, 101)), 5050, "gauss 100")
eq(round(1000 * 1.03 ** 10, 2), 1343.92, "capital 10 ans")
eq(sum(2 ** k for k in range(10)), 1023, "somme 2^k")
eq(premier(lambda k: 1000 * 1.03 ** k >= 2000), 24, "seuil 2000")
eq((round(1000 * 1.03 ** 23, 2), round(1000 * 1.03 ** 24, 2)), (1973.59, 2032.79), "encadrement seuil")
eq(rec(F(1), lambda u: u / 2 + 2, 3), [1, F(5, 2), F(13, 4), F(29, 8)], "escalier cours")

# ---------------------------------------------------------------- 1354
eq(rec(10, lambda u: u - 3, 3), [10, 7, 4, 1], "1354 u")
eq(rec(2, lambda v: 4 * v, 3), [2, 8, 32, 128], "1354 v")
w = [F(k + 1, k + 2) for k in range(3)]
eq((w[1] - w[0], w[2] - w[1], w[1] / w[0], w[2] / w[1]), (F(1, 6), F(1, 12), F(4, 3), F(9, 8)), "1354 w")
eq(rec(1, lambda u: 2 * u + 1, 5)[1:], [3, 7, 15, 31, 63], "1354 programme")

# ---------------------------------------------------------------- 1353
u = lambda m: m ** 2 + 1
eq([u(0), u(1), u(2)], [1, 2, 5], "1353 u")
eq(sp.expand(u(n + 1)), n ** 2 + 2 * n + 2, "1353 u_{n+1}")
eq(sp.expand(u(2 * n)), 4 * n ** 2 + 1, "1353 u_2n")
eq(sp.expand(4 * (n + 1) - 7 - (4 * n - 7)), 4, "1353 v")
eq(sp.simplify(5 * 2 ** (n + 2) / (5 * 2 ** (n + 1))), 2, "1353 w")

# ---------------------------------------------------------------- 1346
eq(rec(2, lambda u: 3 * u - 1, 3), [2, 5, 14, 41], "1346 u")
eq(rec(1, lambda u: 2 * u + 3, 3), [1, 5, 13, 29], "1346 v")
eq(rec(F(5), lambda u: u / 2 + 1, 3), [5, F(7, 2), F(11, 4), F(19, 8)], "1346 w")
eq(rec(3, lambda u: u * u - 2, 2), [3, 7, 47], "1346 t")
fib = [1, 1]
while len(fib) < 6:
    fib.append(fib[-1] + fib[-2])
eq(fib, [1, 1, 2, 3, 5, 8], "1346 fib")

# ---------------------------------------------------------------- 1342 / 1343
eq((5 + 30, -2 + 14 * 4, 12 - 16, -44), (35, 54, -4, 10 + 18 * (-3)), "1342")
eq(((15 - 7) / 4, 7 - 3 * 2), (2, 1), "1342 Q4")
eq((2 * 3 ** 5, F(5, 64), 4 * 2 ** 5, 3 * 2 ** 5, (-2) ** 4, (-2) ** 5), (486, 5 * F(1, 2) ** 6, 128, 96, 16, -32), "1343")

# ---------------------------------------------------------------- 1351 DS 1
uA = lambda m: m * m - 6 * m + 5
eq([uA(k) for k in range(5)], [5, 0, -3, -4, -3], "DS1 A1")
eq(sp.expand(uA(n + 1) - uA(n)), 2 * n - 5, "DS1 A2")
eq(all(uA(k + 1) < uA(k) for k in range(3)) and all(uA(k + 1) > uA(k) for k in range(3, 50)), True, "DS1 A3")
eq((2 * 0.8, 2 * 0.8 ** 2), (1.6, 1.2800000000000002), "DS1 B1")
eq(round(2 + 2 * sum(2 * 0.8 ** k for k in range(1, 6)), 2), 12.76, "DS1 B4")
eq(round(1.6 * (1 - 0.8 ** 5) / 0.2, 5), 5.37856, "DS1 somme")
eq(premier(lambda k: 2 * 0.8 ** k < 0.1), 14, "DS1 C2")

# ---------------------------------------------------------------- 1352 DS 2
a = lambda m: 2 * m + 18
eq((a(1), a(25), premier(lambda m: a(m) == 50, 1), sum(a(m) for m in range(1, 26))), (20, 68, 16, 1100), "DS2 A")
p = lambda m: 50000 * 0.98 ** m
eq((round(p(1)), round(p(2))), (49000, 48020), "DS2 B1")
eq([round(p(m)) for m in (10, 11, 12, 13, 14)], [40854, 40037, 39236, 38451, 37682], "DS2 tableau")
eq(premier(lambda m: p(m) < 40000), 12, "DS2 B3")
eq(premier(lambda m: 30000 + 600 * m > p(m)), 14, "DS2 C2")

# ---------------------------------------------------------------- 1364 DS 3
C = rec(200, lambda c: 1.02 * c + 50, 16)
eq([round(c, 4) for c in C[:4]], [200, 254, 309.08, 365.2616], "DS3 A2")
eq([round(C[k], 2) for k in (12, 13, 14)], [924.25, 992.74, 1062.59], "DS3 tableau")
eq(premier(lambda k: C[k] >= 1000), 14, "DS3 B2")
eq(premier(lambda k: 200 + 50 * k >= 1000), 16, "DS3 C2")
eq((round(254 / 200, 3), round(309.08 / 254, 3)), (1.27, 1.217), "DS3 quotients")

# ---------------------------------------------------------------- 1425
U = rec(F(3, 2), lambda x: 2 * x - 1, 11)
eq(U[:5], [F(3, 2), 2, 3, 5, 9], "1425 termes")
eq(all(U[k] == 1 + F(1, 2) * 2 ** k for k in range(12)), True, "1425 explicite")
eq(premier(lambda k: 1 + F(1, 2) * 2 ** k > 1000), 11, "1425 seuil")
eq((U[10], U[11]), (513, 1025), "1425 u10 u11")

# ---------------------------------------------------------------- 1424
U = rec(F(1), lambda x: x / 2 + 1, 10)
eq(U[:4], [1, F(3, 2), F(7, 4), F(15, 8)], "1424 termes")
eq(all(U[k] == 2 - F(1, 2) ** k for k in range(11)), True, "1424 explicite")
eq(2 - U[10], F(1, 1024), "1424 écart")

# ---------------------------------------------------------------- 1355
eq((F(1, 10), F(1, 100), F(1, 1000)), (F(1, 9 + 1), F(1, 99 + 1), F(1, 999 + 1)), "1355 u")
eq(premier(lambda k: 3 * k - 5 > 1000), 336, "1355 v")
eq((2 * F(1, 3) ** 5, 2 * F(1, 3) ** 10), (F(2, 243), F(2, 59049)), "1355 w")
eq([round((2 * k + 1) / (k + 3), 3) for k in (10, 100, 1000)], [1.615, 1.951, 1.995], "1355 t")
eq(sp.simplify(2 - 5 / (n + 3) - (2 * n + 1) / (n + 3)), 0, "1355 t forme")
eq(premier(lambda k: 3 ** k > 10 ** 6), 13, "1355 b")

# ---------------------------------------------------------------- 1348
eq(sp.simplify(1 / (n + 2) - 1 / (n + 1) + 1 / ((n + 1) * (n + 2))), 0, "1348 t")

# ---------------------------------------------------------------- sommes 1356 / 1344 / 1345
eq((sum(range(1, 21)), sum(5 + 3 * k for k in range(11)), sum(2 ** k for k in range(6)),
    sum(3 * 2 ** k for k in range(6)), sum(F(1, 2) ** k for k in range(5))), (210, 220, 63, 189, F(31, 16)), "1356")
eq((sum(range(1, 101)), sum(3 + 5 * k for k in range(11)), sum(range(2, 51, 3)), len(range(2, 51, 3)),
    sum(10 - 2 * k for k in range(16)), sum(-7 + 4 * k for k in range(30))), (5050, 308, 442, 17, -80, 1530), "1344")
eq((sum(2 ** k for k in range(6)), sum(3 ** k for k in range(6)), sum(4 * F(1, 2) ** k for k in range(5)),
    sum(5 * 3 ** k for k in range(8)), 11 * 100), (63, 364, F(31, 4), 16400, 1100), "1345")

# ---------------------------------------------------------------- 1347
U = rec(100.0, lambda x: 0.8 * x + 40, 15)
eq([round(x, 3) for x in U[:4]], [100, 120, 136, 148.8], "1347 termes")
eq([round(U[k], 1) for k in (5, 10, 15)], [167.2, 189.3, 196.5], "1347 tableau")
eq((round(U[10], 2), round(U[11], 2)), (189.26, 191.41), "1347 seuil")
eq(premier(lambda k: U[k] >= 190), 11, "1347 seuil 190")
eq(math.factorial(10), 3628800, "1347 fact")

# ---------------------------------------------------------------- 1349
U = rec(F(2), lambda x: x / 3 + 4, 12)
eq(U[1:4], [F(14, 3), F(50, 9), F(158, 27)], "1349 termes")
eq((U[1] / U[0], U[2] / U[1]), (F(7, 3), F(25, 21)), "1349 quotients")
eq(all(U[k] == 6 - 4 * F(1, 3) ** k for k in range(13)), True, "1349 explicite")
eq(all(U[k + 1] - U[k] == F(8, 3) * F(1, 3) ** k for k in range(12)), True, "1349 variation")
eq(6 - U[10], F(4, 59049), "1349 écart")
eq(all(sum(U[:k + 1]) == 6 * k + 2 * F(1, 3) ** k for k in range(13)), True, "1349 somme")

# ---------------------------------------------------------------- 1350
U = rec(F(500), lambda x: F(3, 2) * x - 300, 6)
eq(U[:6], [500, 450, 375, F(525, 2), F(375, 4), F(-1275, 8)], "1350 termes")
eq(all(U[k] == 600 - 100 * F(3, 2) ** k for k in range(7)), True, "1350 explicite")
eq(premier(lambda k: 600 - 100 * 1.5 ** k <= 0), 5, "1350 épuisement")
eq((round(600 + 100 * 1.5 ** 11), round(600 + 100 * 1.5 ** 12)), (9250, 13575), "1350 u11 u12")
eq(premier(lambda k: 600 + 100 * 1.5 ** k > 10000), 12, "1350 seuil")

# ---------------------------------------------------------------- 1361
eq(rec(1, lambda v: 3 * v - 4, 3), [1, -1, -7, -25], "1361 v")
eq(all(rec(1, lambda v: 3 * v - 4, 10)[k] == 2 - 3 ** k for k in range(11)), True, "1361 explicite")
eq(premier(lambda k: 100 * 2 ** k > 10000), 7, "1361 seuil")

# ---------------------------------------------------------------- 1362
eq([round(24000 * 1.04 ** k) for k in range(7)], [24000, 24960, 25958, 26997, 28077, 29200, 30368], "1362 tableau")
eq(premier(lambda k: 24000 * 1.04 ** k > 24000 + 1000 * k, 1), 4, "1362 A2")
eq((sum(24000 + 1000 * k for k in range(10)), round(sum(24000 * 1.04 ** k for k in range(10)))), (285000, 288147), "1362 A3")
eq(premier(lambda k: 24000 * 1.04 ** k >= 40000), 14, "1362 B2")
eq((round(24000 * 1.04 ** 13), round(24000 * 1.04 ** 14)), (39962, 41560), "1362 encadrement")
eq(premier(lambda k: 24000 + 1000 * k >= 40000), 16, "1362 contrat A")

# ---------------------------------------------------------------- 1363
uu, S, tab = 1, 0, []
for i in range(6):
    S += uu
    tab.append((uu, S))
    uu = 2 * uu + 1
eq(tab, [(1, 1), (3, 4), (7, 11), (15, 26), (31, 57), (63, 120)], "1363 tableau")
eq(all(sum(2 ** (k + 1) - 1 for k in range(m + 1)) == 2 ** (m + 2) - m - 3 for m in range(20)), True, "1363 somme")

# ---------------------------------------------------------------- nouveau-1
eq([3 * k + 1 for k in (1, 2, 3, 50)], [4, 7, 10, 151], "allumettes")
eq(max(k for k in range(1, 3000) if 3 * k + 1 <= 2026), 675, "allumettes 2026")
eq([k * (k - 1) // 2 for k in (1, 2, 3, 30)], [0, 1, 3, 435], "poignées")
eq(all(math.comb(k, 2) == k * (k - 1) // 2 for k in range(1, 40)), True, "poignées = paires")

# ================================================================ finition 2026-11-02
# 1351 A2 : chaîne de calcul redécoupée pour le téléphone
eq(sp.expand((n + 1) ** 2 - 6 * (n + 1) + 5), n ** 2 - 4 * n, "1351 A2 u_{n+1}")
eq(sp.expand(n ** 2 - 4 * n - (n ** 2 - 6 * n + 5)), 2 * n - 5, "1351 A2 différence")
# 1361 question 1.2 réécrite : u_1 = 4, u_6 = 19
r_ = sp.solve(sp.Eq(4 + 5 * sp.Symbol("r"), 19))[0]
eq(r_, 3, "1361 1.2 raison")
eq(4 + 19 * r_, 61, "1361 1.2 u20")
eq(sum(4 + (k - 1) * r_ for k in range(1, 21)), 650, "1361 1.2 somme")
eq(20 * sp.Rational(4 + 61, 2), 650, "1361 1.2 formule")

# valeurs écrites sur les figures ajoutées
eq(premier(lambda k: 1000 * 1.03 ** k > 2000), 24, "cours_seuil n = 24")
eq(round(1000 * 1.03 ** 24, 2), 2032.79, "cours_seuil u24")
eq(min((k * k - 6 * k + 5, k) for k in range(30)), (-4, 3), "ds1_nuage minimum u3 = -4")
h_ = [2 * F(4, 5) ** k for k in range(6)]
eq(round(float(2 + 2 * sum(h_[1:6])), 2), 12.76, "rebonds D")
eq(premier(lambda k: 50000 * 0.98 ** k < 40000), 12, "ds2 seuil p_n")
eq(premier(lambda k: 30000 + 600 * k > 50000 * 0.98 ** k), 14, "ds2 croisement")
eq((round(50000 * 0.98 ** 12), round(50000 * 0.98 ** 14), 30000 + 600 * 14), (39236, 37682, 38400), "ds2 points verts")
C_ = rec(200, lambda c: 1.02 * c + 50, 17)
eq(premier(lambda k: C_[k] >= 1000), 14, "ds3 C_n seuil")
eq(round(C_[14], 2), 1062.59, "ds3 C14")
eq(premier(lambda k: 200 + 50 * k >= 1000), 16, "ds3 D_n seuil")
eq(premier(lambda k: 100 * 2 ** k > 10000), 7, "te1 bactéries")
cl_ = rec(100, lambda u: 0.8 * u + 40, 15)
eq((premier(lambda k: cl_[k] >= 190), round(cl_[11], 2)), (11, 191.41), "club seuil 190")
eq(all(cl_[k] < 200 for k in range(16)), True, "club sous 200")
eq(round(600 - 100 * 1.5 ** 5, 2), -159.38, "équilibre u5 (départ 500)")
eq([round(600 + 100 * 1.5 ** k, 1) for k in (0, 6)], [700.0, 1739.1], "équilibre départ 700")
eq(all((2 * k + 1) / (k + 3) < 2 for k in range(15)), True, "comportements t_n < 2")
eq(min((k * k - 4 * k, k) for k in range(30)), (-4, 2), "variation_w minimum w2 = -4")
eq([1 + 2 * k for k in (0, 3, 7)], [1, 7, 15], "arith_t")
eq([(-2) ** k for k in (4, 5)], [16, -32], "alternance")
eq(2 - sum(F(1, 2 ** k) for k in range(5)), F(1, 16), "moitiés : il manque 1/16")
eq(3 * 4 + 1, 10 + 3, "allumettes motif 4 = 13")
eq((math.comb(4, 2), math.comb(5, 2)), (6, 10), "poignées p4 = 6, p5 = 10")

print(f"{ok} vérifications : tout est juste.")
