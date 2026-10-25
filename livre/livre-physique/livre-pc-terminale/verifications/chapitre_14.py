"""Vérification des résultats numériques du chapitre 14 (deuxième loi de Newton) et du défi D14.

Lancer : python -I -X utf8 verifications/chapitre_14.py
"""
import io
from contextlib import redirect_stdout
from math import cos, radians, sin, sqrt, tanh

ECHECS = []
G = 9.81


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
verifie("cours ascenseur N (N)", 70 * (G + 1.5), 792, 0.5)
verifie("cours ascenseur affichage (kg)", 70 * (G + 1.5) / G, 80.7, 0.05)
verifie("figure ascenseur poids (N)", 70 * G, 687, 0.5)
verifie("cours plan incliné a", G * sin(radians(20)), 3.36, 0.005)


def programme_cours():
    m, g, k, dt = 80, 9.81, 0.27, 0.1
    v, t = 0, 0
    while t < 30:
        a = g - k * v ** 2 / m
        v = v + a * dt
        t = t + dt
    print(round(v, 1))


s = sortie_de(programme_cours)
print('   cours programme :', s)
if s != '53.9':
    ECHECS.append('cours programme')
vl = sqrt(80 * G / 0.27)
verifie("cours vitesse limite", vl, 53.9, 0.05)
verifie("figure : modèle tanh à 30 s", vl * tanh(G * 30 / vl), 53.9, 0.05)
# Exercice 1
verifie("ex1 m1 d1 = m2 d2", 3.0 * 10 - 1.0 * 30, 0, 1e-9)
# Exercice 3
verifie("ex3 a", 1.9 / 19, 0.10, 1e-9)
verifie("ex3 durée", 2.0 / 0.10, 20, 1e-9)
verifie("ex3 distance", 2.0 * 20 - 0.5 * 0.10 * 400, 20, 1e-9)
# Exercice 4
verifie("ex4 N démarrage", 60 * (G + 1.2), 661, 0.5)
verifie("ex4 affichage démarrage", 60 * (G + 1.2) / G, 67, 0.5)
verifie("ex4 N arrêt", 60 * (G - 1.2), 517, 0.5)
verifie("ex4 affichage arrêt", 60 * (G - 1.2) / G, 53, 0.5)
# Exercice 5
verifie("ex5 frottement", 90 * G, 883, 0.5)
verifie("ex5 tension", 12 * G, 118, 0.5)
# Exercice 6
a6 = G * sin(radians(20)) - 120 / 75
verifie("ex6 g sin alpha", G * sin(radians(20)), 3.36, 0.005)
verifie("ex6 a", a6, 1.76, 0.005)
verifie("ex6 v(8 s)", a6 * 8, 14, 0.05)
verifie("ex6 d(8 s)", 0.5 * a6 * 64, 56, 0.5)
verifie("ex6 N", 75 * G * cos(radians(20)), 691, 0.5)
# Exercice 7
a7 = 100 / 3.6 / 9.0
verifie("ex7 a", a7, 3.1, 0.05)
verifie("ex7 F", 1300 * a7, 4.0e3, 0.05e3)
verifie("ex7 force en virage", 1300 * 10 ** 2 / 25, 5.2e3, 1e-6)
# Exercice 8
a8 = 1.3e7 / 7.8e5 - G
verifie("ex8 a", a8, 6.9, 0.05)
verifie("ex8 v(10 s)", 10 * a8, 69, 0.5)
verifie("ex8 h(10 s)", 50 * a8, 3.4e2, 5)
# Exercice 9


def programme_ex9():
    m, g, k, Pi = 8.4e-3, 9.81, 0.169, 0.0133
    dt, v = 0.005, 0.0
    for n in range(1, 61):
        a = g - Pi / m - k * v / m
        v = v + a * dt
        if n % 20 == 0:
            print(round(n * dt, 2), round(v, 3))


s = sortie_de(programme_ex9).splitlines()
print('   ex9 sorties :', s)
if s != ['0.1 0.36', '0.2 0.403', '0.3 0.408']:
    ECHECS.append('ex9 sorties')
verifie("ex9 a initiale", G - 0.0133 / 8.4e-3, 8.2, 0.05)
verifie("ex9 vitesse limite", (8.4e-3 * G - 0.0133) / 0.169, 0.409, 0.0005)
verifie("ex9 temps caractéristique", 8.4e-3 / 0.169, 0.05, 0.001)
# Exercice 10
verifie("ex10 vmax sèche (km/h)", 3.6 * sqrt(0.80 * G * 50), 71, 0.5)
verifie("ex10 vmax sèche (m/s)", sqrt(0.80 * G * 50), 19.8, 0.05)
verifie("ex10 vmax mouillée (km/h)", 3.6 * sqrt(0.40 * G * 50), 50, 0.5)
# Exercice 11
verifie("ex11 vA", 50 * 2.4 / 80, 1.5, 1e-9)
verifie("ex11 xG", (80 * (-3.0) + 50 * 4.8) / 130, 0, 1e-9)
# Exercice 12
gb = 9.7
v12 = 1357.6 / 3.6
verifie("ex12 v max (m/s)", v12, 377, 0.5)
verifie("ex12 durée", v12 / gb, 39, 0.5)
verifie("ex12 hauteur (km)", 0.5 * gb * (v12 / gb) ** 2 / 1000, 7.3, 0.05)
verifie("ex12 rho", 2 * 118 * gb / (0.80 * v12 ** 2), 0.020, 0.0005)
# Exercice 13
verifie("ex13 vmax", 0.80 * 2.0, 1.6, 1e-9)
verifie("ex13 hauteur", 1.6 + 1.6 * 8.0 + 1.6, 16, 1e-9)
for a, n in ((0.8, 690), (0, 638), (-0.8, 586)):
    verifie(f"ex13 N pour a = {a}", 65 * (G + a), n, 0.5)
# Exercice 14
al, be = radians(15), radians(25)
verifie("ex14 m g sin alpha", 70 * G * sin(al), 177.7, 0.05)
T = (70 * G * sin(al) + 60) / cos(be)
verifie("ex14 T", T, 262, 0.5)
verifie("ex14 N", 70 * G * cos(al) - T * sin(be), 552, 0.5)
verifie("ex14 T au départ", (70 * 1.25 + 70 * G * sin(al) + 60) / cos(be), 359, 0.5)
# Exercice 15
a15 = 27 ** 2 / 1.9
verifie("ex15 a", a15, 384, 0.5)
verifie("ex15 T", 7.26 * a15, 2.8e3, 0.05e3)
verifie("ex15 poids du marteau", 7.26 * G, 71, 0.5)
verifie("ex15 poids du lanceur", 110 * G, 1.08e3, 0.005e3)
verifie("ex15 rapport", 7.26 * a15 / (110 * G), 2.6, 0.05)
# Défi D14


def programme_d14():
    g, R = 9.81, 6.0
    for h in (12.0, 15.0, 18.0):
        v2_haut = 2 * g * (h - 2 * R)
        n_haut = v2_haut / (g * R) - 1
        n_bas = 1 + 2 * h / R
        print(h, round(n_haut, 2), round(n_bas, 2))


s = sortie_de(programme_d14).splitlines()
print('   D14 sorties :', s)
if s != ['12.0 -1.0 5.0', '15.0 0.0 6.0', '18.0 1.0 7.0']:
    ECHECS.append('D14 sorties')
verifie("D14 hauteur minimale", 2.5 * 6.0, 15, 1e-9)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 14 et du défi D14 sont vérifiées.")
