"""Vérification du chapitre 18 (Lentilles minces et images) et du défi D18.

Lancer : python -I -X utf8 verifications/chapitre_18.py
Grandeurs algébriques : axe orienté dans le sens de la lumière, origine au centre optique O.
"""
import io
import math
from contextlib import redirect_stdout

ECHECS = []


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


def image(OA, fp):
    """Position algébrique de l'image (mêmes unités que OA et fp)."""
    return 1 / (1 / fp + 1 / OA)


# Cours
verifie("cours vergence de f' = 20 cm (dioptries)", 1 / 0.20, 5.0)
verifie("cours image à OA = -30 cm, f' = 10 cm (cm)", image(-30, 10), 15)
verifie("cours grandissement", image(-30, 10) / -30, -0.5)


def programme():
    fp = 10
    for OA in [-50, -30, -20, -15, -12, -5]:
        OAp = 1 / (1 / fp + 1 / OA)
        print(OA, 'cm :', round(OAp, 1), 'cm ; gamma =', round(OAp / OA, 2))


s = sortie_de(programme)
print('   cours programme :', s.replace('\n', ' | '))
if s != ('-50 cm : 12.5 cm ; gamma = -0.25\n-30 cm : 15.0 cm ; gamma = -0.5\n-20 cm : 20.0 cm ; gamma = -1.0\n'
         '-15 cm : 30.0 cm ; gamma = -2.0\n-12 cm : 60.0 cm ; gamma = -5.0\n-5 cm : -10.0 cm ; gamma = 2.0'):
    ECHECS.append('cours programme')
# Exercice 1
verifie("ex1 vergence pour 20 cm (d)", 1 / 0.20, 5.0)
verifie("ex1 focale pour 8 dioptries (cm)", 100 / 8, 12.5)
verifie("ex1 focale pour 50 dioptries (mm)", 1000 / 50, 20)
# Exercice 2 : construction (f' = 2 cm, OA = -6 cm, AB = 1,5 cm)
verifie("ex2 position de l'image (cm)", image(-6, 2), 3.0)
verifie("ex2 grandissement", image(-6, 2) / -6, -0.5)
verifie("ex2 taille de l'image (cm)", image(-6, 2) / -6 * 1.5, -0.75)
# Exercice 3
verifie("ex3 OA' (cm)", image(-30, 10), 15)
verifie("ex3 A'B' (cm)", image(-30, 10) / -30 * 2.0, -1.0)
verifie("ex3 objet à -15 cm : OA' (cm)", image(-15, 10), 30)
# Exercice 4 : loupe
verifie("ex4 OA' (cm)", image(-3.0, 5.0), -7.5)
verifie("ex4 grandissement", image(-3.0, 5.0) / -3.0, 2.5)
verifie("ex4 taille d'une lettre de 2,0 mm (mm)", 2.5 * 2.0, 5.0)
# Exercice 5 : projection
verifie("ex5 vergence (d)", 1 / 1.00 + 1 / 0.25, 5.0)
verifie("ex5 distance focale (cm)", 100 / (1 / 1.00 + 1 / 0.25), 20)
verifie("ex5 grandissement", 100 / -25, -4)
# Exercice 7 : appareil photo
OAp7 = image(-3000, 50)
verifie("ex7 position du capteur (mm)", OAp7, 50.85, 0.0005)
verifie("ex7 déplacement de l'objectif (mm)", OAp7 - 50, 0.85, 0.01)
g7 = OAp7 / -3000
verifie("ex7 grandissement", g7, -0.0170, 0.004)
verifie("ex7 taille de l'image d'une personne de 1,80 m (mm)", -g7 * 1800, 30.5, 0.003)
verifie("ex7 position pour un objet à 1,0 m (mm)", image(-1000, 50), 52.6, 0.002)
# Exercice 8 : oeil
verifie("ex8 vergence au repos (d)", 1000 / 17, 58.8, 0.002)
fp8 = 1 / (1 / 17 + 1 / 250)
verifie("ex8 focale pour 25 cm (mm)", fp8, 15.9, 0.004)
verifie("ex8 vergence pour 25 cm (d)", 1000 / fp8, 62.8, 0.002)
verifie("ex8 accommodation (d)", 1000 / fp8 - 1000 / 17, 4.0)
verifie("ex8 taille sur la rétine d'une lettre de 5 mm à 25 cm (mm)", 17 / 250 * 5, 0.34)
# Exercice 9 : focale estimée
verifie("ex9 image d'un objet à 50 cm (cm)", image(-50, 15), 21.4, 0.003)
verifie("ex9 erreur avec un objet à 5,0 m (cm)", image(-500, 15) - 15, 0.46, 0.01)
# Exercice 10 : test de la relation de conjugaison
OA10 = [-15, -20, -25, -30, -40, -50]
OAp10 = [30.2, 19.8, 16.6, 15.1, 13.4, 12.4]
inv = [1 / b - 1 / a for a, b in zip(OA10, OAp10)]
print('   ex10 1/OA\' - 1/OA (cm-1) :', [round(x, 4) for x in inv])
verifie("ex10 moyenne de 1/f' (cm-1)", sum(inv) / 6, 0.100, 0.006)
verifie("ex10 focale (cm)", 6 / sum(inv), 10.0, 0.006)
verifie("ex10 vergence (d)", sum(inv) / 6 * 100, 10.0, 0.006)
# Exercice 12 : vidéoprojecteur
OA12 = 1 / (1 / 5000 - 1 / 20)
verifie("ex12 position de la matrice (mm)", OA12, -20.08, 0.0005)
g12 = 5000 / OA12
verifie("ex12 grandissement", g12, -249, 0.002)
verifie("ex12 largeur de l'image (m)", -g12 * 14 / 1000, 3.49, 0.002)
OA12b = 1 / (1 / 3000 - 1 / 20)
verifie("ex12 matrice pour un écran à 3,0 m (mm)", OA12b, -20.13, 0.0005)
verifie("ex12 déplacement (mm)", OA12b - OA12, -0.054, 0.01)
verifie("ex12 largeur à 3,0 m (m)", 3000 / -OA12b * 14 / 1000, 2.09, 0.003)
# Exercice 13 : smartphone
verifie("ex13 image d'un objet à 10 cm (mm)", image(-100, 4.0), 4.167, 0.001)
verifie("ex13 déplacement (mm)", image(-100, 4.0) - 4.0, 0.167, 0.006)
verifie("ex13 distance minimale de mise au point (mm)", -1 / (1 / 4.2 - 1 / 4.0), 84, 0.002)
verifie("ex13 grandissement à 84 mm", 4.2 / -84, -0.05)
# Exercice 14 : loupe et timbre
verifie("ex14 OA' (cm)", image(-6.0, 8.0), -24)
verifie("ex14 grandissement", image(-6.0, 8.0) / -6.0, 4.0)
verifie("ex14 taille d'un timbre de 2,5 cm (cm)", 4.0 * 2.5, 10)
# Exercice 15 : lentille liquide
verifie("ex15 focale pour un objet à 20 cm (mm)", 1 / (1 / 5.0 + 1 / 200), 4.878, 0.001)
verifie("ex15 vergence à l'infini (d)", 1000 / 5.0, 200)
verifie("ex15 vergence pour 20 cm (d)", 1000 / 5.0 + 1000 / 200, 205)
verifie("ex15 vergence pour 10 cm (d)", 1000 / 5.0 + 1000 / 100, 210)

# Défi D18 : photographier la Lune
alpha = 3474 / 384400
verifie("D18 diamètre apparent (rad)", alpha, 9.04e-3, 0.002)
verifie("D18 diamètre apparent (degrés)", math.degrees(alpha), 0.518, 0.002)
verifie("D18 image avec 300 mm (mm)", 300 * alpha, 2.71, 0.003)
verifie("D18 fraction de la hauteur du capteur (%)", 300 * alpha / 24 * 100, 11, 0.03)
verifie("D18 image avec un smartphone de 4 mm (micrometres)", 4 * alpha * 1000, 36, 0.01)
verifie("D18 nombre de pixels de 1,4 micrometre", 4 * alpha * 1000 / 1.4, 26, 0.01)
verifie("D18 focale pour remplir 24 mm (mm)", 24 / alpha, 2656, 0.002)
verifie("D18 position de l'image avec 300 mm (mm)", image(-384400e6, 300), 300, 1e-6)
verifie("D18 Soleil avec 300 mm (mm)", 300 * 1.392e6 / 1.496e8, 2.79, 0.003)


def programme_d18():
    alpha = 3474 / 384400
    for fp in [4, 50, 300, 1200]:
        print(fp, 'mm :', round(fp * alpha, 2), 'mm')


s18 = sortie_de(programme_d18)
print('   D18 programme :', s18.replace('\n', ' | '))
if s18 != '4 mm : 0.04 mm\n50 mm : 0.45 mm\n300 mm : 2.71 mm\n1200 mm : 10.84 mm':
    ECHECS.append('D18 programme')

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs et sorties du chapitre 18 et du défi D18 sont vérifiées.")
