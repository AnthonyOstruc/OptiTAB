# -*- coding: utf-8 -*-
"""Vérification (sympy) de tous les résultats de la notion 170 « Droites du plan »."""
from fractions import Fraction as Fr

import sympy as sp

x, y, t, a, e = sp.symbols("x y t a e")
ok = 0


def check(cond, msg):
    global ok
    assert cond, msg
    ok += 1


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


def vec(A, B):
    return (B[0] - A[0], B[1] - A[1])


def eq_det(A, u):
    """det(AM, u) développé."""
    return sp.expand((x - A[0]) * u[1] - (y - A[1]) * u[0])


def pente(A, B):
    return Fr(B[1] - A[1], B[0] - A[0])


def meme_droite(e1, e2):
    """Deux équations cartésiennes (expressions = 0) proportionnelles."""
    c1 = [e1.coeff(x), e1.coeff(y), e1.subs({x: 0, y: 0})]
    c2 = [e2.coeff(x), e2.coeff(y), e2.subs({x: 0, y: 0})]
    return sp.Matrix([c1, c2]).rank() == 1


# ---------------------------------------------------------------- cours
check(eq_det((2, 1), (3, 2)) == 2 * x - 3 * y - 1, "cours ex. 1")
check(2 * 8 - 3 * 5 - 1 == 0 and 2 * 1 - 3 * 1 - 1 == -2, "cours appartenance")
m = pente((2, 1), (5, 5))
check(m == Fr(4, 3) and 1 - m * 2 == Fr(-5, 3), "cours pente")
check(2 * (-6) - 4 * (-3) == 0, "cours parallèles")
s = sp.solve([y - (2 * x - 1), x + y - 5], [x, y])
check(s == {x: 2, y: 3}, "cours substitution")
s = sp.solve([2 * x + 3 * y - 12, x - y - 1], [x, y])
check(s == {x: 3, y: 2}, "cours combinaison")
check(det(vec((-1, 2), (2, 8)), vec((-1, 2), (5, 14))) == 0, "cours alignes")
# figure panorama : d2 y = -x/2 + 2 coupe d1 y = 2x + 1
check(sp.solve(2 * x + 1 - (-x / 2 + 2), x) == [sp.Rational(2, 5)], "panorama")


# ---------------------------------------------------------------- 2054 (Python)
def alignes(A, B, C):
    ux, uy = B[0] - A[0], B[1] - A[1]
    vx, vy = C[0] - A[0], C[1] - A[1]
    return ux * vy - uy * vx == 0


def equation_droite(A, B):
    if A == B:
        return None
    xA, yA = A
    xB, yB = B
    return (yA - yB, xB - xA, xA * yB - xB * yA)


check(alignes((-1, 0), (2, 3), (5, 6)) is True, "2054 q1")
check(alignes((0, 1), (2, 2), (4, 6)) is False and det((2, 1), (4, 5)) == 6, "2054 q2")
check(equation_droite((-1, 0), (5, 6)) == (-6, 6, -6), "2054 q3")
check(2 - 3 + 1 == 0, "2054 q3 (2;3) sur x - y + 1 = 0")
check(equation_droite((2, 3), (2, 3)) is None, "2054 q4")
check(equation_droite((2, -1), (2, 5)) == (-6, 0, 12), "2054 q5")
xA, yA, xB, yB = sp.symbols("xA yA xB yB")
aa, bb, cc = yA - yB, xB - xA, xA * yB - xB * yA
check(sp.expand(aa * xA + bb * yA + cc) == 0 and sp.expand(aa * xB + bb * yB + cc) == 0, "2054 q6")
check((-bb, aa) == (xA - xB, yA - yB), "2054 q6 vecteur")

# ---------------------------------------------------------------- 2046 (lecture graphique)
check(2 * 1 - 3 == -1 and Fr(-2, 3) * 3 + 2 == 0, "2046 points de lecture")

# ---------------------------------------------------------------- 2045
A, B, C, D = (-2, 3), (4, -1), (2, -5), (2, 4)
check(vec(A, B) == (6, -4), "2045 q1")
check(pente(A, B) == Fr(-2, 3), "2045 q2")
check(Fr(-2, 5) == Fr(-2, 5) and det((3, -2), (5, -2)) == 4, "2045 q4 q5")
check(Fr(-2, 3) * 4 + Fr(5, 3) == -1 and Fr(-2, 3) * (-2) + Fr(5, 3) == 3, "2045 figure (AB)")

# ---------------------------------------------------------------- 2051
check(det(vec((-1, 2), (2, 8)), vec((-1, 2), (5, 14))) == 0, "2051 q1")
check(det(vec((0, 1), (2, 3)), vec((0, 1), (4, 6))) == 2, "2051 q2")
G, H = (1, -2), (4, 1)
check(sp.solve(det(vec(G, H), (t - 1, 5)), t) == [6], "2051 q3")
check(pente((-1, 2), (2, 8)) == 2 and 2 - 2 * (-1) == 4 and 2 * 5 + 4 == 14, "2051 q4")
check(2 * 7 + 4 == 18, "2051 q5")

# ---------------------------------------------------------------- 2049
m = pente((1, 2), (5, 4))
check(m == Fr(1, 2) and 2 - m == Fr(3, 2), "2049 q1")
check(meme_droite(y - (x / 2 + sp.Rational(3, 2)), x - 2 * y + 3), "2049 q1 cart")
check(1 - (-3) * (-3) == -8, "2049 q2")
check(eq_det((2, -1), (4, -2)) == -2 * x - 4 * y, "2049 q3")
check(eq_det((-2, 4), vec((-2, 4), (3, -1))) == -5 * x - 5 * y + 10, "2049 q5")
check(3 + (-1) - 2 == 0, "2049 q5 verif J")

# ---------------------------------------------------------------- 2047
check(-3 * 0 + 2 == 2 and -3 * 3 + 5 == -4, "2047")

# ---------------------------------------------------------------- 2052
check(2 * (-6) - 4 * (-3) == 0 and 2 - 3 + 1 == 0 and 4 - 6 - 5 == -7, "2052 q1")
check(meme_droite(y - (x / 2 - 1), x - 2 * y - 2), "2052 q2")
check(3 * 2 + (-1) - 5 == 0, "2052 q4")
check(sp.solve([y + x - 4, y - 2 * x + 2], [x, y]) == {x: 2, y: 2}, "2052 q5")

# ---------------------------------------------------------------- 2048
check(sp.solve(3 * x - 2 * y + 6, y) == [3 * x / 2 + 3], "2048 q2")
check(sp.solve(5 * x + 10 * y - 15, y) == [-x / 2 + sp.Rational(3, 2)], "2048 q3")
check(det(vec((0, 2), (1, 1)), vec((0, 2), (-1, 1))) != 0, "2048 q5 b")
check(det(vec((0, 1), (1, Fr(1, 2))), vec((0, 1), (3, Fr(1, 4)))) == Fr(3, 4), "2048 q5 d")

# ---------------------------------------------------------------- 2050
check(Fr(3, 2) * 2 - 1 == 2, "2050 q1")
check(sp.solve(4 * x - 8, x) == [2] and sp.solve(2 * y - 8, y) == [4], "2050 q2")
check(-4 + 5 == 1, "2050 q4")
check(Fr(1, 2) * 4 + 3 == 5 and 0 - 2 * 3 + 6 == 0 and 4 - 2 * 5 + 6 == 0, "2050 q5")

# ---------------------------------------------------------------- 2053
check(sp.solve([2 * x + y - 8, x - y - 1], [x, y]) == {x: 3, y: 2}, "2053 q1")
check(sp.solve(4 * x + 2 * y - 10, y) == [5 - 2 * x], "2053 q2")
check(meme_droite(3 * x - y + 6, 6 * x - 2 * y + 12), "2053 q3")
check(sp.solve([y - x + 2, y - x / 2 - 1], [x, y]) == {x: 6, y: 4}, "2053 q4")
check(sp.solve([x + 2 * y - 4, 3 * x - y - 5], [x, y]) == {x: 2, y: 1}, "2053 q5")

# ---------------------------------------------------------------- nouveau-1 (musée)
check(5 * 4 - 2 * 3 == 14, "n1 q2")
check(sp.solve([5 * a + 3 * e - 63, 2 * a + 4 * e - 42], [a, e]) == {a: 9, e: 6}, "n1 q3")
check(2 * 9 + 3 * 6 == 36, "n1 q5")

# ---------------------------------------------------------------- nouveau-2 (location)
m = pente((2, 15), (6, 21))
check(m == Fr(3, 2) and 15 - m * 2 == 12, "n2 q1")
check(sp.solve(sp.Rational(3, 2) * x + 12 - 3 * x, x) == [8] and 3 * 8 == 24, "n2 q4")
check(sp.solve_univariate_inequality(3 * x < sp.Rational(3, 2) * x + 12, x)
      == sp.And(-sp.oo < x, x < 8), "n2 q5")

print(f"{ok} contrôles : tout est juste.")
