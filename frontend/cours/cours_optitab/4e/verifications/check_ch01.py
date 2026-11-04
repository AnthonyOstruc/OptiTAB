# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 1 (nombres relatifs) — 4ème."""
from fractions import Fraction as F
from sympy import symbols, expand, simplify

D = lambda s: F(s)  # noqa: E731  décimaux exacts : D('2.4')

# Cours / fiche
assert (-7) + (-5) == -12 and (-7) + 5 == -2 and 7 + (-5) == 2
assert 3 - 8 == -5 and -4 - (-9) == 5
assert (-4) * D('-2.5') == 10 and (-3) * 5 == -15
assert [k * (-3) for k in (2, 1, 0, -1, -2)] == [-6, -3, 0, 3, 6]
assert (-2) * 5 * (-3) * (-7) == -210 and (-25) * 17 * (-4) == 1700
assert F(-54, -9) == 6 and F(18, -4) == D('-4.5') and F(-35, 7) == F(35, -7) == -5
assert 6 - 2 * (-3 + 7) == -2 and (6 - 2) * (-3 + 7) == 16
assert F(24, -6) * 2 == -8 and 3 + 5 * D('-1.6') == -5 and 3 - (-7) == 10

# D1
assert sorted([-4, -7, 3]) == [-7, -4, 3] and 3 - (-7) == 10
assert -4 + 9 == 5 and -7 - 2 + 6 == -3 and -4 - 3 == -7
# D2
assert [a * (-2) for a in (3, 2, 1, 0, -1, -2, -3)] == [-6, -4, -2, 0, 2, 4, 6]
assert (-7) * (-6) == 42 and D('2.4') * (-5) == -12
assert D('-0.5') * (-12) == 6 and (-1) * 15 == -15
# D3
assert (-7) * (-4) == 28 and F(28, -4) == -7 and F(-54, -9) == 6 and 6 * (-9) == -54
assert F(18, -4) == D('-4.5') and D('-4.5') * (-4) == 18 and F(0, -12) == 0
# D4
assert 2 * 5 * 3 * 7 == 210 and (-1) ** 10 == 1
assert (-3) * 47 * D('-8.5') * 0 * (-12) == 0
# D5
assert -8 - (-3) == -5 and (-8) * (-3) == 24 and -8 - 3 == -11 and (-8) + (-3) == -11
assert F(-8, -4) == 2 and -8 * 3 - 3 == -27
# D6
assert 14 - 3 * (-2) == 20 and (14 - 3) * (-2) == -22 and -5 + 4 * (-3) == -17
assert (-5 + 4) * (-3) == 3 and F(24, -6) * 2 == -8 and F(24, (-6) * 2) == -2
# D7
assert 8 * 4 == 32 and 5 * (-3) == -15 and 32 - 15 + 2 * 0 == 17 and 8 + 5 + 2 == 15
assert 6 * 4 + 9 * (-3) == -3 and 17 - (-3) == 20
assert 6 * 4 + 9 * (-3) == -3 and 7 * 4 + 8 * (-3) == 4
assert min(b for b in range(16) if 4 * b - 3 * (15 - b) > 0) == 7

# E1
assert 4 - 9 == -5 and -3 * (-5) == 15 and F(12, -4) == -3
assert -3 * (4 - 9) + F(12, -4) == 12
assert F(-3 * 4 - 9 + 12, -4) == D('2.25')
assert -3 * (4 - 9 + F(12, -4)) == 24
# E2
assert (-25) * 17 * (-4) == 1700 and D('-0.5') * (-37) * (-2) == -37
assert 125 * (-7) * 8 == -7000 and D('-2.5') * (-13) * (-4) == -130
assert (-7) * 99 == -693 == -700 + 7 and (-48) * (-25) == 1200
# E3
assert -6 - 4 == -10 and (-3) * (-5) == 15 and F(24, -6) * 2 == -8
assert 5 - 3 * (-2) == 11 and (-2) ** 3 == -8
# E4
assert 3200 - 400 == 2800 and 2800 // 100 == 28 and 28 * D('-0.6') == D('-16.8')
assert 12 + D('-16.8') == D('-4.8')
assert (2900 - 400) // 100 == 25 and 12 + 25 * D('-0.6') == -3
assert 12 / D('0.6') == 20 and 400 + 2000 == 2400 and 20 * D('-0.6') == -12
# E5
ops = [D('-48.5'), 3 * D('-18.5'), -60, 250, -230]
assert ops[1] == D('-55.5')
s = 125
soldes = []
for o in ops:
    s += o
    soldes.append(s)
assert soldes[0] == D('76.5') and soldes[1] == 21 and soldes[2] == -39
assert soldes[3] == 211 and soldes[4] == -19
assert -19 - 125 == -144 == sum(ops)
assert D('-48.5') + D('-55.5') - 60 - 230 == -394 and -394 + 250 == -144
# E6
t = [-6, -2, 1, -4, 3, -1, -5]
assert min(t) == -6 and max(t) == 3 and 3 - (-6) == 9
assert sum(x for x in t if x < 0) == -18 and sum(t) == -14 and F(sum(t), 7) == -2
assert 8 * (-1) - sum(t) == 6 and F(sum(t) + 6, 8) == -1
# E7
x = -3
A, B, C, Dd, E = 5 * x - 7, -2 * x + 4, x * (x + 4), (2 - x) * (x - 1), x * x - 2 * x
assert (A, B, C, Dd, E) == (-22, 10, -3, -20, 15)
assert sorted([A, B, C, Dd, E]) == [-22, -20, -3, 10, 15]

# P1
assert -240 + 8 * 12 == -144 and 85 + 8 * (-5) == 45 and 45 - (-144) == 189
assert 85 - (-240) == 325 and 325 - 8 * 17 == 189
assert F(240, 12) == 20 and F(85, 5) == 17 and -240 + 17 * 12 == -36
assert 85 + 20 * (-5) == -15
assert F(325 - 121, 17) == 12 and -240 + 12 * 12 == -96 and 85 - 12 * 5 == 25
assert 25 - (-96) == 121
# P2
assert D('56.7') - D('-89.2') == D('145.9')
f = lambda c: D('1.8') * c + 32  # noqa: E731
assert f(0) == 32 and f(100) == 212
assert D('1.8') * D('-89.2') == D('-160.56') and f(D('-89.2')) == D('-128.56')
assert D('1.8') * D('56.7') == D('102.06') and f(D('56.7')) == D('134.06')
assert f(-40) == -40 and (D(-4) - 32) / D('1.8') == -20 and f(-20) == -4
assert f(D('56.7')) - f(D('-89.2')) == D('262.62') == D('1.8') * D('145.9')
# P3
a, b, c = 3, 1, -1
sq = [[a, -4, b], [-2, 0, 2], [c, 4, -3]]
sums = [sum(r) for r in sq] + [sum(sq[i][j] for i in range(3)) for j in range(3)]
sums += [sq[0][0] + sq[1][1] + sq[2][2], sq[0][2] + sq[1][1] + sq[2][0]]
assert set(sums) == {0}
sq5 = [[v + 5 for v in r] for r in sq]
assert {sum(r) for r in sq5} == {15} and 3 * (-4) * 1 == -12
# P4
base = [-2, 3, -1, 4]
e2 = [base[i] * base[i + 1] for i in range(3)]
e3 = [e2[i] * e2[i + 1] for i in range(2)]
assert e2 == [-6, -3, -4] and e3 == [18, 12] and e3[0] * e3[1] == 216
base = [-2, 3, -1, -4]
e2 = [base[i] * base[i + 1] for i in range(3)]
e3 = [e2[i] * e2[i + 1] for i in range(2)]
assert e2 == [-6, -3, 4] and e3 == [18, -12] and e3[0] * e3[1] == -216
assert F(-15, 5) == -3 and (-3) * (-2) == 6 and (-15) * 6 == -90
assert ((-1) * (-3)) * ((-3) * (-2)) == 18
# P5
prog = lambda n: F(n * (-4) + 6, -2)  # noqa: E731
assert [prog(n) for n in (5, -3, 0, D('1.5'), 7)] == [7, -9, -3, 0, 11]
assert all(prog(n) == 2 * n - 3 for n in (5, -3, 0, D('1.5'), 7, D('-2.7')))
xs = symbols('x')
assert simplify((xs * (-4) + 6) / (-2) - (2 * xs - 3)) == 0
# P6
alt = [850]
for v in (320, -150, 410, -275, -305):
    alt.append(alt[-1] + v)
assert alt == [850, 1170, 1020, 1430, 1155, 850]
assert max(alt) - 850 == 580 and 320 + 410 == 730 and -150 - 275 - 305 == -730
# P7
off = {"LA": -8, "NY": -5, "Paris": 1, "Tokyo": 9}
assert off["NY"] - off["Paris"] == -6 and 14 - 6 == 8
assert 14 + (off["Tokyo"] - off["Paris"]) == 22 and 14 + (off["LA"] - off["Paris"]) == 5
assert D('10') + D('8.5') - 6 == D('12.5')
assert 11 + (off["Paris"] - off["Tokyo"]) + 14 == 17 and 11 + 14 - 8 == 17
assert (9 + off["Tokyo"] - off["LA"]) - 24 == 2

print("check_ch01 : tous les contrôles passent.")
