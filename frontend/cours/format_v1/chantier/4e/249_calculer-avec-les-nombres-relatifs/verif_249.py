# -*- coding: utf-8 -*-
"""Vérification des calculs de la notion 249 (4e : calculer avec les nombres relatifs) avec sympy.

Tous les nombres décimaux sont écrits en fractions exactes (sympy.Rational) : aucun arrondi.
"""
from functools import reduce
from operator import mul

from sympy import Rational as R, symbols, expand, simplify, solve

x, n, b = symbols("x n b")
n_ok = 0


def ok(cond, msg):
    global n_ok
    assert bool(cond), msg
    n_ok += 1


def eq(v, attendu, msg):
    ok(simplify(v - attendu) == 0, f"{msg} : {v} au lieu de {attendu}")


def prod(*fs):
    return reduce(mul, fs, 1)


def d(s):
    """Nombre décimal écrit à la française -> Rational exact."""
    return R(s.replace(",", "."))


# ====================================================================== cours
eq(-7 + -5, -12, "cours add 1"); eq(-7 + 5, -2, "cours add 2"); eq(7 + -5, 2, "cours add 3")
eq(3 - 8, -5, "cours sous 1"); eq(-4 - (-9), 5, "cours sous 2")
eq(-2 + 5, 3, "cours droite -2+5"); eq(3 - 7, -4, "cours droite 3-7")
eq((-4) * d("-2,5"), 10, "cours prod 1"); eq((-3) * 5, -15, "cours prod 2"); eq((-1) * 8, -8, "cours prod 3")
ok([k * (-3) for k in (2, 1, 0, -1, -2)] == [-6, -3, 0, 3, 6], "cours suite moins par moins")
eq(prod(-2, 5, -3, -7), -210, "cours P"); eq(2 * 5 * 3 * 7, 210, "cours P distances")
eq((-50) * 13 * (-2), 1300, "cours regrouper")
eq(-4 - 3, -7, "cours attention 1"); eq((-4) * (-3), 12, "cours attention 2")
eq(R(-54, -9), 6, "cours quotient 1"); eq(6 * (-9), -54, "cours quotient 1 vérif")
eq(R(18, -4), d("-4,5"), "cours quotient 2"); eq(d("-4,5") * (-4), 18, "cours quotient 2 vérif")
eq(R(-35, 7), -5, "cours quotient 3"); eq(R(35, -7), -5, "cours quotient 3b")
eq(R(0, -12), 0, "cours 0 : -12")
A = 6 - 2 * (-3 + 7); eq(A, -2, "cours A"); eq((6 - 2) * (-3 + 7), 16, "cours A parenthèses")
B = -3 * (5 - 2 * (-4)); eq(B, -39, "cours B"); eq(5 - 2 * (-4), 13, "cours B crochet")
eq(R(-8 + 2, -3), 2, "cours C")
eq(R(-36, 4) * (-3), 27, "cours gauche à droite"); eq(R(-36, 4 * (-3)), 3, "cours mauvais ordre")
eq((4 - 3 * x).subs(x, -2), 10, "cours substitution")
eq(5 * d("-1,6"), -8, "cours température variation"); eq(3 + 5 * d("-1,6"), -5, "cours température finale")
eq(18 - (-35), 53, "cours altitudes"); eq(45 + (-70), -25, "cours compte")

# ====================================================================== fiche (reprend le cours)
eq(R(-54, -9), 6, "fiche quotient"); eq(prod(-2, 5, -3, -7), -210, "fiche produit")

# ====================================================================== 2464 thermomètre
T = {"Brest": 3, "Lille": -4, "Strasbourg": -7}
ok(sorted(T.values()) == [-7, -4, 3], "2464 q1")
ok(max(T, key=lambda v: abs(T[v])) == "Strasbourg", "2464 q2")
eq(3 - (-7), 10, "2464 q3"); eq(-4 + 9, 5, "2464 q4"); eq(-7 + (-2) + 6, -3, "2464 q5"); eq(-7 + (-2), -9, "2464 q5a")
eq(-4 - 3, -7, "2464 q6")

# ====================================================================== 2465 règle des signes
ok([a * (-2) for a in (3, 2, 1, 0, -1, -2, -3)] == [-6, -4, -2, 0, 2, 4, 6], "2465 tableau")
eq((-7) * (-6), 42, "2465 q5a"); eq(d("2,4") * (-5), -12, "2465 q5b")
eq(d("-0,5") * (-12), 6, "2465 q6a"); eq((-1) * 15, -15, "2465 q6b"); eq(-7 - 6, -13, "2465 attention")

# ====================================================================== 2466 division
eq((-7) * (-4), 28, "2466 q1"); eq(R(28, -4), -7, "2466 q1b")
eq(R(-54, -9), 6, "2466 q2"); eq(R(18, -4), d("-4,5"), "2466 q3")
eq(R(-35, 7), -5, "2466 q4a"); eq(R(35, -7), -5, "2466 q4b"); eq(R(0, -12), 0, "2466 q5")
ok(solve(x * 0 + 12, x) == [], "2466 q6 : aucun x tel que 0·x = -12")

# ====================================================================== 2467 plusieurs facteurs
fac = [-2, 5, -3, -7]
ok(sum(1 for v in fac if v < 0) == 3, "2467 q1"); eq(prod(*fac), -210, "2467 q4"); eq(2 * 5 * 3 * 7, 210, "2467 q3")
eq((-2) * (-3), 6, "2467 vérif"); eq(prod(*([-1] * 10)), 1, "2467 q5")
eq(prod(-3, 47, d("-8,5"), 0, -12), 0, "2467 q6")

# ====================================================================== 2468 six calculs
eq(-8 - (-3), -5, "2468 q1"); eq((-8) * (-3), 24, "2468 q2"); eq(-8 - 3, -11, "2468 q3")
eq(-8 + (-3), -11, "2468 q4"); eq(R(-8, -4), 2, "2468 q5"); eq(-8 * 3 - 3, -27, "2468 q6")

# ====================================================================== 2469 priorités
eq(14 - 3 * (-2), 20, "2469 A"); eq((14 - 3) * (-2), -22, "2469 B")
eq(-5 + 4 * (-3), -17, "2469 C"); eq((-5 + 4) * (-3), 3, "2469 D")
eq(R(24, -6) * 2, -8, "2469 E"); eq(R(24, (-6) * 2), -2, "2469 F")

# ====================================================================== 2470 quiz
eq(8 * 4, 32, "2470 q1"); eq(5 * (-3), -15, "2470 q2"); eq(8 * 4 + 5 * (-3) + 2 * 0, 17, "2470 q3")
eq(6 * 4 + 9 * (-3), -3, "2470 q4"); eq(17 - (-3), 20, "2470 q5")
score = lambda bon: 4 * bon - 3 * (15 - bon)
ok(score(6) == -3 and score(7) == 4, "2470 q6 scores")
ok(min(v for v in range(16) if score(v) > 0) == 7, "2470 q6 minimum")
ok(all(score(v + 1) - score(v) == 7 for v in range(15)), "2470 q6 +7 par bonne réponse")

# ====================================================================== 2471 crochets et fractions
eq(4 - 9, -5, "2471 q1"); eq(-3 * (4 - 9), 15, "2471 q2"); eq(R(12, -4), -3, "2471 q3")
eq(-3 * (4 - 9) + R(12, -4), 12, "2471 A")
eq(R(-3 * 4 - 9, 2 - 9), 3, "2471 B"); eq(-3 * 4 - 9, -21, "2471 B num"); eq(2 - 9, -7, "2471 B den")
eq(-3 * (4 - 9 + R(12, -4)), 24, "2471 C"); eq(4 - 9 + R(12, -4), -8, "2471 C crochets")

# ====================================================================== 2472 astucieux
eq((-25) * 17 * (-4), 1700, "2472 q1"); eq(d("-0,5") * (-37) * (-2), -37, "2472 q2")
eq(125 * (-7) * 8, -7000, "2472 q3"); eq(d("-2,5") * (-13) * (-4), -130, "2472 q4")
eq((-7) * 99, -693, "2472 q5"); eq((-7) * 100 - (-7) * 1, -693, "2472 q5 distributivité")
eq((-48) * (-25), 1200, "2472 q6"); eq(12 * (4 * 25), 1200, "2472 q6 décomposition")

# ====================================================================== 2473 erreurs de Nora
eq(-6 - 4, -10, "2473 q1"); eq((-3) * (-5), 15, "2473 q2")
eq(R(40, -5) * 2, -16, "2473 q3"); eq(R(40, (-5) * 2), -4, "2473 q3 calcul de Nora")
eq(5 - 3 * (-2), 11, "2473 q4"); eq((5 - 3) * (-2), -4, "2473 q4 calcul de Nora")
eq((-2) * (-2) * (-2), -8, "2473 q5")

# ====================================================================== 2474 altitude
eq(3200 - 400, 2800, "2474 q1"); eq(R(2800, 100), 28, "2474 q2"); eq(28 * d("-0,6"), d("-16,8"), "2474 q3")
eq(12 + 28 * d("-0,6"), d("-4,8"), "2474 q4")
eq(R(2900 - 400, 100), 25, "2474 q5a"); eq(12 + 25 * d("-0,6"), -3, "2474 q5")
eq(R(12, d("0,6")), 20, "2474 q6a"); eq(400 + 20 * 100, 2400, "2474 q6"); eq(12 + 20 * d("-0,6"), 0, "2474 q6 vérif")
temp_alt = lambda h: 12 + R(h - 400, 100) * d("-0,6")
eq(temp_alt(3200), d("-4,8"), "2474 figure sommet"); eq(temp_alt(2900), -3, "2474 figure refuge"); eq(temp_alt(2400), 0, "2474 figure 0")

# ====================================================================== 2475 compte
ops = [d("-48,5"), 3 * d("-18,5"), -60, 250, -230]
eq(ops[1], d("-55,5"), "2475 q1 abonnements")
soldes = [125]
for o in ops:
    soldes.append(soldes[-1] + o)
ok(soldes == [125, d("76,5"), 21, -39, 211, -19], f"2475 soldes {soldes}")
eq(soldes[-1] - soldes[0], -144, "2475 q6 a"); eq(sum(ops), -144, "2475 q6 b")
eq(sum(o for o in ops if o < 0), -394, "2475 q6 négatifs"); eq(-19 + 19, 0, "2475 q7")

# ====================================================================== 2476 semaine
S = [-6, -2, 1, -4, 3, -1, -5]
ok(min(S) == -6 and max(S) == 3, "2476 q1"); eq(max(S) - min(S), 9, "2476 q2")
eq(sum(v for v in S if v < 0), -18, "2476 q3"); eq(sum(S), -14, "2476 q4"); eq(R(sum(S), 7), -2, "2476 q5")
eq(8 * (-1) - sum(S), 6, "2476 q6"); eq(R(sum(S) + 6, 8), -1, "2476 q6 vérif")

# ====================================================================== 2477 expressions en x = -3
ex = {"A": 5 * x - 7, "B": -2 * x + 4, "C": x * (x + 4), "D": (2 - x) * (x - 1), "E": x * x - 2 * x}
vals = {k: e.subs(x, -3) for k, e in ex.items()}
ok(vals == {"A": -22, "B": 10, "C": -3, "D": -20, "E": 15}, f"2477 valeurs {vals}")
ok(sorted(vals, key=vals.get) == ["A", "D", "C", "B", "E"], "2477 q6 ordre")

# ====================================================================== 2478 sous-marin et drone
sm = lambda t: -240 + 12 * t
dr = lambda t: 85 - 5 * t
eq(sm(8), -144, "2478 q1"); eq(dr(8), 45, "2478 q2"); eq(dr(8) - sm(8), 189, "2478 q3")
eq(dr(0) - sm(0), 325, "2478 q4 départ"); eq(325 - 8 * 17, 189, "2478 q4")
ok(solve(sm(x), x) == [20], "2478 q5"); ok(solve(dr(x), x) == [17], "2478 q6a"); eq(sm(17), -36, "2478 q6b")
eq(dr(20), -15, "2478 erreur fréquente")
ok(solve(dr(x) - sm(x) - 121, x) == [12], "2478 q7"); eq(sm(12), -96, "2478 q7 sm"); eq(dr(12), 25, "2478 q7 drone")

# ====================================================================== 2479 Fahrenheit
F = lambda c: d("1,8") * c + 32
eq(d("56,7") - d("-89,2"), d("145,9"), "2479 q1")
eq(F(0), 32, "2479 q2a"); eq(F(100), 212, "2479 q2b")
eq(d("1,8") * d("-89,2"), d("-160,56"), "2479 q3 produit"); eq(F(d("-89,2")), d("-128,56"), "2479 q3")
eq(d("1,8") * d("56,7"), d("102,06"), "2479 q4 produit"); eq(F(d("56,7")), d("134,06"), "2479 q4")
eq(F(-40), -40, "2479 q5"); ok(solve(F(x) - x, x) == [-40], "2479 q5 seule solution")
eq(-4 - 32, -36, "2479 q6a"); eq(R(-36) / d("1,8"), -20, "2479 q6"); eq(F(-20), -4, "2479 q6 vérif")
eq(F(d("56,7")) - F(d("-89,2")), d("262,62"), "2479 q7"); eq(d("1,8") * d("145,9"), d("262,62"), "2479 q7b")

# ====================================================================== 2480 carré magique
a_, b_, c_ = 3, 1, -1
M = [[a_, -4, b_], [-2, 0, 2], [c_, 4, -3]]
lignes = M + [list(col) for col in zip(*M)] + [[M[i][i] for i in range(3)], [M[i][2 - i] for i in range(3)]]
ok(all(sum(l) == 0 for l in lignes), "2480 carré magique")
ok(all(sum(v + 5 for v in l) == 15 for l in lignes), "2480 q6")
eq(prod(*M[0]), -12, "2480 q7a"); eq(prod(*[v for l in M for v in l]), 0, "2480 q7b")

# ====================================================================== 2481 pyramides
def pyramide(base):
    etages = [list(base)]
    while len(etages[-1]) > 1:
        e = etages[-1]
        etages.append([e[i] * e[i + 1] for i in range(len(e) - 1)])
    return etages


ok(pyramide([-2, 3, -1, 4]) == [[-2, 3, -1, 4], [-6, -3, -4], [18, 12], [216]], "2481 pyramide 1")
ok(pyramide([-2, 3, -1, -4]) == [[-2, 3, -1, -4], [-6, -3, 4], [18, -12], [-216]], "2481 q3")
eq(R(-15, 5), -3, "2481 q4")
ok(pyramide([5, -3, -2]) == [[5, -3, -2], [-15, 6], [-90]], "2481 pyramide 2")
ok(expand(pyramide([n, -3, -2])[-1][0]) == -18 * n, "2481 q6 sommet")
ok(solve(-18 * n - 18, n) == [-1], "2481 q6"); ok(pyramide([-1, -3, -2])[-1][0] == 18, "2481 q6 vérif")

# ====================================================================== 2482 programme de calcul
prog = lambda v: (v * (-4) + 6) / R(-2)
ok([prog(v) for v in (5, -3, 0, d("1,5"))] == [7, -9, -3, 0], "2482 q1-3")
ok(all(prog(v) == 2 * v - 3 for v in (5, -3, 0, d("1,5"))), "2482 q4")
ok(solve(2 * x - 3 - 11, x) == [7], "2482 q5"); eq(prog(7), 11, "2482 q5 vérif")
ok(simplify(prog(x) - (2 * x - 3)) == 0, "2482 q6 démonstration")

# ====================================================================== 2483 randonnée
var = [320, -150, 410, -275, -305]
alt = [850]
for v in var:
    alt.append(alt[-1] + v)
ok(alt == [850, 1170, 1020, 1430, 1155, 850], f"2483 altitudes {alt}")
eq(max(alt) - 850, 580, "2483 q3"); eq(sum(v for v in var if v > 0), 730, "2483 q4")
eq(sum(v for v in var if v < 0), -730, "2483 q5"); eq(sum(var), 0, "2483 q6")

# ====================================================================== 2484 fuseaux horaires
U = {"LA": -8, "NY": -5, "Paris": 1, "Tokyo": 9}
eq(U["NY"] - U["Paris"], -6, "2484 q1"); eq(14 + (U["NY"] - U["Paris"]), 8, "2484 q2")
eq(U["Tokyo"] - U["Paris"], 8, "2484 q3a"); eq(14 + 8, 22, "2484 q3")
eq(U["LA"] - U["Paris"], -9, "2484 q4a"); eq(14 - 9, 5, "2484 q4")
eq(R(10 * 60 + 8 * 60 + 30 - 6 * 60, 60), R(25, 2), "2484 q5 (12 h 30)")
eq(U["Paris"] - U["Tokyo"], -8, "2484 q6a"); eq(11 - 8 + 14, 17, "2484 q6"); eq((11 + 14) - 8, 17, "2484 q6 vérif")
eq(U["Tokyo"] - U["LA"], 17, "2484 q7a"); eq((9 + 17) % 24, 2, "2484 q7")

print(f"verif_249 : {n_ok} contrôles, tout est juste.")
