# -*- coding: utf-8 -*-
"""Figure de la page « Les ions : liste, formules et tests » : tests d'identification.

    python frontend/cours/format_v1/outils/figures_livre.py frontend/contenu/physique-chimie/ions-courants --planche --jobs 1

Cinq tubes à essai : ions cuivre II, fer II et fer III avec la soude (précipités
bleu, vert, rouille), ions chlorure avec le nitrate d'argent et ions sulfate avec
le chlorure de baryum (précipités blancs). Tubes et précipités dessinés en
chemins ; textes dans des nœuds sans fond (contrôle des chevauchements).
"""

NOTE = r"\otMedium\fontsize{9.5}{11.5}\selectfont"
PETIT = r"\otRegular\fontsize{9}{11}\selectfont"

PREAMBULE_EXTRA = r"""
\definecolor{pBleu}{HTML}{3A7BD5}
\definecolor{sBleu}{HTML}{D6E6FA}
\definecolor{pVert}{HTML}{5E8C4A}
\definecolor{sVert}{HTML}{E8F2DD}
\definecolor{pRouille}{HTML}{B5561E}
\definecolor{sRouille}{HTML}{FBE7CF}
\definecolor{pBlanc}{HTML}{FFFFFF}
\definecolor{sIncolore}{HTML}{E4ECF7}
"""

R = 0.3          # rayon du fond du tube
HAUT = 2.7       # haut du tube
NIVEAU = 1.85    # surface du liquide
PRECIP = 0.78    # haut du précipité


def tube(x, solution, precipite, contour_precipite="otInk!35"):
    forme = (f"({x - R},{HAUT}) -- ({x - R},{R}) arc[start angle=180, end angle=360, radius={R}] "
             f"-- ({x + R},{HAUT})")
    s = rf"  \begin{{scope}}\clip {forme} -- cycle;" + "\n"
    s += rf"    \fill[{solution}] ({x - 1},0) rectangle ({x + 1},{NIVEAU});" + "\n"
    s += rf"    \fill[{precipite}] ({x - 1},0) rectangle ({x + 1},{PRECIP});" + "\n"
    # quelques flocons au-dessus du dépôt
    for dx, dy, r in [(-0.12, 0.95, 0.045), (0.1, 1.08, 0.04), (-0.02, 1.25, 0.035), (0.14, 0.9, 0.035)]:
        s += rf"    \fill[{precipite},draw={contour_precipite},line width=0.3pt] ({x + dx},{dy}) circle ({r});" + "\n"
    s += r"  \end{scope}" + "\n"
    s += rf"  \draw[{contour_precipite},line width=0.4pt] ({x - R},{PRECIP}) -- ({x + R},{PRECIP});" + "\n"
    s += rf"  \draw[otInk,line width=0.9pt,line join=round] {forme};" + "\n"
    s += rf"  \draw[otInk,line width=0.9pt] ({x - R - 0.07},{HAUT}) -- ({x + R + 0.07},{HAUT});" + "\n"
    return s


def legende(x, ion, couleur):
    return (rf"  \node[anchor=north,inner sep=0pt,text=otInk] at ({x},-0.15) {{${ion}$}};" + "\n"
            + rf"  \node[anchor=north,inner sep=0pt,font={PETIT},text=otMuted] at ({x},-0.72) {{{couleur}}};" + "\n")


def entete(x, texte):
    return rf"  \node[anchor=south,align=center,inner sep=0pt,font={NOTE},text=otNavy] at ({x},{HAUT + 0.55}) {{{texte}}};" + "\n"


X = [0, 1.55, 3.1, 5.0, 7.25]
TESTS_IONS = ("\n" + chr(92) + "begin{tikzpicture}\n"
              + tube(X[0], "sBleu", "pBleu") + tube(X[1], "sVert", "pVert") + tube(X[2], "sRouille", "pRouille")
              + tube(X[3], "sIncolore", "pBlanc", "otInk!45") + tube(X[4], "sIncolore", "pBlanc", "otInk!45")
              # accolade (trait) commune aux trois tests à la soude
              + rf"  \draw[otNavy!60,line width=0.7pt] ({X[0] - 0.35},{HAUT + 0.3}) -- ({X[0] - 0.35},{HAUT + 0.45}) -- ({X[2] + 0.35},{HAUT + 0.45}) -- ({X[2] + 0.35},{HAUT + 0.3});" + "\n"
              + entete(X[1], "avec la soude")
              + entete(X[3], "nitrate" + chr(92) * 2 + "d’argent")
              + entete(X[4], "chlorure" + chr(92) * 2 + "de baryum")
              + legende(X[0], r"\mathrm{Cu^{2+}}", "bleu") + legende(X[1], r"\mathrm{Fe^{2+}}", "vert")
              + legende(X[2], r"\mathrm{Fe^{3+}}", "rouille") + legende(X[3], r"\mathrm{Cl^{-}}", "blanc")
              + legende(X[4], r"\mathrm{SO_4^{2-}}", "blanc")
              + chr(92) + "end{tikzpicture}")

FIGURES = {"tests_ions": TESTS_IONS}
