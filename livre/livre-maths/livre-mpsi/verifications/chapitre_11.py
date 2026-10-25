# -*- coding: utf-8 -*-
"""Vérifications du chapitre 11 — Analyse asymptotique."""
import math
from math import (isclose, sqrt, log, exp, sin, cos, tan, pi, factorial, comb,
                  atan)

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

x = sp.symbols("x")

def dl(expr, n):
    return sp.series(expr, x, 0, n).removeO()

# --- Exercices 1-2 : équivalents et limites ---------------------------
check("ex1 1−cos x ~ x²/2", sp.limit((1 - sp.cos(x))/(x**2/2), x, 0) == 1)
check("ex1 √(x²+x) ~ x en +∞", sp.limit(sp.sqrt(x**2 + x)/x, x, sp.oo) == 1)
check("ex2 sin3x/tan5x", sp.limit(sp.sin(3*x)/sp.tan(5*x), x, 0) == sp.Rational(3, 5))
check("ex2 x ln(1+1/x)", sp.limit(x*sp.ln(1 + 1/x), x, sp.oo) == 1)
check("ex2 (e^{2x}−1)/sin x", sp.limit((sp.exp(2*x) - 1)/sp.sin(x), x, 0) == 2)
# --- Exercice 3 : DL usuels -------------------------------------------
check("ex3 e^x ordre 3", dl(sp.exp(x), 4) == 1 + x + x**2/2 + x**3/6)
check("ex3 cos ordre 4", dl(sp.cos(x), 5) == 1 - x**2/2 + x**4/24)
check("ex3 ln(1+x) ordre 3", dl(sp.ln(1 + x), 4) == x - x**2/2 + x**3/3)
check("ex3 √(1+x) ordre 2", dl(sp.sqrt(1 + x), 3) == 1 + x/2 - x**2/8)
check("ex3 1/(1−x) ordre 3", dl(1/(1 - x), 4) == 1 + x + x**2 + x**3)
# --- Exercice 4 -------------------------------------------------------
check("ex4 e^x sin x ordre 3", dl(sp.exp(x)*sp.sin(x), 4) == x + x**2 + x**3/3)
check("ex4 cos²x ordre 4", dl(sp.cos(x)**2, 5) == 1 - x**2 + x**4/3)
# --- Exercice 5 -------------------------------------------------------
check("ex5 tan ordre 3", dl(sp.tan(x), 4) == x + x**3/3)
check("ex5 1/(1+e^x) ordre 2", dl(1/(1 + sp.exp(x)), 3) == sp.Rational(1, 2) - x/4)
check("ex5 ln(cos x) ordre 3", dl(sp.ln(sp.cos(x)), 4) == -x**2/2)
# --- Exercice 6 -------------------------------------------------------
check("ex6 arctan ordre 5", dl(sp.atan(x), 6) == x - x**3/3 + x**5/5)
check("ex6 ln(1+x²) ordre 4", dl(sp.ln(1 + x**2), 5) == x**2 - x**4/2)
# --- Exercice 7 -------------------------------------------------------
check("ex7 e^x au-dessus de 1+x", all(exp(t) >= 1 + t for t in [-0.5, -0.1, 0.1, 0.5]))
check("ex7 ln(1+x) au-dessous de x", all(log(1 + t) <= t for t in [-0.5, 0.3, 1.0]))
check("ex7 sin traverse en 0", (sin(0.1) - 0.1) < 0 < (sin(-0.1) - (-0.1)))
# --- Exercice 8 -------------------------------------------------------
check("ex8 √(n+1)−√n ~ 1/(2√n)",
      all(isclose((sqrt(n + 1) - sqrt(n))*2*sqrt(n), 1, rel_tol=2e-2/sqrt(n) + 1e-3)
          for n in [100, 10000]))
check("ex8 sin(1/n) ~ 1/n", isclose(sin(1e-4)*1e4, 1, rel_tol=1e-8))
# --- Exercice 9 -------------------------------------------------------
check("ex9 (cos x)^{1/x²}", sp.limit(sp.cos(x)**(1/x**2), x, 0) == sp.exp(sp.Rational(-1, 2)))
check("ex9 ((1+x)^{1/x}−e)/x", sp.limit(((1 + x)**(1/x) - sp.E)/x, x, 0) == -sp.E/2)
check("ex9 (tan−x)/(x−sin)", sp.limit((sp.tan(x) - x)/(x - sp.sin(x)), x, 0) == 2)
check("ex9 x−x²ln(1+1/x)", sp.limit(x - x**2*sp.ln(1 + 1/x), x, sp.oo) == sp.Rational(1, 2))
# --- Exercice 10 ------------------------------------------------------
h = sp.symbols("h")
check("ex10 √x en 4", sp.series(sp.sqrt(4 + h), h, 0, 3).removeO()
      == 2 + h/4 - h**2/64)
check("ex10 sin en π/6", sp.series(sp.sin(sp.pi/6 + h), h, 0, 3).removeO()
      == sp.Rational(1, 2) + sp.sqrt(3)/2*h - h**2/4)
# --- Exercice 11 ------------------------------------------------------
check("ex11 (e^x−1)/x", dl((sp.exp(x) - 1)/x, 3) == 1 + x/2 + x**2/6)
check("ex11 sin x/x", dl(sp.sin(x)/x, 4) == 1 - x**2/6)
# --- Exercice 12 ------------------------------------------------------
check("ex12 cos x + x²/2", dl(sp.cos(x) + x**2/2, 6) == 1 + x**4/24)
check("ex12 minimum local", all(cos(t) + t*t/2 > 1 for t in [-0.4, -0.1, 0.1, 0.4]))
check("ex12 x³+x⁴ pas d'extremum", (lambda f: f(-0.01) < 0 < f(0.01))(lambda t: t**3 + t**4))
# --- Exercice 13 ------------------------------------------------------
f13 = sp.sqrt(x**2 + x + 1)
dev = sp.series(f13, x, sp.oo, 2)
check("ex13 asymptote +∞", sp.limit(f13 - (x + sp.Rational(1, 2)), x, sp.oo) == 0)
check("ex13 au-dessus", all(sqrt(t*t + t + 1) > t + 0.5 for t in [10, 100, 1000]))
check("ex13 −∞", sp.limit(f13 - (-x - sp.Rational(1, 2)), x, -sp.oo) == 0)
# --- Exercice 14 (Stirling, admis) ------------------------------------
st = lambda n: sqrt(2*pi*n)*(n/math.e)**n
check("ex14 Stirling", all(isclose(factorial(n)/st(n), 1, rel_tol=1/(10*n))
      for n in [10, 30, 60]))
check("ex14 C(2n,n)", all(isclose(comb(2*n, n)*sqrt(pi*n)/4**n, 1, rel_tol=0.15/n)
      for n in [10, 40, 100]))
check("ex14 n!^{1/n} ~ n/e",
      isclose(exp(math.lgamma(1001)/1000)/(1000/math.e), 1, rel_tol=1e-2))
# --- Exercice 15 ------------------------------------------------------
u = lambda n: (1 + 1/n)**n
for n in [100, 1000, 10000]:
    approx = math.e*(1 - 1/(2*n) + 11/(24*n*n))
    check(f"ex15 n={n}", isclose(u(n), approx, rel_tol=5/n**3 + 1e-12))
check("ex15 série", sp.series(sp.exp(x*sp.ln(1 + 1/x)), x, sp.oo, 3)
      .removeO().expand().equals(sp.E - sp.E/(2*x) + 11*sp.E/(24*x**2)))
# --- Exercice 16 ------------------------------------------------------
# x + ln x = y : x_y = y − ln y + o(ln y)
for y in [100.0, 10000.0]:
    lo, hi = 1.0, y
    for _ in range(200):
        mid = (lo + hi)/2
        if mid + log(mid) < y:
            lo = mid
        else:
            hi = mid
    xy = (lo + hi)/2
    check(f"ex16 x~y (y={y})", isclose(xy/y, 1, rel_tol=2*log(y)/y))
    check(f"ex16 2e terme (y={y})", abs((xy - (y - log(y))))/log(y) < 0.2)
# --- Exercice 17 (tan x = x) ------------------------------------------
for n in [10, 100, 1000]:
    lo, hi = n*pi + 1e-9, n*pi + pi/2 - 1e-12
    for _ in range(200):
        mid = (lo + hi)/2
        if tan(mid) < mid:
            lo = mid
        else:
            hi = mid
    xn = (lo + hi)/2
    check(f"ex17 x_n (n={n})", isclose(xn, n*pi + pi/2 - 1/(n*pi), abs_tol=3/(n*n)))
# --- Exercice 18 ------------------------------------------------------
import mpmath  # noqa: F401  (si absent, remplacer par calcul direct)
def I18(n):
    # intégrale exacte par récurrence : I_n + I_{n+1} = 1/(n+1), I_0 = ln 2
    I = log(2)
    for k in range(n):
        I = 1/(k + 1) - I
    return I
check("ex18 récurrence", all(isclose(I18(n) + I18(n + 1), 1/(n + 1)) for n in [3, 7, 15]))
check("ex18 I_n ~ 1/(2n)", all(isclose(I18(n)*2*n, 1, rel_tol=2/n) for n in [20, 100, 400]))
check("ex18 décroissante positive", all(I18(n) > I18(n + 1) > 0 for n in [1, 5, 20]))
# --- Exercice 19 ------------------------------------------------------
a0, b0 = 3.0, 5.0
m19 = lambda t: ((a0**t + b0**t)/2)**(1/t)
check("ex19 limite 0 = moyenne géométrique", isclose(m19(1e-6), sqrt(a0*b0), rel_tol=1e-4))
check("ex19 limite +∞ = max", isclose(m19(200), b0, rel_tol=1e-2))
check("ex19 limite −∞ = min", isclose(m19(-200), a0, rel_tol=1e-2))
check("ex19 t=1 arithmétique", m19(1) == (a0 + b0)/2)
# --- Exercice 20 (Héron quantifiée) -----------------------------------
e0 = 2 - sqrt(2)
rho = e0/(2*sqrt(2))
u20 = 2.0
for n in range(6):
    err = u20 - sqrt(2)
    check(f"ex20 borne n={n}", err <= 2*sqrt(2)*rho**(2**n) + 1e-15)
    u20 = (u20 + 2/u20)/2
# --- Exercice 21 (u_{n+1}=sin u_n) ------------------------------------
u21 = 1.0
vals = []
for n in range(1, 20001):
    u21 = sin(u21)
    if n in (1000, 5000, 20000):
        vals.append((n, u21))
for n, v in vals:
    check(f"ex21 u_n~√(3/n) (n={n})", isclose(v*sqrt(n/3), 1, rel_tol=0.07))
check("ex21 1/u²−1/u'² → 1/3",
      isclose(1/sin(0.01)**2 - 1/0.01**2, 1/3, rel_tol=1e-3))
# --- Exercice 22 (x e^{1/x}) ------------------------------------------
f22 = x*sp.exp(1/x)
check("ex22 développement +∞", sp.limit((f22 - x - 1)*x, x, sp.oo) == sp.Rational(1, 2))
check("ex22 asymptote au-dessus", all(t*exp(1/t) > t + 1 for t in [2.0, 10.0, 100.0]))
check("ex22 0+ → +∞", sp.limit(f22, x, 0, "+") == sp.oo)
check("ex22 0− → 0", sp.limit(f22, x, 0, "-") == 0)
# --- Exercice 23 (Wallis) ---------------------------------------------
Iw = [pi/2, 1.0]
for n in range(2, 200):
    Iw.append((n - 1)/n*Iw[n - 2])
check("ex23 n·I_n·I_{n−1} = π/2", all(isclose(n*Iw[n]*Iw[n - 1], pi/2, rel_tol=1e-12)
      for n in [2, 7, 50, 150]))
check("ex23 I_{n+1}/I_n → 1", isclose(Iw[150]/Iw[149], 1, rel_tol=1e-2))
check("ex23 I_n ~ √(π/2n)", all(isclose(Iw[n]/sqrt(pi/(2*n)), 1, rel_tol=1/n)
      for n in [50, 150]))
check("ex23 I_{2n} formule", all(
    isclose(Iw[2*n], pi/2*comb(2*n, n)/4**n, rel_tol=1e-12) for n in [3, 10, 60]))
check("ex23 C(2n,n) sans Stirling", all(
    isclose(comb(2*n, n)*sqrt(pi*n)/4**n, 1, rel_tol=0.2/n) for n in [20, 80]))
# --- Exercice 24 (vers Stirling) --------------------------------------
for n in [10, 100, 1000]:
    lnfact = math.lgamma(n + 1)
    check(f"ex24 encadrement n={n}",
          n*log(n) - n + 1 <= lnfact <= n*log(n) - n + 1 + log(n))
check("ex24 n!^{1/n}/(n/e) → 1",
      isclose(exp(math.lgamma(1001)/1000)/(1000/math.e), 1, rel_tol=1e-2))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
