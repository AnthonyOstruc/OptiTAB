"""Calcule les tangentes parallèles et le point d'équivalence des courbes de titrage pH-métrique.

Pour une pente s choisie, on cherche de part et d'autre du saut le point où dpH/dV = s ;
les deux tangentes et la droite médiane (équidistante) sont imprimées sous la forme y = s x + b.
Lancer : python -I -X utf8 verifications/tangentes.py
"""
from pathlib import Path
import numpy as np

DONNEES = Path(__file__).resolve().parent.parent / 'figures' / 'donnees'


def tangentes(nom, pente, ve_attendu):
    data = np.loadtxt(DONNEES / f'{nom}.dat', skiprows=1)
    v, ph = data[:, 0], data[:, 1]
    d = np.gradient(ph, v)
    signe = 1 if ph[-1] > ph[0] else -1
    s = signe * abs(pente)
    i_max = np.argmax(np.abs(d))
    # avant le saut : dernier point où |d| <= |s| ; après : premier point où |d| <= |s|
    avant = [i for i in range(1, i_max) if abs(d[i]) <= abs(s)]
    apres = [i for i in range(i_max + 1, len(v) - 1) if abs(d[i]) <= abs(s)]
    i1, i2 = avant[-1], apres[0]
    b1 = ph[i1] - s * v[i1]
    b2 = ph[i2] - s * v[i2]
    bm = (b1 + b2) / 2
    # intersection de la médiane avec la courbe
    f = ph - (s * v + bm)
    k = np.where(np.sign(f[:-1]) != np.sign(f[1:]))[0]
    k = k[np.argmin(np.abs(v[k] - v[i_max]))]
    ve = v[k] - f[k] * (v[k + 1] - v[k]) / (f[k + 1] - f[k])
    phe = np.interp(ve, v, ph)
    print(f"{nom}: pente {s:+.3f} ; tangente 1 en V={v[i1]:.2f} : b1={b1:.3f} ; tangente 2 en V={v[i2]:.2f} : "
          f"b2={b2:.3f} ; médiane b={bm:.3f} ; VE={ve:.2f} mL (attendu {ve_attendu}) ; pH_E={phe:.2f} ; "
          f"dérivée max en V={v[i_max]:.2f}")
    assert abs(ve - ve_attendu) < 0.25, nom
    return s, b1, b2, bm, ve, phe


if __name__ == '__main__':
    tangentes('03-ethanoique-ph', 0.135, 20.0)
    tangentes('03-hcl-naoh-ph', 0.20, 20.0)
    tangentes('03-vinaigre-ph', 0.30, 10.1)
    tangentes('03-deboucheur-ph', 0.25, 21.6)
    tangentes('03-aspirine-ph', 0.20, 13.8)
    tangentes('03-succinique-ph', 0.15, 25.4)
