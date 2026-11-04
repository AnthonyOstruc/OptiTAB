# -*- coding: utf-8 -*-
"""Vérification (sympy) de tous les résultats de la notion 154 : cours, fiche, exercices."""
from sympy import (Rational as R, S, Symbol, expand, factor, solve, sqrt, pi, simplify, solveset,
                   Interval, Union, FiniteSet, Reals, nsimplify, discriminant, N, Complement)

x, t, m, q, X = Symbol("x", real=True), Symbol("t", real=True), Symbol("m", real=True), Symbol("q", real=True), Symbol("X", real=True)
nb = 0


def ok(cond, msg):
    global nb
    nb += 1
    assert cond, msg


def eq(a, b, msg):
    ok(simplify(a - b) == 0, f"{msg} : {a} != {b}")


def racines(p, v=x):
    return sorted(solve(p, v))


def canon(p, v=x):
    a = p.as_poly(v).all_coeffs()[0]
    b = p.as_poly(v).all_coeffs()[1]
    al = -b / (2 * a)
    return a, al, p.subs(v, al)


def ens(ineq, v=x):
    return solveset(ineq, v, Reals)


# ------------------------------------------------------------------ cours
f = 2*x**2 + 4*x - 6
ok(canon(f) == (2, -1, -8), "cours canonique")
ok(racines(f) == [-3, 1], "cours racines")
ok(discriminant(f, x) == 64, "cours delta")
ok(discriminant(x**2 - 6*x + 9, x) == 0 and discriminant(x**2 + x + 1, x) == -3, "cours trois cas")
eq(factor(3*x**2 - 5*x + 2), (x - 1)*(3*x - 2), "cours racine évidente")
ok(racines(x**2 - 7*x + 12) == [3, 4], "cours somme produit")
ok(ens(f <= 0) == Interval(-3, 1), "cours inéquation")
h = -5*(t - 2)**2 + 30
eq(expand(h), -5*t**2 + 20*t + 10, "balle développée")
ok(racines(h, t) == [2 - sqrt(6), 2 + sqrt(6)] and abs(N(2 + sqrt(6)) - 4.449) < 1e-3, "balle sol")
ok(racines(x**4 - 5*x**2 + 4) == [-2, -1, 1, 2], "cours bicarrée")
# démonstration : forme canonique générale
a_, b_, c_ = Symbol("a"), Symbol("b"), Symbol("c")
eq(a_*((x + b_/(2*a_))**2 - (b_**2 - 4*a_*c_)/(4*a_**2)), a_*x**2 + b_*x + c_, "démonstration")

# ------------------------------------------------------------------ 1314
for p, d, r in [(x**2 - 4*x + 3, 4, [1, 3]), (x**2 - 4*x + 4, 0, [2]), (x**2 - 4*x + 5, -4, []),
                (2*x**2 + 8*x + 6, 16, [-3, -1]), (-x**2 + 2*x - 1, 0, [1])]:
    ok(discriminant(p, x) == d and racines(p) == r, f"1314 {p}")
# 1313
ok(racines((x - 2)*(x + 3)) == [-3, 2], "1313 q2")
ok(discriminant(x**2 - 6*x + 9, x) == 0, "1313 q3")
ok(racines(x**2 - 5*x + 6) == [2, 3], "1313 q4")
eq(expand(2*(x - 1)*(x + 4)), 2*x**2 + 6*x - 8, "1313 q5")

# ------------------------------------------------------------------ 1324
f = 2*x**2 - 8*x + 6
ok(discriminant(f, x) == 16 and racines(f) == [1, 3], "1324 A1 A2")
eq(f, 2*(x - 1)*(x - 3), "1324 A3")
ok(canon(f) == (2, 2, -2), "1324 A4")
ok(ens(f >= 0) == Union(Interval(-S.Infinity, 1), Interval(3, S.Infinity)), "1324 A5")
A = x*(8 - x)
ok(canon(A) == (-1, 4, 16), "1324 B")
P = x**2 - (m + 2)*x + 2*m
eq(discriminant(P, x), (m - 2)**2, "1324 C1")
eq(P, (x - 2)*(x - m), "1324 C3")

# ------------------------------------------------------------------ 1325
ok(racines(x**2 - 6*x + 8) == [2, 4], "1325 A1")
ok(ens(-2*x**2 + 10*x - 12 >= 0) == Interval(2, 3), "1325 A2")
Pp, Qq = x**2 - 5*x + 6, x**2 - 3*x + 2
ok(ens(Pp*Qq > 0) == Union(Interval.open(-S.Infinity, 1), Interval.open(3, S.Infinity)), "1325 A3")
f = -x**2 + 4*x - 3
ok([f.subs(x, v) for v in (0, 1, 3)] == [-3, 0, 0], "1325 B1")
ok(canon(f) == (-1, 2, 1), "1325 B3")
h = -5*t**2 + 10*t + R(3, 2)
ok(canon(h, t) == (-5, 1, R(13, 2)), "1325 C1")
sol = racines(h, t)
eq(sol[1], 1 + sqrt(130)/10, "1325 C2")
ok(round(float(sol[1]), 2) == 2.14 and float(sol[0]) < 0, "1325 C2 arrondi")
r6 = racines(h - 6, t)
eq(r6[0], 1 - sqrt(10)/10, "1325 C3 t1")
eq(r6[1] - r6[0], sqrt(10)/5, "1325 C3 durée")
ok(round(float(r6[1] - r6[0]), 2) == 0.63, "1325 C3 arrondi 0,63")
ok(round(float(r6[0]), 2) == 0.68 and round(float(r6[1]), 2) == 1.32, "1325 C3 bornes")
ok(discriminant(10*t**2 - 20*t + 9, t) == 40, "1325 C3 delta")

# ------------------------------------------------------------------ 1328
ok(racines(3*x**2 - 12*x + 9) == [1, 3], "1328 A1")
ok(ens(x**2 - 4*x + 3 < 0) == Interval.open(1, 3), "1328 A2")
eq(2*x**2 - 10*x + 12, 2*(x - 2)*(x - 3), "1328 A3")
ok(canon(-x**2 + 6*x - 5) == (-1, 3, 4), "1328 A4")
h = x**2 - 6*x + 8
ok(discriminant(h, x) == 4 and racines(h) == [2, 4] and canon(h) == (1, 3, -1), "1328 B")
ok(ens(h <= 0) == Interval(2, 4), "1328 B4")
H = -5*t**2 + 20*t + 5
ok(canon(H, t) == (-5, 2, 25), "1328 C1")
eq(racines(H, t)[1], 2 + sqrt(5), "1328 C2")
ok(round(float(2 + sqrt(5)), 2) == 4.24 and round(float(2 - sqrt(5)), 2) == -0.24, "1328 C2 arrondi")

# ------------------------------------------------------------------ 1318
ok(racines(x**2 - 5*x + 6) == [2, 3], "1318 q1")
eq(-x**2 + 4*x - 4, -(x - 2)**2, "1318 q2")
ok(discriminant(x**2 + 2*x + 3, x) == -8, "1318 q3")
eq(2*x**2 - 8*x + 6, 2*(x - 1)*(x - 3), "1318 q4")
eq(-3*x**2 + 6*x - 3, -3*(x - 1)**2, "1318 q5")
ok(ens(2*x**2 - 8*x + 6 <= 0) == Interval(1, 3), "1318 q6a")
ok(ens(-x**2 + 4*x - 4 < 0) == Complement(Reals, FiniteSet(2)), "1318 q6b")

# ------------------------------------------------------------------ 1317
for p, c in [(x**2 - 4*x + 1, (1, 2, -3)), (2*x**2 - 8*x + 5, (2, 2, -3)), (-x**2 + 6*x - 8, (-1, 3, 1)),
             (3*x**2 + 6*x + 2, (3, -1, -1)), (-2*x**2 + 4*x - 1, (-2, 1, 1))]:
    ok(canon(p) == c, f"1317 {p}")

# ------------------------------------------------------------------ 1322
f = -2*x**2 + 12*x - 16
ok(discriminant(f, x) == 16 and racines(f) == [2, 4] and canon(f) == (-2, 3, 2), "1322 q1")
ok(ens(f > 0) == Interval.open(2, 4), "1322 q1d")
eq(expand((x - 2)*(x - 3)), x**2 - 5*x + 6, "1322 q2")
P = x**2 - (m + 1)*x + m
eq(discriminant(P, x), (m - 1)**2, "1322 q3")
eq(P, (x - 1)*(x - m), "1322 q3 facto")
y = Symbol("y", real=True)
ok(sorted(solve([x + y - 8, x**2 + y**2 - 34], [x, y])) == [(3, 5), (5, 3)], "1322 q4")
a1, b1, c1 = Symbol("a1", positive=True), Symbol("b1", positive=True), Symbol("c1", positive=True)
ok(solve([a1 + b1 + c1 - 24, a1*b1 - 48, a1**2 + b1**2 - c1**2], [a1, b1, c1]) in ([(6, 8, 10), (8, 6, 10)], [(8, 6, 10), (6, 8, 10)]), "1322 q5")

# ------------------------------------------------------------------ 1426
eq(expand((x - 2)**2), x**2 - 4*x + 4, "1426 h")
eq(expand((x + 1)**2 + 2), x**2 + 2*x + 3, "1426 p")
ok(((x + 1)**2 + 2).subs(x, 0) == 3 and ((x - 2)**2).subs(x, 0) == 4, "1426 images de 0")

# ------------------------------------------------------------------ 1319
ok(racines(x**2 - 7*x + 12) == [3, 4], "1319 q1")
r = racines(x**2 - 5*x + 6)
ok(r[0]**2 + r[1]**2 == 13, "1319 q2")
eq(expand((x - 2)*(x + 3)), x**2 + x - 6, "1319 q3")
r = racines(2*x**2 + 8*x + 6)
eq(1/r[0] + 1/r[1], R(-4, 3), "1319 q4")
ok(sorted(solve(discriminant(x**2 - m*x + 9, x), m)) == [-6, 6], "1319 q5")
ok(racines(5*x**2 - 3*x - 2) == [R(-2, 5), 1], "1319 q6")
eq(5*x**2 - 3*x - 2, (x - 1)*(5*x + 2), "1319 q6 facto")

# ------------------------------------------------------------------ 1315
for p, r in [(x**2 - 7*x + 12, [3, 4]), (2*x**2 - 8*x + 8, [2]), (x**2 + 2*x + 5, []), (3*x**2 - 12*x + 9, [1, 3]),
             (-x**2 + 6*x - 9, [3]), (2*x**2 + x - 6, [-2, R(3, 2)]), (x**2 - 5*x, [0, 5])]:
    ok(racines(p) == r, f"1315 {p}")
ok(discriminant(2*x**2 + x - 6, x) == 49 and discriminant(x**2 + 2*x + 5, x) == -16, "1315 deltas")

# ------------------------------------------------------------------ 1321
ok(sorted(solve([x + y - 5, x*y - 6], [x, y])) == [(2, 3), (3, 2)], "1321 q2")
eq(expand(3*(x - 2)**2 - 12), 3*x**2 - 12*x, "1321 q3")
ok(sorted(solve(discriminant(x**2 + m*x + 4, x), m)) == [-4, 4], "1321 q4")
ok(ens(2*x**2 - 8*x + 6 < 0) == Interval.open(1, 3), "1321 q1d")

# ------------------------------------------------------------------ 1316
eq(4*x**2 - 12*x + 9, (2*x - 3)**2, "1316 q2")
eq(2*x**2 + 3*x - 5, (x - 1)*(2*x + 5), "1316 q4")
eq(3*x**2 + 6*x - 9, 3*(x - 1)*(x + 3), "1316 q5")
eq(expand((x - 1 - sqrt(5))*(x - 1 + sqrt(5))), x**2 - 2*x - 4, "1316 q6")
ok(discriminant(x**2 + x + 1, x) == -3, "1316 q7")

# ------------------------------------------------------------------ 1320
ok(canon(x*(10 - x)) == (-1, 5, 25), "1320 q1")
ok(canon(-5*t**2 + 20*t + 10, t) == (-5, 2, 30), "cours V : balle (ancienne question 2 de 1320, réécrite le 2026-11-02, voir plus bas)")
Rx = (20 - x)*(300 + 25*x)
eq(expand(Rx), -25*x**2 + 200*x + 6000, "1320 q3a")
ok(canon(expand(Rx)) == (-25, 4, 6400), "1320 q3b")
L, l = Symbol("L", positive=True), Symbol("l", positive=True)
ok(sorted(solve([L*l - 24, (L + 2)*(l + 1) - 40], [L, l])) == [(6, 4), (8, 3)], "1320 q4")

# ------------------------------------------------------------------ 1323
n = Symbol("n", integer=True)
ok(sorted(solve(n*(n + 1) - 506, n)) == [-23, 22], "1323 q1")
h = -5*t**2 + 30*t
ok(canon(h, t) == (-5, 3, 45) and racines(h, t) == [0, 6], "1323 q2ab")
ok(ens(h > 40, t) == Interval.open(2, 4), "1323 q2c")
ok(sorted(solve((8 + 2*x)*(6 + 2*x) - 80, x)) == [-8, 1], "1323 q3")
hh = 3 - x/2 - pi*x/4
eq(x + 2*hh + pi*x/2, 6, "1323 q4a")
Af = x*hh + pi*x**2/8
eq(Af, 3*x - (4 + pi)/8*x**2, "1323 q4b")
xs = 12/(4 + pi)
eq(-3/(2*(-(4 + pi)/8)), xs, "1323 q4c alpha")
eq(Af.subs(x, xs), 18/(4 + pi), "1323 q4c aire")
eq(hh.subs(x, xs), 6/(4 + pi), "1323 q4c h")
ok(round(float(xs), 2) == 1.68 and round(float(18/(4 + pi)), 2) == 2.52 and round(float(6/(4 + pi)), 2) == 0.84, "1323 arrondis")

# ------------------------------------------------------------------ 1326
f = 3*x**2 - 12*x + 9
ok(discriminant(f, x) == 36 and racines(f) == [1, 3], "1326 1.2")
eq(expand((x + 2)*(x - 5)), x**2 - 3*x - 10, "1326 1.3")
B = 50*q - (q**2 + 10*q + 300)
eq(B, -q**2 + 40*q - 300, "1326 2.1")
ok(canon(expand(B), q) == (-1, 20, 100), "1326 2.2")
eq(B, -(q - 10)*(q - 30), "1326 2.3")
ok(ens(B >= 0, q) == Interval(10, 30), "1326 2.3 ensemble")
a = Symbol("a", real=True)
Pa = x**2 - 2*a*x + a**2 - 1
ok(simplify(discriminant(Pa, x)) == 4, "1326 3.1")
ok(sorted(solve(Pa, x), key=lambda e: e.subs(a, 0)) == [a - 1, a + 1], "1326 3.2")
eq(Pa.subs(a, 3), (x - 2)*(x - 4), "1326 3.2 P3")
ok(solveset(a**2 - 1 < 0, a, Reals) == Interval.open(-1, 1), "1326 3.3")

# ------------------------------------------------------------------ 1327
ok(racines(x**2 + 4*x + 5) == [] and racines(2*x**2 - 8*x + 8) == [2], "1327 A1")
ok(ens(x**2 - 5*x + 6 >= 0) == Union(Interval(-S.Infinity, 2), Interval(3, S.Infinity)), "1327 A2a")
ok(ens(-x**2 + 6*x - 9 < 0) == Complement(Reals, FiniteSet(3)), "1327 A2b")
f = -x**2 + 6*x - 5
ok(canon(f) == (-1, 3, 4) and racines(f) == [1, 5], "1327 A3")
A = x*(100 - 2*x)
ok(canon(expand(A)) == (-2, 25, 1250), "1327 B2")
ok(ens(A >= 1200) == Interval(20, 30), "1327 B3")
ok(discriminant(x**2 - 50*x + 600, x) == 100, "1327 B3 delta")

# ------------------------------------------------------------------ 1329
ok(racines(x**2 - 8*x + 15) == [3, 5], "1329 1.1")
ok(ens(-2*x**2 + 8*x - 6 >= 0) == Interval(1, 3), "1329 1.2")
ok(canon(x**2 - 4*x + 3) == (1, 2, -1), "1329 1.3")
Pm = x**2 - 2*m*x + m + 2
eq(discriminant(Pm, x), 4*(m + 1)*(m - 2), "1329 3.1")
ok(solveset(discriminant(Pm, x) > 0, m, Reals) == Union(Interval.open(-S.Infinity, -1), Interval.open(2, S.Infinity)), "1329 3.2")
eq(Pm.subs(m, -1), (x + 1)**2, "1329 m=-1")
eq(Pm.subs(m, 2), (x - 2)**2, "1329 m=2")

# ------------------------------------------------------------------ 1330
f = 2*x**2 - 2*x - 12
ok(discriminant(f, x) == 100 and racines(f) == [-2, 3], "1330 A2")
ok(ens(f < 0) == Interval.open(-2, 3), "1330 A2 inéquation")
f = R(-3, 2)*(x - 1)*(x - 4)
ok(f.subs(x, 0) == -6, "1330 A3")
eq(expand(f), R(-3, 2)*x**2 + R(15, 2)*x - 6, "1330 A3 développée")
g = -x**2 + 2*x + 3
ok(discriminant(g, x) == 16 and racines(g) == [-1, 3] and canon(g) == (-1, 1, 4), "1330 B")
ok(ens(g >= 0) == Interval(-1, 3), "1330 B3")
ok(canon(expand(x*(28 - 2*x))) == (-2, 7, 98), "1330 C")

# ------------------------------------------------------------------ nouveau-1
for p, sommet, pt in [((x - 1)**2 - 4, (1, -4), (3, 0)), (-(x - 2)**2, (2, 0), (0, -4)),
                      (R(1, 2)*(x + 1)**2 + 1, (-1, 1), (1, 3)), (-(x + 1)**2 + 4, (-1, 4), (1, 0))]:
    ok(canon(expand(p))[1:] == sommet and p.subs(x, pt[0]) == pt[1], f"nouveau-1 {p}")
ok(racines((x - 1)**2 - 4) == [-1, 3] and racines(-(x + 1)**2 + 4) == [-3, 1], "nouveau-1 racines")
ok(discriminant(expand(R(1, 2)*(x + 1)**2 + 1), x) < 0, "nouveau-1 C3")

# ------------------------------------------------------------------ nouveau-2
ok(racines(x**2 - 2*x - 1 - (x + 3)) == [-1, 4], "nouveau-2 q1")
ok(ens(x**2 - 2*x - 1 - (x + 3) < 0) == Interval.open(-1, 4), "nouveau-2 q2")
eq(discriminant(x**2 - 4*x - 1 - m, x), 4*m + 20, "nouveau-2 q3")
ok(racines(x**2 - 4*x - 1 + 5) == [2] and (2*2 - 5) == -1 and (x**2 - 2*x - 1).subs(x, 2) == -1, "nouveau-2 tangente")

# ------------------------------------------------------------------ nouveau-3
ok(racines(x**4 - 5*x**2 + 4) == [-2, -1, 1, 2], "nouveau-3 q1")
ok(racines(x**4 - x**2 - 12) == [-2, 2], "nouveau-3 q2")
ok(racines(x**4 + 3*x**2 + 2) == [], "nouveau-3 q3")
xp = Symbol("xp", nonnegative=True)
ok(sorted(solve(xp - 5*sqrt(xp) + 6, xp)) == [4, 9], "nouveau-3 q4")

# ================================================================== finition 2026-11-02
v = Symbol("v", real=True)
# 1320 question 2 réécrite : distance d'arrêt d(v) = 0,005 v² + 0,3 v
d = R(5, 1000)*v**2 + R(3, 10)*v
ok(d.subs(v, 50) == R(55, 2) and d.subs(v, 90) == R(135, 2), "1320 q2a : 27,5 et 67,5")
eq(expand(200*(d - 50)), v**2 + 60*v - 10000, "1320 q2b : mise en inéquation")
ok(discriminant(v**2 + 60*v - 10000, v) == 43600 and simplify(sqrt(43600) - 20*sqrt(109)) == 0, "1320 q2b : Δ")
ok(racines(v**2 + 60*v - 10000, v) == [-30 - 10*sqrt(109), -30 + 10*sqrt(109)], "1320 q2b : racines")
ok(abs(N(-30 + 10*sqrt(109)) - 74.4) < 0.01 and d.subs(v, 74) <= 50 and d.subs(v, 75) == R(50625, 1000), "1320 q2b : 74 km/h, d(75) = 50,625")
ok(ens(d - 50 <= 0, v) == Interval(-30 - 10*sqrt(109), -30 + 10*sqrt(109)), "1320 q2b : ensemble")

# 1329 exercice 2 réécrit : carré inscrit, S(x) = x² + (10 − x)²
Sx = expand(x**2 + (10 - x)**2)
eq(Sx, 2*x**2 - 20*x + 100, "1329 2.1")
ok(canon(Sx) == (2, 5, 50), "1329 2.2 : minimum 50 en 5")
eq(expand(Sx - 58), 2*(x**2 - 10*x + 21), "1329 2.3 : mise en forme")
ok(ens(Sx - 58 <= 0) == Interval(3, 7), "1329 2.3 : [3 ; 7]")
ok(Sx.subs(x, 0) == 100 and Sx.subs(x, 10) == 100, "1329 : x = 0 ou 10, MNPQ = ABCD")

# valeurs portées sur les figures ajoutées
for c_, nb_ in [(3, 2), (4, 1), (5, 0)]:
    ok(len(solve(x**2 - 4*x + c_, x)) == nb_, f"trois_paraboles c = {c_}")
ok(canon(2*x**2 - 8*x + 6) == (2, 2, -2) and racines(2*x**2 - 8*x + 6) == [1, 3], "ds1_f (1324 et 1321)")
ok(canon(-x**2 + 8*x) == (-1, 4, 16), "ds1_aire")
ok(canon(-x**2 + 4*x - 3) == (-1, 2, 1) and racines(-x**2 + 4*x - 3) == [1, 3], "ds2_f")
ok(canon(x**2 - 6*x + 8) == (1, 3, -1) and ens(x**2 - 6*x + 8 <= 0) == Interval(2, 4), "ds3_h")
H = -5*t**2 + 20*t + 5
ok(canon(H, t) == (-5, 2, 25) and racines(H, t)[1] == 2 + sqrt(5) and abs(N(2 + sqrt(5)) - 4.24) < 0.005, "ds3_ballon")
ok(ens(2*(x - 1)*(x - 3) <= 0) == Interval(1, 3) and ens(-(x - 2)**2 < 0) == Complement(Reals, FiniteSet(2)), "signe_kg")
ok(canon(expand((x - 2)**2 - 3)) == (1, 2, -3) and canon(expand(2*(x - 2)**2 - 3)) == (2, 2, -3), "canon_fg")
ok(canon(expand(-2*(x - 3)**2 + 2)) == (-2, 3, 2) and ens(-2*(x - 3)**2 + 2 > 0) == Interval.open(2, 4), "synthese_f")
ok(6 + 8 + 10 == 24 and 6*8/2 == 24 and 6**2 + 8**2 == 10**2, "triangle")
ok(canon(-5*t**2 + 30*t, t) == (-5, 3, 45) and ens(-5*x**2 + 30*x - 40 > 0) == Interval.open(2, 4), "projectile_1323")
ok((8 + 2*1)*(6 + 2*1) == 80, "parterre_corrige")
al = 12/(4 + pi)
ok(abs(N(al) - 1.68) < 0.005 and abs(N(6/(4 + pi)) - 0.84) < 0.005 and abs(N(18/(4 + pi)) - 2.52) < 0.005, "fenetre_corrige")
eq(3 - al/2 - pi*al/4, 6/(4 + pi), "fenetre : h = 6/(4 + π)")
ok(canon(-25*x**2 + 200*x + 6000) == (-25, 4, 6400) and (20 - 4) == 16 and 300 + 25*4 == 400, "theatre_recette")
ok(canon(-q**2 + 40*q - 300, q) == (-1, 20, 100) and ens(-x**2 + 40*x - 300 >= 0) == Interval(10, 30), "benefice")
ok(canon(-2*x**2 + 100*x) == (-2, 25, 1250) and ens(-2*x**2 + 100*x - 1200 >= 0) == Interval(20, 30), "champ_aire")
ok(100 - 2*25 == 50 and 28 - 2*7 == 14 and 7*14 == 98 and 25*50 == 1250, "enclos 25 et 7")
Pm2 = x**2 - 2*m*x + m + 2
ok(racines(Pm2.subs(m, -2)) == [-4, 0] and racines(Pm2.subs(m, -1)) == [-1] and racines(Pm2.subs(m, 0)) == [], "param_cas")
ok(discriminant(Pm2.subs(m, -2), x) > 0 and discriminant(Pm2.subs(m, 0), x) < 0, "param_cas : signes de Δ")
ok(racines(x**2 - 2*x - 1 - (2*x - 2)).__len__() == 2 and racines(x**2 - 2*x - 1 - (2*x - 8)) == [], "parabole_tangente D-2, D-8")

print(f"{nb} vérifications : toutes justes.")
