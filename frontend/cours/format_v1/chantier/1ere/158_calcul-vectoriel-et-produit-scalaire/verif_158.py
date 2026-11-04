# -*- coding: utf-8 -*-
"""Vérification de tous les résultats de la notion 158 (produit scalaire, Première)."""
import math
import sympy as sp

N = 0


def ok(cond, msg):
    global N
    N += 1
    if not cond:
        raise SystemExit("FAUX : " + msg)


def eq(a, b, msg):
    ok(sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0, f"{msg} : {a} != {b}")


def V(a, b):
    return sp.Matrix([a, b])


def dot(u, v):
    return sp.expand(u[0] * v[0] + u[1] * v[1])


def norm(u):
    return sp.sqrt(dot(u, u))


def P(x, y):
    return sp.Matrix([x, y])


def vec(A, B):
    return B - A


def deg(c):
    return math.degrees(math.acos(float(c)))


def arr(x, n=1):
    return round(x + 1e-12, n)


cos = lambda d: sp.cos(sp.pi * sp.Rational(d, 180))

# ------------------------------------------------------------------ cours
eq(4 * 4 * cos(60), 8, "cours équilatéral")
eq(3 * 3, dot(V(3, 0), V(3, 3)), "cours carré AB.AC")
eq((36 - 9 - 16) / sp.Integer(2), sp.Rational(11, 2), "cours polarisation")
eq(dot(V(2, -1), V(3, 6)), 0, "cours orthogonaux")
u, v = V(1, 2), V(3, 1)
eq(dot(u, v) / (norm(u) * norm(v)), sp.sqrt(2) / 2, "cours angle 45")
eq(sp.sqrt(25 + 64 - 2 * 5 * 8 * cos(60)), 7, "cours Al-Kashi 7")
# Al-Kashi angle (cours) : côtés 7, 8, 13 -> angle 120° en face de 13
eq((49 + 64 - 169) / sp.Integer(2 * 7 * 8), -sp.Rational(1, 2), "cours angle 120")
# médiane : MA²+MB² = 2MI² + AB²/2, exemple MA=5, MB=7, AB=6
eq(sp.sqrt((25 + 49 - sp.Rational(36, 2)) / 2), sp.sqrt(28), "cours médiane")
# MA.MB = MI² - AB²/4 (symbolique)
x, y, a, b, c, d = sp.symbols("x y a b c d", real=True)
M, A, B = P(x, y), P(a, b), P(c, d)
I = (A + B) / 2
eq(dot(A - M, B - M), dot(I - M, I - M) - dot(B - A, B - A) / 4, "MA.MB = MI² - AB²/4")
eq(dot(A - M, A - M) + dot(B - M, B - M), 2 * dot(I - M, I - M) + dot(B - A, B - A) / 2, "médiane")
# exemple cours : AB = 6, MA.MB = 7 -> MI = 4
eq(sp.sqrt(7 + 9), 4, "cours MA.MB=7")

# ------------------------------------------------------------------ 1393
u, v, w = V(3, 4), V(2, -1), V(-2, 5)
eq(dot(u, v), 2, "1393 q1"); eq(norm(u), 5, "1393 q2"); eq(dot(u, u), 25, "1393 q3")
eq(dot(2 * u, v), 4, "1393 q4")
eq(dot(u + v, w), 5, "1393 q6"); eq(dot(u, w), 14, "1393 q6b"); eq(dot(v, w), -9, "1393 q6c")

# ------------------------------------------------------------------ 1394
eq(dot(V(3, 4), V(-4, 3)), 0, "1394 q1")
m = sp.symbols("m")
ok(sp.solve(dot(V(2, 3), V(m, -4)), m) == [6], "1394 q2")
eq(dot(V(5, 2), V(2, -5)), 0, "1394 q3")
eq(dot(V(1, 2), V(4, -1)), 2, "1394 q4")
ok(sp.solve(dot(V(m, 3), V(2, -1)), m) == [sp.Rational(3, 2)], "1394 q5")
ok(sorted(sp.solve(dot(V(m, 2), V(m, -8)), m)) == [-4, 4], "1394 q6")

# ------------------------------------------------------------------ 1395
eq(5 * 3 * cos(60), sp.Rational(15, 2), "1395 q1")
eq(4 * 6 * cos(180), -24, "1395 q2")
eq(sp.Rational(6, 12), cos(60), "1395 q3")
eq(sp.sqrt(25 + 4), sp.sqrt(29), "1395 q4")
eq(6 * 4 * cos(120), -12, "1395 q5")

# ------------------------------------------------------------------ 1396
eq(9 + 2 * 5 + 16, 35, "1396 q1"); eq(25 - 12 + 4, 17, "1396 q2"); eq(16 - 9, 7, "1396 q3")
eq(sp.Rational(64 - 36 - 16, 2), 6, "1396 q4")
U, W = V(a, b), V(c, d)
eq(dot(U + W, U + W) + dot(U - W, U - W), 2 * (dot(U, U) + dot(W, W)), "1396 q5")

# ------------------------------------------------------------------ 1397
A, B, C = P(1, 2), P(4, 6), P(2, 5)
ok([dot(vec(A, B), vec(A, C)), dot(vec(B, A), vec(B, C)), dot(vec(C, A), vec(C, B))] == [15, 10, -5], "1397 q1")
eq(dot(vec(P(1, 3), P(5, 7)), vec(P(0, 4), P(3, 1))), 0, "1397 q2")
A, B, C = P(0, 0), P(3, 4), P(1, 5)
eq(dot(vec(A, B), vec(A, C)), 23, "1397 q3 ps"); eq(norm(vec(A, C)), sp.sqrt(26), "1397 q3 AC")
ok(arr(deg(23 / (5 * math.sqrt(26)))) == 25.6, "1397 q3 angle")
A, B, C = P(2, 1), P(5, 3), P(0, 4)
eq(dot(vec(A, B), vec(A, C)), 0, "1397 q4")
A, B, C = P(1, 2), P(4, 6), P(2, 8)
I = (B + C) / 2
ok(I == P(3, 7), "1397 q5 I"); eq(norm(vec(A, I)), sp.sqrt(29), "1397 q5")

# ------------------------------------------------------------------ 1398
eq(sp.sqrt(25 + 49 - 2 * 5 * 7 * cos(60)), sp.sqrt(39), "1398 q1")
eq(sp.Rational(36 + 64 - 100, 2 * 6 * 8), 0, "1398 q2")
eq(sp.Rational(16 + 25 - 36, 40), sp.Rational(1, 8), "1398 q3"); ok(arr(deg(1 / 8)) == 82.8, "1398 q3 angle")
eq(sp.Rational(16 + 36 - 64, 48), -sp.Rational(1, 4), "1398 q5"); ok(arr(deg(-1 / 4)) == 104.5, "1398 q5 angle")

# ------------------------------------------------------------------ 1399
eq(dot(P(0, 0) - P(x, y), P(4, 0) - P(x, y)), (x - 2) ** 2 + y ** 2 - 4, "1399 q2")
eq(dot(P(-1, 0) - P(x, y), P(1, 0) - P(x, y)), x ** 2 + y ** 2 - 1, "1399 q3")
A, B = P(2, 1), P(6, 3)
ok((A + B) / 2 == P(4, 2), "1399 q4 I"); eq(norm(vec(A, B)) / 2, sp.sqrt(5), "1399 q4 r")
eq(sp.sqrt(9 + 9), 3 * sp.sqrt(2), "1399 q5")

# ------------------------------------------------------------------ 1400
A, B, C = P(1, 2), P(5, 4), P(3, 6)
ok([dot(vec(A, B), vec(A, C)), dot(vec(B, A), vec(B, C)), dot(vec(C, A), vec(C, B))] == [16, 4, 4], "1400 q1")
eq(norm(vec(A, B)), 2 * sp.sqrt(5), "1400 AB"); eq(norm(vec(B, C)), 2 * sp.sqrt(2), "1400 BC")
ok(arr(deg(0.8)) == 36.9 and arr(deg(4 / math.sqrt(160))) == 71.6, "1400 q1c")
eq(sp.sqrt(16 + 12 + 9), sp.sqrt(37), "1400 q2a"); eq(sp.sqrt(16 - 12 + 9), sp.sqrt(13), "1400 q2b")
ok(arr(deg(0.2)) == 78.5 and arr(deg(38 / 70)) == 57.1 and arr(deg(60 / 84)) == 44.4, "1400 q3")
ok(abs(deg(0.2) + deg(38 / 70) + deg(60 / 84) - 180) < 1e-9, "1400 q3 somme")
eq(sp.sqrt(12 + 16), 2 * sp.sqrt(7), "1400 q4")

# ------------------------------------------------------------------ 1401 (remplacé)
A, B, C, D = P(0, 0), P(6, 0), P(6, 4), P(0, 4)
eq(dot(vec(A, B), vec(A, C)), 36, "1401 A1")
eq(dot(vec(A, B), vec(A, D)), 0, "1401 A2a"); eq(dot(vec(A, D), vec(A, C)), 16, "1401 A2b")
eq(dot(vec(A, B), vec(C, D)), -36, "1401 A3")
eq(dot(vec(A, C), vec(A, C)), 52, "1401 A4"); eq(norm(vec(A, C)), 2 * sp.sqrt(13), "1401 A4b")
I = (C + D) / 2
eq(dot(vec(A, B), vec(A, I)), 18, "1401 A5")
eq(dot(vec(B, A), vec(B, I)), 18, "1401 A5b")
A, B, C, D = P(0, 0), P(4, 0), P(4, 4), P(0, 4)
I, J = (A + B) / 2, (B + C) / 2
eq(dot(vec(D, A), vec(B, J)), -8, "1401 B1a"); eq(dot(vec(A, I), vec(A, B)), 8, "1401 B1b")
eq(dot(vec(D, A), vec(A, B)), 0, "1401 B1c"); eq(dot(vec(A, I), vec(B, J)), 0, "1401 B1d")
eq(dot(vec(D, I), vec(A, J)), 0, "1401 B3/B4")

# ------------------------------------------------------------------ 1402
u, v = V(4, 3), V(-1, 2)
eq(dot(u, v), 2, "1402 ex1"); ok(arr(deg(2 / (5 * math.sqrt(5)))) == 79.7, "1402 ex1 angle")
A, B, C = P(0, 0), P(6, 0), P(3, 4)
eq(norm(vec(A, C)), 5, "1402 AC"); eq(norm(vec(B, C)), 5, "1402 BC")
ok([dot(vec(A, B), vec(A, C)), dot(vec(B, A), vec(B, C)), dot(vec(C, A), vec(C, B))] == [18, 18, 7], "1402 ps")
ok(arr(deg(0.6)) == 53.1 and arr(deg(7 / 25)) == 73.7, "1402 angles")
ok(abs(2 * deg(0.6) + deg(7 / 25) - 180) < 1e-9, "1402 somme")
eq(sp.Rational(2 * 12, 5), sp.Rational(24, 5), "1402 hauteur")
eq(sp.sqrt(4 + 4), 2 * sp.sqrt(2), "1402 ex3")

# ------------------------------------------------------------------ 1403
u, v = V(3, 4), V(-2, 1)
eq(dot(u, v), -2, "1403 q1"); eq(norm(v), sp.sqrt(5), "1403 q2")
ok(round(math.acos(-2 / (5 * math.sqrt(5))), 2) == 1.75, "1403 q4"); eq(norm(u + v), sp.sqrt(26), "1403 q5")
A, B, C = P(2, 1), P(6, 5), P(4, 7)
eq(dot(vec(A, B), vec(A, C)), 32, "1403 ex2"); eq(dot(vec(B, A), vec(B, C)), 0, "1403 rect B")
eq(norm(vec(A, B)), 4 * sp.sqrt(2), "1403 AB"); eq(norm(vec(A, C)), 2 * sp.sqrt(10), "1403 AC"); eq(norm(vec(B, C)), 2 * sp.sqrt(2), "1403 BC")
ok(arr(deg(32 / (4 * math.sqrt(2) * 2 * math.sqrt(10)))) == 26.6, "1403 angle")
eq(norm(vec(A, (B + C) / 2)), sp.sqrt(34), "1403 médiane")
eq(sp.sqrt(49 + 25 - 2 * 7 * 5 * cos(120)), sp.sqrt(109), "1403 ex3 q1"); eq(sp.sqrt(74), sp.sqrt(49 + 25), "1403 ex3 q2")

# ------------------------------------------------------------------ 1404
A, B, C = P(-1, 2), P(3, 4), P(1, 8)
eq(dot(vec(A, B), vec(A, C)), 20, "1404 ps"); eq(norm(vec(A, B)), 2 * sp.sqrt(5), "1404 AB"); eq(norm(vec(A, C)), 2 * sp.sqrt(10), "1404 AC")
eq(20 / (norm(vec(A, B)) * norm(vec(A, C))), sp.sqrt(2) / 2, "1404 cos 45")
eq(dot(vec(B, A), vec(B, C)), 0, "1404 rect B"); eq(norm(vec(B, C)), 2 * sp.sqrt(5), "1404 BC")
eq(sp.sqrt(9 + 9), 3 * sp.sqrt(2), "1404 ex3")

# ------------------------------------------------------------------ 1405
A, B, C = P(0, 0), P(8, 0), P(4, 6)
ok([dot(vec(A, B), vec(A, C)), dot(vec(B, A), vec(B, C)), dot(vec(C, A), vec(C, B))] == [32, 32, 20], "1405 ps")
eq(norm(vec(A, C)), 2 * sp.sqrt(13), "1405 AC")
ok(arr(deg(32 / (8 * math.sqrt(52)))) == 56.3 and arr(deg(20 / 52)) == 67.4, "1405 angles")
eq(sp.Rational(8 * 6, 2), 24, "1405 aire")
eq(sp.sqrt(-12 + 16), 2, "1405 C2"); eq(sp.sqrt(20 + 16), 6, "1405 C3")
eq(sp.sqrt(100 + 64 - 2 * 10 * 8 * cos(60)), 2 * sp.sqrt(21), "1405 EF")
cE = (100 + 84 - 64) / (2 * 10 * math.sqrt(84)); cF = (64 + 84 - 100) / (2 * 8 * math.sqrt(84))
ok(arr(deg(cE)) == 49.1 and arr(deg(cF)) == 70.9, "1405 E F")
eq(sp.Rational(120, 20) / sp.sqrt(84), 3 / sp.sqrt(21), "1405 cos E exact")
eq(sp.Rational(48, 16) / sp.sqrt(84), 3 / (2 * sp.sqrt(21)), "1405 cos F exact")

# ------------------------------------------------------------------ nouveau-1 (projection, quadrillage)
A, B = P(0, 0), P(4, 0)
for nom, Q, val in [("C", P(3, 2), 12), ("D", P(-2, 3), -8), ("E", P(2, -3), 8), ("F", P(0, 3), 0)]:
    eq(dot(vec(A, B), vec(A, Q)), val, "nouveau-1 " + nom)
eq(6 * 3, 6 * 6 * cos(60), "nouveau-1 équilatéral")

# ------------------------------------------------------------------ nouveau-2 (normes, médiane)
eq(sp.Rational(36 + 16 - 25, 2), sp.Rational(27, 2), "nouveau-2 q1")
eq(sp.Rational(27, 2) / 24, sp.Rational(9, 16), "nouveau-2 cos"); ok(arr(deg(9 / 16)) == 55.8, "nouveau-2 angle")
eq((36 + 16 - sp.Rational(25, 2)) / 2, sp.Rational(79, 4), "nouveau-2 médiane²")
eq(sp.Rational(1, 4) * (36 + 2 * sp.Rational(27, 2) + 16), sp.Rational(79, 4), "nouveau-2 vérif")
ok(arr(math.sqrt(79) / 2, 2) == 4.44, "nouveau-2 AI")
# contrôle numérique : triangle de côtés 6, 4, 5
cA = 9 / 16
Bp = (6.0, 0.0); Cp = (4 * cA, 4 * math.sqrt(1 - cA ** 2))
ok(abs(math.dist(Bp, Cp) - 5) < 1e-12, "nouveau-2 BC")
Ip = ((Bp[0] + Cp[0]) / 2, (Bp[1] + Cp[1]) / 2)
ok(abs(math.hypot(*Ip) - math.sqrt(79) / 2) < 1e-12, "nouveau-2 AI num")

# ------------------------------------------------------------------ nouveau-3 (randonneur)
eq(sp.sqrt(9 + 25 - 2 * 3 * 5 * cos(120)), 7, "nouveau-3 BC")
eq(sp.Rational(9 + 49 - 25, 42), sp.Rational(11, 14), "nouveau-3 cos B"); ok(arr(deg(11 / 14)) == 38.2, "nouveau-3 B")
eq(sp.Rational(25 + 49 - 9, 70), sp.Rational(13, 14), "nouveau-3 cos C"); ok(arr(deg(13 / 14)) == 21.8, "nouveau-3 C")
ok(abs(120 + deg(11 / 14) + deg(13 / 14) - 180) < 1e-9, "nouveau-3 somme")
eq(3 * 5 * cos(120), -sp.Rational(15, 2), "nouveau-3 AB.AC")
eq(sp.Rational(15, 2) / 5, sp.Rational(3, 2), "nouveau-3 AH")
eq(sp.sqrt(9 - sp.Rational(9, 4)), 3 * sp.sqrt(3) / 2, "nouveau-3 BH"); ok(arr(1.5 * math.sqrt(3), 1) == 2.6, "nouveau-3 BH ~")
# contrôle par coordonnées : A(0;0), C(5;0), B = 3(cos120 ; sin120)
Bn = (3 * math.cos(2 * math.pi / 3), 3 * math.sin(2 * math.pi / 3))
ok(abs(math.dist(Bn, (5, 0)) - 7) < 1e-12 and abs(Bn[0] + 1.5) < 1e-12, "nouveau-3 coord")

print(f"{N} vérifications : tout est juste.")
