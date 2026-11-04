# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 2 (fractions et nombres premiers) — 4ème."""
from fractions import Fraction as F
from math import gcd, lcm
from sympy import factorint, isprime, primerange

D = lambda s: F(s)  # noqa: E731
fi = lambda n: factorint(n)  # noqa: E731

# Cours / fiche
assert isprime(97) and fi(360) == {2: 3, 3: 2, 5: 1} and fi(84) == {2: 2, 3: 1, 7: 1}
assert F(84, 60) == F(7, 5) and F(5, 6) + F(7, 15) == F(39, 30) == F(13, 10)
assert F(14, 15) * F(25, 21) == F(10, 9) and F(2, 3) / F(4, 5) == F(5, 6)
assert F(-6, 7) / F(3, 14) == -4 and F(-4, 9) * F(3, 8) == F(-1, 6)
assert F(3, 4) * 28 == 21 and F(2, 3) * F(3, 4) == F(1, 2)

# D1
assert [d for d in range(1, 13) if 12 % d == 0] == [1, 2, 3, 4, 6, 12]
assert [n for n in (1, 2, 9, 17, 21, 29, 51) if isprime(n)] == [2, 17, 29]
assert 51 == 3 * 17 and 91 == 7 * 13 and 97 == 7 * 13 + 6 and isprime(97)
# D2
assert fi(60) == {2: 2, 3: 1, 5: 1} and fi(1001) == {7: 1, 11: 1, 13: 1}
assert 1001 // 7 == 143 and 143 // 11 == 13 and 2 * 3 * 3 * 7 == 126
assert 2 * 3 * 5 * 7 + 1 == 211 and all(211 % p == 1 for p in (2, 3, 5, 7))
# D3
assert fi(90) == {2: 1, 3: 2, 5: 1} and fi(126) == {2: 1, 3: 2, 7: 1} and F(90, 126) == F(5, 7)
assert fi(150) == {2: 1, 3: 1, 5: 2} and fi(210) == {2: 1, 3: 1, 5: 1, 7: 1}
assert F(150, 210) == F(5, 7) and 90 * 210 == 126 * 150 == 18900
assert fi(1430) == {2: 1, 5: 1, 11: 1, 13: 1} and F(1001, 1430) == F(7, 10)
assert F(1001 // 11, 1430 // 11) == F(91, 130) and gcd(91, 130) == 13
# D4
assert F(1, 4) + F(2, 4) == F(3, 4) == F(1, 2) + F(1, 4) and F(1, 2) + F(1, 3) == F(5, 6)
assert F(3, 4) - F(2, 3) == F(1, 12) and 2 - F(3, 5) == F(7, 5) and F(2, 5) < F(1, 2)
# D5
assert F(2, 3) * F(3, 4) == F(6, 12) and F(14 * 25, 15 * 21) == F(350, 315) == F(10, 9)
assert F(-4, 9) * F(3, 8) == F(-1, 6) and 5 * F(7, 10) == F(7, 2)
assert F(2, 3) * 36 == 24 and F(3, 4) * 24 == 18
# D6
assert F(3, 5) * F(5, 3) == 1 and F(2, 3) / F(4, 5) == F(5, 6) and F(-6, 7) / F(3, 14) == -4
assert 5 / F(1, 4) == 20 and F(3, 8) / 6 == F(1, 16) and F(3, 4) / F(1, 8) == 6
# D7
assert F(-2, 3) + F(5, 6) == F(1, 6) and F(1, 2) - F(3, 4) * F(2, 9) == F(1, 3)
assert (F(1, 2) - F(3, 4)) * F(2, 9) == F(-1, 18)
assert F(2, 5) / F(-4, 15) == F(-3, 2) and F(2, 5) / F(-4, 15) + 1 == F(-1, 2)
assert F(5, 6) > F(7, 9) and F(5, 6) == F(15, 18) and F(7, 9) == F(14, 18)
assert sorted([F(-3, 4), F(-2, 3), F(1, 6), F(-5, 6)]) == [F(-5, 6), F(-3, 4), F(-2, 3), F(1, 6)]

# E1
assert F(1, 4) + F(1, 3) + F(1, 6) == F(3, 4)
assert [F(1, 4) * 960, F(1, 3) * 960, F(1, 6) * 960] == [240, 320, 160]
assert 960 - 720 == 240 and F(1, 3) * F(1, 4) == F(1, 12) and F(1, 12) * 960 == 80
assert F(1, 3) / F(1, 6) == 2
# E2
assert F(3, 4) * 28 == 21 and F(2, 3) * 21 == 14 and F(2, 3) * F(3, 4) == F(1, 2) == F(14, 28)
assert F(7, 28) == F(1, 4) and F(4, 7) * 7 == 4 and F(4, 7) * F(1, 4) == F(1, 7)
assert F(1, 3) * F(3, 4) == F(1, 4) and F(1, 4) * 28 == 7 == 21 - 14
# E3
pairs = [n for n in range(4, 61, 2)]
assert len(pairs) == 29
m3 = [n for n in range(6, 61, 3) if n % 2]
assert m3 == [9, 15, 21, 27, 33, 39, 45, 51, 57]
m5 = [n for n in range(10, 61, 5) if n % 2 and n % 3]
assert m5 == [25, 35, 55]
m7 = [n for n in range(14, 61, 7) if n % 2 and n % 3 and n % 5]
assert m7 == [49]
assert 1 + 29 + 9 + 3 + 1 == 43 and len(list(primerange(1, 61))) == 17 == 60 - 43
# E4
assert gcd(84, 60) == 12 and 84 // 6 == 14 and 60 // 6 == 10 and F(84, 8) == D('10.5')
assert [d for d in range(1, 13) if 12 % d == 0] == [1, 2, 3, 4, 6, 12]
# E5
assert 36 / F(3, 5) == 60 and F(1, 4) * 36 == 9 and F(27, 60) == F(9, 20)
assert F(42, 60) == F(7, 10) and F(18, 60) == F(3, 10) and 42 // 6 * 100 == 700
assert F(1, 4) * 60 == 15
# E6
assert F(7, 8) < F(11, 12) and F(-5, 6) < F(-7, 9)
assert sorted([F(2, 3), F(5, 8), F(7, 12), F(3, 4)]) == [F(7, 12), F(5, 8), F(2, 3), F(3, 4)]
assert F(2, 3) < F(17, 24) < F(3, 4)
assert 1 - F(11, 12) < 1 - F(9, 10) < 1 - F(7, 8) and F(7, 8) < F(9, 10) < F(11, 12)
# E7
assert F(1, 2) + F(1, 4) == F(3, 4) and F(1, 3) + F(1, 4) == F(7, 12)
assert F(1, 3) + F(1, 15) == F(2, 5)
assert all(F(1, n) - F(1, n + 1) == F(1, n * (n + 1)) for n in range(1, 20))
assert F(1, 2) + F(1, 6) + F(1, 12) + F(1, 20) == F(4, 5) == F(48, 60)

# P1
assert F(2, 5) + F(1, 4) + F(1, 8) == F(31, 40) and 1 - F(31, 40) == F(9, 40)
assert [F(2, 5) * 2400, F(1, 4) * 2400, F(1, 8) * 2400] == [960, 600, 300]
assert F(9, 40) * 2400 == 540 and F(2, 3) * 540 == 360 and F(2, 3) * F(9, 40) == F(3, 20)
assert F(180, 2400) == F(3, 40) and F(960, 2640) == F(4, 11) and F(4, 11) < F(2, 5)
# P2
assert 18 * 12 == 216 and F(3, 8) * 216 == 81 and F(2, 5) * F(5, 8) == F(1, 4)
assert F(1, 4) * 216 == 54 and F(2, 5) * 216 == D('86.4') and 1 - F(3, 8) - F(1, 4) == F(3, 8)
assert F(1, 3) * F(3, 8) == F(1, 8) and F(1, 8) * 216 == 27 and 27 / D('0.75') == 36
# P3
assert F(1, 2) + F(1, 3) + F(1, 9) == F(17, 18) and isprime(17)
assert [18 // 2, 18 // 3, 18 // 9] == [9, 6, 2] and 9 + 6 + 2 == 17
assert 9 - F(17, 2) == F(1, 2) and 6 - F(17, 3) == F(1, 3) and 2 - F(17, 9) == F(1, 9)
assert F(1, 18) * 17 == F(17, 18)
# P4
assert lcm(12, 18) == 36 and 3600 // 36 == 100 and lcm(36, 30) == 180
assert F(1, 12) + F(1, 18) == F(5, 36)
# P5
k = F(9, 6)
assert k == F(3, 2) and F(3, 4) * k == F(9, 8) and F(2, 5) * k == F(3, 5) and F(1, 8) * k == F(3, 16)
assert F(3, 5) * 1000 == 600 and F(3, 16) * 1000 == D('187.5')
k = F(4, 6)
assert F(3, 4) * k == F(1, 2) and F(2, 5) * k == F(4, 15) and F(1, 8) * k == F(1, 12)
assert round(4000 / 15) == 267 and round(1000 / 12) == 83
assert F(3, 4) / 6 == F(1, 8) and F(1, 2) / F(1, 8) == 4 and F(9, 8) / F(1, 2) == F(9, 4)
# P6
assert F(1, 6) + F(1, 3) == F(1, 2) and F(1, 2) - F(1, 4) == F(1, 4)
assert F(1, 6) * D('1.5') == F(1, 4) and F(3, 4) / F(1, 3) == F(9, 4)
assert D('1.5') + F(9, 4) == D('3.75')
assert 48 // 6 == 8 and 48 // 3 == 16 and 48 // 4 == 12 and 48 / (8 + 16 - 12) == 4
# P7
assert fi(420) == {2: 2, 3: 1, 5: 1, 7: 1} and fi(300) == {2: 2, 3: 1, 5: 2}
assert 420 // 20 * (300 // 20) == 315 and F(420, 25) == D('16.8') and gcd(420, 300) == 60
assert 7 * 5 == 35 and 35 * D('12.50') == D('437.50') and 315 * D('0.90') == D('283.50')
assert D('437.50') - D('283.50') == 154 and D('0.36') / D('12.6') == F(1, 35)

print("check_ch02 : tous les contrôles passent.")
