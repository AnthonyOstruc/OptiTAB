# -*- coding: utf-8 -*-
"""Figure des « Chiffres romains » : cadran d'horloge."""

HEURES = ["XII", "I", "II", "III", "IIII", "V", "VI", "VII", "VIII", "IX", "X", "XI"]


def cadran():
    R = 2.3
    l = [r"\begin{tikzpicture}"]
    l.append(rf"  \fill[otSky!60] (0,0) circle ({R});")
    l.append(rf"  \draw[otNavy,line width=1.6pt] (0,0) circle ({R});")
    for m in range(60):
        a = 90 - 6 * m
        long_ = 0.22 if m % 5 == 0 else 0.1
        epais = 1.0 if m % 5 == 0 else 0.4
        l.append(rf"  \draw[otNavy,line width={epais}pt] ({a}:{R - 0.06}) -- ({a}:{R - 0.06 - long_});")
    for h, txt in enumerate(HEURES):
        a = 90 - 30 * h
        l.append(rf"  \node[text=otNavy,font=\otMedium\bfseries\fontsize{{11}}{{13}}\selectfont] at ({a}:{R - 0.62}) {{{txt}}};")
    # aiguilles : 10 h 10
    l.append(r"  \draw[otInk,line width=2.2pt,line cap=round] (0,0) -- (150:1.0);")
    l.append(r"  \draw[otInk,line width=1.4pt,line cap=round] (0,0) -- (30:1.45);")
    l.append(r"  \fill[otOrange!85!black] (0,0) circle (0.09);")
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


FIGURES = {"cadran_horloge": cadran()}
