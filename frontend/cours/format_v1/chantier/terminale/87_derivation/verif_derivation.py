# -*- coding: utf-8 -*-
"""Vérification (sympy) de tous les résultats de la notion « Dérivation » (Terminale).

    python verif_derivation.py      -> affiche chaque contrôle, code 1 si un contrôle échoue
"""
import sys

import sympy as sp

x = sp.symbols("x", real=True)
X = sp.symbols("X", real=True)
ECHECS = []


def ok(nom, cond):
    cond = bool(cond)
    print(("OK   " if cond else "ÉCHEC") + " " + nom)
    if not cond:
        ECHECS.append(nom)


def egal(a, b):
    return sp.simplify(sp.expand(a - b)) == 0


def ens(cond):
    """Ensemble des réels vérifiant une condition."""
    return sp.solveset(cond, x, sp.S.Reals)


R = sp.S.Reals
oo = sp.oo

# =============================================================== COURS
print("--- cours")
ok("(e^(x^2+1))' = 2x e^(x^2+1)", egal(sp.diff(sp.exp(x**2 + 1), x), 2 * x * sp.exp(x**2 + 1)))
ok("((3x-1)^5)' = 15(3x-1)^4", egal(sp.diff((3 * x - 1)**5, x), 15 * (3 * x - 1)**4))
ok("(sqrt(x^2+9))' = x/sqrt(x^2+9)", egal(sp.diff(sp.sqrt(x**2 + 9), x), x / sp.sqrt(x**2 + 9)))
ok("(e^(3x))' = 3e^(3x)", egal(sp.diff(sp.exp(3 * x), x), 3 * sp.exp(3 * x)))
ok("(1/(x^2+1))' = -2x/(x^2+1)^2", egal(sp.diff(1 / (x**2 + 1), x), -2 * x / (x**2 + 1)**2))
ok("exp(x^2+1) composée : u∘v = e^(2x)+1", egal((sp.exp(x))**2 + 1, sp.exp(2 * x) + 1))
# fonctions de référence : f''
xp = sp.symbols("xp", positive=True)
ok("(x^2)'' = 2", sp.diff(x**2, x, 2) == 2)
ok("(x^3)'' = 6x", sp.diff(x**3, x, 2) == 6 * x)
ok("(1/x)'' = 2/x^3", egal(sp.diff(1 / x, x, 2), 2 / x**3))
ok("(sqrt x)'' = -1/(4 x sqrt x)", egal(sp.diff(sp.sqrt(xp), xp, 2), -1 / (4 * xp * sp.sqrt(xp))))
ok("(ln x)'' = -1/x^2", egal(sp.diff(sp.log(xp), xp, 2), -1 / xp**2))
# exemple x^3 - 3x
f = x**3 - 3 * x
ok("x^3-3x : f' = 3x^2-3", egal(sp.diff(f, x), 3 * x**2 - 3))
ok("x^3-3x : f'' = 6x", egal(sp.diff(f, x, 2), 6 * x))
ok("x^3-3x : tangente en 0 : y = -3x", egal(sp.diff(f, x).subs(x, 0) * x + f.subs(x, 0), -3 * x))
ok("x^3-3x : f(x) - (-3x) = x^3 (change de signe en 0)", egal(f - (-3 * x), x**3))
ok("x^4 : f'' = 12x^2", egal(sp.diff(x**4, x, 2), 12 * x**2))
# inégalités
ok("tangente à exp en 0 : y = x + 1", egal(sp.exp(0) * x + sp.exp(0), x + 1))
ok("tangente à ln en 1 : y = x - 1", egal(sp.diff(sp.log(xp), xp).subs(xp, 1) * (xp - 1) + sp.log(1), xp - 1))
ok("corde de exp sur [0;1] : y = 1 + (e-1)x", egal(1 + (sp.E - 1) * x, sp.exp(0) + (sp.exp(1) - sp.exp(0)) * x))
ok("e^0,5 <= 1 + 0,5(e-1) (≈ 1,859)", sp.exp(sp.Rational(1, 2)) <= 1 + sp.Rational(1, 2) * (sp.E - 1))
print("     1 + 0,5(e-1) ≈", sp.N(1 + (sp.E - 1) / 2, 4), " ; e^0,5 ≈", sp.N(sp.exp(0.5), 4))
# Lorenz
ok("Lorenz L(0,5) = 0,25", sp.Rational(1, 2)**2 == sp.Rational(1, 4))
ok("Lorenz : x^2 <= x sur [0;1]", ens(x**2 - x <= 0) == sp.Interval(0, 1))

# ======================================================= EXERCICE 1253
print("--- 1253 composées rationnelles")
f = lambda t: 1 / (t + 1)
g = lambda t: 2 * t - 3
h = lambda t: t**2
ok("f∘g = 1/(2(x-1))", egal(f(g(x)), 1 / (2 * (x - 1))))
ok("g∘f = (-3x-1)/(x+1)", egal(g(f(x)), (-3 * x - 1) / (x + 1)))
ok("h∘g = 4x^2-12x+9", egal(h(g(x)), 4 * x**2 - 12 * x + 9))
ok("f∘h = 1/(x^2+1)", egal(f(h(x)), 1 / (x**2 + 1)))
ok("g∘h = 2x^2-3", egal(g(h(x)), 2 * x**2 - 3))
ok("f∘g∘h = 1/(2(x-1)(x+1))", egal(f(g(h(x))), 1 / (2 * (x - 1) * (x + 1))))
ok("D f∘g∘h : 2x^2-2 = 0 <=> x = ±1", sp.solveset(2 * x**2 - 2, x, R) == sp.FiniteSet(-1, 1))

# ======================================================= EXERCICE 1261
print("--- 1261 dérivées de composées")
ok("f' = 2x e^(x^2+1)", egal(sp.diff(sp.exp(x**2 + 1), x), 2 * x * sp.exp(x**2 + 1)))
G = sp.log(x**2 + 4)
ok("g' = 2x/(x^2+4)", egal(sp.diff(G, x), 2 * x / (x**2 + 4)))
ok("g(0) = ln 4 = 2 ln 2", egal(G.subs(x, 0), 2 * sp.log(2)))
ok("lim g en ±oo = +oo", sp.limit(G, x, oo) == oo and sp.limit(G, x, -oo) == oo)
ok("h' = 1/sqrt(2x-1)", egal(sp.diff(sp.sqrt(2 * x - 1), x), 1 / sp.sqrt(2 * x - 1)))
ok("k' = -2x/(x^2+3)^2", egal(sp.diff(1 / (x**2 + 3), x), -2 * x / (x**2 + 3)**2))
L = sp.log(3 * x**2 + 2 * x - 1)
ok("3x^2+2x-1 = (3x-1)(x+1)", egal(3 * x**2 + 2 * x - 1, (3 * x - 1) * (x + 1)))
ok("D_l = ]-oo;-1[ U ]1/3;+oo[", ens(3 * x**2 + 2 * x - 1 > 0) ==
   sp.Union(sp.Interval.open(-oo, -1), sp.Interval.open(sp.Rational(1, 3), oo)))
ok("l' = (6x+2)/(3x^2+2x-1)", egal(sp.diff(L, x), (6 * x + 2) / (3 * x**2 + 2 * x - 1)))
ok("m' = (-4x+5) e^(-2x^2+5x)", egal(sp.diff(sp.exp(-2 * x**2 + 5 * x), x), (-4 * x + 5) * sp.exp(-2 * x**2 + 5 * x)))
N = sp.sqrt(x**2 - 4 * x + 3)
ok("x^2-4x+3 = (x-1)(x-3)", egal(x**2 - 4 * x + 3, (x - 1) * (x - 3)))
ok("D_n = ]-oo;1] U [3;+oo[", ens(x**2 - 4 * x + 3 >= 0) == sp.Union(sp.Interval(-oo, 1), sp.Interval(3, oo)))
ok("n' = (x-2)/sqrt(x^2-4x+3)", egal(sp.diff(N, x), (x - 2) / N))
ok("n' -> -oo en 1-", sp.limit((x - 2) / N, x, 1, "-") == -oo)
ok("n' -> +oo en 3+", sp.limit((x - 2) / N, x, 3, "+") == oo)

# ======================================================= EXERCICE 1257
print("--- 1257 produit, quotient, convexité")
H = (x**2 + 3 * x) * (2 * x - 1)
K = (x**2 + 2) / (x - 3)
ok("h = 2x^3+5x^2-3x", egal(H, 2 * x**3 + 5 * x**2 - 3 * x))
ok("h' = 6x^2+10x-3", egal(sp.diff(H, x), 6 * x**2 + 10 * x - 3))
ok("k' = (x^2-6x-2)/(x-3)^2", egal(sp.diff(K, x), (x**2 - 6 * x - 2) / (x - 3)**2))
ok("lim k en 3- = -oo", sp.limit(K, x, 3, "-") == -oo)
ok("lim k en 3+ = +oo", sp.limit(K, x, 3, "+") == oo)
x1 = (-5 - sp.sqrt(43)) / 6
x2 = (-5 + sp.sqrt(43)) / 6
ok("Delta = 172 = 4×43", 10**2 - 4 * 6 * (-3) == 172)
ok("racines de h' : (-5 ± sqrt43)/6", set(sp.solve(6 * x**2 + 10 * x - 3, x)) == {x1, x2})
print("     x1 ≈", sp.N(x1, 5), " x2 ≈", sp.N(x2, 5), " h(x1) ≈", sp.N(H.subs(x, x1), 5), " h(x2) ≈", sp.N(H.subs(x, x2), 5))
ok("x1 ≈ -1,93 ; x2 ≈ 0,26", abs(sp.N(x1) + 1.93) < 0.005 and abs(sp.N(x2) - 0.26) < 0.005)
ok("h(x1) ≈ 10,04 ; h(x2) ≈ -0,41", abs(sp.N(H.subs(x, x1)) - 10.04) < 0.005 and abs(sp.N(H.subs(x, x2)) + 0.41) < 0.005)
ok("lim h en -oo = -oo ; en +oo = +oo", sp.limit(H, x, -oo) == -oo and sp.limit(H, x, oo) == oo)
ok("h'' = 12x+10", egal(sp.diff(H, x, 2), 12 * x + 10))
ok("h(-5/6) = 130/27", H.subs(x, sp.Rational(-5, 6)) == sp.Rational(130, 27))
ok("(-5/6)^2 + 3(-5/6) = -65/36", sp.Rational(-5, 6)**2 + 3 * sp.Rational(-5, 6) == sp.Rational(-65, 36))
ok("2(-5/6) - 1 = -8/3", 2 * sp.Rational(-5, 6) - 1 == sp.Rational(-8, 3))
print("     130/27 ≈", sp.N(sp.Rational(130, 27), 4))

# ======================================================= EXERCICE 1262
print("--- 1262 polynômes, produits, quotients")
ok("f' = 12x^3-15x^2+4x-7", egal(sp.diff(3 * x**4 - 5 * x**3 + 2 * x**2 - 7 * x + 1, x), 12 * x**3 - 15 * x**2 + 4 * x - 7))
ok("g' = 6x^2+2x-6", egal(sp.diff((2 * x + 1) * (x**2 - 3), x), 6 * x**2 + 2 * x - 6))
ok("h' = (x^2-4x-1)/(x-2)^2", egal(sp.diff((x**2 + 1) / (x - 2), x), (x**2 - 4 * x - 1) / (x - 2)**2))
ok("k = 4x^5-4x^4+x^3", egal(x**3 * (2 * x - 1)**2, 4 * x**5 - 4 * x**4 + x**3))
ok("k' = 20x^4-16x^3+3x^2", egal(sp.diff(x**3 * (2 * x - 1)**2, x), 20 * x**4 - 16 * x**3 + 3 * x**2))
ok("k' = x^2(2x-1)(10x-3)", egal(20 * x**4 - 16 * x**3 + 3 * x**2, x**2 * (2 * x - 1) * (10 * x - 3)))
ok("p' = (2x^4+7x^2-2x-1)/(x^2+1)^2",
   egal(sp.diff((2 * x**3 - x + 1) / (x**2 + 1), x), (2 * x**4 + 7 * x**2 - 2 * x - 1) / (x**2 + 1)**2))
ok("(x-1)(2x+1) = 2x^2-x-1", egal((x - 1) * (2 * x + 1), 2 * x**2 - x - 1))
ok("(2x+3)(2x^2-x-1) = 4x^3+4x^2-5x-3", egal((2 * x + 3) * (2 * x**2 - x - 1), 4 * x**3 + 4 * x**2 - 5 * x - 3))
ok("(x^2+3x)(4x-1) = 4x^3+11x^2-3x", egal((x**2 + 3 * x) * (4 * x - 1), 4 * x**3 + 11 * x**2 - 3 * x))
ok("q' = 8x^3+15x^2-8x-3", egal(sp.diff((x**2 + 3 * x) * (x - 1) * (2 * x + 1), x), 8 * x**3 + 15 * x**2 - 8 * x - 3))
ok("q = 2x^4+5x^3-4x^2-3x", egal((x**2 + 3 * x) * (x - 1) * (2 * x + 1), 2 * x**4 + 5 * x**3 - 4 * x**2 - 3 * x))
ok("r = x^2-1 (x ≠ ±1)", egal((x**4 - 2 * x**2 + 1) / (x**2 - 1), x**2 - 1))
ok("r' = 2x", egal(sp.diff((x**4 - 2 * x**2 + 1) / (x**2 - 1), x), 2 * x))

# ======================================================= EXERCICE 1254
print("--- 1254 composées avec racines et valeurs absolues")
F = lambda t: sp.sqrt(t + 2)
Gv = lambda t: sp.Abs(t - 1)
Hq = lambda t: t / (t - 2)
ok("D f∘g = R : |x-1|+2 >= 2 > 0", ens(sp.Abs(x - 1) + 2 >= 0) == R)
ok("D g∘f = [-2;+oo[", ens(x + 2 >= 0) == sp.Interval(-2, oo))
ok("|x-1| = 2 <=> x = -1 ou 3", sp.solveset(sp.Abs(x - 1) - 2, x, R) == sp.FiniteSet(-1, 3))
ok("x/(x-2) + 2 = (3x-4)/(x-2)", egal(Hq(x) + 2, (3 * x - 4) / (x - 2)))
ok("D f∘h = ]-oo;4/3] U ]2;+oo[", ens((3 * x - 4) / (x - 2) >= 0) ==
   sp.Union(sp.Interval(-oo, sp.Rational(4, 3)), sp.Interval.open(2, oo)))
ok("x/(x-2) - 1 = 2/(x-2)", egal(Hq(x) - 1, 2 / (x - 2)))
for t in (-3, 0, 1.5, 2.5, 7):
    ok(f"g∘h({t}) = 2/|x-2|", abs(sp.N(Gv(Hq(sp.nsimplify(t)))) - sp.N(2 / abs(sp.nsimplify(t) - 2))) < 1e-12)
    ok(f"f∘g∘h({t}) = sqrt(2(1+|x-2|)/|x-2|)",
       abs(sp.N(F(Gv(Hq(sp.nsimplify(t))))) - sp.N(sp.sqrt(2 * (1 + abs(sp.nsimplify(t) - 2)) / abs(sp.nsimplify(t) - 2)))) < 1e-12)

# ======================================================= EXERCICE 1256
print("--- 1256 composée exponentielle et convexité")
Gx = sp.exp(-x**2 + 2 * x - 1)
ok("-x^2+2x-1 = -(x-1)^2", egal(-x**2 + 2 * x - 1, -(x - 1)**2))
ok("g' = (-2x+2) e^(...)", egal(sp.diff(Gx, x), (-2 * x + 2) * Gx))
ok("g(1) = 1", Gx.subs(x, 1) == 1)
ok("lim g en ±oo = 0", sp.limit(Gx, x, oo) == 0 and sp.limit(Gx, x, -oo) == 0)
ok("g'' = (4x^2-8x+2) e^(...)", egal(sp.diff(Gx, x, 2), (4 * x**2 - 8 * x + 2) * Gx))
ok("(-2x+2)^2 - 2 = 4x^2-8x+2", egal((-2 * x + 2)**2 - 2, 4 * x**2 - 8 * x + 2))
r1, r2 = (2 - sp.sqrt(2)) / 2, (2 + sp.sqrt(2)) / 2
ok("racines 4x^2-8x+2 : (2 ± sqrt2)/2", set(sp.solve(4 * x**2 - 8 * x + 2, x)) == {r1, r2})
ok("Delta' : 64 - 32 = 32", 8**2 - 4 * 4 * 2 == 32)
ok("x1 ≈ 0,293 ; x2 ≈ 1,707", abs(sp.N(r1) - 0.293) < 5e-4 and abs(sp.N(r2) - 1.707) < 5e-4)
ok("g(x1) = g(x2) = e^(-1/2)", egal(Gx.subs(x, r1), sp.exp(-sp.Rational(1, 2))) and egal(Gx.subs(x, r2), sp.exp(-sp.Rational(1, 2))))
print("     e^(-1/2) ≈", sp.N(sp.exp(-0.5), 4))

# ======================================================= EXERCICE 1260
print("--- 1260 racine composée")
U = x**2 + 4 * x + 3
Fr = sp.sqrt(U)
ok("x^2+4x+3 = (x+1)(x+3)", egal(U, (x + 1) * (x + 3)))
ok("D_f = ]-oo;-3] U [-1;+oo[", ens(U >= 0) == sp.Union(sp.Interval(-oo, -3), sp.Interval(-1, oo)))
ok("f' = (x+2)/sqrt(...)", egal(sp.diff(Fr, x), (x + 2) / Fr))
ok("f'' = -1/((x^2+4x+3) sqrt(...))", egal(sp.diff(Fr, x, 2), -1 / (U * Fr)))
ok("u - (x+2)^2 = -1", egal(U - (x + 2)**2, -1))
ok("lim f en ±oo = +oo", sp.limit(Fr, x, oo) == oo and sp.limit(Fr, x, -oo) == oo)
ok("f(-3) = f(-1) = 0", Fr.subs(x, -3) == 0 and Fr.subs(x, -1) == 0)
ok("f(-6) = f(2) = sqrt 15", Fr.subs(x, -6) == sp.sqrt(15) and Fr.subs(x, 2) == sp.sqrt(15))

# ======================================================= EXERCICE 1259
print("--- 1259 logarithme d'un quotient")
Q = (x**2 + 1) / (x**2 - 4)
Fl = sp.log(Q)
ok("D_f : quotient > 0 <=> |x| > 2", ens(Q > 0) == sp.Union(sp.Interval.open(-oo, -2), sp.Interval.open(2, oo)))
ok("u' = -10x/(x^2-4)^2", egal(sp.diff(Q, x), -10 * x / (x**2 - 4)**2))
ok("f' = -10x/((x^2-4)(x^2+1))", egal(sp.diff(Fl, x), -10 * x / ((x**2 - 4) * (x**2 + 1))))
ok("(x^2-4)(x^2+1) = x^4-3x^2-4", egal((x**2 - 4) * (x**2 + 1), x**4 - 3 * x**2 - 4))
ok("v' = 2x(2x^2-3)", egal(sp.diff(x**4 - 3 * x**2 - 4, x), 2 * x * (2 * x**2 - 3)))
ok("numérateur de f'' = 10(3x^4-3x^2+4)",
   egal(-10 * (x**4 - 3 * x**2 - 4) - (-10 * x) * 2 * x * (2 * x**2 - 3), 10 * (3 * x**4 - 3 * x**2 + 4)))
ok("f'' = 10(3x^4-3x^2+4)/((x^2-4)^2(x^2+1)^2)",
   egal(sp.diff(Fl, x, 2), 10 * (3 * x**4 - 3 * x**2 + 4) / ((x**2 - 4)**2 * (x**2 + 1)**2)))
ok("3X^2-3X+4 : Delta = -39 < 0", (-3)**2 - 4 * 3 * 4 == -39)
ok("lim f en ±oo = 0", sp.limit(Fl, x, oo) == 0 and sp.limit(Fl, x, -oo) == 0)
ok("lim f en -2- = +oo ; en 2+ = +oo", sp.limit(Fl, x, -2, "-") == oo and sp.limit(Fl, x, 2, "+") == oo)
ok("quotient - 1 = 5/(x^2-4) > 0 sur D_f", egal(Q - 1, 5 / (x**2 - 4)))

# ======================================================= EXERCICE 1255
print("--- 1255 polynôme")
P = x**3 - 6 * x**2 + 9 * x + 1
ok("f' = 3(x-1)(x-3)", egal(sp.diff(P, x), 3 * (x - 1) * (x - 3)))
ok("f(1) = 5 ; f(3) = 1", P.subs(x, 1) == 5 and P.subs(x, 3) == 1)
ok("f'(1) = 0 -> tangente y = 5", sp.diff(P, x).subs(x, 1) == 0)
ok("f'' = 6(x-2)", egal(sp.diff(P, x, 2), 6 * (x - 2)))
ok("f(2) = 3", P.subs(x, 2) == 3)
ok("f'(2) = -3 ; tangente en I : y = -3x + 9", sp.diff(P, x).subs(x, 2) == -3 and egal(-3 * (x - 2) + 3, -3 * x + 9))
ok("lim f en -oo = -oo ; +oo = +oo", sp.limit(P, x, -oo) == -oo and sp.limit(P, x, oo) == oo)
ok("f(x) - 5 = (x-1)^2 (x-4)", egal(P - 5, (x - 1)**2 * (x - 4)))

# ======================================================= EXERCICE 1258
print("--- 1258 fonction rationnelle")
Fq = (x**2 + 4 * x + 3) / (x**2 - 1)
ok("x^2+4x+3 = (x+1)(x+3)", egal(x**2 + 4 * x + 3, (x + 1) * (x + 3)))
ok("f = (x+3)/(x-1) pour x ≠ -1", egal(Fq, (x + 3) / (x - 1)))
ok("f = 1 + 4/(x-1)", egal((x + 3) / (x - 1), 1 + 4 / (x - 1)))
ok("f' = -4/(x-1)^2", egal(sp.diff(Fq, x), -4 / (x - 1)**2))
ok("lim f en ±oo = 1", sp.limit(Fq, x, oo) == 1 and sp.limit(Fq, x, -oo) == 1)
ok("lim f en -1 = -1 (des deux côtés)", sp.limit(Fq, x, -1, "-") == -1 and sp.limit(Fq, x, -1, "+") == -1)
ok("lim f en 1- = -oo ; 1+ = +oo", sp.limit(Fq, x, 1, "-") == -oo and sp.limit(Fq, x, 1, "+") == oo)
ok("f'' = 8/(x-1)^3", egal(sp.diff(Fq, x, 2), 8 / (x - 1)**3))
ok("f(x) - 1 = 4/(x-1) : sous y=1 si x<1, au-dessus si x>1", egal(Fq - 1, 4 / (x - 1)))

# ================================================ FINITION 2026-11-02
print("--- finition : figures ajoutées des exercices existants")
H = (x**2 + 3 * x) * (2 * x - 1)
ok("1257 figure : h(-5/6) = 130/27, h'(-5/6) = -43/6", H.subs(x, sp.Rational(-5, 6)) == sp.Rational(130, 27)
   and sp.diff(H, x).subs(x, sp.Rational(-5, 6)) == sp.Rational(-43, 6))
ok("1257 figure : extremums vers -1,93 (10,04) et 0,26 (-0,41)",
   abs(float((-5 - sp.sqrt(43)) / 6) + 1.9262) < 1e-3 and abs(float(H.subs(x, (-5 - sp.sqrt(43)) / 6)) - 10.036) < 1e-2
   and abs(float(H.subs(x, (-5 + sp.sqrt(43)) / 6)) + 0.4069) < 1e-3)
ok("1253 schéma : 2x-3 = -1 <=> x = 1", sp.solve(2 * x - 3 + 1, x) == [1])
ok("1261 figure : h(x) = sqrt(2x-1) vaut 0 en 1/2, taux sqrt(2/t)",
   sp.sqrt(2 * x - 1).subs(x, sp.Rational(1, 2)) == 0)

print("--- nouveau-1 : lecture sur la courbe de f'")
F1 = x**4 / 4 - sp.Rational(3, 2) * x**2
D1 = sp.diff(F1, x)
ok("f' = x^3 - 3x = x(x^2-3)", egal(D1, x**3 - 3 * x) and egal(D1, x * (x**2 - 3)))
ok("f' s'annule en -sqrt3, 0, sqrt3", set(sp.solve(D1, x)) == {0, -sp.sqrt(3), sp.sqrt(3)})
ok("extremums de f' en -1 (2) et 1 (-2)", set(sp.solve(sp.diff(D1, x), x)) == {-1, 1}
   and D1.subs(x, -1) == 2 and D1.subs(x, 1) == -2)
ok("f'' = 3(x-1)(x+1)", egal(sp.diff(F1, x, 2), 3 * (x - 1) * (x + 1)))
ok("signe f'' : + / - / +", sp.diff(F1, x, 2).subs(x, -2) > 0 and sp.diff(F1, x, 2).subs(x, 0) < 0
   and sp.diff(F1, x, 2).subs(x, 2) > 0)
ok("f(1) = f(-1) = -5/4", F1.subs(x, 1) == sp.Rational(-5, 4) and F1.subs(x, -1) == sp.Rational(-5, 4))
T1 = sp.diff(F1, x).subs(x, 1) * (x - 1) + F1.subs(x, 1)
ok("T : y = -2x + 3/4", egal(T1, -2 * x + sp.Rational(3, 4)))
ok("(x-1)^3 = x^3-3x^2+3x-1 ; (x-1)^3(x+3) = x^4-6x^2+8x-3",
   egal((x - 1)**3, x**3 - 3 * x**2 + 3 * x - 1) and egal((x - 1)**3 * (x + 3), x**4 - 6 * x**2 + 8 * x - 3))
ok("f - T = (1/4)(x-1)^3(x+3)", egal(F1 - T1, sp.Rational(1, 4) * (x - 1)**3 * (x + 3)))
ok("f - T > 0 sur ]-oo;-3[ et ]1;+oo[, < 0 sur ]-3;1[",
   ens(F1 - T1 > 0) == sp.Union(sp.Interval.open(-oo, -3), sp.Interval.open(1, oo))
   and ens(F1 - T1 < 0) == sp.Interval.open(-3, 1))
ok("figure n1 : f'(2,2) ≈ 4,05 ; f(2,65) ≈ 1,8 ; T(1,8) = -2,85",
   abs(float(D1.subs(x, 2.2)) - 4.048) < 1e-3 and abs(float(F1.subs(x, 2.65)) - 1.80) < 0.01
   and abs(float(T1.subs(x, 1.8)) + 2.85) < 1e-9)

print("--- nouveau-2 : ln x <= x/e")
L = sp.log(x)
ok("ln'' = -1/x^2", egal(sp.diff(L, x, 2), -1 / x**2))
TL = sp.diff(L, x).subs(x, sp.E) * (x - sp.E) + L.subs(x, sp.E)
ok("tangente en e : y = x/e (passe par O)", egal(TL, x / sp.E) and TL.subs(x, 0) == 0)
G2 = x / sp.E - sp.log(x)
ok("g' = (x-e)/(ex)", egal(sp.diff(G2, x), (x - sp.E) / (sp.E * x)))
ok("g(e) = 0", sp.simplify(G2.subs(x, sp.E)) == 0)
ok("lim g en 0+ = +oo ; en +oo = +oo", sp.limit(G2, x, 0, "+") == oo and sp.limit(G2, x, oo) == oo)
ok("g > 0 pour x != e (contrôle numérique)", all(float(G2.subs(x, v)) > 0 for v in (0.01, 0.5, 1, 2, 2.7, 2.75, 3.14, 10, 100)))
ok("pi^e ≈ 22,46 < e^pi ≈ 23,14", abs(float(sp.pi**sp.E) - 22.46) < 5e-3 and abs(float(sp.E**sp.pi) - 23.14) < 5e-3
   and float(sp.pi**sp.E) < float(sp.E**sp.pi))
ok("figure n2 : ln(0,075) ≈ -2,59 ; 8,3/e ≈ 3,05", abs(float(sp.log(0.075)) + 2.59) < 0.01 and abs(8.3 / float(sp.E) - 3.05) < 0.01)

print("--- nouveau-3 : modèle logistique")
t = sp.symbols("t", real=True)
E3 = sp.exp(-t / 2)
N = 10 / (1 + 9 * E3)
ok("N(0) = 1", N.subs(t, 0) == 1)
ok("lim N en +oo = 10", sp.limit(N, t, oo) == 10)
ok("u' = -4,5 e^(-0,5t)", egal(sp.diff(1 + 9 * E3, t), -sp.Rational(9, 2) * E3))
ok("N' = 45 e^(-0,5t)/(1+9e^(-0,5t))^2", sp.simplify(sp.diff(N, t) - 45 * E3 / (1 + 9 * E3)**2) == 0)
ok("N'' = 22,5 e^(-0,5t)(9e^(-0,5t)-1)/(1+9e^(-0,5t))^3",
   sp.simplify(sp.diff(N, t, 2) - sp.Rational(45, 2) * E3 * (9 * E3 - 1) / (1 + 9 * E3)**3) == 0)
t0 = 4 * sp.log(3)
ok("9e^(-0,5t) - 1 = 0 <=> t = 4 ln 3 = 2 ln 9", sp.simplify((9 * E3 - 1).subs(t, t0)) == 0
   and sp.simplify(2 * sp.log(9) - t0) == 0)
ok("9e^(-0,5t) - 1 > 0 avant t0, < 0 après", float((9 * E3 - 1).subs(t, 4)) > 0 and float((9 * E3 - 1).subs(t, 5)) < 0)
ok("e^(-0,5 t0) = 1/9", sp.simplify(E3.subs(t, t0)) == sp.Rational(1, 9))
ok("4 ln 3 ≈ 4,39", abs(float(t0) - 4.3944) < 1e-4)
ok("N(t0) = 5 ; N'(t0) = 5/4", sp.simplify(N.subs(t, t0)) == 5 and sp.simplify(sp.diff(N, t).subs(t, t0)) == sp.Rational(5, 4))
TN = sp.Rational(5, 4) * (t - t0) + 5
ok("courbe au-dessus de T avant t0, en dessous après (contrôle numérique)",
   all(float((N - TN).subs(t, v)) > 0 for v in (0, 1, 2, 3, 4, 4.3))
   and all(float((N - TN).subs(t, v)) < 0 for v in (4.5, 5, 6, 8, 12, 20)))
ok("figure n3 : T(1,2) ≈ 1,01 et T(7,6) ≈ 9,01", abs(float(TN.subs(t, 1.2)) - 1.007) < 0.01 and abs(float(TN.subs(t, 7.6)) - 9.007) < 0.01)

print()
print(f"{len(ECHECS)} échec(s)" if ECHECS else "Tous les contrôles sont bons.")
sys.exit(1 if ECHECS else 0)
