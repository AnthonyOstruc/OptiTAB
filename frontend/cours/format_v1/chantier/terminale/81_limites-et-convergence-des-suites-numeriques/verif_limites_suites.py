# -*- coding: utf-8 -*-
"""Vérification des résultats de la notion « Limites et convergence des suites ».

    python verif_limites_suites.py      → « TOUT EST JUSTE » ou la liste des erreurs
"""
import math

import sympy as sp

n, k, a, x, m = sp.symbols("n k a x m", positive=True)
oo = sp.oo
erreurs = []


def egal(nom, obtenu, attendu):
    if sp.simplify(obtenu - attendu) != 0 if not (obtenu in (oo, -oo) or attendu in (oo, -oo)) else obtenu != attendu:
        erreurs.append(f"{nom} : obtenu {obtenu}, attendu {attendu}")


def lim(nom, expr, attendu):
    egal(nom, sp.limit(expr, n, oo), attendu)


# ---------------------------------------------------------------- cours
# récurrence de l'exemple : 1 <= u_n <= u_{n+1} <= 2, limite 2
u = [1.0]
for _ in range(60):
    u.append(0.5 * u[-1] + 1)
assert all(1 <= u[i] <= u[i + 1] <= 2 for i in range(59)), "exemple du I"
assert abs(u[-1] - 2) < 1e-12
assert sp.solve(sp.Eq(x, sp.Rational(1, 2) * x + 1), x) == [2]
# 4^n + 1 : héréditaire, jamais divisible par 3
assert sp.expand(4 * (4**k + 1) - 3 - (4**(k + 1) + 1)) == 0
assert all((4**i + 1) % 3 == 2 for i in range(50))
# Bernoulli : (1+a)(1+ka) = 1 + (k+1)a + k a^2
assert sp.expand((1 + k * a) * (1 + a) - (1 + (k + 1) * a + k * a**2)) == 0
assert all((1 + aa) ** i >= 1 + i * aa for aa in (0.01, 0.5, 2, 10) for i in range(40))
# formes indéterminées levées
lim("cours n^2-5n", n**2 - 5 * n, oo)
lim("cours (3n^2+1)/(n^2-5n)", (3 * n**2 + 1) / (n**2 - 5 * n), 3)
assert sp.simplify((n**2 * (3 + 1 / n**2)) / (n**2 * (1 - 5 / n)) - (3 * n**2 + 1) / (n**2 - 5 * n)) == 0
# gendarmes
lim("cours 1+sin n/n (encadrement bas)", 1 - 1 / n, 1)
lim("cours 1+sin n/n (encadrement haut)", 1 + 1 / n, 1)
assert all(1 - 1 / i <= 1 + math.sin(i) / i <= 1 + 1 / i for i in range(1, 500))
# somme géométrique q = 1/2
Sn = sum(sp.Rational(1, 2) ** j for j in range(11))
assert Sn == 2 * (1 - sp.Rational(1, 2) ** 11)
lim("cours S_n", 2 * (1 - sp.Rational(1, 2) ** (n + 1)), 2)


def seuil(e):
    nn, p = 0, 1
    while p >= e:
        p = 0.8 * p
        nn = nn + 1
    return nn


assert seuil(0.001) == 31 and 0.8**30 >= 0.001 > 0.8**31
assert abs(0.8**30 - 0.00124) < 5e-6 and abs(0.8**31 - 0.00099) < 5e-6
# u_n = 1 - 1/(n+1) croissante, majorée par 5, limite 1
lim("cours 1-1/(n+1)", 1 - 1 / (n + 1), 1)

# ---------------------------------------------------------------- exercices
# 1162
for nom, e, l in [("1162.1", 1 / n, 0), ("1162.2", 1 / n**2, 0), ("1162.3", n**3, oo),
                  ("1162.4", sp.sqrt(n), oo), ("1162.5", 5 + 2 / n, 5)]:
    lim(nom, e, l)
# 1163
for nom, e, l in [("1163.1", n + 7, oo), ("1163.2", 3 * n * (1 / n), 3), ("1163.3", (n + 1) / n, 1),
                  ("1163.4", 2 - 5 / n**2, 2)]:
    lim(nom, e, l)
# 1171 (DS)
lim("1171.A1", (2 * n**2 + 3 * n - 1) / (n**2 + 5), 2)
lim("1171.A2", n**3 - 2 * n**2, oo)
lim("1171.A3", 3 * sp.Rational(2, 3) ** n, 0)
lim("1171.B1 bas", (2 * n - 1) / (n + 1), 2)
lim("1171.B1 haut", (2 * n + 1) / (n + 1), 2)
lim("1171.B2 bas", (n**2 - 1) / (n**2 + 1), 1)
assert all((2 * i - 1) / (i + 1) <= (2 * i + math.sin(i)) / (i + 1) <= (2 * i + 1) / (i + 1) for i in range(0, 2000))
assert all((i * i - 1) / (i * i + 1) <= (i * i - 1) / (i * i + math.cos(i)) <= 1 for i in range(2, 2000))
v = [0.0]
for _ in range(60):
    v.append((v[-1] + 3) / 4)
assert all(0 <= v[i] <= 1 and v[i] <= v[i + 1] for i in range(59)) and abs(v[-1] - 1) < 1e-12
assert sp.simplify((x + 3) / 4 - x - 3 * (1 - x) / 4) == 0
assert sp.solve(sp.Eq(x, (x + 3) / 4), x) == [1]
assert abs(v[1] - 0.75) < 1e-12 and abs(v[2] - 0.9375) < 1e-12
# 1167
for nom, e, l in [("1167.1", n**2 - n, oo), ("1167.2", (3 * n**2 + 2 * n + 1) / (5 * n**2 - 4), sp.Rational(3, 5)),
                  ("1167.3", (2 * n**3 - n + 1) / (n**2 + 3 * n), oo), ("1167.4", n - sp.sqrt(n), oo),
                  ("1167.5", (4 * n + 3) / (2 * n**3 - n**2 + 1), 0),
                  ("1167.6", sp.sqrt(n**2 + n) - n, sp.Rational(1, 2)),
                  ("1167.7", (n**4 - 3 * n**2 + 2) / (n**4 + 5 * n**3 - n), 1)]:
    lim(nom, e, l)
assert sp.simplify(n / (sp.sqrt(n**2 + n) + n) - (sp.sqrt(n**2 + n) - n)) == 0
# 1169 (récurrences, inégalités)
assert all(2**i >= i + 1 for i in range(200))
assert all(3**i >= 2 * i * i + 1 for i in range(1, 200))
assert all((4**i - 1) % 3 == 0 for i in range(200))
assert all(2**i >= i * i for i in range(4, 200)) and 2**3 < 9
assert sp.expand(6 * k**2 + 3 - (2 * (k + 1) ** 2 + 1) - 4 * k * (k - 1)) == 0
assert sp.expand(4 * (3 * m + 1) - 1 - 3 * (4 * m + 1)) == 0
assert sp.expand(2 * k**2 - (k + 1) ** 2 - ((k - 1) ** 2 - 2)) == 0
# 1168 (sommes)
for N in range(1, 60):
    assert sum(range(1, N + 1)) == N * (N + 1) // 2
    assert sum(i * i for i in range(1, N + 1)) == N * (N + 1) * (2 * N + 1) // 6
    assert sum(2**i for i in range(N + 1)) == 2 ** (N + 1) - 1
    assert sum(sp.Rational(1, i * (i + 1)) for i in range(1, N + 1)) == sp.Rational(N, N + 1)
assert sp.expand((k + 2) * (2 * k + 3) - (2 * k**2 + 7 * k + 6)) == 0
assert sp.simplify(k * (k + 1) * (2 * k + 1) / 6 + (k + 1) ** 2 - (k + 1) * (k + 2) * (2 * k + 3) / 6) == 0
assert sp.simplify(k / (k + 1) + 1 / ((k + 1) * (k + 2)) - (k + 1) / (k + 2)) == 0
# 1164
lim("1164.1", 2 * 3**n, oo)
lim("1164.2", 5 * sp.Rational(1, 2) ** n, 0)
lim("1164.3", 4 * sp.Rational(1, 3) ** n, 0)
assert [(-2) ** i for i in range(7)] == [1, -2, 4, -8, 16, -32, 64]
# 1165
for nom, e, l in [("1165.1 haut", 1 / n, 0), ("1165.2 bas", (n**2 - 1) / (n**2 + 1), 1),
                  ("1165.4 bas", (3 * n - 2) / (n + 5), 3), ("1165.4 haut", (3 * n + 2) / (n + 5), 3),
                  ("1165.5 bas", (n**3 - 1) / (n**3 - 2), 1), ("1165.5 haut", (n**3 + 1) / (n**3 - 2), 1),
                  ("1165.6 bas", (n - 1) / n**2, 0), ("1165.6 haut", (n + 1) / n**2, 0),
                  ("1165.7 bas", (5 * n**2 - 4) / (5 * n**2 + 2), 1)]:
    lim(nom, e, l)
for i in range(1, 3000):
    s, c, e = math.sin(i), math.cos(i), (-1) ** i
    assert -1 / i <= s / i <= 1 / i
    assert (i * i - 1) / (i * i + 1) <= (i * i + c) / (i * i + 1) <= 1
    assert (3 * i - 2) / (i + 5) <= (3 * i + 2 * s) / (i + 5) <= (3 * i + 2) / (i + 5)
    if i >= 2:
        assert (i**3 - 1) / (i**3 - 2) <= (i**3 + c) / (i**3 - 2) <= (i**3 + 1) / (i**3 - 2)
    assert (i - 1) / i**2 <= (e + i) / i**2 <= (i + 1) / i**2
    assert (5 * i * i - 4) / (5 * i * i + 2) <= (5 * i * i - 1 + 3 * s) / (5 * i * i + 2) <= 1 + 1e-15
# 1166
for nom, e, l in [("1166.1 bas", (n - sp.sqrt(n)) / (n + 1), 1), ("1166.1 haut", (n + sp.sqrt(n)) / (n + 1), 1),
                  ("1166.2 bas", (2 * n**2 - n) / (2 * n**2 - n + 1), 1),
                  ("1166.2 haut", (2 * n**2 + n) / (2 * n**2 - n + 1), 1),
                  ("1166.3 haut", 2 / n, 0), ("1166.4 bas", (n**4 - n**2) / (n**4 + 3 * n), 1),
                  ("1166.4 haut", (n**4 + n**2) / (n**4 + 3 * n), 1),
                  ("1166.5 bas", (4 * n - 3) / (4 * n + 3), 1), ("1166.5 haut", (4 * n + 1) / (4 * n + 3), 1),
                  ("1166.6 bas", (n**2 - n - 1) / (n**2 + 2), 1), ("1166.6 haut", (n**2 - n + 1) / (n**2 + 2), 1)]:
    lim(nom, e, l)
assert all(2 * i * i - i + 1 > 0 for i in range(0, 1000))
assert sp.expand(n * (2 * n - 1) + 1 - (2 * n**2 - n + 1)) == 0
# 1170 (problème)
uu = [1.0]
for _ in range(60):
    uu.append(math.sqrt(uu[-1] + 2))
assert all(0 <= uu[i] <= 2 and uu[i] <= uu[i + 1] for i in range(59)) and abs(uu[-1] - 2) < 1e-12
assert sp.factor(x**2 - x - 2) == (x - 2) * (x + 1)
assert sp.solve(sp.Eq(x**2, x + 2), x) == [2]  # x > 0
assert [round(t, 3) for t in uu[1:4]] == [1.732, 1.932, 1.983]

# ---------------------------------------------------------------- finition 2026-11-02
# 1170 Q4 : algorithme de seuil, seuil(0.001) = 6, valeurs du tableau
def seuil(e):
    rang, t = 0, 1.0
    while 2 - t >= e:
        rang, t = rang + 1, math.sqrt(t + 2)
    return rang
assert seuil(0.001) == 6
tableau = {1: (1.73205, 0.2679), 2: (1.93185, 0.0681), 3: (1.98289, 0.0171), 4: (1.99572, 0.0043),
           5: (1.99893, 0.00107), 6: (1.99973, 0.00027)}
for i, (val, ecart) in tableau.items():
    assert abs(uu[i] - val) < 5e-6 and abs((2 - uu[i]) - ecart) < 5e-5 * max(1, ecart * 100), (i, uu[i])
assert 2 - uu[5] >= 0.001 > 2 - uu[6]
assert all(0.2 < (2 - uu[i + 1]) / (2 - uu[i]) < 0.27 for i in range(0, 6))  # « divisé environ par 4 »
# figures des corrigés
lim("1162 s_n", 5 + 2 / n, 5)
assert all(5 + 2 / i > 5 for i in range(1, 21))
lim("1163 Q4", 2 - 5 / n**2, 2)
assert 2 - 5 / 1 == -3 and all(2 - 5 / i**2 < 2 for i in range(1, 16))
assert [round(math.sqrt(i * i + i) - i, 2) for i in (1, 20)] == [0.41, 0.49]
assert all(math.sqrt(i * i + i) - i < 0.5 for i in range(1, 200))
assert 2 * sum(range(1, 6)) == 5 * 6 == 30 and sum(range(1, 6)) == 15
assert [2**i >= i * i for i in range(0, 7)] == [True, True, True, False, True, True, True]
assert all(2**i >= i * i for i in range(4, 60))
for i in range(1, 41):  # 1166 Q1 : alternance entre les deux gendarmes
    t = (i + (-1) ** i * math.sqrt(i)) / (i + 1)
    bas, haut = (i - math.sqrt(i)) / (i + 1), (i + math.sqrt(i)) / (i + 1)
    assert abs(t - (haut if i % 2 == 0 else bas)) < 1e-12
egal("1166 écart des gendarmes", sp.simplify((n + sp.sqrt(n)) / (n + 1) - (n - sp.sqrt(n)) / (n + 1)), 2 * sp.sqrt(n) / (n + 1))
lim("1166 écart -> 0", 2 * sp.sqrt(n) / (n + 1), 0)
for i in range(1, 31):  # 1171 B1
    assert (2 * i - 1) / (i + 1) <= (2 * i + math.sin(i)) / (i + 1) <= (2 * i + 1) / (i + 1) < 2
lim("1171 B1 bas", (2 * n - 1) / (n + 1), 2)
lim("1171 B1 haut", (2 * n + 1) / (n + 1), 2)

print("TOUT EST JUSTE" if not erreurs else "\n".join(erreurs))
