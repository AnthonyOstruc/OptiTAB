"""Vérification des résultats numériques du chapitre 15 (mouvement dans un champ uniforme) et du défi D15.

Lancer : python -I -X utf8 verifications/chapitre_15.py
"""
import io
from contextlib import redirect_stdout
from math import atan, cos, degrees, pi, radians, sin, sqrt, tan

ECHECS = []
G = 9.81
E_CH, M_E, M_P = 1.60e-19, 9.11e-31, 1.67e-27


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


def vol(v0, alpha, h):
    vx, vz = v0 * cos(radians(alpha)), v0 * sin(radians(alpha))
    t = (vz + sqrt(vz * vz + 2 * G * h)) / G
    return t, vx * t


# L'essentiel : pétanque
verifie("cours date du sommet", 7.0 * sin(radians(40)) / G, 0.46, 0.005)
verifie("cours flèche", 1.0 + (7.0 * sin(radians(40))) ** 2 / (2 * G), 2.0, 0.05)
t, d = vol(7.0, 40, 1.0)
verifie("cours durée du vol", t, 1.10, 0.005)
verifie("cours portée", d, 5.9, 0.05)
verifie("figure : coefficient de la parabole", G / (2 * 49 * cos(radians(40)) ** 2), 0.1705, 0.0005)
verifie("figure : tan alpha", tan(radians(40)), 0.8391, 0.0001)
verifie("figure : abscisse du sommet", 7.0 * cos(radians(40)) * 7.0 * sin(radians(40)) / G, 2.461, 0.002)
# électron dans 1e4 V/m
verifie("cours force électrique", 1.6e-19 * 1e4, 1.6e-15, 1e-20)
verifie("cours poids de l'électron", M_E * G, 8.9e-30, 0.05e-30)
verifie("cours électron 2 kV : Ec", 1.6e-19 * 2000, 3.2e-16, 1e-20)
verifie("cours électron 2 kV : v", sqrt(2 * 1.6e-19 * 2000 / M_E), 2.7e7, 0.05e7)
# données de la balle de tennis : x = 3,0 t ; z = 1,0 + 4,0 t - 4,905 t², arrondies au mm
for k, (xp, zp) in enumerate(zip([0.000, 0.120, 0.240, 0.360, 0.480, 0.600, 0.720],
                                 [1.000, 1.152, 1.289, 1.409, 1.514, 1.604, 1.677])):
    t = 0.040 * k
    verifie(f"cours pointage x{k}", 3.0 * t, xp, 0.0005)
    verifie(f"cours pointage z{k}", 1.0 + 4.0 * t - 4.905 * t * t, zp, 0.0005)


def programme_cours():
    m, g, tau = 0.058, 9.81, 0.040
    x = [0.000, 0.120, 0.240, 0.360, 0.480, 0.600, 0.720]
    z = [1.000, 1.152, 1.289, 1.409, 1.514, 1.604, 1.677]
    for i in range(1, 6):
        vx = (x[i + 1] - x[i - 1]) / (2 * tau)
        vz = (z[i + 1] - z[i - 1]) / (2 * tau)
        Ec = 0.5 * m * (vx ** 2 + vz ** 2)
        Ep = m * g * z[i]
        print(round(Ec, 2), round(Ep, 2), round(Ec + Ep, 2))


s = sortie_de(programme_cours).splitlines()
print('   cours programme :', s)
if s != ['0.64 0.66 1.29', '0.56 0.73 1.29', '0.49 0.8 1.29', '0.43 0.86 1.29', '0.38 0.91 1.29']:
    ECHECS.append('cours programme énergies')
verifie("cours énergie mécanique théorique", 0.058 * (0.5 * 25 + G * 1.0), 1.29, 0.005)
# Exercice 1
verifie("ex1 durée", sqrt(40 / G), 2.0, 0.05)
verifie("ex1 vitesse", sqrt(2 * G * 20), 19.8, 0.05)
# Exercice 2
verifie("ex2 E", 500 / 0.020, 2.5e4, 1e-9)
verifie("ex2 F", E_CH * 2.5e4, 4.0e-15, 1e-20)
verifie("ex2 P", M_E * G, 8.9e-30, 0.05e-30)
# Exercice 3
t3 = sqrt(2 * 0.80 / G)
verifie("ex3 durée", t3, 0.40, 0.005)
verifie("ex3 distance", 2.5 * t3, 1.0, 0.05)
verifie("ex3 vz", G * t3, 3.96, 0.005)
verifie("ex3 v", sqrt(2.5 ** 2 + (G * t3) ** 2), 4.7, 0.05)
# Exercice 4
Em = 0.5 * 0.20 * 64 + 0.20 * G * 1.5
verifie("ex4 Ep", 0.20 * G * 1.5, 2.9, 0.05)
verifie("ex4 Em", Em, 9.3, 0.05)
verifie("ex4 altitude max", Em / (0.20 * G), 4.8, 0.05)
verifie("ex4 vitesse au sol", sqrt(2 * Em / 0.20), 9.7, 0.05)
# Exercice 5
verifie("ex5 Ec", E_CH * 1000, 1.60e-16, 1e-21)
verifie("ex5 v", sqrt(2 * E_CH * 1000 / M_E), 1.9e7, 0.05e7)
# Exercice 6
verifie("ex6 vx", 13.5 * cos(radians(42)), 10.0, 0.05)
verifie("ex6 vz", 13.5 * sin(radians(42)), 9.03, 0.005)
verifie("ex6 coefficient", G / (2 * 13.5 ** 2 * cos(radians(42)) ** 2), 0.0487, 0.00005)
verifie("ex6 flèche", 2.10 + (13.5 * sin(radians(42))) ** 2 / (2 * G), 6.3, 0.05)
t6, d6 = vol(13.5, 42, 2.10)
verifie("ex6 durée", t6, 2.05, 0.005)
verifie("ex6 longueur", d6, 20.6, 0.05)
# Exercice 7
a7, x7 = radians(52), 4.20
v07 = sqrt(G * x7 ** 2 / (2 * cos(a7) ** 2 * (x7 * tan(a7) + 2.20 - 3.05)))
verifie("ex7 v0", v07, 7.1, 0.05)
z74 = -G * x7 ** 2 / (2 * 7.4 ** 2 * cos(a7) ** 2) + x7 * tan(a7) + 2.20
verifie("ex7 hauteur avec 7,4 m/s", z74, 3.41, 0.005)
verifie("ex7 écart (cm)", 100 * (z74 - 3.05), 36, 0.5)
# Exercice 8
a8 = E_CH * 1.0e4 / M_E
verifie("ex8 a", a8, 1.76e15, 0.005e15)
verifie("ex8 coefficient", E_CH * 1.0e4 / (2 * M_E * 2.0e7 ** 2), 2.20, 0.005)
verifie("ex8 déviation (mm)", 1000 * 0.5 * a8 * (0.050 / 2.0e7) ** 2, 5.5, 0.05)
verifie("ex8 tan", a8 * 0.050 / 2.0e7 ** 2, 0.22, 0.005)
verifie("ex8 angle", degrees(atan(a8 * 0.050 / 2.0e7 ** 2)), 12, 0.5)
verifie("figure ex8 : coefficient (cm)", 2.195 / 100, 0.0219, 0.0001)
# Exercice 10
verifie("ex10 v sans frottement", sqrt(2 * G * 8.0), 12.5, 0.05)
W10 = 0.5 * 30 * 81 - 30 * G * 8.0
verifie("ex10 travail", W10, -1.1e3, 0.05e3)
verifie("ex10 force", -W10 / 30, 38, 0.5)
# Exercice 11
verifie("ex11 énergie par intervalle (J)", E_CH * 50e3, 8.0e-15, 1e-20)
v1 = sqrt(2 * E_CH * 50e3 / M_P)
v20 = sqrt(2 * 20 * E_CH * 50e3 / M_P)
verifie("ex11 v1", v1, 3.1e6, 0.05e6)
verifie("ex11 v20", v20, 1.4e7, 0.05e7)
verifie("ex11 L1 (cm)", 100 * v1 / (2 * 10e6), 15, 0.5)
verifie("ex11 L20 (cm)", 100 * v20 / (2 * 10e6), 69, 0.5)
# Exercice 12
tn = 11.9 / 45
verifie("ex12 date au filet", tn, 0.264, 0.0005)
verifie("ex12 hauteur au filet", 2.80 - 0.5 * G * tn ** 2, 2.46, 0.005)
tsol = sqrt(2 * 2.80 / G)
verifie("ex12 durée de chute", tsol, 0.756, 0.0005)
verifie("ex12 point de chute", 45 * tsol, 34, 0.5)
verifie("ex12 vitesse maximale", 18.3 / tsol, 24, 0.5)
al = radians(-6.7)
vx, vz = 50 * cos(al), 50 * sin(al)
verifie("ex12 vx", vx, 49.7, 0.05)
verifie("ex12 vz", vz, -5.8, 0.05)
t12 = 18.3 / vx
verifie("ex12 date à 18,3 m", t12, 0.37, 0.005)
verifie("ex12 hauteur à 18,3 m", 2.80 + vz * t12 - 0.5 * G * t12 ** 2, 0, 0.03)
tf = 11.9 / vx
verifie("ex12 hauteur au filet avec l'angle", 2.80 + vz * tf - 0.5 * G * tf ** 2, 1.13, 0.01)
# Exercice 13
a13 = 1.5e-13 * 1.0e6 / 1.0e-10
verifie("ex13 F", 1.5e-13 * 1.0e6, 1.5e-7, 1e-12)
verifie("ex13 P", 1.0e-10 * G, 9.8e-10, 0.05e-10)
verifie("ex13 P/F", 1.0e-10 * G / 1.5e-7, 0.0065, 0.00005)
verifie("ex13 a", a13, 1.5e3, 1e-6)
verifie("ex13 durée", 0.010 / 20, 5.0e-4, 1e-12)
verifie("ex13 y1 (mm)", 1000 * 0.5 * a13 * 5.0e-4 ** 2, 0.19, 0.005)
verifie("ex13 vy", a13 * 5.0e-4, 0.75, 1e-9)
verifie("ex13 déviation supplémentaire, 0,375 arrondi (mm)", 1000 * 0.010 * 0.75 / 20, 0.38, 0.0051)
verifie("ex13 déviation totale (mm)", 1000 * (0.5 * a13 * 5.0e-4 ** 2 + 0.010 * 0.75 / 20), 0.56, 0.005)
# Exercice 14
vx14, vz14 = 9.5 * cos(radians(22)), 9.5 * sin(radians(22))
verifie("ex14 vx", vx14, 8.81, 0.005)
verifie("ex14 vz", vz14, 3.56, 0.005)
verifie("ex14 altitude max", 1.10 + vz14 ** 2 / (2 * G), 1.75, 0.005)
t14 = (vz14 + sqrt(vz14 ** 2 + 2 * G * 0.60)) / G
verifie("ex14 durée", t14, 0.87, 0.005)
verifie("ex14 distance", vx14 * t14, 7.6, 0.05)
verifie("ex14 vitesse à la réception", sqrt(9.5 ** 2 + 2 * G * 0.60), 10.1, 0.05)
# Exercice 15
m15 = 900 * 4 / 3 * pi * (0.80e-6) ** 3
verifie("ex15 masse", m15, 1.93e-15, 0.005e-15)
verifie("ex15 poids", m15 * G, 1.89e-14, 0.005e-14)
q15 = m15 * G * 0.0100 / 394
verifie("ex15 charge", q15, 4.81e-19, 0.005e-19)
verifie("ex15 multiple de e", q15 / 1.602e-19, 3, 0.01)
for q, n in ((3.20e-19, 2), (4.81e-19, 3), (8.00e-19, 5), (6.41e-19, 4)):
    verifie(f"ex15 multiple pour {q:.3g}", q / 1.602e-19, n, 0.01)
# Défi D15


def programme_d15():
    v0, g, h = 13.5, 9.81, 2.10
    meilleur, angle = 0, 0
    for a in range(30, 51):
        vx = v0 * cos(radians(a))
        vz = v0 * sin(radians(a))
        t = (vz + sqrt(vz ** 2 + 2 * g * h)) / g
        if vx * t > meilleur:
            meilleur, angle = vx * t, a
    print(angle, round(meilleur, 2))


s = sortie_de(programme_d15)
print('   D15 sortie :', s)
if s != '42 20.57':
    ECHECS.append('D15 sortie')
verifie("D15 portée depuis le sol à 45°", 13.5 ** 2 / G, 18.6, 0.05)
verifie("D15 longueur à 35°", vol(13.5, 35, 2.10)[1], 20.07, 0.005)
verifie("D15 écart 42°-35°", vol(13.5, 42, 2.10)[1] - vol(13.5, 35, 2.10)[1], 0.5, 0.01)
verifie("D15 gain de 2 % de vitesse (%)", 100 * (1.02 ** 2 - 1), 4, 0.1)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 15 et du défi D15 sont vérifiées.")
