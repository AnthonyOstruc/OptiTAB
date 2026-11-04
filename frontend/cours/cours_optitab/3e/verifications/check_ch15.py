# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 15 (Transformations et homothéties)."""
import math
from fractions import Fraction as F

T = [(2, 1), (4, 1), (3, 3)]
T2 = [(1, 2), (3, 2), (2, 4)]
sym_y = lambda p: (-p[0], p[1])          # noqa: E731
sym_o = lambda p: (-p[0], -p[1])         # noqa: E731
rot90 = lambda p: (-p[1], p[0])          # noqa: E731
homo = lambda k: (lambda p: (F(k) * p[0], F(k) * p[1]))  # noqa: E731
dist = lambda a, b: math.hypot(a[0] - b[0], a[1] - b[1])  # noqa: E731
aire = lambda a, b, c: abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])) / F(2)  # noqa: E731

# Cours
assert homo(2)((2, 1)) == (4, 2) and homo("-1.5")((2, 1)) == (-3, F(-3, 2))

# Découverte
assert [sym_y(p) for p in T] == [(-2, 1), (-4, 1), (-3, 3)]                    # D1
assert dist(*T[:2]) == dist(sym_y(T[0]), sym_y(T[1])) == 2                     # D1
assert sym_o((3, 2)) == (-3, -2) and sym_o((-1, 4)) == (1, -4)                 # D2
assert [(x + 3, y + 1) for x, y in T2] == [(4, 3), (6, 3), (5, 5)]             # D3
assert (8 - 3, 6 - 1) == (5, 5)                                                # D3
assert [rot90(p) for p in T] == [(-1, 2), (-1, 4), (-3, 3)]                    # D4
assert math.isclose(dist((0, 0), (2, 1)), dist((0, 0), rot90((2, 1))))         # D4
assert sym_o((2, 1)) == (-2, -1) and 4 * 90 == 360                             # D4
assert 4 + 6 + 7 == 17 and 17 * 3 == 51 and 12 * 3 ** 2 == 108                 # D5

# Entraînement
assert [homo(2)(p) for p in T] == [(4, 2), (8, 2), (6, 6)]                     # E1
assert aire(*T) == 2 and aire(*[homo(2)(p) for p in T]) == 8                   # E1
assert math.isclose(dist((0, 0), (4, 2)), 2 * dist((0, 0), (2, 1)))            # E1
img = [homo("-1.5")(p) for p in T]
assert img == [(-3, F(-3, 2)), (-6, F(-3, 2)), (F(-9, 2), F(-9, 2))]           # E2
assert dist(img[0], img[1]) == 3 and aire(*img) == F(9, 2)                     # E2
assert F(10, 4) == F(5, 2) and 3 * F(5, 2) == F(15, 2) and 6 * F(5, 2) ** 2 == F(75, 2)  # E3
assert 18 * 3 == 54 and 20 * 9 == 180 and 18 * F(1, 2) == 9 and 20 * F(1, 4) == 5  # E4
assert 50 * 2 ** 3 == 400 and 50 * F(1, 5) ** 3 == F(2, 5)                     # E4
assert F(30, 100) == F(3, 10) and F(450, 10000) * 10000 == 450                 # E5 (m² -> cm²)
assert F(6000, 100 ** 3) * 100 ** 3 == 6000 and 6000 / 1000 == 6               # E5
assert 5 * 4 == 20 and 3 * 4 == 12 and 100 // 4 == 25                         # E6
assert 360 / 8 == 45 and 3 * 45 == 135 and 360 / 12 == 30                      # E7
assert round(360 / 7, 1) == 51.4                                               # E7

# Problèmes
O = (-1, -1)
assert ((O[0] + 3) / 2, (O[1] + 3) / 2) == (1, 1)                              # P1
assert ((O[0] + 7) / 2, (O[1] + 3) / 2) == (3, 1)                              # P1
assert (O[0] + 2 * (1 - O[0]), O[1] + 2 * (1 - O[1])) == (3, 3)                # P1
assert (O[0] + 2 * (3 - O[0]), O[1] + 2 * (1 - O[1])) == (7, 3)                # P1
assert F(75, 12) == F(25, 4) and math.sqrt(6.25) == 2.5 and 4 * 2.5 == 10      # P2
assert (-2) * (-0.5) == 1 and 3 * 2 * 0.5 == 3 and 3 * (-2) == -6              # P3
assert 5 ** 2 == 3 ** 2 + 4 ** 2 and 3 * 4 / 2 == 6                            # P4
assert (24, 32, 40) == (3 * 8, 4 * 8, 5 * 8) and 24 * 32 / 2 == 384 == 6 * 8 ** 2  # P4
assert round(384 * 0.02, 2) == 7.68                                            # P4
assert 400 / 5 == 80 and round(3.6 * 80, 6) == 288                             # P5
assert round(8.64 * 80 ** 2, 6) == 55296 and round(55296 / 10000, 2) == 5.53   # P5
assert round(216 / 3.6, 6) == 60 and 60 * 5 == 300 and math.isclose(3.6 * 2.4, 8.64)  # P5
A, B, C = (1, 1), (5, 2), (6, 5)
t = (A[0] - B[0], A[1] - B[1])
D = (C[0] + t[0], C[1] + t[1])
assert t == (-4, -1) and D == (2, 4)                                           # P6
assert ((A[0] + C[0]) / 2, (A[1] + C[1]) / 2) == ((B[0] + D[0]) / 2, (B[1] + D[1]) / 2) == (3.5, 3)  # P6
assert math.isclose(dist(A, B), math.sqrt(17)) and math.isclose(dist(C, D), math.sqrt(17))  # P6
assert F(225, 9) == 25 and F(1350, 27) == 50 and 1350 - 50 == 1300             # P7
assert F(1300, 1350) == F(26, 27)                                              # P7

print("check_ch15 : tous les contrôles passent.")
