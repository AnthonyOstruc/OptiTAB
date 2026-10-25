"""Vérification du chapitre 16 (Énergie potentielle et énergie mécanique) et du défi D16.

Lancer : python -I -X utf8 verifications/chapitre_16.py
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
verifie("cours Ep d'un livre de 1,0 kg à 2,0 m (J)", 1.0 * G * 2.0, 19.6, 0.002)
verifie("cours chute libre : vitesse après 10 m (m/s)", math.sqrt(2 * G * 10), 14.0, 0.002)


def programme():
    m, g = 0.60, 9.81
    z = [2.00, 1.80, 1.22, 0.23]
    v = [0.00, 1.96, 3.92, 5.89]
    for i in range(4):
        Ec, Ep = 0.5 * m * v[i]**2, m * g * z[i]
        print('Ec =', round(Ec, 2), '| Ep =', round(Ep, 2), '| Em =', round(Ec + Ep, 2))


s = sortie_de(programme)
print('   cours programme :', s.replace('\n', ' / '))
if s != ('Ec = 0.0 | Ep = 11.77 | Em = 11.77\nEc = 1.15 | Ep = 10.59 | Em = 11.75\n'
         'Ec = 4.61 | Ep = 7.18 | Em = 11.79\nEc = 10.41 | Ep = 1.35 | Em = 11.76'):
    ECHECS.append('cours programme')

# Exercice 1
verifie("ex1 livre sur l'étagère (J)", 0.80 * G * 2.0, 15.7, 0.002)
verifie("ex1 livre au sol, origine à l'étagère (J)", -0.80 * G * 2.0, -15.7, 0.002)
verifie("ex1 alpiniste au mont Blanc (J)", 70 * G * 4808, 3.30e6, 0.003)
verifie("ex1 alpiniste depuis Chamonix, 1035 m (J)", 70 * G * (4808 - 1035), 2.59e6, 0.003)
# Exercice 2 : chute libre
Em2 = 0.20 * G * 10
verifie("ex2 énergie mécanique (J)", Em2, 19.6, 0.002)
verifie("ex2 Ep à 4,0 m (J)", 0.20 * G * 4.0, 7.85, 0.002)
verifie("ex2 Ec à 4,0 m (J)", Em2 - 0.20 * G * 4.0, 11.8, 0.003)
verifie("ex2 vitesse à 4,0 m (m/s)", math.sqrt(2 * (Em2 - 0.20 * G * 4.0) / 0.20), 10.8, 0.005)
verifie("ex2 vitesse au sol (m/s)", math.sqrt(2 * Em2 / 0.20), 14.0, 0.002)
# Exercice 3 : énergies d'une balle lancée
Ep0, Ec0 = 0.10 * G * 1.0, 0.5 * 0.10 * 8.0 ** 2
verifie("ex3 Ep initiale (J)", Ep0, 0.981)
verifie("ex3 Ec initiale (J)", Ec0, 3.2)
verifie("ex3 Em (J)", Ep0 + Ec0, 4.18, 0.002)
verifie("ex3 altitude maximale (m)", (Ep0 + Ec0) / (0.10 * G), 4.26, 0.002)
verifie("ex3 date du sommet (s)", 8.0 / G, 0.82, 0.006)
verifie("ex3 date d'arrivée au sol (s)", (8 + math.sqrt(64 + 2 * G * 1.0)) / G, 1.75, 0.004)
verifie("ex3 vitesse au sol (m/s)", math.sqrt(2 * (Ep0 + Ec0) / 0.10), 9.14, 0.003)
# Exercice 4 : pendule
h30 = 1.0 * (1 - math.cos(math.radians(30)))
verifie("ex4 dénivelé pour 30 degrés (m)", h30, 0.134, 0.003)
verifie("ex4 vitesse au point bas, 30 degrés (m/s)", math.sqrt(2 * G * h30), 1.62, 0.003)
verifie("ex4 vitesse au point bas, 60 degrés (m/s)", math.sqrt(2 * G * 0.5), 3.13, 0.003)


# Exercice 6 : balle de ping-pong
def programme6():
    m, g = 0.0027, 9.81
    z = [2.000, 1.951, 1.805, 1.566, 1.239, 0.830, 0.347]
    v = [0, 0.98, 1.93, 2.84, 3.69, 4.47, 5.17]
    for i in range(7):
        Em = 0.5 * m * v[i]**2 + m * g * z[i]
        print(round(0.1 * i, 1), 's :', round(Em * 1000, 1), 'mJ')


s6 = sortie_de(programme6)
print('   ex6 programme :', s6.replace('\n', ' | '))
if s6 != '0.0 s : 53.0 mJ\n0.1 s : 53.0 mJ\n0.2 s : 52.8 mJ\n0.3 s : 52.4 mJ\n0.4 s : 51.2 mJ\n0.5 s : 49.0 mJ\n0.6 s : 45.3 mJ':
    ECHECS.append('ex6 programme')
verifie("ex6 travail des frottements (mJ)", 45.3 - 53.0, -7.7, 0.002)
verifie("ex6 perte relative (%)", 7.7 / 53.0 * 100, 15, 0.04)
verifie("ex6 vitesse sans frottement à 0,6 s (m/s)", G * 0.6, 5.89, 0.002)
# Exercice 7 : montagnes russes
vB = math.sqrt(2 ** 2 + 2 * G * 35)
vC = math.sqrt(2 ** 2 + 2 * G * 15)
verifie("ex7 Em en A, origine au sol (J)", 0.5 * 500 * 4 + 500 * G * 40, 1.97e5, 0.003)
verifie("ex7 vitesse en B (m/s)", vB, 26.3, 0.002)
verifie("ex7 vitesse en C (m/s)", vC, 17.3, 0.003)
verifie("ex7 énergie dissipée (J)", 0.5 * 500 * (vB ** 2 - 24 ** 2), 2.87e4, 0.003)
verifie("ex7 fraction de Em dissipée (%)", 0.5 * 500 * (vB ** 2 - 24 ** 2) / (0.5 * 500 * 4 + 500 * G * 40) * 100, 15, 0.04)
# Exercice 8 : rebond
verifie("ex8 énergie perdue (J)", 0.058 * G * 0.40, 0.228, 0.003)
verifie("ex8 fraction conservée", 0.80 / 1.20, 0.67, 0.006)
verifie("ex8 hauteur après 5 rebonds (m)", 1.20 * (2 / 3) ** 5, 0.158, 0.003)
# Exercice 9 : balle lancée vers le haut
verifie("ex9 hauteur sans frottement (m)", 12 ** 2 / (2 * G), 7.34, 0.002)
verifie("ex9 travail des frottements (J)", 0.15 * G * (6.5 - 7.34), -1.24, 0.006)
verifie("ex9 vitesse au retour sans frottement (m/s)", 12, 12)
# Exercice 10 : téléski
verifie("ex10 variation d'Em (J)", 75 * G * 300, 2.21e5, 0.003)
verifie("ex10 puissance (W)", 75 * G * 300 / 360, 613, 0.002)
# Exercice 11 : pendule réel
Em0 = 0.20 * G * 1.0 * (1 - math.cos(math.radians(40)))
Em20 = 0.20 * G * 1.0 * (1 - math.cos(math.radians(30)))
verifie("ex11 Em initiale (J)", Em0, 0.459, 0.003)
verifie("ex11 Em après 20 s (J)", Em20, 0.263, 0.003)
verifie("ex11 énergie dissipée (J)", Em0 - Em20, 0.196, 0.006)
verifie("ex11 vitesse maximale au départ (m/s)", math.sqrt(2 * Em0 / 0.20), 2.14, 0.003)
verifie("ex11 puissance moyenne dissipée (mW)", (Em0 - Em20) / 20 * 1000, 9.8, 0.01)
# Exercice 12 : centrale hydroélectrique
verifie("ex12 Ep d'un mètre cube (J)", 1000 * G * 300, 2.94e6, 0.002)
P12 = 1000 * 50 * G * 300
verifie("ex12 puissance reçue (W)", P12, 1.47e8, 0.002)
verifie("ex12 puissance électrique (W)", 0.90 * P12, 1.32e8, 0.004)
verifie("ex12 énergie par jour (MWh)", 0.90 * P12 * 24 / 1e6, 3.18e3, 0.003)
verifie("ex12 foyers alimentés", 0.90 * P12 * 24 * 365 / 1e3 / 4700, 2.5e5, 0.02)
# Exercice 13 : lancer du poids
Ec13 = 0.5 * 7.26 * 13 ** 2
Ep13 = 7.26 * G * 2.1
verifie("ex13 Ec au lâcher (J)", Ec13, 613, 0.002)
verifie("ex13 Ep au lâcher (J)", Ep13, 150, 0.004)
verifie("ex13 Em (J)", Ec13 + Ep13, 763, 0.002)
verifie("ex13 vitesse à l'arrivée (m/s)", math.sqrt(13 ** 2 + 2 * G * 2.1), 14.5, 0.003)
vtop = 13 * math.cos(math.radians(40))
verifie("ex13 vitesse au sommet (m/s)", vtop, 9.96, 0.002)
verifie("ex13 Ec au sommet (J)", 0.5 * 7.26 * vtop ** 2, 360, 0.003)
verifie("ex13 altitude au sommet (m)", (Ec13 + Ep13 - 0.5 * 7.26 * vtop ** 2) / (7.26 * G), 5.66, 0.003)
# Exercice 14 : descente à vélo
sina = math.sin(math.atan(0.10))
verifie("ex14 sinus de la pente", sina, 0.0995, 0.002)
verifie("ex14 perte d'altitude par seconde (m)", 15 * sina, 1.49, 0.003)
verifie("ex14 puissance dissipée (W)", 80 * G * 15 * sina, 1.17e3, 0.003)
verifie("ex14 énergie dissipée sur 2 km (J)", 80 * G * 2000 * sina, 1.56e5, 0.003)
verifie("ex14 vitesse sans frottement après 2 km (m/s)", math.sqrt(15 ** 2 + 2 * G * 2000 * sina), 64.3, 0.003)


# Exercice 15 : rebonds en Python
def programme15():
    h = [1.50, 1.10, 0.81, 0.59, 0.43]
    for i in range(4):
        print('rebond', i + 1, ':', round(h[i + 1] / h[i], 2))
    k = 0.73
    hauteur, n = h[-1], 4
    while hauteur > 0.05:
        hauteur = hauteur * k
        n = n + 1
    print(n, 'rebonds')


s15 = sortie_de(programme15)
print('   ex15 programme :', s15.replace('\n', ' | '))
if s15 != 'rebond 1 : 0.73\nrebond 2 : 0.74\nrebond 3 : 0.73\nrebond 4 : 0.73\n11 rebonds':
    ECHECS.append('ex15 programme')
verifie("ex15 énergie perdue au premier rebond, 58 g (J)", 0.058 * G * (1.50 - 1.10), 0.228, 0.003)
verifie("ex15 fraction perdue (%)", (1 - 0.73) * 100, 27)

# Défi D16 : station de transfert d'énergie par pompage
E16 = 1000 * 1.0e8 * G * 900
verifie("D16 énergie potentielle stockée (J)", E16, 8.83e14, 0.002)
verifie("D16 énergie potentielle (GWh)", E16 / 3.6e12, 245, 0.003)
verifie("D16 énergie restituée (GWh)", 0.90 * E16 / 3.6e12, 221, 0.003)
verifie("D16 énergie de pompage (GWh)", E16 / 0.85 / 3.6e12, 289, 0.003)
verifie("D16 rendement global", 0.85 * 0.90, 0.765)
verifie("D16 nombre de batteries de 52 kWh", 0.90 * E16 / 3.6e6 / 52, 4.2e6, 0.012)
verifie("D16 puissance de turbinage pour 1 m3/s (MW)", 1000 * 1 * G * 900 * 0.90 / 1e6, 7.95, 0.002)
verifie("D16 débit pour 1800 MW (m3/s)", 1.8e9 / (1000 * G * 900 * 0.90), 226, 0.004)
verifie("D16 durée de vidange à 1800 MW (h)", 1.0e8 / (1.8e9 / (1000 * G * 900 * 0.90)) / 3600, 123, 0.004)
verifie("D16 durée de vidange (s)", 1.0e8 / 226, 4.4e5, 0.01)
verifie("D16 pertes au pompage (GWh)", E16 / 0.85 / 3.6e12 - E16 / 3.6e12, 43.3, 0.003)
verifie("D16 pertes au turbinage (GWh)", 0.10 * E16 / 3.6e12, 24.5, 0.003)
verifie("ex14 vitesse sans frottement (km/h)", 64.3 * 3.6, 230, 0.01)
verifie("ex12 énergie annuelle (MWh)", 3.18e3 * 365, 1.16e6, 0.002)
verifie("ex9 vitesse au départ (J)", 0.5 * 0.15 * 12 ** 2, 10.8)


def programme_d16():
    rho, g, h = 1000, 9.81, 900
    for V in [1e6, 1e7, 1e8]:
        E = rho * V * g * h * 0.90 / 3.6e9
        print(round(V), 'm3 :', round(E), 'MWh')


s16 = sortie_de(programme_d16)
print('   D16 programme :', s16.replace('\n', ' | '))
if s16 != '1000000 m3 : 2207 MWh\n10000000 m3 : 22072 MWh\n100000000 m3 : 220725 MWh':
    ECHECS.append('D16 programme')

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs et sorties du chapitre 16 et du défi D16 sont vérifiées.")
