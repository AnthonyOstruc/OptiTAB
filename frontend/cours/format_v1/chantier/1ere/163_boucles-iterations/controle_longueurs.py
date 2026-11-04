# -*- coding: utf-8 -*-
"""Lignes de code trop longues pour un téléphone.

    python controle_longueurs.py [max_bloc=30] [max_en_ligne=24]
"""
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
MAX_BLOC = int(sys.argv[1]) if len(sys.argv) > 1 else 30
MAX_LIGNE = int(sys.argv[2]) if len(sys.argv) > 2 else 24
for nom in ("cours_151.txt", "fiche_61.txt", "exercices.txt"):
    t = (ICI / nom).read_text(encoding="utf-8")
    blocs = list(re.finditer(r"^[ \t]*```(python|console)[ \t]*\r?\n(.*?)^[ \t]*```", t, flags=re.M | re.S))
    for m in blocs:
        for l in m.group(2).splitlines():
            if len(l.rstrip()) > MAX_BLOC:
                print(f"{nom} l.{t[:m.start()].count(chr(10)) + 1} bloc ({len(l.rstrip())}) : {l.rstrip()}")
    hors = re.sub(r"^[ \t]*```(python|console)[ \t]*\r?\n.*?^[ \t]*```", "", t, flags=re.M | re.S)
    for m in re.finditer(r"(?<!`)`([^`\n]+)`(?!`)", hors):
        if len(m.group(1)) > MAX_LIGNE:
            print(f"{nom} en ligne ({len(m.group(1))}) : {m.group(1)}")
    print(nom, len(blocs), "blocs de code")
