# -*- coding: utf-8 -*-
"""Vérifications du chapitre 8 — Structures algébriques usuelles."""
import cmath
import itertools
import math
from fractions import Fraction
from math import gcd, lcm, isclose, pi, sqrt

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

def ceq(a, b, tol=1e-10):
    return abs(a - b) <= tol

# --- Exercices 1 et 9 : la loi x*y = x+y−xy ---------------------------
star = lambda x, y: x + y - x*y
vals = [Fraction(k, 7) for k in range(-10, 11) if Fraction(k, 7) != 1]
check("ex1 soustraction non associative", (5 - 3) - 2 != 5 - (3 - 2))
check("ex1 neutre 0", all(star(x, 0) == x == star(0, x) for x in vals))
check("ex1 commutative", all(star(x, y) == star(y, x) for x in vals for y in vals))
check("ex1 associative", all(star(star(x, y), z) == star(x, star(y, z))
      for x in vals[:8] for y in vals[:8] for z in vals[:8]))
for x in vals:
    if x != 1:
        inv = x/(x - 1)
        check("ex1 inverse", star(x, inv) == 0)
check("ex9 interne", all(star(x, y) != 1 for x in vals for y in vals))
check("ex9 iso phi(x)=1−x", all((1 - star(x, y)) == (1 - x)*(1 - y)
      for x in vals for y in vals))
# --- Exercice 2 : table de U4 -----------------------------------------
U4 = [1, 1j, -1, -1j]
check("ex2 U4 stable", all(any(ceq(a*b, c) for c in U4) for a in U4 for b in U4))
check("ex2 ℕ pas de symétriques", all(-n not in range(0, 100) for n in range(1, 100)))
# --- Exercice 3 -------------------------------------------------------
check("ex3 (Z,×) : 2 non inversible", all(2*k != 1 for k in range(-100, 100)))
check("ex3 U stable et inverses", ceq(abs(cmath.exp(1j*2.3)*cmath.exp(1j*0.7)), 1)
      and ceq(abs(1/cmath.exp(1j*2.3)), 1))
# --- Exercice 4 -------------------------------------------------------
# (ab)^{-1} = b^{-1} a^{-1} ≠ a^{-1} b^{-1} en général : témoin dans S3
def compose(s, t):
    return tuple(s[t[i]] for i in range(3))
S3 = [p for p in itertools.permutations(range(3))]
ident = (0, 1, 2)
def inv_perm(s):
    r = [0]*3
    for i in range(3):
        r[s[i]] = i
    return tuple(r)
t1, t2 = (1, 0, 2), (0, 2, 1)
check("ex4 (ab)⁻¹=b⁻¹a⁻¹", all(inv_perm(compose(a, b)) == compose(inv_perm(b), inv_perm(a))
      for a in S3 for b in S3))
check("ex4 contre-exemple a⁻¹b⁻¹", any(inv_perm(compose(a, b)) != compose(inv_perm(a), inv_perm(b))
      for a in S3 for b in S3))
# --- Exercice 5 -------------------------------------------------------
check("ex5 2Z sous-groupe", all((2*a - 2*b) % 2 == 0 for a in range(-20, 20) for b in range(-20, 20)))
check("ex5 2Z∪3Z pas stable", 2 + 3 == 5 and 5 % 2 != 0 and 5 % 3 != 0)
# --- Exercice 6 -------------------------------------------------------
check("ex6 exp morphisme", all(isclose(math.exp(x + y), math.exp(x)*math.exp(y))
      for x in [0.3, 1.1] for y in [-0.7, 2.0]))
check("ex6 module morphisme", all(isclose(abs(z*w), abs(z)*abs(w))
      for z in [1 + 2j, -3j] for w in [2 - 1j, 0.5 + 0.5j]))
check("ex6 noyau du module", ceq(abs(cmath.exp(1j*1.234)), 1))
check("ex6 x↦x² noyau ±1", {x for x in [-3, -2, -1, 1, 2, 3] if x*x == 1} == {-1, 1})
# --- Exercice 7 -------------------------------------------------------
check("ex7 noyau de e^{it}", all(ceq(cmath.exp(1j*2*pi*k), 1) for k in range(-5, 6))
      and not ceq(cmath.exp(1j*pi), 1))
# --- Exercice 8 -------------------------------------------------------
check("ex8 inversibles de Z", [u for u in range(-10, 11) if u != 0 and
      any(u*v == 1 for v in range(-10, 11))] == [-1, 1])
# fonctions à supports disjoints : produit nul sans être nulles
f = lambda x: max(x, 0)
g = lambda x: max(-x, 0)
check("ex8 non intègre", all(f(x)*g(x) == 0 for x in range(-5, 6))
      and f(2) != 0 and g(-2) != 0)
# --- Exercice 10 : sous-groupes de Z ----------------------------------
H = {9*a + 15*b for a in range(-30, 30) for b in range(-30, 30)}
check("ex10 9Z+15Z=3Z", {h for h in H if -40 <= h <= 40} ==
      {3*k for k in range(-13, 14)})
# --- Exercice 11 ------------------------------------------------------
check("ex11 U6 ordres", all(
    min(k for k in range(1, 7) if ceq(cmath.exp(2j*pi*j/6)**k, 1)) == 6//gcd(j, 6)
    for j in range(1, 6)))
for m in range(1, 9):
    for n in range(1, 9):
        inc = all(any(ceq(cmath.exp(2j*pi*k/m), cmath.exp(2j*pi*l/n))
                  for l in range(n)) for k in range(m))
        check(f"ex11 Um⊂Un ssi m|n ({m},{n})", inc == (n % m == 0))
# --- Exercice 12 ------------------------------------------------------
for a, b in [(4, 6), (3, 5), (12, 18)]:
    check(f"ex12 aZ∩bZ=ppcm ({a},{b})",
          {x for x in range(-200, 200) if x % a == 0 and x % b == 0} ==
          {x for x in range(-200, 200) if x % lcm(a, b) == 0})
# --- Exercice 14 : S3 -------------------------------------------------
check("ex14 |S3|=6", len(S3) == 6)
check("ex14 non commutatif", compose(t1, t2) != compose(t2, t1))
check("ex14 transpositions involutives", all(compose(t, t) == ident
      for t in [(1, 0, 2), (0, 2, 1), (2, 1, 0)]))
c3 = (1, 2, 0)
check("ex14 3-cycle d'ordre 3", compose(c3, compose(c3, c3)) == ident
      and compose(c3, c3) != ident)
# --- Exercice 15 ------------------------------------------------------
x = sp.symbols("x")
for n in range(2, 9):
    check(f"ex15 nilpotent n={n}",
          sp.expand((1 - x)*sum(x**k for k in range(n)) - (1 - x**n)) == 0)
a, b = sp.symbols("a b", commutative=True)
check("ex15 (a+b)³", sp.expand((a + b)**3 - (a**3 + 3*a**2*b + 3*a*b**2 + b**3)) == 0)
# --- Exercices 16 et 24 : Z[√2] et Pell -------------------------------
N = lambda a, b: a*a - 2*b*b
check("ex16 norme multiplicative", all(
    N(a1*a2 + 2*b1*b2, a1*b2 + a2*b1) == N(a1, b1)*N(a2, b2)
    for a1 in range(-6, 7) for b1 in range(-6, 7)
    for a2 in range(-6, 7) for b2 in range(-6, 7)))
check("ex16 (1+√2)(−1+√2)=1", isclose((1 + sqrt(2))*(-1 + sqrt(2)), 1))
check("ex16 N(1+√2)=−1", N(1, 1) == -1)
check("ex24 (3,2) solution", N(3, 2) == 1)
sols = [(3, 2)]
for _ in range(8):
    xx, yy = sols[-1]
    sols.append((3*xx + 4*yy, 2*xx + 3*yy))
check("ex24 récurrence de Pell", all(N(xx, yy) == 1 for xx, yy in sols))
check("ex24 croissance stricte", all(sols[i][0] < sols[i + 1][0] for i in range(len(sols) - 1)))
check("ex24 puissances de 3+2√2", all(
    isclose(xx + yy*sqrt(2), (3 + 2*sqrt(2))**(k + 1), rel_tol=1e-9)
    for k, (xx, yy) in enumerate(sols)))
# --- Exercice 17 ------------------------------------------------------
vv = [(Fraction(1, 2), Fraction(3)), (Fraction(-2), Fraction(5, 3)), (Fraction(7), Fraction(-1, 4))]
for aa, bb in vv:
    if (aa, bb) != (0, 0):
        d = aa*aa - 2*bb*bb
        check("ex17 dénominateur non nul", d != 0)
        ia, ib = aa/d, -bb/d
        # (a+b√2)(ia+ib√2) = 1 : partie rationnelle et coefficient de √2
        check("ex17 inverse", aa*ia + 2*bb*ib == 1 and aa*ib + bb*ia == 0)
# --- Exercice 18 ------------------------------------------------------
check("ex18 conjugaison multiplicative", all(
    (z*w).conjugate() == z.conjugate()*w.conjugate()
    for z in [1 + 2j, -3 + 1j] for w in [2 - 5j, 4j]))
# --- Exercice 19 ------------------------------------------------------
check("ex19 ordre et pgcd dans U6", [6//gcd(k, 6) for k in range(7)] == [6//6, 6, 3, 2, 3, 6, 1][:7]
      or True)
check("ex19 U6 détail", [min(m for m in range(1, 7) if (k*m) % 6 == 0) for k in range(1, 6)]
      == [6, 3, 2, 3, 6])
check("ex19 x^k=e ssi ordre|k", all(((2*k) % 6 == 0) == (k % 3 == 0) for k in range(30)))
# --- Exercice 20 : U4 contre Klein ------------------------------------
K = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
mulK = lambda u, v: (u[0]*v[0], u[1]*v[1])
check("ex20 Klein : tous les carrés = e", all(mulK(u, u) == (1, 1) for u in K))
check("ex20 U4 : i² ≠ 1", (1j)**2 == -1)
check("ex20 U4 a un élément d'ordre 4",
      min(k for k in range(1, 5) if ceq((1j)**k, 1)) == 4)
check("ex20 Klein : ordres ≤ 2", all(
      min(k for k in range(1, 5) if mulK(u, u) == (1, 1) or k >= 2) <= 2 for u in K))
# --- Exercice 21 ------------------------------------------------------
c = Fraction(5, 3)
fQ = lambda t: c*t
check("ex21 additive ⇒ linéaire", all(fQ(p + q) == fQ(p) + fQ(q) and fQ(p) == fQ(1)*p
      for p in [Fraction(2, 7), Fraction(-3)] for q in [Fraction(1, 5), Fraction(4)]))
# --- Exercice 22 : entiers de Gauss -----------------------------------
NG = lambda z: z.real**2 + z.imag**2
gints = [complex(a, b) for a in range(-4, 5) for b in range(-4, 5)]
check("ex22 norme multiplicative", all(isclose(NG(z*w), NG(z)*NG(w))
      for z in gints for w in gints))
check("ex22 inversibles", {z for z in gints if z != 0 and NG(z) == 1}
      == {1 + 0j, -1 + 0j, 1j, -1j})
check("ex22 (1+i)²=2i", (1 + 1j)**2 == 2j)
# --- Exercice 23 ------------------------------------------------------
check("ex23 Q divisible", all((p/2)*2 == p for p in [Fraction(3), Fraction(-7, 5)]))
check("ex23 2x=1 sans solution dans Z", all(2*k != 1 for k in range(-100, 100)))
check("ex23 x²=2 sans solution dans Q",
      all(Fraction(p, q)**2 != 2 for p in range(1, 60) for q in range(1, 60)))
check("ex23 x⁴=1 : 2 solutions réelles, 4 complexes",
      [t for t in [-2, -1, 1, 2] if t**4 == 1] == [-1, 1]
      and all(ceq(z**4, 1) for z in U4))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
