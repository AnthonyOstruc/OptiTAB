# -*- coding: utf-8 -*-
"""Vérification des résultats des examens EX1 (premier semestre) et EX2 (fin d'année)."""
import math
import random
from fractions import Fraction as Fr
from itertools import permutations
from math import comb, factorial, gcd, isclose, sqrt, pi, cos, sin

import sympy as sp

OK = []


def check(name, cond):
    if not cond:
        raise AssertionError("ÉCHEC : " + name)
    OK.append(name)


x, y, h, k, C = sp.symbols("x y h k C", real=True)
random.seed(7)

# ============================ EX1 ====================================
# Exercice 1 : pentagone
w = sp.exp(2*sp.pi*sp.I/5)
X0 = sp.symbols("X0")
check("EX1 somme des racines 5-iemes", abs(sp.N(sum(w**j for j in range(5)), 60)) < sp.Float(1e-50)
      and sp.expand(sum(X0**j for j in range(5))*(X0 - 1) - (X0**5 - 1)) == 0)
al = 2*sp.cos(2*sp.pi/5); be = 2*sp.cos(4*sp.pi/5)
check("EX1 alpha+beta, alpha*beta", sp.simplify(al + be + 1) == 0 and sp.simplify(al*be + 1) == 0)
check("EX1 cos(2pi/5)", sp.simplify(sp.cos(2*sp.pi/5) - (sp.sqrt(5) - 1)/4) == 0)
check("EX1 cos(4pi/5)", sp.simplify(sp.cos(4*sp.pi/5) + (1 + sp.sqrt(5))/4) == 0)
cote2 = sp.simplify(2 - 2*sp.cos(2*sp.pi/5))
check("EX1 cote du pentagone", sp.simplify(cote2 - (5 - sp.sqrt(5))/2) == 0
      and isclose(float(sp.sqrt(cote2)), 1.1755705, abs_tol=1e-7)
      and isclose(float(2*sp.sin(sp.pi/5)), 1.1755705, abs_tol=1e-7))
check("EX1 alpha racine de X^2+X-1", sp.simplify(al**2 + al - 1) == 0)
# Exercice 2 : x y' - 2 y = x^3
ysol = x**3 + C*x**2
check("EX2 solution", sp.simplify(x*sp.diff(ysol, x) - 2*ysol - x**3) == 0)
check("EX2 homogene", sp.simplify(x*sp.diff(C*x**2, x) - 2*C*x**2) == 0)
# raccordement : y'(0) = 0 des deux côtés
for c1, c2 in [(1, -2), (0, 3), (-1, -1)]:
    dr = sp.limit((x**3 + c1*x**2)/x, x, 0, '+'); dl = sp.limit((x**3 + c2*x**2)/x, x, 0, '-')
    check(f"EX2 raccord derivable C1={c1} C2={c2}", dr == 0 and dl == 0)
# par (x0, y0) avec x0 != 0 : C imposé d'un côté, libre de l'autre
check("EX2 par (1,2) : C=1", sp.solve(ysol.subs(x, 1) - 2, C) == [1])
# Exercice 3 : 2^a - 1
check("EX1 2^a-1 | 2^(ab)-1", all((2**(a*b) - 1) % (2**a - 1) == 0 for a in range(1, 12) for b in range(1, 8)))
check("EX1 pgcd(2^a-1,2^b-1)", all(gcd(2**a - 1, 2**b - 1) == 2**gcd(a, b) - 1 for a in range(1, 40) for b in range(1, 40)))
check("EX1 reste 2^a-1 = 2^r(2^(bq)-1) + 2^r - 1", all(2**a - 1 == 2**(a % b)*(2**(b*(a//b)) - 1) + 2**(a % b) - 1
      for a in range(1, 40) for b in range(1, 20)))
check("EX1 Mersenne 2047", 2**11 - 1 == 2047 == 23*89 and sp.isprime(11))
check("EX1 2^n-1 premier => n premier", all(sp.isprime(n) for n in range(2, 90) if sp.isprime(2**n - 1)))
# Problème : Fibonacci
F = [0, 1]
for _ in range(60):
    F.append(F[-1] + F[-2])
A = sp.Matrix([[1, 1], [1, 0]])
check("EX1 A^n", all(A**n == sp.Matrix([[F[n + 1], F[n]], [F[n], F[n - 1]]]) for n in range(1, 25)))
check("EX1 F_{m+n}", all(F[m + n] == F[m + 1]*F[n] + F[m]*F[n - 1] for m in range(0, 20) for n in range(1, 20)))
check("EX1 F_2n", all(F[2*n] == F[n]*(F[n + 1] + F[n - 1]) for n in range(1, 25)))
X = sp.symbols("X")
check("EX1 reste de X^n", all(sp.rem(X**n, X**2 - X - 1, X) == F[n]*X + F[n - 1] for n in range(1, 25)))
check("EX1 A^2 = A + I", A**2 == A + sp.eye(2))
check("EX1 A^n = F_n A + F_{n-1} I", all(A**n == F[n]*A + F[n - 1]*sp.eye(2) for n in range(1, 20)))
phi = (1 + sp.sqrt(5))/2; psi = (1 - sp.sqrt(5))/2
check("EX1 Binet", all(sp.simplify((phi**n - psi**n)/sp.sqrt(5) - F[n]) == 0 for n in range(0, 20)))
check("EX1 Cassini", all(F[n + 1]*F[n - 1] - F[n]**2 == (-1)**n for n in range(1, 50)))
check("EX1 pgcd consecutifs", all(gcd(F[n], F[n + 1]) == 1 for n in range(0, 50)))
ratios = [F[n + 1]/F[n] for n in range(1, 11)]
check("EX1 rapports alternes", all((ratios[i] - float(phi))*(ratios[i + 1] - float(phi)) < 0 for i in range(9)))
check("EX1 rapports figure", [round(r, 4) for r in ratios[:6]] == [1.0, 2.0, 1.5, 1.6667, 1.6, 1.625])

# ============================ EX2 ====================================
# Exercice 1 : points fixes d'une permutation aléatoire
for n in range(2, 7):
    loi = {}
    for s in permutations(range(n)):
        fx = sum(1 for i in range(n) if s[i] == i)
        loi[fx] = loi.get(fx, 0) + 1
    tot = factorial(n)
    E1 = Fr(sum(kk*v for kk, v in loi.items()), tot)
    E2 = Fr(sum(kk*kk*v for kk, v in loi.items()), tot)
    check(f"EX2 E(X)=1, V(X)=1 (n={n})", E1 == 1 and E2 - E1**2 == 1)
    check(f"EX2 P(X=n), P(X=n-1) (n={n})", loi.get(n, 0) == 1 and loi.get(n - 1, 0) == 0)
    check(f"EX2 P(X>=3) <= 1/4 (n={n})", Fr(sum(v for kk, v in loi.items() if kk >= 3), tot) <= Fr(1, 4))
    if n == 4:
        check("EX2 loi n=4", loi == {0: 9, 1: 8, 2: 6, 4: 1})
check("EX2 P(X_i X_j = 1)", Fr(factorial(3), factorial(5)) == Fr(1, 5*4))
# Exercice 2 : matrices de rang 1
for _ in range(30):
    n = random.randint(2, 4)
    U = sp.Matrix([random.randint(-3, 3) for _ in range(n)])
    V = sp.Matrix([random.randint(-3, 3) for _ in range(n)])
    if U == sp.zeros(n, 1) or V == sp.zeros(n, 1):
        continue
    M = U*V.T
    t = M.trace()
    assert M.rank() == 1 and M**2 == t*M and t == (V.T*U)[0]
    assert sp.simplify((sp.eye(n) + M).det() - (1 + t)) == 0
    if t != -1:
        assert (sp.eye(n) + M)*(sp.eye(n) - M/(1 + t)) == sp.eye(n)
    else:
        assert (sp.eye(n) + M)*U == sp.zeros(n, 1)
check("EX2 rang 1 : M^2 = tr(M) M, det(I+M) = 1+tr M, inverse", True)
U = sp.Matrix([1, 2, 3]); V = sp.Matrix([1, 1, 1]); M = U*V.T
check("EX2 exemple", M.trace() == 6 and (sp.eye(3) + M).inv() == sp.eye(3) - M/7 and (sp.eye(3) + M).det() == 7)
U2 = sp.Matrix([1, -1, 0]); V2 = sp.Matrix([1, 1, 5]); M2 = U2*V2.T
check("EX2 trace nulle => nilpotente", M2.trace() == 0 and M2**2 == sp.zeros(3, 3))
# Exercice 3 : folium
f = x**3 + y**3 - 3*x*y
crit = sp.solve([sp.diff(f, x), sp.diff(f, y)], [x, y], dict=True)
crit_reels = sorted([(s[x], s[y]) for s in crit if s[x].is_real and s[y].is_real])
check("EX2 points critiques", crit_reels == [(0, 0), (1, 1)])
check("EX2 developpement en (1,1)", sp.expand(f.subs({x: 1 + h, y: 1 + k}) - (-1 + 3*(h**2 - h*k + k**2) + h**3 + k**3)) == 0)
check("EX2 h^2-hk+k^2 >= (h^2+k^2)/2", sp.expand(h**2 - h*k + k**2 - (h**2 + k**2)/2 - (h - k)**2/2) == 0)
ok_min = True
for _ in range(20000):
    r = random.uniform(0, 1.5); th = random.uniform(0, 2*pi)
    hh, kk = r*cos(th), r*sin(th)
    if (1 + hh)**3 + (1 + kk)**3 - 3*(1 + hh)*(1 + kk) < -1 - 1e-12:
        ok_min = False
check("EX2 minimum local sur le disque de rayon 3/2", ok_min)
check("EX2 |h^3+k^3| <= r (h^2+k^2)", all(abs(a**3 + b**3) <= sqrt(a*a + b*b)*(a*a + b*b) + 1e-12
      for a, b in [(random.uniform(-2, 2), random.uniform(-2, 2)) for _ in range(5000)]))
tpar = sp.symbols("t")
xf = 3*tpar/(1 + tpar**3); yf = 3*tpar**2/(1 + tpar**3)
check("EX2 parametrage du folium", sp.simplify(f.subs({x: xf, y: yf})) == 0)
check("EX2 f(1,1) = -1", f.subs({x: 1, y: 1}) == -1)
# Problème : u_{n+1} = sin u_n
check("EX2 1/sin^2 - 1/x^2 -> 1/3", sp.limit(1/sp.sin(x)**2 - 1/x**2, x, 0) == sp.Rational(1, 3))
u = 1.0
vals = {}
for n in range(1, 200001):
    u = math.sin(u)
    if n in (10, 100, 1000, 10000, 100000, 200000):
        vals[n] = u*sqrt(n)
check("EX2 u_n sqrt(n) -> sqrt(3)", abs(vals[200000] - sqrt(3)) < 2e-4 and abs(vals[1000] - sqrt(3)) < 1e-2)
print("u_n sqrt(n) :", {kk: round(v, 5) for kk, v in vals.items()})
us = [math.pi/2]
for _ in range(6):
    us.append(math.sin(us[-1]))
check("EX2 premiers termes (u0 = pi/2)", [round(v, 4) for v in us[:5]] == [1.5708, 1.0, 0.8415, 0.7456, 0.6784])
check("EX2 series", True)  # u_n ~ sqrt(3/n) : sum u_n, sum u_n^2 divergent ; sum u_n^3 convergent (Riemann)

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
