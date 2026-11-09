# -*- coding: utf-8 -*-
"""Figure « Fractions, décimaux, pourcentages » : disques partagés."""

R = 0.85
CAS = [  # (parts colorées, parts totales, fraction, décimal, pourcentage)
    (1, 2, r"\dfrac{1}{2}", "0{,}5", r"50\,\%"),
    (1, 4, r"\dfrac{1}{4}", "0{,}25", r"25\,\%"),
    (3, 4, r"\dfrac{3}{4}", "0{,}75", r"75\,\%"),
    (1, 3, r"\dfrac{1}{3}", r"0{,}33\ldots", r"\approx 33\,\%"),
]


def disques():
    l = [r"\begin{tikzpicture}"]
    for i, (k, n, frac, dec, pct) in enumerate(CAS):
        cx = i * 2.35
        # parts colorées à partir de midi, dans le sens des aiguilles d'une montre
        if k:
            debut, fin = 90, 90 - 360 * k / n
            l.append(rf"  \fill[otGreen!45] ({cx},0) -- ++({debut}:{R}) arc ({debut}:{fin}:{R}) -- cycle;")
        for j in range(n):
            a = 90 - 360 * j / n
            l.append(rf"  \draw[otNavy,line width=0.7pt] ({cx},0) -- ++({a:.2f}:{R});")
        l.append(rf"  \draw[otNavy,line width=1.1pt] ({cx},0) circle ({R});")
        l.append(rf"  \node[anchor=north,inner sep=2pt] at ({cx},{-R - 0.12}) {{${frac} = {dec}$}};")
        l.append(rf"  \node[anchor=north,inner sep=2pt,text=otGreenDark] at ({cx},{-R - 1.12}) {{${pct}$}};")
    l.append(r"\end{tikzpicture}")
    return "\n".join(x for x in l if x)


FIGURES = {"disques_fractions": disques()}
