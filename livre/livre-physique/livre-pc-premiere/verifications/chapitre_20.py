"""Vérification du chapitre 20 (Lumière : ondes et photons) et du défi D20.

Lancer : python -I -X utf8 verifications/chapitre_20.py
"""
import io
from contextlib import redirect_stdout

ECHECS = []
C, H, EV = 3.00e8, 6.63e-34, 1.60e-19


def verifie(nom, calcule, publie, tol_rel=0.006):
    ok = abs(calcule - publie) <= tol_rel * abs(publie) + 1e-40
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:60s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def sortie_de(fonction):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    return tampon.getvalue().strip()


def compare_sortie(nom, fonction, attendu):
    s = sortie_de(fonction)
    print(f'   {nom} :', s.replace('\n', ' | '))
    if s != attendu:
        ECHECS.append(nom)


def lam_nm(delta_ev):
    return H * C / (delta_ev * EV) * 1e9


def e_ev(lam_en_nm):
    return H * C / (lam_en_nm * 1e-9) / EV


def e_h(n):
    return -13.6 / n**2


# Cours
verifie("cours fréquence à 500 nm (Hz)", C / 500e-9, 6.00e14)
verifie("cours énergie d'un photon de 500 nm (J)", H * C / 500e-9, 3.98e-19, 0.002)
verifie("cours énergie d'un photon de 500 nm (eV)", e_ev(500), 2.49, 0.002)
verifie("cours photon rouge 800 nm (eV)", e_ev(800), 1.6, 0.03)
verifie("cours photon violet 400 nm (eV)", e_ev(400), 3.1, 0.01)
verifie("cours photon X 0,1 nm (eV, ordre 1e4)", e_ev(0.1), 1.2e4, 0.05)
verifie("cours photon micro-onde (eV, ordre 1e-5)", H * 2.45e9 / EV, 1.0e-5, 0.02)
verifie("cours wifi 2,4 GHz (cm)", C / 2.4e9 * 100, 12.5)
verifie("cours radio FM 100 MHz (m)", C / 100e6, 3.0)
verifie("cours niveaux de l'hydrogène n=2", e_h(2), -3.40)
verifie("cours niveaux de l'hydrogène n=3", e_h(3), -1.51, 0.003)
verifie("cours niveaux de l'hydrogène n=4", e_h(4), -0.85)
verifie("cours niveaux de l'hydrogène n=5", e_h(5), -0.54, 0.01)
verifie("cours raie H-alpha (nm)", lam_nm(-1.51 + 3.40), 658, 0.003)
verifie("cours absorption 1 -> 2 (eV)", -3.40 + 13.6, 10.2)


def programme_cours():
    h, c, e = 6.63e-34, 3.00e8, 1.60e-19
    for n in [3, 4, 5, 6]:
        dE = 13.6 / 2**2 - 13.6 / n**2       # eV : ecart entre les niveaux n et 2
        lam = h * c / (dE * e)                # m
        print(n, '-> 2 :', round(dE, 2), 'eV ;', round(lam * 1e9), 'nm')


compare_sortie('cours programme', programme_cours,
               '3 -> 2 : 1.89 eV ; 658 nm\n4 -> 2 : 2.55 eV ; 488 nm\n5 -> 2 : 2.86 eV ; 435 nm\n6 -> 2 : 3.02 eV ; 411 nm')
for lam_mesure, lam_calc in [(656.3, 658), (486.1, 488), (434.0, 435), (410.2, 411)]:
    verifie(f"cours écart dû aux arrondis {lam_mesure} nm (%)", abs(lam_calc - lam_mesure) / lam_mesure * 100, 0.3, 0.5)

# Exercice 1 : domaines
verifie("ex1 wifi 2,4 GHz (cm)", C / 2.4e9 * 100, 12.5)
verifie("ex1 four 2,45 GHz (cm)", C / 2.45e9 * 100, 12.2, 0.005)
verifie("ex1 rayonnement de 0,10 nm (Hz)", C / 0.10e-9, 3.0e18)
verifie("ex1 infrarouge de 10 micrometres (Hz)", C / 10e-6, 3.0e13)
# Exercice 2 : photons
verifie("ex2 rouge 700 nm (J)", H * C / 700e-9, 2.84e-19, 0.002)
verifie("ex2 rouge 700 nm (eV)", e_ev(700), 1.78, 0.003)
verifie("ex2 violet 400 nm (J)", H * C / 400e-9, 4.97e-19, 0.002)
verifie("ex2 violet 400 nm (eV)", e_ev(400), 3.11, 0.002)
verifie("ex2 rapport violet / rouge", 700 / 400, 1.75)
# Exercice 3 : diagramme de l'hydrogène
verifie("ex3 transition 2 -> 1 (eV)", -3.40 + 13.6, 10.2)
verifie("ex3 transition 2 -> 1 (J)", 10.2 * EV, 1.63e-18, 0.002)
verifie("ex3 longueur d'onde (nm)", lam_nm(10.2), 122, 0.003)
verifie("ex3 transition 3 -> 1 (eV)", -1.51 + 13.6, 12.09, 0.001)
verifie("ex3 transition 3 -> 1 (nm)", lam_nm(-1.51 + 13.6), 103, 0.003)
# Exercice 4 : sodium
verifie("ex4 fréquence à 589 nm (Hz)", C / 589e-9, 5.09e14, 0.002)
verifie("ex4 énergie à 589 nm (J)", H * C / 589e-9, 3.38e-19, 0.002)
verifie("ex4 énergie à 589 nm (eV)", e_ev(589), 2.11, 0.002)
verifie("ex4 écart entre les niveaux (eV)", -3.03 + 5.14, 2.11)
# Exercice 5 : micro-ondes et UV
verifie("ex5 photon micro-onde (J)", H * 2.45e9, 1.62e-24, 0.004)
verifie("ex5 photon micro-onde (eV)", H * 2.45e9 / EV, 1.0e-5, 0.02)
verifie("ex5 photon UV de 300 nm (eV)", e_ev(300), 4.14, 0.003)
verifie("ex5 rapport UV / micro-onde", e_ev(300) / (H * 2.45e9 / EV), 4.1e5, 0.01)


# Exercice 6 : programme des domaines
def programme_ex6():
    h, c, e = 6.63e-34, 3.00e8, 1.60e-19

    def domaine(lam):
        if lam < 400e-9:
            return 'UV'
        if lam <= 800e-9:
            return 'visible'
        return 'IR'
    for haut, bas in [(2, 1), (3, 2), (4, 3)]:
        dE = 13.6 / bas**2 - 13.6 / haut**2
        lam = h * c / (dE * e)
        print(haut, '->', bas, ':', round(lam * 1e9), 'nm', domaine(lam))


compare_sortie('ex6 programme', programme_ex6, '2 -> 1 : 122 nm UV\n3 -> 2 : 658 nm visible\n4 -> 3 : 1880 nm IR')
verifie("ex6 transition 5 -> 2 (nm)", lam_nm(13.6 / 4 - 13.6 / 25), 435, 0.003)
verifie("ex6 calcul 2 -> 1 détaillé (eV)", 13.6 / 1 - 13.6 / 4, 10.2)
# Exercice 7 : laser
Eph7 = H * C / 650e-9
verifie("ex7 fréquence (Hz)", C / 650e-9, 4.62e14, 0.002)
verifie("ex7 énergie d'un photon (J)", Eph7, 3.06e-19, 0.002)
verifie("ex7 énergie d'un photon (eV)", Eph7 / EV, 1.91, 0.003)
verifie("ex7 photons par seconde", 1.0e-3 / Eph7, 3.27e15, 0.003)
verifie("ex7 laser vert, énergie d'un photon (J)", H * C / 532e-9, 3.74e-19, 0.002)
verifie("ex7 laser vert, photons par seconde", 1.0e-3 / (H * C / 532e-9), 2.67e15, 0.003)
verifie("ex7 énergie en 1 min (J)", 1.0e-3 * 60, 0.060)
# Exercice 8 : mercure
NIV_HG = [-10.44, -5.55, -4.99, -3.74, -2.71, -1.56]
for haut, bas, lam in [(-2.71, -5.55, 438), (-2.71, -4.99, 545), (-5.55, -10.44, 254)]:
    verifie(f"ex8 transition {haut} -> {bas} (nm)", lam_nm(haut - bas), lam, 0.003)
verifie("ex8 écart E4 - E1 (eV)", -2.71 + 5.55, 2.84)
verifie("ex8 écart E4 - E2 (eV)", -2.71 + 4.99, 2.28)
verifie("ex8 écart E1 - E0 (eV)", -5.55 + 10.44, 4.89)
ecarts_depuis_E0 = [round(n - NIV_HG[0], 2) for n in NIV_HG[1:]]
print('   ex8 écarts depuis E0 :', ecarts_depuis_E0)
if 4.00 in ecarts_depuis_E0 or 4.89 not in ecarts_depuis_E0:
    ECHECS.append('ex8 photon de 4,00 eV')
# Exercice 9 : rayons X
Ex = H * C / 0.050e-9
verifie("ex9 fréquence (Hz)", C / 0.050e-9, 6.0e18)
verifie("ex9 énergie d'un photon X (J)", Ex, 3.98e-15, 0.002)
verifie("ex9 énergie d'un photon X (eV)", Ex / EV, 2.49e4, 0.002)
verifie("ex9 rapport X / visible", Ex / (H * C / 500e-9), 1.0e4)
# Exercice 10 : absorption par l'hydrogène
ecarts_h = [round(e_h(n) - e_h(1), 1) for n in [2, 3, 4]]
print("   ex10 écarts depuis le fondamental :", ecarts_h)
if ecarts_h[:2] != [10.2, 12.1] or 11.0 in ecarts_h:
    ECHECS.append('ex10 photons absorbés')
verifie("ex10 longueur d'onde d'ionisation (nm)", lam_nm(13.6), 91.4, 0.003)
verifie("ex10 énergie cinétique de l'électron (eV)", 15.0 - 13.6, 1.4)
# Exercice 11 : DEL
verifie("ex11 DEL rouge 1,9 eV (nm)", lam_nm(1.9), 654, 0.003)
verifie("ex11 DEL bleue 2,76 eV (nm)", lam_nm(2.76), 450, 0.003)
verifie("ex11 DEL verte 525 nm (eV)", e_ev(525), 2.37, 0.002)
# Exercice 12 : four à micro-ondes
verifie("ex12 longueur d'onde (cm)", C / 2.45e9 * 100, 12.2, 0.005)
verifie("ex12 deux intervalles mesurés (cm)", 13.2 - 1.0, 12.2)
verifie("ex12 écart entre points chauds (cm)", (13.2 - 1.0) / 2, 6.1)
verifie("ex12 célérité mesurée (m/s)", 2 * 0.061 * 2.45e9, 2.99e8, 0.002)
verifie("ex12 photons par seconde à 800 W", 800 / (H * 2.45e9), 4.9e26, 0.01)
# Exercice 13 : feux d'artifice
verifie("ex13 sodium 589 nm (eV)", e_ev(589), 2.11, 0.002)
verifie("ex13 strontium 650 nm (eV)", e_ev(650), 1.91, 0.003)
verifie("ex13 baryum 520 nm (eV)", e_ev(520), 2.39, 0.003)
# Exercice 14 : silicium
verifie("ex14 longueur d'onde maximale (nm)", lam_nm(1.12), 1110, 0.003)
verifie("ex14 photon de 500 nm (eV)", e_ev(500), 2.49, 0.002)
verifie("ex14 photon de 500 nm, énergie perdue (eV)", e_ev(500) - 1.12, 1.37, 0.003)
verifie("ex14 fraction perdue (%)", (2.49 - 1.12) / 2.49 * 100, 55, 0.01)
verifie("ex14 photon de 1500 nm (eV)", e_ev(1500), 0.83, 0.003)
# Exercice 15 : raies de Fraunhofer
verifie("ex15 raie de 656,3 nm (eV)", e_ev(656.3), 1.89, 0.003)
verifie("ex15 raie de 486,1 nm (eV)", e_ev(486.1), 2.56, 0.003)
verifie("ex15 transition 3 -> 2 (eV)", e_h(3) - e_h(2), 1.89, 0.002)
verifie("ex15 transition 4 -> 2 (eV)", e_h(4) - e_h(2), 2.55, 0.002)

# Valeurs intermédiaires des corrigés
verifie("cor3 transition 3 -> 1 (J)", 12.09 * EV, 1.93e-18, 0.003)
verifie("cor5 photon UV de 300 nm (J)", H * C / 300e-9, 6.63e-19)
verifie("cor8 niveau manquant pour 4,00 eV (eV)", -10.44 + 4.00, -6.44)
verifie("cor10 niveau visé avec 11,0 eV (eV)", -13.6 + 11.0, -2.6)
verifie("cor11 DEL verte (J)", H * C / 525e-9, 3.79e-19, 0.002)
verifie("cor14 longueur d'onde maximale (m)", lam_nm(1.12) * 1e-9, 1.11e-6, 0.003)
verifie("cor15 raie de 656,3 nm (J)", H * C / 656.3e-9, 3.03e-19, 0.002)
verifie("cor15 raie de 486,1 nm (J)", H * C / 486.1e-9, 4.09e-19, 0.002)

# Défi D20 : de quoi les étoiles sont-elles faites ?
verifie("D20 transition 5 -> 2 (eV)", e_h(5) - e_h(2), 2.86, 0.002)
verifie("D20 Balmer 5 -> 2 (nm)", lam_nm(e_h(5) - e_h(2)), 435, 0.003)
verifie("D20 écart relatif avec 434,0 nm (%)", (435.3 - 434.0) / 434.0 * 100, 0.3, 0.05)


def programme_d20():
    mesures = [656.3, 589.0, 527.0, 517.3, 486.1, 434.0, 393.4]   # nm
    tables = {'H': [656.3, 486.1, 434.0, 410.2], 'Na': [589.0, 589.6],
              'Mg': [517.3, 518.4], 'Fe': [527.0, 438.4], 'Ca': [393.4, 396.8]}
    trouves = []
    for lam in mesures:
        for el in tables:
            for r in tables[el]:
                if abs(lam - r) < 0.5 and el not in trouves:
                    trouves.append(el)
    print(trouves)


compare_sortie('D20 programme', programme_d20, "['H', 'Na', 'Fe', 'Mg', 'Ca']")
verifie("D20 énergie de la raie du calcium 393,4 nm (eV)", e_ev(393.4), 3.16, 0.003)
verifie("D20 écart hélium 587,6 / sodium 589,0 (nm)", 589.0 - 587.6, 1.4)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs et sorties du chapitre 20 et du défi D20 sont vérifiées.")
