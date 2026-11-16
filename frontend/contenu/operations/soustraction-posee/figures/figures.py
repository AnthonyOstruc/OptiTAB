# -*- coding: utf-8 -*-
"""Figures de « Soustraction posée » (calculs faits et vérifiés par poser.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from poser import PREAMBULE_EXTRA, soustraction, ensemble  # noqa: E402,F401

FIGURES = {}

# Sans retenue : 4 869 − 2 345 = 2 524.
FIGURES["soustraction_simple"] = soustraction("4869", "2345", methode=None, entetes=True)

# 642 − 275 = 367 par les deux méthodes.
FIGURES["soustraction_cassage"] = soustraction("642", "275", methode="cassage")
FIGURES["soustraction_compensation"] = soustraction("642", "275", methode="compensation")

# Avec un zéro en haut : 503 − 278 = 225, les deux méthodes côte à côte.
FIGURES["soustraction_zero"] = ensemble(
    [(soustraction("503", "278", methode="cassage"), 0), (soustraction("503", "278", methode="compensation"), 4.2)],
    titres=[("par cassage", -.65), ("par compensation", -.65)], ytitre=1.35)

# Nombres décimaux : 23,5 − 8,76 = 14,74.
FIGURES["soustraction_decimaux"] = soustraction("23,5o", "8,76", methode="compensation")

# Les barres de la méthode par cassage traversent volontairement le chiffre barré.
TOLERE = {
    "soustraction_cassage": "chiffre barré de la méthode par cassage",
    "soustraction_zero": "chiffres barrés de la méthode par cassage",
}

# Aperçu de la carte (cadre commun à la rubrique).
from poser import apercu  # noqa: E402
FIGURES["carte_soustraction"] = apercu(soustraction("642", "275", methode="compensation"))
