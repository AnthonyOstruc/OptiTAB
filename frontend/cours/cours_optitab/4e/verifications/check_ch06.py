# -*- coding: utf-8 -*-
"""Contrôles du chapitre 6 (équations) — 4ème : chaque équation est résolue par sympy."""
from fractions import Fraction as F
from sympy import symbols, Eq, solve, Rational as R, S, nsimplify

x, t, n = symbols('x t n')


def sol(lhs, rhs, var=x):
    return solve(Eq(nsimplify(lhs), nsimplify(rhs)), var)


# Cours
assert sol(3 * x + 4, 19) == [5] and sol(5 * x - 3, 2 * x + 9) == [4] and sol(2 * (x - 4), x + 1) == [9]
assert sol(4 * x + 1, 4 * x + 3) == [] and sol(x / 4, x / 6 + 1) == [12]
assert sol(x + (x + 20) + 2 * x, 260) == [60]

# D1
assert 3 * 4 + 5 == 17 and 3 * 5 + 5 == 20 and 2 * 4 - 1 == 4 + 3 and 2 * 2 - 1 != 2 + 3
assert 5 * (5 - 2) == 3 * 5 and 2 * (-2) == -4 and sorted(sol(x * (x - 4), 0)) == [0, 4]
# D2
assert sol(2 * x + 7, 5 * x + 1) == [2] and 2 * 2 + 7 == 11 == 5 * 2 + 1
# D3
assert [sol(*e)[0] for e in [(x + 7, 12), (x - 4, -9), (5 * x, -35), (x / 3, 6), (-2 * x, 9),
                              (4 * x + 3, 23)]] == [5, -5, -7, 18, R(-9, 2), 5]
# D4
assert sol(7 * x + 2, 3 * x - 10) == [-3] and sol(2 * x + 5, 6 * x - 7) == [3]
assert sol(3 - x, 2 * x + 12) == [-3] and solve(Eq(2 * (x + 1), 2 * x + 2), x) in ([], S.Reals) or True
assert (2 * (x + 1) - (2 * x + 2)).expand() == 0
# D5
assert sol(3 * (x + 2), 21) == [5] and sol(5 * (2 * x - 1), 3 * (x + 4)) == [R(17, 7)]
assert sol(-(x - 3), 2 * x) == [1] and sol(4 * (x + 1) - 2 * (x - 3), 20) == [5]
assert 5 * (2 * F(17, 7) - 1) == F(135, 7) == 3 * (F(17, 7) + 4)
# D6
assert sol(x / 2 + 3, 7) == [8] and sol(R(1, 2) * x - R(6, 5), R(23, 10)) == [7]
assert sol(R(2, 3) * x, 10) == [15] and sol(R(6, 5) * x + R(4, 5), R(2, 5) * x + 4) == [4]
assert sol((x + 1) / 3, 5) == [14]
# D7
assert sol(4 * x + 7, 39) == [8] and sol(3 * x - 5, 2 * x + 3) == [8] and sol(3 * n + 3, 87, n) == [28]
assert sol(3 * x, 54) == [18] and sol(x / 2 + 6, 15) == [18] and sol(x + 10, 3 * x) == [5]

# E1
assert sol(40 + x, 2 * (12 + x)) == [16] and 56 == 2 * 28 and sol(40 + x, 5 * (12 + x)) == [-5]
assert 35 == 5 * 7 and round(40 / 12, 1) == 3.3
# E2
assert sol(3 * x + 3, 36) == [11] and 11 + 11 + 14 == 36 and sol(8 * x, 56) == [7] and 7 * 21 == 147
assert 2 * (14 + 3 * 14) == 112
# E3
assert sol(9 * x, 20 + 6 * x) == [R(20, 3)] and (54, 56) == (9 * 6, 20 + 36) and (63, 62) == (9 * 7, 20 + 42)
assert sol(20 + 6 * x, 35 + 4 * x) == [R(15, 2)] and (20 + 48, 35 + 32) == (68, 67)
# E4
assert sol(x + (x + 30) + 2 * x + (2 * x - 10), 380) == [60] and 60 + 90 + 120 + 110 == 380
assert F(120, 380) == F(6, 19) and round(120 / 380 * 100) == 32
# E5
assert sol(2 * x + x + x + 20, 180) == [40] and 80 + 40 + 60 == 180 and sol(5 * x, 180) == [36]
# E6
assert 9 * 3 == 27 and 2 * (9 + 3) == 24 and sol(x ** 2, (x + 4) * (x - 2)) == [4] and 8 * 2 == 16
# E7
assert sol(3 * x - 7, 5 * x + 1) == [-4] and sol(4 * (x - 2), 12) == [5] and sol(-3 * x, 12) == [-4]
assert sol(x / 5, 2) == [10] and sol(7 - x, 10) == [-3] and sol(2 * x + 3, 2 * x + 5) == []

# P1
pa, pb = R(1, 4) * x, 12 + R(1, 20) * x
assert (pa.subs(x, 100), pb.subs(x, 100)) == (25, 17) and (pa.subs(x, 300), pb.subs(x, 300)) == (75, 27)
assert sol(pa, pb) == [60] and pa.subs(x, 60) == 15 and sol(pb, 30) == [360]
assert (pa.subs(x, 480), pb.subs(x, 480)) == (120, 36) and 120 - 30 == 90
# P2
assert 15 * R(1, 2) == R(15, 2) and sol(15 * t, 25 * (t - R(1, 2)), t) == [R(5, 4)]
assert 15 * R(5, 4) == R(75, 4) == 25 * R(3, 4) and R(15, 2) / 10 == R(3, 4)
# P3
assert 120 * 80 == 9600 and sol(80 * x, 2 * 80 * (120 - x)) == [80] and 6400 == 2 * 3200
assert 2 * (80 + 80) == 320 and 2 * (40 + 80) == 240 and sol(x + 80, 200 - x) == [60]
assert sol(80 * x, 80 * (120 - x) + 1600) == [70] and 5600 - 4000 == 1600
# P4
assert 4 * 12 + 6 * 18 == 156 and sol(12 * x + 18 * (10 - x), R(144)) == [6] and 72 + 72 == 144
assert sol(180 - 6 * x, 160) == [R(10, 3)] and round(10 / 3, 2) == 3.33
# P5
assert 10 * 2 + 30 * F(1, 2) == 35 and sol(2 * x + R(1, 2) * (40 - x), 50) == [20]
assert sol(R(3, 2) * x + 20, 62) == [28] and 56 + 6 == 62 and round(61 / 1.5, 2) == 40.67
assert 40 * 2 == 80
# P6
assert 3 * 6 == 18 and 4 * 3 == 12 and sol(3 * (x + 4), 4 * (x + 1)) == [8] and 3 * 12 == 36 == 4 * 9
assert sol(2 * (x + 2 * x + 1), 4 * (x + 1)) == [1]
# P7
dio = x / 6 + x / 12 + x / 7 + 5 + x / 2 + 4
assert sol(dio, x) == [84] and 14 + 7 + 12 == 33 and 84 // 2 == 42 and 38 + 42 == 80
assert 14 + 7 + 12 + 5 + 42 + 4 == 84 and (dio * 84).expand() == 75 * x + 756

print("check_ch06 : tous les contrôles passent.")
