# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 4 (Calcul littéral)."""
from sympy import symbols, expand, solve

x, n = symbols("x n")

# Cours
assert expand((2 * x - 3) * (x + 4)) == 2 * x ** 2 + 5 * x - 12
assert (3 * x ** 2 - 5 * x).subs(x, -2) == 22
assert expand(6 * x ** 2 - 9 * x - 3 * x * (2 * x - 3)) == 0
assert expand((x - 2) * (3 * x + 5) - (3 * x * (x - 2) + 5 * (x - 2))) == 0
assert expand((2 * x - 5) * (2 * x + 5)) == 4 * x ** 2 - 25
assert expand((x + 6) ** 2) == x ** 2 + 12 * x + 36
assert expand((2 * x - 3) ** 2) == 4 * x ** 2 - 12 * x + 9
assert 99 ** 2 == 9801 and 103 * 97 == 9991
assert expand(3 * (x + 4) - 3 * x) == 12
assert expand((2 * n + 1) ** 2 - (2 * (2 * n ** 2 + 2 * n) + 1)) == 0

# Découverte
assert (2 * x * x - 3 * x + 1).subs(x, -2) == 15                         # D1
assert (2 * x * x - 3 * x + 1).subs(x, 3) == 10                          # D1
assert expand(7 * x - 4 + 3 * x + 9 - 2 * x) == 8 * x + 5                # D2
assert expand(-(4 * x - 7) + 2 * (3 - x)) == -6 * x + 13                 # D3
assert (-(4 * 0 - 7) + 2 * (3 - 0)) == 13                                # D3 contrôle x=0
assert expand((3 * x + 2) * (x - 5)) == 3 * x ** 2 - 13 * x - 10         # D4
assert expand(7 * (2 * x + 3)) == 14 * x + 21                            # D5
assert expand(4 * x * (3 * x - 2)) == 12 * x ** 2 - 8 * x                # D5
assert expand(5 * (2 * x - 3)) == 10 * x - 15                            # D6
assert expand(4 * (3 * x + 7)) == 12 * x + 28                            # D7
assert expand(-2 * (5 * x - 3)) == -10 * x + 6                           # D7
assert expand(x * (x + 6)) == x ** 2 + 6 * x                             # D7

# Entraînement
assert expand((x - 9) * (x + 9)) == x ** 2 - 81                          # E1
assert expand((5 * x - 2) * (5 * x + 2)) == 25 * x ** 2 - 4              # E1
assert expand((x + 6) ** 2) == x ** 2 + 12 * x + 36                      # E2
assert expand((2 * x - 3) ** 2) == 4 * x ** 2 - 12 * x + 9               # E2
assert 103 * 97 == 9991 and 10000 - 9 == 9991                            # E3
assert 49 ** 2 == 2401 and 2500 - 100 + 1 == 2401                        # E3
assert expand((x - 2) * (3 * x + 5) - (3 * x * (x - 2) + 5 * (x - 2))) == 0  # E4
assert expand(9 * (x - 2) * (x + 2)) == 9 * x ** 2 - 36                  # E4
assert (1 + 2) ** 2 - 1 == 8 and expand((x + 2) ** 2 - x * x) == 4 * x + 4   # E5
assert solve(4 * x + 4 - 4, x) == [0]                                    # E5
assert expand((2 * x + 1) * (3 * x - 4) - 6 * x ** 2) == -5 * x - 4      # E6
assert -5 * 10 - 4 == -54 and 21 * 26 - 600 == -54                       # E6
assert expand((5 - x) * (5 + x)) == 25 - x ** 2                          # E7
assert expand((x + 5) ** 2) == x ** 2 + 10 * x + 25                      # E7
assert expand(4 * (2 * x + 3)) == 8 * x + 12                             # E7

# Problèmes
assert 4 * (3 + 5) - 8 == 24 and 4 * 3 + 12 == 24                        # P1
assert expand(4 * (x + 5) - 8) == 4 * x + 12                             # P1
assert expand((x + 4) ** 2 - x ** 2) == 8 * x + 16                       # P2
assert 8 * 7 + 16 == 72 and 11 ** 2 - 7 ** 2 == 72                       # P2
assert expand((2 * n + 1) ** 2) == 4 * n ** 2 + 4 * n + 1                # P3
assert expand((2 * n) ** 2) == 4 * n ** 2                                # P3
assert expand((x + 3) ** 2 - x ** 2) == 6 * x + 9                        # P4
assert solve(6 * x + 9 - 9, x) == [0] and solve(6 * x + 9 - 39, x) == [5]  # P4
assert 8 ** 2 - 5 ** 2 == 39                                             # P4
assert (5 + 1) ** 2 == 36 and 5 * (5 + 2) == 35                          # P5
assert (-3 + 1) ** 2 == 4 and -3 * (-3 + 2) == 3                         # P5
assert expand((x + 1) ** 2 - x * (x + 2)) == 1                           # P5
assert expand((x - 2) * (x + 5) + 3 * (x - 2)) == x ** 2 + 6 * x - 16    # P6
assert expand((x - 2) * (x + 8)) == x ** 2 + 6 * x - 16                  # P6
assert (2 - 2) * (2 + 8) == 0 and 0 + 0 - 16 == -16                      # P6
assert 4 + 5 + 6 == 15 == 3 * 5 and 11 + 12 + 13 == 36 == 3 * 12         # P7
assert expand(n + (n + 1) + (n + 2)) == 3 * n + 3                        # P7
assert expand(n + (n + 1)) == 2 * n + 1                                  # P7

# Questions ajoutées (standard : exercices complets, >= 5 questions)
assert (2 * x * x - 3 * x + 1).subs(x, 0) == 1                           # D1 Q3
assert (5 * x - x * x).subs(x, -1) == -6                                 # D1 Q4
assert (5 * x - x * x).subs(x, 2) == 6                                   # D1 Q5
assert expand(5 * x + 3 - x - 8) == 4 * x - 5                            # D2 Q2
assert expand(2 * x ** 2 + 3 * x - x ** 2 + x) == x ** 2 + 4 * x         # D2 Q3
assert expand(4 - 2 * x + 7 * x - 9) == 5 * x - 5                        # D2 Q4
assert 8 * 2 + 5 == 21 != 26 == 13 * 2                                   # D2 Q5
assert expand(-(-2 * x + 5)) == 2 * x - 5                                # D3 Q4
assert expand((x + 4) * (x + 2)) == x ** 2 + 6 * x + 8                   # D4 Q3
assert expand((2 * x - 1) * (x + 3)) == 2 * x ** 2 + 5 * x - 3           # D4 Q4
assert (2 * 1 - 1) * (1 + 3) == 4 == 2 + 5 - 3                           # D4 Q5
assert expand(5 * (x + 1)) == 5 * x + 5                                  # D5 Q4
assert expand(x * (x + 7)) == x ** 2 + 7 * x                             # D5 Q5
assert expand(3 * x * (2 * x - 5)) == 6 * x ** 2 - 15 * x                # D7 Q4
assert expand(-(x ** 2 - 4 * x + 1)) == -x ** 2 + 4 * x - 1              # D7 Q5
assert expand((7 - x) * (7 + x)) == 49 - x ** 2                          # E1 Q4
assert expand((6 * x - 1) * (6 * x + 1)) == 36 * x ** 2 - 1              # E1 Q5
assert expand((x + 10) ** 2) == x ** 2 + 20 * x + 100                    # E2 Q3
assert expand((3 * x + 1) ** 2) == 9 * x ** 2 + 6 * x + 1                # E2 Q4
assert (1 + 6) ** 2 == 49 and 1 + 36 == 37 and 37 + 12 == 49             # E2 Q5
assert 101 ** 2 == 10201 == 10000 + 200 + 1                              # E3 Q3
assert 1002 * 998 == 999996 == 10 ** 6 - 4                               # E3 Q4
assert 55 ** 2 - 45 ** 2 == 1000 == 10 * 100                             # E3 Q5
assert expand((x + 1) * ((2 * x - 3) + (x + 7))) == expand((x + 1) * (2 * x - 3) + (x + 1) * (x + 7))  # E4 Q4
assert expand((x + 1) * (3 * x + 4)) == 3 * x ** 2 + 7 * x + 4           # E4 Q4
assert expand(2 * (x - 5) * (x + 5)) == 2 * x ** 2 - 50                  # E4 Q5
assert expand((x + 3) ** 2 - x ** 2) == 6 * x + 9                        # E5 Q4
assert solve(6 * x + 9 - 9, x) == [0]                                    # E5 Q5
assert -5 * (-2) - 4 == 6 and (-3) * (-10) - 24 == 6                     # E6 Q5
assert expand((x - 6) ** 2) == x ** 2 - 12 * x + 36                      # E7 Q4
assert expand(3 * (x - 3) * (x + 3)) == 3 * x ** 2 - 27                  # E7 Q5
assert 4 * (-5 + 5) - 8 == -8 and 4 * (-5) + 12 == -8                    # P1 Q2
assert solve(8 * x + 16 - 56, x) == [5] and 9 ** 2 - 5 ** 2 == 56        # P2 Q5
assert 3 ** 2 == 9 and 7 ** 2 == 49                                      # P3 Q1
assert solve(6 * x + 9 - 100, x) == [sympify := __import__('sympy').Rational(91, 6)]  # P4 Q5
assert float(__import__('sympy').Rational(91, 6)) > 0                    # P4 Q5
assert expand((x + 2) ** 2 - x * (x + 4)) == 4                           # P5 Q5
assert set(solve((x - 2) * (x + 8), x)) == {2, -8}                       # P6 Q5
assert expand(n + (n + 1) + (n + 2) + (n + 3) + (n + 4)) == 5 * n + 10   # P7 Q5

print("check_ch04 : tous les contrôles passent.")
