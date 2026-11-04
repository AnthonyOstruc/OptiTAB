# -*- coding: utf-8 -*-
"""Vérification de tous les résultats de la notion « Utiliser le calcul littéral »."""
from sympy import (symbols, expand, factor, simplify, sqrt, Rational as R, solveset, S,
                   Interval, Union, solve, together, cancel, pi)

x, a, b = symbols("x a b", real=True)
ok = 0


def eq(u, v, msg):
    global ok
    assert simplify(u - v) == 0, (msg, u, v)
    ok += 1


def ens(u, v, msg):
    global ok
    assert u == v, (msg, u, v)
    ok += 1


def ineq(rel, v, msg):
    ens(solveset(rel, x, S.Reals), v, msg)


# ---------------- cours
eq(R(2**5) * R(2)**-2 / 2**4, R(1, 2), "cours puissances")
eq(sqrt(50), 5 * sqrt(2), "sqrt50")
eq(sqrt(R(9, 16)), R(3, 4), "sqrt 9/16")
eq(sqrt((-5)**2), 5, "sqrt(a^2)=|a|")
eq(expand((2*x - 3)**2), 4*x**2 - 12*x + 9, "dev")
eq((x+1)*(2*x-5) + (x+1)*(x+2), 3*(x+1)*(x-1), "fact facteur commun")
eq(9*x**2 - 25, (3*x-5)*(3*x+5), "fact 9x2-25")
eq(1/x + 2/(x+1), (3*x+1)/(x*(x+1)), "fractions littérales")
ens(solveset((2*x-4)*(x+1), x, S.Reals), {2, -1}, "produit nul")
ens(solveset(x**2 - 5*x, x, S.Reals), {0, 5}, "x2=5x")
ineq(-2*x + 6 <= 0, Interval(3, S.Infinity), "-2x+6<=0")
ineq((2*x-4)*(-x+3) > 0, Interval.open(2, 3), "tableau de signes")
ineq(x**2 < 4, Interval.open(-2, 2), "x2<4")
ens(solveset(x**2 - 4, x, S.Reals), {-2, 2}, "x2=4")
ineq((x-1)/(x+2) >= 0, Union(Interval.open(-S.Infinity, -2), Interval(1, S.Infinity)), "quotient cours")
eq((x+3)**2 - (x+2)*(x+4), 1, "comparaison différence cours")
# ---------------- 1900
eq((3*x + 5*x - 7).subs(x, 2), 9, "1900 A")
eq(expand(2*(x-3) - 4*(x+2)), -2*x - 14, "1900 B"); eq((-2*x-14).subs(x, -1), -12, "1900 B val")
eq(expand(5*a - 2*(3*a-4) + a), 8, "1900 C")
eq(expand((x+1)**2 - (x**2+1)), 2*x, "1900 D")
eq(cancel((2*x+6)/(x+3)), 2, "1900 E")
# ---------------- 1906
P, L, l, Sg, r, U, I, Rr, d, v, t, y = symbols("P L l S r U I R d v t y", positive=True)
eq(solve(P - 2*(L+l), L)[0], P/2 - l, "1906 1")
eq(solve(Sg - pi*r**2, r)[0], sqrt(Sg/pi), "1906 2")
eq(solve(I - U/Rr, Rr)[0], U/I, "1906 3")
eq(solve(3*x + 5*y - 20, y)[0], (20-3*x)/5, "1906 4")
eq(solve(d - v*t, t)[0], d/v, "1906 5")
# ---------------- 1901
eq(R(2)**4 * R(2)**-6, R(1, 4), "1901 1"); eq(R(5**7, 5**3), 625, "1901 2")
eq((R(3)**-2)**3, R(1, 729), "1901 3"); eq((2*x**3)**2, 4*x**6, "1901 4")
eq(R(2, 3)**-4, R(81, 16), "1901 5")
# ---------------- 1907
eq(expand((x+1)**2 - (x**2+3)), 2*(x-1), "1907 1")
eq(expand((2*x+5) - (5*x-1)), -3*(x-2), "1907 2")
eq(expand((3*x-4)**2 - 9*x**2), 8*(2-3*x), "1907 3")
eq(expand((x-2)*(x+2) - (x**2-3)), -1, "1907 4")
eq(R(3**20, 2**30), R(9, 8)**10, "1907 5 quotient"); assert 3**20 > 2**30; ok += 1
# ---------------- 1913
ens(solveset(3/(x-2) + 5/(x+2) - 4*x/(x**2-4), x, S.Reals), {1}, "1913 1")
ens(solveset((x+1)/(x-3) - (x-1)/(x-2), x, S.Reals), {R(5, 3)}, "1913 2")
eq(expand((x+1)*(x-2) - (x-1)*(x-3)), 3*x - 5, "1913 2 réduction")
ens(solveset(2/(x+1) - 5/(2*x-1), x, S.Reals), {-7}, "1913 3")
ens(solveset((x**2-9)/(x-3) + 2/x - (x+4), x, S.Reals), {2}, "1913 4")
ens(solveset(1/(x-1) - 1/(x+1) - R(1, 2), x, S.Reals), {-sqrt(5), sqrt(5)}, "1913 5")
# ---------------- 1905
eq(cancel((x**2-9)/(x+3)), x-3, "1905 1"); eq(cancel((2*x**2+4*x)/(2*x)), x+2, "1905 2")
eq(together(1/x + 2/(x+1)) - (3*x+1)/(x*(x+1)), 0, "1905 3")
eq(cancel((x**2-1)/(x**2-2*x+1)), (x+1)/(x-1), "1905 4")
# Q5 réécrite le 2026-11-02 (x²+5x+6 se factorisait hors des identités du programme)
eq(x**2+6*x+9, (x+3)**2, "1905 5 num"); eq(x**2-9, (x-3)*(x+3), "1905 5 den")
eq(cancel((x**2+6*x+9)/(x**2-9)), (x+3)/(x-3), "1905 5")
ens(solveset(x**2-9, x, S.Reals), {-3, 3}, "1905 5 valeurs interdites")
# ---------------- 1910
eq(1 + R(3, 4)*R(2, 9), R(7, 6), "1910 A"); eq(R(4, 5) + R(3, 10)/R(9, 4), R(14, 15), "1910 B")
eq(R(3, 7)/R(5, 14), R(6, 5), "1910 C"); eq(R(1, 2)*(1-R(1, 3))**2, R(2, 9), "1910 D")
eq((R(5, 12)+R(1, 8))/R(7, 6), R(13, 28), "1910 E")
# ---------------- 1903
eq(expand((x+4)**2), x**2+8*x+16, "1903 1"); eq(expand((3*x-2)**2), 9*x**2-12*x+4, "1903 2")
eq(factor(x**2-10*x+25), (x-5)**2, "1903 3"); eq(factor(16*x**2-81), (4*x-9)*(4*x+9), "1903 4")
eq(factor(9*x**2+12*x+4), (3*x+2)**2, "1903 5")
# ---------------- 1908
ineq(3*x-5 <= 7, Interval(-S.Infinity, 4), "1908 1")
ineq(-2*x+3 > 5, Interval.open(-S.Infinity, -1), "1908 2")
ineq(5*x-2 >= 3*x+4, Interval(3, S.Infinity), "1908 3")
ineq(2*(1-x) < 3*x+4, Interval.open(R(-2, 5), S.Infinity), "1908 4")
ineq((x-3)/2 <= (x+1)/4, Interval(-S.Infinity, 7), "1908 5")
# ---------------- 1911
eq(R(1000)**4 * R(1, 100)**3, 10**6, "1911 A"); eq(R(1, 10)**-5 / 100**2, 10, "1911 B")
eq(R(10)**7 * (R(10)**-3)**4 / (R(10)**2)**-3, 10, "1911 C")
eq((R(1, 1000)/100)**-2, 10**10, "1911 D")
eq(R(1, 10000)**-3 * R(10)**-5 / 10000**2, R(1, 10), "1911 E")
# ---------------- 1912
eq(-3*sqrt(50) + 2*sqrt(8) + sqrt(72), -5*sqrt(2), "1912 1")
eq(sqrt(12)*sqrt(27)*sqrt(3), 18*sqrt(3), "1912 2")
eq(expand((3*sqrt(2)-2*sqrt(3))**2), 30-12*sqrt(6), "1912 3")
eq(expand((5-2*sqrt(6))*(5+2*sqrt(6))), 1, "1912 4")
eq(20*sqrt(45)/(12*sqrt(5)), 5, "1912 5")
# ---------------- 1902
eq(sqrt(72), 6*sqrt(2), "1902 1"); eq(sqrt(18)+sqrt(8), 5*sqrt(2), "1902 2")
eq(sqrt(R(50, 8)), R(5, 2), "1902 3"); eq(3/sqrt(5), 3*sqrt(5)/5, "1902 4")
eq(2/sqrt(3), 2*sqrt(3)/3, "1902 5")
# ---------------- 1904
eq(expand((2*x+3)*(x-5) + (x+1)**2), 3*x**2-5*x-14, "1904 1")
eq(9*x**2-16 + (3*x+4)*(x-2), 2*(3*x+4)*(2*x-3), "1904 2")
eq((x-2)*(x+2) - (x-2)**2, 4*(x-2), "1904 3")
eq(expand((x+2)*(x+5) - (x+3)*(x+4)), -2, "1904 4")
eq((x+1)*(x+4) + (x+1)*(2*x-3), (x+1)*(3*x+1), "1904 5")
# ---------------- 1909
ens(solveset(30+5*x - 8*x, x, S.Reals), {10}, "1909 égalité")
ineq(30+5*x < 8*x, Interval.open(10, S.Infinity), "1909 inéquation")
eq(30+5*12, 90, "1909 CA12"); eq(8*12, 96, "1909 CB12")
eq(30+5*11, 85, "1909 CA11"); eq(8*11, 88, "1909 CB11")
eq(30+5*9, 75, "1909 CA9"); eq(8*9, 72, "1909 CB9")
# ---------------- nouveau-1
ens(solveset((3*x-6)*(x+4), x, S.Reals), {2, -4}, "n1 1")
ineq((3*x-6)*(x+4) < 0, Interval.open(-4, 2), "n1 2")
ineq((x+1)/(2-x) >= 0, Interval.Ropen(-1, 2), "n1 3")
ineq(x**2 <= 4*x, Interval(0, 4), "n1 4")
# ---------------- nouveau-2
ens(solveset(x**2-49, x, S.Reals), {-7, 7}, "n2 a"); ens(solveset(x**2-7, x, S.Reals), {-sqrt(7), sqrt(7)}, "n2 b")
ens(solveset(x**2+4, x, S.Reals), S.EmptySet, "n2 c"); ens(solveset((x-1)**2-9, x, S.Reals), {-2, 4}, "n2 d")
ineq(x**2 < 9, Interval.open(-3, 3), "n2 2a")
ineq(x**2 >= 9, Union(Interval(-S.Infinity, -3), Interval(3, S.Infinity)), "n2 2b")
ineq(x**2 <= 2, Interval(-sqrt(2), sqrt(2)), "n2 3")
# ---------------- nouveau-3
fx = (x-1)**2 - 4
eq(expand(fx), x**2-2*x-3, "n3 dev"); eq(fx, (x-3)*(x+1), "n3 fact")
eq(fx.subs(x, 0), -3, "n3 f0")
ens(solveset(fx, x, S.Reals), {-1, 3}, "n3 f=0")
ens(solveset(fx + 3, x, S.Reals), {0, 2}, "n3 f=-3")
ens(solveset(fx - 5, x, S.Reals), {-2, 4}, "n3 f=5")
eq(fx + 4, (x-1)**2, "n3 minorant")

# ================= finition 2026-11-02 (textes et figures ajoutés)
k = symbols("k", real=True)
# 1900 Q3 (calcul aligné) et Q4 (figure : deux rectangles d'aire x)
eq(5*a - 2*(3*a - 4) + a, 8, "1900 C"); eq((5 - 6 + 1)*a + 8, 8, "1900 C étape")
eq((x+1)**2 - x**2 - 1, x + x, "1900 figure"); eq((x+1)**2 - (x**2+1), 2*x, "1900 D")
# 1903 Q1 (figure) : x² + 4x + 4x + 16
eq((x+4)**2, x**2 + 4*x + 4*x + 16, "1903 figure"); eq(2*x*4, 8*x, "1903 double produit")
# 1904 Q5 (figure) : longueurs positives pour x > 3/2
eq((x+4) + (2*x-3), 3*x+1, "1904 longueur"); eq((x+1)*(x+4) + (x+1)*(2*x-3), (x+1)*(3*x+1), "1904 aire")
ens(solveset(2*x-3 > 0, x, S.Reals), Interval.open(R(3, 2), S.Infinity), "1904 x > 3/2")
# 1907 Q1 (figure) : intersection (1 ; 4), A > B pour x > 1
ens(solveset((x+1)**2 - (x**2+3), x, S.Reals), {1}, "1907 intersection"); eq(((x+1)**2).subs(x, 1), 4, "1907 y=4")
ineq((x+1)**2 > x**2 + 3, Interval.open(1, S.Infinity), "1907 A>B")
# 1908 Q4 (figure)
ineq(2*(1-x) < 3*x + 4, Interval.open(R(-2, 5), S.Infinity), "1908 Q4 figure"); eq(R(-2, 5), -0.4, "-2/5 = -0,4")
# 3738 Q3 (figure) : minimum (1 ; -4), racines -1 et 3, f(-2,05) et f(4,05) dans la fenêtre
eq(fx.subs(x, 1), -4, "3738 min"); ens(solveset(fx, x, S.Reals), {-1, 3}, "3738 racines")
assert fx.subs(x, R(-205, 100)) < R(64, 10) and fx.subs(x, R(405, 100)) < R(64, 10); ok += 1
# cours : k(a + b) = ka + kb (figure)
eq(k*(a+b), k*a + k*b, "distributivité")
# 1904 (corrigé redécoupé) : étapes intermédiaires
eq((2*x+3)*(x-5), 2*x**2-7*x-15, "1904 Q1 produit"); eq((3*x+4)*((3*x-4)+(x-2)), (3*x+4)*(4*x-6), "1904 Q2 étape")
eq(4*x-6, 2*(2*x-3), "1904 Q2 fin"); eq((x-2)*((x+2)-(x-2)), 4*(x-2), "1904 Q3 facteur commun")
eq((x-2)*(x+2)-(x-2)**2, 4*(x-2), "1904 Q3")
# 1907 Q3 (redécoupé)
eq((9*x**2-24*x+16)-9*x**2, 8*(2-3*x), "1907 Q3")
print("OK :", ok, "vérifications")
