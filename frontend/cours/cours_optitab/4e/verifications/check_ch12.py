# -*- coding: utf-8 -*-
"""Contrôles du chapitre 12 (triangles) — 4ème. Les « mesures » sont recalculées par trigonométrie."""
from math import cos, sin, radians, sqrt, degrees, acos, atan

r = lambda v, n=1: round(v + 1e-12, n)  # noqa: E731
ok_tri = lambda a, b, c: max(a, b, c) < a + b + c - max(a, b, c)  # noqa: E731

# D1
assert not ok_tri(3, 4, 8) and ok_tri(4, 5, 6) and 5 + 7 == 12 and ok_tri(2.5, 3.5, 5)
assert [c for c in range(1, 20) if ok_tri(6, 9, c)] == list(range(4, 15)) and len(range(4, 15)) == 11
# D2
assert ok_tri(6, 5, 4) and 6 + 5 + 4 == 15
# D3
assert 180 - 52 - 71 == 57 and (180 - 40) / 2 == 70 and 180 - 90 - 35 == 55 and 180 / 6 == 30
# D5
angA = degrees(acos((25 + 36 - 49) / 60))
angB = degrees(acos((25 + 49 - 36) / 70))
assert round(angA) == 78 and round(angB) == 57 and 180 - 78 - 57 == 45 and 5 + 6 + 7 == 18
# D6 (CAC) : BC
assert r(sqrt(25 + 16 - 40 * cos(radians(50)))) == 3.9
# D7 (ACA)
AB = 6 * sin(radians(60)) / sin(radians(80))
AC = 6 * sin(radians(40)) / sin(radians(80))
assert 180 - 40 - 60 == 80 and r(AB) == 5.3 and r(AC) == 3.9

# E1
assert 110 + 70 + 110 + 70 == 360 and 2 * (7 + 4) == 22
# E2
assert (180 - 40) / 2 == 70 and 40 / 2 == 20
# E3
assert 110 / 2 == 55 and 360 - 110 - 100 - 100 == 50 and 50 / 2 == 25 and 55 + 100 + 25 == 180
# E5
assert ok_tri(4, 6, 5) and 45 + 75 < 180 and 180 - 45 - 75 == 60 and 120 + 70 > 180
# E6
assert (180 - 35) / 2 == 72.5 and r(2 * 7 * sin(radians(17.5))) == 4.2 and (180 - 60) / 2 == 60
# E7
assert 70 + 80 + 40 == 190 and not ok_tri(3, 3, 7) and ok_tri(5, 12, 13)
assert [x for x in range(1, 10) if ok_tri(2, 3, x)] == [2, 3, 4]

# P1
assert 40 == 40
# P2
assert (360 - 70 - 70) / 2 == 110 and 70 / 2 == 35 and 35 + 110 + 35 == 180
# P3
DF = sqrt(2 ** 2 + 4 ** 2 - 2 * 2 * 4 * cos(radians(60)))
assert r(DF) == 3.5 and r(3 * DF) == 10.4
# P4
assert 390 + 280 == 670 and 390 - 280 == 110 and not ok_tri(12, 7, 20) and ok_tri(8, 6, 10)
assert 8 + 6 - 10 == 4 and 4 / 10 == 0.4 and 3 + 2 < 8
# P5 (SSA) : t^2 - 12 t cos40 + 36 - AC^2 = 0
def racines(ac):
    b = -12 * cos(radians(40))
    c = 36 - ac ** 2
    d = b * b - 4 * c
    if d < 0:
        return []
    return [x for x in ((-b - sqrt(d)) / 2, (-b + sqrt(d)) / 2) if x > 0]


assert [r(t) for t in racines(4.5)] == [2.3, 6.9] and racines(3) == [] and len(racines(7)) == 1
assert r(6 * sin(radians(40))) == 3.9
# P6
assert 50 / 2 == 25 and 80 * 25 / 2 == 1000 and 2 * 2 * 1000 / 10000 == 0.4
# P7
assert round(degrees(atan(3 / 4))) == 37 and 180 - 2 * 37 == 106 and (180 - 106) / 2 == 37

print("check_ch12 : tous les contrôles passent.")
