# -*- coding: utf-8 -*-
"""Vérification de tous les résultats de la notion 169 (Seconde) : cours, fiche, exercices."""
from sympy import sqrt, Rational as R, pi, cos, sin, tan, acos, asin, atan, symbols, expand, simplify, solve, N, Matrix

ok = 0


def chk(nom, a, b):
    global ok
    dif = simplify(a - b)
    nul = dif.is_zero_matrix if hasattr(dif, "is_zero_matrix") else (dif == 0)
    if not nul:
        raise SystemExit("ÉCHEC %s : %s != %s" % (nom, a, b))
    ok += 1


def ap(nom, a, b, tol):
    global ok
    if abs(float(N(a)) - b) > tol:
        raise SystemExit("ÉCHEC %s : %s != %s" % (nom, float(N(a)), b))
    ok += 1


def d2(p, q):
    return (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2


def mil(p, q):
    return (R(p[0] + q[0], 2), R(p[1] + q[1], 2))


def aire(*pts):
    s = 0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(R(s, 2))


deg = pi / 180
x = symbols('x')

# ---------------------------------------------------------------- cours
ap("arbre", 20 * tan(35 * deg), 14.0, 0.05)
ap("angle tan 3/4", atan(R(3, 4)) / deg, 36.87, 0.01)
chk("trigo 30", sin(30 * deg), R(1, 2)); chk("cos30", cos(30 * deg), sqrt(3) / 2)
chk("45", cos(45 * deg), sqrt(2) / 2); chk("tan60", tan(60 * deg), sqrt(3)); chk("tan30", tan(30 * deg), sqrt(3) / 3)
chk("distance 6-8-10", R(6 * 8, 10), R(24, 5))
A, B, C = (0, 0), (4, 2), (1, 3)
chk("ex coord AB2", d2(A, B), 20); chk("AC2", d2(A, C), 10); chk("BC2", d2(B, C), 10)
chk("aire 5", aire(A, B, C), 5)
# enclos : 40 m de grillage contre un mur
chk("enclos", expand(x * (40 - 2 * x)), expand(200 - 2 * (x - 10) ** 2))
chk("cône exemple", R(1, 3) * pi * 3 ** 2 * 4, 12 * pi)
ap("cône 12pi", 12 * pi, 37.7, 0.05)

# ---------------------------------------------------------------- 2057
A, B, C = (-1, 1), (3, 5), (3, 1)
chk("2057 AC", d2(A, C), 16); chk("BC", d2(B, C), 16); chk("AB", d2(A, B), 32)
M = mil(A, B); chk("M", Matrix(M), Matrix([1, 3]))
D = (2 * M[0] - C[0], 2 * M[1] - C[1]); chk("D", Matrix(D), Matrix([-1, 5]))
chk("ACBD carré côté", d2(B, D), 16); chk("aire carré", aire(A, C, B, D), 16)

# ---------------------------------------------------------------- 2058 (remplacé)
P, Q, M, H = (-2, 4), (4, 1), (4, 6), (2, 2)
PH, PQ = (H[0] - P[0], H[1] - P[1]), (Q[0] - P[0], Q[1] - P[1])
chk("PH", Matrix(PH), Matrix([4, -2])); chk("PQ=3/2 PH", Matrix(PQ), R(3, 2) * Matrix(PH))
chk("det", PH[0] * PQ[1] - PH[1] * PQ[0], 0)
chk("MH2", d2(M, H), 20); chk("PH2", d2(P, H), 20); chk("MP2", d2(M, P), 40)
chk("MQ2", d2(M, Q), 25); ap("MH", sqrt(20), 4.47, 0.005)
chk("PQ", sqrt(d2(P, Q)), 3 * sqrt(5)); chk("aire MPQ", aire(M, P, Q), 15)
chk("aire MPQ formule", 3 * sqrt(5) * 2 * sqrt(5) / 2, 15)
# H bien projeté : produit scalaire nul (contrôle)
chk("perp", (M[0] - H[0]) * PQ[0] + (M[1] - H[1]) * PQ[1], 0)

# ---------------------------------------------------------------- 2069
chk("2069", expand(100 - (x - 10) ** 2), expand(x * (20 - x)))

# ---------------------------------------------------------------- 2056
A, B, D = (-2, 1), (2, 1), (-1, 4)
C = (D[0] + B[0] - A[0], D[1] + B[1] - A[1]); chk("C", Matrix(C), Matrix([3, 4]))
chk("AB2", d2(A, B), 16); chk("AD2", d2(A, D), 10)
chk("K", Matrix(mil(A, C)), Matrix([R(1, 2), R(5, 2)])); chk("K bis", Matrix(mil(B, D)), Matrix(mil(A, C)))
chk("aire para", aire(A, B, C, D), 12)

# ---------------------------------------------------------------- 2060
A, B = (-2, 1), (4, 3)
M = mil(A, B); chk("M", Matrix(M), Matrix([1, 2])); chk("r2", R(d2(A, B), 4), 10)
C, D, E = (4, 1), (-2, 3), (1, 5)
chk("MC", d2(M, C), 10); chk("MD", d2(M, D), 10); chk("ME", d2(M, E), 9)
chk("ACB", d2(A, C) + d2(C, B), d2(A, B)); chk("ADB", d2(A, D) + d2(D, B), d2(A, B))
chk("mil CD", Matrix(mil(C, D)), Matrix(M)); chk("CD2", d2(C, D), 40)
chk("aire ACBD", aire(A, C, B, D), 12)

# ---------------------------------------------------------------- 2072
chk("BC", sqrt(36 + 64), 10)

# ---------------------------------------------------------------- 2061
MH = R(2 * 30, 13); chk("MH", MH, R(60, 13)); ap("MH", MH, 4.62, 0.005)
AH, BH = sqrt(25 - MH ** 2), sqrt(144 - MH ** 2)
chk("AH", AH, R(25, 13)); chk("BH", BH, R(144, 13)); chk("somme", AH + BH, 13)
ap("AH", AH, 1.92, 0.005); ap("BH", BH, 11.08, 0.005)
chk("AH2", 25 - MH ** 2, R(625, 169)); chk("BH2", 144 - MH ** 2, R(20736, 169))

# ---------------------------------------------------------------- 2055
A, B, O = (-3, 1), (1, 5), (0, 0)
M = mil(A, B); chk("M", Matrix(M), Matrix([-1, 3]))
Ap = (2 * B[0] - A[0], 2 * B[1] - A[1]); chk("A'", Matrix(Ap), Matrix([5, 9]))
C = (2 * M[0], 2 * M[1]); chk("C", Matrix(C), Matrix([-2, 6]))
chk("AB", sqrt(d2(A, B)), 4 * sqrt(2)); chk("AA'", sqrt(d2(A, Ap)), 8 * sqrt(2))
chk("OACB", Matrix(mil(O, C)), Matrix(mil(A, B)))
chk("OC2", d2(O, C), 40)

# ---------------------------------------------------------------- 2063
chk("h", 8 * sin(30 * deg), 4); chk("d", 8 * cos(30 * deg), 4 * sqrt(3)); ap("d", 4 * sqrt(3), 6.93, 0.005)
ap("angle", acos(R(2, 8)) / deg, 75.52, 0.01)

# ---------------------------------------------------------------- 2065
chk("CH", sqrt(15 ** 2 - 9 ** 2), 12); chk("BC", sqrt(5 ** 2 + 12 ** 2), 13)
chk("aire", R(14 * 12, 2), 84); chk("P", 14 + 15 + 13, 42)

# ---------------------------------------------------------------- 2066
chk("OH", sqrt(25 - 16), 3); chk("aire", R(8 * 3, 2), 12)
ap("AOH", acos(R(3, 5)) / deg, 53.13, 0.01); ap("AOB", 2 * acos(R(3, 5)) / deg, 106.26, 0.01)

# ---------------------------------------------------------------- 2067
chk("AE", R(2, 3) * 18, 12); chk("DE", R(2, 3) * 15, 10); chk("rapport", R(2, 3) ** 2, R(4, 9))

# ---------------------------------------------------------------- 2064
chk("cos", sqrt(1 - R(6, 10) ** 2), R(8, 10)); chk("tan", R(6, 8), R(3, 4))
chk("opp", 15 * R(6, 10), 9); chk("adj", 15 * R(8, 10), 12); chk("pyth", 81 + 144, 225)
ap("alpha", asin(R(6, 10)) / deg, 36.87, 0.01)

# ---------------------------------------------------------------- 2068
chk("cyl", pi * 36 * 15, 540 * pi); chk("cône", R(1, 3) * 540 * pi, 180 * pi)
ap("cyl", 540 * pi, 1696.46, 0.01); ap("cône", 180 * pi, 565.49, 0.01)
chk("cyl 3,14", R(314, 100) * 540, R(16956, 10)); chk("cône 3,14", R(314, 100) * 180, R(5652, 10))

# ---------------------------------------------------------------- 2070
chk("VF3", sqrt(1 - R(64, 100)), R(6, 10)); chk("VF6", 5 ** 2 + 12 ** 2, 13 ** 2)
# finition 2026-11-02 : affirmations chiffrées
chk("VF3 cos ≠ 0,2", sqrt(1 - R(8, 10) ** 2) != R(2, 10), True)
chk("VF4 largeur", 20 - 25, -5)
chk("VF5 cône", R(1, 3) * pi * 3 ** 2 * 4, 12 * pi); chk("VF5 cylindre", pi * 3 ** 2 * 4, 36 * pi)
chk("VF6 somme", 25 + 144, 169)

# ---------------------------------------------------------------- 2071 (remplacé)
AH, BH = 7 * cos(60 * deg), 7 * sin(60 * deg)
chk("AH", AH, R(7, 2)); chk("BH", BH, 7 * sqrt(3) / 2); ap("BH", BH, 6.06, 0.005)
HC = 9 - AH; chk("HC", HC, R(11, 2))
chk("BH2", BH ** 2, R(147, 4)); chk("HC2", HC ** 2, R(121, 4))
BC2 = BH ** 2 + HC ** 2; chk("BC2", BC2, 67); ap("BC", sqrt(67), 8.19, 0.005)
Al = 9 * BH / 2; chk("aire", Al, 63 * sqrt(3) / 4); ap("aire", Al, 27.28, 0.005)
h = 2 * Al / sqrt(67); chk("h", h, 63 * sqrt(3) / (2 * sqrt(67))); ap("h", h, 6.67, 0.005)
# contrôle par Al-Kashi (hors programme, simple vérification)
chk("alkashi", 49 + 81 - 2 * 7 * 9 * cos(60 * deg), 67)

# ---------------------------------------------------------------- 2059
A, B, C, D = (1, 1), (5, 2), (4, 6), (0, 5)
chk("AB=DC", Matrix([B[0] - A[0], B[1] - A[1]]), Matrix([C[0] - D[0], C[1] - D[1]]))
chk("AB2", d2(A, B), 17); chk("BC2", d2(B, C), 17); chk("AC2", d2(A, C), 34)
chk("K", Matrix(mil(A, C)), Matrix([R(5, 2), R(7, 2)])); chk("KA2", d2(mil(A, C), A), R(34, 4))
ap("R", sqrt(34) / 2, 2.92, 0.005); chk("aire", aire(A, B, C, D), 17)
ap("P", 4 * sqrt(17), 16.49, 0.005)

# ---------------------------------------------------------------- nouveau-1 : pyramide
chk("AC", sqrt(36 + 36), 6 * sqrt(2)); chk("OA2", (3 * sqrt(2)) ** 2, 18)
SO = sqrt(81 - 18); chk("SO", SO, 3 * sqrt(7)); ap("SO", SO, 7.94, 0.005)
V = R(1, 3) * 36 * SO; chk("V", V, 36 * sqrt(7)); ap("V", V, 95.25, 0.005)

# ---------------------------------------------------------------- nouveau-2 : carré inscrit
f = x ** 2 + (10 - x) ** 2
chk("aire1", expand(f), 2 * x ** 2 - 20 * x + 100)
chk("aire2", expand(100 - 4 * x * (10 - x) / 2), expand(f))
chk("canon", expand(2 * (x - 5) ** 2 + 50), expand(f))
chk("f(5)", f.subs(x, 5), 50); chk("f(0)", f.subs(x, 0), 100)
assert sorted(solve(f - 58, x)) == [3, 7]; ok += 1
chk("f(3)", f.subs(x, 3), 58)

# ---------------------------------------------------------------- arrondis écrits dans les textes
ap("AA'", 8 * sqrt(2), 11.31, 0.005); ap("2063 d", 4 * sqrt(3), 6.928, 0.0005)
ap("cyl L", 540 * pi / 1000, 1.7, 0.05); ap("cône L", 180 * pi / 1000, 0.57, 0.005)
ap("2071 BC mm", sqrt(67), 8.2, 0.05); ap("2071 h mm", 63 * sqrt(3) / (2 * sqrt(67)), 6.7, 0.05)
ap("2071 h", 63 * sqrt(3) / (2 * sqrt(67)), 6.67, 0.005); ap("aire 27,3", 63 * sqrt(3) / 4, 27.3, 0.05)
ap("n1 AC", 6 * sqrt(2), 8.49, 0.005); ap("n1 OA", 3 * sqrt(2), 4.24, 0.005)
ap("n1 SO mm", 3 * sqrt(7), 7.9, 0.05); ap("n1 mL", 36 * sqrt(7), 95, 0.5)
ap("2056 AD", sqrt(10), 3.16, 0.005); ap("2058 MH", 2 * sqrt(5), 4.47, 0.005)
chk("n1 SO2", 81 - 18, 63); chk("2071 BH2", R(49 * 3, 4), R(147, 4)); chk("268/4", R(268, 4), 67)
chk("2061 4225", 25 * 169, 4225); chk("2061 24336", 144 * 169, 24336)
chk("n2 f(7)", f.subs(x, 7), 58)

print("verif_169 : %d contrôles, tous OK" % ok)
