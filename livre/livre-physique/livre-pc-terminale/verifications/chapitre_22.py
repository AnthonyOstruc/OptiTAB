"""Vérification des résultats numériques du chapitre 22 (diffraction et interférences) et du défi D22.

Lancer : python -I -X utf8 verifications/chapitre_22.py
"""
import io
from contextlib import redirect_stdout
from math import cos, degrees, pi, sin

ECHECS = []


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
th = 633e-9 / 0.10e-3
verifie("cours angle de diffraction (rad)", th, 6.3e-3, 0.05e-3)
verifie("cours largeur de la tache centrale (cm)", 100 * 2 * 2.0 * th, 2.5, 0.05)
verifie("cours interfrange (mm)", 1000 * 633e-9 * 1.50 / 0.20e-3, 4.75, 0.005)


def programme_cours():
    A, T = 1.0, 1.0
    instants = [k / 1000 for k in range(1000)]
    for phi in [0, pi / 2, 2 * pi / 3, pi]:
        s = [A * sin(2 * pi * t / T) + A * sin(2 * pi * t / T + phi) for t in instants]
        print(round(phi, 2), round(max(s), 2))


s = sortie_de(programme_cours).splitlines()
print('   cours programme :', s)
if s != ['0 2.0', '1.57 1.41', '2.09 1.0', '3.14 0.0']:
    ECHECS.append('cours programme')
for phi, amp in ((0, 2.0), (pi / 2, 1.41), (2 * pi / 3, 1.0), (pi, 0.0)):
    verifie(f"cours amplitude théorique pour phi = {phi:.2f}", 2 * abs(cos(phi / 2)), amp, 0.005)
# Exercice 2
th2 = 0.023 / (2 * 1.80)
verifie("ex2 angle (rad)", th2, 6.4e-3, 0.05e-3)
verifie("ex2 largeur de la fente (mm)", 1000 * 650e-9 / th2, 0.10, 0.005)
# Exercice 3
verifie("ex3 angle (rad)", 40 / 60, 0.67, 0.005)
verifie("ex3 angle (degrés)", degrees(40 / 60), 38, 0.5)
verifie("ex3 angle pour une passe de 400 m (degrés)", degrees(40 / 400), 5.7, 0.05)
# Exercice 4
for nom, d1, d2, k in (("M", 8.0, 11.0, 1.5), ("N", 6.0, 10.0, 2.0), ("P", 9.0, 9.0, 0.0), ("Q", 5.0, 10.0, 2.5)):
    verifie(f"ex4 différence de marche en {nom} (en longueurs d'onde)", (d2 - d1) / 2.0, k, 1e-9)
# Exercice 5
verifie("ex5 interfrange (mm)", 1000 * 532e-9 * 2.00 / 0.25e-3, 4.26, 0.005)
verifie("ex5 interfrange avec D doublé (mm)", 1000 * 532e-9 * 4.00 / 0.25e-3, 8.51, 0.005)
verifie("ex5 interfrange en lumière rouge (mm)", 1000 * 650e-9 * 2.00 / 0.25e-3, 5.20, 0.005)
# Exercice 6
th6 = 0.042 / (2 * 2.00)
verifie("ex6 angle (rad)", th6, 0.0105, 0.00005)
verifie("ex6 diamètre du cheveu (µm)", 1e6 * 633e-9 / th6, 60, 0.5)
# Exercice 7
verifie("ex7 tache bleue (cm)", 100 * 2 * 1.5 * 400e-9 / 50e-6, 2.4, 0.05)
verifie("ex7 tache rouge (cm)", 100 * 2 * 1.5 * 750e-9 / 50e-6, 4.5, 0.05)
# Exercice 10 (cuve à ondes)
lam10 = 0.30 / 20
verifie("ex10 longueur d'onde (cm)", 100 * lam10, 1.5, 1e-9)
n_repos = sum(1 for k in range(-10, 10) if abs((k + 0.5) * 1.5) < 6.0)
n_vibr = sum(1 for k in range(-10, 11) if abs(k * 1.5) < 6.0)
verifie("ex10 lignes de repos entre les sources", n_repos, 8, 0)
verifie("ex10 lignes d'amplitude maximale entre les sources", n_vibr, 7, 0)
verifie("ex10 écart entre deux lignes de repos sur S1S2 (cm)", 1.5 / 2, 0.75, 1e-9)
# Exercice 9 (fentes d'Young)
i11 = 0.038 / 10
verifie("ex9 interfrange (mm)", 1000 * i11, 3.8, 1e-9)
verifie("ex9 longueur d'onde (nm)", 1e9 * i11 * 0.40e-3 / 2.50, 608, 0.5)
verifie("ex9 incertitude relative sur i si lecture à 1 mm (%)", 100 * 0.001 / 0.038, 2.6, 0.05)
# Exercice 12
th12 = 1.22 * 550e-9 / 2.4
verifie("ex12 résolution de Hubble (rad)", th12, 2.8e-7, 0.05e-7)
verifie("ex12 plus petit détail lunaire (m)", th12 * 3.84e8, 107, 1)
verifie("ex12 résolution de l'œil (rad)", 1.22 * 550e-9 / 3e-3, 2.2e-4, 0.05e-4)
verifie("ex12 résolution du JWST à 2 µm (rad)", 1.22 * 2e-6 / 6.5, 3.8e-7, 0.05e-7)
verifie("ex12 détail lunaire à l'œil (km)", 1.22 * 550e-9 / 3e-3 * 3.84e8 / 1000, 86, 0.5)
verifie("cor12 rapport œil / Hubble", 86e3 / 107, 800, 10)
# Exercice 13
verifie("ex13 retard d'une demi-période à 200 Hz (ms)", 1000 * 0.5 / 200, 2.5, 1e-9)
verifie("ex13 retard maximal pour une amplitude 10 fois plus faible (µs)", 1e6 * 0.05 / (pi * 200), 80, 0.5)
verifie("ex13 même chose à 2000 Hz (µs)", 1e6 * 0.05 / (pi * 2000), 8.0, 0.05)
verifie("ex13 atténuation pour un rapport d'amplitudes de 10 (dB)", 20, 20, 0)
# Exercice 14
verifie("ex14 épaisseur de la couche antireflet (nm)", 550 / (4 * 1.38), 99.6, 0.05)
verifie("ex14 longueur d'onde parfaitement éteinte", 4 * 1.38 * 99.6, 550, 0.5)
verifie("ex14 différence de marche pour le bleu (fraction de lambda)", 2 * 1.38 * 99.6 / 450, 0.61, 0.005)
verifie("ex14 différence de marche pour le rouge (fraction de lambda)", 2 * 1.38 * 99.6 / 700, 0.39, 0.005)
# Exercice 15
d15 = 0.774 / 9
verifie("ex15 distance entre deux minimums (cm)", 100 * d15, 8.6, 1e-9)
verifie("ex15 longueur d'onde (cm)", 100 * 2 * d15, 17.2, 1e-9)
verifie("ex15 célérité du son (m/s)", 2 * d15 * 2000, 344, 0.5)
# Défi D22
lam, D, a, b = 633e-9, 2.0, 0.10e-3, 0.50e-3


def intensite(x):
    u = pi * a * x / (lam * D)
    env = 1 if u == 0 else (sin(u) / u) ** 2
    return env * cos(pi * b * x / (lam * D)) ** 2


def programme_d22():
    lam, D, a, b = 633e-9, 2.0, 0.10e-3, 0.50e-3

    def intensite(x):
        u = pi * a * x / (lam * D)
        env = 1 if u == 0 else (sin(u) / u)**2
        return env * cos(pi * b * x / (lam * D))**2

    i = lam * D / b                  # interfrange
    for k in range(6):
        x = k * i
        I = round(intensite(x), 3)
        print(k, round(1000 * x, 2), I)


s = sortie_de(programme_d22).splitlines()
print('   D22 sorties :', s)
if s != ['0 0.0 1.0', '1 2.53 0.875', '2 5.06 0.573', '3 7.6 0.255', '4 10.13 0.055', '5 12.66 0.0']:
    ECHECS.append('D22 sorties')
verifie("D22 largeur de la tache centrale (mm)", 1000 * 2 * lam * D / a, 25.3, 0.05)
verifie("D22 interfrange (mm)", 1000 * lam * D / b, 2.53, 0.005)
verifie("D22 rapport L/i", (2 * lam * D / a) / (lam * D / b), 10, 1e-9)
verifie("D22 nombre de franges brillantes dans la tache", sum(1 for k in range(-10, 11) if abs(k * lam * D / b) < lam * D / a), 9, 0)
verifie("D22 franges si a est divisé par 2", sum(1 for k in range(-30, 31) if abs(k * lam * D / b) < lam * D / (a / 2)), 19, 0)
for x, Iv in ((0, 1.0), (1.27e-3, 0.0), (2.53e-3, 0.875), (6.33e-3, 0.0), (7.595e-3, 0.255)):
    verifie(f"figure D22 : intensité en x = {1000*x:.2f} mm", intensite(x), Iv, 0.005)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 22 et du défi D22 sont vérifiées.")
