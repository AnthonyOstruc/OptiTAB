# -*- coding: utf-8 -*-
"""Figure de la table « Symboles mathématiques » : 12 symboles courants (4 × 3) et leur lecture."""

SYMBOLES = [
    (r"\forall", "pour tout"), (r"\exists", "il existe"), (r"\in", "appartient à"),
    (r"\subset", "est inclus dans"), (r"\Rightarrow", "implique"), (r"\Leftrightarrow", "équivaut à"),
    (r"\Sigma", "somme"), (r"\int", "intégrale"), (r"\infty", "infini"),
    (r"\approx", "environ égal"), (r"\neq", "différent de"), (r"\sqrt{\ }", "racine carrée"),
]
CX, CY = 1.95, 1.35
COLS = 4


def grille():
    l = [r"\begin{tikzpicture}"]
    for k, (sym, lecture) in enumerate(SYMBOLES):
        i, j = k % COLS, k // COLS
        x, y = i * CX, -j * CY
        fond = "otSky" if (i + j) % 2 == 0 else "white"
        l.append(rf"  \fill[{fond}] ({x:.3f},{y:.3f}) rectangle ({x + CX:.3f},{y - CY:.3f});")
        l.append(rf"  \node[text=otNavy,font=\LARGE] at ({x + CX / 2:.3f},{y - 0.52:.3f}) {{${sym}$}};")
        l.append(rf"  \node[text=otMuted!85!black,font=\footnotesize] at ({x + CX / 2:.3f},{y - 1.08:.3f}) {{{lecture}}};")
    l.append(rf"  \draw[otNavy,line width=0.9pt] (0,0) rectangle ({COLS * CX:.3f},{-3 * CY:.3f});")
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


FIGURES = {"symboles": grille()}
