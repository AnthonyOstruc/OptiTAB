"""Vérification du chapitre 14 (Énergie et puissance électriques) et du défi D14.

Lancer : python -I -X utf8 verifications/chapitre_14.py
"""
import io
import math
from contextlib import redirect_stdout
from itertools import combinations

ECHECS = []
E_CH = 1.60e-19


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
verifie("cours charge, 0,50 A pendant 1 min (C)", 0.50 * 60, 30)
verifie("cours nombre d'électrons", 30 / E_CH, 1.9e20, 0.02)
verifie("cours tension à 0,40 A (V)", 4.5 - 1.5 * 0.40, 3.9)
verifie("cours courant de court-circuit (A)", 4.5 / 1.5, 3.0)
verifie("cours puissance E I (W)", 4.5 * 0.40, 1.80)
verifie("cours puissance U I (W)", 3.9 * 0.40, 1.56)
verifie("cours pertes r I2 (W)", 1.5 * 0.40 ** 2, 0.24)
verifie("cours 1 kWh en J", 1000 * 3600, 3.6e6)


def programme():
    import numpy as np
    I = [0, 0.10, 0.20, 0.30, 0.40, 0.50]
    U = [4.52, 4.36, 4.21, 4.07, 3.90, 3.76]
    a, b = np.polyfit(I, U, 1)
    print('E =', round(b, 2), 'V ; r =', round(-a, 2), 'ohm')


s = sortie_de(programme)
print('   cours programme :', s)
if s != 'E = 4.52 V ; r = 1.52 ohm':
    ECHECS.append('cours programme')
# Exercice 1
verifie("ex1 charge (C)", 0.20 * 60, 12)
verifie("ex1 nombre d'électrons", 12 / E_CH, 7.5e19)
# Exercice 2 : caractéristique
verifie("ex2 tension à 0,40 A (V)", 4.5 - 1.5 * 0.40, 3.9)
verifie("ex2 court-circuit (A)", 4.5 / 1.5, 3.0)
verifie("ex2 puissance fournie à 0,40 A (W)", 3.9 * 0.40, 1.56)
# Exercice 3 : bouilloire et lampes
verifie("ex3 énergie (J)", 2000 * 180, 3.6e5)
verifie("ex3 énergie (kWh)", 2.0 * 3 / 60, 0.10)
verifie("ex3 coût (euros)", 0.10 * 0.25, 0.025)
verifie("ex3 LED 1000 h (kWh)", 7 * 1000 / 1000, 7)
verifie("ex3 incandescence 1000 h (kWh)", 60 * 1000 / 1000, 60)
verifie("ex3 économie (euros)", (60 - 7) * 0.25, 13.25)
# Exercice 4 : effet Joule
verifie("ex4 tension (V)", 47 * 0.10, 4.7)
verifie("ex4 puissance (W)", 47 * 0.10 ** 2, 0.47)
verifie("ex4 énergie en 10 min (J)", 0.47 * 600, 282)
verifie("ex4 intensité maximale (mA)", math.sqrt(0.25 / 47) * 1000, 73, 0.005)
# Exercice 5 : moteur
verifie("ex5 puissance reçue (W)", 12 * 2.5, 30)
verifie("ex5 rendement", 21 / 30, 0.70)
verifie("ex5 pertes en 5 min (J)", (30 - 21) * 300, 2700)


# Exercice 6 : consommation annuelle
def programme6():
    appareils = {'box internet': (12, 24), 'television': (90, 4),
                 'refrigerateur': (150, 8), 'four': (2500, 0.5)}
    total = 0
    for nom, (P, h) in appareils.items():
        E = P * h * 365 / 1000
        total = total + E
        print(nom, ':', round(E), 'kWh')
    print('total :', round(total), 'kWh, soit', round(total * 0.25), 'euros')


s6 = sortie_de(programme6)
print('   ex6 programme :', s6.replace('\n', ' | '))
if s6 != ('box internet : 105 kWh\ntelevision : 131 kWh\nrefrigerateur : 438 kWh\nfour : 456 kWh\n'
          'total : 1131 kWh, soit 283 euros'):
    ECHECS.append('ex6 programme')
verifie("ex6 coût de la box (euros)", 105.12 * 0.25, 26, 0.012)
verifie("ex6 box en veille à 6 W 20 h/j (kWh)", 6 * 20 * 365 / 1000, 43.8)
# Exercice 7 : smartphone
Q7 = 4.000 * 3600
verifie("ex7 charge (C)", Q7, 14400)
verifie("ex7 énergie (J)", 3.85 * Q7, 5.54e4)
verifie("ex7 énergie (Wh)", 3.85 * 4.0, 15.4)
verifie("ex7 nombre d'électrons", Q7 / E_CH, 9.0e22)
verifie("ex7 durée de charge (h)", 15.4 / (18 * 0.85), 1.0, 0.01)
# Exercice 8 : pile
verifie("ex8 court-circuit (A)", 9.0 / 2.0, 4.5)
verifie("ex8 puissance dissipée en court-circuit (W)", 2.0 * 4.5 ** 2, 40.5)
I8 = 9.0 / (2.0 + 16)
verifie("ex8 intensité avec 16 ohms (A)", I8, 0.50)
verifie("ex8 tension (V)", 16 * I8, 8.0)
verifie("ex8 puissance utile (W)", 16 * I8 ** 2, 4.0)
verifie("ex8 pertes internes (W)", 2.0 * I8 ** 2, 0.50)
verifie("ex8 rendement", 4.0 / 4.5, 0.89, 0.002)
# Exercice 9 : batterie
verifie("ex9 tension au démarrage (V)", 12.6 - 0.010 * 200, 10.6)
verifie("ex9 puissance du démarreur (W)", 10.6 * 200, 2.12e3)
verifie("ex9 pertes internes (W)", 0.010 * 200 ** 2, 400)
verifie("ex9 tension par grand froid (V)", 12.6 - 0.030 * 200, 6.6)
# Exercice 10 : bilan de puissance
I10 = 6.0 / (1.0 + 11)
verifie("ex10 intensité (A)", I10, 0.50)
verifie("ex10 tension (V)", 11 * I10, 5.5)
verifie("ex10 puissance de la lampe (W)", 11 * I10 ** 2, 2.75)
verifie("ex10 pertes du générateur (W)", 1.0 * I10 ** 2, 0.25)
verifie("ex10 puissance E I (W)", 6.0 * I10, 3.0)
verifie("ex10 rendement du générateur", 5.5 / 6.0, 0.92, 0.005)
# Exercice 11 : panneau solaire
verifie("ex11 puissance reçue (W)", 1000 * 1.7, 1700)
verifie("ex11 puissance électrique (W)", 34 * 10, 340)
verifie("ex11 rendement", 340 / 1700, 0.20)
verifie("ex11 énergie annuelle (kWh)", 340 * 1300 / 1000, 442)
verifie("ex11 nombre de panneaux", 2500 / 442, 5.7, 0.01)
# Exercice 12 : chauffe-eau
Q12 = 200 * 4180 * 50
verifie("ex12 énergie (J)", Q12, 4.18e7)
verifie("ex12 énergie (kWh)", Q12 / 3.6e6, 11.6, 0.003)
verifie("ex12 durée sans pertes (h)", Q12 / 3000 / 3600, 3.9, 0.01)
verifie("ex12 durée avec rendement 0,90 (h)", Q12 / 0.90 / 3000 / 3600, 4.3, 0.01)
verifie("ex12 intensité (A)", 3000 / 230, 13.0, 0.005)
verifie("ex12 résistance (ohm)", 230 ** 2 / 3000, 17.6, 0.003)
verifie("ex12 énergie consommée (kWh)", Q12 / 3.6e6 / 0.90, 12.9, 0.003)
verifie("ex12 coût (euros)", Q12 / 3.6e6 / 0.90 * 0.20, 2.58, 0.003)
# Exercice 13 : voiture électrique
verifie("ex13 autonomie (km)", 52 / 15 * 100, 347, 0.002)
verifie("ex13 intensité à 100 kW (A)", 1e5 / 400, 250)
verifie("ex13 charge à domicile (h)", 52 / 7.4, 7.0, 0.006)
verifie("ex13 charge avec rendement 0,90 (h)", 52 / 7.4 / 0.90, 7.8, 0.006)
verifie("ex13 charge rapide de 80 % (min)", 0.8 * 52 / 100 * 60, 25, 0.003)
# Exercice 14 : lignes à haute tension
verifie("ex14 intensité à 400 kV (A)", 1e9 / 4e5, 2500)
verifie("ex14 résistance de la ligne (ohm)", 0.030 * 100, 3.0)
verifie("ex14 pertes à 400 kV (W)", 3.0 * 2500 ** 2, 1.875e7)
verifie("ex14 pertes relatives (%)", 3.0 * 2500 ** 2 / 1e9 * 100, 1.9, 0.02)
verifie("ex14 intensité à 20 kV (A)", 1e9 / 2e4, 5.0e4)
verifie("ex14 pertes à 20 kV (W)", 3.0 * 5e4 ** 2, 7.5e9)
verifie("ex14 rapport des pertes", (5e4 / 2500) ** 2, 400)
# Exercice 15 : piles
verifie("ex15 énergie d'une pile AA (Wh)", 1.5 * 2.5, 3.75)
verifie("ex15 énergie d'une pile AA (J)", 3.75 * 3600, 1.35e4)
verifie("ex15 durée avec 0,50 W (h)", 3.75 / 0.50, 7.5)
verifie("ex15 prix du kWh (euros)", 2 / 3.75e-3, 533, 0.002)
verifie("ex15 rapport avec le réseau", 533 / 0.25, 2.1e3, 0.02)
verifie("ex15 accumulateur : prix du kWh (euros)", 5 / (2.4e-3 * 500), 4.2, 0.01)
verifie("ex15 rapport pile / accumulateur", 533 / (5 / 1.2), 130, 0.02)
verifie("ex15 rapport accumulateur / réseau", (5 / 1.2) / 0.25, 17, 0.02)
verifie("ex2 puissance dissipée en court-circuit (W)", 1.5 * 3.0 ** 2, 13.5)
verifie("ex12 énergie électrique consommée (J)", 4.18e7 / 0.90, 4.64e7, 0.002)
verifie("ex12 durée (s)", 4.18e7 / 0.90 / 3000, 1.55e4, 0.002)
verifie("ex14 pertes arrondies (W)", 3.0 * 2500 ** 2, 1.9e7, 0.02)
verifie("ex7 puissance reçue par la batterie (W)", 18 * 0.85, 15.3)
verifie("ex13 énergie pour 80 % (kWh)", 0.80 * 52, 41.6)
verifie("D14 four + plaque + bouilloire (W)", 2500 + 3600 + 2200, 8300)
verifie("D14 pertes arrondies dans la rallonge (W)", 0.567 * (2200 / 230) ** 2, 52, 0.005)

# Défi D14 : le tableau électrique
APP = {'bouilloire': 2200, 'four': 2500, 'plaque': 3600, 'lave-linge': 2000, 'frigo': 150, 'lumiere': 100}
for nom, I in [('bouilloire', 9.57), ('four', 10.9), ('plaque', 15.7), ('lave-linge', 8.70),
               ('frigo', 0.65), ('lumiere', 0.43)]:
    verifie(f"D14 intensité {nom} (A)", APP[nom] / 230, I, 0.013)
verifie("D14 bouilloire + lave-linge (A)", (2200 + 2000) / 230, 18.3, 0.003)
verifie("D14 intensité maximale de l'abonnement (A)", 6000 / 230, 26.1, 0.003)
verifie("D14 four + plaque + frigo (W)", 2500 + 3600 + 150, 6250)


def programme_d14():
    appareils = {'bouilloire': 2200, 'four': 2500, 'plaque': 3600,
                 'lave-linge': 2000, 'frigo': 150, 'lumiere': 100}
    n = 0
    for k in range(1, 7):
        for groupe in combinations(appareils, k):
            if sum(appareils[a] for a in groupe) > 6000:
                n = n + 1
    print(n, 'combinaisons sur 63 font disjoncter')


s14 = sortie_de(programme_d14)
print('   D14 programme :', s14)
if s14 != '25 combinaisons sur 63 font disjoncter':
    ECHECS.append('D14 programme')
R = 1.7e-8 * 50 / 1.5e-6
verifie("D14 résistance de la rallonge (ohm)", R, 0.567, 0.002)
verifie("D14 pertes dans la rallonge (W)", R * (2200 / 230) ** 2, 51.9, 0.003)
verifie("D14 chute de tension (V)", R * 2200 / 230, 5.4, 0.01)
verifie("D14 rallonge 2,5 mm2 (W)", 1.7e-8 * 50 / 2.5e-6 * (2200 / 230) ** 2, 31.1, 0.005)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs et sorties du chapitre 14 et du défi D14 sont vérifiées.")
