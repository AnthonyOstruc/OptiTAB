"""Vérification du chapitre 11 (Interactions fondamentales et champs) et du défi D11.

Lancer : python -I -X utf8 verifications/chapitre_11.py
"""
import io
import math
from contextlib import redirect_stdout

ECHECS = []
G, K, E = 6.67e-11, 9.0e9, 1.60e-19
ME, MP = 9.11e-31, 1.67e-27
MT, RT, ML, DTL = 5.97e24, 6.37e6, 7.35e22, 3.84e8
MS, DTS = 1.99e30, 1.50e11


def verifie(nom, calcule, publie, tol_rel=0.006):
    ok = abs(calcule - publie) <= tol_rel * abs(publie) + 1e-300
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:60s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def sortie_de(fonction):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    return tampon.getvalue().strip()


# Cours
verifie("cours Coulomb 10 nC à 10 cm (N)", K * 1.0e-8 * 1.0e-8 / 0.10 ** 2, 9.0e-5)
verifie("cours Terre-Lune (N)", G * MT * ML / DTL ** 2, 1.98e20)
verifie("cours g à la surface (N/kg)", G * MT / RT ** 2, 9.81)
verifie("cours champ entre les plaques (V/m)", 1000 / 0.020, 5.0e4)
verifie("cours force sur un électron (N)", E * 5.0e4, 8.0e-15)
verifie("cours champ de la Lune (N/kg)", G * ML / 1.74e6 ** 2, 1.62)
verifie("cours champ du proton à 5,3e-11 m (V/m)", K * E / 5.3e-11 ** 2, 5e11, 0.03)


def programme():
    G_, M, R = 6.67e-11, 5.97e24, 6.37e6
    for h in [0, 400e3, 2000e3, 35786e3]:
        g = G_ * M / (R + h) ** 2
        print(round(h / 1000), 'km :', round(g, 2), 'N/kg')


s = sortie_de(programme)
print('   cours programme :', s.replace('\n', ' | '))
if s != '0 km : 9.81 N/kg\n400 km : 8.69 N/kg\n2000 km : 5.68 N/kg\n35786 km : 0.22 N/kg':
    ECHECS.append('cours programme')
# Exercice 1
verifie("ex1 nombre d'électrons pour -3,2 nC", 3.2e-9 / E, 2.0e10)
# Exercice 2
F2 = K * 2.0e-9 * 3.0e-9 / 0.050 ** 2
verifie("ex2 force (N)", F2, 2.16e-5)
verifie("ex2 force à distance double (N)", F2 / 4, 5.4e-6)
# Exercice 3
verifie("ex3 Terre-Lune (N)", G * MT * ML / DTL ** 2, 1.98e20)
verifie("ex3 Soleil-Terre (N)", G * MS * MT / DTS ** 2, 3.52e22)
verifie("ex3 rapport Soleil / Lune", (G * MS * MT / DTS ** 2) / (G * MT * ML / DTL ** 2), 178)
# Exercice 4
verifie("ex4 g surface (N/kg)", G * MT / RT ** 2, 9.81)
verifie("ex4 poids 70 kg surface (N)", 70 * G * MT / RT ** 2, 687)
gISS = G * MT / (RT + 400e3) ** 2
verifie("ex4 g station spatiale (N/kg)", gISS, 8.69)
verifie("ex4 poids 70 kg dans la station (N)", 70 * gISS, 608)
verifie("ex4 rapport en %", gISS / (G * MT / RT ** 2) * 100, 89)
# Exercice 6
verifie("ex6 g à 10 000 km d'altitude (N/kg)", G * MT / (RT + 1.0e7) ** 2, 1.49)
verifie("ex6 altitude où g est divisé par 4 (km)", RT / 1000, 6370)
verifie("ex6 champ à la surface de la Lune (N/kg)", round(G * ML / 1.74e6 ** 2, 2), 1.62, 0.0001)
# Exercice 7 : atome d'hydrogène
r = 5.3e-11
Fe = K * E ** 2 / r ** 2
Fg = G * ME * MP / r ** 2
verifie("ex7 force électrostatique (N)", Fe, 8.2e-8)
verifie("ex7 force de gravitation (N)", Fg, 3.6e-47, 0.02)
verifie("ex7 rapport", Fe / Fg, 2.3e39, 0.02)
# Exercice 9 : condensateur
E9 = 1.5e3 / 3.0e-2
verifie("ex9 champ (V/m)", E9, 5.0e4)
verifie("ex9 force sur l'électron (N)", E * E9, 8.0e-15)
verifie("ex9 poids de l'électron (N)", ME * 9.81, 8.9e-30, 0.01)
verifie("ex9 rapport", E * E9 / (ME * 9.81), 9.0e14, 0.01)
# Exercice 11 : point d'équilibre Terre-Lune
q = math.sqrt(MT / ML)
x = DTL * q / (1 + q)
verifie("ex11 rapport des masses", MT / ML, 81.2)
verifie("ex11 racine du rapport", q, 9.01)
verifie("ex11 distance au centre de la Terre (m)", x, 3.46e8)
verifie("ex11 fraction de la distance", x / DTL, 0.90)
# Exercice 12 : toner
V12 = 4 / 3 * math.pi * (5.0e-6) ** 3
m12 = 1.2e3 * V12
verifie("ex12 volume d'une particule (m3)", V12, 5.24e-16)
verifie("ex12 masse (kg)", m12, 6.3e-13, 0.01)
verifie("ex12 poids (N)", m12 * 9.81, 6.2e-12, 0.01)
verifie("ex12 force électrique (N)", 2.0e-14 * 1.0e6, 2.0e-8)
verifie("ex12 rapport (avec le poids arrondi à 6,2e-12 N)", 2.0e-8 / 6.2e-12, 3.2e3, 0.01)
verifie("ex12 nombre de charges élémentaires", 2.0e-14 / E, 1.25e5)
# Exercice 13 : géostationnaire
g13 = G * MT / (RT + 35786e3) ** 2
verifie("ex13 rayon de l'orbite (km)", (RT + 35786e3) / 1000, 42156)
verifie("ex13 champ (N/kg)", g13, 0.224)
verifie("ex13 force sur 3000 kg (N)", 3000 * g13, 672, 0.004)
verifie("ex13 poids au sol (N)", 3000 * 9.81, 2.94e4)
verifie("ex13 rapport poids au sol / force en orbite", 3000 * 9.81 / (3000 * g13), 44, 0.01)
verifie("ex13 champ par g0 (RT / d)^2 (N/kg)", 9.81 * (6370 / 42156) ** 2, 0.224)
# Exercice 14 : Millikan
E14 = 600 / 1.0e-2
q14 = 2.94e-15 * 9.81 / E14
verifie("ex14 champ (V/m)", E14, 6.0e4)
verifie("ex14 charge (C)", q14, 4.81e-19)
verifie("ex14 nombre de charges élémentaires", q14 / E, 3.0, 0.005)
# Exercice 15 : masse de la Terre
M15 = 9.81 * RT ** 2 / G
verifie("ex15 masse de la Terre (kg)", M15, 5.97e24)
verifie("ex15 volume de la Terre (m3)", 4 / 3 * math.pi * RT ** 3, 1.08e21)
verifie("ex15 masse volumique moyenne (kg/m3)", M15 / (4 / 3 * math.pi * RT ** 3), 5.51e3)
verifie("ex15 rapport avec les roches de surface", 5.51e3 / 2.7e3, 2.0, 0.025)
# Défi D11 : deux protons dans un noyau
d = 2.0e-15
Fe11 = K * E ** 2 / d ** 2
Fg11 = G * MP ** 2 / d ** 2
verifie("D11 force électrostatique (N)", Fe11, 57.6)
verifie("D11 force de gravitation (N)", Fg11, 4.65e-35)
verifie("D11 poids d'un proton (N)", MP * 9.81, 1.64e-26)
verifie("D11 rapport électrostatique / gravitation", Fe11 / Fg11, 1.24e36)
verifie("D11 poids d'un proton / gravitation", MP * 9.81 / Fg11, 3.5e8, 0.01)
verifie("D11 masse sur Terre de poids 57,6 N (kg)", Fe11 / 9.81, 5.9, 0.01)
verifie("D11 distance pour 1 N (m)", math.sqrt(K * E ** 2 / 1.0), 1.52e-14)
verifie("D11 rapport des distances", math.sqrt(K * E ** 2 / 1.0) / d, 7.6)


def programme_d11():
    k, G_, e, mp = 9.0e9, 6.67e-11, 1.60e-19, 1.67e-27
    for d_ in [2.0e-15, 1.0e-10, 1.0]:
        Fe = k * e**2 / d_**2
        Fg = G_ * mp**2 / d_**2
        print('d =', d_, 'm : Fe/Fg =', f'{Fe / Fg:.3g}')


s = sortie_de(programme_d11)
print('   D11 programme :', s.replace('\n', ' | '))
if s != ('d = 2e-15 m : Fe/Fg = 1.24e+36\nd = 1e-10 m : Fe/Fg = 1.24e+36\n'
         'd = 1.0 m : Fe/Fg = 1.24e+36'):
    ECHECS.append('D11 programme')

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs et sorties du chapitre 11 et du défi D11 sont vérifiées.")
