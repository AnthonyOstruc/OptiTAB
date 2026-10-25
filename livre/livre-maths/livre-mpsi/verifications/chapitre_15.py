# -*- coding: utf-8 -*-
"""Vérifications du chapitre 15 — Intégration."""
import math
from math import (isclose, sqrt, log, exp, sin, cos, pi, factorial, comb,
                  floor)

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

x, t = sp.symbols("x t", real=True)

# --- Exercice 1 : en escalier ------------------------------------------
# floor vaut k sur [k, k+1[ : integrale = somme des aires des marches
check("ex1 integrale de floor", sum(k*1 for k in range(3)) == 3)
frac = sum(float(sp.integrate(x - k, (x, k, k + 1))) for k in range(3))
check("ex1 partie fractionnaire", isclose(frac, 1.5))
# --- Exercice 2 : propriétés de base -----------------------------------
I2 = sp.integrate(1/(1 + x), (x, 0, 1))
check("ex2 encadrement", sp.Rational(1, 2) <= I2 <= 1 and I2 == sp.log(2))
val2 = float(sp.integrate(sp.sin(x**2), (x, 0, 1)))
check("ex2 inegalite triangulaire", abs(val2) <= 1 and isclose(val2, 0.3102683, abs_tol=1e-5))
check("ex2 Chasles |x|", sp.integrate(sp.Abs(x), (x, -1, 2)) == sp.Rational(5, 2))
# --- Exercice 3 : parité, périodicité ----------------------------------
check("ex3 impaire", sp.integrate(x**3*sp.cos(x), (x, -1, 1)) == 0)
check("ex3 cos^2 sur une periode", sp.integrate(sp.cos(x)**2, (x, 0, 2*sp.pi)) == sp.pi)
a = sp.symbols("a", real=True)
check("ex3 sin sur une periode", sp.simplify(
    sp.integrate(sp.sin(x), (x, a, a + 2*sp.pi))) == 0)
# --- Exercice 4 : valeur moyenne ---------------------------------------
check("ex4 moyenne de sin", sp.integrate(sp.sin(x), (x, 0, sp.pi))/sp.pi == 2/sp.pi)
check("ex4 moyenne de x^2", sp.integrate(x**2, (x, 0, 1)) == sp.Rational(1, 3))
# --- Exercice 5 : sommes de Riemann ------------------------------------
n = 200000
s5a = sum(1/(n + k) for k in range(1, n + 1))
check("ex5 somme 1/(n+k)", isclose(s5a, log(2), abs_tol=1e-5))
s5b = sum(k for k in range(1, n + 1))/n**2
check("ex5 somme k/n^2", isclose(s5b, 0.5, abs_tol=1e-4))
n = 20000
s5c = sum(n/(n*n + k*k) for k in range(1, n + 1))
check("ex5 somme n/(n^2+k^2)", isclose(s5c, pi/4, abs_tol=1e-4))
# --- Exercice 6 : derivee d'une integrale fonction de sa borne ---------
F6 = sp.integrate(sp.exp(-t**2), (t, 0, x))
check("ex6 derivee", sp.diff(F6, x) == sp.exp(-x**2))
G6 = sp.integrate(sp.sin(t), (t, 0, x**2))
check("ex6 borne composee", sp.simplify(sp.diff(G6, x) - 2*x*sp.sin(x**2)) == 0)
# --- Exercice 7 : Taylor reste integral --------------------------------
for n7 in [3, 5, 8]:
    Rn = math.e - sum(1/factorial(k) for k in range(n7 + 1))
    check(f"ex7 reste n={n7}", 0 < Rn <= math.e/factorial(n7 + 1))
# --- Exercice 8 : inegalite de Taylor-Lagrange -------------------------
check("ex8 |sin x - x|", all(abs(sin(v) - v) <= abs(v)**3/6
      for v in [-1.2, -0.3, 0.4, 2.0]))
check("ex8 cos", all(abs(cos(v) - 1 + v*v/2) <= v**4/24
      for v in [-1.0, 0.5, 1.5]))
check("ex8 sin(0.1)", abs(sin(0.1) - 0.1) <= 1e-3/6)
# --- Exercice 9 : continuite uniforme ----------------------------------
check("ex9 racine", all(abs(sqrt(u) - sqrt(v)) <= sqrt(abs(u - v))
      for u, v in [(0, 0.01), (1, 1.2), (4, 4.5), (0.0001, 0.01)]))
check("ex9 x^2 pas UC", all(abs((m + 1/m)**2 - m*m) >= 2 for m in [10, 100, 1000]))
a9 = [1/(2*k*pi + pi/2) for k in range(2, 5)]
b9 = [1/(2*k*pi) for k in range(2, 5)]
check("ex9 sin(1/x) oscille", all(
    abs(sin(1/u) - sin(1/v)) > 0.999 and abs(u - v) < 0.02
    for u, v in zip(a9, b9)))
# --- Exercice 10 : integrale nulle -------------------------------------
f10 = sp.Piecewise((1, sp.Eq(x, 0)), (0, True))
check("ex10 un point ne compte pas", sp.integrate(f10, (x, -1, 1)) == 0)
check("ex10 continue positive", sp.integrate(x**2, (x, -1, 1)) > 0)
# --- Exercice 11 : Riemann corsees -------------------------------------
n = 100000
s11a = sum(sqrt(k) for k in range(1, n + 1))/n**1.5
check("ex11 racines", isclose(s11a, 2/3, abs_tol=1e-4))
n = 20000
s11b = exp(sum(log(1 + k/n) for k in range(1, n + 1))/n)
check("ex11 produit -> 4/e", isclose(s11b, 4/math.e, rel_tol=1e-4))
s11c = sum(sin(k*pi/n) for k in range(1, n + 1))/n
check("ex11 sin(k pi/n)", isclose(s11c, 2/pi, abs_tol=1e-4))
# --- Exercice 12 : erreur lipschitzienne -------------------------------
for n12 in [10, 100]:
    Sn = sum(exp(k/n12) for k in range(n12))/n12
    err = abs((math.e - 1) - Sn)
    check(f"ex12 borne K(b-a)^2/(2n), n={n12}", err <= math.e/(2*n12))
# --- Exercice 13 : I_n = int x^n e^x -----------------------------------
Ivals = [float(sp.integrate(x**k*sp.exp(x), (x, 0, 1))) for k in range(8)]
check("ex13 recurrence", all(isclose(Ivals[k], math.e - k*Ivals[k - 1], abs_tol=1e-9)
      for k in range(1, 8)))
check("ex13 encadrement", all(1/(k + 1) <= Ivals[k] <= math.e/(k + 1)
      for k in range(8)))
I13 = Ivals[7]
for k in range(8, 300):
    I13 = math.e - k*I13
    if k == 299:
        break
# recalcul direct stable pour l'equivalent
import mpmath
mpmath.mp.dps = 30
I200 = float(mpmath.quad(lambda u: u**200*mpmath.e**u, [0, 1]))
check("ex13 n I_n -> e", isclose(200*I200, math.e, rel_tol=1e-2))
# --- Exercice 14 : int 1/(1+x^n) ---------------------------------------
for n14 in [50, 400]:
    J = float(mpmath.quad(lambda u: u**n14/(1 + u**n14), [0, 1]))
    check(f"ex14 n J_n -> ln 2 (n={n14})", isclose(n14*J, log(2), rel_tol=6/n14))
    K = float(mpmath.quad(lambda u: 1/(1 + u**n14), [0, 1]))
    check(f"ex14 K_n -> 1 (n={n14})", isclose(K, 1 - log(2)/n14, abs_tol=4/n14**2))
# --- Exercice 15 : e est irrationnel -----------------------------------
for n15 in [3, 5, 8]:
    An = sum(factorial(n15)//factorial(k) for k in range(n15 + 1))
    rn = factorial(n15)*math.e - An
    check(f"ex15 0 < n! e - A_n < 1 (n={n15})", 0 < rn < 1)
# ln 2 : reste integral = I_n du chapitre 11
for n15 in [10, 50]:
    Sn = sum((-1)**(k - 1)/k for k in range(1, n15 + 1))
    In = float(mpmath.quad(lambda u: u**n15/(1 + u), [0, 1]))
    check(f"ex15 ln2 reste (n={n15})", isclose(abs(log(2) - Sn), In, rel_tol=1e-9))
# --- Exercice 16 : rectangles contre trapezes --------------------------
def rect(n):
    return sum(exp(k/n) for k in range(n))/n
def trap(n):
    return sum((exp(k/n) + exp((k + 1)/n))/2 for k in range(n))/n
e1 = abs(math.e - 1 - rect(10)), abs(math.e - 1 - rect(100))
e2 = abs(math.e - 1 - trap(10)), abs(math.e - 1 - trap(100))
check("ex16 rectangles ordre 1", 8 < e1[0]/e1[1] < 12)
check("ex16 trapezes ordre 2", 80 < e2[0]/e2[1] < 120)
check("ex16 trapezes bien meilleurs", e2[1] < e1[1]/100)
# --- Exercice 17 : Cauchy-Schwarz --------------------------------------
lhs17 = float(sp.integrate(x*sp.exp(x), (x, 0, 1)))**2
rhs17 = float(sp.integrate(x**2, (x, 0, 1))*sp.integrate(sp.exp(2*x), (x, 0, 1)))
check("ex17 CS", lhs17 <= rhs17)
check("ex17 egalite colineaire", isclose(
    float(sp.integrate(x*(2*x), (x, 0, 1)))**2,
    float(sp.integrate(x**2, (x, 0, 1))*sp.integrate(4*x**2, (x, 0, 1)))))
# --- Exercice 18 : valeurs complexes -----------------------------------
check("ex18 int e^{it}", sp.integrate(sp.exp(sp.I*t), (t, 0, sp.pi)) == 2*sp.I)
check("ex18 module", 2 <= pi)
prim = sp.exp(x)*(sp.cos(x) + sp.sin(x))/2
check("ex18 primitive de e^x cos x",
      sp.simplify(sp.diff(prim, x) - sp.exp(x)*sp.cos(x)) == 0)
# --- Exercice 19 : la constante d'Euler --------------------------------
H = 0.0
prev = None
gamma = 0.5772156649015329
for k in range(1, 2001):
    H += 1/k
    u = H - log(k)
    if prev is not None and k > 1:
        check_ok = u <= prev + 1e-15
        if not check_ok:
            raise AssertionError("ex19 decroissance")
    prev = u
OK.append("ex19 u_n decroissante")
check("ex19 limite gamma", 0 < prev - gamma < 1/(2*2000) + 1e-4)
check("ex19 encadrement", gamma < prev < gamma + 1/2000)
# --- Exercice 20 : lemme de Riemann-Lebesgue ---------------------------
vals20 = []
for n20 in [10, 100, 1000]:
    v = float(sp.integrate(t**2*sp.sin(n20*t), (t, 0, 2*sp.pi)))
    vals20.append(abs(v))
    check(f"ex20 valeur exacte -4pi^2/n (n={n20})",
          isclose(v, -4*pi**2/n20, rel_tol=1e-9))
    check(f"ex20 borne C/n (n={n20})", abs(v) <= (4*pi**2 + 8*pi)/n20)
check("ex20 tend vers 0", vals20[2] < vals20[1] < vals20[0])
# --- Exercice 21 : Heine via lipschitz ---------------------------------
check("ex21 sin lipschitzienne", all(abs(sin(u) - sin(v)) <= abs(u - v)
      for u, v in [(0, 1), (2, 2.5), (-3, 3)]))
# --- Exercice 22 : orthogonal aux polynomes -> zeros -------------------
f22 = 6*x**2 - 6*x + 1
check("ex22 orthogonal a 1", sp.integrate(f22, (x, 0, 1)) == 0)
check("ex22 orthogonal a x", sp.integrate(x*f22, (x, 0, 1)) == 0)
roots22 = sp.solve(f22, x)
check("ex22 deux racines dans ]0,1[", all(0 < sp.re(r) < 1 for r in roots22)
      and len(roots22) == 2)
# --- Exercice 23 : aire de l'ellipse -----------------------------------
a23, b23 = sp.symbols("a23 b23", positive=True)
aire = sp.integrate(b23*sp.sin(t)*a23*sp.sin(t), (t, 0, 2*sp.pi))
check("ex23 aire = pi a b", sp.simplify(aire - sp.pi*a23*b23) == 0)
# --- Exercice 24 : Stirling, enfin démontré ----------------------------
def u24(m):
    return exp(math.lgamma(m + 1) - 0.5*log(m) - m*(log(m) - 1))
check("ex24 u_n decroit vers une limite", u24(10) > u24(100) > u24(1000) > 0)
check("ex24 limite = sqrt(2 pi)", isclose(u24(5000), sqrt(2*pi), rel_tol=1e-4))
for m in [10, 100]:
    d = log(u24(m)/u24(m + 1))
    check(f"ex24 |ln(u_n/u_n+1)| <= 1/(6n^2) (n={m})", abs(d) <= 1/(6*m*m))
lnC = math.lgamma(2001) - 2*math.lgamma(1001)
check("ex24 constante par Wallis", isclose(
    exp(lnC + 0.5*log(1000*pi) - 1000*log(4)), 1, rel_tol=1e-3))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
