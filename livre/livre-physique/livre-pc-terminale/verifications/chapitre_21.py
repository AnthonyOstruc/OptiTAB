"""Vérification des résultats numériques du chapitre 21 (intensité sonore et atténuation) et du défi D21.

Lancer : python -I -X utf8 verifications/chapitre_21.py
"""
import io
from contextlib import redirect_stdout
from math import log10, pi, sqrt

ECHECS = []
I0 = 1e-12


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


def L(I):
    return 10 * log10(I / I0)


def I(Lv):
    return I0 * 10 ** (Lv / 10)


# L'essentiel
verifie("cours seuil de douleur (dB)", L(1.0), 120, 1e-9)
verifie("cours intensité doublée (+dB)", 10 * log10(2), 3.0, 0.05)
verifie("cours trois machines à 80 dB", L(3 * I(80)), 84.8, 0.05)
verifie("cours distance doublée (dB)", 20 * log10(2), 6.0, 0.05)


def programme_cours():
    P, I0 = 0.10, 1e-12                 # W, W/m²
    for d in [1, 2, 4, 8, 16]:          # m
        I = P / (4 * pi * d**2)
        L = 10 * log10(I / I0)
        print(d, round(L, 1))


s = sortie_de(programme_cours).splitlines()
print('   cours programme :', s)
if s != ['1 99.0', '2 93.0', '4 87.0', '8 80.9', '16 74.9']:
    ECHECS.append('cours programme')
for d, Lv in ((1, 99.0), (10, 79.0), (100, 59.0)):
    verifie(f"figure atténuation : L à {d} m", L(0.10 / (4 * pi * d ** 2)), Lv, 0.05)
# Exercice 1
verifie("ex1 intensité à 60 dB", I(60), 1.0e-6, 1e-12)
verifie("ex1 niveau pour 3,2e-5 W/m²", L(3.2e-5), 75, 0.1)
verifie("ex1 intensité à 85 dB", I(85), 3.2e-4, 0.05e-4)
verifie("ex1 rapport 100 dB / 70 dB", I(100) / I(70), 1000, 1e-6)
# Exercice 2
verifie("ex2 deux violons", 70 + 10 * log10(2), 73, 0.05)
verifie("ex2 dix violons", 70 + 10 * log10(10), 80, 1e-9)
verifie("ex2 nombre pour 85 dB", 10 ** 1.5, 31.6, 0.05)
# Exercice 3
verifie("ex3 niveau à 4 m", 100 - 20 * log10(2), 94, 0.05)
verifie("ex3 niveau à 20 m", 100 - 20 * log10(10), 80, 1e-9)
verifie("ex3 puissance (W)", I(100) * 4 * pi * 2.0 ** 2, 0.50, 0.005)
verifie("ex3 distance pour 70 dB (m)", 2.0 * 10 ** (30 / 20), 63, 0.5)
# Exercice 4
verifie("ex4 niveau avec bouchons", 105 - 25, 80, 0)
verifie("ex4 fraction d'intensité transmise", 10 ** (-2.5), 3.2e-3, 0.05e-3)
verifie("ex4 durée à 94 dB (h)", 8 / 2 ** ((94 - 85) / 3), 1.0, 1e-9)
verifie("ex4 durée à 105 dB sans protection (min)", 8 * 60 / 2 ** ((105 - 85) / 3), 4.7, 0.05)
# Exercice 5
verifie("ex5 log10(1000)", log10(1000), 3, 1e-12)
verifie("ex5 log10(2)", log10(2), 0.30, 0.005)
verifie("ex5 10^0,5", 10 ** 0.5, 3.16, 0.005)
verifie("ex5 nombre d'ordres de grandeur", log10(1 / I0), 12, 1e-9)
# Exercice 6
verifie("ex6 niveau à 20 m", 110 - 20 * log10(20 / 5), 98, 0.05)
verifie("ex6 niveau à 40 m", 110 - 20 * log10(40 / 5), 91.9, 0.05)
verifie("ex6 distance pour 102 dB (m)", 5 * 10 ** (8 / 20), 12.6, 0.05)
verifie("ex6 niveau avec bouchons à 20 m", 98 - 20, 78, 0.05)
# Exercice 7
verifie("ex7 quinze conversations", 55 + 10 * log10(15), 66.8, 0.05)
verifie("ex7 trente conversations", 55 + 10 * log10(30), 69.8, 0.05)
verifie("ex7 une conversation de plus sur 15", 10 * log10(16 / 15), 0.28, 0.005)
# Exercice 8
verifie("ex8 niveau à 16 m avec absorption de 5 dB/km", 74.9 - 5 * 0.016, 74.8, 0.05)
verifie("ex8 niveau à 1000 m sans absorption", L(0.10 / (4 * pi * 1000 ** 2)), 39.0, 0.05)
verifie("ex8 niveau à 1000 m avec 5 dB/km", L(0.10 / (4 * pi * 1000 ** 2)) - 5, 34.0, 0.05)
# Exercice 9
verifie("ex9 intérieur simple vitrage", 72 - 25, 47, 0)
verifie("ex9 intérieur double vitrage", 72 - 35, 37, 0)
verifie("ex9 rapport d'intensités transmises", 10 ** ((35 - 25) / 10), 10, 1e-9)
verifie("ex9 fenêtre entrouverte (fraction d'intensité)", 10 ** (-10 / 10), 0.1, 1e-12)
# Exercice 10
verifie("ex10 atténuation géométrique de 1 m à 1 km", 20 * log10(1000), 60, 1e-9)
for f, alpha, Lk in ((500, 2.8, 37.2), (1000, 4.7, 35.3), (4000, 24, 16), (8000, 83, -43)):
    verifie(f"ex10 niveau à 1 km pour {f} Hz", 100 - 60 - alpha, Lk, 0.05)
# Exercice 11
verifie("ex11 source linéaire à 100 m", 75 - 10 * log10(4), 69, 0.05)
verifie("ex11 source ponctuelle à 100 m", 75 - 20 * log10(4), 63, 0.05)
verifie("ex11 distance pour 60 dB en source linéaire (m)", 25 * 10 ** (15 / 10), 791, 1)
# Exercice 12
verifie("ex12 distance minimale pour une enceinte (m)", 4 * 10 ** (8 / 20), 10.0, 0.05)
verifie("ex12 distance minimale pour deux enceintes (m)", 4 * 10 ** (11 / 20), 14.2, 0.05)
verifie("ex12 niveau de deux enceintes à 10 m", 102 + 10 * log10(2), 105, 0.05)
# Exercice 13
P13 = I(105)
verifie("ex13 puissance acoustique (W)", P13, 0.032, 0.0005)
I13 = P13 / (4 * pi * 500 ** 2)
verifie("ex13 intensité à 500 m", I13, 1.0e-8, 0.05e-8)
verifie("ex13 niveau à 500 m", L(I13), 40.0, 0.05)
tot = L(I(35) + I13)
verifie("ex13 niveau total la nuit", tot, 41.2, 0.05)
verifie("ex13 émergence", tot - 35, 6.2, 0.05)
Imax = I(38) - I(35)
verifie("ex13 niveau maximal de l'éolienne", L(Imax), 35.0, 0.05)
verifie("ex13 distance minimale (m)", sqrt(P13 / (4 * pi * Imax)), 894, 5)
# Exercice 14
verifie("ex14 atténuation à 5 MHz pour 8 cm aller-retour (dB)", 0.5 * 5 * 16, 40, 1e-9)
verifie("ex14 fraction d'intensité revenue", 10 ** (-4), 1e-4, 1e-12)
verifie("ex14 profondeur maximale à 7,5 MHz (cm)", 60 / (0.5 * 7.5 * 2), 8.0, 1e-9)
verifie("ex14 profondeur maximale à 3,5 MHz (cm)", 60 / (0.5 * 3.5 * 2), 17.1, 0.05)
# Exercice 15
Leq = 10 * log10((1 * 10 ** 9.4 + 3 * 10 ** 8.8) / 8)
verifie("ex15 niveau équivalent sur 8 h", Leq, 87.4, 0.05)
verifie("ex15 dose", 1 / 1 + 3 / 4, 1.75, 1e-9)
verifie("ex15 niveau avec bouchons de 15 dB", 10 * log10((1 * 10 ** 7.9 + 3 * 10 ** 7.3) / 8), 72.4, 0.05)
verifie("ex15 dose à 85 dB pendant 8 h", 8 / 8, 1, 0)
# Valeurs intermédiaires des corrigés
verifie("cor4 facteur de réduction de durée à 105 dB", 2 ** (20 / 3), 102, 0.5)
verifie("cor8 absorption à 16 m (dB)", 5 * 16 / 1000, 0.08, 1e-9)
verifie("cor9 atténuation minimale (dB)", 72 - 35, 37, 0)
verifie("cor13 intensité maximale de l'éolienne", Imax, 3.15e-9, 0.005e-9)
verifie("cor15 énergie 1 h à 94 dB (u.a.)", 10 ** 9.4, 2.51e9, 0.005e9)
verifie("cor15 énergie 8 h à 85 dB (u.a.)", 8 * 10 ** 8.5, 2.53e9, 0.005e9)
# Défi D21


def programme_d21():
    ms = 230                            # kg/m², béton de 10 cm
    for f in [125, 250, 500, 1000, 2000, 4000]:   # Hz
        R = 20 * log10(ms * f) - 47     # loi de masse (dB)
        print(f, round(R, 1))


s = sortie_de(programme_d21).splitlines()
print('   D21 sorties :', s)
if s != ['125 42.2', '250 48.2', '500 54.2', '1000 60.2', '2000 66.3', '4000 72.3']:
    ECHECS.append('D21 sorties')


def Rm(ms, f):
    return 20 * log10(ms * f) - 47


verifie("D21 gain pour une fréquence doublée", 20 * log10(2), 6.0, 0.05)
verifie("D21 cloison double plaque à 500 Hz", Rm(20, 500), 33, 0.05)
verifie("D21 conversation derrière le béton", 60 - Rm(230, 500), 5.8, 0.05)
verifie("D21 conversation derrière la cloison", 60 - Rm(20, 500), 27, 0.05)
verifie("D21 béton à 63 Hz", Rm(230, 63), 36.2, 0.05)
verifie("D21 basses entendues", 90 - Rm(230, 63), 53.8, 0.05)
verifie("D21 aigus entendus", 80 - Rm(230, 4000), 7.7, 0.05)
verifie("D21 masse décuplée (+dB)", 20 * log10(10), 20, 1e-9)
Rp = Rm(15, 500)
verifie("D21 porte à 500 Hz", Rp, 30.5, 0.05)
tau = (8 * 10 ** (-Rm(230, 500) / 10) + 2 * 10 ** (-Rp / 10)) / 10
verifie("D21 indice de la paroi avec porte", -10 * log10(tau), 37.4, 0.05)
verifie("D21 part de la porte dans la transmission (%)", 100 * 2 * 10 ** (-Rp / 10) / (10 * tau), 98, 0.5)
for f, Rb, Rc in ((125, 42.2, 21.0), (1000, 60.2, 39.0), (4000, 72.3, 51.1)):
    verifie(f"figure D21 : béton à {f} Hz", Rm(230, f), Rb, 0.05)
    verifie(f"figure D21 : cloison à {f} Hz", Rm(20, f), Rc, 0.05)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 21 et du défi D21 sont vérifiées.")
