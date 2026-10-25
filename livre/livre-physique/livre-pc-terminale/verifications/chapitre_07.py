"""Vérification des résultats numériques du chapitre 7 (équilibre chimique et sens d'évolution) et du défi D07.

Lancer : python -I -X utf8 verifications/chapitre_07.py
"""
from math import sqrt
from pathlib import Path
import numpy as np

DONNEES = Path(__file__).resolve().parent.parent / 'figures' / 'donnees'
ECHECS = []


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def racine(f, a, b):
    """Dichotomie : f(a) et f(b) de signes contraires."""
    for _ in range(200):
        m = (a + b) / 2
        if f(a) * f(m) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2


# L'essentiel
h = 10 ** -3.4
verifie("essentiel [H3O+] pour pH 3,4", h, 4.0e-4, 0.05e-4)
verifie("essentiel tau", h / 1.0e-2, 0.040, 0.0005)
verifie("essentiel K", (4.0e-4) ** 2 / 9.6e-3, 1.7e-5, 0.05e-5)
x = racine(lambda x: x ** 2 / (1e-2 - x) - 1.7e-5, 0, 0.999e-2)
verifie("essentiel programme : x", x, 4.04e-4, 0.005e-4)
verifie("essentiel programme : tau", x / 1e-2, 0.040, 0.0005)
# Fe3+ + Ag = Fe2+ + Ag+ : K = 1/3,2 (constante tabulée 3,2 pour Ag+ + Fe2+ = Ag + Fe3+),
# cohérente avec E°(Fe3+/Fe2+) = 0,771 V et E°(Ag+/Ag) = 0,7996 V
verifie("constante Fe3+ + Ag : 1/3,2", 1 / 3.2, 0.31, 0.005)
verifie("constante Fe3+ + Ag à partir des E° (entre 0,30 et 0,34)", 10 ** ((0.771 - 0.7996) / 0.05916), 0.32, 0.02)
verifie("essentiel exemple : Qr,i", 0.050 * 0.20 / 0.10, 0.10, 1e-9)
d = np.loadtxt(DONNEES / '07-equilibre.dat', skiprows=1)
verifie("essentiel figure : x à 200 min proche de 2/3", d[-1, 1], 0.6667, 0.01)
verifie("essentiel figure : K = k1/k-1", 0.020 / 0.005, 4.0, 1e-9)
# Exercice 1
verifie("ex1 tau B", 10 ** -3.4 * 1.0 / 1.0e-2, 0.040, 0.0005)
verifie("ex1 tau C", 0.33 / 0.50, 0.66, 1e-9)
# Exercice 2
verifie("ex2 Qr E", 4.0e-4 / (2.0e-3) ** 2, 1.0e2, 1e-9)
# Exercice 3
verifie("ex3 Qr A", 0.10 * 1.0e-4 / 0.10, 1.0e-4, 1e-12)
verifie("ex3 Qr B", 1.0e-3 / (1.0e-3) ** 2, 1.0e3, 1e-9)
verifie("ex3 Qr D", (1.0e-3) ** 2, 1.0e-6, 1e-15)
# Exercice 6 : acide méthanoïque
for c, ph, tau in ((1e-2, 2.90, 12.6), (1e-3, 3.46, 34.7)):
    h = 10 ** -ph
    verifie(f"ex6 tau pour c = {c:g} (%)", 100 * h / c, tau, 0.05)
    verifie(f"ex6 Qr,éq pour c = {c:g}", h * h / (c - h), 1.8e-4, 0.05e-4)
    hk = racine(lambda y: y * y / (c - y) - 1.8e-4, 0, c * 0.999)
    verifie(f"ex6 pH calculé avec K = 1,8e-4 pour c = {c:g}", -np.log10(hk), ph, 0.005)
# Exercice 7 : conductimétrie
lam = (35.0 + 4.09) * 1e-3          # S.m2/mol
publies = ((1.0e-2, 160, 4.09e-4, 1.75e-5, 4.1), (5.0e-3, 112, 2.87e-4, 1.74e-5, 5.7),
           (2.0e-3, 69.6, 1.78e-4, 1.74e-5, 8.9), (1.0e-3, 48.3, 1.24e-4, 1.74e-5, 12.4))
for c, s, hp, qp, tp in publies:
    hm = s * 1e-4 / lam / 1000      # mol/L
    verifie(f"ex7 [H3O+] pour c = {c:g}", hm, hp, 0.005e-4 if hp > 1e-4 else 0.005e-4)
    verifie(f"ex7 Qr,éq pour c = {c:g}", hm * hm / (c - hm), qp, 0.006e-5)
    verifie(f"ex7 tau pour c = {c:g} (%)", 100 * hm / c, tp, 0.05)
    hk = racine(lambda y: y * y / (c - y) - 1.74e-5, 0, c * 0.999)
    verifie(f"ex7 sigma attendu pour c = {c:g} (uS/cm)", hk * 1000 * lam * 1e4, s, 0.5)
# Exercice 8
verifie("ex8 Qr,i A", 0.010 * 0.010 / 0.10, 1.0e-3, 1e-12)
verifie("ex8 Qr,i B", 0.10 * 0.50 / 0.010, 5.0, 1e-9)
xa = racine(lambda x: (0.010 + x) ** 2 / (0.10 - x) - 0.31, 0, 0.0999)
verifie("ex8 x (mol/L)", xa, 0.076, 0.0005)
verifie("ex8 [Fe3+]éq (mol/L)", 0.10 - xa, 2.4e-2, 0.05e-2)
verifie("ex8 tau (%)", 100 * xa / 0.10, 76, 0.5)
verifie("ex8 tau supérieur à 75 % (énoncé)", 100 * xa / 0.10, 76, 1)
verifie("ex8 coefficient de x : 0,02 + 0,31", 0.02 + 0.31, 0.33, 1e-9)
verifie("ex8 terme constant : 0,031 - 1e-4", 0.31 * 0.10 - 1e-4, 0.0309, 1e-9)
# Exercice 9 : ions triiodure
for c2, xp, tp in ((1e-2, 8.664e-4, 0.866), (1e-1, 9.860e-4, 0.986)):
    xi = racine(lambda x: x / ((1e-3 - x) * (c2 - x)) - 710, 0, 0.999e-3)
    verifie(f"ex9 x pour [I-]0 = {c2:g}", xi, xp, 0.0005e-4)
    verifie(f"ex9 tau pour [I-]0 = {c2:g}", xi / 1e-3, tp, 0.0005)
# Exercice 10 : estérification
verifie("ex10 x (1 ; 1)", racine(lambda x: x * x / (1 - x) ** 2 - 4, 0, 0.999), 0.67, 0.005)
x2 = (12 - sqrt(48)) / 6
verifie("ex10 x (1 ; 2)", x2, 0.85, 0.005)
verifie("ex10 vérification de 3x²-12x+8 = 0", 3 * x2 ** 2 - 12 * x2 + 8, 0, 1e-12)
# Exercice 11 : cuivre et zinc
cu = 0.10 / 1.9e37
verifie("ex11 [Cu2+]éq (mol/L)", cu, 5e-39, 0.5e-39)
verifie("ex11 nombre d'ions Cu2+", cu * 0.100 * 6.02e23, 3e-16, 0.5e-16)
nzn = 0.50 / 65.4
verifie("ex11 n(Zn) (mol)", nzn, 7.6e-3, 0.05e-3)
verifie("ex11 [Zn2+] final (mol/L)", nzn / 0.100, 0.076, 0.0005)
verifie("ex11 [Cu2+] final (mol/L)", (0.010 - nzn) / 0.100, 0.024, 0.0005)
verifie("ex11 Qr final", nzn / (0.010 - nzn), 3.2, 0.05)
# Exercice 12 : spectrophotométrie
for fe, scn, a, xp, qp in ((1e-3, 1e-3, 0.394, 8.4e-5, 100), (2e-3, 1e-3, 0.732, 1.56e-4, 100), (1e-3, 3e-3, 1.02, 2.17e-4, 100)):
    xm = a / 4.7e3
    verifie(f"ex12 [FeSCN2+] pour A = {a}", xm, xp, 0.005e-4 if xp > 1e-4 else 0.05e-5)
    verifie(f"ex12 Qr,éq pour A = {a}", xm / ((fe - xm) * (scn - xm)), qp, 1)
    xk = racine(lambda x: x / ((fe - x) * (scn - x)) - 100, 0, min(fe, scn) * 0.999)
    verifie(f"ex12 A attendue avec K = 100 pour A = {a}", 4.7e3 * xk, a, 0.0015 if a < 1 else 0.005)
verifie("ex12 [Fe3+]éq mélange 1", 1.0e-3 - 0.394 / 4.7e3, 9.2e-4, 0.05e-4)
verifie("ex12 tau mélange 1 (%)", 100 * 0.394 / 4.7e3 / 1e-3, 8, 0.5)
verifie("ex12 tau mélange 3 (%)", 100 * 1.02 / 4.7e3 / 1e-3, 22, 0.5)
# Tableau du corrigé 12 : x, [Fe3+]éq et [SCN-]éq en 1e-4 mol/L, puis Qr,éq
for fe, scn, a, xt, fet, scnt, qt in ((1e-3, 1e-3, 0.394, 0.838, 9.16, 9.16, 99.9),
                                      (2e-3, 1e-3, 0.732, 1.56, 18.4, 8.44, 100),
                                      (1e-3, 3e-3, 1.02, 2.17, 7.83, 27.8, 99.6)):
    xm = a / 4.7e3
    verifie(f"cor12 tableau x pour A = {a} (1e-4)", xm * 1e4, xt, 0.0005 if xt < 1 else 0.005)
    verifie(f"cor12 tableau [Fe3+]éq pour A = {a} (1e-4)", (fe - xm) * 1e4, fet, 0.005 if fet < 10 else 0.05)
    verifie(f"cor12 tableau [SCN-]éq pour A = {a} (1e-4)", (scn - xm) * 1e4, scnt, 0.005 if scnt < 10 else 0.05)
    verifie(f"cor12 tableau Qr,éq pour A = {a}", xm / ((fe - xm) * (scn - xm)), qt, 0.05 if qt < 100 else 0.5)
# Exercice 13 : chlorure d'argent
s = sqrt(1.8e-10)
verifie("ex13 s eau (mol/L)", s, 1.3e-5, 0.05e-5)
verifie("ex13 s eau (g/L)", s * 143.3, 1.9e-3, 0.05e-3)
verifie("ex13 racine de K2", sqrt(2.9e-3), 0.054, 0.0005)
s2 = racine(lambda y: y * y / (1 - 2 * y) ** 2 - 2.9e-3, 0, 0.4)
verifie("ex13 s ammoniac (mol/L)", s2, 0.049, 0.0005)
verifie("ex13 masse dissoute (g)", s2 * 143.3, 7.0, 0.05)
verifie("ex13 rapport des solubilités", s2 / s, 3600, 60)
# Exercice 14 : extraction
f1 = 1 / (1 + 50 * 20 / 100)
verifie("ex14 fraction restante, une extraction (%)", 100 * f1, 9.1, 0.05)
verifie("ex14 [I2]aq (mol/L)", 1e-3 * f1, 9.1e-5, 0.05e-5)
verifie("ex14 [I2]cyclo (mol/L)", (1e-3 * 0.100 * (1 - f1)) / 0.020, 4.5e-3, 0.05e-3)
verifie("ex14 fraction restante, deux extractions (%)", 100 * (1 / (1 + 50 * 10 / 100)) ** 2, 2.8, 0.05)
# Exercice 15 : mutarotation
k1, k2 = 0.016, 0.009
a, b = 1.0, 0.0
for _ in range(240):
    v1, v2 = k1 * a, k2 * b
    a, b = a + (v2 - v1), b + (v1 - v2)
print('   ex15 sortie :', round(a, 3), round(b, 3), round(b / a, 2))
if (round(a, 3), round(b, 3), round(b / a, 2)) != (0.361, 0.639, 1.77):
    ECHECS.append('ex15 sortie du programme')
verifie("ex15 K = k1/k-1", k1 / k2, 1.78, 0.005)
verifie("ex15 proportion de beta à l'équilibre", k1 / (k1 + k2), 0.64, 0.005)
# Défi D07
verifie("D07 K", 0.020 / 0.0050, 4.0, 1e-9)
verifie("D07 Qr,i", 1.5 * 1.5 / (0.5 * 0.5), 9.0, 1e-9)
y = racine(lambda y: (1.5 - y) ** 2 / (0.5 + y) ** 2 - 4, 0, 1.4)
verifie("D07 y (mol)", y, 1 / 6, 1e-6)
verifie("D07 nA éq (mol)", 0.5 + y, 0.667, 0.0005)
verifie("D07 nC éq (mol)", 1.5 - y, 1.333, 0.0005)
k1, k2, dt = 0.020, 0.005, 0.1
a = b = 0.50
c = dd = 1.50
for _ in range(1500):
    v = k1 * a * b - k2 * c * dd
    a, b, c, dd = a - v * dt, b - v * dt, c + v * dt, dd + v * dt
sortie = (round(a, 3), round(c, 3), round(c * dd / (a * b), 2))
print('   D07 sortie :', sortie)
if sortie != (0.666, 1.334, 4.01):
    ECHECS.append('D07 sortie du programme')

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 7 et du défi D07 sont vérifiées.")
