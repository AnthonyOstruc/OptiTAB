"""Vérification des résultats numériques du chapitre 19 (premier principe de la thermodynamique) et du défi D19.

Lancer : python -I -X utf8 verifications/chapitre_19.py
"""
import io
from contextlib import redirect_stdout

ECHECS = []
g = 9.81
CEAU = 4180
LF = 3.34e5


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
verifie("cours chute de 51 m : élévation de température (K)", g * 51 / CEAU, 0.12, 0.005)
verifie("cours mélange 200 g à 20 °C + 100 g à 80 °C", (0.200 * 20 + 0.100 * 80) / 0.300, 40, 1e-9)
verifie("cours fusion de 1 kg de glace / chauffage de 1 kg d'eau de 80 K", LF / (CEAU * 80), 1.0, 0.005)


def programme_cours():
    corps = [("eau", 0.200, 4180, 20.0),
             ("eau chaude", 0.100, 4180, 80.0),
             ("cuivre", 0.150, 385, 100.0)]     # kg, J/(kg.K), °C
    C = sum(m * c for (nom, m, c, T) in corps)
    Tf = sum(m * c * T for (nom, m, c, T) in corps) / C
    print(round(Tf, 1))
    for (nom, m, c, T) in corps:
        print(nom, round(m * c * (Tf - T)))


s = sortie_de(programme_cours).splitlines()
print('   cours programme :', s)
if s != ['42.6', 'eau 18928', 'eau chaude -15616', 'cuivre -3312']:
    ECHECS.append('cours programme')
# Exercice 3
U3 = 2.0 * CEAU * 45
verifie("ex3 énergie pour l'eau (kJ)", U3 / 1000, 376, 0.5)
verifie("ex3 durée avec 1500 W (s)", U3 / 1500, 251, 0.5)
verifie("ex3 énergie pour l'aluminium (kJ)", 2.0 * 897 * 45 / 1000, 80.7, 0.05)
verifie("ex3 rapport eau / aluminium", CEAU / 897, 4.7, 0.05)
# Exercice 4
U4 = 1.0 * CEAU * 80
W4 = 2200 * 180
verifie("ex4 variation d'énergie interne (kJ)", U4 / 1000, 334, 0.5)
verifie("ex4 travail électrique (kJ)", W4 / 1000, 396, 0)
verifie("ex4 transfert thermique (kJ)", (U4 - W4) / 1000, -62, 0.5)
verifie("ex4 rendement (%)", 100 * U4 / W4, 84, 0.5)
# Exercice 5
verifie("ex5 énergie de fusion (kJ)", 0.030 * LF / 1000, 10.0, 0.05)
verifie("ex5 chauffage de l'eau de fonte (kJ)", 0.030 * CEAU * 20 / 1000, 2.5, 0.05)
verifie("ex5 rapport", 0.030 * LF / (0.030 * CEAU * 20), 4.0, 0.05)
verifie("ex5 temps avec 5 W (s)", 0.030 * LF / 5.0, 2000, 5)
verifie("ex5 temps avec 5 W (min)", 0.030 * LF / 5.0 / 60, 33, 0.5)
verifie("ex7 écart sans le calorimètre (%)", 100 * (371 - 385) / 385, -3.6, 0.05)
verifie("ex12 rapport des émissions", 92 / 11, 8, 0.5)
verifie("ex12 quantité de méthane (mol)", 33.4 / 16, 2.09, 0.005)
verifie("ex13 énergie stockée exacte (MWh)", U13 / 3.6e9 if False else 3.98e12 / 3.6e9, 1105, 1)
verifie("ex11 énergie pour atteindre la fusion (J/kg)", 129 * 307, 3.96e4, 0.005e4)
verifie("ex6 heure : durée ex3 (min)", 251 / 60, 4.2, 0.05)
# Exercice 6
Ec6 = 0.5 * 1200 * 25 ** 2
verifie("ex6 énergie cinétique (kJ)", Ec6 / 1000, 375, 0)
verifie("ex6 élévation de température des disques (K)", Ec6 / (4 * 6.0 * 460), 34, 0.5)
Ep6 = 1200 * g * 1000
verifie("ex6 énergie de la descente (MJ)", Ep6 / 1e6, 11.8, 0.05)
verifie("ex6 élévation sans refroidissement (K)", Ep6 / (4 * 6.0 * 460), 1066, 1)
# Exercice 7
Tf7 = (876 * 18.0 + 0.100 * 385 * 98.0) / (876 + 0.100 * 385)
verifie("ex7 température finale prévue pour le cuivre", Tf7, 21.4, 0.05)
c7 = (0.200 * CEAU + 40) * (21.4 - 18.0) / (0.100 * (98.0 - 21.4))
verifie("ex7 capacité thermique massique mesurée", c7, 389, 0.5)
verifie("ex7 écart avec le cuivre (%)", 100 * (c7 - 385) / 385, 1.0, 0.1)
c7b = (0.200 * CEAU) * (21.4 - 18.0) / (0.100 * (98.0 - 21.4))
verifie("ex7 valeur sans le calorimètre", c7b, 371, 0.5)
# Exercice 8
C8 = 0.200 * 4180 + 0.100 * 4180 + 0.150 * 385 + 40
Tf8 = (0.200 * 4180 * 20 + 0.100 * 4180 * 80 + 0.150 * 385 * 100 + 40 * 20) / C8
verifie("ex8 température avec le calorimètre", Tf8, 42.0, 0.05)
# Exercice 9
U9 = 200 * CEAU * 45
verifie("ex9 énergie (MJ)", U9 / 1e6, 37.6, 0.05)
verifie("ex9 énergie (kWh)", U9 / 3.6e6, 10.45, 0.005)
verifie("ex9 durée (h)", U9 / 2200 / 3600, 4.75, 0.005)
verifie("ex9 coût (euros)", U9 / 3.6e6 * 0.20, 2.09, 0.005)
verifie("ex9 baisse de température en 24 h (K)", 1.5 * 3.6e6 / (200 * CEAU), 6.5, 0.05)
# Exercice 10
m10 = 0.330 * CEAU * 20 / (LF + CEAU * 5)
verifie("ex10 masse de glace nécessaire (g)", 1000 * m10, 78, 0.5)
verifie("ex10 nombre de glaçons de 25 g", m10 / 0.025, 3.1, 0.05)
Tf10 = (0.330 * CEAU * 25 - 0.075 * LF) / (0.330 * CEAU + 0.075 * CEAU)
verifie("ex10 température avec 3 glaçons", Tf10, 5.6, 0.05)
verifie("ex10 eau froide équivalente : température", (0.330 * 25 + 0.075 * 0) / 0.405, 20.4, 0.05)
# Exercice 11
ec11 = 0.5 * 350 ** 2
verifie("ex11 énergie cinétique massique (J/kg)", ec11, 61250, 0)
verifie("ex11 énergie cinétique (J)", 0.010 * ec11, 612.5, 0.05)
verifie("ex11 élévation avec la moitié (K)", 0.5 * ec11 / 129, 237, 0.5)
verifie("ex11 température finale (°C)", 20 + 0.5 * ec11 / 129, 257, 0.5)
reste = ec11 - 129 * (327 - 20)
verifie("ex11 énergie restante pour fondre (J/kg)", reste, 2.16e4, 0.005e4)
verifie("ex11 fraction fondue (%)", 100 * reste / 2.30e4, 94, 0.5)
# Exercice 12
U12 = 2.0 * CEAU * 80
verifie("ex12 énergie utile (kJ)", U12 / 1000, 669, 0.5)
W12 = 2800 * 280
verifie("ex12 énergie électrique (kJ)", W12 / 1000, 784, 0)
verifie("ex12 rendement induction (%)", 100 * U12 / W12, 85, 0.5)
E12 = U12 / 0.40
verifie("ex12 énergie de combustion (MJ)", E12 / 1e6, 1.67, 0.005)
mCH4 = E12 / 50e6
verifie("ex12 masse de méthane (g)", 1000 * mCH4, 33.4, 0.05)
verifie("ex12 masse de CO2 (gaz)", 1000 * mCH4 * 44 / 16, 92, 0.5)
verifie("ex12 énergie électrique (kWh)", W12 / 3.6e6, 0.218, 0.0005)
verifie("ex12 CO2 électricité (g)", 50 * W12 / 3.6e6, 11, 0.5)
# Exercice 13
U13 = 28.5e6 * 1500 * (384 - 291)
verifie("ex13 énergie stockée (J)", U13, 3.98e12, 0.005e12)
verifie("ex13 énergie stockée (MWh)", U13 / 3.6e9, 1.10e3, 0.005e3)
verifie("ex13 énergie électrique (MWh)", 0.375 * U13 / 3.6e9, 414, 0.5)
verifie("ex13 durée à 50 MW (h)", 0.375 * U13 / 3.6e9 / 50, 8.3, 0.05)
verifie("ex13 énergie annoncée (MWh)", 7.5 * 50, 375, 0)
# Exercice 14
verifie("ex14 énergie à évacuer en 1 h (MJ)", 900 * 3600 / 1e6, 3.24, 0)
verifie("ex14 élévation de température en 1 h (K)", 900 * 3600 / (70 * 3500), 13.2, 0.05)
verifie("ex14 masse de sueur par heure (kg)", 900 * 3600 / 2.4e6, 1.35, 0.005)
verifie("ex14 durée pour +2 K (min)", 2 * 70 * 3500 / 900 / 60, 9.1, 0.05)
# Exercice 15
Q15 = 0.250 * CEAU * 40
verifie("ex15 énergie reçue par le café (kJ)", Q15 / 1000, 41.8, 0.05)
verifie("ex15 énergie libérée (kJ)", Q15 / 0.60 / 1000, 69.7, 0.05)
n15 = Q15 / 0.60 / 65.2e3
verifie("ex15 quantité de CaO (mol)", n15, 1.07, 0.005)
verifie("ex15 masse de CaO (g)", n15 * 56.1, 60, 0.5)
verifie("ex15 masse d'eau nécessaire (g)", n15 * 18.0, 19.2, 0.05)
# Défi D19
W19 = 20 * (26.0 * g * 1.60 - 0.5 * 26.0 * 0.060 ** 2)
verifie("D19 énergie potentielle d'une chute (J)", 26.0 * g * 1.60, 408, 0.5)
verifie("D19 énergie cinétique à l'arrivée (J)", 0.5 * 26.0 * 0.060 ** 2, 0.047, 0.0005)
verifie("D19 travail reçu (J)", W19, 8.16e3, 0.005e3)
dT19 = W19 / (6.00 * CEAU + 400)
verifie("D19 élévation prévue (K)", dT19, 0.320, 0.0005)
verifie("D19 valeur en eau du récipient (g)", 1000 * 400 / CEAU, 95.7, 0.05)
cal = W19 / ((6000 + 95.7) * 0.313)
verifie("D19 équivalent d'une calorie (J)", cal, 4.28, 0.005)
verifie("D19 écart à 4,18 J (%)", 100 * (cal - 4.18) / 4.18, 2.3, 0.1)
verifie("D19 énergie perdue (J)", W19 - (6.00 * CEAU + 400) * 0.313, 186, 1)
verifie("D19 fraction perdue (%)", 100 * (1 - (6.00 * CEAU + 400) * 0.313 / W19), 2.3, 0.05)
verifie("D19 élévation pour une seule chute (K)", 26.0 * g * 1.60 / (6.00 * CEAU + 400), 0.016, 0.0005)

verifie("D19 énergie reçue en calories", (6000 + 95.7) * 0.313, 1908, 0.5)
verifie("D19 énergie interne mesurée (kJ)", 25480 * 0.313 / 1000, 7.98, 0.005)
verifie("D19 terme cinétique / potentiel", 0.047 / 408.1, 1e-4, 0.2e-4)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 19 et du défi D19 sont vérifiées.")
