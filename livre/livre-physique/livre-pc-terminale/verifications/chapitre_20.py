"""Vérification des résultats numériques du chapitre 20 (transferts thermiques et bilans) et du défi D20.

Lancer : python -I -X utf8 verifications/chapitre_20.py
"""
import io
from contextlib import redirect_stdout
from math import exp, log

ECHECS = []
SIGMA = 5.67e-8
S0 = 1361
CEAU = 4180


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


def teq(S, A):
    return ((1 - A) * S / (4 * SIGMA)) ** 0.25


# L'essentiel
R_beton = 0.20 / (1.75 * 10)
R_laine = 0.10 / (0.040 * 10)
verifie("cours résistance du béton (K/W)", R_beton, 0.0114, 0.00005)
verifie("cours flux à travers le béton (W)", 20 / R_beton, 1.75e3, 0.005e3)
verifie("cours résistance de la laine (K/W)", R_laine, 0.25, 1e-9)
verifie("cours flux avec isolant (W)", 20 / (R_beton + R_laine), 77, 0.5)
verifie("cours température à l'interface béton-laine", 20 - 20 / (R_beton + R_laine) * R_beton, 19.1, 0.05)
verifie("cours rapport des flux", (R_beton + R_laine) / R_beton, 23, 0.5)
verifie("cours puissance moyenne reçue (W/m²)", S0 / 4, 340, 0.5)
verifie("cours puissance absorbée (W/m²)", 0.70 * S0 / 4, 238, 0.5)
verifie("cours température sans effet de serre (K)", teq(S0, 0.30), 255, 0.5)
verifie("cours température sans effet de serre (°C)", round(teq(S0, 0.30)) - 273, -18, 0)
verifie("cours écart avec 15 °C (K)", 288 - teq(S0, 0.30), 33, 0.5)
verifie("cours facteur après une durée tau (%)", 100 * exp(-1), 37, 0.5)
verifie("cours facteur après 5 tau (%)", 100 * exp(-5), 0.7, 0.05)
for t, T in ((0, 80), (1500, 42.1), (3000, 28.1), (4500, 23.0)):
    verifie(f"figure Newton : T à {t} s", 20 + 60 * exp(-t / 1500), T, 0.05)


def programme_cours():
    Text, T0, tau = 20.0, 80.0, 1500.0   # °C, °C, s
    T, t, dt = T0, 0.0, 10.0
    while t < 3600:
        T = T + (Text - T) / tau * dt
        t = t + dt
    print(round(T, 2), round(Text + (T0 - Text) * exp(-t / tau), 2))


s = sortie_de(programme_cours)
print('   cours programme :', s)
if s != '25.4 25.44':
    ECHECS.append('cours programme')
# Exercice 2
R2 = 0.040 / (0.15 * 2.0)
verifie("ex2 résistance de la porte (K/W)", R2, 0.133, 0.0005)
verifie("ex2 flux (W)", 19 / R2, 143, 0.5)
verifie("ex2 énergie en 24 h (MJ)", 19 / R2 * 86400 / 1e6, 12.3, 0.05)
verifie("ex2 énergie en 24 h (kWh)", 19 / R2 * 24 / 1000, 3.42, 0.005)
verifie("ex2 épaisseur de bois pour diviser par 2 (cm)", 8.0, 8.0, 0)
# Exercice 3
verifie("ex3 Soleil (W/m²)", SIGMA * 5772 ** 4, 6.29e7, 0.005e7)
verifie("ex3 Terre à 288 K (W/m²)", SIGMA * 288 ** 4, 390, 0.5)
verifie("ex3 peau à 306 K (W/m²)", SIGMA * 306 ** 4, 497, 0.5)
verifie("ex3 rapport Soleil / Terre", (5772 / 288) ** 4, 1.61e5, 0.005e5)
verifie("ex3 doublement de T", 2 ** 4, 16, 0)
# Exercice 4
verifie("ex4 température à tau", 20 + 65 * exp(-1), 43.9, 0.05)
verifie("ex4 température à 2 tau", 20 + 65 * exp(-2), 28.8, 0.05)
verifie("ex4 température à 3 tau", 20 + 65 * exp(-3), 23.2, 0.05)
verifie("ex4 durée pour 60 °C (min)", 20 * log(65 / 40), 9.7, 0.05)
# Exercice 5
for nom, A, P in (("neige fraîche", 0.85, 51), ("forêt", 0.15, 289), ("océan", 0.06, 320)):
    verifie(f"ex5 puissance absorbée, {nom}", (1 - A) * 340, P, 0.5)
# Exercice 6
for nom, R, P in (("simple", 0.115, 174), ("double", 0.238, 84), ("double performant", 0.606, 33)):
    verifie(f"ex6 flux {nom} pour 20 K (W)", 20 / R, P, 0.5)
verifie("ex6 coefficient U simple (W/m²/K)", 1 / (0.115 * 1.5), 5.8, 0.05)
gain = 12 / 0.115 - 12 / 0.606
verifie("ex6 puissance économisée (W)", gain, 84.5, 0.05)
verifie("ex6 énergie économisée en 3600 h (kWh)", gain * 3600 / 1000, 304, 0.5)
verifie("ex6 économie (euros)", gain * 3600 / 1000 * 0.20, 61, 0.5)
# Exercice 7
R7 = 0.30 / (0.040 * 80)
verifie("ex7 résistance de la laine (K/W)", R7, 0.094, 0.0005)
verifie("ex7 flux sans isolant (W)", 20 / 3.0e-3, 6.67e3, 0.005e3)
verifie("ex7 flux avec isolant (W)", 20 / (3.0e-3 + R7), 207, 0.5)
verifie("ex7 résistance surfacique (m².K/W)", 0.30 / 0.040, 7.5, 0)
verifie("ex7 épaisseur minimale pour R = 7 (cm)", 100 * 7 * 0.040, 28, 0)
verifie("ex7 énergie économisée en 3600 h avec 12 K (kWh)", (12 / 3.0e-3 - 12 / (3.0e-3 + R7)) * 3600 / 1000, 1.40e4, 0.005e4)
# Exercice 8
verifie("ex8 durée pour atteindre 30 °C (s)", 1500 * log(60 / 10), 2.69e3, 0.005e3)
verifie("ex8 durée pour 30 °C (min)", 1500 * log(6) / 60, 44.8, 0.05)
verifie("ex8 facteur d'Euler", (1 - 10 / 1500) ** 360, 0.0900, 0.00005)
verifie("ex8 facteur exact", exp(-2.4), 0.0907, 0.00005)
# Exercice 9
verifie("ex9 température de la Terre (K)", teq(S0, 0.30), 255, 0.5)
verifie("ex9 température avec A = 0,60 (K)", teq(S0, 0.60), 221, 0.5)
verifie("ex9 température avec A = 0 (K)", teq(S0, 0.0), 278, 0.5)
verifie("ex9 puissance émise par la Terre (W/m²)", 0.70 * S0 / 4, 238, 0.5)
# Exercice 10
P10 = SIGMA * 1.8 * (306 ** 4 - 293 ** 4)
verifie("ex10 puissance nette rayonnée (W)", P10, 143, 0.5)
P10b = SIGMA * 1.8 * (306 ** 4 - 283 ** 4)
verifie("ex10 près d'une vitre à 10 °C (W)", P10b, 240, 0.5)
verifie("ex10 émission de la peau (W)", SIGMA * 1.8 * 306 ** 4, 895, 0.5)
# Exercice 11
C11 = 0.330 * CEAU + 13
verifie("ex11 capacité thermique (J/K)", C11, 1.39e3, 0.005e3)
tau11 = C11 / (10 * 0.030)
verifie("ex11 temps caractéristique (s)", tau11, 4.64e3, 0.005e3)
verifie("ex11 temps caractéristique (min)", tau11 / 60, 77, 0.5)
verifie("ex11 durée pour 8 °C au réfrigérateur (h)", tau11 * log(21 / 4) / 3600, 2.1, 0.05)
verifie("ex11 durée pour 8 °C au congélateur (min)", tau11 * log(43 / 26) / 60, 39, 0.5)
# Exercice 12
Te = teq(S0, 0.30)
verifie("ex12 température avec une couche totalement absorbante (K)", 2 ** 0.25 * Te, 303, 0.5)
eps = 2 * (1 - (Te / 288) ** 4)
verifie("ex12 fraction absorbée", eps, 0.78, 0.005)
verifie("ex12 température pour eps = 0,80 (K)", Te / (1 - 0.80 / 2) ** 0.25, 289.3, 0.05)
verifie("ex12 température pour eps = 0,78 (K)", Te / (1 - 0.78 / 2) ** 0.25, 288.1, 0.05)
verifie("ex12 hausse pour eps de 0,78 à 0,80 (K)", Te / (1 - 0.80 / 2) ** 0.25 - Te / (1 - 0.78 / 2) ** 0.25, 1.2, 0.05)
# Exercice 13
Sm, Sv = S0 / 1.524 ** 2, S0 / 0.723 ** 2
verifie("ex13 constante solaire de Mars (W/m²)", Sm, 586, 0.5)
verifie("ex13 constante solaire de Vénus (W/m²)", Sv, 2.60e3, 0.005e3)
verifie("ex13 température d'équilibre de Mars (K)", teq(Sm, 0.25), 210, 0.5)
verifie("ex13 température d'équilibre de Vénus (K)", teq(Sv, 0.76), 229, 0.5)
verifie("ex13 écart pour Vénus (K)", 737 - teq(Sv, 0.76), 508, 1)
verifie("ex13 rapport des émissions de Vénus", (737 / teq(Sv, 0.76)) ** 4, 107, 1)
# Exercice 14
tau14 = 6 / log(70 / 50)
verifie("ex14 temps caractéristique (h)", tau14, 17.8, 0.05)
verifie("ex14 température après 12 h", 20 + 70 * exp(-12 / tau14), 55.7, 0.05)
verifie("ex14 rapport avec une tasse (25 min)", tau14 * 60 / 25, 43, 0.5)
verifie("ex14 coefficient hS (W/K)", 2.3e3 / (tau14 * 3600), 0.036, 0.0005)
verifie("ex14 durée pour 60 °C (h)", tau14 * log(70 / 40), 10.0, 0.05)
# Exercice 15
tau15 = 2 / log(12 / 8)
verifie("ex15 temps caractéristique (h)", tau15, 4.93, 0.005)
t15 = tau15 * log(19 / 12)
verifie("ex15 durée depuis le décès (h)", t15, 2.27, 0.005)
verifie("ex15 durée depuis le décès (min)", t15 * 60, 136, 0.5)
verifie("ex15 heure du décès (min après 20 h)", 3 * 60 - t15 * 60, 44, 0.5)
# Valeurs intermédiaires des corrigés
verifie("cor5 rapport océan / neige", 320 / 51, 6.3, 0.05)
verifie("cor7 économie de flux (W)", 12 / 3.0e-3 - 12 / (3.0e-3 + 0.09375), 3.88e3, 0.005e3)
verifie("cor7 rapport des flux", (20 / 3.0e-3) / (20 / (3.0e-3 + 0.09375)), 32, 0.5)
verifie("cor14 temps caractéristique en minutes / 25", 17.8 * 60 / 25, 43, 0.5)
# Défi D20
Tm = (200 * 90 + 50 * 5) / 250
verifie("D20 mélange initial (°C)", Tm, 73, 1e-9)
TA = 20 + (Tm - 20) * exp(-600 / 1500)
TBcafe = 20 + 70 * exp(-600 / 1500)
TB = (200 * TBcafe + 50 * 5) / 250
verifie("D20 option A (°C)", TA, 55.53, 0.005)
verifie("D20 café seul après 10 min (°C)", TBcafe, 66.92, 0.005)
verifie("D20 option B (°C)", TB, 54.54, 0.005)
verifie("D20 écart (K)", TA - TB, 0.99, 0.005)
verifie("D20 formule de l'écart (K)", 0.2 * 15 * (1 - exp(-0.4)), 0.99, 0.005)
verifie("D20 écart maximal (K)", 0.2 * 15, 3.0, 1e-9)
verifie("D20 facteur exp(-0,4)", exp(-0.4), 0.670, 0.0005)


def programme_d20():
    Te, Tc, Tl, tau = 20, 90, 5, 1500      # °C, °C, °C, s
    mc, ml, t = 200, 50, 600               # g, g, s

    def refroidir(T0, t):
        return Te + (T0 - Te) * exp(-t / tau)

    def melanger(Tc, Tl):
        return (mc * Tc + ml * Tl) / (mc + ml)

    TA = refroidir(melanger(Tc, Tl), t)
    TB = melanger(refroidir(Tc, t), Tl)
    print(round(TA, 2), round(TB, 2))


s = sortie_de(programme_d20)
print('   D20 sortie :', s)
if s != '55.53 54.54':
    ECHECS.append('D20 sortie')
for t, T in ((0, 73.0), (300, 63.4), (600, 55.53)):
    verifie(f"figure D20 : option A à {t} s", 20 + 53 * exp(-t / 1500), T, 0.05)
for t, T in ((0, 90.0), (300, 77.3), (600, 66.92)):
    verifie(f"figure D20 : café seul à {t} s", 20 + 70 * exp(-t / 1500), T, 0.05)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 20 et du défi D20 sont vérifiées.")
