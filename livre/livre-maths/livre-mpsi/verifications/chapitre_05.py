# -*- coding: utf-8 -*-
"""Vérifications du chapitre 5 — Nombres réels et suites numériques."""
import math
from fractions import Fraction
from math import isclose, sqrt, log, sin, cos, pi, factorial, floor

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

phi = (1 + sqrt(5))/2
psi = (1 - sqrt(5))/2

# --- Exercice 1 -------------------------------------------------------
check("ex1 somme d'irrationnels rationnelle", sqrt(2) + (-sqrt(2)) == 0)
check("ex1 produit d'irrationnels rationnel", isclose(sqrt(2)*sqrt(8), 4))
# (√2+√3)² = 5+2√6
check("ex1 (√2+√3)²", isclose((sqrt(2) + sqrt(3))**2, 5 + 2*sqrt(6)))
check("ex1 approx décimales de √2", 1.414 <= sqrt(2) < 1.415)
# --- Exercice 2 -------------------------------------------------------
B = [1/n for n in range(1, 100000)]
check("ex2 B max", max(B) == 1 and min(B) > 0 and min(B) < 1e-4)
C = [(-1)**n + 1/n for n in range(1, 100000)]
check("ex2 C sup=3/2", max(C) == 1.5)
check("ex2 C inf=−1", min(C) > -1 and min(C) < -1 + 1e-4)
# --- Exercice 3 -------------------------------------------------------
u = [2 - 1/(n + 1) for n in range(2000)]
check("ex3 u bornée croissante", all(1 <= x < 2 for x in u)
      and all(u[i] < u[i + 1] for i in range(1999)))
check("ex3 sin n + 1/n bornée", all(-1 <= sin(n) + 1/n <= 2 for n in range(1, 5000)))
# --- Exercice 4 -------------------------------------------------------
check("ex4 2^n/n! décroît (n≥1)", all((2**(n + 1)/factorial(n + 1)) <= 2**n/factorial(n)
      for n in range(1, 60)))
check("ex4 n+(−1)^n non monotone", (1 + (-1)) < (0 + 1) and (2 + 1) > (1 - 1))
# --- Exercice 5 -------------------------------------------------------
check("ex5a", isclose((3*10**8 + 1)/(10**16 + 2)*10**8, 3, rel_tol=1e-6))
check("ex5c conjuguée", all(isclose(sqrt(n + 1) - sqrt(n), 1/(sqrt(n + 1) + sqrt(n)))
      for n in range(1, 2000)))
# --- Exercice 6 -------------------------------------------------------
for n in [10, 100, 1000, 10**6]:
    check("ex6a", abs((n + cos(n))/n - 1) <= 1/n)
    s = sum(n/(n**2 + k) for k in range(1, n + 1)) if n <= 1000 else None
    if s is not None:
        check("ex6c bornes", n**2/(n**2 + n) <= s <= n**2/(n**2 + 1))
# --- Exercice 7 -------------------------------------------------------
v = 0.0
for n in range(60):
    attendu = 6*(1 - 0.5**n)
    check(f"ex7 u_{n}", isclose(v, attendu))
    v = v/2 + 3
# --- Exercice 9 (sup A+B = sup A + sup B sur des exemples finis) -------
import random
random.seed(5)
for _ in range(300):
    A = [random.uniform(-5, 5) for _ in range(8)]
    Bb = [random.uniform(-5, 5) for _ in range(8)]
    check("ex9 sup(A+B)", isclose(max(a + b for a in A for b in Bb), max(A) + max(Bb)))
    check("ex9 sup(A∪B)", max(A + Bb) == max(max(A), max(Bb)))
# --- Exercice 10 ------------------------------------------------------
x = math.pi
for n in range(1, 12):
    d = floor(10**n*x)/10**n
    check("ex10 décimaux", d <= x < d + 10**(-n))
# --- Exercice 12 ------------------------------------------------------
s = 0
for n in range(1, 200):
    s += 1/n**2
    check("ex12 majorée par 2−1/n", s <= 2 - 1/n + 1e-12)
s = 0
for n in range(0, 30):
    s += 1/factorial(n)
    check("ex12 série 1/k! majorée par 3", s < 3)
# --- Exercice 13 ------------------------------------------------------
a_ = [sum(Fraction(1, factorial(k)) for k in range(n + 1)) for n in range(1, 25)]
b_ = [a_[i] + Fraction(1, (i + 1)*factorial(i + 1)) for i in range(len(a_))]
check("ex13 a croissante", all(a_[i] < a_[i + 1] for i in range(len(a_) - 1)))
check("ex13 b décroissante", all(b_[i] > b_[i + 1] for i in range(len(b_) - 1)))
check("ex13 a<e<b (approx flottante)",
      all(float(a_[i]) <= math.e <= float(b_[i]) for i in range(len(a_))))
check("ex13 b−a→0", float(b_[-1] - a_[-1]) < 1e-24)
# --- Exercice 14 ------------------------------------------------------
check("ex14 cos(nπ/3) sous-suites", cos(0) == 1 and isclose(cos(3*pi/3), -1))
# --- Exercice 15 ------------------------------------------------------
seq = [2, 3]
for n in range(40):
    seq.append(3*seq[-1] - 2*seq[-2])
check("ex15a u_n=1+2^n", all(seq[n] == 1 + 2**n for n in range(len(seq))))
F = [0, 1]
for n in range(60):
    F.append(F[-1] + F[-2])
check("ex15b Binet", all(isclose(F[n], (phi**n - psi**n)/sqrt(5)) for n in range(40)))
w = [0, 1]
for n in range(40):
    w.append(w[-1] - w[-2])
check("ex15c périodique 6", all(w[n + 6] == w[n] for n in range(30)))
check("ex15c formule", all(isclose(w[n], (2/sqrt(3))*sin(n*pi/3), abs_tol=1e-12)
                           for n in range(30)))
# --- Exercice 16 ------------------------------------------------------
t = 0.0
prev = -1.0
for n in range(80):
    check("ex16 dans [0,2]", 0 <= t <= 2)
    # stricte croissance testée tant que la précision flottante le permet
    check("ex16 croissante", t > prev if n < 25 else t >= prev)
    prev = t
    t = sqrt(2 + t)
check("ex16 limite 2", abs(prev - 2) < 1e-12)
# vitesse géométrique (pour l'exercice 24 du chapitre 6)
t = 0.0
for n in range(30):
    check("ex16 vitesse", abs(t - 2) <= 2*(1/(2*sqrt(2)))**n + 1e-15)
    t = sqrt(2 + t)
# --- Exercice 17 ------------------------------------------------------
t = 0.5
for n in range(6):
    check("ex17 (1/2)^(2^n)", isclose(t, 0.5**(2**n)))
    t = t*t
t = 1.5
for n in range(8):
    t = t*t
check("ex17 diverge", t > 1e30)
# --- Exercice 18 ------------------------------------------------------
om = 1/(1 - 1j/2)
check("ex18 point fixe", abs((1j/2)*om + 1 - om) < 1e-14 and abs(om - (0.8 + 0.4j)) < 1e-14)
z = 0j
for n in range(60):
    check("ex18 module", abs(z - om) <= abs(om)*0.5**n + 1e-15)
    z = (1j/2)*z + 1
# --- Exercice 19 (Cesàro) ---------------------------------------------
uu = [1/(n + 1) + 3 for n in range(5000)]
ces = sum(uu[:5000])/5000
check("ex19 Cesàro", abs(ces - 3) < 0.01)
# --- Exercice 20 ------------------------------------------------------
for k in range(1, 3000):
    check("ex20 encadrement", 1/(k + 1) <= log(1 + 1/k) <= 1/k)
H = 0.0
g_prev = None
for n in range(1, 3000):
    H += 1/n
    check("ex20 Hn≥ln(n+1)", H >= log(n + 1) - 1e-12)
    g = H - log(n)
    if g_prev is not None:
        check("ex20 gamma décroît", g < g_prev)
    g_prev = g
check("ex20 gamma≈0,577", 0.577 < g_prev < 0.578)
# --- Exercice 21 ------------------------------------------------------
for q in range(2, 10):
    aq = sum(Fraction(1, factorial(k)) for k in range(q + 1))
    r = factorial(q)*(math.e - float(aq))
    check("ex21 0<q!(e−a_q)<1/q", 0 < r < 1/q)
    check("ex21 q!a_q entier", (factorial(q)*aq).denominator == 1)
# --- Exercice 22 ------------------------------------------------------
a, b = 4.0, 1.0
pa, pb = a, b
for n in range(40):
    check("ex22 ordre", b <= a + 1e-12)
    na, nb = (a + b)/2, sqrt(a*b)
    check("ex22 a décroît, b croît", na <= a + 1e-12 and nb >= b - 1e-12)
    check("ex22 écart divisé par 2", na - nb <= (a - b)/2 + 1e-12)
    a, b = na, nb
check("ex22 limite commune", abs(a - b) < 1e-12 and 2.24 < a < 2.25)
# --- Exercice 24 ------------------------------------------------------
check("ex24 ratio Fibonacci", isclose(F[40]/F[39], phi, rel_tol=1e-15))
check("ex24 Cassini", all(F[n + 1]*F[n - 1] - F[n]**2 == (-1)**n for n in range(1, 40)))
r = 1.0
for n in range(80):
    r = 1 + 1/r
check("ex24 fraction continue", isclose(r, phi))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
