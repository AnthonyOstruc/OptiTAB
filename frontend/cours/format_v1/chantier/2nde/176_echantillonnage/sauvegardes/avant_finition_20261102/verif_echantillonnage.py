# -*- coding: utf-8 -*-
"""Vérification de la notion « Échantillonnage » (Seconde).

Rejoue les simulations des figures (graines fixes), exécute les programmes
Python du cours et des exercices, et vérifie chaque nombre cité.
Comparaisons en entiers ou en fractions (jamais d'égalité de flottants).
Lancer : python verif_echantillonnage.py
"""
import random
import re
import sys
from fractions import Fraction as F
from math import comb, isqrt
from pathlib import Path

ICI = Path(__file__).parent
sys.path.insert(0, str(ICI / "figures"))
import figures as FIG  # noqa: E402

ok = 0


def check(cond, msg):
    global ok
    if not cond:
        raise AssertionError(msg)
    ok += 1


def ecart(n):
    r = isqrt(n)
    return F(1, r) if r * r == n else None


# ---------------------------------------------------------------- figures
ks = FIG.serie(FIG.GRAINE_COURS, 100, 100, 0.5)
h = FIG.hors_bande(ks, 100, 0.5)
check(len(h) == 4, "cours : 4 points hors bande")
check(all(abs(k - 50) not in (10, 11) for k in ks), "cours : aucun point ambigu au bord")
ks2 = FIG.serie(FIG.GRAINE_N2, 50, 100, 0.4)
h2 = FIG.hors_bande(ks2, 100, 0.4)
check(sorted(ks2[i] for i in h2) == [28, 28, 54], "nouveau-2 : 0,28 ; 0,28 ; 0,54")
check(all(abs(k - 40) not in (9, 10, 11) for k in ks2), "nouveau-2 : lecture sans ambiguïté")
check(F(50 - 3, 50) == F(94, 100), "nouveau-2 : 47/50 = 0,94")
for g in FIG.GRAINES_STAB:
    fr = FIG.cumul(g, 1000, 0.5)
    check(all(0.2 < x < 0.8 for x in fr[9:]), "stabilisation : courbes dans le cadre")
    check(abs(fr[-1] - 0.5) < 0.03, "stabilisation : f(1000) proche de 0,5")

# ---------------------------------------------------------------- propriété 95 %
def proba_proche(n, p):
    """P(|X/n - p| <= 1/sqrt(n)), X ~ B(n, p), calcul exact en fractions."""
    p = F(p)
    r = isqrt(n)
    return sum(comb(n, k) * p**k * (1 - p)**(n - k)
               for k in range(n + 1) if abs(k - n * p) <= r)


for n, p in [(25, "0.5"), (100, "0.5"), (400, "0.5"), (400, "0.3"), (100, "0.4"), (100, "0.2"), (2500, "0.5")]:
    check(proba_proche(n, p) >= F(95, 100), f"au moins 95 % : n={n}, p={p}")

# ---------------------------------------------------------------- programmes Python
def freq(rng, n, p):
    k = 0
    for i in range(n):
        if rng.random() < p:
            k = k + 1
    return k / n


def proche(rng, N, n, p):
    e = 1 / n ** 0.5
    c = 0
    for j in range(N):
        f = freq(rng, n, p)
        if abs(f - p) <= e:
            c = c + 1
    return c / N


rng = random.Random(5)
six = [proche(rng, 1000, 100, 0.5) for _ in range(6)]
check([round(x * 1000) for x in six] == [973, 969, 966, 975, 959, 964], "cours : six appels de proche")
v400 = [round(proche(rng, 1000, 400, 0.3) * 1000) for _ in range(6)]
check({971, 963, 979} <= set(v400), "2010 Q5 : valeurs simulées")

# 2009 : exécution à la main, puis nb_six
tir = [F(x, 100) for x in (12, 77, 5, 31, 29, 90, 18, 33, 2, 60)]
k = sum(1 for t in tir if t < F(3, 10))
check(k == 5 and F(k, 10) == F(1, 2), "2009 Q2")
check(F(62, 100) * 50 == 31, "2009 Q3")
code_nb_six = (
    "from random import randint\n\n"
    "def nb_six(n):\n"
    "    k = 0\n"
    "    for i in range(n):\n"
    "        if randint(1, 6) == 6:\n"
    "            k = k + 1\n"
    "    return k\n")
espace = {}
exec(code_nb_six, espace)
random.seed(1)
r = espace["nb_six"](60000)
check(abs(r - 10000) < 500, "2009 Q5 : nb_six plausible")

# ---------------------------------------------------------------- calculs des textes
check(F(27, 50) == F(54, 100), "cours : 27/50")
check(F(200, 900) - F(1, 6) == F(1, 18) and F(1, 18) > F(1, 30), "cours : dé 900 lancers")
check(F(228, 400) == F(57, 100), "cours : sondage 0,57")
check(ecart(1600) == F(1, 40), "cours : 1/40")
# 2010
check(F(964, 1000) * 500 == 482, "2010 Q4")
# 2004
check(F(11, 20) == F(55, 100) and F(3, 50) == F(6, 100) and F(72, 200) == F(36, 100), "2004 Q1-3")
check(F(375, 1000) * 80 == 30 and F(18, 120) == F(3, 20) == F(15, 100), "2004 Q4-5")
# 2007
check(F(42, 100) - F(1, 10) == F(32, 100) and F(42, 100) + F(1, 10) == F(52, 100), "2007 Q1")
lo, hi = F(52, 100) - ecart(900), F(52, 100) + ecart(900)
check(F(486, 1000) <= lo < F(487, 1000) and F(553, 1000) < hi <= F(554, 1000), "2007 Q2 arrondis")
check(F(2, 25) - ecart(25) == F(-12, 100) and F(2, 25) + ecart(25) == F(28, 100), "2007 Q3")
check(F(256, 1600) == F(16, 100) and ecart(1600) == F(25, 1000), "2007 Q4")
check(F(2, 10) > F(185, 1000), "2007 Q5")
# 2006
def dans(p, n, f):
    e = ecart(n)
    return F(p) - e <= F(f) <= F(p) + e
check([dans("0.5", 400, "0.58"), dans("0.3", 100, "0.39"), dans("0.12", 2500, "0.15"),
       dans("0.65", 225, "0.60"), dans("0.8", 25, "0.55")] == [False, True, False, True, False], "2006")
check(F(583, 1000) <= F(65, 100) - F(1, 15) and F(65, 100) + F(1, 15) <= F(717, 1000), "2006 Q4 arrondis")
# 2005
check(abs(F(52, 400) - F(1, 10)) == F(3, 100) <= F(5, 100), "2005 Q1")
check(F(185, 900) - F(1, 6) == F(35, 900) > F(30, 900) == ecart(900), "2005 Q2")
check(abs(F(2, 10) - F(17, 100)) == F(3, 100) <= F(33, 1000), "2005 Q2 piège de l'arrondi")
check(abs(F(30, 100) - F(52, 100)) == F(22, 100) > F(1, 10), "2005 Q3")
check(F(1290, 2500) == F(516, 1000) and F(16, 1000) <= ecart(2500), "2005 Q4")
# 2008 : plus petit n tel que 1/sqrt(n) <= e  <=>  n * e^2 >= 1
def n_min(e):
    e = F(e)
    n = 1
    while n * e * e < 1:
        n += 1
    return n
check([n_min(x) for x in ("0.1", "0.05", "0.03", "0.02", "0.01")] == [100, 400, 1112, 2500, 10000], "2008")
check(F(10000, 400) == 25, "2008 Q6")
# 2011
check(F(16, 25) == F(64, 100) and F(236, 400) == F(59, 100), "2011 Q1")
check(F(14, 100) <= F(2, 10) and F(9, 100) > F(5, 100), "2011 Q3-4")
# nouveau-1 : données issues de la simulation (graine 7, p = 0,62)
rng = random.Random(7)
paliers, kk, res = [10, 50, 100, 500, 1000, 5000, 10000], 0, []
for i in range(1, 10001):
    if rng.random() < 0.62:
        kk += 1
    if i in paliers:
        res.append(kk)
check(res == [9, 37, 66, 321, 642, 3099, 6196], "nouveau-1 : données")
fr = [F(k, n) for k, n in zip(res, paliers)]
arr = [round(x * 1000) for x in fr]
check(arr == [900, 740, 660, 642, 642, 620, 620], "nouveau-1 : fréquences arrondies")
check(F(6196, 10000) - F(1, 100) == F(6096, 10000) and F(6196, 10000) + F(1, 100) == F(6296, 10000), "nouveau-1 Q4")
# nouveau-2 Q5
check(abs(F(55, 100) - F(2, 5)) == F(15, 100) > F(1, 10), "nouveau-2 Q5")

# ---------------------------------------------------------------- code : lignes <= 30 caractères
for fich in ("cours_216.txt", "fiche_146.txt", "exercices.txt"):
    texte = (ICI / fich).read_text(encoding="utf-8")
    for bloc in re.findall(r"```python\n(.*?)```", texte, re.S):
        for ligne in bloc.splitlines():
            check(len(ligne) <= 30, f"{fich} : ligne de code trop longue : {ligne!r}")

print(f"{ok} vérifications : tout est juste.")
