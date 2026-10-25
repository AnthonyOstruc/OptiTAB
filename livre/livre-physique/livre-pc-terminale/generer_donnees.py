"""Génère les données numériques des figures (courbes de titrage, séries de mesures, simulations).

Les courbes de titrage sont calculées exactement (électroneutralité, autoprotolyse de l'eau,
loi de Kohlrausch avec dilution). Les séries aléatoires utilisent des graines fixes : le livre
est reproductible. Lancer : python -I -X utf8 generer_donnees.py
"""
from math import log10, sqrt
from pathlib import Path
import numpy as np

DOSSIER = Path(__file__).resolve().parent / 'figures' / 'donnees'
KE = 1.0e-14
# Conductivités molaires ioniques à 25 °C, en mS.m2.mol-1
LAMBDA = {'H3O': 35.0, 'HO': 19.9, 'Na': 5.01, 'K': 7.35, 'Cl': 7.63, 'NO3': 7.14,
          'CH3COO': 4.09, 'Ag': 6.19, 'NH4': 7.35}


def ecrire(nom, colonnes, entete, fmt='%.4f'):
    DOSSIER.mkdir(parents=True, exist_ok=True)
    tableau = np.column_stack(colonnes)
    np.savetxt(DOSSIER / f'{nom}.dat', tableau, fmt=fmt, header=entete, comments='')
    print(f'{nom}.dat : {len(tableau)} lignes')


def resoudre_h(bilan):
    """Résout bilan(h) = 0 (fonction croissante de h) par dichotomie sur log10 h."""
    bas, haut = -14.5, 0.5
    for _ in range(200):
        milieu = (bas + haut) / 2
        if bilan(10 ** milieu) > 0:
            haut = milieu
        else:
            bas = milieu
    return 10 ** ((bas + haut) / 2)


def ph_acides_par_base(acides, va, cb, v_ml):
    """pH d'un mélange d'acides (liste de (c, Ka) ; Ka=None pour un acide fort) titré par une base forte."""
    vt = (va + v_ml) / 1000
    na = cb * v_ml / 1000 / vt

    def bilan(h):
        anions = KE / h
        for c, ka in acides:
            ct = c * va / 1000 / vt
            anions += ct if ka is None else ct * ka / (ka + h)
        return h + na - anions
    return -log10(resoudre_h(bilan))


def ph_base_forte_par_acide_fort(cb, vb, ca, v_ml):
    vt = (vb + v_ml) / 1000
    cl = ca * v_ml / 1000 / vt
    na = cb * vb / 1000 / vt
    return -log10(resoudre_h(lambda h: h + na - cl - KE / h))


def derivee(x, y):
    return np.gradient(np.array(y), np.array(x))


def courbes_titrage():
    # Chapitre 3, essentiel et exercice 3 : acide chlorhydrique 1,00e-2 (20,0 mL) par soude 1,00e-2
    v = np.round(np.arange(0, 40.01, 0.25), 2)
    ph = [ph_acides_par_base([(1.00e-2, None)], 20.0, 1.00e-2, x) for x in v]
    ecrire('03-hcl-naoh-ph', [v, ph], 'V pH')
    # Vinaigre dilué dix fois (1,01e-1 mol/L, 10,0 mL) par soude 0,100 : exercice 8
    v = np.round(np.arange(0, 20.01, 0.1), 2)
    ph = [ph_acides_par_base([(1.01e-1, 10 ** -4.76)], 10.0, 0.100, x) for x in v]
    ecrire('03-vinaigre-ph', [v, ph, derivee(v, ph)], 'V pH d')
    # Déboucheur dilué 25 fois : soude 0,108 mol/L (20,0 mL) par acide chlorhydrique 0,100 : exercice 12
    v = np.round(np.arange(0, 35.01, 0.1), 2)
    ph = [ph_base_forte_par_acide_fort(0.108, 20.0, 0.100, x) for x in v]
    ecrire('03-deboucheur-ph', [v, ph], 'V pH')
    # Aspirine : 6,90e-4 mol dans 50,0 mL, pKa 3,5, soude 0,0500 : exercice 13
    v = np.round(np.arange(0, 25.01, 0.1), 2)
    ph = [ph_acides_par_base([(6.90e-4 / 0.0500, 10 ** -3.5)], 50.0, 0.0500, x) for x in v]
    ecrire('03-aspirine-ph', [v, ph, derivee(v, ph)], 'V pH d')
    # Essentiel : acide éthanoïque 1,00e-2 (20,0 mL) par soude 1,00e-2, pour comparer acide fort et faible
    v = np.round(np.arange(0, 40.01, 0.25), 2)
    ph = [ph_acides_par_base([(1.00e-2, 10 ** -4.76)], 20.0, 1.00e-2, x) for x in v]
    ecrire('03-ethanoique-ph', [v, ph, derivee(v, ph)], 'V pH d')
    # Défi D03 : 0,150 g d'acide butanedioïque (diacide, pKa 4,21 et 5,64) dans 50,0 mL, soude 0,100
    v = np.round(np.arange(0, 40.01, 0.2), 2)
    n_acide = 0.150 / 118.09
    ph = [ph_diacide_par_base(n_acide / 0.0500, 10 ** -4.21, 10 ** -5.64, 50.0, 0.100, x) for x in v]
    ecrire('03-succinique-ph', [v, ph, derivee(v, ph)], 'V pH d')


def ph_diacide_par_base(c, k1, k2, va, cb, v_ml):
    """pH d'un diacide H2A (concentration c dans va mL) titré par une base forte."""
    vt = (va + v_ml) / 1000
    ct = c * va / 1000 / vt
    na = cb * v_ml / 1000 / vt

    def bilan(h):
        d = h * h + k1 * h + k1 * k2
        return h + na - ct * (k1 * h + 2 * k1 * k2) / d - KE / h
    return -log10(resoudre_h(bilan))


def sigma(especes, vt):
    """Conductivité en mS/cm : especes = {ion: quantité en mol}, vt en L."""
    s = sum(LAMBDA[ion] * n / vt for ion, n in especes.items())  # lambda (mS.m2/mol) x c (mol/L)
    # c en mol/m3 = 1000 c(mol/L) donne sigma en mS/m ; 1 mS/cm = 100 mS/m : facteur global 1000/100 = 10
    return s * 10


def courbes_conductimetrie():
    # Exercice 4 : 20,0 mL de soude 2,00e-2 + 180 mL d'eau, titrés par l'acide chlorhydrique 0,0500
    v = np.round(np.arange(0, 16.01, 1.0), 2)
    nb0 = 2.00e-2 * 0.0200
    s = []
    for x in v:
        na = 0.0500 * x / 1000
        vt = 0.2000 + x / 1000
        s.append(sigma({'Na': nb0, 'HO': max(nb0 - na, 0) + 1e-12, 'Cl': na, 'H3O': max(na - nb0, 0)}, vt))
    ecrire('03-naoh-hcl-sigma', [v, s], 'V sigma')
    # Essentiel : 20,0 mL d'acide chlorhydrique 1,00e-2 + 180 mL d'eau, soude 0,100
    v = np.round(np.arange(0, 4.01, 0.25), 2)
    na0 = 1.00e-2 * 0.0200
    s = []
    for x in v:
        nb = 0.100 * x / 1000
        vt = 0.2000 + x / 1000
        h = max(na0 - nb, 0) + 1e-12
        oh = max(nb - na0, 0)
        s.append(sigma({'H3O': h, 'Cl': na0, 'Na': nb, 'HO': oh}, vt))
    ecrire('03-hcl-naoh-sigma', [v, s], 'V sigma')
    # Exercice 9 : 20,0 mL de sérum dilué dix fois (Cl- 1,54e-2) + 200 mL d'eau, nitrate d'argent 0,0500
    v = np.round(np.arange(0, 12.01, 0.5), 2)
    ncl0 = 1.54e-2 * 0.0200
    s = []
    for x in v:
        nag = 0.0500 * x / 1000
        vt = 0.2200 + x / 1000
        s.append(sigma({'Na': ncl0, 'Cl': max(ncl0 - nag, 0), 'Ag': max(nag - ncl0, 0), 'NO3': nag}, vt))
    ecrire('03-chlorure-sigma', [v, s], 'V sigma')
    # Exercice 14 : mélange HCl 0,020 + CH3COOH 0,050 (20,0 mL) + 180 mL d'eau, soude 0,100
    v = np.round(np.arange(0, 20.01, 0.5), 2)
    s = []
    for x in v:
        va, vt_ml = 20.0, 200.0 + x
        ph = ph_acides_par_base([(0.020 * va / 200.0, None), (0.050 * va / 200.0, 10 ** -4.76)], 200.0, 0.100, x)
        h = 10 ** -ph
        vt = vt_ml / 1000
        ct = 0.050 * va / 1000
        n_ac = ct * 10 ** -4.76 / (10 ** -4.76 + h)
        s.append(sigma({'H3O': h * vt, 'HO': KE / h * vt, 'Cl': 0.020 * va / 1000, 'Na': 0.100 * x / 1000,
                        'CH3COO': n_ac}, vt))
    ecrire('03-melange-sigma', [v, s], 'V sigma')
    # Exercice 15 : 20,0 mL d'acide chlorhydrique 5,00e-2 sans eau ajoutée, soude 0,100 (dilution non négligeable)
    v = np.round(np.arange(0, 20.01, 1.0), 2)
    na0 = 5.00e-2 * 0.0200
    s, s_corr = [], []
    for x in v:
        nb = 0.100 * x / 1000
        vt = 0.0200 + x / 1000
        h = max(na0 - nb, 0) + 1e-12
        oh = max(nb - na0, 0)
        val = sigma({'H3O': h, 'Cl': na0, 'Na': nb, 'HO': oh}, vt)
        s.append(val)
        s_corr.append(val * (20.0 + x) / 20.0)
    ecrire('03-dilution-sigma', [v, s, s_corr], 'V sigma sigmacorr')


def courbes_cinetique():
    """Données du chapitre 4 : lois d'ordre 1 (avec un léger bruit de mesure) et ordre 2 pour le défi D04."""
    rng = np.random.default_rng(404)
    # Exercice 6 : absorbance du diiode, A = 0,500 (1 - exp(-k t)), k = ln2 / 10 min
    t = np.array([0, 2, 4, 6, 8, 10, 15, 20, 25, 30, 40, 50], dtype=float)
    a = 0.500 * (1 - np.exp(-np.log(2) / 10 * t)) + rng.normal(0, 0.002, t.size) * (t > 0)
    ecrire('04-iodure-absorbance', [t, np.round(a, 3)], 't A', fmt='%.3f')
    # Exercice 8 : volumes équivalents des prélèvements (titrage du peroxyde d'hydrogène), t1/2 = 12 min
    t = np.array([0, 5, 10, 15, 20, 30, 40, 60], dtype=float)
    ve = 16.0 * np.exp(-np.log(2) / 12 * t) + rng.normal(0, 0.03, t.size) * (t > 0)
    ecrire('04-peroxyde-titrage', [t, np.round(ve, 1)], 't VE', fmt='%.1f')
    # Exercice 9 : caféine plasmatique (mg/L), phase d'élimination, t1/2 = 5,0 h
    t = np.array([1, 2, 4, 6, 8, 12], dtype=float)
    c = 3.60 * np.exp(-np.log(2) / 5.0 * (t - 1)) * (1 + rng.normal(0, 0.006, t.size))
    ecrire('04-cafeine', [t, np.round(c, 2)], 't C', fmt='%.2f')
    # Exercice 11 : cristal violet (umol/L), k = 0,0250 min-1
    t = np.arange(0, 40.1, 4.0)
    c = 20.0 * np.exp(-0.0250 * t) * (1 + rng.normal(0, 0.004, t.size) * (t > 0))
    ecrire('04-violet', [t, np.round(c, 2)], 't c', fmt='%.2f')
    # Exercice 12 : décoloration du bleu brillant par l'eau de Javel, deux concentrations en ion hypochlorite
    t = np.arange(0, 60.1, 5.0)
    a1 = 0.800 * np.exp(-np.log(2) / 30 * t)
    a2 = 0.800 * np.exp(-np.log(2) / 15 * t)
    ecrire('04-e133-javel', [t, np.round(a1, 3), np.round(a2, 3)], 't A1 A2', fmt='%.3f')
    # Exercice 15 : hydrolyse du chlorure de tertiobutyle suivie par conductimétrie, t1/2 = 300 s
    t = np.arange(0, 1200.1, 100.0)
    s = 1.62 * (1 - np.exp(-np.log(2) / 300 * t)) + rng.normal(0, 0.004, t.size) * (t > 0)
    ecrire('04-tertiobutyle', [t, np.round(s, 3)], 't sigma', fmt='%.3f')
    # Défi D04 : saponification, [ester]0 = [HO-]0 = 1,00e-2 mol/L, k = 0,11 L/mol/s (ordre 2)
    t = np.array([0, 120, 300, 600, 900, 1200, 1800], dtype=float)
    c = 1.00e-2 / (1 + 0.11 * 1.00e-2 * t)
    ecrire('04-saponification', [t, np.round(c * 1000, 2)], 't c_mmol', fmt='%.2f')


def series_mesures():
    rng = np.random.default_rng(2027)
    # Chapitre 27, essentiel : 40 mesures d'une durée de chute (s)
    mesures = np.round(rng.normal(0.452, 0.012, 40), 3)
    np.savetxt(DOSSIER / '27-chute-mesures.dat', mesures, fmt='%.3f', header='t', comments='')
    bords = np.arange(0.420, 0.4901, 0.005)
    comptes, _ = np.histogram(mesures, bins=bords)
    ecrire('27-chute-histo', [bords[:-1], comptes], 'gauche n', fmt='%.3f')
    # Chapitre 27, essentiel : simulation de Monte-Carlo de v = d / dt
    n = 20000
    d = rng.normal(0.850, 0.003, n)
    dt = rng.normal(2.47e-3, 0.02e-3, n)
    v = d / dt
    np.savetxt(DOSSIER / '27-mc-vitesse-stats.dat', [[v.mean(), v.std(ddof=1)]], fmt='%.4f', header='moyenne ecart', comments='')
    bords = np.arange(330, 358.01, 1.0)
    comptes, _ = np.histogram(v, bins=bords)
    ecrire('27-mc-vitesse-histo', [bords[:-1], comptes], 'gauche n', fmt='%.1f')
    # Exercice 15 : indice de réfraction n = sin i / sin r, angles uniformes à +/- 1 degré
    i = np.radians(rng.uniform(39.0, 41.0, n))
    r = np.radians(rng.uniform(24.0, 26.0, n))
    ind = np.sin(i) / np.sin(r)
    np.savetxt(DOSSIER / '27-mc-indice-stats.dat', [[ind.mean(), ind.std(ddof=1)]], fmt='%.5f', header='moyenne ecart', comments='')
    bords = np.arange(1.44, 1.6201, 0.01)
    comptes, _ = np.histogram(ind, bins=bords)
    ecrire('27-mc-indice-histo', [bords[:-1], comptes], 'gauche n', fmt='%.3f')


def n_stable(z):
    """Nombre de neutrons de la vallée de stabilité (relation semi-empirique Z = A / (1,98 + 0,0155 A^(2/3)))."""
    a = 2.0 * z
    for _ in range(60):
        a = z * (1.98 + 0.0155 * a ** (2 / 3))
    return a - z


def donnees_radioactivite():
    """Données du chapitre 6 : diagramme (N,Z) schématique et simulation de désintégrations aléatoires."""
    # Diagramme (N,Z) : 0 stable, 1 émetteur bêta moins, 2 émetteur bêta plus, 3 émetteur alpha
    lignes = []
    for z in range(1, 101):
        ns = n_stable(z)
        largeur = 2.0 + 0.16 * z
        for n in range(max(0, int(ns - largeur)), int(ns + largeur) + 1):
            ecart = n - ns
            if z >= 84:
                classe = 3 if abs(ecart) <= 0.45 * largeur else (1 if ecart > 0 else 2)
            elif abs(ecart) <= 0.7 + 0.012 * z:
                classe = 0
            else:
                classe = 1 if ecart > 0 else 2
            lignes.append((z, n, classe))
    tab = np.array(lignes)
    ecrire('06-diagramme-nz', [tab[:, 0], tab[:, 1], tab[:, 2]], 'Z N classe', fmt='%d')
    # Simulation : 1000 noyaux, probabilité de désintégration 0,10 par intervalle de temps
    import random
    gen = random.Random(2024)
    n0, p = 1000, 0.10
    n, ks, ns_, nt = n0, [0], [n0], [n0]
    for k in range(1, 41):
        n -= sum(1 for _ in range(n) if gen.random() < p)
        ks.append(k)
        ns_.append(n)
        nt.append(n0 * (1 - p) ** k)
    ecrire('06-simulation', [ks, ns_, np.round(nt, 1)], 'k Nsim Ntheo', fmt='%.1f')


def donnees_equilibre():
    """Données du chapitre 7 : équilibre dynamique, mutarotation du glucose, défi D07."""
    # L'essentiel : A + B = C + D, k1 = 0,020 et k-1 = 0,005 L/mol/min (K = 4), [A]0 = [B]0 = 1 mol/L
    k1, k2, dt = 0.020, 0.005, 0.01
    a = b = 1.0
    c = d = 0.0
    t_, x_, v1_, v2_ = [], [], [], []
    for i in range(int(200 / dt) + 1):
        v1, v2 = k1 * a * b, k2 * c * d
        if i % 200 == 0:
            t_.append(i * dt)
            x_.append(c)
            v1_.append(v1)
            v2_.append(v2)
        a, b = a - (v1 - v2) * dt, b - (v1 - v2) * dt
        c, d = c + (v1 - v2) * dt, d + (v1 - v2) * dt
    ecrire('07-equilibre', [t_, np.round(x_, 4), np.round(v1_, 5), np.round(v2_, 5)], 't x v1 v2', fmt='%.5f')
    # Exercice 15 : mutarotation du glucose, méthode d'Euler du programme (k1 = 0,016 et k-1 = 0,009 min-1)
    k1, k2, dt = 0.016, 0.009, 1.0
    series = []
    for a0, b0 in ((1.0, 0.0), (0.0, 1.0)):
        a, b = a0, b0
        bs = [b]
        for _ in range(240):
            v1, v2 = k1 * a, k2 * b
            a, b = a + (v2 - v1) * dt, b + (v1 - v2) * dt
            bs.append(b)
        series.append(bs)
    t = np.arange(0, 241, 1.0)
    ecrire('07-mutarotation', [t[::5], np.round(series[0][::5], 4), np.round(series[1][::5], 4)], 't b_depuis_alpha b_depuis_beta', fmt='%.4f')
    # Défi D07 : A + B = C + D, V = 1 L, nA = nB = 0,50 mol et nC = nD = 1,50 mol au départ
    k1, k2, dt = 0.020, 0.005, 0.1
    a = b = 0.50
    c = d = 1.50
    t_, a_, c_, q_ = [], [], [], []
    for i in range(int(150 / dt) + 1):
        if i % 50 == 0:
            t_.append(i * dt)
            a_.append(a)
            c_.append(c)
            q_.append(c * d / (a * b))
        v = k1 * a * b - k2 * c * d
        a, b, c, d = a - v * dt, b - v * dt, c + v * dt, d + v * dt
    ecrire('defi-07', [t_, np.round(a_, 4), np.round(c_, 4), np.round(q_, 4)], 't nA nC Qr', fmt='%.4f')


def donnees_bac():
    """Courbes des sujets type bac : titrage de l'acide lactique (sujet 1), chute d'un parachutiste (sujet 5)."""
    # Sujet 1 : 20,0 mL d'acide lactique (pKa 3,86) à 0,0545 mol/L titrés par la soude à 0,100 mol/L
    ka, ca, va, cb = 10 ** -3.86, 0.0545, 20.0, 0.100
    volumes = np.round(np.arange(0, 20.01, 0.1), 2)
    ph = []
    for v in volumes:
        na, ct = cb * v / (va + v), ca * va / (va + v)
        h = resoudre_h(lambda h: h + na - KE / h - ct * ka / (ka + h))
        ph.append(-log10(h))
    ecrire('bac-s1-ph', [volumes, np.round(ph, 3)], 'V pH', fmt='%.3f')
    # Sujet 5 : méthode d'Euler pour un parachutiste, m = 80 kg, k = 0,25 kg/m, pas de 0,1 s
    m, g, k, dt = 80.0, 9.81, 0.25, 0.1
    t, v, ts, vs = 0.0, 0.0, [0.0], [0.0]
    while t < 25 - 1e-9:
        v = v + (g - k / m * v ** 2) * dt
        t = t + dt
        ts.append(round(t, 1))
        vs.append(v)
    ecrire('bac-s5-parachute', [ts, np.round(vs, 3)], 't v', fmt='%.3f')


if __name__ == '__main__':
    donnees_bac()
    courbes_titrage()
    courbes_conductimetrie()
    courbes_cinetique()
    series_mesures()
    donnees_radioactivite()
    donnees_equilibre()
