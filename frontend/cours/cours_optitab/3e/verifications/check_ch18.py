# -*- coding: utf-8 -*-
"""Contrôles du chapitre 18 (Raisonner et démontrer)."""
import math
from fractions import Fraction as F

import sympy as sp

x, a, b, n, k = sp.symbols("x a b n k", integer=True)
R = lambda s: F(s)  # noqa: E731

# Cours
assert sp.expand(n + (n + 1) + (n + 2) - 3 * (n + 1)) == 0
assert R("0.5") ** 2 < R("0.5")

# Découverte
assert R("0.5") ** 2 == R("0.25") and 2 + 3 == 5 and 2 * -3 < -3                    # D1
assert 2 * (1 + 9) == 2 * (5 + 5) == 20 and (1 * 9, 5 * 5) == (9, 25)                # D1
assert all((4 * m) % 2 == 0 for m in range(-50, 50))                                 # D1
assert sp.expand((2 * a + 1) + (2 * b + 1) - 2 * (a + b + 1)) == 0                   # D2
assert sp.expand(2 * a + (2 * b + 1) - (2 * (a + b) + 1)) == 0                       # D2
assert sp.expand((2 * a + 1) * (2 * b + 1) - (2 * (2 * a * b + a + b) + 1)) == 0     # D2
assert sp.expand((2 * n) ** 2 - 4 * n ** 2) == 0                                     # D2
prog = lambda v: 2 * (v + 5) - 2 * v  # noqa: E731
assert prog(3) == prog(-7) == prog(R("0.5")) == 10 and sp.expand(prog(x)) == 10      # D3
assert 3 * R("0.4") == R("1.2") and 300 * 40 == 12000 == R("1.2") * 10000            # D4
assert math.ceil(R("7.2") / 3) == 3 and math.ceil(F(128, 50)) == 3                   # D5
assert math.floor(10 / R("1.5")) == 6 and math.ceil(R("13.2") / R("1.5")) == 9       # D5
assert R("13.2") / R("1.5") == R("8.8")                                              # D5
assert 17 * 7 == 119 < 120 == 5 * 24 and F(17, 24) < F(5, 7)                         # D6
assert round(17 / 24, 1) == round(5 / 7, 1) == 0.7                                   # D6
assert F(3, 8) == R("0.375") and 50 > 49 and 2 ** 10 == 1024 > 1000                 # D6
assert 3 + 4 > 6 and 6 ** 2 == 36 != 3 ** 2 + 4 ** 2 == 25                           # D7
assert round(math.sqrt(16 - 9), 2) == 2.65                                           # D7

# Entraînement
assert [m * (m + 1) for m in range(1, 6)] == [2, 6, 12, 20, 30]                       # E1
assert all((m * m + m) % 2 == 0 for m in range(-200, 200))                           # E1
assert (4 + 5 + 6, 10 + 11 + 12, 99 + 100 + 101) == (15, 33, 300)                    # E2
assert 2025 % 3 == 0 and 674 + 675 + 676 == 2025 and 100 % 3 == 1                   # E2
assert sp.solve(sp.Eq(3 * (x - 2), x + 4), x) == [5] and 3 * (4 - 2) != 4 + 4        # E3
assert sp.solve(sp.Eq(5 * x - 3, 2 * x + 9), x) == [4] and 5 * 2 - 3 != 2 * 2 + 9    # E3
assert set(sp.solve((x - 3) * (2 * x + 1), sp.Symbol("x"))) <= {3, sp.Rational(-1, 2)}  # E3
y = sp.Symbol("y")
assert set(sp.solve((y - 3) * (2 * y + 1), y)) == {3, sp.Rational(-1, 2)}             # E3
notes = [10, 10, 10, 18]
assert sum(notes) / 4 == 12 and sum(v >= 12 for v in notes) == 1                    # E4
assert (sorted(notes)[1] + sorted(notes)[2]) / 2 == 10                               # E4
s5 = [2, 12, 12, 12, 12]
assert sum(s5) / 5 == 10 and sorted(s5)[2] == 12                                     # E4
assert R("4.8") ** 2 + R("6.4") ** 2 == 64 == 8 ** 2                                 # E5
assert R("4.8") * R("6.4") / 2 == R("15.36") and 2 * R("15.36") / 8 == R("3.84")     # E5
assert F(3, R("7.5")) == F(4, 10) == R("0.4") and R("0.4") * 12 == R("4.8")          # E6
assert R("4.2") / 10 == R("0.42") != R("0.4")                                        # E6
assert round(F(4, 3) * 27 * math.pi, 1) == 113.1 and round(F(4, 3) * 9 * math.pi, 1) == 37.7  # E7
assert sp.expand((x + 3) ** 2) == x ** 2 + 6 * x + 9 and (1 + 3) ** 2 == 16 != 10    # E7
assert 150 / 1.5 == 100 and -3 ** 2 == -9 and (-3) ** 2 == 9                         # E7

# Problèmes
assert 4 * R("2.5") == 10 and F(6, 10) == R("0.6") and 10 * R("0.8") == 8           # P1
assert (8 - 6) * 1000 == 2000 and 2000 / 25 == 80                                    # P1
A = lambda m: m * R("2.8") + 6  # noqa: E731
Bp = lambda m: 21 * math.ceil(F(m, 8))  # noqa: E731
assert A(24) == R("73.2") and Bp(24) == 63 and A(24) - Bp(24) == R("10.2")           # P2
assert A(30) == 90 and Bp(30) == 84                                                  # P2
assert [m for m in range(1, 9) if A(m) < Bp(m)] == [1, 2, 3, 4, 5]                   # P2
assert sp.expand(100 - (x - 10) ** 2 - x * (20 - x)) == 0 and 7 * 13 == 91           # P3
assert max(m * (20 - m) for m in range(0, 21)) == 100                                # P3
ABC = (180 - 36) / 2
assert ABC == 72 and ABC / 2 == 36 and 180 - 36 - 72 == 72                           # P4
BC = 2 * 5 * math.sin(math.radians(18))
assert round(BC, 2) == 3.09 and round(5 - 3.09, 2) == 1.91                           # P4
# AD = BC dans la figure exacte (triangle d'or) : vérification numérique par les sinus
AD = 5 * math.sin(math.radians(36)) / math.sin(math.radians(108))
assert math.isclose(AD, BC)                                                          # P4
assert [m * m - 1 for m in (3, 5, 7)] == [8, 24, 48]                                 # P5
assert sp.expand((2 * n + 1) ** 2 - 1 - 4 * n * (n + 1)) == 0                        # P5
assert all((m * m - 1) % 8 == 0 for m in range(1, 400, 2))                           # P5
assert all((m * m - 1) % 2 == 1 for m in range(0, 400, 2)) and 99 % 8 != 0           # P5
hs = lambda m: m * (m - 1) // 2  # noqa: E731
assert [hs(3), hs(4), hs(5), hs(10)] == [3, 6, 10, 45] and hs(12) == 66              # P6
assert 50 not in [hs(m) for m in range(2, 100)] and 10 * 9 == 90 and 11 * 10 == 110  # P6
assert sp.expand((a + b) ** 2 - (2 * a * b + (a ** 2 + b ** 2))) == 0                # P7
assert (3 + 4) ** 2 == 49 == 24 + 25                                                 # P7

print("check_ch18 : tous les contrôles passent.")
