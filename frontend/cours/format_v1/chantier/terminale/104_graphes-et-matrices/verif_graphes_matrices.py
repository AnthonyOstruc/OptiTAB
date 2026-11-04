# -*- coding: utf-8 -*-
"""Vérification de tous les résultats de la notion « Graphes et matrices ».

    python verif_graphes_matrices.py

Chaque bloc reprend un exemple du cours, de la fiche ou un exercice et
contrôle (sympy, calcul exact) les valeurs écrites dans les fichiers finaux.
Arrêt sur la première erreur (assert) ; « TOUT EST JUSTE » sinon.
"""
from itertools import product

from sympy import Matrix, Rational as R, eye, symbols, simplify, zeros, solve, Eq, linsolve

OK = []


def ok(nom):
    OK.append(nom)


def chemins(arcs, sommets, depart, arrivee, longueur):
    """Liste des chemins (sommets répétables) de longueur donnée."""
    succ = {s: [b for a, b in arcs if a == s] for s in sommets}
    res = [[depart]]
    for _ in range(longueur):
        res = [c + [t] for c in res for t in succ[c[-1]]]
    return ["".join(c) for c in res if c[-1] == arrivee]


def adjacence(arcs, sommets, oriente=True):
    n = len(sommets)
    M = zeros(n, n)
    for a, b in arcs:
        M[sommets.index(a), sommets.index(b)] += 1
        if not oriente:
            M[sommets.index(b), sommets.index(a)] += 1
    return M


# ====================================================================== COURS
# I-II. Opérations
A = Matrix([[1, 2, 3], [4, 5, 6]])
assert A[1, 2] == 6
assert A + Matrix([[2, -1, 0], [3, 1, -2]]) == Matrix([[3, 1, 3], [7, 6, 4]])
assert 3 * Matrix([[1, 2], [-1, 4]]) == Matrix([[3, 6], [-3, 12]])
assert A * Matrix([1, 0, -1]) == Matrix([-2, -2])
P1, P2 = Matrix([[1, 2], [3, 4]]), Matrix([[5, 6], [7, 8]])
assert P1 * P2 == Matrix([[19, 22], [43, 50]])
assert P2 * P1 == Matrix([[23, 34], [31, 46]])
assert Matrix([[1, 1], [1, 1]]) * Matrix([[1, -1], [-1, 1]]) == zeros(2, 2)
# figure « produit ligne × colonne »
Bp = Matrix([[1, 0], [-1, 2], [2, 1]])
assert A * Bp == Matrix([[5, 7], [11, 16]])
assert 4 * 1 + 5 * (-1) + 6 * 2 == 11
ok("cours : opérations et produit")

# III. Inverse, systèmes
a, b, c, d = symbols("a b c d")
M = Matrix([[a, b], [c, d]])
assert simplify(M * Matrix([[d, -b], [-c, a]]) - (a * d - b * c) * eye(2)) == zeros(2, 2)
A2 = Matrix([[2, 3], [1, 4]])
assert A2.det() == 5 and A2.inv() == R(1, 5) * Matrix([[4, -3], [-1, 2]])
assert A2.inv() * Matrix([5, 6]) == Matrix([R(2, 5), R(7, 5)])
assert R(1, 5) * Matrix([[4, -3], [-1, 2]]) * Matrix([5, 6]) == R(1, 5) * Matrix([2, 7])
T = Matrix([[1, 1, 0], [0, 1, 1], [0, 0, 1]])
Ti = Matrix([[1, -1, 1], [0, 1, -1], [0, 0, 1]])
assert T * Ti == eye(3) and Ti * T == eye(3)
assert Ti * Matrix([3, 5, 2]) == Matrix([0, 3, 2])
x, y, z = symbols("x y z")
assert solve([x + y - 3, y + z - 5, z - 2], [x, y, z]) == {x: 0, y: 3, z: 2}
ok("cours : inverse et systèmes")

# Pour aller plus loin : déterminant d'ordre 3 (Sarrus)
aa, bb, cc, dd, ee, ff, gg, hh, ii = symbols("a b c d e f g h i")
G = Matrix([[aa, bb, cc], [dd, ee, ff], [gg, hh, ii]])
assert simplify(G.det() - (aa*ee*ii + bb*ff*gg + cc*dd*hh - cc*ee*gg - aa*ff*hh - bb*dd*ii)) == 0
ok("cours : formule de Sarrus")

# IV. Puissances et suites
n = symbols("n", integer=True, nonnegative=True)
S = Matrix([[1, 1], [0, 1]])
for k in range(0, 8):
    assert S ** k == Matrix([[1, k], [0, 1]])
D = Matrix([[2, 0], [0, 3]])
for k in range(0, 8):
    assert D ** k == Matrix([[2 ** k, 0], [0, 3 ** k]])
# suite récurrente d'ordre 2 : u_{n+2} = u_{n+1} + 2 u_n
F = Matrix([[1, 2], [1, 0]])
u = [0, 1]
for k in range(12):
    u.append(u[-1] + 2 * u[-2])
for k in range(10):
    assert F * Matrix([u[k + 1], u[k]]) == Matrix([u[k + 2], u[k + 1]])
assert u[:6] == [0, 1, 1, 3, 5, 11]
# U_{n+1} = A U_n + C
Aa = Matrix([[R(1, 2), 0], [0, R(1, 4)]])
C = Matrix([1, 3])
L = (eye(2) - Aa).inv() * C
assert L == Matrix([2, 4]) and Aa * L + C == L
U = Matrix([0, 0])
for k in range(10):
    assert U == Matrix([2 - 2 * R(1, 2) ** k, 4 - 4 * R(1, 4) ** k])
    assert U == L + Aa ** k * (Matrix([0, 0]) - L)
    U = Aa * U + C
ok("cours : puissances et suites")

# V. Transformations
Rot = Matrix([[0, -1], [1, 0]])
assert Rot * Matrix([2, 1]) == Matrix([-1, 2])
ok("cours : rotation")

# VI-VII. Graphes
SOM = list("ABCDE")
ARETES = [("A", "B"), ("A", "D"), ("B", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("D", "E")]
G = adjacence(ARETES, SOM, oriente=False)
assert G == Matrix([[0, 1, 0, 1, 0], [1, 0, 1, 1, 0], [0, 1, 0, 1, 1], [1, 1, 1, 0, 1], [0, 0, 1, 1, 0]])
deg = [sum(G.row(i)) for i in range(5)]
assert deg == [2, 3, 3, 4, 2] and sum(deg) == 2 * len(ARETES) == 14
G2 = G ** 2
assert G2[0, 2] == 2  # A–B–C et A–D–C
assert G2[0, 0] == 2  # A–B–A, A–D–A
NON_OR = ARETES + [(b_, a_) for a_, b_ in ARETES]
assert sorted(chemins(NON_OR, SOM, "A", "C", 2)) == ["ABC", "ADC"]
# connexe : I + G + G^2 + G^3 + G^4 > 0
Ssum = eye(5) + G + G ** 2 + G ** 3 + G ** 4
assert all(v > 0 for v in Ssum)
# graphe non connexe de la figure (E isolé) : les coefficients (E, ·) sont nuls
G_nc = adjacence([("A", "B"), ("A", "D"), ("B", "C"), ("B", "D"), ("C", "D")], SOM, oriente=False)
Snc = eye(5) + G_nc + G_nc ** 2 + G_nc ** 3 + G_nc ** 4
assert Snc[4, 0] == 0
# graphe complet
for k in (4, 5):
    assert k * (k - 1) // 2 == {4: 6, 5: 10}[k]
ok("cours : graphe non orienté")

# Graphe orienté du cours : triangle A, B, C et D au centre
SO = list("ABCD")
ARCS = [("A", "B"), ("B", "C"), ("C", "A"), ("A", "D"), ("C", "D"), ("D", "B")]
Mo = adjacence(ARCS, SO)
assert Mo == Matrix([[0, 1, 0, 1], [0, 0, 1, 0], [1, 0, 0, 1], [0, 1, 0, 0]])
Mo2 = Mo ** 2
assert Mo2 == Matrix([[0, 1, 1, 0], [1, 0, 0, 1], [0, 2, 0, 1], [0, 0, 1, 0]]), Mo2
assert sorted(chemins(ARCS, SO, "A", "B", 2)) == ["ADB"]
assert sorted(chemins(ARCS, SO, "C", "B", 2)) == ["CAB", "CDB"]
assert Mo2.row(2) == Mo.row(0) + Mo.row(3)
for i, j in product(range(4), range(4)):
    for k in range(1, 6):
        assert (Mo ** k)[i, j] == len(chemins(ARCS, SO, SO[i], SO[j], k))
# sommes des lignes = degrés sortants
assert [sum(Mo.row(i)) for i in range(4)] == [2, 1, 2, 1]
ok("cours : graphe orienté et chemins")

# VIII. Chaînes de Markov
P = Matrix([[R(8, 10), R(2, 10)], [R(3, 10), R(7, 10)]])
pi0 = Matrix([[1, 0]])
assert pi0 * P == Matrix([[R(8, 10), R(2, 10)]])
assert pi0 * P ** 2 == Matrix([[R(7, 10), R(3, 10)]])
assert (P ** 2) == Matrix([[R(70, 100), R(30, 100)], [R(45, 100), R(55, 100)]])
pinv = Matrix([[R(6, 10), R(4, 10)]])
assert pinv * P == pinv
an = symbols("a_n")
assert simplify(an * R(8, 10) + (1 - an) * R(3, 10) - (R(1, 2) * an + R(3, 10))) == 0
for a0 in (1, 0, R(1, 2)):
    pk = Matrix([[a0, 1 - a0]])
    for k in range(12):
        assert pk[0] == R(6, 10) + (a0 - R(6, 10)) * R(1, 2) ** k
        pk = pk * P
# résolution de pi P = pi, p + q = 1
p, q = symbols("p q")
assert solve([Eq(R(8, 10) * p + R(3, 10) * q, p), Eq(p + q, 1)], [p, q]) == {p: R(3, 5), q: R(2, 5)}
# trois états
P3 = Matrix([[R(1, 2), R(1, 2), 0], [R(1, 4), R(1, 2), R(1, 4)], [0, R(1, 2), R(1, 2)]])
assert all(sum(P3.row(i)) == 1 for i in range(3))
pi3 = Matrix([[R(1, 4), R(1, 2), R(1, 4)]])
assert pi3 * P3 == pi3
aa3, bb3, cc3 = symbols("a b c")
sol = solve([Eq(e, v) for e, v in zip(Matrix([[aa3, bb3, cc3]]) * P3, [aa3, bb3, cc3])] + [Eq(aa3 + bb3 + cc3, 1)],
            [aa3, bb3, cc3])
assert sol == {aa3: R(1, 4), bb3: R(1, 2), cc3: R(1, 4)}
pk = Matrix([[1, 0, 0]])
assert pk * P3 == Matrix([[R(1, 2), R(1, 2), 0]])
assert pk * P3 ** 2 == Matrix([[R(3, 8), R(1, 2), R(1, 8)]])
for k in range(1, 12):
    assert pk * P3 ** k == Matrix([[R(1, 4) + R(1, 2) ** (k + 1), R(1, 2), R(1, 4) - R(1, 2) ** (k + 1)]])
ok("cours : chaînes de Markov")

# ================================================================== EXERCICES
# 1135 — Déterminants et inverses
A = Matrix([[3, 2], [1, 4]])
assert A.det() == 10
assert A.inv() == R(1, 10) * Matrix([[4, -2], [-1, 3]]) == Matrix([[R(2, 5), -R(1, 5)], [-R(1, 10), R(3, 10)]])
assert A * A.inv() == eye(2)
B = Matrix([[1, 2, 3], [0, 1, 2], [0, 0, 1]])
Bp = Matrix([[1, -2, 1], [0, 1, -2], [0, 0, 1]])
assert B * Bp == eye(3) and Bp * B == eye(3) and B.inv() == Bp
Cm = Matrix([[2, 1], [4, 2]])
assert Cm.det() == 0
assert Cm * Matrix([1, -2]) == zeros(2, 1)
ok("1135")

# 1134 — Opérations fondamentales
A = Matrix([[2, 3], [1, 4]])
B = Matrix([[1, -1], [2, 3]])
Cm = Matrix([[1, 2, 3], [4, 5, 6]])
assert A + B == Matrix([[3, 2], [3, 7]])
assert 3 * A == Matrix([[6, 9], [3, 12]])
assert A * B == Matrix([[8, 7], [9, 11]])
assert B * A == Matrix([[1, -1], [7, 18]])
assert A * Cm == Matrix([[14, 19, 24], [17, 22, 27]])
assert A * eye(2) == A
ok("1134")

# 1142 — Graphes et chemins (4 sommets)
S4 = list("ABCD")
ARCS42 = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "A"), ("C", "D"), ("D", "A")]
M = adjacence(ARCS42, S4)
assert M == Matrix([[0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1], [1, 0, 0, 0]])
M2, M3 = M ** 2, M ** 3
assert M2 == Matrix([[1, 0, 1, 2], [2, 0, 0, 1], [1, 1, 1, 0], [0, 1, 1, 0]]), M2
assert M3 == Matrix([[3, 1, 1, 1], [1, 2, 2, 0], [1, 1, 2, 2], [1, 0, 1, 2]]), M3
for i, j in product(range(4), range(4)):
    assert M2[i, j] == len(chemins(ARCS42, S4, S4[i], S4[j], 2))
    assert M3[i, j] == len(chemins(ARCS42, S4, S4[i], S4[j], 3))
# énumérations écrites dans le corrigé
assert sorted(chemins(ARCS42, S4, "A", "D", 2)) == ["ABD", "ACD"]
assert sorted(chemins(ARCS42, S4, "A", "A", 2)) == ["ACA"]
assert sorted(chemins(ARCS42, S4, "A", "C", 2)) == ["ABC"]
assert sorted(chemins(ARCS42, S4, "B", "A", 2)) == ["BCA", "BDA"]
assert sorted(chemins(ARCS42, S4, "B", "D", 2)) == ["BCD"]
assert sorted(chemins(ARCS42, S4, "C", "A", 2)) == ["CDA"]
assert sorted(chemins(ARCS42, S4, "C", "B", 2)) == ["CAB"]
assert sorted(chemins(ARCS42, S4, "C", "C", 2)) == ["CAC"]
assert sorted(chemins(ARCS42, S4, "D", "B", 2)) == ["DAB"]
assert sorted(chemins(ARCS42, S4, "D", "C", 2)) == ["DAC"]
assert sorted(chemins(ARCS42, S4, "A", "A", 3)) == ["ABCA", "ABDA", "ACDA"]
assert sorted(chemins(ARCS42, S4, "A", "B", 3)) == ["ACAB"]
assert sorted(chemins(ARCS42, S4, "A", "C", 3)) == ["ACAC"]
assert sorted(chemins(ARCS42, S4, "A", "D", 3)) == ["ABCD"]
assert sorted(chemins(ARCS42, S4, "B", "B", 3)) == ["BCAB", "BDAB"]
assert sorted(chemins(ARCS42, S4, "B", "C", 3)) == ["BCAC", "BDAC"]
assert sorted(chemins(ARCS42, S4, "D", "D", 3)) == ["DABD", "DACD"]
# lignes de M^2 = sommes des lignes des successeurs
assert M2.row(0) == M.row(1) + M.row(2)
# forte connexité : circuit A→B→C→D→A ; critère matriciel
assert all(arc in ARCS42 for arc in [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")])
S = M + M2 + M3 + M ** 4
assert all(v > 0 for v in S)
assert all(v > 0 for v in eye(4) + M + M2 + M3)
assert eye(4) + M + M2 + M3 == Matrix([[5, 2, 3, 3], [3, 3, 3, 2], [3, 2, 4, 3], [2, 1, 2, 3]])
assert M2[1, 1] == 0 and M2[2, 1] == 1 and sorted(chemins(ARCS42, S4, "C", "B", 2)) == ["CAB"]
assert M3.row(0) == M2.row(1) + M2.row(2) and M3.row(3) == M2.row(0)
ok("1142")

# 1141 — Suites matricielles et récurrence
A = Matrix([[3, 1], [0, 2]])
M0 = Matrix([1, 1])
assert A * M0 == Matrix([4, 2]) and A ** 2 * M0 == Matrix([14, 4]) and A ** 3 * M0 == Matrix([46, 8])
assert A ** 2 == Matrix([[9, 5], [0, 4]]) and A ** 3 == Matrix([[27, 19], [0, 8]]) and A ** 4 == Matrix([[81, 65], [0, 16]])
for k in range(0, 12):
    assert A ** k == Matrix([[3 ** k, 3 ** k - 2 ** k], [0, 2 ** k]])
    assert A ** k * M0 == Matrix([2 * 3 ** k - 2 ** k, 2 ** k])
kk = symbols("k", integer=True, nonnegative=True)
Ak = Matrix([[3 ** kk, 3 ** kk - 2 ** kk], [0, 2 ** kk]])
assert simplify(Ak * A - Matrix([[3 ** (kk + 1), 3 ** (kk + 1) - 2 ** (kk + 1)], [0, 2 ** (kk + 1)]])) == zeros(2, 2)
ok("1141")

# 1140 — réécrit le 2026-11-02 (le déterminant d'ordre 3 est hors programme) :
# marche aléatoire entre trois refuges, distribution invariante
P = Matrix([[R(7, 10), R(3, 10), 0], [R(2, 10), R(3, 10), R(5, 10)], [0, R(3, 10), R(7, 10)]])
assert all(sum(P.row(i)) == 1 for i in range(3))
pi0 = Matrix([[1, 0, 0]])
assert pi0 * P == Matrix([[R(7, 10), R(3, 10), 0]])
assert pi0 * P ** 2 == Matrix([[R(55, 100), R(3, 10), R(15, 100)]])
assert R(7, 10) * R(7, 10) + R(3, 10) * R(2, 10) == R(55, 100) and R(7, 10) * R(3, 10) + R(3, 10) * R(3, 10) == R(3, 10)
assert R(3, 10) * R(5, 10) == R(15, 100) == (P ** 2)[0, 2]
# question 4 : P(X_n = B) = 0,3 pour n >= 1, quelle que soit la distribution initiale
x, y, z = symbols("x y z")
assert simplify((Matrix([[x, y, 1 - x - y]]) * P)[1] - R(3, 10)) == 0
assert all((pi0 * P ** n)[1] == R(3, 10) for n in range(1, 15))
a, b, c = symbols("a b c")
assert solve(list(Matrix([[a, b, c]]) * P - Matrix([[a, b, c]])) + [a + b + c - 1], [a, b, c]) == {a: R(1, 5), b: R(3, 10), c: R(1, 2)}
assert R(7, 10) * R(2, 10) + R(2, 10) * R(3, 10) == R(2, 10)
assert all(abs(float((pi0 * P ** 60)[j]) - v) < 1e-9 for j, v in enumerate((0.2, 0.3, 0.5)))
ok("1140 (réécrit : marche aléatoire)")

# 1134 — figure produit ligne × colonne
assert Matrix([[2, 3], [1, 4]]) * Matrix([[1, -1], [2, 3]]) == Matrix([[8, 7], [9, 11]]) and 2 * 1 + 3 * 2 == 8
ok("figure ex1134_produit")

# 1136 — Systèmes linéaires
assert Matrix([[2, 3], [1, 2]]).det() == 1
assert Matrix([[2, 3], [1, 2]]).inv() == Matrix([[2, -3], [-1, 2]])
assert Matrix([[2, -3], [-1, 2]]) * Matrix([7, 4]) == Matrix([2, 1])
assert Matrix([[3, -1], [6, -2]]).det() == 0
assert linsolve([3 * x - y - 5, 6 * x - 2 * y - 10], [x, y]) == linsolve([3 * x - y - 5], [x, y])
assert simplify((3 * x - (3 * x - 5)) - 5) == 0
assert Matrix([[1, 2], [2, 4]]).det() == 0
assert linsolve([x + 2 * y - 3, 2 * x + 4 * y - 7], [x, y]).is_empty
assert 3 * 1 - (-2) == 5 and 6 * 1 - 2 * (-2) == 10
ok("1136")

# 1139 — Transformations géométriques
Rq = Matrix([[0, -1], [1, 0]])
Sx = Matrix([[1, 0], [0, -1]])
H3 = 3 * eye(2)
assert Rq * Matrix([2, 3]) == Matrix([-3, 2])
assert H3 * Sx == Matrix([[3, 0], [0, -3]]) == Sx * H3
assert Sx * Matrix([1, -2]) == Matrix([1, 2])
assert H3 * Sx * Matrix([1, -2]) == Matrix([3, 6])
ok("1139")

# 1138 — Graphes et matrices d'adjacence (5 sommets)
S5 = list("ABCDE")
ARCS38 = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A"), ("A", "C"), ("B", "D")]
M = adjacence(ARCS38, S5)
assert M == Matrix([[0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1], [1, 0, 0, 0, 0]])
M2, M3 = M ** 2, M ** 3
assert M2 == Matrix([[0, 0, 1, 2, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1], [1, 0, 0, 0, 0], [0, 1, 1, 0, 0]])
assert M3 == Matrix([[0, 0, 0, 1, 2], [1, 0, 0, 0, 1], [1, 0, 0, 0, 0], [0, 1, 1, 0, 0], [0, 0, 1, 2, 0]])
for i, j in product(range(5), range(5)):
    assert M2[i, j] == len(chemins(ARCS38, S5, S5[i], S5[j], 2))
    assert M3[i, j] == len(chemins(ARCS38, S5, S5[i], S5[j], 3))
assert sorted(chemins(ARCS38, S5, "A", "C", 2)) == ["ABC"]
assert sorted(chemins(ARCS38, S5, "A", "D", 2)) == ["ABD", "ACD"]
assert sorted(chemins(ARCS38, S5, "B", "D", 2)) == ["BCD"]
assert sorted(chemins(ARCS38, S5, "B", "E", 2)) == ["BDE"]
assert sorted(chemins(ARCS38, S5, "C", "E", 2)) == ["CDE"]
assert sorted(chemins(ARCS38, S5, "D", "A", 2)) == ["DEA"]
assert sorted(chemins(ARCS38, S5, "E", "B", 2)) == ["EAB"]
assert sorted(chemins(ARCS38, S5, "E", "C", 2)) == ["EAC"]
assert sorted(chemins(ARCS38, S5, "A", "D", 3)) == ["ABCD"]
assert sorted(chemins(ARCS38, S5, "A", "E", 3)) == ["ABDE", "ACDE"]
assert sorted(chemins(ARCS38, S5, "B", "A", 3)) == ["BDEA"]
assert sorted(chemins(ARCS38, S5, "B", "E", 3)) == ["BCDE"]
assert sorted(chemins(ARCS38, S5, "C", "A", 3)) == ["CDEA"]
assert sorted(chemins(ARCS38, S5, "D", "B", 3)) == ["DEAB"]
assert sorted(chemins(ARCS38, S5, "D", "C", 3)) == ["DEAC"]
assert sorted(chemins(ARCS38, S5, "E", "C", 3)) == ["EABC"]
assert sorted(chemins(ARCS38, S5, "E", "D", 3)) == ["EABD", "EACD"]
assert chemins(ARCS38, S5, "A", "E", 2) == []
assert M2.row(0) == M.row(1) + M.row(2)
assert all(arc in ARCS38 for arc in [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A")])
Ssum = M + M2 + M3 + M ** 4 + M ** 5
assert all(v > 0 for v in Ssum)
assert all(v > 0 for v in eye(5) + M + M2 + M3 + M ** 4)
ok("1138")

# 1137 — Puissances et suites
A = Matrix([[2, 1], [0, 2]])
M0 = Matrix([1, 1])
assert A ** 2 == Matrix([[4, 4], [0, 4]]) and A ** 3 == Matrix([[8, 12], [0, 8]]) and A ** 4 == Matrix([[16, 32], [0, 16]])
for k in range(0, 12):
    assert A ** k == Matrix([[2 ** k, k * R(2) ** (k - 1)], [0, 2 ** k]])
for k in range(1, 12):
    assert A ** k * M0 == Matrix([2 ** (k - 1) * (k + 2), 2 ** k])
assert [tuple(A ** k * M0) for k in range(1, 5)] == [(3, 2), (8, 4), (20, 8), (48, 16)]
Ak = Matrix([[2 ** kk, kk * 2 ** (kk - 1)], [0, 2 ** kk]])
assert simplify(Ak * A - Matrix([[2 ** (kk + 1), (kk + 1) * 2 ** kk], [0, 2 ** (kk + 1)]])) == zeros(2, 2)
ok("1137")

# nouveau-1 — météo à deux états (ajouté le 2026-11-02)
P = Matrix([[R(9, 10), R(1, 10)], [R(4, 10), R(6, 10)]])
pi0 = Matrix([[1, 0]])
assert pi0 * P == Matrix([[R(9, 10), R(1, 10)]]) and pi0 * P ** 2 == Matrix([[R(85, 100), R(15, 100)]])
assert P ** 2 == Matrix([[R(85, 100), R(15, 100)], [R(6, 10), R(4, 10)]])
assert R(4, 10) * R(9, 10) == R(36, 100) and R(6, 10) * R(4, 10) == R(24, 100) and R(36, 100) + R(24, 100) == R(6, 10)
p, q = symbols("p q")
assert solve(list(Matrix([[p, q]]) * P - Matrix([[p, q]])) + [p + q - 1], [p, q]) == {p: R(4, 5), q: R(1, 5)}
assert Matrix([[R(8, 10), R(2, 10)]]) * P == Matrix([[R(8, 10), R(2, 10)]])
assert R(72, 100) + R(8, 100) == R(8, 10) and R(8, 100) + R(12, 100) == R(2, 10)
ok("nouveau-1 (Markov à deux états)")

# nouveau-2 — graphe non orienté à cinq sommets (ajouté le 2026-11-02)
S5n = ["A", "B", "C", "D", "E"]
AR = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D"), ("D", "E")]
M = adjacence(AR, S5n, oriente=False)
assert M == Matrix([[0, 1, 1, 0, 0], [1, 0, 1, 1, 0], [1, 1, 0, 1, 0], [0, 1, 1, 0, 1], [0, 0, 0, 1, 0]]) and M == M.T
deg = [sum(M.row(i)) for i in range(5)]
assert deg == [2, 3, 3, 3, 1] and sum(deg) == 12 == 2 * len(AR) and 5 * 4 // 2 == 10
assert M ** 2 == Matrix([[2, 1, 1, 2, 0], [1, 3, 2, 1, 1], [1, 2, 3, 1, 1], [2, 1, 1, 3, 0], [0, 1, 1, 0, 1]])
assert [(M ** 2)[i, i] for i in range(5)] == deg
ARsym = AR + [(b, a) for a, b in AR]
assert sorted(chemins(ARsym, S5n, "A", "D", 2)) == ["ABD", "ACD"]
assert (M ** 3)[0, 4] == 2 == 2 * 0 + 1 * 0 + 1 * 0 + 2 * 1 + 0 * 0
assert sorted(chemins(ARsym, S5n, "A", "E", 3)) == ["ABDE", "ACDE"]
assert all(v > 0 for v in eye(5) + M + M ** 2 + M ** 3 + M ** 4)  # connexe (chaîne E-D-B-A-C)
ok("nouveau-2 (graphe non orienté)")

# nouveau-3 — U(n+1) = A U(n) + C, état stable (ajouté le 2026-11-02)
A = Matrix([[R(6, 10), R(2, 10)], [R(2, 10), R(6, 10)]])
Cc = Matrix([8, 2])
U = Matrix([10, 10])
assert A * U + Cc == Matrix([16, 10])
L = (eye(2) - A).inv() * Cc
assert L == Matrix([30, 20]) and A * L + Cc == L
l1, l2 = symbols("l1 l2")
assert solve([2 * l1 - l2 - 40, -l1 + 2 * l2 - 10], [l1, l2]) == {l1: 30, l2: 20}
Pm = Matrix([[1, 1], [1, -1]])
D = Matrix([[R(8, 10), 0], [0, R(4, 10)]])
assert Pm ** 2 == 2 * eye(2) and Pm.inv() == Pm / 2 and Pm * D == Matrix([[R(8, 10), R(4, 10)], [R(8, 10), R(-4, 10)]])
assert Pm * D * Pm.inv() == A
nn = symbols("n", integer=True, nonnegative=True)
for k in range(0, 15):
    assert A ** k == Pm * D ** k * Pm.inv()
    assert A ** k == R(1, 2) * Matrix([[R(8, 10) ** k + R(4, 10) ** k, R(8, 10) ** k - R(4, 10) ** k],
                                       [R(8, 10) ** k - R(4, 10) ** k, R(8, 10) ** k + R(4, 10) ** k]])
    Uk = U
    for _ in range(k):
        Uk = A * Uk + Cc
    assert Uk == Matrix([30 - 15 * R(8, 10) ** k - 5 * R(4, 10) ** k, 20 - 15 * R(8, 10) ** k + 5 * R(4, 10) ** k])
    assert A ** k * (U - L) == Matrix([-15 * R(8, 10) ** k - 5 * R(4, 10) ** k, -15 * R(8, 10) ** k + 5 * R(4, 10) ** k])
assert U - L == Matrix([-20, -10])
ok("nouveau-3 (suite U(n+1) = AU(n) + C)")

print("\n".join("✓ " + o for o in OK))
print("TOUT EST JUSTE")
