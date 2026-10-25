"""Vérification des résultats numériques du chapitre 26 (circuit RC et capteurs capacitifs) et du défi D26.

Lancer : python -I -X utf8 verifications/chapitre_26.py
"""
import io
from contextlib import redirect_stdout
from math import exp, log

ECHECS = []
EPS0 = 8.85e-12
e = 1.60e-19


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def sortie_de(fonction):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    return tampon.getvalue().strip()


# L'essentiel
verifie("cours condensateur plan de 1 m² à 1 mm (nF)", 1e9 * EPS0 * 1.0 / 1e-3, 8.85, 0.005)
verifie("cours temps caractéristique (s)", 10e3 * 100e-6, 1.0, 1e-9)
verifie("cours fraction à tau (%)", 100 * (1 - exp(-1)), 63, 0.5)
verifie("cours fraction à 5 tau (%)", 100 * (1 - exp(-5)), 99.3, 0.05)
for t, u in ((0, 0), (1, 3.16), (2, 4.32), (3, 4.75), (5, 4.97)):
    verifie(f"figure charge : u à {t} tau (V)", 5 * (1 - exp(-t)), u, 0.005)


def programme_cours():
    E, R, C = 5.0, 10e3, 100e-6          # V, ohm, F
    tau, dt = R * C, 0.001               # s
    u, t = 0.0, 0.0
    while u < 0.95 * E:              # 95 % de E
        u = u + (E - u) / tau * dt
        t = t + dt
    print(round(t, 3), round(-tau * log(0.05), 3))


s = sortie_de(programme_cours)
print('   cours programme :', s)
if s != '2.995 2.996':
    ECHECS.append('cours programme')
# Exercice 1
verifie("ex1 charge (C)", 2.0 * 30, 60, 0)
verifie("ex1 nombre d'électrons", 60 / e, 3.75e20, 0.005e20)
verifie("ex1 intensité pour q = 0,5 t² mC à 4 s (mA)", 1.0 * 4, 4.0, 1e-9)
# Exercice 3
verifie("ex3 charge sous 12 V (mC)", 1000 * 470e-6 * 12, 5.64, 0.005)
verifie("ex3 charge du petit condensateur (nC)", 1e9 * 4.7e-9 * 12, 56, 0.5)
verifie("ex3 électrons sur l'armature", 470e-6 * 12 / e, 3.5e16, 0.05e16)
# Exercice 4
verifie("ex4 tension à tau (V)", 6.0 * (1 - exp(-1)), 3.8, 0.05)
verifie("ex4 capacité (µF)", 1e6 * 2.2e-3 / 1.0e3, 2.2, 1e-9)
verifie("ex4 durée de charge à 99 % (ms)", 5 * 2.2, 11, 1e-9)
# Exercice 5
verifie("ex5 charge du flash (C)", 150e-6 * 300, 0.045, 1e-12)
verifie("ex5 intensité moyenne (A)", 150e-6 * 300 / 1e-3, 45, 1e-9)
verifie("ex5 énergie stockée (J)", 0.5 * 150e-6 * 300 ** 2, 6.75, 1e-9)
# Exercice 6
verifie("ex6 tension à 2 tau (part de E, %)", 100 * exp(-2), 13.5, 0.05)
verifie("ex6 tension à 2 tau pour E = 9 V (V)", 9 * exp(-2), 1.22, 0.005)
verifie("ex6 date pour E/2 (en tau)", log(2), 0.69, 0.005)
# Exercice 7
verifie("ex7 rapport t/tau", log(12 / 2), 1.79, 0.005)
verifie("ex7 temps caractéristique (s)", 60 / log(6), 33.5, 0.05)
verifie("ex7 résistance (kOhm)", 60 / log(6) / 1000e-6 / 1000, 33.5, 0.05)
# Exercice 8
verifie("ex8 durée de charge exacte à 99 % (s)", -1.0 * log(0.01), 4.6, 0.05)
u8, t8, vals = 0.0, 0.0, []
while u8 < 0.95 * 5.0:
    u8 = u8 + (5.0 - u8) / 1.0 * 0.5
    t8 = t8 + 0.5
    vals.append(round(u8, 2))
verifie("ex8 durée avec dt = 0,5 s (s)", t8, 2.5, 1e-9)
print('   ex8 valeurs avec dt = 0,5 s :', vals)
if vals != [2.5, 3.75, 4.38, 4.69, 4.84]:
    ECHECS.append('ex8 valeurs dt = 0,5')
# Exercice 9
C9 = EPS0 * 0.04 / 2e-3
verifie("ex9 capacité dans l'air (pF)", 1e12 * C9, 177, 0.5)
verifie("ex9 avec un plastique (pF)", 3 * 1e12 * C9, 531, 0.5)
verifie("ex9 distance divisée par 2 (pF)", 2 * 1e12 * C9, 354, 0.5)
verifie("ex9 surface pour 1 µF à 2 mm dans l'air (m²)", 1e-6 * 2e-3 / EPS0, 226, 0.5)
# Exercice 10
verifie("ex10 charge (C)", 150e-6 * 2000, 0.30, 1e-12)
verifie("ex10 énergie (J)", 0.5 * 150e-6 * 2000 ** 2, 300, 1e-9)
verifie("ex10 temps caractéristique (ms)", 1000 * 50 * 150e-6, 7.5, 1e-9)
verifie("ex10 intensité initiale (A)", 2000 / 50, 40, 1e-9)
verifie("ex10 tension après 10 ms (V)", 2000 * exp(-10 / 7.5), 527, 0.5)
# Exercice 11
verifie("ex11 temps caractéristique (ms)", 1000 * 1e3 * 100e-9, 0.1, 1e-12)
verifie("ex11 fréquence maximale (kHz)", 1 / (10 * 1e-4) / 1000, 1.0, 1e-9)
verifie("ex11 tension atteinte à 5 kHz (V)", 5 * (1 - exp(-0.1e-3 / 1e-4)), 3.2, 0.05)
# Exercice 12
verifie("ex12 temps caractéristique sans doigt (µs)", 1e6 * 1e6 * 10e-12, 10, 1e-9)
verifie("ex12 temps caractéristique avec le doigt (µs)", 1e6 * 1e6 * 11e-12, 11, 1e-9)
verifie("ex12 durée pour atteindre la moitié (µs)", 10 * log(2), 6.9, 0.05)
verifie("ex12 durée avec le doigt (µs)", 11 * log(2), 7.6, 0.05)
verifie("ex12 écart (µs)", 11 * log(2) - 10 * log(2), 0.69, 0.005)
# Exercice 13
x13 = 2.0e-9 * 9.81 / 1.0
verifie("ex13 déplacement de la masse (nm)", 1e9 * x13, 19.6, 0.05)
verifie("ex13 variation relative de capacité (%)", 100 * x13 / 2.0e-6, 0.98, 0.005)
C13 = EPS0 * 1.0e-7 / 2.0e-6
verifie("ex13 capacité au repos (fF)", 1e15 * C13, 443, 0.5)
verifie("ex13 variation de capacité (fF)", 1e15 * C13 * x13 / 2.0e-6, 4.3, 0.05)
# Exercice 14
verifie("ex14 niveau relatif", (78 - 50) / (120 - 50), 0.40, 1e-9)
verifie("ex14 hauteur (m)", 0.40 * 2.5, 1.0, 1e-9)
verifie("ex14 temps pour une cuve pleine aux 3/4 (µs)", 50 + 0.75 * 70, 102.5, 1e-9)
# Exercice 15
tau15 = 60 / 70
verifie("ex15 période (s)", tau15, 0.857, 0.0005)
verifie("ex15 résistance (kOhm)", tau15 / 1.0e-6 / 1000, 857, 0.5)
verifie("ex15 tension de déclenchement (V)", 2.8 * exp(-1), 1.03, 0.005)
verifie("ex15 rythme pour 90 battements (s)", 60 / 90, 0.667, 0.0005)
verifie("ex15 résistance pour 90 battements (kOhm)", 60 / 90 / 1e-6 / 1000, 667, 0.5)
# Défi D26


def programme_d26():
    E, C = 10.0, 1.0e-3                       # V, F
    for R in [10, 100, 1000]:                 # ohms
        tau = R * C
        dt = tau / 1000
        W, t = 0.0, 0.0
        while t < 10 * tau:
            i = E / R * exp(-t / tau)
            W = W + R * i**2 * dt
            t = t + dt
        print(R, round(W, 3), 0.5 * C * E**2)


s = sortie_de(programme_d26).splitlines()
print('   D26 sorties :', s)
if s != ['10 0.05 0.05', '100 0.05 0.05', '1000 0.05 0.05']:
    ECHECS.append('D26 sorties')
verifie("D26 charge finale (C)", 1.0e-3 * 10, 0.010, 1e-12)
verifie("D26 énergie fournie (J)", 10 * 0.010, 0.10, 1e-12)
verifie("D26 énergie stockée (J)", 0.5 * 1.0e-3 * 10 ** 2, 0.05, 1e-12)
verifie("D26 rendement (%)", 100 * 0.05 / 0.10, 50, 1e-9)
verifie("D26 puissance relative à 10 tau", exp(-20), 2e-9, 0.1e-9)
verifie("D26 pertes par étape (J)", 0.5 * 1.0e-3 * 5 ** 2, 0.0125, 1e-12)
verifie("D26 pertes en deux étapes (J)", 2 * 0.5 * 1.0e-3 * 5 ** 2, 0.025, 1e-12)
verifie("D26 rendement en deux étapes (%)", 100 * 0.05 / (0.05 + 0.025), 66.7, 0.05)
verifie("D26 pertes en N = 10 étapes (J)", 10 * 0.5 * 1.0e-3 * 1 ** 2, 0.005, 1e-12)
verifie("D26 rendement en 10 étapes (%)", 100 * 0.05 / 0.055, 90.9, 0.05)
for t, p in ((0, 10.0), (1, 1.35), (2, 0.18)):
    verifie(f"figure D26 : puissance Joule à {t} tau pour R = 10 (W)", 10 ** 2 / 10 * exp(-2 * t), p, 0.005)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 26 et du défi D26 sont vérifiées.")
