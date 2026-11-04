# -*- coding: utf-8 -*-
"""Contrôles numériques et littéraux du chapitre 5 (calcul littéral) — 4ème."""
from fractions import Fraction as F
from sympy import symbols, expand, factor, simplify, Rational as R

x, a, b, n, y, k = symbols('x a b n y k')
eq = lambda e1, e2: simplify(expand(e1) - expand(e2)) == 0  # noqa: E731
A = 3 * x ** 2 - 2 * x + 5
B = (2 * x - 1) * (x + 3)

# Cours / fiche
assert A.subs(x, -1) == 10 and eq(7 * a - 2 + 3 * a + 9, 10 * a + 7)
assert eq(4 * x ** 2 + 3 * x - x ** 2 + x, 3 * x ** 2 + 4 * x)
assert eq(5 * (2 * a - 3), 10 * a - 15) and eq(-2 * (x - 6), -2 * x + 12) and eq(x * (x + 5), x ** 2 + 5 * x)
assert eq(-(3 * x - 7), -3 * x + 7) and eq(5 - (2 * x - 3), 8 - 2 * x)
assert eq((2 * x + 1) * (x + 4), 2 * x ** 2 + 9 * x + 4) and eq(12 * a - 18, 6 * (2 * a - 3))
assert eq(3 * x ** 2 - 6 * x, 3 * x * (x - 2)) and eq(n + (n + 1) + (n + 2), 3 * (n + 1))
assert (x + 3) ** 2 != x ** 2 + 9 and ((x + 3) ** 2).subs(x, 1) == 16
assert eq((x + 3) * (x + 2), x ** 2 + 5 * x + 6)

# D2
assert [A.subs(x, v) for v in (2, -1, 0, R(1, 2), -2)] == [13, 10, 5, R(19, 4), 21]
assert B.subs(x, 2) == 15 and B.subs(x, -3) == 0
# D3
assert eq(5 * y - 8 * y + 2, -3 * y + 2) and eq(2 * x * 3 * x, 6 * x ** 2)
# D4
assert [3 * m + 1 for m in range(1, 6)] == [4, 7, 10, 13, 16] and eq(4 + 3 * (n - 1), 3 * n + 1)
assert 3 * 100 + 1 == 301 and (61 - 1) // 3 == 20 and (100 - 1) % 3 == 0 and (100 - 1) // 3 == 33
# D5
assert eq(3 * (x + 4), 3 * x + 12) and eq(4 * (2 * x + 1) - 3 * (x - 2), 5 * x + 10)
assert (4 * (2 * x + 1) - 3 * (x - 2)).subs(x, 1) == 15
# D6
assert eq(5 * x + 15, 5 * (x + 3)) and eq(x ** 2 + 7 * x, x * (x + 7)) and eq(7 * y + 7, 7 * (y + 1))
assert str(factor(12 * a - 18)) == '6*(2*a - 3)'
# D7
assert eq(2 * (x + 5), 2 * x + 10) and F(1, 2) ** 2 < F(1, 2)
assert (3 * x + 2 * x).subs(x, 1) == (5 * x ** 2).subs(x, 1) and (3 * x + 2 * x).subs(x, 2) != (5 * x ** 2).subs(x, 2)
assert eq(x * (x + 1) - x, x ** 2)

# E1
assert eq((x - 3) * (x + 5), x ** 2 + 2 * x - 15) and eq((2 * a - 1) * (3 * a - 2), 6 * a ** 2 - 7 * a + 2)
assert eq((x + 4) ** 2, x ** 2 + 8 * x + 16) and 13 * 12 == 156 == 100 + 50 + 6
# E2
P, Ar = 2 * (2 * x + 3 + x), x * (2 * x + 3)
assert eq(P, 6 * x + 6) and eq(Ar, 2 * x ** 2 + 3 * x) and P.subs(x, 4) == 30 and Ar.subs(x, 4) == 44
assert P.subs(x, 6) == 42 and Ar.subs(x, 6) == 90 and Ar.subs(x, 8) == 152 and round(152 / 44, 2) == 3.45
# E3
pa, pb, pc = 2 * (x + 3) - 6, 4 * x - x - x, x * (x + 2) - x ** 2
assert eq(pa, 2 * x) and eq(pb, 2 * x) and eq(pc, 2 * x)
assert [e.subs(x, 5) for e in (pa, pb, pc)] == [10, 10, 10] and [e.subs(x, -2) for e in (pa, pb)] == [-4, -4]
# E4
bord = (x + 2) ** 2 - x ** 2
assert eq(bord, 4 * x + 4) and bord.subs(x, 3) == 16 and eq(bord, 4 * (x + 1))
assert bord.subs(x, R(13, 2)) == 30 and R(17, 2) ** 2 - R(13, 2) ** 2 == 30
# E5
assert eq(3 * x - (-x + 4), 4 * x - 4) and eq(2 * (x - 1) - (x + 5), x - 7)
assert eq(-3 * (2 - x) + 4 * x, 7 * x - 6) and eq(x * (x - 2) - 2 * (x - 2), x ** 2 - 4 * x + 4)
assert eq((x + 1) * (x - 1) - x ** 2, -1)
# E6
assert [2 * m + 2 for m in (1, 2, 3, 50, 14)] == [4, 6, 8, 102, 30]
assert eq(4 * n - 2 * (n - 1), 2 * n + 2) and eq(2 * (n + 1), 2 * n + 2)
# E7
assert 7 + 8 + 9 == 24 and 11 + 13 == 24 and 4 * 5 + 5 == 25
assert eq((2 * n + 1) + (2 * n + 3), 4 * (n + 1)) and eq(n * (n + 1) + (n + 1), (n + 1) ** 2)

# P1
grand = (2 * x + 2) * (x + 2)
assert eq(grand, 2 * x ** 2 + 6 * x + 4) and eq(grand - 2 * x * x, 6 * x + 4)
assert (6 * x + 4).subs(x, 4) == 28 == 10 * 6 - 8 * 4 and 28 * 45 == 1260
assert (6 * x + 4).subs(x, 6) == 40 == 14 * 8 - 12 * 6 and 2 * (2 * 4 + 4) == 24
# P2
grille = [[x - 3, x + 2, x + 1], [x + 4, x, x - 4], [x - 1, x - 2, x + 3]]
sommes = [sum(r) for r in grille] + [sum(grille[i][j] for i in range(3)) for j in range(3)]
sommes += [grille[0][0] + grille[1][1] + grille[2][2], grille[0][2] + grille[1][1] + grille[2][0]]
assert all(eq(s_, 3 * x) for s_ in sommes)
assert sorted(c.subs(x, 5) for r in grille for c in r) == list(range(1, 10))
assert [[c.subs(x, 5) for c in r] for r in grille] == [[2, 7, 6], [9, 5, 1], [4, 3, 8]]
assert [[c.subs(x, 10) for c in r] for r in grille] == [[7, 12, 11], [14, 10, 6], [9, 8, 13]]
assert [[c.subs(x, -2) for c in r] for r in grille] == [[-5, 0, -1], [2, -2, -6], [-3, -4, 1]]
# P3
assert 7 ** 2 - 6 ** 2 == 13 and 10 ** 2 - 9 ** 2 == 19 and eq((n - 1) ** 2, n ** 2 - 2 * n + 1)
assert eq(n ** 2 - (n - 1) ** 2, 2 * n - 1) and (25 + 1) // 2 == 13
assert 51 ** 2 - 50 ** 2 == 101 and 1001 ** 2 - 1000 ** 2 == 2001
# P4
assert eq((a + 1) * (a - 1), a ** 2 - 1) and 21 * 19 == 399 and eq((a + b) * (a - b), a ** 2 - b ** 2)
assert 102 * 98 == 9996 and 31 ** 2 == 961 and 99 ** 2 == 9801 and 48 * 52 == 2496
# P5
fond = (30 - 2 * x) * (20 - 2 * x)
assert eq(fond, 4 * x ** 2 - 100 * x + 600) and fond.subs(x, 4) == 264 == 22 * 12
vol = x * fond
assert [vol.subs(x, v) for v in (1, 2, 3, 4, 5, 6)] == [504, 832, 1008, 1056, 1000, 864]
assert max(range(1, 10), key=lambda v: vol.subs(x, v)) == 4 and 24 * 14 == 336
# P6
assert eq(2 * ((x + 5) + (x + 1)), 4 * x + 12) and eq(4 * (x + 3), 4 * x + 12)
assert eq((x + 5) * (x + 1), x ** 2 + 6 * x + 5) and eq((x + 3) ** 2 - (x + 5) * (x + 1), 4)
assert 7 * 3 == 21 and 5 ** 2 == 25
# P7
pA, pB = 8 * x, 30 + 5 * x
assert [pA.subs(x, 5), pB.subs(x, 5)] == [40, 55] and [pA.subs(x, 20), pB.subs(x, 20)] == [160, 130]
assert pA.subs(x, 10) == pB.subs(x, 10) == 80 and pB.subs(x, 18) == 120 and pA.subs(x, 30) - 120 == 120

print("check_ch05 : tous les contrôles passent.")
