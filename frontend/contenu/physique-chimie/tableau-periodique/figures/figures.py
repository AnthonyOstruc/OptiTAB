# -*- coding: utf-8 -*-
"""Figure de la page « Tableau périodique des éléments » : lire une case.

    python frontend/cours/format_v1/outils/figures_livre.py frontend/contenu/physique-chimie/tableau-periodique --planche --jobs 1

L'aperçu du PDF (apercu_tableau_periodique.png) est produit par ../generer.py.
Cadre dessiné en chemin et textes dans des nœuds sans fond : le contrôle des
chevauchements ne voit ainsi que du texte.
"""

NOTE = r"\otMedium\fontsize{10}{12}\selectfont"
RAPPEL = r"otMuted,line width=0.6pt"


def rappel(x1, x2, y, texte):
    return (rf"  \draw[{RAPPEL}] ({x1},{y}) -- ({x2},{y});" + "\n"
            + rf"  \node[anchor=west,inner sep=1pt,font={NOTE},text=otInk] at ({x2 + 0.08},{y}) {{{texte}}};" + "\n")


CASE_ELEMENT = (r"""
\begin{tikzpicture}
  \definecolor{nonMetal}{HTML}{D9E7FF}
  \draw[otNavy!60,fill=nonMetal,line width=1pt,rounded corners=6pt] (0,0) rectangle (3.0,3.4);
  \node[anchor=north west,inner sep=0pt,text=otInk,font=\otMedium\fontsize{15}{16}\selectfont] at (0.3,3.15) {6};
  \node[inner sep=0pt,text=otInk,font=\otMedium\bfseries\fontsize{46}{48}\selectfont] at (1.5,1.95) {C};
  \node[inner sep=0pt,text=otInk,font=\otMedium\fontsize{12}{13}\selectfont] at (1.5,0.92) {carbone};
  \node[inner sep=0pt,text=otInk,font=\otRegular\fontsize{12}{13}\selectfont] at (1.5,0.4) {12,0};
"""
    + rappel(0.75, 3.55, 2.95, r"numéro atomique $Z$")
    + rappel(2.25, 3.55, 1.95, "symbole")
    + rappel(2.4, 3.55, 0.92, "nom")
    + rappel(2.0, 3.55, 0.4, "masse molaire (g/mol)")
    + r"\end{tikzpicture}")

FIGURES = {"case_element": CASE_ELEMENT}
