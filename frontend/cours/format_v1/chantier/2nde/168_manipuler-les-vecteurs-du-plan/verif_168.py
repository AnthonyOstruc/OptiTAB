# -*- coding: utf-8 -*-
"""Vérification de tous les résultats de la notion 168 (vecteurs du plan, Seconde).

Lancer : python verif_168.py  → « OK : n contrôles » ou AssertionError.
"""
from fractions import Fraction as F
import sympy as sp

N = 0


def ok(cond, msg=""):
    global N
    assert cond, msg
    N += 1


def vec(a, b):
    return (b[0] - a[0], b[1] - a[1])


def add(*vs):
    return (sum(v[0] for v in vs), sum(v[1] for v in vs))


def mul(k, v):
    return (k * v[0], k * v[1])


def det(u, v):
    return u[0] * v[1] - v[0] * u[1]


def n2(v):
    return v[0] ** 2 + v[1] ** 2


def mil(a, b):
    return (F(a[0] + b[0], 2), F(a[1] + b[1], 2))


def trans(p, v):
    return (p[0] + v[0], p[1] + v[1])


# ------------------------------------------------------------------ cours / fiche
A, B = (1, 1), (5, 4)
ok(vec(A, B) == (4, 3)); ok(n2(vec(A, B)) == 25); ok(mil(A, B) == (3, F(5, 2)))
A, B, C = (1, 1), (3, 2), (7, 4)
ok(vec(A, B) == (2, 1)); ok(vec(A, C) == (6, 3)); ok(det(vec(A, B), vec(A, C)) == 0)
ok(mul(3, vec(A, B)) == vec(A, C))
# figure base : u = 3i + 2j
ok(n2((3, 2)) == 13)
# figure produit : u(2;1), 2u, -1,5u
ok(mul(F(-3, 2), (2, 1)) == (-3, F(-3, 2)))
# exemple parallélisme du cours : E(0;3), F(4;5) ; EF(4;2) = 2 AB
E, Fp = (0, 3), (4, 5)
ok(vec(E, Fp) == (4, 2)); ok(det(vec((1, 1), (3, 2)), vec(E, Fp)) == 0)
ok(det(vec((1, 1), (3, 2)), vec((1, 1), E)) != 0)  # E hors de (AB) : droites distinctes

# ------------------------------------------------------------------ 1966
u, v, w = (3, -1), (-2, 4), (6, -2)
ok(add(u, v) == (1, 3)); ok(mul(-3, v) == (6, -12))
ok(n2(u) == 10); ok(n2(v) == 20 and sp.sqrt(20) == 2 * sp.sqrt(5))
ok(mul(2, u) == w); ok(det(u, w) == 0); ok(sp.sqrt(n2(w)) == 2 * sp.sqrt(10))

# ------------------------------------------------------------------ 1967 (formel : points au hasard)
import random
random.seed(1)
for _ in range(20):
    P = {c: (random.randint(-9, 9), random.randint(-9, 9)) for c in "ABCDE"}
    V = lambda x, y: vec(P[x], P[y])
    neg = lambda t: mul(-1, t)
    ok(add(V("A", "B"), V("B", "C"), neg(V("A", "C"))) == (0, 0))
    ok(add(V("A", "D"), V("D", "C"), V("C", "B")) == V("A", "B"))
    ok(add(V("A", "B"), neg(V("D", "B")), V("D", "A")) == (0, 0))
    ok(add(mul(2, V("A", "B")), V("B", "C"), V("C", "A")) == V("A", "B"))
    ok(add(V("A", "E"), V("E", "D"), neg(V("A", "D"))) == (0, 0))

# ------------------------------------------------------------------ 1956
A, B, C = (1, -2), (4, 1), (-2, 3)
ok(vec(A, B) == (3, 3)); D = trans(C, vec(A, B)); ok(D == (1, 6))
ok(vec(C, D) == vec(A, B)); ok(vec(B, A) == (-3, -3))
ok(mil(A, D) == mil(B, C))  # ABDC parallélogramme : diagonales [AD] et [BC]
ok(det(vec(A, B), vec(A, C)) == 24)  # non aplati
ok(vec(A, (1, -2)) == (0, 0))  # E = A

# ------------------------------------------------------------------ 1963
A, B, C = (0, 1), (4, 3), (2, -1)
ok(n2(vec(A, B)) == 20); ok(n2(vec(B, C)) == 20); ok(n2(vec(A, C)) == 8)
ok(20 + 8 != 20 and 20 + 20 != 8)
M = mil(A, C); ok(M == (1, 0)); ok(n2(vec(B, M)) == 18 and sp.sqrt(18) == 3 * sp.sqrt(2))
# BM médiane du triangle isocèle en B : (BM) perpendiculaire à (AC) (produit scalaire nul)
bm, ac = vec(B, M), vec(A, C)
ok(bm[0] * ac[0] + bm[1] * ac[1] == 0)
ok(n2(bm) + n2(vec(A, M)) == n2(vec(A, B)))  # Pythagore dans ABM : 18 + 2 = 20

# ------------------------------------------------------------------ 1964
A, B, C = (2, 1), (6, 3), (4, -1)
ok(vec(A, B) == (4, 2)); ok(vec(B, C) == (-2, -4))
D = trans(A, vec(B, C)); ok(D == (0, -3))
ok(vec(A, D) == vec(B, C)); ok(vec(D, C) == vec(A, B))
ok(mil(A, C) == (3, 0)); ok(mil(B, D) == (3, 0))
ok(det(vec(A, B), vec(A, C)) != 0)  # A, B, C non alignés

# ------------------------------------------------------------------ 1965
A, B = (1, -3), (7, 1)
ok(vec(A, B) == (6, 4)); ok(n2(vec(A, B)) == 52 and sp.sqrt(52) == 2 * sp.sqrt(13))
M = mil(A, B); ok(M == (4, -1)); ok(vec(A, M) == (3, 2) == vec(M, B)); ok(n2(vec(A, M)) == 13)

# ------------------------------------------------------------------ 1962
k = sp.symbols("k")
A, B, C, D = (-1, 1), (2, 3), (4, 0), (1, -2)
AB = vec(A, B); ok(AB == (3, 2))
AP = (k + 1, k + 4 - 1); ok(sp.expand(det(AB, AP)) == k + 7)
ok(sp.solve(det(AB, AP), k) == [-7]); P = (-7, -3)
ok(vec(A, P) == mul(-2, AB))
ok(vec(C, D) == (-3, -2)); ok(det(AB, vec(C, D)) == 0)
ok(det(AB, vec(A, C)) == -13)  # C hors de (AB) : parallèles distinctes

# ------------------------------------------------------------------ 1961
t = sp.symbols("t")
A, B, C = (-2, 0), (1, 3), (4, 2)
AB = vec(A, B); ok(AB == (3, 3)); CD = (t - 4, -3)
ok(sp.expand(det(AB, CD)) == 3 - 3 * t); ok(sp.solve(det(AB, CD), t) == [1])
ok(vec(C, (1, -1)) == (-3, -3) == mul(-1, AB))
ok(vec(A, C) == (6, 2)); ok(det(AB, vec(A, C)) == -12)  # C hors de (AB)

# ------------------------------------------------------------------ 1960 (repère quelconque)
for A, B, C in [((0, 0), (5, 1), (1, 4)), ((1, 2), (7, -1), (3, 6))]:
    M = trans(A, mul(F(2, 5), vec(A, B))); N_ = trans(A, mul(F(2, 5), vec(A, C)))
    ok(vec(M, N_) == mul(F(2, 5), vec(B, C)))
    ok(vec(M, A) == mul(F(-2, 5), vec(A, B)))

# ------------------------------------------------------------------ 1959
S = (-3, 2); u, v, w = (5, -1), (-2, 4), (1, -3)
A = trans(S, u); B = trans(A, v); T = trans(B, w)
ok((A, B, T) == ((2, 1), (0, 5), (1, 2)))
ok(vec(S, T) == (4, 0) == add(u, v, w)); ok(n2(vec(S, T)) == 16)
ok(det(u, v) == 18)
# longueur du trajet réel : sqrt(26) + sqrt(20) + sqrt(10) > 4
L = sp.sqrt(26) + sp.sqrt(20) + sp.sqrt(10)
ok(round(float(L), 1) == 12.7)

# ------------------------------------------------------------------ 1957 (symbolique)
x, y, xp, yp, kk = sp.symbols("x y xp yp kk")
ok(sp.expand(det((kk * xp, kk * yp), (xp, yp))) == 0)

# ------------------------------------------------------------------ 1958 (figure : A(0;0), B(5;1), C(1;5))
for A, B, C in [((0, 0), (5, 1), (1, 5)), ((2, -1), (6, 3), (-1, 4))]:
    D = trans(B, mul(F(1, 3), vec(B, C)))
    ok(vec(A, D) == add(mul(F(2, 3), vec(A, B)), mul(F(1, 3), vec(A, C))))
    E = trans(A, add(mul(F(4, 3), vec(A, B)), mul(F(2, 3), vec(A, C))))
    ok(vec(A, E) == mul(2, vec(A, D))); ok(mil(A, E) == D)
A, B, C = (0, 0), (5, 1), (1, 5)
ok(trans(B, mul(F(1, 3), vec(B, C))) == (F(11, 3), F(7, 3)))

# ------------------------------------------------------------------ nouveau-1 (lecture graphique)
A, B, C, D, E, Fp = (-4, 1), (-1, 3), (2, -1), (5, 1), (1, -3), (-2, -5)
ok(vec(A, B) == (3, 2)); ok(vec(C, D) == (3, 2)); ok(vec(E, Fp) == (-3, -2))
ok(vec(E, Fp) == mul(-1, vec(A, B)))
ok(mil(A, D) == mil(B, C))  # ABDC parallélogramme
ok(det(vec(A, B), vec(A, C)) != 0)  # non aplati
ok(n2(vec(A, B)) == 13)

# ------------------------------------------------------------------ nouveau-2 (construction)
u, v = (3, 1), (-1, 2)
ok(add(u, v) == (2, 3)); ok(add(u, mul(-1, v)) == (4, -1)); ok(mul(2, u) == (6, 2))
O = (0, 0)
ok(trans(trans(O, u), v) == (2, 3)); ok(trans(trans(O, u), mul(-1, v)) == (4, -1))
ok(mil(O, (2, 3)) == mil((3, 1), (-1, 2)))  # OUMV parallélogramme
wv = (4, 6); ok(det(add(u, v), wv) == 0); ok(mul(2, add(u, v)) == wv)
ok(det(u, v) == 7)
ok(n2(add(u, v)) == 13 and n2(u) == 10 and n2(v) == 5)
ok(sp.sqrt(13) < sp.sqrt(10) + sp.sqrt(5))

print("OK :", N, "contrôles")
