# -*- coding: utf-8 -*-
"""Vérification sympy de la notion 256 (4e) : Équations et résolution de problèmes.

Chaque équation du cours, de la fiche et des 21 exercices est résolue avec sympy,
chaque vérification et chaque valeur numérique citée est recalculée.
    python verif_256.py   ->  « N contrôles, 0 erreur »
"""
from sympy import Rational as R, S, Eq, solveset, symbols, expand, simplify, FiniteSet, EmptySet

x, n, t, l = symbols("x n t l")
OK, KO = [0], []


def chk(cond, msg):
    if cond:
        OK[0] += 1
    else:
        KO.append(msg)


def sol(lhs, rhs, attendu, var=x, msg=""):
    """attendu : nombre, 'aucune' ou 'tous'."""
    s = solveset(Eq(lhs, rhs), var, domain=S.Reals)
    if attendu == "aucune":
        chk(s == EmptySet, f"{msg} : attendu aucune solution, obtenu {s}")
    elif attendu == "tous":
        chk(s == S.Reals, f"{msg} : attendu tous les réels, obtenu {s}")
    else:
        chk(s == FiniteSet(S(attendu)), f"{msg} : attendu {attendu}, obtenu {s}")


def egal(a, b, msg):
    chk(simplify(S(a) - S(b)) == 0, f"{msg} : {a} != {b}")


def dev(e, attendu, msg):
    chk(expand(e - attendu) == 0, f"{msg} : {expand(e)} != {attendu}")


# ------------------------------------------------------------------ COURS 251
egal(4 * 3 - 1, 11, "cours test 3 gauche"); egal(2 * 3 + 5, 11, "cours test 3 droite")
egal(4 * 4 - 1, 15, "cours test 4 gauche"); egal(2 * 4 + 5, 13, "cours test 4 droite")
sol(3 * x + 2, x + 10, 4, msg="cours balance"); sol(2 * x, 8, 4, msg="cours balance 2"); egal(3 * 4 + 2, 4 + 10, "cours balance v")
sol(x + 8, 3, -5, msg="cours tableau 1"); sol(x - 6, 10, 16, msg="cours tableau 2")
sol(4 * x, 26, R(13, 2), msg="cours tableau 3"); sol(-3 * x, 12, -4, msg="cours tableau 4")
sol(x / 5, -2, -10, msg="cours tableau 5")
sol(7 * x - 5, 3 * x + 11, 4, msg="cours ex 1"); egal(7 * 4 - 5, 23, "cours ex1 verif"); egal(3 * 4 + 11, 23, "cours ex1 verif d")
sol(4 * (x - 3), 2 * (x + 1) + 6, 10, msg="cours ex 2"); egal(4 * 7, 28, "c2"); egal(2 * 11 + 6, 28, "c2d")
sol(8 - 3 * x, x - 4, 3, msg="cours ex 3"); egal(8 - 9, -1, "c3"); egal(3 - 4, -1, "c3d")
sol(3 * x, 7, R(7, 3), msg="cours 3x=7")
sol(R(1, 2) * x + R(12, 10), R(37, 10), 5, msg="cours décimaux"); sol(5 * x + 12, 37, 5, msg="cours x10")
sol(x / 3, x / 5 + 2, 15, msg="cours fractions"); sol(5 * x, 3 * x + 30, 15, msg="cours x15")
sol(3 * x + 5, 3 * x - 1, "aucune", msg="cours aucune"); sol(3 * (x - 2), 3 * x - 6, "tous", msg="cours tous")
sol(x + 4, 10, 6, msg="cours erreur 1"); sol(-3 * x, 12, -4, msg="cours erreur 2")
dev(3 * (2 * x - 5), 6 * x - 15, "cours dev"); dev(-(x - 3), -x + 3, "cours dev 2")
sol(x + (x + 20) + 2 * x, 260, 60, msg="cours partage"); egal(60 + 80 + 120, 260, "cours partage verif")

# ------------------------------------------------------------------ FICHE 171
sol(4 * (x - 3), 2 * x + 8, 10, msg="fiche ex"); egal(4 * 7, 2 * 10 + 8, "fiche verif")
sol(3 * x - 7, 5, 4, msg="fiche erreur 1 (3x = 12)"); sol(-2 * x, 8, -4, msg="fiche erreur 2")

# ------------------------------------------------------------------ 2600
egal(3 * 4 + 5, 17, "2600 q1a"); egal(3 * 5 + 5, 20, "2600 q1b")
egal(2 * 4 - 1, 7, "2600 q2a"); egal(4 + 3, 7, "2600 q2a d"); egal(2 * 2 - 1, 3, "2600 q2b"); egal(2 + 3, 5, "2600 q2b d")
egal(5 * (5 - 2), 15, "2600 q3"); egal(3 * 5, 15, "2600 q3 d")
egal(7 - 2 * (-2), 11, "2600 q4"); egal(-2 + 13, 11, "2600 q4 d"); egal(7 - 2 * 2, 3, "2600 q4 piège")
egal(3 ** 2, 9, "2600 q5"); egal((-3) ** 2, 9, "2600 q5b")
for v, g, d in [(-1, -10, -2), (0, -4, 2), (2, 8, 10), (3, 14, 14)]:
    egal(6 * v - 4, g, f"2600 q6 g {v}"); egal(4 * v + 2, d, f"2600 q6 d {v}")
sol(6 * x - 4, 4 * x + 2, 3, msg="2600 q6 unique")

# ------------------------------------------------------------------ 2601
sol(3 * x + 4, 19, 5, msg="2601 b1"); sol(3 * x, 15, 5, msg="2601 b1 étape")
sol(2 * x + 7, 5 * x + 1, 2, msg="2601 b2"); sol(7, 3 * x + 1, 2, msg="2601 b2 étape"); sol(6, 3 * x, 2, msg="2601 b2 fin")
egal(2 * 2 + 7, 11, "2601 v"); egal(5 * 2 + 1, 11, "2601 v d")

# ------------------------------------------------------------------ 2602
for e, r, a in [(x + 7, 12, 5), (x - 4, -9, -5), (5 * x, -35, -7), (x / 3, 6, 18), (-2 * x, 9, R(-9, 2)), (4 * x + 3, 23, 5)]:
    sol(e, r, a, msg=f"2602 {e} = {r}")
egal(-2 * R(9, 2), -9, "2602 piège")

# ------------------------------------------------------------------ 2603
for e, r, a in [(5 * x - 3, 2 * x + 9, 4), (7 * x + 2, 3 * x - 10, -3), (2 * x + 5, 6 * x - 7, 3),
                (3 - x, 2 * x + 12, -3), (4 * x + 1, 4 * x + 3, "aucune"), (2 * (x + 1), 2 * x + 2, "tous")]:
    sol(e, r, a, msg=f"2603 {e} = {r}")
egal(7 * (-3) + 2, -19, "2603 v2"); egal(3 * (-3) - 10, -19, "2603 v2d")
egal(2 * 3 + 5, 11, "2603 v3"); egal(6 * 3 - 7, 11, "2603 v3d"); egal(3 - (-3), 6, "2603 v4"); egal(2 * (-3) + 12, 6, "2603 v4d")

# ------------------------------------------------------------------ 2604
for e, r, a in [(3 * (x + 2), 21, 5), (2 * (x - 4), x + 1, 9), (5 * (2 * x - 1), 3 * (x + 4), R(17, 7)),
                (-(x - 3), 2 * x, 1), (4 * (x + 1) - 2 * (x - 3), 20, 5)]:
    sol(e, r, a, msg=f"2604 {e} = {r}")
dev(4 * (x + 1) - 2 * (x - 3), 2 * x + 10, "2604 q5 réduit")
egal(5 * (2 * R(17, 7) - 1), R(135, 7), "2604 q6 g"); egal(3 * (R(17, 7) + 4), R(135, 7), "2604 q6 d")
egal(4 * 6 - 2 * 2, 20, "2604 v5")

# ------------------------------------------------------------------ 2605
for e, r, a in [(x / 2 + 3, 7, 8), (R(1, 2) * x - R(6, 5), R(23, 10), 7), (R(2, 3) * x, 10, 15),
                (x / 4, x / 6 + 1, 12), (R(6, 5) * x + R(4, 5), R(2, 5) * x + 4, 4), ((x + 1) / 3, 5, 14)]:
    sol(e, r, a, msg=f"2605 {e} = {r}")
sol(12 * x + 8, 4 * x + 40, 4, msg="2605 q5 x10"); egal(R(6, 5) * 4 + R(4, 5), R(28, 5), "2605 v5")

# ------------------------------------------------------------------ 2606
for e, r, a in [(4 * x + 7, 39, 8), (3 * x - 5, 2 * x + 9, 14), (x + 2 * x, 54, 18), (x / 2 + 6, 17, 22), (x + 10, 3 * x, 5)]:
    sol(e, r, a, msg=f"2606 {e} = {r}")
sol(n + (n + 1) + (n + 2), 87, 28, var=n, msg="2606 consécutifs"); egal(28 + 29 + 30, 87, "2606 v3")
egal(3 * 14 - 5, 37, "2606 v2"); egal(2 * 14 + 9, 37, "2606 v2d")

# ------------------------------------------------------------------ 2607
egal(12 + 5, 17, "2607 q1"); egal(40 + 5, 45, "2607 q1b")
sol(40 + x, 2 * (12 + x), 16, msg="2607 q4"); egal(2 * 28, 56, "2607 v")
sol(40 + x, 5 * (12 + x), -5, msg="2607 q6"); egal(5 * 7, 35, "2607 q6 v")

# ------------------------------------------------------------------ 2608
sol(x + x + (x + 3), 36, 11, msg="2608 triangle"); egal(11 + 11 + 14, 36, "2608 v")
sol(2 * (l + 3 * l), 56, 7, var=l, msg="2608 rectangle"); egal(7 * 21, 147, "2608 aire")

# ------------------------------------------------------------------ 2609
A = lambda v: (v + 3) * 4
B = lambda v: 6 * v - 2
egal(A(2), 20, "2609 A2"); egal(B(2), 10, "2609 B2"); egal(A(-1), 8, "2609 A-1"); egal(B(-1), -8, "2609 B-1")
dev(A(x), 4 * x + 12, "2609 A(x)")
sol(4 * x + 12, 6 * x - 2, 7, msg="2609 q4"); egal(A(7), 40, "2609 v"); egal(B(7), 40, "2609 vB")
sol(4 * x + 12, 30, R(9, 2), msg="2609 q5"); sol(4 * x + 12, 4 * x + 5, "aucune", msg="2609 q6")

# ------------------------------------------------------------------ 2610
dev(x + (x + 30) + 2 * x + (2 * x - 10), 6 * x + 20, "2610 somme")
sol(6 * x + 20, 380, 60, msg="2610 q3"); egal(60 + 90 + 120 + 110, 380, "2610 v")
egal(6 * 100 + 20, 620, "2610 q5"); egal(100 + 130 + 200 + 190, 620, "2610 q5 v")

# ------------------------------------------------------------------ 2611
sol(2 * x + x + (x + 20), 180, 40, msg="2611 q3"); egal(80 + 40 + 60, 180, "2611 v")
sol(x + x + 3 * x, 180, 36, msg="2611 q6"); egal(36 + 36 + 108, 180, "2611 q6 v")

# ------------------------------------------------------------------ 2612
egal(9 * 3, 27, "2612 aire"); egal(2 * (9 + 3), 24, "2612 per")
dev(2 * ((x + 4) + (x - 2)), 4 * x + 4, "2612 périmètre"); sol(4 * x, 4 * x + 4, "aucune", msg="2612 q3")
dev((x + 4) * (x - 2), x ** 2 + 2 * x - 8, "2612 aire dev"); sol(x ** 2, (x + 4) * (x - 2), 4, msg="2612 q5")
egal(8 * 2, 16, "2612 v")

# ------------------------------------------------------------------ 2613
sol(3 * x - 7, 5 * x + 1, -4, msg="2613 q1"); chk(3 * 3 - 7 != 5 * 3 + 1, "2613 q1 élève faux")
sol(4 * (x - 2), 12, 5, msg="2613 q2"); sol(-3 * x, 12, -4, msg="2613 q3"); sol(x / 5, 2, 10, msg="2613 q4")
sol(2 * x + 3, 2 * x + 5, "aucune", msg="2613 q5"); sol(7 - x, 10, -3, msg="2613 q6")

# ------------------------------------------------------------------ 2614
pA = lambda v: R(1, 4) * v
pB = lambda v: 12 + R(1, 20) * v
for v, a, b in [(100, 25, 17), (300, 75, 27), (480, 120, 36)]:
    egal(pA(v), a, f"2614 A {v}"); egal(pB(v), b, f"2614 B {v}")
sol(pA(x), pB(x), 60, msg="2614 A=B"); egal(pA(60), 15, "2614 prix 60")
sol(pB(x), 30, 360, msg="2614 B=C"); sol(pA(x), 30, 120, msg="2614 A=C")
for v in [10, 30, 59]:
    chk(pA(v) < pB(v) and pA(v) < 30, f"2614 zone A {v}")
for v in [61, 100, 200, 359]:
    chk(pB(v) < pA(v) and pB(v) < 30, f"2614 zone B {v}")
for v in [361, 480, 1000]:
    chk(30 < pB(v) and 30 < pA(v), f"2614 zone C {v}")
egal(120 - 30, 90, "2614 économie")

# ------------------------------------------------------------------ 2615
egal(15 * R(1, 2), R(15, 2), "2615 q1")
sol(15 * t, 25 * (t - R(1, 2)), R(5, 4), var=t, msg="2615 q4")
egal(15 * R(5, 4), R(75, 4), "2615 Léo"); egal(25 * R(3, 4), R(75, 4), "2615 Mia")
egal(R(15, 2) / 10, R(3, 4), "2615 q6")

# ------------------------------------------------------------------ 2616
sol(80 * x, 2 * 80 * (120 - x), 80, msg="2616 q3"); egal(80 * 80, 2 * 80 * 40, "2616 v")
egal(2 * (80 + 80), 320, "2616 p1"); egal(2 * (40 + 80), 240, "2616 p2")
sol(2 * (x + 80), 2 * (120 - x + 80), 60, msg="2616 q6")
sol(80 * x, 80 * (120 - x) + 1600, 70, msg="2616 q7"); egal(80 * 70 - 80 * 50, 1600, "2616 q7 v")

# ------------------------------------------------------------------ 2617
egal(11 + 14 + 9, 34, "2617 somme"); chk(abs(34 / 3 - 11.33) < 0.005, "2617 moyenne")
sol((34 + x) / 4, 12, 14, msg="2617 q3"); sol((34 + 2 * x) / 5, 12, 13, msg="2617 q4")
sol((34 + 2 * x) / 5, 15, R(41, 2), msg="2617 q5"); egal(R(74, 5), R(148, 10), "2617 q6")

# ------------------------------------------------------------------ 2618
somme = lambda v: 2 * v + R(1, 2) * (40 - v)
for v, s_ in [(10, 35), (12, 38), (14, 41), (16, 44), (18, 47), (20, 50)]:
    egal(somme(v), s_, f"2618 tableur {v}")
dev(somme(x), R(3, 2) * x + 20, "2618 expression")
sol(R(3, 2) * x + 20, 50, 20, msg="2618 q4"); sol(R(3, 2) * x + 20, 62, 28, msg="2618 62")
sol(R(3, 2) * x + 20, 81, R(122, 3), msg="2618 81"); chk(abs(122 / 3 - 40.67) < 0.005, "2618 approx"); egal(somme(40), 80, "2618 max")

# ------------------------------------------------------------------ 2619
egal(4 * 3, 12, "2619 q1"); egal(3 * 9, 27, "2619 q1b")
dev(3 * (12 - x), 36 - 3 * x, "2619 q2")
sol(4 * x, 36 - 3 * x, R(36, 7), msg="2619 q3"); chk(round(36 / 7, 1) == 5.1, "2619 arrondi")
egal(4 * R(36, 7), R(144, 7), "2619 q4"); egal(3 * (12 - R(36, 7)), R(144, 7), "2619 q4b"); chk(round(144 / 7, 1) == 20.6, "2619 20,6")
chk(round(4 * 5.1, 1) == 20.4 and round(3 * (12 - 5.1), 1) == 20.7, "2619 piège arrondi")
sol(36 - 3 * x, 2 * 4 * x, R(36, 11), msg="2619 q5"); egal(36 - 3 * R(36, 11), R(288, 11), "2619 q5 v"); chk(round(36 / 11, 1) == 3.3, "2619 q5 arrondi")

# ------------------------------------------------------------------ 2620
eq = x / 6 + x / 12 + x / 7 + 5 + x / 2 + 4
sol(eq, x, 84, msg="2620 équation"); dev(84 * eq, 75 * x + 756, "2620 x84")
egal(14 + 7 + 12, 33, "2620 mariage"); egal(14 + 7 + 12 + 5 + 42 + 4, 84, "2620 somme")

print(f"{OK[0]} contrôles, {len(KO)} erreur(s)")
for m in KO:
    print("  ERREUR", m)
