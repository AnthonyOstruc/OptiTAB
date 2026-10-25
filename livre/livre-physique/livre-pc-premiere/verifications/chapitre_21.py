"""Vérification du chapitre 21 (Mesures et incertitudes) et du défi D21.

Lancer : python -I -X utf8 verifications/chapitre_21.py
"""
import io
import random
from contextlib import redirect_stdout
from math import sqrt
from statistics import mean, stdev

ECHECS = []


def verifie(nom, calcule, publie, tol_rel=0.006):
    ok = abs(calcule - publie) <= tol_rel * abs(publie) + 1e-12
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:60s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def compare_sortie(nom, fonction, attendu):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    s = tampon.getvalue().strip()
    print(f'   {nom} :', s.replace('\n', ' | '))
    if s != attendu:
        ECHECS.append(nom)


def stats(x):
    return mean(x), stdev(x), stdev(x) / sqrt(len(x))


# Cours : volume à l'équivalence mesuré par 20 groupes
V = [12.20, 12.25, 12.15, 12.30, 12.20, 12.35, 12.10, 12.25, 12.20, 12.30,
     12.15, 12.25, 12.20, 12.40, 12.25, 12.20, 12.05, 12.30, 12.25, 12.20]
m, s, u = stats(V)
verifie("cours moyenne (mL)", m, 12.23, 0.0005)
verifie("cours écart-type (mL)", s, 0.082, 0.005)
verifie("cours incertitude-type (mL)", u, 0.018, 0.02)
verifie("cours u arrondie (mL)", round(u, 2), 0.02)
classes = {v: V.count(v) for v in sorted(set(V))}
print('   cours histogramme :', classes)
if list(classes.values()) != [1, 1, 2, 6, 5, 3, 1, 1]:
    ECHECS.append('cours histogramme')
verifie("cours écart avec 12,25 mL (en u)", abs(12.25 - 12.23) / 0.02, 1.0)
verifie("cours écart avec 12,50 mL (en u)", abs(12.50 - 12.23) / 0.02, 13.5)
verifie("cours thermomètre gradué au degré (°C)", 1 / sqrt(12), 0.29, 0.01)
verifie("cours pipette 10,00 mL ± 0,02 mL (mL)", 0.02 / sqrt(3), 0.012, 0.04)
verifie("cours incertitude relative (%)", 0.02 / 12.23 * 100, 0.16, 0.03)


def programme_cours():
    V = [12.20, 12.25, 12.15, 12.30, 12.20, 12.35, 12.10, 12.25, 12.20, 12.30,
         12.15, 12.25, 12.20, 12.40, 12.25, 12.20, 12.05, 12.30, 12.25, 12.20]
    n = len(V)
    s = stdev(V)                       # ecart-type experimental (avec n - 1)
    u = s / sqrt(n)                    # incertitude-type de type A
    print(n, 'mesures ; moyenne :', round(mean(V), 2), 'mL')
    print('s =', round(s, 3), 'mL ; u =', round(u, 3), 'mL')


compare_sortie('cours programme', programme_cours, '20 mesures ; moyenne : 12.23 mL\ns = 0.082 mL ; u = 0.018 mL')

# Exercice 1 : histogramme des périodes (mêmes données que l'exercice 6)
T = [143, 145, 141, 139, 144, 147, 143, 142, 149, 145,
     140, 143, 146, 141, 145, 148, 142, 147, 144, 143]
effectifs = [len([t for t in T if d <= t < d + 2]) for d in range(138, 150, 2)]
print('   ex1 effectifs :', effectifs)
if effectifs != [1, 3, 6, 5, 3, 2]:
    ECHECS.append('ex1 effectifs')
verifie("ex1 proportion entre 1,42 s et 1,46 s (%)", (6 + 5) / 20 * 100, 55)
verifie("ex1 moyenne (s)", mean(T) / 100, 1.44, 0.005)
# Exercice 2 : célérité du son
c2 = [339, 342, 345, 340, 336, 343, 341, 339]
m2, s2, u2 = stats(c2)
verifie("ex2 moyenne (m/s)", m2, 340.6, 0.0002)
verifie("ex2 écart-type (m/s)", s2, 2.8, 0.01)
verifie("ex2 incertitude-type (m/s)", u2, 0.98, 0.005)
verifie("ex2 résultat arrondi (m/s)", round(m2), 341)
# Exercice 3 : thermomètres
verifie("ex3 thermomètre à alcool (°C)", 1 / sqrt(12), 0.29, 0.01)
verifie("ex3 thermomètre électronique (°C)", 0.2 / sqrt(3), 0.12, 0.04)
verifie("ex3 incertitude relative alcool (%)", 0.3 / 21.0 * 100, 1.4, 0.025)
verifie("ex3 incertitude relative électronique (%)", 0.1 / 21.4 * 100, 0.5, 0.07)
# Exercice 4 : écriture des résultats (u à un chiffre significatif)
verifie("ex4 incertitude relative de la masse (%)", 0.02 / 12.35 * 100, 0.16, 0.03)
# Exercice 5 : quatre séries de g
for nom, serie, moy in [('A', [9.79, 9.81, 9.83, 9.80, 9.82, 9.78, 9.84, 9.81], 9.81),
                        ('B', [9.65, 9.95, 9.78, 9.88, 9.70, 9.92, 9.84, 9.75], 9.81),
                        ('C', [9.58, 9.60, 9.62, 9.59, 9.61, 9.57, 9.63, 9.60], 9.60),
                        ('D', [9.95, 10.15, 10.02, 9.88, 10.10, 9.98, 10.08, 9.92], 10.01)]:
    verifie(f"ex5 moyenne de la série {nom}", mean(serie), moy, 0.001)
    print(f"   ex5 écart-type de la série {nom} : {stdev(serie):.3f}")
# Exercice 6 : Python


def programme_ex6():
    T = [143, 145, 141, 139, 144, 147, 143, 142, 149, 145,
         140, 143, 146, 141, 145, 148, 142, 147, 144, 143]      # centiemes de s
    s = stdev(T)
    print('moyenne :', mean(T), 'cs')
    print('s =', round(s, 1), 'cs ; u =', round(s / sqrt(20), 1), 'cs')
    for debut in range(138, 150, 2):
        nb = len([t for t in T if debut <= t < debut + 2])
        print(debut, '-', debut + 2, ':', '*' * nb)


compare_sortie('ex6 programme', programme_ex6,
               'moyenne : 143.85 cs\ns = 2.7 cs ; u = 0.6 cs\n138 - 140 : *\n140 - 142 : ***\n142 - 144 : ******\n'
               '144 - 146 : *****\n146 - 148 : ***\n148 - 150 : **')
# Exercice 7 : pipette et éprouvette
verifie("ex7 pipette 20,00 mL ± 0,03 mL (mL)", 0.03 / sqrt(3), 0.017, 0.02)
verifie("ex7 pipette incertitude relative (%)", 0.017 / 20.00 * 100, 0.085, 0.02)
verifie("ex7 éprouvette graduée 0,5 mL (mL)", 0.5 / sqrt(12), 0.14, 0.04)
verifie("ex7 éprouvette incertitude relative (%)", 0.14 / 20.0 * 100, 0.7)
verifie("ex7 rapport éprouvette / pipette", (0.5 / sqrt(12)) / (0.03 / sqrt(3)), 8.3, 0.01)
# Exercice 8 : g par chute libre
t8 = [0.452, 0.448, 0.455, 0.450, 0.446, 0.453, 0.449, 0.451, 0.447, 0.454]
g8 = [2 * 1.000 / t**2 for t in t8]
print('   ex8 valeurs de g :', [round(g, 2) for g in g8])
verifie("ex8 premier g (m/s2)", g8[0], 9.79, 0.001)
m8, s8, u8 = stats(g8)
verifie("ex8 moyenne (m/s2)", m8, 9.86, 0.001)
verifie("ex8 écart-type (m/s2)", s8, 0.13, 0.02)
verifie("ex8 incertitude-type (m/s2)", u8, 0.04, 0.05)
verifie("ex8 écart à 9,81 (m/s2)", 9.86 - 9.81, 0.05)
# Exercice 9 : chronométrage
verifie("ex9 manuel une période (s)", 0.080 / sqrt(10), 0.025, 0.02)
verifie("ex9 dix périodes, s sur T (s)", 0.085 / 10, 0.0085)
verifie("ex9 dix périodes, u sur T (s)", 0.085 / 10 / sqrt(10), 0.0027, 0.01)
verifie("ex9 capteur (s)", 0.002 / sqrt(10), 0.0006, 0.06)
verifie("ex9 période à partir de 10 T (s)", 14.36 / 10, 1.436)
# Exercice 10 : multimètre
a10 = 0.005 * 4.52 + 2 * 0.01
verifie("ex10 demi-étendue calibre 20 V (V)", a10, 0.043, 0.01)
verifie("ex10 incertitude-type calibre 20 V (V)", a10 / sqrt(3), 0.025, 0.02)
a10b = 0.005 * 4.5 + 2 * 0.1
verifie("ex10 demi-étendue calibre 200 V (V)", a10b, 0.22, 0.02)
verifie("ex10 incertitude-type calibre 200 V (V)", a10b / sqrt(3), 0.13, 0.02)
verifie("ex10 incertitude relative 20 V (%)", 0.02 / 4.52 * 100, 0.4, 0.15)
verifie("ex10 incertitude relative 200 V (%)", 0.1 / 4.5 * 100, 2.2, 0.02)
# Exercice 11 : masse volumique
r11 = [7.05, 7.21, 7.12, 6.98, 7.18, 7.09, 7.25, 7.02, 7.15, 7.11]
verifie("ex11 moyenne non arrondie (g/cm3)", mean(r11), 7.116, 0.0001)
m11, s11, u11 = stats(r11)
verifie("ex11 moyenne (g/cm3)", m11, 7.12, 0.001)
verifie("ex11 écart-type (g/cm3)", s11, 0.085, 0.01)
verifie("ex11 incertitude-type (g/cm3)", u11, 0.027, 0.01)
verifie("ex11 écart à l'étain (en u)", (7.29 - 7.12) / 0.03, 5.7, 0.01)
verifie("ex11 écart au zinc (g/cm3)", 7.13 - 7.12, 0.01)
# Exercice 12 : sérum physiologique
c12 = [8.9, 9.1, 9.0, 8.8, 9.2, 9.0, 8.9, 9.1, 9.0, 9.6, 8.9, 9.1]
m12, s12, u12 = stats(c12)
verifie("ex12 moyenne (g/L)", m12, 9.05, 0.001)
verifie("ex12 écart-type (g/L)", s12, 0.21, 0.02)
verifie("ex12 incertitude-type (g/L)", u12, 0.06, 0.01)
sans = [x for x in c12 if x < 9.5]
m12b, s12b, u12b = stats(sans)
verifie("ex12 moyenne sans 9,6 (g/L)", m12b, 9.00, 0.001)
verifie("ex12 écart-type sans 9,6 (g/L)", s12b, 0.12, 0.02)
verifie("ex12 incertitude-type sans 9,6 (g/L)", u12b, 0.04, 0.15)
verifie("ex12 écart de 9,6 à la moyenne (en s)", (9.6 - 9.00) / 0.12, 5.0)
effectifs12 = {x: c12.count(x) for x in sorted(set(c12))}
print('   ex12 effectifs :', effectifs12)
# Exercice 13 : temps de réaction
d13 = [15.2, 17.8, 14.1, 19.5, 16.3, 18.0, 15.7, 16.9, 17.2, 14.8]
t13 = [sqrt(2 * d / 100 / 9.81) for d in d13]
verifie("ex13 première durée (s)", t13[0], 0.176, 0.003)
m13, s13, u13 = stats(t13)
verifie("ex13 moyenne (s)", m13, 0.183, 0.003)
verifie("ex13 écart-type (s)", s13, 0.009, 0.03)
verifie("ex13 incertitude-type (s)", u13, 0.003, 0.05)
verifie("ex13 distance moyenne (cm)", mean(d13), 16.55, 0.001)
# Exercice 14 : balance
p14 = [50.03, 50.04, 50.03, 50.02, 50.03, 50.04, 50.03, 50.03, 50.02, 50.03]
m14, s14, u14 = stats(p14)
verifie("ex14 moyenne (g)", m14, 50.030, 0.00001)
verifie("ex14 écart-type (g)", s14, 0.007, 0.05)
verifie("ex14 incertitude-type (g)", u14, 0.002, 0.06)
verifie("ex14 écart à 50,000 g (en u)", 0.030 / 0.002, 15)
# Exercice 15 : volume d'une goutte
v15 = [1.00, 0.95, 1.05, 1.00, 0.95]
m15, s15, u15 = stats(v15)
verifie("ex15 moyenne pour 20 gouttes (mL)", m15, 0.99, 0.001)
verifie("ex15 écart-type (mL)", s15, 0.042, 0.01)
verifie("ex15 incertitude-type (mL)", u15, 0.019, 0.02)
verifie("ex15 volume d'une goutte (mL)", m15 / 20, 0.0495, 0.001)
verifie("ex15 incertitude-type sur une goutte (mL)", u15 / 20, 0.0009, 0.05)
verifie("ex15 lecture d'une seule goutte (mL)", 0.05 / sqrt(12), 0.014, 0.04)
verifie("ex15 incertitude relative une goutte (%)", (0.05 / sqrt(12)) / 0.0495 * 100, 29, 0.01)
verifie("ex15 rapport des incertitudes relatives", 29 / 1.8, 16, 0.01)
verifie("ex15 incertitude relative vingt gouttes (%)", 0.0009 / 0.0495 * 100, 1.8, 0.02)


# Rapports cités dans les corrigés
verifie("cor3 rapport des incertitudes relatives", 1.4 / 0.5, 2.8)
verifie("cor9 rapport protocole A / capteur", 0.025 / 0.0006, 42, 0.01)
verifie("cor11 écart de 7,25 à la moyenne (en s)", (7.25 - 7.116) / 0.085, 1.6, 0.02)
verifie("cor11 gain de précision de la moyenne", sqrt(10), 3.16, 0.001)
verifie("cor14 u pour cent pesées (g)", 0.0067 / sqrt(100), 0.0007, 0.05)
verifie("cor15 incertitude relative du titrage (%)", 0.05 / 12 * 100, 0.42, 0.01)


# Défi D21 : combien de mesures faut-il ?
def programme_d21():
    random.seed(2026)
    for n in [5, 20, 100, 500]:
        mesures = [random.gauss(12.20, 0.08) for i in range(n)]
        s = stdev(mesures)
        print(n, round(mean(mesures), 3), round(s, 3), round(s / sqrt(n), 4))


compare_sortie('D21 programme', programme_d21,
               '5 12.202 0.095 0.0425\n20 12.194 0.091 0.0204\n100 12.191 0.086 0.0086\n500 12.203 0.08 0.0036')
verifie("D21 u théorique pour n = 500 (mL)", 0.08 / sqrt(500), 0.0036, 0.01)
verifie("D21 rapport u(5) / u(500)", sqrt(500 / 5), 10)
verifie("D21 nombre de mesures pour u = 0,001 mL", (0.08 / 0.001) ** 2, 6400)
verifie("D21 durée de 6400 titrages à 15 min (jours)", 6400 * 15 / 60 / 24, 67, 0.01)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs et sorties du chapitre 21 et du défi D21 sont vérifiées.")
