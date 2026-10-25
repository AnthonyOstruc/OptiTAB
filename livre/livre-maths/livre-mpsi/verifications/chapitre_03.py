# -*- coding: utf-8 -*-
"""Vérifications du chapitre 3 — Nombres complexes."""
import cmath
import math
from math import comb, cos, sin, pi, sqrt, isclose, log

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

def ceq(z, w, tol=1e-10):
    return abs(z - w) <= tol

# --- Exercice 1 -------------------------------------------------------
check("ex1a", (2 + 1j)*(3 - 2j) == 8 - 1j)
check("ex1b", (1 + 1j)**2 == 2j)
check("ex1c", ceq(1/(1 + 1j), (1 - 1j)/2))
check("ex1d", ceq((1 + 1j)/(2 - 1j), (1 + 3j)/5))
check("ex1e", 2026 % 4 == 2 and ceq((1j)**2026, -1))
check("ex1f", (2 - 3j)*(2 + 3j) == 13)
# --- Exercice 3 -------------------------------------------------------
check("ex3 |3+4i|", abs(3 + 4j) == 5)
check("ex3 |1-i|", isclose(abs(1 - 1j), sqrt(2)))
check("ex3 produit", isclose(abs((3 + 4j)*(1 - 1j)), 5*sqrt(2)))
check("ex3 inverse", isclose(abs(1/(2 - 1j)), sqrt(5)/5))
# --- Exercice 4 -------------------------------------------------------
check("ex4 1+i", ceq(sqrt(2)*cmath.exp(1j*pi/4), 1 + 1j))
check("ex4 √3−i", ceq(2*cmath.exp(-1j*pi/6), sqrt(3) - 1j))
check("ex4 −2", ceq(2*cmath.exp(1j*pi), -2))
check("ex4 3i", ceq(3*cmath.exp(1j*pi/2), 3j))
check("ex4 produit", ceq(2*sqrt(2)*cmath.exp(1j*5*pi/12), (1 + 1j)*(sqrt(3) + 1j)))
# --- Exercice 5 -------------------------------------------------------
for t in [0.1 + 0.37*k for k in range(30)]:
    check("ex5 cos²", isclose(cos(t)**2, (1 + cos(2*t))/2))
    check("ex5 sin³", isclose(sin(t)**3, (3*sin(t) - sin(3*t))/4))
    check("ex5 cos·sin²", isclose(cos(t)*sin(t)**2, (cos(t) - cos(3*t))/4))
# --- Exercice 6 -------------------------------------------------------
for t in [0.2 + 0.31*k for k in range(25)]:
    check("ex6 cos3t", isclose(cos(3*t), cos(t)**3 - 3*cos(t)*sin(t)**2))
    check("ex6 sin3t", isclose(sin(3*t), 3*cos(t)**2*sin(t) - sin(t)**3))
# --- Exercice 7 -------------------------------------------------------
z = sp.symbols("z")
check("ex7a", set(sp.solve(z**2 + z + 1)) == {sp.Rational(-1, 2) - sp.sqrt(3)*sp.I/2,
                                              sp.Rational(-1, 2) + sp.sqrt(3)*sp.I/2})
check("ex7b", set(sp.solve(z**2 - 2*z + 5)) == {1 - 2*sp.I, 1 + 2*sp.I})
check("ex7c", set(sp.solve(z**2 + 4)) == {-2*sp.I, 2*sp.I})
# --- Exercice 8 -------------------------------------------------------
check("ex8a", ceq((1 + 1j)**12, -64))
check("ex8b", ceq((sqrt(3) + 1j)**6, -64, 1e-8))
check("ex8c", ceq(((1 + 1j*sqrt(3))/(1 - 1j))**12, -64, 1e-8))
# --- Exercice 9 -------------------------------------------------------
w = (1 + 1j*sqrt(3))/(1 + 1j)
check("ex9 module", isclose(abs(w), sqrt(2)))
check("ex9 argument", isclose(cmath.phase(w), pi/12))
check("ex9 forme algébrique", ceq(w, (1 + sqrt(3))/2 + 1j*(sqrt(3) - 1)/2))
check("ex9 cos π/12", isclose(cos(pi/12), (sqrt(6) + sqrt(2))/4))
check("ex9 sin π/12", isclose(sin(pi/12), (sqrt(6) - sqrt(2))/4))
# --- Exercice 10 ------------------------------------------------------
import random
random.seed(3)
for _ in range(4000):
    a = complex(random.uniform(-5, 5), random.uniform(-5, 5))
    b = complex(random.uniform(-5, 5), random.uniform(-5, 5))
    check("ex10a", abs(abs(a) - abs(b)) <= abs(a - b) + 1e-12)
    if abs(a) <= 1:
        check("ex10c |z²+z|≤2", abs(a*a + a) <= 2 + 1e-12)
        check("ex10c |1+z|≥1−|z|", abs(1 + a) >= 1 - abs(a) - 1e-12)
# --- Exercice 11 ------------------------------------------------------
for t in [0.1 + 0.3*k for k in range(20)]:
    check("ex11 1+e^it", ceq(1 + cmath.exp(1j*t), 2*cos(t/2)*cmath.exp(1j*t/2)))
    check("ex11 1−e^it", ceq(1 - cmath.exp(1j*t), -2j*sin(t/2)*cmath.exp(1j*t/2)))
for p, q in [(0.5, 1.7), (2.2, 0.3), (1.1, 2.9)]:
    check("ex11 e^ip+e^iq", ceq(cmath.exp(1j*p) + cmath.exp(1j*q),
          2*cos((p - q)/2)*cmath.exp(1j*(p + q)/2)))
    check("ex11 cos p+cos q", isclose(cos(p) + cos(q), 2*cos((p + q)/2)*cos((p - q)/2)))
# --- Exercice 12 ------------------------------------------------------
for n in range(1, 12):
    for t in [0.3, 1.1, 2.7]:
        S = sum(cmath.exp(1j*k*t) for k in range(n + 1))
        check("ex12 somme exp", ceq(S, cmath.exp(1j*n*t/2)*sin((n + 1)*t/2)/sin(t/2)))
        check("ex12 somme cos", isclose(sum(cos(k*t) for k in range(n + 1)),
              cos(n*t/2)*sin((n + 1)*t/2)/sin(t/2)))
        check("ex12 somme sin", isclose(sum(sin(k*t) for k in range(n + 1)),
              sin(n*t/2)*sin((n + 1)*t/2)/sin(t/2)))
# --- Exercice 13 ------------------------------------------------------
check("ex13 √(3+4i)", (2 + 1j)**2 == 3 + 4j)
check("ex13 √(−5+12i)", (2 + 3j)**2 == -5 + 12j)
r = sp.solve(z**2 - (3 + 2*sp.I)*z + 5 + 5*sp.I)
check("ex13b racines", set(r) == {2 - sp.I, 1 + 3*sp.I})
check("ex13b somme/produit", sp.simplify((2 - sp.I) + (1 + 3*sp.I) - (3 + 2*sp.I)) == 0
      and sp.simplify((2 - sp.I)*(1 + 3*sp.I) - (5 + 5*sp.I)) == 0)
# --- Exercice 14 ------------------------------------------------------
check("ex14a", set(sp.solve(z**2 - 2*z + 2)) == {1 - sp.I, 1 + sp.I})
check("ex14b", set(sp.solve(z**2 - z + 1)) ==
      {sp.Rational(1, 2) - sp.sqrt(3)*sp.I/2, sp.Rational(1, 2) + sp.sqrt(3)*sp.I/2})
# --- Exercice 15 ------------------------------------------------------
for t in [0.1 + 0.29*k for k in range(25)]:
    check("ex15a", isclose(cos(t) + sin(t), sqrt(2)*cos(t - pi/4)))
    check("ex15b", isclose(sqrt(3)*cos(t) - sin(t), 2*cos(t + pi/6)))
for s in [0, pi/2]:
    check("ex15c", isclose(cos(s) + sin(s), 1))
check("ex15d", isclose(max(3*cos(k/500) + 4*sin(k/500) for k in range(4000)), 5, abs_tol=1e-4))
# --- Exercice 16 ------------------------------------------------------
j3 = cmath.exp(2j*pi/3)
check("ex16 j³", ceq(j3**3, 1))
check("ex16 1+j+j²", ceq(1 + j3 + j3**2, 0))
check("ex16 j²=conj", ceq(j3**2, j3.conjugate()))
check("ex16 (1+j)³", ceq((1 + j3)**3, -1))
for n in range(2, 12):
    check("ex16 somme Un", ceq(sum(cmath.exp(2j*pi*k/n) for k in range(n)), 0))
A, B = sp.symbols("A B")
jj = sp.Rational(-1, 2) + sp.sqrt(3)*sp.I/2
check("ex16 a³+b³", sp.expand((A + B)*(A + jj*B)*(A + jj**2*B) - (A**3 + B**3)) == 0)
# --- Exercice 17 ------------------------------------------------------
roots = [2*cmath.exp(1j*(pi/6 + 2*k*pi/3)) for k in range(3)]
check("ex17a racines cubiques de 8i", all(ceq(r**3, 8j, 1e-8) for r in roots))
check("ex17a formes", ceq(roots[0], sqrt(3) + 1j) and ceq(roots[1], -sqrt(3) + 1j)
      and ceq(roots[2], -2j))
check("ex17b", all(ceq(r**4, -4) for r in [1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]))
check("ex17c", all(ceq(cmath.exp(2j*pi*k/6)**6, 1) for k in range(6)))
# --- Exercice 18 ------------------------------------------------------
check("ex18a", ceq(cmath.exp(2 + 1j*pi/3), math.exp(2)*(0.5 + 1j*sqrt(3)/2)))
check("ex18c", ceq(cmath.exp(log(2) + 1j*pi), -2))
check("ex18d", ceq(cmath.exp(log(2)/2 + 1j*pi/4), 1 + 1j))
# --- Exercice 19 ------------------------------------------------------
a3, b3, c3 = 1 + 1j, 3 + 2j, 7 + 4j
check("ex19a alignés", abs(((c3 - a3)/(b3 - a3)).imag) < 1e-12)
a3, b3, c3 = 1 + 1j, 2 + 3j, -1 + 2j
q = (c3 - a3)/(b3 - a3)
check("ex19b angle droit", abs(q.real) < 1e-12 and ceq(q, 1j))
check("ex19b isocèle", isclose(abs(b3 - a3), abs(c3 - a3)))
a3, b3, c3 = 0, 2, 1 + 1j*sqrt(3)
check("ex19c équilatéral", ceq(a3 + j3*b3 + j3**2*c3, 0, 1e-9))
check("ex19c longueurs", isclose(abs(b3 - a3), abs(c3 - b3)) and isclose(abs(c3 - a3), 2))
check("ex19c e^{iπ/3}=−j²", ceq(cmath.exp(1j*pi/3), -j3**2))
# --- Exercice 20 ------------------------------------------------------
f20 = lambda w: (1 + 1j)*w + 2 - 1j
om = 1 + 2j
check("ex20 point fixe", ceq(f20(om), om))
for _ in range(300):
    w = complex(random.uniform(-4, 4), random.uniform(-4, 4))
    check("ex20 similitude", ceq(f20(w) - om, (1 + 1j)*(w - om)))
check("ex20 rapport/angle", isclose(abs(1 + 1j), sqrt(2)) and isclose(cmath.phase(1 + 1j), pi/4))
# --- Exercice 21 ------------------------------------------------------
for _ in range(2000):
    xx, yy = random.uniform(-6, 6), random.uniform(-6, 6)
    w = complex(xx, yy)
    check("ex21a médiatrice", (abs(abs(w - 1) - abs(w + 1j)) < 1e-9) == (abs(yy + xx) < 1e-9)
          or abs(abs(w - 1) - abs(w + 1j)) >= 1e-9)
# sur la droite y=−x, égalité des distances :
for xx in [k/10 for k in range(-50, 51)]:
    w = complex(xx, -xx)
    check("ex21a égalité sur y=−x", isclose(abs(w - 1), abs(w + 1j)))
# (z−1)/(z−i) réel ssi aligné avec 1 et i (droite x+y=1)
for xx in [k/10 for k in range(-30, 31)]:
    w = complex(xx, 1 - xx)
    if abs(w - 1j) > 1e-9:
        check("ex21c réel sur la droite", abs(((w - 1)/(w - 1j)).imag) < 1e-9)
# (z−1)/(z−i) imaginaire pur ssi sur le cercle de diamètre [1, i]
cc, rr = (1 + 1j)/2, abs(1 - 1j)/2
for th in [k*2*pi/100 for k in range(100)]:
    w = cc + rr*cmath.exp(1j*th)
    if abs(w - 1j) > 1e-9 and abs(w - 1) > 1e-9:
        check("ex21d imaginaire pur sur le cercle", abs(((w - 1)/(w - 1j)).real) < 1e-9)
# --- Exercice 22 ------------------------------------------------------
for n in range(1, 14):
    for t in [0.4, 1.3, 2.1]:
        check("ex22a", ceq((1 + cmath.exp(1j*t))**n,
              2**n*cos(t/2)**n*cmath.exp(1j*n*t/2), 1e-7))
        check("ex22b cos", isclose(sum(comb(n, k)*cos(k*t) for k in range(n + 1)),
              2**n*cos(t/2)**n*cos(n*t/2)))
        check("ex22b sin", isclose(sum(comb(n, k)*sin(k*t) for k in range(n + 1)),
              2**n*cos(t/2)**n*sin(n*t/2)))
    check("ex22c t=π/2", isclose(sum(comb(n, k)*cos(k*pi/2) for k in range(n + 1)),
          2**(n/2)*cos(n*pi/4), abs_tol=1e-8))
# --- Exercice 23 ------------------------------------------------------
om5 = cmath.exp(2j*pi/5)
check("ex23a somme", ceq(sum(om5**k for k in range(5)), 0))
u5 = om5 + om5**4
v5 = om5**2 + om5**3
check("ex23b u réel", abs(u5.imag) < 1e-12 and isclose(u5.real, 2*cos(2*pi/5)))
check("ex23b u+v", ceq(u5 + v5, -1))
check("ex23b uv", ceq(u5*v5, -1))
check("ex23c u", isclose(u5.real, (-1 + sqrt(5))/2))
check("ex23c cos 2π/5", isclose(cos(2*pi/5), (sqrt(5) - 1)/4))
check("ex23d cos π/5", isclose(cos(pi/5), (1 + sqrt(5))/4) and isclose(-v5.real/2, cos(pi/5)))
# --- Exercice 24 ------------------------------------------------------
for n in range(1, 12):
    for t in [0.3, 1.2, 2.5]:
        D = sum(cmath.exp(1j*k*t) for k in range(-n, n + 1))
        check("ex24a Dirichlet", ceq(D, sin((2*n + 1)*t/2)/sin(t/2)))
        check("ex24b", isclose(1 + 2*sum(cos(k*t) for k in range(1, n + 1)),
              sin((2*n + 1)*t/2)/sin(t/2)))
    check("ex24c", isclose(sum(cos(2*k*pi/(2*n + 1)) for k in range(1, n + 1)), -0.5))
check("ex24d n=1", isclose(cos(2*pi/3), -0.5))
check("ex24d n=2", isclose(cos(2*pi/5) + cos(4*pi/5), -0.5))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
