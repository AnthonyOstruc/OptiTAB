# -*- coding: utf-8 -*-
"""Figure de la table « Alphabet grec » : les 24 minuscules avec leur nom (6 × 4)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lettres import LETTRES  # noqa: E402

CX, CY = 1.32, 1.3
COLS = 6


def grille():
    l = [r"\begin{tikzpicture}"]
    for k, (nom, _, mini, _, _) in enumerate(LETTRES):
        i, j = k % COLS, k // COLS
        x, y = i * CX, -j * CY
        fond = "otSky" if (i + j) % 2 == 0 else "white"
        l.append(rf"  \fill[{fond}] ({x:.3f},{y:.3f}) rectangle ({x + CX:.3f},{y - CY:.3f});")
        l.append(rf"  \node[text=otNavy,font=\LARGE] at ({x + CX / 2:.3f},{y - 0.5:.3f}) {{${mini}$}};")
        l.append(rf"  \node[text=otMuted!85!black,font=\footnotesize] at ({x + CX / 2:.3f},{y - 1.03:.3f}) {{{nom}}};")
    l.append(rf"  \draw[otNavy,line width=0.9pt] (0,0) rectangle ({COLS * CX:.3f},{-4 * CY:.3f});")
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


FIGURES = {"lettres_grecques": grille()}
