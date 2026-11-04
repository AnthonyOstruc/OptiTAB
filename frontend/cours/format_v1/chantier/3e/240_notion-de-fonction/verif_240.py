# -*- coding: utf-8 -*-
"""Vérification (sympy) de tous les calculs de la notion 240 « Notion de fonction »."""
from sympy import Rational as R, symbols, solve, expand, sqrt, Eq, nsimplify

x = symbols("x")
n_ok = 0


def ok(cond, msg):
    global n_ok
    assert cond, msg
    n_ok += 1


def antecedents(expr, b, domaine=None):
    s = [v for v in solve(Eq(expr, b), x) if v.is_real]
    s = sorted(s, key=float)
    if domaine:
        s = [v for v in s if domaine[0] <= v <= domaine[1]]
    return s


# ---- cours et fiche
f = 2 * x + 1
ok(f.subs(x, 3) == 7, "cours f(3)")
ok(antecedents(f, 9) == [4], "cours antécédent de 9")
g = x**2 - 3 * x
ok(g.subs(x, -2) == 10, "cours g(-2)")
ok(antecedents(x**2, 9) == [-3, 3] and antecedents(x**2, 0) == [0] and antecedents(x**2, -4) == [], "cours x^2")
c = x**2 - 4 * x + 1
ok([c.subs(x, v) for v in range(-1, 6)] == [6, 1, -2, -3, -2, 1, 6], "cours tableau")
ok(antecedents(c, -2) == [1, 3] and c.subs(x, 5) == 6 and c.subs(x, 2) == -3, "cours lecture")
ok(12 * R(3, 2) == 18, "cours cuve")
ok(f.subs(x, 1) == 3, "fiche M(1;3)")

# ---- 2275
f = 3 * x - 4
ok([f.subs(x, v) for v in (0, 2, -3, R(1, 3))] == [-4, 2, -13, -3], "2275")
# ---- 2276 (tableau donné : cohérent, lecture seulement)
T = {-2: 5, 0: 1, 1: -1, 3: 1, 4: 5}
ok([k for k, v in T.items() if v == 1] == [0, 3] and [k for k, v in T.items() if v == 5] == [-2, 4], "2276")
# ---- 2278
f = x**2 - 2
ok(f.subs(x, 3) == 7 and f.subs(x, -2) == 2 and f.subs(x, 5) == 23 and f.subs(x, -3) == 7, "2278")
# ---- 2279
h = 5 * x + 2
ok(antecedents(h, 17) == [3] and antecedents(h, -8) == [-2] and antecedents(h, 0) == [R(-2, 5)], "2279")
# ---- 2280 : f(x) = -x^2 + 2x + 3 sur [-2 ; 4]
f = -x**2 + 2 * x + 3
D = (-2, 4)
ok(f.subs(x, 1) == 4 and f.subs(x, 4) == -5 and f.subs(x, -2) == -5, "2280 images")
ok(antecedents(f, 3, D) == [0, 2] and antecedents(f, 0, D) == [-1, 3], "2280 antécédents")
ok(antecedents(f, 5, D) == [] and antecedents(f, 4, D) == [1], "2280 max")
# ---- 2281 exemples
ok((x + 5).subs(x, 3) == 8 and (x + 5).subs(x, 8) == 13, "2281 ex1")
ok((x**2 - 1).subs(x, 3) == 8 and (x**2 - 1).subs(x, -3) == 8, "2281 ex2")
# ---- 2282
f = (x + 3)**2
ok(f.subs(x, 1) == 16 and f.subs(x, -3) == 0 and f.subs(x, -5) == 4, "2282 images")
ok((x**2 + 3).subs(x, 1) == 4, "2282 Lucas")
ok(antecedents(f, 25) == [-8, 2], "2282 antécédents de 25")
# ---- 2283 : ligne brisée
def brisee(t):
    P = [(-4, 0), (-1, 3), (1, -1), (3, 1)]
    for (a, b), (c2, d) in zip(P, P[1:]):
        if a <= t <= c2:
            return b + R(d - b, c2 - a) * (t - a)
ok(brisee(-1) == 3 and brisee(1) == -1, "2283 sommets")
ok(sorted({t for t in [R(k, 4) for k in range(-16, 13)] if brisee(t) == 1}) == [-3, 0, 3], "2283 antécédents de 1")
ok([t for t in [R(k, 4) for k in range(-16, 13)] if brisee(t) == 3] == [-1], "2283 antécédents de 3")
ok(max(brisee(R(k, 4)) for k in range(-16, 13)) == 3, "2283 max 3")
ok(all((1 - 2 * x).subs(x, v) == brisee(v) for v in (-1, 0, 1, R(1, 2))), "2283 formule centrale")
# ---- 2284
ok(antecedents(x**2, 16) == [-4, 4] and antecedents(x**2, 7) == [-sqrt(7), sqrt(7)], "2284")
ok(abs(float(sqrt(7)) - 2.65) < 0.005, "2284 arrondi")
# ---- 2285
ok(solve(Eq(x + 2, 2 * x - 1), x) == [3] and (x + 2).subs(x, 3) == 5, "2285 intersection")
ok((x + 2).subs(x, 5) == 7 and (2 * x - 1).subs(x, 5) == 9, "2285 x=5")
# ---- 2286
f = 4 - x**2
ok([f.subs(x, v) for v in range(-3, 4)] == [-5, 0, 3, 4, 3, 0, -5], "2286 tableau")
ok(f.subs(x, R(1, 2)) == R(15, 4) and (4 + 3) / 2 == 3.5, "2286 f(0,5)")
# ---- 2288
f = x**2 - 2 * x - 3
ok(f.subs(x, 4) == 5 and f.subs(x, 0) == -3 and f.subs(x, 2) == -3 and f.subs(x, 1) == -4, "2288 valeurs")
ok(expand((x + 1) * (x - 3)) == f and antecedents(f, 0) == [-1, 3], "2288 factorisation")
ok(antecedents(f, -5) == [], "2288 -5")
ok(f.subs(x, -2) == 5, "2288 extrémité")
# ---- 2289
V = R(8, 10) * x
ok(V.subs(x, R(12, 10)) == R(96, 100) and antecedents(V, R(6, 10)) == [R(3, 4)] and V.subs(x, R(3, 2)) == R(12, 10), "2289")
# ---- 2290
P = lambda k: min(2 * k, 10)
ok((P(3), P(5), P(8)) == (6, 10, 10) and [P(k) for k in (1, 2, 4, 6, 10)] == [2, 4, 8, 10, 10], "2290 valeurs")
ok([k for k in range(13) if P(k) == 10] == list(range(5, 13)) and [k for k in range(13) if P(k) == 7] == [], "2290 antécédents")
# ---- 2291
A = x * (20 - x)
ok(A.subs(x, 3) == 51 and A.subs(x, 17) == 51 and A.subs(x, 10) == 100, "2291")
# ---- 2292
ok(600 / 10 == 60 and 600 / 12 == 50 and 60 * 60 / 1000 == 3.6, "2292 vitesses")
ok(R(300, 60) == 5 and 15 + R(300, 50) == 21, "2292 instants 300 m")
# ---- 2293
f = (x - 2) * (3 * x + 6)
ok(expand(f) == 3 * x**2 - 12 and f.subs(x, 0) == -12 and f.subs(x, -1) == -9, "2293 valeurs")
ok(antecedents(f, 0) == [-2, 2] and antecedents(f, -12) == [0], "2293 antécédents")
# ---- 2294
h = 80 - 5 * x**2
ok([h.subs(x, v) for v in range(5)] == [80, 75, 60, 35, 0] and h.subs(x, 5) == -45, "2294 valeurs")
ok(antecedents(h, 0) == [-4, 4], "2294 sol")
# ---- 2295
f, g = 2 * x + 3, x + 7
ok(f.subs(x, 4) == g.subs(x, 4) == 11 and solve(Eq(f, g), x) == [4], "2295 égalité")
ok((f.subs(x, 2), g.subs(x, 2), f.subs(x, 10), g.subs(x, 10)) == (7, 9, 23, 17), "2295 comparaison")
ok(antecedents(f, 15) == [6] and antecedents(g, 15) == [8], "2295 budget")

print(f"verif_240 : {n_ok} contrôles, tout est juste.")
