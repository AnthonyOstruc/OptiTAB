# -*- coding: utf-8 -*-
"""Vérifications du chapitre 4 — Techniques de calcul différentiel et intégral."""
import math
from math import isclose, pi, sqrt, exp, log, sin, cos, tan, atan, asin, acos

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

x, t, C = sp.symbols("x t C", real=True)

def deq(a, b):
    return sp.simplify(a - b) == 0

# --- Exercice 2 -------------------------------------------------------
check("ex2 x³−x impaire", deq((-x)**3 - (-x), -(x**3 - x)))
check("ex2 x²+cos x paire", deq((-x)**2 + sp.cos(-x), x**2 + sp.cos(x)))
check("ex2 période cos3x", deq(sp.cos(3*(x + 2*sp.pi/3)), sp.cos(3*x)))
check("ex2 période sin(x/2)", deq(sp.sin((x + 4*sp.pi)/2), sp.sin(x/2)))
check("ex2 période commune", deq(sp.cos(3*(x + 4*sp.pi)) + sp.sin((x + 4*sp.pi)/2),
                                 sp.cos(3*x) + sp.sin(x/2)))
# --- Exercice 3 -------------------------------------------------------
derivees = [
    (x**3 - 2*x + 1, 3*x**2 - 2),
    (x**2*sp.exp(x), (x**2 + 2*x)*sp.exp(x)),
    (sp.exp(x)/(x + 1), x*sp.exp(x)/(x + 1)**2),
    (sp.ln(1 + x**2), 2*x/(1 + x**2)),
    (sp.cos(x)**3, -3*sp.sin(x)*sp.cos(x)**2),
    (sp.sqrt(x**2 + 1), x/sp.sqrt(x**2 + 1)),
    (sp.tan(2*x), 2*(1 + sp.tan(2*x)**2)),
    (x*sp.ln(x) - x, sp.ln(x)),
]
for i, (f, fp) in enumerate(derivees):
    check(f"ex3 dérivée {i+1}", deq(sp.diff(f, x), fp))
# --- Exercice 4 -------------------------------------------------------
f = x**3 - 3*x + 1
check("ex4a f'", deq(sp.diff(f, x), 3*x**2 - 3))
check("ex4a extrema", f.subs(x, -1) == 3 and f.subs(x, 1) == -1)
g = x*sp.exp(-x)
check("ex4b g'", deq(sp.diff(g, x), (1 - x)*sp.exp(-x)))
check("ex4b max", deq(g.subs(x, 1), sp.exp(-1)))
check("ex4c min x+1/x", sp.diff(x + 1/x, x).subs(x, 1) == 0 and (1 + 1/1) == 2)
check("ex4c inégalité", all(u + 1/u >= 2 for u in [k/100 for k in range(1, 500)]))
# --- Exercice 5 -------------------------------------------------------
check("ex5 x ln x", sp.limit(x*sp.ln(x), x, 0, "+") == 0)
check("ex5 x²e^-x", sp.limit(x**2*sp.exp(-x), x, sp.oo) == 0)
check("ex5 lnx/√x", sp.limit(sp.ln(x)/sp.sqrt(x), x, sp.oo) == 0)
check("ex5 x^x", sp.limit(x**x, x, 0, "+") == 1)
check("ex5 e^x/x³", sp.limit(sp.exp(x)/x**3, x, sp.oo) == sp.oo)
# --- Exercice 6 -------------------------------------------------------
check("ex6 arcsin(1/2)", isclose(asin(0.5), pi/6))
check("ex6 arccos(−√2/2)", isclose(acos(-sqrt(2)/2), 3*pi/4))
check("ex6 arctan1, arctan√3", isclose(atan(1), pi/4) and isclose(atan(sqrt(3)), pi/3))
check("ex6 arcsin(sin 5π/6)", isclose(asin(sin(5*pi/6)), pi/6))
check("ex6 arccos(cos(−π/3))", isclose(acos(cos(-pi/3)), pi/3))
check("ex6 (arctan 2x)'", deq(sp.diff(sp.atan(2*x), x), 2/(1 + 4*x**2)))
check("ex6 (arcsin x²)'", deq(sp.diff(sp.asin(x**2), x), 2*x/sp.sqrt(1 - x**4)))
# --- Exercice 7 -------------------------------------------------------
primitives = [
    (x**3 + 1/x**2, x**4/4 - 1/x),
    (sp.exp(2*x), sp.exp(2*x)/2),
    (sp.cos(3*x), sp.sin(3*x)/3),
    (1/(2*x + 1), sp.ln(2*x + 1)/2),
    (x/(x**2 + 1), sp.ln(x**2 + 1)/2),
    (sp.sin(x)*sp.cos(x), sp.sin(x)**2/2),
    (1/(1 + 4*x**2), sp.atan(2*x)/2),
    (1/sp.sqrt(1 - x**2), sp.asin(x)),
]
for i, (f, F) in enumerate(primitives):
    check(f"ex7 primitive {i+1}", deq(sp.diff(F, x), f))
# --- Exercice 8 -------------------------------------------------------
y = sp.Function("y")
sol = sp.dsolve(y(x).diff(x) + 3*y(x), y(x), ics={y(0): 2})
check("ex8a", deq(sol.rhs, 2*sp.exp(-3*x)))
sol = sp.dsolve(y(x).diff(x) - 2*y(x), y(x), ics={y(0): -1})
check("ex8b", deq(sol.rhs, -sp.exp(2*x)))
# --- Exercice 9 -------------------------------------------------------
f = x/(1 + x**2)
check("ex9a f'", deq(sp.diff(f, x), (1 - x**2)/(1 + x**2)**2))
check("ex9a extrema", f.subs(x, 1) == sp.Rational(1, 2) and f.subs(x, -1) == sp.Rational(-1, 2))
g = sp.ln(x)/x
check("ex9b g'", deq(sp.diff(g, x), (1 - sp.ln(x))/x**2))
check("ex9b max en e", deq(g.subs(x, sp.E), 1/sp.E))
check("ex9b e^π>π^e", exp(pi) > pi**exp(1))
# --- Exercice 10 ------------------------------------------------------
for u in [k/40 - 0.95 for k in range(200)]:
    check("ex10a e^x≥1+x", exp(u) >= 1 + u - 1e-12)
    if u > -1:
        check("ex10b ln(1+x)≤x", log(1 + u) <= u + 1e-12)
    if u >= 0:
        check("ex10c", u - u*u/2 <= log(1 + u) + 1e-12)
# --- Exercice 11 ------------------------------------------------------
check("ex11 f(0)=1", (0 + exp(0)) == 1)
check("ex11 (f⁻¹)'(1)=1/2", isclose(1/(1 + exp(0)), 0.5))
# --- Exercice 12 ------------------------------------------------------
xx = sp.symbols("xx", real=True)
check("ex12a cos(arcsin x)", deq(sp.cos(sp.asin(xx)), sp.sqrt(1 - xx**2)))
check("ex12b arcsin+arccos", all(isclose(asin(u) + acos(u), pi/2)
                                 for u in [k/10 - 1 for k in range(21)]))
for u in [0.3, 1.5, 4.2]:
    check("ex12c x>0", isclose(atan(u) + atan(1/u), pi/2))
    check("ex12c x<0", isclose(atan(-u) + atan(-1/u), -pi/2))
for u in [k/20 - 2.4 for k in range(49)]:
    check("ex12d sin(2 arctan x)", isclose(sin(2*atan(u)), 2*u/(1 + u*u)))
# --- Exercice 13 ------------------------------------------------------
a, b = sp.symbols("a b", real=True)
check("ex13a ch²−sh²", deq(sp.cosh(x)**2 - sp.sinh(x)**2, 1))
check("ex13b sh(a+b)", deq(sp.sinh(a + b), sp.sinh(a)*sp.cosh(b) + sp.cosh(a)*sp.sinh(b)))
check("ex13c th'", deq(sp.diff(sp.tanh(x), x), 1 - sp.tanh(x)**2))
check("ex13d ch(ln(2+√3))=2",
      sp.simplify(sp.cosh(sp.ln(2 + sp.sqrt(3))).rewrite(sp.exp) - 2) == 0)
check("ex13d 1/(2+√3)", deq(1/(2 + sp.sqrt(3)), 2 - sp.sqrt(3)))
# --- Exercice 14 ------------------------------------------------------
prim2 = [
    (x*sp.exp(x**2), sp.exp(x**2)/2),
    (sp.tan(x), -sp.ln(sp.cos(x))),
    (1/(x*sp.ln(x)), sp.ln(sp.ln(x))),
    (sp.cos(x)*sp.sin(x)**3, sp.sin(x)**4/4),
    (x/sp.sqrt(1 + x**2), sp.sqrt(1 + x**2)),
    (sp.exp(x)/(1 + sp.exp(2*x)), sp.atan(sp.exp(x))),
]
for i, (f, F) in enumerate(prim2):
    check(f"ex14 primitive {i+1}", deq(sp.diff(F, x), f))
# --- Exercice 15 ------------------------------------------------------
check("ex15a", sp.integrate(x*sp.exp(x), (x, 0, 1)) == 1)
check("ex15b", sp.integrate(sp.ln(t), (t, 1, sp.E)) == 1)
check("ex15c", sp.integrate(t*sp.sin(t), (t, 0, sp.pi/2)) == 1)
check("ex15d", sp.integrate(x**2*sp.exp(x), (x, 0, 1)) == sp.E - 2)
# --- Exercice 16 ------------------------------------------------------
check("ex16a", deq(sp.integrate(1/(1 + sp.sqrt(x)), (x, 0, 1)), 2 - 2*sp.ln(2)))
check("ex16b", deq(sp.integrate(1/(sp.exp(t) + 1), (t, 0, 1)),
                   1 + sp.ln(2) - sp.ln(sp.E + 1)))
check("ex16c", sp.integrate(sp.cos(t)**3, (t, 0, sp.pi/2)) == sp.Rational(2, 3))
# --- Exercice 17 ------------------------------------------------------
sol = sp.dsolve(y(x).diff(x) + 2*y(x) - sp.exp(3*x), y(x), ics={y(0): 0})
check("ex17a", deq(sol.rhs, sp.exp(3*x)/5 - sp.exp(-2*x)/5))
yp = (sp.sin(x) - sp.cos(x))/2
check("ex17b particulière", deq(sp.diff(yp, x) - yp, sp.cos(x)))
yp = 1 + x*sp.exp(-x)
check("ex17c résonance", deq(sp.diff(yp, x) + yp, 1 + sp.exp(-x)))
# --- Exercice 18 ------------------------------------------------------
yp = x**2 + 1/x
check("ex18a", deq(sp.diff(yp, x) + yp/x, 3*x))
check("ex18a Cauchy", yp.subs(x, 1) == 2)
yg = (x + C)*sp.exp(x**2)
check("ex18b", deq(sp.diff(yg, x) - 2*x*yg, sp.exp(x**2)))
# --- Exercice 19 ------------------------------------------------------
om = sp.symbols("omega", positive=True)
A, B = sp.symbols("A B")
ygen = A*sp.cos(om*x) + B*sp.sin(om*x)
check("ex19a", deq(sp.diff(ygen, x, 2) + om**2*ygen, 0))
check("ex19b racines", sp.solve(sp.Symbol("r")**2 - 3*sp.Symbol("r") + 2) == [1, 2])
yg = (A + B*x)*sp.exp(-2*x)
check("ex19c double", deq(sp.diff(yg, x, 2) + 4*sp.diff(yg, x) + 4*yg, 0))
yg = sp.exp(-x)*(A*sp.cos(2*x) + B*sp.sin(2*x))
check("ex19d complexes", deq(sp.diff(yg, x, 2) + 2*sp.diff(yg, x) + 5*yg, 0))
yp = -sp.cos(2*x)/3
check("ex19e particulière", deq(sp.diff(yp, x, 2) + yp, sp.cos(2*x)))
yp = -x*sp.exp(x)
check("ex19f résonance", deq(sp.diff(yp, x, 2) - 3*sp.diff(yp, x) + 2*yp, sp.exp(x)))
# --- Exercice 20 ------------------------------------------------------
check("ex20a", isclose(atan(1/2) + atan(1/3), pi/4))
check("ex20b tan(2a)", isclose(tan(2*atan(1/5)), 5/12))
check("ex20b tan(4a)", isclose(tan(4*atan(1/5)), 120/119))
check("ex20b Machin", isclose(4*atan(1/5) - atan(1/239), pi/4))
check("ex20b borne", atan(1/5) < pi/8)
# --- Exercice 21 ------------------------------------------------------
for u in [k/50 for k in range(0, 300)]:
    check("ex21 encadrement", u - u**3/3 - 1e-12 <= atan(u) <= u + 1e-12)
check("ex21 limite", sp.limit(sp.atan(x)/x, x, 0) == 1)
# --- Exercice 22 ------------------------------------------------------
I = [sp.integrate(sp.sin(t)**n, (t, 0, sp.pi/2)) for n in range(8)]
check("ex22a I0 I1", I[0] == sp.pi/2 and I[1] == 1)
check("ex22b décroissante", all(sp.simplify(I[n] - I[n + 1]) >= 0 for n in range(7)))
for n in range(6):
    check(f"ex22c relation n={n}", deq(I[n + 2], sp.Rational(n + 1, n + 2)*I[n]))
check("ex22d", I[2] == sp.pi/4 and I[3] == sp.Rational(2, 3) and I[4] == 3*sp.pi/16)
# --- Exercice 23 ------------------------------------------------------
k23 = log(7/4)/10
T = lambda tt: 20 + 70*exp(-k23*tt)
check("ex23 T(0)=90", isclose(T(0), 90))
check("ex23 T(10)=60", isclose(T(10), 60))
t30 = log(7)/k23
check("ex23 T(t30)=30", isclose(T(t30), 30))
check("ex23 t30≈34,8", isclose(t30, 10*log(7)/log(7/4)) and 34.7 < t30 < 34.9)
# --- Exercice 24 ------------------------------------------------------
c = sp.symbols("c", real=True)
fexp = sp.exp(c*x)
yy = sp.symbols("yy", real=True)
check("ex24A équation fonctionnelle", deq(fexp.subs(x, x + yy), fexp*sp.exp(c*yy)))
ch = (sp.exp(x) + sp.exp(-x))/2
check("ex24B ch solution", deq(sp.diff(ch, x, 2), ch))
check("ex24B conditions", ch.subs(x, 0) == 1 and sp.diff(ch, x).subs(x, 0) == 0)
check("ex24B ch=cosh", deq(ch, sp.cosh(x)))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
