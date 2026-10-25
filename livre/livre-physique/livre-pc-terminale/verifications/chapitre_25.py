"""Vérification des résultats numériques du chapitre 25 (photons et effet photoélectrique) et du défi D25.

Lancer : python -I -X utf8 verifications/chapitre_25.py
"""
import io
from contextlib import redirect_stdout
from math import sqrt

ECHECS = []
h = 6.63e-34
c = 3.00e8
e = 1.60e-19
me = 9.11e-31


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


def E_eV(lam_nm):
    return h * c / (lam_nm * 1e-9) / e


# L'essentiel
verifie("cours photon de 500 nm (J)", h * c / 500e-9, 3.98e-19, 0.005e-19)
verifie("cours photon de 500 nm (eV)", E_eV(500), 2.49, 0.005)
verifie("cours photons par seconde d'un laser de 1 mW à 633 nm", 1e-3 / (h * c / 633e-9), 3.2e15, 0.05e15)
verifie("cours seuil du zinc (nm)", 1e9 * h * c / (4.3 * e), 289, 0.5)
verifie("cours fréquence seuil du sodium (Hz)", 2.28 * e / h, 5.5e14, 0.05e14)
verifie("cours longueur d'onde seuil du sodium (nm)", 1e9 * h * c / (2.28 * e), 545, 0.5)
verifie("cours longueur d'onde maximale pour le silicium (nm)", 1e9 * h * c / (1.12 * e), 1110, 5)
for nu, Ec in ((6.0e14, 0.21), (8.0e14, 1.04), (10.0e14, 1.86)):
    verifie(f"figure Ec(nu) sodium à {nu:.1e} Hz (eV)", h * nu / e - 2.28, Ec, 0.005)
for nu, Ec in ((12e14, 0.67), (14e14, 1.50)):
    verifie(f"figure Ec(nu) zinc à {nu:.1e} Hz (eV)", h * nu / e - 4.3, Ec, 0.005)


def programme_cours():
    U = [0, 1.0, 2.0, 3.0, 4.0, 4.5, 5.0, 5.5, 6.0]           # V
    I = [0.85, 0.85, 0.84, 0.83, 0.80, 0.76, 0.66, 0.42, 0]   # A
    P = [u * i for u, i in zip(U, I)]                          # W
    k = P.index(max(P))
    print(U[k], round(P[k], 2), round(100 * P[k] / (1000 * 0.025), 1))


s = sortie_de(programme_cours)
print('   cours programme :', s)
if s != '4.5 3.42 13.7':
    ECHECS.append('cours programme')
# Exercice 1
for lam, E in ((400, 3.11), (700, 1.78), (254, 4.89), (1000, 1.24)):
    verifie(f"ex1 énergie d'un photon de {lam} nm (eV)", E_eV(lam), E, 0.005)
verifie("ex1 longueur d'onde maximale pour casser C-C (nm)", 1e9 * h * c / (3.6 * e), 345, 0.5)
# Exercice 2
for metal, W, lam0 in (("Cs", 2.1, 592), ("Na", 2.28, 545), ("Zn", 4.3, 289), ("Cu", 4.7, 264)):
    verifie(f"ex2 seuil du {metal} (nm)", 1e9 * h * c / (W * e), lam0, 0.5)
# Exercice 3
Ec3 = E_eV(400) - 2.28
verifie("ex3 énergie du photon (eV)", E_eV(400), 3.11, 0.005)
verifie("ex3 énergie cinétique maximale (eV)", Ec3, 0.83, 0.005)
verifie("ex3 énergie cinétique maximale (J)", Ec3 * e, 1.32e-19, 0.005e-19)
verifie("ex3 vitesse maximale (m/s)", sqrt(2 * Ec3 * e / me), 5.4e5, 0.05e5)
verifie("ex3 énergie cinétique pour 600 nm", E_eV(600) - 2.28, -0.21, 0.005)
# Exercice 5
verifie("ex5 énergie d'un photon de 532 nm (J)", h * c / 532e-9, 3.74e-19, 0.005e-19)
verifie("ex5 photons par seconde du pointeur", 1.0e-3 / (h * c / 532e-9), 2.7e15, 0.05e15)
verifie("ex5 photons solaires par seconde sur 1 m²", 1000 / (h * c / 550e-9), 2.8e21, 0.05e21)
# Exercice 6
nus = [6.9e14, 7.4e14, 8.2e14, 9.6e14]
Us = [0.57, 0.78, 1.12, 1.69]
for nu, U in zip(nus, Us):
    verifie(f"ex6 modèle à {nu:.1e} Hz (V)", h * nu / e - 2.28, U, 0.02)
a6 = (Us[-1] - Us[0]) / (nus[-1] - nus[0])
verifie("ex6 coefficient directeur (V.s)", a6, 4.15e-15, 0.005e-15)
verifie("ex6 constante de Planck", a6 * e, 6.64e-34, 0.005e-34)
b6 = Us[0] - a6 * nus[0]
verifie("ex6 ordonnée à l'origine (V)", b6, -2.29, 0.005)
verifie("ex6 fréquence seuil (Hz)", -b6 / a6, 5.5e14, 0.05e14)
# Exercice 9
verifie("ex9 énergie d'un photon rouge (eV)", E_eV(630), 1.97, 0.005)
verifie("ex9 photons par seconde (pour 0,35 W)", 0.35 / (h * c / 630e-9), 1.1e18, 0.05e18)
verifie("ex9 rendement lumineux (%)", 100 * 0.35 / 1.0, 35, 0)
# Exercice 10
verifie("ex10 longueur d'onde maximale absorbée (nm)", 1e9 * h * c / (1.12 * e), 1110, 5)
verifie("ex10 excès pour 400 nm (eV)", E_eV(400) - 1.12, 1.99, 0.005)
verifie("ex10 fraction perdue pour 400 nm (%)", 100 * (E_eV(400) - 1.12) / E_eV(400), 64, 0.5)
verifie("ex10 énergie d'un photon de 1500 nm (eV)", E_eV(1500), 0.83, 0.005)
# Exercice 11
E11 = 0.10 * (4e-6) ** 2 * 0.01
verifie("ex11 énergie reçue par un pixel (J)", E11, 1.6e-14, 1e-18)
N11 = E11 / (h * c / 550e-9)
verifie("ex11 nombre de photons", N11, 4.4e4, 0.05e4)
verifie("ex11 nombre d'électrons", 0.60 * N11, 2.7e4, 0.05e4)
verifie("ex11 temps de pose pour saturer (ms)", 1000 * 0.01 * 30000 / (0.60 * N11), 11, 0.5)
# Exercice 12
verifie("ex12 rendement d'un panneau (%)", 100 * 400 / (1000 * 1.7), 23.5, 0.05)
verifie("ex12 énergie annuelle (kWh)", 0.235 * 1300 * 17 * 0.8, 4.15e3, 0.005e3)
verifie("ex12 puissance crête de l'installation (kW)", 10 * 0.400, 4.0, 1e-9)
verifie("ex12 énergie par kWc (kWh)", 0.235 * 1300 * 17 * 0.8 / 4.0, 1040, 5)
# Exercice 13
verifie("ex13 énergie d'un photon de 420 nm (eV)", E_eV(420), 2.96, 0.005)
verifie("ex13 énergie cinétique maximale (eV)", E_eV(420) - 2.0, 0.96, 0.005)
verifie("ex13 charge d'une impulsion (C)", 1e6 * e, 1.6e-13, 1e-18)
verifie("ex13 photons détectés sur 1000", 1000 * 0.25, 250, 0)
verifie("ex13 seuil de la photocathode (nm)", 1e9 * h * c / (2.0 * e), 622, 0.5)
# Exercice 14
N14 = 1.0e-6 / (h * c / 450e-9)
verifie("ex14 photons par seconde", N14, 2.26e12, 0.005e12)
verifie("ex14 électrons par seconde", 0.20 * N14, 4.5e11, 0.05e11)
verifie("ex14 intensité du courant (nA)", 1e9 * 0.20 * N14 * e, 72, 0.5)
verifie("ex14 énergie cinétique maximale (eV)", E_eV(450) - 2.1, 0.66, 0.005)
verifie("ex14 courant pour 2,0 µW (nA)", 2 * 1e9 * 0.20 * N14 * e, 145, 0.5)
# Exercice 15
verifie("ex15 énergie de la transition (eV)", 20.66 - 18.70, 1.96, 1e-9)
verifie("ex15 longueur d'onde (nm)", 1e9 * h * c / (1.96 * e), 634, 0.5)
verifie("ex15 énergie avec h précis (nm)", 1239.84 / 1.96, 632.6, 0.05)
# Valeurs intermédiaires des corrigés
verifie("cor3 photon de 600 nm (eV)", E_eV(600), 2.07, 0.005)
verifie("cor5 photon de 550 nm (J)", h * c / 550e-9, 3.62e-19, 0.005e-19)
verifie("cor9 photon de 630 nm (J)", h * c / 630e-9, 3.16e-19, 0.005e-19)
verifie("cor12 couverture des besoins (%)", 100 * 0.235 * 1300 * 17 * 0.8 / 4500, 92, 0.5)
verifie("cor14 photon de 450 nm (J)", h * c / 450e-9, 4.42e-19, 0.005e-19)
verifie("cor14 photon de 450 nm (eV)", E_eV(450), 2.76, 0.005)
verifie("cor14 photon de 700 nm (eV)", E_eV(700), 1.78, 0.005)
verifie("cor8 puissance lumineuse reçue (W)", 1000 * 0.025, 25, 0)
# Défi D25


def programme_d25():
    lam = [940, 630, 590, 525, 470]            # nm
    Us = [1.28, 1.91, 2.04, 2.29, 2.56]        # V
    x = [1e9 / l for l in lam]                 # 1/lambda (m^-1)
    n = len(x)
    mx, my = sum(x) / n, sum(Us) / n
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, Us))
    den = sum((xi - mx)**2 for xi in x)
    a = num / den                              # V.m
    h = a * 1.602e-19 / 2.998e8
    print(round(a * 1e6, 3), round(h * 1e34, 2))


s = sortie_de(programme_d25)
print('   D25 sortie :', s)
if s != '1.203 6.43':
    ECHECS.append('D25 sortie')
for lam, U in ((940, 1.28), (630, 1.91), (590, 2.04), (525, 2.29), (470, 2.56)):
    verifie(f"D25 seuil théorique pour {lam} nm (V)", 1239.84 / lam, round(1239.84 / lam, 2), 0.005)
    verifie(f"D25 écart mesure/théorie pour {lam} nm (%)", 100 * (U - 1239.84 / lam) / (1239.84 / lam), -3, 0.6)
verifie("D25 écart relatif sur h (%)", 100 * (6.43 - 6.626) / 6.626, -3.0, 0.05)
verifie("D25 énergie thermique kT à 300 K (eV)", 1.38e-23 * 300 / e, 0.026, 0.0005)
verifie("D25 inverse de 940 nm (µm^-1)", 1000 / 940, 1.064, 0.0005)
verifie("D25 inverse de 470 nm (µm^-1)", 1000 / 470, 2.128, 0.0005)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 25 et du défi D25 sont vérifiées.")
