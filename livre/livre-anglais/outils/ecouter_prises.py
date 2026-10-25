"""Affiche ce que la reconnaissance vocale entend pour les prises mémorisées contenant un motif.

  python -X utf8 outils/ecouter_prises.py "Chloé" "Filou"
"""
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import audio as A  # noqa: E402
from oreille import conforme, entendre, via_mp3  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
prises = json.loads((RACINE / "build" / "prises.json").read_text(encoding="utf-8"))
cache = RACINE / "build" / "cache-voix"
for cle, (texte, vitesse) in prises.items():
    if not any(m in cle for m in sys.argv[1:]):
        continue
    perso = cle.split("|")[0]
    s = A.synth(perso, texte, vitesse, cache)
    r = entendre(via_mp3(A.normaliser(np.concatenate([A.silence(0.3), s, A.silence(0.3)])), A.SR))
    print(f"{'OK ' if conforme(texte, r) else '!! '} {perso:8} v={vitesse}  « {texte} »  →  « {r} »")
