# -*- coding: utf-8 -*-
"""Vérification de tous les résultats numériques de la notion « Loi binomiale ».

    python verif_loi_binomiale.py

Calcul exact (fractions) recoupé avec scipy.stats.binom. Chaque ligne compare
la valeur exacte à l'arrondi écrit dans cours_99.txt, fiche_41.txt et
exercices.txt ; le script échoue si un arrondi publié est faux.
"""
from fractions import Fraction as Fr
from math import comb, log, sqrt

from scipy.stats import binom

ERREURS = []


def pk(n, p, k):
    return comb(n, k) * p ** k * (1 - p) ** (n - k)


def F(n, p, k):
    return sum(pk(n, p, i) for i in range(0, k + 1))


def verifie(nom, exact, publie, dec=None):
    """Compare l'arrondi publié (chaîne avec virgule) à la valeur exacte."""
    if dec is None:
        dec = len(publie.split(",")[1]) if "," in publie else 0
    v = float(exact)
    ok = abs(round(v, dec) - float(publie.replace(",", "."))) < 10 ** (-dec - 3)
    print(f"{'OK ' if ok else 'ERR'} {nom:<34} exact={v:.6f}  publié={publie}")
    if not ok:
        ERREURS.append(nom)


def check(nom, n, p, k, mode, *publies):
    ex = {"eq": lambda: pk(n, p, k), "le": lambda: F(n, p, k), "ge": lambda: 1 - F(n, p, k - 1)}[mode]()
    sc = {"eq": binom.pmf(k, n, float(p)), "le": binom.cdf(k, n, float(p)), "ge": binom.sf(k - 1, n, float(p))}[mode]
    assert abs(float(ex) - sc) < 1e-12, nom
    for s in publies:
        verifie(nom, ex, s)
    return ex


# ------------------------------------------------------------------ cours et fiche
print("=== COURS : QCM B(10 ; 0,25) ===")
p = Fr(1, 4)
assert comb(10, 5) == 252
check("P(X=5)", 10, p, 5, "eq", "0,058")
verifie("V(X)", 10 * p * (1 - p), "1,875")
verifie("sigma(X)", sqrt(1.875), "1,37")
check("P(X<=4)", 10, p, 4, "le", "0,922")
check("P(X<=5)", 10, p, 5, "le", "0,980")
check("P(X>=5)", 10, p, 5, "ge", "0,078")
k = 0
while F(10, p, k) < Fr(95, 100):
    k += 1
assert k == 5
verifie("ln(0,05)/ln(0,75)", log(0.05) / log(0.75), "10,41")
assert 1 - 0.75 ** 10 < 0.95 <= 1 - 0.75 ** 11
verifie("1-0,75^10", 1 - 0.75 ** 10, "0,944")
verifie("1-0,75^11", 1 - 0.75 ** 11, "0,958")
# arbre (cas général) : 3 chemins à 2 succès
assert sum(1 for c in range(8) if bin(c).count("1") == 2) == 3 == comb(3, 2)


# programme Python du cours, exécuté tel quel
def proba(n, p, k):
    # P(X = k) pour B(n ; p)
    c = comb(n, k)
    q = 1 - p
    return c * p**k * q**(n-k)


def cumul(n, p, k):
    # P(X <= k)
    s = 0
    for i in range(k + 1):
        s = s + proba(n, p, i)
    return s


def seuil(n, p, alpha):
    # plus petit k tel que
    # P(X <= k) >= 1 - alpha
    k = 0
    s = proba(n, p, 0)
    while s < 1 - alpha:
        k = k + 1
        s = s + proba(n, p, k)
    return k


assert abs(cumul(10, 0.25, 4) - 0.921873) < 1e-6


assert seuil(10, 0.25, 0.05) == 5
print("OK  seuil(10, 0.25, 0.05) = 5 (programme du cours)")
# figures : B(20 ; p) maximum et espérances
for pp, e in [(0.2, 4), (0.5, 10), (0.8, 16)]:
    assert 20 * pp == e

# ------------------------------------------------------------------ exercices
print("\n=== 1111 cartes B(5 ; 0,6) ===")
p = Fr(3, 5)
assert comb(5, 3) == 10 and comb(5, 2) == 10
for k, s in [(0, "0,01024"), (1, "0,0768"), (2, "0,2304"), (3, "0,3456"), (4, "0,2592"), (5, "0,07776")]:
    check(f"P(X={k})", 5, p, k, "eq", s)
assert sum(pk(5, p, k) for k in range(6)) == 1
check("P(X<=2)", 5, p, 2, "le", "0,31744", "0,317")
check("P(X<=3)", 5, p, 3, "le", "0,66304")
check("P(X>=4)", 5, p, 4, "ge", "0,33696", "0,337")
verifie("sigma", sqrt(1.2), "1,095")

print("\n=== 1120 logiciels B(14 ; 0,6) ===")
p = Fr(3, 5)
assert comb(14, 9) == 2002 == comb(14, 5)
verifie("0,6^9", p ** 9, "0,010078")
verifie("0,6^9 x 0,4^5", p ** 9 * (1 - p) ** 5, "0,00010320")
check("P(X=9)", 14, p, 9, "eq", "0,2066", "0,207")
check("P(X<=6)", 14, p, 6, "le", "0,1501")
check("P(X>=7)", 14, p, 7, "ge", "0,8499", "0,850")
verifie("V", 14 * p * (1 - p), "3,36")
verifie("sigma", sqrt(3.36), "1,833")

print("\n=== 1117 pois B(16 ; 0,5) ===")
p = Fr(1, 2)
assert comb(16, 9) == 11440 and 2 ** 16 == 65536 and Fr(11440, 65536) == Fr(715, 4096)
check("P(X=9)", 16, p, 9, "eq", "0,1746", "0,175")
assert [comb(16, k) for k in range(11, 17)] == [4368, 1820, 560, 120, 16, 1]
assert sum(comb(16, k) for k in range(11, 17)) == 6885
check("P(X>=11)", 16, p, 11, "ge", "0,1051", "0,105")
check("P(X<=10)", 16, p, 10, "le", "0,8949")
assert [comb(16, k) for k in range(6, 11)] == [8008, 11440, 12870, 11440, 8008]
verifie("P(6<=X<=10)", Fr(51766, 65536), "0,790")
assert F(16, p, 10) - F(16, p, 5) == Fr(51766, 65536)

print("\n=== 1118 clientèle B(20 ; 0,82) ===")
p = Fr(82, 100)
assert comb(20, 16) == 4845 == comb(20, 4) and comb(20, 18) == 190
verifie("0,82^16", p ** 16, "0,0418")
verifie("0,18^4", (1 - p) ** 4, "0,00104976")
check("P(X=16)", 20, p, 16, "eq", "0,2125", "0,213")
check("P(X=18)", 20, p, 18, "eq", "0,1730")
check("P(X=19)", 20, p, 19, "eq", "0,0829")
check("P(X=20)", 20, p, 20, "eq", "0,0189")
check("P(X>=18)", 20, p, 18, "ge", "0,2748", "0,275")
verifie("V", 20 * p * (1 - p), "2,952")
verifie("sigma", sqrt(2.952), "1,718")
verifie("CA moyen", 200 * 20 * p, "3280")

print("\n=== 1115 traitement B(12 ; 0,75) ===")
p = Fr(3, 4)
assert comb(12, 10) == 66
verifie("0,75^10", p ** 10, "0,0563")
check("P(X=10)", 12, p, 10, "eq", "0,2323", "0,232")
check("P(X<=7)", 12, p, 7, "le", "0,1576")
check("P(X>=8)", 12, p, 8, "ge", "0,8424", "0,842")
verifie("coût par guéri", Fr(12 * 150, 9), "200")

print("\n=== 1113 sondage B(25 ; 0,35) ===")
p = Fr(35, 100)
assert comb(25, 8) == 1081575
check("P(X<=9)", 25, p, 9, "le", "0,6303")
check("P(X>=10)", 25, p, 10, "ge", "0,3697", "0,370")
check("P(X=8)", 25, p, 8, "eq", "0,1607", "0,161")
verifie("E", 25 * p, "8,75")
assert Fr(40, 100) * 25 == 10

print("\n=== 1112 qualité B(15 ; 0,1) — ancienne version, réécrite le 2026-11-02 (voir FINITION) ===")
p = Fr(1, 10)
assert comb(15, 2) == 105
verifie("0,9^13", Fr(9, 10) ** 13, "0,2542")
verifie("0,9^14", Fr(9, 10) ** 14, "0,2288")
verifie("0,9^15", Fr(9, 10) ** 15, "0,2059")
check("P(X=2)", 15, p, 2, "eq", "0,2669", "0,267")
check("P(X=0)", 15, p, 0, "eq", "0,2059")
check("P(X=1)", 15, p, 1, "eq", "0,3432")
assert F(15, p, 1) == Fr(24, 10) * Fr(9, 10) ** 14
check("P(X<=1)", 15, p, 1, "le", "0,5490", "0,549")
check("P(X<=2)", 15, p, 2, "le", "0,8159")
check("P(X>=3)", 15, p, 3, "ge", "0,1841", "0,184")
verifie("sigma", sqrt(1.35), "1,162")

print("\n=== 1114 résistance B(30 ; 0,08) ===")
p = Fr(8, 100)
assert comb(30, 2) == 435 and comb(30, 3) == 4060 and comb(30, 4) == 27405 and comb(30, 5) == 142506
check("P(X=0)", 30, p, 0, "eq", "0,0820")
check("P(X=1)", 30, p, 1, "eq", "0,2138")
check("P(X=2)", 30, p, 2, "eq", "0,2696")
check("P(X<=2)", 30, p, 2, "le", "0,5654", "0,565")
check("P(X=3)", 30, p, 3, "eq", "0,2188")
check("P(X=4)", 30, p, 4, "eq", "0,1284")
check("P(X=5)", 30, p, 5, "eq", "0,0581")
check("P(X<=5)", 30, p, 5, "le", "0,9707")
verifie("P(3<=X<=5)", F(30, p, 5) - F(30, p, 2), "0,4053")
verifie("P(3<=X<=5)", F(30, p, 5) - F(30, p, 2), "0,405")
verifie("V", 30 * p * (1 - p), "2,208")
verifie("sigma", sqrt(2.208), "1,486")

print("\n=== 1119 recyclage B(35 ; 0,25) ===")
p = Fr(1, 4)
check("P(X=10)", 35, p, 10, "eq", "0,1318", "0,132")
check("P(X<=12)", 35, p, 12, "le", "0,9244")
check("P(X<=5)", 35, p, 5, "le", "0,0976")
verifie("P(6<=X<=12)", F(35, p, 12) - F(35, p, 5), "0,8268")
verifie("P(6<=X<=12)", F(35, p, 12) - F(35, p, 5), "0,827")
verifie("V", 35 * p * (1 - p), "6,5625")
verifie("sigma", sqrt(6.5625), "2,562")
verifie("E après", 35 * Fr(30, 100), "10,5")
verifie("bénéfice", (35 * Fr(30, 100) - 35 * p) * 200 - 5000, "-4650")
verifie("seuil de rentabilité (ménages)", Fr(5000) / (Fr(5, 100) * 200), "500")

print("\n=== 1116 alcoolémie B(40 ; 0,15) ===")
p = Fr(15, 100)
check("P(X=6)", 40, p, 6, "eq", "0,1742", "0,174")
check("P(X<=4)", 40, p, 4, "le", "0,2633", "0,263")
verifie("V", 40 * p * (1 - p), "5,1")
verifie("sigma", sqrt(5.1), "2,258")

print("\n=== 1121 téléphone B(30 ; 0,15) ===")
p = Fr(15, 100)
assert comb(30, 5) == 142506
check("P(X=5)", 30, p, 5, "eq", "0,1861", "0,186")
verifie("0,85^30", (1 - p) ** 30, "0,0076")
check("P(X>=1)", 30, p, 1, "ge", "0,9924", "0,992")
verifie("V", 30 * p * (1 - p), "3,825")
verifie("sigma", sqrt(3.825), "1,956")
verifie("ln(0,05)/ln(0,85)", log(0.05) / log(0.85), "18,4")
assert 1 - 0.85 ** 18 < 0.95 < 1 - 0.85 ** 19
verifie("1-0,85^18", 1 - 0.85 ** 18, "0,9464")
verifie("1-0,85^19", 1 - 0.85 ** 19, "0,9544")

print("\n=== FINITION 2026-11-02 ===")
import re
from pathlib import Path

ICI = Path(__file__).resolve().parent

print("--- 1112 réécrit : contrôle qualité B(50 ; 0,06) ---")
p = Fr(6, 100)
assert comb(50, 3) == 19600 and comb(50, 2) == 1225
check("P(X=3)", 50, p, 3, "eq", "0,2311")
check("P(X=0)", 50, p, 0, "eq", "0,0453")
check("P(X=1)", 50, p, 1, "eq", "0,1447")
check("P(X=2)", 50, p, 2, "eq", "0,2262")
check("P(X<=2)", 50, p, 2, "le", "0,4162")
verifie("E", 50 * p, "3")
verifie("V", 50 * p * (1 - p), "2,82")
verifie("sigma", sqrt(2.82), "1,679")
for k, v in [(3, "0,6473"), (4, "0,8206"), (5, "0,9224"), (6, "0,9711"), (7, "0,9906")]:
    check(f"tableau P(X<={k})", 50, p, k, "le", v)
assert F(50, p, 5) < Fr(95, 100) <= F(50, p, 6), "seuil k = 6"
check("P(X>=7) arrêt à tort", 50, p, 7, "ge", "0,0289", "0,029")
verifie("risque en %", 100 * (1 - F(50, p, 6)), "2,9")

print("--- code Python du cours EXÉCUTÉ (seuil) ---")
cours = (ICI / "cours_99.txt").read_text(encoding="utf-8")
code = re.search(r"```python\n(.*?)```", cours, re.S).group(1)
env = {}
exec(code, env)
assert env["seuil"](10, 0.25, 0.05) == 5, "seuil QCM"
assert env["seuil"](50, 0.06, 0.05) == 6, "seuil 1112"
print("OK seuil(10, 0.25, 0.05) = 5 et seuil(50, 0.06, 0.05) = 6")

print("--- étiquettes des nouvelles figures (corrigés) ---")
check("cours P(X<=4) B(10;0,25)", 10, Fr(1, 4), 4, "le", "0,922")
check("cours P(X>=5) B(10;0,25)", 10, Fr(1, 4), 5, "ge", "0,078")
check("1111 P(X<=2)", 5, Fr(6, 10), 2, "le", "0,317")
check("1111 P(X>=4)", 5, Fr(6, 10), 4, "ge", "0,337")
check("1120 P(X>=7)", 14, Fr(6, 10), 7, "ge", "0,850")
check("1118 P(X>=18)", 20, Fr(82, 100), 18, "ge", "0,275")
check("1115 P(X>=8)", 12, Fr(75, 100), 8, "ge", "0,842")
check("1113 P(X>=10)", 25, Fr(35, 100), 10, "ge", "0,370")
check("1116 P(X<=4)", 40, Fr(15, 100), 4, "le", "0,263")
check("1112 P(X<=6)", 50, Fr(6, 100), 6, "le", "0,971")
verifie("1121 1-0,85^19", 1 - Fr(85, 100) ** 19, "0,954")
# barres « invisibles » au-delà de la fenêtre des diagrammes
assert 1 - F(40, Fr(15, 100), 16) < 0.001, "1116 : masse au-delà de 16"
assert 1 - F(50, Fr(6, 100), 14) < 0.0001, "1112 : masse au-delà de 14"
assert 1 - F(35, Fr(1, 4), 20) < 0.0001, "1119 : masse au-delà de 20"

print("--- nouveau-1 : trois lancers francs B(3 ; 0,7) ---")
p = Fr(7, 10)
for k, v in [(0, "0,027"), (1, "0,189"), (2, "0,441"), (3, "0,343")]:
    check(f"P(X={k})", 3, p, k, "eq", v)
assert sum(pk(3, p, k) for k in range(4)) == 1
verifie("un chemin à 2 réussites", p ** 2 * (1 - p), "0,147")
verifie("3 x 0,147", 3 * p ** 2 * (1 - p), "0,441")
verifie("0,7 x 0,7 x 0,3", Fr(7, 10) * Fr(7, 10) * Fr(3, 10), "0,147")
check("P(X>=2)", 3, p, 2, "ge", "0,784")
verifie("E = np", 3 * p, "2,1")
verifie("E par la définition", sum(k * pk(3, p, k) for k in range(4)), "2,1")
assert comb(3, 2) == 3

print()
if ERREURS:
    print("ERREURS :", ERREURS)
    raise SystemExit(1)
print("Tous les résultats publiés sont justes.")
