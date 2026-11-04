# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 3 (Arithmétique et nombres premiers)."""
from sympy import Rational as R, isprime, factorint, divisors, gcd, ilcm

# Cours
assert 84 == 14 * 6
assert all(2340 % d == 0 for d in [2, 3, 5, 9, 10])
assert isprime(17) and not isprime(91) and 91 == 7 * 13
assert factorint(360) == {2: 3, 3: 2, 5: 1} and 8 * 9 * 5 == 360
assert R(84, 150) == R(14, 25)
assert gcd(168, 126) == 42 and 168 // 42 == 4 and 126 // 42 == 3
assert ilcm(42, 66) == 462 and divmod(462, 60) == (7, 42)

# Découverte
assert all(2340 % d == 0 for d in [2, 3, 5, 9, 10])                      # D1
assert 2340 == 9 * 260 == 10 * 234                                       # D1
assert [n for n in [1, 2, 17, 21, 49] if isprime(n)] == [2, 17]          # D2
assert 21 == 3 * 7 and 49 == 7 ** 2                                      # D2
assert factorint(420) == {2: 2, 3: 1, 5: 1, 7: 1} and 4 * 3 * 5 * 7 == 420  # D3
assert factorint(198) == {2: 1, 3: 2, 11: 1}                             # D4
assert factorint(252) == {2: 2, 3: 2, 7: 1}                              # D4
assert R(198, 252) == R(11, 14)                                          # D4
assert [n for n in range(70, 131) if n % 14 == 0] == [70, 84, 98, 112, 126]  # D5
assert 714 % 2 == 0 and 714 % 3 == 0 and 714 == 6 * 119                  # D6
assert 1062 % 9 == 0 and 1062 == 9 * 118 and 1062 % 5 != 0               # D6
assert 12 % 3 == 0 and 12 % 9 != 0                                       # D6
assert factorint(180) == {2: 2, 3: 2, 5: 1}                              # D7
assert factorint(360) == {2: 3, 3: 2, 5: 1} and 8 * 9 * 5 == 360         # D7

# Entraînement
assert divisors(72) == [1, 2, 3, 4, 6, 8, 9, 12, 18, 24, 36, 72]         # E1
assert 72 % 5 != 0 and 72 % 7 != 0                                       # E1
assert [a for a in range(10) if (450 + a) % 2 == 0] == [0, 2, 4, 6, 8]   # E2
assert [a for a in range(10) if (9 + a) % 3 == 0] == [0, 3, 6, 9]        # E2
assert [a for a in range(10) if (450 + a) % 6 == 0] == [0, 6]            # E2
assert 450 == 6 * 75 and 456 == 6 * 76                                   # E2
assert R(2 ** 4 * 3 ** 2 * 7, 2 ** 2 * 3 ** 3 * 5) == R(28, 15)          # E3
assert gcd(28, 15) == 1                                                  # E3
assert 2 ** 4 * 3 ** 3 * 3 == 36 ** 2 == 1296                            # E4
assert 84 % 20 != 0                                                      # E5
assert [d for d in range(1, 21) if 84 % d == 0] == [1, 2, 3, 4, 6, 7, 12, 14]  # E5
assert divisors(84) == [1, 2, 3, 4, 6, 7, 12, 14, 21, 28, 42, 84]        # E5
assert factorint(84) == {2: 2, 3: 1, 7: 1} and factorint(126) == {2: 1, 3: 2, 7: 1}  # E6
assert gcd(84, 126) == 42 and R(84, 126) == R(2, 3)                      # E6
assert factorint(12) == {2: 2, 3: 1} and factorint(18) == {2: 1, 3: 2}   # E7
assert ilcm(12, 18) == 36 and 36 == 12 * 3 == 18 * 2 and 24 % 18 != 0    # E7

# Problèmes
assert factorint(156) == {2: 2, 3: 1, 13: 1} and factorint(204) == {2: 2, 3: 1, 17: 1}  # P1
assert gcd(156, 204) == 12 and 156 // 12 == 13 and 204 // 12 == 17       # P1
assert gcd(13, 17) == 1                                                  # P1
assert factorint(42) == {2: 1, 3: 1, 7: 1} and factorint(66) == {2: 1, 3: 1, 11: 1}  # P2
assert ilcm(42, 66) == 462 and 462 == 7 * 60 + 42                        # P2
assert factorint(180) == {2: 2, 3: 2, 5: 1} and factorint(252) == {2: 2, 3: 2, 7: 1}  # P3
assert gcd(180, 252) == 36 and 180 // 36 == 5 and 252 // 36 == 7         # P3
assert 35 * 36 ** 2 == 180 * 252 == 45360                                # P3
assert ilcm(8, 9, 15) == 360                                             # P4
assert not [n for n in range(500, 601) if n % 8 == n % 9 == n % 15 == 0] # P4
assert factorint(24) == {2: 3, 3: 1} and factorint(40) == {2: 3, 5: 1}   # P5
assert ilcm(24, 40) == 120 and 120 // 24 == 5 and 120 // 40 == 3         # P5
assert factorint(54) == {2: 1, 3: 3} and factorint(72) == {2: 3, 3: 2}   # P6
assert ilcm(54, 72) == 216 == 8 * 27 and 216 == 3 * 60 + 36              # P6
assert 216 // 54 == 4 and 216 // 72 == 3                                 # P6
assert gcd(3, 8) == 1 and 3 * 8 == 24                                    # P7
assert [n for n in range(100, 151) if n % 24 == 0] == [120, 144]         # P7
assert 120 % 5 == 0 and 144 % 5 != 0                                     # P7
assert 144 == 3 * 48 == 8 * 18 and (1 + 4 + 4) % 3 == 0                  # P7

# Questions ajoutées (standard : exercices complets, >= 5 questions)
assert (7 + 3 + 1) % 3 != 0 and 731 % 3 != 0                             # D1 Q4
assert 1485 % 5 == 0 and 1485 % 9 == 0                                   # D1 Q5
assert 1485 == 5 * 297 == 9 * 165                                        # D1 Q5
assert not isprime(51) and 51 == 3 * 17                                  # D2 Q4
assert isprime(43) and 43 % 2 and 43 % 3 and 43 % 5                      # D2 Q5
assert factorint(126) == {2: 1, 3: 2, 7: 1}                              # D3 Q5
assert R(11, 14) == R(198, 252) and gcd(11, 14) == 1                     # D4 Q4
assert factorint(90) == {2: 1, 3: 2, 5: 1} and R(90, 126) == R(5, 7)     # D4 Q5
assert [n for n in range(110, 221) if n % 25 == 0] == [125, 150, 175, 200]  # D5 Q4
assert 180 % 14 == 12 and 14 * 12 == 168 and 14 * 13 == 182              # D5 Q5
assert 9 % 3 == 0                                                        # D6 Q5
assert factorint(90) == {2: 1, 3: 2, 5: 1}                               # D7 Q4
assert factorint(900) == {2: 2, 3: 2, 5: 2} and 900 == 30 ** 2           # D7 Q5
assert divisors(54) == [1, 2, 3, 6, 9, 18, 27, 54]                       # E1 Q5
assert sorted(set(divisors(72)) & set(divisors(54))) == [1, 2, 3, 6, 9, 18]  # E1 Q5
assert gcd(72, 54) == 18                                                 # E1 Q5
assert [a for a in range(10) if (9 + a) % 9 == 0] == [0, 9]              # E2 Q4
assert 450 == 9 * 50 and 459 == 9 * 51                                   # E2 Q4
assert [a for a in range(10) if (450 + a) % 5 == 0 and (9 + a) % 3 == 0] == [0]  # E2 Q5
assert R(2 ** 3 * 5 ** 2, 2 * 5 ** 4) == R(4, 25)                        # E3 Q4
assert 2 ** 2 * 3 ** 2 * 7 ** 2 == 1764 == 42 ** 2                       # E4 Q4
assert factorint(50) == {2: 1, 5: 2} and 50 * 2 == 100 == 10 ** 2        # E4 Q5
assert 84 % 9 == 3 and 84 == 9 * 9 + 3                                   # E5 Q4
assert [d for d in divisors(84) if d > 20] == [21, 28, 42, 84]           # E5 Q5
assert ilcm(84, 126) == 252 == 2 ** 2 * 3 ** 2 * 7                       # E6 Q4
assert 42 * 252 == 84 * 126 == 10584                                     # E6 Q5
assert 36 + 36 == 72                                                     # E7 Q4 (10 h 12)
assert [k * 36 for k in range(6)] == [0, 36, 72, 108, 144, 180]          # E7 Q5 (6 départs)
assert 156 == 6 * 26 and 204 == 6 * 34                                   # P1 Q5
assert 1800 % 462 != 0                                                   # P2 Q4
assert [k for k in range(1, 9) if 462 * k <= 3600] == [1, 2, 3, 4, 5, 6, 7]  # P2 Q5
assert divisors(36) == [1, 2, 3, 4, 6, 9, 12, 18, 36]                    # P3 Q5
assert 180 // 18 == 10 and 252 // 18 == 14 and 10 * 14 == 140            # P3 Q5
assert 360 * 2 == 720 and 700 <= 720 <= 750 and 720 // 8 == 90           # P4 Q3-4
assert 240 == 2 * 120 and 240 // 24 == 10 and 240 // 40 == 6             # P5 Q4
assert ilcm(30, 40) == 120 and 120 // 30 == 4                            # P5 Q5
assert 2 * 216 == 432 and 432 == 7 * 60 + 12                             # P6 Q4
assert 8 * 216 == 1728 <= 1800 < 1944 == 9 * 216                         # P6 Q5
assert [n for n in range(150, 201) if n % 24 == 0] == [168, 192]         # P7 Q5
assert 168 % 5 != 0 and 192 % 5 != 0                                     # P7 Q5

print("check_ch03 : tous les contrôles passent.")
