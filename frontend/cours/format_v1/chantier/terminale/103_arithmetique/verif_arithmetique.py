# -*- coding: utf-8 -*-
"""Vérification de tous les résultats numériques de la notion « Arithmétique » (cours, fiche, exercices, figures).

    python verif_arithmetique.py      -> « TOUT EST JUSTE (n contrôles) » ou AssertionError
"""
from math import gcd, isqrt
from sympy import factorint, divisors, isprime, mod_inverse

N = 0


def ok(cond, msg=""):
    global N
    N += 1
    assert cond, msg


def lcm(a, b):
    return a * b // gcd(a, b)


def euclide(a, b):
    lignes = []
    while b:
        lignes.append((a, b, a // b, a % b))
        a, b = b, a % b
    return lignes


def sols_cong(a, b, n):
    return [x for x in range(n) if (a * x - b) % n == 0]


def sols_div(f, g, borne=500):
    """Entiers naturels n tels que g(n) divise f(n) (g(n) non nul)."""
    return [n for n in range(borne) if g(n) != 0 and f(n) % g(n) == 0]


# ------------------------------------------------------------------ cours
ok(42 == (-7) * (-6))
ok(sorted(divisors(12)) == [1, 2, 3, 4, 6, 12])
ok(sols_div(lambda n: n + 5, lambda n: n + 1) == [0, 1, 3])
ok(divisors(90) == [1, 2, 3, 5, 6, 9, 10, 15, 18, 30, 45, 90] and abs(90 ** 0.5 - 9.49) < 0.01)
ok(742 == 16 * 46 + 6 and -17 == 4 * (-5) + 3 and (-17 // 4, -17 % 4) == (-5, 3))
ok(17 % 5 == 2 and 11 % 7 == 4 and -3 % 7 == 4 and 11 == 7 * 1 + 4 and -3 == 7 * (-1) + 4)
ok([pow(3, k, 7) for k in range(1, 7)] == [3, 2, 6, 4, 5, 1] and 100 == 6 * 16 + 4 and pow(3, 100, 7) == 4)
ok([n * n % 4 for n in range(4)] == [0, 1, 0, 1] and 2027 % 4 == 3)
ok(all((a * a + b * b) % 4 != 3 for a in range(40) for b in range(40)))
ok(7 + 3 + 2 + 6 == 18 and 7326 == 9 * 814 and 1 - 3 + 3 - 1 == 0 and 1331 == 11 * 121)
ok(euclide(252, 198) == [(252, 198, 1, 54), (198, 54, 3, 36), (54, 36, 1, 18), (36, 18, 2, 0)] and gcd(252, 198) == 18)
ok([d for d in divisors(252) if 198 % d == 0] == [1, 2, 3, 6, 9, 18])
ok(gcd(15, 28) == 1 and gcd(12, 18) == 6)
ok(252 * 4 + 198 * (-5) == 18 and 1008 - 990 == 18)


def bezout(a, b):
    r0, r1, u0, u1, v0, v1 = a, b, 1, 0, 0, 1
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    return r0, u0, v0


ok(bezout(252, 198) == (18, 4, -5))
ok(12 % 6 == 0 and 4 % 6 != 0 and 3 % 6 != 0 and gcd(6, 4) == 2)
ok(all(n * (n + 1) * (n + 2) % 6 == 0 for n in range(-50, 50)))
ok(3 * (-2) % 7 == 1 and -2 % 7 == 5 and 3 * 5 == 2 * 7 + 1)
ok(sols_cong(3, 2, 7) == [3] and sols_cong(6, 4, 10) == [4, 9] and sols_cong(6, 5, 9) == [] and gcd(6, 9) == 3)
ok(sols_cong(3, 2, 5) == [4] and 3 * 2 % 5 == 1)
ok(3 * (-1) + 5 * 2 == 7 and all(3 * (-1 + 5 * k) + 5 * (2 - 3 * k) == 7 for k in range(-20, 20)))
ok({(x, y) for x in range(-30, 30) for y in range(-30, 30) if 3 * x + 5 * y == 7}
   == {(-1 + 5 * k, 2 - 3 * k) for k in range(-20, 20) if -30 <= -1 + 5 * k < 30 and -30 <= 2 - 3 * k < 30})
ok(gcd(12, 18) == 6 and (12 // 6, 18 // 6, 30 // 6) == (2, 3, 5))
ok(isprime(211) and abs(211 ** 0.5 - 14.5) < 0.05 and [211 % p for p in (2, 3, 5, 7, 11, 13)] == [1, 1, 1, 1, 2, 3])
ok(2 * 3 * 5 * 7 * 11 * 13 + 1 == 30031 == 59 * 509 and isprime(59) and isprime(509))
ok(len([p for p in range(101) if isprime(p)]) == 25 and 11 ** 2 > 100)
ok(factorint(360) == {2: 3, 3: 2, 5: 1} and 360 == 2 * 180 and 180 == 2 * 90 and 90 == 2 * 45 and 45 == 3 * 15 and 15 == 3 * 5)
ok(len(divisors(360)) == 24 == 4 * 3 * 2 and factorint(84) == {2: 2, 3: 1, 7: 1})
ok(gcd(360, 84) == 12 and lcm(360, 84) == 2520 and 12 * 2520 == 360 * 84 == 30240)
ok(pow(2, 12, 13) == 1 and 100 == 12 * 8 + 4 and pow(2, 100, 13) == 3 and 16 % 13 == 3)
ok(pow(2, 340, 341) == 1 and 341 == 11 * 31)
ok((7 * 4 + 3) % 26 == 5 and 7 * 15 == 105 == 4 * 26 + 1 and 15 * (5 - 3) % 26 == 4)
for x in range(26):
    ok((15 * (((7 * x + 3) % 26) - 3)) % 26 == x)
for p in (5, 7, 11, 13, 17):
    for a in range(1, 60):
        ok(pow(a, p, p) == a % p)
        if a % p:
            ok(pow(a, p - 1, p) == 1)

# ------------------------------------------------------------------ fiche
ok(-17 == 4 * (-5) + 3 and 2 % 6 == 8 % 6 and 1 % 6 != 4 % 6)

# ------------------------------------------------------------------ exercices
# 1156
ok([x % 6 for x in (18, 47, 89, 124, 203)] == [0, 5, 5, 4, 5])
ok([x % 9 for x in (27, 64, 91, 145)] == [0, 1, 1, 1] and 145 == 9 * 16 + 1)
ok([x % 11 for x in (33, 78, 156, 234)] == [0, 1, 2, 3] and 234 == 11 * 21 + 3 and 156 == 11 * 14 + 2)
ok([3 * N * N + 2 * N + 1 for N in range(6)] == [1, 6, 17, 34, 57, 86])
ok([(3 * N * N + 2 * N + 1) % 6 for N in range(6)] == [1, 0, 5, 4, 3, 2])
ok([4 * N - 3 for N in range(8)] == [-3, 1, 5, 9, 13, 17, 21, 25] and [(4 * N - 3) % 8 for N in range(8)] == [5, 1] * 4)
ok([N ** 3 - N + 2 for N in range(5)] == [2, 2, 8, 26, 62] and [(N ** 3 - N + 2) % 5 for N in range(5)] == [2, 2, 3, 1, 2])
# 1145
ok(17 - 2 == 15 and 23 == 5 * 4 + 3 and (7 + 9) % 5 == 1 and 63 == 5 * 12 + 3 and 7 * 9 % 5 == 3)
# 1143
ok(84 == 60 * 1 + 24 and 84 == 5 * 16 + 4 and 84 == 8 * 10 + 4 and 84 == 9 * 9 + 3 and 60 == 7 * 8 + 4)
ok(divisors(84) == [1, 2, 3, 4, 6, 7, 12, 14, 21, 28, 42, 84] and divisors(60) == [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60])
ok([d for d in divisors(84) if 60 % d == 0] == [1, 2, 3, 4, 6, 12])
# 1144 (réécrit le 2026-11-02 : diviseurs communs et carrelage au lieu du PPCM)
ok(euclide(84, 60) == [(84, 60, 1, 24), (60, 24, 2, 12), (24, 12, 2, 0)] and gcd(84, 60) == 12)
ok(divisors(12) == [1, 2, 3, 4, 6, 12] == [d for d in divisors(84) if 60 % d == 0] and 84 == 12 * 7 and 60 == 12 * 5)
ok(max(c for c in range(1, 85) if 84 % c == 0 and 60 % c == 0) == 12 and (84 // 12) * (60 // 12) == 35)
ok(84 * 60 == 5040 == 35 * 12 ** 2 and 12 ** 2 == 144)
# 1155 (DS)
ok(euclide(252, 180) == [(252, 180, 1, 72), (180, 72, 2, 36), (72, 36, 2, 0)] and 252 * (-2) + 180 * 3 == 36)
ok(2024 == 6 * 337 + 2 and pow(3, 2024, 7) == 2)
ok(euclide(13, 5)[:3] == [(13, 5, 2, 3), (5, 3, 1, 2), (3, 2, 1, 1)] and 13 * 2 - 5 * 5 == 1 and 5 * 8 == 40 == 3 * 13 + 1)
ok(sols_cong(5, 7, 13) == [4] and 56 % 13 == 4)
ok(gcd(12, 30) == 6 and sols_cong(12, 18, 30) == [4, 9, 14, 19, 24, 29] and sols_cong(2, 3, 5) == [4])
ok(factorint(2024) == {2: 3, 11: 1, 23: 1} and 253 == 11 * 23 and len(divisors(2024)) == 16)
ok(all((p * p - 1) % 24 == 0 for p in range(5, 2000) if isprime(p)))
ok(all(x * x % 8 == 1 for x in (1, 3, 5, 7)))
ok(all((7 ** (2 * n) + 2 * 7 ** n - 3) % 6 == 0 for n in range(40)))
ok(all(7 ** (2 * n + 2) + 2 * 7 ** (n + 1) - 3 == 6 * (8 * 7 ** (2 * n) + 2 * 7 ** n) + 7 ** (2 * n) + 2 * 7 ** n - 3 for n in range(20)))
ok(8 * 2 + 15 * (-1) == 1 and {(x, y) for x in range(-60, 60) for y in range(-60, 60) if 8 * x + 15 * y == 1}
   == {(2 + 15 * k, -1 - 8 * k) for k in range(-10, 10) if -60 <= 2 + 15 * k < 60 and -60 <= -1 - 8 * k < 60})
ok([x for x in range(105) if x % 3 == 1 and x % 5 == 2 and x % 7 == 4] == [67])
ok(67 == 3 * 22 + 1 == 5 * 13 + 2 == 7 * 9 + 4 and [x for x in range(15) if x % 3 == 1 and x % 5 == 2] == [7])
# 1147
ok(pow(2, 100, 7) == 2 and 100 == 3 * 33 + 1 and sols_cong(5, 3, 11) == [5] and 45 == 4 * 11 + 1)
ok(sols_cong(6, 9, 15) == [4, 9, 14] and all((n ** 3 - n) % 6 == 0 for n in range(-100, 100)))
# 1150 (réponses corrigées : diviseurs négatifs)
ok(sols_div(lambda n: n * n + 5, lambda n: n - 4) == [1, 3, 5, 7, 11, 25])
ok([n * n + 5 for n in (1, 3, 5, 7, 11, 25)] == [6, 14, 30, 54, 126, 630])
ok(sols_div(lambda n: n * n - 7, lambda n: n - 4) == [1, 3, 5, 7, 13])
ok([n * n - 7 for n in (1, 3, 5, 7, 13)] == [-6, 2, 18, 42, 162])
ok(sols_div(lambda n: n * n + 2, lambda n: n + 3) == [8] and 66 == 11 * 6)
ok(sols_div(lambda n: n * n + 3 * n - 10, lambda n: n - 5) == [0, 2, 3, 4, 6, 7, 8, 10, 11, 15, 20, 35])
ok(all(n * n + 3 * n - 10 == (n - 5) * (n + 8) + 30 for n in range(-20, 20)) and 35 ** 2 + 105 - 10 == 1320 == 30 * 44)
# 1157
ok(all((4 * n ** 3 + 2 * n) % 6 == 0 for n in range(200)) and [4 * r ** 3 + 2 * r for r in range(3)] == [0, 6, 36])
ok([r ** 4 for r in range(1, 5)] == [1, 16, 81, 256] and all(pow(n, 4, 5) == 1 for n in range(200) if n % 5))
# 1157 Q3 (remplacée le 2026-11-02) : 30 divise n^5 - n
ok(all(n ** 5 - n == (n - 1) * n * (n + 1) * (n * n + 1) for n in range(-50, 50)))
ok(all((n ** 5 - n) % 30 == 0 for n in range(500)) and 2 ** 5 - 2 == 30 and 3 ** 5 - 3 == 240 == 30 * 8)
ok(12 % 4 == 0 and 12 % 6 == 0 and 12 % 24 != 0)
# 1148
ok(euclide(84, 30) == [(84, 30, 2, 24), (30, 24, 1, 6), (24, 6, 4, 0)] and 84 * (-1) + 30 * 3 == 6)
ok(euclide(252, 105) == [(252, 105, 2, 42), (105, 42, 2, 21), (42, 21, 2, 0)] and 252 * (-2) + 105 * 5 == 21)
# Q3 (remplacée le 2026-11-02) : 84x + 30y = 18 et = 20
ok(84 * (-3) + 30 * 9 == 18 == 6 * 3 and -252 + 270 == 18 and 20 == 6 * 3 + 2)
ok(not any(84 * x + 30 * y == 20 for x in range(-100, 100) for y in range(-300, 300)))
ok(euclide(28, 15)[:3] == [(28, 15, 1, 13), (15, 13, 1, 2), (13, 2, 6, 1)] and 28 * 7 + 15 * (-13) == 1 and 225 == 28 * 8 + 1)
ok(mod_inverse(15, 28) == 15 and mod_inverse(7, 26) == 15 and 26 * 3 + 7 * (-11) == 1 and 105 == 26 * 4 + 1)
ok(euclide(26, 7)[:3] == [(26, 7, 3, 5), (7, 5, 1, 2), (5, 2, 2, 1)])
ok(euclide(1071, 462) == [(1071, 462, 2, 147), (462, 147, 3, 21), (147, 21, 7, 0)] and 1071 * (-3) + 462 * 7 == 21)
ok(-3213 + 3234 == 21 and 1071 // 21 == 51 and 462 // 21 == 22 and 1071 * 22 == 462 * 51)
# 1149
ok(isprime(97) and [97 % p for p in (2, 3, 5, 7)] == [1, 1, 2, 6] and 97 == 7 * 13 + 6)
ok(factorint(2023) == {7: 1, 17: 2} and 2023 == 7 * 289 and divisors(2023) == [1, 7, 17, 119, 289, 2023])
ok(44 ** 2 == 1936 and 45 ** 2 == 2025 and isqrt(2023) ** 2 != 2023)
# 1152
ok(all(gcd(4 * n + 1, 6 * n + 1) == 1 and gcd(7 * n + 3, 5 * n + 2) == 1 for n in range(500)))
ok(all(3 * (4 * n + 1) - 2 * (6 * n + 1) == 1 and 5 * (7 * n + 3) - 7 * (5 * n + 2) == 1 for n in range(50)))
ok([(4 * n + 1, 6 * n + 1, 7 * n + 3, 5 * n + 2) for n in range(3)] == [(1, 1, 3, 2), (5, 7, 10, 7), (9, 13, 17, 12)])
# 1159
ok(all((4 ** (2 * n + 1) + 3 ** (n + 2)) % 13 == 0 for n in range(60)) and 16 % 13 == 3)
ok(all(4 ** (2 * n + 3) + 3 ** (n + 3) == 13 * 4 ** (2 * n + 1) + 3 * (4 ** (2 * n + 1) + 3 ** (n + 2)) for n in range(20)))
# 1151
ok(all((3 ** (2 * n) + 4 * 3 ** n - 5) % 8 == 0 for n in range(1, 60)) and 9 + 12 - 5 == 16)
ok(3 ** 8 + 4 * 3 ** 4 - 5 == 6880 == 8 * 860 and 3 ** 10 + 4 * 3 ** 5 - 5 == 60016 == 8 * 7502)
ok(all(3 ** (2 * n + 2) + 4 * 3 ** (n + 1) - 5 == 8 * (3 ** (2 * n) + 3 ** n) + 3 ** (2 * n) + 4 * 3 ** n - 5 for n in range(20)))
# 1153 (réécrit le 2026-11-02 : chiffrement affine, clé y = 5x + 8 mod 26)
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
chif = lambda mot, a, b: "".join(ALPHA[(a * ALPHA.index(c) + b) % 26] for c in mot)
ok(chif("MATHS", 5, 8) == "QIZRU")
ok([5 * ALPHA.index(c) + 8 for c in "MATHS"] == [68, 8, 103, 43, 98] and [(5 * ALPHA.index(c) + 8) % 26 for c in "MATHS"] == [16, 8, 25, 17, 20])
ok(68 == 26 * 2 + 16 and 103 == 26 * 3 + 25 and 43 == 26 + 17 and 98 == 26 * 3 + 20)
ok(5 * 21 == 105 == 26 * 4 + 1 and mod_inverse(5, 26) == 21 and -168 == 26 * (-7) + 14 and 70 == 26 * 2 + 18)
ok(all(((5 * x + 8) % 26 == y) == ((21 * y + 14) % 26 == x) for x in range(26) for y in range(26)))
ok(chif("NPIJA", 21, 14) == "BRAVO" and chif("BRAVO", 5, 8) == "NPIJA")
ok([21 * ALPHA.index(c) + 14 for c in "NPIJA"] == [287, 329, 182, 203, 14] and 287 == 26 * 11 + 1 and 329 == 26 * 12 + 17 and 182 == 26 * 7 and 203 == 26 * 7 + 21)
ok(chif("A", 13, 8) == chif("C", 13, 8) == "I" and 34 == 26 + 8 and gcd(13, 26) == 13)
ok(all(len({(a * x + 8) % 26 for x in range(26)}) == 26 for a in range(26) if gcd(a, 26) == 1)
   and all(len({(a * x + 8) % 26 for x in range(26)}) < 26 for a in range(26) if gcd(a, 26) != 1))
ok(chif("E", 7, 3) == "F" and (15 * (5 - 3)) % 26 == 4)  # schéma du cours
# 1160
ok(sols_cong(5, 8, 12) == [4] and 25 % 12 == 1 and 5 * 5 - 12 * 2 == 1)
ok(sols_cong(6, 4, 10) == [4, 9] and sols_cong(3, 2, 5) == [4] and sols_cong(4, 12, 16) == [3, 7, 11, 15])
ok(sols_cong(3, 2, 10) == [4] and 3 * 9 % 10 != 2)
# 1158
ok(15 % 13 == 2 and pow(2, 12, 13) == 1 and 256 == 13 * 19 + 9 and pow(15, 20, 13) == 9)
ok(64 == 13 * 5 - 1 and pow(8, 15, 13) == 5 and pow(25, 18, 13) == 1)
ok([pow(7, k, 10) for k in range(1, 5)] == [7, 9, 3, 1] and 2025 == 4 * 506 + 1 and pow(7, 2025, 10) == 7)
ok(pow(3, 1234, 8) == 1 and 1234 == 2 * 617)
# 1146 (réécrit le 2026-11-02 : PGCD, Bézout, équation 504x + 420y = 168)
ok(factorint(504) == {2: 3, 3: 2, 7: 1} and factorint(420) == {2: 2, 3: 1, 5: 1, 7: 1} and 2 ** 2 * 3 * 7 == 84 == gcd(504, 420))
ok(504 == 2 * 252 and 252 == 2 * 126 and 126 == 2 * 63 and 63 == 9 * 7 and 420 == 2 * 210 and 210 == 2 * 105 and 105 == 3 * 35)
ok(euclide(504, 420) == [(504, 420, 1, 84), (420, 84, 5, 0)] and 504 * 1 + 420 * (-1) == 84)
ok(504 == 84 * 6 and 420 == 84 * 5 and 168 == 84 * 2 and 504 * 2 + 420 * (-2) == 168 and 6 * 2 + 5 * (-2) == 2)
S = {(x, y) for x in range(-60, 60) for y in range(-80, 80) if 504 * x + 420 * y == 168}
ok(S == {(2 + 5 * k, -2 - 6 * k) for k in range(-30, 30) if -60 <= 2 + 5 * k < 60 and -80 <= -2 - 6 * k < 80})
ok({(-3, 4), (2, -2), (7, -8)} <= S)  # points de la figure ex1146_droite
ok(100 == 84 * 1 + 16 and not any(504 * x + 420 * y == 100 for x in range(-50, 50) for y in range(-60, 60)))
# 1161
ok([pow(3, k, 10) for k in range(1, 7)] == [3, 9, 7, 1, 3, 9] and [3 ** k for k in range(1, 7)] == [3, 9, 27, 81, 243, 729])
ok(87 == 4 * 21 + 3 and pow(3, 87, 10) == 7)
ok([pow(7, r, 11) for r in range(10)] == [1, 7, 5, 2, 3, 10, 4, 6, 9, 8] and 456 == 10 * 45 + 6 and pow(7, 456, 11) == 4)
# 1154
ok(isprime(17) and isprime(23) and 17 * 23 == 391 and 16 * 22 == 352 and gcd(16, 22) == 2)
ok(352 == 3 * 117 + 1 and gcd(3, 352) == 1 and mod_inverse(3, 352) == 235 and 3 * 235 == 705 == 2 * 352 + 1)
ok(10000 == 391 * 25 + 225 and 22500 == 391 * 57 + 213 and pow(100, 3, 391) == 213 and pow(213, 235, 391) == 100)

# ------------------------------------------------------------------ figures
ok([pow(3, k, 10) for k in range(4)] == [1, 3, 9, 7] and [pow(7, k, 10) for k in range(4)] == [1, 7, 9, 3])
ok(198 + 54 == 252 and 3 * 54 + 36 == 198 and 36 + 18 == 54 and 2 * 18 == 36)  # pavage du rectangle
# figures de la finition 2026-11-02
ok(all(n % 5 == k for k, liste in enumerate([[0, 5, 10, 15, 20], [1, 6, 11, 16], [2, 7, 12, 17], [3, 8, 13, 18, 23], [4, 9, 14, 19]]) for n in liste))
ok(84 == 60 * 1 + 24 and 0 <= 24 < 60)  # ex1143_division
ok(60 + 24 == 84 and 2 * 24 + 12 == 60 and 2 * 12 == 24)  # ex1144_euclide : largeur, bande de droite, dernière bande
ok([pow(2, k, 7) for k in range(4)] == [1, 2, 4, 1])  # ex1147_cycle
ok(euclide(84, 30) == [(84, 30, 2, 24), (30, 24, 1, 6), (24, 6, 4, 0)])  # ex1148_euclide
ok(2023 == 7 * 289 and 289 == 17 * 17)  # ex1149_arbre
ok(pow(100, 3, 391) == 213 and pow(213, 235, 391) == 100)  # ex1154_rsa

print(f"TOUT EST JUSTE ({N} contrôles)")
