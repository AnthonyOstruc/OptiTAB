# -*- coding: utf-8 -*-
"""Figure « Puissances de 10 et préfixes » : échelle des préfixes, de pico à téra."""

PREFIXES = [("p", "-12"), ("n", "-9"), (r"\mupmu", "-6"), ("m", "-3"), ("unité", "0"), ("k", "3"), ("M", "6"), ("G", "9"), ("T", "12")]
W = 0.98


def echelle():
    l = [r"\begin{tikzpicture}"]
    for i, (p, e) in enumerate(PREFIXES):
        x = i * W
        fond = "otGreen!35" if e == "0" else "otSky"
        l.append(rf"  \fill[{fond}] ({x},0) rectangle ++({W},1.1);")
        # symboles en police de texte droite (µ droit, comme dans µm) ; « unité » plus petit
        taille = r"\small" if p == "unité" else r"\large"
        texte = "µ" if p == r"\mupmu" else p
        l.append(rf"  \node[text=otNavy] at ({x + W / 2},0.74) {{{taille} {texte}}};")
        l.append(rf"  \node[text=otMuted!80!black] at ({x + W / 2},0.3) {{\footnotesize$10^{{{e}}}$}};")
    l.append(rf"  \draw[otNavy,line width=0.8pt] (0,0) grid[xstep={W},ystep=1.1] ({len(PREFIXES) * W},1.1);")
    for i in range(len(PREFIXES) - 1):
        x1, x2 = i * W + W / 2, (i + 1) * W + W / 2
        l.append(rf"  \draw[otGreenDark,line width=0.8pt,-{{Stealth[length=1.8mm]}}] ({x1 + 0.1},1.3) to[bend left=35] ({x2 - 0.1},1.3);")
    l.append(rf"  \node[anchor=south,text=otGreenDark] at ({len(PREFIXES) * W / 2},1.7) {{$\times 1\,000$ à chaque case vers la droite}};")
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


FIGURES = {"echelle_prefixes": echelle()}
