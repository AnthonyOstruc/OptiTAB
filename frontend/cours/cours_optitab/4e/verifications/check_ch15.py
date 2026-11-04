# -*- coding: utf-8 -*-
"""Contrôles du chapitre 15 (cosinus dans le triangle rectangle) — 4ème."""
from math import cos, acos, radians, degrees, sqrt

c = lambda a: cos(radians(a))  # noqa: E731
ac = lambda x: degrees(acos(x))  # noqa: E731
r = lambda v, n=2: round(v + 1e-12, n)  # noqa: E731

# Cours
assert r(c(35), 3) == 0.819 and r(ac(0.6), 1) == 53.1 and r(10 * c(35), 1) == 8.2 and r(6 / c(50), 1) == 9.3
assert round(ac(4 / 7)) == 55 and r(5 * c(70)) == 1.71 and r(sqrt(25 - (5 * c(70)) ** 2)) == 4.70
# D2
assert round(ac(0.8)) == 37 and round(ac(0.6)) == 53 and 37 + 53 == 90
# D3
AB = 10 * c(35)
assert r(AB, 1) == 8.2 and r(100 - AB ** 2, 1) == 32.9 and r(sqrt(100 - AB ** 2), 1) == 5.7
assert r(c(55), 3) == 0.574 == r(sqrt(100 - AB ** 2) / 10, 3)
# D4
BC = 6 / c(50)
assert r(BC, 3) == 9.334 and r(BC, 1) == 9.3 and r(BC ** 2, 2) == 87.13 and r(BC ** 2 - 36, 2) == 51.13
assert r(sqrt(BC ** 2 - 36), 1) == 7.2 and r(sqrt(9.3 ** 2 - 36), 1) == 7.1
# D5
assert r(ac(4 / 7)) == 55.15 and round(90 - ac(4 / 7)) == 35 and r(sqrt(33)) == 5.74
assert r(sqrt(33) / 7, 3) == 0.821 and r(ac(sqrt(33) / 7)) == 34.85
# D6
assert c(60) - 0.5 < 1e-12
assert [r(c(a), 3) for a in (20, 30, 45, 70, 89)] == [0.940, 0.866, 0.707, 0.342, 0.017]
assert c(25) > c(65) and r(ac(0.9), 1) == 25.8
# D7
assert 4 / 5 == 8 / 10 == 0.8 and r(2 * c(30), 3) == 1.732 and r(ac(0.5)) == 60

# E1
assert r(5 * c(70), 3) == 1.710 and r(25 - (5 * c(70)) ** 2) == 22.08 and r(ac(0.4), 1) == 66.4
assert r(ac(0.2), 1) == 78.5 and r(5 * c(65)) == 2.11 and r(5 * c(75)) == 1.29
# E2
MH = 50 * c(40)
assert r(MH) == 38.30 and r(MH ** 2, 1) == 1467.1 and r(2500 - MH ** 2, 1) == 1032.9 and r(sqrt(2500 - MH ** 2), 1) == 32.1
assert r(50 * c(60)) == 25 and r(ac(40 / 80)) == 60
# E3
assert r(ac(0.6)) == 53.13 and r(180 - 2 * ac(0.6), 1) == 73.7 and r(10 * c(70), 3) == 3.420 and r(20 * c(70)) == 6.84
# E4
assert r(ac(0.8)) == 36.87 and r(90 - ac(0.8), 1) == 53.1 and r(180 - 2 * ac(0.8), 1) == 106.3
d = sqrt(21 ** 2 + 29.7 ** 2)
assert r(21 ** 2 + 29.7 ** 2) == 1323.09 and r(d) == 36.37 and r(29.7 / d, 4) == 0.8165 and r(ac(29.7 / d), 1) == 35.3
# E5
BH = 10 * c(40)
AH2 = 100 - BH ** 2
HC = sqrt(64 - AH2)
assert r(BH) == 7.66 and r(AH2) == 41.32 and r(sqrt(AH2)) == 6.43 and r(64 - AH2) == 22.68 and r(HC) == 4.76
assert r(HC, 3) == 4.763 and r(HC / 8, 3) == 0.595 and r(ac(HC / 8), 1) == 53.5 and r(BH + HC, 1) == 12.4
assert r(180 - 40 - 53.5, 1) == 86.5 and r(180 - 40 - ac(HC / 8), 1) == 86.5
# E6
assert r(ac(5 / 13)) == 67.38 and r(acos(5 / 13), 3) == 1.176 and r(ac(12 / 13)) == 22.62 and 5 ** 2 + 12 ** 2 == 13 ** 2
# E7
ah = sqrt(49 - 3.5 ** 2)
assert r(7 * c(60), 6) == 3.5 and r(ah) == 6.06 and r(9 * ah / 2) == 27.28 and r(5.5 ** 2 + 36.75) == 67
assert r(sqrt(67)) == 8.19 and r(5.5 / sqrt(67), 3) == 0.672 and r(ac(5.5 / sqrt(67)), 1) == 47.8

# P1
DH = 1200 * c(25)
assert r(DH, 1) == 1087.6 and round(DH) == 1088 and round(DH ** 2) == 1182807 and round(1200 ** 2 - DH ** 2) == 257193
assert round(sqrt(1200 ** 2 - DH ** 2)) == 507 and 1350 + 507 == 1857 and 1200 / 5 == 240
assert 1500 ** 2 + 600 ** 2 == 2610000 and round(sqrt(2610000)) == 1616 and r(1500 / sqrt(2610000), 4) == 0.9285
assert r(ac(1500 / sqrt(2610000)), 1) == 21.8
# P2
OH = 3000 * c(15)
OK = 2000 / c(15)
assert r(OH, 1) == 2897.8 and round(9e6 - OH ** 2) == 602886 and round(sqrt(9e6 - OH ** 2)) == 776
assert r(OK, 1) == 2070.6 and round(OK) == 2071 and round(OK ** 2 - 4e6) == 287187 and round(sqrt(OK ** 2 - 4e6)) == 536
assert r(sqrt(OK ** 2 - 4e6), 1) == 535.9 and r(sqrt(2071 ** 2 - 4e6), 1) == 537.6 and 536 - 300 == 236
assert round(sqrt(15e6)) == 3873 and r(3873 / 4000, 3) == 0.968 and r(ac(sqrt(15e6) / 4000), 1) == 14.5
# P3
assert r(4.5 / 5.5, 3) == 0.818 and r(ac(4.5 / 5.5), 1) == 35.1 and 5.5 ** 2 - 4.5 ** 2 == 10 and r(sqrt(10)) == 3.16
L = 5 / c(30)
assert r(L, 3) == 5.774 and r(L) == 5.77 and r(L ** 2) == 33.33 and r(L ** 2 - 25) == 8.33 and r(sqrt(L ** 2 - 25)) == 2.89
assert r(24 * L) == 138.56 and r(240 * L, 1) == 1385.6
# P4
OHb = 12 * c(40)
HP = sqrt(144 - OHb ** 2)
OQ = sqrt(OHb ** 2 + (HP + 5) ** 2)
assert r(OHb, 3) == 9.193 and r(144 - OHb ** 2) == 59.50 and r(HP) == 7.71 and r(HP + 5) == 12.71
assert r(OHb ** 2) == 84.50 and r((HP + 5) ** 2) == 161.63 and r(OQ ** 2) == 246.13 and r(OQ, 1) == 15.7
assert r(OQ, 3) == 15.689 and r(OHb / OQ, 3) == 0.586 and r(ac(OHb / OQ), 1) == 54.1
assert r(OQ / 20, 3) == 0.784 and round(OQ / 20 * 60) == 47
# P5
assert r(1.2 * c(30), 3) == 1.039 and r(1.2 * c(30)) == 1.04 and r(1.2 - 1.2 * c(30), 3) == 0.161
assert r((1.2 * c(30)) ** 2, 6) == 1.08 and r(sqrt(1.44 - 1.08), 6) == 0.6 and r(1.2 * c(60), 6) == 0.6 and r(ac(0.75), 1) == 41.4
# P6
AO = 6 * c(35)
OD = sqrt(36 - AO ** 2)
assert r(AO) == 4.91 and r(2 * AO, 3) == 9.830 and r(36 - AO ** 2) == 11.84 and r(OD) == 3.44
assert r(2 * OD, 3) == 6.883 and r(2 * AO * 2 * OD / 2) == 33.83 and 2 * (90 - 35) == 110
# P7
assert 225 - 36 == 189 and r(sqrt(189)) == 13.75 and r(sqrt(189) / 15, 4) == 0.9165 and r(ac(sqrt(189) / 15), 1) == 23.6
assert 15 / 0.5 == 30 and r(12 / c(30), 3) == 13.856 and r(12 / c(30)) == 13.86
assert r((12 / c(30)) ** 2, 6) == 192 and r(sqrt(48)) == 6.93

print("check_ch15 : tous les contrôles passent.")
