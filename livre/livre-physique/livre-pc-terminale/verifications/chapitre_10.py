"""Vérification des résultats numériques du chapitre 10 (électrolyse et stockage) et du défi D10.

Lancer : python -I -X utf8 verifications/chapitre_10.py
"""
import io
from contextlib import redirect_stdout

ECHECS = []
F = 96500
NA = 6.02e23


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


# L'essentiel : exemple de cuivrage et programme
ne = 1.2 * 1800 / F
verifie("cours n(e-) (mol)", ne, 2.24e-2, 0.005e-2)
verifie("cours n(Cu) (mol)", ne / 2, 1.12e-2, 0.005e-2)
verifie("cours m(Cu) (g)", ne / 2 * 63.5, 0.71, 0.005)
tampon = io.StringIO()
with redirect_stdout(tampon):
    M = 63.5
    I = 1.2

    def masse(t):
        n_e = I * t / F
        return M * n_e / 2

    for t in (600, 1800, 3600):
        print(t, round(masse(t), 2))
sortie = tampon.getvalue().strip().splitlines()
print('   cours programme :', sortie)
if sortie != ['600 0.24', '1800 0.71', '3600 1.42']:
    ECHECS.append('cours programme de cuivrage')
# Exercice 3
verifie("ex3 Q (C)", 0.50 * 1200, 600, 1e-9)
verifie("ex3 n(e-) (mol)", 600 / F, 6.22e-3, 0.005e-3)
verifie("ex3 nombre d'électrons", 600 / F * NA, 3.74e21, 0.01e21)
# Exercice 4
ne4 = 0.60 * 2400 / F
verifie("ex4 n(e-) (mol)", ne4, 1.49e-2, 0.005e-2)
verifie("ex4 m(Cu) (g)", ne4 / 2 * 63.5, 0.47, 0.005)
v4 = ne4 / 2 * 63.5 / 8.96
verifie("ex4 volume (cm3)", v4, 5.3e-2, 0.05e-2)
verifie("ex4 épaisseur (µm)", v4 / 60 * 1e4, 8.8, 0.05)
# Exercice 6
ne6 = 0.25 * 900 / F
verifie("ex6 n(e-) (mol)", ne6, 2.33e-3, 0.005e-3)
verifie("ex6 V(H2) (mL)", ne6 / 2 * 24 * 1000, 28, 0.5)
verifie("ex6 V(O2) (mL)", ne6 / 4 * 24 * 1000, 14, 0.5)
# Exercice 7
n7 = 2.0 / 107.9
verifie("ex7 n(Ag) (mol)", n7, 1.85e-2, 0.005e-2)
verifie("ex7 Q (C)", n7 * F, 1.79e3, 0.005e3)
verifie("ex7 durée (s)", n7 * F / 0.50, 3.6e3, 0.03e3)
verifie("ex7 durée (min)", n7 * F / 0.50 / 60, 60, 0.5)
# Exercice 8
q8 = 250 * 86400
verifie("ex8 n(e-) (mol)", q8 / F, 224, 0.5)
verifie("ex8 m(Cu) (kg)", q8 / F / 2 * 63.5 / 1000, 7.1, 0.05)
verifie("ex8 énergie (kWh)", 0.30 * q8 / 3.6e6, 1.8, 0.05)
verifie("ex8 énergie par kg (kWh)", 0.30 * q8 / 3.6e6 / (q8 / F / 2 * 63.5 / 1000), 0.25, 0.005)
# Exercice 9
q9 = 60 * 3600
verifie("ex9 Q (C)", q9, 2.16e5, 1e-9)
verifie("ex9 n(e-) (mol)", q9 / F, 2.24, 0.005)
verifie("ex9 m(Pb) (g)", q9 / F / 2 * 207.2, 232, 0.5)
verifie("ex9 part d'un démarrage (%)", 100 * 300 / q9, 0.14, 0.005)
# Exercice 10 : programme et calcul direct
tampon = io.StringIO()
with redirect_stdout(tampon):
    I10 = 1500
    M_H2 = 2.0
    t, m = 0, 0
    while m < 1000:
        t = t + 3600
        m = M_H2 * I10 * t / (2 * F)
    print(t, round(t / 3600), round(m))
sortie = tampon.getvalue().strip()
print('   ex10 sortie :', sortie)
if sortie != '64800 18 1007':
    ECHECS.append('ex10 sortie du programme')
verifie("ex10 durée exacte (s)", 2 * F * 1000 / (2.0 * 1500), 6.43e4, 0.005e4)
verifie("ex10 durée exacte (h)", 2 * F * 1000 / (2.0 * 1500) / 3600, 17.9, 0.05)
verifie("ex10 volume à 1 bar (m3)", 500 * 24.8 / 1000, 12.4, 0.05)
# Exercice 11
m11 = 0.96 * 10e-6 * 1e6 * 7.14          # volume en cm3 x masse volumique
verifie("ex11 volume (cm3)", 0.96 * 10e-6 * 1e6, 9.6, 1e-9)
verifie("ex11 m(Zn) (g)", m11, 69, 0.6)
n11 = m11 / 65.4
verifie("ex11 n(Zn) (mol)", n11, 1.05, 0.005)
verifie("ex11 Q (C)", 2 * n11 * F, 2.02e5, 0.005e5)
verifie("ex11 durée (s)", 2 * n11 * F / 200, 1.0e3, 0.02e3)
verifie("ex11 durée (min)", 2 * n11 * F / 200 / 60, 17, 0.5)
# Exercice 12
verifie("ex12 énergie d'une cellule (Wh)", 3.7 * 5.0, 18.5, 1e-9)
verifie("ex12 nombre de cellules", 60000 / 18.5, 3.2e3, 0.05e3)
verifie("ex12 durée de charge (h)", 60 / 11, 5.5, 0.05)
n12 = 5.0 * 3600 / F
verifie("ex12 n(Li) (mol)", n12, 0.187, 0.0005)
verifie("ex12 m(Li), 1,29 arrondi à 1,3 (g)", n12 * 6.94, 1.3, 0.0056)
# Exercice 13
verifie("ex13 puissance (MW)", 160 * 2.0 * 25000 / 1e6, 8.0, 1e-9)
d13 = 25000 / (2 * F)
verifie("ex13 débit par cellule (mol/s)", d13, 0.130, 0.0005)
verifie("ex13 débit total (mol/s)", 160 * d13, 20.7, 0.05)
m13 = 160 * d13 * 86400 * 2.0 / 1e6      # tonnes
verifie("ex13 masse par jour (t)", m13, 3.6, 0.05)
verifie("ex13 énergie par jour (MWh)", 8.0 * 24, 192, 1e-9)
verifie("ex13 énergie par kg (kWh)", 192000 / (m13 * 1000), 54, 0.5)
verifie("ex13 rendement (%)", 100 * 33.3 / 53.6, 62, 0.5)
# Exercice 14
ne14 = 350000 * 86400 / F
verifie("ex14 n(e-) par jour (mol)", ne14, 3.13e5, 0.005e5)
verifie("ex14 m(Al) par jour (t)", ne14 / 3 * 27.0 / 1e6, 2.8, 0.05)
verifie("ex14 m(C) par jour (kg)", ne14 / 4 * 12.0 / 1000, 940, 5)
verifie("ex14 m(CO2) par jour (t)", ne14 / 4 * 44.0 / 1e6, 3.4, 0.05)
e14 = 4.2 * 350000 * 86400
verifie("ex14 énergie par jour (MWh)", e14 / 3.6e9, 35.3, 0.1)
verifie("ex14 énergie par tonne (MWh)", e14 / 3.6e9 / (ne14 / 3 * 27.0 / 1e6), 12.5, 0.1)
# Exercice 15
verifie("ex15 restitution batteries (kWh)", 720 * 0.90, 648, 1e-9)
verifie("ex15 masse de batteries (t)", 720000 / 150 / 1000, 4.8, 1e-9)
verifie("ex15 rendement global (%)", 100 * 0.70 * 0.50, 35, 1e-9)
verifie("ex15 restitution H2 (kWh)", 720 * 0.35, 252, 1e-9)
m15 = 720 * 0.70 / 33.3
verifie("ex15 masse de H2 (kg)", m15, 15.1, 0.05)
n15 = m15 * 1000 / 2.0
verifie("ex15 n(H2) (mol)", n15, 7.6e3, 0.05e3)
verifie("ex15 volume à 300 bar (m3)", n15 * 8.314 * 298 / 3.0e7, 0.62, 0.005)

# Défi D10
tampon = io.StringIO()
with redirect_stdout(tampon):
    U0 = 1.23
    for U in (1.3, 1.6, 2.0, 2.4):
        w = 2 * F * U / 1000
        print(U, round(w), round(U0 / U, 2))
sortie = tampon.getvalue().strip().splitlines()
print('   D10 sorties :', sortie)
if sortie != ['1.3 251 0.95', '1.6 309 0.77', '2.0 386 0.61', '2.4 463 0.51']:
    ECHECS.append('D10 sorties du programme')
w0 = 2 * F * 1.23
verifie("D10 W0 (kJ)", w0 / 1000, 237, 0.5)
verifie("D10 W0 par kg (kWh)", 500 * w0 / 3.6e6, 33.0, 0.05)
verifie("D10 tension thermoneutre (V)", 242000 / (2 * F), 1.25, 0.005)
verifie("D10 chaleur à 2,0 V (kJ/mol)", 2 * F * 2.0 / 1000 - 242, 144, 0.5)
verifie("D10 manque à 1,23 V (kJ/mol)", 242 - w0 / 1000, 5, 0.5)
verifie("D10 figure : rendement à 2,0 V", 1.23 / 2.0, 0.615, 1e-9)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 10 et du défi D10 sont vérifiées.")
