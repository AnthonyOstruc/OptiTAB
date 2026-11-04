# -*- coding: utf-8 -*-
"""Vérification des résultats de la notion 165 (nombres réels, Seconde)."""
from fractions import Fraction as F
from decimal import Decimal as D, ROUND_HALF_UP
import math

ok = 0


def chk(c, msg):
    global ok
    assert c, msg
    ok += 1


# ---------- cours
chk(F(125, 1000) == F(1, 8), "0,125")
chk(abs(5 - (-3)) == 8 and abs(-7) == 7, "distances")
chk(abs(3 + (-5)) == 2 and abs(3) + abs(-5) == 8, "|a+b|")
chk(D("1.41") ** 2 == D("1.9881") and D("1.42") ** 2 == D("2.0164"), "carrés")
chk(1.41 <= math.sqrt(2) <= 1.42, "encadrement racine 2")
chk(D(str(math.pi)).quantize(D("0.001"), ROUND_HALF_UP) == D("3.142"), "pi au millième")
# |x-3|<=2  <=> [1;5]
chk(all((abs(x - 3) <= 2) == (1 <= x <= 5) for x in [i / 10 for i in range(-50, 100)]), "centré")


# ---------- exercice 1934 : la fonction du cours / de l'énoncé
def encadrement(n):
    h = 10 ** (-n)
    a = 1
    while (a + h) ** 2 <= 2:
        a = a + h
    return a, a + h


for n in range(1, 6):
    a, b = encadrement(n)
    chk(a <= math.sqrt(2) < b and abs((b - a) - 10 ** (-n)) < 1e-12, "balayage %d" % n)
a, b = encadrement(2)
chk(round(a, 2) == 1.41 and round(b, 2) == 1.42, "n=2")


def encadrement3(n):
    h = 10 ** (-n)
    a = 1
    while (a + h) ** 2 <= 3:
        a = a + h
    return a, a + h


a, b = encadrement3(2)
chk(round(a, 2) == 1.73 and a <= math.sqrt(3) < b, "racine 3")

# ---------- exercice 1927 : périodiques
chk(F(3, 9) == F(1, 3), "0,333")
chk(F(27, 99) == F(3, 11) and F(3, 11) == F(272727, 999999), "0,2727")
chk(F(15, 90) == F(1, 6) and F(D("1.5")) / 9 == F(1, 6), "0,1666")
chk(F(975, 900) == F(13, 12) and abs(13 / 12 - 1.0833333333) < 1e-9, "1,08333")
chk(F(243, 99) == F(27, 11) and abs(27 / 11 - 2.454545454545) < 1e-9, "2,4545")

# ---------- exercice 1926 : appartenance
chk(-2 <= -2 <= 5, "q1")
chk(not (-2 < -2), "q2")
chk(not (0 < 0), "q3")
chk([x for x in (-1, 0, 2) if x >= 0] == [0, 2], "q4")
chk([x for x in (3.5, 4, 4.1) if 3.5 < x <= 4] == [4], "q5")

# ---------- exercice 1932
chk(F(D("12.3")) == F(123, 10), "12,3")
chk(F(D("0.04")) == F(1, 25), "0,04")
chk(F(7, 4) == F(D("1.75")), "7/4")


def decimal_frac(fr):
    q = fr.denominator
    for p in (2, 5):
        while q % p == 0:
            q //= p
    return q == 1


chk(not decimal_frac(F(1, 6)) and not decimal_frac(F(1, 3)) and decimal_frac(F(5, 2)), "décimaux")

# ---------- exercice 1931
chk((2 + 8) / 2 == 5 and (8 - 2) / 2 == 3, "centre rayon")
chk((-1 - 4, -1 + 4) == (-5, 3), "a=-1 r=4")
chk(all((abs(x + 2) < 3) == (-5 < x < 1) for x in [i / 4 for i in range(-40, 40)]), "|x+2|<3")
chk(abs(-4 - 1) == 5, "x=-4")

# ---------- exercice 1929 : ]2;4]
xs = [i / 4 for i in range(-20, 40)]
chk(all(((-1 <= x <= 4) and (2 < x < 6)) == (2 < x <= 4) for x in xs), "inter 1")
chk(all(((x <= 3) and (x >= 1)) == (1 <= x <= 3) for x in xs), "inter 2")
chk([x for x in (-3, -2, 0, 4, 6) if 2 < x <= 4] == [4], "inter 4")
chk(not any((0 <= x <= 1) and (1 < x < 2) for x in xs), "inter vide")

# ---------- exercice 1930
chk(abs(3 - 8) == 5 and abs(9 - (-4)) == 13, "distances")
chk(sorted(x for x in range(-10, 10) if abs(x - 3) == 2) == [1, 5], "dist 2")

# ---------- exercice 1933
chk(D("3.14") <= D(str(math.pi)) <= D("3.15"), "pi")
chk(D("0.7") <= D(5) / D(7) <= D("0.8") and abs(5 / 7 - 0.714285) < 1e-6, "5/7")
chk(D("3.14159").quantize(D("0.01"), ROUND_HALF_UP) == D("3.14"), "centième")
chk(D("3.14159").quantize(D("0.001"), ROUND_HALF_UP) == D("3.142"), "millième")
chk(D("4.8") ** 2 == D("23.04") and D("3.14") * D("23.04") == D("72.3456"), "aire")
chk(D("72.3456").quantize(D("0.1"), ROUND_HALF_UP) == D("72.3"), "arrondi aire")
chk(round(math.pi * 4.8 ** 2, 1) == 72.4, "aire avec pi exact")

# ---------- exercice 1935
chk((D("29.7") + D("30.3")) / 2 == 30 and (D("30.3") - D("29.7")) / 2 == D("0.3"), "tolérance")
acc = [L for L in (D("29.65"), D("29.90"), D("30.31")) if abs(L - 30) <= D("0.3")]
chk(acc == [D("29.90")], "tiges")
chk(D("30.34").quantize(D("0.1"), ROUND_HALF_UP) == D("30.3") and abs(D("30.34") - 30) > D("0.3"), "arrondi")

# ================= finition 2026-11-02
import sympy as sp

# 1934 (figure) : 1,38 -> 1,41 acceptés, 1,42 refusé, racine de 2 entre 1,41 et 1,42
chk(all(D(a) ** 2 <= 2 for a in ("1.38", "1.39", "1.40", "1.41")) and D("1.42") ** 2 > 2, "fig balayage")
chk(D("1.41") < D(2).sqrt() < D("1.42") and str(D(2).sqrt())[:6] == "1.4142", "fig racine 2")

# 1926 Q5 (figure) : ]3,5 ; 4]
chk([x for x in (D("3.5"), D(4), D("4.1")) if D("3.5") < x <= 4] == [D(4)], "fig appartenance")

# 1928 (figure) : trois ensembles
xs = [D(i) / 4 for i in range(-30, 45)]
chk(all((-2 <= x < 4) == (x >= -2 and x < 4) for x in xs), "traduire")

# 1932 Q4 : 10^n n'est jamais multiple de 3 (somme des chiffres 1), donc 1/3 non décimal
chk(all(10 ** n % 3 == 1 and sum(map(int, str(10 ** n))) == 1 for n in range(0, 30)), "10^n non multiple de 3")
chk(all(F(1, 3) != F(k, 10 ** n) for n in range(0, 8) for k in range(0, 10 ** n + 1)), "1/3 pas k/10^n (n<8)")
chk(F(5, 2) == F(25, 10) and F(-25, 10) == F(-5, 2), "classer")

# 1933 Q3 (figure)
chk(D("0.7") < D(5) / D(7) < D("0.8") and round(5 / 7, 3) == 0.714, "5/7 figure")

# nouveau-1 : droite graduée en quarts
A_, B_, C_, D_ = F(-3, 2), F(-1, 4), F(3, 4), F(7, 4)
chk(A_ == -1 - 2 * F(1, 4) and B_ == -F(1, 4) and C_ == 3 * F(1, 4) and D_ == 1 + 3 * F(1, 4), "lectures")
E_, F_ = F(-3, 4), F(5, 2)
chk(E_ == -3 * F(1, 4) and F_ == 2 + 2 * F(1, 4), "placer E F")
chk(F(5, 4) ** 2 == F(25, 16) and F(25, 16) < 2 < F(3, 2) ** 2 == F(9, 4), "G entre 1,25 et 1,5")
pts = {"A": A_, "B": B_, "C": C_, "D": D_, "E": E_, "F": F_, "G": sp.sqrt(2)}
chk(sorted(k for k, v in pts.items() if -1 <= v <= 1) == ["B", "C", "E"], "dans [-1;1]")
chk(abs(D_ - A_) == F(13, 4), "AD = 3,25")

# nouveau-2 : chiffres significatifs
def cs(t):
    t = t.replace(",", ".").lstrip("0").replace(".", "")
    return len(t.lstrip("0"))
chk(cs("23,4") == 3 and cs("0,052") == 2 and cs("4,80") == 3 and cs("0,0520") == 3, "chiffres significatifs")
chk(D("23.4") * D("15.7") == D("367.38"), "aire")
chk(D("367.38").quantize(D("1"), ROUND_HALF_UP) == 367, "aire 3 cs")
chk(D("23.35") * D("15.65") == D("365.4275") and D("23.45") * D("15.75") == D("369.3375"), "encadrement aire")
chk(D("365.4") <= D("365.4275") and D("369.3375") <= D("369.4"), "arrondi vers l'extérieur")
chk(D("23.4") ** 2 == D("547.56") and D("15.7") ** 2 == D("246.49") and D("547.56") + D("246.49") == D("794.05"), "d²")
dd = sp.sqrt(sp.Rational(79405, 100))
chk(sp.N(dd, 6) > 28.17 and sp.N(dd, 6) < 28.18 and round(float(dd), 1) == 28.2, "d ≈ 28,2")
chk(2 * (D("23.4") + D("15.7")) == D("78.2") and math.ceil(78.2) == 79, "grillage 79 m")

print("verif_165 : %d contrôles OK" % ok)
