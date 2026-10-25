"""Vérification des résultats numériques du chapitre 6 (décroissance radioactive) et du défi D06.

Lancer : python -I -X utf8 verifications/chapitre_06.py
"""
from math import exp, log, log2
from pathlib import Path
import random
import numpy as np

DONNEES = Path(__file__).resolve().parent.parent / 'figures' / 'donnees'
ECHECS = []
NA = 6.02e23
AN = 3.156e7


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def conservation(nom, pere, produits):
    """pere et produits : (A, Z) ; vérifie la conservation du nombre de nucléons et du nombre de charge."""
    a = sum(p[0] for p in produits)
    z = sum(p[1] for p in produits)
    ok = (a, z) == pere
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} {pere} -> {produits}")
    if not ok:
        ECHECS.append(nom)


ALPHA, BM, BP, GAMMA = (4, 2), (0, -1), (0, 1), (0, 0)
# Équations publiées (cours, exercices 1 à 3, 6, 9, 11 à 15, défi)
conservation("cours radon 222 alpha", (222, 86), [(218, 84), ALPHA])
conservation("cours carbone 14 bêta moins", (14, 6), [(14, 7), BM])
conservation("cours fluor 18 bêta plus", (18, 9), [(18, 8), BP])
conservation("ex2 cobalt 60", (60, 27), [(60, 28), BM])
conservation("ex2 américium 241", (241, 95), [(237, 93), ALPHA])
conservation("ex2 tritium", (3, 1), [(3, 2), BM])
conservation("ex3 césium 137", (137, 55), [(137, 56), BM])
conservation("ex3 carbone 11", (11, 6), [(11, 5), BP])
conservation("ex3 thorium 232", (232, 90), [(228, 88), ALPHA])
conservation("ex3 technétium 99m", (99, 43), [(99, 43), GAMMA])
conservation("ex11 iode 131", (131, 53), [(131, 54), BM])
conservation("ex13 uranium 238 -> plomb 206", (238, 92), [(206, 82)] + [ALPHA] * 8 + [BM] * 6)
conservation("ex15 plutonium 238", (238, 94), [(234, 92), ALPHA])
conservation("D06 molybdène 99", (99, 42), [(99, 43), BM])
# Données de la simulation de l'essentiel
d = np.loadtxt(DONNEES / '06-simulation.dat', skiprows=1)
verifie("essentiel simulation : écart relatif maximal à la loi (k <= 10)", float(np.max(np.abs(d[:11, 1] / d[:11, 2] - 1))), 0, 0.05)
# Exemple du cours : charbon de bois à 0,058 Bq/g
verifie("cours 0,23/4 (Bq/g)", 0.23 / 4, 0.058, 0.0006)
# Exercice 4 : iode 131
verifie("ex4 lambda (j-1)", log(2) / 8.0, 0.087, 0.0005)
verifie("ex4 A(24 j) (MBq)", 400 / 2 ** 3, 50, 1e-9)
verifie("ex4 courbe : A(24 j) avec 8,02 j (MBq)", 400 * 2 ** (-24 / 8.02), 50, 0.5)
# Exercice 5 : technétium 99m
for dt, p in ((6, 300), (12, 150), (24, 37.5)):
    verifie(f"ex5 A après {dt} h (MBq)", 600 * 2 ** (-dt / 6.0), p, 1e-9)
verifie("ex5 fraction après 48 h (%)", 100 / 2 ** 8, 0.4, 0.01)
# Exercice 6 : césium 137
lam6 = log(2) / 30.0
verifie("ex6 lambda (an-1)", lam6, 2.31e-2, 0.005e-2)
verifie("ex6 pourcentage restant en 100 ans", 100 * exp(-lam6 * 100), 9.9, 0.05)
verifie("ex6 durée pour diviser par 100 (an)", log(100) / lam6, 2.0e2, 1)
# Exercice 7 : américium 241
lam7 = log(2) / (432.6 * AN)
verifie("ex7 lambda (s-1)", lam7, 5.08e-11, 0.005e-11)
verifie("ex7 N", 3.7e4 / lam7, 7.3e14, 0.05e14)
verifie("ex7 m (g)", 3.7e4 / lam7 / NA * 241, 2.9e-7, 0.05e-7)
verifie("ex7 A(10 ans) (kBq)", 37 * exp(-log(2) * 10 / 432.6), 36.4, 0.05)
verifie("ex7 baisse relative en 10 ans (%)", 100 * (1 - exp(-log(2) * 10 / 432.6)), 1.6, 0.05)
# Exercice 8 : carbone 14
verifie("ex8 rapport A/A0", 0.060 / 0.23, 0.26, 0.005)
verifie("ex8 âge (ans)", 5700 / log(2) * log(0.23 / 0.060), 1.1e4, 0.05e4)
verifie("ex8 50 000 ans en demi-vies", 50000 / 5700, 8.8, 0.05)
verifie("ex8 facteur de division en 50 000 ans (> 400)", 2 ** (50000 / 5700), 437, 1)
# Exercice 10 : simulation (sorties publiées)


def essai(graine, n0, p=0.05):
    random.seed(graine)
    n = n0
    noyaux = [n]
    while n > n0 / 2:
        n = n - sum(1 for _ in range(n) if random.random() < p)
        noyaux.append(n)
    return len(noyaux) - 1, n


sorties = [essai(g, 500) for g in (1, 3, 6)] + [essai(g, 50000) for g in (1, 3, 6)]
print('   ex10 sorties :', sorties)
if sorties != [(13, 243), (15, 246), (12, 244), (14, 24438), (14, 24384), (14, 24486)]:
    ECHECS.append('ex10 sorties du programme')
verifie("ex10 demi-vie du modèle (s)", log(2) / -log(0.95), 13.5, 0.05)
# Exercice 9 : radon
lam9 = log(2) / (3.82 * 86400)
verifie("ex9 lambda (s-1)", lam9, 2.10e-6, 0.005e-6)
verifie("ex9 N par m3", 300 / lam9, 1.4e8, 0.05e8)
verifie("ex9 log2(10)", log(10) / log(2), 3.32, 0.005)
verifie("ex9 durée pour diviser par 10 (j)", log(10) / log(2) * 3.82, 13, 0.5)
# Exercice 11 : iode 131
verifie("ex11 A après 8,02 j (MBq)", 550 / 2, 275, 1e-9)
verifie("ex11 A après 30 j (MBq)", 550 * 2 ** (-30 / 8.02), 41, 0.5)
# Exercice 12 : fluor 18
verifie("ex12 activité au départ (MBq)", 250 * exp(log(2) * 150 / 109.7), 645, 0.5)
e12 = 9.11e-31 * (3.00e8) ** 2
verifie("ex12 énergie d'un photon (J)", e12, 8.20e-14, 0.005e-14)
verifie("ex12 énergie d'un photon (eV)", e12 / 1.602e-19, 5.1e5, 0.05e5)
verifie("ex12 nombre de demi-vies en 24 h", 24 * 60 / 109.7, 13.1, 0.05)
verifie("ex12 fraction restante après 24 h", 2 ** (-24 * 60 / 109.7), 1e-4, 0.15e-4)
# Exercice 13 : uranium-plomb
verifie("ex13 âge (ans)", 4.468e9 / log(2) * log(1.979), 4.40e9, 0.005e9)
# Exercice 14 : radioprotection
verifie("ex14 débit de dose à 50 cm (mSv/h)", 1.4 / 25, 0.056, 1e-9)
verifie("ex14 nombre de couches de demi-atténuation", 2.0 / 0.30, 6.7, 0.05)
verifie("ex14 facteur d'atténuation", 2 ** (2.0 / 0.30), 1.0e2, 3)
verifie("ex14 durée pour 1 mSv sans écran (min)", 60 / 1.4, 43, 0.5)
verifie("ex14 durée pour 1 mSv avec écran (h)", 2 ** (2.0 / 0.30) / 1.4, 72, 1)
verifie("ex14 activité après 24 h (MBq)", 740 / 2 ** 4, 46, 0.5)
# Exercice 15 : plutonium 238
lam15 = log(2) / (87.74 * AN)
n15 = 1.0 / 238 * NA
a15 = lam15 * n15
p15 = a15 * 5.59e6 * 1.602e-19
verifie("ex15 N pour 1,0 g", n15, 2.53e21, 0.005e21)
verifie("ex15 lambda (s-1)", lam15, 2.50e-10, 0.005e-10)
verifie("ex15 activité de 1,0 g (Bq)", a15, 6.3e11, 0.05e11)
verifie("ex15 puissance de 1,0 g (W)", p15, 0.57, 0.005)
verifie("ex15 puissance de la source (W)", p15 * 3500, 2.0e3, 0.05e3)
verifie("ex15 rendement (%)", 110 / (p15 * 3500) * 100, 5.5, 0.05)
verifie("ex15 part restante après 14 ans", 2 ** (-14 / 87.74), 0.90, 0.005)
# Défi D06 : générateur de technétium
l1, l2 = log(2) / 66.0, log(2) / 6.01
verifie("D06 lambda1 (h-1)", l1, 0.01050, 0.000005)
verifie("D06 lambda2 (h-1)", l2, 0.1153, 0.00005)
tm = log(l2 / l1) / (l2 - l1)
verifie("D06 t_m (h)", tm, 23, 0.5)
verifie("D06 rapport limite A2/A1", l2 / (l2 - l1), 1.10, 0.005)
verifie("D06 demi-vie du technétium onze fois plus courte", 66.0 / 6.01, 11, 0.05)
k = l1 / (l2 - l1)
a1 = l1 * exp(-l1 * tm)
a2 = l2 * k * (exp(-l1 * tm) - exp(-l2 * tm))
verifie("D06 A2 = A1 à t_m (écart relatif)", abs(a2 / a1 - 1), 0, 1e-9)
verifie("D06 figure : A2(t_m) en % de A1(0)", 100 * a2 / l1, 78.66, 0.01)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 6 et du défi D06 sont vérifiées.")
