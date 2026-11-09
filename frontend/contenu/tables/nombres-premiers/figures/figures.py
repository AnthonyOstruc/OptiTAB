# -*- coding: utf-8 -*-
"""Figure « Nombres premiers » : crible d'Ératosthène de 1 à 100."""

C = 0.72


def premier(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def crible():
    l = [r"\begin{tikzpicture}"]
    for k in range(100):
        n = k + 1
        x, y = (k % 10) * C, -(k // 10) * C
        if premier(n):
            l.append(rf"  \fill[otGreen!30] ({x},{y}) rectangle ++({C},{-C});")
            l.append(rf"  \node[text=otGreenDark,font=\otMedium\bfseries\fontsize{{10}}{{12}}\selectfont] at ({x + C / 2},{y - C / 2}) {{{n}}};")
        else:
            l.append(rf"  \node[text=otMuted!75,font=\otRegular\fontsize{{10}}{{12}}\selectfont] at ({x + C / 2},{y - C / 2}) {{{n}}};")
    l.append(rf"  \draw[otRule,line width=0.4pt] (0,0) grid[step={C}] ({10 * C},{-10 * C});")
    l.append(rf"  \draw[otNavy,line width=0.9pt] (0,0) rectangle ({10 * C},{-10 * C});")
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


FIGURES = {"crible_100": crible()}
