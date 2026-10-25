"""Vérification du chapitre 17 (Ondes mécaniques) et du défi D17.

Lancer : python -I -X utf8 verifications/chapitre_17.py
"""
import io
import math
from contextlib import redirect_stdout

ECHECS = []
G = 9.81


def verifie(nom, calcule, publie, tol_rel=0.006):
    ok = abs(calcule - publie) <= tol_rel * abs(publie) + 1e-12
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:60s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def sortie_de(fonction):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    return tampon.getvalue().strip()


# Cours
verifie("cours retard sur 170 m dans l'air (s)", 170 / 340, 0.50)
verifie("cours longueur d'onde d'un la 440 Hz dans l'air (m)", 340 / 440, 0.773, 0.002)


def programme():
    d = [0.20, 0.40, 0.60, 0.80]                 # m
    tau = [0.59e-3, 1.17e-3, 1.76e-3, 2.36e-3]   # s
    v = [d[i] / tau[i] for i in range(4)]
    print([round(x) for x in v])
    print('moyenne :', round(sum(v) / 4), 'm/s')


s = sortie_de(programme)
print('   cours programme :', s.replace('\n', ' | '))
if s != '[339, 342, 341, 339]\nmoyenne : 340 m/s':
    ECHECS.append('cours programme')
# Exercice 2 : tonnerre
verifie("ex2 distance de l'orage (km)", 340 * 6.0 / 1000, 2.04)
verifie("ex2 durée de trajet de la lumière (s)", 2040 / 3.0e8, 6.8e-6, 0.002)
verifie("ex2 règle des 3 s (km)", 340 * 3 / 1000, 1.02)
# Exercice 3 : corde
verifie("ex3 célérité (m/s)", 1.6 / 0.20, 8.0)
verifie("ex3 date du passage du sommet en M (s)", 0.20 + (4.0 - 3.0) / 8.0, 0.325)
verifie("ex3 durée de la perturbation en un point (s)", 0.80 / 8.0, 0.10)
# Exercice 4 : oscillogramme
verifie("ex4 période (ms)", 4 * 0.5, 2.0)
verifie("ex4 fréquence (Hz)", 1 / 2.0e-3, 500)
verifie("ex4 longueur d'onde dans l'air (m)", 340 / 500, 0.68)
# Exercice 5 : milieu
verifie("ex5 lambda dans l'air (m)", 340 / 440, 0.773, 0.002)
verifie("ex5 lambda dans l'eau (m)", 1500 / 440, 3.41, 0.003)
verifie("ex5 lambda dans l'acier (m)", 5900 / 440, 13.4, 0.003)


# Exercice 6 : simulation
def programme6():
    from math import sin, pi
    A, T, lam = 0.02, 0.50, 1.0
    t = 0.10
    for i in range(9):
        x = 0.25 * i
        y = A * sin(2 * pi * (t / T - x / lam))
        print(x, 'm :', round(y * 100, 1), 'cm')


s6 = sortie_de(programme6)
print('   ex6 programme :', s6.replace('\n', ' | '))
attendu6 = ('0.0 m : 1.9 cm\n0.25 m : -0.6 cm\n0.5 m : -1.9 cm\n0.75 m : 0.6 cm\n1.0 m : 1.9 cm\n'
            '1.25 m : -0.6 cm\n1.5 m : -1.9 cm\n1.75 m : 0.6 cm\n2.0 m : 1.9 cm')
if s6 != attendu6:
    ECHECS.append('ex6 programme')
verifie("ex6 célérité (m/s)", 1.0 / 0.50, 2.0)
verifie("ex6 fréquence (Hz)", 1 / 0.50, 2.0)
# Exercice 7 : séisme
k = 1 / 3.5 - 1 / 6.0
verifie("ex7 coefficient (s/km)", k, 0.119, 0.003)
d7 = 12 / k
verifie("ex7 distance de l'épicentre (km)", d7, 101, 0.003)
verifie("ex7 arrivée des ondes P (s)", d7 / 6.0, 16.8, 0.003)
verifie("ex7 arrivée des ondes S (s)", d7 / 3.5, 28.8, 0.003)
# Exercice 8 : chauve-souris
verifie("ex8 distance de l'insecte (m)", 340 * 0.012 / 2, 2.04)
verifie("ex8 longueur d'onde (mm)", 340 / 40e3 * 1000, 8.5)
# Exercice 9 : ultrasons
verifie("ex9 longueur d'onde (mm)", 85 / 10, 8.5)
verifie("ex9 célérité (m/s)", 8.5e-3 * 40e3, 340)
verifie("ex9 décalage pour 17 cm (ms)", 0.17 / 340 * 1000, 0.50)
# Exercice 10 : houle
verifie("ex10 célérité (m/s)", 100 / 8.0, 12.5)
verifie("ex10 célérité (km/h)", 12.5 * 3.6, 45)
verifie("ex10 durée pour 50 km (h)", 50e3 / 12.5 / 3600, 1.1, 0.02)
# Exercice 11 : double périodicité
verifie("ex11 célérité (m/s)", 0.40 / 0.050, 8.0)
verifie("ex11 fréquence (Hz)", 1 / 0.050, 20)
# Exercice 12 : échographie
verifie("ex12 longueur d'onde (mm)", 1540 / 3.5e6 * 1000, 0.44, 0.003)
verifie("ex12 profondeur (cm)", 1540 * 65e-6 / 2 * 100, 5.0, 0.002)
verifie("ex12 durée pour 15 cm (microsecondes)", 2 * 0.15 / 1540 * 1e6, 195, 0.003)
# Exercice 13 : tsunami
v_large = math.sqrt(G * 4000)
verifie("ex13 célérité au large (m/s)", v_large, 198, 0.002)
verifie("ex13 célérité au large (km/h)", v_large * 3.6, 713, 0.002)
verifie("ex13 durée pour 1000 km (h)", 1e6 / v_large / 3600, 1.4, 0.01)
verifie("ex13 longueur d'onde au large (km)", v_large * 15 * 60 / 1000, 178, 0.003)
v_cote = math.sqrt(G * 10)
verifie("ex13 célérité près de la côte (m/s)", v_cote, 9.9, 0.002)
verifie("ex13 longueur d'onde près de la côte (km)", v_cote * 15 * 60 / 1000, 8.9, 0.003)
# Exercice 14 : puits
a = G / 2 / 340
t1 = (-1 + math.sqrt(1 + 4 * a * 2.5)) / (2 * a)
verifie("ex14 durée de chute (s)", t1, 2.42, 0.003)
verifie("ex14 profondeur (m)", G / 2 * t1 ** 2, 28.6, 0.003)
verifie("ex14 profondeur sans le son (m)", G / 2 * 2.5 ** 2, 30.7, 0.003)
verifie("ex14 erreur relative (%)", (G / 2 * 2.5 ** 2 - G / 2 * t1 ** 2) / (G / 2 * t1 ** 2) * 100, 7, 0.03)
verifie("ex14 durée du trajet du son (s)", G / 2 * t1 ** 2 / 340, 0.084, 0.01)


def programme14():
    g, v, t = 9.81, 340, 2.5
    h_min, h_max = 0, 100
    while h_max - h_min > 0.01:
        h = (h_min + h_max) / 2
        if (2 * h / g) ** 0.5 + h / v > t:
            h_max = h
        else:
            h_min = h
    print(round(h, 1), 'm')


s14 = sortie_de(programme14)
print('   ex14 programme :', s14)
if s14 != '28.6 m':
    ECHECS.append('ex14 programme')
# Exercice 15 : capteur à ultrasons
verifie("ex15 célérité à 20 degrés (m/s)", 331 + 0.6 * 20, 343)
verifie("ex15 célérité à 0 degré (m/s)", 331, 331)
verifie("ex15 distance réelle à 0 degré (m)", 331 * 5.83e-3 / 2, 0.965, 0.002)
verifie("ex15 distance affichée avec 340 m/s (m)", 340 * 5.83e-3 / 2, 0.991, 0.002)
verifie("ex15 erreur relative (%)", (340 - 331) / 331 * 100, 2.7, 0.01)
verifie("ex15 durée de l'écho pour 2,0 m à 20 degrés (ms)", 2 * 2.0 / 343 * 1000, 11.7, 0.004)

# Défi D17 : localiser un séisme
epi = (55, 30)
stations = [(0, 0), (100, 0), (0, 80)]
for (xs, ys), dpub, tpub in zip(stations, [62.7, 54.1, 74.3], [7.46, 6.44, 8.85]):
    d = math.hypot(epi[0] - xs, epi[1] - ys)
    verifie(f"D17 distance à la station ({xs};{ys}) (km)", d, dpub, 0.002)
    verifie(f"D17 retard S-P à la station ({xs};{ys}) (s)", d * k, tpub, 0.002)
verifie("D17 distance déduite de 7,46 s (km)", 7.46 / k, 62.7, 0.002)
verifie("D17 arrivée des ondes P en A (s)", 62.65 / 6.0, 10.4, 0.006)


def programme_d17():
    stations_ = [(0, 0, 7.46), (100, 0, 6.44), (0, 80, 8.85)]
    kk = 1 / 3.5 - 1 / 6.0
    meilleur = None
    for x in range(0, 101):
        for y in range(0, 101):
            e = 0
            for (xs, ys, dt) in stations_:
                d = ((x - xs)**2 + (y - ys)**2) ** 0.5
                e = e + (d - dt / kk) ** 2
            if meilleur is None or e < meilleur[0]:
                meilleur = (e, x, y)
    print('epicentre :', meilleur[1], 'km ;', meilleur[2], 'km')


s17 = sortie_de(programme_d17)
print('   D17 programme :', s17)
if s17 != 'epicentre : 55 km ; 30 km':
    ECHECS.append('D17 programme')

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs et sorties du chapitre 17 et du défi D17 sont vérifiées.")
