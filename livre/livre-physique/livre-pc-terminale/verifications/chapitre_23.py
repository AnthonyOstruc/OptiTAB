"""Vérification des résultats numériques du chapitre 23 (effet Doppler) et du défi D23.

Lancer : python -I -X utf8 verifications/chapitre_23.py
"""
import io
from contextlib import redirect_stdout
from math import cos, radians, sqrt

ECHECS = []
C = 3.00e8
V = 340.0


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


def app(f, vE, v=V):
    return f * v / (v - vE)


def eloi(f, vE, v=V):
    return f * v / (v + vE)


# L'essentiel
verifie("cours fréquence à l'approche (Hz)", app(900, 25), 971.4, 0.05)
verifie("cours fréquence à l'éloignement (Hz)", eloi(900, 25), 838.4, 0.05)
verifie("cours approximation (Hz)", 900 * 25 / 340, 66, 0.5)
verifie("cours décalage exact (Hz)", app(900, 25) - 900, 71.4, 0.05)


def programme_cours():
    v = 340.0                           # m/s
    f_app, f_eloi = 971.4, 838.4        # Hz
    vE = v * (f_app - f_eloi) / (f_app + f_eloi)
    fE = f_app * (v - vE) / v
    print(round(vE, 1), round(3.6 * vE), round(fE))


s = sortie_de(programme_cours)
print('   cours programme :', s)
if s != '25.0 90 900':
    ECHECS.append('cours programme')
verifie("cours décalage relatif d'une galaxie", 0.0233 * C / 1000, 6990, 5)
# Exercice 1
verifie("ex1 approche (Hz)", app(435, 20), 462, 0.5)
verifie("ex1 éloignement (Hz)", eloi(435, 20), 411, 0.5)
verifie("ex1 approche 488 Hz", app(488, 20), 519, 0.5)
# Exercice 3
verifie("ex3 approche (Hz)", app(500, 40), 566.7, 0.05)
verifie("ex3 éloignement (Hz)", eloi(500, 40), 447.4, 0.05)
verifie("ex3 rapport", app(500, 40) / eloi(500, 40), 1.27, 0.005)
# Exercice 4
for vE, ex, ap in ((10, 30.3, 29.4), (50, 172, 147), (100, 416.7, 294)):
    verifie(f"ex4 décalage exact à {vE} m/s (Hz)", app(1000, vE) - 1000, ex, 0.5)
    verifie(f"ex4 décalage approché à {vE} m/s (Hz)", 1000 * vE / V, ap, 0.5)
verifie("ex4 écart relatif à 10 m/s (%)", 100 * ((app(1000, 10) - 1000) - 1000 * 10 / V) / (app(1000, 10) - 1000), 2.9, 0.05)
# Exercice 5
verifie("ex5 vitesse de l'étoile (km/s)", C * (656.50 - 656.28) / 656.28 / 1000, 101, 0.5)
# Exercice 6
v6 = 3950 * C / (2 * 24.125e9 * cos(radians(25)))
verifie("ex6 vitesse (m/s)", v6, 27.1, 0.05)
verifie("ex6 vitesse (km/h)", 3.6 * v6, 97.6, 0.05)
verifie("ex6 vitesse retenue (km/h)", 3.6 * v6 - 5, 92.6, 0.05)
verifie("ex6 décalage pour 90 km/h (Hz)", 2 * 24.125e9 * 25 * cos(radians(25)) / C, 3.64e3, 0.005e3)
# Exercice 7
vE7 = V * (1062 - 878) / (1062 + 878)
verifie("ex7 vitesse (m/s)", vE7, 32.2, 0.05)
verifie("ex7 vitesse (km/h)", 3.6 * vE7, 116, 0.5)
verifie("ex7 fréquence émise (Hz)", 1062 * (V - vE7) / V, 961, 0.5)
# Exercice 8
verifie("ex8 vitesse du sang (m/s)", 1300 * 1540 / (2 * 4.0e6 * cos(radians(60))), 0.50, 0.005)
verifie("ex8 décalage pour 1,0 m/s (kHz)", 2 * 4.0e6 * 1.0 * 0.5 / 1540 / 1000, 2.6, 0.05)
# Exercice 9
verifie("ex9 longueur d'onde devant à 0,9 v (cm)", 100 * (V - 0.9 * V) / 1000, 3.4, 0.05)
verifie("ex9 longueur d'onde à l'arrêt (cm)", 100 * V / 1000, 34, 0.5)
verifie("ex9 fréquence reçue à 0,9 v (kHz)", app(1000, 0.9 * V) / 1000, 10, 1e-9)
# Exercice 10
verifie("ex10 vitesse radiale maximale (km/s)", C * 0.18 / 656.28 / 1000, 82, 0.5)
verifie("ex10 longueur d'onde moyenne (nm)", (656.10 + 656.46) / 2, 656.28, 1e-9)
# Exercice 11
vE11 = V * (330 - 270) / (330 + 270)
verifie("ex11 vitesse (m/s)", vE11, 34, 1e-9)
verifie("ex11 vitesse (km/h)", 3.6 * vE11, 122, 0.5)
verifie("ex11 fréquence émise (Hz)", 330 * (V - vE11) / V, 297, 1e-9)
# Exercice 12
for lam, d, v_pub in ((659.4, 20, 1417), (663.9, 50, 3474), (671.7, 100, 7039)):
    verifie(f"ex12 vitesse pour {lam} nm (km/s)", 3.00e5 * (lam - 656.3) / 656.3, v_pub, 1)
    verifie(f"ex12 rapport v/d à {d} Mpc", 3.00e5 * (lam - 656.3) / 656.3 / d, round(v_pub / d, 1), 0.1)
verifie("ex12 âge 1/H0 (milliards d'années)", 3.086e19 / 70 / 3.156e7 / 1e9, 14, 0.5)
# Exercice 13
verifie("ex13 décalage maximal (nm)", 500 * 56 / C, 9.3e-5, 0.05e-5)
verifie("ex13 décalage relatif", 56 / C, 1.9e-7, 0.05e-7)
verifie("ex13 vitesse de la Terre due à Jupiter... (m/s)", 12.5, 12.5, 0)
# Exercice 14
verifie("ex14 décalage maximal (kHz)", 437e6 * 7000 / C / 1000, 10.2, 0.05)
verifie("ex14 excursion totale (kHz)", 2 * 437e6 * 7000 / C / 1000, 20.4, 0.05)
verifie("ex14 décalage à 2,4 GHz (kHz)", 2.4e9 * 7000 / C / 1000, 56, 0.5)
# Exercice 15
verifie("ex15 vitesse radiale du vent (m/s)", 560 * C / (2 * 5.6e9), 15, 1e-9)
verifie("ex15 vitesse (km/h)", 3.6 * 15, 54, 0)
verifie("ex15 décalage pour la pluie à 8 m/s (Hz)", 2 * 5.6e9 * 8 / C, 299, 0.5)
# Valeurs intermédiaires des corrigés
verifie("cor5 effet de 0,01 nm sur la vitesse (km/s)", 3.00e5 * 0.01 / 656.28, 4.6, 0.05)
verifie("cor12 1/H0 (s)", 3.086e19 / 70, 4.4e17, 0.05e17)
verifie("cor12 décalage relatif pour 70 nm", 70 / 656.3, 0.11, 0.005)
verifie("cor13 rapport à la précision", (56 / C) / 1e-8, 19, 0.5)
verifie("cor13 rapport des vitesses 51 Peg / Soleil", 56 / 12.5, 4.5, 0.05)
# Défi D23


def programme_d23():
    v, fE, vE, b = 340.0, 900.0, 25.0, 10.0   # m/s, Hz, m/s, m
    for t in [-4, -2, -1, 0, 1, 2, 4]:        # date d'émission (s)
        x = vE * t                            # abscisse de la voiture
        d = sqrt(x**2 + b**2)                 # distance à l'auditeur
        cos_theta = -x / d
        fR = fE * v / (v - vE * cos_theta)
        print(t, round(t + d / v, 2), round(fR, 1))


s = sortie_de(programme_d23).splitlines()
print('   D23 sorties :', s)
ATT = ['-4 -3.7 971.0', '-2 -1.85 969.9', '-1 -0.92 965.9', '0 0.03 900.0', '1 1.08 842.5', '2 2.15 839.5', '4 4.3 838.6']
if s != ATT:
    ECHECS.append('D23 sorties')
verifie("D23 asymptote à l'approche (Hz)", app(900, 25), 971.4, 0.05)
verifie("D23 asymptote à l'éloignement (Hz)", eloi(900, 25), 838.4, 0.05)
verifie("D23 retard au passage (s)", 10 / 340, 0.029, 0.0005)
verifie("D23 dissymétrie : hausse (Hz)", app(900, 25) - 900, 71.4, 0.05)
verifie("D23 dissymétrie : baisse (Hz)", 900 - eloi(900, 25), 61.6, 0.05)
verifie("D23 moyenne des asymptotes (Hz)", (app(900, 25) + eloi(900, 25)) / 2, 904.9, 0.05)
verifie("D23 vitesse déduite (m/s)", V * (971.4 - 838.4) / (971.4 + 838.4), 25.0, 0.05)
verifie("D23 durée de la transition (s)", 2 * 10 / 25, 0.8, 1e-9)


def fR_t(t, b=10.0):
    x = 25 * t
    d = sqrt(x ** 2 + b ** 2)
    return 900 * 340 / (340 + 25 * x / d)


for t, f in ((-0.4, 949.4), (0.4, 855.5)):
    verifie(f"figure D23 : f à t_émission = {t} s (b = 10 m)", fR_t(t), f, 0.05)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 23 et du défi D23 sont vérifiées.")
