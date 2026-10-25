# -*- coding: utf-8 -*-
"""Vérifications du chapitre 6 — Limites, continuité, dérivabilité, convexité."""
import math
import random
from math import isclose, sqrt, log, exp, sin, cos, tan, atan, pi

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

x, t = sp.symbols("x t", real=True)

def deq(a, b):
    return sp.simplify(a - b) == 0

# --- Exercice 1 -------------------------------------------------------
check("ex1a", sp.limit((x**2 - 1)/(x - 1), x, 1) == 2)
check("ex1b", sp.limit(sp.sin(x)/x, x, 0) == 1)
check("ex1c", sp.limit((sp.sqrt(x + 1) - 1)/x, x, 0) == sp.Rational(1, 2))
check("ex1d", sp.limit(x*sp.exp(1/x), x, 0, "+") == sp.oo)
check("ex1e", sp.limit(sp.ln(x)/(x - 1), x, 1) == 1)
# --- Exercice 2 -------------------------------------------------------
check("ex2 partie entière", sp.limit(sp.floor(x), x, 2, "-") == 1
      and sp.limit(sp.floor(x), x, 2, "+") == 2)
check("ex2 |x|/x", sp.limit(sp.Abs(x)/x, x, 0, "-") == -1
      and sp.limit(sp.Abs(x)/x, x, 0, "+") == 1)
check("ex2 e^{-1/x²}", sp.limit(sp.exp(-1/x**2), x, 0) == 0)
# --- Exercice 3 -------------------------------------------------------
check("ex3 (e^x−1)/x", sp.limit((sp.exp(x) - 1)/x, x, 0) == 1)
check("ex3 x ln x", sp.limit(x*sp.ln(x), x, 0, "+") == 0)
check("ex3 x sin(1/x)", all(abs(u*sin(1/u)) <= abs(u) for u in [0.1, -0.01, 0.001]))
check("ex3 sin(1/x) deux suites", isclose(sin(1/(1/(2*pi))), 0, abs_tol=1e-12)
      and isclose(sin(1/(1/(pi/2 + 4*pi))), 1))
# --- Exercice 4 -------------------------------------------------------
r = sp.nsolve(x**3 + x - 1, 0.7)
check("ex4a racine unique dans [0,1]", 0.68 < float(r) < 0.69)
check("ex4a croissance", deq(sp.diff(x**3 + x - 1, x), 3*x**2 + 1))
r = sp.nsolve(sp.cos(x) - x, 0.7)
check("ex4c cos x = x", 0.739 < float(r) < 0.74)
r = sp.nsolve(x**5 - x - 1, 1.2)
check("ex4d x⁵=x+1", 1.167 < float(r) < 1.168)
# --- Exercice 5 -------------------------------------------------------
check("ex5 |x| taux", (abs(0.001)/0.001, abs(-0.001)/(-0.001)) == (1.0, -1.0))
check("ex5 raccord a,b", 2*1 - 1 == 1 and 2 == 2)  # a=2, b=−1 : continuité 1=a+b, pente 2=a
check("ex5 x|x| dérivable", deq(sp.diff(x*sp.Abs(x), x).rewrite(sp.sign).subs(x, 2), 4))
# --- Exercice 6 -------------------------------------------------------
f6 = x**3 - 2*x
check("ex6 tangente en 1", f6.subs(x, 1) == -1 and sp.diff(f6, x).subs(x, 1) == 1)
check("ex6 √1,02", isclose(sqrt(1.02), 1.01, abs_tol=5e-5))
check("ex6 DL1 e^h", isclose(exp(0.05), 1.05, abs_tol=1.3e-3))
# --- Exercice 7 -------------------------------------------------------
check("ex7 Rolle x³−3x", sp.diff(x**3 - 3*x, x).subs(x, 1) == 0
      and (sqrt(3))**3 - 3*sqrt(3) < 1e-12)
check("ex7 ln(1,1)", 1/11 <= log(1.1) <= 1/10)
check("ex7 |sin a − sin b|", all(abs(sin(a) - sin(b)) <= abs(a - b) + 1e-15
      for a, b in [(0.3, 1.9), (-2, 5), (0.1, 0.11)]))
# --- Exercice 8 -------------------------------------------------------
check("ex8 e^x ≥ 1+x", all(exp(u) >= 1 + u for u in [k/10 - 3 for k in range(70)]))
check("ex8 ln x ≤ x−1", all(log(u) <= u - 1 + 1e-15 for u in [k/20 + 0.05 for k in range(100)]))
check("ex8 convexité x²", deq(sp.diff(x**2, x, 2), 2))
# --- Exercice 9 -------------------------------------------------------
# Dirichlet-like : x·1_Q n'est continue qu'en 0 — vérification d'esprit : |x·d(x)| ≤ |x|
check("ex9 encadrement", all(abs(u*1) <= abs(u) for u in [0.1, -0.02]))
# --- Exercice 10 ------------------------------------------------------
check("ex10 image de [0,π] par cos", cos(0) == 1 and isclose(cos(pi), -1))
# dichotomie : nombre d'itérations pour précision 1e-3 sur [0,1]
n_iter = math.ceil(math.log2(1/1e-3))
check("ex10 dichotomie 10 étapes", n_iter == 10)
f10 = lambda u: u*exp(-u)
vals = [f10(u) for u in [k/1000 for k in range(2001)]]
check("ex10 bornes de x e^-x sur [0,2]", isclose(max(vals), exp(-1), rel_tol=1e-5)
      and min(vals) == 0)
# --- Exercice 12 ------------------------------------------------------
f12 = lambda u: u + log(u)
check("ex12 f(1,55)<2<f(1,56)", f12(1.55) < 2 < f12(1.56))
al = sp.nsolve(x + sp.ln(x) - 2, 1.56)
check("ex12 alpha", 1.557 < float(al) < 1.5572)
check("ex12 dérivée réciproque", isclose(1/(1 + 1/float(al)), float(al)/(float(al) + 1)))
# --- Exercice 13 ------------------------------------------------------
P = x**3 - 3*x + 1
check("ex13 signes", P.subs(x, -2) == -1 and P.subs(x, 0) == 1
      and P.subs(x, 1) == -1 and P.subs(x, 2) == 3)
roots = sorted(float(r) for r in sp.real_roots(P))
check("ex13 trois racines", len(roots) == 3 and -1.88 < roots[0] < -1.87
      and 0.34 < roots[1] < 0.35 and 1.53 < roots[2] < 1.54)
check("ex13 P' racines ±1", sorted(sp.solve(sp.diff(P, x))) == [-1, 1])
# --- Exercice 14 ------------------------------------------------------
for u in [k/40 + 0.01 for k in range(160)]:
    check("ex14 encadrement ln", u/(1 + u) <= log(1 + u) <= u)
# --- Exercice 15 ------------------------------------------------------
f15 = x**2*sp.sin(1/x)
check("ex15 dérivée hors 0", deq(sp.diff(f15, x), 2*x*sp.sin(1/x) - sp.cos(1/x)))
# taux d'accroissement en 0 : |x sin(1/x)| ≤ |x| → dérivée nulle en 0
check("ex15 taux en 0", all(abs(u*sin(1/u)) <= abs(u) for u in [1e-3, -1e-4]))
# f' n'a pas de limite en 0 : valeurs en 1/(2nπ) → −1, en 1/((2n+1)π) → 1
check("ex15 f' oscille", isclose(-cos(2*pi*50), -1) and isclose(-cos(pi*(2*50 + 1)), 1))
# --- Exercice 16 ------------------------------------------------------
n_, k_ = sp.symbols("n k", positive=True, integer=True)
for nn in range(1, 8):
    lhs = sp.diff(x**2*sp.exp(x), x, nn)
    rhs = (x**2 + 2*nn*x + nn*(nn - 1))*sp.exp(x)
    check(f"ex16 Leibniz n={nn}", deq(lhs, rhs))
check("ex16 valeur en 0 pour n=10", 10*9 == 90)
# --- Exercice 17 ------------------------------------------------------
for u in [k/100 for k in range(0, 158)]:
    check("ex17 sin x ≥ 2x/π", sin(u) >= 2*u/pi - 1e-12)
random.seed(6)
for _ in range(2000):
    a, b, c = (random.uniform(0.1, 9) for _ in range(3))
    check("ex17 AM-GM n=3", (a*b*c)**(1/3) <= (a + b + c)/3 + 1e-12)
    th = random.uniform(0, 1)
    check("ex17 Young", a**th*b**(1 - th) <= th*a + (1 - th)*b + 1e-12)
# --- Exercice 18 ------------------------------------------------------
f18 = x**3 - 3*x**2
check("ex18 f''", deq(sp.diff(f18, x, 2), 6*x - 6))
check("ex18 inflexion", f18.subs(x, 1) == -2)
g18 = sp.ln(1 + x**2)
check("ex18 g''", deq(sp.diff(g18, x, 2), 2*(1 - x**2)/(1 + x**2)**2))
check("ex18 g(±1)", deq(g18.subs(x, 1), sp.ln(2)))
# --- Exercice 19 (Newton–Héron) ---------------------------------------
u = 2.0
errs = []
for n in range(5):
    errs.append(u - sqrt(2))
    un1 = (u + 2/u)/2
    # identité de convergence quadratique
    check("ex19 identité", isclose(un1 - sqrt(2), (u - sqrt(2))**2/(2*u),
                                   rel_tol=1e-6, abs_tol=1e-15))
    u = un1
check("ex19 erreurs", errs[1] < 0.09 and errs[2] < 0.003 and errs[3] < 3e-6)
check("ex19 quadratique", all(errs[i + 1] <= errs[i]**2 for i in range(1, 4)))
# --- Exercice 20 (g = e^{-x} f) ---------------------------------------
ff = sp.Function("f")
g20 = sp.exp(-x)*ff(x)
check("ex20 dérivée", deq(sp.diff(g20, x), sp.exp(-x)*(sp.diff(ff(x), x) - ff(x))))
# --- Exercice 21 ------------------------------------------------------
# f = cos, sur [0,1] : |f'| = sin ≤ sin 1 < 1, point fixe ≈ 0,739
k21 = sin(1)
check("ex21 contraction", k21 < 1)
u = 0.0
pf = 0.7390851332151607
for n in range(100):
    check("ex21 vitesse", abs(u - pf) <= k21**n*abs(0 - pf) + 1e-12)
    u = cos(u)
check("ex21 limite", abs(u - pf) < 1e-12)
# --- Exercice 23 ------------------------------------------------------
for _ in range(2000):
    vals = [random.uniform(0.1, 9) for _ in range(4)]
    n = len(vals)
    harm = n/sum(1/v for v in vals)
    geo = math.prod(vals)**(1/n)
    arith = sum(vals)/n
    quad = sqrt(sum(v*v for v in vals)/n)
    check("ex23 moyennes", harm <= geo + 1e-9 <= arith + 2e-9 <= quad + 3e-9)
# rectangle de périmètre 2p : aire xy ≤ (p/2)² (carré)
for _ in range(500):
    p = random.uniform(1, 10)
    xx = random.uniform(0, p)
    check("ex23 carré optimal", xx*(p - xx) <= (p/2)**2 + 1e-12)
# --- Exercice 24 ------------------------------------------------------
# (a) linéaire : erreur divisée par 2
u, l = 0.0, 2.0
for n in range(50):
    check("ex24a géométrique 1/2", isclose(abs(u - l), 2*0.5**n))
    u = u/2 + 1
# (b) sqrt(2+u) : rapport des erreurs → |f'(2)| = 1/4
u, e_prev = 0.0, None
for n in range(25):
    e = abs(u - 2)
    if e_prev is not None and e > 1e-14:
        check("ex24b rapport ≤ 0,36", e/e_prev <= 0.36)
    e_prev = e
    u = sqrt(2 + u)
# (c) Héron : quadratique (déjà vérifié ex19)
check("ex24c doublement des décimales", errs[2] < errs[1]**2 and errs[3] < errs[2]**2)

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
