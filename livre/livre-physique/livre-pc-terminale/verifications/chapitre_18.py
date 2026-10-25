"""Vérification des résultats numériques du chapitre 18 (modèle du gaz parfait) et du défi D18.

Lancer : python -I -X utf8 verifications/chapitre_18.py
"""
import io
from contextlib import redirect_stdout
from math import ceil, log, pi

ECHECS = []
R = 8.314
NA = 6.022e23
g = 9.81


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


def K(theta):
    return theta + 273.15


# L'essentiel
n1L = 1.00e5 * 1e-3 / (R * K(20))
verifie("cours 1 L d'air : quantité (mol)", n1L, 0.041, 0.0005)
verifie("cours 1 L d'air : nombre de molécules", n1L * NA, 2.5e22, 0.05e22)
verifie("cours volume molaire à 20 °C (L/mol)", 1000 * R * K(20) / 1.013e5, 24.1, 0.05)
verifie("cours volume molaire à 0 °C (L/mol)", 1000 * R * K(0) / 1.013e5, 22.4, 0.05)
verifie("cours masse volumique de l'air", 1.013e5 * 0.0290 / (R * K(20)), 1.21, 0.005)
verifie("cours écart du volume molaire de CO2 (%)", 100 * (22.41 - 22.26) / 22.41, 0.7, 0.05)
for theta, p in ((0, 1000), (20, 1073), (40, 1146), (60, 1220), (80, 1293)):
    verifie(f"figure zéro absolu : p à {theta} °C (hPa)", 1000 * K(theta) / 273.15, p, 0.5)


def programme_cours():
    V = [60.0, 50.0, 40.0, 30.0, 20.0]         # mL
    p = [1013, 1218, 1521, 2024, 3035]         # hPa
    R, T = 8.314, 293.0                        # SI, K
    for k in range(5):
        n = p[k] * 1e2 * V[k] * 1e-6 / (R * T)
        print(V[k], round(p[k] * V[k]), round(1000 * n, 3))


s = sortie_de(programme_cours).splitlines()
print('   cours programme :', s)
ATTENDU_COURS = ['60.0 60780 2.495', '50.0 60900 2.5', '40.0 60840 2.498', '30.0 60720 2.493', '20.0 60700 2.492']
if s != ATTENDU_COURS:
    ECHECS.append('cours programme')
# Exercice 2
verifie("ex2 volume molaire à 0 °C", 1000 * R * K(0) / 1.013e5, 22.4, 0.05)
n2 = 1.013e5 * 50 / (R * K(20))
verifie("ex2 quantité d'air dans la pièce (mol)", n2, 2.08e3, 0.005e3)
verifie("ex2 masse d'air (kg)", n2 * 0.0290, 60.3, 0.05)
n2b = n2 * K(20) / K(25)
verifie("ex2 quantité à 25 °C", n2b, 2.04e3, 0.005e3)
verifie("ex2 quantité sortie (mol)", n2 - n2b, 35, 0.5)
verifie("ex2 masse sortie (kg)", (n2 - n2b) * 0.0290, 1.0, 0.05)
# Exercice 3
verifie("ex3 pression à 20 mL (hPa)", 1013 * 50 / 20, 2.53e3, 0.005e3)
verifie("ex3 force sur le piston (N)", (1013 * 50 / 20 - 1013) * 100 * 2.5e-4, 38, 0.5)
verifie("ex3 pression à 80 mL (hPa)", 1013 * 50 / 80, 633, 0.5)
# Exercice 4
p4 = 3.30 * K(50) / K(10)
verifie("ex4 pression absolue à chaud (bar)", p4, 3.77, 0.005)
verifie("ex4 pression relative à chaud (bar)", p4 - 1.00, 2.77, 0.005)
verifie("ex4 hausse relative (%)", 100 * (K(50) / K(10) - 1), 14, 0.5)
# Exercice 5
verifie("ex5 masse volumique de l'air", 1.013e5 * 0.0290 / (R * K(20)), 1.21, 0.005)
verifie("ex5 masse volumique de l'hélium", 1.013e5 * 0.0040 / (R * K(20)), 0.166, 0.0005)
verifie("ex5 masse volumique du CO2", 1.013e5 * 0.0440 / (R * K(20)), 1.83, 0.005)
verifie("ex5 rapport CO2/air", 44.0 / 29.0, 1.52, 0.005)
# Exercice 6
n6 = 200e5 * 0.012 / (R * K(20))
verifie("ex6 quantité d'air (mol)", n6, 98.5, 0.05)
verifie("ex6 volume détendu à 1 bar (L)", 12 * 200, 2400, 0)
p6 = 200 * K(12) / K(20)
verifie("ex6 pression à 12 °C (bar)", p6, 194.5, 0.05)
verifie("ex6 volume utilisable (L)", 12 * (194.5 - 50), 1734, 0.5)
verifie("ex6 autonomie (min)", 12 * (194.5 - 50) / (20 * 3.0), 28.9, 0.05)
# Exercice 7
p7 = 1.013e5 + 1025 * g * 20
verifie("ex7 pression à 20 m (Pa)", p7, 3.02e5, 0.005e5)
verifie("ex7 volume en surface (cm³)", 1.0 * p7 / 1.013e5 * K(18) / K(12), 3.0, 0.05)
verifie("ex7 volume sans effet de température (cm³)", 1.0 * p7 / 1.013e5, 2.99, 0.005)
verifie("ex7 effet de la température (%)", 100 * (K(18) / K(12) - 1), 2.1, 0.05)
verifie("ex7 poumons : volume en surface (L)", 6.0 * p7 / 1.013e5, 18, 0.5)
# Exercice 8
verifie("ex8 pente nRT (J)", 60780 * 100 * 1e-6, 6.08, 0.005)
verifie("ex8 pression à 20 mL et 35 °C (hPa)", 3035 * K(35) / 293.0, 3.19e3, 0.005e3)
# Exercice 9
theta9 = [10, 30, 50, 70, 90]
p9 = [881, 944, 1005, 1068, 1130]
for t, p in zip(theta9, p9):
    verifie(f"ex9 donnée {t} °C (modèle)", 850 * K(t) / 273.15, p, 1.0)
a9 = (p9[-1] - p9[0]) / (theta9[-1] - theta9[0])
verifie("ex9 coefficient directeur (hPa/°C)", a9, 3.11, 0.005)
b9 = p9[0] - a9 * theta9[0]
verifie("ex9 ordonnée à l'origine (hPa)", b9, 850, 0.5)
verifie("ex9 température où p = 0 (°C)", -b9 / a9, -273, 1)
# Exercice 10
p10 = 1013 * K(-18) / K(25)
verifie("ex10 pression dans la bouteille (hPa)", p10, 867, 0.5)
verifie("ex10 écart de pression (hPa)", 1013 - p10, 146, 0.5)
verifie("ex10 force sur la face (N)", (1013 - p10) * 100 * 1.0e-2, 146, 0.5)
verifie("ex10 masse équivalente (kg)", (1013 - p10) * 100 * 1.0e-2 / g, 14.9, 0.05)
verifie("ex10 volume à 1013 hPa (L)", 1.5 * K(-18) / K(25), 1.28, 0.005)
# Exercice 11
Vm0 = 1000 * R * K(0) / 1.01325e5
verifie("ex11 volume molaire parfait (L/mol)", Vm0, 22.41, 0.005)
for gaz, vm, ecart in (("N2", 22.40, -0.04), ("O2", 22.39, -0.09), ("CO2", 22.26, -0.7), ("NH3", 22.09, -1.4)):
    verifie(f"ex11 écart pour {gaz} (%)", 100 * (vm - 22.41) / 22.41, ecart, 0.05 if abs(ecart) > 0.5 else 0.006)
n11 = 2000 / 44.0
verifie("ex11 quantité de CO2 (mol)", n11, 45.5, 0.05)
verifie("ex11 pression prévue (bar)", n11 * R * K(20) / 0.0030 / 1e5, 369, 1)
# Exercice 12
n12 = 1.30e5 * 0.060 / (R * K(50))
verifie("ex12 quantité de diazote (mol)", n12, 2.90, 0.005)
verifie("ex12 quantité d'azoture (mol)", 2 / 3 * n12, 1.94, 0.005)
verifie("ex12 masse d'azoture (g)", 2 / 3 * n12 * 65.0, 126, 0.5)
verifie("ex12 pression après refroidissement (bar)", 1.30 * K(20) / K(50), 1.18, 0.005)
# Exercice 13
n13 = 101300 * 3.0 / (R * K(15))
verifie("ex13 quantité d'hélium (mol)", n13, 127, 0.5)
V30 = n13 * R * 226.5 / 1197
verifie("ex13 volume à 30 km (m³)", V30, 200, 1)
verifie("ex13 diamètre au sol (m)", (6 * 3.0 / pi) ** (1 / 3), 1.79, 0.005)
verifie("ex13 diamètre à 30 km (m)", (6 * V30 / pi) ** (1 / 3), 7.3, 0.05)
verifie("ex13 volume à l'éclatement (m³)", pi * 8.0 ** 3 / 6, 268, 0.5)
verifie("ex13 volume à 35 km (m³)", n13 * R * 236.5 / 575, 434, 1)
verifie("ex13 volume à 25 km (m³)", n13 * R * 221.6 / 2549, 91.7, 0.05)
# Exercice 14
r14 = (337 / K(-25)) / (1013 / K(15))
verifie("ex14 rapport des quantités par litre (%)", 100 * r14, 39, 0.5)
verifie("ex14 masse volumique au sommet", 33700 * 0.0290 / (R * K(-25)), 0.474, 0.0005)
verifie("ex14 masse volumique au niveau de la mer", 101300 * 0.0290 / (R * K(15)), 1.23, 0.005)
verifie("ex14 O2 dans 1 L au niveau de la mer (mmol)", 1000 * 0.21 * 101300 * 1e-3 / (R * K(15)), 8.9, 0.05)
verifie("ex14 O2 dans 1 L au sommet (mmol)", 1000 * 0.21 * 33700 * 1e-3 / (R * K(-25)), 3.4, 0.05)
verifie("ex14 rapport dans les poumons (%)", 100 * 337 / 1013, 33, 0.5)
# Exercice 15
T15 = K(30) * 45 / 16
verifie("ex15 volume final (cm³)", 500 / 16, 31.25, 1e-9)
verifie("ex15 température finale (K)", T15, 853, 0.5)
verifie("ex15 température finale (°C)", T15 - 273.15, 579, 0.5)
verifie("ex15 pression si isotherme (bar)", 1.0 * 16, 16, 0)
n15 = 1.0e5 * 500e-6 / (R * K(30))
verifie("ex15 quantité d'air (mol)", n15, 0.0198, 0.00005)
verifie("ex15 masse d'air (g)", 1000 * n15 * 0.0290, 0.575, 0.0005)
# Valeurs intermédiaires des corrigés
verifie("cor5 rapport air/hélium", 29.0 / 4.0, 7.3, 0.05)
pv = [60780, 60900, 60840, 60720, 60700]
moy = sum(pv) / 5
verifie("cor8 moyenne de pV (hPa.mL)", moy, 60800, 50)
verifie("cor8 écart maximal à la moyenne (%)", 100 * max(abs(x - moy) for x in pv) / moy, 0.2, 0.05)
verifie("cor8 incertitude relative de lecture à 20 mL (%)", 100 * 0.5 / 20, 2.5, 0.5)
verifie("cor8 incertitude relative de lecture à 60 mL (%)", 100 * 0.5 / 60, 0.8, 0.2)
verifie("cor13 rapport des volumes 30 km / sol", 200 / 3.0, 67, 0.5)
# Défi D18
q = 1.0 / 1.050
verifie("D18 pression après un coup (hPa)", 1013 * q, 965, 0.5)
verifie("D18 nombre de coups pour 1 hPa", ceil(log(1013) / log(1.05)), 142, 0)
verifie("D18 fraction retirée par coup (%)", 100 * (1 - q), 4.8, 0.05)
verifie("D18 pression limite (hPa)", 1013 * 0.0005 / 0.0505, 10.0, 0.05)
verifie("D18 coups pour atteindre 20 hPa sans volume mort", ceil(log(1013 / 20) / log(1.05)), 81, 0)
q2 = 1.0 / 1.0505
plim = 1013 * 0.0005 / 0.0505
k20 = ceil(log((1013 - plim) / (20 - plim)) / log(1 / q2))
verifie("D18 coups pour 20 hPa avec volume mort", k20, 94, 0)
verifie("D18 coups pour 11 hPa avec volume mort", ceil(log((1013 - plim) / (11 - plim)) / log(1 / q2)), 141, 0)
verifie("D18 pompe à vélo : pression après 30 coups (bar)", 1.0 + 30 * 1.0 * 0.10 / 1.5, 3.0, 1e-9)


def programme_d18():
    p0, V, v, vm = 1013, 1.0, 0.050, 0.0      # hPa, L, L, L
    p, k = p0, 0
    while p > 1 and k < 1000:
        p = (p * V + p0 * vm) / (V + v + vm)
        k = k + 1
    print(k, round(p, 3))


def programme_d18_volume_mort():
    p0, V, v, vm = 1013, 1.0, 0.050, 0.0005
    p, k = p0, 0
    while p > 1 and k < 1000:
        p = (p * V + p0 * vm) / (V + v + vm)
        k = k + 1
    print(k, round(p, 3))


s = sortie_de(programme_d18)
print('   D18 sortie :', s)
if s != '142 0.992':
    ECHECS.append('D18 sortie')
s = sortie_de(programme_d18_volume_mort)
print('   D18 sortie avec volume mort :', s)
if s != '1000 10.03':
    ECHECS.append('D18 sortie avec volume mort')
for k, p in ((0, 1013), (40, 144), (80, 20.4), (120, 2.9), (142, 1.0)):
    verifie(f"figure D18 : sans volume mort, k = {k}", 1013 * q ** k, p, 0.05 * p)
for k, p in ((40, 154), (80, 30.8), (120, 12.6), (160, 10.4)):
    verifie(f"figure D18 : avec volume mort, k = {k}", plim + (1013 - plim) * q2 ** k, p, 0.05 * p)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 18 et du défi D18 sont vérifiées.")
