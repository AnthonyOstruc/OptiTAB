# -*- coding: utf-8 -*-
"""Vérification (sympy) de tous les calculs de la notion 182 « Fonction exponentielle ».

    python verif_exponentielle.py      → affiche chaque contrôle, code de sortie 1 si une erreur

Couvre le cours, la fiche, les 15 exercices et les valeurs placées sur les figures.
"""
import math
import sys

import sympy as sp

x, t, X, a, b = sp.symbols("x t X a b", real=True)
n = sp.symbols("n", integer=True, nonnegative=True)
E = sp.E
exp = sp.exp
OK, KO = 0, []


def check(nom, cond):
    global OK
    if bool(cond):
        OK += 1
    else:
        KO.append(nom)
        print("ERREUR :", nom)


def egal(u, v):
    return sp.simplify(sp.expand(u - v)) == 0


def arrondi(val, ref, tol):
    """|val − ref| ≤ tol (ref : valeur écrite dans le texte)."""
    return abs(float(val) - ref) <= tol


def tronc(val, ref, chiffres):
    """ref = val tronqué à `chiffres` décimales (écriture « 2,5937… »)."""
    return math.floor(float(val) * 10**chiffres) / 10**chiffres == ref


def solve_set(expr_ineq):
    return sp.solveset(expr_ineq, x, sp.S.Reals)


def euler(nn):
    h = 1 / nn
    y = 1
    for _ in range(nn):
        y = y + h * y
    return y


# ======================================================================= COURS
check("cours : e ≈ 2,718", arrondi(E, 2.718, 5e-4))
# démonstration exp(x)exp(-x) = 1 (dérivée nulle)
g = exp(x) * exp(-x)
check("cours : g' = 0", egal(sp.diff(g, x), 0))
check("cours : g(0) = 1", g.subs(x, 0) == 1)
k = exp(x + b) * exp(-x)
check("cours : k' = 0", egal(sp.diff(k, x), 0))
check("cours : k(0) = exp(b)", egal(k.subs(x, 0), exp(b)))
# Euler pas 0,5
ys = [sp.Rational(3, 2) ** j for j in range(5)]
check("cours : Euler pas 0,5", ys == [1, sp.Rational(3, 2), sp.Rational(9, 4), sp.Rational(27, 8), sp.Rational(81, 16)])
check("cours : 5,0625", float(ys[4]) == 5.0625)
check("cours : e^2 ≈ 7,39", arrondi(exp(2), 7.39, 5e-3))
check("cours : euler(10) = 2,5937…", tronc(euler(10), 2.5937, 4))
check("cours : euler(100) = 2,7048…", tronc(euler(100), 2.7048, 4))
check("cours : euler(1000) = 2,7169…", tronc(euler(1000), 2.7169, 4))
check("cours : (1+1/n)^n = euler(n)", all(abs(euler(m) - (1 + 1 / m) ** m) < 1e-9 for m in (10, 100, 1000)))
check("cours : e ≈ 2,71828", arrondi(E, 2.71828, 5e-6))
# règles
check("cours : e^{-1} ≈ 0,368", arrondi(exp(-1), 0.368, 5e-4))
check("cours : e^{x+2} = e^2 e^x", egal(exp(x + 2), exp(2) * exp(x)))
check("cours : e^{5x}/e^{2x} = e^{3x}", egal(exp(5 * x) / exp(2 * x), exp(3 * x)))
check("cours : (e^x)^3 = e^{3x}", egal(exp(x) ** 3, exp(3 * x)))
check("cours : exemple produit", egal(exp(2 * x) * exp(-x + 3), exp(x + 3)))
check("cours : exemple quotient", egal(exp(x) ** 2 / exp(2 * x - 1), E))
check("cours : e^{1+1} ≈ 7,39 et e + e ≈ 5,44", arrondi(exp(2), 7.39, 5e-3) and arrondi(2 * E, 5.44, 5e-3))
# suite e^{-0,5 n}
q = exp(sp.Rational(-1, 2))
check("cours : e^{-0,5} ≈ 0,607", arrondi(q, 0.607, 5e-4))
check("cours : u_{n+1} = q u_n", egal(exp(-(n + 1) / sp.Integer(2)), q * exp(-n / sp.Integer(2))))
check("cours : 0 < q < 1", 0 < float(q) < 1)
# tangente en 0, e^{0,1}
check("cours : tangente y = x + 1", egal(sp.diff(exp(x), x).subs(x, 0) * x + exp(0), x + 1))
check("cours : e^{0,1} ≈ 1,105", arrondi(exp(sp.Rational(1, 10)), 1.105, 5e-4))
# équations
check("cours : e^{2x-1} = e^{x+3} → 4", sp.solve(sp.Eq(2 * x - 1, x + 3), x) == [4])
check("cours : e^{3x} > e^{x+4} → x > 2", solve_set(3 * x > x + 4) == sp.Interval.open(2, sp.oo))
check("cours : (x-2)e^x > 0 ⇔ x > 2", solve_set((x - 2) * exp(x) > 0) == sp.Interval.open(2, sp.oo))
# dérivée e^{at+b}
check("cours : (e^{at+b})' = a e^{at+b}", egal(sp.diff(exp(a * t + b), t), a * exp(a * t + b)))
# étude de (2x-1)e^x sur [-2 ; 1]
f = (2 * x - 1) * exp(x)
check("cours : f' = (2x+1)e^x", egal(sp.diff(f, x), (2 * x + 1) * exp(x)))
check("cours : f(-2) = -5e^{-2}", egal(f.subs(x, -2), -5 * exp(-2)))
check("cours : f(-1/2) = -2e^{-1/2}", egal(f.subs(x, sp.Rational(-1, 2)), -2 * exp(sp.Rational(-1, 2))))
check("cours : f(1) = e", egal(f.subs(x, 1), E))
check("cours : min ≈ -1,21", arrondi(f.subs(x, sp.Rational(-1, 2)), -1.21, 5e-3))
check("cours : min < f(-2) et < f(1)", float(f.subs(x, -0.5)) < float(f.subs(x, -2)) < float(f.subs(x, 1)))
# modèle m(t) = 100 e^{-0,1t}
m = lambda tt: 100 * math.exp(-0.1 * tt)
check("cours : m(10) ≈ 36,8", arrondi(m(10), 36.8, 0.05))
check("cours : e^{-0,1} ≈ 0,905", arrondi(math.exp(-0.1), 0.905, 5e-4))
check("cours : taux ≈ -9,5 %", arrondi(math.exp(-0.1) - 1, -0.095, 5e-4))
check("cours : m(6) ≈ 54,9 et m(7) ≈ 49,7", arrondi(m(6), 54.9, 0.05) and arrondi(m(7), 49.7, 0.05))
nn = 0
while 100 * math.exp(-0.1 * nn) > 50:
    nn += 1
check("cours : programme seuil → 7", nn == 7)
check("cours : Q'(t) = k Q(t)", egal(sp.diff(3 * exp(a * t), t), a * 3 * exp(a * t)))

# ======================================================================= FICHE
check("fiche : e^{3x}/e^{x+1} = e^{2x-1}", egal(exp(3 * x) / exp(x + 1), exp(2 * x - 1)))
check("fiche : (e^{-3t})' = -3e^{-3t}", egal(sp.diff(exp(-3 * t), t), -3 * exp(-3 * t)))

# ======================================================================= 1291
check("1291 Q1", egal(sp.diff(3 * exp(x) - 2 * x + 1, x), 3 * exp(x) - 2))
check("1291 Q2", egal(sp.diff(exp(3 * x), x), 3 * exp(3 * x)))
check("1291 Q3", egal(sp.diff(exp(-2 * x + 1), x), -2 * exp(-2 * x + 1)))
check("1291 Q4", egal(sp.diff(5 * exp(sp.Rational(2, 5) * x) - exp(-x), x), 2 * exp(sp.Rational(2, 5) * x) + exp(-x)))
check("1291 Q5", egal(sp.diff((x + 1) * exp(x), x), (x + 2) * exp(x)))

# ======================================================================= 1290
check("1290 Q1 e^{-3} > 0", float(exp(-3)) > 0)
check("1290 Q2", float(exp(2)) < float(exp(3)) and float(exp(-1)) < float(exp(-0.5)))
check("1290 Q3 tangente", egal(exp(0) + sp.diff(exp(x), x).subs(x, 0) * x, x + 1))
check("1290 Q4 e^{0,1} ≈ 1,10517", arrondi(exp(sp.Rational(1, 10)), 1.10517, 5e-6))
check("1290 Q4 écart ≈ 0,005", arrondi(exp(sp.Rational(1, 10)) - 1.1, 0.005, 6e-4))
check("1290 Q5 signe", solve_set((x - 2) * exp(x) < 0) == sp.Interval.open(-sp.oo, 2))

# ======================================================================= 1289
check("1289 A", egal(exp(2 * x + 3) * exp(-x), exp(x + 3)))
check("1289 B", egal(exp(3 * x) / exp(2 * x + 1), exp(x - 1)))
check("1289 C", egal(exp(x) ** 2 * exp(-3 * x), exp(-x)))
check("1289 D", egal(exp(x + 2) * exp(3 * x - 1) / exp(2 * x), exp(2 * x + 1)))
check("1289 D numérateur", egal(exp(x + 2) * exp(3 * x - 1), exp(4 * x + 1)))
check("1289 E", egal(exp(-x) ** 3 * exp(4 * x + 1) / E, exp(x)))
check("1289 E étape", egal(exp(-3 * x) * exp(4 * x + 1), exp(x + 1)))
check("1289 Q6", egal((exp(x) + exp(-x)) ** 2 - (exp(x) - exp(-x)) ** 2, 4))

# ======================================================================= 1293
check("1293 Q1", sp.solve(sp.Eq(2 * x + 1, x - 3), x) == [-4])
check("1293 Q2", sp.solve(sp.Eq(3 * x - 6, 0), x) == [2])
check("1293 Q3", sp.solve(sp.Eq(4 * x, x + 1), x) == [sp.Rational(1, 3)])
check("1293 Q3 forme", egal(E * exp(x), exp(x + 1)))
check("1293 Q4", solve_set(x - 1 < 2 * x + 3) == sp.Interval.open(-4, sp.oo))
check("1293 Q5", solve_set(exp(-x) >= exp(-2)) == sp.Interval(-sp.oo, 2))
check("1293 Q6", solve_set(sp.Eq(exp(x), -3)) == sp.S.EmptySet)

# ======================================================================= 1298
f = exp(x) - x
check("1298 f'", egal(sp.diff(f, x), exp(x) - 1))
check("1298 e^x > 1 ⇔ x > 0", solve_set(exp(x) > 1) == sp.Interval.open(0, sp.oo))
check("1298 f(0) = 1", f.subs(x, 0) == 1)
check("1298 min global", all(float(f.subs(x, v)) >= 1 for v in [i / 10 for i in range(-50, 51)]))
check("1298 e^{0,1} ≥ 1,1", float(exp(0.1)) >= 1.1)
check("1298 e^{-0,1} ≥ 0,9", float(exp(-0.1)) >= 0.9)
check("1298 e^{0,1} ≤ 10/9", float(exp(0.1)) <= 10 / 9)
check("1298 10/9 ≈ 1,111", arrondi(sp.Rational(10, 9), 1.111, 5e-4))
check("1298 e^{0,1} ≈ 1,105", arrondi(exp(0.1), 1.105, 5e-4))

# ======================================================================= 1294
g = x * exp(x)
check("1294 g'", egal(sp.diff(g, x), (x + 1) * exp(x)))
check("1294 g(-1) = -1/e", egal(g.subs(x, -1), -1 / E))
check("1294 -1/e ≈ -0,368", arrondi(-1 / E, -0.368, 5e-4))
check("1294 g ≥ -1/e", all(float(g.subs(x, v)) >= float(-1 / E) - 1e-12 for v in [i / 10 for i in range(-80, 30)]))
check("1294 g = 0 ⇔ x = 0", solve_set(sp.Eq(g, 0)) == sp.FiniteSet(0))
check("1294 tangente y = x", egal(g.subs(x, 0) + sp.diff(g, x).subs(x, 0) * x, x))
check("1294 g - x factorisé", egal(g - x, x * (exp(x) - 1)))
check("1294 g - x ≥ 0", all(float((g - x).subs(x, v)) >= 0 for v in [i / 10 for i in range(-80, 30)]))

# ======================================================================= 1297
check("1297 Q1", set(sp.solve(x**2 - 3 * x + 2, x)) == {1, 2})
check("1297 Q1 Δ", (-3) ** 2 - 4 * 2 == 1)
check("1297 Q2", solve_set(x**2 - 4 * x + 3 >= 0) == sp.Union(sp.Interval(-sp.oo, 1), sp.Interval(3, sp.oo)))
check("1297 Q2 vérif exp", solve_set(exp(x**2 - 4 * x + 3) >= 1) == sp.Union(sp.Interval(-sp.oo, 1), sp.Interval(3, sp.oo)))
check("1297 Q3 Δ = (e-1)²", egal((1 + E) ** 2 - 4 * E, (E - 1) ** 2))
check("1297 Q3 factorisation", egal((X - 1) * (X - E), X**2 - (1 + E) * X + E))
check("1297 Q3 racines", egal(((1 + E) - (E - 1)) / 2, 1) and egal(((1 + E) + (E - 1)) / 2, E))
eq3 = exp(2 * x) - (1 + E) * exp(x) + E
check("1297 Q3 solutions", egal(eq3.subs(x, 0), 0) and egal(eq3.subs(x, 1), 0))
check("1297 Q4 factorisation", egal((X - 1) * (X + 2), X**2 + X - 2))
check("1297 Q4", solve_set(exp(2 * x) + exp(x) - 2 > 0) == sp.Interval.open(0, sp.oo))
check("1297 Q5 quotient", egal(exp(x + 1) / exp(x - 1), exp(2)))
check("1297 Q5", float(exp(2)) > 2 and arrondi(exp(2), 7.39, 5e-3))
check("1297 Q6", solve_set((x**2 - 1) * exp(-x) <= 0) == sp.Interval(-1, 1))

# ======================================================================= 1299
u = lambda k_: exp(-sp.Rational(1, 2) * k_)
check("1299 u0, u1, u2", u(0) == 1 and arrondi(u(1), 0.607, 5e-4) and arrondi(u(2), 0.368, 5e-4))
check("1299 géométrique", egal(u(n + 1), exp(sp.Rational(-1, 2)) * u(n)))
S = sum(u(k_) for k_ in range(10))
check("1299 somme formule", egal(S, (1 - exp(-5)) / (1 - exp(sp.Rational(-1, 2)))))
check("1299 S ≈ 2,524", arrondi(S, 2.524, 5e-4))
v = lambda k_: 3 * exp(2 * k_ + 1)
check("1299 v géométrique", egal(v(n + 1), exp(2) * v(n)))
check("1299 v0 = 3e", egal(v(0), 3 * E))
check("1299 v5 ≈ 179 622", arrondi(v(5), 179622, 0.5))
check("1299 v6 ≈ 1 327 240", arrondi(v(6), 1327240, 0.5))
nn = 0
while 3 * math.exp(2 * nn + 1) <= 10**6:
    nn += 1
check("1299 programme → 6", nn == 6)

# ======================================================================= 1292
f = (x**2 - 3) * exp(x)
check("1292 f'", egal(sp.diff(f, x), (x + 3) * (x - 1) * exp(x)))
check("1292 trinôme", egal(x**2 + 2 * x - 3, (x + 3) * (x - 1)))
check("1292 f(-5)", egal(f.subs(x, -5), 22 * exp(-5)))
check("1292 f(-3)", egal(f.subs(x, -3), 6 * exp(-3)))
check("1292 f(1)", egal(f.subs(x, 1), -2 * E))
check("1292 f(2)", egal(f.subs(x, 2), exp(2)))
check("1292 arrondis", arrondi(6 * exp(-3), 0.30, 5e-3) and arrondi(-2 * E, -5.44, 5e-3) and arrondi(exp(2), 7.39, 5e-3))
check("1292 22e^{-5} > 0 et < 6e^{-3}", 0 < float(22 * exp(-5)) < float(6 * exp(-3)))
check("1292 zéros", solve_set(sp.Eq(x**2 - 3, 0)) == sp.FiniteSet(-sp.sqrt(3), sp.sqrt(3)))
check("1292 √3 ≈ 1,73", arrondi(sp.sqrt(3), 1.73, 5e-3))
check("1292 signe", sp.solveset(f < 0, x, sp.Interval(-5, 2)) == sp.Interval.open(-sp.sqrt(3), sp.sqrt(3)))
check("1292 tangente", egal(f.subs(x, 0) + sp.diff(f, x).subs(x, 0) * x, -3 * x - 3))

# ======================================================================= 1301
check("1301 Q1", egal(exp(x) + a * exp(x), (1 + a) * exp(x)))
check("1301 pas 0,5", [1.5**j for j in range(3)] == [1, 1.5, 2.25])
check("1301 pas 0,25", [1.25**j for j in range(5)] == [1, 1.25, 1.5625, 1.953125, 2.44140625])
check("1301 y_n = (1+1/n)^n", all(abs(euler(m_) - (1 + 1 / m_) ** m_) < 1e-9 for m_ in (2, 4, 10)))
check("1301 euler(2) = 2,25", abs(euler(2) - 2.25) < 1e-12)
check("1301 euler(4) = 2,4414…", abs(euler(4) - 2.44140625) < 1e-12)
check("1301 tableau", tronc(euler(10), 2.5937, 4) and tronc(euler(100), 2.7048, 4) and tronc(euler(1000), 2.7169, 4))
check("1301 écarts", arrondi(E - euler(10), 0.12, 5e-3) and arrondi(E - euler(100), 0.013, 5e-4)
      and arrondi(E - euler(1000), 0.0014, 5e-5))
check("1301 inférieures à e", all(euler(m_) < float(E) for m_ in (2, 4, 10, 100, 1000)))
check("1301 croissantes", euler(10) < euler(100) < euler(1000))

# ======================================================================= 1295
fs = {1: exp(t), 2: exp(t / 2), 3: exp(-t), 4: exp(-t / 2)}
check("1295 dérivées", egal(sp.diff(fs[1], t), exp(t)) and egal(sp.diff(fs[2], t), exp(t / 2) / 2)
      and egal(sp.diff(fs[3], t), -exp(-t)) and egal(sp.diff(fs[4], t), -exp(-t / 2) / 2))
check("1295 valeurs en 0", all(fs[i].subs(t, 0) == 1 for i in fs))
check("1295 tangentes", egal(1 + sp.diff(fs[1], t).subs(t, 0) * t, t + 1)
      and egal(1 + sp.diff(fs[2], t).subs(t, 0) * t, t / 2 + 1))
check("1295 f1(2) > f2(2)", float(fs[1].subs(t, 2)) > float(fs[2].subs(t, 2)))
check("1295 f3(-2) > f4(-2)", float(fs[3].subs(t, -2)) > float(fs[4].subs(t, -2)))
check("1295 symétrie", egal(fs[1].subs(t, -t), fs[3]))
check("1295 inéquation", sp.solveset(exp(t / 2) <= exp(-t), t, sp.S.Reals) == sp.Interval(-sp.oo, 0))
# courbes de la figure : C1 = f4 (décroissante, la moins raide), C2 = f1, C3 = f3, C4 = f2
check("1295 figure : e^{0,5·2,6} ≈ 3,67", arrondi(math.exp(1.3), 3.67, 5e-3) and arrondi(math.exp(1.65), 5.21, 5e-3))

# ======================================================================= 1300
N = 1000 * exp(sp.Rational(1, 50) * t)
check("1300 N(0)", N.subs(t, 0) == 1000)
check("1300 N(50) = 1000e", egal(N.subs(t, 50), 1000 * E) and arrondi(1000 * E, 2718, 0.5))
check("1300 N'", egal(sp.diff(N, t), 20 * exp(t / 50)) and egal(sp.diff(N, t), N / 50))
check("1300 raison", egal(N.subs(t, n + 1), exp(sp.Rational(1, 50)) * N.subs(t, n)))
check("1300 e^{0,02} ≈ 1,0202", arrondi(exp(0.02), 1.0202, 5e-5))
check("1300 taux 2,02 %", arrondi(exp(0.02) - 1, 0.0202, 5e-5))
Nf = lambda tt: 1000 * math.exp(0.02 * tt)
check("1300 N(34) ≈ 1974, N(35) ≈ 2014", arrondi(Nf(34), 1974, 0.5) and arrondi(Nf(35), 2014, 0.5))
tt = 0
while 1000 * math.exp(0.02 * tt) < 2000:
    tt += 1
check("1300 programme → 35", tt == 35)
check("1300 N(115) ≈ 9974, N(116) ≈ 10176", arrondi(Nf(115), 9974, 0.5) and arrondi(Nf(116), 10176, 0.5))
tt = 0
while 1000 * math.exp(0.02 * tt) <= 10000:
    tt += 1
check("1300 seuil 10 000 → 116", tt == 116)
check("1300 figure N(120) < 12 000", Nf(120) < 12000)

# ======================================================================= 1296
C = 4 * t * exp(-t / 2)
check("1296 C(0)", C.subs(t, 0) == 0)
check("1296 C'", egal(sp.diff(C, t), (4 - 2 * t) * exp(-t / 2)))
check("1296 C(2) = 8/e", egal(C.subs(t, 2), 8 / E) and arrondi(8 / E, 2.94, 5e-3))
check("1296 C(10) = 40e^{-5}", egal(C.subs(t, 10), 40 * exp(-5)) and arrondi(40 * exp(-5), 0.27, 5e-3))
check("1296 tangente y = 4t", egal(sp.diff(C, t).subs(t, 0), 4))
Cf = lambda tt: 4 * tt * math.exp(-tt / 2)
check("1296 tableau 0,7 / 0,8", arrondi(Cf(0.7), 1.97, 5e-3) and arrondi(Cf(0.8), 2.15, 5e-3))
check("1296 tableau 4,3 / 4,4", arrondi(Cf(4.3), 2.004, 5e-4) and arrondi(Cf(4.4), 1.95, 5e-3))
t1 = sp.nsolve(C - 2, t, 0.7)
t2 = sp.nsolve(C - 2, t, 4.3)
check("1296 t1 ∈ ]0,7 ; 0,8[", 0.7 < t1 < 0.8 and arrondi(t1, 0.71, 5e-3))
check("1296 t2 ∈ ]4,3 ; 4,4[", 4.3 < t2 < 4.4 and arrondi(t2, 4.31, 5e-3))
check("1296 durée ≈ 3,6 h", arrondi(t2 - t1, 3.6, 0.05))
check("1296 figure t1, t2", arrondi(t1, 0.7148, 1e-4) and arrondi(t2, 4.3066, 1e-4))

# ======================================================================= nouveau-1
A = 5000 * exp(-t / 5)
check("n1 A(0)", A.subs(t, 0) == 5000)
check("n1 A(5)", egal(A.subs(t, 5), 5000 / E) and arrondi(5000 / E, 1839, 0.5))
check("n1 A'", egal(sp.diff(A, t), -1000 * exp(-t / 5)) and egal(sp.diff(A, t), -A / 5))
check("n1 raison", egal(A.subs(t, n + 1), exp(sp.Rational(-1, 5)) * A.subs(t, n)))
check("n1 e^{-0,2} ≈ 0,8187 ≈ 0,819", arrondi(exp(-0.2), 0.8187, 5e-5) and arrondi(exp(-0.2), 0.819, 5e-4))
check("n1 taux ≈ -18,1 %", arrondi(exp(-0.2) - 1, -0.181, 5e-4) and arrondi(exp(-0.2) - 1, -0.1813, 5e-5))
check("n1 A(t+5) = e^{-1} A(t)", egal(A.subs(t, t + 5), exp(-1) * A))
Af = lambda tt: 5000 * math.exp(-0.2 * tt)
check("n1 A(3) ≈ 2744, A(4) ≈ 2247", arrondi(Af(3), 2744, 0.5) and arrondi(Af(4), 2247, 0.5))
nn = 0
while 5000 * math.exp(-0.2 * nn) > 2500:
    nn += 1
check("n1 programme → 4", nn == 4)
check("n1 A(11) ≈ 554, A(12) ≈ 454", arrondi(Af(11), 554, 0.5) and arrondi(Af(12), 454, 0.5))
nn = 0
while 5000 * math.exp(-0.2 * nn) > 500:
    nn += 1
check("n1 seuil 10 % → 12", nn == 12)
check("n1 figure A(4) = 2246,64", arrondi(Af(4), 2246.64, 5e-3))

# ======================================================================= nouveau-2
check("n2 A1", egal(sp.diff(exp(x) * exp(-x), x), 0))
check("n2 B1", egal(sp.diff(exp(x + b) * exp(-x), x), 0) and egal((exp(x + b) * exp(-x)).subs(x, 0), exp(b)))
check("n2 C1", egal(exp(x / 2) ** 2, exp(x)))
check("n2 C3", egal(exp(2 * a), exp(a) ** 2) and egal(exp(3 * a), exp(a) ** 3))

# ======================================================================= figures (valeurs placées)
check("fig cours_courbe (1 ; e)", arrondi(E, 2.71828, 1e-5))
check("fig cours_etude min", arrondi((2 * -0.5 - 1) * math.exp(-0.5), -1.21306, 1e-5)
      and arrondi(-5 * math.exp(-2), -0.67668, 1e-5))
check("fig cours_modele m(7)", arrondi(m(7), 49.66, 5e-3))
check("fig ex1294 min", arrondi(-math.exp(-1), -0.36788, 1e-5))
check("fig ex1292 points", arrondi(22 * math.exp(-5), 0.14823, 1e-5) and arrondi(6 * math.exp(-3), 0.29872, 1e-5)
      and arrondi(-2 * math.e, -5.43656, 1e-5) and arrondi(math.exp(2), 7.38906, 1e-5))
check("fig ex1300 points", arrondi(Nf(35), 2013.75, 5e-3) and arrondi(Nf(50), 2718.28, 5e-3))
check("fig ex1296 max", arrondi(8 / math.e, 2.94304, 1e-5))

print(f"{OK} contrôles OK, {len(KO)} erreur(s)")
sys.exit(1 if KO else 0)
