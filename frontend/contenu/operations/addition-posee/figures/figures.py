# -*- coding: utf-8 -*-
"""Figures de « Addition posée » (calculs faits et vérifiés par poser.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from poser import PREAMBULE_EXTRA, addition  # noqa: E402,F401

FIGURES = {}

# Unités sous les unités, avec les retenues : 2 748 + 1 395 = 4 143.
FIGURES["addition_colonnes"] = addition(["2748", "1395"], entetes=True)

# Trois nombres, retenue de 2 : 1 268 + 475 + 89 = 1 832.
FIGURES["addition_trois_nombres"] = addition(["1268", "475", "89"])

# Nombres décimaux : virgules alignées, zéros ajoutés en gris.
FIGURES["addition_decimaux"] = addition(["12,5o", "3,84", "0,7o"])

# Aperçu de la carte (cadre commun à la rubrique).
from poser import apercu  # noqa: E402
FIGURES["carte_addition"] = apercu(addition(["2748", "1395"]))
