# -*- coding: utf-8 -*-
"""Vérification de tous les résultats de la notion « Sommes de variables aléatoires ».

    python verif_sommes-de-variables-aleatoires.py

Lois exactes (fractions), espérances et variances calculées par la définition,
lois de sommes par convolution (dés), lois binomiales exactes.
"""
from fractions import Fraction as Fr
from itertools import product
from math import comb, sqrt


def loi(valeurs_probas):
    d = {}
    for v, p in valeurs_probas:
        d[v] = d.get(v, 0) + p
    return d


def E(d):
    return sum(v * p for v, p in d.items())


def V(d):
    m = E(d)
    return sum(p * (v - m) ** 2 for v, p in d.items())


def somme(d1, d2):
    return loi((a + b, p * q) for (a, p), (b, q) in product(d1.items(), d2.items()))


def affine(d, a, b):
    return loi((a * v + b, p) for v, p in d.items())


def binom(n, p):
    return {k: comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)}


def ok(nom, val, attendu, tol=None):
    if tol is None:
        assert val == attendu, f"{nom} : {val} != {attendu}"
    else:
        assert abs(float(val) - attendu) <= tol, f"{nom} : {float(val)} != {attendu}"
    print(f"  ok  {nom} : {val if not isinstance(val, float) else round(val, 6)}")


DE = {k: Fr(1, 6) for k in range(1, 7)}
PIECE = {0: Fr(1, 2), 1: Fr(1, 2)}


def bern(p):
    return {0: 1 - p, 1: p}


print("== COURS / FICHE")
ok("E(dé)", E(DE), Fr(7, 2))
ok("V(dé)", V(DE), Fr(35, 12))
S2 = somme(DE, DE)
ok("E(2 dés)", E(S2), 7)
ok("V(2 dés)", V(S2), Fr(35, 6))
ok("V(2 dés) ≈ 5,83", float(V(S2)), 5.83, 0.005)
ok("P(S=7) = 6/36", S2[7], Fr(6, 36))
ok("loi 2 dés : P(S=k) = (6-|k-7|)/36", all(S2[k] == Fr(6 - abs(k - 7), 36) for k in range(2, 13)), True)
# E(2X - 3Y), V(2X - 3Y) avec E(X)=1, V(X)=4, E(Y)=-0,5, V(Y)=1 (indépendantes)
ok("E(2X-3Y)", 2 * 1 - 3 * Fr(-1, 2), Fr(7, 2))
ok("V(2X-3Y)", 4 * 4 + 9 * 1, 25)
ok("sigma(M_100) dé", sqrt(35 / 12) / 10, 0.171, 0.0005)
for n in (1, 4, 16, 100):
    print(f"      sigma(M_{n}) = {sqrt(35 / 12) / sqrt(n):.4f}")
ok("sigma(M_1)", sqrt(35 / 12), 1.708, 0.0005)
ok("sigma(M_4)", sqrt(35 / 12) / 2, 0.854, 0.0005)
ok("sigma(M_16)", sqrt(35 / 12) / 4, 0.427, 0.0005)
# Bernoulli et binomiale
p = Fr(3, 10)
ok("V(Bernoulli) = p(1-p)", V(bern(p)), p * (1 - p))
B = bern(p)
for _ in range(4):
    B = somme(B, bern(p)) if _ else somme(bern(p), bern(p))
ok("somme de 5 Bernoulli = B(5;p)", B == binom(5, p), True)
ok("E(B(5;0,3)) = np", E(binom(5, p)), 5 * p)
ok("V(B(5;0,3)) = np(1-p)", V(binom(5, p)), 5 * p * (1 - p))

print("== 1285 Additivité de la variance")
ok("Q1", V(S2), Fr(35, 6))
ok("Q1 sigma", sqrt(35 / 6), 2.42, 0.005)
ok("Q2", V(somme(PIECE, PIECE)), Fr(1, 2))
ok("Q3", V(somme(bern(Fr(2, 5)), bern(Fr(2, 5)))), Fr(12, 25))
ok("Q4", V(affine(DE, 3, 0)), Fr(105, 4))
ok("Q5 (déjà vu)", V(bern(Fr(1, 7))), Fr(1, 7) * Fr(6, 7))

print("== 1284 Linéarité de l'espérance")
ok("Q1", E(S2), 7)
ok("Q2", E(somme(PIECE, PIECE)), 1)
ok("Q3", E(somme(bern(Fr(5, 8)), bern(Fr(5, 8)))), Fr(5, 4))
ok("Q4", E(affine(DE, 3, 2)), Fr(25, 2))
dbl = Fr(sum(1 for a in range(1, 7) for b in range(1, 7) if a == b), 36)
ok("P(double)", dbl, Fr(1, 6))
ok("Q5 E(gain)", E(loi([(10, dbl), (2, 1 - dbl)])), Fr(10, 3))

print("== 1288 DS")
S3 = somme(S2, DE)
ok("A1", E(S3), Fr(21, 2))
ok("A2", 2 * 4 + 3 * 6 - 1, 25)
Gi = loi([(3, Fr(1, 2)), (-1, Fr(1, 2))])
G4 = somme(somme(Gi, Gi), somme(Gi, Gi))
ok("A3 E(G_i)", E(Gi), 1)
ok("A3 E(G)", E(G4), 4)
ok("B1", V(S2), Fr(35, 6))
ok("B2", 4 * 5 + 1 * 3, 23)
ok("B3", V(binom(6, Fr(1, 2))), Fr(3, 2))
ok("C1 E", E(binom(20, Fr(2, 5))), 8)
ok("C1 V", V(binom(20, Fr(2, 5))), Fr(24, 5))
ok("C2 E", E(binom(15, Fr(5, 8))), Fr(75, 8))
ok("C2 V", V(binom(15, Fr(5, 8))), Fr(225, 64))
ok("C2 sigma", sqrt(225 / 64), 15 / 8, 1e-12)
ok("D1 E(S100)", 100 * Fr(7, 2), 350)
ok("D1 V(S100)", 100 * Fr(35, 12), Fr(875, 3))
ok("D1 sigma(S100)", sqrt(875 / 3), 17.08, 0.005)
ok("D1 V(M100)", Fr(875, 3) / 100 ** 2, Fr(7, 240))
ok("D1 sigma(M100)", sqrt(7 / 240), 0.171, 0.0005)
pF = Fr(45, 100)
VF = 80 * pF * (1 - pF) / 80 ** 2
ok("D2 V(F)", VF, Fr(99, 32000))
ok("D2 V(F) décimal", float(VF), 0.00309375, 1e-12)
sF = sqrt(VF)
ok("D2 sigma(F)", sF, 0.0556, 0.00005)
ok("D2 borne inf", 0.45 - 2 * sF, 0.339, 0.0005)
ok("D2 borne sup", 0.45 + 2 * sF, 0.561, 0.0005)
N4 = binom(4, Fr(85, 100))
ok("E1 E", E(N4), Fr(17, 5))
ok("E1 V", V(N4), Fr(51, 100))
ok("E1 P(N=3)", float(N4[3]), 0.368475, 1e-9)
ok("E1 P(N=4)", float(N4[4]), 0.52200625, 1e-12)
ok("E1 P(N>=3)", float(N4[3] + N4[4]), 0.89048125, 1e-12)

print("== 1286 Applications")
ok("Q1 E", E(binom(10, Fr(1, 2))), 5)
ok("Q1 V", V(binom(10, Fr(1, 2))), Fr(5, 2))
ok("Q2 E(X)", E(binom(5, Fr(3, 8))), Fr(15, 8))
ok("Q2 V(X)", V(binom(5, Fr(3, 8))), Fr(75, 64))
ok("Q2 E(Y)", E(binom(5, Fr(1, 2))), Fr(5, 2))
ok("Q2 V(Y)", V(binom(5, Fr(1, 2))), Fr(5, 4))
# loi exacte de S = X + Y (rouge ou bleue) par énumération des 8^5 tirages
couleurs = ["R"] * 3 + ["B"] * 4 + ["V"]
loiS = {}
for tir in product(range(8), repeat=5):
    s = sum(1 for i in tir if couleurs[i] != "V")
    loiS[s] = loiS.get(s, 0) + Fr(1, 8 ** 5)
ok("Q2 S ~ B(5;7/8)", loiS == binom(5, Fr(7, 8)), True)
ok("Q2 E(S)", E(loiS), Fr(35, 8))
ok("Q2 V(S)", V(loiS), Fr(35, 64))
ok("Q2 V(X)+V(Y) ≠ V(S)", Fr(75, 64) + Fr(5, 4) != Fr(35, 64), True)
ok("Q3 E", E(S3), Fr(21, 2))
ok("Q3 V", V(S3), Fr(35, 4))
ok("Q3 E(M)", E(affine(S3, Fr(1, 3), 0)), Fr(7, 2))
ok("Q3 V(M)", V(affine(S3, Fr(1, 3), 0)), Fr(35, 36))
Gi = loi([(5, Fr(1, 2)), (-2, Fr(1, 2))])
G4 = somme(somme(Gi, Gi), somme(Gi, Gi))
ok("Q4 E(G_i)", E(Gi), Fr(3, 2))
ok("Q4 V(G_i)", V(Gi), Fr(49, 4))
ok("Q4 E(G)", E(G4), 6)
ok("Q4 V(G)", V(G4), 49)
ok("Q5 E", E(binom(25, Fr(3, 5))), 15)
ok("Q5 V", V(binom(25, Fr(3, 5))), 6)
ok("Q5 E(F)", E(binom(25, Fr(3, 5))) / 25, Fr(3, 5))
ok("Q5 V(F)", V(binom(25, Fr(3, 5))) / 625, Fr(6, 625))

print("== 1287 Situations complexes")
X = binom(100, Fr(5, 100))
ok("Q1 E", E(X), 5)
ok("Q1 V", V(X), Fr(19, 4))
ok("Q1 V(F)", V(X) / 10000, Fr(19, 40000))
ok("Q1 sigma(F)", sqrt(19 / 40000), 0.0218, 0.00005)
# 5 dés : loi exacte de S
S5 = DE
for _ in range(4):
    S5 = somme(S5, DE)
ok("Q2 E(S)", E(S5), Fr(35, 2))
ok("Q2 V(S)", V(S5), Fr(175, 12))
p25 = sum(p for s, p in S5.items() if s >= 25)
p20 = sum(p for s, p in S5.items() if 20 <= s <= 24)
print("      P(S>=25) =", p25, "=", float(p25), " ; P(20<=S<=24) =", p20, "=", float(p20),
      " ; P(S<20) =", 1 - p25 - p20, "=", float(1 - p25 - p20))
ok("Q2 P(S>=25) = 252/7776", p25, Fr(252, 7776))
ok("Q2 P(20<=S<=24) = 2121/7776", p20, Fr(2121, 7776))
ok("Q2 P(S>=25) ≈ 0,0324", float(p25), 0.0324, 0.00005)
ok("Q2 P(20<=S<=24) ≈ 0,2728", float(p20), 0.2728, 0.00005)
ok("Q2 P(S<20) ≈ 0,6948", float(1 - p25 - p20), 0.6948, 0.00005)
EG = 20 * p25 + 10 * p20
ok("Q2 E(G) exact = 26250/7776", EG, Fr(26250, 7776))
ok("Q2 E(G) ≈ 3,38", float(EG), 3.376, 0.0005)
ok("Q2 E(G) avec 0,0324 et 0,2728", 20 * 0.0324 + 10 * 0.2728, 3.376, 0.0005)
ok("Q2 E(N) = E(G) - 8 ≈ -4,62", float(EG - 8), -4.624, 0.0005)
ok("Q2 symétrie P(S>=25) = P(S<=10)", p25, sum(p for s, p in S5.items() if s <= 10))
ok("Q3 E(X)", E(binom(50, Fr(7, 10))), 35)
ok("Q3 V(X)", V(binom(50, Fr(7, 10))), Fr(21, 2))
ok("Q3 E(Y)", E(binom(50, Fr(3, 10))), 15)
ok("Q3 V(Y)", V(binom(50, Fr(3, 10))), Fr(21, 2))
X = binom(200, Fr(3, 5))
ok("Q4 E", E(X), 120)
ok("Q4 V", V(X), 48)
ok("Q4 sigma", sqrt(48), 6.93, 0.005)
sF = sqrt(48) / 200
ok("Q4 sigma(F) = sqrt3/50", sF, sqrt(3) / 50, 1e-12)
ok("Q4 sigma(F)", sF, 0.0346, 0.00005)
a, b = 0.6 - 2 * sF, 0.6 + 2 * sF
ok("Q4 borne inf", a, 0.531, 0.0005)
ok("Q4 borne sup", b, 0.669, 0.0005)
pint = sum(p for k, p in X.items() if a <= k / 200 <= b)
ok("Q4 P(F dans l'intervalle) exacte ≈ 0,949", float(pint), 0.949, 0.0005)
ok("Q4 F dans l'intervalle <=> 107 <= X <= 133", [k for k in X if a <= k / 200 <= b] == list(range(107, 134)), True)
ok("Q4 Bienaymé-Tchebychev : au moins 1 - 1/4", 1 - Fr(1, 4), Fr(3, 4))
N3 = binom(3, Fr(9, 10))
ok("Q5 E(X_i)", E(bern(Fr(9, 10))), Fr(9, 10))
ok("Q5 V(X_i)", V(bern(Fr(9, 10))), Fr(9, 100))
ok("Q5 E(N)", E(N3), Fr(27, 10))
ok("Q5 V(N)", V(N3), Fr(27, 100))
ok("Q5 loi", [N3[k] for k in range(4)], [Fr(1, 1000), Fr(27, 1000), Fr(243, 1000), Fr(729, 1000)])
ok("Q5 E(N^2)", sum(k * k * p for k, p in N3.items()), Fr(756, 100))
ok("Q5 P(N>=2)", N3[2] + N3[3], Fr(972, 1000))

# ------------------------------------------------ finition 2026-11-02 (sympy)
import sympy as sp

print("\n--- Finition 2026-11-02 (sympy) ---")
q = sp.Rational
# 1284 Q4 (figure) : valeurs de 3X + 2 et image de la moyenne
ok("1284 fig. valeurs de 3X+2", [3 * k + 2 for k in range(1, 7)], [5, 8, 11, 14, 17, 20])
ok("1284 fig. 3*3,5+2", 3 * q(7, 2) + 2, q(25, 2))
ok("1284 fig. moyenne des valeurs de 3X+2", sp.Rational(sum(3 * k + 2 for k in range(1, 7)), 6), q(25, 2))
# 1285 Q2 : vérification par la loi de S = X1 + X2
loiS = {0: q(1, 4), 1: q(1, 2), 2: q(1, 4)}
calc = {}
for a, b in product((0, 1), repeat=2):
    calc[a + b] = calc.get(a + b, 0) + q(1, 4)
ok("1285 Q2 loi de S par énumération", calc, loiS)
ES = sum(k * p for k, p in loiS.items())
ok("1285 Q2 E(S)", ES, 1)
ok("1285 Q2 V(S) par la définition", sum(p * (k - ES) ** 2 for k, p in loiS.items()), q(1, 2))
# 1286 Q2 (figure) : 7 boules rouges ou bleues sur 8
ok("1286 Q2 P(rouge ou bleue)", q(3 + 4, 8), q(7, 8))
ok("1286 Q2 V(S)", 5 * q(7, 8) * q(1, 8), q(35, 64))
# 1286 Q4 : écarts à l'espérance
ok("1286 Q4 E(G_i)", 5 * q(1, 2) + (-2) * q(1, 2), q(3, 2))
ok("1286 Q4 écarts", (5 - q(3, 2), -2 - q(3, 2)), (q(7, 2), -q(7, 2)))
ok("1286 Q4 V(G_i)", q(1, 2) * q(7, 2) ** 2 * 2, q(49, 4))
# 1288 E1 (figure) : loi de N ~ B(4 ; 0,85), valeurs arrondies affichées
p85 = q(85, 100)
PN = [sp.binomial(4, k) * p85 ** k * (1 - p85) ** (4 - k) for k in range(5)]
for k, aff in zip(range(5), ("0.0005", "0.0115", "0.0975", "0.3685", "0.5220")):
    ok(f"1288 E1 P(N={k}) arrondi affiché", round(float(PN[k]), 4), float(aff))
ok("1288 E1 P(N>=3) exacte = 0,368475 + 0,52200625", PN[3] + PN[4], q(89048125, 100000000))
ok("1288 E1 P(N>=3) ≈ 0,890", round(float(PN[3] + PN[4]), 3), 0.890)

# ------------------------------------------------ enrichissement 2026-11-02 (sympy)
print("\n--- Enrichissement 2026-11-02 (sympy) ---")


def Es(d):
    return sp.nsimplify(sum(sp.nsimplify(v) * p for v, p in d.items()))


def Vs(d):
    m = Es(d)
    return sp.nsimplify(sum(p * (sp.nsimplify(v) - m) ** 2 for v, p in d.items()))


def aff(d, a, b):
    r = {}
    for v, p in d.items():
        r[a * v + b] = r.get(a * v + b, 0) + p
    return r


def conv(d1, d2):
    r = {}
    for (a, p), (b, s) in product(d1.items(), d2.items()):
        r[a + b] = r.get(a + b, 0) + p * s
    return r


# nouveau-1 : jeu du forain, X points, Y = 2X - 1 euros
X1 = {0: q(4, 10), 1: q(3, 10), 2: q(2, 10), 4: q(1, 10)}
ok("n1 somme des probabilités", sum(X1.values()), 1)
ok("n1 E(X)", Es(X1), q(11, 10))
ok("n1 écarts", [v - q(11, 10) for v in (0, 1, 2, 4)], [-q(11, 10), -q(1, 10), q(9, 10), q(29, 10)])
ok("n1 termes p(x-E)^2", [X1[v] * (v - q(11, 10)) ** 2 for v in (0, 1, 2, 4)], [q(484, 1000), q(3, 1000), q(162, 1000), q(841, 1000)])
ok("n1 V(X)", Vs(X1), q(149, 100))
Y1 = aff(X1, 2, -1)
ok("n1 valeurs de Y", sorted(Y1), [-1, 1, 3, 7])
ok("n1 E(Y) formule", 2 * q(11, 10) - 1, q(6, 5))
ok("n1 E(Y) par la loi", Es(Y1), q(6, 5))
ok("n1 termes E(Y) par la loi", [Y1[v] * v for v in (-1, 1, 3, 7)], [-q(4, 10), q(3, 10), q(6, 10), q(7, 10)])
ok("n1 V(Y)", Vs(Y1), 4 * q(149, 100))
ok("n1 V(Y) = 5,96", 4 * q(149, 100), q(596, 100))
ok("n1 sigma(Y) ≈ 2,44", round(float(sp.sqrt(q(596, 100))), 2), 2.44)
c = sp.symbols("c")
ok("n1 mise équitable c", sp.solve(sp.Eq(2 * q(11, 10) - c, 0), c), [q(11, 5)])

# nouveau-2 : QCM de 5 questions, 4 réponses dont une juste
pB = q(1, 4)
ok("n2 V(X_i)", pB * (1 - pB), q(3, 16))
loiN = {0: 1}
for _ in range(5):
    loiN = conv(loiN, {0: 1 - pB, 1: pB})
ok("n2 loi de N = binomiale(5, 1/4)", loiN, {k: sp.binomial(5, k) * pB ** k * (1 - pB) ** (5 - k) for k in range(6)})
ok("n2 E(N)", Es(loiN), q(5, 4))
ok("n2 V(N)", Vs(loiN), q(15, 16))
ok("n2 probabilités affichées", [round(float(loiN[k]), 3) for k in range(6)], [0.237, 0.396, 0.264, 0.088, 0.015, 0.001])
nn = sp.symbols("N")
ok("n2 T = 4N - (5 - N) = 5N - 5", sp.expand(4 * nn - (5 - nn)), 5 * nn - 5)
T2 = aff(loiN, 5, -5)
ok("n2 E(T)", Es(T2), q(5, 4))
ok("n2 V(T)", Vs(T2), q(375, 16))
ok("n2 sigma(T) ≈ 4,84", round(float(sp.sqrt(q(375, 16))), 2), 4.84)
ok("n2 P(T > 0) = P(N >= 2)", sum(p for t, p in T2.items() if t > 0), 1 - loiN[0] - loiN[1])
ok("n2 P(N >= 2) = 47/128", 1 - loiN[0] - loiN[1], q(47, 128))
ok("n2 P(N >= 2) ≈ 0,367", round(float(q(47, 128)), 3), 0.367)

# nouveau-3 : dé, face du dessus X, face du dessous Z = 7 - X, autre dé Y
De = {k: q(1, 6) for k in range(1, 7)}
ok("n3 E(X)", Es(De), q(7, 2))
ok("n3 somme des carrés des écarts", sum((k - q(7, 2)) ** 2 for k in range(1, 7)), q(35, 2))
ok("n3 V(X)", Vs(De), q(35, 12))
ok("n3 V(X+Y) dés indépendants", Vs(conv(De, De)), q(35, 6))
ok("n3 sigma(X+Y) ≈ 2,42", round(float(sp.sqrt(q(35, 6))), 2), 2.42)
Z = aff(De, -1, 7)
ok("n3 loi de Z = loi de X", Z, De)
XZ = {}
for k in range(1, 7):
    XZ[k + (7 - k)] = XZ.get(k + (7 - k), 0) + q(1, 6)
ok("n3 X+Z = 7 certain", XZ, {7: 1})
ok("n3 V(X+Z)", Vs(XZ), 0)
ok("n3 V(X)+V(Z)", 2 * q(35, 12), q(35, 6))
ok("n3 P(X=1 et Z=1) = 0 et P(X=1)P(Z=1)", (0, q(1, 6) * q(1, 6)), (0, q(1, 36)))
DZ = aff(De, 2, -7)
ok("n3 valeurs de X - Z = 2X - 7", sorted(DZ), [-5, -3, -1, 1, 3, 5])
ok("n3 E(X-Z)", Es(DZ), 0)
ok("n3 V(X-Z) = 4V(X)", Vs(DZ), q(35, 3))
ok("n3 V(X-Y) indépendants", Vs(conv(De, aff(De, -1, 0))), q(35, 6))
ok("n3 loi de X+Y affichée (6/36 en 7)", conv(De, De)[7], q(6, 36))

# nouveau-4 : temps de service, échantillon de taille n
T4 = {2: q(1, 8), 6: q(3, 4), 10: q(1, 8)}
ok("n4 somme des probabilités", sum(T4.values()), 1)
ok("n4 E(X)", Es(T4), 6)
ok("n4 V(X)", Vs(T4), 4)
S = {0: 1}
for _ in range(25):
    S = conv(S, T4)
ok("n4 E(S25) exact", Es(S), 150)
ok("n4 V(S25) exact", Vs(S), 100)
M25 = {s / sp.Integer(25): p for s, p in S.items()}
ok("n4 E(M25)", Es(M25), 6)
ok("n4 V(M25)", Vs(M25), q(4, 25))
ok("n4 sigma(M25)", sp.sqrt(Vs(M25)), q(2, 5))
nsym = sp.symbols("n", positive=True)
ok("n4 2/sqrt(n) <= 0,25 <=> n >= 64", sp.solve(sp.Eq(2 / sp.sqrt(nsym), q(1, 4)), nsym), [64])
S4 = {0: 1}
for _ in range(4):
    S4 = conv(S4, T4)
ok("n4 sigma(M4) = 1", sp.sqrt(Vs({s / sp.Integer(4): p for s, p in S4.items()})), 1)

# nouveau-5 : assurance
pS, pG = q(3, 100), q(1, 3)
X5 = {0: 1 - pS, 1000: pS * (1 - pG), 5000: pS * pG}
ok("n5 loi du coût", X5, {0: q(97, 100), 1000: q(2, 100), 5000: q(1, 100)})
ok("n5 E(X)", Es(X5), 70)
ok("n5 termes", [X5[v] * (v - 70) ** 2 for v in (0, 1000, 5000)], [4753, 17298, 243049])
ok("n5 V(X)", Vs(X5), 265100)
ok("n5 sigma(X) ≈ 514,88", round(float(sp.sqrt(265100)), 2), 514.88)
G5 = aff(X5, -1, 100)
ok("n5 E(G)", Es(G5), 30)
ok("n5 V(G)", Vs(G5), 265100)
ok("n5 E(T)", 1000 * 30, 30000)
ok("n5 V(T)", 1000 * 265100, 265100000)
ok("n5 sigma(T) ≈ 16 282", round(float(sp.sqrt(265100000))), 16282)
ok("n5 sigma(M) ≈ 16,28", round(float(sp.sqrt(265100000)) / 1000, 2), 16.28)
ok("n5 sigma(M) = sigma(X)/sqrt(1000)", sp.sqrt(sp.Integer(265100) / 1000), sp.sqrt(sp.Integer(265100000)) / 1000)
ok("n5 n >= 265100/25", q(265100, 25), 10604)

# nouveau-6 : type examen, chaîne de production
X6 = {8: q(2, 10), 10: q(5, 10), 12: q(3, 10)}
ok("n6 A1 E(X)", Es(X6), q(51, 5))
ok("n6 A1 termes", [X6[v] * (v - q(51, 5)) ** 2 for v in (8, 10, 12)], [q(968, 1000), q(20, 1000), q(972, 1000)])
ok("n6 A1 V(X)", Vs(X6), q(49, 25))
ok("n6 A1 sigma(X)", sp.sqrt(q(49, 25)), q(7, 5))
C6 = aff(X6, q(1, 2), 3)
ok("n6 A2 E(C)", Es(C6), q(81, 10))
ok("n6 A2 V(C)", Vs(C6), q(49, 100))
ok("n6 A2 sigma(C)", sp.sqrt(Vs(C6)), q(7, 10))
p6 = q(4, 100)
PD = [sp.binomial(50, k) * p6 ** k * (1 - p6) ** (50 - k) for k in range(51)]
ok("n6 B2 E(D)", sum(k * PD[k] for k in range(51)), 2)
ok("n6 B2 V(D)", sum(PD[k] * (k - 2) ** 2 for k in range(51)), q(48, 25))
ok("n6 B3 P(D=0) ≈ 0,1299", round(float(PD[0]), 4), 0.1299)
ok("n6 B3 P(D=1), P(D=2)", (round(float(PD[1]), 4), round(float(PD[2]), 4)), (0.2706, 0.2762))
ok("n6 B3 P(D<=2) ≈ 0,677", round(float(PD[0] + PD[1] + PD[2]), 3), 0.677)
ok("n6 B3 P(D>=1) ≈ 0,870", round(float(1 - PD[0]), 3), 0.870)
ok("n6 fig. barres affichées", [round(float(PD[k]), 3) for k in range(7)], [0.130, 0.271, 0.276, 0.184, 0.090, 0.035, 0.011])
ok("n6 B4 E(K)", 50 * q(81, 10), 405)
ok("n6 B4 V(K)", 50 * q(49, 100), q(49, 2))
ok("n6 B4 sigma(K) ≈ 4,95", round(float(sp.sqrt(q(49, 2))), 2), 4.95)
ok("n6 B4 E(K + 6D)", 405 + 6 * 2, 417)
ok("n6 C1 sigma(M49)", q(7, 5) / sp.sqrt(49), q(1, 5))
ok("n6 C2 1,4/sqrt(n) <= 0,1 <=> n >= 196", sp.solve(sp.Eq(q(7, 5) / sp.sqrt(nsym), q(1, 10)), nsym), [196])
print("\nTout est juste.")
