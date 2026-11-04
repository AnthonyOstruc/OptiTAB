# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 1 (Nombres rationnels et fractions) — 3ème.
Chaque assert correspond à un résultat affirmé dans le cours, les exercices ou la fiche."""
from sympy import Rational as R

# Cours
assert -4 + 3 * (5 - 7) == -10
assert (-3) ** 2 == 9 and -(3 ** 2) == -9
assert R(5, 8) == R(25, 40) and R(42, 63) == R(2, 3)
assert R(3, 4) - R(5, 6) == -R(1, 12)
assert R(2, 3) / R(5, 7) == R(14, 15)
assert R(-9, 14) * R(7, 15) == -R(3, 10)
assert 40 * R(3, 5) == 24
assert R(2, 3) < R(3, 4) and -R(5, 6) < -R(3, 4)
assert 2 - R(5, 7) == R(9, 7) and round(9 / 7, 2) == 1.29
assert R(8 + 4, 4) == 3 and R(6 + 3, 3) == 3
assert R(1, 3) * R(3, 5) == R(1, 5)

# Découverte
assert -6 + 11 - 4 == 1                                        # D1
assert 18 - 3 * (2 + 5) == -3 and (18 - 3) * (2 + 5) == 105    # D2
assert R(5, 8) == R(25, 40) and R(42, 63) == R(2, 3)           # D3
assert R(36, 48) == R(3, 4) and R(-45, 60) == -R(3, 4) and R(84, 70) == R(6, 5)  # D4
assert R(7, 12) + R(5, 18) == R(31, 36)                        # D5
assert R(-9, 14) * R(7, 15) == -R(3, 10)                       # D6
assert R(3, 5) / R(-9, 10) == -R(2, 3)                         # D6
assert 40 * R(3, 5) == 24 and 56 * R(7, 8) == 49               # D7
assert R(5, 4) * R(2, 3) == R(5, 6)                            # D7

# Entraînement
assert -R(5, 6) < -R(3, 4) < -R(7, 12)                         # E1
assert (R(2, 3) + R(1, 6)) / (R(5, 4) - R(1, 2)) == R(10, 9)   # E2
assert R(8 + 4, 4) == 3                                        # E3
assert R(2, 3) - R(1, 4) * R(8, 3) == 0                        # E4
assert (R(2, 3) - R(1, 4)) * R(8, 3) == R(10, 9)               # E4
assert (R(5, 4) - R(1, 2)) * R(2, 3) == R(1, 2)                # E5
assert (R(2) - R(1, 2)) * R(2, 3) == 1 and 1 * R(3, 2) + R(1, 2) == 2  # E5
assert R(3, 4) / 6 == R(1, 8) and 10 * R(1, 8) == R(5, 4) == R('1.25')  # E6
assert R(3, 4) * R(10, 6) == R(5, 4)                           # E6
assert 2 - R(5, 7) == R(9, 7) and round(9 / 7, 2) == 1.29      # E7

# Problèmes
assert 1 - R(2, 5) == R(3, 5) and R(1, 3) * R(3, 5) == R(1, 5)          # P1
assert 1 - R(2, 5) - R(1, 5) == R(2, 5) and 270 * R(2, 5) == 108        # P1
assert R(7, 8) * (1 - R(2, 7)) == R(5, 8)                               # P2
assert R(3, 4) - R(5, 8) == R(1, 8) and 30 * 8 == 240                   # P2
assert 240 * R(7, 8) == 210 and 210 * R(5, 7) == 150 and 150 + 30 == 240 * R(3, 4)  # P2
assert 1 - R(3, 8) - R(5, 12) == R(5, 24)                               # P3
assert 15 / R(5, 24) == 72 and 72 * R(3, 8) == 27 and 72 * R(5, 12) == 30 and 27 + 30 + 15 == 72  # P3
assert R(5, 6) * R(3, 5) == R(1, 2) and 15 * 2 == 30                    # P4
assert 30 - 30 * R(5, 6) == 5 and R(3, 5) * 25 == 15                    # P4
assert 1 - R(1, 3) - R(1, 4) == R(5, 12)                                # P5
assert 15000 / R(5, 12) == 36000                                        # P5
assert 36000 * R(1, 3) == 12000 and 36000 * R(1, 4) == 9000             # P5
assert 12000 + 9000 + 15000 == 36000                                    # P5
assert R(4, 5) - R(3, 5) == R(1, 5) and 14 * 5 == 70                    # P6
assert 70 * R(3, 5) == 42 and 42 + 14 == 70 * R(4, 5)                   # P6
assert R(2, 3) == R(8, 12) and R(5, 4) == R(15, 12)                     # P7
assert [n for n in range(30) if R(2, 3) < R(n, 12) < R(5, 4)] == [9, 10, 11, 12, 13, 14]  # P7

# Questions ajoutées (standard : exercices complets, >= 5 questions)
assert -3 + 8 - 9 == -4 and 1 - (-4) == 5 and 5 - (-4) == 9              # D1 Q3-5
assert 5 + 3 * 4 - 2 == 15 and 20 - 12 / 4 == 17 and (5 + 3) * (4 - 2) == 16  # D2 Q3-4
assert R(3, 7) == R(12, 28) and R(54, 72) == R(3, 4) and R(7, 9) == R(35, 45)  # D3 Q3-5
assert R(125, 100) == R(5, 4) and R(17, 51) == R(1, 3)                   # D4 Q4-5
assert R(2, 3) + R(1, 6) == R(5, 6) and R(3, 4) - R(5, 6) == -R(1, 12)   # D5 Q3-4
assert R(1, 2) + R(1, 3) + R(1, 6) == 1                                  # D5 Q5
assert R(4, 9) * R(3, 8) == R(1, 6) and R(5, 6) / R(10, 3) == R(1, 4)    # D6 Q3-4
assert R(-2, 5) * R(-15, 8) == R(3, 4)                                   # D6 Q5
assert 60 * R(3, 4) == 45 and 300 * R(5, 6) == 250                       # D7 Q4-5
assert -R(3, 4) < -R(2, 3) < -R(7, 12)                                   # E1 Q3
assert R(5, 7) == R(50, 70) > R(49, 70) == R(7, 10)                      # E1 Q4
assert round(-7 / 12, 2) == -0.58                                        # E1 Q5
assert R(10, 9) > 1                                                      # E2 Q4
assert (R(3, 4) - R(1, 2)) / R(5, 6) == R(3, 10)                         # E2 Q5
assert R(15 + 5, 5) == 4 and R(9 * 4, 4) == 9 and R(10 + 7, 7) == R(17, 7)  # E3 Q3-5
assert R(1, 2) + R(1, 2) * R(1, 3) == R(2, 3)                            # E4 F
assert (R(1, 2) + R(1, 2)) * R(1, 3) == R(1, 3)                          # E4 G
assert R(2, 3) == 2 * R(1, 3)                                            # E4 Q5
assert (R(1, 2) - R(1, 2)) * R(2, 3) == 0                                # E5 Q2/Q4
assert 15 * R(1, 8) == R(15, 8) == R('1.875') and 3 * R(1, 8) == R(3, 8) # E6 Q3-4
assert 2 / R(1, 8) == 16                                                 # E6 Q5
assert round(9 / 7, 3) == 1.286                                          # E7 Q3
assert 3 - R(8, 5) == R(7, 5) == R('1.4')                                # E7 Q4
assert 270 * R(2, 5) == 108 and 270 * R(1, 5) == 54 and 108 / 27 == 4    # P1 Q4-5
assert 210 * R(2, 7) == 60 and 210 - 60 == 150                           # P2 Q4
assert 25 * R(2, 5) == 10 and R(10, 30) == R(1, 3)                       # P4 Q4-5
assert R(1, 2) + R(1, 3) + R(1, 6) == 1 and 15 + 10 + 5 == 30            # P4 Q5
assert 20000 / R(5, 12) == 48000                                         # P5 Q5
assert 42 + 14 == 56 == 70 * R(4, 5) and 70 - 56 == 14                   # P6 Q4-5
assert 14 - 9 + 1 == 6                                                   # P7 Q4
assert [n for n in range(30) if R(2, 3) < R(n, 12) <= R(5, 4)] == list(range(9, 16))  # P7 Q5

print("check_ch01 : tous les contrôles passent.")
