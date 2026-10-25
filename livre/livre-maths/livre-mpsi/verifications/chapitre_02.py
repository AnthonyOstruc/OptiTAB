# -*- coding: utf-8 -*-
"""Vérifications du chapitre 2 — Calcul algébrique et trigonométrie."""
import math
from fractions import Fraction
from math import comb, factorial, isclose, cos, sin, tan, pi, sqrt, log

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

# --- L'essentiel ------------------------------------------------------
for n in range(1, 60):
    check("somme des k", sum(range(1, n + 1)) == n*(n + 1)//2)
    check("somme des k²", sum(k*k for k in range(1, n + 1)) == n*(n + 1)*(2*n + 1)//6)
    check("somme impairs = n²", sum(2*k - 1 for k in range(1, n + 1)) == n*n)
x = sp.symbols("x")
for n in range(0, 12):
    check("somme géométrique", sp.simplify(sum(x**k for k in range(n + 1))
          - (1 - x**(n + 1))/(1 - x)).equals(0))
a, b = sp.symbols("a b")
for n in range(1, 9):
    check("a^n−b^n", sp.expand((a - b)*sum(a**(n - 1 - k)*b**k for k in range(n)) - (a**n - b**n)) == 0)
for n in range(1, 25):
    for k in range(-2, n + 3):
        c = comb(n, k) if 0 <= k <= n else 0
        cm1 = comb(n - 1, k - 1) if 0 <= k - 1 <= n - 1 else 0
        cm2 = comb(n - 1, k) if 0 <= k <= n - 1 else 0
        check("Pascal", (c == cm1 + cm2) or n == 0)
# --- Exercice 1 -------------------------------------------------------
check("ex1a", sum(range(1, 101)) == 5050)
check("ex1b", sum(2**k for k in range(11)) == 2047)
check("ex1c", sum(1 for k in range(5, 21)) == 16)
for n in range(1, 40):
    check("ex1e", 2*sum(3*k + 2 for k in range(n + 1)) == (n + 1)*(3*n + 4))
check("ex1f", sum(k*k for k in range(1, 51)) == 42925)
# --- Exercice 2 -------------------------------------------------------
for n in range(1, 30):
    check("ex2d produit télescopique", isclose(math.prod(1 + 1/k for k in range(1, n + 1)), n + 1))
# --- Exercice 3 -------------------------------------------------------
check("ex3a", (comb(7, 2), comb(10, 3)) == (21, 120))
check("ex3d coeff x³ de (x−2)^5", sp.expand((x - 2)**5).coeff(x, 3) == 40)
check("ex3e", sp.expand((2*x + 1)**4 - (16*x**4 + 32*x**3 + 24*x**2 + 8*x + 1)) == 0)
# --- Exercice 4 -------------------------------------------------------
X, Y = sp.symbols("X Y")
sol = sp.solve([X + 2*Y - 5, 3*X - Y - 1], [X, Y])
check("ex4a", sol == {X: 1, Y: 2})
check("ex4b infinité", sp.solve([2*X - 4*Y - 6, -X + 2*Y + 3], [X, Y]) == {X: 2*Y + 3})
check("ex4c aucune", sp.solve([X + Y - 2, 2*X + 2*Y - 5], [X, Y]) == [])
# --- Exercice 5 -------------------------------------------------------
check("ex5a", sp.solveset((x - 1)*(x + 2) > 0, x, sp.S.Reals)
      == sp.Union(sp.Interval.open(-sp.oo, -2), sp.Interval.open(1, sp.oo)))
check("ex5b", sp.solveset(x**2 <= 4, x, sp.S.Reals) == sp.Interval(-2, 2))
check("ex5c", sp.solveset((2*x - 3)/(x + 1) <= 0, x, sp.S.Reals)
      == sp.Interval.Lopen(-1, sp.Rational(3, 2)))
check("ex5d", sp.solveset(x**3 >= x, x, sp.S.Reals)
      == sp.Union(sp.Interval(-1, 0), sp.Interval(1, sp.oo)))
# --- Exercice 6 -------------------------------------------------------
check("ex6a", sp.solveset(sp.Abs(x - 3) - 2, x, sp.S.Reals) == sp.FiniteSet(1, 5))
check("ex6b", sp.solveset(sp.Abs(x + 1) < 4, x, sp.S.Reals) == sp.Interval.open(-5, 3))
check("ex6c", sp.solveset(sp.Abs(2*x - 1) >= 3, x, sp.S.Reals)
      == sp.Union(sp.Interval(-sp.oo, -1), sp.Interval(2, sp.oo)))
# --- Exercices 7-8 : valeurs usuelles et angles associés ---------------
vals = {
    "2π/3": (-0.5, sqrt(3)/2), "-π/4": (sqrt(2)/2, -sqrt(2)/2),
    "7π/6": (-sqrt(3)/2, -0.5), "5π/3": (0.5, -sqrt(3)/2),
    "3π/4": (-sqrt(2)/2, sqrt(2)/2), "-π/6": (sqrt(3)/2, -0.5)}
angles = {"2π/3": 2*pi/3, "-π/4": -pi/4, "7π/6": 7*pi/6, "5π/3": 5*pi/3,
          "3π/4": 3*pi/4, "-π/6": -pi/6}
for k, t in angles.items():
    check(f"ex7 {k}", isclose(cos(t), vals[k][0]) and isclose(sin(t), vals[k][1]))
t = sp.symbols("t", real=True)
check("ex8 cos(π−t)+cos(π+t)", sp.simplify(sp.cos(sp.pi - t) + sp.cos(sp.pi + t) + 2*sp.cos(t)) == 0)
check("ex8 sin(π/2+t)", sp.simplify(sp.sin(sp.pi/2 + t) - sp.cos(t)) == 0)
# --- Exercice 9 -------------------------------------------------------
for n in range(1, 30):
    check("ex9a", sp.Rational(0) == sp.nsimplify(sum(Fraction(1, k*(k + 1)) for k in range(1, n + 1)) - Fraction(n, n + 1)))
    check("ex9c", isclose(sum(sqrt(k + 1) - sqrt(k) for k in range(1, n + 1)), sqrt(n + 1) - 1))
    check("ex9d", sum(k*factorial(k) for k in range(1, n + 1)) == factorial(n + 1) - 1)
# --- Exercice 10 ------------------------------------------------------
for n in range(1, 18):
    check("ex10a", sum(comb(n, k) for k in range(n + 1)) == 2**n)
    check("ex10b", sum((-1)**k*comb(n, k) for k in range(n + 1)) == 0)
    check("ex10c pairs", sum(comb(n, k) for k in range(0, n + 1, 2)) == 2**(n - 1))
    check("ex10d", sum(k*comb(n, k) for k in range(n + 1)) == n*2**(n - 1))
    check("ex10e", (n + 1)*sum(Fraction(comb(n, k), k + 1) for k in range(n + 1)) == 2**(n + 1) - 1)
# --- Exercice 11 ------------------------------------------------------
for n in range(1, 16):
    check("ex11a", sum(i + j for i in range(1, n + 1) for j in range(1, n + 1)) == n*n*(n + 1))
    check("ex11b", sum(i*j for i in range(1, n + 1) for j in range(1, n + 1)) == (n*(n + 1)//2)**2)
    check("ex11c", sum(1 for i in range(1, n + 1) for j in range(i, n + 1)) == n*(n + 1)//2)
    check("ex11d", 6*sum(j - i for i in range(1, n + 1) for j in range(i + 1, n + 1)) == n*(n - 1)*(n + 1))
# --- Exercice 12 (et exemple du cours) --------------------------------
Z = sp.symbols("Z")
sol = sp.solve([X + Y + Z - 6, X + 2*Y + 3*Z - 14, 2*X + Y - Z - 1], [X, Y, Z])
check("essentiel pivot", sol == {X: 1, Y: 2, Z: 3})
sol = sp.solve([X - Y + 2*Z - 5, 2*X + Y - Z - 2, X + 3*Y + Z], [X, Y, Z])
check("ex12a", sol == {X: 2, Y: -1, Z: 1})
sol = sp.solve([X + Y - Z - 2, 2*X - Y + Z - 1, 3*X - 3], [X, Y, Z])
check("ex12b droite", sol == {X: 1, Y: Z + 1})
# --- Exercice 13 ------------------------------------------------------
f = lambda u: (2*u + 1)/(u + 2)
check("ex13a", isclose(f(1), 1) and isclose(f(3), 7/5) and all(f(1) <= f(1 + i/50) <= f(3) for i in range(101)))
for n in range(1, 200):
    s = sum(Fraction(1, k) for k in range(n + 1, 2*n + 1))
    check("ex13b", Fraction(1, 2) <= s < 1)
for n in range(1, 400):
    check("ex13c", sqrt(n + 1) - sqrt(n) <= 1/(2*sqrt(n)) + 1e-15)
# --- Exercice 14 ------------------------------------------------------
check("ex14a", (math.floor(2.7), math.floor(-1.2), math.floor(5), math.floor(-0.5)) == (2, -2, 5, -1))
check("ex14c", all((math.floor(2*u + 1) == 5) == (2 <= u < 2.5) for u in [i/40 for i in range(0, 160)]))
import random
random.seed(2)
for _ in range(4000):
    u, v = random.uniform(-9, 9), random.uniform(-9, 9)
    check("ex14d", math.floor(u) + math.floor(v) <= math.floor(u + v) <= math.floor(u) + math.floor(v) + 1)
    check("ex14e", math.floor(2*u) - 2*math.floor(u) in (0, 1))
# --- Exercice 15 ------------------------------------------------------
check("ex15a cos", isclose(cos(pi/12), (sqrt(6) + sqrt(2))/4))
check("ex15a sin", isclose(sin(pi/12), (sqrt(6) - sqrt(2))/4))
check("ex15b", isclose(sin(7*pi/12), (sqrt(6) + sqrt(2))/4))
aa = sp.symbols("aa", real=True)
check("ex15c cos3a", sp.simplify(sp.cos(3*aa) - (4*sp.cos(aa)**3 - 3*sp.cos(aa))) == 0)
check("ex15d tan π/12", isclose(tan(pi/12), 2 - sqrt(3)))
# --- Exercice 16 ------------------------------------------------------
sols = [kk*2*pi for kk in range(-3, 4)] + [pi/3 + kk*2*pi/3 for kk in range(-6, 7)]
check("ex16c", all(isclose(sin(2*s), sin(s), abs_tol=1e-12) for s in sols))
check("ex16d", all(isclose(2*cos(s)**2 - 3*cos(s) + 1, 0, abs_tol=1e-12)
                   for s in [0, pi/3, -pi/3, 2*pi, 7*pi/3]))
# --- Exercice 17 ------------------------------------------------------
check("ex17a", all((cos(u) <= 0.5 + 1e-12) == (pi/3 - 1e-9 <= u <= 5*pi/3 + 1e-9)
                   for u in [i*2*pi/2000 for i in range(2000)]))
check("ex17c", all((2*sin(u)**2 - 1 >= -1e-12) == (pi/4 - 1e-9 <= u <= 3*pi/4 + 1e-9
                   or 5*pi/4 - 1e-9 <= u <= 7*pi/4 + 1e-9)
                   for u in [i*2*pi/2000 for i in range(2000)]))
# --- Exercice 18 ------------------------------------------------------
u_ = sp.tan(t/2)
check("ex18a cos", sp.simplify(sp.cos(t) - (1 - u_**2)/(1 + u_**2)) == 0)
check("ex18a sin", sp.simplify(sp.sin(t) - 2*u_/(1 + u_**2)) == 0)
check("ex18b tan π/8", isclose(tan(pi/8), sqrt(2) - 1))
w = sqrt(2) - 1
check("ex18d", isclose(2*w/(1 + w*w), sqrt(2)/2))
# --- Exercice 19 ------------------------------------------------------
for _ in range(3000):
    a_, b_ = random.uniform(0, 10), random.uniform(0, 10)
    check("ex19a AM-GM", sqrt(a_*b_) <= (a_ + b_)/2 + 1e-12)
    xs = [random.uniform(-4, 4) for _ in range(5)]
    ys = [random.uniform(-4, 4) for _ in range(5)]
    check("ex19 C-S", sum(p*q for p, q in zip(xs, ys))**2
          <= sum(p*p for p in xs)*sum(q*q for q in ys) + 1e-9)
check("ex19c", all((a_ + b_ + c_)*(1/a_ + 1/b_ + 1/c_) >= 9 - 1e-12
      for a_, b_, c_ in [(random.uniform(0.1, 9),)*1 + (random.uniform(0.1, 9), random.uniform(0.1, 9)) for _ in range(2000)]))
# --- Exercice 20 ------------------------------------------------------
for n in range(0, 16):
    for p in range(0, n + 1):
        check("ex20a hockey-stick", sum(comb(k, p) for k in range(p, n + 1)) == comb(n + 1, p + 1))
    check("ex20b Vandermonde", sum(comb(n, k)**2 for k in range(n + 1)) == comb(2*n, n))
# --- Exercice 21 ------------------------------------------------------
m = sp.symbols("m")
M = sp.Matrix([[1, 1, m], [1, m, 1], [m, 1, 1]])
check("ex21 det", sp.factor(M.det()) == -(m - 1)**2*(m + 2))
for mv in [0, 3, -1, sp.Rational(1, 2)]:
    s = sp.solve([X + Y + mv*Z - 1, X + mv*Y + Z - 1, mv*X + Y + Z - 1], [X, Y, Z])
    attendu = sp.S(1)/(sp.S(mv) + 2)
    check("ex21 unique", s == {X: attendu, Y: attendu, Z: attendu})
check("ex21 m=-2 aucune", sp.solve([X + Y - 2*Z - 1, X - 2*Y + Z - 1, -2*X + Y + Z - 1], [X, Y, Z]) == [])
# --- Exercice 22 ------------------------------------------------------
for n in range(2, 25):
    check("ex22a", isclose(math.prod(1 - 1/k for k in range(2, n + 1)), 1/n))
    check("ex22b", isclose(math.prod(1 - 1/k**2 for k in range(2, n + 1)), (n + 1)/(2*n)))
for n in range(1, 25):
    check("ex22c", sum(Fraction(1, k*(k + 1)*(k + 2)) for k in range(1, n + 1))
          == Fraction(1, 4) - Fraction(1, 2*(n + 1)*(n + 2)))
# --- Exercice 23 ------------------------------------------------------
check("ex23 équation", sp.simplify(4*sp.cos(sp.pi/5)**2 - 2*sp.cos(sp.pi/5) - 1) == 0)
check("ex23 valeur", isclose(cos(pi/5), (1 + sqrt(5))/4))
check("ex23 cos 2π/5", isclose(cos(2*pi/5), (sqrt(5) - 1)/4))
# --- Exercice 24 ------------------------------------------------------
T = [sp.Integer(1), x]
for n in range(30):
    T.append(sp.expand(2*x*T[-1] - T[-2]))
check("ex24 T2", T[2] == 2*x**2 - 1)
check("ex24 T3", T[3] == 4*x**3 - 3*x)
check("ex24 T4", T[4] == 8*x**4 - 8*x**2 + 1)
for n in range(10):
    Tn = sp.lambdify(x, T[n])
    check(f"ex24 cos(nt)=T_n(cos t) n={n}",
          all(isclose(cos(n*tv), Tn(cos(tv)), abs_tol=1e-9)
              for tv in [i*0.137 for i in range(60)]))
check("ex24 cos π/8", isclose(cos(pi/8), sqrt(2 + sqrt(2))/2))
check("ex24 8c⁴−8c²+1", isclose(8*cos(pi/8)**4 - 8*cos(pi/8)**2 + 1, 0, abs_tol=1e-12))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
