# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 10 (Statistiques)."""
from sympy import Rational as R


def med(v):
    v = sorted(v)
    n = len(v)
    return v[n // 2] if n % 2 else R(v[n // 2 - 1] + v[n // 2], 2)


def moy(v):
    return R(sum(v), len(v))


notes = [6] * 2 + [8] * 3 + [10] * 6 + [12] * 5 + [16] * 4

# Cours
assert R(12, 30) == R('0.4')
assert len(notes) == 20 and sum(notes) == 220 and moy(notes) == 11
assert moy([2, 3, 3, 8]) == 4 and med([2, 3, 3, 8]) == 3 and 8 - 2 == 6

# Découverte
s = [2, 4, 4, 5, 7, 8]
assert len(s) == 6 and s.count(4) == 2 and R(2, 6) == R(1, 3)            # D1
assert R(3, 6) == R(1, 2) and sum(R(s.count(v), 6) for v in set(s)) == 1  # D1
assert 30 - 12 - 9 == 9 and R(12, 30) == R('0.4') and R(9, 30) == R('0.3')  # D2
assert moy([7, 9, 10, 14]) == 10 and moy([12, 15, 8, 11, 9]) == 11       # D3
assert moy([-3, 5, 0, 2]) == 1 and moy([9, 11, 12, 16]) == 12            # D3
assert sorted([13, 4, 9, 7, 11]) == [4, 7, 9, 11, 13] and med([13, 4, 9, 7, 11]) == 9  # D4
assert med([1, 3, 6, 8, 10, 20]) == 7 and moy([1, 3, 6, 8, 10, 20]) == 8  # D4
t = [-3, 2, 5, -1, 8, 0, 3]
assert max(t) - min(t) == 11 and moy(t) == 2 and med(t) == 2             # D5
assert 2 + 3 + 6 + 5 + 4 == 20 and 5 + 4 == 9 and R(9, 20) == R('0.45')  # D6
assert med(notes) == 10 and max(notes) - min(notes) == 10                # D7

# Entraînement
assert R(360, 40) == 9 and [a * 9 for a in [10, 18, 12]] == [90, 162, 108]  # E1
assert R(18, 40) == R('0.45') and 360 * R('0.45') == 162                  # E1
assert sum([4, 8, 6, 2]) == 20                                           # E2
assert R(5 * 4 + 15 * 8 + 25 * 6 + 35 * 2, 20) == 18                     # E2
assert 4 * 3 + 7 * 5 + 12 * 2 == 71 and R(71, 10) == R('7.1')            # E3
assert abs(R(4 + 7 + 12, 3) - R('7.67')) < R('0.01')                     # E3
assert 12 * 13 == 156 and 18 * 11 == 198 and R(156 + 198, 30) == R('11.8')  # E4
assert 4 * R('12.5') - 34 == 16 and 52 - 34 == 18 and 60 - 34 == 26      # E5
A, B = [9, 10, 10, 11], [2, 10, 10, 18]
assert moy(A) == moy(B) == 10 and med(A) == med(B) == 10                 # E6
assert max(A) - min(A) == 2 and max(B) - min(B) == 16                    # E6
sal = [1800, 1900, 2000, 2100, 2200]
assert moy(sal) == 2000 and med(sal) == 2000                             # E7
assert abs(moy(sal + [9000]) - 3167) < 1 and med(sal + [9000]) == 2050   # E7

# Problèmes
assert 9 * 14 == 126 and R(126 + 24, 10) == 15 and R(126 + 14, 10) == 14  # P1
assert med([14] * 9 + [24]) == 14 and med([13] * 8 + [22] + [24]) == 13  # P1
assert 8 * 13 + 22 == 126                                                # P1
assert R(84 - 80, 80) == R(5, 100) and R(84 - 78, 80 - 78) == 3          # P2
cA = [8, 9, 10, 11, 11, 12, 13, 14, 15]
cB = [4, 6, 9, 12, 13, 14, 16, 17, 19, 20]
assert sum(cA) == 103 and abs(moy(cA) - R('11.4')) < R('0.05') and moy(cB) == 13  # P3
assert med(cA) == 11 and med(cB) == R('13.5')                            # P3
assert max(cA) - min(cA) == 7 and max(cB) - min(cB) == 16                # P3
assert len([v for v in cA if v >= 12]) == 4 and len([v for v in cB if v >= 12]) == 7  # P3
pl = [62, 55, 48, 51, 66, 38, 22, 30, 54, 70, 78, 72]
assert sum(pl) == 646 and abs(moy(pl) - R('53.8')) < R('0.05')           # P4
assert med(pl) == R('54.5') and max(pl) - min(pl) == 56                  # P4
assert len([v for v in pl if v > 60]) == 5                               # P4
assert 4 * 11 == 44 and 6 * 12 == 72 and 72 - 44 == 28 and 28 - 13 == 15  # P5
assert 6 * 14 - 44 == 40                                                 # P5
assert 200 - 30 - 70 - 60 == 40                                          # P6
assert [R(e, 200) * 100 for e in [30, 70, 60, 40]] == [15, 35, 30, 20]   # P6
assert [e * R('1.8') for e in [30, 70, 60, 40]] == [54, 126, 108, 72]    # P6
jA, jB = [12, 14, 15, 13, 16, 14], [5, 25, 8, 22, 6, 24]
assert moy(jA) == 14 and moy(jB) == 15 and med(jA) == 14 and med(jB) == 15  # P7
assert max(jA) - min(jA) == 4 and max(jB) - min(jB) == 20                # P7

print("check_ch10 : tous les contrôles passent.")
