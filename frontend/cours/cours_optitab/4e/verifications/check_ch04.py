# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 4 (carrés et racines carrées) — 4ème."""
from fractions import Fraction as F
from math import sqrt, pi, isqrt

D = lambda s: F(s)  # noqa: E731
r2 = lambda x, n=2: round(x + 1e-12, n)  # noqa: E731

# Cours / fiche
assert (-6) ** 2 == 36 and 2 * 3 ** 2 == 18 and (2 * 3) ** 2 == 36 and 3 ** 2 + 4 ** 2 == 25 and 7 ** 2 == 49
assert D('0.5') ** 2 == D('0.25') and D('4.4') ** 2 == D('19.36') and D('4.5') ** 2 == D('20.25')
assert r2(sqrt(20), 3) == 4.472 and D('4.47') ** 2 == D('19.9809') and D('44.1') / D('4.9') == 9
assert 12 ** 2 == 144 and D('0.3') ** 2 == D('0.09')

# D1
assert [n * n for n in (3, 6, 9, 11, 13, 15)] == [9, 36, 81, 121, 169, 225]
assert [k * k for k in range(1, 16) if 50 <= k * k <= 150] == [64, 81, 100, 121, 144]
assert 14 ** 2 == 196 and isqrt(200) ** 2 != 200
assert sorted({(k * k) % 10 for k in range(10)}) == [0, 1, 4, 5, 6, 9]
# D2
assert D('0.5') ** 2 == D('0.25') and D('0.1') ** 2 == D('0.01') and D('0.5') > D('0.25')
# D3
assert D('1.5') ** 2 == D('2.25') and 25 < 30 < 36 and r2(sqrt(30), 2) == 5.48
assert D('5.48') ** 2 == D('30.0304') and r2(4 * sqrt(30), 1) == 21.9
# D4
assert r2(sqrt(20), 2) == 4.47 and r2(sqrt(50), 2) == 7.07 and r2(sqrt(90), 2) == 9.49
# D5
assert 3 + 4 == 7 and isqrt(25) == 5 and 3 * 4 == isqrt(144) and isqrt(9) == 3 == 6 // 2
assert isqrt(36) == 6 and 10 - 8 == 2
# D6
assert r2(sqrt(2), 4) == 1.4142
# D7
assert (3 + 4) ** 2 == 49 and 5 ** 2 - 3 ** 2 == 16 and (5 - 3) ** 2 == 4
assert isqrt(5 ** 2 - 4 ** 2) == 3 and isqrt(6 ** 2 + 8 ** 2) == 10 and 10 ** 2 - 2 * 6 ** 2 == 28

# E1
assert isqrt(196) == 14 and 4 * 14 == 56 and 56 * D('12.5') == 700
assert r2(sqrt(200), 2) == 14.14 and r2(4 * sqrt(200), 2) == 56.57 and 57 * D('12.5') == D('712.5')
# E2
assert 18 * 8 == 144 and 2 * (18 + 8) == 52 and 4 * 12 == 48 and 5 * 20 == 100
assert r2(sqrt(90), 2) == 9.49 and r2(4 * sqrt(90), 2) == 37.95 and 2 * (6 + 15) == 42
# E3
assert [D('4.9') * t * t for t in (1, 2, 3)] == [D('4.9'), D('19.6'), D('44.1')]
assert D('122.5') / D('4.9') == 25 and r2(sqrt(100 / 4.9), 2) == 4.52
assert r2(324 / 4.9, 2) == 66.12 and r2(sqrt(324 / 4.9), 2) == 8.13
assert D('88.2') / D('4.9') == 18 and r2(sqrt(18), 2) == 4.24 and r2(sqrt(18) / 3, 2) == 1.41
# E4
assert [(v // 10) ** 2 for v in (50, 90, 130, 80, 100)] == [25, 81, 169, 64, 100]
assert 81 * D('1.5') == D('121.5')
# E5
assert D('1.41') ** 2 == D('1.9881') and D('1.42') ** 2 == D('2.0164')
assert D('1.414') ** 2 == D('1.999396') and D('1.415') ** 2 == D('2.002225')
assert D('1.7') ** 2 == D('2.89') and D('1.8') ** 2 == D('3.24') and D('1.6') ** 2 == D('2.56')
# E6
assert 8 ** 2 == 64 == 4 * 16 and r2(sqrt(32), 3) == 5.657
# E7
assert isqrt(86 - 5) == 9 and isqrt(98 // 2) == 7 and 22 ** 2 == 484 and 23 ** 2 == 529
assert 101 ** 2 == 10201

# P1
assert isqrt(2025) == 45 and 43 ** 2 == 1849 and 2025 - 1849 == 176 == 4 * 44
assert 176 * D('0.05') == D('8.8') and D('8.8') * 35 == 308
# P2
assert r2(sqrt(72), 3) == 8.485 and r2(sqrt(72) / 6, 3) == 1.414 and 18 ** 2 == 9 * 36
assert r2(100 / 6, 1) == 16.7 and r2(10000 / 36, 1) == 277.8
# P3
assert 2 * sqrt(1) == 2 and 2 * sqrt(0.25) == 1 and 2 * sqrt(4) == 4 and D('1.5') ** 2 == D('2.25')
assert r2(2 * sqrt(67), 1) == 16.4 and r2(sqrt(67), 3) == 8.185
# P4
assert 6 ** 2 + 8 ** 2 == 100 and 5 ** 2 + 12 ** 2 == 169 and r2(sqrt(5), 2) == 2.24
# P5
assert D('0.3') ** 2 == D('0.09') and D('4.5') ** 2 == D('20.25') and D('4.5') / D('0.3') == 15
assert D('20.25') / D('0.09') == 225 and 225 * D('1.1') == D('247.5')
assert r2(248 / 12, 2) == 20.67 and 21 * D('18.90') == D('396.90') and 248 - 240 == 8
# P6
assert r2(sqrt(39200), 2) == 197.99 and 198 * D('3.6') == D('712.8')
assert r2(sqrt(98), 1) == 9.9 and r2(9.9 * 3.6, 1) == 35.6 and 49 ** 2 == 2401
assert D(2401) / D('9.8') == 245 and r2(3000 / 713, 2) == 4.21 and round(0.2076 * 60) == 12
# P7
assert r2(225 * pi, 1) == 706.9 and r2(200 * pi, 1) == 628.3
assert r2(14 / (225 * pi), 3) == 0.020 and r2(18 / (200 * pi), 3) == 0.029
assert r2(2 * sqrt(200), 1) == 28.3 and r2(1000 / pi, 2) == 318.31
assert r2(sqrt(1000 / pi), 2) == 17.84 and r2(2 * sqrt(1000 / pi), 1) == 35.7

print("check_ch04 : tous les contrôles passent.")
