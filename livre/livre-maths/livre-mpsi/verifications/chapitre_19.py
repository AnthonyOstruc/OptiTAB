# -*- coding: utf-8 -*-
"""Vérifications du chapitre 19 — Procédés sommatoires discrets."""
import math
from fractions import Fraction as Fr
from math import isclose, log, sqrt, exp, factorial, pi, cos, sin

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

n = sp.symbols("n", positive=True, integer=True)
x = sp.symbols("x")

# --- Exercice 1 : convergence/divergence -------------------------------
check("ex1 geometrique 1/2", sp.Sum((sp.Rational(1, 2))**n, (n, 0, sp.oo)).doit() == 2)
check("ex1 divergence grossiere", sp.limit(n/(n + 1), n, sp.oo) == 1)
check("ex1 telescopique", sp.Sum(1/(n*(n + 1)), (n, 1, sp.oo)).doit() == 1)
# --- Exercice 2 : geometriques -----------------------------------------
check("ex2 1/3^n", sp.Sum((sp.Rational(1, 3))**n, (n, 0, sp.oo)).doit() == sp.Rational(3, 2))
check("ex2 (-1/2)^n", sp.Sum((-sp.Rational(1, 2))**n, (n, 0, sp.oo)).doit() == sp.Rational(2, 3))
check("ex2 e", isclose(sum(1/factorial(k) for k in range(25)), math.e))
# --- Exercice 3 : telescopages -----------------------------------------
check("ex3 1/n(n+1)(n+2)", sp.Sum(1/(n*(n + 1)*(n + 2)), (n, 1, sp.oo)).doit()
      == sp.Rational(1, 4))
check("ex3 ln(1+1/n) diverge", sum(log(1 + 1/k) for k in range(1, 1001))
      > log(1000))
check("ex3 somme partielle = ln(n+1)",
      isclose(sum(log(1 + 1/k) for k in range(1, 1000)), log(1000)))
# --- Exercice 4 : comparaison ------------------------------------------
check("ex4 1/n^2 converge", float(sp.Sum(1/n**2, (n, 1, sp.oo)).doit()) < 2)
check("ex4 majoration telescopique", all(
    Fr(1, k*k) <= Fr(1, k*(k - 1)) for k in range(2, 50)))
check("ex4 1/sqrt(n) diverge", sum(1/sqrt(k) for k in range(1, 10001)) > 150)
# --- Exercice 5 : equivalents ------------------------------------------
check("ex5 sin(1/n^2)", isclose(float(sp.limit(sp.sin(1/n**2)*n**2, n, sp.oo)), 1))
check("ex5 1-cos(1/n)", sp.limit((1 - sp.cos(1/n))*2*n**2, n, sp.oo) == 1)
check("ex5 racine", sp.limit((sp.sqrt(n + 1) - sp.sqrt(n))/n*2*n**sp.Rational(3, 2),
      n, sp.oo) == 1)
# --- Exercice 6 : Riemann ----------------------------------------------
check("ex6 alpha=2 converge", sum(1/k**2 for k in range(1, 100000)) < 1.6450)
check("ex6 alpha=1/2 diverge", sum(1/sqrt(k) for k in range(1, 100000)) > 600)
check("ex6 alpha=3/2 converge", sum(1/k**1.5 for k in range(1, 100000)) < 2.613)
# --- Exercice 7 : serie-integrale --------------------------------------
S7 = sum(1/sqrt(k) for k in range(1, 10001))
check("ex7 somme 1/sqrt(k) ~ 2 sqrt(n)", isclose(S7, 2*sqrt(10000), rel_tol=1e-2))
check("ex7 encadrement", 2*(sqrt(10001) - 1) <= S7 <= 2*sqrt(10000) - 1 + 1)
H = sum(1/k for k in range(1, 10001))
check("ex7 H_n ~ ln n", isclose(H, log(10000) + 0.5772, abs_tol=1e-3))
# --- Exercice 8 : series alternees -------------------------------------
S8 = sum((-1)**(k - 1)/k for k in range(1, 10000))
check("ex8 harmonique alternee", isclose(S8, log(2), abs_tol=1e-4))
for N in [10, 100]:
    R = log(2) - sum((-1)**(k - 1)/k for k in range(1, N + 1))
    check(f"ex8 majoration du reste N={N}", abs(R) <= 1/(N + 1))
# --- Exercice 9 : lien suite-serie -------------------------------------
P9 = 1.0
for k in range(1, 100000):
    P9 *= 1 + 1/k**2
check("ex9 produit converge", 3.6 < P9 < 3.8)  # valeur sinh(pi)/pi ~ 3.676
check("ex9 valeur sh(pi)/pi", isclose(P9, math.sinh(pi)/pi, rel_tol=1e-4))
# --- Exercice 10 : restes ----------------------------------------------
for N in [10, 100]:
    R10 = float(sp.Sum(1/n**2, (n, N + 1, sp.oo)).doit())
    check(f"ex10 encadrement reste N={N}", 1/(N + 1) <= R10 <= 1/N)
check("ex10 reste geometrique", sp.Sum((sp.Rational(1, 2))**n, (n, 11, sp.oo)).doit()
      == sp.Rational(1, 2)**10)
# --- Exercice 11 : convergence absolue ---------------------------------
check("ex11 somme sin(n)/n^2 bornee",
      abs(sum(sin(k)/k**2 for k in range(1, 100000))) < 1.645)
check("ex11 harmonique alternee non ACV", H > 9)  # somme des |termes| = H_n
# --- Exercice 12 : produit de Cauchy -----------------------------------
a12, b12 = 0.7, -1.3
ca = [a12**k/factorial(k) for k in range(60)]
cb = [b12**k/factorial(k) for k in range(60)]
cc = [sum(ca[j]*cb[k - j] for j in range(k + 1)) for k in range(60)]
check("ex12 exp(a)exp(b) = exp(a+b)", isclose(sum(cc), exp(a12 + b12), rel_tol=1e-12))
check("ex12 binome dans le produit", all(
    isclose(cc[k], (a12 + b12)**k/factorial(k), rel_tol=1e-9, abs_tol=1e-15)
    for k in range(20)))
check("ex12 carre de la geometrique", sp.Sum((n + 1)*x**n, (n, 0, sp.oo))
      .doit().subs(x, sp.Rational(1, 2)) == 4)
# --- Exercice 13 : exponentielle complexe ------------------------------
z13 = complex(0, 1.1)
S13 = sum(z13**k/factorial(k) for k in range(40))
check("ex13 e^{i theta}", isclose(S13.real, cos(1.1)) and isclose(S13.imag, sin(1.1)))
check("ex13 |e^z| <= e^{|z|}", abs(S13) <= exp(abs(z13)))
# --- Exercice 14 : sommes avec n x^n -----------------------------------
check("ex14 somme n/2^n", sp.Sum(n*(sp.Rational(1, 2))**n, (n, 1, sp.oo)).doit() == 2)
check("ex14 somme n^2/2^n", sp.Sum(n**2*(sp.Rational(1, 2))**n, (n, 1, sp.oo)).doit() == 6)
check("ex14 formule x/(1-x)^2", sp.simplify(
    sp.Sum(n*x**n, (n, 1, sp.oo)).doit() - x/(1 - x)**2).subs(x, sp.Rational(1, 3)) == 0)
# --- Exercice 15 : rearrangement ---------------------------------------
# 1 + 1/3 - 1/2 + 1/5 + 1/7 - 1/4 + ... (deux positifs, un negatif)
S15, pos, neg = 0.0, 1, 2
for _ in range(60000):
    S15 += 1/pos; pos += 2
    S15 += 1/pos; pos += 2
    S15 -= 1/neg; neg += 2
check("ex15 rearrangement -> (3/2) ln 2", isclose(S15, 1.5*log(2), abs_tol=1e-4))
check("ex15 difference avec ln 2", abs(1.5*log(2) - log(2)) > 0.3)
# --- Exercice 16 : familles positives, Fubini --------------------------
S16 = sum(Fr(1, 2**i)*Fr(1, 2**j) for i in range(40) for j in range(40))
check("ex16 produit 2x2", isclose(float(S16), 4, rel_tol=1e-9))
S16b = sum(Fr(n_ + 1, 2**n_) for n_ in range(60))  # paquets i+j = n
check("ex16 par paquets diagonaux", isclose(float(S16b), 4, rel_tol=1e-9))
# --- Exercice 17 : sommation par paquets -------------------------------
check("ex17 1/(n^2-1)", sp.Sum(1/(n**2 - 1), (n, 2, sp.oo)).doit() == sp.Rational(3, 4))
# --- Exercice 18 : Fubini en action ------------------------------------
x18 = sp.Rational(1, 3)
lhs18 = sum(x18**i/(1 - x18) for i in range(80))   # somme sur i de sum_{j>=i} x^j
rhs18 = sum((j + 1)*x18**j for j in range(80))      # somme sur j de (j+1) x^j
check("ex18 deux ordres de sommation", isclose(float(lhs18), float(rhs18), rel_tol=1e-12))
check("ex18 valeur x/(1-x)^2 + 1/(1-x)",
      isclose(float(rhs18), float(1/(1 - x18)**2), rel_tol=1e-9))
# --- Exercice 19 : encadrements de zeta --------------------------------
z2 = float(sp.Sum(1/n**2, (n, 1, sp.oo)).doit())
z3 = float(sp.Sum(1/n**3, (n, 1, sp.oo)).doit())
check("ex19 zeta(2) dans [3/2, 2]", 1.5 <= z2 <= 2)
check("ex19 zeta(3) dans [9/8, 3/2]", 1.125 <= z3 <= 1.5)
check("ex19 Bale", isclose(z2, pi**2/6, rel_tol=1e-12))
# --- Exercice 20 : developpement du reste ------------------------------
for N in [50, 500]:
    R20 = float(sp.Sum(1/n**2, (n, N + 1, sp.oo)).doit())
    check(f"ex20 encadrement fin N={N}", 1/(N + 1) < R20 < 1/(N + sp.Rational(1, 2)))
    check(f"ex20 equivalent N={N}", isclose(N*R20, 1, rel_tol=2/N))
# --- Exercice 21 : gamma par les series --------------------------------
S21 = sum(1/k - log(1 + 1/k) for k in range(1, 200000))
check("ex21 gamma", isclose(S21, 0.5772156649, abs_tol=1e-5))
check("ex21 equivalent du terme", isclose(
    (1/1000 - log(1 + 1/1000))*2*1000**2, 1, rel_tol=1e-3))
# --- Exercice 22 : produit eulerien 2-3 lisse --------------------------
S22 = sum(Fr(1, 2**a*3**b) for a in range(60) for b in range(40))
check("ex22 somme = 3", isclose(float(S22), 3, rel_tol=1e-10))
check("ex22 produit des geometriques", Fr(1, 1 - Fr(1, 2))*Fr(1, 1 - Fr(1, 3)) == 3)
# --- Exercice 23 : condensation de Cauchy ------------------------------
# Riemann alpha via condensation : somme 2^k (2^-k)^alpha = somme (2^{1-alpha})^k
for alpha, cv in [(2, True), (1, False), (0.5, False), (1.5, True)]:
    r = 2**(1 - alpha)
    check(f"ex23 condensation alpha={alpha}", (r < 1) == cv)
check("ex23 1/(n ln n) diverge", sum(1/(k*log(k)) for k in range(2, 200000)) > 2.5)
# condensée de 1/(n ln n) : 2^k/(2^k · k ln 2) = 1/(k ln 2), harmonique divergente
check("ex23 condensee = harmonique/ln 2",
      sum(1/(k*log(2)) for k in range(1, 101)) > 7)
# --- Exercice 24 : Fubini s'effondre -----------------------------------
N24 = 60
A = [[0]*N24 for _ in range(N24)]
for i in range(N24):
    A[i][i] = 1
    if i + 1 < N24:
        A[i + 1][i] = -1
lignes = sum(sum(row) for row in A)
colonnes = sum(sum(A[i][j] for i in range(N24)) for j in range(N24))
check("ex24 sommes par lignes = 1", lignes == 1)
check("ex24 sommes par colonnes = 1 aussi en tronque",
      colonnes == 1)
# version infinie : lignes donnent 1 (seule la premiere ligne contribue 1,
# chaque autre 0) ; colonnes donnent 0 (chaque colonne somme a 0)
sommes_lignes = [sum(A[i]) for i in range(N24)]
sommes_colonnes = [sum(A[i][j] for i in range(N24)) for j in range(N24)]
check("ex24 chaque ligne (sauf la 1re) somme a 0",
      sommes_lignes[0] == 1 and all(s == 0 for s in sommes_lignes[1:]))
check("ex24 chaque colonne sauf la derniere somme a 0",
      all(s == 0 for s in sommes_colonnes[:-1]) and sommes_colonnes[-1] == 1)

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
