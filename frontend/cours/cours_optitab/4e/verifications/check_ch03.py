# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 3 (puissances et notation scientifique) — 4ème."""
from fractions import Fraction as F
from math import pi

D = lambda s: F(s)  # noqa: E731
P = lambda n: F(10) ** n  # noqa: E731  puissance de 10 exacte
close = lambda a, b, tol=0.006: abs(float(a) / float(b) - 1) < tol  # noqa: E731

# Cours / fiche
assert 2 ** 5 == 32 and (-3) ** 2 == 9 and (-2) ** 3 == -8 and -3 ** 2 == -9 and 2 ** 3 == 8
assert P(4) * P(3) == P(7) and P(5) * P(-8) == P(-3) and P(2) / P(5) == P(-3) and P(2) ** 3 == P(6)
assert D('3.45') * P(2) == 345 and D('3.45') * P(-2) == D('0.0345')
assert 45000 == D('4.5') * P(4) and D('0.00072') == D('7.2') * P(-4) and 32 * P(4) == D('3.2') * P(5)
assert 4 * P(3) * 5 * P(-7) == 2 * P(-3) and D('9.8') * P(4) < D('3.1') * P(5)

# D1
assert 3 ** 4 == 81 and 5 ** 3 == 125 and (-2) ** 4 == 16 and 7 ** 0 == 1 and 0 ** 7 == 0
assert 2 ** 3 < 3 ** 2 and 2 ** 4 == 4 ** 2
# D2
assert 2 ** 3 * D('0.1') == D('0.8') and 2 ** 7 == 128 and 128 * D('0.1') == D('12.8')
assert 2 ** 10 * D('0.1') == D('102.4') and 2 ** 13 == 8192 and 2 ** 14 == 16384
assert D('0.1') * 2 ** 13 < 1000 < D('0.1') * 2 ** 14
assert close(2 ** 42, D('4.4') * P(12), 0.01) and D('4.4') * P(12) * P(-4) / P(3) == D('4.4') * P(5)
# D3
assert P(-1) == D('0.1') and P(-3) == D('0.001') and P(5) == 100000 and P(-5) == D('0.00001')
assert P(-3) * P(5) == P(2)
# D4
assert 72 * P(-3) == D('0.072') and D('0.6') * P(4) == 6000 and D('4.7') * P(4) == 47000
assert D('2.5') * P(-4) == D('0.00025')
# D5
assert D('0.8') * P(3) == 8 * P(2) and D('0.056') * P(-3) == D('5.6') * P(-5) == D('0.000056')
# D6
assert 80 * P(-9) == 8 * P(-8) and P(-3) / (8 * P(-8)) == 12500
# D7
assert 3 * P(4) * 2 * P(5) == 6 * P(9) and 9 * P(8) / (3 * P(2)) == 3 * P(6)
assert D('1.2') * P(-3) / (4 * P(5)) == 3 * P(-9)
assert 5 * P(-4) < D('1.5') * P(-3) < 2 * P(-3)

# E1
assert [2 ** (n - 1) for n in range(1, 7)] == [1, 2, 4, 8, 16, 32] and 2 ** 10 == 1024
assert sum(2 ** k for k in range(5)) == 31 == 2 ** 5 - 1 and sum(2 ** k for k in range(6)) == 63
assert close(2 ** 63, D('9.2') * P(18), 0.003)
assert D('9.2') * P(18) * 2 * P(-2) == D('1.84') * P(17) and D('1.84') * P(17) / P(6) == D('1.84') * P(11)
assert D('1.84') * P(11) / (5 * P(8)) == 368
# E2
assert D('1.5') * P(8) / (3 * P(5)) == 500 and 500 == 8 * 60 + 20
assert D('3.84') * P(5) / (3 * P(5)) == D('1.28')
assert D('4.5') * P(9) / (3 * P(5)) == 15000 and 15000 - 4 * 3600 == 600
assert 3 * P(5) * D('3.15') * P(7) == D('9.45') * P(12)
assert D('4.2') * D('9.45') * P(12) == D('3.969') * P(13)
assert D('3.969') * P(13) / (D('4.5') * P(9)) == 8820
# E3
assert 80 * P(-6) == 8 * P(-5) and D('1.2') * P(-7) * P(9) == 120
assert round(float(7 * P(-6) / (D('1.2') * P(-7))), 2) == 58.33
assert round(float(8 * P(-5) / (7 * P(-6))), 1) == 11.4 and 8 * P(-5) / P(-10) == 8 * P(5)
# E4
assert (-2) ** 4 == 16 and -2 ** 4 == -16 and (-2) ** 5 == -32
assert 3 * 2 ** 3 - 4 ** 2 == 8 and (5 - 7) ** 3 * 10 ** 2 == -800 and 2 ** 10 == 1024
assert (3 * 2) ** 3 == 216
# E5
assert 64 * P(9) == D('6.4') * P(10) and D('6.4') * P(10) / (4 * P(6)) == 16000
assert int(64 / D('1.5')) == 42 and 2 * P(12) / (D('6.4') * P(10)) == D('31.25')
assert 2 * P(12) / (5 * P(5)) == 4 * P(6)
# E6
assert round(float(D('8.1') * P(9) / (D('6.8') * P(7)))) == 119
assert round(float(D('6.8') * P(7) / (D('5.5') * P(5)))) == 124
assert round(float(D('8.1') * P(9) / (D('1.49') * P(8)))) == 54
assert round(float(D('1.44') * P(9) / (D('3.29') * P(6)))) == 438
assert close(D('6.8') * P(7) / (D('5.5') * P(5)) * D('1.49') * P(8), D('1.84') * P(10), 0.003)
# E7
assert D('3.5') * P(-2) == D('0.035') and P(5) / P(-2) == P(7)

# P1
assert 6 * P(4) * 24 == D('1.44') * P(6) and D('1.44') * P(6) * 365 == D('5.256') * P(8)
t = 4 * P(13) / (6 * P(4))
assert close(t, D('6.67') * P(8)) and round(float(t / 8760), -2) == 76100
assert close(4 * P(13) / (D('5.256') * P(8)), 76100, 0.001)
assert 3 * P(5) * 3600 == D('1.08') * P(9) and D('1.08') * P(9) / (6 * P(4)) == 18000
v = 4 * P(13) / (50 * 8760)
assert 50 * 8760 == 438000 and close(v, D('9.13') * P(7), 0.001) and round(float(v / (6 * P(4))), -2) == 1500
# P2
assert [1000 * 2 ** k for k in (1, 2, 3)] == [2000, 4000, 8000]
assert 2 ** 15 * 1000 == 32768000 and close(2 ** 15 * 1000, D('3.3') * P(7), 0.01)
assert 2 ** 19 == 524288 and 2 ** 19 < 10 ** 6 < 2 ** 20 and 20 * 20 == 400 and 400 == 6 * 60 + 40
assert close(2 ** 20 * P(3) * P(-12), D('1.05') * P(-3), 0.002)
assert close(2 ** 72 * 1000, D('4.7') * P(24), 0.005) and D('4.7') * P(24) * P(-12) / P(6) == D('4.7') * P(6)
# P3
assert D('0.05') * P(-3) == 5 * P(-5)
n = 5 * P(-5) / (3 * P(-26))
assert close(n, D('1.67') * P(21), 0.002) and close(n / (8 * P(9)), D('2.1') * P(11), 0.01)
ans = n / (D('3.15') * P(7))
assert close(ans, D('5.3') * P(13), 0.002) and round(float(ans / (D('1.38') * P(10))), -2) == 3800
assert close(D('0.25') / (3 * P(-26)), D('8.33') * P(24), 0.001) and 250 / D('0.05') == 5000
# P4
assert 3840 * 2160 == 8294400 and 8294400 * 3 == 24883200 and 24883200 * 60 == 1492992000
assert D('1.5') * P(9) * D('3.6') * P(3) == D('5.4') * P(12)
assert D('5.4') * P(9) / (D('6.25') * P(6)) == 864 and 864 == 14 * 60 + 24
# P5
assert 3000 * 50 * 2 == 300000 and P(-3) ** 3 == P(-9) and 3 * P(5) / P(-9) == 3 * P(14)
assert 3 * P(14) / (2 * P(11)) == 1500 and D('0.6') * 3 * P(14) == D('1.8') * P(14)
assert close(D('1.8') * P(13) / (D('3.15') * P(7)), D('5.71') * P(5), 0.001)
# P6
r = D('6.4') * P(3) + D('3.6') * P(4)
assert r == D('4.24') * P(4) and round(2 * pi * 42400) == 266407
assert round(266407 / 24, -2) == 11100 and round(11100000 / 3600) == 3083
assert 2 * D('3.6') * P(4) / (3 * P(5)) == D('0.24') and 2 * D('0.24') == D('0.48')
# P7
assert D('1.3') * P(9) / P(3) == D('1.3') * P(6) and D('1.3') * P(6) * 8760 == D('1.1388') * P(10)
assert round(float(D('1.1388') * P(10) / (D('4.5') * P(3))), -4) == 2530000
assert round(float(D('4.5') * P(11) / (D('1.1388') * P(10))), 1) == 39.5
assert 8 * P(-3) * 5 * 365 == D('14.6') and D('14.6') * D('0.25') == D('3.65')

print("check_ch03 : tous les contrôles passent.")
