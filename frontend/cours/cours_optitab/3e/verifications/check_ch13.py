# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 13 (Thalès et triangles semblables)."""
from sympy import Rational as R

# Cours
assert R(3, 5) * 7 == R('4.2')                       # exemple emboîtée AN = 4,2
assert R(2, 6) * 9 == 3                              # exemple papillon AN = 3
assert R(4, 10) == R(6, 15) == R(2, 5)               # réciproque
assert 2 * 7 == 14 != 15 == 3 * 5                    # non parallèles (cours)
assert R(9, 15) * 1 == R(9, 15) and 9 / R('1.5') == 6  # ombre cours : h = 6 m
assert 15 * R('2.5') == R('37.5') and 12 * R('2.5') ** 2 == 75  # semblables

# Découverte
assert R(1, 2) == R(1, 2)                                            # D1 Q4
assert R(3, 5) == R(6, 10) and 3 * 10 / 5 == 6                       # D2 Q2
assert R(3, 5) == R('0.6') and R('0.6') * R('7.5') == R('4.5')       # D2 Q3-4
assert R('4.5') < R('7.5') and 6 < 10                                # D2 Q5
assert 4 * 15 / 10 == 6 and R(4, 10) == R('0.4')                     # D3 Q2-3
assert R('0.4') * R('7.5') == 3                                      # D3 Q4
assert 3 + 2 == 5 and R(3) * 12 / 5 == R('7.2')                      # D4 Q1-2
assert 12 - R('7.2') == R('4.8') and R('7.2') / 12 == R(3, 5)        # D4 Q3/Q5
assert 6 * 10 / 4 == 15 and 15 - 6 == 9                              # D5 Q2-3
assert R(10, 4) == R('2.5') and 6 * R('2.5') == 15                   # D5 Q4
assert R(2, 3) * 9 == 6 and R(2, 3) * 12 == 8                        # D6 Q3-4
assert 8 / R(2, 3) == 12                                             # D6 Q5

# Entraînement
assert R(4, 10) == R(2, 5) == R(6, 15)                               # E1 Q1-2
assert R(2, 5) * 10 == 4                                             # E1 Q4
assert 3 * 12 == 36 != 40 == 5 * 8                                   # E2 Q3
assert R(3) * 12 / 8 == R('4.5') and R('4.5') / 12 == R(3, 8)        # E2 Q5
assert R(3) * 8 / 5 == R('4.8') and 3 + 5 == 8                       # E3 Q1-2
assert R('4.8') + 8 == R('12.8') and R(3, 5) * 6 == R('3.6')         # E3 Q3-4
assert 40 + 65 + 75 == 180 and R(9, 6) == R('1.5')                   # E4
assert 180 - 50 - 60 == 70 and 180 - 60 - 70 == 50                   # E6
assert R(10, 4) == R('2.5')                                          # E5 Q1
assert 15 * R('2.5') == R('37.5') and R('2.5') ** 2 == R('6.25')     # E5 Q2-3
assert 12 * R('6.25') == 75 and 12 * R('2.5') == 30                  # E5 Q4-5
assert [3 * 3, 4 * 3, 5 * 3] == [9, 12, 15]                          # E7 Q1
assert 3 + 4 + 5 == 12 and 9 + 12 + 15 == 36 and 36 / 12 == 3        # E7 Q2-3
assert 6 * 9 == 54                                                   # E7 Q4

# Problèmes
assert R(12, 2) == 6 and R('1.5') * 6 == 9                           # P1 Q2-3
assert R('4.5') * (2 / R('1.5')) == 6                                # P1 Q4 (4,5 × 4/3 = 6)
assert 4 + 2 == 6 and R(4, 6) == R(2, 3) == R(6, 9)                  # P2 Q4
assert R(2, 3) * R('7.5') == 5                                       # P2 Q5
assert 3 * 16 / 8 == 6 and 16 - 6 == 10                              # P3 Q3-4
assert R(3, 8) * 12 == R("4.5")                                      # P3 Q5
assert 2 * R('7.4') == R('14.8')                                     # P4 Q4
assert 2 * 39 == 78 and R(78, 3) == 26 and R(39, 3) == 13 and 2 * 13 == 26  # P5
assert R(45, 15) == 3 and 10 * 3 == 30                               # P6 Q1-2
assert 2 * (10 + 15) == 50 and 2 * (30 + 45) == 150 and 150 / 50 == 3  # P6 Q3
assert 10 * 15 == 150 and 30 * 45 == 1350 and 1350 / 150 == 9        # P6 Q4
assert R(20, 10) == 2 != R(40, 15)                                   # P6 Q5
assert R('4.5') / R('7.5') == R(3, 5) == R(6, 10)                    # P7 Q1
assert R('4.2') * 5 / 3 == 7                                         # P7 Q3
assert R('7.5') - R('4.5') == 3 and 10 - 6 == 4                      # P7 Q4

print("check_ch13 : tous les contrôles passent.")
