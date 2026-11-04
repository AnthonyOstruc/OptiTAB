# -*- coding: utf-8 -*-
"""Vérification (sympy) de tous les calculs de la notion 161 « Variables aléatoires réelles ».

    python verif_variables_aleatoires.py

Chaque valeur écrite dans le cours, la fiche et les exercices est recalculée ;
les simulations citées (graines fixes) sont rejouées avec les mêmes fonctions
que les figures (figures/figures.py).
"""
import importlib.util
import math
import random
from fractions import Fraction
from itertools import product
from pathlib import Path

from sympy import Rational as R, sqrt, nsimplify, N

ICI = Path(__file__).resolve().parent
OK = [0]
ERR = []


def check(nom, obtenu, attendu, tol=None):
    if tol is None and isinstance(obtenu, (list, tuple, bool)):
        bon = list(obtenu) == list(attendu) if not isinstance(obtenu, bool) else obtenu == attendu
    elif tol is None:
        bon = nsimplify(obtenu) == nsimplify(attendu)
    else:
        bon = abs(float(obtenu) - float(attendu)) <= tol
    if bon:
        OK[0] += 1
    else:
        ERR.append(f"{nom} : obtenu {obtenu}, attendu {attendu}")


def loi(d):
    s = sum(d.values())
    assert s == 1, f"somme {s}"
    return d


def E(d):
    return sum(p * x for x, p in d.items())


def E2(d):
    return sum(p * x ** 2 for x, p in d.items())


def V(d):
    m = E(d)
    v1 = sum(p * (x - m) ** 2 for x, p in d.items())
    v2 = E2(d) - m ** 2
    assert v1 == v2
    return v1


def loi_de(issues, f):
    """issues équiprobables -> loi de f(issue)."""
    d = {}
    n = len(issues)
    for i in issues:
        d[f(i)] = d.get(f(i), 0) + R(1, n)
    return loi(d)


DE = range(1, 7)
DEUX = list(product(DE, DE))

# ================================================================ COURS
X = loi_de(list(DE), lambda d: 5 if d == 6 else (1 if d % 2 == 0 else -2))
check("cours loi -2", X[-2], R(1, 2)); check("cours loi 1", X[1], R(1, 3)); check("cours loi 5", X[5], R(1, 6))
check("cours P(X<=1)", X[-2] + X[1], R(5, 6))
check("cours E", E(X), R(1, 6))
check("cours E arrondi", N(E(X)), 0.17, 0.005)
check("cours E(X2)", E2(X), R(13, 2))
check("cours V", V(X), R(233, 36))
check("cours V arrondi", N(V(X)), 6.47, 0.005)
check("cours sigma", sqrt(V(X)), sqrt(233) / 6)
check("cours sigma arrondi", N(sqrt(V(X))), 2.54, 0.005)
check("cours sigma 3 déc", N(sqrt(V(X))), 2.544, 0.0005)
check("cours 234/36", R(13, 2), R(234, 36))
# Y = 2X + 1
check("cours E(Y)", 2 * E(X) + 1, R(4, 3))
check("cours V(Y)", 4 * V(X), R(233, 9))
check("cours V(Y) arrondi", N(4 * V(X)), 25.9, 0.05)
check("cours sigma(Y)", N(2 * sqrt(V(X))), 5.09, 0.005)
Yd = {2 * x + 1: p for x, p in X.items()}
check("cours V(Y) direct", V(Yd), R(233, 9))
# urne 3R 2B sans remise
def sans_remise(r, b):
    tot = r + b
    return {
        2: R(r, tot) * R(r - 1, tot - 1),
        1: R(r, tot) * R(b, tot - 1) + R(b, tot) * R(r, tot - 1),
        0: R(b, tot) * R(b - 1, tot - 1),
    }
U = loi(sans_remise(3, 2))
check("urne P0", U[0], R(1, 10)); check("urne P1", U[1], R(3, 5)); check("urne P2", U[2], R(3, 10))
check("urne R1B2", R(3, 5) * R(2, 4), R(3, 10))
# dispersion A / B
A = loi({-1: R(1, 2), 1: R(1, 2)}); B = loi({-3: R(1, 2), 3: R(1, 2)})
check("dispersion E(A)", E(A), 0); check("dispersion E(B)", E(B), 0)
check("dispersion sigma A", sqrt(V(A)), 1); check("dispersion sigma B", sqrt(V(B)), 3)
# forain
G = loi({6: R(1, 6), 3: R(1, 3), 0: R(1, 2)})
check("forain E(G)", E(G), 2)
check("forain mise 2,50", E(G) - R(5, 2), R(-1, 2))
# indicateurs Python (flottants)
from math import sqrt as fsqrt
def indicateurs(x, p):
    Ef = 0
    for i in range(len(x)):
        Ef = Ef + p[i] * x[i]
    Vf = 0
    for i in range(len(x)):
        ecart = x[i] - Ef
        Vf = Vf + p[i] * ecart ** 2
    return Ef, Vf, fsqrt(Vf)
e, v, s = indicateurs([-2, 1, 5], [1 / 2, 1 / 3, 1 / 6])
check("indicateurs E", e, 0.1667, 0.00005); check("indicateurs V", v, 6.4722, 0.00005); check("indicateurs s", s, 2.5441, 0.00005)
# 2 sigma / racine(n)
check("cours 2s/10", N(2 * sqrt(V(X)) / 10), 0.509, 0.0005)
check("cours borne basse", N(R(1, 6) - 2 * sqrt(V(X)) / 10), -0.34, 0.005)
check("cours borne haute", N(R(1, 6) + 2 * sqrt(V(X)) / 10), 0.68, 0.005)

# simulations des figures (mêmes fonctions)
spec = importlib.util.spec_from_file_location("figs", ICI / "figures" / "figures.py")
figs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(figs)
moy = figs.moyennes_cumulees()
check("simulation : 2000 points", len(moy), 2000)
ms = figs.moyennes_echantillons_cours()
mu, sig = 1 / 6, math.sqrt(233) / 6
dedans = sum(abs(m - mu) <= 2 * sig / 10 for m in ms)
check("cours 96 moyennes sur 100", dedans, 96)
check("cours 100 échantillons", len(ms), 100)

# ================================================================ 1331
Xd = loi_de(list(DE), lambda d: d)
check("1331 P(X<=4)", sum(p for x, p in Xd.items() if x <= 4), R(2, 3))
check("1331 P(X>=5)", sum(p for x, p in Xd.items() if x >= 5), R(1, 3))
S = loi_de(DEUX, lambda c: c[0] + c[1])
check("1331 valeurs Y", sorted(S), list(range(2, 13)))
check("1331 P(Y=7)", S[7], R(1, 6))
check("1331 P(Y<=5)", sum(p for x, p in S.items() if x <= 5), R(5, 18))
Z3 = loi_de(list(product("PF", repeat=3)), lambda t: t.count("P"))
check("1331 Z", [Z3[k] for k in range(4)], [R(1, 8), R(3, 8), R(3, 8), R(1, 8)])
check("1331 P(Z>=2)", Z3[2] + Z3[3], R(1, 2))

# ================================================================ 1335
check("1335 P(X>=10)", sum(p for x, p in S.items() if x >= 10), R(1, 6))
for s_ in range(2, 13):
    check(f"1335 loi somme {s_}", S[s_], R(s_ - 1 if s_ <= 7 else 13 - s_, 36))
Y = loi({-2: R(2, 10), 0: R(3, 10), 3: R(4, 10), 5: R(1, 10)})
check("1335 E(Y)", E(Y), R(13, 10)); check("1335 E(Y2)", E2(Y), R(69, 10)); check("1335 V(Y)", V(Y), R(521, 100))
check("1335 sigma(Y)", N(sqrt(V(Y))), 2.28, 0.005)
G = loi_de(list(DE), lambda d: 8 if d == 6 else (2 if d in (2, 4) else -3))
check("1335 loi G", (G[-3], G[2], G[8]), (R(1, 2), R(1, 3), R(1, 6)))
check("1335 E(G)", E(G), R(1, 2)); check("1335 E(G2)", E2(G), R(33, 2)); check("1335 V(G)", V(G), R(65, 4))
check("1335 99/6", E2(G), R(99, 6))
check("1335 sigma(G)", N(sqrt(V(G))), 4.03, 0.005)

# ================================================================ 1336
J = {2: R(2, 6) * R(1, 5), 1: R(2, 6) * R(4, 5) + R(4, 6) * R(2, 5), 0: R(4, 6) * R(3, 5)}
loi(J)
check("1336 P(X=2)", J[2], R(1, 15)); check("1336 P(X=1)", J[1], R(8, 15)); check("1336 P(X=0)", J[0], R(2, 5))
check("1336 W1L2", R(2, 6) * R(4, 5), R(8, 30))
check("1336 P(X>=1)", 1 - J[0], R(3, 5)); check("1336 E(X)", E(J), R(2, 3))
Y = loi({-1: R(1, 3), 2: R(1, 2), 5: R(1, 6)})
check("1336 E(Y)", E(Y), R(3, 2)); check("1336 E(Y2)", E2(Y), R(13, 2)); check("1336 V(Y)", V(Y), R(17, 4))
check("1336 sigma(Y)", N(sqrt(V(Y))), 2.06, 0.005)
Zd = {2 * y + 3: p for y, p in Y.items()}
check("1336 E(Z)", E(Zd), 6); check("1336 V(Z)", V(Zd), 17); check("1336 sigma(Z)", N(sqrt(17)), 4.12, 0.005)
G = loi_de(DEUX, lambda c: 10 if sum(c) in (7, 11) else (-5 if sum(c) in (2, 3, 12) else 1))
check("1336 loi G", (G[-5], G[1], G[10]), (R(1, 9), R(2, 3), R(2, 9)))
check("1336 E(G)", E(G), R(7, 3)); check("1336 E(G) arrondi", N(E(G)), 2.33, 0.005)

# ================================================================ 1339
M = loi_de(DEUX, lambda c: max(c))
for k in range(1, 7):
    check(f"1339 max {k}", M[k], R(2 * k - 1, 36))
check("1339 E(max)", E(M), R(161, 36)); check("1339 E(max) arrondi", N(E(M)), 4.47, 0.005)
Y = loi({-2: R(1, 10), 0: R(4, 10), 1: R(3, 10), 4: R(2, 10)})
check("1339 P(Y<=0)", Y[-2] + Y[0], R(1, 2)); check("1339 P(Y>1)", Y[4], R(1, 5))
check("1339 E(Y)", E(Y), R(9, 10)); check("1339 E(Y2)", E2(Y), R(39, 10)); check("1339 V(Y)", V(Y), R(309, 100))
check("1339 sigma(Y)", N(sqrt(V(Y))), 1.76, 0.005)
Zd = {-y + 2: p for y, p in Y.items()}
check("1339 E(Z)", E(Zd), R(11, 10)); check("1339 V(Z)", V(Zd), R(309, 100))
G = loi_de(list(DE), lambda d: 8 if d == 6 else (2 if d in (4, 5) else -1))
check("1339 E(G)", E(G), R(3, 2)); check("1339 E(G2)", E2(G), R(25, 2)); check("1339 V(G)", V(G), R(41, 4))
check("1339 sigma(G)", N(sqrt(V(G))), 3.20, 0.005)
check("1339 3,2^2", R(32, 10) ** 2, R(1024, 100))
check("1339 sigma != 3,2", sqrt(R(41, 4)) != R(16, 5), True)

# ================================================================ 1333
X3 = loi_de(list(DE), lambda d: 10 if d == 6 else (3 if d in (2, 4) else -2))
check("1333 E(X)", E(X3), R(5, 3)); check("1333 E(X) arrondi", N(E(X3)), 1.67, 0.005)
W = {2: R(4, 10) * R(3, 9), 1: R(4, 10) * R(6, 9) + R(6, 10) * R(4, 9), 0: R(6, 10) * R(5, 9)}
loi(W)
check("1333 Y", (W[0], W[1], W[2]), (R(1, 3), R(8, 15), R(2, 15)))
check("1333 B1N2", R(4, 10) * R(6, 9), R(24, 90))
check("1333 E(Y)", E(W), R(4, 5))
P = loi_de(DEUX, lambda c: c[0] * c[1])
check("1333 E(produit)", E(P), R(49, 4))
check("1333 somme produits", sum(a * b for a, b in DEUX), 441)
for i in DE:
    check(f"1333 ligne {i}", sum(i * j for j in DE), 21 * i)
check("1333 E(N)", E(P) - 10, R(9, 4))

# ================================================================ 1332
p = 1 - R(1, 10) - R(25, 100) - R(4, 10)
check("1332 p", p, R(1, 4))
L = loi({0: R(1, 10), 1: R(1, 4), 2: p, 3: R(2, 5)})
check("1332 P(X>=2)", L[2] + L[3], R(65, 100)); check("1332 P(X<2)", L[0] + L[1], R(35, 100))
Yu = loi({5: R(3, 6), 2: R(2, 6), 10: R(1, 6)})
check("1332 P(Y>=5)", Yu[5] + Yu[10], R(2, 3))
Ec = loi_de(DEUX, lambda c: abs(c[0] - c[1]))
check("1332 écarts", [Ec[k] * 36 for k in range(6)], [6, 10, 8, 6, 4, 2])
check("1332 écarts simplifiés", [Ec[k] for k in range(6)], [R(1, 6), R(5, 18), R(2, 9), R(1, 6), R(1, 9), R(1, 18)])
check("1332 P(Z<=2)", Ec[0] + Ec[1] + Ec[2], R(2, 3))

# ================================================================ 1334
from sympy import symbols, solve
a = symbols("a")
EG = R(1, 2) * (-4) + R(1, 3) * 2 + R(1, 6) * a
check("1334 E(G)", EG - (a / 6 - R(4, 3)), 0)
check("1334 a équitable", solve(EG, a)[0], 8)
check("1334 a mise 1", solve(EG - 1, a)[0], 14)
G14 = loi({-4: R(1, 2), 2: R(1, 3), 14: R(1, 6)})
check("1334 E(G) a=14", E(G14), 1); check("1334 E(G2) a=14", E2(G14), 42); check("1334 V a=14", V(G14), 41)
check("1334 sigma", N(sqrt(41)), 6.40, 0.005)
check("1334 98/3", R(1, 6) * 196, R(98, 3))
NA = loi({-2: R(9, 10), 8: R(1, 10)}); NB = loi({-3: R(85, 100), 12: R(15, 100)}); NC = loi({-5: R(85, 100), 25: R(15, 100)})
check("1334 E(NA)", E(NA), -1); check("1334 E(NB)", E(NB), R(-3, 4)); check("1334 E(NC)", E(NC), R(-1, 2))
check("1334 E(NA2)", E2(NA), 10); check("1334 V(NA)", V(NA), 9)
check("1334 E(NC2)", E2(NC), 115); check("1334 V(NC)", V(NC), R(11475, 100))
check("1334 sigma NC", N(sqrt(V(NC))), 10.71, 0.005)

# ================================================================ 1337
X7 = loi({0: R(4, 10), 2: R(3, 10), 5: R(3, 10)})
check("1337 E", E(X7), R(21, 10)); check("1337 E2", E2(X7), R(87, 10)); check("1337 V", V(X7), R(429, 100))
check("1337 sigma", N(sqrt(V(X7))), 2.07, 0.005)
check("1337 E(3X-2)", 3 * E(X7) - 2, R(43, 10)); check("1337 V(3X-2)", 9 * V(X7), R(3861, 100))
G = loi_de(DEUX, lambda c: 12 if sum(c) == 7 else (5 if c[0] == c[1] else -2))
check("1337 doubles jamais 7", any(c[0] == c[1] and sum(c) == 7 for c in DEUX), False)
check("1337 loi", (G[-2], G[5], G[12]), (R(2, 3), R(1, 6), R(1, 6)))
check("1337 E(G)", E(G), R(3, 2)); check("1337 mise 2", E(G) - 2, R(-1, 2))
check("1337 ex3", (2 * 4 + 1, 4 * 9, 6), (9, 36, 6))

# ================================================================ 1338
X8 = loi_de(list(DE), lambda d: -3 if d <= 2 else (1 if d <= 4 else 4))
check("1338 E", E(X8), R(2, 3)); check("1338 E2", E2(X8), R(26, 3)); check("1338 V", V(X8), R(74, 9))
check("1338 V arrondi", N(V(X8)), 8.22, 0.005); check("1338 sigma", N(sqrt(V(X8))), 2.87, 0.005)
check("1338 A2", (-2 * 5 + 3, 4 * 16, 2 * 4), (-7, 64, 8))
Zr = loi(sans_remise(5, 5))
check("1338 Z", (Zr[0], Zr[1], Zr[2]), (R(2, 9), R(5, 9), R(2, 9)))
check("1338 E", E(Zr), 1); check("1338 E2", E2(Zr), R(13, 9)); check("1338 V", V(Zr), R(4, 9)); check("1338 sigma", sqrt(V(Zr)), R(2, 3))

# ================================================================ 1340
X0 = loi({-1: R(1, 4), 2: R(1, 2), 4: R(1, 4)})
check("1340 E", E(X0), R(7, 4)); check("1340 E2", E2(X0), R(25, 4)); check("1340 V", V(X0), R(51, 16))
check("1340 V arrondi", N(V(X0)), 3.19, 0.005); check("1340 sigma", N(sqrt(V(X0))), 1.79, 0.005)
check("1340 E(3X-1)", 3 * E(X0) - 1, R(17, 4)); check("1340 V(3X-1)", 9 * V(X0), R(459, 16))
check("1340 V(3X-1) arrondi", N(9 * V(X0)), 28.69, 0.005)
Gc = loi_de(list(range(1, 33)), lambda c: 6 if c <= 4 else (2 if c <= 16 else -2))
check("1340 loi", (Gc[-2], Gc[2], Gc[6]), (R(1, 2), R(3, 8), R(1, 8)))
check("1340 E(G)", E(Gc), R(1, 2)); check("1340 E(G2)", E2(Gc), 8); check("1340 V(G)", V(Gc), R(31, 4))
check("1340 sigma", N(sqrt(V(Gc))), 2.78, 0.005)
check("1340 E(N)", E(Gc) - 1, R(-1, 2)); check("1340 200 parties", 200 * R(1, 2), 100)
r = random.Random(2)
def partie_c():
    c = r.randint(1, 32)
    return 6 if c <= 4 else (2 if c <= 16 else -2)
res = [sum(partie_c() for _ in range(n)) / n for n in (10, 100, 10000)]
check("1340 simulation n=10", res[0], 1.6, 1e-9); check("1340 simulation n=100", res[1], 0.64, 1e-9)
check("1340 simulation n=10000", res[2], 0.5036, 1e-9)

# ================================================================ 1341
X1 = loi({0: R(2, 10), 3: R(5, 10), 6: R(3, 10)})
check("1341 E", E(X1), R(33, 10)); check("1341 E2", E2(X1), R(153, 10)); check("1341 V", V(X1), R(441, 100))
check("1341 sigma", sqrt(V(X1)), R(21, 10)); check("1341 E(4X-5)", 4 * E(X1) - 5, R(82, 10))
check("1341 B", (2 * 3 + 1, 4 * 25, 10, -3 + 6, 25, 5), (7, 100, 10, 3, 25, 5))
G = loi_de(DEUX, lambda c: 15 if sum(c) == 7 else (2 if sum(c) % 2 == 0 else -3))
check("1341 loi", (G[-3], G[2], G[15]), (R(1, 3), R(1, 2), R(1, 6)))
check("1341 sommes paires", sum(1 for c in DEUX if sum(c) % 2 == 0), 18)
check("1341 E", E(G), R(5, 2)); check("1341 E2", E2(G), R(85, 2)); check("1341 V", V(G), R(145, 4))
check("1341 sigma", N(sqrt(V(G))), 6.02, 0.005)

# ================================================================ nouveau-1
T = loi({45: R(1, 20), 5: R(4, 20), -5: R(15, 20)})
check("n1 P(X>0)", T[5] + T[45], R(1, 4)); check("n1 P(X>=5)", T[5] + T[45], R(1, 4))
check("n1 P(X<=5)", T[5] + T[-5], R(19, 20)); check("n1 E", E(T), R(-1, 2))
check("n1 bénéfice", (20 * 5 - (50 + 4 * 10)) / R(20), R(1, 2))

# ================================================================ nouveau-2
X2 = loi({0: R(1, 2), 10: R(3, 10), 20: R(1, 5)})
check("n2 E", E(X2), 7); check("n2 V", V(X2), 61); check("n2 E2", E2(X2), 110)
check("n2 sigma", N(sqrt(61)), 7.81, 0.005)
e, v, s = indicateurs([0, 10, 20], [0.5, 0.3, 0.2])
check("n2 python E", e, 7, 1e-9); check("n2 python V", v, 61, 1e-9)
check("n2 flottants", repr(0.7 + 0.2 + 0.1), "0.9999999999999999")
def indicateurs2(valeurs, probas):
    Ef = 0
    E2f = 0
    for i in range(len(valeurs)):
        Ef = Ef + probas[i] * valeurs[i]
        E2f = E2f + probas[i] * valeurs[i] ** 2
    Vf = E2f - Ef ** 2
    return Ef, Vf, fsqrt(Vf)
e, v, s = indicateurs2([0, 10, 20], [0.5, 0.3, 0.2])
check("n2 indicateurs2", (round(e, 6), round(v, 6), round(s, 2)), (7, 61, 7.81))
def est_une_loi(p):
    for q in p:
        if q < 0 or q > 1:
            return False
    ecart = abs(sum(p) - 1)
    return ecart < 1e-9
check("n2 est_une_loi", (est_une_loi([0.7, 0.2, 0.1]), est_une_loi([0.5, 0.6]), est_une_loi([1.2, -0.2])), (True, False, False))

# ================================================================ nouveau-3
X3 = loi_de(list(range(1, 11)), lambda t: 4 if t <= 2 else (1 if t <= 5 else -1))
check("n3 E", E(X3), R(3, 5)); check("n3 E2", E2(X3), 4); check("n3 V", V(X3), R(364, 100))
check("n3 sigma", N(sqrt(V(X3))), 1.91, 0.005)
r = random.Random(4)
def partie3():
    t = r.randint(1, 10)
    return 4 if t <= 2 else (1 if t <= 5 else -1)
res = [sum(partie3() for _ in range(n)) / n for n in (10, 100, 1000, 10000)]
for got, att in zip(res, (1.6, 0.72, 0.609, 0.5948)):
    check(f"n3 simulation {att}", got, att, 1e-9)
for got, att in zip(res, (1, 0.12, 0.009, 0.0052)):
    check(f"n3 écart {att}", abs(got - 0.6), att, 1e-9)
check("n3 2s/100", N(2 * sqrt(V(X3)) / 100), 0.038, 0.0005)

# ================================================================ nouveau-4
D = loi_de(list(DE), lambda d: d)
check("n4 mu", E(D), R(7, 2)); check("n4 E2", E2(D), R(91, 6)); check("n4 V", V(D), R(35, 12))
check("n4 sigma", N(sqrt(V(D))), 1.708, 0.0005)
check("n4 2s/10", N(2 * sqrt(V(D)) / 10), 0.342, 0.0005)
check("n4 borne basse", N(R(7, 2) - 2 * sqrt(V(D)) / 10), 3.158, 0.0005)
check("n4 borne haute", N(R(7, 2) + 2 * sqrt(V(D)) / 10), 3.842, 0.0005)
check("n4 2s/20", N(2 * sqrt(V(D)) / 20), 0.171, 0.0005)
check("n4 bornes 400 bas", N(R(7, 2) - 2 * sqrt(V(D)) / 20), 3.329, 0.0005)
check("n4 bornes 400 haut", N(R(7, 2) + 2 * sqrt(V(D)) / 20), 3.671, 0.0005)
md = figs.moyennes_echantillons_de()
sig = math.sqrt(35 / 12)
hors = sum(abs(m - 3.5) > 2 * sig / 10 for m in md)
check("n4 200 échantillons", len(md), 200)
check("n4 6 hors bande", hors, 6)
check("n4 proportion", (200 - hors) / 200, 0.97, 1e-12)
h4 = 2 * sig / 10
dessus = sorted(m for m in md if m - 3.5 > h4)
dessous = [m for m in md if 3.5 - m > h4]
check("n4 4 juste au-dessus", sum(1 for m in dessus if m < 3.9), 4)
check("n4 1 nettement au-dessus (proche de 4)", [round(m, 1) for m in dessus if m >= 3.9], [4.0])
check("n4 1 au-dessous (proche de 3)", [round(m, 1) for m in dessous], [3.0])
# entonnoirs : chaque moyenne observée est dans son intervalle 0,6 ± 2σ/√n (resp. 0,5 ± …)
for n_, m_ in ((10, 1.6), (100, 0.72), (1000, 0.609), (10000, 0.5948)):
    check(f"n3 {n_} dans la barre", abs(m_ - 0.6) <= 2 * math.sqrt(3.64) / math.sqrt(n_), True)
for n_, m_ in ((10, 1.6), (100, 0.64), (10000, 0.5036)):
    check(f"1340 {n_} dans la barre", abs(m_ - 0.5) <= 2 * math.sqrt(7.75) / math.sqrt(n_), True)

# ================================================================ nouveau-5
A = loi_de(list(DE), lambda d: -1 if d <= 3 else 2)
B = loi_de(list(DE), lambda d: 8 if d == 6 else -1)
check("n5 E(A)", E(A), R(1, 2)); check("n5 E(B)", E(B), R(1, 2))
check("n5 E(A2)", E2(A), R(5, 2)); check("n5 V(A)", V(A), R(9, 4)); check("n5 sigma A", sqrt(V(A)), R(3, 2))
check("n5 E(B2)", E2(B), R(23, 2)); check("n5 V(B)", V(B), R(45, 4)); check("n5 sigma B", sqrt(V(B)), 3 * sqrt(5) / 2)
check("n5 sigma B arrondi", N(3 * sqrt(5) / 2), 3.35, 0.005)
check("n5 P(A>0)", A[2], R(1, 2)); check("n5 P(B>0)", B[8], R(1, 6))

print(f"{OK[0]} contrôles réussis, {len(ERR)} erreur(s)")
for e_ in ERR:
    print("  ERREUR", e_)
raise SystemExit(1 if ERR else 0)
