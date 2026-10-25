# -*- coding: utf-8 -*-
"""Vérifications du chapitre 7 — Arithmétique des entiers relatifs."""
import math
from math import gcd, lcm, factorial, isqrt, prod

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

def est_premier(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, isqrt(n) + 1))

def v(p, n):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k

# --- L'essentiel ------------------------------------------------------
check("essentiel Euclide 252,198", gcd(252, 198) == 18)
check("essentiel rectangle 21x15", gcd(21, 15) == 3)
check("essentiel pgcd×ppcm", gcd(252, 198)*lcm(252, 198) == 252*198)
check("essentiel premiers ≤ 50",
      [p for p in range(2, 51) if est_premier(p)] ==
      [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47])
# --- Exercice 1 -------------------------------------------------------
div60 = [d for d in range(1, 61) if 60 % d == 0]
check("ex1a diviseurs de 60", div60 == [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60])
check("ex1b n|n+6", [n for n in range(1, 100) if (n + 6) % n == 0] == [1, 2, 3, 6])
check("ex1d 6|n(n+1)(n+2)", all(n*(n + 1)*(n + 2) % 6 == 0 for n in range(-200, 200)))
# --- Exercice 2 -------------------------------------------------------
check("ex2a 1234=56·22+2", 1234 == 56*22 + 2 and 0 <= 2 < 56)
check("ex2a −37=5·(−8)+3", -37 == 5*(-8) + 3 and 0 <= 3 < 5)
check("ex2c n²=(n+1)(n−1)+1", all(n*n == (n + 1)*(n - 1) + 1 for n in range(100)))
check("ex2d carrés mod 4", {n*n % 4 for n in range(100)} == {0, 1})
# --- Exercice 3 -------------------------------------------------------
check("ex3 pgcd(252,198)", gcd(252, 198) == 18)
check("ex3 étapes", (252 % 198, 198 % 54, 54 % 36, 36 % 18) == (54, 36, 18, 0))
check("ex3 pgcd(1071,462)", gcd(1071, 462) == 21
      and (1071 % 462, 462 % 147, 147 % 21) == (147, 21, 0))
check("ex3 pgcd(2024,2026)", gcd(2024, 2026) == 2)
# --- Exercice 4 -------------------------------------------------------
check("ex4 Bézout 252,198", 4*252 - 5*198 == 18)
check("ex4 Bézout 17,5", -2*17 + 7*5 == 1)
# --- Exercice 5 -------------------------------------------------------
check("ex5 180=2²3²5, 84=2²·3·7", 180 == 2**2*3**2*5 and 84 == 2**2*3*7)
check("ex5 pgcd/ppcm", gcd(180, 84) == 12 and lcm(180, 84) == 1260)
check("ex5 produit", 12*1260 == 180*84)
check("ex5 15,28", gcd(15, 28) == 1 and lcm(15, 28) == 420)
# --- Exercice 6 -------------------------------------------------------
check("ex6a 2^10 mod 7", pow(2, 10, 7) == 2 and pow(2, 3, 7) == 1)
check("ex6b 3^100 mod 8", pow(3, 100, 8) == 1)
check("ex6c unités de 7^2026", pow(7, 2026, 10) == 9 and 2026 % 4 == 2)
check("ex6d 1234567 mod 9", 1234567 % 9 == 1 and sum(map(int, "1234567")) % 9 == 1)
# --- Exercice 7 -------------------------------------------------------
check("ex7b 191 premier", est_premier(191) and isqrt(191) == 13)
check("ex7c 323=17·19", 323 == 17*19 and not est_premier(323))
# --- Exercice 8 -------------------------------------------------------
check("ex8 360", 360 == 2**3*3**2*5)
check("ex8 1001", 1001 == 7*11*13)
check("ex8 2024", 2024 == 2**3*11*23)
check("ex8 pgcd(360,2024)", gcd(360, 2024) == 8)
check("ex8 nb diviseurs de 360", sum(1 for d in range(1, 361) if 360 % d == 0) == 24
      and (3 + 1)*(2 + 1)*(1 + 1) == 24)
# --- Exercice 9 -------------------------------------------------------
check("ex9a invariance", all(gcd(a, b) == gcd(b, a - 3*b)
      for a in range(1, 60) for b in range(1, 40)))
check("ex9b pgcd(n,n+1)", all(gcd(n, n + 1) == 1 for n in range(1, 2000)))
check("ex9c pgcd(2n+1,n)", all(gcd(2*n + 1, n) == 1 for n in range(1, 2000)))
check("ex9d pgcd(n²+n,2n+1)", all(gcd(n*n + n, 2*n + 1) == 1 for n in range(1, 2000)))
check("ex9d identité", all(4*(n*n + n) == (2*n + 1)**2 - 1 for n in range(100)))
# --- Exercice 10 ------------------------------------------------------
check("ex10 17x+5y=1", 17*(-2) + 5*7 == 1)
check("ex10 17x+5y=4", 17*(-8) + 5*28 == 4)
sols = [(1 + 3*k, 1 - 2*k) for k in range(-50, 50)]
check("ex10 2x+3y=5", all(2*x + 3*y == 5 for x, y in sols))
brute = {(x, y) for x in range(-150, 150) for y in range(-100, 100) if 12*x + 18*y == 30}
check("ex10 toutes les solutions", brute == {(1 + 3*k, 1 - 2*k) for k in range(-51, 50)
      if abs(1 + 3*k) < 150 and abs(1 - 2*k) < 100})
# --- Exercice 11 ------------------------------------------------------
check("ex11a 7|3n ⇒ 7|n", all(n % 7 == 0 for n in range(1, 700) if (3*n) % 7 == 0))
check("ex11b 9|6n ⟺ 3|n", all(((6*n) % 9 == 0) == (n % 3 == 0) for n in range(1, 500)))
check("ex11d 2024/2576", gcd(2024, 2576) == 184 and 2024//184 == 11 and 2576//184 == 14)
# --- Exercice 12 ------------------------------------------------------
check("ex12b 3(2n+1)−2(3n+2)=−1", all(3*(2*n + 1) - 2*(3*n + 2) == -1 for n in range(50)))
check("ex12b irréductible", all(gcd(2*n + 1, 3*n + 2) == 1 for n in range(1, 2000)))
check("ex12c ensemble vs 2 à 2", math.gcd(6, 10, 15) == 1
      and gcd(6, 10) == 2 and gcd(6, 15) == 3 and gcd(10, 15) == 5)
check("ex12d a+b ⊥ ab", all(gcd(a + b, a*b) == 1
      for a in range(1, 60) for b in range(1, 60) if gcd(a, b) == 1))
# --- Exercice 13 ------------------------------------------------------
check("ex13b inverse de 5 mod 7", (5*3) % 7 == 1)
check("ex13b inverse de 17 mod 26", (17*23) % 26 == 1)
check("ex13c 5x≡3[7]", [x for x in range(7) if (5*x) % 7 == 3] == [2])
check("ex13d 17x≡4[26]", [x for x in range(26) if (17*x) % 26 == 4] == [14])
# --- Exercice 14 ------------------------------------------------------
check("ex14 8791236 par 9", 8791236 % 9 == 0 and sum(map(int, "8791236")) == 36)
alt = 6 - 3 + 2 - 1 + 9 - 7 + 8
check("ex14 par 11", alt == 14 and 8791236 % 11 != 0)
check("ex14 chiffre x", [x for x in range(10) if (5304 + 10*x) % 9 == 0] == [6]
      and int("5364") % 9 == 0)
# --- Exercice 15 ------------------------------------------------------
check("ex15a 2^10 mod 11", pow(2, 10, 11) == 1)
check("ex15b 2^2026 mod 11", pow(2, 2026, 11) == 9 and 2026 % 10 == 6 and 2**6 % 11 == 9)
check("ex15c 11|n^11−n", all((n**11 - n) % 11 == 0 for n in range(-100, 100)))
check("ex15d 7^222 mod 13", pow(7, 222, 13) == 12 and 222 % 12 == 6
      and pow(7, 6, 13) == 12)
# --- Exercice 16 ------------------------------------------------------
check("ex16a v2(96)=5, v3(96)=1, v2(2024)=3", v(2, 96) == 5 and v(3, 96) == 1
      and v(2, 2024) == 3)
for p in [2, 3, 5, 7]:
    check(f"ex16b v_{p} produit", all(v(p, a*b) == v(p, a) + v(p, b)
          for a in range(1, 80) for b in range(1, 80)))
check("ex16c divisibilité par valuations",
      all((b % a == 0) == all(v(p, a) <= v(p, b) for p in [2, 3, 5, 7, 11, 13])
          for a in range(1, 100) for b in range(1, 100)
          if all(est_premier(p) or True for p in [a])
          and prod(p**v(p, a) for p in [2, 3, 5, 7, 11, 13]) == a
          and prod(p**v(p, b) for p in [2, 3, 5, 7, 11, 13]) == b))
# --- Exercice 17 ------------------------------------------------------
check("ex17 2^11−1", 2**11 - 1 == 2047 == 23*89)
check("ex17 factorisation", all((2**(a*b) - 1) % (2**a - 1) == 0
      for a in range(2, 12) for b in range(2, 8)))
check("ex17 Mersenne premiers", [n for n in range(2, 14) if est_premier(2**n - 1)]
      == [2, 3, 5, 7, 13])
# --- Exercice 18 ------------------------------------------------------
check("ex18a x≡2[5], x≡3[7]", [x for x in range(35) if x % 5 == 2 and x % 7 == 3] == [17])
check("ex18a inverse de 5 mod 7", (5*3) % 7 == 1)
check("ex18b Sun Zi", [x for x in range(105) if x % 3 == 2 and x % 5 == 3 and x % 7 == 2]
      == [23])
# --- Exercice 19 ------------------------------------------------------
check("ex19c n!+k composés", all(not est_premier(factorial(7) + k) for k in range(2, 8)))
# --- Exercice 20 ------------------------------------------------------
F = [2**(2**n) + 1 for n in range(6)]
check("ex20a F0..F4 premiers", all(est_premier(F[n]) for n in range(5)))
check("ex20a F5 composé", F[5] % 641 == 0)
for n in range(1, 6):
    check(f"ex20b produit n={n}", prod(F[k] for k in range(n)) + 2 == F[n])
check("ex20c premiers entre eux", all(gcd(F[m], F[n]) == 1
      for m in range(6) for n in range(6) if m != n))
# --- Exercice 21 ------------------------------------------------------
def legendre(p, n):
    s, pk = 0, p
    while pk <= n:
        s += n//pk
        pk *= p
    return s
check("ex21 v2(10!)", v(2, factorial(10)) == 8 == 5 + 2 + 1 == legendre(2, 10))
check("ex21 v5(100!)", v(5, factorial(100)) == 24 == 20 + 4 == legendre(5, 100))
check("ex21 zéros de 100!", str(factorial(100)).rstrip("0") != str(factorial(100))
      and len(str(factorial(100))) - len(str(factorial(100)).rstrip("0")) == 24)
check("ex21 Legendre général", all(v(p, factorial(n)) == legendre(p, n)
      for p in [2, 3, 5] for n in range(1, 60)))
# --- Exercice 22 (Wilson) ---------------------------------------------
for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
    check(f"ex22 Wilson p={p}", (factorial(p - 1) + 1) % p == 0)
for n in [4, 6, 8, 9, 10, 12, 15]:
    check(f"ex22 composé n={n}", (factorial(n - 1) + 1) % n != 0)
check("ex22 (n−1)!≡0 pour n composé >4", all(factorial(n - 1) % n == 0
      for n in [6, 8, 9, 10, 12, 14, 15, 16] ))
check("ex22 cas n=4", factorial(3) % 4 == 2)
# --- Exercice 23 (561, nombre de Carmichael) --------------------------
check("ex23 561=3·11·17", 561 == 3*11*17 and not est_premier(561))
check("ex23 560 divisible par 2,10,16", 560 % 2 == 0 and 560 % 10 == 0 and 560 % 16 == 0)
check("ex23 menteur de Fermat", all(pow(a, 561, 561) == a % 561 for a in range(561)))
# --- Exercice 24 (triplets pythagoriciens) ----------------------------
trip = {tuple(sorted((m*m - n*n, 2*m*n))) + (m*m + n*n,)
        for m in range(2, 20) for n in range(1, 20)
        if n < m and gcd(m, n) == 1 and (m - n) % 2 == 1}
check("ex24 paramétrisation valide", all(x*x + y*y == z*z and math.gcd(x, y, z) == 1
      for x, y, z in trip))
brute = {tuple(sorted((x, y))) + (z,) for x in range(1, 150) for y in range(x, 150)
         for z in range(y, 212) if x*x + y*y == z*z and math.gcd(x, y, z) == 1}
param = {t for t in trip if t[2] < 212 and t[0] < 150 and t[1] < 150 and t[1] >= t[0]}
check("ex24 exhaustivité (petits triplets)", brute <= {tuple(sorted(t[:2])) + (t[2],) for t in trip} | brute and
      all(t in {tuple(sorted(u[:2])) + (u[2],) for u in trip} for t in brute))
check("ex24 exemples", (3, 4, 5) in brute and (5, 12, 13) in brute and (20, 21, 29) in brute)
check("ex24 carrés mod 4", all((x % 2 == 0) != (y % 2 == 0) for x, y, z in brute))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
