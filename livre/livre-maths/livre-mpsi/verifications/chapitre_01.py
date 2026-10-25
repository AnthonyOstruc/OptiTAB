# -*- coding: utf-8 -*-
"""Vérifications du chapitre 1 — Raisonnement et vocabulaire ensembliste.

Chaque assertion correspond à un résultat affirmé dans le cours, un énoncé
ou un corrigé. Exécution : python verifications/chapitre_01.py
"""
import itertools
import math
from fractions import Fraction

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

# --- L'essentiel ------------------------------------------------------
# 4^n + 1 héréditaire mais jamais divisible par 3 (contre-exemple du cours)
for n in range(50):
    check(f"4^{n}+1 non divisible par 3", (4**n + 1) % 3 != 0)
for k in range(30):
    check(f"identite 4^(k+1)+1 = 4(4^k+1)-3 (k={k})", 4**(k+1) + 1 == 4*(4**k + 1) - 3)
# P({1,2,3}) a 8 éléments ; en général 2^n
E = {1, 2, 3}
parts = [set(c) for r in range(4) for c in itertools.combinations(E, r)]
check("card P({1,2,3}) = 8", len(parts) == 8)
# 17 ≡ 2 [5]
check("17 ≡ 2 [5]", (17 - 2) % 5 == 0)
# 9π/4 ≡ π/4 [2π] : (9π/4 − π/4)/(2π) = 1 entier
check("9π/4 ≡ π/4 [2π]", Fraction(9, 4) - Fraction(1, 4) == 2 * Fraction(1, 1))

# --- Lois ensemblistes (vérifiées sur toutes les parties d'un ensemble) ---
U = set(range(6))
subsets = [set(c) for r in range(7) for c in itertools.combinations(U, r)]
import random
random.seed(1)
sample = random.sample(subsets, 24)
for A in sample:
    for B in sample:
        check("De Morgan ∪", U - (A | B) == (U - A) & (U - B))
        check("De Morgan ∩", U - (A & B) == (U - A) | (U - B))
        check("A\\(A\\B)=A∩B", A - (A - B) == A & B)
        check("A\\B = A∩complément(B)", A - B == A & (U - B))
        # différence symétrique
        check("A△B=(A∪B)\\(A∩B)", (A - B) | (B - A) == (A | B) - (A & B))
        check("A△B=∅ ssi A=B", (((A - B) | (B - A)) == set()) == (A == B))
        for C in sample[:6]:
            check("distributivité ∪ sur ∩", A | (B & C) == (A | B) & (A | C))
            check("distributivité ∩ sur ∪", A & (B | C) == (A & B) | (A & C))
            check("A\\(B∪C)=(A\\B)∩(A\\C)", A - (B | C) == (A - B) & (A - C))
# indicatrices
def ind(A):
    return {x: (1 if x in A else 0) for x in U}
for A in sample[:10]:
    for B in sample[:10]:
        iA, iB = ind(A), ind(B)
        check("1_{A∩B}=1_A·1_B", all(ind(A & B)[x] == iA[x]*iB[x] for x in U))
        check("1_{Ā}=1−1_A", all(ind(U - A)[x] == 1 - iA[x] for x in U))
        check("1_{A∪B}=1_A+1_B−1_A1_B",
              all(ind(A | B)[x] == iA[x] + iB[x] - iA[x]*iB[x] for x in U))
        check("A⊂B ssi 1_A≤1_B",
              (A <= B) == all(iA[x] <= iB[x] for x in U))

# --- Exercice 1 -------------------------------------------------------
check("n²+n pair", all((n*n + n) % 2 == 0 for n in range(200)))
# --- Exercice 5 -------------------------------------------------------
A = {1, 2, 3, 4, 5}; B = {4, 5, 6, 7}; E10 = set(range(1, 11))
check("ex5 A∪B", A | B == {1, 2, 3, 4, 5, 6, 7})
check("ex5 A∩B", A & B == {4, 5})
check("ex5 A\\B", A - B == {1, 2, 3})
check("ex5 B\\A", B - A == {6, 7})
check("ex5 compl A", E10 - A == {6, 7, 8, 9, 10})
check("ex5 compl B", E10 - B == {1, 2, 3, 8, 9, 10})
check("ex5 De Morgan", E10 - (A | B) == {8, 9, 10} == (E10 - A) & (E10 - B))
# --- Exercice 6 -------------------------------------------------------
check("ex6 card E×F", len(list(itertools.product("ab", [1, 2, 3]))) == 6)
# --- Exercice 7 (sur une grille fine de réels) -------------------------
xs = [i / 100 for i in range(-400, 401)]
img = sorted(x*x for x in xs if 1 <= x <= 2)
check("ex7 f([1,2])=[1,4]", math.isclose(img[0], 1) and math.isclose(img[-1], 4))
img = sorted(x*x for x in xs if -2 <= x <= 1)
check("ex7 f([-2,1])=[0,4]", math.isclose(img[0], 0) and math.isclose(img[-1], 4))
pre = [x for x in xs if 1 <= x*x <= 4]
check("ex7 f⁻¹([1,4])", all(1 <= abs(x) <= 2 for x in pre) and 1.5 in pre and -1.5 in pre)
check("ex7 f⁻¹([−2,−1])=∅", not [x for x in xs if -2 <= x*x <= -1])
check("ex7 g⁻¹([0,1])", all(-0.5 <= x <= 0 for x in xs if 0 <= 2*x + 1 <= 1))
# --- Exercice 9 -------------------------------------------------------
from sympy import symbols, expand, simplify, sqrt, Rational
x, y = symbols("x y")
check("ex9b (x+1)(y−1)−(x−1)(y+1)=2(y−x)",
      expand((x + 1)*(y - 1) - (x - 1)*(y + 1) - 2*(y - x)) == 0)
check("ex9c n impair ⇒ 8 | n²−1", all((n*n - 1) % 8 == 0 for n in range(1, 400, 2)))
# --- Exercice 11 ------------------------------------------------------
check("ex11a n(n+1)/2 entier", all((n*(n + 1)) % 2 == 0 for n in range(500)))
check("ex11b 3 | n(n²+2)", all((n*(n*n + 2)) % 3 == 0 for n in range(-300, 300)))
sols = [xx for xx in [Fraction(i, 10) for i in range(-100, 101)]
        if abs(xx - 1) + abs(xx + 2) == 5]
check("ex11c solutions −3 et 2", sols == [Fraction(-3), Fraction(2)])
# --- Exercice 12 ------------------------------------------------------
check("ex12b f(x)=x+1 solution",
      expand((x + 1)*(y + 1) - (x*y + 1) - (x + y)) == 0)
# --- Exercice 13 ------------------------------------------------------
check("ex13a somme des carrés",
      all(sum(k*k for k in range(1, n + 1)) == n*(n + 1)*(2*n + 1)//6
          for n in range(1, 200)))
check("ex13a factorisation 2k²+7k+6", expand((x + 2)*(2*x + 3) - (2*x**2 + 7*x + 6)) == 0)
check("ex13b 2^n>n", all(2**n > n for n in range(200)))
check("ex13c n!≥2^n pour n≥4", all(math.factorial(n) >= 2**n for n in range(4, 60)))
check("ex13d 7 | 3^(2n+1)+2^(n+2)", all((3**(2*n + 1) + 2**(n + 2)) % 7 == 0
                                        for n in range(100)))
# --- Exercice 14 ------------------------------------------------------
u = [2, 5]
for n in range(60):
    u.append(5*u[-1] - 6*u[-2])
check("ex14a u_n=2^n+3^n", all(u[n] == 2**n + 3**n for n in range(len(u))))
v = [None, 1]
for n in range(1, 40):
    v.append(sum(v[1:n + 1]))
check("ex14c v2..v4 = 1,2,4", (v[2], v[3], v[4]) == (1, 2, 4))
check("ex14c v_n=2^(n−2)", all(v[n] == 2**(n - 2) for n in range(2, 41)))
# --- Exercice 16 ------------------------------------------------------
check("ex16d {1,2,3,4}△{3,4,5,6}",
      ({1, 2, 3, 4} ^ {3, 4, 5, 6}) == {1, 2, 5, 6})
# --- Exercice 18 ------------------------------------------------------
sq = lambda s: {t*t for t in s}
check("ex18c contre-exemple", sq({-1} & {1}) == set() and sq({-1}) & sq({1}) == {1})
check("ex18e f⁻¹(f({1}))={−1,1}", {t for t in range(-5, 6) if t*t in sq({1})} == {-1, 1})
pre = [z for z in xs if -4 <= z*z <= 4]
check("ex18e f(f⁻¹([−4,4]))=[0,4]",
      math.isclose(min(t*t for t in pre), 0) and math.isclose(max(t*t for t in pre), 4))
# --- Exercice 19 ------------------------------------------------------
# E=G={1}, F={1,2} : g∘f=Id, f non surjective, g non injective
f = {1: 1}; g = {1: 1, 2: 1}
check("ex19d g∘f=Id", g[f[1]] == 1)
check("ex19d f non surjective", set(f.values()) != {1, 2})
check("ex19d g non injective", g[1] == g[2])
# --- Exercice 20 ------------------------------------------------------
def f20(n):
    return n // 2 if n % 2 == 0 else -(n + 1) // 2
vals = [f20(n) for n in range(2001)]
check("ex20a premiers termes", vals[:5] == [0, -1, 1, -2, 2])
check("ex20a injective", len(set(vals)) == len(vals))
check("ex20a atteint [−1000,1000]", set(vals) == set(range(-1000, 1001)))
def f20inv(m):
    return 2*m if m >= 0 else -2*m - 1
check("ex20a réciproque", all(f20(f20inv(m)) == m for m in range(-900, 900)))
g20 = lambda t: (2*t + 1)/(t - 1)
g20inv = lambda t: (t + 1)/(t - 2)
pts = [i/7 for i in range(-50, 51) if i/7 != 1 and abs(g20(i/7) - 2) > 1e-12]
check("ex20b réciproque", all(math.isclose(g20inv(g20(t)), t) for t in pts))
h20 = lambda t: t/(1 + abs(t))
h20inv = lambda s: s/(1 - abs(s))
ts = [i/9 for i in range(-80, 81)]
check("ex20c h à valeurs dans ]−1,1[", all(-1 < h20(t) < 1 for t in ts))
check("ex20c réciproque", all(math.isclose(h20inv(h20(t)), t) for t in ts))
# --- Exercice 21 ------------------------------------------------------
for A in sample[:8]:
    sols = [X for X in subsets if (A & X == set() and A | X == U)]
    check("ex21a X=complément(A)", sols == [U - A])
    for B in sample[:8]:
        if A <= B:
            sols = {frozenset(X) for X in subsets if A | X == B}
            attendu = {frozenset(X) for X in subsets if (B - A) <= X <= B}
            check("ex21b solutions = [B\\A, B]", sols == attendu)
# --- Exercice 23 ------------------------------------------------------
maj = [m for m in range(1, 301) if m % 4 == 0 and m % 6 == 0]
check("ex23e majorants de {4,6} = multiples de 12",
      maj == list(range(12, 301, 12)))
# --- Exercice 24 ------------------------------------------------------
E = (1, 2, 3)
PE = [frozenset(c) for r in range(4) for c in itertools.combinations(E, r)]
f24 = {1: frozenset({1, 2}), 2: frozenset(), 3: frozenset({1, 3})}
D = {z for z in E if z not in f24[z]}
check("ex24 D={2}", D == {2})
check("ex24 D sans antécédent", frozenset(D) not in f24.values())
check("ex24 f injective", len(set(f24.values())) == 3)
check("ex24 8^3=512 applications", 8**3 == 512)
# aucune application E→P(E) n'est surjective (vérification exhaustive)
aucune = all(len(set(images)) < 8
             for images in itertools.product(PE, repeat=3))
check("ex24 aucune surjection E→P(E)", aucune)

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
