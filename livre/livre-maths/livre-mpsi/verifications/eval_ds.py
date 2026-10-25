# -*- coding: utf-8 -*-
"""Vérifications des six devoirs surveillés (partie Évaluations)."""
import cmath
import math
from fractions import Fraction as Fr
from itertools import permutations, product
from math import comb, factorial, isclose, sqrt, pi, cos, sin, log, exp, gcd

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

x, y, t = sp.symbols("x y t", real=True)
X = sp.symbols("X")

# ============================ DS 1 ===================================
f = x**2 - 2*x
check("DS1 f([-1,2]) = [-1,3]", sp.calculus.util.function_range(f, x, sp.Interval(-1, 2))
      == sp.Interval(-1, 3))
sol = sp.solve_univariate_inequality(sp.And(f >= 0, f <= 3), x, relational=False) \
    if False else sp.Union(sp.Interval(-1, 0), sp.Interval(2, 3))
check("DS1 f^-1([0,3])", all((0 <= v*v - 2*v <= 3) == (sol.contains(v) == True)
      for v in [i/10 for i in range(-30, 50)]))
check("DS1 reciproque", all(isclose((1 + sqrt(1 + yv))**2 - 2*(1 + sqrt(1 + yv)), yv)
      for yv in [-1, 0, 2.5, 10]))
n = sp.symbols("n", integer=True, positive=True)
k = sp.symbols("k", integer=True)
check("DS1 somme k k!", all(sum(j*factorial(j) for j in range(1, m + 1)) == factorial(m + 1) - 1
      for m in range(1, 12)))
check("DS1 somme C(n,k)/(k+1)", all(sum(Fr(comb(m, j), j + 1) for j in range(m + 1))
      == Fr(2**(m + 1) - 1, m + 1) for m in range(0, 15)))
check("DS1 somme double", all(sum(i for j in range(1, m + 1) for i in range(1, j + 1))
      == m*(m + 1)*(m + 2)//6 for m in range(1, 15)))
check("DS1 Bernoulli", all((1 + xv)**m >= 1 + m*xv for xv in [-1, -0.5, 0, 0.3, 2]
      for m in range(1, 10)))
sols = [v for v in sp.solveset(2*sp.cos(x)**2 + 3*sp.sin(x) - 3, x, sp.Interval.Ropen(0, 2*sp.pi))]
check("DS1 equation trigo", sorted(sols, key=float) == [sp.pi/6, sp.pi/2, 5*sp.pi/6])
check("DS1 cos(pi/8)", sp.simplify(sp.cos(sp.pi/8) - sp.sqrt(2 + sp.sqrt(2))/2) == 0)
for th in [pi/9, 5*pi/9, 7*pi/9]:
    c = cos(th)
    check(f"DS1 racine 8t^3-6t-1 ({th:.3f})", abs(8*c**3 - 6*c - 1) < 1e-12)
check("DS1 somme et produit", isclose(cos(pi/9) + cos(5*pi/9) + cos(7*pi/9), 0, abs_tol=1e-12)
      and isclose(cos(pi/9)*cos(5*pi/9)*cos(7*pi/9), 1/8))
z = sp.symbols("z")
check("DS1 equation du second degre", set(sp.solve(z**2 - (3 + sp.I)*z + 4 + 3*sp.I, z))
      == {2 - sp.I, 1 + 2*sp.I})
check("DS1 (1-3i)^2", sp.expand((1 - 3*sp.I)**2) == -8 - 6*sp.I)
Z = ((x + sp.I*(y - 1))*(x + 1 - sp.I*y))
check("DS1 Im((z-i)conj(z+1))", sp.expand(sp.im(sp.expand(Z))) == sp.expand(y - x - 1))
check("DS1 Re", sp.expand(sp.re(sp.expand(Z)) - (x**2 + x + y**2 - y)) == 0)
for th in [0.3, 2.0, -1.2]:
    zz = cmath.exp(1j*th)
    q = (1 + zz)/(1 - zz)
    check(f"DS1 (1+z)/(1-z) imaginaire pur ({th})", abs(q.real) < 1e-12
          and isclose(q.imag, 1/math.tan(th/2)))
for nn in [2, 3, 5, 8]:
    for kk in range(1, nn):
        zk = -1j/math.tan(kk*pi/nn)
        check(f"DS1 (z+1)^n = (z-1)^n (n={nn},k={kk})", abs((zk + 1)**nn - (zk - 1)**nn)
              < 1e-9*max(1, abs(zk + 1)**nn))

# ============================ DS 2 ===================================
check("DS2 encadrement ln(1+x)", all(xv - xv*xv/2 <= log(1 + xv) <= xv
      for xv in [0, 0.1, 1, 5, 30]))
check("DS2 arctan x + arctan 1/x", all(isclose(math.atan(v) + math.atan(1/v), pi/2) for v in [0.2, 1, 7])
      and all(isclose(math.atan(v) + math.atan(1/v), -pi/2) for v in [-0.2, -3]))
check("DS2 max de x^(1/x) en e", max((v/100)**(100/v) for v in range(50, 1000))
      <= math.e**(1/math.e) + 1e-12)
check("DS2 e^pi > pi^e", math.e**pi > pi**math.e)
yf = sp.Function("yf")
s1 = sp.dsolve((1 + x**2)*yf(x).diff(x) + 2*x*yf(x) - 1, yf(x), ics={yf(0): 1})
check("DS2 ED ordre 1", sp.simplify(s1.rhs - (x + 1)/(1 + x**2)) == 0)
s2 = sp.dsolve(yf(x).diff(x, 2) - 3*yf(x).diff(x) + 2*yf(x) - sp.exp(x), yf(x),
               ics={yf(0): 0, yf(x).diff(x).subs(x, 0): 0})
check("DS2 ED ordre 2", sp.simplify(s2.rhs - (-sp.exp(x) + sp.exp(2*x) - x*sp.exp(x))) == 0)
u = 0.0
for m in range(25):
    check(f"DS2 u_n = 2cos(pi/2^(n+1)) (n={m})", isclose(u, 2*cos(pi/2**(m + 1)), abs_tol=1e-12))
    check(f"DS2 |u_n - 2| <= 2/2^n (n={m})", abs(u - 2) <= 2/2**m + 1e-15)
    u = sqrt(2 + u)
check("DS2 4^n (2 - u_n) -> pi^2/4", isclose(4**10*(2 - 2*cos(pi/2**11)), pi**2/4, rel_tol=1e-5))
check("DS2 corde universelle", all(abs((lambda g: g(0) + g(0.5))(lambda s: math.sin(2*pi*(s + 0.5))
      - math.sin(2*pi*s))) < 1e-12 for _ in [0]))

# ============================ DS 3 ===================================
check("DS3 Bezout 7(-1)+5(2)=3", 7*(-1) + 5*2 == 3)
check("DS3 solutions", all(21*(-1 + 5*kk) + 15*(2 - 7*kk) == 9 for kk in range(-5, 6)))
check("DS3 7^4 = 1 mod 100", pow(7, 4, 100) == 1 and pow(7, 2026, 100) == 49)
check("DS3 30 | n^5 - n", all((m**5 - m) % 30 == 0 for m in range(-50, 200)))
check("DS3 pgcd(n^2+1, n+1)", all(gcd(m*m + 1, m + 1) in (1, 2) for m in range(0, 300))
      and gcd(3*3 + 1, 4) == 2)
check("DS3 generateurs de U12", [kk for kk in range(12) if gcd(kk, 12) == 1] == [1, 5, 7, 11])
check("DS3 ordre de e^(2ik pi/n)", all(
    min(d for d in range(1, nn + 1) if (kk*d) % nn == 0) == nn//gcd(kk, nn)
    for nn in range(1, 20) for kk in range(nn)))
A = sp.Matrix([[1, 1, 1], [0, 1, 1], [0, 0, 1]])
for m in range(0, 8):
    check(f"DS3 A^{m}", A**m == sp.Matrix([[1, m, m*(m + 1)//2], [0, 1, m], [0, 0, 1]]))
check("DS3 A^-1", A.inv() == sp.Matrix([[1, -1, 0], [0, 1, -1], [0, 0, 1]]))
mm = sp.symbols("mm")
Msys = sp.Matrix([[1, 1, mm], [1, mm, 1], [mm, 1, 1]])
check("DS3 det systeme", sp.factor(Msys.det()) == -(mm - 1)**2*(mm + 2))
check("DS3 solution generique", all(Msys.subs(mm, v)*sp.Matrix([1, 1, 1])/(v + 2)
      == sp.Matrix([1, 1, 1]) for v in [0, 3, -5]))
P = X**4 + 2*X**3 + 3*X**2 + 2*X + 1
check("DS3 P = (X^2+X+1)^2", sp.expand((X**2 + X + 1)**2 - P) == 0)
j = sp.Rational(-1, 2) + sp.sqrt(3)/2*sp.I
check("DS3 j racine double", sp.simplify(P.subs(X, j)) == 0
      and sp.simplify(sp.diff(P, X).subs(X, j)) == 0
      and sp.simplify(sp.diff(P, X, 2).subs(X, j)) != 0)
check("DS3 elements simples", sp.apart(1/(X**3 - X), X)
      == -1/X + sp.Rational(1, 2)/(X - 1) + sp.Rational(1, 2)/(X + 1))
check("DS3 primitive", sp.simplify(sp.diff(sp.log((x**2 - 1)/x**2)/2, x) - 1/(x**3 - x)) == 0)
for m in range(2, 9):
    check(f"DS3 reste de X^{m} par (X-1)^2", sp.rem(X**m, (X - 1)**2, X) == m*X - (m - 1))

# ============================ DS 4 ===================================
check("DS4 DL e^sin", sp.series(sp.exp(sp.sin(x)), x, 0, 5).removeO()
      == 1 + x + x**2/2 - x**4/8)
check("DS4 limite", sp.limit((sp.exp(sp.sin(x)) - sp.exp(x))/x**3, x, 0) == sp.Rational(-1, 6))
check("DS4 limite racine", sp.limit(sp.sqrt(x**2 + 2*x) - x, x, sp.oo) == 1)
check("DS4 developpement", sp.limit((sp.sqrt(x**2 + 2*x) - x - 1)*x, x, sp.oo) == sp.Rational(-1, 2))
check("DS4 1/sin^2 - 1/x^2", sp.limit(1/sp.sin(x)**2 - 1/x**2, x, 0) == sp.Rational(1, 3))
def racine(nn):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi)/2
        if mid**nn + mid - 1 < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi)/2
us = [racine(nn) for nn in range(2, 60)]
check("DS4 u_n croissante", all(us[i] < us[i + 1] for i in range(len(us) - 1)))
check("DS4 u_2 = (sqrt5 - 1)/2", isclose(us[0], (sqrt(5) - 1)/2, abs_tol=1e-12))
for nn in [10**3, 10**5, 10**7]:
    lo, hi = 0.0, 1.0
    for _ in range(300):
        mid = (lo + hi)/2
        if nn*math.log1p(-mid) - math.log(mid) > 0:   # u^n - (1-u) avec v = 1 - u
            lo = mid
        else:
            hi = mid
    v = (lo + hi)/2
    check(f"DS4 v_n ~ ln n / n (n={nn})", isclose(v/(log(nn)/nn), 1, rel_tol=0.35))
phi = lambda Pp: (Pp.subs(X, 1), sp.diff(Pp, X).subs(X, 1))
check("DS4 base de F", phi(sp.expand((X - 1)**2)) == (0, 0)
      and phi(sp.expand(X*(X - 1)**2)) == (0, 0))
check("DS4 surjectivite", phi(sp.Integer(1)) == (1, 0) and phi(X - 1) == (0, 1))
check("DS4 decomposition de X^3", sp.expand((X - 1)**2*(X + 2) - (X**3 - 3*X + 2)) == 0
      and phi(X**3 - 3*X + 2) == (0, 0))
check("DS4 x^2 - sin^2 x", sp.series(x**2 - sp.sin(x)**2, x, 0, 6).removeO() == x**4/3)
Pm = sp.Matrix([[0, -1, -1], [0, 1, 0], [0, 0, 1]])
check("DS4 projecteur", Pm*Pm == Pm and Pm.trace() == 2 and Pm.rank() == 2)
check("DS4 image = plan, noyau = D", all(sum(Pm*sp.Matrix(v)) == 0 for v in [[1, 2, 3], [4, -1, 0]])
      and Pm*sp.Matrix([1, 0, 0]) == sp.zeros(3, 1))
Bp = sp.Matrix([[1, 1, 1], [-1, 0, 0], [0, -1, 0]])
check("DS4 base adaptee", Bp.inv()*Pm*Bp == sp.diag(1, 1, 0))
check("DS4 symetrie", (2*Pm - sp.eye(3))**2 == sp.eye(3))

# ============================ DS 5 ===================================
sig = [3, 5, 7, 1, 2, 8, 4, 6]   # image de 1..8
from sympy.combinatorics import Permutation
Ps = Permutation([v - 1 for v in sig])
check("DS5 cycles", sorted(len(c) for c in Ps.cyclic_form) == [2, 2, 4])
check("DS5 signature et ordre", Ps.signature() == -1 and Ps.order() == 4)
a_, b_ = sp.symbols("a_ b_")
for nn in range(1, 6):
    D = sp.Matrix(nn, nn, lambda i, jj: a_ if i == jj else b_)
    check(f"DS5 D_n n={nn}", sp.factor(D.det() - (a_ + (nn - 1)*b_)*(a_ - b_)**(nn - 1)) == 0)
check("DS5 det(J - I)", all(sp.Matrix(nn, nn, lambda i, jj: 0 if i == jj else 1).det()
      == (nn - 1)*(-1)**(nn - 1) for nn in range(1, 7)))
aa, bb, cc = sp.symbols("aa bb cc")
check("DS5 det nul", sp.Matrix([[1, 1, 1], [aa, bb, cc], [bb + cc, cc + aa, aa + bb]]).det().expand() == 0)
In = lambda m: sp.integrate(x**m/(1 + x**2), (x, 0, 1))
check("DS5 I0, I1", In(0) == sp.pi/4 and sp.simplify(In(1) - sp.log(2)/2) == 0)
check("DS5 I_n + I_{n+2}", all(sp.simplify(In(m) + In(m + 2) - sp.Rational(1, m + 1)) == 0
      for m in range(0, 6)))
import mpmath
for m in [20, 200]:
    val = float(mpmath.quad(lambda s: s**m/(1 + s*s), [0, 1]))
    check(f"DS5 encadrement I_n (n={m})", 1/(2*(m + 1)) <= val <= 1/(2*(m - 1)))
nn = 200000
check("DS5 Riemann", isclose(sum(1/sqrt(nn*nn + kk*nn) for kk in range(1, nn + 1)),
      2*(sqrt(2) - 1), abs_tol=1e-5))
check("DS5 Taylor-Lagrange", all(abs(log(1 + v) - v + v*v/2) <= v**3/3 for v in [0.1, 0.5, 1, 3]))
check("DS5 MISSISSIPPI", factorial(11)//(factorial(4)*factorial(4)*factorial(2)) == 34650)
check("DS5 full", 8*comb(4, 3)*7*comb(4, 2) == 1344)
check("DS5 double paire", comb(8, 2)*comb(4, 2)**2*24 == 24192)
check("DS5 bonbons", comb(9, 3) == 84 and comb(13, 3) == 286)
check("DS5 bonbons force brute", sum(1 for t4 in product(range(1, 11), repeat=4) if sum(t4) == 10) == 84)

# ============================ DS 6 ===================================
dist = {1: Fr(1)}   # X_0 = 1 boule rouge sur 2
for m in range(0, 8):
    new = {}
    tot = m + 2
    for r, p in dist.items():
        new[r + 1] = new.get(r + 1, 0) + p*Fr(r, tot)
        new[r] = new.get(r, 0) + p*Fr(tot - r, tot)
    dist = new
    check(f"DS6 Polya uniforme (n={m + 1})", all(v == Fr(1, m + 2) for v in dist.values())
          and sorted(dist) == list(range(1, m + 3)))
    check(f"DS6 esperance (n={m + 1})", sum(r*p for r, p in dist.items()) == Fr(m + 3, 2))
check("DS6 Bayes", Fr(1, 2)*Fr(2, 3)/Fr(1, 2) == Fr(2, 3))
def ps3(Pp, Qq):
    return sum(Pp.subs(X, s)*Qq.subs(X, s) for s in (0, 1, 2))
L0 = (X - 1)*(X - 2)/2; L1 = -X*(X - 2); L2 = X*(X - 1)/2
check("DS6 Lagrange orthonormee", all(ps3(Lp, Lq) == (1 if i == jj else 0)
      for i, Lp in enumerate([L0, L1, L2]) for jj, Lq in enumerate([L0, L1, L2])))
check("DS6 projection de X^2", ps3(X**2 - (2*X - sp.Rational(1, 3)), sp.Integer(1)) == 0
      and ps3(X**2 - (2*X - sp.Rational(1, 3)), X) == 0)
check("DS6 distance", ps3(X**2 - 2*X + sp.Rational(1, 3), X**2 - 2*X + sp.Rational(1, 3)) == sp.Rational(2, 3))
check("DS6 serie n^2/2^n", sp.summation(n**2/2**n, (n, 1, sp.oo)) == 6)
check("DS6 serie (n+1)/n!", sp.summation((n + 1)/sp.factorial(n), (n, 0, sp.oo)) == 2*sp.E)
check("DS6 serie ln(1+(-1)^n/n) converge", abs(sum(math.log1p((-1)**m/m) for m in range(2, 200001))
      - sum(math.log1p((-1)**m/m) for m in range(2, 100001))) < 1e-4)
check("DS6 terme 1/n - ln(1+1/n) ~ 1/(2n^2)", isclose((1/1000 - math.log1p(1/1000))*2e6, 1, rel_tol=1e-3))
F2 = x**2 + x*y + y**2 - 3*x - 3*y
check("DS6 point critique", sp.solve([sp.diff(F2, x), sp.diff(F2, y)], [x, y]) == {x: 1, y: 1})
check("DS6 forme canonique", sp.expand((x - 1)**2 + (x - 1)*(y - 1) + (y - 1)**2 - 3 - F2) == 0)
check("DS6 u^2+uv+v^2 >= 0", sp.expand((x + y/2)**2 + 3*y**2/4 - (x**2 + x*y + y**2)) == 0)
check("DS6 gradient en 0", (sp.diff(F2, x).subs({x: 0, y: 0}), sp.diff(F2, y).subs({x: 0, y: 0})) == (-3, -3))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
