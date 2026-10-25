# -*- coding: utf-8 -*-
"""Vérifications du chapitre 10 — Polynômes et fractions rationnelles."""
from math import cos, sin, pi, sqrt, isclose, atan, log

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

X = sp.symbols("X")
x = sp.symbols("x", real=True)

def pz(e):
    return sp.expand(e) == 0

# --- Exercice 2 -------------------------------------------------------
q, r = sp.div(X**3 + 2*X**2 - X + 1, X**2 + 1, X)
check("ex2a quotient/reste", q == X + 2 and r == -2*X - 1)
q, r = sp.div(X**4 - 1, X - 2, X)
check("ex2b", q == X**3 + 2*X**2 + 4*X + 8 and r == 15)
check("ex2c reste = P(a)", (X**4 - 1).subs(X, 2) == 15)
# --- Exercice 3 -------------------------------------------------------
P3 = X**3 - 6*X**2 + 11*X - 6
check("ex3 racines 1,2,3", pz(P3 - (X - 1)*(X - 2)*(X - 3)))
check("ex3 Viète", 1 + 2 + 3 == 6 and 1*2*3 == 6)
# --- Exercice 4 -------------------------------------------------------
P4 = X**4 - 5*X**3 + 9*X**2 - 7*X + 2
check("ex4 factorisation", pz(P4 - (X - 1)**3*(X - 2)))
d = [P4] + [sp.diff(P4, X, k) for k in range(1, 4)]
check("ex4 multiplicité 3", [e.subs(X, 1) for e in d] == [0, 0, 0, -6])
# --- Exercice 5 -------------------------------------------------------
racines5 = [complex(r) for r in sp.Poly(X**3 - 2*X**2 + 3*X - 4, X).nroots()]
s1 = sum(racines5); s2 = sum(r**2 for r in racines5)
check("ex5 s1=2", abs(s1 - 2) < 1e-9)
check("ex5 s2=−2", abs(s2 + 2) < 1e-9)
# --- Exercice 6 -------------------------------------------------------
coeffs = [2, -3, 0, 1, -5]
h = coeffs[0]; etapes = [h]
for c in coeffs[1:]:
    h = 2*h + c
    etapes.append(h)
check("ex6 Horner P(2)=5", etapes == [2, 1, 2, 5, 5])
q, r = sp.div(2*X**4 - 3*X**3 + X - 5, X - 2, X)
check("ex6 quotient", q == 2*X**3 + X**2 + 2*X + 5 and r == 5)
# --- Exercice 7 -------------------------------------------------------
check("ex7 X⁴−1 sur R", pz(X**4 - 1 - (X - 1)*(X + 1)*(X**2 + 1)))
check("ex7 X³−1", pz(X**3 - 1 - (X - 1)*(X**2 + X + 1)))
check("ex7 X⁴+X²+1", pz(X**4 + X**2 + 1 - (X**2 + X + 1)*(X**2 - X + 1)))
# --- Exercice 8 -------------------------------------------------------
A8 = X**3 - 3*X + 2; B8 = X**2 - 1
check("ex8 A=(X−1)²(X+2)", pz(A8 - (X - 1)**2*(X + 2)))
check("ex8 pgcd", sp.gcd(A8, B8, X) == X - 1)
# --- Exercice 9 -------------------------------------------------------
check("ex9 Taylor en 1", pz(X**3 - (1 + 3*(X - 1) + 3*(X - 1)**2 + (X - 1)**3)))
# --- Exercice 10 ------------------------------------------------------
for lam, fac in [(2, (X - 1)**2*(X + 2)), (-2, (X + 1)**2*(X - 2))]:
    check(f"ex10 λ={lam}", pz(X**3 - 3*X + lam - fac))
check("ex10 seuls λ=±2", all(
    sp.discriminant(X**3 - 3*X + lam, X) != 0 for lam in [0, 1, -1, 3, -3]))
# --- Exercice 11 ------------------------------------------------------
pts = [(k, k) for k in range(4)]
P11 = sp.interpolate(pts, X)
check("ex11 interpolation de l'identité", sp.expand(P11) == X)
# --- Exercice 12 ------------------------------------------------------
P12 = sp.expand((X**2 - 2*X + 2)*(X**2 - 2))
check("ex12 produit", P12 == X**4 - 2*X**3 + 4*X - 4)
check("ex12 racines", P12.subs(X, 1 + sp.I).expand() == 0
      and P12.subs(X, sp.sqrt(2)).expand() == 0)
# --- Exercice 13 ------------------------------------------------------
c1 = (sqrt(5) - 1)/4; c2 = -(1 + sqrt(5))/4
check("ex13 cosinus", isclose(cos(2*pi/5), c1) and isclose(cos(4*pi/5), c2))
f13 = lambda t: (t - 1)*(t**2 - 2*c1*t + 1)*(t**2 - 2*c2*t + 1)
check("ex13 X⁵−1 sur R", all(isclose(f13(t), t**5 - 1, rel_tol=1e-9, abs_tol=1e-9)
      for t in [0.3, 1.7, -2.2, 0.9]))
# --- Exercice 14 ------------------------------------------------------
check("ex14 Bézout", pz(sp.Rational(1, 2)*(X**2 + 1)
      - sp.Rational(1, 2)*(X + 1)*(X - 1) - 1))
check("ex14 premiers entre eux", sp.gcd(X**2 + 1, X - 1, X) == 1)
# --- Exercice 15 ------------------------------------------------------
P15 = -sp.Rational(3, 2)*X**2 + sp.Rational(7, 2)*X + 1
check("ex15 valeurs", [P15.subs(X, k) for k in [0, 1, 2]] == [1, 3, 2])
check("ex15 Lagrange", sp.expand(sp.interpolate([(0, 1), (1, 3), (2, 2)], X) - P15) == 0)
# --- Exercice 16 ------------------------------------------------------
F16 = (X**3 + 1)/(X**2 - 1)
check("ex16 forme irréductible", sp.simplify(F16 - (X**2 - X + 1)/(X - 1)) == 0)
check("ex16 partie entière", sp.simplify((X**2 - X + 1)/(X - 1) - (X + 1/(X - 1))) == 0)
# --- Exercice 17 ------------------------------------------------------
check("ex17a", sp.simplify(1/(X**2 - 1)
      - sp.Rational(1, 2)*(1/(X - 1) - 1/(X + 1))) == 0)
check("ex17b", sp.simplify((X + 2)/(X*(X + 1)) - (2/X - 1/(X + 1))) == 0)
check("ex17c", sp.simplify(1/(X*(X**2 + 1)) - (1/X - X/(X**2 + 1))) == 0)
# --- Exercice 18 ------------------------------------------------------
P18 = (X - 1)**2*(X + 2)
check("ex18 P'/P", sp.simplify(sp.diff(P18, X)/P18 - (2/(X - 1) + 1/(X + 2))) == 0)
# --- Exercice 19 ------------------------------------------------------
T = [sp.Integer(1), X]
for n in range(8):
    T.append(sp.expand(2*X*T[-1] - T[-2]))
for n in [2, 3, 4, 5]:
    check(f"ex19 coeff dominant n={n}", sp.LC(sp.Poly(T[n], X)) == 2**(n - 1))
    rac = [cos((2*k + 1)*pi/(2*n)) for k in range(n)]
    Tn = sp.lambdify(X, T[n])
    check(f"ex19 racines n={n}", all(isclose(Tn(r), 0, abs_tol=1e-9) for r in rac))
    prod = lambda t: 2**(n - 1)*sp.prod([t - r for r in rac])
    check(f"ex19 scindé n={n}", all(isclose(Tn(t), float(prod(t)), rel_tol=1e-8, abs_tol=1e-8)
          for t in [0.2, -0.7, 1.3]))
# --- Exercice 20 ------------------------------------------------------
s3 = sum(r**3 for r in racines5)
check("ex20 s3 par récurrence", abs(s3 - 2) < 1e-9 and 2*(-2) - 3*2 + 3*4 == 2)
# --- Exercice 21 ------------------------------------------------------
P21 = X**4 - 10*X**2 + 1
check("ex21 √2+√3 racine", sp.expand(P21.subs(X, sp.sqrt(2) + sp.sqrt(3))) == 0)
check("ex21 pas de racine rationnelle", P21.subs(X, 1) != 0 and P21.subs(X, -1) != 0)
# --- Exercice 22 (erreur d'interpolation, sur un exemple) --------------
noeuds = [0, pi/4, pi/2]
Pint = sp.interpolate([(t, sin(t)) for t in noeuds], x)
Pl = sp.lambdify(x, Pint)
M3 = 1.0  # |sin'''| ≤ 1
for t in [0.2, 0.7, 1.1, 1.4]:
    borne = M3/6*abs((t - noeuds[0])*(t - noeuds[1])*(t - noeuds[2]))
    check(f"ex22 borne en {t}", abs(sin(t) - Pl(t)) <= borne + 1e-12)
# --- Exercice 23 ------------------------------------------------------
dec = sp.Rational(1, 3)/(X + 1) + (-X + 2)/(3*(X**2 - X + 1))
check("ex23 décomposition", sp.simplify(1/(X**3 + 1) - dec) == 0)
prim = lambda t: (1/3)*log(abs(t + 1)) - (1/6)*log(t*t - t + 1) \
    + (1/sqrt(3))*atan((2*t - 1)/sqrt(3))
for t in [0.5, 1.2, 2.0]:
    h = 1e-6
    deriv = (prim(t + h) - prim(t - h))/(2*h)
    check(f"ex23 primitive en {t}", isclose(deriv, 1/(t**3 + 1), rel_tol=1e-5))
# --- Exercice 24 ------------------------------------------------------
a, b, c, d = sp.symbols("a b c d")
check("ex24 identité des modules", sp.expand((a**2 + b**2)*(c**2 + d**2)
      - ((a*c - b*d)**2 + (a*d + b*c)**2)) == 0)
S = sp.expand((X**2 - sp.sqrt(2))**2 + (1 + sp.sqrt(2))**2*X**2)
check("ex24 exemple", sp.simplify(S - (X**4 + 3*X**2 + 2)) == 0)
check("ex24 X⁴+3X²+2 positif", all((t**4 + 3*t**2 + 2) > 0 for t in [-3, -1, 0, 1, 3]))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
