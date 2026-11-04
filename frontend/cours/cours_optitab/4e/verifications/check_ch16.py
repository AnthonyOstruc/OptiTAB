# -*- coding: utf-8 -*-
"""Contrôles du chapitre 16 (translations, agrandissements et réductions) — 4ème."""
from fractions import Fraction as F
from math import sqrt, pi, acos, degrees, ceil

D = lambda s: F(s)  # noqa: E731
r = lambda v, n=2: round(float(v) + 1e-12, n)  # noqa: E731
t = lambda p, v: (p[0] + v[0], p[1] + v[1])  # noqa: E731


def aire_poly(pts):
    s = 0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


# D1 (translation de la figure a : décalage (1, 2) -> (6, 3))
assert (6 - 1, 3 - 2) == (5, 1)
# D2
v = (3, 2)
assert t((1, 1), v) == (4, 3) and t((2, 4), v) == (5, 6) and t((-2, 3), v) == (1, 5) and t((-1, -2), v) == (2, 0)
assert t((-2, -1), v) == (1, 1) and r(sqrt(13), 1) == 3.6
# D3
assert aire_poly([(0, 0), (4, 0), (1, 3)]) == 6 == aire_poly([(5, 2), (9, 2), (6, 5)])
# D4
assert 5 + 3 + 5 + 3 == 16 and 2 * 5 == 10
# D5
assert (3 * 2, 2 * 2) == (6, 4) and 2 * (3 + 2) == 10 and 2 * (6 + 4) == 20 and 3 * 2 == 6 and 6 * 4 == 24 == 4 * 6
assert F(3, 6) == D('0.5') and D('7.5') / 3 == D('2.5') and 2 * D('2.5') == 5
# D6
assert [x * D('0.5') for x in (10, 8, 6)] == [5, 4, 3] and 25 == 16 + 9 and 10 + 8 + 6 == 24 and 5 + 4 + 3 == 12
assert D('7.5') / 10 == D('0.75') and 8 * D('0.75') == 6 and 6 * D('0.75') == D('4.5') and 10 / D('7.5') == F(4, 3)
# D7
assert 4 * D('1.5') == 6

# E1
assert 3 * 3 == 9 and 24 // 3 == 8 and 7 * 3 == 21 and 100 / D('2.5') == 40
# E2
v = (5, -2)
assert (3 - (-2), -1 - 1) == v and t((1, 3), v) == (6, 1) and t((0, 0), v) == (5, -2) and t((-4, 3), v) == (1, 1)
assert t((6, 1), (-5, 2)) == (1, 3) and r(sqrt(29)) == 5.39
# E3
assert 4 ** 2 + 3 ** 2 == 5 ** 2 and 4 * 3 / 2 == 6
# E4
assert 9 * 50 == 450 and 7 * 50 == 350 and D('1.8') * 50 == 90 and D('4.5') * D('3.5') == D('15.75')
assert 200 / 50 == 4 and 160 / F(50) == D('3.2') and F(1, 50) == D('0.02') and 9 * 7 == 63
# E5
assert F(20, 10) == F(30, 15) == 2 and F(50, 10) == 5 and 15 * 5 == 75 and F(13, 10) != F(18, 15)
assert 15 * D('1.3') == D('19.5') and F(6, 10) == D('0.6') and 15 * D('0.6') == 9 and F(15, 10) == F(30, 20)
# E6
assert 430 / F(43) == 10 and 172 / F(43) == 4 and D('3.5') * 43 == D('150.5') and D('64.5') / 43 == D('1.5')
assert D('8.6') / 430 == F(1, 50)
# E7
assert r(degrees(acos(27 / 48))) == 55.77 and round(degrees(acos((16 + 36 - 25) / 48))) == 56
assert [x * D('1.5') for x in (4, 6, 5)] == [6, 9, D('7.5')] and 15 * D('1.5') == D('22.5')
assert F(30, 15) == 2 and F(4, 6) == F(2, 3)

# P1
assert aire_poly([(0, 0), (3, 0), (4, 2), (1, 2)]) == 6 and 96 // 6 == 16 and (3 + 1, 0 + 2) == (4, 2)
# P2
assert t((1, 1), (3, 2)) == (4, 3) and t((4, 3), (2, -4)) == (6, -1) and t((1, 1), (2, -4)) == (3, -3)
assert t((3, -3), (3, 2)) == (6, -1)
d1, d2, dd = sqrt(13), sqrt(20), sqrt(29)
assert r(d1) == 3.61 and r(d2) == 4.47 and r(d1 + d2) == 8.08 and r(dd) == 5.39 and r(d1 + d2 - dd) == 2.69
# P3
L0 = [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)]
L1 = [(x * 1.5, y * 1.5) for x, y in L0]
L2 = [(x * 2, y * 2) for x, y in L0]
assert aire_poly(L0) == 12 and aire_poly(L1) == 27 and aire_poly(L2) == 48 and 27 / 12 == 2.25 == 1.5 * 1.5
assert 4 + 2 + 2 + 2 + 2 + 4 == 16 and 6 + 3 + 3 + 3 + 3 + 6 == 24
# P4
assert 15 * 200 == 3000 and 8 * 200 == 1600 and 2 * 200 == 400 and 2 * (30 + 16) == 92 and 46 * 200 == 9200
assert r(pi * 4) == 12.57 and r(480 - pi * 4, 1) == 467.4 and round((480 - pi * 4) * 35) == 16360
assert ceil((480 - pi * 4) * 35 / 5000) == 4
# P5
assert 33000 / 1000 == 33 and 12500 / 1000 == 12.5 and F(D('16.5'), 33000) == F(1, 2000) and 11500 / 2000 == 5.75
assert F(165, 330) == D('0.5') and 16500 / D('16.5') == 1000 and F(1, 2) / F(1, 2000) == 1000
# P6
assert D('29.7') / 2 == D('14.85') and r(14.85 / 21, 3) == 0.707 and r(21 / 29.7, 3) == 0.707
assert r(29.7 / 21, 3) == 1.414 and r(42 / 29.7, 3) == 1.414 and r(0.707 * 1.414, 4) == 0.9997
assert D('14.85') * 21 == D('311.85') and 21 * D('29.7') == D('623.7') and D('29.7') * 42 == D('1247.4')
assert D('311.85') * 2 == D('623.7') and D('623.7') * 2 == D('1247.4')
# P7
assert F(200 * 10, 50) == 40 and F(40, 10) == F(200, 50) == 4 and 6 * 4 == 24 and F(200, 10) == 20
assert F(300 * 10, 50) == 60

print("check_ch16 : tous les contrôles passent.")
