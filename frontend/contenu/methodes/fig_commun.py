# -*- coding: utf-8 -*-
"""Outils communs aux figures de la rubrique « Méthodes de calcul ».

    import sys; from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from fig_commun import *
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  boite/.style={draw=otNavy,line width=.8pt,rounded corners=3pt,fill=otSky,minimum height=.8cm,minimum width=1.6cm,inner sep=4pt,font=\fontsize{12}{14}\selectfont},
  fleche/.style={otGreenDark,line width=1pt,-{Stealth[length=2.4mm]}},
  saut/.style={otGreenDark,line width=1pt,-{Stealth[length=2.2mm]}},
  etiq/.style={font=\fontsize{10.5}{12}\selectfont,inner sep=2pt},
  note/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted,inner sep=1pt},
  grad/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otInk,inner sep=1pt},
  accol/.style={line width=.7pt,decorate,decoration={brace,amplitude=4.5pt}},
}
"""


def f(v):
    return ("%.4f" % float(v)).rstrip("0").rstrip(".")


def tikz(L):
    return "\\begin{tikzpicture}\n" + "\n".join(L) + "\n\\end{tikzpicture}"


def carte(L, larg=6.0, haut=3.75):
    """Aperçu des cartes : contenu centré dans un cadre fixe (même échelle partout)."""
    return tikz([r"\begin{scope}[local bounding box=F]"] + L + [
        r"\end{scope}", r"\pgfresetboundingbox",
        r"\path ($(F.center)+(%s,%s)$) rectangle ($(F.center)+(%s,%s)$);" % (f(-larg / 2), f(-haut / 2), f(larg / 2), f(haut / 2))])
