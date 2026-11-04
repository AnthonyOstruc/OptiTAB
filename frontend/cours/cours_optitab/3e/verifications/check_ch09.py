# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 9 (Fonctions linéaires et affines)."""
from sympy import symbols, solve, Rational as R, expand

x = symbols("x")

# Cours
assert 2 * 0 - 3 == -3 and 2 * 2 - 3 == 1
assert R(11 - 5, 4 - 1) == 2 and 5 - 2 * 1 == 3
assert R(21, 6) == R('3.5')
assert solve(20 + 3 * x - (8 + 5 * x), x) == [6] and 20 + 18 == 38

# Découverte
assert R('-2.5') * 4 == -10 and R('-2.5') * (-2) == 5                    # D2
assert 15 / R('-2.5') == -6                                              # D2
assert -3 * 2 + 8 == 2                                                   # D3
assert R('1.5') * 2 == 3 and R('1.5') * 4 == 6                           # D4
assert -0 + 4 == 4 and solve(-x + 4, x) == [4] and -1 + 4 == 3           # D5
assert [2 * a - 3 for a in [0, 1, -2]] == [-3, -1, -7]                   # D6
assert 2 * R('0.5') - 3 == -2                                            # D6

# Entraînement
assert R(21, 6) * (-2) == -7                                             # E1
assert R(10 - 1, 5 - 2) == 3 and 1 - 3 * 2 == -5 and 3 * 5 - 5 == 10     # E2
assert solve(3 * x - 5, x) == [R(5, 3)]                                  # E2
assert R(26 - 14, 5 - 2) == 4 and 14 - 2 * 4 == 6 and 4 * 8 + 6 == 38    # E3
assert -2 * 1 + 3 == 1 and solve(-2 * x + 3, x) == [R(3, 2)]             # E4
assert expand((4 * x + 6) - (4 * x - 1)) == 7                            # E5
assert solve(4 * x - 1 - (4 * x + 6), x) == []                           # E5
assert R(0 - 6, 2 - (-1)) == -2 and 0 - (-2) * 2 == 4                    # E6
assert -2 * (-1) + 4 == 6                                                # E6
assert R(11 - 3, 2 - 0) == 4 == R(23 - 11, 5 - 2)                        # E7
assert 4 * 10 + 3 == 43                                                  # E7

# Problèmes
assert 20 + 3 * 4 == 32 and 8 + 5 * 4 == 28                              # P1
assert 20 + 3 * 6 == 38 == 8 + 5 * 6                                     # P1
assert 20 + 3 * 10 == 50 and 8 + 5 * 10 == 58                            # P1
assert expand((20 + 3 * x) - (8 + 5 * x)) == 12 - 2 * x                  # P1
assert 900 - 35 * 10 == 550 and solve(900 - 35 * x - 200, x) == [20]     # P2
assert solve(900 - 35 * x, x) == [R(180, 7)]                             # P2
assert round(float(R(180, 7) - 25) * 60) == 43                           # P2
assert 900 - 35 * 30 == -150                                             # P2
assert R(20, 12) == R(5, 3) and 18 * R(5, 3) == 30 and 20 * 30 == 600    # P3
assert 12 * 18 == 216 and 216 * R(5, 3) ** 2 == 600                      # P3
assert 2 + 5 == 7 == 3 * 2 + 1 and 0 + 5 != 3 * 0 + 1                    # P4
assert R(7, 2) == R('3.5')                                               # P4
assert 45 + 12 * 6 == 117 and 15 + 18 * 6 == 123                         # P5
assert 45 + 12 * 7 == 129 > 120 and 15 + 18 * 5 == 105                   # P5
assert solve(15 + 18 * x - (45 + 12 * x), x) == [5]                      # P5
assert 3 + R('1.5') * 5 == R('10.5') and 7 + R('1.1') * 5 == R('12.5')   # P6
assert solve(3 + R('1.5') * x - (7 + R('1.1') * x), x) == [10]          # P6
assert 3 + R('1.5') * 10 == 18                                           # P6
assert 3 + R('1.5') * 20 == 33 and 7 + R('1.1') * 20 == 29               # P6
assert solve(4 * x - (10 + 2 * x), x) == [5] and 4 * 5 == 20             # P7
assert 4 * 3 == 12 and 10 + 6 == 16 and 4 * 8 == 32 and 10 + 16 == 26    # P7
assert 4 * 5 <= 22 < 4 * 6 and 10 + 2 * 6 <= 22 < 10 + 2 * 7             # P7

print("check_ch09 : tous les contrôles passent.")
