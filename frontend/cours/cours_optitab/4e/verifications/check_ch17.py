# -*- coding: utf-8 -*-
"""Contrôles du chapitre 17 (pyramides, cônes et volumes) — 4ème."""
from math import pi, sqrt, acos, degrees, floor, ceil

r = lambda v, n=2: round(v + 1e-12, n)  # noqa: E731
pyr = lambda b, h: b * h / 3  # noqa: E731
cone = lambda rr, h: pi * rr * rr * h / 3  # noqa: E731
ac = lambda x: degrees(acos(x))  # noqa: E731

# Cours
assert pyr(36, 5) == 60 and r(cone(3, 10), 1) == 94.2
# D1
assert 5 + 5 - 8 == 2
# D2
assert 16 + 9 == 25 and r(9 * pi) == 28.27
# D3
assert pyr(36, 5) == 60 and 6 * 6 * 5 == 180 and 180 / 60 == 3
# D4
assert r(9 * pi) == 28.27 and r(cone(3, 10)) == 94.25 and r(90 * pi, 1) == 282.7 and r(cone(3, 10) / 10, 1) == 9.4
# D5
assert 4 * 3 / 2 == 6 and pyr(6, 6) == 12 and 16 + 9 == 25 and r(sqrt(52)) == 7.21
# D6
assert 50 * 30 * 40 == 60000 and 0.3 * 1000 == 300
# D7
h = sqrt(21)
assert r(h) == 4.58 and r(2 * h) == 9.17 and r(8 * h) == 36.66 and r(16 + 8 * h, 1) == 52.7

# E1
SH = sqrt(21.6 ** 2 + 17.5 ** 2)
assert 35 * 35 == 1225 and r(pyr(1225, 21.6)) == 8820 and r(21.6 ** 2) == 466.56 and r(SH ** 2) == 772.81
assert r(SH) == 27.80 and r(35 * SH / 2, 1) == 486.5 and round(4 * 35 * SH / 2) == 1946 and r(8820 / 200, 1) == 44.1
# E2
V = cone(2.5, 12)
assert r(6.25 * pi) == 19.63 and r(V) == 78.54 and r(V / 10, 1) == 7.9 and r(sqrt(150.25)) == 12.26
assert floor(1000 / V) == 12 and r(1000 / V, 1) == 12.7 and r(cone(5, 12), 1) == 314.2 and r(cone(5, 12) / V, 6) == 4
# E3
V = cone(2, 1.5)
assert r(V) == 6.28 and r(V * 1.6) == 10.05 and ceil(V * 1.6 / 8) == 2 and 2.25 + 4 == 6.25 and r(ac(0.8), 1) == 36.9
assert r(cone(4, 1.5), 1) == 25.1
# E4
h = 300 / (16 * pi)
assert 75 * 3 / 25 == 9 and r(h) == 5.97 and r(cone(4, h), 1) == 100.0 and r(100 / (16 * pi)) == 1.99
assert r(16 * pi * 5.968 / 3, 1) == 100.0
# E5
assert 6 ** 3 == 216 and pyr(36, 6) == 72 and r(54 * pi, 1) == 169.6 and r(cone(3, 6), 1) == 56.5
assert r(cone(3, 6) / 216) == 0.26
# E6
assert pyr(24, 5) == 40 and 24 * 5 == 120 and r(20 * 5 / 3, 1) == 33.3 and pyr(24, 7) == 56
assert r(cone(3, 4), 1) == 37.7 and r(cone(6, 4), 1) == 150.8 and r(cone(6, 4) / cone(3, 4), 6) == 4
# E7
sh = sqrt(4.24)
assert r(pyr(4, 1.8), 6) == 2.4 and floor(2.4) == 2 and r(sh) == 2.06 and r(sh, 3) == 2.059
assert r(4 * sh) == 8.24 and r(4 * sh + 4) == 12.24 and r(4 * sh + 4, 4) == 12.2365 and r((4 * sh + 4) * 6) == 73.42

# P1
assert r(cone(3, 4)) == 37.70 and r(2 * cone(3, 4)) == 75.40 and r(0.8 * cone(3, 4)) == 30.16
assert round(0.8 * cone(3, 4) / 0.5) == 60 and 180 * 0.5 == 90 > cone(3, 4)
# P2
assert 10 * 8 * 2.5 == 200 and pyr(80, 3) == 80 and r(80 / 280 * 100, 1) == 28.6 and 280 * 40 == 11200
assert 300 / 80 == 3.75
# P3
assert r(48 * pi, 1) == 150.8 and r(48 * pi / 10, 1) == 15.1 and 4 * 4.5 / 9 == 2 and r(6 * pi) == 18.85
assert r(cone(2, 4.5) / cone(4, 9), 6) == 0.125 and r(120 / (48 * pi)) == 0.80
# P4
V = pyr(230 ** 2, 146)
assert 230 ** 2 == 52900 and round(V) == 2574467 and round(V / 1.1) == 2340424 and r(2340424 / 7300, 1) == 320.6
assert 146 ** 2 + 115 ** 2 == 34541 and r(sqrt(34541), 1) == 185.9 and r(115 / sqrt(34541), 3) == 0.619
assert r(ac(115 / sqrt(34541)), 1) == 51.8
# P5
assert r(24 * pi) == 75.40 and r(2 * pi) == 6.28 and r(26 * pi) == 81.68 and r(26 * pi * 0.75) == 61.26
assert r(0.9 * 26 * pi * 0.75) == 55.13 and ceil(0.9 * 26 * pi * 0.75 / 25) == 3
# P6
assert pyr(36, 9) == 108 and r(108 * 0.9, 1) == 97.2 and floor(1000 / 97.2) == 10 and r(cone(3, 9), 1) == 84.8
assert r(27 * pi / 108, 3) == 0.785 and r(36 / pi) == 11.46 and r(sqrt(36 / pi)) == 3.39
# P7
h = sqrt(68.75)
V = cone(3.5, h)
assert r(81 - 12.25) == 68.75 and r(h) == 8.29 and r(V, 1) == 106.4 and r(V / 10, 1) == 10.6
assert floor(18900 / V) == 177 and r(18900 / V, 1) == 177.7 and r(ac(h / 9), 1) == 22.9 and r(cone(3.5, 9), 1) == 115.5

print("check_ch17 : tous les contrôles passent.")
