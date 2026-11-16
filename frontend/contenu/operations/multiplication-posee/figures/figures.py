# -*- coding: utf-8 -*-
"""Figures de « Multiplication posée » (calculs faits et vérifiés par poser.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from poser import PREAMBULE_EXTRA, multiplication, jalousie, ensemble  # noqa: E402,F401

FIGURES = {}

# Par un chiffre, avec les retenues : 347 × 6 = 2 082.
FIGURES["multiplication_un_chiffre"] = multiplication("347", "6", retenues=True)[0]

# Par deux chiffres : 347 × 26 = 9 022 (347 × 6 puis 347 × 20).
FIGURES["multiplication_deux_chiffres"] = multiplication("347", "26")[0]

# Par trois chiffres : 425 × 132 = 56 100.
FIGURES["multiplication_trois_chiffres"] = multiplication("425", "132")[0]

# Nombres décimaux : 4,25 × 3,6 = 15,3.
FIGURES["multiplication_decimaux"] = multiplication(
    "4,25", "3,6", comptes=("2 chiffres après la virgule", "1 chiffre après la virgule", "2 + 1 = 3 chiffres"))[0]

# Méthode par jalousie (per gelosia) : 347 × 26 = 9 022.
FIGURES["multiplication_jalousie"] = jalousie("347", "26", s=1.05)[0]

# Aperçu de la carte (cadre commun à la rubrique).
from poser import apercu  # noqa: E402
FIGURES["carte_multiplication"] = apercu(multiplication("347", "26", notes=False)[0])
