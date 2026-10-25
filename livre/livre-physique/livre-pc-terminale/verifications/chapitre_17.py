"""Vérification des résultats numériques du chapitre 17 (écoulement des fluides) et du défi D17.

Lancer : python -I -X utf8 verifications/chapitre_17.py
"""
import io
from contextlib import redirect_stdout
from math import pi, sqrt

ECHECS = []
g = 9.81
RHO = 1000          # eau (kg/m³)
PATM = 1.013e5      # Pa


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


def disque(d):
    return pi * d ** 2 / 4


# L'essentiel
verifie("cours iceberg : fraction immergée (%)", 100 * 917 / 1025, 89, 0.5)
verifie("cours iceberg : fraction émergée (%)", 100 - 100 * 917 / 1025, 11, 0.5)
verifie("cours glaçon dans l'eau douce (%)", 100 * 917 / 1000, 91.7, 0.05)
verifie("cours pavé : poussée pour 1 L d'eau (N)", RHO * 1e-3 * g, 9.81, 0.005)
D = 5.0e-3 / 60
verifie("cours débit cardiaque (m³/s)", D, 8.3e-5, 0.05e-5)
verifie("cours vitesse dans l'aorte (m/s)", D / disque(0.025), 0.17, 0.005)
verifie("cours vitesse dans les capillaires (mm/s)", 1000 * D / 0.25, 0.33, 0.005)
verifie("cours Torricelli h = 1,25 m", sqrt(2 * g * 1.25), 4.95, 0.005)
verifie("cours activité : masse volumique de l'eau salée", 10.1 / (1e-3 * g), 1.03e3, 0.005e3)


def programme_cours():
    S = pi * 0.050 ** 2       # section du récipient (m²)
    s = pi * 0.002 ** 2       # section de l'orifice (m²)
    h, t, dt = 0.20, 0.0, 0.01
    while h > 0:
        v = sqrt(2 * g * h)           # formule de Torricelli
        h = h - s / S * v * dt        # conservation du débit
        t = t + dt
    T = S / s * sqrt(2 * 0.20 / g)   # exacte
    print(round(t, 1), round(T, 1))


s = sortie_de(programme_cours)
print('   cours programme :', s)
if s != '126.2 126.2':
    ECHECS.append('cours programme vidange')
# Exercice 1
ph, pb = PATM + RHO * g * 0.200, PATM + RHO * g * 0.300
verifie("ex1 pression face supérieure", ph, 1.033e5, 0.0005e5)
verifie("ex1 pression face inférieure", pb, 1.042e5, 0.0005e5)
verifie("ex1 force face supérieure", ph * 0.01, 1033, 0.5)
verifie("ex1 force face inférieure", pb * 0.01, 1042, 0.5)
verifie("ex1 résultante", (pb - ph) * 0.01, 9.81, 0.005)
# Exercice 2
PI2 = 9.810 - 9.180
V2 = PI2 / (RHO * g)
verifie("ex2 poussée", PI2, 0.630, 0.0005)
verifie("ex2 volume (cm³)", V2 * 1e6, 64.2, 0.05)
verifie("ex2 masse volumique", 1.000 / V2, 1.56e4, 0.005e4)
verifie("ex2 volume d'or pur (cm³)", 1e6 / 19300, 51.8, 0.05)
verifie("ex2 indication pour de l'or pur", 9.810 - RHO * g / 19300, 9.30, 0.005)
# Exercice 3
D3 = 10.0e-3 / 50
verifie("ex3 débit (m³/s)", D3, 2.0e-4, 1e-9)
verifie("ex3 débit (L/min)", D3 * 6e4, 12, 0.05)
v3 = D3 / disque(0.015)
verifie("ex3 vitesse dans le tuyau", v3, 1.13, 0.005)
v3b = D3 / disque(0.005)
verifie("ex3 vitesse dans l'embout", v3b, 10.2, 0.05)
verifie("ex3 rapport des vitesses", v3b / v3, 9, 1e-9)
verifie("ex3 hauteur du jet vertical", v3b ** 2 / (2 * g), 5.3, 0.05)
# Exercice 4
dp4 = 0.5 * RHO * (2.0 ** 2 - 0.50 ** 2)
verifie("ex4 vitesse dans l'étranglement", 4 * 0.50, 2.0, 1e-9)
verifie("ex4 différence de pression", dp4, 1.9e3, 0.05e3)
verifie("ex4 différence de hauteur (cm)", 100 * dp4 / (RHO * g), 19, 0.5)
# Exercice 5
v5 = sqrt(2 * g * 0.80)
verifie("ex5 vitesse", v5, 3.96, 0.005)
D5 = v5 * disque(0.010)
verifie("ex5 débit (L/s)", 1000 * D5, 0.31, 0.005)
verifie("ex5 débit (L/min)", 6e4 * D5, 18.7, 0.05)
t5 = sqrt(2 * 0.50 / g)
verifie("ex5 durée de chute", t5, 0.319, 0.0005)
verifie("ex5 portée", v5 * t5, 1.26, 0.005)
# Exercice 6
P6 = 1.20 * 3.0 * g
m6 = 1.50 + 0.17 * 3.0
verifie("ex6 poussée", P6, 35.3, 0.05)
verifie("ex6 masse d'hélium", 0.17 * 3.0, 0.51, 1e-9)
verifie("ex6 masse totale", m6, 2.01, 1e-9)
verifie("ex6 poids", m6 * g, 19.7, 0.05)
verifie("ex6 résultante", P6 - m6 * g, 15.6, 0.05)
verifie("ex6 accélération initiale", (P6 - m6 * g) / m6, 7.8, 0.05)
# Exercice 7
D7 = disque(6.0e-3) * 0.40
verifie("ex7 débit (m³/s)", D7, 1.13e-5, 0.005e-5)
verifie("ex7 débit (L/min)", 6e4 * D7, 0.68, 0.005)
verifie("ex7 vitesse dans la sténose", 0.40 * 4, 1.6, 1e-9)
dp7 = 0.5 * 1060 * (1.6 ** 2 - 0.40 ** 2)
verifie("ex7 chute de pression (Pa)", dp7, 1.27e3, 0.005e3)
verifie("ex7 chute de pression (mmHg)", dp7 / 133.3, 9.5, 0.05)
# Exercice 8
v8 = sqrt(2 * g * 0.120 / ((20 / 5.0) ** 2 - 1))
verifie("ex8 vitesse en A", v8, 0.40, 0.005)
verifie("ex8 vitesse en B", 4 * v8, 1.58, 0.005)
D8 = 20e-4 * v8
verifie("ex8 débit (L/s)", 1000 * D8, 0.79, 0.005)
verifie("ex8 débit (m³/h)", 3600 * D8, 2.85, 0.005)
verifie("ex8 Δh pour un débit double (cm)", 4 * 12.0, 48, 1e-9)
# Exercice 9
verifie("ex9 durée si le diamètre double", 126.2 / 4, 32, 0.5)
verifie("ex9 coefficient de contraction", 126.2 / 152, 0.83, 0.005)
for t, h in ((0, 20.0), (40, 9.3), (80, 2.7), (126.2, 0.0)):
    verifie(f"figure ex9 : h à t = {t} s (cm)", 100 * (sqrt(0.20) - 0.0016 * sqrt(g / 2) * t) ** 2, h, 0.05)
verifie("figure ex9 : pente à l'origine (cm/s)", 100 * 0.0016 * sqrt(2 * g * 0.20), 0.317, 0.0005)
verifie("figure ex9 : tangente nulle à t (s)", 20 / 0.317, 63, 0.5)
# Exercice 10
m10, S10 = 0.0240, 2.00e-4
verifie("ex10 enfoncement dans l'eau (cm)", 100 * m10 / (RHO * S10), 12.0, 0.05)
verifie("ex10 masse volumique du liquide", m10 / (S10 * 0.100), 1200, 0.5)
verifie("ex10 masse volumique minimale", m10 / (S10 * 0.150), 800, 0.5)
verifie("ex10 graduation 1 100 (cm)", 100 * m10 / (1100 * S10), 10.9, 0.05)
# Exercice 11
verifie("ex11 pression au rez-de-chaussée", PATM + RHO * g * 35, 4.45e5, 0.005e5)
verifie("ex11 pression au troisième étage", PATM + RHO * g * 26, 3.56e5, 0.005e5)
verifie("ex11 vitesse théorique", sqrt(2 * g * 35), 26.2, 0.05)
verifie("ex11 vitesse mesurée", 12e-3 / 60 / 1.0e-4, 2.0, 1e-9)
# Exercice 12
verifie("ex12 vitesse de croisière (m/s)", sqrt(2 * 12.8e3 / 0.41), 250, 0.5)
verifie("ex12 vitesse de croisière (km/h)", 3.6 * sqrt(2 * 12.8e3 / 0.41), 900, 1)
verifie("ex12 Δp au décollage (kPa)", 0.5 * 1.22 * (280 / 3.6) ** 2 / 1000, 3.7, 0.05)
verifie("ex12 vitesse indiquée (km/h)", 3.6 * sqrt(2 * 12.8e3 / 1.22), 520, 2)
# Exercice 13
D13 = 0.500 / 60
v13a, v13b = D13 / disque(0.070), D13 / disque(0.022)
verifie("ex13 débit (m³/s)", D13, 8.33e-3, 0.005e-3)
verifie("ex13 vitesse dans le tuyau", v13a, 2.17, 0.005)
verifie("ex13 vitesse à la sortie", v13b, 21.9, 0.05)
verifie("ex13 surpression (Pa)", 0.5 * RHO * (v13b ** 2 - v13a ** 2), 2.4e5, 0.05e5)
verifie("ex13 hauteur théorique", v13b ** 2 / (2 * g), 24.5, 0.05)
verifie("ex13 vitesse pour 20 m", sqrt(2 * g * 20), 19.8, 0.05)
# Exercice 14
r15, r100, r30 = 353 / 288, 353 / 373, 353 / 303
verifie("ex14 masse volumique à 15 °C", r15, 1.23, 0.005)
verifie("ex14 masse volumique à 100 °C", r100, 0.946, 0.0005)
verifie("ex14 poussée", r15 * 2500 * g, 3.01e4, 0.005e4)
verifie("ex14 poids de l'air chaud", r100 * 2500 * g, 2.32e4, 0.005e4)
cap = (r15 - r100) * 2500
verifie("ex14 masse soulevable (kg)", cap, 698, 1)
verifie("ex14 charge utile (kg)", cap - 400, 298, 1)
verifie("ex14 nombre de personnes", (cap - 400) // 80, 3, 0)
cap30 = (r30 - r100) * 2500
verifie("ex14 masse volumique à 30 °C", r30, 1.165, 0.0005)
verifie("ex14 charge utile à 30 °C (kg)", cap30 - 400, 147, 1)
verifie("ex14 personnes à 30 °C", (cap30 - 400) // 80, 1, 0)
verifie("ex14 charge utile à 30 °C, air à 120 °C (kg)", (r30 - 353 / 393) * 2500 - 400, 266, 1)
# Exercice 15
v15 = 20 / disque(2.0)
verifie("ex15 vitesse dans la conduite", v15, 6.37, 0.005)
p15 = PATM + RHO * g * 600 - 0.5 * RHO * v15 ** 2
verifie("ex15 pression à l'entrée de la turbine", p15, 5.97e6, 0.005e6)
verifie("ex15 terme cinétique (Pa)", 0.5 * RHO * v15 ** 2, 2.0e4, 0.05e4)
P15 = RHO * g * 600 * 20
verifie("ex15 puissance hydraulique (MW)", P15 / 1e6, 118, 0.5)
verifie("ex15 puissance électrique (MW)", 0.90 * P15 / 1e6, 106, 0.5)
verifie("ex15 énergie annuelle (GWh)", 0.90 * P15 * 3000 / 1e9, 318, 0.5)
verifie("ex15 nombre de foyers", 0.90 * P15 * 3000 / 4.5e6, 7.1e4, 0.05e4)
# Valeurs intermédiaires des corrigés
verifie("cor2 volume d'or (m³)", 1 / 19300, 5.18e-5, 0.005e-5)
verifie("cor2 poussée sur l'or pur", RHO * g / 19300, 0.508, 0.0005)
verifie("cor3 section du tuyau", disque(0.015), 1.77e-4, 0.005e-4)
verifie("cor5 section de l'orifice", disque(0.010), 7.85e-5, 0.005e-5)
verifie("cor5 débit (m³/s)", D5, 3.11e-4, 0.005e-4)
verifie("cor7 section de l'artère", disque(6.0e-3), 2.83e-5, 0.005e-5)
verifie("cor8 débit (m³/s)", D8, 7.9e-4, 0.05e-4)
verifie("cor9 écart relatif (%)", 100 * (1 - 126.2 / 152), 17, 0.5)
verifie("cor12 vitesse au décollage", 280 / 3.6, 77.8, 0.05)
verifie("cor12 vitesse indiquée (m/s)", sqrt(2 * 12.8e3 / 1.22), 145, 0.5)
verifie("cor14 masse de 4 personnes", 4 * 80, 320, 0)
verifie("cor15 terme cinétique / rho g h (%)", 100 * 0.5 * RHO * v15 ** 2 / (RHO * g * 600), 0.3, 0.05)
verifie("cor15 rho g h (Pa)", RHO * g * 600, 5.886e6, 1)
verifie("cor15 énergie (MWh)", 106 * 3000, 3.18e5, 0)
# Défi D17
H, R = 0.30, 0.10
u = H / (12 * 3600)
s17 = pi * u * R ** 2 / sqrt(2 * g * H)
verifie("D17 vitesse de descente (cm/h)", 100 * u * 3600, 2.5, 1e-9)
verifie("D17 vitesse de descente (m/s)", u, 6.94e-6, 0.005e-6)
for a, b, baisse in ((30.0, 23.0, 7.0), (23.0, 16.9, 6.1), (16.9, 11.7, 5.2), (11.7, 7.5, 4.2)):
    verifie(f"D17 baisse du cylindre de {a} à {b} cm", a - b, baisse, 1e-9)
verifie("D17 section de l'orifice", s17, 9.0e-8, 0.05e-8)
verifie("D17 diamètre de l'orifice (mm)", 2000 * sqrt(s17 / pi), 0.34, 0.005)
verifie("D17 rayon à mi-hauteur (cm)", 100 * R * 0.5 ** 0.25, 8.41, 0.005)
verifie("D17 rayon à 2 cm du fond (cm)", 100 * R * (2 / 30) ** 0.25, 5.08, 0.005)
verifie("D17 durée de vidange du cylindre (h)", pi * R ** 2 / 9.0e-8 * sqrt(2 * H / g) / 3600, 24.0, 0.05)
verifie("D17 cylindre : niveau après 12 h (cm)", 100 * H / 4, 7.5, 1e-9)


def programme_d17():
    s = 9.0e-8                    # orifice (m²)

    def niveau(p, duree):
        h, t, dt = H, 0, 1
        while t < duree and h > 0:
            r = R * (h / H)**p
            v = sqrt(2 * g * h)
            h = h - s*v / (pi*r**2) * dt
            t = t + dt
        return round(100 * max(h, 0.0), 1)

    for n in range(0, 13, 3):
        T = 3600 * n
        print(n, niveau(0, T), niveau(0.25, T))


s = sortie_de(programme_d17).splitlines()
print('   D17 sorties :', s)
if s != ['0 30.0 30.0', '3 23.0 22.5', '6 16.9 15.0', '9 11.7 7.5', '12 7.5 0.0']:
    ECHECS.append('D17 sorties')
for t, hc in ((0, 30.0), (3, 23.0), (6, 16.9), (9, 11.7), (12, 7.5), (24, 0.0)):
    verifie(f"figure D17 : cylindre à {t} h (cm)", 100 * H * (1 - t / 24) ** 2, hc, 0.06)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 17 et du défi D17 sont vérifiées.")
