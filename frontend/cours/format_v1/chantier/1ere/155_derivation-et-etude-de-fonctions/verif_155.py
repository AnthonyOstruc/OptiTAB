# -*- coding: utf-8 -*-
"""Vérification de tous les résultats de la notion 155 (Dérivation), avec sympy."""
import sympy as sp

x, h, r, t = sp.symbols("x h r t", real=True)
X = sp.Symbol("X")
OK = []


def eq(a, b, msg):
    assert sp.simplify(sp.sympify(a) - sp.sympify(b)) == 0, (msg, a, b)
    OK.append(msg)


def d(f, v=x):
    return sp.diff(f, v)


def signes(fp, points, interieur):
    """Vérifie le signe de fp en des points intérieurs des intervalles."""
    for p, s in zip(points, interieur):
        val = fp.subs(x, p)
        assert (val > 0) == (s == "+"), (fp, p, s)


# ---------------------------------------------------------------- cours
eq(sp.limit(((1 + h)**2 - 1) / h, h, 0), 2, "cours f'(1)=2")
eq(sp.expand(2 * (x - 1) + 1), 2 * x - 1, "cours tangente")
eq(d((2*x + 1) * (x**2 - 3)), 6*x**2 + 2*x - 6, "cours produit")
eq(d((3*x - 1) / (x + 2)), 7 / (x + 2)**2, "cours quotient")
eq(d(sp.sqrt(4*x + 1)), 2 / sp.sqrt(4*x + 1), "cours racine ax+b")
eq(d((2*x - 5)**3), 6 * (2*x - 5)**2, "cours cube ax+b")
eq(d(x**3 - 3*x), 3 * (x - 1) * (x + 1), "cours x^3-3x")
eq((x**3 - 3*x).subs(x, -1), 2, "f(-1)=2"); eq((x**3 - 3*x).subs(x, 1), -2, "f(1)=-2")
eq(d(x + 1/x - 2), (x - 1) * (x + 1) / x**2, "cours inégalité"); eq((x + 1/x - 2).subs(x, 1), 0, "d(1)=0")
assert sp.limit(sp.sqrt(h) / h, h, 0, "+") == sp.oo; OK.append("racine non dérivable")

# ---------------------------------------------------------------- 1366
f = x**2
eq((f.subs(x, 4) - f.subs(x, 3)) / 1, 7, "1366 taux 7")
for b, v in [(sp.Rational(7, 2), sp.Rational(13, 2)), (sp.Rational(31, 10), sp.Rational(61, 10)), (sp.Rational(301, 100), sp.Rational(601, 100))]:
    eq((f.subs(x, b) - 9) / (b - 3), v, f"1366 taux {b}")
eq(sp.simplify(((3 + h)**2 - 9) / h), 6 + h, "1366 6+h")
g = x**2 / 2 + 3
eq(g.subs(x, 2), 5, "g(2)=5"); eq(d(g).subs(x, 2), 2, "g'(2)=2"); eq(2*4 + 1, 9, "B sur T")

# ---------------------------------------------------------------- 1365 (courbe de la figure)
F = sp.Rational(5, 54)*x**3 + sp.Rational(1, 9)*x**2 - sp.Rational(19, 18)*x + sp.Rational(25, 27)
eq(F.subs(x, -1), 2, "C"); eq(F.subs(x, 2), 0, "D")
eq(d(F).subs(x, -1), -1, "f'(-1)"); eq(d(F).subs(x, 2), sp.Rational(1, 2), "f'(2)")
eq(-1*(1 + 1) + 2, 0, "T_C par (1;0)"); eq(sp.Rational(1, 2)*0 - 1, -1, "T_D par (0;-1)")

# ---------------------------------------------------------------- 1369
eq(d(3*x**3 - 5*x**2 + 7*x - 2), 9*x**2 - 10*x + 7, "A a")
eq(d(2/x - x**2), -2/x**2 - 2*x, "A b")
eq(d(x**2 * (3*x - 1)), 9*x**2 - 2*x, "A c")
eq(d((x**2 + 1)/x), 1 - 1/x**2, "A d")
eq(d((2*x + 5)**3), 6*(2*x + 5)**2, "A e")
f = 2*x**2 - 8*x + 5
eq(d(f), 4*x - 8, "B1"); eq(f.subs(x, 3), -1, "B2"); eq(d(f).subs(x, 3), 4, "B2'")
eq(sp.expand(4*(x - 3) - 1), 4*x - 13, "B3"); eq(f.subs(x, 2), -3, "B4")
g = -x**3 + 3*x**2 + 9*x - 5
eq(d(g), -3*(x + 1)*(x - 3), "C1"); eq(g.subs(x, -1), -10, "C3a"); eq(g.subs(x, 3), 22, "C3b")
eq(g.subs(x, -4), 71, "g(-4)"); eq(g.subs(x, 6), -59, "g(6)")
signes(d(g), [-2, 0, 4], ["-", "+", "-"])

# ---------------------------------------------------------------- 1371
eq(d(4*x**3 - 5*x**2 + 2*x - 9), 12*x**2 - 10*x + 2, "A1")
eq(d((2*x + 3)*(x - 1)), 4*x + 1, "A2"); eq(d((3*x + 1)/x), -1/x**2, "A3")
eq(d((5*x - 2)**3), 15*(5*x - 2)**2, "A4")
f = -x**2 + 6*x - 5
eq(d(f), -2*x + 6, "B1"); eq(f.subs(x, 1), 0, "B2"); eq(d(f).subs(x, 1), 4, "B2'"); eq(f.subs(x, 3), 4, "B3")
g = 2*x**3 - 3*x**2 - 12*x + 7
eq(d(g), 6*(x + 1)*(x - 2), "C1"); eq(g.subs(x, -1), 14, "C3"); eq(g.subs(x, 2), -13, "C3'")
signes(d(g), [-2, 0, 3], ["+", "-", "+"])

# ---------------------------------------------------------------- 1373
A = x*(20 - x)
eq(d(A), 20 - 2*x, "A'"); eq(A.subs(x, 10), 100, "Amax")
C = x**2 - 10*x + 50
eq(d(C), 2*x - 10, "C'"); eq(C.subs(x, 0), 50, "C0"); eq(C.subs(x, 5), 25, "C5"); eq(C.subs(x, 15), 125, "C15")
s = -t**2 + 6*t + 2
eq(d(s, t), -2*t + 6, "v"); eq(s.subs(t, 3), 11, "smax"); eq(s.subs(t, 0), 2, "s0")

# ---------------------------------------------------------------- 1367
eq(d(5*x**2 + 3*x - 7), 10*x + 3, "1a"); eq(d(x**3 - 2*x**2 + 4), 3*x**2 - 4*x, "1b"); eq(d(1/x + x), 1 - 1/x**2, "1c")
f = x**2 - 4*x + 3
eq(f.subs(x, 2), -1, "2b"); eq(d(f).subs(x, 2), 0, "2b'")
eq(d(x*(2*x + 1)), 4*x + 1, "3a"); eq(d((x + 2)/x), -2/x**2, "3b"); eq(d((3*x - 1)**2), 18*x - 6, "3c")

# ---------------------------------------------------------------- 1372
eq(d((2*x + 5)**4), 8*(2*x + 5)**3, "1a"); eq(d((4 - x)**5), -5*(4 - x)**4, "1b")
eq(d(sp.sqrt(3*x + 6)), 3/(2*sp.sqrt(3*x + 6)), "1c"); eq(d(1/(2*x - 1)), -2/(2*x - 1)**2, "1d")
eq(d(x**2*(x + 1)), 3*x**2 + 2*x, "2a"); eq(d((3*x - 2)*(x**2 + 1)), 9*x**2 - 4*x + 3, "2b")
eq(d(x**2/(x + 1)), x*(x + 2)/(x + 1)**2, "2c")
f = (x**2 - 3)**2
eq(sp.expand(f), x**4 - 6*x**2 + 9, "3a"); eq(d(f), 4*x*(x**2 - 3), "3a'")
assert set(sp.solve(d(f), x)) == {0, sp.sqrt(3), -sp.sqrt(3)}
eq(f.subs(x, 0), 9, "f(0)"); eq(f.subs(x, sp.sqrt(3)), 0, "f(r3)")
signes(d(f), [-2, -1, 1, 2], ["-", "+", "-", "+"])

# ---------------------------------------------------------------- 1368
f = x**3 - 6*x**2 + 9*x + 1
eq(d(f), 3*(x - 1)*(x - 3), "1b"); eq(f.subs(x, 1), 5, "f1"); eq(f.subs(x, 3), 1, "f3"); eq(f.subs(x, 5), 21, "f5")
signes(d(f), [0, 2, 4], ["+", "-", "+"])

# ---------------------------------------------------------------- 1370
f = x**3 - 6*x**2 + 12*x - 3
eq(d(f), 3*(x - 2)**2, "B2"); eq(f.subs(x, 2), 5, "f(2)")
V = x**2*(10 - x)
eq(sp.expand(V), 10*x**2 - x**3, "C1"); eq(d(V), x*(20 - 3*x), "C2")
eq(V.subs(x, sp.Rational(20, 3)), sp.Rational(4000, 27), "Vmax")
assert round(4000/27, 1) == 148.1 and round(20/3, 2) == 6.67
eq(V.subs(x, 2), 32, "V2"); eq(V.subs(x, 8), 128, "V8")

# ---------------------------------------------------------------- 1374
eq(d(3*x**4 - 2*x**3 + x - 5), 12*x**3 - 6*x**2 + 1, "B1")
eq(d((x**2 - 1)*(2*x + 3)), 6*x**2 + 6*x - 2, "B2")
eq(d((2*x - 1)/(x + 2)), 5/(x + 2)**2, "B3")
eq(d(sp.sqrt(5 - 2*x)), -1/sp.sqrt(5 - 2*x), "B4")
f = x**3 - 3*x**2 + 4
eq(d(f), 3*x*(x - 2), "C1"); eq(f.subs(x, 0), 4, "f0"); eq(f.subs(x, 2), 0, "f2")
eq(f.subs(x, 1), 2, "f1"); eq(d(f).subs(x, 1), -3, "f'1"); eq(sp.expand(-3*(x - 1) + 2), -3*x + 5, "C4")
rp = sp.Symbol("r", positive=True)
hh = 500/(sp.pi*rp**2)
S = 2*sp.pi*rp**2 + 2*sp.pi*rp*hh
eq(S, 2*sp.pi*rp**2 + 1000/rp, "D2"); eq(d(S, rp), 4*(sp.pi*rp**3 - 250)/rp**2, "D3")
r0 = (250/sp.pi)**sp.Rational(1, 3)
assert abs(float(r0) - 4.30) < 0.005, float(r0)
eq(hh.subs(rp, r0), 2*r0, "D5"); assert abs(2*float(r0) - 8.60) < 0.01

# ---------------------------------------------------------------- nouveau-1
f = x**3
eq(sp.expand(d(f).subs(x, 1)*(x - 1) + f.subs(x, 1)), 3*x - 2, "T")
dd = x**3 - 3*x + 2
eq(d(dd), 3*(x - 1)*(x + 1), "d'"); eq(dd.subs(x, -2), 0, "d(-2)"); eq(dd.subs(x, -1), 4, "d(-1)"); eq(dd.subs(x, 1), 0, "d(1)")
eq(sp.expand((x - 1)**2*(x + 2)), dd, "factorisation")
signes(d(dd), [-1.5, 0, 2], ["+", "-", "+"])

# ---------------------------------------------------------------- nouveau-2
f = x + 4/x
eq(d(f), (x - 2)*(x + 2)/x**2, "f'"); eq(f.subs(x, 1), 5, "f1"); eq(f.subs(x, 2), 4, "f2"); eq(f.subs(x, 6), sp.Rational(20, 3), "f6")
xp = sp.Symbol("xp", positive=True)
eq(d(xp*sp.sqrt(xp), xp), sp.Rational(3, 2)*sp.sqrt(xp), "g'")
eq(sp.limit(h*sp.sqrt(h)/h, h, 0, "+"), 0, "g'(0)")
eq(1/sp.sqrt(sp.Rational(1, 100)), 10, "h=0,01"); eq(1/sp.sqrt(sp.Rational(1, 10000)), 100, "h=0,0001")

# ---------------------------------------------------------------- nouveau-3 (courbe de f' tracée)
fp = (x + 1)*(x - 3)/3
eq(fp.subs(x, -1), 0, "f'(-1)"); eq(fp.subs(x, 0), -1, "f'(0)"); eq(fp.subs(x, 3), 0, "f'(3)")
eq(fp.subs(x, -3), 4, "f'(-3)"); eq(fp.subs(x, 4), sp.Rational(5, 3), "f'(4)")
signes(fp, [-2, 0, 3.5], ["+", "-", "+"])

# ---------------------------------------------------------------- figures
eq((sp.Rational(1, 2)*x**2 + 1).subs(x, sp.Rational(16, 10)), sp.Rational(228, 100), "M3 sécantes")
eq((sp.Rational(1, 2)*x**2 + 1).subs(x, sp.Rational(22, 10)), sp.Rational(342, 100), "M2 sécantes")

# ---------------------------------------------------------------- finition 2026-11-02
def tangente(f, a):
    return sp.expand(d(f).subs(x, a)*(x - a) + f.subs(x, a))

# cours : enclos le long d'un mur
A = x*(20 - 2*x)
eq(sp.expand(A), 20*x - 2*x**2, "enclos A"); eq(d(A), 20 - 4*x, "enclos A'")
eq(sp.solve(d(A), x)[0], 5, "enclos x=5"); eq(A.subs(x, 5), 50, "enclos 50")
signes(d(A), [1, 8], ["+", "-"])
eq(A.subs(x, 0), 0, "A(0)"); eq(A.subs(x, 10), 0, "A(10)")
# cours : figure x + 1/x et y = 2
eq((x + 1/x).subs(x, 1), 2, "x+1/x en 1")
# 1369 B et C (figures)
f = 2*x**2 - 8*x + 5
eq(tangente(f, 3), 4*x - 13, "fig 1369 T"); eq(tangente(f, 2), -3, "fig 1369 tangente horizontale")
g = -x**3 + 3*x**2 + 9*x - 5
eq(g.subs(x, -1), -10, "fig g(-1)"); eq(g.subs(x, 3), 22, "fig g(3)")
eq(g.subs(x, -4), 71, "g(-4)"); eq(g.subs(x, 6), -59, "g(6)")
# 1371 B et C (figures)
f = -x**2 + 6*x - 5
eq(tangente(f, 1), 4*x - 4, "fig 1371 T"); eq(tangente(f, 3), 4, "fig 1371 horizontale")
g = 2*x**3 - 3*x**2 - 12*x + 7
eq(g.subs(x, -1), 14, "fig g(-1)=14"); eq(g.subs(x, 2), -13, "fig g(2)=-13")
# 1373 : coût en centaines d'euros
C = x**2 - 10*x + 50
eq(C.subs(x, 5), 25, "C(5)"); eq(C.subs(x, 5)*100, 2500, "2500 euros"); eq(C.subs(x, 0), 50, "C(0)"); eq(C.subs(x, 15), 125, "C(15)")
s = -t**2 + 6*t + 2
eq(sp.diff(s, t).subs(t, 3), 0, "v(3)=0"); eq(s.subs(t, 3), 11, "s(3)=11"); eq(s.subs(t, 0), 2, "s(0)")
# 1367 (figure)
eq(tangente(x**2 - 4*x + 3, 2), -1, "fig 1367 y=-1")
# 1372 (figure)
f = (x**2 - 3)**2
eq(f.subs(x, 0), 9, "f(0)=9"); eq(f.subs(x, sp.sqrt(3)), 0, "f(√3)=0")
assert set(sp.solve(d(f), x)) == {0, sp.sqrt(3), -sp.sqrt(3)}; OK.append("f'=0")
# 1370 B (figure) : (x-2)^3 + 5
f = x**3 - 6*x**2 + 12*x - 3
eq(sp.expand((x - 2)**3 + 5), f, "forme (x-2)^3+5"); eq(tangente(f, 2), 5, "fig 1370 y=5")
V = 10*x**2 - x**3
eq(V.subs(x, sp.Rational(20, 3)), sp.Rational(4000, 27), "Vmax"); assert abs(float(sp.Rational(4000, 27)) - 148.148) < 0.001
eq(V.subs(x, 2), 32, "V(2)"); eq(V.subs(x, 8), 128, "V(8)")
# 1374 C et D (figures)
f = x**3 - 3*x**2 + 4
eq(tangente(f, 1), -3*x + 5, "fig 1374 T"); eq(f.subs(x, 0), 4, "f(0)"); eq(f.subs(x, 2), 0, "f(2)")
S = 2*sp.pi*r**2 + 1000/r
r0 = (250/sp.pi)**sp.Rational(1, 3)
assert abs(float(r0) - 4.3012701) < 1e-6 and abs(float(S.subs(r, r0)) - 348.73) < 0.01; OK.append("S(r0) figure")
# nouveau-2 (figure)
eq((x + 4/x).subs(x, 6), sp.Rational(20, 3), "f(6)")

print(f"{len(OK)} vérifications : toutes justes.")
