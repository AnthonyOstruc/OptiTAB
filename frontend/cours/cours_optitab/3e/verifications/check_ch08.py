# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 8 (Notion de fonction)."""
from sympy import symbols, solve, solveset, S, sqrt, Rational as R, expand

x = symbols("x")

# Cours
assert (-2) ** 2 + 1 == 5 == 2 ** 2 + 1
assert 3 ** 2 - 2 == 7 and (-2) ** 2 - 2 == 2 != 1
assert R('0.6') / R('0.8') == R('0.75')

# Découverte
assert [(3 * x - 4).subs(x, a) for a in [0, 2, -3]] == [-4, 2, -13]      # D1
assert (3 * x - 4).subs(x, R(1, 3)) == -3                                # D1
assert [a for a, b in [(-2, 5), (0, 1), (1, -1), (3, 1)] if b == 1] == [0, 3]  # D2
assert 2 not in [-2, 0, 1, 3]                                            # D2
assert 3 ** 2 - 2 == 7 and (-2) ** 2 - 2 == 2                            # D4
assert 5 ** 2 - 2 == 23                                                  # D4
assert solve(5 * x + 2 - 17, x) == [3] and 5 * 3 + 2 == 17               # D5
assert solve(5 * x + 2 + 8, x) == [-2]                                   # D5
assert 0 + 1 == 1 and 4 + 1 == 5 and (-2) ** 2 + 1 == 5                  # D6
assert solveset(x ** 2 + 1, x, domain=S.Reals) == S.EmptySet             # D6
# D7 : conceptuel (pas de calcul)

# Entraînement
assert (1 + 3) ** 2 == 16 and (-3 + 3) ** 2 == 0                         # E1
assert 1 ** 2 + 3 == 4 != 16 and (-5 + 3) ** 2 == 4                      # E1
assert 1 - 2 * 0 == 1                                                    # E2 (f(0) sur segment central)
# sommets (-4;0) -> (-1;3) : y = x + 4 ; y=1 en x=-3 ; (1;-1)->(3;1) : y = x-2 ; y=1 en x=3
assert -3 + 4 == 1 and 3 - 2 == 1                                        # E2 antécédents
assert set(solve(x * x - 16, x)) == {-4, 4}                              # E3
assert solve(x * x, x) == [0]                                            # E3
assert solveset(x * x + 1, x, domain=S.Reals) == S.EmptySet              # E3
assert set(solve(x * x - 7, x)) == {sqrt(7), -sqrt(7)}                   # E3
assert solve(x + 2 - (2 * x - 1), x) == [3] and 3 + 2 == 5 == 2 * 3 - 1  # E4
assert 5 + 2 == 7 and 2 * 5 - 1 == 9                                     # E4
assert solve(2 * x - 6, x) == [3] and solve(2 * x - 6 - 10, x) == [8]    # E5
assert solve(2 * x - 6 + 6, x) == [0] and solve(4 * x - 30, x) == [R(15, 2)]  # E5
# E6 : conceptuel
# E7 : pentes -2, -2, +1
assert R(1 - 5, 0 - (-2)) == -2 and R(-1 - 1, 1 - 0) == -2 and R(1 - (-1), 3 - 1) == 1  # E7

# Problèmes
assert R('0.8') * R('1.2') == R('0.96') and R('0.96') * 1000 == 960      # P1
assert R('0.6') / R('0.8') == R('0.75') and R('0.8') * R('1.5') == R('1.2')  # P1
assert [min(2 * h, 10) for h in [3, 5, 8]] == [6, 10, 10]                # P2
assert 2 * min(2 * 4, 10) != min(2 * 8, 10)                              # P2
assert 3 * (20 - 3) == 51 == 17 * (20 - 17)                              # P3
assert 10 * (20 - 10) == 100                                             # P3
assert 600 + 600 == 1200 and 15 - 10 == 5                                # P4
assert R(600, 10) == 60                                                  # P4
assert set(solve((x - 2) * (3 * x + 6), x)) == {2, -2}                   # P5
assert (0 - 2) * (3 * 0 + 6) == -12                                      # P5
assert expand((x - 2) * (3 * x + 6)) == 3 * x ** 2 - 12                  # P5
assert 80 - 5 * 0 == 80 and 80 - 5 * 4 == 60                             # P6
assert solve(80 - 5 * x ** 2, x) == [-4, 4]                              # P6
assert 80 - 5 * 25 == -45                                                # P6
assert 2 * 4 + 3 == 11 == 4 + 7                                          # P7
assert solve(2 * x + 3 - (x + 7), x) == [4]                              # P7
assert 2 * 10 + 3 == 23 and 10 + 7 == 17 and 2 * 2 + 3 == 7 and 2 + 7 == 9  # P7

print("check_ch08 : tous les contrôles passent.")
