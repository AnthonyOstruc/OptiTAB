"""Vérification des résultats numériques des six sujets type bac et de leurs corrigés.

Lancer : python -I -X utf8 verifications/sujets_bac.py
"""
import io
from contextlib import redirect_stdout
from math import atanh, cos, exp, log, log10, pi, radians, sin, sqrt, tan
from pathlib import Path

ECHECS = []
DONNEES = Path(__file__).resolve().parent.parent / 'figures' / 'donnees'
F, R, G = 96500, 8.314, 6.67e-11
h_planck, c_lum, e = 6.63e-34, 3.00e8, 1.60e-19


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


def compare(nom, sortie, attendu):
    print(f"   {nom} : {sortie}")
    if sortie != attendu:
        ECHECS.append(nom)


def table(nom):
    lignes = (DONNEES / nom).read_text(encoding='utf-8').split('\n')[1:]
    return [[float(x) for x in ligne.split()] for ligne in lignes if ligne.strip()]


# ---------------------------------------------------------------- Sujet 1
# Exercice 1 : détartrant à l'acide lactique
verifie("S1E1 masse d'acide par litre (g)", 1100 * 0.45, 495, 1e-9)
verifie("S1E1 concentration annoncée (mol/L)", 1100 * 0.45 / 90.1, 5.5, 0.05)
verifie("S1E1 volume équivalent attendu (mL)", 1100 * 0.45 / 90.1 / 100 * 20.0 / 0.100, 11.0, 0.05)
courbe = table('bac-s1-ph.dat')
ph = {round(v, 2): p for v, p in courbe}
verifie("S1E1 pH initial lu", ph[0.0], 2.6, 0.05)
verifie("S1E1 pH d'un acide fort à 0,0545 mol/L", -log10(0.0545), 1.3, 0.05)
verifie("S1E1 pH à la demi-équivalence", ph[5.4] + (ph[5.5] - ph[5.4]) / 2, 3.9, 0.05)
verifie("S1E1 pH à l'équivalence", ph[10.9], 8.2, 0.05)
saut = max(range(1, len(courbe)), key=lambda i: courbe[i][1] - courbe[i - 1][1])
verifie("S1E1 volume du saut le plus fort (mL)", courbe[saut][0], 10.9, 0.05)
verifie("S1E1 pH final (20 mL)", ph[20.0], 12.4, 0.05)
cA = 0.100 * 10.9 / 20.0
verifie("S1E1 concentration titrée (mol/L)", cA, 0.0545, 1e-9)
verifie("S1E1 concentration du détartrant (mol/L)", 100 * cA, 5.45, 1e-9)
titre = 100 * 100 * cA * 90.1 / 1100
verifie("S1E1 titre massique (%)", titre, 44.6, 0.05)
verifie("S1E1 incertitude-type sur le titre (%)", 0.011 * titre, 0.49, 0.005)
verifie("S1E1 écart normalisé", abs(44.6 - 45) / 0.49, 0.8, 0.05)
verifie("S1E1 rapport lactate / acide à pH 7,4", 10 ** (7.4 - 3.86), 3.5e3, 0.05e3)
# Exercice 2 : lancer du poids


def programme_s1e2():
    g, v0, h = 9.81, 13.5, 2.10
    meilleur, xmax = 0, 0
    for a in range(20, 61):
        vx = v0 * cos(radians(a))
        vy = v0 * sin(radians(a))
        t = (vy + sqrt(vy**2 + 2 * g * h)) / g
        if vx * t > xmax:
            meilleur, xmax = a, vx * t
    print(meilleur, round(xmax, 2))


compare('S1E2 programme', sortie_de(programme_s1e2), '42 20.57')
g, v0, al, h0 = 9.81, 13.5, radians(40), 2.10
vx, vy = v0 * cos(al), v0 * sin(al)
verifie("S1E2 poids (N)", 7.26 * 9.81, 71.2, 0.05)
verifie("S1E2 force de frottement maximale (N)", 0.5 * 1.2 * 0.47 * pi * 0.060 ** 2 * 13.5 ** 2, 0.58, 0.005)
verifie("S1E2 vx (m/s)", vx, 10.3, 0.05)
verifie("S1E2 vy0 (m/s)", vy, 8.68, 0.005)
verifie("S1E2 coefficient de x² (m^-1)", g / (2 * vx ** 2), 0.0459, 0.00005)
verifie("S1E2 tan alpha", tan(al), 0.839, 0.0005)
tvol = (vy + sqrt(vy ** 2 + 2 * g * h0)) / g
verifie("S1E2 durée du vol (s)", tvol, 1.98, 0.005)
verifie("S1E2 portée (m)", vx * tvol, 20.5, 0.05)
verifie("S1E2 date du sommet (s)", vy / g, 0.885, 0.0005)
verifie("S1E2 hauteur maximale (m)", h0 + vy ** 2 / (2 * g), 5.94, 0.005)
verifie("S1E2 vitesse à l'impact (m/s)", sqrt(v0 ** 2 + 2 * g * h0), 14.9, 0.05)
verifie("S1E2 portée sur sol plat à 45° (m)", v0 ** 2 / g, 18.6, 0.05)
# Exercice 3 : capteur d'humidité
verifie("S1E3 63 % de E (V)", 0.63 * 3.3, 2.1, 0.05)
verifie("S1E3 capacité (pF)", 186e-6 / 1.0e6 * 1e12, 186, 1e-9)
verifie("S1E3 humidité relative (%)", (186 - 161) / 0.34, 74, 0.5)
verifie("S1E3 tau au seuil de 70 % (µs)", 161 + 0.34 * 70, 185, 0.5)
verifie("S1E3 variation de HR pour 1 pF (%)", 1 / 0.34, 2.9, 0.05)
verifie("S1E3 mesures par seconde", 1 / (10 * 186e-6), 538, 0.5)
# ---------------------------------------------------------------- Sujet 2
# Exercice 1 : dihydrogène vert
ne = 200 * 3600 / F
verifie("S2E1 quantité d'électrons (mol)", ne, 7.46, 0.005)
verifie("S2E1 quantité de dihydrogène (mol)", ne / 2, 3.73, 0.005)
verifie("S2E1 masse de dihydrogène (g)", ne / 2 * 2.0, 7.46, 0.005)
verifie("S2E1 volume de dihydrogène (L)", ne / 2 * R * 293 / 1.0e5 * 1000, 91, 0.5)
verifie("S2E1 quantité de dioxygène (mol)", ne / 4, 1.87, 0.005)
verifie("S2E1 énergie électrique (MJ)", 1.9 * 200 * 3600 / 1e6, 1.37, 0.005)
verifie("S2E1 énergie électrique (kWh)", 1.9 * 200 * 3600 / 3.6e6, 0.38, 1e-9)
verifie("S2E1 énergie par kilogramme (kWh/kg)", 0.38 / (ne / 2 * 2.0e-3), 50.9, 0.05)
nb = 200e5 * 50e-3 / (R * 293)
verifie("S2E1 quantité dans la bouteille (mol)", nb, 411, 0.5)
verifie("S2E1 masse dans la bouteille (kg)", nb * 2.0e-3, 0.82, 0.005)
verifie("S2E1 masse réelle avec Z = 1,13 (kg)", nb * 2.0e-3 / 1.13, 0.73, 0.005)
verifie("S2E1 quantité de dihydrogène consommée par la pile (mol)", 730 / 2.0, 365, 1e-9)
verifie("S2E1 charge débitée par la pile (C)", 2 * 365 * F, 7.04e7, 0.005e7)
verifie("S2E1 énergie électrique de la pile (J)", 0.70 * 2 * 365 * F, 4.93e7, 0.005e7)
verifie("S2E1 énergie électrique de la pile (kWh)", 0.70 * 2 * 365 * F / 3.6e6, 13.7, 0.05)
verifie("S2E1 énergie pour produire 0,73 kg (kWh)", 0.73 * 50.9, 37.2, 0.05)
verifie("S2E1 rendement de la chaîne (%)", 100 * 13.7 / 37.2, 37, 0.5)
verifie("S2E1 volume de dihydrogène (m³)", 3.73 * R * 293 / 1.0e5, 9.1e-2, 0.05e-2)
# Exercice 2 : échographie Doppler
verifie("S2E2 longueur d'onde (mm)", 1540 / 5.0e6 * 1000, 0.31, 0.005)
verifie("S2E2 durée de l'aller-retour (µs)", 2 * 0.040 / 1540 * 1e6, 52, 0.5)
verifie("S2E2 vitesse du sang (m/s)", 1300 * 1540 / (2 * 5.0e6 * cos(radians(60))), 0.40, 0.005)
verifie("S2E2 atténuation par cm à 5 MHz (dB)", 0.5 * 5, 2.5, 1e-9)
verifie("S2E2 atténuation sur l'aller-retour (dB)", 2 * 4.0 * 2.5, 20, 1e-9)
verifie("S2E2 rapport des intensités", 10 ** (20 / 10), 100, 1e-9)
verifie("S2E2 profondeur maximale (cm)", 60 / 2.5 / 2, 12, 1e-9)
verifie("S2E2 profondeur maximale à 2,5 MHz (cm)", 60 / 1.25 / 2, 24, 1e-9)
verifie("S2E2 longueur d'onde à 2,5 MHz (mm)", 1540 / 2.5e6 * 1000, 0.62, 0.005)
# Exercice 3 : datation au carbone 14
lam_a = log(2) / 5700
verifie("S2E3 constante radioactive (an^-1)", lam_a, 1.22e-4, 0.005e-4)
verifie("S2E3 constante radioactive (s^-1)", lam_a / (365.25 * 24 * 3600), 3.85e-12, 0.005e-12)
verifie("S2E3 rapport d'activités", 0.122 / 0.23, 0.530, 0.0005)
verifie("S2E3 âge (ans)", log(0.23 / 0.122) / lam_a, 5.2e3, 0.05e3)
verifie("S2E3 noyaux de carbone 14 par gramme", 0.23 / (lam_a / (365.25 * 24 * 3600)), 6.0e10, 0.05e10)
verifie("S2E3 rapport d'activités à 50 000 ans (%)", 100 * 2 ** (-50000 / 5700), 0.23, 0.005)
verifie("S2E3 activité à 50 000 ans (Bq/g)", 0.23 * 2 ** (-50000 / 5700), 5.3e-4, 0.05e-4)
# ---------------------------------------------------------------- Sujet 3
# Exercice 1 : arôme de banane
verifie("S3E1 masse d'alcool (g)", 0.200 * 88.1, 17.6, 0.05)
verifie("S3E1 volume d'acide (mL)", 0.400 * 60.1 / 1.05, 22.9, 0.05)
verifie("S3E1 masse maximale d'ester (g)", 0.200 * 130.2, 26.0, 0.05)
verifie("S3E1 quantité d'ester obtenue (mol)", 20.8 / 130.2, 0.160, 0.0005)
verifie("S3E1 rendement (%)", 100 * 20.8 / 130.2 / 0.200, 80, 0.5)
xeq = (2.4 - sqrt(2.4 ** 2 - 4 * 3 * 0.32)) / 6
verifie("S3E1 avancement à l'équilibre (mol)", xeq, 0.169, 0.0005)
verifie("S3E1 quotient avec x = 0,169", 0.169 ** 2 / ((0.200 - 0.169) * (0.400 - 0.169)), 4.0, 0.05)
verifie("S3E1 rendement à l'équilibre (%)", 100 * xeq / 0.200, 84.5, 0.05)
verifie("S3E1 rendement à l'équilibre, mélange équimolaire (%)", 100 * 2 / 3, 67, 0.5)
# Exercice 2 : satellite d'observation
M_T, R_T = 5.97e24, 6371e3
r = R_T + 694e3
v = sqrt(G * M_T / r)
T = 2 * pi * r / v
verifie("S3E2 rayon de l'orbite (km)", r / 1000, 7065, 0.5)
verifie("S3E2 vitesse (m/s)", v, 7.51e3, 0.005e3)
verifie("S3E2 période (min)", T / 60, 98.5, 0.05)
verifie("S3E2 période (s)", T, 5.91e3, 0.005e3)
verifie("S3E2 orbites par jour", 86400 / T, 14.6, 0.05)
verifie("S3E2 T²/r³ (s²/m³)", T ** 2 / r ** 3, 9.91e-14, 0.005e-14)
verifie("S3E2 accélération sur l'orbite (m/s²)", G * M_T / r ** 2, 7.98, 0.005)
verifie("S3E2 limite de diffraction (rad)", 600e-9 / 0.65, 9.2e-7, 0.05e-7)
verifie("S3E2 résolution au sol (m)", 600e-9 / 0.65 * 694e3, 0.64, 0.005)
rgeo = (G * M_T * 86164 ** 2 / (4 * pi ** 2)) ** (1 / 3)
verifie("S3E2 altitude géostationnaire (km)", (rgeo - R_T) / 1000, 35.8e3, 0.05e3)
verifie("S3E2 résolution depuis l'orbite géostationnaire (m)", 600e-9 / 0.65 * 35.8e6, 33, 0.5)
# Exercice 3 : bouilloire et thé
Qb = 1.0 * 4180 * (100 - 18)
verifie("S3E3 énergie reçue par l'eau (J)", Qb, 3.43e5, 0.005e5)
verifie("S3E3 durée idéale (s)", Qb / 2200, 156, 0.5)
verifie("S3E3 rendement (%)", 100 * Qb / (2200 * 180), 87, 0.5)
tau = 10 / log(60 / 40)
verifie("S3E3 temps caractéristique (min)", tau, 24.7, 0.05)
verifie("S3E3 date à 40 °C (min)", tau * log(3), 27, 0.5)
verifie("S3E3 température à 30 min (°C)", 20 + 60 * exp(-30 / tau), 37.8, 0.05)
# ---------------------------------------------------------------- Sujet 4
# Exercice 1 : décomposition de l'eau oxygénée
verifie("S4E1 concentration à 10 volumes (mol/L)", 2 * 10 / 22.4, 0.89, 0.005)
n0 = 0.20 * 20.0e-3
dpmax = n0 / 2 * R * 298 / 250e-6
verifie("S4E1 quantité initiale (mol)", n0, 4.0e-3, 1e-12)
verifie("S4E1 dioxygène maximal (mol)", n0 / 2, 2.0e-3, 1e-12)
verifie("S4E1 surpression maximale (kPa)", dpmax / 1000, 19.8, 0.05)
k = log(2) / 4.0
for t, p in ((2, 5.8), (4, 9.9), (6, 12.8), (8, 14.9), (12, 17.3), (16, 18.6), (20, 19.2), (30, 19.7)):
    verifie(f"S4E1 surpression à {t} min (kPa)", dpmax / 1000 * (1 - exp(-k * t)), p, 0.05)
verifie("S4E1 constante de vitesse (min^-1)", k, 0.173, 0.0005)
verifie("S4E1 test ordre 1 à 8 min (min^-1)", log(19.8 / (19.8 - 14.9)) / 8, 0.17, 0.005)
verifie("S4E1 vitesse initiale (mol/L/min)", k * 0.20, 0.035, 0.0005)
verifie("S4E1 avancement pour 9,9 kPa (mol)", 9.9e3 * 250e-6 / (R * 298), 1.0e-3, 0.005e-3)
# Exercice 2 : lunette astronomique
verifie("S4E2 grossissement", 900 / 10, 90, 1e-9)
verifie("S4E2 longueur de la lunette (mm)", 900 + 10, 910, 1e-9)
verifie("S4E2 diamètre apparent de Jupiter (rad)", 45 / 3600 * pi / 180, 2.2e-4, 0.05e-4)
verifie("S4E2 angle de l'image (rad)", 90 * 45 / 3600 * pi / 180, 2.0e-2, 0.05e-2)
verifie("S4E2 angle de l'image (degrés)", 90 * 45 / 3600, 1.1, 0.05)
verifie("S4E2 oculaire pour G = 36 (mm)", 900 / 36, 25, 1e-9)
verifie("S4E2 Lune dans la lunette (degrés)", 0.5 * 90, 45, 1e-9)
verifie("S4E2 limite de diffraction (rad)", 550e-9 / 0.070, 7.9e-6, 0.05e-6)
verifie("S4E2 limite de diffraction (secondes d'arc)", 550e-9 / 0.070 * 180 / pi * 3600, 1.6, 0.05)
# Exercice 3 : château d'eau
verifie("S4E3 pression au robinet fermé (Pa)", 1.013e5 + 1000 * 9.81 * 35, 4.4e5, 0.05e5)
verifie("S4E3 surpression (bar)", 1000 * 9.81 * 35 / 1e5, 3.4, 0.05)
verifie("S4E3 vitesse de Torricelli (m/s)", sqrt(2 * 9.81 * 35), 26, 0.5)
S = pi * 0.012 ** 2 / 4
verifie("S4E3 débit théorique (L/min)", S * sqrt(2 * 9.81 * 35) * 60000, 178, 0.5)
verifie("S4E3 vitesse réelle (m/s)", 12e-3 / 60 / S, 1.8, 0.05)
verifie("S4E3 durée de remplissage (min)", 150 / 12, 12.5, 1e-9)
# ---------------------------------------------------------------- Sujet 5
# Exercice 1 : pile zinc-air
Qz = 0.620 * 3600
verifie("S5E1 charge (C)", Qz, 2232, 1e-9)
verifie("S5E1 quantité d'électrons (mol)", Qz / F, 2.31e-2, 0.005e-2)
verifie("S5E1 quantité de zinc (mol)", Qz / F / 2, 1.16e-2, 0.005e-2)
verifie("S5E1 masse de zinc (g)", Qz / F / 2 * 65.4, 0.76, 0.005)
verifie("S5E1 durée de fonctionnement (h)", 620 / 1.2, 517, 0.5)
verifie("S5E1 durée en jours de 16 h", 620 / 1.2 / 16, 32, 0.5)
verifie("S5E1 énergie (J)", 1.4 * Qz, 3.1e3, 0.05e3)
verifie("S5E1 énergie massique (Wh/kg)", 1.4 * Qz / 3600 / 1.9e-3, 4.6e2, 0.05e2)
verifie("S5E1 quantité de dioxygène (mol)", Qz / F / 4, 5.8e-3, 0.05e-3)
verifie("S5E1 volume de dioxygène (L)", Qz / F / 4 * 24, 0.14, 0.005)
verifie("S5E1 volume d'air (L)", Qz / F / 4 * 24 / 0.21, 0.66, 0.005)
# Exercice 2 : parachutiste


def programme_s5e2():
    m, g, k = 80, 9.81, 0.25
    vlim = (m * g / k) ** 0.5
    t, v, z, dt = 0.0, 0.0, 0.0, 0.1
    while v < 0.95 * vlim:
        v = v + (g - k / m * v**2) * dt
        z = z + v * dt
        t = t + dt
    print(round(t, 1), round(v, 1), round(z))


compare('S5E2 programme', sortie_de(programme_s5e2), '10.4 53.3 373')
vl = sqrt(80 * 9.81 / 0.25)
verifie("S5E2 vitesse limite (m/s)", vl, 56, 0.5)
verifie("S5E2 vitesse limite (km/h)", vl * 3.6, 202, 0.5)
verifie("S5E2 durée exacte pour 95 % (s)", vl / 9.81 * atanh(0.95), 10.5, 0.05)
verifie("S5E2 chute libre en 10,4 s (m)", 0.5 * 9.81 * 10.4 ** 2, 531, 0.5)
verifie("S5E2 vitesse limite avec le parachute (m/s)", sqrt(80 * 9.81 / 30), 5.1, 0.05)
verifie("S5E2 puissance des frottements à vitesse limite (W)", 80 * 9.81 * vl, 4.4e4, 0.05e4)
para = table('bac-s5-parachute.dat')
verifie("S5E2 figure : vitesse à 5 s (m/s)", dict((round(t, 1), v) for t, v in para)[5.0], 39.6, 0.05)
verifie("S5E2 figure : vitesse à 25 s (m/s)", para[-1][1], 56.0, 0.05)
verifie("S5E2 figure : pente à l'origine (m/s²)", para[1][1] / 0.1, 9.81, 1e-9)
# Exercice 3 : diamètre d'un cheveu
a_ch = 2 * 650e-9 * 2.00 / 0.037
rel = sqrt((0.1 / 3.7) ** 2 + (0.01 / 2.00) ** 2)
verifie("S5E3 demi-angle (rad)", 0.037 / 2 / 2.00, 9.25e-3, 1e-9)
verifie("S5E3 diamètre (µm)", a_ch * 1e6, 70, 0.5)
verifie("S5E3 incertitude relative (%)", 100 * rel, 2.7, 0.05)
verifie("S5E3 incertitude-type (µm)", rel * a_ch * 1e6, 1.9, 0.05)
verifie("S5E3 incertitude-type sur l'écart (µm)", sqrt(1.9 ** 2 + 1 ** 2), 2.1, 0.05)
verifie("S5E3 écart normalisé", abs(70.3 - 72) / sqrt(1.9 ** 2 + 1 ** 2), 0.8, 0.05)
verifie("S5E3 diamètre avec trois chiffres (µm)", a_ch * 1e6, 70.3, 0.05)
# ---------------------------------------------------------------- Sujet 6
# Exercice 1 : paracétamol
na_ = 3.0 / 109.1
nb_ = 4.0 * 1.08 / 102.1
verifie("S6E1 quantité de 4-aminophénol (mol)", na_, 2.75e-2, 0.005e-2)
verifie("S6E1 quantité d'anhydride (mol)", nb_, 4.23e-2, 0.005e-2)
verifie("S6E1 masse maximale (g)", na_ * 151.2, 4.16, 0.005)
verifie("S6E1 rendement (%)", 100 * 3.3 / 151.2 / na_, 79, 0.5)
verifie("S6E1 économie d'atomes (%)", 100 * 151.2 / (109.1 + 102.1), 71.6, 0.05)
verifie("S6E1 coefficient d'étalonnage (L/mg)", 9800 / 151.2 / 1000, 0.0648, 0.00005)
c_mg = 0.640 / 0.0648
verifie("S6E1 concentration mesurée (mg/L)", c_mg, 9.88, 0.005)
verifie("S6E1 masse du comprimé (mg)", c_mg * 50, 494, 0.5)
verifie("S6E1 incertitude-type (mg)", 0.015 * c_mg * 50, 7.4, 0.05)
verifie("S6E1 écart normalisé", abs(494 - 500) / 7.4, 0.8, 0.05)
verifie("S6E1 absorbance attendue pour 500 mg", 0.0648 * 10.0, 0.648, 1e-9)
# Exercice 2 : photovoltaïque spatial
verifie("S6E2 longueur d'onde seuil (nm)", h_planck * c_lum / (1.12 * e) * 1e9, 1110, 0.5)
Eph = h_planck * c_lum / 550e-9
verifie("S6E2 énergie d'un photon à 550 nm (J)", Eph, 3.62e-19, 0.005e-19)
verifie("S6E2 énergie d'un photon à 550 nm (eV)", Eph / e, 2.26, 0.005)
verifie("S6E2 part perdue pour ce photon (%)", 100 * (1 - 1.12 / 2.26), 50, 0.5)
verifie("S6E2 photons par seconde et par m²", 1361 / Eph, 3.8e21, 0.05e21)
verifie("S6E2 puissance électrique (kW)", 1361 * 20 * 0.30 / 1000, 8.2, 0.05)
verifie("S6E2 énergie par orbite (kWh)", 1361 * 20 * 0.30 * (98.5 - 35) / 60 / 1000, 8.6, 0.05)
# Exercice 3 : niveau sonore d'un concert
verifie("S6E3 intensité à 10 m (W/m²)", 1e-12 * 10 ** 10.5, 3.2e-2, 0.05e-2)
verifie("S6E3 puissance sonore (W)", 1e-12 * 10 ** 10.5 * 4 * pi * 10 ** 2, 40, 0.5)
verifie("S6E3 niveau à 40 m (dB)", 105 - 20 * log10(4), 93, 0.5)
verifie("S6E3 deux enceintes à 40 m (dB)", 105 - 20 * log10(4) + 10 * log10(2), 96, 0.5)
verifie("S6E3 distance pour 85 dB (m)", 10 * 10 ** ((105 - 85) / 20), 100, 1e-9)
verifie("S6E3 durée d'exposition à 105 dB (min)", 8 * 60 / 2 ** ((105 - 85) / 3), 4.7, 0.05)
verifie("S6E3 niveau avec bouchons (dB)", 105 - 25, 80, 1e-9)
verifie("S6E3 durée d'exposition à 96 dB (min)", 8 * 60 / 2 ** ((96 - 85) / 3), 38, 0.5)

# ---------------------------------------------------------------- Compléments des corrigés
# Sujet 1
verifie("S1E1 masse d'acide par litre mesurée (g)", 5.45 * 90.1, 491, 0.5)
for x0, y0 in ((8.7, 4.46), (12.5, 11.692)):
    verifie(f"S1E1 tangente de pente 0,25 au point d'abscisse {x0}", y0 - 0.25 * x0, 2.285 if x0 < 10 else 8.567, 0.0005)
verifie("S1E1 droite équidistante au volume équivalent", (2.285 + 8.567) / 2 + 0.25 * 10.9, ph[10.9], 0.1)
verifie("S1E2 aire du maître-couple (m²)", pi * 0.060 ** 2, 1.13e-2, 0.005e-2)
verifie("S1E2 discriminant", 0.839 ** 2 + 4 * 0.0459 * 2.10, 1.089, 0.0005)
verifie("S1E2 racine positive (m)", (0.839 + sqrt(1.089)) / (2 * 0.0459), 20.5, 0.05)
verifie("S1E3 dix temps caractéristiques (ms)", 10 * 0.186, 1.86, 1e-9)
# Sujet 2
verifie("S2E3 nombre de demi-vies en 50 000 ans", 50000 / 5700, 8.8, 0.05)
verifie("S2E3 date de la mort (année)", 1991 - log(0.23 / 0.122) / lam_a, -3200, 50)
# Sujet 3
verifie("S3E1 quotient avec les valeurs arrondies", 0.169 ** 2 / (0.031 * 0.231), 4.0, 0.05)
verifie("S3E1 avancement, mélange équimolaire (mol)", 0.4 / 3, 0.133, 0.0005)
verifie("S3E2 rayon géostationnaire (m)", rgeo, 4.215e7, 0.0005e7)
verifie("S3E3 énergie électrique (J)", 2200 * 180, 3.96e5, 1e-9)
# Sujet 4
verifie("S4E1 dioxygène libéré par litre à 10 volumes (mol)", 10 / 22.4, 0.446, 0.0005)
verifie("S4E2 bande vue dans la lunette (secondes d'arc)", 90 * 4, 360, 1e-9)
verifie("S4E2 détail limite vu dans la lunette (secondes d'arc)", 90 * 1.6, 144, 1e-9)
verifie("S4E2 grossissement avec l'oculaire de 4 mm", 900 / 4, 225, 1e-9)
verifie("S4E3 débit théorique (m³/s)", S * sqrt(2 * 9.81 * 35), 2.96e-3, 0.005e-3)
verifie("S4E3 section du robinet (m²)", S, 1.13e-4, 0.005e-4)
verifie("S4E3 rapport des vitesses", sqrt(2 * 9.81 * 35) / (12e-3 / 60 / S), 15, 0.5)


def programme_s4e1():
    t = [2, 4, 6, 8, 12, 16]
    dP = [5.8, 9.9, 12.8, 14.9, 17.3, 18.6]
    dPmax = 19.8
    for i in range(len(t)):
        k = log(dPmax / (dPmax - dP[i])) / t[i]
        print(t[i], round(k, 3))


compare('S4E1 programme', sortie_de(programme_s4e1).replace('\n', ' | '), '2 0.173 | 4 0.173 | 6 0.173 | 8 0.175 | 12 0.172 | 16 0.175')
verifie("S4E1 demi-vie avec k = 0,173 (min)", log(2) / 0.173, 4.0, 0.05)
# Sujet 5
verifie("S5E1 énergie (Wh)", 1.4 * 2232 / 3600, 0.87, 0.005)
verifie("S5E2 tangente à l'origine à 5 s (m/s)", 9.81 * 5, 49, 0.5)
verifie("S5E2 hauteur de chute équivalente (m)", 5.1 ** 2 / (2 * 9.81), 1.3, 0.05)
# Sujet 6
pts_etal = [(2, 0.131), (4, 0.258), (6, 0.390), (8, 0.517), (10, 0.649), (12, 0.777)]
pente = sum(c * a for c, a in pts_etal) / sum(c * c for c, _ in pts_etal)
verifie("S6E1 pente de la droite d'étalonnage (L/mg)", pente, 0.0648, 0.00005)
verifie("S6E1 pente par le dernier point (L/mg)", 0.777 / 12.0, 0.0648, 0.00005)
verifie("S6E1 absorbance sans dilution", 0.0648 * 494, 32, 0.5)
verifie("S6E1 part de la masse perdue en sous-produit (%)", 100 * (1 - 151.2 / (109.1 + 102.1)), 28, 0.5)
verifie("S6E2 longueur d'onde seuil (m)", h_planck * c_lum / (1.12 * e), 1.11e-6, 0.005e-6)
verifie("S6E2 consommation par orbite (kWh)", 5.0 * 98.5 / 60, 8.2, 0.05)
verifie("S6E2 énergie à stocker pour l'éclipse (kWh)", 5.0 * 35 / 60, 2.9, 0.05)
verifie("S6E3 atténuation quand la distance double (dB)", 10 * log10(4), 6, 0.05)
verifie("S6E3 niveau avec bouchons à 96 dB (dB)", 96 - 25, 71, 1e-9)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs des sujets type bac sont vérifiées.")
