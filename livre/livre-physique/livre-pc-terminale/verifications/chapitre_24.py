"""Vérification des résultats numériques du chapitre 24 (lunette astronomique) et du défi D24.

Lancer : python -I -X utf8 verifications/chapitre_24.py
"""
import io
from contextlib import redirect_stdout
from math import atan, degrees, radians, tan

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


LUNE = radians(0.52)
# L'essentiel
verifie("cours diamètre apparent de la Lune (rad)", LUNE, 9.1e-3, 0.05e-3)
verifie("cours grossissement avec 25 mm", 700 / 25, 28, 1e-9)
verifie("cours grossissement avec 10 mm", 700 / 10, 70, 1e-9)
verifie("cours image intermédiaire de la Lune (mm)", 700 * tan(LUNE), 6.4, 0.05)
verifie("cours longueur de la lunette avec 25 mm (mm)", 700 + 25, 725, 0)
verifie("cours grossissement maximal utile", 2 * 70, 140, 0)


def programme_cours():
    f1 = 700                           # mm, objectif
    theta = radians(0.52)              # diamètre apparent de la Lune
    for f2 in [25, 10, 6]:             # mm, oculaires
        G = f1 / f2
        theta2 = atan(G * tan(theta))
        print(f2, round(G), round(degrees(theta2), 1))


s = sortie_de(programme_cours).splitlines()
print('   cours programme :', s)
if s != ['25 28 14.3', '10 70 32.4', '6 117 46.6']:
    ECHECS.append('cours programme')
verifie("cours angle avec l'approximation, 6 mm (degrés)", 700 / 6 * 0.52, 60.7, 0.05)
# Exercice 1
verifie("ex1 longueur (mm)", 900 + 20, 920, 0)
verifie("ex1 grossissement", 900 / 20, 45, 1e-9)
# Exercice 2
verifie("ex2 image avec 1,0 m (mm)", 1000 * tan(LUNE), 9.1, 0.05)
verifie("ex2 image avec 300 mm (mm)", 300 * tan(LUNE), 2.7, 0.05)
verifie("ex2 image avec 2000 mm (mm)", 2000 * tan(LUNE), 18.2, 0.05)
# Exercice 3
for f2, G in ((40, 25), (20, 50), (9, 111)):
    verifie(f"ex3 grossissement avec {f2} mm", 1000 / f2, G, 0.5)
# Exercice 5
verifie("ex5 focale de l'objectif (m)", 1 / 1.25, 0.80, 1e-9)
verifie("ex5 focale de l'oculaire (cm)", 100 / 40, 2.5, 1e-9)
verifie("ex5 grossissement", 0.80 / 0.025, 32, 1e-9)
verifie("ex5 longueur (cm)", 80 + 2.5, 82.5, 1e-9)
# Exercice 6
verifie("ex6 grossissement", 700 / 10, 70, 1e-9)
verifie("ex6 angle apparent (approximation, degrés)", 70 * 0.52, 36.4, 0.05)
verifie("ex6 angle apparent exact (degrés)", degrees(atan(70 * tan(LUNE))), 32.4, 0.05)
verifie("ex6 diamètre de l'image intermédiaire (mm)", 2 * 700 * tan(LUNE / 2), 6.35, 0.005)
# Exercice 7
verifie("ex7 angle minimal à travers la lunette (rad)", 3e-4 / 70, 4.3e-6, 0.05e-6)
verifie("ex7 plus petit cratère (km)", 3e-4 / 70 * 3.84e8 / 1000, 1.6, 0.05)
verifie("ex7 plus petit cratère à l'œil nu (km)", 3e-4 * 3.84e8 / 1000, 115, 0.5)
verifie("ex7 limite de diffraction (rad)", 1.22 * 550e-9 / 0.070, 9.6e-6, 0.05e-6)
verifie("ex7 cratère limite de diffraction (km)", 1.22 * 550e-9 / 0.070 * 3.84e8 / 1000, 3.7, 0.05)
# Exercice 8
G43 = max(G for G in range(1, 100) if (G * LUNE - atan(G * tan(LUNE))) / atan(G * tan(LUNE)) < 0.05)
verifie("ex8 grossissement limite pour 5 % d'écart", G43, 43, 0)
verifie("ex8 diamètre apparent de Jupiter (rad)", radians(45 / 3600), 2.2e-4, 0.05e-4)
verifie("ex9 vergence de l'objectif (dioptries)", 1 / 1.00, 1.0, 1e-9)
verifie("ex9 vergence de l'oculaire (dioptries)", 1 / 0.050, 20, 1e-9)
verifie("ex9 nouveau grossissement", 100 / 2.5, 40, 1e-9)
verifie("ex9 nouvelle longueur (cm)", 100 + 2.5, 102.5, 1e-9)
verifie("ex6 champ de l'oculaire suffisant (degrés)", 50 - 32.4, 17.6, 0.05)
# Exercice 9
verifie("ex9 focale de l'oculaire (cm)", 105 / 21, 5.0, 1e-9)
verifie("ex9 focale de l'objectif (cm)", 105 * 20 / 21, 100, 1e-9)
# Exercice 10
verifie("ex10 grossissement inversé", 20 / 900, 0.022, 0.0005)
verifie("ex10 inverse", 900 / 20, 45, 1e-9)
# Exercice 11
verifie("ex11 champ apparent (degrés)", 10 * 6.5, 65, 1e-9)
verifie("ex11 largeur du champ à 1000 m (m)", 2 * 1000 * tan(radians(3.25)), 114, 0.5)
verifie("ex11 pupille de sortie (mm)", 50 / 10, 5.0, 1e-9)
# Exercice 12
verifie("ex12 grossissement", 16160 / 25, 646, 0.5)
mars = 25 / 3600 * 3.14159265 / 180
verifie("ex12 diamètre apparent de Mars (rad)", mars, 1.21e-4, 0.005e-4)
verifie("ex12 angle apparent dans la lunette (degrés)", degrees(16160 / 25 * mars), 4.5, 0.05)
verifie("ex12 grossissement pour égaler la Lune", LUNE / mars, 75, 0.5)
verifie("ex12 focale de l'oculaire nécessaire (mm)", 16160 / (LUNE / mars), 215, 1)
# Exercice 13
io_ang = 4.22e5 / 6.3e8
verifie("ex13 élongation maximale d'Io (rad)", io_ang, 6.7e-4, 0.05e-4)
verifie("ex13 élongation maximale d'Io (minutes)", degrees(io_ang) * 60, 2.3, 0.05)
verifie("ex13 rayon apparent de Jupiter (minutes)", 22.5 / 60, 0.375, 1e-9)
verifie("ex13 écart au bord (minutes)", degrees(io_ang) * 60 - 0.375, 1.93, 0.01)
verifie("ex13 grossissement minimal", 5 / (degrees(io_ang) * 60 - 0.375), 2.6, 0.05)
# Exercice 14
for f2, G, Gb in ((25, 36, 72), (12, 75, 150), (6, 150, 300)):
    verifie(f"ex14 grossissement avec {f2} mm", 900 / f2, G, 0.5)
    verifie(f"ex14 grossissement avec {f2} mm et Barlow", 2 * 900 / f2, Gb, 0.5)
verifie("ex14 grossissement maximal utile", 2 * 80, 160, 0)
# Exercice 15
verifie("ex15 focale de l'objectif (cm)", 100 / 2, 50, 1e-9)
verifie("ex15 focale de l'oculaire (cm)", 100 / 8, 12.5, 1e-9)
verifie("ex15 grossissement", 50 / 12.5, 4, 1e-9)
verifie("ex15 distance entre les lentilles (cm)", 50 + 12.5, 62.5, 1e-9)
verifie("ex15 taille de l'image intermédiaire (cm)", 50 * 0.050, 2.5, 1e-9)
verifie("ex15 angle de sortie (rad)", 2.5 / 12.5, 0.20, 1e-9)
# Défi D24


def programme_d24():
    D, f1 = 70, 700                    # mm
    for f2 in [40, 25, 10, 4]:         # mm, oculaires
        G = f1 / f2
        x = f2 * (f1 + f2) / f1        # position du cercle oculaire
        print(f2, round(G, 1), round(x, 1), round(D / G, 1))


s = sortie_de(programme_d24).splitlines()
print('   D24 sorties :', s)
if s != ['40 17.5 42.3 4.0', '25 28.0 25.9 2.5', '10 70.0 10.1 1.0', '4 175.0 4.0 0.4']:
    ECHECS.append('D24 sorties')
verifie("D24 position pour 10 mm (mm)", 10 * 710 / 700, 10.14, 0.005)
verifie("D24 grossissement minimal pour une pupille de 7 mm", 70 / 7, 10, 1e-9)
verifie("D24 pupille de sortie pour G = 140 (mm)", 70 / 140, 0.5, 1e-9)
verifie("D24 rapport d'éclairement 10 mm / 40 mm", (1.0 / 4.0) ** 2, 1 / 16, 1e-9)
verifie("D24 focale d'oculaire pour G = 10 (mm)", 700 / 10, 70, 1e-9)
# figure : f1 = 7, f2 = 1, tan(theta) = 0.05, demi-ouverture 1,5
verifie("figure D24 : position du cercle oculaire", 8 + 1 * 8 / 7, 9.143, 0.0005)
verifie("figure D24 : demi-diamètre du cercle oculaire", 1.5 / 7, 0.214, 0.0005)
verifie("figure D24 : rayon de bord haut au niveau de l'oculaire", -0.35 - 1.85 / 7, -0.614, 0.0005)
verifie("figure D24 : rayon de bord haut au cercle oculaire", -0.35 - 1.85 / 7 + 0.35 * (1 * 8 / 7), -0.214, 0.0005)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 24 et du défi D24 sont vérifiées.")
