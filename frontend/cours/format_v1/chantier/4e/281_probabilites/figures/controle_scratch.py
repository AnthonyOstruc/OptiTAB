# -*- coding: utf-8 -*-
"""Contrôle « aucun texte sur un trait » des figures de blocs Scratch.

Dans les vraies figures, le texte des blocs est écrit sur le fond coloré du bloc : le
détecteur de figures_livre.py prend ce fond pour un trait (d'où les TOLERE). Ici, chaque
figure de blocs est recompilée avec SCRATCH_CONTROLE=1 : fonds blancs, textes noirs,
contours conservés (contours des cases foncés). Le détecteur vérifie alors réellement
qu'aucun texte ne touche le contour d'un bloc, d'une case, d'un menu ou d'un hexagone.

    python controle_scratch.py            (depuis ce dossier figures/)

Sortie : 0 erreur attendue. Fichiers de travail : build/controle/.
"""
import os
import sys
from pathlib import Path

os.environ["SCRATCH_CONTROLE"] = "1"
ICI = Path(__file__).resolve().parent
OUTILS = ICI.parents[3] / "outils"
sys.path.insert(0, str(OUTILS))
sys.path.insert(0, str(ICI))

import figures_livre as FL  # noqa: E402
import figures as FG        # noqa: E402

noms = [n for n in FG.TOLERE if n in FG.FIGURES] if len(sys.argv) < 2 else sys.argv[1:]
build = ICI / "build" / "controle"
sortie = build / "png"
erreurs = 0
from concurrent.futures import ThreadPoolExecutor  # noqa: E402

with ThreadPoolExecutor(max_workers=4) as pool:
    res = list(pool.map(lambda n: FL.compiler_un(n, FG.FIGURES[n], build, sortie, None, FG.PREAMBULE_EXTRA, None), noms))
for nom, bon, msgs in res:
    vraies = [m for m in msgs if not m.startswith("(avertissement)") and "large" not in m]
    if not bon and vraies:
        erreurs += 1
        print("✗ %s : %s" % (nom, " | ".join(vraies)))
print("%d figure(s) de blocs contrôlée(s), %d en erreur" % (len(noms), erreurs))
sys.exit(1 if erreurs else 0)
