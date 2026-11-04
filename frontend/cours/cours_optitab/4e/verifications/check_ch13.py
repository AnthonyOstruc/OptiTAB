# -*- coding: utf-8 -*-
"""Contrôles du chapitre 13 (Pythagore) — 4ème."""
from fractions import Fraction as F
from math import sqrt, isqrt

D = lambda s: F(s)  # noqa: E731
r = lambda v, n=2: round(float(v) + 1e-12, n)  # noqa: E731
rect = lambda a, b, c: max(a, b, c) ** 2 * 2 == a * a + b * b + c * c  # noqa: E731

# Cours
assert 81 + 144 == 225 == 15 ** 2 and 289 - 64 == 225 and 841 == 400 + 441 and 81 != 36 + 49
# D1
assert 5 ** 2 + 12 ** 2 == 13 ** 2
# D2
assert 9 ** 2 + 12 ** 2 == 225 and 9 + 12 + 15 == 36 and 9 * 12 / 2 == 54 and 2 * 54 / 15 == 7.2
# D3
assert 17 ** 2 - 8 ** 2 == 225 and 17 + 8 + 15 == 40 and 8 * 15 / 2 == 60 and r(120 / 17) == 7.06
assert 289 + 64 == 353
# D4
assert 49 + 25 == 74 and 64 < 74 < 81 and r(sqrt(74), 1) == 8.6 and r(sqrt(74)) == 8.60
assert r(12 + sqrt(74), 1) == 20.6 and 100 - 36 == 64
# D5
assert rect(20, 21, 29) and rect(7, 24, 25)
# D6
assert not rect(6, 7, 9) and rect(8, 15, 17) and rect(1.5, 2, 2.5) and not rect(4, 5, 6)
# D7
assert rect(3, 4, 5) and rect(6, 8, 10) and rect(30, 40, 50) and rect(5, 12, 13)
assert isqrt(81 + 1600) == 41 and 41 ** 2 == 1681 and 61 ** 2 - 11 ** 2 == 3600 and isqrt(3600) == 60

# E1
assert D('4.5') ** 2 - D('1.2') ** 2 == D('18.81') and r(sqrt(18.81)) == 4.34
assert r(sqrt(16.25)) == 4.03 and D('20.25') - D('4.2') ** 2 == D('2.61') and r(sqrt(2.61)) == 1.62
# E2
assert 40 ** 2 + 20 ** 2 == 2000 and r(sqrt(2000)) == 44.72 and r(60 - sqrt(2000)) == 15.28
assert r((60 - sqrt(2000)) / 60 * 100, 1) == 25.5 and r((60 - sqrt(2000)) / 5) == 3.06
assert r((40 - sqrt(800)) / 40 * 100, 1) == 29.3
# E3
assert 100 - 36 == 64 and 12 * 8 / 2 == 48 and 10 + 10 + 12 == 32 and 100 - 64 == 36 and 16 * 6 / 2 == 48
# E4
assert 6 ** 2 + 8 ** 2 == 100 and 3 ** 2 + 4 ** 2 == 25 and 9 ** 2 + 4 ** 2 == 97 and r(sqrt(97)) == 9.85
assert 100 != 25 + 97
# E5
assert 64 + 36 == 100 and 16 * 12 / 2 == 96 == 4 * 24 and 169 - 25 == 144
# E6
assert rect(3, 4, 5) and 12 * D('0.5') == 6 and rect(6, 8, 10) and 5 + 12 + 13 == 30 and not rect(2, 5, 5)

# P1
assert D('2.4') ** 2 + D('3.2') ** 2 == 16 and D('5.76') + D('20.25') == D('26.01') == D('5.1') ** 2
assert D('2.4') / D('3.2') == D('0.75') and r(2.4 / 4.5 * 100, 1) == 53.3 and D('2.4') / D('0.6') == 4
assert r(sqrt(21.76)) == 4.66
# P2
assert 105 ** 2 + 68 ** 2 == 15649 and r(sqrt(15649), 1) == 125.1 and 105 + 68 == 173
assert r(173 - sqrt(15649), 1) == 47.9 and r((173 - sqrt(15649)) / 173 * 100, 1) == 27.7
assert r(sqrt(15649) / 7) == 17.87 and r(173 / 7) == 24.71 and r(sqrt(15649) / 2, 1) == 62.5
assert 68 ** 2 + 40 ** 2 == 6224 and r(sqrt(6224), 1) == 78.9
# P3
assert D('2.25') - D('0.81') == D('1.44') and D('1.8') * D('1.2') / 2 == D('1.08')
assert 2 * D('1.5') * D('2.2') == D('6.6') and D('6.6') + D('2.16') + D('3.96') == D('12.72')
assert D('1.08') * D('2.2') == D('2.376')
# P4
assert 30 ** 2 + 20 ** 2 == 1300 and r(sqrt(1300)) == 36.06 and 1300 + 144 == 1444 and isqrt(1444) == 38
assert r(sqrt(40 ** 2 + 30 ** 2 + 20 ** 2), 1) == 53.9
# P5
assert r(sqrt(2)) == 1.41 and r(sqrt(3)) == 1.73 and [n for n in range(1, 20) if isqrt(n) ** 2 == n] == [1, 4, 9, 16]
# P6
assert 15 + 8 + 9 == 32 and 15 ** 2 + 8 ** 2 == 289 and 8 ** 2 + 6 ** 2 == 100 and 32 / 8 == 4 and 10 / 8 == 1.25
# P7
d = 55 * 2.54
k = sqrt(d * d / 337)
assert r(d, 1) == 139.7 and 16 ** 2 + 9 ** 2 == 337 and r(k, 3) == 7.610
assert r(16 * k, 1) == 121.8 and r(9 * k, 1) == 68.5 and r(16 * k * 9 * k / 1e4) == 0.83
k2 = d / 5
assert r(4 * k2) == 111.76 and r(3 * k2) == 83.82 and r(4 * k2 * 3 * k2 / 1e4) == 0.94
assert r(sqrt(121.8 ** 2 + 68.5 ** 2), 1) == 139.7

print("check_ch13 : tous les contrôles passent.")
