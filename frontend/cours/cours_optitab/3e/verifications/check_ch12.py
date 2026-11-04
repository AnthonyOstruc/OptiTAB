# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 12 (Pythagore)."""
from sympy import Rational as R, sqrt, simplify
import math

# Cours
assert 6 ** 2 + 8 ** 2 == 10 ** 2 and 13 ** 2 - 5 ** 2 == 12 ** 2
assert 9 ** 2 + 12 ** 2 == 15 ** 2 and 6 ** 2 + 8 ** 2 == 100
assert 3 ** 2 + 4 ** 2 == 5 ** 2

# Découverte
assert 6 + 8 + 10 == 24 and 6 * 8 / 2 == 24                              # D2
assert 13 ** 2 - 5 ** 2 == 144 and 5 * 12 / 2 == 30                      # D3
assert 4 ** 2 + 7 ** 2 == 65 and round(math.sqrt(65), 1) == 8.1          # D4
assert 64 < 65 < 81 and round(4 + 7 + math.sqrt(65), 1) == 19.1          # D4
assert 15 ** 2 == 225 == 9 ** 2 + 12 ** 2                                # D5
assert 9 ** 2 == 81 != 5 ** 2 + 7 ** 2 == 74                             # D6
assert round(math.sqrt(74), 1) == 8.6                                    # D6
assert 7 ** 2 + 24 ** 2 == 625 == 25 ** 2                                # D7
assert sqrt(10 ** 2 - 6 ** 2) == 8 and sqrt(R('1.5') ** 2 + 4) == R('2.5')  # D7

# Entraînement
assert 25 - R('1.4') ** 2 == R('23.04') == R('4.8') ** 2                 # E1
assert 25 - 9 == 16 and 25 - R('4.9') ** 2 == R('0.99')                  # E1
assert round(math.sqrt(0.99), 2) == 0.99                                 # E1
assert 20 ** 2 + 15 ** 2 == 625 and 2 * (20 + 15) == 70 and 20 * 15 == 300  # E2
assert simplify(sqrt(450) - 15 * sqrt(2)) == 0 and round(15 * math.sqrt(2), 1) == 21.2  # E2
assert 7 - 1 == 6 and 10 - 2 == 8 and 6 ** 2 + 8 ** 2 == 100             # E3
assert 6 ** 2 + 8 ** 2 == 10 ** 2 and 6 * 8 / 2 == 24 and R(48, 10) == R('4.8')  # E4
assert 16 - R('2.4') ** 2 == R('10.24') == R('3.2') ** 2                 # E5
assert R('2.4') * R('3.2') / 2 == R('3.84') and R('3.84') * 25 == 96     # E5
assert R('2.4') + R('3.2') + 4 == R('9.6')                               # E5
assert R('0.9') ** 2 + R('1.2') ** 2 == R('2.25') == R('1.5') ** 2       # E6
assert 4 - (-2) == 6 and 9 - 1 == 8 and 36 + 64 == 100                   # E7

# Problèmes
assert 10 ** 2 + R('0.75') ** 2 == R('100.5625')                         # P1
assert round(math.sqrt(100.5625), 2) == 10.03                            # P1
assert R('0.75') / 10 * 100 == R('7.5') and R(75, 5) == 15               # P1
assert 160 + 120 == 280 and 160 ** 2 + 120 ** 2 == 200 ** 2              # P2
assert 280 - 200 == 80 and round(80 / 280 * 100, 1) == 28.6              # P2
assert R(80 * 60, 4000) == R('1.2')                                      # P2
assert 13 ** 2 - 5 ** 2 == 12 ** 2 and 10 * 12 / 2 == 60 and 13 + 13 + 10 == 36  # P3
assert 3 ** 2 + 4 ** 2 == 5 ** 2 and 5 ** 2 + 12 ** 2 == 13 ** 2         # P4
assert round(10 * math.sqrt(2), 1) == 14.1 and round(10 * math.sqrt(3), 1) == 17.3  # P4
assert simplify(sqrt(300) - 10 * sqrt(3)) == 0                           # P4
assert 36 + R('20.25') == R('56.25') == R('7.5') ** 2                    # P5
assert 4 * R('7.5') == 30 and 30 * R('2.40') == 72                       # P5
assert 36 + 64 == 100 and 4 * 10 == 40                                   # P5
assert 120 ** 2 + R('67.5') ** 2 == R('18956.25')                        # P6
assert round(math.sqrt(18956.25), 1) == 137.7                            # P6
assert round(math.sqrt(18956.25) / 2.54) == 54                           # P6
assert R(120, R('67.5')) == R(16, 9) and 120 * R('67.5') == 8100         # P6
assert 12 ** 2 + 5 ** 2 == 13 ** 2 and R(13, 26) == R('0.5')             # P7
assert 12 + 5 + 13 == 30 and 17 - 13 == 4                                # P7

print("check_ch12 : tous les contrôles passent.")
