"""Vérification des résultats numériques du chapitre 5 (mécanismes réactionnels) et du défi D05.

Lancer : python -I -X utf8 verifications/chapitre_05.py
"""
from math import log, sqrt

ECHECS = []


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


CHI = {'H': 2.20, 'C': 2.55, 'N': 3.04, 'O': 3.44, 'Cl': 3.16, 'Br': 2.96, 'I': 2.66}

# L'essentiel et exercice 2 : différences d'électronégativité
for a, b, publie in (('C', 'H', 0.35), ('C', 'Cl', 0.61), ('C', 'O', 0.89), ('O', 'H', 1.24),
                     ('H', 'Br', 0.76), ('C', 'N', 0.49), ('N', 'H', 0.84)):
    verifie(f"Δχ {a}-{b}", abs(CHI[a] - CHI[b]), publie, 1e-9)
verifie("liaison C-H non polarisée (Δχ < 0,4)", float(abs(CHI['C'] - CHI['H']) < 0.4), 1.0, 0)
verifie("liaison C-N polarisée (Δχ ≥ 0,4)", float(abs(CHI['C'] - CHI['N']) >= 0.4), 1.0, 0)

# Exercice 10 : facteur sur la vitesse
verifie("ex10 rapport des temps de demi-réaction", 40 / 2, 20, 1e-9)

# Exercice 11 : modèle des chocs
f = sqrt(303.15 / 293.15)
verifie("ex11 facteur sur la fréquence des chocs", f, 1.017, 0.0005)
verifie("ex11 augmentation relative (%)", (f - 1) * 100, 1.7, 0.05)
verifie("ex11 facteur sur la proportion de chocs efficaces", 2 / f, 2, 0.05)
verifie("ex11 concentrations doublées", 2 * 2, 4, 0)
verifie("ex11 dilution par 5", 5 * 5, 25, 0)

# Exercice 12 : ozone détruit par 1,0 kg de CFC-12
n_cfc = 1000 / 120.9
verifie("ex12 n(CF2Cl2) (mol)", n_cfc, 8.27, 0.005)
verifie("ex12 n(Cl) (mol)", 2 * n_cfc, 16.5, 0.05)
n_o3 = 1.0e5 * 2 * n_cfc
verifie("ex12 n(O3) (mol)", n_o3, 1.65e6, 0.005e6)
verifie("ex12 m(O3) (g)", n_o3 * 48.0, 7.9e7, 0.05e7)

# Exercice 15 : SN1 / SN2
verifie("ex15 k du 2-bromo-2-méthylpropane (s-1)", log(2) / 85, 8.2e-3, 0.05e-3)
verifie("ex15 t1/2 du bromométhane pour [HO-] = 0,050 (min)", 50 * 0.10 / 0.050, 100, 1e-9)

# Défi D05 : horloge à iode
di2 = 5.0e-4 / 2
verifie("D05 [I2] produit avant le virage (mol/L)", di2, 2.5e-4, 1e-12)
verifie("D05 baisse relative maximale de [H2O2] (%)", di2 / 0.010 * 100, 2.5, 1e-9)
experiences = [(0.020, 0.020, 52, 0.0120), (0.020, 0.040, 26, 0.0120), (0.040, 0.020, 27, 0.0116),
               (0.010, 0.020, 103, 0.0121), (0.020, 0.010, 105, 0.0119)]
ks = []
for i, (h, iod, tc, publie) in enumerate(experiences, 1):
    k = di2 / (tc * h * iod)
    ks.append(k)
    verifie(f"D05 k de l'expérience {i} (L/mol/s)", k, publie, 0.00005)
verifie("D05 k moyen (L/mol/s)", sum(ks) / len(ks), 0.012, 0.0005)
verifie("D05 t_c pour 0,030 / 0,030 (s)", di2 / (0.012 * 0.030 * 0.030), 23, 0.5)
for x, tc, publie in ((0.010, 105, 0.009524), (0.020, 52, 0.019231), (0.040, 26, 0.038462),
                      (0.010, 103, 0.009709), (0.040, 27, 0.037037)):
    verifie(f"D05 1/t_c (figure) pour t_c = {tc} s", 1 / tc, publie, 5e-7)
verifie("D05 pente de la droite 1/t_c = f(c) (L/mol/s)", 0.012 * 0.020 / di2, 0.96, 1e-9)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 5 et du défi D05 sont vérifiées.")
