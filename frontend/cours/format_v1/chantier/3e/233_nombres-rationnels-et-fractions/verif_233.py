# -*- coding: utf-8 -*-
"""Vérification des résultats de la notion 233 (nombres rationnels et fractions, 3e)."""
from fractions import Fraction as F
from decimal import Decimal as D, ROUND_HALF_UP
from sympy import factorint

ok = 0


def chk(c, msg):
    global ok
    assert c, msg
    ok += 1


# ---------- cours / fiche
chk(F(5, 8) == F(25, 40) and F(42, 63) == F(2, 3), "fractions égales")
chk(factorint(84) == {2: 2, 3: 1, 7: 1} and factorint(120) == {2: 3, 3: 1, 5: 1} and F(84, 120) == F(7, 10), "84/120")
chk(F(3, 4) - F(5, 6) == F(-1, 12), "3/4-5/6")
chk(F(1, 2) + F(1, 3) == F(5, 6), "1/2+1/3")
chk(F(2, 3) / F(5, 7) == F(14, 15), "2/3 : 5/7")
chk(F(-9, 14) * F(7, 15) == F(-3, 10), "-9/14*7/15")
chk(F(6 + 3, 3) == 3, "(6+3)/3")
chk(F(2, 3) - F(1, 4) * F(8, 3) == 0, "priorités cours")
chk(F(3, 5) * 40 == 24 and F(1, 3) * F(3, 5) == F(1, 5), "fraction de")
chk(F(2, 3) < F(3, 4) and F(-5, 6) < F(-3, 4), "comparaisons")
chk(D(9) / D(7) > D("1.285") and (D(9) / D(7)).quantize(D("0.01"), ROUND_HALF_UP) == D("1.29"), "9/7")
chk(F(3, 4) == F(75, 100), "0,75")

# ---------- 2181
chk(1 - F(3, 8) == F(5, 8) and F(9, 12) == F(3, 4), "2181")
# ---------- 2098
chk(sorted([F(2, 4), F(3, 4), F(5, 4), F(6, 4), F(7, 4)]) == [F(1, 2), F(3, 4), F(5, 4), F(3, 2), F(7, 4)], "2098 ordre")
chk(F(7, 4) == 1 + F(3, 4), "2098 Q4")
# ---------- 2099
chk(F(3, 4) == F(6, 8) == F(9, 12) and F(54, 72) == F(3, 4) and F(7, 9) == F(35, 45), "2099")
# ---------- 2100
for a, b, r in [(36, 48, F(3, 4)), (-45, 60, F(-3, 4)), (84, 70, F(6, 5)), (125, 100, F(5, 4)), (17, 51, F(1, 3))]:
    chk(F(a, b) == r, "2100 %d/%d" % (a, b))
chk(factorint(36) == {2: 2, 3: 2} and factorint(48) == {2: 4, 3: 1} and factorint(51) == {3: 1, 17: 1}, "2100 décompositions")
# ---------- 2182
chk(F(2, 3) + F(1, 6) == F(5, 6) and F(7, 12) + F(5, 18) == F(31, 36), "2182")
chk(F(1, 2) + F(1, 3) + F(1, 6) == 1, "2182 Q5")
from math import lcm
chk(lcm(12, 18) == 36, "ppcm")
# ---------- 2183
chk(F(2, 3) * F(3, 4) == F(1, 2) and F(3, 5) / F(-9, 10) == F(-2, 3) and F(5, 6) / F(10, 3) == F(1, 4), "2183")
chk(F(-3, 5) * F(-5, 3) == 1, "inverse")
# ---------- 2103
chk(F(7, 8) * 56 == 49 and F(3, 4) * 60 == 45 and F(5, 6) * 300 == 250 and F(2, 3) * F(5, 4) == F(5, 6), "2103")
# ---------- 2104
chk(F(-5, 6) < F(-3, 4) < F(-2, 3) < F(-7, 12), "2104 ordre")
chk(F(5, 7) > F(7, 10) and F(7, 10) < F(5, 7) < F(3, 4), "2104 Q4-5")
chk(F(5, 7) == F(100, 140) and F(7, 10) == F(98, 140) and F(3, 4) == F(105, 140), "2104 en 140e")
# ---------- 2184
C = (F(2, 3) + F(1, 6)) / (F(5, 4) - F(1, 2))
chk(C == F(10, 9) and C > 1, "2184 C")
chk((F(3, 4) - F(1, 2)) / F(5, 6) == F(3, 10), "2184 D")
# ---------- 2185
chk(F(8 + 4, 4) == 3 and F(15 + 5, 5) == 4 and F(17, 7) != 11, "2185")
# ---------- 2107
chk(F(2, 3) - F(1, 4) * F(8, 3) == 0 and (F(2, 3) - F(1, 4)) * F(8, 3) == F(10, 9), "2107 D E")
Fv, G = F(1, 2) + F(1, 2) * F(1, 3), (F(1, 2) + F(1, 2)) * F(1, 3)
chk(Fv == F(2, 3) and G == F(1, 3) and Fv == 2 * G, "2107 F G")


# ---------- 2108
def prog(x):
    return (x - F(1, 2)) * F(2, 3)


chk(prog(F(5, 4)) == F(1, 2) and prog(F(1, 2)) == 0 and prog(2) == 1, "2108")
chk(all(prog(F(k, 7)) == F(2, 3) * F(k, 7) - F(1, 3) for k in range(-10, 10)), "2108 Q5")
# ---------- 2109
u = F(3, 4) / 6
chk(u == F(1, 8) and 10 * u == F(5, 4) and 15 * u == F(15, 8) and 3 * u == F(3, 8) and 2 / u == 16, "2109")
# ---------- 2110
chk(2 - F(5, 7) == F(9, 7) and (D(9) / D(7)).quantize(D("0.001"), ROUND_HALF_UP) == D("1.286"), "2110")
chk(3 - F(8, 5) == F(7, 5) == F(14, 10), "2110 Q4")
# ---------- 2111
lu = F(2, 5)
ma = F(1, 3) * (1 - lu)
chk(ma == F(1, 5) and 1 - lu - ma == F(2, 5) and lu * 270 == 108 and ma * 270 == 54 and (1 - lu - ma) * 270 / 27 == 4, "2111")
# ---------- 2112
apres = F(7, 8) * F(5, 7)
chk(apres == F(5, 8) and F(3, 4) - apres == F(1, 8), "2112 fractions")
cap = 30 * 8
chk(cap == 240 and F(7, 8) * cap == 210 and F(2, 7) * 210 == 60 and 210 - 60 + 30 == F(3, 4) * cap, "2112")
# ---------- 2113
mat = F(3, 8) + F(5, 12)
chk(mat == F(19, 24) and 1 - mat == F(5, 24), "2113")
T = 15 / (1 - mat)
chk(T == 72 and F(3, 8) * T == 27 and F(5, 12) * T == 30 and 27 + 30 + 15 == 72, "2113 km")
# ---------- 2114
fa = F(3, 5) * F(5, 6)
N = 15 / fa
chk(fa == F(1, 2) and N == 30 and N * F(1, 6) == 5 and F(2, 5) * 25 == 10 and F(10, 30) == F(1, 3), "2114")
chk(F(3, 5) * 30 == 18, "2114 erreur fréquente")
# ---------- 2115 (vrai/faux)
chk(F(2, 3) + F(1, 4) == F(11, 12) != F(3, 7), "2115 Q1")
chk(F(2, 3) * F(3, 4) == F(1, 2), "2115 Q2")
chk(D("0.25") * 4 == 1, "2115 Q3")
chk(F(7, 9) < F(78, 100) and F(7, 9) == F(700, 900) and F(78, 100) == F(702, 900), "2115 Q4")
chk(7 / F(1, 2) == 14, "2115 Q5")
# ---------- 2116
deb = F(1, 3) + F(1, 6)
chk(deb == F(1, 2) and 1 / deb == 2, "2116")
chk(F(1, 3) * 1200 == 400 and F(1, 6) * 1200 == 200 and F(1200, 600) == 2, "2116 débits")
reste = 1 - F(1, 3)
t = reste / deb
chk(t == F(4, 3) and t * 60 == 80 and 60 + t * 60 == 140, "2116 Q5 : 2 h 20")
# ---------- 2117
sol = [n for n in range(0, 40) if F(2, 3) < F(n, 12) < F(5, 4)]
chk(sol == [9, 10, 11, 12, 13, 14], "2117")
chk(len([n for n in range(0, 40) if F(2, 3) < F(n, 12) <= F(5, 4)]) == 7, "2117 Q5")

print("verif_233 :", ok, "contrôles, tout est juste.")
