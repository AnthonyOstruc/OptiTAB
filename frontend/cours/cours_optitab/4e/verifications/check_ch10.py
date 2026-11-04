# -*- coding: utf-8 -*-
"""Contrôles du chapitre 10 (statistiques) — 4ème."""
from fractions import Fraction as F
from statistics import median
mean = lambda xs: sum(F(x) for x in xs) / len(xs)  # noqa: E731

D = lambda s: F(s)  # noqa: E731
r = lambda v, n=2: round(float(v) + 1e-12, n)  # noqa: E731


def serie(vals, effs):
    out = []
    for v, e in zip(vals, effs):
        out += [v] * e
    return out


# Cours
assert F(9, 25) == D('0.36') and D('0.4') * 360 == 144
assert F(14 * 4 + 12 * 3 + 15 * 2 + 18, 10) == 14
assert median([5, 7, 9, 9, 11, 12, 15]) == 9 and median([5, 7, 9, 9, 11, 12, 15, 20]) == 10
assert mean([5, 7, 9, 9, 11, 12, 15, 20]) == 11 and mean([5, 7, 9, 9, 11, 12, 15, 100]) == 21

# D1
eff = [8, 5, 4, 6, 2]
assert sum(eff) == 25 and [F(e, 25) * 100 for e in eff] == [32, 20, 16, 24, 8]
assert r(7 / 30 * 100, 1) == 23.3 and r(8 / 30 * 100, 1) == 26.7
# D2
fr = serie([0, 1, 2, 3, 4], [4, 9, 7, 3, 2])
assert len(fr) == 25 and F(4, 25) == D('0.16') and F(12, 25) == D('0.48') and sum(fr) == 40 and mean(fr) == D('1.6')
# D3
n = [12, 15, 8, 17, 13]
assert mean(n) == 13 and r(74 / 6) == 12.33 and 14 * 6 - 65 == 19 and 16 * 6 - 65 == 31
assert max(n) - min(n) == 9 and median(n) == 13
# D5
assert mean([14, 12, 15, 18]) == D('14.75') and F(40 + 36 + 30 + 18, 10) == D('12.4') and F(66, 4) == D('16.5')
# D6
assert [D(p) * 360 for p in ('0.30', '0.15', '0.40', '0.15')] == [108, 54, 144, 54]
assert [D(p) * 240 for p in ('0.30', '0.15', '0.40', '0.15')] == [72, 36, 96, 36]
# D7
pt = serie([36, 37, 38, 39, 40], [3, 5, 8, 6, 3])
assert sum(pt) == 951 and mean(pt) == D('38.04') and median(pt) == 38 and F(9, 25) == D('0.36')

# E1
A, B = [12, 14, 15, 13, 16, 14, 14], [6, 10, 18, 22, 20, 12, 10]
assert mean(A) == mean(B) == 14 and max(A) - min(A) == 4 and max(B) - min(B) == 16
assert median(A) == 14 and median(B) == 12
# E2
no = serie([6, 8, 10, 12, 14, 16, 18], [2, 3, 5, 6, 4, 3, 2])
assert len(no) == 25 and sum(no) == 298 and mean(no) == D('11.92') and median(no) == 12
assert F(sum(1 for x in no if x >= 10), 25) == D('0.8') and mean([x + 1 for x in no]) == D('12.92')
# E3
gl = [45, 52, 38, 61, 70, 84, 57]
assert sum(gl) == 407 and r(407 / 7) == 58.14 and median(gl) == 57 and max(gl) - min(gl) == 46
assert r(141 / 407 * 100, 1) == 34.6 and 60 * 7 - 407 == 13
# E4
assert D('12.5') * 24 == 300 and D('11.5') * 26 == 299 and F(599, 50) == D('11.98') and r(317 / 27) == 11.74
# E5
sal = serie([1500, 1800, 2100, 2600, 8000], [4, 2, 1, 1, 1])
assert sum(sal) == 22300 and r(22300 / 9) == 2477.78 and median(sal) == 1800
assert sum(1 for s in sal if s < 22300 / 9) == 7 and r(7 / 9 * 100, 1) == 77.8
s8 = sal[:-1]
assert mean(s8) == D('1787.5') and median(s8) == 1650 and 8000 - 1500 == 6500 and 2600 - 1500 == 1100
# E6
assert 11 * 5 - (8 + 11 + 14 + 9) == 13 and median([8, 11, 13, 14, 9]) == 11 and 12 * 6 - 55 == 17
assert median([8, 11, 13, 14, 9, 17]) == 12
# E7
ec = [12, 25, 30, 18, 15]
cen = [D('0.5'), D('1.5'), D('2.5'), D('3.5'), D('4.5')]
assert sum(ec) == 100 and 18 + 15 == 33 and 12 + 25 == 37 and sum(c * e for c, e in zip(cen, ec)) == 249
assert r(0.49 * 60, 1) == 29.4

# P1
ca = [D(x) for x in ('12.1', '12.4', '12.0', '12.3', '12.2', '12.2')]
cb = [D(x) for x in ('11.8', '12.9', '11.7', '12.6', '11.9', '12.3')]
assert sum(ca) == sum(cb) == D('73.2') and mean(ca) == mean(cb) == D('12.2')
assert max(ca) - min(ca) == D('0.4') and max(cb) - min(cb) == D('1.2')
assert median(ca) == D('12.2') and median(cb) == D('12.1')
assert sum(1 for t in ca if t < D('12.2')) == 2 and sum(1 for t in cb if t < D('12.2')) == 3
# P2
assert [F(v, 200) * 100 for v in (86, 48, 36, 30)] == [43, 24, 18, 15]
assert [F(v, 200) * 360 for v in (86, 48, 36, 30)] == [D('154.8'), D('86.4'), D('64.8'), 54]
assert D('0.43') * 15000 == 6450
# P3
assert mean([11, 9, 13, 10]) == D('10.75') and 11 + 18 + 13 + 20 == 62 and r(62 / 6) == 10.33
assert F(108 - 62, 3) == F(46, 3) and r(46 / 3) == 15.33 and r(108.5 / 9) == 12.06 and r(122 / 9) == 13.56
# P4
assert r(4 / 102 * 100, 1) == 3.9 and (106 - 100) / (102 - 100) == 3
# P5
pl = [52, 45, 48, 55, 68, 50, 35, 30, 55, 70, 80, 65]
assert sum(pl) == 653 and r(653 / 12) == 54.42 and median(pl) == D('53.5') and max(pl) - min(pl) == 50
assert sum(1 for p in pl if p > 653 / 12) == 6
assert pl[11] + pl[0] + pl[1] == 162 and pl[5] + pl[6] + pl[7] == 115 and r(205 / 653 * 100, 1) == 31.4
# P6
ta = [24, 25, 26, 25, 25, 24, 26, 25, 25, 25]
tb = [18, 19, 35, 20, 18, 40, 19, 18, 21, 22]
assert mean(ta) == 25 and mean(tb) == 23 and max(ta) - min(ta) == 2 and max(tb) - min(tb) == 22
assert median(ta) == 25 and median(tb) == D('19.5') and sum(1 for t in tb if t > 30) == 2
# P7
ag = serie([12, 13, 14, 15, 16, 17], [5, 8, 10, 7, 6, 4])
assert sum(ag) == 573 and r(573 / 40) == 14.33 and median(ag) == 14 and F(13, 40) == D('0.325')
ag2 = ag + [18] * 5
assert sum(ag2) == 663 and r(663 / 45) == 14.73 and median(ag2) == 14 and max(ag2) - min(ag2) == 6

print("check_ch10 : tous les contrôles passent.")
