"""Vérification du chapitre 13 (Forces et variation de la vitesse) et du défi D13.

Lancer : python -I -X utf8 verifications/chapitre_13.py
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


# Cours : chute d'une balle, Delta t = 0,10 s
verifie("cours variation de vitesse en chute libre, 0,10 s (m/s)", G * 0.10, 0.98, 0.002)
verifie("cours voiture 1000 kg, F = 2000 N, 1,0 s : Delta v (m/s)", 2000 * 1.0 / 1000, 2.0)


def programme():
    dt = 0.10
    y = [0.80, 0.75, 0.60, 0.36, 0.02]
    v = [(y[i + 1] - y[i]) / dt for i in range(4)]
    for i in range(3):
        print('Delta v =', round(v[i + 1] - v[i], 2), 'm/s')


s = sortie_de(programme)
print('   cours programme :', s.replace('\n', ' | '))
if s != 'Delta v = -1.0 m/s\nDelta v = -0.9 m/s\nDelta v = -1.0 m/s':
    ECHECS.append('cours programme')
# positions de la balle lâchée en y = 0,80 m (modèle, arrondies au cm)
for i, yp in enumerate([0.80, 0.75, 0.60, 0.36, 0.02]):
    if round(0.80 - 0.5 * G * (0.10 * i) ** 2, 2) != yp:
        ECHECS.append(f'cours position {i}')

# Exercice 1 : palet à vitesse constante
verifie("ex1 vitesse (m/s)", 0.016 / 0.040, 0.40)
verifie("ex1 longueur du vecteur, 1 cm pour 0,10 m/s (cm)", 0.40 / 0.10, 4.0)
# Exercice 2 : chute verticale, Delta t = 0,050 s
ys = [round(100 * 0.5 * G * (0.05 * i) ** 2, 1) for i in range(7)]
print('   ex2 positions (cm) :', ys)
if ys != [0.0, 1.2, 4.9, 11.0, 19.6, 30.7, 44.1]:
    ECHECS.append('ex2 positions')
v3 = (ys[4] - ys[3]) / 100 / 0.05
v4 = (ys[5] - ys[4]) / 100 / 0.05
verifie("ex2 v3 (m/s)", v3, 1.72)
verifie("ex2 v4 (m/s)", v4, 2.22)
verifie("ex2 Delta v (m/s)", v4 - v3, 0.50)
verifie("ex2 Delta v / Delta t (m/s2)", (v4 - v3) / 0.05, 10.0)
verifie("ex2 somme des forces (N)", 0.058 * (v4 - v3) / 0.05, 0.58, 0.01)
verifie("ex2 poids (N)", 0.058 * G, 0.57, 0.01)
# Exercice 3 : rôle de la masse
verifie("ex3 chariot 2,0 kg (m/s)", 20 * 0.50 / 2.0, 5.0)
verifie("ex3 chariot 10 kg (m/s)", 20 * 0.50 / 10, 1.0)
verifie("ex3 force pour 5,0 m/s avec 10 kg (N)", 10 * 5.0 / 0.50, 100)
verifie("ex9 tangente à l'origine : vitesse à 5 s (m/s)", G * 5, 49, 0.002)
verifie("ex11 longueur de v2 à 2 m/s par cm (cm)", 2.26 / 2, 1.13)
verifie("ex11 longueur de Delta v2 (cm)", 0.99 / 2, 0.50, 0.011)
verifie("ex15 rapport des champs Terre / Lune", 9.81 / 1.62, 6.0, 0.011)
# Exercice 4 : freinage
dv4 = 50 / 3.6
verifie("ex4 Delta v (m/s)", dv4, 13.9)
verifie("ex4 force (N)", 1200 * dv4 / 2.5, 6.7e3, 0.01)
verifie("ex4 Delta v en 0,10 s (m/s)", dv4 / 2.5 * 0.10, 0.56, 0.01)
verifie("ex4 camion 12 t (N)", 12000 * dv4 / 2.5, 6.7e4, 0.01)


# Exercice 6 : programme de la balle lancée
def programme6():
    dt = 0.10
    x = [0, 0.30, 0.60, 0.90, 1.20, 1.50, 1.80]
    y = [0, 0.35, 0.60, 0.76, 0.82, 0.77, 0.63]
    vx = [(x[i + 1] - x[i]) / dt for i in range(6)]
    vy = [(y[i + 1] - y[i]) / dt for i in range(6)]
    for i in range(5):
        print('vx =', round(vx[i], 1), '| Delta vy =', round(vy[i + 1] - vy[i], 1))


s6 = sortie_de(programme6)
print('   ex6 programme :', s6.replace('\n', ' | '))
if s6 != ('vx = 3.0 | Delta vy = -1.0\nvx = 3.0 | Delta vy = -0.9\nvx = 3.0 | Delta vy = -1.0\n'
          'vx = 3.0 | Delta vy = -1.1\nvx = 3.0 | Delta vy = -0.9'):
    ECHECS.append('ex6 programme')
for i, (xp, yp) in enumerate(zip([0, 0.30, 0.60, 0.90, 1.20, 1.50, 1.80],
                                 [0, 0.35, 0.60, 0.76, 0.82, 0.77, 0.63])):
    t = 0.1 * i
    if abs(3.0 * t - xp) > 0.001 or abs(4.0 * t - 0.5 * G * t * t - yp) > 0.006:
        ECHECS.append(f'ex6 position {i}')
verifie("ex6 moyenne des Delta vy (m/s)", (-1.0 - 0.9 - 1.0 - 1.1 - 0.9) / 5, -0.98)
verifie("ex6 accélération déduite (m/s2)", 0.98 / 0.10, 9.8)
verifie("ex6 poids d'une balle de 60 g (N)", 0.060 * G, 0.59, 0.01)
# Exercice 7 : mouvement circulaire
R, v, dt7 = 0.50, 2.0, 0.10
theta = v * dt7 / R
verifie("ex7 angle entre deux positions (degrés)", math.degrees(theta), 22.9, 0.003)
corde = 2 * R * math.sin(theta / 2)
verifie("ex7 corde M2M3 (m)", corde, 0.199, 0.003)
verifie("ex7 vitesse estimée (m/s)", corde / dt7, 1.99, 0.003)
dv7 = 2 * (corde / dt7) * math.sin(theta / 2)
verifie("ex7 norme de Delta v (m/s)", dv7, 0.79, 0.01)
verifie("ex7 force (N)", 0.20 * dv7 / dt7, 1.6, 0.02)
# Exercice 8 : palet de hockey
verifie("ex8 force (N)", 0.17 * 30 / 0.010, 510)
verifie("ex8 poids (N)", 0.17 * G, 1.67, 0.01)
verifie("ex8 rapport", 510 / (0.17 * G), 306, 0.01)
# Exercice 9 : parachutiste
verifie("ex9 frottements à 55 m/s (N)", 80 * G, 785, 0.002)
sf9 = 80 * (6 - 55) / 3.0
verifie("ex9 somme des forces à l'ouverture (N)", sf9, -1307, 0.002)
verifie("ex9 frottements à l'ouverture (N)", -sf9 + 80 * G, 2.09e3, 0.01)
verifie("ex9 Delta v pendant les 0,5 premières secondes (m/s)", G * 0.5, 4.9, 0.002)
# Exercice 10 : chariot
xs10 = [round(0.5 * 1.2 * (0.1 * i) ** 2, 3) for i in range(7)]
print('   ex10 positions (m) :', xs10)
if xs10 != [0.0, 0.006, 0.024, 0.054, 0.096, 0.15, 0.216]:
    ECHECS.append('ex10 positions')
v10 = [(xs10[i + 1] - xs10[i]) / 0.1 for i in range(6)]
print('   ex10 vitesses (m/s) :', [round(a, 2) for a in v10])
verifie("ex10 Delta v (m/s)", v10[3] - v10[2], 0.12)
verifie("ex10 force (N)", 0.50 * 0.12 / 0.10, 0.60)
# Exercice 11 : parabole, Delta t = 0,10 s, v0 = (2,0 ; 3,5)
pts11 = [(round(2.0 * 0.1 * i, 3), round(3.5 * 0.1 * i - 0.5 * G * (0.1 * i) ** 2, 3)) for i in range(8)]
print('   ex11 positions (m) :', pts11)
attendu11 = [(0.0, 0.0), (0.2, 0.301), (0.4, 0.504), (0.6, 0.609), (0.8, 0.615), (1.0, 0.524),
             (1.2, 0.334), (1.4, 0.047)]
if pts11 != attendu11:
    ECHECS.append('ex11 positions')
v2 = ((0.6 - 0.4) / 0.1, (0.609 - 0.504) / 0.1)
v3b = ((0.8 - 0.6) / 0.1, (0.615 - 0.609) / 0.1)
verifie("ex11 v2y (m/s)", v2[1], 1.05)
verifie("ex11 v3y (m/s)", v3b[1], 0.06)
verifie("ex11 norme v2 (m/s)", math.hypot(*v2), 2.26, 0.003)
verifie("ex11 norme v3 (m/s)", math.hypot(*v3b), 2.0, 0.003)
verifie("ex11 Delta v (m/s)", v2[1] - v3b[1], 0.99)
verifie("ex11 force (N)", 0.060 * 0.99 / 0.10, 0.59, 0.01)
# Exercice 12 : service au tennis
verifie("ex12 force (N)", 0.058 * 50 / 0.0050, 580)
verifie("ex12 poids (N)", 0.058 * G, 0.57, 0.01)
verifie("ex12 rapport", 580 / (0.058 * G), 1.0e3, 0.03)
verifie("ex12 service à 220 km/h (N)", 0.058 * 220 / 3.6 / 0.0050, 709, 0.002)
verifie("ex12 Delta v en 0,10 s après la frappe (m/s)", G * 0.10, 0.98, 0.002)
# Exercice 13 : lanceur
P0 = 7.8e5 * G
verifie("ex13 poids au décollage (N)", P0, 7.65e6)
verifie("ex13 somme des forces (N)", 1.40e7 - P0, 6.35e6)
verifie("ex13 Delta v en 1,0 s (m/s)", (1.40e7 - P0) / 7.8e5, 8.1, 0.01)
verifie("ex13 somme des forces à 380 t (N)", 1.40e7 - 3.8e5 * G, 1.03e7, 0.005)
verifie("ex13 Delta v en 1,0 s à 380 t (m/s)", (1.40e7 - 3.8e5 * G) / 3.8e5, 27.0, 0.005)
verifie("ex13 rapport poussée / poids", 1.40e7 / P0, 1.83, 0.005)
# Exercice 14 : ceinture et airbag
v14 = 60 / 3.6
verifie("ex14 vitesse (m/s)", v14, 16.7)
verifie("ex14 force avec ceinture et airbag (N)", 75 * v14 / 0.12, 1.04e4, 0.005)
verifie("ex14 force sans protection (N)", 75 * v14 / 0.010, 1.25e5, 0.005)
verifie("ex14 rapport des forces", 0.12 / 0.010, 12)
verifie("ex14 poids (N)", 75 * G, 736, 0.002)
verifie("ex14 rapport force / poids avec protection", 75 * v14 / 0.12 / (75 * G), 14, 0.02)


# Exercice 15 : simulation d'un tir
def programme15(g=9.81):
    from math import cos, sin, radians
    dt = 0.01
    vx, vy = 20 * cos(radians(45)), 20 * sin(radians(45))
    x, y = 0, 0
    while y >= 0:
        x, y = x + vx * dt, y + vy * dt
        vy = vy - g * dt
    print(round(x, 1), 'm')


s15 = sortie_de(programme15)
print('   ex15 programme :', s15)
if s15 != '41.0 m':
    ECHECS.append('ex15 programme')
s15l = sortie_de(lambda: programme15(1.62))
print('   ex15 programme Lune :', s15l)
if s15l != "247.1 m":
    ECHECS.append('ex15 programme Lune')
verifie("ex15 portée théorique (m)", 400 / G, 40.8, 0.002)
verifie("ex15 rapport Lune / Terre", 247.1 / 41.0, 6.0, 0.01)
verifie("ex15 Delta vy à chaque pas (m/s)", G * 0.01, 0.098, 0.002)


# Défi D13 : freiner à temps
def freinage(v_kmh, a, dt=0.01):
    v, x = v_kmh / 3.6, 0
    while v > 0:
        x = x + v * dt
        v = v - a * dt
    return x


for v_kmh, sec, mouil in [(50, 12.4, 19.7), (90, 39.9, 63.8), (130, 83.3, 133.1)]:
    verifie(f"D13 freinage à {v_kmh} km/h, route sèche (m)", freinage(v_kmh, 0.8 * G), sec, 0.004)
    verifie(f"D13 freinage à {v_kmh} km/h, route mouillée (m)", freinage(v_kmh, 0.5 * G), mouil, 0.002)
verifie("D13 freinage à 100 km/h, route sèche (m)", freinage(100, 0.8 * G), 49.3, 0.002)
verifie("D13 rapport 100 / 50 km/h", freinage(100, 0.8 * G) / freinage(50, 0.8 * G), 4.0, 0.01)
for v_kmh, react in [(50, 13.9), (90, 25.0), (130, 36.1)]:
    verifie(f"D13 distance de réaction à {v_kmh} km/h (m)", v_kmh / 3.6 * 1.0, react, 0.003)
for v_kmh, a, total in [(50, 0.8, 26), (50, 0.5, 34), (90, 0.8, 65), (90, 0.5, 89), (130, 0.8, 119),
                        (130, 0.5, 169)]:
    verifie(f"D13 distance d'arrêt à {v_kmh} km/h, {a} g (m)", v_kmh / 3.6 + freinage(v_kmh, a * G), total, 0.012)
verifie("D13 force de freinage, 1200 kg, 0,8 g (N)", 1200 * 0.8 * G, 9.42e3, 0.002)
verifie("D13 Delta v en 0,01 s (m/s)", 0.8 * G * 0.01, 0.078, 0.01)
verifie("D13 distance d'arrêt à 130 km/h, sec (m)", 36.1 + 83.1, 119, 0.003)
verifie("D13 distance d'arrêt à 130 km/h, mouillé (m)", 36.1 + 133, 169, 0.003)
verifie("D13 distance d'arrêt à 90 km/h, sec (m)", 25.0 + 39.8, 65, 0.005)
verifie("D13 distance de sécurité : 2 s à 130 km/h (m)", 130 / 3.6 * 2, 72, 0.005)
verifie("D13 distance de sécurité : 2 s à 90 km/h (m)", 90 / 3.6 * 2, 50, 0.002)


def programme_d13():
    v, x, dt = 130 / 3.6, 0, 0.01
    while v > 0:
        x = x + v * dt
        v = v - 0.8 * 9.81 * dt
    print(round(x, 1), 'm')


s13 = sortie_de(programme_d13)
print('   D13 programme :', s13)
if s13 != '83.3 m':
    ECHECS.append('D13 programme')

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs et sorties du chapitre 13 et du défi D13 sont vérifiées.")
