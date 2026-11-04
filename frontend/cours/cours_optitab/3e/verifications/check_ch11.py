# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 11 (Probabilités)."""
from sympy import Rational as R, isprime, symbols, solve

x = symbols("x")
D = range(1, 7)
des = [(a, b) for a in D for b in D]

# Cours
assert R(3, 6) == R(1, 2) and R(5, 10) == R(1, 2)
assert R(2, 4) == R(1, 2)
assert R(3, 5) ** 2 == R(9, 25) and R(3, 5) * R(2, 4) == R(3, 10)

# Découverte
assert R(len([a for a in D if a % 2 == 0]), 6) == R(1, 2)               # D1
assert R(len([a for a in D if a % 3 == 0]), 6) == R(1, 3)               # D1
assert R(len([a for a in D if isprime(a)]), 6) == R(1, 2)               # D1
assert R(len([a for a in D if a > 4]), 6) == R(1, 3)                    # D1
assert R(5, 10) == R(1, 2) and R(2, 10) == R(1, 5)                      # D2
assert 1 - R(1, 6) == R(5, 6)                                           # D3
assert R(2, 8) == R(1, 4) and R(4, 8) == R(1, 2) and R(6, 8) == R(3, 4) and 360 / 8 == 45  # D4
assert R(1, 2) ** 2 == R(1, 4) and 1 - R(1, 4) == R(3, 4)               # D5
assert R(46, 100) == R('0.46')                                          # D6
assert R(8, 32) == R(1, 4) and R(4, 32) == R(1, 8) and R(12, 32) == R(3, 8)  # D7

# Entraînement
assert len(des) == 36 and sum(a + b == 7 for a, b in des) == 6          # E1
assert sum(a + b == 2 for a, b in des) == 1                             # E1
assert sum(a + b >= 10 for a, b in des) == 6                            # E1
assert R(3, 5) ** 2 == R(9, 25) and R(2, 5) ** 2 == R(4, 25)            # E2
assert 2 * R(3, 5) * R(2, 5) == R(12, 25) and R(9 + 12 + 4, 25) == 1    # E2
assert R(2, 5) * R(1, 4) == R(1, 10)                                    # E3
assert R(3, 5) * R(2, 4) + R(2, 5) * R(3, 4) == R(3, 5)                 # E3
assert R(3, 10) + R(1, 10) + R(3, 5) == 1                               # E3
assert R(5, 6) ** 2 == R(25, 36) and 1 - R(25, 36) == R(11, 36)         # E4
assert sum(a == 6 or b == 6 for a, b in des) == 11                      # E4
assert sum((a == 6) != (b == 6) for a, b in des) == 10 and R(10, 36) == R(5, 18)  # E4
assert solve(30 - 2 * (6 + x), x) == [9] and R(9, 18) == R(1, 2)        # E5
codes = [(a, b) for a in range(4) for b in range(4)]
assert len(codes) == 16 and sum(a != b for a, b in codes) == 12         # E6
assert sum(a + b == 3 for a, b in codes) == 4                           # E6
assert R(8 + 4 - 1, 32) == R(11, 32)                                    # E7

# Problèmes
assert R(8, 6) + R(4, 6) == 2                                           # P1
assert R(2, 5) * R(4, 5) == R(8, 25) and R(3, 5) * R(1, 5) == R(3, 25)  # P2
assert 1 - R(3, 25) == R(22, 25) and R(8 + 3, 25) == R(11, 25)          # P2
assert abs(R(327, 1000) - R(1, 3)) > abs(R(3354, 10000) - R(1, 3))      # P3
assert round(float(abs(R(327, 1000) - R(1, 3))), 3) == 0.006            # P3
assert round(float(abs(R(3354, 10000) - R(1, 3))), 3) == 0.002          # P3
assert R(20, 200) == R(1, 10) and R(19, 200) == R(19, 200)              # P4
p_aucun = R(180, 200) * R(179, 199)
assert abs(1 - p_aucun - R('0.19')) < R('0.001')                        # P4
assert 3 * 2 == 6 and 3 * 2 * 4 == 24                                   # P5
assert R(3, 4) / 5 == R(3, 20) and R(3, 20) * 2 + R(1, 4) == R(11, 20)  # P6
assert R(98, 400) == R('0.245')                                         # P6
assert R(1, 3) * R(3, 4) == R(1, 4) and R(2, 3) * R(1, 2) == R(1, 3)    # P7
assert R(1, 4) + R(1, 3) == R(7, 12) and 1 - R(7, 12) == R(5, 12)       # P7

print("check_ch11 : tous les contrôles passent.")
