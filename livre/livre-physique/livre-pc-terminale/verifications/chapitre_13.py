"""Vérification des résultats numériques du chapitre 13 (décrire un mouvement) et du défi D13.

Lancer : python -I -X utf8 verifications/chapitre_13.py
"""
import io
from contextlib import redirect_stdout
from math import atan, cos, degrees, pi, sin, sqrt

ECHECS = []


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
verifie("cours v à 0,50 s", sqrt(5.0 ** 2 + (-9.8 * 0.50 + 8.7) ** 2), 6.3, 0.05)
verifie("cours vy à 0,50 s", -9.8 * 0.50 + 8.7, 3.8, 1e-9)
tf = 25 / 8.0
verifie("cours durée de freinage (s)", tf, 3.1, 0.05)
verifie("cours distance de freinage (m)", 25 * tf - 0.5 * 8.0 * tf ** 2, 39, 0.5)
v = 2 * pi * 0.10 * 50
verifie("cours centrifugeuse v (m/s)", v, 31, 0.5)
verifie("cours centrifugeuse a (m/s2)", v * v / 0.10, 9.9e3, 0.05e3)
# données du pointage : x = 1,20 t et y = 1,90 t - 4,9 t², arrondies au mm
tau = 0.040
for k, (xp, yp) in enumerate(zip([0.000, 0.048, 0.096, 0.144, 0.192, 0.240, 0.288],
                                 [0.000, 0.068, 0.121, 0.157, 0.179, 0.184, 0.174])):
    t = k * tau
    verifie(f"cours pointage x{k}", 1.20 * t, xp, 0.0005)
    verifie(f"cours pointage y{k}", 1.90 * t - 4.9 * t * t, yp, 0.0005)


def programme_cours():
    x = [0.000, 0.048, 0.096, 0.144, 0.192, 0.240, 0.288]
    y = [0.000, 0.068, 0.121, 0.157, 0.179, 0.184, 0.174]
    vx = [(x[i + 1] - x[i - 1]) / (2 * tau) for i in range(1, 6)]
    vy = [(y[i + 1] - y[i - 1]) / (2 * tau) for i in range(1, 6)]
    ay = [(vy[i + 1] - vy[i - 1]) / (2 * tau) for i in range(1, 4)]
    print([round(a, 1) for a in ay])
    # vecteurs de la figure : v2, v4, a3
    print(vx[1], vy[1], vx[3], vy[3])


s = sortie_de(programme_cours).splitlines()
print('   cours programme :', s[0])
if s[0] != '[-9.8, -9.7, -9.8]':
    ECHECS.append('cours programme')
vx2, vy2, vx4, vy4 = (float(u) for u in s[1].split())
verifie("figure v2 x (échelle 1 m/s = 0,05)", 0.05 * vx2, 0.060, 1e-9)
verifie("figure v2 y", 0.05 * vy2, 0.0556, 0.0001)
verifie("figure v4 y", 0.05 * vy4, 0.0169, 0.0001)
verifie("figure a3 (échelle 1 m/s2 = 0,01)", 0.01 * (vy4 - vy2) / (2 * tau), -0.0969, 0.0001)
# Exercice 1
verifie("ex1 v(0)", sqrt(3.0 ** 2 + 4.0 ** 2), 5.0, 1e-9)
# Exercice 2
verifie("ex2 vA", 0.60 / 0.20, 3.0, 1e-9)
verifie("ex2 v2", (0.40 + 0.60) / 0.40, 2.5, 1e-9)
verifie("ex2 v4", (0.80 + 1.00) / 0.40, 4.5, 1e-9)
verifie("ex2 a3", (4.5 - 2.5) / 0.40, 5.0, 1e-9)
# Exercice 4
v4 = 2 * pi * 8.0 / 6.0
verifie("ex4 v", v4, 8.4, 0.05)
verifie("ex4 a", v4 ** 2 / 8.0, 8.8, 0.05)
verifie("ex4 a/g", v4 ** 2 / 8.0 / 9.8, 0.9, 0.01)
# Exercice 5
verifie("ex5 an", 144 / 50, 2.9, 0.05)
verifie("ex5 a", sqrt(1.5 ** 2 + (144 / 50) ** 2), 3.2, 0.05)
# Exercice 6
verifie("ex6 a", 11.6 / 4.0, 2.9, 1e-9)
verifie("ex6 distance", 0.5 * 2.9 * 16, 23.2, 1e-9)
verifie("ex6 temps restant", 76.8 / 11.6, 6.6, 0.05)
verifie("ex6 temps total", 4 + 76.8 / 11.6, 10.6, 0.05)
# Exercice 7
verifie("ex7 durée de freinage", 25 / 7.5, 3.3, 0.05)
verifie("ex7 distance de freinage sèche", 625 / 15, 42, 0.5)
verifie("ex7 arrêt sèche", 25 + 625 / 15, 67, 0.5)
verifie("ex7 freinage mouillé", 625 / 8, 78, 0.5)
verifie("ex7 arrêt mouillé", 25 + 625 / 8, 103, 0.5)
# Exercice 8 : données y = 4,905 t² arrondies au mm et sortie
for k, yp in enumerate([0.000, 0.012, 0.049, 0.110, 0.196, 0.307, 0.441]):
    verifie(f"ex8 donnée y{k}", 4.905 * (k * 0.050) ** 2, yp, 0.0005)


def programme_ex8():
    y = [0.000, 0.012, 0.049, 0.110, 0.196, 0.307, 0.441]
    v = [(y[i + 1] - y[i - 1]) / (2 * 0.050) for i in range(1, 6)]
    print([round(vi, 2) for vi in v])


s = sortie_de(programme_ex8)
print('   ex8 sortie :', s)
if s != '[0.49, 0.98, 1.47, 1.97, 2.45]':
    ECHECS.append('ex8 sortie')
verifie("ex8 a", 0.49 / 0.050, 9.8, 1e-9)
# Exercice 9
verifie("ex9 at", 5.0 / 4.0, 1.25, 1e-9)
verifie("ex9 an", 64 / 20, 3.2, 1e-9)
verifie("ex9 a", sqrt(1.25 ** 2 + 3.2 ** 2), 3.4, 0.05)
verifie("ex9 angle", degrees(atan(1.25 / 3.2)), 21, 0.5)
# Exercice 10
r = 6.791e6
v10 = 2 * pi * r / (92.8 * 60)
verifie("ex10 v (m/s)", v10, 7.66e3, 0.005e3)
verifie("ex10 v (km/h)", v10 * 3.6, 27600, 50)
verifie("ex10 a", v10 ** 2 / r, 8.65, 0.005)
verifie("ex10 tours par jour", 1440 / 92.8, 15.5, 0.05)
verifie("ex10 rapport a/g (%)", 100 * v10 ** 2 / r / 9.81, 88, 0.5)
# Exercice 11


def programme_ex11():
    R, T, tau = 2.0, 4.0, 0.1

    def x(t): return R * cos(2 * pi * t / T)

    def y(t): return R * sin(2 * pi * t / T)
    t = 0.5
    ax = (x(t + tau) - 2 * x(t) + x(t - tau)) / tau ** 2
    ay = (y(t + tau) - 2 * y(t) + y(t - tau)) / tau ** 2
    print(round(ax, 3), round(ay, 3))


s = sortie_de(programme_ex11)
print('   ex11 sortie :', s)
if s != '-3.482 -3.482':
    ECHECS.append('ex11 sortie')
verifie("ex11 position", 2.0 * cos(pi / 4), 1.41, 0.005)
verifie("ex11 norme calculée", sqrt(2) * 3.482, 4.92, 0.005)
verifie("ex11 v²/R", 2.0 * (2 * pi / 4.0) ** 2, 4.93, 0.005)
# Exercice 12
g = 9.81
v12 = sqrt(8 * g * 7.6)
verifie("ex12 v", v12, 24, 0.5)
verifie("ex12 tours par minute", 60 * v12 / (2 * pi * 7.6), 31, 0.5)
verifie("ex12 at", v12 / 20, 1.2, 0.05)
an = (v12 / 2) ** 2 / 7.6
verifie("ex12 an à mi-parcours", an, 19.6, 0.05)
verifie("ex12 a à mi-parcours", sqrt(an ** 2 + (v12 / 20) ** 2), 19.7, 0.05)
verifie("ex12 angle", degrees(atan((v12 / 20) / an)), 3.6, 0.05)
# Exercice 13
verifie("ex13 v0", sqrt(4.78 ** 2 + 5.70 ** 2), 7.44, 0.005)
verifie("ex13 angle", degrees(atan(5.70 / 4.78)), 50, 0.5)
ts = 5.70 / 9.80
verifie("ex13 date du sommet", ts, 0.582, 0.0005)
verifie("ex13 hauteur max", -4.90 * ts ** 2 + 5.70 * ts + 2.10, 3.76, 0.005)
tp = 4.60 / 4.78
verifie("ex13 date au panier", tp, 0.962, 0.0005)
verifie("ex13 hauteur au panier", -4.90 * tp ** 2 + 5.70 * tp + 2.10, 3.05, 0.005)
# Exercice 14
verifie("ex14 aA", 22 ** 2 / 15, 32, 0.5)
verifie("ex14 aA/g", 22 ** 2 / 15 / 9.8, 3.3, 0.05)
verifie("ex14 aB", 12 ** 2 / 8.0, 18, 1e-9)
verifie("ex14 aB/g", 18 / 9.8, 1.8, 0.05)
verifie("ex14 boucle circulaire", 22 ** 2 / 8.0, 60, 0.6)
verifie("ex14 boucle circulaire / g", 22 ** 2 / 8.0 / 9.8, 6.2, 0.05)
# Exercice 15
v15 = 320 / 3.6
an15 = v15 ** 2 / 7000
verifie("ex15 an", an15, 1.1, 0.05)
verifie("ex15 vitesse sur ligne classique (km/h)", 3.6 * sqrt(an15 * 1200), 130, 3)
af = v15 ** 2 / (2 * 3300)
verifie("ex15 décélération", af, 1.2, 0.05)
verifie("ex15 durée", v15 / af, 74, 0.5)
verifie("ex15 rapport à g", af / 9.8, 0.12, 0.005)
# Défi D13


def programme_d13():
    R, V = 0.35, 8.0
    w = V / R
    for t in (0.00, 0.05, 0.10):
        ax = R * w ** 2 * sin(w * t)
        ay = R * w ** 2 * cos(w * t)
        print(t, round(sqrt(ax ** 2 + ay ** 2)))


s = sortie_de(programme_d13).splitlines()
print('   D13 sorties :', s)
if s != ['0.0 183', '0.05 183', '0.1 183']:
    ECHECS.append('D13 sorties')
verifie("D13 vitesse au sommet", 2 * 8.0, 16, 1e-9)
verifie("D13 a en multiples de g", 8.0 ** 2 / 0.35 / 9.81, 19, 0.5)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 13 et du défi D13 sont vérifiées.")
