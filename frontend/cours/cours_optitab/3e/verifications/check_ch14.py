# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 14 (Trigonométrie)."""
import math
from math import sin, cos, tan, asin, acos, atan, radians, degrees

d = radians
r1 = lambda v: round(v, 1)  # noqa: E731
r2 = lambda v: round(v, 2)  # noqa: E731

# Cours
assert r2(10 * sin(d(35))) == 5.74
assert r1(degrees(acos(0.6))) == 53.1 and r1(90 - degrees(acos(0.6))) == 36.9
assert round(cos(d(60)), 10) == 0.5

# Découverte
assert 6 / 10 == 0.6 and 8 / 10 == 0.8                                  # D2
assert r1(12 * sin(d(30))) == 6.0 and r1(12 * cos(d(30))) == 10.4        # D3
assert abs((12 * cos(d(30))) ** 2 + 36 - 144) < 1e-9                     # D3
assert r1(9 * cos(d(40))) == 6.9 and r1(9 * sin(d(40))) == 5.8           # D4
assert r1(7 / cos(d(50))) == 10.9 and r1(7 * cos(d(50))) == 4.5         # D5
assert r1(7 * tan(d(50))) == 8.3                                         # D5
assert round(degrees(acos(0.6))) == 53 and round(90 - degrees(acos(0.6))) == 37  # D6

# Entraînement
assert r1(degrees(atan(5 / 12))) == 22.6 and math.isclose(math.hypot(5, 12), 13)  # E1
assert r1(degrees(asin(5 / 13))) == 22.6                                 # E1
assert round(degrees(asin(0.8))) == 53 and r1(degrees(atan(0.75))) == 36.9  # E2
assert r1(18 * sin(d(65))) == 16.3 and r1(18 * cos(d(65))) == 7.6        # E3
assert abs((18 * sin(d(65))) ** 2 + (18 * cos(d(65))) ** 2 - 324) < 1e-9  # E3
assert r1(7 * tan(d(38))) == 5.5 and r1(7 / cos(d(38))) == 8.9           # E4
assert r1(degrees(atan(0.08))) == 4.6 and r2(math.sqrt(100.64)) == 10.03  # E5
assert r1(40 * sin(d(55))) == 32.8 and r1(40 * sin(d(55)) + 1.2) == 34.0  # E6
assert r1(40 * cos(d(55))) == 22.9 and r1(40 * sin(d(70))) == 37.6       # E6
assert round(degrees(asin(2.7 / 4.5))) == 37 and math.isclose(math.sqrt(4.5 ** 2 - 2.7 ** 2), 3.6)  # E7
assert r1(degrees(acos(3.6 / 4.5))) == 36.9                              # E7

# Problèmes
h1 = 25 * tan(d(32))
assert r2(h1) == 15.62 and r1(h1 + 1.6) == 17.2 and round(1.6 / (h1 + 1.6), 2) == 0.09  # P1
hh, v = 4 * tan(d(35)), 4 / cos(d(35))
assert r2(hh) == 2.80 and r2(v) == 4.88 and r2(8 * hh / 2) == 11.20      # P2
assert round(2 * v * 12) == 117                                          # P2
AT = 30 * tan(d(52))
assert r1(AT) == 38.4 and r1(30 / cos(d(52))) == 48.7                    # P3
assert round(degrees(atan(AT / 50))) == 38                               # P3
assert 90 * 20 == 1800 and round(1800 * sin(d(12))) == 374               # P4
assert round(1800 * cos(d(12))) == 1761 and round(1000 / sin(d(12)) / 90) == 53  # P4
assert round(90 * 3.6) == 324                                            # P4
d1, d2 = 45 / tan(d(8)), 45 / tan(d(15))
assert round(d1) == 320 and round(d2) == 168 and round(d1 - d2) == 152   # P5
a = degrees(atan(0.12))
assert r1(a) == 6.8 and r1(math.hypot(100, 12)) == 100.7                 # P6
assert round(2000 * sin(d(a))) == 238 and math.isclose(tan(d(45)), 1)    # P6
assert r1(25 * sin(d(75)) + 2) == 26.1 and r1(25 * sin(d(60)) + 2) == 23.7  # P7
assert round(degrees(asin(20 / 25))) == 53                               # P7
assert round(degrees(asin(23 / 25))) == 67 and r1(25 * cos(asin(0.92))) == 9.8  # P7

print("check_ch14 : tous les contrôles passent.")
