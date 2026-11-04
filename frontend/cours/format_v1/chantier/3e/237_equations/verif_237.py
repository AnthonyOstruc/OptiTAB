# -*- coding: utf-8 -*-
"""Vérification sympy de tous les résultats de la notion 237 « Équations » (cours, fiche, exercices)."""
from sympy import symbols, Eq, solve, Rational as R, expand, sqrt, factor

x, n = symbols("x n")
OK = 0


def sol(eq, attendu, var=x):
    global OK
    s = solve(eq, var)
    assert sorted(s, key=float) == sorted(attendu, key=float), (eq, s, attendu)
    OK += 1


def egal(a, b):
    global OK
    assert expand(a - b) == 0, (a, b)
    OK += 1


def vrai(c):
    global OK
    assert c
    OK += 1


# cours / fiche
sol(Eq(5*x - 7, 2*x + 8), [5]); vrai(5*5 - 7 == 18 and 2*5 + 8 == 18)
sol(Eq(3*(2*x - 5), 4*x + 9), [12]); vrai(3*(24 - 5) == 57 and 4*12 + 9 == 57)
sol(Eq(3*x + 2, x + 8), [3]); sol(Eq(2*x, 6), [3])
sol(Eq(4*x - 1, 2*x + 5), [3])
sol(Eq((x - 2)*(x + 3), 0), [-3, 2])
sol(Eq(x**2, 5*x), [0, 5])
sol(Eq(x**2, 49), [-7, 7]); sol(Eq(x**2, 12), [-sqrt(12), sqrt(12)]); vrai(abs(float(sqrt(12)) - 3.46) < 0.005)
vrai(solve(Eq(x**2, -4), x) == [] or all(not s.is_real for s in solve(Eq(x**2, -4), x)))
egal((x - 7)*(x + 7), x**2 - 49)
sol(Eq(5*x, 3*x + 12), [6]); vrai(5*6 == 30 and 3*6 + 12 == 30)
vrai(R(7, 3) != R(233, 100))
# figure cours_produit : sommet et bornes
vrai(((-4.2 - 2)*(-4.2 + 3)) < 8.4 and ((3.2 - 2)*(3.2 + 3)) < 8.4)

# 2201
sol(Eq(4*x + 3, x + 12), [3]); sol(Eq(3*x + 3, 12), [3]); sol(Eq(3*x, 9), [3]); vrai(4*3 + 3 == 15 == 3 + 12)
# 2202
sol(Eq(x + 13, 4), [-9]); sol(Eq(-4*x, 18), [R(-9, 2)]); sol(Eq(x/5, -3), [-15]); sol(Eq(7*x - 5, 30), [5]); sol(Eq(5 - 3*x, 11), [-2])
vrai(5 - 3*2 == -1)
# 2203
egal(8*x + 3 - 5*x, 3*x + 3); sol(Eq(8*x + 3, 5*x - 12), [-5]); vrai(8*(-5) + 3 == -37 == 5*(-5) - 12)
sol(Eq(9*x - 4, 4*x + 21), [5]); vrai(9*5 - 4 == 41 == 4*5 + 21)
sol(Eq(2*x + 10, 7*x), [2])
# 2204
egal(3*(2*x - 5), 6*x - 15); sol(Eq(3*(2*x - 5), 4*x + 9), [12]); sol(Eq(5*(x - 2), 3*x), [5]); sol(Eq(2*(x + 3), 4*(x - 1)), [5])
sol(Eq(6*x - 5, 4*x + 9), [7]); vrai(3*(2*7 - 5) == 27 and 4*7 + 9 == 37)
# 2205
sol(Eq(5*x + 2, 9), [R(7, 5)]); vrai(R(7, 5) == R(14, 10)); sol(Eq(3*x, 7), [R(7, 3)]); sol(Eq(2*x - 1, 6), [R(7, 2)])
vrai(abs(3*2.33 - 6.99) < 1e-9)
# 2206
vrai(2*3 + 5 == 11); vrai(3**2 != 6); vrai(4*3 - 1 == 2*3 + 5 == 11); vrai((-2)**2 == 4)
vrai((-1)**2 + 3*(-1) == -2 and 2*(-1) - 1 == -3)
# 2207
sol(Eq(2*x + 7, 19), [6]); sol(Eq(x/3, 12), [36]); sol(Eq(x + 5, 3*x), [R(5, 2)]); sol(Eq(x/4 - 2, 8), [40])
# 2208
sol(Eq(x/3 + x/4, 14), [24]); egal(12*(x/3 + x/4), 7*x); sol(Eq(x/2 - x/5, 6), [20]); sol(Eq(2*x/3, 8), [12]); sol(Eq(7*x, 14), [2])
# 2209
vrai(solve(Eq(4*(x - 2), 4*x - 8), x) == []); egal(4*(x - 2), 4*x - 8)
vrai(solve(Eq(4*(x - 2), 4*x + 1), x) == []); vrai(expand(4*(x - 2) - (4*x + 1)) == -9)
vrai(expand(3*x + 5 - (3*x - 5)) == 10); egal(2*(x + 3) - x, x + 6)
# 2210
sol(Eq((2*x - 7)*(x + 4), 0), [R(7, 2), -4]); sol(Eq(x*(3*x - 9), 0), [0, 3]); sol(Eq((5 - x)*(2*x + 1), 0), [5, R(-1, 2)])
# 2211
sol(Eq(x**2, 49), [7, -7]); sol(Eq(x**2, 12), [sqrt(12), -sqrt(12)]); sol(Eq(x**2, 0), [0])
vrai(all(not s.is_real for s in solve(Eq(x**2 + 9, 0), x))); sol(Eq(2*x**2 - 50, 0), [5, -5])
# 2212
egal(x*(x - 6), x**2 - 6*x); sol(Eq(x**2 - 6*x, 0), [0, 6]); sol(Eq(x**2, 5*x), [0, 5]); sol(Eq(2*x**2, 8*x), [0, 4])
egal(2*x*(x - 4), 2*x**2 - 8*x)
# 2213
egal(2*(x + 4) - 5, 2*x + 3); sol(Eq(3*(x - 1), 2*(x + 4) - 5), [6]); vrai(3*5 == 15 == 2*10 - 5)
sol(Eq((x + 5)*(3*x - 6), 0), [-5, 2]); sol(Eq(x**2 - 81, 0), [9, -9]); sol(Eq((2*x + 1)**2, 9), [1, -2])
# 2214
f = (x + 1)*(x - 3)
sol(Eq(f, 0), [-1, 3]); egal(f, x**2 - 2*x - 3); sol(Eq(f, -3), [0, 2]); vrai(f.subs(x, 1) == -4)
vrai(f.subs(x, -2.2) < 7 and f.subs(x, 4.2) < 7)
# 2215
sol(Eq(6*x + 10*(28 - x), 232), [12]); vrai(12*6 + 16*10 == 232 and 72 + 160 == 232)
# 2216
sol(Eq(2*x + 2*(x + 7), 58), [11]); vrai(18*11 == 198 and 2*11 + 2*18 == 58)
sol(Eq(x + x + 7, 58), [R(51, 2)]); vrai(2*(25.5 + 32.5) == 116)
# 2217
A = 3*(x + 4) - 2*x; B = (x + 1)**2 - x**2
egal(A, x + 12); egal(B, 2*x + 1); vrai(A.subs(x, 5) == 17 and B.subs(x, 5) == 11)
sol(Eq(A, B), [11]); vrai(A.subs(x, 11) == 23 == B.subs(x, 11)); sol(Eq(A, 0), [-12])
# 2218
sol(Eq(38 + 12*n, 30*n), [R(19, 9)], n); vrai(38 + 24 == 62 and 74 < 90 and 62 > 60)
sol(Eq(38 + 24*n, 30*n), [R(19, 3)], n); vrai(38 + 24*6 == 182 > 180 and 38 + 24*7 == 206 < 210)
# 2219
egal((x + 2)**2, x**2 + 4*x + 4); egal(x*(x + 5), x**2 + 5*x); sol(Eq((x + 2)**2, x*(x + 5)), [4])
vrai(6**2 == 4*9 == 36); sol(Eq(x**2 + 4, x**2 + 5*x), [R(4, 5)]); vrai(abs(2.8**2 - 7.84) < 1e-9 and abs(0.8*5.8 - 4.64) < 1e-9)
# 2220
sol(Eq(9*x, 40 + 4*x), [8]); vrai(9*8 == 72 == 40 + 32); vrai(9*5 == 45 and 40 + 20 == 60 and 9*12 == 108 and 40 + 48 == 88)
sol(Eq(9*x - (40 + 4*x), 20), [12])
# 2221
sol(Eq(x + 5, 2*(x - 7)), [19]); vrai(24 == 2*12); sol(Eq(x + 5, 2*x - 7), [12]); vrai(17 != 2*5)

print("verif_237 : %d contrôles OK" % OK)
