# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 2 (Puissances, racines, écriture scientifique)."""
from sympy import Rational as R, sqrt, simplify

# Cours
assert 7 ** 4 == 2401 and R(2) ** -3 == R(1, 8) and 9 ** 0 == 1
assert (-5) ** 2 == 25 and -(5 ** 2) == -25 and (-2) ** 3 == -8 and (-2) ** 4 == 16
assert 3 ** 4 * 3 ** 2 == 3 ** 6 and 5 ** 7 // 5 ** 3 == 5 ** 4 and (2 ** 3) ** 4 == 2 ** 12
assert (2 * 5) ** 3 == 2 ** 3 * 5 ** 3
assert R('7.4') * 10 ** 7 == 74000000 and R('5.6') * R(10) ** -5 == R('0.000056')
assert 3 * 10 ** 5 * 4 * R(10) ** -2 == R('1.2') * 10 ** 4
assert simplify(sqrt(72) - 6 * sqrt(2)) == 0
assert sqrt(9 + 16) == 5 and sqrt(9) + sqrt(16) == 7
assert 6 ** 2 < 37 < R('6.1') ** 2
assert 3 * 10 ** 5 * 500 == R('1.5') * 10 ** 8

# Découverte
assert 7 ** 4 == 2401 and R(2) ** -3 == R(1, 8) and 9 ** 0 == 1          # D1
assert (-5) ** 2 == 25 and -(5 ** 2) == -25                              # D2
assert (-2) ** 3 == -8 and (-2) ** 4 == 16                               # D2
assert 3 ** 4 * 3 ** 2 == 3 ** 6 and 5 ** 7 // 5 ** 3 == 5 ** 4          # D3
assert (2 ** 3) ** 4 == 2 ** 12                                          # D3
assert R('7.4') * 10 ** 7 == 74000000                                    # D4
assert R('9.2') * R(10) ** -5 == R('0.000092')                           # D4
assert sqrt(144) == 12 and sqrt(R(81, 100)) == R(9, 10)                  # D5
assert sqrt(R(49, 64)) == R(7, 8)                                        # D5
assert 10 ** 3 == 1000 and R(10) ** -2 == R('0.01') and 10 ** 0 == 1     # D6
assert 10 ** 6 == 1000000 and R(10) ** -3 == R('0.001')                  # D6
assert sqrt(5) ** 2 == 5 and sqrt(5 ** 2) == 5                           # D7
assert sqrt(16) + sqrt(9) == 7 and sqrt(16 + 9) == 5                     # D7

# Entraînement
assert 6 * 10 ** 8 * 4 * R(10) ** -5 == R('2.4') * 10 ** 4               # E1
assert R('8.4') * R(10) ** -3 / (R('2.1') * 10 ** 5) == 4 * R(10) ** -8  # E2
assert 6 ** 2 < 37 < R('6.1') ** 2 and round(37 ** 0.5, 1) == 6.1        # E3
assert round(37 ** 0.5, 4) == 6.0828                                     # E3
assert simplify(sqrt(98) - 7 * sqrt(2)) == 0                             # E4
assert simplify(sqrt(200) - 10 * sqrt(2)) == 0                           # E4
assert simplify(sqrt(98) + sqrt(200) - 17 * sqrt(2)) == 0                # E4
assert sqrt(9 + 16) == 5 and sqrt(9) + sqrt(16) == 7                     # E5
assert 2 ** 10 == 1024 and 10 ** 3 == 1000                               # E6
assert 3 ** 4 == 81 and 4 ** 3 == 64 and 2 ** 6 == 64                    # E6
assert sqrt(169) == 13 and sqrt(7) ** 2 == 7                             # E7
assert simplify(sqrt(32) - 4 * sqrt(2)) == 0 and round(float(4 * sqrt(2)), 2) == 5.66  # E7

# Problèmes
assert 120 // 20 == 6 and 2 ** 6 == 64 and 800 * 2 ** 6 == 51200         # P1
assert R(51200) == R('5.12') * 10 ** 4                                   # P1
assert R('1.8') / (4 * 10 ** 12) == R('4.5') * R(10) ** -13              # P2
assert R('4.5') * R(10) ** -13 * R(10) ** -3 == R('4.5') * R(10) ** -16  # P2
assert 8 * 60 + 20 == 500                                                # P3
assert 3 * 10 ** 5 * 500 == R('1.5') * 10 ** 8                           # P3
assert R('1.5') * 10 ** 8 * 10 ** 3 == R('1.5') * 10 ** 11               # P3
assert round(2 ** 0.5, 3) == 1.414 and R('1.4') ** 2 == R('1.96') != 2   # P4
assert R('6.4') * 10 ** 9 / (8 * 10 ** 6) == 800                         # P5
assert divmod(800, 60) == (13, 20) and R(800, 600) == R(4, 3)            # P5
assert R('0.1') * 2 ** 10 == R('102.4') and R('102.4') / 10 == R('10.24')  # P6
assert 2 ** 20 == 1048576 and R('0.1') * 2 ** 20 == R('104857.6')        # P6
assert R('104857.6') / 1000 > 100                                        # P6
assert 5 ** 2 == 25 and 2 * 25 == 50                                     # P7
assert simplify(sqrt(50) - 5 * sqrt(2)) == 0                             # P7
assert round(float(5 * sqrt(2)), 1) == 7.1 and (5 * sqrt(2)) ** 2 == 50  # P7
assert 10 ** 2 == 100 == 4 * 25                                          # P7

# Questions ajoutées (standard : exercices complets, >= 5 questions)
assert 5 ** 3 == 125 and (-3) ** 4 == 81                                 # D1 Q2
assert R(10) ** -1 == R('0.1') and R(1, 25) == R(5) ** -2                # D1 Q4-5
assert (-1) ** 10 == 1 and (-1) ** 15 == -1                              # D2 Q5
assert 7 ** 5 * R(7) ** -2 == 7 ** 3                                     # D3 Q4
assert (3 * 5) ** 2 == 225 == 3 ** 2 * 5 ** 2                            # D3 Q5
assert R('3.45') * 10 ** 3 == 3450 and 6 * R(10) ** -2 == R('0.06')      # D4 Q3-4
assert 25 * 10 ** 3 == R('2.5') * 10 ** 4                                # D4 Q5
assert sqrt(225) == 15 and sqrt(1) == 1 and sqrt(0) == 0                 # D5 Q4-5
assert sqrt(10 ** 4) == 100                                              # D5 Q5
assert 2 * 10 ** 3 * R('3.5') * 10 ** 4 == 7 * 10 ** 7                   # E1 Q3
assert (5 * R(10) ** -2) ** 2 == R('2.5') * R(10) ** -3                  # E1 Q4
assert R('2.4') * 10 ** 4 == 24000                                       # E1 Q5
assert 9 * 10 ** 4 / (3 * R(10) ** -2) == 3 * 10 ** 6                    # E2 Q3
assert 4 * R(10) ** -8 == R('0.00000004')                                # E2 Q4
assert 6 ** 2 < 37 < 7 ** 2 and 9 ** 2 < 90 < 10 ** 2                    # E3 Q1/Q4
assert round(90 ** 0.5, 1) == 9.5 and round(90 ** 0.5, 4) == 9.4868      # E3 Q5
assert simplify(sqrt(75) - 5 * sqrt(3)) == 0                             # E4 Q4
assert simplify(sqrt(27) - 3 * sqrt(3)) == 0                             # E4 Q4
assert simplify(sqrt(75) - sqrt(27) - 2 * sqrt(3)) == 0                  # E4 Q5
assert sqrt(4 * 9) == 6 == sqrt(4) * sqrt(9)                             # E5 Q3
assert sqrt(36 * 25) == 30                                               # E5 Q5
assert (-3) ** 4 == 81 and -(3 ** 4) == -81                              # E6 Q4
assert 5 ** 0 == 1 and 0 ** 5 == 0                                       # E6 Q5
assert 4 * 13 == 52                                                      # E7 Q2
assert (2 * sqrt(3)) ** 2 == 12                                          # E7 Q4
assert 800 * 2 ** 9 == 409600 and 180 // 20 == 9                         # P1 Q3
assert 800 * 2 ** 7 == 102400 > 100000 > 51200                           # P1 Q4
assert 7 * 20 == 140                                                     # P1 Q4
assert R('4.5') * R(10) ** -13 * 10 ** 15 == 450                         # P2 Q4
assert 9 / (R('4.5') * R(10) ** -13) == 2 * 10 ** 13                     # P2 Q5
assert 5 * 4 * 10 ** 12 == 2 * 10 ** 13                                  # P2 Q5
assert 3 * 10 ** 5 * R('1.28') == R('3.84') * 10 ** 5                    # P3 Q4
assert 3 * 10 ** 5 * R('3.15') * 10 ** 7 == R('9.45') * 10 ** 12         # P3 Q5
assert simplify(sqrt(8) - 2 * sqrt(2)) == 0                              # P4 Q4
assert round(float(2 * sqrt(2)), 2) == 2.83                              # P4 Q4
assert float(2 * sqrt(2) / sqrt(2)) == 2 and 8 / 2 == 4                  # P4 Q5
assert abs(R('6.4') * 10 ** 9 / 600 - R('1.07') * 10 ** 7) < 10 ** 5     # P5 Q4
assert 8 * 10 ** 6 * 3600 == R('2.88') * 10 ** 10                        # P5 Q5
assert R('2.88') * 10 ** 10 / 10 ** 9 == R('28.8')                       # P5 Q5
assert 2 ** 21 == 2097152 < 3300000 < 4194304 == 2 ** 22                 # P6 Q5
assert R('0.1') * 2 ** 22 / 1000 > 330                                   # P6 Q5
assert 9 == 3 ** 2                                                       # P7 Q5

print("check_ch02 : tous les contrôles passent.")
