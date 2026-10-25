"""Vérification des six devoirs surveillés (énoncés et corrigés).

Lancer : python -I -X utf8 verifications/devoirs.py
"""
import io
from contextlib import redirect_stdout
from math import sqrt, sin, radians
from statistics import mean, stdev, linear_regression

ECHECS = []


def verifie(nom, calcule, publie, tol_rel=0.006):
    ok = abs(calcule - publie) <= tol_rel * abs(publie) + 1e-12
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:62s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def compare_sortie(nom, fonction, attendu):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    s = tampon.getvalue().strip()
    print(f'   {nom} :', s.replace('\n', ' | '))
    if s != attendu:
        ECHECS.append(nom)


# ---------------------------------------------------------------- Devoir 1
c_et = [1.0, 2.0, 3.0, 4.0, 5.0]
A_et = [0.16, 0.33, 0.48, 0.64, 0.81]
k = sum(c * a for c, a in zip(c_et, A_et)) / sum(c * c for c in c_et)
verifie("D1 ex1 coefficient k (L/mg)", k, 0.161, 0.005)
verifie("D1 ex1 concentration diluée (mg/L)", 0.52 / k, 3.2, 0.01)
verifie("D1 ex1 concentration du sirop (mg/L)", 20 * 0.52 / k, 64, 0.01)
verifie("D1 ex1 boisson diluée 8 fois (mg/L)", 64 / 8, 8.0)
verifie("D1 ex1 masse par verre de 25 cL (mg)", 8.0 * 0.25, 2.0)
verifie("D1 ex1 DJA pour 30 kg (mg)", 5 * 30, 150)
verifie("D1 ex1 nombre de verres", 150 / 2.0, 75)
verifie("D1 ex2 cuivre initial (mol)", 0.635 / 63.5, 1.00e-2)
verifie("D1 ex2 ions argent initiaux (mol)", 0.100 * 0.0500, 5.00e-3)
xmax = min(0.635 / 63.5, 0.100 * 0.0500 / 2)
verifie("D1 ex2 avancement maximal (mol)", xmax, 2.50e-3)
verifie("D1 ex2 cuivre restant (mol)", 0.0100 - xmax, 7.50e-3)
verifie("D1 ex2 masse de cuivre restante (g)", 7.50e-3 * 63.5, 0.476, 0.002)
verifie("D1 ex2 masse d'argent déposée (g)", 2 * xmax * 107.9, 0.540, 0.002)
verifie("D1 ex2 concentration finale en Cu2+ (mol/L)", xmax / 0.0500, 5.00e-2)
verifie("D1 ex2 masse finale du fil (g)", 0.476 + 0.540, 1.016)
verifie("D1 ex3 masse molaire du saccharose (g/mol)", 12 * 12.0 + 22 * 1.0 + 11 * 16.0, 342.0)
verifie("D1 ex3 concentration en masse (g/L)", 35 / 0.33, 106, 0.003)
verifie("D1 ex3 concentration en quantité (mol/L)", 35 / 0.33 / 342.0, 0.310, 0.003)
verifie("D1 ex3 quantité dans la canette (mol)", 35 / 342.0, 0.102, 0.004)
verifie("D1 ex3 nombre de molécules", 35 / 342.0 * 6.02e23, 6.16e22, 0.003)
verifie("D1 ex3 masse pour 100,0 mL (g)", 0.310 * 0.1000 * 342.0, 10.6, 0.003)
verifie("D1 ex3 volume de solution mère (mL)", 0.0310 * 50.0 / 0.310, 5.0)

# ---------------------------------------------------------------- Devoir 2
c1 = 5 * 2.00e-2 * 17.8 / (2 * 10.0)
verifie("D2 ex1 concentration de S1 (mol/L)", c1, 0.0890)
verifie("D2 ex1 concentration commerciale (mol/L)", 10 * c1, 0.890)
verifie("D2 ex1 dioxygène pour 10 volumes (mol)", 10 / 22.4, 0.446, 0.002)
verifie("D2 ex1 concentration attendue (mol/L)", 2 * 10 / 22.4, 0.893, 0.001)
verifie("D2 ex1 écart relatif (%)", (0.893 - 0.890) / 0.893 * 100, 0.3, 0.2)
verifie("D2 ex1 volume équivalent sans dilution (mL)", 10 * 17.8, 178)
for nom, valeur, publie in [("CH2O", 4 + 2 * 1 + 6, 12), ("HCN", 1 + 4 + 5, 10), ("CCl4", 4 + 4 * 7, 32)]:
    verifie(f"D2 ex2 électrons de valence de {nom}", valeur, publie)
    verifie(f"D2 ex2 doublets de {nom}", valeur / 2, publie / 2)
verifie("D2 ex2 écart C=O", 3.44 - 2.55, 0.89, 0.001)
verifie("D2 ex2 écart C≡N", 3.04 - 2.55, 0.49, 0.001)
verifie("D2 ex2 écart C-Cl", 3.16 - 2.55, 0.61, 0.001)
verifie("D2 ex2 écart C-H", 2.55 - 2.20, 0.35, 0.001)

# ---------------------------------------------------------------- Devoir 3
n_alc = 21.7 * 0.81 / 88.0
n_acide = 23.0 * 1.05 / 60.0
verifie("D3 ex1 masse molaire de l'alcool C5H12O (g/mol)", 5 * 12.0 + 12 * 1.0 + 16.0, 88.0)
verifie("D3 ex1 masse molaire de l'ester C7H14O2 (g/mol)", 7 * 12.0 + 14 * 1.0 + 2 * 16.0, 130.0)
verifie("D3 ex1 masse d'alcool (g)", 21.7 * 0.81, 17.6, 0.003)
verifie("D3 ex1 quantité d'alcool (mol)", n_alc, 0.200, 0.003)
verifie("D3 ex1 masse d'acide (g)", 23.0 * 1.05, 24.2, 0.003)
verifie("D3 ex1 quantité d'acide (mol)", n_acide, 0.40, 0.01)
verifie("D3 ex1 masse maximale d'ester (g)", 0.200 * 130.0, 26.0)
verifie("D3 ex1 quantité d'ester obtenue (mol)", 20.8 / 130.0, 0.160)
verifie("D3 ex1 rendement (%)", 20.8 / 26.0 * 100, 80)
casse = 3 * 345 + 10 * 415 + 6.5 * 498
forme = 8 * 804 + 10 * 463
verifie("D3 ex2 énergie des liaisons rompues (kJ)", casse, 8422)
verifie("D3 ex2 énergie des liaisons formées (kJ)", forme, 11062)
verifie("D3 ex2 énergie molaire de réaction (kJ/mol)", casse - forme, -2640)
verifie("D3 ex2 masse molaire du butane (g/mol)", 4 * 12.0 + 10 * 1.0, 58.0)
verifie("D3 ex2 pouvoir calorifique estimé (MJ/kg)", 2640 / 58.0, 45.5, 0.002)
verifie("D3 ex2 écart aux tables (%)", (45.8 - 45.5) / 45.8 * 100, 0.66, 0.02)
verifie("D3 ex2 énergie de la cartouche (MJ)", 0.190 * 45.8, 8.70, 0.002)
verifie("D3 ex2 énergie pour 1 L d'eau (kJ)", 1.0 * 4.18 * 80, 334, 0.002)
verifie("D3 ex2 litres d'eau chauffés", 0.40 * 8.70e6 / (1.0 * 4180 * 80), 10.4, 0.004)
n_but = 190 / 58.0
verifie("D3 ex2 quantité de butane (mol)", n_but, 3.28, 0.003)
verifie("D3 ex2 masse de CO2 (g)", 4 * n_but * 44.0, 577, 0.002)
verifie("D3 ex3 CO2 de l'éthanol (g/MJ)", 2 / 0.046 * 44.0 / 26.8, 71, 0.01)
verifie("D3 ex3 CO2 du butane (g/MJ)", 4 / 0.058 * 44.0 / 45.8, 66, 0.01)
verifie("D3 ex3 masse molaire de l'éthanol (g/mol)", 2 * 12.0 + 6 * 1.0 + 16.0, 46.0)
verifie("D3 ex3 masse d'éthanol pour 1 MJ (g)", 1000 / 26.8, 37.3, 0.002)
verifie("D3 ex3 quantité d'éthanol pour 1 MJ (mol)", 1000 / 26.8 / 46.0, 0.811, 0.002)
verifie("D3 ex3 masse de butane pour 1 MJ (g)", 1000 / 45.8, 21.8, 0.002)
verifie("D3 ex3 quantité de butane pour 1 MJ (mol)", 1000 / 45.8 / 58.0, 0.376, 0.002)
verifie("D3 ex2 énergie utile (MJ)", 0.40 * 8.70, 3.48, 0.002)
verifie("D3 ex2 CO2 (mol)", 4 * 3.28, 13.1, 0.003)

# ---------------------------------------------------------------- Devoir 4
G, MT, RT = 6.67e-11, 5.97e24, 6.371e6
m_iss, r = 4.20e5, 6.371e6 + 4.00e5
F = G * MT * m_iss / r**2
verifie("D4 ex1 distance au centre de la Terre (m)", r, 6.77e6, 0.001)
verifie("D4 ex1 force exercée par la Terre (N)", F, 3.65e6, 0.002)
verifie("D4 ex1 champ de gravitation à 400 km (N/kg)", F / m_iss, 8.69, 0.002)
verifie("D4 ex1 baisse relative du champ (%)", (9.81 - 8.69) / 9.81 * 100, 11, 0.04)
FL = G * 7.35e22 * m_iss / 3.84e8**2
verifie("D4 ex1 force exercée par la Lune (N)", FL, 14.0, 0.005)
verifie("D4 ex1 rapport Terre / Lune", F / FL, 2.6e5, 0.01)
verifie("D4 ex1 longueur du vecteur à 1 cm pour 1e6 N (cm)", F / 1e6, 3.65, 0.002)
h = [0, 5, 10, 15, 20, 25]
P = [1.01, 1.52, 2.02, 2.52, 3.03, 3.53]
reg = linear_regression(h, P)
verifie("D4 ex2 pente (bar/m)", reg.slope, 0.101, 0.005)
verifie("D4 ex2 ordonnée à l'origine (bar)", reg.intercept, 1.01, 0.003)
verifie("D4 ex2 masse volumique (kg/m3)", reg.slope * 1e5 / 9.81, 1.03e3, 0.005)
P20 = 1.013e5 + 1025 * 9.81 * 20
verifie("D4 ex2 pression à 20 m (Pa)", P20, 3.02e5, 0.002)
verifie("D4 ex2 volume des poumons à 20 m (L)", 6.0 * 1.013e5 / P20, 2.0, 0.01)
verifie("D4 ex2 rapport des pressions", P20 / 1.013e5, 3.0, 0.01)
verifie("D4 ex2 différence de pression à 20 m (Pa)", 1.03e3 * 9.81 * 20, 2.02e5, 0.002)
verifie("D4 ex2 différence relevée (bar)", 3.03 - 1.01, 2.02)
verifie("D4 ex2 volume à 20 m, relevés (L)", 1.01 * 6.0 / 3.03, 2.0)
verifie("D4 ex2 volume en remontant (L)", 6.0 * 3.03 / 1.01, 18)
verifie("D4 ex1 force de la Terre au sol (rappel)", 4.20e5 * 9.81, 4.12e6, 0.002)
verifie("D4 ex3 poids de la pierre (N)", 19.0 * 9.81, 186, 0.003)
verifie("D4 ex3 longueur de v2 (cm)", 2.50 / 0.5, 5.0)
verifie("D4 ex3 longueur de v3 (cm)", 2.30 / 0.5, 4.6)
verifie("D4 ex3 longueur de delta v (cm)", 0.20 / 0.5, 0.4)
x = [0, 1.40, 2.70, 3.90, 5.00, 6.00, 6.90]
dt = 0.50
v = {i: (x[i + 1] - x[i - 1]) / (2 * dt) for i in range(1, 6)}
verifie("D4 ex3 vitesse v2 (m/s)", v[2], 2.50)
verifie("D4 ex3 vitesse v3 (m/s)", v[3], 2.30)
verifie("D4 ex3 variation de vitesse (m/s)", v[3] - v[2], -0.20)
verifie("D4 ex3 somme des forces (N)", 19.0 * abs(v[3] - v[2]) / dt, 7.6)
verifie("D4 ex3 distance d'arrêt depuis M3 (m)", v[3]**2 / (2 * 0.40), 6.6, 0.005)
verifie("D4 ex3 abscisse d'arrêt (m)", 3.90 + v[3]**2 / (2 * 0.40), 10.5, 0.002)

# ---------------------------------------------------------------- Devoir 5
verifie("D5 ex1 énergie de la batterie (W.h)", 36 * 10, 360)
verifie("D5 ex1 énergie de la batterie (J)", 360 * 3600, 1.30e6, 0.004)
verifie("D5 ex1 intensité (A)", 250 / 36, 6.9, 0.01)
verifie("D5 ex1 tension aux bornes (V)", 37.0 - 0.15 * 6.9, 36.0, 0.002)
verifie("D5 ex1 puissance dissipée dans r (W)", 0.15 * 6.9**2, 7.1, 0.01)
verifie("D5 ex1 autonomie (h)", 360 / 250, 1.44)
verifie("D5 ex1 distance à 25 km/h (km)", 1.44 * 25, 36)
verifie("D5 ex1 puissance mécanique (W)", 0.80 * 250, 200)
verifie("D5 ex1 coût d'une recharge (euros)", 0.360 * 0.25, 0.09)
hs = 200 * sin(radians(15))
verifie("D5 ex2 dénivelé (m)", hs, 51.8, 0.002)
verifie("D5 ex2 travail du poids (J)", 70 * 9.81 * hs, 3.55e4, 0.002)
verifie("D5 ex2 vitesse sans frottement (m/s)", sqrt(2 * 9.81 * hs), 31.9, 0.002)
verifie("D5 ex2 vitesse sans frottement (km/h)", sqrt(2 * 9.81 * hs) * 3.6, 115, 0.003)
verifie("D5 ex2 énergie cinétique finale (J)", 0.5 * 70 * 20.0**2, 1.40e4)
verifie("D5 ex2 travail des frottements (J)", 0.5 * 70 * 400 - 70 * 9.81 * hs, -2.15e4, 0.003)
verifie("D5 ex2 force de frottement (N)", (70 * 9.81 * hs - 0.5 * 70 * 400) / 200, 108, 0.003)
verifie("D5 ex2 énergie mécanique perdue (%)", (70 * 9.81 * hs - 14000) / (70 * 9.81 * hs) * 100, 61, 0.01)
y = [1.500, 1.488, 1.451, 1.390, 1.304, 1.193, 1.059]
for i, t in enumerate([0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]):
    verifie(f"D5 ex3 position à t = {t} s (m)", 1.5 - 0.5 * 9.81 * t**2, y[i], 0.0007)


def programme_d5():
    m, g, dt = 0.058, 9.81, 0.05
    y = [1.500, 1.488, 1.451, 1.390, 1.304, 1.193, 1.059]     # m
    for i in range(1, len(y) - 1):
        v = (y[i - 1] - y[i + 1]) / (2 * dt)
        Ec = 0.5 * m * v**2
        Ep = m * g * y[i]
        print(round(Ec, 3), round(Ep, 3), round(Ec + Ep, 3))


compare_sortie('D5 ex3 programme', programme_d5,
               '0.007 0.847 0.854\n0.028 0.826 0.853\n0.063 0.791 0.854\n0.113 0.742 0.854\n0.174 0.679 0.853')
verifie("D5 ex3 énergie mécanique initiale (J)", 0.058 * 9.81 * 1.500, 0.853, 0.002)
verifie("D5 ex3 énergie après le rebond (J)", 0.058 * 9.81 * 1.10, 0.626, 0.002)
verifie("D5 ex3 énergie perdue au rebond (J)", 0.058 * 9.81 * 0.40, 0.228, 0.003)
verifie("D5 ex3 fraction perdue (%)", 0.40 / 1.50 * 100, 27, 0.02)

# ---------------------------------------------------------------- Devoir 6
d = [8.52, 8.48, 8.60, 8.45, 8.55, 8.50, 8.58, 8.47]
md, sd = mean(d), stdev(d)
verifie("D6 ex1 moyenne de 10 longueurs d'onde (cm)", md, 8.519, 0.0005)
verifie("D6 ex1 écart-type (cm)", sd, 0.054, 0.01)
verifie("D6 ex1 longueur d'onde (mm)", md, 8.52, 0.001)
verifie("D6 ex1 célérité (m/s)", md / 10 * 1e-2 * 40.0e3, 340.8, 0.0003)
verifie("D6 ex1 longueur d'onde (cm)", md / 10, 0.8519, 0.0002)
verifie("D6 ex1 incertitude-type arrondie sur v (m/s)", sd / sqrt(8) / 10 * 1e-2 * 40.0e3, 0.8, 0.06)
verifie("D6 ex1 écart à 340 m/s (m/s)", 340.8 - 340, 0.8)
verifie("D6 ex1 écart à 343 m/s (en u)", (343 - 340.8) / 0.8, 2.75, 0.01)
verifie("D6 ex2 inverse de OA' (1/m)", 1 / 0.050 + 1 / -5.00, 19.8)
verifie("D6 ex2 déplacement (mm)", 50.5 - 50.0, 0.5)
verifie("D6 ex1 incertitude-type sur 10 lambda (cm)", sd / sqrt(8), 0.019, 0.01)
verifie("D6 ex1 incertitude-type sur v (m/s)", sd / sqrt(8) / 10 * 1e-2 * 40.0e3, 0.76, 0.01)
verifie("D6 ex1 célérité à 15 °C (m/s)", 331 + 0.6 * 15, 340)
verifie("D6 ex1 célérité à 20 °C (m/s)", 331 + 0.6 * 20, 343)
OAp = 1 / (1 / 0.050 - 1 / 5.00)
verifie("D6 ex2 position de l'image (mm)", OAp * 1000, 50.5, 0.001)
verifie("D6 ex2 grandissement", OAp / -5.00, -0.0101, 0.001)
verifie("D6 ex2 taille de l'image (mm)", OAp / -5.00 * 2.00 * 1000, -20.2, 0.001)
verifie("D6 ex2 vergence (dioptries)", 1 / 0.050, 20)
verifie("D6 ex2 déplacement de l'objectif (mm)", (OAp - 0.050) * 1000, 0.5, 0.02)
verifie("D6 ex2 construction : image (cm)", 1 / (1 / 5 - 1 / 15), 7.5)
verifie("D6 ex2 construction : grandissement", 7.5 / -15, -0.5)
for lam, E in [(625, 1.99), (525, 2.37), (465, 2.67)]:
    verifie(f"D6 ex3 énergie d'un photon de {lam} nm (eV)", 6.63e-34 * 3.00e8 / (lam * 1e-9) / 1.60e-19, E, 0.003)
verifie("D6 ex3 fréquence à 525 nm (Hz)", 3.00e8 / 525e-9, 5.71e14, 0.002)
verifie("D6 ex3 énergie à 525 nm (J)", 6.63e-34 * 3.00e8 / 525e-9, 3.79e-19, 0.002)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs des six devoirs surveillés sont vérifiées.")
