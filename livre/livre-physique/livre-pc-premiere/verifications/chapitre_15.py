"""Vérification du chapitre 15 (Travail et énergie cinétique) et du défi D15.

Lancer : python -I -X utf8 verifications/chapitre_15.py
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


def ec(m, v):
    return 0.5 * m * v * v


# Cours
verifie("cours Ec voiture 1000 kg à 72 km/h (J)", ec(1000, 20), 2.0e5)
verifie("cours travail 100 N, 10 m, 60 degrés (J)", 100 * 10 * math.cos(math.radians(60)), 500)
verifie("cours travail du poids, 2,0 kg, 3,0 m (J)", 2.0 * G * 3.0, 58.9, 0.002)
verifie("cours chute de 5,0 m : vitesse (m/s)", math.sqrt(2 * G * 5.0), 9.9, 0.002)


def programme():
    m, g, v = 0.50, 9.81, 0.0
    for h in [1, 2, 3, 4, 5]:
        v = (2 * g * h) ** 0.5
        print(h, 'm :', round(v, 1), 'm/s ; Ec =', round(0.5 * m * v**2, 1), 'J')


s = sortie_de(programme)
print('   cours programme :', s.replace('\n', ' | '))
if s != ('1 m : 4.4 m/s ; Ec = 4.9 J\n2 m : 6.3 m/s ; Ec = 9.8 J\n3 m : 7.7 m/s ; Ec = 14.7 J\n'
         '4 m : 8.9 m/s ; Ec = 19.6 J\n5 m : 9.9 m/s ; Ec = 24.5 J'):
    ECHECS.append('cours programme')
# Exercice 1
verifie("ex1 voiture à 90 km/h (J)", ec(1200, 90 / 3.6), 3.75e5)
verifie("ex1 voiture à 130 km/h (J)", ec(1200, 130 / 3.6), 7.82e5, 0.002)
verifie("ex1 rapport 130 / 90", (130 / 90) ** 2, 2.09, 0.002)
verifie("ex1 balle de tennis (J)", ec(0.058, 50), 72.5)
verifie("ex1 piéton (J)", ec(70, 1.4), 68.6)
verifie("ex1 vitesse de la voiture pour 72,5 J (m/s)", math.sqrt(2 * 72.5 / 1200), 0.35, 0.01)
# Exercice 2 : luge
verifie("ex2 travail à 30 degrés (J)", 50 * 20 * math.cos(math.radians(30)), 866, 0.001)
verifie("ex2 travail horizontal (J)", 50 * 20, 1000)
verifie("ex2 composante utile (N)", 50 * math.cos(math.radians(30)), 43.3, 0.002)
# Exercice 3 : travail du poids
verifie("ex3 balle 0,50 kg, 2,0 m (J)", 0.50 * G * 2.0, 9.81)
verifie("ex3 escalier 60 kg, 3,0 m (J)", -60 * G * 3.0, -1766, 0.002)
verifie("ex3 randonneur 70 kg, 800 m (J)", -70 * G * 800, -5.49e5, 0.002)
# Exercice 5 : chute
verifie("ex5 vitesse après 5,0 m (m/s)", math.sqrt(2 * G * 5.0), 9.90, 0.002)
verifie("ex5 vitesse après 20 m (m/s)", math.sqrt(2 * G * 20), 19.8, 0.002)
verifie("ex5 Ec de 0,20 kg après 5,0 m (J)", 0.20 * G * 5.0, 9.81)


# Exercice 6 : programme
def programme6():
    from math import cos, radians
    F, d = 100, 10
    for angle in [0, 30, 60, 90, 120, 180]:
        W = F * d * cos(radians(angle))
        print(angle, 'degres :', round(W), 'J')


s6 = sortie_de(programme6)
print('   ex6 programme :', s6.replace('\n', ' | '))
if s6 != '0 degres : 1000 J\n30 degres : 866 J\n60 degres : 500 J\n90 degres : 0 J\n120 degres : -500 J\n180 degres : -1000 J':
    ECHECS.append('ex6 programme')
# Exercice 7 : freinage
dEc7 = -ec(1000, 25)
verifie("ex7 variation d'Ec (J)", dEc7, -3.125e5)
verifie("ex7 force de freinage (N)", -dEc7 / 50, 6.25e3)
verifie("ex7 distance à 130 km/h (m)", ec(1000, 130 / 3.6) / 6.25e3, 104, 0.004)
# Exercice 8 : skieur
Ep8 = 80 * G * 30
verifie("ex8 travail du poids (J)", Ep8, 2.35e4, 0.003)
verifie("ex8 vitesse sans frottement (m/s)", math.sqrt(2 * G * 30), 24.3, 0.002)
verifie("ex8 Ec à 18 m/s (J)", ec(80, 18), 1.30e4, 0.004)
Wf8 = ec(80, 18) - Ep8
verifie("ex8 travail des frottements (J)", Wf8, -1.06e4, 0.003)
verifie("ex8 force de frottement (N)", -Wf8 / 100, 106, 0.003)
# Exercice 9 : lancer
verifie("ex9 vitesse au sol (m/s)", math.sqrt(10 ** 2 + 2 * G * 1.5), 11.4, 0.003)
verifie("ex9 vitesse au sol, 2,0 m (m/s)", math.sqrt(10 ** 2 + 2 * G * 2.0), 11.8, 0.003)
# Exercice 10 : chariot
WF10 = 40 * 15 * math.cos(math.radians(20))
verifie("ex10 travail de la poussée (J)", WF10, 564, 0.002)
verifie("ex10 travail des frottements (J)", -30 * 15, -450)
verifie("ex10 variation d'Ec (J)", WF10 - 450, 114, 0.004)
verifie("ex10 vitesse finale (m/s)", math.sqrt(2 * (WF10 - 450) / 30), 2.75, 0.003)
# Exercice 11 : descente à vitesse constante
verifie("ex11 travail du poids (J)", 1500 * G * 16, 2.35e5, 0.003)
verifie("ex11 force de freinage moyenne (N)", 1500 * G * 16 / 200, 1.18e3, 0.003)
# Exercice 12 : tir à l'arc
verifie("ex12 travail de la corde (J)", 150 * 0.50, 75)
v12 = math.sqrt(2 * 75 / 0.020)
verifie("ex12 vitesse de la flèche (m/s)", v12, 86.6, 0.002)
verifie("ex12 vitesse (km/h)", v12 * 3.6, 312, 0.002)
verifie("ex12 hauteur sans frottement (m)", v12 ** 2 / (2 * G), 382, 0.003)
# Exercice 13 : distance de freinage
for v_kmh, d in [(50, 12.3), (90, 39.8), (130, 83.1)]:
    verifie(f"ex13 distance de freinage à {v_kmh} km/h (m)", (v_kmh / 3.6) ** 2 / (2 * 0.8 * G), d, 0.003)
verifie("ex13 rapport 100 / 50 km/h", 4, 4)
verifie("ex13 route mouillée à 90 km/h (m)", 25 ** 2 / (2 * 0.5 * G), 63.7, 0.003)
# Exercice 14 : saut à la perche
Ec14 = ec(75, 9.5)
verifie("ex14 Ec (J)", Ec14, 3.38e3, 0.003)
verifie("ex14 élévation (m)", 9.5 ** 2 / (2 * G), 4.60, 0.002)
verifie("ex14 hauteur atteinte (m)", 9.5 ** 2 / (2 * G) + 1.1, 5.7, 0.003)
verifie("ex14 vitesse pour 6,2 m (m/s)", math.sqrt(2 * G * (6.2 - 1.1)), 10.0, 0.003)
# Exercice 15 : atterrissage
Ec15 = ec(64000, 70)
verifie("ex15 Ec à l'atterrissage (J)", Ec15, 1.57e8, 0.002)
verifie("ex15 force de freinage moyenne (N)", Ec15 / 1500, 1.05e5, 0.005)
verifie("ex15 rapport au poids", Ec15 / 1500 / (64000 * G), 0.17, 0.03)
verifie("ex15 distance sans inverseurs (m)", Ec15 / (0.6 * Ec15 / 1500), 2.5e3, 0.003)
verifie("ex15 poids de l'avion (N)", 64000 * G, 6.28e5, 0.002)
verifie("ex1 rapport des vitesses 130 / 90", 130 / 90, 1.44, 0.004)
verifie("ex13 rapport mouillé / sec à 90 km/h", 0.8 / 0.5, 1.6)
verifie("ex10 Ec finale arrondie (J)", 564 - 450, 114)

# Défi D15 : rouler moins vite
CS, RHO, FR = 0.65, 1.2, 150
utile_par_litre = 35e6 * 0.30


def conso(v_kmh):
    v = v_kmh / 3.6
    f = 0.5 * RHO * CS * v * v + FR
    return f, f * 1e5, f * 1e5 / utile_par_litre


for v_kmh, fair, W, litres in [(90, 244, 3.94e7, 3.75), (110, 364, 5.14e7, 4.90), (130, 509, 6.59e7, 6.27)]:
    f, Wc, L = conso(v_kmh)
    verifie(f"D15 frottement de l'air à {v_kmh} km/h (N)", f - FR, fair, 0.003)
    verifie(f"D15 travail moteur sur 100 km à {v_kmh} km/h (J)", Wc, W, 0.003)
    verifie(f"D15 carburant à {v_kmh} km/h (L)", L, litres, 0.003)
verifie("D15 énergie utile par litre (MJ)", utile_par_litre / 1e6, 10.5)
verifie("D15 économie 130 -> 110 km/h (L)", conso(130)[2] - conso(110)[2], 1.37, 0.01)
verifie("D15 économie relative (%)", (conso(130)[2] - conso(110)[2]) / conso(130)[2] * 100, 22, 0.02)
verifie("D15 CO2 à 130 km/h (kg)", conso(130)[2] * 2.3, 14.4, 0.003)
verifie("D15 CO2 à 110 km/h (kg)", conso(110)[2] * 2.3, 11.3, 0.004)
verifie("D15 durée de 100 km à 130 km/h (min)", 100 / 130 * 60, 46, 0.005)
verifie("D15 durée de 100 km à 110 km/h (min)", 100 / 110 * 60, 55, 0.01)


def programme_d15():
    Cs, rho, fr = 0.65, 1.2, 150
    for v_kmh in [90, 110, 130]:
        v = v_kmh / 3.6
        f = 0.5 * rho * Cs * v**2 + fr
        W = f * 100e3
        print(v_kmh, 'km/h :', round(W / 10.5e6, 2), 'L/100 km')


s15 = sortie_de(programme_d15)
print('   D15 programme :', s15.replace('\n', ' | '))
if s15 != '90 km/h : 3.75 L/100 km\n110 km/h : 4.9 L/100 km\n130 km/h : 6.27 L/100 km':
    ECHECS.append('D15 programme')

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs et sorties du chapitre 15 et du défi D15 sont vérifiées.")
