"""Vérification des résultats numériques du chapitre 16 (mouvement dans un champ de gravitation) et du défi D16.

Lancer : python -I -X utf8 verifications/chapitre_16.py
"""
import io
from contextlib import redirect_stdout
from math import cos, pi, radians, sin, sqrt

ECHECS = []
G = 6.67e-11
MT = 5.97e24
RT = 6.371e6
GM_COURS = G * MT          # 3,98e14
GM = 3.98e14               # valeur donnée dans les exercices


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


def orbite(r, gm=GM):
    v = sqrt(gm / r)
    return v, 2 * pi * r / v


# L'essentiel
verifie("cours g au sol", GM_COURS / RT ** 2, 9.81, 0.005)
verifie("cours g à 420 km", GM_COURS / (RT + 420e3) ** 2, 8.6, 0.05)
v, T = orbite(6.791e6, GM_COURS)
verifie("cours ISS v", v, 7.66e3, 0.005e3)
verifie("cours ISS T (s)", T, 5.57e3, 0.005e3)
verifie("cours ISS T (min)", T / 60, 92.9, 0.05)
verifie("cours rayon géostationnaire", (GM_COURS * 86164 ** 2 / (4 * pi ** 2)) ** (1 / 3), 4.215e7, 0.0005e7)
verifie("cours altitude géostationnaire (km)", ((GM_COURS * 86164 ** 2 / (4 * pi ** 2)) ** (1 / 3) - RT) / 1000, 35800, 30)
verifie("cours rapport g(420 km)/g(sol) (%)", 100 * RT ** 2 / (RT + 420e3) ** 2, 88, 0.5)


def programme_cours():
    planetes = {"Mercure": (0.387, 0.241), "Vénus": (0.723, 0.615), "Terre": (1.000, 1.000),
                "Mars": (1.524, 1.881), "Jupiter": (5.203, 11.86), "Saturne": (9.537, 29.45)}
    for nom, (a, T) in planetes.items():
        print(nom, round(T ** 2 / a ** 3, 3))


s = sortie_de(programme_cours).splitlines()
print('   cours programme :', s)
if s != ['Mercure 1.002', 'Vénus 1.001', 'Terre 1.0', 'Mars 1.0', 'Jupiter 0.999', 'Saturne 1.0']:
    ECHECS.append('cours programme Kepler')
verifie("cours masse du Soleil", 4 * pi ** 2 * 1.496e11 ** 3 / (G * 3.156e7 ** 2), 1.99e30, 0.005e30)
# Activité expérimentale : Europe
verifie("activité rayon d'Europe (m)", 9.39 * 71492e3, 6.71e8, 0.005e8)
verifie("activité masse de Jupiter", 4 * pi ** 2 * 6.71e8 ** 3 / (G * (3.551 * 86400) ** 2), 1.90e27, 0.005e27)
for t, x in ((0, 6.2), (1, 5.6), (2, -8.3), (3, -2.5), (4, 9.3), (5, -1.0), (6, -9.0), (7, 4.8)):
    verifie(f"figure Europe : point t = {t} j", 9.39 * sin(2 * pi * (t + 0.4) / 3.551), x, 0.25)
verifie("figure Europe : premier minimum (j)", 0.75 * 3.551 - 0.4, 2.263, 0.001)
# Exercice 1
F = G * MT * 7.35e22 / 3.84e8 ** 2
verifie("ex1 F", F, 1.98e20, 0.005e20)
verifie("ex1 aL", F / 7.35e22, 2.70e-3, 0.005e-3)
verifie("ex1 gL", G * 7.35e22 / 1.737e6 ** 2, 1.62, 0.005)
# Exercice 2
v, T = orbite(RT + 550e3)
verifie("ex2 v", v, 7.58e3, 0.005e3)
verifie("ex2 T (s)", T, 5.73e3, 0.005e3)
verifie("ex2 T (min)", T / 60, 95.6, 0.05)
# Exercice 4
r4 = (GM * 86164 ** 2 / (4 * pi ** 2)) ** (1 / 3)
verifie("ex4 r", r4, 4.21e7, 0.005e7)
verifie("ex4 altitude (km)", (r4 - RT) / 1000, 35800, 50)
verifie("ex4 v", 2 * pi * r4 / 86164, 3.07e3, 0.005e3)
# Exercice 5
MJ = 4 * pi ** 2 * 4.22e8 ** 3 / (G * (1.769 * 86400) ** 2)
verifie("ex5 T (s)", 1.769 * 86400, 1.528e5, 0.0005e5)
verifie("ex5 MJ", MJ, 1.90e27, 0.005e27)
verifie("ex5 MJ/MT", MJ / MT, 319, 0.5)
# Exercice 6
verifie("ex6 vA", 54.5 * 0.586 / 35.1, 0.91, 0.005)
a6 = (0.586 + 35.1) / 2
verifie("ex6 a", a6, 17.8, 0.05)
verifie("ex6 T", a6 ** 1.5, 75.4, 0.05)
verifie("ex6 retour", 1986 + a6 ** 1.5, 2061, 1)
# Exercice 8
verifie("ex8 MT", 4 * pi ** 2 * 3.844e8 ** 3 / (G * (27.32 * 86400) ** 2), 6.03e24, 0.005e24)
# Exercice 9
v, T = orbite(RT + 20200e3)
verifie("ex9 T (s)", T, 4.31e4, 0.005e4)
verifie("ex9 T (h)", T / 3600, 11.98, 0.01)
verifie("ex9 v", v, 3.87e3, 0.005e3)
# Exercice 10
v, T = orbite(RT + 786e3)
verifie("ex10 T (s)", T, 6.03e3, 0.005e3)
verifie("ex10 T (min)", T / 60, 100.5, 0.05)
verifie("ex10 tours", 86400 / T, 14.3, 0.05)
# Exercice 11
v1 = sqrt(GM / RT)
ve = 2 * pi * RT / 86164
verifie("ex11 v1", v1, 7.90e3, 0.005e3)
verifie("ex11 rotation à l'équateur", ve, 465, 0.5)
verifie("ex11 Kourou", ve * cos(radians(5.2)), 463, 0.5)
verifie("ex11 Baïkonour", ve * cos(radians(46)), 323, 0.5)
verifie("ex11 Kourou (%)", 100 * ve * cos(radians(5.2)) / v1, 5.9, 0.05)
verifie("ex11 Baïkonour (%)", 100 * ve * cos(radians(46)) / v1, 4.1, 0.05)
# Exercice 12
v, T = orbite(RT + 540e3)
verifie("ex12 v", v, 7.59e3, 0.005e3)
verifie("ex12 T (min)", T / 60, 95.4, 0.05)
verifie("ex12 a", v ** 2 / (RT + 540e3), 8.3, 0.05)
v, T = orbite(RT + 500e3)
verifie("ex12 v à 500 km", v, 7.61e3, 0.005e3)
verifie("ex12 T à 500 km (min)", T / 60, 94.5, 0.05)
# Exercice 13
verifie("ex13 masse de Mars (Phobos)", 4 * pi ** 2 * 9.376e6 ** 3 / (G * (7.66 * 3600) ** 2), 6.42e23, 0.005e23)
verifie("ex13 masse de Mars (Deimos)", 4 * pi ** 2 * 2.3463e7 ** 3 / (G * (30.3 * 3600) ** 2), 6.43e23, 0.005e23)
verifie("ex13 orbite synchrone (km)", (G * 6.42e23 * (24.6 * 3600) ** 2 / (4 * pi ** 2)) ** (1 / 3) / 1000, 2.04e4, 0.005e4)
# Exercice 14
for nom, a, t in (("b", 0.01154, 1.511), ("e", 0.02925, 6.100), ("h", 0.06189, 18.77)):
    ty = t / 365.25
    verifie(f"ex14 T²/a³ pour {nom}", ty ** 2 / a ** 3, 11.1, 0.05)
verifie("ex14 masse de l'étoile", 1 / 11.1, 0.090, 0.001)
verifie("ex14 rapport des distances", 1 / 0.02925, 34, 0.5)
# Exercice 15
r1, r2 = 6.671e6, 4.215e7
verifie("ex15 v1", sqrt(GM / r1), 7.72e3, 0.005e3)
verifie("ex15 v2", sqrt(GM / r2), 3.07e3, 0.005e3)
a15 = (r1 + r2) / 2
verifie("ex15 a (km)", a15 / 1000, 2.44e4, 0.005e4)
T15 = 2 * pi * sqrt(a15 ** 3 / GM)
verifie("ex15 période de l'ellipse", T15, 3.80e4, 0.005e4)
verifie("ex15 durée du transfert (h)", T15 / 2 / 3600, 5.3, 0.05)
verifie("figure ex15 : demi-petit axe (cm)", sqrt(0.6671 * 4.215), 1.677, 0.001)
# Défi D16


def programme_d16():
    etoiles = {"S2": (1031, 16.05), "S38": (1169, 19.2), "S55": (889, 12.8)}
    for nom, (a, T) in etoiles.items():
        M = a ** 3 / T ** 2
        print(nom, round(M / 1e6, 2))


s = sortie_de(programme_d16).splitlines()
print('   D16 sorties :', s)
if s != ['S2 4.25', 'S38 4.33', 'S55 4.29']:
    ECHECS.append('D16 sorties')
M = 1031 ** 3 / 16.05 ** 2 * 1.99e30
verifie("D16 masse (kg)", M, 8.5e36, 0.05e36)
RS = 2 * G * M / 3.00e8 ** 2
verifie("D16 rayon (m)", RS, 1.25e10, 0.005e10)
verifie("D16 rayon (ua)", RS / 1.496e11, 0.084, 0.0005)
rp = 1031 * (1 - 0.886)
verifie("D16 distance minimale (ua)", rp, 118, 0.5)
verifie("D16 rapport à RS", rp * 1.496e11 / RS, 1400, 10)
verifie("D16 rapport des vitesses", 1.886 / 0.114, 16.5, 0.05)
verifie("D16 vitesse minimale (km/s)", 7650 / (1.886 / 0.114), 460, 5)
verifie("D16 fraction de c (%)", 100 * 7650e3 / 3.00e8, 2.5, 0.05)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 16 et du défi D16 sont vérifiées.")
