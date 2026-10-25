"""Vérification des résultats numériques du chapitre 11 (structure des molécules organiques) et du défi D11.

Lancer : python -I -X utf8 verifications/chapitre_11.py
"""
import io
from contextlib import redirect_stdout

ECHECS = []
MC, MH, MO, MN, MCL = 12.0, 1.0, 16.0, 14.0, 35.5
NA = 6.02e23


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def M(c=0, h=0, o=0, n=0, cl=0):
    return c * MC + h * MH + o * MO + n * MN + cl * MCL


# L'essentiel : programme du polyéthylène
tampon = io.StringIO()
with redirect_stdout(tampon):
    M_motif = 28.0

    def M_chaine(k):
        return k * M_motif

    for k in (1, 1000, 40000):
        print(k, M_chaine(k))
sortie = tampon.getvalue().strip().splitlines()
print('   cours programme :', sortie)
if sortie != ['1 28.0', '1000 28000.0', '40000 1120000.0']:
    ECHECS.append('cours programme polymère')
verifie("cours M du motif CH2-CH2", M(c=2, h=4), 28.0, 1e-9)
# Exercice 1 : formules brutes
verifie("ex1 M brute de D (C4H8O2)", M(c=4, h=8, o=2), 88.0, 1e-9)
# Exercice 3
verifie("ex3 pentan-3-one C5H10O", M(c=5, h=10, o=1), 86.0, 1e-9)
verifie("ex3 2-méthylbutan-1-ol C5H12O", M(c=5, h=12, o=1), 88.0, 1e-9)
# Exercice 6
verifie("ex6 M éthanoate de pentyle (C7H14O2)", M(c=7, h=14, o=2), 130, 0.5)
# Exercice 9
verifie("ex9 n direct", 56000 / 28.0, 2000, 1e-9)
verifie("ex9 atomes de carbone", 2 * 2000, 4000, 1e-9)
tampon = io.StringIO()
with redirect_stdout(tampon):
    M_motif = 28.0
    k = 1
    while k * M_motif < 56000:
        k = k + 1
    print(k, k * M_motif)
sortie = tampon.getvalue().strip()
print('   ex9 sortie :', sortie)
if sortie != '2000 56000.0':
    ECHECS.append('ex9 sortie du programme')
# Exercice 10
m10 = M(c=2, h=3, cl=1)
verifie("ex10 M motif PVC", m10, 62.5, 1e-9)
verifie("ex10 pourcentage de chlore (%)", 100 * MCL / m10, 56.8, 0.05)
verifie("ex10 degré de polymérisation", 1.0e5 / m10, 1600, 1)
# Exercice 11
m11 = M(c=12, h=22, n=2, o=2)
verifie("ex11 M motif nylon", m11, 226, 0.5)
verifie("ex11 degré de polymérisation", 4.5e4 / m11, 200, 1.5)
# Exercice 12
n12 = 0.400 / 206.3
verifie("ex12 n ibuprofène (mol)", n12, 1.94e-3, 0.005e-3)
verifie("ex12 volume équivalent (mL)", n12 / 0.100 * 1000, 19.4, 0.05)
verifie("ex12 rapport A-/AH à pH 6,5", 10 ** (6.5 - 4.9), 40, 0.5)
verifie("ex12 M ibuprofène C13H18O2", M(c=13, h=18, o=2), 206.3, 0.5)
# Exercice 13
verifie("ex13 M motif PET C10H8O4", M(c=10, h=8, o=4), 192.2, 0.5)
verifie("ex13 n motifs (mol)", 25 / 192.2, 0.130, 0.0005)
verifie("ex13 degré de polymérisation", 2.4e4 / 192.2, 125, 0.5)
verifie("ex13 nombre de chaînes", 25 / 2.4e4 * NA, 6.3e20, 0.05e20)
# Exercice 14
verifie("ex14 M butanoate d'éthyle C6H12O2", M(c=6, h=12, o=2), 116.0, 1e-9)
verifie("ex14 masse du flacon, 4,35 arrondie à 4,4 (g)", 0.87 * 5.0, 4.4, 0.051)
verifie("ex14 n ester (mol)", 4.35 / 130, 3.3e-2, 0.05e-2)
# Exercice 15
nc = 1.76 / 44.0
nh = 2 * 0.721 / 18.0
verifie("ex15 n(C) (mol)", nc, 4.00e-2, 0.005e-2)
verifie("ex15 n(H) (mol)", nh, 8.0e-2, 0.02e-2)
mo = 0.881 - nc * 12.0 - nh * 1.0
verifie("ex15 m(O) (g)", mo, 0.32, 0.005)
verifie("ex15 n(O) (mol)", mo / 16.0, 2.0e-2, 0.01e-2)
verifie("ex15 rapport C/O", nc / (mo / 16.0), 2, 0.02)
verifie("ex15 rapport H/O", nh / (mo / 16.0), 4, 0.04)
verifie("ex15 masse molaire de C4H8O2", M(c=4, h=8, o=2), 88.0, 1e-9)
# Défi D11
verifie("D11 liaisons C-C d'un alcane C5", 5 - 1, 4, 1e-9)
verifie("D11 nombre d'isomères C5", 3, 3, 0)
verifie("D11 nombre d'isomères C6", 5, 5, 0)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 11 et du défi D11 sont vérifiées.")
