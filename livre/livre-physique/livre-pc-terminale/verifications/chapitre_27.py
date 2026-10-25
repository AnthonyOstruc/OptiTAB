"""Vérification des résultats numériques du chapitre 27 (mesures et incertitudes) et du défi D27.

Lancer : python -I -X utf8 verifications/chapitre_27.py
Les programmes aléatoires sont exécutés avec une graine fixée : la sortie publiée est celle d'une exécution,
et l'on vérifie aussi qu'elle concorde avec le calcul par la formule de composition.
"""
import io
import random
from contextlib import redirect_stdout
from math import pi, radians, sin, sqrt
from pathlib import Path
from statistics import mean, stdev

ECHECS = []
DONNEES = Path(__file__).resolve().parent.parent / 'figures' / 'donnees'


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def sortie_de(fonction, graine):
    random.seed(graine)
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    return tampon.getvalue().strip()


def compare(nom, sortie, attendu):
    print(f"   {nom} : {sortie}")
    if sortie != attendu:
        ECHECS.append(nom)


def lire(nom):
    lignes = (DONNEES / nom).read_text(encoding='utf-8').split('\n')[1:]
    return [[float(x) for x in ligne.split()] for ligne in lignes if ligne.strip()]


# L'essentiel : 40 durées de chute
t40 = [v[0] for v in lire('27-chute-mesures.dat')]
verifie("cours nombre de mesures", len(t40), 40, 0)
verifie("cours moyenne des durées (s)", mean(t40), 0.45175, 1e-9)
verifie("cours écart-type expérimental (s)", stdev(t40), 0.013, 0.0005)
verifie("cours incertitude-type de la moyenne (s)", stdev(t40) / sqrt(40), 0.0020, 0.00005)
verifie("cours plus petite valeur (s)", min(t40), 0.426, 1e-9)
verifie("cours plus grande valeur (s)", max(t40), 0.481, 1e-9)
histo = lire('27-chute-histo.dat')
verifie("cours effectif total de l'histogramme", sum(n for _, n in histo), 40, 0)
verifie("cours classe la plus fréquente (s)", max(histo, key=lambda c: c[1])[0], 0.450, 1e-9)
dans = sum(1 for t in t40 if abs(t - mean(t40)) <= stdev(t40))
verifie("cours mesures à moins d'un écart-type de la moyenne", dans, 29, 0)
verifie("cours part à moins d'un écart-type (%)", 100 * dans / 40, 72.5, 1e-9)
# Type B
verifie("cours voltmètre demi-étendue (V)", 0.005 * 5.03 + 2 * 0.01, 0.045, 0.0005)
verifie("cours voltmètre incertitude-type (V)", (0.005 * 5.03 + 2 * 0.01) / sqrt(3), 0.026, 0.0005)
verifie("cours fiole jaugée 100 mL (mL)", 0.10 / sqrt(3), 0.058, 0.0005)
verifie("cours règle graduée au mm (mm)", 0.5 / sqrt(3), 0.29, 0.005)
# Composition : g = 2 h / t^2
g = 2 * 1.000 / 0.4518 ** 2
rel_g = sqrt((0.0020 / 1.000) ** 2 + (2 * 0.0020 / 0.4518) ** 2)
verifie("cours g (m/s²)", g, 9.798, 0.0005)
verifie("cours terme de t (%)", 100 * 2 * 0.0020 / 0.4518, 0.89, 0.005)
verifie("cours incertitude relative sur g (%)", 100 * rel_g, 0.91, 0.005)
verifie("cours u(g) (m/s²)", rel_g * g, 0.089, 0.0005)
verifie("cours écart normalisé g", abs(9.798 - 9.81) / 0.089, 0.13, 0.005)
# Monte-Carlo : v = d / dt


def programme_cours():
    v = []
    for k in range(20000):
        d = random.gauss(0.850, 0.003)          # m
        dt = random.gauss(2.47e-3, 2e-5)        # s
        v.append(d / dt)
    print(round(mean(v), 1), round(stdev(v), 1))


compare('cours programme Monte-Carlo', sortie_de(programme_cours, 0), '344.2 3.0')
verifie("cours v calculée directement (m/s)", 0.850 / 2.47e-3, 344.1, 0.05)
rel_v = sqrt((0.003 / 0.850) ** 2 + (0.02 / 2.47) ** 2)
verifie("cours u(v) par la formule (m/s)", rel_v * 0.850 / 2.47e-3, 3.0, 0.05)
verifie("cours écart normalisé v / 343 m/s", abs(344.2 - 343) / 3.0, 0.4, 0.05)
st = lire('27-mc-vitesse-stats.dat')[0]
verifie("figure Monte-Carlo moyenne (m/s)", st[0], 344.2, 0.05)
verifie("figure Monte-Carlo écart-type (m/s)", st[1], 3.0, 0.06)
verifie("figure Monte-Carlo effectif", sum(n for _, n in lire('27-mc-vitesse-histo.dat')), 20000, 30)
# Exercice 1
T1 = [1.43, 1.45, 1.41, 1.44, 1.46, 1.42, 1.44, 1.43]
verifie("ex1 moyenne (s)", mean(T1), 1.435, 1e-9)
verifie("ex1 écart-type (s)", stdev(T1), 0.016, 0.0005)
verifie("ex1 incertitude-type (s)", stdev(T1) / sqrt(8), 0.0057, 0.00005)
# Exercice 2
verifie("ex2 thermomètre (°C)", 0.5 / sqrt(3), 0.29, 0.005)
verifie("ex2 fiole 250 mL (mL)", 0.15 / sqrt(3), 0.087, 0.0005)
verifie("ex2 multimètre demi-étendue (V)", 0.008 * 4.82 + 0.02, 0.059, 0.0005)
verifie("ex2 multimètre (V)", (0.008 * 4.82 + 0.02) / sqrt(3), 0.034, 0.0005)
verifie("ex2 relatif thermomètre (%)", 100 * 0.29 / 21, 1.4, 0.05)
verifie("ex2 relatif fiole (%)", 100 * 0.087 / 250, 0.035, 0.0005)
verifie("ex2 relatif multimètre (%)", 100 * 0.034 / 4.82, 0.71, 0.005)
# Exercice 3
verifie("ex3 relatif masse (%)", 100 * 0.024 / 12.348, 0.19, 0.005)
verifie("ex3 relatif concentration (%)", 100 * 0.00087 / 0.05124, 1.7, 0.05)
verifie("ex3 relatif longueur d'onde (%)", 100 * 1.5 / 632.8, 0.24, 0.005)
verifie("ex3 relatif célérité (%)", 100 * 3.4 / 343.3, 0.99, 0.005)
# Exercice 4
classes = [(11.75, 2), (11.85, 7), (11.95, 15), (12.05, 14), (12.15, 8), (12.25, 3)]
verifie("ex4 effectif hors valeur isolée", sum(n for _, n in classes), 49, 0)
verifie("ex4 part entre 11,9 et 12,1 mL (%)", 100 * 29 / 50, 58, 1e-9)
m4 = sum(c * n for c, n in classes) / 49
verifie("ex4 moyenne estimée (mL)", m4, 12.01, 0.005)
verifie("ex4 moyenne avec la valeur isolée (mL)", (m4 * 49 + 13.45) / 50, 12.04, 0.005)
# Exercice 5
verifie("ex5 groupe A", abs(4.02 - 4.18) / 0.12, 1.3, 0.05)
verifie("ex5 groupe B", abs(3.85 - 4.18) / 0.08, 4.1, 0.05)
verifie("ex5 groupe C", abs(4.25 - 4.18) / 0.02, 3.5, 0.05)
# Exercice 6
verifie("ex6 relatif une mesure (%)", 100 * 0.12 / 1.43, 8.4, 0.05)
verifie("ex6 dix mesures (s)", 0.12 / sqrt(10), 0.038, 0.0005)
verifie("ex6 nombre de mesures pour 0,010 s", (0.12 / 0.010) ** 2, 144, 1e-9)
verifie("ex6 vingt périodes (s)", 0.12 / 20, 0.006, 1e-12)
verifie("ex6 dix mesures de vingt périodes (s)", 0.12 / sqrt(10) / 20, 0.0019, 0.00005)
# Exercice 7
rho = 85.32 / 9.5
rel7 = sqrt((0.01 / 85.32) ** 2 + (0.3 / 9.5) ** 2)
verifie("ex7 masse volumique (g/cm3)", rho, 8.98, 0.005)
verifie("ex7 relatif volume (%)", 100 * 0.3 / 9.5, 3.2, 0.05)
verifie("ex7 relatif masse (%)", 100 * 0.01 / 85.32, 0.012, 0.0005)
verifie("ex7 u(rho) (g/cm3)", rel7 * rho, 0.28, 0.005)
verifie("ex7 écart normalisé cuivre", abs(8.98 - 8.96) / 0.28, 0.07, 0.005)
verifie("ex7 écart normalisé laiton", abs(8.98 - 8.50) / 0.28, 1.7, 0.05)
verifie("ex7 u(rho) maximale pour exclure le laiton", (8.98 - 8.50) / 2, 0.24, 1e-9)
verifie("ex7 u(V) maximale (mL)", 0.24 / 8.98 * 9.5, 0.25, 0.005)
# Exercice 9
f8 = [98, 101, 103, 99, 100, 102, 97, 104, 100, 101, 99, 102]


def programme_ex9():
    f = f8
    N = len(f)
    m, s = mean(f), stdev(f)
    print(N, m, round(s, 2), round(s / N**0.5, 2))


compare('ex9 programme', sortie_de(programme_ex9, 0), '12 100.5 2.07 0.6')
verifie("ex9 incertitude-type à deux chiffres (mm)", stdev(f8) / sqrt(12), 0.60, 0.005)
verifie("ex9 écart normalisé avec 100 mm", 0.5 / 0.60, 0.83, 0.005)
# Exercice 8
cA = 0.100 * 12.35 / 10.00
rel9 = sqrt((0.001 / 0.100) ** 2 + (0.04 / 12.35) ** 2 + (0.012 / 10.00) ** 2)
verifie("ex8 incertitude de la pipette (mL)", 0.02 / sqrt(3), 0.012, 0.0005)
verifie("ex8 concentration (mol/L)", cA, 0.1235, 1e-9)
verifie("ex8 terme de V_E (%)", 100 * 0.04 / 12.35, 0.32, 0.005)
verifie("ex8 incertitude relative (%)", 100 * rel9, 1.06, 0.005)
verifie("ex8 u(cA) (mol/L)", rel9 * cA, 0.0013, 0.00005)
verifie("ex8 écart normalisé", abs(0.1235 - 0.125) / 0.0013, 1.2, 0.05)
# Exercice 11


def programme_ex11():
    R = []
    for k in range(100000):
        U = random.uniform(5.03 - 0.045, 5.03 + 0.045)            # V
        I = random.uniform(22.1e-3 - 0.3e-3, 22.1e-3 + 0.3e-3)    # A
        R.append(U / I)
    print(round(mean(R), 1), round(stdev(R), 1))


compare('ex11 programme', sortie_de(programme_ex11, 0), '227.6 2.1')
verifie("ex11 u(U) (V)", 0.045 / sqrt(3), 0.026, 0.0005)
verifie("ex11 u(I) (mA)", 0.3 / sqrt(3), 0.17, 0.005)
rel10 = sqrt((0.045 / sqrt(3) / 5.03) ** 2 + (0.3 / sqrt(3) / 22.1) ** 2)
verifie("ex11 R = U/I (ohm)", 5.03 / 22.1e-3, 227.6, 0.05)
verifie("ex11 u(R) par la formule (ohm)", rel10 * 5.03 / 22.1e-3, 2.1, 0.05)
verifie("ex11 tolérance basse (ohm)", 220 * 0.95, 209, 1e-9)
verifie("ex11 tolérance haute (ohm)", 220 * 1.05, 231, 1e-9)
# Exercice 10
lam = 0.200e-3 * 4.75e-3 / 1.500
rel11 = sqrt((0.0058 / 0.200) ** 2 + (0.05 / 4.75) ** 2 + (0.005 / 1.500) ** 2)
verifie("ex10 interfrange (mm)", 47.5 / 10, 4.75, 1e-9)
verifie("ex10 u(a) (mm)", 0.010 / sqrt(3), 0.0058, 0.00005)
verifie("ex10 longueur d'onde (nm)", 1e9 * lam, 633, 0.5)
verifie("ex10 terme de a (%)", 100 * 0.0058 / 0.200, 2.9, 0.05)
verifie("ex10 terme de i (%)", 100 * 0.05 / 4.75, 1.1, 0.05)
verifie("ex10 terme de D (%)", 100 * 0.005 / 1.500, 0.33, 0.005)
verifie("ex10 incertitude relative (%)", 100 * rel11, 3.1, 0.05)
verifie("ex10 u(lambda) (nm)", 1e9 * lam * rel11, 20, 0.5)
verifie("ex10 écart normalisé", abs(633 - 632.8) / 20, 0.01, 0.005)
# Exercice 12
m12 = [9.981, 9.976, 9.985, 9.979, 9.983, 9.974, 9.980, 9.987, 9.978, 9.982]
verifie("ex12 masse moyenne (g)", mean(m12), 9.9805, 1e-9)
verifie("ex12 écart-type (g)", stdev(m12), 0.0040, 0.00005)
verifie("ex12 incertitude-type (g)", stdev(m12) / sqrt(10), 0.0013, 0.00005)
verifie("ex12 volume (mL)", mean(m12) / 0.9982, 9.9985, 0.00005)
verifie("ex12 u(V) (mL)", 0.0013 / 0.9982, 0.0013, 0.00005)
verifie("ex12 écart normalisé", abs(9.9985 - 10.00) / 0.0013, 1.2, 0.05)
# Exercice 13
m13 = 5.00e-3 * 28.0e-3 * 176.1 * 200.0 / 10.00
rel13 = sqrt(0.010 ** 2 + (0.05 / 28.0) ** 2 + (0.012 / 10.00) ** 2 + (0.087 / 200.0) ** 2)
verifie("ex13 quantité de diiode (mmol)", 1000 * 5.00e-3 * 28.0e-3, 0.140, 1e-9)
verifie("ex13 masse (mg)", 1000 * m13, 493.1, 0.05)
verifie("ex13 incertitude relative (%)", 100 * rel13, 1.02, 0.005)
verifie("ex13 u(m) (mg)", 1000 * m13 * rel13, 5.0, 0.05)
verifie("ex13 écart normalisé", abs(493.1 - 500) / 5.0, 1.4, 0.05)
verifie("ex13 tolérance basse (mg)", 500 * 0.95, 475, 1e-9)
# Exercice 14
d14 = [28.62, 28.70, 28.55, 28.66, 28.71, 28.59, 28.64, 28.68, 28.60, 28.65]
T14 = mean(d14) / 20
uT14 = stdev(d14) / sqrt(10) / 20
verifie("ex14 durée moyenne de 20 périodes (s)", mean(d14), 28.640, 1e-9)
verifie("ex14 écart-type (s)", stdev(d14), 0.051, 0.0005)
verifie("ex14 période (s)", T14, 1.4320, 1e-9)
verifie("ex14 u(T) (s)", uT14, 0.00080, 0.000005)
g14 = 4 * pi ** 2 * 0.510 / 1.4320 ** 2
rel14 = sqrt((0.003 / 0.510) ** 2 + (2 * 0.00080 / 1.4320) ** 2)
verifie("ex14 g (m/s²)", g14, 9.818, 0.0005)
verifie("ex14 terme de L (%)", 100 * 0.003 / 0.510, 0.59, 0.005)
verifie("ex14 terme de T (%)", 100 * 2 * 0.00080 / 1.4320, 0.11, 0.005)
verifie("ex14 u(g) (m/s²)", g14 * rel14, 0.059, 0.0005)
verifie("ex14 écart normalisé", abs(9.818 - 9.81) / 0.059, 0.14, 0.005)
# Exercice 15


def programme_ex15():
    n = []
    for k in range(20000):
        i = radians(random.uniform(39, 41))
        r = radians(random.uniform(24, 26))
        n.append(sin(i) / sin(r))
    print(round(mean(n), 3), round(stdev(n), 3))


compare('ex15 programme', sortie_de(programme_ex15, 0), '1.522 0.038')
verifie("ex15 indice avec 40° et 25°", sin(radians(40)) / sin(radians(25)), 1.521, 0.0005)
verifie("ex15 écart normalisé crown", abs(1.522 - 1.52) / 0.038, 0.05, 0.005)
verifie("ex15 écart normalisé flint", abs(1.522 - 1.62) / 0.038, 2.6, 0.05)
st15 = lire('27-mc-indice-stats.dat')[0]
verifie("figure ex15 moyenne", st15[0], 1.52, 0.005)
verifie("figure ex15 écart-type", st15[1], 0.038, 0.0005)
verifie("figure ex15 effectif", sum(n for _, n in lire('27-mc-indice-histo.dat')), 20000, 50)
# Défi D27


def programme_d27():
    s, N = 0.013, 40
    moyennes = []
    for k in range(2000):
        serie = [random.gauss(0.452, s) for j in range(N)]
        moyennes.append(mean(serie))
    print(round(stdev(moyennes), 5), round(s / N**0.5, 5))


compare('D27 programme', sortie_de(programme_d27, 0), '0.00205 0.00206')
verifie("D27 N minimal pour révéler le retard", (2 * 0.013 / 0.010) ** 2, 6.76, 1e-9)
verifie("D27 écart normalisé avec 40 mesures", 0.010 / (0.013 / sqrt(40)), 4.9, 0.05)
t_vrai = sqrt(2 * 1.000 / 9.81)
verifie("D27 durée sans retard pour 1 m (s)", t_vrai, 0.4515, 0.00005)
verifie("D27 g avec le retard (m/s²)", 2 / (t_vrai + 0.010) ** 2, 9.39, 0.005)
verifie("D27 écart normalisé sur g", abs(9.39 - 9.81) / 0.084, 5.0, 0.05)
verifie("D27 u(g) avec le retard (m/s²)", 9.39 * sqrt(0.002 ** 2 + (2 * 0.0020 / 0.4615) ** 2), 0.084, 0.0005)
hauteurs = [0.20, 0.40, 0.60, 0.80, 1.00]
publies = [0.2119, 0.2956, 0.3597, 0.4139, 0.4615]
for h, t in zip(hauteurs, publies):
    verifie(f"D27 durée mesurée pour h = {h} m (s)", sqrt(2 * h / 9.81) + 0.010, t, 0.00005)
x = [sqrt(h) for h in hauteurs]
mx, my = mean(x), mean(publies)
a = sum((xi - mx) * (yi - my) for xi, yi in zip(x, publies)) / sum((xi - mx) ** 2 for xi in x)
b = my - a * mx
verifie("D27 coefficient directeur (s/m^0,5)", a, 0.4515, 0.00005)
verifie("D27 ordonnée à l'origine (s)", b, 0.010, 0.00005)
verifie("D27 g déduit de la pente (m/s²)", 2 / a ** 2, 9.81, 0.005)
verifie("D27 pente par deux points (s/m^0,5)", (0.4615 - 0.2119) / (1 - sqrt(0.20)), 0.4515, 0.00005)
verifie("D27 racine de 0,20", sqrt(0.20), 0.447, 0.0005)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 27 et du défi D27 sont vérifiées.")
