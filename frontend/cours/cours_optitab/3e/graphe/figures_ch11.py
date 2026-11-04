# -*- coding: utf-8 -*-
"""Figures du chapitre 11 (Probabilités) — 3ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import arbre2, new_fig, BLUE, ORANGE, GREEN, DARK, DIR_COURS, DIR_EXOS, ROOT
import matplotlib.pyplot as plt
import matplotlib.patches as mp

# Cours — arbre de deux pièces
arbre2(os.path.join(DIR_COURS, "probabilites_3e_arbre_pieces.png"),
       [("P", "1/2"), ("F", "1/2")],
       [[("P   → PP", "1/2"), ("F   → PF", "1/2")],
        [("P   → FP", "1/2"), ("F   → FF", "1/2")]])

# Exercice — deux pièces (même arbre)
arbre2(os.path.join(DIR_EXOS, "probabilites_3e_pieces.png"),
       [("P", "1/2"), ("F", "1/2")],
       [[("P   → PP", "1/2"), ("F   → PF", "1/2")],
        [("P   → FP", "1/2"), ("F   → FF", "1/2")]])

# Avec remise : 3 R, 2 B
arbre2(os.path.join(DIR_EXOS, "probabilites_3e_remise.png"),
       [("R", "3/5"), ("B", "2/5")],
       [[("R   → RR", "3/5"), ("B   → RB", "2/5")],
        [("R   → BR", "3/5"), ("B   → BB", "2/5")]])

# Sans remise : 3 R, 2 B
arbre2(os.path.join(DIR_EXOS, "probabilites_3e_sans_remise.png"),
       [("R", "3/5"), ("B", "2/5")],
       [[("R   → RR", "2/4"), ("B   → RB", "2/4")],
        [("R   → BR", "3/4"), ("B   → BB", "1/4")]])


def tableau_des():
    """Tableau à double entrée des sommes de deux dés, cases de somme 7 surlignées."""
    fig, ax = new_fig(6.6, 6.0)
    n = 6
    for i in range(n + 1):
        for j in range(n + 1):
            x, y = j, n - i
            if i == 0 and j == 0:
                txt, face = "+", "#d6eafc"
            elif i == 0:
                txt, face = str(j), "#d6eafc"
            elif j == 0:
                txt, face = str(i), "#fdebd0"
            else:
                s = i + j
                txt = str(s)
                face = "#c8e6c9" if s == 7 else "white"
            ax.add_patch(mp.Rectangle((x, y), 1, 1, facecolor=face,
                                      edgecolor=DARK, lw=1.2))
            bold = "bold" if (i == 0 or j == 0 or (i and j and i + j == 7)) else "normal"
            col = GREEN if (i and j and i + j == 7) else DARK
            ax.text(x + 0.5, y + 0.5, txt, ha="center", va="center",
                    fontsize=13, color=col, fontweight=bold)
    ax.text(3.5, 7.35, "dé 2", ha="center", fontsize=12, color=BLUE, fontweight="bold")
    ax.text(-0.45, 3.0, "dé 1", va="center", fontsize=12, color=ORANGE,
            fontweight="bold", rotation=90)
    ax.set_xlim(-0.8, 7.2)
    ax.set_ylim(-0.2, 7.7)
    ax.set_aspect("equal")
    ax.axis("off")
    path = os.path.join(DIR_EXOS, "probabilites_3e_des.png")
    fig.savefig(path, dpi=175, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", os.path.relpath(path, ROOT))


tableau_des()
print("Figures chapitre 11 : OK")
