# -*- coding: utf-8 -*-
"""Vérification de tous les résultats de la notion 172 (cours, fiche, exercices)."""
import sympy as sp
from sympy import Interval as I, Union as U, oo, S, Rational as R, sqrt, FiniteSet as F

x = sp.symbols("x", real=True)
ok = 0


def eq(a, b, msg):
    global ok
    a, b = sp.simplify(a), sp.simplify(b)
    assert a == b, f"{msg} : {a} != {b}"
    ok += 1


def sol(expr, dom=S.Reals):
    return sp.solveset(expr, x, dom)


# ---------------- cours / fiche
f = x**2 - 2*x - 3
g = x + 1
eq(f.subs(x, 4), 5, "f(4)")
eq(sol(sp.Eq(f, -3)), F(0, 2), "antécédents de -3")
eq(f.subs(x, -2), 5, "A(-2;5)")
eq(f.subs(x, 1), -4, "f(1)")
eq(sol(sp.Eq(f, g)), F(-1, 4), "f=g")
eq(sp.factor(f - g), (x + 1)*(x - 4), "facto f-g")
eq(sol(f - g <= 0), I(-1, 4), "f<=g")
eq(sol(f < 0), I.open(-1, 3), "f<0")
eq(sol(f <= 0), I(-1, 3), "f<=0")
eq(sp.factor(f), (x + 1)*(x - 3), "facto f")
eq((3*x**2 - 5).subs(x, -x), 3*x**2 - 5, "g paire")
eq((x**3 - 3*x).subs(x, -x), -(x**3 - 3*x), "h impaire")
eq(f.subs(x, -1), 0, "f(-1)")
# figure parité : h(2)=2, h(-2)=-2 ; g(1)=-2
eq((x**3 - 3*x).subs(x, 2), 2, "h(2)")
eq((3*x**2 - 5).subs(x, 1), -2, "g(1)")

# ---------------- 2035
f = x**2 - 3*x + 1
eq(f.subs(x, 2), -1, "2035 A")
eq(f.subs(x, -1), 5, "2035 B")
eq(f.subs(x, 0), 1, "2035 C")
eq(f.subs(x, 3), 1, "2035 Q4")
eq(sol(sp.Eq(f, 1)), F(0, 3), "2035 Q5")

# ---------------- 2037 (table) : rien à calculer, cohérence f(x)<=0 sur la table
tab = {-3: 5, -2: 2, -1: 0, 0: -1, 1: 0, 2: 2, 3: 5}
assert {k for k, v in tab.items() if v <= 0} == {-1, 0, 1}
assert {k for k, v in tab.items() if v == 2} == {-2, 2}
ok += 2

# ---------------- 2036
f = x**2 - 4
assert [f.subs(x, k) for k in range(-3, 4)] == [5, 0, -3, -4, -3, 0, 5]
eq(sol(f), F(-2, 2), "2036 f=0")
eq(f.subs(x, -x), f, "2036 paire")

# ---------------- 2040
eq((x**2 - 5).subs(x, -x), x**2 - 5, "2040 f paire")
eq((x**3 - x).subs(x, -x), -(x**3 - x), "2040 g impaire")
h = x**3 + x**2
eq(h.subs(x, 1), 2, "h(1)")
eq(h.subs(x, -1), 0, "h(-1)")

# ---------------- 2039
f, g = x**2 - 2, x
eq(sol(sp.Eq(f, g)), F(-1, 2), "2039 f=g")
eq(sp.expand((x + 1)*(x - 2)), sp.expand(f - g), "2039 facto")
eq(sol(f - g >= 0), U(I(-oo, -1), I(2, oo)), "2039 f>=g")
eq(f.subs(x, -1), -1, "2039 y(-1)")
eq(f.subs(x, 2), 2, "2039 y(2)")

# ---------------- 2038 (ligne brisée)
P = [(-3, 1), (-1, 4), (2, -2), (5, 1)]


def fpoly(t):
    for (x0, y0), (x1, y1) in zip(P, P[1:]):
        if x0 <= t <= x1:
            return y0 + (y1 - y0) * (t - x0) / (x1 - x0)


def zeros(k):
    res = set()
    for (x0, y0), (x1, y1) in zip(P, P[1:]):
        if (y0 - k) * (y1 - k) <= 0 and y0 != y1:
            res.add(R(x0) + (R(k) - y0) * R(x1 - x0, y1 - y0))
    return res


assert zeros(0) == {1, 4}
assert zeros(1) == {-3, R(1, 2), 5}
ts = [R(i, 100) for i in range(-300, 501)]
assert [t for t in ts if fpoly(t) >= 1] == [t for t in ts if -3 <= t <= R(1, 2) or t == 5]
assert [t for t in ts if fpoly(t) <= 0] == [t for t in ts if 1 <= t <= 4]
eq(sp.Rational(-2 - 4, 2 + 1), -2, "pente BC")
eq(sp.Rational(1 + 2, 5 - 2), 1, "pente CD")
ok += 4

# ---------------- 2041
fv = {0: 1, 1: 4, 2: 7, 3: 10}
gv = {0: 0, 1: 2, 2: 5, 3: 9}
assert [fv[abs(k)] for k in (-3, -2, -1)] == [10, 7, 4]
assert [-gv[abs(k)] for k in (-3, -2, -1)] == [-9, -5, -2]
ok += 2

# ---------------- 2042
P2 = (x - 2)*(x + 3)
eq(sol(P2), F(-3, 2), "2042 P=0")
eq(sol(P2 <= 0), I(-3, 2), "2042 P<=0")
eq(sol(P2 > 0), U(I.open(-oo, -3), I.open(2, oo)), "2042 P>0")

# ---------------- 2043
Q = (2*x - 3)/(x + 1)
dom = S.Reals - F(-1)
eq(sol(Q, dom), F(R(3, 2)), "2043 Q=0")
eq(sol(Q >= 0, dom), U(I.open(-oo, -1), I(R(3, 2), oo)), "2043 Q>=0")
eq(sol(Q < 0, dom), I.open(-1, R(3, 2)), "2043 Q<0")

# ---------------- 2044
f, g = 2*x + 3, x + 8
eq(f.subs(x, 4), 11, "f(4)")
eq(g.subs(x, 4), 12, "g(4)")
eq(sol(sp.Eq(f, g)), F(5), "f=g")
eq(f.subs(x, 5), 13, "f(5)")
eq(sol(f <= g, I(0, oo)), I(0, 5), "f<=g")
eq(f.subs(x, 20), 43, "f(20)")
eq(g.subs(x, 20), 28, "g(20)")

# ---------------- nouveau-1
f = (x**3 - 3*x)/2
D = I(-2, 2)
eq(f.subs(x, -2), -1, "n1 f(-2)")
eq(f.subs(x, 0), 0, "n1 f(0)")
eq(f.subs(x, 1), -1, "n1 f(1)")
eq(sol(sp.Eq(f, 1), D), F(-1, 2), "n1 f=1")
eq(sol(sp.Eq(f, -1), D), F(-2, 1), "n1 f=-1")
eq(sol(sp.Eq(f, 2), D), S.EmptySet, "n1 f=2")
eq(sol(f < 1, D), U(I.Ropen(-2, -1), I.open(-1, 2)), "n1 f<1")
eq(sol(f, D), F(-sqrt(3), 0, sqrt(3)), "n1 f=0")
eq(sol(f > 0, D), U(I.open(-sqrt(3), 0), I.Lopen(sqrt(3), 2)), "n1 f>0")
eq(sp.maximum(f, x, D), 1, "n1 max")
eq(sp.minimum(f, x, D), -1, "n1 min")

# ---------------- nouveau-2
A = x*(10 - x)
D = I.open(0, 10)
eq(A.subs(x, 2), 16, "A(2)")
eq(A.subs(x, 4), 24, "A(4)")
eq(sp.expand((x - 3)*(7 - x)), sp.expand(A - 21), "facto A-21")
eq(sol(sp.Eq(A, 21), D), F(3, 7), "A=21")
eq(sol(A >= 21, D), I(3, 7), "A>=21")

# ---------------- figures (revérification et ajouts du 2026-11-02)
# chaque point dessiné est-il bien sur sa courbe ?
eq((x**2 - 3*x + 1).subs(x, 2), -1, "fig 2035 A")
eq((x**2 - 3*x + 1).subs(x, -1), 5, "fig 2035 B")
eq(sol(sp.Eq(x**2 - 3*x + 1, 1)), F(0, 3), "fig 2035 y=1")
eq((x**2 - 5).subs(x, R(5, 2)), R(5, 4), "fig 2040 f(2,5)=1,25")
eq((x**3 - x).subs(x, R(3, 2)), R(15, 8), "fig 2040 g(1,5)=1,875")
eq(((x**3 + x**2).subs(x, 1), (x**3 + x**2).subs(x, -1)), (2, 0), "fig 2040 h")
eq(((3*x**2 - 5).subs(x, 1), (x**3 - 3*x).subs(x, 2)), (-2, 2), "fig cours parité M et N")
eq(sol(sp.Eq(x**2 - 2, x)), F(-1, 2), "fig 2039 intersections")
eq(sol((x**2 - 2*x - 3) < 0), I.open(-1, 3), "fig cours f<0")
eq(sol(sp.Eq((2*x - 3)/(x + 1), 0), S.Reals - F(-1)), F(R(3, 2)), "fig 2043 zéro")
eq(((2*x - 3)/(x + 1)).subs(x, -6), 3, "fig 2043 Q(-6)=3")
eq(sol(sp.Eq((x**3 - 3*x)/2, 1), I(-2, 2)), F(-1, 2), "fig 3748 y=1")
eq(sol(sp.Eq((x**3 - 3*x)/2, -1), I(-2, 2)), F(-2, 1), "fig 3748 y=-1")
eq(sol((x**3 - 3*x)/2 < 1, I(-2, 2)), U(I.Ropen(-2, -1), I.open(-1, 2)), "fig 3748 f<1")
eq(sol((x**3 - 3*x)/2 > 0, I(-2, 2)), U(I.open(-sqrt(3), 0), I.Lopen(sqrt(3), 2)), "fig 3748 f>0")
# 2037 : points de la table
T37 = {-3: 5, -2: 2, -1: 0, 0: -1, 1: 0, 2: 2, 3: 5}
eq(sp.Tuple(*sorted(k for k, v in T37.items() if v == 2)), sp.Tuple(-2, 2), "fig 2037 f=2")
eq(sp.Tuple(*sorted(k for k, v in T37.items() if v <= 0)), sp.Tuple(-1, 0, 1), "fig 2037 f<=0")
# 2041 : symétriques (f paire, g impaire)
Tf, Tg = {0: 1, 1: 4, 2: 7, 3: 10}, {0: 0, 1: 2, 2: 5, 3: 9}
eq(sp.Tuple(*[Tf[k] for k in (3, 2, 1)]), sp.Tuple(10, 7, 4), "fig 2041 f(-k)=f(k)")
eq(sp.Tuple(*[-Tg[k] for k in (3, 2, 1)]), sp.Tuple(-9, -5, -2), "fig 2041 g(-k)=-g(k)")

print(f"verif_172 : {ok} contrôles OK")
