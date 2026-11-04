# -*- coding: utf-8 -*-
"""Contrôles du chapitre 9 (graphiques) — 4ème : valeurs lues = valeurs des données des figures."""
from fractions import Fraction as F
from math import exp, log
import numpy as np

D = lambda s: F(s)  # noqa: E731
r = lambda v, n=2: round(float(v) + 1e-12, n)  # noqa: E731


def lin(pts, x):
    xs, ys = zip(*pts)
    return float(np.interp(x, xs, ys))


TEMP = [(0, 4), (3, 2), (6, 1), (9, 6), (12, 12), (15, 14), (18, 10), (21, 7), (24, 5)]
assert lin(TEMP, 9) == 6 and max(t for _, t in TEMP) == 14 and min(t for _, t in TEMP) == 1
assert lin(TEMP, 11) == 10 and lin(TEMP, 18) == 10 and 14 - 1 == 13
# D2
assert [4 * c for c in range(1, 6)] == [4, 8, 12, 16, 20] and [c * c for c in range(1, 6)] == [1, 4, 9, 16, 25]
assert 4 * D('2.5') == 10 and D('2.5') ** 2 == D('6.25')
# D3
PL = [2, 3, 5, 8, 12, 15, 17, 18, 18.5]
assert [PL[i + 1] - PL[i] for i in range(8)] == [1, 2, 3, 4, 3, 2, 1, 0.5] and PL[-1] - PL[0] == 16.5
# D4
assert F(30, 10) == 3 and 38 - 30 == 8 and 25 - 12 == 13 and 40 - 28 == 12 and F(30, 12) == D('2.5')
# D5
taxi = lambda d: D('2.5') + D('1.2') * d  # noqa: E731
assert [taxi(d) for d in (0, 5, 10, 15, 20)] == [D('2.5'), D('8.5'), D('14.5'), D('20.5'), D('26.5')]
assert taxi(12) == D('16.9') and taxi(7) == D('10.9') and taxi(5) / 5 != taxi(10) / 10
# D6
assert 800 - 200 * 4 == 0 and 25 * 4 == 100 and 20 * 2 - 5 * 4 == 20
# D7
VIT = [(0, 0), (10, 50), (40, 50), (50, 0), (60, 0)]
assert lin(VIT, 5) == 25 and lin(VIT, 45) == 25 and round(50 / 3.6 * 30) == 417

# E1
assert 800 / 80 == 10 and r(1.71 * 800 ** (1 / 3)) == 15.87 and 15 * 80 == 1200 and r(1.71 * 1600 ** (1 / 3), 1) == 20.0
# E2
assert 4 * 50 == 200 and F(200, 40) == 5 and 4 * 100 == 400 == 5 * (100 - 20)
assert F(600, 4) == 150 and 20 + 600 // 5 == 140 and 600 - 4 * 140 == 40
# E3
POP = dict([(1950, 8000), (1960, 9500), (1970, 12000), (1980, 15500), (1990, 17000), (2000, 16500),
            (2010, 18000), (2020, 21000)])
ans = sorted(POP)
inc = [POP[ans[i + 1]] - POP[ans[i]] for i in range(7)]
assert inc == [1500, 2500, 3500, 1500, -500, 1500, 3000] and F(21000 - 8000, 8000) == D('1.625')
assert (12000 + 15500) // 2 == 13750
# E4
assert [x * (10 - x) for x in range(1, 10)] == [9, 16, 21, 24, 25, 24, 21, 16, 9]
# E5
assert (3 * 2, 10 + 2) == (6, 12) and (3 * 8, 10 + 8) == (24, 18) and 3 * 5 == 10 + 5 == 15
assert r(20 / 3) == 6.67 and round((20 / 3 - 6) * 60) == 40
# E6
h = lambda t: -5 * t * t + 20 * t  # noqa: E731
assert h(1) == 15 and h(2) == 20 and h(3) == 15 and h(4) == 0 and h(2.5) == 18.75
# E7
BB = [3.4, 4.5, 5.6, 6.4, 7.0, 7.5, 7.9, 8.3, 8.6, 8.9, 9.2, 9.4, 9.6]
assert BB[3] < 6.8 < BB[4] and r(BB[3] - BB[0], 1) == 3.0 and r(BB[12] - BB[9], 1) == 0.7
assert r((BB[12] - BB[0]) / 12) == 0.52

# P1
LEA = [(0, 0), (15, 4), (25, 4), (45, 9), (60, 9), (90, 0)]
assert F(4, F(1, 4)) == 16 and F(5, F(1, 3)) == 15 and F(9, F(1, 2)) == 18 and F(18, D('1.5')) == 12
assert lin(LEA, 33) == 6 and lin(LEA, 70) == 6
# P2
assert F(30, 3) == 10 and F(30, D('1.25')) == 24 and r(30 * (16.5 / 16.5) ** 0.5) == 30
# P3
T = lambda t: 20 + 180 * exp(-(t - 40) / 22.0)  # noqa: E731
assert F(180, 10) == 18 and round(T(60)) in (92, 93) and round(T(40) - T(50)) == 66
assert round(T(60) - T(70)) == 26 and round(40 + 22 * log(180 / 80)) == 58
# P4
assert [x * (40 - 2 * x) for x in range(2, 20, 2)] == [72, 128, 168, 192, 200, 192, 168, 128, 72]
assert 5 * (40 - 10) == 150 and r(40 / 3 * (40 - 80 / 3)) < 200
# P5
assert 200 + 5 * 30 == 350 and 9 * 30 == 270 and 9 * 80 - (200 + 5 * 80) == 120 and 9 * 50 == 200 + 5 * 50 == 450
assert 4 * 125 - 200 == 300
# P6
assert 220 - 14 == 206 and r(180 / 206, 3) == 0.874 and D('0.6') * 206 == D('123.6') and D('0.75') * 206 == D('154.5')
assert F(180 - 90, 10) == 9
# P7
hb = lambda x: -D('0.2') * x * x + D('1.6') * x + 2  # noqa: E731
assert hb(0) == 2 and hb(1) == D('3.4') and hb(4) == D('5.2') and hb(7) == D('3.4')
assert hb(D('7.25')) == D('3.0875') and hb(9) == D('0.2') and hb(D('9.1')) == D('-0.002')
assert D('7.25') ** 2 == D('52.5625')

print("check_ch09 : tous les contrôles passent.")
