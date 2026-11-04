# -*- coding: utf-8 -*-
"""Contrôles du chapitre 14 (Thalès, triangles emboîtés) — 4ème."""
from fractions import Fraction as F
from math import sqrt

D = lambda s: F(s)  # noqa: E731
r = lambda v, n=2: round(float(v) + 1e-12, n)  # noqa: E731


def thales(am, ab, ac, bc):
    """Renvoie (AN, MN) pour M sur [AB], N sur [AC], (MN) // (BC)."""
    k = F(am) / F(ab)
    return k * F(ac), k * F(bc)


def triangle_ok(a, b, c):
    a, b, c = sorted(map(F, (a, b, c)))
    return a + b > c


# Cours
assert thales(3, 5, 10, 8) == (6, D('4.8')) and F(6, 10) == D('4.8') / 8 == D('0.6')
assert D('1.5') * 12 / 2 == 9
# D2
assert F(5 * 3, 2) == D('7.5') and F(2, 5) * D('7.5') == 3
# D3
assert thales(3, 5, 10, 8) == (6, D('4.8')) and 10 - 6 == 4 and triangle_ok(5, 10, 8)
# D4
assert F(4, 10) == D('0.4') and thales(4, 10, 12, 15) == (D('4.8'), 6)
assert 10 + 12 + 15 == 37 and 4 + D('4.8') + 6 == D('14.8') == D('0.4') * 37 and triangle_ok(10, 12, 15)
# D5
AC5, BC5 = F(10 * 6, 4), F(10 * 5, 4)
assert AC5 == 15 and AC5 - 6 == 9 and BC5 == D('12.5') and F(6 * 5, 4) == D('7.5') and triangle_ok(10, 15, 12.5)
# D6
assert F(2, 8) == D('0.25') and thales(2, 8, 6, 9) == (D('1.5'), D('2.25')) and D('1.5') * 4 == 6
assert thales(6, 8, 6, 9) == (D('4.5'), D('6.75')) and triangle_ok(8, 6, 9)
# D7
assert F(5 * 3, 2) == D('7.5') and F(5 * 4, 2) == 10 and D('7.5') - 3 == D('4.5')
assert 2 + 3 + 4 == 9 and 5 + D('7.5') + 10 == D('22.5') == D('2.5') * 9 and triangle_ok(5, 7.5, 10)

# E1
assert F(12) * D('1.5') / 2 == 9 and 4 + D('2.25') == D('6.25') == D('2.5') ** 2
assert 12 * D('2.5') / 2 == 15 and 144 + 81 == 225
# E2
k = D('2.4') / 6
assert k == D('0.4') and 6 * 3 / D('2.4') == D('7.5') and 6 * D('3.2') / D('2.4') == 8
assert 6 - D('2.4') == D('3.6') and D('7.5') - 3 == D('4.5')
assert D('2.4') + 3 + D('3.2') == D('8.6') and 6 + D('7.5') + 8 == D('21.5') and D('0.4') * D('21.5') == D('8.6')
assert D('3.6') + 8 + D('4.5') + D('3.2') == D('19.3') and triangle_ok(6, 7.5, 8)
# E3
assert 2 + 3 == 5 and 5 + 3 == 8 and F(8 * 3, 2) == 12 and 8 * D('2.5') / 2 == 10
assert F(5 * 12, 8) == D('7.5') and F(5 * 10, 8) == D('6.25') and D('7.5') - 3 == 12 - D('7.5') == D('4.5')
assert F(2, 5) == F(3, D('7.5')) == D('2.5') / D('6.25')  # Thalès dans APQ
# E4
assert F(2 * 9, 6) == 3 and F(2 * 6, 6) == 2 and 6 - 2 == 4 and 36 - D('20.25') == D('15.75')
assert r(sqrt(15.75)) == 3.97 and r(sqrt(15.75) / 3) == 1.32 and r(2 * sqrt(15.75) / 3) == 2.65
# E5
x = 2
assert 9 * x == 3 * (x + 4) == 3 * x + 12 and F(x, x + 4) == F(3, 9) and 6 * D('2.5') / 2 == D('7.5')
assert triangle_ok(6, 9, 7.5)
# E6
assert F(3 * 8, 2) == 12 and F(3 * 8, 5) == D('4.8') and F(5) * D('4.5') / 3 == D('7.5') and D('7.5') - D('4.5') == 3
assert F(5, 3) == D('7.5') / D('4.5') == 8 / D('4.8') and F(3, 5) == D('4.5') / D('7.5') == D('4.8') / 8
# E7
assert 64 + 36 == 100 and F(2 * 6, 8) == D('1.5') and F(2 * 10, 8) == D('2.5') and 4 + D('2.25') == D('6.25')

# P1
assert F(20) * D('1.8') / 4 == 9 and 16 + D('3.24') == D('19.24') and r(sqrt(19.24)) == 4.39
assert 20 * D('1.35') / 9 == 3 and 30 * D('1.8') / 5 == D('10.8')
# P2
assert F(30 * 90, 90) == 30 and 8100 - 2025 == 6075 and r(sqrt(6075), 1) == 77.9 and r(sqrt(6075) / 3, 1) == 26.0
assert r(77.9 / 3, 2) == 25.97 and 25 * 90 == 2250
# P3
assert 12 + 36 == 48 and F(48 * 15, 12) == 60 and F(48 * 13, 12) == 52 and 52 - 13 == 39
assert 60 / D('0.5') == 120 and 48 + 52 - 60 == 40 and triangle_ok(48, 52, 60)
# P4
mn = lambda x: 12 * F(8 - x, 8)  # noqa: E731
assert 8 - 3 == 5 and mn(3) == D('7.5') and D('7.5') * 3 == D('22.5')
assert all(mn(x) == 12 - D('1.5') * x for x in range(9))
assert [mn(x) * x for x in (2, 4, 6)] == [18, 24, 18] and 12 / D('2.5') == D('4.8') and mn(D('4.8')) == D('4.8')
# P5
assert 2 * D('0.4') / D('0.5') == D('1.6') and 4 - D('0.64') == D('3.36') and r(sqrt(3.36)) == 1.83
assert D('0.8') * D('1.6') / 2 == D('0.64') and 2 * D('0.35') / D('0.5') == D('1.4')
assert D('0.5') * D('1.5') / 2 == D('0.375')
# P6
assert [d * D('0.6') / 12 for d in (3, 6, 9)] == [D('0.15'), D('0.3'), D('0.45')]
assert D('0.15') + D('0.3') + D('0.45') == D('0.9') and 144 + D('0.36') == D('144.36')
assert r(sqrt(144.36)) == 12.01 and D('0.6') / 12 == D('0.05') == D('0.15') / 3
# P7
x = 24
assert 20 * x == 15 * (x + 8) == 15 * x + 120 and F(x, x + 8) == F(15, 20) == D('0.75')
x = 12
assert 25 * x == 15 * (x + 8) and F(12, 20) == F(15, 25)

print("check_ch14 : tous les contrôles passent.")
