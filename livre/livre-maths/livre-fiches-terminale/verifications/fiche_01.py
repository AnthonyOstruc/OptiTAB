# -*- coding: utf-8 -*-
"""Vérification des formules et des valeurs de la fiche 01 — Suites numériques."""
import math
from fractions import Fraction as Fr

import sympy as sp

OK = []


def check(name, cond):
    if not cond:
        raise AssertionError("ÉCHEC : " + name)
    OK.append(name)


n, q, u0, r, a, b, x, k = sp.symbols("n q u0 r a b x k")
i = sp.symbols("i", integer=True)

# 1. Suites arithmétiques et géométriques
for N in range(0, 12):
    check(f"somme arithmetique N={N}", sum(Fr(3) + 2*j for j in range(N + 1)) == (N + 1)*(Fr(3) + Fr(3) + 2*N)/2)
    check(f"somme geometrique N={N}", sum(Fr(5)*Fr(2, 3)**j for j in range(N + 1))
          == Fr(5)*(1 - Fr(2, 3)**(N + 1))/(1 - Fr(2, 3)))
check("1+2+...+n", sp.simplify(sp.summation(i, (i, 1, n)) - n*(n + 1)/2) == 0)
check("1+q+...+q^n", all(sum(Fr(qq)**j for j in range(N + 1)) == (1 - Fr(qq)**(N + 1))/(1 - Fr(qq))
      for qq in [2, Fr(1, 3), -5, Fr(-7, 2)] for N in range(0, 15)))
check("terme general u_p", sp.simplify((u0 + n*r) - ((u0 + 7*r) + (n - 7)*r)) == 0)
# arithmético-géométrique
ell = b/(1 - a)
check("point fixe", sp.simplify(a*ell + b - ell) == 0)
for A_, B_, U0 in [(Fr(1, 2), Fr(1), Fr(0)), (Fr(3), Fr(-2), Fr(5)), (Fr(-1, 3), Fr(4), Fr(2))]:
    L_ = B_/(1 - A_)
    u = U0
    for m in range(10):
        assert u == L_ + (U0 - L_)*A_**m
        u = A_*u + B_
check("u_n = l + (u0 - l) a^n", True)

# 2. Récurrence : 4^(k+1) + 1 = 4(4^k + 1) - 3, jamais divisible par 3
check("heredite 4^n+1", sp.expand(4*(4**k + 1) - 3 - (4**(k + 1) + 1)) == 0)
check("4^n+1 jamais multiple de 3", all((4**m + 1) % 3 == 2 for m in range(0, 60)))

# 3. Limites
check("FI quotient -3/2", sp.limit((3*x**2 - x)/(1 - 2*x**2), x, sp.oo) == sp.Rational(-3, 2))
check("factorisation quotient", sp.simplify((3*x**2 - x)/(1 - 2*x**2) - (3 - 1/x)/(1/x**2 - 2)) == 0)
check("conjuguee", sp.simplify(sp.sqrt(x + 1) - sp.sqrt(x) - 1/(sp.sqrt(x + 1) + sp.sqrt(x))) == 0
      and sp.limit(sp.sqrt(x + 1) - sp.sqrt(x), x, sp.oo) == 0)
check("3^n - 2^n", sp.limit(3**x - 2**x, x, sp.oo) == sp.oo
      and sp.simplify(3**x*(1 - sp.Rational(2, 3)**x) - (3**x - 2**x)) == 0)
check("0,9^n -> 0 et 1,1^n -> +oo", 0.9**2000 < 1e-90 and 1.1**2000 > 1e80)
check("1 - 1/(n+1) majoree par 5, limite 1", all(1 - 1/(m + 1) <= 5 for m in range(100))
      and sp.limit(1 - 1/(x + 1), x, sp.oo) == 1)
check("sin(n)/n -> 0", sp.limit(sp.sin(x)/x, x, sp.oo) == 0)
# Bernoulli
check("Bernoulli", all((1 + aa)**m >= 1 + m*aa for aa in [0.01, 0.5, 2, 10] for m in range(0, 60)))
check("heredite Bernoulli", sp.expand((1 + k*a)*(1 + a) - (1 + (k + 1)*a + k*a**2)) == 0)

# 5. u_{n+1} = sqrt(u_n + 6), u0 = 0
u = 0.0
vals = [u]
for m in range(30):
    u = math.sqrt(u + 6)
    vals.append(u)
check("encadrement 0 <= u_n <= u_{n+1} <= 3", all(0 <= vals[m] <= vals[m + 1] <= 3 for m in range(30)))
check("valeurs du schema", [round(v, 4) for v in vals[:5]] == [0.0, 2.4495, 2.9068, 2.9844, 2.9974])
check("point fixe 3", sp.solve(sp.Eq(x**2 - x - 6, 0), x) == [-2, 3] and abs(vals[-1] - 3) < 1e-12)

# 6. Algorithmes
def seuil(s):
    m, v = 0, 0
    while v <= s:
        v = 0.5*v + 1
        m = m + 1
    return m


check("seuil(1.99) = 8", seuil(1.99) == 8)
check("u_n = 2 - 2*0,5^n", all(abs((2 - 2*0.5**m) - w) < 1e-12 for m, w in
      enumerate([0, 1, 1.5, 1.75, 1.875, 1.9375, 1.96875, 1.984375, 1.9921875])))
check("u7, u8", round(2 - 2*0.5**7, 3) == 1.984 and round(2 - 2*0.5**8, 3) == 1.992)


def somme(m):
    v, S = 1, 1
    for _ in range(m):
        v = 3*v
        S = S + v
    return S


check("somme(4) = 121", somme(4) == 121 == (3**5 - 1)//2)
h = [Fr(1)]
for _ in range(3):
    h.append((h[-1] + 2/h[-1])/2)
check("Heron sqrt(2)", float(h[1]) == 1.5 and round(float(h[2]), 4) == 1.4167 and round(float(h[3]), 5) == 1.41422)

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
