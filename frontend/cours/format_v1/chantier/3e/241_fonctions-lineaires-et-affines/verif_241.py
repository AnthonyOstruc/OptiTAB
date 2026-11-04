# -*- coding: utf-8 -*-
"""Vérification sympy des résultats de la notion 241 (cours, fiche, 21 exercices)."""
from sympy import Rational as R, symbols, solve, expand, nsimplify

x = symbols("x")
n = 0


def ok(cond, msg):
    global n
    n += 1
    assert cond, msg


# cours / fiche
g = lambda t: 2 * t - 3
ok(g(0) == -3 and g(2) == 1, "cours g")
ok(R(11 - 5, 4 - 1) == 2 and 5 - 2 * 1 == 3, "cours deux points")
ok(R(21, 6) == R(7, 2), "cours linéaire")
ok(R(84) / R(12, 10) == 70, "cours pourcentage")
ok(solve(20 + 3 * x - (8 + 5 * x), x) == [6] and 20 + 18 == 38, "cours tarifs")
ok(R(12, 10) * R(85, 100) == R(102, 100), "fiche évolutions")
# 2297
f = lambda t: R(-5, 2) * t
ok(f(4) == -10 and f(-2) == 5 and solve(f(x) - 15, x) == [-6] and f(-4) == 10, "2297")
# 2298
g = lambda t: -3 * t + 8
ok([g(0), g(1), g(2)] == [8, 5, 2], "2298")
# 2299, 2300
ok(R(3, 2) * 2 == 3 and R(3, 2) * 4 == 6, "2299")
ok(solve(-x + 4, x) == [4] and -1 + 4 == 3, "2300")
# 2301
ok(R(19, 10) * 25 == R(95, 2) and R(19, 10) * 40 == 76 and R(57) / R(19, 10) == 30, "2301")
# 2303, 2304, 2305
ok(R(21, 6) * -2 == -7, "2303")
a = R(10 - 1, 5 - 2); b = 1 - a * 2
ok(a == 3 and b == -5 and a * 5 + b == 10 and solve(a * x + b, x) == [R(5, 3)], "2304")
a = R(26 - 14, 5 - 2); b = 14 - 2 * a
ok(a == 4 and b == 6 and 4 * 8 + 6 == 38, "2305")
# 2306
ok(-2 * 1 + 3 == 1 and solve(-2 * x + 3, x) == [R(3, 2)], "2306")
# 2307
ok(expand((4 * x + 6) - (4 * x - 1)) == 7, "2307")
# 2308
ok(R(12, 10) * 50 == 60 and R(85, 100) * 80 == 68 and R(84) / R(12, 10) == 70, "2308")
# 2309
ok(R(8 - 3, 2) == R(5, 2) and (R(155, 10) - 8) / 3 == R(5, 2), "2309 accroissements")
ok(R(5, 2) * 5 + 3 == R(155, 10) and R(5, 2) * 10 + 3 == 28, "2309")
# 2310
A = lambda t: 20 + 3 * t; B = lambda t: 8 + 5 * t
ok(A(4) == 32 and B(4) == 28 and A(10) == 50 and B(10) == 58 and expand(A(x) - B(x)) == 12 - 2 * x, "2310")
# 2311
V = lambda t: 900 - 35 * t
ok(V(10) == 550 and solve(V(x) - 200, x) == [20] and V(30) == -150, "2311")
t = R(900, 35)
ok(abs(float(t) - 25.714) < 1e-3 and round(float((t - 25) * 60)) == 43, "2311 vidange")
# 2312
k = R(20, 12)
ok(k == R(5, 3) and 18 * k == 30 and 20 * 30 == 600 and 216 * k ** 2 == 600 and 216 * 4 == 864, "2312")
ok(216 * k == 360, "2312 erreur")
# 2313
ok(2 + 5 == 7 and 3 * 2 + 1 == 7 and R(13 - 7, 4 - 2) == 3 and R(7, 2) == R(35, 10), "2313")
# 2314
A = lambda d: 45 + 12 * d; B = lambda d: 15 + 18 * d
ok(A(6) == 117 and B(6) == 123, "2314 a")
ok(max(d for d in range(30) if A(d) <= 120) == 6 and max(d for d in range(30) if B(d) <= 120) == 5, "2314 b")
ok([d for d in range(1, 30) if B(d) < A(d)] == [1, 2, 3, 4] and A(5) == B(5) == 105, "2314 c")
# 2315
ok(60 * R(7, 10) == 42 and R(315, 10) / R(7, 10) == 45 and R(8, 10) * R(7, 10) == R(56, 100), "2315")
# 2316
L = lambda h: 4 * h; P = lambda h: 2 * h + 10
ok(solve(L(x) - P(x), x) == [5] and L(5) == P(5) == 20, "2316 a")
ok(L(3) == 12 and P(3) == 16 and L(8) == 32 and P(8) == 26, "2316 b")
ok(max(h for h in range(30) if L(h) <= 22) == 5 and max(h for h in range(30) if P(h) <= 22) == 6 and L(6) == 24, "2316 c")

print(f"{n} contrôles : tout est juste.")
