# -*- coding: utf-8 -*-
"""Figures de « Division posée » (calculs faits et vérifiés par poser.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from poser import PREAMBULE_EXTRA, division, ensemble, multiples, analyse  # noqa: E402,F401

FIGURES = {}

# Vocabulaire : 1 475 ÷ 6 = 245, reste 5.
FIGURES["division_vocabulaire"] = division("1475", 6, noms=True)[0]

# Déroulé pas à pas de 1 475 ÷ 6 (même cadre à chaque étape).
ETAPE = dict(slots="cdu", egalite="", cadre=True)
FIGURES["division_etape_1"] = division("1475", 6, jusqua=-1, accolade="on prend 14", **ETAPE)[0]
FIGURES["division_etape_2"] = division("1475", 6, jusqua=0, actif=0, **ETAPE)[0]
FIGURES["division_etape_3"] = division("1475", 6, jusqua=1, actif=1, abaisse=1, **ETAPE)[0]
FIGURES["division_etape_4"] = division("1475", 6, jusqua=2, actif=2, abaisse=2, **ETAPE)[0]

# Le zéro au quotient : 3 624 ÷ 6 = 604.
FIGURES["division_zero"] = division("3624", 6, slots="cdu")[0]

# Diviseur à deux chiffres : 9 782 ÷ 23 = 425, reste 7, avec la table des multiples.
_ch, _k, _nz, _et, _q, _qt, _r = analyse("9782", 23)
FIGURES["division_deux_chiffres"] = division(
    "9782", 23, extra=multiples(23, x0=4.3, y0=-.05, surligne=tuple(x[2] for x in _et), RH=.47))[0]

# Méthode longue et méthode courte côte à côte (1 475 ÷ 6).
FIGURES["division_courte"] = ensemble(
    [(division("1475", 6, egalite="")[0], 0), (division("1475", 6, courte=True, egalite="")[0], 4.6)],
    titres=[("méthode longue", 1.35), ("méthode courte", 1.35)])

# Quotient décimal : 47 ÷ 4 = 11,75 et 18,6 ÷ 4 = 4,65.
FIGURES["division_decimale"] = ensemble(
    [(division("47", 4, zeros=2)[0], 0), (division("18,6", 4, zeros=1)[0], 4.8)],
    titres=[("47 ÷ 4", 1.2), ("18,6 ÷ 4", 1.2)])

# Division qui ne s'arrête pas : 10 ÷ 3 = 3,333…
FIGURES["division_infinie"] = division("10", 3, zeros=3, suite=True,
                                       egalite="le reste 1 revient sans fin : $10 \\div 3 = 3{,}333\\ldots$")[0]

# France / pays anglophones : la même division, deux écritures.
FIGURES["division_anglaise"] = ensemble(
    [(division("1475", 6, egalite="")[0], 0), (division("1475", 6, style="anglais", egalite="")[0], 5.0)],
    titres=[("en France", 1.35), ("Royaume-Uni, États-Unis", 1.15)], ytitre=1.45)

# Aperçu de la carte (cadre commun à la rubrique) : 156 ÷ 6 = 26.
from poser import apercu  # noqa: E402
FIGURES["carte_division"] = apercu(division("156", 6, egalite="")[0])
