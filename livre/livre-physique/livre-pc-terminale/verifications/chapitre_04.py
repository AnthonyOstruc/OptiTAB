"""Vérification des résultats numériques du chapitre 4 (cinétique chimique) et du défi D04.

Lancer : python -I -X utf8 verifications/chapitre_04.py
"""
from math import exp, log, log2
from pathlib import Path
import numpy as np

DONNEES = Path(__file__).resolve().parent.parent / 'figures' / 'donnees'
ECHECS = []


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def lire(nom):
    return np.loadtxt(DONNEES / f'{nom}.dat', skiprows=1)


# L'essentiel : données du programme (ordre 1, [R]0 = 10 mmol/L, t1/2 = 25 min)
k_ess = log(2) / 25
c_ess = [10.0, 8.71, 7.58, 6.60, 5.74, 5.00, 4.35, 3.79, 3.30]
for i, c in enumerate(c_ess):
    verifie(f"essentiel [R] à {5 * i} min", 10 * exp(-k_ess * 5 * i), c, 0.005)
v_ess = [-(c_ess[i + 1] - c_ess[i - 1]) / 10 for i in range(1, 8)]
verifie("essentiel k = v/[R] moyen (min-1)", np.mean([v / c for v, c in zip(v_ess, c_ess[1:8])]), 0.028, 0.0005)
verifie("essentiel 7 t1/2 : fraction restante < 1 %", 2 ** -7, 0.0078, 0.0001)

# Exercice 2 : [I2]f = 4,0 mmol/L, t1/2 = 15 min
verifie("ex2 [I2] à t1/2 (mmol/L)", 4.0 * (1 - 2 ** (-15 / 15)), 2.0, 1e-9)
verifie("ex2 [I2] à 30 min (mmol/L)", 4.0 * (1 - 2 ** (-30 / 15)), 3.0, 1e-9)
# Exercice 3 : [R]0 = 60 mmol/L, k = 1/30 min-1
k3 = 1 / 30
verifie("ex3 t1/2 (min)", log(2) / k3, 21, 0.3)
verifie("ex3 T0 coupe l'axe des temps (min)", 1 / k3, 30, 1e-9)
verifie("ex3 T1/2 coupe l'axe des temps (min)", log(2) / k3 + 1 / k3, 51, 0.3)
verifie("ex3 v(0) (mmol/L/min)", k3 * 60, 2.0, 1e-9)
verifie("ex3 v(t1/2) (mmol/L/min)", k3 * 30, 1.0, 1e-9)
verifie("ex3 quotient v/[R] (min-1)", 2.0 / 60, 0.033, 0.0005)
# Exercice 6 : absorbance du diiode
d6 = lire('04-iodure-absorbance')
verifie("ex6 n(H2O2)0 (mol)", 1.0e-2 * 10.0e-3, 1.0e-4, 1e-12)
verifie("ex6 n(I-)0 (mol)", 0.10 * 40.0e-3, 4.0e-3, 1e-12)
verifie("ex6 [I2]f (mol/L)", 1.0e-4 / 50.0e-3, 2.0e-3, 1e-12)
verifie("ex6 A finale", 250 * 2.0e-3, 0.500, 1e-12)
publie6 = [0, 0.25, 0.49, 0.69, 0.85, 1.00, 1.30, 1.51, 1.64, 1.76, 1.87, 1.94]
for (t, a), p in zip(d6, publie6):
    verifie(f"ex6 [I2] à {t:g} min (mmol/L)", 4 * a, p, 0.0051)
verifie("ex6 A à 10 min (t1/2)", d6[d6[:, 0] == 10][0, 1], 0.250, 0.0015)
verifie("ex6 tangente à l'origine : date où elle atteint 2,0 mmol/L", 10 / log(2), 14.4, 0.05)
verifie("ex6 v(0) (mol/L/min)", 2.0e-3 / 14.4, 1.4e-4, 0.05e-4)
# Exercice 8 : titrage des prélèvements
d8 = lire('04-peroxyde-titrage')
c8 = 2.5 * 0.0200 * d8[:, 1] / 10.0
for (t, _), c, p in zip(d8, c8, [0.0800, 0.0600, 0.0450, 0.0335, 0.0255, 0.0140, 0.0080, 0.0025]):
    verifie(f"ex8 [H2O2] à {t:g} min (mol/L)", c, p, 1e-9)
verifie("ex8 t1/2 par interpolation (min)", np.interp(0.040, c8[::-1], d8[::-1, 0]), 12, 0.6)
verifie("ex8 quotient 5/0", c8[1] / c8[0], 0.75, 0.005)
verifie("ex8 quotient 10/5", c8[2] / c8[1], 0.75, 0.005)
verifie("ex8 quotient 15/10", c8[3] / c8[2], 0.74, 0.005)
verifie("ex8 k = -ln(0,75)/5 (min-1)", -log(0.75) / 5, 0.058, 0.0005)
verifie("ex8 ln2/k (min)", log(2) / (-log(0.75) / 5), 12, 0.1)
# Exercice 9 : caféine
d9 = lire('04-cafeine')
for (t, c), p in zip(d9, [1.275, 1.144, 0.867, 0.593, 0.315, -0.261]):
    verifie(f"ex9 ln C à {t:g} h", log(c), p, 0.0005)
p9 = np.polyfit(d9[:, 0], np.log(d9[:, 1]), 1)
verifie("ex9 ordonnée à l'origine", p9[1], 1.42, 0.005)
verifie("ex9 coefficient directeur (h-1)", p9[0], -0.140, 0.0005)
verifie("ex9 k (h-1)", -p9[0], 0.14, 0.005)
verifie("ex9 t1/2 (h)", log(2) / -p9[0], 5.0, 0.05)
verifie("ex9 C(6 h)/C(1 h)", d9[3, 1] / d9[0, 1], 0.5, 0.01)
# Exercice 10 : autocatalyse, c(t) = 2,0/(1 + exp((t - 6)/1,2)) mmol/L
verifie("ex10 vitesse maximale (mmol/L/min)", 2.0 / (4 * 1.2), 0.42, 0.005)
verifie("ex10 tangente en 6 min : intersections (min)", 6 - 1.0 * 2.4, 3.6, 1e-9)
# Exercice 11 : programme Python (cristal violet)
d11 = lire('04-violet')
t11, c11 = [float(x) for x in d11[:, 0]], [float(x) for x in d11[:, 1]]
V = [-(c11[i + 1] - c11[i - 1]) / (t11[i + 1] - t11[i - 1]) for i in range(1, len(t11) - 1)]
q = [V[i] / c11[i + 1] for i in range(len(V))]
sortie1 = [round(v, 3) for v in V]
sortie2 = [round(x, 4) for x in q]
print('   ex11 sortie :', sortie1, sortie2)
if sortie1 != [0.46, 0.422, 0.357, 0.315, 0.308, 0.28, 0.254, 0.226, 0.201] or \
        sortie2 != [0.0254, 0.0259, 0.0243, 0.0234, 0.0252, 0.0255, 0.0255, 0.0252, 0.0248]:
    ECHECS.append('ex11 sortie du programme')
verifie("ex11 k moyen (min-1)", np.mean(q), 0.025, 0.0005)
verifie("ex11 t1/2 (min)", log(2) / np.mean(q), 28, 0.5)
# Exercice 12 : décoloration par l'eau de Javel
d12 = lire('04-e133-javel')
verifie("ex12 A1 à 30 min", d12[d12[:, 0] == 30][0, 1], 0.400, 1e-9)
verifie("ex12 A1 à 60 min", d12[d12[:, 0] == 60][0, 1], 0.200, 1e-9)
verifie("ex12 A2 à 15 min", d12[d12[:, 0] == 15][0, 2], 0.400, 1e-9)
verifie("ex12 k1 = ln2/30 (min-1)", log(2) / 30, 2.3e-2, 0.05e-2)
verifie("ex12 t1/2 prévu pour [ClO-] = 0,020 (min)", 30 * 0.040 / 0.020, 60, 1e-9)
# Exercice 13 : catalase
n13 = 48e-3 / 24.0
verifie("ex13 n(O2) (mol)", n13, 2.0e-3, 1e-12)
verifie("ex13 n(H2O2)0 (mol)", 2 * n13, 4.0e-3, 1e-12)
verifie("ex13 [H2O2]0 (mol/L)", 2 * n13 / 20.0e-3, 0.20, 1e-9)
# Exercice 14 : lentilles de contact
n14 = log2(3.0 / 0.01)
verifie("ex14 nombre de demi-vies", n14, 8.2, 0.05)
verifie("ex14 durée (h)", n14 * 30 / 60, 4.1, 0.05)
verifie("ex14 teneur après 6 h (%)", 3.0 / 2 ** 12, 7.3e-4, 0.05e-4)
verifie("ex14 durée avec un disque usé (h)", n14 * 45 / 60, 6.2, 0.05)
verifie("ex14 teneur après 6 h avec un disque usé (%)", 3.0 / 2 ** 8, 0.012, 0.0005)
# Exercice 15 : chlorure de tertiobutyle
d15 = lire('04-tertiobutyle')
t15, s15 = d15[1:, 0], d15[1:, 1]
a15, b15 = np.polyfit(t15, np.log(1 - s15 / 1.62), 1)
print('   ex15 sortie :', round(a15, 6), round(b15, 3))
if (round(a15, 6), round(b15, 3)) != (-0.002328, 0.006):
    ECHECS.append('ex15 sortie du programme')
verifie("ex15 k (s-1)", -a15, 2.33e-3, 0.005e-3)
verifie("ex15 t1/2 (s)", log(2) / -a15, 300, 5)
verifie("ex15 sigma à 300 s ~ sigma_inf/2", d15[d15[:, 0] == 300][0, 1], 0.81, 0.005)
verifie("ex15 k' à 35 °C (s-1)", log(2) / 120, 5.8e-3, 0.05e-3)
verifie("ex15 rapport des constantes", 300 / 120, 2.5, 1e-9)

# Défi D04 : saponification (ordre 2)
dd = lire('04-saponification')
td, cd = dd[:, 0], dd[:, 1] / 1000
for t, c, p in zip(td, cd, [-4.605, -4.730, -4.890, -5.113, -5.292, -5.447, -5.696]):
    verifie(f"D04 ln c à {t:g} s", log(c), p, 0.0005)
pentes = np.diff(np.log(cd)) / np.diff(td) * 1e4
for i, p in enumerate([-10.4, -8.9, -7.4, -6.0, -5.1, -4.1]):
    verifie(f"D04 coefficient directeur du segment {i + 1} (1e-4 s-1)", pentes[i], p, 0.05)
for t, c, p in zip(td, cd, [100.0, 113.3, 133.0, 166.1, 198.8, 232.0, 297.6]):
    verifie(f"D04 1/c à {t:g} s", 1 / c, p, 0.05)
k_d, b_d = np.polyfit(td, 1 / cd, 1)
print('   D04 sortie :', round(k_d, 4), round(b_d, 1))
if (round(k_d, 4), round(b_d, 1)) != (0.1098, 100.1):
    ECHECS.append('D04 sortie du programme')
verifie("D04 k (L/mol/s)", k_d, 0.11, 0.002)
verifie("D04 t1/2 = 1/(k c0) (s)", 1 / (0.11 * 1.00e-2), 9.1e2, 5)
verifie("D04 t1/2 pour c0 = 5,0e-3 (s)", 1 / (0.11 * 5.0e-3), 1.8e3, 20)
verifie("D04 c0/4 atteint à 3 t1/2 (s)", 3 / (0.11 * 1.00e-2), 2.7e3, 30)
verifie("D04 1/c à 2727 s (L/mol)", 100 + 0.11 * 2727, 400, 0.5)
verifie("D04 c(1800 s) si ordre 1 (mmol/L)", 10.0 / 4, 2.50, 1e-9)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 4 et du défi D04 sont vérifiées.")
