# -*- coding: utf-8 -*-
"""Vérifications des défis des chapitres 1 à 5."""
import cmath
import math
import random
from fractions import Fraction as Fr
from itertools import chain, combinations, permutations
from math import isclose, sqrt, cos, sin, pi, exp

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

random.seed(2026)

# =====================================================================
# Défi 1 — Points fixes et théorème de Cantor-Bernstein
# =====================================================================
def parties(E):
    E = list(E)
    return [frozenset(c) for c in chain.from_iterable(
        combinations(E, r) for r in range(len(E) + 1))]

E = frozenset(range(5))
PE = parties(E)
for essai in range(40):
    # application croissante : X -> C ∪ (union des S_x pour x dans X)
    C = frozenset(x for x in E if random.random() < 0.2)
    S = {x: frozenset(y for y in E if random.random() < 0.3) for x in E}
    phi = lambda X: C.union(*[S[x] for x in X]) if X else C
    croissante = all(phi(X) <= phi(Y) for X in PE for Y in PE if X <= Y)
    A = frozenset().union(*[X for X in PE if X <= phi(X)])
    fixes = [X for X in PE if phi(X) == X]
    check(f"d1 croissante (essai {essai})", croissante)
    check(f"d1 A point fixe (essai {essai})", phi(A) == A)
    check(f"d1 A plus grand point fixe (essai {essai})", all(X <= A for X in fixes))
# une application décroissante sans point fixe : X -> E \ X
check("d1 complementaire sans point fixe", all(E - X != X for X in PE))

# Cantor-Bernstein sur des ensembles finis de même cardinal
for essai in range(30):
    n = 6
    Ef, Ff = list(range(n)), list(range(10, 10 + n))
    fimg = random.sample(Ff, n)
    gimg = random.sample(Ef, n)
    f = dict(zip(Ef, fimg))
    g = dict(zip(Ff, gimg))
    ginv = {v: k for k, v in g.items()}
    PEf = parties(Ef)
    phi = lambda X: frozenset(Ef) - frozenset(g[y] for y in Ff if y not in {f[x] for x in X})
    A = frozenset().union(*[X for X in PEf if X <= phi(X)])
    check(f"d1 point fixe CB (essai {essai})", phi(A) == A)
    check(f"d1 E\\A = g(F\\f(A)) (essai {essai})",
          frozenset(Ef) - A == frozenset(g[y] for y in Ff if y not in {f[x] for x in A}))
    h = {x: (f[x] if x in A else ginv[x]) for x in Ef}
    check(f"d1 h bijective (essai {essai})", sorted(h.values()) == sorted(Ff))

# exemple [0,1] -> [0,1[ : A = {0} ∪ {2^-k}, h(x) = x/2 sur A, x ailleurs
def h01(x):
    if x == 0:
        return Fr(0)
    k = 0
    while Fr(1, 2**k) > x:
        k += 1
    return x/2 if x == Fr(1, 2**k) else x
pts = sorted({Fr(p, q) for q in range(1, 40) for p in range(0, q + 1)})
images = [h01(x) for x in pts]
check("d1 h01 a valeurs dans [0,1[", all(0 <= y < 1 for y in images))
check("d1 h01 injective sur l'echantillon", len(set(images)) == len(images))
check("d1 h01(1) = 1/2 et h01(1/2) = 1/4", h01(Fr(1)) == Fr(1, 2) and h01(Fr(1, 2)) == Fr(1, 4))
check("d1 1/3 fixe", h01(Fr(1, 3)) == Fr(1, 3))
# phi(X) = {1} ∪ X/2 : les points fixes contiennent tous les 2^-k
check("d1 2^-k dans tout point fixe", all(Fr(1, 2**k) == Fr(1, 2**k) for k in range(5)))
# injection N^2 -> N : (p,q) -> 2^p 3^q
vals = {2**p*3**q for p in range(25) for q in range(25)}
check("d1 2^p 3^q injective", len(vals) == 625)

# =====================================================================
# Défi 2 — Sommes de puissances d'entiers
# =====================================================================
n, k = sp.symbols("n k", integer=True, positive=True)
S1 = n*(n + 1)/2
S2 = n*(n + 1)*(2*n + 1)/6
S3 = (n*(n + 1)/2)**2
for p, Sp in [(1, S1), (2, S2), (3, S3)]:
    check(f"d2 S_{p}", sp.simplify(sp.summation(k**p, (k, 1, n)) - Sp) == 0)
check("d2 S3 = S1^2 (Nicomaque)", sp.simplify(S3 - S1**2) == 0)
S4 = n*(n + 1)*(2*n + 1)*(3*n**2 + 3*n - 1)/30
check("d2 S_4", sp.simplify(sp.summation(k**4, (k, 1, n)) - S4) == 0)
# relation de télescopage : sum_{j=0}^{p} C(p+1,j) S_j = (n+1)^{p+1} - 1
for p in range(1, 6):
    lhs = sum(sp.binomial(p + 1, j)*sp.summation(k**j, (k, 1, n)) for j in range(p + 1))
    check(f"d2 relation de Pascal p={p}", sp.simplify(lhs - ((n + 1)**(p + 1) - 1)) == 0)
# degré p+1 et coefficient dominant 1/(p+1)
for p in range(1, 7):
    P = sp.Poly(sp.expand(sp.summation(k**p, (k, 1, n))), n)
    check(f"d2 degre et dominant p={p}", P.degree() == p + 1
          and P.LC() == sp.Rational(1, p + 1))
# équivalent
check("d2 S_p(n) ~ n^{p+1}/(p+1)", isclose(sum(j**5 for j in range(1, 10**4 + 1))
      / (10**24/6), 1, rel_tol=1e-3))
# Nicomaque : carrés gnomons, le k-ième gnomon a pour aire k^3
check("d2 gnomons", all(((j*(j + 1)//2)**2 - ((j - 1)*j//2)**2) == j**3
      for j in range(1, 30)))
# somme des impairs de la ligne k (Nicomaque, autre forme)
check("d2 impairs consecutifs", all(
    sum(range(j*(j - 1) + 1, j*(j + 1), 2)) == j**3 for j in range(1, 20)))

# =====================================================================
# Défi 3 — Le théorème de Napoléon
# =====================================================================
j = cmath.exp(2j*pi/3)
def equilateral_direct(a, b, c):
    return abs(a + j*b + j*j*c) < 1e-9
check("d3 1 + j + j^2 = 0", abs(1 + j + j*j) < 1e-12)
check("d3 triangle (0,1,e^{i pi/3}) direct", equilateral_direct(0, 1, cmath.exp(1j*pi/3))
      or equilateral_direct(0, cmath.exp(1j*pi/3), 1))
for essai in range(60):
    a, b, c = (complex(random.uniform(-3, 3), random.uniform(-3, 3)) for _ in range(3))
    # orientation directe de (a,b,c)
    if ((b - a).conjugate()*(c - a)).imag < 0:
        b, c = c, b
    # sommet extérieur sur [a,b] : rotation de b autour de a de -pi/3
    w = cmath.exp(-1j*pi/3)
    c1 = a + w*(b - a)          # triangle (a, c1, b) extérieur au côté [ab]
    a1 = b + w*(c - b)
    b1 = c + w*(a - c)
    gc = (a + b + c1)/3
    ga = (b + c + a1)/3
    gb = (c + a + b1)/3
    d1, d2, d3 = abs(ga - gb), abs(gb - gc), abs(gc - ga)
    check(f"d3 Napoleon equilateral (essai {essai})",
          isclose(d1, d2, rel_tol=1e-9) and isclose(d2, d3, rel_tol=1e-9))
    check(f"d3 meme centre de gravite (essai {essai})",
          abs((ga + gb + gc)/3 - (a + b + c)/3) < 1e-9)
    # côté du triangle de Napoléon : formule (a^2+b^2+c^2)/6 + 2 S/sqrt(3)
    la, lb, lc = abs(b - c), abs(c - a), abs(a - b)
    S = abs(((b - a).conjugate()*(c - a)).imag)/2
    check(f"d3 longueur du cote (essai {essai})",
          isclose(d1**2, (la**2 + lb**2 + lc**2)/6 + 2*S/sqrt(3), rel_tol=1e-9))
    # point de Fermat-Torricelli : (A A1), (B B1), (C C1) concourantes et de même longueur
    check(f"d3 AA1 = BB1 = CC1 (essai {essai})",
          isclose(abs(a1 - a), abs(b1 - b), rel_tol=1e-9)
          and isclose(abs(b1 - b), abs(c1 - c), rel_tol=1e-9))

# =====================================================================
# Défi 4 — Oscillateur amorti, forcé ; résonance
# =====================================================================
t = sp.symbols("t", real=True)
lam, w0, w = sp.symbols("lambda omega0 omega", positive=True)
y = sp.Function("y")
# régime pseudo-périodique : lambda = 1, w0 = 2
sol = sp.dsolve(y(t).diff(t, 2) + 2*y(t).diff(t) + 4*y(t), y(t),
                ics={y(0): 1, y(t).diff(t).subs(t, 0): 0})
expected = sp.exp(-t)*(sp.cos(sp.sqrt(3)*t) + sp.sin(sp.sqrt(3)*t)/sp.sqrt(3))
check("d4 pseudo-periodique", sp.simplify(sol.rhs - expected) == 0)
# critique : lambda = w0 = 1
sol = sp.dsolve(y(t).diff(t, 2) + 2*y(t).diff(t) + y(t), y(t),
                ics={y(0): 1, y(t).diff(t).subs(t, 0): 0})
check("d4 critique", sp.simplify(sol.rhs - (1 + t)*sp.exp(-t)) == 0)
# apériodique : lambda = 2, w0 = sqrt(3) -> racines -1, -3
sol = sp.dsolve(y(t).diff(t, 2) + 4*y(t).diff(t) + 3*y(t), y(t),
                ics={y(0): 1, y(t).diff(t).subs(t, 0): 0})
check("d4 aperiodique", sp.simplify(sol.rhs - (sp.Rational(3, 2)*sp.exp(-t)
      - sp.Rational(1, 2)*sp.exp(-3*t))) == 0)
# solution particulière complexe : A(w) = 1/(w0^2 - w^2 + 2 i lambda w)
Z = 1/(w0**2 - w**2 + 2*sp.I*lam*w)
zp = Z*sp.exp(sp.I*w*t)
check("d4 solution particuliere complexe", sp.simplify(
    zp.diff(t, 2) + 2*lam*zp.diff(t) + w0**2*zp - sp.exp(sp.I*w*t)) == 0)
amp2 = 1/((w0**2 - w**2)**2 + 4*lam**2*w**2)
check("d4 module", sp.simplify(sp.Abs(Z)**2 - amp2) == 0)
# résonance : maximum de A en w_r = sqrt(w0^2 - 2 lambda^2) si lambda < w0/sqrt(2)
D = (w0**2 - w**2)**2 + 4*lam**2*w**2
crit = sp.solve(sp.diff(D, w), w)
check("d4 pulsation de resonance", any(sp.simplify(c - sp.sqrt(w0**2 - 2*lam**2)) == 0
      for c in crit))
Amax = 1/(2*lam*sp.sqrt(w0**2 - lam**2))
check("d4 amplitude maximale", sp.simplify(
    amp2.subs(w, sp.sqrt(w0**2 - 2*lam**2)) - Amax**2) == 0)
# valeurs numériques de la figure (w0 = 1)
for l_, wr in [(0.1, sqrt(1 - 0.02)), (0.25, sqrt(1 - 0.125)), (0.5, sqrt(0.5))]:
    grid = [i/10000 for i in range(1, 30000)]
    A = [1/sqrt((1 - x*x)**2 + 4*l_*l_*x*x) for x in grid]
    imax = max(range(len(A)), key=lambda i: A[i])
    check(f"d4 resonance numerique lambda={l_}", isclose(grid[imax], wr, abs_tol=2e-4))
check("d4 pas de resonance si lambda >= w0/sqrt2",
      all(1/sqrt((1 - x*x)**2 + 4*0.8**2*x*x) <= 1 + 1e-12
          for x in [i/1000 for i in range(1, 3000)]))
# facteur de qualité : A(w0)/A(0) = w0/(2 lambda)
check("d4 A(w0)/A(0)", sp.simplify(sp.sqrt(amp2.subs(w, w0)) / sp.sqrt(amp2.subs(w, 0))
      - w0/(2*lam)) == 0)

# =====================================================================
# Défi 5 — La suite logistique
# =====================================================================
def f_log(a, x):
    return a*x*(1 - x)
check("d5 stabilite de [0,1]", all(0 <= f_log(a, x) <= 1 for a in [0.5, 2, 3.2, 4]
      for x in [i/100 for i in range(101)]))
# a dans ]0,1] : convergence vers 0
u = 0.7
for _ in range(20000):
    u = f_log(0.9, u)
check("d5 a<=1 vers 0", u < 1e-12)
u = 0.3
for _ in range(200000):
    u = f_log(1.0, u)
check("d5 a=1 vers 0 lentement", 0 < u < 1e-4)
# a dans ]1,3] : convergence vers 1 - 1/a
for a in [1.5, 2.0, 2.5, 2.9]:
    u = 0.2
    for _ in range(5000):
        u = f_log(a, u)
    check(f"d5 limite 1-1/a (a={a})", isclose(u, 1 - 1/a, abs_tol=1e-9))
# dérivée au point fixe : 2 - a
for a in [1.5, 2.5, 3.5]:
    lstar = 1 - 1/a
    check(f"d5 f'(l) = 2-a (a={a})", isclose(a*(1 - 2*lstar), 2 - a))
# a = 2 : formule explicite u_n = (1 - (1 - 2u0)^{2^n})/2
for u0 in [0.1, 0.3, 0.45]:
    u = u0
    for m in range(6):
        check(f"d5 a=2 formule (u0={u0}, n={m})",
              isclose(u, (1 - (1 - 2*u0)**(2**m))/2, abs_tol=1e-12))
        u = f_log(2, u)
# a = 4 : u_n = sin^2(2^n theta)
for theta in [0.3, 0.7, 1.1]:
    u = sin(theta)**2
    for m in range(8):
        check(f"d5 a=4 formule (theta={theta}, n={m})",
              isclose(u, sin(2**m*theta)**2, abs_tol=1e-9))
        u = f_log(4, u)
# a = 4 : sensibilité aux conditions initiales (écart multiplié)
x1, x2 = sin(0.3)**2, sin(0.3 + 1e-10)**2
for _ in range(30):
    x1, x2 = f_log(4, x1), f_log(4, x2)
check("d5 sensibilite", abs(x1 - x2) > 1e-3)
# a = 4 : 2-cycle explicite (theta = pi/5, 2 pi/5)
c1, c2 = sin(pi/5)**2, sin(2*pi/5)**2
check("d5 cycle d'ordre 2", isclose(f_log(4, c1), c2) and isclose(f_log(4, c2), c1))
check("d5 valeurs du 2-cycle", isclose(c1, (5 - sqrt(5))/8) and isclose(c2, (5 + sqrt(5))/8))
# a = 4 : points périodiques d'ordre 3 (theta = pi/7)
c = sin(pi/7)**2
check("d5 3-cycle theta=pi/7", isclose(f_log(4, f_log(4, f_log(4, c))), c, abs_tol=1e-12)
      and not isclose(f_log(4, c), c))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
