"""Vérification des résultats numériques du chapitre 12 (stratégies de synthèse) et du défi D12.

Lancer : python -I -X utf8 verifications/chapitre_12.py
"""
import io
from contextlib import redirect_stdout
from math import sqrt

ECHECS = []


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


# L'essentiel : exemple aspirine et programme multiétapes
n_max = 5.00 / 138.1
verifie("cours n max aspirine (mol)", n_max, 3.62e-2, 0.005e-2)
verifie("cours m max aspirine (g)", n_max * 180.2, 6.52, 0.005)
verifie("cours rendement aspirine", 4.2 / (n_max * 180.2), 0.64, 0.005)
tampon = io.StringIO()
with redirect_stdout(tampon):
    etapes = [0.85, 0.90, 0.70]
    r = 1.0
    for e in etapes:
        r = r * e
    print(round(r, 3))
sortie = tampon.getvalue().strip()
print('   cours programme :', sortie)
if sortie != '0.535':
    ECHECS.append('cours programme multiétapes')
# Exercice 3
verifie("ex3 m max (g)", 0.100 * 88.1, 8.8, 0.05)
verifie("ex3 rendement", 5.9 / 8.81, 0.67, 0.005)
# Exercice 6
verifie("ex6 m max (g)", 5.00 / 138.1 * 180.2, 6.52, 0.005)
verifie("ex6 rendement", 4.2 / 6.52, 0.64, 0.005)
# Exercice 8
verifie("ex8 EA addition (%)", 100 * 60.1 / (42.1 + 18.0), 100, 0.05)
verifie("ex8 EA substitution (%)", 100 * 60.1 / (123.0 + 40.0), 37, 0.5)
# Exercice 9
tampon = io.StringIO()
with redirect_stdout(tampon):
    etapes = [0.85, 0.90, 0.70]
    r = 1.0
    for e in etapes:
        r = r * e
    print(round(r, 3), round(0.50 * r, 3))
sortie = tampon.getvalue().strip()
print('   ex9 sortie :', sortie)
if sortie != '0.535 0.268':
    ECHECS.append('ex9 sortie du programme')
verifie("ex9 nouveau rendement global", 0.85 * 0.90 * 0.95, 0.73, 0.005)
verifie("ex9 gain en améliorant la 3e étape", 0.95 / 0.70, 1.357, 0.005)
# Exercice 11 : données de la figure (palier 78 %, montée exponentielle tau = 12 min)
for t, y in ((5, 26), (10, 44), (15, 56), (20, 63), (30, 72), (40, 75), (50, 77), (60, 78)):
    verifie(f"ex11 point à {t} min (%)", 78 * (1 - 2.718281828 ** (-t / 12)), y, 0.6)
# Exercice 12
verifie("ex12 EA Boots (%)", 100 * 206.3 / 514.5, 40.1, 0.05)
verifie("ex12 EA BHC (%)", 100 * 206.3 / 266.8, 77.3, 0.05)
verifie("ex12 déchets Boots (t/t)", (514.5 - 206.3) / 206.3, 1.5, 0.01)
verifie("ex12 déchets BHC (t/t)", (266.8 - 206.3) / 206.3, 0.29, 0.005)
# Exercice 13
verifie("ex13 rendement global 0,9^4", 0.90 ** 4, 0.66, 0.005)
verifie("ex13 rendement 0,9^30 (%)", 100 * 0.90 ** 30, 4, 0.3)
# Exercice 14
n14 = 5.45 / 109.1
verifie("ex14 n max (mol)", n14, 5.00e-2, 0.005e-2)
verifie("ex14 m max (g)", n14 * 151.2, 7.55, 0.005)
verifie("ex14 rendement", 6.0 / 7.55, 0.79, 0.005)
verifie("ex14 masse brute estimée (g)", 6.0 / 0.90, 6.7, 0.05)
verifie("ex14 rendement sans recristallisation (%)", 100 * (6.0 / 0.90) / 7.553, 88, 0.5)
# Exercice 15
verifie("ex15 EA estérification (%)", 100 * 88.1 / (60.1 + 46.1), 83, 0.5)

# Défi D12


def taux(r):
    return (2 / 3) * (1 + r - sqrt(r * r - r + 1))


verifie("D12 taux pour r = 1", taux(1), 2 / 3, 1e-9)
verifie("D12 taux pour r = 2", taux(2), 0.845, 0.0005)
verifie("D12 taux pour r = 5,5", taux(5.5), 0.950, 0.0005)
# racine de 3x² - 4(1+r)x + 4r = 0 : contrôle pour r = 2
r2 = 2
a, b, c = 3, -4 * (1 + r2), 4 * r2
x = (-b - sqrt(b * b - 4 * a * c)) / (2 * a)
verifie("D12 racine du trinôme pour r = 2", x, taux(2), 1e-9)
tampon = io.StringIO()
with redirect_stdout(tampon):
    r = 1.0
    while taux(r) < 0.95:
        r = r + 0.5
    print(r, round(taux(r), 3))
sortie = tampon.getvalue().strip()
print('   D12 sortie :', sortie)
if sortie != '5.5 0.95':
    ECHECS.append('D12 sortie du programme')

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 12 et du défi D12 sont vérifiées.")
