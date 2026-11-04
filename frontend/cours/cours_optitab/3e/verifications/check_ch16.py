# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 16 (Géométrie dans l'espace)."""
import math
from fractions import Fraction as F

pi = math.pi
boule = lambda r: F(4, 3) * r ** 3       # noqa: E731  (coefficient de pi)
cone = lambda r, h: F(r * r * h, 3)       # noqa: E731  (coefficient de pi)

# Cours
assert cone(4, 9) == 48 and round(48 * pi, 1) == 150.8
assert F(1, 2) ** 3 == F(1, 8)

# Découverte
assert 8 * 5 * 3 == 120 and (8 * 3, 8 * 5, 5 * 3) == (24, 40, 15)          # D1
assert 2 * (24 + 40 + 15) == 158 and F(120, 1000) == F(12, 100)             # D1
assert round(9 * pi, 1) == 28.3 and 9 * 10 == 90 and round(90 * pi) == 283  # D2
assert 9 * 20 == 180 and 36 * 10 == 360                                     # D2
assert 6 ** 2 == 36 and 36 * 9 / 3 == 108 and 36 * 9 == 324 == 3 * 108      # D3
assert 3 * 144 / 36 == 12                                                   # D3
assert 8 / 2 == 4 and 4 ** 2 == 16 and cone(4, 9) == 48 and round(48 * pi) == 151  # D4
assert 16 * 9 == 144 == 3 * 48 and cone(8, 9) == 4 * cone(4, 9)             # D4
assert boule(3) == 36 and round(36 * pi, 1) == 113.1 and 4 * 3 ** 2 == 36   # D5
assert boule(6) == 288 == 8 * 36 and 4 * 6 ** 2 == 144 == 4 * 36            # D5
assert 6 * 2 ** 2 == 24 and 2 ** 3 == 8                                     # D6

# Entraînement
assert 8 * 5 == 40 and 8 * 5 * 6 == 240 and 40 * 2 == 80 and 40 * 4 == 160 and 8 * 6 == 48  # E1
assert 0 < 2 < 6 and 0 < 3 < 4 and 0 < 1 < 3 and (6 / 2, 4 / 2, 3 / 2) == (3, 2, 1.5)  # E2
assert 20 + 50 == 70 and 35 + 35 == 70                                      # E3
assert 5 ** 2 - 3 ** 2 == 4 ** 2 and round(16 * pi, 1) == 50.3              # E4
assert 5 ** 2 - 3 ** 2 == 16 and math.isqrt(16) == 4                        # E4
assert 1 * 2 == 2 and boule(1) / 2 == F(2, 3) and 2 + F(2, 3) == F(8, 3)    # E5
assert round(8000 * pi / 3) == 8378 and round(8378 / 20) == 419             # E5
assert boule(5) == F(500, 3) and boule(2) == F(32, 3) and boule(5) - boule(2) == 156  # E6
assert round(156 * pi) == 490 and round(156 * pi * 7.8) == 3823             # E6
assert cone(6, 12) == 144 and 144 * F(1, 8) == 18 and 144 - 18 == 126       # E7
assert 6 * F(1, 2) == 3 and 36 * F(1, 4) == 9 and round(126 * pi) == 396 and F(126, 144) == F(7, 8)  # E7

# Problèmes
assert 9 * 8 == 72 and cone(3, 2) == 6 and round(78 * pi) == 245           # P1
m = 0.8 * 78 * pi * 0.75
assert round(0.8 * 78 * pi, 1) == 196.0 and round(m) == 147 and math.ceil(m / 25) == 6  # P1
assert round(math.sqrt(72), 2) == 8.49 and 72 + 36 == 108 and round(math.sqrt(108), 2) == 10.39  # P2
assert math.isclose(math.sqrt(72), 6 * math.sqrt(2)) and math.isclose(math.sqrt(108), 6 * math.sqrt(3))  # P2
assert 10 < math.sqrt(108) < 11 and 6 ** 3 == 216 == 6 * 6 ** 2             # P2
assert cone(3, 10) == 30 and boule(3) / 2 == 18 and round(48 * pi, 1) == 150.8  # P3
assert round(2000 / (48 * pi), 1) == 13.3 and int(2000 // (48 * pi)) == 13 and 13 * 2.5 - 12 == 20.5  # P3
assert 35 ** 2 * F(216, 10) / 3 == 8820 and 35 / 2 == 17.5                  # P4
SI = math.sqrt(21.6 ** 2 + 17.5 ** 2)
assert round(21.6 ** 2 + 17.5 ** 2, 2) == 772.81 and round(SI, 1) == 27.8   # P4
assert round(35 * SI / 2, 1) == 486.5 and round(4 * 35 * SI / 2) == 1946    # P4
L = 2 * pi * 6371
assert round(L) == 40030 and round(L / 360, 1) == 111.2 and round(30 * L / 360) == 3336  # P5
assert f"{4 * pi * 6371 ** 2:.2e}" == "5.10e+08" and f"{4 / 3 * pi * 6371 ** 3:.2e}" == "1.08e+12"  # P5
assert cone(4, 12) == 64 and round(64 * pi) == 201                          # P6
assert F(10, 12) == F(5, 6) and round(4 * 5 / 6, 2) == 3.33                 # P6
assert 64 * F(5, 6) ** 3 == F(1000, 27) and round(1000 * pi / 27, 1) == 116.4  # P6
assert round(125 / 216, 3) == 0.579 and round(100 * 125 / 216) == 58        # P6
assert 80 * 40 * 50 == 160000 and 80 * 40 * 45 == 144000 and 144 / 6 == 24  # P7
assert boule(6) == 288 and round(288 * pi) == 905                           # P7
h = 288 * pi / 3200
assert round(h, 2) == 0.28 and round(45 + h, 1) == 45.3 < 50                # P7

print("check_ch16 : tous les contrôles passent.")
