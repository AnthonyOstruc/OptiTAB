# -*- coding: utf-8 -*-
"""Vérifications du chapitre 16 — Dénombrement."""
import math
from itertools import combinations, permutations, product
from math import comb, factorial, perm, isclose

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

# --- Exercice 1 : premiers décomptes -----------------------------------
check("ex1 menus", 3*4*2 == 24)
check("ex1 codes PIN", 10**4 == 10000)
check("ex1 plaques AB-123-CD", 26**2*10**3*26**2 == 456976000)
# --- Exercice 2 : unions -----------------------------------------------
check("ex2 au moins une matiere", 18 + 15 - 8 == 25)
check("ex2 aucune", 30 - 25 == 5)
A = set(range(0, 20, 2)); B = set(range(0, 20, 3))
check("ex2 formule union", len(A | B) == len(A) + len(B) - len(A & B))
# --- Exercice 3 : listes -----------------------------------------------
check("ex3 mots de 3 lettres", 26**3 == 17576)
check("ex3 sans repetition", 26*25*24 == 15600 == perm(26, 3))
check("ex3 injections", perm(5, 3) == 60
      and sum(1 for p in permutations(range(5), 3)) == 60)
check("ex3 applications", 5**3 == len(list(product(range(5), repeat=3))))
# --- Exercice 4 : anagrammes -------------------------------------------
check("ex4 MPSI", factorial(4) == 24)
check("ex4 OPTITAB", factorial(7)//factorial(2) == 2520)
check("ex4 OPTITAB brute force", len({p for p in permutations("OPTITAB")}) == 2520)
check("ex4 rangements", factorial(5) == 120)
# --- Exercice 5 : combinaisons -----------------------------------------
check("ex5 C(5,2)", comb(5, 2) == 10)
check("ex5 C(10,3)", comb(10, 3) == 120)
check("ex5 mains", comb(32, 5) == 201376)
check("ex5 comites", comb(12, 4) == 495)
# --- Exercice 6 : triangle de Pascal -----------------------------------
check("ex6 Pascal", all(comb(n, p) == comb(n - 1, p - 1) + comb(n - 1, p)
      for n in range(1, 10) for p in range(1, n)))
check("ex6 symetrie", all(comb(n, p) == comb(n, n - p)
      for n in range(10) for p in range(n + 1)))
check("ex6 somme ligne", all(sum(comb(n, p) for p in range(n + 1)) == 2**n
      for n in range(10)))
check("ex6 ligne 6", [comb(6, p) for p in range(7)] == [1, 6, 15, 20, 15, 6, 1])
# --- Exercice 7 : binome -----------------------------------------------
check("ex7 coefficient de x^3 dans (1+x)^7", comb(7, 3) == 35)
check("ex7 somme alternee", all(sum((-1)**k*comb(n, k) for k in range(n + 1)) == 0
      for n in range(1, 10)))
# --- Exercice 8 : parties ----------------------------------------------
E8 = range(5)
allparts = [s for r in range(6) for s in combinations(E8, r)]
check("ex8 2^n parties", len(allparts) == 32)
check("ex8 parties paires", sum(1 for s in allparts if len(s) % 2 == 0) == 16)
check("ex8 contenant 0", sum(1 for s in allparts if 0 in s) == 16)
# --- Exercice 9 : tiroirs ----------------------------------------------
check("ex9 13 > 12 mois", 13 > 12)
check("ex9 n+1 dans 2n : consecutifs", all(
    any(abs(a - b) == 1 for a in s for b in s if a != b)
    for s in combinations(range(1, 9), 5)))  # n = 4 : tout choix de 5 dans 1..8
check("ex9 quarts du carre", isclose((2**0.5/2)**2, 0.5) and 5 > 4)
# --- Exercice 10 : comites ---------------------------------------------
check("ex10 exactement 2 femmes", comb(7, 2)*comb(5, 2) == 210)
check("ex10 au moins une femme", comb(12, 4) - comb(5, 4) == 490)
check("ex10 double comptage president", comb(12, 4)*4 == 12*comb(11, 3) == 1980)
# --- Exercice 11 : mains de cartes -------------------------------------
check("ex11 exactement 2 as", comb(4, 2)*comb(28, 3) == 19656)
check("ex11 au moins un as", comb(32, 5) - comb(28, 5) == 103096)
check("ex11 verif complementaire", comb(28, 5) == 98280)
# --- Exercice 12 : chemins sur une grille ------------------------------
def chemins(p, q):
    if p == 0 or q == 0:
        return 1
    return chemins(p - 1, q) + chemins(p, q - 1)
check("ex12 formule", all(chemins(p, q) == comb(p + q, p)
      for p in range(6) for q in range(6)))
check("ex12 (4,3)", comb(7, 4) == 35)
check("ex12 par un point", comb(3, 1)*comb(4, 3) == 12)  # (0,0)->(1,2)->(4,3)
# --- Exercice 13 : comite avec chef ------------------------------------
check("ex13 k C(n,k) = n C(n-1,k-1)", all(
    k*comb(n, k) == n*comb(n - 1, k - 1)
    for n in range(1, 12) for k in range(1, n + 1)))
check("ex13 somme k C(n,k)", all(
    sum(k*comb(n, k) for k in range(n + 1)) == n*2**(n - 1)
    for n in range(1, 12)))
check("ex13 somme k(k-1)C(n,k)", all(
    sum(k*(k - 1)*comb(n, k) for k in range(n + 1)) == n*(n - 1)*2**(n - 2)
    for n in range(2, 12)))
# --- Exercice 14 : Vandermonde -----------------------------------------
check("ex14 Vandermonde", all(
    sum(comb(p, k)*comb(q, n - k) for k in range(n + 1)) == comb(p + q, n)
    for p in range(8) for q in range(8) for n in range(p + q + 1)))
check("ex14 somme des carres", all(
    sum(comb(n, k)**2 for k in range(n + 1)) == comb(2*n, n)
    for n in range(10)))
# --- Exercice 15 : surjections sur 2 et 3 éléments ---------------------
def nb_surj(n, p):
    return sum(1 for f in product(range(p), repeat=n) if len(set(f)) == p)
check("ex15 sur 2", all(nb_surj(n, 2) == 2**n - 2 for n in range(2, 9)))
check("ex15 sur 3", all(nb_surj(n, 3) == 3**n - 3*2**n + 3 for n in range(3, 9)))
# --- Exercice 16 : x1+...+xp = n ---------------------------------------
def nb_sol(p, n):
    if p == 1:
        return 1
    return sum(nb_sol(p - 1, n - k) for k in range(n + 1))
check("ex16 etoiles et barres", all(
    nb_sol(p, n) == comb(n + p - 1, p - 1)
    for p in range(1, 6) for n in range(8)))
check("ex16 x+y+z=10", comb(12, 2) == 66)
# --- Exercice 17 : applications monotones ------------------------------
def nb_str_croiss(p, n):
    return sum(1 for c in combinations(range(n), p))
check("ex17 strictement croissantes", all(
    nb_str_croiss(p, n) == comb(n, p) for n in range(1, 9) for p in range(n + 1)))
def nb_croiss(p, n):
    return sum(1 for f in product(range(n), repeat=p)
               if all(f[i] <= f[i + 1] for i in range(p - 1)))
check("ex17 croissantes larges", all(
    nb_croiss(p, n) == comb(n + p - 1, p)
    for n in range(1, 6) for p in range(1, 5)))
# --- Exercice 18 : binome et analyse -----------------------------------
check("ex18 somme C(n,k)/(k+1)", all(
    sum(comb(n, k)/(k + 1) for k in range(n + 1))*(n + 1) == 2**(n + 1) - 1
    for n in range(10)))
# --- Exercice 19 : derangements ----------------------------------------
def derangements_bf(n):
    return sum(1 for p in permutations(range(n))
               if all(p[i] != i for i in range(n)))
D = [1, 0]
for n in range(2, 11):
    D.append((n - 1)*(D[n - 1] + D[n - 2]))
check("ex19 recurrence vs brute force", all(D[n] == derangements_bf(n)
      for n in range(8)))
check("ex19 formule serie", all(
    D[n] == round(sum((-1)**k/factorial(k) for k in range(n + 1))*factorial(n))
    for n in range(11)))
check("ex19 D_n/n! -> 1/e", isclose(D[10]/factorial(10), 1/math.e, rel_tol=1e-7))
check("ex19 autre recurrence", all(D[n] == n*D[n - 1] + (-1)**n
      for n in range(2, 11)))
# --- Exercice 20 : crible a 3 ensembles --------------------------------
m2 = len(range(2, 101, 2)); m3 = len(range(3, 101, 3)); m5 = len(range(5, 101, 5))
m6 = len(range(6, 101, 6)); m10 = len(range(10, 101, 10)); m15 = len(range(15, 101, 15))
m30 = len(range(30, 101, 30))
union = m2 + m3 + m5 - m6 - m10 - m15 + m30
reste = 100 - union
brute = sum(1 for k in range(1, 101) if k % 2 and k % 3 and k % 5)
check("ex20 crible", (m2, m3, m5, m6, m10, m15, m30) == (50, 33, 20, 16, 10, 6, 3))
check("ex20 resultat 26", reste == 26 == brute)
# --- Exercice 21 : Catalan ---------------------------------------------
def catalan_bf(n):
    # chemins de (0,0) a (n,n) ne passant jamais strictement au-dessus de la diagonale
    def rec(x, y):
        if x == n and y == n:
            return 1
        total = 0
        if x < n:
            total += rec(x + 1, y)
        if y < x:  # rester sous la diagonale (y <= x)
            pass
        if y < n and y + 1 <= x:
            total += rec(x, y + 1)
        return total
    return rec(0, 0)
check("ex21 Catalan", all(catalan_bf(n) == comb(2*n, n)//(n + 1)
      for n in range(1, 8)))
check("ex21 valeurs", [comb(2*n, n)//(n + 1) for n in range(1, 6)]
      == [1, 2, 5, 14, 42])
check("ex21 reflexion", all(
    comb(2*n, n) - comb(2*n, n - 1) == comb(2*n, n)//(n + 1)
    for n in range(1, 10)))
# --- Exercice 22 : double comptage -------------------------------------
check("ex22 C(2n,2)", all(comb(2*n, 2) == 2*comb(n, 2) + n**2
      for n in range(1, 12)))
check("ex22 crosse de hockey", all(
    sum(comb(k, 2) for k in range(2, n + 1)) == comb(n + 1, 3)
    for n in range(2, 14)))
# --- Exercice 23 : points fixes ----------------------------------------
def nb_avec_k_fixes(n, k):
    return sum(1 for p in permutations(range(n))
               if sum(1 for i in range(n) if p[i] == i) == k)
for n in range(1, 8):
    check(f"ex23 formule n={n}", all(
        nb_avec_k_fixes(n, k) == comb(n, k)*D[n - k] for k in range(n + 1)))
check("ex23 partition de n!", all(
    sum(comb(n, k)*D[n - k] for k in range(n + 1)) == factorial(n)
    for n in range(1, 11)))
check("ex23 moyenne des points fixes = 1", all(
    sum(k*comb(n, k)*D[n - k] for k in range(n + 1)) == factorial(n)
    for n in range(1, 11)))
# --- Exercice 24 : parties sans elements consecutifs -------------------
def sans_consecutifs(n):
    cnt = 0
    for r in range(n + 1):
        for s in combinations(range(1, n + 1), r):
            if all(s[i + 1] - s[i] >= 2 for i in range(len(s) - 1)):
                cnt += 1
    return cnt
F = [0, 1]
for _ in range(20):
    F.append(F[-1] + F[-2])
check("ex24 Fibonacci", all(sans_consecutifs(n) == F[n + 2] for n in range(1, 13)))
check("ex24 par cardinal", all(
    sum(comb(n - k + 1, k) for k in range(n + 1)) == F[n + 2]
    for n in range(1, 13)))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
