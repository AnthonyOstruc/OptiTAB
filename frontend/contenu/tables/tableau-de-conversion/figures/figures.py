# -*- coding: utf-8 -*-
"""Figures du « Tableau de conversion »."""

UNITES = ["km", "hm", "dam", "m", "dm", "cm", "mm"]
W = 1.15  # largeur d'une case (cm)


def bande():
    l = [r"\begin{tikzpicture}"]
    for i, u in enumerate(UNITES):
        x = i * W
        fond = "otNavy" if u == "m" else "otSky"
        texte = "white" if u == "m" else "otNavy"
        l.append(rf"  \fill[{fond}] ({x},0) rectangle ++({W},0.8);")
        l.append(rf"  \node[text={texte},font=\otMedium\bfseries\fontsize{{11}}{{13}}\selectfont] at ({x + W / 2},0.4) {{{u}}};")
    l.append(rf"  \draw[otNavy,line width=0.8pt] (0,0) grid[xstep={W},ystep=0.8] ({7 * W},0.8);")
    # flèches ×10 (vers la droite, au-dessus) et ÷10 (vers la gauche, en dessous)
    for i in range(6):
        x1, x2 = i * W + W / 2, (i + 1) * W + W / 2
        l.append(rf"  \draw[otGreenDark,line width=0.8pt,-{{Stealth[length=1.8mm]}}] ({x1 + 0.12},1.0) to[bend left=35] ({x2 - 0.12},1.0);")
        l.append(rf"  \draw[otOrange!85!black,line width=0.8pt,-{{Stealth[length=1.8mm]}}] ({x2 - 0.12},-0.2) to[bend left=35] ({x1 + 0.12},-0.2);")
    l.append(rf"  \node[anchor=south,text=otGreenDark] at ({3.5 * W},1.45) {{$\times 10$ à chaque case vers la droite}};")
    l.append(rf"  \node[anchor=north,text=otOrange!75!black] at ({3.5 * W},-0.65) {{$\div 10$ à chaque case vers la gauche}};")
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


def metre_carre():
    """1 m² = 100 dm² : un carré de 1 m découpé en 10 × 10 carrés de 1 dm."""
    c = 0.36
    l = [r"\begin{tikzpicture}"]
    l.append(rf"  \fill[otSky] (0,0) rectangle ({10 * c},{10 * c});")
    l.append(rf"  \fill[otGreen!45] (0,{9 * c}) rectangle ({c},{10 * c});")
    l.append(rf"  \draw[otNavy!45,line width=0.4pt] (0,0) grid[step={c}] ({10 * c},{10 * c});")
    l.append(rf"  \draw[otNavy,line width=1.1pt] (0,0) rectangle ({10 * c},{10 * c});")
    l.append(rf"  \cote[0.32]{{0,0}}{{{10 * c},0}}{{$1$ m $= 10$ dm}}".replace("{0,0}", "{(0,0)}"))
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


def metre_carre_simple():
    c = 0.36
    n = 10 * c
    return "\n".join([
        r"\begin{tikzpicture}",
        rf"  \fill[otSky] (0,0) rectangle ({n},{n});",
        rf"  \fill[otGreen!45] (0,{n - c}) rectangle ({c},{n});",
        rf"  \draw[otNavy!45,line width=0.4pt] (0,0) grid[step={c}] ({n},{n});",
        rf"  \draw[otNavy,line width=1.1pt] (0,0) rectangle ({n},{n});",
        rf"  \draw[cote] (0,-0.35) -- ({n},-0.35);",
        rf"  \node[anchor=north,inner sep=2pt] at ({n / 2},-0.42) {{$1$ m $= 10$ dm}};",
        rf"  \draw[cote] (-0.35,0) -- (-0.35,{n});",
        rf"  \node[anchor=east,inner sep=2pt,align=right] at (-0.45,{n / 2}) {{$1$ m\\$= 10$ dm}};",
        rf"  \draw[otGreenDark,line width=0.7pt] ({c / 2},{n}) -- ({c / 2},{n + 0.32});",
        rf"  \node[anchor=south,text=otGreenDark,inner sep=2pt] at ({c / 2},{n + 0.32}) {{$1$ dm$^2$}};",
        rf"  \node[anchor=west,align=left,inner sep=2pt] at ({n + 0.5},{n / 2 - 0.3}) {{$1$ m$^2$\\$= 10 \times 10$ dm$^2$\\$= 100$ dm$^2$}};",
        r"\end{tikzpicture}",
    ])


FIGURES = {"bande_unites": bande(), "metre_carre": metre_carre_simple()}

TOLERE = {"bande_unites": "« m » écrit en blanc sur la case bleue pleine de l’unité de référence : le fond plein est pris pour un trait (vérifié à l’œil)"}
