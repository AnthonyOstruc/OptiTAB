# -*- coding: utf-8 -*-
"""Vérification des résultats des devoirs maison DM1 à DM4 (partie Évaluations)."""
import math
import random
from fractions import Fraction as Fr
from math import comb, factorial, exp, log, sqrt, pi, isclose

import mpmath as mp
import sympy as sp

OK = []


def check(name, cond):
    if not cond:
        raise AssertionError("ÉCHEC : " + name)
    OK.append(name)


x, t, a, b = sp.symbols("x t a b", real=True)
random.seed(2026)

# ============================ DM 1 ===================================
# A. Inégalité arithmético-géométrique : tests aléatoires
for _ in range(2000):
    n = random.randint(1, 9)
    xs = [random.uniform(0.01, 10) for _ in range(n)]
    A = sum(xs)/n
    G = math.prod(xs)**(1/n)
    H = n/sum(1/v for v in xs)
    if not (H <= G*(1 + 1e-12) and G <= A*(1 + 1e-12)):
        raise AssertionError("DM1 IAG")
check("DM1 H <= G <= A (2000 tirages)", True)
# Pas de Cauchy « vers le bas » : x_n = moyenne des n-1 premiers
xs = [1.0, 2.0, 7.0]
A3 = sum(xs)/3
check("DM1 ajout de la moyenne", isclose(sum(xs + [A3])/4, A3))
# Inégalité ln t <= t - 1, égalité seulement en 1
check("DM1 ln t <= t-1", all(math.log(v) <= v - 1 for v in [0.01, 0.5, 0.99, 1, 1.01, 3, 50]))
check("DM1 tangente en 1", sp.diff(sp.log(x), x).subs(x, 1) == 1)
# (1+1/n)^n croissante (IAG appliquée à n copies de 1+1/n et à 1)
check("DM1 (1+1/n)^n croissante", all((1 + Fr(1, n))**n < (1 + Fr(1, n + 1))**(n + 1) for n in range(1, 60)))
check("DM1 moyenne arithmetique", all(Fr(n*(1 + Fr(1, n)) + 1, n + 1) == 1 + Fr(1, n + 1) for n in range(1, 30)))
# minimum de x + 4/x^2
f = x + 4/x**2
check("DM1 minimum x + 4/x^2", sp.solve(sp.diff(f, x), x) == [2] and f.subs(x, 2) == 3)
check("DM1 produit des trois termes", sp.simplify((x/2)*(x/2)*(4/x**2)) == 1)
# n! <= ((n+1)/2)^n, égalité pour n = 1, 2
check("DM1 n! <= ((n+1)/2)^n", all(factorial(n) <= Fr(n + 1, 2)**n for n in range(1, 40))
      and factorial(2) == Fr(3, 2)**2 - Fr(1, 4) and factorial(1) == 1)
check("DM1 egalite seulement n=1", all(factorial(n) < Fr(n + 1, 2)**n for n in range(2, 40)))
# volume maximal : x+y+z = 3 => xyz <= 1
check("DM1 pave", all(v[0]*v[1]*(3 - v[0] - v[1]) <= 1 + 1e-12
      for v in [(random.uniform(0, 1.5), random.uniform(0, 1.5)) for _ in range(500)]))
# valeurs de (1+1/n)^n pour la figure
vals = [float((1 + Fr(1, n))**n) for n in range(1, 11)]
check("DM1 valeurs figure", isclose(vals[0], 2) and isclose(vals[1], 2.25) and isclose(vals[9], 2.5937424601))

# ============================ DM 2 ===================================
primes = [p for p in range(3, 200) if sp.isprime(p)]
for p in primes:
    QR = sorted({(k*k) % p for k in range(1, p)})
    check(f"DM2 nombre de residus p={p}", len(QR) == (p - 1)//2)
    # x^2 = y^2 <=> x = +-y
    assert all(((u*u - v*v) % p == 0) == (u == v or u + v == p)
               for u in range(1, p) for v in range(1, p))
    # inverse : seuls 1 et p-1 sont leur propre inverse
    check(f"DM2 auto-inverses p={p}", [u for u in range(1, p) if (u*u) % p == 1] == [1, p - 1])
    check(f"DM2 Wilson p={p}", factorial(p - 1) % p == p - 1)
    for aa in range(1, p):
        crit = pow(aa, (p - 1)//2, p)
        check(f"DM2 Euler p={p} a={aa}", (crit == 1) == (aa in QR) and crit in (1, p - 1))
        if aa not in QR:
            # appariement x <-> x' avec x x' = a : aucun point fixe
            assert all((u*u - aa) % p != 0 for u in range(1, p))
    check(f"DM2 -1 carre p={p}", ((p - 1) in QR) == (p % 4 == 1))
    if p % 4 == 1:
        h = factorial((p - 1)//2) % p
        check(f"DM2 ((p-1)/2)!^2 = -1 p={p}", (h*h) % p == p - 1)
check("DM2 residus mod 13", sorted({(k*k) % 13 for k in range(1, 13)}) == [1, 3, 4, 9, 10, 12])
check("DM2 carres de 1..6 mod 13", [(k*k) % 13 for k in range(1, 7)] == [1, 4, 9, 3, 12, 10])
check("DM2 3^6 et 2^6 mod 13", pow(3, 6, 13) == 1 and pow(2, 6, 13) == 12)
check("DM2 4^2 = 3 mod 13", 16 % 13 == 3)
check("DM2 6! mod 13", factorial(6) % 13 == 5 and 25 % 13 == 12)
# Infinité de premiers 1 mod 4 : les diviseurs premiers de (2m)^2+1 sont 1 mod 4
for m in [1, 3, 15, 105, 1155, 7*11*13]:
    N = (2*m)**2 + 1
    check(f"DM2 diviseurs de (2m)^2+1, m={m}", all(q % 4 == 1 for q in sp.factorint(N)))
check("DM2 exemple (2*5*13)^2+1", sp.factorint((2*5*13)**2 + 1) == {16901: 1}
      and sp.isprime(16901) and 16901 % 4 == 1)

# ============================ DM 3 ===================================
# Formule d'erreur des trapèzes : int f - T = -1/2 int (t-a)(b-t) f''(t) dt
for _ in range(20):
    cs = [sp.Rational(random.randint(-5, 5), random.randint(1, 4)) for _ in range(5)]
    P = sum(c*t**k for k, c in enumerate(cs))
    aa, bb = sp.Rational(random.randint(-3, 0)), sp.Rational(random.randint(1, 4))
    lhs = sp.integrate(P, (t, aa, bb)) - (bb - aa)*(P.subs(t, aa) + P.subs(t, bb))/2
    rhs = -sp.Rational(1, 2)*sp.integrate((t - aa)*(bb - t)*sp.diff(P, t, 2), (t, aa, bb))
    assert sp.simplify(lhs - rhs) == 0
check("DM3 formule d'erreur (20 polynomes)", True)
check("DM3 exemple t^2", sp.integrate(t**2, (t, 0, 1)) - sp.Rational(1, 2) == -sp.Rational(1, 6)
      and -sp.Rational(1, 2)*sp.integrate(t*(1 - t)*2, (t, 0, 1)) == -sp.Rational(1, 6))
check("DM3 int (t-a)(b-t) = (b-a)^3/6", sp.simplify(sp.integrate((t - a)*(b - t), (t, a, b)) - (b - a)**3/6) == 0)
g = 1/(1 + t**2)
g2 = sp.simplify(sp.diff(g, t, 2))
check("DM3 derivee seconde", sp.simplify(g2 - (6*t**2 - 2)/(1 + t**2)**3) == 0)
check("DM3 sup |f''| = 2", max(abs(float(g2.subs(t, s/1000))) for s in range(0, 1001)) <= 2 + 1e-12
      and g2.subs(t, 0) == -2)


def trap(fun, aa, bb, n):
    h = (bb - aa)/n
    return h*(fun(aa)/2 + sum(fun(aa + k*h) for k in range(1, n)) + fun(bb)/2)


T10 = trap(lambda s: 1/(1 + s*s), 0, 1, 10)
check("DM3 trapezes n=10", abs(T10 - pi/4) <= 1/600 and isclose(T10, 0.7849814972, abs_tol=1e-9))
check("DM3 erreur effective n=10", isclose(pi/4 - T10, 4.1666e-4, rel_tol=1e-3))
check("DM3 n minimal 1e-6", math.ceil(sqrt(1e6/6)) == 409 and 1/(6*408**2) > 1e-6 >= 1/(6*409**2))
# e_k = int_k^{k+1} ln - (ln k + ln(k+1))/2
def e_k(k):
    return (k + 1)*log(k + 1) - k*log(k) - 1 - (log(k) + log(k + 1))/2
check("DM3 0 <= e_k <= 1/(12k^2)", all(0 <= e_k(k) <= 1/(12*k*k) for k in range(1, 2000)))
check("DM3 e_k ~ 1/(12k^2)", isclose(e_k(1000)*12e6, 1, rel_tol=1e-3))
check("DM3 int_1^n ln", sp.simplify(sp.integrate(sp.log(t), (t, 1, x)) - (x*sp.log(x) - x + 1)) == 0)
for n in [5, 50]:
    lhs = math.lgamma(n + 1)
    rhs = n*log(n) - n + 0.5*log(n) + 1 - sum(e_k(k) for k in range(1, n))
    check(f"DM3 identite ln n! (n={n})", isclose(lhs, rhs, abs_tol=1e-10))
S_e = float(mp.nsum(lambda k: (k + 1)*mp.log(k + 1) - k*mp.log(k) - 1 - (mp.log(k) + mp.log(k + 1))/2, [1, mp.inf]))
C = 1 - S_e
check("DM3 constante C = ln sqrt(2 pi)", isclose(C, 0.5*log(2*pi), abs_tol=1e-9))
check("DM3 valeurs C et somme", isclose(C, 0.9189385, abs_tol=1e-6) and isclose(S_e, 0.0810615, abs_tol=1e-6))
check("DM3 reste <= 1/(12(n-1))", all(sum(e_k(k) for k in range(n, 20000)) <= 1/(12*(n - 1)) for n in [2, 5, 10, 50]))
# Wallis
W = [sp.pi/2, sp.Integer(1)]
for n in range(2, 14):
    W.append(sp.Rational(n - 1, n)*W[n - 2])
check("DM3 Wallis integrales", all(sp.simplify(sp.integrate(sp.sin(t)**n, (t, 0, sp.pi/2)) - W[n]) == 0 for n in range(0, 8)))
check("DM3 W_2p", all(sp.simplify(W[2*q] - sp.factorial(2*q)/(4**q*sp.factorial(q)**2)*sp.pi/2) == 0 for q in range(0, 7)))
check("DM3 (n+1) W_{n+1} W_n = pi/2", all(sp.simplify((n + 1)*W[n + 1]*W[n] - sp.pi/2) == 0 for n in range(0, 12)))
Wn = lambda n: float(mp.quad(lambda s: mp.sin(s)**n, [0, mp.pi/2]))
check("DM3 W_n ~ sqrt(pi/(2n))", isclose(Wn(4000)/sqrt(pi/8000), 1, rel_tol=1e-3))
check("DM3 K = sqrt(2 pi)", isclose(math.lgamma(10001) - (10000*log(10000) - 10000 + 0.5*log(10000)), log(sqrt(2*pi)), abs_tol=1e-5))
# Valeurs de la figure : ln n! - (n ln n - n + 1/2 ln n)
d = [math.lgamma(n + 1) - (n*log(n) - n + 0.5*log(n)) for n in range(1, 9)]
check("DM3 figure d_1 = 1", isclose(d[0], 1) and all(d[i] > d[i + 1] for i in range(7)) and d[7] > C)

# ============================ DM 4 ===================================
# cosh t <= exp(t^2/2) : g(t) = t^2/2 - ln cosh t croissante sur R+
check("DM4 g'(t) = t - tanh t", sp.simplify(sp.diff(t**2/2 - sp.log(sp.cosh(t)), t) - (t - sp.tanh(t))) == 0)
check("DM4 tanh t <= t", all(math.tanh(s) <= s for s in [0, 0.1, 1, 3, 10]))
check("DM4 cosh <= exp(t^2/2)", all(math.cosh(s) <= exp(s*s/2) for s in [0.01*k for k in range(0, 1000)]))
# E(e^{tS_n}) = cosh(t)^n : vérification exacte pour n = 4
n4 = 4
E = sum(comb(n4, k)*sp.Rational(1, 2**n4)*sp.exp(t*(2*k - n4)) for k in range(n4 + 1))
check("DM4 fonction generatrice", sp.simplify((E - sp.cosh(t)**n4).rewrite(sp.exp)) == 0)
# optimisation : -ta + n t^2/2 minimal en t = a/n, valeur -a^2/(2n)
nn = sp.symbols("n", positive=True)
expo = -t*a + nn*t**2/2
check("DM4 t optimal", sp.solve(sp.diff(expo, t), t) == [a/nn]
      and sp.simplify(expo.subs(t, a/nn) + a**2/(2*nn)) == 0)
# sondage : epsilon = 0.05, risque 5 %
eps, risk = 0.05, 0.05
n_tch = math.ceil(1/(4*eps**2*risk))
n_hoef2 = math.ceil(log(2/risk)/(2*eps**2))
n_hoef1 = math.ceil(log(1/risk)/(2*eps**2))
check("DM4 seuils", (n_tch, n_hoef2, n_hoef1) == (2000, 738, 600))
check("DM4 seuils exacts", 2*exp(-2*737*eps**2) > risk >= 2*exp(-2*738*eps**2)
      and 1/(4*1999*eps**2) > risk >= 1/(4*2000*eps**2))
# F_n - 1/2 >= eps  <=>  S_n >= 2 n eps
check("DM4 lien F_n / S_n", all(isclose((n + 2*n*eps)/(2*n) - 0.5, eps) for n in [10, 100]))
# probabilités exactes P(|F_n - 1/2| >= 0.05) pour la figure


def p_exact(n):
    tot = Fr(0)
    for k in range(n + 1):
        if abs(Fr(k, n) - Fr(1, 2)) >= Fr(1, 20):
            tot += comb(n, k)
    return float(tot/2**n)


pe = {n: p_exact(n) for n in [100, 200, 300, 400, 500, 600, 738, 1000]}
check("DM4 probabilites exactes", isclose(pe[100], 0.3682, abs_tol=5e-4) and isclose(pe[400], 0.0510, abs_tol=5e-4))
check("DM4 exacte < Hoeffding < Tchebychev a n=738", pe[738] < 2*exp(-2*738*eps**2) < 1/(4*738*eps**2))
check("DM4 valeur exacte n=738", isclose(pe[738], 0.0072, abs_tol=3e-4))
print("probas exactes :", {k: round(v, 5) for k, v in pe.items()})
# Bienaymé-Tchebychev : V(S_n) = n
check("DM4 variance", sum(comb(n4, k)*Fr(1, 2**n4)*(2*k - n4)**2 for k in range(n4 + 1)) == n4)

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
