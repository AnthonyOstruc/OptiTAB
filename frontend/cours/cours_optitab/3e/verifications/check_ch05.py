# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 5 (Équations et mise en équation)."""
from sympy import symbols, solve, expand, sqrt, Rational as R, S, solveset

x = symbols("x")

# Cours
assert solve(5 * x - 7 - (2 * x + 8), x) == [5] and 5 * 5 - 7 == 18 == 2 * 5 + 8
assert solve(x / 3 + x / 4 - 14, x) == [24]
assert solve(2 * x + 3 - (2 * x + 5), x) == [] and expand(2 * (x + 3) - (2 * x + 6)) == 0
assert set(solve((x - 4) * (2 * x + 3), x)) == {4, -R(3, 2)}
assert set(solve(x * x - 5 * x, x)) == {0, 5}
assert solve(3 * x + 12 - 5 * x, x) == [6]

# Découverte
assert solve(x + 13 - 4, x) == [-9] and solve(-4 * x - 18, x) == [-R(9, 2)]  # D1
assert solve(x - 7 + 3, x) == [4] and solve(x / 5 + 3, x) == [-15]           # D1
assert solve(3 * x, x) == [0]                                                # D1
assert solve(7 * x - 5 - 30, x) == [5]                                       # D2
assert solve(2 * x + 9 - 1, x) == [-4] and solve(5 - 3 * x - 11, x) == [-2]  # D2
assert solve(4 * x + 7 - 7, x) == [0]                                        # D2
assert solve(8 * x + 3 - (5 * x - 12), x) == [-5]                            # D3
assert 8 * (-5) + 3 == -37 == 5 * (-5) - 12                                  # D3
assert solve(9 * x - 4 - (4 * x + 21), x) == [5]                             # D3
assert solve(2 * x + 10 - 7 * x, x) == [2]                                   # D3
assert solve(3 * (2 * x - 5) - (4 * x + 9), x) == [12]                       # D4
assert solve(5 * (x - 2) - 3 * x, x) == [5]                                  # D4
assert solve(2 * (x + 3) - 4 * (x - 1), x) == [5] and 2 * 8 == 16 == 4 * 4   # D4
assert solve(5 * x + 2 - 9, x) == [R(7, 5)] and R(7, 5) == R('1.4')          # D5
assert solve(3 * x - 7, x) == [R(7, 3)]                                      # D5
assert solve(2 * x - 1 - 6, x) == [R(7, 2)]                                  # D5
assert 2 * 3 + 5 == 11 and 3 ** 2 != 6 and 4 * 3 - 1 == 11 == 2 * 3 + 5      # D6
assert (-2) ** 2 == 4 and 5 * 0 + 3 == 3                                     # D6
assert solve(2 * x + 7 - 19, x) == [6] and solve(x / 3 - 12, x) == [36]      # D7
assert solve(x + 5 - 3 * x, x) == [R(5, 2)]                                  # D7
assert solve(x / 4 - 2 - 8, x) == [40]                                       # D7
assert R(5, 2) + 5 == 3 * R(5, 2) and 40 / 4 - 2 == 8                        # D7

# Entraînement
assert solve(x / 3 + x / 4 - 14, x) == [24] and 24 / 3 + 24 / 4 == 14        # E1
assert solve(x / 2 - x / 5 - 6, x) == [20] and 10 - 4 == 6                   # E1
assert solve(2 * x / 3 - 8, x) == [12]                                       # E1
assert expand(4 * (x - 2) - (4 * x - 8)) == 0                                # E2
assert solve(4 * (x - 2) - (4 * x + 1), x) == []                             # E2
assert solve(3 * x + 5 - (3 * x - 5), x) == []                               # E2
assert expand(2 * (x + 3) - (2 * x + 6)) == 0                                # E2
assert set(solve((2 * x - 7) * (x + 4), x)) == {R(7, 2), -4}                 # E3
assert set(solve(x * (3 * x - 9), x)) == {0, 3}                              # E3
assert set(solve(x * x - 49, x)) == {-7, 7}                                  # E4
assert set(solve(x * x - 12, x)) == {-2 * sqrt(3), 2 * sqrt(3)}              # E4
assert solveset(x * x + 2, x, domain=S.Reals) == S.EmptySet                  # E4
assert solve(x * x, x) == [0]                                                # E4
assert solveset(x * x + 9, x, domain=S.Reals) == S.EmptySet                  # E4
assert set(solve(x * x - 6 * x, x)) == {0, 6}                                # E5
assert set(solve(x * x - 5 * x, x)) == {0, 5}                                # E5
assert set(solve(2 * x * x - 8 * x, x)) == {0, 4}                            # E5
assert solve(3 * (x - 1) - (2 * (x + 4) - 5), x) == [6]                      # E6
assert 3 * 5 == 15 == 2 * 10 - 5                                             # E6
assert solve(4 * (2 * x - 1) - (5 * x + 8), x) == [4] and 4 * 7 == 28 == 20 + 8  # E6
assert set(solve((3 * x - 6) * (2 * x + 10), x)) == {2, -5}                  # E7
assert set(solve(x * x - 25, x)) == {-5, 5}                                  # E7
assert set(solve(x * x - 49, x)) == {-7, 7}                                  # E7

# Problèmes
assert solve(6 * x + 10 * (28 - x) - 232, x) == [12]                         # P1
assert 12 * 6 + 16 * 10 == 232                                               # P1
assert solve(2 * x + 2 * (x + 7) - 58, x) == [11]                            # P2
assert 2 * (11 + 18) == 58 and 11 * 18 == 198                                # P2
assert expand(3 * (x + 4) - 2 * x) == x + 12                                 # P3
assert solve(x + 12 - 25, x) == [13] and 17 * 3 - 26 == 25                   # P3
assert solve(x + 12, x) == [-12]                                             # P3
assert 38 + 12 * 2 > 30 * 2 and 38 + 12 * 3 <= 30 * 3                        # P4
assert 38 + 24 * 6 > 30 * 6 and 38 + 24 * 7 <= 30 * 7                        # P4 Q5
assert solve((x + 2) ** 2 - x * (x + 5), x) == [4]                           # P5
assert (4 + 2) ** 2 == 36 == 4 * (4 + 5)                                     # P5
assert solve(9 * x - (40 + 4 * x), x) == [8] and 9 * 8 == 72 == 40 + 4 * 8   # P6
assert 9 * 5 == 45 < 60 == 40 + 4 * 5                                        # P6 Q3
assert 9 * 12 == 108 and 40 + 4 * 12 == 88 and 108 - 88 == 20                # P6 Q4
assert solve(9 * x - (40 + 4 * x) - 20, x) == [12]                           # P6 Q5
assert solve(x + 5 - 2 * (x - 7), x) == [19] and 24 == 2 * 12                # P7

print("check_ch05 : tous les contrôles passent.")
