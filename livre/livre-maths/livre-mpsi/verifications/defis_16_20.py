# -*- coding: utf-8 -*-
"""Vérifications des défis des chapitres 16 à 20."""
import math
from fractions import Fraction as Fr
from itertools import product
from math import comb, factorial, isclose, sqrt, pi, sin, cos, tan, exp, log

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

# =====================================================================
# Défi 16 — Nombres de Stirling de seconde espèce
# =====================================================================
S = {(0, 0): 1}
for n in range(1, 14):
    for k in range(0, n + 1):
        S[(n, k)] = (S.get((n - 1, k - 1), 0) if k >= 1 else 0) + k*S.get((n - 1, k), 0)
def partitions_bf(n):
    # nombre de partitions de {0..n-1} en k blocs, par fonctions de restriction de croissance
    cnt = {}
    def rec(i, blocs, m):
        if i == n:
            cnt[m] = cnt.get(m, 0) + 1
            return
        for b in range(m + 1):
            rec(i + 1, blocs, m + 1 if b == m else m)
    rec(0, None, 0)
    return cnt
for n in range(1, 8):
    bf = partitions_bf(n)
    check(f"d16 S({n},k) par force brute", all(bf.get(k, 0) == S[(n, k)] for k in range(1, n + 1)))
check("d16 S(n,2) = 2^(n-1) - 1", all(S[(n, 2)] == 2**(n - 1) - 1 for n in range(2, 13)))
check("d16 S(n,n-1) = C(n,2)", all(S[(n, n - 1)] == comb(n, 2) for n in range(2, 13)))
check("d16 ligne 6", [S[(6, k)] for k in range(1, 7)] == [1, 31, 90, 65, 15, 1])
def surj_bf(n, k):
    return sum(1 for f in product(range(k), repeat=n) if len(set(f)) == k)
check("d16 surjections = k! S(n,k)", all(surj_bf(n, k) == factorial(k)*S[(n, k)]
      for n in range(1, 7) for k in range(1, n + 1)))
check("d16 k^n = somme C(k,j) j! S(n,j)", all(
    k**n == sum(comb(k, j)*factorial(j)*S[(n, j)] for j in range(0, n + 1))
    for n in range(1, 9) for k in range(0, 9)))
X = sp.symbols("X")
for n in range(1, 7):
    rhs = sum(S[(n, j)]*sp.prod([X - i for i in range(j)]) for j in range(0, n + 1))
    check(f"d16 X^{n} en factorielles descendantes", sp.expand(rhs - X**n) == 0)
check("d16 lien defi 12 : X^3 = H1 + 6H2 + 6H3", [factorial(j)*S[(3, j)] for j in (1, 2, 3)]
      == [1, 6, 6])
B = [sum(S[(n, k)] for k in range(0, n + 1)) for n in range(0, 9)]
check("d16 Bell", B[:7] == [1, 1, 2, 5, 15, 52, 203])
check("d16 recurrence de Bell", all(B[n + 1] == sum(comb(n, k)*B[k] for k in range(n + 1))
      for n in range(0, 8)))
check("d16 S(n,3)", all(S[(n, 3)] == (3**n - 3*2**n + 3)//6 for n in range(3, 13)))
# les 7 partitions de {1,2,3,4} en 2 blocs
check("d16 S(4,2) = 7", S[(4, 2)] == 7)

# =====================================================================
# Défi 17 — Le collectionneur de vignettes
# =====================================================================
def p_complete(n, m):
    return sum((-1)**j*comb(n, j)*Fr(n - j, n)**m for j in range(n + 1))
check("d17 P(complete) = n! S(m,n)/n^m", all(p_complete(n, m) == Fr(factorial(n)*S[(m, n)], n**m)
      for n in range(1, 6) for m in range(n, 13)))
check("d17 de : m = 12", isclose(float(p_complete(6, 12)), 0.4378, abs_tol=1e-4))
check("d17 de : m = 13 premier rang >= 1/2", float(p_complete(6, 12)) < 0.5 < float(p_complete(6, 13)))
check("d17 S(12,6) et S(13,6)", S[(12, 6)] == 1323652 and S[(13, 6)] == 9321312)
# espérance de X_m par force brute (n = 3, m = 4)
n_, m_ = 3, 4
tot = sum(len(set(t)) for t in product(range(n_), repeat=m_))
check("d17 E(X_m) force brute", Fr(tot, n_**m_) == n_*(1 - Fr(n_ - 1, n_)**m_))
# variance de Y = n - X
tot2 = sum((n_ - len(set(t)))**2 for t in product(range(n_), repeat=m_))
p = Fr(n_ - 1, n_)**m_
q = Fr(n_ - 2, n_)**m_
EY = n_*p
VY = Fr(tot2, n_**m_) - EY**2
check("d17 V(Y) formule", VY == n_*p + n_*(n_ - 1)*q - n_**2*p**2)
check("d17 q <= p^2", all(Fr(nn - 2, nn)**mm <= (Fr(nn - 1, nn)**mm)**2
      for nn in range(2, 30) for mm in range(1, 50)))
check("d17 borne n e^(-m/n)", all(nn*(1 - 1/nn)**mm <= nn*exp(-mm/nn)
      for nn in range(2, 200, 7) for mm in range(1, 2000, 13)))
check("d17 n = 100, c = 3 : m = 761", math.ceil(100*log(100) + 3*100) == 761
      and 100*exp(-761/100) <= exp(-3))
check("d17 exact n = 100, m = 761 < 5%", float(1 - p_complete(100, 761)) < 0.05)
# courbe pour la figure : n = 20
pts = [(m, float(p_complete(20, m))) for m in range(20, 141, 10)]
check("d17 transition vers n ln n = 60", pts[4][1] < 0.6 and pts[8][1] > 0.85)
check("d17 E(X_m)/n ~ 1 - e^(-m/n)", isclose(1 - (1 - 1/1000)**2000, 1 - exp(-2), abs_tol=1e-3))
check("d17 n=100 : 230 achats pour 90 vignettes en moyenne",
      100*(1 - 0.99**230) >= 90 > 100*(1 - 0.99**229))
check("d17 ln(1-x) >= -x/(1-x)", all(log(1 - t) >= -t/(1 - t) for t in [0.001, 0.1, 0.5, 0.9]))
check("d17 mediane du de ~ n ln n + 0.37 n", isclose(6*log(6) - 6*log(log(2)), 12.95, abs_tol=0.01))
check("d17 valeurs exactes du de", Fr(720*1323652, 6**12) == p_complete(6, 12)
      and isclose(float(p_complete(6, 13)), 0.5139, abs_tol=1e-4))

# =====================================================================
# Défi 18 — Séries de Fourier et inégalité de Bessel
# =====================================================================
x = sp.symbols("x", real=True)
def ps(f, g):
    return sp.integrate(f*g, (x, -sp.pi, sp.pi))/sp.pi
for k in range(0, 4):
    for l in range(0, 4):
        ck, cl = (sp.cos(k*x) if k else 1/sp.sqrt(2)), (sp.cos(l*x) if l else 1/sp.sqrt(2))
        check(f"d18 <c{k},c{l}>", sp.simplify(ps(ck, cl) - (1 if k == l else 0)) == 0)
        if k >= 1 and l >= 1:
            check(f"d18 <s{k},s{l}>", sp.simplify(ps(sp.sin(k*x), sp.sin(l*x)) - (1 if k == l else 0)) == 0)
        if l >= 1:
            check(f"d18 <c{k},s{l}>", sp.simplify(ps(ck, sp.sin(l*x))) == 0)
for k in range(1, 7):
    check(f"d18 b_{k}", sp.simplify(ps(x, sp.sin(k*x)) - 2*(-1)**(k + 1)/sp.Integer(k)) == 0)
    check(f"d18 a_{k}", ps(x, sp.cos(k*x)) == 0)
check("d18 norme de x", sp.simplify(ps(x, x) - 2*sp.pi**2/3) == 0)
check("d18 Bessel", all(sum(4/k**2 for k in range(1, n + 1)) <= 2*pi**2/3 for n in range(1, 500, 37)))
check("d18 distance", all(isclose(float(sp.integrate((x - sum(2*(-1)**(k + 1)*sp.sin(k*x)/k
      for k in range(1, n + 1)))**2, (x, -sp.pi, sp.pi))/sp.pi),
      2*pi**2/3 - 4*sum(1/k**2 for k in range(1, n + 1)), rel_tol=1e-9) for n in [1, 2, 3]))
def Sn(t, n):
    return 2*sum((-1)**(k + 1)*sin(k*t)/k for k in range(1, n + 1))
check("d18 S_n(pi/2) -> pi/2", isclose(Sn(pi/2, 20001), pi/2, abs_tol=1e-3))
gibbs = max(Sn(t, 1000) for t in [pi - i*1e-5 for i in range(1, 1000)])
check("d18 Gibbs ~ 9 %", isclose((gibbs - pi)/(2*pi), 0.0895, abs_tol=1e-3))
import mpmath
check("d18 constante de Gibbs 2 Si(pi)", isclose(float(2*mpmath.si(mpmath.pi)), 3.7038, abs_tol=1e-4))

# =====================================================================
# Défi 19 — zeta(2) = pi^2/6 par la cotangente
# =====================================================================
for m in range(1, 12):
    xs = [1/tan(r*pi/(2*m + 1))**2 for r in range(1, m + 1)]
    check(f"d19 somme des cot^2 (m={m})", isclose(sum(xs), m*(2*m - 1)/3, rel_tol=1e-9))
    P = [(-1)**k*comb(2*m + 1, 2*k + 1) for k in range(m + 1)]  # coefficients de X^(m-k)
    check(f"d19 racines de P_m (m={m})", all(abs(sum(P[k]*xr**(m - k) for k in range(m + 1)))
          < 1e-6*max(1, xr**m) for xr in xs))
th = sp.symbols("th")
for m in range(1, 5):
    lhs = sp.expand(sp.sin((2*m + 1)*th), trig=True)
    rhs = sum((-1)**k*sp.binomial(2*m + 1, 2*k + 1)*sp.cos(th)**(2*m - 2*k)*sp.sin(th)**(2*k + 1)
              for k in range(m + 1))
    check(f"d19 developpement de sin((2m+1)t) (m={m})", sp.simplify(lhs - rhs) == 0)
check("d19 encadrement", all(1/tan(t)**2 < 1/t**2 < 1 + 1/tan(t)**2
      for t in [0.01, 0.3, 1.0, 1.5]))
for m in [10, 100, 1000]:
    s = sum(1/r**2 for r in range(1, m + 1))
    lo = pi**2*m*(2*m - 1)/(3*(2*m + 1)**2)
    hi = pi**2*2*m*(m + 1)/(3*(2*m + 1)**2)
    check(f"d19 encadrement de la somme (m={m})", lo < s < hi)
check("d19 impairs pi^2/8", isclose(sum(1/(2*k + 1)**2 for k in range(200000)), pi**2/8, abs_tol=2e-6))
check("d19 alternee pi^2/12", isclose(sum((-1)**(k + 1)/k**2 for k in range(1, 200000)),
      pi**2/12, abs_tol=1e-9))
S10 = sum(1/k**2 for k in range(1, 11))
lo_pi, hi_pi = sqrt(6*(S10 + 1/11)), sqrt(6*(S10 + 1/10.5))
check("d19 encadrement de pi", isclose(S10, 1.549768, abs_tol=1e-6) and lo_pi < pi < hi_pi
      and hi_pi - lo_pi < 5e-3 and isclose(lo_pi, 3.1375, abs_tol=1e-4)
      and isclose(hi_pi, 3.1417, abs_tol=1e-4))
check("d19 zeta(2) symbolique", sp.summation(1/sp.Symbol("k", positive=True, integer=True)**2,
      (sp.Symbol("k", positive=True, integer=True), 1, sp.oo)) == sp.pi**2/6)

# =====================================================================
# Défi 20 — Le point de Fermat
# =====================================================================
A, Bp, C = (-1.0, 0.0), (1.0, 0.0), (0.0, 2.0)
def f(Mx, My):
    return sum(math.hypot(Mx - P_[0], My - P_[1]) for P_ in (A, Bp, C))
F = (0.0, 1/sqrt(3))
def unit(P_, M_):
    d = math.hypot(M_[0] - P_[0], M_[1] - P_[1])
    return ((M_[0] - P_[0])/d, (M_[1] - P_[1])/d)
us = [unit(P_, F) for P_ in (A, Bp, C)]
check("d20 somme des vecteurs unitaires nulle", abs(sum(u[0] for u in us)) < 1e-12
      and abs(sum(u[1] for u in us)) < 1e-12)
check("d20 angles de 120 degres", all(isclose(us[i][0]*us[j][0] + us[i][1]*us[j][1], -0.5)
      for i in range(3) for j in range(i + 1, 3)))
check("d20 valeur minimale 2 + sqrt 3", isclose(f(*F), 2 + sqrt(3)))
grid_min = min(f(i/200, j/200) for i in range(-200, 201) for j in range(-100, 400))
check("d20 minimum global sur une grille", grid_min >= f(*F) - 1e-9)
# gradient de la distance
check("d20 gradient de la distance", isclose(
    (math.hypot(0.5 + 1e-7 - 1, 0.3) - math.hypot(0.5 - 1e-7 - 1, 0.3))/(2e-7),
    (0.5 - 1)/math.hypot(0.5 - 1, 0.3), rel_tol=1e-6))
# angles du triangle < 120 degrés
def angle(P_, Q_, R_):
    v = (Q_[0] - P_[0], Q_[1] - P_[1]); w = (R_[0] - P_[0], R_[1] - P_[1])
    return math.acos((v[0]*w[0] + v[1]*w[1])/(math.hypot(*v)*math.hypot(*w)))
check("d20 angles < 2pi/3", all(angle(P_, Q_, R_) < 2*pi/3 for P_, Q_, R_ in
      [(A, Bp, C), (Bp, C, A), (C, A, Bp)]))
# dérivée directionnelle en A : 1 - 2 cos(A/2) < 0
angA = angle(A, Bp, C)
check("d20 derivee en A negative", 1 - 2*cos(angA/2) < 0)
# lien Napoléon : C' sommet du triangle équilatéral extérieur sur [AB], CC' = 2 + sqrt3
Cprime = (0.0, -sqrt(3))
check("d20 CC' = f(F)", isclose(math.hypot(C[0] - Cprime[0], C[1] - Cprime[1]), 2 + sqrt(3)))
check("d20 F sur (CC')", isclose(F[0], 0.0))
# minoration à l'infini
check("d20 f(M) >= 3|M| - somme", all(f(R_*cos(t), R_*sin(t)) >= 3*R_ - (1 + 1 + 2)
      for R_ in [5, 50] for t in [0, 1, 2, 4]))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
